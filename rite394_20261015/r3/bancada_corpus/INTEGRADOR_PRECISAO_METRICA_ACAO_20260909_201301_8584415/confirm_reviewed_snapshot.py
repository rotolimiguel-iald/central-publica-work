"""Record the primary task's completed source review in a new configuration only."""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
assert len(sys.argv) == 3
source, target = map(lambda s: Path(s).resolve(), sys.argv[1:])
assert source.is_relative_to(ROOT) and target.is_relative_to(ROOT) and not target.exists()
raw = source.read_bytes()
config = json.loads(raw)
assert config["root_confirmed"] is False
pin_checks = []
for item in config["modules"]:
    for path_key, hash_key in (("source", "sha256"), ("build_result", "build_result_sha256")):
        p = Path(item[path_key]).resolve()
        data = p.read_bytes()
        assert hashlib.sha256(data).hexdigest() == item[hash_key], str(p)
        pin_checks.append({"path": str(p), "bytes": len(data), "sha256": item[hash_key]})
    receipt = json.loads(Path(item["build_result"]).read_bytes())
    assert receipt["status"] == "PASS_COMPILED_SCOPE"
assert hashlib.sha256(Path(config["source_um"]).read_bytes()).hexdigest() == config["source_um_sha256"]
config["root_confirmed"] = True
config["approval_basis"] = (
    "Primary task reviewed the mathematical source contracts and frozen leaf receipts, "
    "including all conditional area, wave, regularity and signature hypotheses. "
    "This is the primary task's own review, not user, external scientific or independent-agent approval. "
    "Authorized scope: additive new Chatgpt copy, joint Lean verification and report only. "
    "Canonical v338 is not this prototype's base; only deltas may be ported by its coding task.")
config["primary_review_utc"] = datetime.now(timezone.utc).isoformat()
config["unconfirmed_configuration"] = {"path": str(source), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
config["primary_review_pins"] = pin_checks
data = (json.dumps(config, ensure_ascii=False, indent=2) + "\n").encode()
tmp = target.with_suffix(".json.tmp_" + datetime.now().strftime("%H%M%S_%f"))
with tmp.open("xb") as handle:
    handle.write(data)
    handle.flush()
    os.fsync(handle.fileno())
assert tmp.read_bytes() == data and data
tmp.rename(target)
assert target.read_bytes() == data and source.read_bytes() == raw
print(json.dumps({"configuration": str(target), "modules": len(config["modules"]), "sha256": hashlib.sha256(data).hexdigest()}))
