"""Independent continuation049 audit. Default and --build-only never write.
--seal exclusively creates a new manifest after build and documentary checks.
Local Lean closure is all-new049; external direct imports are not a full package rebuild.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import re
import sys
import uuid

ROOT = Path(__file__).resolve().parent
KERNEL = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/tgl_kernel")
TOOLCHAIN = Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0")
MODULES = ["BoundedGraphOperator", "ClosedAntilinearStandardSubspace",
           "ContinuousModularMultipliers", "BoundedGraphStandardSubspace",
           "ContinuousModularDomain", "ContinuousModularStandardSubspace"]
INTEGRATION = "Imports049All"
NAMESPACE = "ChatgptAudit.Continuous049"
BUILD = ROOT / "CONTINUACAO049_CLEAN_BUILD.json"
RUNNER = ROOT / "clean_continuation049.py"
MANIFEST = ROOT / "CONTINUACAO049_MANIFESTO.json"
REVIEW = ROOT / "CONTINUACAO049_REVISAO_INDEPENDENTE.md"
REPORT = ROOT / "CONTINUACAO049_PARECER.md"
DELIVERY = ROOT / "TUNEL/DO_CHATGPT/ENTREGA_049_subespaco_padrao_continuo.md"
DERIVATIONS = [ROOT / name for name in [
    "CONTINUACAO049_DERIVACAO_PREVIA.md", "DERIVACAO049_INFRA.md",
    "DERIVACAO049_GRAFO_LIMITADO.md", "DERIVACAO049_SUBESPACO_PADRAO.md",
    "DERIVACAO049_MULTIPLICADORES.md", "DERIVACAO049_TOMITA_GRAFO.md",
    "DERIVACAO049_DOMINIO.md", "DERIVACAO049_INSTANCIA_CONTINUA.md"]]
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MODULE_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*")
INSTANCE_RE = re.compile(r"(?m)^[ \t]*(?:(?:local|scoped|noncomputable|unsafe)\s+)*instance\b")
AXIOM_RE = re.compile(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
BOUNDARY = "Direct imports and companions only; transitive package closure not measured."


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def key(path):
    return os.path.normcase(str(Path(path).resolve(strict=True)))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def record(path):
    path = Path(path).resolve(strict=True)
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def snapshot(paths):
    return [record(p) for p in sorted({Path(p).resolve(strict=True) for p in paths}, key=str)]


def unique_object(pairs):
    result = {}
    for name, value in pairs:
        check(name not in result, "Duplicate JSON key: " + name)
        result[name] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_bytes().decode("utf-8-sig"), object_pairs_hook=unique_object)


def verify_record(row):
    check(isinstance(row, dict) and set(row) == {"path", "bytes", "sha256"}, "Invalid file record")
    check(isinstance(row["path"], str) and Path(row["path"]).is_absolute(), "Nonabsolute artifact path")
    check(type(row["bytes"]) is int and row["bytes"] >= 0, "Invalid artifact size")
    check(re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None, "Invalid SHA256")
    check(record(row["path"]) == row, "Changed artifact: " + row["path"])


def indexed(rows, label):
    check(isinstance(rows, list), "Expected file list: " + label)
    result = {}
    for row in rows:
        verify_record(row)
        k = key(row["path"])
        check(k not in result, "Duplicate artifact in " + label + ": " + row["path"])
        result[k] = row
    return result


def require_covered(path, records, label):
    check(key(path) in records, "Uncovered " + label + ": " + str(path))
    check(records[key(path)] == record(path), "Record crosslink mismatch: " + str(path))


def internal(path, clean):
    result = Path(path).resolve(strict=True)
    check(result.is_relative_to(clean), "Artifact escapes clean directory: " + str(path))
    return result


def module_file(directory, name, suffix):
    check(MODULE_RE.fullmatch(name) is not None, "Invalid Lean module name")
    return directory / Path(*name.split(".")).with_suffix(suffix)


def mask_lean(text):
    """Mask comments/strings; preserve offsets for independently counted declarations."""
    chars = list(text)
    i, depth, in_string = 0, 0, False
    while i < len(text):
        if depth:
            if text.startswith("/-", i):
                chars[i:i+2] = "  "; depth += 1; i += 2
            elif text.startswith("-/", i):
                chars[i:i+2] = "  "; depth -= 1; i += 2
            else:
                if text[i] not in "\r\n": chars[i] = " "
                i += 1
        elif in_string:
            if text[i] == "\\":
                chars[i] = " "; i += 1
                if i < len(text):
                    if text[i] not in "\r\n": chars[i] = " "
                    i += 1
            else:
                if text[i] == '"': in_string = False
                if text[i] not in "\r\n": chars[i] = " "
                i += 1
        elif text.startswith("--", i):
            end = text.find("\n", i)
            if end < 0: end = len(text)
            for j in range(i, end):
                if text[j] != "\r": chars[j] = " "
            i = end
        elif text.startswith("/-", i):
            chars[i:i+2] = "  "; depth = 1; i += 2
        elif text[i] == '"':
            chars[i] = " "; in_string = True; i += 1
        else:
            i += 1
    check(depth == 0 and not in_string, "Unterminated Lean comment/string")
    return "".join(chars)


def imports(text):
    result = []
    code = mask_lean(text)
    for match in re.finditer(r"(?m)^\ufeff?[ \t]*(?:(?:public|private)\s+)?import\s+([^\r\n]+)", code):
        names = match.group(1).split()
        if names[:1] == ["all"]: names = names[1:]
        check(bool(names), "Empty import")
        for name in names:
            check(MODULE_RE.fullmatch(name) is not None, "Unsupported import: " + name)
            if name not in result: result.append(name)
    return result


def source_info(text, module):
    code = mask_lean(text)
    check(not re.search(r"\b(?:sorry|admit|axiom|native_decide|unsafe)\b", code), "Forbidden proof token: " + module)
    check(not re.search(r"set_option\s+linter\.[\w.]+\s+false", code), "Disabled linter: " + module)
    check(not re.search(r"(?m)^\s*(?:#(?:eval|check|reduce|synth|run)|run_elab|initialize|builtin_initialize|macro|elab|syntax)\b", code),
          "Unsupported metaprogramming/output command: " + module)
    namespaces = re.findall(r"(?m)^namespace\s+([\w.]+)", code)
    check(namespaces == [NAMESPACE], "Unexpected namespace: " + module)
    rows = []
    for ordinal, match in enumerate(INSTANCE_RE.finditer(code), 1):
        tail = code[match.end():].lstrip()
        found = re.match(r"(?:[A-Za-z_][\w']*|\u00ab[^\u00bb]+\u00bb)", tail)
        check(found is not None and found.group(0) != "where", "Anonymous instance: " + module)
        rows.append({"ordinal": ordinal, "line": text.count("\n", 0, match.start()) + 1,
                     "name": found.group(0), "anonymous": False, "insertion_offset": match.end()})
    declaration_matches = list(re.finditer(r"(?m)^[ \t]*(?:(?:noncomputable)\s+)?(theorem|lemma|def|abbrev|structure)\s+([\w.']+)", code))
    declarations = [(m.group(1), m.group(2)) for m in declaration_matches]
    # This is a bounded recognizer, not a Lean parser: never silently omit unsupported declarations.
    covered_keywords = {m.start(1) for m in declaration_matches}
    for m in INSTANCE_RE.finditer(code):
        covered_keywords.add(m.start() + re.search(r"\binstance\b", m.group(0)).start())
    all_keywords = {m.start() for m in re.finditer(
        r"(?<![\w.'])\b(?:theorem|lemma|def|abbrev|structure|instance|class|inductive|opaque)\b", code)}
    check(all_keywords == covered_keywords, "Unsupported/uncensused declaration syntax: " + module)
    printed = re.findall(r"(?m)^[ \t]*#print\s+axioms\s+([\w.']+)", code)
    check(not re.search(r"(?m)^\s*#print\s+(?!axioms\b)", code), "Unsupported print command")
    named = [name for _, name in declarations] + [row["name"] for row in rows]
    check(len(named) == len(set(named)), "Duplicate source declaration: " + module)
    check(len(printed) == len(set(printed)) and set(printed) == set(named), "Axiom coverage: " + module)
    expected = [n if n.startswith(NAMESPACE + ".") else NAMESPACE + "." + n for n in printed]
    instance_names = {r["name"] for r in rows}
    return {"namespace": NAMESPACE, "expected_axiom_rows": expected,
            "instance_axiom_rows": [expected[i] for i, n in enumerate(printed) if n in instance_names],
            "axiom_prints": len(expected), "theorems": sum(k in {"theorem", "lemma"} for k, _ in declarations),
            "definitions": sum(k in {"def", "abbrev", "structure"} for k, _ in declarations),
            "instances": rows, "anonymous_instances": 0}


def log_rows(raw):
    output = raw.decode("utf-8")
    check("sorryAx" not in output, "sorryAx in Lean output")
    check(not re.search(r"\b(?:error|warning)(?:\([^\n]*?\))?:", output, re.IGNORECASE), "Lean error/warning")
    rows = [{"declaration": m.group(1), "axioms": [a.strip() for a in (m.group(2) or "").split(",") if a.strip()]}
            for m in AXIOM_RE.finditer(output)]
    check(not AXIOM_RE.sub("", output).strip(), "Unrecognized Lean output beyond axiom prints")
    check(all(set(r["axioms"]) <= ALLOWED_AXIOMS for r in rows), "Unpermitted axiom")
    return rows


def companions(olean):
    check(olean.is_file(), "Missing olean: " + str(olean))
    return [olean] + [Path(str(olean) + s) for s in [".private", ".server"] if Path(str(olean) + s).is_file()]


def runner_contract():
    """Check fixed constants without importing/executing the runner under audit."""
    tree = ast.parse(RUNNER.read_text(encoding="utf-8-sig"))
    values = {n.targets[0].id: n.value for n in tree.body
              if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)}
    for name, expected in [("MODULES", MODULES), ("INTEGRATION", INTEGRATION), ("NAMESPACE", NAMESPACE)]:
        check(ast.literal_eval(values[name]) == expected, "Runner contract differs: " + name)
    for name, expected in [("KERNEL", KERNEL), ("TOOLCHAIN", TOOLCHAIN)]:
        call = values[name]
        check(isinstance(call, ast.Call) and len(call.args) == 1, "Unrecognized configured path")
        check(key(ast.literal_eval(call.args[0])) == key(expected), "Runner path differs: " + name)


def inspect_build():
    runner_contract()
    for path in DERIVATIONS: check(path.is_file(), "Missing prior derivation: " + str(path))
    d = read_json(BUILD)
    check(d["schema"] == "chatgpt.clean049.build.v1" and d["status"] == "PASS", "Invalid build marker")
    check(d["development_only"] is False and d["fresh_clean_build"] is True and d["inputs_stable"] is True,
          "Development/nonfresh/unstable build")
    check(d["H3"] == "OPEN" and d["physical_reconstruction"] == "OPEN" and d["canonical_gate_changed"] is False,
          "Build scientific scope changed")
    clean = Path(d["clean_directory"]).resolve(strict=True)
    check(clean.parent == ROOT and re.fullmatch(r"CONTINUACAO049_CLEAN_\d{8}_\d{6}_\d{6}", clean.name), "Invalid clean root")
    files = indexed(d["build_files"], "build_files")
    check(set(files) == {key(p) for p in clean.rglob("*") if p.is_file()}, "Clean inventory is not exact")
    for row in d["build_files"]: internal(row["path"], clean)
    check(not (clean / "FAILURE.json").exists(), "Failure file in successful build")
    before_path, after_path, plan_path = [clean / n for n in ["FROZEN_INPUTS.json", "FROZEN_INPUTS_AFTER.json", "BUILD_PLAN.json"]]
    for p in [before_path, after_path, plan_path]: require_covered(p, files, "build document")
    before, after, plan = read_json(before_path), read_json(after_path), read_json(plan_path)
    check(before == after == d["frozen_before"] == d["frozen_after"], "Frozen snapshots disagree")
    frozen = indexed(before, "frozen inputs")
    check(bool(frozen), "Empty input snapshot")
    check(plan["schema"] == "chatgpt.clean049.plan.v1", "Invalid build plan")

    originals, graph, infos, order, visiting = {}, {}, {}, [], set()
    def visit(module):
        if module in order: return
        check(module not in visiting, "Local import cycle")
        visiting.add(module)
        original, copy = module_file(ROOT, module, ".lean"), module_file(clean, module, ".lean")
        require_covered(copy, files, "copied source")
        require_covered(original, frozen, "original source")
        require_covered(copy, frozen, "frozen source copy")
        raw = original.read_bytes()
        check(raw == copy.read_bytes(), "Source copy is not exact: " + module)
        text = raw.decode("utf-8-sig")
        info, deps = source_info(text, module), imports(text)
        for dep in deps:
            if dep in MODULES: visit(dep)
            else: check(dep.startswith("Mathlib."), "Undeclared local/historical import: " + dep)
        originals[module], graph[module], infos[module] = record(original), deps, info
        order.append(module); visiting.remove(module)
    for module in MODULES: visit(module)
    check(set(order) == set(MODULES) and len(order) == len(MODULES), "Incomplete final module set")
    integration = module_file(clean, INTEGRATION, ".lean")
    check(integration.read_bytes() == ("".join("import " + m + "\n" for m in order)).encode("utf-8"), "Integration source differs")
    require_covered(integration, frozen, "integration source")
    graph[INTEGRATION] = list(order)
    infos[INTEGRATION] = {"expected_axiom_rows": [], "axiom_prints": 0, "theorems": 0,
                          "definitions": 0, "instances": [], "anonymous_instances": 0}
    check(d["modules"] == order and d["integration_module"] == INTEGRATION, "Final module/order mismatch")
    for field, expected in [("build_order", order + [INTEGRATION]), ("graph", graph),
                            ("original_sources", originals), ("source_info", infos)]:
        check(d[field] == expected and plan[field] == expected, "Plan/build/source crosslink: " + field)

    packages = sorted(p for p in (KERNEL / ".lake/packages").iterdir() if p.is_dir())
    external_roots = [p / ".lake/build/lib/lean" for p in packages if (p / ".lake/build/lib/lean").is_dir()]
    external_roots.append(TOOLCHAIN / "lib/lean")
    lean_path = [str(p) for p in [clean, *external_roots]]
    check(d["lean_path"] == plan["lean_path"] == lean_path, "LEAN_PATH differs from package/stdlib roots")
    check(key(ROOT) not in {key(p) for p in lean_path}, "Root fallback in LEAN_PATH")
    canonical_build = KERNEL / ".lake/build/lib/lean"
    if canonical_build.exists(): check(key(canonical_build) not in {key(p) for p in lean_path}, "Canonical fallback")
    lean = TOOLCHAIN / "bin/lean.exe"
    check(d["toolchain"] == record(lean), "Toolchain pin mismatch")
    expected_frozen = {lean, RUNNER, *DERIVATIONS, *ROOT.glob("DERIVACAO049_*.md")}
    for cfg in [KERNEL / n for n in ["lean-toolchain", "lake-manifest.json", "lakefile.toml", "lakefile.lean"]]:
        if cfg.is_file(): expected_frozen.add(cfg)
    for package in packages:
        for name in ["lean-toolchain", "lake-manifest.json"]:
            if (package / name).is_file(): expected_frozen.add(package / name)
    external = {}
    for dep in sorted({name for names in graph.values() for name in names if name not in MODULES}):
        check(not module_file(clean, dep, ".olean").exists(), "External module shadowed in clean: " + dep)
        candidates = [module_file(p, dep, ".olean") for p in external_roots]
        found = [p for p in candidates if p.is_file()]
        check(len(found) == 1, "External resolution not unique: " + dep)
        artifacts = companions(found[0])
        external[dep] = {"resolved": str(found[0]), "files": snapshot(artifacts)}
        expected_frozen.update(artifacts)
    check(d["external_direct_imports"] == plan["external_direct_imports"] == external, "External import/artifact crosslink")
    check(d["external_boundary"] == plan["external_boundary"] == BOUNDARY, "External trust boundary changed")
    for module in order:
        expected_frozen.update([module_file(ROOT, module, ".lean"), module_file(clean, module, ".lean")])
    expected_frozen.add(integration)
    check(before == snapshot(expected_frozen), "Frozen input coverage is not exact")

    check(len(d["steps"]) == len(order) + 1, "Missing integration/compilation step")
    expected_files = {before_path, after_path, plan_path, integration}
    expected_files.update(module_file(clean, module, ".lean") for module in order)
    previous_end = datetime.fromisoformat(plan["created_utc"])
    for index, module in enumerate(order + [INTEGRATION], 1):
        meta_path = clean / f"{index:02d}_{module}.json"
        log = clean / f"{index:02d}_{module}.log"
        source, olean = module_file(clean, module, ".lean"), module_file(clean, module, ".olean")
        check(d["steps"][index - 1] == record(meta_path), "Step metadata pin/order mismatch")
        for p in [meta_path, log, source, olean]: require_covered(p, files, "step artifact")
        m = read_json(meta_path)
        check(m["module"] == module and m["passed"] is True and m["exit_code"] == 0, "Unsuccessful step")
        check(m["inputs_stable"] is True and m["axiom_coverage_exact"] is True and m["issues"] == [], "Step verification failure")
        check(m["cwd"] == str(clean) and m["lean_path"] == lean_path, "Step environment mismatch")
        check(m["command"] == [str(lean), "-o", str(olean), str(source)], "Unexpected Lean invocation")
        check(m["source"] == record(source) and m["log"] == record(log), "Step source/log pins differ")
        check(m["frozen_input_snapshot"] == record(before_path), "Step snapshot crosslink differs")
        artifacts = companions(olean)
        check(m["output_artifacts"] == snapshot(artifacts), "Output artifact set differs")
        for artifact in artifacts: require_covered(artifact, files, "output companion")
        rows = log_rows(log.read_bytes())
        check(m["axiom_rows"] == rows and [r["declaration"] for r in rows] == infos[module]["expected_axiom_rows"], "Axiom rows/order differ")
        check(m["source_info"] == infos[module], "Metadata source census differs")
        start, end = datetime.fromisoformat(m["started_utc"]), datetime.fromisoformat(m["ended_utc"])
        check(start.tzinfo is not None and end.tzinfo is not None and previous_end <= start <= end, "Nonserial/invalid timestamps")
        previous_end = end
        expected_files.update([meta_path, log, *artifacts])
    check(previous_end <= datetime.fromisoformat(d["created_utc"]), "Marker predates finished build")
    check(set(files) == {key(p) for p in expected_files}, "Unexpected/missing clean artifact")
    totals = {k: sum(infos[m][k] for m in order) for k in ["theorems", "definitions", "axiom_prints"]}
    totals["instances"] = sum(len(infos[m]["instances"]) for m in order)
    check(d["totals"] == totals and totals["axiom_prints"] == sum(totals[k] for k in ["theorems", "definitions", "instances"]), "Build census mismatch")
    d["audit_evidence"] = snapshot([BUILD, *[Path(r["path"]) for r in before + d["build_files"]]])
    return d, totals


def exclusive_json(path, value):
    check(path.parent.resolve() == ROOT and not path.exists(), "Existing/outside seal cannot be written")
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temp = path.with_name(path.name + ".tmp_" + uuid.uuid4().hex)
    with temp.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    check(temp.read_bytes() == raw and not path.exists(), "Temporary seal verification failed")
    temp.rename(path)
    check(path.read_bytes() == raw, "Final seal verification failed")


def documentary_paths():
    result = {RUNNER, Path(__file__).resolve(), BUILD, REVIEW, REPORT, DELIVERY, *DERIVATIONS}
    result.update(ROOT.glob("DERIVACAO049_*.md"))
    result.update(module_file(ROOT, m, ".lean") for m in MODULES)
    for name in ["finalize_reports049.py", "revise_continuation049.py", "probe_continuation049.py"]:
        if (ROOT / name).is_file(): result.add(ROOT / name)
    return result


def prior_attempt_paths():
    """Preserve available local failed/development evidence, without treating it as passed input."""
    result = set()
    for pattern in ["CONTINUACAO049_DEVELOPMENT_*", "CONTINUACAO049_CLEAN_*", "DEV049_*"]:
        for path in ROOT.glob(pattern):
            if path.is_file() and path.suffix == ".json": result.add(path)
            elif path.is_dir():
                result.update(p for p in path.rglob("*") if p.is_file() and p.suffix in {".lean", ".log", ".json"})
    for pattern in ["*049*.bak_*"] + [m + ".lean.bak_*" for m in MODULES]:
        result.update(p for p in ROOT.glob(pattern) if p.is_file())
    return result


def main():
    mode = sys.argv[1:]
    check(mode in [[], ["--build-only"], ["--seal"]], "Only --build-only or --seal accepted")
    if mode == ["--seal"]: check(not MANIFEST.exists(), "Continuation049 is already sealed")
    if mode == []: check(MANIFEST.is_file(), "Default verification requires the seal")
    build, counts = inspect_build()
    if mode == ["--build-only"]:
        print(json.dumps({"status": "BUILD_PASS", "sealed": False, "counts": counts,
              "build_files": len(build["build_files"]), "frozen_inputs": len(build["frozen_before"]),
              "audited_files": len(build["audit_evidence"]), "historical_records": 0,
              "steps": len(build["steps"]), "canonical_gate_changed": False}))
        return
    mandatory = documentary_paths()
    for path in mandatory: check(path.is_file(), "Missing documentary evidence: " + str(path))
    review = REVIEW.read_text(encoding="utf-8")
    check("BUILD_PASS" in review, "Independent review lacks build result")
    check("Build SHA256: " + digest(BUILD) in review, "Independent review belongs to another build digest")
    check("Diretório final: " + Path(build["clean_directory"]).as_posix() in review, "Independent review belongs to another clean directory")
    if mode == ["--seal"]:
        evidence = {Path(r["path"]) for r in build["audit_evidence"]} | mandatory | prior_attempt_paths()
        manifest = {"schema": "chatgpt.continuation049.v1", "created_utc": datetime.now(timezone.utc).isoformat(),
                    "status": "PASS", "scope": "Explicit continuous multiplier model and standard real subspace; conclusions limited to compiled declarations",
                    "H3": "OPEN", "physical_reconstruction": "OPEN", "broad_quantum_gravity_goal": "OPEN",
                    "canonical_gate_changed": False, "counts": counts, "modules": build["modules"],
                    "new_modules": build["modules"], "recompiled_upstream_modules": [],
                    "clean_directory": build["clean_directory"], "fresh_clean_build": True,
                    "clean_build": record(BUILD), "files": snapshot(evidence),
                    "limitations": [BOUNDARY, "No historical Chatgpt/canonical oleans are used for the local Lean closure.",
                        "Frozen inputs before/after are stored; per-step metadata pins that snapshot and records the runner's stability result.",
                        "No full external source-to-binary reconstruction is claimed.",
                        "Compilation alone does not identify a physical algebra/state, spacetime net, Bisognano-Wichmann, H3, or alter the canonical gate."]}
        exclusive_json(MANIFEST, manifest)
    manifest = read_json(MANIFEST)
    check(manifest["schema"] == "chatgpt.continuation049.v1" and manifest["status"] == "PASS", "Invalid seal")
    check(manifest["H3"] == manifest["physical_reconstruction"] == manifest["broad_quantum_gravity_goal"] == "OPEN"
          and manifest["canonical_gate_changed"] is False, "Seal scientific scope changed")
    check(manifest["counts"] == counts and manifest["modules"] == manifest["new_modules"] == build["modules"]
          and manifest["recompiled_upstream_modules"] == [], "Sealed census/module mismatch")
    check(manifest["clean_build"] == record(BUILD) and key(manifest["clean_directory"]) == key(build["clean_directory"])
          and manifest["fresh_clean_build"] is True, "Seal/build crosslink differs")
    files = indexed(manifest["files"], "seal")
    for row in build["audit_evidence"]: require_covered(row["path"], files, "sealed build evidence")
    for path in mandatory: require_covered(path, files, "sealed documentary evidence")
    print(json.dumps({"status": "PASS", "sealed": True, "read_only": mode != ["--seal"], "counts": counts,
          "files": len(files), "steps": len(build["steps"]), "H3": "OPEN", "physical_reconstruction": "OPEN",
          "broad_quantum_gravity_goal": "OPEN", "canonical_gate_changed": False}))


if __name__ == "__main__":
    main()
