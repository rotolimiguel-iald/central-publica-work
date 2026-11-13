"""Blind synthetic R22 table -> MAS/HMS -> equations -> 72 identities.

No observed data, estimator, solver, RNG, Monte Carlo, projection, jitter,
D/Z/t/h/ratio, FREEZE_R2 or v410 artifacts are used. All centers are fictional.
"""
from __future__ import annotations

import ast
import configparser
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import types

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WORK09 = ROOT.parents[1]
UPSTREAM_BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
PKG = UPSTREAM_BASE / "network" / "upstream" / "h0_constrainer" / "h0_constrainer"
ORDER = WORK09 / "ORDEM_KIMI_H0DN_03C_11nov.md"
OUTPUT = ROOT / "MONTAGEM_FIXTURES_SINTETICOS.json"
TOL = 1.0e-12
HOSTS = [
    "N7250", "N4536", "N3972", "N4424", "N4639", "N4038", "M101",
    "N2442", "N1365", "N5643", "N5584", "N1559", "N5468", "N1448",
    "N2525", "N3370", "N5861", "N3147", "N3021", "N1309", "N3982",
    "N1015", "N3447", "N5917", "U9391", "N3583", "N2608", "N7541",
    "N0691", "N3254", "N5728", "N7678", "M1337", "N4680", "N7329",
    "N0976", "N0105",
]
ANCHORS = ["N4258", "LMC", "MW"]
OFFSETS = {"N4258": 0.31, "LMC": -0.17, "MW": 0.23}
REF_ERRORS = {"N4258": 0.011, "LMC": 0.012, "MW": 0.013}
GEOMETRIC_ERRORS = {"N4258": 0.021, "LMC": 0.022, "MW": 0.023}
THETA_HOST = {host: 10.0 + 0.01 * k for k, host in enumerate(HOSTS)}
THETA_MB = -2.25
THETA_LOGH = 0.50


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def make_fixture() -> dict:
    reference_rows = []
    for anchor in ANCHORS:
        reference_rows.append({
            "host": anchor,
            "mu_host": OFFSETS[anchor],
            "mu_error": REF_ERRORS[anchor],
            "method": "ceph_hst",
            "anchor": anchor,
            "source": "R22",
            "PGC": 800000 + ANCHORS.index(anchor),
            "role": "synthetic_mas_reference",
        })
    host_rows = []
    for anchor in ANCHORS:
        for k, host in enumerate(HOSTS):
            host_rows.append({
                "host": host,
                "mu_host": THETA_HOST[host] + OFFSETS[anchor],
                "mu_error": 0.04 + 0.0005 * k,
                "method": "ceph_hst",
                "anchor": anchor,
                "source": "R22",
                "PGC": 900000 + k,
                "role": "synthetic_host_measurement",
                "theta_host_fictional": THETA_HOST[host],
                "mas_offset_fictional": OFFSETS[anchor],
            })
    sn_rows = []
    for k, host in enumerate(HOSTS):
        sn_rows.append({
            "host": host,
            "SN": f"SYN{k:02d}",
            "m0_Bi": THETA_HOST[host] + THETA_MB,
            "sigma": 0.03 + 0.0001 * k,
        })
    anchor_rows = [
        {"anchor": anchor, "mu_value": -7.0 - i, "mu_sigma": GEOMETRIC_ERRORS[anchor]}
        for i, anchor in enumerate(ANCHORS)
    ]
    alpha = THETA_LOGH - 0.2 * THETA_MB - 5.0
    return {
        "schema": "h0dn.r22.synthetic-table-fixture.v1",
        "synthetic_only": True,
        "observed_centers_used": False,
        "hosts_reference_order": HOSTS,
        "reference_host": "N7250",
        "anchors": ANCHORS,
        "generative_convention": {
            "equation": "y_raw = A @ theta + O_MAS",
            "corrected_equation": "y_raw - O_MAS = A @ theta",
            "host_raw": "mu_host[k,a] = theta_host[k] + mas_offset[a]",
            "sn_calibrator": "m0_Bi[k] = theta_host[k] + theta_MB",
            "hubble_intercept": "alpha_sn1a + 5 = theta_logH - 0.2 * theta_MB",
            "triplets_are_not_required_equal": True,
            "second_difference_pairs": ["N4258-LMC", "N4258-MW"],
        },
        "theta_truth_fictional": {
            "host": THETA_HOST,
            "SNe Ia M_B": THETA_MB,
            "log_10(H0)": THETA_LOGH,
        },
        "mas_offsets_fictional": OFFSETS,
        "mas_reference_errors_fictional": REF_ERRORS,
        "geometric_anchor_errors_fictional": GEOMETRIC_ERRORS,
        "anchor_reference_rows": reference_rows,
        "host_measurement_rows": host_rows,
        "sn1a_calibrator_rows": sn_rows,
        "anchor_rows": anchor_rows,
        "config_fictional": {
            "host_data": "host_data.dat",
            "sn1a_calib": "sn1a_calib.dat",
            "anchors": "anchors.dat",
            "alpha_sn1a": alpha,
            "alpha_sn1a_error": 0.02,
            "unused_hosts_via_covariance": False,
            "verbose": False,
            "warn": False,
            "logfile": "none",
            "savefile": "none",
        },
        "identity_count": 72,
        "absolute_tolerance_mag": TOL,
        "rng_or_seed_used": False,
    }


def load_module(name: str):
    code = (PKG / f"{name}.py").read_text(encoding="utf-8")
    tree = ast.parse(code)
    mod = types.ModuleType("h0_constrainer." + name)
    mod.__package__ = "h0_constrainer"
    mod.__file__ = str(PKG / f"{name}.py")
    sys.modules[mod.__name__] = mod
    setattr(sys.modules["h0_constrainer"], name, mod)
    exec(compile(tree, mod.__file__, "exec"), mod.__dict__)
    return mod


def assembly_namespace():
    package = types.ModuleType("h0_constrainer")
    package.__path__ = [str(PKG)]
    sys.modules["h0_constrainer"] = package
    config_reader = load_module("config_reader")
    data_loader = load_module("data_loader")
    intercept = load_module("intercept")
    equations = load_module("equations")
    assert intercept is not None
    tree = ast.parse((PKG / "main.py").read_text(encoding="utf-8"))
    function = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "main"
    )
    end = next(
        i for i, node in enumerate(function.body)
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "eq_data" for target in node.targets)
    )
    function.body = function.body[: end + 1] + [
        ast.Return(ast.Call(func=ast.Name(id="locals", ctx=ast.Load()), args=[], keywords=[]))
    ]
    module = ast.Module(body=[function], type_ignores=[])
    ast.fix_missing_locations(module)
    forbidden = {"solver", "logger", "evaluate"}
    assert not any(isinstance(node, ast.Name) and node.id in forbidden for node in ast.walk(module))
    namespace = {
        "os": os,
        "sys": sys,
        "np": np,
        "pd": pd,
        "config_reader": config_reader,
        "data_loader": data_loader,
        "equations": equations,
    }
    exec(compile(module, "main_synthetic_assembly_only.py", "exec"), namespace)
    return namespace


def write_inputs(directory: Path, fixture: dict) -> Path:
    columns = ["host", "mu_host", "mu_error", "method", "anchor", "source", "PGC"]
    host_rows = fixture["anchor_reference_rows"] + fixture["host_measurement_rows"]
    pd.DataFrame(host_rows)[columns].to_csv(
        directory / "host_data.dat", sep=" ", index=False, float_format="%.17g"
    )
    pd.DataFrame(fixture["sn1a_calibrator_rows"]).to_csv(
        directory / "sn1a_calib.dat", sep=" ", index=False, float_format="%.17g"
    )
    pd.DataFrame(fixture["anchor_rows"]).to_csv(
        directory / "anchors.dat", sep=" ", index=False, float_format="%.17g"
    )
    values = dict(fixture["config_fictional"])
    values["datadir"] = str(directory.resolve()) + os.sep
    config = configparser.ConfigParser()
    config["DEFAULT"] = {key: str(value) for key, value in values.items()}
    config_path = directory / "synthetic.ini"
    with config_path.open("w", encoding="utf-8") as handle:
        config.write(handle)
    return config_path


def identity_matrix(eq: dict, host_df: pd.DataFrame) -> tuple[np.ndarray, list[dict]]:
    lookup = {}
    for i, row in host_df.iterrows():
        key = (str(row["host"]), str(row["anchor"]))
        assert key not in lookup
        lookup[key] = int(i)
    rows = []
    metadata = []
    identity_id = 0
    for k in range(1, len(HOSTS)):
        for other, pair in [("LMC", "N4258-LMC"), ("MW", "N4258-MW")]:
            identity_id += 1
            i_kn = lookup[(HOSTS[k], "N4258")]
            i_ko = lookup[(HOSTS[k], other)]
            i_0n = lookup[(HOSTS[0], "N4258")]
            i_0o = lookup[(HOSTS[0], other)]
            row = np.zeros(eq["coeffs"].shape[0], dtype=float)
            row[i_kn] = 1.0
            row[i_ko] = -1.0
            row[i_0n] = -1.0
            row[i_0o] = 1.0
            rows.append(row)
            metadata.append({
                "identity_id": identity_id,
                "k": k,
                "host": HOSTS[k],
                "reference_host": HOSTS[0],
                "pair": pair,
                "row_indices_zero_based": [i_kn, i_ko, i_0n, i_0o],
                "coefficients": [1, -1, -1, 1],
                "expression": f"(y_{HOSTS[k]},N4258-y_{HOSTS[k]},{other})-(y_N7250,N4258-y_N7250,{other})=0",
            })
    return np.asarray(rows), metadata


def main() -> None:
    fixture = make_fixture()
    namespace = assembly_namespace()
    with tempfile.TemporaryDirectory(prefix="_synthetic_r22_", dir=HERE) as temp:
        config_path = write_inputs(Path(temp), fixture)
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            state = namespace["main"](str(config_path))
        assert captured.getvalue() == "", captured.getvalue()

    eq = state["eq_data"]
    host_df = state["host_df"]
    A = np.asarray(eq["coeffs"], dtype=float)
    C = np.asarray(eq["covar"], dtype=float)
    y = np.asarray(eq["yval"], dtype=float)
    assert A.shape == (149, 39)
    assert C.shape == (149, 149)
    assert y.shape == (149,)
    assert len(host_df) == 111
    assert len(state["sn1a_calib_df"]) == 37

    offset_by_mas = {}
    for method, anchor, source, value in zip(
        state["mas_ref_method"], state["mas_ref_anchor"],
        state["mas_ref_source"], state["mas_ref_value"],
    ):
        key = f"{method}&{anchor}&{source}"
        offset_by_mas[key] = float(value)
    expected_offset_by_mas = {f"ceph_hst&{a}&R22": OFFSETS[a] for a in ANCHORS}
    assert set(offset_by_mas) == set(expected_offset_by_mas)
    mas_recovery_error = max(
        abs(offset_by_mas[key] - expected_offset_by_mas[key]) for key in offset_by_mas
    )

    theta_by_name = dict(THETA_HOST)
    theta_by_name["SNe Ia M_B"] = THETA_MB
    theta_by_name["log_10(H0)"] = THETA_LOGH
    parameter_names = [str(p["objname"]) for p in eq["parinfo"]]
    theta = np.asarray([theta_by_name[name] for name in parameter_names], dtype=float)
    O = np.zeros(y.shape[0], dtype=float)
    for i, row in host_df.iterrows():
        O[int(i)] = offset_by_mas[str(row["mas_name"])]
    y_theta = A @ theta
    y_raw_expected = y_theta + O
    corrected = y - O

    B, identity_metadata = identity_matrix(eq, host_df)
    residuals = B @ y
    residuals_theta = B @ y_theta
    identity_results = []
    for meta, residual, residual_theta in zip(identity_metadata, residuals, residuals_theta):
        identity_results.append({
            **meta,
            "residual_raw_mag": float(residual),
            "residual_A_theta_mag": float(residual_theta),
            "tolerance_mag": TOL,
            "pass": bool(abs(residual) <= TOL and abs(residual_theta) <= TOL),
        })

    host_C = C[:111, :111]
    host_rank = int(np.linalg.matrix_rank(host_C, tol=1.0e-10))
    constraint_rank = int(np.linalg.matrix_rank(B, tol=1.0e-12))
    max_raw_model_error = float(np.max(np.abs(y - y_raw_expected)))
    max_corrected_model_error = float(np.max(np.abs(corrected - y_theta)))
    max_identity = float(np.max(np.abs(residuals)))
    max_identity_theta = float(np.max(np.abs(residuals_theta)))
    max_BA = float(np.max(np.abs(B @ A)))
    max_BCB = float(np.max(np.abs(B @ C @ B.T)))
    min_nl_separation = min(
        abs(float(host_df.iloc[i]["mu_host"]) - float(host_df.iloc[i + 37]["mu_host"]))
        for i in range(37)
    )
    min_nm_separation = min(
        abs(float(host_df.iloc[i]["mu_host"]) - float(host_df.iloc[i + 37]["mu_host"]))
        for i in range(37, 74)
    )
    checks = {
        "shape_and_row_map_pass": True,
        "mas_reference_recovery_pass": bool(mas_recovery_error <= TOL),
        "raw_generative_identity_pass": bool(max_raw_model_error <= TOL),
        "offset_corrected_A_theta_pass": bool(max_corrected_model_error <= TOL),
        "all_72_raw_identities_pass": bool(max_identity <= TOL),
        "all_72_A_theta_identities_pass": bool(max_identity_theta <= TOL),
        "constraint_rank_72_pass": constraint_rank == 72,
        "host_covariance_rank_39_pass": host_rank == 39,
        "host_covariance_nullity_72_pass": 111 - host_rank == 72,
        "BA_zero_pass": bool(max_BA <= TOL),
        "BCB_zero_pass": bool(max_BCB <= TOL),
        "triplets_nontrivially_distinct_pass": bool(min(min_nl_separation, min_nm_separation) > 0.1),
    }
    completed = all(checks.values())
    code_paths = [PKG / f"{name}.py" for name in ["main", "config_reader", "data_loader", "intercept", "equations"]]
    result = {
        "status": "FULL_ASSEMBLY_ROUTINE_COMPLETED" if completed else "FULL_ROUTINE_NOT_COMPLETED",
        "FULL_ROUTINE_NOT_COMPLETED": not completed,
        "routine_scope": {
            "definition": "Complete synthetic R22 assembly required by B5: raw tables -> parsing/filtering -> MAS/HMS extraction -> A,C,y -> known-offset map -> 72 raw and A*theta identities.",
            "solver_required": False,
            "solver_called": False,
            "estimator_evaluate_called": False,
            "full_255_row_observed_network_rebuilt": False,
            "note": "The synthetic fixture has 149 equations (111 host + 37 calibrator + 1 intercept) and 39 parameters. It validates the complete R22 subsystem that generates the 72 constraints, not unrelated H0DN methods or the observed 255-row vector."
        },
        "label": "ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO",
        "declaration": "[DECLARADO pelo Kimi]",
        "order": {
            "path": str(ORDER),
            "sha256": sha256_path(ORDER),
        },
        "flags": {
            "observed_vector_read": False,
            "observed_support_tests": 0,
            "observed_values_used": False,
            "observed_centers_used_in_fixtures": False,
            "estimator_evaluate_called": False,
            "solver_on_observed_called": False,
            "solver_called": False,
            "Z_t_h_or_ratio_computed": False,
            "D_or_power_computed": False,
            "new_seed_generated": False,
            "monte_carlo_run": False,
            "rng_used": False,
            "projection_or_jitter_used": False,
            "freeze_R2_or_v410_modified": False,
            "observed_conference_executed": False,
        },
        "observed_vector_read": False,
        "observed_support_tests": 0,
        "hashes": {
            "algorithm": "sha256",
            "order_sha256": sha256_path(ORDER),
            "script_sha256": sha256_path(Path(__file__).resolve()),
            "fixture_specification_canonical_json_sha256": canonical_sha256(fixture),
            "upstream_code": [
                {"path": str(path), "sha256": sha256_path(path)} for path in code_paths
            ],
        },
        "fixture": fixture,
        "execution": {
            "equation_shape": list(A.shape),
            "covariance_shape": list(C.shape),
            "host_rows": len(host_df),
            "calibrator_rows": len(state["sn1a_calib_df"]),
            "host_covariance_rank": host_rank,
            "host_covariance_nullity": 111 - host_rank,
            "constraint_rank": constraint_rank,
            "mas_reference_recovery_max_abs_mag": mas_recovery_error,
            "raw_minus_A_theta_minus_O_max_abs_mag": max_raw_model_error,
            "corrected_minus_A_theta_max_abs_mag": max_corrected_model_error,
            "raw_72_residual_max_abs_mag": max_identity,
            "A_theta_72_residual_max_abs_mag": max_identity_theta,
            "BA_max_abs": max_BA,
            "BCBT_max_abs": max_BCB,
            "minimum_abs_N4258_minus_LMC_triplet_separation_mag": min_nl_separation,
            "minimum_abs_N4258_minus_MW_triplet_separation_mag": min_nm_separation,
            "absolute_tolerance_mag": TOL,
            "checks": checks,
        },
        "identity_results": identity_results,
        "limitations": [
            "Validation is limited to the synthetic R22 subsystem and does not rebuild or inspect the observed 255-row vector.",
            "Passing the fixtures proves the tested synthetic assembly path only; it does not prove observed centers, physical covariance, power, or admission of a variant.",
            "No solver or estimator is part of B5 assembly validation; neither was called."
        ],
    }
    if not completed:
        result["failure"] = "SYNTHETIC_ASSEMBLY_CHECK_FAILED"
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "checks": checks,
        "raw_72_residual_max_abs_mag": max_identity,
        "A_theta_72_residual_max_abs_mag": max_identity_theta,
        "output": str(OUTPUT),
        "observed_vector_read": False,
        "observed_support_tests": 0,
    }, ensure_ascii=False, indent=2))
    if not completed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
