#!/usr/bin/env python3
"""
Grey Wolf Optimizer (GWO) Demo Script

This script demonstrates the GWO algorithm on various benchmark functions
and provides comprehensive analysis and visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from typing import Dict, List, Tuple
import seaborn as sns

from gwo_optimizer import GreyWolfOptimizer
from benchmark_functions import BenchmarkFunctions, get_function_info

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class GWODemo:
    """Demo class for showcasing GWO algorithm performance."""
    
    def __init__(self):
        self.function_info = get_function_info()
        self.results = {}
    
    def run_single_test(self, 
                       func_name: str, 
                       dimensions: int = 2, 
                       num_wolves: int = 30,
                       max_iter: int = 500,
                       seed: int = 42) -> Dict:
        """
        Run GWO on a single benchmark function.
        
        Args:
            func_name: Name of the benchmark function
            dimensions: Number of dimensions
            num_wolves: Number of wolves in the population
            max_iter: Maximum number of iterations
            seed: Random seed for reproducibility
            
        Returns:
            Dictionary containing results
        """
        if func_name not in self.function_info:
            raise ValueError(f"Function {func_name} not found in benchmark functions")
        
        func_info = self.function_info[func_name]
        func = func_info['function']
        
        # Handle special cases for 2D functions
        if func_info['dimensions'] == 2 and dimensions != 2:
            print(f"Warning: {func_name} is a 2D function. Setting dimensions to 2.")
            dimensions = 2
        
        # Get domain bounds
        domain = func_info['domain']
        lb, ub = domain[0], domain[1]
        
        print(f"\n{'='*60}")
        print(f"Testing GWO on {func_name.upper()} function")
        print(f"Dimensions: {dimensions}, Wolves: {num_wolves}, Iterations: {max_iter}")
        print(f"Domain: [{lb}, {ub}], Global minimum: {func_info['global_minimum']}")
        print(f"{'='*60}")
        
        # Create and run GWO
        gwo = GreyWolfOptimizer(
            objective_func=func,
            dim=dimensions,
            lb=lb,
            ub=ub,
            num_wolves=num_wolves,
            max_iter=max_iter,
            seed=seed
        )
        
        best_position, best_fitness, history = gwo.optimize(verbose=True)
        
        # Calculate statistics
        stats = gwo.get_statistics()
        
        # Store results
        result = {
            'function_name': func_name,
            'dimensions': dimensions,
            'best_position': best_position,
            'best_fitness': best_fitness,
            'global_minimum': func_info['global_minimum'],
            'error': abs(best_fitness - func_info['global_minimum']),
            'convergence_iteration': stats['convergence_iteration'],
            'execution_time': history['execution_time'],
            'final_population_std': stats['fitness_std'],
            'history': history,
            'optimizer': gwo
        }
        
        self.results[func_name] = result
        
        # Print summary
        print(f"\nResults Summary:")
        print(f"Best fitness: {best_fitness:.6f}")
        print(f"Global minimum: {func_info['global_minimum']}")
        print(f"Error: {result['error']:.6f}")
        print(f"Best position: {best_position}")
        print(f"Convergence at iteration: {stats['convergence_iteration']}")
        print(f"Execution time: {history['execution_time']:.2f} seconds")
        
        return result
    
    def run_comprehensive_test(self, 
                             functions: List[str] = None,
                             dimensions: int = 2,
                             num_wolves: int = 30,
                             max_iter: int = 500) -> Dict:
        """
        Run GWO on multiple benchmark functions.
        
        Args:
            functions: List of function names to test (None for all)
            dimensions: Number of dimensions
            num_wolves: Number of wolves
            max_iter: Maximum iterations
            
        Returns:
            Dictionary with all results
        """
        if functions is None:
            # Test all functions that support the given dimensions
            functions = []
            for name, info in self.function_info.items():
                if info['dimensions'] == 'any' or info['dimensions'] == dimensions:
                    functions.append(name)
        
        print(f"Running comprehensive test on {len(functions)} functions")
        print(f"Dimensions: {dimensions}, Wolves: {num_wolves}, Iterations: {max_iter}")
        
        results = {}
        for i, func_name in enumerate(functions, 1):
            print(f"\nProgress: {i}/{len(functions)}")
            try:
                result = self.run_single_test(
                    func_name=func_name,
                    dimensions=dimensions,
                    num_wolves=num_wolves,
                    max_iter=max_iter,
                    seed=42 + i  # Different seed for each function
                )
                results[func_name] = result
            except Exception as e:
                print(f"Error testing {func_name}: {e}")
                continue
        
        self.results.update(results)
        return results
    
    def plot_convergence_comparison(self, functions: List[str] = None):
        """Plot convergence comparison for multiple functions."""
        if functions is None:
            functions = list(self.results.keys())
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        for i, func_name in enumerate(functions[:4]):  # Plot first 4 functions
            if func_name in self.results:
                result = self.results[func_name]
                history = result['history']
                
                ax = axes[i]
                ax.plot(history['best_fitness'], 'b-', linewidth=2, label='Best Fitness')
                ax.plot(history['avg_fitness'], 'r--', linewidth=1, label='Average Fitness')
                ax.axhline(y=result['global_minimum'], color='g', linestyle=':', 
                          label=f'Global Min: {result["global_minimum"]}')
                
                ax.set_title(f'{func_name.upper()} Function')
                ax.set_xlabel('Iteration')
                ax.set_ylabel('Fitness Value')
                ax.legend()
                ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_performance_summary(self):
        """Plot performance summary across all tested functions."""
        if not self.results:
            print("No results to plot. Run tests first.")
            return
        
        # Prepare data
        func_names = list(self.results.keys())
        errors = [self.results[name]['error'] for name in func_names]
        times = [self.results[name]['execution_time'] for name in func_names]
        convergence_iters = [self.results[name]['convergence_iteration'] for name in func_names]
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Error comparison
        axes[0, 0].bar(func_names, errors, color='skyblue', alpha=0.7)
        axes[0, 0].set_title('Error from Global Minimum')
        axes[0, 0].set_ylabel('Absolute Error')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Execution time comparison
        axes[0, 1].bar(func_names, times, color='lightcoral', alpha=0.7)
        axes[0, 1].set_title('Execution Time')
        axes[0, 1].set_ylabel('Time (seconds)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Convergence iteration comparison
        axes[1, 0].bar(func_names, convergence_iters, color='lightgreen', alpha=0.7)
        axes[1, 0].set_title('Convergence Iteration')
        axes[1, 0].set_ylabel('Iteration')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Fitness vs Time scatter
        axes[1, 1].scatter(times, errors, s=100, alpha=0.7, c='purple')
        axes[1, 1].set_xlabel('Execution Time (seconds)')
        axes[1, 1].set_ylabel('Error')
        axes[1, 1].set_title('Error vs Execution Time')
        
        # Add function names as annotations
        for i, name in enumerate(func_names):
            axes[1, 1].annotate(name, (times[i], errors[i]), 
                               xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.tight_layout()
        plt.show()
    
    def print_summary_table(self):
        """Print a summary table of all results."""
        if not self.results:
            print("No results to display. Run tests first.")
            return
        
        print("\n" + "="*100)
        print("GWO PERFORMANCE SUMMARY")
        print("="*100)
        print(f"{'Function':<15} {'Best Fitness':<15} {'Global Min':<12} {'Error':<10} {'Time(s)':<8} {'Conv. Iter':<10}")
        print("-"*100)
        
        for func_name, result in self.results.items():
            print(f"{func_name:<15} {result['best_fitness']:<15.6f} "
                  f"{result['global_minimum']:<12.6f} {result['error']:<10.6f} "
                  f"{result['execution_time']:<8.2f} {result['convergence_iteration']:<10}")
        
        print("="*100)
    
    def demonstrate_2d_visualization(self, func_name: str = 'ackley'):
        """Demonstrate 2D visualization of a function with GWO optimization."""
        if func_name not in self.function_info:
            print(f"Function {func_name} not found.")
            return
        
        func_info = self.function_info[func_name]
        if func_info['dimensions'] != 2:
            print(f"{func_name} is not a 2D function.")
            return
        
        # Run GWO
        result = self.run_single_test(func_name, dimensions=2, max_iter=200)
        gwo = result['optimizer']
        
        # Create 2D visualization
        func = func_info['function']
        domain = func_info['domain']
        
        # Create meshgrid
        x = np.linspace(domain[0], domain[1], 100)
        y = np.linspace(domain[0], domain[1], 100)
        X, Y = np.meshgrid(x, y)
        
        # Calculate function values
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = func(np.array([X[i, j], Y[i, j]]))
        
        # Plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Function contour plot
        contour = ax1.contour(X, Y, Z, levels=20, cmap='viridis')
        ax1.clabel(contour, inline=True, fontsize=8)
        ax1.set_title(f'{func_name.upper()} Function Contour')
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        
        # Add global minimum
        if func_info['global_minimizer'] != 'varies':
            global_min_pos = func_info['global_minimizer']
            ax1.plot(global_min_pos[0], global_min_pos[1], 'r*', markersize=15, label='Global Minimum')
        
        # Add final wolf positions
        final_positions = np.array([wolf.position for wolf in gwo.wolves])
        ax1.scatter(final_positions[:, 0], final_positions[:, 1], 
                   c='red', s=50, alpha=0.6, label='Final Wolf Positions')
        
        # Add alpha wolf
        ax1.scatter(gwo.alpha.position[0], gwo.alpha.position[1], 
                   c='yellow', s=100, marker='*', label='Alpha Wolf')
        
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Convergence plot
        ax2.plot(gwo.best_fitness_history, 'b-', linewidth=2, label='Best Fitness')
        ax2.plot(gwo.avg_fitness_history, 'r--', linewidth=1, label='Average Fitness')
        ax2.axhline(y=func_info['global_minimum'], color='g', linestyle=':', 
                   label=f'Global Min: {func_info["global_minimum"]}')
        ax2.set_title('Convergence History')
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Fitness Value')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def main():
    """Main demo function."""
    print("🐺 Grey Wolf Optimizer (GWO) Demo")
    print("="*50)
    
    demo = GWODemo()
    
    # Example 1: Single function test
    print("\n1. Single Function Test (Ackley)")
    demo.run_single_test('ackley', dimensions=2, max_iter=200)
    demo.results['ackley']['optimizer'].plot_convergence()
    
    # Example 2: 2D visualization
    print("\n2. 2D Visualization Demo")
    demo.demonstrate_2d_visualization('rastrigin')
    
    # Example 3: Comprehensive test on multiple functions
    print("\n3. Comprehensive Test on Multiple Functions")
    test_functions = ['sphere', 'ackley', 'rastrigin', 'griewank', 'booth', 'matyas']
    demo.run_comprehensive_test(functions=test_functions, dimensions=2, max_iter=200)
    
    # Example 4: Performance analysis
    print("\n4. Performance Analysis")
    demo.plot_convergence_comparison()
    demo.plot_performance_summary()
    demo.print_summary_table()
    
    # Example 5: Higher dimensional test
    print("\n5. Higher Dimensional Test")
    demo.run_single_test('sphere', dimensions=10, max_iter=300)
    
    print("\n🎉 Demo completed successfully!")

if __name__ == "__main__":
    main()