import numpy as np
import matplotlib.pyplot as plt
from advanced_gwo import AdvancedGWO
from test_functions import get_test_function
import time
import json

class BasicGWO:
    """
    Basic GWO implementation for comparison
    """
    def __init__(self, func, bounds, pop_size=50, max_gen=100, verbose=False):
        self.func = func
        self.bounds = np.array(bounds)
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.verbose = verbose
        
        self.dim = len(bounds)
        self.lb = self.bounds[:, 0]
        self.ub = self.bounds[:, 1]
        
        self.archive = []
        self.hypervolume_history = []
        self.reference_point = np.array([3.0, 3.0])
        
    def initialize_population(self):
        return np.random.uniform(self.lb, self.ub, (self.pop_size, self.dim))
    
    def calculate_hypervolume(self, front):
        """Simple 2D hypervolume calculation"""
        if len(front) == 0:
            return 0.0
        
        if front.shape[1] == 2:
            sorted_front = front[np.argsort(front[:, 0])]
            hv = 0.0
            for i in range(len(sorted_front)):
                if i == 0:
                    width = self.reference_point[0] - sorted_front[i, 0]
                else:
                    width = sorted_front[i-1, 0] - sorted_front[i, 0]
                height = self.reference_point[1] - sorted_front[i, 1]
                hv += width * height
            return max(0, hv)
        return 0.0
    
    def fast_non_dominated_sort(self, objectives):
        """Fast non-dominated sorting"""
        objectives = np.array(objectives)
        n = len(objectives)
        
        if n == 0:
            return []
            
        is_dominated = np.zeros(n, dtype=bool)
        
        for i in range(n):
            for j in range(i + 1, n):
                if np.all(objectives[i] <= objectives[j]) and np.any(objectives[i] < objectives[j]):
                    is_dominated[j] = True
                elif np.all(objectives[j] <= objectives[i]) and np.any(objectives[j] < objectives[i]):
                    is_dominated[i] = True
                    
        return np.where(~is_dominated)[0]
    
    def optimize(self):
        """Basic GWO optimization"""
        population = self.initialize_population()
        
        for generation in range(self.max_gen):
            # Evaluate population
            objectives = np.array([self.func(ind) for ind in population])
            
            # Update archive (simple non-dominated sorting)
            non_dom_indices = self.fast_non_dominated_sort(objectives)
            if len(non_dom_indices) > 0:
                archive_objectives = objectives[non_dom_indices]
                self.archive = [(population[i], objectives[i]) for i in non_dom_indices]
                
                # Calculate hypervolume
                hv = self.calculate_hypervolume(archive_objectives)
                self.hypervolume_history.append(hv)
                
                # Random leader selection
                if len(self.archive) >= 3:
                    alpha_idx, beta_idx, delta_idx = np.random.choice(len(self.archive), 3, replace=False)
                    alpha_pos = self.archive[alpha_idx][0]
                    beta_pos = self.archive[beta_idx][0]
                    delta_pos = self.archive[delta_idx][0]
                else:
                    alpha_pos = population[0]
                    beta_pos = population[1]
                    delta_pos = population[2]
            else:
                alpha_pos = population[0]
                beta_pos = population[1]
                delta_pos = population[2]
                self.hypervolume_history.append(0.0)
            
            # Update coefficient a
            a = 2 * (1 - generation / self.max_gen)
            
            # Basic GWO position update
            for i in range(self.pop_size):
                A1 = 2 * a * np.random.random(self.dim) - a
                C1 = 2 * np.random.random(self.dim)
                D_alpha = np.abs(C1 * alpha_pos - population[i])
                X1 = alpha_pos - A1 * D_alpha
                
                A2 = 2 * a * np.random.random(self.dim) - a
                C2 = 2 * np.random.random(self.dim)
                D_beta = np.abs(C2 * beta_pos - population[i])
                X2 = beta_pos - A2 * D_beta
                
                A3 = 2 * a * np.random.random(self.dim) - a
                C3 = 2 * np.random.random(self.dim)
                D_delta = np.abs(C3 * delta_pos - population[i])
                X3 = delta_pos - A3 * D_delta
                
                population[i] = (X1 + X2 + X3) / 3
                population[i] = np.clip(population[i], self.lb, self.ub)
        
        if self.archive:
            return np.array([sol for sol, _ in self.archive]), np.array([obj for _, obj in self.archive])
        else:
            return np.array([]), np.array([])

def run_benchmark(test_function_name, dim=30, runs=3, max_gen=100, pop_size=50):
    """
    Run benchmark comparison between Basic GWO and Advanced GWO
    """
    print(f"\n{'='*60}")
    print(f"BENCHMARKING: {test_function_name}")
    print(f"{'='*60}")
    
    # Get test function
    test_func = get_test_function(test_function_name, dim=dim)
    bounds = test_func.bounds
    
    results = {
        'basic_gwo': {'hypervolumes': [], 'times': [], 'archive_sizes': []},
        'advanced_gwo': {'hypervolumes': [], 'times': [], 'archive_sizes': []}
    }
    
    for run in range(runs):
        print(f"\nRun {run + 1}/{runs}")
        
        # Basic GWO
        print("  Running Basic GWO...")
        start_time = time.time()
        basic_gwo = BasicGWO(test_func, bounds, pop_size=pop_size, max_gen=max_gen, verbose=False)
        basic_solutions, basic_objectives = basic_gwo.optimize()
        basic_time = time.time() - start_time
        
        basic_hv = basic_gwo.hypervolume_history[-1] if basic_gwo.hypervolume_history else 0.0
        results['basic_gwo']['hypervolumes'].append(basic_hv)
        results['basic_gwo']['times'].append(basic_time)
        results['basic_gwo']['archive_sizes'].append(len(basic_solutions))
        
        # Advanced GWO
        print("  Running Advanced GWO...")
        start_time = time.time()
        advanced_gwo = AdvancedGWO(
            test_func, bounds, pop_size=pop_size, max_gen=max_gen, 
            archive_size=100, F=0.5, CR=0.7, n_jobs=2, verbose=False
        )
        advanced_solutions, advanced_objectives = advanced_gwo.optimize()
        advanced_time = time.time() - start_time
        
        advanced_hv = advanced_gwo.hypervolume_history[-1] if advanced_gwo.hypervolume_history else 0.0
        results['advanced_gwo']['hypervolumes'].append(advanced_hv)
        results['advanced_gwo']['times'].append(advanced_time)
        results['advanced_gwo']['archive_sizes'].append(len(advanced_solutions))
        
        print(f"    Basic GWO:    HV={basic_hv:.4f}, Time={basic_time:.2f}s, Archive={len(basic_solutions)}")
        print(f"    Advanced GWO: HV={advanced_hv:.4f}, Time={advanced_time:.2f}s, Archive={len(advanced_solutions)}")
    
    # Calculate statistics
    print(f"\n{'='*60}")
    print(f"RESULTS SUMMARY ({runs} runs)")
    print(f"{'='*60}")
    
    for method, data in results.items():
        method_name = method.replace('_', ' ').title()
        hv_mean = np.mean(data['hypervolumes'])
        hv_std = np.std(data['hypervolumes'])
        time_mean = np.mean(data['times'])
        size_mean = np.mean(data['archive_sizes'])
        
        print(f"{method_name:15s}: HV={hv_mean:.4f}±{hv_std:.4f}, Time={time_mean:.2f}s, Size={size_mean:.1f}")
    
    # Improvement calculation
    basic_hv_mean = np.mean(results['basic_gwo']['hypervolumes'])
    advanced_hv_mean = np.mean(results['advanced_gwo']['hypervolumes'])
    
    if basic_hv_mean > 0:
        improvement = ((advanced_hv_mean - basic_hv_mean) / basic_hv_mean) * 100
        print(f"\nHypervolume Improvement: {improvement:.2f}%")
    else:
        print(f"\nHypervolume Improvement: N/A (Basic GWO failed)")
    
    return results, basic_gwo, advanced_gwo

def plot_comparison(results, basic_gwo, advanced_gwo, test_function_name):
    """
    Plot comparison results
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot Pareto fronts
    if len(basic_gwo.archive) > 0:
        basic_objectives = np.array([obj for _, obj in basic_gwo.archive])
        ax1.scatter(basic_objectives[:, 0], basic_objectives[:, 1], 
                   c='blue', s=30, alpha=0.7, label='Basic GWO')
    
    if len(advanced_gwo.archive) > 0:
        advanced_objectives = np.array([obj for _, obj in advanced_gwo.archive])
        ax1.scatter(advanced_objectives[:, 0], advanced_objectives[:, 1], 
                   c='red', s=30, alpha=0.7, label='Advanced GWO')
    
    ax1.set_xlabel('Objective 1')
    ax1.set_ylabel('Objective 2')
    ax1.set_title(f'{test_function_name} - Pareto Front Comparison')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot convergence histories
    ax2.plot(basic_gwo.hypervolume_history, 'b-', linewidth=2, label='Basic GWO')
    ax2.plot(advanced_gwo.hypervolume_history, 'r-', linewidth=2, label='Advanced GWO')
    ax2.set_xlabel('Generation')
    ax2.set_ylabel('Hypervolume')
    ax2.set_title('Convergence Comparison')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot hypervolume statistics
    methods = ['Basic GWO', 'Advanced GWO']
    hv_means = [np.mean(results['basic_gwo']['hypervolumes']), 
                np.mean(results['advanced_gwo']['hypervolumes'])]
    hv_stds = [np.std(results['basic_gwo']['hypervolumes']), 
               np.std(results['advanced_gwo']['hypervolumes'])]
    
    ax3.bar(methods, hv_means, yerr=hv_stds, capsize=5, 
            color=['blue', 'red'], alpha=0.7)
    ax3.set_ylabel('Hypervolume')
    ax3.set_title('Hypervolume Comparison')
    ax3.grid(True, alpha=0.3)
    
    # Plot execution time comparison
    time_means = [np.mean(results['basic_gwo']['times']), 
                  np.mean(results['advanced_gwo']['times'])]
    time_stds = [np.std(results['basic_gwo']['times']), 
                 np.std(results['advanced_gwo']['times'])]
    
    ax4.bar(methods, time_means, yerr=time_stds, capsize=5, 
            color=['blue', 'red'], alpha=0.7)
    ax4.set_ylabel('Execution Time (s)')
    ax4.set_title('Execution Time Comparison')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{test_function_name.lower()}_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """
    Main benchmarking script
    """
    print("Advanced GWO Benchmark Suite")
    print("=" * 60)
    
    # Test functions to benchmark
    test_functions = ['UF1', 'UF7', 'ZDT1', 'ZDT2', 'ZDT3']
    
    all_results = {}
    
    for test_func_name in test_functions:
        try:
            print(f"\nTesting {test_func_name}...")
            results, basic_gwo, advanced_gwo = run_benchmark(
                test_func_name, dim=30, runs=3, max_gen=50, pop_size=50
            )
            
            all_results[test_func_name] = results
            
            # Plot comparison
            plot_comparison(results, basic_gwo, advanced_gwo, test_func_name)
            
        except Exception as e:
            print(f"Error testing {test_func_name}: {e}")
            continue
    
    # Overall summary
    print(f"\n{'='*60}")
    print("OVERALL BENCHMARK SUMMARY")
    print(f"{'='*60}")
    
    for test_func, results in all_results.items():
        basic_hv = np.mean(results['basic_gwo']['hypervolumes'])
        advanced_hv = np.mean(results['advanced_gwo']['hypervolumes'])
        
        if basic_hv > 0:
            improvement = ((advanced_hv - basic_hv) / basic_hv) * 100
            print(f"{test_func:10s}: {improvement:+7.2f}% improvement")
        else:
            print(f"{test_func:10s}: N/A (Basic GWO failed)")
    
    # Save results
    with open('benchmark_results.json', 'w') as f:
        # Convert numpy arrays to lists for JSON serialization
        json_results = {}
        for test_func, results in all_results.items():
            json_results[test_func] = {
                'basic_gwo': {
                    'hypervolumes': results['basic_gwo']['hypervolumes'],
                    'times': results['basic_gwo']['times'],
                    'archive_sizes': results['basic_gwo']['archive_sizes']
                },
                'advanced_gwo': {
                    'hypervolumes': results['advanced_gwo']['hypervolumes'],
                    'times': results['advanced_gwo']['times'],
                    'archive_sizes': results['advanced_gwo']['archive_sizes']
                }
            }
        json.dump(json_results, f, indent=2)
    
    print(f"\nResults saved to 'benchmark_results.json'")

if __name__ == "__main__":
    main()