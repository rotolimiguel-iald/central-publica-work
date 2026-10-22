# -*- coding: utf-8 -*-
"""poder_cego_ramo_b.py -- PODER AS CEGAS do ramo B do ringdown (tau* = k GM/c^3), calculado SO com as sigmas publicadas por evento
e com o spin do remanescente (entrada da previsao de Kerr). NUNCA le nem imprime valores centrais de dtau220 (medianas/quantis).
beta nunca literal: alpha lido do um.py canonico por regex; beta = alpha*sqrt(e) em runtime. Saida: PODER_CEGO_RAMO_B.json ao lado.
Lente: pre_registro (rascunho V1 do ramo B), 05/10/2026. Somente leitura fora desta pasta."""
import json, hashlib, math, re, os, datetime
R = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "PODER_CEGO_RAMO_B.json")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def load(p):
    return json.load(open(p, encoding="utf-8")), sha(p)


# --- beta em runtime, alpha lido do um.py (nunca digitado aqui)
src = open(UM, encoding="utf-8", errors="replace").read(2000000)
alpha = float(re.search(r"^SEALED_CODATA_ALPHA\s*=\s*([0-9.eE+-]+)", src, re.M).group(1))
G = float(re.search(r"^G_NEWTON\s*=\s*([0-9.eE+-]+)", src, re.M).group(1))
C = float(re.search(r"^C_LIGHT\s*=\s*([0-9.eE+-]+)", src, re.M).group(1))
H = float(re.search(r"^H_PLANCK_EXACT\s*=\s*([0-9.eE+-]+)", src, re.M).group(1))
HBAR = H / (2 * math.pi)
beta = alpha * math.sqrt(math.e)
tP = math.sqrt(HBAR * G / C ** 5)
MSUN = 1.98892e30  # [KNOWN] so para o numero ilustrativo de GM/c^3 em segundos


# --- Berti-Cardoso-Will 2006, l=m=2, n=0 [KNOWN]; os mesmos coeficientes que o um.py usa (um.py:155704)
def bcw220(a):
    mw = 1.5251 - 1.1568 * (1 - a) ** 0.1292
    q = 0.7000 + 1.4187 * (1 - a) ** (-0.4990)
    return mw, q


def k_kms(a):  # 2pi/kappa em unidades de GM/c^3, Kerr: kappa = sqrt(1-a^2) / (2 M (1 + sqrt(1-a^2)))
    s = math.sqrt(1 - a * a)
    return 4 * math.pi * (1 + s) / s


# --- as sigmas por evento: desvio-padrao completo do posterior (ddof=1) do arquivo E0 (NAO se le mean_df/median_df)
e0, h_e0 = load(os.path.join(R, "bis", "E0_ROUTE_IV_POWER_v2.json"))
sig_std = {r["event"]: float(r["sigma_tau"]) for r in e0["per_event"]}
# --- catalogo C4 GWTC-5.0: so a LARGURA 90% de dtau220 (q95-q05) e o spin (q05,q50,q95); a mediana de dtau220 nao e lida
cat, h_cat = load(os.path.join(R, "C4_CATALOG_220.json"))
comb, h_comb = load(os.path.join(R, "C4_CATALOG_COMBINATION.json"))
sel31 = list(comb["selected_events"])
ctrl2 = list(comb["additional_control_events"])
rows = {}
for r in cat["rows"]:
    q = r["quantiles"]
    dt = q["dtau220"]
    sp = q["spin"]
    rows[r["event"]] = dict(width90=float(dt[2] - dt[0]), spin_q05=float(sp[0]), spin_q50=float(sp[1]), spin_q95=float(sp[2]), N=int(r["N"]))
# --- GWTC-3 (18; 10 selecionados pelos autores): so largura e spin
g3, h_g3 = load(os.path.join(R, "C4_GWTC3_220.json"))
sel3, h_sel3 = load(os.path.join(R, "C4_GWTC3_SELECTION.json"))
rows3 = {}
for r in g3["rows"]:
    q = r["quantiles"]
    dt = q["dtau220"]
    sp = q["spin"]
    rows3[r["event"]] = dict(width90=float(dt[2] - dt[0]), spin_q50=float(sp[1]), N=int(r["N"]))
# --- GW250114 (release da descoberta, Zenodo 17018009): so largura e spin
ini, h_ini = load(os.path.join(R, "C4_220_INITIAL.json"))
w_ini = float(ini["quantiles"]["dtau220"][2] - ini["quantiles"]["dtau220"][0])
a_ini = float(ini["quantiles"]["spin_non_evolved"][1])
Z90 = 2 * 1.6448536269514722  # largura 90% de uma gaussiana em unidades de sigma


def ensemble(events, sig_of, spin_of, k_fn):
    W = 0.0
    S = 0.0
    per = []
    for ev in events:
        s = sig_of(ev)
        a = spin_of(ev)
        mw, q = bcw220(a)
        N = mw * q
        k = k_fn(a)
        d = -beta * k * N
        w = 1.0 / s ** 2
        W += w
        S += w * d
        per.append(dict(event=ev, sigma=s, spin_q50=a, Momega220=mw, Q220=q, N_a=N, k=k, delta_pred=d))
    sc = 1 / math.sqrt(W)
    dbar = S / W
    return dict(n=len(events), sigma_comb=sc, delta_pred_weighted=dbar, power=abs(dbar) / sc, I_tau=W, per_event=per)


cands = {"k=1 (GM/c^3)": lambda a: 1.0,
         "k=2 (2GM/c^3 = r_s/c)": lambda a: 2.0,
         "k=4pi (2 pi r_s/c)": lambda a: 4 * math.pi,
         "k=8pi (hbar/k_B T_H, a=0)": lambda a: 8 * math.pi,
         "k=2pi/kappa(a_f) (KMS de Kerr)": k_kms}
out = dict(gerado=datetime.datetime.now().astimezone().isoformat(), script=os.path.basename(__file__), script_sha256=sha(os.path.abspath(__file__)),
           cegueira="so sigmas (std ddof=1 do posterior; e largura 90% de dtau220 como controle) e spin; NENHUM valor central de dtau220 lido ou impresso",
           beta=beta, alpha_lido_do_um_py=alpha, t_planck_s=tP, GMsun_over_c3_s=G * MSUN / C ** 3,
           fontes={"E0_ROUTE_IV_POWER_v2.json": h_e0, "C4_CATALOG_220.json": h_cat, "C4_CATALOG_COMBINATION.json": h_comb,
                   "C4_GWTC3_220.json": h_g3, "C4_GWTC3_SELECTION.json": h_sel3, "C4_220_INITIAL.json": h_ini, "um.py": sha(UM)},
           selecao={"GWTC5_31": sel31, "GWTC5_controles_2": ctrl2, "GWTC3_10": sel3["selected_events"], "GWTC3_todos": list(rows3.keys())},
           largura90_vs_std={ev: dict(width90_over_3p29=rows[ev]["width90"] / Z90, std_ddof1=sig_std.get(ev)) for ev in sel31 if ev in rows},
           GW250114_release_descoberta=dict(sigma_from_width90=w_ini / Z90, spin_q50=a_ini, N_a=bcw220(a_ini)[0] * bcw220(a_ini)[1]),
           resultados={})
for nome, kf in cands.items():
    out["resultados"][nome] = {
        "GWTC5_31_std": ensemble(sel31, lambda e: sig_std[e], lambda e: rows[e]["spin_q50"], kf),
        "GWTC5_31_width90": ensemble(sel31, lambda e: rows[e]["width90"] / Z90, lambda e: rows[e]["spin_q50"], kf),
        "GWTC5_33_std": ensemble(sel31 + ctrl2, lambda e: sig_std[e], lambda e: rows[e]["spin_q50"], kf),
        "GWTC3_10_width90": ensemble(sel3["selected_events"], lambda e: rows3[e]["width90"] / Z90, lambda e: rows3[e]["spin_q50"], kf),
        "GW250114_sozinho_width90": ensemble(["GW250114_082203"], lambda e: w_ini / Z90, lambda e: a_ini, kf),
    }
# fracao por realizacao (difusao de fase), DECLARADO pelo verificador de 28/09 (razao 0,273 +- 0,06): poder x 0,27
out["fator_realizacao_difusao_de_fase_DECLARADO"] = 0.273
# controle nulo: ramo canonico tau* = t_Planck, GW150914-like (f=250 Hz, tau_GR=4 ms)
om = 2 * math.pi * 250.0
out["controle_ramo_canonico_delta"] = -0.5 * beta * tP * om ** 2 * 0.004
# clausula de sistematica (Fase 6, regra 2): sist_rel = sigma_sys/|delta_pred| > 0,3 -> INCONCLUSIVE; sigma_sys de familia da 013-bis ~ 0,03 (SYSTEMATICS_ADENDO)
d1 = abs(out["resultados"]["k=1 (GM/c^3)"]["GWTC5_31_std"]["delta_pred_weighted"])
out["k_minimo_para_sist_rel_0p3"] = {"sigma_sys_0p029": 0.029 / 0.3 / d1, "sigma_sys_0p038": 0.038 / 0.3 / d1}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("beta =", beta, "| t_P =", tP, "| GMsun/c^3 =", out["GMsun_over_c3_s"], "s")
print("controle canonico delta (250 Hz, 4 ms) =", out["controle_ramo_canonico_delta"])
print("GW250114 (release): sigma(width90/3.29) = %.4f ; a_f = %.4f ; N(a) = %.4f" % (out["GW250114_release_descoberta"]["sigma_from_width90"], a_ini, out["GW250114_release_descoberta"]["N_a"]))
for nome, res in out["resultados"].items():
    print("\n##", nome)
    for conj, r in res.items():
        print("  %-26s n=%2d  sigma_comb=%.5f  delta_pred=%+.5f  PODER=%6.2f sigma  (x0.273 realizacao: %5.2f)" % (conj, r["n"], r["sigma_comb"], r["delta_pred_weighted"], r["power"], r["power"] * 0.273))
print("\nk minimo para sist_rel <= 0,3:", out["k_minimo_para_sist_rel_0p3"])
print("\nTABELA (31; so sigma e spin): evento | std | w90/3.29 | a_f | N(a) | k_KMS(a)")
for p in out["resultados"]["k=2pi/kappa(a_f) (KMS de Kerr)"]["GWTC5_31_std"]["per_event"]:
    print("  %-18s %.4f  %.4f  %.3f  %.3f  %.2f" % (p["event"], p["sigma"], rows[p["event"]]["width90"] / Z90, p["spin_q50"], p["N_a"], p["k"]))
print("saida:", OUT, sha(OUT)[:16])
