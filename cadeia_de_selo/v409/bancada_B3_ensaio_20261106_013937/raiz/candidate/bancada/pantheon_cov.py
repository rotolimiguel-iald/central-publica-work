# -*- coding: utf-8 -*-
"""pantheon_cov.py -- o Pantheon+ LIGADO à Bancada (30/09/2026): a covariância STAT+SYS 1701×1701 (em disco desde antes; a gerência dissera
«ausente», errata de 28/09), a amostra só-cosmologia (zHD > 0,01 e sem calibradores Cefeida) e a verossimilhança com a magnitude absoluta M
PROFILADA analiticamente (o padrão de Brout et al. 2022): χ²_prof = rᵀC⁻¹r − (1ᵀC⁻¹r)²/(1ᵀC⁻¹1), r = m_b_corr − μ(z), μ = 5 log10(D_L/Mpc) + 25,
D_L = (1 + z_HEL)·D_M(z_HD). Para o ajuste por mínimos quadrados: resíduos BRANQUEADOS L⁻¹(r − M̂·1), com C = L Lᵀ, cuja norma² é o χ²_prof.
A matriz é lida do .dat uma vez e guardada em tabelas/pantheon_cov_v1.npy com o sha256 da fonte ao lado (proveniência)."""
import hashlib
import json
import io
import os
import time

import numpy as np
import torch

from . import fontes


def _sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()



SYMMETRY_MAX_ABS = 1.0e-7
SYMMETRY_MAX_REL_FROBENIUS = 1.0e-6


def _covariance_format(C):
    """Accept only bounded decimal-rounding asymmetry; do not alter source C.

    The existing consumer still symmetrizes its selected Cm as (Cm+Cm.T)/2.
    These are format tolerances, not a new covariance model or statistical fit.
    """
    if C.ndim != 2 or C.shape[0] != C.shape[1] or C.shape[0] == 0 or not np.isfinite(C).all():
        raise ValueError("covariância Pantheon: forma/valores inválidos")
    difference = C - C.T
    max_abs = float(np.max(np.abs(difference)))
    norm = float(np.linalg.norm(C, ord="fro"))
    relative = float(np.linalg.norm(difference, ord="fro") / norm) if norm else 0.0
    if (not np.isfinite(max_abs) or not np.isfinite(relative)
            or max_abs > SYMMETRY_MAX_ABS or relative > SYMMETRY_MAX_REL_FROBENIUS):
        raise ValueError("covariância Pantheon: assimetria excede limites de formato "
                         + repr(dict(max_abs=max_abs, rel_frobenius=relative,
                                     max_abs_limit=SYMMETRY_MAX_ABS, rel_frobenius_limit=SYMMETRY_MAX_REL_FROBENIUS)))
    return dict(max_abs=max_abs, rel_frobenius=relative,
                max_abs_limit=SYMMETRY_MAX_ABS, rel_frobenius_limit=SYMMETRY_MAX_REL_FROBENIUS,
                policy="BOUNDED_PUBLISHED_DECIMAL_ROUNDING", source_modified=False,
                consumer_symmetrization="Cm = 0.5 * (C_selected + C_selected.T)")


def carregar_cov(dir_tabelas):
    """Pinned bytes only. Legacy/unverified caches are not trusted or rewritten."""
    src = fontes.PANTHEON_COV
    raw, h = fontes.read_checked(src)
    npy = os.path.join(dir_tabelas, "pantheon_cov_v1.npy")
    meta = npy + ".json"
    if os.path.isfile(npy) and os.path.isfile(meta):
        m, _ = fontes.json_checked(meta)
        if m.get("fonte_sha256") == h and m.get("cache_sha256"):
            cache, cache_sha = fontes.read_checked(npy)
            if cache_sha != m["cache_sha256"]:
                raise ValueError("cache Pantheon difere do hash de seus bytes")
            C = np.load(io.BytesIO(cache), allow_pickle=False)
            if C.shape != (m["n"], m["n"]):
                raise ValueError("cache Pantheon inválido")
            symmetry = _covariance_format(C)
            return C, dict(m, simetria_formato=symmetry, escrita_em_disco=False)
    # No disk mutation during loading; migrate caches only in an explicit deployment.
    f = io.StringIO(raw.decode("utf-8-sig"))
    n = int(f.readline().strip())
    vals = np.loadtxt(f, dtype=np.float64)
    if n < 1 or vals.size != n * n or not np.isfinite(vals).all():
        raise ValueError("covariância Pantheon inválida")
    C = vals.reshape(n, n)
    symmetry = _covariance_format(C)
    m = dict(fonte=src, fonte_sha256=h, n=n, cache="LEGACY_IGNORED_OR_ABSENT_PARSED_IN_RAM",
             simetrica_max_abs=symmetry["max_abs"], simetria_formato=symmetry, escrita_em_disco=False)
    return C, m


class PantheonCov:
    def __init__(self, cols, dev, dir_tabelas, z_min=0.01, calibradores=False):
        """calibradores=False: a amostra só-cosmologia (zHD > z_min e sem calibradores). calibradores=True (01/10/2026, SH0ES na Bancada): a amostra
        de H0 = (zHD > z_min) OU calibrador Cefeida; para os calibradores μ = CEPH_DIST (Riess et al. 2022), M profilado como antes."""
        self.dev = dev; self.calibradores = bool(calibradores)
        C, self.meta = carregar_cov(dir_tabelas)
        zHD = np.asarray(cols["zHD"], float); zHEL = np.asarray(cols["zHEL"], float); mb = np.asarray(cols["m_b_corr"], float)
        cal = np.asarray(cols["IS_CALIBRATOR"]).astype(int)
        assert C.shape[0] == len(zHD), (C.shape, len(zHD))
        mask = ((zHD > z_min) | (cal == 1)) if self.calibradores else ((zHD > z_min) & (cal == 0))
        self.n = int(mask.sum()); self.z_min = z_min; self.n_total = int(len(zHD)); self.n_calibradores = int((cal == 1).sum())
        Cm = 0.5 * (C[np.ix_(mask, mask)] + C[np.ix_(mask, mask)].T)
        T = lambda a: torch.as_tensor(np.asarray(a, float), device=dev, dtype=torch.float64)
        Ct = T(Cm)
        L = torch.linalg.cholesky(Ct)
        self.Linv = torch.linalg.inv(L)
        self.Cinv = torch.cholesky_inverse(L)
        um = torch.ones(self.n, device=dev, dtype=torch.float64)
        self.one_Cinv = self.Cinv @ um                    # C⁻¹·1
        self.norm = float(um @ self.one_Cinv)              # 1ᵀC⁻¹1
        self.zHD = T(zHD[mask]); self.zHEL = T(zHEL[mask]); self.mb = T(mb[mask])
        ceph = np.asarray(cols.get("CEPH_DIST", np.full(len(zHD), -9.0)), float); hf = np.asarray(cols.get("USED_IN_SH0ES_HF", np.zeros(len(zHD))), float)
        self.is_cal = T(cal[mask].astype(float)) > 0.5; self.ceph = T(np.where(cal[mask] == 1, ceph[mask], 0.0)); self.hf_sh0es = T(hf[mask]) > 0.5
        self.n_cal_usados = int(cal[mask].sum()); self.n_hosts = int(len(np.unique(np.round(ceph[mask][cal[mask] == 1], 4)))) if self.calibradores else 0
        self.diag_ratio = dict(cov_diag_sobre_errdiag2_mediana=float(np.median(np.diag(Cm) / np.asarray(cols["m_b_corr_err_DIAG"], float)[mask] ** 2)))
        self.proveniencia = dict(covariancia=self.meta, amostra=dict(z_min=z_min, n_usadas=self.n, n_total=self.n_total,
                                                                   n_calibradores_excluidos=(0 if self.calibradores else self.n_calibradores), n_calibradores_usados=self.n_cal_usados, n_hospedeiras=self.n_hosts,
                                                                   criterio=("(zHD > z_min) OU IS_CALIBRATOR == 1: a amostra de H0 (calibradores com μ = CEPH_DIST; M profilado)" if self.calibradores
                                                                             else "zHD > z_min e IS_CALIBRATOR == 0 (só cosmologia; M profilado)")),
                                 verossimilhanca="χ²_prof = rᵀC⁻¹r − (1ᵀC⁻¹r)²/(1ᵀC⁻¹1); μ = 5 log10((1+z_HEL) D_M(z_HD)/Mpc) + 25" + (" ; calibradores: μ = CEPH_DIST" if self.calibradores else ""),
                                 referencia="Brout et al. 2022, ApJ 938, 110 (Pantheon+ cosmology; STAT+SYS)" + ("; Riess et al. 2022, ApJL 934, L7 (SH0ES: calibradores Cefeida)" if self.calibradores else ""))

    def mu(self, DM):
        """μ (B, n) a partir de D_M(z_HD) em Mpc (B, n); com calibradores, μ = CEPH_DIST onde IS_CALIBRATOR == 1 (a distância Cefeida substitui o modelo)."""
        mu = 5.0 * torch.log10((1.0 + self.zHEL[None, :]) * DM) + 25.0
        if self.calibradores:
            mu = torch.where(self.is_cal[None, :], self.ceph[None, :].expand_as(mu), mu)
        return mu

    def M_hat(self, mu):
        r = self.mb[None, :] - mu
        return (r @ self.one_Cinv) / self.norm

    def chi2_prof(self, mu):
        r = self.mb[None, :] - mu
        q = ((r @ self.Cinv) * r).sum(1)
        b = r @ self.one_Cinv
        return q - b * b / self.norm

    def residuos_brancos(self, mu):
        r = self.mb[None, :] - mu
        Mh = (r @ self.one_Cinv) / self.norm
        rr = r - Mh[:, None]
        return rr @ self.Linv.T
