"""Pin a new sign correction without modifying frozen inputs or manifests."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

HERE = Path(__file__).resolve().parent
assert HERE == Path(r"C:\IALD\Central de Patentes\Chatgpt\POSITIVIDADE_BRST_FORMAL_072_20260910")

def pin(path):
    raw = path.read_bytes()
    raw.decode("utf-8-sig")
    return {"path": str(path), "bytes": len(raw), "lines": len(raw.splitlines()),
            "sha256": hashlib.sha256(raw).hexdigest()}

frozen = [HERE / "ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md",
          HERE / "MANIFESTO_ESTADO_INTERAGENTE_FORMAL_072.json"]
before = [pin(path) for path in frozen]
artifacts = [pin(HERE / "PRECISAO_COMUTADOR_GRADUADO_E_R0.md"), pin(Path(__file__).resolve())]
after = [pin(path) for path in frozen]
assert before == after
data = {
    "measured_at_utc": datetime.now(timezone.utc).isoformat(),
    "status": "DERIVED written sign correction; REAL measured pins",
    "correction": "For Q odd: [A,Q]_gr = -(-1)^parity(A) [Q,A]_gr. Charge sign flip alone translates the order only for even A.",
    "R0": "R0 = (N_aux^-1 h_qt)|im Q0, with N_aux^-1=0 on the auxiliary vacuum sector.",
    "frozen_inputs": before,
    "new_artifacts": artifacts,
    "frozen_inputs_stable_during_measurement": True,
    "no_CAS_Lean_um_execution": True,
    "custody": "Only new files in the same authorized Chatgpt folder; prior note and manifest untouched.",
}
target = HERE / "MANIFESTO_PRECISAO_SINAL_072.json"
temporary = HERE / "MANIFESTO_PRECISAO_SINAL_072.json.new"
assert not target.exists() and not temporary.exists()
raw = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with temporary.open("xb") as handle:
    handle.write(raw)
assert temporary.read_bytes() == raw and len(raw) > 1000
temporary.rename(target)
assert target.read_bytes() == raw
print(json.dumps({"adendo": artifacts[0], "manifest": pin(target), "frozen_inputs": before,
                  "inputs_stable": True}, ensure_ascii=False, indent=2))
