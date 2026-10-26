import TGLExt.V350ScalarRightTomitaAdjoint
import TGLExt.V350ScalarTomitaSquare

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

theorem scalarRightSquare_S_image {P : SiteProfile}
    (d e : HomogeneousRightData P)
    (he : homogeneousRightCoreElement e = star (homogeneousRightCoreElement d))
    (x : scalarTomitaSquareDomain P) :
    scalarClosedTomita P (scalarRightClosedTomitaInput d (scalarTomitaSquareInput P x)) =
      scalarGNSRepresentation P (homogeneousRightCoreElement e)
        (scalarTomitaSquareAdjointInput P x : ScalarGNSHilbert P) := by
  rw [scalarClosedTomita_right_intertwines,he]
  rfl

/-- Right multiplication preserves the actual composition domain, provided
the algebraic adjoint has its own homogeneous right data. -/
theorem scalarRight_mem_squareDomain {P : SiteProfile}
    (d e : HomogeneousRightData P)
    (he : homogeneousRightCoreElement e = star (homogeneousRightCoreElement d))
    (x : scalarTomitaSquareDomain P) :
    homogeneousRightGNS d (x : ScalarGNSHilbert P) ∈ scalarTomitaSquareDomain P := by
  refine ⟨scalarRight_mem_closedTomitaDomain d (scalarTomitaSquareInput P x),?_⟩
  change scalarClosedTomita P
    (scalarRightClosedTomitaInput d (scalarTomitaSquareInput P x)) ∈ scalarTomitaAdjointDomain P
  rw [scalarRightSquare_S_image d e he x]
  exact (scalarRightTomitaAdjointInput e (scalarTomitaSquareAdjointInput P x)).property

def scalarRightSquareInput {P : SiteProfile}
    (d e : HomogeneousRightData P)
    (he : homogeneousRightCoreElement e = star (homogeneousRightCoreElement d))
    (x : scalarTomitaSquareDomain P) : scalarTomitaSquareDomain P :=
  ⟨homogeneousRightGNS d (x : ScalarGNSHilbert P),scalarRight_mem_squareDomain d e he x⟩

/-- Equality for A=S†S on its complete domain, not only algebraic vectors. -/
theorem scalarTomitaSquare_right_intertwines {P : SiteProfile}
    (d e : HomogeneousRightData P)
    (he : homogeneousRightCoreElement e = star (homogeneousRightCoreElement d))
    (x : scalarTomitaSquareDomain P) :
    scalarTomitaSquare P (scalarRightSquareInput d e he x) =
      star (homogeneousRightGNS e) (scalarTomitaSquare P x) := by
  have hi : scalarTomitaSquareAdjointInput P (scalarRightSquareInput d e he x) =
      scalarRightTomitaAdjointInput e (scalarTomitaSquareAdjointInput P x) := by
    apply Subtype.ext
    exact scalarRightSquare_S_image d e he x
  calc
    _ = scalarTomitaAdjoint P
        (scalarTomitaSquareAdjointInput P (scalarRightSquareInput d e he x)) := rfl
    _ = scalarTomitaAdjoint P
        (scalarRightTomitaAdjointInput e (scalarTomitaSquareAdjointInput P x)) :=
      congrArg (scalarTomitaAdjoint P) hi
    _ = star (homogeneousRightGNS e)
        (scalarTomitaAdjoint P (scalarTomitaSquareAdjointInput P x)) :=
      scalarTomitaAdjoint_left_intertwines e (scalarTomitaSquareAdjointInput P x)
    _ = _ := rfl

#print axioms scalarRightSquare_S_image
#print axioms scalarRight_mem_squareDomain
#print axioms scalarRightSquareInput
#print axioms scalarTomitaSquare_right_intertwines
end
end TGLV350.Regular
