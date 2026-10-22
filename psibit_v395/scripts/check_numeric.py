"""Conferência NUMÉRICA independente (Python puro) dos enunciados da pedra Psibit.

NÃO é prova (a prova é o termo Lean); é o controle: o número deve concordar com a frase.
Replica, com `math` apenas, as definições do Psibit.lean:
  v(th) = (cos th, -sin th);  codeAmp = (v0^2, sign v0, sign v1);  decodeAmp (w,a,b) = (a*sqrt w, b*sqrt(1-w))
  rhoOut(th) = S E00 S^T com S = [[c, s], [-s, c]] (SMatrix.lean Smat_eq) -> [[c^2, -cs], [-cs, s^2]]
  rhoWeight = v0^2; rhoParity = sign(v0*v1); decodeRho(w,p) = [[w, p*sqrt(w(1-w))],[p*sqrt(w(1-w)), 1-w]]
  diagExpect(rho) = diag(rho)
Saída: JSON em stdout.
"""
import json
import math


def sgn(x):
    return (x > 0) - (x < 0)


def v(th):
    return (math.cos(th), -math.sin(th))


def code_amp(th):
    a, b = v(th)
    return (a * a, sgn(a), sgn(b))


def decode_amp(c):
    w, a, b = c
    return (a * math.sqrt(w), b * math.sqrt(max(0.0, 1.0 - w)))


def rho_out(th):
    c, s = math.cos(th), math.sin(th)
    S = [[c, s], [-s, c]]
    E = [[1.0, 0.0], [0.0, 0.0]]
    # S E S^T
    SE = [[sum(S[i][k] * E[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    return [[sum(SE[i][k] * S[j][k] for k in range(2)) for j in range(2)] for i in range(2)]


def decode_rho(w, p):
    m = p * math.sqrt(max(0.0, w * (1.0 - w)))
    return [[w, m], [m, 1.0 - w]]


def sign_pat(x):
    return 1.0 if x >= 0 else -1.0


def bin_entropy(p):
    return sum(-q * math.log(q) for q in (p, 1 - p) if q > 0)


N = 200000
two_pi = 2 * math.pi
err_amp = 0.0
err_pat = 0.0
err_rho = 0.0
err_rho_matrix_vs_closed = 0.0
states = set()
min_gap_generic = 1e9
collapse_equal_max_diff = 0.0
parity_flip_ok = True
parity_vs_fd_ok = True
generic_count = 0
for k in range(N):
    th = two_pi * k / N
    a, b = v(th)
    c = code_amp(th)
    d = decode_amp(c)
    err_amp = max(err_amp, abs(d[0] - a), abs(d[1] - b))
    # convenção das patentes
    w = a * a
    dp = (sign_pat(a) * math.sqrt(w), sign_pat(b) * math.sqrt(max(0.0, 1 - w)))
    err_pat = max(err_pat, abs(dp[0] - a), abs(dp[1] - b))
    # densidade
    rho = rho_out(th)
    cs = math.cos(th) * math.sin(th)
    closed = [[math.cos(th) ** 2, -cs], [-cs, math.sin(th) ** 2]]
    err_rho_matrix_vs_closed = max(err_rho_matrix_vs_closed,
                                   max(abs(rho[i][j] - closed[i][j]) for i in range(2) for j in range(2)))
    par = sgn(a * b)
    rd = decode_rho(a * a, par)
    err_rho = max(err_rho, max(abs(rho[i][j] - rd[i][j]) for i in range(2) for j in range(2)))
    if abs(a) > 1e-9 and abs(b) > 1e-9:
        states.add((sgn(a), sgn(b)))
    # colapso: diag igual em th e -th; densidade difere por 2|cs| fora dos eixos
    rn = rho_out(-th)
    collapse_equal_max_diff = max(collapse_equal_max_diff, abs(rho[0][0] - rn[0][0]), abs(rho[1][1] - rn[1][1]))
    if abs(math.sin(2 * th)) > 1e-6:
        generic_count += 1
        min_gap_generic = min(min_gap_generic, abs(rho[0][1] - rn[0][1]) / abs(math.sin(2 * th)))
        # paridade inverte sob th -> -th
        if sgn(-a * 0 + (a * b)) != -sgn(math.cos(-th) * (-math.sin(-th))):
            parity_flip_ok = False
        # sinal da derivada do Nome (diferença finita central) = paridade
        h = 1e-6
        fd = (math.cos(th + h) ** 2 - math.cos(th - h) ** 2) / (2 * h)
        if abs(fd) > 1e-4 and sgn(fd) != par:
            parity_vs_fd_ok = False

# Verbo = derivada do Nome: rho01 = 1/2 d(cos^2)/dth (diferença finita central)
err_verbo = 0.0
for k in range(0, 1000):
    th = two_pi * k / 1000 + 0.123
    h = 1e-6
    fd = (math.cos(th + h) ** 2 - math.cos(th - h) ** 2) / (2 * h)
    err_verbo = max(err_verbo, abs(rho_out(th)[0][1] - 0.5 * fd))

# pureza rho01^2 = rho00 rho11
err_pureza = max(abs(rho_out(two_pi * k / 1000)[0][1] ** 2 - rho_out(two_pi * k / 1000)[0][0] * rho_out(two_pi * k / 1000)[1][1])
                 for k in range(1000))

# sinal global: v(th+pi) = -v(th); rho igual
err_global = 0.0
for k in range(1000):
    th = two_pi * k / 1000
    va, vb = v(th), v(th + math.pi)
    err_global = max(err_global, abs(va[0] + vb[0]), abs(va[1] + vb[1]))
    r1, r2 = rho_out(th), rho_out(th + math.pi)
    err_global = max(err_global, max(abs(r1[i][j] - r2[i][j]) for i in range(2) for j in range(2)))

# ponto fixo pi/4
th = math.pi / 4
fixed = rho_out(th)
diag_fixed = [fixed[0][0], fixed[1][1]]
H = bin_entropy(math.cos(th) ** 2)
out = {
    "N_angulos": N,
    "erro_max_decodeAmp_codeAmp": err_amp,
    "erro_max_convencao_patente_zero_vai_a_mais1": err_pat,
    "erro_max_decodeRho_vs_rhoOut": err_rho,
    "erro_max_rhoOut_matriz_vs_forma_fechada": err_rho_matrix_vs_closed,
    "estados_genericos_visitados(sign v0, sign v1)": sorted([list(s) for s in states]),
    "n_estados_genericos": len(states),
    "colapso_igual_em_theta_e_menos_theta_max_diff_diagonal": collapse_equal_max_diff,
    "pontos_genericos(sin2th!=0)": generic_count,
    "razao_min_|rho01(th)-rho01(-th)|/|sin 2th|_(esperado_1)": min_gap_generic,
    "paridade_inverte_sob_th_para_-th": parity_flip_ok,
    "paridade_igual_ao_sinal_da_derivada_do_Nome_(dif_finita)": parity_vs_fd_ok,
    "erro_max_Verbo_menos_meia_derivada_do_Nome_(dif_finita)": err_verbo,
    "erro_max_pureza_rho01^2-rho00*rho11": err_pureza,
    "erro_max_sinal_global_(v(th+pi)=-v e rho igual)": err_global,
    "ponto_fixo_pi/4_diag_do_colapso": diag_fixed,
    "entropia_Shannon_nats_no_ponto_fixo": H,
    "ln2": math.log(2),
    "|H-ln2|": abs(H - math.log(2)),
    "maximo_da_entropia_binaria_na_grade_(<=ln2)": max(bin_entropy(math.cos(two_pi * k / 20000) ** 2) for k in range(20000)),
    "nota": "controle numérico em ponto flutuante (IEEE-754); não substitui o termo Lean.",
}
print(json.dumps(out, ensure_ascii=False, indent=1))
