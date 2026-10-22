from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import uuid
FOLDER = Path(__file__).resolve().parent
SOURCE = FOLDER / "write_criterion_contract087_new.py"
DEST = FOLDER / "write_criterion_contract087_v2_new.py"
PROVENANCE = FOLDER / "PROVENIENCIA_EMISSOR_V2_087.json"
old = SOURCE.read_bytes()
old_line = b"for token, value in LINKS.items():"
new_line = b"for token, value in sorted(LINKS.items(), key=lambda item: -len(item[0])):"
if old.count(old_line) != 1:
    raise RuntimeError("Expected single loop not found")
new = old.replace(old_line, new_line, 1)
def save(path, data):
    if path.exists():
        raise FileExistsError(str(path))
    temp = path.with_name(path.name + ".pending_" + uuid.uuid4().hex)
    with temp.open("xb") as h:
        h.write(data)
        h.flush()
        os.fsync(h.fileno())
    if temp.read_bytes() != data:
        raise RuntimeError("Temporary verification")
    if path.exists():
        raise FileExistsError(str(path))
    os.rename(temp, path)
    if path.read_bytes() != data:
        raise RuntimeError("Roundtrip verification")
save(DEST, new)
if SOURCE.read_bytes() != old:
    raise RuntimeError("Historical script changed")
record = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "source": {"path": SOURCE.as_posix(), "bytes": len(old), "sha256": hashlib.sha256(old).hexdigest()},
    "destination": {"path": DEST.as_posix(), "bytes": len(new), "sha256": hashlib.sha256(new).hexdigest()},
    "change": "One loop now orders reference tokens by descending length, preventing @DESCENT from consuming @DESCENT_APPLICATION.",
    "failure_preserved": "Historical emitter exited 1 before note creation, RuntimeError: Unused reference token: @DESCENT_APPLICATION.",
    "source_bytes_unchanged": True,
    "no_mathematical_change": True,
    "new_emitter_executed_by_this_helper": False,
}
save(PROVENANCE, (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps(record, ensure_ascii=False, indent=2))

