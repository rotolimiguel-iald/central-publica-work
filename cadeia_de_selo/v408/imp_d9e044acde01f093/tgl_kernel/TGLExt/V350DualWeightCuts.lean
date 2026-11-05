import TGLExt.V350StrongOperatorIntegral
import TGLExt.V350RegularDualAction

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1200000

namespace TGLV350.Regular
open MeasureTheory TGLExt
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The actual dual orbit, strongly continuous and bounded by unitary conjugation. -/
def dualIntegralFamily (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    StrongIntegral.Family (H := RegularHilbert H) where
  op := fun s => dualAmbient s A
  continuous_apply := dualAmbient_strongly_continuous A
  bound := ‖A‖
  bound_nonneg := norm_nonneg A
  norm_bound := fun s => le_of_eq
    ((StarAlgEquiv.isometry (dualAmbient (H := H) s)).norm_map_of_map_zero
      (map_zero (dualAmbient (H := H) s)) A)

/-- A finite strong integral of the dual action. This is unnormalized, and is
only a bounded cutoff of the prospective operator-valued weight. -/
def dualWeightCut (R : ℝ) (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    RegularHilbert H →L[ℂ] RegularHilbert H :=
  StrongIntegral.operatorIntegral (dualIntegralFamily A) (-R) R

theorem dualWeightCut_apply (R : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualWeightCut R A v = ∫ s in (-R)..R, dualAmbient s A v := rfl

theorem dualWeightCut_norm_le (R : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    ‖dualWeightCut R A‖ ≤ ‖A‖ * |2*R| := by
  have h := StrongIntegral.operatorIntegral_norm_le (dualIntegralFamily A) (-R) R
  convert h using 1 <;> dsimp [dualWeightCut, dualIntegralFamily] <;> congr 2 <;> ring

theorem dualAmbient_nonneg (s : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    0 ≤ dualAmbient s A := by
  have h := OrderHomClass.monotone (dualAmbient (H := H) s) hA
  simpa only [map_zero] using h

theorem dualWeightCut_nonneg (R : ℝ) (hR : 0 ≤ R)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    0 ≤ dualWeightCut R A :=
  StrongIntegral.operatorIntegral_nonneg (dualIntegralFamily A) (-R) R (by linarith)
    (fun s => dualAmbient_nonneg s A hA)

theorem dualWeightCut_mono_radius {R S : ℝ} (hR : 0 ≤ R) (hRS : R ≤ S)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    dualWeightCut R A ≤ dualWeightCut S A :=
  StrongIntegral.operatorIntegral_mono_interval (dualIntegralFamily A)
    (neg_le_neg hRS) (by linarith) hRS (fun s => dualAmbient_nonneg s A hA)

/-- Each cutoff belongs to the same generated algebra, not to a replacement model. -/
theorem dualWeightCut_mem (P : SiteProfile) (R : ℝ)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hA : A ∈ regularCoreAlgebra P) : dualWeightCut R A ∈ regularCoreAlgebra P := by
  apply StrongIntegral.operatorIntegral_mem
  intro s
  exact (regularDualAction P s ⟨A, hA⟩).property

/-- On the embedded algebra the unnormalized dual integral grows with interval length. -/
theorem dualWeightCut_fibre (R : ℝ) (A : H →L[ℂ] H) :
    dualWeightCut R (fibre A) = (2*R : ℝ) • fibre A := by
  apply ContinuousLinearMap.ext
  intro v
  rw [dualWeightCut_apply]
  simp only [dualAmbient_fibre, intervalIntegral.integral_const]
  change (R - -R) • fibre A v = (2*R : ℝ) • fibre A v
  congr 1
  ring

theorem dualWeightCut_one (R : ℝ) :
    dualWeightCut R (1 : RegularHilbert H →L[ℂ] RegularHilbert H) =
      (2*R : ℝ) • (1 : RegularHilbert H →L[ℂ] RegularHilbert H) := by
  simpa only [fibre_one] using dualWeightCut_fibre R (1 : H →L[ℂ] H)

#print axioms dualIntegralFamily
#print axioms dualWeightCut_apply
#print axioms dualWeightCut_norm_le
#print axioms dualWeightCut_nonneg
#print axioms dualWeightCut_mono_radius
#print axioms dualWeightCut_mem
#print axioms dualWeightCut_fibre
#print axioms dualWeightCut_one
end
end TGLV350.Regular
