import TGLExt.V350ScalarGNSRepresentation
import TGLExt.V350DualOrbitStrongLimits
import TGLExt.V350RegularNormality

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

/-- Transfer bounded strong nets to the actual completed finite-ideal representation.
This does not claim closability of the involutive graph. -/
theorem scalarGNSRepresentation_tendsto_of_uniformly_bounded (P : SiteProfile)
    {ι : Type*} {l : Filter ι}
    (T : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (C : ℝ)
    (hbound : ∀ i, ‖(T i).val‖ ≤ C)
    (hT : ∀ v, Tendsto (fun i => (T i).val v) l (𝓝 (B.val v)))
    (v : ScalarGNSHilbert P) :
    Tendsto (fun i => scalarGNSRepresentation P (T i) v) l
      (𝓝 (scalarGNSRepresentation P B v)) := by
  apply tendsto_subtype_rng.mpr
  exact dualOrbit_tendsto_of_uniformly_bounded
    (fun i => (T i).val) B.val C hbound hT v.val

#print axioms scalarGNSRepresentation_tendsto_of_uniformly_bounded
end
end TGLV350.Regular
