"""Independent KKT comparison and fail-closed fixtures before blinded trials."""
from pathlib import Path
import importlib.util
import hashlib
import json
import numpy as np
from scipy import linalg

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("scorer_reviewed", BASE / "estimator.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def independent_blue(A, C, h_index):
    n, p = A.shape
    block = np.block([[C, A], [A.T, np.zeros((p, p))]])
    right = np.zeros(n + p)
    right[n + h_index] = 1.0
    solution = linalg.lstsq(block, right, cond=1e-12, lapack_driver="gelsd")[0]
    return solution[:n], float(np.max(np.abs(block @ solution-right)))

def main():
    with np.load(BASE / "network/network.npz", allow_pickle=False) as net:
        A, C, c = net["A"], net["C"], net["c_cepheid"]
        hi = int(net["h_index"])
    rows, meta, null = mod.geometry(A, C, c, hi)
    result = {"geometry": meta, "comparisons": {}}
    for (label, value), design in zip(rows.items(), (A, np.column_stack([A, c]))):
        w, kkt_res = independent_blue(design, C, hi)
        err = float(np.max(np.abs(w-value["influence"])))
        var = float(w @ C @ w)
        if not (err < 1e-7 and kkt_res < 1e-8 and abs(var-value["variance_h"]) < 1e-10):
            raise ValueError("independent_KKT_disagrees")
        result["comparisons"][label] = dict(weight_difference=err, kkt_residual=kkt_res,
                                            variance=var, response_c=float(w @ c))
    # No observed centers. Deterministic four-row fixture with one duplicate.
    C0 = np.array([[1,1,0,0],[1,1,0,0],[0,0,4,0],[0,0,0,9]], float)
    A0 = np.array([[1,0],[1,0],[1,1],[1,-1]], float)
    c0 = np.array([0,0,1,0], float)
    f, fm, fn = mod.geometry(A0, C0, c0, 0)
    assert fm["cov_rank"] == 3 and fm["cov_nullity"] == 1
    bad = c0 + np.array([1,-1,0,0])
    try:
        mod.geometry(A0, C0, bad, 0)
    except ValueError as error:
        assert "deterministic" in str(error)
    else:
        raise AssertionError("invalid support admitted")
    fixture = dict(weights=np.stack([x["influence"] for x in f.values()]), null_basis=fn,
                   gradient_h=np.array([1,0,0]), gradient_k=np.zeros(3),
                   sd_null=np.ones(2), sd_tgl=np.ones(2), logK=np.array(0.1), H0=np.array(67.))
    data = dict(local=np.array([[3,3,7,-1.]]), background=np.zeros((1,3)))
    scored = mod.evaluate(data, fixture)
    assert np.isfinite(scored["z_null"]).all()
    data["local"][0,0] = np.nan
    try:
        mod.evaluate(data, fixture)
    except ValueError as error:
        assert "nonfinite" in str(error)
    else:
        raise AssertionError("NaN admitted")
    result["fixtures"] = ["singular_support_rank","forbidden_support_response_refused","finite_score","NaN_refused"]
    result["sources"] = {str(path):hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in [BASE/"estimator.py",BASE/"network/network.npz",Path(__file__)]}
    dest = Path(__file__).with_name("INDEPENDENT_GEOMETRY_REVIEW.json")
    with dest.open("x", encoding="utf-8") as handle:
        json.dump(result,handle,indent=2)
    print(json.dumps(result,indent=2))
if __name__ == "__main__":
    main()

