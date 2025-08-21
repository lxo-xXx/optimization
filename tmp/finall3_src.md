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
industrial processes. [1]A significant portion of the input energy in
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
...

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

نتایج کد قسمت B: جدول HYSYS قسمت 2 (از p.xlsx) ذکر شود. مدلسازی GAMS به دلیل حدس‌های اولیه و شرایط مرزی همگرا نشد.

2.  **Conclusions**

References

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