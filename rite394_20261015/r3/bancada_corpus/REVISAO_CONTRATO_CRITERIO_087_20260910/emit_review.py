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
ROOT = BASE / "CONTRATO_CRITERIO_ANOMALIAS_087_20260910"
SOURCE = ROOT / "CRITERIO_074_GRUPOS_EXATOS_E_MAPA_085_086.md"
MANIFEST = ROOT / "MANIFESTO_CONTRATO_CRITERIO_087.json"
REPORT = OUT / "PARECER_CINCO_CONDICOES_E_LIMITE_Q2_087.md"
RECEIPT = OUT / "REGISTRO_REVISAO_CONTRATO_CRITERIO_087.json"
assert not REPORT.exists() and not RECEIPT.exists()
author = json.loads(MANIFEST.read_bytes())
keys = ["criterion", "normal", "frame", "admissible"]
rows = [author["note"], *[author["sources_before"][k] for k in keys]]
paths = [Path(row["path"]) for row in rows] + [MANIFEST]
assert all(p.is_relative_to(BASE) for p in paths)

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

def check(name, ok, detail):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})

for row in rows:
    current = pin(Path(row["path"]))
    check("selected_author_pin_matches", current["bytes"] == row["bytes"] and current["sha256"] == row["sha256"], row["path"])

payload = OUT / "REVIEW.payload.md"
source_pin = pin(SOURCE)
text = payload.read_bytes().decode("utf-8").replace("{{BYTES}}", str(source_pin["bytes"])).replace("{{SHA}}", source_pin["sha256"])
links = sorted(set(re.findall(r"\]\(<(C:/[^>]+)>\)", text)))
link_records = []
for link in links:
    match = re.match(r"^(.*?)(?::([0-9]+))?$", link)
    path = Path(match.group(1))
    line = int(match.group(2)) if match.group(2) else None
    exists = path.is_file()
    count = len(path.read_bytes().decode("utf-8").splitlines()) if exists else 0
    ok = exists and (line is None or 1 <= line <= count)
    check("local_link_and_line_valid", ok, link)
    link_records.append({"link": link, "exists": exists, "line": line, "line_count": count})
assert all(c["pass"] for c in checks), checks
publish(REPORT, text.encode("utf-8"))
after = [pin(p) for p in paths]
for a, b in zip(before, after):
    check("reviewed_source_unchanged", a == b, a["path"])
check("report_matches_prepared_bytes", REPORT.read_bytes() == text.encode("utf-8"), str(REPORT))
failed = [c for c in checks if not c["pass"]]
receipt = {
    "status": "PASS_DOCUMENTARY" if not failed else "FAIL_DOCUMENTARY",
    "mathematical_review": "FAVORABLE_NO_MATERIAL_ERROR_IDENTIFIED_IN_SPECIFIED_PARTIAL_SCOPE",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "reviewer": "/root/selected_geometry_design",
    "source": source_pin,
    "report": pin(REPORT),
    "scope": "Audit087 confronted with criterion074 section6, normal-translation074 including metric-frame correction, and admissibility-Q2 contract072. Five sufficient conditions and two spectral gradings; H4 nonzero not automatically contradictory.",
    "read_full_documents": [str(p) for p in paths if p.suffix == ".md"],
    "not_reaudited": ["Full primary causal literature", "Ordinary cohomology071/073", "Descent/off-shell application075", "First-page085 and full antecedent086 theory", "N1 author-owned087 source", "Actual quantum anomaly/QME"],
    "before": before,
    "after": after,
    "links": link_records,
    "checks_passed": sum(c["pass"] for c in checks),
    "checks_total": len(checks),
    "failed_checks": failed,
    "checks": checks,
    "helper": pin(Path(__file__).resolve()),
    "payload": pin(payload),
    "execution_counts": {"mathematical": 0, "CAS": 0, "Lean": 0, "um_execution_or_import": 0, "canonical_recapture": 0},
    "discovery_limitation": "Initial broad rg encountered access-denied package folders unrelated to the target; exact paths of required files were then read successfully. No exhaustive filesystem audit claimed.",
}
publish(RECEIPT, (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"status": receipt["status"], "checks_passed": receipt["checks_passed"], "checks_total": receipt["checks_total"], "files_unchanged": len(before), "report": pin(REPORT), "receipt": pin(RECEIPT)}, ensure_ascii=False, indent=2))
