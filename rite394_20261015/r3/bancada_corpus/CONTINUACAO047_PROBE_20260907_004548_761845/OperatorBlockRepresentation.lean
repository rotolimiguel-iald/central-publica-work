import Mathlib.Analysis.CStarAlgebra.CompletelyPositiveMap
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.InnerProductSpace.StarOrder

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace ChatgptAudit.Expectation047

open scoped ComplexOrder

noncomputable section

variable (H : Type*) [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- Finite operator matrices act on the Hilbert direct sum by row times column. -/
def operatorBlockCLM (k : ℕ) (M : CStarMatrix (Fin k) (Fin k) (H →L[ℂ] H)) :
    (PiLp 2 (fun _ : Fin k => H)) →L[ℂ] (PiLp 2 (fun _ : Fin k => H)) :=
  (PiLp.continuousLinearEquiv 2 ℂ (fun _ : Fin k => H)).symm.toContinuousLinearMap.comp
    (ContinuousLinearMap.pi (fun i =>
      ∑ j, (M i j).comp (PiLp.proj 2 (fun _ : Fin k => H) j)))

theorem operator_block_apply (k : ℕ)
    (M : CStarMatrix (Fin k) (Fin k) (H →L[ℂ] H))
    (v : PiLp 2 (fun _ : Fin k => H)) (i : Fin k) :
    operatorBlockCLM H k M v i = ∑ j, M i j (v j) := by
  simp [operatorBlockCLM]

/-- Recover one entry of an arbitrary operator on the finite Hilbert direct sum. -/
def operatorBlockEntry (k : ℕ)
    (T : (PiLp 2 (fun _ : Fin k => H)) →L[ℂ] (PiLp 2 (fun _ : Fin k => H)))
    (i j : Fin k) : H →L[ℂ] H :=
  (PiLp.proj 2 (fun _ : Fin k => H) i).comp
    (T.comp ((PiLp.continuousLinearEquiv 2 ℂ (fun _ : Fin k => H)).symm.toContinuousLinearMap.comp
      (ContinuousLinearMap.single ℂ (fun _ : Fin k => H) j)))

theorem operator_block_entry_apply (k : ℕ)
    (T : (PiLp 2 (fun _ : Fin k => H)) →L[ℂ] (PiLp 2 (fun _ : Fin k => H)))
    (i j : Fin k) (v : H) :
    operatorBlockEntry H k T i j v = T (PiLp.single 2 j v) i := rfl

theorem operator_block_entry_recover (k : ℕ)
    (M : CStarMatrix (Fin k) (Fin k) (H →L[ℂ] H)) (i j : Fin k) :
    operatorBlockEntry H k (operatorBlockCLM H k M) i j = M i j := by
  ext v
  simp [operator_block_entry_apply, operator_block_apply, PiLp.single_apply, apply_ite]

/-- No coordinate is lost, including the vacuous zero dimensional case. -/
theorem operator_block_injective (k : ℕ) :
    Function.Injective (operatorBlockCLM H k) := by
  intro M N h
  apply CStarMatrix.ext
  intro i j
  have he := congrArg (fun T => operatorBlockEntry H k T i j) h
  simpa only [operator_block_entry_recover] using he

omit [InnerProductSpace ℂ H] in
theorem operator_block_sum_single (k : ℕ) (v : PiLp 2 (fun _ : Fin k => H)) :
    ∑ j, PiLp.single 2 j (v j) = v := by
  apply PiLp.ext
  intro i
  simp

/-- Every bounded operator on a finite direct sum has a matrix of bounded entries. -/
theorem operator_block_surjective (k : ℕ) :
    Function.Surjective (operatorBlockCLM H k) := by
  intro T
  refine ⟨CStarMatrix.ofMatrix (fun i j => operatorBlockEntry H k T i j), ?_⟩
  ext v i
  rw [operator_block_apply]
  change (∑ j, operatorBlockEntry H k T i j (v j)) = T v i
  simp only [operator_block_entry_apply]
  have hs : (∑ j, T (PiLp.single 2 j (v j))) = T v := by
    rw [← map_sum, operator_block_sum_single]
  simpa only [map_sum, PiLp.proj_apply] using
    congrArg (PiLp.proj 2 (fun _ : Fin k => H) i) hs

theorem operator_block_add (k : ℕ)
    (M N : CStarMatrix (Fin k) (Fin k) (H →L[ℂ] H)) :
    operatorBlockCLM H k (M+N) = operatorBlockCLM H k M+operatorBlockCLM H k N := by
  ext v i
  simp [operator_block_apply, Finset.sum_add_distrib]

theorem operator_block_smul (k : ℕ) (c : ℂ)
    (M : CStarMatrix (Fin k) (Fin k) (H →L[ℂ] H)) :
    operatorBlockCLM H k (c • M) = c • operatorBlockCLM H k M := by
  ext v i
  simp [operator_block_apply, Finset.smul_sum]

theorem operator_block_mul (k : ℕ)
    (M N : CStarMatrix (Fin k) (Fin k) (H →L[ℂ] H)) :
    operatorBlockCLM H k (M*N) = operatorBlockCLM H k M*operatorBlockCLM H k N := by
  ext v i
  simp only [mul_apply_eq_comp, operator_block_apply, CStarMatrix.mul_apply,
    _root_.sum_apply, map_sum]
  exact Finset.sum_comm

variable [CompleteSpace H]

theorem operator_block_star (k : ℕ)
    (M : CStarMatrix (Fin k) (Fin k) (H →L[ℂ] H)) :
    operatorBlockCLM H k (star M) = star (operatorBlockCLM H k M) := by
  apply ContinuousLinearMap.ext
  intro v
  apply ext_inner_left ℂ
  intro w
  rw [ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.adjoint_inner_right]
  simp only [PiLp.inner_apply, operator_block_apply, CStarMatrix.star_apply,
    inner_sum, sum_inner, ContinuousLinearMap.star_eq_adjoint,
    ContinuousLinearMap.adjoint_inner_right]
  exact Finset.sum_comm

/-- A concrete star algebra equivalence, with an explicit entrywise inverse. -/
def operatorBlockRepresentation (k : ℕ) :
    CStarMatrix (Fin k) (Fin k) (H →L[ℂ] H) ≃⋆ₐ[ℂ]
      ((PiLp 2 (fun _ : Fin k => H)) →L[ℂ] (PiLp 2 (fun _ : Fin k => H))) where
  toFun := operatorBlockCLM H k
  invFun := fun T => CStarMatrix.ofMatrix (fun i j => operatorBlockEntry H k T i j)
  left_inv := by
    intro M
    apply CStarMatrix.ext
    intro i j
    exact operator_block_entry_recover H k M i j
  right_inv := by
    intro T
    obtain ⟨M, rfl⟩ := operator_block_surjective H k T
    congr 1
    apply CStarMatrix.ext
    intro i j
    exact operator_block_entry_recover H k M i j
  map_add' := operator_block_add H k
  map_mul' := operator_block_mul H k
  map_smul' := operator_block_smul H k
  map_star' := operator_block_star H k

theorem operator_block_representation_apply (k : ℕ)
    (M : CStarMatrix (Fin k) (Fin k) (H →L[ℂ] H))
    (v : PiLp 2 (fun _ : Fin k => H)) (i : Fin k) :
    operatorBlockRepresentation H k M v i = ∑ j, M i j (v j) :=
  operator_block_apply H k M v i

theorem operator_block_nonneg_representation_iff (k : ℕ)
    (M : CStarMatrix (Fin k) (Fin k) (H →L[ℂ] H)) :
    0 ≤ operatorBlockRepresentation H k M ↔ 0 ≤ M := by
  constructor
  · intro h
    have hs := map_nonneg (operatorBlockRepresentation H k).symm h
    simpa only [StarAlgEquiv.symm_apply_apply] using hs
  · exact map_nonneg (operatorBlockRepresentation H k)

/-- The represented quadratic form is exactly the finite block quadratic form. -/
theorem operator_block_inner (k : ℕ)
    (M : CStarMatrix (Fin k) (Fin k) (H →L[ℂ] H))
    (v : PiLp 2 (fun _ : Fin k => H)) :
    inner ℂ v (operatorBlockRepresentation H k M v) =
      ∑ i, ∑ j, inner ℂ (v i) (M i j (v j)) := by
  simp only [PiLp.inner_apply, operator_block_representation_apply, inner_sum]

/-- C-star positivity is equivalent to entrywise Hermiticity and all Hilbert block tests. -/
theorem operator_block_nonneg_iff (k : ℕ)
    (M : CStarMatrix (Fin k) (Fin k) (H →L[ℂ] H)) :
    0 ≤ M ↔
      (∀ i j, star (M i j) = M j i) ∧
      ∀ v : Fin k → H, 0 ≤ (∑ i, ∑ j, inner ℂ (v i) (M i j (v j))).re := by
  constructor
  · intro hM
    have hT : (operatorBlockRepresentation H k M).IsPositive :=
      (ContinuousLinearMap.nonneg_iff_isPositive _).mp
        ((operator_block_nonneg_representation_iff H k M).mpr hM)
    refine ⟨?_, ?_⟩
    · intro i j
      exact CStarMatrix.star_apply_of_isSelfAdjoint hM.isSelfAdjoint
    · intro v
      change 0 ≤ RCLike.re (∑ i, ∑ j, inner ℂ (v i) (M i j (v j)))
      have hv := hT.re_inner_nonneg_right (WithLp.toLp 2 v)
      simpa only [operator_block_inner, PiLp.toLp_apply] using hv
  · rintro ⟨hstar, hq⟩
    have hM : IsSelfAdjoint M := by
      change star M = M
      apply CStarMatrix.ext
      intro i j
      exact hstar j i
    apply (operator_block_nonneg_representation_iff H k M).mp
    apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
    apply ContinuousLinearMap.isPositive_def'.mpr
    refine ⟨hM.map (operatorBlockRepresentation H k), ?_⟩
    intro v
    change 0 ≤ (inner ℂ (operatorBlockRepresentation H k M v) v).re
    change 0 ≤ RCLike.re (inner ℂ (operatorBlockRepresentation H k M v) v)
    rw [inner_re_symm, operator_block_inner]
    exact hq (fun i => v i)

#print axioms operatorBlockCLM
#print axioms operator_block_apply
#print axioms operatorBlockEntry
#print axioms operator_block_entry_apply
#print axioms operator_block_entry_recover
#print axioms operator_block_injective
#print axioms operator_block_sum_single
#print axioms operator_block_surjective
#print axioms operator_block_add
#print axioms operator_block_smul
#print axioms operator_block_mul
#print axioms operator_block_star
#print axioms operatorBlockRepresentation
#print axioms operator_block_representation_apply
#print axioms operator_block_nonneg_representation_iff
#print axioms operator_block_inner
#print axioms operator_block_nonneg_iff

end

end ChatgptAudit.Expectation047
