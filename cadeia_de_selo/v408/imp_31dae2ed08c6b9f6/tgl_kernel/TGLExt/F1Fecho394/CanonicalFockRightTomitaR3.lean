import TGLExt.F1Fecho394.GenericFiniteStarRightR1
import TGLExt.F1Fecho394.CanonicalFockRegularRightGNSR11
import TGLExt.F1Fecho394.CanonicalFockFullWeightTomitaR5
/-! Actual regular right multiplication preserves the full closed Tomita graph
on the existing Fock weight GNS. No modular identity is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockRightTomita
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockRegularRightGNS F1Fecho.CanonicalFockWeightSandwich
open F1Fecho.CanonicalFockFullWeightStarCore F1Fecho.CanonicalFockFullWeightTomita
open F1Fecho.CanonicalFockWeightClosedTomita
open scoped Topology
def scalarWeightStarRegularRightProduct  (t : ℝ)
    (A : scalarWeightStarCore ) : scalarWeightStarCore  :=
  F1Fecho.GenericFiniteStarRight.product weightContext A (regularRightCoreElement t)
    (scalarRegularRightProduct t ⟨A.val,A.property.1⟩).property

theorem scalarWeightStarRegularRight_embedding  (t : ℝ)
    (A : scalarWeightStarCore ) :
    scalarWeightStarEmbedding  (scalarWeightStarRegularRightProduct  t A) =
      regularRightGNS  t (scalarWeightStarEmbedding  A) :=
  (regularRightGNS_intertwines  t ⟨A.val,A.property.1⟩).symm

theorem scalarWeightStarRegularRight_star_embedding  (t : ℝ)
    (A : scalarWeightStarCore ) :
    scalarWeightStarEmbedding  (star (scalarWeightStarRegularRightProduct  t A)) =
      scalarGNSRepresentation  (star (regularRightCoreElement  t))
        (scalarWeightStarEmbedding  (star A)) := by
  have hi := scalarWeightGNSAction_intertwines  (star (regularRightCoreElement  t))
    ⟨(star A).val,(star A).property.1⟩
  apply Eq.trans ?_ hi.symm
  apply congrArg (scalarWeightGNSEmbedding )
  apply Subtype.ext
  apply Subtype.ext
  have he : star (A.val * (⟨regularUnitary t,regular_mem t⟩ : weightContext.algebra.toStarSubalgebra)) =
    star (⟨regularUnitary t,regular_mem t⟩ : weightContext.algebra.toStarSubalgebra) * star A.val :=
    star_mul A.val (⟨regularUnitary t,regular_mem t⟩ : weightContext.algebra.toStarSubalgebra)
  exact congrArg Subtype.val he

def regularRightGraphMap  (t : ℝ)
    (p : GNSHilbert × GNSHilbert) :
    GNSHilbert × GNSHilbert :=
  (regularRightGNS  t p.1,
    scalarGNSRepresentation  (star (regularRightCoreElement  t)) p.2)

theorem regularRightGraphMap_continuous  (t : ℝ) :
    Continuous (regularRightGraphMap  t) :=
  ((regularRightGNS  t).continuous.comp continuous_fst).prodMk
    ((scalarGNSRepresentation  (star (regularRightCoreElement  t))).continuous.comp continuous_snd)

theorem regularRightGraphMap_preserves_weight_graph  (t : ℝ) :
    Set.MapsTo (regularRightGraphMap  t) (scalarWeightTomitaGraph )
      (scalarWeightTomitaGraph ) := by
  rintro p ⟨A,rfl⟩
  refine ⟨scalarWeightStarRegularRightProduct  t A,?_⟩
  exact Prod.ext (scalarWeightStarRegularRight_embedding  t A)
    (scalarWeightStarRegularRight_star_embedding  t A)

theorem regularRightGraphMap_preserves_closed_graph  (t : ℝ) :
    Set.MapsTo (regularRightGraphMap  t) (closure (F1Fecho.RegularScalarTomitaGraph.scalarTomitaGraph weightContext))
      (closure (F1Fecho.RegularScalarTomitaGraph.scalarTomitaGraph weightContext)) := by
  have h := (regularRightGraphMap_preserves_weight_graph  t).closure
    (regularRightGraphMap_continuous  t)
  simpa only [scalarWeightTomitaGraph_closure_eq] using h

theorem scalarRegularRight_mem_closedTomitaDomain  (t : ℝ)
    (x : closedTomitaDomain) :
    regularRightGNS  t (x : GNSHilbert) ∈ closedTomitaDomain :=
  ⟨scalarGNSRepresentation  (star (regularRightCoreElement  t)) (closedTomita x),
    regularRightGraphMap_preserves_closed_graph  t (F1Fecho.RegularScalarClosedTomita.scalarClosedTomita_graph (H := F) (D := weightContext) x)⟩

def scalarRegularRightClosedTomitaInput  (t : ℝ)
    (x : closedTomitaDomain) : closedTomitaDomain :=
  ⟨regularRightGNS  t (x : GNSHilbert),scalarRegularRight_mem_closedTomitaDomain  t x⟩

/-- The actual closed S intertwines right multiplication by lambda_t with
left multiplication by lambda_t*. The identity holds on its full domain. -/
theorem scalarClosedTomita_regular_right_intertwines  (t : ℝ)
    (x : closedTomitaDomain) :
    closedTomita (scalarRegularRightClosedTomitaInput  t x) =
      scalarGNSRepresentation  (star (regularRightCoreElement  t)) (closedTomita x) :=
  F1Fecho.RegularScalarTomitaClosure.scalarTomitaGraph_closure_single_valued (H := F) weightContext (regularRightGNS  t (x : GNSHilbert)) _ _
    (F1Fecho.RegularScalarClosedTomita.scalarClosedTomita_graph (H := F) (D := weightContext) (scalarRegularRightClosedTomitaInput  t x))
    (regularRightGraphMap_preserves_closed_graph  t (F1Fecho.RegularScalarClosedTomita.scalarClosedTomita_graph (H := F) (D := weightContext) x))


end F1Fecho.CanonicalFockRightTomita
#print axioms F1Fecho.CanonicalFockRightTomita.scalarWeightStarRegularRightProduct
#print axioms F1Fecho.CanonicalFockRightTomita.scalarWeightStarRegularRight_embedding
#print axioms F1Fecho.CanonicalFockRightTomita.scalarWeightStarRegularRight_star_embedding
#print axioms F1Fecho.CanonicalFockRightTomita.regularRightGraphMap
#print axioms F1Fecho.CanonicalFockRightTomita.regularRightGraphMap_continuous
#print axioms F1Fecho.CanonicalFockRightTomita.regularRightGraphMap_preserves_weight_graph
#print axioms F1Fecho.CanonicalFockRightTomita.regularRightGraphMap_preserves_closed_graph
#print axioms F1Fecho.CanonicalFockRightTomita.scalarRegularRight_mem_closedTomitaDomain
#print axioms F1Fecho.CanonicalFockRightTomita.scalarRegularRightClosedTomitaInput
#print axioms F1Fecho.CanonicalFockRightTomita.scalarClosedTomita_regular_right_intertwines
