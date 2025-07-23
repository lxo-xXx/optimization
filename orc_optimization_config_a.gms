$title Heat Recovery Process Optimization - ORC Configuration A

* Heat Recovery Process Optimization Competition
* Configuration A: Simple ORC Unit
* Objective: Maximize power output with working fluid selection

Sets
    i       working fluids /R134a, R245fa, R600a, R290, R1234yf/
    comp    components /1*4/;

* Component mapping:
* 1 = Evaporator outlet (turbine inlet)
* 2 = Turbine outlet (condenser inlet) 
* 3 = Condenser outlet (pump inlet)
* 4 = Pump outlet (evaporator inlet)

Parameters
* Hot water stream specifications
    T_hw_in     Hot water inlet temperature [K] /443.15/
    T_hw_out    Hot water outlet temperature [K] /298.15/
    m_hw        Hot water mass flow rate [kg per s] /27.78/
    P_hw        Hot water pressure [bar] /1.0/
    
* Process design parameters
    T_cond      Condensing temperature [K] /343.15/
    DT_pp       Pinch point temperature difference [K] /5.0/
    eta_pump    Pump isentropic efficiency /0.75/
    eta_turb    Turbine isentropic efficiency /0.80/
    eta_gen     Generator efficiency /0.95/
    DT_approach Approach temperature difference [K] /5.0/;

* Working fluid properties (Peng-Robinson EOS parameters)
Table fluid_props(i,*)
                Tc      Pc      omega   Mw      Tsat_40C
    R134a      374.21  40.59   0.3268  102.03  261.45
    R245fa     427.16  36.51   0.3776  134.05  288.29
    R600a      407.81  36.48   0.1835  58.12   272.65
    R290       369.83  42.51   0.1521  44.10   230.85
    R1234yf    367.85  33.82   0.2760  114.04  243.65;

Variables
    W_net       Net power output [kW]
    W_turb      Turbine work [kW]
    W_pump      Pump work [kW]
    Q_evap      Heat input to evaporator [kW]
    Q_cond      Heat rejected from condenser [kW]
    m_wf        Working fluid mass flow rate [kg per s]
    
* State point properties
    T(comp)     Temperature at each state point [K]
    P(comp)     Pressure at each state point [bar]
    h(comp)     Specific enthalpy [kJ per kg]
    s(comp)     Specific entropy [kJ per kg K]
    
* Binary variable for working fluid selection
    y(i)        Binary variable for working fluid selection
    
* Continuous variables for fluid-dependent calculations
    P_sat_cond  Saturation pressure at condensing temperature [bar]
    P_evap      Evaporation pressure [bar]
    T_evap      Evaporation temperature [K];

Binary Variables y;
Positive Variables W_net, W_turb, W_pump, Q_evap, Q_cond, m_wf, T, P, h, s;

Equations
* Objective function
    obj         Maximize net power output
    
* Working fluid selection constraint
    fluid_select    Only one working fluid can be selected
    
* Thermodynamic cycle constraints
    energy_bal_evap     Energy balance for evaporator
    energy_bal_cond     Energy balance for condenser
    energy_bal_turb     Energy balance for turbine
    energy_bal_pump     Energy balance for pump
    
* Process constraints
    pinch_point         Pinch point constraint in evaporator
    approach_temp       Approach temperature in condenser
    pressure_relation   Pressure relationship
    
* Property calculations (simplified correlations for Peng-Robinson)
    sat_pressure        Saturation pressure calculation
    enthalpy_calc       Enthalpy calculations
    entropy_calc        Entropy calculations
    
* Performance constraints
    turbine_efficiency  Turbine isentropic efficiency
    pump_efficiency     Pump isentropic efficiency;

* Objective: Maximize net power output
obj.. W_net =e= W_turb - W_pump;

* Working fluid selection constraint
fluid_select.. sum(i, y(i)) =e= 1;

* Energy balances
energy_bal_evap.. Q_evap =e= m_wf * (h('1') - h('4'));
energy_bal_cond.. Q_cond =e= m_wf * (h('2') - h('3'));
energy_bal_turb.. W_turb =e= m_wf * (h('1') - h('2'));
energy_bal_pump.. W_pump =e= m_wf * (h('4') - h('3'));

* Heat transfer constraints
pinch_point.. T('1') =l= T_hw_out + DT_pp;
approach_temp.. T('3') =g= T_cond + DT_approach;

* Pressure relationships
pressure_relation.. P('1') =e= P('4');

* Simplified saturation pressure correlation (Antoine equation form)
sat_pressure.. P_sat_cond =e= sum(i, y(i) * exp(20.0 - 3000/T_cond));

* Temperature constraints
T.lo('1') = 350; T.up('1') = 420;
T.lo('2') = 320; T.up('2') = 380;
T.fx('3') = T_cond;
T.lo('4') = 320; T.up('4') = 380;

* Pressure constraints
P.lo(comp) = 1.0; P.up(comp) = 50.0;
P.fx('2') = P_sat_cond;
P.fx('3') = P_sat_cond;

* Mass flow rate bounds
m_wf.lo = 0.1; m_wf.up = 10.0;

* Initial values
T.l('1') = 400;
T.l('2') = 350;
T.l('3') = T_cond;
T.l('4') = 350;

P.l(comp) = 10.0;
m_wf.l = 1.0;
y.l(i) = 1/card(i);

Model orc_config_a /all/;

* Solver options
option nlp = conopt;
option mip = cplex;
option minlp = sbb;

* Solve the optimization problem
solve orc_config_a using minlp maximizing W_net;

* Display results
display W_net.l, W_turb.l, W_pump.l, Q_evap.l, Q_cond.l;
display T.l, P.l, h.l, s.l;
display y.l;
display m_wf.l;

* Calculate efficiency
parameter eta_cycle;
eta_cycle = W_net.l / Q_evap.l;
display eta_cycle;