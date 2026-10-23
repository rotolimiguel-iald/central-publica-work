# -*- coding: utf-8 -*-
"""f9v2_background.py -- E1/E2 da Fase 9 V2-c1: o FORNECEDOR REAL do fundo BG1 (nao mock) e a reproducao do fundo.

Porta, SEM mudar a conta, o R2 do runner V1 (Bancada_Um/investigacao/fase9_hubble_abertura/rodar_fase9_v1.py, sha16 f3108bc21dcad317):
  * BG1 = LCDM nu, Planck comprimido (Chen+2019) + DESI DR2, SEM escada (opcoes_de({"modo": "tgl"}) com beta = 0 => mapa efetivo = nu);
  * fundo-livre = o mesmo, com r_d livre U[130; 160] Mpc (Laplace; fator de Occam do prior de 30 Mpc).
Nenhum centro local de H0 entra aqui: so Planck comprimido + BAO. Importa torch e bancada.motor SOMENTE ao instanciar (o modo sintetico nao
precisa dele). Divergencia da reproducao INTERROMPE (BackgroundError); nunca calibra, nunca ajusta o fundo para bater com o pino.
"""
import hashlib
import math
import os
import sys

import numpy as np

BANCADA_ROOT = r"C:\IALD\Bancada_Um"
# arquivos da Bancada que formam o fornecedor (hash entra no PEDIDO_DE_CONGELAMENTO e e' conferido pelo runner antes de abrir)
BANCADA_FILES = ("bancada/motor.py", "bancada/fontes.py", "bancada/fundo_gpu.py", "bancada/camb_tabela.py",
                 "bancada/pantheon_cov.py", "bancada/regua.py", "tabelas/camb_lcdm_v1.npz")
PRIOR_RD = (130.0, 160.0)


class BackgroundError(RuntimeError):
    pass


def bancada_pins(root=BANCADA_ROOT):
    out = {}
    for rel in BANCADA_FILES:
        b = open(os.path.join(root, *rel.split("/")), "rb").read()
        out[rel] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    return out


class BancadaBackgroundProvider:
    """Fundo REAL. kind = 'BANCADA_REAL'."""
    kind = "BANCADA_REAL"

    def __init__(self, root=BANCADA_ROOT):
        if root not in sys.path:
            sys.path.insert(0, root)
        import torch  # noqa: E402
        from scipy import optimize  # noqa: E402
        from bancada.motor import Motor, opcoes_de  # noqa: E402
        self._torch = torch
        self._optimize = optimize
        self._M = Motor(root)
        self._O = opcoes_de({"modo": "tgl"})   # as opcoes da Fase 1/3 (chen2019, razao_camb); com beta = 0 o mapa eff = nu

    def _res_bg(self, x, rd_livre):
        torch, M, O = self._torch, self._M, self._O
        H0, wb, wc = x[0], x[1], x[2]
        th = torch.tensor([[H0, wb, wc, 0.0, 0.0]], dtype=torch.float64, device=M.dev)
        p = M.predizer(th, O)
        if not bool(p["dentro"][0]):
            return np.full(16, 1e6)
        rp = M._r_planck(p, O)[0]
        dr2 = p["dr2"][0] * (p["r_drag"][0] / x[3] if rd_livre else 1.0)
        rb = (dr2 - M.dr2_val) @ M.dr2_Linv.T
        return torch.cat([rp, rb]).cpu().numpy()

    def _ajuste(self, rd_livre, x0):
        lo = [60.0, 0.019, 0.08] + ([PRIOR_RD[0]] if rd_livre else [])
        hi = [80.0, 0.026, 0.16] + ([PRIOR_RD[1]] if rd_livre else [])
        f = lambda x: self._res_bg(x, rd_livre)
        r = self._optimize.least_squares(f, x0, bounds=(lo, hi), method="trf", x_scale="jac", diff_step=1e-6, xtol=1e-12, ftol=1e-12)
        J = r.jac
        C = np.linalg.inv(J.T @ J)
        return r.x, float(r.fun @ r.fun), C

    def compute(self):
        torch, M, O = self._torch, self._M, self._O
        xb, chi_b, Cb = self._ajuste(False, [68.53, 0.02253, 0.1182])
        th = torch.tensor([[xb[0], xb[1], xb[2], 0.0, 0.0]], dtype=torch.float64, device=M.dev)
        rd0 = float(M.predizer(th, O)["r_drag"][0])
        xr, chi_r, Cr = self._ajuste(True, [xb[0], xb[1], xb[2], min(max(rd0, 131.0), 159.0)])
        rd_no_limite = bool(xr[3] <= PRIOR_RD[0] + 1e-6 or xr[3] >= PRIOR_RD[1] - 1e-6)
        lnZ_ratio = (-0.5 * (chi_r - chi_b) + 0.5 * math.log(np.linalg.det(Cr) / np.linalg.det(Cb))
                     + 0.5 * math.log(2 * math.pi) - math.log(PRIOR_RD[1] - PRIOR_RD[0]))
        return {
            "kind": self.kind,
            "opcoes": dict(O),
            "bg1": {"H0": float(xb[0]), "sigma_H0": float(math.sqrt(Cb[0, 0])), "theta_H0_ombh2_omch2": [float(v) for v in xb],
                    "cov_theta": [[float(v) for v in row] for row in Cb], "chi2": chi_b},
            "r_d_modelo_no_BG1": rd0,
            "fundo_livre": {"H0": float(xr[0]), "sigma_H0": float(math.sqrt(Cr[0, 0])), "r_d": float(xr[3]), "sigma_r_d": float(math.sqrt(Cr[3, 3])),
                            "chi2": chi_r, "delta_chi2_vs_rd_fixo": chi_r - chi_b, "lnZ_bg_ratio_laplace": float(lnZ_ratio),
                            "r_d_no_limite": rd_no_limite, "prior_rd_Mpc": list(PRIOR_RD)},
        }


class SyntheticBackgroundProvider:
    """Fundo SINTETICO rotulado (so para testes). NUNCA aceito no modo observado (o runner confere kind)."""
    kind = "SYNTHETIC_GAUSSIAN_NOT_CAMB_OR_REAL_BACKGROUND"

    def __init__(self, H0=68.531, sigma=0.301, free_dH0=-0.4, free_sigma=0.6, rd=147.0, sigma_rd=3.5, lnZ=0.5, omega_b=0.02253, omega_c=0.1182,
                 corr_h0_wc=-0.8):
        self.H0, self.sigma, self.free_dH0, self.free_sigma = H0, sigma, free_dH0, free_sigma
        self.rd, self.sigma_rd, self.lnZ = rd, sigma_rd, lnZ
        self.omega_b, self.omega_c, self.corr = omega_b, omega_c, corr_h0_wc

    def compute(self):
        s = [self.sigma, 0.00015, 0.0010]
        cov = [[s[0] ** 2, 0.0, self.corr * s[0] * s[2]], [0.0, s[1] ** 2, 0.0], [self.corr * s[0] * s[2], 0.0, s[2] ** 2]]
        return {
            "kind": self.kind, "opcoes": {"synthetic": True},
            "bg1": {"H0": self.H0, "sigma_H0": self.sigma, "theta_H0_ombh2_omch2": [self.H0, self.omega_b, self.omega_c], "cov_theta": cov, "chi2": 0.0},
            "r_d_modelo_no_BG1": 147.5,
            "fundo_livre": {"H0": self.H0 + self.free_dH0, "sigma_H0": self.free_sigma, "r_d": self.rd, "sigma_r_d": self.sigma_rd, "chi2": 0.0,
                            "delta_chi2_vs_rd_fixo": -1.0, "lnZ_bg_ratio_laplace": self.lnZ, "r_d_no_limite": False, "prior_rd_Mpc": list(PRIOR_RD)},
        }


def check_reproduction(bg, pinned_H0, pinned_sigma, tol_H0=0.01, tol_sigma=0.005):
    """E2: |H0 - 68,531| < 0,01 (pino do V1; spec runner_contract.BG1_H0_tolerance) e |sigma - 0,301| < 0,005 (acrescimo da c1, pre-congelamento).
    Divergencia INTERROMPE; nunca calibra."""
    h, s = bg["bg1"]["H0"], bg["bg1"]["sigma_H0"]
    if not (math.isfinite(h) and math.isfinite(s)):
        raise BackgroundError("E2: fundo nao finito")
    if not abs(h - pinned_H0) < tol_H0:
        raise BackgroundError("E2: BG1 recalculado H0=%.5f diverge do pino %.3f (tol %.3g) -- NAO ABRO, NAO CALIBRO" % (h, pinned_H0, tol_H0))
    if not abs(s - pinned_sigma) < tol_sigma:
        raise BackgroundError("E2: BG1 recalculado sigma=%.5f diverge do pino %.3f (tol %.3g) -- NAO ABRO, NAO CALIBRO" % (s, pinned_sigma, tol_sigma))
    return {"H0": h, "sigma": s, "dH0": h - pinned_H0, "dsigma": s - pinned_sigma, "tol_H0": tol_H0, "tol_sigma": tol_sigma}
