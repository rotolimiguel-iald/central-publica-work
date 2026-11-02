import TGLExt.V350ScalarTomitaGraphCore
import TGLExt.V350ScalarTomitaRootGraphCore
import TGLExt.V350GraphCoreNormTransfer

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable (P : SiteProfile)

theorem scalarTomitaSquare_norm_match (x : (scalarTomitaSquare P).domain) :
    ‖scalarClosedTomita P (Submodule.inclusion (scalarTomitaSquareDomain_le P) x)‖ =
      ‖scalarTomitaPositiveRoot P (Submodule.inclusion (scalarTomitaSquareDomain_le_root P) x)‖ := by
  obtain ⟨u,hu,hn⟩ := scalarTomitaPositiveRoot_energy_on_square_domain P x
  have he : Submodule.inclusion (scalarTomitaSquareDomain_le_root P) x = u :=
    Subtype.ext hu.symm
  have hn' : ‖scalarTomitaPositiveRoot P
      (Submodule.inclusion (scalarTomitaSquareDomain_le_root P) x)‖^2 =
        ‖scalarClosedTomita P (scalarTomitaSquareInput P x)‖^2 :=
    (congrArg (fun v => ‖scalarTomitaPositiveRoot P v‖^2) he).trans hn
  have hS := norm_nonneg (scalarClosedTomita P (scalarTomitaSquareInput P x))
  have hB := norm_nonneg (scalarTomitaPositiveRoot P
    (Submodule.inclusion (scalarTomitaSquareDomain_le_root P) x))
  change ‖scalarClosedTomita P (scalarTomitaSquareInput P x)‖ = _
  nlinarith only [hn',hS,hB]

theorem scalarClosedTomitaDomain_le_root :
    scalarClosedTomitaDomain P ≤ (scalarTomitaPositiveRoot P).domain :=
  graphCore_norm_domain_transfer (scalarClosedTomitaDomain P)
    (scalarTomitaPositiveRoot P).domain (scalarTomitaSquare P).domain
    (antilinearRealMap (scalarClosedTomitaDomain P) (scalarClosedTomita P))
    ((scalarTomitaPositiveRoot P).toFun.restrictScalars ℝ)
    (scalarTomitaSquareDomain_le P) (scalarTomitaSquareDomain_le_root P)
    (scalarTomitaSquare_graph_core P) (scalarTomitaRoot_real_graph_closed P)
    (scalarTomitaSquare_norm_match P)

theorem scalarTomitaRootDomain_le_closed :
    (scalarTomitaPositiveRoot P).domain ≤ scalarClosedTomitaDomain P :=
  graphCore_norm_domain_transfer (scalarTomitaPositiveRoot P).domain
    (scalarClosedTomitaDomain P) (scalarTomitaSquare P).domain
    ((scalarTomitaPositiveRoot P).toFun.restrictScalars ℝ)
    (antilinearRealMap (scalarClosedTomitaDomain P) (scalarClosedTomita P))
    (scalarTomitaSquareDomain_le_root P) (scalarTomitaSquareDomain_le P)
    (scalarTomitaSquare_root_graph_core P) (scalarClosedTomita_is_closed (P := P))
    (fun x => (scalarTomitaSquare_norm_match P x).symm)

/-- Exact equality on the original GNS space, not an unspecified equivalent model. -/
theorem scalarTomitaPositiveRoot_domain_eq :
    (scalarTomitaPositiveRoot P).domain = scalarClosedTomitaDomain P :=
  le_antisymm (scalarTomitaRootDomain_le_closed P) (scalarClosedTomitaDomain_le_root P)

/-- The norm identity extends from the square domain to the full domain of S. -/
theorem scalarTomitaPositiveRoot_norm (x : scalarClosedTomitaDomain P) :
    ‖scalarTomitaPositiveRoot P (Submodule.inclusion (scalarClosedTomitaDomain_le_root P) x)‖ =
      ‖scalarClosedTomita P x‖ := by
  obtain ⟨y,hy,hn⟩ := graphCore_norm_extension (scalarClosedTomitaDomain P)
    (scalarTomitaPositiveRoot P).domain (scalarTomitaSquare P).domain
    (antilinearRealMap (scalarClosedTomitaDomain P) (scalarClosedTomita P))
    ((scalarTomitaPositiveRoot P).toFun.restrictScalars ℝ)
    (scalarTomitaSquareDomain_le P) (scalarTomitaSquareDomain_le_root P)
    (scalarTomitaSquare_graph_core P) (scalarTomitaRoot_real_graph_closed P)
    (scalarTomitaSquare_norm_match P) x
  have he : Submodule.inclusion (scalarClosedTomitaDomain_le_root P) x = y :=
    Subtype.ext hy.symm
  exact (congrArg (fun v => ‖scalarTomitaPositiveRoot P v‖) he).trans hn.symm

theorem scalarTomitaPositiveRoot_energy (x : scalarClosedTomitaDomain P) :
    ‖scalarTomitaPositiveRoot P (Submodule.inclusion (scalarClosedTomitaDomain_le_root P) x)‖^2 =
      ‖scalarClosedTomita P x‖^2 :=
  congrArg (fun a : ℝ => a^2) (scalarTomitaPositiveRoot_norm P x)

#print axioms scalarTomitaSquare_norm_match
#print axioms scalarClosedTomitaDomain_le_root
#print axioms scalarTomitaRootDomain_le_closed
#print axioms scalarTomitaPositiveRoot_domain_eq
#print axioms scalarTomitaPositiveRoot_norm
#print axioms scalarTomitaPositiveRoot_energy
end
end TGLV350.Regular
