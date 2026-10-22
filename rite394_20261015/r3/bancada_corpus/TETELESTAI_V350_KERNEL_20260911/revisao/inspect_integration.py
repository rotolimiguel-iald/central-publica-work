"""Inspect ASTs as data and exercise only the standalone gate extension."""
from pathlib import Path
import ast
import copy
import datetime
import hashlib
import json
import re

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "latest_run.txt").read_text(encoding="utf-8"))
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write(path, raw):
    assert path.resolve().is_relative_to(REVIEW)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        previous = path.read_bytes()
        backup = path.with_name(path.name + ".bak_" + STAMP)
        backup.write_bytes(previous)
        assert backup.read_bytes() == previous
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(raw)
    assert temporary.read_bytes() == raw and temporary.stat().st_size == len(raw)
    temporary.replace(path)

manifest = json.loads((RUN / "manifest.json").read_bytes())
raw = (ROOT / "um.py").read_bytes()
tree = ast.parse(raw)
original = ast.parse((ROOT / "fontes/um_v350_original.py").read_bytes())
embedded = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign)
    and any(isinstance(k, ast.Name) and k.id == "_EMBEDDED_KERNEL_FILES" for k in n.targets)).value)
ext_raw = (RUN / "integration/gate_extension.py").read_bytes()
ext_tree = ast.parse(ext_raw)
names = {n.name for n in ext_tree.body if isinstance(n, ast.FunctionDef)} | {"_V350_MODULAR_CONTRACTS"}
def extract(t):
    return [n for n in t.body if (isinstance(n, ast.FunctionDef) and n.name in names)
            or (isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id in names for x in n.targets))]
def function(t, name):
    return next(n for n in t.body if isinstance(n, ast.FunctionDef) and n.name == name)
def canonical(n):
    return ast.dump(n, include_attributes=False)
static = {
    "um_read_mode": "AST_ONLY__NOT_EXECUTED_OR_IMPORTED",
    "um_sha256": sha(raw),
    "gate_extension_ast_identical": [canonical(n) for n in extract(ext_tree)] == [canonical(n) for n in extract(tree)],
    "legacy_evaluator_ast_unchanged": canonical(function(tree,"evaluate_quantum_gravity_closure")) == canonical(function(original,"evaluate_quantum_gravity_closure")),
    "final_return": ast.unparse(function(tree,"verify_tgl_kernel_formalization").body[-1]),
    "frontier_assignment": [ast.unparse(n) for n in ast.walk(function(tree,"prove_qg_closure_gate"))
                            if isinstance(n,ast.Assign) and "evaluate_v350_kernel_frontier" in ast.unparse(n)],
}
regular = ["L2OperatorLift","L2Translation","L2StrongContinuity","RegularTowerRepresentation","RegularGeneratedAlgebra"]
comparisons = []
for name in regular:
    source = RUN / "sources/TGLV350" / (name + ".lean")
    expected = source.read_text(encoding="utf-8")
    for dependency in regular:
        expected = expected.replace("import TGLV350." + dependency, "import TGLExt.V350" + dependency)
    relative = "TGLExt/V350" + name + ".lean"
    integrated = (ROOT / "kernel" / relative).read_bytes()
    write(RUN / "integrated_sources" / relative, integrated)
    comparisons.append({"file": relative, "sha256": sha(integrated),
                        "same_except_import_paths": integrated.decode("utf-8") == expected,
                        "embedded_matches_file": embedded[relative] == integrated.decode("utf-8")})
for relative in manifest["modules"]:
    if relative.startswith("TGLExt/"):
        frozen = (RUN / "sources" / relative).read_bytes()
        comparisons.append({"file": relative, "sha256": sha(frozen),
                            "embedded_matches_file": embedded[relative] == frozen.decode("utf-8")})
static["integrated_source_comparison"] = comparisons

# No monolithic AST is executed. This standalone extension has only a constant and pure functions.
assert all(isinstance(n, (ast.Expr, ast.Assign, ast.FunctionDef)) for n in ext_tree.body)
assert not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(ext_tree))
namespace = {}
exec(compile(ext_tree, str(RUN / "integration/gate_extension.py"), "exec"), namespace)
contracts = namespace["_V350_MODULAR_CONTRACTS"]
checks = []
def check(name, value):
    checks.append({"name": name, "passed": bool(value)})
def status(kernel):
    return namespace["verify_v350_modular_provenance"](kernel)
axioms = {name: ["propext", "Classical.choice", "Quot.sound"] for pair in contracts.values() for name in pair}
# Explicit synthetic input is a control of Python decisions, not evidence of a Lean theorem.
good = {"lake_build_ok": False, "incremental_build_ok": True, "dependency_hashes_verified": True,
        "changed_source_hashes_verified": True, "audit_returncode": 0, "all_verified": True,
        "axiom_report": axioms}
check("synthetic_complete_evidence_accepted", all(status(good).values()))
check("empty_input_rejected", not any(status({}).values()))
for key in ["incremental_build_ok", "dependency_hashes_verified", "changed_source_hashes_verified", "all_verified", "audit_returncode"]:
    candidate = copy.deepcopy(good)
    candidate.pop(key)
    check("missing_" + key, not any(status(candidate).values()))
for flag, pair in contracts.items():
    for name in pair:
        candidate = copy.deepcopy(good)
        candidate["axiom_report"].pop(name)
        check("missing_" + name, not status(candidate)[flag])
    for bad in [["sorryAx"], ["Lean.trustCompiler"], ["Foreign.hidden"], "propext", None, 0]:
        candidate = copy.deepcopy(good)
        candidate["axiom_report"][pair[1]] = bad
        check("rejected_axioms_" + flag + "_" + str(bad), not status(candidate)[flag])
for rc in [1, -1, None]:
    candidate = copy.deepcopy(good)
    candidate["audit_returncode"] = rc
    check("audit_failure_" + str(rc), not any(status(candidate).values()))
candidate = copy.deepcopy(good)
candidate["gpf_H1_internal_susy_relative_gap_discharged"] = True
check("unsupported_gravity_flag_rejected", not namespace["v350_gravity_flags_have_proof"](candidate))
candidate = copy.deepcopy(good)
candidate.update({"qgf_continuous_modular_realization_constructed": False, "qgf_full_TGL_witness_constructed": False})
namespace["finalize_v350_modular_frontier"](candidate)
check("later_flags_stay_false", candidate["qgf_continuous_modular_realization_constructed"] is False and candidate["qgf_full_TGL_witness_constructed"] is False)
frontier = namespace["evaluate_v350_kernel_frontier"](candidate)
check("scope_only_duality", frontier["scope"] == "PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT" and frontier["full_plan_complete"] is False and frontier["legacy_gate_changed"] is False)

log_evidence = []
for relative in manifest["modules"]:
    source_sha = sha((RUN / "sources" / relative).read_bytes())
    binary = ROOT / "build" / Path(relative).with_suffix(".olean")
    binary_sha = sha(binary.read_bytes()) if binary.is_file() else None
    matches = []
    for p in sorted((ROOT / "logs").glob(Path(relative).stem + "_*.json")):
        row = json.loads(p.read_bytes())
        if row.get("sha256") == source_sha and row.get("returncode") == 0 and row.get("output_sha256") == binary_sha:
            matches.append((p, row))
    if matches:
        p, row = matches[-1]
        write(RUN / "author_logs" / p.name, p.read_bytes())
        for key in ["stdout", "stderr"]:
            logpath = Path(row[key])
            write(RUN / "author_logs" / logpath.name, logpath.read_bytes())
        log_evidence.append({"module": relative, "matching_source_and_binary_log": str(p), "source_sha256": source_sha, "binary_sha256": binary_sha})
    else:
        log_evidence.append({"module": relative, "matching_source_and_binary_log": None})

out = {"timestamp": STAMP, "static": static, "gate_controls_input": "SYNTHETIC__NOT_PROOF_EVIDENCE",
       "gate_checks": checks, "gate_passed": sum(c["passed"] for c in checks), "gate_total": len(checks),
       "author_logs": log_evidence}
write(RUN / "integration_inspection.json", json.dumps(out, indent=2, ensure_ascii=False).encode("utf-8"))
print(json.dumps({"static": {k:v for k,v in static.items() if k != "integrated_source_comparison"},
                  "all_integrated_sources_match": all(c["embedded_matches_file"] and c.get("same_except_import_paths", True) for c in comparisons),
                  "gate_passed": out["gate_passed"], "gate_total": len(checks), "matching_author_logs": sum(x["matching_source_and_binary_log"] is not None for x in log_evidence)}, ensure_ascii=False))
