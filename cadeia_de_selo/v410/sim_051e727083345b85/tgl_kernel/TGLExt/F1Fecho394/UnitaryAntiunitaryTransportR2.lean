import TGLExt.V350AntiunitaryPositiveConjugation
/-! Transport of an involutive antiunitary between arbitrary Hilbert spaces. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.UnitaryAntiunitaryTransport
variable {H E:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E]
def conjugate (U:H≃ₗᵢ[ℂ]E) (J:H≃ₛₗᵢ[starRingEnd ℂ]H) : E≃ₛₗᵢ[starRingEnd ℂ]E :=
  U.symm.trans (J.trans U)
theorem on_unitary (U:H≃ₗᵢ[ℂ]E) (J:H≃ₛₗᵢ[starRingEnd ℂ]H) (x:H) :
    conjugate U J (U x)=U (J x) := by
  change U (J (U.symm (U x)))=U (J x)
  rw [LinearIsometryEquiv.symm_apply_apply]
theorem involutive (U:H≃ₗᵢ[ℂ]E) (J:H≃ₛₗᵢ[starRingEnd ℂ]H)
    (hJ:Function.Involutive J) : Function.Involutive (conjugate U J) := by
  intro x
  change U (J (U.symm (U (J (U.symm x)))))=x
  rw [LinearIsometryEquiv.symm_apply_apply,hJ,LinearIsometryEquiv.apply_symm_apply]
end F1Fecho.UnitaryAntiunitaryTransport
#print axioms F1Fecho.UnitaryAntiunitaryTransport.on_unitary
#print axioms F1Fecho.UnitaryAntiunitaryTransport.involutive
