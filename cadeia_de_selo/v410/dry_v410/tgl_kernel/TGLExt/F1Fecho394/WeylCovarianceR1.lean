import TGLExt.F1Fecho394.WeylOperatorsGenericR2
/-! Functorial covariance of the constructed displacement operators. The action
on the total exponential family is explicit; covariance is derived from it. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.WeylConstruction
open F1Fecho.WeylCoefficients F1Fecho.GramExtension
variable {H F : Type*}
  [NormedAddCommGroup H] [InnerProductSpace ℂ H]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]
variable (v : H → F)
  (hkernel : ∀ g h, inner ℂ (v g) (v h) = Complex.exp (inner ℂ g h))
  (htotal : Total (𝕜 := ℂ) v)

theorem inverse_on_family (u : H ≃ₗᵢ[ℂ] H) (V : F ≃ₗᵢ[ℂ] F)
    (hV : ∀ g, V (v g) = v (u g)) (g : H) : V.symm (v g) = v (u.symm g) := by
  apply V.injective
  rw [LinearIsometryEquiv.apply_symm_apply, hV, LinearIsometryEquiv.apply_symm_apply]

theorem W_covariance (u : H ≃ₗᵢ[ℂ] H) (V : F ≃ₗᵢ[ℂ] F)
    (hV : ∀ g, V (v g) = v (u g)) (f : H) :
    V.conjStarAlgEquiv (W v hkernel htotal f) = W v hkernel htotal (u f) := by
  apply clm_ext_total v htotal
  intro g
  rw [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply, inverse_on_family v u V hV,
    W_apply, map_smul, hV, W_apply, map_add, LinearIsometryEquiv.apply_symm_apply]
  have ha : amplitude f (u.symm g) = amplitude (u f) g := by
    rw [← amplitude_isometry u f (u.symm g), LinearIsometryEquiv.apply_symm_apply]
  rw [ha]

end F1Fecho.WeylConstruction
#print axioms F1Fecho.WeylConstruction.inverse_on_family
#print axioms F1Fecho.WeylConstruction.W_covariance
