"""Measure a new written characteristic-class proof and its immutable input."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
assert ROOT.name == "CLASSES_CARACTERISTICAS_C0_20260909_221649"
assert ROOT.parent.name == "Chatgpt"

def measure(path):
    data = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(data), "lines": len(data.decode("utf-8-sig").splitlines()), "sha256": hashlib.sha256(data).hexdigest()}

source = ROOT.parent / "BV_ANOMALIAS_SIGMA_FORMAL_20260909_215557" / "BV_LOCAL_SIGMA_E_RENORMALIZACAO_CONDICIONAL.md"
source_record = measure(source)
note = ROOT / "EULER_PONTRYAGIN_ON_SHELL_E_LIMITE_C0.md"
manifest = {
    "measured_at_utc": datetime.now(timezone.utc).isoformat(),
    "status": "DERIVED_WRITTEN_NO_NEW_LEAN_OR_CAS",
    "result": "No nonzero Euler/Pontryagin certificate modulo the natural algebraic differential EOM ideal for Lambda>0; scalar constant sector and compact Einstein tests.",
    "demonstrated_bridges": ["off-shell rational identities complexify by polynomial identity", "natural tensorial primitive glues globally", "S4/CP2 evaluation matrix determinant is 6"],
    "open_contracts": ["weak stationary vanishing equals differential EOM ideal in the same admissible class, if weak equality is not defined by that ideal", "remaining C0/KT assumptions", "full sigma H1 classification", "QME and full BV propagators"],
    "input": source_record,
    "new_artifacts": [measure(note), measure(Path(__file__).resolve())],
    "primary_sources_consulted": [
        {"url": "https://arxiv.org/pdf/hep-th/9505173", "locations": "(3.19)-(3.20), (7.33), (8.4)-(8.8), section 9, Appendix E", "role": "Polynomial covariant A2, invariant forms and exact scope of characteristic condition"},
        {"url": "https://arxiv.org/pdf/math/9807055", "locations": "Introduction, (6)-(7), S4 and CP2 examples", "role": "Positive Einstein test metrics, characteristic and signature formulas"},
        {"url": "https://arxiv.org/pdf/1409.1296", "locations": "Section 2 after Lemma 2.4", "role": "Euler and Pontryagin numbers of CP2"},
    ],
    "input_unchanged_during_measurement": measure(source)["sha256"] == source_record["sha256"],
    "originals_modified": False,
    "um_imported_or_executed": False,
}
output = ROOT / "MANIFESTO_CLASSES_C0.json"
temp = ROOT / "MANIFESTO_CLASSES_C0.json.new"
assert not output.exists() and not temp.exists()
data = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with temp.open("xb") as stream:
    stream.write(data)
assert temp.read_bytes() == data and len(data) > 1000
temp.rename(output)
print(json.dumps({"manifest": measure(output), "note": manifest["new_artifacts"][0], "input_unchanged": manifest["input_unchanged_during_measurement"]}, ensure_ascii=False, indent=2))
