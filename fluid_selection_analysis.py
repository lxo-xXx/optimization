#!/usr/bin/env python3
"""
Working Fluid Selection Analysis Based on Literature Requirements

Based on the 2015-2016 literature requirements:
1. High critical temperature
2. Low critical pressure  
3. Temperature difference of 35-50°C between source and critical temperature
4. Maximize enthalpy of vaporization
5. Maximize Hvap/Cp ratio
6. Minimize specific heat capacity
7. Critical pressure constraint: pe <= 0.9 * pc
"""

import math

class WorkingFluidAnalysis:
    def __init__(self):
        self.T_source = 443.15  # Hot water inlet temperature [K]
        self.T_source_celsius = 170.0  # [°C]
        
        # Working fluid database (expanded based on literature)
        self.fluids = {
            'R134a': {
                'Tc': 374.21, 'Pc': 40.59, 'omega': 0.3268, 'Mw': 102.03,
                'Hvap': 217.0, 'cp_avg': 1.25, 'Tb': 247.08, 'GWP': 1430
            },
            'R245fa': {
                'Tc': 427.16, 'Pc': 36.51, 'omega': 0.3776, 'Mw': 134.05,
                'Hvap': 196.0, 'cp_avg': 1.35, 'Tb': 288.29, 'GWP': 1030
            },
            'R600a': {  # Isobutane
                'Tc': 407.81, 'Pc': 36.48, 'omega': 0.1835, 'Mw': 58.12,
                'Hvap': 365.6, 'cp_avg': 2.15, 'Tb': 272.65, 'GWP': 3
            },
            'R290': {  # Propane
                'Tc': 369.83, 'Pc': 42.51, 'omega': 0.1521, 'Mw': 44.10,
                'Hvap': 425.9, 'cp_avg': 2.85, 'Tb': 230.85, 'GWP': 3
            },
            'R1234yf': {
                'Tc': 367.85, 'Pc': 33.82, 'omega': 0.2760, 'Mw': 114.04,
                'Hvap': 178.0, 'cp_avg': 1.15, 'Tb': 243.65, 'GWP': 4
            },
            'R1234ze': {
                'Tc': 382.52, 'Pc': 36.35, 'omega': 0.3136, 'Mw': 114.04,
                'Hvap': 185.0, 'cp_avg': 1.20, 'Tb': 254.15, 'GWP': 6
            },
            'n-Butane': {
                'Tc': 425.12, 'Pc': 37.96, 'omega': 0.2002, 'Mw': 58.12,
                'Hvap': 385.0, 'cp_avg': 2.45, 'Tb': 272.65, 'GWP': 4
            },
            'n-Pentane': {
                'Tc': 469.70, 'Pc': 33.70, 'omega': 0.2515, 'Mw': 72.15,
                'Hvap': 357.6, 'cp_avg': 2.75, 'Tb': 309.22, 'GWP': 4
            },
            'Cyclopentane': {
                'Tc': 511.69, 'Pc': 45.15, 'omega': 0.1956, 'Mw': 70.13,
                'Hvap': 389.0, 'cp_avg': 2.90, 'Tb': 322.40, 'GWP': 5
            },
            'R236fa': {
                'Tc': 398.07, 'Pc': 32.00, 'omega': 0.3770, 'Mw': 152.04,
                'Hvap': 165.0, 'cp_avg': 1.40, 'Tb': 271.71, 'GWP': 9810
            }
        }
    
    def calculate_selection_criteria(self, fluid_name, fluid_props):
        """Calculate fluid selection criteria based on literature"""
        
        # 1. Temperature difference from critical temperature
        DT_critical = fluid_props['Tc'] - self.T_source
        
        # 2. Enthalpy of vaporization to heat capacity ratio
        Hvap_cp_ratio = fluid_props['Hvap'] / fluid_props['cp_avg']
        
        # 3. Critical pressure limit (max evaporation pressure)
        max_evap_pressure = 0.9 * fluid_props['Pc']
        
        # 4. Optimal temperature difference check (35-50°C)
        optimal_temp_diff = 35 <= DT_critical <= 50
        
        # 5. Score calculation (higher is better)
        # Maximize: Tc, Hvap, Hvap/Cp ratio
        # Minimize: Pc, cp_avg
        # Penalize if outside optimal temperature range
        
        tc_score = fluid_props['Tc'] / 500.0  # Normalize to ~1
        pc_score = (50.0 - fluid_props['Pc']) / 50.0  # Higher pressure = lower score
        hvap_score = fluid_props['Hvap'] / 500.0
        hvap_cp_score = Hvap_cp_ratio / 300.0
        cp_score = (5.0 - fluid_props['cp_avg']) / 5.0  # Lower cp = higher score
        temp_diff_score = 1.0 if optimal_temp_diff else 0.5
        
        overall_score = (tc_score + pc_score + hvap_score + hvap_cp_score + 
                        cp_score + temp_diff_score) / 6.0
        
        return {
            'DT_critical': DT_critical,
            'Hvap_cp_ratio': Hvap_cp_ratio,
            'max_evap_pressure': max_evap_pressure,
            'optimal_temp_diff': optimal_temp_diff,
            'overall_score': overall_score,
            'tc_score': tc_score,
            'pc_score': pc_score,
            'hvap_score': hvap_score,
            'hvap_cp_score': hvap_cp_score,
            'cp_score': cp_score,
            'temp_diff_score': temp_diff_score
        }
    
    def analyze_all_fluids(self):
        """Analyze all fluids and rank them"""
        
        results = {}
        for fluid_name, fluid_props in self.fluids.items():
            results[fluid_name] = {
                **fluid_props,
                **self.calculate_selection_criteria(fluid_name, fluid_props)
            }
        
        # Sort by overall score (descending)
        sorted_fluids = sorted(results.items(), key=lambda x: x[1]['overall_score'], reverse=True)
        
        return sorted_fluids
    
    def print_analysis(self):
        """Print comprehensive fluid selection analysis"""
        
        print("=" * 80)
        print("WORKING FLUID SELECTION ANALYSIS")
        print("Based on Literature Requirements (2015-2016)")
        print("=" * 80)
        print()
        
        print("Selection Criteria:")
        print("1. High critical temperature (Tc)")
        print("2. Low critical pressure (Pc)")
        print("3. Optimal temperature difference: 35-50°C from critical")
        print("4. Maximize enthalpy of vaporization (Hvap)")
        print("5. Maximize Hvap/Cp ratio")
        print("6. Minimize specific heat capacity (Cp)")
        print("7. Critical pressure constraint: pe ≤ 0.9 × pc")
        print("8. Low GWP preferred (environmental consideration)")
        print()
        
        print(f"Source Temperature: {self.T_source_celsius}°C ({self.T_source} K)")
        print()
        
        sorted_fluids = self.analyze_all_fluids()
        
        # Print detailed results
        print("DETAILED ANALYSIS RESULTS:")
        print("-" * 80)
        
        headers = ["Fluid", "Tc(K)", "Pc(bar)", "ΔT(K)", "Hvap", "Hvap/Cp", "Max Pe", "Score"]
        print(f"{headers[0]:<12} {headers[1]:<8} {headers[2]:<8} {headers[3]:<8} {headers[4]:<8} {headers[5]:<8} {headers[6]:<8} {headers[7]:<8}")
        print("-" * 80)
        
        for fluid_name, props in sorted_fluids:
            print(f"{fluid_name:<12} "
                  f"{props['Tc']:<8.1f} "
                  f"{props['Pc']:<8.1f} "
                  f"{props['DT_critical']:<8.1f} "
                  f"{props['Hvap']:<8.1f} "
                  f"{props['Hvap_cp_ratio']:<8.1f} "
                  f"{props['max_evap_pressure']:<8.1f} "
                  f"{props['overall_score']:<8.3f}")
        
        print()
        print("RANKING AND RECOMMENDATIONS:")
        print("-" * 50)
        
        for i, (fluid_name, props) in enumerate(sorted_fluids[:5], 1):
            status = "✓ OPTIMAL" if props['optimal_temp_diff'] else "⚠ ACCEPTABLE"
            gwp_status = "Low GWP" if props['GWP'] < 100 else "High GWP"
            
            print(f"{i}. {fluid_name}")
            print(f"   Score: {props['overall_score']:.3f}")
            print(f"   Temperature difference: {props['DT_critical']:.1f}°C ({status})")
            print(f"   Critical pressure: {props['Pc']:.1f} bar")
            print(f"   Max evaporation pressure: {props['max_evap_pressure']:.1f} bar")
            print(f"   Hvap/Cp ratio: {props['Hvap_cp_ratio']:.1f}")
            print(f"   Environmental: {gwp_status} (GWP = {props['GWP']})")
            print()
        
        # Find optimal fluids based on temperature difference criterion
        optimal_fluids = [(name, props) for name, props in sorted_fluids 
                         if props['optimal_temp_diff']]
        
        print("FLUIDS MEETING OPTIMAL TEMPERATURE DIFFERENCE (35-50°C):")
        print("-" * 60)
        
        if optimal_fluids:
            for fluid_name, props in optimal_fluids:
                print(f"• {fluid_name}: ΔT = {props['DT_critical']:.1f}°C, Score = {props['overall_score']:.3f}")
        else:
            print("No fluids meet the optimal temperature difference criterion.")
            print("Consider fluids with closest temperature differences.")
        
        print()
        print("FINAL RECOMMENDATION:")
        print("-" * 30)
        
        best_fluid_name, best_props = sorted_fluids[0]
        print(f"Primary choice: {best_fluid_name}")
        print(f"• Highest overall score: {best_props['overall_score']:.3f}")
        print(f"• Critical temperature: {best_props['Tc']:.1f} K")
        print(f"• Temperature difference: {best_props['DT_critical']:.1f}°C")
        print(f"• Hvap/Cp ratio: {best_props['Hvap_cp_ratio']:.1f}")
        print(f"• Environmental impact: GWP = {best_props['GWP']}")
        
        # Check if we have environmentally friendly alternatives
        eco_fluids = [(name, props) for name, props in sorted_fluids 
                     if props['GWP'] < 100]
        
        if eco_fluids and eco_fluids[0][0] != best_fluid_name:
            eco_name, eco_props = eco_fluids[0]
            print()
            print(f"Eco-friendly alternative: {eco_name}")
            print(f"• Score: {eco_props['overall_score']:.3f}")
            print(f"• Low GWP: {eco_props['GWP']}")
            print(f"• Temperature difference: {eco_props['DT_critical']:.1f}°C")
        
        return sorted_fluids

if __name__ == "__main__":
    analyzer = WorkingFluidAnalysis()
    results = analyzer.print_analysis()
    
    # Generate summary for GAMS implementation
    print()
    print("=" * 80)
    print("SUMMARY FOR GAMS IMPLEMENTATION")
    print("=" * 80)
    
    top_5 = results[:5]
    print("Top 5 fluids to include in GAMS optimization:")
    for i, (fluid_name, props) in enumerate(top_5, 1):
        print(f"{i}. {fluid_name} (Score: {props['overall_score']:.3f})")
    
    print()
    print("Recommended GAMS fluid set:")
    fluid_names = [name for name, _ in top_5]
    print(f"i working fluids /{', '.join(fluid_names)}/")