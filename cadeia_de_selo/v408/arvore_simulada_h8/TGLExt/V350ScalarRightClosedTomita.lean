import TGLExt.V350ScalarRightStarGraph

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

theorem homogeneousRightGraphMap_preserves_closed_graph {P : SiteProfile}
    (d : HomogeneousRightData P) :
    Set.MapsTo (homogeneousRightGraphMap d) (closure (scalarTomitaGraph P))
      (closure (scalarTomitaGraph P)) := by
  have h := (homogeneousRightGraphMap_preserves_weight_graph d).closure
    (homogeneousRightGraphMap_continuous d)
  simpa only [scalarWeightTomitaGraph_closure_eq] using h

theorem scalarRight_mem_closedTomitaDomain {P : SiteProfile}
    (d : HomogeneousRightData P) (x : scalarClosedTomitaDomain P) :
    homogeneousRightGNS d (x : ScalarGNSHilbert P) ∈ scalarClosedTomitaDomain P :=
  ⟨scalarGNSRepresentation P (star (homogeneousRightCoreElement d)) (scalarClosedTomita P x),
    homogeneousRightGraphMap_preserves_closed_graph d (scalarClosedTomita_graph x)⟩

def scalarRightClosedTomitaInput {P : SiteProfile}
    (d : HomogeneousRightData P) (x : scalarClosedTomitaDomain P) : scalarClosedTomitaDomain P :=
  ⟨homogeneousRightGNS d (x : ScalarGNSHilbert P),scalarRight_mem_closedTomitaDomain d x⟩

/-- Domain invariance and an equality for the same closed S: S R_y = π(y*) S
on D(S). No KMS analytic extension or identification of S†S is assumed. -/
theorem scalarClosedTomita_right_intertwines {P : SiteProfile}
    (d : HomogeneousRightData P) (x : scalarClosedTomitaDomain P) :
    scalarClosedTomita P (scalarRightClosedTomitaInput d x) =
      scalarGNSRepresentation P (star (homogeneousRightCoreElement d)) (scalarClosedTomita P x) :=
  scalarTomitaGraph_closure_single_valued P
    (homogeneousRightGNS d (x : ScalarGNSHilbert P)) _ _
    (scalarClosedTomita_graph (scalarRightClosedTomitaInput d x))
    (homogeneousRightGraphMap_preserves_closed_graph d (scalarClosedTomita_graph x))

theorem matrixUnit_closedTomita_right_intertwines (P : SiteProfile) (N : ℕ) (i j : chainIdx N)
    (x : scalarClosedTomitaDomain P) :
    scalarClosedTomita P (scalarRightClosedTomitaInput (matrixUnitRightData P N i j) x) =
      scalarGNSRepresentation P (star (homogeneousRightCoreElement (matrixUnitRightData P N i j)))
        (scalarClosedTomita P x) :=
  scalarClosedTomita_right_intertwines _ x

#print axioms homogeneousRightGraphMap_preserves_closed_graph
#print axioms scalarRight_mem_closedTomitaDomain
#print axioms scalarRightClosedTomitaInput
#print axioms scalarClosedTomita_right_intertwines
#print axioms matrixUnit_closedTomita_right_intertwines
end
end TGLV350.Regular
