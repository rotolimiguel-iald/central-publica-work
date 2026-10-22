from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
ORIGIN = BASE / "ERRO_RECONSTRUCAO_FINITA_20260909"

def pin(p):
    b = p.read_bytes()
    return {"path": p.as_posix(), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}

def new(p, b):
    assert p.resolve().is_relative_to(OUT) and not p.exists()
    t = p.with_name(p.name + ".tmp")
    with t.open("xb") as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    assert t.read_bytes() == b
    os.rename(t, p)
    assert p.read_bytes() == b

copies = []
for name in ["build_source.py", "CONFIG_BUILD.json"]:
    source = ORIGIN / name
    before = pin(source)
    raw = source.read_bytes()
    new(OUT / name, raw)
    assert pin(source) == before
    copies.append({"source": before, "copy": pin(OUT / name), "byte_identical": True})
new(OUT / "BUILDER_PROVENANCE.json", (json.dumps({"created_utc": datetime.now(timezone.utc).isoformat(),
    "copies": copies, "scope": "Approved builder83 copied byte for byte; no compiler or um.py executed by setup."},
    ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps(copies))
