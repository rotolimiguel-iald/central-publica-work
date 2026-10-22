from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
HERE = Path(__file__).resolve().parent
sources = [
    ROOT / "FOCK_HADAMARD_QUARTETOS_073_20260910" / "FOCK_DOMINIO_WICK_E_P0.md",
    ROOT / "POLARIZACAO_BRST_HADAMARD_073_20260910" / "POLARIZACAO_ADAPTADA_E_MAJORANTE.md",
    ROOT / "EXTENSAO_BRST_COMPLETA_20260909_220941_811364" / "EXTENSAO_BRST_E_CORRECOES_SUAVES.md",
    ROOT / "POSITIVIDADE_BRST_FORMAL_072_20260910" / "ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md",
    ROOT / "POSITIVIDADE_BRST_FORMAL_072_20260910" / "PRECISAO_COMUTADOR_GRADUADO_E_R0.md",
]


def pin(path):
    raw = path.read_bytes()
    if raw != path.read_bytes():
        raise RuntimeError(f"File changed during measurement: {path}")
    return {"path": str(path), "bytes": len(raw), "lines": len(raw.decode("utf-8").splitlines()), "sha256": hashlib.sha256(raw).hexdigest(), "double_read_stable": True}


record = {
    "arc": "073",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "DERIVED_WRITTEN_COROLLARY",
    "read_only_sources": [pin(p) for p in sources],
    "new_artifacts": [pin(HERE / "COMUTANTE_ESCALAR_E_CARGA_CONDICIONAL.md"), pin(Path(__file__).resolve())],
    "primary_sources_consulted": ["https://arxiv.org/pdf/hep-th/9807078v2", "https://arxiv.org/pdf/1301.7037v3"],
    "scope": {
        "scalar_commutant": "Continuous finite-particle-increase operators on the completed nuclear smooth Fock domain; complete Cauchy band.",
        "formal_nilpotency": "Conditional on an implemented nilpotent represented derivation; scalar ring C[[z]] of ghost zero.",
        "symmetry": "Conditional on common-domain Krein adjoints and the explicitly stated graded star compatibility.",
        "no_current_or_qme_constructed": True,
        "no_original_modified": True,
        "no_um_execution_import": True,
        "no_lean_cas_execution": True,
        "no_external_approval_claim": True,
    },
}
target = HERE / "MANIFESTO_COMUTANTE_FOCK_073.json"
temp = HERE / "MANIFESTO_COMUTANTE_FOCK_073.json.new"
if target.exists() or temp.exists():
    raise FileExistsError("New artifacts only")
encoded = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with temp.open("xb") as stream:
    stream.write(encoded)
if temp.read_bytes() != encoded or temp.stat().st_size != len(encoded):
    raise RuntimeError("Temporary verification failed")
temp.rename(target)
print(json.dumps({"manifest": pin(target), "note": record["new_artifacts"][0], "fock_source": record["read_only_sources"][0]}, ensure_ascii=False, indent=2))
