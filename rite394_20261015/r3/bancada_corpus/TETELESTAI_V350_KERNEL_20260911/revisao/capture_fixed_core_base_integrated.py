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
RUN = Path((REVIEW / "fixed_core_base_latest_run.txt").read_text(encoding="utf-8"))
MANIFEST = json.loads((RUN / "manifest.json").read_bytes())
FIRST=Path(MANIFEST["previous_run"])
FIRST_M=json.loads((FIRST/"manifest.json").read_bytes())
MANIFEST["sources"]={**FIRST_M["sources"],**MANIFEST["sources"]}
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
             "compile_integrated.py", "compile_lean.py", "test_gate_extension.py", "integrate_v350.py", "kernel_incremental_evidence.json", "MINUTA_BASE_FIXA.md", "record_fixed_base_progress.py"]:
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

# Prior custodied bounded-values integration is the baseline.
previous = Path((REVIEW / "constant_fibre_identification_latest_run.txt").read_text(encoding="utf-8"))
oldcap = max(p for p in previous.glob("final_integrated_*") if (p / "verification.json").exists())
baseline = json.loads((oldcap / "verification.json").read_bytes())
before_path = next(p for p in sorted(ROOT.glob("um.py.bak_*"), reverse=True)
                   if sha(p.read_bytes()) == baseline["um_sha256"])
before_embedded, before_rest = embedded_and_rest(before_path.read_bytes())
old_records = {r["file"]: r for r in baseline["records"]}
new_names = ["StrongOperatorField", "OperatorFieldFaithfulness", "TwistedCommutantField", "RegularCoreCommutant", "FixedCoreBaseIdentification"]
source_matches = {}
for name in new_names:
    rel = "TGLExt/V350" + name + ".lean"
    dev_row = MANIFEST["sources"]["TGLV350/" + name + ".lean"]
    dev = Path(dev_row["snapshot"]).read_bytes()
    integrated = (ROOT / "kernel" / rel).read_bytes()
    source_matches[name] = {"dev_sha256": sha(dev), "integrated_sha256": sha(integrated),
        "dev_still_frozen": sha(Path(dev_row["path"]).read_bytes()) == dev_row["sha256"],
        "same_except_import_paths": integrated.decode("utf-8") == dev.decode("utf-8").replace("import TGLV350.", "import TGLExt.V350"),
        "same_after_import_rewrite_and_EOL_normalization": integrated.decode("utf-8").replace("\r\n","\n") == dev.decode("utf-8").replace("\r\n","\n").replace("import TGLV350.", "import TGLExt.V350"),
        "dev_CRLF":dev.count(b"\r\n"),"integrated_CRLF":integrated.count(b"\r\n"),
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
    "gate_extension_byte_identical_to_70": gate_before.read_bytes() == (ROOT / "gate_extension.py").read_bytes(),
    "added_embedded_files": sorted(set(embedded) - set(before_embedded)),
    "removed_embedded_files": sorted(set(before_embedded) - set(embedded)),
    "changed_old_embedded_files": sorted(n for n in before_embedded if n in embedded and before_embedded[n] != embedded[n]),
    "countermodel_references": sorted(n for n, t in embedded.items() if any(x in t for x in
         ["zeroTraceLegacyCore", "legacy_contract_accepts_zero_trace", "zeroTraceLegacyCore_has_no_threeLocks"])),
    "redundant_prototype_references": sorted(n for n, t in embedded.items() if "OperatorOrderLimits" in n or "OperatorOrderLimits" in t),
    "reused_same_binary_and_source_as_70": sorted(r["file"] for r in records if r["file"] in old_records and
         r["source_sha256"] == old_records[r["file"]]["source_sha256"] and r["binary_sha256"] == old_records[r["file"]]["binary_sha256"]),
    "new_compilations_relative_to_70": sorted(r["file"] for r in records if r["file"] not in old_records or
         r["binary_sha256"] != old_records[r["file"]]["binary_sha256"]),
    "previous_reviews_preserved": all(sha(Path(p).read_bytes()) == h for p, h in MANIFEST["previous_reviews"].items() if Path(p).name != "REVIEW_FIXED_CORE_BASE.md")}
evidence=json.loads((DEST/"kernel_incremental_evidence.json").read_bytes())
flags=("qgf_continuous_modular_realization_constructed","qgf_unconditional_continuous_corner_proved","qgf_full_TGL_witness_constructed","gpf_H1_internal_susy_relative_gap_discharged","gpf_H2_smooth_modular_four_frame_discharged","gpf_H3_local_horizon_equilibrium_discharged")
summary["six_flags"]={f:evidence[f] for f in flags}
summary["full_monolithic_runtime_run"]=gate["full_monolithic_runtime_run"]
summary["legacy_gate_changed"]=gate["frontier"]["legacy_gate_changed"]
summary["full_plan_complete"]=gate["frontier"]["full_plan_complete"]
summary["new_targets_axioms"]={n:axioms.get(n) for n in MANIFEST["declarations"]}
summary["evidence_axioms_equal_log"]=evidence["axiom_report"]==axioms
summary["artifact_sha256"]={p.name:sha(p.read_bytes()) for p in DEST.iterdir() if p.is_file()}
summary["recorder_ast_parse_ok"]=isinstance(ast.parse((DEST/"record_fixed_base_progress.py").read_bytes()),ast.Module)
save(DEST / "verification.json", summary)
save(DEST / "axioms.json", axioms)
print(json.dumps({k: v for k, v in summary.items() if k != "records"}, ensure_ascii=False))
