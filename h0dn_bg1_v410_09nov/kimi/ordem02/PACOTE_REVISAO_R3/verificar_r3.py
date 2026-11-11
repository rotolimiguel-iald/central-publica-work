from pathlib import Path
import hashlib
import json
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED = {
    "SEEDS_R3_REGISTRADAS.json": "bf672cfbc01a22d992f1622316a81eae1008ab35a37f22c9ad2126a7cb44b6a0",
    "C_fisica_R3_A1_REDUCIDA.npz": "ca24579ec4af62f8134c590fdf80e781b486029795177cba763bfe804dc89124",
    "A1_HOST_DECOMPOSITION.json": "b852a31deeb4296dbd7fc97f8d2f6dad7777e4d703bd0cdf8fa9fa938447ce95",
    "DECOMPOSICAO_FISICA_R3.json": "b8e0afb59d74f8be5edaaf0913fb91418852a198a6df9866722301b579dbd1db",
    "CERTIFICADO_DE_PODER_R3.json": "c36c35d1c3148e090ab000a7837aa7557adc5df5bf0abe303a94a5d649095b16",
    "A1_SINTETICOS.json": "075f635f13268c9062f0eec659f2d9026d68669b6afbb5c2151f25dca2087600",
    "PACOTE_REVISAO_R3/ORDEM_REVISAO_R3.md": "2e25461d66f64ff0230be6ac840d3126658074ec9f142d66e9cfdb07a36c0d7c",
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

hashes = {name: sha(ROOT / name) for name in EXPECTED}
seeds = json.loads((ROOT / "SEEDS_R3_REGISTRADAS.json").read_text(encoding="utf-8"))
decomp = json.loads((ROOT / "DECOMPOSICAO_FISICA_R3.json").read_text(encoding="utf-8"))
cert = json.loads((ROOT / "CERTIFICADO_DE_PODER_R3.json").read_text(encoding="utf-8"))
syn = json.loads((ROOT / "A1_SINTETICOS.json").read_text(encoding="utf-8"))
with np.load(ROOT / "C_fisica_R3_A1_REDUCIDA.npz", allow_pickle=False) as d:
    A, C = d["A"], d["C"]
    B = d["exact_host_constraints"]
    sigma = d["sigma_independent"]
    FH = d["F_HMS_effective"]
    FM = d["F_MAS_host"]
    FA = d["F_anchor_host"]
    C_rec = np.diag(sigma ** 2) + FH @ FH.T + FM @ FM.T + FA @ FA.T
    host_error = float(np.max(np.abs(C_rec - C[:166, :166])))
    null_C = float(np.max(np.abs(C[:166, :166] @ B)))
    null_A = float(np.max(np.abs(B.T @ A[:166])))
    rank = int(np.linalg.matrix_rank(C))
    host_rank = int(np.linalg.matrix_rank(C[:166, :166]))
    symmetry = float(np.max(np.abs(C - C.T)))
    forbidden = sorted(set(d.files) & {"y", "y_obs", "local", "observed", "observed_y"})
checks = {
    "hashes_match": hashes == EXPECTED,
    "covariance_symmetric": symmetry < 1e-14,
    "full_support_rank_183": rank == 183,
    "host_rank_94": host_rank == 94,
    "constraint_rank_72": int(np.linalg.matrix_rank(B)) == 72,
    "constraint_null_C": null_C < 1e-12,
    "constraint_null_A": null_A < 1e-10,
    "host_reconstruction_exact": host_error < 1e-14,
    "synthetic_only_pass": syn["status"] == "A1_SYNTHETIC_SUPPORT_AND_ESTIMATOR_PASS" and syn["deterministic_no_RNG"] and syn["out_of_support_synthetic_rejected"],
    "synthetic_precision": syn["published_baseline_max_parameter_recovery_error"] < 1e-7 and syn["free_cepheid_model_max_parameter_recovery_error"] < 1e-7,
    "no_admitted_variant": decomp["admitted_physical_variants"] == [] and cert["admitted_variants"] == [],
    "power_not_evaluable": cert["power_gate"] == "NOT_EVALUABLE" and cert["D_by_variant_and_model"] == {} and cert["D_conservador"] is None,
    "mc_not_run": cert["mc_status"] == "NOT_RUN_NO_ADMITTED_COVARIANCE",
    "no_new_seeds": seeds["new_seed_count"] == 0 and seeds["rng_called"] is False and seeds["R2_seeds_read_or_touched"] is False,
    "opening_blocked": decomp["opening_allowed"] is False and cert["opening_allowed"] is False,
    "no_observed_arrays": len(forbidden) == 0,
    "no_observed_support_now": decomp["observed_support_tests_now"] == 0 and syn["observed_support_tests"] == 0,
}
validated = all(checks.values())
result = {
    "status": "R3_REVIEW_VALIDATED__A1_ALGEBRA_CLOSED__POWER_NOT_EVALUABLE" if validated else "R3_REVIEW_VALIDATION_FAILED",
    "A1_algebra_closed": True,
    "full_physical_covariance_closed": False,
    "admitted_variants": [],
    "D_conservador": None,
    "power_gate": "NOT_EVALUABLE",
    "mc_status": "NOT_RUN_NO_ADMITTED_COVARIANCE",
    "new_seed_count": 0,
    "observed_vector_read": False,
    "observed_support_tests_now": 0,
    "opening_allowed": False,
    "checks": checks,
    "metrics": {"host_reconstruction_max_abs": host_error, "constraint_C_max_abs": null_C, "constraint_A_max_abs": null_A, "covariance_rank": rank, "host_rank": host_rank},
    "hashes": hashes,
}
(HERE / "VALIDACAO_R3.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
if not validated:
    raise RuntimeError("R3 review validation failed")
