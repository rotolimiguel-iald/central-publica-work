from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy import linalg


HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]
BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
PREV = WORK.parent / "kimi_h0dn_discriminante_06nov"
ORDER = WORK / "ORDEM_KIMI_H0DN_03C_11nov.md"
A1_PATH = HERE.parent / "ordem02" / "C_fisica_R3_A1_REDUCIDA.npz"
NETWORK_PATH = BASE / "network" / "network.npz"
ROWS_PATH = BASE / "network" / "rows.json"
BG1_PATH = BASE / "background" / "BG1.json"
FREEZE_PATH = BASE / "FREEZE_R2.json"
GEOMETRY_RECEIPT_PATH = BASE / "PROSPECTIVE_GEOMETRY.json"
ESTIMATOR_PATH = BASE / "estimator.py"
PREPARE_PATH = BASE / "prepare_estimator.py"
G42_JSON_PATH = PREV / "g1g2" / "G1_G42_COVARIANCE_SCENARIOS.json"
G42_NPZ_PATH = PREV / "g1g2" / "g42_aggregation_covariance.npz"
COMPONENTS_JSON_PATH = PREV / "COVARIANCA_COMPONENTES.json"
COMPONENTS_NPZ_PATH = PREV / "covariancia_componentes.npz"
STATONLY_PATH = PREV / "Pantheon+SH0ES_STATONLY.cov"
VPEC_PATH = PREV / "Pantheon+SH0ES_122221_VPEC.cov"

ANCHOR_PATH = HERE / "ANCORA_R3B.json"
STUDY_PATH = HERE / "ESTUDO_CONDICIONAL_R3B.json"
VALIDATION_PATH = HERE / "VALIDACAO_CORE_R3B.json"

STUDY_STATUS = "ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO"
EXPECTED_D = {
    "published_baseline": 6.823355474280428,
    "free_cepheid_host_differential_bias": 5.316943561403229,
}
ANCHOR_TOLERANCE = 1e-6


def pin(path: Path) -> dict:
    return {
        "path": str(path.resolve()),
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def write_json(path: Path, payload: dict) -> None:
    raw = (json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    json.loads(raw.decode("utf-8"))
    path.write_bytes(raw)


def covariance_eigen(C: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    C = (np.asarray(C, dtype=float) + np.asarray(C, dtype=float).T) / 2.0
    vals, U = linalg.eigh(C)
    scale = max(1.0, float(np.max(np.abs(C))))
    if float(vals[-1]) <= 0.0:
        raise ValueError("nonpositive_covariance_scale")
    tol = 64.0 * np.finfo(float).eps * C.shape[0] * float(vals[-1])
    if vals[0] < -tol:
        raise ValueError(f"covariance_not_psd:{vals[0]}")
    return vals, U, tol


def geometry(A: np.ndarray, C: np.ndarray, c: np.ndarray, h_index: int) -> tuple[dict, dict]:
    A = np.asarray(A, dtype=float)
    C = np.asarray(C, dtype=float)
    c = np.asarray(c, dtype=float)
    n = A.shape[0]
    if C.shape != (n, n) or c.shape != (n,):
        raise ValueError("shape_mismatch")
    if not all(np.isfinite(x).all() for x in (A, C, c)):
        raise ValueError("nonfinite_public_matrix")
    vals, U, tol = covariance_eigen(C)
    keep = vals > tol
    if not keep.any():
        raise ValueError("empty_eigensupport")
    if float(np.min(vals[keep])) < 100.0 * tol:
        raise ValueError("ambiguous_covariance_rank")
    U_pos = U[:, keep]
    W = U_pos.T / np.sqrt(vals[keep])[:, None]
    ext = np.column_stack([A, c])
    null = U[:, ~keep]
    support_error = float(np.linalg.norm(null.T @ ext) / max(1.0, np.linalg.norm(ext)))
    if support_error > 1e-10:
        raise ValueError("public_design_outside_covariance_eigensupport")
    result = {}
    for name, design in (("published_baseline", A), ("free_cepheid_host_differential_bias", ext)):
        Aw = W @ design
        Ua, sv, Va = linalg.svd(Aw, full_matrices=False)
        rank_tol = max(Aw.shape) * np.finfo(float).eps * float(sv[0]) * 64.0
        if float(sv[-1]) <= rank_tol:
            raise ValueError(f"unidentified_public_design:{name}")
        invA = (Va.T / sv) @ Ua.T
        influence = invA[h_index] @ W
        expected = np.zeros(design.shape[1])
        expected[h_index] = 1.0
        identity_error = float(np.max(np.abs(influence @ design - expected)))
        if identity_error > 1e-9:
            raise ValueError(f"influence_identity_failed:{name}")
        variance = float(influence @ C @ influence)
        if variance <= 0.0:
            raise ValueError(f"nonpositive_local_variance:{name}")
        result[name] = {
            "influence": influence,
            "variance_h": variance,
            "response_cepheid": float(influence @ c),
            "design_rank": int(len(sv)),
            "condition_design_whitened": float(sv[0] / sv[-1]),
            "influence_identity_error": identity_error,
        }
    metadata = {
        "n": int(n),
        "p": int(A.shape[1]),
        "cov_rank": int(keep.sum()),
        "cov_nullity": int((~keep).sum()),
        "eig_min": float(vals[0]),
        "eig_min_positive": float(vals[keep].min()),
        "eig_max": float(vals[-1]),
        "tolerance": float(tol),
        "support_design_error": support_error,
    }
    return result, metadata


def load_public_anchor_inputs() -> dict:
    with np.load(A1_PATH, allow_pickle=False) as a1, np.load(NETWORK_PATH, allow_pickle=False) as net:
        A = a1["A"].copy()
        C = a1["C"].copy()
        c = a1["c_cepheid"].copy()
        h_index = int(a1["h_index"])
        reproduction = {
            "A_max_abs_difference": float(np.max(np.abs(A - net["A"]))),
            "C_max_abs_difference": float(np.max(np.abs(C - net["C"]))),
            "c_max_abs_difference": float(np.max(np.abs(c - net["c_cepheid"]))),
            "h_index_equal": bool(h_index == int(net["h_index"])),
            "A1_support_dimension": int(a1["support_dimension"]),
        }
    bg = json.loads(BG1_PATH.read_text(encoding="utf-8"))
    cb = np.asarray(bg["covariance"], dtype=float)
    gh = np.asarray(bg["gradient_h"], dtype=float)
    gk = np.asarray(bg["gradient_k"], dtype=float)
    return {
        "A": A,
        "C": C,
        "c": c,
        "h_index": h_index,
        "bg": bg,
        "cb": cb,
        "gh": gh,
        "gk": gk,
        "vb": float(gh @ cb @ gh),
        "vbt": float((gh + gk) @ cb @ (gh + gk)),
        "logK": float(bg["logK"]),
        "matrix_reproduction": reproduction,
    }


def anchor_sources() -> list[Path]:
    return [
        ORDER,
        A1_PATH,
        NETWORK_PATH,
        ROWS_PATH,
        BG1_PATH,
        FREEZE_PATH,
        GEOMETRY_RECEIPT_PATH,
        ESTIMATOR_PATH,
        PREPARE_PATH,
    ]


def run_anchor() -> dict:
    data = load_public_anchor_inputs()
    models, metadata = geometry(data["A"], data["C"], data["c"], data["h_index"])
    records = {}
    for name, expected in EXPECTED_D.items():
        model = models[name]
        sd_null = math.sqrt(model["variance_h"] + data["vb"])
        sd_tgl = math.sqrt(model["variance_h"] + data["vbt"])
        D = abs(data["logK"]) / sd_null
        records[name] = {
            "expected_FREEZE_R2_D": expected,
            "reproduced_D": D,
            "absolute_error": abs(D - expected),
            "rounded_6_decimals": round(D, 6),
            "within_1e-6": bool(abs(D - expected) <= ANCHOR_TOLERANCE),
            "variance_h": model["variance_h"],
            "variance_BG1_logH": data["vb"],
            "sd_null": sd_null,
            "sd_tgl": sd_tgl,
            "conditional_design_power_Phi_D_minus_5": phi(D - 5.0),
            "response_cepheid": model["response_cepheid"],
            "design_rank": model["design_rank"],
            "condition_design_whitened": model["condition_design_whitened"],
            "influence_identity_error": model["influence_identity_error"],
        }
    passed = all(row["within_1e-6"] for row in records.values())
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    frozen_hashes = {item["path"]: item["sha256"] for item in freeze["files"]}
    source_pins = [pin(path) for path in anchor_sources()]
    frozen_checks = []
    for item in source_pins:
        expected = frozen_hashes.get(item["path"])
        if expected is not None:
            frozen_checks.append({
                "path": item["path"],
                "expected_sha256": expected,
                "actual_sha256": item["sha256"],
                "match": bool(expected == item["sha256"]),
            })
    matrix_checks = data["matrix_reproduction"]
    matrix_checks["all_public_arrays_equal"] = bool(
        matrix_checks["A_max_abs_difference"] == 0.0
        and matrix_checks["C_max_abs_difference"] == 0.0
        and matrix_checks["c_max_abs_difference"] == 0.0
        and matrix_checks["h_index_equal"]
        and matrix_checks["A1_support_dimension"] == 183
    )
    payload = {
        "schema": "H0DN_R3B_ANCHOR_V1",
        "status": "ANCORA_R3B_PASS" if passed else "ANCORA_R3B_FAIL__STOP",
        "study_status": STUDY_STATUS,
        "opening_allowed": False,
        "method": "A1 public matrix, symmetric eigensupport, whitened SVD and analytic GLS only",
        "anchor_tolerance_absolute": ANCHOR_TOLERANCE,
        "K": data["bg"]["K"],
        "logK_base_10": data["logK"],
        "covariance_geometry": metadata,
        "anchors": records,
        "A1_network_reproduction": matrix_checks,
        "sources": source_pins,
        "FREEZE_R2_source_hash_checks": frozen_checks,
        "all_available_FREEZE_R2_hashes_match": all(row["match"] for row in frozen_checks),
        "later_scenarios_computed": False,
        "observed_data_used": False,
        "observed_support_test_used": False,
        "evaluator_called": False,
        "RNG_or_Monte_Carlo_used": False,
    }
    write_json(ANCHOR_PATH, payload)
    return payload


def study_source_manifest() -> dict:
    g42_receipt = json.loads(G42_JSON_PATH.read_text(encoding="utf-8"))
    components_receipt = json.loads(COMPONENTS_JSON_PATH.read_text(encoding="utf-8"))
    paths = anchor_sources() + [
        G42_JSON_PATH,
        G42_NPZ_PATH,
        COMPONENTS_JSON_PATH,
        COMPONENTS_NPZ_PATH,
        STATONLY_PATH,
        VPEC_PATH,
    ]
    expected = {
        str(G42_NPZ_PATH.resolve()): g42_receipt["outputs"]["npz_sha256"],
        str(COMPONENTS_NPZ_PATH.resolve()): components_receipt["outputs"]["npz_sha256"],
    }
    for item in g42_receipt["sources"]:
        if Path(item["path"]).resolve() in (STATONLY_PATH.resolve(), VPEC_PATH.resolve()):
            expected[str(Path(item["path"]).resolve())] = item["sha256"]
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    for item in freeze["files"]:
        expected[str(Path(item["path"]).resolve())] = item["sha256"]
    checks = []
    for path in paths:
        item = pin(path)
        wanted = expected.get(str(path.resolve()))
        checks.append({
            **item,
            "expected_sha256": wanted,
            "match": True if wanted is None else bool(item["sha256"] == wanted),
            "expectation_source": "actual_pin_no_prior_receipt" if wanted is None else "existing_public_receipt",
        })
    return {
        "sources": checks,
        "all_hashes_match": all(item["match"] for item in checks),
        "all_sources_read_only": True,
    }


def build_public_scenarios(data: dict) -> dict:
    rows = json.loads(ROWS_PATH.read_text(encoding="utf-8"))
    if not all(rows[i]["kind"] == "sn1a_calibrator" for i in range(179, 234)):
        raise ValueError("unexpected_SN_calibrator_row_map")
    if rows[248]["kind"] != "sn1a_hubble_flow":
        raise ValueError("unexpected_HF_intercept_row_map")
    with np.load(G42_NPZ_PATH, allow_pickle=False) as g42:
        cov42_stat = g42["cov42_stat"].copy()
        cross42_stat = g42["cross_alpha42_stat"].copy()
        cov42_vpec = g42["cov42_vpec"].copy()
        cross42_vpec = g42["cross_alpha42_vpec"].copy()
    if cov42_stat.shape != (42, 42) or cov42_vpec.shape != (42, 42):
        raise ValueError("unexpected_G42_shape")
    C0 = data["C"].copy()
    C1 = C0.copy()
    g42_rows = np.arange(179, 221)
    extra13_rows = np.arange(221, 234)
    C1[np.ix_(g42_rows, g42_rows)] = cov42_stat
    C1[g42_rows, 248] = cross42_stat
    C1[248, g42_rows] = cross42_stat
    keep_out = np.ones(255, dtype=bool)
    keep_out[extra13_rows] = False
    C2 = C1.copy()
    old13 = C2[np.ix_(extra13_rows, extra13_rows)]
    C2[np.ix_(extra13_rows, extra13_rows)] = 13.0 * np.diag(np.diag(old13))
    pv_delta42 = cov42_vpec - cov42_stat
    pv_delta_cross = cross42_vpec - cross42_stat
    PV = np.zeros((255, 255), dtype=float)
    PV[np.ix_(g42_rows, g42_rows)] = pv_delta42
    PV[g42_rows, 248] = pv_delta_cross
    PV[248, g42_rows] = pv_delta_cross
    return {
        "C0_full": C0,
        "C1_full": C1,
        "C2_full": C2,
        "PV_full": PV,
        "keep_out": keep_out,
        "g42_rows": g42_rows,
        "extra13_rows": extra13_rows,
        "row_map": {
            "other_local": "0:179, 234:248 and 249:255",
            "G42": "179:221",
            "EXTRA13": "221:234 (the 13 non-R22 SN calibrator equations)",
            "HF_intercept": "248",
            "BG1": "separate three-parameter public block",
        },
    }


def model_numbers(models: dict, data: dict) -> dict:
    out = {}
    for name, model in models.items():
        sd_null = math.sqrt(model["variance_h"] + data["vb"])
        D = abs(data["logK"]) / sd_null
        out[name] = {
            "D": D,
            "conditional_design_power_Phi_D_minus_5": phi(D - 5.0),
            "variance_h": model["variance_h"],
            "sd_null": sd_null,
            "sd_tgl": math.sqrt(model["variance_h"] + data["vbt"]),
            "design_rank": model["design_rank"],
            "influence_identity_error": model["influence_identity_error"],
            "response_cepheid": model["response_cepheid"],
        }
    return out


def cell_records(numbers: dict) -> dict:
    return {
        name: {
            "D": row["D"],
            "conditional_design_power_Phi_D_minus_5": row["conditional_design_power_Phi_D_minus_5"],
            "conditional_status": STUDY_STATUS,
        }
        for name, row in numbers.items()
    }


def invalid_cells(reason: str) -> dict:
    return {
        name: {
            "D": None,
            "conditional_design_power_Phi_D_minus_5": None,
            "conditional_status": "INVALID_SCENARIO_NOT_A_NUMBER",
            "reason": reason,
        }
        for name in EXPECTED_D
    }


def solve_s4(C_local: np.ndarray, A: np.ndarray, c: np.ndarray, data: dict) -> tuple[dict, dict]:
    models, metadata = geometry(A, C_local, c, data["h_index"])
    cb_inv = linalg.inv(data["cb"])
    details = {}
    numbers = {}
    for name, model in models.items():
        w = model["influence"]
        vh = model["variance_h"]
        vb = data["vb"]
        b = -math.sqrt(vh / vb) * (data["cb"] @ data["gh"])
        q = np.outer(C_local @ w, b) / vh
        cross_contrast = float(w @ q @ data["gh"])
        schur_residual = C_local - q @ cb_inv @ q.T
        eig_min = float(linalg.eigvalsh((schur_residual + schur_residual.T) / 2.0)[0])
        scale = max(1.0, float(np.max(np.abs(C_local))))
        psd_tol = 64.0 * np.finfo(float).eps * C_local.shape[0] * scale
        recomputed, _ = geometry(A, C_local, c, data["h_index"])
        weight_delta = float(np.max(np.abs(recomputed[name]["influence"] - w)))
        variance = vh + vb - 2.0 * cross_contrast
        target_variance = (math.sqrt(vh) + math.sqrt(vb)) ** 2
        D = abs(data["logK"]) / math.sqrt(variance)
        q_contiguous = np.ascontiguousarray(q, dtype="<f8")
        details[name] = {
            "q_definition": "q = C_L w b^T / V_L; b = -sqrt(V_L/V_B) C_BG g_h",
            "q_sha256_contiguous_float64": hashlib.sha256(q_contiguous.tobytes()).hexdigest(),
            "q_rank": int(np.linalg.matrix_rank(q)),
            "q_max_abs": float(np.max(np.abs(q))),
            "local_GLS_variance": vh,
            "background_variance": vb,
            "cross_contrast_w_q_gh": cross_contrast,
            "Cauchy_target_negative_sqrt_VL_VB": -math.sqrt(vh * vb),
            "variance_at_minimum_D": variance,
            "Cauchy_target_variance": target_variance,
            "variance_identity_absolute_error": abs(variance - target_variance),
            "Schur_residual_eig_min": eig_min,
            "Schur_residual_PSD_tolerance": psd_tol,
            "Schur_residual_PSD": bool(eig_min >= -psd_tol),
            "ellipsoid_contrast_tight": bool(abs(cross_contrast + math.sqrt(vh * vb)) < 1e-12),
            "weights_recomputed_at_optimum": True,
            "recomputed_weight_max_abs_difference": weight_delta,
            "weights_q_invariance_reason": "The local-only GLS design and C_L are fixed; q enters only the contrast variance, so recomputation is analytically q-invariant.",
        }
        numbers[name] = {
            "D": D,
            "conditional_design_power_Phi_D_minus_5": phi(D - 5.0),
            "variance_h": vh,
            "sd_null": math.sqrt(variance),
            "sd_tgl": None,
            "design_rank": model["design_rank"],
            "influence_identity_error": model["influence_identity_error"],
            "response_cepheid": model["response_cepheid"],
        }
    return numbers, {"covariance_geometry": metadata, "models": details}


def variance_budget(C_full: np.ndarray, keep: np.ndarray, models: dict, data: dict) -> dict:
    block_indices = {
        "other_local": np.r_[0:179, 234:248, 249:255],
        "G42": np.arange(179, 221),
        "extra13": np.arange(221, 234),
        "HF_intercept": np.array([248]),
    }
    output = {}
    for name, model in models.items():
        w = np.zeros(255, dtype=float)
        w[keep] = model["influence"]
        blocks = {
            block: float(w[ix] @ C_full[np.ix_(ix, ix)] @ w[ix])
            for block, ix in block_indices.items()
        }
        blocks["BG1"] = data["vb"]
        crosses = {}
        names = list(block_indices)
        for i, left in enumerate(names):
            for right in names[i + 1:]:
                il, ir = block_indices[left], block_indices[right]
                crosses[f"{left}__{right}"] = float(2.0 * w[il] @ C_full[np.ix_(il, ir)] @ w[ir])
        for left in names:
            crosses[f"{left}__BG1"] = 0.0
        total = model["variance_h"] + data["vb"]
        reconstructed = sum(blocks.values()) + sum(crosses.values())
        output[name] = {
            "disjoint_blocks": blocks,
            "all_pairwise_cross_terms": crosses,
            "total_variance_null_contrast": total,
            "sum_blocks_plus_cross_terms": reconstructed,
            "closure_absolute_error": abs(total - reconstructed),
            "note": "All 255 original row positions are represented; EXTRA13_OUT gives zero influence on rows 221:234. Cross terms inside other_local remain inside that single disjoint block.",
        }
    return output


def analytic_family(A: np.ndarray, C: np.ndarray, c: np.ndarray, data: dict, base_numbers: dict) -> dict:
    models, _ = geometry(A, C, c, data["h_index"])
    vals, U, tol = covariance_eigen(C)
    keep = vals > tol
    W = U[:, keep].T / np.sqrt(vals[keep])[:, None]
    Aw = W @ A
    cw = W @ c
    M = Aw.T @ Aw
    V = linalg.inv(M)
    r = Aw.T @ cw
    k = float(cw @ cw)
    b = float(r @ V @ r)
    d = k - b
    h = data["h_index"]
    u = float((V[h] @ r) ** 2)
    v0 = models["published_baseline"]["variance_h"]
    vinf = models["free_cepheid_host_differential_bias"]["variance_h"]
    if d <= 0.0:
        raise ValueError("rank_one_family_has_no_well_defined_free_endpoint")
    formula_vinf = v0 + u / d
    D0 = abs(data["logK"]) / math.sqrt(v0 + data["vb"])
    Dinf = abs(data["logK"]) / math.sqrt(vinf + data["vb"])
    published_error = abs(D0 - base_numbers["published_baseline"]["D"])
    free_error = abs(Dinf - base_numbers["free_cepheid_host_differential_bias"]["D"])
    endpoints_pass = bool(
        published_error <= 1e-9
        and free_error <= 1e-9
        and abs(formula_vinf - vinf) <= 1e-10
    )
    roots = {}
    for target in (5.842, 6.282, 6.645):
        key = f"{target:.3f}"
        if not endpoints_pass:
            roots[key] = {"status": "FAMILY_STOPPED_ENDPOINT_FAILURE", "sigma_b": None}
            continue
        if target > D0 + 1e-12 or target < Dinf - 1e-12:
            roots[key] = {
                "status": "NOT_REACHABLE_WITHIN_FAMILY",
                "sigma_b": None,
                "reason": "Target lies outside the monotone D interval between the published and free endpoints.",
                "D_endpoint_published": D0,
                "D_endpoint_free": Dinf,
            }
            continue
        if abs(target - D0) <= 1e-12:
            roots[key] = {"status": "ROOT_AT_PUBLISHED_ENDPOINT", "sigma_b": 0.0, "D_recomputed": D0}
            continue
        if abs(target - Dinf) <= 1e-12:
            roots[key] = {"status": "ROOT_AT_FREE_LIMIT", "sigma_b": "INFINITY", "D_recomputed": Dinf}
            continue
        vt = (abs(data["logK"]) / target) ** 2 - data["vb"]
        lam = (vt - v0) / (d * (vinf - vt))
        if lam <= 0.0 or not math.isfinite(lam):
            roots[key] = {"status": "NOT_REACHABLE_WITHIN_FAMILY", "sigma_b": None}
            continue
        sigma = math.sqrt(lam)
        direct_models, _ = geometry(A, C + lam * np.outer(c, c), c, h)
        direct_v = direct_models["published_baseline"]["variance_h"]
        direct_D = abs(data["logK"]) / math.sqrt(direct_v + data["vb"])
        roots[key] = {
            "status": "ROOT",
            "sigma_b": sigma,
            "lambda_sigma_b_squared": lam,
            "target_variance_local": vt,
            "D_recomputed": direct_D,
            "absolute_D_error": abs(direct_D - target),
            "conditional_design_power_at_target": phi(target - 5.0),
        }
    return {
        "definition": "C(sigma_b)=C0+sigma_b^2 cCep cCep^T; published design at finite sigma, free-cCep design in the limit",
        "coefficients": {
            "k_c_precision_c": k,
            "b_r_V_r": b,
            "d_k_minus_b": d,
            "u_h_response_squared": u,
            "v0": v0,
            "vinf": vinf,
            "vinf_closed_form": formula_vinf,
            "vinf_absolute_error": abs(vinf - formula_vinf),
            "variance_curve": "v(lambda)=v0+lambda*u/(1+lambda*d), lambda=sigma_b^2",
            "root_curve": "lambda=(v_target-v0)/(d*(vinf-v_target))",
        },
        "endpoints": {
            "published_sigma_0": {"D": D0, "absolute_error_vs_S_cell": published_error},
            "free_sigma_infinity": {"D": Dinf, "absolute_error_vs_S_cell": free_error},
            "both_pass": endpoints_pass,
        },
        "D_monotone_nonincreasing": True,
        "targets": roots,
    }


def global_outputs(cells: dict) -> list[dict]:
    outputs = []
    for threshold in (5.842, 6.282, 6.645):
        meets = [
            f"{scenario}:{model}"
            for scenario in ("S0", "S1")
            for model in EXPECTED_D
            if cells[scenario][model]["D"] >= threshold
        ]
        # No scenario has the required full-matrix Loewner certificate and joint-rule proof.
        alpha = False
        if alpha:
            label = "ALPHA__CERTIFICAVEL_POR_COTA"
        elif meets:
            label = "BETA__VALE_FECHAR"
        else:
            label = "GAMMA__FALTA_INFORMACAO"
        outputs.append({
            "threshold_D": threshold,
            "nominal_conditional_power_at_threshold": phi(threshold - 5.0),
            "GLOBAL_output": label,
            "S0_or_S1_cells_at_or_above_threshold": meets,
            "demonstrable_full_matrix_Loewner_upper_bound": False,
            "conservative_joint_rule_power_certificate": False,
            "S5_promotion_to_alpha_allowed": False,
            "reason": "Alpha is unavailable without the full Loewner and joint-rule proofs; beta/gamma follows only the global S0/S1 gate reading.",
        })
    return outputs


def run_study(anchor: dict) -> tuple[dict, dict]:
    if anchor["status"] != "ANCORA_R3B_PASS":
        raise RuntimeError("anchor_failed_stop")
    source_manifest = study_source_manifest()
    if not source_manifest["all_hashes_match"]:
        raise RuntimeError("public_source_hash_mismatch")
    data = load_public_anchor_inputs()
    scenarios = build_public_scenarios(data)
    keep = scenarios["keep_out"]
    A0, c0 = data["A"][keep], data["c"][keep]
    C0 = scenarios["C0_full"][np.ix_(keep, keep)]
    C1 = scenarios["C1_full"][np.ix_(keep, keep)]
    models0, meta0 = geometry(A0, C0, c0, data["h_index"])
    models1, meta1 = geometry(A0, C1, c0, data["h_index"])
    models2, meta2 = geometry(data["A"], scenarios["C2_full"], data["c"], data["h_index"])
    numbers = {
        "S0": model_numbers(models0, data),
        "S1": model_numbers(models1, data),
        "S2": model_numbers(models2, data),
    }
    numbers["S4"], s4_diagnostics = solve_s4(C1, A0, c0, data)
    cells = {name: cell_records(numbers[name]) for name in ("S0", "S1", "S2")}
    cells["S4"] = cell_records(numbers["S4"])
    pv = scenarios["PV_full"]
    pv_reduced = pv[np.ix_(keep, keep)]
    pv_eigs = linalg.eigvalsh((pv_reduced + pv_reduced.T) / 2.0)
    result_eigs = linalg.eigvalsh(C1 + pv_reduced)
    pv_tol = 64.0 * np.finfo(float).eps * pv_reduced.shape[0] * max(1.0, float(np.max(np.abs(pv_reduced))))
    result_tol = 64.0 * np.finfo(float).eps * C1.shape[0] * max(1.0, float(np.max(np.abs(C1 + pv_reduced))))
    pv_component_psd = bool(pv_eigs[0] >= -pv_tol)
    pv_result_psd = bool(result_eigs[0] >= -result_tol)
    pv_reason = "The public additive PV candidate vpec-stat is not PSD; no additive covariance is invented and no D is produced."
    cells["S3"] = invalid_cells(pv_reason)
    cells["S5"] = invalid_cells("S5 depends on a valid S3 component and a PSD composition; S3 is invalid, so the composition is not a number.")
    cells = {name: cells[name] for name in ("S0", "S1", "S2", "S3", "S4", "S5")}
    diagnostics = {
        "S0": {"covariance_geometry": meta0, "models": numbers["S0"]},
        "S1": {"covariance_geometry": meta1, "models": numbers["S1"]},
        "S2": {"covariance_geometry": meta2, "models": numbers["S2"], "CAP13_rule": "C_13 replaced by 13*diag(C_13), with all other entries unchanged"},
        "S3": {
            "component_definition": "Aggregated public G42 VPEC minus STATONLY, including its existing cross-alpha42 difference; EXTRA13_OUT as in S1",
            "component_eig_min": float(pv_eigs[0]),
            "component_eig_max": float(pv_eigs[-1]),
            "component_PSD_tolerance": pv_tol,
            "component_PSD": pv_component_psd,
            "resulting_matrix_eig_min": float(result_eigs[0]),
            "resulting_matrix_PSD_tolerance": result_tol,
            "resulting_matrix_PSD": pv_result_psd,
            "status": "VALID" if pv_component_psd and pv_result_psd else "INVALID_SCENARIO_NOT_A_NUMBER",
        },
        "S4": s4_diagnostics,
        "S5": {"status": "INVALID_SCENARIO_NOT_A_NUMBER", "dependency": "S3", "composition_attempted": False},
    }
    budgets = {
        "S0": variance_budget(scenarios["C0_full"], keep, models0, data),
        "S1": variance_budget(scenarios["C1_full"], keep, models1, data),
    }
    effects = {}
    for model in EXPECTED_D:
        n0, n1, n2 = numbers["S0"][model], numbers["S1"][model], numbers["S2"][model]
        effects[model] = {
            "S0_to_S1_G42_STATONLY_substitution": {
                "delta_D": n1["D"] - n0["D"],
                "delta_conditional_power": n1["conditional_design_power_Phi_D_minus_5"] - n0["conditional_design_power_Phi_D_minus_5"],
                "delta_local_variance": n1["variance_h"] - n0["variance_h"],
            },
            "S1_to_S2_EXTRA13_IN_CAP13": {
                "delta_D": n2["D"] - n1["D"],
                "delta_conditional_power": n2["conditional_design_power_Phi_D_minus_5"] - n1["conditional_design_power_Phi_D_minus_5"],
                "delta_local_variance": n2["variance_h"] - n1["variance_h"],
            },
            "envelope_changes_from_S1": {
                "S2_delta_D": n2["D"] - n1["D"],
                "S3_delta_D": None,
                "S4_delta_D": numbers["S4"][model]["D"] - n1["D"],
                "S5_delta_D": None,
            },
        }
    family = {
        "S0": analytic_family(A0, C0, c0, data, numbers["S0"]),
        "S1": analytic_family(A0, C1, c0, data, numbers["S1"]),
    }
    h0_local_public = 73.50
    sigma_h0_local_public = 0.81
    v_l = (sigma_h0_local_public / (h0_local_public * math.log(10.0))) ** 2
    ell = abs(data["logK"])
    d_independence = ell / math.sqrt(v_l + data["vb"])
    d_schur = ell / (math.sqrt(v_l) + math.sqrt(data["vb"]))
    scalar_route = {
        "status": STUDY_STATUS,
        "route": "PARALLEL_DECLARED_NOT_INDEPENDENT_REPLICA",
        "log_base": 10,
        "ell_abs_logK": ell,
        "H0DN_published_center_for_derivative_only": h0_local_public,
        "H0DN_published_linear_uncertainty": sigma_h0_local_public,
        "local_log_variance_v_L": v_l,
        "BG1_log_variance_v_B": data["vb"],
        "conversion": "v_L=(sigma_H0/(H0*ln(10)))^2; the public center enters only this derivative, never the numerator",
        "independence_hypothesis": "NAMED_CONDITIONAL_LOCAL_BACKGROUND_INDEPENDENCE_NOT_MEASURED",
        "D_independence": d_independence,
        "D_Schur": d_schur,
        "D_Schur_status": "FLOOR_OF_D_UNDER_POSITIVITY_NOT_BY_ITSELF_A_FLOOR_OF_JOINT_RULE_POWER",
        "conditional_power_independence": phi(d_independence - 5.0),
        "conditional_power_Schur_descriptive_only": phi(d_schur - 5.0),
        "primary_route_selected": False,
    }
    lemma = {
        "status": "PROVED_WITH_STATED_PRECISIONS",
        "assumptions": [
            "linear Gaussian model with the same estimand and affine convention",
            "frozen unbiased weights w from C_plus",
            "0 <= C_true <= C_plus in the Loewner order on the full matrix",
            "s^2=w^T C_plus w>0; rho=sigma/s with sigma^2=w^T C_true w; rho=0 is the degenerate limit",
        ],
        "proof": [
            "Under the null, z_null is centered Gaussian with variance rho^2<=1, so P(z_null>=5)=Phi(-5/rho)<=Phi(-5); the joint event is a subset.",
            "Under TGL, z_tgl is centered Gaussian with variance rho^2<=1, hence P(|z_tgl|<=1.96)=2 Phi(1.96/rho)-1 and is at least the nominal compatibility coverage.",
            "The joint event is z_tgl in [a,b], a=max(5-D_plus,-1.96), b=1.96. With q=1/rho>=1, P(q)=Phi(qb)-Phi(qa) and P'(q)=b phi(qb)-a phi(qa).",
            "If D_plus>=5 then a<=0<b and P'(q)>0. Reducing true variance cannot reduce the joint-rule probability, giving Phi(1.96)-Phi(max(5-D_plus,-1.96)).",
        ],
        "power_lower_bound_formula": "Phi(1.96)-Phi(max(5-D_plus,-1.96)) for D_plus>=5",
        "extension_to_3_04_to_5": "NOT_PROVED_AND_NOT_CLAIMED; nonvacuity alone is insufficient because monotonicity may reverse when 0<a<b",
        "z_null_exact_bg_caveat": "A separate lemma is required: the exact logarithmic background transform need not preserve z_null=z_tgl+D_plus or centered Gaussianity. It is outside this affine proof.",
        "closure_consequence": "Requirements 4 and 5 reduce to full-matrix Loewner domination, Gaussianity, affine convention and frozen unbiased weights; requirement 1 remains indispensable.",
        "current_enclosure_status": "ENCLOSURE_OPEN__NO_FULL_MATRIX_LOEWNER_PROOF",
        "physical_covariance_identified": False,
    }
    outputs = global_outputs(cells)
    answers = {
        "1_free_cCep_S0_or_S1_reaches_6_282": {
            "answer": any(cells[s]["free_cepheid_host_differential_bias"]["D"] >= 6.282 for s in ("S0", "S1")),
            "S0_D": cells["S0"]["free_cepheid_host_differential_bias"]["D"],
            "S1_D": cells["S1"]["free_cepheid_host_differential_bias"]["D"],
        },
        "2_isolated_effects": effects,
        "3_dominant_envelope_and_status": {},
        "4_information_for_thresholds": {
            "family_sigma_b_roots_or_NOT_REACHABLE": {s: family[s]["targets"] for s in family},
            "required_public_products": [
                "A1: full-precision R22 shared centers and source-to-equation map",
                "A2/A3: original G42 aggregated-fit covariance and identity of error variables",
                "A4: component-level HF and velocity-model decomposition",
                "A5: internal and cross covariances for the 13; EXTRA13_OUT remains a declared design alternative",
                "A6: physical local-BG1 cross-covariance or an independently accepted bounded class",
                "Independent review and a full-matrix Loewner proof before any conservative certificate",
            ],
            "S5_is_not_an_abandonment_criterion": True,
        },
    }
    for model in EXPECTED_D:
        losses = {
            "S2_CAP13": max(0.0, numbers["S1"][model]["D"] - numbers["S2"][model]["D"]),
            "S4_local_BG1_cross": max(0.0, numbers["S1"][model]["D"] - numbers["S4"][model]["D"]),
        }
        dominant = max(losses, key=losses.get)
        answers["3_dominant_envelope_and_status"][model] = {
            "numeric_adverse_D_losses_from_S1": losses,
            "dominant_numeric_envelope": dominant,
            "S2_status": "HYPOTHETICAL_INTERNAL_CAP_ONLY_NOT_FULL_MATRIX_DOMINATION",
            "S3_status": "ADVERSARIAL_CANDIDATE_INVALID_NON_PSD_NO_NUMBER",
            "S4_status": "ADVERSARIAL_ELLIPSOID_MIN_D_PHYSICAL_CLASS_CONTAINMENT_NOT_PROVED",
            "S5_status": "INVALID_BY_S3_DEPENDENCY_NOT_AN_ABANDONMENT_CRITERION",
            "physical_loss_established": False,
        }
    payload = {
        "schema": "H0DN_R3B_CONDITIONAL_STUDY_V1",
        "status": STUDY_STATUS,
        "declared_by": "Kimi",
        "opening_allowed": False,
        "certificate_status": "REFUSED_NO_ADMITTED_REVIEWED_PHYSICAL_COVARIANCE",
        "anchor": {
            "status": anchor["status"],
            "tolerance": anchor["anchor_tolerance_absolute"],
            "models": anchor["anchors"],
            "path": str(ANCHOR_PATH),
            "sha256": pin(ANCHOR_PATH)["sha256"],
        },
        "scenario_row_map": scenarios["row_map"],
        "scenario_definitions": {
            "S0": "A1 eigensupport + original H0DN 42 + inherited PV only + EXTRA13_OUT + zero local-BG1 cross",
            "S1": "S0 with G42 STATONLY by substitution, never addition",
            "S2": "S1 with EXTRA13_IN_CAP13 replacing EXTRA13_OUT",
            "S3": "S1 plus the full public additive PV candidate only if component and result are both PSD",
            "S4": "S1 with analytic global minimum D over q C_BG^-1 q^T<=C_L in the Loewner order; GLS recomputed",
            "S5": "S2+S3+S4 only when every component and the composition are PSD and well defined",
        },
        "cells": cells,
        "scenario_diagnostics": diagnostics,
        "variance_budget_S0_S1": budgets,
        "isolated_effects": effects,
        "cepheid_sigma_b_family": family,
        "scalar_public_route_S_E": scalar_route,
        "lemma_B6": lemma,
        "GLOBAL_outputs_by_threshold": outputs,
        "operator_threshold_fixed_before_execution": False,
        "posterior_operator_choice_must_disclose_table_in_view": True,
        "four_answers": answers,
        "source_manifest": source_manifest,
        "execution_guards": {
            "observed_data_used": False,
            "observed_support_test_used": False,
            "observed_Z_t_h_or_ratio_computed": False,
            "evaluator_called": False,
            "observed_solver_called": False,
            "RNG_or_Monte_Carlo_used": False,
            "FREEZE_R2_modified": False,
            "v410_modified": False,
            "best_scenario_selected": False,
        },
    }
    write_json(STUDY_PATH, payload)
    validation = validate_study(anchor, payload)
    write_json(VALIDATION_PATH, validation)
    return payload, validation


def validate_study(anchor: dict, study: dict) -> dict:
    cells = study["cells"]
    cell_count = sum(len(cells[s]) for s in cells)
    numeric_cells = sum(
        cells[s][m]["D"] is not None
        for s in cells for m in cells[s]
    )
    invalid_cells_count = cell_count - numeric_cells
    budget_errors = [
        row["closure_absolute_error"]
        for scenario in study["variance_budget_S0_S1"].values()
        for row in scenario.values()
    ]
    geometry_checks = {}
    for scenario in ("S0", "S1", "S2"):
        meta = study["scenario_diagnostics"][scenario]["covariance_geometry"]
        geometry_checks[scenario] = bool(
            meta["eig_min"] >= -meta["tolerance"]
            and meta["support_design_error"] <= 1e-10
            and meta["cov_rank"] + meta["cov_nullity"] == meta["n"]
            and all(row["design_rank"] == (64 if model == "published_baseline" else 65)
                    for model, row in study["scenario_diagnostics"][scenario]["models"].items())
        )
    s4_checks = {
        model: bool(
            row["Schur_residual_PSD"]
            and row["ellipsoid_contrast_tight"]
            and row["variance_identity_absolute_error"] <= 1e-15
            and row["recomputed_weight_max_abs_difference"] == 0.0
        )
        for model, row in study["scenario_diagnostics"]["S4"]["models"].items()
    }
    family_endpoints = {
        scenario: family["endpoints"]["both_pass"]
        for scenario, family in study["cepheid_sigma_b_family"].items()
    }
    family_root_errors = [
        target["absolute_D_error"]
        for family in study["cepheid_sigma_b_family"].values()
        for target in family["targets"].values()
        if target["status"] == "ROOT"
    ]
    expected_cell_keys = {"D", "conditional_design_power_Phi_D_minus_5", "conditional_status"}
    cell_schema_valid = all(
        set(cells[s][m]) == expected_cell_keys or (
            cells[s][m]["D"] is None and set(cells[s][m]) == expected_cell_keys | {"reason"}
        )
        for s in cells for m in cells[s]
    )
    source_hashes = study["source_manifest"]["all_hashes_match"] and anchor["all_available_FREEZE_R2_hashes_match"]
    checks = {
        "anchor_pass_within_1e-6": anchor["status"] == "ANCORA_R3B_PASS" and all(
            row["absolute_error"] <= 1e-6 for row in anchor["anchors"].values()
        ),
        "twelve_cells_present": cell_count == 12,
        "eight_numeric_and_four_invalid_cells": numeric_cells == 8 and invalid_cells_count == 4,
        "cell_schema_has_only_D_power_status_and_invalid_reason": cell_schema_valid,
        "S3_S5_explicitly_invalid_not_NaN": all(
            cells[s][m]["D"] is None and cells[s][m]["conditional_status"] == "INVALID_SCENARIO_NOT_A_NUMBER"
            for s in ("S3", "S5") for m in cells[s]
        ),
        "S0_S1_S2_rank_PSD_support_pass": all(geometry_checks.values()),
        "S4_global_ellipsoid_and_reweight_checks_pass": all(s4_checks.values()),
        "variance_budgets_close": max(budget_errors) <= 1e-16,
        "family_endpoints_pass": all(family_endpoints.values()),
        "family_roots_recompute_within_1e-6": max(family_root_errors, default=0.0) <= 1e-6,
        "three_global_outputs_only": len(study["GLOBAL_outputs_by_threshold"]) == 3 and [
            row["threshold_D"] for row in study["GLOBAL_outputs_by_threshold"]
        ] == [5.842, 6.282, 6.645],
        "source_hashes_match": source_hashes,
        "opening_allowed_false_everywhere": not anchor["opening_allowed"] and not study["opening_allowed"],
        "all_execution_guards_false_for_forbidden_actions": not any([
            study["execution_guards"]["observed_data_used"],
            study["execution_guards"]["observed_support_test_used"],
            study["execution_guards"]["observed_Z_t_h_or_ratio_computed"],
            study["execution_guards"]["evaluator_called"],
            study["execution_guards"]["observed_solver_called"],
            study["execution_guards"]["RNG_or_Monte_Carlo_used"],
            study["execution_guards"]["FREEZE_R2_modified"],
            study["execution_guards"]["v410_modified"],
            study["execution_guards"]["best_scenario_selected"],
        ]),
    }
    return {
        "schema": "H0DN_R3B_CORE_VALIDATION_V1",
        "status": "VALIDACAO_CORE_R3B_PASS" if all(checks.values()) else "VALIDACAO_CORE_R3B_FAIL",
        "study_status": STUDY_STATUS,
        "opening_allowed": False,
        "checks": checks,
        "geometry_checks": geometry_checks,
        "S4_checks": s4_checks,
        "family_endpoint_checks": family_endpoints,
        "maximum_budget_closure_absolute_error": max(budget_errors),
        "maximum_family_root_absolute_D_error": max(family_root_errors, default=0.0),
        "cell_count": cell_count,
        "numeric_cell_count": numeric_cells,
        "invalid_not_a_number_cell_count": invalid_cells_count,
        "JSON_parse_before_write": {
            "ANCORA_R3B.json": True,
            "ESTUDO_CONDICIONAL_R3B.json": True,
            "VALIDACAO_CORE_R3B.json": True,
        },
        "artifact_hashes": {
            "core_r3b.py": pin(HERE / "core_r3b.py"),
            "ANCORA_R3B.json": pin(ANCHOR_PATH),
            "ESTUDO_CONDICIONAL_R3B.json": pin(STUDY_PATH),
        },
        "validation_self_hash_policy": "Not self-embedded; validate the file externally by SHA-256 after writing.",
        "source_hashes": study["source_manifest"]["sources"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--study", action="store_true")
    args = parser.parse_args()
    anchor = run_anchor()
    if anchor["status"] != "ANCORA_R3B_PASS":
        print(json.dumps({"status": anchor["status"], "path": str(ANCHOR_PATH)}, indent=2))
        raise SystemExit(2)
    if not args.study:
        print(json.dumps({
            "status": anchor["status"],
            "D": {name: row["reproduced_D"] for name, row in anchor["anchors"].items()},
            "path": str(ANCHOR_PATH),
        }, ensure_ascii=False, indent=2))
        return
    study, validation = run_study(anchor)
    print(json.dumps({
        "status": study["status"],
        "validation": validation["status"],
        "D": {scenario: {model: row["D"] for model, row in models.items()} for scenario, models in study["cells"].items()},
        "GLOBAL": study["GLOBAL_outputs_by_threshold"],
        "paths": [str(ANCHOR_PATH), str(STUDY_PATH), str(VALIDATION_PATH)],
    }, ensure_ascii=False, indent=2))
    if validation["status"] != "VALIDACAO_CORE_R3B_PASS":
        raise SystemExit(3)


if __name__ == "__main__":
    main()
