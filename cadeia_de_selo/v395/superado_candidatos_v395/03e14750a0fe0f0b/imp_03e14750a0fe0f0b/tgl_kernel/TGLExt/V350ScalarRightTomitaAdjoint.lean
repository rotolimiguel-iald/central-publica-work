import TGLExt.V350ScalarRightClosedTomita
import TGLExt.V350ScalarTomitaAdjoint

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

/-- The closed-S intertwining determines a relation for its maximal adjoint.
The left operator is pi(y), while the right operator is the Hilbert adjoint
of R_y. This uses every vector in D(S), not only the algebraic core. -/
theorem scalarRightTomitaAdjoint_pairing {P : SiteProfile}
    (d : HomogeneousRightData P) (z : scalarTomitaAdjointDomain P)
    (x : scalarClosedTomitaDomain P) :
    inner ℂ (scalarClosedTomita P x)
      (scalarGNSRepresentation P (homogeneousRightCoreElement d) z) =
    inner ℂ (star (homogeneousRightGNS d) (scalarTomitaAdjoint P z))
      (x : ScalarGNSHilbert P) := by
  have hp : (scalarGNSRepresentation P (homogeneousRightCoreElement d)).adjoint =
      scalarGNSRepresentation P (star (homogeneousRightCoreElement d)) :=
    (map_star (scalarGNSRepresentation P) (homogeneousRightCoreElement d)).symm
  calc
    _ = inner ℂ
        ((scalarGNSRepresentation P (homogeneousRightCoreElement d)).adjoint
          (scalarClosedTomita P x)) (z : ScalarGNSHilbert P) :=
      ((scalarGNSRepresentation P (homogeneousRightCoreElement d)).adjoint_inner_left _ _).symm
    _ = inner ℂ
        (scalarGNSRepresentation P (star (homogeneousRightCoreElement d))
          (scalarClosedTomita P x)) (z : ScalarGNSHilbert P) :=
      congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
        inner ℂ (T (scalarClosedTomita P x)) (z : ScalarGNSHilbert P)) hp
    _ = inner ℂ (scalarClosedTomita P (scalarRightClosedTomitaInput d x))
        (z : ScalarGNSHilbert P) :=
      congrArg (fun v : ScalarGNSHilbert P => inner ℂ v (z : ScalarGNSHilbert P))
        (scalarClosedTomita_right_intertwines d x).symm
    _ = inner ℂ (scalarTomitaAdjoint P z)
        (homogeneousRightGNS d (x : ScalarGNSHilbert P)) :=
      scalarTomitaAdjoint_pairing P z (scalarRightClosedTomitaInput d x)
    _ = _ := ((homogeneousRightGNS d).adjoint_inner_left _ _).symm

theorem scalarRightTomitaAdjoint_maximal {P : SiteProfile}
    (d : HomogeneousRightData P) (z : scalarTomitaAdjointDomain P) :
    ∃ hz : scalarGNSRepresentation P (homogeneousRightCoreElement d) z ∈
        scalarTomitaAdjointDomain P,
      scalarTomitaAdjoint P
        ⟨scalarGNSRepresentation P (homogeneousRightCoreElement d) z,hz⟩ =
      star (homogeneousRightGNS d) (scalarTomitaAdjoint P z) :=
  scalarTomitaAdjoint_maximal P (scalarRightTomitaAdjoint_pairing d z)

def scalarRightTomitaAdjointInput {P : SiteProfile}
    (d : HomogeneousRightData P) (z : scalarTomitaAdjointDomain P) :
    scalarTomitaAdjointDomain P :=
  ⟨scalarGNSRepresentation P (homogeneousRightCoreElement d) z,
    (scalarRightTomitaAdjoint_maximal d z).choose⟩

theorem scalarTomitaAdjoint_left_intertwines {P : SiteProfile}
    (d : HomogeneousRightData P) (z : scalarTomitaAdjointDomain P) :
    scalarTomitaAdjoint P (scalarRightTomitaAdjointInput d z) =
      star (homogeneousRightGNS d) (scalarTomitaAdjoint P z) :=
  (scalarRightTomitaAdjoint_maximal d z).choose_spec

theorem matrixUnit_TomitaAdjoint_left_intertwines (P : SiteProfile)
    (N : ℕ) (i j : chainIdx N) (z : scalarTomitaAdjointDomain P) :
    scalarTomitaAdjoint P
        (scalarRightTomitaAdjointInput (matrixUnitRightData P N i j) z) =
      homogeneousRightGNS (matrixUnitTwistedRightData P N i j)
        (scalarTomitaAdjoint P z) := by
  rw [scalarTomitaAdjoint_left_intertwines,matrixUnitRightGNS_adjoint]

#print axioms scalarRightTomitaAdjoint_pairing
#print axioms scalarRightTomitaAdjoint_maximal
#print axioms scalarRightTomitaAdjointInput
#print axioms scalarTomitaAdjoint_left_intertwines
#print axioms matrixUnit_TomitaAdjoint_left_intertwines
end
end TGLV350.Regular
