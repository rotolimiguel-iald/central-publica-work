import TGLExt.F1Fecho394.RegularScalarGNSRepresentationR2
import TGLExt.V350DualOrbitStrongLimits
/-! Positivity and bounded-strong continuity of the actual Fock weight GNS representation. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.GenericGNSOrder
open TGLV350.Regular MeasureTheory Filter
open F1Fecho.RegularScalarGNS F1Fecho.RegularScalarGNSRepresentation
open scoped Topology
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (D : Context H)
/-- Transfer bounded strong nets to the actual completed finite-ideal representation.
This does not claim closability of the involutive graph. -/
theorem scalarGNSRepresentation_tendsto_of_uniformly_bounded 
    {ι : Type*} {l : Filter ι}
    (T : ι → D.algebra.toStarSubalgebra)
    (B : D.algebra.toStarSubalgebra) (C : ℝ)
    (hbound : ∀ i, ‖(T i).val‖ ≤ C)
    (hT : ∀ v, Tendsto (fun i => (T i).val v) l (𝓝 (B.val v)))
    (v : (GNSHilbert D)) :
    Tendsto (fun i => scalarGNSRepresentation D (T i) v) l
      (𝓝 (scalarGNSRepresentation D B v)) := by
  apply tendsto_subtype_rng.mpr
  exact dualOrbit_tendsto_of_uniformly_bounded
    (fun i => (T i).val) B.val C hbound hT v.val

theorem scalarGNSRepresentation_nonneg 
    (B : D.algebra.toStarSubalgebra) (hB : 0 ≤ B) :
    0 ≤ scalarGNSRepresentation D B := by
  have ha : 0 ≤ dualOrbitRepresentation B.val := by
    have h := OrderHomClass.monotone (dualOrbitRepresentation (H:=H))
      (show (0 : RegularHilbert H →L[ℂ] RegularHilbert H) ≤ B.val from hB)
    simpa only [map_zero] using h
  rw [ContinuousLinearMap.nonneg_iff_isPositive,
    ContinuousLinearMap.isPositive_iff_complex] at ha ⊢
  intro v
  exact ha v.val

theorem scalarGNSRepresentation_monotone  :
    Monotone (scalarGNSRepresentation D) := by
  intro A B h
  have hp := scalarGNSRepresentation_nonneg D (B-A) (sub_nonneg.mpr h)
  rw [map_sub] at hp
  exact sub_nonneg.mp hp

end F1Fecho.GenericGNSOrder
#print axioms F1Fecho.GenericGNSOrder.scalarGNSRepresentation_tendsto_of_uniformly_bounded
#print axioms F1Fecho.GenericGNSOrder.scalarGNSRepresentation_nonneg
#print axioms F1Fecho.GenericGNSOrder.scalarGNSRepresentation_monotone
