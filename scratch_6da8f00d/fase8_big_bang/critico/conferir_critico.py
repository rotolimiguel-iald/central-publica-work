# -*- coding: utf-8 -*-
"""Crítico de completude — Fase 8. Reconfere por script os números que as quatro lentes repetem.
β nunca literal: α lido do um.py por regex."""
import re, math, json, hashlib, io, os
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
raw = open(UM, "rb").read()
sha = hashlib.sha256(raw).hexdigest()
txt = raw.decode("utf-8", errors="replace")
m = re.search(r"SEALED_CODATA_ALPHA\s*=\s*([0-9.eE+-]+)", txt)
alpha = float(m.group(1))
beta = alpha * math.sqrt(math.e)
ver = re.search(r'UM_VERSION\s*=\s*"(v\d+)"', txt)
out = {"um_py_sha256_16": sha[:16], "um_version": ver.group(1) if ver else None,
       "alpha_regex": alpha, "beta": beta}
# lei por era
out["delta_rad"] = 4*beta/3; out["delta_mat"] = beta; out["delta_lambda"] = 0.0
# N_eff dial (época CMB)
F = (7/8)*(4/11)**(4/3); N_SM = 3.044
dNdb = (4/3)*(1+F*N_SM)/F
dN = dNdb*beta
out["F"] = F; out["dNeff_dbeta"] = dNdb; out["Delta_Neff_CMB"] = dN; out["Neff_TGL"] = N_SM+dN
# conta da gerência
out["Delta_Neff_gerencia"] = out["delta_rad"]*(1+F*N_SM)/F
# época BBN (g* = 10.75; uma espécie de neutrino = 7/8*2 = 1.75)
out["Delta_Nnu_BBN_gstar_10p75"] = out["delta_rad"]*10.75/1.75
# época do D (após aniquilação e±): fração por espécie = F/(1+F*N_SM)·... = mesma do CMB
out["Delta_Nnu_pos_aniquilacao"] = dN
# speed-up
S = math.sqrt(1+4*beta/3); out["S_BBN"] = S; out["S_minus_1"] = S-1
# tensões (medidas transcritas no frozen — [DECLARADO]; só para conferir a aritmética das lentes)
med = [("Planck18 TTTEEE+lowE",2.92,0.19),("Planck18 +lens+BAO",2.99,0.17),("ACT DR6+Planck",2.86,0.13),("ACT+Planck+BBN",2.89,0.11),("CMB-SPA",2.97,0.12)]
out["tensoes"] = [{"f":f,"Delta/sigma":dN/s,"z_TGL_vs_centro":abs(N_SM+dN-o)/s,"z_SM_vs_centro":abs(N_SM-o)/s} for f,o,s in med]
out["sigma_Neff_5sigma_centro_padrao"] = dN/5
out["sigma_Neff_5sigma_centro_2p97"] = (N_SM+dN-2.97)/5
out["S4_0p03_centro_padrao"] = dN/0.03
out["S4_0p03_centro_2p97"] = (N_SM+dN-2.97)/0.03
# D/H: as três escalas das lentes
DH, sDH = 2.527e-5, 0.030e-5
for nome, k in [("sessao_0p57",0.57),("steigman_1p57",1.57),("cyburt_1p618",1.618)]:
    dln = k*math.log(S)
    out[f"DH_dln_{nome}"] = dln
    out[f"DH_z_soobs_{nome}"] = dln/(sDH/DH)
    out[f"sigma_beta_soobs_{nome}"] = (sDH/DH)/(k*(4/3)/2)  # d ln DH/dβ ≈ k·(4/3)/2 em β→0
# mapa B
out["mapa_B_rho_m_sobre_rho_r_T1MeV_ordem"] = "1e-6..1e-7 (lentes: 1.12e-6 vs 8.0e-7 — difere pela definição de z(T); ambos ~1e-8 em dH/H)"
# contagem no um.py
out["um_py_count_big_bang"] = len(re.findall(r"big bang", txt, flags=re.I))
out["um_py_count_2p527"] = len(re.findall(r"2\.527", txt))
out["um_py_count_0p57_steigman"] = len(re.findall(r"0\.57", txt))
out["um_py_has_tens_now_1p61"] = bool(re.search(r"tens_now\s*=\s*1\.61", txt))
out["um_py_has_tens_act_2p49"] = bool(re.search(r"tens_act\s*=\s*2\.49", txt))
out["um_py_count_Aver"] = len(re.findall(r"Aver", txt))
out["um_py_count_0p2449"] = len(re.findall(r"0\.2449", txt))
out["um_py_count_0p2453"] = len(re.findall(r"0\.2453", txt))
out["um_py_count_Cyburt"] = len(re.findall(r"Cyburt", txt))
out["um_py_count_Steigman"] = len(re.findall(r"Steigman", txt))
json.dump(out, io.open(os.path.join(os.path.dirname(__file__),"NUMEROS_CRITICO.json"),"w",encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
