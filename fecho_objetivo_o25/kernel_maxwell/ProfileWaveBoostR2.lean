import MaxwellTensorBoostR2
import ProfileTensorWaveR1
import MaxwellMomentTransportR3
import CovariantTensorPullbackR3
import SpacetimeLorentzFourierR3

/-! Actual tensor covariance of the integrable regular Maxwell wave under the
canonical longitudinal boost. Both the mass-shell measure and both tensor
indices are transported. This is not yet a charge identity. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Matrix MeasureTheory TGLExt TGLExt.ImportedSQ F1Fecho.OrbitalSpatial
open F1Fecho.SpacetimeLorentz F1Fecho.CovariantTensor
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016

def boostTensor (s : ℝ) : TensorValue→L[ℂ]TensorValue :=
  pull (((theBoost s).val.map Complex.ofReal).transpose)

theorem tensorDensity_eq_sum (h : H1) (y : MomentumCoordinates) :
    tensorDensity h y=∑j : Fin 2,h y j •
      (fun μ ν=>(cartesianStrength y j μ ν:ℂ)) := by
  ext μ ν
  simp [tensorDensity,profileDensity,Finset.sum_apply,smul_eq_mul,mul_comm]

theorem complexStrength_boost_ae (s : ℝ) :
    ∀ᵐy ∂orbitalMeasure 0,∀j : Fin 2,
      (fun μ ν=>(cartesianStrength (coordinateBoost 0 s y) j μ ν:ℂ))=
      boostTensor s (fun μ ν=>(cartesianStrength y j μ ν:ℂ)) := by
  filter_upwards [cartesianStrength_boost_ae s] with y hy
  intro j
  ext μ ν
  rw [hy j]
  simp [boostTensor,pull,pullLinear,Matrix.mul_apply,Matrix.transpose_apply,
    Matrix.map_apply,Matrix.of_apply]

theorem tensorDensity_boost_ae (s : ℝ) (h : H1) :
    ∀ᵐy ∂orbitalMeasure 0,
      tensorDensity (B0 s h) (coordinateBoost 0 s y)=boostTensor s (tensorDensity h y) := by
  have hb:=(coordinateBoost_measurePreserving 0 s).quasiMeasurePreserving.ae
    (B0_profile_ae s h)
  filter_upwards [hb,coordinateBoost_inverse_ae (-s),complexStrength_boost_ae s] with y hy hi hs
  simp only [neg_neg,id_eq] at hi
  rw [tensorDensity_eq_sum,tensorDensity_eq_sum,map_sum]
  apply Finset.sum_congr rfl
  intro j _
  rw [map_smul,hy,hi,hs j]

theorem wavePhase_boost_ae (s : ℝ) (x : Spacetime) :
    ∀ᵐy ∂orbitalMeasure 0,wavePhase x (coordinateBoost 0 s y)=
      wavePhase ((action (theBoost s)).symm x) y := by
  filter_upwards [shell_boost_ae s] with y hy
  have hs : shellEmbedding (coordinateBoost 0 s y)=
      action (theBoost s) (shellEmbedding y) := by
    apply PiLp.ext
    intro i
    exact congrFun hy i
  have hp : inner ℝ (metricFlip (action (theBoost s) (shellEmbedding y))) x=
      inner ℝ (metricFlip (shellEmbedding y)) ((action (theBoost s)).symm x) := by
    simpa only [metricFlip_inner,orbitPairing,mul_comm] using
      pairing_transfer (theBoost s) (shellEmbedding y) x
  simp only [wavePhase,hs,hp]

theorem profileWave_boost (s : ℝ) (h : H1) (hh : RegularProfile h) (x : Spacetime) :
    (fun μ ν=>profileWave (B0 s h) μ ν x)=
      boostTensor s (fun μ ν=>profileWave h μ ν ((action (theBoost s)).symm x)) := by
  have hhB : RegularProfile (B0 s h) := by
    intro m
    simpa only [pow_one] using moment_B0_integrable s h m 1 (by
      simpa only [pow_one] using hh m)
  rw [profileWave_tensor_integral _ hhB,profileWave_tensor_integral _ hh]
  have hm:=coordinateBoost_measurePreserving 0 s
  have hi:=tensorWaveIntegrand_integrable (B0 s h) hhB x
  have hc:=MeasureTheory.integral_map hm.measurable.aemeasurable
    (show AEStronglyMeasurable (tensorWaveIntegrand (B0 s h) x)
      (Measure.map (coordinateBoost 0 s) (orbitalMeasure 0)) from by
        rw [hm.map_eq]; exact hi.aestronglyMeasurable)
  rw [hm.map_eq] at hc
  rw [hc]
  calc
    _ = ∫y,boostTensor s (tensorWaveIntegrand h ((action (theBoost s)).symm x) y)
        ∂orbitalMeasure 0 := by
      apply integral_congr_ae
      filter_upwards [tensorDensity_boost_ae s h,wavePhase_boost_ae s x] with y hd hp
      simp only [tensorWaveIntegrand,hd,hp,map_smul]
    _ = _ := (boostTensor s).integral_comp_comm
      (tensorWaveIntegrand_integrable h hh _)

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.complexStrength_boost_ae
#print axioms F1Fecho.MaxwellGlobal.tensorDensity_boost_ae
#print axioms F1Fecho.MaxwellGlobal.wavePhase_boost_ae
#print axioms F1Fecho.MaxwellGlobal.profileWave_boost
