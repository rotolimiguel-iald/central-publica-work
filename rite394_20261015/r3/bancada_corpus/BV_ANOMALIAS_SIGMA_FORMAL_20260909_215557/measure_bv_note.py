"""Measure immutable inputs and new authored notes; never run the terminal model."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent
assert ROOT.name == "BV_ANOMALIAS_SIGMA_FORMAL_20260909_215557"
assert WORK.name == "Chatgpt"

def measure(path):
    data = path.read_bytes()
    decoded = data.decode("utf-8-sig")
    return {
        "path": str(path.resolve()),
        "bytes": len(data),
        "lines": len(decoded.splitlines()),
        "sha256": hashlib.sha256(data).hexdigest(),
    }

inputs = [
    WORK / "QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633" / "OPERADOR_JACOBI_GAUGE_E_ESCOPO.md",
    WORK / "HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912" / "ESTADO_FISICO_HADAMARD_E_CONTRATOS.md",
    WORK / "REDUCAO_ESCALAR_VETOR_SIGMA_20260909_212531" / "REDUCAO_ADM_MODOS_FISICOS.md",
    WORK / "MODOS_TENSORIAIS_EXATOS_20260909" / "ACAO_TT_E_MODOS_EXATOS.md",
    WORK / "RENORMALIZACAO_SIGMA_EFT_20260909" / "CONTRATERMOS_SIGMA_E_ORDEM_EFT.md",
    WORK / "RENORMALIZACAO_SIGMA_EFT_20260909" / "VERIFICACAO_SIGMA_HEAT.json",
]
notes = [ROOT / "BV_LOCAL_SIGMA_E_RENORMALIZACAO_CONDICIONAL.md", ROOT / "REVISAO_PROPRIA_COEFICIENTE_SIGMA.md", Path(__file__).resolve()]
records = [measure(path) for path in inputs]
receipt = json.loads(inputs[-1].read_text(encoding="utf-8-sig"))
manifest = {
    "measured_at_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Written derivations and primary-source audit; no new Lean or CAS execution; no um.py read/import/execute in this front.",
    "statuses": {
        "epsilon_adic_lifting": "DERIVED conditional on reference H1 exactness in the admissible complex",
        "all_orders_qme": "DERIVED conditional on Q1-Q3 and relevant cohomology",
        "reference_C0_application": "OPEN explicit regularity/equivariant condition and primitive class contract",
        "epsilon_equals_one_specialization": "OPEN",
        "full_BV_Hadamard_matrix": "OPEN beyond physical linear state",
        "background_independence_and_global_anomalies": "OPEN separate contracts",
        "uv_completion": "OPEN",
        "heat_kernel_review": "DERIVED own written checks; other receipt measured, not rerun",
    },
    "local_inputs": records,
    "new_authored_artifacts": [measure(path) for path in notes],
    "existing_heat_receipt_keys": list(receipt),
    "primary_sources_consulted": [
        {"url": "https://arxiv.org/pdf/hep-th/9505173", "sections": "2,4,7 including (7.33),9,10.4", "scope": "Einstein-Yang-Mills local BRST classification with explicit assumptions"},
        {"url": "https://arxiv.org/pdf/hep-th/0002245", "sections": "4.7,5.3,6.4,11.1", "scope": "Formal local series and homological tools; section 11 Yang-Mills not promoted to sigma-gravity"},
        {"url": "https://arxiv.org/html/1110.5232v3", "sections": "4.1-4.2", "scope": "Anomalous master Ward identity, QME, finite renormalization"},
        {"url": "https://arxiv.org/html/1306.1058v4", "sections": "3.4,5,6", "scope": "pAQFT gravity; pure-gravity cohomology statement"},
        {"url": "https://arxiv.org/html/1804.07640", "sections": "Introduction,4,4.1", "scope": "Background independence obstructions distinct from fixed-background gauge QME"},
        {"url": "https://arxiv.org/abs/2209.02393", "sections": "Abstract", "scope": "Adler-Bardeen theorem restricted to renormalizable Yang-Mills"},
        {"url": "https://arxiv.org/pdf/hep-th/9802118", "sections": "Abstract,Introduction", "scope": "Gauged principal sigma is not diffeomorphism-only sigma"},
        {"url": "https://arxiv.org/html/1407.8079v2", "sections": "2.4,3.3", "scope": "Physical state versus full BRST covariance contracts"},
        {"url": "https://arxiv.org/abs/2212.07800", "sections": "Abstract", "scope": "Formal locally covariant effective quantum gravity"},
        {"url": "https://arxiv.org/html/hep-th/0306138v3", "sections": "2.1,4.1", "scope": "Universal heat kernel coefficient conventions"},
    ],
    "input_hashes_unchanged_during_measurement": all(measure(path)["sha256"] == record["sha256"] for path, record in zip(inputs, records)),
}
output = ROOT / "MANIFESTO_BV_ANOMALIAS.json"
temp = ROOT / "MANIFESTO_BV_ANOMALIAS.json.new"
assert not output.exists() and not temp.exists(), "Refuse to overwrite an existing artifact"
data = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with temp.open("xb") as stream:
    stream.write(data)
assert temp.read_bytes() == data and len(data) > 1000
temp.rename(output)
print(json.dumps({"manifest": measure(output), "notes": manifest["new_authored_artifacts"], "unchanged": manifest["input_hashes_unchanged_during_measurement"], "existing_receipt": receipt}, ensure_ascii=False, indent=2))
