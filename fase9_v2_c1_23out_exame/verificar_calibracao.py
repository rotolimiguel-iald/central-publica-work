# -*- coding: utf-8 -*-
"""verificar_calibracao.py -- auditoria c1 (23/10/2026), item 4: (a) os limiares brutos equivalentes recomputados com o fundo REAL (qualificacao) batem
com o recibo; (b) SEM vazamento de centro: com os H0 dos leitores trocados por NaN (e por valores absurdos) os limiares e os taus sao identicos;
(c) o mapeamento 6,37 <-> 5 sigma calibrado (p bilateral = 2 Phi(-5)) e o 5 bruto <-> 3,94; (d) o mapa z_delta(u) e' monotono;
(e) MC independente PEQUENO pelo pipeline completo (endpoint_statistics) com y sorteado da nula TGL e covariancia verdadeira = canto (1,1).
Nenhum centro observado entra. python -P -E -B -X utf8 verificar_calibracao.py [n_mc]"""
import sys, os, json, math, copy, time
sys.dont_write_bytecode = True
PK = r"C:\IALD\Central de Patentes\work\fase9_v2_c1_23out"
sys.path.insert(0, os.path.join(PK, "runner"))
import numpy as np
from scipy import stats as sps
import f9v2_calibration as CAL, f9v2_stats as ST
spec = json.load(open(os.path.join(PK, "spec", "PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json"), encoding="utf-8"))["spec"]
bgd = json.load(open(os.path.join(PK, "testes", "QUALIFICACAO_FORNECEDOR_REAL.json"), encoding="utf-8"))["fundo"]
rec = json.load(open(os.path.join(PK, "calibracao", "CALIBRACAO_CAUDA_RECIBO.json"), encoding="utf-8"))
R = {"modo_spec": spec["calibracao_de_cauda"]["modo"]}
live = CAL.primary_thresholds(spec, bgd, "sup_caixa")
R["limiares_vivos_sup"] = live; R["recibo"] = rec["limiares_equivalentes_P_primaria_BG1"]
R["limiares_iguais_ao_recibo"] = all(abs(live[k] - rec["limiares_equivalentes_P_primaria_BG1"][k]) <= 1e-6 * abs(live[k]) for k in live)
for nome, val in (("nan", float("nan")), ("absurdo_1000", 1000.0), ("zero", 0.0)):
    s2 = copy.deepcopy(spec)
    for r in s2["leitores"].values():
        r["H0"] = val
    l2 = CAL.primary_thresholds(s2, bgd, "sup_caixa")
    R["sem_vazamento_" + nome] = l2 == live
# taus, mapa, p
consts = {k: v for k, v in spec["S5_propagacao"]["constantes_E"].items() if k != "origem"}
lei = spec["lei"]; beta = spec["beta"]["alpha_read"] * math.sqrt(math.e)
law = ST.Law(beta, lei["K_frozen_V1"], ST.lnE_pinned(lei["Omega_m"], lei["Omega_r"], lei["z_star"]), bgd["bg1"]["H0"], bgd["bg1"]["cov_theta"], bgd["bg1"]["theta_H0_ombh2_omch2"], lei["z_star"], consts, s5=True)
ids = spec["familias"]["P_primaria"]["ids"]; sig = {k: v["sigma"] for k, v in spec["leitores"].items()}; amps = spec["covariancia"]["amplitudes_km_s_Mpc"]; grid = spec["covariancia"]["grid"]
ep = ST.grid_endpoints(amps, sig, ids, grid["lambda_N"], grid["lambda_T"])
tau = CAL.taus(amps, sig, ids, ep, law, grid["lambda_N"], grid["lambda_T"])
R["ids"] = ids; R["tau"] = {k: tau[k] for k in ("tau_f_sup", "tau_f_proprio", "tau_d_sup", "tau_d_proprio", "V_T", "V_L")}; R["tau_f_sup_em"] = tau["tau_f_sup_em"]
R["tau_iguais_recibo"] = all(abs(tau[k] - rec["analitico"]["tau"][k]) < 1e-12 for k in ("tau_f_sup", "tau_f_proprio", "tau_d_sup", "tau_d_proprio"))
# tau_f independente: max nos 4 cantos da caixa de w'Cw (Var e' linear em lambda) + V_T recomputado por g'Cth g
w = ep["minimum"]["weights"]
cantos = {(a, b): float(w @ ST.covariance(amps, sig, ids, a, b) @ w) for a in (0.0, 1.0) for b in (0.0, 1.0)}
g = law.K * (np.array([1.0, 0, 0]) + law.theta[0] * (2 * law.beta / 3) * law.gl)
VT_ind = float(g @ np.array(bgd["bg1"]["cov_theta"]) @ g)
R["tau_f_sup_independente_cantos"] = math.sqrt(max(cantos.values()) + VT_ind); R["cantos_var"] = {str(k): v for k, v in cantos.items()}
R["ponto_de_analise_min"] = [ep["minimum"]["lambda_N"], ep["minimum"]["lambda_T"]]
zmap = CAL.ZDeltaMap(ep["minimum"]["sigma_comb"], law)
R["mapa_monotono"] = zmap.monotone
p637 = zmap.p_two_sided(live["z_delta_bruto_para_5sigma_calibrado"], tau["tau_f_sup"])[0]
R["p_em_6_37_sup"] = p637; R["p_gauss_5sigma_bilateral"] = 2 * sps.norm.sf(5.0); R["z_cal_de_bruto_5_sup"] = zmap.z_cal(5.0, tau["tau_f_sup"]); R["z_cal_de_bruto_6_37_sup"] = zmap.z_cal(live["z_delta_bruto_para_5sigma_calibrado"], tau["tau_f_sup"])
# (e) MC pelo pipeline completo, nula TGL, C_verdadeira = canto (1,1)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
rng = np.random.default_rng(20261023)
C_true = ST.covariance(amps, sig, ids, 1.0, 1.0); VT = law.V(law.beta)
Y = rng.multivariate_normal(np.full(len(ids), law.K * law.mu), C_true + VT * np.ones((len(ids), len(ids))), size=n)
t0 = time.time(); zs = []
for y in Y:
    st = ST.endpoint_statistics(y, ids, ep["minimum"]["covariance"], law, bgd["fundo_livre"], fast=True)
    zs.append(np.nan if st["z_delta"] is None else st["z_delta"])
zs = np.abs(np.array(zs)); R["mc"] = {"n": n, "segundos": round(time.time() - t0, 1), "indefinidos": int(np.isnan(zs).sum())}
for t in (2.0, 3.0, 3.8, 5.0):
    k = int(np.nansum(zs >= t)); pa = zmap.p_two_sided(t, tau["tau_f_sup"])[0]
    R["mc"]["bruto_%.1f" % t] = {"mc_k": k, "mc_frac": k / n, "analitico_sup": pa, "esperado_k": pa * n, "z_pois": (k - pa * n) / math.sqrt(max(pa * n, 1e-9))}
print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
json.dump(R, open("VERIFICACAO_CALIBRACAO.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
