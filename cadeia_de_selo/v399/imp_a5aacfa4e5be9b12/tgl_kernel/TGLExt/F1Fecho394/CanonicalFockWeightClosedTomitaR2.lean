import TGLExt.F1Fecho394.RegularScalarClosedTomitaR1
import TGLExt.F1Fecho394.CanonicalFockWeightStarDensityR2
/-! Closed densely defined antilinear involution for the scalar dual weight
of the same regular Fock core. This is the graph closure of Lambda(A) ->
Lambda(A*); no equality with the geometric modular group or scaled trace
is assumed or concluded. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightClosedTomita
open F1Fecho.CanonicalFockGNS F1Fecho.RegularScalarGNS
open F1Fecho.RegularScalarTomitaGraph F1Fecho.RegularScalarClosedTomita

abbrev closedTomitaDomain := scalarClosedTomitaDomain weightContext
abbrev closedTomita := scalarClosedTomita weightContext

theorem domain_dense : Dense (closedTomitaDomain : Set (F1Fecho.CanonicalFockGNS.GNSHilbert)) := by
  apply Dense.mono ?_ F1Fecho.CanonicalFockWeightStarDensity.scalarTomitaGraph_domain_dense
  rintro x ⟨p,hp,rfl⟩
  exact ⟨p.2,subset_closure hp⟩

theorem graph_eq :
    Set.range (fun x : closedTomitaDomain =>
      ((x : F1Fecho.CanonicalFockGNS.GNSHilbert),closedTomita x)) =
      closure (scalarTomitaGraph weightContext) :=
  scalarClosedTomita_graph_eq

theorem graph_closed : IsClosed (Set.range (fun x : closedTomitaDomain =>
    ((x : F1Fecho.CanonicalFockGNS.GNSHilbert),closedTomita x))) :=
  scalarClosedTomita_is_closed

theorem maps_domain (x : closedTomitaDomain) : closedTomita x ∈ closedTomitaDomain :=
  scalarClosedTomita_maps_domain x

theorem involutive (x : closedTomitaDomain) :
    closedTomita ⟨closedTomita x,maps_domain x⟩ = x :=
  scalarClosedTomita_involutive x

theorem extends_star (A : finiteStarCore weightContext) :
    closedTomita ⟨scalarGNSStarEmbedding weightContext A,
      scalarStarCore_mem_closedTomitaDomain A⟩ = scalarGNSStarEmbedding weightContext (star A) :=
  scalarClosedTomita_extends_star A

end F1Fecho.CanonicalFockWeightClosedTomita
#print axioms F1Fecho.CanonicalFockWeightClosedTomita.closedTomitaDomain
#print axioms F1Fecho.CanonicalFockWeightClosedTomita.closedTomita
#print axioms F1Fecho.CanonicalFockWeightClosedTomita.domain_dense
#print axioms F1Fecho.CanonicalFockWeightClosedTomita.graph_eq
#print axioms F1Fecho.CanonicalFockWeightClosedTomita.graph_closed
#print axioms F1Fecho.CanonicalFockWeightClosedTomita.maps_domain
#print axioms F1Fecho.CanonicalFockWeightClosedTomita.involutive
#print axioms F1Fecho.CanonicalFockWeightClosedTomita.extends_star
