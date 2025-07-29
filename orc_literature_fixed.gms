$title ORC Optimization Based on Literature Requirements (Fixed)

* Heat Recovery Process Optimization Competition
* Literature-based model with optimal fluid selection (CORRECTED)
* Fixed compilation errors and division by zero issues

Sets
    i       working fluids /R600a, n_Butane, n_Pentane, Cyclopentane, R245fa/
    comp    components /1*4/;

Parameters
* Hot water stream specifications
    T_hw_in     Hot water inlet temperature [K] /443.15/
    T_hw_out    Hot water outlet temperature [K] /298.15/
    m_hw        Hot water mass flow rate [kg per s] /27.78/
    cp_hw       Hot water specific heat [kJ per kg K] /4.18/
    
* Process design parameters
    T_cond      Condensing temperature [K] /343.15/
    T_ambient   Ambient temperature [K] /298.15/
    DT_pp       Pinch point temperature difference [K] /5.0/
    eta_pump    Pump isentropic efficiency /0.75/
    eta_turb    Turbine isentropic efficiency /0.80/
    eta_gen     Generator efficiency /0.95/
    DT_approach Approach temperature difference [K] /5.0/
    
* Available heat
    Q_available Available heat from hot water [kW];

Q_available = m_hw * cp_hw * (T_hw_in - T_hw_out);

* Optimized working fluid properties (CORRECTED)
Table fluid_props(i,*)
                Tc      Pc      omega   Mw      Hvap    cp_avg  GWP     
    R600a      407.81  36.48   0.1835  58.12   365.6   2.15    3       
    n_Butane   425.12  37.96   0.2002  58.12   385.0   2.45    4       
    n_Pentane  469.70  33.70   0.2515  72.15   357.6   2.75    4       
    Cyclopentane 511.69 45.15  0.1956  70.13   389.0   2.90    5       
    R245fa     427.16  36.51   0.3776  134.05  196.0   1.35    1030;

Variables
    W_net       Net power output [kW]
    W_turb      Turbine work [kW]
    W_pump      Pump work [kW]
    Q_evap      Heat input to evaporator [kW]
    m_wf        Working fluid mass flow rate [kg per s]
    T_evap      Evaporation temperature [K]
    P_evap      Evaporation pressure [bar]
    P_cond      Condensation pressure [bar]
    
* Literature-based criteria variables
    DT_critical     Temperature difference from critical [K]
    Hvap_cp_ratio   Enthalpy of vaporization to heat capacity ratio
    
* Exergy variables
    Ex_in       Exergy input [kW]
    Ex_out      Exergy output [kW]
    Ex_dest     Exergy destruction [kW]
    
* Efficiency variables (avoid division by zero)
    eta_thermal Thermal efficiency
    eta_exergy  Exergy efficiency;

Binary Variables
    y(i)        Working fluid selection;

Positive Variables W_turb, W_pump, Q_evap, m_wf, T_evap, P_evap, P_cond, Ex_in, Ex_out, Ex_dest;
Free Variables W_net, DT_critical, Hvap_cp_ratio, eta_thermal, eta_exergy;

Equations
* Objective function
    obj         Maximize net power output
    
* Working fluid selection constraint
    fluid_select    Only one working fluid can be selected
    
* Literature-based fluid selection criteria
    temp_diff_criterion     Temperature difference from critical
    hvap_cp_criterion      Enthalpy of vaporization to cp ratio
    critical_pressure_limit Critical pressure constraint (pe <= 0.9*pc)
    
* Energy balances (simplified but correct)
    energy_bal_hw       Energy balance for hot water
    power_calculation   Power calculation based on thermodynamic cycle
    pump_work_calc      Pump work calculation
    
* Process constraints
    pinch_point         Pinch point constraint in evaporator
    
* Exergy calculations
    exergy_input       Exergy input calculation
    exergy_output      Exergy output calculation
    exergy_destruction Exergy destruction calculation
    
* Efficiency definitions (safe from division by zero)
    thermal_eff_calc   Thermal efficiency calculation
    exergy_eff_calc    Exergy efficiency calculation;

* Objective: Maximize net power output
obj.. W_net =e= eta_gen * W_turb - W_pump;

* Working fluid selection constraint
fluid_select.. sum(i, y(i)) =e= 1;

* Literature-based fluid selection criteria
temp_diff_criterion.. DT_critical =e= sum(i, y(i) * fluid_props(i,'Tc')) - T_hw_in;

hvap_cp_criterion.. Hvap_cp_ratio =e= sum(i, y(i) * fluid_props(i,'Hvap')) / 
                                     sum(i, y(i) * fluid_props(i,'cp_avg'));

* Critical pressure constraint: pe <= 0.9 * pc (2016 paper requirement)
critical_pressure_limit.. P_evap =l= 0.9 * sum(i, y(i) * fluid_props(i,'Pc'));

* Energy balance for hot water
energy_bal_hw.. Q_evap =e= Q_available;

* Power calculation based on simplified thermodynamic cycle
power_calculation.. W_turb =e= m_wf * sum(i, y(i) * fluid_props(i,'cp_avg')) * 
                              (T_evap - T_cond) * eta_turb;

* Pump work calculation
pump_work_calc.. W_pump =e= m_wf * sum(i, y(i) * fluid_props(i,'cp_avg')) * 
                           (T_evap - T_cond) * 0.05 / eta_pump;

* Process constraints
pinch_point.. T_evap =l= T_hw_in - DT_pp;

* Exergy analysis
exergy_input.. Ex_in =e= Q_evap * (1 - T_ambient/T_hw_in);

exergy_output.. Ex_out =e= W_net;

exergy_destruction.. Ex_dest =e= Ex_in - Ex_out;

* Safe efficiency calculations (avoid division by zero)
thermal_eff_calc.. eta_thermal * Q_evap =e= W_net;

exergy_eff_calc.. eta_exergy * Ex_in =e= Ex_out;

* Variable bounds
T_evap.lo = T_cond + 10; T_evap.up = T_hw_in - 10;
P_evap.lo = 5.0; P_evap.up = 30.0;
P_cond.lo = 3.0; P_cond.up = 15.0;
m_wf.lo = 5.0; m_wf.up = 100.0;

* Literature criteria bounds
DT_critical.lo = -80; DT_critical.up = 100;
Hvap_cp_ratio.lo = 100; Hvap_cp_ratio.up = 200;

* Efficiency bounds
eta_thermal.lo = 0.05; eta_thermal.up = 0.30;
eta_exergy.lo = 0.10; eta_exergy.up = 0.50;

* Initial values (feasible)
T_evap.l = 400;
P_evap.l = 20.0;
P_cond.l = 8.0;
m_wf.l = 30.0;
Q_evap.l = Q_available;
W_turb.l = 8000;
W_pump.l = 400;
W_net.l = 7000;

* Initialize with best fluid (R600a) based on analysis
y.l('R600a') = 1.0;
y.l('n_Butane') = 0.0;
y.l('n_Pentane') = 0.0;
y.l('Cyclopentane') = 0.0;
y.l('R245fa') = 0.0;

Model orc_literature_fixed /all/;

* Solver options
option mip = cplex;
option minlp = sbb;
option reslim = 600;
option iterlim = 50000;

* Solve the optimization problem
solve orc_literature_fixed using minlp maximizing W_net;

* Display results
display "=== LITERATURE-BASED ORC OPTIMIZATION RESULTS (FIXED) ===";
display W_net.l, W_turb.l, W_pump.l, Q_evap.l;
display T_evap.l, P_evap.l, P_cond.l, m_wf.l;
display eta_thermal.l, eta_exergy.l;
display Ex_in.l, Ex_out.l, Ex_dest.l;
display DT_critical.l, Hvap_cp_ratio.l;
display y.l;

* Find optimal fluid
parameter optimal_fluid_index;
loop(i,
    if(y.l(i) > 0.5,
        optimal_fluid_index = ord(i);
    );
);

* Calculate derived metrics
parameter derived_metrics(*);
derived_metrics('Net Power (kW)') = W_net.l;
derived_metrics('Thermal Efficiency (%)') = eta_thermal.l * 100;
derived_metrics('Exergy Efficiency (%)') = eta_exergy.l * 100;
derived_metrics('Exergy Destruction (kW)') = Ex_dest.l;
derived_metrics('Mass Flow Rate (kg/s)') = m_wf.l;
derived_metrics('Evaporation Temperature (K)') = T_evap.l;
derived_metrics('Evaporation Pressure (bar)') = P_evap.l;
derived_metrics('Pressure Ratio') = P_evap.l / P_cond.l;
derived_metrics('Optimal Fluid Index') = optimal_fluid_index;

* Literature analysis
parameter literature_metrics(*);
literature_metrics('Critical Temperature (K)') = sum(i, y.l(i) * fluid_props(i,'Tc'));
literature_metrics('Critical Pressure (bar)') = sum(i, y.l(i) * fluid_props(i,'Pc'));
literature_metrics('Temperature Difference (K)') = DT_critical.l;
literature_metrics('Hvap/Cp Ratio') = Hvap_cp_ratio.l;
literature_metrics('Max Evap Pressure (bar)') = P_evap.l;
literature_metrics('Critical Pressure Limit (bar)') = 0.9 * sum(i, y.l(i) * fluid_props(i,'Pc'));
literature_metrics('GWP') = sum(i, y.l(i) * fluid_props(i,'GWP'));

display "=== PERFORMANCE METRICS ===";
display derived_metrics;

display "=== LITERATURE-BASED ANALYSIS ===";
display literature_metrics;

* Compliance check
parameter compliance_check(*);
compliance_check('Critical Pressure OK') = 1$(P_evap.l <= 0.9 * sum(i, y.l(i) * fluid_props(i,'Pc')));
compliance_check('Pinch Point OK') = 1$(T_evap.l <= T_hw_in - DT_pp);
compliance_check('Positive Power') = 1$(W_net.l > 0);
compliance_check('Realistic Efficiency') = 1$(eta_thermal.l < 0.30);

display "=== COMPLIANCE CHECK ===";
display compliance_check;

* Fluid name mapping
parameter fluid_names(*);
fluid_names(1) = 1; * R600a
fluid_names(2) = 2; * n_Butane  
fluid_names(3) = 3; * n_Pentane
fluid_names(4) = 4; * Cyclopentane
fluid_names(5) = 5; * R245fa

display "=== FLUID SELECTION ===";
display "Selected fluid index:", optimal_fluid_index;
if(optimal_fluid_index = 1, display "Selected fluid: R600a (Isobutane)";);
if(optimal_fluid_index = 2, display "Selected fluid: n-Butane";);
if(optimal_fluid_index = 3, display "Selected fluid: n-Pentane";);
if(optimal_fluid_index = 4, display "Selected fluid: Cyclopentane";);
if(optimal_fluid_index = 5, display "Selected fluid: R245fa";);

* Generate final report
file fixed_report /literature_fixed_report.txt/;
put fixed_report;
put "Literature-Based Heat Recovery Process Optimization - CORRECTED"/;
put "==============================================================="/;
put /;
put "Problem Solved Successfully: ", orc_literature_fixed.modelstat:1:0/;
put "Solver Status: ", orc_literature_fixed.solvestat:1:0/;
put /;
put "Selected Working Fluid:"/;
put "- Fluid Index: ", optimal_fluid_index:1:0/;
if(optimal_fluid_index = 1, put "- Fluid Name: R600a (Isobutane)"/;);
if(optimal_fluid_index = 2, put "- Fluid Name: n-Butane"/;);
if(optimal_fluid_index = 3, put "- Fluid Name: n-Pentane"/;);
if(optimal_fluid_index = 4, put "- Fluid Name: Cyclopentane"/;);
if(optimal_fluid_index = 5, put "- Fluid Name: R245fa"/;);
put "- Critical Temperature: ", sum(i, y.l(i) * fluid_props(i,'Tc')):6:1, " K"/;
put "- Critical Pressure: ", sum(i, y.l(i) * fluid_props(i,'Pc')):6:1, " bar"/;
put "- GWP: ", sum(i, y.l(i) * fluid_props(i,'GWP')):6:0/;
put /;
put "Thermodynamic Performance:"/;
put "- Net Power Output: ", W_net.l:8:1, " kW"/;
put "- Thermal Efficiency: ", (eta_thermal.l*100):6:2, " %"/;
put "- Exergy Efficiency: ", (eta_exergy.l*100):6:2, " %"/;
put "- Mass Flow Rate: ", m_wf.l:6:1, " kg/s"/;
put /;
put "Operating Conditions:"/;
put "- Evaporation Temperature: ", T_evap.l:6:1, " K"/;
put "- Evaporation Pressure: ", P_evap.l:6:1, " bar"/;
put "- Condensation Pressure: ", P_cond.l:6:1, " bar"/;
put "- Pressure Ratio: ", (P_evap.l/P_cond.l):6:2/;
put /;
put "Literature Criteria:"/;
put "- Temperature Difference: ", DT_critical.l:6:1, " K"/;
put "- Hvap/Cp Ratio: ", Hvap_cp_ratio.l:6:1/;
put "- Critical Pressure Limit: ", (0.9 * sum(i, y.l(i) * fluid_props(i,'Pc'))):6:1, " bar"/;
put /;
put "Environmental Impact:"/;
put "- GWP: ", sum(i, y.l(i) * fluid_props(i,'GWP')):6:0/;
if(sum(i, y.l(i) * fluid_props(i,'GWP')) < 100, put "- Rating: EXCELLENT (Low GWP)"/;);
if(sum(i, y.l(i) * fluid_props(i,'GWP')) >= 100, put "- Rating: POOR (High GWP)"/;);
putclose fixed_report;

display "Fixed report saved to literature_fixed_report.txt";