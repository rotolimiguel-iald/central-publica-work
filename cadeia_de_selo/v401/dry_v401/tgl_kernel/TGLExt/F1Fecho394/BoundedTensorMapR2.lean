import Mathlib.Analysis.InnerProductSpace.TensorProduct
import Mathlib.LinearAlgebra.TensorProduct.Basis
import Mathlib.Analysis.Normed.Operator.ContinuousLinearMap
/-! A bounded tensor map on the existing algebraic Hilbert tensor product.
The operator norm estimate is proved from a finite-dimensional second factor
and an orthonormal expansion. No tensor continuity premise is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open scoped TensorProduct
open Module
namespace F1Fecho.BoundedTensor

variable {E F G H : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]
  [NormedAddCommGroup G] [InnerProductSpace ℂ G]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H]

theorem norm_sum_tmul_sq {I : Type*} [Fintype I]
    (v : I → E) (e : I → F) (he : Orthonormal ℂ e) :
    ‖∑ i, v i ⊗ₜ[ℂ] e i‖^2 = ∑ i, ‖v i‖^2 := by
  classical
  rw [@InnerProductSpace.norm_sq_eq_re_inner ℂ]
  simp only [sum_inner,inner_sum,TensorProduct.inner_tmul,orthonormal_iff_ite.mp he]
  simp [inner_self_eq_norm_sq_to_K,← Complex.ofReal_pow]

theorem norm_map_first_le (A : E →L[ℂ] G) (x : E ⊗[ℂ] F) :
    ‖TensorProduct.map A.toLinearMap (LinearMap.id : F →ₗ[ℂ] F) x‖ ≤ ‖A‖ * ‖x‖ := by
  classical
  obtain ⟨V,hV,hx⟩ := TensorProduct.exists_finite_submodule_right_of_setFinite
    ({x} : Set (E ⊗[ℂ] F)) (Set.finite_singleton x)
  letI : Module.Finite ℂ V := hV
  obtain ⟨y,hy⟩ := Set.singleton_subset_iff.mp hx
  let e := stdOrthonormalBasis ℂ V
  obtain ⟨v,hv⟩ := TensorProduct.eq_repr_basis_right e.toBasis y
  have hr : x = ∑ i, v i ⊗ₜ[ℂ] ((e i : V) : F) := by
    rw [← hy,← hv]
    simp [Finsupp.sum_fintype]
  have he : Orthonormal ℂ (fun i => ((e i : V) : F)) :=
    e.orthonormal.comp_linearIsometry V.subtypeₗᵢ
  have hm : TensorProduct.map A.toLinearMap (LinearMap.id : F →ₗ[ℂ] F) x =
      ∑ i, A (v i) ⊗ₜ[ℂ] ((e i : V) : F) := by
    rw [hr]
    simp
  apply (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (norm_nonneg _) (norm_nonneg _))).mp
  rw [hm,norm_sum_tmul_sq _ _ he,hr,mul_pow,norm_sum_tmul_sq _ _ he,Finset.mul_sum]
  apply Finset.sum_le_sum
  intro i hi
  have h := A.le_opNorm (v i)
  simpa only [mul_pow] using
    (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (norm_nonneg _) (norm_nonneg _))).mpr h

theorem norm_map_second_le (B : F →L[ℂ] H) (x : E ⊗[ℂ] F) :
    ‖TensorProduct.map (LinearMap.id : E →ₗ[ℂ] E) B.toLinearMap x‖ ≤ ‖B‖ * ‖x‖ := by
  have he : TensorProduct.comm ℂ E H
      (TensorProduct.map (LinearMap.id : E →ₗ[ℂ] E) B.toLinearMap x) =
      TensorProduct.map B.toLinearMap (LinearMap.id : E →ₗ[ℂ] E) (TensorProduct.comm ℂ E F x) := by
    induction x using TensorProduct.induction_on with
    | zero => simp
    | tmul x y => simp
    | add x y hx hy => simp only [map_add,hx,hy]
  have h := norm_map_first_le B (TensorProduct.comm ℂ E F x)
  rw [← he,TensorProduct.norm_comm,TensorProduct.norm_comm] at h
  exact h

theorem norm_map_le (A : E →L[ℂ] G) (B : F →L[ℂ] H) (x : E ⊗[ℂ] F) :
    ‖TensorProduct.map A.toLinearMap B.toLinearMap x‖ ≤ (‖A‖ * ‖B‖) * ‖x‖ := by
  have he : TensorProduct.map A.toLinearMap B.toLinearMap x =
      TensorProduct.map A.toLinearMap (LinearMap.id : H →ₗ[ℂ] H)
        (TensorProduct.map (LinearMap.id : E →ₗ[ℂ] E) B.toLinearMap x) := by
    induction x using TensorProduct.induction_on with
    | zero => simp
    | tmul x y => simp
    | add x y hx hy => simp only [map_add,hx,hy]
  rw [he]
  calc
    _ ≤ ‖A‖ * ‖TensorProduct.map (LinearMap.id : E →ₗ[ℂ] E) B.toLinearMap x‖ :=
      norm_map_first_le A _
    _ ≤ ‖A‖ * (‖B‖ * ‖x‖) := mul_le_mul_of_nonneg_left (norm_map_second_le B x) (norm_nonneg _)
    _ = _ := by ring

def mapCLM (A : E →L[ℂ] G) (B : F →L[ℂ] H) : E ⊗[ℂ] F →L[ℂ] G ⊗[ℂ] H :=
  (TensorProduct.map A.toLinearMap B.toLinearMap).mkContinuous (‖A‖*‖B‖) (norm_map_le A B)

theorem mapCLM_tmul (A : E →L[ℂ] G) (B : F →L[ℂ] H) (x : E) (y : F) :
    mapCLM A B (x ⊗ₜ[ℂ] y) = A x ⊗ₜ[ℂ] B y := rfl

theorem mapCLM_norm_le (A : E →L[ℂ] G) (B : F →L[ℂ] H) :
    ‖mapCLM A B‖ ≤ ‖A‖*‖B‖ :=
  (mapCLM A B).opNorm_le_bound (mul_nonneg (norm_nonneg _) (norm_nonneg _)) (norm_map_le A B)

end F1Fecho.BoundedTensor
#print axioms F1Fecho.BoundedTensor.norm_sum_tmul_sq
#print axioms F1Fecho.BoundedTensor.norm_map_first_le
#print axioms F1Fecho.BoundedTensor.norm_map_le
#print axioms F1Fecho.BoundedTensor.mapCLM_norm_le
