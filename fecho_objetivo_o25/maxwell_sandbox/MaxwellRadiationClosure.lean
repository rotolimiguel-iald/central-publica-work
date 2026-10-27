import OppositeNullSimultaneous
import RealProfileMaxwellNonzeroR3

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! Free-streaming radiation and its trace-free anisotropic response. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open F1Fecho.MaxwellStress ChatgptAudit.WignerRapidityMeasure016 F1Fecho.NullFrequency
open F1Fecho.WeightedPlancherel F1Fecho.OrbitalScreen

/-- Regular moments are preserved by longitudinal reflection. -/
theorem regularProfile_momentumReflection (h : H1) (hh : RegularProfile h) :
    RegularProfile (momentumReflectionH1 h) := by
  intro m
  have hi := longitudinalReflection_measurePreserving.integrable_comp_of_integrable (hh m)
  apply hi.congr
  filter_upwards [Lp.coeFn_compMeasurePreserving h longitudinalReflection_measurePreserving] with y hy
  change shellEnergy (longitudinalReflection y) ^ m * ‖h (longitudinalReflection y)‖ =
    shellEnergy y ^ m * ‖(Lp.compMeasurePreserving longitudinalReflectionEquiv
      longitudinalReflection_measurePreserving h) y‖
  simp only [Function.comp_apply] at hy
  have he : shellEnergy (longitudinalReflection y) = shellEnergy y := by
    simp [shellEnergy, energy, transverseMass, longitudinalReflection]
  rw [hy, he]
  simp only [longitudinalReflectionEquiv, MeasurableEquiv.ofInvolutive_apply]

/-- Regular moments are closed under addition. -/
theorem regularProfile_add (h k : H1) (hh : RegularProfile h) (hk : RegularProfile k) :
    RegularProfile (h + k) := by
  intro m
  have hi := (hh m).add (hk m)
  apply hi.mono' ((shellEnergy_continuous.pow m).aestronglyMeasurable.mul
    (Lp.aestronglyMeasurable (h + k)).norm)
  filter_upwards [Lp.coeFn_add h k] with y hy
  change |shellEnergy y ^ m * ‖(h + k) y‖| ≤ _
  rw [abs_of_nonneg (mul_nonneg (pow_nonneg (shellEnergy_nonneg y) m) (norm_nonneg _))]
  simp only [hy, Pi.add_apply]
  simpa [mul_add] using mul_le_mul_of_nonneg_left (norm_add_le (h y) (k y))
    (pow_nonneg (shellEnergy_nonneg y) m)

/-- Real parity of each Maxwell component under longitudinal reflection. -/
def momentumParitySignR (μ ν : Fin 4) : ℝ :=
  ![![1, 1, -1, -1], ![1, 1, 1, 1], ![-1, 1, 1, 1], ![-1, 1, 1, 1]] μ ν

/-- Parity of each Maxwell component under longitudinal reflection. -/
def momentumParitySign (μ ν : Fin 4) : ℂ := (momentumParitySignR μ ν : ℂ)

theorem momentumParitySignR_sq (μ ν : Fin 4) : momentumParitySignR μ ν * momentumParitySignR μ ν = 1 := by
  fin_cases μ <;> fin_cases ν <;> norm_num [momentumParitySignR]

/-- Exact parity of the Cartesian strength under longitudinal reflection. -/
theorem cartesianStrength_momentumReflection (y : MomentumCoordinates) (μ ν : Fin 4) :
    cartesianStrength (longitudinalReflection y) 0 μ ν =
      momentumParitySignR μ ν * cartesianStrength y 0 μ ν := by
  fin_cases μ <;> fin_cases ν <;>
    norm_num [momentumParitySignR, cartesianStrength, transverseRatio, transverseMass,
      shellEnergy, energy, longitudinalReflection, Matrix.of_apply,
      Matrix.cons_val_zero', Matrix.cons_val_succ']

/-- The profile density transforms by its exact component parity. -/
theorem profileDensity_momentumReflection (h : H1) (hs : ∀ᵐ y ∂orbitalMeasure 0, h y 1 = 0)
    (μ ν : Fin 4) :
    (fun y => profileDensity (momentumReflectionH1 h) μ ν y) =ᵐ[orbitalMeasure 0]
      (fun y => momentumParitySign μ ν * profileDensity h μ ν (longitudinalReflection y)) := by
  filter_upwards [Lp.coeFn_compMeasurePreserving h longitudinalReflection_measurePreserving,
    longitudinalReflection_measurePreserving.quasiMeasurePreserving.ae hs] with z hz hs1
  simp only [Function.comp_apply] at hz
  simp only [longitudinalReflectionEquiv, MeasurableEquiv.ofInvolutive_apply] at hs1
  change profileDensity (Lp.compMeasurePreserving longitudinalReflectionEquiv
    longitudinalReflection_measurePreserving h) μ ν z = _
  unfold profileDensity
  rw [hz]
  simp only [longitudinalReflectionEquiv, MeasurableEquiv.ofInvolutive_apply,
    Fin.sum_univ_two, hs1, PiLp.zero_apply, mul_zero, add_zero,
    cartesianStrength_momentumReflection, momentumParitySign, Finset.mul_sum,
    ← mul_assoc, ← Complex.ofReal_mul, momentumParitySignR_sq, Complex.ofReal_one, one_mul]

/-- The wave at the origin is the unphased profile-density integral. -/
theorem profileWave_zero_integral (h : H1) (μ ν : Fin 4) :
    profileWave h μ ν 0 = ∫ y, profileDensity h μ ν y ∂orbitalMeasure 0 := by
  simp [profileWave, wavePhase]

/-- Longitudinal reflection multiplies each wave by its component parity. -/
theorem profileWave_momentumReflection (h : H1) (hs : ∀ᵐ y ∂orbitalMeasure 0, h y 1 = 0)
    (μ ν : Fin 4) :
    profileWave (momentumReflectionH1 h) μ ν 0 = momentumParitySign μ ν * profileWave h μ ν 0 := by
  rw [profileWave_zero_integral, profileWave_zero_integral,
    ← integral_longitudinalReflection (profileDensity h μ ν), ← integral_const_mul]
  apply integral_congr_ae
  filter_upwards [profileDensity_momentumReflection h hs μ ν] with y hy
  exact hy

/-- Lower-wave parity at the origin. -/
theorem lowerProfileWave_momentumReflection (h : H1) (hs : ∀ᵐ y ∂orbitalMeasure 0, h y 1 = 0)
    (μ ν : Fin 4) :
    lowerProfileWave (momentumReflectionH1 h) μ ν 0 =
      momentumParitySign μ ν * lowerProfileWave h μ ν 0 := by
  unfold lowerProfileWave
  rw [profileWave_momentumReflection h hs]
  ring

/-- Real-wave parity at the origin. -/
theorem realProfileWave_momentumReflection (h : H1) (hs : ∀ᵐ y ∂orbitalMeasure 0, h y 1 = 0)
    (μ ν : Fin 4) :
    realProfileWave (momentumReflectionH1 h) μ ν 0 =
      momentumParitySign μ ν * realProfileWave h μ ν 0 := by
  unfold realProfileWave
  rw [lowerProfileWave_momentumReflection h hs]
  fin_cases μ <;> fin_cases ν <;> simp [momentumParitySign, momentumParitySignR]

/-- The longitudinally symmetrized wave has coefficient one plus the parity. -/
theorem realProfileWave_symmetricReflection (h : H1) (hh : RegularProfile h)
    (hs : ∀ᵐ y ∂orbitalMeasure 0, h y 1 = 0) (μ ν : Fin 4) :
    realProfileWave (h + momentumReflectionH1 h) μ ν 0 =
      (1 + momentumParitySign μ ν) * realProfileWave h μ ν 0 := by
  rw [realProfileWave_add h (momentumReflectionH1 h) hh (regularProfile_momentumReflection h hh),
    realProfileWave_momentumReflection h hs]
  ring

/-- Pressure contrast in the 1--2 screen directions, with the common trace removed. -/
theorem stress_screen_contrast (F : Fin 4 → Fin 4 → ℂ) :
    stress metricSignC F 2 2 - stress metricSignC F 1 1 =
      ∑ α : Fin 4, metricSignC α * (F 1 α ^ 2 - F 2 α ^ 2) := by
  norm_num [stress, Fin.sum_univ_four, metricSignC, pow_two] <;> simp <;> ring

/-- The symmetrized pressure contrast is an explicit signed sum of five squares. -/
theorem realProfileStress_symmetricReflection_contrast (h : H1) (hh : RegularProfile h)
    (hs : ∀ᵐ y ∂orbitalMeasure 0, h y 1 = 0) :
    (realProfileStress (h + momentumReflectionH1 h) 2 2 0 -
      realProfileStress (h + momentumReflectionH1 h) 1 1 0).re =
    (((2 * realProfileWave h 1 0 0) ^ 2 + (2 * realProfileWave h 2 1 0) ^ 2 -
      (2 * realProfileWave h 1 2 0) ^ 2 - (2 * realProfileWave h 1 3 0) ^ 2 +
      (2 * realProfileWave h 2 3 0) ^ 2).re) := by
  unfold realProfileStress
  rw [stress_screen_contrast]
  have hz (μ : Fin 4) : realProfileWave h μ μ 0 = 0 := by
    have ha := realProfileWave_antisymmetric h μ μ 0
    linear_combination (1 / 2 : ℂ) * ha
  norm_num [Fin.sum_univ_four, realProfileWave_symmetricReflection h hh hs,
    momentumParitySign, momentumParitySignR, metricSignC, hz, metricSignC_square, pow_two,
    Matrix.of_apply, Matrix.cons_val_zero', Matrix.cons_val_succ', Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.cons_val_succ]
  simp
  ring

/-- The tensor01 constructor has zero second helicity component. -/
theorem momentumSmear_singleFiber (f : SchwartzTensor) (b : Spacetime → ℂ)
    (hf : ∀ p, f p = b p • tensorUnit01) :
    ∀ᵐ y ∂orbitalMeasure 0, (momentumSmearCLM f) y 1 = 0 := by
  filter_upwards [(globalCoefficient_memLp f).coeFn_toLp] with y hy
  change (momentumSmear f) y 1 = 0
  rw [show (momentumSmear f) y = globalCoefficient f y from hy]
  simp [globalCoefficient, hf, tensorUnit01, Fin.sum_univ_four, cartesianStrength]

/-- The tensor01 wave has zero 23 component at the origin. -/
theorem momentumSmear_wave23_zero (f : SchwartzTensor) (b : Spacetime → ℂ)
    (hf : ∀ p, f p = b p • tensorUnit01) :
    realProfileWave (momentumSmearCLM f) 2 3 0 = 0 := by
  have hs := momentumSmear_singleFiber f b hf
  have hp : profileWave (momentumSmearCLM f) 2 3 0 = 0 := by
    rw [profileWave_zero_integral]
    apply integral_eq_zero_of_ae
    filter_upwards [hs] with y hy
    simp [profileDensity, hy, cartesianStrength]
  simp [realProfileWave, lowerProfileWave, hp]

/-- The real stress is conserved after longitudinal symmetrization. -/
theorem realProfileStress_symmetricReflection_conserved (h : H1) (hh : RegularProfile h)
    (ν : Fin 4) (x : Spacetime) :
    (∑ μ : Fin 4, metricSignC μ *
      deriv (fun t : ℝ => realProfileStress (h + momentumReflectionH1 h) μ ν
        (x + t • spacetimeBasis μ)) 0) = 0 :=
  realProfileStress_conserved (h + momentumReflectionH1 h)
    (regularProfile_add h (momentumReflectionH1 h) hh (regularProfile_momentumReflection h hh)) ν x

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.regularProfile_momentumReflection
#print axioms F1Fecho.MaxwellGlobal.regularProfile_add
#print axioms F1Fecho.MaxwellGlobal.profileDensity_momentumReflection
#print axioms F1Fecho.MaxwellGlobal.profileWave_zero_integral
#print axioms F1Fecho.MaxwellGlobal.profileWave_momentumReflection
#print axioms F1Fecho.MaxwellGlobal.lowerProfileWave_momentumReflection
#print axioms F1Fecho.MaxwellGlobal.realProfileWave_momentumReflection
#print axioms F1Fecho.MaxwellGlobal.realProfileWave_symmetricReflection
#print axioms F1Fecho.MaxwellGlobal.realProfileStress_symmetricReflection_contrast
#print axioms F1Fecho.MaxwellGlobal.momentumSmear_singleFiber
#print axioms F1Fecho.MaxwellGlobal.momentumSmear_wave23_zero
#print axioms F1Fecho.MaxwellGlobal.realProfileStress_symmetricReflection_conserved
