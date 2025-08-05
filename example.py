#!/usr/bin/env python3
"""
Simple example demonstrating GWO usage.
"""

import numpy as np
from gwo_optimizer import GreyWolfOptimizer
from benchmark_functions import BenchmarkFunctions

def main():
    """Demonstrate basic GWO usage."""
    print("🐺 Grey Wolf Optimizer Example")
    print("=" * 40)
    
    # Example 1: Sphere function (easy)
    print("\n1. Optimizing Sphere Function")
    print("-" * 30)
    
    gwo_sphere = GreyWolfOptimizer(
        objective_func=BenchmarkFunctions.sphere,
        dim=5,
        lb=-10,
        ub=10,
        num_wolves=20,
        max_iter=100,
        seed=42
    )
    
    best_pos, best_fit, history = gwo_sphere.optimize(verbose=False)
    print(f"Best position: {best_pos}")
    print(f"Best fitness: {best_fit:.2e}")
    print(f"Expected minimum: 0")
    print(f"Error: {abs(best_fit - 0):.2e}")
    
    # Example 2: Ackley function (challenging)
    print("\n2. Optimizing Ackley Function")
    print("-" * 30)
    
    gwo_ackley = GreyWolfOptimizer(
        objective_func=BenchmarkFunctions.ackley,
        dim=2,
        lb=-32.768,
        ub=32.768,
        num_wolves=30,
        max_iter=200,
        seed=123
    )
    
    best_pos, best_fit, history = gwo_ackley.optimize(verbose=False)
    print(f"Best position: {best_pos}")
    print(f"Best fitness: {best_fit:.2e}")
    print(f"Expected minimum: 0")
    print(f"Error: {abs(best_fit - 0):.2e}")
    
    # Example 3: Custom function
    print("\n3. Optimizing Custom Function")
    print("-" * 30)
    
    def custom_function(x):
        """Custom function: f(x) = sum(x^2) + sin(x[0]) * cos(x[1])"""
        return np.sum(x**2) + np.sin(x[0]) * np.cos(x[1])
    
    gwo_custom = GreyWolfOptimizer(
        objective_func=custom_function,
        dim=3,
        lb=-5,
        ub=5,
        num_wolves=25,
        max_iter=150,
        seed=456
    )
    
    best_pos, best_fit, history = gwo_custom.optimize(verbose=False)
    print(f"Best position: {best_pos}")
    print(f"Best fitness: {best_fit:.6f}")
    
    # Example 4: Show convergence
    print("\n4. Convergence Analysis")
    print("-" * 30)
    
    # Get statistics
    stats = gwo_ackley.get_statistics()
    print(f"Convergence iteration: {stats['convergence_iteration']}")
    print(f"Final population std: {stats['fitness_std']:.2e}")
    print(f"Execution time: {history['execution_time']:.2f} seconds")
    
    print("\n🎉 Example completed successfully!")
    print("The GWO algorithm is working correctly!")

if __name__ == "__main__":
    main()