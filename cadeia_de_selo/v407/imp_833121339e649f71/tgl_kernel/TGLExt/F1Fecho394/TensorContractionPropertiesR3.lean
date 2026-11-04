import TGLExt.F1Fecho394.TensorContractionR5
import TGLExt.F1Fecho394.BosonicTwoParticle
import Mathlib.Analysis.InnerProductSpace.Adjoint
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open scoped TensorProduct InnerProductSpace
open UniformSpace
namespace F1Fecho.TensorContraction
open F1Rede.BosonicTwoParticle
variable {E G : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup G] [InnerProductSpace ℂ G]

theorem inner_contraction (J : E ≃ₗᵢ⋆[ℂ] E)
    (z : Completion (E ⊗[ℂ] G)) (x : E) (y : G) :
    inner ℂ (y : Completion G) (contraction J z x) =
      inner ℂ ((J x ⊗ₜ[ℂ] y : E ⊗[ℂ] G) : Completion (E ⊗[ℂ] G)) z := by
  refine Completion.induction_on z (isClosed_eq
    (continuous_const.inner ((ContinuousLinearMap.apply ℂ (Completion G) x).continuous.comp
      (contraction J).continuous)) (continuous_const.inner continuous_id)) ?_
  intro t
  induction t using TensorProduct.induction_on with
  | zero => simp only [Completion.coe_zero,map_zero,ContinuousLinearMap.zero_apply,inner_zero_left,inner_zero_right]
  | tmul a b => simp only [contraction_tmul,inner_smul_right,Completion.inner_coe,
      TensorProduct.inner_tmul,mul_comm]
  | add a b ha hb => simpa only [Completion.coe_add,map_add,ContinuousLinearMap.add_apply,
      inner_add_right,ha,hb]

theorem contraction_eq_zero (J : E ≃ₗᵢ⋆[ℂ] E) (z : Completion (E ⊗[ℂ] G))
    (hzero : contraction J z = 0) : z = 0 := by
  have hall (w : Completion (E ⊗[ℂ] G)) : inner ℂ w z = 0 := by
    refine Completion.induction_on w (isClosed_eq (continuous_id.inner continuous_const) continuous_const) ?_
    intro t
    induction t using TensorProduct.induction_on with
    | zero => simp only [Completion.coe_zero,map_zero,ContinuousLinearMap.zero_apply,inner_zero_left,inner_zero_right]
    | tmul a b =>
      obtain ⟨x,rfl⟩ := J.surjective a
      rw [← inner_contraction J z x b,hzero]
      simp
    | add a b ha hb => simpa only [Completion.coe_add,inner_add_left,ha,hb,add_zero]
  exact inner_self_eq_zero.mp (hall z)

theorem contraction_injective (J : E ≃ₗᵢ⋆[ℂ] E) : Function.Injective (contraction (G := G) J) := by
  intro z w h
  apply sub_eq_zero.mp
  apply contraction_eq_zero J
  rw [map_sub,h,sub_self]

def conjugate (J : E ≃ₗᵢ⋆[ℂ] E) (u : E ≃ₗᵢ[ℂ] E) : E ≃ₗᵢ[ℂ] E :=
  (J.trans u).trans J.symm

@[simp] theorem J_conjugate (J : E ≃ₗᵢ⋆[ℂ] E) (u : E ≃ₗᵢ[ℂ] E) (x : E) :
    J (conjugate J u x) = u (J x) := by simp [conjugate]

def tensorAction (u : E ≃ₗᵢ[ℂ] E) (v : G ≃ₗᵢ[ℂ] G) :
    Completion (E ⊗[ℂ] G) ≃ₗᵢ[ℂ] Completion (E ⊗[ℂ] G) :=
  completionEquiv (TensorProduct.congrIsometry u v)

theorem contraction_covariance (J : E ≃ₗᵢ⋆[ℂ] E)
    (u : E ≃ₗᵢ[ℂ] E) (v : G ≃ₗᵢ[ℂ] G)
    (z : Completion (E ⊗[ℂ] G)) (x : E) :
    contraction J (tensorAction u v z) (conjugate J u x) =
      completionEquiv v (contraction J z x) := by
  refine Completion.induction_on z (isClosed_eq
    ((ContinuousLinearMap.apply ℂ (Completion G) (conjugate J u x)).continuous.comp
      ((contraction J).continuous.comp (tensorAction u v).continuous))
    ((completionEquiv v).continuous.comp
      ((ContinuousLinearMap.apply ℂ (Completion G) x).continuous.comp (contraction J).continuous))) ?_
  intro t
  induction t using TensorProduct.induction_on with
  | zero => simp only [Completion.coe_zero,map_zero,ContinuousLinearMap.zero_apply,inner_zero_left,inner_zero_right]
  | tmul a b =>
    rw [tensorAction,completionEquiv_coe]
    change contraction J ((u a ⊗ₜ[ℂ] v b : E ⊗[ℂ] G) : Completion (E ⊗[ℂ] G)) _ = _
    rw [contraction_tmul,contraction_tmul,J_conjugate,u.inner_map_map]
    simp
  | add a b ha hb =>
    simpa only [Completion.coe_add,map_add,ContinuousLinearMap.add_apply,ha,hb]

theorem contraction_intertwines (J : E ≃ₗᵢ⋆[ℂ] E)
    (u : E ≃ₗᵢ[ℂ] E) (v : G ≃ₗᵢ[ℂ] G)
    (z : Completion (E ⊗[ℂ] G)) (hz : tensorAction u v z = z) (x : E) :
    contraction J z (conjugate J u x) = completionEquiv v (contraction J z x) := by
  simpa only [hz] using contraction_covariance J u v z x

section Complete
variable [CompleteSpace E]
def reduced (J : E ≃ₗᵢ⋆[ℂ] E) (z : Completion (E ⊗[ℂ] G)) : E →L[ℂ] E :=
  (contraction J z).adjoint.comp (contraction J z)

theorem reduced_compact (J : E ≃ₗᵢ⋆[ℂ] E) (z : Completion (E ⊗[ℂ] G)) :
    IsCompactOperator (reduced J z) :=
  (contraction_compact J z).clm_comp (contraction J z).adjoint

theorem reduced_symmetric (J : E ≃ₗᵢ⋆[ℂ] E) (z : Completion (E ⊗[ℂ] G)) :
    (reduced J z).IsSymmetric := by
  intro x y
  change inner ℂ ((contraction J z).adjoint (contraction J z x)) y =
    inner ℂ x ((contraction J z).adjoint (contraction J z y))
  rw [ContinuousLinearMap.adjoint_inner_left,ContinuousLinearMap.adjoint_inner_right]

theorem reduced_commutes (J : E ≃ₗᵢ⋆[ℂ] E)
    (u : E ≃ₗᵢ[ℂ] E) (v : G ≃ₗᵢ[ℂ] G)
    (z : Completion (E ⊗[ℂ] G)) (hz : tensorAction u v z = z) :
    Commute (reduced J z) (conjugate J u).toContinuousLinearEquiv.toContinuousLinearMap := by
  apply ContinuousLinearMap.ext
  intro x
  apply ext_inner_right ℂ
  intro y
  obtain ⟨w,rfl⟩ := (conjugate J u).surjective y
  change inner ℂ ((reduced J z) (conjugate J u x)) (conjugate J u w) =
    inner ℂ (conjugate J u ((reduced J z) x)) (conjugate J u w)
  rw [(conjugate J u).inner_map_map]
  simp only [reduced,ContinuousLinearMap.comp_apply,ContinuousLinearMap.adjoint_inner_left]
  rw [contraction_intertwines J u v z hz x,contraction_intertwines J u v z hz w,
    (completionEquiv v).inner_map_map]

theorem eq_zero_of_reduced_eq_zero (J : E ≃ₗᵢ⋆[ℂ] E)
    (z : Completion (E ⊗[ℂ] G)) (hz : reduced J z = 0) : z = 0 := by
  apply contraction_injective J
  rw [map_zero]
  ext x
  apply (inner_self_eq_zero (𝕜 := ℂ)).mp
  have h := congrArg (fun B : E →L[ℂ] E => inner ℂ (B x) x) hz
  simpa only [reduced,ContinuousLinearMap.comp_apply,ContinuousLinearMap.adjoint_inner_left,
    ContinuousLinearMap.zero_apply,inner_zero_left] using h
end Complete
end F1Fecho.TensorContraction
#print axioms F1Fecho.TensorContraction.contraction_injective
#print axioms F1Fecho.TensorContraction.contraction_covariance
#print axioms F1Fecho.TensorContraction.reduced_commutes
#print axioms F1Fecho.TensorContraction.eq_zero_of_reduced_eq_zero
