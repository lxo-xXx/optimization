# Multi-Objective Grey Wolf Optimization (MOGWO) Algorithm

This repository contains a complete implementation of the Multi-Objective Grey Wolf Optimization algorithm for solving multi-objective optimization problems, specifically tested on UF1 and UF7 benchmark problems.

## Project Overview

Grey Wolf Optimization (GWO) is a meta-heuristic optimization algorithm inspired by the social hierarchy and hunting behavior of grey wolves. This implementation extends the standard GWO to handle multi-objective optimization problems using Pareto dominance concepts and external archiving.

## Features

- **Multi-Objective Optimization**: Handles problems with multiple conflicting objectives
- **Pareto Front Generation**: Finds a set of non-dominated solutions
- **External Archive**: Maintains diverse Pareto optimal solutions
- **Crowding Distance**: Ensures diversity in the solution set
- **Benchmark Problems**: Implements UF1 and UF7 test problems
- **Visualization**: Generates plots for Pareto fronts and convergence analysis
- **Comprehensive Documentation**: Includes flowcharts, pseudocode, and detailed explanations

## Files Structure

```
├── gwo_multi_objective.py      # Main implementation
├── gwo_pseudocode.md          # Detailed pseudocode
├── gwo_flowchart.py           # Flowchart generation
├── test_gwo.py                # Test script with smaller parameters
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── MOGWO_Flowchart.png        # Algorithm flowchart
├── MOGWO_Modifications.png    # Modifications from standard GWO
├── UF1_test_result.png        # UF1 test results
└── UF7_test_result.png        # UF7 test results
```

## Algorithm Components

### 1. Wolf Hierarchy
- **Alpha (α)**: Best solutions from the archive
- **Beta (β)**: Second-tier solutions from the archive  
- **Delta (δ)**: Third-tier solutions from the archive
- **Omega (ω)**: Remaining population members

### 2. Key Modifications from Standard GWO

1. **Pareto Dominance**: Replaces single-objective fitness comparison
2. **External Archive**: Maintains non-dominated solutions
3. **Leader Selection**: Selects α, β, δ from archive using random selection
4. **Crowding Distance**: Maintains diversity in the Pareto front
5. **Archive Management**: Dynamically updates and maintains archive size

### 3. Benchmark Problems

#### UF1 Problem
- **Objectives**: 2
- **Variables**: 30 (configurable)
- **Bounds**: x₁ ∈ [0,1], xᵢ ∈ [-1,1] for i = 2,...,n
- **Characteristics**: Convex Pareto front

#### UF7 Problem  
- **Objectives**: 2
- **Variables**: 30 (configurable)
- **Bounds**: x₁ ∈ [0,1], xᵢ ∈ [-1,1] for i = 2,...,n
- **Characteristics**: Complex Pareto front with different scaling

## Installation and Usage

### Prerequisites
```bash
pip install numpy matplotlib
```

### Running the Algorithm

1. **Full Implementation** (500 iterations, 100 wolves):
```bash
python3 gwo_multi_objective.py
```

2. **Quick Test** (50 iterations, 20 wolves):
```bash
python3 test_gwo.py
```

3. **Generate Flowcharts**:
```bash
python3 gwo_flowchart.py
```

### Algorithm Parameters

- `n_wolves`: Population size (default: 100)
- `max_iterations`: Maximum iterations (default: 500)
- `archive_size`: Maximum archive size (default: 100)
- `n_vars`: Problem dimension (default: 30)

## Results

### UF1 Problem Results
- **Pareto solutions found**: 100
- **f1 range**: [0.2841, 1.0022]
- **f2 range**: [0.0383, 0.5399]
- **Mean f1**: 0.6984
- **Mean f2**: 0.2095

### UF7 Problem Results
- **Pareto solutions found**: 100
- **f1 range**: [0.0040, 1.1433]  
- **f2 range**: [0.0208, 1.0039]
- **Mean f1**: 0.3200
- **Mean f2**: 0.6960

## Algorithm Performance

The MOGWO algorithm demonstrates excellent performance on both benchmark problems:

1. **Convergence**: Steadily increases archive size throughout iterations
2. **Diversity**: Maintains well-distributed Pareto fronts
3. **Quality**: Finds high-quality non-dominated solutions
4. **Efficiency**: Balances exploration and exploitation effectively

## Visualization

The implementation provides several types of plots:

1. **Pareto Front Plots**: Scatter plots of objective values
2. **Convergence Plots**: Archive size evolution over iterations
3. **Objective Evolution**: Individual objective function trends
4. **Algorithm Flowcharts**: Visual representation of the algorithm steps

## Implementation Details

### Core Classes

- `Wolf`: Represents individual solutions with position and fitness
- `BenchmarkProblem`: Abstract base class for optimization problems
- `UF1`/`UF7`: Specific benchmark problem implementations
- `MultiObjectiveGWO`: Main algorithm implementation

### Key Methods

- `dominates()`: Pareto dominance comparison
- `update_archive()`: Archive management with dominance filtering
- `select_diverse_solutions()`: Crowding distance-based selection
- `select_leaders()`: Leader selection from archive
- `update_position()`: Wolf position update based on leaders

## Complexity Analysis

- **Time Complexity**: O(max_iterations × n_wolves × (n_objectives × archive_size + dimension))
- **Space Complexity**: O(n_wolves + archive_size) × dimension

## References

1. Mirjalili, S., Mirjalili, S. M., & Lewis, A. (2014). Grey wolf optimizer. Advances in Engineering Software, 69, 46-61.
2. Mirjalili, S., Saremi, S., Mirjalili, S. M., & Coelho, L. D. S. (2016). Multi-objective grey wolf optimizer: A novel algorithm for multi-criterion optimization. Expert Systems with Applications, 47, 106-119.
3. Zhang, Q., Zhou, A., Zhao, S., Suganthan, P. N., Liu, W., & Tiwari, S. (2008). Multiobjective optimization test instances for the CEC 2009 special session and competition.

## Contributing

Feel free to contribute by:
- Adding more benchmark problems
- Implementing additional multi-objective algorithms
- Improving visualization capabilities
- Enhancing documentation

## License

This project is available for educational and research purposes. 
