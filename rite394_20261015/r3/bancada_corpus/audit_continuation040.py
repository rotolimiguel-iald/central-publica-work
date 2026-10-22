"""Read-only audit by default; --write seals only new continuation040 artifacts."""
from pathlib import Path
import hashlib, json, re, sys, os
from datetime import datetime, timezone
import clean_continuation035 as common

ROOT = Path(__file__).resolve().parent
MODULES = ["RelativeEntropyClock", "StateClockObstruction", "IntrinsicFisherClock",
           "AffineClockAndRegion", "StateClockMatchingControls"]
MANIFEST = ROOT / "CONTINUACAO040_MANIFESTO.json"
BUILD = ROOT / "CONTINUACAO040_CLEAN_BUILD.json"
DELIVERY = ROOT / "TUNEL/DO_CHATGPT/ENTREGA_040_H3_dinamico_e_o_relogio_relativo.md"
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
    declared_names = [name for _, name in declarations]
    check(len(declared_names) == len(set(declared_names)), "Duplicate source declaration")
    check(set(printed) == set(declared_names), "Incomplete declaration axiom coverage")
    namespaces = re.findall(r"(?m)^namespace\s+([\w.]+)", code)
    check(namespaces == ["ChatgptAudit.Clock040"], "Unexpected namespace")
    instance_rows = common.instances(raw.decode("utf-8-sig"))
    check(not any(row["anonymous"] for row in instance_rows), "Anonymous instance")
    return {"theorems": sum(k in {"theorem", "lemma"} for k, _ in declarations),
            "definitions_including_structures": sum(k in {"def", "abbrev", "structure"} for k, _ in declarations),
            "structures": sum(k == "structure" for k, _ in declarations),
            "instances": len(instance_rows), "anonymous_instances": 0,
            "printed": ["ChatgptAudit.Clock040." + name for name in printed]}


# Only these successful, sealed clean batches may override older root artifacts.
# The baseline of 035 has deliberate instance-name insertions, not source equality.
HISTORICAL_BATCHES = {
    35: (["CentralizerDensity", "LikelihoodDensityLog", "DensityStateUniqueness",
          "CentralizerPhaseOrbit", "SitePhaseCovariance", "AngularScreenMetric",
          "AngularAreaObservability"],
         ["UnitaryStateDerivative", "SitePauliObservables", "PauliOperationalSurface",
          "PauliProbabilityModel", "PauliMeasurementFisher"]),
    36: ([], ["OpticalTidalScreen", "OpticalScreenInvariant", "OpticalJacobiArea", "OpticalAreaFreedom"]),
    37: ([], ["QuarticClockTransport", "BinaryRelativeQuartic", "SummableRelativeQuartic",
              "JacobiAreaQuarticLimit", "FourthOrderMatchingControls", "QuarticMatchingClockControls"]),
}


def inspect_historical_build(stage, pins, require_covered):
    """Recheck pinned artifacts and their recorded compilation crosslinks, without rebuilding.

    Only artifacts actually used by 040 must occur in its frozen input snapshot.
    Other historical evidence is pinned and included in the final audit manifest;
    it is not retroactively described as an input captured by the 040 runner.
    """
    label = f"{stage:03d}"
    marker = ROOT / ("CONTINUACAO" + label + "_CLEAN_BUILD.json")
    common.verify_pin(marker, pins)
    require_covered(marker)
    previous = read_json(marker)
    baseline, modules = HISTORICAL_BATCHES[stage]
    order = baseline + modules
    integration_name = "Imports" + label + "All"
    check(previous["status"] == "PASS" and previous["fresh_clean_build"] is True and
          previous["inputs_stable"] is True, "Unverified historical build " + label)
    # 035 predates this field; its pinned exact batch and marker identify the final build.
    check((previous.get("development_only", False) if stage == 35 else
           previous.get("development_only")) is False, "Historical development marker " + label)
    check(previous["modules"] == modules and previous["baseline_modules"] == baseline and
          previous["build_order"] == order and previous["integration_module"] == integration_name,
          "Historical batch mismatch " + label)
    check(previous["source" + label + "_copies_exact"] is True and
          previous["anonymous_instances_remaining"] == 0, "Historical source guard " + label)
    clean = Path(previous["clean_directory"]).resolve(strict=True)
    check(clean.parent == ROOT and clean.name.startswith("CONTINUACAO" + label + "_CLEAN_"),
          "Historical clean directory escaped " + label)
    files = {path_key(row["path"]): row for row in previous["files"]}
    check(len(files) == len(previous["files"]), "Duplicate historical file record " + label)
    sources = {row["module"]: row for row in previous["sources"]}
    check(len(sources) == len(previous["sources"]) and list(sources) == order,
          "Historical source set/order " + label)
    check([row["module"] for row in previous["steps"]] == order + [integration_name],
          "Historical serial/integration order " + label)
    evidence = {marker}

    def verify_old(path):
        path = Path(path)
        common.verify_pin(path, pins)
        check(path_key(path) in files, "Historical artifact absent from marker: " + str(path))
        verify_record(files[path_key(path)])
        evidence.add(path)

    # These scripts are audit dependencies, not retrospectively asserted compilation inputs.
    for filename in ["clean_continuation" + label + ".py", "audit_continuation" + label + ".py"]:
        script = ROOT / filename
        common.verify_pin(script, pins)
        evidence.add(script)
    expected_prints, overrides = {}, {}
    for module in order:
        row = sources[module]
        source, original = clean / (module + ".lean"), ROOT / (module + ".lean")
        binary = clean / (module + ".olean")
        check(path_key(row["source"]) == path_key(source) and
              path_key(row["original_source"]) == path_key(original),
              "Historical source location mismatch: " + module)
        for path in [source, original, binary]:
            verify_old(path)
        raw, raw_original = source.read_bytes(), original.read_bytes()
        check(row["proof_sha256"] == common.digest(source) and
              row["original_sha256"] == common.digest(original), "Historical source digest: " + module)
        check(row["source_equals_original"] is (raw == raw_original),
              "Historical exact-copy flag: " + module)
        role = "baseline" if module in baseline else "batch"
        check(row["role"] == role, "Historical source role: " + module)
        if stage == 35 and role == "baseline":
            renamed, changes = common.name_baseline_instances(module, raw_original)
            check(raw == renamed and row["transpositions"] == changes,
                  "035 baseline changed beyond exact instance-name insertions: " + module)
        else:
            check(raw == raw_original and row["transpositions"] == [],
                  "Historical batch source transformed: " + module)
        code = common.mask_lean(raw.decode("utf-8-sig"))
        namespaces = re.findall(r"(?m)^namespace\s+([\w.]+)", code)
        if stage == 35:
            expected_namespace = ("ChatgptAudit.Density033" if module in baseline[:3] else
                                  "ChatgptAudit.Angular034" if module in baseline else
                                  "ChatgptAudit.Observable035")
        else:
            expected_namespace = "ChatgptAudit.Optical036" if stage == 36 else "ChatgptAudit.Quartic037"
        check(namespaces == [expected_namespace] and row["namespace"] == expected_namespace,
              "Historical namespace mismatch: " + module)
        check(not re.search(r"\b(?:sorry|admit|axiom|native_decide)\b", code) and
              not re.search(r"set_option\s+linter\.[\w.]+\s+false", code),
              "Forbidden historical proof construct: " + module)
        check(not any(item["anonymous"] for item in common.instances(raw.decode("utf-8-sig"))),
              "Anonymous historical compiled instance: " + module)
        printed = re.findall(r"(?m)^#print\s+axioms\s+([\w.]+)", code)
        check(len(printed) == len(set(printed)), "Duplicate historical axiom print: " + module)
        qualified = [name if name.startswith(expected_namespace + ".") else
                     expected_namespace + "." + name for name in printed]
        check(qualified == row["expected_axiom_rows"], "Historical print crosslink: " + module)
        expected_prints[module] = qualified
        overrides[module] = (source, binary)
    integration = clean / (integration_name + ".lean")
    verify_old(integration)
    check(integration.read_bytes() == "".join("import " + m + "\n" for m in order).encode("utf-8"),
          "Historical import-all content mismatch " + label)
    for index, step in enumerate(previous["steps"], 1):
        name = step["module"]
        metadata = clean / f"{index:02d}_{name}.json"
        check(path_key(step["metadata"]) == path_key(metadata), "Historical metadata escaped " + name)
        verify_old(metadata)
        meta = read_json(metadata)
        source, binary, log = clean / (name + ".lean"), clean / (name + ".olean"), clean / f"{index:02d}_{name}.log"
        check(meta["module"] == name and meta["passed"] is True and meta["exit_code"] == 0,
              "Historical failed compilation: " + name)
        for key in ["source_stable", "inputs_stable", "fresh_clean_build", "axiom_coverage_exact"]:
            check(meta[key] is True, "Historical compilation guard: " + name + ":" + key)
        check(meta["issues"] == [] and meta["anonymous_instances"] == 0,
              "Historical compilation issues: " + name)
        check(bool(meta["inputs_before"]) and meta["inputs_before"] == meta["inputs_after"],
              "Historical recorded input stability: " + name)
        old_inputs = {path_key(row["path"]): row for row in meta["inputs_before"]}
        check(len(old_inputs) == len(meta["inputs_before"]), "Duplicate historical compilation input: " + name)
        check(path_key(meta["metadata"]) == path_key(metadata) and
              path_key(meta["clean_directory"]) == path_key(clean) and path_key(meta["cwd"]) == path_key(clean),
              "Historical compilation self crosslink: " + name)
        for key, path, digest_key in [("source", source, "proof_sha256"),
                                     ("olean", binary, "olean_sha256"), ("log", log, "log_sha256")]:
            check(path_key(meta[key]) == path_key(path), "Historical artifact crosslink: " + name + ":" + key)
            verify_old(path)
            check(common.digest(path) == meta[digest_key], "Historical compiled artifact digest: " + name)
        check(path_key(source) in old_inputs and old_inputs[path_key(source)] == common.record(source),
              "Historical compiled source absent from captured inputs: " + name)
        check(meta["role"] == (sources[name]["role"] if name in sources else "integration"),
              "Historical compilation role: " + name)
        check(meta["lean_path"] == previous["lean_path"] and
              path_key(meta["lean_path"][0]) == path_key(clean) and
              path_key(ROOT) not in {path_key(p) for p in meta["lean_path"]} and
              path_key(common.KERNEL / ".lake/build/lib/lean") not in
              {path_key(p) for p in meta["lean_path"]}, "Historical import environment: " + name)
        check(len(meta["command"]) == 4 and meta["command"][1] == "-o" and
              path_key(meta["command"][0]) == path_key(common.TOOLCHAIN / "bin/lean.exe") and
              path_key(meta["command"][2]) == path_key(binary) and
              path_key(meta["command"][3]) == path_key(source), "Historical compilation command: " + name)
        compiler_key = path_key(meta["command"][0])
        check(compiler_key in old_inputs and old_inputs[compiler_key] == previous["toolchain"],
              "Historical compiler snapshot crosslink: " + name)
        raw_log = log.read_text(encoding="utf-8")
        check("sorryAx" not in raw_log and not re.search(r"\b(?:error|warning)(?:\([^\n]*?\))?:", raw_log),
              "Historical compilation warning/error: " + name)
        rows = common.parse_axioms(raw_log)
        check([item["declaration"] for item in rows] == expected_prints.get(name, []) == meta["expected_axiom_rows"]
              and rows == meta["axiom_rows"], "Historical axiom log crosslink: " + name)
        check(all(set(item["axioms"]) <= ALLOWED_AXIOMS for item in rows), "Historical unexpected axiom: " + name)
        check(meta["output_artifacts"] == common.snapshot(common.companions(binary)),
              "Historical output companions mismatch: " + name)
        for item in meta["output_artifacts"]:
            verify_old(item["path"])
    return overrides, evidence


def inspect_build():
    data = read_json(BUILD)
    check(data["schema"] == "chatgpt.clean040.build.v1", "Unexpected build schema")
    check(data["status"] == "PASS" and data["fresh_clean_build"] is True, "No successful clean build")
    check(data.get("development_only") is False, "Development attempt cannot seal")
    check(data["modules"] == MODULES and data["build_order"] == MODULES, "Unexpected build batch")
    check(data["baseline_modules"] == [], "Unexpected rebuilt baseline")
    check(data["source040_copies_exact"] is True, "Missing exact-copy assertion")
    check(data["anonymous_instances_remaining"] == 0 and data["inputs_stable"] is True, "Dirty inputs")
    clean = Path(data["clean_directory"]).resolve(strict=True)
    check(clean.parent == ROOT and clean.name.startswith("CONTINUACAO040_CLEAN_"), "Wrong clean directory")
    check(data["integration_module"] == "Imports040All", "Missing integration module")
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

    for filename in ["BUILD_PLAN.json", "FROZEN_INPUTS.json", "FROZEN_INPUTS_AFTER.json", "Imports040All.lean"]:
        require_covered(clean / filename)
    plan = read_json(clean / "BUILD_PLAN.json")
    check(plan["schema"] == "chatgpt.clean040.plan.v1", "Unexpected plan schema")
    check(plan["build_order"] == MODULES and path_key(plan["clean_directory"]) == path_key(clean), "Plan mismatch")
    check(plan["modules"] == MODULES and plan["baseline_modules"] == [] and
          plan["integration_module"] == "Imports040All", "Plan batch mismatch")
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
    check(boundary["kind"] == "pinned_pre040_not_recompiled", "Wrong boundary kind")
    check(path_key(boundary["directory"]) == path_key(clean / "boundary"), "Wrong boundary directory")
    check(plan["boundary_modules"] == boundary["modules"] and
          plan["external_direct_inputs"] == boundary["external_direct_inputs"], "Boundary plan mismatch")
    check(boundary["limitation"] == plan["external_limit"], "Boundary limitation mismatch")
    expected_manifests = [ROOT / ("CONTINUACAO%03d_MANIFESTO.json" % i) for i in [29, 32, 33, 34, 35, 36, 37]]
    check([path_key(row["path"]) for row in boundary["manifests"]] ==
          [path_key(p) for p in expected_manifests], "Wrong historical manifests")
    historical, pin_tables = {}, {}
    for row, stage in zip(boundary["manifests"], [29, 32, 33, 34, 35, 36, 37]):
        verify_record(row)
        require_covered(row["path"])
        manifest_data = read_json(row["path"])
        accepted_status = (str(manifest_data["status"]).startswith("REAL:") if stage <= 35 else
                           manifest_data["status"] == "PASS")
        check(accepted_status, "Historical manifest without recognized custody status")
        pins = common.load_pins(Path(row["path"]))
        check(len(pins) == len(manifest_data["files"]), "Duplicate historical manifest path")
        pin_tables[stage] = pins
        historical.update(pins)
    # common is the sealed035 helper; verify its current bytes before trusting its results.
    common.verify_pin(ROOT / "clean_continuation035.py", pin_tables[35])
    overrides, override_pins, historical_evidence = {}, {}, set()
    for stage in [35, 36, 37]:
        old_overrides, old_evidence = inspect_historical_build(stage, pin_tables[stage], require_covered)
        overrides.update(old_overrides)
        override_pins.update({module: pin_tables[stage] for module in old_overrides})
        historical_evidence.update(old_evidence)

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
            check(row["source_status"] == "PIN029_037_EXACT_BYTES", "Historical source status")
        else:
            check(canonical, "Unpinned bench source refused")
            check(row["source_status"] == "REAL_CURRENT_READ_NO_HISTORICAL_SOURCE_PIN", "Unpinned source status")
        check(row["source_to_olean_provenance"] == "NOT_ESTABLISHED_OR_REBUILT_BY_THIS_RUN",
              "Unsupported general source-to-olean provenance claim")
        if module in overrides:
            common.verify_pin(original["path"], override_pins[module])
            common.verify_pin(expected_binary, override_pins[module])
        real_imports = common.imports(Path(copied["path"]).read_text(encoding="utf-8-sig"))
        check(real_imports == row["imports"] == graph[module], "Boundary source import mismatch")
        check(not set(real_imports) & set(MODULES), "Historical boundary imports a rebuilt040 module")
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
            check(item["pinned_in_manifest029_037"] is True, "Boundary binary pin flag missing")
            for artifact in [old, new]:
                verify_record(artifact)
                require_covered(artifact["path"])
            common.verify_pin(old["path"], historical)
            if module in overrides:
                common.verify_pin(old["path"], override_pins[module])
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
        check(row["namespace"] == "ChatgptAudit.Clock040" and row["role"] == "batch", "Source role mismatch")
        check(common.imports(copied.read_text(encoding="utf-8-sig")) == graph[module], "Batch import graph mismatch")
        census[module] = source_census(original)
        check(census[module]["printed"] == row["expected_axiom_rows"], "Print census mismatch")
        check(census[module]["theorems"] == row["theorems"] and
              census[module]["definitions_including_structures"] == row["definitions"] and
              row["instances"] == common.instances(original.read_bytes().decode("utf-8-sig")) and
              row["anonymous_instances"] == 0, "Source census crosslink mismatch")
        for key in totals:
            totals[key] += census[module][key]
    custody_keys = {path_key(row["path"]) for row in plan["custody_before"]}
    check(bool(custody_keys) and len(custody_keys) == len(plan["custody_before"]),
          "Missing or duplicate custody snapshot")
    mandatory_custody = [ROOT / "clean_continuation040.py", common.TOOLCHAIN / "bin/lean.exe",
                         ROOT / "TUNEL/PARA_CHATGPT/ORDEM_009_H3_dinamico_e_o_relogio_relativo.md",
                         *expected_manifests,
                         *[ROOT / f"CONTINUACAO{stage:03d}_CLEAN_BUILD.json" for stage in [35, 36, 37]]]
    check(all(path_key(p) in custody_keys for p in mandatory_custody), "Runner custody evidence incomplete")
    expected_frozen_keys = set(custody_keys)
    for row in sources.values():
        expected_frozen_keys.update([path_key(row["source"]), path_key(row["original_source"])])
    for row in boundary_map.values():
        expected_frozen_keys.update([path_key(row["original_source"]["path"]), path_key(row["source_copy"]["path"])])
        for item in row["files"]:
            expected_frozen_keys.update([path_key(item["original"]["path"]), path_key(item["copy"]["path"])])
    for row in external_map.values():
        expected_frozen_keys.update(path_key(item["path"]) for item in row["files"])
    check({path_key(row["path"]) for row in frozen} == expected_frozen_keys,
          "Frozen inputs do not equal the declared custody/source/boundary closure")
    expected_order = MODULES + ["Imports040All"]
    check([row["module"] for row in data["steps"]] == expected_order, "Wrong serial build order")
    integration = clean / "Imports040All.lean"
    check(integration.read_text(encoding="utf-8") ==
          "".join("import " + m + "\n" for m in MODULES), "Import-all content mismatch")
    check(graph["Imports040All"] == MODULES, "Integration graph mismatch")
    check(set(graph) == set(MODULES) | set(boundary_map) | {"Imports040All"}, "Unexpected local graph node")
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
        check(meta["role"] == ("batch" if name in sources else "integration"), "Compilation role mismatch")
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
        expected_input_keys = custody_keys | {path_key(row["original_source"]) for row in sources.values()}
        expected_input_keys.update([path_key(meta["source"]), path_key(common.TOOLCHAIN / "bin/lean.exe")])
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
                expected_input_keys.add(path_key(sources[dep]["source"]))
                expected_input_keys.update(path_key(p) for p in common.companions(clean / (dep + ".olean")))
            elif dep in boundary_map:
                check(row["kind"] == "pinned_pre040" and
                      path_key(resolved) == path_key(clean / "boundary" /
                      common.module_relative(dep, ".olean")), "Boundary import fallback")
                boundary_row = boundary_map[dep]
                required_inputs = [boundary_row["original_source"]["path"], boundary_row["source_copy"]["path"]]
                for item in boundary_row["files"]:
                    required_inputs.extend([item["original"]["path"], item["copy"]["path"]])
                check(all(path_key(p) in input_keys for p in required_inputs), "Boundary input evidence incomplete")
                expected_input_keys.update(path_key(p) for p in required_inputs)
            else:
                check(row["kind"] == "external_direct" and
                      path_key(resolved) == path_key(external_map[dep]["resolved"]), "Unknown import resolution")
                expected_input_keys.update(path_key(item["path"]) for item in external_map[dep]["files"])
        check(input_keys == expected_input_keys, "Compilation input snapshot differs from declared dependency closure")
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
    data = dict(data)
    data["audit_historical_evidence"] = common.snapshot(historical_evidence)
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
                      ROOT / "clean_continuation040.py", ROOT / "revise_continuation040.py",
                      ROOT / "CONTINUACAO040_DERIVACAO_PREVIA.md", ROOT / "CONTINUACAO040_PARECER.md",
                      DELIVERY])
        paths.update(Path(row["path"]) for row in build["audit_historical_evidence"])
        history = []
        for directory in sorted(ROOT.glob("CONTINUACAO040_CLEAN_*")):
            failure = directory / "FAILURE.json"
            if failure.exists():
                paths.add(failure)
                selected = [p for p in directory.iterdir()
                            if p.is_file() and p.suffix in {".lean", ".json", ".log", ".olean", ".private", ".server"}]
                paths.update(selected)
                history.append({"directory": str(directory), "failure": str(failure)})
        for pattern in ["*040*.bak_*", "CONTINUACAO040_DEVELOPMENT_*.json"] + [m + ".lean.bak_*" for m in MODULES]:
            paths.update(ROOT.glob(pattern))
        result = {"schema": "chatgpt.continuation040.v1", "created_utc": datetime.now(timezone.utc).isoformat(),
                  "status": "PASS", "scope": "modular stationarity, instantaneous-state clock obstruction, conditional Fisher and relative-entropy clocks, affine reparametrization and regional area controls",
                  "broad_quantum_gravity_goal": "OPEN", "h3_status": "OPEN", "canonical_gate_changed": False,
                  "modules": MODULES, "counts": totals, "fresh_clean_build": True,
                  "clean_build": common.record(BUILD), "clean_directory": build["clean_directory"],
                  "anonymous_instances_remaining": 0, "files": common.snapshot(paths),
                  "preserved_failed_attempts": history,
                  "boundary_limit": build["boundary"]["limitation"],
                  "historical_artifact_evidence": build["audit_historical_evidence"],
                  "evidence_limits": [
                      "The modular flow of a fixed state is stationary; this does not select a cubic clock coefficient or parametrize a nonconstant amplitude-state curve.",
                      "A differentiable bilateral reading of the instantaneous even state curve has zero derivative at the origin; history, orientation and one-sided readings are additional data outside that obstruction.",
                      "Fisher-length and relative-entropy clock constructions retain their explicit branch, orientation, normalization and regularity hypotheses; one-site results are not promoted to a general summable-profile theorem.",
                      "Quartic clock coefficients are compared in the inverse direction that parametrizes states by the optical time, only under the stated profile and screen hypotheses.",
                      "Affine reparametrization rigidity requires affineness on an interval; initial calibration alone does not identify optical and statistical time.",
                      "An angular area density also depends on tangent directions and their normalization; an algebra and state alone are not asserted to select that scalar.",
                      "H3 remains OPEN: neither a general heat-matter flux law nor a physical metric, screen or clock selection is supplied by this audit; a quartic mismatch is not a refutation of a merely quadratic statement.",
                      "Stage035/036/037 clean source, binary and metadata pins are checked in chronological override order, with no root olean fallback for those modules.",
                      "The 035 baseline copies are checked against exact instance-name insertions; their compiled bytes are not falsely identified with their original sources.",
                      "Historical compilation records are rechecked, not rerun. Audit-only historical evidence is recorded separately from the 040 frozen compilation inputs.",
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
        check(result["fresh_clean_build"] is True and result["canonical_gate_changed"] is False and
              result["broad_quantum_gravity_goal"] == "OPEN" and result["h3_status"] == "OPEN",
              "Manifest scope/guard mismatch")
        check(path_key(result["clean_directory"]) == path_key(build["clean_directory"]) and
              result["boundary_limit"] == build["boundary"]["limitation"], "Manifest build crosslink mismatch")
        check(result["historical_artifact_evidence"] == build["audit_historical_evidence"],
              "Manifest historical evidence crosslink mismatch")
        manifest_files = {path_key(row["path"]): row for row in result["files"]}
        check(len(manifest_files) == len(result["files"]), "Duplicate manifest file record")
        required = [*build["files"], *build["audit_historical_evidence"]]
        required.extend(common.record(p) for p in [BUILD, Path(__file__).resolve(),
                        ROOT / "clean_continuation035.py", ROOT / "clean_continuation040.py",
                        ROOT / "revise_continuation040.py", ROOT / "CONTINUACAO040_DERIVACAO_PREVIA.md",
                        ROOT / "CONTINUACAO040_PARECER.md", DELIVERY])
        for row in required:
            check(manifest_files.get(path_key(row["path"])) == row, "Missing or inconsistent sealed evidence")
        for row in result["files"]:
            verify_record(row)
    print(json.dumps({"status": "PASS", "files": len(result["files"]),
                      "modules": len(MODULES), **totals, "manifest": str(MANIFEST)}))

if __name__ == "__main__":
    main()
