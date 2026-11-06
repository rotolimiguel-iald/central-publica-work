import TGLExt.F1Fecho394.ClosedTomitaOperatorR1
import TGLExt.O16.RecognitionSquare
/-! The pairing-defined square relation is the exact maximal-adjoint
composition already constructed from a closed dense antilinear involution. -/
set_option autoImplicit false
set_option maxHeartbeats 700000
noncomputable section
namespace F1Fecho.ClosedTomitaSquareGraph
open F1Fecho.ClosedTomitaOperator ORDEM016.D6
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (A:Input H)

def graph : Set (H×H) := Set.range (fun x:A.domain=>((x:H),A.operator x))

theorem square_graph : antilinearSquareGraph (graph A)=((scalarTomitaSquare A).graph:Set (H×H)) := by
  ext p
  constructor
  · rintro ⟨sx,⟨v,hv⟩,hp⟩
    have hx:(v:H)=p.1:=congrArg Prod.fst hv
    have hs:A.operator v=sx:=congrArg Prod.snd hv
    have hh:∀y:A.domain,inner ℂ (A.operator y) (A.operator v)=inner ℂ p.2 (y:H) := by
      intro y
      have he := (hp y (A.operator y) ⟨y,rfl⟩).symm
      rwa [←hs] at he
    obtain ⟨hy,hyval⟩:=scalarTomitaAdjoint_maximal A hh
    let w:scalarTomitaSquareDomain A:=⟨v,v.property,hy⟩
    apply (LinearPMap.mem_graph_iff (scalarTomitaSquare A)).mpr
    exact ⟨w,hx,hyval⟩
  · intro hp
    obtain ⟨w,hx,hz⟩:=(LinearPMap.mem_graph_iff (scalarTomitaSquare A)).mp hp
    refine ⟨A.operator (scalarTomitaSquareInput A w),?_,?_⟩
    · exact ⟨scalarTomitaSquareInput A w,Prod.ext hx rfl⟩
    · intro y sy hy
      obtain ⟨v,hv⟩:=hy
      have hyv:(v:H)=y:=congrArg Prod.fst hv
      have hsy:A.operator v=sy:=congrArg Prod.snd hv
      have he:=scalarTomitaSquare_pairing A w v
      rwa [hz,hyv,hsy] at he

theorem resolvent_mem (x:H) :
    (scalarTomitaResolvent A x,x-scalarTomitaResolvent A x)∈antilinearSquareGraph (graph A) := by
  rw [square_graph]
  obtain ⟨u,hu,he⟩:=scalarTomitaResolvent_equation A x
  apply (LinearPMap.mem_graph_iff (scalarTomitaSquare A)).mpr
  refine ⟨u,hu,?_⟩
  rw [hu] at he
  exact eq_sub_of_add_eq' he

theorem resolvent_inverse (x y:H) (hxy:(x,y)∈antilinearSquareGraph (graph A)) :
    scalarTomitaResolvent A (x+y)=x := by
  rw [square_graph] at hxy
  obtain ⟨u,hu,hv⟩:=(LinearPMap.mem_graph_iff (scalarTomitaSquare A)).mp hxy
  have he:=scalarTomitaResolvent_inverse A u
  rwa [hu,hv] at he
end F1Fecho.ClosedTomitaSquareGraph
#print axioms F1Fecho.ClosedTomitaSquareGraph.square_graph
#print axioms F1Fecho.ClosedTomitaSquareGraph.resolvent_mem
#print axioms F1Fecho.ClosedTomitaSquareGraph.resolvent_inverse
