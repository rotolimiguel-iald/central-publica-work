"""Publish only three new narrative documents; no delivery finalizer or canonical execution."""
from pathlib import Path
import hashlib
import json
import re
import sys
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
RELATIVE_SOURCES = [
    "REEXAME_SUFICIENCIA_085_20260910/REEXAME_SUFICIENCIA.md",
    "INSPECAO_CANONICO_NAVEGACAO_086_20260910/ESTADO_CANONICO_INSPECAO_086.json",
    "INSPECAO_CANONICO_NAVEGACAO_086_20260910/PARECER_INSPECAO_CANONICA_086.md",
    "PONTRYAGIN_CARACTERISTICO_E_LIMITE_BBH_086_20260910_062514_4956488/NAO_EXATIDAO_INVARIANTE_E_LIMITE_DA_IMPORTACAO_BBH.md",
    "REVISAO_PONTRYAGIN_CARACTERISTICO_086_20260910/PARECER_TRANSGRESSAO_GL_E_CONTRATO_CARACTERISTICO_086.md",
    "CORRENTES_WEYL_UMA_DERIVADA_086_20260910/CLASSIFICACAO_CORRENTES_W_NABLA_W_E_DIVERGENCIA.md",
    "SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/ESTRITEZA_E_DETECTOR_PRINCIPAL_DE_DIVERGENCIA.md",
    "REVISAO_SIMBOLO_DIVERGENCIA_086_20260910_064135_2856684/PARECER_ESTRITEZA_E_DIVERGENCIA_086.md",
    "COROLARIOS_CE_E_LIDER_CUBICO_086_20260910/COHOMOLOGIA_CE3_E_IMAGEM_CUBICA_ZERO_APOS_C6.md",
]
NAMES = ["REEXAME_SUFICIENCIA.md", "MEMORIA_DE_TRABALHO_086.md", "DESENHO_DO_FECHAMENTO_ADENDO_086.md"]

def pin(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def publish_json(path, obj):
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    tmp = path.with_name(path.name + ".pending")
    if path.exists() or tmp.exists():
        raise FileExistsError(str(path))
    with tmp.open("xb") as stream:
        stream.write(data)
    if tmp.read_bytes() != data or not data:
        raise ValueError("Temporary bytes mismatch")
    tmp.rename(path)
    if path.read_bytes() != data:
        raise ValueError("Final bytes mismatch")

cap = BASE / "PINS_ANTES_NARRATIVOS_086.json"
if sys.argv[1] == "capture":
    publish_json(cap, {"utc": datetime.now(timezone.utc).isoformat(),
                      "sources_before": [pin(ROOT / s) for s in RELATIVE_SOURCES], "helper": pin(__file__)})
    print(json.dumps({"capture": pin(cap), "sources": len(RELATIVE_SOURCES)}))
elif sys.argv[1] == "publish":
    old = json.loads(cap.read_bytes().decode("utf-8"))
    after = [pin(ROOT / s) for s in RELATIVE_SOURCES]
    checks = [{"kind": "source_unchanged", "path": a["path"], "passed": a == b}
              for a, b in zip(old["sources_before"], after, strict=True)]
    checks.append({"kind": "helper_unchanged", "passed": old["helper"] == pin(__file__)})
    snap = json.loads((ROOT / RELATIVE_SOURCES[1]).read_bytes().decode("utf-8-sig"))
    checks.append({"kind": "snapshot_read_counts", "passed": snap["embedded_files"] == 683 and
                  snap["present"] == 77 and len(snap["modules"]) == 98 and len(snap["absent"]) == 21})
    checks.append({"kind": "snapshot_four_pins_unchanged", "passed":
                  len(snap["comparison_with_delivery085"]) == 4 and
                  all(x["unchanged"] for x in snap["comparison_with_delivery085"])})
    checks.append({"kind": "snapshot_no_execution_or_delta", "passed":
                  not snap["new_canonical_content_detected"] and not snap["um_executed_or_imported"] and
                  not snap["originals_written"] and snap["seal_um_hash_matches"]})
    drafts = []
    links = set()
    for name in NAMES:
        final = BASE / name
        draft = final.with_name(name + ".pending_text")
        raw = draft.read_bytes()
        content = raw.decode("utf-8")
        checks.append({"kind": "narrative_utf8_nonempty", "path": str(final),
                       "passed": len(raw) > 3000 and "\x00" not in content and not final.exists()})
        links.update(re.findall(r"\]\(<(C:/[^>]+)>\)", content))
        drafts.append((draft, final, raw))
    final_names = {p.as_posix() for _, p, _ in drafts}
    for link in sorted(links):
        clean = re.sub(r":\d+$", "", link)
        checks.append({"kind": "local_link", "path": clean,
                       "passed": Path(clean).is_file() or clean in final_names})
    failed = [x for x in checks if not x["passed"]]
    if failed:
        print(json.dumps({"failed": failed}, ensure_ascii=False))
        raise SystemExit(2)
    for draft, final, raw in drafts:
        draft.rename(final)
        if final.read_bytes() != raw:
            raise ValueError("Published bytes mismatch")
    record = {"utc": datetime.now(timezone.utc).isoformat(), "author": "/root/finish_gibbs_realization",
              "status": "NEW_NARRATIVES_ONLY_NOT_DELIVERY_FINALIZATION",
              "narratives": [pin(p) for _, p, _ in drafts], "capture": pin(cap), "helper": pin(__file__),
              "sources_before": old["sources_before"], "sources_after": after,
              "checks": checks, "checks_total": len(checks), "checks_passed": len(checks), "failed_checks": [],
              "checks_are_documentary": True,
              "new_mathematical_executions": 0, "new_cas_runs": 0, "new_lean_runs": 0,
              "canonical_files_reopened_here": False, "um_executed_or_imported": False,
              "existing_files_modified": False,
              "pending_reviews_at_narrative_cut": ["Specific independent review of CE/cubic-image corollaries.",
                                                     "Specific independent review of one-derivative current note."],
              "limits": "Root may attach completed pending reviews in a new final addendum; these narratives do not anticipate them."}
    path = BASE / "REGISTRO_EMISSAO_NARRATIVOS_086.json"
    publish_json(path, record)
    print(json.dumps({"narratives": record["narratives"], "record": pin(path),
                      "checks": len(checks)}, ensure_ascii=False))
else:
    raise ValueError("Expected capture or publish")
