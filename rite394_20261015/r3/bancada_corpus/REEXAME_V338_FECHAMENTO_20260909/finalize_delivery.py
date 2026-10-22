"""Publish new local delivery files only after checking completed build and audit receipts."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
COPY = ROOT / "COPIA_INTEGRADA_20260909_203352_868028"
PREP = ROOT / "INTEGRADOR_PRECISAO_METRICA_ACAO_20260909_201301_8584415"
BUILD = PREP / "BUILD_SUCCESSOR_20260909_203414_443930"
AUDIT = ROOT / "AUDITORIA_INTEGRACAO_93_V2_20260909_203946_6451878"
pins = {}

def read(p):
    raw = p.read_bytes()
    pins[str(p)] = {"path": str(p), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    return raw

def write_new(p, text):
    assert p.resolve().is_relative_to(ROOT) and not p.exists()
    raw = text.encode("utf-8")
    assert len(raw) > 0
    tmp = p.with_name(p.name + ".tmp_" + datetime.now().strftime("%H%M%S_%f"))
    with tmp.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(p)
    assert read(p) == raw

build = json.loads(read(BUILD / "TRANSPOSED_RESULT.json"))
audit = json.loads(read(AUDIT / "AUDITORIA_INTEGRACAO_93.json"))
integration = json.loads(read(COPY / "INTEGRATION_RESULT.json"))
config = json.loads(read(PREP / "CONFIG_93_CONFIRMADA_RAIZ.json"))
texts = json.loads(read(OUT / "DELIVERY_TEXTS.json"))
assert build["status"] == "PASS_TRANSPOSED_SCOPE"
assert len(build["runs"]) == 13 and all(r["exit_code"] == 0 and r["valid"] and r["warning_lines"] == 0 for r in build["runs"])
assert build["input_boundary_unchanged"] and build["cached_boundary_unchanged"] and not build["um_py_executed"]
assert audit["status"] == "PASS_STATIC_INTEGRATION_SCOPE" and not audit["failed_checks"]
assert audit["counts"]["checks"] == audit["counts"]["passed_checks"] == 2191
assert audit["counts"]["modules"] == 93 and audit["counts"]["total"] == 1638
assert integration["declaration_counts"] == {"modules": 10, "theorems": 108, "other_declarations": 24, "local_instances": 0, "total": 132}
read(COPY / "um.py")
assert pins[str(COPY / "um.py")]["sha256"] == integration["integrated_copy"]["sha256"]
for item in config["modules"]:
    for pkey, hkey in (("source", "sha256"), ("build_result", "build_result_sha256")):
        p = Path(item[pkey])
        read(p)
        assert pins[str(p)]["sha256"] == item[hkey]
for p in (
    OUT / "RECEIPT_V338.json", OUT / "RECEIPT_FORMAL_SOURCES_V338.json",
    OUT / "NOTA_CAPTURAS_E_ESCOPO.md", OUT / "audit_snapshot.py", OUT / "audit_formal_sources.py",
    Path(__file__), BUILD / "BUILD_PLAN.json", COPY / "CONFIG_APROVADA.json",
    AUDIT / "RELATORIO_INTEGRACAO_93.md", AUDIT / "PROVENIENCIA_CORRECAO_HISTORICA.json",
    ROOT / "HABITANTE_CURVO_SIGMA_20260909_202000" / "HABITANTE_CURVO_SIGMA_E_AREA.md",
    ROOT / "HABITANTE_CURVO_SIGMA_20260909_202000" / "MANIFESTO_HABITANTE_CURVO.json",
    ROOT / "HABITANTE_CURVO_SIGMA_20260909_202000" / "VERIFICACAO_SIMBOLICA.json",
    ROOT / "REPRESENTACAO_FISHER_LORENTZ_LOCAL_20260909_202637_1088578" / "NOTA_REPRESENTACAO_LOCAL.md",
    ROOT / "CONSERVACAO_SIGMA_AGREGADA_20260909_202331_958482" / "ENTREGA_CONSERVACAO_SIGMA.md",
    ROOT / "CONSERVACAO_SIGMA_AGREGADA_20260909_202331_958482" / "MANIFESTO_CONSERVACAO_SIGMA.json",
    ROOT / "REVISAO_ERRO_GIBBS_20260909_201100" / "ANALISE_SEMANTICA_PROPRIA.md",
):
    read(p)
report = OUT / "REEXAME_V338.md"
handoff = ROOT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_065_ESPONTANEA_metrica_sigma_precisao_reexame_v338.md"
manifest_path = OUT / "MANIFESTO_ENTREGA_065.json"
assert all(not p.exists() for p in (report, handoff, manifest_path))
for path, pin in pins.items():
    raw = Path(path).read_bytes()
    assert len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"], path
write_new(report, texts["report"])
write_new(handoff, texts["handoff"])
manifest = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "DELIVERY_065_COMPLETED__SCOPED_PROOFS_AND_REEXAM__GENERAL_GOAL_OPEN",
    "canonical_observation": audit["current_canonical"],
    "working_copy": pins[str(COPY / "um.py")],
    "delta": integration["declaration_counts"], "accumulated": audit["counts"],
    "compiled_runs": len(build["runs"]),
    "build_status": build["status"], "static_audit_status": audit["status"],
    "written_proofs_not_in_Lean_count": ["curved categorical Einstein-sigma inhabitant and local area", "local general Fisher-reflected representation using Nash"],
    "general_goal_remaining": ["joint general correspondence of selected data, matter and area", "coupled quantum gravitational sector, anomalies and claimed UV route", "global and finite-precision scope when claimed"],
    "originals_written": False, "um_executed_or_imported": False, "nature_tests_run": False,
    "source_pins": list(pins.values()),
}
write_new(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": manifest["status"], "report": pins[str(report)], "handoff": pins[str(handoff)], "manifest": pins[str(manifest_path)], "working_copy": manifest["working_copy"]}, ensure_ascii=False, indent=2))
