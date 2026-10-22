from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent

def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

before = json.loads((BASE / "PINS_INICIAIS.json").read_text(encoding="utf-8"))
after = []
for expected in before:
    actual = pin(Path(expected["path"]))
    actual["unchanged"] = actual["bytes"] == expected["bytes"] and actual["sha256"] == expected["sha256"]
    if not actual["unchanged"]:
        raise RuntimeError(f"Changed source: {actual['path']}")
    after.append(actual)

note = BASE / "PARECER_CERTIFICADO_A6_078.md"
links = re.findall(r"\]\(<(C:/[^>]+)>\)", note.read_text(encoding="utf-8"))
for target in links:
    if not Path(target).is_file():
        raise RuntimeError(f"Missing linked source: {target}")

manifest = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "author": "/root/finish_gibbs_realization",
    "status": "DERIVED_INDEPENDENT_REVIEW_NO_MATERIAL_ERROR_FOUND_IN_STATED_SCOPE",
    "source_pins_after": after,
    "new_artifacts": [pin(note), pin(BASE / "PINS_INICIAIS.json"), pin(Path(__file__))],
    "local_links_verified": links,
    "analytical_checks": [
        "Coordinate order tau,x,y,z with z spacelike; positive Lambda in stated Ricci convention",
        "ODE fundamental solutions and Wronskian k^3 z^2",
        "All components of linearized Einstein equation and sigma decoupling at constant phi0",
        "Four Weyl-form squares, trace signs and -4k/z0 coefficient",
        "Exact Killing fields and evaluation of all prolonged s0 generators including antifields",
        "Non-exact A6 and obstruction for the specific H3(C5) class only"
    ],
    "primary_reference_checked": {"url": "https://arxiv.org/pdf/1801.03178", "scope": "Section2 conformal geometry; concrete sign independently calculated"},
    "preliminary_interpretation_correction": "My earlier sign reservation treated z as timelike. The source uses spacelike z; no change to its Ricci convention is needed.",
    "source_scripts_executed": False,
    "um_executed_or_imported": False,
    "lean_or_cas_executed": False,
    "originals_written": False,
    "limits": "No assertion about all classes with the same leader, full BRST anomaly, ML of Einstein-sigma, QME or UV. No approval attributed to others."
}
dest = BASE / "MANIFESTO_REVISAO_A6_078.json"
temp = dest.with_name(dest.name + ".pending")
data = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")
if dest.exists():
    raise RuntimeError("Existing manifest")
with temp.open("xb") as stream:
    stream.write(data)
if not data or temp.read_bytes() != data:
    raise RuntimeError("Write mismatch")
temp.rename(dest)
if dest.read_bytes() != data:
    raise RuntimeError("Final byte mismatch")
print(json.dumps({"note": pin(note), "manifest": pin(dest), "sources_unchanged": len(after), "links": len(links)}, ensure_ascii=False))
