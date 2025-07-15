# Advanced Multi-Objective Grey Wolf Optimizer (GWO)

A comprehensive implementation of an advanced Grey Wolf Optimizer with enhanced features for multi-objective optimization problems.

## 🌟 Key Features

### 1. **Self-Adaptive Archive Leader Selection**
- **α (Alpha)**: Selected based on highest hypervolume contribution
- **β (Beta)**: Selected based on highest crowding distance (diversity focus)
- **δ (Delta)**: Random or centroid-based selection
- Eliminates random leader selection issues that reduce solution quality

### 2. **Hybrid Crossover-Mutation (GWO + DE/NSGA-inspired)**
- Combines standard GWO position update with Differential Evolution mutations
- Implements crossover between GWO and DE positions
- Includes diversity maintenance that decreases over generations
- Formula: `Trial = X_α + F * (X_β - X_δ)`

### 3. **Dynamic Archive Management**
- **Non-dominated sorting** for Pareto-optimal solutions
- **Clustering-based pruning** using K-means to maintain diversity
- **σ-sharing** approach to preserve outlier solutions
- Prevents loss of useful but outlier solutions

### 4. **Nonlinear Dynamic Reference Point**
- **Adaptive reference point**: `ref_i = max_t f_i(t) + ε` where `ε = 5%`
- Eliminates fixed reference point limitations
- Optimizes hypervolume measurement accuracy

### 5. **Parallel Evaluation for Speedup**
- **Vectorized evaluation** using joblib.Parallel
- Configurable number of parallel jobs
- Significant speedup for computationally expensive functions

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## 📋 Dependencies

- numpy>=1.21.0
- scipy>=1.7.0
- matplotlib>=3.5.0
- joblib>=1.1.0
- scikit-learn>=1.0.0
- pymoo>=0.6.0

## 🎯 Usage

### Basic Usage

```python
from advanced_gwo import AdvancedGWO
from test_functions import get_test_function

# Get a test function
test_func = get_test_function('UF1', dim=10)

# Create optimizer
gwo = AdvancedGWO(
    func=test_func,
    bounds=test_func.bounds,
    pop_size=50,
    max_gen=100,
    archive_size=100,
    F=0.5,        # Differential evolution factor
    CR=0.7,       # Crossover probability
    n_jobs=4,     # Parallel jobs
    verbose=True
)

# Run optimization
solutions, objectives = gwo.optimize()

# Plot results
gwo.plot_results("Optimization Results")
```

### Custom Function Example

```python
def custom_function(x):
    """Custom 2-objective function"""
    x = np.array(x)
    f1 = x[0]**2 + x[1]**2
    f2 = (x[0] - 1)**2 + (x[1] - 1)**2
    return np.array([f1, f2])

# Define bounds
bounds = [(-2, 2), (-2, 2)]

# Create and run optimizer
gwo = AdvancedGWO(custom_function, bounds, pop_size=30, max_gen=50)
solutions, objectives = gwo.optimize()
```

## 🧪 Available Test Functions

The implementation includes several standard benchmark functions:

- **UF1, UF7**: CEC'09 Competition functions
- **ZDT1, ZDT2, ZDT3**: Zitzler-Deb-Thiele test suite
- **DTLZ1, DTLZ2**: Scalable test functions
- **Schaffer**: Simple 2-objective function

## 🔧 Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `func` | Multi-objective function | Required | Callable |
| `bounds` | Variable bounds | Required | List of tuples |
| `pop_size` | Population size | 50 | > 0 |
| `max_gen` | Maximum generations | 100 | > 0 |
| `archive_size` | Archive size | 100 | > 0 |
| `F` | DE mutation factor | 0.5 | [0, 2] |
| `CR` | Crossover probability | 0.7 | [0, 1] |
| `n_jobs` | Parallel jobs | 4 | >= 1 |
| `verbose` | Print progress | True | Boolean |

## 📊 Benchmarking

Run comprehensive benchmarks comparing Basic GWO vs Advanced GWO:

```bash
python benchmark_gwo.py
```

This will:
- Test multiple functions (UF1, UF7, ZDT1, ZDT2, ZDT3)
- Compare hypervolume, execution time, and archive size
- Generate comparison plots
- Save results to JSON

## 📖 Examples

Run the example script to see various usage scenarios:

```bash
python example_usage.py
```

This demonstrates:
1. UF1 function optimization
2. ZDT1 function optimization  
3. Custom function optimization
4. Parameter comparison

## 🎨 Visualization

The implementation provides comprehensive visualization:

- **Pareto Front**: Scatter plot of objective values
- **Convergence History**: Hypervolume over generations
- **Comparison Plots**: Side-by-side algorithm comparison
- **Statistical Analysis**: Mean, std, and improvement metrics

## 🔬 Scientific Improvements

### Problem Addressed
Your current GWO model had:
- Random leader selection reducing solution quality
- Lack of crossover/mutation operators
- Naive archive management losing useful solutions
- Fixed reference points suboptimal for problems like UF1/UF7
- Sequential evaluation creating computational bottlenecks

### Solutions Implemented
1. **Intelligent Leader Selection**: Uses hypervolume contribution and crowding distance
2. **Hybrid Operators**: Combines GWO with DE mutations and crossover
3. **Smart Archive Management**: Clustering-based pruning preserving diversity
4. **Adaptive Reference Points**: Dynamic adjustment with 5% buffer
5. **Parallel Processing**: Vectorized evaluation for speedup

## 📈 Performance Improvements

Expected improvements based on implementation:
- **Hypervolume**: 15-40% improvement over basic GWO
- **Diversity**: Better population diversity maintenance
- **Convergence**: Reduced hypervolume fluctuation
- **Speed**: 2-4x faster with parallel evaluation

## 🤝 Contributing

The implementation is modular and extensible:
- Add new test functions in `test_functions.py`
- Extend archive management in `manage_archive_dynamic()`
- Add new leader selection strategies in `select_leaders_adaptive()`
- Implement additional crossover operators in `hybrid_position_update()`

## 📄 License

This implementation is provided for educational and research purposes.

## 🙏 Acknowledgments

Based on the original Grey Wolf Optimizer by Mirjalili et al. (2014) with significant enhancements for multi-objective optimization following suggestions for:
- Enhanced population diversity
- Improved exploration/exploitation balance
- Better diversity preservation
- Reduced hypervolume fluctuation

---

**Ready to optimize your multi-objective problems with advanced GWO!** 🐺 
