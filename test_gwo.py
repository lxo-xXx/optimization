import numpy as np
import matplotlib.pyplot as plt
from gwo_multi_objective import UF1, UF7, MultiObjectiveGWO

def test_small_run():
    """Test the algorithm with smaller parameters for quick verification"""
    print("Testing Multi-Objective GWO with smaller parameters...")
    
    # Test UF1 with smaller parameters
    print("\n=== Testing UF1 ===")
    problem_uf1 = UF1(n_vars=10)  # Smaller dimension
    
    gwo_uf1 = MultiObjectiveGWO(
        problem=problem_uf1,
        n_wolves=20,      # Smaller population
        max_iterations=50, # Fewer iterations
        archive_size=20   # Smaller archive
    )
    
    pareto_front_uf1 = gwo_uf1.optimize()
    
    print(f"UF1 Results:")
    print(f"  - Pareto solutions found: {len(pareto_front_uf1)}")
    
    if pareto_front_uf1:
        f1_values = [sol.fitness[0] for sol in pareto_front_uf1]
        f2_values = [sol.fitness[1] for sol in pareto_front_uf1]
        print(f"  - f1 range: [{min(f1_values):.4f}, {max(f1_values):.4f}]")
        print(f"  - f2 range: [{min(f2_values):.4f}, {max(f2_values):.4f}]")
        
        # Simple plot
        plt.figure(figsize=(8, 6))
        plt.scatter(f1_values, f2_values, c='red', alpha=0.7)
        plt.xlabel('f1')
        plt.ylabel('f2')
        plt.title('UF1 - Pareto Front (Test Run)')
        plt.grid(True, alpha=0.3)
        plt.savefig('UF1_test_result.png')
        plt.close()
        print("  - Plot saved as UF1_test_result.png")
    
    # Test UF7 with smaller parameters
    print("\n=== Testing UF7 ===")
    problem_uf7 = UF7(n_vars=10)
    
    gwo_uf7 = MultiObjectiveGWO(
        problem=problem_uf7,
        n_wolves=20,
        max_iterations=50,
        archive_size=20
    )
    
    pareto_front_uf7 = gwo_uf7.optimize()
    
    print(f"UF7 Results:")
    print(f"  - Pareto solutions found: {len(pareto_front_uf7)}")
    
    if pareto_front_uf7:
        f1_values = [sol.fitness[0] for sol in pareto_front_uf7]
        f2_values = [sol.fitness[1] for sol in pareto_front_uf7]
        print(f"  - f1 range: [{min(f1_values):.4f}, {max(f1_values):.4f}]")
        print(f"  - f2 range: [{min(f2_values):.4f}, {max(f2_values):.4f}]")
        
        # Simple plot
        plt.figure(figsize=(8, 6))
        plt.scatter(f1_values, f2_values, c='blue', alpha=0.7)
        plt.xlabel('f1')
        plt.ylabel('f2')
        plt.title('UF7 - Pareto Front (Test Run)')
        plt.grid(True, alpha=0.3)
        plt.savefig('UF7_test_result.png')
        plt.close()
        print("  - Plot saved as UF7_test_result.png")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_small_run()