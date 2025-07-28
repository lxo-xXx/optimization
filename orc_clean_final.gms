$title Heat Recovery Process Optimization - Clean Final Solution

Sets
    i       working fluids /R134a, R245fa, R600a, R290, R1234yf/
    comp    components /1*4/;

Scalars
    T_hw_in     Hot water inlet temperature [K] /443.15/
    T_hw_out    Hot water outlet temperature [K] /343.15/
    m_hw        Hot water mass flow rate [kg per s] /100.0/
    T_ambient   Ambient air temperature [K] /298.15/
    T_cond      Condensing temperature [K] /333.15/
    DT_pinch    Pinch point temperature difference [K] /10.0/
    DT_approach Approach temperature difference [K] /5.0/
    eta_turb    Turbine isentropic efficiency /0.80/
    eta_pump    Pump isentropic efficiency /0.75/
    eta_gen     Generator efficiency /0.95/;

Table fluid_props(i,*) Working fluid properties
                Tc      Pc      omega   Mw      Hvap    cp_avg  GWP
    R134a      374.21  40.59   0.3268  102.03  217.0   1.25    1430
    R245fa     427.16  36.51   0.3776  134.05  196.7   1.35    1030
    R600a      407.81  36.48   0.1835  58.12   365.6   2.15    3
    R290       369.89  42.51   0.1521  44.10   425.2   2.25    3
    R1234yf    367.85  33.82   0.276   114.04  178.3   1.45    4;

Variables
    W_net       Net power output [kW]
    Q_evap      Heat input to evaporator [kW]
    m_wf        Working fluid mass flow rate [kg per s]
    T(comp)     Temperature at each state point [K]
    P(comp)     Pressure at each state point [bar]
    h(comp)     Specific enthalpy [kJ per kg]
    Tr_eff      Effective reduced temperature
    alpha_eff   Effective alpha parameter;

Binary Variables
    y(i)        Working fluid selection;

W_net.lo = 0; W_net.up = 50000;
Q_evap.lo = 10000; Q_evap.up = 50000;
m_wf.lo = 50; m_wf.up = 150;

T.lo('1') = 400; T.up('1') = 433;
T.lo('2') = 350; T.up('2') = 420;
T.lo('3') = T_cond + DT_approach; T.up('3') = T_cond + DT_approach + 5;
T.lo('4') = T_cond + DT_approach; T.up('4') = 370;

P.lo('1') = 15; P.up('1') = 35;
P.lo('2') = 8; P.up('2') = 25;
P.lo('3') = 8; P.up('3') = 25;
P.lo('4') = 15; P.up('4') = 35;

h.lo(comp) = 200; h.up(comp) = 900;
Tr_eff.lo = 0.8; Tr_eff.up = 1.0;
alpha_eff.lo = 0.95; alpha_eff.up = 1.1;

Equations
    obj                 Maximize net power output
    fluid_select        Only one working fluid can be selected
    critical_limit      Critical pressure constraint
    energy_bal_evap     Energy balance for evaporator
    energy_bal_turb     Energy balance for turbine
    energy_bal_hw       Energy balance for hot water
    pinch_point         Pinch point constraint
    approach_temp       Approach temperature constraint
    reduced_temp        Reduced temperature calculation
    alpha_pr            PR alpha function
    enthalpy_calc       Simplified enthalpy calculation;

obj.. W_net =e= eta_gen * m_wf * (h('1') - h('2'));

fluid_select.. sum(i, y(i)) =e= 1;

critical_limit.. P('1') =l= 0.7 * sum(i, y(i) * fluid_props(i,'Pc'));

energy_bal_evap.. Q_evap =e= m_wf * (h('1') - h('4'));
energy_bal_turb.. h('2') =e= h('1') - eta_turb * (h('1') - h('3'));
energy_bal_hw.. Q_evap =e= m_hw * 4.18 * (T_hw_in - T_hw_out);

pinch_point.. T('1') =l= T_hw_in - DT_pinch;
approach_temp.. T('3') =g= T_cond + DT_approach;

reduced_temp.. Tr_eff =e= sum(i, y(i) * T('1') / fluid_props(i,'Tc'));
alpha_pr.. alpha_eff =e= 1.0 + 0.05 * (1 - Tr_eff) * sum(i, y(i) * fluid_props(i,'omega'));

enthalpy_calc(comp).. h(comp) =e= 
    sum(i, y(i) * fluid_props(i,'cp_avg') * T(comp)) +
    sum(i, y(i) * fluid_props(i,'Hvap')) * 0.6$(ord(comp) <= 2) +
    20 * alpha_eff * (T(comp) - 350) / 100;

T.l('1') = 425;
T.l('2') = 375;
T.l('3') = T_cond + DT_approach;
T.l('4') = T_cond + DT_approach + 2;

P.l('1') = 25;
P.l('2') = 15;
P.l('3') = 15;
P.l('4') = 25;

h.l('1') = 700;
h.l('2') = 550;
h.l('3') = 400;
h.l('4') = 410;

m_wf.l = 100;
Tr_eff.l = 0.9;
alpha_eff.l = 1.02;
y.l('R600a') = 1;

Model orc_clean_final /all/;

option minlp = dicopt;
option nlp = conopt;

Solve orc_clean_final using minlp maximizing W_net;

display W_net.l, Q_evap.l, m_wf.l;
display T.l, P.l, h.l;
display Tr_eff.l, alpha_eff.l;
display y.l;

Parameter results(*);
results('Net Power (kW)') = W_net.l;
results('Thermal Efficiency (%)') = W_net.l / Q_evap.l * 100;
results('Mass Flow Rate (kg/s)') = m_wf.l;
results('Evap Temperature (K)') = T.l('1');
results('Evap Pressure (bar)') = P.l('1');
results('Available Heat (kW)') = Q_evap.l;

display results;

Parameter status(*);
status('Solver Status') = orc_clean_final.solvestat;
status('Model Status') = orc_clean_final.modelstat;

display status;

if(orc_clean_final.modelstat = 1,
    display "OPTIMAL SOLUTION ACHIEVED";
elseif orc_clean_final.modelstat = 2,
    display "LOCAL OPTIMUM FOUND";
else
    display "CHECK MODEL STATUS";
);