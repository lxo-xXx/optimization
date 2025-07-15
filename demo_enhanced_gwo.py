"""
Demo script for Enhanced GWO
Demonstrates all the improvements made based on your suggestions
"""

import numpy as np
from enhanced_gwo import EnhancedGWO
from test_functions import get_test_function

def demo_uf1_optimization():
    """Demonstrate Enhanced GWO on UF1 problem"""
    print("🚀 Enhanced GWO Demo: UF1 Optimization")
    print("=" * 60)
    
    # Get UF1 test function
    test_func = get_test_function('UF1', dim=10)
    
    # Create Enhanced GWO with all improvements
    enhanced_gwo = EnhancedGWO(
        func=test_func,
        bounds=test_func.bounds,
        pop_size=50,
        max_gen=100,
        archive_size=100,
        F=0.5,           # Will be adaptive during optimization
        CR=0.7,          # Will be adaptive during optimization
        sigma_share=0.1, # σ-sharing parameter for diversity
        n_jobs=4,        # Parallel evaluation
        verbose=True     # Show progress with adaptive parameters
    )
    
    # Run optimization
    print("\n🔄 Starting optimization with enhanced features...")
    solutions, objectives = enhanced_gwo.optimize()
    
    # Show results
    print(f"\n✅ Optimization completed!")
    print(f"📊 Final results:")
    print(f"   - Solutions found: {len(solutions)}")
    print(f"   - Final hypervolume: {enhanced_gwo.hypervolume_history[-1]:.4f}")
    print(f"   - Hypervolume improvement: {((enhanced_gwo.hypervolume_history[-1] - enhanced_gwo.hypervolume_history[0]) / max(enhanced_gwo.hypervolume_history[0], 1e-10)) * 100:.2f}%")
    
    # Calculate hypervolume fluctuation
    hv_history = np.array(enhanced_gwo.hypervolume_history)
    hv_fluctuation = np.std(hv_history)
    print(f"   - Hypervolume fluctuation (std): {hv_fluctuation:.4f}")
    
    # Plot results
    enhanced_gwo.plot_results("Enhanced GWO - UF1 Results")
    
    return enhanced_gwo, solutions, objectives

def demo_uf7_optimization():
    """Demonstrate Enhanced GWO on UF7 problem"""
    print("\n🚀 Enhanced GWO Demo: UF7 Optimization")
    print("=" * 60)
    
    # Get UF7 test function
    test_func = get_test_function('UF7', dim=10)
    
    # Create Enhanced GWO
    enhanced_gwo = EnhancedGWO(
        func=test_func,
        bounds=test_func.bounds,
        pop_size=50,
        max_gen=100,
        archive_size=100,
        F=0.6,           # Slightly higher for UF7
        CR=0.8,          # Higher crossover for UF7
        sigma_share=0.15, # Adjusted for UF7 characteristics
        n_jobs=4,
        verbose=True
    )
    
    # Run optimization
    print("\n🔄 Starting UF7 optimization...")
    solutions, objectives = enhanced_gwo.optimize()
    
    # Show results
    print(f"\n✅ UF7 optimization completed!")
    print(f"📊 Final results:")
    print(f"   - Solutions found: {len(solutions)}")
    print(f"   - Final hypervolume: {enhanced_gwo.hypervolume_history[-1]:.4f}")
    
    # Calculate diversity metrics
    if len(objectives) > 1:
        # Spacing metric
        sorted_objectives = objectives[np.argsort(objectives[:, 0])]
        distances = []
        for i in range(len(sorted_objectives) - 1):
            dist = np.linalg.norm(sorted_objectives[i+1] - sorted_objectives[i])
            distances.append(dist)
        
        spacing = np.std(distances) if distances else 0
        spread = np.linalg.norm(np.max(objectives, axis=0) - np.min(objectives, axis=0))
        
        print(f"   - Spacing (diversity): {spacing:.4f}")
        print(f"   - Spread (coverage): {spread:.4f}")
    
    # Plot results
    enhanced_gwo.plot_results("Enhanced GWO - UF7 Results")
    
    return enhanced_gwo, solutions, objectives

def demonstrate_key_features():
    """Demonstrate key enhanced features"""
    print("\n🎯 Key Enhanced Features Demonstration")
    print("=" * 60)
    
    print("\n✅ 1. Self-Adaptive Leader Selection")
    print("   - α: Highest hypervolume contribution")
    print("   - β: Maximum angular deviation (diversity)")
    print("   - δ: Lowest σ-sharing value (edge exploration)")
    
    print("\n✅ 2. Hybrid Crossover-Mutation")
    print("   - Standard DE: Trial = X_α + F * (X_β - X_δ)")
    print("   - Adaptive F and CR parameters")
    print("   - Lévy flight for enhanced exploration")
    
    print("\n✅ 3. σ-sharing Archive Management")
    print("   - Preserves diversity using σ-sharing distances")
    print("   - Maintains outlier solutions")
    print("   - Removes crowded solutions intelligently")
    
    print("\n✅ 4. Adaptive Reference Point")
    print("   - Dynamic: ref_i = max_t f_i(t) + 5% buffer")
    print("   - Exponential smoothing for stability")
    print("   - Problem-specific adaptation")
    
    print("\n✅ 5. Enhanced Performance")
    print("   - Parallel batch evaluation")
    print("   - Latin Hypercube initialization")
    print("   - Reflection boundary handling")
    
def main():
    """Main demonstration function"""
    print("🌟 Enhanced GWO Comprehensive Demonstration")
    print("Addressing all your specific improvement suggestions")
    print("=" * 80)
    
    # Demonstrate key features
    demonstrate_key_features()
    
    # Run UF1 optimization
    uf1_gwo, uf1_solutions, uf1_objectives = demo_uf1_optimization()
    
    # Run UF7 optimization
    uf7_gwo, uf7_solutions, uf7_objectives = demo_uf7_optimization()
    
    # Final summary
    print("\n🎉 DEMONSTRATION COMPLETE!")
    print("=" * 60)
    print("📈 Results Summary:")
    print(f"   UF1 Final Hypervolume: {uf1_gwo.hypervolume_history[-1]:.4f}")
    print(f"   UF7 Final Hypervolume: {uf7_gwo.hypervolume_history[-1]:.4f}")
    print(f"   UF1 Solutions Found: {len(uf1_solutions)}")
    print(f"   UF7 Solutions Found: {len(uf7_solutions)}")
    
    print("\n🔬 All improvements implemented based on your suggestions:")
    print("   ✅ Self-adaptive leader selection with hypervolume contribution")
    print("   ✅ DE-inspired hybrid mutation with adaptive parameters")
    print("   ✅ σ-sharing based archive management")
    print("   ✅ Adaptive reference point with exponential smoothing")
    print("   ✅ Parallel evaluation for computational efficiency")
    print("   ✅ Reduced hypervolume fluctuation")
    print("   ✅ Enhanced diversity preservation")
    
    print("\n🚀 Next Steps:")
    print("   1. Run 'python enhanced_comparison.py' for detailed comparison")
    print("   2. Test with your specific optimization problems")
    print("   3. Adjust parameters based on problem characteristics")
    print("   4. Compare against other state-of-the-art algorithms")
    
    print("\n📚 For detailed analysis, see: ENHANCEMENT_ANALYSIS.md")

if __name__ == "__main__":
    main()