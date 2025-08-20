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

Working-fluid candidates and selection (pure fluids)
- We consider a set of at least five pure working fluids drawn from the recommended list and literature. Thermophysical constants (Tc, Pc, omega, MW) are treated as known for each candidate. Heat-capacity treatment follows the model: Cp(T) polynomials if available, otherwise a constant cp_avg. The optimal fluid is selected within the optimization (or via a screen–then–solve protocol) while ensuring that only one pure fluid is active in each run.

Decision levers
- Operating variables: state temperatures T(s) and pressures P(s) at the cycle points; working-fluid mass flow m_wf.
- Working-fluid identity: chosen from the candidate set (exactly one pure fluid active).
- Recuperator (Configuration B): internal duty and pinch.

Performance targets
- Maximize net electrical power while satisfying process and thermodynamic constraints.
- Primary focus on Configuration A per assignment; Configuration B is treated as an optional extension.
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
- Fluid selection dof: either binary indicators y_i (sum_i y_i = 1) for an integrated selection, or an external screening step that activates one pure fluid per run.

Objective (baseline)
- Maximize net power:
$$
W_{net} = \eta_{gen}\,\big( W_{turb} - W_{pump} \big) \quad (1)
$$

Energy balances and duties
$$
Q_{evap} = \dot{m}_{wf}\,\big(H_3 - H_2\big) \quad \text{(simple A)} \quad (2a)
$$
$$
Q_{evap} = \dot{m}_{wf}\,\big(H_3 - H_6\big) \quad \text{(recuperated B)} \quad (2b)
$$
$$
W_{turb} = \dot{m}_{wf}\,\big(H_3 - H_4\big) \quad (3)
$$
$$
W_{pump} = \dot{m}_{wf}\,\big(H_2 - H_1\big) \quad (4)
$$
$$
\dot{m}_{hot}\,C_{p,water}\,(T_{hw,in} - T_{hw,out}) \ge Q_{evap} \quad (5)
$$

Isentropic relations (engineering form)
- Turbine (3 -> 4):
$$
T_{4s} = T_3\,\Big( \tfrac{P_4}{P_3} \Big)^{\frac{k_3-1}{k_3}},\quad T_4 = T_3 - \eta_{turb}\,\big(T_3 - T_{4s}\big) \quad (6)
$$
- Pump (1 -> 2):
$$
T_{2s} = T_1\,\Big( \tfrac{P_2}{P_1} \Big)^{\frac{k_1-1}{k_1}},\quad T_2 = T_1 + \frac{T_{2s} - T_1}{\eta_{pump}} \quad (7)
$$
- Here k = cp / (cp - R_spec) and cp(T) is obtained from the derivative of H_ideal(T).
- Note: A full PR-based isentropic step would use s-const constraints; the above is a robust approximation that preserves units and trends without introducing additional differential relations.

Heat-transfer and pressure-structure constraints
$$
T_3 \le T_{hw,in} - \Delta T_{pinch} \quad (8)
$$
$$
T_1 \ge T_{cond} + \Delta T_{approach} \quad (9)
$$
$$
P_2 = P_3,\quad P_1 = P_4 \quad (10)
$$
$$
P_3 \le \alpha_{pc}\,P_c \quad (11)
$$

Recuperator constraints (Configuration B)
$$
\dot{m}_{wf}\,\big(H_4 - H_5\big) = \dot{m}_{wf}\,\big(H_6 - H_2\big) \quad (12)
$$
$$
T_4 - T_6 \ge \Delta T_{recup},\quad T_5 - T_2 \ge \Delta T_{recup} \quad (13)
$$

Thermodynamics: PR EOS and enthalpy model
$$
\alpha(T) = \big[ 1 + \kappa\,(1 - \sqrt{T/T_c}) \big]^2,\quad \kappa = 0.37464 + 1.54226\,\omega - 0.26992\,\omega^2 \quad (14)
$$
$$
A = 0.45724\,\frac{R_{bar}^2\,T_c^2}{P_c}\,\alpha(T)\,\frac{P}{(R_{bar}T)^2},\quad B = 0.07780\,\frac{R_{bar}T_c}{P_c}\,\frac{P}{R_{bar}T} \quad (15)
$$
$$
Z_{v} = 1 + B + \frac{A B}{3 + 2B},\quad Z_{l} = B + \frac{A B}{2 + 3B} \quad (16)
$$
$$
H_{ideal}(T) = \int_{T_{ref}}^{T} C_p(T)\,dT,\quad H_{dep} = R_{spec} T (Z - 1),\quad H = H_{ideal} + H_{dep} \quad (17)
$$
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
$$
\max\ J = W_{net} - \lambda_{mass}\,\dot{m}_{wf} - \lambda_{press}\,P_3 \quad (18)
$$
- Nonnegative weights encode preferences for lower flow (smaller equipment) and lower high-side pressure (operability/safety).

Reporting and comparison
- We present tabulated results for A and B: W_pump, W_turb, W_net, m_wf, key temperatures/pressures; for B, we also include Q_recup and internal pinch. When comparing with flowsheet simulations, we ensure matched boundary conditions and the same working fluid to avoid misleading differences.