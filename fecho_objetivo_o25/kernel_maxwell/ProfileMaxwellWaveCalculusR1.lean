import ProfileMaxwellWaveR4
import RegularMaxwellWaveEquationR1

/-! Differentiable source-free waves for every actual regular H1 profile.
The second L1 energy moment pays the derivative estimate. There is no
new test-profile or equation assumption in the consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016

theorem profileDensity_moment_integrable (h : H1) (hh : RegularProfile h)
    (μ ν : Fin 4) (m : ℕ) :
    Integrable (fun y=>shellEnergy y^m*‖profileDensity h μ ν y‖) (orbitalMeasure 0) := by
  apply ((hh (m+1)).const_mul 2).mono'
  · exact (shellEnergy_continuous.pow m).measurable.aestronglyMeasurable.mul
      (profileDensity_measurable h μ ν).norm
  · exact Filter.Eventually.of_forall (fun y=>by
      rw [Real.norm_of_nonneg (mul_nonneg (pow_nonneg (shellEnergy_nonneg y) m) (norm_nonneg _))]
      have hb:=mul_le_mul_of_nonneg_left (profileDensity_bound h μ ν y)
        (pow_nonneg (shellEnergy_nonneg y) m)
      simpa only [pow_succ,mul_assoc,mul_left_comm,mul_comm] using hb)

def profileDerivativeIntegrand (h : H1) (μ ν ρ : Fin 4)
    (x : Spacetime) (y : MomentumCoordinates) : ℂ :=
  (-Complex.I*(lowerShellMomentum y ρ:ℂ))*(wavePhase x y*profileDensity h μ ν y)

theorem profileDerivativeIntegrand_bound (h : H1) (μ ν ρ : Fin 4)
    (x : Spacetime) (y : MomentumCoordinates) :
    ‖profileDerivativeIntegrand h μ ν ρ x y‖ ≤ shellEnergy y*‖profileDensity h μ ν y‖ := by
  rw [profileDerivativeIntegrand,norm_mul,norm_mul,norm_neg,Complex.norm_I,
    one_mul,Complex.norm_real,Real.norm_eq_abs,norm_mul,wavePhase_norm,one_mul]
  exact mul_le_mul_of_nonneg_right (lowerShellMomentum_bound y ρ) (norm_nonneg _)

theorem profilePhaseDensity_integrable (h : H1) (hh : RegularProfile h)
    (μ ν : Fin 4) (x : Spacetime) :
    Integrable (fun y=>wavePhase x y*profileDensity h μ ν y) (orbitalMeasure 0) := by
  apply (profileDensity_integrable h hh μ ν).norm.mono'
  · exact (wavePhase_continuous_right x).measurable.aestronglyMeasurable.mul
      (profileDensity_measurable h μ ν)
  · exact Filter.Eventually.of_forall (fun y=>by rw [norm_mul,wavePhase_norm,one_mul])

theorem profileDerivativeIntegrand_integrable (h : H1) (hh : RegularProfile h)
    (μ ν ρ : Fin 4) (x : Spacetime) :
    Integrable (profileDerivativeIntegrand h μ ν ρ x) (orbitalMeasure 0) := by
  have hi : Integrable (fun y=>shellEnergy y*‖profileDensity h μ ν y‖) (orbitalMeasure 0) := by
    simpa only [pow_one] using profileDensity_moment_integrable h hh μ ν 1
  apply hi.mono'
  · exact ((measurable_const.mul (Complex.continuous_ofReal.measurable.comp
      (lowerShellMomentum_continuous ρ).measurable)).aestronglyMeasurable.mul
      (profilePhaseDensity_integrable h hh μ ν x).aestronglyMeasurable)
  · exact Filter.Eventually.of_forall (profileDerivativeIntegrand_bound h μ ν ρ x)

theorem profileWave_line_hasDerivAt (h : H1) (hh : RegularProfile h)
    (μ ν ρ : Fin 4) (x : Spacetime) (t : ℝ) :
    HasDerivAt (fun u : ℝ=>profileWave h μ ν (x+u • spacetimeBasis ρ))
      (∫ y,profileDerivativeIntegrand h μ ν ρ (x+t • spacetimeBasis ρ) y ∂orbitalMeasure 0) t := by
  have hi : Integrable (fun y=>shellEnergy y*‖profileDensity h μ ν y‖) (orbitalMeasure 0) := by
    simpa only [pow_one] using profileDensity_moment_integrable h hh μ ν 1
  apply (hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (s:=Set.univ) (bound:=fun y=>shellEnergy y*‖profileDensity h μ ν y‖)
    Filter.univ_mem
    (Filter.Eventually.of_forall (fun u=>(profilePhaseDensity_integrable h hh μ ν
      (x+u • spacetimeBasis ρ)).aestronglyMeasurable))
    (profilePhaseDensity_integrable h hh μ ν (x+t • spacetimeBasis ρ))
    (profileDerivativeIntegrand_integrable h hh μ ν ρ (x+t • spacetimeBasis ρ)).aestronglyMeasurable
    (Filter.Eventually.of_forall (fun y u _=>profileDerivativeIntegrand_bound h μ ν ρ
      (x+u • spacetimeBasis ρ) y)) hi ?_).2
  exact Filter.Eventually.of_forall (fun y u _=>by
    simpa only [profileDerivativeIntegrand,mul_assoc] using
      (wavePhase_line_hasDerivAt x ρ y u).mul_const (profileDensity h μ ν y))

theorem profileWave_partial (h : H1) (hh : RegularProfile h) (μ ν ρ : Fin 4) (x : Spacetime) :
    deriv (fun t : ℝ=>profileWave h μ ν (x+t • spacetimeBasis ρ)) 0=
      ∫ y,profileDerivativeIntegrand h μ ν ρ x y ∂orbitalMeasure 0 := by
  simpa only [zero_smul,add_zero] using (profileWave_line_hasDerivAt h hh μ ν ρ x 0).deriv

theorem profileDensity_divergence_regular (h : H1) (ν : Fin 4)
    (y : MomentumCoordinates) (hy : y.1≠0) :
    ∑ μ : Fin 4,(lowerShellMomentum y μ:ℂ)*profileDensity h μ ν y=0 := by
  calc
    _ = ∑ μ : Fin 4,∑ j : Fin 2,h y j*
        ((lowerShellMomentum y μ:ℂ)*(cartesianStrength y j μ ν:ℂ)) := by
      simp only [profileDensity,Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro μ _
      apply Finset.sum_congr rfl
      intro j _
      ring
    _ = ∑ j : Fin 2,h y j*
        (∑ μ : Fin 4,(lowerShellMomentum y μ:ℂ)*(cartesianStrength y j μ ν:ℂ)) := by
      rw [Finset.sum_comm]
      simp only [Finset.mul_sum]
    _ = 0 := by
      simp only [lowerShellMomentum,cartesian_divergence_regular y hy,mul_zero,Finset.sum_const_zero]

theorem profileWave_divergence_zero (h : H1) (hh : RegularProfile h) (ν : Fin 4) (x : Spacetime) :
    (∑ μ : Fin 4,deriv (fun t : ℝ=>profileWave h μ ν (x+t • spacetimeBasis μ)) 0)=0 := by
  simp only [profileWave_partial h hh]
  rw [← integral_finsetSum Finset.univ (fun μ _=>profileDerivativeIntegrand_integrable h hh μ ν μ x)]
  calc
    _ = ∫ _ : MomentumCoordinates,(0:ℂ) ∂orbitalMeasure 0 := by
      apply integral_congr_ae
      filter_upwards [cartesian_regular_ae] with y hy
      calc
        _ = (-Complex.I*wavePhase x y)*
            (∑ μ : Fin 4,(lowerShellMomentum y μ:ℂ)*profileDensity h μ ν y) := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro μ _
          simp only [profileDerivativeIntegrand]
          ring
        _ = 0 := by rw [profileDensity_divergence_regular h ν y hy,mul_zero]
    _ = 0 := integral_zero _ _

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.profileDensity_moment_integrable
#print axioms F1Fecho.MaxwellGlobal.profileWave_line_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.profileWave_partial
#print axioms F1Fecho.MaxwellGlobal.profileWave_divergence_zero
