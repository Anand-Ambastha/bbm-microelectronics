#!/usr/bin/env python3
"""make_plots.py - waveform / sweep figures from the ACTUAL ngspice output in ../results -> ../figures"""
import json, os, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', 'results'); F = os.path.join(H, '..', 'figures')
plt.rcParams.update({'font.size': 9, 'axes.grid': True, 'grid.alpha': .3})
def load(f, names):
    a = np.loadtxt(os.path.join(R, f)); d = {'t': a[:, 0]}
    for i, n in enumerate(names): d[n] = a[:, 2*i+1]
    return d
C = load('conv_wave.csv', ['in', 'n1', 'n2', 'n3', 'out', 'itot', 'i3', 'i3g'])
B = load('bbm_wave.csv', ['in', 'n1', 'A', 'B', 'do', 'out', 'itot', 'i3', 'i3g'])
S = json.load(open(os.path.join(R, 'summary.json')))
w = lambda d: (d['t'] >= 39e-9) & (d['t'] <= 55e-9)   # one full cycle in steady state (3rd rising edge at 41 ns)
def tn(d): return d['t'][w(d)]*1e9

# 1) functional verification: input/output of both circuits
fig, ax = plt.subplots(2, 1, figsize=(7.5, 5), sharex=True)
for a, d, n in zip(ax, (C, B), ('Conventional (4 inverters)', 'BBM delay cell (PtNf)')):
    a.plot(tn(d), d['in'][w(d)], 'k--', lw=1.2, label='in'); a.plot(tn(d), d['out'][w(d)], 'C3', lw=1.8, label='out')
    a.set_ylabel('V'); a.set_title(n, fontsize=9); a.legend(loc='center right')
ax[1].set_xlabel('time (ns)'); fig.tight_layout(); fig.savefig(os.path.join(F, 'fig_wave_in_out.png'), dpi=300); plt.close(fig)

# 2) BBM mechanism: skewed A (PMOS gate) and B (NMOS gate) of stage 3
fig, ax = plt.subplots(3, 1, figsize=(7.5, 6.8), sharex=True)
ax[0].plot(tn(B), B['n1'][w(B)], 'k', label='n1 (stage-2 input)')
ax[0].plot(tn(B), B['in'][w(B)], 'k--', lw=.8, label='in'); ax[0].legend(loc='center right', fontsize=7)
ax[1].plot(tn(B), B['A'][w(B)], 'C3', lw=1.8, label='A = po  (PMOS gate of stage 3)'); ax[1].plot(tn(B), B['B'][w(B)], 'C0', lw=1.8, label='B = no  (NMOS gate of stage 3)')
ax[1].axhline(0.9, color='gray', lw=.6, ls=':'); ax[1].legend(loc='center right', fontsize=7)
ax[2].plot(tn(B), B['do'][w(B)], 'C2', label='do (merged output of stage 3)'); ax[2].plot(tn(B), B['out'][w(B)], 'C1', label='out'); ax[2].legend(loc='center right', fontsize=7)
ax[2].set_xlabel('time (ns)')
for a in ax: a.set_ylabel('V')
nd = S['bbm_nodes']
ax[1].set_title('Skewed signal pair: isolation times  t_if(B->A, falling) = %.0f ps,  t_ir(A->B, rising) = %.0f ps  (50 %% crossings)' % (nd['t_iso_fall_ps'], nd['t_iso_rise_ps']), fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(F, 'fig_wave_bbm_skew.png'), dpi=300); plt.close(fig)

# 3) stage-3 supply and ground currents, conventional vs BBM  (analogue of paper Fig. 11)
fig, ax = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)
for a, d, n in zip(ax, (C, B), ('Conventional: stage 3 (inv2)', 'BBM: stage 3 (P2/N2 merge)')):
    a.plot(tn(d), d['i3'][w(d)]*1e6, 'C3', label='supply current of stage 3 (i_P)'); a.plot(tn(d), d['i3g'][w(d)]*1e6, 'C0', label='ground current of stage 3 (i_N)')
    a.set_title(n, fontsize=9); a.set_xlabel('time (ns)'); a.legend(fontsize=7)
ax[0].set_ylabel('current (uA)'); fig.tight_layout(); fig.savefig(os.path.join(F, 'fig_stage3_currents.png'), dpi=300); plt.close(fig)

# 4) charge vs delay: sweeps
fig, ax = plt.subplots(figsize=(6.5, 4.2))
for k, c, lab in (('sweep_std', 'C3', 'Conventional (paper 750 ps sizing, inv1 lengths scaled)'), ('sweep_bbm', 'C0', 'BBM PtNf (paper 750 ps sizing, P1/Pt/Nf lengths scaled)')):
    x = [r['Tp_ps'] for r in S[k]]; y = [r['Q_fC_per_cycle'] for r in S[k]]; ax.plot(x, y, 'o-', color=c, label=lab, ms=4)
ax.set_xlabel('Tp (ps)'); ax.set_ylabel('supply charge per cycle (fC)'); ax.legend(fontsize=7); ax.set_title('Charge vs delay - one-parameter scaling sweeps (NOT re-optimised)', fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(F, 'fig_Q_vs_Tp_scaling.png'), dpi=300); plt.close(fig)

# 5) optimised results (if available)
p = os.path.join(R, 'summary_opt.json')
if os.path.exists(p):
    O = json.load(open(p)); fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for kind, c, lab in (('conventional', 'C3', 'Conventional (re-optimised)'), ('bbm', 'C0', 'BBM PtNf (re-optimised)')):
        x = [O[t][kind]['metrics']['Tp_ps'] for t in sorted(O, key=float)]; y = [O[t][kind]['metrics']['Q_fC_per_cycle'] for t in sorted(O, key=float)]
        ax.plot(x, y, 'o-', color=c, label=lab)
    ax.set_xlabel('Tp (ps)'); ax.set_ylabel('supply charge per cycle (fC)'); ax.legend(); ax.set_title('Charge at matched delay targets (own DE optimisation, ngspice)', fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(F, 'fig_Q_vs_Tp_optimised.png'), dpi=300); plt.close(fig)

# 6) CL sweep
fig, ax = plt.subplots(figsize=(6.2, 4)); cl = [float(r['cl'][:-1]) for r in S['sweep_cl']]
for n, c in (('conventional', 'C3'), ('bbm', 'C0')): ax.plot(cl, [r[n]['Q_fC_per_cycle'] for r in S['sweep_cl']], 'o-', color=c, label=n)
ax.set_xlabel('CL (fF)'); ax.set_ylabel('Q per cycle (fC)'); ax.legend(); ax.set_title('Load sensitivity (paper 750 ps sizing, unchanged)', fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(F, 'fig_CL_sweep.png'), dpi=300); plt.close(fig)
print('plots done')
