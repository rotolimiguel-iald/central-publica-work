import TGLExt.V350ScalarTomitaPositiveRoot
import TGLExt.V350PartialSquareEnergy

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable (P : SiteProfile)

/-- Equality of energies on D(S†S). Extension to all D(S) remains a separate proof. -/
theorem scalarTomitaPositiveRoot_energy_on_square_domain
    (x : (scalarTomitaSquare P).domain) :
    ∃ u : (scalarTomitaPositiveRoot P).domain,
      (u : ScalarGNSHilbert P)=(x : ScalarGNSHilbert P) ∧
        ‖scalarTomitaPositiveRoot P u‖^2 =
          ‖scalarClosedTomita P (scalarTomitaSquareInput P x)‖^2 := by
  obtain ⟨u,hu,hn⟩ := partialSquare_energy (scalarTomitaPositiveRoot P) (scalarTomitaSquare P)
    (resolventSquareRoot_formalAdjoint (scalarTomitaResolvent P)
      (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_injective P))
    (scalarTomitaPositiveRoot_square P) x
  exact ⟨u,hu,hn.trans (scalarTomitaSquare_quadratic P x)⟩

/-- A zero vector of the root gives a zero vector of its square on the full
successive domain; no inverse boundedness or spectral gap follows. -/
theorem scalarTomitaPositiveRoot_zero_only
    (x : (scalarTomitaPositiveRoot P).domain)
    (hz : scalarTomitaPositiveRoot P x=0) : (x : ScalarGNSHilbert P)=0 := by
  let B := scalarTomitaPositiveRoot P
  have hg : ((x : ScalarGNSHilbert P),0) ∈ (partialOperatorSquare B).graph := by
    apply (partialOperatorSquare_graph_iff B _ _).mpr
    refine ⟨0,?_,?_⟩
    · exact (LinearPMap.mem_graph_iff B).mpr ⟨x,rfl,hz⟩
    · exact (LinearPMap.mem_graph_iff B).mpr ⟨0,rfl,B.toFun.map_zero⟩
  rw [scalarTomitaPositiveRoot_square P] at hg
  obtain ⟨u,hu,hAu⟩ := (LinearPMap.mem_graph_iff (scalarTomitaSquare P)).mp hg
  exact hu.symm.trans (scalarTomitaSquare_zero_only P u hAu)

#print axioms scalarTomitaPositiveRoot_energy_on_square_domain
#print axioms scalarTomitaPositiveRoot_zero_only
end
end TGLV350.Regular
