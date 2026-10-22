"""Measure frozen inputs and copy integration tools; do not integrate, compile, or execute um.py."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import re

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
PREVIOUS = BASE / "INTEGRADOR_SELETOR_LOCALIDADE_20260909_174443_581582"
PREVIOUS_BUILD = PREVIOUS / "BUILD_SUCCESSOR_20260909_174751_385895"
INVENTORY = BASE / "REEXAME_GIBBS_DINAMICA_20260909/INVENTARIO_SEIS_FONTES.json"
SOURCE_UM = BASE / "COPIA_INTEGRADA_20260909_174634_173402/um.py"
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def record(path):
    raw = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def read(path):
    return json.loads(path.read_bytes().decode("utf-8"))


def new_file(path, raw):
    assert path.resolve().is_relative_to(OUT)
    assert not path.exists()
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.stat().st_size == len(raw) and temporary.read_bytes() == raw
    os.rename(temporary, path)
    assert path.read_bytes() == raw


def write_json(path, data):
    new_file(path, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def declarations(text):
    pattern = re.compile(r"(?m)^(?:noncomputable[ \t]+)?"
                         r"(abbrev|def|structure|theorem|local[ \t]+instance)[ \t]+"
                         r"([^\W\d]\w*'*)(?=[ \t\r\n:({\[])")
    entries = [(re.sub(r"[ \t]+", " ", m.group(1)), m.group(2)) for m in pattern.finditer(text)]
    names = [name for _, name in entries]
    assert len(names) == len(set(names))
    prints = re.findall(r"(?m)^#print axioms ([\w.']+)[ \t]*$", text)
    assert len(prints) == len(set(prints)) and set(prints) == set(names)
    instance_headers = re.findall(r"(?m)^[ \t]*(?:(?:local|scoped|noncomputable|private|protected)[ \t]+)*instance\b[^\r\n]*", text)
    assert len(instance_headers) == sum(kind == "local instance" for kind, _ in entries)
    return entries


def count_modules(modules):
    ds = [d for module in modules for d in module["declarations"]]
    assert len(ds) == len({d["name"] for d in ds})
    theorems = sum(d["kind"] == "theorem" for d in ds)
    return {"modules": len(modules), "theorems": theorems,
            "other_declarations": len(ds) - theorems,
            "local_instances": sum(d["kind"] == "local instance" for d in ds), "total": len(ds)}


def main():
    assert OUT.is_relative_to(BASE)
    input_pins = [record(INVENTORY), record(SOURCE_UM)]
    inventory = read(INVENTORY)
    plan_path = PREVIOUS_BUILD / "BUILD_PLAN.json"
    result_path = PREVIOUS_BUILD / "TRANSPOSED_RESULT.json"
    prior_cfg_path = PREVIOUS / "CONFIG_CINCO_APROVADA.json"
    input_pins.extend(record(p) for p in (plan_path, result_path, prior_cfg_path))
    plan, result, prior_cfg = read(plan_path), read(result_path), read(prior_cfg_path)
    assert result["status"] == "PASS_TRANSPOSED_SCOPE"
    assert result["input_boundary_unchanged"] and result["cached_boundary_unchanged"]
    assert result["plan"] == record(plan_path)
    assert all(run["valid"] and run["exit_code"] == 0 and run["warning_lines"] == 0 for run in result["runs"])
    assert all(set(row["axioms"]) <= TRIO for run in result["runs"] for row in run["axiom_rows"])
    assert plan["integrated_copy"] == record(SOURCE_UM)
    integration_path = Path(plan["integration_result"]["path"])
    assert record(integration_path) == plan["integration_result"]
    input_pins.append(record(integration_path))

    # Parse and literal-evaluate source text only. Neither um.py is imported or executed.
    tree = ast.parse(SOURCE_UM.read_bytes().decode("utf-8"))
    tables = [node.value for node in tree.body if isinstance(node, ast.Assign)
              and any(isinstance(target, ast.Name) and target.id == "_EMBEDDED_KERNEL_FILES" for target in node.targets)]
    assert len(tables) == 1 and isinstance(tables[0], ast.Dict)
    embedded = ast.literal_eval(tables[0])
    assert isinstance(embedded, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in embedded.items())
    old_modules = plan["modules"]
    predecessor_counts = count_modules(old_modules)
    assert predecessor_counts["modules"] == plan["counts"]["total_modules"]
    assert predecessor_counts["theorems"] == plan["counts"]["theorems"]
    assert predecessor_counts["other_declarations"] == plan["counts"]["other_declarations"]
    assert predecessor_counts["total"] == plan["counts"]["all_declarations"]
    for module in old_modules:
        actual = declarations(embedded[module["key"]])
        assert [{"kind": kind, "name": module["namespace"] + "." + name} for kind, name in actual] == module["declarations"]

    config_modules, measured_modules, receipt_checks = [], [], []
    for item in inventory["modules"]:
        source_path, receipt_path = Path(item["source"]["path"]), Path(item["receipt"]["path"])
        source_pin, receipt_pin = record(source_path), record(receipt_path)
        assert source_pin == item["source"] and receipt_pin == item["receipt"]
        input_pins.extend([source_pin, receipt_pin])
        receipt = read(receipt_path)
        assert receipt["status"] == "PASS_COMPILED_SCOPE" and receipt["boundary_unchanged"]
        assert any(source["sha256"] == source_pin["sha256"] for source in receipt["sources"])
        assert all(run["exit_code"] == 0 for run in receipt["runs"])
        assert all(set(row["axioms"]) <= TRIO for row in receipt["axiom_rows"])
        text = source_path.read_bytes().decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        module_name = source_path.stem
        assert module_name == item["module"] and "TGLExt/" + module_name + ".lean" not in embedded
        namespaces = re.findall(r"(?m)^namespace ([\w.]+)\s*$", text)
        assert len(namespaces) == 1
        assert not any(re.search(r"(?m)^namespace " + re.escape(namespaces[0]) + r"\s*$", old) for old in embedded.values())
        ds = [{"kind": kind, "name": namespaces[0] + "." + name} for kind, name in declarations(text)]
        assert sum(d["kind"] == "theorem" for d in ds) == item["theorems"]
        assert sum(d["kind"] != "theorem" for d in ds) == item["other_declarations"]
        assert len(ds) == item["axiom_audits"]
        assert not re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b", text)
        rows = {row["name"] for row in receipt["axiom_rows"]}
        assert {d["name"] for d in ds} <= rows
        config_modules.append({"source": source_pin["path"], "sha256": source_pin["sha256"],
                               "build_result": receipt_pin["path"], "build_result_sha256": receipt_pin["sha256"]})
        measured_modules.append({"module": module_name, "namespace": namespaces[0], "declarations": ds})
        receipt_checks.append({"module": module_name, "receipt_status": receipt["status"],
                               "all_runs_exit_zero": True, "allowed_axioms_only": True,
                               "source_pin_matches_inventory_and_receipt": True,
                               "source_declaration_count_matches_inventory": True})

    assert len({m["namespace"] for m in measured_modules}) == len(measured_modules)
    counts = count_modules(measured_modules)
    accumulated = count_modules(old_modules + measured_modules)
    assert counts["modules"] == inventory["counts"]["modules"]
    assert counts["theorems"] == inventory["counts"]["theorems"]
    assert counts["other_declarations"] == inventory["counts"]["other_declarations"]
    assert counts["total"] == inventory["counts"]["axiom_audits"]
    script_copies = []
    for name in ("integrate_approved_copy.py", "prepare_successor.py", "run_successor.py"):
        origin = PREVIOUS / name
        before = record(origin)
        raw = origin.read_bytes()
        ast.parse(raw.decode("utf-8"))
        new_file(OUT / name, raw)
        assert record(origin) == before and (OUT / name).read_bytes() == raw
        script_copies.append({"source": before, "copy": record(OUT / name), "bytes_identical": True})
        input_pins.append(before)

    cfg = {
        "root_confirmed": False,
        "approval_basis": "Preparação por subagente: pins medidos e compatibilidade estática verificada. A tarefa principal ainda não confirmou esta configuração. Nenhuma aprovação externa é atribuída.",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_um": SOURCE_UM.as_posix(), "source_um_sha256": record(SOURCE_UM)["sha256"],
        "canonical_kernel": prior_cfg["canonical_kernel"],
        "canonical_kernel_basis": "Inherited unchanged from the frozen predecessor configuration; no canonical writes.",
        "predecessor_integration_result": record(integration_path),
        "predecessor_build_result": record(result_path),
        "predecessor_build_plan": record(plan_path),
        "inventory": record(INVENTORY),
        "modules": config_modules,
        "measured_counts": {
            "total": counts,
            "per_module": [{"module": m["module"], **count_modules([m])} for m in measured_modules],
            "predecessor": predecessor_counts, "accumulated": accumulated},
        "scope": "Six frozen leaf PASS sources over predecessor 77. Static preparation only; no integration, compiler, um.py execution, external approval, gate or flag change. Cumulative counts derive from predecessor BUILD_PLAN modules, not its five-module INTEGRATION_RESULT delta."
    }
    cfg_path = OUT / "CONFIG_83_NAO_CONFIRMADA.json"
    write_json(cfg_path, cfg)
    assert all(record(Path(pin["path"])) == pin for pin in input_pins)
    receipt = {
        "status": "PREPARED_UNCONFIRMED_NOT_INTEGRATED_NOT_COMPILED",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "configuration": record(cfg_path), "script_copies": script_copies,
        "preparation_script": record(Path(__file__).resolve()),
        "source_inventory": record(INVENTORY), "predecessor_plan": record(plan_path),
        "predecessor_result": record(result_path),
        "counts": {"predecessor": predecessor_counts, "new": counts, "accumulated": accumulated},
        "receipt_checks": receipt_checks, "input_pins": input_pins,
        "input_pins_unchanged_after_preparation": True,
        "um_py_executed_or_imported": False, "integration_executed": False,
        "lean_executed": False, "root_approval_granted": False,
        "notes": "This preparation checks the measured leaf declarations, receipt status, exit codes and allowed axiom rows. It does not replace the main task semantic review or the future joint compilation. Recursive cache provenance remains enforced by the unchanged prepare_successor.py."
    }
    write_json(OUT / "RECIBO_PREPARACAO_NAO_CONFIRMADA.json", receipt)
    command_text = f'''# Comandos posteriores à confirmação da tarefa principal

[REAL] Preparação estática em pasta nova; os três scripts foram copiados byte a byte. Não houve integração ou compilação nesta preparação. `um.py` foi apenas analisado com AST e `literal_eval`.

[OPEN] A tarefa principal deve ler esta configuração e, se confirmar seus pins e o escopo, gravar uma **nova** `CONFIG_83_APROVADA.json` com `root_confirmed: true` e sua própria fundamentação. A configuração não confirmada permanece intacta.

Acumulado medido pelo `BUILD_PLAN.json` predecessor e declarações das seis fontes: {accumulated['modules']} módulos, {accumulated['theorems']} teoremas, {accumulated['other_declarations']} outras declarações, {accumulated['total']} auditorias. Há {accumulated['local_instances']} instâncias locais nomeadas nesse total.

Os comandos abaixo são instruções para a tarefa principal e **não foram executados**:

```powershell
$taskPython = 'C:\\Users\\rotol\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe'
& $taskPython -B '{OUT / 'integrate_approved_copy.py'}' '{OUT / 'CONFIG_83_APROVADA.json'}'
```

O comando de integração imprime a nova pasta `COPIA_INTEGRADA_...`. Usar exatamente esse caminho no argumento seguinte:

```powershell
& $taskPython -B '{OUT / 'prepare_successor.py'}' '<PASTA_NOVA_COPIA_INTEGRADA_RETORNADA>' '{plan_path}' '{result_path}'
```

A preparação sucessora imprime o novo `BUILD_PLAN.json`. Usar exatamente o caminho retornado:

```powershell
& $taskPython -B '{OUT / 'run_successor.py'}' '<BUILD_PLAN_JSON_RETORNADO>'
```

O script de integração exige confirmação e falha com a configuração entregue. A compilação sucessora, quando autorizada pela tarefa principal, preservará 77 módulos por proveniência de cache e compilará seis folhas mais raiz e duas auditorias. Não executa nem importa `um.py`.
'''
    new_file(OUT / "COMANDOS_PARA_TAREFA_PRINCIPAL.md", command_text.encode("utf-8"))
    print(json.dumps({"folder": OUT.as_posix(), "configuration": record(cfg_path), "counts": receipt["counts"], "status": receipt["status"], "scripts": script_copies}, ensure_ascii=False))


if __name__ == "__main__":
    main()
