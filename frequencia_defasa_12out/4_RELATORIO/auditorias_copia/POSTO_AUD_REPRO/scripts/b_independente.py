# -*- coding: utf-8 -*-
"""Auditor REPRO, item (3c): SEGUNDO CALCULO INDEPENDENTE (sem o codigo do construtor).
- alpha lido por regex PROPRIA dos bytes do um.py (linha que COMECA com ALPHA_FINE_CODATA_2018 =), sem executar o um.py;
  beta = alpha*sqrt(e) em runtime (float64, mpmath dps 60 e sympy exato). O numero de conferencia de beta e LIDO do
  PREREGISTRO.json congelado e o numero do operador dos bytes de V4: nenhum literal de beta/alpha/thetaM aqui.
- algebra EXATA em sympy (theta simbolico, taxas e tempo simbolicos) para as identidades;
- alta precisao (mpmath dps 60) para os numeros em thetaM;
- amostragem PROPRIA (semente e amostradores diferentes dos do construtor) para as afirmacoes gerais.
Grava so saidas/B_INDEPENDENTE.json na pasta do auditor."""
import os, re, json, math, hashlib, collections
import numpy as np
import mpmath as mp
import sympy as sp

AUD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UMPY = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\um.py"
PRE = "C:\\IALD\\Central de Patentes\\work\\frequencia_defasa_12out\\1_PREREGISTRO\\PREREGISTRO.json"
V4 = "C:\\IALD\\Central de Patentes\\work\\cunhagens_10out\\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt"
R = collections.OrderedDict()

# ---------------------------------------------------------------- alpha e beta (runtime)
ub = open(UMPY, "rb").read()
R["um_py_sha256"] = hashlib.sha256(ub).hexdigest()
ms = list(re.finditer(rb"^ALPHA_FINE_CODATA_2018[ \t]*=[ \t]*([0-9.eE+\-]+)[ \t]*(?:#[^\n]*)?\r?$", ub, re.M))
assert len(ms) == 1, "FALHA VISIVEL: atribuicao de alpha nao e unica: %d" % len(ms)
a_txt = ms[0].group(1).decode()
R["alpha_texto"] = a_txt
R["alpha_linha"] = ub.count(b"\n", 0, ms[0].start()) + 1
alpha = float(a_txt)
beta = alpha * math.sqrt(math.e)
mp.mp.dps = 60
alpha_mp = mp.mpf(a_txt)
beta_mp = alpha_mp * mp.sqrt(mp.e)
beta_sp = sp.Rational(sp.nsimplify(a_txt, rational=True)) * sp.sqrt(sp.E)
pre = json.load(open(PRE, encoding="utf-8"))
conf = pre["beta_runtime"]["beta_float64"]
R["beta_float64_repr"] = repr(beta)
R["beta_conferencia_lida_do_preregistro"] = conf
R["beta_confere_repr"] = repr(beta) == conf
R["beta_mp60"] = mp.nstr(beta_mp, 40)
R["beta_sympy_60dig"] = str(sp.N(beta_sp, 40))
R["beta_mp_vs_sympy"] = mp.nstr(abs(beta_mp - mp.mpf(str(sp.N(beta_sp, 70)))), 5)
R["beta_float_vs_mp"] = mp.nstr(abs(mp.mpf(beta) - beta_mp), 5)
thM = math.asin(math.sqrt(beta))
thM_mp = mp.asin(mp.sqrt(beta_mp))
R["thetaM_float64"] = repr(thM)
R["thetaM_mp"] = mp.nstr(thM_mp, 40)

# ---------------------------------------------------------------- algebra exata (sympy)
th, t, g01, g10, b = sp.symbols("theta t g01 g10 b", real=True)
c, s = sp.cos(th), sp.sin(th)
rho = sp.Matrix([[1, 0], [0, 0]])
Q0 = sp.eye(2) - rho
Rot = sp.Matrix([[c, -s], [s, c]])          # receita do um.py (l.6518)
S = sp.Matrix([[c, s], [-s, c]])            # Smat (kernel): cos*1 + sin*Grot
Qth_umpy = sp.simplify(Rot * Q0 * Rot.T)
Qth_ker = sp.simplify(S.H * Q0 * S)
F = sp.simplify(S * rho * S.H)              # rhoOut th
anti = sp.simplify(Qth_umpy * rho + rho * Qth_umpy)
Dt = lambda X: sp.Matrix([[X[0, 0], sp.exp(-t * g01) * X[0, 1]], [sp.exp(-t * g10) * X[1, 0], X[1, 1]]])
Dinf = lambda X: sp.Matrix([[X[0, 0], 0], [0, X[1, 1]]])
z = lambda M: all(sp.simplify(e) == 0 for e in M)
E = collections.OrderedDict()
E["B2.a Q_th (um.py) = [[s^2,-sc],[-sc,c^2]]"] = z(Qth_umpy - sp.Matrix([[s**2, -s*c], [-s*c, c**2]]))
E["B2.a Q_th (um.py) = S^H Q0 S (kernel)"] = z(Qth_umpy - Qth_ker)
E["B2.a {Q_th,rho*} = [[2s^2,-sc],[-sc,0]]"] = z(anti - sp.Matrix([[2*s**2, -s*c], [-s*c, 0]]))
E["B2.a Tr{Q_th,rho*} = 2 s^2"] = sp.simplify(anti.trace() - 2*s**2) == 0
E["B2.a sum|.|^2 = 2 s^2 (1+s^2)"] = sp.simplify(sum(e**2 for e in anti) - 2*s**2*(1 + s**2)) == 0
E["B3.a Tr(rho* Q_th) = s^2"] = sp.simplify((rho*Qth_umpy).trace() - s**2) == 0
E["B3.a Tr(F_th(1) Q0) = s^2"] = sp.simplify((F*Q0).trace() - s**2) == 0
E["B3.a (rhoOut th)_11 = s^2"] = sp.simplify(F[1, 1] - s**2) == 0
E["B4.b rhoOut: Tr 1, idempotente, hermitiana"] = (sp.simplify(F.trace() - 1) == 0) and z(F*F - F) and z(F - F.H)
E["B5.a D_inf F = diag(c^2, s^2)"] = z(Dinf(F) - sp.diag(c**2, s**2))
E["B5.a det D_inf F = c^2 s^2 = sin^2(2th)/4"] = sp.simplify(Dinf(F).det() - sp.sin(2*th)**2/4) == 0
E["B5.a pureza D_inf F = 1 - 2 s^2 c^2"] = sp.simplify((Dinf(F)**2).trace() - (1 - 2*s**2*c**2)) == 0
E["B5.c det D_t F = c^2 s^2 (1 - e^{-t(g01+g10)})"] = sp.simplify(Dt(F).det() - c**2*s**2*(1 - sp.exp(-t*(g01 + g10)))) == 0
E["B5.c Tr D_t F = 1"] = sp.simplify(Dt(F).trace() - 1) == 0
E["B6.a Tr(rho* D_t Q_th) = s^2 (todo t, toda taxa)"] = sp.simplify((rho*Dt(Qth_umpy)).trace() - s**2) == 0
ad = sp.simplify(Dt(Qth_umpy)*rho + rho*Dt(Qth_umpy))
E["B6.b {D_t Q_th, rho*} = [[2s^2,-e^{-t g01}sc],[-e^{-t g10}sc,0]]"] = z(ad - sp.Matrix([[2*s**2, -sp.exp(-t*g01)*s*c], [-sp.exp(-t*g10)*s*c, 0]]))
E["B6.b {D_inf Q_th, rho*} = diag(2s^2, 0)"] = z(sp.simplify(Dinf(Qth_umpy)*rho + rho*Dinf(Qth_umpy)) - sp.diag(2*s**2, 0))
M = sp.Matrix(2, 2, sp.symbols("m00 m01 m10 m11"))
E["P1.b 2x2: Tr M^2 = (Tr M)^2 - 2 det M"] = sp.expand((M*M).trace() - (M.trace()**2 - 2*M.det())) == 0
# B5.b em b simbolico
E["B5.b det diag(1-b,b) = b(1-b): zero so em b=0,1"] = sp.solve(sp.Eq(sp.diag(1 - b, b).det(), 0), b) == [0, 1]
E["B5.b pureza diag(1-b,b) = 1 - 2b(1-b)"] = sp.expand((sp.diag(1 - b, b)**2).trace() - (1 - 2*b*(1 - b))) == 0
# B7.a1: S(th)^n = S(n th) para n = 1..12 (simbolico)
E["B7.a1 S(th)^n = S(n th), n=1..12"] = all(z(sp.simplify(sp.expand_trig(S**n - S.subs(th, n*th)))) for n in range(1, 13))
# P4: d = posto, rho = P/d: Tr rho^2 = 1/d
d = sp.symbols("d", positive=True, integer=True)
E["P4 Tr(P/d)^2 = Tr(P)/d^2 = 1/d e = Tr(P/d) <=> d = 1"] = (sp.simplify(d/d**2 - 1/d) == 0) and (sp.solve(sp.Eq(1/d, 1), d) == [1])
R["algebra_exata_sympy"] = E
R["algebra_exata_todas_verdadeiras"] = all(E.values())

# ---------------------------------------------------------------- numeros em thetaM (mpmath dps 60)
cM, sM = mp.cos(thM_mp), mp.sin(thM_mp)
N = collections.OrderedDict()
N["B3.b leak Tr(rho* Q_thM) = sin^2 thM; |leak - beta|"] = mp.nstr(abs(sM**2 - beta_mp), 5)
N["B2.b |{Q_thM,rho*}|_F = sqrt(2 beta (1+beta))"] = mp.nstr(mp.sqrt(2*beta_mp*(1 + beta_mp)), 20)
N["B2.b |{Q_thM,rho*}|_F direto (2s^2,-sc,-sc,0)"] = mp.nstr(mp.sqrt((2*sM**2)**2 + 2*(sM*cM)**2), 20)
N["B2.b Tr = 2 beta"] = mp.nstr(2*sM**2, 20)
N["B5.b pureza 1 - 2 beta (1 - beta)"] = mp.nstr(1 - 2*beta_mp*(1 - beta_mp), 30)
N["B5.b autovalores D_inf F = (1-beta, beta)"] = [mp.nstr(cM**2, 20), mp.nstr(sM**2, 20)]
# B5.c: sigma_min de D_t F (2x2 hermitiana, posto 2 <=> det != 0) em gamma = beta, t = 0.5 e em gamma = 1, t = 0.5
def lam_min(gamma, tt):
    s22 = mp.sin(2*thM_mp)**2
    return (1 - mp.sqrt(1 - s22*(1 - mp.e**(-2*gamma*tt)))) / 2
N["B5.c sigma_min(gamma=beta, t=0.5)"] = mp.nstr(lam_min(beta_mp, mp.mpf(1)/2), 15)
N["B5.c sigma_min(gamma=1, t=0.5)"] = mp.nstr(lam_min(mp.mpf(1), mp.mpf(1)/2), 15)
N["B5.c sigma_min(gamma=1, t=1)"] = mp.nstr(lam_min(mp.mpf(1), mp.mpf(1)), 15)
# menor sigma_min sobre G_t (t>0) x gamma {1, beta}
Gt = [mp.mpf(x) for x in ("0.5", "1", "2", "5", "10", "100")]
mins = sorted([(lam_min(gm, tt), nm, tt) for nm, gm in (("1", mp.mpf(1)), ("beta", beta_mp)) for tt in Gt])
N["B5.c menor sigma_min com t>0 em G_t x gamma"] = [mp.nstr(mins[0][0], 6), "gamma=" + mins[0][1], "t=" + mp.nstr(mins[0][2], 3)]
# B6.b: norma F de {D_t Q_thM, rho*} com gamma = 1
N["B6.b |{D_t Q_thM,rho*}|_F gamma=1 t=0.5, t=10"] = [mp.nstr(mp.sqrt((2*sM**2)**2 + 2*(mp.e**(-tt)*sM*cM)**2), 17) for tt in (mp.mpf("0.5"), mp.mpf(10))]
# B3.d: numero do operador lido dos bytes de V4 (l.16)
v4 = open(V4, "rb").read().decode("utf-8").split("\n")
mop = re.search(r"\\approx\s*([0-9.]+)", v4[15])
op = mop.group(1)
N["B3.d numero do operador (V4 l.16, bytes)"] = op
N["B3.d |beta - numero do operador|"] = mp.nstr(abs(beta_mp - mp.mpf(op)), 10)
N["B3.d <= 5e-7"] = bool(abs(beta_mp - mp.mpf(op)) <= mp.mpf("5e-7"))
R["numeros_thetaM_mp60"] = N

# ---------------------------------------------------------------- B7.a2: oscilacao angular (fila monotona propria)
NN, Wn = 100000, int(math.ceil(math.pi / thM)) + 2
x = [math.sin(n * thM) ** 2 for n in range(NN)]
dq_max, dq_min = collections.deque(), collections.deque()
menor, idx = 9.0, -1
for i, v in enumerate(x):
    while dq_max and x[dq_max[-1]] <= v:
        dq_max.pop()
    dq_max.append(i)
    while dq_min and x[dq_min[-1]] >= v:
        dq_min.pop()
    dq_min.append(i)
    ini = i - Wn + 1
    if dq_max[0] < ini:
        dq_max.popleft()
    if dq_min[0] < ini:
        dq_min.popleft()
    if ini >= 0:
        osc = x[dq_max[0]] - x[dq_min[0]]
        if osc < menor:
            menor, idx = osc, ini
R["B7.a2"] = {"W": Wn, "N": NN, "n_janelas": NN - Wn + 1, "menor_oscilacao": repr(menor), "janela_do_minimo": idx,
             "cota_cos_thM_menos_1e-9": repr(math.cos(thM) - 1e-9), "passa": menor >= math.cos(thM) - 1e-9,
             "prova_da_cota [DERIVED aqui]": "W >= ceil(pi/th)+1 termos consecutivos de n*th mod pi, passo th: algum termo a <= th/2 de pi/2 "
                                            "(sin^2 >= cos^2(th/2)) e algum a <= th/2 de 0 ou pi (sin^2 <= sin^2(th/2)); "
                                            "max - min >= cos^2(th/2) - sin^2(th/2) = cos th > 0, logo sin^2(n th) nao converge",
             "pi": repr(max(math.sin(n * math.pi) ** 2 for n in range(NN)))}

# ---------------------------------------------------------------- amostragem propria (semente 4242, amostradores diferentes)
rng = np.random.default_rng(4242)
def unitario(n):     # exp(i H) com H hermitiana gaussiana (nao QR)
    A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    H = (A + A.conj().T) / 2
    w, V = np.linalg.eigh(H)
    return (V * np.exp(1j * w)) @ V.conj().T
def posto(A, tol=1e-9):
    sv = np.linalg.svd(A, compute_uv=False)
    return int((sv > tol * max(1.0, sv[0])).sum())
viol = collections.Counter()
cont = collections.Counter()
for n in (2, 3, 4, 5):
    for k in range(400):
        # puro: |psi><psi| com psi complexo NAO normalizado depois normalizado; misto: Wishart G G^H / Tr de posto r
        r = 1 + (k % n)
        G = rng.normal(size=(n, r)) + 1j * rng.normal(size=(n, r))
        rh = G @ G.conj().T
        rh = rh / np.trace(rh).real
        pur = np.trace(rh @ rh).real
        rk = posto(rh)
        idem = np.linalg.norm(rh @ rh - rh) < 1e-10
        p1 = abs(pur - 1) < 1e-10
        cont["P1.a estados"] += 1
        if not (p1 == (rk == 1) == idem):
            viol["P1.a"] += 1
        if rk != r:
            viol["amostrador posto"] += 1
        # B4.a: Ad(u) preserva traco e posto
        u = unitario(n)
        ru = u @ rh @ u.conj().T
        if abs(np.trace(ru) - np.trace(rh)) > 1e-12 or posto(ru) != rk:
            viol["B4.a"] += 1
        cont["B4.a"] += 1
        # P3.a: P X P = <a,Xa> P, Tr(P X) = <a,Xa>, para a NAO normalizado tambem (sonda: a hipotese <a,a>=1 tem peso?)
        a = rng.normal(size=n) + 1j * rng.normal(size=n)
        for nome, aa in (("normalizado", a / np.linalg.norm(a)), ("nao_normalizado", a)):
            P = np.outer(aa, aa.conj())
            w = aa.conj() @ rh @ aa
            if np.linalg.norm(P @ rh @ P - w * P) > 1e-10 * (1 + np.linalg.norm(P) ** 2) or abs(np.trace(P @ rh) - w) > 1e-10 * (1 + np.linalg.norm(P)):
                viol["P3.a " + nome] += 1
            cont["P3.a " + nome] += 1
# P4: projecoes de posto d em n = 6 (Gram-Schmidt por QR de gaussiana), rho = P/d
for dd in range(1, 7):
    for k in range(50):
        Qm, _ = np.linalg.qr(rng.normal(size=(6, dd)) + 1j * rng.normal(size=(6, dd)))
        P = Qm @ Qm.conj().T
        rh = P / dd
        ok = abs(np.trace(P).real - dd) < 1e-10 and posto(P) == dd and abs(np.trace(rh).real - 1) < 1e-12 and abs(np.trace(rh @ rh).real - 1 / dd) < 1e-12
        igual = abs(np.trace(rh @ rh).real - np.trace(rh).real) < 1e-12
        if not ok or (igual != (dd == 1)):
            viol["P4"] += 1
        cont["P4"] += 1
# B9.b e B8.b em varredura de theta: D atua (existe t>0) <=> c != 0 e s != 0 ; usa a forma exata (fora diagonal -cs)
ths = np.linspace(-2 * math.pi, 2 * math.pi, 4001)
for tt in ths:
    cc, ss = math.cos(tt), math.sin(tt)
    atua = abs(cc * ss) > 1e-12                     # D_t F != F para t>0 <=> entrada fora da diagonal != 0
    trans_e_vaza = cc * cc > 1e-12 and ss * ss > 1e-12
    if atua != trans_e_vaza:
        viol["B9.b"] += 1
    cont["B9.b"] += 1
R["amostragem_propria"] = {"semente": 4242, "contagens": dict(cont), "violacoes": dict(viol)}
# B5.e(ii) e B9.a/B9.a' (negativos): testemunhas
R["B5.e(ii) testemunha thM: posto D_inf F, posto F"] = [posto(np.diag([math.cos(thM) ** 2, math.sin(thM) ** 2])), posto(np.array([[math.cos(thM) ** 2, -math.cos(thM) * math.sin(thM)], [-math.cos(thM) * math.sin(thM), math.sin(thM) ** 2]]))]
R["B9.a testemunha th=0: |t|^2, D atua?"] = [1.0, False]
R["B9.a' testemunha th=pi/2: |r|^2 exato (sympy), off-diag exato"] = [str(sp.sin(sp.pi/2)**2), str(sp.cos(sp.pi/2)*sp.sin(sp.pi/2))]
SAIDA = os.path.join(AUD, "saidas", "B_INDEPENDENTE.json")
open(SAIDA, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str))
print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
