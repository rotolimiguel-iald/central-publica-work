# -*- coding: utf-8 -*-
"""Revisor terceiro: recalculo do zero. alfa CODATA 2018; beta = alfa*sqrt(e) em runtime; nada lido do candidato alem da comparacao final."""
import math, json, sys
sys.stdout.reconfigure(encoding="utf-8")
ALPHA_CODATA_2018 = 7.2973525693e-3
beta = ALPHA_CODATA_2018*math.sqrt(math.e)
s45 = math.sin(math.pi/4)
u=1.0
print("beta",beta)
m=beta*s45*u; print("m2 meV",m*1e3)
print("prop meV",beta*0.5*u*1e3, "razao",m/(beta*.5*u))
print("retida eV",beta*u,"transm",(1-beta)*u)
print("meio tom",math.exp(-.5),"tonica",math.exp(.5)*u,"E0",math.exp(-.5)*math.exp(.5)*u)
print("m formula", u*ALPHA_CODATA_2018*math.exp(.5)*s45*1e3)
print("razao m/E0",beta*s45)
hw=math.sqrt(2)*beta*u; print("hbar omega meV",hw*1e3,"meia",hw*.5e3)
hbc=197.3269804e-9 # eV m
R=beta*(u/hbc)**2; print("R m-2",R,"raio um",1e6/math.sqrt(R),"lambda um",2*math.pi*hbc/hw*1e6)
eV=1.602176634e-19; hbar=1.054571817e-34
print("K_si",(math.exp(.5)*u*eV)**3/hbar**2)
print("Ep/4pi eV", 1.220890e28/(4*math.pi), "Ep/sqrt2pi",1.220890e28/math.sqrt(2*math.pi))
# Moffatt
print("K/Mg2 com energia total 3/2 Mga alfa:",4*1.5,"so potencial:",4)
# GA com as constantes seladas da base
c=299792458.0;G=6.674e-11;MSUN=1.98892e30;MPC=3.0857e22
W=c**2/(4*math.pi*G); pm=W*MPC/MSUN
f=2*beta**2*pm; print("M/R",f,"v km/s",beta*c/math.sqrt(2*math.pi)/1e3)
print("M(57)",f*57,"R_cf4 p/ 1.98643e16",1.9864285664963284e16/f,"razao",f*57/1.9864285664963284e16)
print("2pi/beta",2*math.pi/beta)
print("MW x",f*.1/1e12,"GL x",f*1.5/5e12,"sen45:",f*.1/1e12*s45,f*1.5/5e12*s45,"M57 sen45",f*57*s45)
anc=5.4e16; print("sig",(anc-f*57)/5/anc,"beta/5",beta/5, "dec",math.log10(1e17/1e15))
for M in (5.4e16,1e15,1e17):
    Mk=M*MSUN;tau=4*math.pi*G*Mk/c**3;RB=c/(beta/tau);print(M,"tau",tau,"RB Mpc",RB/MPC,"RB/rs",RB/(2*G*Mk/c**2),"M volta",W*beta*RB/MSUN,"res",abs(W*beta*RB/MSUN-M)/M)
# o neutrino: Delta m21 para E0 pedido
for d in (7.42e-5,7.49e-5,7.50e-5,7.53e-5): print("sqrt(dm21)",math.sqrt(d)*1e3,"E0 pedido",math.sqrt(d)/(beta*s45))
