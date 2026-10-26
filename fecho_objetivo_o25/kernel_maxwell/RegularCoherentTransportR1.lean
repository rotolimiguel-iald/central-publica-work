import RegularMaxwellFockDomainR5
import FiniteCoherentKernelR3

/-! Transport of the UNIQUE finite coherent coefficients under existing
one-particle unitaries preserving the actual regular profile class. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open F1Fecho.Exponential F1Fecho.CoherentKernel

 def regularLabelEquiv (u : H1 ≃ₗᵢ[ℂ] H1)
    (hu : ∀h,StrongRegularProfile h→StrongRegularProfile (u h))
    (hv : ∀h,StrongRegularProfile h→StrongRegularProfile (u.symm h)) : RegularLabel ≃ RegularLabel where
  toFun h:=⟨u h.val,hu h.val h.property⟩
  invFun h:=⟨u.symm h.val,hv h.val h.property⟩
  left_inv h:=Subtype.ext (u.symm_apply_apply h.val)
  right_inv h:=Subtype.ext (u.apply_symm_apply h.val)

 def regularGamma (u : H1 ≃ₗᵢ[ℂ] H1)
    (hu : ∀h,StrongRegularProfile h→StrongRegularProfile (u h))
    (ψ : regularFockDomain) : regularFockDomain :=
  ⟨gamma u ψ.val,gamma_mem_regularFockDomain u hu ψ.val ψ.property⟩

 theorem regularSynthesis_equivMapDomain (u : H1 ≃ₗᵢ[ℂ] H1)
    (hu : ∀h,StrongRegularProfile h→StrongRegularProfile (u h))
    (hv : ∀h,StrongRegularProfile h→StrongRegularProfile (u.symm h))
    (c : RegularLabel→₀ℂ) :
    regularSynthesis (Finsupp.equivMapDomain (regularLabelEquiv u hu hv) c)=
      gamma u (regularSynthesis c) := by
  simp only [regularSynthesis,Finsupp.linearCombination_apply,Finsupp.sum_equivMapDomain]
  simp only [Finsupp.sum,map_sum,map_smul,gamma_exponential,regularLabelEquiv,Equiv.coe_fn_mk]

 theorem regularCoefficients_gamma (u : H1 ≃ₗᵢ[ℂ] H1)
    (hu : ∀h,StrongRegularProfile h→StrongRegularProfile (u h))
    (hv : ∀h,StrongRegularProfile h→StrongRegularProfile (u.symm h))
    (ψ : regularFockDomain) :
    regularCoefficients (regularGamma u hu ψ)=
      Finsupp.equivMapDomain (regularLabelEquiv u hu hv) (regularCoefficients ψ) := by
  apply regularSynthesis_injective
  rw [regularCoefficients_spec,regularSynthesis_equivMapDomain,regularCoefficients_spec]
  rfl

 theorem finiteKernel_reindex {ι κ : Type*} (e : ι ≃ κ) (M : κ→κ→ℂ) (c d : ι→₀ℂ) :
    finiteKernel M (Finsupp.equivMapDomain e c) (Finsupp.equivMapDomain e d)=
      finiteKernel (fun i j=>M (e i) (e j)) c d := by
  simp only [finiteKernel,Finsupp.sum_equivMapDomain]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.regularSynthesis_equivMapDomain
#print axioms F1Fecho.MaxwellGlobal.regularCoefficients_gamma
#print axioms F1Fecho.MaxwellGlobal.finiteKernel_reindex
