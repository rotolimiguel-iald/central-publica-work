from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.stats import norm

BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
OUT = Path(r"C:\IALD\Central de Patentes\work\kimi_h0dn_discriminante_06nov\DISCRIMINANTE_CONJUNTO.json")
Q = float(norm.ppf(0.975))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wilson(success: int, total: int) -> dict:
    phat = success / total
    z = float(norm.ppf(0.975))
    den = 1 + z * z / total
    center = (phat + z * z / (2 * total)) / den
    radius = z * math.sqrt(phat * (1 - phat) / total + z * z / (4 * total * total)) / den
    return {
        "success": int(success),
        "total": int(total),
        "estimate": phat,
        "ci95": [center - radius, center + radius],
    }


def joint_gaussian(mu_x: float, mu_y: float, rho: float) -> float:
    """P(X>=5, |Y|<=Q) for standardized bivariate normal (X,Y)."""
    conditional_sd = math.sqrt(max(1e-30, 1 - rho * rho))

    def integrand(y: float) -> float:
        conditional_mean_x = mu_x + rho * (y - mu_y)
        return float(norm.pdf(y - mu_y) * norm.sf((5 - conditional_mean_x) / conditional_sd))

    value, error = quad(integrand, -Q, Q, epsabs=1e-12, epsrel=1e-11, limit=200)
    if not math.isfinite(value) or error > 1e-7:
        raise ValueError(("quadrature_failed", value, error))
    return float(value)


results = json.loads((BASE / "blind_custodian/UNBLINDED_RESULTS.json").read_text(encoding="utf-8"))
manifest = json.loads((BASE / "blind_custodian/SCORES_MANIFEST.json").read_text(encoding="utf-8"))
background = json.loads((BASE / "background/BG1.json").read_text(encoding="utf-8"))

with np.load(BASE / "estimator_frozen.npz", allow_pickle=False) as src:
    est = {key: src[key] for key in src.files}
with np.load(BASE / "network/network.npz", allow_pickle=False) as src:
    C = src["C"].copy()

cb = np.asarray(background["covariance"], dtype=float)
gh = np.asarray(background["gradient_h"], dtype=float)
gk = np.asarray(background["gradient_k"], dtype=float)
logk = float(est["logK"])
model_names = [str(x) for x in est["model_names"]]

analytic = {}
for index, name in enumerate(model_names):
    w = est["weights"][index]
    vh = float(w @ C @ w)
    sd0 = float(est["sd_null"][index])
    sdt = float(est["sd_tgl"][index])
    cross = vh + float(gh @ cb @ (gh + gk))
    rho = cross / (sd0 * sdt)
    if abs(rho) >= 1:
        raise ValueError(("invalid_correlation", name, rho))
    d = logk / sd0
    mu_tgl_null = -logk / sdt
    analytic[name] = {
        "D_null_units": d,
        "correlation_z_null_z_tgl": rho,
        "mean_z_tgl_under_null": mu_tgl_null,
        "power_joint_under_TGL": joint_gaussian(d, 0.0, rho),
        "false_joint_under_null": joint_gaussian(0.0, mu_tgl_null, rho),
        "power_null_only_under_TGL": float(norm.sf(5 - d)),
        "coverage95_TGL_only": 0.95,
    }

rows = []
checked_scores = 0
for case in results["outputs"]:
    if case["kind"] != "ordinary":
        continue
    blocks = sorted(
        [row for row in manifest if row["case_id"] == case["id"]],
        key=lambda row: row["first"],
    )
    if len(blocks) != 4:
        raise ValueError(("unexpected_block_count", case["id"], len(blocks)))
    arrays = {"z_null": [], "z_tgl": []}
    for block in blocks:
        path = Path(block["score_path"])
        if sha(path) != block["score_sha256"]:
            raise ValueError("score_hash_mismatch:" + str(path))
        checked_scores += 1
        with np.load(path, allow_pickle=False) as score:
            arrays["z_null"].append(score["z_null"])
            arrays["z_tgl"].append(score["z_tgl"])
    arrays = {key: np.concatenate(parts, axis=0) for key, parts in arrays.items()}
    for index, name in enumerate(model_names):
        z = arrays["z_null"][:, index]
        zt = arrays["z_tgl"][:, index]
        reject = z >= 5
        compatible = np.abs(zt) <= Q
        joint = reject & compatible
        model_report = case["models"][index]
        if model_report["name"] != name:
            raise ValueError("model_order_mismatch")
        if int(reject.sum()) != model_report["rejection"]["success"]:
            raise ValueError("rejection_reproduction_failed")
        if case["hypothesis"] == 1:
            expected = model_report["TGL_compatibility_coverage95"]["success"]
            if int(compatible.sum()) != expected:
                raise ValueError("coverage_reproduction_failed")
        rows.append({
            "case_id": case["id"],
            "hypothesis": int(case["hypothesis"]),
            "fixed_bias": float(case["fixed_bias"]),
            "random_sd": float(case["random_sd"]),
            "model": name,
            "null_rejection": wilson(int(reject.sum()), len(z)),
            "tgl_compatibility95": wilson(int(compatible.sum()), len(z)),
            "joint_discrimination_candidate": wilson(int(joint.sum()), len(z)),
            "joint_among_null_rejections": float(joint.sum() / reject.sum()) if reject.any() else None,
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
            "empirical_joint": row["joint_discrimination_candidate"],
            "analytic_joint": (
                analytic[name]["power_joint_under_TGL"] if hypothesis == 1
                else analytic[name]["false_joint_under_null"]
            ),
        }

payload = {
    "status": "EXPLORATORY_JOINT_DISCRIMINATION_ON_FROZEN_SYNTHETIC_SCORES",
    "rule_candidate": "z_null >= 5 AND abs(z_tgl) <= 1.959963984540054",
    "rule_status": "POST_HOC_EXPLORATORY_REQUIRES_PROSPECTIVE_FREEZE_BEFORE_ANY_DECISIVE_USE",
    "observed_data_used": False,
    "new_seeds_generated": False,
    "new_observed_fit": False,
    "nature_verdict": False,
    "gate_effect": "NONE",
    "score_blocks_hash_verified": checked_scores,
    "source_counts_reproduced": True,
    "analytic_no_nuisance": analytic,
    "summary_no_nuisance": summary,
    "ordinary_scenarios": rows,
    "sources": [
        {"path": str(BASE / "blind_custodian/UNBLINDED_RESULTS.json"), "sha256": sha(BASE / "blind_custodian/UNBLINDED_RESULTS.json")},
        {"path": str(BASE / "blind_custodian/SCORES_MANIFEST.json"), "sha256": sha(BASE / "blind_custodian/SCORES_MANIFEST.json")},
        {"path": str(BASE / "estimator_frozen.npz"), "sha256": sha(BASE / "estimator_frozen.npz")},
        {"path": str(BASE / "network/network.npz"), "sha256": sha(BASE / "network/network.npz")},
        {"path": str(BASE / "background/BG1.json"), "sha256": sha(BASE / "background/BG1.json")},
    ],
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": payload["status"],
    "score_blocks_hash_verified": checked_scores,
    "summary_no_nuisance": summary,
    "output": str(OUT),
    "output_sha256": sha(OUT),
}, ensure_ascii=False, indent=2))
