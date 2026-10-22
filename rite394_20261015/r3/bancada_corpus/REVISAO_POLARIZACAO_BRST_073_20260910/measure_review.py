from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
HERE = Path(__file__).resolve().parent
inputs = [
    ROOT / "POLARIZACAO_BRST_HADAMARD_073_20260910" / "POLARIZACAO_ADAPTADA_E_MAJORANTE.md",
    ROOT / "EXTENSAO_BRST_COMPLETA_20260909_220941_811364" / "EXTENSAO_BRST_E_CORRECOES_SUAVES.md",
    ROOT / "HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912" / "ESTADO_FISICO_HADAMARD_E_CONTRATOS.md",
    ROOT / "RADICAL_GNS_BRST_073_20260910" / "RADICAL_DA_PSEUDOCOVARIANCIA_E_P0.md",
    ROOT / "RADICAL_GNS_BRST_073_20260910" / "REPARO_DO_BLOCO_E_LIMITE_HADAMARD.md",
]


def measure(path):
    data = path.read_bytes()
    if data != path.read_bytes():
        raise RuntimeError(f"Unstable file: {path}")
    return {"path": str(path), "bytes": len(data), "lines": len(data.decode("utf-8").splitlines()), "sha256": hashlib.sha256(data).hexdigest(), "double_read_stable": True}


payload = {
    "arc": "073",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "DERIVED_INDEPENDENT_WRITTEN_REVIEW",
    "inputs_read_only": [measure(p) for p in inputs],
    "new_artifacts": [measure(HERE / "PARECER_POLARIZACAO_E_RADICAL.md"), measure(Path(__file__).resolve())],
    "primary_source_consulted": "https://link.springer.com/article/10.1007/s00023-025-01539-1",
    "no_originals_modified": True,
    "no_um_execution_import": True,
    "no_lean_cas_execution": True,
    "no_external_approval_claim": True,
    "scope": "No material error found in the written adapted-polarization construction; Fock/Wick and interacting charge remain distinct contracts.",
}
target = HERE / "MANIFESTO_REVISAO_POLARIZACAO_073.json"
tmp = HERE / "MANIFESTO_REVISAO_POLARIZACAO_073.json.new"
if target.exists() or tmp.exists():
    raise FileExistsError("New artifacts only")
raw = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with tmp.open("xb") as stream:
    stream.write(raw)
if tmp.read_bytes() != raw or tmp.stat().st_size != len(raw):
    raise RuntimeError("Temporary verification failed")
tmp.rename(target)
print(json.dumps({"manifest": measure(target), "review": payload["new_artifacts"][0], "source": payload["inputs_read_only"][0]}, ensure_ascii=False, indent=2))
