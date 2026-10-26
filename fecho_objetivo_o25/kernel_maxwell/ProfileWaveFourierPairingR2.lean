import ProfileMaxwellWaveR5
import PhysicalFourierDerivativeR4
import Mathlib.MeasureTheory.Integral.Prod

/-! Actual Fourier pairing of the regular on-shell wave with a scalar Schwartz
 test. The positive angular inverse transform and the negative wave phase are
 explicitly paired. Integrability of the joint kernel is proved, not assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory SchwartzMap Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open scoped FourierTransform

 theorem wavePhase_continuous_joint :
    Continuous (fun q : Spacetime×MomentumCoordinates=>wavePhase q.1 q.2) := by
  unfold wavePhase
  exact Complex.continuous_exp.comp (continuous_const.mul (Complex.continuous_ofReal.comp
    (((metricFlip.continuous.comp (shellEmbedding_continuous.comp continuous_snd)).inner continuous_fst).neg)))

 theorem scalarPhysicalFourier_integral (f : 𝓢(Spacetime,ℂ)) (y : MomentumCoordinates) :
    scalarPhysicalFourier f (shellEmbedding y)=
      ∫x,(starRingEnd ℂ) (wavePhase x y)*f x := by
  change (𝓕⁻ f) ((2*Real.pi)⁻¹ • metricFlip (shellEmbedding y))=_
  rw [SchwartzMap.fourierInv_coe,Real.fourierInv_eq']
  apply integral_congr_ae
  apply ae_of_all
  intro x
  simp only [smul_eq_mul,wavePhase,← Complex.exp_conj,map_mul,Complex.conj_I,
    Complex.conj_ofReal,real_inner_smul_right]
  congr 2
  rw [real_inner_comm x]
  push_cast
  field_simp [Real.pi_ne_zero]
  <;> ring

 theorem scalarPhysicalFourier_conj_integral (f : 𝓢(Spacetime,ℂ)) (y : MomentumCoordinates) :
    (starRingEnd ℂ) (scalarPhysicalFourier f (shellEmbedding y))=
      ∫x,(starRingEnd ℂ) (f x)*wavePhase x y := by
  rw [scalarPhysicalFourier_integral,← integral_conj]
  apply integral_congr_ae
  apply ae_of_all
  intro x
  simp only [map_mul,starRingEnd_self_apply,mul_comm]

 theorem profileWave_pairing_integrable (f : 𝓢(Spacetime,ℂ)) (h : H1)
    (hh : RegularProfile h) (μ ν : Fin 4) :
    Integrable (fun q : Spacetime×MomentumCoordinates=>
      (starRingEnd ℂ) (f q.1)*wavePhase q.1 q.2*profileDensity h μ ν q.2)
      (volume.prod (orbitalMeasure 0)) := by
  have hm : AEStronglyMeasurable (fun q : Spacetime×MomentumCoordinates=>
      (starRingEnd ℂ) (f q.1)*wavePhase q.1 q.2*profileDensity h μ ν q.2)
      (volume.prod (orbitalMeasure 0)) :=
    ((Complex.continuous_conj.comp (f.continuous.comp continuous_fst)).measurable.aestronglyMeasurable.mul
      wavePhase_continuous_joint.measurable.aestronglyMeasurable).mul
        (profileDensity_measurable h μ ν).comp_snd
  have hi : Integrable (fun q : Spacetime×MomentumCoordinates=>
      ‖f q.1‖*‖profileDensity h μ ν q.2‖) (volume.prod (orbitalMeasure 0)) :=
    f.integrable.norm.mul_prod (profileDensity_integrable h hh μ ν).norm
  exact hi.mono' hm (ae_of_all _ (fun q=>by
    simp only [norm_mul,Complex.norm_conj,wavePhase_norm,mul_one]
    exact le_rfl))

 theorem profileWave_fourier_pairing (f : 𝓢(Spacetime,ℂ)) (h : H1)
    (hh : RegularProfile h) (μ ν : Fin 4) :
    (∫x,(starRingEnd ℂ) (f x)*profileWave h μ ν x)=
      ∫y,(starRingEnd ℂ) (scalarPhysicalFourier f (shellEmbedding y))*
        profileDensity h μ ν y ∂orbitalMeasure 0 := by
  simp only [profileWave,← integral_const_mul]
  have hs:=integral_integral_swap
    (f:=fun (x : Spacetime) (y : MomentumCoordinates)=>
      (starRingEnd ℂ) (f x)*wavePhase x y*profileDensity h μ ν y)
    (profileWave_pairing_integrable f h hh μ ν)
  have he : (fun x : Spacetime=>∫ y,
      (starRingEnd ℂ) (f x)*(wavePhase x y*profileDensity h μ ν y) ∂orbitalMeasure 0)=
      (fun x : Spacetime=>∫ y,
      (starRingEnd ℂ) (f x)*wavePhase x y*profileDensity h μ ν y ∂orbitalMeasure 0) := by
    funext x
    congr 1
    funext y
    ring
  rw [he,hs]
  apply integral_congr_ae
  apply ae_of_all
  intro y
  rw [integral_mul_const,scalarPhysicalFourier_conj_integral]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.scalarPhysicalFourier_integral
#print axioms F1Fecho.MaxwellGlobal.scalarPhysicalFourier_conj_integral
#print axioms F1Fecho.MaxwellGlobal.profileWave_pairing_integrable
#print axioms F1Fecho.MaxwellGlobal.profileWave_fourier_pairing
