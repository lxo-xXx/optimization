import math


def UF1(sol):
    """UF1 benchmark function from CEC 2009 UF suite.
    
    This is a two-objective minimization problem with a concave Pareto front.
    The true Pareto front is defined by f2 = 1 - sqrt(f1).
    
    Args:
        sol: Decision vector of length 30, where x1 ∈ [0,1] and x2...x30 ∈ [-1,1]
        
    Returns:
        List of two objective values [f1, f2] to minimize
    """
    x1 = sol[0]
    n = len(sol)
    
    # Calculate sums for odd and even indexed variables
    sum1 = 0.0  # for odd j (J1)
    sum2 = 0.0  # for even j (J2)
    
    for j in range(2, n + 1):  # j from 2 to n (1-indexed)
        # Python index j-1 corresponds to x_j in mathematical notation
        term = sol[j - 1] - math.sin(6 * math.pi * x1 + j * math.pi / n)
        term = term ** 2
        
        if j % 2 == 1:  # odd index j
            sum1 += term
        else:           # even index j
            sum2 += term
    
    # Count elements in J1 and J2
    J1_count = len([j for j in range(3, n + 1) if j % 2 == 1])  # odd j >= 3
    J2_count = len([j for j in range(2, n + 1) if j % 2 == 0])  # even j >= 2
    
    # Calculate objectives
    f1 = x1 + 2 * sum1 / J1_count if J1_count > 0 else x1
    f2 = 1 - math.sqrt(x1) + 2 * sum2 / J2_count if J2_count > 0 else 1 - math.sqrt(x1)
    
    return [f1, f2]


def UF7(sol):
    """UF7 benchmark function from CEC 2009 UF suite.
    
    This is a two-objective minimization problem with a linear Pareto front.
    The true Pareto front is defined by f2 = 1 - f1.
    
    Args:
        sol: Decision vector of length 30, where x1 ∈ [0,1] and x2...x30 ∈ [-1,1]
        
    Returns:
        List of two objective values [f1, f2] to minimize
    """
    x1 = sol[0]
    n = len(sol)
    
    # Calculate sums for odd and even indexed variables
    sum1 = 0.0  # for odd j (J1)
    sum2 = 0.0  # for even j (J2)
    
    for j in range(2, n + 1):  # j from 2 to n (1-indexed)
        # Calculate yj = xj - sin(6πx1 + jπ/n)
        yj = sol[j - 1] - math.sin(6 * math.pi * x1 + j * math.pi / n)
        term = yj ** 2
        
        if j % 2 == 1:  # odd index j
            sum1 += term
        else:           # even index j
            sum2 += term
    
    # Count elements in J1 and J2
    J1_count = len([j for j in range(3, n + 1) if j % 2 == 1])  # odd j >= 3
    J2_count = len([j for j in range(2, n + 1) if j % 2 == 0])  # even j >= 2
    
    # Calculate objectives
    f1 = math.sqrt(5) * x1 + 2 * sum1 / J1_count if J1_count > 0 else math.sqrt(5) * x1
    f2 = 1 - math.sqrt(5) * x1 + 2 * sum2 / J2_count if J2_count > 0 else 1 - math.sqrt(5) * x1
    
    return [f1, f2]


def get_true_pareto_front(problem, n_points=100):
    """Generate points on the true Pareto front for visualization.
    
    Args:
        problem: String identifier ('UF1' or 'UF7')
        n_points: Number of points to generate
        
    Returns:
        List of [f1, f2] pairs representing the true Pareto front
    """
    if problem == 'UF1':
        # True Pareto front: f2 = 1 - sqrt(f1), where f1 ∈ [0, 1]
        f1_values = [i / (n_points - 1) for i in range(n_points)]
        return [[f1, 1 - math.sqrt(f1)] for f1 in f1_values]
    
    elif problem == 'UF7':
        # True Pareto front: f2 = 1 - f1, where f1 ∈ [0, 1]
        # Note: For UF7, x1 ranges from 0 to 1/sqrt(5) ≈ 0.447
        # This gives f1 from 0 to 1 and f2 from 0 to 1
        f1_values = [i / (n_points - 1) for i in range(n_points)]
        return [[f1, 1 - f1] for f1 in f1_values]
    
    else:
        raise ValueError(f"Unknown problem: {problem}")


def get_bounds(problem, dim=30):
    """Get the bounds for decision variables.
    
    Args:
        problem: String identifier ('UF1' or 'UF7')
        dim: Dimension of decision space (default 30)
        
    Returns:
        Tuple of (lower_bounds, upper_bounds)
    """
    if problem in ['UF1', 'UF7']:
        # x1 ∈ [0, 1], x2...x30 ∈ [-1, 1]
        lower_bounds = [0.0] + [-1.0] * (dim - 1)
        upper_bounds = [1.0] + [1.0] * (dim - 1)
        return lower_bounds, upper_bounds
    else:
        raise ValueError(f"Unknown problem: {problem}")