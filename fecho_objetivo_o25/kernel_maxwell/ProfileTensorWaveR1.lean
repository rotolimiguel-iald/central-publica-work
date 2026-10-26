import ProfileMaxwellWaveR5
import Mathlib.MeasureTheory.SpecificCodomains.Pi

/-! Bochner realization of all sixteen components of the same regular Maxwell
wave. This permits continuous tensor maps to pass through the actual integral. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory TGLExt.ImportedSQ
open ChatgptAudit.WignerRapidityMeasure016

def tensorDensity (h : H1) (y : MomentumCoordinates) : TensorValue :=
  fun μ ν=>profileDensity h μ ν y

def tensorWaveIntegrand (h : H1) (x : Spacetime) (y : MomentumCoordinates) : TensorValue :=
  wavePhase x y • tensorDensity h y

theorem profileWaveIntegrand_integrable (h : H1) (hh : RegularProfile h)
    (μ ν : Fin 4) (x : Spacetime) :
    Integrable (fun y=>wavePhase x y*profileDensity h μ ν y) (orbitalMeasure 0) := by
  apply (profileDensity_integrable h hh μ ν).norm.mono'
  · exact (wavePhase_continuous_right x).measurable.aestronglyMeasurable.mul
      (profileDensity_measurable h μ ν)
  · exact ae_of_all _ (fun y=>by rw [norm_mul,wavePhase_norm,one_mul])

theorem tensorWaveIntegrand_integrable (h : H1) (hh : RegularProfile h) (x : Spacetime) :
    Integrable (tensorWaveIntegrand h x) (orbitalMeasure 0) := by
  apply Integrable.of_eval
  intro μ
  apply Integrable.of_eval
  intro ν
  exact profileWaveIntegrand_integrable h hh μ ν x

theorem profileWave_tensor_integral (h : H1) (hh : RegularProfile h) (x : Spacetime) :
    (fun μ ν=>profileWave h μ ν x)=∫y,tensorWaveIntegrand h x y ∂orbitalMeasure 0 := by
  ext μ ν
  rw [eval_integral (fun μ=>(tensorWaveIntegrand_integrable h hh x).eval μ)]
  rw [eval_integral (fun ν=>((tensorWaveIntegrand_integrable h hh x).eval μ).eval ν)]
  rfl

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.profileWaveIntegrand_integrable
#print axioms F1Fecho.MaxwellGlobal.tensorWaveIntegrand_integrable
#print axioms F1Fecho.MaxwellGlobal.profileWave_tensor_integral
