from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

BASE = Path(__file__).resolve().parent

def pin(path):
    data = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

before = json.loads((BASE / "PINS_INICIAIS.json").read_text(encoding="utf-8"))
after = []
for expected in before:
    actual = pin(Path(expected["path"]))
    actual["unchanged"] = actual["bytes"] == expected["bytes"] and actual["sha256"] == expected["sha256"]
    if not actual["unchanged"]:
        raise RuntimeError(f"Changed source: {expected['path']}")
    after.append(actual)
verification = json.loads((BASE / "VERIFICACAO_DOCUMENTAL_078.json").read_text(encoding="utf-8"))
if not all(c["passed"] is True for c in verification["checks"]):
    raise RuntimeError("Failed documentary check")
artifacts = ["PARECER_RELATORIO_078.md", "VERIFICACAO_DOCUMENTAL_078.json", "PINS_INICIAIS.json", "check_documents_078.py", Path(__file__).name]
receipt = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "author": "/root/finish_gibbs_realization",
    "status": "PASS_INDEPENDENT_DOCUMENTARY_REVIEW_WITH_STATED_SOURCE_LIMITS",
    "source_pins_after": after,
    "new_artifacts": [pin(BASE / name) for name in artifacts],
    "documentary_checks": len(verification["checks"]),
    "documentary_checks_passed": sum(c["passed"] is True for c in verification["checks"]),
    "links_checked": verification["links_total"],
    "line_anchors_checked": verification["line_anchors"],
    "cas_assertions_recorded_elsewhere": sum(verification["recorded_cas_counts"]),
    "cas_executions_in_this_review": 0,
    "lean_compilations_in_this_review": 0,
    "canonical_recaptures_in_this_review": 0,
    "um_executed_or_imported": False,
    "originals_written": False,
    "stage079_included": False,
    "semantic_scope": [
        "Obstruction concerns the specific H3(C5) class, not every class with the same leader",
        "Four coefficient rings belong to an auxiliary tower and have no assumed comparison to Einstein-sigma",
        "Power note consumed with fiber-domain and induction addendum",
        "Preserved .pending draft is historical and not the approved mathematical text",
        "122 CAS records, 119 documentary checks and zero Lean are distinct evidence counts",
        "Capture/helper provenance and four stored canonical pins agree with delivery077"
    ]
}
destination = BASE / "RECIBO_REVISAO_RELATORIO_078.json"
temp = destination.with_name(destination.name + ".pending")
if destination.exists():
    raise RuntimeError("Existing receipt")
data = json.dumps(receipt, ensure_ascii=False, indent=2).encode("utf-8")
with temp.open("xb") as stream:
    stream.write(data)
if not data or temp.read_bytes() != data:
    raise RuntimeError("Staging mismatch")
temp.rename(destination)
if destination.read_bytes() != data:
    raise RuntimeError("Final mismatch")
print(json.dumps({"note": pin(BASE / "PARECER_RELATORIO_078.md"), "receipt": pin(destination), "source_count": len(after), "checks": receipt["documentary_checks"], "links": receipt["links_checked"]}, ensure_ascii=False))
