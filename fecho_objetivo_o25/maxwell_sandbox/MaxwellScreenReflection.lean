import MaxwellRadiationClosure

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! Transverse-screen reflection for free-streaming Maxwell radiation. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open F1Fecho.MaxwellStress ChatgptAudit.WignerRapidityMeasure016 F1Fecho.NullFrequency
open F1Fecho.WeightedPlancherel F1Fecho.OrbitalScreen

/-- Reverse both transverse momentum coordinates, leaving the longitudinal one fixed. -/
def screenReflection (y : MomentumCoordinates) : MomentumCoordinates := (-y.1, y.2)

theorem screenReflection_measurable : Measurable screenReflection := by
  unfold screenReflection
  fun_prop

theorem screenReflection_involutive : Function.Involutive screenReflection := by
  intro y
  cases y
  simp [screenReflection]

def screenReflectionEquiv : MomentumCoordinates ≃ᵐ MomentumCoordinates :=
  MeasurableEquiv.ofInvolutive screenReflection screenReflection_involutive
    screenReflection_measurable

theorem screenReflection_weight (y : MomentumCoordinates) :
    orbitalWeight 0 (screenReflection y) = orbitalWeight 0 y := by
  simp [screenReflection, orbitalWeight, energy, transverseMass, sq]

theorem screenReflection_measurePreserving :
    MeasurePreserving screenReflectionEquiv (orbitalMeasure 0) (orbitalMeasure 0) := by
  have hm : MeasurePreserving screenReflection momentumMeasure momentumMeasure := by
    change MeasurePreserving (Prod.map (fun x : Transverse => -x) id)
      ((volume : Measure Transverse).prod (volume : Measure ℝ))
      ((volume : Measure Transverse).prod (volume : Measure ℝ))
    exact (Measure.measurePreserving_neg _).prod (MeasurePreserving.id _)
  refine ⟨screenReflection_measurable, ?_⟩
  ext s hs
  rw [Measure.map_apply screenReflectionEquiv.measurable hs]
  simp only [orbitalMeasure, withDensity_apply _ (screenReflectionEquiv.measurable hs),
    withDensity_apply _ hs]
  calc
    (∫⁻ y in screenReflectionEquiv ⁻¹' s, orbitalWeight 0 y ∂momentumMeasure) =
        ∫⁻ y in screenReflection ⁻¹' s,
          orbitalWeight 0 (screenReflection y) ∂momentumMeasure := by
      apply setLIntegral_congr_fun_ae (screenReflection_measurable hs)
      filter_upwards [] with y
      intro _
      exact (screenReflection_weight y).symm
    _ = ∫⁻ y in s, orbitalWeight 0 y ∂momentumMeasure :=
      hm.setLIntegral_comp_preimage hs (orbitalWeight_measurable 0)

theorem integral_screenReflection (f : MomentumCoordinates → ℂ) :
    (∫ y, f (screenReflection y) ∂orbitalMeasure 0) = ∫ y, f y ∂orbitalMeasure 0 :=
  screenReflection_measurePreserving.integral_comp' f

/-- Pullback by transverse-screen reflection on the one-particle space. -/
def screenReflectionH1 : H1 →ₗᵢ[ℂ] H1 :=
  Lp.compMeasurePreservingₗᵢ ℂ screenReflectionEquiv screenReflection_measurePreserving

theorem regularProfile_screenReflection (h : H1) (hh : RegularProfile h) :
    RegularProfile (screenReflectionH1 h) := by
  intro m
  have hi := screenReflection_measurePreserving.integrable_comp_of_integrable (hh m)
  apply hi.congr
  filter_upwards [Lp.coeFn_compMeasurePreserving h screenReflection_measurePreserving] with y hy
  change shellEnergy (screenReflection y) ^ m * ‖h (screenReflection y)‖ =
    shellEnergy y ^ m * ‖(Lp.compMeasurePreserving screenReflectionEquiv
      screenReflection_measurePreserving h) y‖
  simp only [Function.comp_apply] at hy
  have he : shellEnergy (screenReflection y) = shellEnergy y := by
    simp [shellEnergy, energy, transverseMass, screenReflection, sq]
  rw [hy, he]
  simp only [screenReflectionEquiv, MeasurableEquiv.ofInvolutive_apply]

/-- Real parity of each Maxwell component under transverse-screen reflection. -/
def screenParitySignR (μ ν : Fin 4) : ℝ :=
  ![![1, 1, -1, -1], ![1, 1, -1, -1], ![-1, -1, 1, 1], ![-1, -1, 1, 1]] μ ν

def screenParitySign (μ ν : Fin 4) : ℂ := (screenParitySignR μ ν : ℂ)

theorem screenParitySignR_sq (μ ν : Fin 4) :
    screenParitySignR μ ν * screenParitySignR μ ν = 1 := by
  fin_cases μ <;> fin_cases ν <;> norm_num [screenParitySignR]

theorem cartesianStrength_screenReflection (y : MomentumCoordinates) (j : Fin 2) (μ ν : Fin 4) :
    cartesianStrength (screenReflection y) j μ ν =
      screenParitySignR μ ν * cartesianStrength y j μ ν := by
  fin_cases j <;> fin_cases μ <;> fin_cases ν <;>
    norm_num [screenParitySignR, cartesianStrength, transverseRatio, transverseMass,
      shellEnergy, energy, screenReflection, Matrix.of_apply, sq,
      Matrix.cons_val_zero', Matrix.cons_val_succ'] <;> ring

theorem profileDensity_screenReflection (h : H1)
    (hs : ∀ᵐ y ∂orbitalMeasure 0, h y 1 = 0) (μ ν : Fin 4) :
    (fun y => profileDensity (screenReflectionH1 h) μ ν y) =ᵐ[orbitalMeasure 0]
      (fun y => screenParitySign μ ν * profileDensity h μ ν (screenReflection y)) := by
  filter_upwards [Lp.coeFn_compMeasurePreserving h screenReflection_measurePreserving,
    screenReflection_measurePreserving.quasiMeasurePreserving.ae hs] with z hz hs1
  simp only [Function.comp_apply] at hz
  simp only [screenReflectionEquiv, MeasurableEquiv.ofInvolutive_apply] at hs1
  change profileDensity (Lp.compMeasurePreserving screenReflectionEquiv
    screenReflection_measurePreserving h) μ ν z = _
  unfold profileDensity
  rw [hz]
  simp only [screenReflectionEquiv, MeasurableEquiv.ofInvolutive_apply,
    Fin.sum_univ_two, hs1, mul_zero, add_zero, cartesianStrength_screenReflection,
    screenParitySign, Finset.mul_sum, ← mul_assoc, ← Complex.ofReal_mul,
    screenParitySignR_sq, Complex.ofReal_one, one_mul]

theorem profileWave_screenReflection (h : H1)
    (hs : ∀ᵐ y ∂orbitalMeasure 0, h y 1 = 0) (μ ν : Fin 4) :
    profileWave (screenReflectionH1 h) μ ν 0 = screenParitySign μ ν * profileWave h μ ν 0 := by
  rw [profileWave_zero_integral, profileWave_zero_integral,
    ← integral_screenReflection (profileDensity h μ ν), ← integral_const_mul]
  apply integral_congr_ae
  filter_upwards [profileDensity_screenReflection h hs μ ν] with y hy
  exact hy

theorem lowerProfileWave_screenReflection (h : H1)
    (hs : ∀ᵐ y ∂orbitalMeasure 0, h y 1 = 0) (μ ν : Fin 4) :
    lowerProfileWave (screenReflectionH1 h) μ ν 0 =
      screenParitySign μ ν * lowerProfileWave h μ ν 0 := by
  unfold lowerProfileWave
  rw [profileWave_screenReflection h hs]
  ring

theorem realProfileWave_screenReflection (h : H1)
    (hs : ∀ᵐ y ∂orbitalMeasure 0, h y 1 = 0) (μ ν : Fin 4) :
    realProfileWave (screenReflectionH1 h) μ ν 0 =
      screenParitySign μ ν * realProfileWave h μ ν 0 := by
  unfold realProfileWave
  rw [lowerProfileWave_screenReflection h hs]
  fin_cases μ <;> fin_cases ν <;> simp [screenParitySign, screenParitySignR]

theorem realProfileWave_screenSymmetric (h : H1) (hh : RegularProfile h)
    (hs : ∀ᵐ y ∂orbitalMeasure 0, h y 1 = 0) (μ ν : Fin 4) :
    realProfileWave (h + screenReflectionH1 h) μ ν 0 =
      (1 + screenParitySign μ ν) * realProfileWave h μ ν 0 := by
  rw [realProfileWave_add h (screenReflectionH1 h) hh (regularProfile_screenReflection h hh),
    realProfileWave_screenReflection h hs]
  ring

/-- The single-fiber property survives transverse-screen symmetrization. -/
theorem screenSymmetric_singleFiber (h : H1)
    (hs : ∀ᵐ y ∂orbitalMeasure 0, h y 1 = 0) :
    ∀ᵐ y ∂orbitalMeasure 0, (h + screenReflectionH1 h) y 1 = 0 := by
  filter_upwards [hs, Lp.coeFn_compMeasurePreserving h screenReflection_measurePreserving,
    screenReflection_measurePreserving.quasiMeasurePreserving.ae hs,
    Lp.coeFn_add h (screenReflectionH1 h)] with y hy hr hrs ha
  simp only [Function.comp_apply] at hr
  simp only [screenReflectionEquiv, MeasurableEquiv.ofInvolutive_apply] at hrs
  rw [show (h + screenReflectionH1 h) y = h y + screenReflectionH1 h y from ha]
  rw [show screenReflectionH1 h y = h (screenReflection y) from hr]
  change h y 1 + h (screenReflection y) 1 = 0
  rw [hy, hrs, add_zero]

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.screenReflection_measurePreserving
#print axioms F1Fecho.MaxwellGlobal.regularProfile_screenReflection
#print axioms F1Fecho.MaxwellGlobal.cartesianStrength_screenReflection
#print axioms F1Fecho.MaxwellGlobal.profileWave_screenReflection
#print axioms F1Fecho.MaxwellGlobal.realProfileWave_screenSymmetric
#print axioms F1Fecho.MaxwellGlobal.screenSymmetric_singleFiber
