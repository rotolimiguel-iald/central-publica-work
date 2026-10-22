import TGLExt.V350L2CutIntegral
import TGLExt.V350ZeroFromTranslatedCuts

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Translation and character commutation determine one constant fibre action.
The conclusion holds on all of Lebesgue L2, with no separability assumption on H. -/
theorem eq_fibre_of_shift_character_commutation
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hshift : ∀ t : ℝ, shift t * B = B * shift t)
    (hchar : ∀ s : ℝ, characterMultiplier s * B = B * characterMultiplier s) :
    B = fibre (fibreCandidate B) := by
  have hcut := character_commutation_measurableCut B hchar
  have hproj := commutes_unitIntervalProjection B hshift
    (hcut (Set.Ioc (0 : ℝ) 1) measurableSet_Ioc)
  let A := B - fibre (fibreCandidate B)
  have hAsh : ∀ t : ℝ, shift t * A = A * shift t := by
    intro t
    dsimp only [A]
    rw [mul_sub, sub_mul, hshift, shift_commutes_fibre]
  have hAcut : ∀ (S : Set ℝ) (hS : MeasurableSet S),
      measurableCut S hS * A = A * measurableCut S hS := by
    intro S hS
    dsimp only [A]
    rw [mul_sub, sub_mul, hcut S hS, fibre_commutes_measurableCut]
  have hread : ∀ f : RegularHilbert H, testEmbeddingCLM.adjoint (A f) = 0 := by
    intro f
    change testEmbeddingCLM.adjoint (B f - fibre (fibreCandidate B) f) = 0
    rw [map_sub, commutation_fibreCandidate_read B hproj, testEmbedding_adjoint_fibre, sub_self]
  have hz := eq_zero_of_shift_commutation_unitCut_zero A hAsh
    (unitCut_mul_eq_zero_of_zero_read A hAcut hread)
  exact sub_eq_zero.mp hz

theorem existsUnique_fibre_of_shift_character_commutation
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hshift : ∀ t : ℝ, shift t * B = B * shift t)
    (hchar : ∀ s : ℝ, characterMultiplier s * B = B * characterMultiplier s) :
    ∃! C : H →L[ℂ] H, B = fibre C := by
  refine ⟨fibreCandidate B, eq_fibre_of_shift_character_commutation B hshift hchar, ?_⟩
  intro C hC
  apply fibre_injective
  exact hC.symm.trans (eq_fibre_of_shift_character_commutation B hshift hchar)

/-- Every fixed-core operator is a constant fibre on the original tower Hilbert
space. Membership of the extracted fibre operator in the original algebra M
is still a separate obligation. -/
theorem dualFixedCore_eq_fibre_candidate (P : TGLExt.SiteProfile)
    (B : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))
    (hB : B ∈ dualFixedCore P) : B = fibre (fibreCandidate B) :=
  eq_fibre_of_shift_character_commutation B
    (fun t => (dualFixedCore_commutes_shift_and_character P B hB t).1)
    (fun s => (dualFixedCore_commutes_shift_and_character P B hB s).2)

#print axioms eq_fibre_of_shift_character_commutation
#print axioms existsUnique_fibre_of_shift_character_commutation
#print axioms dualFixedCore_eq_fibre_candidate
end
end TGLV350.Regular
