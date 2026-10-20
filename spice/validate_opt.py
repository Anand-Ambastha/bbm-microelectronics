#!/usr/bin/env python3
"""validate_opt.py - re-run optimised sizings (../results/opt_<target>.json) with the full main testbench"""
import json, glob, os, run_all as r
O = {}
for f in sorted(glob.glob(os.path.join(r.RES, 'opt_*.json'))):
    t = os.path.basename(f)[4:-5]; d = json.load(open(f)); O[t] = {}
    for kind, net in (('conventional', 'conventional_inverter.sp'), ('bbm', 'bbm_inverter.sp')):
        p = d[kind]['params']; over = {k: '%dn' % v for k, v in p.items()}
        if kind == 'conventional': over.update(wp1='220n', wn1='220n')
        m = r.run(net, over, tag='opt_%s_%s' % (t, kind), keep_wave=False)
        if t == '0.5':
            for s in ('conv_wave.csv', 'bbm_wave.csv'):
                src = os.path.join(r.RES, s); os.replace(src, os.path.join(r.RES, 'opt0.5_' + s)) if False else None
        met = r.metrics(m)
        if kind == 'bbm': met.update(A_max=m['a_max'], A_min=m['a_min'], B_max=m['b_max'], B_min=m['b_min'], t_iso_fall_ps=m['t_iso_fall_b_to_a']*1e12, t_iso_rise_ps=m['t_iso_rise_a_to_b']*1e12)
        O[t][kind] = dict(params=p, metrics=met)
json.dump(O, open(os.path.join(r.RES, 'summary_opt.json'), 'w'), indent=1)
for t in O:
    c, b = O[t]['conventional']['metrics'], O[t]['bbm']['metrics']
    print(t, 'conv Tp=%.0f Q=%.1f PDP=%.3f | bbm Tp=%.0f Q=%.1f PDP=%.3f | Qsave=%.1f%%' % (c['Tp_ps'], c['Q_fC_per_cycle'], c['PDP_fJ'], b['Tp_ps'], b['Q_fC_per_cycle'], b['PDP_fJ'], 100*(1-b['Q_fC_per_cycle']/c['Q_fC_per_cycle'])))
