# -*- coding: utf-8 -*-
"""C -- os 14 controles, recalculados pelo auditor SEM o codigo do construtor (mpmath 40 digitos; C11 em float64
como o protocolo manda). Cada controle tem de FALHAR SEM A HIPOTESE: o que se mede e que o enunciado de origem,
sem a hipotese nomeada, cai na instancia dada."""
import json, math, os, re

import mpmath as mp

mp.mp.dps = 40
R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UMPY = os.path.join(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um", "N\u00f3s", "um.py")
alpha_txt = None
for ln in open(UMPY, "rb").read().split(b"\n"):
    m = re.match(rb"ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", ln)
    if m:
        alpha_txt = m.group(1).decode()
        break
beta = mp.mpf(alpha_txt) * mp.sqrt(mp.e)
thM = mp.asin(mp.sqrt(beta))
M = mp.matrix
I2 = mp.eye(2)
P = M([[1, 0], [0, 0]])
Q0 = I2 - P


def tr(A):
    return sum(A[i, i] for i in range(A.rows))


def rank(A, tol=mp.mpf("1e-25")):
    return sum(1 for s in mp.svd_r(A, compute_uv=False) if s > tol)


def rot_S(th):
    return M([[mp.cos(th), mp.sin(th)], [-mp.sin(th), mp.cos(th)]])


def rhoOut(th):
    S = rot_S(th)
    return S * P * S.T


def deph(g, t, X):
    return M([[mp.e ** (-t * g[i][j]) * X[i, j] for j in range(2)] for i in range(2)])


def diagE(X):
    return M([[X[0, 0], 0], [0, X[1, 1]]])


def nrm(X):
    return mp.sqrt(sum(abs(X[i, j]) ** 2 for i in range(X.rows) for j in range(X.cols)))


res = {}
C1 = mp.diag([mp.mpf(2) / 3, mp.mpf(2) / 3, mp.mpf(-1) / 3])
res["C1"] = dict(traco=mp.nstr(tr(C1), 15), traco_quadrado=mp.nstr(tr(C1 * C1), 15), posto=rank(C1),
                 menor_autovalor=mp.nstr(min(C1[i, i] for i in range(3)), 5),
                 falha_sem_hipotese=(abs(tr(C1) - 1) < 1e-30 and abs(tr(C1 * C1) - 1) < 1e-30 and rank(C1) == 3))
C2 = P / 2
res["C2"] = dict(posto=rank(C2), pureza=mp.nstr(tr(C2 * C2), 10), falha_sem_hipotese=(rank(C2) == 1 and abs(tr(C2 * C2) - 0.25) < 1e-30))
H = I2 / 2
res["C3"] = dict(traco=mp.nstr(tr(H), 5), posto=rank(H), falha_sem_hipotese=(rank(H) == 2 and abs(tr(H) - 1) < 1e-30))
res["C4"] = dict(peso=mp.nstr(tr(P * Q0), 5), PrhoP_norma=mp.nstr(nrm(P * Q0 * P), 5),
                 falha_sem_hipotese=(tr(P * Q0) == 0 and nrm(P * Q0 * P) == 0))
out5 = (I2 * H * I2) / tr(I2 * H)
res["C5"] = dict(posto_saida=rank(out5), falha_sem_hipotese=(rank(out5) == 2))
A6 = mp.diag([2, 1])
res["C6"] = dict(traco=mp.nstr(tr(A6 * P * A6.T), 5), falha_sem_hipotese=(tr(A6 * P * A6.T) == 4))
Y7 = Q0 * P * Q0.T
res["C7"] = dict(posto=rank(Y7), falha_sem_hipotese=(rank(Y7) == 0))
c8 = {}
for lab, th in (("0", mp.mpf(0)), ("pi/2", mp.pi / 2)):
    F = rhoOut(th)
    c8[lab] = dict(dist=mp.nstr(nrm(diagE(F) - F), 5), posto=rank(diagE(F)))
res["C8"] = dict(c8, falha_sem_hipotese=all(float(mp.mpf(v["dist"])) < 1e-30 and v["posto"] == 1 for v in c8.values()))
F = rhoOut(thM)
g0 = [[0, 0], [0, 0]]
d9 = max(nrm(deph(g0, t, F) - F) for t in (0, 0.5, 1, 2, 5, 10, 100))
res["C9"] = dict(max_dist_Dt_id=mp.nstr(d9, 5), dist_F_a_Dinf=mp.nstr(nrm(F - diagE(F)), 8),
                 falha_sem_hipotese=(d9 == 0 and nrm(F - diagE(F)) > 1e-6))
R = M([[mp.cos(thM), -mp.sin(thM)], [mp.sin(thM), mp.cos(thM)]])
Qth = R * Q0 * R.T
plus = M([[0.5, 0.5], [0.5, 0.5]])
g1 = [[0, 1], [1, 0]]
vals = [tr(plus * deph(g1, t, Qth)) for t in (0, 0.5, 1, 2, 5, 10, 100)]
res["C10"] = dict(valores=[mp.nstr(v, 10) for v in vals], variacao=mp.nstr(max(vals) - min(vals), 8),
                  formula_t0=mp.nstr(mp.mpf(0.5) - mp.sin(thM) * mp.cos(thM), 10),
                  falha_sem_hipotese=(max(vals) - min(vals) >= 1e-3))
mx11 = max(math.sin(n * math.pi) ** 2 for n in range(100001))
res["C11"] = dict(max_sin2_npi_float64=mx11, falha_sem_hipotese=(mx11 <= 1e-10))
F0 = rhoOut(mp.mpf(0))
d12 = max(nrm(deph(g, t, F0) - F0) for g in ([[0, 1], [1, 0]], [[0, beta], [beta, 0]]) for t in (0.5, 1, 2, 5, 10, 100))
res["C12"] = dict(t2=mp.nstr(mp.cos(0) ** 2, 5), max_dist=mp.nstr(d12, 5), falha_sem_hipotese=(d12 == 0))
F90 = rhoOut(mp.pi / 2)
d13 = max(nrm(deph(g, t, F90) - F90) for g in ([[0, 1], [1, 0]], [[0, beta], [beta, 0]]) for t in (0.5, 1, 2, 5, 10, 100))
res["C13"] = dict(r2=mp.nstr(mp.sin(mp.pi / 2) ** 2, 5), max_dist=mp.nstr(d13, 5), falha_sem_hipotese=(d13 < 1e-30))
res["C14"] = dict(norma=mp.nstr(nrm(Q0 * P + P * Q0), 5), falha_sem_hipotese=(nrm(Q0 * P + P * Q0) == 0))
res["todos_falham_sem_hipotese"] = all(v["falha_sem_hipotese"] for k, v in res.items() if k.startswith("C"))
with open(os.path.join(R2, "saidas", "C_CONTROLES_INDEPENDENTE.json"), "x", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1, default=str)
for k, v in res.items():
    print(k, v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items()})
