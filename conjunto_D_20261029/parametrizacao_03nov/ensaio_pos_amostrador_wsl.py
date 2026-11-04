# -*- coding: utf-8 -*-
"""ensaio_pos_amostrador_wsl.py -- exercita, com posterior FALSO (sorteado), o trecho do pe_runner_D que so roda DEPOIS da convergencia (e que o mini-ensaio PARTIAL nao alcanca):
posterior_columns -> remnant_conversion.derive (LAL SimIMREOBFinalMassSpin + Planck18 pinado) -> colunas pareadas -> cegueira (semente de TESTE) -> estagio cego. Sem dado real, sem a semente oficial."""
import json
import os
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "codigo_D"))
import blinding_D as B  # noqa: E402
import estagio_cego_D as EC  # noqa: E402
import pe_runner_D as P  # noqa: E402
import v1_ramo_b as V  # noqa: E402
import pandas as pd  # noqa: E402
from remnant_conversion import derive  # noqa: E402

jobs = json.loads((HERE / "JOBS_D_V1.json").read_text())
ev = "GW250118_170523"
cfg = jobs["D_" + ev]
v1, _ = V.carregar_v1()
row = V.tabela_eventos(v1)[ev]
rng = np.random.default_rng(3)
n = 1500
z = row["Mf_det_mediana_GR"]
post = pd.DataFrame({"mass_1": rng.normal(52, 4, n), "mass_2": rng.normal(41, 4, n), "chi_1": np.clip(rng.normal(0.12, 0.2, n), -0.9, 0.9), "chi_2": np.clip(rng.normal(0.1, 0.25, n), -0.9, 0.9),
                     "luminosity_distance": rng.normal(1900, 300, n), "theta_jn": rng.uniform(0.2, 1.2, n), "phase": rng.uniform(0, 6.28, n), "ra": rng.uniform(0, 6.28, n),
                     "dec": rng.uniform(-1, 1, n), "psi": rng.uniform(0, 3.14, n), "geocent_time": rng.normal(cfg["event_GPS"], 0.01, n),
                     "dtau220": rng.normal(-0.2, 0.33, n), "dtau440": np.zeros(n), "domega220": np.zeros(n), "domega440": np.zeros(n)})
t = time.time()
cols = P.posterior_columns(post, cfg)
derived, receipt = derive(cols, cfg, lambda: None)
assert set(derived) == set(P.DERIVED_PHYSICAL) and all(np.asarray(v).shape == (n,) and np.isfinite(v).all() for v in derived.values())
cols.update(derived)
tmp = Path(tempfile.mkdtemp(prefix="pos_amostrador_"))
seed = tmp / "seed.bin"
seed.write_bytes(os.urandom(32))
import hashlib  # noqa: E402
reg = {"blinding": {"seed_path": str(seed), "seed_commitment_sha256": hashlib.sha256(seed.read_bytes()).hexdigest(), "offset_half_range": 1.0}}
science = B.shifted_samples({k: cols[k] for k in P.DEFORMATIONS}, ev, reg)
science["paired_physical_columns"] = {k: cols[k].tolist() for k in P.PHYSICAL + P.DERIVED_PHYSICAL}
science.update(convergence_status="CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW")
eg = EC.estagio_cego({ev: json.loads(json.dumps(science))}, v1)       # passa por json: o formato gravado pelo pe_runner
print(json.dumps({"derive_status": receipt["status"], "N": receipt["N"], "s": round(time.time() - t, 1),
                  "chaves_do_ANALYST_OUTPUT": sorted(science.keys()), "evento_no_estagio_cego": list(eg["por_evento"]), "recusados": eg["eventos_recusados"],
                  "sigma_invariante_ok": abs(eg["por_evento"][ev]["sigma"] - float(np.std(post["dtau220"], ddof=1))) < 1e-9}))
