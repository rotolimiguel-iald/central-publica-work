# -*- coding: utf-8 -*-
"""f9v2_stats.py -- a ESTATISTICA do executor da Fase 9 V2-c1 (X13 = SIM: o texto descreve o que o executor faz).

O que o executor faz (e o que esta' dito no spec V2-c1, secao estatisticas_do_executor):
  * o fundo e' MARGINALIZADO: y ~ N(P f, C + V f f'), com V = variancia da PREVISAO local (S5: propaga H0, Omega_m, Omega_r do fundo; sem S5: (K sigma_bg)^2);
  * z_delta = (beta_hat - beta_TGL)/sigma_beta, pelo PERFIL de ln L (que inclui o log-det de S), sigma_beta = media dos dois lados (os dois lados sao obrigatorios);
  * z_disc = sinal sqrt|chi2_LCDM - chi2_TGL| (forma quadratica, sem o log-det; a variante com log-det vai ao lado);
  * ln B por quadratura de Gauss-Legendre com n = 100 (decisorio) e n = 200 (conferencia): |diferenca| > QUAD_TOL => RECUSA, sem veredito;
  * dispersao: chi2_int/(n-1) e p com a covariancia do ponto, SEM o fundo.
Nenhum centro local e' fabricado aqui: as funcoes recebem y. Sem estado global. Numpy float64.
"""
import math

import numpy as np
from scipy import optimize
from scipy import stats as sps
from scipy.special import logsumexp

PRIOR_BETA = (-0.05, 0.05)
PRIOR_SHIFT = (-0.15, 0.15)
QUAD_N = 100
QUAD_CHECK_N = 200
QUAD_TOL = 1e-6
CEPHEID_IDS = ("L1_sh0es_r22", "L1b_sh0es_r25")
NMAP = {"L1_sh0es_r22": "L1N", "L1b_sh0es_r25": "L1bN", "L2_cchp": "L2N", "L3_sbf": "L3N", "L4_masers_6": "L4N"}
TMAP = {"L2_cchp": "L2T", "L3_sbf": "L3T"}


class StatsError(RuntimeError):
    pass


class QuadratureUnstable(StatsError):
    """E3: as quadraturas n=100 e n=200 discordam alem da tolerancia => RECUSA, sem veredito."""


def _fin(x, name, positive=False):
    if isinstance(x, bool) or not isinstance(x, (int, float, np.floating, np.integer)):
        raise StatsError("%s deve ser numerico" % name)
    v = float(x)
    if not math.isfinite(v) or (positive and v <= 0):
        raise StatsError("%s deve ser finito e valido" % name)
    return v


# ------------------------------------------------------------------ caixa de covariancia
def covariance(amps, sigmas, ids, lam_n, lam_t):
    if not (0 <= lam_n <= 1 and 0 <= lam_t <= 1):
        raise StatsError("parametro de covariancia fora da caixa pre-registrada")
    n = len(ids)
    C = np.zeros((n, n))
    for i, a in enumerate(ids):
        C[i, i] = _fin(sigmas[a], "sigma " + a, positive=True) ** 2
        for j in range(i):
            b = ids[j]
            v = 0.0
            if a in NMAP and b in NMAP:
                v += lam_n * amps[NMAP[a]] * amps[NMAP[b]]
            if a in TMAP and b in TMAP:
                v += lam_t * amps[TMAP[a]] * amps[TMAP[b]]
            C[i, j] = C[j, i] = v
    return C


def gls_weights(C):
    n = C.shape[0]
    w0 = np.linalg.solve(C, np.ones(n))
    den = float(w0.sum())
    if not den > 0:
        raise StatsError("denominador do GLS nao positivo")
    return w0 / den, math.sqrt(1.0 / den)


def grid_endpoints(amps, sigmas, ids, grid_n, grid_t, eig_min=1e-12, tie_tol=1e-12):
    """Extremos de sigma_comb na grade (lambda_N externo, lambda_T interno; empate: o primeiro). So pontos positivo-definidos."""
    best = {"minimum": None, "maximum": None}
    accepted = 0
    rejected = 0
    for ln in grid_n:
        for lt in grid_t:
            C = covariance(amps, sigmas, ids, ln, lt)
            if not float(np.linalg.eigvalsh(C).min()) > eig_min:
                rejected += 1
                continue
            w, sc = gls_weights(C)
            accepted += 1
            pt = {"lambda_N": ln, "lambda_T": lt, "sigma_comb": sc, "covariance": C, "weights": w}
            for kind in best:
                old = best[kind]
                if old is None or (sc < old["sigma_comb"] - tie_tol if kind == "minimum" else sc > old["sigma_comb"] + tie_tol):
                    best[kind] = pt
    if not accepted:
        raise StatsError("grade de covariancia vazia")
    return {"accepted": accepted, "rejected": rejected, **best}


def max_variance_of_estimator(amps, sigmas, ids, w, grid_n, grid_t):
    """sup sobre a grade de Var(w'y) quando a covariancia VERDADEIRA e' a do ponto da grade (calibracao com sistematicas)."""
    best = -1.0
    arg = None
    for ln in grid_n:
        for lt in grid_t:
            C = covariance(amps, sigmas, ids, ln, lt)
            if not float(np.linalg.eigvalsh(C).min()) > 1e-12:
                continue
            v = float(w @ C @ w)
            if v > best:
                best, arg = v, (ln, lt)
    return best, arg


# ------------------------------------------------------------------ a lei e o fundo (S5)
def e_lcdm(z, H0, ombh2, omch2, c):
    """Replica de um.py::_v378_lcdm_E: E(z) do LCDM plano com radiacao (foton + N_eff); neutrino massivo como materia, m/93.14."""
    h2 = (H0 / 100.0) ** 2
    og = c["og_coef"] * c["TCMB"] ** 4
    Or = og * (1.0 + c["Neff"] * (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)) / h2
    Om = (ombh2 + omch2 + c["mnu_eV"] / 93.14) / h2
    OL = 1.0 - Om - Or
    return math.sqrt(Om * (1.0 + z) ** 3 + Or * (1.0 + z) ** 4 + OL), Om, Or


def lnE_pinned(Om, Orad, zstar):
    e2 = Om * (1 + zstar) ** 3 + Orad * (1 + zstar) ** 4 + 1.0 - Om - Orad
    if not e2 > 0:
        raise StatsError("E(z*)^2 nao positivo")
    return 0.5 * math.log(e2)


def grad_lnE(theta, zstar, consts):
    """Gradiente de ln E(z*; H0, omega_b, omega_c) por diferencas centrais (passo relativo 1e-5)."""
    g = np.zeros(3)
    th = np.array(theta, float)
    for i in range(3):
        h = 1e-5 * abs(th[i])
        up, dn = th.copy(), th.copy()
        up[i] += h
        dn[i] -= h
        g[i] = (math.log(e_lcdm(zstar, *up, consts)[0]) - math.log(e_lcdm(zstar, *dn, consts)[0])) / (2 * h)
    return g


class Law:
    """K_b = exp(2b/3 ln E_pin); previsao local P_b = K_b mu; variancia da previsao V_b (S5 ou ingenua)."""

    def __init__(self, beta, K_frozen, lnE_pin, mu, cov_theta, theta_hat, zstar, consts, s5=True, tol_K=1e-12):
        self.beta = _fin(beta, "beta", positive=True)
        self.lnE = _fin(lnE_pin, "lnE")
        self.K = math.exp(2.0 * self.beta / 3.0 * self.lnE)
        if not math.isclose(self.K, K_frozen, rel_tol=tol_K):
            raise StatsError("K recalculado (%r) difere do K congelado (%r)" % (self.K, K_frozen))
        self.mu = _fin(mu, "mu", positive=True)
        self.Cth = np.array(cov_theta, float)
        self.theta = np.array(theta_hat, float)
        self.s5 = bool(s5)
        self.gl = grad_lnE(self.theta, zstar, consts)
        self.sigma_bg = math.sqrt(self.Cth[0, 0])
        self.zstar, self.consts = zstar, consts

    def Kb(self, b):
        return math.exp(2.0 * b / 3.0 * self.lnE)

    def pbar(self, b):
        return self.Kb(b) * self.mu

    def V(self, b):
        k = self.Kb(b)
        if not self.s5:
            return (k * self.sigma_bg) ** 2
        g = k * (np.array([1.0, 0.0, 0.0]) + self.theta[0] * (2.0 * b / 3.0) * self.gl)
        return float(g @ self.Cth @ g)

    def V_vec(self, bs):
        bs = np.asarray(bs, float)
        k = np.exp(2.0 * bs / 3.0 * self.lnE)
        if not self.s5:
            return (k * self.sigma_bg) ** 2
        e0 = np.array([1.0, 0.0, 0.0])
        g = k[:, None] * (e0[None, :] + self.theta[0] * (2.0 * bs / 3.0)[:, None] * self.gl[None, :])
        return np.einsum("ni,ij,nj->n", g, self.Cth, g)

    def K_at_theta(self, b=None):
        """K recalculado com o theta_hat do PROPRIO fundo (sensibilidade, nao entra na previsao pre-registrada)."""
        b = self.beta if b is None else b
        E, Om, Orad = e_lcdm(self.zstar, *self.theta, self.consts)
        return E ** (2.0 * b / 3.0), E, Om, Orad


# ------------------------------------------------------------------ verossimilhanca marginal
def marg_lnl(y, C, pbar, V, ft):
    ft = np.asarray(ft, float)
    y = np.asarray(y, float)
    S = C + V * np.outer(ft, ft)
    r = y - pbar * ft
    try:
        L = np.linalg.cholesky(S)
    except np.linalg.LinAlgError as e:
        raise StatsError("S nao positivo-definida") from e
    z = np.linalg.solve(L, r)
    q = float(z @ z)
    logdet = 2.0 * float(np.log(np.diag(L)).sum()) + len(y) * math.log(2 * math.pi)
    return -0.5 * (q + logdet), q


def marg_lnl_batch(y, C, pbars, Vs, fts):
    """Versao em lote de marg_lnl: pbars (nb,), Vs (nb,), fts (nb,n) -> lnL (nb,)."""
    y = np.asarray(y, float)
    n = len(y)
    pbars, Vs, fts = np.asarray(pbars, float), np.asarray(Vs, float), np.asarray(fts, float)
    S = C[None, :, :] + Vs[:, None, None] * (fts[:, :, None] * fts[:, None, :])
    r = y[None, :] - pbars[:, None] * fts
    try:
        L = np.linalg.cholesky(S)
    except np.linalg.LinAlgError as e:
        raise StatsError("S nao positivo-definida (lote)") from e
    z = np.linalg.solve(L, r[:, :, None])[:, :, 0]
    q = np.sum(z * z, axis=1)
    logdet = 2.0 * np.sum(np.log(np.diagonal(L, axis1=1, axis2=2)), axis=1) + n * math.log(2 * math.pi)
    return -0.5 * (q + logdet)


def beta_profile(ell, lo=PRIOR_BETA[0], hi=PRIOR_BETA[1], ngrid=401, ell_vec=None):
    bs = np.linspace(lo, hi, ngrid)
    vals = np.asarray(ell_vec(bs)) if ell_vec is not None else np.array([ell(b) for b in bs])
    i = int(np.argmax(vals))
    a, b = bs[max(i - 1, 0)], bs[min(i + 1, ngrid - 1)]
    res = optimize.minimize_scalar(lambda t: -ell(t), bounds=(a, b), method="bounded", options={"xatol": 1e-13})
    bhat, Lmax = float(res.x), float(-res.fun)
    if vals[i] > Lmax:
        bhat, Lmax = float(bs[i]), float(vals[i])
    edge = bool(bhat <= lo + 1e-6 or bhat >= hi - 1e-6)

    def side(bound):
        g = lambda t: ell(t) - (Lmax - 0.5)
        if g(bound) > 0:
            return None
        return abs(optimize.brentq(g, min(bhat, bound), max(bhat, bound), xtol=1e-15, rtol=1e-13) - bhat)

    sm, sp = side(lo), side(hi)
    sig = 0.5 * (sm + sp) if (sm is not None and sp is not None) else None
    return {"beta_hat": bhat, "lnL_max": Lmax, "side_minus": sm, "side_plus": sp, "sigma_beta": sig, "at_prior_edge": edge}


def ln_evidence_uniform(fn, lo, hi, n, fn_vec=None):
    x, w = np.polynomial.legendre.leggauss(n)
    t = 0.5 * (hi - lo) * x + 0.5 * (hi + lo)
    v = np.asarray(fn_vec(t)) if fn_vec is not None else np.array([fn(float(ti)) for ti in t])
    return float(logsumexp(v, b=w / 2.0))


def ln_mass_in_prior(rhat, s, lo, hi, n):
    """ln da massa do posterior gaussiano de r_d dentro do prior [lo, hi], por GL n-pontos (truncamento do Laplace)."""
    x, w = np.polynomial.legendre.leggauss(n)
    t = 0.5 * (hi - lo) * x + 0.5 * (hi + lo)
    dens = np.exp(-0.5 * ((t - rhat) / s) ** 2) / (s * math.sqrt(2 * math.pi))
    return math.log(float(np.sum(w * dens) * 0.5 * (hi - lo)))


def signed_sqrt(x):
    return math.copysign(math.sqrt(abs(x)), x)


def gls_dispersion(C, y):
    n = len(y)
    w, sc = gls_weights(C)
    m = float(w @ np.asarray(y, float))
    r = np.asarray(y, float) - m
    chi2 = float(r @ np.linalg.solve(C, r))
    if n > 1:
        return {"mean": m, "sigma_comb": sc, "chi2_int": chi2, "chi2_por_gl": chi2 / (n - 1), "p": float(sps.chi2.sf(chi2, n - 1)), "n": n}
    return {"mean": m, "sigma_comb": sc, "chi2_int": 0.0, "chi2_por_gl": 0.0, "p": 1.0, "n": n}


def endpoint_statistics(y, ids, C, law, bgfree, check_quadrature=True, fast=False):
    """Todas as estatisticas do executor em UM ponto da caixa de covariancia. y = centros locais (na ordem de ids).
    fast=True (so simulacao): pula a conferencia n=200; o modo observado NUNCA usa fast."""
    y = np.asarray(y, float)
    n = len(y)
    one = np.ones(n)
    cef = np.array([1.0 if i in CEPHEID_IDS else 0.0 for i in ids])
    lT, qT = marg_lnl(y, C, law.K * law.mu, law.V(law.beta), one)
    lL, qL = marg_lnl(y, C, law.mu, law.V(0.0), one)
    ell = lambda b: marg_lnl(y, C, law.pbar(b), law.V(b), one)[0]
    ell_vec = lambda bs: marg_lnl_batch(y, C, law.mu * np.exp(2.0 * np.asarray(bs) / 3.0 * law.lnE), law.V_vec(bs), np.ones((len(bs), n)))
    prof = beta_profile(ell, ell_vec=ell_vec, ngrid=201 if fast else 401)
    z_delta = None if prof["sigma_beta"] is None else (prof["beta_hat"] - law.beta) / prof["sigma_beta"]
    V0 = law.V(0.0)
    ell_s_vec = lambda ss: marg_lnl_batch(y, C, np.full(len(ss), law.mu), np.full(len(ss), V0), 1.0 + np.asarray(ss)[:, None] * cef[None, :])
    ns = (QUAD_N,) if fast else (QUAD_N, QUAD_CHECK_N)
    zb = {k: ln_evidence_uniform(None, *PRIOR_BETA, k, fn_vec=ell_vec) for k in ns}
    zs = {k: (ln_evidence_uniform(None, *PRIOR_SHIFT, k, fn_vec=ell_s_vec) if cef.any() else lL) for k in ns}
    f = bgfree
    LF, _ = marg_lnl(y, C, f["H0"], f["sigma_H0"] ** 2, one)
    mass = {k: ln_mass_in_prior(f["r_d"], f["sigma_r_d"], f["prior_rd_Mpc"][0], f["prior_rd_Mpc"][1], k) for k in ns}
    zf = {k: LF + f["lnZ_bg_ratio_laplace"] + mass[k] for k in ns}
    diffs = {}
    if not fast:
        diffs = {"beta_livre": abs(zb[QUAD_N] - zb[QUAD_CHECK_N]), "shift": abs(zs[QUAD_N] - zs[QUAD_CHECK_N]),
                 "fundo_livre_massa": abs(mass[QUAD_N] - mass[QUAD_CHECK_N])}
        if check_quadrature and any(not (v <= QUAD_TOL) for v in diffs.values()):
            raise QuadratureUnstable("E3: quadraturas 100/200 discordam alem de %.1e: %r -- RECUSA, sem veredito" % (QUAD_TOL, diffs))
    disp = gls_dispersion(C, y)
    out = {
        "lnL_TGL": lT, "lnL_LCDM": lL, "chi2_TGL": qT, "chi2_LCDM": qL,
        "z_disc": signed_sqrt(qL - qT), "z_disc_logdet_ao_lado": signed_sqrt(2.0 * (lT - lL)),
        "beta": prof, "z_delta": z_delta,
        "lnB_lcdm": lT - lL,
        "lnB_livre": lT - zb[QUAD_N], "lnB_shift": lT - zs[QUAD_N], "lnB_fundo_livre": lT - zf[QUAD_N],
        "quadratura_diferencas": diffs, "dispersao": disp,
    }
    if not fast:
        out.update({"lnB_livre_n200": lT - zb[QUAD_CHECK_N], "lnB_shift_n200": lT - zs[QUAD_CHECK_N], "lnB_fundo_livre_n200": lT - zf[QUAD_CHECK_N]})
    return out


# ------------------------------------------------------------------ poder so com sigma
def power_sigma_only(K, mu, sigma_comb, V_pred):
    """D = (K-1) mu / sqrt(sigma_comb^2 + V_pred); V_pred = (K sigma_bg)^2 na formula pre-registrada, ou a variancia S5."""
    return (K - 1.0) * mu / math.sqrt(sigma_comb ** 2 + V_pred)
