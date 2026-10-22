from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "dual_latest_run.txt").read_text(encoding="utf-8"))
manifest = json.loads((RUN / "manifest.json").read_bytes())
environment = json.loads((ROOT / "environment.json").read_bytes())

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
    assert temp.read_bytes() == raw and temp.stat().st_size == len(raw)
    temp.replace(p)

source_text = '''import TGLV350.RegularDualAction
import TGLV350.L2BoundedStrongContinuity
set_option autoImplicit false
set_option maxHeartbeats 1000000
open TGLExt TGLV350.Regular Filter
open scoped Topology
noncomputable section
universe u
namespace DualIndependentTypes
example (P : SiteProfile) (s t : ℝ) :
    (regularDualAction P s ⟨regularUnitary P t, regularUnitary_mem P t⟩).val =
      Complex.exp (-Complex.I * (s : ℂ) * (t : ℂ)) • regularUnitary P t := by
  change dualAmbient s (regularUnitary P t) = _
  exact dualAmbient_regular P s t
example (P : SiteProfile) (s : ℝ) (A : (regularCoreAlgebra P).toStarSubalgebra) :
    regularDualAction P (-s) (regularDualAction P s A) = A := by
  calc
    _ = regularDualAction P (s + -s) A := by rw [regularDualAction_add]; rfl
    _ = A := by rw [add_neg_cancel, regularDualAction_zero]; rfl
example (P : SiteProfile) (s : ℝ) (A : (theFactorObject P).toStarSubalgebra) :
    regularDualAction P s (regularCoreEmbedding P A) = regularCoreEmbedding P A :=
  regularDualAction_fixes_embedding P s A
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
def anyFilter {ι : Type u} (l : Filter ι)
    (T : ι → (H →L[ℂ] H)) (S : H →L[ℂ] H) (C : ℝ)
    (hbound : ∀ i, ‖T i‖ ≤ C)
    (hT : ∀ v : H, Tendsto (fun i => T i v) l (𝓝 (S v)))
    (f : RegularHilbert H) :
    Tendsto (fun i => fibre (T i) f) l (𝓝 (fibre S f)) :=
  fibre_tendsto_of_uniformly_bounded T S C hbound hT f
#check anyFilter
#print axioms anyFilter
end DualIndependentTypes
end
'''
source = RUN / "sources/DualTypeBoundary.lean"
write(source, source_text.encode("utf-8"))
env = os.environ.copy()
env["LEAN_PATH"] = manifest["lean_path"]
env["TMP"] = env["TEMP"] = str(RUN / "tmp")
command = [environment["lean"], str(source)]
result = subprocess.run(command, cwd=RUN / "sources", env=env, capture_output=True)
write(RUN / "logs/DualTypeBoundary.stdout.txt", result.stdout)
write(RUN / "logs/DualTypeBoundary.stderr.txt", result.stderr)
record = {"command": command, "returncode": result.returncode,
          "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
          "cases": ["negative Weyl sign on restricted algebra", "inverse on every algebra element", "same embedding fixed", "arbitrary universe/index/filter without topology or NeBot"]}
write(RUN / "type_probes.json", json.dumps(record, indent=2).encode("utf-8"))
print(json.dumps(record), flush=True)
print(result.stdout.decode("utf-8", errors="replace"), flush=True)
