# -*- coding: utf-8 -*-
"""ORDEM 05, item 2: estimadores S1, S2 e S4, somente de desenho.

Reconstroi as definicoes de core_r3b.py a partir das matrizes publicas.
Nao carrega vetor observado, nao chama avaliador/abertura/solver e nao usa RNG.
Todas as escritas ficam nesta pasta, ao lado deste script.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy import linalg


OUT = Path(__file__).resolve().parent
EXPECTED_OUT = Path(r"C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\ordem05\estimadores")
if OUT != EXPECTED_OUT.resolve():
    raise RuntimeError("pasta_de_escrita_inesperada")

BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
PREV = Path(r"C:\IALD\Central de Patentes\work\kimi_h0dn_discriminante_06nov")
R3B = Path(r"C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\ordem03B")
EMENDA = Path(r"C:\IALD\Central de Patentes\work\h0dn_bg1_v411_emenda_11nov")

NETWORK = BASE / "network" / "network.npz"
ROWS = BASE / "network" / "rows.json"
BG1 = BASE / "background" / "BG1.json"
G42_NPZ = PREV / "g1g2" / "g42_aggregation_covariance.npz"
G42_JSON = PREV / "g1g2" / "G1_G42_COVARIANCE_SCENARIOS.json"
CORE = R3B / "core_r3b.py"
STUDY = R3B / "ESTUDO_CONDICIONAL_R3B.json"
VALIDATION = R3B / "VALIDACAO_CORE_R3B.json"
ORDER05 = R3B.parents[1] / "ORDEM_KIMI_H0DN_05_11nov.md"
S0_NPZ = EMENDA / "artefatos" / "estimador_s0_v411.npz"
S0_MANIFEST = EMENDA / "artefatos" / "MANIFESTO_S0.json"
PACKAGE_PINS = EMENDA / "artefatos" / "PINOS.json"
V411_GEOMETRY = EMENDA / "codigo" / "estimator_v411.py"

MODELS = ("published_baseline", "free_cepheid_host_differential_bias")
STATUS = "ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO"
D_TOL = 1e-12
POWER_TOL = 1e-12


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def pin(path: Path) -> dict:
    raw = path.read_bytes()
    return {
        "path": str(path.resolve()),
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
    }


def phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def geometry(A: np.ndarray, C: np.ndarray, c: np.ndarray, h_index: int):
    """Mesma algebra de eigensuporte/SVD de core_r3b.py e da v411."""
    A = np.asarray(A, dtype=float)
    C = np.asarray(C, dtype=float)
    c = np.asarray(c, dtype=float)
    n = A.shape[0]
    if C.shape != (n, n) or c.shape != (n,):
        raise ValueError("shape_mismatch")
    if not all(np.isfinite(x).all() for x in (A, C, c)):
        raise ValueError("nonfinite_public_matrix")
    if np.max(np.abs(C - C.T)) > 1e-12 * max(1.0, float(np.max(np.abs(C)))):
        raise ValueError("asymmetric_covariance")
    vals, U = linalg.eigh((C + C.T) / 2.0)
    if float(vals[-1]) <= 0.0:
        raise ValueError("nonpositive_covariance_scale")
    tol = 64.0 * np.finfo(float).eps * n * float(vals[-1])
    if float(vals[0]) < -tol:
        raise ValueError("covariance_not_psd")
    keep = vals > tol
    if not keep.any():
        raise ValueError("empty_eigensupport")
    if float(np.min(vals[keep])) < 100.0 * tol:
        raise ValueError("ambiguous_covariance_rank")
    U_pos = U[:, keep]
    W = U_pos.T / np.sqrt(vals[keep])[:, None]
    null = U[:, ~keep]
    ext = np.column_stack([A, c])
    support_error = float(np.linalg.norm(null.T @ ext) / max(1.0, np.linalg.norm(ext)))
    if support_error > 1e-10:
        raise ValueError("public_design_outside_covariance_eigensupport")
    result = {}
    for name, design in (("published_baseline", A), ("free_cepheid_host_differential_bias", ext)):
        Aw = W @ design
        Ua, sv, Va = linalg.svd(Aw, full_matrices=False)
        rank_tol = max(Aw.shape) * np.finfo(float).eps * float(sv[0]) * 64.0
        if float(sv[-1]) <= rank_tol:
            raise ValueError("unidentified_public_design:" + name)
        invA = (Va.T / sv) @ Ua.T
        influence = invA[h_index] @ W
        expected = np.zeros(design.shape[1])
        expected[h_index] = 1.0
        identity_error = float(np.max(np.abs(influence @ design - expected)))
        if identity_error > 1e-9:
            raise ValueError("influence_identity_failed:" + name)
        variance = float(influence @ C @ influence)
        if variance <= 0.0:
            raise ValueError("nonpositive_local_variance")
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
    return result, metadata, null


def build_scenario(label: str, keep: np.ndarray, C_full: np.ndarray, public: dict, coupled: bool):
    A, c, h_full = public["A"], public["c"], public["h"]
    colmask = np.abs(A[keep]).sum(axis=0) > 0
    if not colmask[h_full]:
        raise ValueError("H0_column_removed")
    h = int(np.sum(colmask[:h_full]))
    A_local = A[keep][:, colmask]
    c_local = c[keep]
    C_local = C_full[np.ix_(keep, keep)]
    if public["param_names"][h] != "log_10(H0)":
        raise ValueError("wrong_H0_column")
    res, meta, null = geometry(A_local, C_local, c_local, h)
    n = len(keep)
    gh, gk, cb = public["gh"], public["gk"], public["cb"]
    vb, vbt, logK = public["vb"], public["vbt"], public["logK"]
    cb_inv = linalg.inv(cb)
    weights = np.stack([res[m]["influence"] for m in MODELS])
    variance_h = np.array([res[m]["variance_h"] for m in MODELS])
    q = np.zeros((2, n, 3), dtype=float)
    joint = None
    if coupled:
        joint = np.zeros((2, n + 3, n + 3), dtype=float)
    model_details = {}
    for i, model in enumerate(MODELS):
        w = weights[i]
        vh = float(variance_h[i])
        if coupled:
            b = -math.sqrt(vh / vb) * (cb @ gh)
            q[i] = np.outer(C_local @ w, b) / vh
            joint[i, :n, :n] = C_local
            joint[i, :n, n:] = q[i]
            joint[i, n:, :n] = q[i].T
            joint[i, n:, n:] = cb
        cross_null = float(w @ q[i] @ gh)
        cross_law = float(w @ q[i] @ (gh + gk))
        var_null = float(vh + vb - 2.0 * cross_null)
        var_law = float(vh + vbt - 2.0 * cross_law)
        if var_null <= 0.0 or var_law <= 0.0:
            raise ValueError("nonpositive_contrast_variance")
        schur = C_local - q[i] @ cb_inv @ q[i].T
        schur_min = float(linalg.eigvalsh((schur + schur.T) / 2.0)[0])
        psd_tol = 64.0 * np.finfo(float).eps * n * max(1.0, float(np.max(np.abs(C_local))))
        if schur_min < -psd_tol:
            raise ValueError("S4_Schur_residual_not_PSD")
        if coupled:
            target_cross = -math.sqrt(vh * vb)
            target_var = (math.sqrt(vh) + math.sqrt(vb)) ** 2
            if abs(cross_null - target_cross) >= 1e-12:
                raise ValueError("S4_ellipsoid_not_tight")
            if abs(var_null - target_var) > 1e-15:
                raise ValueError("S4_Cauchy_variance_identity_failed")
            joint_min = float(linalg.eigvalsh((joint[i] + joint[i].T) / 2.0)[0])
            joint_tol = 64.0 * np.finfo(float).eps * (n + 3) * max(1.0, float(np.max(np.abs(joint[i]))))
            if joint_min < -joint_tol:
                raise ValueError("S4_joint_covariance_not_PSD")
            contrast_null = np.r_[w, -gh]
            contrast_law = np.r_[w, -(gh + gk)]
            joint_var_null = float(contrast_null @ joint[i] @ contrast_null)
            joint_var_law = float(contrast_law @ joint[i] @ contrast_law)
            if abs(joint_var_null - var_null) > 1e-18 or abs(joint_var_law - var_law) > 1e-18:
                raise ValueError("S4_joint_quadratic_form_mismatch")
        else:
            target_cross = 0.0
            target_var = vh + vb
            joint_min = None
            joint_tol = None
        sd_null = math.sqrt(var_null)
        sd_law = math.sqrt(var_law)
        D = abs(logK) / sd_null
        model_details[model] = {
            "variance_h": vh,
            "variance_BG1_logH": vb,
            "variance_BG1_logHK": vbt,
            "cross_contrast_null_w_q_gh": cross_null,
            "cross_contrast_law_w_q_gh_plus_gk": cross_law,
            "variance_null_contrast": var_null,
            "variance_law_contrast": var_law,
            "sd_null": sd_null,
            "sd_tgl": sd_law,
            "D": D,
            "conditional_design_power_Phi_D_minus_5": phi(D - 5.0),
            "design_rank": res[model]["design_rank"],
            "condition_design_whitened": res[model]["condition_design_whitened"],
            "response_cepheid": res[model]["response_cepheid"],
            "influence_identity_error": res[model]["influence_identity_error"],
            "q_sha256_contiguous_float64": sha256_bytes(np.ascontiguousarray(q[i], dtype="<f8").tobytes()),
            "q_rank": int(np.linalg.matrix_rank(q[i])),
            "q_max_abs": float(np.max(np.abs(q[i]))),
            "Cauchy_target_cross_null": target_cross,
            "Cauchy_target_variance_null": target_var,
            "Schur_residual_eig_min": schur_min,
            "Schur_residual_PSD_tolerance": psd_tol,
            "Schur_residual_PSD": bool(schur_min >= -psd_tol),
            "joint_covariance_eig_min": joint_min,
            "joint_covariance_PSD_tolerance": joint_tol,
        }
    sd_null = np.array([model_details[m]["sd_null"] for m in MODELS])
    sd_tgl = np.array([model_details[m]["sd_tgl"] for m in MODELS])
    D = np.array([model_details[m]["D"] for m in MODELS])
    power = np.array([model_details[m]["conditional_design_power_Phi_D_minus_5"] for m in MODELS])
    arrays = {
        "scenario": np.asarray(label),
        "design_status": np.asarray(STATUS),
        "keep": np.asarray(keep, dtype=np.int64),
        "colmask": colmask,
        "h_index": np.asarray(h, dtype=np.int64),
        "h_index_network255": np.asarray(h_full, dtype=np.int64),
        "weights": weights,
        "null_basis": null,
        "gradient_h": gh,
        "gradient_k": gk,
        "variance_h": variance_h,
        "variance_background_null": np.asarray(vb),
        "variance_background_law": np.asarray(vbt),
        "cross_contrast_null": np.array([model_details[m]["cross_contrast_null_w_q_gh"] for m in MODELS]),
        "cross_contrast_law": np.array([model_details[m]["cross_contrast_law_w_q_gh_plus_gk"] for m in MODELS]),
        "variance_null": np.array([model_details[m]["variance_null_contrast"] for m in MODELS]),
        "variance_law": np.array([model_details[m]["variance_law_contrast"] for m in MODELS]),
        "sd_null": sd_null,
        "sd_tgl": sd_tgl,
        "D": D,
        "conditional_design_power": power,
        "logK": np.asarray(logK),
        "H0": np.asarray(public["H0"]),
        "model_names": np.asarray(MODELS),
        "row_names": np.asarray(public["row_names"])[keep],
        "param_names": np.asarray(public["param_names"])[colmask],
        "design_rank": np.array([res[m]["design_rank"] for m in MODELS], dtype=np.int64),
        "condition_design_whitened": np.array([res[m]["condition_design_whitened"] for m in MODELS]),
        "response_cepheid": np.array([res[m]["response_cepheid"] for m in MODELS]),
        "influence_identity_error": np.array([res[m]["influence_identity_error"] for m in MODELS]),
        "covariance_full_255": C_full,
        "covariance_local": C_local,
        "covariance_background": cb,
        "cross_covariance": q,
        "covariance_used": joint if coupled else C_local,
        "covariance_rank": np.asarray(meta["cov_rank"], dtype=np.int64),
        "covariance_nullity": np.asarray(meta["cov_nullity"], dtype=np.int64),
        "covariance_eig_min": np.asarray(meta["eig_min"]),
        "covariance_eig_min_positive": np.asarray(meta["eig_min_positive"]),
        "covariance_eig_max": np.asarray(meta["eig_max"]),
        "covariance_tolerance": np.asarray(meta["tolerance"]),
        "support_design_error": np.asarray(meta["support_design_error"]),
    }
    details = {
        "n_rows": n,
        "n_columns": int(colmask.sum()),
        "keep_first_last": [int(keep[0]), int(keep[-1])],
        "h_index": h,
        "covariance_geometry": meta,
        "models": model_details,
        "covariance_arrays": {
            "covariance_full_255": list(C_full.shape),
            "covariance_local": list(C_local.shape),
            "covariance_background": list(cb.shape),
            "cross_covariance": list(q.shape),
            "covariance_used": list((joint if coupled else C_local).shape),
        },
    }
    return arrays, details


def save_npz(path: Path, arrays: dict) -> None:
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("wb") as handle:
        np.savez_compressed(handle, **arrays)
    tmp.replace(path)


def write_json(path: Path, payload: dict) -> None:
    raw = (json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    json.loads(raw.decode("utf-8"))
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(raw)
    tmp.replace(path)


def main() -> None:
    source_paths = [ORDER05, CORE, STUDY, VALIDATION, NETWORK, ROWS, BG1, G42_JSON, G42_NPZ,
                    S0_NPZ, S0_MANIFEST, PACKAGE_PINS, V411_GEOMETRY]
    sources = {str(p.resolve()): pin(p) for p in source_paths}
    study = json.loads(STUDY.read_text(encoding="utf-8"))
    validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
    g42_receipt = json.loads(G42_JSON.read_text(encoding="utf-8"))
    package_receipt = json.loads(PACKAGE_PINS.read_text(encoding="utf-8"))
    if validation["status"] != "VALIDACAO_CORE_R3B_PASS" or not all(validation["checks"].values()):
        raise RuntimeError("R3B_validation_not_passed")
    if study["status"] != STATUS or study["opening_allowed"]:
        raise RuntimeError("unexpected_R3B_study_status")
    if pin(STUDY)["sha256"] != validation["artifact_hashes"]["ESTUDO_CONDICIONAL_R3B.json"]["sha256"]:
        raise RuntimeError("study_hash_mismatch")
    if pin(CORE)["sha256"] != validation["artifact_hashes"]["core_r3b.py"]["sha256"]:
        raise RuntimeError("core_hash_mismatch")
    if pin(G42_NPZ)["sha256"] != g42_receipt["outputs"]["npz_sha256"]:
        raise RuntimeError("G42_hash_mismatch")
    r3b_hashes = {str(Path(row["path"]).resolve()): row["sha256"] for row in study["source_manifest"]["sources"]}
    for path in (NETWORK, ROWS, BG1, G42_NPZ):
        if pin(path)["sha256"] != r3b_hashes[str(path.resolve())]:
            raise RuntimeError("public_source_hash_mismatch:" + str(path))
    package_checks = {}
    for rel, expected in package_receipt["arquivos"].items():
        actual = pin(EMENDA / rel)
        package_checks[rel] = actual["sha256"] == expected["sha256"] and actual["bytes"] == expected["bytes"]
    if not all(package_checks.values()):
        raise RuntimeError("emenda_package_pin_mismatch")

    with np.load(NETWORK, allow_pickle=False) as net:
        A = net["A"].copy()
        C = net["C"].copy()
        c = net["c_cepheid"].copy()
        h = int(net["h_index"])
        row_names = np.array([str(x) for x in net["row_names"]])
        param_names = np.array([str(x) for x in net["param_names"]])
    if A.shape != (255, 64) or C.shape != (255, 255) or c.shape != (255,):
        raise ValueError("unexpected_network_shape")
    rows = json.loads(ROWS.read_text(encoding="utf-8"))
    if len(rows) != 255 or not all(rows[i]["kind"] == "sn1a_calibrator" for i in range(179, 234)):
        raise ValueError("unexpected_SN_calibrator_row_map")
    if rows[248]["kind"] != "sn1a_hubble_flow":
        raise ValueError("unexpected_HF_intercept_row_map")
    sn_rows = [i for i, name in enumerate(row_names) if name.startswith("SNe Ia equation")]
    extra13 = np.array(sn_rows[42:], dtype=np.int64)
    if not np.array_equal(extra13, np.arange(221, 234)):
        raise ValueError("unexpected_EXTRA13_indices")
    g42_rows = np.arange(179, 221)
    keep_out = np.array([i for i in range(255) if i not in set(extra13)], dtype=np.int64)
    keep_all = np.arange(255, dtype=np.int64)

    bg = json.loads(BG1.read_text(encoding="utf-8"))
    cb = np.asarray(bg["covariance"], dtype=float)
    gh = np.asarray(bg["gradient_h"], dtype=float)
    gk = np.asarray(bg["gradient_k"], dtype=float)
    if cb.shape != (3, 3) or float(linalg.eigvalsh(cb)[0]) <= 0.0:
        raise ValueError("BG_covariance_not_positive_definite")
    public = {
        "A": A, "c": c, "h": h, "row_names": row_names, "param_names": param_names,
        "cb": cb, "gh": gh, "gk": gk,
        "vb": float(gh @ cb @ gh),
        "vbt": float((gh + gk) @ cb @ (gh + gk)),
        "logK": float(bg["logK"]), "H0": float(bg["H0"]),
    }
    if abs(public["vb"] - float(bg["variance_h"])) > 1e-18:
        raise ValueError("BG_null_variance_mismatch")
    if abs(public["vbt"] - float(bg["variance_h_plus_k"])) > 1e-18:
        raise ValueError("BG_law_variance_mismatch")

    with np.load(G42_NPZ, allow_pickle=False) as g42:
        cov42_stat = g42["cov42_stat"].copy()
        cross42_stat = g42["cross_alpha42_stat"].copy()
    if cov42_stat.shape != (42, 42) or cross42_stat.shape != (42,):
        raise ValueError("unexpected_G42_shape")
    C1_full = C.copy()
    C1_full[np.ix_(g42_rows, g42_rows)] = cov42_stat
    C1_full[g42_rows, 248] = cross42_stat
    C1_full[248, g42_rows] = cross42_stat
    C2_full = C1_full.copy()
    old13 = C2_full[np.ix_(extra13, extra13)]
    C2_full[np.ix_(extra13, extra13)] = 13.0 * np.diag(np.diag(old13))

    with np.load(S0_NPZ, allow_pickle=False) as s0:
        if not np.array_equal(s0["keep"], keep_out):
            raise ValueError("S0_keep_does_not_match_S1_S4")
        if list(s0["model_names"]) != list(MODELS):
            raise ValueError("model_order_mismatch")
        if float(s0["logK"]) != public["logK"] or float(s0["H0"]) != public["H0"]:
            raise ValueError("BG_center_or_logK_mismatch")
        if not np.array_equal(s0["gradient_h"], gh) or not np.array_equal(s0["gradient_k"], gk):
            raise ValueError("BG_gradient_mismatch")

    built = {
        "S1": build_scenario("S1", keep_out, C1_full, public, coupled=False),
        "S2": build_scenario("S2", keep_all, C2_full, public, coupled=False),
        "S4": build_scenario("S4", keep_out, C1_full, public, coupled=True),
    }
    max_weight_delta = float(np.max(np.abs(built["S4"][0]["weights"] - built["S1"][0]["weights"])))
    if max_weight_delta != 0.0:
        raise ValueError("S4_weights_changed_at_optimum")

    comparisons = {}
    for label, (_, details) in built.items():
        comparisons[label] = {}
        for model in MODELS:
            got = details["models"][model]
            expected = study["cells"][label][model]
            d_error = abs(got["D"] - expected["D"])
            p_error = abs(got["conditional_design_power_Phi_D_minus_5"] - expected["conditional_design_power_Phi_D_minus_5"])
            q_expected = study["scenario_diagnostics"][label]["models"][model].get("q_sha256_contiguous_float64") if label == "S4" else None
            q_match = None if q_expected is None else got["q_sha256_contiguous_float64"] == q_expected
            comparisons[label][model] = {
                "D_recalculated": got["D"],
                "D_03C": expected["D"],
                "D_absolute_error": d_error,
                "power_recalculated": got["conditional_design_power_Phi_D_minus_5"],
                "power_03C": expected["conditional_design_power_Phi_D_minus_5"],
                "power_absolute_error": p_error,
                "within_D_tolerance_1e-12": bool(d_error <= D_TOL),
                "within_power_tolerance_1e-12": bool(p_error <= POWER_TOL),
                "q_sha256_matches_03C": q_match,
            }
            if d_error > D_TOL or p_error > POWER_TOL or q_match is False:
                raise RuntimeError("03C_comparison_failed:" + label + ":" + model)

    filenames = {"S1": "estimador_s1_v411.npz", "S2": "estimador_s2_v411.npz", "S4": "estimador_s4_v411.npz"}
    for label, (arrays, _) in built.items():
        save_npz(OUT / filenames[label], arrays)

    # Reabre somente os NPZ de desenho recem-gravados e valida o contrato externo.
    for label, filename in filenames.items():
        with np.load(OUT / filename, allow_pickle=False) as saved:
            expected_n = len(built[label][0]["keep"])
            if saved["weights"].shape != (2, expected_n):
                raise ValueError("saved_weight_shape_mismatch")
            if saved["sd_null"].shape != (2,) or saved["sd_tgl"].shape != (2,) or saved["D"].shape != (2,):
                raise ValueError("saved_scale_shape_mismatch")
            if int(saved["keep"][0]) < 0 or int(saved["keep"][-1]) > 254:
                raise ValueError("saved_network_indices_out_of_range")
            for key in ("weights", "null_basis", "sd_null", "sd_tgl", "D", "covariance_used"):
                if not np.isfinite(saved[key]).all():
                    raise ValueError("nonfinite_saved_array:" + key)
            if np.any(saved["sd_null"] <= 0.0) or np.any(saved["sd_tgl"] <= 0.0):
                raise ValueError("nonpositive_saved_scale")

    outputs = {name: pin(OUT / name) for name in filenames.values()}
    manifest = {
        "schema": "H0DN_ORDEM05_ESTIMADORES_S1_S2_S4_V1",
        "status": "ESTIMADORES_PINADOS__SOMENTE_DESENHO",
        "study_status": STATUS,
        "opening_allowed": False,
        "certificate_status": "REFUSED_NO_ADMITTED_REVIEWED_PHYSICAL_COVARIANCE",
        "script": pin(Path(__file__).resolve()),
        "inputs": sources,
        "emenda_package_all_19_pins_match": all(package_checks.values()),
        "conventions": {
            "keep": "indices int64 das linhas na rede original de 255; os pesos seguem essa ordem",
            "weights": "matriz 2 x n; ordem dos modelos em model_names",
            "sd_null": "sqrt(V_L + V_B - 2 w^T q g_h)",
            "sd_tgl": "sqrt(V_L + V_BT - 2 w^T q (g_h + g_k))",
            "D": "abs(logK) / sd_null; somente desenho, sem estimativa observada",
            "conditional_design_power": "Phi(D - 5), a mesma potencia condicional de 03-C",
            "covariance_full_255": "matriz local de 255 linhas apos a substituicao do cenario",
            "covariance_local": "submatriz nas linhas keep efetivamente usada pela geometria",
            "cross_covariance": "q com forma 2 x n x 3; zero em S1/S2 e otimo por modelo em S4",
            "covariance_used_S1_S2": "covariancia local n x n",
            "covariance_used_S4": "covariancia conjunta por modelo, forma 2 x (n+3) x (n+3), blocos [C_L,q;q^T,C_BG]",
            "S4_sd_tgl_provenance": "recalculado de desenho com o mesmo q que minimiza D do nulo; 03-C tinha sd_tgl=null e nao fornece valor de conferencia",
        },
        "scenario_definitions": {
            "S1": "EXTRA13_OUT + G42 STATONLY por substituicao, nunca adicao; cross local-BG1 zero",
            "S2": "S1 com EXTRA13_IN_CAP13: C_13 substituido por 13*diag(C_13), demais entradas preservadas",
            "S4": "S1 com q=C_L w b^T/V_L e b=-sqrt(V_L/V_B) C_BG g_h; minimo global de D sob q C_BG^-1 q^T <= C_L",
        },
        "outputs": outputs,
        "scenarios": {label: details for label, (_, details) in built.items()},
        "checks_against_03C": comparisons,
        "S4_weights_recomputed_max_abs_difference_vs_S1": max_weight_delta,
        "S4_q_hashes_match_03C": all(comparisons["S4"][m]["q_sha256_matches_03C"] for m in MODELS),
        "non_numbers_not_fabricated": {
            label: {
                model: {
                    "D": None,
                    "conditional_design_power": None,
                    "status": study["cells"][label][model]["conditional_status"],
                    "reason": study["cells"][label][model]["reason"],
                } for model in MODELS
            } for label in ("S3", "S5")
        },
        "limitations": [
            "S1 e uma sensibilidade G42 STATONLY agregada; a admissao fisica da covariancia nao esta estabelecida.",
            "S2 e um teto hipotetico interno do bloco EXTRA13, nao uma dominacao de Loewner da matriz fisica completa.",
            "S4 e um envelope adversarial no elipsoide; a contencao da covariancia fisica nesse elipsoide nao esta provada.",
            "sd_tgl de S4 e derivacao de desenho nova exigida pelo esquema do rito; nao existia em 03-C.",
            "Os tres artefatos servem as linhas de estresse; nao alteram o primario, nao certificam poder e nao autorizam abertura.",
            "S3 e S5 permanecem INVALID_SCENARIO_NOT_A_NUMBER; nenhum NPZ foi criado para eles.",
        ],
        "execution_guards": {
            "observed_data_used": False,
            "observed_vector_opened": False,
            "observed_D_H0_ratio_or_Z_computed": False,
            "evaluator_or_opening_called": False,
            "observed_solver_called": False,
            "RNG_or_Monte_Carlo_used": False,
            "seeds_used": False,
            "FREEZE_R2_modified": False,
            "preexisting_v410_files_modified": False,
            "emenda_package_modified": False,
            "writes_limited_to": str(OUT),
        },
        "software": {
            "python": sys.version,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
    }
    manifest_path = OUT / "MANIFESTO_ESTIMADORES_S1_S2_S4.json"
    write_json(manifest_path, manifest)
    sum_files = [Path(__file__).resolve()] + [OUT / name for name in filenames.values()] + [manifest_path]
    sums = "".join(pin(path)["sha256"] + "  " + path.name + "\n" for path in sum_files)
    (OUT / "SHA256SUMS.txt").write_text(sums, encoding="utf-8", newline="\n")

    # Confere que nenhum arquivo do pacote da emenda mudou durante a execucao.
    for rel, expected in package_receipt["arquivos"].items():
        actual = pin(EMENDA / rel)
        if actual["sha256"] != expected["sha256"] or actual["bytes"] != expected["bytes"]:
            raise RuntimeError("emenda_package_changed_during_execution")
    print(json.dumps({
        "status": manifest["status"],
        "D": {label: {m: built[label][1]["models"][m]["D"] for m in MODELS} for label in built},
        "sd_tgl": {label: {m: built[label][1]["models"][m]["sd_tgl"] for m in MODELS} for label in built},
        "max_03C_D_error": max(row["D_absolute_error"] for c in comparisons.values() for row in c.values()),
        "max_03C_power_error": max(row["power_absolute_error"] for c in comparisons.values() for row in c.values()),
        "outputs": {p.name: pin(p) for p in sum_files + [OUT / "SHA256SUMS.txt"]},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
