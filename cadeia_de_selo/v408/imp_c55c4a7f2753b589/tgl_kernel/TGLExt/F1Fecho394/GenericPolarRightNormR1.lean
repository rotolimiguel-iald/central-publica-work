import TGLExt.F1Fecho394.GenericPolarRightAlgebraR2
/-! Norm and order consequences of a proved polar-right identity.
The order compares pi(b)pi(b)* and pi(c)pi(c)*, never the opposite product. -/
set_option autoImplicit false
set_option maxHeartbeats 600000
noncomputable section
namespace F1Fecho.GenericPolarRightAlgebra
open TGLV350.Regular
variable {𝒜 : Type*} {H : Type} [Ring 𝒜] [Algebra ℂ 𝒜] [StarRing 𝒜] [StarModule ℂ 𝒜]
variable [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (N : Submodule ℂ 𝒜) (Λ : N →ₗ[ℂ] H) (π : 𝒜 →⋆ₐ[ℂ] (H →L[ℂ] H))
variable (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
def rightProduct (b : 𝒜) (hb : ScalarPolarRight N Λ π J b) (a : N) : N :=
  ⟨a.val*b,(hb a).choose⟩
theorem rightProduct_embedding (b : 𝒜) (hb : ScalarPolarRight N Λ π J b) (a : N) :
    Λ (rightProduct N Λ π J b hb a) = J (π (star b) (J.symm (Λ a))) :=
  (hb a).choose_spec
theorem rightProduct_norm (b : 𝒜) (hb : ScalarPolarRight N Λ π J b) (a : N) :
    ‖Λ (rightProduct N Λ π J b hb a)‖ = ‖π (star b) (J.symm (Λ a))‖ := by
  rw [rightProduct_embedding,J.norm_map]
private theorem star_apply_norm_sq_mono (B C : H →L[ℂ] H)
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
theorem rightProduct_squared_norm_mono (b c : 𝒜)
    (hb : ScalarPolarRight N Λ π J b) (hc : ScalarPolarRight N Λ π J c)
    (hbc : π b*star (π b) ≤ π c*star (π c)) (a : N) :
    ‖Λ (rightProduct N Λ π J b hb a)‖^2 ≤ ‖Λ (rightProduct N Λ π J c hc a)‖^2 := by
  rw [rightProduct_norm,rightProduct_norm]
  simpa only [map_star] using star_apply_norm_sq_mono (π b) (π c) hbc (J.symm (Λ a))
end F1Fecho.GenericPolarRightAlgebra
#print axioms F1Fecho.GenericPolarRightAlgebra.rightProduct
#print axioms F1Fecho.GenericPolarRightAlgebra.rightProduct_embedding
#print axioms F1Fecho.GenericPolarRightAlgebra.rightProduct_norm
#print axioms F1Fecho.GenericPolarRightAlgebra.rightProduct_squared_norm_mono
