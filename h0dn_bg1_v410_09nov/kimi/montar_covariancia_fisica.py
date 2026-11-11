from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np

BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
PREV = Path(r"C:\IALD\Central de Patentes\work\kimi_h0dn_discriminante_06nov")
OUT = Path(r"C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


with np.load(BASE / "network/network.npz", allow_pickle=False) as net:
    A = net["A"].copy()
    C0 = net["C"].copy()
    c = net["c_cepheid"].copy()
    h_index = int(net["h_index"])
    F_hms = net["factor_HMS"].copy()
    row_names = net["row_names"].copy()
    param_names = net["param_names"].copy()
with np.load(BASE / "estimator_frozen.npz", allow_pickle=False) as est:
    null_published = est["null_basis"].copy()
    logk = float(est["logK"])
with np.load(OUT / "y_obs.npz", allow_pickle=False) as obs:
    y = obs["y_centered"].copy()

bg = json.loads((BASE / "background/BG1.json").read_text(encoding="utf-8"))
cb = np.asarray(bg["covariance"], dtype=float)

spec = importlib.util.spec_from_file_location("r2_estimator", BASE / "estimator.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

published_host = C0[:166, :166]
host_rank = int(np.linalg.matrix_rank(published_host))
host_nullity = 166 - host_rank
assert host_nullity == 72

T_hms = F_hms @ F_hms.T
C_hms = C0 + np.diag(np.diag(T_hms))


def joint(C: np.ndarray) -> np.ndarray:
    out = np.zeros((258, 258))
    out[:255, :255] = C
    out[255:, 255:] = cb
    return out


def support(C: np.ndarray) -> dict:
    models, metadata, null = module.geometry(A, C, c, h_index)
    projection = y @ null
    max_projection = float(np.max(np.abs(projection))) if null.shape[1] else 0.0
    tolerance = 1e-8 * max(1.0, float(np.max(np.abs(y))))
    return {
        "rank": metadata["cov_rank"],
        "nullity": metadata["cov_nullity"],
        "eig_min": metadata["eig_min"],
        "eig_min_positive": metadata["eig_min_positive"],
        "tolerance_eigen": metadata["tolerance"],
        "support_design_error": metadata["support_design_error"],
        "null_basis_shape": list(null.shape),
        "max_abs_projection": max_projection,
        "tolerance": tolerance,
        "pass": bool(max_projection <= tolerance),
        "null_basis": null,
    }


published_support = support(C0)
published_support.pop("null_basis")
hms_support = support(C_hms)

arrays = {
    "C_published_joint": joint(C0),
    "C_full_HMS_diagnostic_joint": joint(C_hms),
    "BG1_covariance": cb,
    "BG1_cross_block_conditional_independence": np.zeros((255, 3)),
    "A": A,
    "c_cepheid": c,
    "row_names": row_names,
    "param_names": param_names,
    "null_basis_published": null_published,
    "null_basis_full_HMS_diagnostic": hms_support.pop("null_basis"),
    "admission": np.array(["NOT_ADMITTED_PHYSICAL_COVARIANCE_OPEN"]),
}
with np.load(PREV / "g1g2/g42_aggregation_covariance.npz", allow_pickle=False) as g42:
    for component in ["full", "stat", "vpec"]:
        cov42 = g42[f"cov42_{component}"]
        cross42 = g42[f"cross_alpha42_{component}"]
        C_new = C0.copy()
        idx = np.arange(179, 221)
        C_new[np.ix_(idx, idx)] = cov42
        C_new[idx, 248] = cross42
        C_new[248, idx] = cross42
        arrays[f"C_G42_{component}_diagnostic_joint"] = joint(C_new)

npz_path = OUT / "C_fisica_258x258.npz"
with (OUT / "C_fisica_258x258.tmp.npz").open("wb") as handle:
    np.savez_compressed(handle, **arrays)
(OUT / "C_fisica_258x258.tmp.npz").replace(npz_path)

payload = {
    "status": "G3_G4_OBSTRUCTION_EXACT__FULL_HMS_NOT_ADMITTED",
    "G1_G2": {
        "aggregation": "Arithmetic mean within each SH0ES calibrator; 42 R22, 25 multi-curve and 17 single-curve",
        "aliases": {"2008fv": "2008fv_comb", "1994D": "1994DRichmond"},
        "identity_provenance": "CLOSED",
        "evidence": str(PREV / "g1g2/G2_IDS_PROVENIENCIA_RESOLVIDA.json"),
    },
    "blocks": {
        "host_published": {
            "rank": host_rank,
            "nullity": host_nullity,
            "method": "Published diagonal mu_error plus anchor/MAS/HMS shared factors; HMS diagonal is already contained in mu_error",
            "source": str(BASE / "network/network.npz"),
        },
        "SN_only": {
            "method": "Public STATONLY aggregated by the G42 arithmetic operator; no cross covariance with compressed HF for matched calibrators",
            "source": str(PREV / "Pantheon+SH0ES_STATONLY.cov"),
            "cross_alpha42_abs_max": 0.0,
        },
        "Cepheid_host": {
            "method": "Public STAT+SYS contains Cepheid-host covariance; cannot be added wholesale without duplication",
            "source": str(PREV / "Pantheon+SH0ES_STAT+SYS.cov"),
        },
        "peculiar_velocity": {
            "method": "Public VPEC component for sensitivity, not automatic addition; H0DN adds its own velocity variance",
            "source": str(PREV / "Pantheon+SH0ES_122221_VPEC.cov"),
        },
        "BG1": {
            "method": "Independent BG1 block only under explicit conditional independence, not a measured zero cross-covariance",
            "source": str(BASE / "background/BG1.json"),
            "shape": list(cb.shape),
        },
    },
    "obstruction": {
        "published_rank": published_support["rank"],
        "published_nullity": published_support["nullity"],
        "published_support": published_support,
        "invariance": "A is in C support, so (y-Ax)N=yN for every parameter vector x; centering cannot repair support",
        "evidence": str(OUT / "TESTE_CENTRALIZACAO_PUBLICADA.json"),
    },
    "full_HMS_diagnostic": {
        "support": hms_support,
        "admitted": False,
        "reason": "HMS diagonal is already contained in host mu_error; adding it may double-count variance and is not a physical closure",
        "source_semantics": str(BASE / "network/build_network.py") + " lines 381-383",
    },
    "G42_scenarios": {
        "source": str(PREV / "g1g2/G1_G42_COVARIANCE_SCENARIOS.json"),
        "admitted": False,
        "note": "Sensitivity only; includes possible Cepheid and intrinsic-scatter duplication and leaves 13 additional calibrators outside the R22 bridge",
    },
    "remaining_open": [
        "Source-validated decomposition of host independent and shared HMS variance without duplication",
        "Covariance for the 13 additional non-R22 calibrators from their original sources",
        "Cepheid-host, intrinsic-scatter and PV decomposition before transplanting public matrices",
        "Independent review and route-selection accounting before any observed opening",
    ],
    "forbidden_actions_preserved": {
        "estimator_evaluate_called": False,
        "solver_called": False,
        "Z_t_h_or_ratio_computed": False,
        "new_R2_seed": False,
        "freeze_files_modified": False,
    },
    "outputs": {
        "npz": str(npz_path),
        "sha256": sha(npz_path),
    },
}
json_path = OUT / "DECOMPOSICAO_COVARIANCIA.json"
json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": payload["status"],
    "host_nullity": host_nullity,
    "published_support_pass": published_support["pass"],
    "published_max_projection": published_support["max_abs_projection"],
    "full_HMS_support_pass": hms_support["pass"],
    "full_HMS_rank": hms_support["rank"],
    "npz_sha256": sha(npz_path),
    "json_sha256": sha(json_path),
}, ensure_ascii=False, indent=2))
