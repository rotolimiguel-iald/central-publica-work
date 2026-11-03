import Mathlib.Analysis.InnerProductSpace.Adjoint
/-! Adjoint of the restriction to a reducing closed subspace. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.ClosedSubmoduleRestriction
variable {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
variable (S : Submodule ℂ E) [CompleteSpace S]
theorem adjoint_restrict (A B : E →L[ℂ] E)
    (hA : ∀ x∈S, A x∈S) (hB : ∀ x∈S, B x∈S) (hs : star A=B) :
    (A.restrict hA).adjoint=B.restrict hB := by
  ext1 x
  apply ext_inner_left ℂ
  intro y
  rw [ContinuousLinearMap.adjoint_inner_right]
  change inner ℂ (A y.val) x.val=inner ℂ y.val (B x.val)
  rw [←hs,ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_right]
def endomorphismStar : Star (S →L[ℂ] S) := inferInstance

theorem closure_range_preserved {X : Type} [AddCommMonoid X] [Module ℂ X]
    (V : X →ₗ[ℂ] E) (A : E →L[ℂ] E)
    (h : ∀ x, A (V x) ∈ V.range.topologicalClosure) :
    ∀ y∈V.range.topologicalClosure, A y∈V.range.topologicalClosure := by
  have hm : V.range.topologicalClosure ≤ V.range.topologicalClosure.comap A.toLinearMap := by
    apply Submodule.topologicalClosure_minimal
    · rintro _ ⟨x,rfl⟩
      exact h x
    · exact (Submodule.isClosed_topologicalClosure _).preimage A.continuous
  exact fun y hy => hm hy

end F1Fecho.ClosedSubmoduleRestriction
#print axioms F1Fecho.ClosedSubmoduleRestriction.adjoint_restrict
#print axioms F1Fecho.ClosedSubmoduleRestriction.endomorphismStar
#print axioms F1Fecho.ClosedSubmoduleRestriction.closure_range_preserved
