"""Read-only audit by default; --write seals only new continuation036 artifacts."""
from pathlib import Path
import hashlib, json, re, sys, os
from datetime import datetime, timezone
import clean_continuation035 as common

ROOT = Path(__file__).resolve().parent
MODULES = ["OpticalTidalScreen", "OpticalScreenInvariant", "OpticalJacobiArea", "OpticalAreaFreedom"]
MANIFEST = ROOT / "CONTINUACAO036_MANIFESTO.json"
BUILD = ROOT / "CONTINUACAO036_CLEAN_BUILD.json"
DELIVERY = ROOT / "TUNEL/DO_CHATGPT/ENTREGA_036_ESPONTANEA_area_optica_e_liberdade_radiativa.md"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

def check(condition, message):
    if not condition:
        raise RuntimeError(message)

def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))

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
    check(namespaces == ["ChatgptAudit.Optical036"], "Unexpected namespace")
    instance_rows = common.instances(raw.decode("utf-8-sig"))
    check(not any(row["anonymous"] for row in instance_rows), "Anonymous instance")
    return {"theorems": sum(k in {"theorem", "lemma"} for k, _ in declarations),
            "definitions_including_structures": sum(k in {"def", "abbrev", "structure"} for k, _ in declarations),
            "structures": sum(k == "structure" for k, _ in declarations),
            "instances": len(instance_rows), "anonymous_instances": 0,
            "printed": ["ChatgptAudit.Optical036." + name for name in printed]}

def inspect_build():
    data = read_json(BUILD)
    check(data["status"] == "PASS" and data["fresh_clean_build"] is True, "No successful clean build")
    check(data.get("development_only") is False, "Development attempt cannot seal")
    check(data["modules"] == MODULES and data["build_order"] == MODULES, "Unexpected build batch")
    check(data["baseline_modules"] == [], "Unexpected rebuilt baseline")
    check(data["anonymous_instances_remaining"] == 0 and data["inputs_stable"] is True, "Dirty inputs")
    clean = Path(data["clean_directory"]).resolve(strict=True)
    check(clean.parent == ROOT and clean.name.startswith("CONTINUACAO036_CLEAN_"), "Wrong clean directory")
    check(data["integration_module"] == "Imports036All", "Missing integration module")
    check(data["lean_path"][0] == str(clean), "Wrong first import location")
    check(str(ROOT) not in data["lean_path"], "Root fallback forbidden")
    check(not any("tgl_kernel" in x and ".lake\\build\\lib\\lean" in x and ".lake\\packages" not in x
                  for x in data["lean_path"]), "Unrestricted canonical fallback forbidden")
    records = data["files"]
    check(len(records) == len({os.path.normcase(row["path"]) for row in records}), "Duplicate build record")
    for row in records:
        verify_record(row)
    recorded = {os.path.normcase(str(Path(row["path"]).resolve())): row for row in records}
    def require_covered(path):
        key = os.path.normcase(str(Path(path).resolve(strict=True)))
        check(key in recorded, "Uncovered build evidence: " + str(path))
        verify_record(recorded[key])
    for filename in ["BUILD_PLAN.json", "FROZEN_INPUTS.json", "FROZEN_INPUTS_AFTER.json", "Imports036All.lean"]:
        require_covered(clean / filename)
    plan = read_json(clean / "BUILD_PLAN.json")
    check(plan["build_order"] == MODULES and plan["clean_directory"] == str(clean), "Plan mismatch")
    check(plan["sources"] == data["sources"] and plan["lean_path"] == data["lean_path"], "Plan crosslink mismatch")
    frozen = read_json(clean / "FROZEN_INPUTS.json")
    check(bool(frozen) and frozen == read_json(clean / "FROZEN_INPUTS_AFTER.json"), "Frozen snapshot mismatch")
    for row in frozen:
        require_covered(row["path"])
        verify_record(row)
    package_root = common.KERNEL / ".lake/packages"
    package_dirs = sorted([p for p in package_root.iterdir() if p.is_dir()], key=lambda p: p.name)
    external_roots = [p / ".lake/build/lib/lean" for p in package_dirs
                      if (p / ".lake/build/lib/lean").is_dir()] + [common.TOOLCHAIN / "lib/lean"]
    check(data["lean_path"] == [str(clean), str(clean / "boundary"), *map(str, external_roots)],
          "Full LEAN_PATH mismatch")
    boundary = data["boundary"]
    check(Path(boundary["directory"]) == clean / "boundary", "Wrong boundary directory")
    historical = {}
    check([Path(row["path"]) for row in boundary["manifests"]] ==
          [ROOT / ("CONTINUACAO%03d_MANIFESTO.json" % i) for i in [29,32,33,34]], "Wrong historical manifests")
    for row in boundary["manifests"]:
        verify_record(row)
        require_covered(row["path"])
        historical.update(common.load_pins(Path(row["path"])))
    for row in boundary["modules"]:
        original, copied = row["original_source"], row["source_copy"]
        require_covered(original["path"])
        require_covered(copied["path"])
        check(Path(copied["path"]).resolve().is_relative_to(clean / "boundary_sources"), "Boundary source path")
        check(Path(original["path"]).read_bytes() == Path(copied["path"]).read_bytes(), "Boundary source copy")
        has_pin = os.path.normcase(str(Path(original["path"]).resolve())) in historical
        check(row["source_has_historical_pin"] is has_pin, "Historical pin flag mismatch")
        if has_pin:
            common.verify_pin(original["path"], historical)
            check(row["source_status"] == "PIN029_034_EXACT_BYTES", "Historical source status")
        else:
            check(row["module"].startswith(("TGL.", "TGLExt.")), "Unpinned bench source refused")
            check(row["source_status"] == "REAL_CURRENT_READ_NO_HISTORICAL_SOURCE_PIN", "Unpinned source status")
        check(common.imports(Path(copied["path"]).read_text(encoding="utf-8-sig")) == row["imports"],
              "Boundary source import mismatch")
        check(bool(row["files"]), "Empty boundary binary list")
        for item in row["files"]:
            old, new = item["original"], item["copy"]
            verify_record(old)
            verify_record(new)
            require_covered(old["path"])
            require_covered(new["path"])
            common.verify_pin(old["path"], historical)
            check(Path(new["path"]).resolve().is_relative_to(clean / "boundary"), "Boundary binary path")
            check(old["sha256"] == new["sha256"] and old["bytes"] == new["bytes"], "Binary copy mismatch")
    for row in boundary["external_direct_inputs"]:
        expected = next((p / common.module_relative(row["module"], ".olean") for p in external_roots
                         if (p / common.module_relative(row["module"], ".olean")).is_file()), None)
        check(expected is not None and expected.resolve() == Path(row["resolved"]).resolve(), "External resolution")
        for item in row["files"]:
            require_covered(item["path"])
            verify_record(item)
    sources = {row["module"]: row for row in data["sources"]}
    check(set(sources) == set(MODULES), "Wrong source set")
    totals = {"theorems": 0, "definitions_including_structures": 0, "structures": 0,
              "instances": 0, "anonymous_instances": 0}
    census = {}
    for module in MODULES:
        row = sources[module]
        original, copied = ROOT / (module + ".lean"), clean / (module + ".lean")
        check(Path(row["source"]) == copied and Path(row["original_source"]) == original, "Source path mismatch")
        check(copied.read_bytes() == original.read_bytes(), "Source copy differs")
        check(common.digest(original) == row["original_sha256"] == row["proof_sha256"], "Source pin mismatch")
        check(row["source_equals_original"] is True and row["transpositions"] == [], "Source transformed")
        census[module] = source_census(original)
        check(census[module]["printed"] == row["expected_axiom_rows"], "Print census mismatch")
        for key in totals:
            totals[key] += census[module][key]
    expected_order = MODULES + ["Imports036All"]
    check([row["module"] for row in data["steps"]] == expected_order, "Wrong serial build order")
    integration = clean / "Imports036All.lean"
    check(integration.read_text(encoding="utf-8") ==
          "".join("import " + m + "\n" for m in MODULES), "Import-all content mismatch")
    for step in data["steps"]:
        name = step["module"]
        metadata = Path(step["metadata"])
        check(metadata.parent.resolve() == clean, "Metadata escapes clean directory")
        require_covered(metadata)
        meta = read_json(metadata)
        check(meta["module"] == name and meta["exit_code"] == 0 and meta["passed"] is True,
              "Failed compilation")
        for key in ["source_stable", "inputs_stable", "fresh_clean_build", "axiom_coverage_exact"]:
            check(meta[key] is True, "Failed compilation guard: " + key)
        check(meta["issues"] == [] and meta["anonymous_instances"] == 0, "Compilation issue")
        check(bool(meta["inputs_before"]) and meta["inputs_before"] == meta["inputs_after"], "Inputs changed or absent")
        for row in meta["inputs_before"]:
            require_covered(row["path"])
            verify_record(row)
        for key in ["source", "olean", "log"]:
            require_covered(meta[key])
        for row in meta["import_resolutions"]:
            resolved = Path(row["resolved"]).resolve()
            require_covered(resolved)
            if row["kind"] == "rebuilt":
                check(resolved == clean / (row["module"] + ".olean"), "Rebuilt import fallback")
            elif row["kind"] == "pinned_pre036":
                check(resolved.is_relative_to(clean / "boundary"), "Boundary import fallback")
            else:
                check(row["kind"] == "external_direct" and
                      any(resolved.is_relative_to(p.resolve()) for p in external_roots), "Unknown import resolution")
        check(meta["cwd"] == str(clean) and meta["lean_path"] == data["lean_path"], "Environment mismatch")
        check(Path(meta["source"]) == clean / (name + ".lean"), "Wrong compiled source")
        check(Path(meta["olean"]) == clean / (name + ".olean"), "Wrong compiled binary")
        check(common.digest(meta["source"]) == meta["proof_sha256"], "Compiled source changed")
        check(common.digest(meta["olean"]) == meta["olean_sha256"], "Binary changed")
        check(common.digest(meta["log"]) == meta["log_sha256"], "Log changed")
        raw_log = Path(meta["log"]).read_text(encoding="utf-8")
        check("sorryAx" not in raw_log and not re.search(r"\b(?:error|warning)(?:\([^\n]*?\))?:", raw_log),
              "Error or warning in log")
        rows = common.parse_axioms(raw_log)
        printed = census[name]["printed"] if name in census else []
        check([row["declaration"] for row in rows] == printed == meta["expected_axiom_rows"], "Axiom mismatch")
        check(rows == meta["axiom_rows"], "Parsed axiom mismatch")
        for row in rows:
            check(set(row["axioms"]) <= ALLOWED_AXIOMS, "Unexpected axiom")
        for row in meta["output_artifacts"]:
            verify_record(row)
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
                      ROOT / "clean_continuation036.py", ROOT / "revise_continuation036.py",
                      ROOT / "CONTINUACAO036_DERIVACAO_PREVIA.md", ROOT / "CONTINUACAO036_PARECER.md",
                      DELIVERY])
        history = []
        for directory in sorted(ROOT.glob("CONTINUACAO036_CLEAN_*")):
            failure = directory / "FAILURE.json"
            if failure.exists():
                paths.add(failure)
                selected = [p for p in directory.iterdir()
                            if p.is_file() and p.suffix in {".lean", ".json", ".log"}]
                paths.update(selected)
                history.append({"directory": str(directory), "failure": str(failure)})
        for pattern in ["*036*.bak_*", "Optical*.lean.bak_*", "CONTINUACAO036_DEVELOPMENT_*.json"]:
            paths.update(ROOT.glob(pattern))
        result = {"schema": "chatgpt.continuation036.v1", "created_utc": datetime.now(timezone.utc).isoformat(),
                  "status": "PASS", "scope": "conditional optical geometry of the existing plane-wave family029",
                  "broad_quantum_gravity_goal": "OPEN", "canonical_gate_changed": False,
                  "modules": MODULES, "counts": totals, "fresh_clean_build": True,
                  "clean_build": common.record(BUILD), "clean_directory": build["clean_directory"],
                  "anonymous_instances_remaining": 0, "files": common.snapshot(paths),
                  "preserved_failed_attempts": history,
                  "boundary_limit": build["boundary"]["limitation"],
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
