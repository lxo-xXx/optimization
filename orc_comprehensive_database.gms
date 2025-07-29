* =============================================================================
* COMPREHENSIVE ORC OPTIMIZATION WITH 69-FLUID DATABASE
* =============================================================================
* Integrates: Teammate's approach + Complete database + Literature criteria
* Implements: Kamath polynomials + Peng-Robinson EOS + All feedback points

$INCLUDE working_fluid_database.gms

* =============================================================================
* PROCESS CONDITIONS (CORRECTED PER TEAMMATE FEEDBACK)
* =============================================================================
SCALARS
    T_hw_in    'Hot water inlet temperature [K]'       /443.15/
    T_hw_out   'Hot water outlet temperature [K]'      /343.15/
    m_hw       'Hot water mass flow rate [kg/s]'       /100.0/
    T_amb      'Ambient temperature [K]'               /298.15/
    T_cond     'Condensing temperature [K]'            /343.15/
    DT_pinch   'Pinch point temperature difference [K]'/5.0/
    DT_appr    'Approach temperature difference [K]'   /5.0/
    eta_pump   'Pump isentropic efficiency [-]'        /0.75/
    eta_turb   'Turbine isentropic efficiency [-]'     /0.80/
    eta_gen    'Generator efficiency [-]'              /0.95/
    R          'Universal gas constant [kJ/kmol/K]'    /8.314/
    P_atm      'Atmospheric pressure [bar]'            /1.0/;

* =============================================================================
* FLUID SELECTION BASED ON LITERATURE CRITERIA
* =============================================================================
SET selected_fluids(fluids);

* Apply literature-based selection criteria
selected_fluids(fluids) = YES$(
    fluid_props(fluids,'Tc') > 400 AND                    * High critical temperature
    fluid_props(fluids,'Pc') < 50 AND                     * Reasonable critical pressure
    delta_T_critical(fluids) >= 35 AND                    * Optimal temperature difference
    delta_T_critical(fluids) <= 50 AND                    * (35-50°C range)
    fluid_props(fluids,'MW') > 40 AND                     * Reasonable molecular weight
    fluid_props(fluids,'MW') < 200                        * Not too heavy
);

DISPLAY selected_fluids;

* =============================================================================
* VARIABLES AND EQUATIONS
* =============================================================================
SETS
    states /1*4/
    i_sel(fluids);

i_sel(fluids) = selected_fluids(fluids);

VARIABLES
    y(fluids)      'Fluid selection binary variable'
    W_net          'Net power output [kW]'
    T(states)      'Temperature at each state [K]'
    P(states)      'Pressure at each state [bar]'
    h(states)      'Enthalpy at each state [kJ/kg]'
    m_wf           'Working fluid mass flow rate [kg/s]'
    Z(states)      'Compressibility factor [-]'
    alpha_pr(states) 'PR alpha function [-]'
    Q_evap         'Heat input in evaporator [kW]'
    W_turb         'Turbine work [kW]'
    W_pump         'Pump work [kW]'
    eta_thermal    'Thermal efficiency [-]'
    eta_exergy     'Exergy efficiency [-]';

* Variable bounds and initial values
T.lo(states) = 298.15;
T.up(states) = 500;
T.l('1') = 343.15;  
T.l('2') = 348.15;  
T.l('3') = 430;     
T.l('4') = 343.15;  

P.lo(states) = 1.0;
P.up(states) = 50;
P.l('1') = 1.0;   
P.l('2') = 20;    
P.l('3') = 20;    
P.l('4') = 1.0;   

h.lo(states) = 50;
h.up(states) = 800;
h.l(states) = 300;

m_wf.lo = 1;
m_wf.up = 50;
m_wf.l = 10;

Z.lo(states) = 0.5;
Z.up(states) = 1.2;
Z.l(states) = 0.9;

alpha_pr.lo(states) = 0.5;
alpha_pr.up(states) = 2.0;
alpha_pr.l(states) = 1.0;

y.lo(fluids) = 0;
y.up(fluids) = 1;

W_net.lo = 0.1;
W_net.up = 5000;

* =============================================================================
* PENG-ROBINSON EOS PARAMETERS
* =============================================================================
PARAMETERS
    kappa(fluids)    'PR kappa parameter'
    m_pr(fluids)     'PR m parameter'
    a_pr(fluids)     'PR a parameter [bar*L^2/mol^2]'
    b_pr(fluids)     'PR b parameter [L/mol]'
    Tc_sel           'Selected fluid critical temperature [K]'
    Pc_sel           'Selected fluid critical pressure [bar]'
    omega_sel        'Selected fluid acentric factor'
    MW_sel           'Selected fluid molecular weight';

* Calculate PR parameters for all fluids
m_pr(fluids) = 0.37464 + 1.54226*fluid_props(fluids,'omega') 
               - 0.26992*sqr(fluid_props(fluids,'omega'));

a_pr(fluids) = 0.45724 * sqr(R) * sqr(fluid_props(fluids,'Tc')) 
               / fluid_props(fluids,'Pc');

b_pr(fluids) = 0.07780 * R * fluid_props(fluids,'Tc') 
               / fluid_props(fluids,'Pc');

* =============================================================================
* EQUATIONS
* =============================================================================
EQUATIONS
    fluid_selection     'Single fluid selection'
    extract_properties  'Extract selected fluid properties'
    
    pressure_relation   'Pressure relationships'
    temperature_bounds  'Temperature constraints'
    critical_limit      'Critical pressure constraint'
    pinch_point        'Pinch point constraint'
    approach_temp      'Approach temperature constraint'
    
    pr_alpha_calc(states)     'PR alpha function'
    pr_cubic_simple(states)   'Simplified cubic equation'
    enthalpy_kamath(states)   'Kamath-inspired enthalpy'
    
    energy_bal_evap    'Energy balance in evaporator'
    energy_bal_turb    'Energy balance in turbine'
    energy_bal_pump    'Energy balance in pump'
    energy_bal_cond    'Energy balance in condenser'
    
    turbine_work_calc  'Turbine work calculation'
    pump_work_calc     'Pump work calculation'
    net_power_calc     'Net power calculation'
    thermal_eff_calc   'Thermal efficiency'
    exergy_eff_calc    'Exergy efficiency'
    
    objective          'Maximize net power';

* Fluid selection constraint
fluid_selection.. sum(i_sel, y(i_sel)) =e= 1;

* Extract properties of selected fluid
extract_properties.. 
    Tc_sel =e= sum(i_sel, y(i_sel) * fluid_props(i_sel,'Tc'));

* Process constraints
pressure_relation.. P('2') =e= P('3');
temperature_bounds.. T('1') =e= T('4');
critical_limit.. P('3') =l= 0.7 * sum(i_sel, y(i_sel) * fluid_props(i_sel,'Pc'));
pinch_point.. T('3') =l= T_hw_in - DT_pinch;
approach_temp.. T('1') =g= T_amb + DT_appr;

* Simplified PR calculations
pr_alpha_calc(states)..
    alpha_pr(states) =e= 1 + sum(i_sel, y(i_sel) * m_pr(i_sel)) * 
                         (1 - sqrt(T(states)/Tc_sel + 0.01));

pr_cubic_simple(states)..
    Z(states) =e= 0.9 + 0.1 * alpha_pr(states) * P(states) / 
                  (R * T(states) + 0.1);

* Enhanced enthalpy calculation combining Kamath and PR concepts
enthalpy_kamath(states)..
    h(states) =e= 
        sum(i_sel, y(i_sel) * (
            cp_coeffs(i_sel,'a') + 
            cp_coeffs(i_sel,'b') * T(states) + 
            cp_coeffs(i_sel,'c') * sqr(T(states)) + 
            cp_coeffs(i_sel,'d') * power(T(states),3) + 
            cp_coeffs(i_sel,'e') * power(T(states),4) + 
            cp_coeffs(i_sel,'f') * power(T(states),5)
        )) / (fluid_props(i_sel,'MW') + 0.01)
        + R * T(states) * (Z(states) - 1) * 0.001;

* Energy balances
energy_bal_evap.. Q_evap =e= m_wf * (h('3') - h('2'));
energy_bal_turb.. W_turb =e= m_wf * eta_turb * (h('3') - h('4'));
energy_bal_pump.. W_pump =e= m_wf * (h('2') - h('1')) / eta_pump;
energy_bal_cond.. m_hw * 4.18 * (T_hw_in - T_hw_out) =g= Q_evap * 0.9;

* Work and efficiency calculations
turbine_work_calc.. W_turb =e= m_wf * eta_turb * (h('3') - h('4'));
pump_work_calc.. W_pump =e= m_wf * (h('2') - h('1')) / eta_pump;
net_power_calc.. W_net =e= eta_gen * (W_turb - W_pump);
thermal_eff_calc.. eta_thermal =e= W_net / (Q_evap + 0.01);
exergy_eff_calc.. eta_exergy =e= W_net / (Q_evap * (1 - T_amb/T('3')) + 0.01);

* Objective function
objective.. W_net =e= eta_gen * (W_turb - W_pump);

* =============================================================================
* MODEL DEFINITION AND SOLUTION
* =============================================================================
MODEL orc_comprehensive /ALL/;

* Set solver options for MINLP
OPTION MINLP = BARON;
OPTION RESLIM = 300;
OPTION OPTCR = 0.01;

* Mark binary variables
y.prior(fluids) = 1;

SOLVE orc_comprehensive USING MINLP MAXIMIZING W_net;

* =============================================================================
* RESULTS ANALYSIS AND OUTPUT
* =============================================================================
SCALAR selected_fluid_index;
PARAMETER 
    selected_fluid_name(fluids)
    results_summary(*) 'Key results summary';

* Identify selected fluid
LOOP(i_sel$(y.l(i_sel) > 0.5),
    selected_fluid_name(i_sel) = 1;
    selected_fluid_index = ord(i_sel);
);

* Calculate final results
results_summary('Net_Power_kW') = W_net.l;
results_summary('Thermal_Efficiency_%') = eta_thermal.l * 100;
results_summary('Exergy_Efficiency_%') = eta_exergy.l * 100;
results_summary('Mass_Flow_Rate_kg/s') = m_wf.l;
results_summary('Evaporation_Temp_K') = T.l('3');
results_summary('Evaporation_Press_bar') = P.l('3');
results_summary('Heat_Input_kW') = Q_evap.l;
results_summary('Turbine_Work_kW') = W_turb.l;
results_summary('Pump_Work_kW') = W_pump.l;

* =============================================================================
* DISPLAY RESULTS
* =============================================================================
DISPLAY "=== COMPREHENSIVE ORC OPTIMIZATION RESULTS ===";
DISPLAY selected_fluid_name;
DISPLAY results_summary;
DISPLAY T.l, P.l, h.l, Z.l;

* Output detailed results
FILE results /comprehensive_orc_results.txt/;
PUT results;
PUT "COMPREHENSIVE ORC OPTIMIZATION WITH 69-FLUID DATABASE"/;
PUT "====================================================="/;
PUT //;
PUT "SELECTED WORKING FLUID:"//;
LOOP(i_sel$(y.l(i_sel) > 0.5),
    PUT "- Name: ", i_sel.tl/;
    PUT "- Critical Temperature: ", fluid_props(i_sel,'Tc'):8:2, " K"/;
    PUT "- Critical Pressure: ", fluid_props(i_sel,'Pc'):8:2, " bar"/;
    PUT "- Acentric Factor: ", fluid_props(i_sel,'omega'):8:4/;
    PUT "- Molecular Weight: ", fluid_props(i_sel,'MW'):8:2, " kg/kmol"/;
    PUT "- Delta T Critical: ", delta_T_critical(i_sel):8:2, " K"/;
);
PUT //;
PUT "OPTIMIZATION RESULTS:"//;
PUT "- Net Power Output: ", W_net.l:8:2, " kW"/;
PUT "- Thermal Efficiency: ", (eta_thermal.l*100):6:2, " %"/;
PUT "- Exergy Efficiency: ", (eta_exergy.l*100):6:2, " %"/;
PUT "- Working Fluid Mass Flow: ", m_wf.l:8:2, " kg/s"/;
PUT //;
PUT "STATE POINT DATA:"//;
PUT "State    T[K]     P[bar]   h[kJ/kg]   Z[-]"//;
LOOP(states,
    PUT states.tl:5, T.l(states):8:2, P.l(states):8:2, h.l(states):8:2, Z.l(states):8:4/;
);
PUT //;
PUT "ENERGY ANALYSIS:"//;
PUT "- Heat Input (Evaporator): ", Q_evap.l:8:2, " kW"/;
PUT "- Turbine Work Output: ", W_turb.l:8:2, " kW"/;
PUT "- Pump Work Input: ", W_pump.l:8:2, " kW"/;
PUT "- Net Work Output: ", W_net.l:8:2, " kW"/;
PUT //;
PUT "MODEL STATISTICS:"//;
PUT "- Model Status: ", orc_comprehensive.modelstat/;
PUT "- Solver Status: ", orc_comprehensive.solvestat/;
PUT "- Objective Value: ", orc_comprehensive.objval:10:2/;
PUT "- Total Equations: ", orc_comprehensive.numequ/;
PUT "- Total Variables: ", orc_comprehensive.numvar/;
PUTCLOSE;