import TGLExt.V351AntiunitaryResolventPhase
import TGLExt.V351ScalarTomitaImaginaryPowers
import TGLExt.V350ScalarTomitaPolarInvolution

set_option autoImplicit false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt
noncomputable section

/-- The original polar antiunitary commutes with the original resolvent phase group.
This is not yet identification of the modular action with regular conjugation. -/
theorem scalarTomitaImaginaryPower_polar_commutes (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P (scalarTomitaImaginaryPower P t x) =
      scalarTomitaImaginaryPower P t (scalarTomitaPolarFactor P x) :=
  resolventImaginaryPower_antiunitary (scalarTomitaPolarFactor P)
    (scalarTomitaResolvent P) (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_le_one P)
    (scalarTomitaResolvent_injective P) (scalarTomitaResolvent_complement_injective P)
    (scalarTomitaPolar_conjugate_resolvent P) t x

theorem scalarTomitaImaginaryPower_polar_conjugate (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P
      (scalarTomitaImaginaryPower P t ((scalarTomitaPolarFactor P).symm x)) =
        scalarTomitaImaginaryPower P t x := by
  rw [scalarTomitaImaginaryPower_polar_commutes, LinearIsometryEquiv.apply_symm_apply]

/-- Equality of bounded complex-linear operators, not just a formal pairing. -/
theorem scalarTomitaImaginaryPower_polar_operator (P : SiteProfile) (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarTomitaImaginaryPower P t).toLinearIsometry.toContinuousLinearMap =
        (scalarTomitaImaginaryPower P t).toLinearIsometry.toContinuousLinearMap := by
  apply ContinuousLinearMap.ext
  intro x
  exact scalarTomitaImaginaryPower_polar_conjugate P t x

#print axioms scalarTomitaImaginaryPower_polar_commutes
#print axioms scalarTomitaImaginaryPower_polar_conjugate
#print axioms scalarTomitaImaginaryPower_polar_operator
end
end TGLV350.Regular
