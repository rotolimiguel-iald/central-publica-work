from pathlib import Path
import json
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent / "astra_bell_fock_tt_05nov/h0dn_bg1_06nov"
PP = Path(r"C:\IALD\observaveis_tgl\tgl_data_cache\pantheon\Pantheon+SH0ES.dat")
pp = pd.read_csv(PP, sep=r"\s+", usecols=["CID", "m_b_corr", "MU_SH0ES"], dtype={"CID": str})
mapping = json.loads((BASE / "cross_rung/mapping.json").read_text(encoding="utf-8"))
cal = pd.read_csv(
    BASE / "network/upstream/data/sn1a_calib.dat",
    sep=r"\s+", comment="#", header=None,
    usecols=[0, 1, 2, 3, 4], names=["number", "host", "CID", "m0", "sigma"],
    dtype={"CID": str},
)
rows = []
for row in mapping:
    indices = row["pp_indices"]
    if not indices:
        continue
    source = cal.loc[cal.CID == row["CID"]].iloc[0]
    mbc = pp.iloc[indices].m_b_corr.to_numpy(dtype=float)
    mu = pp.iloc[indices].MU_SH0ES.to_numpy(dtype=float)
    rows.append({
        "host": row["host"], "CID": row["CID"], "multiplicity": len(indices),
        "m0_Bi": float(source.m0),
        "mean_m_b_corr": float(mbc.mean()),
        "difference_mean_minus_m0": float(mbc.mean() - source.m0),
        "mean_MU_SH0ES": float(mu.mean()),
        "max_abs_pairwise_m_b_corr": float(np.max(mbc) - np.min(mbc)),
    })
for subset_name, subset in [("all47", rows), ("multi26", [r for r in rows if r["multiplicity"] > 1]), ("single21", [r for r in rows if r["multiplicity"] == 1])]:
    differences = np.array([r["difference_mean_minus_m0"] for r in subset])
    print(subset_name, json.dumps({
        "count": len(subset),
        "max_abs_difference": float(np.max(np.abs(differences))),
        "median_abs_difference": float(np.median(np.abs(differences))),
        "within_0.0005": int(np.sum(np.abs(differences) <= 0.0005)),
        "within_0.001": int(np.sum(np.abs(differences) <= 0.001)),
        "within_0.005": int(np.sum(np.abs(differences) <= 0.005)),
        "within_0.01": int(np.sum(np.abs(differences) <= 0.01)),
    }))
for row in rows:
    print(json.dumps(row))
