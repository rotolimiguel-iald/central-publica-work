import TGLExt.V350ScalarRegularRightGNS
import TGLExt.V350ScalarWeightTomitaIdentification

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory
noncomputable section

def scalarWeightStarRegularRightProduct (P : SiteProfile) (t : ℝ)
    (A : scalarWeightStarCore P) : scalarWeightStarCore P :=
  ⟨A.val * regularRightCoreElement P t,
    (scalarRegularRightProduct P t ⟨A.val,A.property.1⟩).property,
    by
      change HasFiniteScalarSquare P (star (A.val.val * regularUnitary P t))
      rw [star_mul]
      exact HasFiniteScalarSquare.left_mul P _ _ A.property.2⟩

theorem scalarWeightStarRegularRight_embedding (P : SiteProfile) (t : ℝ)
    (A : scalarWeightStarCore P) :
    scalarWeightStarEmbedding P (scalarWeightStarRegularRightProduct P t A) =
      regularRightGNS P t (scalarWeightStarEmbedding P A) :=
  (regularRightGNS_intertwines P t ⟨A.val,A.property.1⟩).symm

theorem scalarWeightStarRegularRight_star_embedding (P : SiteProfile) (t : ℝ)
    (A : scalarWeightStarCore P) :
    scalarWeightStarEmbedding P (star (scalarWeightStarRegularRightProduct P t A)) =
      scalarGNSRepresentation P (star (regularRightCoreElement P t))
        (scalarWeightStarEmbedding P (star A)) := by
  have hi := scalarWeightGNSAction_intertwines P (star (regularRightCoreElement P t))
    ⟨(star A).val,(star A).property.1⟩
  apply Eq.trans ?_ hi.symm
  apply congrArg (scalarWeightGNSEmbedding P)
  apply Subtype.ext
  apply Subtype.ext
  exact star_mul _ _

def regularRightGraphMap (P : SiteProfile) (t : ℝ)
    (p : ScalarGNSHilbert P × ScalarGNSHilbert P) :
    ScalarGNSHilbert P × ScalarGNSHilbert P :=
  (regularRightGNS P t p.1,
    scalarGNSRepresentation P (star (regularRightCoreElement P t)) p.2)

theorem regularRightGraphMap_continuous (P : SiteProfile) (t : ℝ) :
    Continuous (regularRightGraphMap P t) :=
  ((regularRightGNS P t).continuous.comp continuous_fst).prodMk
    ((scalarGNSRepresentation P (star (regularRightCoreElement P t))).continuous.comp continuous_snd)

theorem regularRightGraphMap_preserves_weight_graph (P : SiteProfile) (t : ℝ) :
    Set.MapsTo (regularRightGraphMap P t) (scalarWeightTomitaGraph P)
      (scalarWeightTomitaGraph P) := by
  rintro p ⟨A,rfl⟩
  refine ⟨scalarWeightStarRegularRightProduct P t A,?_⟩
  exact Prod.ext (scalarWeightStarRegularRight_embedding P t A)
    (scalarWeightStarRegularRight_star_embedding P t A)

theorem regularRightGraphMap_preserves_closed_graph (P : SiteProfile) (t : ℝ) :
    Set.MapsTo (regularRightGraphMap P t) (closure (scalarTomitaGraph P))
      (closure (scalarTomitaGraph P)) := by
  have h := (regularRightGraphMap_preserves_weight_graph P t).closure
    (regularRightGraphMap_continuous P t)
  simpa only [scalarWeightTomitaGraph_closure_eq] using h

theorem scalarRegularRight_mem_closedTomitaDomain (P : SiteProfile) (t : ℝ)
    (x : scalarClosedTomitaDomain P) :
    regularRightGNS P t (x : ScalarGNSHilbert P) ∈ scalarClosedTomitaDomain P :=
  ⟨scalarGNSRepresentation P (star (regularRightCoreElement P t)) (scalarClosedTomita P x),
    regularRightGraphMap_preserves_closed_graph P t (scalarClosedTomita_graph x)⟩

def scalarRegularRightClosedTomitaInput (P : SiteProfile) (t : ℝ)
    (x : scalarClosedTomitaDomain P) : scalarClosedTomitaDomain P :=
  ⟨regularRightGNS P t (x : ScalarGNSHilbert P),scalarRegularRight_mem_closedTomitaDomain P t x⟩

/-- The actual closed S intertwines right multiplication by lambda_t with
left multiplication by lambda_t*. The identity holds on its full domain. -/
theorem scalarClosedTomita_regular_right_intertwines (P : SiteProfile) (t : ℝ)
    (x : scalarClosedTomitaDomain P) :
    scalarClosedTomita P (scalarRegularRightClosedTomitaInput P t x) =
      scalarGNSRepresentation P (star (regularRightCoreElement P t)) (scalarClosedTomita P x) :=
  scalarTomitaGraph_closure_single_valued P (regularRightGNS P t (x : ScalarGNSHilbert P)) _ _
    (scalarClosedTomita_graph (scalarRegularRightClosedTomitaInput P t x))
    (regularRightGraphMap_preserves_closed_graph P t (scalarClosedTomita_graph x))

#print axioms scalarWeightStarRegularRightProduct
#print axioms scalarWeightStarRegularRight_embedding
#print axioms scalarWeightStarRegularRight_star_embedding
#print axioms regularRightGraphMap
#print axioms regularRightGraphMap_continuous
#print axioms regularRightGraphMap_preserves_weight_graph
#print axioms regularRightGraphMap_preserves_closed_graph
#print axioms scalarRegularRight_mem_closedTomitaDomain
#print axioms scalarRegularRightClosedTomitaInput
#print axioms scalarClosedTomita_regular_right_intertwines
end
end TGLV350.Regular
