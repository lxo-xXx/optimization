import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Callable
import random
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Wolf:
    """Represents a wolf in the GWO algorithm"""
    position: np.ndarray
    fitness: np.ndarray  # Multi-objective fitness values
    
    def __post_init__(self):
        self.position = np.array(self.position)
        self.fitness = np.array(self.fitness)

class BenchmarkProblem(ABC):
    """Abstract base class for benchmark problems"""
    
    @abstractmethod
    def evaluate(self, x: np.ndarray) -> np.ndarray:
        """Evaluate the objective functions for given decision variables"""
        pass
    
    @abstractmethod
    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get lower and upper bounds for decision variables"""
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """Get the dimension of decision variables"""
        pass

class UF1(BenchmarkProblem):
    """UF1 benchmark problem"""
    
    def __init__(self, n_vars: int = 30):
        self.n_vars = n_vars
    
    def evaluate(self, x: np.ndarray) -> np.ndarray:
        """
        UF1: Two-objective optimization problem
        f1(x) = x1 + 2/|J1| * sum((x_j - sin(6*pi*x1 + j*pi/n))^2) for j in J1
        f2(x) = 1 - sqrt(x1) + 2/|J2| * sum((x_j - sin(6*pi*x1 + j*pi/n))^2) for j in J2
        where J1 = {j | j is odd, 2 <= j <= n}, J2 = {j | j is even, 2 <= j <= n}
        """
        n = len(x)
        x1 = x[0]
        
        # Calculate J1 (odd indices) and J2 (even indices)
        J1_sum = 0
        J2_sum = 0
        J1_count = 0
        J2_count = 0
        
        for j in range(2, n + 1):  # 1-indexed in formula, 0-indexed in implementation
            idx = j - 1  # Convert to 0-indexed
            if j % 2 == 1:  # Odd j (J1)
                J1_sum += (x[idx] - np.sin(6 * np.pi * x1 + j * np.pi / n)) ** 2
                J1_count += 1
            else:  # Even j (J2)
                J2_sum += (x[idx] - np.sin(6 * np.pi * x1 + j * np.pi / n)) ** 2
                J2_count += 1
        
        # Objective functions
        f1 = x1 + (2.0 / max(J1_count, 1)) * J1_sum
        f2 = 1 - np.sqrt(x1) + (2.0 / max(J2_count, 1)) * J2_sum
        
        return np.array([f1, f2])
    
    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        lower = np.zeros(self.n_vars)
        upper = np.ones(self.n_vars)
        lower[1:] = -1  # x2, x3, ..., xn in [-1, 1]
        return lower, upper
    
    def get_dimension(self) -> int:
        return self.n_vars

class UF7(BenchmarkProblem):
    """UF7 benchmark problem"""
    
    def __init__(self, n_vars: int = 30):
        self.n_vars = n_vars
    
    def evaluate(self, x: np.ndarray) -> np.ndarray:
        """
        UF7: Two-objective optimization problem with more complex structure
        """
        n = len(x)
        x1 = x[0]
        
        # Calculate sums for odd and even indices
        sum_odd = 0
        sum_even = 0
        count_odd = 0
        count_even = 0
        
        for j in range(2, n + 1):
            idx = j - 1
            y_j = x[idx] - np.sin(6 * np.pi * x1 + j * np.pi / n)
            
            if j % 2 == 1:  # Odd
                sum_odd += y_j ** 2
                count_odd += 1
            else:  # Even
                sum_even += y_j ** 2
                count_even += 1
        
        # Objective functions for UF7
        f1 = np.power(x1, 0.2) + (2.0 / max(count_odd, 1)) * sum_odd
        f2 = 1 - np.power(x1, 0.2) + (2.0 / max(count_even, 1)) * sum_even
        
        return np.array([f1, f2])
    
    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        lower = np.zeros(self.n_vars)
        upper = np.ones(self.n_vars)
        lower[1:] = -1
        return lower, upper
    
    def get_dimension(self) -> int:
        return self.n_vars

class MultiObjectiveGWO:
    """Multi-Objective Grey Wolf Optimization Algorithm"""
    
    def __init__(self, 
                 problem: BenchmarkProblem,
                 n_wolves: int = 100,
                 max_iterations: int = 500,
                 archive_size: int = 100):
        self.problem = problem
        self.n_wolves = n_wolves
        self.max_iterations = max_iterations
        self.archive_size = archive_size
        self.dimension = problem.get_dimension()
        self.lower_bounds, self.upper_bounds = problem.get_bounds()
        
        # Initialize population
        self.wolves = []
        self.archive = []  # External archive for Pareto optimal solutions
        
        # Leaders (alpha, beta, delta)
        self.alpha = None
        self.beta = None
        self.delta = None
        
        # Convergence tracking
        self.convergence_data = []
    
    def initialize_population(self):
        """Initialize the wolf population randomly"""
        self.wolves = []
        for _ in range(self.n_wolves):
            position = np.random.uniform(self.lower_bounds, self.upper_bounds)
            fitness = self.problem.evaluate(position)
            wolf = Wolf(position, fitness)
            self.wolves.append(wolf)
            
            # Add to archive
            self.update_archive(wolf)
    
    def dominates(self, sol1: Wolf, sol2: Wolf) -> bool:
        """Check if sol1 dominates sol2 (Pareto dominance)"""
        better_in_all = np.all(sol1.fitness <= sol2.fitness)
        better_in_at_least_one = np.any(sol1.fitness < sol2.fitness)
        return better_in_all and better_in_at_least_one
    
    def update_archive(self, new_wolf: Wolf):
        """Update the external archive with non-dominated solutions"""
        # Remove dominated solutions from archive
        self.archive = [wolf for wolf in self.archive if not self.dominates(new_wolf, wolf)]
        
        # Add new wolf if it's not dominated by any solution in archive
        if not any(self.dominates(wolf, new_wolf) for wolf in self.archive):
            self.archive.append(Wolf(new_wolf.position.copy(), new_wolf.fitness.copy()))
        
        # Maintain archive size
        if len(self.archive) > self.archive_size:
            # Remove crowded solutions (simplified crowding distance)
            self.archive = self.select_diverse_solutions(self.archive, self.archive_size)
    
    def select_diverse_solutions(self, solutions: List[Wolf], size: int) -> List[Wolf]:
        """Select diverse solutions using crowding distance"""
        if len(solutions) <= size:
            return solutions
        
        # Calculate crowding distance
        n_obj = len(solutions[0].fitness)
        distances = np.zeros(len(solutions))
        
        for obj in range(n_obj):
            # Sort by objective
            sorted_indices = np.argsort([sol.fitness[obj] for sol in solutions])
            
            # Boundary solutions get infinite distance
            distances[sorted_indices[0]] = float('inf')
            distances[sorted_indices[-1]] = float('inf')
            
            # Calculate distances for intermediate solutions
            obj_min = solutions[sorted_indices[0]].fitness[obj]
            obj_max = solutions[sorted_indices[-1]].fitness[obj]
            
            if obj_max - obj_min > 0:
                for i in range(1, len(sorted_indices) - 1):
                    idx = sorted_indices[i]
                    prev_idx = sorted_indices[i - 1]
                    next_idx = sorted_indices[i + 1]
                    
                    distances[idx] += (solutions[next_idx].fitness[obj] - 
                                     solutions[prev_idx].fitness[obj]) / (obj_max - obj_min)
        
        # Select solutions with highest crowding distance
        selected_indices = np.argsort(distances)[-size:]
        return [solutions[i] for i in selected_indices]
    
    def select_leaders(self):
        """Select alpha, beta, and delta wolves from archive"""
        if len(self.archive) == 0:
            return
        
        # Select leaders using different strategies
        # Alpha: Random selection from archive
        self.alpha = random.choice(self.archive)
        
        # Beta: Select based on different criteria
        remaining = [w for w in self.archive if not np.array_equal(w.position, self.alpha.position)]
        if remaining:
            self.beta = random.choice(remaining)
        else:
            self.beta = self.alpha
        
        # Delta: Another selection
        remaining = [w for w in self.archive if not np.array_equal(w.position, self.alpha.position) 
                    and not np.array_equal(w.position, self.beta.position)]
        if remaining:
            self.delta = random.choice(remaining)
        else:
            self.delta = self.beta
    
    def update_position(self, wolf: Wolf, iteration: int) -> Wolf:
        """Update wolf position based on alpha, beta, and delta"""
        a = 2 - 2 * iteration / self.max_iterations  # Linearly decreasing from 2 to 0
        
        # Calculate positions based on alpha, beta, and delta
        positions = []
        
        for leader in [self.alpha, self.beta, self.delta]:
            if leader is None:
                continue
                
            r1 = np.random.random(self.dimension)
            r2 = np.random.random(self.dimension)
            
            A = 2 * a * r1 - a
            C = 2 * r2
            
            D = np.abs(C * leader.position - wolf.position)
            X = leader.position - A * D
            
            positions.append(X)
        
        # Average the positions
        if positions:
            new_position = np.mean(positions, axis=0)
        else:
            new_position = wolf.position.copy()
        
        # Ensure bounds
        new_position = np.clip(new_position, self.lower_bounds, self.upper_bounds)
        
        # Evaluate new position
        new_fitness = self.problem.evaluate(new_position)
        
        return Wolf(new_position, new_fitness)
    
    def optimize(self) -> List[Wolf]:
        """Main optimization loop"""
        print("Initializing population...")
        self.initialize_population()
        
        print(f"Starting optimization for {self.max_iterations} iterations...")
        
        for iteration in range(self.max_iterations):
            # Select leaders from archive
            self.select_leaders()
            
            # Update each wolf
            new_wolves = []
            for wolf in self.wolves:
                new_wolf = self.update_position(wolf, iteration)
                
                # Update archive
                self.update_archive(new_wolf)
                
                new_wolves.append(new_wolf)
            
            self.wolves = new_wolves
            
            # Track convergence
            if len(self.archive) > 0:
                avg_f1 = np.mean([w.fitness[0] for w in self.archive])
                avg_f2 = np.mean([w.fitness[1] for w in self.archive])
                self.convergence_data.append([iteration, len(self.archive), avg_f1, avg_f2])
            
            if iteration % 50 == 0:
                print(f"Iteration {iteration}: Archive size = {len(self.archive)}")
        
        print(f"Optimization completed. Final archive size: {len(self.archive)}")
        return self.archive
    
    def plot_results(self, title: str = "Pareto Front"):
        """Plot the Pareto front"""
        if not self.archive:
            print("No solutions in archive to plot.")
            return
        
        # Extract objective values
        f1_values = [wolf.fitness[0] for wolf in self.archive]
        f2_values = [wolf.fitness[1] for wolf in self.archive]
        
        plt.figure(figsize=(10, 6))
        plt.scatter(f1_values, f2_values, c='red', alpha=0.7, s=50)
        plt.xlabel('f1')
        plt.ylabel('f2')
        plt.title(f'{title} - Pareto Front')
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def plot_convergence(self):
        """Plot convergence characteristics"""
        if not self.convergence_data:
            print("No convergence data to plot.")
            return
        
        data = np.array(self.convergence_data)
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        
        # Archive size over iterations
        ax1.plot(data[:, 0], data[:, 1])
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('Archive Size')
        ax1.set_title('Archive Size Evolution')
        ax1.grid(True, alpha=0.3)
        
        # Average f1 over iterations
        ax2.plot(data[:, 0], data[:, 2])
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Average f1')
        ax2.set_title('Average f1 Evolution')
        ax2.grid(True, alpha=0.3)
        
        # Average f2 over iterations
        ax3.plot(data[:, 0], data[:, 3])
        ax3.set_xlabel('Iteration')
        ax3.set_ylabel('Average f2')
        ax3.set_title('Average f2 Evolution')
        ax3.grid(True, alpha=0.3)
        
        # Combined objectives
        ax4.plot(data[:, 0], data[:, 2], label='f1', alpha=0.7)
        ax4.plot(data[:, 0], data[:, 3], label='f2', alpha=0.7)
        ax4.set_xlabel('Iteration')
        ax4.set_ylabel('Objective Value')
        ax4.set_title('Objectives Evolution')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def main():
    """Main function to run the experiments"""
    print("Multi-Objective Grey Wolf Optimization Algorithm")
    print("=" * 50)
    
    # Test problems
    problems = {
        'UF1': UF1(n_vars=30),
        'UF7': UF7(n_vars=30)
    }
    
    results = {}
    
    for problem_name, problem in problems.items():
        print(f"\nSolving {problem_name} problem...")
        print("-" * 30)
        
        # Initialize GWO
        gwo = MultiObjectiveGWO(
            problem=problem,
            n_wolves=100,
            max_iterations=500,
            archive_size=100
        )
        
        # Optimize
        pareto_front = gwo.optimize()
        results[problem_name] = {
            'pareto_front': pareto_front,
            'gwo_instance': gwo
        }
        
        # Display results
        print(f"Number of Pareto optimal solutions found: {len(pareto_front)}")
        
        if pareto_front:
            f1_values = [sol.fitness[0] for sol in pareto_front]
            f2_values = [sol.fitness[1] for sol in pareto_front]
            
            print(f"f1 range: [{min(f1_values):.4f}, {max(f1_values):.4f}]")
            print(f"f2 range: [{min(f2_values):.4f}, {max(f2_values):.4f}]")
            
            # Plot results
            gwo.plot_results(f"{problem_name} Problem")
            gwo.plot_convergence()
    
    # Compare results
    print("\n" + "=" * 50)
    print("COMPARISON OF RESULTS")
    print("=" * 50)
    
    for problem_name, result in results.items():
        pareto_front = result['pareto_front']
        print(f"\n{problem_name}:")
        print(f"  - Pareto solutions found: {len(pareto_front)}")
        
        if pareto_front:
            f1_values = [sol.fitness[0] for sol in pareto_front]
            f2_values = [sol.fitness[1] for sol in pareto_front]
            
            print(f"  - f1 statistics: min={min(f1_values):.4f}, max={max(f1_values):.4f}, mean={np.mean(f1_values):.4f}")
            print(f"  - f2 statistics: min={min(f2_values):.4f}, max={max(f2_values):.4f}, mean={np.mean(f2_values):.4f}")

if __name__ == "__main__":
    main()