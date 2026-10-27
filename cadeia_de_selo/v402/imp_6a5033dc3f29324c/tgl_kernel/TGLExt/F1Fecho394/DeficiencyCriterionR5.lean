import Mathlib.Analysis.InnerProductSpace.LinearPMap
import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.Tactic
/-! A closed symmetric operator is self-adjoint when both actual adjoint
nonreal eigenspaces vanish. Proof by projection onto its closed L2 graph.
No self-adjoint extension or resolvent surjectivity is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.DeficiencyCriterion
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

 theorem selfAdjoint_of_no_deficiency (G : H →ₗ.[ℂ] H)
    (hc : G.IsClosed) (hs : G.IsFormalAdjoint G) (hd : Dense (G.domain : Set H))
    (hplus : ∀ x : H, (x,Complex.I • x) ∈ G.adjoint.graph → x=0)
    (hminus : ∀ x : H, (x,-Complex.I • x) ∈ G.adjoint.graph → x=0) :
    IsSelfAdjoint G := by
  have hsub := hs.le_adjoint hd
  apply LinearPMap.isSelfAdjoint_def.mpr
  apply le_antisymm _ hsub
  apply LinearPMap.le_of_le_graph
  intro p hp
  let E := WithLp 2 (H × H)
  let e : E ≃L[ℂ] H × H := WithLp.prodContinuousLinearEquiv 2 ℂ H H
  let L : Submodule ℂ E := G.graph.comap e.toLinearMap
  have hL : IsClosed (L : Set E) := hc.preimage e.continuous
  letI : CompleteSpace L := hL.completeSpace_coe
  let w : E := e.symm p
  let q : E := L.starProjection w
  let r : E := w-q
  have hq : e q ∈ G.graph := Submodule.starProjection_apply_mem L w
  have hr : e r ∈ G.adjoint.graph := by
    change e (w-q) ∈ G.adjoint.graph
    rw [map_sub]
    apply G.adjoint.graph.sub_mem
    · simpa only [w,ContinuousLinearEquiv.apply_symm_apply] using hp
    · exact LinearPMap.le_graph_of_le hsub hq
  have horth (x : G.domain) : inner ℂ r (e.symm ((x:H),G x))=0 := by
    apply Submodule.starProjection_inner_eq_zero w _
    change e (e.symm ((x:H),G x)) ∈ G.graph
    simpa only [ContinuousLinearEquiv.apply_symm_apply] using G.mem_graph x
  let u := (e r).1
  let v := (e r).2
  have hswap : (v,-u) ∈ G.adjoint.graph := by
    rw [LinearPMap.adjoint_graph_eq_graph_adjoint hd,Submodule.mem_adjoint_iff]
    intro a b hab
    obtain ⟨x,hx⟩ := G.mem_graph_iff'.mp hab
    have hx1 : (x:H)=a := congrArg Prod.fst hx
    have hx2 : G x=b := congrArg Prod.snd hx
    rw [← hx1,← hx2]
    have hh := horth x
    change inner ℂ u (x:H) + inner ℂ v (G x)=0 at hh
    have hh' := congrArg (starRingEnd ℂ) hh
    simp only [map_add,map_zero,inner_conj_symm] at hh'
    simp only [Prod.fst,Prod.snd,inner_neg_right,sub_neg_eq_add]
    exact (add_comm _ _).trans hh'
  have hm : u+Complex.I • v=0 := by
    apply hminus
    have hh := G.adjoint.graph.add_mem hr (G.adjoint.graph.smul_mem Complex.I hswap)
    convert hh using 1
    ext <;> simp [u,v,smul_add,smul_smul,neg_smul,Complex.I_sq] <;> module
  have hp' : u-Complex.I • v=0 := by
    apply hplus
    have hh := G.adjoint.graph.sub_mem hr (G.adjoint.graph.smul_mem Complex.I hswap)
    convert hh using 1
    ext <;> simp [u,v,smul_sub,smul_smul,neg_smul,Complex.I_sq] <;> module
  have hu : u=0 := by
    have h2 : (2:ℂ) • u=0 := by
      calc
        (2:ℂ) • u=(u+Complex.I • v)+(u-Complex.I • v) := by module
        _=0 := by rw [hm,hp',add_zero]
    exact (smul_eq_zero.mp h2).resolve_left (by norm_num)
  have hv : v=0 := by
    rw [hu,zero_add] at hm
    exact (smul_eq_zero.mp hm).resolve_left Complex.I_ne_zero
  have hr0 : r=0 := by
    apply e.injective
    exact (Prod.ext hu hv).trans (map_zero e).symm
  have he : w=q := sub_eq_zero.mp hr0
  have hw : e w ∈ G.graph := by rw [he]; exact hq
  simpa only [w,ContinuousLinearEquiv.apply_symm_apply] using hw

end F1Fecho.DeficiencyCriterion
#print axioms F1Fecho.DeficiencyCriterion.selfAdjoint_of_no_deficiency
