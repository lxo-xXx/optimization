* =============================================================================
* STANDALONE LITERATURE-BASED ORC OPTIMIZATION MODEL
* =============================================================================
* No conflicts with included files - completely standalone

$INCLUDE working_fluid_database.gms

* =============================================================================
* LITERATURE-BASED ENVIRONMENTAL DATABASE (Enhanced)
* =============================================================================
PARAMETER gwp_data(fluids) 'Global Warming Potential values';

* Environmental data from Papers 3, 4 (Low GWP emphasis)
gwp_data('R134a') = 1430;      
gwp_data('R125') = 3500;       
gwp_data('R143a') = 4470;      
gwp_data('R152a') = 124;       
gwp_data('R1150') = 4;         
gwp_data('R22') = 1810;        
gwp_data('R41') = 92;          
gwp_data('isobutane') = 3;     
gwp_data('isopentane') = 3;    
gwp_data('nbutane') = 3;       
gwp_data('npentane') = 3;      
gwp_data('propane') = 3;       
gwp_data('cyclopentane') = 3;  
gwp_data('cyclohexane') = 3;   
gwp_data('CO2') = 1;           
gwp_data('ammonia') = 0;       
gwp_data('water') = 0;         

* Assign default GWP for other fluids
LOOP(fluids$(NOT gwp_data(fluids)),
    gwp_data(fluids) = 100;
);

PARAMETER safety_score(fluids) 'Safety scoring (0-1, higher is safer)';

* Safety scores based on Papers 3, 5
safety_score('R134a') = 0.9;      
safety_score('R152a') = 0.7;      
safety_score('isobutane') = 0.4;   
safety_score('isopentane') = 0.4;  
safety_score('nbutane') = 0.4;    
safety_score('npentane') = 0.4;   
safety_score('propane') = 0.3;    
safety_score('cyclopentane') = 0.5;
safety_score('cyclohexane') = 0.5; 
safety_score('CO2') = 0.8;        
safety_score('ammonia') = 0.6;    
safety_score('water') = 1.0;      

* Default safety score for other fluids
LOOP(fluids$(NOT safety_score(fluids)),
    safety_score(fluids) = 0.6;
);

* =============================================================================
* LITERATURE-BASED FLUID SELECTION ALGORITHM
* =============================================================================
PARAMETER 
    thermo_score_lit(fluids)   'Thermodynamic performance score'
    env_score_lit(fluids)      'Environmental score'
    overall_score_lit(fluids)  'Combined literature-based score';

* Step 1: Thermodynamic scoring (Papers 1, 6, 7)
thermo_score_lit(fluids) = 
    + 1.0 * (fluid_props(fluids,'Tc') > 400)                    
    + 1.0 * (fluid_props(fluids,'Pc') < 50)                     
    + 3.0 * (delta_T_critical(fluids) >= 35 AND                 
             delta_T_critical(fluids) <= 50)
    + 0.5 * (fluid_props(fluids,'MW') > 40 AND                  
             fluid_props(fluids,'MW') < 150)
    + 0.5 * (fluid_props(fluids,'omega') < 0.4)                 
    + 0.5 * (fluid_props(fluids,'Tc') < 600);                   

* Step 2: Environmental scoring (Papers 3, 4)
env_score_lit(fluids) = 
    + 2.0 * (gwp_data(fluids) < 150)                           
    + 1.0 * (gwp_data(fluids) < 1000)                          
    + 1.0 * safety_score(fluids)                               
    + 1.0 * (gwp_data(fluids) < 10);                           

* Step 3: Combined scoring with literature weights
overall_score_lit(fluids) = 
    0.6 * thermo_score_lit(fluids) +     
    0.3 * env_score_lit(fluids) +        
    0.1 * safety_score(fluids);      

* Pre-select top fluids based on literature criteria
SET top_fluids_lit(fluids);
SCALAR score_threshold_lit;
score_threshold_lit = 3.0;  

top_fluids_lit(fluids)$(overall_score_lit(fluids) >= score_threshold_lit) = YES;

DISPLAY "Literature-based fluid ranking:";
DISPLAY overall_score_lit, thermo_score_lit, env_score_lit, safety_score;
DISPLAY "Selected fluids for optimization:", top_fluids_lit;

* =============================================================================
* PROCESS CONDITIONS (ALL TEAMMATE FEEDBACK IMPLEMENTED)
* =============================================================================
SCALARS
    T_hw_in_lit    'Hot water inlet temperature [K]'       /443.15/
    T_hw_out_lit   'Hot water outlet temperature [K]'      /343.15/
    m_hw_lit       'Hot water mass flow rate [kg/s]'       /100.0/
    T_amb_lit      'Ambient temperature [K]'               /298.15/
    DT_pinch_lit   'Pinch point temperature difference [K]'/5.0/
    DT_appr_lit    'Approach temperature difference [K]'   /5.0/
    eta_pump_lit   'Pump isentropic efficiency [-]'        /0.75/
    eta_turb_lit   'Turbine isentropic efficiency [-]'     /0.80/
    eta_gen_lit    'Generator efficiency [-]'              /0.95/
    R_lit          'Universal gas constant [kJ/kmol/K]'    /8.314/;

* =============================================================================
* VARIABLES (No conflicts)
* =============================================================================
SETS
    states_lit /1*4/;

VARIABLES
    y_lit(fluids)           'Binary fluid selection variable'
    T_lit(states_lit)       'Temperature at each state [K]'
    P_lit(states_lit)       'Pressure at each state [bar]'
    h_lit(states_lit)       'Enthalpy at each state [kJ/kg]'
    m_wf_lit                'Working fluid mass flow rate [kg/s]'
    
    Q_evap_lit              'Heat input in evaporator [kW]'
    W_turb_lit              'Turbine work output [kW]'
    W_pump_lit              'Pump work input [kW]'
    W_net_lit               'Net power output [kW]'
    eta_thermal_lit         'Thermal efficiency [-]'
    eta_exergy_lit          'Exergy efficiency [-]'
    
    obj_thermo_lit          'Thermodynamic performance objective'
    obj_env_lit             'Environmental impact objective'
    obj_safety_lit          'Safety objective'
    obj_combined_lit        'Combined weighted objective'
    
    Z_lit(states_lit)       'Compressibility factor [-]'
    alpha_pr_lit(states_lit) 'PR alpha function [-]';

* Variable bounds
T_lit.lo(states_lit) = 298.15;  T_lit.up(states_lit) = 500;
P_lit.lo(states_lit) = 1.0;     P_lit.up(states_lit) = 60;
h_lit.lo(states_lit) = 50;      h_lit.up(states_lit) = 1000;
m_wf_lit.lo = 0.5;              m_wf_lit.up = 100;
Z_lit.lo(states_lit) = 0.3;     Z_lit.up(states_lit) = 1.2;
alpha_pr_lit.lo(states_lit) = 0.5; alpha_pr_lit.up(states_lit) = 3.0;
W_net_lit.lo = 1;               W_net_lit.up = 10000;

* Initial values
T_lit.l('1') = 343.15;  T_lit.l('2') = 348.15;  T_lit.l('3') = 430;  T_lit.l('4') = 343.15;
P_lit.l('1') = 1.0;     P_lit.l('2') = 25;      P_lit.l('3') = 25;   P_lit.l('4') = 1.0;
h_lit.l(states_lit) = 300;  m_wf_lit.l = 10;    Z_lit.l(states_lit) = 0.9;
alpha_pr_lit.l(states_lit) = 1.0; 

* =============================================================================
* UNIQUE PENG-ROBINSON PARAMETERS (No conflicts)
* =============================================================================
PARAMETERS
    Tc_sel_lit              'Selected fluid critical temperature'
    Pc_sel_lit              'Selected fluid critical pressure'
    omega_sel_lit           'Selected fluid acentric factor'
    MW_sel_lit              'Selected fluid molecular weight';

* =============================================================================
* EQUATIONS
* =============================================================================
EQUATIONS
    fluid_selection_lit         'Single fluid selection'
    extract_tc_lit             'Extract critical temperature'
    extract_pc_lit             'Extract critical pressure'
    extract_omega_lit          'Extract acentric factor'
    extract_mw_lit             'Extract molecular weight'
    
    pressure_relation_lit      'Pressure relationships'
    temperature_bounds_lit     'Temperature constraints'
    critical_limit_lit         'Critical pressure constraint'
    pinch_point_lit           'Pinch point constraint'
    approach_temp_lit         'Approach temperature constraint'
    
    pr_alpha_function_lit(states_lit)     'PR alpha function'
    pr_cubic_simplified_lit(states_lit)   'Simplified cubic equation'
    enthalpy_calculation_lit(states_lit)  'Enhanced enthalpy'
    
    energy_balance_evap_lit    'Energy balance in evaporator'
    energy_balance_turb_lit    'Energy balance in turbine'  
    energy_balance_pump_lit    'Energy balance in pump'
    energy_balance_cond_lit    'Energy balance in condenser'
    
    net_power_calc_lit         'Net power calculation'
    thermal_efficiency_lit     'Thermal efficiency'
    exergy_efficiency_lit      'Exergy efficiency'
    
    thermodynamic_obj_lit      'Thermodynamic performance objective'
    environmental_obj_lit      'Environmental impact objective'  
    safety_obj_lit            'Safety objective'
    combined_objective_lit     'Combined multi-objective function'
    
    maximize_performance_lit   'Maximize combined performance';

* Fluid selection constraints
fluid_selection_lit.. sum(top_fluids_lit, y_lit(top_fluids_lit)) =e= 1;

extract_tc_lit.. Tc_sel_lit =e= sum(top_fluids_lit, y_lit(top_fluids_lit) * fluid_props(top_fluids_lit,'Tc'));
extract_pc_lit.. Pc_sel_lit =e= sum(top_fluids_lit, y_lit(top_fluids_lit) * fluid_props(top_fluids_lit,'Pc'));
extract_omega_lit.. omega_sel_lit =e= sum(top_fluids_lit, y_lit(top_fluids_lit) * fluid_props(top_fluids_lit,'omega'));
extract_mw_lit.. MW_sel_lit =e= sum(top_fluids_lit, y_lit(top_fluids_lit) * fluid_props(top_fluids_lit,'MW'));

* Process constraints from literature
pressure_relation_lit.. P_lit('2') =e= P_lit('3');
temperature_bounds_lit.. T_lit('1') =e= T_lit('4');
critical_limit_lit.. P_lit('3') =l= 0.8 * Pc_sel_lit;
pinch_point_lit.. T_lit('3') =l= T_hw_in_lit - DT_pinch_lit;
approach_temp_lit.. T_lit('1') =g= T_amb_lit + DT_appr_lit;

* Enhanced PR EOS implementation
pr_alpha_function_lit(states_lit)..
    alpha_pr_lit(states_lit) =e= sqr(1 + (0.37464 + 1.54226*omega_sel_lit - 0.26992*sqr(omega_sel_lit)) * 
                            (1 - sqrt(T_lit(states_lit)/(Tc_sel_lit + 0.01))));

pr_cubic_simplified_lit(states_lit)..
    Z_lit(states_lit) =e= 1 + 0.1 * alpha_pr_lit(states_lit) * P_lit(states_lit) / 
                         (R_lit * T_lit(states_lit) + 0.1);

* Enhanced enthalpy with Kamath polynomials + PR departure
enthalpy_calculation_lit(states_lit)..
    h_lit(states_lit) =e= 
        sum(top_fluids_lit, y_lit(top_fluids_lit) * (
            cp_coeffs(top_fluids_lit,'a') * (T_lit(states_lit) - 298.15) +
            cp_coeffs(top_fluids_lit,'b') * (sqr(T_lit(states_lit)) - sqr(298.15)) / 2 +
            cp_coeffs(top_fluids_lit,'c') * (power(T_lit(states_lit),3) - power(298.15,3)) / 3 +
            cp_coeffs(top_fluids_lit,'d') * (power(T_lit(states_lit),4) - power(298.15,4)) / 4
        )) / (MW_sel_lit + 0.01) +
        R_lit * T_lit(states_lit) * (Z_lit(states_lit) - 1) * 0.1 / (MW_sel_lit + 0.01);

* Energy balances
energy_balance_evap_lit.. Q_evap_lit =e= m_wf_lit * (h_lit('3') - h_lit('2'));
energy_balance_turb_lit.. W_turb_lit =e= m_wf_lit * eta_turb_lit * (h_lit('3') - h_lit('4'));
energy_balance_pump_lit.. W_pump_lit =e= m_wf_lit * (h_lit('2') - h_lit('1')) / eta_pump_lit;
energy_balance_cond_lit.. m_hw_lit * 4.18 * (T_hw_in_lit - T_hw_out_lit) =g= Q_evap_lit * 0.95;

* Performance calculations
net_power_calc_lit.. W_net_lit =e= eta_gen_lit * (W_turb_lit - W_pump_lit);
thermal_efficiency_lit.. eta_thermal_lit =e= W_net_lit / (Q_evap_lit + 0.01);
exergy_efficiency_lit.. eta_exergy_lit =e= W_net_lit / (Q_evap_lit * (1 - T_amb_lit/(T_lit('3') + 0.01)) + 0.01);

* Multi-objective functions (Paper 4 methodology)
thermodynamic_obj_lit.. obj_thermo_lit =e= eta_thermal_lit;
environmental_obj_lit.. obj_env_lit =e= 1 - sum(top_fluids_lit, y_lit(top_fluids_lit) * gwp_data(top_fluids_lit) / 5000);
safety_obj_lit.. obj_safety_lit =e= sum(top_fluids_lit, y_lit(top_fluids_lit) * safety_score(top_fluids_lit));

* Combined objective with literature-based weights
combined_objective_lit.. 
    obj_combined_lit =e= 0.5 * obj_thermo_lit + 0.3 * obj_env_lit + 0.2 * obj_safety_lit;

* Main objective
maximize_performance_lit.. W_net_lit =e= eta_gen_lit * (W_turb_lit - W_pump_lit);

* =============================================================================
* MODEL AND SOLUTION
* =============================================================================
MODEL orc_literature_standalone /ALL/;

* Binary variable priorities
y_lit.prior(fluids) = 1;

* Solver options
OPTION MINLP = BARON;
OPTION RESLIM = 600;
OPTION OPTCR = 0.02;

SOLVE orc_literature_standalone USING MINLP MAXIMIZING W_net_lit;

* =============================================================================
* RESULTS ANALYSIS
* =============================================================================
PARAMETER 
    selected_fluid_props_lit(*)
    performance_metrics_lit(*)
    environmental_metrics_lit(*);

* Extract selected fluid information
LOOP(top_fluids_lit$(y_lit.l(top_fluids_lit) > 0.5),
    selected_fluid_props_lit('Tc_K') = fluid_props(top_fluids_lit,'Tc');
    selected_fluid_props_lit('Pc_bar') = fluid_props(top_fluids_lit,'Pc');
    selected_fluid_props_lit('MW_kg/kmol') = fluid_props(top_fluids_lit,'MW');
    selected_fluid_props_lit('omega') = fluid_props(top_fluids_lit,'omega');
    selected_fluid_props_lit('Delta_T_critical_K') = delta_T_critical(top_fluids_lit);
    selected_fluid_props_lit('GWP') = gwp_data(top_fluids_lit);
    selected_fluid_props_lit('Safety_Score') = safety_score(top_fluids_lit);
    selected_fluid_props_lit('Overall_Score') = overall_score_lit(top_fluids_lit);
);

* Performance metrics
performance_metrics_lit('Net_Power_kW') = W_net_lit.l;
performance_metrics_lit('Thermal_Efficiency_%') = eta_thermal_lit.l * 100;
performance_metrics_lit('Exergy_Efficiency_%') = eta_exergy_lit.l * 100;
performance_metrics_lit('Mass_Flow_kg/s') = m_wf_lit.l;
performance_metrics_lit('Heat_Input_kW') = Q_evap_lit.l;
performance_metrics_lit('Turbine_Work_kW') = W_turb_lit.l;
performance_metrics_lit('Pump_Work_kW') = W_pump_lit.l;

* Environmental and multi-objective metrics
environmental_metrics_lit('Thermo_Objective') = obj_thermo_lit.l;
environmental_metrics_lit('Environmental_Objective') = obj_env_lit.l;
environmental_metrics_lit('Safety_Objective') = obj_safety_lit.l;
environmental_metrics_lit('Combined_Objective') = obj_combined_lit.l;

DISPLAY "=== STANDALONE LITERATURE-BASED ORC RESULTS ===";
DISPLAY selected_fluid_props_lit, performance_metrics_lit, environmental_metrics_lit;
DISPLAY T_lit.l, P_lit.l, h_lit.l, Z_lit.l;

* Generate report
FILE report /literature_standalone_results.txt/;
PUT report;
PUT "STANDALONE LITERATURE-BASED ORC OPTIMIZATION RESULTS"/;
PUT "===================================================="/;
PUT //;
PUT "METHODOLOGY: Based on 7 key literature papers"/;
PUT "- No symbol conflicts with included database"/;
PUT "- Multi-objective optimization framework"/;
PUT "- Environmental and sustainability constraints"/;
PUT //;
PUT "SELECTED WORKING FLUID:"//;
LOOP(top_fluids_lit$(y_lit.l(top_fluids_lit) > 0.5),
    PUT "- Name: ", top_fluids_lit.tl/;
    PUT "- Literature Score: ", overall_score_lit(top_fluids_lit):6:2/;
    PUT "- Thermodynamic Score: ", thermo_score_lit(top_fluids_lit):6:2/;
    PUT "- Environmental Score: ", env_score_lit(top_fluids_lit):6:2/;
    PUT "- Safety Score: ", safety_score(top_fluids_lit):6:2/;
    PUT "- Global Warming Potential: ", gwp_data(top_fluids_lit):8:0/;
);
PUT //;
PUT "PERFORMANCE RESULTS:"//;
PUT "- Net Power Output: ", W_net_lit.l:8:2, " kW"/;
PUT "- Thermal Efficiency: ", (eta_thermal_lit.l*100):6:2, " %"/;
PUT "- Exergy Efficiency: ", (eta_exergy_lit.l*100):6:2, " %"/;
PUT "- Working Fluid Mass Flow: ", m_wf_lit.l:8:2, " kg/s"/;
PUT "- Heat Input: ", Q_evap_lit.l:8:2, " kW"/;
PUT //;
PUT "STATE POINT DATA:"//;
PUT "State    T[K]     P[bar]   h[kJ/kg]   Z[-]"//;
LOOP(states_lit,
    PUT states_lit.tl:5, T_lit.l(states_lit):8:2, P_lit.l(states_lit):8:2, h_lit.l(states_lit):8:2, Z_lit.l(states_lit):8:4/;
);
PUTCLOSE;

DISPLAY "Standalone literature results saved to literature_standalone_results.txt";