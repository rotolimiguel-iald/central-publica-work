import TGLExt.V350RegularApproximation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open MeasureTheory Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def shiftCharacterFamily (s : ℝ) : StrongIntegral.Family (H := RegularHilbert H) where
  op t := characterPhase s t • shift t
  continuous_apply v := (characterPhase_continuous s).smul (shift_strongly_continuous v)
  bound := 1
  bound_nonneg := zero_le_one
  norm_bound t := ContinuousLinearMap.opNorm_le_bound _ zero_le_one (fun v => by
    change ‖characterPhase s t • shift t v‖ ≤ 1 * ‖v‖
    rw [norm_smul,characterPhase_norm,shift_norm])

def shiftCharacterAverage (s h : ℝ) : RegularHilbert H →L[ℂ] RegularHilbert H :=
  (h⁻¹ : ℝ) • StrongIntegral.operatorIntegral (shiftCharacterFamily s) 0 h

theorem shiftCharacterAverage_apply (s h : ℝ) (v : RegularHilbert H) :
    shiftCharacterAverage s h v = h⁻¹ • ∫ t in 0..h, characterPhase s t • shift t v := rfl

theorem shiftCharacterAverage_norm_le_one (s h : ℝ) :
    ‖shiftCharacterAverage (H := H) s h‖ ≤ 1 := by
  by_cases hh : h = 0
  · subst h
    simp [shiftCharacterAverage]
  · have hb := StrongIntegral.operatorIntegral_norm_le (shiftCharacterFamily (H := H) s) 0 h
    change ‖StrongIntegral.operatorIntegral (shiftCharacterFamily (H := H) s) 0 h‖ ≤ 1 * |h-0| at hb
    simp only [sub_zero,one_mul] at hb
    calc
      ‖shiftCharacterAverage (H := H) s h‖ = |h⁻¹| *
          ‖StrongIntegral.operatorIntegral (shiftCharacterFamily (H := H) s) 0 h‖ := by
        change ‖((h⁻¹ : ℝ) : ℂ) • StrongIntegral.operatorIntegral (shiftCharacterFamily s) 0 h‖ = _
        rw [norm_smul,Complex.norm_real,Real.norm_eq_abs]
      _ ≤ |h⁻¹| * |h| := mul_le_mul_of_nonneg_left hb (abs_nonneg _)
      _ = 1 := by rw [abs_inv,inv_mul_cancel₀ (abs_ne_zero.mpr hh)]

theorem shiftCharacterAverage_norm_map_le (s h : ℝ) (v : RegularHilbert H) :
    ‖shiftCharacterAverage s h v‖ ≤ ‖v‖ :=
  ((shiftCharacterAverage s h).le_opNorm v).trans (by
    simpa only [one_mul] using mul_le_mul_of_nonneg_right
      (shiftCharacterAverage_norm_le_one (H := H) s h) (norm_nonneg v))

theorem shiftCharacterAverage_tendsto_identity (s : ℝ) (v : RegularHilbert H) :
    Tendsto (fun h : ℝ => shiftCharacterAverage s h v) (𝓝[≠] 0) (𝓝 v) := by
  have hc := (shiftCharacterFamily (H := H) s).continuous_apply v
  have hd := intervalIntegral.integral_hasDerivAt_right
    (hc.intervalIntegrable 0 0) hc.stronglyMeasurable.stronglyMeasurableAtFilter hc.continuousAt
  have ht := hd.tendsto_slope_zero
  simpa only [zero_add,intervalIntegral.integral_same,sub_zero,
    shiftCharacterFamily,characterPhase,mul_zero,Complex.exp_zero,shift_zero,
    one_smul,one_apply_eq_self,shiftCharacterAverage_apply,Complex.ofReal_zero,
    ContinuousLinearMap.smul_apply] using ht

#print axioms shiftCharacterFamily
#print axioms shiftCharacterAverage
#print axioms shiftCharacterAverage_apply
#print axioms shiftCharacterAverage_norm_le_one
#print axioms shiftCharacterAverage_norm_map_le
#print axioms shiftCharacterAverage_tendsto_identity
end
end TGLV350.Regular
