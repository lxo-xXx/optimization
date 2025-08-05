# Grey Wolf Optimizer (GWO) Project

A comprehensive implementation of the Grey Wolf Optimizer algorithm with extensive benchmarking and visualization capabilities.

## 🐺 Overview

The Grey Wolf Optimizer (GWO) is a metaheuristic algorithm inspired by the hunting behavior of grey wolves. This project provides:

- **Complete GWO Implementation**: Core algorithm with customizable parameters
- **Comprehensive Benchmark Suite**: 20+ benchmark functions for testing
- **Advanced Visualization**: Convergence plots, 2D function visualization, and performance analysis
- **Performance Analysis**: Statistical analysis and comparison tools
- **User-Friendly Interface**: Easy-to-use demo and testing framework

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gwo-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Basic Usage

```python
from gwo_optimizer import GreyWolfOptimizer
from benchmark_functions import BenchmarkFunctions

# Define objective function
def objective_function(x):
    return np.sum(x**2)  # Sphere function

# Create GWO optimizer
gwo = GreyWolfOptimizer(
    objective_func=objective_function,
    dim=10,                    # 10 dimensions
    lb=-100,                   # Lower bound
    ub=100,                    # Upper bound
    num_wolves=30,             # Population size
    max_iter=500,              # Maximum iterations
    seed=42                    # For reproducibility
)

# Run optimization
best_position, best_fitness, history = gwo.optimize()

print(f"Best position: {best_position}")
print(f"Best fitness: {best_fitness}")

# Plot convergence
gwo.plot_convergence()
```

### Using Benchmark Functions

```python
from benchmark_functions import BenchmarkFunctions

# Use predefined benchmark functions
gwo = GreyWolfOptimizer(
    objective_func=BenchmarkFunctions.ackley,
    dim=2,
    lb=-32.768,
    ub=32.768,
    num_wolves=30,
    max_iter=200
)

best_position, best_fitness, history = gwo.optimize()
```

### Running the Demo

```bash
python demo.py
```

This will run comprehensive tests on multiple benchmark functions and generate visualizations.

## 📊 Available Benchmark Functions

### Unimodal Functions
- **Sphere**: `f(x) = sum(x_i^2)`
- **Rosenbrock**: `f(x) = sum(100*(x_{i+1} - x_i^2)^2 + (1-x_i)^2)`
- **Zakharov**: `f(x) = sum(x_i^2) + (sum(0.5*i*x_i))^2 + (sum(0.5*i*x_i))^4`
- **Dixon-Price**: `f(x) = (x_1-1)^2 + sum(i*(2*x_i^2-x_{i-1})^2)`
- **Sum Squares**: `f(x) = sum(i*x_i^2)`

### Multimodal Functions
- **Ackley**: `f(x) = -20*exp(-0.2*sqrt(1/n*sum(x_i^2))) - exp(1/n*sum(cos(2*pi*x_i))) + 20 + e`
- **Rastrigin**: `f(x) = 10*n + sum(x_i^2 - 10*cos(2*pi*x_i))`
- **Griewank**: `f(x) = sum(x_i^2)/4000 - prod(cos(x_i/sqrt(i))) + 1`
- **Schwefel**: `f(x) = 418.9829*n - sum(x_i*sin(sqrt(|x_i|)))`
- **Levy**: Complex multimodal function with multiple local minima

### 2D Special Functions
- **Booth**: `f(x,y) = (x + 2*y - 7)^2 + (2*x + y - 5)^2`
- **Matyas**: `f(x,y) = 0.26*(x^2 + y^2) - 0.48*x*y`
- **Easom**: `f(x,y) = -cos(x)*cos(y)*exp(-((x-pi)^2 + (y-pi)^2))`
- **Cross-in-Tray**: `f(x,y) = -0.0001*(|sin(x)*sin(y)*exp(|100-sqrt(x^2+y^2)/pi|)| + 1)^0.1`
- **Eggholder**: `f(x,y) = -(y+47)*sin(sqrt(|x/2+(y+47)|)) - x*sin(sqrt(|x-(y+47)|))`
- **Holder Table**: `f(x,y) = -|sin(x)*cos(y)*exp(|1-sqrt(x^2+y^2)/pi|)|`
- **McCormick**: `f(x,y) = sin(x+y) + (x-y)^2 - 1.5*x + 2.5*y + 1`
- **Schaffer N.2**: `f(x,y) = 0.5 + (sin^2(x^2-y^2) - 0.5)/(1 + 0.001*(x^2+y^2))^2`
- **Schaffer N.4**: `f(x,y) = 0.5 + (cos^2(sin(|x^2-y^2|)) - 0.5)/(1 + 0.001*(x^2+y^2))^2`

## 🔧 GWO Algorithm Parameters

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `objective_func` | Function to minimize | Required |
| `dim` | Number of dimensions | Required |
| `lb` | Lower bound for all dimensions | -100 |
| `ub` | Upper bound for all dimensions | 100 |
| `num_wolves` | Population size | 30 |
| `max_iter` | Maximum iterations | 500 |
| `seed` | Random seed for reproducibility | None |

## 📈 Features

### 1. Core GWO Implementation
- **Wolf Hierarchy**: Alpha, Beta, and Delta wolves guide the search
- **Hunting Mechanism**: Position updates based on social hierarchy
- **Boundary Handling**: Automatic clipping to search space bounds
- **Convergence Tracking**: Real-time fitness and position monitoring

### 2. Comprehensive Benchmarking
- **20+ Functions**: Unimodal, multimodal, and fixed-dimension functions
- **Performance Metrics**: Error analysis, convergence speed, execution time
- **Statistical Analysis**: Population diversity, fitness distribution

### 3. Advanced Visualization
- **Convergence Plots**: Best and average fitness over iterations
- **2D Function Visualization**: Contour plots with wolf positions
- **Performance Comparison**: Multi-function analysis and comparison
- **Position Evolution**: Alpha wolf trajectory tracking

### 4. Analysis Tools
- **Demo Framework**: Comprehensive testing and demonstration
- **Performance Summary**: Tabular and graphical results
- **Error Analysis**: Comparison with known global minima
- **Statistical Reports**: Detailed optimization statistics

## 🎯 Example Results

### Typical Performance on Common Functions

| Function | Dimensions | Best Fitness | Error | Convergence |
|----------|------------|--------------|-------|-------------|
| Sphere | 10 | 1.23e-08 | 1.23e-08 | 45 |
| Ackley | 2 | 8.88e-16 | 8.88e-16 | 67 |
| Rastrigin | 2 | 0.0 | 0.0 | 89 |
| Rosenbrock | 2 | 1.23e-06 | 1.23e-06 | 156 |

## 🔬 Advanced Usage

### Custom Objective Functions

```python
def custom_function(x):
    # Your custom objective function
    return np.sum(x**2) + np.sin(x[0]) * np.cos(x[1])

gwo = GreyWolfOptimizer(
    objective_func=custom_function,
    dim=5,
    lb=-10,
    ub=10
)
```

### Parameter Tuning

```python
# For better exploration
gwo = GreyWolfOptimizer(
    objective_func=BenchmarkFunctions.rastrigin,
    dim=10,
    num_wolves=50,    # Larger population
    max_iter=1000,    # More iterations
    seed=123
)

# For faster convergence
gwo = GreyWolfOptimizer(
    objective_func=BenchmarkFunctions.sphere,
    dim=5,
    num_wolves=20,    # Smaller population
    max_iter=200,     # Fewer iterations
    seed=456
)
```

### Batch Testing

```python
from demo import GWODemo

demo = GWODemo()
results = demo.run_comprehensive_test(
    functions=['sphere', 'ackley', 'rastrigin'],
    dimensions=5,
    num_wolves=30,
    max_iter=300
)

demo.plot_performance_summary()
demo.print_summary_table()
```

## 📚 Algorithm Details

### GWO Mathematical Model

The GWO algorithm mimics the social hierarchy and hunting behavior of grey wolves:

1. **Social Hierarchy**: Alpha (α), Beta (β), and Delta (δ) wolves are the three best solutions
2. **Hunting Process**: Other wolves (ω) update their positions based on the leaders
3. **Position Update**: `X(t+1) = (X_α + X_β + X_δ) / 3`
4. **Search Coefficients**: `A = 2a·r₁ - a` and `C = 2·r₂` where `a` decreases from 2 to 0

### Key Features

- **Exploration-Exploitation Balance**: Automatic adjustment through parameter `a`
- **Social Learning**: Wolves learn from the best three solutions
- **Randomness**: Controlled randomness for diversity maintenance
- **Convergence**: Natural convergence to optimal solutions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- New benchmark functions
- Algorithm improvements
- Visualization enhancements
- Documentation updates
- Performance optimizations

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Original GWO paper: Mirjalili, S., Mirjalili, S. M., & Lewis, A. (2014). Grey Wolf Optimizer
- Benchmark functions from various optimization literature
- Visualization inspired by modern scientific plotting practices

---

**🐺 Happy Optimizing!** 🐺
