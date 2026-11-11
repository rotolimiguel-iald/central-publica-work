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
import types

import numpy as np
import pandas as pd

BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
PKG = BASE / "network/upstream/h0_constrainer/h0_constrainer"
OUT = Path(r"C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi")
OUT.mkdir(parents=True, exist_ok=True)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def main_truncated():
    tree = ast.parse((PKG / "main.py").read_text(encoding="utf-8"))
    function = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == "main")
    end = next(
        i for i, x in enumerate(function.body)
        if isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "eq_data" for t in x.targets)
    )
    function.body = function.body[: end + 1] + [
        ast.Return(ast.Call(func=ast.Name(id="locals", ctx=ast.Load()), args=[], keywords=[]))
    ]
    ast.fix_missing_locations(tree)
    assert not any(isinstance(n, ast.Name) and n.id in {"solver", "logger"} for n in ast.walk(tree))
    return tree


def json_safe(value):
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating, np.integer, np.bool_)):
        return value.item()
    return value


def published_parameter_vector(param_names: np.ndarray) -> np.ndarray:
    rows = json.loads((OUT / "PARAMETROS_PUBLICADOS_TABELAS.json").read_text(encoding="utf-8"))["A6.T12.2"]

    def host_code(name: str) -> str:
        if name.startswith("NGC "):
            return "N" + name.split()[1].zfill(4)
        if name.startswith("UGC "):
            return "U" + name.split()[1].zfill(4)
        if name == "Mrk 1337":
            return "M1337"
        if name.startswith("M "):
            return "M" + name.split()[1]
        if name.startswith("IC "):
            return "IC" + name.split()[1]
        return name

    published = {}
    for row in rows:
        try:
            published[host_code(row[0])] = float(row[1])
        except (ValueError, TypeError):
            continue
    published.update({
        "Fornax": 31.455,
        "Virgo": 31.060,
        "SNe Ia M_B": -19.252,
        "SBF M_offset": -0.023,
        "log_10(H0)": float(np.log10(73.499)),
    })
    missing = [name for name in param_names if name not in published]
    if missing:
        raise ValueError(("missing_published_parameters", missing))
    return np.array([published[name] for name in param_names])


package = types.ModuleType("h0_constrainer")
package.__path__ = [str(PKG)]
sys.modules["h0_constrainer"] = package
config_reader = load_module("config_reader")
data_loader = load_module("data_loader")
intercept = load_module("intercept")
equations = load_module("equations")
namespace = dict(os=os, sys=sys, np=np, pd=pd, config_reader=config_reader, data_loader=data_loader, equations=equations)
exec(compile(main_truncated(), "main_observed_vector_only.py", "exec"), namespace)

config = configparser.ConfigParser()
config.read(BASE / "network/upstream/h0_constrainer/configs/base_variants_config.ini")
config["DEFAULT"]["datadir"] = str((BASE / "network/upstream/data").resolve()) + os.sep
config["DEFAULT"]["verbose"] = "False"
config["DEFAULT"]["warn"] = "False"
config["DEFAULT"]["logfile"] = "none"
config["DEFAULT"]["savefile"] = "none"
config_path = OUT / "observed_vector_only.ini"
config.write(config_path.open("w", encoding="utf-8"))

captured = io.StringIO()
with contextlib.redirect_stdout(captured):
    state = namespace["main"](str(config_path))
if captured.getvalue():
    raise RuntimeError("Unexpected upstream stdout; no durable result emitted")

eq = state["eq_data"]
y = np.asarray(eq["yval"], dtype=float)
with np.load(BASE / "network/network.npz", allow_pickle=False) as frozen:
    A0 = frozen["A"].copy()
    C0 = frozen["C"].copy()
    row_names0 = frozen["row_names"].copy()
    param_names0 = frozen["param_names"].copy()
    h_index = int(frozen["h_index"])
with np.load(BASE / "estimator_frozen.npz", allow_pickle=False) as estimator:
    null_basis = estimator["null_basis"].copy()

assert y.shape == (255,)
assert np.isfinite(y).all()
assert np.array_equal(eq["coeffs"], A0)
assert np.array_equal(eq["covar"], C0)
assert np.array_equal(np.asarray(eq["eq_descr"], dtype=str), row_names0)
assert np.array_equal(np.asarray([p["objname"] for p in eq["parinfo"]], dtype=str), param_names0)
assert int(eq["ihub"]) == h_index == 63
parameter_values = published_parameter_vector(param_names0)
y_uncentered = y.copy()
y_centered = y_uncentered - A0 @ parameter_values
assert np.array_equal(y_centered, y_uncentered - eq["coeffs"] @ parameter_values)

# This is a support check only, never an evaluation or a fit.
support_max_abs = float(np.max(np.abs(y_centered @ null_basis))) if null_basis.shape[1] else 0.0
support_tolerance = 1e-8 * max(1.0, float(np.max(np.abs(y_centered))))
support_pass = support_max_abs <= support_tolerance
null_residual = (y_centered @ null_basis) @ null_basis.T
support_diagnostics = {
    "max_abs": support_max_abs,
    "tolerance": support_tolerance,
    "pass": support_pass,
    "largest_projected_rows": [
        {"row": int(i), "abs_residual": float(abs(null_residual[i])), "description": str(eq["eq_descr"][i])}
        for i in np.argsort(np.abs(null_residual))[::-1][:20]
    ],
}
print(json.dumps(support_diagnostics, ensure_ascii=False, indent=2))

rows_metadata = json.loads((BASE / "network/rows.json").read_text(encoding="utf-8"))
assert len(rows_metadata) == 255

raw_files = {
    "hosts": BASE / "network/upstream/data/host_data.dat",
    "groups": BASE / "network/upstream/data/groups.dat",
    "sn1a_calib": BASE / "network/upstream/data/sn1a_calib.dat",
    "sn1a_hf": BASE / "network/upstream/data/sn1a_hf_pp.dat",
    "sn1a_cov": BASE / "network/upstream/data/sn1a_covar_pp.dat",
    "sbf_calib": BASE / "network/upstream/data/sbf_calib.dat",
    "sbf_hf": BASE / "network/upstream/data/sbf_hf.dat",
    "megamasers": BASE / "network/upstream/data/megamaser.dat",
    "anchors": BASE / "network/upstream/data/anchors.dat",
}
assert all(path.exists() for path in raw_files.values())

host_df = state["host_df"]
groups_df = state["groups_df"]
sn1a_df = state["sn1a_calib_df"]
sbf_df = state["sbf_calib_df"]
mm_df = state["mm_df"]
starts = {
    "sn1a": int(eq["ieq_sn1a_start"]),
    "sbf": int(eq["ieq_sbf_start"]),
    "mm": int(eq["ieq_mm_start"]),
    "sn1a_hf": int(eq["ieq_h0_m1a"]),
    "sbf_hf": int(eq["ieq_h0_msbf"]),
}

# The aggregation rule established for the R22 set, with identity/provenance separated.
aggregation = {
    "rule": "unweighted arithmetic mean of light curves within each SH0ES calibrator",
    "R22_count": 42,
    "R22_multi_curve": 25,
    "R22_single_curve": 17,
    "max_mean_error_mag": 0.000499725341796875,
    "aliases": {"2008fv": "2008fv_comb", "1994D": "1994DRichmond"},
    "source": "C:/IALD/Central de Patentes/work/kimi_h0dn_discriminante_06nov/g1g2/G1_ARITHMETIC_CANDIDATE.json",
    "identity_provenance": "C:/IALD/Central de Patentes/work/kimi_h0dn_discriminante_06nov/g1g2/G2_IDS_PROVENIENCIA_RESOLVIDA.json",
    "extra_13": "Independent original sources; no covariance borrowed from unrelated Pantheon+ rows",
}

row_records = []
for i, row in enumerate(rows_metadata):
    record = {
        "row": i,
        "description": row["description"],
        "shape": row["shape"],
        "kind": row.get("kind", ""),
        "host": row.get("host", ""),
        "method": row.get("method", ""),
        "anchor": row.get("anchor", ""),
        "source": row.get("source", ""),
        "source_file": row.get("source_file", ""),
        "source_line": row.get("source_line"),
        "y_centered": float(y_centered[i]),
        "y_uncentered": float(y_uncentered[i]),
        "center_offset": float((A0 @ parameter_values)[i]),
        "reconstructed": True,
        "raw": {},
    }
    kind = row.get("kind")
    if kind == "host":
        source = host_df.iloc[i]
        record["raw"] = {
            "mu_host": float(source.mu_host),
            "mu_error": float(source.mu_error),
            "MAS": str(source.mas_name),
            "HMS": str(source.hms_name),
        }
    elif kind == "group":
        source = groups_df.iloc[i - len(host_df)]
        record["raw"] = {
            "group": str(source.group),
            "host": str(source.host),
            "sigma": float(source.sigma),
            "constraint": "mu_host - mu_group = 0",
            "source_file": "data/groups.dat",
            "source_row_zero_based": i - len(host_df),
        }
    elif kind == "sn1a_calibrator":
        j = i - starts["sn1a"]
        source = sn1a_df.iloc[j]
        record["raw"] = {
            "CID": str(source.SN),
            "m0_Bi": float(source.m0_Bi),
            "sigma": float(source.sigma),
            "source_file": "data/sn1a_calib.dat",
            "source_row_zero_based": j,
        }
        record["aggregation"] = aggregation if j < 42 else aggregation["extra_13"]
    elif kind == "sn1a_hubble_flow":
        record["raw"] = {
            "a_sn1a": float(eq["a_sn1a"]),
            "a_sn1a_err": float(eq["a_sn1a_err"]),
            "intercept_equation": "a_sn1a + 5",
            "method": "upstream compute_alpha over 277 Hubble-flow rows and the published covariance; no manual adjustment",
            "source_files": ["data/sn1a_hf_pp.dat", "data/sn1a_covar_pp.dat"],
        }
    elif kind == "sbf_calibrator":
        j = i - starts["sbf"]
        source = sbf_df.iloc[j]
        record["raw"] = {
            "host": str(source.host),
            "M110": float(source.M110),
            "M110_error": float(source.M110_error),
            "m110": float(source.m110),
            "m110_error": float(source.m110_error),
            "source_file": "data/sbf_calib.dat",
            "source_row_zero_based": j,
        }
    elif kind == "sbf_hubble_flow":
        record["raw"] = {
            "a_sbf": float(eq["a_sbf"]),
            "a_sbf_err": float(eq["a_sbf_err"]),
            "intercept_equation": "a_sbf + 5",
            "method": "upstream compute_alpha over the published SBF flow; no manual adjustment",
            "source_file": "data/sbf_hf.dat",
        }
    elif kind == "megamaser":
        j = i - starts["mm"]
        source = mm_df.iloc[j]
        record["raw"] = {
            "name": str(source["name"]),
            "logh_value": float(source.logh_value),
            "logh_error": float(source.logh_error),
            "source_file": "data/megamaser.dat",
            "source_row_zero_based": j,
        }
    else:
        raise ValueError(("unmapped_row", i, kind))
    row_records.append(record)

npz_path = OUT / "y_obs.npz"
with (OUT / "y_obs.tmp.npz").open("wb") as handle:
    np.savez_compressed(
        handle,
        y_centered=y_centered,
        y_uncentered=y_uncentered,
        center_offsets=parameter_values,
        row_names=np.asarray(eq["eq_descr"], dtype=str),
        param_names=np.asarray([p["objname"] for p in eq["parinfo"]], dtype=str),
        A=eq["coeffs"],
        C=eq["covar"],
        null_basis=null_basis,
    )
(OUT / "y_obs.tmp.npz").replace(npz_path)

payload = {
    "status": "Y_OBS_CONSTRUCTED__NO_EVALUATION_NO_FIT",
    "row_count": 255,
    "centered_and_uncentered_are_identical": False,
    "centering_rule": "y_centered = y_uncentered - A @ x_published, using the published host distances and baseline parameters; support projection is invariant under this subtraction",
    "parameter_values": parameter_values.tolist(),
    "h_index": h_index,
    "support_check_only": {
        "null_basis_shape": list(null_basis.shape),
        "max_abs_y_times_null": support_max_abs,
        "tolerance": support_tolerance,
        "pass": support_pass,
        "diagnostics": support_diagnostics,
        "meaning": "Support validation only; estimator.evaluate was not called",
    },
    "upstream_identity": {
        "A_bit_identical_to_FREEZE": True,
        "C_bit_identical_to_FREEZE": True,
        "row_names_bit_identical": True,
        "param_names_bit_identical": True,
        "solver_called": False,
        "estimator_evaluate_called": False,
        "Z_t_h_or_ratio_computed": False,
        "new_R2_seed": False,
        "freeze_files_modified": False,
    },
    "aggregation": aggregation,
    "rows": row_records,
    "source_files": [
        {"role": role, "path": str(path), "sha256": sha(path)}
        for role, path in raw_files.items()
    ],
    "code_sources": [
        {"path": str(PKG / "main.py"), "sha256": sha(PKG / "main.py")},
        {"path": str(PKG / "equations.py"), "sha256": sha(PKG / "equations.py")},
        {"path": str(PKG / "data_loader.py"), "sha256": sha(PKG / "data_loader.py")},
        {"path": str(PKG / "intercept.py"), "sha256": sha(PKG / "intercept.py")},
        {"path": str(BASE / "network/upstream/h0_constrainer/configs/base_variants_config.ini"), "sha256": sha(BASE / "network/upstream/h0_constrainer/configs/base_variants_config.ini")},
    ],
    "outputs": {
        "y_obs_npz": str(npz_path),
        "y_obs_sha256": sha(npz_path),
        "observed_vector_only_ini": str(config_path),
        "observed_vector_only_ini_sha256": sha(config_path),
    },
}
json_path = OUT / "CONSTRUCAO_Y_OBS.json"
json_path.write_text(json.dumps(json_safe(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": payload["status"],
    "rows": len(row_records),
    "centered_equals_uncentered": False,
    "support_pass": support_pass,
    "A_C_identical": True,
    "y_obs_sha256": sha(npz_path),
    "construction_sha256": sha(json_path),
}, ensure_ascii=False, indent=2))
