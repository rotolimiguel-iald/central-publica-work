import TGLExt.V350ScalarTomitaRootDomain
import TGLExt.V350PartialSelfadjointRange
import TGLExt.V350DenseAntilinearExtension

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable (P : SiteProfile)

theorem scalarTomitaPositiveRoot_denseRange : DenseRange (scalarTomitaPositiveRoot P).toFun :=
  partialSelfadjoint_denseRange (scalarTomitaPositiveRoot P)
    (scalarTomitaPositiveRoot_dense P) (scalarTomitaPositiveRoot_selfadjoint P)
    (scalarTomitaPositiveRoot_zero_only P)

/-- S read on the already proved identical root domain. -/
def scalarTomitaRootImage :
    (scalarTomitaPositiveRoot P).domain →ₛₗ[starRingEnd ℂ] ScalarGNSHilbert P :=
  (scalarClosedTomita P).comp (Submodule.inclusion (scalarTomitaRootDomain_le_closed P))

theorem scalarTomitaRootImage_norm (x : (scalarTomitaPositiveRoot P).domain) :
    ‖scalarTomitaRootImage P x‖=‖scalarTomitaPositiveRoot P x‖ := by
  have h := scalarTomitaPositiveRoot_norm P
    (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) x)
  have he : Submodule.inclusion (scalarClosedTomitaDomain_le_root P)
      (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) x)=x := Subtype.ext rfl
  rw [he] at h
  exact h.symm

theorem scalarTomitaRootImage_denseRange : DenseRange (scalarTomitaRootImage P) := by
  apply Dense.mono ?_ (scalarClosedTomita_domain_dense (P := P))
  intro y hy
  let x : scalarClosedTomitaDomain P := ⟨y,hy⟩
  refine ⟨⟨scalarClosedTomita P x,
    scalarClosedTomitaDomain_le_root P (scalarClosedTomita_maps_domain x)⟩,?_⟩
  change scalarClosedTomita P ⟨scalarClosedTomita P x,_⟩=y
  exact scalarClosedTomita_involutive x

/-- The polar factor is constructed as an antiunitary on the original H_I.
This declaration alone does not claim U^2=1 or identify a modular weight. -/
def scalarTomitaPolarFactor : ScalarGNSHilbert P ≃ₛₗᵢ[starRingEnd ℂ] ScalarGNSHilbert P :=
  denseAntilinearEquiv (scalarTomitaRootImage P) (scalarTomitaPositiveRoot P).toFun
    (scalarTomitaPositiveRoot_denseRange P) (scalarTomitaRootImage_norm P)
    (scalarTomitaRootImage_denseRange P)

theorem scalarTomitaPolarFactor_root (x : (scalarTomitaPositiveRoot P).domain) :
    scalarTomitaPolarFactor P (scalarTomitaPositiveRoot P x)=scalarTomitaRootImage P x :=
  denseAntilinearEquiv_apply _ _ _ _ _ x

/-- Exact S=UB on the full domain D(S), with both maps on the same H_I. -/
theorem scalarTomitaPolarFactor_factorization (x : scalarClosedTomitaDomain P) :
    scalarTomitaPolarFactor P
      (scalarTomitaPositiveRoot P (Submodule.inclusion (scalarClosedTomitaDomain_le_root P) x))=
        scalarClosedTomita P x :=
  scalarTomitaPolarFactor_root P (Submodule.inclusion (scalarClosedTomitaDomain_le_root P) x)

theorem scalarTomitaPolarFactor_norm (x : ScalarGNSHilbert P) :
    ‖scalarTomitaPolarFactor P x‖=‖x‖ := (scalarTomitaPolarFactor P).norm_map x

theorem scalarTomitaPolarFactor_surjective : Function.Surjective (scalarTomitaPolarFactor P) :=
  (scalarTomitaPolarFactor P).surjective

#print axioms scalarTomitaPositiveRoot_denseRange
#print axioms scalarTomitaRootImage
#print axioms scalarTomitaRootImage_norm
#print axioms scalarTomitaRootImage_denseRange
#print axioms scalarTomitaPolarFactor
#print axioms scalarTomitaPolarFactor_root
#print axioms scalarTomitaPolarFactor_factorization
#print axioms scalarTomitaPolarFactor_norm
#print axioms scalarTomitaPolarFactor_surjective
end
end TGLV350.Regular
