"""Read-only source measurement and exclusive creation of this review manifest."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "RENORMALIZACAO_SIGMA_EFT_20260909"
assert ROOT.name == "REVISAO_FONTE_QUARTICA_20260909_221154"
assert ROOT.parent.name == "Chatgpt"

def measure(path):
    data = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(data), "lines": len(data.decode("utf-8-sig").splitlines()), "sha256": hashlib.sha256(data).hexdigest()}

receipt_path = SOURCE / "VERIFICACAO_FONTE_QUARTICA.json"
receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
script_path = Path(receipt["source"]["path"])
inputs = [SOURCE / "FONTE_QUARTICA_E_HABITANTE_CORRIGIDO.md", receipt_path, script_path]
records = [measure(path) for path in inputs]
checks = receipt["checks"]
manifest = {
    "measured_at_utc": datetime.now(timezone.utc).isoformat(),
    "authorship": "Independent written mathematical analysis by this session; no attribution of approval to another party.",
    "status": "DERIVED_WRITTEN_REVIEW__NO_NEW_CAS_OR_LEAN",
    "inputs": records,
    "existing_receipt_observations": {
        "declared_status": receipt["status"],
        "declared_count": receipt["check_count"],
        "observed_count": len(checks),
        "all_passed_flags": all(item["passed"] for item in checks),
        "all_zero_residual_strings": all(item["residual"] == "0" for item in checks),
        "script_hash_matches_receipt": records[-1]["sha256"] == receipt["source"]["sha256"],
        "script_bytes_match_receipt": records[-1]["bytes"] == receipt["source"]["bytes"],
        "rerun_by_this_review": False,
    },
    "new_artifacts": [measure(ROOT / "REVISAO_VARIACIONAL_E_FRIEDMANN.md"), measure(Path(__file__).resolve())],
    "unchanged_during_measurement": all(measure(path)["sha256"] == record["sha256"] for path, record in zip(inputs, records)),
    "scope_limits": ["classical truncated ambient action", "finite Lorentzian coefficients are inputs", "no complete quantum stress", "no corrected-background Hadamard construction", "no UV/bounce claim", "probability representation theorem not rederived"],
    "um_executed_or_imported": False,
    "originals_modified": False,
}
output = ROOT / "MANIFESTO_REVISAO_FONTE_QUARTICA.json"
temp = ROOT / "MANIFESTO_REVISAO_FONTE_QUARTICA.json.new"
assert not output.exists() and not temp.exists()
data = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with temp.open("xb") as stream:
    stream.write(data)
assert temp.read_bytes() == data and len(data) > 1000
temp.rename(output)
print(json.dumps({"manifest": measure(output), "review": manifest["new_artifacts"][0], "receipt_observations": manifest["existing_receipt_observations"], "unchanged": manifest["unchanged_during_measurement"]}, ensure_ascii=False, indent=2))
