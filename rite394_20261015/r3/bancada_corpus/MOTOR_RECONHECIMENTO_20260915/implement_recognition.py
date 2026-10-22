"""Patch only the existing runtime consumer; preserve every other source byte."""
from pathlib import Path
from datetime import datetime
import ast
import difflib
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "um_ORIGINAL_SNAPSHOT.py"
TARGET = ROOT / "um.py"
STAMP = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S_%f")


def write_checked(path, data):
    if path.exists():
        raise FileExistsError(path)
    temp = path.with_name(path.name + ".tmp_" + STAMP)
    with temp.open("xb") as stream:
        stream.write(data)
    assert temp.read_bytes() == data
    os.replace(temp, path)
    assert path.read_bytes() == data


raw = SOURCE.read_bytes()
text = raw.decode("utf-8-sig")
tree = ast.parse(text)
node = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
            and n.name == "prove_decision_commutation")
lines = text.splitlines(keepends=True)
old = "".join(lines[node.lineno - 1:node.end_lineno])
newline = "\r\n" if "\r\n" in old else "\n"
new = old.replace("\r\n", "\n").replace(
    "    beta = SEALED_CODATA_ALPHA * ONE * math.sqrt(math.e)   # jamais literal\n",
    "    # Recognition is a pinching predicate, not arithmetic equality as a dynamics.\n"
    "    # The finite gradient law is conditional on L = Gamma * (E - id).\n"
    "    if type(ONE) not in (int, float) or not math.isfinite(ONE) or ONE != 1:\n"
    "        raise ValueError(\"Recognition requires the numerical unit ONE=1\")\n"
    "    beta = SEALED_CODATA_ALPHA * ONE * math.sqrt(math.e)   # jamais literal\n",
)
block = '''    # 2026-09-15: link recognition to the EXISTING decision/gradient consumer.
    # This is a finite runtime realization, not an additional Lean theorem.
    # E^2=E fixes the recognized subspace; L=Gamma*(E-id) is a named time-law input.
    # The reference scales below are test units, not measured physical parameters.
    tau_reference = 1.0
    omega_reference = 1.0
    gamma = 0.5 * beta * tau_reference * omega_reference ** 2
    if not math.isfinite(gamma) or gamma <= 0.0:
        raise ValueError("Recognition reference rate must be finite and positive")
    c_plus = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)
    c_minus = np.eye(4, dtype=complex) - c_plus
    recognize = lambda state: c_plus @ state @ c_plus + c_minus @ state @ c_minus
    difference = lambda state: state - recognize(state)
    recognize_flow = lambda state, time: (recognize(state)
        + math.exp(-gamma * time) * difference(state))
    psi = np.array([1.0, 1.0j, 1.0, -1.0j], dtype=complex) / 2.0
    rho = np.outer(psi, psi.conj())
    rho_fixed = recognize(rho)
    rho_difference = difference(rho)
    time_reference = 1.0 / gamma
    rho_t = recognize_flow(rho, time_reference)
    generator = -gamma * difference(rho_t)
    # Separate jump-operator evaluation of the generator (GKSL).
    lindblad = np.zeros_like(rho_t)
    for projector in (c_plus, c_minus):
        jump = math.sqrt(gamma) * projector
        jump_square = jump.conj().T @ jump
        lindblad += (jump @ rho_t @ jump.conj().T
                     - 0.5 * (jump_square @ rho_t + rho_t @ jump_square))
    recognition_residuals = {
        "idempotence": float(np.linalg.norm(recognize(rho_fixed) - rho_fixed)),
        "complement_idempotence": float(np.linalg.norm(difference(rho_difference) - rho_difference)),
        "hs_orthogonality": float(abs(np.vdot(rho_fixed, rho_difference))),
        "fixed_sector": float(np.linalg.norm(recognize_flow(rho_fixed, time_reference) - rho_fixed)),
        "lindblad_generator_scaled": float(np.linalg.norm(lindblad - generator) / gamma),
        "semigroup": float(np.linalg.norm(
            recognize_flow(rho, 0.9 / gamma)
            - recognize_flow(recognize_flow(rho, 0.2 / gamma), 0.7 / gamma))),
    }
    phi_initial = 0.5 * float(np.vdot(rho_difference, rho_difference).real)
    delta_t = difference(rho_t)
    phi_t = 0.5 * float(np.vdot(delta_t, delta_t).real)
    phi_dot = float(np.vdot(delta_t, generator).real)
    recognition_residuals["lyapunov_scaled"] = abs(phi_dot + 2.0 * gamma * phi_t) / gamma
    recognition_residuals["phi_exponential"] = abs(phi_t - math.exp(-2.0) * phi_initial)
    step = 1e-4 / gamma
    finite_derivative = (recognize_flow(rho, time_reference + step)
                         - recognize_flow(rho, time_reference - step)) / (2.0 * step)
    recognition_residuals["ode_finite_difference_scaled"] = float(
        np.linalg.norm(finite_derivative - generator) / gamma)
    matrix_samples = [recognize_flow(rho, exposure / gamma)
                      for exposure in (0.0, 0.25, 1.0, 3.0)]
    recognition_residuals["trace"] = max(float(abs(np.trace(state) - 1.0))
                                          for state in matrix_samples)
    minimum_eigenvalue = min(float(np.linalg.eigvalsh(state).min())
                            for state in matrix_samples)
    # Keep the FULL state for dephasing. The selected output is a control.
    identity2 = np.eye(2, dtype=complex)
    zero2 = np.zeros((2, 2), dtype=complex)
    quarter_turn = np.block([[zero2, identity2], [-identity2, zero2]])
    selected_transport = c_minus @ quarter_turn @ c_plus
    rho_selected = selected_transport @ rho @ selected_transport.conj().T
    selection_probability = float(np.trace(rho_selected).real)
    if not math.isfinite(selection_probability) or selection_probability <= 0.0:
        raise ValueError("Selected recognition control has zero or invalid probability")
    rho_selected /= selection_probability
    selected_difference = float(np.linalg.norm(difference(rho_selected)))
    selected_flow_change = float(np.linalg.norm(
        recognize_flow(rho_selected, time_reference) - rho_selected))
    recognition_residuals["selected_difference"] = selected_difference
    recognition_residuals["selected_flow_change"] = selected_flow_change
    # Uniform-sign subtraction is NOT this channel: it changes the trace.
    wrong_trace_change = float(abs(np.trace(rho - gamma * c_minus) - 1.0))
    recognition_ok = bool(
        all(math.isfinite(value) for value in recognition_residuals.values())
        and all(value < (1e-7 if key == "ode_finite_difference_scaled" else 1e-12)
                for key, value in recognition_residuals.items())
        and math.isfinite(minimum_eigenvalue) and minimum_eigenvalue >= -1e-12
        and phi_initial > 1e-3 and 0.0 < phi_t < phi_initial and phi_dot < 0.0
        and 0.0 < selection_probability <= 1.0
        and wrong_trace_change > gamma
    )
    recognition_dynamics = {
        "status": ("FINITE_RECOGNITION_DYNAMICS_VERIFIED__POSTSELECTED_STATE_FIXED"
                   if recognition_ok else "RECOGNITION_DYNAMICS_FAILED"),
        "all_verified": recognition_ok,
        "law": "E(rho)=sum C_a rho C_a; Q=id-E; L=-Gamma Q; T_t=E+exp(-Gamma*t)Q",
        "time_law_status": "INPUT: homogeneous scalar relaxation on the complement; not implied by E^2=E alone",
        "logical_reading_status": "ONTO: recognized means E(rho)=rho; coherence is not arithmetic 1=0",
        "metric_status": "Finite Hilbert-Schmidt metric; not a spacetime metric",
        "kernel_status": "Existing DecisionCommutation/Ergodicity results reused; this runtime specialization is not a new kernel theorem",
        "rate": {"beta": beta, "gamma_reference": gamma,
                 "tau_reference": tau_reference, "omega_reference": omega_reference,
                 "status": "REFERENCE_UNITS_ONLY_NOT_A_PHYSICAL_PREDICTION"},
        "phi_initial": phi_initial, "phi_at_reference_time": phi_t,
        "phi_derivative": phi_dot, "residuals": recognition_residuals,
        "minimum_eigenvalue": minimum_eigenvalue,
        "selection_probability": selection_probability,
        "selected_state_is_fixed": bool(selected_difference < 1e-12 and selected_flow_change < 1e-12),
        "effective_dephasing_on_full_state": bool(phi_t < phi_initial),
        "effective_dephasing_after_selection": bool(selected_flow_change >= 1e-12),
        "wrong_subtraction_trace_change": wrong_trace_change,
        "sample": {"initial_real": rho.real.tolist(), "initial_imag": rho.imag.tolist(),
                   "evolved_real": rho_t.real.tolist(), "evolved_imag": rho_t.imag.tolist()},
        "does_not_gate_core": True,
    }
'''
anchor = "    checks = [\n"
assert new.count(anchor) == 1
new = new.replace(anchor, block + anchor)
needle = '        ("GKLS genuino = fluxo gradiente da entropia relativa'
assert new.count(needle) == 1
new = new.replace(needle,
    '        ("[DERIVED/RUNTIME] reconhecimento E, complemento Q e lei L=-Gamma Q: semigrupo, GKSL, traco e gradiente Hilbert-Schmidt", recognition_ok),\n'
    '        ("[CONTROLE] o estado selecionado C_- V rho V* C_- ja e reconhecido: dephasing posterior zero", recognition_dynamics["selected_state_is_fixed"]),\n'
    + needle)
needle = '        "checks": checks, "all_verified": all_v,\n'
assert new.count(needle) == 1
new = new.replace(needle, '        "recognition_dephasing": recognition_dynamics,\n' + needle)
assert new != old
ast.parse(new)
new = new.replace("\n", newline)
patched_text = "".join(lines[:node.lineno - 1]) + new + "".join(lines[node.end_lineno:])
patched = patched_text.encode("utf-8-sig" if raw.startswith(b"\xef\xbb\xbf") else "utf-8")
assert raw == text.encode("utf-8-sig" if raw.startswith(b"\xef\xbb\xbf") else "utf-8")
modified_tree = ast.parse(patched)
before_nodes = [ast.dump(n, include_attributes=False) for n in tree.body
                if not (isinstance(n, ast.FunctionDef) and n.name == node.name)]
after_nodes = [ast.dump(n, include_attributes=False) for n in modified_tree.body
               if not (isinstance(n, ast.FunctionDef) and n.name == node.name)]
assert before_nodes == after_nodes
assert len([n for n in tree.body if isinstance(n, ast.FunctionDef)]) == len(
    [n for n in modified_tree.body if isinstance(n, ast.FunctionDef)])
write_checked(TARGET, patched)
write_checked(ROOT / "recognition_in_existing_consumer.diff", "".join(difflib.unified_diff(
    old.splitlines(keepends=True), new.splitlines(keepends=True),
    fromfile="um.py:prove_decision_commutation:before",
    tofile="um.py:prove_decision_commutation:after")).encode("utf-8"))
receipt = {"timestamp": STAMP, "source": str(SOURCE), "target": str(TARGET),
           "source_sha256": hashlib.sha256(raw).hexdigest(),
           "target_sha256": hashlib.sha256(patched).hexdigest(),
           "modified_top_level_functions": [node.name],
           "new_top_level_functions": 0, "all_other_ast_nodes_unchanged": True,
           "embedded_kernel_unchanged": True, "gate_functions_unchanged": True,
           "original_line": node.lineno, "source_original_modified": False}
write_checked(ROOT / "IMPLEMENTATION_RECEIPT.json", (json.dumps(receipt, indent=2) + "\n").encode())
print(json.dumps(receipt))
