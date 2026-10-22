"""Read frozen proof receipts and prepare an UNCONFIRMED configuration; no Lean/um execution."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, re, sys

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
HERE = Path(__file__).resolve().parent
PREVIOUS = BASE / "INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394"
PREVIOUS_BUILD = PREVIOUS / "BUILD_SUCCESSOR_20260909_192313_320129"
COPY = BASE / "COPIA_INTEGRADA_20260909_192248_937671"
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
SOURCES = [
    ("PRECISAO_PREFIXO_CARATER_20260909_195301_3136224", "CharacterPrefixStability", "BUILD_20260909_200132_598834"),
    ("PRECISAO_PREFIXO_CARATER_20260909_195301_3136224", "FiniteCharacterResolution", "BUILD_20260909_200630_996675"),
    ("PRECISAO_PREFIXO_CARATER_20260909_195301_3136224", "RecordCharacterMeshControl", "BUILD_20260909_200841_461876"),
    ("ERRO_RECONSTRUCAO_FINITA_20260909", "FiniteResponseErrorBounds", "BUILD_20260909_195624_030733"),
    ("ERRO_RECONSTRUCAO_FINITA_20260909", "MixedGibbsFiniteAccuracy", "BUILD_20260909_200412_567584"),
    ("ERRO_RECONSTRUCAO_FINITA_20260909", "GibbsSamplingWindow", "BUILD_20260909_201028_081251"),
    ("METRICA_FISHER_SELECIONADA_20260909_195323_635574", "SelectedFisherLorentzMetric", "BUILD_20260909_200624_640468"),
    ("VARIACAO_ESCALAR_DENSIDADE_20260909_200600", "ScalarMatterDensityVariation", "BUILD_20260909_200520_881623"),
]

def record(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def new_file(path, raw):
    assert path.resolve().is_relative_to(BASE) and not path.exists(), path
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    os.rename(temp, path)
    assert path.read_bytes() == raw

def new_json(path, obj):
    new_file(path, (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

def count(modules):
    decls = [d for module in modules for d in module["declarations"]]
    theorem_count = sum(d["kind"] == "theorem" for d in decls)
    return {"modules": len(modules), "theorems": theorem_count,
            "other_declarations": len(decls) - theorem_count,
            "local_instances": sum(d["kind"] == "local instance" for d in decls),
            "total": len(decls)}

def main():
    assert len(sys.argv) <= 2, "Optional argument: extra-source JSON list."
    plan_path = PREVIOUS_BUILD / "BUILD_PLAN.json"
    result_path = PREVIOUS_BUILD / "TRANSPOSED_RESULT.json"
    plan, result = read_json(plan_path), read_json(result_path)
    integration_path = COPY / "INTEGRATION_RESULT.json"
    integration = read_json(integration_path)
    source_pin = record(COPY / "um.py")
    assert plan["integrated_copy"] == source_pin == integration["integrated_copy"]
    assert result["plan"] == record(plan_path)
    assert result["status"] == "PASS_TRANSPOSED_SCOPE"
    assert result["input_boundary_unchanged"] and result["cached_boundary_unchanged"]
    assert not result["um_py_executed"] and not result["canonical_changes"]
    assert all(run["exit_code"] == 0 and run["valid"] and run["warning_lines"] == 0 for run in result["runs"])
    for run in result["runs"]:
        assert all(set(row["axioms"]) <= ALLOWED for row in run["axiom_rows"])
    tree = ast.parse((COPY / "um.py").read_text(encoding="utf-8"))
    tables = [node for node in tree.body if isinstance(node, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in node.targets)]
    assert len(tables) == 1
    embedded = ast.literal_eval(tables[0].value)
    predecessor = count(plan["modules"])
    for key, source_key in [("modules", "total_modules"), ("theorems", "theorems"),
                            ("other_declarations", "other_declarations"), ("total", "all_declarations")]:
        assert predecessor[key] == plan["counts"][source_key] == result["counts"][source_key]
    specs = [{"source": (BASE / folder / (name + ".lean")).as_posix(),
              "build_result": (BASE / folder / build / "BUILD_RESULT.json").as_posix()}
             for folder, name, build in SOURCES]
    if len(sys.argv) == 2:
        extra = read_json(sys.argv[1])
        assert isinstance(extra, list)
        specs.extend(extra)
    pattern = re.compile(r"(?m)^(?:noncomputable[ \t]+)?(abbrev|def|structure|theorem|local[ \t]+instance)[ \t]+([^\W\d]\w*'*)(?=[ \t\r\n:({\[])")
    modules, namespaces, all_names = [], set(), set()
    for spec in specs:
        path, receipt_path = Path(spec["source"]), Path(spec["build_result"])
        pin, receipt_pin = record(path), record(receipt_path)
        proof = read_json(receipt_path)
        assert proof["status"] == "PASS_COMPILED_SCOPE" and proof["boundary_unchanged"]
        assert pin in proof["sources"], path
        assert proof["approved_library"] == record(result_path)
        assert all(run["exit_code"] == 0 for run in proof["runs"])
        text = path.read_text(encoding="utf-8")
        key = "TGLExt/" + path.name
        assert key not in embedded
        ns = re.findall(r"(?m)^namespace ([\w.]+)\s*$", text)
        assert len(ns) == 1 and ns[0] not in namespaces
        assert all(not re.search(r"(?m)^namespace " + re.escape(ns[0]) + r"\s*$", old) for old in embedded.values())
        namespaces.add(ns[0])
        declarations = [{"kind": re.sub(r"[ \t]+", " ", match.group(1)),
                         "name": ns[0] + "." + match.group(2)} for match in pattern.finditer(text)]
        names = [item["name"] for item in declarations]
        assert names and len(names) == len(set(names)) and not (set(names) & all_names)
        all_names.update(names)
        prints = re.findall(r"(?m)^#print axioms ([\w.']+)[ \t]*$", text)
        assert len(prints) == len(set(prints)) and {ns[0] + "." + name for name in prints} == set(names)
        instances = re.findall(r"(?m)^[ \t]*(?:(?:local|scoped|noncomputable|private|protected)[ \t]+)*instance\b[^\r\n]*", text)
        assert len(instances) == sum(d["kind"] == "local instance" for d in declarations)
        assert not re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b", text)
        rows = proof["axiom_rows"]
        assert len(rows) == len(names) and {row["name"] for row in rows} == set(names)
        assert all(set(row["axioms"]) <= ALLOWED for row in rows)
        log_records = []
        for run in proof["runs"]:
            log = receipt_path.parent / (run["module"] + ".log")
            log_text = log.read_text(encoding="utf-8")
            assert not re.search(r"(?im)\b(?:warning|error):", log_text), log
            log_records.append(record(log))
        item = {"module": path.stem, "key": key, "namespace": ns[0], "source": pin,
                "build_result": receipt_pin, "declarations": declarations,
                "imports": re.findall(r"(?m)^import ([\w.]+)$", text), "logs": log_records,
                "receipt_status": proof["status"], "leaf_exit_codes": [r["exit_code"] for r in proof["runs"]]}
        measured = count([item])
        assert measured["theorems"] == proof["theorems"] and measured["other_declarations"] == proof["definitions"]
        modules.append(item)
    names = {m["module"] for m in modules}
    assert len(names) == len(modules)
    dependencies = {m["module"]: sorted({name.split(".")[-1] for name in m["imports"]} & names) for m in modules}
    order = []
    while len(order) < len(modules):
        ready = [m["module"] for m in modules if m["module"] not in order and set(dependencies[m["module"]]) <= set(order)]
        assert ready, "Local import cycle"
        order.extend(ready)
    delta = count(modules)
    accumulated = {key: predecessor[key] + delta[key] for key in predecessor}
    stem = str(accumulated["modules"])
    config_path = HERE / ("CONFIG_" + stem + "_NAO_CONFIRMADA.json")
    inventory_path = HERE / ("INVENTARIO_" + stem + ".json")
    assert not config_path.exists() and not inventory_path.exists()
    script_copies = []
    for name in ["integrate_approved_copy.py", "prepare_successor.py", "run_successor.py"]:
        origin, copied = PREVIOUS / name, HERE / name
        raw = origin.read_bytes()
        if copied.exists():
            assert copied.read_bytes() == raw
        else:
            new_file(copied, raw)
        script_copies.append({"source": record(origin), "copy": record(copied), "byte_identical": True})
    inventory = {"status": "PREPARED_STATIC_ONLY_NOT_CONFIRMED", "created_utc": datetime.now(timezone.utc).isoformat(),
                 "base": source_pin, "predecessor_build_plan": record(plan_path), "predecessor_build_result": record(result_path),
                 "modules": modules, "delta": delta, "predecessor": predecessor, "accumulated": accumulated,
                 "embedded_before": len(embedded), "lean_embedded_before": sum(k.endswith('.lean') for k in embedded),
                 "embedded_after_expected": len(embedded) + len(modules),
                 "lean_embedded_after_expected": sum(k.endswith('.lean') for k in embedded) + len(modules),
                 "full_theorem_audit_before": len(re.findall(r"(?m)^#print axioms ", embedded['TGL/Audit.lean'])),
                 "local_dependencies": dependencies, "topological_order": order,
                 "scripts": script_copies, "root_confirmed": False, "independent_semantic_approval_attributed": False,
                 "integration_executed": False, "lean_executed": False, "um_py_executed_or_imported": False}
    new_json(inventory_path, inventory)
    config = {"root_confirmed": False,
              "approval_basis": "No approval attributed. Frozen leaf receipts and predecessor compilation were checked statically. Main task must confirm this measured snapshot in a NEW configuration before integration.",
              "created_utc": datetime.now(timezone.utc).isoformat(), "source_um": source_pin["path"],
              "source_um_sha256": source_pin["sha256"],
              "canonical_kernel": read_json(PREVIOUS / 'CONFIG_83_APROVADA.json')["canonical_kernel"],
              "canonical_kernel_basis": "Inherited metadata only; no canonical writes or execution.",
              "predecessor_integration_result": record(integration_path), "predecessor_build_result": record(result_path),
              "predecessor_build_plan": record(plan_path), "inventory": record(inventory_path),
              "modules": [{"source": m["source"]["path"], "sha256": m["source"]["sha256"],
                           "build_result": m["build_result"]["path"], "build_result_sha256": m["build_result"]["sha256"]} for m in modules],
              "measured_counts": {"total": delta, "per_module": [{"module": m["module"], **count([m])} for m in modules],
                                  "predecessor": predecessor, "accumulated": accumulated},
              "scope": "Additive successor of verified copy83 only. No canonical update, seal, physical flag or claim of physical completion. Joint compilation and static audit remain required."}
    new_json(config_path, config)
    for module in modules:
        assert record(module["source"]["path"]) == module["source"]
        assert record(module["build_result"]["path"]) == module["build_result"]
    assert record(COPY / "um.py") == source_pin
    new_json(HERE / ("PREPARATION_RECEIPT_" + stem + ".json"),
             {"status": inventory["status"], "configuration": record(config_path), "inventory": record(inventory_path),
              "preparation_script": record(__file__), "scripts": script_copies, "counts": config["measured_counts"],
              "approval_attributed": False, "um_py_executed_or_imported": False, "integration_or_lean_executed": False})
    print(json.dumps({"configuration": record(config_path), "delta": delta, "accumulated": accumulated,
                      "root_confirmed": False, "status": inventory["status"]}, ensure_ascii=False))

if __name__ == "__main__":
    main()
