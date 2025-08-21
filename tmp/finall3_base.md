M<sup>1</sup>, M<sup>2</sup> ,M<sup>3</sup>,M<sup>4</sup>,M<sup>5</sup>

<sup>1</sup>Student number : 40, Msc. Process Design in Chemical
Engineering , Sharif university of Technology

<sup>2</sup>Student number : 40, Msc. Process Design in Chemical
Engineering , Sharif university of Technology

<sup>3</sup>Student number : 40, Msc. Process Design in Chemical
Engineering , Sharif university of Technology

<sup>4</sup>Student number : 40, Msc. Process Design in Chemical
Engineering , Sharif university of Technology

<sup>5</sup>Student number : 40, Msc. Process Design in Chemical
Engineering , Sharif university of Technology

Abstract

The Organic Rankine Cycle (ORC) offers a promising solution for
converting low-grade heat into The Organic Rankine Cycle (ORC) is an
effective and innovative approach for converting low-grade heat into
electricity by utilizing organic fluids with suitable thermodynamic
properties. This study examines how different working fluids affect the
efficiency of the ORC across various configurations. Through a
combination of experimental testing and simulation, the research
identifies five fluids (Cyclopentane, Dichloromethane, n-Pentane, R113,
and R141b) as top performers under different operating conditions. The
findings clearly show that the choice of working fluid plays a vital
role in improving the overall performance of the ORC system.
Furthermore, this study highlights the importance of selecting the
appropriate fluid to maximize energy recovery and enhance system
reliability. The flexibility of ORC technology is emphasized,
demonstrating its potential as an efficient and adaptable solution for
reducing energy waste and optimizing resource utilization in industrial
applications. Ultimately, the results underline the significant benefits
of ORC in increasing energy efficiency and promoting sustainable energy
practices, paving the way for broader adoption of clean and
environmentally friendly power generation technologies.

*Keywords:* Rankine Cycle, GAMS, Fluid selection;

1.  **Introduction**

Growing concerns over energy security and environmental sustainability
underscore the need for efficient utilization of waste-heat streams in
industrial processes. \[1\]A significant portion of the input energy in
production systems is dissipated to the environment as unused thermal
energy, which not only leads to substantial energy losses but also
contributes to greenhouse-gas emissions. Among emerging waste-heat
recovery technologies, the Organic Rankine Cycle (ORC) has attracted
considerable attention due to its ability to operate with low- to
medium-temperature heat sources and its flexibility in employing organic
working fluids with low boiling points. These advantages enable ORCs to
be deployed across a wide range of applications, including geothermal,
solar, biomass, and industrial waste-heat recovery.

In recent years, research in this field has evolved from purely
thermodynamic analyses toward multi-objective optimization and hybrid
approaches. For instance, Palma-Flores et al. (2015; 2016) proposed
pioneering frameworks for assessing ORC working fluids by integrating
thermodynamic and economic perspectives, highlighting the importance of
coupling technical and cost evaluations\[2, 3\]. More recent studies
emphasize performance enhancement and environmental benefits: Oyekale et
al. (2020) demonstrated that employing siloxane mixtures in
solar–biomass ORC systems can significantly improve exergy efficiency
and reduce CO₂ emissions\[4\]. Similarly, Wang et al. (2024) developed a
multi-objective optimization framework that simultaneously accounts for
capital cost, thermal efficiency, and environmental performance, thereby
providing a roadmap for sustainable ORC design\[5\]. Furthermore, the
recent review by Damarseckin (2024) suggests that the future of ORCs
lies in their integration with smart-energy networks and renewable-based
hybrid systems\[6\].

Despite these advancements, several critical research gaps remain.
First, most investigations have focused on conceptual design and
thermodynamic modeling, whereas industrial-scale operational evaluation
has been underexplored. Second, many studies consider only a single
configuration, limiting systematic comparisons across different ORC
layouts. Third, there is a lack of integration between equation-based
mathematical optimization and process-simulation validation, which is
essential to bridge the gap between theory and practical deployment.

Motivated by these gaps, the present study addresses the design and
optimization of two ORC configurations—a basic cycle and a recuperated
cycle—by employing GAMS for mathematical optimization and Aspen HYSYS
for process validation. This integrated approach not only enhances
understanding of the interaction between working-fluid selection,
operating conditions, and cycle efficiency, but also provides a
practical roadmap for the industrial implementation of sustainable ORC
systems.

<img src="media/image1.png" style="width:2.97376in;height:1.96835in" />

Figure 1. Rankine cycle for Config. A \[4\]

In the following, the thermodynamic modeling of the ORC (Organic Rankine
Cycle) is examined. To model this cycle using various assumptions, three
different approaches for the thermodynamic simulation of the cycle
showen in Figure 1.

1.  **Problem statement**

> <span dir="rtl"></span>Our goal is to convert low- to medium-grade
> waste heat into electricity using an organic Rankine cycle (ORC) under
> realistic industrial constraints and formulate the optimization in an
> equation-oriented (EO) manner suitable for exact solutions.
>
> <span dir="rtl"></span>A single hot-water stream is the heat source.
> The sink is an air-cooled condenser. Two ORC configurations are
> analyzed under identical boundary conditions:
>
> • Configuration A (simple cycle): evaporator → turbine → condenser →
> pump
>
> • Configuration B (recuperated cycle): the simple cycle augmented with
> an internal heat exchanger (recuperator) that preheats the working
> fluid using turbine exhaust
>
> <span dir="rtl"></span>We consider a set of at least five pure working
> fluids drawn from the recommended list and literature. Thermophysical
> constants (Tc, Pc, omega, MW) are treated as known for each candidate.
> Heat‑capacity treatment follows the model: Cp(T) polynomials if
> available, otherwise a constant cp\_avg. The optimal fluid is selected
> within the optimization (or via a screen–then–solve protocol) while
> ensuring that only one pure fluid is active in each run.
>
> Thermophysical modeling<span dir="rtl">:</span> Property calculations
> use the Peng–Robinson (PR) equation of state. A stable cubic‑root
> selection consistent with liquid/vapor phases (Kamath‑compatible
> handling) provides compressibility Z and departure functions.
> Ideal‑gas enthalpy uses Cp(T) polynomials if present, otherwise a
> constant *C**p*<sub>*a**v**g*</sub>.
>
> It is assumed that the outlet flow from the evaporator is the lowest
> possible value considering the outlet water inlet outside 165°C and
> since stream 1 is the inlet to the turbine, we assume all the flow is
> vapor. Stream 2 is assumed to be the turbine outlet once and also the
> water pressure of stream 3 is assumed to be completely liquid with
> respect to the material point so that the inlet to the pump is
> completely liquid. The pressures of streams (1,4) and (2,3) are equal
> considering that we have pressure drops in the heat exchangers.
>
> For fair comparisons against flowsheet simulations, matched boundary
> conditions (source/sink), identical fluid identity and property
> package, and consistent unit systems are required. Differences in
> fluid choice, bounds, or property methods can materially change
> *W*<sub>*t**u**r**b*</sub> and *W*<sub>*n**e**t*</sub>.
>
> In this approach, five components -Cyclopentane, Dichloromethane,
> n-Pentane, R113, and R141b- are selected.

1.  **Problem formulation**

The given specifications are listed in Table 1.

Table 1. Source/sink and equipment data (nominal)

<table>
<colgroup>
<col style="width: 59%" />
<col style="width: 17%" />
<col style="width: 23%" />
</colgroup>
<thead>
<tr class="header">
<th>Item</th>
<th>Value</th>
<th>Units</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Hot-water pressure</td>
<td>10</td>
<td>bara</td>
</tr>
<tr class="even">
<td>Hot-water inlet temperature</td>
<td>443.15</td>
<td>K</td>
</tr>
<tr class="odd">
<td>Hot-water outlet temperature</td>
<td>343.15</td>
<td>K</td>
</tr>
<tr class="even">
<td>Hot-water mass flow</td>
<td>100</td>
<td>kg/s</td>
</tr>
<tr class="odd">
<td>Cooling air inlet temperature</td>
<td>298.15</td>
<td>K (25 °C)</td>
</tr>
<tr class="even">
<td>Water heat capacity</td>
<td>4.675</td>
<td>kJ/(kg*K)</td>
</tr>
<tr class="odd">
<td>Condenser approach</td>
<td>5</td>
<td>K</td>
</tr>
<tr class="even">
<td>Evaporator pinch</td>
<td>5</td>
<td>K</td>
</tr>
<tr class="odd">
<td>Pump isentropic efficiency</td>
<td>0.75</td>
<td>-</td>
</tr>
<tr class="even">
<td>Turbine isentropic efficiency</td>
<td>0.80</td>
<td>-</td>
</tr>
<tr class="odd">
<td>Generator efficiency</td>
<td>0.95</td>
<td>-</td>
</tr>
</tbody>
</table>

To determine the enthalpy of each stream, Equation 1 is used. The actual
enthalpy of each stream includes three to four parameters: the ideal gas
enthalpy, the residual enthalpy indicating the deviation from the ideal
state, the formation enthalpy which is a constant value for the
substance, and if the substance is in the liquid phase, the enthalpy of
vaporization should be added to the actual enthalpy.

*H*<sup>*r**e**a**l*</sup> = *H*<sup>*i**g*</sup> + *H*<sup>*r**e**s*</sup> + *H*<sup>*f**o**r**m*</sup> + *H*<sup>*v**a**p*</sup>      *e**q*.1

If the stream is two-phase, Equation 2 must be used, which calculates
the enthalpy for saturated vapor and liquid, and then the vapor fraction
of the stream is inserted into the equation to obtain the actual
enthalpy.

*H* = *v**a**p*. *f**r**a**c* \* *H*<sup>*S**a**t*.*v**a**p*</sup> + (1 − *v**a**p*. *f**r**a**c*) \* *H*<sup>*S**a**t*.*l**i**q*</sup>  *e**q*.2

To calculate the ideal gas enthalpy of a stream, Equation 3 is used.
Coefficients a to f are read from the Aspen HYSYS software, and by
inputting the temperature in Kelvin into Equation 3, the ideal gas
enthalpy (Kj / Kg) is obtained.

*H*<sup>*i**g*</sup> = *a* + *b**T* + *c**T*<sup>2</sup> + *d**T*<sup>3</sup> + *e**T*<sup>4</sup> + *f**T*<sup>5</sup>     *e**q*.3

To calculate the second parameter in Equation 1, the residual enthalpy,
existing EOS[1] are used. Considering the problem's requirements, the
PR[2] equation of state is chosen. Using the relations provided in
\[7\], presented as Equations 4 to 12, the desired parameter is
calculated. To solve the cubic equation in Equation 5, the Kamath method
is used.

$H^{Res} = RT\left( Z - 1 - \frac{A}{B\sqrt{8}}\left( 1 + \frac{m\sqrt{T\_{r}}}{\sqrt{\alpha}} \right)\ln\left\lbrack \frac{Z + \left( 1 + \sqrt{2} \right)B}{Z + \left( 1 - \sqrt{2} \right)B} \right\rbrack \right)\\\\\\\\$eq.4

*Z*<sup>3</sup> − (1 − *B*)*Z*<sup>2</sup> + (*A* − 2*B* − 3*B*<sup>2</sup>)*Z* − (*A**B* − *B*<sup>2</sup> − *B*<sup>3</sup>)
eq.5

$T\_{r} = \frac{T}{T\_{c}}$ eq.6

*α*= \[1 + *m*(1 − *T*<sub>*r*</sub><sup>0.5</sup>)\]<sup>2</sup> eq.7

*m* = 0.375 + 1.54*ω* − 0.27*ω*<sup>2</sup> eq.8

$a = 0.457235\\\frac{R^{2}T\_{C}^{2}}{P\_{C}}\*\\\alpha$ eq.9

$b = 0.077796\\\frac{RT\_{c}}{P\_{C}}$ eq.10

$A = \frac{aP}{(RT)^{2}}$ eq.11

$B = \frac{bP}{RT}$ eq.12

Assuming the purity of each stream, by substituting either the
temperature or pressure of a stream, other parameters of that stream,
such as the fugacity coefficient (Equations 13 & 14) or the
compressibility factor, can be calculated.

*f**o**r* *p**u**r**e* *s**y**s**t**e**m*→ *φ*<sup>*v*</sup> = *φ*<sup>*l*</sup>
eq.13

$\ln(\varphi) = (z - 1) - \ln(z - B) + \frac{A}{2B\sqrt{2}}\ln\left( \frac{z + \left( 1 - \sqrt{2} \right)B}{z + \left( 1 + \sqrt{2} \right)B} \right)$
eq.14

To find the molar flow rate of the pure component in the cycle, Equation
15 is used, which determines the molar flow rate of the component by
balancing the energy in the cycle's evaporator.

*ṅ*(*H*<sub>1</sub> − *H*<sub>4</sub>)= *ṁ*<sub>*w*</sub>*C*<sub>*p*, *w*</sub>(Δ*T* − 5)       *e**q*.15

Subsequently, the thermodynamic parameters of the mentioned cycle are
calculated, and the pump's required work is determined using Equation 16
& 17. Finally, the turbine's generated work is calculated using Equation
18.

$$\mathrm{\Delta}H\_{pump} = \\\frac{\left( P\_{4} - P\_{3} \right)\*\dot{n}\*MW}{density}\\\\\\\\\\\\\\\\eq.16$$

$$W\_{pump} = \\\frac{\mathrm{\Delta}H\_{pump}}{\eta\_{pump}}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\eq.17$$

*W*<sub>*t**u**r**b**i**n**e*</sub>= *ṅ*(*H*<sub>1</sub> − *H*<sub>2</sub>)               *e**q*.18

Given that the fluid at the turbine inlet must be steam and the heating
fluid is water, the boiling point of the selected fluid must be lower
than the boiling point of water (100 degrees Celsius).

Also, the fluid at the inlet of the flow pump 3 is completely liquid.
And given the cooling air temperature of 25 degrees, the best case
scenario is that the outlet from the cooler can be 30 degrees Celsius,
so fluids whose boiling points are higher than 30 degrees Celsius should
be selected.

Given these constraints, 16 fluids (table 2) were selected, of which
these three fluids (Actone, Ethanol, FC72) were also removed due to
their inappropriateness for the Ping-Robinson equations (due to the
warning of the Hysys software), and also the fluid (R124) can liquefy at
temperatures much lower than 30 degrees, and its boiling point is
probably incorrectly stated as 36.1 in the Excel file.

Table 2. Selected fluids.

<table>
<colgroup>
<col style="width: 15%" />
<col style="width: 53%" />
<col style="width: 30%" />
</colgroup>
<thead>
<tr class="header">
<th> </th>
<th>Name</th>
<th><span
class="math display"><em>T</em><sub><em>b</em></sub>@ 1 <em>b</em><em>a</em><em>r</em></span></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>1</td>
<td>2,2-dimethylbutane</td>
<td>49.73101</td>
</tr>
<tr class="even">
<td>2</td>
<td>4-methyl-2-pentene</td>
<td>58.58</td>
</tr>
<tr class="odd">
<td>3</td>
<td>Acetone</td>
<td>56.07</td>
</tr>
<tr class="even">
<td>4</td>
<td>Benzene</td>
<td>80.06</td>
</tr>
<tr class="odd">
<td>5</td>
<td>Cyclopentane</td>
<td>49.24801</td>
</tr>
<tr class="even">
<td>6</td>
<td>Dichloromethane</td>
<td>39.85</td>
</tr>
<tr class="odd">
<td>7</td>
<td>Ethanol</td>
<td>78.15</td>
</tr>
<tr class="even">
<td>8</td>
<td>FC72</td>
<td>55.9</td>
</tr>
<tr class="odd">
<td>9</td>
<td>Isohexane</td>
<td>60.11</td>
</tr>
<tr class="even">
<td>10</td>
<td>Methanol</td>
<td>64.54</td>
</tr>
<tr class="odd">
<td>11</td>
<td>n-heptane</td>
<td>97.9</td>
</tr>
<tr class="even">
<td>12</td>
<td>n-hexane</td>
<td>69.18</td>
</tr>
<tr class="odd">
<td>13</td>
<td>n-pentane</td>
<td>35.78</td>
</tr>
<tr class="even">
<td>14</td>
<td>R113</td>
<td>47.57</td>
</tr>
<tr class="odd">
<td>15</td>
<td>R124</td>
<td>36.1</td>
</tr>
<tr class="even">
<td>16</td>
<td>R141b</td>
<td>31.99999</td>
</tr>
</tbody>
</table>

1.  **Results and discution**

نتایج قسمت A

| Spec | Hysys | GAMS | Error% | توضیح |
|---|---:|---:|---:|---|
| Wt | 8699.537 | 44853.5 | -415.585 | Heat Flow [kJ/s] |
| Wp | 242.70688 | 242.803 | -0.0396 | Heat Flow [kJ/s] |
| Molar Flow | 1.3898043 | 1.39 | -0.01408 | [kgmole/s] |
| H1 | -90102.27 | -90025.2 | 0.085523 | Molar Enthalpy [kJ/kmole] |
| H2 | -96361.81 | -122292 | -26.9095 | Molar Enthalpy [kJ/kmole] |
| H4 | -122262.9 | -121975 | 0.235481 | Molar Enthalpy [kJ/kmole] |
| P1 | 20.959427 | 20.985 | -0.12201 | Pressure [bar] |
| T2 | 312.40593 | 312.409 | -0.00098 | Temperature [K] |
| T4 | 313.24878 | 313.151 | 0.031215 | Temperature [K] |

Here is the data from the spreadsheet in the image:

| Hysys | Name | Wp | Wt | Wnet(Kj/s) |
|---|---|---|---|---|
| 1 | 2,2-dimethylbutane | 258.134799 | 6839.564 | 5213.5163 |
| 2 | 4-methyl-2-pentene | 219.5780021 | 6365.124 | 4872.8213 |
| 3 | Acetone | 56.07 |  |  |
| 4 | Benzene | 92.17404287 | 5588.065 | 4378.2778 |
| 5 | Cyclopentane | 221.3920083 | 7617.756 | 5872.813 |
| 6 | Dichloromethane | 242.7068797 | 8699.537 | 6716.9227 |
| 7 | Ethanol | 78.47 |  |  |
| 8 | FC72 | 65.9 |  |  |
| 9 | Isohexane | 205.8012394 | 6114.503 | 4685.8008 |
| 10 | Methanol | 108.9162242 | 6929.143 | 5434.3979 |
| 11 | n-heptane | 71.80336678 | 3557.273 | 2774.0151 |
| 12 | n-hexane | 166.2908911 | 5674.165 | 4373.0408 |
| 13 | n-pentane | 344.476657 | 7579.137 | 5718.8307 |
| 14 | R113 | 278.818838 | 7197.7 | 5479.2284 |
| 15 | R124 | 36.6 |  |  |
| 16 | R141b | 362.5213291 | 8510.272 | 6445.6959 |

نتایج: با توجه به جواب مدلسازی، سیال انتخاب‌شده همان سیال HYSYS است؛ خطا در اکثر متغیرها مناسب است و فقط کار توربین و آنتالپی جریان ۲ نیاز به بهبود دارند.

نتیجه: با توجه به ۵ سیال انتخاب‌شده، سیالات با جرم مولکولی بزرگ‌تر W_net بزرگ‌تری ایجاد کرده‌اند؛ مطابق ادبیات (1,2).

1) Song C, Gu M, Miao Z, Liu C, Xu J. Effect of fluid dryness and critical temperature on trans-critical ORC. Energy 2019;174:97–109. https://doi.org/10.1016/j.energy.2019.02.171

2) Xu J, Yu C. Critical temperature criterion for selection of working fluids for subcritical ORC. Energy 2014;74:719–33. https://doi.org/10.1016/j.energy.2014.07.038

2.  **Conclutions**

References
[Appendix – Added Results (as requested)]

نتایج قسمت A

| Spec | Hysys | GAMS | Error% | توضیح |
|---|---:|---:|---:|---|
| Wt | 8699.537 | 44853.5 | -415.585 | Heat Flow [kJ/s] |
| Wp | 242.70688 | 242.803 | -0.0396 | Heat Flow [kJ/s] |
| Molar Flow | 1.3898043 | 1.39 | -0.01408 | [kgmole/s] |
| H1 | -90102.27 | -90025.2 | 0.085523 | Molar Enthalpy [kJ/kmole] |
| H2 | -96361.81 | -122292 | -26.9095 | Molar Enthalpy [kJ/kmole] |
| H4 | -122262.9 | -121975 | 0.235481 | Molar Enthalpy [kJ/kmole] |
| P1 | 20.959427 | 20.985 | -0.12201 | Pressure [bar] |
| T2 | 312.40593 | 312.409 | -0.00098 | Temperature [K] |
| T4 | 313.24878 | 313.151 | 0.031215 | Temperature [K] |

Here is the data from the spreadsheet in the image (Part A candidates):

| Hysys | Name | Wp | Wt | Wnet(Kj/s) |
|---|---|---|---|---|
| 1 | 2,2-dimethylbutane | 258.134799 | 6839.564 | 5213.5163 |
| 2 | 4-methyl-2-pentene | 219.5780021 | 6365.124 | 4872.8213 |
| 3 | Acetone | 56.07 |  |  |
| 4 | Benzene | 92.17404287 | 5588.065 | 4378.2778 |
| 5 | Cyclopentane | 221.3920083 | 7617.756 | 5872.813 |
| 6 | Dichloromethane | 242.7068797 | 8699.537 | 6716.9227 |
| 7 | Ethanol | 78.47 |  |  |
| 8 | FC72 | 65.9 |  |  |
| 9 | Isohexane | 205.8012394 | 6114.503 | 4685.8008 |
| 10 | Methanol | 108.9162242 | 6929.143 | 5434.3979 |
| 11 | n-heptane | 71.80336678 | 3557.273 | 2774.0151 |
| 12 | n-hexane | 166.2908911 | 5674.165 | 4373.0408 |
| 13 | n-pentane | 344.476657 | 7579.137 | 5718.8307 |
| 14 | R113 | 278.818838 | 7197.7 | 5479.2284 |
| 15 | R124 | 36.6 |  |  |
| 16 | R141b | 362.5213291 | 8510.272 | 6445.6959 |

نتایج: سیال انتخاب شده همان سیال HYSYS است؛ اغلب خطاها کوچک‌اند و فقط کار توربین و آنتالپی جریان ۲ انحراف دارند.

نتیجه: از بین ۵ سیال انتخابی، سیالات با جرم مولکولی بزرگ‌تر W_net بیشتری ایجاد کرده‌اند؛ مطابق ادبیات (1,2) درباره معیار دمای بحرانی.

1) Song C, Gu M, Miao Z, Liu C, Xu J. Energy 2019;174:97–109. https://doi.org/10.1016/j.energy.2019.02.171

2) Xu J, Yu C. Energy 2014;74:719–33. https://doi.org/10.1016/j.energy.2014.07.038

1.  
2.  
3.  
4.  
5.  
6.  
7.  
8.  

Miller, T., et al., *Waste Heat Utilization in Marine Energy Systems for
Enhanced Efficiency.* Energies, 2024. **17**(22): p. 5653.Palma-Flores,
O., A. Flores-Tlacuahuac, and G. Canseco-Melchorb, *Simultaneous
molecular and process design for waste heat recovery.* Energy, 2016.
**99**: p. 32-47.Canseco Melchor, G., O. Palma Flores, and A. Flores
Tlacuahuac, *Simultaneous molecular and process design for waste heat
recovery.* 2016.Oyekale, J., et al., *Impacts of renewable energy
resources on effectiveness of grid-integrated systems: Succinct review
of current challenges and potential solution strategies.* Energies,
2020. **13**(18): p. 4856.Zhang, S., et al., *Thermo-economic assessment
and multi-objective optimization of organic Rankine cycle driven by
solar energy and waste heat.* Energy, 2024. **290**: p.
130223.Damarseckin, S., et al., *A comparative review of ORC and R-ORC
technologies in terms of energy, exergy, and economic performance.*
Heliyon, 2024. **10**(23).Chung, Yongchul G., Emmanuel Haldoupis,
Benjamin J. Bucior, Maciej Haranczyk, Seulchan Lee, Hongda Zhang,
Konstantinos D. Vogiatzis et al. "Advances, updates, and analytics for
the computation-ready, experimental metal–organic framework database:
CoRE MOF 2019." *Journal of Chemical & Engineering Data* 64, no. 12
(2019): 5985-5998.

[1] Equations of State

[2] Peng Robinson
