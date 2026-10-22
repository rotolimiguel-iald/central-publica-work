"""Read a coherent snapshot of selected canonical evidence, without importing um.py."""
import ast
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
CANON = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
BASE83 = ROOT / "COPIA_INTEGRADA_20260909_192248_937671" / "um.py"
PLAN83 = ROOT / "INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394" / "BUILD_SUCCESSOR_20260909_192313_320129" / "BUILD_PLAN.json"
pins = {}

def read(path):
    raw = path.read_bytes()
    pins[str(path)] = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    return raw

def table(raw):
    tree = ast.parse(raw.decode("utf-8-sig"))
    found = [n for n in tree.body if isinstance(n, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in n.targets)]
    assert len(found) == 1
    result = ast.literal_eval(found[0].value)
    assert isinstance(result, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in result.items())
    return result

def from_import(text):
    lines = text.replace("\r\n", "\n").splitlines(keepends=True)
    first = next(i for i, s in enumerate(lines) if s.startswith("import "))
    return "".join(lines[first:])

raw = read(CANON / "um.py")
source = raw.decode("utf-8-sig")
canonical = table(raw)
bench = table(read(BASE83))
plan = json.loads(read(PLAN83))
seal = json.loads(read(CANON / "um_absoluto_selo.json"))
manifest = json.loads(read(CANON / "tgl_kernel_proof_manifest.json"))
run = read(CANON / "rodada_v338_stdout.txt").decode("utf-8-sig")
modules = [{"module": m["module"], "key": m["key"], "present": m["key"] in canonical,
            "body_from_first_import_identical": m["key"] in canonical and
             from_import(canonical[m["key"]]) == from_import(bench[m["key"]])}
           for m in plan["modules"]]
captures = []
for kind in ("build", "audit"):
    path = CANON / f"tgl_kernel_{kind}_capture.txt"
    capture = read(path).decode("utf-8").replace("\r\n", "\n")
    head, sep, body = capture.partition("--- STDOUT ---\n")
    assert sep
    stdout, sep, stderr = body.rpartition("\n--- STDERR ---\n")
    assert sep and stderr.endswith("\n")
    stderr = stderr[:-1]
    lengths = re.search(r"# len\(stdout\)=(\d+) len\(stderr\)=(\d+)", head)
    assert lengths and len(stdout) == int(lengths[1]) and len(stderr) == int(lengths[2])
    actual = hashlib.sha256(stdout.encode()).hexdigest()
    captures.append({"kind": kind, "returncode": int(re.search(r"# returncode: (-?\d+)", head)[1]),
                     "stdout_characters": len(stdout), "stdout_sha256": actual,
                     "manifest_stdout_sha256": manifest[f"{kind}_stdout_sha256"],
                     "matches_manifest": actual == manifest[f"{kind}_stdout_sha256"],
                     "warning_lines": len(re.findall(r"^warning:", stdout, re.M))})
keys = ["timestamp", "formal_source_hash", "qg_closure_verdict", "renormalization_wall_verdict",
        "linearized_spin2_sector_proved", "dephasing_reach_verdict", "fail_closed_selftest",
        "rite_checkpoints", "collapse_definition"]
result = {
    "status": "READ_ONLY_SNAPSHOT_COMPLETED__NO_NEW_CANONICAL_EXECUTION",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "canonical_files": len(canonical), "baseline83_files": len(bench),
    "baseline83_modules": modules,
    "baseline_modules_in_canonical": sum(m["present"] for m in modules),
    "baseline_bodies_identical": sum(m["body_from_first_import_identical"] for m in modules),
    "missing_from_canonical": [m["module"] for m in modules if not m["present"]],
    "seal_excerpt": {k: seal[k] for k in keys if k in seal},
    "seal_um_hash_matches": seal["sha256"]["um.py"] == pins[str(CANON / "um.py")]["sha256"],
    "seal_proof_manifest_hash_matches": seal["sha256"]["tgl_kernel_proof_manifest.json"] == pins[str(CANON / "tgl_kernel_proof_manifest.json")]["sha256"],
    "recorded_run_lines": [{"line": i, "text": line} for i, line in enumerate(run.splitlines(), 1)
        if any(word in line for word in ("teoremas limpos:", "FAIL_CLOSED_SELFTEST_PASSED", "rite_checkpoints:", "exit=", "anomalias", "renormal"))],
    "source_v338_markers": [{"line": i, "text": line[:350]} for i, line in enumerate(source.splitlines(), 1)
        if "v338" in line][:12],
    "capture_correspondence": captures,
    "interpretation": "Source presence, recorded execution and capture correspondence are separate claims. A hash mismatch is a provenance discrepancy, not itself a failed theorem. Cached nature rites are not new data runs.",
    "source_pins": pins,
    "um_executed_or_imported_here": False,
    "originals_written": False,
}
for path, pin in pins.items():
    data = Path(path).read_bytes()
    assert len(data) == pin["bytes"] and hashlib.sha256(data).hexdigest() == pin["sha256"], path
result["all_read_sources_unchanged_at_end"] = True
target = OUT / "RECEIPT_V338.json"
assert target.resolve().is_relative_to(ROOT) and not target.exists()
data = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
tmp = target.with_suffix(".json.tmp_" + datetime.now().strftime("%H%M%S_%f"))
with tmp.open("xb") as handle:
    handle.write(data)
    handle.flush()
    os.fsync(handle.fileno())
assert tmp.read_bytes() == data and data
tmp.rename(target)
assert target.read_bytes() == data
print(json.dumps({k: result[k] for k in ("status", "canonical_files", "baseline_modules_in_canonical", "baseline_bodies_identical", "missing_from_canonical", "seal_um_hash_matches", "seal_proof_manifest_hash_matches", "capture_correspondence", "recorded_run_lines")}, ensure_ascii=False))
