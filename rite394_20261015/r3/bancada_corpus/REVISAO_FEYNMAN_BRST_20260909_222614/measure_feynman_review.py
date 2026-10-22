"""Measure existing Feynman sources and the new independent algebraic review."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parent
assert ROOT.name == "REVISAO_FEYNMAN_BRST_20260909_222614"
assert ROOT.parent.name == "Chatgpt"
BASE = ROOT.parent / "EXTENSAO_BRST_COMPLETA_20260909_220941_811364"

def measure(path):
    data = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(data), "lines": len(data.decode("utf-8-sig").splitlines()), "sha256": hashlib.sha256(data).hexdigest()}

paths = [BASE / "ADENDO_FEYNMAN_PARIDADE_E_CONTATOS.md", BASE / "EXTENSAO_BRST_E_CORRECOES_SUAVES.md"]
records = [measure(path) for path in paths]
manifest = {
    "measured_at_utc": datetime.now(timezone.utc).isoformat(),
    "status": "DERIVED_INDEPENDENT_WRITTEN_ALGEBRAIC_REVIEW",
    "scope": "Signs, graded parity, inverse blocks, time-ordering contacts including mixed derivatives, linear Ward identities. Existence of the principal note Hadamard pairs is an input to this review.",
    "input_sources": records,
    "new_artifacts": [measure(ROOT / "REVISAO_ALGEBRICA_FEYNMAN_E_CONTATOS.md"), measure(Path(__file__).resolve())],
    "input_hashes_unchanged_during_measurement": all(measure(path)["sha256"] == rec["sha256"] for path, rec in zip(paths, records)),
    "lean_executed": False,
    "cas_executed": False,
    "um_executed_or_imported": False,
    "originals_modified": False,
}
output = ROOT / "MANIFESTO_REVISAO_FEYNMAN.json"
temp = ROOT / "MANIFESTO_REVISAO_FEYNMAN.json.new"
assert not output.exists() and not temp.exists()
data = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with temp.open("xb") as stream:
    stream.write(data)
assert temp.read_bytes() == data and len(data) > 1000
temp.rename(output)
print(json.dumps({"manifest": measure(output), "review": manifest["new_artifacts"][0], "unchanged": manifest["input_hashes_unchanged_during_measurement"]}, ensure_ascii=False, indent=2))
