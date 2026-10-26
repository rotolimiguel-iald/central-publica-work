import TGLExt.V350RegularNormality
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1200000

namespace TGLV350.StrongIntegral
open MeasureTheory
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Data for a bounded strongly continuous family. No operator-norm continuity
or Bochner integrability with values in B(H) is assumed. -/
structure Family where
  op : ℝ → (H →L[ℂ] H)
  continuous_apply : ∀ v, Continuous (fun t => op t v)
  bound : ℝ
  bound_nonneg : 0 ≤ bound
  norm_bound : ∀ t, ‖op t‖ ≤ bound

def vectorIntegral (F : Family (H := H)) (a b : ℝ) (v : H) : H :=
  ∫ t in a..b, F.op t v

theorem vectorIntegral_add (F : Family (H := H)) (a b : ℝ) (v w : H) :
    vectorIntegral F a b (v+w) = vectorIntegral F a b v + vectorIntegral F a b w := by
  simp only [vectorIntegral, map_add]
  exact intervalIntegral.integral_add
    ((F.continuous_apply v).intervalIntegrable a b)
    ((F.continuous_apply w).intervalIntegrable a b)

theorem vectorIntegral_smul (F : Family (H := H)) (a b : ℝ) (c : ℂ) (v : H) :
    vectorIntegral F a b (c • v) = c • vectorIntegral F a b v := by
  simp only [vectorIntegral, map_smul, intervalIntegral.integral_smul]

theorem vectorIntegral_bound (F : Family (H := H)) (a b : ℝ) (v : H) :
    ‖vectorIntegral F a b v‖ ≤ (F.bound * |b-a|) * ‖v‖ := by
  have hb := intervalIntegral.norm_integral_le_of_norm_le_const
    (a := a) (b := b) (fun t _ => (F.op t).le_of_opNorm_le (F.norm_bound t) v)
  calc
    ‖vectorIntegral F a b v‖ ≤ (F.bound * ‖v‖) * |b-a| := hb
    _ = _ := by ring

/-- The integral is constructed on vectors and then proved to be a bounded operator. -/
def operatorIntegral (F : Family (H := H)) (a b : ℝ) : H →L[ℂ] H :=
  ({ toFun := vectorIntegral F a b
     map_add' := vectorIntegral_add F a b
     map_smul' := vectorIntegral_smul F a b } : H →ₗ[ℂ] H).mkContinuous
    (F.bound * |b-a|) (vectorIntegral_bound F a b)

theorem operatorIntegral_apply (F : Family (H := H)) (a b : ℝ) (v : H) :
    operatorIntegral F a b v = ∫ t in a..b, F.op t v := rfl

theorem operatorIntegral_norm_le (F : Family (H := H)) (a b : ℝ) :
    ‖operatorIntegral F a b‖ ≤ F.bound * |b-a| :=
  ContinuousLinearMap.opNorm_le_bound _ (mul_nonneg F.bound_nonneg (abs_nonneg _))
    (vectorIntegral_bound F a b)

theorem operatorIntegral_commutes (F : Family (H := H)) (a b : ℝ)
    (B : H →L[ℂ] H) (hcomm : ∀ t, B * F.op t = F.op t * B) :
    B * operatorIntegral F a b = operatorIntegral F a b * B := by
  ext v
  change B (∫ t in a..b, F.op t v) = ∫ t in a..b, F.op t (B v)
  rw [← B.intervalIntegral_comp_comm ((F.continuous_apply v).intervalIntegrable a b)]
  apply intervalIntegral.integral_congr
  intro t _
  exact congrArg (fun T : H →L[ℂ] H => T v) (hcomm t)

/-- The integral belongs to the same concrete von Neumann algebra as its integrands. -/
theorem operatorIntegral_mem (F : Family (H := H)) (a b : ℝ)
    (N : VonNeumannAlgebra H) (hmem : ∀ t, F.op t ∈ N) : operatorIntegral F a b ∈ N := by
  rw [← SetLike.mem_coe, ← VonNeumannAlgebra.centralizer_centralizer]
  rw [Set.mem_centralizer_iff]
  intro B hB
  apply operatorIntegral_commutes
  intro t
  exact (hB (F.op t) (hmem t)).symm

theorem inner_operatorIntegral (F : Family (H := H)) (a b : ℝ) (v w : H) :
    inner ℂ v (operatorIntegral F a b w) = ∫ t in a..b, inner ℂ v (F.op t w) := by
  exact ((innerSL ℂ v).intervalIntegral_comp_comm
    ((F.continuous_apply w).intervalIntegrable a b)).symm

theorem re_inner_operatorIntegral (F : Family (H := H)) (a b : ℝ) (v w : H) :
    (inner ℂ v (operatorIntegral F a b w)).re =
      ∫ t in a..b, (inner ℂ v (F.op t w)).re := by
  rw [inner_operatorIntegral]
  exact (Complex.reCLM.intervalIntegral_comp_comm
    ((continuous_const.inner (F.continuous_apply w)).intervalIntegrable a b)).symm

theorem operatorIntegral_inner (F : Family (H := H)) (a b : ℝ) (v w : H) :
    inner ℂ (operatorIntegral F a b v) w = ∫ t in a..b, inner ℂ (F.op t v) w := by
  rw [← inner_conj_symm (operatorIntegral F a b v) w,
    inner_operatorIntegral, ← intervalIntegral.intervalIntegral_conj]
  apply intervalIntegral.integral_congr
  intro t _
  exact inner_conj_symm _ _

/-- A positive integrand has a positive strong integral over an oriented interval a≤b. -/
theorem operatorIntegral_nonneg (F : Family (H := H)) (a b : ℝ) (hab : a ≤ b)
    (hpos : ∀ t, 0 ≤ F.op t) : 0 ≤ operatorIntegral F a b := by
  rw [ContinuousLinearMap.nonneg_iff_isPositive, ContinuousLinearMap.isPositive_def]
  constructor
  · intro v w
    change inner ℂ (operatorIntegral F a b v) w = inner ℂ v (operatorIntegral F a b w)
    rw [operatorIntegral_inner, inner_operatorIntegral]
    apply intervalIntegral.integral_congr
    intro t _
    exact ((ContinuousLinearMap.nonneg_iff_isPositive _).mp (hpos t)).inner_left_eq_inner_right v w
  · intro v
    change 0 ≤ RCLike.re (inner ℂ (operatorIntegral F a b v) v)
    rw [inner_re_symm]
    change 0 ≤ (inner ℂ v (operatorIntegral F a b v)).re
    rw [re_inner_operatorIntegral]
    apply intervalIntegral.integral_nonneg_of_forall hab
    intro t
    exact ((ContinuousLinearMap.nonneg_iff_isPositive _).mp (hpos t)).re_inner_nonneg_right v

/-- Positive cuts increase when the integration interval increases. -/
theorem operatorIntegral_mono_interval (F : Family (H := H)) {a b c d : ℝ}
    (hca : c ≤ a) (hab : a ≤ b) (hbd : b ≤ d) (hpos : ∀ t, 0 ≤ F.op t) :
    operatorIntegral F a b ≤ operatorIntegral F c d := by
  rw [← sub_nonneg, ContinuousLinearMap.nonneg_iff_isPositive,
    ContinuousLinearMap.isPositive_def']
  constructor
  · exact (IsSelfAdjoint.of_nonneg (operatorIntegral_nonneg F c d (hca.trans (hab.trans hbd)) hpos)).sub
      (IsSelfAdjoint.of_nonneg (operatorIntegral_nonneg F a b hab hpos))
  · intro v
    change 0 ≤ RCLike.re (inner ℂ ((operatorIntegral F c d - operatorIntegral F a b) v) v)
    rw [inner_re_symm]
    change 0 ≤ (inner ℂ v ((operatorIntegral F c d - operatorIntegral F a b) v)).re
    simp only [sub_apply, inner_sub_right, Complex.sub_re,
      re_inner_operatorIntegral, sub_nonneg]
    apply intervalIntegral.integral_mono_interval hca hab hbd
    · exact Filter.Eventually.of_forall fun t =>
        ((ContinuousLinearMap.nonneg_iff_isPositive _).mp (hpos t)).re_inner_nonneg_right v
    · exact (Complex.continuous_re.comp
        (continuous_const.inner (F.continuous_apply v))).intervalIntegrable c d

#print axioms operatorIntegral
#print axioms operatorIntegral_norm_le
#print axioms operatorIntegral_mem
#print axioms inner_operatorIntegral
#print axioms operatorIntegral_nonneg
#print axioms operatorIntegral_mono_interval
end
end TGLV350.StrongIntegral
