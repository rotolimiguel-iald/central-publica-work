"""Additional exact-type probes; compiled only under revisao."""
from pathlib import Path
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
RUN = Path((REVIEW / "latest_run.txt").read_text(encoding="utf-8"))
manifest = json.loads((RUN / "manifest.json").read_bytes())
environment = json.loads((ROOT / "environment.json").read_bytes())
stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")

def write(path, raw):
    assert path.resolve().is_relative_to(REVIEW)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path.with_name(path.name + ".bak_" + stamp)
        old = path.read_bytes()
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = path.with_name(path.name + ".tmp")
    temp.write_bytes(raw)
    assert temp.read_bytes() == raw and temp.stat().st_size == len(raw)
    temp.replace(path)

positive = '''import TGLExt.V350GateContract
import TGLV350.RegularGeneratedAlgebra
set_option autoImplicit false
open TGLExt ChatgptAudit TGLV350 TGLV350.Regular
noncomputable section
namespace IndependentReview
def unconditionalInclusion (P : SiteProfile) :
    commutantSet (rTowerImage P) ⊆ commutantSet (commutantSet (towerImage P)) :=
  right_commutant_subset_left_bicommutant P
def originalCertificate : ModularRealizationCertificate := TGLExt.V350Gate.checkedModular
example : RegularHilbert (TowerHilbert mixProfile) =
    MeasureTheory.Lp (TowerHilbert mixProfile) 2 (MeasureTheory.volume : MeasureTheory.Measure ℝ) := rfl
example (t : ℝ) (A : (theFactorObject mixProfile).toStarSubalgebra) :
    regularUnitary mixProfile t * fibre (A : WH →L[ℂ] WH) * star (regularUnitary mixProfile t) =
      fibre (TGLExt.V350Continuous.towerWedgeData.modularFlow t A).val :=
  regular_covariance_on_factor mixProfile t A
example (v : WH) : originalCertificate.J v = towerJ mixProfile v := rfl
#check unconditionalInclusion
#check originalCertificate
#check TGLV350.tower_commutation_equality
#check TGLV350.compression_variable_tendsto
#check TGLV350.Regular.regularCore_minimal
#check TGLV350.Regular.regularCoreEmbedding_injective
#check TGLV350.Regular.regular_strongly_continuous
#print axioms unconditionalInclusion
#print axioms originalCertificate
end IndependentReview
end
'''
negative = '''import TGLExt.V350GateContract
set_option autoImplicit false
namespace IndependentNegative
theorem nominal : True := True.intro
def rejectTrue : (P : TGLExt.SiteProfile) → TGLExt.ConverseClauseContract P := nominal
noncomputable def conditional (h : False) : TGLExt.ModularRealizationCertificate := False.elim h
noncomputable def rejectHiddenPremise : TGLExt.ModularRealizationCertificate := conditional
end IndependentNegative
'''
env = os.environ.copy()
env["LEAN_PATH"] = manifest["lean_path"]
env["TMP"] = env["TEMP"] = str(RUN / "tmp")
records = []
for name, text, expected in [("PositiveTypes", positive, 0), ("NegativeTypes", negative, 1)]:
    source = RUN / "sources" / (name + ".lean")
    write(source, text.encode("utf-8"))
    command = [environment["lean"], str(source)]
    result = subprocess.run(command, cwd=RUN / "sources", env=env, capture_output=True)
    write(RUN / "logs" / (name + ".stdout.txt"), result.stdout)
    write(RUN / "logs" / (name + ".stderr.txt"), result.stderr)
    output = result.stdout.decode("utf-8", errors="replace")
    errors = re.findall(r":(\d+):\d+: error:", output)
    record = {"name": name, "command": command, "returncode": result.returncode,
              "expected_returncode": expected, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "error_lines": errors, "passed": result.returncode == expected and (name != "NegativeTypes" or errors == ["5", "7"])}
    records.append(record)
    print(json.dumps(record), flush=True)
    print(output, flush=True)
write(RUN / "type_probes.json", json.dumps(records, indent=2).encode("utf-8"))
