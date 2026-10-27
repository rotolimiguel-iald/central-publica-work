from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

root = Path(r"C:\IALD\Central de Patentes\work\fecho_objetivo_o25")
sandbox = root / "maxwell_sandbox"
digest = lambda path: sha256(path.read_bytes()).hexdigest()
parent = json.loads((root / "MAXWELL_ANISOTROPIC_RADIATION_RECEIPT.json").read_text(encoding="utf-8"))
for name, hashes in parent["sources"].items():
    assert digest(sandbox / f"{name}.lean") == hashes["source_sha256"]
source = sandbox / "MaxwellRadiationSelection.lean"
olean = sandbox / "MaxwellRadiationSelection.olean"
log = sandbox / "BUILD_RADIATION_SELECTION.log"
text = log.read_text(encoding="utf-8")
assert "sorryAx" not in text
assert "error:" not in text
required = ["universalPerfectFluidScreenClosure_impossible", "tensor01_not_perfectFluidScreen"]
assert all(name in text for name in required)
receipt = {
    "schema": "tgl.formal-receipt.v1",
    "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    "scope": "Selection of the general free-streaming radiation closure in the realized Maxwell dynamics",
    "status": "COMPILED_NO_SORRY_AX",
    "sandbox": str(sandbox).replace("\\", "/"),
    "source": source.name,
    "source_sha256": digest(source),
    "olean_sha256": digest(olean),
    "build_log_sha256": digest(log),
    "lean_version": "4.31.0",
    "depends_on_receipts": ["MAXWELL_ANISOTROPIC_RADIATION_RECEIPT.json"],
    "proved_items": required,
    "printed_axioms": ["propext", "Classical.choice", "Quot.sound"],
    "sorry_ax_present": False,
    "universal_tgl_l_screen_closure_excluded": True,
    "general_free_streaming_closure_selected": True,
    "special_isotropic_states_excluded": False,
    "cosmological_neff_protocol_frozen": False,
    "interpretation": "A universal perfect-fluid screen closure is incompatible with the realized regular Maxwell radiation dynamics. The general closure must permit free-streaming anisotropic response. This does not claim that special isotropic states are impossible, nor does it by itself freeze or experimentally confirm Neff.",
    "canonical_kernel_modified": False,
    "production_modified": False,
    "public_mirror_modified": False,
}
out = root / "TGL_RADIATION_SELECTION_RECEIPT.json"
out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out)
print(receipt["source_sha256"])
print(receipt["olean_sha256"])
