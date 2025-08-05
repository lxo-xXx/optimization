#!/usr/bin/env python3
"""
Simple test script for GWO implementation.
"""

import numpy as np
from gwo_optimizer import GreyWolfOptimizer
from benchmark_functions import BenchmarkFunctions

def test_basic_functionality():
    """Test basic GWO functionality."""
    print("Testing basic GWO functionality...")
    
    # Test with sphere function
    gwo = GreyWolfOptimizer(
        objective_func=BenchmarkFunctions.sphere,
        dim=5,
        lb=-10,
        ub=10,
        num_wolves=20,
        max_iter=100,
        seed=42
    )
    
    best_position, best_fitness, history = gwo.optimize(verbose=False)
    
    print(f"Best fitness: {best_fitness}")
    print(f"Best position: {best_position}")
    print(f"Expected global minimum: 0")
    print(f"Error: {abs(best_fitness - 0)}")
    
    assert best_fitness < 1e-6, f"GWO failed to converge to sphere function minimum. Best fitness: {best_fitness}"
    print("✅ Basic functionality test passed!")

def test_2d_functions():
    """Test GWO on 2D functions."""
    print("\nTesting 2D functions...")
    
    test_functions = [
        ('ackley', BenchmarkFunctions.ackley, -32.768, 32.768, 0),
        ('rastrigin', BenchmarkFunctions.rastrigin, -5.12, 5.12, 0),
        ('booth', BenchmarkFunctions.booth, -10, 10, 0)
    ]
    
    for func_name, func, lb, ub, expected_min in test_functions:
        print(f"Testing {func_name} function...")
        
        gwo = GreyWolfOptimizer(
            objective_func=func,
            dim=2,
            lb=lb,
            ub=ub,
            num_wolves=30,
            max_iter=200,
            seed=42
        )
        
        best_position, best_fitness, history = gwo.optimize(verbose=False)
        
        error = abs(best_fitness - expected_min)
        print(f"  Best fitness: {best_fitness:.6f}")
        print(f"  Error: {error:.6f}")
        
        # For 2D functions, we expect good convergence (relaxed for challenging functions)
        if func_name == 'booth':
            assert error < 0.1, f"{func_name} failed to converge properly. Error: {error}"
        else:
            assert error < 1e-3, f"{func_name} failed to converge properly. Error: {error}"
    
    print("✅ 2D functions test passed!")

def test_convergence_plotting():
    """Test convergence plotting functionality."""
    print("\nTesting convergence plotting...")
    
    gwo = GreyWolfOptimizer(
        objective_func=BenchmarkFunctions.ackley,
        dim=2,
        lb=-32.768,
        ub=32.768,
        num_wolves=20,
        max_iter=50,
        seed=42
    )
    
    best_position, best_fitness, history = gwo.optimize(verbose=False)
    
    # Test that history is properly recorded
    assert len(gwo.best_fitness_history) == 50, "History not properly recorded"
    assert len(gwo.avg_fitness_history) == 50, "Average fitness history not recorded"
    assert len(gwo.alpha_positions) == 50, "Alpha positions not recorded"
    
    # Test statistics
    stats = gwo.get_statistics()
    assert 'best_fitness' in stats, "Statistics missing best_fitness"
    assert 'best_position' in stats, "Statistics missing best_position"
    assert 'convergence_iteration' in stats, "Statistics missing convergence_iteration"
    
    print("✅ Convergence plotting test passed!")

def test_benchmark_functions():
    """Test benchmark functions."""
    print("\nTesting benchmark functions...")
    
    # Test a few functions
    test_cases = [
        (np.array([0, 0]), BenchmarkFunctions.sphere, 0),
        (np.array([1, 1]), BenchmarkFunctions.rosenbrock, 0),
        (np.array([0, 0]), BenchmarkFunctions.ackley, 0),
        (np.array([0, 0]), BenchmarkFunctions.rastrigin, 0)
    ]
    
    for position, func, expected in test_cases:
        result = func(position)
        assert abs(result - expected) < 1e-10, f"Benchmark function test failed. Expected {expected}, got {result}"
    
    print("✅ Benchmark functions test passed!")

def main():
    """Run all tests."""
    print("🐺 GWO Test Suite")
    print("=" * 40)
    
    try:
        test_basic_functionality()
        test_2d_functions()
        test_convergence_plotting()
        test_benchmark_functions()
        
        print("\n🎉 All tests passed successfully!")
        print("The GWO implementation is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    main()