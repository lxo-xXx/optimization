* ================================================================
* DEMONSTRATION 2: DIMENSIONAL INCONSISTENCY ERRORS
* This script shows dimensional problems in classmate's approach
* ================================================================

$TITLE Demonstration of Dimensional Errors

SETS
    st /1*4/;

PARAMETERS
    R       "Gas constant [bar*L/(mol*K)]"     /0.08314/
    Tc      "Critical temperature [K]"        /456.83/
    Pc      "Critical pressure [bar]"         /36.62/
    omega   "Acentric factor [-]"             /0.2931/
    
    P(st)   "Pressure [bar]"                  /1*4  10/
    T(st)   "Temperature [K]"                 /1*4  350/;

VARIABLES
    a_dim(st)   "Dimensional PR constant [bar*L²/mol²]"
    b_dim(st)   "Dimensional PR constant [L/mol]"
    Z(st)       "Compressibility factor [-]";

EQUATIONS
    calc_a_dimensional(st)   "Calculate dimensional a"
    calc_b_dimensional(st)   "Calculate dimensional b"
    wrong_eos(st)           "Dimensionally wrong EOS";

* Calculate dimensional constants (like classmate)
calc_a_dimensional(st)..
    a_dim(st) =E= 0.45724 * R**2 * Tc**2 / Pc;

calc_b_dimensional(st)..
    b_dim(st) =E= 0.07780 * R * Tc / Pc;

* Classmate's approach: Use dimensional values directly
wrong_eos(st)..
    Z(st)**3 + (1-b_dim(st))*Z(st)**2 + (a_dim(st)-3*b_dim(st)**2-2*b_dim(st))*Z(st)
    - (a_dim(st)*b_dim(st)-b_dim(st)**2-b_dim(st)**3) =E= 0;

* Bounds
Z.LO(st) = 0.1; Z.UP(st) = 2.0; Z.L(st) = 1.0;
a_dim.L(st) = 10; b_dim.L(st) = 0.1;

MODEL WRONG_DIMENSIONS /ALL/;

* This will solve but give dimensionally wrong results
SOLVE WRONG_DIMENSIONS USING NLP MINIMIZING Z('1');

DISPLAY "=== DIMENSIONAL ANALYSIS ===";
DISPLAY "a_dim units: [bar*L²/mol²]", a_dim.L;
DISPLAY "b_dim units: [L/mol]", b_dim.L;
DISPLAY "Z should be dimensionless", Z.L;

DISPLAY "=== PROBLEM EXPLANATION ===";
DISPLAY "The EOS cubic requires dimensionless A_pr and B_pr:";
DISPLAY "A_pr = a_dim * P / (R*T)²  [dimensionless]";
DISPLAY "B_pr = b_dim * P / (R*T)   [dimensionless]";
DISPLAY "Using dimensional values directly is mathematically wrong";

* Show what the correct values should be
PARAMETERS
    A_pr_correct(st) "Correct dimensionless A parameter"
    B_pr_correct(st) "Correct dimensionless B parameter";

A_pr_correct(st) = a_dim.L(st) * P(st) / (R * T(st))**2;
B_pr_correct(st) = b_dim.L(st) * P(st) / (R * T(st));

DISPLAY "=== CORRECT DIMENSIONLESS VALUES ===";
DISPLAY A_pr_correct, B_pr_correct;