# Grey Wolf Optimizer with Advanced Features

A comprehensive implementation of the Grey Wolf Optimizer (GWO) with advanced features for multi-objective optimization, including Opposition-Based Learning, Elite Archive, and adaptive nonlinear parameter decay.

## Features

### Core Algorithm
- **Grey Wolf Optimizer (GWO)**: Swarm-based metaheuristic inspired by wolf pack hierarchy
- **Multi-Objective Support**: Handles multiple conflicting objectives simultaneously
- **Modular Design**: Clean, extensible object-oriented architecture

### Advanced Enhancements
- **Opposition-Based Learning (OBL)**: Improves initial population diversity and convergence speed
- **Elite Archive**: Maintains non-dominated solutions with diversity preservation
- **Adaptive Nonlinear Parameter Decay**: Balances exploration and exploitation effectively
- **Hypervolume Tracking**: Monitors convergence quality over iterations

### Benchmark Problems
- **UF1**: Concave Pareto front (f₂ = 1 - √f₁)
- **UF7**: Linear Pareto front (f₂ = 1 - f₁)
- Both problems from CEC 2009 UF suite with 30 decision variables

## Installation

1. Clone or download the repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```python
from gwo import GWO
from benchmarks import UF1, get_bounds

# Configure the algorithm
bounds = get_bounds('UF1', dim=30)
gwo = GWO(
    func=UF1,
    dim=30,
    bounds=bounds,
    pop_size=50,
    max_iter=200,
    archive_size=100,
    power_a=3
)

# Run optimization
final_positions, final_objectives, hv_history = gwo.run()
```

### Complete Experiment
```bash
python main.py
```

This runs the complete experimental evaluation on both UF1 and UF7 problems, generating:
- Convergence plots showing hypervolume progression
- Pareto front approximations compared to true fronts
- Detailed analysis and statistics

## Algorithm Components

### 1. Dominance and Selection (`domination.py`)
- `dominates()`: Pareto dominance checking
- `non_dominated_sort()`: Fast non-dominated sorting (NSGA-II style)
- `crowding_distance()`: Diversity estimation
- `select_N()`: Multi-objective selection

### 2. Elite Archive (`archive.py`)
- Maintains non-dominated solutions
- Automatic dominance filtering
- Diversity-based size management
- Leader selection for wolf guidance

### 3. Benchmark Functions (`benchmarks.py`)
- UF1 and UF7 implementations
- True Pareto front generation
- Problem bounds specification

### 4. GWO Algorithm (`gwo.py`)
- Opposition-Based Learning initialization
- Adaptive parameter decay: `a(t) = 2(1 - (t/T)³)`
- Multi-objective position updates
- Hypervolume convergence tracking

## Mathematical Formulation

### GWO Position Update
For each wolf, the position is updated based on three leaders (α, β, δ):

```
D₁ = |C₁ · X_α - X_wolf|,  X₁ = X_α - A₁ · D₁
D₂ = |C₂ · X_β - X_wolf|,  X₂ = X_β - A₂ · D₂  
D₃ = |C₃ · X_δ - X_wolf|,  X₃ = X_δ - A₃ · D₃

X_wolf(t+1) = (X₁ + X₂ + X₃) / 3
```

Where:
- `A = 2a·r - a` and `C = 2r` (coefficient vectors)
- `a = 2(1 - (t/T)³)` (adaptive parameter)
- `r` is random vector in [0,1]

### Opposition-Based Learning
For each decision variable:
```
x'ᵢ = lbᵢ + ubᵢ - xᵢ
```
Where `lbᵢ` and `ubᵢ` are lower and upper bounds.

### Hypervolume Calculation
For 2D problems with reference point (ref₁, ref₂):
```
HV = Σ (f₁ᵢ₊₁ - f₁ᵢ) × (ref₂ - f₂ᵢ)
```

## Experimental Results

### Configuration
- Population size: 50 wolves
- Iterations: 200
- Archive size: 100
- Decision variables: 30
- Nonlinear decay power: 3

### Performance Metrics
- **Hypervolume**: Measures convergence quality and diversity
- **Pareto Front Coverage**: Visual comparison with true fronts
- **Convergence Speed**: Rate of hypervolume improvement

### Key Findings
1. **UF7 achieves higher hypervolume** due to its linear Pareto front
2. **UF1 requires careful diversity maintenance** for its concave front
3. **Opposition-Based Learning provides strong initialization**
4. **Elite Archive maintains solution quality** throughout optimization
5. **Adaptive parameter decay balances exploration/exploitation**

## File Structure

```
├── domination.py      # Multi-objective utilities
├── archive.py         # Elite archive management
├── benchmarks.py      # UF1 and UF7 test problems
├── gwo.py            # Main GWO algorithm
├── main.py           # Experimental evaluation
├── requirements.txt   # Dependencies
└── README.md         # This file
```

## Algorithm Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|--------|
| `pop_size` | Population size | 50 | 20-100 |
| `max_iter` | Maximum iterations | 200 | 100-500 |
| `archive_size` | Archive capacity | 100 | 50-200 |
| `power_a` | Nonlinear decay power | 3 | 1-5 |
| `dim` | Decision variables | 30 | 10-50 |

## Extending the Implementation

### Adding New Problems
```python
def new_problem(sol):
    # Implement your objective function
    f1 = ...  # First objective
    f2 = ...  # Second objective
    return [f1, f2]
```

### Custom Archive Strategies
```python
class CustomArchive(Archive):
    def get_leaders(self, k):
        # Implement custom leader selection
        return selected_leaders
```

### Alternative Parameter Schedules
```python
def custom_decay(iteration, max_iter):
    # Implement custom parameter decay
    return a_value
```

## Performance Tips

1. **Population Size**: Balance between diversity and computational cost
2. **Archive Size**: Larger archives preserve more solutions but slow convergence
3. **Decay Power**: Higher values delay exploitation, lower values speed convergence
4. **Reference Point**: Should be beyond the worst expected objective values

## References

1. Mirjalili, S., Mirjalili, S. M., & Lewis, A. (2014). Grey wolf optimizer. *Advances in Engineering Software*, 69, 46-61.

2. Mirjalili, S., Saremi, S., Mirjalili, S. M., & Coelho, L. D. S. (2016). Multi-objective grey wolf optimizer: a novel algorithm for multi-criterion optimization. *Expert Systems with Applications*, 47, 106-119.

3. Zhang, Q., Zhou, A., Zhao, S., Suganthan, P. N., Liu, W., & Tiwari, S. (2008). Multiobjective optimization test instances for the CEC 2009 special session and competition. *University of Essex*, 264, 1-30.

## License

This implementation is provided for educational and research purposes.

## Authors

Implementation by: [Your Name]
Algorithm concept: Seyedali Mirjalili et al. 
