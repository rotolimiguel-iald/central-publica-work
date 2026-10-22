"""Fresh, serial continuation 054 build; writes only new artifacts under Chatgpt.

Run this script explicitly with Python. Merely reading or importing it does not build.
Historical dependencies, including the verified clean035, clean036, and clean037 outputs, are copied, pinned to manifests029/032/033/034/035/036/037/040/041/043/045/046/047/052/053, and not rebuilt.
Individual canonical source files without historical pins are hashed on this read
only for import discovery; this does not establish source-to-olean provenance.
External package dependencies remain a declared read-only boundary.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import subprocess
import sys
import traceback

ROOT = Path(__file__).resolve().parent
KERNEL = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/tgl_kernel")
TOOLCHAIN = Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0")
BASELINE = []
ALL_MODULES = ['PolarizerModularCost', 'PolarizerCostSeries', 'TowerModularCost', 'ModularCostDerivative']
MODULES = list(ALL_MODULES)
DEVELOPMENT = len(sys.argv) == 3 and sys.argv[1] in {"--development", "--module"}
if len(sys.argv) > 1 and not DEVELOPMENT:
    raise RuntimeError("Only --development N or --module NAME is accepted")
if DEVELOPMENT and sys.argv[1] == "--development":
    count = int(sys.argv[2])
    if not 1 <= count <= len(ALL_MODULES):
        raise RuntimeError("Invalid development prefix")
    REQUESTED = ALL_MODULES[:count]
elif DEVELOPMENT:
    if sys.argv[2] not in ALL_MODULES:
        raise RuntimeError("Unknown development module")
    REQUESTED = [sys.argv[2]]
else:
    REQUESTED = list(ALL_MODULES)
BUILD_ORDER = BASELINE + MODULES
INTEGRATION = "Imports054All"
MARKER = ROOT / ("CONTINUACAO054_DEVELOPMENT_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f") + ".json" if DEVELOPMENT else "CONTINUACAO054_CLEAN_BUILD.json")
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MODULE_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*")
INSTANCE_RE = re.compile(
    r"(?m)^[ \t]*(?:(?:local|scoped|noncomputable|unsafe)\s+)*instance\b"
)


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def record(path):
    path = Path(path).resolve(strict=True)
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": digest(path)}


def new_bytes(path, raw, allow_empty=False):
    path = Path(path)
    if not path.resolve().is_relative_to(ROOT) or path.exists() or (not raw and not allow_empty):
        raise RuntimeError(f"Exclusive nonempty output refused: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.stat().st_size != len(raw) or temporary.read_bytes() != raw:
        raise RuntimeError(f"Temporary verification failed: {temporary}")
    temporary.rename(path)
    if path.read_bytes() != raw:
        raise RuntimeError(f"Final verification failed: {path}")


def new_json(path, data):
    new_bytes(path, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def mask_lean(text):
    """Mask nested comments and strings, preserving every character offset."""
    chars = list(text)
    i = 0
    depth = 0
    string = False
    while i < len(text):
        if depth:
            if text.startswith("/-", i):
                chars[i:i+2] = "  "
                depth += 1
                i += 2
            elif text.startswith("-/", i):
                chars[i:i+2] = "  "
                depth -= 1
                i += 2
            else:
                if text[i] not in "\r\n":
                    chars[i] = " "
                i += 1
        elif string:
            if text[i] == "\\":
                chars[i] = " "
                i += 1
                if i < len(text):
                    if text[i] not in "\r\n":
                        chars[i] = " "
                    i += 1
            else:
                if text[i] == '"':
                    string = False
                if text[i] not in "\r\n":
                    chars[i] = " "
                i += 1
        elif text.startswith("--", i):
            end = text.find("\n", i)
            if end < 0:
                end = len(text)
            for j in range(i, end):
                if text[j] != "\r":
                    chars[j] = " "
            i = end
        elif text.startswith("/-", i):
            chars[i:i+2] = "  "
            depth = 1
            i += 2
        elif text[i] == '"':
            chars[i] = " "
            string = True
            i += 1
        else:
            i += 1
    if depth or string:
        raise RuntimeError("Unterminated Lean comment or string")
    return "".join(chars)


def imports(text):
    result = []
    code = mask_lean(text)
    for match in re.finditer(r"(?m)^\ufeff?[ \t]*(?:(?:public|private)\s+)?import\s+([^\r\n]+)", code):
        tokens = match.group(1).split()
        if tokens[:1] == ["all"]:
            tokens = tokens[1:]
        if not tokens:
            raise RuntimeError("Empty import")
        for name in tokens:
            if not MODULE_RE.fullmatch(name):
                raise RuntimeError(f"Unsupported import syntax: {name}")
            if name not in result:
                result.append(name)
    return result


def instances(text):
    code = mask_lean(text)
    result = []
    for ordinal, match in enumerate(INSTANCE_RE.finditer(code), 1):
        tail = code[match.end():].lstrip()
        name = re.match(r"(?:[A-Za-z_][\w']*|\u00ab[^\u00bb]+\u00bb)", tail)
        anonymous = name is None or name.group(0) in {"where"}
        result.append({
            "ordinal": ordinal,
            "line": text.count("\n", 0, match.start()) + 1,
            "name": None if anonymous else name.group(0),
            "anonymous": anonymous,
            "insertion_offset": match.end(),
        })
    return result


def name_baseline_instances(module, raw):
    text = raw.decode("utf-8")
    changes = []
    for row in instances(text):
        if row["anonymous"]:
            name = f"inst_{module}_{row['ordinal']}"
            if re.search(r"\b" + re.escape(name) + r"\b", mask_lean(text)):
                raise RuntimeError(f"Instance name already present: {name}")
            changes.append({**row, "new_name": name})
    changed = text
    for row in reversed(changes):
        pos = row["insertion_offset"]
        changed = changed[:pos] + " " + row["new_name"] + changed[pos:]
    if any(row["anonymous"] for row in instances(changed)):
        raise RuntimeError(f"Anonymous instance remains in baseline copy: {module}")
    return changed.encode("utf-8"), changes


def checked_source(text, module):
    code = mask_lean(text)
    if re.search(r"\b(?:sorry|admit|axiom|native_decide|unsafe)\b", code):
        raise RuntimeError(f"Forbidden proof token in {module}")
    if re.search(r"set_option\s+linter\.[\w.]+\s+false", code):
        raise RuntimeError(f"Disabled linter in {module}")
    if re.search(r"(?m)^\s*(?:#(?:eval|check|reduce|synth|run)|run_elab|initialize|builtin_initialize|macro|elab|syntax)\b", code):
        raise RuntimeError(f"Unsupported metaprogramming/output command: {module}")
    if re.search(r"(?m)^\s*#print\s+(?!axioms\b)", code):
        raise RuntimeError(f"Unsupported print command: {module}")
    rows = instances(text)
    if any(row["anonymous"] for row in rows):
        raise RuntimeError(f"Anonymous instance in build batch: {module}")
    namespaces = re.findall(r"(?m)^namespace\s+([\w.]+)", code)
    if len(namespaces) != 1:
        raise RuntimeError(f"Expected one namespace in {module}")
    matches = list(re.finditer(r"(?m)^[ \t]*(?:noncomputable\s+)?(theorem|lemma|def|abbrev|structure)\s+([\w.']+)", code))
    declarations = [(m.group(1), m.group(2)) for m in matches]
    covered = {m.start(1) for m in matches}
    for m in INSTANCE_RE.finditer(code):
        covered.add(m.start() + re.search(r"\binstance\b", m.group(0)).start())
    keywords = {m.start() for m in re.finditer(
        r"(?<![\w.'])\b(?:theorem|lemma|def|abbrev|structure|instance|class|inductive|opaque)\b", code)}
    if covered != keywords:
        raise RuntimeError(f"Unsupported or uncounted declaration in {module}")
    printed = re.findall(r"(?m)^#print\s+axioms\s+([\w.]+)", code)
    theorems = [name for kind, name in declarations if kind in {"theorem", "lemma"}]
    # Named instances are declarations to audit, but are not counted as definitions.
    instance_names = [row["name"] for row in rows]
    declared_names = [name for _, name in declarations] + instance_names
    if len(declared_names) != len(set(declared_names)):
        raise RuntimeError(f"Duplicate source declaration in {module}")
    if len(printed) != len(set(printed)) or set(declared_names) != set(printed):
        raise RuntimeError(f"Axiom print coverage mismatch in {module}")
    qualified = [name if name.startswith(namespaces[0] + ".") else namespaces[0] + "." + name
                 for name in printed]
    instance_axiom_rows = [qualified[i] for i, name in enumerate(printed) if name in instance_names]
    return {"namespace": namespaces[0], "expected_axiom_rows": qualified,
            "instance_axiom_rows": instance_axiom_rows, "axiom_prints": len(qualified),
            "theorems": len(theorems), "definitions": sum(k in {"def", "abbrev", "structure"} for k, _ in declarations),
            "instances": rows, "anonymous_instances": 0}


def parse_axioms(output):
    pattern = r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)"
    rows = []
    for match in re.finditer(pattern, output):
        names = [x.strip() for x in (match.group(2) or "").split(",") if x.strip()]
        rows.append({"declaration": match.group(1), "axioms": names})
    if re.sub(pattern, "", output).strip():
        raise RuntimeError("Unrecognized Lean output beyond axiom prints")
    return rows


def module_relative(name, suffix):
    if not MODULE_RE.fullmatch(name):
        raise RuntimeError(f"Invalid module: {name}")
    return Path(*name.split(".")).with_suffix(suffix)


def load_pins(path):
    raw = path.read_bytes()
    data = json.loads(raw.decode("utf-8-sig"))
    return {os.path.normcase(str(Path(row["path"]).resolve())): row
            for row in data["files"]}


def verify_pin(path, pins):
    row = record(path)
    key = os.path.normcase(row["path"])
    expected = pins.get(key)
    if expected is None or expected["sha256"].lower() != row["sha256"] or expected["bytes"] != row["bytes"]:
        raise RuntimeError(f"Source/binary not in exact sealed boundary: {path}")
    return row


def companions(olean):
    result = [olean]
    for suffix in [".private", ".server"]:
        extra = Path(str(olean) + suffix)
        if extra.is_file():
            result.append(extra)
    return result


def snapshot(paths):
    return [record(path) for path in sorted({Path(p).resolve() for p in paths}, key=str)]


def run_build():
    global MODULES, BUILD_ORDER
    order, visiting = [], set()
    def visit_new(module):
        if module in order:
            return
        if module in visiting:
            raise RuntimeError("New-module cycle")
        visiting.add(module)
        for dep in imports((ROOT/(module+".lean")).read_text(encoding="utf-8")):
            if dep in ALL_MODULES:
                visit_new(dep)
        visiting.remove(module)
        order.append(module)
    for module in REQUESTED:
        visit_new(module)
    MODULES = order
    BUILD_ORDER = BASELINE + MODULES
    if MARKER.exists():
        raise RuntimeError(f"Success marker already exists; no overwrite: {MARKER}")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    clean = ROOT / (("CONTINUACAO054_DEVELOPMENT_" if DEVELOPMENT else "CONTINUACAO054_CLEAN_") + stamp)
    clean.mkdir(exist_ok=False)
    steps = []
    try:
        boundary_dir = clean / "boundary"
        boundary_dir.mkdir(exist_ok=False)
        boundary_sources = clean / "boundary_sources"
        boundary_sources.mkdir(exist_ok=False)
        manifests = {i: ROOT / f"CONTINUACAO{i:03d}_MANIFESTO.json" for i in [29, 32, 33, 34, 35, 36, 37, 40, 41, 43, 45, 46, 47, 52, 53]}
        pins = {i: load_pins(path) for i, path in manifests.items()}
        boundary_pins = {}
        for index in sorted(pins):
            boundary_pins.update(pins[index])
        previous_build_paths = []
        overrides = {}
        for old_index in [35, 36, 37, 40, 41, 43, 45, 46, 47, 52, 53]:
            previous_build_path = ROOT / f"CONTINUACAO{old_index:03d}_CLEAN_BUILD.json"
            verify_pin(previous_build_path, pins[old_index])
            previous_build = json.loads(previous_build_path.read_text(encoding="utf-8"))
            if previous_build["status"] != "PASS" or previous_build.get("development_only", False):
                raise RuntimeError(f"No verified final{old_index} dependency boundary")
            previous_build_paths.append(previous_build_path)
            for row in previous_build["sources"]:
                src = Path(row["source"])
                binary = Path(previous_build["clean_directory"]) / module_relative(row["module"], ".olean")
                verify_pin(src, pins[old_index])
                verify_pin(binary, pins[old_index])
                overrides[row["module"]] = (src, binary)
        upstream_path = ROOT / "CONTINUACAO045_UPSTREAM.json"
        verify_pin(upstream_path, pins[45])
        upstream = json.loads(upstream_path.read_text(encoding="utf-8"))
        upstream_paths = [upstream_path]
        for item in upstream["files"]:
            current = verify_pin(Path(item["path"]), pins[45])
            if current["sha256"] != item["sha256"] or current["bytes"] != item["bytes"]:
                raise RuntimeError("Historical upstream045 record changed")
            upstream_paths.append(Path(item["path"]))
        order_file = ROOT / "TUNEL/PARA_CHATGPT/ORDEM_008_instancias_nomeadas_e_ambiente_limpo.md"
        custody_paths = [Path(__file__).resolve(), *previous_build_paths, *upstream_paths, order_file, ROOT / "TUNEL/PARA_CHATGPT/ORDEM_009_H3_dinamico_e_o_relogio_relativo.md", ROOT / "TUNEL/PARA_CHATGPT/ORDEM_010_horizontes_concretos_aperiodico_e_o_relogio_apos_a_obstrucao.md", *manifests.values(),
                         ROOT / "verify_stage.ps1", ROOT / "audit_continuation033.py",
                         ROOT / "audit_continuation034.py"]
        derivation_names = {'PolarizerModularCost': 'DERIVACAO054_GENERICO.md', 'PolarizerCostSeries': 'DERIVACAO054_SERIE.md', 'TowerModularCost': 'DERIVACAO054_TORRE.md', 'ModularCostDerivative': 'DERIVACAO054_DERIVADA.md'}
        required_derivations = ["CONTINUACAO054_DERIVACAO_PREVIA.md", "DERIVACAO054_INFRA.md"]
        required_derivations.extend(derivation_names[module] for module in MODULES)
        for name in required_derivations:
            if not (ROOT / name).is_file():
                raise RuntimeError(f"Missing prior derivation: {name}")
        custody_paths.extend(sorted(ROOT.glob("DERIVACAO054_*.md")))
        custody_paths.extend(sorted(ROOT.glob("NOTA054_*.md")))
        if not (ROOT / "CONTINUACAO054_DERIVACAO_PREVIA.md").is_file():
            raise RuntimeError("Missing prior derivation")
        for optional in [ROOT / "CONTINUACAO054_DERIVACAO_PREVIA.md",
                         KERNEL / "lean-toolchain", KERNEL / "lake-manifest.json",
                         KERNEL / "lakefile.toml", KERNEL / "lakefile.lean"]:
            if optional.is_file():
                custody_paths.append(optional)
        lean_exe = TOOLCHAIN / "bin/lean.exe"
        stdlib = TOOLCHAIN / "lib/lean"
        if not lean_exe.is_file() or not stdlib.is_dir():
            raise RuntimeError("Configured Lean 4.31.0 toolchain unavailable")
        package_root = KERNEL / ".lake/packages"
        package_dirs = sorted([p for p in package_root.iterdir() if p.is_dir()], key=lambda p: p.name)
        external_roots = [p / ".lake/build/lib/lean" for p in package_dirs
                          if (p / ".lake/build/lib/lean").is_dir()] + [stdlib]
        for package in package_dirs:
            for filename in ["lake-manifest.json", "lean-toolchain"]:
                if (package / filename).is_file():
                    custody_paths.append(package / filename)
        custody_paths.append(lean_exe)
        for name in ["Init", "Lean", "Std"]:
            path = stdlib / (name + ".olean")
            if path.is_file():
                custody_paths.extend(companions(path))
        custody_before = snapshot(custody_paths)
        sources = []
        infos = {}
        graph = {}
        for module in BUILD_ORDER:
            original = ROOT / (module + ".lean")
            raw = original.read_bytes()
            source_original = record(original)
            if hashlib.sha256(raw).hexdigest() != source_original["sha256"]:
                raise RuntimeError(f"Source changed while copying: {original}")
            if module in BASELINE:
                verify_pin(original, pins[33 if module in BASELINE[:3] else 34])
                copied, changes = name_baseline_instances(module, raw)
            else:
                copied, changes = raw, []
            source = clean / (module + ".lean")
            info = checked_source(copied.decode("utf-8"), module)
            if info["namespace"] != "ChatgptAudit.Cost054":
                raise RuntimeError("Unexpected new namespace")
            new_bytes(source, copied)
            row = {"module": module, "role": "baseline" if module in BASELINE else "batch",
                   "source": str(source), "original_source": str(original),
                   "proof_sha256": digest(source), "original_sha256": source_original["sha256"],
                   "source_equals_original": copied == raw, "transpositions": changes, **info}
            sources.append(row)
            infos[module] = row
            graph[module] = imports(copied.decode("utf-8"))
        if any(not row["source_equals_original"] for row in sources if row["role"] == "batch"):
            raise RuntimeError("A 054 source copy differs from the current source")
        source_map = {row["module"]: row for row in sources}
        boundary_modules = {}
        external = {}
        visiting = set()

        def resolve_external(module):
            candidates = [base / module_relative(module, ".olean") for base in external_roots]
            available = [path for path in candidates if path.is_file()]
            if not available:
                raise RuntimeError(f"Unresolved external import: {module}")
            resolved = available[0].resolve()
            if module in BUILD_ORDER or module == INTEGRATION or module.startswith(("TGL.", "TGLExt.")):
                raise RuntimeError(f"External fallback forbidden: {module}")
            external[module] = {
                "module": module, "resolved": str(resolved),
                "files": [record(path) for path in companions(resolved)],
                "other_candidates": [str(p.resolve()) for p in available[1:]],
                "transitive_external_closure_rebuilt": False,
            }

        def visit(module):
            if module in source_map:
                if module in visiting:
                    raise RuntimeError(f"Import cycle: {module}")
                visiting.add(module)
                for dep in graph[module]:
                    visit(dep)
                visiting.remove(module)
                return
            if module in boundary_modules or module in external:
                return
            if module.startswith(("TGL.", "TGLExt.")):
                original_source = ROOT / "fontes/tgl_kernel" / module_relative(module, ".lean")
                original_olean = ROOT / module_relative(module, ".olean")
            else:
                original_source = ROOT / module_relative(module, ".lean")
                original_olean = ROOT / module_relative(module, ".olean")
            if module in overrides:
                original_source, original_olean = overrides[module]
            if not original_source.is_file():
                resolve_external(module)
                return
            if module in visiting:
                raise RuntimeError(f"Boundary import cycle: {module}")
            canonical_source = module.startswith(("TGL.", "TGLExt."))
            source_has_pin034 = os.path.normcase(str(original_source.resolve())) in boundary_pins
            if source_has_pin034 or not canonical_source:
                original_source_row = verify_pin(original_source, boundary_pins)
                source_status = "PIN029_053_EXACT_BYTES"
            else:
                original_source_row = record(original_source)
                source_status = "REAL_CURRENT_READ_NO_HISTORICAL_SOURCE_PIN"
            verify_pin(original_olean, boundary_pins)
            deps = imports(original_source.read_text(encoding="utf-8-sig"))
            if any(dep in source_map for dep in deps):
                raise RuntimeError(f"Pre054 boundary imports a rebuilt module: {module}")
            copied_source = boundary_sources / module_relative(module, ".lean")
            new_bytes(copied_source, original_source.read_bytes())
            if digest(copied_source) != original_source_row["sha256"]:
                raise RuntimeError(f"Boundary source changed during copy: {module}")
            copied_files = []
            for old in companions(original_olean):
                suffix = str(old)[len(str(original_olean)):]
                relative = module_relative(module, ".olean")
                new = Path(str(boundary_dir / relative) + suffix)
                old_row = verify_pin(old, boundary_pins)
                new_bytes(new, old.read_bytes())
                if digest(new) != old_row["sha256"]:
                    raise RuntimeError(f"Boundary binary changed during copy: {module}")
                copied_files.append({"original": old_row, "copy": record(new),
                                     "pinned_in_manifest029_053": True, "primary_olean": old == original_olean})
            boundary_modules[module] = {
                "module": module, "original_source": original_source_row,
                "source_copy": record(copied_source), "imports": deps, "files": copied_files,
                "source_status": source_status, "source_has_historical_pin": source_has_pin034,
                "source_to_olean_provenance": "NOT_ESTABLISHED_OR_REBUILT_BY_THIS_RUN",
            }
            graph[module] = deps
            visiting.add(module)
            for dep in deps:
                visit(dep)
            visiting.remove(module)

        for module in BUILD_ORDER:
            visit(module)
        position = {name: i for i, name in enumerate(BUILD_ORDER)}
        for module in BUILD_ORDER:
            for dep in graph[module]:
                if dep in position and position[dep] >= position[module]:
                    raise RuntimeError(f"Explicit build order is not topological: {module} imports {dep}")
        integration_path = clean / (INTEGRATION + ".lean")
        new_bytes(integration_path, ("\n".join("import " + m for m in BUILD_ORDER) + "\n").encode("utf-8"))
        graph[INTEGRATION] = list(BUILD_ORDER)
        infos[INTEGRATION] = {"source": str(integration_path), "expected_axiom_rows": [],
                             "namespace": None, "anonymous_instances": 0}
        lean_path = [clean, boundary_dir, *external_roots]
        if ROOT.resolve() in [p.resolve() for p in lean_path] or KERNEL / ".lake/build/lib/lean" in lean_path:
            raise RuntimeError("Unrestricted local/canonical kernel fallback refused")
        env = os.environ.copy()
        env["LEAN_PATH"] = os.pathsep.join(str(p) for p in lean_path)
        env.pop("LEAN_SRC_PATH", None)
        env.pop("LEAN_SYSROOT", None)
        build_plan = {
            "schema": "chatgpt.clean054.plan.v1", "created_utc": now(),
            "clean_directory": str(clean), "modules": MODULES, "baseline_modules": BASELINE,
            "build_order": BUILD_ORDER, "integration_module": INTEGRATION,
            "sources": sources, "import_graph": graph, "lean_path": [str(p) for p in lean_path],
            "boundary_modules": list(boundary_modules.values()),
            "external_direct_inputs": list(external.values()), "custody_before": custody_before,
            "external_limit": (
                 "Boundary oleans and local bench sources are pinned to manifests029/032/033/034/035/036/037/040/041/043/045/046/047/052/053, not rebuilt. "
                "Individual TGL/TGLExt sources lacking historical source pins are copied and hashed now only "
                "for import discovery; this run does not establish source-to-olean provenance. "
                "Stage035/036/037/040/041/043 sources and binaries are selected from their verified clean directories, never root fallback. Only direct imports crossing this closure into Mathlib/packages/stdlib are hashed here; "
                "their external transitive binary closure is neither rebuilt nor exhaustively hashed. "
                "Lean/toolchain and package configuration remain read-only external dependencies."
            ),
            "historical_cause": "DECLARADO in order008; this run makes no causal claim about prior failures.",
        }
        new_json(clean / "BUILD_PLAN.json", build_plan)
        compiled = {}
        frozen_paths = set(custody_paths) | {integration_path}
        for row in sources:
            frozen_paths.update([Path(row["source"]), Path(row["original_source"])])
        for row in boundary_modules.values():
            frozen_paths.update([Path(row["original_source"]["path"]), Path(row["source_copy"]["path"])])
            for item in row["files"]:
                frozen_paths.update([Path(item["original"]["path"]), Path(item["copy"]["path"])])
        for row in external.values():
            frozen_paths.update(Path(item["path"]) for item in row["files"])
        frozen_reference = snapshot(frozen_paths)
        frozen_hashes = {row["path"]: row for row in frozen_reference}
        for row in custody_before:
            if frozen_hashes[row["path"]] != row:
                raise RuntimeError(f"Custody input changed during setup: {row['path']}")
        for row in sources:
            if frozen_hashes[str(Path(row["source"]).resolve())]["sha256"] != row["proof_sha256"]:
                raise RuntimeError(f"Clean source changed during setup: {row['module']}")
            if frozen_hashes[str(Path(row["original_source"]).resolve())]["sha256"] != row["original_sha256"]:
                raise RuntimeError(f"Original source changed during setup: {row['module']}")
        new_json(clean / "FROZEN_INPUTS.json", frozen_reference)

        def resolved_closure(module):
            seen = set()
            resolved = []
            paths = {Path(infos[module]["source"]), lean_exe}
            def walk(dep):
                if dep in seen:
                    return
                seen.add(dep)
                if dep in source_map:
                    if dep not in compiled:
                        raise RuntimeError(f"Missing clean predecessor; fallback prohibited: {module} -> {dep}")
                    binary = clean / (dep + ".olean")
                    if not binary.is_file():
                        raise RuntimeError(f"Missing clean binary: {dep}")
                    candidates = [base / module_relative(dep, ".olean") for base in lean_path]
                    first = next((p for p in candidates if p.is_file()), None)
                    if first is None or first.resolve() != binary.resolve():
                        raise RuntimeError(f"Clean module import shadowed: {dep}")
                    if snapshot(companions(binary)) != compiled[dep]["output_artifacts"]:
                        raise RuntimeError(f"Already compiled binary changed: {dep}")
                    paths.update(companions(binary))
                    paths.add(Path(source_map[dep]["source"]))
                    resolved.append({"module": dep, "kind": "rebuilt", "resolved": str(binary)})
                    for child in graph[dep]:
                        walk(child)
                elif dep in boundary_modules:
                    row = boundary_modules[dep]
                    binary = boundary_dir / module_relative(dep, ".olean")
                    candidates = [base / module_relative(dep, ".olean") for base in lean_path]
                    first = next((p for p in candidates if p.is_file()), None)
                    if first is None or first.resolve() != binary.resolve():
                        raise RuntimeError(f"Pinned boundary import shadowed: {dep}")
                    for item in row["files"]:
                        paths.update([Path(item["original"]["path"]), Path(item["copy"]["path"])])
                    paths.update([Path(row["original_source"]["path"]), Path(row["source_copy"]["path"])])
                    resolved.append({"module": dep, "kind": "pinned_pre054", "resolved": str(binary)})
                    for child in graph[dep]:
                        walk(child)
                else:
                    row = external[dep]
                    paths.update(Path(item["path"]) for item in row["files"])
                    resolved.append({"module": dep, "kind": "external_direct", "resolved": row["resolved"]})
            for dep in graph[module]:
                walk(dep)
            paths.update(custody_paths)
            paths.update(Path(row["original_source"]) for row in sources)
            return resolved, paths

        for index, module in enumerate(BUILD_ORDER + [INTEGRATION], 1):
            source = Path(infos[module]["source"])
            olean = clean / (module + ".olean")
            if any(p.exists() for p in companions(olean)):
                raise RuntimeError(f"Compilation output is not fresh: {module}")
            resolutions, input_paths = resolved_closure(module)
            before = snapshot(input_paths)
            for row in before:
                frozen = frozen_hashes.get(row["path"])
                if frozen is not None and row != frozen:
                    raise RuntimeError(f"Frozen input changed before compilation: {row['path']}")
            metadata = clean / f"{index:02d}_{module}.json"
            log = clean / f"{index:02d}_{module}.log"
            command = [str(lean_exe), "-o", str(olean), str(source)]
            started = now()
            print(json.dumps({"event": "compile_start", "module": module, "index": index,
                              "total": len(BUILD_ORDER) + 1, "clean_directory": str(clean)}), flush=True)
            completed = subprocess.run(command, cwd=clean, env=env, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, check=False)
            output_raw = completed.stdout
            new_bytes(log, output_raw, allow_empty=True)
            after = snapshot(input_paths)
            output = completed.stdout.decode("utf-8", errors="replace")
            axiom_rows = parse_axioms(output)
            errors = [line for line in output.splitlines()
                      if re.search(r"\b(?:error|warning)(?:\([^\n]*?\))?:", line)]
            bad_axioms = [row for row in axiom_rows if not set(row["axioms"]) <= ALLOWED_AXIOMS]
            coverage_ok = [row["declaration"] for row in axiom_rows] == infos[module]["expected_axiom_rows"]
            source_before = next(row for row in before if row["path"] == str(source.resolve()))
            source_after = next(row for row in after if row["path"] == str(source.resolve()))
            passed = completed.returncode == 0 and not errors and not bad_axioms and coverage_ok \
                and before == after and olean.is_file() and "sorryAx" not in output
            data = {
                "module": module, "timestamp": now(), "started_utc": started,
                "exit_code": completed.returncode, "proof_sha256": source_after["sha256"],
                "source_stable": source_before == source_after, "log": str(log),
                "source": str(source), "olean": str(olean), "metadata": str(metadata),
                "clean_directory": str(clean), "inputs_stable": before == after,
                "fresh_clean_build": True, "passed": passed, "command": command,
                "cwd": str(clean), "lean_path": [str(p) for p in lean_path],
                "inputs_before": before, "inputs_after": after, "import_resolutions": resolutions,
                "log_sha256": digest(log), "olean_sha256": digest(olean) if olean.is_file() else None,
                "output_artifacts": snapshot(companions(olean)) if olean.is_file() else [],
                "axiom_rows": axiom_rows, "expected_axiom_rows": infos[module]["expected_axiom_rows"],
                "axiom_coverage_exact": coverage_ok, "issues": errors,
                "anonymous_instances": infos[module]["anonymous_instances"],
                "role": "integration" if module == INTEGRATION else source_map[module]["role"],
            }
            new_json(metadata, data)
            steps.append({"module": module, "metadata": str(metadata)})
            print(json.dumps({"event": "compile_end", "module": module,
                              "exit_code": completed.returncode, "passed": passed}), flush=True)
            if not passed:
                raise RuntimeError(f"Clean compilation rejected: {module}; see {metadata}")
            compiled[module] = data
        for module, data in compiled.items():
            if snapshot(companions(Path(data["olean"]))) != data["output_artifacts"]:
                raise RuntimeError(f"Clean output changed before final marker: {module}")
        frozen_after = snapshot(frozen_paths)
        new_json(clean / "FROZEN_INPUTS_AFTER.json", frozen_after)
        if frozen_reference != frozen_after:
            raise RuntimeError("Inputs changed over the full clean build")
        files = snapshot([p for p in clean.rglob("*") if p.is_file()] + list(frozen_paths))
        result = {
            "schema": "chatgpt.clean054.build.v1", "status": "PASS", "created_utc": now(),
            "clean_directory": str(clean), "modules": MODULES, "baseline_modules": BASELINE,
            "build_order": BUILD_ORDER, "integration_module": INTEGRATION, "steps": steps,
            "sources": sources, "fresh_clean_build": True, "anonymous_instances_remaining": 0, "development_only": DEVELOPMENT,
            "source054_copies_exact": True, "inputs_stable": True,
            "lean_path": [str(p) for p in lean_path], "toolchain": record(lean_exe),
            "boundary": {
                "kind": "pinned_pre054_not_recompiled",
                "manifests": [record(p) for p in manifests.values()], "directory": str(boundary_dir),
                "modules": list(boundary_modules.values()),
                "external_direct_inputs": list(external.values()),
                "limitation": build_plan["external_limit"],
            },
            "import_graph": graph, "historical_cause": build_plan["historical_cause"], "files": files,
            "canonical_gate_changed": False, "H3": "OPEN", "physical_reconstruction": "OPEN",
        }
        new_json(MARKER, result)
        print(json.dumps({"status": "PASS", "marker": str(MARKER), "clean_directory": str(clean),
                          "steps": len(steps)}), flush=True)
    except BaseException as error:
        failure = {"schema": "chatgpt.clean054.failure.v1", "status": "FAILED",
                   "created_utc": now(), "clean_directory": str(clean), "steps": steps,
                   "error": repr(error), "traceback": traceback.format_exc(),
                   "preserved_files": [str(p) for p in sorted(clean.rglob("*")) if p.is_file()],
                   "success_marker_created": MARKER.exists()}
        new_json(clean / "FAILURE.json", failure)
        raise


if __name__ == "__main__":
    run_build()
