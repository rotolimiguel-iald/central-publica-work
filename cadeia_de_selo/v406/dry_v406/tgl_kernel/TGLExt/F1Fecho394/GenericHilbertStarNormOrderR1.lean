import TGLExt.V350AntiunitaryPositiveConjugation
set_option autoImplicit false
noncomputable section
namespace F1Fecho.GenericHilbertStarNormOrder
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem star_apply_norm_sq_mono (B C : H →L[ℂ] H)
    (hbc : B*star B ≤ C*star C) (v : H) : ‖star B v‖^2 ≤ ‖star C v‖^2 := by
  have hp := (ContinuousLinearMap.nonneg_iff_isPositive _).mp (sub_nonneg.mpr hbc)
  have hv := hp.re_inner_nonneg_left v
  have hn (D : H →L[ℂ] H) : ‖star D v‖^2 = (inner ℂ ((D*star D) v) v).re := by
    have he := ContinuousLinearMap.apply_norm_sq_eq_inner_adjoint_left (𝕜 := ℂ) (star D) v
    simpa only [RCLike.re_eq_complex_re,ContinuousLinearMap.star_eq_adjoint,
      ContinuousLinearMap.adjoint_adjoint,ContinuousLinearMap.mul_def] using he
  rw [hn B,hn C]
  simpa only [RCLike.re_eq_complex_re,ContinuousLinearMap.sub_apply,inner_sub_left,
    Complex.sub_re,sub_nonneg] using hv

end F1Fecho.GenericHilbertStarNormOrder
#print axioms F1Fecho.GenericHilbertStarNormOrder.star_apply_norm_sq_mono
