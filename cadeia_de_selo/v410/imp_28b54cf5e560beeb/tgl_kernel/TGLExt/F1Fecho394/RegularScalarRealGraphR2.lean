import TGLExt.F1Fecho394.RegularScalarClosedTomitaR1
/-! The actual closed GNS adjunction graph is a closed REAL linear subspace.
No complex linearity of its antilinear operator is imposed. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularScalarRealGraph
open F1Fecho.RegularScalarGNS F1Fecho.RegularScalarTomitaGraph
open F1Fecho.RegularScalarClosedTomita
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (D:Context H)
def closedGraph : Submodule ℝ (GNSHilbert D×GNSHilbert D) where
  carrier:=closure (scalarTomitaGraph D)
  zero_mem':=subset_closure scalarTomitaGraph_zero
  add_mem':=fun hx hy=>scalarClosedGraph_add hx hy
  smul_mem':=by
    intro c p hp
    have he:=scalarClosedGraph_conj_smul (c:ℂ) hp
    change ((c:ℂ) • p.1,(c:ℂ) • p.2)∈closure (scalarTomitaGraph D)
    have hc : starRingEnd ℂ (c:ℂ)=(c:ℂ) := Complex.conj_ofReal c
    rw [hc] at he
    exact he

theorem closedGraph_closed : IsClosed (closedGraph D:Set (GNSHilbert D×GNSHilbert D)) :=
  isClosed_closure

theorem closedGraph_mem (x y:GNSHilbert D) :
    (x,y)∈closedGraph D ↔ ∃z:scalarClosedTomitaDomain D,(z:GNSHilbert D)=x ∧ scalarClosedTomita D z=y := by
  change (x,y)∈closure (scalarTomitaGraph D) ↔ _
  rw [←scalarClosedTomita_graph_eq]
  constructor
  · rintro ⟨z,hz⟩
    exact ⟨z,congrArg Prod.fst hz,congrArg Prod.snd hz⟩
  · rintro ⟨z,hx,hy⟩
    exact ⟨z,Prod.ext hx hy⟩
end F1Fecho.RegularScalarRealGraph
#print axioms F1Fecho.RegularScalarRealGraph.closedGraph
#print axioms F1Fecho.RegularScalarRealGraph.closedGraph_closed
#print axioms F1Fecho.RegularScalarRealGraph.closedGraph_mem
