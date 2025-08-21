# ایرادات و پیشنهادهای اصلاح برای MMMMMM.gms (FA/EN)

## بخش فارسی (FA)

در این بخش، مهم‌ترین ایرادات کد `MMMMMM.gms` و راهکارهای پیشنهادی برای هر مورد ارائه شده‌اند. ارجاع‌های داخل پرانتز به شماره معادله‌ها/روابط در فایل شما اشاره دارند.

- کار توربین اشتباه (e45.. w_turbine = molar_flow*(H1 − H2))
  - ایراد: کار توربین باید بر اساس اختلاف آنتالپی بین ورودی و خروجی توربین باشد (H3 − H4)، نه بین خروجی کندانسور و خروجی پمپ (H1 − H2).
  - راهکار: جایگزینی با w_turbine = molar_flow*(H3 − H4) و اعمال راندمان توربین: w_turbine = η_turb·molar_flow·(H3 − H4).

- موازنه حرارتی تبخیرکننده اشتباه (e42.. molar_flow*(H1 − H4) = ...)
  - ایراد: گرمای جذب‌شده در اواپراتور باید ṁ_wf·(H3 − H2) باشد. استفاده از (H1 − H4) متعلق به مسیر کندانسور است.
  - راهکار: تصحیح به molar_flow*(H3 − H2) = m_waste*Cpw*(Tin_waste − Tout_waste) و اعمال قیود مجزا برای پینچ/اَپروچ؛ از جای‌گذاری “−5” داخل موازنه اجتناب شود.

- فشار جریان ۴ اشتباه در روابط PR (e33–e34 برای stream 4)
  - ایراد: برای جریان ۴ (خروجی توربین) فشار باید فشار پایین (P4) باشد، ولی از P1 استفاده شده است.
  - راهکار: تعریف P4 = P_low و جایگزینی P1 با P4 در cap_a_4 و cap_b_4.

- انتخاب ریشه Z نامتناسب با فاز (e4 و e29)
  - ایراد: در جریان ۱ (مایع)، باقیمانده آنتالپی با Z_v1 محاسبه شده است؛ باید از Z_l1 استفاده شود. در جریان ۴ (بخار)، از Z_l4 استفاده شده که باید Z_v4 باشد.
  - راهکار: جایگزینی Z مناسب با فاز هر جریان: (stream 1 → Z_l1)، (stream 4 → Z_v4).

- رابطه غیر فیزیکی برای T4 (e41.. T4 = Tb + 1)
  - ایراد: تنظیم دمای خروجی توربین بر اساس نقطه جوش نرمال سیال (Tb) صحیح نیست.
  - راهکار: تعیین T4 از طریق روابط ایزنتروپیک/انرژی (یا قید اشباع/سوپرهیت حداقلی) و حذف وابستگی به Tb.

- اعمال‌نشدن راندمان توربین (η_turb)
  - ایراد: علی‌رغم تعریف، η_turb در معادله کار توربین اعمال نشده است.
  - راهکار: اعمال η_turb در کار توربین (یا استفاده از روابط T4s/T4).

- محدودیت بخارکیفیت (steam_quality) ناقص
  - ایراد: کران‌های steam_quality کامنت شده‌اند؛ فقط مثبت بودن کافی نیست و می‌تواند >1 شود.
  - راهکار: اعمال 0 ≤ steam_quality ≤ 1 و پیوند آن با شاخص‌های فازی (مثلاً steam_quality ≈ V_2).

- استفاده از چگالی ثابت در پمپ و نام‌گذاری گمراه‌کننده (e43–e44)
  - ایراد: استفاده از density ثابت از جدول برای محاسبه توان پمپ دقیق نیست و متغیر deltah_pump در واقع توان را نشان می‌دهد.
  - راهکار: یا محاسبه Δh_pump ویژه (kJ/kg) و سپس W_pump = ṁ·Δh/η، یا تغییر نام به W_pump_raw و استفاده از ΔP بر حسب Pa (1 bar = 1e5 Pa) برای یکسان‌سازی واحدها.

- ناسازگاری واحدها در آنتالپی (ضرب بر MW به‌جای تقسیم)
  - ایراد: ترم‌های H_ideal از پلی‌نوم Cp(T) معمولاً بر حسب kJ/kmol به‌دست می‌آیند؛ برای تبدیل به kJ/kg باید تقسیم بر MW شود، نه ضرب در MW (e1,e27,e46).
  - راهکار: h = (H_ideal_kmol + h_form_kmol + H_res_kmol)/MW و اطمینان از هم‌واحدسازی hvap/hform.

- برابری فوگاسیتی در همه حالت‌ها (e26 و e69)
  - ایراد: φ_liq = φ_vap در جریان‌های ۱ و ۲ باعث تحمیل اشباع می‌شود؛ با فرض‌های زیرسرد/سوپرهیت ناسازگار است.
  - راهکار: فقط در نقاط اشباع از برابری فوگاسیتی استفاده شود یا به‌صورت شرطی/گزینشی اعمال شود.

- ساختار فشار و فقدان P4
  - ایراد: P2 و P3 ثابت 1 bar هستند، اما P4 تعریف نشده و در روابط stream 4 از P1 استفاده شده است.
  - راهکار: تعریف P4 و اعمال قیود ساختار فشار: P2 = P3 = P_low و P4 = P_low.

- جریمه Big‑M در تابع هدف (مقیاس‌بندی)
  - نکته: ρ = 100000 ممکن است در برابر W_net (kW) بسیار بزرگ باشد و عددی‌سازی را دشوار کند.
  - راهکار: تنظیم ρ متناسب با مقیاس توان (مثلاً 1e2–1e3) یا نرمال‌سازی متغیرهای باینری.

- تعبیه −5 K در موازنه منبع (e42)
  - ایراد: کاهش دما برای اَپروچ در موازنه منبع جای‌گذاری شده است.
  - راهکار: اعمال اَپروچ/پینچ به‌صورت قیود جدا (inequality) و حذف آن از موازنه انرژی.

---

## English (EN)

This section lists the key issues found in `MMMMMM.gms` and a recommended fix for each.

- Turbine work uses wrong states (e45.. w_turbine = molar_flow*(H1 − H2))
  - Issue: Turbine work must use (H3 − H4), not (H1 − H2).
  - Fix: Set w_turbine = molar_flow*(H3 − H4) and apply η_turb: w_turbine = η_turb·molar_flow·(H3 − H4).

- Evaporator energy balance uses wrong states (e42.. molar_flow*(H1 − H4) = ...)
  - Issue: Evaporator duty is ṁ_wf·(H3 − H2). Using (H1 − H4) corresponds to the condenser path.
  - Fix: Replace with molar_flow*(H3 − H2) = m_waste*Cpw*(Tin − Tout) and enforce pinch/approach via separate inequalities; avoid hard-coding “−5 K”.

- Wrong pressure for stream 4 PR parameters (e33–e34)
  - Issue: Stream 4 (turbine outlet) should use low pressure (P4), but P1 is used.
  - Fix: Define P4 = P_low and use P4 in cap_a_4 and cap_b_4.

- Inconsistent Z-root selection with phase (e4 and e29)
  - Issue: Stream 1 residual uses Z_v1 (should be liquid Z_l1). Stream 4 residual uses Z_l4 (should be vapor Z_v4).
  - Fix: Use Z consistent with phase: stream 1 → Z_l1; stream 4 → Z_v4.

- Non-physical turbine outlet temperature constraint (e41.. T4 = Tb + 1)
  - Issue: T4 tied to normal boiling temperature is not physical.
  - Fix: Determine T4 via isentropic/energy relations (or saturation/superheat constraints) and remove Tb dependency.

- Turbine efficiency not applied
  - Issue: η_turb is defined but not used in w_turbine.
  - Fix: Apply η_turb (or implement T4s/T4 isentropic equations).

- Steam quality bounds missing
  - Issue: steam_quality bounds are commented; variable can exceed 1 despite being positive.
  - Fix: Enforce 0 ≤ steam_quality ≤ 1 and link to phase indicators (e.g., steam_quality ≈ V_2).

- Constant density in pump and misleading naming (e43–e44)
  - Issue: Using a fixed density from the table is crude; variable name deltah_pump actually represents power.
  - Fix: Either compute specific Δh_pump [kJ/kg] and then W_pump = ṁ·Δh/η, or rename and use ΔP in Pa consistently (1 bar = 1e5 Pa).

- Enthalpy unit conversion error (multiplying by MW vs dividing)
  - Issue: H_ideal from Cp(T) polynomials is typically kJ/kmol; to get kJ/kg, divide by MW, not multiply (e1,e27,e46).
  - Fix: h = (H_ideal_kmol + h_form_kmol + H_res_kmol)/MW and ensure hvap/hform units are consistent.

- Unconditional fugacity equality (e26, e69)
  - Issue: φ_liq = φ_vap at streams 1 and 2 enforces saturation even when subcooled/superheated conditions are intended.
  - Fix: Use fugacity equality only at saturation points or apply conditionally.

- Pressure structure and missing P4
  - Issue: P2 and P3 are fixed at 1 bar, but P4 is not defined; stream 4 uses P1 incorrectly.
  - Fix: Define P4 and impose P2 = P3 = P_low and P4 = P_low.

- Big‑M penalty scaling in the objective
  - Note: ρ = 100000 may dwarf W_net (kW) and impair numerics.
  - Fix: Scale ρ to the power magnitude (e.g., 1e2–1e3) or normalize the binary terms.

- Hard-coding −5 K inside the source balance (e42)
  - Issue: Approach should be an external constraint, not embedded in the energy equation.
  - Fix: Move approach/pinch to separate inequalities; keep balances clean.

---

### Quick fix checklist
- [ ] Replace w_turbine and evaporator duty states
- [ ] Define P4 and use it in stream 4 PR parameters
- [ ] Use Z_l1 (stream 1) and Z_v4 (stream 4) in residual enthalpies
- [ ] Remove T4 = Tb + 1; implement isentropic/energy-based constraints
- [ ] Apply η_turb to turbine work
- [ ] Enforce 0 ≤ steam_quality ≤ 1 and link to phase indicators
- [ ] Rework pump power with consistent units (Pa) and/or specific enthalpy
- [ ] Correct MW conversion (divide, not multiply) and align hvap/hform units
- [ ] Make fugacity equality conditional (only at saturation)
- [ ] Move −5 K approach into constraints; keep balances physically clean