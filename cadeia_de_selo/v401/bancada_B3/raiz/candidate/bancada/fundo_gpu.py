# -*- coding: utf-8 -*-
"""fundo_gpu.py -- o FUNDO V3 da TGL em LOTE, na GPU (PyTorch/CUDA, float64), com a mesma matemática do worker selado
tgl_camb_worker_v3.py (sha256 72032b3a...):

    Φ_total(a) = 1 + β |1 + w_eff(a)|,   E²(a) = ρ(a) + β J(a) + c,   J(a) = ∫_a^∞ 3 (ρ+p)² / (ρ ã) dã,
    fecho E(a = 1) = 1 (Ω_Λ pela raiz de Ω_r + Ω_m + Ω_Λ + β J(1) + c = 1).

NUMÉRICA (declarada; a validação mede, não supõe):
  * grade uniforme em x = ln a com N pontos (N = 4k + 1); integrais CUMULATIVAS de ordem 4 (Simpson composto obtido por extrapolação de
    Richardson dos trapézios em h e 2h) em dois níveis: J nos nós pares; D_M e r_s nos nós múltiplos de 4;
  * valores em pontos arbitrários (os z do BAO, z*, z_drag) por interpolação de Lagrange CÚBICA nos nós;
  * Ω_Λ pelo ponto fixo Ω_Λ ← 1 − Ω_r − Ω_m − c − β J1(Ω_Λ) (contração: |β ∂J1/∂Ω_Λ| ≪ 1), J1 por Simpson;
  * o ΛCDM de referência (β = 0, c = 0) tem E² = ρ exatamente: não precisa de J.
O worker selado usa trapézios em grades de 400 001 / 20 001 / 60 001 pontos; a diferença entre os dois é MEDIDA em ferramentas/diagnostico_fundo.py.
O CAMB entra só via a tabela (camb_tabela.py): r_s e r_drag da TGL = valor do CAMB × (integral TGL / integral ΛCDM), como no worker.
"""
import math

import torch

C_KMS = 299792.458
X_MIN = -math.log(1.0 + 1.0e8)
X_MAX = math.log(1.0e3)


def omega_r_h2(TCMB=2.7255, Neff=3.046):
    og = 4.4814e-7 * TCMB ** 4
    return og * (1.0 + Neff * (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)), og


def _cum_simpson(f, h, reverso=False):
    """Integral cumulativa de ordem 4 de f (B,N), N ímpar, nos nós PARES: devolve (B,(N+1)/2).
    direto: ∫_{x0}^{x_{2k}};  reverso: ∫_{x_{2k}}^{x_{N-1}}."""
    if reverso:
        f = torch.flip(f, [1])
    tf = torch.zeros_like(f)
    tf[:, 1:] = torch.cumsum(0.5 * (f[:, 1:] + f[:, :-1]), 1) * h
    fe = f[:, ::2]
    tc = torch.zeros_like(fe)
    tc[:, 1:] = torch.cumsum(0.5 * (fe[:, 1:] + fe[:, :-1]), 1) * (2.0 * h)
    out = (4.0 * tf[:, ::2] - tc) / 3.0
    return torch.flip(out, [1]) if reverso else out


def _interp_cubico(v, x0, h, alvo):
    """Lagrange cúbico de v (B,M) em nós uniformes x0 + k h, nos alvos (B,K)."""
    M = v.shape[1]
    pos = (alvo - x0) / h
    base = torch.clamp(torch.floor(pos).long() - 1, 0, M - 4)
    t = pos - base.to(pos.dtype)
    idx = base[..., None] + torch.arange(4, device=v.device)
    vv = torch.gather(v, 1, idx.reshape(v.shape[0], -1)).reshape(idx.shape)
    w0 = -(t - 1) * (t - 2) * (t - 3) / 6.0
    w1 = t * (t - 2) * (t - 3) / 2.0
    w2 = -t * (t - 1) * (t - 3) / 2.0
    w3 = t * (t - 1) * (t - 2) / 6.0
    return vv[..., 0] * w0 + vv[..., 1] * w1 + vv[..., 2] * w2 + vv[..., 3] * w3


class FundoV3Lote:
    """Calcula, para um LOTE de pontos (tensores (B,)), os observáveis do fundo V3 (e do ΛCDM de referência)."""

    def __init__(self, dispositivo="cuda", n_grade=20001, n_j1=4001, mnu=0.06, TCMB=2.7255, Neff=3.046):
        n_grade = int(n_grade)
        if (n_grade - 1) % 4:
            raise ValueError("n_grade tem de ser 4k + 1")
        if (int(n_j1) - 1) % 2:
            raise ValueError("n_j1 tem de ser ímpar")
        self.dev = torch.device(dispositivo)
        self.dt = torch.float64
        self.n = n_grade
        self.h = (X_MAX - X_MIN) / (self.n - 1)
        self.x = torch.linspace(X_MIN, X_MAX, self.n, device=self.dev, dtype=self.dt)
        self.x2 = self.x[::2]
        self.x4 = self.x[::4]
        self.ea4 = torch.exp(-4.0 * self.x); self.ea3 = torch.exp(-3.0 * self.x)
        self.xs = torch.linspace(0.0, X_MAX, int(n_j1), device=self.dev, dtype=self.dt)
        self.hs = X_MAX / (int(n_j1) - 1)
        self.es4 = torch.exp(-4.0 * self.xs); self.es3 = torch.exp(-3.0 * self.xs)
        self.mnu, self.TCMB, self.Neff = mnu, TCMB, Neff
        self.orh2, self.ogh2 = omega_r_h2(TCMB, Neff)
        self.tail_fator = 3.0 * math.exp(-6.0 * X_MAX) / 6.0
        w = torch.ones(int(n_j1), device=self.dev, dtype=self.dt)        # pesos de Simpson para J1
        w[1:-1:2] = 4.0; w[2:-1:2] = 2.0
        self.w_simpson = w * self.hs / 3.0

    def _dens(self, Or, Om, OL, e4, e3):
        rho = Or[:, None] * e4 + Om[:, None] * e3 + OL[:, None]
        rpp = (4.0 / 3.0) * Or[:, None] * e4 + Om[:, None] * e3
        return rho, rpp

    def _J1(self, Or, Om, OL):
        rho, rpp = self._dens(Or, Om, OL, self.es4, self.es3)
        return (3.0 * rpp * rpp / rho) @ self.w_simpson + self.tail_fator * Om ** 2 / OL

    def _fecho(self, Or, Om, beta, c, iters=16):
        """Ponto fixo sem sincronizar a GPU a cada passo: 16 iterações de uma contração de fator |β ∂J1/∂Ω_Λ| ≪ 1 (o resíduo final é
        devolvido e conferido pela validação)."""
        OL = 1.0 - Or - Om - c
        if not bool(torch.any(beta != 0)):
            return OL, torch.zeros_like(OL)
        for _ in range(iters):
            OL = 1.0 - Or - Om - c - beta * self._J1(Or, Om, OL)
        return OL, Or + Om + OL + beta * self._J1(Or, Om, OL) + c - 1.0

    def fundo(self, H0, ombh2, omch2, beta, c):
        """Devolve dict com E nos nós pares e as integrais cumulativas de D_M e r_s nos nós múltiplos de 4."""
        h2 = (H0 / 100.0) ** 2
        Or = self.orh2 / h2
        Om = (ombh2 + omch2 + self.mnu / 93.14) / h2
        OL, res = self._fecho(Or, Om, beta, c)
        lcdm = not bool(torch.any(beta != 0)) and not bool(torch.any(c != 0))
        if lcdm:
            rho2, rpp2 = self._dens(Or, Om, OL, self.ea4[::2], self.ea3[::2])
            E2 = rho2
        else:
            rho, rpp = self._dens(Or, Om, OL, self.ea4, self.ea3)
            J = _cum_simpson(3.0 * rpp * rpp / rho, self.h, reverso=True) + (self.tail_fator * Om ** 2 / OL)[:, None]
            rho2, rpp2 = rho[:, ::2], rpp[:, ::2]
            del rho, rpp
            E2 = rho2 + beta[:, None] * J + c[:, None]
            del J
        if not bool(torch.all(E2 > 0)):
            raise ValueError("E^2 <= 0 na grade")
        E = torch.sqrt(E2)
        Phi = 1.0 + beta[:, None] * rpp2 / rho2
        h2g = 2.0 * self.h
        ex = torch.exp(-self.x2)[None, :]
        Cdm = _cum_simpson(ex / E, h2g)                                        # ∫_{X_MIN}^{x} e^{-x}/E, nós ×4
        Rb = 3.0 * ombh2[:, None] * torch.exp(self.x2)[None, :] / (4.0 * self.ogh2)
        Crs = _cum_simpson((C_KMS / torch.sqrt(3.0 * (1.0 + Rb))) * ex / (H0[:, None] * E), h2g)
        i0 = int(round((0.0 - X_MIN) / (4.0 * self.h)))
        return dict(E=E, Phi=Phi, rho2=rho2, rpp2=rpp2, Om=Om, OL=OL, res_fecho=res, Cdm=Cdm, Crs=Crs, H0=H0,
                    C0=_interp_cubico(Cdm, X_MIN, 4.0 * self.h, torch.zeros_like(H0)[:, None])[:, 0])

    def DM(self, fd, z):
        """D_M (Mpc) nos redshifts z (B,K): (c/H0) ∫_{-ln(1+z)}^{0} e^{-x}/E dx."""
        Cz = _interp_cubico(fd["Cdm"], X_MIN, 4.0 * self.h, -torch.log1p(z))
        return C_KMS / fd["H0"][:, None] * (fd["C0"][:, None] - Cz)

    def DM_com_boost(self, fd, z, logK2):
        """01/10/2026 (SH0ES): D_M (Mpc) com a taxa E multiplicada por exp(logK2) nos nós pares (logK2: (B, N2)) -- a lei ACUMULADA nas distâncias,
        D_M = (c/H0) ∫ e^{-x} dx / (E·K): o mesmo integrador cumulativo de `fundo`, com o fator da lei dentro."""
        E2 = fd["E"] * torch.exp(logK2)
        ex = torch.exp(-self.x2)[None, :]
        Cdm = _cum_simpson(ex / E2, 2.0 * self.h)
        C0 = _interp_cubico(Cdm, X_MIN, 4.0 * self.h, torch.zeros_like(fd["H0"])[:, None])[:, 0]
        Cz = _interp_cubico(Cdm, X_MIN, 4.0 * self.h, -torch.log1p(z))
        return C_KMS / fd["H0"][:, None] * (C0[:, None] - Cz)

    def Ez(self, fd, z):
        return _interp_cubico(fd["E"], X_MIN, 2.0 * self.h, -torch.log1p(z))

    def rs_int(self, fd, z_lo):
        """∫ de a = 1e-8 até a(z_lo) de c_s dz/H -- a integral do horizonte sonoro, (B,)."""
        return _interp_cubico(fd["Crs"], X_MIN, 4.0 * self.h, -torch.log1p(z_lo)[:, None])[:, 0]

    def residuo_segunda(self, fd):
        """d(E²)/dx + 3Φ(ρ+p) = 0, conferido no passado físico (autoverificação do worker), nos nós pares."""
        E2 = fd["E"] ** 2
        dE2 = torch.gradient(E2, spacing=(self.x2,), dim=1)[0]
        alvo = -3.0 * fd["Phi"] * fd["rpp2"]
        i0 = int(round((0.0 - X_MIN) / (2.0 * self.h)))
        sl = slice(11, i0 + 1)
        return torch.max(torch.abs(dE2[:, sl] - alvo[:, sl]) / torch.abs(alvo[:, sl]), dim=1).values
