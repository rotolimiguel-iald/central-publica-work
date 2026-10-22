"""Read-only audit by default; --write seals only new continuation037 artifacts."""
from pathlib import Path
import hashlib, json, re, sys, os
from datetime import datetime, timezone
import clean_continuation035 as common

ROOT = Path(__file__).resolve().parent
MODULES = ["QuarticClockTransport", "BinaryRelativeQuartic", "SummableRelativeQuartic", "JacobiAreaQuarticLimit", "FourthOrderMatchingControls", "QuarticMatchingClockControls"]
MANIFEST = ROOT / "CONTINUACAO037_MANIFESTO.json"
BUILD = ROOT / "CONTINUACAO037_CLEAN_BUILD.json"
DELIVERY = ROOT / "TUNEL/DO_CHATGPT/ENTREGA_037_ESPONTANEA_quarta_ordem_area_e_relogio.md"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

def check(condition, message):
    if not condition:
        raise RuntimeError(message)

def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))

def path_key(path):
    """Normalize Windows junctions and case before comparing provenance paths."""
    return os.path.normcase(str(Path(path).resolve()))


def verify_record(row):
    actual = common.record(row["path"])
    check(actual["sha256"] == row["sha256"] and actual["bytes"] == row["bytes"],
          "Hash or size mismatch: " + row["path"])

def source_census(path):
    raw = Path(path).read_bytes()
    code = common.mask_lean(raw.decode("utf-8-sig"))
    check(not re.search(r"\b(?:sorry|admit|axiom|native_decide)\b", code), "Forbidden proof token")
    check(not re.search(r"set_option\s+linter\.[\w.]+\s+false", code), "Disabled linter")
    declarations = re.findall(r"(?m)^(theorem|lemma|def|abbrev|structure)\s+([\w.]+)", code)
    printed = re.findall(r"(?m)^#print\s+axioms\s+([\w.]+)", code)
    check(len(printed) == len(set(printed)), "Duplicate axiom print")
    check(set(printed) == {name for _, name in declarations}, "Incomplete declaration axiom coverage")
    namespaces = re.findall(r"(?m)^namespace\s+([\w.]+)", code)
    check(namespaces == ["ChatgptAudit.Quartic037"], "Unexpected namespace")
    instance_rows = common.instances(raw.decode("utf-8-sig"))
    check(not any(row["anonymous"] for row in instance_rows), "Anonymous instance")
    return {"theorems": sum(k in {"theorem", "lemma"} for k, _ in declarations),
            "definitions_including_structures": sum(k in {"def", "abbrev", "structure"} for k, _ in declarations),
            "structures": sum(k == "structure" for k, _ in declarations),
            "instances": len(instance_rows), "anonymous_instances": 0,
            "printed": ["ChatgptAudit.Quartic037." + name for name in printed]}

def inspect_build():
    data = read_json(BUILD)
    check(data["status"] == "PASS" and data["fresh_clean_build"] is True, "No successful clean build")
    check(data.get("development_only") is False, "Development attempt cannot seal")
    check(data["modules"] == MODULES and data["build_order"] == MODULES, "Unexpected build batch")
    check(data["baseline_modules"] == [], "Unexpected rebuilt baseline")
    check(data["source037_copies_exact"] is True, "Missing exact-copy assertion")
    check(data["anonymous_instances_remaining"] == 0 and data["inputs_stable"] is True, "Dirty inputs")
    clean = Path(data["clean_directory"]).resolve(strict=True)
    check(clean.parent == ROOT and clean.name.startswith("CONTINUACAO037_CLEAN_"), "Wrong clean directory")
    check(data["integration_module"] == "Imports037All", "Missing integration module")
    check(path_key(data["lean_path"][0]) == path_key(clean), "Wrong first import location")
    check(path_key(ROOT) not in {path_key(p) for p in data["lean_path"]}, "Root fallback forbidden")
    check(path_key(common.KERNEL / ".lake/build/lib/lean") not in
          {path_key(p) for p in data["lean_path"]}, "Unrestricted canonical fallback forbidden")
    records = data["files"]
    check(len(records) == len({path_key(row["path"]) for row in records}), "Duplicate build record")
    for row in records:
        verify_record(row)
    recorded = {path_key(row["path"]): row for row in records}

    def require_covered(path):
        key = path_key(path)
        check(key in recorded, "Uncovered build evidence: " + str(path))
        verify_record(recorded[key])

    for filename in ["BUILD_PLAN.json", "FROZEN_INPUTS.json", "FROZEN_INPUTS_AFTER.json", "Imports037All.lean"]:
        require_covered(clean / filename)
    plan = read_json(clean / "BUILD_PLAN.json")
    check(plan["build_order"] == MODULES and path_key(plan["clean_directory"]) == path_key(clean), "Plan mismatch")
    check(plan["modules"] == MODULES and plan["baseline_modules"] == [] and
          plan["integration_module"] == "Imports037All", "Plan batch mismatch")
    check(plan["sources"] == data["sources"] and plan["lean_path"] == data["lean_path"], "Plan crosslink mismatch")
    check(plan["import_graph"] == data["import_graph"], "Plan import graph mismatch")
    frozen = read_json(clean / "FROZEN_INPUTS.json")
    check(bool(frozen) and frozen == read_json(clean / "FROZEN_INPUTS_AFTER.json"), "Frozen snapshot mismatch")
    check(len(frozen) == len({path_key(row["path"]) for row in frozen}), "Duplicate frozen input")
    for row in frozen:
        require_covered(row["path"])
        verify_record(row)
    for row in plan["custody_before"]:
        check(row in frozen, "Custody record absent from frozen inputs")
        verify_record(row)

    package_root = common.KERNEL / ".lake/packages"
    package_dirs = sorted([p for p in package_root.iterdir() if p.is_dir()], key=lambda p: p.name)
    external_roots = [p / ".lake/build/lib/lean" for p in package_dirs
                      if (p / ".lake/build/lib/lean").is_dir()] + [common.TOOLCHAIN / "lib/lean"]
    expected_lean_path = [clean, clean / "boundary", *external_roots]
    check([path_key(p) for p in data["lean_path"]] == [path_key(p) for p in expected_lean_path],
          "Full LEAN_PATH mismatch")
    boundary = data["boundary"]
    check(boundary["kind"] == "pinned_pre037_not_recompiled", "Wrong boundary kind")
    check(path_key(boundary["directory"]) == path_key(clean / "boundary"), "Wrong boundary directory")
    check(plan["boundary_modules"] == boundary["modules"] and
          plan["external_direct_inputs"] == boundary["external_direct_inputs"], "Boundary plan mismatch")
    check(boundary["limitation"] == plan["external_limit"], "Boundary limitation mismatch")
    expected_manifests = [ROOT / ("CONTINUACAO%03d_MANIFESTO.json" % i) for i in [29, 32, 33, 34, 36]]
    check([path_key(row["path"]) for row in boundary["manifests"]] ==
          [path_key(p) for p in expected_manifests], "Wrong historical manifests")
    historical = {}
    pins36 = None
    for row in boundary["manifests"]:
        verify_record(row)
        require_covered(row["path"])
        pins = common.load_pins(Path(row["path"]))
        historical.update(pins)
        if path_key(row["path"]) == path_key(ROOT / "CONTINUACAO036_MANIFESTO.json"):
            pins36 = pins
    check(pins36 is not None, "No sealed036 pin table")
    common.verify_pin(ROOT / "clean_continuation035.py", pins36)
    previous_path = ROOT / "CONTINUACAO036_CLEAN_BUILD.json"
    require_covered(previous_path)
    common.verify_pin(previous_path, pins36)
    previous = read_json(previous_path)
    previous_modules = ["OpticalTidalScreen", "OpticalScreenInvariant", "OpticalJacobiArea", "OpticalAreaFreedom"]
    check(previous["status"] == "PASS" and previous["development_only"] is False and
          previous["fresh_clean_build"] is True, "Unverified final036 boundary")
    check(previous["modules"] == previous_modules and previous["build_order"] == previous_modules,
          "Unexpected036 batch")
    previous_clean = Path(previous["clean_directory"]).resolve(strict=True)
    check(previous_clean.parent == ROOT and previous_clean.name.startswith("CONTINUACAO036_CLEAN_"),
          "Wrong verified036 directory")
    previous_sources = {row["module"]: row for row in previous["sources"]}
    check(len(previous_sources) == len(previous["sources"]) and set(previous_sources) == set(previous_modules),
          "Wrong verified036 source set")
    previous_files = {path_key(row["path"]): row for row in previous["files"]}
    previous_steps = {row["module"]: row for row in previous["steps"]}
    check([row["module"] for row in previous["steps"]] == previous_modules + ["Imports036All"],
          "Wrong verified036 integration order")
    overrides = {}
    for module in previous_modules:
        row = previous_sources[module]
        source = previous_clean / (module + ".lean")
        binary = previous_clean / (module + ".olean")
        check(path_key(row["source"]) == path_key(source), "036 source escaped verified build")
        check(row["source_equals_original"] is True and row["transpositions"] == [], "036 source transformed")
        check(row["proof_sha256"] == common.digest(source), "036 source pin mismatch")
        for path in [source, binary]:
            common.verify_pin(path, pins36)
            check(path_key(path) in previous_files, "036 artifact absent from verified marker")
            verify_record(previous_files[path_key(path)])
        metadata = Path(previous_steps[module]["metadata"])
        check(metadata.resolve(strict=True).parent == previous_clean, "036 metadata escaped verified build")
        common.verify_pin(metadata, pins36)
        old_meta = read_json(metadata)
        check(old_meta["module"] == module and old_meta["passed"] is True and old_meta["exit_code"] == 0,
              "036 compilation crosslink failed")
        check(path_key(old_meta["source"]) == path_key(source) and
              path_key(old_meta["olean"]) == path_key(binary), "036 source/binary crosslink failed")
        check(old_meta["proof_sha256"] == common.digest(source) and
              old_meta["olean_sha256"] == common.digest(binary), "036 compiled artifact hash mismatch")
        overrides[module] = (source, binary)

    graph = data["import_graph"]
    boundary_map = {row["module"]: row for row in boundary["modules"]}
    external_map = {row["module"]: row for row in boundary["external_direct_inputs"]}
    check(len(boundary_map) == len(boundary["modules"]), "Duplicate boundary module")
    check(len(external_map) == len(boundary["external_direct_inputs"]), "Duplicate external module")
    check(not (set(MODULES) & set(boundary_map)) and not (set(MODULES) & set(external_map)) and
          not (set(boundary_map) & set(external_map)), "Overlapping module resolution classes")
    for module, row in boundary_map.items():
        original, copied = row["original_source"], row["source_copy"]
        canonical = module.startswith(("TGL.", "TGLExt."))
        expected_source = (ROOT / "fontes/tgl_kernel" if canonical else ROOT) / common.module_relative(module, ".lean")
        expected_binary = ROOT / common.module_relative(module, ".olean")
        if module in overrides:
            expected_source, expected_binary = overrides[module]
        check(path_key(original["path"]) == path_key(expected_source), "Wrong historical source origin: " + module)
        check(path_key(copied["path"]) == path_key(clean / "boundary_sources" /
              common.module_relative(module, ".lean")), "Wrong boundary source destination")
        for item in [original, copied]:
            require_covered(item["path"])
            verify_record(item)
        check(Path(original["path"]).read_bytes() == Path(copied["path"]).read_bytes(), "Boundary source copy")
        has_pin = path_key(original["path"]) in historical
        check(row["source_has_historical_pin"] is has_pin, "Historical pin flag mismatch")
        if has_pin:
            common.verify_pin(original["path"], historical)
            check(row["source_status"] == "PIN029_036_EXACT_BYTES", "Historical source status")
        else:
            check(canonical, "Unpinned bench source refused")
            check(row["source_status"] == "REAL_CURRENT_READ_NO_HISTORICAL_SOURCE_PIN", "Unpinned source status")
        check(row["source_to_olean_provenance"] == "NOT_ESTABLISHED_OR_REBUILT_BY_THIS_RUN",
              "Unsupported general source-to-olean provenance claim")
        if module in overrides:
            common.verify_pin(original["path"], pins36)
            common.verify_pin(expected_binary, pins36)
        real_imports = common.imports(Path(copied["path"]).read_text(encoding="utf-8-sig"))
        check(real_imports == row["imports"] == graph[module], "Boundary source import mismatch")
        check(not set(real_imports) & set(MODULES), "Historical boundary imports a rebuilt037 module")
        expected_companions = common.companions(expected_binary)
        check([path_key(item["original"]["path"]) for item in row["files"]] ==
              [path_key(p) for p in expected_companions], "Incomplete boundary binary companions")
        check(sum(item["primary_olean"] is True for item in row["files"]) == 1, "Primary boundary binary missing")
        for item, old_path in zip(row["files"], expected_companions):
            old, new = item["original"], item["copy"]
            suffix = str(old_path)[len(str(expected_binary)):]
            expected_copy = Path(str(clean / "boundary" / common.module_relative(module, ".olean")) + suffix)
            check(path_key(new["path"]) == path_key(expected_copy), "Wrong boundary binary destination")
            check(item["primary_olean"] is (suffix == ""), "Wrong primary boundary binary flag")
            check(item["pinned_in_manifest029_036"] is True, "Boundary binary pin flag missing")
            for artifact in [old, new]:
                verify_record(artifact)
                require_covered(artifact["path"])
            common.verify_pin(old["path"], historical)
            if module in overrides:
                common.verify_pin(old["path"], pins36)
            check(old["sha256"] == new["sha256"] and old["bytes"] == new["bytes"], "Binary copy mismatch")

    for module, row in external_map.items():
        expected = next((p / common.module_relative(module, ".olean") for p in external_roots
                         if (p / common.module_relative(module, ".olean")).is_file()), None)
        check(expected is not None and path_key(expected) == path_key(row["resolved"]), "External resolution")
        check([path_key(item["path"]) for item in row["files"]] ==
              [path_key(p) for p in common.companions(Path(row["resolved"]))], "External companions mismatch")
        for item in row["files"]:
            require_covered(item["path"])
            verify_record(item)

    sources = {row["module"]: row for row in data["sources"]}
    check(len(sources) == len(data["sources"]) and set(sources) == set(MODULES), "Wrong source set")
    totals = {"theorems": 0, "definitions_including_structures": 0, "structures": 0,
              "instances": 0, "anonymous_instances": 0}
    census = {}
    for module in MODULES:
        row = sources[module]
        original, copied = ROOT / (module + ".lean"), clean / (module + ".lean")
        check(path_key(row["source"]) == path_key(copied) and
              path_key(row["original_source"]) == path_key(original), "Source path mismatch")
        require_covered(original)
        require_covered(copied)
        check(copied.read_bytes() == original.read_bytes(), "Source copy differs")
        check(common.digest(original) == row["original_sha256"] == row["proof_sha256"], "Source pin mismatch")
        check(row["source_equals_original"] is True and row["transpositions"] == [], "Source transformed")
        check(row["namespace"] == "ChatgptAudit.Quartic037" and row["role"] == "batch", "Source role mismatch")
        check(common.imports(copied.read_text(encoding="utf-8-sig")) == graph[module], "Batch import graph mismatch")
        census[module] = source_census(original)
        check(census[module]["printed"] == row["expected_axiom_rows"], "Print census mismatch")
        for key in totals:
            totals[key] += census[module][key]
    expected_order = MODULES + ["Imports037All"]
    check([row["module"] for row in data["steps"]] == expected_order, "Wrong serial build order")
    integration = clean / "Imports037All.lean"
    check(integration.read_text(encoding="utf-8") ==
          "".join("import " + m + "\n" for m in MODULES), "Import-all content mismatch")
    check(graph["Imports037All"] == MODULES, "Integration graph mismatch")
    check(set(graph) == set(MODULES) | set(boundary_map) | {"Imports037All"}, "Unexpected local graph node")
    positions = {module: i for i, module in enumerate(expected_order)}

    def expected_closure(module):
        seen, ordered = set(), []
        def walk(dep):
            check(dep in sources or dep in boundary_map or dep in external_map, "Unresolved graph dependency")
            if dep in seen:
                return
            seen.add(dep)
            ordered.append(dep)
            if dep in sources:
                check(positions[dep] < positions[module], "Non-topological rebuilt dependency")
            if dep in graph:
                for child in graph[dep]:
                    walk(child)
        for dep in graph[module]:
            walk(dep)
        return ordered

    for index, step in enumerate(data["steps"], 1):
        name = step["module"]
        metadata = Path(step["metadata"])
        check(path_key(metadata) == path_key(clean / f"{index:02d}_{name}.json"), "Wrong compilation metadata path")
        require_covered(metadata)
        meta = read_json(metadata)
        check(meta["module"] == name and meta["exit_code"] == 0 and meta["passed"] is True, "Failed compilation")
        check(path_key(meta["metadata"]) == path_key(metadata) and
              path_key(meta["clean_directory"]) == path_key(clean), "Metadata self crosslink mismatch")
        for key in ["source_stable", "inputs_stable", "fresh_clean_build", "axiom_coverage_exact"]:
            check(meta[key] is True, "Failed compilation guard: " + key)
        check(meta["issues"] == [] and meta["anonymous_instances"] == 0, "Compilation issue")
        check(bool(meta["inputs_before"]) and meta["inputs_before"] == meta["inputs_after"], "Inputs changed or absent")
        input_keys = {path_key(row["path"]) for row in meta["inputs_before"]}
        check(len(input_keys) == len(meta["inputs_before"]), "Duplicate compilation input")
        for row in meta["inputs_before"]:
            require_covered(row["path"])
            verify_record(row)
        for key in ["source", "olean", "log"]:
            require_covered(meta[key])
        check([row["module"] for row in meta["import_resolutions"]] == expected_closure(name),
              "Compilation dependency closure mismatch")
        for row in meta["import_resolutions"]:
            dep = row["module"]
            resolved = Path(row["resolved"]).resolve(strict=True)
            require_covered(resolved)
            check(path_key(resolved) in input_keys, "Imported binary missing from compilation inputs")
            expected = next((p / common.module_relative(dep, ".olean") for p in expected_lean_path
                             if (p / common.module_relative(dep, ".olean")).is_file()), None)
            check(expected is not None and path_key(expected) == path_key(resolved), "Actual import shadowing")
            if dep in sources:
                check(row["kind"] == "rebuilt" and
                      path_key(resolved) == path_key(clean / (dep + ".olean")), "Rebuilt import fallback")
            elif dep in boundary_map:
                check(row["kind"] == "pinned_pre037" and
                      path_key(resolved) == path_key(clean / "boundary" /
                      common.module_relative(dep, ".olean")), "Boundary import fallback")
                boundary_row = boundary_map[dep]
                required_inputs = [boundary_row["original_source"]["path"], boundary_row["source_copy"]["path"]]
                for item in boundary_row["files"]:
                    required_inputs.extend([item["original"]["path"], item["copy"]["path"]])
                check(all(path_key(p) in input_keys for p in required_inputs), "Boundary input evidence incomplete")
            else:
                check(row["kind"] == "external_direct" and
                      path_key(resolved) == path_key(external_map[dep]["resolved"]), "Unknown import resolution")
        check(path_key(meta["cwd"]) == path_key(clean) and meta["lean_path"] == data["lean_path"], "Environment mismatch")
        check(path_key(meta["source"]) == path_key(clean / (name + ".lean")), "Wrong compiled source")
        check(path_key(meta["olean"]) == path_key(clean / (name + ".olean")), "Wrong compiled binary")
        check(path_key(meta["log"]) == path_key(clean / f"{index:02d}_{name}.log"), "Wrong compilation log")
        check(path_key(meta["source"]) in input_keys, "Compiled source missing from input snapshot")
        check(common.digest(meta["source"]) == meta["proof_sha256"], "Compiled source changed")
        check(common.digest(meta["olean"]) == meta["olean_sha256"], "Binary changed")
        check(common.digest(meta["log"]) == meta["log_sha256"], "Log changed")
        check(meta["command"][1] == "-o" and len(meta["command"]) == 4 and
              path_key(meta["command"][0]) == path_key(common.TOOLCHAIN / "bin/lean.exe") and
              path_key(meta["command"][2]) == path_key(meta["olean"]) and
              path_key(meta["command"][3]) == path_key(meta["source"]), "Compilation command mismatch")
        check(path_key(meta["command"][0]) in input_keys, "Compiler absent from input snapshot")
        raw_log = Path(meta["log"]).read_text(encoding="utf-8")
        check("sorryAx" not in raw_log and not re.search(r"\b(?:error|warning)(?:\([^\n]*?\))?:", raw_log),
              "Error or warning in log")
        rows = common.parse_axioms(raw_log)
        printed = census[name]["printed"] if name in census else []
        check([row["declaration"] for row in rows] == printed == meta["expected_axiom_rows"], "Axiom mismatch")
        check(rows == meta["axiom_rows"], "Parsed axiom mismatch")
        for row in rows:
            check(set(row["axioms"]) <= ALLOWED_AXIOMS, "Unexpected axiom")
        check(meta["output_artifacts"] == common.snapshot(common.companions(Path(meta["olean"]))),
              "Output artifact coverage mismatch")
        for row in meta["output_artifacts"]:
            require_covered(row["path"])
            verify_record(row)
    verify_record(data["toolchain"])
    require_covered(data["toolchain"]["path"])
    check(path_key(data["toolchain"]["path"]) == path_key(common.TOOLCHAIN / "bin/lean.exe"), "Wrong toolchain")
    return data, totals


def new_json(path, data):
    check(not path.exists(), "Exclusive manifest creation refused")
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    check(temporary.stat().st_size == len(raw) and temporary.read_bytes() == raw, "Temporary verification failed")
    temporary.rename(path)
    check(path.read_bytes() == raw, "Manifest byte verification failed")

def main():
    write = sys.argv[1:] == ["--write"]
    check(not sys.argv[1:] or write, "Only --write is accepted")
    build, totals = inspect_build()
    if write:
        check(not MANIFEST.exists(), "Sealed manifest cannot be replaced")
        paths = {Path(row["path"]) for row in build["files"]}
        paths.update([BUILD, Path(__file__).resolve(), ROOT / "clean_continuation035.py",
                      ROOT / "clean_continuation037.py", ROOT / "revise_continuation037.py",
                      ROOT / "CONTINUACAO037_DERIVACAO_PREVIA.md", ROOT / "CONTINUACAO037_PARECER.md",
                      DELIVERY])
        paths.update([ROOT / "audit_continuation036.py", ROOT / "clean_continuation036.py",
                      ROOT / "CONTINUACAO036_CLEAN_BUILD.json"])
        previous = read_json(ROOT / "CONTINUACAO036_CLEAN_BUILD.json")
        paths.update(Path(row["metadata"]) for row in previous["steps"])
        history = []
        for directory in sorted(ROOT.glob("CONTINUACAO037_CLEAN_*")):
            failure = directory / "FAILURE.json"
            if failure.exists():
                paths.add(failure)
                selected = [p for p in directory.iterdir()
                            if p.is_file() and p.suffix in {".lean", ".json", ".log", ".olean", ".private", ".server"}]
                paths.update(selected)
                history.append({"directory": str(directory), "failure": str(failure)})
        for pattern in ["*037*.bak_*", "CONTINUACAO037_DEVELOPMENT_*.json"] + [m + ".lean.bak_*" for m in MODULES]:
            paths.update(ROOT.glob(pattern))
        result = {"schema": "chatgpt.continuation037.v1", "created_utc": datetime.now(timezone.utc).isoformat(),
                  "status": "PASS", "scope": "exact fourth-order global entropy and optical area; clock dependence of fourth-order matching",
                  "broad_quantum_gravity_goal": "OPEN", "canonical_gate_changed": False,
                  "modules": MODULES, "counts": totals, "fresh_clean_build": True,
                  "clean_build": common.record(BUILD), "clean_directory": build["clean_directory"],
                  "anonymous_instances_remaining": 0, "files": common.snapshot(paths),
                  "preserved_failed_attempts": history,
                  "boundary_limit": build["boundary"]["limitation"],
                  "evidence_limits": [
                      "The relative-entropy and entropy coefficients concern the existing global SummableAmplitude states.",
                      "No moving-cutoff fourth-order entropy theorem with unrestricted cutoff rate is asserted.",
                      "The optical area belongs to the existing conditional plane-wave family; matching requires stated hypotheses.",
                      "Fourth-order matching depends on the clock convention; no general microscopic gravitational dynamics is derived.",
                      "Stage036 imports are linked to its pinned clean sources and binaries, never root olean fallback.",
                      "Other historical binaries are pinned but not rebuilt; individual unpinned TGL sources serve import discovery only.",
                      "Originals, canonical kernel, um.py, Atlas, memories, previous seals and the canonical gate remain untouched."
                  ],
                  "review": "Independent review is reported separately; canonical incorporation is not claimed."}
        new_json(MANIFEST, result)
    else:
        check(MANIFEST.is_file(), "No sealed manifesto yet")
        result = read_json(MANIFEST)
        check(result["modules"] == MODULES and result["counts"] == totals and result["status"] == "PASS",
              "Manifest summary mismatch")
        check(result["clean_build"] == common.record(BUILD), "Build marker pin mismatch")
        for row in result["files"]:
            verify_record(row)
    print(json.dumps({"status": "PASS", "files": len(result["files"]),
                      "modules": len(MODULES), **totals, "manifest": str(MANIFEST)}))

if __name__ == "__main__":
    main()
