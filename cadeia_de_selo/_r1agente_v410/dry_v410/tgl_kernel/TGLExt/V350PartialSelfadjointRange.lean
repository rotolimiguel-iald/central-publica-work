import Mathlib.Analysis.InnerProductSpace.LinearPMap

set_option autoImplicit false
set_option linter.unusedSectionVars false

namespace TGLV350.Regular
open scoped LinearPMap
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- A densely defined self-adjoint partial map with zero kernel has dense range.
No lower bound, bounded inverse, or surjectivity is asserted. -/
theorem partialSelfadjoint_denseRange (B : H →ₗ.[ℂ] H)
    (hd : Dense (B.domain : Set H)) (hs : IsSelfAdjoint B)
    (hk : ∀ x : B.domain, B x=0 → (x : H)=0) : DenseRange B.toFun := by
  have he : B.adjoint=B := hs
  have ho : B.toFun.range.orthogonal=⊥ := by
    apply le_antisymm ?_ bot_le
    intro z hz
    change z=0
    have hp : ∀ x : B.domain, inner ℂ (0 : H) (x : H)=inner ℂ z (B x) := by
      intro x
      have h := hz (B x) ⟨x,rfl⟩
      rw [inner_zero_left]
      exact (inner_eq_zero_symm.mp h).symm
    have hm : z ∈ B.adjoint.domain :=
      LinearPMap.mem_adjoint_domain_of_exists z ⟨0,hp⟩
    have ha : B.adjoint ⟨z,hm⟩=0 := LinearPMap.adjoint_apply_eq hd ⟨z,hm⟩ hp
    have hg : (z,0) ∈ B.adjoint.graph :=
      (LinearPMap.mem_graph_iff B.adjoint).mpr ⟨⟨z,hm⟩,rfl,ha⟩
    rw [he] at hg
    obtain ⟨x,hx,hBx⟩ := (LinearPMap.mem_graph_iff B).mp hg
    exact hx.symm.trans (hk x hBx)
  change Dense (Set.range B.toFun)
  rw [dense_iff_closure_eq]
  exact congrArg (fun V : Submodule ℂ H => (V : Set H))
    (B.toFun.range.topologicalClosure_eq_top_iff.mpr ho)

#print axioms partialSelfadjoint_denseRange
end
end TGLV350.Regular
