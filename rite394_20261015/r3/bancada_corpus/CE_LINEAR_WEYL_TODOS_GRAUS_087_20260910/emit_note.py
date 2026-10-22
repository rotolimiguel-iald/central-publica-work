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
TARGET = OUT / "ACICLICIDADE_CE_LINEAR_E_PRIMEIRO_DIFERENCIAL.md"
MANIFEST = OUT / "MANIFESTO_CE_LINEAR_087.json"
assert not TARGET.exists() and not MANIFEST.exists()
SOURCES = [
    "SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/ESTRITEZA_E_DETECTOR_PRINCIPAL_DE_DIVERGENCIA.md",
    "SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/MANIFESTO_SIMBOLO_DIVERGENCIA_086.json",
    "REVISAO_SIMBOLO_DIVERGENCIA_086_20260910_064135_2856684/PARECER_ESTRITEZA_E_DIVERGENCIA_086.md",
    "REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md",
    "PRIMEIRA_PAGINA_TODOS_GRAUS_085_20260910/COHOMOLOGIA_S0_GERAL_E_INVARIANTES_POSITIVOS.md",
    "COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md",
    "GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md",
]

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
    assert tmp.read_bytes() == data and len(data) > 0
    os.replace(tmp, path)
    assert path.read_bytes() == data

before = [pin(BASE / p) for p in SOURCES]
payload = OUT / "NOTE.payload.md"
body = payload.read_bytes()
text = body.decode("utf-8")
checks = []

def check(name, condition, detail=None):
    row = {"name": name, "pass": bool(condition)}
    if detail is not None:
        row["detail"] = detail
    checks.append(row)

links = sorted(set(re.findall(r"\]\(<(C:/[^>]+)>\)", text)))
for link in links:
    check("local_link_exists", Path(link).is_file(), link)
check("note_has_all_degrees_and_d1_scope", all(s in text for s in ["para todo inteiro", "E=q+1", "no máximo cinco", "Não se calcula"]), "documentary presence only")
check("new_outputs_only", all(not p.exists() for p in [TARGET, MANIFEST]))
assert all(c["pass"] for c in checks), checks
publish(TARGET, body)
after = [pin(BASE / p) for p in SOURCES]
for a, b in zip(before, after):
    check("source_unchanged", a == b, a["path"])
check("published_bytes_equal_payload", TARGET.read_bytes() == body)
check("no_existing_source_modified", before == after)
failed = [c for c in checks if not c["pass"]]
manifest = {
    "status": "PASS_DOCUMENTARY" if not failed else "FAIL_DOCUMENTARY",
    "mathematical_status": "DERIVED_WRITTEN_PENDING_INDEPENDENT_REVIEW",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "author_agent": "/root/selected_geometry_design",
    "task": "087 linear CE module in all degrees",
    "scope": "Finite jets, fixed oriented Lorentzian 4D space form, K>0 and kappa nonzero real fixed, projected constant sigma, inert Rher. No full BRST or QME conclusion.",
    "result": "Horizontal linear invariant forms vanish in p=0..4; all CE cohomology of N1 vanishes; induced first BRST differential is acyclic in m=E-q=1.",
    "source": pin(TARGET),
    "before": before,
    "after": after,
    "local_links": links,
    "primary_sources": [{"title": "Chevalley and Eilenberg (1948)", "url": "https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/chev-eilen.pdf", "read_scope": "Section23 finite coefficients; Theorem24.1 and its algebraic proof, pages115-119", "local_pdf_pin": None}],
    "helpers": [pin(Path(__file__).resolve()), pin(payload)],
    "execution_counts": {"mathematical": 0, "CAS": 0, "Lean": 0, "um_execution_or_import": 0},
    "checks_total": len(checks),
    "checks_passed": sum(c["pass"] for c in checks),
    "failed_checks": failed,
    "checks": checks,
    "limitations": ["Not an independent approval of antecedent self-authored proofs", "No local finiteness under g assumed", "No freedom of the curved Weyl tower assumed", "No inverse limit or Mittag-Leffler assertion", "No canonical file recapture", "No math execution; checks are documentary"],
}
publish(MANIFEST, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"status": manifest["status"], "checks_passed": manifest["checks_passed"], "checks_total": manifest["checks_total"], "source": pin(TARGET), "manifest": pin(MANIFEST)}, ensure_ascii=False, indent=2))
