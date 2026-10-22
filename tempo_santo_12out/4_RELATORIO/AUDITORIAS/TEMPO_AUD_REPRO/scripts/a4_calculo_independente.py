"""A4 — SEGUNDO CALCULO INDEPENDENTE do auditor (nao usa o codigo do construtor).
beta: alpha lido dos BYTES do um.py (busca propria por linha + ast.parse da AST de topo; nunca executa);
beta = alpha*sqrt(e) em mpmath (50 digitos) e em float. Nenhum literal de beta neste arquivo.
Afirmacoes recalculadas por formas fechadas em mpmath e por construcao propria em numpy:
 T1 (min ||TH-HT-i1||_F = sqrt n), T3/T11 (omega_1, P_1, omega_k), T4 (det T, M_N, boost k=100, volume Davies),
 T6 (pureza de Davies), T7 (lambda_min de T_{-t} psi+), T8 (k_eps), T9 (||F^2-F||, queda do posto numerico,
 e a FALHA do T9.o(c): potencia de T em float64 x potencia exata do T em float).
Saida: JSON no caminho dado."""
import ast
import json
import math
import os
import sys

import mpmath as mp
import numpy as np

UMPY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
PRE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO\PREREGISTRO.json"
mp.mp.dps = 50
out = {}

# ---------------------------------------------------------------- beta dos bytes do um.py
raw = open(UMPY, "rb").read()
import hashlib
out["um_py"] = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
txt = raw.decode("utf-8")
lines = txt.split("\n")
ocorr = []
for i, ln in enumerate(lines, 1):
    if "ALPHA_FINE_CODATA_2018" in ln and "=" in ln and ln.lstrip().startswith("ALPHA_FINE_CODATA_2018"):
        ocorr.append({"linha": i, "indentada": ln[:1] in (" ", "\t"), "texto": ln.strip()[:120]})
sealed_lines = [{"linha": i, "texto": ln.strip()[:120]} for i, ln in enumerate(lines, 1)
                if ln.startswith("SEALED_CODATA_ALPHA")]
tree = ast.parse(txt)
top_sealed = [n for n in tree.body if isinstance(n, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id == "SEALED_CODATA_ALPHA" for t in n.targets)]
top_alpha = [n for n in tree.body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == "ALPHA_FINE_CODATA_2018" for t in n.targets)]
sealed_val = ast.literal_eval(top_sealed[0].value) if len(top_sealed) == 1 else None
nao_indent = [o for o in ocorr if not o["indentada"]]
cont = None
if len(nao_indent) == 1:
    L = nao_indent[0]["linha"]
    for n in tree.body:
        if n.lineno <= L <= (n.end_lineno or n.lineno):
            cont = {"tipo": type(n).__name__, "ini": n.lineno, "fim": n.end_lineno,
                    "alvos": [getattr(t, "id", None) for t in getattr(n, "targets", [])]}
    lit = nao_indent[0]["texto"].split("=", 1)[1].split("#")[0].strip()
    alpha_l = ast.literal_eval(lit)
else:
    alpha_l = None
out["alpha"] = {"ocorrencias_atribuicao": ocorr, "nao_indentadas": len(nao_indent), "SEALED_linhas": sealed_lines,
                "SEALED_na_AST_de_topo": [n.lineno for n in top_sealed], "ALPHA_FINE_na_AST_de_topo": [n.lineno for n in top_alpha],
                "SEALED_valor": sealed_val, "alpha_linha_nao_indentada": alpha_l, "conteiner_da_linha": cont,
                "iguais": sealed_val == alpha_l}
alpha = alpha_l
assert alpha is not None and alpha == sealed_val, "fail-closed: alpha nao lido"
beta_f = alpha * math.sqrt(math.e)
beta = mp.mpf(alpha) * mp.sqrt(mp.e)  # alpha float -> mpf exato do literal em float
beta_dec = mp.mpf(str(alpha)) * mp.sqrt(mp.e)  # alpha decimal exato do literal
conf = json.load(open(PRE, encoding="utf-8"))["numeros_de_conferencia"]
out["beta"] = {"float": beta_f, "mpmath_do_float_alpha": mp.nstr(beta, 25), "mpmath_do_literal_decimal": mp.nstr(beta_dec, 25),
               "conferencia_preregistro": conf["beta"], "dif_float_conferencia": abs(beta_f - conf["beta"])}

B = beta  # 50 digitos
lam = 1 - 2 * B
res = {}
# ---------------------------------------------------------------- T3 / T11
w1 = mp.log((1 - B) / B)
P1 = 2 * mp.pi / w1
res["T3"] = {"omega1": mp.nstr(w1, 20), "omega1_conf": conf["omega1"], "P1": mp.nstr(P1, 20), "P1_conf": conf["P1"],
             "identidade_2artanh(1-2b)=ln((1-b)/b)": mp.nstr(abs(2 * mp.atanh(lam) - w1), 5)}
wk = {}
for k in (1, 10, 100, 1000):
    # construcao propria: populacoes de C^k(E00) = T^k (1,0), T = [[1-b, b],[b, 1-b]] em mpmath
    p = mp.matrix([[1], [0]])
    Tm = mp.matrix([[1 - B, B], [B, 1 - B]])
    Tk = Tm ** k
    v = Tk * p
    c = v[0] - v[1]
    wk[str(k)] = {"omega_k_por_populacoes": mp.nstr(mp.log(v[0] / v[1]), 20),
                  "2artanh(lam^k)": mp.nstr(2 * mp.atanh(lam ** k), 20),
                  "conf": conf["omega_k"][str(k)], "c_k": mp.nstr(c, 20)}
res["T11"] = wk
# ---------------------------------------------------------------- T4
res["T4_detT"] = {"det": mp.nstr(Tm[0, 0] * Tm[1, 1] - Tm[0, 1] * Tm[1, 0], 20), "1-2b": mp.nstr(lam, 20), "conf": conf["det_T"]}
th = mp.asin(mp.sqrt(B))
MN = {}
for N in (100, 1000, 10000):
    # distancia de Frobenius entre rho_k e rho_N (rho_k = R(k th) E00 R(k th)^T), k em [N, 2N]
    best = mp.mpf(0)
    for m in range(0, N + 1):
        a = m * th  # rho_{N+m} vs rho_N: so importa o angulo relativo m*th
        # rho(phi) = [[cos^2, -cos sin],[-cos sin, sin^2]]; ||rho(phi1)-rho(phi2)||_F = sqrt(2)|sin(phi1-phi2)|
        d = mp.sqrt(2) * abs(mp.sin(a))
        if d > best:
            best = d
    MN[str(N)] = {"M_N": mp.nstr(best, 20), "conf": conf["noland_M_N"][str(N)]}
res["T4_M_N"] = MN
# conferencia direta (sem a forma fechada) em numpy para N = 100
S = lambda phi: np.array([[math.cos(phi), math.sin(phi)], [-math.sin(phi), math.cos(phi)]])
E00 = np.array([[1.0, 0.0], [0.0, 0.0]])
thf = math.asin(math.sqrt(beta_f))
rN = S(100 * thf) @ E00 @ S(100 * thf).T
res["T4_M_100_numpy_direto"] = max(float(np.linalg.norm(S(k * thf) @ E00 @ S(k * thf).T - rN)) for k in range(100, 201))
res["T4_boost_k100"] = {"sqrt2*e^-100": mp.nstr(mp.sqrt(2) * mp.exp(-100), 25), "conf": conf["boost_k100_decimal"]}
g01 = B * abs(mp.log((1 - B) / B))
res["T4_volume_davies_t1"] = {"e^-2g01": mp.nstr(mp.exp(-2 * g01), 20), "conf": conf["vol_davies_t1"], "g01": mp.nstr(g01, 20),
                              "g01_conf": conf["g01"]}
# ---------------------------------------------------------------- T6
res["T6_pur_psi_t1"] = {"(1+e^-2g01)/2": mp.nstr((1 + mp.exp(-2 * g01)) / 2, 20), "conf": conf["pur_psi_t1"]}
# ---------------------------------------------------------------- T7
def lmin(gt):
    # T_{-t} psi+ = 1/2 [[1, e^{gt}],[e^{gt}, 1]]: autovalores (1 +- e^{gt})/2
    M = mp.matrix([[mp.mpf(1) / 2, mp.exp(gt) / 2], [mp.exp(gt) / 2, mp.mpf(1) / 2]])
    ev = mp.eigsy(M)[0]
    return min(ev[0], ev[1]), (1 - mp.exp(gt)) / 2


res["T7"] = {}
for nome, gt, ck in (("gt=beta", B, "neg_beta"), ("gt=1", mp.mpf(1), "neg_1"), ("gt=10", mp.mpf(10), "neg_10"),
                     ("davies t=1", g01, "neg_davies")):
    e, f = lmin(gt)
    res["T7"][nome] = {"lambda_min_eigsy": mp.nstr(e, 20), "(1-e^gt)/2": mp.nstr(f, 20), "conf": conf[ck]}
# ---------------------------------------------------------------- T8
res["T8_k_eps"] = {}
for eps in ("0.1", "0.001", "1e-06"):
    q = mp.log(mp.mpf(eps)) / mp.log(lam)
    k = int(mp.floor(q)) + 1
    res["T8_k_eps"][eps] = {"k_eps": k, "lam^k<eps": bool(lam ** k < mp.mpf(eps)), "eps<=lam^(k-1)": bool(mp.mpf(eps) <= lam ** (k - 1)),
                            "frac": mp.nstr(q - mp.floor(q), 16), "conf_k": conf["k_eps"][eps], "conf_frac": conf["frac_eps"][eps]}
# ---------------------------------------------------------------- T9
IR = mp.matrix([[0.5, -0.5], [-0.5, 0.5]])
nIR = mp.sqrt(sum(IR[i, j] ** 2 for i in range(2) for j in range(2)))
res["T9_F"] = {"||I-R||_F": mp.nstr(nIR, 10)}
for t in ("1e-6", "0.001", "0.1", "1", "10", "30"):
    tt = mp.mpf(t)
    F = mp.matrix([[0.5, 0.5], [0.5, 0.5]]) + mp.exp(-tt) * IR
    F2 = F * F - F
    nn = mp.sqrt(sum(F2[i, j] ** 2 for i in range(2) for j in range(2)))
    res["T9_F"]["t=" + t] = {"||F^2-F||_F": mp.nstr(nn, 20), "e^-t(1-e^-t)": mp.nstr(mp.exp(-tt) * (1 - mp.exp(-tt)), 20),
                             "det F": mp.nstr(F[0, 0] * F[1, 1] - F[0, 1] * F[1, 0], 20), "e^-t": mp.nstr(mp.exp(-tt), 20)}
# queda do posto numerico (limiar 1e-12 * s_max): s(T^k) = {1, lam^k}
kdrop = int(mp.floor(mp.log(mp.mpf("1e-12")) / mp.log(lam))) + 1
res["T9_k_drop_exato"] = {"k": kdrop, "conf": conf["k_rank_drop"]}

# a FALHA do T9.o(c): construcao propria do T em float (|S|^2 entrada a entrada, S = [[c, s],[-s, c]])
c0, s0 = math.cos(thf), math.sin(thf)
Tf = np.array([[c0 * c0, s0 * s0], [s0 * s0, c0 * c0]])  # |S|^2
Tf_alt = np.array([[1 - beta_f, beta_f], [beta_f, 1 - beta_f]])
Rf = np.full((2, 2), 0.5)
lamf = 1.0 - 2.0 * beta_f
colsum = [mp.mpf(Tf[0, 0]) + mp.mpf(Tf[1, 0]) - 1, mp.mpf(Tf[0, 1]) + mp.mpf(Tf[1, 1]) - 1]
colsum_alt = [mp.mpf(Tf_alt[0, 0]) + mp.mpf(Tf_alt[1, 0]) - 1]
res["T9c"] = {"T_float_igual_ao_do_construtor_|S|^2": None, "delta_coluna_T(|S|^2)": [mp.nstr(x, 6) for x in colsum],
              "delta_coluna_T([[1-b,b],[b,1-b]])": [mp.nstr(x, 6) for x in colsum_alt]}
# potencia em float64 (matrix_power) e potencia EXATA do float (mpmath 60 dig., quadrados repetidos)
mp.mp.dps = 60
Tm_f = mp.matrix([[mp.mpf(Tf[0, 0]), mp.mpf(Tf[0, 1])], [mp.mpf(Tf[1, 0]), mp.mpf(Tf[1, 1])]])
lam_m = mp.mpf(1) - 2 * B


def dev_exact(k):
    Pk = Tm_f ** k
    Ref = mp.matrix([[0.5, 0.5], [0.5, 0.5]]) + (lam_m ** k) * IR
    return max(abs(Pk[i, j] - Ref[i, j]) for i in range(2) for j in range(2))


Pw = np.eye(2)
first_over = None
worst = 0.0
kworst = 0
for k in range(0, 10001):
    if k > 0:
        pass
    Mk = np.linalg.matrix_power(Tf, k)
    d = float(np.max(np.abs(Mk - (Rf + lamf ** k * (np.eye(2) - Rf)))))
    if d > worst:
        worst, kworst = d, k
    if first_over is None and d > 1e-13:
        first_over = k
res["T9c"].update({"matrix_power_float64_max_dif_k<=1e4": worst, "k_do_max": kworst, "primeiro_k_acima_de_1e-13": first_over,
                   "potencia_exata_do_T_float_dif_k=4096": mp.nstr(dev_exact(4096), 6),
                   "potencia_exata_do_T_float_dif_k=1e4": mp.nstr(dev_exact(10000), 6),
                   "k*|delta|/2 em k=1e4": mp.nstr(10000 * abs(colsum[0]) / 2, 6)})
# T1: min_T ||TH-HT-i1||_F por vetorizacao PROPRIA (linha-major) e por argumento de traco
rng = np.random.default_rng(777)
dev = 0.0
for n in (2, 3, 4, 5, 8):
    I = np.eye(n)
    for _ in range(50):
        A = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
        H = (A + A.conj().T) / 2
        # vec linha-major: vec(TH) = (I kron H^T) vec(T); vec(HT) = (H kron I) vec(T)
        L = np.kron(I, H.T) - np.kron(H, I)
        b = (1j * I).reshape(-1)
        v = np.linalg.lstsq(L, b, rcond=None)[0]
        dev = max(dev, abs(np.linalg.norm(L @ v - b) - math.sqrt(n)))
res["T1_lstsq_desvio_max_de_sqrt_n"] = dev
res["T1_argumento"] = "tr(TH-HT)=0 => <TH-HT, i1>_F = 0 => ||TH-HT-i1||^2 = ||TH-HT||^2 + n >= n, igualdade em T=0"
out["recalculo"] = res


def conv(o):
    if isinstance(o, dict):
        return {k: conv(v) for k, v in o.items()}
    if isinstance(o, list):
        return [conv(v) for v in o]
    if isinstance(o, (mp.mpf,)):
        return mp.nstr(o, 20)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


tmp = sys.argv[1] + ".tmp"
with open(tmp, "w", encoding="utf-8") as fo:
    json.dump(conv(out), fo, indent=1, ensure_ascii=False)
os.replace(tmp, sys.argv[1])
print(json.dumps(conv(out), ensure_ascii=False, indent=1))
