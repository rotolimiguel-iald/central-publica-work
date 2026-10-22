# -*- coding: utf-8 -*-
"""Reproducao independente (auditor) dos numeros das estrategias A/B/juiz a partir do core v391 e de beta de RUNTIME.
Nenhum dado observado novo: o unico centro e o que o core carrega. Nenhum literal de beta."""
import json, math, re, hashlib, os, datetime

UMPY = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/um.py"
alphas=[]
with open(UMPY,'rb') as fh:
    for k,ln in enumerate(fh,1):
        m=re.match(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9][0-9.eE+-]*)\s*$", ln.rstrip(b"\r\n"))
        if m: alphas.append((k,m.group(1).decode()))
assert len(alphas)==1
beta=float(alphas[0][1])*math.sqrt(math.e)
out={"beta":repr(beta),"alpha_linha":alphas[0][0]}
core=json.load(open("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N"+chr(0xF3)+"s/um_absoluto.json",encoding="utf-8"))
core=core.get("core",core)
hr=core["hubble_ratio_opening_v388"]["numbers"]
K=hr["H0_local_previsto"]/hr["H0_bg"]
out["K_do_core"]=K; out["lnK"]=math.log(K); out["lnE_zstar_implicito"]=math.log(K)/(2*beta/3)
hb,sb=hr["H0_bg"],0.301
def chi2min(c,s,k):
    # min_h [(c-k h)^2/s^2 + (h-hb)^2/sb^2]  (fundo perfilado)
    h=(c*k/s**2 + hb/sb**2)/(k**2/s**2+1/sb**2)
    return (c-k*h)**2/s**2+(h-hb)**2/sb**2
def zdisc(c,s): return math.sqrt(max(chi2min(c,s,1.0)-chi2min(c,s,K),0.0))
def zdelta(c,s): return (c-K*hb)/math.sqrt(s**2+(K*sb)**2)
c,s=hr["media_GLS_locais"],hr["sigma_GLS_locais"]
out["z_disc_reproduzido"]=zdisc(c,s); out["z_disc_core"]=hr["z_disc"]
out["z_delta_reproduzido_quadratura"]=zdelta(c,s); out["z_delta_core"]=hr["z_delta"]
out["poder_previo_centro_na_TGL_sigma_GLS"]=zdisc(K*hb,s)
# sigma_comb maxima para 5 sigma no centro do core
lo,hi=0.1,2.0
for _ in range(200):
    mid=(lo+hi)/2
    if zdisc(c,mid)>=5: lo=mid
    else: hi=mid
out["sigma_comb_max_para_5sigma_no_centro_do_core"]=lo
def centro_min(s):
    lo,hi=hb,80.0
    for _ in range(200):
        mid=(lo+hi)/2
        if zdisc(mid,s)>=5: hi=mid
        else: lo=mid
    return hi
out["centro_min_5sigma_sigma_0p9494_teto_P"]=centro_min(0.9494)
out["centro_min_5sigma_sigma_0p8635_teto_R25"]=centro_min(0.8635)
out["centro_min_5sigma_sigma_GLS"]=centro_min(s)
out["zdisc_centro_core_sigma_0p9494"]=zdisc(c,0.9494); out["zdisc_centro_core_sigma_0p8035"]=zdisc(c,0.8035)
out["zdisc_centro_core_sigma_0p8635"]=zdisc(c,0.8635); out["zdisc_centro_core_sigma_0p7494"]=zdisc(c,0.7494)
out["zdisc_centro_core_sigma_0p756"]=zdisc(c,0.756)
# N_eff
F=(7/8)*(4/11)**(4/3); NSM=3.044
dN=(4/3)*(1+F*NSM)/F*beta
out["F"]=F; out["dNeff"]=dN; out["dNeff_por_beta"]=dN/beta; out["S_BBN"]=math.sqrt(1+4*beta/3)
out["R_dNeff_over_lnK"]=dN/math.log(K); out["R_forma_fechada"]=2*(1+F*NSM)/(F*math.log(K)/(2*beta/3))
out["Neff_TGL"]=NSM+dN
for nome,sig in [("SO_baseline",0.055),("SO_goal",0.050),("SO_ASO",0.045),("S4",0.030),("alvo",0.0239)]:
    out["poder_Neff_"+nome]=dN/sig
    out["quadratura_par_5p913_"+nome]=math.hypot(5.913,dN/sig); out["quadratura_par_5p963_"+nome]=math.hypot(5.963,dN/sig)
out["Neff_TGL_vs_CMBSPA_2p82_0p12"]=(NSM+dN-2.82)/0.12; out["Neff_TGL_vs_2p96_0p24"]=(NSM+dN-2.96)/0.24
out["Neff_TGL_vs_Planck_2p99_0p17"]=(NSM+dN-2.99)/0.17
out["Neff_SO_baseline_se_2p82_persistir"]=(NSM+dN-2.82)/0.055
# m2
m2=beta*math.sin(math.pi/4)*1000.0
out["m2_meV"]=m2
out["m2_vs_JUNO_8p6603_0p0693"]=(8.6603-m2)/0.0693; out["m2_vs_NuFIT_8p6776_0p0576"]=(8.6776-m2)/0.0576; out["m2_vs_PDG_8p6776_0p1037"]=(8.6776-m2)/0.1037
out["m2_2031_centro_NuFIT_0p25pct"]=(8.6776-m2)/(0.0025*8.6776); out["m2_2031_centro_JUNO_0p25pct"]=(8.6603-m2)/(0.0025*8.6603)
out["precisao_que_mata_pct_em_Dm2_centro_NuFIT"]=2*100*(8.6776-m2)/5/8.6776
out["BG4_sobre_BG1_69p2_68p531"]=69.2/68.531; out["H0_local_com_BG4"]=K*69.2; out["z_delta_com_BG4"]=(c-K*69.2)/math.sqrt(s**2+(K*sb)**2)
out["sigma_beta_implicita_Hubble"]=hr["sigma_beta"]; out["beta_sobre_2"]=beta/2
json.dump(out,open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"medidas","numeros_auditor.json"),"w",encoding="utf-8"),indent=1)
for k,v in out.items(): print(k,"=",v)
