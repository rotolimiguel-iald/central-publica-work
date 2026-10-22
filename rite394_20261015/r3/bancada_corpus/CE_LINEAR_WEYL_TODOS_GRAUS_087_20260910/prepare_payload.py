from pathlib import Path
from datetime import datetime, timezone
import os

root = Path(__file__).resolve().parent
changes = {"NOTE.payload.md": [("COC ADEIAS", "COCADEIAS")], "emit_note.py": [('"não calcula"', '"Não se calcula"')]}
for name, replacements in changes.items():
    path = root / name
    original = path.read_bytes()
    updated = original.decode("utf-8")
    for old, new in replacements:
        assert old in updated
        updated = updated.replace(old, new)
    data = updated.encode("utf-8")
    backup = path.with_name(path.name + ".bak_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    with backup.open("xb") as stream:
        stream.write(original)
    assert backup.read_bytes() == original
    temp = path.with_name(path.name + ".tmp_edit")
    with temp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == data
    os.replace(temp, path)
    assert path.read_bytes() == data
print("Prepared two new, not-yet-published own inputs; byte backups retained.")
