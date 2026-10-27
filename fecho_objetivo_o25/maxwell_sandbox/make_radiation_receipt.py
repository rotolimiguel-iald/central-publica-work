from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

root = Path(r"C:\IALD\Central de Patentes\work\fecho_objetivo_o25")
sandbox = root / "maxwell_sandbox"
source = sandbox / "MaxwellRadiationClosure.lean"
olean = sandbox / "MaxwellRadiationClosure.olean"
log = sandbox / "BUILD_RADIATION_CLOSURE.log"
text = log.read_text(encoding="utf-8")
required = [
    "realProfileStress_symmetricReflection_contrast",
    "momentumSmear_singleFiber",
    "momentumSmear_wave23_zero",
    "realProfileStress_symmetricReflection_conserved",
]
assert "sorryAx" not in text
assert "error:" not in text
assert all(name in text for name in required)
digest = lambda path: sha256(path.read_bytes()).hexdigest()
receipt = {
    "schema": "tgl.formal-receipt.v1",
    "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    "scope": "Longitudinally symmetrized free-streaming Maxwell radiation: conserved stress and exact screen-pressure contrast",
    "status": "COMPILED_NO_SORRY_AX",
    "sandbox": str(sandbox).replace("\\", "/"),
    "source": source.name,
    "source_sha256": digest(source),
    "olean_sha256": digest(olean),
    "build_log_sha256": digest(log),
    "lean_version": "4.31.0",
    "proved_items": required + [
        "regularProfile_momentumReflection",
        "regularProfile_add",
        "realProfileWave_symmetricReflection",
    ],
    "printed_axioms": ["propext", "Classical.choice", "Quot.sound"],
    "sorry_ax_present": False,
    "contrast": "T22 - T11 = Re((2F10)^2 + (2F21)^2 - (2F12)^2 - (2F13)^2 + (2F23)^2)",
    "interpretation": "The exact symmetrized radiation contrast is formally proved, including the previously omitted F13 term. A concrete nonzero anisotropic witness is not yet sealed in this receipt. This is not an experimental confirmation.",
    "canonical_kernel_modified": False,
    "production_modified": False,
    "public_mirror_modified": False,
}
out = root / "MAXWELL_RADIATION_CLOSURE_RECEIPT.json"
out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out)
print(receipt["source_sha256"])
print(receipt["olean_sha256"])
