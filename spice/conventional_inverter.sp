* conventional_inverter.sp
* REFERENCE circuit: standard CMOS delay cell = 4 cascaded static CMOS inverters
* (paper Fig. 9(a)): input unit inv -> inv1 (w,l) -> inv2 (w,l) -> output unit inv -> CL
* Sizing of inv1/inv2 = the paper's Tp=750 ps "std." sizing (Fig. 11 caption).
.include models_180nm_L1.lib
.param vdd=1.8 cl=2f per=20n pw=10n tedge=50p
* ---- sizing (override with .param edits by the runner) ----
.param wp1=220n lp1=370n wn1=220n ln1=880n  wp2=880n lp2=730n wn2=1050n ln2=1320n
.param wpu=860n wnu=220n lu=180n
.temp 27

.subckt cinv in out vdd vss wn=220n wp=860n lnn=180n lpp=180n
MP out in vdd vdd pmos w={wp} l={lpp} ad={0.8u*wp} as={0.8u*wp} pd={1.5u+wp} ps={1.5u+wp}
MN out in vss 0   nmos w={wn} l={lnn} ad={0.8u*wn} as={0.8u*wn} pd={1.5u+wn} ps={1.5u+wn}
.ends

* each stage has its own 0 V-offset supply so per-stage charge can be measured
Vdd1 s1 0 dc {vdd}
Vdd2 s2 0 dc {vdd}
Vdd3 s3 0 dc {vdd}
Vdd4 s4 0 dc {vdd}
Vg1 g1 0 dc 0
Vg2 g2 0 dc 0
Vg3 g3 0 dc 0
Vg4 g4 0 dc 0
Vin in 0 pulse(0 {vdd} 1n {tedge} {tedge} {pw} {per})
X1 in  n1  s1 g1 cinv wn={wnu} wp={wpu} lnn={lu} lpp={lu}
X2 n1  n2  s2 g2 cinv wn={wn1} wp={wp1} lnn={ln1} lpp={lp1}
X3 n2  n3  s3 g3 cinv wn={wn2} wp={wp2} lnn={ln2} lpp={lp2}
X4 n3  out s4 g4 cinv wn={wnu} wp={wpu} lnn={lu} lpp={lu}
CL out 0 {cl}

.tran 1p 101n 0 2p
.options reltol=1e-4 abstol=1e-14 vntol=1e-7 chgtol=1e-17 method=gear
.control
set filetype=ascii
run
let itot = -(vdd1#branch+vdd2#branch+vdd3#branch+vdd4#branch)
let i3 = -vdd3#branch
let i3g = vg3#branch
meas tran tpLH trig v(in) val=0.9 rise=3 targ v(out) val=0.9 rise=3
meas tran tpHL trig v(in) val=0.9 fall=3 targ v(out) val=0.9 fall=3
meas tran qtot  integ itot from=21n to=101n
meas tran q_st3 integ i3 from=21n to=101n
meas tran vout_max max v(out) from=21n to=101n
meas tran vout_min min v(out) from=21n to=101n
meas tran ipk3 max i3 from=21n to=101n
wrdata ../results/conv_wave.csv v(in) v(n1) v(n2) v(n3) v(out) itot i3 i3g
.endc
.end
