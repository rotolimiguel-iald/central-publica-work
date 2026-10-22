"""Independent dual/bounded review; all writes stay in revisao; um.py is never run."""
from pathlib import Path
import ast
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
PREVIOUS = Path((REVIEW / "latest_run.txt").read_text(encoding="utf-8"))
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
RUN = REVIEW / ("dual_independent_" + STAMP)
RUN.mkdir()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write(p, raw):
    assert p.resolve().is_relative_to(REVIEW)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = p.with_name(p.name + ".tmp")
    temp.write_bytes(raw)
    assert temp.stat().st_size == len(raw) and temp.read_bytes() == raw
    temp.replace(p)

def save(p, obj):
    write(p, json.dumps(obj, indent=2, ensure_ascii=False).encode("utf-8"))

environment = json.loads((ROOT / "environment.json").read_bytes())
prior_manifest = json.loads((PREVIOUS / "manifest.json").read_bytes())
prior_compile = json.loads((PREVIOUS / "compilation.json").read_bytes())
assert prior_compile["all_exit_zero"]
dependencies = {}
for name, row in prior_manifest["dependencies"].items():
    dependencies[name] = {"binary": row["frozen_binary"], "sha256": row["binary_sha256"],
                          "source": str(PREVIOUS / "dependency_sources" / Path(*name.split(".")).with_suffix(".lean")),
                          "source_sha256": row["source_sha256"]}
for row in prior_compile["records"]:
    name = row["module"][:-5].replace("/", ".")
    dependencies[name] = {"binary": str(PREVIOUS / "build" / Path(row["module"]).with_suffix(".olean")),
                          "sha256": row["output_sha256"], "source": str(PREVIOUS / "sources" / row["module"]),
                          "source_sha256": row["source_sha256"]}
for name, row in dependencies.items():
    binary, source = Path(row["binary"]), Path(row["source"])
    raw = binary.read_bytes()
    assert sha(raw) == row["sha256"] and sha(source.read_bytes()) == row["source_sha256"]
    target = RUN / "build" / Path(*name.split(".")).with_suffix(".olean")
    write(target, raw)
    row["frozen_binary"] = str(target)
    for companion in binary.parent.glob(binary.name + ".*"):
        if companion.is_file():
            write(target.with_name(companion.name), companion.read_bytes())

names = ["L2CharacterMultiplier", "GeneratedEquivariance", "RegularDualAction", "L2BoundedStrongContinuity"]
snapshots = {}
declarations = []
for name in names:
    p = ROOT / "kernel/TGLV350" / (name + ".lean")
    raw = p.read_bytes()
    target = RUN / "sources/TGLV350" / p.name
    write(target, raw)
    source = raw.decode("utf-8")
    for imported in re.findall(r"^import\s+([\w.]+)", source, re.M):
        assert imported in dependencies or imported in {"TGLV350." + n for n in names}, imported
    declarations += ["TGLV350.Regular." + d for d in re.findall(r"^(?:noncomputable\s+)?(?:def|theorem|abbrev)\s+(\w+)", source, re.M)]
    integrated = ROOT / "kernel/TGLExt" / ("V350" + p.name)
    integrated_raw = integrated.read_bytes()
    write(RUN / "integrated_sources/TGLExt" / integrated.name, integrated_raw)
    snapshots[name] = {"dev_path": str(p), "dev_sha256": sha(raw), "integrated_path": str(integrated),
                       "integrated_sha256": sha(integrated_raw),
                       "same_except_import_paths": integrated_raw.decode("utf-8") == source.replace("import TGLV350.", "import TGLExt.V350")}
    assert snapshots[name]["same_except_import_paths"]

# Freeze integration inputs as data. Never compile or exec any part of um.py.
um_raw = (ROOT / "um.py").read_bytes()
tree = ast.parse(um_raw)
embedded = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in n.targets)).value)
embedded_checks = {}
for name, row in snapshots.items():
    rel = "TGLExt/V350" + name + ".lean"
    embedded_checks[rel] = sha(embedded[rel].encode("utf-8")) == row["integrated_sha256"]
assert all(embedded_checks.values())
for name in ["gate_extension.py", "integration.json", "integrate_v350.py", "compile_lean.py", "compile_integrated.py", "test_gate_extension.py"]:
    write(RUN / "integration" / name, (ROOT / name).read_bytes())
for name in ["TGLExt.lean", "TGL/Audit.lean"]:
    write(RUN / "integration/kernel" / name, (ROOT / "kernel" / name).read_bytes())
previous_report = REVIEW / "REVIEW_MODULAR_AND_REGULAR.md"
previous_report_sha = sha(previous_report.read_bytes())

env = os.environ.copy()
env["LEAN_PATH"] = os.pathsep.join([str(RUN / "build")] + environment["lean_path"][2:])
env["TMP"] = env["TEMP"] = str(RUN / "tmp")
(RUN / "tmp").mkdir()
version = subprocess.run([environment["lean"], "--version"], env=env, cwd=RUN, capture_output=True)
manifest = {"timestamp": STAMP, "previous_run": str(PREVIOUS), "run": str(RUN),
            "mode": "INDEPENDENT_RECOMPILATION_FOUR_NEW_MODULES_WITH_PREVIOUSLY_FROZEN_DEPENDENCIES",
            "lean_version": version.stdout.decode("utf-8").strip(), "compiler_sha256": sha(Path(environment["lean"]).read_bytes()),
            "lean_path": env["LEAN_PATH"], "snapshots": snapshots, "dependencies": dependencies,
            "all_declarations": declarations, "um_sha256": sha(um_raw), "embedded_files": len(embedded),
            "embedded_checks": embedded_checks, "previous_report_sha256": previous_report_sha,
            "gate_extension_unchanged": (RUN / "integration/gate_extension.py").read_bytes() == (PREVIOUS / "integration/gate_extension.py").read_bytes()}
save(RUN / "manifest.json", manifest)
write(REVIEW / "dual_latest_run.txt", str(RUN).encode("utf-8"))

# Audit every new definition/theorem, including helpers not printed by standalone sources.
audit = "import TGLV350.RegularDualAction\nimport TGLV350.L2BoundedStrongContinuity\n"
audit += "\n".join("#check " + name + "\n#print axioms " + name for name in declarations) + "\n"
write(RUN / "sources/DualFullAudit.lean", audit.encode("utf-8"))
print(json.dumps({"run": str(RUN), "frozen_dependencies": len(dependencies), "new_declarations": len(declarations),
                  "um_sha256": manifest["um_sha256"], "embedded_files": len(embedded)}), flush=True)
records = []
for relative in ["TGLV350/" + n + ".lean" for n in names] + ["DualFullAudit.lean"]:
    source = RUN / "sources" / relative
    output = RUN / "build" / Path(relative).with_suffix(".olean")
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [environment["lean"], "-o", str(output), str(source)]
    started = time.monotonic()
    result = subprocess.run(command, cwd=RUN / "sources", env=env, capture_output=True)
    stdout = result.stdout.decode("utf-8", errors="replace")
    axioms = {name: [a.strip() for a in body.split(",") if a.strip()]
              for name, body in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", stdout, re.S)}
    for name in re.findall(r"'([\w.']+)' does not depend on any axioms", stdout):
        axioms[name] = []
    log = RUN / "logs" / Path(relative).stem
    write(log.with_suffix(".stdout.txt"), result.stdout)
    write(log.with_suffix(".stderr.txt"), result.stderr)
    row = {"module": relative, "command": command, "returncode": result.returncode,
           "seconds": round(time.monotonic()-started, 3), "source_sha256": sha(source.read_bytes()),
           "output_sha256": sha(output.read_bytes()) if output.is_file() else None,
           "axioms": axioms, "axioms_allowed": bool(axioms) and all(set(a) <= {"propext", "Classical.choice", "Quot.sound"} for a in axioms.values()),
           "stdout": str(log.with_suffix(".stdout.txt")), "stderr": str(log.with_suffix(".stderr.txt"))}
    records.append(row)
    save(RUN / "compilation.json", {"records": records, "complete": False})
    print(json.dumps({k:row[k] for k in ["module","returncode","seconds","axioms_allowed"]}), flush=True)
    if result.returncode:
        print(stdout, flush=True)
        break
report = {"records": records, "complete": len(records) == 5, "all_exit_zero": len(records) == 5 and all(r["returncode"] == 0 for r in records),
          "full_audit_all_expected_names": len(records) == 5 and set(records[-1]["axioms"]) == set(declarations),
          "frozen_dependency_changes": [n for n,r in dependencies.items() if sha(Path(r["frozen_binary"]).read_bytes()) != r["sha256"]],
          "source_changes": [n for n,r in snapshots.items() if sha(Path(r["dev_path"]).read_bytes()) != r["dev_sha256"] or sha(Path(r["integrated_path"]).read_bytes()) != r["integrated_sha256"]],
          "previous_report_preserved": sha(previous_report.read_bytes()) == previous_report_sha}
save(RUN / "compilation.json", report)
print(json.dumps({k:v for k,v in report.items() if k != "records"}), flush=True)
