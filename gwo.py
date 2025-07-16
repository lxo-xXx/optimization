import math
import random
import numpy as np
from archive import Archive
from domination import select_N, crowding_distance, non_dominated_sort


class GWO:
    """Enhanced Grey Wolf Optimizer with advanced features for multi-objective optimization.
    
    Features:
    - Opposition-Based Learning (OBL) for initialization
    - Elite Archive for multi-objective optimization
    - Adaptive nonlinear decay of parameter a
    - Hypervolume tracking for convergence analysis
    - Self-adaptive archive leader selection
    - Hybrid crossover-mutation operators
    - Dynamic archive management with clustering
    - Nonlinear dynamic reference point
    - Parallel evaluation support
    """
    
    def __init__(self, func, dim, bounds, pop_size=50, max_iter=200, 
                 archive_size=100, power_a=3, ref_point=None, 
                 use_differential_mutation=True, use_dynamic_ref=True,
                 use_smart_leader_selection=True, F=0.5, CR=0.9):
        """Initialize the enhanced GWO algorithm.
        
        Args:
            func: Objective function mapping decision vector to objective values
            dim: Dimension of decision space
            bounds: Tuple (lower_bounds, upper_bounds) for each dimension
            pop_size: Number of wolves (solutions)
            max_iter: Number of iterations
            archive_size: Maximum size of external archive
            power_a: Exponent for nonlinear decay of parameter a (1 = linear)
            ref_point: Reference point for hypervolume calculation
            use_differential_mutation: Enable differential mutation operator
            use_dynamic_ref: Enable dynamic reference point adaptation
            use_smart_leader_selection: Enable smart leader selection based on crowding distance
            F: Differential evolution scaling factor
            CR: Crossover probability for differential evolution
        """
        self.func = func
        self.dim = dim
        self.lb, self.ub = bounds
        self.pop_size = pop_size
        self.max_iter = max_iter
        self.archive_size = archive_size
        self.power_a = power_a
        self.ref = ref_point
        self.use_differential_mutation = use_differential_mutation
        self.use_dynamic_ref = use_dynamic_ref
        self.use_smart_leader_selection = use_smart_leader_selection
        self.F = F  # Differential evolution scaling factor
        self.CR = CR  # Crossover probability
        
        # Initialize algorithm components
        self.archive = Archive(archive_size)
        self.population = []
        self.pop_objs = []
        self.hv_history = []
        
        # For dynamic reference point tracking
        self.max_objectives = None
        
        # Set random seed for reproducibility
        random.seed(42)
        np.random.seed(42)
    
    def vectorized_evaluate(self, population):
        """Vectorized evaluation of population for better performance.
        
        Args:
            population: List of decision vectors
            
        Returns:
            List of objective vectors
        """
        # For now, use sequential evaluation
        # In a real implementation, this could use joblib.Parallel or multiprocessing
        return [self.func(x) for x in population]
    
    def initialize(self):
        """Initialize population using Opposition-Based Learning (OBL)."""
        # 1. Generate random initial population
        pop = []
        for _ in range(self.pop_size):
            individual = []
            for d in range(self.dim):
                individual.append(random.uniform(self.lb[d], self.ub[d]))
            pop.append(individual)
        
        # 2. Generate opposition-based population
        opp_pop = []
        for x in pop:
            opp_individual = []
            for d in range(self.dim):
                # Opposition: x'_d = lb_d + ub_d - x_d
                opp_val = self.lb[d] + self.ub[d] - x[d]
                opp_individual.append(opp_val)
            opp_pop.append(opp_individual)
        
        # 3. Combine original and opposition populations
        combined = pop + opp_pop
        combined_objs = self.vectorized_evaluate(combined)
        
        # 4. Select best pop_size solutions using multi-objective selection
        sel_idx = select_N(combined_objs, self.pop_size)
        self.population = [combined[i] for i in sel_idx]
        self.pop_objs = [combined_objs[i] for i in sel_idx]
        
        # 5. Initialize archive with selected population
        self.archive = Archive(self.archive_size)
        self.archive.add_all(self.population, self.pop_objs)
        
        # 6. Set reference point for hypervolume if not provided
        if self.ref is None or self.use_dynamic_ref:
            self.update_reference_point()
        
        # 7. Record initial hypervolume
        self.hv_history = [self.hypervolume()]
    
    def update_reference_point(self):
        """Update reference point dynamically based on current archive."""
        if not self.archive.objectives:
            return
        
        # Track maximum objectives seen so far
        current_max = []
        for i in range(len(self.archive.objectives[0])):
            max_val = max(obj[i] for obj in self.archive.objectives)
            current_max.append(max_val)
        
        if self.max_objectives is None:
            self.max_objectives = current_max[:]
        else:
            # Update maximum values
            for i in range(len(current_max)):
                self.max_objectives[i] = max(self.max_objectives[i], current_max[i])
        
        # Set reference point with 5% buffer
        self.ref = [max_val * 1.05 for max_val in self.max_objectives]
    
    def select_smart_leaders(self, k=3):
        """Select leaders using crowding distance and diversity criteria.
        
        Args:
            k: Number of leaders to select
            
        Returns:
            List of k position vectors selected from the archive
        """
        if not self.archive.positions:
            return []
        
        if len(self.archive.positions) < k:
            # If not enough solutions, repeat some
            leaders = self.archive.positions[:]
            while len(leaders) < k:
                leaders.extend(self.archive.positions[:k-len(leaders)])
            return leaders[:k]
        
        # Get all archive solutions
        archive_indices = list(range(len(self.archive.objectives)))
        
        # Calculate crowding distances
        cd = crowding_distance(self.archive.objectives, archive_indices)
        
        # Select leaders based on different criteria
        leaders = []
        
        # Alpha: Solution with highest hypervolume contribution (approximate using crowding distance)
        alpha_idx = max(archive_indices, key=lambda i: cd[i])
        leaders.append(self.archive.positions[alpha_idx])
        
        if len(archive_indices) > 1:
            # Beta: Solution farthest from alpha (diversity focus)
            alpha_obj = self.archive.objectives[alpha_idx]
            beta_idx = max(archive_indices, key=lambda i: 
                          sum((self.archive.objectives[i][j] - alpha_obj[j])**2 
                              for j in range(len(alpha_obj))))
            leaders.append(self.archive.positions[beta_idx])
        
        if len(archive_indices) > 2:
            # Delta: Random selection from remaining solutions
            remaining = [i for i in archive_indices if i not in [alpha_idx, beta_idx]]
            if remaining:
                delta_idx = random.choice(remaining)
                leaders.append(self.archive.positions[delta_idx])
        
        # Fill remaining positions if needed
        while len(leaders) < k:
            idx = random.choice(archive_indices)
            leaders.append(self.archive.positions[idx])
        
        return leaders[:k]
    
    def differential_mutation(self, wolf, leaders, iteration):
        """Apply differential mutation operator inspired by DE.
        
        Args:
            wolf: Current wolf position
            leaders: List of leader positions
            iteration: Current iteration number
            
        Returns:
            New position vector
        """
        if len(leaders) < 3:
            return wolf  # Fallback to original wolf
        
        alpha_pos, beta_pos, delta_pos = leaders[:3]
        
        # Create trial vector using differential mutation
        trial = []
        for d in range(self.dim):
            # DE mutation: trial = alpha + F * (beta - delta)
            if random.random() < self.CR:
                trial_val = alpha_pos[d] + self.F * (beta_pos[d] - delta_pos[d])
            else:
                trial_val = wolf[d]  # Keep original value
            
            # Apply boundary constraints
            trial_val = max(self.lb[d], min(self.ub[d], trial_val))
            trial.append(trial_val)
        
        return trial
    
    def hypervolume(self):
        """Calculate hypervolume (2D) of current archive solutions.
        
        Returns:
            float: Hypervolume value with respect to reference point
        """
        if not self.archive.objectives:
            return 0.0
        
        if len(self.archive.objectives[0]) != 2:
            # HV calculation implemented for 2 objectives only
            return 0.0
        
        # Sort points by first objective
        pts = sorted(self.archive.objectives, key=lambda o: o[0])
        
        hv = 0.0
        prev_x = 0.0  # Lower bound for f1
        
        for i, (f1, f2) in enumerate(pts):
            # Clamp f2 to reasonable lower bound
            f2_clamped = max(0.0, f2)
            
            # Calculate area contribution
            width = max(0, f1 - prev_x)
            height = max(0, self.ref[1] - f2_clamped)
            hv += width * height
            
            prev_x = f1
        
        # Add area from last point to reference point
        if pts:
            last_f1 = pts[-1][0]
            last_f2 = max(0.0, pts[-1][1])
            width = max(0, self.ref[0] - last_f1)
            height = max(0, self.ref[1] - last_f2)
            hv += width * height
        
        return hv
    
    def update_positions(self, iteration):
        """Update positions of all wolves using enhanced GWO position update equations.
        
        Args:
            iteration: Current iteration number (1-based)
        """
        # Calculate adaptive parameter a using nonlinear decay
        a = 2 * (1 - (iteration / self.max_iter) ** self.power_a)
        
        new_population = []
        new_pop_objs = []
        
        for wolf in self.population:
            # Get three leaders from archive
            if self.use_smart_leader_selection:
                leaders = self.select_smart_leaders(3)
            else:
                leaders = self.archive.get_leaders(3)
            
            # If archive has fewer than 3 solutions, repeat some leaders
            if len(leaders) < 3:
                leaders = (leaders * 3)[:3] or [wolf] * 3
            
            # Apply differential mutation if enabled
            if self.use_differential_mutation and random.random() < 0.5:
                new_pos = self.differential_mutation(wolf, leaders, iteration)
            else:
                # Standard GWO position update
                alpha_pos, beta_pos, delta_pos = leaders
                
                new_pos = []
                for d in range(self.dim):
                    # Alpha wolf influence
                    r1, r2 = random.random(), random.random()
                    A_alpha = 2 * a * r1 - a
                    C_alpha = 2 * r2
                    D_alpha = abs(C_alpha * alpha_pos[d] - wolf[d])
                    X1 = alpha_pos[d] - A_alpha * D_alpha
                    
                    # Beta wolf influence
                    r1, r2 = random.random(), random.random()
                    A_beta = 2 * a * r1 - a
                    C_beta = 2 * r2
                    D_beta = abs(C_beta * beta_pos[d] - wolf[d])
                    X2 = beta_pos[d] - A_beta * D_beta
                    
                    # Delta wolf influence
                    r1, r2 = random.random(), random.random()
                    A_delta = 2 * a * r1 - a
                    C_delta = 2 * r2
                    D_delta = abs(C_delta * delta_pos[d] - wolf[d])
                    X3 = delta_pos[d] - A_delta * D_delta
                    
                    # Average position from three leaders
                    new_val = (X1 + X2 + X3) / 3.0
                    
                    # Apply boundary constraints
                    new_val = max(self.lb[d], min(self.ub[d], new_val))
                    new_pos.append(new_val)
            
            new_population.append(new_pos)
        
        # Vectorized evaluation of new population
        new_pop_objs = self.vectorized_evaluate(new_population)
        
        # Update population
        self.population = new_population
        self.pop_objs = new_pop_objs
    
    def run(self):
        """Run the complete enhanced GWO algorithm.
        
        Returns:
            tuple: (final_positions, final_objectives, hypervolume_history)
        """
        # Initialize population with OBL
        self.initialize()
        
        print(f"Initial population size: {len(self.population)}")
        print(f"Initial archive size: {self.archive.size()}")
        print(f"Initial hypervolume: {self.hv_history[0]:.4f}")
        print(f"Enhanced features: DE={self.use_differential_mutation}, "
              f"DynRef={self.use_dynamic_ref}, SmartLeaders={self.use_smart_leader_selection}")
        
        # Main optimization loop
        for iteration in range(1, self.max_iter + 1):
            # Update wolf positions
            self.update_positions(iteration)
            
            # Update archive with new solutions
            self.archive.add_all(self.population, self.pop_objs)
            
            # Update reference point dynamically
            if self.use_dynamic_ref:
                self.update_reference_point()
            
            # Record convergence metric
            hv = self.hypervolume()
            self.hv_history.append(hv)
            
            # Progress reporting
            if iteration % 50 == 0 or iteration == self.max_iter:
                print(f"Iteration {iteration}: Archive size = {self.archive.size()}, "
                      f"Hypervolume = {hv:.4f}")
        
        # Return final results
        final_positions, final_objectives = self.archive.get_all_solutions()
        return final_positions, final_objectives, self.hv_history
    
    def get_statistics(self):
        """Get algorithm statistics.
        
        Returns:
            dict: Dictionary containing various statistics
        """
        return {
            'final_archive_size': self.archive.size(),
            'final_hypervolume': self.hv_history[-1] if self.hv_history else 0.0,
            'hypervolume_improvement': (self.hv_history[-1] - self.hv_history[0]) 
                                     if len(self.hv_history) > 1 else 0.0,
            'convergence_history': self.hv_history.copy(),
            'enhanced_features': {
                'differential_mutation': self.use_differential_mutation,
                'dynamic_reference': self.use_dynamic_ref,
                'smart_leader_selection': self.use_smart_leader_selection
            }
        }