from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
HERE = Path(__file__).resolve().parent
inputs = [
    ROOT / "NATURALIDADE_E_CURVATURA_B0_074_20260910" / "NORMALIZACAO_S_E_OBSTRUCAO_EULER.md",
    ROOT / "NATURALIDADE_E_CURVATURA_B0_074_20260910" / "PRECISAO_METRICA_E_FRAME_DE_REFERENCIA.md",
    ROOT / "COHOMOLOGIA_ESPECTADOR_B0_073_20260910" / "PRIMITIVA_ORDINARIA_COM_B0_E_LIMITE_ADMISSIVEL.md",
]


def pin(path):
    raw = path.read_bytes()
    if raw != path.read_bytes():
        raise RuntimeError(f"Unstable file: {path}")
    return {"path": str(path), "bytes": len(raw), "lines": len(raw.decode("utf-8").splitlines()), "sha256": hashlib.sha256(raw).hexdigest(), "double_read_stable": True}


record = {
    "arc": "075",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "DERIVED_INDEPENDENT_WRITTEN_AUDIT_AND_TOP_FORM_COMPLEMENT",
    "inputs_read_only": [pin(p) for p in inputs],
    "new_artifacts": [pin(HERE / "SIMBOLOS_GRASSMANN_E_PRIMEIRO_DESCENDENTE.md"), pin(Path(__file__).resolve())],
    "primary_source_consulted": "https://arxiv.org/pdf/hep-th/0002245v3",
    "unused_fetch_failure": "https://arxiv.org/pdf/math/9803115v1 returned cache miss in this audit and was not used as evidence.",
    "scope": "Natural horizontal descent in positive ghost, with free off-shell jets; top-form naturalization conditional on ordinary exactness; no E2 or anomaly calculation.",
    "no_original_modification": True,
    "no_um_execution_import": True,
    "no_lean_cas_execution": True,
    "no_external_approval_claim": True,
}
target = HERE / "MANIFESTO_AUDITORIA_DESCIDA_075.json"
temp = HERE / "MANIFESTO_AUDITORIA_DESCIDA_075.json.pending"
if target.exists() or temp.exists():
    raise FileExistsError("New files only")
raw = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with temp.open("xb") as stream:
    stream.write(raw)
if temp.read_bytes() != raw or temp.stat().st_size != len(raw):
    raise RuntimeError("Temporary verification failed")
temp.rename(target)
print(json.dumps({"manifest": pin(target), "note": record["new_artifacts"][0]}, ensure_ascii=False, indent=2))
