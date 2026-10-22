import TGLExt.V350DualClosedForm
import TGLExt.MonotoneOperatorLimit
import Mathlib.MeasureTheory.Measure.OpenPos

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

namespace TGLV350.Regular
open MeasureTheory
open scoped ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem dualQuadraticIntegrand_continuous
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    Continuous (dualQuadraticIntegrand A v) :=
  ENNReal.continuous_ofReal.comp (Complex.continuous_re.comp
    (continuous_const.inner (dualAmbient_strongly_continuous A v)))

/-- Continuity and full support of Lebesgue upgrade vanishing almost everywhere
to vanishing at every dual parameter. -/
theorem dualQuadraticIntegral_zero_iff_integrand_zero
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral A v = 0 ↔ ∀ s, dualQuadraticIntegrand A v s = 0 := by
  have hc : ENNReal.ofReal dualHaarFactor ≠ 0 :=
    ne_of_gt (ENNReal.ofReal_pos.mpr dualHaarFactor_pos)
  constructor
  · intro h
    have hi : (∫⁻ s : ℝ, dualQuadraticIntegrand A v s) = 0 :=
      (mul_eq_zero.mp h).resolve_left hc
    have hae := (lintegral_eq_zero_iff (dualQuadraticIntegrand_measurable A v)).mp hi
    have heq := MeasureTheory.Measure.eq_of_ae_eq hae
      (dualQuadraticIntegrand_continuous A v) continuous_const
    exact fun s => congrFun heq s
  · intro h
    have heq : dualQuadraticIntegrand A v = 0 := funext h
    simp only [dualQuadraticIntegral, heq, Pi.zero_apply, lintegral_zero, mul_zero]

/-- On a positive input, a zero integral cannot hide a nonzero action at s=0. -/
theorem dualQuadraticIntegral_zero_implies_apply_zero
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (v : RegularHilbert H) (hv : dualQuadraticIntegral A v = 0) : A v = 0 := by
  have hz := (dualQuadraticIntegral_zero_iff_integrand_zero A v).mp hv 0
  have hzero : ENNReal.ofReal (inner ℂ v (A v)).re = 0 := by
    unfold dualQuadraticIntegrand at hz
    rw [dualAmbient_zero] at hz
    exact hz
  have hn := dualQuadratic_nonneg A hA v 0
  rw [dualAmbient_zero] at hn
  have hq : (inner ℂ v (A v)).re = 0 := le_antisymm (ENNReal.ofReal_eq_zero.mp hzero) hn
  have hb := ChatgptAudit.Expectation047.positive_apply_norm_sq_le A hA v
  change ‖A v‖^2 ≤ ‖A‖ * (inner ℂ v (A v)).re at hb
  rw [hq, mul_zero] at hb
  have hnorm : ‖A v‖ = 0 := by nlinarith [sq_nonneg ‖A v‖]
  exact norm_eq_zero.mp hnorm

/-- Faithfulness of the positive-input evaluation family. This is not yet a
faithful normal semifinite trace or a constructed operator-valued weight. -/
theorem dualQuadraticIntegral_faithful
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    (∀ v, dualQuadraticIntegral A v = 0) ↔ A = 0 := by
  constructor
  · intro h
    apply ContinuousLinearMap.ext
    intro v
    exact dualQuadraticIntegral_zero_implies_apply_zero A hA v (h v)
  · rintro rfl
    exact dualQuadraticIntegral_zero

theorem dualQuadraticIntegral_detects_nonzero_positive
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hne : A ≠ 0) :
    ∃ v, 0 < dualQuadraticIntegral A v := by
  by_contra! h
  apply hne
  exact (dualQuadraticIntegral_faithful A hA).mp (fun v => le_antisymm (h v) bot_le)

/-- Positivity of the operator increment gives monotonicity of every evaluation. -/
theorem dualQuadraticIntegral_mono
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H) (hAB : A ≤ B)
    (v : RegularHilbert H) : dualQuadraticIntegral A v ≤ dualQuadraticIntegral B v := by
  apply mul_le_mul_right
  apply lintegral_mono
  intro s
  apply ENNReal.ofReal_le_ofReal
  have hd := dualAmbient_nonneg s (B-A) (sub_nonneg.mpr hAB)
  have hq := ((ContinuousLinearMap.nonneg_iff_isPositive _).mp hd).re_inner_nonneg_right v
  simp only [map_sub, _root_.sub_apply, inner_sub_right] at hq
  exact sub_nonneg.mp hq

#print axioms dualQuadraticIntegrand_continuous
#print axioms dualQuadraticIntegral_zero_iff_integrand_zero
#print axioms dualQuadraticIntegral_zero_implies_apply_zero
#print axioms dualQuadraticIntegral_faithful
#print axioms dualQuadraticIntegral_detects_nonzero_positive
#print axioms dualQuadraticIntegral_mono
end
end TGLV350.Regular
