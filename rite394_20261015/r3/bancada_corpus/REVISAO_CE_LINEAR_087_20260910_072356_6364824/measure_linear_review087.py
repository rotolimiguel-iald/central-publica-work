"""Read-only custody of mathematical sources; new review publication only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys

BASE = Path(__file__).resolve().parent
SRC = BASE.parent / "CE_LINEAR_WEYL_TODOS_GRAUS_087_20260910"
SOURCE = SRC / "ACICLICIDADE_CE_LINEAR_E_PRIMEIRO_DIFERENCIAL.md"
MANIFEST = SRC / "MANIFESTO_CE_LINEAR_087.json"
origin = json.loads(MANIFEST.read_bytes().decode("utf-8-sig"))
paths = [SOURCE, MANIFEST] + [Path(x["path"]) for x in origin["before"] + origin["helpers"]]

def pin(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def recorded_matches(x):
    actual = pin(x["path"])
    return actual["bytes"] == x["bytes"] and actual["sha256"] == x["sha256"]

def publish_json(path, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temp = path.with_name(path.name + ".pending")
    if temp.exists() or path.exists():
        raise FileExistsError(str(path))
    with temp.open("xb") as stream:
        stream.write(raw)
    if temp.read_bytes() != raw:
        raise ValueError("Temporary mismatch")
    temp.rename(path)
    if path.read_bytes() != raw:
        raise ValueError("Final mismatch")

capture = BASE / "PINS_ANTES_REVISAO_N1_087.json"
if sys.argv[1] == "capture":
    publish_json(capture, {"utc": datetime.now(timezone.utc).isoformat(),
                          "sources_before": [pin(p) for p in paths], "helper": pin(__file__)})
    print(json.dumps({"capture": pin(capture), "sources": len(paths)}))
elif sys.argv[1] == "finish":
    before = json.loads(capture.read_bytes().decode("utf-8"))
    after = [pin(p) for p in paths]
    checks = [{"kind": "source_unchanged", "path": a["path"], "passed": a == b}
              for a, b in zip(before["sources_before"], after, strict=True)]
    for x in [origin["source"]] + origin["before"] + origin["after"] + origin["helpers"]:
        checks.append({"kind": "recorded_pin_matches", "path": Path(x["path"]).resolve().as_posix(),
                       "passed": recorded_matches(x)})
    checks.append({"kind": "origin_counts_consistent", "passed":
                   origin["checks_total"] == len(origin["checks"]) and
                   origin["checks_passed"] == sum(x["pass"] for x in origin["checks"])})
    checks.append({"kind": "origin_zero_execution", "passed": all(v == 0 for v in origin["execution_counts"].values())})
    checks.append({"kind": "helper_unchanged", "passed": before["helper"] == pin(__file__)})
    draft = BASE / "PARECER_ACICLICIDADE_LINEAR_E_D1_087.md.pending_text"
    note = BASE / "PARECER_ACICLICIDADE_LINEAR_E_D1_087.md"
    raw = draft.read_bytes()
    content = raw.decode("utf-8")
    checks.append({"kind": "review_utf8_nonempty", "passed": len(raw) > 8000 and "\x00" not in content and not note.exists()})
    for link in sorted(set(re.findall(r"\]\(<(C:/[^>]+)>\)", content))):
        clean = re.sub(r":\d+$", "", link)
        checks.append({"kind": "review_local_link", "path": clean, "passed": Path(clean).is_file()})
    failed = [x for x in checks if not x["passed"]]
    if failed:
        print(json.dumps({"failed": failed}, ensure_ascii=False))
        raise SystemExit(2)
    draft.rename(note)
    if note.read_bytes() != raw:
        raise ValueError("Published note differs")
    record = {"utc": datetime.now(timezone.utc).isoformat(), "author": "/root/finish_gibbs_realization",
              "status": "INDEPENDENT_WRITTEN_REVIEW_NO_MATERIAL_ERROR_IDENTIFIED_WITHIN_SCOPE",
              "review": pin(note), "helper": pin(__file__), "capture": pin(capture),
              "sources_before": before["sources_before"], "sources_after": after,
              "all_sources_unchanged": before["sources_before"] == after,
              "checks": checks, "checks_total": len(checks), "checks_passed": len(checks), "failed_checks": [],
              "check_type": "Documentary custody only; written mathematics is not an executed test.",
              "primary_sources_read": [{"url": "https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/chev-eilen.pdf",
                 "scope": "Section23, finite-dimensional coefficient definition; Theorem24.1 and algebraic proof, printed pages115-119."}],
              "new_mathematical_executions": 0, "new_cas_runs": 0, "new_lean_runs": 0,
              "um_executed_or_imported": False, "existing_files_modified": False,
              "limits": ["Review of new N1 argument, not a new independent approval of self-authored antecedent review086.",
                         "No use of reviewer's N2 computation as proof of N1.",
                         "Fixed scalar-inert finite-jet category; no g-local finiteness assumed.",
                         "CE and induced d1 acyclicity only, not zero cochains, H(s0), full BRST, QME or UV."]}
    result = BASE / "RECIBO_REVISAO_CE_LINEAR_087.json"
    publish_json(result, record)
    print(json.dumps({"review": pin(note), "receipt": pin(result), "checks": len(checks), "sources": len(paths)}, ensure_ascii=False))
else:
    raise ValueError("Expected capture or finish")
