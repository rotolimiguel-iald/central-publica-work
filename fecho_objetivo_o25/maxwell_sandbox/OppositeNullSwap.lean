import OppositeNullOrbit
import ConstructedRealNullStressMomentR1
import CoherentNullPositivity

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! The opposite lift is an involution swapping the two null densities. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open TGLExt.NullEnergyScaling TGLExt.NullMomentumInvariant
open F1Fecho.MaxwellStress ChatgptAudit.WignerRapidityMeasure016 F1Fecho.NullFrequency
open F1Fecho.WeightedPlancherel F1Fecho.OrbitalScreen
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore F1Fecho.CoherentKernel
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions

/-- The fiber sign is involutive. -/
theorem oppositeFiberSign_involutive (v : Fiber) :
    oppositeFiberSign (oppositeFiberSign v) = v := by
  ext j
  simp only [oppositeFiberSign_apply]
  by_cases hj : j = 0 <;> simp [hj]

/-- Longitudinal reflection is involutive on the one-particle space. -/
theorem momentumReflectionH1_involutive (h : H1) :
    momentumReflectionH1 (momentumReflectionH1 h) = h := by
  apply Lp.ext
  filter_upwards [Lp.coeFn_compMeasurePreserving (momentumReflectionH1 h)
      longitudinalReflection_measurePreserving,
    longitudinalReflection_measurePreserving.quasiMeasurePreserving.ae
      (Lp.coeFn_compMeasurePreserving h longitudinalReflection_measurePreserving)] with y hy hy'
  change (Lp.compMeasurePreserving longitudinalReflectionEquiv
    longitudinalReflection_measurePreserving (momentumReflectionH1 h)) y = h y
  rw [hy]
  change (Lp.compMeasurePreserving longitudinalReflectionEquiv
    longitudinalReflection_measurePreserving h) (longitudinalReflectionEquiv y) = h y
  rw [hy']
  change h (longitudinalReflectionEquiv (longitudinalReflectionEquiv y)) = h y
  have hr : longitudinalReflectionEquiv (longitudinalReflectionEquiv y) = y :=
    longitudinalReflection_involutive y
  rw [hr]

/-- Reflection and fiber sign together form an involution. -/
theorem oppositeLift_involutive (h : H1) : oppositeLift (oppositeLift h) = h := by
  apply Lp.ext
  filter_upwards [fiberLiftMap_ae oppositeFiberSign (momentumReflectionH1 (oppositeLift h)),
    Lp.coeFn_compMeasurePreserving (oppositeLift h) longitudinalReflection_measurePreserving,
    longitudinalReflection_measurePreserving.quasiMeasurePreserving.ae
      (fiberLiftMap_ae oppositeFiberSign (momentumReflectionH1 h)),
    longitudinalReflection_measurePreserving.quasiMeasurePreserving.ae
      (Lp.coeFn_compMeasurePreserving h longitudinalReflection_measurePreserving)]
      with y ho hr hi hh
  change fiberLiftMap oppositeFiberSign (momentumReflectionH1 (oppositeLift h)) y = h y
  rw [ho]
  change oppositeFiberSign ((Lp.compMeasurePreserving longitudinalReflectionEquiv
    longitudinalReflection_measurePreserving (oppositeLift h)) y) = h y
  rw [hr]
  change oppositeFiberSign ((fiberLiftMap oppositeFiberSign (momentumReflectionH1 h))
    (longitudinalReflectionEquiv y)) = h y
  rw [hi]
  change oppositeFiberSign (oppositeFiberSign ((Lp.compMeasurePreserving
    longitudinalReflectionEquiv longitudinalReflection_measurePreserving h)
      (longitudinalReflectionEquiv y))) = h y
  rw [hh]
  change oppositeFiberSign (oppositeFiberSign
    (h (longitudinalReflectionEquiv (longitudinalReflectionEquiv y)))) = h y
  have hr' : longitudinalReflectionEquiv (longitudinalReflectionEquiv y) = y :=
    longitudinalReflection_involutive y
  rw [hr']
  exact oppositeFiberSign_involutive _

/-- The opposite lift is norm preserving. -/
theorem oppositeLift_norm (h : H1) : ‖oppositeLift h‖ = ‖h‖ := by
  unfold oppositeLift momentumReflectionH1
  rw [(fiberLift oppositeFiberSign).norm_map]
  exact (Lp.compMeasurePreservingₗᵢ ℂ longitudinalReflectionEquiv
    longitudinalReflection_measurePreserving).norm_map h

/-- The opposite density of `h` is the direct density of `oppositeLift h`. -/
theorem axisCompact_realOppositeStress3D_eq_direct (h : H1) (hh : AxisCompactProfile h)
    (x : NullFourierSpace) :
    realOppositeStress3D h x = realNullStress (oppositeLift h) x := by
  rw [axisCompact_realOppositeStress3D h hh,
    axisCompact_realNullStress (oppositeLift h) (axisCompactProfile_oppositeLift h hh)]
  rfl

/-- Real diagonal coherent stress with the exponential normalization made explicit. -/
theorem axisCompact_coherentNullStress_diag_eq (h : H1) (hh : AxisCompactProfile h)
    (x : NullFourierSpace) :
    (unitaryFourierCoherentNullStress h h x).re =
      unitaryFourierStressScale * Real.exp (‖h‖ ^ 2) * realNullStress h x := by
  have hi : inner ℂ h h = ((‖h‖ ^ 2 : ℝ) : ℂ) := by
    rw [← inner_self_ofReal_re, inner_self_eq_norm_sq]
    norm_cast
  have he : Complex.exp (inner ℂ h h) = (Real.exp (‖h‖ ^ 2) : ℂ) := by
    rw [hi]
    exact (Complex.ofReal_exp _).symm
  unfold unitaryFourierCoherentNullStress unitaryFourierCoherentStress realNullStress
  simp_rw [coherentProfileStress_diagonal]
  rw [he]
  simp only [Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero,
    realProfileStress_im_zero, Complex.add_re]
  ring

/-- Direct null momentum of a coherent AxisCompact exponential in Fourier coordinates. -/
theorem calibrated_nullPlaneMomentum_exponential_eq {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (hh : AxisCompactProfile h.val) :
    nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val =
      ∫ x : NullFourierSpace,
        unitaryFourierStressScale * Real.exp (‖h.val‖ ^ 2) * realNullStress h.val x := by
  unfold nullPlaneMomentum momentumIntegrand
  calc
    _ = ∫ z : ℝ × Transverse,
        (unitaryFourierFockNullStress (regularExponential h) (regularExponential h)
          (nullContractCoordinateEquiv z)).re := by
      apply integral_congr_ae
      filter_upwards [] with z
      exact calibrated_nullEnergy_contract_coordinates A (regularExponential h) z
    _ = ∫ z : ℝ × Transverse,
        (unitaryFourierCoherentNullStress h.val h.val (nullContractCoordinateEquiv z)).re := by
      simp_rw [unitaryFourierFockNullStress_exponential]
    _ = ∫ z : ℝ × Transverse,
        unitaryFourierStressScale * Real.exp (‖h.val‖ ^ 2) *
          realNullStress h.val (nullContractCoordinateEquiv z) := by
      apply integral_congr_ae
      filter_upwards [] with z
      exact axisCompact_coherentNullStress_diag_eq h.val hh (nullContractCoordinateEquiv z)
    _ = _ := by
      simpa only [MeasureTheory.Measure.volume_eq_prod] using
        (nullContractCoordinateEquiv_measurePreserving.integral_comp'
          (fun x : NullFourierSpace =>
            unitaryFourierStressScale * Real.exp (‖h.val‖ ^ 2) * realNullStress h.val x))

/-- Opposite null momentum of a coherent AxisCompact exponential in Fourier coordinates. -/
theorem calibrated_oppositeNullPlaneMomentum_exponential_eq {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (hh : AxisCompactProfile h.val) :
    oppositeNullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val =
      ∫ x : NullFourierSpace, unitaryFourierRealOppositeStress h.val
        (oppositeNullPlanePoint (x 0) (nullFourierScreen x)) := by
  unfold oppositeNullPlaneMomentum oppositeMomentumIntegrand
  calc
    _ = ∫ z : ℝ × Transverse, unitaryFourierRealOppositeStress h.val
        (oppositeNullPlanePoint ((nullContractCoordinateEquiv z) 0)
          (nullFourierScreen (nullContractCoordinateEquiv z))) := by
      apply integral_congr_ae
      filter_upwards [] with z
      rw [nullContractCoordinateEquiv_oppositePlane]
      exact calibrated_oppositeNullEnergy_exponential A h _
    _ = _ := by
      simpa only [MeasureTheory.Measure.volume_eq_prod] using
        (nullContractCoordinateEquiv_measurePreserving.integral_comp'
          (fun x : NullFourierSpace => unitaryFourierRealOppositeStress h.val
            (oppositeNullPlanePoint (x 0) (nullFourierScreen x))))

/-- The opposite lift as a regular coherent label on the same AxisCompact core. -/
def oppositeLiftLabel (h : RegularLabel) (hh : AxisCompactProfile h.val) : RegularLabel :=
  ⟨oppositeLift h.val, axisCompactProfile_strongRegular _ (axisCompactProfile_oppositeLift h.val hh)⟩

theorem axisCompactProfile_oppositeLiftLabel (h : RegularLabel) (hh : AxisCompactProfile h.val) :
    AxisCompactProfile (oppositeLiftLabel h hh).val :=
  axisCompactProfile_oppositeLift h.val hh

theorem oppositeLiftLabel_involutive (h : RegularLabel) (hh : AxisCompactProfile h.val) :
    oppositeLiftLabel (oppositeLiftLabel h hh) (axisCompactProfile_oppositeLiftLabel h hh) = h := by
  apply Subtype.ext
  exact oppositeLift_involutive h.val

/-- The opposite lift exchanges the calibrated null momenta. -/
theorem calibrated_oppositeNullPlaneMomentum_eq_direct {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (hh : AxisCompactProfile h.val) :
    oppositeNullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val =
    nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential (oppositeLiftLabel h hh)).val := by
  rw [calibrated_oppositeNullPlaneMomentum_exponential_eq A h hh,
    calibrated_nullPlaneMomentum_exponential_eq A (oppositeLiftLabel h hh)
      (axisCompactProfile_oppositeLiftLabel h hh)]
  apply integral_congr_ae
  filter_upwards [] with x
  simp only [unitaryFourierRealOppositeStress, oppositeLiftLabel, oppositeLift_norm]
  change unitaryFourierStressScale * Real.exp (‖h.val‖ ^ 2) * realOppositeStress3D h.val x = _
  rw [axisCompact_realOppositeStress3D_eq_direct h.val hh]

/-- A direct positive momentum becomes positive opposite momentum after the lift. -/
theorem calibrated_oppositeNullPlaneMomentum_oppositeLift_pos {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (hh : AxisCompactProfile h.val)
    (hp : 0 < nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val) :
    0 < oppositeNullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential (oppositeLiftLabel h hh)).val := by
  rw [calibrated_oppositeNullPlaneMomentum_eq_direct A (oppositeLiftLabel h hh)
    (axisCompactProfile_oppositeLiftLabel h hh), oppositeLiftLabel_involutive]
  exact hp

/-- Concrete coherent AxisCompact witness with strictly positive opposite null momentum. -/
theorem exists_axisCompact_oppositeNullPlaneMomentum_pos {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) :
    ∃ h : RegularLabel, AxisCompactProfile h.val ∧
      0 < oppositeNullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
        (regularExponential h).val := by
  obtain ⟨h, hh, hb⟩ := exists_axisCompact_nonzero_boostPair
  let label : RegularLabel := ⟨h, axisCompactProfile_strongRegular h hh⟩
  have hQ : nullPlaneCharge (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential label).val ≠ 0 := by
    rw [calibrated_nullPlaneCharge_eq_moment,
      axisCompact_fockNullStress_real_moment (regularExponential label)
        (axisCompactFock_exponential label hh),
      regularFockBoostPair_exponential, coherentBoostPair_diagonal_im]
    exact mul_ne_zero (ne_of_gt (Real.exp_pos _)) hb
  have hp := nullPlaneMomentum_pos_of_charge_ne_zero A label hh hQ
  exact ⟨oppositeLiftLabel label hh, axisCompactProfile_oppositeLiftLabel label hh,
    calibrated_oppositeNullPlaneMomentum_oppositeLift_pos A label hh hp⟩

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.oppositeFiberSign_involutive
#print axioms F1Fecho.MaxwellGlobal.momentumReflectionH1_involutive
#print axioms F1Fecho.MaxwellGlobal.oppositeLift_involutive
#print axioms F1Fecho.MaxwellGlobal.oppositeLift_norm
#print axioms F1Fecho.MaxwellGlobal.axisCompact_realOppositeStress3D_eq_direct
#print axioms F1Fecho.MaxwellGlobal.axisCompact_coherentNullStress_diag_eq
#print axioms F1Fecho.MaxwellGlobal.calibrated_nullPlaneMomentum_exponential_eq
#print axioms F1Fecho.MaxwellGlobal.calibrated_oppositeNullPlaneMomentum_exponential_eq
#print axioms F1Fecho.MaxwellGlobal.oppositeLiftLabel_involutive
#print axioms F1Fecho.MaxwellGlobal.calibrated_oppositeNullPlaneMomentum_eq_direct
#print axioms F1Fecho.MaxwellGlobal.calibrated_oppositeNullPlaneMomentum_oppositeLift_pos
#print axioms F1Fecho.MaxwellGlobal.exists_axisCompact_oppositeNullPlaneMomentum_pos
