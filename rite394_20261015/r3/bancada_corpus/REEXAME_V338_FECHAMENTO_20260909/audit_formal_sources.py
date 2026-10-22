"""Verify the recorded formal source set and incorporated declarations, by reading only."""
import ast
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
CANON = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
KERNEL = CANON / "tgl_kernel"
ROOT = OUT.parent.resolve()
PRIOR = ROOT / "INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394" / "BUILD_SUCCESSOR_20260909_192313_320129" / "BUILD_PLAN.json"
pins = {}

def read(p):
    raw = p.read_bytes()
    pins[str(p)] = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    return raw

manifest = json.loads(read(CANON / "tgl_kernel_proof_manifest.json"))
seal = json.loads(read(CANON / "um_absoluto_selo.json"))
plan = json.loads(read(PRIOR))
raw_um = read(CANON / "um.py")
tree = ast.parse(raw_um.decode("utf-8"))
entries = [n for n in tree.body if isinstance(n, ast.Assign) and any(
    isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in n.targets)]
assert len(entries) == 1
embedded = ast.literal_eval(entries[0].value)
rows = []
current_hashes = {}
for rel, expected in manifest["formal_files_sha256"].items():
    p = (KERNEL / rel).resolve()
    assert p.is_relative_to(KERNEL.resolve())
    raw = read(p)
    actual = hashlib.sha256(raw).hexdigest()
    current_hashes[rel] = actual
    rows.append({"path": rel, "manifest_matches": actual == expected,
                 "embedded": rel in embedded,
                 "embedded_bytes_match": rel in embedded and raw == embedded[rel].encode("utf-8")})
aggregate = hashlib.sha256()
for rel in sorted(current_hashes):
    aggregate.update(rel.encode())
    aggregate.update(current_hashes[rel].encode())
declarations = []
allowed = {"propext", "Classical.choice", "Quot.sound"}
for module in plan["modules"]:
    if module["key"] not in embedded:
        continue
    for d in module["declarations"]:
        name = d["name"]
        axioms = manifest["axiom_report"].get(name)
        declarations.append({"name": name, "kind": d["kind"], "recorded": axioms is not None,
                             "axioms": axioms, "allowed_only": axioms is not None and set(axioms) <= allowed})
result = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "RECORDED_SOURCE_CORRESPONDENCE_CHECKED__NO_COMPILATION",
    "formal_files_count": len(rows), "formal_files_match_manifest": sum(r["manifest_matches"] for r in rows),
    "embedded_file_count": len(embedded),
    "embedded_bytes_matching_materialized": sum(r["embedded_bytes_match"] for r in rows),
    "non_embedded_recorded_files": [r["path"] for r in rows if not r["embedded"]],
    "aggregate_matches_manifest": aggregate.hexdigest() == manifest["formal_source_hash"],
    "aggregate_matches_seal": aggregate.hexdigest() == seal["formal_source_hash"],
    "incorporated_declarations": len(declarations),
    "incorporated_theorems": sum(d["kind"] == "theorem" for d in declarations),
    "incorporated_declarations_recorded_allowed": sum(d["allowed_only"] for d in declarations),
    "formal_files": rows, "declarations": declarations, "source_pins": pins,
    "originals_written": False, "um_executed_or_imported": False,
    "scope": "Current bytes compared with already recorded hashes and axiom reports; no fresh Lean execution or claim that imported literature has been formalized.",
}
for path, pin in pins.items():
    raw = Path(path).read_bytes()
    assert len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"], path
result["all_read_sources_unchanged_at_end"] = True
data = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
p = OUT / "RECEIPT_FORMAL_SOURCES_V338.json"
assert not p.exists() and p.resolve().is_relative_to(ROOT)
tmp = p.with_suffix(".json.tmp_" + datetime.now().strftime("%H%M%S_%f"))
with tmp.open("xb") as f:
    f.write(data)
    f.flush()
    os.fsync(f.fileno())
assert tmp.read_bytes() == data and data
tmp.rename(p)
assert p.read_bytes() == data
print(json.dumps({k: v for k, v in result.items() if k not in ("formal_files", "declarations", "source_pins")}, ensure_ascii=False))
