"""Real CAMB supplier integration; synthetic qualification, never an opening API.

Reuses the immutable ORDEM018 prediction_worker. The Gaussian consumer below
accepts only synthetic vectors. H5 means BAO-only free rd, not a generic early
universe change. This module grants no admission and emits no scientific token.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import math

HERE = Path(__file__).resolve().parent
MODELS = ("H1_TGL", "H2_LCDM", "H5_rd_free")


class BackgroundError(ValueError):
    pass


def require(ok, reason):
    if not ok:
        raise BackgroundError(reason)


def finite(value, name, positive=False):
    require(type(value) in (float, int), "NON_NUMERIC:" + name)
    value = float(value)
    require(math.isfinite(value) and (not positive or value > 0), "NONFINITE_OR_DOMAIN:" + name)
    return value


def read_pinned(path, digest):
    raw = Path(path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == digest, "PIN_MISMATCH:" + str(path))
    return raw


def load_supplier(manifest_sha256):
    manifest = json.loads(read_pinned(HERE / "SUPPLIER_COPY_MANIFEST.json", manifest_sha256))
    for item in manifest["pins"]:
        raw = read_pinned(HERE / item["copy"], item["sha256"])
        require(len(raw) == item["bytes"], "COPY_LENGTH")
    path = HERE / "supplier_copy" / "background_controls.py"
    spec = importlib.util.spec_from_file_location("f3_pinned_background_engine", path)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)  # top-level is stdlib only; no main or old claim
    engine.runtime_check()  # package versions and every pinned CAMB binary/data file
    return engine


def predict(engine, configuration, point_id):
    """Exactly the old physical worker, with a new explicit theory configuration."""
    require(configuration["scope"] == "PREDICTIONS_ONLY_NO_OBSERVED_CENTERS_NO_LIKELIHOOD_NO_EVIDENCE_NO_NETWORK", "SCOPE")
    require(point_id in {p["id"] for p in configuration["points"]}, "POINT_NOT_PREREGISTERED")
    return engine.prediction_worker(configuration, point_id, "reference")


def physical_mean(background, rows, model, alpha_fine, rd_Mpc=None):
    """Same background formulas as five_model_assembly.py:253-264, explicit rows.

    A local row is H0*K rather than the joint assembly's log10(H0*K) magnitudes;
    this distinction is encoded in its observable name. No observed row is read.
    """
    require(model in MODELS, "UNKNOWN_MODEL")
    require(background.get("physics_status") == "STANDARD_BACKGROUND_THEORY_CONTROL_NOT_OBSERVATION", "BACKGROUND_KIND")
    alpha = finite(alpha_fine, "ALPHA_FINE_CODATA_2018", True)
    require(alpha < 1, "ALPHA_DOMAIN")
    beta = alpha * math.sqrt(math.e)
    H0 = finite(background["theta"][0], "H0", True)
    E = finite(background["E_law"], "E", True)
    K = math.exp((2 * beta / 3) * math.log(E))
    require(math.isclose(background["I_law"], (2 / 3) * math.log(E), rel_tol=1e-12, abs_tol=1e-14), "E_I_MISMATCH")
    if model == "H5_rd_free":
        rd = finite(rd_Mpc, "rd", True)
        require(130 <= rd <= 160, "RD_PRIOR")
    else:
        require(rd_Mpc is None, "UNEXPECTED_RD")
        rd = finite(background["rdrag_Mpc"], "rdrag", True)
    low = {float(row["z"]): row for row in background["low_z"]}
    values = []
    for row in rows:
        obs = row["observable"]
        if row["block"] == "CMB":
            require(obs in ("R", "lA", "ombh2"), "CMB_OBSERVABLE")
            values.append(background["theta"][1] if obs == "ombh2" else background[obs])
        elif row["block"] == "BAO":
            require(obs in ("DM_over_rd", "DH_over_rd", "DV_over_rd"), "BAO_OBSERVABLE")
            z = finite(row["z"], "z")
            require(z in low, "REDSHIFT_NOT_COMPUTED")
            values.append(low[z][obs.replace("_over_rd", "_Mpc")] / rd)
        elif row["block"] == "LOCAL":
            require(obs == "H0_local_km_s_Mpc", "LOCAL_OBSERVABLE")
            values.append(H0 * K if model == "H1_TGL" else H0)
        else:
            raise BackgroundError("UNKNOWN_BLOCK")
    require(len({r["id"] for r in rows}) == len(rows), "DUPLICATE_ROW")
    values = [finite(v, "prediction") for v in values]
    return {"mean": values, "beta_runtime": beta, "K_theta": K,
            "theta": background["theta"], "model": model,
            "rd_Mpc": rd, "rd_prior_density_per_Mpc": 1 / 30 if model == "H5_rd_free" else None,
            "scope": "THEORY_PREDICTION_NOT_FROZEN_SCALAR_K", "decision_eligible": False}


def synthetic_log_likelihood(values, mean, covariance, *, dataset_kind):
    """Normalized Gaussian in the declared native rows; no evidence/fit here."""
    import numpy as np
    require(dataset_kind == "SYNTHETIC", "OBSERVED_INPUT_NOT_AUTHORIZED")
    y = np.array([finite(x, "y") for x in values], dtype=float)
    mu = np.array([finite(x, "mu") for x in mean], dtype=float)
    C = np.array([[finite(x, "cov") for x in row] for row in covariance], dtype=float)
    require(y.ndim == 1 and mu.shape == y.shape and C.shape == (len(y), len(y)), "SHAPE")
    require(np.allclose(C, C.T, rtol=0, atol=1e-13), "NONSYMMETRIC_COVARIANCE")
    try:
        L = np.linalg.cholesky(C)
    except np.linalg.LinAlgError as exc:
        raise BackgroundError("COVARIANCE_NOT_SPD") from exc
    r = np.linalg.solve(L, y - mu)
    logdet = float(2 * np.log(np.diag(L)).sum())
    quadratic = float(r @ r)
    return {"lnL": -.5 * (quadratic + logdet + len(y) * math.log(2 * math.pi)),
            "quadratic": quadratic, "logdet": logdet, "normalization": "LEBESGUE_NATIVE_ROW_UNITS",
            "dataset_kind": "SYNTHETIC", "evidence": None, "decision_eligible": False}


def propagate_theta(jacobian, covariance_theta, *, scope):
    """Common J Ctheta J^T; every row uses the SAME theta perturbation.

    No covariance supplied means conditional-only, never an unconditional claim.
    Full nonlinear marginalization uses the existing theta_integrator contract;
    this first-order diagnostic does not replace it or certify its convergence.
    """
    import numpy as np
    require(scope in ("CONDITIONAL_FIXED_THETA", "LINEARIZED_SYNTHETIC_COVARIANCE"), "UNCONDITIONAL_NOT_QUALIFIED")
    J = np.array([[finite(x, "J") for x in row] for row in jacobian], dtype=float)
    require(J.ndim == 2 and J.shape[1] == 3, "J_THETA_ORDER_H0_OMBH2_OMCH2")
    if covariance_theta is None:
        require(scope == "CONDITIONAL_FIXED_THETA", "MISSING_COVARIANCE_THETA")
        return {"scope": scope, "covariance_prediction": None, "unconditional": False}
    require(scope == "LINEARIZED_SYNTHETIC_COVARIANCE", "COVARIANCE_SCOPE")
    C = np.array([[finite(x, "Ctheta") for x in row] for row in covariance_theta], dtype=float)
    require(C.shape == (3, 3) and np.allclose(C, C.T, rtol=0, atol=1e-13), "CTHETA_SHAPE_OR_SYMMETRY")
    require(float(np.linalg.eigvalsh(C).min()) >= 0, "CTHETA_NOT_PSD")
    out = J @ C @ J.T
    return {"scope": scope, "covariance_prediction": out.tolist(), "theta_order": ["H0", "ombh2", "omch2"],
            "unconditional": False, "linearization_error_bound": None, "decision_eligible": False}
