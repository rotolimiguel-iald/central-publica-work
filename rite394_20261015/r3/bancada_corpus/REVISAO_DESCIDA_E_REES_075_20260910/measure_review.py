from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
HERE = Path(__file__).resolve().parent
sources = [
    ROOT / "DESCIDA_NATURAL_SIMBOLOS_075_20260910" / "DESCIDA_NATURAL_POR_OPERADORES.md",
    ROOT / "DESCIDA_NATURAL_SIMBOLOS_075_20260910" / "ADENDO_PRIMEIRO_DESCENDENTE_E_COMPOSICAO_075.md",
    ROOT / "COMPLETACAO_REES_BRST_074_20260910" / "COMPLETACAO_POR_LACOS_E_VALENCIA.md",
    ROOT / "AUDITORIA_DESCIDA_NATURAL_075_20260910" / "SIMBOLOS_GRASSMANN_E_PRIMEIRO_DESCENDENTE.md",
]


def pin(path):
    data = path.read_bytes()
    if data != path.read_bytes():
        raise RuntimeError(f"Unstable source: {path}")
    return {"path": str(path), "bytes": len(data), "lines": len(data.decode("utf-8").splitlines()), "sha256": hashlib.sha256(data).hexdigest(), "double_read_stable": True}


record = {
    "arc": "075",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "DERIVED_INDEPENDENT_DOCUMENTARY_AND_MATHEMATICAL_REVIEW",
    "sources_read_only": [pin(p) for p in sources],
    "new_artifacts": [pin(HERE / "PARECER_INDEPENDENTE_DESCIDA_E_REES.md"), pin(Path(__file__).resolve())],
    "finding": "No material error found in the stated composition; horizontal primitive operations preserve E/N/Rees with B0 connections. Universal off-shell consistency and free ghost jets remain explicit hypotheses.",
    "not_established": ["Total cocycle exactness", "Remaining E2 groups", "Causal counterterm hierarchy", "QME", "General quantum background independence", "UV completion"],
    "no_original_modified": True,
    "no_um_execution_import": True,
    "no_lean_cas_execution": True,
    "no_external_approval_claim": True,
}
target = HERE / "MANIFESTO_REVISAO_DESCIDA_REES_075.json"
temp = HERE / "MANIFESTO_REVISAO_DESCIDA_REES_075.json.pending"
if target.exists() or temp.exists():
    raise FileExistsError("New artifacts only")
raw = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with temp.open("xb") as stream:
    stream.write(raw)
if temp.read_bytes() != raw or temp.stat().st_size != len(raw):
    raise RuntimeError("Temporary verification failed")
temp.rename(target)
print(json.dumps({"manifest": pin(target), "review": record["new_artifacts"][0], "source_pins": record["sources_read_only"][:2]}, ensure_ascii=False, indent=2))
