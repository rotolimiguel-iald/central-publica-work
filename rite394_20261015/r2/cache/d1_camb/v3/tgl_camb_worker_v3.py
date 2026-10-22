# -*- coding: utf-8 -*-
"""
tgl_camb_worker_v3.py — o fundo da V3 do D1 (protocolo D1_CAMB_V3, pré-registrado na v363, hash d5c35ea6d20b76eb).

A ROTA [INPUT por repasse; confirmação de uma linha do operador PENDENTE]: fator sobre o fluido TOTAL, com o vácuo na composição,
    Φ_total(a) = 1 + β |1 + w_eff(a)|,   w_eff = p_total / ρ_total  (radiação, matéria e vácuo somados).
AS EQUAÇÕES (não é o H² = (8πG/3)Φρ do worker da V2):
    segunda:  dH/dt = −4πG Φ_total (ρ + p)
    primeira, por primitiva (teorema do kernel `tgl_first_friedmann_from_primitive`):  H² = (8πG/3) P + C,  dP/da = Φ_total dρ/da.
A NORMALIZAÇÃO DA PRIMITIVA [DECLARADA AQUI, ANTES DE QUALQUER DADO]: P(a → ∞) = ρ_Λ, isto é,
    P(a) = ρ(a) + β J(a),   J(a) = ∫_a^∞ 3 (ρ+p)² / (ρ ã) dã,
de modo que C = 0 significa «a assíntota de de Sitter não é tocada por β» (Φ(w = −1) = 1: a fronteira silenciosa). Com esta escolha,
na era da radiação P → (1 + 4β/3) ρ e na da matéria P → (1 + β) ρ — os limites de w constante (`tgl_first_friedmann_constant_w`).
Qualquer outra normalização é um deslocamento de C; «C livre» é a sensibilidade pré-registrada.
O FECHO: H(a = 1) = H0 exatamente (Ω_Λ resolvido por raiz de Ω_r + Ω_m + Ω_Λ + βJ(1) + c = 1, c = C/H0²). Diferença declarada para a V2:
lá o parâmetro H0 dava H(0) = H0·√Φ(0).
O CAMB entra só onde a V2 o usava: z*, z_drag, r*, r_drag e D_A(z*) de ΛCDM com os mesmos (H0, ω_b, ω_c). r_s e r_drag da TGL vêm da
INTEGRAL de c_s/H em u = ln(1+z) (razão TGL/ΛCDM das integrais sobre o valor do CAMB), não de reescala de época única.
AUTOVERIFICAÇÕES gravadas em cada chamada: (1) DM_TGL(β = 0)/DM_CAMB (limite 5e-3, RELIDO pelo pipeline); (2) resíduo da SEGUNDA equação
d(E²)/du + 3Φ(ρ+p) = 0 na grade; (3) E(z = 0) = 1.
"""
import sys, json
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import cumulative_trapezoid

C_KMS = 299792.458
X_MIN = -np.log(1.0 + 1.0e8)     # a = 1/(1+1e8)
X_MAX = np.log(1.0e3)            # a = 1000 (cauda analítica acima)
NGRID = 400001


def _omega_r_h2(TCMB=2.7255, Neff=3.046):
    og = 4.4814e-7 * TCMB ** 4
    return og * (1.0 + Neff * (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)), og


class FundoV3:
    """E(a) = H/H0 da rota do fator total por primitiva. x = ln a."""

    def __init__(self, H0, ombh2, omch2, beta, c=0.0, mnu=0.06, TCMB=2.7255, Neff=3.046):
        self.H0, self.beta, self.c = float(H0), float(beta), float(c)
        h2 = (self.H0 / 100.0) ** 2
        orh2, self.ogh2 = _omega_r_h2(TCMB, Neff)
        self.Or = orh2 / h2
        self.Om = (ombh2 + omch2 + mnu / 93.14) / h2
        self.ombh2 = float(ombh2)
        self.OL = self._fecho()
        self.x = np.linspace(X_MIN, X_MAX, NGRID)
        rho, rpp = self._rho_rpp(self.x, self.OL)
        g = 3.0 * rpp * rpp / rho
        tail = 3.0 * (self.Om ** 2) * np.exp(-6.0 * X_MAX) / (6.0 * self.OL)
        # acumulação DO FUTURO PARA O PASSADO (estável: a acumulação a partir do passado perde a parte tardia por cancelamento em float64)
        cum_top = cumulative_trapezoid(g[::-1], self.x[::-1], initial=0.0)
        self.J = -cum_top[::-1] + tail
        self.rho, self.rpp = rho, rpp
        self.Phi = 1.0 + self.beta * rpp / rho
        self.E2 = rho + self.beta * self.J + self.c
        if not np.all(self.E2 > 0):
            raise ValueError('E^2 <= 0 na grade')
        self.E = np.sqrt(self.E2)

    def _rho_rpp(self, x, OL):
        a4 = np.exp(-4.0 * x); a3 = np.exp(-3.0 * x)
        rho = self.Or * a4 + self.Om * a3 + OL
        rpp = (4.0 / 3.0) * self.Or * a4 + self.Om * a3
        return rho, rpp

    def _J1(self, OL):
        xs = np.linspace(0.0, X_MAX, 40001)
        rho, rpp = self._rho_rpp(xs, OL)
        return float(np.trapezoid(3.0 * rpp * rpp / rho, xs)) + 3.0 * (self.Om ** 2) * np.exp(-6.0 * X_MAX) / (6.0 * OL)

    def _fecho(self):
        f = lambda OL: self.Or + self.Om + OL + self.beta * self._J1(OL) + self.c - 1.0
        return brentq(f, 1e-4, 1.5, xtol=1e-14, rtol=1e-14, maxiter=200)

    def residuo_segunda_equacao(self):
        # d(E²)/du + 3Φ(ρ+p) = 0 (u = -x) conferido por diferença central no passado físico (z >= 0), onde (ρ+p) não é desprezível
        dE2 = np.gradient(self.E2, self.x)
        alvo = -3.0 * self.Phi * self.rpp
        sl = (self.x <= 0.0) & (np.arange(self.x.size) > 10)
        return float(np.max(np.abs(dE2[sl] - alvo[sl]) / np.abs(alvo[sl])))

    def E_de_z(self, z):
        return np.interp(-np.log1p(np.asarray(z, float)), self.x, self.E)

    def DM(self, z):
        """D_M(z) = (c/H0) ∫_0^{ln(1+z)} (1+z)/E du, u = -x."""
        z = np.atleast_1d(np.asarray(z, float))
        out = []
        for zz in z:
            u = np.linspace(0.0, np.log1p(zz), 20001)
            E = np.interp(-u, self.x, self.E)
            out.append(C_KMS / self.H0 * float(np.trapezoid(np.exp(u) / E, u)))
        return np.array(out)

    def rs_integral(self, z_lo):
        u = np.linspace(np.log1p(z_lo), -X_MIN, 60001); z = np.expm1(u)
        Rb = 3.0 * self.ombh2 / (4.0 * self.ogh2 * (1.0 + z))
        cs = C_KMS / np.sqrt(3.0 * (1.0 + Rb))
        E = np.interp(-u, self.x, self.E)
        return float(np.trapezoid(cs * (1.0 + z) / (self.H0 * E), u))


def derivados(p):
    import camb
    beta = float(p['beta']); H0 = float(p['H0']); ombh2 = float(p['ombh2']); omch2 = float(p['omch2'])
    c = float(p.get('c', 0.0)); tau = float(p.get('tau', 0.0544)); ns = float(p.get('ns', 0.9649)); As = float(p.get('As', 2.1e-9))
    mnu = float(p.get('mnu', 0.06)); TCMB = float(p.get('TCMB', 2.7255)); Neff = float(p.get('Neff', 3.046))
    desi_z = list(p.get('desi_z', []))
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, mnu=mnu, tau=tau, TCMB=TCMB, nnu=Neff)
    pars.InitPower.set_params(ns=ns, As=As)
    pars.set_dark_energy(w=-1.0, wa=0.0)
    pars.set_for_lmax(20, lens_potential_accuracy=0)
    res = camb.get_background(pars)
    der = res.get_derived_params()
    z_star, z_drag = float(der['zstar']), float(der['zdrag'])
    rstar_camb, rdrag_camb = float(der['rstar']), float(der['rdrag'])
    DM_star_camb = float(res.angular_diameter_distance(z_star)) * (1.0 + z_star)

    tgl = FundoV3(H0, ombh2, omch2, beta, c=c, mnu=mnu, TCMB=TCMB, Neff=Neff)
    lcdm = tgl if (beta == 0.0 and c == 0.0) else FundoV3(H0, ombh2, omch2, 0.0, c=0.0, mnu=mnu, TCMB=TCMB, Neff=Neff)
    r_star = rstar_camb * tgl.rs_integral(z_star) / lcdm.rs_integral(z_star)
    r_drag = rdrag_camb * tgl.rs_integral(z_drag) / lcdm.rs_integral(z_drag)
    DM_star = float(tgl.DM(z_star)[0])
    selfcheck = float(lcdm.DM(z_star)[0]) / DM_star_camb
    Om = (ombh2 + omch2 + mnu / 93.14) / (H0 / 100.0) ** 2
    R = np.sqrt(Om) * H0 / C_KMS * DM_star
    lA = np.pi * DM_star / r_star
    H_desi = [float(H0 * tgl.E_de_z(z)) for z in desi_z]
    DM_desi = [float(v) for v in tgl.DM(desi_z)] if desi_z else []
    return dict(beta=beta, c=c, H0=H0, ombh2=ombh2, omch2=omch2, Omega_L=tgl.OL, Omega_m=Om, z_star=z_star, z_drag=z_drag,
                r_star_LCDM=rstar_camb, r_drag_LCDM=rdrag_camb, r_star_TGL=r_star, r_drag_TGL=r_drag,
                DM_star_LCDM=DM_star_camb, DM_star_TGL=DM_star, dm_selfcheck_ratio=selfcheck, R=float(R), lA=float(lA),
                desi_z=desi_z, H_at_DESI=H_desi, DM_at_DESI=DM_desi,
                E_at_z0=float(tgl.E_de_z(0.0)), second_friedmann_residual=tgl.residuo_segunda_equacao(),
                Phi_z0=float(np.interp(0.0, tgl.x, tgl.Phi)), P_over_rho_zstar=float(np.interp(-np.log1p(z_star), tgl.x, (tgl.E2 - tgl.c) / tgl.rho)))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Uso: python tgl_camb_worker_v3.py entrada.json saida.json', file=sys.stderr); sys.exit(2)
    p = json.load(open(sys.argv[1]))
    json.dump(derivados(p), open(sys.argv[2], 'w'), indent=1)
