# -*- coding: utf-8 -*-
"""
13_rodar_nivel2.py — a cadeia do Estagio B, contra TGL_NIVEL2_V1 (ja hasheado)
===============================================================================
V2 (11/08/2026, pos-reinicio espontaneo da maquina): CHECKPOINT EM DISCO.
O reinicio de 22:44 matou a variante L no bloco 7/10 (~17h de cadeia, que so
existia em memoria) e o JSON da S (que so era gravado ao final das DUAS).
Duas licoes, ambas ja pagas uma vez pelo programa (v149: per_tracer nao
persistido):
  (i)  emcee.backends.HDFBackend: a cadeia vive em 13_nivel2_chains.h5,
       gravada passo a passo; a rodada RETOMA sozinha do ultimo passo;
  (ii) o resultado de CADA variante e gravado IMEDIATAMENTE ao fim dela
       (merge em 13_nivel2_resultado.json), nao ao final do conjunto.
NADA das regras muda: mesmo frozen (hash conferido), mesmos gates, mesma
semente, mesmas variantes. Rodar com o python do tgl_pycbc_env.
===============================================================================
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NW, NSTEP, NBURN = 48, 3400, 650   # 3400: NSTEP>=40*tau com margem (tau~72 medido; o gate congelado exige >=40; extensao respeita o frozen)
SEED = 20260810
NPROC = 24
H5 = os.path.join(HERE, "13_nivel2_chains.h5")
RESULT = os.path.join(HERE, "13_nivel2_resultado.json")

LIKE = None


def _carregar_n2():
    import importlib.util as ilu
    spec = ilu.spec_from_file_location(
        "n2", os.path.join(HERE, "12_nivel2_frozen_e_verossimilhanca.py"))
    n2 = ilu.module_from_spec(spec)
    sys.modules["n2"] = n2
    spec.loader.exec_module(n2)
    return n2


def _init(variante):
    os.environ["OMP_NUM_THREADS"] = "1"
    global LIKE
    n2 = _carregar_n2()
    n2._preparar_data_alias()
    LIKE = n2.LikeN2(variante)


def _logpost(theta):
    return LIKE.log_post(theta)


def rhat_grupos(chain_beta_por_walker, k=4):
    nw = chain_beta_por_walker.shape[1]
    grupos = np.array_split(np.arange(nw), k)
    seqs = [chain_beta_por_walker[:, g].ravel() for g in grupos]
    n = min(len(s) for s in seqs)
    seqs = np.array([s[:n] for s in seqs])
    m = seqs.mean(axis=1)
    W = seqs.var(axis=1, ddof=1).mean()
    B = n * m.var(ddof=1)
    return float(np.sqrt(((n - 1) / n * W + B / n) / W))


def _gravar_parcial(n2, variante, res):
    """persistencia IMEDIATA por variante (a licao do reinicio)."""
    out = {"frozen_hash": n2.FROZEN_HASH,
           "config": {"walkers": NW, "steps": NSTEP, "burn": NBURN,
                      "nproc": NPROC, "seed": SEED},
           "variantes": {}}
    if os.path.exists(RESULT):
        try:
            out = json.load(open(RESULT, encoding="utf-8"))
        except Exception:
            pass
    out["frozen_hash"] = n2.FROZEN_HASH        # sempre atual (o merge preservava o velho — defeito achado 12/08)
    out.setdefault("variantes", {})[variante] = res
    with open(RESULT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)


def rodar_variante(n2, variante):
    import emcee
    from multiprocessing import Pool
    backend = emcee.backends.HDFBackend(H5, name="var" + variante)
    ja = 0
    try:
        ja = int(backend.iteration)
    except Exception:
        ja = 0
    t0 = time.time()
    estado = None
    # v164-hardening: pool NOVO a cada lote (auto-cura se um worker morrer),
    # maxtasksperchild recicla workers do CAMB, lotes menores = sinal frequente.
    _POOLKW = dict(initializer=_init, initargs=(variante,), maxtasksperchild=4096)
    if ja == 0:
        backend.reset(NW, 7)
        rng = np.random.default_rng(SEED)
        p0 = np.column_stack([
            rng.uniform(-0.02, 0.06, NW),
            rng.normal(67.4, 1.2, NW),
            rng.normal(0.02237, 0.0003, NW),
            rng.normal(0.1200, 0.0025, NW),
            rng.normal(0.9649, 0.008, NW),
            rng.normal(math.log(2.1e-9 * 1e10), 0.03, NW),
            rng.normal(0.0544, 0.007, NW),
        ])
        with Pool(NPROC, **_POOLKW) as pool:
            for tent in range(6):
                lps = np.array(pool.map(_logpost, [list(p0[i]) for i in range(NW)]))
                bad = ~np.isfinite(lps)
                if not bad.any():
                    break
                for i in np.where(bad)[0]:
                    p0[i] = [rng.uniform(-0.02, 0.06), rng.normal(67.4, 1.2),
                             rng.normal(0.02237, 0.0003), rng.normal(0.1200, 0.0025),
                             rng.normal(0.9649, 0.008),
                             rng.normal(math.log(2.1e-9 * 1e10), 0.03),
                             rng.normal(0.0544, 0.007)]
        estado = p0
    else:
        print("   [%s] RETOMANDO do passo %d (checkpoint h5)" % (variante, ja),
              flush=True)
        estado = None
    passo = max(1, NSTEP // 40)
    # v164-tuning: POOL UNICO por variante (o custo de partida dos workers CAMB
    # dominava o lote); a causa raiz do stall era o PIPE do console, ja eliminada
    # (stdout->arquivo). Tripwire: o monitor de mtime do h5 pega silencio >10min
    # e o checkpoint torna o reinicio gratuito.
    with Pool(NPROC, **_POOLKW) as pool:
        sam = emcee.EnsembleSampler(NW, 7, _logpost, pool=pool, backend=backend)
        while int(backend.iteration) < NSTEP:
            resta = min(passo, NSTEP - int(backend.iteration))
            estado = sam.run_mcmc(estado, resta, progress=False)
            estado = None                      # dali em diante, o backend guia
            print("   [%s] passo %d/%d  (%.0f s nesta sessao)"
                  % (variante, int(backend.iteration), NSTEP, time.time() - t0),
                  flush=True)
    dt = time.time() - t0

    ch_w = backend.get_chain(discard=NBURN)
    ch = backend.get_chain(discard=NBURN, flat=True)
    try:
        acc = float(np.mean(backend.accepted / backend.iteration))
    except Exception:
        acc = float("nan")
    try:
        tau = float(np.max(emcee.autocorr.integrated_time(backend.get_chain(),
                                                          quiet=True)))
    except Exception:
        tau = float("nan")
    rhat = rhat_grupos(ch_w[:, :, 0])
    ess = ch.shape[0] / tau if np.isfinite(tau) and tau > 0 else 0.0

    G = n2.FROZEN["gates_de_convergencia"]
    gates_ok = {
        "aceitacao": bool(G["aceitacao"][0] <= acc <= G["aceitacao"][1]),
        "tau": bool(np.isfinite(tau) and NSTEP >= G["nstep_sobre_tau_min"] * tau),
        "rhat": bool(rhat < G["rhat_max_beta"]),
        "ess": bool(ess >= G["ess_min_beta"]),
    }
    convergiu = all(gates_ok.values())

    nomes = ["beta_TGL", "H0", "ombh2", "omch2", "ns", "logA", "tau"]
    res = {"variante": variante, "segundos_ultima_sessao": dt, "aceitacao": acc,
           "tau_max": tau, "rhat_beta": rhat, "ess_beta": ess,
           "n_amostras": int(ch.shape[0]), "gates_ok": gates_ok,
           "convergiu": convergiu, "retomada_de_passo": ja, "params": {}}
    for i, n in enumerate(nomes):
        q = np.percentile(ch[:, i], [15.865, 50.0, 84.135])
        res["params"][n] = {"mediana": float(q[1]),
                            "sigma_simetrico": float(0.5 * (q[2] - q[0]))}
    qb = np.percentile(ch[:, 0], [3e-05, 0.135, 2.5, 15.865, 50.0,
                                  84.135, 97.5, 99.865, 99.99997])
    b, sig = float(qb[4]), float(0.5 * (qb[5] - qb[3]))
    res["beta_quantis"] = {"q5s_lo": float(qb[0]), "q3s_lo": float(qb[1]),
                           "q95_lo": float(qb[2]), "mediana": b,
                           "q95_hi": float(qb[6]), "q3s_hi": float(qb[7]),
                           "q5s_hi": float(qb[8]), "sigma": sig}
    res["beta_vs_teoria"] = {
        "alpha_sqrt_e": n2.BETA_TGL,
        "desvio_sigmas": abs(b - n2.BETA_TGL) / sig if sig > 0 else None,
        "vs_zero_sigmas": abs(b) / sig if sig > 0 else None,
        "sigma_sobre_beta": sig / n2.BETA_TGL,
    }
    v = (n2.veredito_frozen(b, sig, float(qb[0]), float(qb[8]), float(qb[1]),
                            float(qb[7]), float(qb[2]), float(qb[6]))
         if convergiu else "N2_NOT_CONVERGED")
    res["veredito"] = v
    _gravar_parcial(n2, variante, res)         # PERSISTE JA (a licao)
    return res


def main():
    import multiprocessing as mp
    mp.set_executable(sys.executable)          # conserto do venv/Store (10/08)
    n2 = _carregar_n2()
    n2._preparar_data_alias()
    print("=" * 84)
    print(" TGL_NIVEL2_V1 — Estagio B (F4): o MCMC completo  [V2: checkpoint h5 + retomada]")
    print(" frozen hash = %s   (congelado ANTES de qualquer cadeia)" % n2.FROZEN_HASH[:32])
    print(" beta_TGL = %.10f | %d walkers x %d passos (burn %d) | %d processos | seed %d"
          % (n2.BETA_TGL, NW, NSTEP, NBURN, NPROC, SEED))
    print(" regua RELATIVIZADA em unidades de beta; CONFIRMED proibido; fail-closed")
    print("=" * 84, flush=True)

    saidas = {}
    for variante in ("S", "L"):
        print(" >>> VARIANTE %s (%s)" % (variante,
              "PRIMARIA free-streaming" if variante == "S"
              else "co-rodada, fluido suave; expectativa declarada: quase cega"),
              flush=True)
        res = rodar_variante(n2, variante)
        saidas[variante] = res
        b = res["params"]["beta_TGL"]
        print()
        print(" [%s] GATES: aceit %.3f | R-hat %.4f | ESS %.0f -> %s"
              % (variante, res["aceitacao"], res["rhat_beta"], res["ess_beta"],
                 "CONVERGIU" if res["convergiu"] else "NAO CONVERGIU"))
        print(" [%s] beta_TGL = %+.6f +- %.6f  (sigma/beta = %.2f)"
              % (variante, b["mediana"], b["sigma_simetrico"],
                 res["beta_vs_teoria"]["sigma_sobre_beta"]))
        print(" [%s] >>> %s" % (variante, res["veredito"]), flush=True)

    sha = hashlib.sha256(open(RESULT, "rb").read()).hexdigest()
    print()
    print("=" * 84)
    print(" VEREDITOS (contra o frozen %s):" % n2.FROZEN_HASH[:16])
    for v, r in saidas.items():
        print("   variante %s: %s" % (v, r["veredito"]))
    print(" CONFIRMED proibido. O rito nao move gate algum; o veredito vai ao operador (D1).")
    print(" resultado em %s (sha %s)" % (os.path.basename(RESULT), sha[:16]))
    print("=" * 84)


if __name__ == "__main__":
    main()
