#!/usr/bin/env python3
"""make_schematics.py - redraws the circuits that were simulated (matplotlib, 300 dpi) -> ../figures/"""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
import os
FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
LW = 1.4
def ln(ax, xs, ys, **k): ax.plot(xs, ys, color=k.pop('c', 'k'), lw=k.pop('lw', LW), solid_capstyle='round', **k)
def dot(ax, x, y): ax.add_patch(Circle((x, y), 0.06, color='k', zorder=5))
def mos(ax, cx, cy, kind, gate='left', name='', size=''):
    """vertical MOSFET centred at (cx,cy). gate lead ends at (cx-0.9,cy) [left] ; returns dict of terminals.
    nmos: top=drain, bottom=source ; pmos: top=source, bottom=drain"""
    s = -1 if gate == 'left' else 1
    ln(ax, [cx, cx], [cy-0.4, cy+0.4])                       # channel
    ln(ax, [cx+s*0.2, cx+s*0.2], [cy-0.4, cy+0.4])           # gate plate
    gx = cx+s*0.2
    if kind == 'p':
        ln(ax, [gx+s*0.14, cx+s*0.9], [cy, cy]); ax.add_patch(Circle((gx+s*0.07, cy), 0.07, fc='w', ec='k', lw=LW, zorder=4))
    else:
        ln(ax, [gx, cx+s*0.9], [cy, cy])
    t = (cx-s*0.45)                                           # terminal x (opposite side of gate)
    for yy in (cy+0.4, cy-0.4):
        ln(ax, [cx, t], [yy, yy]); ln(ax, [t, t], [yy, yy+(0.4 if yy > cy else -0.4)])
    ax.text(cx+s*(-0.0)+(0.55 if s == -1 else -0.55), cy+0.02, name, fontsize=8, ha='left' if s == -1 else 'right', va='center')
    if size: ax.text(cx+(0.55 if s == -1 else -0.55), cy-0.28, size, fontsize=6, ha='left' if s == -1 else 'right', va='center', color='#444')
    return dict(g=(cx+s*0.9, cy), top=(t, cy+0.8), bot=(t, cy-0.8), t=t)
def vdd(ax, x, y): ln(ax, [x-0.25, x+0.25], [y, y]); ln(ax, [x, x], [y-0.0, y-0.2]); ax.text(x, y+0.12, 'VDD', ha='center', fontsize=7)
def gnd(ax, x, y):
    ln(ax, [x, x], [y, y-0.15]); 
    for i, w in enumerate((0.25, 0.16, 0.07)): ln(ax, [x-w, x+w], [y-0.15-0.07*i]*2)
def inv(ax, x, y, label=''):
    ax.add_patch(Polygon([[x, y-0.4], [x, y+0.4], [x+0.8, y]], fc='w', ec='k', lw=LW)); ax.add_patch(Circle((x+0.87, y), 0.07, fc='w', ec='k', lw=LW))
    ax.text(x+0.3, y-0.62, label, fontsize=7, ha='center')
    return (x, y), (x+0.94, y)

def bbm_cell():
    fig, ax = plt.subplots(figsize=(13, 6.2)); ax.set_xlim(-1, 15.5); ax.set_ylim(-1.1, 6.3); ax.axis('off')
    ax.set_title('Break-before-make (BBM) delay cell - PtNf topology (paper Fig. 9(b) + Fig. 8), as simulated\n(transistor labels: W/L in nm)', fontsize=11)
    ln(ax, [-0.8, 0.0], [3, 3]); ax.text(-0.9, 3.15, 'in', fontsize=9, ha='right'); i1 = inv(ax, 0, 3, 'unit inv (X1)')
    # stage 2 stack at x=4.5
    cx = 4.6
    P1 = mos(ax, cx, 4.6, 'p', 'left', 'P1', '220/740'); Pt = mos(ax, cx, 3.0, 'p', 'left', 'Pt', '220/350'); N1 = mos(ax, cx, 1.4, 'n', 'left', 'N1', '390/180')
    t = P1['t']
    vdd(ax, t, 5.8); ln(ax, [t, t], [P1['top'][1], 5.8])
    ln(ax, [t, t], [P1['bot'][1], Pt['top'][1]]); A = (t, P1['bot'][1]); dot(ax, *A)
    ln(ax, [t, t], [Pt['bot'][1], N1['top'][1]]); B = (t, N1['top'][1]); dot(ax, *B)
    gnd(ax, t, N1['bot'][1]); ln(ax, [t, t], [N1['bot'][1], N1['bot'][1]-0.0])
    # gate nets: P1 gate & N1 gate = n1 (bus left of the Pt gate lead, NOT connected to Pt) ; Pt gate = GND
    gx = P1['g'][0]; bx = gx-0.55
    ln(ax, [bx, bx], [P1['g'][1], N1['g'][1]]); ln(ax, [bx, gx], [P1['g'][1]]*2); ln(ax, [bx, gx], [N1['g'][1]]*2)
    ln(ax, [i1[1][0], bx], [2.2, 2.2]) if False else None
    ln(ax, [i1[1][0], bx], [3, 3]); dot(ax, bx, 3.0); ax.text(bx-0.15, 3.18, 'n1', fontsize=8, ha='right')
    ln(ax, [Pt['g'][0], Pt['g'][0]], [Pt['g'][1], 2.3]); gnd(ax, Pt['g'][0], 2.3)
    ax.text(Pt['g'][0]-0.15, 1.95, 'Pt gate=GND\n(always ON)', fontsize=6, ha='left', va='top')
    # Nf across A-B at x=7.0, gate on right side
    NF = mos(ax, 7.4, 3.0, 'n', 'right', 'Nf', '220/950')
    ln(ax, [t, NF['t']], [A[1], A[1]]); ln(ax, [NF['t'], NF['t']], [A[1], NF['top'][1]])
    ln(ax, [t, NF['t']], [B[1], B[1]]); ln(ax, [NF['t'], NF['t']], [B[1], NF['bot'][1]])
    ax.text(t+1.2, A[1]+0.15, 'A (po)', fontsize=9, color='#c0392b', fontweight='bold'); ax.text(t+1.2, B[1]-0.3, 'B (no)', fontsize=9, color='#1f5fa8', fontweight='bold')
    # stage 3 at x=10.6
    c3 = 10.6
    P2 = mos(ax, c3, 4.2, 'p', 'left', 'P2', '220/180'); N2 = mos(ax, c3, 1.8, 'n', 'left', 'N2', '220/220')
    t3 = P2['t']; vdd(ax, t3, 5.4); ln(ax, [t3, t3], [P2['top'][1], 5.4]); gnd(ax, t3, N2['bot'][1])
    ln(ax, [t3, t3], [P2['bot'][1], N2['top'][1]]); D = (t3, 3.0); dot(ax, *D)
    ax.text(t3+0.15, 3.15, 'do', fontsize=9, fontweight='bold')
    # A -> P2 gate ; B -> N2 gate  (routing lines)
    ln(ax, [A[0], A[0]], [A[1], A[1]]); 
    yA = 5.05; ln(ax, [t, t], [A[1], A[1]])
    ln(ax, [A[0]+0.0, 8.6, 8.6, P2['g'][0]], [A[1], A[1], P2['g'][1], P2['g'][1]], c='#c0392b')
    ln(ax, [B[0], 9.0, 9.0, N2['g'][0]], [B[1], B[1], N2['g'][1], N2['g'][1]], c='#1f5fa8')
    # Nf gate <- do (feedback)
    ln(ax, [NF['g'][0], NF['g'][0]+0.0], [3.0, 3.0]); ln(ax, [NF['g'][0], NF['g'][0]], [3.0, 6.0]); ln(ax, [NF['g'][0], 12.3], [6.0, 6.0]); ln(ax, [12.3, 12.3], [6.0, 3.0]); 
    ln(ax, [t3, 13.0], [3.0, 3.0]); dot(ax, 12.3, 3.0)
    ax.text(9.6, 6.1, 'level-restoration feedback (do -> Nf gate)', fontsize=7, ha='center', color='#555')
    i4 = inv(ax, 13.0, 3.0, 'unit inv (X4)'); ln(ax, [i4[1][0], 15.0], [3, 3]); ax.text(15.1, 3.1, 'out', fontsize=9)
    ln(ax, [14.55, 14.55], [3, 2.1]); ln(ax, [14.3, 14.8], [2.1, 2.1]); ln(ax, [14.3, 14.8], [1.9, 1.9]); ln(ax, [14.55, 14.55], [1.9, 1.5]); gnd(ax, 14.55, 1.5); dot(ax, 14.55, 3); ax.text(14.9, 2.0, 'CL', fontsize=8)
    ax.text(5.9, -0.45, 'CMOS -> BBM converter\n(P1, Pt, N1, Nf)', ha='center', fontsize=8, style='italic')
    ax.text(10.9, -0.45, 'BBM -> CMOS converter\n(P2, N2)', ha='center', fontsize=8, style='italic')
    fig.savefig(os.path.join(FIG, 'fig_circuit_bbm_cell.png'), dpi=300, bbox_inches='tight'); plt.close(fig)

def conv_cell():
    fig, ax = plt.subplots(figsize=(13, 3.6)); ax.set_xlim(-1, 15.5); ax.set_ylim(-1.8, 2.6); ax.axis('off')
    ax.set_title('Conventional (reference) delay cell - four cascaded static CMOS inverters (paper Fig. 9(a)), as simulated', fontsize=11)
    xs = [0, 3.4, 6.8, 10.2]; labels = ['X1 unit\n860/180 | 220/180', 'X2 (inv1)\n220/370 | 220/880', 'X3 (inv2)\n880/730 | 1050/1320', 'X4 unit\n860/180 | 220/180']
    prev = (-0.8, 0)
    ln(ax, [-0.8, 0], [0, 0]); ax.text(-0.9, 0.15, 'in', ha='right')
    for x, l, k in zip(xs, labels, ('X1', 'n1', 'n2', 'n3')):
        a, b = inv(ax, x, 0, ''); ax.text(x+0.45, -0.75, l + '\n(Wp/Lp | Wn/Ln, nm)', fontsize=6.5, ha='center', va='top')
        if x != xs[-1]: ln(ax, [b[0], x+3.4], [0, 0]); ax.text(b[0]+1.0, 0.12, ('n1', 'n2', 'n3')[xs.index(x)], fontsize=8)
    ln(ax, [xs[-1]+0.94, 14.0], [0, 0]); ax.text(14.1, 0.12, 'out', fontsize=9)
    ln(ax, [13.3, 13.3], [0, -0.7]); ln(ax, [13.05, 13.55], [-0.7, -0.7]); ln(ax, [13.05, 13.55], [-0.9, -0.9]); ln(ax, [13.3, 13.3], [-0.9, -1.2]); gnd(ax, 13.3, -1.2); dot(ax, 13.3, 0); ax.text(13.65, -0.8, 'CL', fontsize=8)
    fig.savefig(os.path.join(FIG, 'fig_circuit_conventional.png'), dpi=300, bbox_inches='tight'); plt.close(fig)

def cmos_inv_and_aup():
    fig, ax = plt.subplots(figsize=(5, 4.6)); ax.set_xlim(-2, 4); ax.set_ylim(-1.5, 5); ax.axis('off')
    P = mos(ax, 1.5, 3.2, 'p', 'left', 'PMOS'); N = mos(ax, 1.5, 1.2, 'n', 'left', 'NMOS'); t = P['t']
    vdd(ax, t, 4.6); ln(ax, [t, t], [P['top'][1], 4.6]); ln(ax, [t, t], [P['bot'][1], N['top'][1]]); gnd(ax, t, N['bot'][1])
    gx = P['g'][0]; ln(ax, [gx, gx], [3.2, 1.2]); ln(ax, [-1.5, gx], [2.2, 2.2]); dot(ax, gx, 2.2); ax.text(-1.55, 2.35, 'A', fontsize=10, ha='right')
    ln(ax, [t, 3.4], [2.2, 2.2]); dot(ax, t, 2.2); ax.text(3.45, 2.3, 'Y = A\u0305', fontsize=10)
    ax.set_title('Generic static CMOS inverter (illustrative; the AUP1G04\ninternal transistor netlist is not published in the datasheet)', fontsize=8)
    fig.savefig(os.path.join(FIG, 'fig_cmos_inverter_generic.png'), dpi=300, bbox_inches='tight'); plt.close(fig)

def bbm_concept():
    """conceptual (ideal transport-delay) timing diagram redrawn from the description of paper Fig. 1(b)"""
    import numpy as np
    fig, ax = plt.subplots(figsize=(7.5, 3.4)); ax.axis('off')
    tir, tif = 1.2, 1.2
    def sig(edges, y0, hi=0.8, tr=0.25):
        xs = [0]; ys = [y0]
        for te, lev in edges: xs += [te, te+tr]; ys += [ys[-1], lev]
        xs.append(12); ys.append(ys[-1]); return xs, ys
    # NMOS gate (ni) and PMOS gate (pi): rising input -> pi rises first (isolation), ni follows (information)
    pi = sig([(2, .8), (7, 0)], 0); ni = sig([(2+tir, .8), (7+tif*0+0.0, 0)], 0)
    ni = sig([(2+tir, .8), (7-0.0, 0)], 0)   # fall of ni = isolation on falling input -> ni falls first
    pi = sig([(2, .8), (7+tif, 0)], 0)
    for i, (n, s, c) in enumerate((('pi (PMOS gate)', pi, '#c0392b'), ('ni (NMOS gate)', ni, '#1f5fa8'))):
        y = 1.6-1.0*i; ax.plot(s[0], [v+y for v in s[1]], color=c, lw=2); ax.text(-0.2, y+0.35, n, ha='right', fontsize=8)
    ax.annotate('', xy=(2+tir+0.0, 1.55), xytext=(2.0, 1.55), arrowprops=dict(arrowstyle='<->', lw=0.9)); ax.text(2.0+tir/2, 1.62, 't_ir', ha='center', fontsize=8)
    ax.annotate('', xy=(7+tif, 0.45), xytext=(7.0, 0.45), arrowprops=dict(arrowstyle='<->', lw=0.9)); ax.text(7.0+tif/2, 0.52, 't_if', ha='center', fontsize=8)
    ax.text(2.0, 2.0, 'isolation edge', fontsize=7, color='#c0392b'); ax.text(3.4, 0.9, 'information edge', fontsize=7, color='#1f5fa8')
    ax.axvspan(2, 2+tir+0.2, ymin=0.0, ymax=0.9, color='#bbb', alpha=0.35); ax.text(2+tir/2+0.1, -0.35, 'both devices OFF\n(output high-Z)', fontsize=7, ha='center')
    ax.axvspan(7, 7+tif+0.2, ymin=0.0, ymax=0.9, color='#bbb', alpha=0.35); ax.text(7+tif/2+0.1, -0.35, 'both devices OFF', fontsize=7, ha='center')
    ax.set_xlim(-3.5, 12); ax.set_ylim(-0.7, 2.3)
    ax.set_title('Conceptual BBM timing (redrawn from the paper\'s description of Fig. 1(b); not simulation data)', fontsize=8)
    fig.savefig(os.path.join(FIG, 'fig_bbm_concept_timing.png'), dpi=300, bbox_inches='tight'); plt.close(fig)

if __name__ == '__main__':
    bbm_cell(); conv_cell(); cmos_inv_and_aup(); bbm_concept(); print('ok')
