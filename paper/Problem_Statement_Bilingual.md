## بیان مسئله (Problem Statement)

::: {dir=rtl}
### بیان مسئله (فارسی)

این پژوهش به تبدیل بهینهٔ حرارت اتلافی با دمای پایین تا متوسط به برق با استفاده از چرخهٔ رانکین آلی (ORC) تحت قیود واقع‌بینانهٔ صنعتی می‌پردازد. منبع حرارت، جریان آبِ داغِ فرایندی با مشخصات اسمی زیر است: دمای ورودی 443.15 کلوین (170 °C)، دمای خروجی 343.15 کلوین (70 °C)، دبی جرمی 100 kg/s و فشار نزدیک به اتمسفر. دفع حرارت در کندانسورِ هوا-خنک با حداقل اختلاف دمای نزدیک‌شونده (Approach) 5 کلوین نسبت به محیط انجام می‌شود. دو پیکربندی ORC بر پایهٔ شرایط منبع/چاه حرارتی یکسان بررسی می‌شوند: (1) چرخهٔ ساده شامل اواپراتور، توربین، کندانسور و پمپ (پیکربندی A) و (2) چرخهٔ بازیاب (ریکوپراتوری) با یک مبدل حرارتی داخلی برای بازیافت حرارت خروجی توربین و پیش‌گرمایش سیال کاری قبل از اواپراتور (پیکربندی B).

فرمول‌بندی به‌صورت «معادله‌گرا» (Equation-Oriented) در GAMS انجام می‌شود؛ متغیرهای حالت (دما، فشار، آنتالپی) و جریان هم‌زمان با محاسبات خواص ترمودینامیکی به‌کمک معادلهٔ حالت پنگ–رابینسون (PR EOS) بهینه می‌شوند. برای انتخاب پایدار ریشهٔ بخار/مایع مکعبی و محاسبهٔ منظم توابع انحرافی، از رویهٔ سازگار با الگوریتم کامَث استفاده می‌گردد. انتخاب سیال کاری از پایگاه دادهٔ جامع (پیوست 1) با خواص بحرانی و ضرایب گرمای ویژهٔ ایده‌آل انجام می‌شود؛ سپس غربال‌گری ترمودینامیکی فضای جست‌وجو را محدود و انتخاب نهایی در بهینه‌سازی تعیین می‌شود.

- داده‌های ورودی:
  - منبع حرارت: آب داغ با Tin=443.15 K، Tout=343.15 K، ṁ=100 kg/s
  - چاه/عملکرد: کندانسور هوا-خنک؛ ΔT_approach=5 K؛ ΔT_pinch=5 K (در صورت عدم تغییر)
  - راندمان تجهیزات: η_pump, η_turbine، راندمان ژنراتور η_gen
  - خواص سیالات: Tc، Pc، ω، MW و چندجمله‌ای‌های Cp(T) از پیوست 1

- متغیرهای تصمیم:
  - دما و فشار نقاط چرخه T(s), P(s)
  - دبی جرمی سیال کاری ṁ_wf
  - آنتالپی‌های ویژه h(s) (مستخرج از PR EOS و توابع انحرافی)
  - بار ریکوپراتور و پینچ داخلی (در پیکربندی B)
  - هویت سیال کاری (انتخاب‌شده از پایگاه دادهٔ غربال‌شده)

- اهداف:
  - حالت پایه (تک‌هدفه): بیشینه‌سازی توان خالص W_net=η_gen (W_turb−W_pump)
  - حالت چندهدفه (اختیاری): بیشینه‌سازی J=W_net−λ_mass ṁ_wf−λ_press P_high−λ_env EnvPenalty(fluid)

- قیود:
  - موازنه‌های انرژی: اواپراتور Q_evap=ṁ_wf(h3−h2)، توربین W_turb=ṁ_wf η_turb(h3−h4)، پمپ W_pump=ṁ_wf(h2−h1)/η_pump، کندانسور ṁ_hot Cp,water (Tin−Tout)≥Q_evap، و موازنهٔ ریکوپراتور با حداقل پینچ داخلی (B)
  - قیود انتقال حرارت: T3≤Tin−ΔT_pinch و T1≥T_cond+ΔT_approach
  - ساختار فشار: P2=P3 (فشار بالا)، P1=P4 (فشار پایین) با حدود پایدار/واقعی
  - قیود ترمودینامیکی PR EOS: محاسبهٔ a(T), b، α(T)=[1+κ(1−√(T/Tc))]^2 (κ تابع ω)، انتخاب ریشهٔ فشردگی سازگار با فاز، محاسبهٔ آنتالپی انحرافی و اعمال سقف فشار بحرانی P_high≤α_pc Pc

- فرضیات:
  - حالت پایا؛ یک سیال کاری در هر اجرا؛ اتلافات گرمایی خارج از مبدل‌ها ناچیز؛ افت فشارها در تجهیزات منظور می‌شود
  - دقت PR EOS در دامنهٔ بهره‌برداری کافی است؛ H_ideal(T) از Cp(T) پیوست 1
  - شرایط محیط برای ارزیابی Approach ثابت فرض می‌شود

- خروجی‌ها و سنجه‌ها:
  - W_net، η_thermal، کار ویژه، ṁ_wf، سیال منتخب، فشارهای بالا/پایین، دماهای نقاط؛ در B: بار ریکوپراتور و پینچ داخلی

- دامنه و اعتبارسنجی:
  - مدل EO مرجع بهینه‌سازی است؛ در صورت نیاز، متغیرهای کلیدی تحت شرایط مرزی منطبق در Aspen HYSYS راستی‌آزمایی می‌شود.
:::

---

### Problem Statement (English)

This study addresses the optimal conversion of low‑ to medium‑grade waste heat into electricity using Organic Rankine Cycles (ORCs) under industrially realistic constraints. A single hot‑water stream serves as the heat source with the following nominal specifications: inlet temperature 443.15 K (170 °C), outlet temperature 343.15 K (70 °C), mass flow 100 kg/s, and near‑ambient pressure. Heat rejection is provided by an air‑cooled condenser operated with a minimum approach temperature of 5 K to ambient. Two ORC configurations are evaluated under identical source/sink conditions: (i) a simple cycle comprising evaporator, turbine, condenser, and pump (Configuration A), and (ii) a recuperated cycle that adds an internal heat exchanger to recover turbine exhaust heat upstream of the evaporator (Configuration B).

The problem is formulated in an equation‑oriented (EO) manner in GAMS. State variables (temperatures, pressures, enthalpies) and flow variables are optimized concurrently with thermodynamic property calculations evaluated by the Peng–Robinson (PR) equation of state. Kamath‑compatible cubic‑root handling is used to ensure robust liquid/vapor compressibility selection and stable departure‑function enthalpies. Working‑fluid candidates are drawn from a comprehensive database (Attachment 1) including critical properties and ideal‑gas heat‑capacity coefficients. A thermodynamic screening narrows the search space; final selection is determined by optimization.

Given data
- Heat source: water, Tin = 443.15 K, Tout = 343.15 K, ṁ = 100 kg/s
- Sink/operation: air‑cooled condenser; ΔT_approach = 5 K; evaporator pinch ΔT_pinch = 5 K (unless varied)
- Equipment efficiencies: η_pump, η_turbine; generator efficiency η_gen
- Fluid properties: Tc, Pc, acentric factor ω, molecular weight MW, Cp(T) polynomials (Attachment 1)

Decision variables
- State temperatures T(s) and pressures P(s)
- Working‑fluid mass flow ṁ_wf
- Specific enthalpies h(s) (implied via PR EOS + departure functions)
- Recuperator duty and internal pinch (Configuration B)
- Working‑fluid identity (selected from the screened database)

Objectives
- Baseline (single‑objective): maximize W_net = η_gen (W_turb − W_pump)
- Optional multi‑objective: maximize J = W_net − λ_mass ṁ_wf − λ_press P_high − λ_env EnvPenalty(fluid)

Constraints
- Energy balances: evaporator Q_evap = ṁ_wf (h3 − h2); turbine W_turb = ṁ_wf η_turb (h3 − h4); pump W_pump = ṁ_wf (h2 − h1) / η_pump; condenser duty bounded by source availability ṁ_hot Cp,water (Tin − Tout) ≥ Q_evap; recuperator (B) with a minimum internal pinch
- Heat‑transfer constraints: T3 ≤ Tin − ΔT_pinch; T1 ≥ T_cond + ΔT_approach
- Pressure structure: P2 = P3 (high), P1 = P4 (low); bounds consistent with fluid/equipment limits
- PR‑based feasibility: a(T), b, α(T) = [1 + κ(1 − √(T/Tc))]^2 with κ(ω); phase‑consistent Z selection; departure enthalpies; critical‑pressure cap P_high ≤ α_pc Pc

Assumptions
- Steady state; single working fluid per run; negligible heat losses outside modeled exchangers; pressure drops lumped into equipment
- PR EOS accuracy is adequate over the operating domain; H_ideal(T) from Attachment‑1 Cp(T)
- Ambient conditions are fixed for the condenser approach evaluation

Outputs and indicators
- W_net, thermal efficiency, specific work, ṁ_wf, selected fluid, high/low pressures, state temperatures; for B: recuperator duty and internal pinch

Scope and validation
- The EO model is the authoritative optimization formulation; where applicable, key variables and duties are cross‑checked in Aspen HYSYS under matched boundary conditions.

