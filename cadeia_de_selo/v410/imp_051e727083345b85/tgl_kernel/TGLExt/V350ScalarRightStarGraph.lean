import TGLExt.V350ScalarHomogeneousRightGNS
import TGLExt.V350ScalarWeightTomitaIdentification

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory
noncomputable section

def homogeneousRightCoreElement {P : SiteProfile} (d : HomogeneousRightData P) :
    (regularCoreAlgebra P).toStarSubalgebra :=
  ⟨fibre d.left,amplified_factor_mem P d.left d.left_mem⟩

def scalarWeightStarRightProduct {P : SiteProfile} (d : HomogeneousRightData P)
    (A : scalarWeightStarCore P) : scalarWeightStarCore P :=
  ⟨A.val * homogeneousRightCoreElement d,
    scalarWeight_right_homogeneous_finite P d.right d.left d.frequency
      d.right_mem d.homogeneous d.vacuum ⟨A.val,A.property.1⟩,
    by
      change HasFiniteScalarSquare P (star (A.val.val * fibre d.left))
      rw [star_mul]
      exact HasFiniteScalarSquare.left_mul P _ _ A.property.2⟩

theorem scalarWeightStarRight_embedding {P : SiteProfile} (d : HomogeneousRightData P)
    (A : scalarWeightStarCore P) :
    scalarWeightStarEmbedding P (scalarWeightStarRightProduct d A) =
      homogeneousRightGNS d (scalarWeightStarEmbedding P A) :=
  (homogeneousRightGNS_intertwines d ⟨A.val,A.property.1⟩).symm

theorem scalarWeightStarRight_star_embedding {P : SiteProfile} (d : HomogeneousRightData P)
    (A : scalarWeightStarCore P) :
    scalarWeightStarEmbedding P (star (scalarWeightStarRightProduct d A)) =
      scalarGNSRepresentation P (star (homogeneousRightCoreElement d))
        (scalarWeightStarEmbedding P (star A)) := by
  have hi := scalarWeightGNSAction_intertwines P (star (homogeneousRightCoreElement d))
    ⟨(star A).val,(star A).property.1⟩
  apply Eq.trans ?_ hi.symm
  apply congrArg (scalarWeightGNSEmbedding P)
  apply Subtype.ext
  apply Subtype.ext
  change star (A.val.val * fibre d.left) = star (fibre d.left) * star A.val.val
  exact star_mul _ _

/-- Both graph coordinates are transported by bounded operators on the
same GNS. The second coordinate is left multiplication by the actual y*. -/
def homogeneousRightGraphMap {P : SiteProfile} (d : HomogeneousRightData P)
    (p : ScalarGNSHilbert P × ScalarGNSHilbert P) :
    ScalarGNSHilbert P × ScalarGNSHilbert P :=
  (homogeneousRightGNS d p.1,
    scalarGNSRepresentation P (star (homogeneousRightCoreElement d)) p.2)

theorem homogeneousRightGraphMap_continuous {P : SiteProfile} (d : HomogeneousRightData P) :
    Continuous (homogeneousRightGraphMap d) :=
  ((homogeneousRightGNS d).continuous.comp continuous_fst).prodMk
    ((scalarGNSRepresentation P (star (homogeneousRightCoreElement d))).continuous.comp continuous_snd)

theorem homogeneousRightGraphMap_preserves_weight_graph {P : SiteProfile}
    (d : HomogeneousRightData P) :
    Set.MapsTo (homogeneousRightGraphMap d) (scalarWeightTomitaGraph P)
      (scalarWeightTomitaGraph P) := by
  rintro p ⟨A,rfl⟩
  refine ⟨scalarWeightStarRightProduct d A,?_⟩
  exact Prod.ext (scalarWeightStarRight_embedding d A)
    (scalarWeightStarRight_star_embedding d A)

#print axioms homogeneousRightCoreElement
#print axioms scalarWeightStarRightProduct
#print axioms scalarWeightStarRight_embedding
#print axioms scalarWeightStarRight_star_embedding
#print axioms homogeneousRightGraphMap
#print axioms homogeneousRightGraphMap_continuous
#print axioms homogeneousRightGraphMap_preserves_weight_graph
end
end TGLV350.Regular
