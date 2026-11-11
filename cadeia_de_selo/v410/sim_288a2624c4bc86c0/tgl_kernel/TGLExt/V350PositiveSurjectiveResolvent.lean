import TGLExt.V350AntilinearAdjointGraph
import Mathlib.Analysis.InnerProductSpace.Projection.Submodule
import Mathlib.Tactic

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (T : H →ₗ.[ℂ] H)
variable (hp : ∀ x : T.domain, 0 ≤ (inner ℂ (x : H) (T x)).re)
variable (hr : ∀ z : H, ∃ x : T.domain, (x : H)+T x=z)

include hp hr in
theorem positive_surjective_resolvent_domain_dense : Dense (T.domain : Set H) := by
  have ho : T.domain.orthogonal = ⊥ := by
    apply le_antisymm ?_ bot_le
    intro v hv
    change v=0
    obtain ⟨x,hx⟩ := hr v
    have hzero : (inner ℂ (x : H) ((x : H)+T x)).re = 0 := by
      rw [hx]
      exact congrArg Complex.re (hv (x : H) x.property)
    rw [inner_add_right,Complex.add_re] at hzero
    have hn : (inner ℂ (x : H) (x : H)).re = ‖(x : H)‖^2 :=
      (norm_sq_eq_re_inner (𝕜 := ℂ) (x : H)).symm
    have hz : (x : H)=0 := by
      apply norm_eq_zero.mp
      have hpos := hp x
      nlinarith only [hzero,hn,hpos,norm_nonneg (x : H)]
    have hxs : x=0 := Subtype.ext hz
    have ht0 : T (0 : T.domain)=0 := T.toFun.map_zero
    simpa only [hxs,Submodule.coe_zero,ht0,add_zero] using hx.symm
  rw [dense_iff_closure_eq]
  exact congrArg (fun V : Submodule ℂ H => (V : Set H))
    (T.domain.topologicalClosure_eq_top_iff.mpr ho)

include hp hr in
/-- Positivity gives density; full range of I+T eliminates any adjoint extension.
This proves self-adjointness, not merely symmetry of a prescribed domain. -/
theorem positive_surjective_resolvent_selfadjoint (hs : T.IsFormalAdjoint T) :
    IsSelfAdjoint T := by
  have hd := positive_surjective_resolvent_domain_dense T hp hr
  have hle : T.adjoint ≤ T := by
    apply LinearPMap.le_of_le_graph
    rintro ⟨y,v⟩ hgraph
    obtain ⟨a,ha,hv⟩ := (LinearPMap.mem_graph_iff T.adjoint).mp hgraph
    obtain ⟨x,hx⟩ := hr ((a : H)+T.adjoint a)
    have hax : (a : H)=(x : H) := by
      apply ext_inner_right ℂ
      intro b
      obtain ⟨u,hu⟩ := hr b
      have hadj := LinearPMap.adjoint_isFormalAdjoint (T := T) hd a u
      have hsym := hs x u
      calc
        inner ℂ (a : H) b = inner ℂ (a : H) ((u : H)+T u) := by rw [hu]
        _ = inner ℂ ((a : H)+T.adjoint a) (u : H) := by
          rw [inner_add_right,inner_add_left,hadj]
        _ = inner ℂ ((x : H)+T x) (u : H) := by rw [hx]
        _ = inner ℂ (x : H) ((u : H)+T u) := by
          rw [inner_add_left,inner_add_right,hsym]
        _ = inner ℂ (x : H) b := by rw [hu]
    have hval : T x=T.adjoint a := by
      apply add_left_cancel (a := (x : H))
      exact hx.trans (congrArg (fun z : H => z+T.adjoint a) hax)
    exact (LinearPMap.mem_graph_iff T).mpr ⟨x,hax.symm.trans ha,hval.trans hv⟩
  rw [LinearPMap.isSelfAdjoint_def]
  exact le_antisymm hle (hs.le_adjoint hd)

#print axioms positive_surjective_resolvent_domain_dense
#print axioms positive_surjective_resolvent_selfadjoint
end
end TGLV350.Regular
