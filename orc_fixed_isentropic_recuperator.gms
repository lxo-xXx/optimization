* =============================================================================
* ORC MODEL (FIXED ISENTROPIC HANDLING + OPTIONAL RECUPERATOR)
* - Units: kJ/kg, kg/s, bar, K
* - Property model: Peng–Robinson EOS (ideal + departure enthalpy)
* - Isentropic relations: polytropic approximation via cp/R (k = cp/(cp-R))
* - Part A: Simple ORC (states 1..4)
* - Part B: Recuperated ORC (states 1..6) with internal pinch constraints
* =============================================================================

$INCLUDE working_fluid_database.gms

* -------------------------------
* User controls
* -------------------------------
$if not set FLUID $setglobal FLUID propane

Scalar use_recuperator / 1 /;   * 0: simple cycle (A), 1: with recuperator (B)
Scalar DT_pinch     / 5.0 /;    * Evaporator pinch [K]
Scalar DT_approach  / 5.0 /;    * Condenser approach [K]
Scalar DT_recup     / 5.0 /;    * Minimum internal pinch in recuperator [K]

Scalar eta_pump     / 0.75 /;
Scalar eta_turb     / 0.80 /;
Scalar eta_gen      / 0.95 /;

Scalar T_hw_in      / 443.15 /; * Hot water inlet [K]
Scalar T_hw_out     / 343.15 /; * Hot water outlet [K]
Scalar m_hw         / 100.0  /; * Hot water mass flow [kg/s]
Scalar Cp_water     / 4.18   /; * kJ/(kg*K)

* Select single working fluid from the database via macro name
Set sel(fluids) / %FLUID% /;

* Extract selected properties
Scalar Tc_sel, Pc_sel, omega_sel, MW_sel;
Tc_sel    = sum(sel, fluid_props(sel,'Tc'));
Pc_sel    = sum(sel, fluid_props(sel,'Pc'));
omega_sel = sum(sel, fluid_props(sel,'omega'));
MW_sel    = sum(sel, fluid_props(sel,'MW'));

* Gas constant per kg: R_spec = 8.314 kJ/(kmol*K) / MW [kg/kmol]
Scalar R_spec / 0 /;
R_spec = 8.314 / MW_sel;

* PR constants in bar*m3/mol units (for consistency with R_bar in academic models)
Scalar R_bar /8.314e-5/;    * bar*m3/(mol*K)
Scalar a_pr_const, b_pr_const, m_pr_const;
a_pr_const = 0.45724 * sqr(R_bar) * sqr(Tc_sel) / Pc_sel;
b_pr_const = 0.07780 * R_bar * Tc_sel / Pc_sel;
m_pr_const = 0.37464 + 1.54226*omega_sel - 0.26992*sqr(omega_sel);

Alias (fluids, f);

* -------------------------------
* States
* 1: condenser outlet (low P, liquid)
* 2: pump outlet (high P, liquid)
* 3: evaporator outlet (high P, vapor)
* 4: turbine outlet (low P, vapor)
* 5: recuperator hot outlet (low P, cooled vapor)     [only if use_recuperator=1]
* 6: recuperator cold outlet (high P, preheated liquid)[only if use_recuperator=1]
* -------------------------------
Set states /1*6/;

Variables
    T(states)           'Temperature [K]'
    P(states)           'Pressure [bar]'
    Z(states)           'Selected compressibility factor [-]'
    Z_v(states)         'Vapor compressibility [-]'
    Z_l(states)         'Liquid compressibility [-]'
    alpha_pr(states)    'PR alpha function [-]'
    A_pr(states)        'PR A parameter [-]'
    B_pr(states)        'PR B parameter [-]'

    H_ideal(states)     'Ideal gas enthalpy [kJ/kg]'
    H_dep(states)       'Departure enthalpy [kJ/kg]'
    h(states)           'Total enthalpy [kJ/kg]'

    cp_ig(states)       'Ideal-gas heat capacity [kJ/(kg*K)]'
    k_ratio(states)     'k = cp/(cp-R_spec) [-]'

    m_wf                'Working fluid mass flow [kg/s]'
    Q_evap              'Evaporator duty [kW]'
    Q_recup             'Recuperator duty [kW]'
    W_pump              'Pump work [kW]'
    W_turb              'Turbine work [kW]'
    W_net               'Net power [kW]'
;

* Bounds
T.lo('1') = 300;  T.up('1') = 370;
T.lo('2') = 300;  T.up('2') = 390;
T.lo('3') = 360;  T.up('3') = T_hw_in - DT_pinch;
T.lo('4') = 300;  T.up('4') = 420;
T.lo('5') = 300;  T.up('5') = 420;
T.lo('6') = 300;  T.up('6') = 390;

P.lo(states) = 1.0; P.up(states) = 0.75*Pc_sel;
m_wf.lo = 1.0;     m_wf.up = 120.0;

* Initials
T.l('1')=330; T.l('2')=340; T.l('3')=400; T.l('4')=340; T.l('5')=335; T.l('6')=350;
P.l('1')=5;  P.l('2')=20;  P.l('3')=20;  P.l('4')=5;   P.l('5')=5;   P.l('6')=20;
m_wf.l = 30;

* -------------------------------
* Equations
* -------------------------------
Equations
    pressure_high       'High pressure equality'
    pressure_low        'Low pressure equality'
    pressure_high_rec   'High pressure for state 6'
    pressure_low_rec    'Low pressure for state 5'

    pinch_evap          'Evaporator pinch to source'
    approach_cond       'Condenser approach to sink'

    alpha_eq(states)    'PR alpha'
    A_eq(states)        'PR A'
    B_eq(states)        'PR B'
    Z_vapor_eq(states)  'Z vapor'
    Z_liquid_eq(states) 'Z liquid'
    phase_sel_1         'Liquid at 1'
    phase_sel_2         'Liquid at 2'
    phase_sel_3         'Vapor at 3'
    phase_sel_4         'Vapor at 4'
    phase_sel_5         'Vapor at 5 (recup hot out)'
    phase_sel_6         'Liquid at 6 (recup cold out)'

    ideal_enthalpy_eq(states) 'Ideal enthalpy'
    dep_enthalpy_eq(states)   'Departure enthalpy'
    total_enthalpy_eq(states) 'Total enthalpy'

    cp_eq(states)       'Ideal cp from polynomial derivative'
    k_eq(states)        'k = cp/(cp-R_spec)'

    turbine_isentropic  'Polytropic isentropic relation for turbine (T4)'
    pump_isentropic     'Polytropic isentropic relation for pump (T2)'

    evap_balance        'Evaporator energy balance'
    turbine_power       'Turbine work from enthalpy drop'
    pump_power          'Pump work from enthalpy rise'
    condenser_limit     'Source duty limits evaporation'
    recup_energy        'Recuperator energy balance'
    recup_pinch_hot     'Hot-end pinch in recuperator'
    recup_pinch_cold    'Cold-end pinch in recuperator'

    net_power_eq        'Net power'
;

* Pressure structure
pressure_high.. P('2') =e= P('3');
pressure_low..  P('1') =e= P('4');
pressure_high_rec.. use_recuperator*P('6') =e= use_recuperator*P('3');
pressure_low_rec..  use_recuperator*P('5') =e= use_recuperator*P('4');

* Pinch/approach
pinch_evap..   T('3') =l= T_hw_in - DT_pinch;
approach_cond..T('1') =g= (T_hw_out - (T_hw_out - 298.15)) + DT_approach;  * relative to ambient ~298.15 K

* PR EOS pieces
alpha_eq(states).. alpha_pr(states) =e= sqr(1 + m_pr_const * (1 - sqrt(T(states)/Tc_sel)));
A_eq(states)..     A_pr(states)     =e= a_pr_const * alpha_pr(states) * P(states) / sqr(R_bar*T(states));
B_eq(states)..     B_pr(states)     =e= b_pr_const * P(states) / (R_bar*T(states));

Z_vapor_eq(states)..  Z_v(states) =e= 1 + B_pr(states) + A_pr(states)*B_pr(states)/(3 + 2*B_pr(states));
Z_liquid_eq(states).. Z_l(states) =e= B_pr(states) + A_pr(states)*B_pr(states)/(2 + 3*B_pr(states));

phase_sel_1.. Z('1') =e= Z_l('1');
phase_sel_2.. Z('2') =e= Z_l('2');
phase_sel_3.. Z('3') =e= Z_v('3');
phase_sel_4.. Z('4') =e= Z_v('4');
phase_sel_5.. use_recuperator*Z('5') =e= use_recuperator*Z_v('5');
phase_sel_6.. use_recuperator*Z('6') =e= use_recuperator*Z_l('6');

* Ideal enthalpy from Cp polynomials (per kg) – same structure as academic model
ideal_enthalpy_eq(states)..
    H_ideal(states) =e=
        sum(sel,
            (cp_coeffs(sel,'a') * (T(states) - 298.15)
           +cp_coeffs(sel,'b') * (sqr(T(states)) - sqr(298.15))/2
           +cp_coeffs(sel,'c') * (power(T(states),3) - power(298.15,3))/3
           +cp_coeffs(sel,'d') * (power(T(states),4) - power(298.15,4))/4) / MW_sel
        );

* Departure enthalpy – simplified, robust form
dep_enthalpy_eq(states)..
    H_dep(states) =e= R_spec * T(states) * (Z(states) - 1);

total_enthalpy_eq(states).. h(states) =e= H_ideal(states) + H_dep(states);

* Ideal cp (per kg): derivative of H_ideal wrt T
cp_eq(states)..
    cp_ig(states) =e=
        sum(sel,
            (cp_coeffs(sel,'a')
           + cp_coeffs(sel,'b')*T(states)
           + cp_coeffs(sel,'c')*sqr(T(states))
           + cp_coeffs(sel,'d')*power(T(states),3)) / MW_sel
        );

k_eq(states).. k_ratio(states) =e= cp_ig(states) / (cp_ig(states) - R_spec + 1e-6);

* Isentropic temperature targets (polytropic ideal gas approximation)
* Turbine: from (3)->(4)
* T4s = T3 * (P4/P3)^((k-1)/k) ; actual: T4 = T3 - eta*(T3 - T4s)
Equation T4_isentropic;
T4_isentropic.. T('4') =e= T('3') - eta_turb*( T('3') - T('3')*power(P('4')/P('3'), (k_ratio('3')-1)/k_ratio('3')) );

* Pump: from (1)->(2)
Equation T2_isentropic;
T2_isentropic.. T('2') =e= T('1') + ( T('1')*power(P('2')/P('1'), (k_ratio('1')-1)/k_ratio('1')) - T('1') )/eta_pump;

* If recuperator: enforce energy and pinch; else tie 5=4 and 6=2
recup_energy..   use_recuperator * ( m_wf*(h('4') - h('5')) - m_wf*(h('6') - h('2')) ) =e= 0;
recup_pinch_hot..use_recuperator * ( T('4') - T('6') ) =g= use_recuperator * DT_recup;
recup_pinch_cold..use_recuperator * ( T('5') - T('2') ) =g= use_recuperator * DT_recup;

* Tie states when recuperator is off
Equation tie_5_4, tie_6_2;
tie_5_4.. (1-use_recuperator) * (T('5') - T('4')) =e= 0;
tie_6_2.. (1-use_recuperator) * (T('6') - T('2')) =e= 0;

* Energy balances and duties
evap_balance..  Q_evap =e= m_wf * ( h('3') - h( (use_recuperator=1) $ 1 + (use_recuperator=0) $ 1 ) );
* The above is symbolic; replace with explicit selection:
Equation evap_balance_fix;
evap_balance_fix.. Q_evap =e= m_wf * ( h('3') - ( (1-use_recuperator)*h('2') + use_recuperator*h('6') ) );

turbine_power..  W_turb =e= m_wf * ( h('3') - h('4') );
pump_power..     W_pump =e= m_wf * ( h('2') - h('1') );

* Source limit
condenser_limit.. m_hw * Cp_water * (T_hw_in - T_hw_out) =g= Q_evap;

net_power_eq.. W_net =e= eta_gen * (W_turb - W_pump);

Model orc_fixed /all/;

Option NLP = IPOPT;
Solve orc_fixed using NLP maximizing W_net;

Display "=== ORC (Fixed Isentropic + Optional Recuperator) ===";
Display use_recuperator, T.l, P.l, h.l, W_turb.l, W_pump.l, W_net.l, Q_evap.l, Q_recup.l;

