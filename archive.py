import random
from domination import dominates, select_N


class Archive:
    """External archive for storing non-dominated solutions in multi-objective optimization."""
    
    def __init__(self, max_size):
        """Initialize the archive.
        
        Args:
            max_size: Maximum number of solutions to store in the archive
        """
        self.max_size = max_size
        self.positions = []   # list of solution position vectors
        self.objectives = []  # corresponding list of objective vectors
    
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
        
        # Trim archive if it exceeds max_size using diversity-based selection
        if len(new_objectives) > self.max_size:
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