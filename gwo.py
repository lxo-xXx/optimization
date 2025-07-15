import math
import random
from archive import Archive
from domination import select_N


class GWO:
    """Grey Wolf Optimizer with advanced features for multi-objective optimization.
    
    Features:
    - Opposition-Based Learning (OBL) for initialization
    - Elite Archive for multi-objective optimization
    - Adaptive nonlinear decay of parameter a
    - Hypervolume tracking for convergence analysis
    """
    
    def __init__(self, func, dim, bounds, pop_size=50, max_iter=200, 
                 archive_size=100, power_a=3, ref_point=None):
        """Initialize the GWO algorithm.
        
        Args:
            func: Objective function mapping decision vector to objective values
            dim: Dimension of decision space
            bounds: Tuple (lower_bounds, upper_bounds) for each dimension
            pop_size: Number of wolves (solutions)
            max_iter: Number of iterations
            archive_size: Maximum size of external archive
            power_a: Exponent for nonlinear decay of parameter a (1 = linear)
            ref_point: Reference point for hypervolume calculation
        """
        self.func = func
        self.dim = dim
        self.lb, self.ub = bounds
        self.pop_size = pop_size
        self.max_iter = max_iter
        self.archive_size = archive_size
        self.power_a = power_a
        self.ref = ref_point
        
        # Initialize algorithm components
        self.archive = Archive(archive_size)
        self.population = []
        self.pop_objs = []
        self.hv_history = []
        
        # Set random seed for reproducibility
        random.seed(42)
    
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
        combined_objs = [self.func(x) for x in combined]
        
        # 4. Select best pop_size solutions using multi-objective selection
        sel_idx = select_N(combined_objs, self.pop_size)
        self.population = [combined[i] for i in sel_idx]
        self.pop_objs = [combined_objs[i] for i in sel_idx]
        
        # 5. Initialize archive with selected population
        self.archive = Archive(self.archive_size)
        self.archive.add_all(self.population, self.pop_objs)
        
        # 6. Set reference point for hypervolume if not provided
        if self.ref is None:
            # Set reference point slightly worse than worst objectives
            worst_obj = []
            for i in range(len(self.pop_objs[0])):
                worst_val = max(objs[i] for objs in self.pop_objs)
                worst_obj.append(worst_val * 1.1)
            self.ref = worst_obj
        
        # 7. Record initial hypervolume
        self.hv_history = [self.hypervolume()]
    
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
        """Update positions of all wolves using GWO position update equations.
        
        Args:
            iteration: Current iteration number (1-based)
        """
        # Calculate adaptive parameter a using nonlinear decay
        a = 2 * (1 - (iteration / self.max_iter) ** self.power_a)
        
        new_population = []
        new_pop_objs = []
        
        for wolf in self.population:
            # Get three leaders from archive (alpha, beta, delta)
            leaders = self.archive.get_leaders(3)
            
            # If archive has fewer than 3 solutions, repeat some leaders
            if len(leaders) < 3:
                leaders = (leaders * 3)[:3] or [wolf] * 3
            
            alpha_pos, beta_pos, delta_pos = leaders
            
            # Calculate new position using GWO update equations
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
            
            # Evaluate new position
            new_obj = self.func(new_pos)
            new_population.append(new_pos)
            new_pop_objs.append(new_obj)
        
        # Update population
        self.population = new_population
        self.pop_objs = new_pop_objs
    
    def run(self):
        """Run the complete GWO algorithm.
        
        Returns:
            tuple: (final_positions, final_objectives, hypervolume_history)
        """
        # Initialize population with OBL
        self.initialize()
        
        print(f"Initial population size: {len(self.population)}")
        print(f"Initial archive size: {self.archive.size()}")
        print(f"Initial hypervolume: {self.hv_history[0]:.4f}")
        
        # Main optimization loop
        for iteration in range(1, self.max_iter + 1):
            # Update wolf positions
            self.update_positions(iteration)
            
            # Update archive with new solutions
            self.archive.add_all(self.population, self.pop_objs)
            
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
            'convergence_history': self.hv_history.copy()
        }