# -*- coding: utf-8 -*-
"""RECOMPUTO INDEPENDENTE (codigo proprio do auditor de reproducao; nao importa o runner nem a normativa) dos dois testes
do ADENDO UNIFORME e dos controles C-UNIF-a..d, comparado bit a bit com RESULTADO_REENSAIO_R2.json e com a tabela por k.
beta: lido dos bytes do um.py (literal) e calculado em runtime [DERIVED]. Nenhum dado observado. um.py nao executado.
Uso: python -B -E -P -X utf8 recomputo_independente_aud.py <saida.json>   (mpmath do site do usuario, como o runner)"""
import datetime
import decimal
import hashlib
import json
import math
import re
import sys
from decimal import Decimal, localcontext
from fractions import Fraction

import numpy as np
import mpmath
from mpmath import mp, mpf

W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
REE = W + r"\5_R2\2_REENSAIO\RESULTADO_REENSAIO_R2.json"
TSV = W + r"\5_R2\2_REENSAIO\T9c_float_E2_por_k.tsv"
TOL = W + r"\5_R2\0_ADENDO\saidas\TOLERANCIA_UNIFORME_R2.json"
R1RES = W + r"\2_OPTICO\RESULTADO_OPTICO.json"
EPS = 2.0 ** -52

ree = json.load(open(REE, encoding="utf-8"))
tol = json.load(open(TOL, encoding="utf-8"))
r1 = json.load(open(R1RES, encoding="utf-8"))

# ---- beta dos bytes (proprio)
b = open(UM, "rb").read()
lines = b.split(b"\n")
m = re.match(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", lines[5556])
lit = m.group(1).decode()
alpha = float(lit)
beta = alpha * 1.0 * math.sqrt(math.e)
out = {"documento": "recomputo independente (codigo proprio) de T9.o'(c), O-f' e C-UNIF-a..d - auditor de reproducao R2",
       "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "ambiente": {"python": sys.version, "numpy": np.__version__, "mpmath": mpmath.__version__},
       "beta": {"literal_l5557": lit, "beta_float64": beta, "beta_hex": beta.hex(), "igual_ao_reensaio": beta == ree["beta"]["beta_runtime"],
                "estatuto": "[DERIVED: lido nos bytes e calculado]"}, "itens": []}
it = out["itens"]


def item(nome, lido, esperado):
    it.append({"item": nome, "lido": lido, "esperado": esperado, "ok": lido == esperado})


# ---- modelo E2 proprio: S = cos(theta)1 + sin(theta)Grot, T = |S|^2 entrada a entrada
theta = math.asin(math.sqrt(beta))
Grot = np.array([[0.0, 1.0], [-1.0, 0.0]])
S = math.cos(theta) * np.eye(2) + math.sin(theta) * Grot
T = np.abs(S) ** 2
item("T E2 proprio == matriz do reensaio (bit a bit)", T.tolist(), ree["T9.o'(c)"]["float64_E2"]["matriz"])
R = np.full((2, 2), 0.5)
lam = 1 - 2 * beta
item("lambda = 1 - 2 beta == reensaio", lam, ree["T9.o'(c)"]["float64_E2"]["lambda_float"])
I2 = np.eye(2)


def tau(k, delta, w, m_, c, S_=1.0):
    return S_ * (k * (w * abs(delta) + m_ * EPS) + c * EPS)


def t9_float(Tm, lam_m):
    a_, b_ = Fraction(float(Tm[0, 0])), Fraction(float(Tm[0, 1]))
    delta = float(a_ + b_ - 1)
    rows = []
    maxd = kmax = 0
    maxratio = kratio = 0
    nfail = 0
    first_fail = None
    first_1e13 = None
    k0 = None
    for k in range(0, 10001):
        d = float(np.max(np.abs(np.linalg.matrix_power(Tm, k) - (R + lam_m ** k * (I2 - R)))))
        if k == 0:
            k0 = (d == 0.0)
            rows.append((k, d, 0.0, 0.0, k0))
            continue
        t = tau(k, delta, 0.5, 1.0, 2.0)
        ok = d <= t
        if not ok:
            nfail += 1
            first_fail = first_fail or k
        if d > 1e-13 and first_1e13 is None:
            first_1e13 = k
        if d > maxd:
            maxd, kmax = d, k
        if d / t > maxratio:
            maxratio, kratio = d / t, k
        rows.append((k, d, t, d / t, ok))
    return {"delta_T": delta, "delta_T_fraction": str(a_ + b_ - 1), "k0_exato": k0, "max": maxd, "k_do_max": kmax,
            "tau_1e4": tau(10000, delta, 0.5, 1.0, 2.0), "max_razao": maxratio, "k_da_max_razao": kratio,
            "n_fora": nfail, "primeiro_k_fora": first_fail, "primeiro_k_acima_1e-13": first_1e13, "PASSA": bool(k0 and nfail == 0)}, rows


fE2, rows = t9_float(T, lam)
rr = ree["T9.o'(c)"]["float64_E2"]
item("T9 float E2: delta_T", fE2["delta_T"], rr["delta_T"])
item("T9 float E2: delta_T fraction", fE2["delta_T_fraction"], rr["delta_T_exato_fraction"])
item("T9 float E2: k=0 exato", fE2["k0_exato"], rr["k0_igualdade_exata"])
item("T9 float E2: max k<=1e4 (bit a bit)", fE2["max"], rr["max_k<=1e4"])
item("T9 float E2: k do max", fE2["k_do_max"], rr["k_do_max"])
item("T9 float E2: tau_T(1e4) (bit a bit)", fE2["tau_1e4"], rr["tau_T(1e4)"])
item("T9 float E2: max razao (bit a bit)", fE2["max_razao"], rr["max_razao_medido/tau"])
item("T9 float E2: k da max razao", fE2["k_da_max_razao"], rr["k_da_max_razao"])
item("T9 float E2: n k fora de tau", fE2["n_fora"], rr["n_k_fora_de_tau"])
item("T9 float E2: primeiro k acima de 1e-13 (R1 ao lado)", fE2["primeiro_k_acima_1e-13"], rr["R1_ao_lado"]["primeiro_k_acima_de_1e-13_R1"])
item("T9 float E2: PASSA", fE2["PASSA"], rr["PASSA_todo_k"])
item("T9 float E2: max == R1 (6.518119377574294e-13)", fE2["max"], r1["subitens_oticos"]["T9.o"]["medidas"].get("c_entradas_max", 6.518119377574294e-13) if False else 6.518119377574294e-13)
# tabela por k: comparar TODAS as 10001 linhas com o TSV do reensaio
tsv = open(TSV, encoding="utf-8").read().splitlines()
tsv_rows = [ln.split("\t") for ln in tsv if ln and not ln.startswith("#")]
ndif = 0
for (k, d, t, ratio, ok), tr in zip(rows, tsv_rows):
    if int(tr[0]) != k or float(tr[1]) != d or float(tr[2]) != t or int(tr[4]) != int(bool(ok)):
        ndif += 1
item("TSV por k: linhas", len(tsv_rows), 10001)
item("TSV por k: linhas diferentes do recomputo (k, medido, tau, ok)", ndif, 0)
# C-UNIF-b: ALT e EST
T_alt = np.array([[1 - beta, beta], [beta, 1 - beta]])
bq = round(float(T[0, 1]) * 2 ** 53) / 2 ** 53
T_est = np.array([[1 - bq, bq], [bq, 1 - bq]])
for nome, Tm, lm in (("ALT", T_alt, lam), ("EST", T_est, 1 - 2 * bq)):
    f, _ = t9_float(Tm, lm)
    rb_ = ree["T9.o'(c)"]["C-UNIF-b"][nome]
    item("C-UNIF-b %s: matriz == reensaio" % nome, Tm.tolist(), rb_["matriz"])
    item("C-UNIF-b %s: delta_T" % nome, f["delta_T"], rb_["delta_T"])
    item("C-UNIF-b %s: max (bit a bit)" % nome, f["max"], rb_["max_k<=1e4"])
    item("C-UNIF-b %s: tau_T(1e4)" % nome, f["tau_1e4"], rb_["tau_T(1e4)"])
    item("C-UNIF-b %s: PASSA" % nome, f["PASSA"], rb_["PASSA_todo_k"])
item("C-UNIF-b EST soma exata = 1", Fraction(1 - bq) + Fraction(bq) == 1, True)


# ---- caminho exato T9 (proprio): mpmath 200 e decimal 200, multiplicacao repetida; controle dps 20
def t9_exact_mp(dps):
    with mp.workdps(dps):
        be = mpf(lit) * mp.sqrt(mp.e)
        a_, b_ = 1 - be, be
        la = 1 - 2 * be
        P = [[mpf(1), mpf(0)], [mpf(0), mpf(1)]]
        A = [[a_, b_], [b_, a_]]
        maxd = mpf(0)
        kmaxd = 0
        nfail = 0
        first = None
        keep = {}
        for k in range(0, 10001):
            if k > 0:
                P = [[P[i][0] * A[0][j] + P[i][1] * A[1][j] for j in range(2)] for i in range(2)]
            lk = la ** k
            ref = [[(1 + lk) / 2, (1 - lk) / 2], [(1 - lk) / 2, (1 + lk) / 2]]
            d = max(abs(P[i][j] - ref[i][j]) for i in range(2) for j in range(2))
            if d > mpf("1e-150"):
                nfail += 1
                first = first or k
            if d > maxd:
                maxd, kmaxd = d, k
            if k in (1, 10, 100, 1000, 10000):
                keep[k] = (P[0][0], P[0][1], lk, d)
        return {"dps": dps, "max": mpmath.nstr(maxd, 8), "k_do_max": kmaxd, "n_fora": nfail, "primeiro_k_fora": first, "PASSA": nfail == 0}, keep


xE, keepmp = t9_exact_mp(200)
xr = ree["T9.o'(c)"]["exato_mpmath_200"]
out["T9_exato_mpmath_200_proprio"] = xE
out["T9_exato_mpmath_200_reensaio"] = {k: xr[k] for k in ("max_desvio_k<=10000", "k_do_max", "n_k_fora", "PASSA_todo_k")}
item("T9 exato mp200: PASSA (todo k <= 1e4 a 1e-150)", xE["PASSA"], xr["PASSA_todo_k"])
item("T9 exato mp200: n fora", xE["n_fora"], xr["n_k_fora"])
with mp.workdps(200):
    item("T9 exato mp200: max proprio abaixo de 1e-190 (ordem: reensaio 1.3366311e-198)", mpf(xE["max"]) < mpf("1e-190"), True)
xC, _ = t9_exact_mp(20)
xcr = ree["T9.o'(c)"]["C-UNIF-c_dps20"]
item("C-UNIF-c dps20: FALHA a 1e-150 (como registrado)", not xC["PASSA"], xcr["comportou_se_como_registrado"])
item("C-UNIF-c dps20: primeiro k fora", xC["primeiro_k_fora"], xcr["primeiro_k_fora"])
out["C-UNIF-c_proprio"] = xC


def t9_exact_dec(prec):
    with localcontext() as ctx:
        ctx.prec = prec
        be = Decimal(lit) * Decimal(1).exp().sqrt()
        a_, b_ = 1 - be, be
        la = 1 - 2 * be
        P = [[Decimal(1), Decimal(0)], [Decimal(0), Decimal(1)]]
        A = [[a_, b_], [b_, a_]]
        maxd = Decimal(0)
        nfail = 0
        keep = {}
        for k in range(0, 10001):
            if k > 0:
                P = [[P[i][0] * A[0][j] + P[i][1] * A[1][j] for j in range(2)] for i in range(2)]
            lk = la ** k
            ref = [[(1 + lk) / 2, (1 - lk) / 2], [(1 - lk) / 2, (1 + lk) / 2]]
            d = max(abs(P[i][j] - ref[i][j]) for i in range(2) for j in range(2))
            if d > Decimal("1e-150"):
                nfail += 1
            if d > maxd:
                maxd = d
            if k in (1, 10, 100, 1000, 10000):
                keep[k] = (P[0][0], P[0][1], lk, d)
        return {"prec": prec, "max": "%.6E" % maxd, "n_fora": nfail, "PASSA": nfail == 0}, keep


xD, keepD = t9_exact_dec(200)
xdr = ree["T9.o'(c)"]["exato_decimal_200"]
item("T9 exato decimal200: PASSA", xD["PASSA"], xdr["PASSA_todo_k"])
out["T9_exato_decimal_200_proprio"] = xD
# C-UNIF-d proprio: mpmath x decimal
with mp.workdps(200):
    worst = mpf(0)
    for k in (1, 10, 100, 1000, 10000):
        for i in range(3):
            worst = max(worst, abs(mpf(str(keepD[k][i])) - keepmp[k][i]))
    out["C-UNIF-d_T9_proprio_max_dif"] = mpmath.nstr(worst, 6)
    item("C-UNIF-d T9: mpmath x decimal concordam a 1e-150", worst <= mpf("1e-150"), ree["T9.o'(c)"]["C-UNIF-d"]["concordam_1e-150_todos"])

# ---- O-f' float E4 proprio
c1, s1 = math.cosh(1.0), math.sinh(1.0)
fo = ree["O-f'"]["float64_E4"]
item("O-f c1 hex == reensaio", c1.hex(), fo["c1_hex"])
item("O-f s1 hex == reensaio", s1.hex(), fo["s1_hex"])
mu = Fraction(c1) - Fraction(s1)
with localcontext() as ctx:
    ctx.prec = 200
    mu_d = Decimal(mu.numerator) / Decimal(mu.denominator)
    ideal = (-Decimal(1)).exp()
    delta_B = float((mu_d - ideal) / ideal)
m_B = (math.exp(2.0) + 1.0) / 2.0
pB = tol["O-f'"]["parametros"]
item("O-f delta_B (proprio, decimal 200) == congelado", delta_B, pB["delta_B_rel"])
item("O-f m_B = (e^2+1)/2 == congelado", m_B, pB["m"])
x, y = 1.0, -1.0
worst10 = 0.0
rels = {}
nfail10 = 0
sym = True
for k in range(1, 101):
    x, y = c1 * x + s1 * y, s1 * x + c1 * y
    sym = sym and (x == -y)
    nrm = math.hypot(x, y)
    ref = math.sqrt(2.0) * math.exp(-k)
    rel = abs(nrm - ref) / ref
    t = tau(k, delta_B, 1.0, m_B, 3.0)
    rels[k] = (rel, t, rel <= t)
    if k <= 10:
        worst10 = max(worst10, rel)
        if rel > t:
            nfail10 += 1
item("O-f E4: max rel k<=10 (bit a bit)", worst10, fo["max_rel_k<=10"])
item("O-f E4: tau_B(10) (bit a bit)", rels[10][1], fo["tau_B_rel(10)"])
item("O-f E4: n k<=10 fora", nfail10, fo["n_k<=10_fora_de_tau"])
item("O-f E4: rel k=1..10 bit a bit == reensaio", all(rels[k][0] == fo["por_k"]["k=%d" % k]["rel"] for k in range(1, 11)), True)
item("O-f E4: orbita na reta nula exata k<=100", sym, fo["orbita_fica_na_reta_nula_exatamente_k<=100"])
item("O-f E4: k=11..100 todos dentro (informativo)", all(rels[k][2] for k in range(11, 101)), fo["informativo_k11..100_todos_dentro_de_tau"])
item("O-f E4: PASSA k<=10", nfail10 == 0, fo["PASSA_k<=10"])
B = np.array([[c1, s1], [s1, c1]])
item("O-f |det B - 1| <= 1e-12", abs(float(np.linalg.det(B)) - 1) <= 1e-12, True)
item("O-f |cosh^2 - sinh^2 - 1| <= 1e-12", abs(c1 * c1 - s1 * s1 - 1) <= 1e-12, True)
# C-UNIF-a proprio
first_mp = None
v = np.array([1.0, -1.0])
ca = ree["O-f'"]["C-UNIF-a"]
same_mp = True
for k in range(1, 13):
    v = B @ v
    ref = math.sqrt(2.0) * math.exp(-k)
    w_ = np.linalg.matrix_power(B, k) @ np.array([1.0, -1.0])
    r_mp = abs(float(np.linalg.norm(w_)) - ref) / ref
    t = tau(k, delta_B, 1.0, m_B, 3.0)
    if first_mp is None and r_mp > t:
        first_mp = k
    same_mp = same_mp and (r_mp == ca["por_k"]["k=%d" % k]["rel_matrix_power"])
item("C-UNIF-a: primeiro k matrix_power fora de tau_B", first_mp, ca["primeiro_k_matrix_power_fora_de_tau"])
item("C-UNIF-a: FALHA em algum k <= 10 (como registrado)", first_mp is not None and first_mp <= 10, ca["comportou_se_como_registrado"])
item("C-UNIF-a: rel_matrix_power k=1..12 bit a bit == reensaio", same_mp, True)


# ---- O-f exato proprio (mpmath 200): (cosh 1 - sinh 1)^k aplicado via orbita, vs sqrt2 e^-k
def of_exact(dps):
    with mp.workdps(dps):
        e1 = mp.e
        ch, sh = (e1 + 1 / e1) / 2, (e1 - 1 / e1) / 2
        x_, y_ = mpf(1), mpf(-1)
        worst = mpf(0)
        kw = 0
        nfail = 0
        keep = {}
        for k in range(1, 101):
            x_, y_ = ch * x_ + sh * y_, sh * x_ + ch * y_
            nr = mp.sqrt(x_ * x_ + y_ * y_)
            ref = mp.sqrt(2) * mp.exp(-k)
            rel = abs(nr - ref) / ref
            if rel > mpf("1e-150"):
                nfail += 1
            if rel > worst:
                worst, kw = rel, k
            if k in (10, 100):
                keep[k] = nr
        return {"max_rel": mpmath.nstr(worst, 8), "k_do_max": kw, "n_fora": nfail, "PASSA": nfail == 0}, keep


oX, keepof = of_exact(200)
oxr = ree["O-f'"]["exato_mpmath_200"]
out["Of_exato_mpmath_200_proprio"] = oX
out["Of_exato_mpmath_200_reensaio"] = {k: oxr[k] for k in ("max_rel", "k_do_max", "n_k_fora", "PASSA_todo_k")}
item("O-f exato mp200: PASSA (k=1..100 a 1e-150 rel)", oX["PASSA"], oxr["PASSA_todo_k"])
item("O-f exato mp200: max rel igual ao reensaio (string 8 dig)", oX["max_rel"], oxr["max_rel"])
# decimal 200 das strings da R1 (k=10, 100)
with localcontext() as ctx:
    ctx.prec = 200
    e1 = Decimal(1).exp()
    ch, sh = (e1 + 1 / e1) / 2, (e1 - 1 / e1) / 2
    xd, yd = Decimal(1), Decimal(-1)
    r1of = r1["subitens_oticos"]["T4.o"]["medidas"]["Of"]["decimal_200"]
    okstr = True
    for k in range(1, 101):
        xd, yd = ch * xd + sh * yd, sh * xd + ch * yd
        if k in (10, 100):
            nr = (xd * xd + yd * yd).sqrt()
            okstr = okstr and (str(nr) == r1of["k=%d" % k]["norma"])
item("O-f decimal200: strings da R1 (norma k=10,100) reproduzidas", okstr, True)

# ---- vereditos pela regra O1/O2 (recomputados a partir dos MEUS numeros)
o1 = "PASSA" if (xE["PASSA"] and fE2["PASSA"] and (not xC["PASSA"]) and worst <= mpf("1e-150")) else "FALHA/INVALIDO"
o2 = "PASSA" if (oX["PASSA"] and nfail10 == 0 and (first_mp is not None and first_mp <= 10)) else "FALHA/INVALIDO"
item("veredito O1 T9.o'(c) recomputado", o1, ree["T9.o'(c)"]["resultado"])
item("veredito O2 O-f' recomputado", o2, ree["O-f'"]["resultado"])
out["n_itens"] = len(it)
out["falhas"] = [x for x in it if not x["ok"]]
out["todos_ok"] = not out["falhas"]
out["estatuto"] = "[REAL - recomputado aqui, modelo sintetico]; beta [DERIVED]; PASSA = validade na face testada, nao creditacao; nada move o gate"
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: v for k, v in out.items() if k != "itens"}, ensure_ascii=False, indent=1, default=str))
for x in it:
    print(("OK  " if x["ok"] else "DIF ") + x["item"], "|", x["lido"], "|", x["esperado"])
