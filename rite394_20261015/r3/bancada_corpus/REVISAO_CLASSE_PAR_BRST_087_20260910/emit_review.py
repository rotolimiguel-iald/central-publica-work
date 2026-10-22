from pathlib import Path
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).resolve().parent
BASE = OUT.parent
assert BASE == Path(r"C:\IALD\Central de Patentes\Chatgpt")
ROOT = BASE / "CLASSE_PAR_BRST_COMPLETA_087_20260910"
SOURCE = ROOT / "CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md"
AUTHOR_MANIFEST = ROOT / "MANIFESTO_CLASSE_PAR_BRST_087.json"
REPORT = OUT / "PARECER_CLASSE_PAR_E_BRST_CLASSICO_COMPLETO_087.md"
RECEIPT = OUT / "REGISTRO_REVISAO_CLASSE_PAR_087.json"
assert not REPORT.exists() and not RECEIPT.exists()

def pin(path):
    path = Path(path)
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

author = json.loads(AUTHOR_MANIFEST.read_bytes())
listed = [author["note"], *author["sources"]]
paths = [Path(row["path"]) for row in listed]
extra = BASE / "REVISAO_SIMBOLO_DIVERGENCIA_086_20260910_064135_2856684/PARECER_ESTRITEZA_E_DIVERGENCIA_086.md"
paths.extend([AUTHOR_MANIFEST, extra])
paths = list(dict.fromkeys(paths))
assert all(p.is_relative_to(BASE) for p in paths)
before = [pin(p) for p in paths]
checks = []

def check(name, condition, detail):
    checks.append({"name": name, "pass": bool(condition), "detail": detail})

for row in listed:
    actual = pin(row["path"])
    check("author_pin_matches_bytes", actual["bytes"] == row["bytes"] and actual["sha256"] == row["sha256"], row["path"])
source_pin = pin(SOURCE)
payload = OUT / "REVIEW.payload.md"
text = payload.read_bytes().decode("utf-8").replace("{{SOURCE_BYTES}}", str(source_pin["bytes"])).replace("{{SOURCE_SHA}}", source_pin["sha256"])
links = sorted(set(re.findall(r"\]\(<(C:/[^>]+)>\)", text)))
for link in links:
    check("review_local_link_exists", Path(link).is_file(), link)
assert all(c["pass"] for c in checks), checks
publish(REPORT, text.encode("utf-8"))
after = [pin(p) for p in paths]
for a, b in zip(before, after):
    check("source_unchanged", a == b, a["path"])
check("report_published_as_prepared", REPORT.read_bytes() == text.encode("utf-8"), str(REPORT))
failed = [c for c in checks if not c["pass"]]
receipt = {
    "status": "PASS_DOCUMENTARY" if not failed else "FAIL_DOCUMENTARY",
    "mathematical_review": "FAVORABLE_NO_MATERIAL_ERROR_IDENTIFIED_IN_COMPOSITION_SCOPE",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "reviewer": "/root/selected_geometry_design",
    "scope": "Independent review of root087 composition: classical full BV-BRST density cycle, E6, connecting-map image, free line detected at C6 and formal projections, explicit Pontryagin primitive. N2 specific independent review remains distinct.",
    "source": source_pin,
    "report": pin(REPORT),
    "before": before,
    "after": after,
    "mathematical_reads_this_review": [str(SOURCE), str(BASE / "COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md"), str(BASE / "TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md"), str(BASE / "REVISAO_TRANSGRESSAO_BRST_076_20260910/PARECER_TRANSGRESSAO_TOTAL_E_GHOST4.md"), str(BASE / "SOBREVIVENTE_PONTRYAGIN_077_20260910/PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md"), str(BASE / "REVISOES_RAIZ_077_20260910/PARECER_PONTRYAGIN_E_C5_077.md"), str(BASE / "TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md")],
    "other_measured_antecedents": "Other manifest entries are custody checks and/or previously consumed antecedents; not asserted as fresh independent mathematical re-reviews.",
    "local_links": links,
    "helper": pin(Path(__file__).resolve()),
    "payload": pin(payload),
    "execution_counts": {"mathematical": 0, "CAS": 0, "Lean": 0, "um_execution_or_import": 0, "canonical_recapture": 0},
    "checks_passed": sum(c["pass"] for c in checks),
    "checks_total": len(checks),
    "failed_checks": failed,
    "checks": checks,
    "additive_precision": "s complete is the CLASSICAL BV-BRST differential with all valences, not a renormalized quantum BRST operator.",
    "limitations": ["No independent approval of reviewer-authored086 proof", "N2 input review is distinct", "No full H4 classification", "No inverse-limit interchange or Mittag-Leffler assumption", "No causal admissibility, quantum anomaly, QME, UV or physical closure asserted"],
}
publish(RECEIPT, (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"status": receipt["status"], "checks_passed": receipt["checks_passed"], "checks_total": receipt["checks_total"], "files_unchanged": len(before), "report": pin(REPORT), "receipt": pin(RECEIPT)}, ensure_ascii=False, indent=2))
