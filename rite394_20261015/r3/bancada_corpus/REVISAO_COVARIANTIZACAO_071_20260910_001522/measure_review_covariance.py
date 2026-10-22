"""Measure immutable review inputs and newly written artifacts; never overwrite."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
HERE = Path(__file__).resolve().parent
EXPECTED = ROOT / "REVISAO_COVARIANTIZACAO_071_20260910_001522"
assert HERE == EXPECTED

def pin(path):
    raw = path.read_bytes()
    raw.decode("utf-8-sig")
    return {
        "path": str(path),
        "bytes": len(raw),
        "lines": len(raw.splitlines()),
        "crlf": raw.count(b"\r\n"),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }

inputs = [
    ROOT / "COVARIANTIZACAO_SUAVE_071_20260910_001058_826723" / "COVARIANTIZACAO_E_H2_GLOBAL.md",
    ROOT / "COVARIANTIZACAO_SUAVE_071_20260910_001058_826723" / "COROLARIO_H5_E_ANOMALIA_LOCAL.md",
    ROOT / "M2_SUAVE_RELATIVO_071_20260910_000347" / "M2_SUAVE_POR_COMPATIBILIDADE_E_SPENCER.md",
    ROOT / "M2_SUAVE_RELATIVO_071_20260910_000347" / "COROLARIO_H0_H1_E_FINITUDE.md",
    ROOT / "M2_SUAVE_RELATIVO_071_20260910_000347" / "PRECISAO_FATORACAO_FINITA_OPERADORES.md",
    ROOT / "M2_SUAVE_RELATIVO_071_20260910_000347" / "MANIFESTO_M2_SUAVE_RELATIVO_071.json",
    ROOT / "REGULARIDADE_KT_JATOS_20260909_224852" / "CERTIFICADO_POLINOMIAL_EINSTEIN_SIGMA.md",
    ROOT / "NORMALIDADE_RELATIVA_070_20260909_233414" / "NORMALIDADE_FORMAL_E_RESIDUO_SUAVE.md",
]
before = [pin(path) for path in inputs]
artifacts = [
    pin(HERE / "PARECER_COVARIANTIZACAO_SUAVE.md"),
    pin(HERE / "ADENDO_REVISAO_H5_E_ANOMALIA_LOCAL.md"),
    pin(Path(__file__).resolve()),
]
after = [pin(path) for path in inputs]
assert before == after, "Input changed while measuring; fail closed."
payload = {
    "measured_at_utc": datetime.now(timezone.utc).isoformat(),
    "status": {
        "mathematical_review": "DERIVED: own written analysis; no material error identified within declared contracts",
        "measurement": "REAL: fresh byte reads and SHA256; input pins stable across this measurement",
        "machine_proof": "No CAS or Lean run; no um.py execution or import",
        "custody": "Only new files in this Chatgpt folder; no frozen input modified",
    },
    "precision": "For alpha=s beta with gh(alpha)=q, antigh(beta)<=11-q; central q=2 gives bound 9.",
    "scope": "Natural covariant H2 characteristic and smooth full-vielbein H1,4; Q2 and renormalized QME remain separate.",
    "inputs": before,
    "artifacts": artifacts,
    "inputs_stable_during_measurement": True,
    "primary_references": [
        {"url": "https://arxiv.org/pdf/hep-th/9505173v2", "locators": "Sections 3-7; equations (3.6)-(3.7), (6.15); Appendices B-C and E", "evidence": "Read by web tool; no local PDF hash asserted"},
        {"url": "https://arxiv.org/pdf/hep-th/0002245v3", "locators": "Theorem 7.1 and section 7.3", "evidence": "Read by web tool; no local PDF hash asserted"},
    ],
}
destination = HERE / "MANIFESTO_REVISAO_COVARIANTIZACAO_071.json"
temporary = HERE / "MANIFESTO_REVISAO_COVARIANTIZACAO_071.json.new"
assert not destination.exists() and not temporary.exists()
data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with temporary.open("xb") as handle:
    handle.write(data)
assert temporary.read_bytes() == data and len(data) > 1000
temporary.rename(destination)
assert destination.read_bytes() == data
print(json.dumps({"manifest": pin(destination), "artifacts": artifacts, "reviewed_sources": before[:2], "inputs_stable": True}, ensure_ascii=False, indent=2))
