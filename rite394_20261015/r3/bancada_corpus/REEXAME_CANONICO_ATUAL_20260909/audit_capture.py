"""Verify recorded capture hashes using the serialization domain in um.py; read only."""
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

base = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
out = Path(__file__).resolve().parent / "RECEIPT_CAPTURE.json"
assert not out.exists()
manifest_bytes = (base / "tgl_kernel_proof_manifest.json").read_bytes()
manifest = json.loads(manifest_bytes)
rows = []
for kind in ("build", "audit"):
    path = base / f"tgl_kernel_{kind}_capture.txt"
    raw = path.read_bytes()
    # The canonical writer uses text mode: normalize CRLF before recovering stdout.
    text = raw.decode("utf-8").replace("\r\n", "\n")
    head, sep, body = text.partition("--- STDOUT ---\n")
    assert sep
    stdout, sep, stderr = body.rpartition("\n--- STDERR ---\n")
    assert sep and stderr.endswith("\n")
    stderr = stderr[:-1]
    lengths = re.search(r"# len\(stdout\)=(\d+) len\(stderr\)=(\d+)", head)
    assert lengths and len(stdout) == int(lengths[1]) and len(stderr) == int(lengths[2])
    actual = hashlib.sha256(stdout.encode("utf-8")).hexdigest()
    rows.append({"path": str(path), "raw_bytes": len(raw),
                 "raw_sha256": hashlib.sha256(raw).hexdigest(),
                 "returncode": int(re.search(r"# returncode: (-?\d+)", head)[1]),
                 "stdout_characters": len(stdout), "stderr_characters": len(stderr),
                 "stdout_sha256": actual,
                 "manifest_stdout_sha256": manifest[f"{kind}_stdout_sha256"],
                 "matches_manifest": actual == manifest[f"{kind}_stdout_sha256"],
                 "warning_lines": len(re.findall(r"^warning:", stdout, re.M))})
result = {"created_utc": datetime.now(timezone.utc).isoformat(),
          "status": "CURRENT_BUILD_CAPTURE_DOES_NOT_MATCH_MANIFEST__AUDIT_CAPTURE_MATCHES",
          "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
          "interpretation": "A provenance discrepancy, not proof of a failed build or false theorem; no causal explanation established.",
          "rows": rows, "no_original_written": True, "no_um_executed_or_imported": True}
assert not rows[0]["matches_manifest"] and rows[1]["matches_manifest"]
assert all(r["returncode"] == 0 for r in rows)
data = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
temp = out.with_suffix(".json.tmp_" + datetime.now().strftime("%H%M%S_%f"))
with temp.open("xb") as handle:
    handle.write(data)
    handle.flush()
    os.fsync(handle.fileno())
assert temp.read_bytes() == data
temp.rename(out)
assert out.read_bytes() == data
print(json.dumps(result, ensure_ascii=False))
