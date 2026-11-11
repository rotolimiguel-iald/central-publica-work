from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(r"C:\IALD\Central de Patentes\work\kimi_h0dn_discriminante_06nov")
BASE = HERE.parent / "astra_bell_fock_tt_05nov/h0dn_bg1_06nov"
PP = Path(r"C:\IALD\observaveis_tgl\tgl_data_cache\pantheon\Pantheon+SH0ES.dat")
OUT1 = HERE / "g1g2/G1_CANDIDATE_AGGREGATION.json"
OUT2 = HERE / "g1g2/G2_ID_METADATA.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_cov(path: Path) -> np.ndarray:
    raw = np.loadtxt(path)
    n = int(raw[0])
    matrix = raw[1:].reshape(n, n)
    return 0.5 * (matrix + matrix.T)


def gls_sigma(C: np.ndarray) -> float:
    one = np.ones(len(C))
    return float(np.sqrt(1.0 / (one @ np.linalg.solve(C, one))))


full = load_cov(HERE / "Pantheon+SH0ES_STAT+SYS.cov")
stat = load_cov(HERE / "Pantheon+SH0ES_STATONLY.cov")
mapping = json.loads((BASE / "cross_rung/mapping.json").read_text(encoding="utf-8"))
pp = pd.read_csv(
    PP,
    sep=r"\s+",
    usecols=[
        "CID", "IDSURVEY", "zCMB", "zHEL", "RA", "DEC", "IS_CALIBRATOR",
        "USED_IN_SH0ES_HF", "m_b_corr_err_DIAG", "m_b_corr_err_RAW", "m_b_corr_err_VPEC",
    ],
    dtype={"CID": str},
)
pp["CID_lower"] = pp.CID.str.lower()

rows = []
for row in mapping:
    indices = row["pp_indices"]
    if not indices:
        continue
    cal_sigma = float(row["cal_sigma"])
    raw_errors = pp.iloc[indices].m_b_corr_err_RAW.to_numpy(dtype=float)
    full_diag = np.diag(full)[indices]
    stat_diag = np.diag(stat)[indices]
    full_gls = gls_sigma(full[np.ix_(indices, indices)])
    stat_gls = gls_sigma(stat[np.ix_(indices, indices)])
    inv_full_diag = float(np.sqrt(1 / np.sum(1 / full_diag**2)))
    inv_stat_diag = float(np.sqrt(1 / np.sum(1 / stat_diag**2)))
    inv_raw = float(np.sqrt(1 / np.sum(1 / raw_errors**2)))
    rows.append({
        "host": row["host"],
        "CID": row["CID"],
        "multiplicity": len(indices),
        "cal_sigma": cal_sigma,
        "full_gls_sigma": full_gls,
        "stat_gls_sigma": stat_gls,
        "inverse_full_diag_sigma": inv_full_diag,
        "inverse_stat_diag_sigma": inv_stat_diag,
        "inverse_raw_sigma": inv_raw,
        "ratios_to_cal_sigma": {
            "full_gls": full_gls / cal_sigma,
            "stat_gls": stat_gls / cal_sigma,
            "inverse_full_diag": inv_full_diag / cal_sigma,
            "inverse_stat_diag": inv_stat_diag / cal_sigma,
            "inverse_raw": inv_raw / cal_sigma,
        },
    })

methods = ["full_gls", "stat_gls", "inverse_full_diag", "inverse_stat_diag", "inverse_raw"]
summary = {}
for subset_name, subset in [
    ("all47_matched", rows),
    ("multi26", [row for row in rows if row["multiplicity"] > 1]),
    ("single21", [row for row in rows if row["multiplicity"] == 1]),
]:
    summary[subset_name] = {}
    for method in methods:
        ratios = np.array([row["ratios_to_cal_sigma"][method] for row in subset])
        summary[subset_name][method] = {
            "ratio_min": float(ratios.min()),
            "ratio_median": float(np.median(ratios)),
            "ratio_max": float(ratios.max()),
            "within_5pct": int(np.sum(np.abs(ratios - 1) <= 0.05)),
            "within_10pct": int(np.sum(np.abs(ratios - 1) <= 0.10)),
            "within_20pct": int(np.sum(np.abs(ratios - 1) <= 0.20)),
            "count": len(ratios),
        }

payload1 = {
    "status": "CANDIDATE_AGGREGATORS_ONLY__NO_CENTER_FIT",
    "observed_magnitude_or_modulus_centers_read": False,
    "observed_fit": False,
    "methods": summary,
    "rows": rows,
    "interpretation": "No candidate is adopted by closeness alone. A validated source-level aggregation rule is still required.",
    "sources": [
        {"path": str(HERE / "Pantheon+SH0ES_STAT+SYS.cov"), "sha256": sha(HERE / "Pantheon+SH0ES_STAT+SYS.cov")},
        {"path": str(HERE / "Pantheon+SH0ES_STATONLY.cov"), "sha256": sha(HERE / "Pantheon+SH0ES_STATONLY.cov")},
        {"path": str(BASE / "cross_rung/mapping.json"), "sha256": sha(BASE / "cross_rung/mapping.json")},
        {"path": str(PP), "sha256": sha(PP)},
    ],
}
OUT1.write_text(json.dumps(payload1, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

ids = [
    "2008fv", "2008fv_comb", "1994D", "1994DRichmond", "2021rhu", "1998bu",
    "1989B", "ASASSN-14lp", "2021J", "2020nvb",
]
metadata = {}
for cid in ids:
    selected = pp.loc[pp.CID_lower == cid.lower()].drop(columns=["CID_lower"])
    metadata[cid] = {
        "rows": len(selected),
        "records": selected.to_dict(orient="records"),
    }

payload2 = {
    "status": "PUBLIC_ID_METADATA_ONLY",
    "observed_magnitude_or_modulus_centers_read": False,
    "observed_fit": False,
    "ids": metadata,
    "source": {"path": str(PP), "sha256": sha(PP)},
    "note": "Presence of an alias is evidence for investigation, not proof of identity. Host, coordinates, redshift and original data provenance must agree.",
}
OUT2.write_text(json.dumps(payload2, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "aggregation_summary": summary,
    "id_row_counts": {key: value["rows"] for key, value in metadata.items()},
    "G1_output": str(OUT1),
    "G1_sha256": sha(OUT1),
    "G2_output": str(OUT2),
    "G2_sha256": sha(OUT2),
}, ensure_ascii=False, indent=2))
