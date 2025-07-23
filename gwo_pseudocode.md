# Multi-Objective Grey Wolf Optimization (MOGWO) Algorithm Pseudocode

## Main Algorithm

```
Algorithm: Multi-Objective Grey Wolf Optimization (MOGWO)

Input: 
    - Problem: Multi-objective optimization problem
    - n_wolves: Number of wolves in the population
    - max_iterations: Maximum number of iterations
    - archive_size: Maximum size of external archive
    - bounds: Decision variable bounds [lower, upper]

Output:
    - Archive: Set of Pareto optimal solutions

BEGIN
    // Step 1: Initialize Parameters
    Initialize population of n_wolves randomly within bounds
    Initialize empty external archive
    Initialize α, β, δ leaders as null
    Set iteration counter t = 0
    
    // Step 2: Evaluate Initial Population
    FOR each wolf i in population DO
        Evaluate objective functions: fitness[i] = f(position[i])
        Update archive with wolf[i] using Pareto dominance
    END FOR
    
    // Step 3: Main Optimization Loop
    WHILE t < max_iterations DO
        
        // Step 3.1: Select Leaders from Archive
        IF archive is not empty THEN
            α = Random selection from archive
            β = Random selection from archive (different from α)
            δ = Random selection from archive (different from α and β)
        END IF
        
        // Step 3.2: Update Wolf Positions
        FOR each wolf i in population DO
            // Calculate convergence parameter
            a = 2 - 2 * t / max_iterations
            
            // Update position based on α leader
            r1_α = Random vector in [0,1]
            r2_α = Random vector in [0,1]
            A_α = 2 * a * r1_α - a
            C_α = 2 * r2_α
            D_α = |C_α * α.position - wolf[i].position|
            X1 = α.position - A_α * D_α
            
            // Update position based on β leader
            r1_β = Random vector in [0,1]
            r2_β = Random vector in [0,1]
            A_β = 2 * a * r1_β - a
            C_β = 2 * r2_β
            D_β = |C_β * β.position - wolf[i].position|
            X2 = β.position - A_β * D_β
            
            // Update position based on δ leader
            r1_δ = Random vector in [0,1]
            r2_δ = Random vector in [0,1]
            A_δ = 2 * a * r1_δ - a
            C_δ = 2 * r2_δ
            D_δ = |C_δ * δ.position - wolf[i].position|
            X3 = δ.position - A_δ * D_δ
            
            // Calculate new position as average
            new_position[i] = (X1 + X2 + X3) / 3
            
            // Apply boundary constraints
            new_position[i] = Clip(new_position[i], lower_bounds, upper_bounds)
            
            // Evaluate new position
            new_fitness[i] = f(new_position[i])
            
            // Update wolf
            wolf[i].position = new_position[i]
            wolf[i].fitness = new_fitness[i]
            
            // Update archive
            Update_Archive(wolf[i])
        END FOR
        
        // Step 3.3: Increment iteration counter
        t = t + 1
        
    END WHILE
    
    // Step 4: Return Pareto Front
    RETURN archive
END
```

## Supporting Functions

### 1. Pareto Dominance Check

```
Function: Dominates(solution1, solution2)
Input: Two solutions with their objective values
Output: Boolean indicating if solution1 dominates solution2

BEGIN
    better_in_all = True
    better_in_at_least_one = False
    
    FOR each objective i DO
        IF solution1.fitness[i] > solution2.fitness[i] THEN
            better_in_all = False
            BREAK
        END IF
        IF solution1.fitness[i] < solution2.fitness[i] THEN
            better_in_at_least_one = True
        END IF
    END FOR
    
    RETURN (better_in_all AND better_in_at_least_one)
END
```

### 2. Archive Update

```
Function: Update_Archive(new_solution)
Input: New solution to be considered for archive
Output: Updated archive

BEGIN
    // Remove solutions dominated by new solution
    FOR each solution in archive DO
        IF Dominates(new_solution, solution) THEN
            Remove solution from archive
        END IF
    END FOR
    
    // Check if new solution is dominated by any solution in archive
    is_dominated = False
    FOR each solution in archive DO
        IF Dominates(solution, new_solution) THEN
            is_dominated = True
            BREAK
        END IF
    END FOR
    
    // Add new solution if it's not dominated
    IF NOT is_dominated THEN
        Add new_solution to archive
    END IF
    
    // Maintain archive size using crowding distance
    IF size(archive) > archive_size THEN
        archive = Select_Diverse_Solutions(archive, archive_size)
    END IF
END
```

### 3. Crowding Distance Selection

```
Function: Select_Diverse_Solutions(solutions, target_size)
Input: Set of solutions, target size
Output: Subset of solutions with highest diversity

BEGIN
    IF size(solutions) <= target_size THEN
        RETURN solutions
    END IF
    
    n_objectives = number of objectives
    distances = Array of zeros with size(solutions)
    
    // Calculate crowding distance for each objective
    FOR each objective j DO
        // Sort solutions by objective j
        sorted_indices = Sort_Indices_By_Objective(solutions, j)
        
        // Boundary solutions get infinite distance
        distances[sorted_indices[0]] = ∞
        distances[sorted_indices[last]] = ∞
        
        // Calculate normalized distance for intermediate solutions
        obj_min = solutions[sorted_indices[0]].fitness[j]
        obj_max = solutions[sorted_indices[last]].fitness[j]
        
        IF obj_max - obj_min > 0 THEN
            FOR i = 1 to size(sorted_indices) - 2 DO
                idx = sorted_indices[i]
                prev_idx = sorted_indices[i-1]
                next_idx = sorted_indices[i+1]
                
                distances[idx] += (solutions[next_idx].fitness[j] - 
                                 solutions[prev_idx].fitness[j]) / (obj_max - obj_min)
            END FOR
        END IF
    END FOR
    
    // Select solutions with highest crowding distance
    selected_indices = Select_Top_K_Indices(distances, target_size)
    RETURN solutions[selected_indices]
END
```

## Modifications from Standard GWO

### 1. **Fitness Evaluation**
- **Standard GWO**: Single objective value comparison
- **MOGWO**: Multi-objective evaluation with Pareto dominance

### 2. **Leader Selection**
- **Standard GWO**: α, β, δ are the three best solutions based on fitness
- **MOGWO**: α, β, δ are randomly selected from the Pareto optimal archive

### 3. **Solution Comparison**
- **Standard GWO**: Direct fitness comparison (f1 < f2)
- **MOGWO**: Pareto dominance comparison considering all objectives

### 4. **Archive Management**
- **Standard GWO**: No archive, only current population
- **MOGWO**: External archive maintaining non-dominated solutions

### 5. **Diversity Maintenance**
- **Standard GWO**: Natural diversity through population
- **MOGWO**: Crowding distance mechanism to maintain solution diversity

## Algorithm Complexity

- **Time Complexity**: O(max_iterations × n_wolves × (n_objectives × archive_size + dimension))
- **Space Complexity**: O(n_wolves + archive_size) × dimension

## Key Features of the Implementation

1. **Pareto Optimality**: Solutions are compared using Pareto dominance
2. **External Archive**: Maintains the best non-dominated solutions found
3. **Crowding Distance**: Ensures diversity in the Pareto front
4. **Adaptive Leaders**: Leaders are selected from current best solutions
5. **Boundary Handling**: Ensures solutions remain within feasible region

## UF1 Problem Specific Implementation

```
Function: Evaluate_UF1(x)
Input: Decision vector x of dimension n
Output: Objective vector [f1, f2]

BEGIN
    x1 = x[0]
    J1_sum = 0, J2_sum = 0
    J1_count = 0, J2_count = 0
    
    FOR j = 2 to n DO
        y_j = x[j-1] - sin(6π × x1 + j × π/n)
        
        IF j is odd THEN
            J1_sum += y_j²
            J1_count += 1
        ELSE
            J2_sum += y_j²
            J2_count += 1
        END IF
    END FOR
    
    f1 = x1 + (2/J1_count) × J1_sum
    f2 = 1 - √x1 + (2/J2_count) × J2_sum
    
    RETURN [f1, f2]
END
```

## UF7 Problem Specific Implementation

```
Function: Evaluate_UF7(x)
Input: Decision vector x of dimension n
Output: Objective vector [f1, f2]

BEGIN
    x1 = x[0]
    sum_odd = 0, sum_even = 0
    count_odd = 0, count_even = 0
    
    FOR j = 2 to n DO
        y_j = x[j-1] - sin(6π × x1 + j × π/n)
        
        IF j is odd THEN
            sum_odd += y_j²
            count_odd += 1
        ELSE
            sum_even += y_j²
            count_even += 1
        END IF
    END FOR
    
    f1 = x1^0.2 + (2/count_odd) × sum_odd
    f2 = 1 - x1^0.2 + (2/count_even) × sum_even
    
    RETURN [f1, f2]
END
```