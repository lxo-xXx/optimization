$title Enhanced Heat Recovery Process Optimization - ORC Configuration A with Peng-Robinson EOS

* Heat Recovery Process Optimization Competition
* Configuration A: Simple ORC Unit with Enhanced Property Calculations
* Using Peng-Robinson EOS and Kamath algorithm

Sets
    i       working fluids /R134a, R245fa, R600a, R290, R1234yf/
    comp    components /1*4/
    iter    iterations /1*20/;

* Component mapping:
* 1 = Evaporator outlet (turbine inlet) - superheated vapor
* 2 = Turbine outlet (condenser inlet) - wet/superheated vapor
* 3 = Condenser outlet (pump inlet) - saturated liquid
* 4 = Pump outlet (evaporator inlet) - compressed liquid

Parameters
* Hot water stream specifications
    T_hw_in     Hot water inlet temperature [K] /443.15/
    T_hw_out    Hot water outlet temperature [K] /298.15/
    m_hw        Hot water mass flow rate [kg per s] /27.78/
    P_hw        Hot water pressure [bar] /1.0/
    cp_hw       Hot water specific heat [kJ per kg K] /4.18/
    
* Process design parameters
    T_cond      Condensing temperature [K] /343.15/
    DT_pp       Pinch point temperature difference [K] /5.0/
    eta_pump    Pump isentropic efficiency /0.75/
    eta_turb    Turbine isentropic efficiency /0.80/
    eta_gen     Generator efficiency /0.95/
    DT_approach Approach temperature difference [K] /5.0/
    
* Universal constants
    R_gas       Universal gas constant [kJ per kmol K] /8.314/;

* Working fluid properties for Peng-Robinson EOS
Table fluid_props(i,*)
                Tc      Pc      omega   Mw      Tb      Hfg_298
    R134a      374.21  40.59   0.3268  102.03  247.08  217.0
    R245fa     427.16  36.51   0.3776  134.05  288.29  196.0
    R600a      407.81  36.48   0.1835  58.12   272.65  365.6
    R290       369.83  42.51   0.1521  44.10   230.85  425.9
    R1234yf    367.85  33.82   0.2760  114.04  243.65  178.0;

* Ideal gas heat capacity coefficients (Cp = A + B*T + C*T^2 + D*T^3)
Table cp_coeff(i,*)
                A       B           C           D
    R134a      88.25   0.1992      -1.92e-4    6.50e-8
    R245fa     106.9   0.2479      -1.43e-4    3.48e-8
    R600a      96.49   0.1967      -6.90e-5    1.01e-8
    R290       68.15   0.1836      -6.25e-5    7.33e-9
    R1234yf    90.23   0.2156      -1.67e-4    5.12e-8;

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
    rho(comp)   Density [kg per m3]
    
* Thermodynamic properties
    Z(comp)     Compressibility factor
    phi(comp)   Fugacity coefficient
    
* Binary variable for working fluid selection
    y(i)        Binary variable for working fluid selection
    
* Auxiliary variables for property calculations
    Tr(comp)    Reduced temperature
    Pr(comp)    Reduced pressure
    alpha(comp) Alpha parameter for PR EOS
    a(comp)     Attraction parameter
    b           Covolume parameter
    
* Saturation properties
    P_sat       Saturation pressure at condensing temperature [bar]
    T_sat_evap  Saturation temperature at evaporation pressure [K];

Binary Variables y;
Positive Variables W_net, W_turb, W_pump, Q_evap, Q_cond, m_wf, T, P, h, s, rho;
Variables Z, phi, Tr, Pr, alpha, a, b, P_sat, T_sat_evap;

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
    energy_bal_hw       Energy balance for hot water
    
* Process constraints
    pinch_point         Pinch point constraint in evaporator
    approach_temp       Approach temperature in condenser
    pressure_relation   Pressure relationship in cycle
    
* Peng-Robinson EOS constraints
    pr_eos(comp)        Peng-Robinson equation of state
    reduced_temp(comp)  Reduced temperature calculation
    reduced_press(comp) Reduced pressure calculation
    alpha_calc(comp)    Alpha parameter calculation
    attraction_param(comp) Attraction parameter calculation
    covolume_param      Covolume parameter calculation
    
* Saturation constraints
    sat_pressure        Saturation pressure at condensing temperature
    sat_temp_evap       Saturation temperature at evaporation pressure
    
* Property calculations
    enthalpy_calc(comp) Enthalpy calculation
    entropy_calc(comp)  Entropy calculation
    density_calc(comp)  Density calculation
    
* Performance constraints
    turbine_efficiency  Turbine isentropic efficiency
    pump_efficiency     Pump isentropic efficiency;

* Objective: Maximize net power output
obj.. W_net =e= eta_gen * W_turb - W_pump;

* Working fluid selection constraint
fluid_select.. sum(i, y(i)) =e= 1;

* Energy balances
energy_bal_evap.. Q_evap =e= m_wf * (h('1') - h('4'));
energy_bal_cond.. Q_cond =e= m_wf * (h('2') - h('3'));
energy_bal_turb.. W_turb =e= m_wf * (h('1') - h('2'));
energy_bal_pump.. W_pump =e= m_wf * (h('4') - h('3'));
energy_bal_hw.. Q_evap =e= m_hw * cp_hw * (T_hw_in - T_hw_out);

* Process constraints
pinch_point.. T('1') =l= T_hw_out + DT_pp;
approach_temp.. T('3') =g= T_cond + DT_approach;
pressure_relation.. P('1') =e= P('4');

* Peng-Robinson EOS implementation
pr_eos(comp).. P(comp) =e= R_gas * T(comp) / (1/rho(comp) - b) - 
                          a(comp) / (1/rho(comp)**2 + 2*b/rho(comp) - b**2);

reduced_temp(comp).. Tr(comp) =e= T(comp) / sum(i, y(i) * fluid_props(i,'Tc'));
reduced_press(comp).. Pr(comp) =e= P(comp) / sum(i, y(i) * fluid_props(i,'Pc'));

alpha_calc(comp).. alpha(comp) =e= (1 + sum(i, y(i) * (0.37464 + 1.54226*fluid_props(i,'omega') 
                                  - 0.26992*sqr(fluid_props(i,'omega')))) * (1 - sqrt(Tr(comp))))**2;

attraction_param(comp).. a(comp) =e= 0.45724 * sqr(R_gas) * sum(i, y(i) * sqr(fluid_props(i,'Tc'))) 
                                    * alpha(comp) / sum(i, y(i) * fluid_props(i,'Pc'));

covolume_param.. b =e= 0.07780 * R_gas * sum(i, y(i) * fluid_props(i,'Tc')) 
                      / sum(i, y(i) * fluid_props(i,'Pc'));

* Saturation properties (simplified Antoine equation)
sat_pressure.. P_sat =e= sum(i, y(i) * fluid_props(i,'Pc') * 
                         exp(7.0 * (1 - fluid_props(i,'Tc')/T_cond)));

* Simplified enthalpy calculations
enthalpy_calc('1').. h('1') =e= sum(i, y(i) * (cp_coeff(i,'A') * T('1') + 
                               0.5 * cp_coeff(i,'B') * sqr(T('1')))) / sum(i, y(i) * fluid_props(i,'Mw'));

enthalpy_calc('2').. h('2') =e= h('1') - W_turb/m_wf;
enthalpy_calc('3').. h('3') =e= sum(i, y(i) * fluid_props(i,'Hfg_298')) / sum(i, y(i) * fluid_props(i,'Mw'));
enthalpy_calc('4').. h('4') =e= h('3') + W_pump/m_wf;

* Simplified entropy calculations
entropy_calc(comp).. s(comp) =e= sum(i, y(i) * cp_coeff(i,'A') * log(T(comp))) / 
                                sum(i, y(i) * fluid_props(i,'Mw'));

* Density calculation
density_calc(comp).. rho(comp) =e= P(comp) * sum(i, y(i) * fluid_props(i,'Mw')) / 
                                  (Z(comp) * R_gas * T(comp));

* Efficiency constraints
turbine_efficiency.. h('2') =e= h('1') - eta_turb * (h('1') - h('2'));
pump_efficiency.. h('4') =e= h('3') + (h('4') - h('3')) / eta_pump;

* Variable bounds and initial values
T.lo('1') = 350; T.up('1') = 430;
T.lo('2') = 300; T.up('2') = 400;
T.fx('3') = T_cond;
T.lo('4') = 340; T.up('4') = 380;

P.lo(comp) = 0.5; P.up(comp) = 60.0;
P.fx('2') = P_sat;
P.fx('3') = P_sat;

h.lo(comp) = 0; h.up(comp) = 1000;
s.lo(comp) = 0; s.up(comp) = 10;
rho.lo(comp) = 1; rho.up(comp) = 2000;

m_wf.lo = 0.1; m_wf.up = 20.0;
Z.lo(comp) = 0.1; Z.up(comp) = 1.5;

* Initial values
T.l('1') = 410;
T.l('2') = 360;
T.l('3') = T_cond;
T.l('4') = 350;

P.l('1') = 15.0;
P.l('4') = 15.0;
P.l('2') = 5.0;
P.l('3') = 5.0;

h.l(comp) = 300;
s.l(comp) = 1.5;
rho.l(comp) = 100;
Z.l(comp) = 0.8;

m_wf.l = 2.0;
y.l(i) = 1/card(i);

Model orc_enhanced /all/;

* Solver options
option nlp = conopt;
option mip = cplex;
option minlp = dicopt;
option reslim = 3600;
option iterlim = 10000;

* Solve the optimization problem
solve orc_enhanced using minlp maximizing W_net;

* Display results
display W_net.l, W_turb.l, W_pump.l, Q_evap.l, Q_cond.l;
display T.l, P.l, h.l, s.l, rho.l;
display y.l;
display m_wf.l;

* Calculate performance metrics
parameters
    eta_cycle   Cycle thermal efficiency
    eta_exergy  Exergetic efficiency
    SFC         Specific fuel consumption;

eta_cycle = W_net.l / Q_evap.l;
eta_exergy = W_net.l / (Q_evap.l * (1 - 298.15/T_hw_in));
SFC = 3600 / W_net.l;

display eta_cycle, eta_exergy, SFC;

* Results summary
parameter results_summary(*);
results_summary('Net Power (kW)') = W_net.l;
results_summary('Thermal Efficiency (%)') = eta_cycle * 100;
results_summary('Mass Flow Rate (kg/s)') = m_wf.l;
results_summary('Evaporation Temperature (K)') = T.l('1');
results_summary('Evaporation Pressure (bar)') = P.l('1');

display results_summary;