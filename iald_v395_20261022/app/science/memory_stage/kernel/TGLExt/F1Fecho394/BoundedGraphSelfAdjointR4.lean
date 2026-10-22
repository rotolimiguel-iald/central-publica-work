import Mathlib.Analysis.InnerProductSpace.LinearPMap
import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.Tactic
/-! A maximality criterion from an actual bounded parametrization of a graph.
No self-adjoint extension, resolvent estimate, or surjectivity is assumed.
The proof uses the orthogonal projection of the L2 product graph. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.BoundedGraphSelfAdjoint
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

private theorem clm_pairing (A : H →L[ℂ] H) (hA : IsSelfAdjoint A) (x y : H) :
    inner ℂ (A x) y = inner ℂ x (A y) := hA.isSymmetric x y

private theorem bounded_pair_zero (A B : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B)
    (hAB : A * B = B * A) (hAi : Function.Injective A)
    (u v : H) (h0 : A u + B v = 0) (h1 : A v = B u) : u=0 ∧ v=0 := by
  have hc (x : H) : A (B x) = B (A x) :=
    congrArg (fun C : H →L[ℂ] H => C x) hAB
  have hu : A u = -(B v) := eq_neg_of_add_eq_zero_left h0
  have hdouble : A (A u) + B (B u) = 0 := by
    rw [hu,map_neg,← h1,hc]
    exact neg_add_cancel _
  have hi : inner ℂ (A u) (A u) + inner ℂ (B u) (B u) = 0 := by
    rw [clm_pairing A hA u (A u),clm_pairing B hB u (B u),← inner_add_right,hdouble,inner_zero_right]
  have hr : ‖A u‖ ^ 2 + ‖B u‖ ^ 2 = 0 := by
    simpa only [map_add,inner_self_eq_norm_sq,map_zero] using
      congrArg (RCLike.re : ℂ → ℝ) hi
  have hau : A u = 0 := norm_eq_zero.mp (by nlinarith [sq_nonneg ‖B u‖,norm_nonneg (A u)])
  have hu0 : u=0 := hAi (by simpa only [map_zero] using hau)
  have hav : A v=0 := by simpa only [hu0,map_zero] using h1
  exact ⟨hu0,hAi (by simpa only [map_zero] using hav)⟩

private theorem graph_constraint (G : H →ₗ.[ℂ] H)
    (hs : G.IsFormalAdjoint G) (A B : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B)
    (hgraph : ∀ x : H, (A x,B x) ∈ G.graph)
    (p : H × H) (hp : p ∈ G.graph) : A p.2 = B p.1 := by
  obtain ⟨y,rfl⟩ := G.mem_graph_iff'.mp hp
  apply ext_inner_left ℂ
  intro x
  obtain ⟨z,hz⟩ := G.mem_graph_iff'.mp (hgraph x)
  have hz1 : (z:H)=A x := congrArg Prod.fst hz
  have hz2 : G z=B x := congrArg Prod.snd hz
  have h := hs z y
  rw [hz1,hz2,clm_pairing B hB x (y:H),clm_pairing A hA x (G y)] at h
  exact h.symm

private theorem adjoint_constraint (G : H →ₗ.[ℂ] H)
    (hd : Dense (G.domain : Set H)) (A B : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B)
    (hgraph : ∀ x : H, (A x,B x) ∈ G.graph)
    (p : H × H) (hp : p ∈ G.adjoint.graph) : A p.2 = B p.1 := by
  rw [LinearPMap.adjoint_graph_eq_graph_adjoint hd] at hp
  have hh := (Submodule.mem_adjoint_iff G.graph p).mp hp
  apply ext_inner_left ℂ
  intro x
  have h := sub_eq_zero.mp (hh (A x) (B x) (hgraph x))
  rw [clm_pairing B hB x p.1,clm_pairing A hA x p.2] at h
  exact h.symm

theorem adjoint_graph_le_of_bounded_pair (G : H →ₗ.[ℂ] H)
    (hc : G.IsClosed) (hs : G.IsFormalAdjoint G)
    (hd : Dense (G.domain : Set H)) (A B : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B)
    (hAB : A * B = B * A) (hAi : Function.Injective A)
    (hgraph : ∀ x : H, (A x,B x) ∈ G.graph) :
    G.adjoint.graph ≤ G.graph := by
  let E := WithLp 2 (H × H)
  let e : E ≃L[ℂ] H × H := WithLp.prodContinuousLinearEquiv 2 ℂ H H
  let L : Submodule ℂ E := G.graph.comap e.toLinearMap
  have hL : IsClosed (L : Set E) := hc.preimage e.continuous
  letI : CompleteSpace L := hL.completeSpace_coe
  intro p hp
  let w : E := e.symm p
  let q : E := L.starProjection w
  let r : E := w-q
  have hq : e q ∈ G.graph := Submodule.starProjection_apply_mem L w
  have hwrel : A (e w).2 = B (e w).1 := by
    simpa only [w,ContinuousLinearEquiv.apply_symm_apply] using
      adjoint_constraint G hd A B hA hB hgraph p hp
  have hqrel := graph_constraint G hs A B hA hB hgraph (e q) hq
  have hrrel : A (e r).2 = B (e r).1 := by
    change A (e (w-q)).2 = B (e (w-q)).1
    rw [map_sub]
    change A ((e w).2-(e q).2) = B ((e w).1-(e q).1)
    rw [map_sub,map_sub,hwrel,hqrel]
  have horth (x : H) : inner ℂ r (e.symm (A x,B x)) = 0 := by
    apply Submodule.starProjection_inner_eq_zero w _
    change e (e.symm (A x,B x)) ∈ G.graph
    simpa only [ContinuousLinearEquiv.apply_symm_apply] using hgraph x
  have hsum : A (e r).1 + B (e r).2 = 0 := by
    apply (inner_self_eq_zero (𝕜 := ℂ)).mp
    have h := horth (A (e r).1 + B (e r).2)
    change inner ℂ (e r).1 (A (A (e r).1+B (e r).2)) +
      inner ℂ (e r).2 (B (A (e r).1+B (e r).2)) = 0 at h
    rw [← clm_pairing A hA (e r).1 _,← clm_pairing B hB (e r).2 _,← inner_add_left] at h
    exact h
  obtain ⟨hu,hv⟩ := bounded_pair_zero A B hA hB hAB hAi (e r).1 (e r).2 hsum hrrel
  have hr0 : r=0 := by
    apply e.injective
    exact (Prod.ext hu hv).trans (map_zero e).symm
  have heq : w=q := sub_eq_zero.mp hr0
  have hw : e w ∈ G.graph := by rw [heq]; exact hq
  simpa only [w,ContinuousLinearEquiv.apply_symm_apply] using hw

theorem selfAdjoint_of_bounded_pair (G : H →ₗ.[ℂ] H)
    (hc : G.IsClosed) (hs : G.IsFormalAdjoint G)
    (hd : Dense (G.domain : Set H)) (A B : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B)
    (hAB : A * B = B * A) (hAi : Function.Injective A)
    (hgraph : ∀ x : H, (A x,B x) ∈ G.graph) : IsSelfAdjoint G := by
  apply LinearPMap.isSelfAdjoint_def.mpr
  exact le_antisymm
    (LinearPMap.le_of_le_graph (adjoint_graph_le_of_bounded_pair G hc hs hd A B hA hB hAB hAi hgraph))
    (hs.le_adjoint hd)

end F1Fecho.BoundedGraphSelfAdjoint
#print axioms F1Fecho.BoundedGraphSelfAdjoint.adjoint_graph_le_of_bounded_pair
#print axioms F1Fecho.BoundedGraphSelfAdjoint.selfAdjoint_of_bounded_pair
