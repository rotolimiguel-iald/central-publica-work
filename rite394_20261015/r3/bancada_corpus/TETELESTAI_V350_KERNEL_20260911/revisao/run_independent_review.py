"""Read-only review of implementation; all outputs stay beside this script."""
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
assert REVIEW.name == "revisao"
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
RUN = REVIEW / ("independent_" + STAMP)
RUN.mkdir()

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def write(path, raw):
    assert path.resolve().is_relative_to(REVIEW)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = path.read_bytes()
        backup = path.with_name(path.name + ".bak_" + STAMP)
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(raw)
    assert temporary.stat().st_size == len(raw) and temporary.read_bytes() == raw
    temporary.replace(path)

def save_json(path, data):
    write(path, json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

environment = json.loads((ROOT / "environment.json").read_bytes())
modules = [
    "TGLExt/V350CompressionLimit.lean", "TGLExt/V350TowerCommutation.lean",
    "TGLExt/V350TowerDuality.lean", "TGLExt/V350ModularCertificate.lean",
    "TGLExt/V350GateContract.lean", "TGLExt/V350WedgeModularData.lean",
    "TGLV350/L2OperatorLift.lean", "TGLV350/L2Translation.lean",
    "TGLV350/L2StrongContinuity.lean", "TGLV350/RegularTowerRepresentation.lean",
    "TGLV350/RegularGeneratedAlgebra.lean",
]
module_names = {p[:-5].replace("/", ".") for p in modules}
snapshots = {}
for relative in modules + ["../gate_extension.py", "../integrate_v350.py",
                            "../compile_lean.py", "../compile_integrated.py",
                            "../test_gate_extension.py", "../integration.json",
                            "TGLExt.lean", "TGL/Audit.lean"]:
    source = (ROOT / "kernel" / relative).resolve()
    raw = source.read_bytes()
    dest = RUN / ("sources/" + relative if not relative.startswith("../")
                  else "integration/" + relative[3:])
    write(dest, raw)
    snapshots[str(source.relative_to(ROOT))] = {"sha256": digest(raw), "bytes": len(raw),
                                               "snapshot": str(dest)}

# Pin the project import closure and identify the actual cached binary selected by LEAN_PATH.
# Mathlib/Lean remain the installed compiler/library trust base; they are not rebuilt here.
dependencies = {}
seen = set()
def walk(name):
    if name in seen:
        return
    seen.add(name)
    source = ROOT / "kernel" / Path(*name.split(".")).with_suffix(".lean")
    if not source.is_file():
        return
    raw = source.read_bytes()
    if name not in module_names:
        binary = next((Path(p) / Path(*name.split(".")).with_suffix(".olean")
                       for p in environment["lean_path"]
                       if (Path(p) / Path(*name.split(".")).with_suffix(".olean")).is_file()), None)
        if binary is None:
            raise RuntimeError("Missing project dependency " + name)
        depsnapshot = RUN / "dependency_sources" / source.relative_to(ROOT / "kernel")
        write(depsnapshot, raw)
        dependencies[name] = {"source": str(source), "source_sha256": digest(raw),
                              "binary": str(binary), "binary_sha256": digest(binary.read_bytes())}
    for imported in re.findall(r"^import\s+([\w.]+)", raw.decode("utf-8"), re.M):
        walk(imported)

for module in module_names:
    walk(module)

# Lean resolves a namespace at its first search root. Freeze its complete project
# import closure there, so selected new modules cannot fall back to stale binaries.
for name, row in dependencies.items():
    binary = Path(row["binary"])
    destination = RUN / "build" / Path(*name.split(".")).with_suffix(".olean")
    write(destination, binary.read_bytes())
    assert digest(destination.read_bytes()) == row["binary_sha256"]
    row["frozen_binary"] = str(destination)
    for companion in binary.parent.glob(binary.name + ".*"):
        if companion.is_file():
            write(destination.with_name(companion.name), companion.read_bytes())

env = os.environ.copy()
env["LEAN_PATH"] = os.pathsep.join([str(RUN / "build")] + environment["lean_path"])
env["TMP"] = env["TEMP"] = str(RUN / "tmp")
(RUN / "tmp").mkdir()
version = subprocess.run([environment["lean"], "--version"], capture_output=True, cwd=RUN, env=env)
manifest = {"timestamp": STAMP, "run": str(RUN), "mode": "INDEPENDENT_RECOMPILATION_OF_FROZEN_SOURCES_WITH_CACHED_BASE_DEPENDENCIES",
            "lean_version": version.stdout.decode("utf-8").strip(),
            "compiler_sha256": digest(Path(environment["lean"]).read_bytes()),
            "lean_path": env["LEAN_PATH"], "snapshots": snapshots, "dependencies": dependencies,
            "modules": modules}
save_json(RUN / "manifest.json", manifest)
write(REVIEW / "latest_run.txt", str(RUN).encode("utf-8"))
print(json.dumps({"run": str(RUN), "modules": len(modules), "cached_project_dependencies": len(dependencies)}), flush=True)
records = []
for relative in modules:
    source = RUN / "sources" / relative
    output = RUN / "build" / Path(relative).with_suffix(".olean")
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [environment["lean"], "-o", str(output), str(source)]
    start = time.monotonic()
    result = subprocess.run(command, cwd=RUN / "sources", env=env, capture_output=True)
    stdout = result.stdout.decode("utf-8", errors="replace")
    axioms = {}
    for name, body in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", stdout, re.S):
        axioms[name] = [a.strip() for a in body.split(",") if a.strip()]
    for name in re.findall(r"'([\w.']+)' does not depend on any axioms", stdout):
        axioms[name] = []
    log = RUN / "logs" / Path(relative).stem
    write(log.with_suffix(".stdout.txt"), result.stdout)
    write(log.with_suffix(".stderr.txt"), result.stderr)
    record = {"module": relative, "command": command, "returncode": result.returncode,
              "seconds": round(time.monotonic() - start, 3), "source_sha256": digest(source.read_bytes()),
              "output_sha256": digest(output.read_bytes()) if output.is_file() else None,
              "stdout": str(log.with_suffix(".stdout.txt")), "stderr": str(log.with_suffix(".stderr.txt")),
              "axioms": axioms, "axioms_allowed": bool(axioms) and all(
                  set(a) <= {"propext", "Classical.choice", "Quot.sound"} for a in axioms.values())}
    records.append(record)
    save_json(RUN / "compilation.json", {"records": records, "complete": False})
    print(json.dumps({k: record[k] for k in ["module", "returncode", "seconds", "axioms_allowed"]}), flush=True)
    if result.returncode:
        print(stdout[:12000], flush=True)
        break

changed = []
for name, row in dependencies.items():
    if digest(Path(row["source"]).read_bytes()) != row["source_sha256"] or digest(Path(row["binary"]).read_bytes()) != row["binary_sha256"]:
        changed.append(name)
source_changes = [name for name, row in snapshots.items() if digest((ROOT / name).read_bytes()) != row["sha256"]]
report = {"records": records, "complete": len(records) == len(modules),
          "all_exit_zero": len(records) == len(modules) and all(r["returncode"] == 0 for r in records),
          "dependencies_changed": changed, "implementation_files_changed_during_review": source_changes}
save_json(RUN / "compilation.json", report)
print(json.dumps({k: v for k, v in report.items() if k != "records"}), flush=True)
