* ================================================================
* DEMONSTRATION 1: UNDEFINED VARIABLES ERROR
* This script shows the fatal compilation error in classmate's model
* ================================================================

$TITLE Demonstration of Undefined Variables Error

* This reproduces the exact problem from classmate's model
SETS
    st /1*4/;

PARAMETERS
    R /8.314/;

* Define only dimensional constants (like classmate did)
VARIABLES
    a(st), b(st)  "Dimensional PR constants"
    Z(st)         "Compressibility factor";

* The classmate's EOS equation that WILL FAIL
EQUATIONS
    EOS_FAILS(st) "This equation will cause compilation error";

* This is EXACTLY what the classmate wrote
EOS_FAILS(st).. Z(st)**3 + (1-B(st))*Z(st)**2 + (A(st)-3*B(st)**2-2*B(st))*Z(st)
                - (A(st)*B(st)-B(st)**2-B(st)**3) =E= 0;

MODEL DEMO_FAIL /ALL/;

* Try to solve - this will FAIL with compilation error
SOLVE DEMO_FAIL USING NLP MINIMIZING Z('1');

* EXPECTED ERROR MESSAGES:
* Error: Unknown symbol 'A'
* Error: Unknown symbol 'B'
* The model uses A(st) and B(st) but only defines a(st) and b(st)

DISPLAY "This script demonstrates the compilation failure";
DISPLAY "Variables A(st) and B(st) are used but never defined";