from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent / "astra_bell_fock_tt_05nov/h0dn_bg1_06nov"
PP = Path(r"C:\IALD\observaveis_tgl\tgl_data_cache\pantheon\Pantheon+SH0ES.dat")
OUT = HERE / "G1_G42_COVARIANCE_SCENARIOS.json"
OUT_NPZ = HERE / "g42_aggregation_covariance.npz"
Q = float(norm.ppf(0.975))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_cov(path: Path) -> np.ndarray:
    raw = np.loadtxt(path)
    n = int(raw[0])
    matrix = raw[1:].reshape(n, n)
    return 0.5 * (matrix + matrix.T)


def joint_gaussian(mu_x: float, rho: float) -> float:
    conditional_sd = math.sqrt(max(1e-30, 1 - rho * rho))

    def integrand(y: float) -> float:
        mean_x = mu_x + rho * y
        return float(norm.pdf(y) * norm.sf((5 - mean_x) / conditional_sd))

    value, error = quad(integrand, -Q, Q, epsabs=1e-11, epsrel=1e-10, limit=200)
    if error > 1e-7:
        raise ValueError(("quadrature_failed", value, error))
    return float(value)


pp = pd.read_csv(PP, sep=r"\s+", usecols=["CID", "IS_CALIBRATOR"], dtype={"CID": str})
mapping = json.loads((BASE / "cross_rung/mapping.json").read_text(encoding="utf-8"))[:42]
full = load_cov(HERE.parent / "Pantheon+SH0ES_STAT+SYS.cov")
stat = load_cov(HERE.parent / "Pantheon+SH0ES_STATONLY.cov")
vpec = load_cov(HERE.parent / "Pantheon+SH0ES_122221_VPEC.cov")
with np.load(BASE / "cross_rung/raw_cross_diagnostic.npz", allow_pickle=False) as raw:
    hf_indices = raw["hf_pp_indices"].copy()
    hf_weights = raw["weights"].copy()
with np.load(BASE / "network/network.npz", allow_pickle=False) as net:
    A = net["A"].copy()
    C0 = net["C"].copy()
    c = net["c_cepheid"].copy()
    h_index = int(net["h_index"])
with np.load(BASE / "estimator_frozen.npz", allow_pickle=False) as frozen:
    sd0_reference = frozen["sd_null"].copy()
    sdt_reference = frozen["sd_tgl"].copy()
    logk = float(frozen["logK"])
bg = json.loads((BASE / "background/BG1.json").read_text(encoding="utf-8"))
cb = np.asarray(bg["covariance"], dtype=float)
gh = np.asarray(bg["gradient_h"], dtype=float)
gk = np.asarray(bg["gradient_k"], dtype=float)
vb = float(gh @ cb @ gh)
vbt = float((gh + gk) @ cb @ (gh + gk))
cross_bg = float(gh @ cb @ (gh + gk))

G = np.zeros((42, len(pp)))
groups = []
for j, item in enumerate(mapping):
    if item["CID"] == "2008fv":
        indices = pp.index[pp.CID == "2008fv_comb"].tolist()
    else:
        indices = item["pp_indices"]
    if not indices:
        raise ValueError(("missing_R22_calibrator", item["CID"]))
    if not all(int(pp.iloc[index].IS_CALIBRATOR) == 1 for index in indices):
        raise ValueError(("not_SH0ES_calibrator", item["CID"], indices))
    G[j, indices] = 1 / len(indices)
    groups.append({"row": j, "host": item["host"], "CID": item["CID"], "pp_indices": indices})
if np.count_nonzero(G.sum(axis=0)) == 0 or not np.allclose(G.sum(axis=1), 1):
    raise ValueError("aggregation_normalization_failed")


def import_geometry():
    import importlib.util
    spec = importlib.util.spec_from_file_location("r2_estimator", BASE / "estimator.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.geometry


geometry = import_geometry()
components = {"full": full, "stat": stat, "vpec": vpec}
scenarios = []
arrays = {"G": G, "group_pp_indices": np.array([g["pp_indices"] for g in groups], dtype=object)}
for name, matrix in components.items():
    cov42 = G @ matrix @ G.T
    cross_alpha42 = G @ (-0.2 * matrix[:, hf_indices] @ hf_weights)
    arrays[f"cov42_{name}"] = cov42
    arrays[f"cross_alpha42_{name}"] = cross_alpha42
    Cnew = C0.copy()
    idx = np.arange(179, 221)
    Cnew[np.ix_(idx, idx)] = cov42
    Cnew[idx, 248] = cross_alpha42
    Cnew[248, idx] = cross_alpha42
    try:
        models, metadata, null = geometry(A, Cnew, c, h_index)
    except Exception as exc:
        scenarios.append({"component": name, "geometry_status": "REFUSED", "error": str(exc)})
        continue
    record = {
        "component": name,
        "geometry_status": "PASS_WITH_SCOPE",
        "metadata": metadata,
        "cross_alpha42_abs_max": float(np.max(np.abs(cross_alpha42))),
        "cross_alpha42_l2": float(np.linalg.norm(cross_alpha42)),
        "models": {},
    }
    for i, (model_name, model) in enumerate(models.items()):
        vh = float(model["variance_h"])
        sd0 = math.sqrt(vh + vb)
        sdt = math.sqrt(vh + vbt)
        d = logk / sd0
        rho = (vh + cross_bg) / (sd0 * sdt)
        record["models"][model_name] = {
            "variance_h": vh,
            "sd_null": sd0,
            "sd_tgl": sdt,
            "D": d,
            "power_null_only": float(norm.sf(5 - d)),
            "power_joint_linear_analytic": joint_gaussian(d, rho),
            "correlation": rho,
            "reference_sd_null": float(sd0_reference[i]),
            "reference_sd_tgl": float(sdt_reference[i]),
        }
    scenarios.append(record)

with OUT_NPZ.open("xb") as handle:
    np.savez_compressed(handle, **arrays)

payload = {
    "status": "G42_AGGREGATION_SOLVED__SCENARIOS_NOT_PHYSICAL_ADMISSION",
    "aggregation": {
        "rule": "unweighted arithmetic mean of light curves within each SH0ES calibrator",
        "R22_calibrators": 42,
        "multi_curve_calibrators": sum(len(g["pp_indices"]) > 1 for g in groups),
        "single_curve_calibrators": sum(len(g["pp_indices"]) == 1 for g in groups),
        "all_IS_CALIBRATOR_one": True,
        "mean_m0_error_previously_verified_max_mag": 0.000499725341796875,
        "source_confirmation_still_required": True,
    },
    "scope": {
        "observed_H0_fit": False,
        "new_seeds": False,
        "physical_covariance_admitted": False,
        "extra_13_calibrators_closed": False,
        "cepheid_host_double_counting_resolved": False,
        "thresholds_recomputed_exact_BG": False,
        "note": "These are covariance sensitivity scenarios using the G42 bridge. STAT+SYS may duplicate Cepheid-host information; extra 13 H0DN calibrators remain in their published diagonal form.",
    },
    "groups": groups,
    "scenarios": scenarios,
    "outputs": {"npz": str(OUT_NPZ), "npz_sha256": sha(OUT_NPZ)},
    "sources": [
        {"path": str(HERE.parent / "Pantheon+SH0ES_STAT+SYS.cov"), "sha256": sha(HERE.parent / "Pantheon+SH0ES_STAT+SYS.cov")},
        {"path": str(HERE.parent / "Pantheon+SH0ES_STATONLY.cov"), "sha256": sha(HERE.parent / "Pantheon+SH0ES_STATONLY.cov")},
        {"path": str(HERE.parent / "Pantheon+SH0ES_122221_VPEC.cov"), "sha256": sha(HERE.parent / "Pantheon+SH0ES_122221_VPEC.cov")},
        {"path": str(BASE / "network/network.npz"), "sha256": sha(BASE / "network/network.npz")},
        {"path": str(BASE / "estimator_frozen.npz"), "sha256": sha(BASE / "estimator_frozen.npz")},
        {"path": str(BASE / "background/BG1.json"), "sha256": sha(BASE / "background/BG1.json")},
    ],
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": payload["status"],
    "aggregation": payload["aggregation"],
    "scenarios": scenarios,
    "output": str(OUT),
    "output_sha256": sha(OUT),
}, ensure_ascii=False, indent=2))
