import TGLExt.V350CharacterLocality
import TGLExt.V350L2MeasurableCut
import TGLExt.V350FixedCoreShiftCommutation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2000000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Commutation with every character forces commutation with every measurable
cut. The Fourier argument takes place on L1 pairings of actual L2 vectors. -/
theorem character_commutation_measurableCut
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hB : ∀ s : ℝ, characterMultiplier s * B = B * characterMultiplier s)
    (S : Set ℝ) (hS : MeasurableSet S) :
    measurableCut S hS * B = B * measurableCut S hS := by
  apply ContinuousLinearMap.ext
  intro g
  apply ext_inner_left ℂ
  intro f
  change inner ℂ f (measurableCut S hS (B g)) = inner ℂ f (B (measurableCut S hS g))
  rw [← ContinuousLinearMap.adjoint_inner_left B (measurableCut S hS g) f,
    measurableCut_inner, measurableCut_inner]
  exact integral_congr_ae (ae_restrict_of_ae (character_commutation_local_pairing B hB f g).symm)

/-- Fixed core operators preserve every measurable spatial cut. Membership in
F still does not assert that the corresponding fibre action is constant. -/
theorem dualFixedCore_commutes_measurableCut (P : TGLExt.SiteProfile)
    (B : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))
    (hB : B ∈ dualFixedCore P) (S : Set ℝ) (hS : MeasurableSet S) :
    measurableCut S hS * B = B * measurableCut S hS :=
  character_commutation_measurableCut B
    (fun s => (dualFixedCore_commutes_shift_and_character P B hB s).2) S hS

#print axioms character_commutation_measurableCut
#print axioms dualFixedCore_commutes_measurableCut
end
end TGLV350.Regular
