import TGLExt.V350ScalarTomitaSquare
import TGLExt.V350ClosedAntilinearResolvent
import TGLExt.V350PositiveSurjectiveResolvent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable (P : SiteProfile)

/-- The full range of I+S†S is obtained from the same closed graph of S. -/
theorem scalarTomitaSquare_resolvent_surjective (z : ScalarGNSHilbert P) :
    ∃ x : (scalarTomitaSquare P).domain,
      (x : ScalarGNSHilbert P)+scalarTomitaSquare P x=z := by
  obtain ⟨x,hx⟩ := closedAntilinear_complex_resolvent
    (scalarClosedTomitaDomain P) (scalarClosedTomita P)
    (scalarClosedTomita_is_closed (P := P)) z
  obtain ⟨hy,hval⟩ := scalarTomitaAdjoint_maximal P hx
  let w : scalarTomitaSquareDomain P := ⟨(x : ScalarGNSHilbert P),x.property,hy⟩
  refine ⟨w,?_⟩
  change (x : ScalarGNSHilbert P)+scalarTomitaAdjoint P ⟨scalarClosedTomita P x,hy⟩=z
  rw [hval]
  abel

theorem scalarTomitaSquare_domain_dense :
    Dense ((scalarTomitaSquare P).domain : Set (ScalarGNSHilbert P)) :=
  positive_surjective_resolvent_domain_dense (scalarTomitaSquare P)
    (scalarTomitaSquare_positive P) (scalarTomitaSquare_resolvent_surjective P)

/-- Actual self-adjointness on the composition domain, not a separate model. -/
theorem scalarTomitaSquare_selfadjoint : IsSelfAdjoint (scalarTomitaSquare P) :=
  positive_surjective_resolvent_selfadjoint (scalarTomitaSquare P)
    (scalarTomitaSquare_positive P) (scalarTomitaSquare_resolvent_surjective P)
    (scalarTomitaSquare_symmetric P)

theorem scalarTomitaSquare_isClosed : (scalarTomitaSquare P).IsClosed :=
  (scalarTomitaSquare_selfadjoint P).isClosed

theorem scalarClosedTomita_zero_only (x : scalarClosedTomitaDomain P)
    (hz : scalarClosedTomita P x=0) : (x : ScalarGNSHilbert P)=0 := by
  have hh : (⟨scalarClosedTomita P x,scalarClosedTomita_maps_domain x⟩ :
      scalarClosedTomitaDomain P)=0 := Subtype.ext hz
  have hi := scalarClosedTomita_involutive x
  rw [hh,map_zero] at hi
  exact hi.symm

/-- The positive self-adjoint composition has no zero vector in its kernel
apart from zero; no spectral gap is asserted. -/
theorem scalarTomitaSquare_zero_only (x : (scalarTomitaSquare P).domain)
    (hz : scalarTomitaSquare P x=0) : (x : ScalarGNSHilbert P)=0 := by
  have hq := scalarTomitaSquare_quadratic P x
  rw [hz,inner_zero_right] at hq
  have hn : ‖scalarClosedTomita P (scalarTomitaSquareInput P x)‖=0 :=
    (sq_eq_zero_iff).mp hq.symm
  exact scalarClosedTomita_zero_only P (scalarTomitaSquareInput P x) (norm_eq_zero.mp hn)

#print axioms scalarTomitaSquare_resolvent_surjective
#print axioms scalarTomitaSquare_domain_dense
#print axioms scalarTomitaSquare_selfadjoint
#print axioms scalarTomitaSquare_isClosed
#print axioms scalarClosedTomita_zero_only
#print axioms scalarTomitaSquare_zero_only
end
end TGLV350.Regular
