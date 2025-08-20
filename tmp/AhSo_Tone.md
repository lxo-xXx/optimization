Milad Sohrabi<sup>a</sup>, Majid Ahmadian<sup>b</sup>

<sup>a</sup>Student number : 402211297, Msc. Process Design in Chemical
Engineering , Sharif university of Technology

<sup>b</sup>Student number : 402200694, Msc. Process Design in Chemical
Engineering , Sharif university of Technology

Abstract

The Organic Rankine Cycle (ORC) offers a promising solution for
converting low-grade heat into electricity by utilizing organic fluids
with favorable thermodynamic properties. This study explores the impact
of different working fluids on ORC efficiency across various
configurations. Through experimental and simulation analyses, the study
identifies R142b, FC-72 and dichloromethane as top performers under
different conditions. Results demonstrate that fluid selection
critically influences ORC performance. This research underscores the
ORC's versatility in enhancing energy efficiency and reducing waste
across industrial applications.

*Keywords:* Rankine Cycle, GAMS, Fluid selection;

#  Introduction 

The Organic Rankine Cycle (ORC) represents a significant advancement in
power generation technology, leveraging low-grade heat sources for the
production of electricity. Named after its working principle derived
from the conventional Rankine cycle, the ORC differentiates itself by
employing organic fluids with favorable thermodynamic properties instead
of water. This adaptation allows the ORC to efficiently exploit heat
from diverse and typically low-temperature sources, such as geothermal
reservoirs, solar thermal energy, industrial waste heat, and biomass
combustion.

The selection of an appropriate working fluid is a critical aspect of
optimizing ORC performance. The ideal fluid must possess several key
characteristics to ensure efficiency and safety. These include

suitable boiling and condensation points relative to the heat source and
sink, high thermal stability, low viscosity, and minimal environmental
impact. Additionally, the fluid should exhibit a high molecular weight
and density, which contribute to higher cycle efficiency and lower
volumetric flow rates.

Evaluating potential working fluids involves a comprehensive analysis of
their thermophysical properties and compatibility with system
components. Fluids such as refrigerants, hydrocarbons, and siloxanes are
commonly considered due to their varied boiling points and thermal
properties. Moreover, the environmental and safety considerations, such
as global warming potential (GWP) and flammability, are integral to the
selection process.

In summary, the ORC's adaptability to low-temperature heat sources and
the judicious choice of working fluid renders it a versatile and
sustainable option for enhancing energy efficiency and mitigating waste.
Continued research and development in this field aim to refine fluid
selection criteria and expand the applicability of ORC technology across
various industrial sectors.

Abbas et al. \[1\] experimentally examined a cascaded two-Organic
Rankine Cycle (ORC) system across various temperatures and pressures to
optimize performance. Cyclopentane was used in the high-temperature (HT)
cycle, while pentane, butane, and propane were tested in the
low-temperature (LT) cycle. Results highlighted that pentane maximized
heat transfer, absorbing 23 kW, but most heat from the HT cycle was not
transferred to the LT cycle.

Yu et al. \[2\] focuses on optimizing the design and operation of a
solar energy-driven ORC system utilizing a parabolic trough collector
and a two-tank sensible thermal energy storage system. Results showed
that a recuperative ORC significantly outperforms a basic ORC, with
toluene emerging as the best working fluid despite vacuum condensation
issues.

Abbas et al. \[3\] explored the thermal efficiency of a Cascaded
Dual-Organic Rankine Cycle (CD-ORC) system using alkanes and low-GWP
refrigerants through simulations with EBSILON@Professional. The analysis
revealed that thermal efficiency in the HT-ORC is influenced by the
critical temperature, molecular mass, and critical pressure of the
working fluids, with cyclic alkanes like cyclohexane showing superior
performance. In the LT-ORC, refrigerants with high critical
temperatures, such as R1366mzz(Z) and R1233zd(E), achieved the highest
efficiency. The CD-ORC system demonstrated a potential 25% efficiency
improvement over regular ORC systems.

<img src="media/image1.png" style="width:2.97376in;height:1.96835in" />

Figure 1. Rankine cycle for Config. A \[4\]

In the following, the thermodynamic modeling of the ORC (Organic Rankine
Cycle) is examined. To model this cycle using various assumptions, three
different approaches for the thermodynamic simulation of the cycle
showen in Figure 1.

# Configuration A – Approach 1

To model the thermodynamics of Figure 1 using Approach 1, which is based
on obtaining the enthalpy of different streams, assumptions include: the
turbine outlet pressure is 1 bar, zero pressure drop for equipment, a
minimum temperature approach of 5°C for cycle heat exchangers, an
evaporator outlet temperature of 165°C, purity of each stream, condenser
outlet temperature slightly less than the boiling point of the
substance, a 1°C temperature increase across the pump, 75% pump
efficiency, 80% turbine isentropic efficiency, 95% electric motor
efficiency, and operational constraints such as the turbine inlet being
fully vapor and the turbine outlet having a steam quality that can
decrease to 90% as mentioned in \[2\]. The specifications of the hot
water flow rate are given in Table 1.

Table 1. Waste Water property

| Parameter   | Value      |
|-------------|------------|
| Pressure    | 10 bara    |
| Temperature | 170 °C     |
| Flowrate    | 100 kg/s   |
| Composition | Pure Water |

To determine the enthalpy of each stream, Equation 1 is used. The actual
enthalpy of each stream includes three to four parameters: the ideal gas
enthalpy, the residual enthalpy indicating the deviation from the ideal
state, the formation enthalpy which is a constant value for the
substance, and if the substance is in the liquid phase, the enthalpy of
vaporization should be added to the actual enthalpy.

$$H^{real} = H^{ig} + H^{res} + H^{form} + H^{vap}\ \ \ \ \ \ eq.1$$

If the stream is two-phase, Equation 2 must be used, which calculates
the enthalpy for saturated vapor and liquid, and then the vapor fraction
of the stream is inserted into the equation to obtain the actual
enthalpy.

$H = vap.\ frac*H^{Sat.vap} + (1 - vap.\ frac)*H^{Sat.liq}\ \ eq.2$

To calculate the ideal gas enthalpy of a stream, Equation 3 is used.
Coefficients a to f are read from the Aspen HYSYS software, and by
inputting the temperature in Kelvin into Equation 3, the ideal gas
enthalpy (Kj / Kg) is obtained.

$$H^{ig} = a + bT + cT^{2} + {dT}^{3} + {eT}^{4} + {fT}^{5}\ \ \ \ \ eq.3$$

To calculate the second parameter in Equation 1, the residual enthalpy,
existing EOS[^1] are used. Considering the problem's requirements, the
PR[^2] equation of state is chosen. Using the relations provided in
\[5\], presented as Equations 4 to 12, the desired parameter is
calculated. To solve the cubic equation in Equation 5, the Kamath method
is used.

$H^{Res} = RT\left( Z - 1 - \frac{A}{B\sqrt{8}}\left( 1 + \frac{m\sqrt{T_{r}}}{\sqrt{\alpha}} \right)\ln\left\lbrack \frac{Z + \left( 1 + \sqrt{2} \right)B}{Z + \left( 1 - \sqrt{2} \right)B} \right\rbrack \right)\ \ \ \ $eq.4

$Z^{3} - (1 - B)Z^{2} + \left( A - 2B - 3B^{2} \right)Z - \left( AB - B^{2} - B^{3} \right)$
eq.5

$T_{r} = \frac{T}{T_{c}}$ eq.6

$\alpha = \ \left\lbrack 1 + m\left( 1 - {T_{r}}^{0.5} \right) \right\rbrack^{2}$
eq.7

$m = 0.375 + 1.54\omega - 0.27\omega^{2}$ eq.8

$a = 0.457235\ \frac{R^{2}T_{C}^{2}}{P_{C}}*\ \alpha$ eq.9

$b = 0.077796\ \frac{RT_{c}}{P_{C}}$ eq.10

$A = \frac{aP}{(RT)^{2}}$ eq.11

$B = \frac{bP}{RT}$ eq.12

Assuming the purity of each stream, by substituting either the
temperature or pressure of a stream, other parameters of that stream,
such as the fugacity coefficient (Equations 13 & 14) or the
compressibility factor, can be calculated.

$for\ pure\ system \rightarrow \ \varphi^{v} = \varphi^{l}$ eq.13

$\ln(\varphi) = (z - 1) - \ln(z - B) + \frac{A}{2B\sqrt{2}}\ln\left( \frac{z + \left( 1 - \sqrt{2} \right)B}{z + \left( 1 + \sqrt{2} \right)B} \right)$
eq.14

To find the molar flow rate of the pure component in the cycle, Equation
15 is used, which determines the molar flow rate of the component by
balancing the energy in the cycle's evaporator.

$$\dot{n}\left( H_{1} - H_{4} \right) = \ {\dot{m}}_{w}C_{p,w}(\mathrm{\Delta}T - 5)\ \ \ \ \ \ \ eq.15$$

Subsequently, the thermodynamic parameters of the mentioned cycle are
calculated, and the pump's required work is determined using Equation 16
& 17. Finally, the turbine's generated work is calculated using Equation
18.

$$\mathrm{\Delta}H_{pump} = \ \frac{\left( P_{4} - P_{3} \right)*\dot{n}*MW}{density}\ \ \ \ \ \ \ \ eq.16$$

$$W_{pump} = \ \frac{\mathrm{\Delta}H_{pump}}{\eta_{pump}}\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ eq.17$$

$$W_{turbine} = \ \dot{n}\left( H_{1} - H_{2} \right)\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ eq.18$$

To select among the 74 components listed in the provided Excel file, two
constraints are applied: the condenser outlet temperature must be at
least 30°C, and the selected component must have a boiling point lower
than water. By applying these constraints, 15 components listed in Table
2 are identified as candidates for the best substance for this cycle.

Table 2. Candidates for best component

| Working Fluid      |           |           |
|--------------------|-----------|-----------|
| 2,2-dimethylbutane | FC72      | R113      |
| 4-methyl-2-pentene | Isohexane | Benzene   |
| Acetone            | Methanol  | Ethanol   |
| Cyclopentane       | n-hexane  | n-heptane |
| Dichloromethane    | n-pentane | R141b     |

In this approach, five components - dichloromethane, FC-72, methanol,
n-heptane, and R-113 - are selected.

# Configuration A – Approach 2

In Approach 2, similar to the previous case, the mentioned relations and
assumptions are used, with the difference that the turbine outlet is
assumed to be saturated vapor at 1 bar pressure, ensuring no liquid
forms inside the turbine. Therefore, only the vapor enthalpy is used,
resulting in reduced generated work. The same components as in Approach
1 are used in Approach 2.

# Configuration A – Approach 3

In Approach 3, the general relations of the previous two approaches are
used, with the difference that since only dichloromethane converts to
approximately 94% liquid, and the other components remain in their
gaseous state, the vapor fraction of this component is included in the
equations. Additionally, using Equation 19 \[6\], the turbine outlet
temperature is calculated considering the pressure drop and the K value,
which equals $C_{p}/C_{v}$ of the component in the ideal state, and the
turbine's isentropic efficiency equal to 80%. The components used in the
Approach 3 are the same as those in the previous two approaches.

$$\eta_{turbine} = \frac{1 - \frac{T_{2}}{T_{1}}}{1 - \pi_{i}^{\frac{1 - k}{k}}}\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ eq.19$$

# Configuration B

In the Bonus section of this project, the performance comparison among
five components - isohexane, FC-72, R-113, dichloromethane, and R-141b -
is conducted. This section follows the structure shown in Figure 2.

<img src="media/image2.png" style="width:2.30844in;height:1.90067in" />

Figure 2. Configuration B\[4\]

The assumptions used in this section are similar to those of Approach 3
in Configuation 1, with the difference that the pump outlet temperature
is considered to be 304.15 K to maintain the 5°C approach temperature
for the middle heat exchanger in Figure 2. With this assumption, the
minimum approach temperature for all candidate components is met. Also,
the UA values are derived from \[7\] considering the water-organic fluid
type, and the required area for the cycle's evaporator is determined and
substituted into the equations. In this section, similar to the previous
sections, the primary task is to calculate the actual enthalpy of the
cycle streams, assuming the turbine inlet stream is at 165°C and in the
saturated vapor state. By calculating the enthalpy of streams 1, 6, 2,
5, and 4 and using two additional relations compared to the previous
approaches, 20, 21 and 22, the turbine work, cycle work, and all
required parameters are determined and calculated.

$$H_{6} - H_{5} = H_{3} - H_{2}\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ eq.20$$

$$U*A*f*LMTD = \ {\dot{m}}_{w}C_{p,w}(\mathrm{\Delta}T)\ \ \ \ \ \ \ eq.21$$

$LMTD = \ \frac{\left( T_{in,waste} - T_{1} \right) - \left( T_{out,waste} - T_{6} \right)}{\ln\frac{\left( T_{in,waste} - T_{1} \right)}{\left( T_{out,waste} - T_{6} \right)}}\ \ \ \ \ \ \ \ \ \ \ \ \ $eq.22

# Results & discussion 

The results obtained from configuration A- Approach 1 are presented in
Table 3. Comparing these results with the simulations conducted in Aspen
HYSYS, it is observed that FC72, with a net work production of 21296 kW,
exhibits the highest work output among the candidate components listed
in Table 2. Table 3 also highlights the differences between the results
obtained from the model in GAMS software and the simulation results from
Aspen HYSYS. It is evident that the modeling results closely match the
HYSYS simulation outcomes, with an average error percentage of 0.32%,
showing the results verified and acceptable.

Table 3. Config.A approach 1 Results

| Spec                     | Model    | HYSYS    | Error % |
|--------------------------|----------|----------|---------|
| W<sub>pump</sub> (KW)    | 311.66   | 312.4    | 0.24%   |
| W<sub>turbine</sub> (KW) | 22639.9  | 22616    | 0.11%   |
| 𝑛 ̇(mole/s)               | 0.8202   | 0.8212   | 0.12%   |
| P1 (bar)                 | 13.65    | 13.657   | 0.05%   |
| T2 (K)                   | 332.7    | 332.9    | 0.06%   |
| T4 (K)                   | 330      | 329.9    | 0.03%   |
| H1 (Kj/Kmol)             | -2932254 | -2932305 | 0.00%   |
| H2 (Kj/Kmol)             | -2959858 | -2959825 | 0.00%   |
| H4 (Kj/Kmol)             | -2986405 | -2986691 | 0.01%   |
| Z factor 1               | 0.5007   | 0.5004   | 0.06%   |
| Z factor liq 2           | 0.0084   | 0.00821  | 2.32%   |
| Z factor Vap 2           | 0.9367   | 0.9367   | 0.00%   |
| Z factor 4               | 0.1131   | 0.1117   | 1.25%   |

Additionally, the results for the other two approaches are presented in
Tables 4 and 5. Approach 2 achieves an average error percentage of
0.35%, and Approach 3 has an average error percentage of 0.57%, both
yielding reliable and valid results.

Table 4. Config.A approach 2 Results

| Spec                     | Model    | HYSYS      | Error % |
|--------------------------|----------|------------|---------|
| W<sub>pump</sub> (KW)    | 311.54   | 312.4      | 0.28%   |
| W<sub>turbine</sub> (KW) | 20290.6  | 20255      | 0.18%   |
| 𝑛 ̇(mole/s)               | 0.8202   | 0.8218     | 0.19%   |
| P1 (bar)                 | 13.65    | 13.657     | 0.05%   |
| T2 (K)                   | 332.4    | 332.9      | 0.15%   |
| T4 (K)                   | 330      | 329.9      | 0.03%   |
| H1 (Kj/Kmol)             | -2932254 | -2932304.7 | 0.00%   |
| H2 (Kj/Kmol)             | -2956995 | -2956943.3 | 0.00%   |
| H4 (Kj/Kmol)             | -2986405 | -2986691.3 | 0.01%   |
| Z factor 1               | 0.5007   | 0.5004     | 0.06%   |
| Z factor liq 2           | 0.0084   | 0.00821    | 2.32%   |
| Z factor Vap 2           | 0.9367   | 0.9367054  | 0.00%   |
| Z factor 4               | 0.1131   | 0.1117     | 1.25%   |

Consequently, in the modeling of Approach 2, FC72 is identified as the
selected component with a net work production of 18964 kW. However, in
Approach 3, given the assumptions made, dichloromethane is determined to
be the selected component with a net work production of 8029 kW. The
comparison of the results from Approaches 1 and 2 confirms that
components with higher molecular weight and density exhibit superior
performance in the Rankine cycle. Furthermore, the results from Approach
3 indicate that components with a vapor fraction less than one, or at
their saturation point, perform better in the Rankine cycle compared to
their superheated state.

Table 5. Config.A approach 3 Results

| Spec                     | Model   | HYSYS    | Error % |
|--------------------------|---------|----------|---------|
| W<sub>pump</sub> (KW)    | 240.62  | 242.6    | 0.82%   |
| W<sub>turbine</sub> (KW) | 8705.6  | 8695     | 0.12%   |
| 𝑛 ̇(mole/s)               | 1.3937  | 1.389    | 0.34%   |
| P1 (bar)                 | 20.97   | 20.95    | 0.10%   |
| T2 (K)                   | 312.88  | 312.4    | 0.15%   |
| T4 (K)                   | 314     | 313.1    | 0.29%   |
| H1 (Kj/Kmol)             | -90083  | -90100.7 | 0.02%   |
| H2 (Kj/Kmol)             | -96330  | -96359.9 | 0.03%   |
| H4 (Kj/Kmol)             | -121951 | -122277  | 0.27%   |
| Z factor 1               | 0.7546  | 0.7549   | 0.04%   |
| Z factor liq 2           | 0.0026  | 0.00253  | 2.81%   |
| Z factor Vap 2           | 0.9753  | 0.975241 | 0.01%   |
| Z factor 4               | 0.0541  | 5.28E-02 | 2.46%   |

In examining the results for Configuration B, presented in Table 6, it
is observed that R141b, with a net work production of 8463 kW,
outperforms the other candidates listed in Table 2. Comparing the
selected component in Approach 3 of Configuration A with the results
obtained in Configuration B reveals that dichloromethane in
Configuration A performs better than R141b, placing R141b as the
second-best component. However, in Configuration B, the positions of
these two components are reversed. The reason for this is that
dichloromethane exits the turbine at its saturated vapor temperature,
while R141b exits in a superheated state, allowing for thermal exchange
with the pump's discharge stream.

Table 6. Config.B Results

| Spec                     | Model    | HYSYS   | Error % |
|--------------------------|----------|---------|---------|
| 𝑛 ̇(mole/s)               | 1.3976   | 1.392   | 0.40%   |
| P1 (bar)                 | 23.4233  | 23.44   | 0.07%   |
| Z factor 2               | 0.9752   | 0.9751  | 0.01%   |
| T2 (K)                   | 334.5349 | 333.8   | 0.22%   |
| T5 (K)                   | 304.15   | 304.6   | 0.15%   |
| Z factor 5               | 0.0826   | 0.0886  | 6.73%   |
| T4 (K)                   | 303.15   | 303.1   | 0.02%   |
| Z factor 4               | 0.0036   | 0.0038  | 5.34%   |
| T6 (K)                   | 328.7977 | 328.8   | 0.00%   |
| H1 (Kj/Kmol)             | -329923  | -329948 | 0.01%   |
| Z factor 1               | 0.6537   | 0.6535  | 0.03%   |
| H6 (Kj/Kmol)             | -361905  | -362069 | 0.05%   |
| Z factor 6               | 0.0796   | 0.0853  | 6.73%   |
| H2 (Kj/Kmol)             | -336599  | -336669 | 0.02%   |
| H5 (Kj/Kmol)             | -365133  | -365242 | 0.03%   |
| H4 (Kj/Kmol)             | -362815  | -365529 | 0.74%   |
| H3 (Kj/Kmol)             | -333371  | -339842 | 1.90%   |
| W<sub>pump</sub> (KW)    | 400.54   | 399.1   | 0.36%   |
| W<sub>turbine</sub> (KW) | 9330.12  | 9351    | 0.22%   |

# Conclusion

The performance evaluation of different working fluids in ORC systems
reveals significant insights into optimizing energy efficiency. The
experimental studies and simulations demonstrate that the selection of
appropriate working fluids, such as cyclopentane, FC-72, and
dichloromethane, is crucial for maximizing the efficiency of ORC
configurations. The findings show that FC-72 consistently achieved the
highest net work output across different approaches, emphasizing the
importance of molecular weight and density in fluid performance. The
comparison between various configurations also highlights that fluids
exiting the turbine in a saturated vapor state perform better than those
in a superheated state, due to enhanced thermal exchange capabilities.

References

\[1\] : Wammedh Khider Abbas, Experimental Study of two cascade.., 2021.

\[2\] : Haoshui Yu, Optimal design and operation, 2021.

\[3\] : Wammedh Khider Abbas, Cascaded dual-loop organic… , 2021.

\[4\] : Palma-Flores, O., Flores-Tlacuahuac, A., & Canseco-Melchor, G.
(2015)

\[5\] : Lee, computional method in chemical eng, 2019.

\[6\] : stlukes-glenrothes.org

\[7\] : biegler & grossmann, systematic methods, 1997.

[^1]: Equations of State

[^2]: Peng Robinson
