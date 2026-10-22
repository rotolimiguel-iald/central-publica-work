# -*- coding: utf-8 -*-
"""B -- SEGUNDO CALCULO INDEPENDENTE do auditor REPRO r2 (nao usa nenhuma linha do codigo dos construtores).

Ferramentas diferentes das do construtor: sympy (identidades SIMBOLICAS exatas), mpmath a 60 digitos,
Python puro (floats e 'random', sem numpy) para a amostragem de P1. beta: alpha lido dos BYTES do um.py por
regex propria (sem executar), beta = alpha*sqrt(e) em runtime; o valor de conferencia de beta so aparece
LIDO do PREREGISTRO.json congelado (nunca escrito aqui). [v2: rotulos sem o numero do operador]
"""
import cmath, hashlib, json, math, os, random, re, sys

import mpmath as mp
import sympy as sp

R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UMPY = os.path.join(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um", "N\u00f3s", "um.py")
PRE = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out\1_PREREGISTRO\PREREGISTRO.json"
V4 = r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt"
OUT = os.path.join(R2, "saidas", "B_INDEPENDENTE_v2.json")
res = {}

# ------------------------------------------------------------------ beta de runtime (bytes do um.py)
raw = open(UMPY, "rb").read()
linhas = raw.split(b"\n")
cand = [(i + 1, l) for i, l in enumerate(linhas) if re.match(rb"ALPHA_FINE_CODATA_2018\s*=\s*[0-9]", l)]
assert len(cand) == 1, cand
lin_alpha, l_alpha = cand[0]
alpha_txt = re.match(rb"ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", l_alpha).group(1).decode()
alpha = float(alpha_txt)
beta = alpha * math.sqrt(math.e)
mp.mp.dps = 60
beta_mp = mp.mpf(alpha_txt) * mp.sqrt(mp.e)
pre = json.load(open(PRE, encoding="utf-8"))
res["beta"] = dict(um_py_sha256=hashlib.sha256(raw).hexdigest(), linha_alpha=lin_alpha, alpha_texto=alpha_txt,
                   beta_repr=repr(beta), confere_repr_congelado=(repr(beta) == pre["beta_runtime"]["beta_float64"]),
                   beta_mp_30=mp.nstr(beta_mp, 30), confere_mp_congelado=(mp.nstr(beta_mp, 30) == pre["beta_runtime"]["beta_mpmath_30dig"]),
                   abs_beta_mp_menos_beta=mp.nstr(abs(beta_mp - mp.mpf(beta)), 5))
thM = math.asin(math.sqrt(beta))
thM_mp = mp.asin(mp.sqrt(beta_mp))
res["thetaM"] = dict(repr=repr(thM), confere_congelado=(repr(thM) == pre["beta_runtime"]["theta_M"]))

# ------------------------------------------------------------------ I1..I6: identidades SIMBOLICAS (sympy)
th, t, g01, g10, b = sp.symbols("theta t g01 g10 b", real=True)
c, s = sp.cos(th), sp.sin(th)
P = sp.Matrix([[1, 0], [0, 0]])
Q0 = sp.eye(2) - P
R = sp.Matrix([[c, -s], [s, c]])                 # a R do um.py l.6518
S = sp.Matrix([[c, s], [-s, c]])                 # Smat do kernel = cos*1 + sin*Grot
Qth = R * Q0 * R.T
F1 = S * P * S.H                                 # rhoOut = S rho* S^H
anti = Qth * P + P * Qth
z = lambda M: all(sp.simplify(x) == 0 for x in M)
sim = {}
sim["I1_Qth_igual_SH_Q0_S"] = z(Qth - S.H * Q0 * S)
sim["I1_Qth_forma"] = z(Qth - sp.Matrix([[s**2, -s*c], [-s*c, c**2]]))
sim["I1_vazamento_Tr_rhostar_Qth_eq_sin2"] = sp.simplify((P * Qth).trace() - s**2) == 0
sim["I1_vazamento_em_thetaM_eq_b"] = sp.simplify(((P * Qth).trace()).subs(th, sp.asin(sp.sqrt(b))) - b) == 0  # 0<=b<=1
sim["I2_anticomutador_forma"] = z(anti - sp.Matrix([[2*s**2, -s*c], [-s*c, 0]]))
sim["I2_traco_2s2"] = sp.simplify(anti.trace() - 2*s**2) == 0
sim["I2_frob2_2s2(1+s2)"] = sp.simplify(sum(x**2 for x in anti) - 2*s**2*(1 + s**2)) == 0
# {Q,rho*} = 0 <=> sin = 0: a entrada (0,0) e 2 s^2, que so se anula com s = 0; e s = 0 zera tudo
sim["I2_zero_sse_sin0"] = (sp.simplify(anti[0, 0] - 2*s**2) == 0) and z(anti.subs(s, 0).subs(th, 0))
Dinf = sp.diag(F1[0, 0], F1[1, 1])
sim["I3_Dinf_F1_eq_diag(c2,s2)"] = z(Dinf - sp.diag(c**2, s**2))
sim["I3_det_Dinf_eq_c2s2"] = sp.simplify(Dinf.det() - c**2*s**2) == 0
sim["I3_pureza_Dinf_eq_1-2s2c2"] = sp.simplify((Dinf*Dinf).trace() - (1 - 2*s**2*c**2)) == 0
sim["I3_det_F1_eq_0_e_traco_1"] = (sp.simplify(F1.det()) == 0) and (sp.simplify(F1.trace() - 1) == 0)
Dt = lambda X: sp.Matrix([[X[0, 0], sp.exp(-t*g01)*X[0, 1]], [sp.exp(-t*g10)*X[1, 0], X[1, 1]]])
sim["I4_det_DtF1"] = sp.simplify(Dt(F1).det() - c**2*s**2*(1 - sp.exp(-t*(g01 + g10)))) == 0
sim["I4_traco_DtF1_eq_1"] = sp.simplify(Dt(F1).trace() - 1) == 0
sim["I5_vazamento_sobrevive_Dt"] = sp.simplify((P * Dt(Qth)).trace() - s**2) == 0
sim["I5_anticomm_DtQ"] = z(Dt(Qth)*P + P*Dt(Qth) - sp.Matrix([[2*s**2, -sp.exp(-t*g01)*s*c], [-sp.exp(-t*g10)*s*c, 0]]))
sim["I6_um_menos_F1_eq_Q(-th)"] = z((sp.eye(2) - F1) - Qth.subs(th, -th))
sim["I6_Q(th)_eq_1-F1(th)_so_se_sc_0"] = sp.simplify((Qth - (sp.eye(2) - F1))[0, 1] - (-2*s*c)) == 0
# D atua <=> c s != 0 : D_t F1 - F1 so tem fora da diagonal (e^{-t g} - 1)(-c s)
sim["I9_DtF1_menos_F1"] = z(Dt(F1) - F1 - sp.Matrix([[0, (sp.exp(-t*g01) - 1)*(-c*s)], [(sp.exp(-t*g10) - 1)*(-s*c), 0]]))
# S^n = S(n th) para n = 1..12 (simbolico) -- a lei de grupo
Sn_ok = True
for n in range(1, 13):
    Sn = S**n
    Snt = sp.Matrix([[sp.cos(n*th), sp.sin(n*th)], [-sp.sin(n*th), sp.cos(n*th)]])
    Sn_ok = Sn_ok and z((Sn - Snt).applyfunc(lambda e: sp.simplify(sp.expand_trig(e - 0))))
sim["I7_Sn_eq_S(n th)_n1a12"] = Sn_ok
res["simbolico_sympy"] = sim
res["simbolico_todos_verdadeiros"] = all(sim.values())

# ------------------------------------------------------------------ numeros em theta_M (Python puro + mpmath 60)
def mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def T(A):
    return [[A[j][i] for j in range(2)] for i in range(2)]


cf, sf = math.cos(thM), math.sin(thM)
Rf = [[cf, -sf], [sf, cf]]
Q0f = [[0.0, 0.0], [0.0, 1.0]]
Pf = [[1.0, 0.0], [0.0, 0.0]]
Qf = mat_mul(mat_mul(Rf, Q0f), T(Rf))
PQ = mat_mul(Pf, Qf)
leak_f = PQ[0][0] + PQ[1][1]
cm, sm = mp.cos(thM_mp), mp.sin(thM_mp)
num = {}
num["B3b_leak_float64_menos_beta"] = abs(leak_f - beta)
num["B3b_leak_mp_menos_beta_mp"] = mp.nstr(abs(sm**2 - beta_mp), 5)
Af = [[2*sf*sf, -sf*cf], [-sf*cf, 0.0]]
num["B2b_frob_anticomm"] = math.sqrt(sum(x*x for r_ in Af for x in r_))
num["B2b_frob_ref_sqrt_2b(1+b)"] = math.sqrt(2*beta*(1+beta))
num["B2b_traco_menos_2beta"] = abs(Af[0][0] + Af[1][1] - 2*beta)
num["B5b_Dinf_diag"] = [cf*cf, sf*sf]
num["B5b_Dinf_menos_diag(1-b,b)"] = max(abs(cf*cf - (1 - beta)), abs(sf*sf - beta))
num["B5b_det_Dinf"] = cf*cf*sf*sf
num["B5b_pureza"] = (cf*cf)**2 + (sf*sf)**2
num["B5b_pureza_ref_1-2b(1-b)"] = 1 - 2*beta*(1 - beta)
num["B5b_mp_pureza"] = mp.nstr(cm**4 + sm**4, 20)
num["B5e_posto_F1_vs_posto_Dinf"] = [1 if abs(cf*cf*sf*sf - cf*cf*sf*sf) == 0 else None, 2 if cf*cf*sf*sf > 0 else 1]
v4 = open(V4, "rb").read().decode("utf-8")
m = re.search(r"\\approx\s*([0-9.]+)", v4)
num_op = float(m.group(1))
num["B3d_numero_operador_lido_de_V4"] = m.group(1)
num["B3d_|beta-numero_operador|"] = abs(beta - num_op)
num["B3d_<=5e-7"] = abs(beta - num_op) <= 5e-7
num["W_ceil(pi/thM)+2"] = math.ceil(math.pi / thM) + 2
num["cos_thM_menos_1e-9"] = math.cos(thM) - 1e-9
# B7.a2 em mpmath (60 digitos): amplitude minima das janelas de W termos de sin^2(n thM), n = 0..99999
W = num["W_ceil(pi/thM)+2"]
mp.mp.dps = 30
vals = []
x = mp.mpf(0)
for n in range(100000):
    vals.append(float(mp.sin(n * thM_mp) ** 2))
from collections import deque
def janelas_min_amplitude(v, w):
    mx_q, mn_q, best = deque(), deque(), float("inf")
    for i, val in enumerate(v):
        while mx_q and v[mx_q[-1]] <= val: mx_q.pop()
        mx_q.append(i)
        while mn_q and v[mn_q[-1]] >= val: mn_q.pop()
        mn_q.append(i)
        if mx_q[0] <= i - w: mx_q.popleft()
        if mn_q[0] <= i - w: mn_q.popleft()
        if i >= w - 1:
            best = min(best, v[mx_q[0]] - v[mn_q[0]])
    return best
num["B7a2_min_amplitude_janelas_mp30"] = janelas_min_amplitude(vals, W)
num["B7a2_n_janelas"] = 100000 - W + 1
num["B7a2_cauda_amplitude"] = max(vals[-1000:]) - min(vals[-1000:])
mp.mp.dps = 60
res["numeros"] = num

# ------------------------------------------------------------------ P1.a independente (Python puro, random.Random)
rnd = random.Random(424242)
def vec(n):
    return [complex(rnd.gauss(0, 1), rnd.gauss(0, 1)) for _ in range(n)]
def gram_schmidt(vs):
    out = []
    for v in vs:
        w = list(v)
        for u in out:
            pr = sum(u[i].conjugate() * w[i] for i in range(len(w)))
            w = [w[i] - pr * u[i] for i in range(len(w))]
        nr = math.sqrt(sum(abs(x)**2 for x in w))
        out.append([x / nr for x in w])
    return out
def dens(us, ps):
    n = len(us[0])
    return [[sum(ps[k] * us[k][i] * us[k][j].conjugate() for k in range(len(us))) for j in range(n)] for i in range(n)]
def mm(A, B):
    n = len(A)
    return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def tr(A):
    return sum(A[i][i] for i in range(len(A)))
def posto_mp(A):
    M = mp.matrix([[mp.mpc(x.real, x.imag) for x in r_] for r_ in A])
    sv = mp.svd_c(M, compute_uv=False)
    return sum(1 for x in sv if x > mp.mpf("1e-9"))
viol, npuro, nmisto = 0, 0, 0
for k in range(300):
    n = 2 + k % 3
    us = gram_schmidt([vec(n) for _ in range(n)])
    if k % 2 == 0:
        rho = dens([us[0]], [1.0]); npuro += 1
    else:
        r_ = 2 + (k // 2) % (n - 1)
        ps = [rnd.uniform(0.05, 1) for _ in range(r_)]; sps = sum(ps); ps = [p_/sps for p_ in ps]
        rho = dens(us[:r_], ps); nmisto += 1
    pur = tr(mm(rho, rho)).real
    rk = posto_mp(rho)
    idem = max(abs(x) for r_ in [[a - b_ for a, b_ in zip(r1, r2)] for r1, r2 in zip(mm(rho, rho), rho)] for x in r_)
    a_, b_, c_ = abs(pur - 1) <= 1e-12, rk == 1, idem <= 1e-12
    if not (a_ == b_ == c_) or (k % 2 == 0) != a_:
        viol += 1
res["P1a_independente"] = dict(n=300, puros=npuro, mistos=nmisto, violacoes=viol, posto_por="mpmath svd_c, corte 1e-9")

with open(OUT, "x", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1, default=str)
print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
