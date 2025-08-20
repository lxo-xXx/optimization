* ================================================================
* DEMONSTRATION 4: MISSING ENERGY BALANCES
* Shows why energy balances are critical for ORC modeling
* ================================================================

$TITLE Demonstration of Missing Energy Balances

SETS
    st /1*4/;

PARAMETERS
    m_wf        "Working fluid mass flow [kg/s]"     /50.0/
    m_hw        "Hot water mass flow [kg/s]"         /100.0/
    T_hw_in     "Hot water inlet temperature [K]"    /443.15/
    T_hw_out    "Hot water outlet temperature [K]"   /343.15/
    Cp_water    "Water specific heat [kJ/(kg*K)]"    /4.18/;

VARIABLES
    h(st)       "Specific enthalpy [kJ/kg]"
    Q_evap      "Evaporator heat [kW]"
    Q_cond      "Condenser heat [kW]"
    Q_available "Available heat from hot water [kW]"
    W_turb      "Turbine work [kW]"
    W_pump      "Pump work [kW]"
    W_net       "Net work [kW]"
    energy_balance_error "Energy balance violation";

* Set realistic enthalpy values for ORC cycle
h.FX('1') = 200;  * Saturated liquid from condenser
h.FX('2') = 210;  * Compressed liquid from pump  
h.FX('3') = 450;  * Superheated vapor from evaporator
h.FX('4') = 280;  * Wet vapor from turbine

EQUATIONS
    * MISSING IN CLASSMATE'S MODEL:
    evaporator_balance     "Q_evap = m_wf * (h3 - h2)"
    condenser_balance      "Q_cond = m_wf * (h4 - h1)"
    turbine_work_balance   "W_turb = m_wf * (h3 - h4)"
    pump_work_balance      "W_pump = m_wf * (h2 - h1)"
    net_work_balance       "W_net = W_turb - W_pump"
    
    * Heat source constraint (MISSING IN CLASSMATE'S MODEL):
    heat_source_limit      "Q_evap <= Q_available"
    
    * Energy conservation (MISSING IN CLASSMATE'S MODEL):
    overall_energy_balance "Q_evap = W_net + Q_cond";

* Calculate available heat from hot water
Q_available.FX = m_hw * Cp_water * (T_hw_in - T_hw_out);

* Energy balance equations
evaporator_balance..
    Q_evap =E= m_wf * (h('3') - h('2'));

condenser_balance..
    Q_cond =E= m_wf * (h('4') - h('1'));

turbine_work_balance..
    W_turb =E= m_wf * (h('3') - h('4'));

pump_work_balance..
    W_pump =E= m_wf * (h('2') - h('1'));

net_work_balance..
    W_net =E= W_turb - W_pump;

heat_source_limit..
    Q_evap =L= Q_available;

overall_energy_balance..
    energy_balance_error =E= Q_evap - W_net - Q_cond;

* Bounds
Q_evap.LO = 0; Q_evap.UP = 50000;
Q_cond.LO = 0; Q_cond.UP = 50000;
W_turb.LO = 0; W_turb.UP = 20000;
W_pump.LO = 0; W_pump.UP = 5000;
W_net.LO = 0;  W_net.UP = 15000;

MODEL ENERGY_DEMO /ALL/;

SOLVE ENERGY_DEMO USING NLP MINIMIZING energy_balance_error;

DISPLAY "=== AVAILABLE HEAT SOURCE ===";
DISPLAY "Hot water provides [kW]:", Q_available.L;

DISPLAY "=== ENERGY BALANCE RESULTS ===";
DISPLAY "Evaporator heat [kW]:", Q_evap.L;
DISPLAY "Condenser heat [kW]:", Q_cond.L;
DISPLAY "Turbine work [kW]:", W_turb.L;
DISPLAY "Pump work [kW]:", W_pump.L;
DISPLAY "Net work [kW]:", W_net.L;

DISPLAY "=== ENERGY CONSERVATION CHECK ===";
DISPLAY "Energy balance error [kW]:", energy_balance_error.L;
DISPLAY "Should be near zero for conservation";

DISPLAY "=== WHAT CLASSMATE'S MODEL MISSES ===";
DISPLAY "1. No evaporator energy balance";
DISPLAY "2. No condenser energy balance";
DISPLAY "3. No heat source constraints";
DISPLAY "4. No energy conservation validation";
DISPLAY "5. Cannot verify thermodynamic consistency";

* Show energy flow analysis
PARAMETERS
    heat_input      "Heat input [kW]"
    heat_output     "Heat output [kW]"
    work_output     "Work output [kW]"
    efficiency      "Thermal efficiency [%]";

heat_input = Q_evap.L;
heat_output = Q_cond.L;
work_output = W_net.L;
efficiency = (work_output / heat_input) * 100;

DISPLAY "=== ENERGY FLOW ANALYSIS ===";
DISPLAY "Heat IN (evaporator):", heat_input;
DISPLAY "Work OUT (net):", work_output;
DISPLAY "Heat OUT (condenser):", heat_output;
DISPLAY "Thermal efficiency [%]:", efficiency;

DISPLAY "=== WHY THIS MATTERS ===";
DISPLAY "Without energy balances, the model:";
DISPLAY "- Cannot validate thermodynamic consistency";
DISPLAY "- Cannot optimize heat exchanger sizing";
DISPLAY "- Cannot ensure realistic operating conditions";
DISPLAY "- Cannot comply with competition constraints";
DISPLAY "- Produces meaningless results";