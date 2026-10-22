"""Conferência numérica INDEPENDENTE (Python/numpy, sem Lean) das afirmações matemáticas da pedra TestemunhaEstatica.

Não prova nada: confere, em ponto flutuante, que as definições do fonte descrevem o objeto que a docstring diz (a base de Bell, o projetor, o
traço parcial, o fluxo, a compressão do canto). Os parâmetros de teste (b_test, g_test) são sorteados por semente fixa: NÃO são o acoplamento
da teoria (que nunca entra literal).
Uso: python -I -X utf8 check_numeric.py
"""
import json
import math

import numpy as np

W = r"C:\IALD\Central de Patentes\work\testemunha_estatica_v396"
rng = np.random.default_rng(220126)
b_test = float(rng.uniform(0.2, 1.1))
g_test = float(rng.uniform(0.5, 2.0))

checks = []


def chk(nome, residuo, tol=1e-12):
    ok = bool(abs(residuo) <= tol)
    checks.append({"nome": nome, "residuo": float(abs(residuo)), "ok": ok})
    return ok


# índice (a,c) -> 2a + c   (Fin 2 × Fin 2 achatado em ordem lexicográfica: 00,01,10,11)
def ix(a, c):
    return 2 * a + c


def bsign(i):
    v = np.zeros(4)
    for a in range(2):
        for c in range(2):
            p1, p2 = a, c
            if i == 0:
                val = 1.0 if p1 == p2 else 0.0
            elif i == 1:
                val = (1.0 if p1 == 0 else -1.0) if p1 == p2 else 0.0
            elif i == 2:
                val = 0.0 if p1 == p2 else 1.0
            else:
                val = 0.0 if p1 == p2 else (1.0 if p1 == 0 else -1.0)
            v[ix(a, c)] = val
    return v


B = np.stack([bsign(i) for i in range(4)], axis=1)  # colunas = b_i
U = B / math.sqrt(2.0)  # colunas = u_i (ortonormais)

# 1. bsign_gram: <b_i,b_j> = 2 delta
chk("bsign_gram  B^T B - 2 I", np.abs(B.T @ B - 2 * np.eye(4)).max())
# 2. bsign_complete: sum_i b_i(p) b_i(q) = 2 delta
chk("bsign_complete  B B^T - 2 I", np.abs(B @ B.T - 2 * np.eye(4)).max())
# 3. bellUnit ortonormal e completa
chk("bellUnit_orthonormal  U^T U - I", np.abs(U.T @ U - np.eye(4)).max())
chk("bellUnit_complete  U U^T - I", np.abs(U @ U.T - np.eye(4)).max())
# 4. o 1º vetor é (e00+e11)/sqrt2
bell = np.array([1, 0, 0, 1]) / math.sqrt(2.0)
chk("bellUnit_zero  u0 - (e00+e11)/sqrt2", np.abs(U[:, 0] - bell).max())

# 5. projetor de Bell (entradas 1/2 em (00|11, 00|11))
P = np.zeros((4, 4))
for p in (0, 3):
    for q in (0, 3):
        P[p, q] = 0.5
chk("projetor  P - |Phi+><Phi+|", np.abs(P - np.outer(bell, bell)).max())
chk("bell_idem  P P - P", np.abs(P @ P - P).max())
chk("bell_trace_one  tr P - 1", np.trace(P) - 1.0)
chk("P auto-adjunto", np.abs(P - P.T).max())

# 6. traço parcial (ptr = soma sobre o 2º fator) e o outro sítio
def ptr_second(X):
    out = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            out[i, j] = sum(X[ix(i, k), ix(j, k)] for k in range(2))
    return out


def ptr_first(X):
    out = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            out[i, j] = sum(X[ix(k, i), ix(k, j)] for k in range(2))
    return out


R2, R1 = ptr_second(P), ptr_first(P)
chk("bell_reduced_half (2º sítio)  ptr P - I/2", np.abs(R2 - 0.5 * np.eye(2)).max())
chk("o outro sítio  ptr1 P - I/2", np.abs(R1 - 0.5 * np.eye(2)).max())
chk("indivíduo NÃO ecoa  ||R R - R|| = 1/4 (distância ao eco)", np.abs(R2 @ R2 - R2).max() - 0.25)
chk("tr(R R) = 1/2", np.trace(R2 @ R2) - 0.5)
chk("bell_cci_half  1 - tr(R R) - 1/2", 1 - np.trace(R2 @ R2) - 0.5)
chk("par puro  tr(P P) - 1", np.trace(P @ P) - 1.0)

# 7. o dente: o produto não ligado reduz a projetor puro (ecoa), CCI = 0
e00 = np.zeros(4)
e00[0] = 1.0
Pp = np.outer(e00, e00)
Rp = ptr_second(Pp)
chk("produto: R = e00 e idempotente", np.abs(Rp @ Rp - Rp).max())
chk("produto: CCI = 1 - tr(R R) = 0", 1 - np.trace(Rp @ Rp))

# 8. o fluxo: F_t = U diag(exp(-t b d)) U^T, d = (0, g, g, g)
d = np.array([0.0, g_test, g_test, g_test])
res_closed = 0.0
res_eig = 0.0
res_static = 0.0
for t in np.linspace(0.0, 3.0, 13):
    e = math.exp(-t * b_test * g_test)
    F = U @ np.diag(np.exp(-t * b_test * d)) @ U.T
    res_closed = max(res_closed, np.abs(F - (P + e * (np.eye(4) - P))).max())
    for i in range(4):
        res_eig = max(res_eig, np.abs(F @ U[:, i] - math.exp(-t * b_test * d[i]) * U[:, i]).max())
    # vetor aleatório: fixado em todo t sse está na reta; testa o vetor de Bell e um vetor fora
    res_static = max(res_static, np.abs(F @ B[:, 0] - B[:, 0]).max())
chk("psionFlow_eq  F_t - (P + e^{-t b g}(1-P))", res_closed)
chk("bellUnit_eigen  F_t u_i - e^{-t b d_i} u_i", res_eig)
chk("reta habitada  F_t Phi+ - Phi+", res_static)
fora = max(np.abs(U @ np.diag(np.exp(-1.0 * b_test * d)) @ U.T @ B[:, k] - B[:, k]).max() for k in (1, 2, 3))
checks.append({"nome": "testemunha global falsa  max_k ||F_1 b_k - b_k|| (k=1..3) > 0", "valor": float(fora), "ok": bool(fora > 0.1)})
# conjunto estático = reta: fixados por F_1 formam o núcleo de (F_1 - I)
F1 = U @ np.diag(np.exp(-1.0 * b_test * d)) @ U.T
sv = np.linalg.svd(F1 - np.eye(4), compute_uv=False)
checks.append({"nome": "dimensão do conjunto fixo = 1 (valores singulares de F_1 - I)", "valores_singulares": [float(s) for s in sv],
               "ok": bool(sum(1 for s in sv if s < 1e-12) == 1)})
# P x = ((x00 + x11)/2) b0  (bellProjectorR_mulVec)
x = rng.normal(size=4)
chk("bellProjectorR_mulVec  P x - ((x00+x11)/2) b0", np.abs(P @ x - ((x[0] + x[3]) / 2) * B[:, 0]).max())
# coordenadas de Bell: y_i = <b_i,x>/2 ; síntese: x = sum y_i b_i
y = (B.T @ x) / 2
chk("synth_coord  sum_i y_i b_i - x", np.abs(B @ y - x).max())
chk("coord_synth  <b_i, B y>/2 - y", np.abs((B.T @ (B @ y)) / 2 - y).max())

# 9. o limite: F_t x -> P x
Fbig = U @ np.diag(np.exp(-60.0 * b_test * d)) @ U.T
chk("the_flow_delivers_to_the_psion  F_60 x - P x", np.abs(Fbig @ x - P @ x).max(), 1e-9)

# 10. a compressão do canto: P Y P = tr(P Y) P  (para Y complexa aleatória), idempotente, conserva tr(P Y)
Y = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
C = P @ Y @ P
chk("scalarises  P Y P - tr(P Y) P", np.abs(C - np.trace(P @ Y) * P).max())
chk("stable  P(PYP)P - PYP", np.abs(P @ C @ P - C).max())
chk("preserves  tr(P (PYP)) - tr(P Y)", abs(np.trace(P @ C) - np.trace(P @ Y)))
chk("step(P) = P  (P P P - P)", np.abs(P @ P @ P - P).max())
# não tem inversa à esquerda: o passo não é injetivo (duas matrizes distintas com a mesma compressão)
Y2 = Y + (np.eye(4) - P) @ rng.normal(size=(4, 4)) @ (np.eye(4) - P)
chk("colapso não injetivo  P Y2 P - P Y P (Y2 != Y)", np.abs(P @ Y2 @ P - C).max())
checks.append({"nome": "Y2 != Y (a perda é real)", "valor": float(np.abs(Y2 - Y).max()), "ok": bool(np.abs(Y2 - Y).max() > 0.1)})

# 11. sqrt2: (1/sqrt2)^2 = 1/2
chk("inv_sqrt_two_sq", (1 / math.sqrt(2.0)) ** 2 - 0.5)

ok_all = all(c["ok"] for c in checks)
out = {
    "o_que_e": "conferência numérica independente (numpy) das definições e identidades da pedra TestemunhaEstatica; NÃO é prova",
    "parametros_de_teste_sorteados_por_semente(nao_sao_o_acoplamento_da_teoria)": {"semente": 220126, "b_test": b_test, "g_test": g_test},
    "n_checagens": len(checks),
    "todas_ok": ok_all,
    "checagens": checks,
}
json.dump(out, open(W + r"\conferencia_numerica.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print("checagens:", len(checks), "| todas ok:", ok_all)
for c in checks:
    if not c["ok"]:
        print("FALHA:", c)
