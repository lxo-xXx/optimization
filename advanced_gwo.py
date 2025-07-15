import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from joblib import Parallel, delayed
import warnings
warnings.filterwarnings('ignore')

class AdvancedGWO:
    """
    Advanced Multi-Objective Grey Wolf Optimizer with enhanced features:
    1. Self-Adaptive Archive Leader Selection
    2. Hybrid Crossover-Mutation (GWO + DE/NSGA-inspired)
    3. Dynamic Archive Management
    4. Nonlinear Dynamic Reference Point
    5. Parallel Evaluation for Speedup
    """
    
    def __init__(self, func, bounds, pop_size=50, max_gen=100, archive_size=100, 
                 F=0.5, CR=0.7, n_jobs=4, verbose=True):
        """
        Initialize Advanced GWO
        
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
            Differential evolution factor
        CR : float
            Crossover probability
        n_jobs : int
            Number of parallel jobs
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
        self.verbose = verbose
        
        self.dim = len(bounds)
        self.lb = self.bounds[:, 0]
        self.ub = self.bounds[:, 1]
        
        # Initialize population and archive
        self.population = None
        self.archive = []
        self.hypervolume_history = []
        self.reference_point = None
        
    def evaluate_parallel(self, population):
        """Parallel evaluation of population"""
        if self.n_jobs == 1:
            return np.array([self.func(ind) for ind in population])
        else:
            results = Parallel(n_jobs=self.n_jobs)(
                delayed(self.func)(ind) for ind in population
            )
            return np.array(results)
    
    def initialize_population(self):
        """Initialize population with random solutions"""
        self.population = np.random.uniform(
            self.lb, self.ub, (self.pop_size, self.dim)
        )
        
    def update_dynamic_reference_point(self, objectives):
        """Update reference point dynamically based on current objectives"""
        if len(objectives) == 0:
            self.reference_point = np.array([3.0, 3.0])  # Default for UF problems
        else:
            # Dynamic reference point: max + 5% buffer
            max_obj = np.max(objectives, axis=0)
            buffer = 0.05 * np.abs(max_obj)
            self.reference_point = max_obj + buffer
            
    def calculate_hypervolume(self, front):
        """Calculate hypervolume using Monte Carlo method"""
        if len(front) == 0:
            return 0.0
            
        # Simple 2D hypervolume calculation
        if front.shape[1] == 2:
            # Sort by first objective
            sorted_front = front[np.argsort(front[:, 0])]
            hv = 0.0
            for i in range(len(sorted_front)):
                if i == 0:
                    width = self.reference_point[0] - sorted_front[i, 0]
                else:
                    width = sorted_front[i-1, 0] - sorted_front[i, 0]
                height = self.reference_point[1] - sorted_front[i, 1]
                hv += width * height
            return max(0, hv)
        else:
            # Monte Carlo approximation for higher dimensions
            n_samples = 10000
            ref_point = self.reference_point
            
            # Generate random points in the reference space
            random_points = np.random.uniform(
                np.min(front, axis=0), ref_point, (n_samples, front.shape[1])
            )
            
            # Count dominated points
            dominated = 0
            for point in random_points:
                if np.any(np.all(front <= point, axis=1)):
                    dominated += 1
                    
            volume = np.prod(ref_point - np.min(front, axis=0))
            return (dominated / n_samples) * volume
    
    def calculate_crowding_distance(self, objectives):
        """Calculate crowding distance for diversity preservation"""
        if len(objectives) <= 2:
            return np.full(len(objectives), float('inf'))
            
        distances = np.zeros(len(objectives))
        n_obj = objectives.shape[1]
        
        for m in range(n_obj):
            # Sort by m-th objective
            sorted_indices = np.argsort(objectives[:, m])
            
            # Boundary solutions get infinite distance
            distances[sorted_indices[0]] = float('inf')
            distances[sorted_indices[-1]] = float('inf')
            
            # Calculate distances for intermediate solutions
            obj_range = objectives[sorted_indices[-1], m] - objectives[sorted_indices[0], m]
            if obj_range > 0:
                for i in range(1, len(sorted_indices) - 1):
                    distances[sorted_indices[i]] += (
                        objectives[sorted_indices[i+1], m] - objectives[sorted_indices[i-1], m]
                    ) / obj_range
                    
        return distances
    
    def select_leaders_adaptive(self, archive_objectives):
        """
        Self-Adaptive Archive Leader Selection based on:
        α = highest hypervolume contribution
        β = highest crowding distance (diversity)
        δ = random or centroid-based selection
        """
        if len(archive_objectives) < 3:
            # Not enough solutions, use available ones
            indices = list(range(len(archive_objectives)))
            while len(indices) < 3:
                indices.append(np.random.choice(len(archive_objectives)))
            return indices[:3]
        
        # Calculate crowding distances
        crowding_distances = self.calculate_crowding_distance(archive_objectives)
        
        # α: Highest hypervolume contribution (approximate using distance to nadir)
        nadir_point = np.max(archive_objectives, axis=0)
        hv_contributions = np.sum((nadir_point - archive_objectives), axis=1)
        alpha_idx = np.argmax(hv_contributions)
        
        # β: Highest crowding distance (diversity focus)
        # Exclude alpha to avoid duplication
        available_indices = list(range(len(archive_objectives)))
        available_indices.remove(alpha_idx)
        available_crowding = crowding_distances[available_indices]
        beta_idx = available_indices[np.argmax(available_crowding)]
        
        # δ: Random selection from remaining solutions
        remaining_indices = [i for i in available_indices if i != beta_idx]
        if remaining_indices:
            delta_idx = np.random.choice(remaining_indices)
        else:
            delta_idx = np.random.choice(len(archive_objectives))
            
        return [alpha_idx, beta_idx, delta_idx]
    
    def hybrid_position_update(self, wolf_pos, alpha_pos, beta_pos, delta_pos, a, generation):
        """
        Hybrid position update combining GWO with DE-inspired mutations
        """
        # Standard GWO position update
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
        
        # Standard GWO position
        gwo_pos = (X1 + X2 + X3) / 3
        
        # DE-inspired mutation
        if np.random.random() < self.CR:
            # Differential mutation: Trial = X_α + F * (X_β - X_δ)
            de_pos = alpha_pos + self.F * (beta_pos - delta_pos)
            
            # Crossover between GWO and DE positions
            mask = np.random.random(self.dim) < self.CR
            new_pos = np.where(mask, de_pos, gwo_pos)
        else:
            new_pos = gwo_pos
            
        # Add diversity maintenance (combine with previous position)
        diversity_factor = 0.1 * (1 - generation / self.max_gen)  # Decreases over time
        new_pos = (1 - diversity_factor) * new_pos + diversity_factor * wolf_pos
        
        # Ensure bounds
        new_pos = np.clip(new_pos, self.lb, self.ub)
        
        return new_pos
    
    def manage_archive_dynamic(self, new_solutions, new_objectives):
        """
        Dynamic Archive Management with clustering-based pruning
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
            
        # If archive is still too large, apply clustering-based pruning
        if len(selected_solutions) > self.archive_size:
            # Use K-means clustering to maintain diversity
            n_clusters = min(self.archive_size, len(selected_solutions))
            
            if n_clusters > 1:
                kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                cluster_labels = kmeans.fit_predict(selected_objectives)
                
                # Select one representative from each cluster (closest to centroid)
                final_solutions = []
                final_objectives = []
                
                for cluster_id in range(n_clusters):
                    cluster_indices = np.where(cluster_labels == cluster_id)[0]
                    if len(cluster_indices) > 0:
                        # Select the solution closest to cluster centroid
                        cluster_center = kmeans.cluster_centers_[cluster_id]
                        cluster_objs = np.array([selected_objectives[i] for i in cluster_indices])
                        distances = np.sum((cluster_objs - cluster_center)**2, axis=1)
                        best_idx = cluster_indices[np.argmin(distances)]
                        
                        final_solutions.append(selected_solutions[best_idx])
                        final_objectives.append(selected_objectives[best_idx])
            else:
                final_solutions = selected_solutions[:self.archive_size]
                final_objectives = selected_objectives[:self.archive_size]
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
        """Main optimization loop"""
        # Initialize population
        self.initialize_population()
        
        # Evaluate initial population
        objectives = self.evaluate_parallel(self.population)
        
        # Initialize archive with initial non-dominated solutions
        non_dom_indices = self.fast_non_dominated_sort(objectives)
        initial_solutions = self.population[non_dom_indices]
        initial_objectives = objectives[non_dom_indices]
        self.manage_archive_dynamic(initial_solutions, initial_objectives)
        
        # Main optimization loop
        for generation in range(self.max_gen):
            # Update dynamic reference point
            if self.archive:
                archive_objectives = np.array([obj for _, obj in self.archive])
                self.update_dynamic_reference_point(archive_objectives)
                
                # Calculate hypervolume
                hv = self.calculate_hypervolume(archive_objectives)
                self.hypervolume_history.append(hv)
                
                if self.verbose and generation % 10 == 0:
                    print(f"Generation {generation}: Archive size = {len(self.archive)}, Hypervolume = {hv:.4f}")
                
                # Select leaders adaptively
                if len(self.archive) >= 3:
                    leader_indices = self.select_leaders_adaptive(archive_objectives)
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
            
            # Update coefficient a (decreases linearly from 2 to 0)
            a = 2 * (1 - generation / self.max_gen)
            
            # Update wolf positions
            new_population = np.zeros_like(self.population)
            for i in range(self.pop_size):
                new_population[i] = self.hybrid_position_update(
                    self.population[i], alpha_pos, beta_pos, delta_pos, a, generation
                )
            
            self.population = new_population
            
            # Evaluate new population
            new_objectives = self.evaluate_parallel(self.population)
            
            # Update archive with new solutions
            self.manage_archive_dynamic(self.population, new_objectives)
        
        # Final results
        if self.archive:
            final_solutions = np.array([sol for sol, _ in self.archive])
            final_objectives = np.array([obj for _, obj in self.archive])
            
            if self.verbose:
                print(f"\nOptimization completed!")
                print(f"Final archive size: {len(self.archive)}")
                print(f"Final hypervolume: {self.hypervolume_history[-1]:.4f}")
                
            return final_solutions, final_objectives
        else:
            return np.array([]), np.array([])
    
    def plot_results(self, title="Advanced GWO Results"):
        """Plot the Pareto front and convergence history"""
        if not self.archive:
            print("No results to plot!")
            return
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot Pareto front
        objectives = np.array([obj for _, obj in self.archive])
        ax1.scatter(objectives[:, 0], objectives[:, 1], c='red', s=30, alpha=0.7)
        ax1.set_xlabel('Objective 1')
        ax1.set_ylabel('Objective 2')
        ax1.set_title('Pareto Front')
        ax1.grid(True, alpha=0.3)
        
        # Plot convergence
        ax2.plot(self.hypervolume_history, 'b-', linewidth=2)
        ax2.set_xlabel('Generation')
        ax2.set_ylabel('Hypervolume')
        ax2.set_title('Convergence History')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{title.lower().replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
        plt.show()