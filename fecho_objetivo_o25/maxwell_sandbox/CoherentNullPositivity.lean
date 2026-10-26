import AxisCompactNullMomentum
import AxisCompactFockNonzeroEnergyR4
import TGLExt.NullEnergyScaling

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! Positivity of the coherent null density and strict positivity of its integral
when the modular charge is nonzero. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open TGLExt.NullEnergyScaling
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore F1Fecho.CoherentKernel
open F1Fecho.WeightedPlancherel F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open ChatgptAudit.WignerRapidityMeasure016
open scoped FourierTransform

private theorem coherent_square_eq_real (a : ℂ) :
    ((Real.sqrt 2 : ℂ)⁻¹ * ((starRingEnd ℂ) a + a))^2 = (2 * a.re ^ 2 : ℂ) := by
  have ha : (starRingEnd ℂ) a + a = (2 * a.re : ℂ) := by
    apply Complex.ext <;> simp [Complex.add_re, Complex.add_im] <;> ring
  have hs : (Real.sqrt 2 : ℂ)^2 = 2 := by
    exact_mod_cast Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)
  have hi : ((Real.sqrt 2 : ℂ)⁻¹)^2 = (1 / 2 : ℂ) := by
    rw [inv_pow, hs]
    norm_num
  rw [ha, mul_pow, hi]
  push_cast
  ring

private theorem coherent_square_re_nonneg (a : ℂ) :
    0 ≤ (((Real.sqrt 2 : ℂ)⁻¹ * ((starRingEnd ℂ) a + a))^2).re := by
  rw [coherent_square_eq_real]
  norm_cast
  positivity

/-- The diagonal coherent null density is real and nonnegative. -/
theorem axisCompact_coherentNullStress_diag_nonneg (h : H1) (hh : AxisCompactProfile h)
    (x : NullFourierSpace) : 0 ≤ (unitaryFourierCoherentNullStress h h x).re := by
  rw [axisCompact_coherentNullStress h h hh hh x]
  have hi : inner ℂ h h = ((‖h‖ ^ 2 : ℝ) : ℂ) := by
    rw [← inner_self_ofReal_re, inner_self_eq_norm_sq]
    norm_cast
  have he : Complex.exp (inner ℂ h h) = (Real.exp (‖h‖ ^ 2) : ℂ) := by
    rw [hi]
    exact (Complex.ofReal_exp _).symm
  rw [he, coherent_square_eq_real, coherent_square_eq_real]
  norm_cast
  unfold unitaryFourierStressScale
  positivity

/-- The finite-Fock stress reduces to the coherent stress on an exponential vector. -/
theorem unitaryFourierFockNullStress_exponential (h : RegularLabel) (x : NullFourierSpace) :
    unitaryFourierFockNullStress (regularExponential h) (regularExponential h) x =
      unitaryFourierCoherentNullStress h.val h.val x := by
  simp only [unitaryFourierFockNullStress, unitaryFourierPointStressForm,
    pointStressForm_exponential, unitaryFourierCoherentNullStress,
    unitaryFourierCoherentStress]

/-- Positivity of the calibrated null density on a coherent AxisCompact vector. -/
theorem calibrated_nullEnergy_exponential_nonneg {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (hh : AxisCompactProfile h.val)
    (z : ℝ × (Fin 2 → ℝ)) :
    0 ≤ nullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val (z.1 • nullDir + screenEmbed z.2) := by
  rw [calibrated_nullEnergy_contract_coordinates, unitaryFourierFockNullStress_exponential]
  exact axisCompact_coherentNullStress_diag_nonneg h.val hh
    (nullContractCoordinateEquiv z)

/-- If the charge is nonzero, a nonnegative integrable null density cannot have
    zero unweighted integral. -/
theorem nullPlaneMomentum_ne_zero_of_charge_ne_zero {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (hh : AxisCompactProfile h.val)
    (hQ : nullPlaneCharge (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val ≠ 0) :
    nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val ≠ 0 := by
  have hi := axisCompact_calibrated_nullMomentum_integrable A (regularExponential h)
    (axisCompactFock_exponential h hh)
  have hnonneg := calibrated_nullEnergy_exponential_nonneg A h hh
  intro hzero
  have hae := (integral_eq_zero_iff_of_nonneg hnonneg hi).mp hzero
  apply hQ
  unfold nullPlaneCharge
  apply integral_eq_zero_of_ae
  filter_upwards [hae] with z hz
  simp [hz]

/-- Nonzero modular charge forces strictly positive null momentum. -/
theorem nullPlaneMomentum_pos_of_charge_ne_zero {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (hh : AxisCompactProfile h.val)
    (hQ : nullPlaneCharge (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val ≠ 0) :
    0 < nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val := by
  have hnonneg : 0 ≤ nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val := by
    unfold nullPlaneMomentum momentumIntegrand
    exact integral_nonneg (calibrated_nullEnergy_exponential_nonneg A h hh)
  exact lt_of_le_of_ne hnonneg (Ne.symm
    (nullPlaneMomentum_ne_zero_of_charge_ne_zero A h hh hQ))

/-- Concrete positive null momentum with integrability on the whole boost orbit. -/
theorem exists_axisCompact_nullPlaneMomentum_pos {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) :
    ∃ ψ : regularFockDomain, AxisCompactFock ψ ∧
      0 < nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ.val ∧
      ∀ s : ℝ, Integrable (momentumIntegrand
        (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
        ((lightBoost A.toCertificate).V s ψ.val)) := by
  obtain ⟨h, hh, hb⟩ := exists_axisCompact_nonzero_boostPair
  let label : RegularLabel := ⟨h, axisCompactProfile_strongRegular h hh⟩
  let ψ : regularFockDomain := regularExponential label
  have hψ : AxisCompactFock ψ := axisCompactFock_exponential label hh
  have hQ : nullPlaneCharge (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ.val ≠ 0 := by
    rw [calibrated_nullPlaneCharge_eq_moment, axisCompact_fockNullStress_real_moment ψ hψ,
      regularFockBoostPair_exponential, coherentBoostPair_diagonal_im]
    exact mul_ne_zero (ne_of_gt (Real.exp_pos _)) hb
  refine ⟨ψ, hψ, nullPlaneMomentum_pos_of_charge_ne_zero A label hh hQ, ?_⟩
  intro s
  exact momentumIntegrable_boost (lightBoost A.toCertificate) (toStress (regularMaxwellCalibratedForm A))
    s ψ.val (axisCompact_calibrated_nullMomentum_integrable A ψ hψ)

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.axisCompact_coherentNullStress_diag_nonneg
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierFockNullStress_exponential
#print axioms F1Fecho.MaxwellGlobal.calibrated_nullEnergy_exponential_nonneg
#print axioms F1Fecho.MaxwellGlobal.nullPlaneMomentum_ne_zero_of_charge_ne_zero
#print axioms F1Fecho.MaxwellGlobal.nullPlaneMomentum_pos_of_charge_ne_zero
#print axioms F1Fecho.MaxwellGlobal.exists_axisCompact_nullPlaneMomentum_pos
