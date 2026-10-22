"""Pin new review artifacts and recheck all previously read sources without modifying them."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

folder = Path(__file__).resolve().parent
receipt = json.loads((folder / "RECEIPT_CURRENT.json").read_bytes())
for name, pin in receipt["source_pins"].items():
    data = Path(name).read_bytes()
    assert len(data) == pin["bytes"] and hashlib.sha256(data).hexdigest() == pin["sha256"], name
handoff = folder.parent / "TUNEL" / "DO_CHATGPT" / "ENTREGA_064_ESPONTANEA_reexame_canonico_e_pendencias.md"
paths = [folder / name for name in ["REEXAME.md", "RECEIPT_CURRENT.json", "RECEIPT_CAPTURE.json",
                                  "audit_current.py", "audit_capture.py", "finalize.py"]] + [handoff]
pins = []
for path in paths:
    data = path.read_bytes()
    pins.append({"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
payload = {"status": "REEXAM_DELIVERED_064__ORIGINAL_SOURCES_UNCHANGED",
           "created_utc": datetime.now(timezone.utc).isoformat(), "artifacts": pins,
           "goal_completed": False, "um_executed_or_imported": False,
           "scope": "Canonical file available at the examined path remains v337; later work at an unknown path is not covered."}
data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
dest = folder / "DELIVERY_MANIFEST.json"
assert not dest.exists()
tmp = dest.with_suffix(".json.tmp_" + datetime.now().strftime("%H%M%S_%f"))
with tmp.open("xb") as handle:
    handle.write(data)
    handle.flush()
    os.fsync(handle.fileno())
assert tmp.read_bytes() == data
tmp.rename(dest)
assert dest.read_bytes() == data
print(json.dumps({"status": payload["status"], "manifest": str(dest), "source_pins_rechecked": len(receipt["source_pins"])}))
