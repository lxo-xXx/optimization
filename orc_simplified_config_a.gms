$title Simplified Heat Recovery Process Optimization - Configuration A

* Simplified ORC Configuration A with working fluid selection
* Focuses on core optimization while maintaining accuracy

Sets
    i working fluids /R134a, R245fa, R600a, R290, R1234yf/;

Parameters
* Hot water stream
    T_hw_in     /443.15/    * Hot water inlet temperature [K]
    T_hw_out    /298.15/    * Hot water outlet temperature [K] 
    m_hw        /27.78/     * Hot water mass flow rate [kg/s]
    cp_hw       /4.18/      * Hot water specific heat [kJ/kg-K]
    
* Process parameters
    T_cond      /343.15/    * Condensing temperature [K]
    DT_pp       /5.0/       * Pinch point temperature difference [K]
    eta_pump    /0.75/      * Pump efficiency
    eta_turb    /0.80/      * Turbine efficiency
    eta_gen     /0.95/      * Generator efficiency;

* Working fluid properties
Table props(i,*)
                Tc      Pc      omega   Mw      cp_avg
    R134a      374.21  40.59   0.3268  102.03  0.85
    R245fa     427.16  36.51   0.3776  134.05  1.10
    R600a      407.81  36.48   0.1835  58.12   1.65
    R290       369.83  42.51   0.1521  44.10   2.20
    R1234yf    367.85  33.82   0.2760  114.04  0.90;

Variables
    W_net       Net power output [kW]
    W_turb      Turbine work [kW] 
    W_pump      Pump work [kW]
    Q_evap      Heat input [kW]
    m_wf        Working fluid mass flow rate [kg/s]
    T_evap      Evaporation temperature [K]
    P_evap      Evaporation pressure [bar]
    P_cond      Condensation pressure [bar];

Binary Variables
    y(i)        Working fluid selection;

Positive Variables W_net, W_turb, W_pump, Q_evap, m_wf, T_evap, P_evap, P_cond;

Equations
    obj         Objective function
    select      Fluid selection constraint
    heat_bal    Heat balance
    power_bal   Power balance
    pinch       Pinch point constraint
    sat_press   Saturation pressure correlation
    mass_flow   Mass flow constraint;

* Maximize net power
obj.. W_net =e= eta_gen * W_turb - W_pump;

* Select exactly one fluid
select.. sum(i, y(i)) =e= 1;

* Heat balance (simplified)
heat_bal.. Q_evap =e= m_hw * cp_hw * (T_hw_in - T_hw_out);

* Power calculations (simplified)
power_bal.. W_turb =e= m_wf * sum(i, y(i) * props(i,'cp_avg')) * 
                      (T_evap - T_cond) * eta_turb;

* Pump work (simplified)
W_pump =e= m_wf * 1.5 / eta_pump;  * Simplified pump work

* Pinch point constraint
pinch.. T_evap =l= T_hw_out + DT_pp;

* Saturation pressure correlation (Antoine-type)
sat_press.. P_cond =e= sum(i, y(i) * props(i,'Pc') * 
                       exp(5.0 * (1 - props(i,'Tc')/T_cond)));

* Mass flow constraint
mass_flow.. Q_evap =e= m_wf * sum(i, y(i) * props(i,'cp_avg')) * 
                      (T_evap - T_cond);

* Variable bounds
T_evap.lo = 350; T_evap.up = 430;
P_evap.lo = 5; P_evap.up = 50;
P_cond.lo = 1; P_cond.up = 20;
m_wf.lo = 0.5; m_wf.up = 10;

* Initial values
T_evap.l = 400;
P_evap.l = 15;
P_cond.l = 8;
m_wf.l = 2;
y.l(i) = 0.2;

Model simple_orc /all/;

* Solver options
option mip = cplex;
option minlp = sbb;
option reslim = 300;

solve simple_orc using minlp maximizing W_net;

* Display results
display W_net.l, W_turb.l, W_pump.l, Q_evap.l;
display T_evap.l, P_evap.l, P_cond.l, m_wf.l;
display y.l;

* Calculate efficiency
parameter eta_thermal;
eta_thermal = W_net.l / Q_evap.l;
display eta_thermal;