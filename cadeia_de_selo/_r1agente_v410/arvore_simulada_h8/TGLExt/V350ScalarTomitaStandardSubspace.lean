import TGLExt.V350ScalarClosedTomita
import TGLExt.ClosedAntilinearStandardSubspace

set_option autoImplicit false

namespace TGLV350.Regular
open TGLExt
noncomputable section

/-- The standard real subspace of the closed original finite-ideal graph.
This does not identify its polar data with the scalar weight's modular group. -/
def scalarTomitaStandardSubspace (P : SiteProfile) : StandardSubspace (ScalarGNSHilbert P) :=
  ChatgptAudit.Continuous049.closedAntilinearStandardSubspace
    (scalarClosedTomitaDomain P) (scalarClosedTomita P)
    scalarClosedTomita_is_closed scalarClosedTomita_maps_domain
    scalarClosedTomita_involutive scalarClosedTomita_domain_dense

theorem scalarTomitaStandardSubspace_mem (P : SiteProfile) (x : ScalarGNSHilbert P) :
    x ∈ (scalarTomitaStandardSubspace P).toClosedSubmodule ↔
      ∃ hx : x ∈ scalarClosedTomitaDomain P, scalarClosedTomita P ⟨x,hx⟩ = x :=
  Iff.rfl

theorem scalarClosedTomitaDomain_fixed_sum (P : SiteProfile) (x : ScalarGNSHilbert P) :
    x ∈ scalarClosedTomitaDomain P ↔
      ∃ h k : ScalarGNSHilbert P, h ∈ (scalarTomitaStandardSubspace P).toClosedSubmodule ∧
        k ∈ (scalarTomitaStandardSubspace P).toClosedSubmodule ∧ x = h + Complex.I • k :=
  ChatgptAudit.Continuous049.mem_domain_iff_fixed_sum
    (scalarClosedTomitaDomain P) (scalarClosedTomita P)
    scalarClosedTomita_maps_domain scalarClosedTomita_involutive x

theorem scalarClosedTomita_fixed_decomposition (P : SiteProfile)
    (x : scalarClosedTomitaDomain P) :
    ∃ h k : ScalarGNSHilbert P, h ∈ (scalarTomitaStandardSubspace P).toClosedSubmodule ∧
      k ∈ (scalarTomitaStandardSubspace P).toClosedSubmodule ∧
      (x : ScalarGNSHilbert P) = h + Complex.I • k ∧
      scalarClosedTomita P x = h - Complex.I • k :=
  ChatgptAudit.Continuous049.domain_fixed_decomposition
    (scalarClosedTomitaDomain P) (scalarClosedTomita P)
    scalarClosedTomita_maps_domain scalarClosedTomita_involutive x

#print axioms scalarTomitaStandardSubspace
#print axioms scalarTomitaStandardSubspace_mem
#print axioms scalarClosedTomitaDomain_fixed_sum
#print axioms scalarClosedTomita_fixed_decomposition
end
end TGLV350.Regular
