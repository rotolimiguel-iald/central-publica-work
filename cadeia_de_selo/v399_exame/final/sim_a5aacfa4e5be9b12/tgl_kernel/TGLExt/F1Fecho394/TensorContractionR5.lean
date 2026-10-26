import TGLExt.F1Fecho394.BoundedTensorMapR2
import Mathlib.Analysis.InnerProductSpace.Completion
import Mathlib.Analysis.Normed.Operator.Extend
import Mathlib.Analysis.Normed.Operator.Compact.Basic
/-! A tensor defines a compact operator after conjugating its first slot.
The tensor is completed, while the second factor need not be complete. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open scoped TensorProduct
open UniformSpace
namespace F1Fecho.TensorContraction
variable {E G : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup G] [InnerProductSpace ℂ G]

def evalJ (J : E ≃ₗᵢ⋆[ℂ] E) (a : E) : E →ₗ[ℂ] ℂ where
  toFun x := inner ℂ (J x) a
  map_add' x y := by simp [inner_add_left]
  map_smul' c x := by simp [J.map_smulₛₗ,inner_smul_left]

def raw (J : E ≃ₗᵢ⋆[ℂ] E) : E ⊗[ℂ] G →ₗ[ℂ] E →ₗ[ℂ] G :=
  TensorProduct.lift
  { toFun := fun a =>
      { toFun := fun b => (evalJ J a).smulRight b
        map_add' := by intro x y; ext z; simp
        map_smul' := by intro c x; ext z; simp [smul_smul,mul_comm] }
    map_add' := by intro x y; ext b z; simp [evalJ, inner_add_right, add_smul]
    map_smul' := by intro c x; ext b z; simp [evalJ, inner_smul_right, mul_smul] }

@[simp] theorem raw_tmul (J : E ≃ₗᵢ⋆[ℂ] E) (a : E) (b : G) (x : E) :
    raw J (a ⊗ₜ[ℂ] b) x = inner ℂ (J x) a • b := rfl

theorem norm_raw_le (J : E ≃ₗᵢ⋆[ℂ] E) (z : E ⊗[ℂ] G) (x : E) :
    ‖raw J z x‖ ≤ ‖z‖ * ‖x‖ := by
  classical
  obtain ⟨V,hV,hz⟩ := TensorProduct.exists_finite_submodule_right_of_setFinite
    ({z} : Set (E ⊗[ℂ] G)) (Set.finite_singleton z)
  letI : Module.Finite ℂ V := hV
  obtain ⟨y,hy⟩ := Set.singleton_subset_iff.mp hz
  let e := stdOrthonormalBasis ℂ V
  obtain ⟨v,hv⟩ := TensorProduct.eq_repr_basis_right e.toBasis y
  have hr : z = ∑ i, v i ⊗ₜ[ℂ] ((e i : V) : G) := by
    rw [← hy,← hv]
    simp [Finsupp.sum_fintype]
  have he : Orthonormal ℂ (fun i => ((e i : V) : G)) :=
    e.orthonormal.comp_linearIsometry V.subtypeₗᵢ
  have hm : raw J z x = ∑ i, inner ℂ (J x) (v i) • ((e i : V) : G) := by
    rw [hr]; simp
  have hn : ‖raw J z x‖^2 = ∑ i, ‖inner ℂ (J x) (v i)‖^2 := by
    rw [hm,@InnerProductSpace.norm_sq_eq_re_inner ℂ]
    simp only [sum_inner,inner_sum,inner_smul_left,inner_smul_right,
      orthonormal_iff_ite.mp he]
    simp only [mul_ite,mul_one,mul_zero,Finset.sum_ite_eq',map_sum]
    apply Finset.sum_congr rfl
    intro i hi
    rw [← RCLike.inner_apply,inner_self_eq_norm_sq_to_K,if_pos hi]
    simp only [← RCLike.ofReal_pow,RCLike.ofReal_re]
  apply (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (norm_nonneg _) (norm_nonneg _))).mp
  rw [hn,hr,mul_pow,F1Fecho.BoundedTensor.norm_sum_tmul_sq _ _ he,Finset.sum_mul]
  apply Finset.sum_le_sum
  intro i hi
  have h : ‖inner ℂ (J x) (v i)‖ ≤ ‖v i‖ * ‖x‖ := by
    simpa only [J.norm_map,mul_comm] using norm_inner_le_norm (J x) (v i)
  simpa only [mul_pow] using
    (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (norm_nonneg _) (norm_nonneg _))).mpr h

def algebraic (J : E ≃ₗᵢ⋆[ℂ] E) (z : E ⊗[ℂ] G) : E →L[ℂ] G :=
  (raw J z).mkContinuous ‖z‖ (norm_raw_le J z)

@[simp] theorem algebraic_apply (J : E ≃ₗᵢ⋆[ℂ] E) (z : E ⊗[ℂ] G) (x : E) :
    algebraic J z x = raw J z x := rfl

def algebraicLinear (J : E ≃ₗᵢ⋆[ℂ] E) : E ⊗[ℂ] G →L[ℂ] (E →L[ℂ] G) :=
  ({ toFun := algebraic J
     map_add' := by intro x y; ext a; simp
     map_smul' := by intro c x; ext a; simp } : E ⊗[ℂ] G →ₗ[ℂ] (E →L[ℂ] G)).mkContinuous 1
     (by intro z; simpa using (algebraic J z).opNorm_le_bound (norm_nonneg z) (norm_raw_le J z))

def algebraicCompleted (J : E ≃ₗᵢ⋆[ℂ] E) : E ⊗[ℂ] G →L[ℂ] (E →L[ℂ] Completion G) :=
  (ContinuousLinearMap.compL ℂ E G (Completion G) Completion.toComplL).comp
    (algebraicLinear J)

def contraction (J : E ≃ₗᵢ⋆[ℂ] E) : Completion (E ⊗[ℂ] G) →L[ℂ] (E →L[ℂ] Completion G) :=
  (algebraicCompleted J).extend Completion.toComplL

@[simp] theorem contraction_coe (J : E ≃ₗᵢ⋆[ℂ] E) (z : E ⊗[ℂ] G) :
    contraction J (z : Completion (E ⊗[ℂ] G)) = algebraicCompleted J z := by
  exact ContinuousLinearMap.extend_eq _ Completion.denseRange_coe (Completion.isUniformInducing_coe _) z

@[simp] theorem contraction_tmul (J : E ≃ₗᵢ⋆[ℂ] E) (a : E) (b : G) (x : E) :
    contraction J ((a ⊗ₜ[ℂ] b : E ⊗[ℂ] G) : Completion (E ⊗[ℂ] G)) x =
      inner ℂ (J x) a • (b : Completion G) := by
  rw [contraction_coe]
  change ((inner ℂ (J x) a • b : G) : Completion G) = _
  exact Completion.coe_smul _ _

theorem contraction_compact (J : E ≃ₗᵢ⋆[ℂ] E) (z : Completion (E ⊗[ℂ] G)) :
    IsCompactOperator (contraction J z) := by
  have hc : IsClosed {z : Completion (E ⊗[ℂ] G) | IsCompactOperator (contraction J z)} :=
    isClosed_setOf_isCompactOperator.preimage (contraction J).continuous
  refine Completion.induction_on z hc ?_
  intro t
  induction t using TensorProduct.induction_on with
  | zero =>
    simp only [Completion.coe_zero,map_zero]
    change IsCompactOperator (fun _ : E => (0 : Completion G))
    exact isCompactOperator_zero
  | tmul a b =>
    let e : E →L[ℂ] ℂ := (evalJ J a).mkContinuous ‖a‖ (by
      intro x; simpa only [evalJ,LinearMap.coe_mk,AddHom.coe_mk,J.norm_map,mul_comm]
        using norm_inner_le_norm (J x) a)
    have h : contraction J ((a ⊗ₜ[ℂ] b : E ⊗[ℂ] G) : Completion (E ⊗[ℂ] G)) =
        (ContinuousLinearMap.smulRight (ContinuousLinearMap.id ℂ ℂ) (b : Completion G)).comp e := by
      ext x; rw [contraction_tmul]; rfl
    rw [h]
    exact (isCompactOperator_of_locallyCompactSpace_dom e).clm_comp
      (ContinuousLinearMap.smulRight (ContinuousLinearMap.id ℂ ℂ) (b : Completion G))
  | add a b ha hb =>
    simp only [Completion.coe_add,map_add]
    change IsCompactOperator (fun x => contraction J (a : Completion (E ⊗[ℂ] G)) x + contraction J (b : Completion (E ⊗[ℂ] G)) x)
    exact ha.add hb

end F1Fecho.TensorContraction
#print axioms F1Fecho.TensorContraction.norm_raw_le
#print axioms F1Fecho.TensorContraction.contraction_tmul
#print axioms F1Fecho.TensorContraction.contraction_compact
