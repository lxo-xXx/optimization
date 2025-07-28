# 🔧 GAMS PUT STATEMENT ERROR FIX

## ❌ **THE PROBLEM**
Error 409: "Unrecognizable item" in GAMS put statements occurs when arithmetic expressions are not properly formatted.

## 🔍 **YOUR SPECIFIC ERRORS**
Lines causing compilation errors in `orc_improved_kamath_pr.gms`:

```gms
put "- Thermal Efficiency: ", eta_thermal.l*100:6:2, " %"/;           ❌ Line 302
put "- Exergy Efficiency: ", eta_exergy.l*100:6:2, " %"/;             ❌ Line 303  
put "- Critical Pressure Limit: ", 0.9 * sum(i, y.l(i) * fluid_props(i,'Pc')):6:1, " bar"/; ❌ Line 308
```

## ✅ **THE FIX**
Enclose arithmetic expressions in parentheses:

```gms
put "- Thermal Efficiency: ", (eta_thermal.l*100):6:2, " %"/;         ✅ CORRECT
put "- Exergy Efficiency: ", (eta_exergy.l*100):6:2, " %"/;           ✅ CORRECT
put "- Critical Pressure Limit: ", (0.9 * sum(i, y.l(i) * fluid_props(i,'Pc'))):6:1, " bar"/; ✅ CORRECT
```

## 🛠️ **ALTERNATIVE APPROACH**
Use intermediate variables for complex expressions:

```gms
SCALAR thermal_eff_percent, exergy_eff_percent, critical_pressure_limit;

thermal_eff_percent = eta_thermal.l * 100;
exergy_eff_percent = eta_exergy.l * 100;
critical_pressure_limit = 0.9 * sum(i, y.l(i) * fluid_props(i,'Pc'));

put "- Thermal Efficiency: ", thermal_eff_percent:6:2, " %"/;
put "- Exergy Efficiency: ", exergy_eff_percent:6:2, " %"/;
put "- Critical Pressure Limit: ", critical_pressure_limit:6:1, " bar"/;
```

## 📝 **GAMS PUT STATEMENT RULES**

### ✅ **CORRECT FORMATS:**
```gms
put variable_name:6:2;                          // Simple variable
put (expression):6:2;                           // Arithmetic expression
put "text", variable:6:2, "more text"/;        // Mixed content
```

### ❌ **INCORRECT FORMATS:**
```gms
put variable*100:6:2;                           // Missing parentheses
put sum(i, expr):6:2;                          // Complex sum without parentheses
put a + b * c:6:2;                             // Multiple operations without parentheses
```

## 🔧 **QUICK FIX FOR YOUR FILE**

Replace these exact lines in your `orc_improved_kamath_pr.gms`:

**Line 302:** Change to:
```gms
put "- Thermal Efficiency: ", (eta_thermal.l*100):6:2, " %"/;
```

**Line 303:** Change to:
```gms
put "- Exergy Efficiency: ", (eta_exergy.l*100):6:2, " %"/;
```

**Line 308:** Change to:
```gms
put "- Critical Pressure Limit: ", (0.9 * sum(i, y.l(i) * fluid_props(i,'Pc'))):6:1, " bar"/;
```

## ✅ **VERIFICATION**
After making these changes, your GAMS file should compile without Error 409.

The key rule: **Always enclose arithmetic expressions in parentheses when using them in put statements!**