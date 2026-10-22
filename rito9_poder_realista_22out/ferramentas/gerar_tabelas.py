"""Gera tabelas em markdown (tabelas.md) a partir dos dados crus da rodada e do veredito. So leitura dos dados.

Uso: python gerar_tabelas.py <dir_work>
"""
import csv
import json
import math
import os
import statistics
import sys

W = sys.argv[1]
S = os.path.join(W, "saida_rodada")


def rd(p):
    with open(p, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


casos = rd(os.path.join(S, "n_req_por_caso.csv"))
der = {r["case_id"]: r for r in rd(os.path.join(W, "derivados_KK_por_caso.csv"))}
ver = json.load(open(os.path.join(W, "veredito.json"), encoding="utf-8"))
pr = json.load(open(os.path.join(W, "PREREGISTRO.json"), encoding="utf-8"))
mc = rd(os.path.join(S, "verificacao_mc.csv"))
rob = rd(os.path.join(S, "robustez_numerica.csv"))
ELLS = [10, 20, 30]


def n(r):
    return int(r["n_req"]) if r["n_req"] != "" else None


def fmt(x, d=3):
    if x is None:
        return "NA"
    if isinstance(x, float):
        if x != 0 and (abs(x) >= 1e5 or abs(x) < 1e-2):
            return f"{x:.3g}"
        return f"{x:.{d}g}"
    return str(x)


out = []
P = out.append

# ---- A: n_req por familia e ell
P("### A. n_req (neutrinos detectados necessarios; oraculo) por familia e ell: minimo / mediana / maximo\n")
P("| familia | ell = 10 km | ell = 20 km | ell = 30 km |")
P("|---|---|---|---|")
for fam in ("P1", "P2", "P3", "REF_ESQUELETO", "SENS_VETO", "SENS_ZERO"):
    cells = []
    for ell in ELLS:
        ns = sorted(n(r) for r in casos if r["familia"] == fam and float(r["ell_km"]) == ell and n(r) is not None)
        cells.append("NA" if not ns else f"{ns[0]} / {ns[len(ns)//2]} / {ns[-1]}")
    P(f"| {fam} | " + " | ".join(cells) + " |")
P("")

# ---- B: P2 por tau e f (ell=20), min-max sobre a forma do surto
P("### B. P2 (ell = 20 km): n_req min–max sobre as 16 formas de surto, por (tau, f)\n")
P("| tau (ms) | f = 0.5 | f = 0.8 |")
P("|---|---|---|")
for tau in (30, 100, 300, 1000):
    cells = []
    for f in (0.5, 0.8):
        ns = sorted(n(r) for r in casos if r["familia"] == "P2" and float(r["ell_km"]) == 20 and float(r["tau_ms"]) == tau and float(r["f_tail"]) == f)
        cells.append(f"{ns[0]}–{ns[-1]} (med {ns[len(ns)//2]})")
    P(f"| {tau} | " + " | ".join(cells) + " |")
P("")
P("P2, mesma tabela para ell = 10 e 30 km (min–max sobre a forma do surto):\n")
P("| ell | tau (ms) | f = 0.5 | f = 0.8 |")
P("|---|---|---|---|")
for ell in (10, 30):
    for tau in (30, 100, 300, 1000):
        cells = []
        for f in (0.5, 0.8):
            ns = sorted(n(r) for r in casos if r["familia"] == "P2" and float(r["ell_km"]) == ell and float(r["tau_ms"]) == tau and float(r["f_tail"]) == f)
            cells.append(f"{ns[0]}–{ns[-1]}")
        P(f"| {ell} | {tau} | " + " | ".join(cells) + " |")
P("")

# ---- C: melhores e piores casos P1 e P2
P("### C. Melhor e pior caso por familia realista e ell\n")
P("| familia | ell | melhor caso | n_req | pior caso | n_req |")
P("|---|---|---|---|---|---|")
for fam in ("P1", "P2"):
    for ell in ELLS:
        sub = [r for r in casos if r["familia"] == fam and float(r["ell_km"]) == ell and n(r) is not None]
        b = min(sub, key=n)
        w = max(sub, key=n)
        P(f"| {fam} | {ell} | {b['perfil_id']} | {n(b)} | {w['perfil_id']} | {n(w)} |")
P("")

# ---- D: REF vs esqueleto do Kimi
sk = json.load(open("C:\\Users\\rotol\\Documents\\kimi\\workspace\\estudo_iald_qg\\ferramentas\\estudo_poder_esqueleto.json", encoding="utf-8"))
P("### D. Bancada REF (H0 = N(0, sigma_e) do esqueleto do Kimi): criterio EXATO x CLT do esqueleto\n")
P("| ell (km) | sigma_e (ms) | n_req exato (este estudo) | n_5sigma LLR-CLT (esqueleto) | n_5sigma media (esqueleto) |")
P("|---|---|---|---|---|")
for ell in ELLS:
    for se in (0.5, 1.0, 3.0, 10.0):
        mine = [r for r in casos if r["familia"] == "REF_ESQUELETO" and float(r["ell_km"]) == ell and abs(float(r["gamma_ms"]) * 0.42466090014400953 - se) < 1e-6]
        e_llr = [x for x in sk["tabela_llr"] if x["ell_km"] == ell and x["sigma_e_ms"] == se][0]["n_5sigma"]
        e_med = [x for x in sk["tabela_media"] if x["ell_km"] == ell and x["sigma_e_ms"] == se][0]["n_5sigma"]
        P(f"| {ell} | {se:g} | {n(mine[0])} | {e_llr} | {e_med} |")
P("")

# ---- E: SENS_VETO e SENS_ZERO
P("### E. Sensibilidades (fora do veredito)\n")
P("SENS_VETO (surto K3_S10_G1_damped + cauda tau = 100 ms com fracao f; f = 0 e o P1 puro):\n")
P("| f (cauda) | ell = 10 | ell = 20 | ell = 30 | q1_sat (H1 em regiao 'impossivel' sob H0), ell = 20 |")
P("|---|---|---|---|---|")
base = [r for r in casos if r["familia"] == "P1" and r["perfil_id"] == "K3_S10_G1_damped"]
cells = [str(n([r for r in base if float(r['ell_km']) == ell][0])) for ell in ELLS]
q1 = [r for r in base if float(r["ell_km"]) == 20][0]["q1_sat"]
P(f"| 0 (P1) | " + " | ".join(cells) + f" | {float(q1):.3g} |")
for f in (0.001, 0.01, 0.1):
    sub = [r for r in casos if r["familia"] == "SENS_VETO" and float(r["f_tail"]) == f]
    cells = [str(n([r for r in sub if float(r['ell_km']) == ell][0])) for ell in ELLS]
    q1 = [r for r in sub if float(r["ell_km"]) == 20][0]["q1_sat"]
    P(f"| {f:g} | " + " | ".join(cells) + f" | {float(q1):.3g} |")
P("")
P("SENS_ZERO (ponto-zero conhecido so a menos de N(0, sigma_off^2) por evento; surto K4_S10_G1_damped):\n")
P("| sigma_off (ms) | P1-like ell=10 | ell=20 | ell=30 | P2-like (tau=100, f=0.8) ell=10 | ell=20 | ell=30 |")
P("|---|---|---|---|---|---|---|")
b1 = [r for r in casos if r["familia"] == "P1" and r["perfil_id"] == "K4_S10_G1_damped"]
b2 = [r for r in casos if r["familia"] == "P2" and r["perfil_id"] == "K4_S10_G1_damped_tau100_f0.8"]
P("| 0 (oraculo) | " + " | ".join(str(n([r for r in b1 if float(r['ell_km']) == ell][0])) for ell in ELLS) + " | " +
  " | ".join(str(n([r for r in b2 if float(r['ell_km']) == ell][0])) for ell in ELLS) + " |")
for so in (0.5, 1.0, 2.0, 4.0):
    s1 = [r for r in casos if r["familia"] == "SENS_ZERO" and float(r["sigma_offset_ms"]) == so and float(r["f_tail"]) == 0.0]
    s2 = [r for r in casos if r["familia"] == "SENS_ZERO" and float(r["sigma_offset_ms"]) == so and float(r["f_tail"]) == 0.8]
    P(f"| {so:g} | " + " | ".join(str(n([r for r in s1 if float(r['ell_km']) == ell][0])) for ell in ELLS) + " | " +
      " | ".join(str(n([r for r in s2 if float(r['ell_km']) == ell][0])) for ell in ELLS) + " |")
P("")

# ---- F: parede K-K
KK = pr["taxa_KK"]
P("### F. A parede instrumental (Kyutoku–Kashiyama), em funcao de n_req — 1 Mt, R = 1 Mpc^-3 Myr^-1, D_eff = 200 Mpc\n")
P("| caso | ell | n_req | fusoes ate 200 Mpc | exposicao (Mt ano) | D_max de UM evento (Mpc) | massa p/ 10 eventos (Mt) | fator acima do alcance |")
P("|---|---|---|---|---|---|---|---|")
sel = []
for fam in ("P1", "P2", "P3"):
    for ell in ELLS:
        sub = [r for r in casos if r["familia"] == fam and float(r["ell_km"]) == ell and n(r) is not None]
        b = min(sub, key=n)
        sel.append(b)
for r in sel:
    d = der[r["case_id"]]
    def mil(x):
        return f"{float(x):,.0f}".replace(",", ".")
    P(f"| {r['familia']} {r['perfil_id']} | {r['ell_km']} | {r['n_req']} | {mil(d['fusoes_necessarias_ate_Deff'])} | {mil(d['exposicao_Mt_ano'])} | "
      f"{float(d['Dmax_um_evento_Mpc']):.2f} | {mil(d['massa_detector_Mt_para_max_eventos'])} | {mil(d['fator_acima_do_alcance'])} |")
P("")
P("(melhor caso = menor n_req dentro de cada familia e ell; P3 mostrado so para registro: o rendimento real e MENOR — ver texto.)\n")

# ---- G: verificacoes
P("### G. Verificacoes numericas\n")
dc = [abs(float(r["c_hat_mc"]) - float(r["c_lattice"])) for r in mc if r.get("c_hat_mc") not in ("", None) and r["c_hat_mc"] != "nan"]
dp = [abs(float(r["poder_mc"]) - float(r["poder_lattice"])) for r in mc if r.get("poder_mc") not in ("", None)]
P(f"- Simulacao por amostragem por importancia (M = {pr['verificacao_mc']['M']} por ponto, semente {pr['verificacao_mc']['seed_base']}): {len(mc)} pontos em "
  f"{len(set(r['case_id'] for r in mc))} casos; todos dentro da tolerancia: {all(r['ok'] == 'True' for r in mc)}; "
  f"max |c_MC - c_rede| = {max(dc):.3f} (tol {pr['verificacao_mc']['tol_c']}); max |poder_MC - poder_rede| = {max(dp):.4f}.")
dn = [abs(int(r["n_req_variante"]) - int(r["n_req_base"])) for r in rob if r.get("n_req_variante") not in ("", None)]
dcr = [abs(float(r["c_variante"]) - float(r["c_base"])) for r in rob if r.get("c_variante") not in ("", None)]
P(f"- Robustez numerica (cap 60; passo da rede / 2): {len(rob)} comparacoes; todas dentro da tolerancia: {all(r['ok'] == 'True' for r in rob)}; "
  f"max |n_req - n_req_base| = {max(dn)}; max |c - c_base| = {max(dcr):.4f}.")
P(f"- Gates do veredito: " + "; ".join(f"{k}={v}" for k, v in ver["gates"].items()))
P("")
with open(os.path.join(W, "tabelas.md"), "x", encoding="utf-8") as f:
    f.write("\n".join(out))
print("\n".join(out))
