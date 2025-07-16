#!/usr/bin/env python3
"""
Demonstration script for Enhanced Grey Wolf Optimizer improvements.
This script shows a quick comparison between original and enhanced versions.
"""

import matplotlib.pyplot as plt
import numpy as np
from gwo import GWO
from benchmarks import UF1, UF7, get_bounds


def quick_demo():
    """Run a quick demonstration of the enhanced GWO features."""
    print("🚀 Enhanced Grey Wolf Optimizer - Quick Demo")
    print("=" * 50)
    
    # Reduced parameters for quick demo
    dim = 10
    pop_size = 20
    max_iter = 50
    archive_size = 50
    
    print(f"Demo Configuration:")
    print(f"- Population size: {pop_size}")
    print(f"- Iterations: {max_iter}")
    print(f"- Dimensions: {dim}")
    print(f"- Archive size: {archive_size}")
    
    # Test on UF1 problem
    bounds = get_bounds('UF1', dim)
    ref_point = [2.0, 2.0]
    
    print(f"\n🔄 Running Original GWO on UF1...")
    gwo_original = GWO(
        func=UF1,
        dim=dim,
        bounds=bounds,
        pop_size=pop_size,
        max_iter=max_iter,
        archive_size=archive_size,
        ref_point=ref_point,
        use_differential_mutation=False,
        use_dynamic_ref=False,
        use_smart_leader_selection=False
    )
    
    _, _, hv_original = gwo_original.run()
    
    print(f"\n✨ Running Enhanced GWO on UF1...")
    gwo_enhanced = GWO(
        func=UF1,
        dim=dim,
        bounds=bounds,
        pop_size=pop_size,
        max_iter=max_iter,
        archive_size=archive_size,
        ref_point=ref_point,
        use_differential_mutation=True,
        use_dynamic_ref=True,
        use_smart_leader_selection=True,
        F=0.5,
        CR=0.9
    )
    
    _, _, hv_enhanced = gwo_enhanced.run()
    
    # Compare results
    print(f"\n📊 Results Comparison:")
    print(f"Original GWO:")
    print(f"  - Final hypervolume: {hv_original[-1]:.4f}")
    print(f"  - Archive size: {gwo_original.archive.size()}")
    
    print(f"Enhanced GWO:")
    print(f"  - Final hypervolume: {hv_enhanced[-1]:.4f}")
    print(f"  - Archive size: {gwo_enhanced.archive.size()}")
    
    improvement = ((hv_enhanced[-1] - hv_original[-1]) / hv_original[-1]) * 100 if hv_original[-1] > 0 else 0
    print(f"  - Improvement: {improvement:.2f}%")
    
    # Plot comparison
    plt.figure(figsize=(12, 5))
    
    # Convergence comparison
    plt.subplot(1, 2, 1)
    plt.plot(range(len(hv_original)), hv_original, 'b--', linewidth=2, label='Original GWO')
    plt.plot(range(len(hv_enhanced)), hv_enhanced, 'g-', linewidth=2, label='Enhanced GWO')
    plt.xlabel('Iteration')
    plt.ylabel('Hypervolume')
    plt.title('Convergence Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Pareto front comparison
    plt.subplot(1, 2, 2)
    
    # Plot solutions
    orig_pos, orig_objs = gwo_original.archive.get_all_solutions()
    enh_pos, enh_objs = gwo_enhanced.archive.get_all_solutions()
    
    if orig_objs:
        orig_f1 = [obj[0] for obj in orig_objs]
        orig_f2 = [obj[1] for obj in orig_objs]
        plt.scatter(orig_f1, orig_f2, c='blue', s=30, alpha=0.7, label='Original GWO', marker='o')
    
    if enh_objs:
        enh_f1 = [obj[0] for obj in enh_objs]
        enh_f2 = [obj[1] for obj in enh_objs]
        plt.scatter(enh_f1, enh_f2, c='green', s=30, alpha=0.7, label='Enhanced GWO', marker='^')
    
    plt.xlabel('f1')
    plt.ylabel('f2')
    plt.title('Pareto Front Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('demo_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\n✅ Demo completed! Plot saved as 'demo_comparison.png'")
    
    # Show enhancement features
    print(f"\n🔧 Enhancement Features Demonstrated:")
    print(f"1. ✅ Self-Adaptive Leader Selection")
    print(f"2. ✅ Differential Mutation (DE-inspired)")
    print(f"3. ✅ Dynamic Reference Point")
    print(f"4. ✅ Clustering-based Archive Management")
    print(f"5. ✅ Sigma-sharing Diversity Control")
    
    # Get diversity metrics
    orig_diversity = gwo_original.archive.get_diversity_metrics()
    enh_diversity = gwo_enhanced.archive.get_diversity_metrics()
    
    print(f"\n📏 Diversity Metrics:")
    print(f"Original - Avg distance: {orig_diversity['avg_distance']:.4f}")
    print(f"Enhanced - Avg distance: {enh_diversity['avg_distance']:.4f}")
    
    return {
        'original': {'hv': hv_original, 'gwo': gwo_original},
        'enhanced': {'hv': hv_enhanced, 'gwo': gwo_enhanced}
    }


if __name__ == "__main__":
    results = quick_demo()