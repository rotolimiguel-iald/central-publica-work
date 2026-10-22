from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
HERE = Path(__file__).resolve().parent
INPUTS = [
    ROOT / "EXTENSAO_BRST_COMPLETA_20260909_220941_811364" / "EXTENSAO_BRST_E_CORRECOES_SUAVES.md",
    ROOT / "HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912" / "ESTADO_FISICO_HADAMARD_E_CONTRATOS.md",
    ROOT / "CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909" / "DICIONARIO_GRASSMANN_E_ACAO_BV.md",
    ROOT / "POSITIVIDADE_BRST_FORMAL_072_20260910" / "ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md",
    ROOT / "POSITIVIDADE_BRST_FORMAL_072_20260910" / "PRECISAO_COMUTADOR_GRADUADO_E_R0.md",
]
OUTPUTS = [
    HERE / "RADICAL_DA_PSEUDOCOVARIANCIA_E_P0.md",
    HERE / "REPARO_DO_BLOCO_E_LIMITE_HADAMARD.md",
    Path(__file__).resolve(),
]


def pin(path):
    first = path.read_bytes()
    second = path.read_bytes()
    if first != second:
        raise RuntimeError(f"Unstable input: {path}")
    text = first.decode("utf-8")
    return {
        "path": str(path),
        "bytes": len(first),
        "lines": len(text.splitlines()),
        "sha256": hashlib.sha256(first).hexdigest(),
        "double_read_stable": True,
    }


payload = {
    "arc": "073",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "DERIVED_WRITTEN_MATHEMATICS_ONLY",
    "inputs_read_only": [pin(p) for p in INPUTS],
    "new_artifacts": [pin(p) for p in OUTPUTS],
    "primary_sources_read": [
        "https://arxiv.org/html/1407.8079v2",
        "https://arxiv.org/pdf/hep-th/9807078v2",
    ],
    "scope": {
        "finite_counterexample": "Proves insufficiency of automatic P0 after quotient by covariance radical; not nonexistence of a valid extension.",
        "saturation": "Exact sequence and S1/S2 for canonical physical identification; algebraic Fock transport conditional on those conditions.",
        "repair": "Finite smooth constraint-block repair demonstrated; global formula remains subject to Hadamard and common-domain controls.",
        "no_um_execution_or_import": True,
        "no_lean_or_cas_execution": True,
        "no_existing_artifact_modified": True,
        "no_external_approval_claim": True,
    },
}
target = HERE / "MANIFESTO_RADICAL_E_REPARO_073.json"
temporary = HERE / "MANIFESTO_RADICAL_E_REPARO_073.json.new"
if target.exists() or temporary.exists():
    raise FileExistsError("New files only: manifest or temporary already exists")
encoded = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with temporary.open("xb") as stream:
    stream.write(encoded)
if temporary.read_bytes() != encoded or temporary.stat().st_size != len(encoded):
    raise RuntimeError("Temporary verification failed")
temporary.rename(target)
print(json.dumps({"manifest": pin(target), "new_artifacts": payload["new_artifacts"]}, ensure_ascii=False, indent=2))
