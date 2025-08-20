* ==================================================================================
* ORC MODEL (PURE-FLUID SELECTION, CONSISTENT UNITS, PR EOS, ISENTROPIC HANDLING)
* - Units: kJ/kg, kg/s, bar, K
* - Objective: maximize net power for Configuration A (simple); B optional
* - Fixes: R_spec, H_ideal per kg, consistent PR parameters, P structure, no spurious terms
* ==================================================================================

Set component / c1*c5 /, properties / Tc, Pc, omega, MW, Tb, rho, hform, hvap /, coeffs / a, b, c, d, e, f /;

Parameter prop(component,properties), cpcoef(component,coeffs);

* Example data (replace with your validated values)
$ondata
prop('c1','Tc') = 511.72 ; prop('c1','Pc') = 45.828 ; prop('c1','omega') = 0.192  ; prop('c1','MW')=70.13 ; prop('c1','Tb')=321.151 ; prop('c1','rho')=717.504 ; prop('c1','hform')=-77236.64 ; prop('c1','hvap')=27.29 ;
prop('c2','Tc') = 510.00 ; prop('c2','Pc') = 60.700 ; prop('c2','omega') = 0.199  ; prop('c2','MW')=84.93 ; prop('c2','Tb')=312.151 ; prop('c2','rho')=1293.882; prop('c2','hform')=-95400.00 ; prop('c2','hvap')=29.55 ;
prop('c3','Tc') = 469.65 ; prop('c3','Pc') = 33.640 ; prop('c3','omega') = 0.2539 ; prop('c3','MW')=72.15 ; prop('c3','Tb')=308.154 ; prop('c3','rho')=611.196 ; prop('c3','hform')=-146440.0 ; prop('c3','hvap')=27.40 ;
prop('c4','Tc') = 486.15 ; prop('c4','Pc') = 33.800 ; prop('c4','omega') = 0.245  ; prop('c4','MW')=187.38; prop('c4','Tb')=318.153 ; prop('c4','rho')=1519.32 ; prop('c4','hform')=-726800.0 ; prop('c4','hvap')=28.45 ;
prop('c5','Tc') = 477.50 ; prop('c5','Pc') = 42.140 ; prop('c5','omega') = 0.2211 ; prop('c5','MW')=116.95; prop('c5','Tb')=303.154 ; prop('c5','rho')=1221.277; prop('c5','hform')=-320950.0 ; prop('c5','hvap')=26.70 ;

cpcoef('c1','a')= 1.56197E-08 ; cpcoef('c1','b')=-0.764518   ; cpcoef('c1','c')= 0.00386825 ; cpcoef('c1','d')=-1.44055E-06 ; cpcoef('c1','e')= 2.31157E-10 ; cpcoef('c1','f')=-8.26099E-23 ;
cpcoef('c2','a')= 0.00000000 ; cpcoef('c2','b')= 0.15257    ; cpcoef('c2','c')= 0.000956096; cpcoef('c2','d')=-5.11287E-07 ; cpcoef('c2','e')= 1.23938E-10 ; cpcoef('c2','f')= 0.0        ;
cpcoef('c3','a')= 63.198    ; cpcoef('c3','b')=-0.0117017  ; cpcoef('c3','c')= 0.0033164  ; cpcoef('c3','d')=-1.1705E-06  ; cpcoef('c3','e')= 1.99636E-10 ; cpcoef('c3','f')=-8.66485E-15;
cpcoef('c4','a')= 0.0000000 ; cpcoef('c4','b')= 0.326199   ; cpcoef('c4','c')= 0.000766879; cpcoef('c4','d')=-4.30466E-07 ; cpcoef('c4','e')= 9.21086E-11 ; cpcoef('c4','f')= 0.0        ;
cpcoef('c5','a')= 0.0000000 ; cpcoef('c5','b')= 0.207743   ; cpcoef('c5','c')= 0.00112342 ; cpcoef('c5','d')=-5.30367E-07 ; cpcoef('c5','e')= 1.02107E-10 ; cpcoef('c5','f')= 0.0        ;
$offdata

* Source/sink and efficiencies
Scalar T_hw_in /443.15/, T_hw_out /343.15/, m_hot /100/, Cp_water /4.18/;
Scalar dT_pinch /5.0/, dT_approach /5.0/;
Scalar eta_pump /0.75/, eta_turb /0.80/, eta_gen /0.95/;

* Selection variables
Binary Variable y(component);
Equation one_fluid; one_fluid.. sum(component, y(component)) =e= 1;

* Selected properties
Scalar Tc, Pc, omega, MW, R_spec, hform, hvap;
Tc    = sum(component, y(component)*prop(component,'Tc'));
Pc    = sum(component, y(component)*prop(component,'Pc'));
omega = sum(component, y(component)*prop(component,'omega'));
MW    = sum(component, y(component)*prop(component,'MW'));
hform = sum(component, y(component)*prop(component,'hform'))/MW ;
hvap  = sum(component, y(component)*prop(component,'hvap')) ;
R_spec = 8.314 / MW ;

* Cp polynomials per kg
Parameter a_cp, b_cp, c_cp, d_cp, e_cp, f_cp;
a_cp = sum(component, y(component)*cpcoef(component,'a'))/MW;
b_cp = sum(component, y(component)*cpcoef(component,'b'))/MW;
c_cp = sum(component, y(component)*cpcoef(component,'c'))/MW;
d_cp = sum(component, y(component)*cpcoef(component,'d'))/MW;
e_cp = sum(component, y(component)*cpcoef(component,'e'))/MW;
f_cp = sum(component, y(component)*cpcoef(component,'f'))/MW;

* States 1..4 (simple cycle)
Set s /1*4/;

Variables T(s), P(s), Z(s), Z_v(s), Z_l(s), alpha(s), A_pr(s), B_pr(s), H_ideal(s), H_dep(s), H(s), cp(s), k_ratio(s);
Variable m_wf, Q_evap, W_turb, W_pump, W_net;

* Bounds and initials
T.lo('1')=300; T.up('1')=370;  T.l('1')=330;
T.lo('2')=300; T.up('2')=390;  T.l('2')=340;
T.lo('3')=360; T.up('3')=T_hw_in - dT_pinch; T.l('3')=400;
T.lo('4')=300; T.up('4')=420;  T.l('4')=340;
P.lo(s)=1.0; P.up(s)=0.75*Pc;  P.l('1')=5; P.l('2')=20; P.l('3')=20; P.l('4')=5;
m_wf.lo=1.0; m_wf.up=120.0;    m_wf.l=30;

Equations p_high, p_low, pinch, approach, alpha_eq(s), A_eq(s), B_eq(s), Zv_eq(s), Zl_eq(s), phase1,phase2,phase3,phase4,
          hideal_eq(s), hdep_eq(s), cp_eq(s), k_eq(s), evap_bal, turb_power, pump_power, source_cap, net_power;

p_high..    P('2') =e= P('3');
p_low..     P('1') =e= P('4');
pinch..     T('3') =l= T_hw_in - dT_pinch;
approach..  T('1') =g= 298.15 + dT_approach;

* PR alpha and parameters (R_bar in bar*m3/mol/K)
Scalar R_bar /8.314e-5/;
alpha_eq(s).. alpha(s) =e= sqr( 1 + (0.37464 + 1.54226*omega - 0.26992*sqr(omega)) * (1 - sqrt(T(s)/Tc)) );
A_eq(s)..     A_pr(s)  =e= 0.45724 * alpha(s) * P(s) / sqr(R_bar*T(s)/Tc);
B_eq(s)..     B_pr(s)  =e= 0.07780 * P(s) / (R_bar*T(s)/Tc);

Zv_eq(s)..    Z_v(s) =e= 1 + B_pr(s) + A_pr(s)*B_pr(s)/(3 + 2*B_pr(s));
Zl_eq(s)..    Z_l(s) =e=     B_pr(s) + A_pr(s)*B_pr(s)/(2 + 3*B_pr(s));

phase1.. Z('1') =e= Z_l('1');
phase2.. Z('2') =e= Z_l('2');
phase3.. Z('3') =e= Z_v('3');
phase4.. Z('4') =e= Z_v('4');

* Ideal enthalpy per kg (reference 298.15 K)
hideal_eq(s).. H_ideal(s) =e= a_cp*(T(s)-298.15)
                            + b_cp*(sqr(T(s))-sqr(298.15))/2
                            + c_cp*(power(T(s),3)-power(298.15,3))/3
                            + d_cp*(power(T(s),4)-power(298.15,4))/4
                            + e_cp*(power(T(s),5)-power(298.15,5))/5
                            + f_cp*(power(T(s),6)-power(298.15,6))/6;

hdep_eq(s)..  H_dep(s)   =e= R_spec * T(s) * ( Z(s) - 1 );

cp_eq(s)..    cp(s)      =e= a_cp + b_cp*T(s) + c_cp*sqr(T(s)) + d_cp*power(T(s),3) + e_cp*power(T(s),4) + f_cp*power(T(s),5);
k_eq(s)..     k_ratio(s) =e= cp(s) / ( cp(s) - R_spec + 1e-6 );

* Total enthalpy
Equation h_total(s); h_total(s).. H(s) =e= H_ideal(s) + H_dep(s);

* Isentropic (engineering) for temperature targets
Equation T4_iso, T2_iso;
T4_iso.. T('4') =e= T('3') - eta_turb*( T('3') - T('3')*power(P('4')/P('3'), (k_ratio('3')-1)/k_ratio('3')) );
T2_iso.. T('2') =e= T('1') + ( T('1')*power(P('2')/P('1'), (k_ratio('1')-1)/k_ratio('1')) - T('1') )/eta_pump;

* Duties and powers
evap_bal..   Q_evap  =e= m_wf * ( H('3') - H('2') );
turb_power.. W_turb  =e= m_wf * ( H('3') - H('4') );
pump_power.. W_pump  =e= m_wf * ( H('2') - H('1') );
source_cap.. m_hot*Cp_water*(T_hw_in - T_hw_out) =g= Q_evap;
net_power..  W_net   =e= eta_gen * ( W_turb - W_pump );

Model ORC_A / one_fluid, p_high, p_low, pinch, approach, alpha_eq, A_eq, B_eq, Zv_eq, Zl_eq,
              phase1,phase2,phase3,phase4, hideal_eq, hdep_eq, cp_eq, k_eq, h_total, T4_iso, T2_iso,
              evap_bal, turb_power, pump_power, source_cap, net_power /;

* Initialize one fluid (optional):
y.l('c1') = 1; y.up(component)=1; y.lo(component)=0;

Option NLP = IPOPT; Option MINLP = DICOPT;
Solve ORC_A using MINLP maximizing W_net;

Display y.l, T.l, P.l, H.l, W_net.l, W_turb.l, W_pump.l, Q_evap.l;

