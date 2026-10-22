"""Exercise the real patched consumer, not an import of um.py or a fake gate."""
from pathlib import Path
from datetime import datetime
import ast
import copy
import hashlib
import json
import math
import os
import sys
import numpy as np

ROOT = Path(__file__).resolve().parent
old_bytes = (ROOT / "um_ORIGINAL_SNAPSHOT.py").read_bytes()
new_bytes = (ROOT / "um.py").read_bytes()
old_tree = ast.parse(old_bytes)
new_tree = ast.parse(new_bytes)
manifest = json.loads((ROOT / "tgl_kernel_proof_manifest.json").read_bytes())
cases = []


def check(name, condition):
    cases.append({"name": name, "passed": bool(condition)})
    if not condition:
        raise AssertionError(name)


def function_node(tree):
    return next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                and n.name == "prove_decision_commutation")


def load_consumer(tree, replacement=None):
    node = copy.deepcopy(function_node(tree))
    if replacement:
        code = ast.unparse(node)
        old, new = replacement
        if old not in code:
            raise AssertionError("Mutation does not hit its target: " + old)
        node = ast.parse(code.replace(old, new, 1)).body[0]
    alpha = next(n for n in tree.body if isinstance(n, ast.Assign)
                 and any(isinstance(a, ast.Name) and a.id == "SEALED_CODATA_ALPHA"
                         for a in n.targets))
    module = ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(alpha), node], type_ignores=[]))
    env = {"math": math, "np": np}
    exec(compile(module, "<actual-um-consumer>", "exec"), env)
    return env["prove_decision_commutation"], env["SEALED_CODATA_ALPHA"]


flag_names = {}
sources = {}
for node in ast.walk(new_tree):
    if isinstance(node, ast.Dict):
        for key, value in zip(node.keys, node.values):
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                if key.value.startswith("ext_kd_") and isinstance(value, ast.Constant):
                    flag_names[key.value] = value.value
                if key.value == "TGLExt/DecisionCommutation.lean" and isinstance(value, ast.Constant):
                    sources[key.value] = value.value
check("existing_ten_kernel_consumers_located", len(flag_names) == 10)
source_hashes = {name: hashlib.sha256(source.encode("utf-8")).hexdigest()
                 for name, source in sources.items()}
check("existing_embedded_source_matches_copied_proof_manifest",
      bool(source_hashes) and all(manifest["formal_files_sha256"].get(k) == v
                                  for k, v in source_hashes.items()))
allowed = {"propext", "Classical.choice", "Quot.sound"}
per_theorem = {}
for flag, theorem in flag_names.items():
    axioms = manifest["axiom_report"].get(theorem)
    valid = isinstance(axioms, list) and all(isinstance(a, str) and a in allowed for a in axioms)
    check("recorded_axioms:" + theorem, valid)
    per_theorem[flag] = valid
parts = {"external_ladder": {"per_theorem": per_theorem}}
original, original_alpha = load_consumer(old_tree)
modified, alpha = load_consumer(new_tree)
before = original(1, copy.deepcopy(parts))
after = modified(1, copy.deepcopy(parts))
check("baseline_consumer_passes_with_matching_recorded_evidence", before["all_verified"])
check("extended_consumer_passes", after["all_verified"])
check("existing_numeric_values_unchanged", before["values"] == after["values"])
check("existing_verdict_unchanged", before["verdict"] == after["verdict"])
check("recorded_evidence_not_mutated", parts["external_ladder"]["per_theorem"] == per_theorem)
check("core_gate_remains_outside_this_consumer", after["does_not_gate_core"] is True)
report = after["recognition_dephasing"]
check("recognition_report_present_and_passes", report["all_verified"])
check("selected_state_fixed", report["selected_state_is_fixed"] is True)
check("full_state_has_effective_dephasing", report["effective_dephasing_on_full_state"] is True)
check("postselection_is_not_reported_as_effective_dephasing",
      report["effective_dephasing_after_selection"] is False)
check("beta_computed_from_source_alpha", report["rate"]["beta"] == alpha * math.sqrt(math.e))
check("reference_rate_not_a_physical_prediction",
      report["rate"]["status"] == "REFERENCE_UNITS_ONLY_NOT_A_PHYSICAL_PREDICTION")
check("time_law_is_explicit_input", report["time_law_status"].startswith("INPUT:"))
check("no_new_kernel_theorem_claim", "not a new kernel theorem" in report["kernel_status"])

# Independent oracle: construct the Liouvillian from jump operators on all
# matrix units, then exponentiate by Hermitian diagonalization. No closed-form
# recognition_flow from the implementation is used for this evaluation.
gamma = report["rate"]["gamma_reference"]
c_plus = np.diag([1., 1., 0., 0.]).astype(complex)
c_minus = np.eye(4) - c_plus
jumps = [np.sqrt(gamma) * p for p in (c_plus, c_minus)]
liouvillian = np.zeros((16, 16), dtype=complex)
for col in range(16):
    unit = np.zeros(16, dtype=complex)
    unit[col] = 1.
    state = unit.reshape(4, 4)
    derivative = sum((jump @ state @ jump.conj().T
                      - .5 * ((jump.conj().T @ jump) @ state
                              + state @ (jump.conj().T @ jump))) for jump in jumps)
    liouvillian[:, col] = derivative.reshape(16)
eigenvalues, eigenvectors = np.linalg.eigh(liouvillian)
check("independent_generator_negative_semidefinite", eigenvalues.max() <= 1e-14)
check("independent_generator_has_eight_fixed_and_eight_decaying_modes",
      np.count_nonzero(np.abs(eigenvalues) < 1e-14) == 8
      and np.count_nonzero(np.abs(eigenvalues + gamma) < 1e-14) == 8)
sample = report["sample"]
rho = np.array(sample["initial_real"]) + 1j * np.array(sample["initial_imag"])
runtime_state = np.array(sample["evolved_real"]) + 1j * np.array(sample["evolved_imag"])
oracle_operator = (eigenvectors * np.exp(eigenvalues / gamma)) @ eigenvectors.conj().T
oracle_state = (oracle_operator @ rho.reshape(16)).reshape(4, 4)
oracle_residual = float(np.linalg.norm(runtime_state - oracle_state))
check("runtime_state_matches_independent_lindblad_exponential", oracle_residual < 1e-12)
check("oracle_state_trace_one", abs(np.trace(oracle_state) - 1.) < 1e-12)
check("oracle_state_positive", np.linalg.eigvalsh(oracle_state).min() >= -1e-12)
dephased = c_plus @ rho @ c_plus + c_minus @ rho @ c_minus
check("single_complete_recognition_already_idempotent",
      np.linalg.norm(c_plus @ dephased @ c_plus + c_minus @ dephased @ c_minus - dephased) == 0.)

for name in per_theorem:
    missing = copy.deepcopy(parts)
    del missing["external_ladder"]["per_theorem"][name]
    check("missing_kernel_evidence_fails_closed:" + name,
          modified(1, missing)["all_verified"] is False)
check("empty_kernel_evidence_does_not_gain_a_seal", modified(1, {})["all_verified"] is False)
for value in (True, False, 0, -1, float("nan"), float("inf"), "1", None):
    refused = False
    try:
        modified(value, parts)
    except ValueError:
        refused = True
    check("invalid_unit_refused:" + repr(value), refused)

mutations = [
    ("growth_instead_of_decay", ("math.exp(-gamma * time)", "math.exp(gamma * time)")),
    ("identity_misread_as_pinching",
     ("lambda state: c_plus @ state @ c_plus + c_minus @ state @ c_minus", "lambda state: state")),
    ("wrong_generator_sign", ("generator = -gamma * difference(rho_t)", "generator = gamma * difference(rho_t)")),
    ("unselected_state_misreported_as_selected",
     ("selected_transport = c_minus @ quarter_turn @ c_plus", "selected_transport = quarter_turn")),
]
for name, replacement in mutations:
    mutant, _ = load_consumer(new_tree, replacement)
    refused = False
    try:
        refused = mutant(1, parts)["all_verified"] is False
    except (ValueError, ZeroDivisionError, OverflowError):
        refused = True
    check("adulterated_law_refused:" + name, refused)

# Preserve the kernel literals, caller, all gate readers and all other functions.
def other_nodes(tree):
    return [ast.dump(n, include_attributes=False) for n in tree.body
            if not (isinstance(n, ast.FunctionDef) and n.name == "prove_decision_commutation")]
check("all_other_program_nodes_unchanged", other_nodes(old_tree) == other_nodes(new_tree))
compile(new_bytes, str(ROOT / "um.py"), "exec")
check("complete_program_compiles_without_executing", True)
result = {"timestamp": datetime.now().astimezone().isoformat(),
          "status": "SCOPED_RUNTIME_AND_ADVERSARIAL_TESTS_PASSED",
          "tests_passed": len(cases), "cases": cases,
          "python": sys.executable, "numpy_version": np.__version__,
          "source_sha256": hashlib.sha256(new_bytes).hexdigest(),
          "unchanged_kernel_source_hashes": source_hashes,
          "proof_manifest_sha256": hashlib.sha256((ROOT / "tgl_kernel_proof_manifest.json").read_bytes()).hexdigest(),
          "proof_status": "Previously recorded axioms and matching embedded source; no fresh Lean compilation",
          "oracle_residual": oracle_residual, "program_imported": False,
          "full_program_run": False, "canonical_modified": False,
          "new_top_level_functions": 0, "gate_readers_unchanged": True}
for name, payload in [("TEST_RESULTS.json", result), ("RESULTADO_MOTOR_RECONHECIMENTO.json", after)]:
    path = ROOT / name
    if path.exists():
        raise FileExistsError(path)
    data = (json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(data)
    assert temp.read_bytes() == data
    os.replace(temp, path)
print(json.dumps({"status": result["status"], "tests_passed": len(cases),
                  "oracle_residual": oracle_residual, "output": str(ROOT / "RESULTADO_MOTOR_RECONHECIMENTO.json")}))
