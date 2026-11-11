import TGLExt.V350L2OperatorLift
import Mathlib.Analysis.SpecialFunctions.Gaussian.GaussianIntegral

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 900000

namespace TGLV350.Regular
open MeasureTheory
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- A strictly positive auxiliary profile, with no physical scale parameter. -/
def gaussianProfile (s : ℝ) : ℝ := Real.exp (-(s ^ 2))

theorem gaussianProfile_continuous : Continuous gaussianProfile :=
  ((continuous_id.pow 2).neg).rexp

theorem gaussianProfile_pos (s : ℝ) : 0 < gaussianProfile s := Real.exp_pos _

theorem gaussianProfile_le_one (s : ℝ) : gaussianProfile s ≤ 1 := by
  exact Real.exp_le_one_iff.mpr (neg_nonpos.mpr (sq_nonneg s))

theorem gaussianProfile_memLp_vector (v : H) :
    MemLp (fun s : ℝ => (gaussianProfile s : ℂ) • v) 2 volume := by
  have hm : Continuous (fun s : ℝ => (gaussianProfile s : ℂ) • v) :=
    (Complex.continuous_ofReal.comp gaussianProfile_continuous).smul continuous_const
  apply (memLp_two_iff_integrable_sq_norm hm.aestronglyMeasurable).mpr
  have he : (fun s : ℝ => ‖(gaussianProfile s : ℂ) • v‖ ^ 2) =
      (fun s : ℝ => Real.exp (-2 * s ^ 2) * ‖v‖ ^ 2) := by
    funext s
    rw [norm_smul,Complex.norm_real,Real.norm_eq_abs,
      abs_of_pos (gaussianProfile_pos s),mul_pow]
    congr 1
    unfold gaussianProfile
    rw [pow_two,← Real.exp_add]
    congr 1
    ring
  rw [he]
  exact (integrable_exp_neg_mul_sq (by norm_num : 0 < (2 : ℝ))).mul_const _

#print axioms gaussianProfile
#print axioms gaussianProfile_continuous
#print axioms gaussianProfile_pos
#print axioms gaussianProfile_le_one
#print axioms gaussianProfile_memLp_vector
end
end TGLV350.Regular
