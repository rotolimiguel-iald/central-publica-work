"""Read-only comparison of canonical um.py and the delivered copy; never imports either."""
import ast
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
OUT = Path(__file__).resolve().parent
CANON = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
COPY = ROOT / "COPIA_INTEGRADA_20260909_192248_937671" / "um.py"
BUILD = ROOT / "INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394" / "BUILD_SUCCESSOR_20260909_192313_320129"
pins = {}

def read(path):
    data = path.read_bytes()
    pins[str(path)] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    return data

def table(data):
    tree = ast.parse(data.decode("utf-8-sig"))
    candidates = [node for node in tree.body if isinstance(node, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in node.targets)]
    assert len(candidates) == 1
    result = ast.literal_eval(candidates[0].value)
    assert isinstance(result, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in result.items())
    return result

def write_new(path, data):
    assert path.resolve().is_relative_to(ROOT.resolve())
    assert not path.exists()
    tmp = path.with_name(path.name + ".tmp_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    with tmp.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    assert tmp.read_bytes() == data and len(data) > 0
    tmp.rename(path)
    assert path.read_bytes() == data

canonical = table(read(CANON / "um.py"))
delivered = table(read(COPY))
seal = json.loads(read(CANON / "um_absoluto_selo.json"))
run_text = read(CANON / "rodada_v337_stdout.txt").decode("utf-8-sig")
index_text = read(ROOT.parent / "memory" / "TGL_INDICE_VIVO.md").decode("utf-8-sig")
atlas_text = read(ROOT.parent / "memory" / "TGL_ATLAS.md").decode("utf-8-sig")
plan = json.loads(read(BUILD / "BUILD_PLAN.json"))
build_receipt = json.loads(read(BUILD / "TRANSPOSED_RESULT.json"))
static = json.loads(read(ROOT / "AUDITORIA_INTEGRACAO_83_20260909" / "AUDITORIA_INTEGRACAO_83.json"))
read(ROOT / "ESTABILIDADE_CARATER_GLOBAL_20260909_193729_5618013" / "NOTA_ESTABILIDADE_CARATER_GLOBAL.md")
read(ROOT / "NOTA_ESPECTRO_MODULAR_20260909_192614_296855" / "NOTA_ESPECTRO_MODULAR.md")
read(OUT / "audit_current.py")

module_rows = [{"module": m["module"], "key": m["key"],
                "in_canonical": m["key"] in canonical,
                "in_delivered": m["key"] in delivered} for m in plan["modules"]]
added = sorted(set(delivered) - set(canonical))
removed = sorted(set(canonical) - set(delivered))
changed = sorted(k for k in set(canonical) & set(delivered) if canonical[k] != delivered[k])
selected_seal_keys = ["timestamp", "qg_closure_verdict", "renormalization_wall_verdict",
                      "dephasing_reach_verdict", "linearized_spin2_sector_proved",
                      "fail_closed_selftest", "rite_checkpoints"]
result = {
    "status": "READ_ONLY_REEXAM_COMPLETED__NO_NEW_RUNTIME_OR_LEAN_BUILD",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Canonical v337 and already delivered copy83; no claim to have located an unpublished sister-session version.",
    "canonical_embedded_files": len(canonical),
    "delivered_embedded_files": len(delivered),
    "added_files": added, "removed_files": removed, "changed_existing_files": changed,
    "delivered_module_count": len(module_rows),
    "delivered_modules_absent_canonical": sum(not m["in_canonical"] for m in module_rows),
    "module_presence": module_rows,
    "seal_excerpt": {k: seal[k] for k in selected_seal_keys if k in seal},
    "recorded_canonical_run": [line for line in run_text.splitlines()
        if "teoremas limpos: 4241/4241" in line or "rite_checkpoints:" in line
        or ">>> FAIL_CLOSED_SELFTEST_PASSED <<<" in line],
    "canonical_run_was_executed_here": False,
    "delivered_prior_build": {"status": build_receipt["status"], "runs": [
        {k: r.get(k) for k in ["module", "exit_code", "valid", "warning_lines"]}
        for r in build_receipt["runs"]]},
    "delivered_prior_static_audit": {"status": static["status"], "counts": static["counts"]},
    "navigation_discrepancy": {
        "index_mentions_latest_complete_v320": "última COMPLETA custodiada | v320" in index_text,
        "atlas_latest_entry_mentions_complete_v336": "ultima COMPLETA custodiada e a v336" in atlas_text,
        "interpretation": "The index contains a stale historical reference; neither statement is a new complete run."
    },
    "source_pins": pins,
}
assert len(module_rows) == 83 and len(added) == 83 and not removed
assert all(not m["in_canonical"] and m["in_delivered"] for m in module_rows)
assert len(build_receipt["runs"]) == 9
assert all(r["exit_code"] == 0 and r["valid"] and r["warning_lines"] == 0 for r in build_receipt["runs"])
for path, pin in pins.items():
    data = Path(path).read_bytes()
    assert len(data) == pin["bytes"] and hashlib.sha256(data).hexdigest() == pin["sha256"], path
result["all_read_sources_unchanged_at_end"] = True
destination = OUT / "RECEIPT_CURRENT.json"
write_new(destination, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"receipt": str(destination), "canonical_files": len(canonical),
                 "copy_files": len(delivered), "modules_not_incorporated": len(added),
                 "changed_existing": changed, "prior_static_counts": static["counts"],
                 "canonical_recorded_run": result["recorded_canonical_run"]}, ensure_ascii=False))
