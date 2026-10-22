# -*- coding: utf-8 -*-
"""Ensaio numerico curto de I1-I2 (F1.IDENTIDADE). alpha lido nos BYTES da l.5557 do um.py v391 (sem executar o
um.py); beta = alpha*sqrt(e) calculado em runtime e usado so como taxa de defasagem de teste. Estatuto: COMPUTED.
Grava logs/ENSAIO_NUMERICO.json."""
import os, json, math, hashlib, re
import numpy as np

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/um.py"
b = open(U, "rb").read()
sha16 = hashlib.sha256(b).hexdigest()[:16]
linha = b.split(b"\n")[5556].decode("utf-8").rstrip("\r")
m = re.fullmatch(r"ALPHA_FINE_CODATA_2018 = ([0-9.eE+-]+)", linha)
assert m, linha
ALPHA = float(m.group(1))
BETA = ALPHA * math.sqrt(math.e)  # runtime, nunca literal


def ident(a):
    q = math.sqrt(max(0.0, 1 - a * a))
    v = np.array([q, a], dtype=complex)
    return q, v, np.outer(v, v.conj())


def dephase(P, g01, g10, t):
    D = P.copy()
    D[0, 1] *= math.exp(-t * g01)
    D[1, 0] *= math.exp(-t * g10)
    return D


q, v, P = ident(ALPHA)
res = {"um_py_sha16": sha16, "linha_5557": linha, "alpha": ALPHA, "beta_runtime": BETA, "estatuto": "COMPUTED",
       "I2": {}, "I1": [], "C2": {}, "C3": {}}
res["I2"] = {
    "q": q, "q2_mais_a2_menos_1": q * q + ALPHA * ALPHA - 1,
    "traco_menos_1": abs(np.trace(P) - 1),
    "norma_P2_menos_P": float(np.linalg.norm(P @ P - P)),
    "posto": int(np.linalg.matrix_rank(P)),
    "leitura_interior": float(P[1, 1].real), "leitura_interior_menos_alpha2": float(P[1, 1].real - ALPHA ** 2),
    "leitura_inscricao_menos_q2": float(P[0, 0].real - q * q),
    "alpha_recuperado": math.sqrt(P[1, 1].real), "recuperado_menos_alpha": math.sqrt(P[1, 1].real) - ALPHA,
    "auto_leitura_v_P_v_menos_1": abs(np.vdot(v, P @ v) - 1),
}
for t in [0.0, 0.1, 1.0, 10.0, 100.0, 1000.0]:
    D = dephase(P, BETA, BETA, t)
    det = np.linalg.det(D).real
    formula = q * q * ALPHA * ALPHA * (1 - math.exp(-t * 2 * BETA))
    res["I1"].append({"t": t, "traco_menos_1": abs(np.trace(D) - 1), "det": det, "det_formula": formula,
                      "det_menos_formula": det - formula, "posto_numpy": int(np.linalg.matrix_rank(D)),
                      "posto_por_det": 2 if formula > 0 else 1})
E = np.diag(np.diag(P))
res["I1_limite"] = {"traco_menos_1": abs(np.trace(E) - 1), "posto": int(np.linalg.matrix_rank(E)),
                    "det": float(np.linalg.det(E).real)}
for a in [0.0, 1.0]:
    _, _, Pa = ident(a)
    res["C2"][str(a)] = {"P": [[float(x.real) for x in r] for r in Pa], "posto_limite": int(np.linalg.matrix_rank(np.diag(np.diag(Pa))))}
for a in [1.5, -1.5]:
    qa = math.sqrt(max(0.0, 1 - a * a))  # Real.sqrt de negativo = 0, como no Lean
    res["C3"][str(a)] = {"q2_mais_a2": qa * qa + a * a, "quebra": abs(qa * qa + a * a - 1) > 1e-12}
a = -ALPHA
_, _, Pn = ident(a)
res["C3"]["alpha_negativo"] = {"a": a, "forma": math.sqrt(1 - a * a) ** 2 + a * a, "recuperado": math.sqrt(Pn[1, 1].real)}
ok = (res["I2"]["traco_menos_1"] < 1e-12 and res["I2"]["norma_P2_menos_P"] < 1e-12 and res["I2"]["posto"] == 1
      and abs(res["I2"]["leitura_interior_menos_alpha2"]) < 1e-15
      and all(r["traco_menos_1"] < 1e-12 for r in res["I1"])
      and all(r["posto_por_det"] == (1 if r["t"] == 0 else 2) for r in res["I1"])
      and res["I1_limite"]["posto"] == 2)
res["criterios_pre_registrados_ok"] = bool(ok)
json.dump(res, open(os.path.join(AQUI, "logs", "ENSAIO_NUMERICO.json"), "w", encoding="utf-8"), indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
