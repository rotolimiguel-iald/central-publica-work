import TGLExt.V351PerturbedWeightNorm
import TGLExt.V350ScalarGNSNormality

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section

private theorem star_apply_norm_sq_mono {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (B C : H →L[ℂ] H) (hbc : B*star B ≤ C*star C) (v : H) :
    ‖star B v‖^2 ≤ ‖star C v‖^2 := by
  have hp := (ContinuousLinearMap.nonneg_iff_isPositive _).mp (sub_nonneg.mpr hbc)
  have hv := hp.re_inner_nonneg_left v
  have hn (D : H →L[ℂ] H) :
      ‖star D v‖^2 = (inner ℂ ((D*star D) v) v).re := by
    have he := ContinuousLinearMap.apply_norm_sq_eq_inner_adjoint_left
      (𝕜 := ℂ) (star D) v
    simpa only [RCLike.re_eq_complex_re,ContinuousLinearMap.star_eq_adjoint,
      ContinuousLinearMap.adjoint_adjoint,ContinuousLinearMap.mul_def] using he
  rw [hn B,hn C]
  simpa only [RCLike.re_eq_complex_re,sub_apply,inner_sub_left,Complex.sub_re,
    sub_nonneg] using hv

/-- Order of right perturbations on the original square-finite domain. The
hypothesis compares b b* and c c*, not b* b and c* c. -/
theorem scalarWeight_right_perturbed_mono (P : SiteProfile)
    (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (hc : c ∈ scalarPolarRightAlgebra P)
    (hbc : b * star b ≤ c * star c) (A : scalarWeightLeftIdeal P) :
    dualQuadraticIntegral (star b.val * (star A.val.val*A.val.val) * b.val)
      (regularVacuum P) ≤
    dualQuadraticIntegral (star c.val * (star A.val.val*A.val.val) * c.val)
      (regularVacuum P) := by
  rw [scalarWeight_right_perturbed_norm P b hb A,
    scalarWeight_right_perturbed_norm P c hc A]
  apply ENNReal.ofReal_le_ofReal
  have ho := scalarGNSRepresentation_monotone P hbc
  have hp : scalarGNSRepresentation P b * star (scalarGNSRepresentation P b) ≤
      scalarGNSRepresentation P c * star (scalarGNSRepresentation P c) := by
    simpa only [map_mul,map_star] using ho
  have hn := star_apply_norm_sq_mono (scalarGNSRepresentation P b)
    (scalarGNSRepresentation P c) hp
    ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A))
  simpa only [map_star] using hn

end
end TGLV350.Regular
