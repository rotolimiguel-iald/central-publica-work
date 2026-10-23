import Mathlib.Analysis.InnerProductSpace.StandardSubspace
/-! The cyclic half of standardness implies density of the complex span.
Generic Hilbert-space formulation avoids expanding a particular L2 carrier. -/
set_option autoImplicit false
set_option maxHeartbeats 300000
noncomputable section
namespace F1Fecho.StandardComplexSpan
open ClosedSubmodule
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

theorem dense (K : StandardSubspace H) :
    (Submodule.span ℂ (K.toClosedSubmodule : Set H)).topologicalClosure = ⊤ := by
  let p := Submodule.span ℂ (K.toClosedSubmodule : Set H)
  let C : ClosedSubmodule ℝ H :=
    { toSubmodule := p.topologicalClosure.restrictScalars ℝ
      isClosed' := p.isClosed_topologicalClosure }
  have hk : K.toClosedSubmodule ≤ C := by
    intro x hx
    exact p.le_topologicalClosure (Submodule.subset_span hx)
  have hi : K.toClosedSubmodule.mulI ≤ C := by
    intro x hx
    change x ∈ K.toClosedSubmodule.toSubmodule.map
      (scalarSMulCLE H Complex.UnitI).toLinearMap at hx
    obtain ⟨y,hy,rfl⟩ := hx
    change Complex.I • y ∈ p.topologicalClosure
    exact p.topologicalClosure.smul_mem Complex.I (p.le_topologicalClosure (Submodule.subset_span hy))
  have ht : (⊤ : ClosedSubmodule ℝ H) ≤ C := by
    rw [← K.IsCyclic]
    exact sup_le hk hi
  apply top_unique
  intro x _
  exact ht (by trivial : x ∈ (⊤ : ClosedSubmodule ℝ H))
end F1Fecho.StandardComplexSpan
#print axioms F1Fecho.StandardComplexSpan.dense
