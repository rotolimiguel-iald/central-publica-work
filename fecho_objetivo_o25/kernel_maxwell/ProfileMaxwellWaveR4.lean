import RegularMaxwellProfilesR3
import RegularMaxwellWaveR2

/-! The pointwise wave on the actual regular H1 domain, rather than on test
labels. Translation covariance is proved for the existing U1. There is no
point evaluation of an L2 profile: only its integrable on-shell wave integral. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open ChatgptAudit.WignerOrbit016

def profileDensity (h : H1) (μ ν : Fin 4) (y : MomentumCoordinates) : ℂ :=
  ∑ j : Fin 2,(cartesianStrength y j μ ν:ℂ)*h y j

theorem profileDensity_measurable (h : H1) (μ ν : Fin 4) :
    AEStronglyMeasurable (profileDensity h μ ν) (orbitalMeasure 0) := by
  have hj (j : Fin 2) : AEStronglyMeasurable
      (fun y=>(cartesianStrength y j μ ν:ℂ)*h y j) (orbitalMeasure 0) :=
    (Complex.continuous_ofReal.measurable.comp (cartesianStrength_measurable j μ ν)).aestronglyMeasurable.mul
      ((PiLp.continuous_apply 2 _ j).comp_aestronglyMeasurable (Lp.aestronglyMeasurable h))
  simpa only [profileDensity,Fin.sum_univ_two,Pi.add_apply] using (hj 0).add (hj 1)

theorem profileDensity_bound (h : H1) (μ ν : Fin 4) (y : MomentumCoordinates) :
    ‖profileDensity h μ ν y‖≤2*shellEnergy y*‖h y‖ := by
  have hj (j : Fin 2) : ‖(cartesianStrength y j μ ν:ℂ)*h y j‖≤ shellEnergy y*‖h y‖ := by
    rw [norm_mul,Complex.norm_real,Real.norm_eq_abs]
    exact mul_le_mul (cartesianStrength_bound y j μ ν) (PiLp.norm_apply_le (h y) j)
      (norm_nonneg _) (shellEnergy_nonneg y)
  have hs:=norm_add_le ((cartesianStrength y 0 μ ν:ℂ)*h y 0)
    ((cartesianStrength y 1 μ ν:ℂ)*h y 1)
  change ‖∑ j : Fin 2,(cartesianStrength y j μ ν:ℂ)*h y j‖≤_
  rw [Fin.sum_univ_two]
  nlinarith only [hs,hj 0,hj 1]

theorem profileDensity_integrable (h : H1) (hh : RegularProfile h) (μ ν : Fin 4) :
    Integrable (profileDensity h μ ν) (orbitalMeasure 0) := by
  have hi : Integrable (fun y=>shellEnergy y*‖h y‖) (orbitalMeasure 0) := by
    simpa only [pow_one] using hh 1
  exact (hi.const_mul 2).mono' (profileDensity_measurable h μ ν)
    (Filter.Eventually.of_forall (fun y=>by
      simpa only [mul_assoc] using profileDensity_bound h μ ν y))

def profileWave (h : H1) (μ ν : Fin 4) (x : Spacetime) : ℂ :=
  ∫ y,wavePhase x y*profileDensity h μ ν y ∂orbitalMeasure 0

theorem profileWave_continuous (h : H1) (hh : RegularProfile h) (μ ν : Fin 4) :
    Continuous (profileWave h μ ν) := by
  apply continuous_of_dominated (bound:=fun y=>‖profileDensity h μ ν y‖)
  · intro x
    exact (wavePhase_continuous_right x).measurable.aestronglyMeasurable.mul
      (profileDensity_measurable h μ ν)
  · intro x
    exact Filter.Eventually.of_forall (fun y=>by rw [norm_mul,wavePhase_norm,one_mul])
  · exact (profileDensity_integrable h hh μ ν).norm
  · exact Filter.Eventually.of_forall (fun y=>(wavePhase_continuous_left y).mul continuous_const)

theorem profileWave_momentumSmear (f : SchwartzTensor) (μ ν : Fin 4) (x : Spacetime) :
    profileWave (momentumSmearCLM f) μ ν x=regularWave f μ ν x := by
  apply integral_congr_ae
  filter_upwards [(globalCoefficient_memLp f).coeFn_toLp] with y hy
  change wavePhase x y*profileDensity (momentumSmear f) μ ν y=
    wavePhase x y*waveDensity f μ ν y
  simp only [profileDensity,waveDensity,momentumSmear,hy]

theorem wavePhase_translation (a : Fin 4→ℝ) (x : Spacetime) (y : MomentumCoordinates) :
    wavePhase x y*orbitalPhase 0 a y=wavePhase (x-WithLp.toLp 2 a) y := by
  unfold wavePhase orbitalPhase phase
  rw [← Complex.exp_add]
  congr 1
  rw [inner_sub_right]
  have hp : inner ℝ (metricFlip (shellEmbedding y)) (WithLp.toLp 2 a)=
      orbitPairing a (shellMomentum 0 y) := by
    rw [metricFlip_inner]
    simp only [shellEmbedding,PiLp.toLp_apply,orbitPairing]
    ring
  rw [hp]
  push_cast
  ring

theorem profileDensity_U1 (a : Fin 4→ℝ) (h : H1) (μ ν : Fin 4) :
    profileDensity (U1 a h) μ ν=ᵐ[orbitalMeasure 0]
      fun y=>orbitalPhase 0 a y*profileDensity h μ ν y := by
  filter_upwards [orbitalTranslation_ae 0 a h] with y hy
  change (∑ j : Fin 2,(cartesianStrength y j μ ν:ℂ)*orbitalTranslation 0 a h y j)=_
  rw [hy]
  simp only [profileDensity,PiLp.smul_apply,smul_eq_mul,Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem profileWave_U1 (a : Fin 4→ℝ) (h : H1) (μ ν : Fin 4) (x : Spacetime) :
    profileWave (U1 a h) μ ν x=profileWave h μ ν (x-WithLp.toLp 2 a) := by
  apply integral_congr_ae
  filter_upwards [profileDensity_U1 a h μ ν] with y hy
  rw [hy,← mul_assoc,wavePhase_translation]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.profileDensity_integrable
#print axioms F1Fecho.MaxwellGlobal.profileWave_continuous
#print axioms F1Fecho.MaxwellGlobal.profileWave_momentumSmear
#print axioms F1Fecho.MaxwellGlobal.wavePhase_translation
#print axioms F1Fecho.MaxwellGlobal.profileWave_U1
