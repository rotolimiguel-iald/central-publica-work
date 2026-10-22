from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).resolve().parent
BASE = OUT.parent
assert BASE == Path(r"C:\IALD\Central de Patentes\Chatgpt")
ROOT = BASE / "REEXAME_SUFICIENCIA_087_20260910"
EMISSION = ROOT / "REGISTRO_EMISSAO_NARRATIVOS_087.json"
SNAP87 = ROOT / "ESTADO_CANONICO_087.json"
SNAP86 = BASE / "REEXAME_SUFICIENCIA_086_20260910/ESTADO_CANONICO_086.json"
REPORT = OUT / "PARECER_DOCUMENTAL_NARRATIVOS_087.md"
RECEIPT = OUT / "REGISTRO_REVISAO_DOCUMENTAL_087.json"
assert not REPORT.exists() and not RECEIPT.exists()
emission = json.loads(EMISSION.read_bytes())
rows = [*emission["outputs"], *emission["sources_before"]]
paths = list(dict.fromkeys([Path(row["path"]) for row in rows] + [EMISSION, SNAP86]))
assert all(p.is_relative_to(BASE) for p in paths), "No canonical files may be opened"

def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def publish(path, data):
    assert path.parent == OUT and not path.exists()
    tmp = path.with_name(path.name + ".tmp_new")
    with tmp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == data
    os.replace(tmp, path)
    assert path.read_bytes() == data

before = [pin(p) for p in paths]
checks = []

def check(name, ok, detail=None):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})

for row in rows:
    actual = pin(Path(row["path"]))
    check("emission_pin_matches", actual["bytes"] == row["bytes"] and actual["sha256"] == row["sha256"], row["path"])
narratives = [Path(row["path"]) for row in emission["outputs"]]
assert len(narratives) == 3
all_links = []
for path in narratives:
    text = path.read_bytes().decode("utf-8")
    all_links.extend(re.findall(r"\]\(<(C:/[^>]+)>\)", text))
unique_links = sorted(set(all_links))
for link in unique_links:
    match = re.match(r"^(.*?)(?::([0-9]+))?$", link)
    target = Path(match.group(1))
    assert target.is_relative_to(BASE), "Narrative local links expected within Chatgpt"
    line = int(match.group(2)) if match.group(2) else None
    exists = target.is_file()
    count = len(target.read_bytes().decode("utf-8").splitlines()) if exists else 0
    check("narrative_link_exists", exists and (line is None or 1 <= line <= count), link)
old = json.loads(SNAP86.read_bytes())
new = json.loads(SNAP87.read_bytes())
for key in ["embedded_files", "modules", "present", "absent", "seal_um_hash_matches", "seal_excerpt"]:
    check("snapshot_metadata_matches_086", old[key] == new[key], key)
def canonical_metadata(snapshot):
    return {row["path"]: {"bytes": row["bytes"], "sha256": row["sha256"]} for row in snapshot["pins"] if "/Artigo/" in row["path"]}
old_pins = canonical_metadata(old)
new_pins = canonical_metadata(new)
check("four_recorded_canonical_pins_equal", len(new_pins) == 4 and new_pins == old_pins, "Metadata comparison only; canonical files not opened")
check("snapshot_counts_recount", len(new["modules"]) == 98 and sum(row["present"] for row in new["modules"]) == 77 and len(new["absent"]) == 21 and new["embedded_files"] == 683)
check("snapshot_comparison_flags", len(new["comparison_with_delivery086"]) == 4 and all(row["unchanged"] for row in new["comparison_with_delivery086"]))
check("emission_zero_math_and_original_writes", all(emission[key] == 0 for key in ["mathematical_executions", "cas_executions", "lean_executions"]) and not emission["um_executed_or_imported"] and not emission["original_files_written"])
assert all(c["pass"] for c in checks), checks
payload = OUT / "REVIEW.payload.md"
review = payload.read_bytes().decode("utf-8").replace("{{LINK_OCCURRENCES}}", str(len(all_links))).replace("{{LINK_UNIQUE}}", str(len(unique_links)))
publish(REPORT, review.encode("utf-8"))
after = [pin(p) for p in paths]
for a, b in zip(before, after):
    check("source_preserved", a == b, a["path"])
check("report_matches_prepared_bytes", REPORT.read_bytes() == review.encode("utf-8"))
failed = [c for c in checks if not c["pass"]]
receipt = {
    "status": "PASS_DOCUMENTARY" if not failed else "FAIL_DOCUMENTARY",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "reviewer": "/root/selected_geometry_design",
    "scope": "Full reading of three narratives087; fidelity to separately reviewed087 results, snapshot087 and prior086 snapshot metadata; no independent mathematical reapproval of own N1.",
    "narratives": [pin(p) for p in narratives],
    "report": pin(REPORT),
    "before": before,
    "after": after,
    "canonical_snapshot": pin(SNAP87),
    "previous_snapshot": pin(SNAP86),
    "canonical_metadata_compared_not_reopened": new_pins,
    "counts": {"documentary_files_preserved": len(paths), "narratives": len(narratives), "source_pin_entries_from_emission": len(emission["sources_before"]), "link_occurrences": len(all_links), "unique_link_targets": len(unique_links), "embedded_files_recorded": new["embedded_files"], "present_modules_recounted": sum(row["present"] for row in new["modules"]), "absent_modules_recorded": len(new["absent"])},
    "checks_passed": sum(c["pass"] for c in checks),
    "checks_total": len(checks),
    "failed_checks": failed,
    "checks": checks,
    "helper": pin(Path(__file__).resolve()),
    "payload": pin(payload),
    "execution_counts": {"mathematical": 0, "CAS": 0, "Lean": 0, "um_execution_or_import": 0, "canonical_recapture": 0},
    "limitations": ["Documentary review, not new theorem verification", "N1 source author consumes independent review, not self-approval", "No audit of future finalizer/config/tunnel/addendum", "Historical083/086/Lean results not counted as fresh executions", "Later087 results and subsequent stages excluded unless already in three narratives"],
}
publish(RECEIPT, (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"status": receipt["status"], "checks_passed": receipt["checks_passed"], "checks_total": receipt["checks_total"], "counts": receipt["counts"], "report": pin(REPORT), "receipt": pin(RECEIPT)}, ensure_ascii=False, indent=2))
