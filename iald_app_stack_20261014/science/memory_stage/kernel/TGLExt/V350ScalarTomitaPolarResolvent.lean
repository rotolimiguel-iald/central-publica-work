import TGLExt.V350ScalarTomitaPolarFactor
import TGLExt.V350ScalarTomitaResolventFlip
import TGLExt.V350ResolventGraphTransport

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable (P : SiteProfile)

theorem scalarTomitaPositiveRoot_resolvent_graph (x : (scalarTomitaPositiveRoot P).domain) :
    (scalarTomitaResolvent P (x : ScalarGNSHilbert P),
      scalarTomitaResolvent P (scalarTomitaPositiveRoot P x)) ∈ (scalarTomitaPositiveRoot P).graph :=
  resolvent_sqrt_graph_transport_of_commute (scalarTomitaResolvent P) (scalarTomitaResolvent P)
    (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_injective P) (Commute.refl _) _ _
    ((LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot P)).mpr ⟨x,rfl,rfl⟩)

/-- Bounded antiunitary transport of the resolvent, extended from its dense root image. -/
theorem scalarTomitaPolarFactor_resolvent (z : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P (scalarTomitaResolvent P z)=
      scalarTomitaPolarFactor P z - scalarTomitaResolvent P (scalarTomitaPolarFactor P z) := by
  refine (scalarTomitaPositiveRoot_denseRange P).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) z
  rintro _ ⟨x,rfl⟩
  obtain ⟨u,hu,hBu⟩ := (LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot P)).mp
    (scalarTomitaPositiveRoot_resolvent_graph P x)
  have he : Submodule.inclusion (scalarTomitaRootDomain_le_closed P) u =
      (⟨scalarTomitaResolvent P (x : ScalarGNSHilbert P),
        scalarTomitaResolvent_memDomain P (x : ScalarGNSHilbert P)⟩ : scalarClosedTomitaDomain P) :=
    Subtype.ext hu
  calc
    _ = scalarTomitaPolarFactor P (scalarTomitaPositiveRoot P u) :=
      congrArg (scalarTomitaPolarFactor P) hBu.symm
    _ = scalarClosedTomita P (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) u) :=
      scalarTomitaPolarFactor_root P u
    _ = scalarClosedTomita P ⟨scalarTomitaResolvent P (x : ScalarGNSHilbert P),
        scalarTomitaResolvent_memDomain P (x : ScalarGNSHilbert P)⟩ :=
      congrArg (scalarClosedTomita P) he
    _ = scalarClosedTomita P (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) x) -
        scalarTomitaResolvent P (scalarClosedTomita P
          (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) x)) :=
      scalarTomitaResolvent_flip P (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) x)
    _ = _ := congrArg (fun y : ScalarGNSHilbert P => y-scalarTomitaResolvent P y)
      (scalarTomitaPolarFactor_root P x).symm

#print axioms scalarTomitaPositiveRoot_resolvent_graph
#print axioms scalarTomitaPolarFactor_resolvent
end
end TGLV350.Regular
