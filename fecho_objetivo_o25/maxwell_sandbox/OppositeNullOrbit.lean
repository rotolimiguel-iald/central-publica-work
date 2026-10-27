import OppositeNullIntegrability

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! Opposite-null integrability on the entire boost orbit. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open TGLExt.NullMomentumInvariant
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions

/-- Every boost translate of a coherent AxisCompact label has integrable opposite momentum. -/
theorem axisCompact_calibrated_oppositeMomentum_orbit_integrable {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (hh : AxisCompactProfile h.val)
    (s : ℝ) :
    Integrable (oppositeMomentumIntegrand
      (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      ((lightBoost A.toCertificate).V s (regularExponential h).val)) := by
  exact oppositeMomentumIntegrable_boost (lightBoost A.toCertificate)
    (toStress (regularMaxwellCalibratedForm A)) s (regularExponential h).val
    (axisCompact_calibrated_oppositeMomentum_integrable A h hh)

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.axisCompact_calibrated_oppositeMomentum_orbit_integrable
