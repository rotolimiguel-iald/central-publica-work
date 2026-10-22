"""Independent normality review: writes only below revisao; never imports um.py."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
ENVIRONMENT = json.loads((ROOT / "environment.json").read_bytes())
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}

def stamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write(path, raw):
    assert path.resolve().is_relative_to(REVIEW)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = path.read_bytes()
        backup = path.with_name(path.name + ".bak_" + stamp())
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = path.with_name(path.name + ".tmp_" + stamp())
    temp.write_bytes(raw)
    assert temp.stat().st_size == len(raw) and temp.read_bytes() == raw
    temp.replace(path)

def save(path, value):
    write(path, json.dumps(value, indent=2, ensure_ascii=False).encode("utf-8"))

def freeze_source(run, relative, author_log=None):
    path = ROOT / "kernel" / relative
    raw = path.read_bytes()
    snapshot = run / "sources" / relative
    write(snapshot, raw)
    row = {"path": str(path), "snapshot": str(snapshot), "sha256": sha(raw),
           "lines": len(raw.decode("utf-8").splitlines())}
    if author_log:
        log_path = ROOT / "logs" / author_log
        log = json.loads(log_path.read_bytes())
        assert log["sha256"] == row["sha256"] and log["returncode"] == 0
        assert log["source_unchanged_during_compile"]
        binary = ROOT / "build" / Path(relative).with_suffix(".olean")
        assert sha(binary.read_bytes()) == log["output_sha256"]
        row["author_log"] = str(log_path)
        row["author_binary_sha256"] = log["output_sha256"]
        for item in [log_path, Path(log["stdout"]), Path(log["stderr"])]:
            write(run / "author_logs" / item.name, item.read_bytes())
    return row

def compile_one(run, manifest, relative):
    source = run / "sources" / relative
    output = run / "build" / Path(relative).with_suffix(".olean")
    output.parent.mkdir(parents=True, exist_ok=True)
    assert not output.exists(), "Independent compilation must not overwrite a binary"
    env = os.environ.copy()
    env["LEAN_PATH"] = manifest["lean_path"]
    env["TMP"] = env["TEMP"] = str(run / "tmp")
    command = [ENVIRONMENT["lean"], "-o", str(output), str(source)]
    started = time.monotonic()
    result = subprocess.run(command, cwd=run / "sources", env=env, capture_output=True)
    stdout = result.stdout.decode("utf-8", errors="replace")
    axioms = {n: [re.sub(r"\.\{[^}]*\}$", "", x.strip()) for x in body.split(",") if x.strip()] for n, body in
              re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", stdout, re.S)}
    for name in re.findall(r"'([\w.']+)' does not depend on any axioms", stdout):
        axioms[name] = []
    prefix = run / "logs" / Path(relative).stem
    write(prefix.with_suffix(".stdout.txt"), result.stdout)
    write(prefix.with_suffix(".stderr.txt"), result.stderr)
    row = {"module": relative, "command": command, "returncode": result.returncode,
           "seconds": round(time.monotonic() - started, 3), "source_sha256": sha(source.read_bytes()),
           "output_sha256": sha(output.read_bytes()) if output.exists() else None,
           "axioms": axioms, "axioms_allowed": bool(axioms) and all(set(x) <= ALLOWED for x in axioms.values()),
           "stdout": str(prefix.with_suffix(".stdout.txt")), "stderr": str(prefix.with_suffix(".stderr.txt"))}
    report_path = run / "compilation.json"
    report = json.loads(report_path.read_bytes()) if report_path.exists() else {"records": []}
    report["records"].append(row)
    report["all_exit_zero"] = all(r["returncode"] == 0 for r in report["records"])
    report["sources_unchanged"] = all(sha(Path(r["path"]).read_bytes()) == r["sha256"] for r in manifest["sources"].values())
    report["dependencies_unchanged"] = all(sha(Path(r["frozen_binary"]).read_bytes()) == r["sha256"] for r in manifest["dependencies"].values())
    report["previous_reviews_preserved"] = all(sha(Path(p).read_bytes()) == h for p, h in manifest["previous_reviews"].items())
    save(report_path, report)
    print(json.dumps({k: row[k] for k in ["module", "returncode", "seconds", "axioms_allowed"]}), flush=True)
    if result.returncode:
        print(stdout, flush=True)
        raise SystemExit(result.returncode)
    return row

def audit(run, manifest, name):
    lines = []
    declarations = []
    for rel, row in manifest["sources"].items():
        source = Path(row["snapshot"]).read_text(encoding="utf-8")
        namespace = "ChatgptAudit.Expectation047" if "MonotoneOperatorLimit" in rel else (
            "TGLV350.ContractAudit" if "CoreContractCounterexample" in rel else "TGLV350.Regular")
        lines.append("import " + rel[:-5].replace("/", "."))
        declarations.extend(namespace + "." + n for n in re.findall(
            r"^(?:noncomputable\s+)?(?:def|theorem|abbrev)\s+(\w+)", source, re.M))
    lines += ["set_option pp.universes true"]
    for declaration in declarations:
        lines += ["#check " + declaration, "#print axioms " + declaration]
    write(run / "sources" / (name + ".lean"), ("\n".join(lines) + "\n").encode("utf-8"))
    record = compile_one(run, manifest, name + ".lean")
    save(run / (name + ".json"), {"expected_declarations": declarations, "expected_count": len(declarations),
         "audit_names_exact": set(record["axioms"]) == set(declarations),
         "all_allowed": record["axioms_allowed"], "record": record})

if sys.argv[1] == "init":
    previous = Path((REVIEW / "dual_latest_run.txt").read_text(encoding="utf-8"))
    prior = json.loads((previous / "manifest.json").read_bytes())
    run = REVIEW / ("normality_independent_" + stamp())
    run.mkdir()
    (run / "tmp").mkdir()
    dependencies = {}
    for name, row in prior["dependencies"].items():
        dependencies[name] = {"binary": row["frozen_binary"], "sha256": row["sha256"],
                              "source": row["source"], "source_sha256": row["source_sha256"]}
    prior_compile = json.loads((previous / "compilation.json").read_bytes())
    assert prior_compile["all_exit_zero"]
    topology = sorted(previous.glob("topology_addendum_*"))[-1]
    for base, records in [(previous, prior_compile["records"]),
                          (topology, json.loads((topology / "compilation.json").read_bytes())["records"])]:
        for row in records:
            if not row["module"].startswith("TGLV350/"):
                continue
            assert row["returncode"] == 0
            name = row["module"][:-5].replace("/", ".")
            dependencies[name] = {"binary": str(previous / "build" / Path(row["module"]).with_suffix(".olean")),
                                  "sha256": row["output_sha256"], "source": str(base / "sources" / row["module"]),
                                  "source_sha256": row["source_sha256"]}
    for name, row in dependencies.items():
        binary, source = Path(row["binary"]), Path(row["source"])
        assert sha(binary.read_bytes()) == row["sha256"]
        assert sha(source.read_bytes()) == row["source_sha256"]
        live_source = ROOT / "kernel" / Path(*name.split(".")).with_suffix(".lean")
        assert sha(live_source.read_bytes()) == row["source_sha256"], str(live_source)
        target = run / "build" / Path(*name.split(".")).with_suffix(".olean")
        write(target, binary.read_bytes())
        row["frozen_binary"] = str(target)
        frozen_source = run / "dependency_sources" / Path(*name.split(".")).with_suffix(".lean")
        write(frozen_source, source.read_bytes())
        row["frozen_source"] = str(frozen_source)
        for companion in binary.parent.glob(binary.name + ".*"):
            if companion.is_file():
                write(target.with_name(companion.name), companion.read_bytes())
    sources = {}
    for rel, log in [("TGLExt/MonotoneOperatorLimit.lean", None),
                     ("TGLV350/L2Order.lean", "L2Order_20260911_215425_688208.json"),
                     ("TGLV350/CoreContractCounterexample.lean", "CoreContractCounterexample_20260911_215722_529319.json")]:
        sources[rel] = freeze_source(run, rel, log)
    version = subprocess.run([ENVIRONMENT["lean"], "--version"], capture_output=True)
    manifest = {"run": str(run), "previous_run": str(previous),
                "mode": "INDEPENDENT_RECOMPILATION_NEW_SOURCES_AND_MONOTONE_OPERATOR_LIMIT_WITH_FROZEN_PROJECT_DEPENDENCIES",
                "compiler_sha256": sha(Path(ENVIRONMENT["lean"]).read_bytes()),
                "lean_version": version.stdout.decode("utf-8").strip(),
                "lean_path": os.pathsep.join([str(run / "build")] + ENVIRONMENT["lean_path"][2:]),
                "sources": sources, "dependencies": dependencies,
                "previous_reviews": {str(REVIEW / n): sha((REVIEW / n).read_bytes()) for n in
                                     ["REVIEW_MODULAR_AND_REGULAR.md", "REVIEW_DUAL_AND_BOUNDED.md"]},
                "initial_um_sha256": sha((ROOT / "um.py").read_bytes())}
    save(run / "manifest.json", manifest)
    write(REVIEW / "normality_latest_run.txt", str(run).encode("utf-8"))
    print(json.dumps({"run": str(run), "frozen_dependencies": len(dependencies)}), flush=True)
    for rel in sources:
        compile_one(run, manifest, rel)
    audit(run, manifest, "NormalityInitialAudit")
elif sys.argv[1] == "add":
    run = Path((REVIEW / "normality_latest_run.txt").read_text(encoding="utf-8"))
    manifest = json.loads((run / "manifest.json").read_bytes())
    rel, log = sys.argv[2], sys.argv[3]
    assert rel not in manifest["sources"]
    manifest["sources"][rel] = freeze_source(run, rel, log)
    save(run / "manifest.json", manifest)
    compile_one(run, manifest, rel)
    audit(run, manifest, "NormalityFullAudit")
else:
    raise SystemExit("Usage: init | add TGLV350/RegularNormality.lean author_log.json")
