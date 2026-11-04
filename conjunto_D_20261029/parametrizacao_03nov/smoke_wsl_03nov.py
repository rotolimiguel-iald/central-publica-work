# -*- coding: utf-8 -*-
"""Smoke no WSL (/opt/lal_env) SEM dado real: (1) pinos/guarda/runtime no WSL; (2) anti-CLI do guarda; (3) injecao C2 pelo injection_design ORIGINAL (copia RO, 2 trocas em
memoria) em ruido gaussiano sintetico, com o SNR-alvo conferido; (4) fatia de verossimilhanca em ruido zero: o pico de dtau220 cai na verdade injetada (GR e RB).
Nenhum strain de D e aberto: o ruido e gerado pela PSD de projeto do bilby."""
import hashlib
import json
import math
import os
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

T0 = time.time()
CODE = Path(__file__).resolve().parent / "codigo_D"
sys.path.insert(0, str(CODE))
import blinding_D as B  # noqa: E402
import gerar_jobs_D as J  # noqa: E402
import gerar_pinos_D as GP  # noqa: E402
import guard_D as G  # noqa: E402
import injecao_c2 as I  # noqa: E402

out = {"python": sys.version.split()[0], "etapas": {}}
tmp = Path(tempfile.mkdtemp(prefix="smoke_D_"))
(tmp / "priv").mkdir()
seed = tmp / "priv" / "seed.bin"
seed.write_bytes(os.urandom(32))
G.PINOS, G.RELOGIO, G.JOBS, G.CONGELAMENTO, G.PRIV, G.SAIDAS = tmp / "P.json", tmp / "R.json", tmp / "J.json", tmp / "C.json", tmp / "priv", tmp / "priv" / "pe"
G.SAIDAS.mkdir()
B.SEMENTE_PADRAO = str(seed)
t = time.time()
pinos, dig = GP.montar(destino=G.PINOS, runtime_json=str(CODE.parent / "runtime_wsl.json"))
out["etapas"]["pinos_no_WSL"] = {"s": round(time.time() - t, 2), "sha16": dig[:16]}
ordem = tmp / "ordem.json"
ordem.write_text(json.dumps({"opcao": "c", "ordem_operador_sha256": "3" * 64, "decidido_utc": "2026-11-03T00:00:00Z"}))
G.abrir_relogio(21, ordem)
t = time.time()
reg, dig2 = G.checked_registration()
out["etapas"]["checked_registration_no_WSL"] = {"s": round(time.time() - t, 2), "ok": dig2 == dig}
out["etapas"]["runtime_pinado"] = {"check_runtime": G.check_runtime(reg), "pacotes": reg["runtime_esperado"]["pacotes"]}
cfg0 = {"output_directory_name": "x", "privacy_mode": "procedural_same_host"}
try:
    G.output_path("x").mkdir(parents=True, exist_ok=True)
    (G.output_path("x") / "PRIVATE.log").write_text("")
    ctx = {"registration_sha256": dig, "job": "j", "controller_pid": os.getpid(), "controller_start_ticks": "0", "stop_utc": "2999-01-01T00:00:00+00:00",
           "config_sha256": hashlib.sha256(json.dumps(cfg0, sort_keys=True).encode()).hexdigest()}
    (G.output_path("x") / "LAUNCH_CONTEXT.json").write_text(json.dumps(ctx))
    G.validate_launch(str(G.output_path("x") / "LAUNCH_CONTEXT.json"), reg, dig, "j", cfg0)
    out["etapas"]["anti_CLI"] = "FALHA: CLI direto aceito"
except Exception as exc:                                              # noqa: BLE001
    out["etapas"]["anti_CLI"] = "recusado (%s): %s" % (type(exc).__name__, str(exc)[:90])

import bilby  # noqa: E402

bilby.core.utils.logger.setLevel("ERROR")
dq = json.loads(Path("/mnt/c/IALD/Central de Patentes/work/conjunto_D_20261029/smoke/dq_meta_D_v2.json").read_text())
des = I.desenho_c2(pinos, dq, "minima")
mod = I.carregar_injection_design()
AMOSTRADOR = {"nlive": 512, "walks": 50, "maxcall": 3000000, "workers": 24}
res = []
for inj in des["injecoes"][:4]:
    jobname, cfg = J.job_c2(reg, inj, AMOSTRADOR, 8 * 3600)
    G.validate_job_D(reg, jobname, cfg)
    ifos = bilby.gw.detector.InterferometerList(["H1", "L1"])
    for ifo in ifos:
        ifo.set_strain_data_from_power_spectral_density(sampling_frequency=4096, duration=16, start_time=inj["segment_start_GPS"])
        ifo.strain_data.roll_off = 0.2
        ifo.minimum_frequency = 20.0
        ifo.maximum_frequency = 1024.0
    t = time.time()
    rec = mod.inject_into_ifos(ifos, cfg, reg)
    res.append({"id": inj["id"], "SNR_alvo": inj["target_network_optimal_SNR"], "SNR_injetado": round(rec["optimal_network_SNR"], 6),
                "dtau220": rec["parameters"]["dtau220"], "d_L_final_Mpc": round(rec["parameters"]["luminosity_distance"], 1), "s": round(time.time() - t, 2)})
out["etapas"]["injecao_C2_ruido_gaussiano"] = res

fatias = []
for classe in ("GR", "RB"):
    inj = next(x for x in des["injecoes"] if x["classe"] == classe)
    jobname, cfg = J.job_c2(reg, inj, AMOSTRADOR, 8 * 3600)
    ifos = bilby.gw.detector.InterferometerList(["H1", "L1"])
    for ifo in ifos:
        ifo.set_strain_data_from_zero_noise(sampling_frequency=4096, duration=16, start_time=inj["segment_start_GPS"])
        ifo.strain_data.roll_off = 0.2
        ifo.minimum_frequency = 20.0
        ifo.maximum_frequency = 1024.0
    rec = mod.inject_into_ifos(ifos, cfg, reg)
    P = rec["parameters"]
    gen = bilby.gw.WaveformGenerator(duration=16, sampling_frequency=4096, start_time=inj["segment_start_GPS"], frequency_domain_source_model=mod.pseob_frequency_domain,
                                     parameter_conversion=mod.parameter_conversion,
                                     waveform_arguments={"minimum_frequency": 20.0, "maximum_frequency": 1024.0, "reference_frequency": 20.0, "catch_waveform_errors": False,
                                                         "analysis_time_contract": {"start_GPS": inj["segment_start_GPS"], "duration_s": 16, "roll_off_s": 0.2}})
    lk = bilby.gw.likelihood.GravitationalWaveTransient(interferometers=ifos, waveform_generator=gen)
    grade = np.linspace(-0.8, 0.5, 27)
    ll = []
    for d in grade:
        lk.parameters.update(dict(P, dtau220=float(d)))
        ll.append(float(lk.log_likelihood_ratio()))
    i0 = int(np.argmin(abs(grade)))
    fatias.append({"classe": classe, "dtau220_injetado": P["dtau220"], "pico_da_fatia_passo_0p05": float(grade[int(np.argmax(ll))]),
                   "dlogL_pico_menos_em_dtau0": float(max(ll) - ll[i0])})
out["etapas"]["fatia_de_verossimilhanca_ruido_zero"] = fatias
out["tempo_total_s"] = round(time.time() - T0, 1)
print(json.dumps(out, indent=1, ensure_ascii=False))
