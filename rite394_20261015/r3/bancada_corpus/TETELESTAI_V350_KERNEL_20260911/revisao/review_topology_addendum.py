from pathlib import Path
import ast
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "dual_latest_run.txt").read_text(encoding="utf-8"))
MANIFEST = json.loads((RUN / "manifest.json").read_bytes())
ENVIRONMENT = json.loads((ROOT / "environment.json").read_bytes())
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
ADDENDUM = RUN / ("topology_addendum_" + STAMP)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write(p, raw):
    assert p.resolve().is_relative_to(REVIEW)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        before = p.read_bytes()
        backup = p.with_name(p.name + ".bak_" + STAMP)
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temp = p.with_name(p.name + ".tmp")
    temp.write_bytes(raw)
    assert temp.read_bytes() == raw and temp.stat().st_size == len(raw)
    temp.replace(p)

dev = ROOT / "kernel/TGLV350/RegularTopology.lean"
integrated = ROOT / "kernel/TGLExt/V350RegularTopology.lean"
raw, integrated_raw = dev.read_bytes(), integrated.read_bytes()
assert integrated_raw.decode("utf-8") == raw.decode("utf-8").replace("import TGLV350.", "import TGLExt.V350")
write(ADDENDUM / "sources/TGLV350/RegularTopology.lean", raw)
write(ADDENDUM / "integrated_sources/TGLExt/V350RegularTopology.lean", integrated_raw)
names = ["TGLV350.Regular." + n for n in re.findall(r"^theorem\s+(\w+)", raw.decode("utf-8"), re.M)]
audit = "import TGLV350.RegularTopology\n"
audit += "#check Set.isClosed_centralizer\n#check ContinuousLinearMapWOT.toCLM\n"
audit += "\n".join("#check " + n + "\n#print axioms " + n for n in names) + "\n"
write(ADDENDUM / "sources/TopologyFullAudit.lean", audit.encode("utf-8"))
um_raw = (ROOT / "um.py").read_bytes()
tree = ast.parse(um_raw)
embedded = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign) and
    any(isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in n.targets)).value)
assert embedded["TGLExt/V350RegularTopology.lean"].encode("utf-8") == integrated_raw
write(ADDENDUM / "integration.json", (ROOT / "integration.json").read_bytes())
manifest = {"addendum": str(ADDENDUM), "dev_sha256": sha(raw), "integrated_sha256": sha(integrated_raw),
            "source_lines": len(raw.decode("utf-8").splitlines()), "same_except_import_paths": True,
            "embedded_matches": True, "um_sha256": sha(um_raw), "embedded_files": len(embedded),
            "declarations": names, "base_run": str(RUN), "lean_path": MANIFEST["lean_path"]}
write(ADDENDUM / "manifest.json", json.dumps(manifest, indent=2).encode("utf-8"))
env = os.environ.copy()
env["LEAN_PATH"] = MANIFEST["lean_path"]
env["TMP"] = env["TEMP"] = str(RUN / "tmp")
records = []
for rel in ["TGLV350/RegularTopology.lean", "TopologyFullAudit.lean"]:
    source = ADDENDUM / "sources" / rel
    output = RUN / "build" / Path(rel).with_suffix(".olean")
    command = [ENVIRONMENT["lean"], "-o", str(output), str(source)]
    result = subprocess.run(command, cwd=ADDENDUM / "sources", env=env, capture_output=True)
    stdout = result.stdout.decode("utf-8", errors="replace")
    axioms = {n:[x.strip() for x in b.split(",") if x.strip()] for n,b in
              re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", stdout, re.S)}
    for name in re.findall(r"'([\w.']+)' does not depend on any axioms", stdout):
        axioms[name] = []
    write(ADDENDUM / "logs" / (Path(rel).stem + ".stdout.txt"), result.stdout)
    write(ADDENDUM / "logs" / (Path(rel).stem + ".stderr.txt"), result.stderr)
    row = {"module": rel, "command": command, "returncode": result.returncode,
           "source_sha256": sha(source.read_bytes()), "output_sha256": sha(output.read_bytes()) if output.exists() else None,
           "axioms": axioms, "axioms_allowed": bool(axioms) and all(set(x)<={"propext","Classical.choice","Quot.sound"} for x in axioms.values())}
    records.append(row)
    write(ADDENDUM / "compilation.json", json.dumps({"records": records}, indent=2).encode("utf-8"))
    print(json.dumps({k:v for k,v in row.items() if k not in ["command","axioms"]}), flush=True)
    if result.returncode:
        print(stdout, flush=True)
        break
