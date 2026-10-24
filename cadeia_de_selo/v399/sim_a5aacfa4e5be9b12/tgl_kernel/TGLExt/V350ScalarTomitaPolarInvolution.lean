import TGLExt.V350AntiunitaryPositiveConjugation
import TGLExt.V350ScalarTomitaPolarResolvent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt ChatgptAudit.Continuous049
noncomputable section
variable (P : SiteProfile)

theorem scalarTomitaPolar_conjugate_resolvent :
    antiunitaryConjugate (scalarTomitaPolarFactor P) (scalarTomitaResolvent P)=
      1-scalarTomitaResolvent P := by
  apply ContinuousLinearMap.ext
  intro x
  have h := scalarTomitaPolarFactor_resolvent P ((scalarTomitaPolarFactor P).symm x)
  simpa only [antiunitaryConjugate_apply,LinearIsometryEquiv.apply_symm_apply,
    ContinuousLinearMap.sub_apply,ContinuousLinearMap.one_apply] using h

theorem scalarTomitaPolar_conjugate_complement :
    antiunitaryConjugate (scalarTomitaPolarFactor P) (1-scalarTomitaResolvent P)=
      scalarTomitaResolvent P := by
  apply ContinuousLinearMap.ext
  intro x
  change scalarTomitaPolarFactor P ((scalarTomitaPolarFactor P).symm x -
    scalarTomitaResolvent P ((scalarTomitaPolarFactor P).symm x))=scalarTomitaResolvent P x
  rw [map_sub,LinearIsometryEquiv.apply_symm_apply,
    scalarTomitaPolarFactor_resolvent P ((scalarTomitaPolarFactor P).symm x),
    LinearIsometryEquiv.apply_symm_apply]
  abel

theorem scalarTomitaPolar_sqrt_resolvent (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P (hilbertPositiveSqrt (scalarTomitaResolvent P) x)=
      hilbertPositiveSqrt (1-scalarTomitaResolvent P) (scalarTomitaPolarFactor P x) := by
  have h := (antiunitaryConjugate_sqrt (scalarTomitaPolarFactor P)
    (scalarTomitaResolvent P) (scalarTomitaResolvent_nonneg P)).symm.trans
      (congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => hilbertPositiveSqrt T)
        (scalarTomitaPolar_conjugate_resolvent P))
  have hv := congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
    T (scalarTomitaPolarFactor P x)) h
  simpa only [antiunitaryConjugate_apply,LinearIsometryEquiv.symm_apply_apply,hilbertPositiveSqrt] using hv

theorem scalarTomitaPolar_sqrt_complement (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P (hilbertPositiveSqrt (1-scalarTomitaResolvent P) x)=
      hilbertPositiveSqrt (scalarTomitaResolvent P) (scalarTomitaPolarFactor P x) := by
  have h := (antiunitaryConjugate_sqrt (scalarTomitaPolarFactor P)
    (1-scalarTomitaResolvent P) (hilbertComplement_nonneg _ (scalarTomitaResolvent_le_one P))).symm.trans
      (congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => hilbertPositiveSqrt T)
        (scalarTomitaPolar_conjugate_complement P))
  have hv := congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
    T (scalarTomitaPolarFactor P x)) h
  simpa only [antiunitaryConjugate_apply,LinearIsometryEquiv.symm_apply_apply,hilbertPositiveSqrt] using hv

def scalarTomitaRootLift (x : ScalarGNSHilbert P) : (scalarTomitaPositiveRoot P).domain :=
  boundedGraphLift (hilbertPositiveSqrt (scalarTomitaResolvent P)) (hilbertPositiveSqrt (1-scalarTomitaResolvent P))
    (positive_sqrt_injective _ (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_injective P)) x

theorem scalarTomitaRootLift_coe (x : ScalarGNSHilbert P) :
    (scalarTomitaRootLift P x : ScalarGNSHilbert P)=hilbertPositiveSqrt (scalarTomitaResolvent P) x := rfl

theorem scalarTomita_sqrt_factor (x : ScalarGNSHilbert P) :
    scalarClosedTomita P (Submodule.inclusion (scalarTomitaRootDomain_le_closed P)
      (scalarTomitaRootLift P x)) =
        scalarTomitaPolarFactor P (hilbertPositiveSqrt (1-scalarTomitaResolvent P) x) :=
  (scalarTomitaPolarFactor_root P (scalarTomitaRootLift P x)).symm.trans
    (congrArg (scalarTomitaPolarFactor P) (bounded_graph_lift_apply _ _ _ x))

/-- Involution is proved from the original S, its resolvent and the positive root.
It is not inserted as a premise of the polar construction. -/
theorem scalarTomitaPolarFactor_involutive : Function.Involutive (scalarTomitaPolarFactor P) := by
  have hd : DenseRange (hilbertPositiveSqrt (scalarTomitaResolvent P) :
      ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := scalarTomitaPositiveRoot_dense P
  intro z
  refine hd.induction ?_ (isClosed_eq (by fun_prop) continuous_id) z
  rintro _ ⟨v,rfl⟩
  let x := Submodule.inclusion (scalarTomitaRootDomain_le_closed P) (scalarTomitaRootLift P v)
  have he : (⟨scalarClosedTomita P x,scalarClosedTomita_maps_domain x⟩ : scalarClosedTomitaDomain P)=
      Submodule.inclusion (scalarTomitaRootDomain_le_closed P)
        (scalarTomitaRootLift P (scalarTomitaPolarFactor P v)) :=
    Subtype.ext ((scalarTomita_sqrt_factor P v).trans (scalarTomitaPolar_sqrt_complement P v))
  have h : hilbertPositiveSqrt (scalarTomitaResolvent P) v =
      scalarTomitaPolarFactor P
        (hilbertPositiveSqrt (1-scalarTomitaResolvent P) (scalarTomitaPolarFactor P v)) :=
    (scalarClosedTomita_involutive x).symm.trans
      ((congrArg (scalarClosedTomita P) he).trans
        (scalarTomita_sqrt_factor P (scalarTomitaPolarFactor P v)))
  exact (congrArg (scalarTomitaPolarFactor P) (scalarTomitaPolar_sqrt_resolvent P v)).trans h.symm

#print axioms scalarTomitaPolar_conjugate_resolvent
#print axioms scalarTomitaPolar_conjugate_complement
#print axioms scalarTomitaPolar_sqrt_resolvent
#print axioms scalarTomitaPolar_sqrt_complement
#print axioms scalarTomitaRootLift
#print axioms scalarTomitaRootLift_coe
#print axioms scalarTomita_sqrt_factor
#print axioms scalarTomitaPolarFactor_involutive
end
end TGLV350.Regular
