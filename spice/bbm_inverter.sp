* bbm_inverter.sp
* OPTIMISED circuit: break-before-make (BBM) delay cell, paper Fig. 9(b) with the
* PtNf full-swing delay element of Fig. 8:
*   input unit inv -> [P1 / Pt / N1 + Nf  : CMOS->BBM converter, outputs A(po), B(no)]
*                  -> [P2 / N2            : BBM->CMOS converter (merge), output DO]
*                  -> output unit inv -> CL
* Pt : PMOS in triode (gate=GND, always ON) between A and B = bidirectional delay element
* Nf : NMOS level-restoration transistor between A and B, gate driven by DO (next-stage output)
* Sizing = the paper's PtNf Tp=750 ps sizing (Fig. 11 caption).
.include models_180nm_L1.lib
.param vdd=1.8 cl=2f per=20n pw=10n tedge=50p
.param wp1=220n lp1=740n wn1=390n ln1=180n  wpt=220n lpt=350n  wnf=220n lnf=950n
.param wp2=220n lp2=180n wn2=220n ln2=220n
.param wpu=860n wnu=220n lu=180n
.temp 27

.subckt cinv in out vdd vss wn=220n wp=860n lnn=180n lpp=180n
MP out in vdd vdd pmos w={wp} l={lpp} ad={0.8u*wp} as={0.8u*wp} pd={1.5u+wp} ps={1.5u+wp}
MN out in vss 0   nmos w={wn} l={lnn} ad={0.8u*wn} as={0.8u*wn} pd={1.5u+wn} ps={1.5u+wn}
.ends

Vdd1 s1 0 dc {vdd}
Vdd2 s2 0 dc {vdd}
Vdd3 s3 0 dc {vdd}
Vdd4 s4 0 dc {vdd}
Vg1 g1 0 dc 0
Vg2 g2 0 dc 0
Vg3 g3 0 dc 0
Vg4 g4 0 dc 0
Vin in 0 pulse(0 {vdd} 1n {tedge} {tedge} {pw} {per})
X1 in n1 s1 g1 cinv wn={wnu} wp={wpu} lnn={lu} lpp={lu}
* ---- stage 2: CMOS -> BBM converter (split output A,B) ----
MP1 A n1 s2 s2 pmos w={wp1} l={lp1} ad={0.8u*wp1} as={0.8u*wp1} pd={1.5u+wp1} ps={1.5u+wp1}
MN1 B n1 g2 0  nmos w={wn1} l={ln1} ad={0.8u*wn1} as={0.8u*wn1} pd={1.5u+wn1} ps={1.5u+wn1}
MPT A 0  B s2 pmos w={wpt} l={lpt} ad={0.8u*wpt} as={0.8u*wpt} pd={1.5u+wpt} ps={1.5u+wpt}
MNF A do B 0  nmos w={wnf} l={lnf} ad={0.8u*wnf} as={0.8u*wnf} pd={1.5u+wnf} ps={1.5u+wnf}
* ---- stage 3: BBM -> CMOS converter (split inputs A (PMOS gate), B (NMOS gate)) ----
MP2 do A s3 s3 pmos w={wp2} l={lp2} ad={0.8u*wp2} as={0.8u*wp2} pd={1.5u+wp2} ps={1.5u+wp2}
MN2 do B g3 0  nmos w={wn2} l={ln2} ad={0.8u*wn2} as={0.8u*wn2} pd={1.5u+wn2} ps={1.5u+wn2}
X4 do out s4 g4 cinv wn={wnu} wp={wpu} lnn={lu} lpp={lu}
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
* node A (PMOS gate of stage 3) and B (NMOS gate of stage 3) levels -> full swing check
meas tran A_max max v(A) from=21n to=101n
meas tran A_min min v(A) from=21n to=101n
meas tran B_max max v(B) from=21n to=101n
meas tran B_min min v(B) from=21n to=101n
* isolation times: time between 50% crossings of the two skewed nodes
meas tran t_iso_fall_B_to_A trig v(B) val=0.9 fall=3 targ v(A) val=0.9 fall=3
meas tran t_iso_rise_A_to_B trig v(A) val=0.9 rise=3 targ v(B) val=0.9 rise=3
wrdata ../results/bbm_wave.csv v(in) v(n1) v(A) v(B) v(do) v(out) itot i3 i3g
.endc
.end
