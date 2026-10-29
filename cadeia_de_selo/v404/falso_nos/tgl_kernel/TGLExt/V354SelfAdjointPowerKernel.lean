import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Tactic

set_option autoImplicit false

namespace TGLV354.TraceCompletion
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- General Hilbert-space kernel identity, with no finite-rank hypothesis.
It supplies the support comparison for positive shift-related operators. -/
theorem selfAdjoint_pow_ker (A : H →L[ℂ] H) (hA : IsSelfAdjoint A)
    (n : ℕ) (hn : 0 < n) : (A ^ n).ker = A.ker := by
  have hsq (x : H) (hx : A (A x) = 0) : A x = 0 := by
    have hker : x ∈ (A.adjoint.comp A).ker := by
      change A.adjoint (A x) = 0
      rw [hA.adjoint_eq]
      exact hx
    rw [A.ker_adjoint_comp_self] at hker
    exact hker
  have hforward (k : ℕ) (x : H) : (A ^ (k+1)) x = 0 → A x = 0 := by
    induction k with
    | zero => simpa only [zero_add, pow_one] using (id : A x = 0 → A x = 0)
    | succ k ih =>
      intro hx
      apply ih
      rw [pow_succ', ContinuousLinearMap.mul_apply]
      have hy := hsq ((A ^ k) x)
      apply hy
      simpa only [pow_succ', ContinuousLinearMap.mul_apply] using hx
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hn)
  ext x
  change (A ^ (k+1)) x = 0 ↔ A x = 0
  constructor
  · exact hforward k x
  · intro hx
    simp only [pow_succ, ContinuousLinearMap.mul_apply, hx, map_zero]

theorem selfAdjoint_pow_closedRange (A : H →L[ℂ] H) (hA : IsSelfAdjoint A)
    (n : ℕ) (hn : 0 < n) :
    (A ^ n).range.topologicalClosure = A.range.topologicalClosure := by
  have h := (A ^ n).orthogonal_ker
  rw [(hA.pow n).adjoint_eq, selfAdjoint_pow_ker A hA n hn] at h
  have h' := A.orthogonal_ker
  rw [hA.adjoint_eq] at h'
  exact h.symm.trans h'

/-- The support inclusions use the actual factorization witnesses. They do not
assert equality of the polar supports with the two positive supports. -/
theorem selfAdjoint_factor_supports (A B r s : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B)
    (n : ℕ) (hn : 0 < n) (hArs : A ^ n = r*s) (hBsr : B ^ n = s*r) :
    r.ker ≤ B.ker ∧ A.range.topologicalClosure ≤ r.range.topologicalClosure := by
  constructor
  · rw [← selfAdjoint_pow_ker B hB n hn]
    intro x hx
    change (B ^ n) x = 0
    rw [hBsr, ContinuousLinearMap.mul_apply]
    rw [show r x = 0 from hx, map_zero]
  · rw [← selfAdjoint_pow_closedRange A hA n hn]
    apply Submodule.topologicalClosure_mono
    rintro x ⟨y,rfl⟩
    refine ⟨s y,?_⟩
    exact (congrArg (fun T : H →L[ℂ] H => T y) hArs).symm

#print axioms selfAdjoint_pow_ker
#print axioms selfAdjoint_pow_closedRange
#print axioms selfAdjoint_factor_supports
end TGLV354.TraceCompletion
