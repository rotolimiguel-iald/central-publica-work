"""Bounded replay of the canonical v392 consumer, with the preregistered rule.

Never import um.py. Execute only the five pinned AST FunctionDefs and the alpha
assignment. Capture the actual consumer's local closures with a return profiler.
Run --freeze first, then --replay <freeze receipt>; every execution is immutable.
No observed data, network, persistent service, production write, or gate change.
"""
from __future__ import annotations

import argparse
import ast
import copy
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time
import traceback

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCES = ROOT / "sources"
FUNCTIONS = {
    "prove_decision_commutation", "_recognition_reading_modes",
    "_v361_pinch", "_v361_herm_fn", "_v361_flow",
}
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


class ContractError(ValueError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True,
                      allow_nan=False).encode("utf-8")


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def pin(path):
    data = Path(path).read_bytes()
    return {"relative_path": relative(path), "sha256": digest(data), "bytes": len(data)}


def new(path, value):
    path = Path(path)
    data = value if isinstance(value, bytes) else encode(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(path)
    tmp = path.with_name(path.name + ".tmp_" + stamp())
    with tmp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if tmp.read_bytes() != data or path.exists():
        raise ContractError("Atomic output verification failed")
    tmp.rename(path)


def check_hash(data, expected, label):
    if digest(data) != expected:
        raise ContractError("Stale or corrupted bytes: " + label)


def basename(path):
    return str(path).replace("\\", "/").split("/")[-1]


def freeze():
    """Hash code and inputs without running the scientific consumer."""
    files = [Path(__file__), ROOT / "PREREGISTRO_R1.json", ROOT / "SOURCE_MANIFEST.json"]
    manifest = json.loads(files[2].read_bytes())
    prereg = json.loads(files[1].read_bytes())
    check_hash(files[2].read_bytes(), prereg["sources"]["sha256"], "source manifest")
    for entry in manifest["copies"]:
        candidate = SOURCES / basename(entry["path"])
        check_hash(candidate.read_bytes(), entry["sha256"], candidate.name)
        files.append(candidate)
    receipt = HERE / "freezes" / (stamp() + ".json")
    new(receipt, {"created_utc": now(), "unit": "F1.REGRA.MOTOR",
                  "phase": "CODE_AND_INPUTS_FROZEN_BEFORE_CONSUMER_EXECUTION",
                  "files": [pin(p) for p in files],
                  "runtime": runtime_info(), "run_started": False})
    print(str(receipt))


def runtime_info():
    return {"python_executable": sys.executable, "python": sys.version,
            "numpy": np.__version__, "platform": platform.platform(),
            "float_dtype": "float64/complex128"}


def verify_freeze(receipt):
    frozen = json.loads(receipt.read_bytes())
    if frozen["phase"] != "CODE_AND_INPUTS_FROZEN_BEFORE_CONSUMER_EXECUTION":
        raise ContractError("Not a pre-execution freeze")
    for entry in frozen["files"]:
        path = (ROOT / entry["relative_path"]).resolve()
        if not path.is_relative_to(ROOT):
            raise ContractError("Frozen path escaped the unit")
        data = path.read_bytes()
        check_hash(data, entry["sha256"], entry["relative_path"])
        if len(data) != entry["bytes"]:
            raise ContractError("Frozen length mismatch")
    return frozen


def load_actual():
    """Validate source identity and recorded axioms before compiling a tiny AST."""
    manifest = json.loads((ROOT / "SOURCE_MANIFEST.json").read_bytes())
    original = ast.parse((SOURCES / "um.py").read_bytes())
    extracted_bytes = (SOURCES / "actual_consumer_functions.py").read_bytes()
    extracted = ast.parse(extracted_bytes)
    original_nodes = {n.name: n for n in original.body
                      if isinstance(n, ast.FunctionDef) and n.name in FUNCTIONS}
    alpha_nodes = [n for n in original.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "SEALED_CODATA_ALPHA" for t in n.targets)]
    if len(alpha_nodes) != 1 or len(original_nodes) != 5:
        raise ContractError("Canonical AST boundary not found")
    expected = {**original_nodes, "SEALED_CODATA_ALPHA": alpha_nodes[0]}
    found = set()
    for node in extracted.body:
        name = node.name if isinstance(node, ast.FunctionDef) else "SEALED_CODATA_ALPHA"
        if name in found or name not in expected or ast.dump(node) != ast.dump(expected[name]):
            raise ContractError("Extraction differs from canonical AST")
        found.add(name)
    if found != set(expected):
        raise ContractError("Missing extracted AST")
    proof = json.loads((SOURCES / "tgl_kernel_proof_manifest.json").read_bytes())
    kernel_key = "TGLExt/DecisionCommutation.lean"
    embedded = []
    for node in ast.walk(original):
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and key.value == kernel_key and isinstance(value, ast.Constant):
                    embedded.append(value.value)
    if len(set(embedded)) != 1:
        raise ContractError("Ambiguous kernel source")
    check_hash(embedded[0].encode("utf-8"), proof["formal_files_sha256"][kernel_key], kernel_key)
    records = manifest["recorded_kernel_evidence"]
    if len(records) != 10:
        raise ContractError("Expected ten actual theorem records")
    flags = {}
    for name, record in records.items():
        axioms = proof["axiom_report"].get(record["declaration"])
        if (record.get("verified") is not True or not isinstance(axioms, list)
                or axioms != record["axioms"] or not set(axioms) <= ALLOWED_AXIOMS):
            raise ContractError("Kernel evidence invalid: " + name)
        flags[name] = True
    environment = {"math": math, "np": np}
    exec(compile(extracted, str(SOURCES / "actual_consumer_functions.py"), "exec"), environment)
    return environment, {"external_ladder": {"per_theorem": flags}}, records


def capture_consumer(environment, parts):
    consumer = environment["prove_decision_commutation"]
    captured = {}
    previous = sys.getprofile()

    def profiler(frame, event, arg):
        if event == "return" and frame.f_code is consumer.__code__:
            captured.update(frame.f_locals)

    try:
        sys.setprofile(profiler)
        result = consumer(1, copy.deepcopy(parts))
    finally:
        sys.setprofile(previous)
    for key in ("recognize", "recognize_flow", "gamma", "rho", "c_plus", "c_minus"):
        if key not in captured:
            raise ContractError("Actual runtime closure not captured: " + key)
    return result, captured


def finite_number(value, name, minimum=0.0, positive=False):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.integer, np.floating)):
        raise ContractError(name + " must be a numeric non-boolean scalar")
    number = float(value)
    if not math.isfinite(number) or number < minimum or (positive and number <= minimum):
        raise ContractError(name + " is not finite/in range")
    return number


def valid_state(value, tol, label):
    arr = np.asarray(value)
    if arr.shape != (4, 4) or arr.dtype.kind not in "fci":
        raise ContractError(label + " must be a numeric 4x4 matrix, excluding booleans")
    arr = np.asarray(arr, dtype=np.complex128)
    if not np.isfinite(arr).all():
        raise ContractError(label + " contains nonfinite entries")
    if np.linalg.norm(arr - arr.conj().T) > tol:
        raise ContractError(label + " is not Hermitian")
    if abs(np.trace(arr) - 1.0) > tol or float(np.linalg.eigvalsh(arr).min()) < -tol:
        raise ContractError(label + " must have trace one and be positive")
    return arr


class RuleMotor:
    def __init__(self, captured, target, spec, flags):
        self.tol = finite_number(spec["tol_algebra"], "tol_algebra", positive=True)
        self.rule_tol = finite_number(spec["tol_rule"], "tol_rule", positive=True)
        self.rate = finite_number(captured["gamma"], "rate", positive=True)
        if len(flags) != 10 or any(v is not True for v in flags.values()):
            raise ContractError("Incomplete kernel evidence")
        self.read = captured["recognize"]
        self._flow = captured["recognize_flow"]
        self.target = valid_state(target, self.tol, "target").copy()
        if np.linalg.norm(self.read(self.target) - self.target) > self.tol:
            raise ContractError("Target must be fixed by the actual reading")

    def evaluate(self, state, exposure):
        state = valid_state(state, self.tol, "state")
        exposure = finite_number(exposure, "exposure")
        evolved = valid_state(self._flow(state, exposure / self.rate), self.tol, "evolved state")
        inscription = self.read(evolved)
        read_error = float(np.linalg.norm(inscription - self.target))
        raw_error = float(np.linalg.norm(evolved - self.target))
        admitted = read_error <= self.rule_tol
        return {"exposure": exposure, "time_reference_units": exposure / self.rate,
                "state_real": evolved.real.tolist(), "state_imag": evolved.imag.tolist(),
                "reading_real": inscription.real.tolist(), "reading_imag": inscription.imag.tolist(),
                "read_error_hs": read_error, "raw_error_hs": raw_error,
                "read_rule": admitted, "raw_rule": raw_error <= self.rule_tol,
                "verdict": "SATISFACTION_ADMITTED" if admitted else "SATISFACTION_REFUSED",
                "trace_error": float(abs(np.trace(evolved) - 1.0)),
                "hermiticity_error": float(np.linalg.norm(evolved - evolved.conj().T)),
                "minimum_eigenvalue": float(np.linalg.eigvalsh(evolved).min()),
                "complement_norm_hs": float(np.linalg.norm(evolved - inscription))}


def execute(receipt):
    start, timer = now(), time.perf_counter()
    attempt = HERE / "runs" / stamp()
    attempt.mkdir(parents=True, exist_ok=False)
    checks = []

    def check(name, predicate, details=None):
        entry = {"name": name, "passed": bool(predicate)}
        if details is not None:
            entry["details"] = details
        checks.append(entry)
        if not entry["passed"]:
            raise ContractError("Verification failed: " + name)

    def refused(name, action):
        try:
            action()
        except (ContractError, ValueError, TypeError) as exc:
            check(name, True, {"refused_with": type(exc).__name__, "message": str(exc)})
        else:
            check(name, False)

    try:
        frozen = verify_freeze(receipt)
        spec = json.loads((ROOT / "PREREGISTRO_R1.json").read_bytes())
        new(attempt / "INPUT.json", {"start_utc": start, "command": [sys.executable, *sys.argv],
                                     "cwd": os.getcwd(), "runtime": runtime_info(),
                                     "freeze": {"path": str(receipt), "sha256": digest(receipt.read_bytes())},
                                     "frozen_inputs": frozen["files"], "preregistration": spec})
        environment, parts, evidence = load_actual()
        result, actual = capture_consumer(environment, parts)
        new(attempt / "ACTUAL_CONSUMER_RESULT.json", result)
        check("actual_consumer_all_verified", result["all_verified"] is True)
        check("both_reading_modes_verified", all(v["ok"] for v in result["recognition_dephasing"]["reading_modes"]["modes"].values()))
        check("gate_unchanged", result["does_not_gate_core"] is True)
        target = np.array(spec["target_real"], dtype=float) + 1j * np.array(spec["target_imag"], dtype=float)
        flags = parts["external_ladder"]["per_theorem"]
        motor = RuleMotor(actual, target, spec, flags)
        initial = actual["rho"].copy()
        E, flow, rate = actual["recognize"], actual["recognize_flow"], actual["gamma"]
        tol = spec["tol_algebra"]
        check("target_predefined_equals_actual_reading", np.linalg.norm(E(initial) - target) <= tol)
        check("rate_from_runtime_beta", rate == environment["SEALED_CODATA_ALPHA"] * math.sqrt(math.e) / 2.0)
        grid = spec["exposure_grid"]
        exposures = np.linspace(grid["start"], grid["stop"], grid["count"])
        rows = [motor.evaluate(initial, float(x)) for x in exposures]
        previous_hash = "0" * 64
        ledger = []
        for index, row in enumerate(rows):
            item = {"index": index, "previous_sha256": previous_hash, "record": row}
            previous_hash = digest(compact(item))
            item["sha256"] = previous_hash
            ledger.append(compact(item))
        new(attempt / "TRAJECTORY.jsonl", b"\n".join(ledger) + b"\n")
        check("read_rule_all_points", all(r["read_rule"] for r in rows))
        check("raw_rule_false_all_finite_points", all(not r["raw_rule"] for r in rows))
        norms = [r["complement_norm_hs"] for r in rows]
        check("complement_strictly_decreases", all(a > b > 0.0 for a, b in zip(norms, norms[1:])))
        decay_error = max(abs(r["complement_norm_hs"] - norms[0] * math.exp(-r["exposure"])) for r in rows)
        check("prescribed_exponential_decay", decay_error <= tol, decay_error)
        # Matrix units test the entire linear operator, rather than one state.
        units = [np.eye(16, dtype=complex)[:, i].reshape(4, 4) for i in range(16)]
        E_matrix = np.column_stack([E(u).reshape(16) for u in units])
        check("E_idempotence_on_full_space", np.linalg.norm(E_matrix @ E_matrix - E_matrix) <= tol)
        check("E_self_adjoint_HS", np.linalg.norm(E_matrix - E_matrix.conj().T) <= tol)
        fixed_dimension = int(np.sum(np.linalg.svd(E_matrix, compute_uv=False) > spec["spectral_cutoff"]))
        check("fixed_complex_dimension_eight", fixed_dimension == 8, fixed_dimension)
        # Independent GKLS construction, using jumps, then spectral exponential.
        jumps = [math.sqrt(rate) * actual[p] for p in ("c_plus", "c_minus")]
        generator = np.column_stack([sum((j @ u @ j.conj().T - 0.5 *
                                         ((j.conj().T @ j) @ u + u @ (j.conj().T @ j)))
                                        for j in jumps).reshape(16) for u in units])
        check("GKLS_generator_matches_actual_law", np.linalg.norm(generator - rate * (E_matrix - np.eye(16))) / rate <= tol)
        values, vectors = np.linalg.eigh(generator)
        check("GKLS_generator_Hermitian", np.linalg.norm(generator - generator.conj().T) <= tol)
        check("GKLS_generator_nonpositive", float(values.max()) <= tol)
        check("GKLS_nullity_eight", int(np.sum(np.abs(values / rate) <= spec["spectral_cutoff"])) == 8)
        oracle = lambda exposure: (vectors * np.exp(values * exposure / rate)) @ vectors.conj().T
        errors = []
        composed_errors = []
        semigroup_errors = []
        for exposure in spec["exposure_checkpoints"]:
            actual_operator = np.column_stack([flow(u, exposure / rate).reshape(16) for u in units])
            errors.append(float(np.linalg.norm(actual_operator - oracle(exposure))))
            oracle_state = (oracle(exposure) @ initial.reshape(16)).reshape(4, 4)
            composed = flow(flow(initial, 0.37 * exposure / rate), 0.63 * exposure / rate)
            composed_errors.append(float(np.linalg.norm(composed - oracle_state)))
            semigroup_errors.append(float(np.linalg.norm(composed - flow(initial, exposure / rate))))
        check("independent_GKLS_all_operator_checkpoints", max(errors) <= tol, max(errors))
        check("independent_GKLS_composed_trajectory", max(composed_errors) <= tol, max(composed_errors))
        check("semigroup_checkpoints", max(semigroup_errors) <= tol, max(semigroup_errors))
        check("reading_and_flow_commute", max(float(np.linalg.norm(E(flow(initial, x / rate)) - flow(E(initial), x / rate))) for x in exposures) <= tol)
        check("trace_preserved", max(r["trace_error"] for r in rows) <= tol)
        check("Hermiticity_preserved", max(r["hermiticity_error"] for r in rows) <= tol)
        check("positivity_preserved", min(r["minimum_eigenvalue"] for r in rows) >= -tol)
        # The result verdict is determined by the new rule, not a detached label.
        incompatible = np.diag([1.0, 0.0, 0.0, 0.0]).astype(complex)
        incompatible_rows = [motor.evaluate(incompatible, float(x)) for x in spec["exposure_checkpoints"]]
        check("incompatible_fixed_input_is_refused", all(not r["read_rule"] and r["verdict"] == "SATISFACTION_REFUSED" for r in incompatible_rows))
        alternative_motor = RuleMotor(actual, incompatible, spec, flags)
        check("incompatible_fixed_target_is_refused", alternative_motor.evaluate(initial, 1.0)["verdict"] == "SATISFACTION_REFUSED")
        check("idempotence_does_not_force_target", np.linalg.norm(E(E(incompatible)) - E(incompatible)) <= tol and np.linalg.norm(E(incompatible) - target) > spec["tol_rule"])
        zero_rate_control = E(initial) + math.exp(-0.0 * 1.0) * (initial - E(initial))
        check("zero_rate_leaves_complement_unchanged", np.linalg.norm(zero_rate_control - initial) <= tol and np.linalg.norm(zero_rate_control - target) > spec["tol_rule"])
        for value in (float("nan"), float("inf"), -float("inf"), True, False, -1.0, "1"):
            refused("invalid_exposure_" + repr(value), lambda v=value: motor.evaluate(initial, v))
        for value in (-1.0, 0.0, float("nan"), float("inf"), True, False):
            bad = {**actual, "gamma": value}
            refused("invalid_rate_" + repr(value), lambda b=bad: RuleMotor(b, target, spec, flags))
        invalid_states = {
            "boolean_matrix": np.eye(4, dtype=bool), "wrong_shape": np.eye(2),
            "trace_two": np.eye(4) / 2.0, "nonpositive": np.diag([2., -1., 0., 0.]),
            "nonhermitian": initial + np.eye(4, k=1) * 0.1,
            "NaN": np.full((4, 4), float("nan")), "Inf": np.full((4, 4), float("inf")),
        }
        for name, value in invalid_states.items():
            refused("invalid_state_" + name, lambda v=value: motor.evaluate(v, 1.0))
            refused("invalid_target_" + name, lambda v=value: RuleMotor(actual, v, spec, flags))
        refused("target_not_fixed", lambda: RuleMotor(actual, initial, spec, flags))
        for missing in flags:
            bad_flags = {k: v for k, v in flags.items() if k != missing}
            refused("missing_evidence_preflight_" + missing, lambda bf=bad_flags: RuleMotor(actual, target, spec, bf))
            bad_result = environment["prove_decision_commutation"](1, {"external_ladder": {"per_theorem": bad_flags}})
            check("missing_evidence_consumer_" + missing, bad_result["all_verified"] is False)
        source_bytes = (SOURCES / "actual_consumer_functions.py").read_bytes()
        corrupted = bytes([source_bytes[0] ^ 1]) + source_bytes[1:]
        refused("one_bit_source_corruption", lambda: check_hash(corrupted, digest(source_bytes), "actual consumer"))
        new(attempt / "NEGATIVE_CONTROLS.json", {"incompatible_fixed_input": incompatible_rows,
                                                "incompatible_target_verdict": alternative_motor.evaluate(initial, 1.0),
                                                "zero_rate_change": float(np.linalg.norm(zero_rate_control - initial)),
                                                "zero_rate_is_control_not_production_law": True})
        summary = {"passed": True, "status": "FINITE_CONTINUOUS_MOTOR_RULE_VERIFIED",
                   "rule_dependent_verdict": rows[-1]["verdict"], "incompatible_verdict": incompatible_rows[-1]["verdict"],
                   "checks": checks, "checks_passed": len(checks), "point_count": len(rows),
                   "beta_runtime": result["values"]["beta"], "gamma_reference": rate,
                   "fixed_space_complex_dimension": fixed_dimension,
                   "complement_initial": norms[0], "complement_final": norms[-1],
                   "maximum_read_error_hs": max(r["read_error_hs"] for r in rows),
                   "maximum_oracle_operator_error_hs": max(errors),
                   "maximum_composed_oracle_error_hs": max(composed_errors),
                   "maximum_semigroup_error_hs": max(semigroup_errors),
                   "minimum_state_eigenvalue": min(r["minimum_eigenvalue"] for r in rows),
                   "trajectory_last_hash": previous_hash, "kernel_evidence": evidence,
                   "scope": "Finite synthetic trajectory; rate units INPUT; neither physical confirmation nor exact equality from tolerance.",
                   "raw_state_and_reading_kept_separate": True, "does_not_gate_core": True,
                   "daemon": False, "observed_data": False}
        exit_code = 0
    except Exception as exc:
        summary = {"passed": False, "status": "REFUSED_OR_FAILED", "checks": checks,
                   "exception": type(exc).__name__, "error": str(exc), "traceback": traceback.format_exc()}
        exit_code = 1
    finish = now()
    summary.update({"start_utc": start, "finish_utc": finish, "seconds": time.perf_counter() - timer,
                    "exit_code": exit_code, "runtime": runtime_info(),
                    "artifacts": [pin(p) for p in sorted(attempt.iterdir()) if p.is_file()]})
    new(attempt / "RESULT.json", summary)
    print(json.dumps({"result": str(attempt / "RESULT.json"), "passed": summary["passed"],
                      "exit_code": exit_code, "seconds": summary["seconds"]}))
    return exit_code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--freeze", action="store_true")
    group.add_argument("--replay", type=Path, help="Immutable freeze JSON; resolve relative to current working directory")
    args = parser.parse_args()
    if args.freeze:
        freeze()
        return 0
    return execute(args.replay.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
