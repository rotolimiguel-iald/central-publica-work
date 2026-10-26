import TGLExt.F1Fecho394.PositiveRegularizedRootR3
/-! A resolvent equation from bounded graph parameters. In particular this
uses A²+B², without incorrectly imposing A²+B²=1 after second quantization. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.BoundedPairResolvent
open ChatgptAudit.UnboundedTransform016 F1Fecho.PositiveRegularized
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (G:H→ₗ.[ℂ]H) (hs:IsSelfAdjoint G) (A B:H→L[ℂ]H)
  (hA:IsSelfAdjoint A) (hB:IsSelfAdjoint B)
  (hgraph:∀x:H,(A x,B x)∈G.graph)

include hs hA hB hgraph in
theorem domain_relation (x:G.domain) : A (G x)=B (x:H) := by
  apply ext_inner_left ℂ
  intro y
  obtain ⟨v,hv,hv'⟩:=(LinearPMap.mem_graph_iff G).mp (hgraph y)
  calc
    inner ℂ y (A (G x)) = inner ℂ (A y) (G x) := (hA.isSymmetric y (G x)).symm
    _ = inner ℂ (v:H) (G x) := congrArg (fun z=>inner ℂ z (G x)) hv.symm
    _ = inner ℂ (G v) (x:H) := (selfadjoint_formal G hs v x).symm
    _ = inner ℂ (B y) (x:H) := congrArg (fun z=>inner ℂ z (x:H)) hv'
    _ = inner ℂ y (B (x:H)) := hB.isSymmetric y (x:H)

include hs hA hB hgraph in
theorem equation (hAB:A*B=B*A) :
    (A*A+B*B)*selfadjointSquareResolvent G hs=A*A := by
  ext x
  have h1:=domain_relation G hs A B hA hB hgraph (input G hs x)
  change A (L G hs x)=B (R G hs x) at h1
  have h2:=domain_relation G hs A B hA hB hgraph (second G hs x)
  change A (G (second G hs x))=B (L G hs x) at h2
  rw [eq_sub_of_add_eq' (PositiveRegularized.equation G hs x),map_sub] at h2
  have hc (v:H) : A (B v)=B (A v) := congrArg (fun F:H→L[ℂ]H=>F v) hAB
  change A (A (R G hs x))+B (B (R G hs x))=A (A x)
  symm
  calc
    A (A x) = A (B (L G hs x)+A (R G hs x)) := congrArg A (eq_add_of_sub_eq h2)
    _ = A (A (R G hs x))+B (A (L G hs x)) := by rw [map_add,hc]; abel
    _ = A (A (R G hs x))+B (B (R G hs x)) := by rw [h1]

end F1Fecho.BoundedPairResolvent
#print axioms F1Fecho.BoundedPairResolvent.domain_relation
#print axioms F1Fecho.BoundedPairResolvent.equation
