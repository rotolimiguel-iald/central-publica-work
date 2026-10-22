import TGLExt.F1Fecho394.DeficiencyCriterionR5
/-! Adjoint and closure identities for densely defined symmetric operators.
The final criterion proves essential self-adjointness from actual deficiency
spaces, rather than assuming a self-adjoint extension. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.DeficiencyCriterion
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem submodule_adjoint_closure (L : Submodule ℂ (H × H)) :
    L.topologicalClosure.adjoint = L.adjoint := by
  ext p
  rw [Submodule.mem_adjoint_iff,Submodule.mem_adjoint_iff]
  constructor
  · intro h a b hab
    exact h a b (L.le_topologicalClosure hab)
  · intro h a b hab
    have hc : IsClosed {q : H × H | inner ℂ q.2 p.1 - inner ℂ q.1 p.2=0} :=
      isClosed_eq ((continuous_snd.inner continuous_const).sub
        (continuous_fst.inner continuous_const)) continuous_const
    have hs : _root_.closure (L : Set (H × H)) ⊆
        {q : H × H | inner ℂ q.2 p.1-inner ℂ q.1 p.2=0} := by
      apply hc.closure_subset_iff.mpr
      rintro ⟨x,y⟩ hxy
      exact h x y hxy
    exact hs hab

theorem adjoint_closure (A : H →ₗ.[ℂ] H) (hd : Dense (A.domain : Set H))
    (hc : A.IsClosable) : A.closure.adjoint=A.adjoint := by
  have hd' : Dense (A.closure.domain : Set H) := hd.mono A.le_closure.1
  apply LinearPMap.eq_of_eq_graph
  rw [LinearPMap.adjoint_graph_eq_graph_adjoint hd',
    ← hc.graph_closure_eq_closure_graph,submodule_adjoint_closure,
    LinearPMap.adjoint_graph_eq_graph_adjoint hd]

theorem symmetric_closable (A : H →ₗ.[ℂ] H) (hd : Dense (A.domain : Set H))
    (hs : A.IsFormalAdjoint A) : A.IsClosable :=
  (LinearPMap.adjoint_isClosed hd).isClosable.leIsClosable (hs.le_adjoint hd)

theorem closure_le_adjoint (A : H →ₗ.[ℂ] H) (hd : Dense (A.domain : Set H))
    (hs : A.IsFormalAdjoint A) : A.closure ≤ A.adjoint := by
  apply LinearPMap.le_of_le_graph
  rw [← (symmetric_closable A hd hs).graph_closure_eq_closure_graph]
  exact (LinearPMap.adjoint_isClosed hd).closure_subset_iff.mpr
    (LinearPMap.le_graph_of_le (hs.le_adjoint hd))

theorem closure_formal_selfadjoint (A : H →ₗ.[ℂ] H) (hd : Dense (A.domain : Set H))
    (hs : A.IsFormalAdjoint A) : A.closure.IsFormalAdjoint A.closure := by
  have hd' : Dense (A.closure.domain : Set H) := hd.mono A.le_closure.1
  have hsub : A.closure ≤ A.closure.adjoint := by
    rw [adjoint_closure A hd (symmetric_closable A hd hs)]
    exact closure_le_adjoint A hd hs
  intro x y
  let z : A.closure.adjoint.domain := ⟨x,hsub.1 x.property⟩
  have hh := LinearPMap.adjoint_isFormalAdjoint hd' z y
  have he : A.closure x=A.closure.adjoint z := hsub.2 rfl
  rw [← he] at hh
  exact hh

theorem essentialSelfAdjoint_of_no_deficiency (A : H →ₗ.[ℂ] H)
    (hd : Dense (A.domain : Set H)) (hs : A.IsFormalAdjoint A)
    (hplus : ∀ x : H, (x,Complex.I • x) ∈ A.adjoint.graph → x=0)
    (hminus : ∀ x : H, (x,-Complex.I • x) ∈ A.adjoint.graph → x=0) :
    IsSelfAdjoint A.closure := by
  have hc := symmetric_closable A hd hs
  apply selfAdjoint_of_no_deficiency A.closure hc.closure_isClosed
    (closure_formal_selfadjoint A hd hs) (hd.mono A.le_closure.1)
  · simpa only [adjoint_closure A hd hc] using hplus
  · simpa only [adjoint_closure A hd hc] using hminus

end F1Fecho.DeficiencyCriterion
#print axioms F1Fecho.DeficiencyCriterion.adjoint_closure
#print axioms F1Fecho.DeficiencyCriterion.closure_formal_selfadjoint
#print axioms F1Fecho.DeficiencyCriterion.essentialSelfAdjoint_of_no_deficiency
