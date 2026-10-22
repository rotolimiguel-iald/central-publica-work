from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent

def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

before = json.loads((BASE / "PINS_INICIAIS.json").read_text(encoding="utf-8"))
after = []
receipts = []
for expected in before:
    path = Path(expected["path"])
    actual = pin(path)
    actual["unchanged"] = actual["sha256"] == expected["sha256"] and actual["bytes"] == expected["bytes"]
    if not actual["unchanged"]:
        raise RuntimeError(f"Changed source: {path}")
    after.append(actual)
    if path.name.startswith("RESULTADO_"):
        record = json.loads(path.read_text(encoding="utf-8"))
        entries = record["checks"]
        actual_code = pin(Path(record["source"]["path"]))
        entry = {
            "path": str(path), "entries": len(entries),
            "true_entries": sum(c["passed"] is True for c in entries),
            "unique_names": len({c["name"] for c in entries}),
            "declared_count_matches": len(entries) == record["checks_total"],
            "code_bytes_match": actual_code["bytes"] == record["source"]["bytes"],
            "code_hash_matches": actual_code["sha256"] == record["source"]["sha256"],
        }
        if entry["entries"] != entry["true_entries"] or entry["entries"] != entry["unique_names"] or not all(entry[k] for k in ["declared_count_matches", "code_bytes_match", "code_hash_matches"]):
            raise RuntimeError("Receipt mismatch")
        if "inputs" in record:
            entry["input_pins_match_now"] = all(pin(Path(p["path"]))["sha256"] == p["sha256"] and pin(Path(p["path"]))["bytes"] == p["bytes"] for p in record["inputs"])
            if not entry["input_pins_match_now"]:
                raise RuntimeError("Receipt input mismatch")
        receipts.append(entry)

note = BASE / "PARECER_CODIGOS_E_RECIBOS_078.md"
links = re.findall(r"\]\(<(C:/[^>]+)>\)", note.read_text(encoding="utf-8"))
if not all(Path(link).is_file() for link in links):
    raise RuntimeError("Missing local link")
manifest = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "author": "/root/finish_gibbs_realization",
    "status": "DERIVED_STATIC_REVIEW_NO_MATERIAL_IMPLEMENTATION_ERROR_FOUND_WITHIN_DECLARED_SCOPE",
    "source_pins_after": after,
    "new_artifacts": [pin(note), pin(BASE / "PINS_INICIAIS.json"), pin(Path(__file__))],
    "receipt_documentary_checks": receipts,
    "total_true_entries_recorded": sum(r["true_entries"] for r in receipts),
    "local_links_verified": links,
    "custody_precision": "Einstein code captures its variable before after symbolic computations. Its input_sources_unchanged covers receipt emission, not the full preceding computation interval.",
    "source_scripts_executed_or_imported": False,
    "sympy_executed_or_imported": False,
    "lean_or_um_executed_or_imported": False,
    "originals_written": False,
    "limits": "Static source and receipt review, not an independent CAS run. Written BRST proof remains separate; no conclusion about every lift, QME or UV."
}
target = BASE / "MANIFESTO_REVISAO_ESTATICA_078.json"
temporary = target.with_name(target.name + ".pending")
data = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")
if target.exists():
    raise RuntimeError("Existing destination")
with temporary.open("xb") as stream:
    stream.write(data)
if temporary.read_bytes() != data or not data:
    raise RuntimeError("Staging mismatch")
temporary.rename(target)
if target.read_bytes() != data:
    raise RuntimeError("Final mismatch")
print(json.dumps({"note": pin(note), "manifest": pin(target), "sources_unchanged": len(after), "recorded_true_entries": manifest["total_true_entries_recorded"], "links": len(links)}, ensure_ascii=False))
