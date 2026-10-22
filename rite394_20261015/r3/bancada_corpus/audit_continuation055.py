"""Strict read-only audit; --build-only checks the build; --seal creates a new055 seal."""
from pathlib import Path
import ast, hashlib, json, re, sys, os
from datetime import datetime, timezone
import clean_continuation035 as common

ROOT = Path(__file__).resolve().parent
MODULES = ['ExchangeEntropyResponse', 'ExchangeMicroscopicDynamics', 'ExchangeModularCost']
MANIFEST = ROOT / "CONTINUACAO055_MANIFESTO.json"
BUILD = ROOT / "CONTINUACAO055_CLEAN_BUILD.json"
DELIVERY = ROOT / "TUNEL/DO_CHATGPT/ENTREGA_055_troca_conservada_e_entropia_regional.md"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

SCIENTIFIC_SCOPE = 'Conserved two-site exchange dynamics and actual regional state restrictions in the same product-state tower, regional entropy and modular-energy response, and comparison with the independently constructed polarizer cost054; scope limited to compiled declarations'
SCIENTIFIC_LIMITATIONS = ['The exchange interaction, unit local energy gap, and evolution parameter are explicit microscopic inputs, not a derivation of a physical interaction or dimensional scale.', 'Regional energy transfer and its conserved current are not identified with constructedHeat or a stress-energy flux through a gravitational screen.', 'Regional Bernoulli entropy and relative entropy refer to proved restrictions of the actual unitary orbit. They are not the full entropy of the two-site state or a global Araki relative entropy.', 'The local modular response must be linked to the same finite-prefix K and polarizer cost054. The quadratic Taylor coefficient is half the second derivative; modular-energy weights are distinct from unweighted conserved energy.', 'All faithful weights, including equal weights and tracial marginals, retain the hypotheses of the compiled statements. Positive physical temperature is not inferred over the entire faithful domain.', 'Historical pinned binaries and recorded source-metadata-binary crosslinks, including continuation054, are checked and copied, not rebuilt in this batch.', 'External direct imports and companions crossing the local closure are hashed; their transitive closure is not exhaustively rebuilt or hashed.', "H3, microscopic heat-to-screen matching, area matching, physical localization, energy/time/temperature and area scales, and general gravitational reconstruction remain open; canonical_gate_changed=false describes this batch's writes."]

NAMESPACE = "ChatgptAudit.Exchange055"
RUNNER = ROOT / "clean_continuation055.py"
REVIEW = ROOT / "CONTINUACAO055_REVISAO_INDEPENDENTE.md"
REPORT = ROOT / "CONTINUACAO055_PARECER.md"
AREA_NOTE = ROOT / "CONTINUACAO055_DERIVACAO_PREVIA.md"
ORDER010 = ROOT / "TUNEL/PARA_CHATGPT/ORDEM_010_horizontes_concretos_aperiodico_e_o_relogio_apos_a_obstrucao.md"
DERIVATIONS = [ROOT / name for name in ['CONTINUACAO055_DERIVACAO_PREVIA.md', 'DERIVACAO055_INFRA.md', 'DERIVACAO055_ENTROPIA.md', 'DERIVACAO055_DINAMICA.md', 'DERIVACAO055_CUSTO.md']]

MODULE_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*")
INSTANCE_RE = re.compile(r"(?m)^[ \t]*(?:(?:local|scoped|noncomputable|unsafe)\s+)*instance\b")
AXIOM_RE = re.compile(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")


def check(condition, message):
    if not condition:
        raise RuntimeError(message)

def unique_object(pairs):
    result = {}
    for name, value in pairs:
        check(name not in result, "Duplicate JSON key: " + name)
        result[name] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)


def path_key(path):
    """Normalize Windows junctions and case before comparing provenance paths."""
    return os.path.normcase(str(Path(path).resolve()))


def verify_record(row):
    actual = common.record(row["path"])
    check(actual["sha256"] == row["sha256"] and actual["bytes"] == row["bytes"],
          "Hash or size mismatch: " + row["path"])

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
    check(module in MODULES, "Unexpected source module: " + module)
    namespace = NAMESPACE
    check(namespaces == [namespace], "Unexpected namespace: " + module)
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
    expected = [n if n.startswith(namespace + ".") else namespace + "." + n for n in printed]
    instance_names = {r["name"] for r in rows}
    return {"namespace": namespace, "expected_axiom_rows": expected,
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


def source_census(path):
    text = Path(path).read_bytes().decode("utf-8-sig")
    info = source_info(text, Path(path).stem)
    code = mask_lean(text)
    return {"theorems": info["theorems"], "definitions_including_structures": info["definitions"],
            "structures": len(re.findall(r"(?m)^[ \t]*(?:noncomputable\s+)?structure\s+", code)),
            "instances": len(info["instances"]), "anonymous_instances": 0,
            "axiom_prints": info["axiom_prints"], "printed": info["expected_axiom_rows"],
            "instance_axiom_rows": info["instance_axiom_rows"], "instance_rows": info["instances"]}


def runner_contract():
    tree = ast.parse(RUNNER.read_text(encoding="utf-8-sig"))
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in {"ALL_MODULES", "BASELINE", "INTEGRATION"}:
                    values[target.id] = ast.literal_eval(node.value)
    check(values == {"ALL_MODULES": MODULES, "BASELINE": [], "INTEGRATION": "Imports055All"},
          "Runner batch contract differs from independent auditor")


# Only these successful, sealed clean batches may override older root artifacts.
# The baseline of 035 has deliberate instance-name insertions, not source equality.
HISTORICAL_BATCHES = {35: (['CentralizerDensity',
       'LikelihoodDensityLog',
       'DensityStateUniqueness',
       'CentralizerPhaseOrbit',
       'SitePhaseCovariance',
       'AngularScreenMetric',
       'AngularAreaObservability'],
      ['UnitaryStateDerivative',
       'SitePauliObservables',
       'PauliOperationalSurface',
       'PauliProbabilityModel',
       'PauliMeasurementFisher']),
 36: ([],
      ['OpticalTidalScreen', 'OpticalScreenInvariant', 'OpticalJacobiArea', 'OpticalAreaFreedom']),
 37: ([],
      ['QuarticClockTransport',
       'BinaryRelativeQuartic',
       'SummableRelativeQuartic',
       'JacobiAreaQuarticLimit',
       'FourthOrderMatchingControls',
       'QuarticMatchingClockControls']),
 40: ([],
      ['RelativeEntropyClock',
       'StateClockObstruction',
       'IntrinsicFisherClock',
       'AffineClockAndRegion',
       'StateClockMatchingControls']),
 41: ([], ['OpticalHeatFlow', 'OpticalHeatClausius']),
 43: ([],
      ['JacobiRiccatiProfile',
       'OpticalNullCongruence',
       'OpticalEquilibriumScreen',
       'OpticalConstructedHeat']),
 45: ([],
      ['TGLExt.TheLiftFiresOnThePeriodicTower',
       'TGLExt.TheModularFlowIsAHorizon',
       'StateClockDichotomy',
       'HorizonAreaScale',
       'FiniteSitePermutations',
       'FiniteSiteHorizons']),
 46: ([],
      ['AperiodicPhaseAverage',
       'BoundedOmegaLimit',
       'AperiodicVectorAverage',
       'AperiodicAveragePrefix',
       'AperiodicCentralizerExpectation',
       'AperiodicTowerLift']),
 47: ([],
      ['ExpectationAlgebra',
       'GeneralExpectationPositive',
       'OperatorBlockRepresentation',
       'ExpectationBlockPositive',
       'GeneralExpectationCP',
       'ExpectationContinuity',
       'MonotoneOperatorLimit',
       'ExpectationNormality']),
 53: ([],
      ['HorizonGNSImplementation',
       'SymplecticPolarizer',
       'TowerStatePolarizer',
       'LocalPolarizerWitness',
       'CovariantAreaCounterexample'])}

HISTORICAL_BATCHES[52] = ([], ['LocalHorizontalPauli', 'ModularHorizontalRotation', 'HorizontalAreaSelection', 'QuantumOrbitArea'])
HISTORICAL_BATCHES[54] = ([], ['PolarizerModularCost', 'PolarizerCostSeries', 'TowerModularCost', 'ModularCostDerivative'])

HISTORICAL_045_NAMESPACES = {'TGLExt.TheLiftFiresOnThePeriodicTower': 'TGLExt',
 'TGLExt.TheModularFlowIsAHorizon': 'TGLExt',
 'StateClockDichotomy': 'ChatgptAudit.Clock045',
 'HorizonAreaScale': 'ChatgptAudit.Area045',
 'FiniteSitePermutations': 'ChatgptAudit.Horizons045',
 'FiniteSiteHorizons': 'ChatgptAudit.Horizons045'}


def inspect_historical_build(stage, pins, require_covered):
    """Recheck pinned artifacts and their recorded compilation crosslinks, without rebuilding.

    Only artifacts actually used by 055 must occur in its frozen input snapshot.
    Other historical evidence is pinned and included in the final audit manifest;
    it is not retroactively described as an input captured by the 055 runner.
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
        source, original = clean / common.module_relative(module, ".lean"), ROOT / common.module_relative(module, ".lean")
        binary = clean / common.module_relative(module, ".olean")
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
        elif stage == 45:
            expected_namespace = HISTORICAL_045_NAMESPACES[module]
        elif stage == 46:
            expected_namespace = "ChatgptAudit.Aperiodic046"
        elif stage == 47:
            expected_namespace = "ChatgptAudit.Expectation047"
        elif stage == 52:
            expected_namespace = "ChatgptAudit.Orbit052"
        elif stage == 53:
            expected_namespace = "ChatgptAudit.Covariant053"
        elif stage == 54:
            expected_namespace = "ChatgptAudit.Cost054"
        else:
            expected_namespace = {36: "ChatgptAudit.Optical036", 37: "ChatgptAudit.Quartic037", 40: "ChatgptAudit.Clock040", 41: "ChatgptAudit.Heat041", 43: "ChatgptAudit.Optical043"}[stage]
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
        if stage in {47, 52, 53, 54}:
            # Replay the recorded census, including separately counted named instances.
            instance_rows = common.instances(raw.decode("utf-8-sig"))
            declarations = re.findall(r"(?m)^[ \t]*(?:noncomputable\s+)?(theorem|lemma|def|abbrev|structure)\s+([\w.']+)", code)
            expected_names = [expected_namespace + "." + name for _, name in declarations]
            instance_names = [expected_namespace + "." + item["name"] for item in instance_rows]
            check(row["instances"] == instance_rows and row["instance_axiom_rows"] == instance_names,
                  "Historical named-instance census crosslink: " + module)
            check(len(qualified) == len(expected_names) + len(instance_names) and
                  set(qualified) == set(expected_names + instance_names) and row["axiom_prints"] == len(qualified),
                  "Historical declaration/print census: " + module)
            check(row["theorems"] == sum(kind in {"theorem", "lemma"} for kind, _ in declarations) and
                  row["definitions"] == sum(kind not in {"theorem", "lemma"} for kind, _ in declarations),
                  "Historical theorem/definition census: " + module)
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
        source, binary, log = clean / common.module_relative(name, ".lean"), clean / common.module_relative(name, ".olean"), clean / f"{index:02d}_{name}.log"
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


def inspect_upstream045(require_covered, pins):
    manifest_path = ROOT / "CONTINUACAO045_UPSTREAM.json"
    common.verify_pin(manifest_path, pins)
    require_covered(manifest_path)
    data = read_json(manifest_path)
    check(data["schema"] == "chatgpt.upstream045.v1", "Wrong upstream schema")
    names = ["TheLiftFiresOnThePeriodicTower", "TheModularFlowIsAHorizon"]
    check([item["module"] for item in data["items"]] == ["TGLExt." + n for n in names],
          "Wrong upstream module set or order")
    mapping = [("TGLExt.PeriodicCentralizerExpectation", "PeriodicCentralizerExpectation"),
               ("TGLExt.TracialCentralizerExpectation", "TracialCentralizerExpectation"),
               ("TGLExt.ModularPower", "ModularPower")]
    expected_records = [common.record(ROOT / "prepare_continuation045.py")]
    for name, item in zip(names, data["items"]):
        origin = common.KERNEL / "TGLExt" / (name + ".lean")
        snapshot = ROOT / "CONTINUACAO045_UPSTREAM" / "TGLExt" / (name + ".lean")
        adapted = ROOT / "TGLExt" / (name + ".lean")
        for key, path in [("origin", origin), ("snapshot", snapshot), ("adapted", adapted)]:
            check(path_key(item[key]["path"]) == path_key(path), "Unexpected upstream path")
            require_covered(path)
            verify_record(item[key])
            check(item[key] == common.record(path), "Upstream record crosslink")
            expected_records.append(item[key])
        raw = origin.read_bytes()
        check(raw == snapshot.read_bytes(), "Snapshot is not exact original bytes")
        text = raw.decode("utf-8-sig")
        changes = []
        for before, after in mapping:
            old_import = "import " + before
            if re.search(r"(?m)^" + re.escape(old_import) + r"\s*$", text):
                text = re.sub(r"(?m)^" + re.escape(old_import) + r"(?=\s*$)", "import " + after, text)
                changes.append({"from": before, "to": after})
        code = common.mask_lean(text)
        declarations = re.findall(r"(?m)^(?:theorem|lemma|def|abbrev|structure)\s+([\w.]+)", code)
        printed = re.findall(r"(?m)^#print\s+axioms\s+([\w.]+)", code)
        missing = [declaration for declaration in declarations if declaration not in printed]
        closing = re.search(r"(?m)^end\s*\r?\nend TGLExt\s*$", text)
        check(closing is not None, "Missing upstream closing namespace")
        text = text[:closing.start()] + "\n".join("#print axioms " + n for n in missing) + "\n" + text[closing.start():]
        check(adapted.read_bytes() == text.encode("utf-8"), "Upstream transposition differs from deterministic replay")
        check(item["import_transpositions"] == changes and item["added_axiom_prints"] == missing
              and item["proof_body_unchanged"] is True, "Upstream transformation metadata mismatch")
    check(data["files"] == expected_records, "Upstream file inventory mismatch")
    for row in expected_records:
        common.verify_pin(row["path"], pins)
        require_covered(row["path"])
        verify_record(row)
    return [row["path"] for row in expected_records]


def inspect_build():
    runner_contract()
    data = read_json(BUILD)
    check(data["schema"] == "chatgpt.clean055.build.v1", "Unexpected build schema")
    check(data["status"] == "PASS" and data["fresh_clean_build"] is True, "No successful clean build")
    check(data.get("development_only") is False, "Development attempt cannot seal")
    check(data["modules"] == MODULES and data["build_order"] == MODULES, "Unexpected build batch")
    check(data["baseline_modules"] == [], "Unexpected rebuilt baseline")
    check(data["source055_copies_exact"] is True, "Missing exact-copy assertion")
    check(data["anonymous_instances_remaining"] == 0 and data["inputs_stable"] is True, "Dirty inputs")
    clean = Path(data["clean_directory"]).resolve(strict=True)
    check(clean.parent == ROOT and clean.name.startswith("CONTINUACAO055_CLEAN_"), "Wrong clean directory")
    check(data["integration_module"] == "Imports055All", "Missing integration module")
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

    for filename in ["BUILD_PLAN.json", "FROZEN_INPUTS.json", "FROZEN_INPUTS_AFTER.json", "Imports055All.lean"]:
        require_covered(clean / filename)
    plan = read_json(clean / "BUILD_PLAN.json")
    check(plan["schema"] == "chatgpt.clean055.plan.v1", "Unexpected plan schema")
    check(plan["build_order"] == MODULES and path_key(plan["clean_directory"]) == path_key(clean), "Plan mismatch")
    check(plan["modules"] == MODULES and plan["baseline_modules"] == [] and
          plan["integration_module"] == "Imports055All", "Plan batch mismatch")
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
    check(boundary["kind"] == "pinned_pre055_not_recompiled", "Wrong boundary kind")
    check(path_key(boundary["directory"]) == path_key(clean / "boundary"), "Wrong boundary directory")
    check(plan["boundary_modules"] == boundary["modules"] and
          plan["external_direct_inputs"] == boundary["external_direct_inputs"], "Boundary plan mismatch")
    check(boundary["limitation"] == plan["external_limit"], "Boundary limitation mismatch")
    expected_manifests = [ROOT / ("CONTINUACAO%03d_MANIFESTO.json" % i) for i in [29, 32, 33, 34, 35, 36, 37, 40, 41, 43, 45, 46, 47, 52, 53, 54]]
    check([path_key(row["path"]) for row in boundary["manifests"]] ==
          [path_key(p) for p in expected_manifests], "Wrong historical manifests")
    historical, pin_tables = {}, {}
    for row, stage in zip(boundary["manifests"], [29, 32, 33, 34, 35, 36, 37, 40, 41, 43, 45, 46, 47, 52, 53, 54]):
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
    upstream_paths = inspect_upstream045(require_covered, pin_tables[45])
    overrides, override_pins, historical_evidence = {}, {}, {ROOT / "CONTINUACAO045_UPSTREAM.json", *map(Path, upstream_paths)}
    for stage in [35, 36, 37, 40, 41, 43, 45, 46, 47, 52, 53, 54]:
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
            check(row["source_status"] == "PIN029_054_EXACT_BYTES", "Historical source status")
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
        check(not set(real_imports) & set(MODULES), "Historical boundary imports a rebuilt055 module")
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
            check(item["pinned_in_manifest029_054"] is True, "Boundary binary pin flag missing")
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
              "instances": 0, "anonymous_instances": 0, "axiom_prints": 0}
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
        check(row["namespace"] == "ChatgptAudit.Exchange055" and row["role"] == "batch", "Source role mismatch")
        check(imports(copied.read_text(encoding="utf-8-sig")) == graph[module], "Batch import graph mismatch")
        census[module] = source_census(original)
        check(census[module]["printed"] == row["expected_axiom_rows"], "Print census mismatch")
        check(census[module]["theorems"] == row["theorems"] and
              census[module]["definitions_including_structures"] == row["definitions"] and
              row["instances"] == census[module]["instance_rows"] and
              row["instance_axiom_rows"] == census[module]["instance_axiom_rows"] and
              row["axiom_prints"] == census[module]["axiom_prints"] and
              row["anonymous_instances"] == 0, "Source census crosslink mismatch")
        for key in totals:
            totals[key] += census[module][key]
    custody_keys = {path_key(row["path"]) for row in plan["custody_before"]}
    check(bool(custody_keys) and len(custody_keys) == len(plan["custody_before"]),
          "Missing or duplicate custody snapshot")
    check(all(path_key(p) in custody_keys for p in upstream_paths), "Upstream not frozen before compilation")
    mandatory_custody = [ROOT / "CONTINUACAO045_UPSTREAM.json", RUNNER, common.TOOLCHAIN / "bin/lean.exe", ORDER010, AREA_NOTE, *DERIVATIONS,
                         ROOT / "TUNEL/PARA_CHATGPT/ORDEM_008_instancias_nomeadas_e_ambiente_limpo.md",
                         ROOT / "verify_stage.ps1", ROOT / "audit_continuation033.py", ROOT / "audit_continuation034.py",
                         ROOT / "TUNEL/PARA_CHATGPT/ORDEM_009_H3_dinamico_e_o_relogio_relativo.md",
                         *expected_manifests,
                         *[ROOT / f"CONTINUACAO{stage:03d}_CLEAN_BUILD.json" for stage in [35, 36, 37, 40, 41, 43, 45, 46, 47, 52, 53, 54]]]
    check(all(path_key(p) in custody_keys for p in mandatory_custody), "Runner custody evidence incomplete")
    expected_frozen_keys = set(custody_keys) | {path_key(clean / "Imports055All.lean")}
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
    expected_order = MODULES + ["Imports055All"]
    check([row["module"] for row in data["steps"]] == expected_order, "Wrong serial build order")
    integration = clean / "Imports055All.lean"
    check(integration.read_text(encoding="utf-8") ==
          "".join("import " + m + "\n" for m in MODULES), "Import-all content mismatch")
    check(graph["Imports055All"] == MODULES, "Integration graph mismatch")
    check(set(graph) == set(MODULES) | set(boundary_map) | {"Imports055All"}, "Unexpected local graph node")
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
                check(row["kind"] == "pinned_pre055" and
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
        rows = log_rows(raw_log.encode("utf-8"))
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

def documentary_paths():
    paths = {BUILD, Path(__file__).resolve(), RUNNER, REVIEW, REPORT, DELIVERY, AREA_NOTE, ORDER010, *DERIVATIONS}
    paths.update(ROOT / (name + ".lean") for name in MODULES)
    paths.update(ROOT.glob("DERIVACAO055_*.md"))
    paths.update(ROOT.glob("NOTA055_*.md"))
    paths.update(ROOT.glob("CONTINUACAO055_REVISAO_*.md"))
    for name in ["revise_continuation055.py", "finalize_reports055.py", "probe_continuation055.py"]:
        if (ROOT / name).is_file(): paths.add(ROOT / name)
    return paths


def prior_attempt_paths():
    """Preserve available development evidence; it never becomes a proved input."""
    paths = set()
    for pattern in ["CONTINUACAO055_CLEAN_*", "CONTINUACAO055_DEVELOPMENT_*", "DEV055_*"]:
        for path in ROOT.glob(pattern):
            if path.is_file() and path.suffix == ".json": paths.add(path)
            elif path.is_dir():
                paths.update(p for p in path.rglob("*") if p.is_file() and p.suffix in {".lean", ".json", ".log"})
    for pattern in ["*055*.bak_*"] + [name + ".lean.bak_*" for name in MODULES]:
        paths.update(p for p in ROOT.glob(pattern) if p.is_file())
    return paths


def main():
    mode = sys.argv[1:]
    check(mode in [[], ["--build-only"], ["--seal"]], "Only --build-only or --seal accepted")
    if mode == ["--seal"]: check(not MANIFEST.exists(), "Continuation055 is already sealed")
    if mode == []: check(MANIFEST.is_file(), "Default verification requires the seal")
    build, totals = inspect_build()
    counts = {"theorems": totals["theorems"], "definitions": totals["definitions_including_structures"],
              "axiom_prints": totals["axiom_prints"], "instances": totals["instances"]}
    check(counts["axiom_prints"] == counts["theorems"] + counts["definitions"] + counts["instances"],
          "Declaration census total differs from axiom coverage")
    if mode == ["--build-only"]:
        print(json.dumps({"status": "BUILD_PASS", "sealed": False, "counts": counts,
              "build_files": len(build["files"]), "historical_records": len(build["audit_historical_evidence"]),
              "steps": len(build["steps"]), "modules": MODULES, "canonical_gate_changed": False}))
        return
    mandatory = documentary_paths()
    for path in mandatory: check(path.is_file(), "Missing documentary evidence: " + str(path))
    review = REVIEW.read_text(encoding="utf-8-sig")
    check("BUILD_PASS" in review, "Independent review lacks build result")
    check("Build SHA256: " + common.digest(BUILD) in review, "Independent review belongs to another build digest")
    check("Diretório final: " + Path(build["clean_directory"]).as_posix() in review,
          "Independent review belongs to another final directory")
    if mode == ["--seal"]:
        paths = {Path(row["path"]) for row in build["files"] + build["audit_historical_evidence"]}
        paths.update(mandatory)
        paths.update(prior_attempt_paths())
        result = {"schema": "chatgpt.continuation055.v1", "created_utc": datetime.now(timezone.utc).isoformat(),
                  "status": "PASS", "scope": SCIENTIFIC_SCOPE,
                  "H3": "OPEN", "physical_reconstruction": "OPEN", "broad_quantum_gravity_goal": "OPEN",
                  "canonical_gate_changed": False, "counts": counts, "modules": MODULES,
                  "clean_directory": build["clean_directory"], "fresh_clean_build": True,
                  "clean_build": common.record(BUILD), "files": common.snapshot(paths),
                  "limitations": SCIENTIFIC_LIMITATIONS}
        new_json(MANIFEST, result)
    manifest = read_json(MANIFEST)
    check(manifest["schema"] == "chatgpt.continuation055.v1" and manifest["status"] == "PASS", "Invalid seal")
    check(manifest["scope"] == SCIENTIFIC_SCOPE and manifest["limitations"] == SCIENTIFIC_LIMITATIONS,
          "Scientific scope or limitations differ from the audited batch")
    check(manifest["H3"] == manifest["physical_reconstruction"] == manifest["broad_quantum_gravity_goal"] == "OPEN"
          and manifest["canonical_gate_changed"] is False, "Scientific status mismatch")
    check(manifest["counts"] == counts and manifest["modules"] == MODULES, "Sealed counts mismatch")
    check(manifest["clean_build"] == common.record(BUILD) and manifest["fresh_clean_build"] is True
          and path_key(manifest["clean_directory"]) == path_key(build["clean_directory"]), "Sealed build mismatch")
    records = manifest["files"]
    check(len(records) == len({path_key(row["path"]) for row in records}), "Duplicate seal record")
    for row in records: verify_record(row)
    recorded = {path_key(row["path"]): row for row in records}
    required_paths = {path_key(row["path"]) for row in build["files"] + build["audit_historical_evidence"]}
    required_paths.update(path_key(path) for path in mandatory)
    check(required_paths <= set(recorded), "Sealed evidence coverage incomplete")
    print(json.dumps({"status": "PASS", "sealed": True, "read_only": mode != ["--seal"],
          "counts": counts, "files": len(records), "steps": len(build["steps"]),
          "H3": "OPEN", "physical_reconstruction": "OPEN", "broad_quantum_gravity_goal": "OPEN",
          "canonical_gate_changed": False}))


if __name__ == "__main__":
    main()
