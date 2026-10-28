import TGLExt.V350DualWeightExhaustion
import Mathlib.Topology.Semicontinuity.Basic

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

namespace TGLV350.Regular
open MeasureTheory
open scoped ENNReal ComplexConjugate
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem operatorQuadratic_smul (A : H →L[ℂ] H) (v : H) (c : ℂ) :
    (inner ℂ (c • v) (A (c • v))).re = ‖c‖^2 * (inner ℂ v (A v)).re := by
  simp only [map_smul, inner_smul_left, inner_smul_right, ← mul_assoc,
    Complex.mul_conj, Complex.mul_re, Complex.ofReal_re,
    Complex.ofReal_im, zero_mul, sub_zero, Complex.normSq_eq_norm_sq]

theorem operatorQuadratic_parallelogram (A : H →L[ℂ] H) (v w : H) :
    (inner ℂ (v+w) (A (v+w))).re + (inner ℂ (v-w) (A (v-w))).re =
      2 * (inner ℂ v (A v)).re + 2 * (inner ℂ w (A w)).re := by
  simp only [map_add, map_sub, inner_add_left, inner_sub_left,
    inner_add_right, inner_sub_right, Complex.add_re, Complex.sub_re]
  ring

theorem dualQuadraticIntegrand_smul_vector
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) (c : ℂ)
    (s : ℝ) :
    dualQuadraticIntegrand A (c • v) s =
      ENNReal.ofReal (‖c‖^2) * dualQuadraticIntegrand A v s := by
  unfold dualQuadraticIntegrand
  rw [operatorQuadratic_smul, ENNReal.ofReal_mul (sq_nonneg _)]

/-- Homogeneity in the vector, including c=0 and integral value infinity. -/
theorem dualQuadraticIntegral_smul_vector
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) (c : ℂ) :
    dualQuadraticIntegral A (c • v) =
      ENNReal.ofReal (‖c‖^2) * dualQuadraticIntegral A v := by
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_smul_vector,
    lintegral_const_mul _ (dualQuadraticIntegrand_measurable A v)]
  ac_rfl

theorem dualAmbient_real_smul (s r : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    dualAmbient s (r • A) = r • dualAmbient s A := by
  change dualAmbient s ((r : ℂ) • A) = (r : ℂ) • dualAmbient s A
  exact map_smul (dualAmbient (H := H) s) (r : ℂ) A

theorem dualQuadraticIntegrand_smul_operator (r : ℝ) (hr : 0 ≤ r)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) (s : ℝ) :
    dualQuadraticIntegrand (r • A) v s =
      ENNReal.ofReal r * dualQuadraticIntegrand A v s := by
  unfold dualQuadraticIntegrand
  rw [dualAmbient_real_smul]
  change ENNReal.ofReal (inner ℂ v ((r : ℂ) • dualAmbient s A v)).re = _
  rw [inner_smul_right]
  simp only [Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
  exact ENNReal.ofReal_mul hr

theorem dualQuadraticIntegral_smul_operator (r : ℝ) (hr : 0 ≤ r)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral (r • A) v = ENNReal.ofReal r * dualQuadraticIntegral A v := by
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_smul_operator r hr,
    lintegral_const_mul _ (dualQuadraticIntegrand_measurable A v)]
  ac_rfl

theorem dualQuadraticIntegrand_parallelogram
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (v w : RegularHilbert H) (s : ℝ) :
    dualQuadraticIntegrand A (v+w) s + dualQuadraticIntegrand A (v-w) s =
      2 * dualQuadraticIntegrand A v s + 2 * dualQuadraticIntegrand A w s := by
  unfold dualQuadraticIntegrand
  rw [← ENNReal.ofReal_add (dualQuadratic_nonneg A hA (v+w) s)
    (dualQuadratic_nonneg A hA (v-w) s), operatorQuadratic_parallelogram]
  rw [ENNReal.ofReal_add (mul_nonneg (by norm_num) (dualQuadratic_nonneg A hA v s))
    (mul_nonneg (by norm_num) (dualQuadratic_nonneg A hA w s))]
  simp only [ENNReal.ofReal_mul (by norm_num : (0 : ℝ) ≤ 2), ENNReal.ofReal_ofNat]

/-- The parallelogram law is proved in ENNReal without subtracting infinities. -/
theorem dualQuadraticIntegral_parallelogram
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (v w : RegularHilbert H) :
    dualQuadraticIntegral A (v+w) + dualQuadraticIntegral A (v-w) =
      2 * dualQuadraticIntegral A v + 2 * dualQuadraticIntegral A w := by
  have hsum : (∫⁻ s, dualQuadraticIntegrand A (v+w) s) +
      (∫⁻ s, dualQuadraticIntegrand A (v-w) s) =
      2 * (∫⁻ s, dualQuadraticIntegrand A v s) +
        2 * (∫⁻ s, dualQuadraticIntegrand A w s) := by
    rw [← lintegral_add_left (dualQuadraticIntegrand_measurable A (v+w))]
    calc
      _ = ∫⁻ s, 2 * dualQuadraticIntegrand A v s + 2 * dualQuadraticIntegrand A w s :=
        lintegral_congr (dualQuadraticIntegrand_parallelogram A hA v w)
      _ = _ := by
        rw [lintegral_add_left (measurable_const.mul (dualQuadraticIntegrand_measurable A v)),
          lintegral_const_mul _ (dualQuadraticIntegrand_measurable A v),
          lintegral_const_mul _ (dualQuadraticIntegrand_measurable A w)]
  simp only [dualQuadraticIntegral, ← mul_add]
  rw [hsum]
  ring

theorem dualQuadraticIntegral_add_vector_le
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (v w : RegularHilbert H) :
    dualQuadraticIntegral A (v+w) ≤
      2 * dualQuadraticIntegral A v + 2 * dualQuadraticIntegral A w := by
  rw [← dualQuadraticIntegral_parallelogram A hA v w]
  exact le_self_add

theorem dualCutEvaluation_continuous (R : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    Continuous (fun v : RegularHilbert H => ENNReal.ofReal dualHaarFactor *
      ENNReal.ofReal (inner ℂ v (dualWeightCut R A v)).re) := by
  have h : Continuous (fun v : RegularHilbert H =>
      ENNReal.ofReal (dualHaarFactor * (inner ℂ v (dualWeightCut R A v)).re)) :=
    ENNReal.continuous_ofReal.comp
    (continuous_const.mul (Complex.continuous_re.comp
      (continuous_id.inner (dualWeightCut R A).continuous)))
  simpa only [ENNReal.ofReal_mul dualHaarFactor_pos.le] using h

/-- Lower semicontinuity follows from the actual increasing finite-cut representation. -/
theorem dualQuadraticIntegral_lowerSemicontinuous
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    LowerSemicontinuous (dualQuadraticIntegral A) := by
  have heq : dualQuadraticIntegral A = fun v => ⨆ n : ℕ,
      ENNReal.ofReal dualHaarFactor *
        ENNReal.ofReal (inner ℂ v (dualWeightCut (n : ℝ) A v)).re :=
    funext (dualQuadraticIntegral_eq_iSup_cuts A hA)
  rw [heq]
  exact lowerSemicontinuous_iSup fun n => (dualCutEvaluation_continuous (n : ℝ) A).lowerSemicontinuous

#print axioms operatorQuadratic_smul
#print axioms operatorQuadratic_parallelogram
#print axioms dualQuadraticIntegral_smul_vector
#print axioms dualQuadraticIntegral_smul_operator
#print axioms dualQuadraticIntegral_parallelogram
#print axioms dualQuadraticIntegral_add_vector_le
#print axioms dualCutEvaluation_continuous
#print axioms dualQuadraticIntegral_lowerSemicontinuous
end
end TGLV350.Regular
