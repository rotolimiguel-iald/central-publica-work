import TGLExt.V350PartialPositiveResolvent
import TGLExt.V350ScalarTomitaSelfAdjoint

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable (P : SiteProfile)

/-- A bounded resolvent of the actual S†S, on the same scalar GNS Hilbert space. -/
def scalarTomitaResolvent : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P :=
  partialPositiveResolvent (scalarTomitaSquare P) (scalarTomitaSquare_positive P)
    (scalarTomitaSquare_resolvent_surjective P)

theorem scalarTomitaResolvent_equation (z : ScalarGNSHilbert P) :
    ∃ x : (scalarTomitaSquare P).domain,
      (x : ScalarGNSHilbert P)=scalarTomitaResolvent P z ∧
        (x : ScalarGNSHilbert P)+scalarTomitaSquare P x=z :=
  partialPositiveResolvent_equation _ _ _ z

theorem scalarTomitaResolvent_inverse (x : (scalarTomitaSquare P).domain) :
    scalarTomitaResolvent P ((x : ScalarGNSHilbert P)+scalarTomitaSquare P x)=
      (x : ScalarGNSHilbert P) :=
  partialPositiveResolvent_inverse _ _ _ x

theorem scalarTomitaResolvent_norm_le (z : ScalarGNSHilbert P) :
    ‖scalarTomitaResolvent P z‖ ≤ ‖z‖ := partialPositiveResolvent_norm_le _ _ _ z

theorem scalarTomitaResolvent_injective : Function.Injective (scalarTomitaResolvent P) :=
  partialPositiveResolvent_injective _ _ _

theorem scalarTomitaResolvent_nonneg : 0 ≤ scalarTomitaResolvent P :=
  partialPositiveResolvent_nonneg _ _ _ (scalarTomitaSquare_symmetric P)

theorem scalarTomitaResolvent_le_one : scalarTomitaResolvent P ≤ 1 :=
  partialPositiveResolvent_le_one _ _ _ (scalarTomitaSquare_symmetric P)

theorem scalarTomitaResolvent_selfadjoint : IsSelfAdjoint (scalarTomitaResolvent P) :=
  IsSelfAdjoint.of_nonneg (scalarTomitaResolvent_nonneg P)

/-- Equality as partial maps includes the exact composition domain. -/
theorem scalarTomitaResolvent_graph :
    resolventGraphOperator (scalarTomitaResolvent P) (scalarTomitaResolvent_injective P) =
      scalarTomitaSquare P :=
  partialPositiveResolvent_graph _ _ _

#print axioms scalarTomitaResolvent
#print axioms scalarTomitaResolvent_equation
#print axioms scalarTomitaResolvent_inverse
#print axioms scalarTomitaResolvent_norm_le
#print axioms scalarTomitaResolvent_injective
#print axioms scalarTomitaResolvent_nonneg
#print axioms scalarTomitaResolvent_le_one
#print axioms scalarTomitaResolvent_selfadjoint
#print axioms scalarTomitaResolvent_graph
end
end TGLV350.Regular
