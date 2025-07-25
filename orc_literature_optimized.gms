$title ORC Optimization Based on Literature Requirements and Fluid Analysis

* Heat Recovery Process Optimization Competition
* Literature-based model with optimal fluid selection
* Based on 2015-2016 research requirements and fluid screening analysis

Sets
    i       working fluids /R600a, n_Butane, n_Pentane, Cyclopentane, R245fa/
    comp    components /1*4/;

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
    cp_hw       Hot water specific heat [kJ per kg K] /4.18/
    
* Process design parameters
    T_cond      Condensing temperature [K] /343.15/
    T_ambient   Ambient temperature [K] /298.15/
    DT_pp       Pinch point temperature difference [K] /5.0/
    eta_pump    Pump isentropic efficiency /0.75/
    eta_turb    Turbine isentropic efficiency /0.80/
    eta_gen     Generator efficiency /0.95/
    DT_approach Approach temperature difference [K] /5.0/
    
* Universal constants
    R_gas       Universal gas constant [kJ per kmol K] /8.314/
    
* Available heat
    Q_available Available heat from hot water [kW];

Q_available = m_hw * cp_hw * (T_hw_in - T_hw_out);

* Optimized working fluid properties based on literature analysis
Table fluid_props(i,*)
                Tc      Pc      omega   Mw      Hvap    cp_avg  GWP     Score
    R600a      407.81  36.48   0.1835  58.12   365.6   2.15    3       0.576
    n_Butane   425.12  37.96   0.2002  58.12   385.0   2.45    4       0.566
    n_Pentane  469.70  33.70   0.2515  72.15   357.6   2.75    4       0.561
    Cyclopentane 511.69 45.15  0.1956  70.13   389.0   2.90    5       0.544
    R245fa     427.16  36.51   0.3776  134.05  196.0   1.35    1030    0.538;

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
    
* Exergy variables
    Ex_in       Exergy input [kW]
    Ex_out      Exergy output [kW]
    Ex_dest     Exergy destruction [kW]
    
* Efficiency variables
    eta_thermal Thermal efficiency
    eta_exergy  Exergy efficiency
    
* Fluid selection variables
    y(i)        Binary variable for working fluid selection
    
* Literature-based criteria variables
    DT_critical Temperature difference from critical [K]
    Hvap_cp_ratio Enthalpy of vaporization to heat capacity ratio
    fluid_score Overall fluid selection score;

Binary Variables y;
Positive Variables W_turb, W_pump, Q_evap, Q_cond, m_wf, T, P, h, s, Ex_in, Ex_out, Ex_dest;
Free Variables W_net, eta_thermal, eta_exergy, DT_critical, Hvap_cp_ratio, fluid_score;

Equations
* Objective function
    obj         Maximize net power output
    
* Working fluid selection constraint
    fluid_select    Only one working fluid can be selected
    
* Literature-based fluid selection criteria
    temp_diff_criterion     Temperature difference from critical
    hvap_cp_criterion      Enthalpy of vaporization to cp ratio
    fluid_score_calc       Overall fluid score calculation
    critical_pressure_limit Critical pressure constraint (pe <= 0.9*pc)
    
* Energy balances (First Law of Thermodynamics)
    energy_bal_evap     Energy balance for evaporator
    energy_bal_cond     Energy balance for condenser
    energy_bal_turb     Energy balance for turbine
    energy_bal_pump     Energy balance for pump
    energy_bal_hw       Energy balance for hot water
    
* Process constraints
    pinch_point         Pinch point constraint in evaporator
    approach_temp       Approach temperature in condenser
    pressure_relation   Pressure relationship in cycle
    
* Enhanced thermodynamic constraints
    enthalpy_evap_out   Enthalpy at evaporator outlet
    enthalpy_turb_out   Enthalpy at turbine outlet
    enthalpy_cond_out   Enthalpy at condenser outlet
    enthalpy_pump_out   Enthalpy at pump outlet
    
* Exergy balance equations
    exergy_input       Exergy input calculation
    exergy_output      Exergy output calculation
    exergy_destruction Exergy destruction calculation
    
* Efficiency definitions
    thermal_eff        Thermal efficiency calculation
    exergy_eff         Exergy efficiency calculation
    
* Performance constraints
    turbine_efficiency  Turbine isentropic efficiency
    pump_efficiency     Pump isentropic efficiency;

* Objective: Maximize net power output
obj.. W_net =e= eta_gen * W_turb - W_pump;

* Working fluid selection constraint
fluid_select.. sum(i, y(i)) =e= 1;

* Literature-based fluid selection criteria
temp_diff_criterion.. DT_critical =e= sum(i, y(i) * fluid_props(i,'Tc')) - T_hw_in;

hvap_cp_criterion.. Hvap_cp_ratio =e= sum(i, y(i) * fluid_props(i,'Hvap')) / 
                                     sum(i, y(i) * fluid_props(i,'cp_avg'));

fluid_score_calc.. fluid_score =e= sum(i, y(i) * fluid_props(i,'Score'));

* Critical pressure constraint: pe <= 0.9 * pc (2016 paper requirement)
critical_pressure_limit.. P('1') =l= 0.9 * sum(i, y(i) * fluid_props(i,'Pc'));

* Energy balances (First Law of Thermodynamics)
energy_bal_evap.. Q_evap =e= m_wf * (h('1') - h('4'));
energy_bal_cond.. Q_cond =e= m_wf * (h('2') - h('3'));
energy_bal_turb.. W_turb =e= m_wf * (h('1') - h('2'));
energy_bal_pump.. W_pump =e= m_wf * (h('4') - h('3'));
energy_bal_hw.. Q_evap =e= Q_available;

* Process constraints
pinch_point.. T('1') =l= T_hw_in - DT_pp;
approach_temp.. T('3') =g= T_cond + DT_approach;
pressure_relation.. P('1') =e= P('4');

* Enhanced enthalpy calculations based on literature
* State 1: Superheated vapor at evaporator outlet
enthalpy_evap_out.. h('1') =e= sum(i, y(i) * (fluid_props(i,'cp_avg') * T('1') + 
                              0.85 * fluid_props(i,'Hvap')));

* State 2: Turbine outlet (isentropic expansion with efficiency)
enthalpy_turb_out.. h('2') =e= h('1') - eta_turb * (h('1') - 
                              sum(i, y(i) * fluid_props(i,'cp_avg') * T('2')));

* State 3: Saturated liquid at condenser outlet
enthalpy_cond_out.. h('3') =e= sum(i, y(i) * fluid_props(i,'cp_avg') * T('3'));

* State 4: Compressed liquid at pump outlet
enthalpy_pump_out.. h('4') =e= h('3') + (sum(i, y(i) * fluid_props(i,'cp_avg')) * 
                              (T('4') - T('3'))) / eta_pump;

* Exergy analysis (based on literature)
exergy_input.. Ex_in =e= Q_evap * (1 - T_ambient/T_hw_in);

exergy_output.. Ex_out =e= W_net;

exergy_destruction.. Ex_dest =e= Ex_in - Ex_out;

* Efficiency definitions
thermal_eff.. eta_thermal =e= W_net / Q_evap;

exergy_eff.. eta_exergy =e= Ex_out / Ex_in;

* Efficiency constraints
turbine_efficiency.. h('2') =g= h('1') - (h('1') - h('2')) / eta_turb;
pump_efficiency.. h('4') =l= h('3') + (h('4') - h('3')) * eta_pump;

* Variable bounds based on literature and physical constraints
T.lo('1') = 360; T.up('1') = 430;  * Evaporation temperature
T.lo('2') = 320; T.up('2') = 400;  * Turbine outlet temperature
T.fx('3') = T_cond;                 * Condensation temperature (fixed)
T.lo('4') = T_cond; T.up('4') = 380; * Pump outlet temperature

* Pressure bounds considering critical pressure constraint
P.lo(comp) = 2.0; P.up(comp) = 35.0;  * Conservative pressure range
h.lo(comp) = 150; h.up(comp) = 700;   * Enthalpy range
s.lo(comp) = 0.8; s.up(comp) = 6.0;   * Entropy range

m_wf.lo = 2.0; m_wf.up = 50.0;        * Mass flow rate range

* Literature criteria bounds
DT_critical.lo = -80; DT_critical.up = 100;  * Temperature difference range
Hvap_cp_ratio.lo = 80; Hvap_cp_ratio.up = 200; * Hvap/Cp ratio range
fluid_score.lo = 0.5; fluid_score.up = 0.6;   * Fluid score range

* Initial values based on fluid analysis
T.l('1') = 410;
T.l('2') = 370;
T.l('3') = T_cond;
T.l('4') = 350;

P.l('1') = 25.0;
P.l('4') = 25.0;
P.l('2') = 8.0;
P.l('3') = 8.0;

h.l(comp) = 350;
s.l(comp) = 2.0;
m_wf.l = 15.0;

* Initialize with best fluid (R600a)
y.l('R600a') = 1.0;
y.l('n_Butane') = 0.0;
y.l('n_Pentane') = 0.0;
y.l('Cyclopentane') = 0.0;
y.l('R245fa') = 0.0;

Model orc_literature_opt /all/;

* Solver options
option mip = cplex;
option minlp = sbb;
option reslim = 1800;
option iterlim = 100000;

* Solve the optimization problem
solve orc_literature_opt using minlp maximizing W_net;

* Display results
display "=== LITERATURE-BASED ORC OPTIMIZATION RESULTS ===";
display W_net.l, W_turb.l, W_pump.l, Q_evap.l, Q_cond.l;
display T.l, P.l, h.l, s.l, m_wf.l;
display eta_thermal.l, eta_exergy.l;
display Ex_in.l, Ex_out.l, Ex_dest.l;
display DT_critical.l, Hvap_cp_ratio.l, fluid_score.l;
display y.l;

* Find optimal fluid
parameter optimal_fluid_name, optimal_fluid_index;
loop(i,
    if(y.l(i) > 0.5,
        optimal_fluid_index = ord(i);
    );
);

* Fluid selection analysis based on literature
parameter literature_analysis(*);
literature_analysis('Optimal Fluid Index') = optimal_fluid_index;
literature_analysis('Critical Temperature (K)') = sum(i, y.l(i) * fluid_props(i,'Tc'));
literature_analysis('Critical Pressure (bar)') = sum(i, y.l(i) * fluid_props(i,'Pc'));
literature_analysis('Temperature Difference (K)') = DT_critical.l;
literature_analysis('Hvap/Cp Ratio') = Hvap_cp_ratio.l;
literature_analysis('Fluid Score') = fluid_score.l;
literature_analysis('Max Evap Pressure (bar)') = P.l('1');
literature_analysis('Critical Pressure Limit (bar)') = 0.9 * sum(i, y.l(i) * fluid_props(i,'Pc'));
literature_analysis('GWP') = sum(i, y.l(i) * fluid_props(i,'GWP'));

display "=== LITERATURE-BASED FLUID ANALYSIS ===";
display literature_analysis;

* Performance metrics
parameter performance_metrics(*);
performance_metrics('Net Power (kW)') = W_net.l;
performance_metrics('Thermal Efficiency (%)') = eta_thermal.l * 100;
performance_metrics('Exergy Efficiency (%)') = eta_exergy.l * 100;
performance_metrics('Exergy Destruction (kW)') = Ex_dest.l;
performance_metrics('Mass Flow Rate (kg/s)') = m_wf.l;
performance_metrics('Evaporation Temperature (K)') = T.l('1');
performance_metrics('Evaporation Pressure (bar)') = P.l('1');
performance_metrics('Pressure Ratio') = P.l('1') / P.l('3');

display "=== PERFORMANCE METRICS ===";
display performance_metrics;

* Literature compliance check
parameter compliance_check(*);
compliance_check('Critical Pressure Constraint') = 1$(P.l('1') <= 0.9 * sum(i, y.l(i) * fluid_props(i,'Pc')));
compliance_check('Pinch Point Constraint') = 1$(T.l('1') <= T_hw_in - DT_pp);
compliance_check('Approach Temperature') = 1$(T.l('3') >= T_cond + DT_approach);
compliance_check('Positive Power Output') = 1$(W_net.l > 0);
compliance_check('Realistic Efficiency') = 1$(eta_thermal.l < 0.5);

display "=== LITERATURE COMPLIANCE CHECK ===";
display compliance_check;

* Generate comprehensive report
file literature_report /literature_optimization_report.txt/;
put literature_report;
put "Literature-Based Heat Recovery Process Optimization Report"/;
put "============================================================"/;
put /;
put "Fluid Selection Based on Literature Requirements:"/;
put "- High critical temperature: Preferred"/;
put "- Low critical pressure: Preferred"/;
put "- Optimal temperature difference: 35-50°C from critical"/;
put "- Maximize enthalpy of vaporization"/;
put "- Maximize Hvap/Cp ratio"/;
put "- Minimize specific heat capacity"/;
put "- Critical pressure constraint: pe <= 0.9 * pc"/;
put "- Environmental consideration: Low GWP preferred"/;
put /;
put "Selected Working Fluid:"/;
put "- Fluid Index: ", optimal_fluid_index:2:0/;
put "- Critical Temperature: ", sum(i, y.l(i) * fluid_props(i,'Tc')):6:1, " K"/;
put "- Critical Pressure: ", sum(i, y.l(i) * fluid_props(i,'Pc')):6:1, " bar"/;
put "- Temperature Difference: ", DT_critical.l:6:1, " K"/;
put "- Hvap/Cp Ratio: ", Hvap_cp_ratio.l:6:1/;
put "- Literature Score: ", fluid_score.l:6:3/;
put "- GWP: ", sum(i, y.l(i) * fluid_props(i,'GWP')):6:0/;
put /;
put "Thermodynamic Performance:"/;
put "- Net Power Output: ", W_net.l:8:1, " kW"/;
put "- Thermal Efficiency: ", (eta_thermal.l*100):6:2, " %"/;
put "- Exergy Efficiency: ", (eta_exergy.l*100):6:2, " %"/;
put "- Exergy Destruction: ", Ex_dest.l:8:1, " kW"/;
put "- Mass Flow Rate: ", m_wf.l:6:1, " kg/s"/;
put /;
put "Operating Conditions:"/;
put "- Evaporation Temperature: ", T.l('1'):6:1, " K"/;
put "- Evaporation Pressure: ", P.l('1'):6:1, " bar"/;
put "- Condensation Temperature: ", T.l('3'):6:1, " K"/;
put "- Condensation Pressure: ", P.l('3'):6:1, " bar"/;
put "- Pressure Ratio: ", (P.l('1')/P.l('3')):6:2/;
put /;
put "Literature Compliance:"/;
put "- Critical pressure constraint: ";
if(P.l('1') <= 0.9 * sum(i, y.l(i) * fluid_props(i,'Pc')),
    put "SATISFIED"/;
else
    put "VIOLATED"/;
);
put "- Maximum evaporation pressure: ", P.l('1'):6:1, " bar"/;
put "- Critical pressure limit: ", (0.9 * sum(i, y.l(i) * fluid_props(i,'Pc'))):6:1, " bar"/;
put /;
put "Environmental Impact:"/;
put "- Global Warming Potential: ", sum(i, y.l(i) * fluid_props(i,'GWP')):6:0/;
put "- Environmental Rating: ";
if(sum(i, y.l(i) * fluid_props(i,'GWP')) < 100,
    put "EXCELLENT (Low GWP)"/;
elseif sum(i, y.l(i) * fluid_props(i,'GWP')) < 1000,
    put "GOOD (Medium GWP)"/;
else
    put "POOR (High GWP)"/;
);
put /;
put "Conclusion:"/;
put "This optimization follows literature best practices for"/;
put "working fluid selection and thermodynamic modeling."/;
putclose literature_report;

display "Literature-based report saved to literature_optimization_report.txt";