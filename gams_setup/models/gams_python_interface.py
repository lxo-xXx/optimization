"""
GAMS-Python Integration Interface
Combines GAMS optimization models with Python metaheuristics
"""

import os
import sys
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import subprocess
import tempfile
import json

try:
    from gams import GamsWorkspace, GamsDatabase, GamsSet, GamsParameter
    GAMS_AVAILABLE = True
except ImportError:
    GAMS_AVAILABLE = False
    print("Warning: GAMS Python API not available. Install with: pip install gamsapi")

class GAMSPythonInterface:
    """
    Interface for integrating GAMS optimization models with Python
    Supports hybrid optimization approaches combining exact and metaheuristic methods
    """
    
    def __init__(self, gams_dir: Optional[str] = None, working_dir: Optional[str] = None):
        """
        Initialize GAMS-Python interface
        
        Args:
            gams_dir: Path to GAMS installation directory
            working_dir: Working directory for GAMS files
        """
        self.gams_dir = gams_dir or os.environ.get('GAMS_PATH', '')
        self.working_dir = working_dir or tempfile.mkdtemp()
        
        if GAMS_AVAILABLE:
            try:
                self.workspace = GamsWorkspace(
                    system_directory=self.gams_dir,
                    working_directory=self.working_dir
                )
            except Exception as e:
                print(f"Warning: Could not initialize GAMS workspace: {e}")
                self.workspace = None
        else:
            self.workspace = None
    
    def run_gams_model(self, model_file: str, parameters: Optional[Dict] = None) -> Dict:
        """
        Run a GAMS model with optional parameter updates
        
        Args:
            model_file: Path to .gms file
            parameters: Dictionary of parameters to update
            
        Returns:
            Dictionary containing results and statistics
        """
        if not GAMS_AVAILABLE or not self.workspace:
            return self._run_gams_subprocess(model_file, parameters)
        
        try:
            # Load model
            job = self.workspace.add_job_from_file(model_file)
            
            # Update parameters if provided
            if parameters:
                db = self.workspace.add_database()
                for param_name, param_value in parameters.items():
                    if isinstance(param_value, dict):
                        # Handle multi-dimensional parameters
                        param = db.add_parameter(param_name, len(param_value))
                        for key, value in param_value.items():
                            param.add_record(key).value = value
                    else:
                        # Handle scalar parameters
                        param = db.add_parameter(param_name, 0)
                        param.add_record().value = param_value
                
                job.run(databases=db)
            else:
                job.run()
            
            # Extract results
            results = self._extract_results(job)
            return results
            
        except Exception as e:
            print(f"Error running GAMS model: {e}")
            return {"error": str(e)}
    
    def _run_gams_subprocess(self, model_file: str, parameters: Optional[Dict] = None) -> Dict:
        """
        Fallback method to run GAMS via subprocess
        """
        try:
            # Prepare command
            cmd = ["gams", model_file]
            
            # Add parameter definitions if provided
            if parameters:
                param_file = os.path.join(self.working_dir, "params.gms")
                with open(param_file, 'w') as f:
                    for param_name, param_value in parameters.items():
                        if isinstance(param_value, dict):
                            f.write(f"Parameter {param_name} /\n")
                            for key, value in param_value.items():
                                f.write(f"  {key} {value}\n")
                            f.write("/;\n")
                        else:
                            f.write(f"Scalar {param_name} /{param_value}/;\n")
                
                cmd.extend(["--include", param_file])
            
            # Run GAMS
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.working_dir)
            
            return {
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _extract_results(self, job) -> Dict:
        """Extract results from GAMS job"""
        results = {
            "variables": {},
            "parameters": {},
            "equations": {},
            "model_status": None,
            "solve_status": None,
            "objective_value": None
        }
        
        try:
            # Extract variable values
            for variable in job.out_db:
                if variable.type == variable.Type.Variable:
                    var_data = {}
                    for record in variable:
                        key = tuple(record.keys) if record.keys else "scalar"
                        var_data[key] = {
                            "level": record.level,
                            "marginal": record.marginal,
                            "lower": record.lower,
                            "upper": record.upper
                        }
                    results["variables"][variable.name] = var_data
                
                elif variable.type == variable.Type.Parameter:
                    param_data = {}
                    for record in variable:
                        key = tuple(record.keys) if record.keys else "scalar"
                        param_data[key] = record.value
                    results["parameters"][variable.name] = param_data
            
            # Extract model statistics if available
            # This would need to be customized based on your specific GAMS model structure
            
        except Exception as e:
            results["extraction_error"] = str(e)
        
        return results
    
    def create_hybrid_optimizer(self, gams_model: str, metaheuristic_class):
        """
        Create a hybrid optimizer combining GAMS exact methods with metaheuristics
        
        Args:
            gams_model: Path to GAMS model file
            metaheuristic_class: Python metaheuristic class (e.g., your GWO)
            
        Returns:
            HybridOptimizer instance
        """
        return HybridOptimizer(self, gams_model, metaheuristic_class)
    
    def benchmark_solvers(self, model_file: str, solvers: List[str]) -> Dict:
        """
        Benchmark different GAMS solvers on the same model
        
        Args:
            model_file: Path to .gms file
            solvers: List of solver names to test
            
        Returns:
            Dictionary with solver performance comparison
        """
        results = {}
        
        for solver in solvers:
            print(f"Testing solver: {solver}")
            
            # Modify model to use specific solver
            temp_model = self._modify_model_solver(model_file, solver)
            
            # Run model
            result = self.run_gams_model(temp_model)
            results[solver] = result
            
            # Cleanup
            if os.path.exists(temp_model):
                os.remove(temp_model)
        
        return results
    
    def _modify_model_solver(self, model_file: str, solver: str) -> str:
        """Create temporary model file with specified solver"""
        with open(model_file, 'r') as f:
            content = f.read()
        
        # Simple solver substitution (you may need more sophisticated parsing)
        content = content.replace("using lp", f"using lp solver {solver}")
        content = content.replace("using nlp", f"using nlp solver {solver}")
        content = content.replace("using mip", f"using mip solver {solver}")
        
        temp_file = os.path.join(self.working_dir, f"temp_{solver}_{os.path.basename(model_file)}")
        with open(temp_file, 'w') as f:
            f.write(content)
        
        return temp_file


class HybridOptimizer:
    """
    Hybrid optimizer combining GAMS exact methods with Python metaheuristics
    """
    
    def __init__(self, gams_interface: GAMSPythonInterface, gams_model: str, metaheuristic_class):
        self.gams_interface = gams_interface
        self.gams_model = gams_model
        self.metaheuristic_class = metaheuristic_class
        self.results_history = []
    
    def optimize(self, initial_solution: Optional[np.ndarray] = None, 
                max_iterations: int = 100, **kwargs) -> Dict:
        """
        Run hybrid optimization combining exact and metaheuristic methods
        
        Args:
            initial_solution: Starting solution for metaheuristic
            max_iterations: Maximum iterations for metaheuristic
            **kwargs: Additional arguments for metaheuristic
            
        Returns:
            Dictionary with optimization results
        """
        # Stage 1: Use metaheuristic to explore solution space
        print("Stage 1: Metaheuristic exploration...")
        meta_optimizer = self.metaheuristic_class(**kwargs)
        
        if hasattr(meta_optimizer, 'run'):
            meta_results = meta_optimizer.run()
        else:
            # Fallback for different metaheuristic interfaces
            meta_results = meta_optimizer.optimize()
        
        # Stage 2: Use GAMS for local refinement
        print("Stage 2: GAMS refinement...")
        best_meta_solution = self._extract_best_solution(meta_results)
        gams_results = self._refine_with_gams(best_meta_solution)
        
        # Stage 3: Combine results
        hybrid_results = {
            "metaheuristic_results": meta_results,
            "gams_results": gams_results,
            "best_solution": self._select_best_solution(meta_results, gams_results),
            "optimization_stages": ["metaheuristic", "gams_refinement"]
        }
        
        self.results_history.append(hybrid_results)
        return hybrid_results
    
    def _extract_best_solution(self, meta_results) -> np.ndarray:
        """Extract best solution from metaheuristic results"""
        # This needs to be adapted based on your metaheuristic's output format
        if isinstance(meta_results, tuple) and len(meta_results) >= 2:
            return meta_results[0]  # Assuming first element is positions
        elif isinstance(meta_results, dict) and 'best_solution' in meta_results:
            return meta_results['best_solution']
        else:
            # Fallback - return random solution
            return np.random.randn(10)
    
    def _refine_with_gams(self, solution: np.ndarray) -> Dict:
        """Use GAMS to refine the metaheuristic solution"""
        # Convert solution to GAMS parameters
        parameters = {
            "initial_x": {f"i{i}": float(val) for i, val in enumerate(solution)}
        }
        
        # Run GAMS model
        return self.gams_interface.run_gams_model(self.gams_model, parameters)
    
    def _select_best_solution(self, meta_results, gams_results) -> Dict:
        """Select the best solution from both optimization stages"""
        # This is a simplified selection - you'd implement proper comparison logic
        return {
            "source": "hybrid",
            "meta_objective": self._get_objective_value(meta_results),
            "gams_objective": self._get_objective_value(gams_results),
            "selected": "gams" if gams_results.get("success", False) else "metaheuristic"
        }
    
    def _get_objective_value(self, results) -> Optional[float]:
        """Extract objective value from results"""
        if isinstance(results, dict):
            return results.get("objective_value")
        return None


# Example usage and integration templates
def create_gwo_gams_hybrid():
    """
    Example: Create hybrid GWO-GAMS optimizer
    """
    # Import your existing GWO
    try:
        from gwo import GWO  # Your existing implementation
        
        # Initialize GAMS interface
        gams_interface = GAMSPythonInterface()
        
        # Create hybrid optimizer
        hybrid = gams_interface.create_hybrid_optimizer(
            gams_model="models/optimization_problem.gms",
            metaheuristic_class=GWO
        )
        
        return hybrid
        
    except ImportError:
        print("GWO class not found. Please ensure it's in the Python path.")
        return None


def example_optimization_workflow():
    """
    Example workflow for hybrid optimization
    """
    # Setup
    gams_interface = GAMSPythonInterface()
    
    # Test GAMS installation
    test_results = gams_interface.run_gams_model("models/test_model.gms")
    print("GAMS Test Results:", test_results)
    
    # Create and run hybrid optimizer if GWO is available
    hybrid = create_gwo_gams_hybrid()
    if hybrid:
        results = hybrid.optimize(max_iterations=50)
        print("Hybrid Optimization Results:", results)
    
    return test_results


if __name__ == "__main__":
    # Run example workflow
    example_optimization_workflow()