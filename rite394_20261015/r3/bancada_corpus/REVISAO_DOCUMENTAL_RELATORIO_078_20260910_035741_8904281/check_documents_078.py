from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
from urllib.parse import unquote

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
MAIN = ROOT / "REEXAME_SUFICIENCIA_078_20260910"

def pin(path):
    data = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def new(path, data):
    if path.exists():
        raise RuntimeError(f"Existing destination: {path}")
    temp = path.with_name(path.name + ".pending")
    with temp.open("xb") as stream:
        stream.write(data)
    if not data or temp.read_bytes() != data:
        raise RuntimeError("Staging mismatch")
    temp.rename(path)
    if path.read_bytes() != data:
        raise RuntimeError("Final mismatch")

registry_path = ROOT / "REVISOES_RAIZ_078_20260910/REGISTRO_RAIZ_078.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
capture_path = MAIN / "ESTADO_CANONICO_078.json"
capture = json.loads(capture_path.read_text(encoding="utf-8"))
provenance_path = MAIN / "PROVENIENCIA_CAPTURE_CURRENT078.json"
provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
prior_path = ROOT / "REEXAME_SUFICIENCIA_077_20260910/ESTADO_CANONICO_077.json"
prior = json.loads(prior_path.read_text(encoding="utf-8"))
paths = [registry_path, capture_path, provenance_path, prior_path,
         Path(provenance["source"]["path"]), Path(provenance["new_helper"]["path"])]
paths += [Path(e["path"]) for e in registry["sources"] + registry["outputs"]]
paths += [ROOT / "REEXAME_SUFICIENCIA_077_20260910/REEXAME_SUFICIENCIA.md",
          ROOT / "COMPARACAO_LIM1_COEFICIENTES_078_20260910/MANIFESTO_LIM1_COEFICIENTES_078.json"]
paths = list(dict.fromkeys(p.resolve() for p in paths))
before = [pin(p) for p in paths]
new(BASE / "PINS_INICIAIS.json", json.dumps(before, ensure_ascii=False, indent=2).encode("utf-8"))

checks = []
def check(name, condition, detail=None):
    item = {"name": name, "passed": bool(condition)}
    if detail is not None:
        item["detail"] = detail
    checks.append(item)
    if not condition:
        raise RuntimeError(name)

for entry in registry["sources"] + registry["outputs"]:
    actual = pin(Path(entry["path"]))
    check("root_registry_pin:" + entry["path"], actual["bytes"] == entry["bytes"] and actual["sha256"] == entry["sha256"])

links = []
for path in paths:
    if path.suffix.lower() != ".md":
        continue
    body = path.read_text(encoding="utf-8")
    for match in re.finditer(r"\]\((?:<([^>]+)>|([^\)\n]+))\)", body):
        raw = (match.group(1) or match.group(2)).strip()
        if not re.match(r"^[A-Za-z]:[/\\]", raw):
            continue
        decoded = unquote(raw)
        line_number = None
        line_match = re.match(r"^(.*):(\d+)$", decoded)
        if line_match:
            decoded, line_number = line_match.group(1), int(line_match.group(2))
        target = Path(decoded)
        okay = target.is_file()
        if okay and line_number is not None:
            okay = 1 <= line_number <= len(target.read_text(encoding="utf-8-sig").splitlines())
        entry = {"from": path.as_posix(), "target": raw, "file_path": target.as_posix(), "line_number": line_number, "valid": okay}
        links.append(entry)
        check("link:" + str(len(links)), okay, entry)

for label in ("source", "new_helper"):
    expected = provenance[label]
    actual = pin(Path(expected["path"]))
    check("capture_provenance_pin:" + label, actual["bytes"] == expected["bytes"] and actual["sha256"] == expected["sha256"])
source_bytes = Path(provenance["source"]["path"]).read_bytes()
helper_bytes = Path(provenance["new_helper"]["path"]).read_bytes()
check("helper_exact_ordered_byte_replacements", source_bytes.replace(b"077", b"078").replace(b"076", b"077") == helper_bytes)
check("helper_replacement_counts", provenance["replacement_counts_in_original"] == {"077": source_bytes.count(b"077"), "076": source_bytes.count(b"076")})

prior_pins = {p["path"]: p for p in prior["pins"]}
capture_pins = {p["path"]: p for p in capture["pins"]}
comparisons = capture["comparison_with_delivery077"]
check("four_canonical_comparisons", len(comparisons) == 4)
for comparison in comparisons:
    path = comparison["path"]
    check("canonical_captured_pin_unchanged:" + path, comparison["unchanged"] is True and capture_pins[path] == prior_pins[path])
expected_prior = capture_pins[prior_path.as_posix()]
check("prior_capture_pin_current", pin(prior_path)["sha256"] == expected_prior["sha256"] and pin(prior_path)["bytes"] == expected_prior["bytes"])
check("module_inventory_98_unique", len(capture["modules"]) == len({m["module"] for m in capture["modules"]}) == 98)
check("present77_absent21", sum(m["present"] is True for m in capture["modules"]) == capture["present"] == 77 and [m["module"] for m in capture["modules"] if not m["present"]] == capture["absent"] and len(capture["absent"]) == 21)
check("embedded683_stable_seal_status", capture["embedded_files"] == 683 and capture["all_read_sources_unchanged"] is True and capture["seal_um_hash_matches"] is True)

receipt_paths = [ROOT / "CONTROLE_WEYL_PONTUAL_078_20260910/RESULTADO_WEYL_PONTUAL_078.json", ROOT / "CONTROLE_EINSTEIN_LINEARIZADO_078_20260910/RESULTADO_EINSTEIN_LINEARIZADO_078.json"]
counts = []
all_names = []
for path, count in zip(receipt_paths, (17, 105)):
    record = json.loads(path.read_text(encoding="utf-8"))
    check("receipt_count:" + path.name, len(record["checks"]) == record["checks_total"] == count and all(c["passed"] is True for c in record["checks"]))
    actual_code = pin(Path(record["source"]["path"]))
    check("receipt_source_pin:" + path.name, actual_code["bytes"] == record["source"]["bytes"] and actual_code["sha256"] == record["source"]["sha256"])
    counts.append(count)
    all_names += [c["name"] for c in record["checks"]]
check("122_unique_recorded_symbolic_checks", sum(counts) == len(all_names) == len(set(all_names)) == 122)
check("no_lean_no_um_no079_in_root_registry", registry["new_lean_compilations"] == 0 and registry["um_executed_or_imported"] is False and registry["stage079_included"] is False)

for expected in before:
    actual = pin(Path(expected["path"]))
    check("source_stable:" + expected["path"], actual["bytes"] == expected["bytes"] and actual["sha256"] == expected["sha256"])

result = {"created_utc": datetime.now(timezone.utc).isoformat(), "status": "PASS_DOCUMENTARY_CHECKS_ONLY", "sources": before,
          "checks": checks, "checks_total": len(checks), "links": links, "links_total": len(links),
          "line_anchors": sum(e["line_number"] is not None for e in links), "recorded_cas_counts": counts,
          "canonical_recaptured_in_this_documentary_review": False,
          "capture078_was_previously_executed_read_only_in_this_stage": True,
          "source_calculations_rerun": False, "um_executed_or_imported": False,
          "limits": "Documentary consistency and stored pins, not mathematical rerun, new canonical capture, or a Lean proof."}
target = BASE / "VERIFICACAO_DOCUMENTAL_078.json"
new(target, json.dumps(result, ensure_ascii=False, indent=2).encode("utf-8"))
print(json.dumps({"sources": len(before), "checks": len(checks), "links": len(links), "line_anchors": result["line_anchors"], "recorded_cas": sum(counts), "result": pin(target)}, ensure_ascii=False))
