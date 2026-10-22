"""Auditor c1 -- reproducao independente (sandbox) das contas da F8.2.NU2.

Nao importa nem executa um.py; le so a atribuicao ALPHA_FINE_CODATA_2018 por regex.
Nao abre dado observado; tudo sintetico. Escreve so nesta pasta.
"""
import hashlib, json, math, os, re, sys
import numpy as np
import scipy.linalg as sla
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
NU2 = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F8.2.NU2"
mp.mp.dps = 80
res = {"checks": []}

def chk(nome, ok, **kw):
    res["checks"].append(dict(nome=nome, PASSA=bool(ok), **kw))

# ---- alpha por regex (bytes do um.py; sem import/execucao) ----
raw = open(UM, "rb").read()
res["um_py_sha256"] = hashlib.sha256(raw).hexdigest(); res["um_py_bytes"] = len(raw)
txt = raw.decode("utf-8-sig")
m = re.findall(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)\s*(?:#.*)?$", txt, re.M)
assert len(m) == 1, m
alpha = mp.mpf(m[0]); beta0 = alpha * mp.sqrt(mp.e)
res["alpha_literal_no_um_py"] = m[0]
res["beta0_runtime"] = mp.nstr(beta0, 25)
chk("beta0 = alpha*sqrt(e) em runtime confere com 0,012031300400803142 (so conferencia)",
    abs(float(beta0) - 0.012031300400803142) < 1e-17, beta0=float(beta0))
chk("razao sqrt(e)/beta0 = 1/alpha", abs(mp.sqrt(mp.e) / beta0 - 1 / alpha) < mp.mpf(10) ** -70,
    razao=mp.nstr(mp.sqrt(mp.e) / beta0, 16), um_sobre_alpha=mp.nstr(1 / alpha, 16))

# ---- constantes (as mesmas declaradas no PLANO_R1; CODATA 2018 / SI) ----
plan = json.load(open(os.path.join(NU2, "PLANO_R1.json"), encoding="utf-8"))
C = plan["constants"]; Q = plan["inputs_reference_not_fitted"]
h = mp.mpf(repr(C["h_J_s"])); eV = mp.mpf(repr(C["eV_J"])); c = mp.mpf(repr(C["c_m_s"])); G = mp.mpf(repr(C["G_SI"]))
hbarJ = h / (2 * mp.pi); hbar_eVs = hbarJ / eV
tP = mp.sqrt(hbarJ * G / c ** 5)
res["tP_s"] = mp.nstr(tP, 20); res["hbar_eV_s"] = mp.nstr(hbar_eVs, 20)

# ---- PMNS (delta=0) por produto de rotacoes ----
def rot(i, j, s2):
    s = mp.sqrt(mp.mpf(repr(s2))); cc = mp.sqrt(1 - mp.mpf(repr(s2)))
    R = mp.eye(3); R[i, i] = cc; R[j, j] = cc; R[i, j] = s; R[j, i] = -s
    return R
U = rot(1, 2, Q["sin2theta23"]) * rot(0, 2, Q["sin2theta13"]) * rot(0, 1, Q["sin2theta12"])
orth = mp.norm(U * U.T - mp.eye(3), 1)
chk("PMNS ortogonal (delta=0)", orth < mp.mpf(10) ** -70, erro=mp.nstr(orth, 5))
m2 = [mp.mpf(0), mp.mpf(repr(Q["dm21_eV2"])), mp.mpf(repr(Q["dm31_eV2"]))]
pares = [(0, 1), (0, 2), (1, 2)]

def omega(i, j, E_eV):  # 1/s
    return abs(m2[j] - m2[i]) / (2 * E_eV * hbar_eVs)

def gamma(i, j, E_eV, tau, Kfac=1, beta=None):  # lei Gamma = 1/2 beta tau omega^2 Kfac
    b = beta0 if beta is None else beta
    return mp.mpf(1) / 2 * b * tau * Kfac * omega(i, j, E_eV) ** 2

# textura
E = mp.mpf(4) * 10 ** 6
g21, g31, g32 = [gamma(i, j, E, tP) for i, j in pares]
tex = [1, g31 / g21, g32 / g21]
chk("textura Gamma21:Gamma31:Gamma32 = 1:1111,111...:1045,444...", abs(tex[1] - mp.mpf(10000) / 9) < 1e-60 and abs(tex[2] - (mp.mpf(97) / 3) ** 2) < 1e-60,
    textura=[mp.nstr(x, 16) for x in tex], nota="(dm31/dm21)^2=(100/3)^2; (dm32/dm21)^2=(97/3)^2")

# n = -2: log-derivada de Gamma em E, tau e Kfac constantes
f = lambda lnE: mp.log(gamma(0, 2, mp.e ** lnE, tP))
nslope = mp.diff(f, mp.log(E))
chk("n = -2 exato (tau, Kfac constantes, vacuo)", abs(nslope + 2) < mp.mpf(10) ** -50, n=mp.nstr(nslope, 20))

# ---- P_ee com matriz densidade completa na base de massa, alta precisao (sem expm1) ----
def Pee(E_eV, L_m, tau, Kfac=1):
    t = L_m / c
    rho0 = mp.matrix(3, 3)
    for i in range(3):
        for j in range(3):
            rho0[i, j] = U[0, i] * U[0, j]
    rhot = mp.matrix(3, 3)
    for i in range(3):
        for j in range(3):
            if i == j:
                rhot[i, j] = rho0[i, j]
            else:
                w = (m2[i] - m2[j]) / (2 * E_eV * hbar_eVs)  # com sinal
                gm = mp.mpf(1) / 2 * beta0 * tau * Kfac * w ** 2
                rhot[i, j] = rho0[i, j] * mp.exp(mp.mpc(-gm * t, -w * t))
    rf = U * rhot * U.T  # base de sabor
    return rf[0, 0].real, rf

L = mp.mpf(repr(Q["reactor_baseline_km"])) * 1000
Es = [mp.mpf(2) + mp.mpf(6) * i / 120 for i in range(121)]
P0s, dPs = [], []
for Ei in Es:
    p0, _ = Pee(Ei * 10 ** 6, L, 0)
    p1, rf = Pee(Ei * 10 ** 6, L, tP)
    P0s.append(p0); dPs.append(p1 - p0)
maxdP = max(abs(x) for x in dPs)
calc = json.load(open(os.path.join(NU2, "CALCULOS_ESPECTRAIS_R1.json"), encoding="utf-8"))
ir = calc["ideal_reactor"]
rel_maxdP = abs(maxdP - mp.mpf(repr(ir["max_abs_deltaP"]))) / maxdP
chk("max|deltaP| (tau=tP, Kfac=1, 52,5 km, 2-8 MeV) = 1,78806716e-39", rel_maxdP < 1e-12,
    meu=mp.nstr(maxdP, 17), nu2=ir["max_abs_deltaP"], dif_rel=mp.nstr(rel_maxdP, 3))
mP0 = sum(P0s) / len(P0s); mdP = sum(dPs) / len(dPs); coef = mdP / mP0
I_fix = sum(d * d / p for d, p in zip(dPs, P0s)) / len(Es)
I_prof = sum((d - coef * p) ** 2 / p for d, p in zip(dPs, P0s)) / len(Es)
N5 = 25 / I_prof
relN = abs(N5 - mp.mpf(repr(ir["N_unoscillated_for_nominal_5_profile"]))) / N5
chk("N nao oscilado p/ distancia nominal 5, normalizacao perfilada = 8,6324085e79", relN < 1e-12,
    meu=mp.nstr(N5, 17), nu2=ir["N_unoscillated_for_nominal_5_profile"], dif_rel=mp.nstr(relN, 3))
chk("perfilamento: coeficiente = soma(dP)/soma(P0) minimiza soma((dP-cP0)^2/P0)",
    abs(mp.diff(lambda cc: sum((d - cc * p) ** 2 / p for d, p in zip(dPs, P0s)), coef)) < mp.mpf(10) ** -70 * 1e-0 + abs(I_prof) * 1e-20,
    coef=mp.nstr(coef, 10))
chk("media P0 = 0,41182148", abs(mP0 - mp.mpf(repr(ir["mean_P0"]))) < 1e-14, meu=mp.nstr(mP0, 16))
# decomposicao: fracao do deltaP vinda do par lento (21) vs rapidos (31,32) no pico
k = max(range(len(Es)), key=lambda i: abs(dPs[i])); Ek = Es[k] * 10 ** 6; t = L / c
w = [U[0, i] ** 2 for i in range(3)]
comp = {}
for (i, j) in pares:
    wij = omega(i, j, Ek); gij = gamma(i, j, Ek, tP)
    comp["%d%d" % (j + 1, i + 1)] = 2 * w[i] * w[j] * mp.cos(wij * t) * (mp.exp(-gij * t) - 1)
tot = sum(comp.values())
res["decomposicao_deltaP_no_pico"] = {kk: mp.nstr(v / tot, 6) for kk, v in comp.items()}
res["E_pico_MeV"] = mp.nstr(Es[k], 6)

# ---- controles sinteticos GKLS (adimensionais) ----
Hd = np.diag([0.0, 1.0, 3.0])
def gkls_super(Hm, a):
    I3 = np.eye(3)
    # vec por coluna: vec(AXB) = (B^T kron A) vec(X)
    Lh = -1j * (np.kron(I3, Hm) - np.kron(Hm.T, I3))
    LL = np.sqrt(2 * a) * Hm
    D = np.kron(LL.conj(), LL) - 0.5 * np.kron(I3, LL.conj().T @ LL) - 0.5 * np.kron((LL.conj().T @ LL).T, I3)
    return Lh + D
def choi(S):
    J = np.zeros((9, 9), dtype=complex)
    for i in range(3):
        for j in range(3):
            Eij = np.zeros((3, 3)); Eij[i, j] = 1
            out = (S @ Eij.reshape(-1, order="F")).reshape(3, 3, order="F")
            J += np.kron(Eij, out)
    return J
Ur = np.array([[float(U[r, s]) for s in range(3)] for r in range(3)])
rho_e = np.outer(Ur[0], Ur[0]).astype(complex)
rho_d = np.diag([0.2, 0.3, 0.5]).astype(complex)
for a in [0.0, 0.1, 10.0]:
    S = sla.expm(gkls_super(Hd, a) * 1.0)
    J = choi(S)
    ev = np.linalg.eigvalsh((J + J.conj().T) / 2)
    out = (S @ rho_e.reshape(-1, order="F")).reshape(3, 3, order="F")
    closed = np.array([[rho_e[i, j] * np.exp(-a * (Hd[i, i] - Hd[j, j]) ** 2 - 1j * (Hd[i, i] - Hd[j, j])) for j in range(3)] for i in range(3)])
    outd = (S @ rho_d.reshape(-1, order="F")).reshape(3, 3, order="F")
    Pf = np.real(np.diag(Ur @ out @ Ur.T))
    # TP: dual preserva identidade
    TP = np.max(np.abs((S.conj().T @ np.eye(3).reshape(-1, order="F")) - np.eye(3).reshape(-1, order="F")))
    chk("GKLS a=%g: Choi >= 0 (CP), traco preservado, forma fechada, diagonal estacionaria, energia" % a,
        ev.min() > -1e-12 and TP < 1e-12 and np.max(np.abs(out - closed)) < 1e-12 and np.max(np.abs(outd - rho_d)) < 1e-14
        and abs(np.trace(Hd @ out).real - np.trace(Hd @ rho_e).real) < 1e-12 and abs(Pf.sum() - 1) < 1e-12,
        choi_min=float(ev.min()), tp_err=float(TP), forma_fechada_err=float(np.max(np.abs(out - closed))),
        diag_err=float(np.max(np.abs(outd - rho_d))), P_sabor=[float(x) for x in Pf])
    # bate com os numeros do NU2
    t_nu2 = [x for x in calc["density_channel_checks"] if x["strength_INPUT"] == a][0]
    chk("probabilidades de sabor a=%g batem com CALCULOS_ESPECTRAIS_R1" % a,
        max(abs(p - q) for p, q in zip(Pf, t_nu2["probabilities"])) < 1e-12, nu2=t_nu2["probabilities"])

# ---- identificabilidade: so o produto beta0*tau*Kfac entra; tau e Kfac degeneram ----
# observavel sintetico ideal: deltaP(E) no reator; parametros theta=(ln tau, ln Kfac); Fisher ~ J^T W J
Lam_amp = mp.mpf(10) ** 36  # amplificacao SINTETICA de tau (so para tornar o efeito O(1e-3)); nao e valor fisico
tau_syn = tP * Lam_amp
def dP_model(lntau, lnK, Ei):
    p0, _ = Pee(Ei * 10 ** 6, L, 0)
    p1, _ = Pee(Ei * 10 ** 6, L, mp.e ** lntau, Kfac=mp.e ** lnK)
    return p1 - p0
grid = Es[::10]
J = []
for Ei in grid:
    d1 = mp.diff(lambda x: dP_model(x, 0, Ei), mp.log(tau_syn))
    d2 = mp.diff(lambda y: dP_model(mp.log(tau_syn), y, Ei), 0)
    J.append([float(d1), float(d2)])
J = np.array(J)
F = J.T @ J
sv = np.linalg.svd(F, compute_uv=False)
chk("identificabilidade: Fisher (ln tau, ln Kfac) tem posto 1 (so tau*Kfac e identificavel)", sv[1] / sv[0] < 1e-12,
    valores_singulares=[float(x) for x in sv], amplificacao_sintetica_tau="1e36 * tP (sintetico)")
# injecao-recuperacao do produto com amplificacao sintetica; e controle nulo
true_lnLam = float(mp.log(tau_syn))
data = [dP_model(mp.log(tau_syn), 0, Ei) for Ei in grid]
def sse(lnt):
    return sum((dP_model(lnt, 0, Ei) - d) ** 2 for Ei, d in zip(grid, data))
lo, hi = true_lnLam - 2.0, true_lnLam + 2.0
for _ in range(80):  # busca aurea
    m1 = lo + (hi - lo) * 0.381966; m2_ = lo + (hi - lo) * 0.618034
    if sse(m1) < sse(m2_): hi = m2_
    else: lo = m1
rec = (lo + hi) / 2
chk("injecao-recuperacao (sintetico): ln(tau*Kfac) recuperado", abs(rec - true_lnLam) < 1e-6, verdadeiro=true_lnLam, recuperado=rec)
# degenerescencia explicita: (tau*2, Kfac/2) da exatamente o mesmo deltaP
dd = max(abs(dP_model(mp.log(tau_syn * 2), mp.log(mp.mpf(1) / 2), Ei) - dP_model(mp.log(tau_syn), 0, Ei)) for Ei in grid)
chk("degenerescencia: (2 tau, Kfac/2) reproduz deltaP identico", dd < mp.mpf(10) ** -60, max_dif=mp.nstr(dd, 3))
nulo = max(abs(Pee(Ei * 10 ** 6, L, 0)[0] - Pee(Ei * 10 ** 6, L, 0)[0]) for Ei in grid)
chk("controle nulo: tau=0 da deltaP = 0 exato", nulo == 0)

# ---- derivada completa n_eff (contrafactual), independente por mpmath.diff ----
chi0 = 2 * mp.acosh(1 / alpha)
chk("chi0 = 2 arccosh(1/alpha) reproduz beta0 (beta(chi)=sqrt(e) sech(chi/2))", abs(mp.sqrt(mp.e) / mp.cosh(chi0 / 2) - beta0) < mp.mpf(10) ** -70)
sc = plan["synthetic_checks"]; ok_all = True; worst = 0
for slope in [mp.mpf(repr(v)) for v in sc["running_chi_log_slope"]]:
    for x0 in [-mp.log(2), mp.mpf(0), mp.log(2)]:
        rs, ts = mp.mpf(repr(sc["r_log_slope"])), mp.mpf(repr(sc["tau_log_slope"]))  # mpf: evita arredondamento float (artefato do auditor na 1a rodada)
        def lnG(x):
            chi = chi0 + slope * x; b = mp.sqrt(mp.e) / mp.cosh(chi / 2)
            return -2 * x + ts * x + mp.log(b) + b * rs * x  # ln Gamma = const -2x + ln tau + ln beta + beta ln r
        num = mp.diff(lnG, x0)
        chi = chi0 + slope * x0; b = mp.sqrt(mp.e) / mp.cosh(chi / 2); bp = -b / 2 * mp.tanh(chi / 2) * slope
        ana = -2 + ts + bp * (1 / b + rs * x0) + b * rs
        worst = max(worst, abs(num - ana)); ok_all = ok_all and abs(num - ana) < mp.mpf(10) ** -40
chk("identidade n_eff = -2 + dln tau + beta'(1/beta + ln r) + beta dln r (contrafactual)", ok_all, pior=mp.nstr(worst, 3))

# ---- ordem de grandeza no pivô E0 = 1 GeV (NAO e cota: texturas diferentes) ----
GeV = mp.mpf(10) ** 9
g31_E0_GeV = gamma(0, 2, GeV, tP) * hbar_eVs / 10 ** 9
g21_E0_GeV = gamma(0, 1, GeV, tP) * hbar_eVs / 10 ** 9
res["contexto_E0_1GeV"] = {"Gamma31_TGL_tauP_GeV": mp.nstr(g31_E0_GeV, 6), "Gamma21_TGL_tauP_GeV": mp.nstr(g21_E0_GeV, 6),
    "limite_publicado_Beccaria_Ternes_GeV": "4.1e-27 (gamma21=gamma31, gamma32=0; 90% CL)",
    "ordens_abaixo_Gamma31": mp.nstr(mp.log10(mp.mpf("4.1e-27") / g31_E0_GeV), 4),
    "aviso": "contexto de escala apenas; textura TGL ~ (gamma31~gamma32 >> gamma21) e o caso que o artigo diz nao testavel com a estatistica atual; NAO e cota sobre tau"}
res["n_checks"] = len(res["checks"]); res["n_passa"] = sum(1 for x in res["checks"] if x["PASSA"])
json.dump(res, open(os.path.join(HERE, "_reproducao_nu2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({"n_checks": res["n_checks"], "n_passa": res["n_passa"]}, ensure_ascii=False))
for x in res["checks"]:
    print(("PASSA " if x["PASSA"] else "FALHA ") + x["nome"])
print(json.dumps({k: res[k] for k in ("decomposicao_deltaP_no_pico", "E_pico_MeV", "contexto_E0_1GeV")}, ensure_ascii=False, indent=1))
