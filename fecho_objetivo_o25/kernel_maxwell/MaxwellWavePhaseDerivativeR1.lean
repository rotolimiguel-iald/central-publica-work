import RegularMaxwellWaveR2
import PhysicalFourierDerivativeR4
import Mathlib.Analysis.Calculus.ParametricIntegral

/-! Differentiation of the actual on-shell spacetime phase, paired with the
physical inverse-angular Fourier convention. No interchange of integral and
derivative is assumed in this layer. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016

def lowerShellMomentum (y : MomentumCoordinates) (ρ : Fin 4) : ℝ :=
  metricFlip (shellEmbedding y) ρ

theorem lowerShellMomentum_bound (y : MomentumCoordinates) (ρ : Fin 4) :
    |lowerShellMomentum y ρ|≤shellEnergy y := by
  fin_cases ρ
  · change |shellEnergy y|≤shellEnergy y
    exact (abs_of_nonneg (shellEnergy_nonneg y)).le
  · change |-y.2|≤shellEnergy y
    simpa only [abs_neg] using (abs_spatial_le_energy y).2.2
  · change |-y.1 0|≤shellEnergy y
    simpa only [abs_neg] using (abs_spatial_le_energy y).1
  · change |-y.1 1|≤shellEnergy y
    simpa only [abs_neg] using (abs_spatial_le_energy y).2.1

theorem lowerShellMomentum_continuous (ρ : Fin 4) : Continuous (fun y=>lowerShellMomentum y ρ) :=
  (PiLp.continuous_apply 2 _ ρ).comp (metricFlip.continuous.comp shellEmbedding_continuous)

theorem wavePhase_line_hasDerivAt (x : Spacetime) (ρ : Fin 4)
    (y : MomentumCoordinates) (t : ℝ) :
    HasDerivAt (fun u : ℝ=>wavePhase (x+u • spacetimeBasis ρ) y)
      ((-Complex.I*(lowerShellMomentum y ρ:ℂ))*wavePhase (x+t • spacetimeBasis ρ) y) t := by
  have hi : inner ℝ (metricFlip (shellEmbedding y)) (spacetimeBasis ρ)=lowerShellMomentum y ρ := by
    simp [spacetimeBasis,EuclideanSpace.inner_single_right,lowerShellMomentum]
  have hx := (hasDerivAt_const t x).add ((hasDerivAt_id t).smul_const (spacetimeBasis ρ))
  have hp := (hasDerivAt_const t (metricFlip (shellEmbedding y))).inner ℝ hx
  simp only [inner_zero_left,zero_add,hi,one_smul] at hp
  have he := (hp.neg.ofReal_comp.const_mul Complex.I).cexp
  convert he using 1 <;> simp only [wavePhase,Complex.ofReal_neg] <;> ring

def waveDerivativeIntegrand (f : SchwartzTensor) (μ ν ρ : Fin 4)
    (x : Spacetime) (y : MomentumCoordinates) : ℂ :=
  (-Complex.I*(lowerShellMomentum y ρ:ℂ))*waveIntegrand f μ ν x y

theorem waveDerivativeIntegrand_bound (f : SchwartzTensor) (μ ν ρ : Fin 4)
    (x : Spacetime) (y : MomentumCoordinates) :
    ‖waveDerivativeIntegrand f μ ν ρ x y‖≤shellEnergy y*‖waveDensity f μ ν y‖ := by
  rw [waveDerivativeIntegrand,norm_mul,norm_mul,norm_neg,Complex.norm_I,
    one_mul,Complex.norm_real,Real.norm_eq_abs,waveIntegrand_norm]
  exact mul_le_mul_of_nonneg_right (lowerShellMomentum_bound y ρ) (norm_nonneg _)

theorem waveDerivativeIntegrand_integrable (f : SchwartzTensor) (μ ν ρ : Fin 4) (x : Spacetime) :
    Integrable (waveDerivativeIntegrand f μ ν ρ x) (orbitalMeasure 0) := by
  have hi : Integrable (fun y=>shellEnergy y*‖waveDensity f μ ν y‖) (orbitalMeasure 0) := by
    simpa only [pow_one] using waveDensity_moment_integrable f μ ν 1
  apply hi.mono'
  · exact ((measurable_const.mul (Complex.continuous_ofReal.measurable.comp
      (lowerShellMomentum_continuous ρ).measurable)).mul
      (waveIntegrand_measurable f μ ν x)).aestronglyMeasurable
  · exact Filter.Eventually.of_forall (waveDerivativeIntegrand_bound f μ ν ρ x)

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.lowerShellMomentum_bound
#print axioms F1Fecho.MaxwellGlobal.wavePhase_line_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.waveDerivativeIntegrand_bound
#print axioms F1Fecho.MaxwellGlobal.waveDerivativeIntegrand_integrable
