from common import *
d = Document('/mnt/user-data/uploads/CBS_LAB-f3e46712f932.docx'); P = d.paragraphs; T = d.tables[1]
b = S['baseline']; c0, b0 = b['conventional'], b['bbm']
o5, o1 = O['0.5'], O['1']; r1, q1 = o1['conventional'], o1['bbm']; m_r, m_q = r1['metrics'], q1['metrics']
def Cu(i): return Cur(P[i]._p, P[i]._parent)
J = 'j'
set_blank(P[24], 'Implementation and Simulation of a Break-Before-Make CMOS Inverter for Low-Power Delay Generation', 12, True)
set_blank(P[28], 'Break-Before-Make (BBM) CMOS inverter / delay cell (PtNf full-swing topology, Fig. 9(b) and Fig. 8 of the paper), compared with a conventional 4-inverter CMOS delay cell')
set_blank(P[30], 'Break-before-make (dual-ramp, time-skewed) switching to eliminate direct-path (short-circuit) current; supply charge/energy per delay reduced')
set_blank(P[44], 'Break-before-Make CMOS Inverter for Power-Efficient Delay Implementation')
set_blank(P[46], 'J. Puhan, D. Raič, T. Tuma, and Á. Bűrmen')
set_blank(P[48], 'The Scientific World Journal, vol. 2014, Article ID 349131 (doi:10.1155/2014/349131)')
set_blank(P[50], '2014')
fill_after_label(P[52], 'ngspice-42 (open-source SPICE, batch mode, Ubuntu 24 container). Transient analysis; Python 3 / NumPy used only for post-processing and cross-check. NOT the paper\'s HSPICE.')
fill_after_label(P[53], 'SUBSTITUTE Level-1 (Shichman\u2013Hodges) 0.18 \u00b5m-class model built from the parameters in the caption of Fig. 4 of the paper (V_TN = 0.5 V, V_TP = \u22120.5 V, K_PN = 350 \u00b5A/V\u00b2, K_PP = 90 \u00b5A/V\u00b2, C_ox = 8.6 fF/\u00b5m\u00b2, L_min = 180 nm). It is NOT the TSMC 0.18 \u00b5m HSPICE model used by the authors (proprietary); \u03bb, \u03b3, \u03c6, junction and overlap capacitances are student assumptions (file models_180nm_L1.lib).')
fill_after_label(P[54], '1.8 V (same for both circuits)')
fill_after_label(P[55], '27 \u00b0C (ngspice .temp 27; Level-1 parameters are not temperature-tuned)')
fill_after_label(P[56], 'C_L = 2 fF at the output of the output unit inverter (\u2248 one unit-inverter input capacitance); sweep 0.5\u201310 fF also run. Input: 0\u21921.8 V pulse, 50 ps edges, 20 ns period (50 MHz), 50 % duty.')

# 5 circuit diagram
set_blank(P[58], 'Transistor-level schematics of the two circuits exactly as simulated (redrawn from paper Figs. 8 and 9; sizes W/L in nm).')
c = Cu(58)
c.image(os.path.join(FIG, 'fig_circuit_conventional.png'), 6.4, 'Fig. 1. Reference: conventional delay cell (4 static CMOS inverters). Netlist: conventional_inverter.sp')
c.image(os.path.join(FIG, 'fig_circuit_bbm_cell.png'), 6.4, 'Fig. 2. Optimised circuit: BBM delay cell, PtNf topology. Netlist: bbm_inverter.sp (sizes shown = paper\'s 750 ps sizing)')

# 6 design details
c = Cu(60)
set_blank(P[60], 'Circuit reconstruction. The paper\'s Fig. 9(b) delay cell is: input unit inverter \u2192 split-output BBM inverter (CMOS-to-BBM converter, Fig. 1(a)) \u2192 split-input merge inverter (BBM-to-CMOS converter, Fig. 1(c)) \u2192 output unit inverter. The bidirectional delay element is the PtNf full-swing implementation of Fig. 8: P1 (source V_DD), node A (po), Pt (PMOS, gate tied to GND, i.e. always conducting in triode), node B (no), N1 (source GND); Nf is an NMOS connected across A\u2013B whose gate is driven by the next-stage output (do) to restore the low level of A. Stage 3 has P2 (gate A) and N2 (gate B) with joined drains (do). These connections were read directly from the figures in the PDF; the polarity of Nf\'s gate (connected to the merged output) and the 2-transistor stage-3 follow the paper\'s statement that the level-restoration control signals are taken from the next-stage output. Transistor count: conventional 8; BBM 10 (two unit inverters = 4, plus P1, Pt, N1, Nf = 4, plus P2, N2 = 2).', size=10.5, align=J)
c.para('**Sizing used.** Both cells use the sizing printed in the Fig. 11 caption of the paper for T_p = 750 ps (unit inverters not specified by the paper, student choice W_p/W_n = 860/220 nm, L = 180 nm, following the symmetric stage of Fig. 4). Conventional: inv1 W_p/L_p = 220/370, W_n/L_n = 220/880; inv2 W_p/L_p = 880/730, W_n/L_n = 1050/1320 (nm). BBM: P1 220/740, N1 390/180, Pt 220/350, Nf 220/950, P2 220/180, N2 220/220 (nm). Source/drain parasitics follow the paper\'s rule A_d = A_s = 0.8 \u00b5m\u00d7w, P_d = P_s = 1.5 \u00b5m + w.', size=10.5, align=J)
c.para('**Measurement definitions (identical for both circuits).** Delay: 50 % (0.9 V) crossing of the input to 50 % crossing of the cell output, rising and falling, 3rd edge of each (steady state). T_p = (t_pLH + t_pHL)/2. Charge: supply charge of the whole cell (all four stages; the input source is not counted) integrated over 4 complete cycles (21\u2013101 ns) divided by 4 \u2192 Q per cycle (one rising + one falling slope, the paper\'s metric); energy per cycle E = Q\u00b7V_DD; average power P_avg = E / T_cycle at 50 MHz; PDP = P_avg \u00d7 T_p. Because E per cycle is independent of frequency (leakage is zero in a Level-1 model), P_avg and PDP scale with the chosen 50 MHz test frequency; Q (or E) per cycle is the frequency-independent comparison. Area is the gate-area proxy \u03a3 W\u00b7L over all transistors (not a layout area).', size=10.5, align=J)
c.para('**Tools and flow.** run_all.py (baseline, scaling sweeps, C_L and edge-rate sweeps, no-skew ablation), optimize.py (differential-evolution re-sizing at T_p targets 0.5 ns and 1.0 ns, constraints: |T_p/target \u2212 1| \u2264 2 %, |t_pLH \u2212 t_pHL| \u2264 15 % of T_p, output swing \u2265 1.7 V / \u2264 0.1 V, BBM node levels restored and isolation times > 0), validate_opt.py (re-run optimised sizes on the full testbench). Checks performed: (i) convergence errors (none in final runs); (ii) no floating nodes (all nodes have DC paths; DC operating point converged); (iii) independent Python trapezoidal integration of the raw waveform reproduces ngspice charge to < 0.01 % (67.349 vs 67.354 fC and 40.304 vs 40.310 fC); (iv) one bug turned up and was fixed: ngspice treats the name gnd as node 0, which silently shorted a current-sense source.', size=10.5, align=J)

# 7 functional verification
c = Cu(66)  # after "Observation:" label -> put image before? insert after label
set_blank(P[67], 'Input and output waveforms of both circuits over one steady-state cycle (data from conv_wave.csv / bbm_wave.csv produced by ngspice) are in Fig. 3; the BBM internal skewed nodes are in Fig. 4. Both circuits are non-inverting overall (4 inversions).', size=10.5, align=J)
c = Cu(67)
c.image(os.path.join(FIG, 'fig_wave_in_out.png'), 5.0, 'Fig. 3. Functional verification: in (dashed) and out for the conventional and BBM cells (paper 750 ps sizing).')
c.image(os.path.join(FIG, 'fig_wave_bbm_skew.png'), 5.0, 'Fig. 4. BBM mechanism: node A (PMOS gate of stage 3) and node B (NMOS gate of stage 3) switch at different times; stage 3 output do follows.')
c.table([['in', 'out (ideal)', 'out (conventional, simulated steady state)', 'out (BBM, simulated steady state)'], ['0', '0', '%.3f V (logic 0)' % c0['Vout_min'], '%.3f V (logic 0)' % b0['Vout_min']], ['1 (1.8 V)', '1', '%.3f V (logic 1)' % c0['Vout_max'], '%.3f V (logic 1)' % b0['Vout_max']]], size=8.5)
c.para('(Table shows extreme values over the measured window, including small over/undershoot; settled levels are 0 V and 1.8 V.)', size=8.5, italic=True)
set_blank(P[68], 'Observation: Both circuits reproduce the input with a delay of about 0.5\u20130.6 ns and full-swing outputs (V_out(max) = %.2f / %.2f V, V_out(min) = %.3f / %.3f V for conventional / BBM). In the BBM cell, on a rising input, node A (PMOS gate) rises 155 ps before node B (NMOS gate) and on a falling input B falls 258 ps before A (50 %% crossings), i.e. an isolation interval exists in every transition and the merge stage never has both gates in the conducting range at once. Node A overshoots to %.2f V and node B undershoots to %.2f V through gate-drain coupling (Miller) and then settle to full rails (Nf restores the low level of A). Function verified.' % (c0['Vout_max'], b0['Vout_max'], c0['Vout_min'], b0['Vout_min'], S['bbm_nodes']['A_max'], S['bbm_nodes']['B_min']), size=10.5, align=J)

# 8 table
def fmt(m, k, f='%.2f'): return f % m[k]
rowsT = [
 ['VDD', '1.8 V', '1.8 V', '1.8 V'],
 ['Transistor Count', '8', '10', '10'],
 ['Power (P_avg @ 50 MHz)', '%.2f \u00b5W' % m_r['Pavg_uW'], '%.2f \u00b5W' % b0['Pavg_uW'], '%.2f \u00b5W' % m_q['Pavg_uW']],
 ['Delay (T_p)', '%.0f ps' % m_r['Tp_ps'], '%.0f ps' % b0['Tp_ps'], '%.0f ps' % m_q['Tp_ps']],
 ['PDP (P_avg \u00d7 T_p)', '%.2f fJ' % m_r['PDP_fJ'], '%.2f fJ' % b0['PDP_fJ'], '%.2f fJ' % m_q['PDP_fJ']],
 ['Area (gate-area proxy \u03a3W\u00b7L)', '%.2f \u00b5m\u00b2' % area_um2('conventional', r1['params'] | dict(wp1=220, wn1=220)), '%.2f \u00b5m\u00b2' % area_um2('bbm', {}), '%.2f \u00b5m\u00b2' % area_um2('bbm', q1['params'])],
 ['Other: Q per cycle (E = Q\u00b7VDD)', '%.1f fC (%.1f fJ)' % (m_r['Q_fC_per_cycle'], m_r['E_fJ_per_cycle']), '%.1f fC (%.1f fJ)' % (b0['Q_fC_per_cycle'], b0['E_fJ_per_cycle']), '%.1f fC (%.1f fJ)' % (m_q['Q_fC_per_cycle'], m_q['E_fJ_per_cycle'])]]
for i, row in enumerate(rowsT, 1):
    for j, v in enumerate(row):
        cell = T.cell(i, j)
        if j == 0: continue
        cell.text = ''; r = cell.paragraphs[0].add_run(v); r.font.size = Pt(8.5); r.font.name = FONT
cc = Cu(69)
cc.para('Column meaning: **Reference/Existing** = conventional 4-inverter cell, re-sized (own differential-evolution optimisation) for T_p \u2248 1.0 ns; **Student Circuit** = BBM cell exactly as built from the paper\'s published 750 ps sizing, not re-sized (its T_p = 563 ps does NOT match the reference, so it is shown for completeness only and must not be used for improvement); **Optimized Circuit** = BBM PtNf re-sized by the same optimiser for T_p \u2248 1.0 ns. All values from ngspice, full testbench, 27 \u00b0C, C_L = 2 fF.', size=9, align=J, italic=True)
# supplementary tables go after the template table: anchor = table element
from docx.table import Table as _T
cc = Cur(T._tbl, T._parent)
def pair(lbl, c, b):
    return [lbl, '%.0f / %.0f' % (c['Tp_ps'], b['Tp_ps']), '%.1f / %.1f' % (c['Q_fC_per_cycle'], b['Q_fC_per_cycle']), '%.2f / %.2f' % (c['Pavg_uW'], b['Pavg_uW']), '%.2f / %.2f' % (c['PDP_fJ'], b['PDP_fJ']),
            '%+.1f %%' % (-pct(c['Q_fC_per_cycle'], b['Q_fC_per_cycle'])), '%+.1f %%' % (-pct(c['Pavg_uW'], b['Pavg_uW'])), '%+.1f %%' % (pct(c['Tp_ps'], b['Tp_ps']) * -1), '%.1f %%' % pct(c['PDP_fJ'], b['PDP_fJ'])]
cc.para('Supplementary comparison (conventional / BBM). \u0394 columns = change of BBM relative to conventional (negative = BBM lower).', bold=True, size=9)
cc.table([['Case', 'T_p (ps)', 'Q (fC/cycle)', 'P_avg (\u00b5W)', 'PDP (fJ)', '\u0394Q', '\u0394Power', '\u0394Delay', 'PDP impr.'],
 pair('Paper 750 ps sizing (delays not matched)', c0, b0), pair('Re-optimised, target 0.5 ns', o5['conventional']['metrics'], o5['bbm']['metrics']), pair('Re-optimised, target 1.0 ns', m_r, m_q)], size=7.5)
cc.para('Optimised parameter sets (nm): ' + '; '.join('%s %s: %s' % (t, k, ', '.join('%s=%d' % kv for kv in O[t][k]['params'].items())) for t in ('0.5', '1') for k in ('conventional', 'bbm')), size=7.5, align=J)

# 9 optimisation
fill_after_label(P[71], 'Transistor sizing of both cells (channel lengths/widths; for BBM mainly l_P1, w_N1, l_N1, w_Pt, l_Pt, l_Nf, l_P2, l_N2 and the delay-element transistor Pt), for a fixed delay target, minimising supply charge per cycle Q. Method: scipy differential evolution driving ngspice (960 simulations per case).')
fill_after_label(P[72], 'Paper 750 ps sizing: Q = %.1f fC (conventional, T_p = %.0f ps) and %.1f fC (BBM, T_p = %.0f ps).' % (c0['Q_fC_per_cycle'], c0['Tp_ps'], b0['Q_fC_per_cycle'], b0['Tp_ps']))
fill_after_label(P[73], 'T_p \u2248 1.0 ns: Q = %.1f fC (conventional) and %.1f fC (BBM). T_p \u2248 0.5 ns: Q = %.1f fC and %.1f fC.' % (m_r['Q_fC_per_cycle'], m_q['Q_fC_per_cycle'], o5['conventional']['metrics']['Q_fC_per_cycle'], o5['bbm']['metrics']['Q_fC_per_cycle']))
set_blank(P[75], 'The paper\'s own comparison sizes every cell for the same delay; comparing the BBM cell at the paper\'s sizing with an un-resized conventional cell (Q = 67 fC vs 40 fC, a misleading "40 %%") is unfair because the conventional chain at 750-ps sizing is far from the optimum for a 0.5 ns or 1.0 ns target (its charge falls to %.0f fC at 0.5 ns). Re-sizing both circuits for equal delay gives numbers I can stand behind. Limits: the optimiser is much smaller than the paper\'s (100-node SADE), so neither sizing is guaranteed globally optimal.' % o5['conventional']['metrics']['Q_fC_per_cycle'], size=10.5, align=J)

# 10 results
set_blank(P[78], 'Actual ngspice results (raw files in results/: *.log measurement logs, *_wave.csv waveforms, summary.json, summary_opt.json).', size=10.5)
c = Cu(78)
c.image(os.path.join(FIG, 'fig_stage3_currents.png'), 5.6, 'Fig. 5. Stage-3 supply (i_P) and ground (i_N) currents. In the BBM cell the merged stage never carries a large overlapping current; the peak supply current of stage 3 is %.1f \u00b5A (BBM) vs %.1f \u00b5A (conventional).' % (S['wave_check']['bbm']['ipeak_stage3_uA'], S['wave_check']['conventional']['ipeak_stage3_uA']))
c.image(os.path.join(FIG, 'fig_Q_vs_Tp_optimised.png'), 4.4, 'Fig. 6. Charge per cycle at matched delay targets after re-optimisation (two targets only).')
c.image(os.path.join(FIG, 'fig_Q_vs_Tp_scaling.png'), 4.2, 'Fig. 7. One-parameter scaling sweeps from the paper\'s 750 ps sizing (not re-optimised; the conventional cell is NOT at its optimum away from 750 ps, so this plot overstates the BBM advantage).')
rows = [['C_L', 'T_p conv / BBM (ps)', 'Q conv / BBM (fC)', 'BBM charge change']]
for r in S['sweep_cl']: rows.append([r['cl'].replace('f', ' fF'), '%.0f / %.0f' % (r['conventional']['Tp_ps'], r['bbm']['Tp_ps']), '%.1f / %.1f' % (r['conventional']['Q_fC_per_cycle'], r['bbm']['Q_fC_per_cycle']), '%.1f %%' % -pct(r['conventional']['Q_fC_per_cycle'], r['bbm']['Q_fC_per_cycle'])])
c.para('Table. Load sensitivity at the paper\'s 750 ps sizing (delays not matched, so absolute savings are inflated; trend only).', size=9, bold=True)
c.table(rows, size=8)
rows = [['Input edge', 'T_p conv / BBM (ps)', 'Q conv / BBM (fC)']]
for r in S['sweep_edge']: rows.append([r['tedge'].replace('p', ' ps'), '%.0f / %.0f' % (r['conventional']['Tp_ps'], r['bbm']['Tp_ps']), '%.1f / %.1f' % (r['conventional']['Q_fC_per_cycle'], r['bbm']['Q_fC_per_cycle'])])
c.para('Table. Input-edge-rate sensitivity (same sizing).', size=9, bold=True); c.table(rows, size=8)
a = S['ablation_noskew']
c.para('Ablation (documented, not used for the improvement figure): removing the delay element (A, B joined by 10 \u03a9, Nf deleted) with identical device sizes gives T_p = %.0f ps and Q = %.1f fC, a different (much faster) circuit, because the Pt resistance is what creates the delay. It therefore cannot isolate the short-circuit saving; a simple min(i_P, i_N) crowbar estimate for stage 3 gives %.2f fC (conventional) and %.2f fC (BBM) per cycle, i.e. only a few percent of stage-3 charge in this model.' % (a['Tp_ps'], a['Q_fC_per_cycle'], S['wave_check']['conventional']['crowbar_est_stage3_fC_per_cycle'], S['wave_check']['bbm']['crowbar_est_stage3_fC_per_cycle']), size=9.5, align=J)
for i, t in ((80, 'Functional waveform (Figs. 3, 4)'), (81, 'Power measurement (Section 8 table)'), (82, 'Delay measurement (Section 8 table)'), (83, 'PDP calculation (Section 8 table)'), (84, 'Optimization result (Section 9, Fig. 6)'), (85, 'Comparative result (Section 8, Section 12)')):
    for r in P[i].runs: r.text = ''
    P[i].runs[0].text = '\u2611 ' + t
# 11 result
set_blank(P[87], 'The implemented circuits were successfully simulated (ngspice-42) and the performance was evaluated. Improvement is computed for the delay-matched re-optimised pair at T_p \u2248 1.0 ns (conventional %.0f ps, BBM %.0f ps).' % (m_r['Tp_ps'], m_q['Tp_ps']), size=10.5)
fill_after_label(P[88], 'P_avg = %.2f \u00b5W (conventional) vs %.2f \u00b5W (BBM) at 50 MHz, %.1f %% lower (Q = %.1f vs %.1f fC per cycle).' % (m_r['Pavg_uW'], m_q['Pavg_uW'], pct(m_r['Pavg_uW'], m_q['Pavg_uW']), m_r['Q_fC_per_cycle'], m_q['Q_fC_per_cycle']))
fill_after_label(P[89], '%.0f ps (conventional) vs %.0f ps (BBM): %.1f %% shorter, i.e. matched by design (target 1.0 ns \u00b1 2 %%).' % (m_r['Tp_ps'], m_q['Tp_ps'], pct(m_r['Tp_ps'], m_q['Tp_ps'])))
fill_after_label(P[90], '%.2f fJ (conventional) vs %.2f fJ (BBM) (PDP = P_avg \u00d7 T_p at 50 MHz).' % (m_r['PDP_fJ'], m_q['PDP_fJ']))
fill_after_label(P[91], '8 (conventional) vs 10 (BBM).')
fill_after_label(P[92], '%.1f %%  [= (%.3f \u2212 %.3f)/%.3f \u00d7 100, from the logged PDP values]' % (pct(m_r['PDP_fJ'], m_q['PDP_fJ']), m_r['PDP_fJ'], m_q['PDP_fJ'], m_r['PDP_fJ']))
# 12 discussion
c = Cu(93)
set_blank(P[94], 'At T_p \u2248 1.0 ns the BBM cell cuts PDP by %.1f %% and charge by %.1f %%. At \u2248 0.5 ns the cuts are %.1f %% (PDP) and %.1f %% (charge). The paper\'s Table 1 shows the same pattern: a 10 %% saving at 0.5 ns, 36 %% at 1.0 ns, a bit over 40 %% from 3.5 ns, and no gain below about 0.35 ns. My saving at 1 ns is smaller than the paper\'s.' % (pct(m_r['PDP_fJ'], m_q['PDP_fJ']), pct(m_r['Q_fC_per_cycle'], m_q['Q_fC_per_cycle']), pct(o5['conventional']['metrics']['PDP_fJ'], o5['bbm']['metrics']['PDP_fJ']), pct(o5['conventional']['metrics']['Q_fC_per_cycle'], o5['bbm']['metrics']['Q_fC_per_cycle'])), size=10.5, align=J)
c = Cu(94)
c.para('BBM is not free. It needs 10 transistors instead of 8, plus two wires between stages. At the paper\'s 750 ps sizing the BBM cell is also slower (563 ps against 507 ps, with rise and fall delays of %.0f and %.0f ps), so the %.0f %% charge saving at that point should not be quoted. The gate-area proxy at 1.0 ns is %.2f \u00b5m\u00b2 for BBM and %.2f \u00b5m\u00b2 for the conventional cell, but that is not a layout area. With sizes fixed, the gain shrinks as the load grows (41 %% at 0.5 fF, 34 %% at 10 fF) and with slow input edges (38.7 %% at 500 ps). I did not test delays at or below 0.35 ns, where the paper finds no advantage.' % (b0['tpLH_ps'], b0['tpHL_ps'], pct(c0['Q_fC_per_cycle'], b0['Q_fC_per_cycle']), area_um2('bbm', q1['params']), area_um2('conventional', r1['params'] | dict(wp1=220, wn1=220))), size=10.5, align=J)
c.para('Why does it save charge? Eq. (16) of the paper gives charge proportional to T_p with a smaller slope than Eq. (9), because Q_s is about zero. In my runs the crowbar charge of the conventional stage 3 is small, so I think most of the saving comes from how the delay is made. BBM gets it from a long, narrow Pt (and long P1 and Nf) that load only the small first stage. The conventional chain needs a big, long-channel inv2 whose capacitance is charged every cycle. The paper makes a similar remark about the third-stage gate capacitance. I did not separate the two effects rigorously.', size=10.5, align=J)
c.para('Limits. Level-1 has no velocity saturation, sub-threshold current or gate leakage, so static power is zero, and only 27 \u00b0C was run. \u03bb, \u03b3 and the capacitances are my assumptions, so absolute fC values cannot be compared with the paper\'s TSMC numbers. The unit-inverter sizes and C_L are assumed too. One corner, no mismatch, a reduced optimiser, no layout parasitics (as in the paper), and the input driver\'s charge is not counted.', size=10.5, align=J)
# 13 conclusion
set_blank(P[98], 'I rebuilt the paper\'s break-before-make delay cell (PtNf) from its figures, wrote ngspice netlists for it and for a conventional 4-inverter reference, and simulated both with a substitute Level-1 0.18 \u00b5m-class model at 1.8 V. Both work and give full-swing outputs. In the BBM cell the PMOS-gate and NMOS-gate nodes of the last stage switch 155 to 258 ps apart (paper sizing), so the two transistors never conduct together.', size=10.5, align=J)
set_blank(P[99], 'With both cells re-sized for the same delay, BBM cut PDP by %.1f %% at about 1.0 ns and %.1f %% at about 0.5 ns, and the charge per cycle by %.1f %% and %.1f %%. That follows the paper\'s trend, more benefit at longer delay, but not its numbers. I would call it a qualitative confirmation for this substitute model, not a reproduction of the TSMC results.' % (pct(m_r['PDP_fJ'], m_q['PDP_fJ']), pct(o5['conventional']['metrics']['PDP_fJ'], o5['bbm']['metrics']['PDP_fJ']), pct(m_r['Q_fC_per_cycle'], m_q['Q_fC_per_cycle']), pct(o5['conventional']['metrics']['Q_fC_per_cycle'], o5['bbm']['metrics']['Q_fC_per_cycle'])), size=10.5, align=J)
# 14 refs
set_blank(P[102], '[1] ' + CITE + ' https://pmc.ncbi.nlm.nih.gov/articles/PMC4265520/', 9.5)
set_blank(P[103], '[2] ngspice circuit simulator, version 42, https://ngspice.sourceforge.io/ (simulations and .meas measurements).  [3] Level-1 MOSFET model parameters taken from the caption of Fig. 4 of [1]. Unlisted parameters are student assumptions (see models_180nm_L1.lib).', 9.5)
d.save('/home/claude/out/CBS_Experiment.docx'); print('saved')
