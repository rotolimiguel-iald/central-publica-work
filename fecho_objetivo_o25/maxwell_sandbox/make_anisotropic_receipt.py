from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

root = Path(r"C:\IALD\Central de Patentes\work\fecho_objetivo_o25")
sandbox = root / "maxwell_sandbox"
digest = lambda path: sha256(path.read_bytes()).hexdigest()
closure = json.loads((root / "MAXWELL_RADIATION_CLOSURE_RECEIPT.json").read_text(encoding="utf-8"))
assert digest(sandbox / "MaxwellRadiationClosure.lean") == closure["source_sha256"]
logs = {}
for name in ["MaxwellScreenReflection", "MaxwellRadiationWitness"]:
    log = sandbox / f"BUILD_{'SCREEN_REFLECTION' if name == 'MaxwellScreenReflection' else 'RADIATION_WITNESS'}.log"
    text = log.read_text(encoding="utf-8")
    assert "sorryAx" not in text
    assert "error:" not in text
    logs[name] = log
required = [
    "screenReflection_measurePreserving",
    "realProfileWave_screenSymmetric",
    "screenSymmetric_singleFiber",
    "exists_tensor01_radiation_witness",
    "tensor01_fullySymmetric_pressure_contrast_pos",
    "fullySymmetrizedProfile_regular",
    "fullySymmetrized_stress_conserved",
    "exists_fullySymmetric_anisotropic_radiation",
]
combined_logs = logs["MaxwellScreenReflection"].read_text(encoding="utf-8") + logs["MaxwellRadiationWitness"].read_text(encoding="utf-8")
assert all(name in combined_logs for name in required)
sources = {}
for name in ["MaxwellScreenReflection", "MaxwellRadiationWitness"]:
    source = sandbox / f"{name}.lean"
    olean = sandbox / f"{name}.olean"
    sources[name] = {
        "source_sha256": digest(source),
        "olean_sha256": digest(olean),
        "build_log_sha256": digest(logs[name]),
    }
receipt = {
    "schema": "tgl.formal-receipt.v1",
    "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    "scope": "Concrete conserved free-streaming Maxwell radiation with strictly positive screen-pressure anisotropy",
    "status": "COMPILED_NO_SORRY_AX",
    "sandbox": str(sandbox).replace("\\", "/"),
    "lean_version": "4.31.0",
    "depends_on_receipts": ["MAXWELL_RADIATION_CLOSURE_RECEIPT.json"],
    "sources": sources,
    "proved_items": required,
    "printed_axioms": ["propext", "Classical.choice", "Quot.sound"],
    "sorry_ax_present": False,
    "construction": "Explicit compact-support smooth tensor01 Schwartz witness, symmetrized in the transverse screen and then longitudinally",
    "anisotropy": "T22 - T11 = Re((2F10)^2) > 0 after exact F13 screen-parity cancellation, F23=0, and F21/F12 antisymmetric cancellation",
    "p1_substep": "FREE_STREAMING_ANISOTROPIC_REALIZATION_PROVED",
    "tgl_s_selection_derived": False,
    "tgl_l_excluded": False,
    "interpretation": "A nonzero anisotropic free-streaming Maxwell sector is formally inhabited and conserved. Existence of this realization does not derive the cosmological TGL-S selection, exclude TGL-L, freeze Neff, or provide experimental confirmation.",
    "canonical_kernel_modified": False,
    "production_modified": False,
    "public_mirror_modified": False,
}
out = root / "MAXWELL_ANISOTROPIC_RADIATION_RECEIPT.json"
out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out)
for name, item in sources.items():
    print(name, item["source_sha256"], item["olean_sha256"])
