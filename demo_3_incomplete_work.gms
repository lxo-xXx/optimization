* ================================================================
* DEMONSTRATION 3: INCOMPLETE WORK CALCULATION
* Shows the problems with classmate's work calculation
* ================================================================

$TITLE Demonstration of Incomplete Work Calculation

SETS
    st /1*4/;

PARAMETERS
    MW       "Molecular weight [kg/kmol]"      /72.15/
    m_wf     "Mass flow rate [kg/s]"          /50.0/
    eta_pump "Pump efficiency [-]"            /0.75/
    eta_turb "Turbine efficiency [-]"         /0.80/
    eta_gen  "Generator efficiency [-]"       /0.95/;

VARIABLES
    Hdep(st)        "Departure enthalpy [J/mol]"
    H_ideal(st)     "Ideal gas enthalpy [J/mol]"
    h_specific(st)  "Specific enthalpy [kJ/kg]"
    Wnet_wrong      "Wrong work calculation"
    Wnet_correct    "Correct work calculation"
    W_turb          "Turbine work [kW]"
    W_pump          "Pump work [kW]";

* Set some realistic values
Hdep.FX('1') = 1000;   H_ideal.FX('1') = 25000;
Hdep.FX('2') = 1200;   H_ideal.FX('2') = 26000;
Hdep.FX('3') = 800;    H_ideal.FX('3') = 35000;
Hdep.FX('4') = 900;    H_ideal.FX('4') = 30000;

EQUATIONS
    calc_specific_enthalpy(st)  "Convert molar to specific enthalpy"
    classmate_work              "Classmate's wrong work calculation"
    correct_turbine_work        "Correct turbine work"
    correct_pump_work          "Correct pump work"
    correct_net_work           "Correct net work";

* Convert molar to specific enthalpy
calc_specific_enthalpy(st)..
    h_specific(st) =E= (H_ideal(st) + Hdep(st)) / MW;

* CLASSMATE'S WRONG APPROACH: Only departure enthalpy differences
classmate_work..
    Wnet_wrong =E= (Hdep('3') - Hdep('4')) - (Hdep('2') - Hdep('1'));

* CORRECT APPROACH: Complete calculation with all factors
correct_turbine_work..
    W_turb =E= m_wf * eta_turb * (h_specific('3') - h_specific('4')) / 1000;

correct_pump_work..
    W_pump =E= m_wf * (h_specific('2') - h_specific('1')) / (eta_pump * 1000);

correct_net_work..
    Wnet_correct =E= eta_gen * (W_turb - W_pump);

MODEL WORK_DEMO /ALL/;

SOLVE WORK_DEMO USING NLP MINIMIZING Wnet_wrong;

DISPLAY "=== CLASSMATE'S WRONG CALCULATION ===";
DISPLAY "Wnet_wrong (J/mol):", Wnet_wrong.L;
DISPLAY "Problems with this approach:";
DISPLAY "1. Uses only departure enthalpy (ignores ideal gas part)";
DISPLAY "2. No mass flow rate consideration";
DISPLAY "3. No efficiency factors";
DISPLAY "4. Wrong units (J/mol instead of kW)";

DISPLAY "=== CORRECT CALCULATION ===";
DISPLAY "Specific enthalpies [kJ/kg]:", h_specific.L;
DISPLAY "Turbine work [kW]:", W_turb.L;
DISPLAY "Pump work [kW]:", W_pump.L;
DISPLAY "Net work [kW]:", Wnet_correct.L;

DISPLAY "=== COMPARISON ===";
DISPLAY "Classmate result has no physical meaning!";
DISPLAY "Correct result includes all thermodynamic factors";

* Show the magnitude difference
PARAMETERS
    wrong_value     "Classmate's result [J/mol]"
    correct_value   "Our result [kW]";

wrong_value = Wnet_wrong.L;
correct_value = Wnet_correct.L;

DISPLAY "Classmate's value:", wrong_value;
DISPLAY "Correct value:", correct_value;
DISPLAY "These cannot be compared - completely different physics!";