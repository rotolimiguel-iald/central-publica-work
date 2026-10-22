"""Preserve a visible record of the superseded partial compilation, without a PASS claim."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

base = Path(r"C:\IALD\Central de Patentes\Chatgpt")
out = Path(__file__).resolve().parent
partial = base / "COPIA_INTEGRADA_20260909_161645_481582/BUILD_TRANSPOSED_20260909_161710_098626"
successor = base / "ADAPTADOR_INCREMENTAL_20260909_162620_395030/BUILD_INCREMENTAL_20260909_162634_176093/BUILD_PLAN.json"
assert out.parent == base and not (partial / "TRANSPOSED_RESULT.json").exists()


def record(path):
    data = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


payload = {
    "status": "INTERRUPTED_BY_ROOT_FOR_VERIFIED_CACHE_REUSE__NOT_A_COMPLETED_BUILD",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "session_id": 27458, "tool_exit_code_after_interrupt": 1,
    "reason": "The old 45 sources were proved byte-identical to their prior PASS build. Root stopped this partial sequential run and started a fresh isolated plan compiling the 18 new leaves and all aggregate roots/audits.",
    "partial_plan": record(partial / "BUILD_PLAN.json"),
    "successor_plan": record(successor),
    "retained_logs": [record(path) for path in sorted(partial.glob("*.log"))],
    "completed_pass_claim": False,
    "partial_outputs_reused_by_successor": False,
    "old_sources_or_logs_modified": False,
}
path = out / "REGISTRO_COMPILACAO_PARCIAL_INTERROMPIDA.json"
assert not path.exists()
raw = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
temp = path.with_name(path.name + ".tmp")
with temp.open("xb") as stream:
    stream.write(raw)
    stream.flush()
    os.fsync(stream.fileno())
assert temp.read_bytes() == raw
os.rename(temp, path)
assert path.read_bytes() == raw
print(json.dumps({"status": payload["status"], "retained_logs": len(payload["retained_logs"])}))
