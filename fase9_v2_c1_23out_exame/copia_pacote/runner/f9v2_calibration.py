# -*- coding: utf-8 -*-
"""f9v2_calibration.py -- CALIBRACAO DE CAUDA do z_delta e do z_disc: o «5 sigma» da Fase 9 V2 tem de ser um p CALIBRADO, nao a raiz do qui-quadrado.

Reducao exata (fundo marginalizado, f = 1): todas as hipoteses sem shift dependem de y so por m = media GLS (peso w do ponto de analise) e pelo
chi2_int, que nao depende de b. Entao, a menos de uma constante:
    ell(b; m) = -1/2 [ (m - P_b)^2 / (sigma_c^2 + V_b) + ln(sigma_c^2 + V_b) ],   P_b = K_b mu,  V_b = variancia da previsao (S5).
Logo z_delta e' uma funcao DETERMINISTICA de u = m - K mu, e z_disc de x = m - mu (forma fechada, quadratica). Sob a nula,
    TGL verdadeira:   u ~ N(0, tau_f^2),  tau_f^2 = sup_grade Var(w_min' y | C_verdadeira) + V_T     (falsificacao: ponto de MENOR sigma_comb)
    LCDM verdadeira:  x ~ N(0, tau_d^2),  tau_d^2 = sup_grade Var(w_max' y | C_verdadeira) + V_L     (discriminacao: ponto de MAIOR sigma_comb)
O sup sobre a grade de covariancia e' a SISTEMATICA (a caixa nao e' medida); a nula sem sistematica e' o caso C_verdadeira = C_analise.
p_cal -> z_cal por Phi^{-1}: dois lados para |z_delta| (p/2), um lado para z_disc. Para um estimador linear-gaussiano z_cal = z; onde a
estatistica nao e' linear (perfil com log-det, forma quadratica de variancias diferentes) z_cal != z, e e' z_cal que a funcao de veredito le.
A reducao e' VERIFICADA contra o pipeline completo por simulacao (calibracao/rodar_calibracao.py).
"""
import math

import numpy as np
from scipy import optimize
from scipy import stats as sps

import f9v2_stats as S


def zdelta_of_m(m, sigma_c, law):
    """z_delta do pipeline completo reduzido a m (None se o perfil nao fecha / beta_hat na borda). Mesmo beta_profile do executor."""
    def ell(b):
        s2 = sigma_c ** 2 + law.V(b)
        return -0.5 * ((m - law.pbar(b)) ** 2 / s2 + math.log(s2))

    def ell_vec(bs):
        bs = np.asarray(bs, float)
        s2 = sigma_c ** 2 + law.V_vec(bs)
        return -0.5 * ((m - law.mu * np.exp(2.0 * bs / 3.0 * law.lnE)) ** 2 / s2 + np.log(s2))

    prof = S.beta_profile(ell, ell_vec=ell_vec)
    if prof["sigma_beta"] is None or prof["at_prior_edge"]:
        return None
    return (prof["beta_hat"] - law.beta) / prof["sigma_beta"]


class ZDeltaMap:
    """u -> z_delta, em grade; p_cal bilateral sob u ~ N(0, tau^2)."""

    def __init__(self, sigma_c, law, half_range=16.0, step=0.1):
        self.sigma_c, self.law = sigma_c, law
        self.centre = law.K * law.mu
        self.u = np.arange(-half_range, half_range + 1e-9, step)
        self.f = np.array([np.nan if (z := zdelta_of_m(self.centre + ui, sigma_c, law)) is None else z for ui in self.u])
        ok = np.isfinite(self.f)
        if ok.sum() < 20:
            raise S.StatsError("mapa z_delta(u) quase vazio")
        d = np.diff(self.f[ok])
        self.monotone = bool(np.all(d > 0))
        self.u_ok, self.f_ok = self.u[ok], self.f[ok]

    def z_of_u(self, u):
        z = zdelta_of_m(self.centre + u, self.sigma_c, self.law)
        return float("nan") if z is None else z

    def root(self, t, refine=True):
        """u tal que z_delta(u) = t (t pode ser negativo). Devolve (u, extrapolado)."""
        f, u = self.f_ok, self.u_ok
        if t < f[0]:
            return float(u[0]), True
        if t > f[-1]:
            return float(u[-1]), True
        u0 = float(np.interp(t, f, u))
        if not refine:
            return u0, False
        i = int(np.searchsorted(f, t))
        a, b = float(u[max(i - 1, 0)]), float(u[min(i, len(u) - 1)])
        try:
            g = lambda x: self.z_of_u(x) - t
            if g(a) * g(b) < 0:
                return float(optimize.brentq(g, a, b, xtol=1e-12)), False
        except (ValueError, RuntimeError):
            pass
        return u0, False

    def p_two_sided(self, t, tau, refine=True):
        t = abs(t)
        u_hi, ex1 = self.root(+t, refine)
        u_lo, ex2 = self.root(-t, refine)
        p = float(sps.norm.sf(u_hi / tau) + sps.norm.sf(-u_lo / tau))
        return min(1.0, p), bool(ex1 or ex2)

    def z_cal(self, raw, tau, refine=True):
        if raw is None or not math.isfinite(raw):
            return raw
        p, ex = self.p_two_sided(abs(raw), tau, refine)
        zc = float(sps.norm.isf(min(max(p, 1e-300), 1.0) / 2.0))
        return math.copysign(zc, raw)


class ZDiscMap:
    """x = m - mu; Delta_q(x) = x^2/A - (x-d)^2/B, A = sigma_c^2 + V_L, B = sigma_c^2 + V_T, d = (K-1) mu. p unilateral sob x ~ N(0, tau^2)."""

    def __init__(self, sigma_c, law):
        self.A = sigma_c ** 2 + law.V(0.0)
        self.B = sigma_c ** 2 + law.V(law.beta)
        self.d = (law.K - 1.0) * law.mu

    def dq(self, x):
        return x * x / self.A - (x - self.d) ** 2 / self.B

    def z_raw(self, x):
        return S.signed_sqrt(self.dq(x))

    def p_one_sided(self, t, tau):
        """P(z_disc >= t | LCDM), t >= 0: Delta_q >= t^2 => x <= x1 ou x >= x2 (a e' menor que 1/A - 1/B > 0, parabola para cima)."""
        a = 1.0 / self.A - 1.0 / self.B
        b = 2.0 * self.d / self.B
        c = -self.d ** 2 / self.B - t * t
        disc = b * b - 4 * a * c
        r = math.sqrt(disc)
        x1, x2 = (-b - r) / (2 * a), (-b + r) / (2 * a)
        return float(sps.norm.cdf(x1 / tau) + sps.norm.sf(x2 / tau))

    def z_cal(self, raw, tau):
        if raw is None or not math.isfinite(raw):
            return raw
        if raw <= 0:
            return raw
        p = min(max(self.p_one_sided(raw, tau), 1e-300), 1.0)
        return float(sps.norm.isf(p))


def taus(amps, sigmas, ids, ep, law, grid_n, grid_t):
    """tau_f (falsificacao, ponto de menor sigma_comb) e tau_d (discriminacao, ponto de maior), com e sem a sistematica da caixa."""
    VT, VL = law.V(law.beta), law.V(0.0)
    wmin, wmax = ep["minimum"]["weights"], ep["maximum"]["weights"]
    smin, amin = S.max_variance_of_estimator(amps, sigmas, ids, wmin, grid_n, grid_t)
    smax, amax = S.max_variance_of_estimator(amps, sigmas, ids, wmax, grid_n, grid_t)
    own_min = float(wmin @ ep["minimum"]["covariance"] @ wmin)
    own_max = float(wmax @ ep["maximum"]["covariance"] @ wmax)
    return {
        "tau_f_sup": math.sqrt(smin + VT), "tau_f_sup_em": {"lambda_N": amin[0], "lambda_T": amin[1]},
        "tau_f_proprio": math.sqrt(own_min + VT),
        "tau_d_sup": math.sqrt(smax + VL), "tau_d_sup_em": {"lambda_N": amax[0], "lambda_T": amax[1]},
        "tau_d_proprio": math.sqrt(own_max + VL),
        "V_T": VT, "V_L": VL,
    }


def threshold_equivalents(zmap, zdisc, tau_f, tau_d):
    """Limiares BRUTOS equivalentes aos limiares calibrados (3 e 5 sigma): o score bruto cujo p_cal iguala o p gaussiano."""
    out = {}
    for k in (3.0, 5.0):
        p2 = 2.0 * sps.norm.sf(k)
        p1 = sps.norm.sf(k)
        g = lambda t: zmap.p_two_sided(t, tau_f, refine=False)[0] - p2
        h = lambda t: zdisc.p_one_sided(t, tau_d) - p1
        try:
            tf = optimize.brentq(g, 0.5, 15.0, xtol=1e-6)
        except ValueError:
            tf = float("nan")
        try:
            td = optimize.brentq(h, 0.05, 30.0, xtol=1e-6)
        except ValueError:
            td = float("nan")
        out["z_delta_bruto_para_%dsigma_calibrado" % int(k)] = tf
        out["z_disc_bruto_para_%dsigma_calibrado" % int(k)] = td
    return out


def primary_thresholds(spec, bgd, mode, consts=None):
    """Limiares brutos equivalentes (P_primaria x BG1) com o fundo `bgd` (saida do fornecedor): a MESMA conta que o runner faz ao vivo e que o recibo guarda.
    mode 'bruto' usa os taus 'proprio'. Usado pelo script de calibracao, pelo runner (guarda) e pelos testes (pacote sintetico)."""
    import math as _m
    lei = spec["lei"]
    consts = consts or {k: v for k, v in spec["S5_propagacao"]["constantes_E"].items() if k != "origem"}
    beta = spec["beta"]["alpha_read"] * _m.sqrt(_m.e)
    law = S.Law(beta, lei["K_frozen_V1"], S.lnE_pinned(lei["Omega_m"], lei["Omega_r"], lei["z_star"]), bgd["bg1"]["H0"], bgd["bg1"]["cov_theta"],
                bgd["bg1"]["theta_H0_ombh2_omch2"], lei["z_star"], consts, s5=bool(spec["S5_propagacao"]["habilitado"]))
    ids = spec["familias"]["P_primaria"]["ids"]
    sig = {k: v["sigma"] for k, v in spec["leitores"].items()}
    grid = spec["covariancia"]["grid"]
    ep = S.grid_endpoints(spec["covariancia"]["amplitudes_km_s_Mpc"], sig, ids, grid["lambda_N"], grid["lambda_T"])
    tau = taus(spec["covariancia"]["amplitudes_km_s_Mpc"], sig, ids, ep, law, grid["lambda_N"], grid["lambda_T"])
    sup = mode == "sup_caixa"
    return threshold_equivalents(ZDeltaMap(ep["minimum"]["sigma_comb"], law), ZDiscMap(ep["maximum"]["sigma_comb"], law),
                                 tau["tau_f_sup" if sup else "tau_f_proprio"], tau["tau_d_sup" if sup else "tau_d_proprio"])
