# -*- coding: utf-8 -*-
"""simlib.py -- simulacao SINTETICA sob as nulas (TGL verdadeira / LCDM verdadeira) para calibrar a cauda e projetar o poder. Nenhum centro observado.
O fundo vem de testes/QUALIFICACAO_FORNECEDOR_REAL.json (so Planck comprimido + DESI DR2; nenhum H0 local)."""
import json
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "runner"))
import f9v2_calibration as CAL  # noqa: E402
import f9v2_stats as ST  # noqa: E402
import f9v2_verdict as VER  # noqa: E402

SPEC_PATH = os.path.join(ROOT, "spec", "PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json")
QUAL_PATH = os.path.join(ROOT, "testes", "QUALIFICACAO_FORNECEDOR_REAL.json")
CLASSES = ["INCONCLUSIVE_SYSTEMATICS", "FALSIFIED_AT_5SIGMA", "TENSION_3_TO_5_SIGMA", "NOT_FALSIFIED_UNDERPOWERED", "NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_", "NOT_FALSIFIED_POWERED"]
CLASS_NAMES = ["INCONCLUSIVE", "FALSIFIED", "TENSION", "UNDERPOWERED", "DISCRIMINATES", "POWERED_NOT_DISCRIMINATED"]
_CTX = {}


def classify(tok):
    body = tok.split("__", 1)[1] if "__" in tok else tok
    for c, n in zip(CLASSES, CLASS_NAMES):
        if body.startswith(c):
            return n
    return "OUTRO"


def ctx(fam="P_primaria", s5=True):
    key = (fam, s5)
    if key in _CTX:
        return _CTX[key]
    spec = json.load(open(SPEC_PATH, encoding="utf-8"))["spec"]
    q = json.load(open(QUAL_PATH, encoding="utf-8"))["fundo"]
    lei = spec["lei"]
    consts = {k: v for k, v in spec["S5_propagacao"]["constantes_E"].items() if k != "origem"}
    beta = spec["beta"]["alpha_read"] * math.sqrt(math.e)
    law = ST.Law(beta, lei["K_frozen_V1"], ST.lnE_pinned(lei["Omega_m"], lei["Omega_r"], lei["z_star"]), q["bg1"]["H0"], q["bg1"]["cov_theta"],
                 q["bg1"]["theta_H0_ombh2_omch2"], lei["z_star"], consts, s5=s5)
    ids = spec["familias"][fam]["ids"]
    sig = {k: v["sigma"] for k, v in spec["leitores"].items()}
    amps = spec["covariancia"]["amplitudes_km_s_Mpc"]
    grid = spec["covariancia"]["grid"]
    ep = ST.grid_endpoints(amps, sig, ids, grid["lambda_N"], grid["lambda_T"])
    fn, _ = VER.load_pinned_verdict(spec["funcao_de_veredito"]["fonte"], spec["funcao_de_veredito"]["sha256"])
    nc = ST.grid_endpoints(amps, sig, spec["familias"]["N_sem_cefeidas"]["ids"], grid["lambda_N"], grid["lambda_T"])
    c = dict(spec=spec, law=law, ids=ids, sig=sig, amps=amps, grid=grid, ep=ep, fn=fn, bgfree=q["fundo_livre"], bg=q["bg1"],
             power_cef=ST.power_sigma_only(law.K, law.mu, nc["maximum"]["sigma_comb"], law.V(law.beta)))
    c["zmap"] = CAL.ZDeltaMap(ep["minimum"]["sigma_comb"], law)
    c["zdm"] = CAL.ZDiscMap(ep["maximum"]["sigma_comb"], law)
    c["tau"] = CAL.taus(amps, sig, ids, ep, law, grid["lambda_N"], grid["lambda_T"])
    # LUT z_delta calibrado (interpolacao; so para simulacao) por modo
    raw = np.concatenate([np.linspace(0.0, 4.0, 81), np.linspace(4.2, 10.0, 59)])
    lut = {}
    for mode, tk in (("sup_caixa", c["tau"]["tau_f_sup"]), ("proprio", c["tau"]["tau_f_proprio"])):
        lut[mode] = (raw, np.array([c["zmap"].z_cal(float(r), tk, refine=False) if r > 0 else 0.0 for r in raw]))
    c["lut"] = lut
    _CTX[key] = c
    return c


def zcal_lut(c, mode, zraw):
    if zraw is None:
        return None
    if mode == "bruto":
        return zraw
    raw, cal = c["lut"][mode]
    a = abs(zraw)
    if a > raw[-1]:
        return math.copysign(cal[-1] + (a - raw[-1]), zraw)
    return math.copysign(float(np.interp(a, raw, cal)), zraw)


def covariance_at(c, lam_n, lam_t):
    return ST.covariance(c["amps"], c["sig"], c["ids"], lam_n, lam_t)


def draw_y(c, null, C_true, rng, n):
    law = c["law"]
    m = len(c["ids"])
    if null == "TGL":
        mean, V = law.K * law.mu, law.V(law.beta)
    elif null == "LCDM":
        mean, V = law.mu, law.V(0.0)
    else:
        raise ValueError(null)
    cov = C_true + V * np.ones((m, m))
    return rng.multivariate_normal(np.full(m, mean), cov, size=n)


def assemble_and_verdict(c, y, mode, st_min=None, st_max=None):
    """Replica de runner.eval_family (sem diagnosticos) para UMA realizacao y; devolve (token, st_min, st_max, z_delta_fed, z_disc_fed)."""
    law, ep, ids = c["law"], c["ep"], c["ids"]
    bgfree = c["bgfree"]
    st_min = st_min or ST.endpoint_statistics(y, ids, ep["minimum"]["covariance"], law, bgfree, fast=True)
    st_max = st_max or ST.endpoint_statistics(y, ids, ep["maximum"]["covariance"], law, bgfree, fast=True)
    st = {"minimum": st_min, "maximum": st_max}
    VT = law.V(law.beta)
    zread = [(c["sig"][i], (float(y[k]) - law.K * law.mu) / math.sqrt(c["sig"][i] ** 2 + VT)) for k, i in enumerate(ids)]
    edge = any(st[s]["beta"]["at_prior_edge"] or st[s]["z_delta"] is None for s in st)
    zd_raw, zdisc_raw = st_min["z_delta"], st_max["z_disc"]
    tau = c["tau"]
    if mode == "bruto":
        zd_fed, zdisc_fed = zd_raw, zdisc_raw
    else:
        tf = tau["tau_f_sup"] if mode == "sup_caixa" else tau["tau_f_proprio"]
        td = tau["tau_d_sup"] if mode == "sup_caixa" else tau["tau_d_proprio"]
        zd_fed = zcal_lut(c, mode, zd_raw)
        zdisc_fed = c["zdm"].z_cal(zdisc_raw, td)
    r = {"fundo": "BG1", "n_local": len(ids), "n_alvos_declarados": 0, "required_sources_admitted": True, "beta_livre_no_limite": bool(edge),
         "minimum": {"z_delta": 0.0 if zd_fed is None else float(zd_fed), "sigma_z_por_alvo": zread},
         "maximum": {"poder_previo": ST.power_sigma_only(law.K, law.mu, ep["maximum"]["sigma_comb"], VT), "z_disc": float(zdisc_fed),
                     "lnB_lcdm": st_max["lnB_lcdm"], "lnB_livre": st_max["lnB_livre"], "lnB_shift": st_max["lnB_shift"], "lnB_fundo_livre": st_max["lnB_fundo_livre"],
                     "poder_nao_cefeida": c["power_cef"]},
         "use_novel_parametros": True,
         "dispersao_endpoints": {s: {"chi2_por_gl": st[s]["dispersao"]["chi2_por_gl"], "p": st[s]["dispersao"]["p"]} for s in ("minimum", "maximum")}}
    return c["fn"](json.loads(json.dumps(r))), st_min, st_max, zd_fed, zdisc_fed
