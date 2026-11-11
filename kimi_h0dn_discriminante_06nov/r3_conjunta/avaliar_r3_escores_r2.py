from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.stats import norm

BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
OUT = Path(r"C:\IALD\Central de Patentes\work\kimi_h0dn_discriminante_06nov\r3_conjunta\R3_DIAGNOSTICO_ESCORES_R2.json")
COMPATIBILITY = float(norm.ppf(0.975))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rate(mask: np.ndarray) -> dict:
    return {"success": int(mask.sum()), "total": int(mask.size), "estimate": float(mask.mean())}


results = json.loads((BASE / "blind_custodian/UNBLINDED_RESULTS.json").read_text(encoding="utf-8"))
manifest = json.loads((BASE / "blind_custodian/SCORES_MANIFEST.json").read_text(encoding="utf-8"))
supplement = json.loads((BASE / "blind_custodian/EXACT_BG_SUPPLEMENT.json").read_text(encoding="utf-8"))
cuts = {row["name"]: float(row["exact_future_q_over_sd0"]) for row in supplement["quadrature"]}
model_names = ["published_baseline", "free_cepheid_host_differential_bias"]

rows = []
verified = 0
for case in results["outputs"]:
    if case["kind"] != "ordinary":
        continue
    blocks = sorted(
        [row for row in manifest if row["case_id"] == case["id"]],
        key=lambda row: row["first"],
    )
    arrays = {"z_null": [], "z_tgl": [], "z_null_exact_bg": []}
    for block in blocks:
        path = Path(block["score_path"])
        if sha(path) != block["score_sha256"]:
            raise ValueError("score_hash_mismatch:" + str(path))
        verified += 1
        with np.load(path, allow_pickle=False) as score:
            for key in arrays:
                arrays[key].append(score[key])
    arrays = {key: np.concatenate(parts) for key, parts in arrays.items()}
    for index, name in enumerate(model_names):
        compatible = np.abs(arrays["z_tgl"][:, index]) <= COMPATIBILITY
        linear_reject = arrays["z_null"][:, index] >= 5
        exact_reject = arrays["z_null_exact_bg"][:, index] >= cuts[name]
        rows.append({
            "case_id": case["id"],
            "hypothesis": int(case["hypothesis"]),
            "fixed_bias": float(case["fixed_bias"]),
            "random_sd": float(case["random_sd"]),
            "model": name,
            "exact_cut": cuts[name],
            "linear_null_rejection": rate(linear_reject),
            "exact_null_rejection": rate(exact_reject),
            "tgl_compatibility95": rate(compatible),
            "linear_joint": rate(linear_reject & compatible),
            "exact_joint": rate(exact_reject & compatible),
        })

summary = {}
for name in model_names:
    for hypothesis in (0, 1):
        row = next(
            row for row in rows
            if row["model"] == name
            and row["hypothesis"] == hypothesis
            and row["fixed_bias"] == 0
            and row["random_sd"] == 0
        )
        summary[f"{name}__hypothesis_{hypothesis}"] = {
            "exact_cut": cuts[name],
            "exact_null_rejection": row["exact_null_rejection"],
            "exact_joint": row["exact_joint"],
        }

payload = {
    "status": "R3_EXPLORATORY_EXACT_BG_ON_FROZEN_R2_SCORES",
    "rule": "z_null_exact_bg >= model_exact_cut AND abs(z_tgl) <= 1.959963984540054",
    "rule_status": "DIAGNOSTIC_ONLY; R3 thresholds must be recomputed after physical covariance closes",
    "new_seeds": False,
    "observed_fit": False,
    "observed_data_used": False,
    "score_blocks_hash_verified": verified,
    "summary_no_nuisance": summary,
    "ordinary_scenarios": rows,
    "sources": [
        {"path": str(BASE / "blind_custodian/UNBLINDED_RESULTS.json"), "sha256": sha(BASE / "blind_custodian/UNBLINDED_RESULTS.json")},
        {"path": str(BASE / "blind_custodian/SCORES_MANIFEST.json"), "sha256": sha(BASE / "blind_custodian/SCORES_MANIFEST.json")},
        {"path": str(BASE / "blind_custodian/EXACT_BG_SUPPLEMENT.json"), "sha256": sha(BASE / "blind_custodian/EXACT_BG_SUPPLEMENT.json")},
    ],
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": payload["status"],
    "score_blocks_hash_verified": verified,
    "summary_no_nuisance": summary,
    "output": str(OUT),
    "output_sha256": sha(OUT),
}, ensure_ascii=False, indent=2))
