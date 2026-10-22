"""Reproducible delivery audit. Canonical files are read only."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
folder = Path(__file__).resolve().parent
assert folder.parent == Path(r"C:\IALD\Central de Patentes\Chatgpt")
names = ["CollapseContract", "CollapseCostAndAttestation", "TowerCollapseRealization", "QuantumCollapseWitness"]
def record(path):
    raw = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
def save_new(path, raw):
    assert path.parent == folder and not path.exists()
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as handle:
        handle.write(raw); handle.flush(); os.fsync(handle.fileno())
    assert temp.read_bytes() == raw
    os.rename(temp, path)
    assert path.read_bytes() == raw
baseline = json.loads((folder / "BASELINE.json").read_text(encoding="utf-8"))
accepted = []
for path in sorted(folder.glob("BUILD_*/BUILD_RESULT.json")):
    candidate = json.loads(path.read_text(encoding="utf-8"))
    if candidate["status"] == "PASS_COMPILED_SCOPE" and [Path(s["path"]).stem for s in candidate["sources"]] == names:
        accepted.append((path, candidate))
if not accepted:
    raise RuntimeError("No accepted complete build")
build_path, build = accepted[-1]
checks = []
def check(label, condition):
    checks.append({"check": label, "passed": bool(condition)})
for item in build["sources"] + build["external_boundary"]:
    check("artifact_unchanged:" + item["path"], record(Path(item["path"])) == item)
check("standard_axioms_only", all(set(r["axioms"]) <= {"propext", "Classical.choice", "Quot.sound"} for r in build["axiom_rows"]))
check("no_compile_errors_or_warnings", build["status"] == "PASS_COMPILED_SCOPE" and all(r["exit_code"] == 0 for r in build["runs"]))
original = Path(baseline["original"]["path"])
check("original_um_unchanged", record(original) == baseline["original"])
for item in baseline["embedded_source_checks"]:
    now = record(Path(item["path"]))
    check("canonical_source_unchanged:" + item["module"], all(now[k] == item[k] for k in now))
for item in baseline["memory_read_only"]:
    check("memory_unchanged:" + item["path"], record(Path(item["path"])) == item)
raw_um = original.read_bytes()
tree = ast.parse(raw_um.decode("utf-8-sig"))
canonical_names = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
proposal = folder / "collapse_contract_proposal.py"
prototype_tree = ast.parse(proposal.read_text(encoding="utf-8"))
prototype_names = {n.name for n in prototype_tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
python_collisions = sorted(canonical_names & prototype_names)
check("no_python_top_level_name_collision", not python_collisions)
namespace_files = []
kernel = original.parent / "tgl_kernel"
for path in (kernel / "TGLExt").glob("*.lean"):
    if re.search(r"(?m)^namespace\s+ChatgptAudit\.Collapse057\s*$", path.read_text(encoding="utf-8")):
        namespace_files.append(path.as_posix())
check("new_namespace_absent_in_canonical_sources", not namespace_files)
runtime_sources = [record(proposal), record(folder / "check_collapse_contract.py")]
env = os.environ.copy(); env["PYTHONDONTWRITEBYTECODE"] = "1"
command = [sys.executable, "-B", str(folder / "check_collapse_contract.py")]
runtime = subprocess.run(command, cwd=folder, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)
stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
runtime_path = folder / ("RUNTIME_AUDIT_" + stamp + ".json")
save_new(runtime_path, runtime.stdout)
check("runtime_exit_zero", runtime.returncode == 0)
runtime_data = json.loads(runtime.stdout) if runtime.returncode == 0 else {}
check("runtime_exact_checks_passed", runtime_data.get("status") == "PASS_EXACT_CHECKS")
check("only_synthetic_testimony", runtime_data.get("records") == "SYNTHETIC_TEST_FIXTURES_ONLY")
check("runtime_sources_unchanged", runtime_sources == [record(proposal), record(folder / "check_collapse_contract.py")])
counts = []
for name in names:
    text = (folder / (name + ".lean")).read_text(encoding="utf-8")
    declarations = re.findall(r"(?m)^(?:noncomputable\s+)?(def|theorem|structure|abbrev)\s+(\w+)", text)
    prints = re.findall(r"(?m)^#print axioms (\w+)$", text)
    check("axiom_coverage:" + name, set(prints) == {n for _, n in declarations} and len(prints) == len(declarations))
    check("no_forbidden_proof_tokens:" + name, not re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b", text))
    counts.append({"module": name, "theorems": sum(k == "theorem" for k, _ in declarations),
                   "definitions": sum(k != "theorem" for k, _ in declarations), "axiom_rows": len(prints)})
report = {
    "status": "PASS_DELIVERY_SCOPE" if all(c["passed"] for c in checks) else "FAIL_VISIBLE",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "complete_build_result": record(build_path), "module_counts": counts,
    "theorems": sum(c["theorems"] for c in counts), "declarations": sum(c["axiom_rows"] for c in counts),
    "runtime": {"result": record(runtime_path), "command": command, "sources": runtime_sources,
                "checks": runtime_data.get("checks"), "all_records_synthetic": True},
    "original_um": record(original), "canonical_selected_source_count": len(baseline["embedded_source_checks"]),
    "python_collisions": python_collisions, "canonical_namespace_hits": namespace_files,
    "checks": checks,
    "limitations": {
        "independent_review": False, "physical_collapse_proof": False, "born_rule_derived": False,
        "physical_cost_law_derived": False, "external_attestation_received": False,
        "um_modified_or_executed": False, "gravitational_reconstruction_completed": False,
        "all_transitive_dependencies_recompiled": False,
        "canonical_lean_namespace_search": "Exact namespace header search, not a complete Lean environment collision audit.",
    },
}
output = folder / ("AUDITORIA_" + stamp + ".json")
save_new(output, (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"status": report["status"], "report": output.as_posix(),
                  "theorems": report["theorems"], "declarations": report["declarations"],
                  "runtime_checks": report["runtime"]["checks"],
                  "failed_checks": [c["check"] for c in checks if not c["passed"]]}))
sys.exit(0 if report["status"] == "PASS_DELIVERY_SCOPE" else 1)
