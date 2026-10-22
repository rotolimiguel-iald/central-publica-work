import TGLExt.V350ScalarTomitaResolvent
import TGLExt.V350ResolventSquareRoot

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable (P : SiteProfile)

/-- A positive self-adjoint square root of the concrete S†S, constructed by CFC
of its bounded resolvent. Equality of its domain with D(S) is not asserted here. -/
def scalarTomitaPositiveRoot : ScalarGNSHilbert P →ₗ.[ℂ] ScalarGNSHilbert P :=
  resolventSquareRoot (scalarTomitaResolvent P) (scalarTomitaResolvent_nonneg P)
    (scalarTomitaResolvent_injective P)

theorem scalarTomitaPositiveRoot_closed : (scalarTomitaPositiveRoot P).IsClosed :=
  resolventSquareRoot_closed _ _ _ (scalarTomitaResolvent_le_one P)

theorem scalarTomitaPositiveRoot_dense :
    Dense ((scalarTomitaPositiveRoot P).domain : Set (ScalarGNSHilbert P)) :=
  resolventSquareRoot_dense _ _ _

theorem scalarTomitaPositiveRoot_selfadjoint : IsSelfAdjoint (scalarTomitaPositiveRoot P) :=
  resolventSquareRoot_selfadjoint _ _ _ (scalarTomitaResolvent_le_one P)

theorem scalarTomitaPositiveRoot_positive (x : (scalarTomitaPositiveRoot P).domain) :
    0 ≤ (inner ℂ (x : ScalarGNSHilbert P) (scalarTomitaPositiveRoot P x)).re :=
  resolventSquareRoot_positive _ _ _ x

/-- The square agrees with the original composition as partial maps, not just
on an algebraic core or up to an unspecified unitary equivalence. -/
theorem scalarTomitaPositiveRoot_square :
    partialOperatorSquare (scalarTomitaPositiveRoot P) = scalarTomitaSquare P :=
  (resolventSquareRoot_square _ _ _ (scalarTomitaResolvent_le_one P)).trans
    (scalarTomitaResolvent_graph P)

#print axioms scalarTomitaPositiveRoot
#print axioms scalarTomitaPositiveRoot_closed
#print axioms scalarTomitaPositiveRoot_dense
#print axioms scalarTomitaPositiveRoot_selfadjoint
#print axioms scalarTomitaPositiveRoot_positive
#print axioms scalarTomitaPositiveRoot_square
end
end TGLV350.Regular
