import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, List, Tuple, Optional
import time
import random

class Wolf:
    """Represents a wolf in the Grey Wolf Optimizer algorithm."""
    
    def __init__(self, position: np.ndarray, fitness: float = float('inf')):
        self.position = position.copy()
        self.fitness = fitness
    
    def update_position(self, new_position: np.ndarray):
        """Update the wolf's position."""
        self.position = new_position.copy()
    
    def update_fitness(self, fitness: float):
        """Update the wolf's fitness value."""
        self.fitness = fitness

class GreyWolfOptimizer:
    """
    Grey Wolf Optimizer (GWO) implementation.
    
    GWO is a metaheuristic algorithm inspired by the hunting behavior of grey wolves.
    It mimics the social hierarchy and hunting mechanism of grey wolves in nature.
    """
    
    def __init__(self, 
                 objective_func: Callable[[np.ndarray], float],
                 dim: int,
                 lb: float = -100.0,
                 ub: float = 100.0,
                 num_wolves: int = 30,
                 max_iter: int = 500,
                 seed: Optional[int] = None):
        """
        Initialize the Grey Wolf Optimizer.
        
        Args:
            objective_func: The objective function to minimize
            dim: Dimension of the search space
            lb: Lower bound for all dimensions
            ub: Upper bound for all dimensions
            num_wolves: Number of wolves in the population
            max_iter: Maximum number of iterations
            seed: Random seed for reproducibility
        """
        self.objective_func = objective_func
        self.dim = dim
        self.lb = lb
        self.ub = ub
        self.num_wolves = num_wolves
        self.max_iter = max_iter
        
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        
        # Initialize wolf population
        self.wolves = []
        self.alpha = None  # Best wolf
        self.beta = None   # Second best wolf
        self.delta = None  # Third best wolf
        
        # History for plotting
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.alpha_positions = []
        
        self._initialize_population()
    
    def _initialize_population(self):
        """Initialize the wolf population with random positions."""
        for _ in range(self.num_wolves):
            position = np.random.uniform(self.lb, self.ub, self.dim)
            fitness = self.objective_func(position)
            wolf = Wolf(position, fitness)
            self.wolves.append(wolf)
        
        self._update_alpha_beta_delta()
    
    def _update_alpha_beta_delta(self):
        """Update the alpha, beta, and delta wolves based on fitness."""
        # Sort wolves by fitness (minimization problem)
        sorted_wolves = sorted(self.wolves, key=lambda w: w.fitness)
        
        self.alpha = sorted_wolves[0]
        self.beta = sorted_wolves[1]
        self.delta = sorted_wolves[2]
    
    def _calculate_a(self, iteration: int) -> float:
        """Calculate the parameter 'a' which decreases linearly from 2 to 0."""
        return 2 - iteration * (2 / self.max_iter)
    
    def _calculate_coefficients(self, a: float) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate the coefficients A and C for the hunting mechanism."""
        r1 = np.random.random()
        r2 = np.random.random()
        
        A = 2 * a * r1 - a
        C = 2 * r2
        
        return A, C
    
    def _update_wolf_position(self, wolf: Wolf, iteration: int):
        """Update a wolf's position using the GWO hunting mechanism."""
        a = self._calculate_a(iteration)
        
        # Calculate new position based on alpha, beta, and delta
        new_position = np.zeros(self.dim)
        
        for leader in [self.alpha, self.beta, self.delta]:
            A, C = self._calculate_coefficients(a)
            
            D = np.abs(C * leader.position - wolf.position)
            X = leader.position - A * D
            
            new_position += X
        
        # Average the positions from all three leaders
        new_position /= 3
        
        # Ensure bounds
        new_position = np.clip(new_position, self.lb, self.ub)
        
        # Update wolf position and fitness
        wolf.update_position(new_position)
        wolf.update_fitness(self.objective_func(new_position))
    
    def optimize(self, verbose: bool = True) -> Tuple[np.ndarray, float, dict]:
        """
        Run the Grey Wolf Optimizer.
        
        Returns:
            Tuple of (best_position, best_fitness, history_dict)
        """
        start_time = time.time()
        
        if verbose:
            print(f"Starting GWO optimization with {self.num_wolves} wolves")
            print(f"Search space: {self.dim} dimensions, bounds: [{self.lb}, {self.ub}]")
            print(f"Maximum iterations: {self.max_iter}")
            print("-" * 50)
        
        for iteration in range(self.max_iter):
            # Update all wolf positions
            for wolf in self.wolves:
                self._update_wolf_position(wolf, iteration)
            
            # Update alpha, beta, delta
            self._update_alpha_beta_delta()
            
            # Record history
            self.best_fitness_history.append(self.alpha.fitness)
            self.avg_fitness_history.append(np.mean([w.fitness for w in self.wolves]))
            self.alpha_positions.append(self.alpha.position.copy())
            
            # Print progress
            if verbose and (iteration + 1) % 50 == 0:
                print(f"Iteration {iteration + 1}/{self.max_iter}: "
                      f"Best fitness = {self.alpha.fitness:.6f}")
        
        end_time = time.time()
        
        if verbose:
            print("-" * 50)
            print(f"Optimization completed in {end_time - start_time:.2f} seconds")
            print(f"Best fitness: {self.alpha.fitness:.6f}")
            print(f"Best position: {self.alpha.position}")
        
        history = {
            'best_fitness': self.best_fitness_history,
            'avg_fitness': self.avg_fitness_history,
            'alpha_positions': self.alpha_positions,
            'execution_time': end_time - start_time
        }
        
        return self.alpha.position, self.alpha.fitness, history
    
    def plot_convergence(self, figsize: Tuple[int, int] = (12, 8)):
        """Plot the convergence history of the optimization."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
        
        # Plot fitness convergence
        ax1.plot(self.best_fitness_history, 'b-', label='Best Fitness', linewidth=2)
        ax1.plot(self.avg_fitness_history, 'r--', label='Average Fitness', linewidth=1)
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('Fitness Value')
        ax1.set_title('GWO Convergence History')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot alpha position evolution (first 3 dimensions)
        alpha_positions = np.array(self.alpha_positions)
        if self.dim >= 3:
            ax2.plot(alpha_positions[:, 0], 'b-', label='Dimension 1', linewidth=2)
            ax2.plot(alpha_positions[:, 1], 'r-', label='Dimension 2', linewidth=2)
            ax2.plot(alpha_positions[:, 2], 'g-', label='Dimension 3', linewidth=2)
        else:
            for i in range(self.dim):
                ax2.plot(alpha_positions[:, i], label=f'Dimension {i+1}', linewidth=2)
        
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Position Value')
        ax2.set_title('Alpha Wolf Position Evolution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def get_statistics(self) -> dict:
        """Get optimization statistics."""
        return {
            'best_fitness': self.alpha.fitness,
            'best_position': self.alpha.position,
            'final_population_fitness': [w.fitness for w in self.wolves],
            'fitness_std': np.std([w.fitness for w in self.wolves]),
            'convergence_iteration': np.argmin(self.best_fitness_history) + 1
        }