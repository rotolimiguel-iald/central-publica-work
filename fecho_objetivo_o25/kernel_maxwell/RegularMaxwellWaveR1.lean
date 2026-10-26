import RegularMaxwellWaveDensityR1

/-! Pointwise continuous Maxwell wave from the same Schwartz mass-shell profile.
The phase is exp(-i p.x), paired with the physical positive-Fourier convention.
This is the classical coherent wave kernel, not yet the local Wick stress. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016

def wavePhase (x : Spacetime) (y : MomentumCoordinates) : ℂ :=
  Complex.exp (Complex.I*((-(inner ℝ (metricFlip (shellEmbedding y)) x):ℝ):ℂ))

theorem wavePhase_norm (x : Spacetime) (y : MomentumCoordinates) : ‖wavePhase x y‖=1 :=
  Complex.norm_exp_I_mul_ofReal _

theorem wavePhase_continuous_left (y : MomentumCoordinates) : Continuous (fun x=>wavePhase x y) := by
  unfold wavePhase
  fun_prop

theorem wavePhase_continuous_right (x : Spacetime) : Continuous (wavePhase x) := by
  unfold wavePhase
  exact Complex.continuous_exp.comp (continuous_const.mul
    (Complex.continuous_ofReal.comp (((metricFlip.continuous.comp shellEmbedding_continuous).inner continuous_const).neg)))

def waveIntegrand (f : SchwartzTensor) (μ ν : Fin 4) (x : Spacetime) (y : MomentumCoordinates) : ℂ :=
  wavePhase x y*waveDensity f μ ν y

theorem waveIntegrand_norm (f : SchwartzTensor) (μ ν : Fin 4) (x : Spacetime) (y : MomentumCoordinates) :
    ‖waveIntegrand f μ ν x y‖=‖waveDensity f μ ν y‖ := by
  rw [waveIntegrand,norm_mul,wavePhase_norm,one_mul]

theorem waveIntegrand_measurable (f : SchwartzTensor) (μ ν : Fin 4) (x : Spacetime) :
    Measurable (waveIntegrand f μ ν x) :=
  (wavePhase_continuous_right x).measurable.mul (waveDensity_measurable f μ ν)

theorem waveIntegrand_integrable (f : SchwartzTensor) (μ ν : Fin 4) (x : Spacetime) :
    Integrable (waveIntegrand f μ ν x) (orbitalMeasure 0) := by
  exact (waveDensity_integrable f μ ν).norm.mono'
    (waveIntegrand_measurable f μ ν x).aestronglyMeasurable
    (Filter.Eventually.of_forall (fun y=>(waveIntegrand_norm f μ ν x y).le))

def regularWave (f : SchwartzTensor) (μ ν : Fin 4) (x : Spacetime) : ℂ :=
  ∫ y,waveIntegrand f μ ν x y ∂orbitalMeasure 0

theorem regularWave_continuous (f : SchwartzTensor) (μ ν : Fin 4) : Continuous (regularWave f μ ν) := by
  apply continuous_of_dominated (bound:=fun y=>‖waveDensity f μ ν y‖)
  · exact fun x=>(waveIntegrand_measurable f μ ν x).aestronglyMeasurable
  · exact fun x=>Filter.Eventually.of_forall (fun y=>(waveIntegrand_norm f μ ν x y).le)
  · exact (waveDensity_integrable f μ ν).norm
  · exact Filter.Eventually.of_forall (fun y=>(wavePhase_continuous_left y).mul continuous_const)

def physicalWave (f : SchwartzTensor) (μ ν : Fin 4) : Spacetime→ℂ :=
  regularWave (physicalFourierCLM f) μ ν

theorem physicalWave_continuous (f : SchwartzTensor) (μ ν : Fin 4) :
    Continuous (physicalWave f μ ν) := regularWave_continuous _ _ _

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.wavePhase_norm
#print axioms F1Fecho.MaxwellGlobal.waveIntegrand_integrable
#print axioms F1Fecho.MaxwellGlobal.regularWave_continuous
#print axioms F1Fecho.MaxwellGlobal.physicalWave_continuous
