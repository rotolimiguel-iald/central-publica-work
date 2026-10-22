# -*- coding: utf-8 -*-
# Análise do diamante pequeno na rede: controles de convenção, controle sem massa (Hislop–Longo/Casini–Huerta)
# e o termo de primeira ordem na massa contra Cadamuro–Fröb–Minz (Ann. Henri Poincaré 2024, arXiv:2312.04629, Eq. 4.15).
#
# Canais quirais (a = 1, k_F = π/2): c_n ≈ e^{ik_F n} R(x_n) + e^{-ik_F n} L(x_n).  R move-se para a direita.
# Dicionário com CFM (γ⁰ = [[0,1],[-1,0]], γ¹ = [[0,1],[1,0]], γ* = diag(1,-1); ψ₁ = L, ψ₂ = iR, fixado pelo termo de massa
# m(R†L + L†R) da rede e conferido abaixo pelo propagador): H_LL = H₁₁, H_RR = H₂₂, H_RL = -i H₂₁, G_LR = i G₁₂ = F₀/(2π).
# Ordem 1 (CFM 4.15, ℓ = 1):  H_RL^{(1)}(x,y) = -2π mℓ S(x,y),
#   S = ln(mℓ(1-x²)μ/2)(1-x²)/2 δ(x+y) + |x-y|/8 - (1-x²)/2 δ(x-y) - (2-x²-y²)/8 pv_μ 1/|x+y|.
# O termo local -2πmℓ·(-(1-x²)/2)δ(x-y) = m β(x) δ(x-y) é EXATAMENTE a carga geométrica da massa (β = π(1-x²)); o resto é não geométrico.
import numpy as np, glob, os, json, re, sys
from scipy import integrate, special
AQUI = os.path.dirname(os.path.abspath(__file__)); DADOS = os.path.join(AQUI, 'dados')
KMAX = 4
EG = np.euler_gamma
Q = dict(limit=400, epsabs=1e-12, epsrel=1e-11)

def f(k, x):
    return np.sin(k * np.pi * (x + 1) / 2)

def fp(k, x):
    return k * np.pi / 2 * np.cos(k * np.pi * (x + 1) / 2)

# ---------------- contínuo (ℓ = 1) ----------------
def cont_massless_RR():
    M = np.zeros((KMAX, KMAX), complex)
    for k in range(1, KMAX + 1):
        for l in range(1, KMAX + 1):
            v = integrate.quad(lambda x: f(k, x) * (np.pi * (1 - x * x) * fp(l, x) + (-2 * np.pi * x) * f(l, x) / 2), -1, 1, **Q)[0]
            M[k - 1, l - 1] = -1j * v
    return M

def cont_G_LR(mu_m):
    M = np.zeros((KMAX, KMAX))
    for k in range(1, KMAX + 1):
        for l in range(1, KMAX + 1):
            def inner(x):
                g = lambda y: f(l, y) * mu_m * special.k0(mu_m * abs(x - y)) / (2 * np.pi)
                return integrate.quad(g, -1, x, **Q)[0] + integrate.quad(g, x, 1, **Q)[0]
            M[k - 1, l - 1] = integrate.quad(lambda x: f(k, x) * inner(x), -1, 1, **Q)[0]
    return M

def cont_first_order_parts(mu=1.0):
    A = np.zeros((KMAX, KMAX)); B1 = np.zeros_like(A); T2 = np.zeros_like(A); T3 = np.zeros_like(A); T4 = np.zeros_like(A)
    for k in range(1, KMAX + 1):
        for l in range(1, KMAX + 1):
            A[k-1, l-1] = integrate.quad(lambda x: f(k, x) * f(l, -x) * (1 - x * x) / 2, -1, 1, **Q)[0]
            B1[k-1, l-1] = integrate.quad(lambda x: f(k, x) * f(l, -x) * (1 - x * x) / 2 * np.log((1 - x * x) * mu / 2), -1, 1, points=[0], **Q)[0]
            def in2(x):
                return integrate.quad(lambda y: f(l, y) * (x - y), -1, x, **Q)[0] + integrate.quad(lambda y: f(l, y) * (y - x), x, 1, **Q)[0]
            T2[k-1, l-1] = integrate.quad(lambda x: f(k, x) * in2(x), -1, 1, **Q)[0] / 8
            T3[k-1, l-1] = -integrate.quad(lambda x: f(k, x) * f(l, x) * (1 - x * x) / 2, -1, 1, **Q)[0]
            def J(x):
                c = 1 - abs(x)
                g = lambda z: f(l, z - x) * (2 - x * x - (z - x) ** 2) / 8
                g0 = g(0.0)
                s = integrate.quad(lambda z: (g(z) - g0) / abs(z), -c, 0, **Q)[0] + integrate.quad(lambda z: (g(z) - g0) / abs(z), 0, c, **Q)[0]
                s += g0 * 2 * np.log(mu * c * np.exp(-EG))
                if x < 0: s += integrate.quad(lambda z: g(z) / abs(z), x - 1, -c, **Q)[0]
                if x > 0: s += integrate.quad(lambda z: g(z) / abs(z), c, x + 1, **Q)[0]
                return s
            T4[k-1, l-1] = -integrate.quad(lambda x: f(k, x) * J(x), -1, 1, points=[0], limit=200, epsabs=1e-10, epsrel=1e-9)[0]
    return {'A_log': A, 'B1': B1, 'T2': T2, 'T3_local': T3, 'T4': T4}

# ---------------- rede ----------------
def carrega(ell):
    out = {}
    for p in glob.glob(os.path.join(DADOS, 'H_l%d_m*_s*_d*.npz' % ell)):
        z = np.load(p)
        key = (str(z['mell']), int(z['sinal']), int(z['dps']))
        out[key] = z
    return out

def vetores(ell, k, quiral):
    n = np.arange(2 * ell); x = (n - ell + 0.5) / ell
    fase = np.exp(1j * np.pi * n / 2) if quiral == 'R' else np.exp(-1j * np.pi * n / 2)
    return fase * f(k, x) / np.sqrt(ell)

def smear(ell, Mop, qa, qb):
    M = np.zeros((KMAX, KMAX), complex)
    V = {q: [vetores(ell, k, q) for k in range(1, KMAX + 1)] for q in ('R', 'L')}
    for k in range(KMAX):
        for l in range(KMAX):
            M[k, l] = np.conj(V[qa][k]) @ Mop @ V[qb][l]
    return M

def janelas(ell, dH, mell, w_frac=0.25):
    # somas de janela do núcleo RL demodulado: antidiagonal |x+y|<=w e diagonal |x-y|<=w, média de dois sítios vizinhos
    N = 2 * ell; n = np.arange(N); x = n - ell + 0.5; m = float(mell) / ell; w = w_frac * ell
    dem = np.exp(-1j * np.pi * (n[:, None] + n[None, :]) / 2) * dH
    res = []
    for xf in (-0.6, -0.45, 0.45, 0.6):
        n0 = int(round(xf * ell + ell - 0.5)); vals_a = []; vals_d = []
        for nn in (n0, n0 + 1):
            xa = x[nn]
            vals_a.append(dem[nn, np.abs(xa + x) <= w].sum()); vals_d.append(dem[nn, np.abs(xa - x) <= w].sum())
        xm = (x[n0] + x[n0 + 1]) / 2
        l2 = ell * ell - xm * xm
        P_anti = -(np.pi * m / ell) * (l2 * np.log(m * l2 * np.exp(EG) / (2 * w)) + abs(xm) * w + w * w / 4)
        zint = integrate.quad(lambda z: (2 * (ell**2 - xm**2) - 2 * xm * z - z * z) / abs(2 * xm + z), -w, w, limit=200)[0]
        P_diag = -2 * np.pi * m * ell * (-(l2) / (2 * ell**2) + w * w / (8 * ell**2) - zint / (8 * ell**2))
        res.append({'x/l': round(xm / ell, 4), 'anti_rede': complex(np.mean(vals_a)), 'anti_previsto': P_anti,
                    'diag_rede': complex(np.mean(vals_d)), 'diag_previsto': P_diag, 'm_beta': m * np.pi * l2 / ell})
    return res

if __name__ == '__main__':
    ells = sorted(set(int(re.search(r'H_l(\d+)_', os.path.basename(p)).group(1)) for p in glob.glob(os.path.join(DADOS, 'H_l*.npz'))))
    print('ℓ disponíveis:', ells)
    cont = cont_first_order_parts(mu=1.0)
    cont3 = cont_first_order_parts(mu=3.0)
    mu_indep = float(np.abs((cont['B1'] + cont['T4']) - (cont3['B1'] + cont3['T4'])).max())
    print('independência de μ (B1+T4): %.2e' % mu_indep)
    M0c = cont_massless_RR()
    rel = {'versao': 'DIAMANTE_REDE_V1', 'fonte_analitica': 'Cadamuro-Frob-Minz, Ann. Henri Poincare (2024), arXiv:2312.04629, Eq. (4.15)',
           'KMAX': KMAX, 'mu_independencia': mu_indep, 'por_ell': {}}
    MASSAS = ('0.0001', '0.0003', '0.001', '0.003', '0.01', '0.03', '0.1')
    Gc = {me: cont_G_LR(float(me)) for me in MASSAS}
    for ell in ells:
        D = carrega(ell)
        d0 = max(k[2] for k in D if k[0] == '0')
        H0 = D[('0', 1, d0)]['H']
        r = {}
        M0 = smear(ell, H0, 'R', 'R'); M0L = smear(ell, H0, 'L', 'L')
        r['sem_massa_RR_erro_rel'] = float(np.abs(M0 - M0c).max() / np.abs(M0c).max())
        r['sem_massa_LL_erro_rel'] = float(np.abs(M0L + M0c).max() / np.abs(M0c).max())
        r['por_massa'] = {}
        for me in MASSAS:
            ks = [k for k in D if k[0] == me]
            if not ks: continue
            dps = min(k[2] for k in ks)
            Hp, Hm = D[(me, 1, dps)]['H'], D[(me, -1, dps)]['H']
            Cp, Cm = D[(me, 1, dps)]['C'], D[(me, -1, dps)]['C']
            dH = (Hp - Hm) / 2
            Godd = -(Cp - Cm) / 2
            MG = smear(ell, Godd, 'L', 'R')
            M1 = smear(ell, dH, 'R', 'L')
            mm = float(me)
            pred = -2 * np.pi * mm * (cont['A_log'] * np.log(mm) + cont['B1'] + cont['T2'] + cont['T3_local'] + cont['T4'])
            geo = -2 * np.pi * mm * cont['T3_local']
            e = {'G_LR_erro_rel': float(np.abs(MG - Gc[me]).max() / np.abs(Gc[me]).max()),
                 'G_LR_sinal': float(np.sign(np.real(np.sum(MG * Gc[me])))),
                 'M1_imag_max': float(np.abs(M1.imag).max()), 'M1_real_max': float(np.abs(M1.real).max()),
                 'M1_erro_rel': float(np.abs(M1.real - pred).max() / np.abs(pred).max()),
                 'nao_geometrico_rede': (M1.real - geo).tolist(), 'nao_geometrico_previsto': (pred - geo).tolist(),
                 'M1_rede': M1.real.tolist(), 'M1_previsto': pred.tolist()}
            e['nao_geometrico_erro_rel'] = float(np.abs((M1.real - geo) - (pred - geo)).max() / np.abs(pred - geo).max())
            e['razao_resto_sobre_geometrico_sem_massa'] = float(np.linalg.norm(pred - geo) / np.linalg.norm(M0c))
            e['janelas'] = [{k2: (str(v) if isinstance(v, complex) else v) for k2, v in d.items()} for d in janelas(ell, dH, me)]
            if len([k for k in ks if k[1] == 1]) > 1:
                dps2 = max(k[2] for k in ks)
                dH2 = (D[(me, 1, dps2)]['H'] - D[(me, -1, dps2)]['H']) / 2
                e['controle_precisao_dps'] = [dps, dps2]
                e['controle_precisao_max_dif'] = float(np.abs(dH2 - dH).max())
            r['por_massa'][me] = e
        # ajuste em ln(mℓ): M1/(mℓ) = a ln(mℓ) + b, por elemento
        ms = [me for me in ('0.0001', '0.0003', '0.001') if me in r['por_massa']]
        if len(ms) >= 2:
            X = np.array([[np.log(float(me)), 1.0] for me in ms])
            Y = np.array([np.array(r['por_massa'][me]['M1_rede']) / float(me) for me in ms])
            coef = np.linalg.lstsq(X, Y.reshape(len(ms), -1), rcond=None)[0]
            a_lat = coef[0].reshape(KMAX, KMAX); b_lat = coef[1].reshape(KMAX, KMAX)
            a_c = -2 * np.pi * cont['A_log']; b_c = -2 * np.pi * (cont['B1'] + cont['T2'] + cont['T3_local'] + cont['T4'])
            r['coef_log_erro_rel'] = float(np.abs(a_lat - a_c).max() / np.abs(a_c).max())
            r['coef_const_erro_rel'] = float(np.abs(b_lat - b_c).max() / np.abs(b_c).max())
            r['coef_log_rede'] = a_lat.tolist(); r['coef_log_previsto'] = a_c.tolist()
            r['coef_const_rede'] = b_lat.tolist(); r['coef_const_previsto'] = b_c.tolist()
        rel['por_ell'][ell] = r
        linha = 'ℓ=%3d  sem massa RR %.2e LL %.2e' % (ell, r['sem_massa_RR_erro_rel'], r['sem_massa_LL_erro_rel'])
        for me, e in r['por_massa'].items():
            linha += ' | mℓ=%s G_LR %.1e(s%+d) M1 %.2e NG %.2e im %.1e' % (me, e['G_LR_erro_rel'], e['G_LR_sinal'], e['M1_erro_rel'], e['nao_geometrico_erro_rel'], e['M1_imag_max'])
            if 'controle_precisao_max_dif' in e: linha += ' prec %.1e' % e['controle_precisao_max_dif']
        if 'coef_log_erro_rel' in r: linha += ' | log %.2e const %.2e' % (r['coef_log_erro_rel'], r['coef_const_erro_rel'])
        print(linha, flush=True)
    rel['continuo'] = {k: v.tolist() for k, v in cont.items()}
    json.dump(rel, open(os.path.join(AQUI, 'analise_rede_resultado.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
