"""Fresh pins for a conditional written theorem; all writes are new files."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
HERE = Path(__file__).resolve().parent
assert HERE == ROOT / "POSITIVIDADE_BRST_FORMAL_072_20260910"

def pin(path):
    raw = path.read_bytes()
    raw.decode("utf-8-sig")
    return {
        "path": str(path), "bytes": len(raw), "lines": len(raw.splitlines()),
        "crlf": raw.count(b"\r\n"), "sha256": hashlib.sha256(raw).hexdigest(),
    }

sources = [
    ROOT / "CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909" / "PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md",
    ROOT / "CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909" / "DICIONARIO_GRASSMANN_E_ACAO_BV.md",
    ROOT / "EXTENSAO_BRST_COMPLETA_20260909_220941_811364" / "EXTENSAO_BRST_E_CORRECOES_SUAVES.md",
    ROOT / "HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912" / "ESTADO_FISICO_HADAMARD_E_CONTRATOS.md",
]
before = [pin(path) for path in sources]
note = pin(HERE / "ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md")
script = pin(Path(__file__).resolve())
after = [pin(path) for path in sources]
assert before == after, "A reviewed source changed during measurement."
payload = {
    "measured_at_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Arco072: conditional formal physical state for the ambient Einstein-S3-sigma model",
    "statutes": {
        "written_theorem": "DERIVED/KNOWN; not Lean",
        "quartet_certificate": "DERIVED algebraic: Q^2=0, {Q,h}=N_aux, null closed vectors are exact",
        "formal_lift": "DERIVED conditional on P0-P2; explicit coefficient recurrence and normalized vector state",
        "measurement": "REAL byte reads, SHA256, stable input pins across this measurement",
    },
    "open_contracts": [
        "Compatible Hadamard/Wick realization and common operator domain for the free quartet/null-completeness certificate",
        "Renormalized QME/current identities and on-shell comparison in the actually admitted Q2 space",
        "Charge implementation, compatible ghost grading and scalar commutant on a complete Cauchy band, or explicit charge nilpotence",
        "Compatible states across cutoffs/backgrounds; no global state limit asserted",
    ],
    "limitations": [
        "No statement of nonperturbative positivity, convergence, UV completion or physical confirmation",
        "Every free closed vector lifts conditionally; not every free observable is shown to have a local interacting lift",
        "The algebraic quartet polarization is not declared Hadamard by a Cauchy splitting alone",
        "Formal positivity is stated over C[[z]] with a locally finite perturbative organization",
    ],
    "inputs": before,
    "artifacts": [note, script],
    "inputs_stable_during_measurement": True,
    "executions": {"CAS": False, "Lean": False, "um_py": False, "proof_script": False, "stdlib_measurement_only": True},
    "custody": "New files only in this Chatgpt directory. No original, frozen note or PASS leaf edited.",
    "primary_sources_read": [
        {"url": "https://arxiv.org/pdf/hep-th/9807078v2", "locators": "Sections4.2-4.3, equation4.8, Theorem4, Corollaries5-6", "scope": "Formal BRST positivity stability; QED-specific verification not imported"},
        {"url": "https://arxiv.org/pdf/hep-th/9807215v1", "locators": "Theorem1 and section3", "scope": "Summary of the stability theorem; boundary-specific QED hypotheses kept separate"},
        {"url": "https://arxiv.org/pdf/hep-th/0411196", "locators": "Section2, equation2.4", "scope": "Secondary formulation by the theorem authors; primary research references above used for the proof contract"},
        {"url": "https://arxiv.org/pdf/1301.7037v3", "locators": "Section4, Theorem4.2, equations65-66", "scope": "On-shell BV implementation by BRST charge, conditional on QME/anomaly removal"},
        {"url": "https://arxiv.org/html/1306.1058v4", "locators": "Section3.4 equations67-68, section5, AppendixB", "scope": "Perturbative gravity state/charge organization; no generic free positivity theorem imported"},
        {"url": "https://arxiv.org/html/1407.8079v2", "locators": "Sections2-3", "scope": "Classical BRST phase space and Hadamard covariances; not a Fock null-completeness proof"},
    ],
    "web_pin_policy": "URLs and locators record consulted primary sources; no unmeasured PDF hash asserted.",
}
target = HERE / "MANIFESTO_ESTADO_INTERAGENTE_FORMAL_072.json"
temporary = HERE / "MANIFESTO_ESTADO_INTERAGENTE_FORMAL_072.json.new"
assert not target.exists() and not temporary.exists()
data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with temporary.open("xb") as handle:
    handle.write(data)
assert temporary.read_bytes() == data and len(data) > 1000
temporary.rename(target)
assert target.read_bytes() == data
print(json.dumps({"note": note, "manifest": pin(target), "script": script, "source_count": len(sources), "inputs_stable": True}, ensure_ascii=False, indent=2))
