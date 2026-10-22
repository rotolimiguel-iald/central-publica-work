"""Documentary custody only. No mathematical, Lean, or um execution."""
from pathlib import Path
import hashlib
import json
import re
import sys
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
SOURCE_DIR = ROOT / "SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910"
NOTE_SOURCE = SOURCE_DIR / "ESTRITEZA_E_DETECTOR_PRINCIPAL_DE_DIVERGENCIA.md"
MAN_SOURCE = SOURCE_DIR / "MANIFESTO_SIMBOLO_DIVERGENCIA_086.json"

def pin(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}

def publish(path, data):
    path = Path(path)
    pending = path.with_name(path.name + ".pending")
    if path.exists() or pending.exists():
        raise FileExistsError(str(path))
    if not data:
        raise ValueError("Empty output")
    with pending.open("xb") as stream:
        stream.write(data)
    if pending.read_bytes() != data:
        raise ValueError("Written bytes differ")
    pending.rename(path)
    if path.read_bytes() != data:
        raise ValueError("Final bytes differ")

def publish_json(path, value):
    publish(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

manifest = json.loads(MAN_SOURCE.read_bytes().decode("utf-8-sig"))
paths = [NOTE_SOURCE, MAN_SOURCE] + [Path(p["path"]) for p in manifest["sources_before"]]
capture_path = BASE / "PINS_ANTES_REVISAO_086.json"
if sys.argv[1] == "capture":
    publish_json(capture_path, {"utc": datetime.now(timezone.utc).isoformat(),
                 "sources_before": [pin(p) for p in paths],
                 "helper": pin(__file__)})
    print(json.dumps({"capture": pin(capture_path), "source_count": len(paths)}))
elif sys.argv[1] == "finish":
    old = json.loads(capture_path.read_bytes().decode("utf-8"))
    current = [pin(p) for p in paths]
    checks = []
    for before, after in zip(old["sources_before"], current, strict=True):
        checks.append({"kind": "source_unchanged", "path": before["path"],
                       "passed": before == after})
    for expected in [manifest["note"]] + manifest["sources_before"] + manifest["sources_after"]:
        checks.append({"kind": "recorded_pin_matches_current", "path": expected["path"],
                       "passed": pin(expected["path"]) == expected})
    checks.append({"kind": "source_manifest_count_consistent", "passed":
                   manifest["checks_total"] == len(manifest["checks"]) and
                   manifest["checks_passed"] == sum(c["passed"] for c in manifest["checks"])})
    checks.append({"kind": "source_manifest_no_math_execution", "passed":
                   manifest["new_algebraic_executions"] == 0 and manifest["new_lean_runs"] == 0 and
                   not manifest["um_executed_or_imported"]})
    draft = BASE / "PARECER_ESTRITEZA_E_DIVERGENCIA_086.md.pending_text"
    note = BASE / "PARECER_ESTRITEZA_E_DIVERGENCIA_086.md"
    raw = draft.read_bytes()
    content = raw.decode("utf-8")
    links = sorted(set(re.findall(r"\]\(<(C:/[^>]+)>\)", content)))
    for item in links:
        clean = re.sub(r":\d+$", "", item)
        checks.append({"kind": "review_local_link_exists", "path": clean,
                       "passed": Path(clean).is_file()})
    checks.append({"kind": "helper_unchanged", "passed": old["helper"] == pin(__file__)})
    checks.append({"kind": "review_utf8_nonempty", "passed": len(raw) > 10000 and "\x00" not in content})
    failures = [c for c in checks if not c["passed"]]
    if failures:
        print(json.dumps({"failed": failures}, ensure_ascii=False))
        raise SystemExit(2)
    if note.exists():
        raise FileExistsError(str(note))
    draft.rename(note)
    if note.read_bytes() != raw:
        raise ValueError("Final note bytes differ")
    receipt = {"created_utc": datetime.now(timezone.utc).isoformat(),
        "author": "/root/finish_gibbs_realization",
        "status": "INDEPENDENT_WRITTEN_REVIEW_NO_MATERIAL_ERROR_IDENTIFIED_WITHIN_STATED_SCOPE",
        "review": pin(note), "capture": pin(capture_path), "helper": pin(__file__),
        "sources_before": old["sources_before"], "sources_after": current,
        "all_sources_unchanged": old["sources_before"] == current,
        "checks": checks, "checks_total": len(checks),
        "checks_passed": sum(c["passed"] for c in checks), "failed_checks": failures,
        "check_type": "Documentary custody and links only; written mathematics is not counted as executed checks.",
        "primary_sources_read": [
            {"url": "https://arxiv.org/pdf/1805.03751", "scope": "Section3.1, Killing/Calabi flat compatibility; no curved Weyl freeness imported."},
            {"url": "https://arxiv.org/pdf/math-ph/0202019", "scope": "Equations2.1-2.4 and2.6-2.7, flat massless spinor jets only."}],
        "new_mathematical_executions": 0, "new_cas_runs": 0, "new_lean_runs": 0,
        "um_executed_or_imported": False, "existing_files_modified": False,
        "limits": ["Finite quadratic gauge-invariant Weyl/EOM currents on a fixed oriented four-dimensional space form.",
                   "No tensor spectators; scalar inert coefficient extension of fixed real operator.",
                   "Does not assert surjectivity or freeness of the curved Weyl tower.",
                   "CE/lifting consequence uses separately established084/085/080 contracts.",
                   "No physical anomaly calculation, QME, UV, or whole-theory verdict."]}
    receipt_path = BASE / "RECIBO_REVISAO_SIMBOLO_086.json"
    publish_json(receipt_path, receipt)
    print(json.dumps({"review": pin(note), "receipt": pin(receipt_path),
                      "checks": len(checks), "passed": len(checks), "sources": len(paths)}, ensure_ascii=False))
else:
    raise ValueError("Expected capture or finish")
