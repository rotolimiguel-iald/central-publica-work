import TGLExt.V350ScalarCutVacuum

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory
noncomputable section

/-- The same bounded functional is realized by the concrete cutoff vector,
for every operator of the ambient regular Hilbert space and R ≥ 0. -/
theorem scalarCutVacuum_inner_action (P : SiteProfile) (R : ℝ) (hR : 0 ≤ R)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) :
    inner ℂ (scalarCutVacuum P R) (dualOrbitRepresentation A (scalarCutVacuum P R)) =
      dualCutFunctional R (regularVacuum P) A := by
  rw [L2.inner_def,dualCutFunctional_apply,dualWeightCut,
    StrongIntegral.inner_operatorIntegral,
    intervalIntegral.integral_of_le (by linarith : -R ≤ R),← integral_const_mul,
    ← integral_indicator measurableSet_Ioc]
  apply integral_congr_ae
  filter_upwards [scalarCutVacuum_ae P R,
    operatorFieldLift_ae (dualIntegralFamily A) (scalarCutVacuum P R)] with s h1 h2
  change inner ℂ (scalarCutVacuum P R s)
    (operatorFieldLift (dualIntegralFamily A) (scalarCutVacuum P R) s) = _
  rw [h2,h1]
  by_cases hs : s ∈ Set.Ioc (-R) R
  · simp only [Set.indicator_of_mem hs]
    change inner ℂ ((↑(Real.sqrt dualHaarFactor) : ℂ) • regularVacuum P)
      (dualAmbient s A ((↑(Real.sqrt dualHaarFactor) : ℂ) • regularVacuum P)) = _
    rw [map_smul,inner_smul_left,inner_smul_right]
    have hc : (↑(Real.sqrt dualHaarFactor) : ℂ) * (↑(Real.sqrt dualHaarFactor) : ℂ) =
        (dualHaarFactor : ℂ) := by
      rw [← Complex.ofReal_mul,← pow_two,Real.sq_sqrt dualHaarFactor_pos.le]
    rw [Complex.conj_ofReal,← mul_assoc,hc]
    rfl
  · simp only [Set.indicator_of_notMem hs,map_zero,inner_zero_left]

theorem scalarCutLinear_norm_sq (P : SiteProfile) (R : ℝ) (hR : 0 ≤ R)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) :
    ‖dualOrbitRepresentation A (scalarCutVacuum P R)‖ ^ 2 =
      (dualCutFunctional R (regularVacuum P) (star A * A)).re := by
  rw [← scalarCutVacuum_inner_action P R hR]
  rw [map_mul,map_star]
  change _ = (inner ℂ (scalarCutVacuum P R)
    ((dualOrbitRepresentation A).adjoint
      (dualOrbitRepresentation A (scalarCutVacuum P R)))).re
  rw [ContinuousLinearMap.adjoint_inner_right]
  exact (inner_self_eq_norm_sq (𝕜 := ℂ) _).symm

#print axioms scalarCutVacuum_inner_action
#print axioms scalarCutLinear_norm_sq
end
end TGLV350.Regular
