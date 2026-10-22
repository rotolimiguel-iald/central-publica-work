# -*- coding: utf-8 -*-
# Conferencia (nao e teste pre-registrado): le alpha nos BYTES do um.py v391 sem executa-lo, calcula beta = alpha*sqrt(e)
# em runtime e confere as IDENTIDADES canonicas que a trilha cita. Objetivo do levantamento: mostrar quais numeros sao
# identidades por construcao (nao podem servir de falsificador). Nenhum dado observado. beta nunca literal.
import re, ast, math, hashlib, json, os
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
UM = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\um.py"
with open(UM, "rb") as fh:
    B = fh.read()
sha = hashlib.sha256(B).hexdigest()


def le_atribuicao(nome):
    m = re.search(rb"(?m)^" + nome.encode() + rb"\s*=\s*([0-9.eE+\-]+)", B)
    if not m:
        raise SystemExit("FALHA VISIVEL: atribuicao de %s nao encontrada" % nome)
    linha = B.count(b"\n", 0, m.start()) + 1
    return ast.literal_eval(m.group(1).decode()), linha


alpha, l_alpha = le_atribuicao("ALPHA_FINE_CODATA_2018")
alpha_sel, l_sel = le_atribuicao("SEALED_CODATA_ALPHA")
beta = alpha * math.sqrt(math.e)
beta_exp = alpha * math.exp(0.5)
CONFERENCIA = "0.012031300400803142"          # so para conferencia (texto), nunca usado no calculo
theta = math.asin(math.sqrt(beta))
P = np.array([[1.0, 0.0], [0.0, 0.0]])          # rho* = |0><0| (posto 1)
Q0 = np.eye(2) - P
c, s = math.cos(theta), math.sin(theta)
R = np.array([[c, -s], [s, c]])
Qt = R @ Q0 @ R.T
anti0 = Q0 @ P + P @ Q0
antit = Qt @ P + P @ Qt
F1 = R @ P @ R.T                                 # F(1): o posto 1 transportado (Ad R)
DF1 = np.diag(np.diag(F1))                       # D_inf(F(1)): endpoint do dephasing (esperanca diagonal)
out = {
    "um_py_sha16": sha[:16],
    "ALPHA_FINE_CODATA_2018": {"valor": alpha, "linha": l_alpha},
    "SEALED_CODATA_ALPHA": {"valor": alpha_sel, "linha": l_sel, "igual_ao_anterior": alpha_sel == alpha},
    "beta_runtime": repr(beta), "beta_via_exp_meio": repr(beta_exp),
    "confere_texto_conferencia": repr(beta) == CONFERENCIA,
    "theta_M": theta,
    "IDENTIDADE_vazamento_Tr_rho_Qtheta": float(np.trace(P @ Qt)), "vazamento_menos_beta": float(np.trace(P @ Qt)) - beta,
    "anticomutador_theta0_norma": float(np.linalg.norm(anti0)),
    "anticomutador_thetaM_norma": float(np.linalg.norm(antit)),
    "anticomutador_thetaM_forma_fechada_sqrt_2beta_1mais_beta": math.sqrt(2 * beta * (1 + beta)),
    "traco_anticomutador_thetaM": float(np.trace(antit)), "dois_beta": 2 * beta,
    "F1_idempotente_residuo": float(np.linalg.norm(F1 @ F1 - F1)), "F1_traco": float(np.trace(F1)),
    "posto_F1": int(np.linalg.matrix_rank(F1)), "pureza_F1": float(np.trace(F1 @ F1)),
    "D_F1_diagonal": [float(DF1[0, 0]), float(DF1[1, 1])], "um_menos_beta": 1 - beta,
    "posto_D_F1": int(np.linalg.matrix_rank(DF1)), "traco_D_F1": float(np.trace(DF1)),
    "pureza_D_F1": float(np.trace(DF1 @ DF1)), "pureza_forma_fechada_1_menos_2beta_mais_2beta2": 1 - 2 * beta + 2 * beta * beta,
    "nota": "[DERIVED/REAL medido aqui] identidades algebricas de theta_M = arcsin sqrt(beta): nao discriminam beta; "
            "o vazamento = beta e a definicao de theta_M; o endpoint D(F(1)) = diag(1-beta, beta) ja e teorema "
            "(dephased_rhoOut_*, measurement_channel_endpoint) com theta generico.",
}
print(json.dumps(out, ensure_ascii=False, indent=1))
with open(os.path.join(AQUI, "CONFERENCIA_BETA.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
