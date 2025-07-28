* =============================================================================
* CORRECT GAMS PUT STATEMENT SYNTAX
* =============================================================================
* This file shows the correct way to write the problematic put statements

* INCORRECT (causes Error 409):
* put "- Thermal Efficiency: ", eta_thermal.l*100:6:2, " %"/;
* put "- Exergy Efficiency: ", eta_exergy.l*100:6:2, " %"/;
* put "- Critical Pressure Limit: ", 0.9 * sum(i, y.l(i) * fluid_props(i,'Pc')):6:1, " bar"/;

* CORRECT (enclose arithmetic expressions in parentheses):
put "- Thermal Efficiency: ", (eta_thermal.l*100):6:2, " %"/;
put "- Exergy Efficiency: ", (eta_exergy.l*100):6:2, " %"/;
put "- Critical Pressure Limit: ", (0.9 * sum(i, y.l(i) * fluid_props(i,'Pc'))):6:1, " bar"/;

* ALTERNATIVE (use intermediate variables):
SCALAR thermal_eff_percent, exergy_eff_percent, critical_pressure_limit;
thermal_eff_percent = eta_thermal.l * 100;
exergy_eff_percent = eta_exergy.l * 100;
critical_pressure_limit = 0.9 * sum(i, y.l(i) * fluid_props(i,'Pc'));

put "- Thermal Efficiency: ", thermal_eff_percent:6:2, " %"/;
put "- Exergy Efficiency: ", exergy_eff_percent:6:2, " %"/;
put "- Critical Pressure Limit: ", critical_pressure_limit:6:1, " bar"/;

* GAMS PUT STATEMENT RULES:
* 1. Simple variables: variable_name:width:decimals
* 2. Arithmetic expressions: (expression):width:decimals
* 3. Complex expressions: use intermediate variables
* 4. Always enclose calculations in parentheses for clarity