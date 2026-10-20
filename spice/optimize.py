#!/usr/bin/env python3
"""optimize.py - reduced-scale re-sizing study (differential evolution, scipy) at fixed delay targets.
Minimises supply charge per cycle Q subject to  Tp ~= target (+-2 %), tpLH/tpHL symmetry, full output swing,
and (BBM) restored node levels.  Uses short, fast simulations (period 10 ns, 3 measured cycles).
Same VDD/model/temperature/CL/input as the main testbench.  Output: ../results/opt_<target>.json
Usage: python3 optimize.py 0.5 1.0 """
import sys, re, os, json, subprocess, tempfile, shutil, numpy as np
from scipy.optimize import differential_evolution
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, '..', 'results')
VDD = 1.8
FAST = [('.tran 1p 101n 0 2p', '.tran 2p 41n 0 4p'), ('from=21n to=101n', 'from=11n to=41n'),
        ('per=20n pw=10n', 'per=10n pw=5n')]
def prep(net):
    t = open(os.path.join(HERE, net)).read()
    t = re.sub(r'^wrdata.*\n', '', t, flags=re.M)
    for a, b in FAST: t = t.replace(a, b)
    return t
TEMPL = {n: prep(n + '_inverter.sp') for n in ('conventional', 'bbm')}
def sim(kind, p):
    t = TEMPL[kind]
    for k, v in p.items():
        t, n = re.subn(r'(^\.param[^\n]*?\b%s=)\S+' % k, r'\g<1>%.0fn' % v, t, flags=re.M); assert n == 1, k
    d = tempfile.mkdtemp(); shutil.copy(os.path.join(HERE, 'models_180nm_L1.lib'), d)
    open(os.path.join(d, 'n.sp'), 'w').write(t)
    r = subprocess.run(['ngspice', '-b', 'n.sp'], capture_output=True, text=True, cwd=d); shutil.rmtree(d)
    L = r.stdout + r.stderr
    if re.search(r'(?i)error|timestep too small', L): return None
    return {k.lower(): float(v) for k, v in re.findall(r'^(\w+)\s+=\s+([-+0-9.eE]+)', L, flags=re.M)}
SPECS = {  # name: (bounds list of (param, lo, hi))
 'conventional': [('lp1',180,1500),('ln1',180,1500),('wp2',220,1500),('lp2',180,1500),('wn2',220,1500),('ln2',180,1500)],
 'bbm': [('lp1',180,1500),('wn1',220,800),('ln1',180,600),('wpt',220,800),('lpt',180,1500),('lnf',180,1500),('lp2',180,600),('ln2',180,600)]}
def mk(kind, x):
    p = {k: v for (k, _, _), v in zip(SPECS[kind], x)}
    if kind == 'conventional': p.update(wp1=220, wn1=220)
    return p
def obj(x, kind, target):
    m = sim(kind, mk(kind, x))
    if m is None or 'tplh' not in m or 'tphl' not in m or 'qtot' not in m: return 1e3
    tp = 0.5*(m['tplh'] + m['tphl'])*1e9; Q = m['qtot']/3*1e15
    pen = 2000*max(0, abs(tp/target - 1) - 0.02) + 300*max(0, abs(m['tplh']-m['tphl'])/(tp*1e-9) - 0.15)
    pen += 300*max(0, 1.70 - m['vout_max']) + 300*max(0, m['vout_min'] - 0.10)
    if kind == 'bbm':
        pen += 300*(max(0, 1.65-m['a_max']) + max(0, 1.65-m['b_max']) + max(0, m['a_min']-0.10) + max(0, m['b_min']-0.10))
        for k in ('t_iso_fall_b_to_a', 't_iso_rise_a_to_b'):
            if k not in m or m[k] <= 0: pen += 100
    return Q + pen
if __name__ == '__main__':
    for target in map(float, sys.argv[1:]):
        out = {}
        for kind in ('conventional', 'bbm'):
            b = [(lo, hi) for _, lo, hi in SPECS[kind]]
            r = differential_evolution(obj, b, args=(kind, target), maxiter=14, popsize=7, seed=1, polish=False,
                                       tol=1e-3, mutation=(0.5, 1.0), recombination=0.8, init='sobol')
            out[kind] = dict(params={k: round(v) for (k, _, _), v in zip(SPECS[kind], r.x)}, obj=r.fun, nfev=r.nfev)
            print(target, kind, out[kind], flush=True)
        json.dump(out, open(os.path.join(RES, 'opt_%g.json' % target), 'w'), indent=1)
