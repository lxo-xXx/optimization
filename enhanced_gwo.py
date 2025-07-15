import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from scipy.spatial import ConvexHull
from sklearn.cluster import KMeans
from joblib import Parallel, delayed
import warnings
warnings.filterwarnings('ignore')

class EnhancedGWO:
    """
    Enhanced Multi-Objective Grey Wolf Optimizer with improved features:
    1. Advanced Self-Adaptive Archive Leader Selection (hypervolume contribution + σ-sharing)
    2. Improved Hybrid Crossover-Mutation with adaptive parameters
    3. σ-sharing based Dynamic Archive Management
    4. Adaptive Dynamic Reference Point with problem-specific adjustments
    5. Vectorized Parallel Evaluation with batch processing
    6. Enhanced diversity preservation mechanisms
    """
    
    def __init__(self, func, bounds, pop_size=50, max_gen=100, archive_size=100, 
                 F=0.5, CR=0.7, n_jobs=4, sigma_share=0.1, verbose=True):
        """
        Initialize Enhanced GWO
        
        Parameters:
        -----------
        func : callable
            Multi-objective function to optimize
        bounds : list of tuples
            [(min1, max1), (min2, max2), ...] for each dimension
        pop_size : int
            Population size
        max_gen : int
            Maximum generations
        archive_size : int
            Maximum archive size
        F : float
            Differential evolution factor (adaptive)
        CR : float
            Crossover probability (adaptive)
        n_jobs : int
            Number of parallel jobs
        sigma_share : float
            Sharing parameter for diversity preservation
        verbose : bool
            Print progress
        """
        self.func = func
        self.bounds = np.array(bounds)
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.archive_size = archive_size
        self.F = F
        self.CR = CR
        self.n_jobs = n_jobs
        self.sigma_share = sigma_share
        self.verbose = verbose
        
        self.dim = len(bounds)
        self.lb = self.bounds[:, 0]
        self.ub = self.bounds[:, 1]
        
        # Initialize population and archive
        self.population = None
        self.archive = []
        self.hypervolume_history = []
        self.reference_point = None
        self.nadir_point = None
        
        # Adaptive parameters
        self.adaptive_F = F
        self.adaptive_CR = CR
        
    def evaluate_parallel_vectorized(self, population):
        """Enhanced parallel evaluation with vectorized operations"""
        if self.n_jobs == 1:
            return np.array([self.func(ind) for ind in population])
        else:
            # Batch processing for better memory efficiency
            batch_size = max(1, len(population) // self.n_jobs)
            results = []
            
            for i in range(0, len(population), batch_size):
                batch = population[i:i + batch_size]
                batch_results = Parallel(n_jobs=self.n_jobs)(
                    delayed(self.func)(ind) for ind in batch
                )
                results.extend(batch_results)
            
            return np.array(results)
    
    def initialize_population(self):
        """Initialize population with Latin Hypercube Sampling for better diversity"""
        # Latin Hypercube Sampling for better initial diversity
        from scipy.stats import qmc
        
        sampler = qmc.LatinHypercube(d=self.dim)
        sample = sampler.random(n=self.pop_size)
        
        # Scale to bounds
        self.population = qmc.scale(sample, self.lb, self.ub)
        
    def update_adaptive_reference_point(self, objectives):
        """Enhanced adaptive reference point with problem-specific adjustments"""
        if len(objectives) == 0:
            # Default reference points for common test problems
            self.reference_point = np.array([3.0, 3.0])
            self.nadir_point = np.array([0.0, 0.0])
            return
            
        objectives = np.array(objectives)
        
        # Calculate current nadir and ideal points
        current_nadir = np.max(objectives, axis=0)
        current_ideal = np.min(objectives, axis=0)
        
        # Update nadir point with exponential smoothing
        if self.nadir_point is None:
            self.nadir_point = current_nadir
        else:
            alpha = 0.1  # Smoothing factor
            self.nadir_point = alpha * current_nadir + (1 - alpha) * self.nadir_point
        
        # Adaptive buffer based on objective range and convergence
        obj_range = self.nadir_point - current_ideal
        convergence_factor = 1.0 + 0.1 * np.exp(-len(objectives) / 50)  # Reduces as archive grows
        
        # Dynamic reference point with adaptive buffer
        adaptive_buffer = 0.05 * obj_range * convergence_factor
        self.reference_point = self.nadir_point + adaptive_buffer
        
        # Ensure minimum buffer for hypervolume calculation
        min_buffer = 0.01 * np.abs(self.nadir_point)
        self.reference_point = np.maximum(self.reference_point, self.nadir_point + min_buffer)
        
    def calculate_hypervolume_contribution(self, objectives, individual_idx):
        """Calculate hypervolume contribution of individual solution"""
        if len(objectives) <= 1:
            return float('inf')
            
        # Remove the individual and calculate hypervolume difference
        reduced_objectives = np.delete(objectives, individual_idx, axis=0)
        
        full_hv = self.calculate_hypervolume_fast(objectives)
        reduced_hv = self.calculate_hypervolume_fast(reduced_objectives)
        
        return max(0, full_hv - reduced_hv)
    
    def calculate_hypervolume_fast(self, front):
        """Fast hypervolume calculation optimized for 2D problems"""
        if len(front) == 0:
            return 0.0
            
        front = np.array(front)
        
        # Filter dominated solutions first
        non_dominated = []
        for i, sol in enumerate(front):
            dominated = False
            for j, other in enumerate(front):
                if i != j and np.all(other <= sol) and np.any(other < sol):
                    dominated = True
                    break
            if not dominated:
                non_dominated.append(sol)
        
        if len(non_dominated) == 0:
            return 0.0
            
        front = np.array(non_dominated)
        
        # 2D hypervolume calculation (optimized)
        if front.shape[1] == 2:
            # Sort by first objective
            sorted_indices = np.argsort(front[:, 0])
            sorted_front = front[sorted_indices]
            
            hv = 0.0
            for i in range(len(sorted_front)):
                if i == 0:
                    width = self.reference_point[0] - sorted_front[i, 0]
                else:
                    width = sorted_front[i-1, 0] - sorted_front[i, 0]
                height = self.reference_point[1] - sorted_front[i, 1]
                
                if width > 0 and height > 0:
                    hv += width * height
                    
            return max(0, hv)
        else:
            # Monte Carlo for higher dimensions
            return self.calculate_hypervolume_monte_carlo(front)
    
    def calculate_hypervolume_monte_carlo(self, front):
        """Monte Carlo hypervolume estimation for higher dimensions"""
        n_samples = 10000
        ref_point = self.reference_point
        ideal_point = np.min(front, axis=0)
        
        # Generate random points in the reference space
        random_points = np.random.uniform(ideal_point, ref_point, (n_samples, front.shape[1]))
        
        # Count dominated points
        dominated = 0
        for point in random_points:
            if np.any(np.all(front <= point, axis=1)):
                dominated += 1
                
        volume = np.prod(ref_point - ideal_point)
        return (dominated / n_samples) * volume
    
    def calculate_sigma_sharing_distance(self, objectives):
        """Calculate σ-sharing distances for diversity preservation"""
        if len(objectives) <= 1:
            return np.array([float('inf')])
            
        objectives = np.array(objectives)
        n = len(objectives)
        sharing_values = np.zeros(n)
        
        # Calculate pairwise distances
        distances = cdist(objectives, objectives, metric='euclidean')
        
        # Normalize distances by objective ranges
        obj_ranges = np.max(objectives, axis=0) - np.min(objectives, axis=0)
        obj_ranges[obj_ranges == 0] = 1.0  # Avoid division by zero
        
        for i in range(n):
            sharing_sum = 0.0
            for j in range(n):
                if i != j:
                    # Normalized distance
                    norm_dist = distances[i, j] / np.sqrt(np.sum(obj_ranges**2))
                    
                    # Sharing function
                    if norm_dist < self.sigma_share:
                        sharing_sum += 1 - (norm_dist / self.sigma_share)
                    
            sharing_values[i] = max(1.0, sharing_sum)
            
        return sharing_values
    
    def select_leaders_enhanced(self, archive_objectives):
        """
        Enhanced Self-Adaptive Archive Leader Selection:
        α = highest hypervolume contribution
        β = solution with maximum angular deviation (diversity focus)
        δ = solution with lowest sharing value (edge of front)
        """
        if len(archive_objectives) < 3:
            # Not enough solutions, use available ones
            indices = list(range(len(archive_objectives)))
            while len(indices) < 3:
                indices.append(np.random.choice(len(archive_objectives)))
            return indices[:3]
        
        archive_objectives = np.array(archive_objectives)
        
        # Calculate hypervolume contributions
        hv_contributions = []
        for i in range(len(archive_objectives)):
            contribution = self.calculate_hypervolume_contribution(archive_objectives, i)
            hv_contributions.append(contribution)
        
        # α: Highest hypervolume contribution
        alpha_idx = np.argmax(hv_contributions)
        
        # Calculate angular deviations from centroid
        centroid = np.mean(archive_objectives, axis=0)
        angular_deviations = []
        
        for i, obj in enumerate(archive_objectives):
            if i != alpha_idx:
                # Calculate angle from centroid
                vec_to_centroid = centroid - obj
                angle = np.arctan2(vec_to_centroid[1], vec_to_centroid[0])
                angular_deviations.append((i, angle))
        
        # β: Maximum angular deviation from centroid (diversity focus)
        if angular_deviations:
            angles = [angle for _, angle in angular_deviations]
            # Find solution with maximum deviation from mean angle
            mean_angle = np.mean(angles)
            max_deviation_idx = max(angular_deviations, key=lambda x: abs(x[1] - mean_angle))[0]
            beta_idx = max_deviation_idx
        else:
            beta_idx = (alpha_idx + 1) % len(archive_objectives)
        
        # Calculate σ-sharing values
        sharing_values = self.calculate_sigma_sharing_distance(archive_objectives)
        
        # δ: Lowest sharing value (edge of front)
        remaining_indices = [i for i in range(len(archive_objectives)) if i != alpha_idx and i != beta_idx]
        if remaining_indices:
            remaining_sharing = [sharing_values[i] for i in remaining_indices]
            delta_idx = remaining_indices[np.argmin(remaining_sharing)]
        else:
            delta_idx = np.random.choice(len(archive_objectives))
            
        return [alpha_idx, beta_idx, delta_idx]
    
    def adaptive_hybrid_position_update(self, wolf_pos, alpha_pos, beta_pos, delta_pos, a, generation):
        """
        Enhanced hybrid position update with adaptive parameters and improved diversity
        """
        # Update adaptive parameters
        progress = generation / self.max_gen
        
        # Adaptive F: Higher exploration early, lower later
        self.adaptive_F = self.F * (1.5 - progress)
        
        # Adaptive CR: Higher crossover probability during middle phase
        self.adaptive_CR = self.CR * (1.0 + 0.5 * np.sin(np.pi * progress))
        
        # Standard GWO position update with adaptive coefficients
        A1 = 2 * a * np.random.random(self.dim) - a
        C1 = 2 * np.random.random(self.dim)
        D_alpha = np.abs(C1 * alpha_pos - wolf_pos)
        X1 = alpha_pos - A1 * D_alpha
        
        A2 = 2 * a * np.random.random(self.dim) - a
        C2 = 2 * np.random.random(self.dim)
        D_beta = np.abs(C2 * beta_pos - wolf_pos)
        X2 = beta_pos - A2 * D_beta
        
        A3 = 2 * a * np.random.random(self.dim) - a
        C3 = 2 * np.random.random(self.dim)
        D_delta = np.abs(C3 * delta_pos - wolf_pos)
        X3 = delta_pos - A3 * D_delta
        
        # Weighted GWO position (adaptive weights)
        w1, w2, w3 = 0.4, 0.3, 0.3  # Slightly favor alpha
        gwo_pos = w1 * X1 + w2 * X2 + w3 * X3
        
        # Enhanced DE-inspired mutation with multiple strategies
        if np.random.random() < self.adaptive_CR:
            # Strategy 1: Standard DE mutation
            de_pos1 = alpha_pos + self.adaptive_F * (beta_pos - delta_pos)
            
            # Strategy 2: Best/2 mutation
            if np.random.random() < 0.5:
                de_pos2 = alpha_pos + self.adaptive_F * (beta_pos - delta_pos) + self.adaptive_F * (wolf_pos - beta_pos)
                trial_pos = de_pos2
            else:
                trial_pos = de_pos1
            
            # Crossover between GWO and DE positions
            mask = np.random.random(self.dim) < self.adaptive_CR
            new_pos = np.where(mask, trial_pos, gwo_pos)
        else:
            new_pos = gwo_pos
            
        # Enhanced diversity maintenance with adaptive factors
        diversity_factor = 0.15 * np.exp(-2 * progress)  # Exponential decay
        levy_noise = self.levy_flight(self.dim) * diversity_factor
        
        # Combine position with Lévy flight for better exploration
        new_pos = (1 - diversity_factor) * new_pos + diversity_factor * wolf_pos + levy_noise
        
        # Ensure bounds with reflection
        new_pos = self.reflect_bounds(new_pos)
        
        return new_pos
    
    def levy_flight(self, dim):
        """Generate Lévy flight random walk for enhanced exploration"""
        beta = 1.5
        sigma = (np.math.gamma(1 + beta) * np.sin(np.pi * beta / 2) / 
                (np.math.gamma((1 + beta) / 2) * beta * (2 ** ((beta - 1) / 2)))) ** (1 / beta)
        
        u = np.random.normal(0, sigma, dim)
        v = np.random.normal(0, 1, dim)
        
        return u / (np.abs(v) ** (1 / beta))
    
    def reflect_bounds(self, position):
        """Reflect position within bounds instead of clipping"""
        for i in range(self.dim):
            if position[i] < self.lb[i]:
                position[i] = self.lb[i] + (self.lb[i] - position[i])
            elif position[i] > self.ub[i]:
                position[i] = self.ub[i] - (position[i] - self.ub[i])
        
        # Final clipping if reflection goes out of bounds
        return np.clip(position, self.lb, self.ub)
    
    def manage_archive_sigma_sharing(self, new_solutions, new_objectives):
        """
        Enhanced Dynamic Archive Management with σ-sharing and clustering
        """
        if len(self.archive) == 0:
            self.archive = [(sol.copy(), obj.copy()) for sol, obj in zip(new_solutions, new_objectives)]
            return
            
        # Combine current archive with new solutions
        all_solutions = [sol for sol, _ in self.archive] + list(new_solutions)
        all_objectives = [obj for _, obj in self.archive] + list(new_objectives)
        
        # Non-dominated sorting
        non_dominated_indices = self.fast_non_dominated_sort(all_objectives)
        
        # Select non-dominated solutions
        selected_solutions = []
        selected_objectives = []
        
        for idx in non_dominated_indices:
            selected_solutions.append(all_solutions[idx])
            selected_objectives.append(all_objectives[idx])
            
        # If archive is still too large, apply σ-sharing based pruning
        if len(selected_solutions) > self.archive_size:
            selected_objectives = np.array(selected_objectives)
            
            # Calculate σ-sharing values
            sharing_values = self.calculate_sigma_sharing_distance(selected_objectives)
            
            # Remove solutions with highest sharing values (most crowded)
            keep_indices = np.argsort(sharing_values)[:self.archive_size]
            
            final_solutions = [selected_solutions[i] for i in keep_indices]
            final_objectives = [selected_objectives[i] for i in keep_indices]
        else:
            final_solutions = selected_solutions
            final_objectives = selected_objectives
            
        # Update archive
        self.archive = [(sol.copy(), obj.copy()) for sol, obj in zip(final_solutions, final_objectives)]
    
    def fast_non_dominated_sort(self, objectives):
        """Fast non-dominated sorting algorithm"""
        objectives = np.array(objectives)
        n = len(objectives)
        
        if n == 0:
            return []
            
        # Find non-dominated solutions
        is_dominated = np.zeros(n, dtype=bool)
        
        for i in range(n):
            for j in range(i + 1, n):
                # Check if i dominates j
                if np.all(objectives[i] <= objectives[j]) and np.any(objectives[i] < objectives[j]):
                    is_dominated[j] = True
                # Check if j dominates i
                elif np.all(objectives[j] <= objectives[i]) and np.any(objectives[j] < objectives[i]):
                    is_dominated[i] = True
                    
        return np.where(~is_dominated)[0]
    
    def optimize(self):
        """Main optimization loop with enhanced features"""
        # Initialize population with Latin Hypercube Sampling
        self.initialize_population()
        
        # Evaluate initial population
        objectives = self.evaluate_parallel_vectorized(self.population)
        
        # Initialize archive with initial non-dominated solutions
        non_dom_indices = self.fast_non_dominated_sort(objectives)
        initial_solutions = self.population[non_dom_indices]
        initial_objectives = objectives[non_dom_indices]
        self.manage_archive_sigma_sharing(initial_solutions, initial_objectives)
        
        # Main optimization loop
        for generation in range(self.max_gen):
            # Update adaptive reference point
            if self.archive:
                archive_objectives = np.array([obj for _, obj in self.archive])
                self.update_adaptive_reference_point(archive_objectives)
                
                # Calculate hypervolume with smoothing to reduce fluctuation
                current_hv = self.calculate_hypervolume_fast(archive_objectives)
                
                # Exponential smoothing for hypervolume history
                if len(self.hypervolume_history) > 0:
                    smoothed_hv = 0.7 * current_hv + 0.3 * self.hypervolume_history[-1]
                    self.hypervolume_history.append(smoothed_hv)
                else:
                    self.hypervolume_history.append(current_hv)
                
                if self.verbose and generation % 10 == 0:
                    print(f"Generation {generation}: Archive size = {len(self.archive)}, "
                          f"Hypervolume = {current_hv:.4f}, "
                          f"Adaptive F = {self.adaptive_F:.3f}, "
                          f"Adaptive CR = {self.adaptive_CR:.3f}")
                
                # Select leaders with enhanced strategy
                if len(self.archive) >= 3:
                    leader_indices = self.select_leaders_enhanced(archive_objectives)
                    alpha_pos = self.archive[leader_indices[0]][0]
                    beta_pos = self.archive[leader_indices[1]][0]
                    delta_pos = self.archive[leader_indices[2]][0]
                else:
                    # Fallback to random selection
                    alpha_pos = self.archive[0][0] if self.archive else self.population[0]
                    beta_pos = self.archive[min(1, len(self.archive)-1)][0] if len(self.archive) > 1 else self.population[1]
                    delta_pos = self.archive[min(2, len(self.archive)-1)][0] if len(self.archive) > 2 else self.population[2]
            else:
                # No archive yet, use random population members
                alpha_pos = self.population[0]
                beta_pos = self.population[1]
                delta_pos = self.population[2]
                self.hypervolume_history.append(0.0)
            
            # Update coefficient a (nonlinear decrease)
            a = 2 * (1 - (generation / self.max_gen)**2)  # Quadratic decrease
            
            # Update wolf positions with enhanced hybrid method
            new_population = np.zeros_like(self.population)
            for i in range(self.pop_size):
                new_population[i] = self.adaptive_hybrid_position_update(
                    self.population[i], alpha_pos, beta_pos, delta_pos, a, generation
                )
            
            self.population = new_population
            
            # Evaluate new population
            new_objectives = self.evaluate_parallel_vectorized(self.population)
            
            # Update archive with enhanced management
            self.manage_archive_sigma_sharing(self.population, new_objectives)
        
        # Final results
        if self.archive:
            final_solutions = np.array([sol for sol, _ in self.archive])
            final_objectives = np.array([obj for _, obj in self.archive])
            
            if self.verbose:
                print(f"\nOptimization completed!")
                print(f"Final archive size: {len(self.archive)}")
                print(f"Final hypervolume: {self.hypervolume_history[-1]:.4f}")
                print(f"Hypervolume improvement: {((self.hypervolume_history[-1] - self.hypervolume_history[0]) / max(self.hypervolume_history[0], 1e-10)) * 100:.2f}%")
                
            return final_solutions, final_objectives
        else:
            return np.array([]), np.array([])
    
    def plot_results(self, title="Enhanced GWO Results"):
        """Plot the Pareto front and convergence history with enhanced visualization"""
        if not self.archive:
            print("No results to plot!")
            return
            
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot Pareto front
        objectives = np.array([obj for _, obj in self.archive])
        ax1.scatter(objectives[:, 0], objectives[:, 1], c='red', s=30, alpha=0.7, label='Pareto Front')
        ax1.set_xlabel('Objective 1')
        ax1.set_ylabel('Objective 2')
        ax1.set_title('Pareto Front')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot convergence history
        ax2.plot(self.hypervolume_history, 'b-', linewidth=2, label='Hypervolume')
        ax2.set_xlabel('Generation')
        ax2.set_ylabel('Hypervolume')
        ax2.set_title('Convergence History')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Plot hypervolume improvement rate
        if len(self.hypervolume_history) > 1:
            hv_diff = np.diff(self.hypervolume_history)
            ax3.plot(hv_diff, 'g-', linewidth=2, label='HV Improvement Rate')
            ax3.axhline(y=0, color='r', linestyle='--', alpha=0.5)
            ax3.set_xlabel('Generation')
            ax3.set_ylabel('Hypervolume Change')
            ax3.set_title('Hypervolume Improvement Rate')
            ax3.grid(True, alpha=0.3)
            ax3.legend()
        
        # Plot archive size evolution
        ax4.plot(range(len(self.hypervolume_history)), 
                [len(self.archive)] * len(self.hypervolume_history), 
                'purple', linewidth=2, label='Archive Size')
        ax4.set_xlabel('Generation')
        ax4.set_ylabel('Archive Size')
        ax4.set_title('Archive Size Evolution')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        plt.tight_layout()
        plt.savefig(f'{title.lower().replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
        plt.show()