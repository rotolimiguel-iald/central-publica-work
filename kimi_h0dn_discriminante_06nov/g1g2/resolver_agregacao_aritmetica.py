from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent / "astra_bell_fock_tt_05nov/h0dn_bg1_06nov"
PP = Path(r"C:\IALD\observaveis_tgl\tgl_data_cache\pantheon\Pantheon+SH0ES.dat")
OUT = HERE / "G1_ARITHMETIC_CANDIDATE.json"
N = 3492
Y = np.fromfile(HERE / "ally_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=N)
pp = pd.read_csv(PP, sep=r"\s+", usecols=["CID", "m_b_corr"], dtype={"CID": str})
mapping = json.loads((BASE / "cross_rung/mapping.json").read_text(encoding="utf-8"))
cal = pd.read_csv(
    BASE / "network/upstream/data/sn1a_calib.dat", sep=r"\s+", comment="#", header=None,
    usecols=[0, 1, 2, 3, 4], names=["number", "host", "CID", "m0", "sigma"], dtype={"CID": str},
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


rows = []
for item in mapping:
    indices = item["pp_indices"]
    if not indices:
        continue
    m0 = float(cal.loc[cal.CID == item["CID"]].iloc[0].m0)
    candidate_lists = []
    for index in indices:
        reference = float(pp.iloc[index].m_b_corr)
        candidates = sorted(
            range(3130, 3207),
            key=lambda raw: abs(float(Y[raw] - reference)),
        )[:6]
        candidate_lists.append(candidates)
    best = None
    for combination in itertools.product(*candidate_lists):
        if len(set(combination)) != len(combination):
            continue
        values = Y[list(combination)]
        error = abs(float(values.mean() - m0))
        if best is None or error < best["mean_error"]:
            best = {
                "raw_indices": list(combination),
                "raw_values": [float(value) for value in values],
                "raw_mean": float(values.mean()),
                "mean_error": error,
                "candidate_reference_differences": [
                    float(Y[raw] - pp.iloc[index].m_b_corr)
                    for raw, index in zip(combination, indices)
                ],
            }
    rows.append({
        "host": item["host"], "CID": item["CID"], "multiplicity": len(indices),
        "m0_Bi": m0, **best,
    })

for subset_name, subset in [
    ("all47", rows),
    ("multi26", [row for row in rows if row["multiplicity"] > 1]),
    ("single21", [row for row in rows if row["multiplicity"] == 1]),
]:
    errors = np.array([row["mean_error"] for row in subset])
    print(subset_name, json.dumps({
        "count": len(subset),
        "max_error": float(errors.max()),
        "median_error": float(np.median(errors)),
        "within_0.0005": int(np.sum(errors <= 0.0005)),
        "within_0.001": int(np.sum(errors <= 0.001)),
        "within_0.005": int(np.sum(errors <= 0.005)),
        "within_0.01": int(np.sum(errors <= 0.01)),
    }))
for row in rows:
    print(json.dumps(row))

payload = {
    "status": "CANDIDATE_ARITHMETIC_AGGREGATION__REQUIRES_SOURCE_CONFIRMATION",
    "method": "Nearest m_b_corr candidates, unique raw rows, minimize abs(mean(raw Y)-m0_Bi); no inverse-variance weights and no H0 fit",
    "rows": rows,
    "sources": [
        {"path": str(HERE / "ally_shoes_ceph_topantheonwt6.0_112221.fits"), "sha256": sha(HERE / "ally_shoes_ceph_topantheonwt6.0_112221.fits")},
        {"path": str(PP), "sha256": sha(PP)},
        {"path": str(BASE / "cross_rung/mapping.json"), "sha256": sha(BASE / "cross_rung/mapping.json")},
    ],
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("output", OUT, "sha256", sha(OUT))
