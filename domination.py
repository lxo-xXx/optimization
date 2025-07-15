def dominates(obj_a, obj_b):
    """Return True if solution with objectives obj_a dominates solution with obj_b.
    
    Args:
        obj_a: List of objective values for solution A
        obj_b: List of objective values for solution B
        
    Returns:
        bool: True if obj_a dominates obj_b (assuming minimization)
    """
    better_or_equal = False
    for a, b in zip(obj_a, obj_b):
        if a > b:    # a is worse in this objective (minimization)
            return False
        if a < b:    # a is better in this objective
            better_or_equal = True
    return better_or_equal


def non_dominated_sort(pop_objs):
    """Group indices of pop_objs into Pareto fronts using NSGA-II fast sort.
    
    Args:
        pop_objs: List of objective vectors for population
        
    Returns:
        List of lists: Each inner list contains indices of solutions in that front
    """
    n = len(pop_objs)
    S = [set() for _ in range(n)]        # S[i]: set of solutions dominated by i
    dominated_count = [0] * n            # number of solutions that dominate i
    fronts = [[]]                        # fronts[0] will be the first Pareto front
    
    # Build domination structure
    for p in range(n):
        for q in range(n):
            if p == q:
                continue
            if dominates(pop_objs[p], pop_objs[q]):
                S[p].add(q)
            elif dominates(pop_objs[q], pop_objs[p]):
                dominated_count[p] += 1
        
        # If not dominated by anyone, belongs to first front
        if dominated_count[p] == 0:
            fronts[0].append(p)
    
    # Iteratively find subsequent fronts
    i = 0
    while i < len(fronts) and fronts[i]:
        next_front = []
        for p in fronts[i]:
            for q in S[p]:
                dominated_count[q] -= 1
                if dominated_count[q] == 0:
                    next_front.append(q)
        i += 1
        fronts.append(next_front)
    
    # Remove empty fronts
    return [f for f in fronts if f]


def crowding_distance(pop_objs, front):
    """Calculate crowding distances for solutions in the given front.
    
    Args:
        pop_objs: List of objective vectors for population
        front: List of indices of solutions in this front
        
    Returns:
        dict: Mapping from solution index to crowding distance
    """
    if not front:
        return {}
    
    distances = {i: 0.0 for i in front}
    m = len(pop_objs[0])  # number of objectives
    
    for j in range(m):
        # Sort by j-th objective value
        front_sorted = sorted(front, key=lambda i: pop_objs[i][j])
        
        # Get min and max values for this objective
        min_val = pop_objs[front_sorted[0]][j]
        max_val = pop_objs[front_sorted[-1]][j]
        
        # Boundary solutions get infinite distance
        distances[front_sorted[0]] = float('inf')
        distances[front_sorted[-1]] = float('inf')
        
        # Skip if all solutions have equal value for this objective
        if max_val == min_val:
            continue
        
        # Assign crowding distance for interior points
        for k in range(1, len(front_sorted) - 1):
            prev_i = front_sorted[k - 1]
            next_i = front_sorted[k + 1]
            distance_contrib = (pop_objs[next_i][j] - pop_objs[prev_i][j]) / (max_val - min_val)
            distances[front_sorted[k]] += distance_contrib
    
    return distances


def select_N(pop_objs, N):
    """Select N solutions from pop_objs using non-domination and crowding distance.
    
    Args:
        pop_objs: List of objective vectors for population
        N: Number of solutions to select
        
    Returns:
        List of indices of selected solutions
    """
    if len(pop_objs) <= N:
        return list(range(len(pop_objs)))
    
    fronts = non_dominated_sort(pop_objs)
    selected_indices = []
    
    for front in fronts:
        if not front:
            break
        
        if len(selected_indices) + len(front) <= N:
            # Take entire front
            selected_indices.extend(front)
        else:
            # Partially take from this front based on crowding distance
            remaining = N - len(selected_indices)
            cd = crowding_distance(pop_objs, front)
            
            # Sort by crowding distance (descending - prefer more isolated solutions)
            front_sorted = sorted(front, key=lambda i: cd[i], reverse=True)
            selected_indices.extend(front_sorted[:remaining])
            break
    
    return selected_indices