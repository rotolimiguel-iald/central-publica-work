"""Separate addendum after the fourth module was explicitly declared stable."""
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
RUN = Path((REVIEW / "dual_weight_latest_run.txt").read_text(encoding="utf-8"))
BASE = json.loads((RUN / "manifest.json").read_bytes())
BUILD = json.loads((RUN / "compilation.json").read_bytes())
assert BUILD["all_exit_zero"] and BUILD["full_audit_names_exact"] and BUILD["all_axioms_allowed"]
ENVIRONMENT = json.loads((ROOT / "environment.json").read_bytes())
ADDENDUM = RUN / ("exhaustion_addendum_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write(path, raw):
    assert path.resolve().is_relative_to(REVIEW)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        before = path.read_bytes()
        backup = path.with_name(path.name + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temp = path.with_name(path.name + ".tmp")
    temp.write_bytes(raw)
    assert temp.read_bytes() == raw and temp.stat().st_size == len(raw)
    temp.replace(path)

def save(path, data):
    write(path, json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

relative = "TGLV350/DualWeightExhaustion.lean"
source = ROOT / "kernel" / relative
raw = source.read_bytes()
snapshot = ADDENDUM / "sources" / relative
write(snapshot, raw)
log_path = ROOT / "logs/DualWeightExhaustion_20260911_223746_013821.json"
author = json.loads(log_path.read_bytes())
assert author["returncode"] == 0 and author["source_unchanged_during_compile"] and author["sha256"] == sha(raw)
assert sha((ROOT / "build/TGLV350/DualWeightExhaustion.olean").read_bytes()) == author["output_sha256"]
for path in [log_path, Path(author["stdout"]), Path(author["stderr"])]:
    write(ADDENDUM / "author_logs" / path.name, path.read_bytes())
declarations = ["TGLV350.Regular." + n for n in re.findall(r"^theorem\s+(\w+)", raw.decode("utf-8"), re.M)]
assert len(declarations) == 3
manifest = {"source": str(source), "snapshot": str(snapshot), "source_sha256": sha(raw),
    "source_lines": len(raw.decode("utf-8").splitlines()), "declarations": declarations,
    "mode": "SEPARATE_INDEPENDENT_RECOMPILATION_AFTER_STABILITY_NOTICE",
    "base_run": str(RUN), "base_manifest_sha256": sha((RUN / "manifest.json").read_bytes()),
    "base_compilation_sha256": sha((RUN / "compilation.json").read_bytes()),
    "author_log": str(log_path), "author_binary_sha256": author["output_sha256"],
    "lean_path": BASE["lean_path"]}
save(ADDENDUM / "manifest.json", manifest)
audit = "import TGLV350.DualWeightExhaustion\n"
for name in declarations:
    audit += "set_option pp.universes true in\n#check " + name + "\n#print axioms " + name + "\n"
audit += '''
set_option autoImplicit false
open MeasureTheory TGLV350.Regular TGLV350.StrongIntegral
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

-- Coercion of the restricted action gives the very same integrand, on the whole algebra.
example (P : TGLExt.SiteProfile) (A : (regularCoreAlgebra P).toStarSubalgebra)
    (R : ℝ) (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    dualWeightCut R A.val v = ∫ s in (-R)..R,
      ((regularDualAction P s A).val : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
        RegularHilbert (TGLExt.TowerHilbert P)) v := rfl

-- Fixed Haar factor, without division by the growing interval length.
example (R : ℝ) (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    normalizedDualCut R A = ((2 * Real.pi)⁻¹ : ℝ) • dualWeightCut R A := rfl

-- The integral in operatorIntegral_apply has Hilbert vectors as values.
example (F : Family (H := H)) (a b : ℝ) (v : H) :
    operatorIntegral F a b v = (∫ t in a..b, F.op t v : H) := rfl
end
'''
write(ADDENDUM / "sources/ExhaustionFullAudit.lean", audit.encode("utf-8"))
env = os.environ.copy()
env["LEAN_PATH"] = BASE["lean_path"]
env["TMP"] = env["TEMP"] = str(RUN / "tmp")
records = []
for rel in [relative, "ExhaustionFullAudit.lean"]:
    path = ADDENDUM / "sources" / rel
    output = RUN / "build" / Path(rel).with_suffix(".olean")
    assert not output.exists()
    command = [ENVIRONMENT["lean"], "-o", str(output), str(path)]
    start = time.monotonic()
    result = subprocess.run(command, env=env, cwd=ADDENDUM / "sources", capture_output=True)
    stdout = result.stdout.decode("utf-8", errors="replace")
    axioms = {n: [x.strip() for x in body.split(",") if x.strip()] for n, body in
              re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", stdout, re.S)}
    for name in re.findall(r"'([\w.']+)' does not depend on any axioms", stdout):
        axioms[name] = []
    outlog = ADDENDUM / "logs" / (Path(rel).stem + ".stdout.txt")
    errlog = ADDENDUM / "logs" / (Path(rel).stem + ".stderr.txt")
    write(outlog, result.stdout)
    write(errlog, result.stderr)
    row = {"module": rel, "command": command, "returncode": result.returncode,
        "seconds": round(time.monotonic() - start, 3), "source_sha256": sha(path.read_bytes()),
        "output_sha256": sha(output.read_bytes()) if output.exists() else None,
        "axioms": axioms, "axioms_allowed": bool(axioms) and all(set(v) <= {"propext", "Classical.choice", "Quot.sound"} for v in axioms.values()),
        "stdout": str(outlog), "stderr": str(errlog)}
    records.append(row)
    report = {"records": records, "all_exit_zero": len(records) == 2 and all(r["returncode"] == 0 for r in records),
        "audit_names_exact": set(axioms) == set(declarations),
        "source_unchanged": sha(source.read_bytes()) == manifest["source_sha256"],
        "base_manifest_preserved": sha((RUN / "manifest.json").read_bytes()) == manifest["base_manifest_sha256"],
        "base_compilation_preserved": sha((RUN / "compilation.json").read_bytes()) == manifest["base_compilation_sha256"],
        "additional_same_object_type_probes": 3}
    save(ADDENDUM / "compilation.json", report)
    print(json.dumps({k: row[k] for k in ["module", "returncode", "seconds", "axioms_allowed"]}), flush=True)
    if result.returncode:
        print(stdout, flush=True)
        break
