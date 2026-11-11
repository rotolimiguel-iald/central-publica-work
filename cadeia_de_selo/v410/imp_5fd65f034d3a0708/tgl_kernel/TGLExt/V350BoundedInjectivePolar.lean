import TGLExt.V350DenseLinearPolarExtension
import TGLExt.V350DualFormRepresentation
import TGLExt.V350ResolventGraphTransport

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
noncomputable section
variable {H K : Type}
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]

def boundedMapModulus (C : H →L[ℂ] K) : H →L[ℂ] H := CFC.sqrt (C.adjoint.comp C)

theorem boundedMapGram_nonneg (C : H →L[ℂ] K) : 0 ≤ C.adjoint.comp C :=
  (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
    (ContinuousLinearMap.isPositive_adjoint_comp_self C)

theorem boundedMapModulus_norm (C : H →L[ℂ] K) (x : H) :
    ‖boundedMapModulus C x‖ = ‖C x‖ := by
  have h := boundedPositiveSquareRoot_energy (C.adjoint.comp C) (boundedMapGram_nonneg C) x
  change ‖boundedMapModulus C x‖ ^ 2 = (inner ℂ (C.adjoint (C x)) x).re at h
  rw [C.adjoint_inner_left] at h
  have hself : (inner ℂ (C x) (C x)).re = ‖C x‖ ^ 2 := inner_self_eq_norm_sq (𝕜 := ℂ) _
  rw [hself] at h
  nlinarith only [h,norm_nonneg (boundedMapModulus C x),norm_nonneg (C x)]

theorem boundedMapModulus_injective (C : H →L[ℂ] K) (hi : Function.Injective C) :
    Function.Injective (boundedMapModulus C) :=
  positive_sqrt_injective _ (boundedMapGram_nonneg C) (C.adjoint_comp_self_injective_iff.mpr hi)

theorem boundedMapModulus_denseRange (C : H →L[ℂ] K) (hi : Function.Injective C) :
    DenseRange (boundedMapModulus C) :=
  ChatgptAudit.Continuous049.bounded_graph_domain_dense (boundedMapModulus C) 0
    (boundedMapModulus_injective C hi) (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg _))

/-- Injectivity and dense range yield a unitary polar factor even when C
has no bounded inverse. It is not the modular antiunitary J. -/
def boundedInjectivePolar (C : H →L[ℂ] K) (hi : Function.Injective C)
    (hd : DenseRange C) : H ≃ₗᵢ[ℂ] K :=
  denseLinearEquiv C.toLinearMap (boundedMapModulus C).toLinearMap
    (boundedMapModulus_denseRange C hi) (fun x => (boundedMapModulus_norm C x).symm) hd

theorem boundedInjectivePolar_modulus (C : H →L[ℂ] K) (hi : Function.Injective C)
    (hd : DenseRange C) (x : H) :
    boundedInjectivePolar C hi hd (boundedMapModulus C x) = C x :=
  denseLinearEquiv_apply _ _ _ _ _ x

theorem boundedMapGram_commutes_of_intertwines (C : H →L[ℂ] K)
    (A : H →L[ℂ] H) (B : K →L[ℂ] K)
    (h : C.comp A = B.comp C) (hs : C.comp (star A) = (star B).comp C) :
    Commute (C.adjoint.comp C) A := by
  have ha : A.comp C.adjoint = C.adjoint.comp B := by
    have he := congrArg ContinuousLinearMap.adjoint hs
    simpa only [ContinuousLinearMap.adjoint_comp,ContinuousLinearMap.star_eq_adjoint,
      ContinuousLinearMap.adjoint_adjoint] using he
  change (C.adjoint.comp C).comp A = A.comp (C.adjoint.comp C)
  rw [ContinuousLinearMap.comp_assoc,h,← ContinuousLinearMap.comp_assoc,← ha,
    ContinuousLinearMap.comp_assoc]

/-- A *-intertwiner transports its polar unitary. Both A and A* are required. -/
theorem boundedInjectivePolar_intertwines (C : H →L[ℂ] K) (hi : Function.Injective C)
    (hd : DenseRange C) (A : H →L[ℂ] H) (B : K →L[ℂ] K)
    (h : C.comp A = B.comp C) (hs : C.comp (star A) = (star B).comp C)
    (x : H) : boundedInjectivePolar C hi hd (A x) = B (boundedInjectivePolar C hi hd x) := by
  have hc := positive_sqrt_commutes_of_commute _ A
    (boundedMapGram_commutes_of_intertwines C A B h hs)
  refine (boundedMapModulus_denseRange C hi).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) x
  rintro _ ⟨y,rfl⟩
  have he : A (boundedMapModulus C y) = boundedMapModulus C (A y) :=
    (congrArg (fun T : H →L[ℂ] H => T y) hc.eq).symm
  rw [he,boundedInjectivePolar_modulus,boundedInjectivePolar_modulus]
  exact congrArg (fun T : H →L[ℂ] K => T y) h

#print axioms boundedMapModulus
#print axioms boundedMapGram_nonneg
#print axioms boundedMapModulus_norm
#print axioms boundedMapModulus_injective
#print axioms boundedMapModulus_denseRange
#print axioms boundedInjectivePolar
#print axioms boundedInjectivePolar_modulus
#print axioms boundedMapGram_commutes_of_intertwines
#print axioms boundedInjectivePolar_intertwines
end
end TGLV350.Regular
