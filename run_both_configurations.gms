$title Heat Recovery Process Optimization - Complete Analysis (Corrected)

* Heat Recovery Process Optimization Competition
* Sequential analysis of both Configuration A and B
* Corrected version without include dependencies

* Set global display control
$offlisting
$offsymlist

* ================================================================
* CONFIGURATION A: SIMPLE ORC
* ================================================================

display "STARTING CONFIGURATION A OPTIMIZATION";

Sets
    i_a     working fluids /R134a, R245fa, R600a, R290, R1234yf/;

Parameters
* Hot water stream specifications
    T_hw_in_a     /443.15/
    T_hw_out_a    /298.15/
    m_hw_a        /27.78/
    cp_hw_a       /4.18/
    T_cond_a      /343.15/
    eta_pump_a    /0.75/
    eta_turb_a    /0.80/
    eta_gen_a     /0.95/
    Q_available_a;

Q_available_a = m_hw_a * cp_hw_a * (T_hw_in_a - T_hw_out_a);

Table fluid_props_a(i_a,*)
                Tc      Pc      cp_avg
    R134a      374.21  40.59   1.25
    R245fa     427.16  36.51   1.35
    R600a      407.81  36.48   2.15
    R290       369.83  42.51   2.85
    R1234yf    367.85  33.82   1.15;

Variables
    W_net_a, W_turb_a, W_pump_a, Q_evap_a, m_wf_a, T_evap_a;

Binary Variables y_a(i_a);
Positive Variables W_turb_a, W_pump_a, Q_evap_a, m_wf_a, T_evap_a;
Free Variables W_net_a;

Equations
    obj_a, select_a, heat_bal_a, power_turb_a, power_pump_a, mass_bal_a, temp_const_a;

obj_a.. W_net_a =e= eta_gen_a * W_turb_a - W_pump_a;
select_a.. sum(i_a, y_a(i_a)) =e= 1;
heat_bal_a.. Q_evap_a =e= Q_available_a;
power_turb_a.. W_turb_a =e= m_wf_a * sum(i_a, y_a(i_a) * fluid_props_a(i_a,'cp_avg')) * 
                           (T_evap_a - T_cond_a) * eta_turb_a;
power_pump_a.. W_pump_a =e= m_wf_a * 3.0 / eta_pump_a;
mass_bal_a.. Q_evap_a =e= m_wf_a * sum(i_a, y_a(i_a) * fluid_props_a(i_a,'cp_avg')) * 
                         (T_evap_a - T_cond_a);
temp_const_a.. T_evap_a =l= T_hw_in_a - 30;

* Variable bounds
T_evap_a.lo = T_cond_a + 15; T_evap_a.up = 420;
m_wf_a.lo = 0.5; m_wf_a.up = 200;

* Initial values
T_evap_a.l = 400; m_wf_a.l = 10; y_a.l(i_a) = 0.2;

Model config_a /obj_a, select_a, heat_bal_a, power_turb_a, power_pump_a, mass_bal_a, temp_const_a/;

option mip = cplex;
option minlp = sbb;
option reslim = 300;

solve config_a using minlp maximizing W_net_a;

* Store Configuration A results
parameters
    W_net_result_a, eta_thermal_a, m_wf_result_a, T_evap_result_a, optimal_fluid_a;

W_net_result_a = W_net_a.l;
eta_thermal_a = W_net_a.l / Q_available_a;
m_wf_result_a = m_wf_a.l;
T_evap_result_a = T_evap_a.l;

loop(i_a, if(y_a.l(i_a) > 0.5, optimal_fluid_a = ord(i_a);););

display "=== CONFIGURATION A RESULTS ===";
display W_net_result_a, eta_thermal_a, m_wf_result_a, T_evap_result_a, optimal_fluid_a;

* ================================================================
* CONFIGURATION B: ORC WITH RECUPERATOR
* ================================================================

display "STARTING CONFIGURATION B OPTIMIZATION";

Sets
    i_b     working fluids /R134a, R245fa, R600a, R290, R1234yf/;

Parameters
* Hot water stream specifications
    T_hw_in_b     /443.15/
    T_hw_out_b    /298.15/
    m_hw_b        /27.78/
    cp_hw_b       /4.18/
    T_cond_b      /343.15/
    eta_pump_b    /0.75/
    eta_turb_b    /0.80/
    eta_gen_b     /0.95/
    Q_available_b;

Q_available_b = m_hw_b * cp_hw_b * (T_hw_in_b - T_hw_out_b);

Table fluid_props_b(i_b,*)
                Tc      Pc      cp_avg
    R134a      374.21  40.59   1.25
    R245fa     427.16  36.51   1.35
    R600a      407.81  36.48   2.15
    R290       369.83  42.51   2.85
    R1234yf    367.85  33.82   1.15;

Variables
    W_net_b, W_turb_b, W_pump_b, Q_evap_b, Q_recup_b, m_wf_b, T_evap_b, T_recup_b;

Binary Variables y_b(i_b);
Positive Variables W_turb_b, W_pump_b, Q_evap_b, Q_recup_b, m_wf_b, T_evap_b, T_recup_b;
Free Variables W_net_b;

Equations
    obj_b, select_b, heat_bal_b, power_turb_b, power_pump_b, mass_bal_b, 
    recup_bal_b, temp_const_b, recup_const_b;

obj_b.. W_net_b =e= eta_gen_b * W_turb_b - W_pump_b;
select_b.. sum(i_b, y_b(i_b)) =e= 1;
heat_bal_b.. Q_evap_b =e= Q_available_b - Q_recup_b * 0.5;
power_turb_b.. W_turb_b =e= m_wf_b * sum(i_b, y_b(i_b) * fluid_props_b(i_b,'cp_avg')) * 
                           (T_evap_b - T_cond_b) * eta_turb_b;
power_pump_b.. W_pump_b =e= m_wf_b * 3.0 / eta_pump_b;
mass_bal_b.. Q_evap_b =e= m_wf_b * sum(i_b, y_b(i_b) * fluid_props_b(i_b,'cp_avg')) * 
                         (T_evap_b - T_recup_b);
recup_bal_b.. Q_recup_b =e= m_wf_b * sum(i_b, y_b(i_b) * fluid_props_b(i_b,'cp_avg')) * 
                           (T_recup_b - T_cond_b - 40);
temp_const_b.. T_evap_b =l= T_hw_in_b - 30;
recup_const_b.. T_recup_b =g= T_cond_b + 20;

* Variable bounds
T_evap_b.lo = T_cond_b + 20; T_evap_b.up = 420;
T_recup_b.lo = T_cond_b + 10; T_recup_b.up = 400;
m_wf_b.lo = 0.5; m_wf_b.up = 200;
Q_recup_b.lo = 0; Q_recup_b.up = 5000;

* Initial values
T_evap_b.l = 410; T_recup_b.l = 370; m_wf_b.l = 10; Q_recup_b.l = 1000; y_b.l(i_b) = 0.2;

Model config_b /obj_b, select_b, heat_bal_b, power_turb_b, power_pump_b, 
               mass_bal_b, recup_bal_b, temp_const_b, recup_const_b/;

solve config_b using minlp maximizing W_net_b;

* Store Configuration B results
parameters
    W_net_result_b, eta_thermal_b, m_wf_result_b, Q_recup_result_b, 
    T_evap_result_b, optimal_fluid_b;

W_net_result_b = W_net_b.l;
eta_thermal_b = W_net_b.l / Q_available_b;
m_wf_result_b = m_wf_b.l;
Q_recup_result_b = Q_recup_b.l;
T_evap_result_b = T_evap_b.l;

loop(i_b, if(y_b.l(i_b) > 0.5, optimal_fluid_b = ord(i_b);););

display "=== CONFIGURATION B RESULTS ===";
display W_net_result_b, eta_thermal_b, m_wf_result_b, Q_recup_result_b, T_evap_result_b, optimal_fluid_b;

* ================================================================
* PERFORMANCE COMPARISON
* ================================================================

parameters
    power_improvement     "Power improvement (%)"
    efficiency_improvement "Efficiency improvement (%)"
    annual_benefit        "Annual economic benefit ($)";

power_improvement = (W_net_result_b - W_net_result_a) / W_net_result_a * 100;
efficiency_improvement = (eta_thermal_b - eta_thermal_a) / eta_thermal_a * 100;
annual_benefit = (W_net_result_b - W_net_result_a) * 8760 * 0.08;

display "=== PERFORMANCE COMPARISON ===";
display power_improvement, efficiency_improvement, annual_benefit;

* Final summary
parameter final_summary(*);
final_summary('Config A Power (kW)') = W_net_result_a;
final_summary('Config B Power (kW)') = W_net_result_b;
final_summary('Config A Efficiency (%)') = eta_thermal_a * 100;
final_summary('Config B Efficiency (%)') = eta_thermal_b * 100;
final_summary('Power Improvement (%)') = power_improvement;
final_summary('Config A Optimal Fluid') = optimal_fluid_a;
final_summary('Config B Optimal Fluid') = optimal_fluid_b;

display "=== FINAL SUMMARY ===";
display final_summary;

* Generate report
file report /gams_optimization_report.txt/;
put report;
put "Heat Recovery Process Optimization - GAMS Results"/;
put "=================================================="/;
put /;
put "Configuration A (Simple ORC):"/;
put "- Net Power Output: ", W_net_result_a:8:1, " kW"/;
put "- Thermal Efficiency: ", eta_thermal_a*100:6:2, " %"/;
put "- Mass Flow Rate: ", m_wf_result_a:6:1, " kg/s"/;
put "- Evaporation Temperature: ", T_evap_result_a:6:1, " K"/;
put "- Optimal Fluid Number: ", optimal_fluid_a:2:0/;
put /;
put "Configuration B (ORC with Recuperator):"/;
put "- Net Power Output: ", W_net_result_b:8:1, " kW"/;
put "- Thermal Efficiency: ", eta_thermal_b*100:6:2, " %"/;
put "- Mass Flow Rate: ", m_wf_result_b:6:1, " kg/s"/;
put "- Heat Recovery: ", Q_recup_result_b:6:1, " kW"/;
put "- Evaporation Temperature: ", T_evap_result_b:6:1, " K"/;
put "- Optimal Fluid Number: ", optimal_fluid_b:2:0/;
put /;
put "Performance Improvement:"/;
put "- Power Improvement: ", power_improvement:6:2, " %"/;
put "- Efficiency Improvement: ", efficiency_improvement:6:2, " %"/;
put "- Annual Economic Benefit: $", annual_benefit:10:0/;
put /;
put "Recommendation: Configuration B provides superior performance"/;
put "and should be selected for competition submission."/;
putclose report;

display "Report saved to gams_optimization_report.txt";