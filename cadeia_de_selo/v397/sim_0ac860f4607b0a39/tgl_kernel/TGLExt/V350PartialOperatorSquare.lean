import TGLExt.V350ResolventGraph
import TGLExt.ContinuousModularSquare

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open ChatgptAudit.Continuous049 ChatgptAudit.Continuous050
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Genuine successive domain, reusing the existing generic partialSquareDomain. -/
def partialOperatorSquare (T : H →ₗ.[ℂ] H) : H →ₗ.[ℂ] H where
  domain := partialSquareDomain T
  toFun := T.toFun.comp
    ((T.toFun.comp (Submodule.inclusion
      (show partialSquareDomain T ≤ T.domain from fun _ hf => hf.choose))).codRestrict
      T.domain (fun x => x.property.choose_spec))

theorem partialOperatorSquare_domain_iff (T : H →ₗ.[ℂ] H) (x : H) :
    x ∈ (partialOperatorSquare T).domain ↔
      ∃ hx : x ∈ T.domain, T ⟨x,hx⟩ ∈ T.domain := Iff.rfl

theorem partialOperatorSquare_graph_iff (T : H →ₗ.[ℂ] H) (x z : H) :
    (x,z) ∈ (partialOperatorSquare T).graph ↔
      ∃ y : H, (x,y) ∈ T.graph ∧ (y,z) ∈ T.graph := by
  rw [LinearPMap.mem_graph_iff]
  constructor
  · rintro ⟨w,hw,hz⟩
    let u : T.domain := ⟨w, w.property.choose⟩
    let v : T.domain := ⟨T u, w.property.choose_spec⟩
    refine ⟨T u, ?_, ?_⟩
    · rw [LinearPMap.mem_graph_iff]
      exact ⟨u,hw,rfl⟩
    · rw [LinearPMap.mem_graph_iff]
      exact ⟨v,rfl,hz⟩
  · rintro ⟨y,hxy,hyz⟩
    rw [LinearPMap.mem_graph_iff] at hxy hyz
    obtain ⟨u,hu,hTu⟩ := hxy
    obtain ⟨v,hv,hTv⟩ := hyz
    dsimp only [Prod.fst, Prod.snd] at hu hTu hv hTv
    have hTuD : T u ∈ T.domain := by
      rw [hTu, ← hv]
      exact v.property
    let w : (partialOperatorSquare T).domain := ⟨u, ⟨u.property,hTuD⟩⟩
    refine ⟨w,hu,?_⟩
    change T ⟨T u,hTuD⟩ = z
    have he : (⟨T u,hTuD⟩ : T.domain) = v := Subtype.ext (hTu.trans hv.symm)
    rw [he]
    exact hTv

/-- Squaring a bounded-pair graph yields the resolvent graph, with equality
of the full successive domain. No domain invariance is assumed. -/
theorem boundedGraph_square_eq_resolvent
    (A B R : H →L[ℂ] H) (hiA : Function.Injective A) (hiR : Function.Injective R)
    (hc : A*B = B*A) (hA : A*A = R) (hB : B*B = 1-R) :
    partialOperatorSquare (boundedGraphOperator A B hiA) = resolventGraphOperator R hiR := by
  have hs : A*A+B*B = 1 := by rw [hA,hB]; abel
  have hcv (u : H) : B (A u) = A (B u) :=
    congrArg (fun F : H →L[ℂ] H => F u) hc.symm
  have hAv (u : H) : A (A u) = R u := congrArg (fun F : H →L[ℂ] H => F u) hA
  have hBv (u : H) : B (B u) = (1-R) u := congrArg (fun F : H →L[ℂ] H => F u) hB
  apply LinearPMap.eq_of_eq_graph
  ext p
  rcases p with ⟨x,z⟩
  rw [partialOperatorSquare_graph_iff]
  constructor
  · rintro ⟨y,hxy,hyz⟩
    have hxy' := (bounded_graph_equation_iff A B hiA hc hs x y).mp hxy
    have hyz' := (bounded_graph_equation_iff A B hiA hc hs y z).mp hyz
    apply (resolvent_graph_equation R hiR x z).mpr
    calc
      (1-R) x = B (B x) := (hBv x).symm
      _ = B (A y) := by rw [hxy']
      _ = A (B y) := hcv y
      _ = A (A z) := by rw [hyz']
      _ = R z := hAv z
  · intro hxz
    obtain ⟨u,hu,hz⟩ := (bounded_graph_param_iff R (1-R) hiR x z).mp hxz
    refine ⟨A (B u), ?_, ?_⟩
    · apply (bounded_graph_param_iff A B hiA x (A (B u))).mpr
      exact ⟨A u, (hAv u).trans hu, hcv u⟩
    · apply (bounded_graph_param_iff A B hiA (A (B u)) z).mpr
      exact ⟨B u, rfl, (hBv u).trans hz⟩

#print axioms partialOperatorSquare
#print axioms partialOperatorSquare_domain_iff
#print axioms partialOperatorSquare_graph_iff
#print axioms boundedGraph_square_eq_resolvent
end
end TGLV350.Regular
