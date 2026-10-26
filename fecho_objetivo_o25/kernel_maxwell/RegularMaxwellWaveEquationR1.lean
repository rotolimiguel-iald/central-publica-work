import RegularMaxwellWaveCalculusR2

/-! The source-free divergence equation for the actual continuous differentiable
spacetime wave. The previously built on-shell symbol is integrated on its
proved full-measure chart, using the genuine derivative majorant. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016

theorem cartesian_regular_ae : ∀ᵐ y ∂orbitalMeasure 0,y.1≠(0:Transverse) := by
  rw [ae_iff]
  have hs : {y : MomentumCoordinates | ¬ y.1≠(0:Transverse)}=
      ({0}:Set Transverse)×ˢ(Set.univ:Set ℝ) := by ext y; simp
  rw [hs]
  exact exceptional_axis_orbital_null 0

theorem waveDensity_divergence_regular (f : SchwartzTensor) (ν : Fin 4)
    (y : MomentumCoordinates) (hy : y.1≠0) :
    ∑ μ : Fin 4,(lowerShellMomentum y μ:ℂ)*waveDensity f μ ν y=0 := by
  calc
    _ = ∑ μ : Fin 4,∑ j : Fin 2,globalCoefficient f y j*
        ((lowerShellMomentum y μ:ℂ)*(cartesianStrength y j μ ν:ℂ)) := by
      simp only [waveDensity,Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro μ _
      apply Finset.sum_congr rfl
      intro j _
      ring
    _ = ∑ j : Fin 2,globalCoefficient f y j*
        (∑ μ : Fin 4,(lowerShellMomentum y μ:ℂ)*(cartesianStrength y j μ ν:ℂ)) := by
      rw [Finset.sum_comm]
      simp only [Finset.mul_sum]
    _ = 0 := by
      simp only [lowerShellMomentum,cartesian_divergence_regular y hy,mul_zero,Finset.sum_const_zero]

theorem waveDerivativeIntegrand_divergence_regular (f : SchwartzTensor) (ν : Fin 4)
    (x : Spacetime) (y : MomentumCoordinates) (hy : y.1≠0) :
    ∑ μ : Fin 4,waveDerivativeIntegrand f μ ν μ x y=0 := by
  calc
    _ = (-Complex.I*wavePhase x y)*
        (∑ μ : Fin 4,(lowerShellMomentum y μ:ℂ)*waveDensity f μ ν y) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro μ _
      simp only [waveDerivativeIntegrand,waveIntegrand]
      ring
    _ = 0 := by rw [waveDensity_divergence_regular f ν y hy,mul_zero]

theorem regularWave_divergence_zero (f : SchwartzTensor) (ν : Fin 4) (x : Spacetime) :
    (∑ μ : Fin 4,deriv (fun t : ℝ=>regularWave f μ ν (x+t • spacetimeBasis μ)) 0)=0 := by
  simp only [regularWave_partial]
  rw [← integral_finsetSum Finset.univ (fun μ _=>waveDerivativeIntegrand_integrable f μ ν μ x)]
  calc
    _ = ∫ _ : MomentumCoordinates,(0:ℂ) ∂orbitalMeasure 0 := by
      apply integral_congr_ae
      filter_upwards [cartesian_regular_ae] with y hy
      exact waveDerivativeIntegrand_divergence_regular f ν x y hy
    _ = 0 := integral_zero _ _

theorem physicalWave_divergence_zero (f : SchwartzTensor) (ν : Fin 4) (x : Spacetime) :
    (∑ μ : Fin 4,deriv (fun t : ℝ=>physicalWave f μ ν (x+t • spacetimeBasis μ)) 0)=0 :=
  regularWave_divergence_zero (physicalFourierCLM f) ν x

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.waveDensity_divergence_regular
#print axioms F1Fecho.MaxwellGlobal.waveDerivativeIntegrand_divergence_regular
#print axioms F1Fecho.MaxwellGlobal.regularWave_divergence_zero
#print axioms F1Fecho.MaxwellGlobal.physicalWave_divergence_zero
