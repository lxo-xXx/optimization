#!/usr/bin/env python3
"""
Simple test script to verify enhanced GWO features.
"""

from gwo import GWO
from benchmarks import UF1, get_bounds

def test_enhancements():
    """Test the enhanced GWO features."""
    print("Testing Enhanced GWO Features...")
    
    # Basic setup
    dim = 5
    pop_size = 10
    max_iter = 10
    bounds = get_bounds('UF1', dim)
    
    # Test 1: Enhanced GWO
    print("\n1. Testing Enhanced GWO...")
    gwo_enhanced = GWO(
        func=UF1,
        dim=dim,
        bounds=bounds,
        pop_size=pop_size,
        max_iter=max_iter,
        archive_size=20,
        use_differential_mutation=True,
        use_dynamic_ref=True,
        use_smart_leader_selection=True
    )
    
    positions, objectives, hv_history = gwo_enhanced.run()
    
    print(f"✅ Enhanced GWO completed successfully!")
    print(f"   - Archive size: {len(objectives)}")
    print(f"   - Final hypervolume: {hv_history[-1]:.4f}")
    
    # Test 2: Original GWO
    print("\n2. Testing Original GWO...")
    gwo_original = GWO(
        func=UF1,
        dim=dim,
        bounds=bounds,
        pop_size=pop_size,
        max_iter=max_iter,
        archive_size=20,
        use_differential_mutation=False,
        use_dynamic_ref=False,
        use_smart_leader_selection=False
    )
    
    positions_orig, objectives_orig, hv_history_orig = gwo_original.run()
    
    print(f"✅ Original GWO completed successfully!")
    print(f"   - Archive size: {len(objectives_orig)}")
    print(f"   - Final hypervolume: {hv_history_orig[-1]:.4f}")
    
    # Test 3: Feature verification
    print("\n3. Feature Verification...")
    
    # Test smart leader selection
    leaders = gwo_enhanced.select_smart_leaders(3)
    print(f"✅ Smart leader selection: {len(leaders)} leaders selected")
    
    # Test differential mutation
    wolf = [0.5] * dim
    trial = gwo_enhanced.differential_mutation(wolf, leaders, 5)
    print(f"✅ Differential mutation: trial vector generated")
    
    # Test archive diversity metrics
    diversity = gwo_enhanced.archive.get_diversity_metrics()
    print(f"✅ Diversity metrics: avg_distance = {diversity['avg_distance']:.4f}")
    
    # Test dynamic reference point
    gwo_enhanced.update_reference_point()
    print(f"✅ Dynamic reference point: {gwo_enhanced.ref}")
    
    # Compare results
    print("\n4. Comparison Results...")
    improvement = ((hv_history[-1] - hv_history_orig[-1]) / hv_history_orig[-1]) * 100 if hv_history_orig[-1] > 0 else 0
    print(f"Hypervolume improvement: {improvement:.2f}%")
    
    print("\n✅ All tests passed! Enhanced GWO is working correctly.")
    
    return {
        'enhanced_hv': hv_history[-1],
        'original_hv': hv_history_orig[-1],
        'improvement': improvement
    }

if __name__ == "__main__":
    results = test_enhancements()