import TGLExt.F1Fecho394.RegularScalarGNSRepresentationR2
import TGLExt.V350DualOrbitStrongLimits
/-! Bounded strong nets act strongly on the actual scalar dual-weight GNS
completion. This transports the concrete representation, not a trace law. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularScalarGNSStrongContinuity
open TGLV350.Regular Filter F1Fecho.RegularScalarGNS F1Fecho.RegularScalarGNSRepresentation
open scoped Topology
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem scalarGNSRepresentation_tendsto_of_uniformly_bounded (D : Context H)
    {ι : Type*} {l : Filter ι}
    (T : ι → D.algebra.toStarSubalgebra) (B : D.algebra.toStarSubalgebra) (C : ℝ)
    (hbound : ∀ i, ‖(T i).val‖ ≤ C)
    (hT : ∀ v, Tendsto (fun i => (T i).val v) l (𝓝 (B.val v)))
    (v : GNSHilbert D) :
    Tendsto (fun i => scalarGNSRepresentation D (T i) v) l
      (𝓝 (scalarGNSRepresentation D B v)) := by
  apply tendsto_subtype_rng.mpr
  exact dualOrbit_tendsto_of_uniformly_bounded
    (fun i => (T i).val) B.val C hbound hT v.val
end F1Fecho.RegularScalarGNSStrongContinuity
#print axioms F1Fecho.RegularScalarGNSStrongContinuity.scalarGNSRepresentation_tendsto_of_uniformly_bounded
