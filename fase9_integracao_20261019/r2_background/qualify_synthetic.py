"""One preregistered seven-call CAMB qualification; no observed likelihood input."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import sys
import time

HERE = Path(__file__).resolve().parent


def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def new_json(path, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    temp = path.with_suffix(path.suffix + ".new")
    if path.exists():
        raise FileExistsError(path)
    with temp.open("xb") as f:
        f.write(raw)
    if temp.stat().st_size != len(raw):
        raise RuntimeError("Incomplete output")
    temp.rename(path)


def main():
    raw = (HERE / "PLAN_SYNTHETIC_R1.json").read_bytes()
    plan_sha = hashlib.sha256(raw).hexdigest()
    if len(sys.argv) != 2 or sys.argv[1] != plan_sha:
        raise RuntimeError("Independent plan pin required")
    plan = json.loads(raw)
    for item in plan["execution_pins"]:
        source = (HERE / item["path"]).read_bytes()
        if hashlib.sha256(source).hexdigest() != item["sha256"]:
            raise RuntimeError("Execution pin mismatch:" + item["path"])
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        if os.environ.get(key) != "1":
            raise RuntimeError("Single-thread environment required")
    new_json(HERE / "START_SYNTHETIC_R1.json", {"started_utc": stamp(), "plan_sha256": plan_sha, "execution_count": 1})
    start = time.perf_counter()
    import physical_background_adapter as api
    import numpy as np
    results = {}; checks = []; attempted = 0
    def check(name, passed, **detail):
        checks.append({"name": name, "passed": bool(passed), **detail})
        if not passed:
            raise AssertionError(name)
    def refused(name, operation):
        try:
            operation()
        except api.BackgroundError as exc:
            checks.append({"name": name, "passed": True, "refusal": str(exc)})
        else:
            raise AssertionError("Expected refusal:" + name)
    try:
        engine = api.load_supplier(plan["supplier_manifest_sha256"])
        cfg = json.loads((HERE / "CONFIGURATION_SYNTHETIC_R1.json").read_bytes())
        for point in cfg["points"]:
            if attempted >= plan["resources"]["max_solver_calls"] or time.perf_counter() - start >= plan["resources"]["total_timeout_seconds"]:
                raise RuntimeError("Resource budget")
            attempted += 1
            new_json(HERE / ("CALL_" + point["id"] + ".json"), {"point": point, "started_utc": stamp(), "attempt": attempted})
            result = api.predict(engine, cfg, point["id"])
            new_json(HERE / ("PREDICTION_" + point["id"] + ".json"), result)
            results[point["id"]] = result
        rows = plan["rows"]; alpha = plan["alpha_fine_input"]
        center = results["center"]
        predictions = {m: api.physical_mean(center, rows, m, alpha, 145.0 if m == "H5_rd_free" else None) for m in api.MODELS}
        tgl = predictions["H1_TGL"]; lcdm = predictions["H2_LCDM"]; h5 = predictions["H5_rd_free"]
        check("seven_real_solver_returns", len(results) == 7 and attempted == 7)
        check("h5_preserves_cmb", h5["mean"][:3] == lcdm["mean"][:3])
        h5_same = api.physical_mean(center, rows, "H5_rd_free", alpha, center["rdrag_Mpc"])
        check("h5_at_physical_rd_recovers_lcdm", np.max(np.abs(np.array(h5_same["mean"]) - lcdm["mean"])) <= 1e-12)
        check("h5_changes_bao", max(abs(x-y) for x,y in zip(h5["mean"][3:6],lcdm["mean"][3:6])) > 1e-8)
        check("tgl_background_same_local_shift_only", tgl["mean"][:6] == lcdm["mean"][:6] and tgl["mean"][6] > lcdm["mean"][6])
        sigma = np.array(plan["synthetic_row_sigma"])
        corr = np.eye(len(rows)); corr[3,4] = corr[4,3] = .2
        C = corr * sigma[:,None] * sigma[None,:]
        y = np.array(tgl["mean"])
        likelihood = {m: api.synthetic_log_likelihood(y.tolist(), p["mean"], C.tolist(), dataset_kind="SYNTHETIC") for m,p in predictions.items()}
        expected = -.5 * (np.linalg.slogdet(C)[1] + len(rows)*np.log(2*np.pi))
        check("normalized_gaussian_at_mean", abs(likelihood["H1_TGL"]["lnL"] - expected) < 1e-11)
        order = list(reversed(range(len(rows))))
        reordered = api.synthetic_log_likelihood(y[order].tolist(), np.array(tgl["mean"])[order].tolist(), C[np.ix_(order,order)].tolist(), dataset_kind="SYNTHETIC")
        check("row_permutation_invariant", abs(reordered["lnL"] - expected) < 1e-11)
        scale = np.arange(1,len(rows)+1,dtype=float)
        transformed = api.synthetic_log_likelihood((y*scale).tolist(), (y*scale).tolist(), (C*scale[:,None]*scale[None,:]).tolist(), dataset_kind="SYNTHETIC")
        check("density_measure_jacobian", abs(transformed["lnL"] - expected + np.log(scale).sum()) < 1e-10)
        J = np.column_stack([(np.array(api.physical_mean(results["plus"+str(i)],rows,"H1_TGL",alpha)["mean"]) - np.array(api.physical_mean(results["minus"+str(i)],rows,"H1_TGL",alpha)["mean"]))/(2*step) for i,step in enumerate(plan["fd_steps"])])
        H0K_J = J[6:8]
        Ctheta = np.array(plan["synthetic_covariance_theta"])
        propagated = api.propagate_theta(J.tolist(), Ctheta.tolist(), scope="LINEARIZED_SYNTHETIC_COVARIANCE")
        Cp = np.array(propagated["covariance_prediction"])
        check("common_theta_creates_common_local_covariance", Cp[6,7] > 0 and abs(Cp[6,7]-Cp[6,6]) < 1e-12 and np.max(abs(H0K_J[0]-H0K_J[1])) < 1e-12)
        check("output_covariance_psd", np.linalg.eigvalsh(Cp).min() >= -1e-9)
        conditional = api.propagate_theta(J.tolist(), None, scope="CONDITIONAL_FIXED_THETA")
        refused("unconditional_without_admitted_covariance", lambda: api.propagate_theta(J.tolist(), None, scope="UNCONDITIONAL"))
        refused("missing_covariance_is_not_zero", lambda: api.propagate_theta(J.tolist(), None, scope="LINEARIZED_SYNTHETIC_COVARIANCE"))
        refused("non_psd_covariance", lambda: api.propagate_theta(J.tolist(), [[-1,0,0],[0,1,0],[0,0,1]], scope="LINEARIZED_SYNTHETIC_COVARIANCE"))
        refused("observed_input_rejected", lambda: api.synthetic_log_likelihood(y.tolist(), y.tolist(), C.tolist(), dataset_kind="OBSERVED"))
        refused("nan_rejected", lambda: api.synthetic_log_likelihood([float('nan')]*len(y), y.tolist(), C.tolist(), dataset_kind="SYNTHETIC"))
        refused("missing_redshift_not_interpolated", lambda: api.physical_mean(center,[{"id":"bad","block":"BAO","observable":"DM_over_rd","z":.7}],"H2_LCDM",alpha))
        out = {"status":"PASS_SYNTHETIC_PHYSICAL_ENGINE_WITH_SCOPE", "passed": True,
               "checks":checks, "predictions_center":predictions, "synthetic_lnL":likelihood,
               "derivative_method":"central differences, first order propagation; truncation error not certified",
               "jacobian_rows":J.tolist(), "synthetic_covariance":C.tolist(), "propagation":propagated,
               "conditional_without_covariance":conditional,
               "frozen_scalar_K":plan["frozen_scalar_K"], "difference_Kphysical_theta_vs_frozen_scalar":tgl["K_theta"]-plan["frozen_scalar_K"],
               "no_parameter_fitting":True, "observed_reads":False, "decision_eligible":False,
               "lnB":None, "statistical_sigma":None, "physical_scope":"flat LCDM thermal-neutrino CAMB; H5 BAO-only free rd, CMB fixed prescription"}
    except BaseException as exc:
        out = {"status":"FAILED_NO_RETRY", "passed":False,"error":str(exc),"checks":checks}
    out.update({"ended_utc":stamp(), "seconds":time.perf_counter()-start,"solver_calls_attempted":attempted,"solver_calls_returned":len(results),"plan_sha256":plan_sha,"python":sys.version,"exit_code":0 if out["passed"] else 1})
    new_json(HERE / "RESULT_SYNTHETIC_R1.json", out)
    print(json.dumps({k:out[k] for k in ["status","seconds","solver_calls_attempted","solver_calls_returned","exit_code"]}))
    return out["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
