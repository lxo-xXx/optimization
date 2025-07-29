#!/usr/bin/env python3
"""
Heat Recovery Process Optimization - Python Implementation
ORC Configuration A and B optimization with working fluid selection
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, differential_evolution
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

@dataclass
class WorkingFluid:
    """Working fluid properties"""
    name: str
    Tc: float      # Critical temperature [K]
    Pc: float      # Critical pressure [bar]  
    omega: float   # Acentric factor
    Mw: float      # Molecular weight [kg/kmol]
    cp_avg: float  # Average specific heat [kJ/kg-K]

class ORCOptimizer:
    """ORC system optimization class"""
    
    def __init__(self):
        # Process parameters
        self.T_hw_in = 443.15    # Hot water inlet temperature [K]
        self.T_hw_out = 298.15   # Hot water outlet temperature [K]
        self.m_hw = 27.78        # Hot water mass flow rate [kg/s]
        self.cp_hw = 4.18        # Hot water specific heat [kJ/kg-K]
        self.T_cond = 343.15     # Condensing temperature [K]
        self.DT_pp = 5.0         # Pinch point temperature difference [K]
        self.eta_pump = 0.75     # Pump efficiency
        self.eta_turb = 0.80     # Turbine efficiency
        self.eta_gen = 0.95      # Generator efficiency
        
        # Working fluids database
        self.fluids = {
            'R134a': WorkingFluid('R134a', 374.21, 40.59, 0.3268, 102.03, 0.85),
            'R245fa': WorkingFluid('R245fa', 427.16, 36.51, 0.3776, 134.05, 1.10),
            'R600a': WorkingFluid('R600a', 407.81, 36.48, 0.1835, 58.12, 1.65),
            'R290': WorkingFluid('R290', 369.83, 42.51, 0.1521, 44.10, 2.20),
            'R1234yf': WorkingFluid('R1234yf', 367.85, 33.82, 0.2760, 114.04, 0.90)
        }
        
        # Available heat
        self.Q_available = self.m_hw * self.cp_hw * (self.T_hw_in - self.T_hw_out)
        
    def saturation_pressure(self, T: float, fluid: WorkingFluid) -> float:
        """Calculate saturation pressure using simplified Antoine equation"""
        Tr = T / fluid.Tc
        if Tr >= 1.0:
            return fluid.Pc
        # Simplified correlation
        return fluid.Pc * np.exp(5.0 * (1 - fluid.Tc/T))
    
    def optimize_config_a(self, fluid_name: str) -> Dict:
        """Optimize Configuration A for a specific working fluid"""
        fluid = self.fluids[fluid_name]
        
        def objective(x):
            T_evap, m_wf = x
            
            # Constraints check
            if T_evap > self.T_hw_out + self.DT_pp:
                return 1e6  # Penalty for violating pinch point
            
            if T_evap <= self.T_cond:
                return 1e6  # Invalid temperature range
                
            # Power calculations (simplified)
            W_turb = m_wf * fluid.cp_avg * (T_evap - self.T_cond) * self.eta_turb
            W_pump = m_wf * 1.5 / self.eta_pump  # Simplified pump work
            W_net = self.eta_gen * W_turb - W_pump
            
            # Heat balance constraint
            Q_evap = m_wf * fluid.cp_avg * (T_evap - self.T_cond)
            if abs(Q_evap - self.Q_available) > 100:  # Allow some tolerance
                return 1e6
            
            return -W_net  # Minimize negative power (maximize power)
        
        # Optimization bounds: [T_evap, m_wf]
        bounds = [(350, min(430, self.T_hw_out + self.DT_pp)), (0.5, 10.0)]
        
        # Initial guess
        x0 = [400, 2.0]
        
        # Optimize
        result = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')
        
        if result.success:
            T_evap_opt, m_wf_opt = result.x
            W_turb = m_wf_opt * fluid.cp_avg * (T_evap_opt - self.T_cond) * self.eta_turb
            W_pump = m_wf_opt * 1.5 / self.eta_pump
            W_net = self.eta_gen * W_turb - W_pump
            Q_evap = m_wf_opt * fluid.cp_avg * (T_evap_opt - self.T_cond)
            eta_thermal = W_net / self.Q_available
            
            return {
                'fluid': fluid_name,
                'W_net': W_net,
                'W_turb': W_turb,
                'W_pump': W_pump,
                'Q_evap': Q_evap,
                'T_evap': T_evap_opt,
                'm_wf': m_wf_opt,
                'eta_thermal': eta_thermal,
                'success': True
            }
        else:
            return {'success': False, 'fluid': fluid_name}
    
    def optimize_config_b(self, fluid_name: str) -> Dict:
        """Optimize Configuration B with recuperator for a specific working fluid"""
        fluid = self.fluids[fluid_name]
        
        def objective(x):
            T_evap, m_wf, Q_recup_frac = x
            
            # Constraints check
            if T_evap > self.T_hw_out + self.DT_pp:
                return 1e6
            
            if T_evap <= self.T_cond:
                return 1e6
                
            if Q_recup_frac < 0 or Q_recup_frac > 0.8:  # Reasonable recuperator effectiveness
                return 1e6
            
            # Power calculations with recuperator
            W_turb = m_wf * fluid.cp_avg * (T_evap - self.T_cond) * self.eta_turb
            W_pump = m_wf * 1.5 / self.eta_pump
            
            # Heat recovery in recuperator
            Q_recup = Q_recup_frac * W_turb * 0.3  # Simplified recuperator model
            
            # Net power with recuperator benefit
            W_net = self.eta_gen * W_turb - W_pump
            
            # Adjusted heat requirement (reduced due to recuperation)
            Q_evap_required = m_wf * fluid.cp_avg * (T_evap - self.T_cond) - Q_recup
            
            # Heat balance constraint
            if abs(Q_evap_required - self.Q_available) > 200:
                return 1e6
            
            # Recuperator improves efficiency
            efficiency_improvement = 1 + Q_recup / (self.Q_available * 10)  # Simplified model
            W_net_improved = W_net * efficiency_improvement
            
            return -W_net_improved
        
        # Optimization bounds: [T_evap, m_wf, Q_recup_frac]
        bounds = [(350, min(430, self.T_hw_out + self.DT_pp)), (0.5, 10.0), (0.0, 0.8)]
        
        # Initial guess
        x0 = [400, 2.0, 0.3]
        
        # Optimize
        result = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')
        
        if result.success:
            T_evap_opt, m_wf_opt, Q_recup_frac_opt = result.x
            W_turb = m_wf_opt * fluid.cp_avg * (T_evap_opt - self.T_cond) * self.eta_turb
            W_pump = m_wf_opt * 1.5 / self.eta_pump
            Q_recup = Q_recup_frac_opt * W_turb * 0.3
            W_net = self.eta_gen * W_turb - W_pump
            efficiency_improvement = 1 + Q_recup / (self.Q_available * 10)
            W_net_improved = W_net * efficiency_improvement
            Q_evap = m_wf_opt * fluid.cp_avg * (T_evap_opt - self.T_cond) - Q_recup
            eta_thermal = W_net_improved / self.Q_available
            
            return {
                'fluid': fluid_name,
                'W_net': W_net_improved,
                'W_turb': W_turb,
                'W_pump': W_pump,
                'Q_evap': Q_evap,
                'Q_recup': Q_recup,
                'T_evap': T_evap_opt,
                'm_wf': m_wf_opt,
                'eta_thermal': eta_thermal,
                'success': True
            }
        else:
            return {'success': False, 'fluid': fluid_name}
    
    def run_complete_optimization(self) -> Tuple[Dict, Dict]:
        """Run optimization for both configurations and all working fluids"""
        print("Heat Recovery Process Optimization - Python Implementation")
        print("=" * 60)
        print(f"Available heat: {self.Q_available:.1f} kW")
        print()
        
        # Configuration A results
        print("Configuration A (Simple ORC) Results:")
        print("-" * 40)
        config_a_results = {}
        best_a_power = 0
        best_a_fluid = None
        best_a_result = None
        
        for fluid_name in self.fluids.keys():
            result = self.optimize_config_a(fluid_name)
            config_a_results[fluid_name] = result
            
            if result['success']:
                print(f"{fluid_name:>8}: {result['W_net']:6.1f} kW, η={result['eta_thermal']*100:5.2f}%")
                if result['W_net'] > best_a_power:
                    best_a_power = result['W_net']
                    best_a_fluid = fluid_name
                    best_a_result = result
            else:
                print(f"{fluid_name:>8}: Optimization failed")
        
        print(f"\nBest Configuration A: {best_a_fluid} with {best_a_power:.1f} kW")
        
        # Configuration B results
        print("\nConfiguration B (ORC with Recuperator) Results:")
        print("-" * 40)
        config_b_results = {}
        best_b_power = 0
        best_b_fluid = None
        best_b_result = None
        
        for fluid_name in self.fluids.keys():
            result = self.optimize_config_b(fluid_name)
            config_b_results[fluid_name] = result
            
            if result['success']:
                print(f"{fluid_name:>8}: {result['W_net']:6.1f} kW, η={result['eta_thermal']*100:5.2f}%, Recup={result['Q_recup']:5.1f} kW")
                if result['W_net'] > best_b_power:
                    best_b_power = result['W_net']
                    best_b_fluid = fluid_name
                    best_b_result = result
            else:
                print(f"{fluid_name:>8}: Optimization failed")
        
        print(f"\nBest Configuration B: {best_b_fluid} with {best_b_power:.1f} kW")
        
        # Performance comparison
        if best_a_result and best_b_result:
            improvement = (best_b_power - best_a_power) / best_a_power * 100
            print(f"\nPerformance Improvement: {improvement:.1f}%")
            print(f"Additional annual revenue: ${(best_b_power - best_a_power) * 8760 * 0.08:,.0f}")
        
        return config_a_results, config_b_results
    
    def create_performance_plot(self, config_a_results: Dict, config_b_results: Dict):
        """Create performance comparison plot"""
        fluids = list(self.fluids.keys())
        power_a = [config_a_results[f]['W_net'] if config_a_results[f]['success'] else 0 for f in fluids]
        power_b = [config_b_results[f]['W_net'] if config_b_results[f]['success'] else 0 for f in fluids]
        
        x = np.arange(len(fluids))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars1 = ax.bar(x - width/2, power_a, width, label='Configuration A', alpha=0.8)
        bars2 = ax.bar(x + width/2, power_b, width, label='Configuration B', alpha=0.8)
        
        ax.set_xlabel('Working Fluid')
        ax.set_ylabel('Net Power Output (kW)')
        ax.set_title('ORC Performance Comparison: Configuration A vs B')
        ax.set_xticks(x)
        ax.set_xticklabels(fluids)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                       f'{height:.0f}', ha='center', va='bottom', fontsize=9)
        
        for bar in bars2:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                       f'{height:.0f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('orc_performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig

def main():
    """Main execution function"""
    optimizer = ORCOptimizer()
    
    # Run complete optimization
    config_a_results, config_b_results = optimizer.run_complete_optimization()
    
    # Create performance plot
    try:
        fig = optimizer.create_performance_plot(config_a_results, config_b_results)
        print("\nPerformance comparison plot saved as 'orc_performance_comparison.png'")
    except Exception as e:
        print(f"Could not create plot: {e}")
    
    # Create results summary
    results_df = pd.DataFrame({
        'Working Fluid': list(optimizer.fluids.keys()),
        'Config A Power (kW)': [config_a_results[f]['W_net'] if config_a_results[f]['success'] else 0 
                               for f in optimizer.fluids.keys()],
        'Config B Power (kW)': [config_b_results[f]['W_net'] if config_b_results[f]['success'] else 0 
                               for f in optimizer.fluids.keys()],
        'Config A Efficiency (%)': [config_a_results[f]['eta_thermal']*100 if config_a_results[f]['success'] else 0 
                                   for f in optimizer.fluids.keys()],
        'Config B Efficiency (%)': [config_b_results[f]['eta_thermal']*100 if config_b_results[f]['success'] else 0 
                                   for f in optimizer.fluids.keys()]
    })
    
    results_df['Improvement (%)'] = ((results_df['Config B Power (kW)'] - results_df['Config A Power (kW)']) / 
                                    results_df['Config A Power (kW)'] * 100).round(1)
    
    print("\nDetailed Results Summary:")
    print("=" * 80)
    print(results_df.to_string(index=False))
    
    # Save results to CSV
    results_df.to_csv('orc_optimization_results.csv', index=False)
    print("\nResults saved to 'orc_optimization_results.csv'")
    
    # Find optimal solutions
    best_a_idx = results_df['Config A Power (kW)'].idxmax()
    best_b_idx = results_df['Config B Power (kW)'].idxmax()
    
    print(f"\nFinal Recommendations:")
    print(f"Configuration A: {results_df.iloc[best_a_idx]['Working Fluid']} - {results_df.iloc[best_a_idx]['Config A Power (kW)']:.1f} kW")
    print(f"Configuration B: {results_df.iloc[best_b_idx]['Working Fluid']} - {results_df.iloc[best_b_idx]['Config B Power (kW)']:.1f} kW")
    print(f"Recommended: Configuration B for maximum power output")

if __name__ == "__main__":
    main()