# -*- coding: utf-8 -*-
# Sonda do auditor (estatuto): o «Tudo» tipado pela pedra, D_inf(F_thM(1)) = diag(1-beta, beta), e um ponto
# de UMA passagem; sob o canal iterado da F1.ATRATOR, C = D o Ad(S) o D, ele NAO e fixo e C^n -> I/2.
# beta NUNCA literal: alpha lido dos bytes da linha unica 'ALPHA_FINE_CODATA_2018 = ...' do um.py (sem executar).
import re, math, json, os, hashlib
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
UMPY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um" + "\\N\u00f3s\\um.py"
b = open(UMPY, "rb").read()
sha = hashlib.sha256(b).hexdigest()
linhas = b.split(b"\n")
alvo = [i for i, l in enumerate(linhas, 1) if re.match(rb"^ALPHA_FINE_CODATA_2018\s*=\s*[0-9.eE+-]+\s*$", l.strip())]
if len(alvo) != 1:
    raise SystemExit("FALHA VISIVEL: linha de ALPHA_FINE_CODATA_2018 nao unica: %r" % alvo)
alpha_txt = linhas[alvo[0] - 1].split(b"=", 1)[1].strip().decode()
beta = float(alpha_txt) * math.sqrt(math.e)
conf = repr(beta) == "0.012031300400803142"   # so conferencia (a ordem fornece o numero)
thM = math.asin(math.sqrt(beta))
c, s = math.cos(thM), math.sin(thM)
S = np.array([[c, s], [-s, c]], dtype=complex)          # Smat do kernel
rho_star = np.array([[1, 0], [0, 0]], dtype=complex)
D = lambda x: np.diag(np.diag(x))                         # D_inf = diagExpect
F = lambda x: S @ x @ S.conj().T                          # Ad(S)
tudo = D(F(rho_star))                                     # o ponto final de uma passagem
C = lambda x: D(F(D(x)))                                  # canal da F1.ATRATOR
x = tudo.copy(); traj = []
for n in range(0, 4097):
    if n in (0, 1, 2, 10, 100, 1000, 4096):
        traj.append({"n": n, "p0": float(x[0, 0].real), "p1": float(x[1, 1].real),
                     "posto": int(np.linalg.matrix_rank(x, tol=1e-12)), "dist_I2": float(np.linalg.norm(x - np.eye(2) / 2))})
    x = C(x)
out = {"um_py_sha256": sha, "alpha_linha": alvo[0], "alpha_texto": alpha_txt, "beta_repr": repr(beta),
       "beta_confere": conf, "theta_M": thM,
       "tudo_uma_passagem": {"p0": float(tudo[0, 0].real), "p1": float(tudo[1, 1].real),
                             "p1_menos_beta": float(tudo[1, 1].real) - beta,
                             "posto": int(np.linalg.matrix_rank(tudo, tol=1e-12))},
       "C_de_tudo_igual_tudo": bool(np.allclose(C(tudo), tudo, atol=1e-15)),
       "C_de_tudo_p1": float(C(tudo)[1, 1].real),
       "C_de_tudo_p1_forma_fechada_2b(1-b)": 2 * beta * (1 - beta),
       "trajetoria": traj,
       "leitura": "[REAL medido aqui] o ponto final de UMA passagem carrega beta como peso; o canal iterado o leva a I/2 "
                  "(beta so fixa a taxa lambda = 1 - 2beta, cf. F1.ATRATOR). O «Tudo» da pedra nao e o atrator."}
json.dump(out, open(os.path.join(AQUI, "SONDA_ITERACAO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
