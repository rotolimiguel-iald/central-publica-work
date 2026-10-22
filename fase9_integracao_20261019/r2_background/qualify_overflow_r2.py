"""Focused R2 arithmetic regression; does not load/call CAMB or a supplier."""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import math
import sys
import time

HERE = Path(__file__).resolve().parent


def write_new(name, obj):
    with (HERE / name).open("x", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, allow_nan=False)


def main():
    plan_raw = (HERE / "PLAN_OVERFLOW_R2.json").read_bytes()
    digest = hashlib.sha256(plan_raw).hexdigest()
    if len(sys.argv) != 2 or digest != sys.argv[1]:
        raise RuntimeError("Independent preregistration pin required")
    plan = json.loads(plan_raw)
    for item in plan["pins"]:
        if hashlib.sha256((HERE / item["name"]).read_bytes()).hexdigest() != item["sha256"]:
            raise RuntimeError("Execution pin mismatch")
    if (HERE / "RESULT_OVERFLOW_R2.json").exists():
        raise RuntimeError("Prior result present")
    start = datetime.datetime.now(datetime.timezone.utc).isoformat(); clock = time.perf_counter()
    write_new("START_OVERFLOW_R2.json", {"started_utc": start, "plan_sha256": digest, "execution_count": 1, "solver_calls": 0})
    records = []; exit_code = 1
    try:
        import physical_background_adapter_r2 as api
        import numpy as np
        old = json.loads((HERE / "RESULT_SYNTHETIC_R1.json").read_bytes())
        original_plan = json.loads((HERE / "PLAN_SYNTHETIC_R1.json").read_bytes())
        bg = json.loads((HERE / "PREDICTION_center.json").read_bytes())
        def check(name, condition):
            if not condition:
                raise AssertionError(name)
            records.append({"name": name, "passed": True})
        def refuse(name, callback):
            try:
                callback()
            except api.BackgroundError as exc:
                records.append({"name": name, "passed": True, "refusal": str(exc)})
            else:
                raise AssertionError("Nonfinite result accepted:" + name)
        for model in api.MODELS:
            p = api.physical_mean(bg, original_plan["rows"], model, original_plan["alpha_fine_input"], 145.0 if model == "H5_rd_free" else None)
            check("nominal_mean_" + model, p == old["predictions_center"][model])
        mu = old["predictions_center"]["H1_TGL"]["mean"]
        ll = api.synthetic_log_likelihood(mu, mu, old["synthetic_covariance"], dataset_kind="SYNTHETIC")
        check("nominal_likelihood_unchanged", ll == old["synthetic_lnL"]["H1_TGL"])
        cp = api.propagate_theta(old["jacobian_rows"], original_plan["synthetic_covariance_theta"], scope="LINEARIZED_SYNTHETIC_COVARIANCE")
        check("nominal_propagation_unchanged", cp == old["propagation"])
        refuse("quadratic_overflow", lambda: api.synthetic_log_likelihood([1e308], [0.0], [[1.0]], dataset_kind="SYNTHETIC"))
        refuse("residual_subtraction_overflow", lambda: api.synthetic_log_likelihood([1e308], [-1e308], [[1.0]], dataset_kind="SYNTHETIC"))
        refuse("propagated_matrix_overflow", lambda: api.propagate_theta([[1e200,0,0]], np.eye(3).tolist(), scope="LINEARIZED_SYNTHETIC_COVARIANCE"))
        refuse("intermediate_matrix_overflow", lambda: api.propagate_theta([[1e200,0,0]], (np.eye(3)*1e200).tolist(), scope="LINEARIZED_SYNTHETIC_COVARIANCE"))
        enormous = copy.deepcopy(bg); enormous["E_law"] = 1e308; enormous["I_law"] = 2*math.log(1e308)/3
        refuse("K_exponential_overflow", lambda: api.physical_mean(enormous, original_plan["rows"], "H1_TGL", .999))
        enormous["theta"][0] = 1e308
        refuse("H0_times_K_overflow", lambda: api.physical_mean(enormous, original_plan["rows"], "H1_TGL", original_plan["alpha_fine_input"]))
        refuse("huge_int_conversion", lambda: api.synthetic_log_likelihood([10**400], [0], [[1]], dataset_kind="SYNTHETIC"))
        check("no_camb_import", "camb" not in sys.modules)
        exit_code = 0
        error = None
    except BaseException as exc:
        error = type(exc).__name__ + ":" + str(exc)
    result = {"schema": "F3_OVERFLOW_R2_RESULT", "passed": exit_code == 0, "exit_code": exit_code,
              "checks": records, "count": len(records), "error": error, "started_utc": start,
              "ended_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "seconds": time.perf_counter()-clock,
              "plan_sha256": digest, "solver_calls": 0, "observed_reads": False,
              "historical_CAMB_calls": "Seven R1 calls preserved, not repeated"}
    write_new("RESULT_OVERFLOW_R2.json", result)
    print(json.dumps({k:result[k] for k in ("passed","count","exit_code","seconds","solver_calls","error")}))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
