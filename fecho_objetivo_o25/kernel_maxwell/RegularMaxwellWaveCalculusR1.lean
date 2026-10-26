import MaxwellWavePhaseDerivativeR1

/-! The actual on-shell wave is differentiable in every spacetime coordinate.
The first energy moment is the integrable derivative majorant, rather than a
formal interchange of operations. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open scoped Topology

theorem waveIntegrand_line_hasDerivAt (f : SchwartzTensor) (μ ν ρ : Fin 4)
    (x : Spacetime) (y : MomentumCoordinates) (t : ℝ) :
    HasDerivAt (fun u : ℝ=>waveIntegrand f μ ν (x+u • spacetimeBasis ρ) y)
      (waveDerivativeIntegrand f μ ν ρ (x+t • spacetimeBasis ρ) y) t := by
  simpa only [waveIntegrand,waveDerivativeIntegrand,mul_assoc] using
    (wavePhase_line_hasDerivAt x ρ y t).mul_const (waveDensity f μ ν y)

theorem regularWave_line_hasDerivAt (f : SchwartzTensor) (μ ν ρ : Fin 4)
    (x : Spacetime) (t : ℝ) :
    HasDerivAt (fun u : ℝ=>regularWave f μ ν (x+u • spacetimeBasis ρ))
      (∫ y,waveDerivativeIntegrand f μ ν ρ (x+t • spacetimeBasis ρ) y ∂orbitalMeasure 0) t := by
  have hi : Integrable (fun y=>shellEnergy y*‖waveDensity f μ ν y‖) (orbitalMeasure 0) := by
    simpa only [pow_one] using waveDensity_moment_integrable f μ ν 1
  exact (hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (s:=Set.univ) (bound:=fun y=>shellEnergy y*‖waveDensity f μ ν y‖)
    (Filter.univ_mem' (fun _=>Set.mem_univ _))
    (Filter.Eventually.of_forall (fun u=>(waveIntegrand_measurable f μ ν
      (x+u • spacetimeBasis ρ)).aestronglyMeasurable))
    (waveIntegrand_integrable f μ ν (x+t • spacetimeBasis ρ))
    (waveDerivativeIntegrand_integrable f μ ν ρ (x+t • spacetimeBasis ρ)).aestronglyMeasurable
    (Filter.Eventually.of_forall (fun y u _=>waveDerivativeIntegrand_bound f μ ν ρ
      (x+u • spacetimeBasis ρ) y)) hi
    (Filter.Eventually.of_forall (fun y u _=>waveIntegrand_line_hasDerivAt f μ ν ρ x y u))).2

theorem regularWave_partial (f : SchwartzTensor) (μ ν ρ : Fin 4) (x : Spacetime) :
    deriv (fun t : ℝ=>regularWave f μ ν (x+t • spacetimeBasis ρ)) 0=
      ∫ y,waveDerivativeIntegrand f μ ν ρ x y ∂orbitalMeasure 0 := by
  simpa only [zero_smul,add_zero] using (regularWave_line_hasDerivAt f μ ν ρ x 0).deriv

theorem physicalWave_line_hasDerivAt (f : SchwartzTensor) (μ ν ρ : Fin 4)
    (x : Spacetime) (t : ℝ) :
    HasDerivAt (fun u : ℝ=>physicalWave f μ ν (x+u • spacetimeBasis ρ))
      (∫ y,waveDerivativeIntegrand (physicalFourierCLM f) μ ν ρ
        (x+t • spacetimeBasis ρ) y ∂orbitalMeasure 0) t :=
  regularWave_line_hasDerivAt (physicalFourierCLM f) μ ν ρ x t

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.waveIntegrand_line_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.regularWave_line_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.regularWave_partial
#print axioms F1Fecho.MaxwellGlobal.physicalWave_line_hasDerivAt
