"""Documentary pins and publication only; no mathematical program execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
SOURCES = [
    "SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/ESTRITEZA_E_DETECTOR_PRINCIPAL_DE_DIVERGENCIA.md",
    "SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/MANIFESTO_SIMBOLO_DIVERGENCIA_086.json",
    "REVISAO_SIMBOLO_DIVERGENCIA_086_20260910_064135_2856684/PARECER_ESTRITEZA_E_DIVERGENCIA_086.md",
    "CORRENTES_WEYL_UMA_DERIVADA_086_20260910/CLASSIFICACAO_CORRENTES_W_NABLA_W_E_DIVERGENCIA.md",
    "REVISAO_CORRENTES_UMA_DERIVADA_086_20260910_065540_575112/PARECER_CLASSIFICACAO_E_NORMALIZACAO_086.md",
    "COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md",
    "REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md",
    "COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md",
    "COROLARIOS_CE_E_LIDER_CUBICO_086_20260910/COHOMOLOGIA_CE3_E_IMAGEM_CUBICA_ZERO_APOS_C6.md",
]

def pin(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def write_json_new(path, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    tmp = path.with_name(path.name + ".pending")
    if path.exists() or tmp.exists():
        raise FileExistsError(str(path))
    with tmp.open("xb") as stream:
        stream.write(raw)
    if tmp.read_bytes() != raw:
        raise ValueError("Temporary bytes differ")
    tmp.rename(path)
    if path.read_bytes() != raw:
        raise ValueError("Final bytes differ")

capture = BASE / "PINS_ANTES_RELATIVO_087.json"
if sys.argv[1] == "capture":
    write_json_new(capture, {"utc": datetime.now(timezone.utc).isoformat(),
                            "sources_before": [pin(ROOT / s) for s in SOURCES], "helper": pin(__file__)})
    print(json.dumps({"capture": pin(capture), "sources": len(SOURCES)}))
elif sys.argv[1] == "finish":
    before = json.loads(capture.read_bytes().decode("utf-8"))
    after = [pin(ROOT / s) for s in SOURCES]
    checks = [{"kind": "source_unchanged", "path": a["path"], "passed": a == b}
              for a, b in zip(before["sources_before"], after, strict=True)]
    checks.append({"kind": "helper_unchanged", "passed": before["helper"] == pin(__file__)})
    frozen_manifest = json.loads((ROOT / SOURCES[1]).read_bytes().decode("utf-8-sig"))
    checks.append({"kind": "antecedent_note_matches_frozen_pin", "passed": pin(ROOT / SOURCES[0]) == frozen_manifest["note"]})
    draft = BASE / "GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md.pending_text"
    note = BASE / "GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md"
    raw = draft.read_bytes()
    content = raw.decode("utf-8")
    checks.append({"kind": "note_nonempty_utf8", "passed": len(raw) > 15000 and "\x00" not in content and not note.exists()})
    for link in sorted(set(re.findall(r"\]\(<(C:/[^>]+)>\)", content))):
        target = re.sub(r":\d+$", "", link)
        checks.append({"kind": "local_link_exists", "path": target, "passed": Path(target).is_file()})
    failures = [c for c in checks if not c["passed"]]
    if failures:
        print(json.dumps({"failed": failures}, ensure_ascii=False))
        raise SystemExit(2)
    draft.rename(note)
    if note.read_bytes() != raw:
        raise ValueError("Final note differs")
    value = {"utc": datetime.now(timezone.utc).isoformat(), "author": "/root/finish_gibbs_realization",
             "status": "NEW_WRITTEN_DERIVATION_PENDING_INDEPENDENT_REVIEW_EXCLUDED_FROM086",
             "note": pin(note), "capture": pin(capture), "helper": pin(__file__),
             "sources_before": before["sources_before"], "sources_after": after,
             "all_sources_unchanged": before["sources_before"] == after,
             "checks": checks, "checks_total": len(checks), "checks_passed": len(checks), "failed_checks": [],
             "check_type": "Documentary only; no mathematical identities counted as executed checks.",
             "primary_sources_read": [
                 {"url": "https://arxiv.org/pdf/hep-th/9505173", "scope": "Section7.2 decomposition and AppendixB isotropy Lie algebra cohomology only; no nonlinear maximum-degree theorem imported."},
                 {"url": "https://arxiv.org/pdf/math-ph/0202019", "scope": "Flat massless spinor jets, equations2.1-2.7, as antecedent086; no curved freeness assumed."},
                 {"url": "https://arxiv.org/pdf/1805.03751", "scope": "Flat/constant-curvature Calabi compatibility as antecedent086."}],
             "new_mathematical_executions": 0, "new_cas_runs": 0, "new_lean_runs": 0,
             "um_executed_or_imported": False, "existing_files_modified": False,
             "domain": "Fixed oriented four-dimensional Lorentzian space form, constant sigma projected to metric sector, fixed nonzero real K and kappa, scalar-inert real algebra extension, finite jets algebraically.",
             "results_proposed_for_review": ["Curved scalar and one-form generators with finite triangular lifts.",
                 "No natural quadratic effective two-forms.", "Relative cohomology only in degree4, free rank2.",
                 "Isotropy-invariant full Killing CE cohomology free ranks2,4,2 in degrees4,7,10 and zero otherwise."],
             "limits": ["Not full BRST cohomology or all higher differentials.", "No completed infinite-jet coefficient algebra.",
                        "No tensor spectators, varying backgrounds, QME, physical anomaly coefficient, or UV result.",
                        "Limited structural feedback is not represented as full independent review."]}
    manifest = BASE / "MANIFESTO_RELATIVO_CE_087.json"
    write_json_new(manifest, value)
    print(json.dumps({"note": pin(note), "manifest": pin(manifest), "checks": len(checks)}, ensure_ascii=False))
else:
    raise ValueError("Expected capture or finish")
