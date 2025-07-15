"""
Example usage of Advanced GWO with various test functions
"""
import numpy as np
from advanced_gwo import AdvancedGWO
from test_functions import get_test_function

def example_uf1():
    """Example optimization of UF1 function"""
    print("=" * 60)
    print("EXAMPLE 1: UF1 Function Optimization")
    print("=" * 60)
    
    # Get UF1 test function
    test_func = get_test_function('UF1', dim=10)  # Smaller dimension for faster execution
    
    # Create Advanced GWO optimizer
    gwo = AdvancedGWO(
        func=test_func,
        bounds=test_func.bounds,
        pop_size=50,
        max_gen=100,
        archive_size=100,
        F=0.5,        # Differential evolution factor
        CR=0.7,       # Crossover probability
        n_jobs=2,     # Parallel jobs
        verbose=True
    )
    
    # Run optimization
    solutions, objectives = gwo.optimize()
    
    print(f"\nOptimization completed!")
    print(f"Found {len(solutions)} Pareto-optimal solutions")
    print(f"Final hypervolume: {gwo.hypervolume_history[-1]:.4f}")
    
    # Plot results
    gwo.plot_results("UF1 Optimization Results")
    
    return gwo, solutions, objectives

def example_zdt1():
    """Example optimization of ZDT1 function"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: ZDT1 Function Optimization")
    print("=" * 60)
    
    # Get ZDT1 test function
    test_func = get_test_function('ZDT1', dim=10)
    
    # Create Advanced GWO optimizer with different parameters
    gwo = AdvancedGWO(
        func=test_func,
        bounds=test_func.bounds,
        pop_size=40,
        max_gen=80,
        archive_size=80,
        F=0.7,        # Higher DE factor for more exploration
        CR=0.9,       # Higher crossover probability
        n_jobs=2,
        verbose=True
    )
    
    # Run optimization
    solutions, objectives = gwo.optimize()
    
    print(f"\nOptimization completed!")
    print(f"Found {len(solutions)} Pareto-optimal solutions")
    print(f"Final hypervolume: {gwo.hypervolume_history[-1]:.4f}")
    
    # Plot results
    gwo.plot_results("ZDT1 Optimization Results")
    
    return gwo, solutions, objectives

def example_custom_function():
    """Example with a custom multi-objective function"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Custom Multi-Objective Function")
    print("=" * 60)
    
    def custom_function(x):
        """
        Custom 2-objective function
        Minimize: f1 = x1^2 + x2^2
        Minimize: f2 = (x1-1)^2 + (x2-1)^2
        """
        x = np.array(x)
        f1 = x[0]**2 + x[1]**2
        f2 = (x[0] - 1)**2 + (x[1] - 1)**2
        return np.array([f1, f2])
    
    # Define bounds
    bounds = [(-2, 2), (-2, 2)]
    
    # Create Advanced GWO optimizer
    gwo = AdvancedGWO(
        func=custom_function,
        bounds=bounds,
        pop_size=30,
        max_gen=50,
        archive_size=50,
        F=0.5,
        CR=0.8,
        n_jobs=1,  # Single thread for simple function
        verbose=True
    )
    
    # Run optimization
    solutions, objectives = gwo.optimize()
    
    print(f"\nOptimization completed!")
    print(f"Found {len(solutions)} Pareto-optimal solutions")
    print(f"Final hypervolume: {gwo.hypervolume_history[-1]:.4f}")
    
    # Print some example solutions
    print("\nExample Pareto-optimal solutions:")
    for i, (sol, obj) in enumerate(zip(solutions[:5], objectives[:5])):
        print(f"Solution {i+1}: x={sol[:2]}, f={obj}")
    
    # Plot results
    gwo.plot_results("Custom Function Optimization Results")
    
    return gwo, solutions, objectives

def compare_improvements():
    """Compare different improvement features"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Comparing Improvement Features")
    print("=" * 60)
    
    test_func = get_test_function('ZDT2', dim=10)
    
    # Standard configuration
    print("\nRunning with standard configuration...")
    gwo_standard = AdvancedGWO(
        func=test_func,
        bounds=test_func.bounds,
        pop_size=30,
        max_gen=50,
        archive_size=50,
        F=0.5,
        CR=0.5,
        n_jobs=1,
        verbose=False
    )
    
    solutions_std, objectives_std = gwo_standard.optimize()
    hv_std = gwo_standard.hypervolume_history[-1]
    
    # Enhanced configuration
    print("Running with enhanced configuration...")
    gwo_enhanced = AdvancedGWO(
        func=test_func,
        bounds=test_func.bounds,
        pop_size=30,
        max_gen=50,
        archive_size=50,
        F=0.8,        # Higher exploration
        CR=0.9,       # Higher crossover
        n_jobs=2,     # Parallel evaluation
        verbose=False
    )
    
    solutions_enh, objectives_enh = gwo_enhanced.optimize()
    hv_enh = gwo_enhanced.hypervolume_history[-1]
    
    # Compare results
    print(f"\nComparison Results:")
    print(f"Standard config:  HV={hv_std:.4f}, Archive size={len(solutions_std)}")
    print(f"Enhanced config:  HV={hv_enh:.4f}, Archive size={len(solutions_enh)}")
    
    improvement = ((hv_enh - hv_std) / hv_std) * 100 if hv_std > 0 else 0
    print(f"Improvement: {improvement:.2f}%")
    
    return gwo_standard, gwo_enhanced

def main():
    """Run all examples"""
    print("Advanced GWO - Example Usage")
    print("=" * 60)
    
    try:
        # Example 1: UF1 function
        gwo1, sol1, obj1 = example_uf1()
        
        # Example 2: ZDT1 function
        gwo2, sol2, obj2 = example_zdt1()
        
        # Example 3: Custom function
        gwo3, sol3, obj3 = example_custom_function()
        
        # Example 4: Compare configurations
        gwo4_std, gwo4_enh = compare_improvements()
        
        print("\n" + "=" * 60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error in examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()