import TGLExt.V350ScalarRegularRightTomita
import TGLExt.V350ScalarTomitaAdjoint
import TGLExt.V350ScalarTomitaSquare

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

/-- The closed-S intertwining determines a relation for its maximal adjoint.
The left operator is pi(y), while the right operator is the Hilbert adjoint
of R_y. This uses every vector in D(S), not only the algebraic core. -/
theorem scalarRegularRightTomitaAdjoint_pairing (P : SiteProfile) (t : ℝ) (z : scalarTomitaAdjointDomain P)
    (x : scalarClosedTomitaDomain P) :
    inner ℂ (scalarClosedTomita P x)
      (scalarGNSRepresentation P (regularRightCoreElement P t) z) =
    inner ℂ (star (regularRightGNS P t) (scalarTomitaAdjoint P z))
      (x : ScalarGNSHilbert P) := by
  have hp : (scalarGNSRepresentation P (regularRightCoreElement P t)).adjoint =
      scalarGNSRepresentation P (star (regularRightCoreElement P t)) :=
    (map_star (scalarGNSRepresentation P) (regularRightCoreElement P t)).symm
  calc
    _ = inner ℂ
        ((scalarGNSRepresentation P (regularRightCoreElement P t)).adjoint
          (scalarClosedTomita P x)) (z : ScalarGNSHilbert P) :=
      ((scalarGNSRepresentation P (regularRightCoreElement P t)).adjoint_inner_left _ _).symm
    _ = inner ℂ
        (scalarGNSRepresentation P (star (regularRightCoreElement P t))
          (scalarClosedTomita P x)) (z : ScalarGNSHilbert P) :=
      congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
        inner ℂ (T (scalarClosedTomita P x)) (z : ScalarGNSHilbert P)) hp
    _ = inner ℂ (scalarClosedTomita P (scalarRegularRightClosedTomitaInput P t x))
        (z : ScalarGNSHilbert P) :=
      congrArg (fun v : ScalarGNSHilbert P => inner ℂ v (z : ScalarGNSHilbert P))
        (scalarClosedTomita_regular_right_intertwines P t x).symm
    _ = inner ℂ (scalarTomitaAdjoint P z)
        (regularRightGNS P t (x : ScalarGNSHilbert P)) :=
      scalarTomitaAdjoint_pairing P z (scalarRegularRightClosedTomitaInput P t x)
    _ = _ := ((regularRightGNS P t).adjoint_inner_left _ _).symm

theorem scalarRegularRightTomitaAdjoint_maximal (P : SiteProfile) (t : ℝ) (z : scalarTomitaAdjointDomain P) :
    ∃ hz : scalarGNSRepresentation P (regularRightCoreElement P t) z ∈
        scalarTomitaAdjointDomain P,
      scalarTomitaAdjoint P
        ⟨scalarGNSRepresentation P (regularRightCoreElement P t) z,hz⟩ =
      star (regularRightGNS P t) (scalarTomitaAdjoint P z) :=
  scalarTomitaAdjoint_maximal P (scalarRegularRightTomitaAdjoint_pairing P t z)

def scalarRegularRightTomitaAdjointInput (P : SiteProfile) (t : ℝ) (z : scalarTomitaAdjointDomain P) :
    scalarTomitaAdjointDomain P :=
  ⟨scalarGNSRepresentation P (regularRightCoreElement P t) z,
    (scalarRegularRightTomitaAdjoint_maximal P t z).choose⟩

theorem scalarTomitaAdjoint_regular_left_intertwines (P : SiteProfile) (t : ℝ) (z : scalarTomitaAdjointDomain P) :
    scalarTomitaAdjoint P (scalarRegularRightTomitaAdjointInput P t z) =
      star (regularRightGNS P t) (scalarTomitaAdjoint P z) :=
  (scalarRegularRightTomitaAdjoint_maximal P t z).choose_spec

theorem scalarRegularRightSquare_S_image (P : SiteProfile) (t : ℝ)
    (x : scalarTomitaSquareDomain P) :
    scalarClosedTomita P (scalarRegularRightClosedTomitaInput P t (scalarTomitaSquareInput P x)) =
      scalarGNSRepresentation P (regularRightCoreElement P (-t))
        (scalarTomitaSquareAdjointInput P x : ScalarGNSHilbert P) := by
  rw [scalarClosedTomita_regular_right_intertwines,regularRightCoreElement_star]
  rfl

theorem scalarRegularRight_mem_squareDomain (P : SiteProfile) (t : ℝ)
    (x : scalarTomitaSquareDomain P) :
    regularRightGNS P t (x : ScalarGNSHilbert P) ∈ scalarTomitaSquareDomain P := by
  refine ⟨scalarRegularRight_mem_closedTomitaDomain P t (scalarTomitaSquareInput P x),?_⟩
  change scalarClosedTomita P
    (scalarRegularRightClosedTomitaInput P t (scalarTomitaSquareInput P x)) ∈ scalarTomitaAdjointDomain P
  rw [scalarRegularRightSquare_S_image]
  exact (scalarRegularRightTomitaAdjointInput P (-t) (scalarTomitaSquareAdjointInput P x)).property

def scalarRegularRightSquareInput (P : SiteProfile) (t : ℝ)
    (x : scalarTomitaSquareDomain P) : scalarTomitaSquareDomain P :=
  ⟨regularRightGNS P t (x : ScalarGNSHilbert P),scalarRegularRight_mem_squareDomain P t x⟩

/-- The SAME positive selfadjoint A=S†S commutes on its entire composition
 domain with right multiplication by the regular unitary lambda_t. -/
theorem scalarTomitaSquare_regular_right_commutes (P : SiteProfile) (t : ℝ)
    (x : scalarTomitaSquareDomain P) :
    scalarTomitaSquare P (scalarRegularRightSquareInput P t x) =
      regularRightGNS P t (scalarTomitaSquare P x) := by
  have hi : scalarTomitaSquareAdjointInput P (scalarRegularRightSquareInput P t x) =
      scalarRegularRightTomitaAdjointInput P (-t) (scalarTomitaSquareAdjointInput P x) := by
    apply Subtype.ext
    exact scalarRegularRightSquare_S_image P t x
  calc
    _ = scalarTomitaAdjoint P
        (scalarTomitaSquareAdjointInput P (scalarRegularRightSquareInput P t x)) := rfl
    _ = scalarTomitaAdjoint P
        (scalarRegularRightTomitaAdjointInput P (-t) (scalarTomitaSquareAdjointInput P x)) :=
      congrArg (scalarTomitaAdjoint P) hi
    _ = star (regularRightGNS P (-t))
        (scalarTomitaAdjoint P (scalarTomitaSquareAdjointInput P x)) :=
      scalarTomitaAdjoint_regular_left_intertwines P (-t) (scalarTomitaSquareAdjointInput P x)
    _ = _ := by rw [regularRightGNS_star,neg_neg]; rfl

/-- The inverse is the already constructed right action at -t. -/
theorem scalarRegularRight_squareDomain_iff (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    regularRightGNS P t x ∈ scalarTomitaSquareDomain P ↔ x ∈ scalarTomitaSquareDomain P := by
  constructor
  · intro hx
    have h := scalarRegularRight_mem_squareDomain P (-t) ⟨regularRightGNS P t x,hx⟩
    change (regularRightGNS P (-t) * regularRightGNS P t) x ∈ scalarTomitaSquareDomain P at h
    simpa only [regularRightGNS_mul,neg_add_cancel,regularRightGNS_zero,
      ContinuousLinearMap.one_apply] using h
  · intro hx
    exact scalarRegularRight_mem_squareDomain P t ⟨x,hx⟩

#print axioms scalarRegularRightTomitaAdjoint_pairing
#print axioms scalarRegularRightTomitaAdjoint_maximal
#print axioms scalarRegularRightTomitaAdjointInput
#print axioms scalarTomitaAdjoint_regular_left_intertwines
#print axioms scalarRegularRightSquare_S_image
#print axioms scalarRegularRight_mem_squareDomain
#print axioms scalarRegularRightSquareInput
#print axioms scalarTomitaSquare_regular_right_commutes
#print axioms scalarRegularRight_squareDomain_iff
end
end TGLV350.Regular
