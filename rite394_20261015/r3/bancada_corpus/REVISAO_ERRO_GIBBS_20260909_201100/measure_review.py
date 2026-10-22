"""Read sources and prior receipts only; record this review without running Lean or um.py."""
from pathlib import Path
import datetime, hashlib, json, os, re

ROOT = Path(__file__).resolve().parent
BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
SOURCES = BASE / "ERRO_RECONSTRUCAO_FINITA_20260909"
LIB = BASE / "INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394" / "BUILD_SUCCESSOR_20260909_192313_320129"
specs = [
    ("FiniteResponseErrorBounds", "BUILD_20260909_195624_030733"),
    ("MixedGibbsFiniteAccuracy", "BUILD_20260909_200412_567584"),
    ("GibbsSamplingWindow", "BUILD_20260909_201028_081251"),
]

def rec(path):
    data = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def new(path, data):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    assert temporary.read_bytes() == data
    os.rename(temporary, path)
    assert path.read_bytes() == data

records = []
inputs = []
for module, name in specs:
    source = SOURCES / (module + ".lean")
    build = SOURCES / name
    receipt_path = build / "BUILD_RESULT.json"
    receipt = json.loads(receipt_path.read_bytes())
    assert receipt["status"] == "PASS_COMPILED_SCOPE"
    assert receipt["sources"] == [rec(source)]
    assert source.read_bytes() == (build / source.name).read_bytes()
    assert receipt["boundary_unchanged"]
    assert len(receipt["runs"]) == 2 and all(r["exit_code"] == 0 for r in receipt["runs"])
    rows = receipt["axiom_rows"]
    assert all(set(row["axioms"]) <= {"propext", "Classical.choice", "Quot.sound"} for row in rows)
    logs = [build / (r["module"] + ".log") for r in receipt["runs"]]
    warnings = sum("warning:" in line for log in logs for line in log.read_text(encoding="utf-8").splitlines())
    assert warnings == 0
    anchors = [{"line": n, "name": m.group(2), "kind": m.group(1)}
               for n, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1)
               if (m := re.match(r"^(def|theorem) (\w+)", line))]
    assert len(anchors) == len(rows)
    inputs.extend([source, receipt_path, build / source.name] + logs)
    records.append({"module": module, "source": rec(source), "receipt": rec(receipt_path),
                    "theorems": receipt["theorems"], "definitions": receipt["definitions"],
                    "axiom_rows": len(rows), "warnings": warnings,
                    "source_equals_receipted_build": True, "logs": [rec(log) for log in logs],
                    "declaration_lines": anchors})

dependencies = [LIB / "TGLExt" / name for name in [
    "FiniteResponseReconstruction.lean", "GeneralSourceResponseReconstruction.lean",
    "ProbeResponseRecord.lean", "MixedGibbsGravitationalBridge.lean",
]]
dependencies.append(Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\packages\mathlib\Mathlib\Analysis\Calculus\Taylor.lean"))
inputs.extend(dependencies)
before = [rec(path) for path in inputs]
note = ROOT / "ANALISE_SEMANTICA_PROPRIA.md"
manifest = {
    "status": "SEMANTIC_REVIEW_RECORDED__THREE_PRIOR_PASS_RECEIPTS_MATCH_CURRENT_SOURCES",
    "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "review_note": rec(note), "measurement_script": rec(Path(__file__).resolve()),
    "modules": records, "consulted_dependencies": [rec(path) for path in dependencies],
    "totals": {"theorems": sum(r["theorems"] for r in records),
               "definitions": sum(r["definitions"] for r in records),
               "axiom_rows": sum(r["axiom_rows"] for r in records), "warnings": 0},
    "own_analysis": {
        "coefficient_3delta_over_2": "Correct for the given ten-probe component decoder.",
        "coefficient_16B_epsilon": "Correct: 16 trace-product summands in dimension four.",
        "coefficient_1_plus_8GB": "Correct for fixed g and gInv; no curvature or metric-error stability claimed.",
        "normalization": "Response divided by negative pi; absolute error divided by positive pi.",
        "gibbs_sign": "Negative entropy response agrees with mixed Gibbs derivative and normalized positive quadratic source.",
        "Taylor_C": "Existence derived from smooth mixed entropy on compact parameter interval, before time/noise/data quantifiers.",
        "clock_window": "Positive explicit radius and nonzero witness; does not itself guarantee arbitrarily small reconstruction error.",
        "explicit_M_k": "DERIVED written proof verified; not formally compiled in these leaves."
    },
    "scope": {"new_compilation_run": False, "um_py_executed_or_imported": False,
              "reviewed_sources_modified": False, "approval_in_other_persons_name": False,
              "gate_moved": False}
}
assert before == [rec(path) for path in inputs]
manifest["inputs_unchanged_during_final_measurement"] = True
target = ROOT / "MANIFESTO_REVISAO_PROPRIA.json"
new(target, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"manifest": rec(target), "note": rec(note), "totals": manifest["totals"]}, ensure_ascii=False))
