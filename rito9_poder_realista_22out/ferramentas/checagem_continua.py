"""Checagem INDEPENDENTE do modelo de celulas: KL(H1||H0) e KL(H0||H1) por integracao numerica no tempo CONTINUO
(kernel exponencial de media tau0(1-beta)/beta no lugar do pente geometrico) x o que a rodada gravou.

So leitura dos dados da rodada. Uso: python checagem_continua.py <dir_work>
"""
import csv
import json
import math
import os
import sys

import numpy as np
from scipy.signal import fftconvolve

W = sys.argv[1]
sys.path.insert(0, os.path.join(W, "ferramentas"))
import nucleo_poder as N  # noqa: E402

pr = json.load(open(os.path.join(W, "PREREGISTRO.json"), encoding="utf-8"))
um = N.ler_alpha_um(pr["beta"]["um_py"])
beta = N.beta_de_alpha(um["alpha"])
rows = {r["case_id"]: r for r in csv.DictReader(open(os.path.join(W, "saida_rodada", "n_req_por_caso.csv"), encoding="utf-8"))}
p1 = pr["familias"]["P1"]

CASOS = [
    ("P2|K3_S10_G1_flat_tau1000_f0.5|ell20", 3, 10, 1, "flat", 1000.0, 0.5, 20.0),
    ("P2|K4_S14_G2_damped_tau100_f0.8|ell10", 4, 14, 2, "damped", 100.0, 0.8, 10.0),
    ("P2|K3_S14_G1_damped_tau30_f0.5|ell30", 3, 14, 1, "damped", 30.0, 0.5, 30.0),
    ("REF_ESQUELETO|sig3|ell20", None, None, None, None, None, 0.0, 20.0),
]
saida = []
for cid, K, S, G, amp, tau, f, ell in CASOS:
    tau0 = ell * 1e3 / N.C_M_S * 1e3
    m = tau0 * (1 - beta) / beta
    dt = 0.002 if (tau is None or tau <= 100) else 0.02
    t_hi = (40 * tau if tau else 0) + 12 * 10 + 41.4 * m + 20
    t_hi = max(t_hi, 400.0)
    t = np.arange(-30.0, t_hi, dt)
    if K is None:
        f0 = np.exp(-0.5 * (t / 3.0) ** 2) / (3.0 * math.sqrt(2 * math.pi))
    else:
        g = N.perfil_burst(K, S, G, amp, p1["mu1_ms"], p1["r_damped"])
        B = sum(w * np.exp(-0.5 * ((t - mu) / s) ** 2) / (s * math.sqrt(2 * math.pi)) for w, mu, s in g)
        T = np.where(t >= 0, np.exp(-np.maximum(t, 0) / tau) / tau, 0.0)
        f0 = (1 - f) * B + f * T
    xk = np.arange(0, 41.4 * m, dt)
    k = np.exp(-xk / m) / m * dt                    # massa por passo (exponencial continua)
    f1 = fftconvolve(f0, k, mode="full")[: t.size]
    f1 = np.maximum(f1, 0.0)
    a0 = f0 * dt
    a1 = f1 * dt
    a0 = a0 / a0.sum()
    a1 = a1 / a1.sum()
    ok = (a0 > 1e-300) & (a1 > 1e-300)
    lam = np.log(a1[ok] / a0[ok])
    lam_c = np.minimum(lam, 40.0)
    kl10 = float((a1[ok] * lam_c).sum())
    kl01 = float(-(a0[ok] * lam).sum())
    r = rows[cid]
    saida.append(dict(case_id=cid, kl_h1_h0_continuo=kl10, kl_h1_h0_celulas=float(r["kl_h1_h0_cap"]),
                      rel1=kl10 / float(r["kl_h1_h0_cap"]) - 1, kl_h0_h1_continuo=kl01,
                      kl_h0_h1_celulas=float(r["kl_h0_h1"]), rel0=kl01 / float(r["kl_h0_h1"]) - 1))
for s in saida:
    print(json.dumps(s))
with open(os.path.join(W, "checagem_continua.json"), "x", encoding="utf-8") as f:
    json.dump(saida, f, indent=2)
