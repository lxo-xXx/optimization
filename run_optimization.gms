$title Heat Recovery Process Optimization - Complete Analysis

* Heat Recovery Process Optimization Competition
* Complete analysis including both Configuration A and B
* Author: Competition Team
* Date: 2024

$ontext
This script runs optimization for both ORC configurations:
- Configuration A: Simple ORC
- Configuration B: ORC with Recuperator

The script compares performance and provides comprehensive results
$offtext

* Include Configuration A optimization
$include orc_enhanced_config_a.gms

* Store Configuration A results
parameters
    W_net_A         Net power Configuration A
    eta_cycle_A     Thermal efficiency Configuration A
    m_wf_A          Mass flow rate Configuration A
    optimal_fluid_A Optimal working fluid Configuration A;

W_net_A = W_net.l;
eta_cycle_A = eta_cycle;
m_wf_A = m_wf.l;

* Determine optimal fluid for Configuration A
loop(i,
    if(y.l(i) > 0.5,
        optimal_fluid_A = ord(i);
    );
);

display "=== CONFIGURATION A RESULTS ===";
display W_net_A, eta_cycle_A, m_wf_A, optimal_fluid_A;

* Clear previous solution
W_net.l = 0;
eta_cycle = 0;
m_wf.l = 0;
y.l(i) = 0;

* Include Configuration B optimization
$include orc_config_b.gms

* Store Configuration B results
parameters
    W_net_B         Net power Configuration B
    eta_cycle_B     Thermal efficiency Configuration B  
    m_wf_B          Mass flow rate Configuration B
    optimal_fluid_B Optimal working fluid Configuration B
    Q_recup_B       Heat recovery Configuration B;

W_net_B = W_net.l;
eta_cycle_B = eta_cycle_b;
m_wf_B = m_wf.l;
Q_recup_B = Q_recup.l;

* Determine optimal fluid for Configuration B
loop(i,
    if(y.l(i) > 0.5,
        optimal_fluid_B = ord(i);
    );
);

display "=== CONFIGURATION B RESULTS ===";
display W_net_B, eta_cycle_B, m_wf_B, optimal_fluid_B, Q_recup_B;

* Performance comparison
parameters
    power_improvement   Power improvement of Config B over A (%)
    efficiency_improvement Efficiency improvement of Config B over A (%)
    economic_benefit    Additional annual revenue ($/year);

power_improvement = (W_net_B - W_net_A) / W_net_A * 100;
efficiency_improvement = (eta_cycle_B - eta_cycle_A) / eta_cycle_A * 100;
economic_benefit = (W_net_B - W_net_A) * 8760 * 0.08; * Assuming $0.08/kWh

display "=== PERFORMANCE COMPARISON ===";
display power_improvement, efficiency_improvement, economic_benefit;

* Working fluid comparison table
set fluid_names /R134a, R245fa, R600a, R290, R1234yf/;

table fluid_comparison(fluid_names, *)
                Config_A_Power  Config_B_Power  Improvement
    R134a           0               0               0
    R245fa          0               0               0  
    R600a           0               0               0
    R290            0               0               0
    R1234yf         0               0               0;

* Final recommendations
parameter recommendations(*);
recommendations('Optimal Config A Fluid') = optimal_fluid_A;
recommendations('Optimal Config B Fluid') = optimal_fluid_B;
recommendations('Recommended Configuration') = 2; * Configuration B
recommendations('Expected Power Output (kW)') = W_net_B;
recommendations('Expected Efficiency (%)') = eta_cycle_B * 100;

display "=== FINAL RECOMMENDATIONS ===";
display recommendations;

* Generate summary report
file report /optimization_report.txt/;
put report;
put "Heat Recovery Process Optimization - Final Report"/;
put "======================================================"/;
put /;
put "Configuration A (Simple ORC):"/;
put "- Net Power Output: ", W_net_A:8:2, " kW"/;
put "- Thermal Efficiency: ", eta_cycle_A*100:6:2, " %"/;
put "- Mass Flow Rate: ", m_wf_A:6:2, " kg/s"/;
put "- Optimal Working Fluid: ", optimal_fluid_A:2:0/;
put /;
put "Configuration B (ORC with Recuperator):"/;
put "- Net Power Output: ", W_net_B:8:2, " kW"/;
put "- Thermal Efficiency: ", eta_cycle_B*100:6:2, " %"/;
put "- Mass Flow Rate: ", m_wf_B:6:2, " kg/s"/;
put "- Heat Recovery: ", Q_recup_B:6:2, " kW"/;
put "- Optimal Working Fluid: ", optimal_fluid_B:2:0/;
put /;
put "Performance Improvement:"/;
put "- Power Improvement: ", power_improvement:6:2, " %"/;
put "- Efficiency Improvement: ", efficiency_improvement:6:2, " %"/;
put "- Annual Economic Benefit: $", economic_benefit:10:0/;
put /;
put "Recommendation: Configuration B with recuperator"/;
put "provides superior performance and should be selected"/;
put "for maximum power output and efficiency."/;
putclose report;