# -*- coding: utf-8 -*-
"""poder_cego_ramo_b_v2.py -- PODER AS CEGAS do ramo B do ringdown (tau* = k GM/c^3), v2 (05/10/2026, correcao G1 do critico).
Copia de poder_cego_ramo_b.py com TRES mudancas, todas ditas:
  (1) a previsao usa a forma EXATA  delta = -x/(1+x), x = beta*k*N(a)  (taxas somam: 1/tau_obs = 1/tau_GR + Gamma);
      a forma LINEAR delta = -x fica como coluna AO LADO (era a unica da v1; superestimava o poder dos k grandes em 35-40 %);
  (2) a lista de k e a tabela UNIFICADA do critico (G2): {1, 2, 4, 4pi, 8pi, 1/kappa(a), 2pi/kappa(a) sem co-rotacao,
      2pi/kappa(a) com co-rotacao omega -> omega - 2 Omega_H (R-MOD)}; os 5 nomes da v1 sao mantidos IDENTICOS para conferencia;
  (3) saidas novas: sigma(beta_lido) por k (1a ordem), k_min pelas DUAS regras de sistematica (Fase 6: sigma_sys/|delta| <= 0,3;
      fisica/013-bis: sigma_sys <= |delta|/5), N90 por escala, a tabela k x chi lida de RAMO_B_FISICA_TABELAS.json, e a
      conferencia com CRITICO_RECOMPUTO.json.
Cegueira: calculado SO com as sigmas publicadas por evento (std ddof=1 do posterior; largura 90 % como controle) e com o spin do
remanescente. NUNCA le nem imprime valores centrais de dtau220 (medianas/quantis centrais). Nenhuma deformacao registrada entra aqui.
beta nunca literal: alpha lido do um.py canonico por regex; beta = alpha*sqrt(e) em runtime. Saida: PODER_CEGO_RAMO_B_v2.json ao lado.
Lente: gerencia auxiliar (rascunho 2 do V1 do ramo B), 05/10/2026. Somente leitura fora desta pasta."""
import json, hashlib, math, re, os, datetime
R = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "PODER_CEGO_RAMO_B_v2.json")
FIS = os.path.join(HERE, "..", "fisica_do_ramo_b", "RAMO_B_FISICA_TABELAS.json")
CRIT = os.path.join(HERE, "..", "critico", "CRITICO_RECOMPUTO.json")
P5 = os.path.join(R, "RINGDOWN_5SIGMA_V1.json")


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


def kerr_kappa_hat(a):  # kappa em unidades de 1/M: sqrt(1-a^2) / (2 (1 + sqrt(1-a^2)))
    s = math.sqrt(1 - a * a)
    return s / (2 * (1 + s))


def kerr_omegaH_hat(a):  # Omega_H em unidades de 1/M: a / (2 (1 + sqrt(1-a^2)))
    s = math.sqrt(1 - a * a)
    return a / (2 * (1 + s))


def k_kms(a):  # 2pi/kappa em unidades de GM/c^3 = 4 pi (1+s)/s ; = kms_factor do um.py:155706 ; a=0 -> 8 pi
    return 2 * math.pi / kerr_kappa_hat(a)


def k_inv_kappa(a):  # 1/kappa em unidades de GM/c^3 = 2 (1+s)/s ; a=0 -> 4
    return 1.0 / kerr_kappa_hat(a)


def corot_factor(a):  # (F - 2 Omega_H) / F  com F = M omega_R (BCW); co-rotacao omega -> omega - m Omega_H, m = 2
    mw, _ = bcw220(a)
    return (mw - 2 * kerr_omegaH_hat(a)) / mw


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


def ensemble(events, sig_of, spin_of, k_fn, n_fn):
    """media ponderada 1/sigma^2 das previsoes por evento; devolve as DUAS formas (linear ao lado, exata e a que vale)."""
    W = 0.0
    S_lin = 0.0
    S_exa = 0.0
    S_kN = 0.0
    per = []
    for ev in events:
        s = sig_of(ev)
        a = spin_of(ev)
        mw, q = bcw220(a)
        N = n_fn(a, mw, q)
        k = k_fn(a)
        x = beta * k * N
        d_lin = -x
        d_exa = -x / (1 + x)
        w = 1.0 / s ** 2
        W += w
        S_lin += w * d_lin
        S_exa += w * d_exa
        S_kN += w * (k * N)
        per.append(dict(event=ev, sigma=s, spin_q50=a, Momega220=mw, Q220=q, N_a=N, k=k, x=x, delta_lin=d_lin, delta_exact=d_exa))
    sc = 1 / math.sqrt(W)
    dbar_lin = S_lin / W
    dbar_exa = S_exa / W
    kN_bar = S_kN / W
    return dict(n=len(events), sigma_comb=sc,
                delta_pred_weighted_exact=dbar_exa, power_exact=abs(dbar_exa) / sc,
                delta_pred_weighted_linear=dbar_lin, power_linear=abs(dbar_lin) / sc,
                ratio_exact_over_linear=(abs(dbar_exa) / sc) / (abs(dbar_lin) / sc),
                kN_weighted_mean=kN_bar,
                sigma_beta_lido_first_order=sc / kN_bar,          # sigma(beta_lido) ~ sigma_comb / <k N>_w  (dx/ddelta = -1/(1+delta)^2 ~ -1)
                sigma_beta_lido_over_beta=(sc / kN_bar) / beta,
                I_tau=W, per_event=per)


N_plain = lambda a, mw, q: mw * q
N_corot = lambda a, mw, q: mw * q * corot_factor(a) ** 2  # Gamma com (omega - 2 Omega_H)^2: N -> N * ((F-2Omega_H)/F)^2

# os 5 nomes da v1 IDENTICOS (conferencia com o critico) + os 3 da tabela unificada (G2)
cands = {
    "k=1 (GM/c^3)": (lambda a: 1.0, N_plain),
    "k=2 (2GM/c^3 = r_s/c)": (lambda a: 2.0, N_plain),
    "k=4 (1/kappa Schwarzschild = 4GM/c^3)": (lambda a: 4.0, N_plain),
    "k=4pi (2 pi r_s/c)": (lambda a: 4 * math.pi, N_plain),
    "k=8pi (hbar/k_B T_H, a=0)": (lambda a: 8 * math.pi, N_plain),
    "k=1/kappa(a_f) (Kerr)": (k_inv_kappa, N_plain),
    "k=2pi/kappa(a_f) (KMS de Kerr)": (k_kms, N_plain),
    "k=2pi/kappa(a_f) com co-rotacao omega->omega-2Omega_H (R-MOD)": (k_kms, N_corot),
}
out = dict(gerado=datetime.datetime.now().astimezone().isoformat(), script=os.path.basename(__file__), script_sha256=sha(os.path.abspath(__file__)),
           versao="v2 (05/10/2026): previsao EXATA -x/(1+x) como a que vale; LINEAR ao lado; 8 candidatos a k; sigma(beta_lido); k_min nas duas regras",
           cegueira="so sigmas (std ddof=1 do posterior; e largura 90% de dtau220 como controle) e spin; NENHUM valor central de dtau220 lido ou impresso; nenhuma deformacao registrada entra",
           beta=beta, alpha_lido_do_um_py=alpha, t_planck_s=tP, GMsun_over_c3_s=G * MSUN / C ** 3,
           fontes={"E0_ROUTE_IV_POWER_v2.json": h_e0, "C4_CATALOG_220.json": h_cat, "C4_CATALOG_COMBINATION.json": h_comb,
                   "C4_GWTC3_220.json": h_g3, "C4_GWTC3_SELECTION.json": h_sel3, "C4_220_INITIAL.json": h_ini, "um.py": sha(UM)},
           selecao={"GWTC5_31": sel31, "GWTC5_controles_2": ctrl2, "GWTC3_10": sel3["selected_events"], "GWTC3_todos": list(rows3.keys())},
           largura90_vs_std={ev: dict(width90_over_3p29=rows[ev]["width90"] / Z90, std_ddof1=sig_std.get(ev)) for ev in sel31 if ev in rows},
           GW250114_release_descoberta=dict(sigma_from_width90=w_ini / Z90, spin_q50=a_ini, N_a=bcw220(a_ini)[0] * bcw220(a_ini)[1],
                                            kappa_hat=kerr_kappa_hat(a_ini), OmegaH_hat=kerr_omegaH_hat(a_ini), k_kms=k_kms(a_ini),
                                            k_inv_kappa=k_inv_kappa(a_ini), corot_factor=corot_factor(a_ini)),
           resultados={})
for nome, (kf, nf) in cands.items():
    out["resultados"][nome] = {
        "GWTC5_31_std": ensemble(sel31, lambda e: sig_std[e], lambda e: rows[e]["spin_q50"], kf, nf),
        "GWTC5_31_width90": ensemble(sel31, lambda e: rows[e]["width90"] / Z90, lambda e: rows[e]["spin_q50"], kf, nf),
        "GWTC5_33_std": ensemble(sel31 + ctrl2, lambda e: sig_std[e], lambda e: rows[e]["spin_q50"], kf, nf),
        "GWTC3_10_width90": ensemble(sel3["selected_events"], lambda e: rows3[e]["width90"] / Z90, lambda e: rows3[e]["spin_q50"], kf, nf),
        "GW250114_sozinho_width90": ensemble(["GW250114_082203"], lambda e: w_ini / Z90, lambda e: a_ini, kf, nf),
    }
# fracao por realizacao (difusao de fase), DECLARADO pelo verificador de 28/09 (razao 0,273 +- 0,06): poder x 0,27
out["fator_realizacao_difusao_de_fase_DECLARADO"] = 0.273
# controle nulo: ramo canonico tau* = t_Planck, GW150914-like (f=250 Hz, tau_GR=4 ms)
om = 2 * math.pi * 250.0
out["controle_ramo_canonico_delta"] = -0.5 * beta * tP * om ** 2 * 0.004

# --- k_min pelas DUAS regras de sistematica (G3), sobre o conjunto A (31, std):
#     regra da casa (Fase 6, regra 2; gw_stack.py): sist_rel = sigma_sys/|delta_pred| <= 0,3
#     regra da fisica / 013-bis systematic_gate (floor_divisor_primary_INPUT = 5): sigma_sys <= |delta_pred|/5  (= sist_rel <= 0,2)
#     (a) por ESCALA LINEAR de |delta(k=1)| (como o critico fez); (b) EXATO: raiz de |delta_bar_exact(k)| = limiar, bissecao em k
d1_lin = abs(out["resultados"]["k=1 (GM/c^3)"]["GWTC5_31_std"]["delta_pred_weighted_linear"])
d1_exa = abs(out["resultados"]["k=1 (GM/c^3)"]["GWTC5_31_std"]["delta_pred_weighted_exact"])


def dbar_exact_at_k(kval):
    return abs(ensemble(sel31, lambda e: sig_std[e], lambda e: rows[e]["spin_q50"], lambda a: kval, N_plain)["delta_pred_weighted_exact"])


def k_root(threshold):
    lo, hi = 0.01, 2000.0
    if dbar_exact_at_k(hi) < threshold:
        return None  # inatingivel: delta_exact satura em -1
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if dbar_exact_at_k(mid) < threshold:
            lo = mid
        else:
            hi = mid
    return hi


out["k_minimo_duas_regras_conjunto_A"] = {}
for s_sys in (0.029, 0.038):
    thr_f6 = s_sys / 0.3
    thr_5s = 5 * s_sys
    out["k_minimo_duas_regras_conjunto_A"][str(s_sys)] = {
        "regra_fase6_sist_rel_0p3": {"limiar_|delta|": thr_f6, "k_min_escala_linear_delta1_lin": thr_f6 / d1_lin,
                                     "k_min_escala_linear_delta1_exato": thr_f6 / d1_exa, "k_min_exato_raiz": k_root(thr_f6)},
        "regra_fisica_013bis_|delta|_sobre_5": {"limiar_|delta|": thr_5s, "k_min_escala_linear_delta1_lin": thr_5s / d1_lin,
                                                "k_min_escala_linear_delta1_exato": thr_5s / d1_exa, "k_min_exato_raiz": k_root(thr_5s)},
    }
# compatibilidade com a v1 (mesma chave, mesma regra, agora sobre o delta linear e o exato)
out["k_minimo_para_sist_rel_0p3"] = {"sigma_sys_0p029_lin": 0.029 / 0.3 / d1_lin, "sigma_sys_0p038_lin": 0.038 / 0.3 / d1_lin,
                                      "sigma_sys_0p029_exato_raiz": k_root(0.029 / 0.3), "sigma_sys_0p038_exato_raiz": k_root(0.038 / 0.3)}

# --- N90 por ESCALA (G7): N90(k) = N90_RB * (poder(1)/poder(k))^2, com N90_RB lido do planning_targets do RINGDOWN_5SIGMA_V1
#     (R-B, populacao GWTC5_31, N90_mixture_illustration_not_selection) -- numero de PLANEJAMENTO, nao valor central
j5, h_5 = load(P5)
n90_rb = None
for t in j5.get("planning_targets", []):
    if t.get("population") == "GWTC5_31" and t.get("reading") == "R-B":
        n90_rb = t.get("N90_mixture_illustration_not_selection")
out["fontes"]["RINGDOWN_5SIGMA_V1.json"] = h_5
out["N90_por_escala_DERIVED"] = {"N90_RB_k1_lido_do_5SIGMA_planning": n90_rb, "nota": "N90(k) = N90(k=1) x (poder_exato(k=1)/poder_exato(k))^2 -- escala, nao leitura", "por_k": {}}
p1 = out["resultados"]["k=1 (GM/c^3)"]["GWTC5_31_std"]["power_exact"]
p1_lin = out["resultados"]["k=1 (GM/c^3)"]["GWTC5_31_std"]["power_linear"]
for nome, res in out["resultados"].items():
    pe = res["GWTC5_31_std"]["power_exact"]
    pl = res["GWTC5_31_std"]["power_linear"]
    out["N90_por_escala_DERIVED"]["por_k"][nome] = {"escala_exata": (n90_rb * (p1 / pe) ** 2) if (n90_rb and pe > 0) else None,
                                                     "escala_linear_1_sobre_k2": (n90_rb * (p1_lin / pl) ** 2) if (n90_rb and pl > 0) else None}

# --- tabela k x chi (G2) LIDA de RAMO_B_FISICA_TABELAS.json (nao recalculada aqui): x e delta_exato em chi = 0 / 0,68 / 0,9
fis, h_fis = load(FIS)
out["fontes"]["RAMO_B_FISICA_TABELAS.json"] = h_fis
tab = {}
for r in fis["tabela_k"]:
    if r["chi"] in (0.0, 0.68, 0.9):
        lab = r["k_label"].split(" (")[0]
        tab.setdefault(lab, {})[str(r["chi"])] = dict(k=r["k"], x=r["x"], delta_exact=r["delta_exact"], delta_lin=r["delta_lin"], N_pure=r["N_pure"], omega=r["omega_used"])
out["tabela_k_x_chi_lida_da_fisica"] = tab
# 4pi nao esta na tabela da fisica: calculado aqui com o MESMO N (BCW) da fisica para chi = 0 / 0,68 / 0,9 (dito)
tab4pi = {}
for chi in (0.0, 0.68, 0.9):
    mw, q = bcw220(chi)
    x = beta * 4 * math.pi * mw * q
    tab4pi[str(chi)] = dict(k=4 * math.pi, x=x, delta_exact=-x / (1 + x), delta_lin=-x, N_pure=4 * math.pi * mw * q, omega="ω")
out["tabela_k_x_chi_lida_da_fisica"]["k=4π (calculado aqui, mesmo N BCW)"] = tab4pi

# --- conferencia com o critico (CRITICO_RECOMPUTO.json): poder exato dos 5 k que ele recomputou
crit, h_crit = load(CRIT)
out["fontes"]["CRITICO_RECOMPUTO.json"] = h_crit
conf = {}
for nome, r in crit["poder_31_exato_vs_linear"].items():
    mine = out["resultados"][nome]["GWTC5_31_std"]
    conf[nome] = {"critico_poder_exato": r["poder_exato"], "v2_poder_exato": mine["power_exact"], "diff": mine["power_exact"] - r["poder_exato"],
                  "critico_delta_exato": r["delta_exato"], "v2_delta_exato": mine["delta_pred_weighted_exact"],
                  "critico_poder_lin": r["poder_lin"], "v2_poder_lin": mine["power_linear"]}
out["conferencia_com_o_critico"] = conf
out["conferencia_com_o_critico_max_abs_diff_poder_exato"] = max(abs(v["diff"]) for v in conf.values())

json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("beta =", beta, "| t_P =", tP, "| GMsun/c^3 =", out["GMsun_over_c3_s"], "s")
print("controle canonico delta (250 Hz, 4 ms) =", out["controle_ramo_canonico_delta"])
g = out["GW250114_release_descoberta"]
print("GW250114 (release): sigma(width90/3.29) = %.4f ; a_f = %.4f ; N(a) = %.4f ; kappa_hat = %.5f ; OmegaH_hat = %.5f ; 2pi/kappa = %.3f ; 1/kappa = %.4f ; corot = %.4f" % (
    g["sigma_from_width90"], g["spin_q50"], g["N_a"], g["kappa_hat"], g["OmegaH_hat"], g["k_kms"], g["k_inv_kappa"], g["corot_factor"]))
for nome, res in out["resultados"].items():
    print("\n##", nome)
    for conj, r in res.items():
        print("  %-26s n=%2d  sc=%.5f  d_EXATO=%+.5f  PODER_EXATO=%6.2f  | d_lin=%+.5f  poder_lin=%6.2f  (razao %.3f)  x0.273: %5.2f  sigma_beta=%.5f (%.2f beta)" % (
            conj, r["n"], r["sigma_comb"], r["delta_pred_weighted_exact"], r["power_exact"], r["delta_pred_weighted_linear"], r["power_linear"],
            r["ratio_exact_over_linear"], r["power_exact"] * 0.273, r["sigma_beta_lido_first_order"], r["sigma_beta_lido_over_beta"]))
print("\nk_min nas duas regras (conjunto A):", json.dumps(out["k_minimo_duas_regras_conjunto_A"], indent=1))
print("\nN90 por escala:", json.dumps(out["N90_por_escala_DERIVED"], indent=1))
print("\nCONFERENCIA COM O CRITICO (poder exato, 31 std):")
for nome, c in conf.items():
    print("  %-40s critico %.4f  v2 %.4f  diff %+.2e" % (nome, c["critico_poder_exato"], c["v2_poder_exato"], c["diff"]))
print("max |diff| =", out["conferencia_com_o_critico_max_abs_diff_poder_exato"])
print("\nsaida:", OUT, sha(OUT)[:16], os.path.getsize(OUT), "B")
