import TGLExt.V350ScalarTomitaAdjoint
import TGLExt.V350AntilinearComposition

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable (P : SiteProfile)

/-- The composition domain is exactly x in D(S) with Sx in D(S†). -/
def scalarTomitaSquareDomain : Submodule ℂ (ScalarGNSHilbert P) :=
  antilinearPreimageDomain (scalarClosedTomitaDomain P) (scalarTomitaAdjointDomain P)
    (scalarClosedTomita P)

def scalarTomitaSquareInput : scalarTomitaSquareDomain P →ₗ[ℂ]
    scalarClosedTomitaDomain P :=
  antilinearPreimageInput _ _ _

theorem scalarTomitaSquareInput_coe (x : scalarTomitaSquareDomain P) :
    (scalarTomitaSquareInput P x : ScalarGNSHilbert P) = x := rfl

theorem scalarTomitaSquareInput_image_mem (x : scalarTomitaSquareDomain P) :
    scalarClosedTomita P (scalarTomitaSquareInput P x) ∈ scalarTomitaAdjointDomain P :=
  antilinearPreimageInput_mem _ _ _ x

def scalarTomitaSquareAdjointInput : scalarTomitaSquareDomain P →ₛₗ[starRingEnd ℂ]
    scalarTomitaAdjointDomain P :=
  antilinearPreimageMap _ _ _

/-- The actual complex-linear composition. Self-adjointness is not part of
this definition and must be proved separately. -/
def scalarTomitaSquare : ScalarGNSHilbert P →ₗ.[ℂ] ScalarGNSHilbert P where
  domain := scalarTomitaSquareDomain P
  toFun := (antilinearComposite (scalarClosedTomitaDomain P) (scalarTomitaAdjointDomain P)
    (scalarClosedTomita P) (scalarTomitaAdjoint P).toFun).toFun

theorem scalarTomitaSquare_domain_iff (x : ScalarGNSHilbert P) :
    x ∈ (scalarTomitaSquare P).domain ↔
      ∃ hx : x ∈ scalarClosedTomitaDomain P,
        scalarClosedTomita P ⟨x,hx⟩ ∈ scalarTomitaAdjointDomain P := Iff.rfl

theorem scalarTomitaSquare_apply (x : scalarTomitaSquareDomain P) :
    scalarTomitaSquare P x = scalarTomitaAdjoint P
      ⟨scalarClosedTomita P (scalarTomitaSquareInput P x),
        scalarTomitaSquareInput_image_mem P x⟩ := rfl

theorem scalarTomitaSquare_pairing (x : scalarTomitaSquareDomain P)
    (y : scalarClosedTomitaDomain P) :
    inner ℂ (scalarTomitaSquare P x) (y : ScalarGNSHilbert P) =
      inner ℂ (scalarClosedTomita P y)
        (scalarClosedTomita P (scalarTomitaSquareInput P x)) :=
  (scalarTomitaAdjoint_pairing P (scalarTomitaSquareAdjointInput P x) y).symm

theorem scalarTomitaSquare_symmetric :
    (scalarTomitaSquare P).IsFormalAdjoint (scalarTomitaSquare P) := by
  intro x y
  calc
    _ = inner ℂ (scalarClosedTomita P (scalarTomitaSquareInput P y))
        (scalarClosedTomita P (scalarTomitaSquareInput P x)) :=
      scalarTomitaSquare_pairing P x (scalarTomitaSquareInput P y)
    _ = (starRingEnd ℂ) (inner ℂ
        (scalarClosedTomita P (scalarTomitaSquareInput P x))
        (scalarClosedTomita P (scalarTomitaSquareInput P y))) :=
      (inner_conj_symm (𝕜 := ℂ)
        (scalarClosedTomita P (scalarTomitaSquareInput P y))
        (scalarClosedTomita P (scalarTomitaSquareInput P x))).symm
    _ = (starRingEnd ℂ) (inner ℂ (scalarTomitaSquare P y) (x : ScalarGNSHilbert P)) :=
      congrArg (starRingEnd ℂ)
        (scalarTomitaSquare_pairing P y (scalarTomitaSquareInput P x)).symm
    _ = _ := inner_conj_symm (𝕜 := ℂ) (x : ScalarGNSHilbert P) (scalarTomitaSquare P y)

theorem scalarTomitaSquare_quadratic (x : scalarTomitaSquareDomain P) :
    (inner ℂ (x : ScalarGNSHilbert P) (scalarTomitaSquare P x)).re =
      ‖scalarClosedTomita P (scalarTomitaSquareInput P x)‖^2 := by
  calc
    _ = (inner ℂ (scalarTomitaSquare P x) (x : ScalarGNSHilbert P)).re :=
      inner_re_symm (𝕜 := ℂ) (x : ScalarGNSHilbert P) (scalarTomitaSquare P x)
    _ = (inner ℂ (scalarClosedTomita P (scalarTomitaSquareInput P x))
        (scalarClosedTomita P (scalarTomitaSquareInput P x))).re :=
      congrArg Complex.re (scalarTomitaSquare_pairing P x (scalarTomitaSquareInput P x))
    _ = _ := (norm_sq_eq_re_inner (𝕜 := ℂ)
      (scalarClosedTomita P (scalarTomitaSquareInput P x))).symm

theorem scalarTomitaSquare_positive (x : scalarTomitaSquareDomain P) :
    0 ≤ (inner ℂ (x : ScalarGNSHilbert P) (scalarTomitaSquare P x)).re := by
  rw [scalarTomitaSquare_quadratic]
  exact sq_nonneg _

#print axioms scalarTomitaSquareDomain
#print axioms scalarTomitaSquareInput
#print axioms scalarTomitaSquareInput_coe
#print axioms scalarTomitaSquareInput_image_mem
#print axioms scalarTomitaSquareAdjointInput
#print axioms scalarTomitaSquare
#print axioms scalarTomitaSquare_domain_iff
#print axioms scalarTomitaSquare_apply
#print axioms scalarTomitaSquare_pairing
#print axioms scalarTomitaSquare_symmetric
#print axioms scalarTomitaSquare_quadratic
#print axioms scalarTomitaSquare_positive
end
end TGLV350.Regular
