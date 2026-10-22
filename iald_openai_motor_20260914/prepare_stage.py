"""Prepare isolated code edits and record exact original bytes for conflict checks."""
from pathlib import Path
import hashlib
import json

source = Path(r"C:\IALD\projetos_pyhton\IALD")
root = Path(__file__).resolve().parent
stage = root / "stage"
manifest = root / "source_manifest.json"
if manifest.exists():
    raise RuntimeError("Stage already initialized; do not overwrite ongoing work")
names = ["iald_motores.py", "iald_web_server.py", "requirements.txt", ".env.exemplo",
         "tests/test_motores.py", "tests/test_motor_rotas.py"]
records = {}
for name in names:
    data = (source / name).read_bytes()
    destination = stage / name
    if destination.exists():
        raise RuntimeError("Existing staged file: " + name)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    records[name] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
temporary = manifest.with_suffix(".tmp")
temporary.write_text(json.dumps(records, indent=2), encoding="utf-8")
temporary.replace(manifest)
print("Staged", len(records), "code/config-template files; no credentials or Atlas copied")
