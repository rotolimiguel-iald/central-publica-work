from pathlib import Path
import hashlib
import json
import os
import datetime as dt

folder = Path(__file__).resolve().parent
source = folder / "write_reinspection087_new.py"
dest = folder / "write_reinspection087_v2_new.py"
raw = source.read_bytes()
old = b'total-present != old["absent"]'
new = b'total-present != len(old["absent"])'
if raw.count(old) != 1:
    raise RuntimeError("Expected unique schema correction absent")
changed = raw.replace(old, new)
def emit(p, data):
    tmp = p.with_name(p.name + ".pending_new")
    if p.exists() or tmp.exists():
        raise FileExistsError(str(p))
    with tmp.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    if tmp.read_bytes() != data:
        raise RuntimeError("Verification failed")
    os.rename(tmp, p)
    if p.read_bytes() != data:
        raise RuntimeError("Post-rename verification failed")
def pin(p):
    b = p.read_bytes()
    return {"path": p.as_posix(), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
emit(dest, changed)
if source.read_bytes() != raw:
    raise RuntimeError("Original helper changed")
record = {"created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
          "historical_failure_preserved": {"helper": pin(source), "exit_code": 1,
            "reason": "Capture086 stores absent as a list, not an integer; old helper compared its integer count with the list.",
            "original_exception": "RuntimeError: Inconsistent capture086 module inventory",
            "outputs_before_failure": "No note or receipt emitted; helper only was present."},
          "new_helper": pin(dest),
          "exact_replacement": {"old": old.decode(), "new": new.decode()},
          "source_helper_byte_identical_after": True,
          "existing_files_modified": False,
          "canonical_execution_or_import": False}
emit(folder / "PROVENIENCIA_EMISSOR_V2_REINSPECAO_087.json",
     (json.dumps(record, ensure_ascii=False, indent=2)+"\n").encode("utf-8"))
print(json.dumps({"new_helper": pin(dest), "provenance": pin(folder / "PROVENIENCIA_EMISSOR_V2_REINSPECAO_087.json")}, ensure_ascii=False))

