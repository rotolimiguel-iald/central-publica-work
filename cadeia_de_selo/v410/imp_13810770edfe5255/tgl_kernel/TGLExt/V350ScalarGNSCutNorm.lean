import TGLExt.V350ScalarGNSCutMaps
import TGLExt.V350ScalarBoundedCuts

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem measurableCut_norm_sq (S : Set ℝ) (hS : MeasurableSet S) (f : RegularHilbert H) :
    ‖measurableCut S hS f‖ ^ 2 = ∫ x : ℝ in S, ‖f x‖ ^ 2 := by
  rw [← Fourier.L2_integral_norm_sq,← integral_indicator hS]
  apply integral_congr_ae
  filter_upwards [measurableCut_ae S hS f] with x hx
  rw [hx]
  by_cases hxs : x ∈ S <;> simp [hxs]

theorem dualCutFunctional_square_re (R : ℝ) (v : RegularHilbert H)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    (dualCutFunctional R v (star A * A)).re =
      dualHaarFactor * ∫ s in (-R)..R, ‖dualAmbient s A v‖ ^ 2 := by
  simp only [dualCutFunctional_apply,Complex.mul_re,Complex.ofReal_re,
    Complex.ofReal_im,zero_mul,sub_zero]
  rw [dualWeightCut,StrongIntegral.re_inner_operatorIntegral]
  congr 1
  apply intervalIntegral.integral_congr
  intro s _
  change (inner ℂ v (dualAmbient s (star A * A) v)).re = _
  rw [map_mul,map_star]
  change (inner ℂ v ((dualAmbient s A).adjoint (dualAmbient s A v))).re = _
  rw [ContinuousLinearMap.adjoint_inner_right]
  exact inner_self_eq_norm_sq (𝕜 := ℂ) (dualAmbient s A v)

/-- The cutoff contraction realizes exactly the bounded functional already constructed.
The factor is the original Haar factor; no new normalization or state is inserted. -/
theorem scalarGNSCutMap_embedding_norm_sq (P : SiteProfile) (R : ℝ) (hR : 0 ≤ R)
    (A : finiteDualLeftIdeal P) :
    ‖scalarGNSCutMap P R (scalarGNSEmbedding P A)‖ ^ 2 =
      (dualCutFunctional R (regularVacuum P) (star A.val.val * A.val.val)).re := by
  change ‖measurableCut (Set.Ioc (-R) R) measurableSet_Ioc (scalarGNSOrbit P A)‖ ^ 2 = _
  rw [measurableCut_norm_sq,dualCutFunctional_square_re,
    intervalIntegral.integral_of_le (by linarith : -R ≤ R),← integral_const_mul]
  apply integral_congr_ae
  filter_upwards [ae_restrict_of_ae (scalarGNSOrbit_ae P A)] with s hs
  rw [hs,norm_smul,mul_pow,Real.norm_eq_abs,sq_abs,Real.sq_sqrt dualHaarFactor_pos.le]

#print axioms measurableCut_norm_sq
#print axioms dualCutFunctional_square_re
#print axioms scalarGNSCutMap_embedding_norm_sq
end
end TGLV350.Regular
