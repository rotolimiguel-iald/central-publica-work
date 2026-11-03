import TGLExt.V350ScalarTomitaResolvent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable (P : SiteProfile)

theorem scalarTomitaResolvent_memDomain (z : ScalarGNSHilbert P) :
    scalarTomitaResolvent P z ∈ scalarClosedTomitaDomain P := by
  obtain ⟨u,hu,_⟩ := scalarTomitaResolvent_equation P z
  rw [← hu]
  exact (scalarTomitaSquareInput P u).property

/-- The actual resolvent is exchanged with its complement by S on D(S).
This bounded-resolvent identity does not by itself supply the square-root flip. -/
theorem scalarTomitaResolvent_flip (x : scalarClosedTomitaDomain P) :
    scalarClosedTomita P ⟨scalarTomitaResolvent P (x : ScalarGNSHilbert P),
      scalarTomitaResolvent_memDomain P (x : ScalarGNSHilbert P)⟩ =
        scalarClosedTomita P x - scalarTomitaResolvent P (scalarClosedTomita P x) := by
  obtain ⟨u,hu,hueq⟩ := scalarTomitaResolvent_equation P (x : ScalarGNSHilbert P)
  let uS := scalarTomitaSquareInput P u
  let w : scalarClosedTomitaDomain P := x-uS
  have hw : (w : ScalarGNSHilbert P)=scalarTomitaSquare P u := by
    change (x : ScalarGNSHilbert P)-(u : ScalarGNSHilbert P)=scalarTomitaSquare P u
    rw [← hueq]
    abel
  have hwAdj : (w : ScalarGNSHilbert P) ∈ scalarTomitaAdjointDomain P := by
    rw [hw]
    exact scalarTomitaAdjoint_maps_domain P (scalarTomitaSquareAdjointInput P u)
  let v : scalarClosedTomitaDomain P :=
    ⟨scalarClosedTomita P w,scalarClosedTomita_maps_domain w⟩
  have hvS : scalarClosedTomita P v=(w : ScalarGNSHilbert P) :=
    scalarClosedTomita_involutive w
  have hvAdj : scalarClosedTomita P v ∈ scalarTomitaAdjointDomain P := by
    rw [hvS]
    exact hwAdj
  let vA : scalarTomitaSquareDomain P := ⟨(v : ScalarGNSHilbert P),⟨v.property,hvAdj⟩⟩
  have hAv : scalarTomitaSquare P vA=scalarClosedTomita P uS := by
    have he : scalarTomitaSquareAdjointInput P vA =
        ⟨scalarTomitaAdjoint P (scalarTomitaSquareAdjointInput P u),
          scalarTomitaAdjoint_maps_domain P (scalarTomitaSquareAdjointInput P u)⟩ :=
      Subtype.ext (hvS.trans hw)
    change scalarTomitaAdjoint P (scalarTomitaSquareAdjointInput P vA)=_
    rw [he]
    exact scalarTomitaAdjoint_involutive P (scalarTomitaSquareAdjointInput P u)
  have hveq : (vA : ScalarGNSHilbert P)+scalarTomitaSquare P vA=scalarClosedTomita P x := by
    calc
      _ = scalarClosedTomita P w + scalarClosedTomita P uS :=
        congrArg (fun y => (vA : ScalarGNSHilbert P)+y) hAv
      _ = scalarClosedTomita P (w+uS) := ((scalarClosedTomita P).map_add w uS).symm
      _ = scalarClosedTomita P x := congrArg (scalarClosedTomita P) (sub_add_cancel x uS)
  have hr : scalarTomitaResolvent P (scalarClosedTomita P x)=scalarClosedTomita P w := by
    calc
      _ = scalarTomitaResolvent P ((vA : ScalarGNSHilbert P)+scalarTomitaSquare P vA) :=
        congrArg (scalarTomitaResolvent P) hveq.symm
      _ = (vA : ScalarGNSHilbert P) := scalarTomitaResolvent_inverse P vA
  have he : (⟨scalarTomitaResolvent P (x : ScalarGNSHilbert P),
      scalarTomitaResolvent_memDomain P (x : ScalarGNSHilbert P)⟩ : scalarClosedTomitaDomain P)=uS :=
    Subtype.ext hu.symm
  rw [he,hr]
  change scalarClosedTomita P uS=scalarClosedTomita P x-scalarClosedTomita P (x-uS)
  rw [map_sub]
  abel

#print axioms scalarTomitaResolvent_memDomain
#print axioms scalarTomitaResolvent_flip
end
end TGLV350.Regular
