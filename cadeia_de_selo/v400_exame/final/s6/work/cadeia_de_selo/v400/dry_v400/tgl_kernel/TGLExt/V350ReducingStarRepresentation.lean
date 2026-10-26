import Mathlib

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

namespace TGLV350.Regular
noncomputable section
variable {A H : Type} [Semiring A] [StarRing A] [Algebra ℂ A]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Restriction to a complete invariant subspace of a star representation.
Invariance is required for every algebra element, hence also for adjoints. -/
def reducingStarRepresentation (ρ : A →⋆ₐ[ℂ] (H →L[ℂ] H))
    (S : Submodule ℂ H) [CompleteSpace S]
    (h : ∀ a, ∀ v ∈ S, ρ a v ∈ S) : A →⋆ₐ[ℂ] (S →L[ℂ] S) where
  toFun a := (ρ a).restrict (h a)
  map_one' := by
    ext1 v
    apply Subtype.ext
    change ρ 1 v.val = v.val
    rw [map_one]
    rfl
  map_mul' a b := by
    ext1 v
    apply Subtype.ext
    change ρ (a*b) v.val = ρ a (ρ b v.val)
    rw [map_mul]
    rfl
  map_zero' := by
    ext1 v
    apply Subtype.ext
    change ρ 0 v.val = 0
    rw [map_zero]
    rfl
  map_add' a b := by
    ext1 v
    apply Subtype.ext
    change ρ (a+b) v.val = ρ a v.val + ρ b v.val
    rw [map_add]
    rfl
  commutes' c := by
    ext1 v
    apply Subtype.ext
    change ρ (algebraMap ℂ A c) v.val = c • v.val
    exact congrArg (fun T : H →L[ℂ] H => T v.val) (ρ.commutes c)
  map_star' a := by
    ext1 v
    apply ext_inner_left ℂ
    intro w
    rw [ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_right]
    change inner ℂ w.val (ρ (star a) v.val) = inner ℂ (ρ a w.val) v.val
    rw [map_star,ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_right]

#print axioms reducingStarRepresentation
end
end TGLV350.Regular
