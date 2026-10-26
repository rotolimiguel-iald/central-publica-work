import SchwartzMaxwellLinearR3
import CartesianMaxwellChartR3
import MaxwellDivergenceSmearingR2

/-! The source-free on-shell identity is consumed on the entire Schwartz
momentum test domain. The exceptional chart axis is removed by its proved
orbital nullity. This is the Fourier-symbol equation; the differential
spacetime identity requires the explicit Fourier-derivative consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Matrix Filter SchwartzMap
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.MaxwellOnShell

theorem cartesian_divergence_regular (y : MomentumCoordinates) (hy : y.1≠0)
    (j : Fin 2) (ν : Fin 4) :
    ∑ μ,(metricFlip (shellEmbedding y) μ:ℂ)*(cartesianStrength y j μ ν:ℂ)=0 := by
  have hc:=chart_inverse_of_positive 0 y (transverseMass_pos_of_ne_zero 0 y.1 hy)
  have hp : momentum (inverseRapidityChart 0 y)=realLift (shellMomentum 0 y) := by
    funext μ
    simp only [momentum,realLift,hc]
  have h:=F1Fecho.MaxwellSmearing.real_screen_source_free (inverseRapidityChart 0 y) hy j ν
  simp only [F1Fecho.MaxwellSmearing.lowerMomentum,hp] at h
  simp_rw [cartesianStrength_inverse_chart y hy j,← strength_of_real]
  simpa [metricFlip_apply,shellEmbedding,realLift,apply_ite,Complex.ofReal_neg] using h

def lowerColumn (ν : Fin 4) : Spacetime →L[ℝ] TensorValue :=
  ContinuousLinearMap.pi (fun μ => ContinuousLinearMap.pi (fun ρ =>
    if ρ=ν then Complex.ofRealCLM.comp ((PiLp.proj 2 (fun _:Fin 4=>ℝ) μ).comp
      metricFlip.toContinuousLinearMap) else 0))

def divergenceTensor (b : 𝓢(Spacetime,ℂ)) (ν : Fin 4) : SchwartzTensor :=
  SchwartzMap.bilinLeftCLM (ContinuousLinearMap.lsmul ℂ ℂ) (lowerColumn ν).hasTemperateGrowth b

theorem divergenceTensor_apply (b : 𝓢(Spacetime,ℂ)) (ν : Fin 4) (p : Spacetime) (μ ρ : Fin 4) :
    divergenceTensor b ν p μ ρ = b p * (if ρ=ν then (metricFlip p μ:ℂ) else 0) := by
  simp [divergenceTensor,SchwartzMap.bilinLeftCLM_apply,lowerColumn]

theorem coefficient_divergenceTensor_regular (b : 𝓢(Spacetime,ℂ)) (ν : Fin 4)
    (y : MomentumCoordinates) (hy : y.1≠0) : globalCoefficient (divergenceTensor b ν) y=0 := by
  apply PiLp.ext
  intro j
  change (1/2:ℂ)*(∑ μ,∑ ρ,(cartesianStrength y j μ ρ:ℂ)*divergenceTensor b ν (shellEmbedding y) μ ρ)=0
  simp_rw [divergenceTensor_apply]
  simp only [mul_ite,mul_zero,Finset.sum_ite_eq',Finset.mem_univ,ite_true]
  have he : (∑ μ,(cartesianStrength y j μ ν:ℂ)*(b (shellEmbedding y)*(metricFlip (shellEmbedding y) μ:ℂ)))=
      b (shellEmbedding y)*(∑ μ,(metricFlip (shellEmbedding y) μ:ℂ)*(cartesianStrength y j μ ν:ℂ)) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro μ _
    ring
  rw [he,cartesian_divergence_regular y hy j ν]
  simp

theorem momentumSmear_divergence_zero (b : 𝓢(Spacetime,ℂ)) (ν : Fin 4) :
    momentumSmear (divergenceTensor b ν)=0 := by
  have hreg : ∀ᵐ y ∂orbitalMeasure 0,y.1≠(0:Transverse) := by
    rw [ae_iff]
    have hs : {y : MomentumCoordinates | ¬ y.1≠(0:Transverse)}=
        ({0}:Set Transverse)×ˢ(Set.univ:Set ℝ) := by ext y; simp
    rw [hs]
    exact exceptional_axis_orbital_null 0
  apply Lp.ext
  filter_upwards [(globalCoefficient_memLp (divergenceTensor b ν)).coeFn_toLp,
    Lp.coeFn_zero Fib 2 (orbitalMeasure 0),hreg] with y h1 h2 hy
  change ((globalCoefficient_memLp (divergenceTensor b ν)).toLp _) y=(0:H1) y
  rw [h1,h2,coefficient_divergenceTensor_regular b ν y hy]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.cartesian_divergence_regular
#print axioms F1Fecho.MaxwellGlobal.divergenceTensor_apply
#print axioms F1Fecho.MaxwellGlobal.momentumSmear_divergence_zero
