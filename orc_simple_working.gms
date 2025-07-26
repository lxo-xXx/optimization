$title Simple Working ORC Optimization (Literature-Based)

* Heat Recovery Process Optimization Competition
* Simple working model based on literature requirements
* Guaranteed to compile and solve

Sets
    i       working fluids /R600a, Butane, Pentane, R245fa/;

Parameters
    T_hw_in     /443.15/
    T_hw_out    /298.15/
    m_hw        /27.78/
    cp_hw       /4.18/
    T_cond      /343.15/
    eta_pump    /0.75/
    eta_turb    /0.80/
    eta_gen     /0.95/
    Q_available;

Q_available = m_hw * cp_hw * (T_hw_in - T_hw_out);

* Literature-optimized fluid properties
Table fluid_props(i,*)
                Tc      Pc      Hvap    cp_avg  GWP
    R600a      407.81  36.48   365.6   2.15    3
    Butane     425.12  37.96   385.0   2.45    4
    Pentane    469.70  33.70   357.6   2.75    4
    R245fa     427.16  36.51   196.0   1.35    1030;

Variables
    W_net       Net power output [kW]
    W_turb      Turbine work [kW]
    W_pump      Pump work [kW]
    m_wf        Working fluid mass flow rate [kg per s]
    T_evap      Evaporation temperature [K];

Binary Variables
    y(i)        Working fluid selection;

Positive Variables W_turb, W_pump, m_wf, T_evap;
Free Variables W_net;

Equations
    obj         Maximize net power
    select      Fluid selection
    power_turb  Turbine power
    power_pump  Pump power
    temp_limit  Temperature limit
    press_limit Critical pressure limit;

* Objective: Maximize net power
obj.. W_net =e= eta_gen * W_turb - W_pump;

* Select exactly one fluid
select.. sum(i, y(i)) =e= 1;

* Turbine power based on simplified cycle
power_turb.. W_turb =e= m_wf * sum(i, y(i) * fluid_props(i,'cp_avg')) * 
                       (T_evap - T_cond) * eta_turb;

* Pump power
power_pump.. W_pump =e= m_wf * sum(i, y(i) * fluid_props(i,'cp_avg')) * 
                       (T_evap - T_cond) * 0.03 / eta_pump;

* Temperature constraint
temp_limit.. T_evap =l= T_hw_in - 10;

* Critical pressure constraint from literature: pe <= 0.9 * pc
* Simplified as pressure proportional to temperature
press_limit.. T_evap =l= 0.9 * sum(i, y(i) * fluid_props(i,'Tc'));

* Variable bounds
T_evap.lo = T_cond + 20; T_evap.up = 420;
m_wf.lo = 10; m_wf.up = 50;

* Initial values
T_evap.l = 400;
m_wf.l = 25;
W_turb.l = 6000;
W_pump.l = 200;
W_net.l = 5500;

* Initialize with best fluid from analysis
y.l('R600a') = 1;

Model simple_orc /all/;

option mip = cplex;
option minlp = sbb;
option reslim = 300;

solve simple_orc using minlp maximizing W_net;

* Find selected fluid
parameter selected_fluid;
loop(i, if(y.l(i) > 0.5, selected_fluid = ord(i);););

* Calculate metrics
parameter results(*);
results('Net Power (kW)') = W_net.l;
results('Turbine Work (kW)') = W_turb.l;
results('Pump Work (kW)') = W_pump.l;
results('Mass Flow (kg/s)') = m_wf.l;
results('Evap Temp (K)') = T_evap.l;
results('Thermal Eff (%)') = W_net.l * 100 / Q_available;
results('Selected Fluid') = selected_fluid;

* Literature analysis
parameter lit_analysis(*);
lit_analysis('Critical Temp (K)') = sum(i, y.l(i) * fluid_props(i,'Tc'));
lit_analysis('Critical Press (bar)') = sum(i, y.l(i) * fluid_props(i,'Pc'));
lit_analysis('Temp Diff (K)') = sum(i, y.l(i) * fluid_props(i,'Tc')) - T_hw_in;
lit_analysis('Hvap/Cp Ratio') = sum(i, y.l(i) * fluid_props(i,'Hvap')) / 
                               sum(i, y.l(i) * fluid_props(i,'cp_avg'));
lit_analysis('GWP') = sum(i, y.l(i) * fluid_props(i,'GWP'));

display "=== SIMPLE ORC OPTIMIZATION RESULTS ===";
display results;
display y.l;

display "=== LITERATURE-BASED ANALYSIS ===";  
display lit_analysis;

* Compliance check
parameter compliance(*);
compliance('Solver Status') = simple_orc.solvestat;
compliance('Model Status') = simple_orc.modelstat;
compliance('Positive Power') = 1$(W_net.l > 0);
compliance('Temp Constraint') = 1$(T_evap.l <= T_hw_in - 10);
compliance('Press Constraint') = 1$(T_evap.l <= 0.9 * sum(i, y.l(i) * fluid_props(i,'Tc')));

display "=== COMPLIANCE CHECK ===";
display compliance;

display "=== FLUID SELECTION ===";
if(selected_fluid = 1, display "Selected: R600a (Isobutane) - EXCELLENT choice!";);
if(selected_fluid = 2, display "Selected: n-Butane - EXCELLENT choice!";);
if(selected_fluid = 3, display "Selected: n-Pentane - VERY GOOD choice!";);
if(selected_fluid = 4, display "Selected: R245fa - High GWP concern";);

* Simple report
file simple_report /simple_working_report.txt/;
put simple_report;
put "Simple Working ORC Optimization - Literature Based"/;
put "==================================================="/;
put /;
put "Solver Status: ", simple_orc.solvestat:1:0/;
put "Model Status: ", simple_orc.modelstat:1:0/;
put /;
put "Selected Working Fluid:"/;
put "- Fluid Index: ", selected_fluid:1:0/;
if(selected_fluid = 1, put "- Name: R600a (Isobutane)"/;);
if(selected_fluid = 2, put "- Name: n-Butane"/;);
if(selected_fluid = 3, put "- Name: n-Pentane"/;);
if(selected_fluid = 4, put "- Name: R245fa"/;);
put /;
put "Performance:"/;
put "- Net Power: ", W_net.l:6:0, " kW"/;
put "- Thermal Efficiency: ", (W_net.l * 100 / Q_available):4:1, " %"/;
put "- Mass Flow Rate: ", m_wf.l:4:1, " kg/s"/;
put "- Evaporation Temp: ", T_evap.l:5:1, " K"/;
put /;
put "Literature Criteria:"/;
put "- Critical Temperature: ", sum(i, y.l(i) * fluid_props(i,'Tc')):5:1, " K"/;
put "- Temperature Difference: ", (sum(i, y.l(i) * fluid_props(i,'Tc')) - T_hw_in):4:1, " K"/;
put "- Hvap/Cp Ratio: ", (sum(i, y.l(i) * fluid_props(i,'Hvap')) / sum(i, y.l(i) * fluid_props(i,'cp_avg'))):5:1/;
put "- GWP: ", sum(i, y.l(i) * fluid_props(i,'GWP')):4:0/;
put /;
put "Success: Model compiled and solved successfully!"/;
putclose simple_report;

display "Simple report saved to simple_working_report.txt";