from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

HERE = Path(r"C:\IALD\Central de Patentes\work\kimi_h0dn_discriminante_06nov")
BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
FULL_PATH = HERE / "Pantheon+SH0ES_STAT+SYS.cov"
STAT_PATH = HERE / "Pantheon+SH0ES_STATONLY.cov"
VPEC_PATH = HERE / "Pantheon+SH0ES_122221_VPEC.cov"
OUT_JSON = HERE / "COVARIANCA_COMPONENTES.json"
OUT_NPZ = HERE / "covariancia_componentes.npz"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


ASYMMETRY = {}


def load_cov(path: Path) -> np.ndarray:
    with path.open("r", encoding="ascii") as handle:
        n = int(handle.readline().strip())
    matrix = np.loadtxt(path, skiprows=1)
    if matrix.size == n * n:
        matrix = matrix.reshape(n, n)
    if matrix.shape != (n, n):
        raise ValueError(("covariance_shape", path, matrix.shape, n))
    if not np.isfinite(matrix).all():
        raise ValueError("nonfinite_covariance")
    asymmetry = float(np.max(np.abs(matrix - matrix.T)))
    if asymmetry > 1e-6:
        raise ValueError(("asymmetric_covariance", asymmetry))
    ASYMMETRY[str(path)] = asymmetry
    return 0.5 * (matrix + matrix.T)


def stats(block: np.ndarray) -> dict:
    diag = np.diag(block)
    off = block[~np.eye(len(block), dtype=bool)] if len(block) > 1 else np.array([])
    return {
        "shape": list(block.shape),
        "diag_min": float(diag.min()),
        "diag_max": float(diag.max()),
        "offdiag_abs_max": float(np.max(np.abs(off))) if off.size else 0.0,
        "frobenius_norm": float(np.linalg.norm(block)),
        "eigen_min": float(np.linalg.eigvalsh(block)[0]),
        "eigen_max": float(np.linalg.eigvalsh(block)[-1]),
    }


full = load_cov(FULL_PATH)
stat = load_cov(STAT_PATH)
vpec = load_cov(VPEC_PATH)
sys_delta = full - stat
vpec_delta = vpec - stat

mapping = json.loads((BASE / "cross_rung/mapping.json").read_text(encoding="utf-8"))
rows = json.loads((BASE / "network/rows.json").read_text(encoding="utf-8"))
with np.load(BASE / "cross_rung/raw_cross_diagnostic.npz", allow_pickle=False) as raw:
    hf_indices = raw["hf_pp_indices"].copy()
    hf_weights = raw["weights"].copy()
    full_cross_alpha = raw["raw_pp_to_alpha_covariance"].copy()

cal_indices = np.array(sorted({i for row in mapping for i in row["pp_indices"]}), dtype=int)
if len(cal_indices) != 82 or len(hf_indices) != 277:
    raise ValueError("unexpected_mapping_dimensions")
if not np.allclose(-0.2 * full[:, hf_indices] @ hf_weights, full_cross_alpha, atol=2e-12, rtol=1e-10):
    raise ValueError("full_cross_alpha_reproduction_failed")

# The 55 calibrator rows are 179..233; the compressed Hubble-flow intercept is row 248.
singleton_network = []
singleton_release = []
singleton_hosts = []
for j, row in enumerate(mapping):
    network_row = 179 + j
    if rows[network_row].get("kind") != "sn1a_calibrator":
        raise ValueError(("network_calibrator_order", j, rows[network_row]))
    if rows[network_row].get("host") != row["host"]:
        raise ValueError(("network_host_mismatch", j, rows[network_row].get("host"), row["host"]))
    if len(row["pp_indices"]) == 1:
        singleton_network.append(network_row)
        singleton_release.append(row["pp_indices"][0])
        singleton_hosts.append(row["host"])
singleton_network = np.asarray(singleton_network, dtype=int)
singleton_release = np.asarray(singleton_release, dtype=int)
if len(singleton_network) != 21 or rows[248].get("kind") != "sn1a_hubble_flow":
    raise ValueError("singleton_or_hf_mapping_failed")


def cross_alpha(matrix: np.ndarray) -> np.ndarray:
    return -0.2 * matrix[:, hf_indices] @ hf_weights


stat_cross_alpha = cross_alpha(stat)
vpec_cross_alpha = cross_alpha(vpec)
vpec_delta_cross_alpha = cross_alpha(vpec_delta)
sys_delta_cross_alpha = full_cross_alpha - stat_cross_alpha

blocks = {
    "cal": cal_indices,
    "hf": hf_indices,
}
arrays = {
    "cal_release_indices": cal_indices,
    "hf_release_indices": hf_indices,
    "hf_weights": hf_weights,
    "singleton_network_rows": singleton_network,
    "singleton_release_indices": singleton_release,
    "singleton_hosts": np.asarray(singleton_hosts),
    "full_cross_alpha": full_cross_alpha,
    "stat_cross_alpha": stat_cross_alpha,
    "vpec_cross_alpha": vpec_cross_alpha,
    "vpec_delta_cross_alpha": vpec_delta_cross_alpha,
    "sys_delta_cross_alpha": sys_delta_cross_alpha,
}
summary_blocks = {}
for name, indices in blocks.items():
    ix = np.ix_(indices, indices)
    arrays[f"{name}_full"] = full[ix]
    arrays[f"{name}_stat"] = stat[ix]
    arrays[f"{name}_vpec"] = vpec[ix]
    arrays[f"{name}_sys_delta"] = sys_delta[ix]
    arrays[f"{name}_vpec_delta"] = vpec_delta[ix]
    summary_blocks[name] = {
        "full": stats(full[ix]),
        "stat": stats(stat[ix]),
        "vpec": stats(vpec[ix]),
        "sys_delta": stats(sys_delta[ix]),
        "vpec_delta": stats(vpec_delta[ix]),
    }

cross_indices = np.ix_(cal_indices, hf_indices)
arrays["cross_full"] = full[cross_indices]
arrays["cross_stat"] = stat[cross_indices]
arrays["cross_vpec"] = vpec[cross_indices]
arrays["cross_sys_delta"] = sys_delta[cross_indices]
arrays["cross_vpec_delta"] = vpec_delta[cross_indices]

cross_summary = {}
for name, values in [
    ("full", full_cross_alpha),
    ("stat", stat_cross_alpha),
    ("vpec", vpec_cross_alpha),
    ("vpec_delta", vpec_delta_cross_alpha),
    ("sys_delta", sys_delta_cross_alpha),
]:
    matched = values[cal_indices]
    singles = values[singleton_release]
    cross_summary[name] = {
        "matched82_abs_max": float(np.max(np.abs(matched))),
        "matched82_l2": float(np.linalg.norm(matched)),
        "singleton21_abs_max": float(np.max(np.abs(singles))),
        "singleton21_l2": float(np.linalg.norm(singles)),
    }

with OUT_NPZ.open("xb") as handle:
    np.savez_compressed(handle, **arrays)

payload = {
    "status": "PUBLIC_COVARIANCE_COMPONENTS_PREPARED__AGGREGATION_STILL_OPEN",
    "observed_magnitude_or_modulus_centers_read": False,
    "observed_fit": False,
    "transplant_into_H0DN_performed": False,
    "components": {
        "full": "Pantheon+SH0ES_STAT+SYS.cov",
        "stat": "Pantheon+SH0ES_STATONLY.cov",
        "vpec_file": "Pantheon+SH0ES_122221_VPEC.cov",
        "sys_delta": "full - stat; includes Cepheid-host covariance and must not be transplanted wholesale",
        "vpec_delta": "vpec_file - stat; arithmetic component for audit, not an automatically additive H0DN term",
    },
    "mapping": {
        "matched_calibrator_light_curves": len(cal_indices),
        "exact_matched_calibrator_IDs": sum(bool(row["pp_indices"]) for row in mapping),
        "singleton_calibrators": len(singleton_network),
        "multi_curve_calibrators_pending_weights": sum(len(row["pp_indices"]) > 1 for row in mapping),
        "absent_IDs": [row["CID"] for row in mapping if not row["pp_indices"]],
        "unverified_aliases": {"2008fv": "2008fv_comb", "1994D": "1994DRichmond"},
        "hf_curves": len(hf_indices),
        "network_rows_verified": True,
    },
    "subblocks": summary_blocks,
    "cross_to_compressed_HF": cross_summary,
    "outputs": {"npz": str(OUT_NPZ), "npz_sha256": sha(OUT_NPZ)},
    "sources": [
        {
            "path": str(FULL_PATH),
            "sha256": sha(FULL_PATH),
            "url": "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES_STAT%2BSYS.cov",
            "github_blob_sha": "d1a1498154e7ba826df14bdbef35ebcb7f5efba1",
        },
        {
            "path": str(STAT_PATH),
            "sha256": sha(STAT_PATH),
            "url": "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES_STATONLY.cov",
            "github_blob_sha": "bd0fef3f25150a3aee5100b3f35c895cbdf63235",
        },
        {
            "path": str(VPEC_PATH),
            "sha256": sha(VPEC_PATH),
            "url": "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/sytematic_groupings/Pantheon%2BSH0ES_122221_VPEC.cov",
            "github_blob_sha": "ecc6e59a3e954f93ece55f0883c3cf104d9329fc",
        },
        {"path": str(BASE / "cross_rung/mapping.json"), "sha256": sha(BASE / "cross_rung/mapping.json")},
        {"path": str(BASE / "cross_rung/raw_cross_diagnostic.npz"), "sha256": sha(BASE / "cross_rung/raw_cross_diagnostic.npz")},
        {"path": str(BASE / "network/rows.json"), "sha256": sha(BASE / "network/rows.json")},
    ],
    "remaining_blockers": [
        "Recover the aggregation weights for the 26 multi-curve matched calibrators.",
        "Validate the two aliases and resolve all eight absent IDs without guessing identity.",
        "Separate Cepheid-host covariance from SN-only/host/PV components before changing H0DN.",
        "Audit H0DN additional velocity variance against the HF covariance already present.",
    ],
}
OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": payload["status"],
    "mapping": payload["mapping"],
    "cross_to_compressed_HF": cross_summary,
    "json": str(OUT_JSON),
    "json_sha256": sha(OUT_JSON),
    "npz": str(OUT_NPZ),
    "npz_sha256": sha(OUT_NPZ),
}, ensure_ascii=False, indent=2))
