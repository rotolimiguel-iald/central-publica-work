import TGLExt.F1Fecho394.CanonicalFockGNSRepresentationR6
import TGLExt.F1Fecho394.CanonicalFockWeightCompletionR5
import TGLExt.V350AntiunitaryPositiveConjugation
import Mathlib.Algebra.Star.Subalgebra
import TGLExt.F1Fecho394.GenericPolarRightAlgebraR2
/-! Algebraic closure on the actual full-weight Fock domain. Consumes the
generic star algebra directly and checks its carrier against the native predicate.
J remains explicit until the actual polar consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
open TGLV350.Regular (antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockRegular
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
variable (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
/-- The actual polar right identity on the existing full weight domain. -/
def ScalarPolarRight  (b : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra) : Prop :=
  ∀ A : scalarWeightLeftIdeal, ∃ h : A.val*b ∈ scalarWeightLeftIdeal,
    scalarWeightGNSEmbedding ⟨A.val*b,h⟩ =
      antiunitaryConjugate (H := GNSHilbert) J
        (scalarGNSRepresentation (star b)) (scalarWeightGNSEmbedding A)

/-- Consume the already proved generic star algebra in one application. -/
abbrev scalarPolarRightAlgebra := F1Fecho.GenericPolarRightAlgebra.scalarPolarRightAlgebra
  (H := GNSHilbert) (𝒜 := F1Fecho.CanonicalFockRegular.core.toStarSubalgebra)
  scalarWeightLeftIdeal scalarWeightGNSEmbedding scalarGNSRepresentation J

theorem scalarPolarRightAlgebra_mem_iff
    (b : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra) :
    b ∈ scalarPolarRightAlgebra J ↔ ScalarPolarRight J b ∧ ScalarPolarRight J (star b) := Iff.rfl
end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.ScalarPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRightAlgebra
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRightAlgebra_mem_iff
