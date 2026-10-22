"""Pin and verify the author's completed integrated build, without running it."""
from pathlib import Path
import datetime
import hashlib
import json
import re

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "latest_run.txt").read_text(encoding="utf-8"))
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

for name in ["integrated_compile.json", "integration.json", "gate_tests.json", "gate_extension.py"]:
    write(DEST / name, (ROOT / name).read_bytes())
build = json.loads((DEST / "integrated_compile.json").read_bytes())
gate = json.loads((DEST / "gate_tests.json").read_bytes())
integration = json.loads((DEST / "integration.json").read_bytes())
records = []
for row in build["records"]:
    source = Path(row["source"])
    relative = source.relative_to(ROOT / "kernel")
    source_raw = source.read_bytes()
    binary = ROOT / "build" / relative.with_suffix(".olean")
    records.append({"file": relative.as_posix(), "returncode": row["returncode"],
                    "source_sha256": sha(source_raw), "source_hash_matches": sha(source_raw) == row["sha256"],
                    "binary_sha256": sha(binary.read_bytes()), "binary_hash_matches": sha(binary.read_bytes()) == row.get("output_sha256")})
    write(DEST / "sources" / relative, source_raw)
    for stream in ["stdout", "stderr"]:
        p = Path(row[stream])
        write(DEST / "logs" / p.name, p.read_bytes())
audit = Path(build["records"][-1]["stdout"]).read_text(encoding="utf-8")
axioms = {}
for name, body in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", audit, re.S):
    axioms[name] = [a.strip() for a in body.split(",") if a.strip()]
for name in re.findall(r"'([\w.']+)' does not depend on any axioms", audit):
    axioms.setdefault(name, [])
raw = (ROOT / "um.py").read_bytes()
summary = {"mode": "INDEPENDENT_INSPECTION_AND_HASH_VERIFICATION_OF_AUTHOR_BUILD__NOT_ROOT_RECOMPILATION",
           "path": str(DEST), "records": records, "integrated_modules": len(records),
           "exact_expected_file_set": {r["file"] for r in records} == set(integration["added_kernel_files"] + integration["updated_kernel_files"]),
           "all_exit_zero": all(r["returncode"] == 0 for r in records),
           "all_hashes_match": all(r["source_hash_matches"] and r["binary_hash_matches"] for r in records),
           "audit_distinct": len(axioms), "audit_unexpected_axioms": {k:v for k,v in axioms.items() if not set(v) <= {"propext","Classical.choice","Quot.sound"}},
           "gate_checks_count": len(gate["checks"]), "gate_checks_all_passed": all(c["passed"] for c in gate["checks"]),
           "um_sha256": sha(raw), "um_matches_gate_report": sha(raw) == gate["working_um_sha256"],
           "um_matches_integration_report": sha(raw) == integration["working_sha256"]}
save(DEST / "verification.json", summary)
print(json.dumps({k:v for k,v in summary.items() if k != "records"}, ensure_ascii=False))
