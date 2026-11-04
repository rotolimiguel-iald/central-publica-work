import TGLExt.F1Fecho394.CanonicalFockGNSRepresentationR6
import TGLExt.F1Fecho394.GenericGNSOrderR2
/-! Positivity and bounded-strong continuity of the actual Fock weight GNS representation. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockGNSOrder
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation
open scoped Topology
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : PartialOrder (GNSHilbert →L[ℂ] GNSHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := GNSHilbert)
/-- Transfer bounded strong nets to the actual completed finite-ideal representation.
This does not claim closability of the involutive graph. -/
theorem scalarGNSRepresentation_tendsto_of_uniformly_bounded 
    {ι : Type*} {l : Filter ι}
    (T : ι → core.toStarSubalgebra)
    (B : core.toStarSubalgebra) (C : ℝ)
    (hbound : ∀ i, ‖(T i).val‖ ≤ C)
    (hT : ∀ v, Tendsto (fun i => (T i).val v) l (𝓝 (B.val v)))
    (v : GNSHilbert) :
    Tendsto (fun i => scalarGNSRepresentation (T i) v) l
      (𝓝 (scalarGNSRepresentation B v)) :=
  F1Fecho.GenericGNSOrder.scalarGNSRepresentation_tendsto_of_uniformly_bounded
    weightContext T B C hbound hT v

theorem scalarGNSRepresentation_nonneg 
    (B : core.toStarSubalgebra) (hB : 0 ≤ B) :
    0 ≤ scalarGNSRepresentation B :=
  F1Fecho.GenericGNSOrder.scalarGNSRepresentation_nonneg weightContext B hB

theorem scalarGNSRepresentation_monotone  :
    Monotone (scalarGNSRepresentation) :=
  F1Fecho.GenericGNSOrder.scalarGNSRepresentation_monotone weightContext

end F1Fecho.CanonicalFockGNSOrder
#print axioms F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_tendsto_of_uniformly_bounded
#print axioms F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_nonneg
#print axioms F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_monotone
