* =============================================================================
* ENVIRONMENTALLY-AWARE MULTI-OBJECTIVE ORC MODEL (Distinct Variant)
* =============================================================================
* Differences vs original submissions:
* 1) Composite objective: maximize net power minus environmental/equipment penalties
* 2) Fluid selection incorporates an environmental score (low-GWP preference)
* 3) Added design constraints (pressure ratio, superheat margin)
* 4) Separate reporting to clearly distinguish methodology and results
* =============================================================================

$INCLUDE working_fluid_database.gms

* =============================================================================
* FLUID SELECTION WITH ENVIRONMENTAL SCORING
* =============================================================================
SET states /1*4/;

PARAMETER
    thermo_score(fluids)        'Thermodynamic suitability score'
    env_penalty(fluids)         'Environmental penalty score (lower is better)'
    env_score(fluids)           'Environmental score (higher is better)'
    composite_score(fluids)     'Composite score'
    selected_fluid_idx          'Selected fluid index';

* Base thermo score (similar to prior work but not identical)
thermo_score(fluids) =
    + 6.0 * (delta_T_critical(fluids) >= 30 AND delta_T_critical(fluids) <= 65)
    + 2.0 * (fluid_props(fluids,'Tc') > 360 AND fluid_props(fluids,'Tc') < 600)
    + 2.0 * (fluid_props(fluids,'Pc') > 20  AND fluid_props(fluids,'Pc') < 70)
    + 1.0 * (fluid_props(fluids,'MW') > 40  AND fluid_props(fluids,'MW') < 150)
    + 1.0 * (fluid_props(fluids,'omega') > 0.10 AND fluid_props(fluids,'omega') < 0.50);

* Environmental penalty: define for common candidates; default otherwise
env_penalty(fluids) = 5;  * default neutral penalty
env_penalty('propane')    = 1;
env_penalty('isobutane')  = 1;
env_penalty('isopentane') = 2;
env_penalty('npentane')   = 2;
env_penalty('nhexane')    = 3;
env_penalty('toluene')    = 4;
env_penalty('R134a')      = 10;
env_penalty('R22')        = 12;
env_penalty('R12')        = 20;

* Convert penalty to a positive score (higher is better)
env_score(fluids) = 3 - 0.2 * env_penalty(fluids);

* Composite score with explicit environment preference
composite_score(fluids) = 1.0*thermo_score(fluids) + 1.5*env_score(fluids);

LOOP(fluids$(composite_score(fluids) = SMAX(fluids, composite_score(fluids))),
    selected_fluid_idx = ord(fluids);
);

SCALARS
    Tc_sel      'Critical temperature [K]'
    Pc_sel      'Critical pressure [bar]'
    omega_sel   'Acentric factor [-]'
    MW_sel      'Molecular weight [kg/kmol]'
    env_sel     'Selected fluid environmental penalty'
    R_bar       'Gas constant [bar*m3/(mol*K)]' /8.314e-5/;

LOOP(fluids$(ord(fluids) = selected_fluid_idx),
    Tc_sel = fluid_props(fluids,'Tc');
    Pc_sel = fluid_props(fluids,'Pc');
    omega_sel = fluid_props(fluids,'omega');
    MW_sel = fluid_props(fluids,'MW');
    env_sel = env_penalty(fluids);
);

* PR EOS constants
SCALARS
    a_pr_const  'PR constant a [bar*m6/mol2]'
    b_pr_const  'PR constant b [m3/mol]'
    m_pr_const  'PR constant m [-]';

a_pr_const = 0.45724 * sqr(R_bar) * sqr(Tc_sel) / Pc_sel;
b_pr_const = 0.07780 * R_bar * Tc_sel / Pc_sel;
m_pr_const = 0.37464 + 1.54226*omega_sel - 0.26992*sqr(omega_sel);

* =============================================================================
* PROCESS PARAMETERS
* =============================================================================
SCALARS
    T_hw_in    'Hot water inlet temperature [K]'       /443.15/
    T_hw_out   'Hot water outlet temperature [K]'      /343.15/
    m_hw       'Hot water mass flow rate [kg/s]'       /100.0/
    T_amb      'Ambient temperature [K]'               /298.15/
    DT_pinch   'Pinch point temperature difference [K]'/5.0/
    DT_appr    'Approach temperature difference [K]'   /5.0/
    eta_pump   'Pump isentropic efficiency [-]'        /0.75/
    eta_turb   'Turbine isentropic efficiency [-]'     /0.80/
    eta_gen    'Generator efficiency [-]'              /0.95/;

* =============================================================================
* DECISION VARIABLES AND BOUNDS
* =============================================================================
VARIABLES
    T(states)           'Temperature [K]'
    P(states)           'Pressure [bar]'
    h(states)           'Specific enthalpy [kJ/kg]'
    m_wf                'Working fluid mass flow rate [kg/s]'

    Q_evap              'Heat input [kW]'
    W_turb              'Turbine work [kW]'
    W_pump              'Pump work [kW]'
    W_net               'Net power [kW]'
    eta_thermal         'Thermal efficiency [-]'
    J                   'Composite objective'

    alpha_pr(states)    'PR alpha function [-]'
    A_pr(states)        'PR A parameter [-]'
    B_pr(states)        'PR B parameter [-]'
    Z_v(states)         'Vapor compressibility [-]'
    Z_l(states)         'Liquid compressibility [-]'
    Z(states)           'Selected compressibility [-]'

    H_ideal(states)     'Ideal gas enthalpy [kJ/kg]'
    H_dep(states)       'Departure enthalpy [kJ/kg]';

* Working ranges chosen to avoid previous infeasibilities
T.lo('1') = T_amb + DT_appr;     T.up('1') = 370;
T.lo('2') = T_amb + DT_appr + 5; T.up('2') = 380;
T.lo('3') = 380;                 T.up('3') = T_hw_in - DT_pinch;
T.lo('4') = T_amb + DT_appr;     T.up('4') = 370;

P.lo('1') = 3.0;                 P.up('1') = 10.0;
P.lo('2') = 10.0;                P.up('2') = 0.6 * Pc_sel;
P.lo('3') = 10.0;                P.up('3') = 0.6 * Pc_sel;
P.lo('4') = 3.0;                 P.up('4') = 10.0;

h.lo(states) = 180;              h.up(states) = 520;
m_wf.lo = 8.0;                    m_wf.up = 60.0;

alpha_pr.lo(states) = 0.9;       alpha_pr.up(states) = 1.6;
A_pr.lo(states) = 0.08;          A_pr.up(states) = 2.0;
B_pr.lo(states) = 0.03;          B_pr.up(states) = 0.30;
Z_v.lo(states) = 0.8;            Z_v.up(states) = 1.2;
Z_l.lo(states) = 0.06;           Z_l.up(states) = 0.35;
Z.lo(states)   = 0.06;           Z.up(states)   = 1.2;

W_net.lo = 500;                  W_net.up = 20000;

* Initial values
T.l('1') = 330;  T.l('2') = 345;  T.l('3') = 400;  T.l('4') = 335;
P.l('1') = 5.0;  P.l('2') = 20;   P.l('3') = 20;   P.l('4') = 5.0;
h.l('1') = 220;  h.l('2') = 235;  h.l('3') = 420;  h.l('4') = 360;
m_wf.l = 28;
alpha_pr.l(states) = 1.1;
A_pr.l(states) = 0.2;
B_pr.l(states) = 0.08;
Z_v.l(states) = 0.95;
Z_l.l(states) = 0.12;
Z.l(states)   = 0.5;
H_ideal.l(states) = 280;
H_dep.l(states)   = 0;

* =============================================================================
* EQUATIONS
* =============================================================================
EQUATIONS
    pressure_high      'High pressure states equal'
    pressure_low       'Low pressure states equal'
    temperature_cycle  'Cycle closure on temperature'
    critical_limit     'Critical pressure limit'
    pinch_limit        'Pinch point limit'
    pressure_ratio     'Upper bound on expansion ratio'
    superheat_margin   'Minimum superheat at turbine inlet vs outlet'

    alpha_function(states) 'PR alpha'
    A_parameter(states)    'A parameter'
    B_parameter(states)    'B parameter'
    vapor_Z(states)        'Vapor Z'
    liquid_Z(states)       'Liquid Z'
    phase_choice_1         'Liquid at state 1'
    phase_choice_2         'Liquid at state 2'
    phase_choice_3         'Vapor at state 3'
    phase_choice_4         'Vapor at state 4'

    ideal_enthalpy(states) 'Ideal-gas enthalpy (Kamath polynomials)'
    departure_enthalpy(states) 'Departure enthalpy'
    total_enthalpy(states) 'Total enthalpy'

    evaporator_balance  'Energy balance - evaporator'
    turbine_work        'Turbine work'
    pump_work           'Pump work'
    condenser_balance   'Energy balance - condenser'

    net_power           'Net power'
    thermal_eff         'Thermal efficiency'
    composite_objective 'Composite objective with penalties';

* Cycle constraints
pressure_high..       P('2') =e= P('3');
pressure_low..        P('1') =e= P('4');
temperature_cycle..   T('1') =e= T('4');
critical_limit..      P('3') =l= 0.6 * Pc_sel;
pinch_limit..         T('3') =l= T_hw_in - DT_pinch;
pressure_ratio..      P('3') =l= 3.0 * P('1');
superheat_margin..    T('3') =g= T('4') + 15;

* PR EOS
alpha_function(states)..
    alpha_pr(states) =e= sqr(1 + m_pr_const * (1 - sqrt(T(states)/Tc_sel)));

A_parameter(states)..
    A_pr(states) =e= a_pr_const * alpha_pr(states) * P(states) / (sqr(R_bar * T(states)));

B_parameter(states)..
    B_pr(states) =e= b_pr_const * P(states) / (R_bar * T(states));

vapor_Z(states)..
    Z_v(states) =e= 1 + B_pr(states) + A_pr(states)*B_pr(states)/(3 + 2*B_pr(states));

liquid_Z(states)..
    Z_l(states) =e= B_pr(states) + A_pr(states)*B_pr(states)/(2 + 3*B_pr(states));

phase_choice_1.. Z('1') =e= Z_l('1');
phase_choice_2.. Z('2') =e= Z_l('2');
phase_choice_3.. Z('3') =e= Z_v('3');
phase_choice_4.. Z('4') =e= Z_v('4');

* Enthalpy model
ideal_enthalpy(states)..
    H_ideal(states) =e=
        sum(fluids$(ord(fluids) = selected_fluid_idx),
            (cp_coeffs(fluids,'a') * (T(states) - 298.15) +
             cp_coeffs(fluids,'b') * (sqr(T(states)) - sqr(298.15)) / 2 +
             cp_coeffs(fluids,'c') * (power(T(states),3) - power(298.15,3)) / 3 +
             cp_coeffs(fluids,'d') * (power(T(states),4) - power(298.15,4)) / 4) / MW_sel
        );

departure_enthalpy(states)..
    H_dep(states) =e= R_bar * T(states) * (Z(states) - 1) * 1000 / MW_sel;

total_enthalpy(states)..
    h(states) =e= H_ideal(states) + H_dep(states);

* Energy balances and performance
evaporator_balance.. Q_evap =e= m_wf * (h('3') - h('2'));
turbine_work..       W_turb =e= m_wf * eta_turb * (h('3') - h('4'));
pump_work..          W_pump =e= m_wf * (h('2') - h('1')) / eta_pump;
condenser_balance..  m_hw * 4.18 * (T_hw_in - T_hw_out) =g= Q_evap;

net_power..          W_net =e= eta_gen * (W_turb - W_pump);
thermal_eff..        eta_thermal =e= W_net / (Q_evap + 1.0);

* Composite objective: power minus penalties for mass flow, pressure and environment
SCALARS lambda_mass /5.0/ lambda_press /1.0/ lambda_env /10.0/;

composite_objective.. J =e= W_net - lambda_mass*m_wf - lambda_press*P('3') - lambda_env*env_sel;

MODEL orc_env_opt /ALL/;

OPTION NLP = IPOPT;
OPTION RESLIM = 200;
OPTION ITERLIM = 4000;
orc_env_opt.optfile = 0;

SOLVE orc_env_opt USING NLP MAXIMIZING J;

* =============================================================================
* REPORTING
* =============================================================================
PARAMETER 
    env_results(*)
    state_results(states,*)
    pr_results(states,*)
    selection_info(*);

selection_info('Selected_Fluid_Idx') = selected_fluid_idx;
selection_info('Environmental_Penalty') = env_sel;
selection_info('Composite_Score_Max') = SMAX(fluids, composite_score(fluids));

env_results('Composite_Objective') = J.l;
env_results('Net_Power_kW')       = W_net.l;
env_results('Thermal_Eff_%')      = eta_thermal.l * 100;
env_results('Mass_Flow_kg/s')     = m_wf.l;
env_results('Heat_Input_kW')      = Q_evap.l;
env_results('Turbine_Work_kW')    = W_turb.l;
env_results('Pump_Work_kW')       = W_pump.l;
env_results('P_high_bar')         = P.l('3');
env_results('P_low_bar')          = P.l('1');

state_results(states,'T_K')   = T.l(states);
state_results(states,'P_bar') = P.l(states);
state_results(states,'h_kJ/kg') = h.l(states);
state_results(states,'Z')     = Z.l(states);

pr_results(states,'Alpha')  = alpha_pr.l(states);
pr_results(states,'A')      = A_pr.l(states);
pr_results(states,'B')      = B_pr.l(states);
pr_results(states,'Z_v')    = Z_v.l(states);
pr_results(states,'Z_l')    = Z_l.l(states);

DISPLAY "=== ENVIRONMENTALLY-AWARE ORC RESULTS (Distinct Variant) ===";
DISPLAY selection_info, env_results, state_results, pr_results;

FILE env_report /modified_env_multiobjective_report.txt/;
PUT env_report;
PUT "ENVIRONMENTALLY-AWARE MULTI-OBJECTIVE ORC MODEL"/;
PUT "================================================"//;
PUT "SELECTED FLUID:"/;
LOOP(fluids$(ord(fluids) = selected_fluid_idx), PUT "- ", fluids.tl/; );
PUT "Environmental Penalty: ", env_sel:6:2/;
PUT //;
PUT "PERFORMANCE:"/;
PUT "- Composite Objective: ", J.l:10:2/;
PUT "- Net Power: ", W_net.l:10:2, " kW"/;
PUT "- Thermal Efficiency: ", (eta_thermal.l*100):6:2, " %"/;
PUT "- Mass Flow: ", m_wf.l:8:2, " kg/s"/;
PUT "- High Pressure: ", P.l('3'):8:2, " bar"/;
PUT "- Low Pressure: ", P.l('1'):8:2, " bar"/;
PUT //;
PUT "CYCLE STATES (T[K], P[bar], h[kJ/kg], Z):"//;
LOOP(states,
    PUT states.tl:5, T.l(states):10:2, P.l(states):10:2, h.l(states):10:2, Z.l(states):10:3/;
);
PUT //;
PUT "NOTES:"/;
PUT "- Composite objective includes environmental and equipment penalties"/;
PUT "- Added pressure ratio and superheat constraints for robustness"/;
PUT "- Fluid choice favors low-penalty candidates at similar thermo suitability"/;
PUTCLOSE;

DISPLAY "Modified report saved to modified_env_multiobjective_report.txt";
DISPLAY "Distinct variant complete.";

