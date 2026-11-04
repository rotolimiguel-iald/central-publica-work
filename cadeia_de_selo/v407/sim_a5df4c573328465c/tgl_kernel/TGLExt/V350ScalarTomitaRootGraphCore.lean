import TGLExt.V350PartialSquareGraphCore
import TGLExt.V350ScalarTomitaRootEnergy

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section
variable (P : SiteProfile)

theorem scalarTomitaSquareDomain_le_root :
    (scalarTomitaSquare P).domain ≤ (scalarTomitaPositiveRoot P).domain :=
  partialSquare_domain_le (scalarTomitaPositiveRoot P) (scalarTomitaSquare P)
    (scalarTomitaPositiveRoot_square P)

theorem scalarTomitaRoot_real_graph_closed :
    IsClosed (Set.range (fun x : (scalarTomitaPositiveRoot P).domain =>
      ((x : ScalarGNSHilbert P),scalarTomitaPositiveRoot P x))) := by
  let B := scalarTomitaPositiveRoot P
  have he : Set.range (fun x : B.domain => ((x : ScalarGNSHilbert P),B x)) =
      (B.graph : Set (ScalarGNSHilbert P × ScalarGNSHilbert P)) := by
    ext p
    constructor
    · rintro ⟨u,rfl⟩
      exact LinearPMap.mem_graph B u
    · intro hp
      obtain ⟨u,hu,hBu⟩ := (LinearPMap.mem_graph_iff B).mp hp
      exact ⟨u,Prod.ext hu hBu⟩
  rw [he]
  exact scalarTomitaPositiveRoot_closed P

theorem scalarTomitaSquare_root_graph_core :
    DenseRange (realGraphInclusion (scalarTomitaPositiveRoot P).domain
      ((scalarTomitaPositiveRoot P).toFun.restrictScalars ℝ)
      (scalarTomitaSquare P).domain (scalarTomitaSquareDomain_le_root P)) :=
  partialSquare_graph_core (scalarTomitaPositiveRoot P) (scalarTomitaSquare P)
    (scalarTomitaPositiveRoot_square P)
    (resolventSquareRoot_formalAdjoint (scalarTomitaResolvent P)
      (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_injective P))
    (scalarTomitaRoot_real_graph_closed P) (scalarTomitaSquare_resolvent_surjective P)

theorem scalarTomitaSquare_root_graph_approximation
    (x : (scalarTomitaPositiveRoot P).domain) :
    ∃ u : ℕ → (scalarTomitaSquare P).domain,
      Tendsto (fun n => (u n : ScalarGNSHilbert P)) atTop (𝓝 (x : ScalarGNSHilbert P)) ∧
      Tendsto (fun n => scalarTomitaPositiveRoot P
        (Submodule.inclusion (scalarTomitaSquareDomain_le_root P) (u n))) atTop
          (𝓝 (scalarTomitaPositiveRoot P x)) :=
  realGraphCore_sequence (scalarTomitaPositiveRoot P).domain
    ((scalarTomitaPositiveRoot P).toFun.restrictScalars ℝ)
    (scalarTomitaSquare P).domain (scalarTomitaSquareDomain_le_root P)
    (scalarTomitaSquare_root_graph_core P) x

#print axioms scalarTomitaSquareDomain_le_root
#print axioms scalarTomitaRoot_real_graph_closed
#print axioms scalarTomitaSquare_root_graph_core
#print axioms scalarTomitaSquare_root_graph_approximation
end
end TGLV350.Regular
