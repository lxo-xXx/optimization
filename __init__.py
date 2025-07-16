"""
Enhanced Grey Wolf Optimizer for Multi-Objective Optimization

This package provides an enhanced implementation of the Grey Wolf Optimizer (GWO)
with significant improvements for multi-objective optimization problems.

Key Features:
- Self-adaptive archive leader selection
- Hybrid crossover-mutation operators
- Dynamic archive management with clustering
- Nonlinear dynamic reference point
- Vectorized evaluation support

Example:
    >>> from enhanced_gwo import GWO
    >>> from enhanced_gwo.benchmarks import UF1, get_bounds
    >>> 
    >>> bounds = get_bounds('UF1', dim=30)
    >>> gwo = GWO(
    ...     func=UF1,
    ...     dim=30,
    ...     bounds=bounds,
    ...     use_differential_mutation=True,
    ...     use_dynamic_ref=True,
    ...     use_smart_leader_selection=True
    ... )
    >>> positions, objectives, hv_history = gwo.run()
"""

from .gwo import GWO
from .archive import Archive
from .benchmarks import UF1, UF7, get_bounds, get_true_pareto_front
from .domination import dominates, non_dominated_sort, crowding_distance, select_N

__version__ = "1.0.0"
__author__ = "Enhanced GWO Contributors"
__email__ = "your-email@example.com"
__license__ = "MIT"
__description__ = "Enhanced Grey Wolf Optimizer for Multi-Objective Optimization"
__url__ = "https://github.com/your-username/enhanced-gwo"

# Public API
__all__ = [
    # Core algorithm
    'GWO',
    'Archive',
    
    # Benchmark functions
    'UF1',
    'UF7',
    'get_bounds',
    'get_true_pareto_front',
    
    # Utility functions
    'dominates',
    'non_dominated_sort',
    'crowding_distance',
    'select_N',
    
    # Package metadata
    '__version__',
    '__author__',
    '__email__',
    '__license__',
    '__description__',
    '__url__',
]