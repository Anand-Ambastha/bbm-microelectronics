import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); FIG = os.path.join(ROOT, 'figures')
NAVY, TEAL, GREY, RED = RGBColor(0x14, 0x2B, 0x4D), RGBColor(0x0E, 0x8A, 0x8A), RGBColor(0x55, 0x5F, 0x6B), RGBColor(0xC0, 0x39, 0x2B)
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
blank = prs.slide_layouts[6]
def tb(sl, x, y, w, h, text, size=18, bold=False, color=GREY, align=None):
    s = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = s.text_frame; tf.word_wrap = True
    lines = text if isinstance(text, list) else [text]
    for i, l in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.space_after = Pt(6)
        r = p.add_run(); r.text = l; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = 'Calibri'
        if align: p.alignment = align
    return s
def slide(title, notes):
    sl = prs.slides.add_slide(blank)
    bar = sl.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(1.0)); bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
    tb(sl, 0.5, 0.18, 12.3, 0.7, title, 30, True, RGBColor(255, 255, 255))
    sl.notes_slide.notes_text_frame.text = notes
    tb(sl, 0.5, 7.05, 12.3, 0.35, 'Source: TI SN74AUP1G04 datasheet SCES571K (Rev. K). [DS] = datasheet value; [Calc] = student calculation.', 10, False, GREY)
    return sl
def table(sl, rows, x, y, w, colw, size=14):
    t = sl.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(0.4*len(rows))).table
    for j, cw in enumerate(colw): t.columns[j].width = Inches(cw)
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = t.cell(i, j); c.text = v or ' '; p = c.text_frame.paragraphs[0]; p.runs[0].font.size = Pt(size); p.runs[0].font.name = 'Calibri'; p.runs[0].font.bold = (i == 0)
            if i == 0: c.fill.solid(); c.fill.fore_color.rgb = TEAL; p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else: c.fill.solid(); c.fill.fore_color.rgb = RGBColor(0xF2, 0xF6, 0xF8) if i % 2 else RGBColor(255, 255, 255)

# 1
sl = slide('SN74AUP1G04, a low-power single inverter gate', 'TIME 0:00-0:35. Good morning. My case study is the Texas Instruments SN74AUP1G04, a single inverter gate from the AUP, Advanced Ultra-low-Power, logic family. It performs Y equals NOT A, but its value is in how little power it uses and how small it is. I checked every number against the manufacturer\'s datasheet, revision K, and I will mark datasheet values and my own calculations separately.')
tb(sl, 0.7, 1.5, 7.2, 3.5, ['Function: Y = A\u0305 (one inverter)', 'Family: TI AUP, battery-powered portable logic', 'Packages: SOT-23 (2.90 \u00d7 1.60 mm) down to X2SON 0.8 \u00d7 0.8 mm (0.64 mm\u00b2)', 'V_CC: 0.8 V to 3.6 V; 3.6 V-tolerant inputs/outputs', 'Status: ACTIVE (ti.com, Oct 2026)'], 20)
sl.shapes.add_picture(os.path.join(FIG, 'fig_cmos_inverter_generic.png'), Inches(8.6), Inches(1.4), height=Inches(4.3))
tb(sl, 8.4, 5.8, 4.5, 0.9, 'Generic CMOS inverter (illustrative, TI does not publish the internal netlist)', 12, False, GREY)
# 2
sl = slide('Supply range and power-related specifications', 'TIME 0:35-1:50. The device works from 0.8 to 3.6 volts. Static current is at most 0.9 microamps over temperature, 0.5 at 25 degrees. Input capacitance is 1.5 picofarads and the power dissipation capacitance Cpd is 3.9 picofarads up to 2.5 volts, 4.1 at 3.3 volts, measured at 10 megahertz. The I-off specification means that when VCC is zero the leakage stays below 0.6 microamps, which allows live insertion. My calculation: at 1.8 volts, 10 megahertz and a 5 picofarad load, dynamic power is Cpd plus CL times VCC squared times f, about 288 microwatts, while worst-case static power is under 2 microwatts. So dynamic power dominates whenever the gate toggles.')
table(sl, [['Parameter [DS]', 'Value', 'Conditions'],
 ['Recommended V_CC', '0.8, 3.6 V', 'abs. max 4.6 V'],
 ['I_CC (static)', '\u2264 0.5 \u00b5A (25 \u00b0C); \u2264 0.9 \u00b5A (\u221240\u201385 \u00b0C)', 'V_I = GND or V_CC, I_O = 0'],
 ['C_pd', '3.9 pF (\u2264 2.5 V); 4.1 pF (3.3 V)', 'f = 10 MHz, 25 \u00b0C'],
 ['C_i / C_o', '1.5 pF / 2.5 pF typ', ''],
 ['I_off', '\u2264 0.6 \u00b5A', 'V_CC = 0 V, V up to 3.6 V'],
 ['Drive (I_OH / I_OL)', '\u00b120 \u00b5A (0.8 V) \u2026 \u00b14 mA (3 V)', 'recommended conditions']], 0.5, 1.4, 12.3, [3.0, 5.3, 4.0], 15)
tb(sl, 0.5, 4.6, 12.3, 2.2, ['[Calc] P_dyn = (C_pd + C_L)\u00b7V_CC\u00b2\u00b7f = (3.9 + 5) pF \u00d7 1.8\u00b2 V\u00b2 \u00d7 10 MHz \u2248 288 \u00b5W', '[Calc] P_static,max = 0.9 \u00b5A \u00d7 1.8 V \u2248 1.6 \u00b5W  (< 1 % of P_dyn)', 'So: dynamic power dominates, reduce C_L, V_CC and activity.'], 18, False, NAVY)
# 3
sl = slide('Propagation delay and loading conditions', 'TIME 1:50-2:50. Delay depends on supply voltage and load. The datasheet test uses 5, 10, 15 and 30 picofarad loads including probe, a 1 megaohm resistor, a threshold of VCC over two, and inputs with edges of 3 nanoseconds or faster. At 1.8 volts and 25 degrees, typical delay is 3.4 nanoseconds with 5 picofarads and 6.3 with 30. At 3.3 volts it is 2.1 and 4.0. At 1.2 volts it is 5.9 with 5 picofarads, and at 0.8 volts the datasheet gives 15.6 nanoseconds. So you trade speed for low voltage. The headline number, 3.9 nanoseconds maximum at 3.3 volts, is the 5 picofarad, full-temperature maximum.')
sl.shapes.add_picture(os.path.join(FIG, 'fig_aup_tpd.png'), Inches(0.5), Inches(1.3), width=Inches(7.2))
table(sl, [['t_pd A\u2192Y [DS]', 'typ 25 \u00b0C', 'max \u221240\u201385 \u00b0C'], ['1.8 V, 5 pF', '3.4 ns', '7.0 ns'], ['1.8 V, 30 pF', '6.3 ns', '10.5 ns'], ['3.3 V, 5 pF', '2.1 ns', '3.9 ns'], ['1.2 V, 5 pF', '5.9 ns', '13.5 ns'], ['0.8 V, 5 pF', '15.6 ns*', '\u2013']], 8.0, 1.4, 4.9, [1.9, 1.4, 1.6], 13)
tb(sl, 8.0, 4.1, 4.9, 2.8, ['Test: C_L = 5/10/15/30 pF incl. probe, 1 M\u03a9, V_M = V_CC/2, t_r/t_f \u2264 3 ns, PRR \u2264 10 MHz.', '*single value listed at 0.8 V.'], 13)
# 4
sl = slide('Applications and engineering relevance', 'TIME 2:50-3:40. TI lists applications such as barcode scanners, blood-pressure monitors, field transmitters, wireless peripherals, NAS and server boards. A key use is level translation: because inputs tolerate 3.6 volts, the gate can bring 3.3 volt peripheral signals down to the 0.8 to 1.2 volt levels of new microcontrollers. For our microelectronics course it is a real example of low-power CMOS design: small capacitances, reduced drive and slower edges to limit overshoot, input hysteresis for slow inputs, and I-off protection. It also connects to my research-paper review: a normal CMOS inverter has a short moment when both transistors conduct, and the break-before-make technique removes that structurally; TI does not say the AUP gate uses it.')
tb(sl, 0.7, 1.4, 6.2, 5.4, ['Typical uses [DS]', '\u2022 Battery-powered portable / medical devices', '\u2022 Barcode scanners, field transmitters, HVAC', '\u2022 Wireless keyboards, mice, headsets', '\u2022 Down-translation 3.3 V \u2192 0.8\u20131.2 V (3.6 V-tolerant I/O)'], 20, False, NAVY)
tb(sl, 7.2, 1.4, 5.6, 5.4, ['Why it matters to ECC-305 [Expl]', '\u2022 Real low-power CMOS: small C_pd, low I_CC', '\u2022 Slow edges + low drive limit noise', '\u2022 Hysteresis tolerates slow inputs', '\u2022 Link to BBM: short-circuit current is part of dynamic power'], 20, False, TEAL)
# 5
sl = slide('Limitations and design trade-offs', 'TIME 3:40-4:35. The device is not fast: a few nanoseconds at 3.3 volts and tens at 0.8 volts, and the datasheet gives no maximum clock frequency. Output drive is small, 4 milliamps at 3 volts and 1.9 at 1.65 volts, so delay grows with load and it cannot drive LEDs or long lines. Inputs must not change slower than 200 nanoseconds per volt, and unused inputs must be tied. An input held between rails can draw up to 50 microamps at 3.3 volts. Absolute maximums are 4.6 volts supply and 20 milliamps on the output; ESD ratings are 2000 volts human body model. One discrepancy I found: the TI product page lists supply current max 10 microamps while the datasheet says 0.9; I used the datasheet.')
table(sl, [['Limitation [DS]', 'Value / consequence'], ['Speed', '3.2 ns max (25 °C) / 3.9 ns (−40–85 °C) @3.3 V, 5 pF; 13.5 ns max @1.2 V; no f_max given'], ['Drive', '\u00b14 mA @3 V, \u00b11.9 mA @1.65 V \u2192 delay grows with C_L'], ['Input edge rate', '\u2264 200 ns/V; unused inputs tied to V_CC/GND'], ['\u0394I_CC', 'up to 50 \u00b5A if V_I = V_CC \u2212 0.6 V (3.3 V)'], ['Abs. max', 'V_CC 4.6 V; I_O \u00b120 mA; 50 mA via V_CC/GND; ESD 2 kV HBM'], ['Spec discrepancy', 'Product page: I_CC max 10 \u00b5A vs datasheet 0.9 \u00b5A (datasheet used)']], 0.5, 1.4, 12.3, [2.6, 9.7], 16)
tb(sl, 0.5, 5.5, 12.3, 1.3, 'Trade-off: low power and tiny package vs speed and drive. For high drive or 5 V operation choose a different family (e.g. LVC).', 18, True, RED)
# 6
sl = slide('Summary and references', 'TIME 4:35-5:00. To summarise: the SN74AUP1G04 is a tiny, ultra-low-power inverter for 0.8 to 3.6 volt systems with under one microamp of static current, a few nanoseconds of delay at typical loads, and strong protection features, at the price of limited drive and speed. Dynamic power dominates, so loads and supply voltage are the design levers. All numbers come from the datasheet unless I marked them as my calculation. Thank you; I am happy to take questions.')
tb(sl, 0.7, 1.4, 12, 3, ['\u2022 Ultra-low static power (I_CC \u2264 0.9 \u00b5A) and 0.8\u20133.6 V operation', '\u2022 t_pd about 2\u20136 ns typ at 1.8\u20133.3 V and 5 pF; delay rises with load and falls with V_CC', '\u2022 Dynamic power dominates: P = (C_pd + C_L)\u00b7V_CC\u00b2\u00b7f', '\u2022 Limited drive/speed, choose by application'], 20, False, NAVY)
tb(sl, 0.7, 4.6, 12, 2.3, ['[1] Texas Instruments, SN74AUP1G04 Low-Power Single Inverter Gate, datasheet SCES571K, Rev. K (Jun 2014), https://www.ti.com/lit/gpn/SN74AUP1G04', '[2] TI product page https://www.ti.com/product/SN74AUP1G04', '[3] Puhan et al., Break-before-Make CMOS Inverter\u2026, Sci. World J. 2014, Art. 349131'], 13)
prs.save(os.path.join(ROOT, 'Case_Study_Presentation.pptx')); print('pptx ok')
