import OppositeNullSimultaneous
import TGLExt.FutureNullDynamics

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! A concrete inhabited FutureNullState from the calibrated Maxwell realization. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open TGLExt.NullEnergyScaling TGLExt.NullMomentumInvariant TGLExt.NullRestSector
open TGLExt.FutureNullDynamics
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions

/-- The concrete future state: both boost orbits integrable and both components positive. -/
noncomputable def axisCompactFutureNullState {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) :
    FutureNullState (lightBoost A.toCertificate) (toStress (regularMaxwellCalibratedForm A)) := by
  let h : RegularLabel := Classical.choose (exists_axisCompact_bothNullMomenta_pos A)
  have hh : AxisCompactProfile h.val := (Classical.choose_spec
    (exists_axisCompact_bothNullMomenta_pos A)).1
  have hp : 0 < nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val := (Classical.choose_spec
    (exists_axisCompact_bothNullMomenta_pos A)).2.1
  have hm : 0 < oppositeNullPlaneMomentum
      (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val := (Classical.choose_spec
    (exists_axisCompact_bothNullMomenta_pos A)).2.2
  exact {
    vec := (regularExponential h).val
    integrablePlus := by
      intro s
      exact momentumIntegrable_boost (lightBoost A.toCertificate)
        (toStress (regularMaxwellCalibratedForm A)) s (regularExponential h).val
        (axisCompact_calibrated_nullMomentum_integrable A (regularExponential h)
          (axisCompactFock_exponential h hh))
    integrableMinus := by
      intro s
      exact axisCompact_calibrated_oppositeMomentum_orbit_integrable A h hh s
    plus_pos := hp
    minus_pos := hm }

/-- The concrete state has strictly positive invariant mass. -/
theorem axisCompactFutureNullState_mass_pos {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) :
    0 < invariantMass (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (axisCompactFutureNullState A).vec :=
  invariantMass_pos (lightBoost A.toCertificate) (toStress (regularMaxwellCalibratedForm A))
    (axisCompactFutureNullState A)

/-- Its invariant mass is constant along the boost orbit. -/
theorem axisCompactFutureNullState_mass_boost {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (s : ℝ) :
    invariantMass (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (futureBoost (lightBoost A.toCertificate) (toStress (regularMaxwellCalibratedForm A)) s
        (axisCompactFutureNullState A)).vec =
    invariantMass (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (axisCompactFutureNullState A).vec :=
  invariantMass_boost (lightBoost A.toCertificate) (toStress (regularMaxwellCalibratedForm A))
    s (axisCompactFutureNullState A)

/-- The constructed rest frame has zero longitudinal momentum. -/
theorem axisCompactFutureNullState_rest_momentum_zero {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) :
    longitudinalMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (futureRestFrame (lightBoost A.toCertificate) (toStress (regularMaxwellCalibratedForm A))
        (axisCompactFutureNullState A)).vec = 0 :=
  futureRestFrame_momentum_zero (lightBoost A.toCertificate)
    (toStress (regularMaxwellCalibratedForm A)) (axisCompactFutureNullState A)

/-- Rest energy is the invariant mass computed in the original concrete state. -/
theorem axisCompactFutureNullState_rest_energy {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) :
    energyReading (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (futureRestFrame (lightBoost A.toCertificate) (toStress (regularMaxwellCalibratedForm A))
        (axisCompactFutureNullState A)).vec =
    invariantMass (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (axisCompactFutureNullState A).vec :=
  futureRestFrame_energy (lightBoost A.toCertificate) (toStress (regularMaxwellCalibratedForm A))
    (axisCompactFutureNullState A)

/-- The concrete rest energy is strictly positive. -/
theorem axisCompactFutureNullState_rest_energy_pos {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) :
    0 < energyReading (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (futureRestFrame (lightBoost A.toCertificate) (toStress (regularMaxwellCalibratedForm A))
        (axisCompactFutureNullState A)).vec :=
  futureRestFrame_energy_pos (lightBoost A.toCertificate)
    (toStress (regularMaxwellCalibratedForm A)) (axisCompactFutureNullState A)

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.axisCompactFutureNullState
#print axioms F1Fecho.MaxwellGlobal.axisCompactFutureNullState_mass_pos
#print axioms F1Fecho.MaxwellGlobal.axisCompactFutureNullState_mass_boost
#print axioms F1Fecho.MaxwellGlobal.axisCompactFutureNullState_rest_momentum_zero
#print axioms F1Fecho.MaxwellGlobal.axisCompactFutureNullState_rest_energy
#print axioms F1Fecho.MaxwellGlobal.axisCompactFutureNullState_rest_energy_pos
