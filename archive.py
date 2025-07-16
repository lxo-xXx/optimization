import random
import math
import numpy as np
from domination import dominates, select_N, crowding_distance


class Archive:
    """Enhanced external archive for storing non-dominated solutions with advanced diversity preservation."""
    
    def __init__(self, max_size, use_clustering=True, sigma_share=0.1):
        """Initialize the archive.
        
        Args:
            max_size: Maximum number of solutions to store in the archive
            use_clustering: Enable clustering-based pruning for better diversity
            sigma_share: Sigma parameter for sharing function (diversity control)
        """
        self.max_size = max_size
        self.use_clustering = use_clustering
        self.sigma_share = sigma_share
        self.positions = []   # list of solution position vectors
        self.objectives = []  # corresponding list of objective vectors
    
    def euclidean_distance(self, obj1, obj2):
        """Calculate Euclidean distance between two objective vectors.
        
        Args:
            obj1: First objective vector
            obj2: Second objective vector
            
        Returns:
            float: Euclidean distance
        """
        return math.sqrt(sum((a - b)**2 for a, b in zip(obj1, obj2)))
    
    def sigma_sharing_pruning(self, objectives_list, positions_list, target_size):
        """Apply sigma-sharing based pruning to maintain diversity.
        
        Args:
            objectives_list: List of objective vectors
            positions_list: List of position vectors
            target_size: Target number of solutions to keep
            
        Returns:
            tuple: (selected_positions, selected_objectives)
        """
        if len(objectives_list) <= target_size:
            return positions_list, objectives_list
        
        # Calculate sharing values for each solution
        sharing_values = []
        for i, obj_i in enumerate(objectives_list):
            sharing = 0.0
            for j, obj_j in enumerate(objectives_list):
                if i != j:
                    dist = self.euclidean_distance(obj_i, obj_j)
                    if dist < self.sigma_share:
                        sharing += 1.0 - (dist / self.sigma_share)
            sharing_values.append(sharing)
        
        # Select solutions with lowest sharing values (most isolated)
        indexed_sharing = [(i, sharing) for i, sharing in enumerate(sharing_values)]
        indexed_sharing.sort(key=lambda x: x[1])  # Sort by sharing value (ascending)
        
        selected_indices = [idx for idx, _ in indexed_sharing[:target_size]]
        selected_positions = [positions_list[i] for i in selected_indices]
        selected_objectives = [objectives_list[i] for i in selected_indices]
        
        return selected_positions, selected_objectives
    
    def clustering_based_pruning(self, objectives_list, positions_list, target_size):
        """Apply clustering-based pruning to preserve edge solutions and diversity.
        
        Args:
            objectives_list: List of objective vectors
            positions_list: List of position vectors
            target_size: Target number of solutions to keep
            
        Returns:
            tuple: (selected_positions, selected_objectives)
        """
        if len(objectives_list) <= target_size:
            return positions_list, objectives_list
        
        # Calculate crowding distances
        indices = list(range(len(objectives_list)))
        cd = crowding_distance(objectives_list, indices)
        
        # Always preserve boundary solutions (infinite crowding distance)
        boundary_indices = [i for i in indices if cd[i] == float('inf')]
        remaining_indices = [i for i in indices if cd[i] != float('inf')]
        
        selected_indices = boundary_indices[:]
        
        # If we need more solutions, select based on crowding distance
        if len(selected_indices) < target_size:
            remaining_needed = target_size - len(selected_indices)
            
            # Sort remaining by crowding distance (descending)
            remaining_sorted = sorted(remaining_indices, key=lambda i: cd[i], reverse=True)
            selected_indices.extend(remaining_sorted[:remaining_needed])
        
        # If we have too many boundary solutions, keep the most diverse ones
        elif len(selected_indices) > target_size:
            # Use sigma-sharing among boundary solutions
            boundary_objs = [objectives_list[i] for i in boundary_indices]
            boundary_pos = [positions_list[i] for i in boundary_indices]
            selected_pos, selected_objs = self.sigma_sharing_pruning(
                boundary_objs, boundary_pos, target_size)
            return selected_pos, selected_objs
        
        selected_positions = [positions_list[i] for i in selected_indices]
        selected_objectives = [objectives_list[i] for i in selected_indices]
        
        return selected_positions, selected_objectives
    
    def add(self, pos, obj):
        """Add a solution to the archive if it's not dominated.
        
        Args:
            pos: Position vector of the solution
            obj: Objective vector of the solution
            
        Returns:
            bool: True if solution was added, False if it was dominated
        """
        # Check if dominated by any existing archive member
        for arch_obj in self.objectives:
            if dominates(arch_obj, obj):
                return False  # pos is dominated, skip
        
        # Remove any archive members that this solution dominates
        new_positions = []
        new_objectives = []
        for p, o in zip(self.positions, self.objectives):
            if not dominates(obj, o):
                new_positions.append(p)
                new_objectives.append(o)
        
        # Add the new solution
        new_positions.append(pos)
        new_objectives.append(obj)
        
        # Trim archive if it exceeds max_size using enhanced diversity-based selection
        if len(new_objectives) > self.max_size:
            if self.use_clustering:
                self.positions, self.objectives = self.clustering_based_pruning(
                    new_objectives, new_positions, self.max_size)
            else:
                # Fallback to original crowding distance-based selection
                sel_idx = select_N(new_objectives, self.max_size)
                self.positions = [new_positions[i] for i in sel_idx]
                self.objectives = [new_objectives[i] for i in sel_idx]
        else:
            self.positions = new_positions
            self.objectives = new_objectives
        
        return True
    
    def add_all(self, positions, objectives_list):
        """Add multiple solutions to the archive.
        
        Args:
            positions: List of position vectors
            objectives_list: List of corresponding objective vectors
        """
        for pos, obj in zip(positions, objectives_list):
            self.add(pos, obj)
    
    def get_leaders(self, k):
        """Get k leader solutions from the archive for guiding wolves.
        
        Args:
            k: Number of leaders to select
            
        Returns:
            List of k position vectors selected from the archive
        """
        if len(self.positions) == 0:
            return []  # empty archive (should not happen if called after initialization)
        
        if len(self.positions) >= k:
            # Sample without replacement
            indices = random.sample(range(len(self.positions)), k)
        else:
            # Sample with replacement if archive has fewer than k solutions
            indices = [random.randrange(len(self.positions)) for _ in range(k)]
        
        return [self.positions[i] for i in indices]
    
    def get_extreme_solutions(self):
        """Get extreme solutions for each objective (useful for reference point adaptation).
        
        Returns:
            dict: Dictionary with 'min' and 'max' keys containing extreme solutions
        """
        if not self.objectives:
            return {'min': [], 'max': []}
        
        n_objectives = len(self.objectives[0])
        min_solutions = []
        max_solutions = []
        
        for i in range(n_objectives):
            # Find minimum and maximum for each objective
            min_idx = min(range(len(self.objectives)), key=lambda j: self.objectives[j][i])
            max_idx = max(range(len(self.objectives)), key=lambda j: self.objectives[j][i])
            
            min_solutions.append({
                'position': self.positions[min_idx],
                'objective': self.objectives[min_idx],
                'objective_idx': i
            })
            max_solutions.append({
                'position': self.positions[max_idx],
                'objective': self.objectives[max_idx],
                'objective_idx': i
            })
        
        return {'min': min_solutions, 'max': max_solutions}
    
    def size(self):
        """Return the current number of solutions in the archive."""
        return len(self.positions)
    
    def is_empty(self):
        """Check if the archive is empty."""
        return len(self.positions) == 0
    
    def get_all_solutions(self):
        """Get all solutions in the archive.
        
        Returns:
            tuple: (positions, objectives) - all positions and objectives in archive
        """
        return self.positions.copy(), self.objectives.copy()
    
    def get_diversity_metrics(self):
        """Calculate diversity metrics for the current archive.
        
        Returns:
            dict: Dictionary containing diversity metrics
        """
        if len(self.objectives) < 2:
            return {'avg_distance': 0.0, 'min_distance': 0.0, 'max_distance': 0.0}
        
        distances = []
        for i in range(len(self.objectives)):
            for j in range(i + 1, len(self.objectives)):
                dist = self.euclidean_distance(self.objectives[i], self.objectives[j])
                distances.append(dist)
        
        return {
            'avg_distance': sum(distances) / len(distances),
            'min_distance': min(distances),
            'max_distance': max(distances),
            'num_solutions': len(self.objectives)
        }