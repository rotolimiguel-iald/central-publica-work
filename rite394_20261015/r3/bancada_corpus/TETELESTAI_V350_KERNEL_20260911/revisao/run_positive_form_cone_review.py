"""Freeze and independently compile the positive form cone and its printed declarations plus the order instance."""
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
PREVIOUS = Path((REVIEW / "dual_fixed_form_affiliation_latest_run.txt").read_text(encoding="utf-8"))
RUN = REVIEW / ("positive_form_cone_independent_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
NAMES = ["PositiveFormCone"]
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write(path, raw):
    assert path.resolve().is_relative_to(REVIEW)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        before = path.read_bytes()
        if before == raw:
            return
        backup = path.with_name(path.name + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temp = path.with_name(path.name + ".tmp")
    temp.write_bytes(raw)
    assert temp.stat().st_size == len(raw) and temp.read_bytes() == raw
    temp.replace(path)

def save(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8"))

environment = json.loads((ROOT / "environment.json").read_bytes())
prior = json.loads((PREVIOUS / "manifest.json").read_bytes())
prior_build = json.loads((PREVIOUS / "compilation.json").read_bytes())
assert prior_build["all_exit_zero"]
dependencies = {}
for name, row in prior["dependencies"].items():
    dependencies[name] = {"binary": row["frozen_binary"], "sha256": row["sha256"],
                          "source": row["frozen_source"], "source_sha256": row["source_sha256"]}
for relative, row in prior["sources"].items():
    record = next(r for r in prior_build["records"] if r["module"] == relative)
    assert record["returncode"] == 0
    dependencies[relative[:-5].replace("/", ".")] = {
        "binary": str(PREVIOUS / "build" / Path(relative).with_suffix(".olean")),
        "sha256": record["output_sha256"], "source": row["snapshot"], "source_sha256": row["sha256"]}
for name, row in dependencies.items():
    binary, source = Path(row["binary"]), Path(row["source"])
    raw = binary.read_bytes()
    source_raw = source.read_bytes()
    assert sha(raw) == row["sha256"] and sha(source_raw) == row["source_sha256"]
    rel = Path(*name.split("."))
    live = ROOT / "kernel" / rel.with_suffix(".lean")
    assert sha(live.read_bytes()) == row["source_sha256"], str(live)
    target = RUN / "build" / rel.with_suffix(".olean")
    write(target, raw)
    frozen_source = RUN / "dependency_sources" / rel.with_suffix(".lean")
    write(frozen_source, source_raw)
    row["frozen_binary"] = str(target)
    row["frozen_source"] = str(frozen_source)
    for companion in binary.parent.glob(binary.name + ".*"):
        if companion.is_file():
            write(target.with_name(companion.name), companion.read_bytes())

sources = {}
declarations = []
generated = []
for name in NAMES:
    relative = "TGLV350/" + name + ".lean"
    source = ROOT / "kernel" / relative
    snapshot = RUN / "sources" / relative
    write(snapshot, source.read_bytes())
    raw = snapshot.read_bytes()
    assert source.read_bytes() == raw
    text = raw.decode("utf-8")
    candidate_logs = []
    for p in sorted((ROOT / "logs").glob(name + "_*.json"), reverse=True):
        data = json.loads(p.read_bytes())
        if data.get("sha256") == sha(raw) and data.get("returncode") == 0 and data.get("source_unchanged_during_compile"):
            candidate_logs.append((p, data))
    assert candidate_logs, name + " has no matching successful author log"
    log_path, author = candidate_logs[0]
    binary = ROOT / "build" / Path(relative).with_suffix(".olean")
    assert sha(binary.read_bytes()) == author["output_sha256"]
    for item in [log_path, Path(author["stdout"]), Path(author["stderr"])]:
        write(RUN / "author_logs" / item.name, item.read_bytes())
    namespace = "TGLV350.Regular"
    local_declarations = []
    for line in text.splitlines():
        if line.strip() == "namespace ClosedPositiveForm":
            namespace = "TGLV350.Regular.ClosedPositiveForm"
        elif line.strip() == "end ClosedPositiveForm":
            namespace = "TGLV350.Regular"
        line = re.sub(r"^@\[[^]]+\]\s*", "", line)
        match = re.match(r"^(?:noncomputable\s+)?(?:def|theorem|abbrev|structure|instance)\s+([\w.]+)", line)
        if match:
            local_declarations.append(namespace + "." + match.group(1))
    declarations.extend(local_declarations)
    imports = re.findall(r"^import\s+([\w.]+)", text, re.M)
    assert all(n.startswith("Mathlib.") or n in dependencies or n in {"TGLV350." + x for x in NAMES} for n in imports)
    sources[relative] = {"path": str(source), "snapshot": str(snapshot), "sha256": sha(raw),
                         "lines": len(text.splitlines()), "imports": imports, "declarations": local_declarations,
                         "author_log": str(log_path), "author_binary_sha256": author["output_sha256"]}
generated = ["ReviewPositiveFormCone.orderInstance"]

(RUN / "tmp").mkdir(parents=True)
env = os.environ.copy()
env["LEAN_PATH"] = os.pathsep.join([str(RUN / "build")] + environment["lean_path"][2:])
env["TMP"] = env["TEMP"] = str(RUN / "tmp")
version = subprocess.run([environment["lean"], "--version"], env=env, cwd=RUN, capture_output=True)
manifest = {"run": str(RUN), "previous_run": str(PREVIOUS),
    "mode": "INDEPENDENT_RECOMPILATION_POSITIVE_FORM_CONE_WITH_ORDER_INSTANCE_WITH_FROZEN_PROJECT_DEPENDENCIES",
    "sources": sources, "dependencies": dependencies, "declarations": declarations,
    "generated_declarations": generated, "prior_declarations_in_full_audit": [], "lean_path": env["LEAN_PATH"],
    "lean_version": version.stdout.decode("utf-8").strip(), "compiler_sha256": sha(Path(environment["lean"]).read_bytes()),
    "previous_reviews": {str(p): sha(p.read_bytes()) for p in REVIEW.glob("REVIEW_*.md")},
    "initial_um_sha256": sha((ROOT / "um.py").read_bytes())}
for name in ["integration.json", "gate_extension.py"]:
    write(RUN / "initial_integration" / name, (ROOT / name).read_bytes())
write(RUN / "research_note/DUAL_WEIGHT_CONSTRUCTION.md", (REVIEW / "DUAL_WEIGHT_CONSTRUCTION.md").read_bytes())
save(RUN / "manifest.json", manifest)
write(REVIEW / "positive_form_cone_latest_run.txt", str(RUN).encode("utf-8"))

audit = "\n".join("import TGLV350." + n for n in NAMES) + "\n"
audit += "noncomputable def ReviewPositiveFormCone.orderInstance {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] (N : VonNeumannAlgebra H) : PartialOrder (TGLV350.Regular.AffiliatedPositiveForm N) := inferInstance\n"
for name in declarations + generated:
    audit += "set_option pp.universes true in\n#check " + name + "\n#print axioms " + name + "\n"
write(RUN / "sources/PositiveFormConeFullAudit.lean", audit.encode("utf-8"))
print(json.dumps({"run": str(RUN), "frozen_dependencies": len(dependencies),
                  "authored_declarations": len(declarations), "generated_declarations": len(generated)}), flush=True)
records = []
for relative in list(sources) + ["PositiveFormConeFullAudit.lean"]:
    source = RUN / "sources" / relative
    output = RUN / "build" / Path(relative).with_suffix(".olean")
    output.parent.mkdir(parents=True, exist_ok=True)
    assert not output.exists()
    command = [environment["lean"], "-o", str(output), str(source)]
    start = time.monotonic()
    result = subprocess.run(command, env=env, cwd=RUN / "sources", capture_output=True)
    stdout = result.stdout.decode("utf-8", errors="replace")
    axioms = {n: [re.sub(r"\.\{[^}]*\}$", "", x.strip()) for x in body.split(",") if x.strip()]
              for n, body in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", stdout, re.S)}
    for name in re.findall(r"'([\w.']+)' does not depend on any axioms", stdout):
        axioms[name] = []
    outlog = RUN / "logs" / (Path(relative).stem + ".stdout.txt")
    errlog = RUN / "logs" / (Path(relative).stem + ".stderr.txt")
    write(outlog, result.stdout)
    write(errlog, result.stderr)
    record = {"module": relative, "command": command, "returncode": result.returncode,
        "seconds": round(time.monotonic() - start, 3), "source_sha256": sha(source.read_bytes()),
        "output_sha256": sha(output.read_bytes()) if output.exists() else None,
        "axioms": axioms, "axioms_allowed": bool(axioms) and all(set(x) <= ALLOWED for x in axioms.values()),
        "stdout": str(outlog), "stderr": str(errlog)}
    records.append(record)
    save(RUN / "compilation.json", {"records": records, "complete": False})
    print(json.dumps({k: record[k] for k in ["module", "returncode", "seconds", "axioms_allowed"]}), flush=True)
    if result.returncode:
        print(stdout, flush=True)
        break
report = {"records": records, "complete": len(records) == 2,
    "all_exit_zero": len(records) == 2 and all(r["returncode"] == 0 for r in records),
    "full_audit_names_exact": len(records) == 2 and set(records[-1]["axioms"]) == set(declarations + generated),
    "all_axioms_allowed": all(r["axioms_allowed"] for r in records),
    "sources_unchanged": all(sha(Path(r["path"]).read_bytes()) == r["sha256"] for r in sources.values()),
    "dependencies_unchanged": all(sha(Path(r["frozen_binary"]).read_bytes()) == r["sha256"] and sha(Path(r["frozen_source"]).read_bytes()) == r["source_sha256"] for r in dependencies.values()),
    "previous_reviews_preserved": all(sha(Path(p).read_bytes()) == h for p, h in manifest["previous_reviews"].items())}
save(RUN / "compilation.json", report)
print(json.dumps({k: v for k, v in report.items() if k != "records"}), flush=True)
