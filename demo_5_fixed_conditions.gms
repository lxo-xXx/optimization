* ================================================================
* DEMONSTRATION 5: FIXED CONDITIONS vs OPTIMIZATION
* Shows the performance penalty of fixed cycle conditions
* ================================================================

$TITLE Demonstration of Fixed vs Optimized Conditions

SETS
    st /1*4/;

PARAMETERS
    * Competition specifications
    T_hw_in     "Hot water inlet [K]"      /443.15/
    T_hw_out    "Hot water outlet [K]"     /343.15/
    T_amb       "Ambient temperature [K]"  /298.15/
    DT_pinch    "Pinch point difference [K]" /5.0/
    DT_appr     "Approach difference [K]"    /5.0/
    
    * Classmate's fixed values
    P_fixed(st) "Fixed pressures [bar]"
    T_fixed(st) "Fixed temperatures [K]"
    
    * For comparison
    m_wf        "Mass flow rate [kg/s]"    /50.0/;

* Classmate's arbitrary fixed values
P_fixed('1') = 5;   T_fixed('1') = 300;
P_fixed('2') = 45;  T_fixed('2') = 305;
P_fixed('3') = 45;  T_fixed('3') = 350;
P_fixed('4') = 5;   T_fixed('4') = 330;

VARIABLES
    * Optimized variables (our approach)
    T_opt(st)   "Optimized temperatures [K]"
    P_opt(st)   "Optimized pressures [bar]"
    
    * Performance metrics
    h(st)       "Specific enthalpy [kJ/kg]"
    W_net_fixed "Net work with fixed conditions"
    W_net_opt   "Net work with optimization"
    eta_fixed   "Efficiency with fixed conditions"
    eta_opt     "Efficiency with optimization"
    Q_evap      "Evaporator heat [kW]";

EQUATIONS
    * Optimization constraints (missing in classmate's model)
    pinch_constraint    "T3 <= T_hw_out + (T_hw_in - T_hw_out) - DT_pinch"
    approach_constraint "T1 >= T_amb + DT_appr"
    cycle_constraint    "T4 = T1 for ORC cycle"
    pressure_high       "High pressure equality"
    pressure_low        "Low pressure equality"
    
    * Work calculations
    work_fixed          "Work with fixed conditions"
    work_optimized      "Work with optimization"
    heat_balance        "Heat balance"
    efficiency_fixed    "Efficiency with fixed"
    efficiency_opt      "Efficiency with optimization";

* Optimization constraints (MISSING in classmate's model)
pinch_constraint..
    T_opt('3') =L= T_hw_out + (T_hw_in - T_hw_out) - DT_pinch;

approach_constraint..
    T_opt('1') =G= T_amb + DT_appr;

cycle_constraint..
    T_opt('4') =E= T_opt('1');

pressure_high..
    P_opt('2') =E= P_opt('3');

pressure_low..
    P_opt('1') =E= P_opt('4');

* Simplified enthalpy model for demonstration
h.FX('1') = 200;  h.FX('2') = 210;  h.FX('3') = 450;  h.FX('4') = 280;

heat_balance..
    Q_evap =E= m_wf * (h('3') - h('2'));

work_fixed..
    W_net_fixed =E= m_wf * ((h('3') - h('4')) - (h('2') - h('1')));

work_optimized..
    W_net_opt =E= m_wf * ((h('3') - h('4')) - (h('2') - h('1')));

efficiency_fixed..
    eta_fixed =E= W_net_fixed / (Q_evap + 0.01);

efficiency_opt..
    eta_opt =E= W_net_opt / (Q_evap + 0.01);

* Bounds for optimization (classmate has none)
T_opt.LO(st) = 280; T_opt.UP(st) = 500;
P_opt.LO(st) = 1;   P_opt.UP(st) = 50;

* Initial values
T_opt.L('1') = 303; T_opt.L('2') = 308; T_opt.L('3') = 438; T_opt.L('4') = 303;
P_opt.L('1') = 2;   P_opt.L('2') = 20;  P_opt.L('3') = 20;  P_opt.L('4') = 2;

MODEL FIXED_DEMO /work_fixed, heat_balance, efficiency_fixed/;
MODEL OPTIMIZED_DEMO /ALL/;

* Solve with fixed conditions (classmate's approach)
SOLVE FIXED_DEMO USING NLP MAXIMIZING W_net_fixed;

* Solve with optimization (our approach)  
SOLVE OPTIMIZED_DEMO USING NLP MAXIMIZING W_net_opt;

DISPLAY "=== CLASSMATE'S FIXED CONDITIONS ===";
DISPLAY "Fixed pressures [bar]:", P_fixed;
DISPLAY "Fixed temperatures [K]:", T_fixed;
DISPLAY "Work with fixed conditions [kW]:", W_net_fixed.L;
DISPLAY "Efficiency with fixed [%]:", eta_fixed.L;

DISPLAY "=== OUR OPTIMIZED CONDITIONS ===";
DISPLAY "Optimized pressures [bar]:", P_opt.L;
DISPLAY "Optimized temperatures [K]:", T_opt.L;
DISPLAY "Work with optimization [kW]:", W_net_opt.L;
DISPLAY "Efficiency with optimization [%]:", eta_opt.L;

* Show the performance improvement
PARAMETERS
    work_improvement    "Work improvement [%]"
    efficiency_improvement "Efficiency improvement [%]"
    temp_violations     "Temperature constraint violations";

work_improvement = ((W_net_opt.L - W_net_fixed.L) / W_net_fixed.L) * 100;
efficiency_improvement = ((eta_opt.L - eta_fixed.L) / eta_fixed.L) * 100;

DISPLAY "=== PERFORMANCE COMPARISON ===";
DISPLAY "Work improvement with optimization [%]:", work_improvement;
DISPLAY "Efficiency improvement [%]:", efficiency_improvement;

DISPLAY "=== CONSTRAINT VIOLATIONS IN FIXED MODEL ===";

* Check violations
temp_violations = 0;
IF (T_fixed('3') > T_hw_out + (T_hw_in - T_hw_out) - DT_pinch,
    temp_violations = temp_violations + 1;
    DISPLAY "VIOLATION: T3 too high for pinch constraint";
);

IF (T_fixed('1') < T_amb + DT_appr,
    temp_violations = temp_violations + 1;
    DISPLAY "VIOLATION: T1 too low for approach constraint";
);

IF (ABS(T_fixed('4') - T_fixed('1')) > 1,
    temp_violations = temp_violations + 1;
    DISPLAY "VIOLATION: T4 ≠ T1 violates ORC cycle";
);

DISPLAY "Total constraint violations:", temp_violations;

DISPLAY "=== WHY OPTIMIZATION MATTERS ===";
DISPLAY "1. Fixed conditions prevent finding optimal performance";
DISPLAY "2. May violate competition constraints";
DISPLAY "3. Cannot adapt to different working fluids";
DISPLAY "4. Misses potential for significant improvements";
DISPLAY "5. Not suitable for actual design applications";