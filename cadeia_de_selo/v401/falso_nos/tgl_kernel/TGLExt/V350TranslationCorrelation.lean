import TGLExt.V350UnitIntervalProjection
import Mathlib.Analysis.Convolution

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 600000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def realInnerBilinear : H →L[ℝ] H →L[ℝ] ℂ :=
  (LinearMap.mk₂ ℝ (inner ℂ)
    (fun x y z => inner_add_left x y z)
    (fun r x y => by
      rw [RCLike.real_smul_eq_coe_smul (K := ℂ) r x]
      exact inner_smul_real_left (𝕜 := ℂ) x y r)
    (fun x y z => inner_add_right x y z)
    (fun r x y => by
      rw [RCLike.real_smul_eq_coe_smul (K := ℂ) r y]
      exact inner_smul_real_right (𝕜 := ℂ) x y r)
    ).mkContinuous₂ 1 (fun x y => by
      change ‖inner ℂ x y‖ ≤ 1 * ‖x‖ * ‖y‖
      simpa only [one_mul] using norm_inner_le_norm x y)

theorem translationCorrelation_integrable (f g : ℝ → H)
    (hf : Integrable f) (hg : Integrable g) :
    Integrable (fun p : ℝ × ℝ => inner ℂ (g p.2) (f (p.2 - p.1)))
      (volume.prod volume) := by
  have hi := hg.convolution_integrand (realInnerBilinear (H := H)) hf.comp_neg
  change Integrable (fun p : ℝ × ℝ => inner ℂ (g p.2) (f (-(p.1-p.2))))
    (volume.prod volume) at hi
  simpa only [neg_sub] using hi

theorem integral_translationCorrelation (f g : ℝ → H)
    (hf : Integrable f) (hg : Integrable g) :
    (∫ t : ℝ, ∫ x : ℝ, inner ℂ (g x) (f (x-t))) =
      inner ℂ (∫ x : ℝ, g x) (∫ x : ℝ, f x) := by
  rw [integral_integral_swap (translationCorrelation_integrable f g hf hg)]
  have he : ∀ x : ℝ, (∫ t : ℝ, inner ℂ (g x) (f (x-t))) =
      inner ℂ (g x) (∫ t : ℝ, f t) := by
    intro x
    rw [show (∫ t : ℝ, inner ℂ (g x) (f (x-t))) =
        ∫ t : ℝ, inner ℂ (g x) (f t) from
      integral_sub_left_eq_self (fun t : ℝ => inner ℂ (g x) (f t)) volume x]
    exact integral_inner hf (g x)
  simp_rw [he]
  have hi := integral_inner (𝕜 := ℂ) hg (∫ x : ℝ, f x)
  have hc := congrArg (starRingEnd ℂ) hi
  rw [← integral_conj] at hc
  simpa only [inner_conj_symm] using hc

#print axioms translationCorrelation_integrable
#print axioms integral_translationCorrelation
end
end TGLV350.Regular
