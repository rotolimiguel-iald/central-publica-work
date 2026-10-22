# -*- coding: utf-8 -*-
"""A FISICA DO RAMO B (lente da v386, 05/10/2026) -- tabela por script, nada literal.

Regua: beta = alpha_CODATA2018 * sqrt(e) LIDO DO FONTE do um.py por regex (nunca literal aqui);
BCW 2006 (l=m=2, n=0) LIDO do pipeline V2 (ringdown_dephasing_v2.py) por regex; QNM exatos de Kerr
(Leaver) LIDOS por hash do resultado da ORDEM 013; V2 e C6 lidos por hash do cache do rito.
Nao roda um.py. Nao abre dado novo. Escreve so nesta pasta.
"""
import hashlib, json, math, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
UM = os.path.join(NOS, "um.py")
V2PY = os.path.join(NOS, "eco_ancorado_v1", "ringdown_dephasing_v2.py")
CORE = os.path.join(NOS, "um_absoluto.json")
C6 = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw\C6_RESULTS_GW250114.json"
V2RES = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw\RINGDOWN_DEPHASING_V2_RESULT.json"
LEAVER = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_013_INSUMOS\revisao_da_gerencia\leaver_kerr_result.json"

def sha16(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]

def rx_float(src, name):
    m = re.search(r"^\s*%s\s*=\s*([0-9.eE+-]+)" % re.escape(name), src, re.M)
    if not m:
        raise SystemExit("FAIL-CLOSED: constante %s nao encontrada" % name)
    return float(m.group(1))

inputs = {}
um_src = open(UM, encoding="utf-8", errors="replace").read()
ALPHA = rx_float(um_src, "SEALED_CODATA_ALPHA")
C_LIGHT = rx_float(um_src, "C_LIGHT")
G_NEWTON = rx_float(um_src, "G_NEWTON")
BETA = ALPHA * math.sqrt(math.e)                     # em runtime, nunca literal
inputs["um.py"] = dict(sha16=sha16(UM), SEALED_CODATA_ALPHA=ALPHA, C_LIGHT=C_LIGHT, G_NEWTON=G_NEWTON)

v2_src = open(V2PY, encoding="utf-8", errors="replace").read()
HBAR = rx_float(v2_src, "HBAR") if re.search(r"^\s*HBAR\s*=", v2_src, re.M) else None
m = re.search(r"G = ([0-9.e-]+); C = ([0-9.e]+); MSUN = ([0-9.e]+); HBAR = ([0-9.e-]+)", v2_src)
if not m:
    raise SystemExit("FAIL-CLOSED: constantes do pipeline V2 nao encontradas")
G_V2, C_V2, MSUN, HBAR = (float(x) for x in m.groups())
m = re.search(r"mw = ([0-9.]+) - ([0-9.]+) \* \(1 - a\) \*\* ([0-9.]+); q = ([0-9.]+) \+ ([0-9.]+) \* \(1 - a\) \*\* \(-([0-9.]+)\)", v2_src)
if not m:
    raise SystemExit("FAIL-CLOSED: ajuste BCW nao encontrado no pipeline V2")
f1, f2, f3, q1, q2, q3 = (float(x) for x in m.groups())
BCW = dict(f1=f1, f2=-f2, f3=f3, q1=q1, q2=q2, q3=-q3)
inputs["ringdown_dephasing_v2.py"] = dict(sha16=sha16(V2PY), G=G_V2, C=C_V2, MSUN=MSUN, HBAR=HBAR, BCW_l2m2n0=BCW,
                                          prediction_line="tau_obs/tau_GR - 1 = -(1/2) beta tau* omega^2 tau_GR; ramo A tau*=t_Planck; ramo B tau*=G M_f/c^3")
T_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 5)
TMSUN = G_NEWTON * MSUN / C_LIGHT ** 3                # G M_sun / c^3 [s]

core = json.load(open(CORE, encoding="utf-8"))["core"]
beta_core = core["ringdown_dephasing_result_v2"]["beta_runtime"]
inputs["um_absoluto.json"] = dict(sha16=sha16(CORE), beta_runtime_V2=beta_core, beta_here=BETA, rel_diff=abs(BETA - beta_core) / beta_core,
                                  delta_pred_B_v2=core["ringdown_scope_v376"]["delta_pred_B_v2"], delta_pred_A_v2=core["ringdown_scope_v376"]["delta_pred_A_v2"],
                                  branch_B_concurrent_values=core["ringdown_scope_v376"]["branch_B_concurrent_values"],
                                  c6_primary_start_lnB_vs_GR=core["ringdown_scope_v376"]["c6_primary_start_lnB_vs_GR"],
                                  R2_power_check="Gamma(100 Hz) = 1.280e-40 s^-1 (ledger v383, lido)")
if inputs["um_absoluto.json"]["rel_diff"] > 1e-9:
    raise SystemExit("FAIL-CLOSED: beta recomputado difere do beta do core")

leaver = json.load(open(LEAVER, encoding="utf-8"))
inputs["leaver_kerr_result.json"] = dict(sha16=sha16(LEAVER), fonte="ORDEM 013, revisao da gerencia (Leaver 1985, fracoes continuadas), s=-2 l=m=2 n=0")
c6 = json.load(open(C6, encoding="utf-8"))
inputs["C6_RESULTS_GW250114.json"] = dict(sha16=sha16(C6), status=c6.get("status"), bytes=os.path.getsize(C6))
v2 = json.load(open(V2RES, encoding="utf-8"))
inputs["RINGDOWN_DEPHASING_V2_RESULT.json"] = dict(sha16=sha16(V2RES), bytes=os.path.getsize(V2RES))

# ---------------------------------------------------------------- QNM 220 de Kerr
def bcw(chi):
    chi = min(max(chi, 0.0), 0.998)
    F = BCW["f1"] + BCW["f2"] * (1 - chi) ** BCW["f3"]           # M omega_R
    Q = BCW["q1"] + BCW["q2"] * (1 - chi) ** BCW["q3"]           # Q = omega_R tau / 2
    return F, Q, F / (2 * Q)                                       # F_I = M omega_I = M / tau

def kerr_horizon(chi):
    s = math.sqrt(1 - chi * chi); rp = 1 + s
    kappa_hat = s / (2 * rp)                                        # kappa * (G M / c^3)
    Omega_hat = chi / (2 * rp)                                      # Omega_H * (G M / c^3)
    return kappa_hat, Omega_hat, rp

# ---------------------------------------------------------------- candidatos a k (tau* = k G M / c^3)
def k_candidates(chi):
    kap, Om, rp = kerr_horizon(chi)
    return [
        ("k=1 (t_M = GM/c^3; unidade geometrica; CONVENCAO DA V2 selada)", 1.0, "ω"),
        ("k=2 (r_s/c = 2GM/c^3; travessia do raio de Schwarzschild)", 2.0, "ω"),
        ("k=4 (1/κ de Schwarzschild = 4GM/c^3; tempo de Killing por unidade de rapidez)", 4.0, "ω"),
        ("k=8π (β_H = 2π/κ de Schwarzschild = 8πGM/c^3; periodo KMS/modular; Hawking 1975; tempo termico Connes-Rovelli: 1 unidade modular = β_H)", 8 * math.pi, "ω"),
        ("k=1/κ̂(χ) (Kerr; 1/κ; [CONJECTURE] para χ≠0 — Kay-Wald 1991)", 1.0 / kap, "ω"),
        ("k=2π/κ̂(χ) (Kerr; β_H(χ) = 4π(1+√(1−χ²))/√(1−χ²); = kms_factor do um.py:155706; sem co-rotacao)", 2 * math.pi / kap, "ω"),
        ("k=2π/κ̂(χ) com co-rotacao ω→ω−2Ω_H (gerador de Killing do horizonte H−Ω_H J; Frolov-Thorne [KNOWN, a conferir])", 2 * math.pi / kap, "ω−2Ω_H"),
    ]

def x_of(chi, k, corot, mass_ratio=1.0):
    F, Q, FI = bcw(chi)
    kap, Om, rp = kerr_horizon(chi)
    Fc = F - 2 * Om if corot == "ω−2Ω_H" else F
    # x = Gamma*tau = (1/2) beta k t_M (omega_c)^2 tau = (1/2) beta k (M omega_c)^2 / (M omega_I)
    return 0.5 * BETA * k * mass_ratio * Fc * Fc / FI

def delta_exact(x):   # tau_obs/tau_GR - 1 com 1/tau_obs = 1/tau_GR + Gamma
    return -x / (1 + x)

# ---------------------------------------------------------------- (a)+(b) tabela N(χ) e δ por k
spins = [0.0, 0.5, 0.6, 0.65, 0.68, 0.69, 0.7, 0.8, 0.9, 0.95]
tab_N = []
for chi in spins:
    F, Q, FI = bcw(chi)
    key = "%.6f" % chi
    lv = leaver.get(key)
    row = dict(chi=chi, F_bcw=F, Q_bcw=Q, FI_bcw=FI, N_bcw=F * Q)
    if lv:
        FR, FIe = lv["M_omega_R"], -lv["M_omega_I"]
        row.update(F_leaver=FR, FI_leaver=FIe, Q_leaver=FR / (2 * FIe), N_leaver=FR * FR / (2 * FIe),
                   err_F_pct=100 * (F / FR - 1), err_FI_pct=100 * (FI / FIe - 1), err_N_pct=100 * (F * Q / (FR * FR / (2 * FIe)) - 1))
    kap, Om, rp = kerr_horizon(chi)
    row.update(kappa_hat=kap, Omega_H_hat=Om, two_pi_over_kappa_hat=2 * math.pi / kap, corot_factor=(F - 2 * Om) / F)
    tab_N.append(row)

tab_k = []
for chi in [0.0, 0.68, 0.69, 0.7, 0.9]:
    for name, k, cor in k_candidates(chi):
        x = x_of(chi, k, cor)
        tab_k.append(dict(chi=chi, k_label=name, k=k, omega_used=cor, x=x, delta_lin=-x, delta_exact=delta_exact(x), N_pure=x / BETA,
                          Gamma_over_omega=(x * bcw(chi)[2] / bcw(chi)[0]) if cor == "ω" else None))

# ---------------------------------------------------------------- GW250114 [KNOWN — lido das macros LaTeX do arXiv pela LEITURA_04 da ORDEM 013]
GW250114 = dict(
    fonte="LVK PRL 135, 111403 (arXiv:2509.08054) e PRL 136, 041403 (arXiv:2509.08099); lido na casa em ORDEM_013_INSUMOS/LEITURA_04_LITERATURA.md (macros LaTeX)",
    estatuto="[KNOWN — conferido na fonte LaTeX pela frente de literatura da ORDEM 013; nao reconferido hoje]",
    M_f_src=62.7, M_f_src_err=(+1.0, -1.1), M_f_det=68.1, M_f_det_err=(+0.8, -0.9), chi_f=0.68, chi_f_err=0.01, z=0.09,
    m1_src=33.6, m2_src=32.2, D_L_Mpc=403, SNR_net=80, SNR_ringdown_220_from_10p5tM=21, SNR_220_221_from_6tM=26,
    f_220_Hz=251.7, tau_220_ms=4.09, dtau220_median=-0.01, dtau220_90_up=0.10, dtau220_90_dn=0.09, df220=(0.02, 0.02),
    pyRing_postmerger_dtau220=(-0.14, +0.25, -0.23),
)
CATALOGOS = dict(
    GWTC3_hier=dict(dtau220=0.13, up=0.21, dn=0.22, fonte="arXiv:2112.06861 subsec_rin3 [KNOWN lido na casa]"),
    GWTC3_best_single_GW200129=dict(dtau220=0.11, pm=0.23, SNR=26.5, fonte="arXiv:2112.06861 [KNOWN lido na casa]"),
    GWTC4_pSEOB_combined=dict(dtau220=0.17, pm=0.11, fonte="arXiv:2603.19021 (preprint) [KNOWN lido na casa]"),
    GWTC4_pSEOB_hier=dict(dtau220=0.16, up=0.18, dn=0.16, fonte="arXiv:2603.19021 [KNOWN lido na casa]"),
    GWTC4_pyRing_hier=dict(dtau220=0.18, up=0.27, dn=0.26, fonte="arXiv:2603.19021 [KNOWN lido na casa]"),
    GW150914_like_single_event="a ler da fonte (nao ha numero conferido na casa para o δτ̂_220 do GW150914 isolado; o melhor evento isolado do GWTC-3 e o GW200129, acima)",
)
sig_dn = GW250114["dtau220_90_dn"] / 1.6449   # aprox. gaussiana da semi-largura 90% (lado negativo)
sig_up = GW250114["dtau220_90_up"] / 1.6449
chi = GW250114["chi_f"]
F, Q, FI = bcw(chi)
tM_det = TMSUN * GW250114["M_f_det"]
qnm_check = dict(f220_bcw_Hz=F / (2 * math.pi * tM_det), tau220_bcw_ms=1e3 * tM_det / FI, Q_bcw=Q,
                 f220_pSEOB_Hz=GW250114["f_220_Hz"], tau220_pSEOB_ms=GW250114["tau_220_ms"])
M_tot_src = GW250114["m1_src"] + GW250114["m2_src"]
M_chirp_src = (GW250114["m1_src"] * GW250114["m2_src"]) ** 0.6 / M_tot_src ** 0.2
mass_choices = [
    ("M_f,det = (1+z) M_f,src (fixa os QNMs OBSERVADOS; convencao da V2)", GW250114["M_f_det"], 1.0, "x invariante: tau* ∝ M e omega ∝ 1/M no MESMO referencial"),
    ("M_f,src (referencial de repouso do remanescente)", GW250114["M_f_src"], 1.0, "x identico ao de M_f,det se omega e tau sao os do repouso; misturar referenciais custa (1+z)^±1 — a declarar"),
    ("M_tot,src = m1+m2 (massa total pre-fusao)", M_tot_src, M_tot_src / GW250114["M_f_src"], "k efetivo × M_tot/M_f"),
    ("M_chirp,src (massa chirp)", M_chirp_src, M_chirp_src / GW250114["M_f_src"], "k efetivo × M_c/M_f"),
]
REALIZ = 0.273   # [DECLARADO — verificacao RD-01 (28/09): por realizacao com difusao de fase, delta_tau medio = 0,273 ± 0,06 do ensemble]
gw_rows = []
for name, k, cor in k_candidates(chi):
    for mname, Mval, ratio, note in mass_choices:
        x = x_of(chi, k, cor, ratio)
        d = delta_exact(x)
        s = sig_dn if d < GW250114["dtau220_median"] else sig_up
        d_eff = REALIZ * d
        s_eff = sig_dn if d_eff < GW250114["dtau220_median"] else sig_up
        gw_rows.append(dict(k_label=name, k=k, omega_used=cor, M_choice=mname, M_Msun=Mval, mass_ratio=ratio, x=x, delta_exact=d, delta_lin=-x,
                            z_vs_GW250114_median_gauss_approx=(d - GW250114["dtau220_median"]) / s,
                            inside_90pct=(GW250114["dtau220_median"] - GW250114["dtau220_90_dn"] <= d <= GW250114["dtau220_median"] + GW250114["dtau220_90_up"]),
                            delta_eff_realizacao_0p273=d_eff, z_eff_realizacao=(d_eff - GW250114["dtau220_median"]) / s_eff,
                            sigma_needed_5sigma=abs(d) / 5, note=note))

# ---------------------------------------------------------------- a familia unificada tau* = k G m_X / c^3 (m_X = m_P da' o ramo A)
M_PLANCK_KG = math.sqrt(HBAR * C_LIGHT / G_NEWTON)
mP_over_Mf = M_PLANCK_KG / (GW250114["M_f_det"] * MSUN)
familia = dict(
    forma="τ★ = k · G m_X / c³  ⟹  x = β · k · N(χ_f) · (m_X / M_f)   — a mesma dobra c³ em duas massas (memoria 16/09, leitura (d)): m_X = m_P da' o ramo A (t_Planck, pedra 84_: G m_P/c³ = t_P), m_X = M_f da' o ramo B",
    t_P_eq_G_mP_over_c3_resid=abs(G_NEWTON * M_PLANCK_KG / C_LIGHT ** 3 - T_PLANCK) / T_PLANCK,
    GW250114_mP_over_Mf_det=mP_over_Mf, x_ramo_A_k1=BETA * F * Q * mP_over_Mf, delta_ramo_A_k1=-BETA * F * Q * mP_over_Mf,
    x_ramo_A_k8pi=BETA * 8 * math.pi * F * Q * mP_over_Mf,
    V2_stack_delta_pred_A=core["ringdown_dephasing_result_v2"]["stacks"]["3.0"]["delta_pred_A"],
    nota="o ramo A e' invisivel por construcao em qualquer k: x_A ~ 1e-42; a correspondencia com a RG e' o que ele devolve (ringdown_scope_v376)",
)

# ---------------------------------------------------------------- (c) a identidade: a fracao le beta vezes um numero puro
identidade = dict(
    lei="Γ_ω = ½ β τ★ ω²  com  τ★ = k · G M_X / c³  (ramo B)  [lei: REAL na forma (dephasing_reach); τ★ do ramo B: INPUT]",
    observavel="δτ̂_220 ≡ τ_obs/τ_RG − 1  com  1/τ_obs = 1/τ_RG + Γ  ⟹  δτ̂_220 = −x/(1+x),  x = Γ·τ_RG",
    x="x = ½ β k (M_X/M_f) (M_f ω_c)² / (M_f ω_I) = β · k · (M_X/M_f) · N(χ_f),  N(χ) = F(χ)·Q(χ) = F²/(2F_I),  F = M_f ω_R, F_I = M_f ω_I = M_f/τ, Q = ω_R τ/2;  com co-rotacao F → F − 2Ω̂_H",
    leitura_de_beta="β_lido = x / (k · (M_X/M_f) · N(χ_f))  com  x = −δτ̂/(1+δτ̂)  ⟹  a fracao medida e uma leitura de β dividida por um numero puro conhecido (so spin e k)",
    independencia_da_massa="x NAO depende de M quando τ★ ∝ M_f (unidade geometrica): depende so de χ_f, de k e da razao M_X/M_f — por isso «qual M» so entra como fator M_X/M_f",
    sinal="dephasing extra ⟹ 1/τ_obs > 1/τ_RG ⟹ τ_obs < τ_RG ⟹ δτ̂_220 < 0 (linha MAIS LARGA); os catalogos puxam δτ̂ > 0 (linha mais estreita) [KNOWN]",
    numeros_puros_N=dict((("chi=%.2f" % r["chi"]), dict(N_bcw=r["N_bcw"], N_leaver=r.get("N_leaver"), two_pi_over_kappa=r["two_pi_over_kappa_hat"], corot_factor=r["corot_factor"])) for r in tab_N),
    exemplo_GW250114=dict(chi=chi, N_bcw=F * Q, N_leaver=(leaver["0.680000"]["M_omega_R"] ** 2 / (2 * -leaver["0.680000"]["M_omega_I"])),
                          x_k1=x_of(chi, 1, "ω"), delta_k1_exact=delta_exact(x_of(chi, 1, "ω")), delta_k1_lin=-x_of(chi, 1, "ω"),
                          x_k8pi=x_of(chi, 8 * math.pi, "ω"), delta_k8pi_exact=delta_exact(x_of(chi, 8 * math.pi, "ω"))),
)

# ---------------------------------------------------------------- reproducao do −0,0194 da V2 (k=1, M = M_f,det)
rep = dict(note="a V2 selada usa k=1 com M = M_f,det (SimIMREOBFinalMassSpin) e δ_lin = −Γ τ_RG por serie; o −0,0194 e a media ponderada (variancia inversa) das 15 series a 3 ms")
try:
    ps = v2.get("per_series") or v2.get("series") or []
    rep["n_per_series"] = len(ps)
    if ps:
        rep["keys_per_series"] = sorted(list(ps[0].keys()))[:40]
        chk = []
        for r in ps[:200]:
            a = r.get("a_f", r.get("af", r.get("spin_f")))
            dB = r.get("delta_pred_B")
            if a is not None and dB is not None:
                Fa, Qa, FIa = bcw(float(a))
                chk.append(dict(a_f=float(a), delta_pred_B_file=float(dB), minus_beta_F_Q=-BETA * Fa * Qa, diff=float(dB) + BETA * Fa * Qa))
        rep["check_delta_B_eq_minus_beta_F_Q"] = chk[:20]
        rep["max_abs_diff_first20"] = max((abs(c["diff"]) for c in chk[:20]), default=None)
        rep["n_checked"] = len(chk)
except Exception as e:  # fail visible
    rep["error"] = repr(e)
rep["stack_3ms_delta_pred_B_core"] = core["ringdown_dephasing_result_v2"]["stacks"]["3.0"]["delta_pred_B"]
rep["stack_3ms_power_B_core"] = core["ringdown_dephasing_result_v2"]["stacks"]["3.0"]["power_B"]
rep["stack_3ms_sigma_core"] = core["ringdown_dephasing_result_v2"]["stacks"]["3.0"]["sigma"]

# ---------------------------------------------------------------- (d) poder
poder = dict(regra="5σ pede σ_total ≤ |δ|/5; lei √N so com σ comparaveis, nao correlacionadas e sem piso comum; piso sistematico comum (familia de forma de onda) NAO cai com N",
             sigma_1_opcoes={"GW250114-like (1σ ≈ 0.09/1.645)": sig_dn, "GW200129-like (melhor isolado GWTC-3: 0.23/1.645)": 0.23 / 1.6449,
                             "evento tipico O4 ~0.20 (1σ) [INPUT]": 0.20, "evento tipico O3 ~0.30 (1σ) [INPUT]": 0.30},
             piso_sistematico_declarado={"SEOB x Phenom ~0.9 do efeito k=1 (ORDEM 013) [DECLARADO]": 0.9 * abs(delta_exact(x_of(chi, 1, "ω"))),
                                         "familia 0.029 (013-bis) [DECLARADO]": 0.029},
             linhas=[])
for name, k, cor in k_candidates(chi):
    d = abs(delta_exact(x_of(chi, k, cor)))
    row = dict(k_label=name, delta_abs=d, sigma_5sigma=d / 5, N_por_sigma1={})
    for lab, s1 in poder["sigma_1_opcoes"].items():
        row["N_por_sigma1"][lab] = math.ceil((5 * s1 / d) ** 2)
    row["atingivel_com_piso"] = {lab: (d > 5 * s) for lab, s in poder["piso_sistematico_declarado"].items()}
    row["N_com_piso_0.029_sigma1_0.058"] = (math.ceil(25 * sig_dn ** 2 / (d * d / 25 - 0.029 ** 2)) if d * d / 25 > 0.029 ** 2 else "impossivel por N: |δ|/5 < piso")
    poder["linhas"].append(row)

# ---------------------------------------------------------------- (f) o que falsifica
falsificar = dict(
    FALSIFICA_o_par=("(k, M_X, ω_c, local-na-fonte, realizacao-ou-ensemble) fixados ANTES; fracao medida δτ̂ (ou a largura populacional de δf̂, se o mecanismo for difusao de fase) "
                     "incompativel com −x/(1+x), x = β k (M_X/M_f) N(χ_f), a ≥ 5σ com σ_sys da familia de forma de onda e do inicio da janela CONTROLADA (< |δ|/5) ⟹ FALSIFIED_AT_(k,M) — cai o PAR, nao a lei nem β"),
    NAO_falsifica=("coincidir com a RG (δτ̂ = 0 dentro de σ) com |δ| < 5σ ⟹ NOT_FALSIFIED_UNDERPOWERED (correspondencia recuperada: a RG e o limite classico, nao rival); "
                   "sistematica > limiar ⟹ INCONCLUSIVE_SYSTEMATICS; um unico modo 220 com (M_f, χ_f) livres e NAO identificavel (Kerr 1,25% mais leve imita o k=1) — sem (M_f,χ_f) da inspiral (IMR) ou 2º modo o teste e vazio por construcao [REAL, ORDEM 013]"),
    vereditos_permitidos=["TGL_RINGDOWN_BRANCH_B_EXCLUDED_AT_(k,M)", "TGL_RINGDOWN_NOT_FALSIFIED_POWERED", "TGL_RINGDOWN_NOT_FALSIFIED_UNDERPOWERED", "TGL_RINGDOWN_INCONCLUSIVE_SYSTEMATICS", "TGL_RINGDOWN_GR_TENSION_REPORTED"],
    vereditos_proibidos=["CONFIRMED", "PROVED"],
)

out = dict(
    quando="2026-10-05", lente="A FISICA DO RAMO B (cânone + literatura [KNOWN])", beta_TGL_runtime=BETA, alpha_lido=ALPHA, sqrt_e=math.sqrt(math.e),
    t_Planck_s=T_PLANCK, GMsun_over_c3_s=TMSUN, inputs=inputs, tabela_N_chi=tab_N, tabela_k=tab_k,
    GW250114_KNOWN=GW250114, catalogos_KNOWN=CATALOGOS, qnm_check_GW250114=qnm_check,
    massas_GW250114=dict(M_tot_src=M_tot_src, M_chirp_src=M_chirp_src, ratio_tot_over_f=M_tot_src / GW250114["M_f_src"], ratio_chirp_over_f=M_chirp_src / GW250114["M_f_src"], one_plus_z=1 + GW250114["z"]),
    GW250114_por_k_e_M=gw_rows, identidade=identidade, familia_unificada=familia, reproducao_V2=rep, poder=poder, falsificar=falsificar,
    decisoes_do_operador=[
        "k em τ★ = k·GM/c³: 1 (unidade geometrica, V2) · 2 (r_s/c) · 4 (1/κ) · 8π (β_H = 2π/κ, periodo KMS/modular de Schwarzschild — a leitura «tempo emergente do fluxo modular»: 1 unidade modular = β_H) · 2π/κ̂(χ_f) de Kerr com ou sem co-rotacao ω→ω−2Ω_H (para χ≠0 e' [CONJECTURE]: Kay–Wald 1991 — nao ha Hartle–Hawking de Kerr)",
        "qual M: M_f,det (fixa os QNMs observados; convencao da V2) · M_f,src (repouso; x identico se tudo no mesmo referencial) · M_tot (×1,05) · M_chirp (×0,46) — e o referencial declarado (misturar custa (1+z)^±1)",
        "onde a lei age: LOCAL na fonte (durante o ringdown; τ★ e' propriedade do remanescente) — na propagacao o ramo B apaga a onda (Γ_B·D/c ~ 2e17 e-folds: erro de tipo, nao teste) [REAL, auditoria 28/09]",
        "mecanismo/estimando: amortecimento da envoltoria por realizacao (δτ̂ le x inteiro) OU difusao de fase (ensemble; por realizacao so ~0,27x e o estimando passa a ser a largura populacional de δf̂) — identificacao [ONTO] que fixa a previsao efetiva e o poder",
        "o observavel e a fonte: δτ̂_220 publicado (pSEOBNR IMR; posteriores Zenodo 17018009 — NAO esta em disco: so o strain 32 s do GW250114 na Bancada) vs reanalise propria (so-220 com (M_f,χ_f) da inspiral; a parede do pSEOBNRv4HM_PA do lalsuite 7.26 e a receita R0–R9 da ORDEM 015)",
        "o piso sistematico aceito (familia SEOB×Phenom 0,029 [DECLARADO 013-bis]; inicio da janela): com ele k ≤ 4 e a co-rotacao sao inalcancaveis por N; so k ~ 8π/2π/κ̂ sem co-rotacao supera o piso — e esses ja leem ~6σ contra o δτ̂ publicado do GW250114 na leitura por envoltoria (NAO-CEGO; sem veredito)",
        "vereditos e cegueira: EXCLUDED_AT_(k,M) / NOT_FALSIFIED_POWERED / UNDERPOWERED / INCONCLUSIVE_SYSTEMATICS / GR_TENSION_REPORTED; CONFIRMED proibido; declarar NAO-CEGO quanto ao GW250114 publicado e quanto aos 89 eventos da V2",
    ],
    aviso="os z contra o GW250114 sao leitura NAO-CEGA de um numero PUBLICADO (aprox. gaussiana da semi-largura 90%); nenhum veredito; PROVADA ≠ CONFIRMADA; NOT_FALSIFIED ≠ CONFIRMED",
)
jp = os.path.join(HERE, "RAMO_B_FISICA_TABELAS.json")
json.dump(out, open(jp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---------------------------------------------------------------- markdown (dados, nao prosa)
L = []
L.append("# A FISICA DO RAMO B — tabelas por script (05/10/2026)\n")
L.append("β_TGL = α·√e lido do fonte (um.py `SEALED_CODATA_ALPHA`) em runtime = %.15g (core V2: %.15g; diff rel %.1e). t_Planck = %.6e s. GM☉/c³ = %.6e s.\n" % (BETA, beta_core, inputs["um_absoluto.json"]["rel_diff"], T_PLANCK, TMSUN))
L.append("Entradas por hash: " + "; ".join("%s %s" % (k, v["sha16"]) for k, v in inputs.items()) + "\n")
L.append("## (a)/(b) O numero puro N(χ) = F·Q = F²/(2F_I) do modo 220 (BCW 2006 lido do pipeline V2; Leaver lido por hash)\n")
L.append("| χ_f | F=Mω_R (BCW) | F_I=M/τ (BCW) | Q (BCW) | N=F·Q (BCW) | N (Leaver) | erro N % | κ̂ | Ω̂_H | 2π/κ̂ | (F−2Ω̂_H)/F |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|")
for r in tab_N:
    L.append("| %.2f | %.4f | %.5f | %.4f | %.4f | %s | %s | %.5f | %.5f | %.2f | %.3f |" % (
        r["chi"], r["F_bcw"], r["FI_bcw"], r["Q_bcw"], r["N_bcw"], ("%.4f" % r["N_leaver"]) if "N_leaver" in r else "—", ("%+.2f" % r["err_N_pct"]) if "err_N_pct" in r else "—",
        r["kappa_hat"], r["Omega_H_hat"], r["two_pi_over_kappa_hat"], r["corot_factor"]))
L.append("\nSchwarzschild exato (Leaver): Mω_R = %.5f, Mω_I = %.5f (1/τ = %.4f c³/GM), Q = %.4f, N = %.4f. Ajuste BCW em χ=0: F = %.4f (erro %+.2f%%, limite BCW 1,85%%), Q = %.4f (erro %+.2f%%, limite BCW 0,88%%); F_I = F/(2Q) combina os dois: %.5f (%+.2f%%); N = F·Q cancela parte: %+.2f%%.\n" % (
    leaver["0.000000"]["M_omega_R"], leaver["0.000000"]["M_omega_I"], -leaver["0.000000"]["M_omega_I"], leaver["0.000000"]["Q"], tab_N[0]["N_leaver"], tab_N[0]["F_bcw"], tab_N[0]["err_F_pct"],
    tab_N[0]["Q_bcw"], 100 * (tab_N[0]["Q_bcw"] / tab_N[0]["Q_leaver"] - 1), tab_N[0]["FI_bcw"], tab_N[0]["err_FI_pct"], tab_N[0]["err_N_pct"]))
L.append("## (b) δτ̂_220 = −x/(1+x), x = β·k·N(χ) por candidato a k (τ★ = k·GM_f/c³; M_X = M_f)\n")
L.append("| χ_f | k (origem) | k | ω usado | N puro = x/β | x = Γτ | δ_lin | δ_exato |")
L.append("|---|---|---|---|---|---|---|---|")
for r in tab_k:
    L.append("| %.2f | %s | %.4f | %s | %.4f | %.5f | %+.5f | %+.5f |" % (r["chi"], r["k_label"].split(" (")[0], r["k"], r["omega_used"], r["N_pure"], r["x"], r["delta_lin"], r["delta_exact"]))
L.append("\nConvencao que reproduz o «−0,0194» do registro: **k = 1, M = M_f,det, δ_lin = −β·F·Q por serie** (GW250114-like χ=0,68: δ_lin = %+.5f, δ_exato = %+.5f; o −0,0194 selado e a media ponderada das 15 series da V2 com os seus spins). Reproducao por serie: n=%s, max|diff| (20 primeiras) = %s.\n" % (
    -x_of(0.68, 1, "ω"), delta_exact(x_of(0.68, 1, "ω")), rep.get("n_checked"), rep.get("max_abs_diff_first20")))
L.append("## (c) A identidade exata (a pergunta do operador em forma operacional)\n")
for k_, v_ in identidade.items():
    if k_ in ("numeros_puros_N", "exemplo_GW250114"):
        continue
    L.append("- **%s**: %s" % (k_, v_))
ex = identidade["exemplo_GW250114"]
L.append("- **GW250114 (χ_f = 0,68)**: N = %.4f (BCW) / %.4f (Leaver); k=1: x = %.5f, δ = %+.5f; k=8π: x = %.4f, δ = %+.4f. Leitura de β: β_lido = −δτ̂/(1+δτ̂) / (k·N).\n" % (ex["N_bcw"], ex["N_leaver"], ex["x_k1"], ex["delta_k1_exact"], ex["x_k8pi"], ex["delta_k8pi_exact"]))
L.append("## (a) QUAL M — GW250114 [KNOWN]: M_f,src 62,7; M_f,det 68,1; m1+m2 = %.1f (M_tot/M_f = %.3f); M_chirp = %.1f (M_c/M_f = %.3f); 1+z = %.2f\n" % (M_tot_src, M_tot_src / 62.7, M_chirp_src, M_chirp_src / 62.7, 1.09))
L.append("## (d) GW250114 por k e M: δ previsto vs δτ̂_220 publicado = −0,01 (+0,10/−0,09) 90%% [KNOWN]; σ₋ ≈ %.4f, σ₊ ≈ %.4f (gauss. aprox.); leitura NAO-CEGA, sem veredito\n" % (sig_dn, sig_up))
L.append("| k | M_X | x | δ_exato (envoltoria, por realizacao) | z vs mediana | dentro do 90%? | δ_eff difusao de fase (×0,273 [DECLARADO RD-01]) | z_eff | σ p/ 5σ |")
L.append("|---|---|---|---|---|---|---|---|---|")
for r in gw_rows:
    L.append("| %s | %s | %.4f | %+.4f | %+.2f | %s | %+.4f | %+.2f | %.4f |" % (r["k_label"].split(" (")[0] + (" co-rot" if r["omega_used"] != "ω" else ""), r["M_choice"].split(" ")[0], r["x"], r["delta_exact"], r["z_vs_GW250114_median_gauss_approx"], "sim" if r["inside_90pct"] else "NAO", r["delta_eff_realizacao_0p273"], r["z_eff_realizacao"], r["sigma_needed_5sigma"]))
L.append("\n**A familia unificada** τ★ = k·G·m_X/c³ ⟹ x = β·k·N(χ_f)·(m_X/M_f): m_X = m_P da' o ramo A (G·m_P/c³ = t_P, residuo %.1e), m_X = M_f o ramo B. GW250114: m_P/M_f,det = %.3e ⟹ x_A(k=1) = %.3e (δ = %+.3e; V2 empilhada: %+.3e), x_A(k=8π) = %.3e — invisivel em qualquer k.\n" % (
    familia["t_P_eq_G_mP_over_c3_resid"], familia["GW250114_mP_over_Mf_det"], familia["x_ramo_A_k1"], familia["delta_ramo_A_k1"], familia["V2_stack_delta_pred_A"], familia["x_ramo_A_k8pi"]))
L.append("\nQNM de conferencia (BCW, M_f,det 68,1, χ 0,68): f_220 = %.1f Hz, τ_220 = %.3f ms, Q = %.3f — pSEOB publica f = %.1f Hz, τ = %.2f ms [KNOWN].\n" % (qnm_check["f220_bcw_Hz"], qnm_check["tau220_bcw_ms"], qnm_check["Q_bcw"], qnm_check["f220_pSEOB_Hz"], qnm_check["tau220_pSEOB_ms"]))
L.append("Catalogos [KNOWN, lidos na casa]: GWTC-3 hier. δτ̂_220 = +0,13 (+0,21/−0,22); melhor evento isolado GW200129 = +0,11 ± 0,23 (SNR 26,5); GWTC-4.0 pSEOB conj. +0,17 ± 0,11; hier. +0,16 (+0,18/−0,16); pyRing hier. +0,18 (+0,27/−0,26). GW150914 isolado: a ler da fonte. Sinal dos catalogos: δτ̂ > 0 (linha mais ESTREITA) — oposto ao dephasing.\n")
L.append("## (d) Poder: N eventos para 5σ por k (σ_1 por evento; lei √N so sem correlacao e sem piso comum)\n")
L.append("| k | |δ| | σ p/ 5σ | N (σ₁=%.3f GW250114-like) | N (σ₁=%.3f GW200129-like) | N (σ₁=0,20) | N (σ₁=0,30) | piso 0,029 (013-bis): atingivel? | N com piso 0,029 e σ₁ 0,058 |" % (sig_dn, 0.23 / 1.6449))
L.append("|---|---|---|---|---|---|---|---|---|")
for r in poder["linhas"]:
    ns = list(r["N_por_sigma1"].values())
    L.append("| %s | %.4f | %.4f | %d | %d | %d | %d | %s | %s |" % (r["k_label"].split(" (")[0], r["delta_abs"], r["sigma_5sigma"], ns[0], ns[1], ns[2], ns[3],
             "sim" if r["atingivel_com_piso"]["familia 0.029 (013-bis) [DECLARADO]"] else "NAO", r["N_com_piso_0.029_sigma1_0.058"]))
L.append("\nRegistro ja na casa [DERIVED; NAO-CEGO, 013-bis 22/09]: N₉₀(5σ, k=1) = 335 eventos GW250114-like ou ≈ 3.300 de mistura O4; O5 inteiro 2,2–3,1σ com sistematica zero; 3G fecha por contagem (~207 eventos SNR_RD ≥ 50) so com modelo validado a 0,40%% de τ₂₂₀; condicao sistematica VERMELHA (familia 0,029 = 7× o piso 0,0040 do k=1).\n")
L.append("## (f) Falsificar / nao falsificar\n")
for k_, v_ in falsificar.items():
    L.append("- **%s**: %s" % (k_, v_))
L.append("\n## Decisoes que so o operador pode tomar (o pre-registro V1 do ramo B as fixa ANTES de abrir dado)\n")
for i, d in enumerate(out["decisoes_do_operador"], 1):
    L.append("%d. %s" % (i, d))
L.append("\n" + out["aviso"] + "\n")
mp = os.path.join(HERE, "RAMO_B_FISICA_TABELAS.md")
open(mp, "w", encoding="utf-8").write("\n".join(L))
print("\n".join(L))
print("\nESCRITO:", jp, os.path.getsize(jp), "|", mp, os.path.getsize(mp))
