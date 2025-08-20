# Problem Statement and Problem Formulation (Equation-Oriented, PR EOS + Kamath)

## Problem Statement (<= 1000 words)

Objective
- We aim to convert low- to medium-grade waste heat into electricity using an Organic Rankine Cycle (ORC) under industrially realistic constraints, and to formulate the optimization in an equation-oriented (EO) manner suitable for rigorous solution.

Scope and configurations
- A single hot-water stream is the heat source. The sink is an air-cooled condenser. Two ORC configurations are analyzed under identical boundary conditions:
  - Configuration A (simple cycle): evaporator -> turbine -> condenser -> pump
  - Configuration B (recuperated cycle): the simple cycle augmented with an internal heat exchanger (recuperator) that preheats the working fluid using turbine exhaust

Given data (nominal)

Table 1. Source/sink and equipment data (nominal)

| Item | Symbol | Value | Units |
|---|---|---:|---|
| Hot-water inlet temperature | T_hw_in | 443.15 | K |
| Hot-water outlet temperature | T_hw_out | 343.15 | K |
| Hot-water mass flow | m_hot | 100 | kg/s |
| Water heat capacity | Cp_water | 4.18 | kJ/(kg*K) |
| Condenser approach | dT_approach | 5 | K |
| Evaporator pinch | dT_pinch | 5 | K |
| Pump isentropic efficiency | eta_pump | 0.75 | - |
| Turbine isentropic efficiency | eta_turb | 0.80 | - |
| Generator efficiency | eta_gen | 0.95 | - |

Working-fluid properties (single-fluid model)
- We consider a single, fixed working fluid. Its thermophysical constants (Tc, Pc, omega, MW) are treated as known. Heat-capacity treatment follows the model: either Cp(T) coefficients are used, or a constant cp_avg is adopted. No fluid screening is assumed in this report.

Decision levers
- Operating variables: state temperatures T(s) and pressures P(s) at the cycle points; working-fluid mass flow m_wf.
- Recuperator (Configuration B): internal duty and pinch.

Performance targets
- Maximize net electrical power while satisfying process and thermodynamic constraints.
- Compare architectures (A vs B) on a like-for-like basis.
- Optionally explore trade-offs (e.g., operating conservatism) with a composite objective.

Thermophysical modeling
- Property calculations use the Peng–Robinson (PR) equation of state. A stable cubic-root selection consistent with liquid/vapor phases (Kamath-compatible handling) provides compressibility Z and departure functions. Ideal-gas enthalpy uses the same approach as the model code: Cp(T) polynomials if present, otherwise a constant cp_avg. Total enthalpy is H = H_ideal(T) + H_departure(T,P,Z).

Assumptions
- Steady state; single working fluid per case; negligible heat losses outside modeled exchangers; pressure drops lumped into equipment where applicable.
- PR EOS provides adequate accuracy over the operating window; Cp(T) polynomials are valid in the temperature range of interest.
- Ambient conditions remain fixed for condenser approach evaluation.

Key outputs
- Net power W_net, thermal efficiency, specific work, working-fluid mass flow, high/low pressures, state temperatures, and (for Configuration B) recuperator duty and internal pinch.

Validation note
- For fair comparisons against flowsheet simulations, matched boundary conditions (source/sink), identical fluid identity and property package, and consistent unit systems are required. Differences in fluid choice, bounds, or property methods can materially change W_turb and W_net.

## Problem Formulation (<= 1000 words)

Sets and states
- We use a four-state numbering for the simple cycle:
  - 1: condenser outlet (low pressure, liquid)
  - 2: pump outlet (high pressure, liquid)
  - 3: evaporator outlet (high pressure, vapor)
  - 4: turbine outlet (low pressure, vapor)
- For the recuperated cycle, we add two states:
  - 5: recuperator hot outlet (low pressure, cooled vapor)
  - 6: recuperator cold outlet (high pressure, preheated liquid)

Decision variables
- T(s) [K], P(s) [bar], Z(s) [-], H_ideal(s) [kJ/kg], H_dep(s) [kJ/kg], H(s) [kJ/kg]
- m_wf [kg/s], Q_evap [kW], Q_recup [kW], W_pump [kW], W_turb [kW], W_net [kW]

Objective (baseline)
- Maximize net power:
```
W_net = eta_gen * ( W_turb - W_pump )   .......... (eq. 1)
```

Energy balances and duties
```
Q_evap  = m_wf * ( H(3) - H(2) )        ; simple A   .......... (eq. 2A)
Q_evap  = m_wf * ( H(3) - H(6) )        ; recup.  B   .......... (eq. 2B)
W_turb  = m_wf * ( H(3) - H(4) )                      .......... (eq. 3)
W_pump  = m_wf * ( H(2) - H(1) )                      .......... (eq. 4)

m_hot * Cp_water * ( T_hw_in - T_hw_out ) >= Q_evap   .......... (eq. 5)
```

Isentropic relations (engineering form)
- Turbine (3 -> 4):
```
T4s = T3 * ( P4 / P3 )^((k3 - 1)/k3)     ; polytropic approx.
T4  = T3 - eta_turb * ( T3 - T4s )       .......... (eq. 6)
```
- Pump (1 -> 2):
```
T2s = T1 * ( P2 / P1 )^((k1 - 1)/k1)
T2  = T1 + ( T2s - T1 ) / eta_pump       .......... (eq. 7)
```
- Here k = cp / (cp - R_spec) and cp(T) is obtained from the derivative of H_ideal(T).
- Note: A full PR-based isentropic step would use s-const constraints; the above is a robust approximation that preserves units and trends without introducing additional differential relations.

Heat-transfer and pressure-structure constraints
```
T(3) <= T_hw_in - dT_pinch               ; evaporator pinch  .......... (eq. 8)
T(1) >= T_cond + dT_approach             ; condenser approach .......... (eq. 9)
P(2) =  P(3)                             ; high pressure      .......... (eq.10)
P(1) =  P(4)                             ; low pressure       .......... (eq.10)
P(3) <= alpha_pc * Pc                    ; critical-pressure  .......... (eq.11)
```

Recuperator constraints (Configuration B)
```
m_wf * ( H(4) - H(5) ) = m_wf * ( H(6) - H(2) )      .......... (eq.12)
T(4) - T(6) >= dT_recup  ;  T(5) - T(2) >= dT_recup   .......... (eq.13)
```

Thermodynamics: PR EOS and enthalpy model
```
alpha(T) = [ 1 + kappa * ( 1 - sqrt( T / Tc ) ) ]^2  .......... (eq.14)
kappa    = 0.37464 + 1.54226*omega - 0.26992*omega^2

A = 0.45724 * (R_bar^2 * Tc^2 / Pc) * alpha(T) * P / (R_bar*T)^2  .......... (eq.15a)
B = 0.07780 * (R_bar * Tc / Pc)      * P / (R_bar*T)               .......... (eq.15b)

Z_vapor  = 1 + B + A*B/(3 + 2*B) ; Z_liquid = B + A*B/(2 + 3*B)    .......... (eq.16)

H_ideal(T) = integral Cp(T) dT from T_ref to T
H_dep(T,P,Z) = R_spec * T * ( Z - 1 )
H(T,P) = H_ideal(T) + H_dep(T,P,Z)                                 .......... (eq.17)
```
- Phase consistency: use Z_liquid downstream of condenser/pump, Z_vapor downstream of evaporator/turbine.
- Units: H in kJ/kg, m_wf in kg/s, hence powers in kW by construction.

Variable bounds (illustrative)
```
300 <= T(1) <= 370     ; K
300 <= T(2) <= 390
360 <= T(3) <= T_hw_in - dT_pinch
300 <= T(4) <= 420
1   <= P(s) <= 0.75*Pc ; bar
1   <= m_wf <= 120     ; kg/s
```

Optional multi-objective extension
```
Maximize  J = W_net - lambda_mass * m_wf - lambda_press * P(3)    .......... (eq.18)
```
- Nonnegative weights encode preferences for lower flow (smaller equipment) and lower high-side pressure (operability/safety).

Reporting and comparison
- We present tabulated results for A and B: W_pump, W_turb, W_net, m_wf, key temperatures/pressures; for B, we also include Q_recup and internal pinch. When comparing with flowsheet simulations, we ensure matched boundary conditions and the same working fluid to avoid misleading differences.