import TGLExt.V351PerturbedWeightNorm

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section

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
  let v := (scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A)
  have ho : scalarGNSRepresentation P (b*star b) ≤
      scalarGNSRepresentation P (c*star c) := OrderHomClass.mono _ hbc
  have hp := (ContinuousLinearMap.nonneg_iff_isPositive _).mp (sub_nonneg.mpr ho)
  have hv := hp.re_inner_nonneg_left v
  have hn (d : (regularCoreAlgebra P).toStarSubalgebra) :
      ‖scalarGNSRepresentation P (star d) v‖^2 =
      (inner ℂ (scalarGNSRepresentation P (d*star d) v) v).re := by
    have he := ContinuousLinearMap.apply_norm_sq_eq_inner_adjoint_left
      (scalarGNSRepresentation P (star d)) v
    simpa only [map_mul, map_star, ContinuousLinearMap.star_eq_adjoint,
      ContinuousLinearMap.adjoint_adjoint, ContinuousLinearMap.mul_def] using he
  change ‖scalarGNSRepresentation P (star b) v‖^2 ≤
    ‖scalarGNSRepresentation P (star c) v‖^2
  rw [hn b,hn c]
  simpa only [ContinuousLinearMap.sub_apply,inner_sub_left,Complex.sub_re,
    sub_nonneg] using hv

end
end TGLV350.Regular

