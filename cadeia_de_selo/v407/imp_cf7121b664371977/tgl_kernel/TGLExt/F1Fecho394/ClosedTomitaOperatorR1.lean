import TGLExt.V350AntilinearAdjointGraph
import TGLExt.V350AntilinearComposition
import TGLExt.V350ClosedAntilinearResolvent
import TGLExt.V350PositiveSurjectiveResolvent
import TGLExt.V350PartialPositiveResolvent
import TGLExt.V351ResolventImaginaryContinuity
/-! The positive selfadjoint operator S_nu^* S_nu and its bounded resolvent
on any Hilbert space carrying a closed dense antilinear involution. Its domain is the exact adjoint
composition domain. No equality with regular or geometric modular flow is
inserted; the scalar weight is not called a scaled trace. -/
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.ClosedTomitaOperator
open TGLExt TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
structure Input (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] where
  domain : Submodule ℂ H
  operator : domain →ₛₗ[starRingEnd ℂ] H
  dense : Dense (domain : Set H)
  closed : IsClosed (Set.range (fun x : domain => ((x : H), operator x)))
  maps_domain : ∀ x : domain, operator x ∈ domain
  involutive : ∀ x : domain, operator ⟨operator x,maps_domain x⟩ = x
variable (A : Input H)
local instance : PartialOrder (H →L[ℂ] H) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := H)
abbrev scalarClosedTomitaDomain := A.domain
abbrev scalarClosedTomita := A.operator
 theorem scalarClosedTomita_domain_dense : Dense (scalarClosedTomitaDomain A : Set H) := A.dense
 theorem scalarClosedTomita_is_closed : IsClosed (Set.range (fun x : scalarClosedTomitaDomain A => ((x:H),scalarClosedTomita A x))) := A.closed
 theorem scalarClosedTomita_maps_domain (x:scalarClosedTomitaDomain A) : scalarClosedTomita A x ∈ scalarClosedTomitaDomain A := A.maps_domain x
 theorem scalarClosedTomita_involutive (x:scalarClosedTomitaDomain A) : scalarClosedTomita A ⟨scalarClosedTomita A x,scalarClosedTomita_maps_domain A x⟩ = x := A.involutive x
def scalarTomitaAdjointDomain : Submodule ℂ (H) :=
  maximalAntilinearAdjointDomain (H := H) (scalarClosedTomitaDomain A) (scalarClosedTomita A)

/-- The maximal complex-antilinear adjoint of the same closed operator on the given Hilbert space. -/
def scalarTomitaAdjoint : H →ₛₗ.[starRingEnd ℂ] H :=
  maximalAntilinearAdjoint (H := H) (scalarClosedTomitaDomain A) (scalarClosedTomita A)
    (scalarClosedTomita_domain_dense A )

theorem scalarTomitaAdjoint_pairing (y : scalarTomitaAdjointDomain A)
    (x : scalarClosedTomitaDomain A) :
    inner ℂ (scalarClosedTomita A x) (y : H) =
      inner ℂ (scalarTomitaAdjoint A y) (x : H) :=
  maximalAntilinearAdjoint_pairing (H := H) _ _ _ y x

theorem scalarTomitaAdjoint_maximal {y z : H}
    (h : ∀ x : scalarClosedTomitaDomain A,
      inner ℂ (scalarClosedTomita A x) y = inner ℂ z (x : H)) :
    ∃ hy : y ∈ scalarTomitaAdjointDomain A, scalarTomitaAdjoint A ⟨y,hy⟩ = z :=
  maximalAntilinearAdjoint_maximal (H := H) _ _ _ h

theorem scalarTomitaAdjoint_domain_iff (y : H) :
    y ∈ scalarTomitaAdjointDomain A ↔ ∃ z : H,
      ∀ x : scalarClosedTomitaDomain A,
        inner ℂ (scalarClosedTomita A x) y = inner ℂ z (x : H) := Iff.rfl

theorem scalarTomitaAdjoint_isClosed :
    IsClosed (Set.range (fun y : scalarTomitaAdjointDomain A =>
      ((y : H),scalarTomitaAdjoint A y))) :=
  maximalAntilinearAdjoint_isClosed (H := H) _ _ _


/-- The composition domain is exactly x in D(S) with Sx in D(S†). -/
def scalarTomitaSquareDomain : Submodule ℂ (H) :=
  antilinearPreimageDomain (H := H) (scalarClosedTomitaDomain A) (scalarTomitaAdjointDomain A)
    (scalarClosedTomita A)

def scalarTomitaSquareInput : scalarTomitaSquareDomain A →ₗ[ℂ]
    scalarClosedTomitaDomain A :=
  antilinearPreimageInput (H := H) _ _ _

theorem scalarTomitaSquareInput_coe (x : scalarTomitaSquareDomain A) :
    (scalarTomitaSquareInput A x : H) = x := rfl

theorem scalarTomitaSquareInput_image_mem (x : scalarTomitaSquareDomain A) :
    scalarClosedTomita A (scalarTomitaSquareInput A x) ∈ scalarTomitaAdjointDomain A :=
  antilinearPreimageInput_mem (H := H) _ _ _ x

def scalarTomitaSquareAdjointInput : scalarTomitaSquareDomain A →ₛₗ[starRingEnd ℂ]
    scalarTomitaAdjointDomain A :=
  antilinearPreimageMap (H := H) _ _ _

/-- The actual complex-linear composition. Self-adjointness is not part of
this definition and must be proved separately. -/
def scalarTomitaSquare : H →ₗ.[ℂ] H where
  domain := scalarTomitaSquareDomain A
  toFun := (antilinearComposite (scalarClosedTomitaDomain A) (scalarTomitaAdjointDomain A)
    (scalarClosedTomita A) (scalarTomitaAdjoint A).toFun).toFun

theorem scalarTomitaSquare_domain_iff (x : H) :
    x ∈ (scalarTomitaSquare A).domain ↔
      ∃ hx : x ∈ scalarClosedTomitaDomain A,
        scalarClosedTomita A ⟨x,hx⟩ ∈ scalarTomitaAdjointDomain A := Iff.rfl

theorem scalarTomitaSquare_apply (x : scalarTomitaSquareDomain A) :
    scalarTomitaSquare A x = scalarTomitaAdjoint A
      ⟨scalarClosedTomita A (scalarTomitaSquareInput A x),
        scalarTomitaSquareInput_image_mem A x⟩ := rfl

theorem scalarTomitaSquare_pairing (x : scalarTomitaSquareDomain A)
    (y : scalarClosedTomitaDomain A) :
    inner ℂ (scalarTomitaSquare A x) (y : H) =
      inner ℂ (scalarClosedTomita A y)
        (scalarClosedTomita A (scalarTomitaSquareInput A x)) :=
  (scalarTomitaAdjoint_pairing A (scalarTomitaSquareAdjointInput A x) y).symm

theorem scalarTomitaSquare_symmetric :
    (scalarTomitaSquare A).IsFormalAdjoint (scalarTomitaSquare A) := by
  intro x y
  calc
    _ = inner ℂ (scalarClosedTomita A (scalarTomitaSquareInput A y))
        (scalarClosedTomita A (scalarTomitaSquareInput A x)) :=
      scalarTomitaSquare_pairing A x (scalarTomitaSquareInput A y)
    _ = (starRingEnd ℂ) (inner ℂ
        (scalarClosedTomita A (scalarTomitaSquareInput A x))
        (scalarClosedTomita A (scalarTomitaSquareInput A y))) :=
      (inner_conj_symm (𝕜 := ℂ)
        (scalarClosedTomita A (scalarTomitaSquareInput A y))
        (scalarClosedTomita A (scalarTomitaSquareInput A x))).symm
    _ = (starRingEnd ℂ) (inner ℂ (scalarTomitaSquare A y) (x : H)) :=
      congrArg (starRingEnd ℂ)
        (scalarTomitaSquare_pairing A y (scalarTomitaSquareInput A x)).symm
    _ = _ := inner_conj_symm (𝕜 := ℂ) (x : H) (scalarTomitaSquare A y)

theorem scalarTomitaSquare_quadratic (x : scalarTomitaSquareDomain A) :
    (inner ℂ (x : H) (scalarTomitaSquare A x)).re =
      ‖scalarClosedTomita A (scalarTomitaSquareInput A x)‖^2 := by
  calc
    _ = (inner ℂ (scalarTomitaSquare A x) (x : H)).re :=
      inner_re_symm (𝕜 := ℂ) (x : H) (scalarTomitaSquare A x)
    _ = (inner ℂ (scalarClosedTomita A (scalarTomitaSquareInput A x))
        (scalarClosedTomita A (scalarTomitaSquareInput A x))).re :=
      congrArg Complex.re (scalarTomitaSquare_pairing A x (scalarTomitaSquareInput A x))
    _ = _ := (norm_sq_eq_re_inner (𝕜 := ℂ)
      (scalarClosedTomita A (scalarTomitaSquareInput A x))).symm

theorem scalarTomitaSquare_positive (x : scalarTomitaSquareDomain A) :
    0 ≤ (inner ℂ (x : H) (scalarTomitaSquare A x)).re := by
  rw [scalarTomitaSquare_quadratic A]
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

/-- The full range of I+S†S is obtained from the same closed graph of S. -/
theorem scalarTomitaSquare_resolvent_surjective (z : H) :
    ∃ x : (scalarTomitaSquare A).domain,
      (x : H)+scalarTomitaSquare A x=z := by
  obtain ⟨x,hx⟩ := closedAntilinear_complex_resolvent (H := H)
    (scalarClosedTomitaDomain A) (scalarClosedTomita A)
    (scalarClosedTomita_is_closed A ) z
  obtain ⟨hy,hval⟩ := scalarTomitaAdjoint_maximal A hx
  let w : scalarTomitaSquareDomain A := ⟨(x : H),x.property,hy⟩
  refine ⟨w,?_⟩
  change (x : H)+scalarTomitaAdjoint A ⟨scalarClosedTomita A x,hy⟩=z
  rw [hval]
  abel

theorem scalarTomitaSquare_domain_dense :
    Dense ((scalarTomitaSquare A).domain : Set (H)) :=
  positive_surjective_resolvent_domain_dense (H := H) (scalarTomitaSquare A)
    (scalarTomitaSquare_positive A) (scalarTomitaSquare_resolvent_surjective A)

/-- Actual self-adjointness on the composition domain, not a separate model. -/
theorem scalarTomitaSquare_selfadjoint : IsSelfAdjoint (scalarTomitaSquare A) :=
  positive_surjective_resolvent_selfadjoint (H := H) (scalarTomitaSquare A)
    (scalarTomitaSquare_positive A) (scalarTomitaSquare_resolvent_surjective A)
    (scalarTomitaSquare_symmetric A)

theorem scalarTomitaSquare_isClosed : (scalarTomitaSquare A).IsClosed :=
  (scalarTomitaSquare_selfadjoint A).isClosed

theorem scalarClosedTomita_zero_only (x : scalarClosedTomitaDomain A)
    (hz : scalarClosedTomita A x=0) : (x : H)=0 := by
  have hh : (⟨scalarClosedTomita A x,scalarClosedTomita_maps_domain A x⟩ :
      scalarClosedTomitaDomain A)=0 := Subtype.ext hz
  have hi := scalarClosedTomita_involutive A x
  rw [hh,map_zero] at hi
  exact hi.symm

/-- The positive self-adjoint composition has no zero vector in its kernel
apart from zero; no spectral gap is asserted. -/
theorem scalarTomitaSquare_zero_only (x : (scalarTomitaSquare A).domain)
    (hz : scalarTomitaSquare A x=0) : (x : H)=0 := by
  have hq := scalarTomitaSquare_quadratic A x
  rw [hz,inner_zero_right] at hq
  have hn : ‖scalarClosedTomita A (scalarTomitaSquareInput A x)‖=0 :=
    (sq_eq_zero_iff).mp hq.symm
  exact scalarClosedTomita_zero_only A (scalarTomitaSquareInput A x) (norm_eq_zero.mp hn)

#print axioms scalarTomitaSquare_resolvent_surjective
#print axioms scalarTomitaSquare_domain_dense
#print axioms scalarTomitaSquare_selfadjoint
#print axioms scalarTomitaSquare_isClosed
#print axioms scalarClosedTomita_zero_only
#print axioms scalarTomitaSquare_zero_only

/-- A bounded resolvent of the actual S†S, on the same scalar GNS Hilbert space. -/
def scalarTomitaResolvent : H →L[ℂ] H :=
  partialPositiveResolvent (H := H) (scalarTomitaSquare A) (scalarTomitaSquare_positive A)
    (scalarTomitaSquare_resolvent_surjective A)

theorem scalarTomitaResolvent_equation (z : H) :
    ∃ x : (scalarTomitaSquare A).domain,
      (x : H)=scalarTomitaResolvent A z ∧
        (x : H)+scalarTomitaSquare A x=z :=
  partialPositiveResolvent_equation (H := H) _ _ _ z

theorem scalarTomitaResolvent_inverse (x : (scalarTomitaSquare A).domain) :
    scalarTomitaResolvent A ((x : H)+scalarTomitaSquare A x)=
      (x : H) :=
  partialPositiveResolvent_inverse (H := H) _ _ _ x

theorem scalarTomitaResolvent_norm_le (z : H) :
    ‖scalarTomitaResolvent A z‖ ≤ ‖z‖ := partialPositiveResolvent_norm_le (H := H) _ _ _ z

theorem scalarTomitaResolvent_injective : Function.Injective (scalarTomitaResolvent A) :=
  partialPositiveResolvent_injective (H := H) _ _ _

theorem scalarTomitaResolvent_nonneg : 0 ≤ scalarTomitaResolvent A :=
  partialPositiveResolvent_nonneg (H := H) _ _ _ (scalarTomitaSquare_symmetric A)

theorem scalarTomitaResolvent_le_one : scalarTomitaResolvent A ≤ 1 :=
  partialPositiveResolvent_le_one (H := H) _ _ _ (scalarTomitaSquare_symmetric A)

theorem scalarTomitaResolvent_selfadjoint : IsSelfAdjoint (scalarTomitaResolvent A) :=
  IsSelfAdjoint.of_nonneg (scalarTomitaResolvent_nonneg A)

/-- Equality as partial maps includes the exact composition domain. -/
theorem scalarTomitaResolvent_graph :
    resolventGraphOperator (H := H) (scalarTomitaResolvent A) (scalarTomitaResolvent_injective A) =
      scalarTomitaSquare A :=
  partialPositiveResolvent_graph (H := H) _ _ _

#print axioms scalarTomitaResolvent
#print axioms scalarTomitaResolvent_equation
#print axioms scalarTomitaResolvent_inverse
#print axioms scalarTomitaResolvent_norm_le
#print axioms scalarTomitaResolvent_injective
#print axioms scalarTomitaResolvent_nonneg
#print axioms scalarTomitaResolvent_le_one
#print axioms scalarTomitaResolvent_selfadjoint
#print axioms scalarTomitaResolvent_graph

#print axioms scalarTomitaAdjoint
#print axioms scalarTomitaAdjoint_pairing
#print axioms scalarTomitaAdjoint_maximal
#print axioms scalarTomitaAdjoint_isClosed
end F1Fecho.ClosedTomitaOperator
