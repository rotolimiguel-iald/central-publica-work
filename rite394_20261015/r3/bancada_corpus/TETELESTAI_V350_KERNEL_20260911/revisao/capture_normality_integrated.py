"""Read-only inspection of author integration; um.py is parsed as data, never executed."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "normality_latest_run.txt").read_text(encoding="utf-8"))
MANIFEST = json.loads((RUN / "manifest.json").read_bytes())
DEST = RUN / ("final_integrated_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
DEST.mkdir()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write(p, raw):
    assert p.resolve().is_relative_to(REVIEW) and not p.exists()
    p.parent.mkdir(parents=True, exist_ok=True)
    temp = p.with_name(p.name + ".tmp")
    temp.write_bytes(raw)
    assert temp.read_bytes() == raw and temp.stat().st_size == len(raw)
    temp.replace(p)

def save(p, data):
    write(p, json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

def embedded_and_rest(raw):
    tree = ast.parse(raw)
    assignments = [n for n in tree.body if isinstance(n, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in n.targets)]
    assert len(assignments) == 1
    node = assignments[0]
    embedded = ast.literal_eval(node.value)
    tree.body.remove(node)
    return embedded, ast.dump(tree, include_attributes=False)

for name in ["integrated_compile.json", "integration.json", "gate_tests.json", "gate_extension.py",
             "compile_integrated.py", "compile_lean.py", "test_gate_extension.py", "integrate_v350.py"]:
    write(DEST / name, (ROOT / name).read_bytes())
build = json.loads((DEST / "integrated_compile.json").read_bytes())
gate = json.loads((DEST / "gate_tests.json").read_bytes())
integration = json.loads((DEST / "integration.json").read_bytes())
records = []
for row in build["records"]:
    source = Path(row["source"])
    relative = source.relative_to(ROOT / "kernel")
    raw = source.read_bytes()
    binary = ROOT / "build" / relative.with_suffix(".olean")
    records.append({"file": relative.as_posix(), "returncode": row["returncode"],
                    "source_sha256": sha(raw), "source_hash_matches": sha(raw) == row["sha256"],
                    "binary_sha256": sha(binary.read_bytes()), "binary_hash_matches": sha(binary.read_bytes()) == row.get("output_sha256"),
                    "timestamp": row.get("timestamp")})
    write(DEST / "sources" / relative, raw)
    for stream in ["stdout", "stderr"]:
        path = Path(row[stream])
        write(DEST / "logs" / path.name, path.read_bytes())
audit_row = next(r for r in build["records"] if Path(r["source"]).as_posix().endswith("TGL/Audit.lean"))
audit = Path(audit_row["stdout"]).read_text(encoding="utf-8")
axioms = {n: [a.strip() for a in body.split(",") if a.strip()] for n, body in
          re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", audit, re.S)}
for name in re.findall(r"'([\w.']+)' does not depend on any axioms", audit):
    axioms.setdefault(name, [])
raw = (ROOT / "um.py").read_bytes()
embedded, rest = embedded_and_rest(raw)

previous = Path(MANIFEST["previous_run"])
baselines = [json.loads(p.read_bytes()) for p in previous.glob("final_integrated_*/verification.json")]
baseline = next(b for b in baselines if b["integrated_modules"] == 18)
before_path = next(p for p in sorted(ROOT.glob("um.py.bak_*"), reverse=True)
                   if sha(p.read_bytes()) == baseline["um_sha256"])
before_embedded, before_rest = embedded_and_rest(before_path.read_bytes())
old_records = {r["file"]: r for r in baseline["records"]}
new_names = ["L2Order", "RegularNormality", "CoreContractCounterexample"]
source_matches = {}
for name in new_names:
    rel = "TGLExt/V350" + name + ".lean"
    dev_row = MANIFEST["sources"]["TGLV350/" + name + ".lean"]
    dev = Path(dev_row["snapshot"]).read_bytes()
    integrated = (ROOT / "kernel" / rel).read_bytes()
    source_matches[name] = {"dev_sha256": sha(dev), "integrated_sha256": sha(integrated),
        "dev_still_frozen": sha(Path(dev_row["path"]).read_bytes()) == dev_row["sha256"],
        "same_except_import_paths": integrated.decode("utf-8") == dev.decode("utf-8").replace("import TGLV350.", "import TGLExt.V350"),
        "embedded_matches": embedded[rel].encode("utf-8") == integrated}
gate_before = Path(baseline["path"]) / "gate_extension.py"
summary = {"mode": "INDEPENDENT_SOURCE_LOG_AND_BINARY_HASH_INSPECTION__NO_INDEPENDENT_ROOT_REBUILD",
    "path": str(DEST), "records": records, "integrated_modules": len(records),
    "exact_expected_file_set": {r["file"] for r in records} == set(integration["added_kernel_files"] + integration["updated_kernel_files"]),
    "all_exit_zero": all(r["returncode"] == 0 for r in records),
    "all_hashes_match": all(r["source_hash_matches"] and r["binary_hash_matches"] for r in records),
    "audit_distinct": len(axioms), "audit_unexpected_axioms": {k: v for k, v in axioms.items() if not set(v) <= {"propext", "Classical.choice", "Quot.sound"}},
    "gate_checks_count": len(gate["checks"]), "gate_checks_all_passed": all(c["passed"] for c in gate["checks"]),
    "um_sha256": sha(raw), "um_matches_gate_report": sha(raw) == gate["working_um_sha256"],
    "um_matches_integration_report": sha(raw) == integration["working_sha256"], "embedded_files": len(embedded),
    "source_matches": source_matches, "previous_layer": baseline["path"], "previous_um_backup": str(before_path),
    "previous_um_sha256": sha(before_path.read_bytes()),
    "python_ast_outside_embedded_unchanged": rest == before_rest,
    "gate_extension_byte_identical_to_18": gate_before.read_bytes() == (ROOT / "gate_extension.py").read_bytes(),
    "added_embedded_files": sorted(set(embedded) - set(before_embedded)),
    "removed_embedded_files": sorted(set(before_embedded) - set(embedded)),
    "changed_old_embedded_files": sorted(n for n in before_embedded if n in embedded and before_embedded[n] != embedded[n]),
    "countermodel_references": sorted(n for n, t in embedded.items() if any(x in t for x in
         ["zeroTraceLegacyCore", "legacy_contract_accepts_zero_trace", "zeroTraceLegacyCore_has_no_threeLocks"])),
    "redundant_prototype_references": sorted(n for n, t in embedded.items() if "OperatorOrderLimits" in n or "OperatorOrderLimits" in t),
    "reused_same_binary_and_source_as_18": sorted(r["file"] for r in records if r["file"] in old_records and
         r["source_sha256"] == old_records[r["file"]]["source_sha256"] and r["binary_sha256"] == old_records[r["file"]]["binary_sha256"]),
    "new_compilations_relative_to_18": sorted(r["file"] for r in records if r["file"] not in old_records or
         r["binary_sha256"] != old_records[r["file"]]["binary_sha256"]),
    "previous_reviews_preserved": all(sha(Path(p).read_bytes()) == h for p, h in MANIFEST["previous_reviews"].items())}
save(DEST / "verification.json", summary)
save(DEST / "axioms.json", axioms)
print(json.dumps({k: v for k, v in summary.items() if k != "records"}, ensure_ascii=False))
