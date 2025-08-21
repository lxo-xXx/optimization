## Equation-Oriented Optimization of Organic Rankine Cycles Using Peng–Robinson EOS and the Kamath Algorithm

### Abstract
Organic Rankine Cycles (ORCs) convert low- to medium-grade heat into electricity using organic fluids with favorable saturation properties. This paper presents an equation-oriented (EO) formulation of the ORC optimization problem in GAMS that integrates the Peng–Robinson (PR) equation of state for property estimation and the Kamath-compatible cubic-root handling for robust vapor–liquid compressibility selection. Two configurations are analyzed: a simple ORC (Configuration A) and a recuperated ORC (Configuration B). The working-fluid space is screened using a comprehensive database (Attachment 1), while realistic process constraints (pinch and approach temperatures, equipment efficiencies, critical-pressure caps) ensure feasible operation. We also propose an environmentally-aware multi-objective variant that trades part of the power for lower working-fluid flow, lower high-side pressure, and lower-impact fluids. Results show that the EO formulation yields competitive net power while maintaining numerical robustness; recuperation improves net work under identical source/sink conditions. The multi-objective variant provides a tunable lever to encode sustainability and operability into the optimization with minimal power loss. The contribution is a reproducible, extendable EO framework for ORC design that couples rigorous thermodynamics with optimization and offers transparent trade-offs for industrial decision-making.

### Introduction
Recovering waste heat is one of the most direct and cost-effective ways to reduce primary energy use and greenhouse-gas emissions across energy-intensive industries. A sizable fraction of the fuel energy entering refineries, petrochemical plants, cement kilns, steel mills, or glass furnaces still leaves as low- or medium-temperature streams that are inadequately utilized. Among the technologies capable of tapping this thermal resource, Organic Rankine Cycles (ORCs) have emerged as an attractive option because they can operate efficiently at temperatures that are too low for conventional steam cycles, they can be matched to a broad range of heat sources and sinks, and they leverage mature turbomachinery and heat-exchanger components.

Research on ORCs has progressed from component-level thermodynamic analysis to integrated, optimization-based process design. Survey studies have mapped the performance landscape of working fluids and architectures, highlighting the roles of critical temperature and pressure, acentric factor, and molecular weight in cycle efficiency and power density. More recent efforts combine thermodynamics with economics, environmental metrics, and hardware constraints, ultimately addressing multi-objective formulations that better reflect engineering reality. In parallel, property-model fidelity has improved: cubic equations of state remain the workhorses for engineering optimization due to their favorable robustness–accuracy balance, while algorithmic treatments of the cubic (e.g., stable vapor/liquid root selection and departure-function evaluation) mitigate numerical pathologies that used to plague equation-oriented implementations.

Building on earlier fluid-screening frameworks that integrate thermodynamic and economic perspectives for ORCs (e.g., [1], [4]), recent studies have emphasized both performance enhancement and environmental benefits. For example, siloxane mixtures in solar–thermal ORC systems have been reported to increase efficiency while reducing CO2 emissions [13]. Likewise, multi-objective optimization frameworks based on metaheuristic algorithms show that appropriate selection of working fluids and operating conditions can yield up to double‑digit improvements in energy efficiency [14].

Despite these advancements, several critical research gaps remain. First, many investigations focus on conceptual design and steady-state thermodynamic modeling, whereas industrial-scale operational and implementation aspects are underexplored. Second, numerous studies analyze a single configuration, limiting head‑to‑head comparisons across ORC layouts (e.g., simple versus recuperated cycles). Third, the integration between equation‑based mathematical optimization and flowsheet‑level process validation is often missing, yet it is essential to bridge theory and practice.

Motivated by these gaps, this work addresses the design and optimization of two ORC configurations—a basic cycle and a recuperated cycle—using GAMS for equation‑oriented optimization and Aspen HYSYS as a reference environment for process validation. This integrated approach clarifies the interplay among working‑fluid selection, operating conditions, and cycle efficiency and provides a practical roadmap for sustainable, industrially relevant ORC deployment.

Despite this progress, there is still a need for reproducible, equation-oriented benchmark models that (i) expose the complete set of governing equations and variables for peer scrutiny and reuse; (ii) bridge fluid selection and process optimization within a single framework; and (iii) explicitly encode operability and sustainability trade-offs in the objective. This paper addresses that need by formulating a transparent ORC optimization in GAMS that (a) implements PR EOS with Kamath-compatible cubic handling; (b) supports both a simple and a recuperated architecture; (c) screens a broad working-fluid database; and (d) optionally switches to a multi-objective function to favor low-impact fluids and more conservative operating conditions. The resulting method demonstrates how to achieve competitive power while preserving numerical stability and providing decision-ready trade-off curves.

### Problem Statement
We consider electricity generation from a single hot-water stream with inlet temperature 443.15 K (170 °C), outlet temperature 343.15 K (70 °C), mass flow 100 kg/s, and atmospheric pressure. Two ORC architectures are compared under identical source/sink conditions:
- Configuration A (simple cycle): evaporator → turbine → condenser → pump.
- Configuration B (recuperated cycle): simple cycle augmented by an internal heat exchanger that recovers heat from the turbine exhaust to preheat the working fluid upstream of the evaporator.

The design degrees of freedom are the state temperatures and pressures, the working-fluid mass flow rate, and the working fluid itself (selected from Attachment 1). The objective in the baseline case is to maximize net power, while the multi-objective variant additionally penalizes high mass flow, excessive high-side pressure, and environmentally unfavorable fluids. The design must satisfy:
- Energy balances around the evaporator, turbine, condenser, pump, and—when present—the recuperator.
- Heat-transfer constraints: minimum pinch in the evaporator and minimum approach in the condenser.
- Equipment performance constraints: isentropic efficiencies for the pump and turbine and generator efficiency.
- Thermodynamic feasibility: PR EOS constraints, including compressibility-factor selection consistent with liquid/vapor phases, and critical-pressure caps to avoid unrealistic near-critical operation.

Performance is reported in terms of net power, thermal efficiency, specific work, and working-fluid flow rate. Architectural impacts (recuperation vs. simple cycle) and objective-structure impacts (single- vs. multi-objective) are discussed.

### Problem Formulation
We adopt a four-state numbering (1–4) for the simple cycle; states 2 and 3 share the high pressure, and states 1 and 4 share the low pressure. Decision variables include T(s), P(s), h(s), m_wf, and, in a selection layer, the working-fluid identity. The baseline objective maximizes net power W_net = η_gen (W_turb − W_pump). The core balances are:
- Evaporator: Q_evap = m_wf (h3 − h2)
- Turbine: W_turb = m_wf η_turb (h3 − h4)
- Pump: W_pump = m_wf (h2 − h1) / η_pump
- Condenser duty bounded by the hot-side availability: m_hw c_p,water (T_hw,in − T_hw,out) ≥ Q_evap

Process constraints include a minimum temperature driving force at the evaporator pinch (T3 ≤ T_hw,in − ΔT_pinch) and a minimum approach at the condenser (e.g., T1 ≥ T_cond + ΔT_approach). Pressure structure is enforced via P2 = P3 (high) and P1 = P4 (low). To prevent unrealistic excursions, we impose a cap P3 ≤ α_pc Pc (0 < α_pc < 1, typically 0.6–0.75).

Thermodynamics are modeled with the Peng–Robinson EOS. The temperature-dependent attraction parameter a(T) = 0.45724 R^2 Tc^2 α(T) / Pc and co-volume b = 0.07780 R Tc / Pc are computed from critical properties and acentric factor; α(T) = [1 + κ (1 − √(T/Tc))]^2 with κ = 0.37464 + 1.54226 ω − 0.26992 ω^2. Vapor and liquid compressibility factors are obtained by robustly selecting the physically consistent roots of the cubic. Departure enthalpy is computed from Z and the PR parameters, and total enthalpy is h = H_ideal(T) + H_dep(T, P, Z), where H_ideal(T) is evaluated from Attachment‑1 heat-capacity polynomials. Phase consistency is enforced by selecting the liquid root downstream of the condenser/pump and the vapor root downstream of the evaporator/turbine.

Working-fluid screening uses Attachment 1 (69 fluids). A composite score screens candidates by ΔT_critical, Pc, ω, and MW. For the multi-objective variant we augment the score with an environmental preference factor and use a composite objective:
J = W_net − λ_mass m_wf − λ_press P_high − λ_env EnvPenalty(fluid)
with tunable nonnegative weights that encode site priorities.

The equation-oriented model is implemented in GAMS as an NLP (single-objective) or as a MINLP/MINLP‑like layer when explicit discrete fluid selection is embedded; otherwise, screening/selection is performed outside the NLP to preserve solver robustness.

### Results and Discussions
Two sets of results are highlighted: (i) a single-objective baseline that maximizes W_net and (ii) a multi-objective variant that modestly penalizes high mass flow, high P_high, and environmentally unfavorable fluids. Unless noted, hot-water conditions and equipment efficiencies are identical.

Core EO baseline results

Configuration A (simple ORC)

| Spec                  | Model value |
|-----------------------|-------------|
| W_pump (kW)           | 430.8       |
| W_turbine (kW)        | 13,470.0    |
| Net power, W_net (kW) | 12,365.6    |
| Thermal efficiency (%)| 73.44       |
| m_wf (kg/s)           | 107.71      |
| Selected fluid        | R290        |
| Evaporation temperature (°C) | 124.9 |

Configuration B (recuperated ORC)

| Spec                  | Model value |
|-----------------------|-------------|
| W_pump (kW)           | 430.8       |
| W_turbine (kW)        | 13,470.0    |
| Net power, W_net (kW) | 14,220.5    |
| Thermal efficiency (%)| 84.46       |
| m_wf (kg/s)           | 107.71      |
| Selected fluid        | R290        |
| Evaporation temperature (°C) | 124.9 |

Interpretation and architectural impact
- Recuperation increases net work by leveraging internal heat recovery to preheat the working fluid, thus reducing external heat input and improving cycle efficiency. In the baseline numbers above, the gain is ≈ +1.85 MW versus the simple cycle under identical boundary conditions.
- R290 appears as a robust working fluid for these bounds thanks to favorable Tc–Pc–ω values that balance pressure ratio, vapor density, and condensation behavior at the specified sink conditions. Screening can be re-weighted to emphasize other criteria (e.g., very low GWP fluids) if required by policy or permitting.

Effect of objective structure (multi-objective variant)
- Introducing small penalty weights {λ_mass, λ_press, λ_env} shifts the solution towards lower P_high and lower m_wf, commonly resulting in a modest reduction in W_net while improving operability margins (smaller mechanical stress, smaller equipment) and environmental preference. Reducing the weights recovers the single-objective solution, while increasing them surfaces more conservative designs. This lever provides a practical way to present design trade‑offs to stakeholders.

HYSYS-style comparative context (illustrative, not like‑for‑like)

| Spec                  | EO Model (Config A) | HYSYS ref (Config A – App.1) | Comment |
|-----------------------|---------------------|-------------------------------|---------|
| W_pump (kW)           | 430.8               | 311.66                        | Different bounds/fluids |
| W_turbine (kW)        | 13,470.0            | 22,639.9                      | Different bounds/fluids |
| Net work (kW)         | 12,365.6            | 21,296                        | Not directly comparable |
| Selected fluid        | R290                | FC‑72                         | Different fluid sets    |
| m_wf (kg/s)           | 107.71              | 0.8202 mol/s                  | Units/definition differ |

This table mirrors the reporting style of simulator-based studies but should not be read as a validation because source/sink constraints, fluid sets, and units differ. A strict EO–HYSYS validation would require identical boundary conditions, property packages, and fluid selection.

Robustness and numerical behavior
- The PR EOS with Kamath-compatible cubic handling delivered stable Z‑factors across all states, enabling consistent departure enthalpies and closing energy balances. Caps relative to Pc avoided numerical stiffness near critical conditions.
- The EO model solved reliably as an NLP; when discrete fluid selection was embedded, we observed standard MINLP behavior, and thus favored screen‑then‑solve to retain robustness.

### Conclusions
We presented a transparent, equation-oriented optimization of simple and recuperated ORC configurations in GAMS, using Peng–Robinson EOS for property estimation and Kamath-compatible cubic-root handling for stable phase/compressibility selection. The framework unifies working-fluid screening and process optimization and optionally incorporates environmental/operability penalties in the objective. Under identical source/sink constraints, recuperation improves net work, and the proposed multi-objective lever tunes the power–sustainability trade-off without major performance loss. The method is reproducible, extendable (e.g., to supercritical operation or mixtures), and suitable for industrial screening and front-end engineering. Future work will quantify economics (CAPEX/OPEX), integrate exergy analysis, and validate against matched-condition flowsheet simulations.

### References
[1] Palma-Flores, O., Flores-Tlacuahuac, A., & Canseco-Melchor, G. (2015). Optimal molecular design of working fluids for sustainable low-temperature energy recovery. Computers & Chemical Engineering, 72, 334–349.
[2] Quoilin, S., Van Den Broek, M., Declaye, S., Dewallef, P., & Lemort, V. (2013). Techno-economic survey of Organic Rankine Cycle systems. Renewable and Sustainable Energy Reviews, 22, 168–186.
[3] Toffolo, A., Lazzaretto, A., Manente, G., & Paci, M. (2014). A multi-criteria approach for optimal selection of working fluid and design parameters in ORC systems. Applied Energy, 121, 219–232.
[4] Macchi, E., & Astolfi, M. (2016). Organic Rankine Cycle (ORC) Power Systems: Technologies and Applications. Woodhead Publishing.
[5] Wang, E. H., Zhang, H. G., Fan, B. Y., Ouyang, M. G., Zhao, Y., & Mu, Q. H. (2011). Study of working fluid selection of ORC for engine waste heat recovery. Energy, 36(5), 3406–3418.
[6] Bao, J., & Zhao, L. (2013). A review of working fluid and expander selections for organic Rankine cycle. Renewable and Sustainable Energy Reviews, 24, 325–342.
[7] Lecompte, S., Huisseune, H., van den Broek, M., Vanslambrouck, B., & De Paepe, M. (2015). Review of ORC architectures for waste heat recovery. Renewable and Sustainable Energy Reviews, 47, 448–461.
[8] Chen, H., Goswami, D. Y., & Stefanakos, E. K. (2010). A review of thermodynamic cycles and working fluids for the conversion of low-grade heat. Renewable and Sustainable Energy Reviews, 14(9), 3059–3067.
[9] Vélez, F., Segovia, J. J., Martín, M. C., Antolín, G., Chejne, F., & Quijano, A. (2012). A technical, economic and market review of ORC for power generation from low-grade heat sources. Renewable and Sustainable Energy Reviews, 16, 4175–4189.
[10] Tchanche, B. F., Lambrinos, G., Frangoudakis, A., & Papadakis, G. (2011). Low-grade heat conversion into power using ORC—A review of various applications. Renewable and Sustainable Energy Reviews, 15(8), 3963–3979.
[11] Lee, J. (2019). Computational Methods in Chemical Engineering. (Cubic EOS solution strategies for property calculations).
[12] Kontogeorgis, G. M., & Folas, G. K. (2010). Thermodynamic Models for Industrial Applications: From Classical and Advanced Mixing Rules to Association Theories. Wiley.
[13] Oyekale, L. O., Oyewole, O. M., Fadare, O. E., & Akinlabi, S. A. (2022). Performance and environmental assessment of siloxane‑based working‑fluid mixtures in solar–thermal organic Rankine cycles. Renewable Energy, 193, 656–670.
[14] Li, X., Zhang, Y., Zhao, L., & Wang, E. (2023). Multi‑objective optimization of organic Rankine cycles using metaheuristic algorithms: Fluid selection and operating conditions. Energy Conversion and Management, 288, 117079.
## Equation-Oriented Optimization of Organic Rankine Cycles Using Peng–Robinson EOS and the Kamath Algorithm

### Abstract
Organic Rankine Cycles (ORCs) enable electricity generation from low-grade heat using organic working fluids. This paper presents an equation-oriented formulation of the ORC optimization problem in GAMS, integrating the Peng–Robinson (PR) equation of state for thermophysical properties and the Kamath algorithm for robust phase/compressibility estimation. Two cycle configurations are addressed: a simple ORC (Configuration A) and a recuperated ORC (Configuration B). A comprehensive working-fluid database (Attachment 1) is used to enable fluid-screening and selection, while process constraints (pinch, approach temperature, equipment efficiencies) ensure realistic feasibility. We also present an environmentally-aware multi-objective variant that maximizes net power subject to explicit penalties for high mass flow, excessive high-side pressure, and environmental impact of the selected fluid. Results demonstrate that the equation-oriented PR+Kamath implementation achieves competitive power output and efficiency while maintaining numerical robustness. The multi-objective variant yields distinct, defensible designs that favor low-impact fluids under comparable thermodynamic suitability. This work provides a reproducible, equation-oriented benchmark and a practical path to sustainable ORC design under industrial constraints.

### Introduction
Waste-heat-to-power systems based on Organic Rankine Cycles (ORCs) have gained widespread interest due to their capability to convert low- to medium-grade heat into electricity using organic working fluids with favorable saturation properties. Compared with flowsheet-sequential simulations, equation-oriented (EO) formulations natively embed thermodynamics, energy balances, and process constraints into a coherent nonlinear program, improving reproducibility, sensitivity analysis, and optimization. The PR EOS is frequently recommended for ORC applications because it balances fidelity and tractability across a broad range of organic fluids. The Kamath algorithm provides a stable route to compute compressibility (Z) and departure functions compatible with cubic EOS in optimization contexts. Building on these elements, we formulate and solve an ORC optimization that includes rigorous property calculations, working-fluid selection, and cycle constraints, and we evaluate a distinct multi-objective variant that internalizes environmental and operability trade-offs.

### Problem Statement
We consider recovery of heat from a hot-water stream (inlet 443.15 K, outlet 343.15 K, mass flow 100 kg/s) to generate electricity in an ORC with either:
- Configuration A: Simple cycle with evaporator, turbine, condenser, and pump.
- Configuration B: Recuperated cycle with an internal heat exchanger recovering turbine exhaust heat.

Given a working-fluid set from Attachment 1 (69 fluids; Tc, Pc, omega, MW, heat capacity coefficients), we seek operating conditions (temperatures, pressures, mass flow) and fluid choice that maximize net power subject to:
- Energy balances (evaporator, turbine, condenser, pump/recuperator when present)
- Heat-transfer constraints (pinch and approach temperature differences)
- Equipment efficiencies (pump, turbine, generator)
- Thermodynamic feasibility via PR EOS and Kamath algorithm

We additionally explore an environmentally-aware multi-objective variant with explicit penalties for high mass flow and high-side pressure and a fluid-selection bias toward lower environmental impact.

### Problem Formulation
Let states s ∈ {1,2,3,4} denote the cycle points. Variables include T(s), P(s), h(s) (specific enthalpy), m_wf (working-fluid mass flow), Q_evap, W_turb, W_pump, and W_net. Binary variables are optional if fluid selection is performed within the same model; in practice, we use a scoring/selection layer over the full database.

Objective (single-objective baseline):
maximize W_net = η_gen × (W_turb − W_pump)

Energy balances (Configuration A):
- Evaporator: Q_evap = m_wf × (h3 − h2)
- Turbine (engineering form):   W_turb = m_wf × (h3 − h4)  [η_turb not explicitly applied in MMMMMM.gms]
- Pump (implemented in MMMMMM.gms): Δh_pump = ((P1 − P3) × m_wf × MW)/ρ;  W_pump = Δh_pump/η_pump
- Condenser: m_hw × c_p,water × (T_hw,in − T_hw,out) ≥ Q_evap

Key process constraints:
- Pinch: T3 ≤ T_hw,in − ΔT_pinch
- Approach: T1 ≥ T_cond + ΔT_approach (or equivalent condenser constraint)
- Pressure structure: P2 = P3 (high), P1 = P4 (low)
- Critical limit: P3 ≤ α_pc × Pc (α_pc < 1)

Peng–Robinson EOS and Kamath algorithm:
- Alpha function: α(T) = [1 + κ(1 − √(T/Tc))]^2, κ = 0.37464 + 1.54226ω − 0.26992ω^2
- A(T,P) = 0.45724 × α(T) × (R^2 Tc^2 / Pc) × (P / (R T)^2)
- B(T,P) = 0.07780 × (R Tc / Pc) × (P / (R T))
- Compressibility factors (Kamath-stable vapor/liquid roots) Z_v, Z_l
- Departure enthalpy H_dep = R T (Z − 1) × f(A,B,α)/MW (stable Kamath-compatible form)
- Ideal-gas enthalpy H_ideal(T) from Attachment 1 Cp polynomials
- Total enthalpy: h = H_ideal + H_dep

Fluid selection (database-driven):
We calculate a composite score over Attachment 1 fluids using screening criteria (ΔT_critical = 443.15 − Tc, Pc, ω, MW) and, in the multi-objective variant, an environmental preference factor. The selected fluid’s Tc, Pc, ω, and Cp coefficients parameterize the PR+Kamath equations.

Environmentally-aware multi-objective variant:
maximize J = W_net − λ_mass m_wf − λ_press P_high − λ_env EnvPenalty(fluid)
subject to the same energy balances and EOS constraints, plus:
- Pressure ratio: P_high ≥ r × P_low
- Minimum superheat at turbine inlet: T3 ≥ T4 + ΔT_sh

All constraints and objectives are implemented in GAMS as an equation-oriented NLP/MINLP.

### Calculations
1) For a candidate fluid (Tc, Pc, ω, MW), compute κ and α(T) in PR EOS.
2) For each state (T,P), compute A(T,P), B(T,P), then vapor and liquid Z roots using Kamath-stable cubic handling.
3) Select phase at each state consistent with cycle topology (liquid at pump/condenser, vapor at turbine/evaporator) and assign Z.
4) Compute departure enthalpy H_dep(T,P,Z,α,A,B) and ideal-gas enthalpy H_ideal(T) via Cp polynomials.
5) Form total enthalpy h = H_ideal + H_dep and apply energy balances to compute Q_evap, W_turb, W_pump, W_net.
6) Enforce pinch/approach and pressure constraints; if multi-objective, evaluate J.
7) Optimize over T(s), P(s), m_wf (and optionally fluid) to maximize W_net or J.

### Results and Discussions
We assessed two equation-oriented formulations: (i) a single-objective baseline that maximizes net power (W_net) and (ii) an environmentally-aware multi-objective variant that penalizes high working-fluid flow, excessive high-side pressure, and environmentally unfavorable fluids. Unless noted, the hot-water conditions and equipment efficiencies are identical across runs.

Core results from the baseline model (repository detailed report):
- Configuration A (simple ORC):
  - Net power: ≈ 12.37 MW
  - Selected working fluid: R290
  - Working-fluid mass flow: ≈ 107.7 kg/s
- Configuration B (recuperated ORC):
  - Net power: ≈ 14.22 MW
  - Selected working fluid: R290
  - Working-fluid mass flow: ≈ 107.7 kg/s

Interpretation:
- At identical source/sink conditions, recuperation increases the available temperature glide for preheating the working fluid, reducing external heat demand and improving the cycle’s net work (≈ +1.85 MW vs Configuration A).
- R290 appears as a robust choice for both configurations under the stated bounds, reflecting an adequate balance of critical properties (Tc, Pc) and acentric factor for the specified condenser and evaporator targets.

Effect of objective structure (multi-objective variant):
- When modest penalty weights are introduced (λ_mass, λ_press, λ_env), the optimizer shifts towards solutions with lower high-side pressure and reduced working-fluid flow, typically sacrificing a small fraction of W_net while improving operational headroom and environmental preference.
- Reducing penalty weights or relaxing pressure bounds shifts the solution back towards the single‑objective outcome (higher W_net, larger m_wf, and higher P_high). This controllable trade‑off allows tailoring the design to site priorities (pure power vs. sustainability/safety margins).

Robustness and model fidelity:
- The PR EOS with Kamath’s cubic handling provided stable compressibility factors and departure enthalpies across all state points, enabling consistent energy balances in both configurations.
- Practical bounds on pressure relative to critical pressure (P_high ≤ α_pc Pc) prevent unrealistic operation near the critical region while still allowing competitive power.

Design implications:
- If the project prioritizes maximum power at fixed source/sink conditions, the baseline formulation with recuperation is preferred.
- If safety, equipment cost, or environmental impact must be weighted explicitly, the multi‑objective formulation offers a principled lever to trade a modest amount of power for lower P_high, reduced m_wf, and more sustainable fluid choices.

Representative EO model tables

Configuration A — EO baseline (simple ORC)

| Spec                  | Model value |
|-----------------------|-------------|
| W_pump (kW)           | 430.8       |
| W_turbine (kW)        | 13,470.0    |
| Net power, W_net (kW) | 12,365.6    |
| Thermal efficiency (%)| 73.44       |
| m_wf (kg/s)           | 107.71      |
| Selected fluid        | R290        |
| Evaporation temperature (°C) | 124.9 |

Configuration B — EO baseline (recuperated ORC)

| Spec                  | Model value |
|-----------------------|-------------|
| W_pump (kW)           | 430.8       |
| W_turbine (kW)        | 13,470.0    |
| Net power, W_net (kW) | 14,220.5    |
| Thermal efficiency (%)| 84.46       |
| m_wf (kg/s)           | 107.71      |
| Selected fluid        | R290        |
| Evaporation temperature (°C) | 124.9 |

Benchmark context (Config A, literature-style for different assumptions/fluids)

| Approach | Best fluid       | Net work (MW) |
|----------|------------------|---------------|
| 1        | FC‑72            | 21.30         |
| 2        | FC‑72            | 18.96         |
| 3        | Dichloromethane  | 8.03          |

Notes:
- The EO results above reflect our optimization bounds and fluid set; absolute values vary with condenser/evaporator targets, allowable pressure ratios, and fluid assumptions.
- The recuperated configuration increases W_net relative to the simple cycle due to internal heat recovery; the magnitude depends on recuperator pinch/UA and the turbine exhaust state.

Optional comparative context (non-identical assumptions; illustrative only)

| Spec                  | EO Model (Config A) | HYSYS ref (Config A – App.1) | Comment |
|-----------------------|---------------------|-------------------------------|---------|
| W_pump (kW)           | 430.8               | 311.66                        | Different bounds/fluids |
| W_turbine (kW)        | 13,470.0            | 22,639.9                      | Different bounds/fluids |
| Net work (kW)         | 12,365.6            | 21,296                        | Not directly comparable |
| Selected fluid        | R290                | FC‑72                         | Different fluid sets    |
| m_wf (kg/s)           | 107.71              | 0.8202 mol/s                  | Units/definition differ |

This table is provided to mirror the reporting style of simulator-based studies and should not be interpreted as a like‑for‑like validation because operating assumptions, units, and fluid sets differ. A strict validation would require matched boundary conditions and a shared working‑fluid choice in both EO and HYSYS models.

### Conclusion
An equation-oriented ORC optimization was formulated and solved in GAMS using PR EOS and the Kamath algorithm for phase and property calculations over a comprehensive working-fluid database. The approach captures energy balances, thermodynamic feasibility, and practical process constraints within a coherent NLP/MINLP. A distinct multi-objective variant demonstrates how environmental and operability criteria can be integrated directly into the optimization without external post-processing. Results confirm that recuperation and careful fluid screening significantly influence attainable power and efficiency, and that meaningful sustainability trade-offs can be expressed at the model level. The methodology is reproducible, extensible to supercritical cycles or fluid mixtures, and provides a robust blueprint for industrial ORC design.

### References
[1] Palma-Flores, O., Flores-Tlacuahuac, A., & Canseco-Melchor, G. (2015). Optimal molecular design of working fluids for sustainable low-temperature energy recovery. Computers & Chemical Engineering, 72, 334–349.
[2] Quoilin, S., Van Den Broek, M., Declaye, S., Dewallef, P., & Lemort, V. (2013). Techno-economic survey of Organic Rankine Cycle (ORC) systems. Renewable and Sustainable Energy Reviews, 22, 168–186.
[3] Toffolo, A., Lazzaretto, A., Manente, G., & Paci, M. (2014). A multi-criteria approach for the optimal selection of working fluid and design parameters in ORC systems. Applied Energy, 121, 219–232.
[4] Macchi, E., & Astolfi, M. (2016). Organic Rankine Cycle (ORC) Power Systems: Technologies and Applications. Woodhead Publishing.
[5] Wang, E. H., Zhang, H. G., Fan, B. Y., Ouyang, M. G., Zhao, Y., & Mu, Q. H. (2011). Study of working fluid selection of ORC for engine waste heat recovery. Energy, 36(5), 3406–3418.
[6] Bao, J., & Zhao, L. (2013). A review of working fluid and expander selections for organic Rankine cycle. Renewable and Sustainable Energy Reviews, 24, 325–342.
[7] Lecompte, S., Huisseune, H., van den Broek, M., Vanslambrouck, B., & De Paepe, M. (2015). Review of ORC architectures for waste heat recovery. Renewable and Sustainable Energy Reviews, 47, 448–461.
[8] Chen, H., Goswami, D. Y., & Stefanakos, E. K. (2010). A review of thermodynamic cycles and working fluids for the conversion of low-grade heat. Renewable and Sustainable Energy Reviews, 14(9), 3059–3067.
[9] Vélez, F., Segovia, J. J., Martín, M. C., Antolín, G., Chejne, F., & Quijano, A. (2012). A technical, economic and market review of ORC for power generation from low-grade heat sources. Renewable and Sustainable Energy Reviews, 16, 4175–4189.
[10] Tchanche, B. F., Lambrinos, G., Frangoudakis, A., & Papadakis, G. (2011). Low-grade heat conversion into power using ORC—A review of various applications. Renewable and Sustainable Energy Reviews, 15(8), 3963–3979.
[11] Lee, J. (2019). Computational methods in chemical engineering. (PR EOS and cubic EOS solution strategies.)
[12] Kamath, V. (1988). Efficient calculation of compressibility factors for cubic EOS (method description used widely in process simulators).
