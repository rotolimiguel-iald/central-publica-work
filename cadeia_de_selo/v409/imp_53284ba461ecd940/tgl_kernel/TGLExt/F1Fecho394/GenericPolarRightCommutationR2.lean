import TGLExt.F1Fecho394.GenericPolarRightNormR1
/-! A proved right action commutes with the left representation on the same
GNS completion. Dense range and left multiplication are explicit obligations. -/
set_option autoImplicit false
set_option maxHeartbeats 700000
noncomputable section
namespace F1Fecho.GenericPolarRightAlgebra
open TGLV350.Regular
variable {𝒜 : Type*} {H : Type} [Ring 𝒜] [Algebra ℂ 𝒜] [StarRing 𝒜] [StarModule ℂ 𝒜]
variable [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (N : Submodule ℂ 𝒜) (Λ : N →ₗ[ℂ] H) (π : 𝒜 →⋆ₐ[ℂ] (H →L[ℂ] H))
variable (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
 theorem commutes_left_of_right_identity
    (hdense : DenseRange Λ)
    (hleft : ∀ c : 𝒜, ∀ a : N, ∃ hc : c*a.val∈N,
      Λ ⟨c*a.val,hc⟩=π c (Λ a))
    (b : 𝒜) (hb : ScalarPolarRight N Λ π J b) (c : 𝒜) :
    Commute (antiunitaryConjugate J (π (star b))) (π c) := by
  let R := antiunitaryConjugate J (π (star b))
  have hR (a : N) : Λ (rightProduct N Λ π J b hb a)=R (Λ a) :=
    rightProduct_embedding N Λ π J b hb a
  have hcore (a : N) : R (π c (Λ a))=π c (R (Λ a)) := by
    obtain ⟨hca,hcae⟩:=hleft c a
    let ca : N:=⟨c*a.val,hca⟩
    let ab:=rightProduct N Λ π J b hb a
    obtain ⟨hcab,hcabe⟩:=hleft c ab
    have he : rightProduct N Λ π J b hb ca=⟨c*ab.val,hcab⟩ :=
      Subtype.ext (mul_assoc c a.val b)
    calc
      R (π c (Λ a))=R (Λ ca) :=congrArg R hcae.symm
      _=Λ (rightProduct N Λ π J b hb ca) :=(hR ca).symm
      _=Λ ⟨c*ab.val,hcab⟩ :=congrArg Λ he
      _=π c (Λ ab) :=hcabe
      _=π c (R (Λ a)) :=congrArg (π c) (hR a)
  ext1 x
  exact hdense.induction_on x
    (isClosed_eq (R.continuous.comp (π c).continuous)
      ((π c).continuous.comp R.continuous)) hcore
end F1Fecho.GenericPolarRightAlgebra
#print axioms F1Fecho.GenericPolarRightAlgebra.commutes_left_of_right_identity
