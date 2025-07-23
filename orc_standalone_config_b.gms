$title Heat Recovery Process Optimization - Configuration B (Standalone)

* Heat Recovery Process Optimization Competition
* Configuration B: ORC Unit with Recuperator (30% bonus)
* Standalone version without include dependencies

Sets
    i       working fluids /R134a, R245fa, R600a, R290, R1234yf/
    comp    components /1*6/;

* Component mapping for Configuration B:
* 1 = Evaporator outlet (turbine inlet) - superheated vapor
* 2 = Turbine outlet (recuperator hot inlet) - wet/superheated vapor
* 3 = Recuperator hot outlet (condenser inlet) - cooled vapor
* 4 = Condenser outlet (pump inlet) - saturated liquid
* 5 = Pump outlet (recuperator cold inlet) - compressed liquid
* 6 = Recuperator cold outlet (evaporator inlet) - preheated liquid

Parameters
* Hot water stream specifications
    T_hw_in     Hot water inlet temperature [K] /443.15/
    T_hw_out    Hot water outlet temperature [K] /298.15/
    m_hw        Hot water mass flow rate [kg per s] /27.78/
    cp_hw       Hot water specific heat [kJ per kg K] /4.18/
    
* Process design parameters
    T_cond      Condensing temperature [K] /343.15/
    DT_pp       Pinch point temperature difference [K] /5.0/
    eta_pump    Pump isentropic efficiency /0.75/
    eta_turb    Turbine isentropic efficiency /0.80/
    eta_gen     Generator efficiency /0.95/
    DT_approach Approach temperature difference [K] /5.0/
    DT_recup    Recuperator minimum temperature difference [K] /10.0/
    
* Available heat
    Q_available Available heat from hot water [kW];

Q_available = m_hw * cp_hw * (T_hw_in - T_hw_out);

* Working fluid properties (simplified)
Table fluid_props(i,*)
                Tc      Pc      omega   Mw      cp_avg
    R134a      374.21  40.59   0.3268  102.03  1.25
    R245fa     427.16  36.51   0.3776  134.05  1.35
    R600a      407.81  36.48   0.1835  58.12   2.15
    R290       369.83  42.51   0.1521  44.10   2.85
    R1234yf    367.85  33.82   0.2760  114.04  1.15;

Variables
    W_net       Net power output [kW]
    W_turb      Turbine work [kW]
    W_pump      Pump work [kW]
    Q_evap      Heat input to evaporator [kW]
    Q_recup     Heat recovered in recuperator [kW]
    m_wf        Working fluid mass flow rate [kg per s]
    T_evap      Evaporation temperature [K]
    T_recup_hot Recuperator hot side temperature [K]
    T_recup_cold Recuperator cold side temperature [K]
    P_evap      Evaporation pressure [bar]
    P_cond      Condensation pressure [bar];

Binary Variables
    y(i)        Working fluid selection;

Positive Variables W_turb, W_pump, Q_evap, Q_recup, m_wf, T_evap, T_recup_hot, T_recup_cold, P_evap, P_cond;
Free Variables W_net;

Equations
    obj         Maximize net power output
    select      Fluid selection constraint
    heat_bal    Heat balance
    power_turb  Turbine power calculation
    power_pump  Pump power calculation
    mass_bal    Mass flow constraint
    recup_bal   Recuperator heat balance
    temp_const  Temperature constraints
    recup_const Recuperator temperature constraint
    press_const Pressure constraints;

* Objective: Maximize net power
obj.. W_net =e= eta_gen * W_turb - W_pump;

* Select exactly one fluid
select.. sum(i, y(i)) =e= 1;

* Heat balance (reduced due to recuperation)
heat_bal.. Q_evap =e= Q_available - Q_recup * 0.5;

* Power calculations
power_turb.. W_turb =e= m_wf * sum(i, y(i) * fluid_props(i,'cp_avg')) * 
                       (T_evap - T_cond) * eta_turb;

power_pump.. W_pump =e= m_wf * 3.0 / eta_pump;

* Mass flow constraint from heat balance
mass_bal.. Q_evap =e= m_wf * sum(i, y(i) * fluid_props(i,'cp_avg')) * 
                     (T_evap - T_recup_cold);

* Recuperator heat balance
recup_bal.. Q_recup =e= m_wf * sum(i, y(i) * fluid_props(i,'cp_avg')) * 
                       (T_recup_cold - T_cond - 50);

* Temperature constraints
temp_const.. T_evap =l= T_hw_in - 30;

* Recuperator temperature constraint
recup_const.. T_recup_hot =g= T_recup_cold + DT_recup;

* Pressure relationship (simplified)
press_const.. P_cond =e= sum(i, y(i) * fluid_props(i,'Pc') * 
                         exp(5.0 * (1 - fluid_props(i,'Tc')/T_cond)));

* Variable bounds
T_evap.lo = T_cond + 20;
T_evap.up = 420;
T_recup_hot.lo = T_cond + 10;
T_recup_hot.up = 400;
T_recup_cold.lo = T_cond + 5;
T_recup_cold.up = 400;
P_evap.lo = 5;
P_evap.up = 50;
P_cond.lo = 1;
P_cond.up = 20;
m_wf.lo = 0.5;
m_wf.up = 200;
Q_recup.lo = 0;
Q_recup.up = 5000;

* Initial values
T_evap.l = 410;
T_recup_hot.l = 380;
T_recup_cold.l = 360;
P_evap.l = 15;
P_cond.l = 8;
m_wf.l = 10;
Q_recup.l = 1000;
y.l(i) = 0.2;

Model orc_config_b /all/;

* Solver options
option mip = cplex;
option minlp = sbb;
option reslim = 600;

solve orc_config_b using minlp maximizing W_net;

* Display results
display "=== CONFIGURATION B RESULTS ===";
display W_net.l, W_turb.l, W_pump.l, Q_evap.l, Q_recup.l;
display T_evap.l, T_recup_hot.l, T_recup_cold.l, m_wf.l;
display y.l;

* Calculate efficiency
parameter eta_thermal_b;
eta_thermal_b = W_net.l / Q_available;
display eta_thermal_b;

* Find optimal fluid
parameter optimal_fluid_b;
loop(i,
    if(y.l(i) > 0.5,
        optimal_fluid_b = ord(i);
    );
);

display optimal_fluid_b;

* Results summary
parameter results_b(*);
results_b('Net Power (kW)') = W_net.l;
results_b('Thermal Efficiency (%)') = eta_thermal_b * 100;
results_b('Mass Flow Rate (kg/s)') = m_wf.l;
results_b('Heat Recovery (kW)') = Q_recup.l;
results_b('Evaporation Temperature (K)') = T_evap.l;
results_b('Optimal Fluid Number') = optimal_fluid_b;

display results_b;