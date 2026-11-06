import TGLExt.F1Fecho394.RegularNormalizedFourierR2
import TGLExt.V351FourierTranslation
/-! Exact translation/character covariance of the normalized coefficient code. -/
set_option autoImplicit false
set_option maxErrors 3
set_option maxHeartbeats 900000
noncomputable section
namespace F1Fecho.RegularSpectralTranslation
open MeasureTheory Filter TGLV350.Regular
open F1Fecho.RegularNormalizedFourier
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem phase_rescale (c t s : ℝ) (hc : c ≠ 0) :
    characterPhase (c*t) (s/c) = characterPhase t s := by
  unfold characterPhase
  congr 1
  push_cast
  have hcc : (c : ℂ) ≠ 0 := by exact_mod_cast hc
  field_simp [hcc]
  <;> ring

theorem rescale_character (c : ℝ) (hc : 0<c) (t : ℝ) (f : RegularHilbert H) :
    RegularL2Rescale.rescale c hc (characterMultiplier (c*t) f) =
      characterMultiplier t (RegularL2Rescale.rescale c hc f) := by
  apply Lp.ext
  filter_upwards [RegularL2Rescale.rescale_ae c hc (characterMultiplier (c*t) f),
    (RegularL2Rescale.div_qmp c hc).ae (characterMultiplier_ae (c*t) f),
    characterMultiplier_ae t (RegularL2Rescale.rescale c hc f),RegularL2Rescale.rescale_ae c hc f]
    with s h1 h2 h3 h4
  rw [h1,h2,h3,h4]
  change (Real.sqrt c)⁻¹ • (characterPhase (c*t) (s/c) • f (s/c)) =
    characterPhase t s • ((Real.sqrt c)⁻¹ • f (s/c))
  rw [phase_rescale c t s hc.ne',smul_comm]

theorem normalizedFourier_shift (t : ℝ) (f : RegularHilbert H) :
    normalizedFourier (shift t f) = characterMultiplier t (normalizedFourier f) := by
  change RegularL2Rescale.rescale (2*Real.pi) (by positivity)
    (Lp.fourierTransformₗᵢ ℝ H (shift t f)) = _
  rw [fourier_shift,rescale_character]
  rfl

theorem code_shift (t : ℝ) (f : RegularHilbert H) :
    RegularSpectralCode.code (shift t f) =
      fibre (shift t) (shift t (RegularSpectralCode.code f)) := by
  apply Lp.ext
  filter_upwards [RegularSpectralCode.code_ae (shift t f),shift_ae t f,
    fibre_ae (shift t) (shift t (RegularSpectralCode.code f)),
    shift_ae t (RegularSpectralCode.code f),
    (measurePreserving_sub_right volume t).quasiMeasurePreserving.ae (RegularSpectralCode.code_ae f)]
    with s h1 h2 h3 h4 h5
  rw [h1,h2,h3,h4,h5,←ContinuousLinearMap.mul_apply,shift_mul]
  congr 1
  congr 1
  ring

theorem spectralCode_shift (t : ℝ) (f : RegularHilbert H) :
    spectralCode (shift t f) =
      characterMultiplier t (fibre (shift t) (spectralCode f)) := by
  change normalizedFourier (RegularSpectralCode.code (shift t f)) = _
  rw [code_shift,normalizedFourier_fibre,normalizedFourier_shift]
  exact congrArg (fun T : RegularHilbert (RegularHilbert H) →L[ℂ]
      RegularHilbert (RegularHilbert H) => T (normalizedFourier (RegularSpectralCode.code f)))
      (characterMultiplier_commutes_fibre t (shift t)).symm

end F1Fecho.RegularSpectralTranslation
#print axioms F1Fecho.RegularSpectralTranslation.phase_rescale
#print axioms F1Fecho.RegularSpectralTranslation.rescale_character
#print axioms F1Fecho.RegularSpectralTranslation.normalizedFourier_shift
#print axioms F1Fecho.RegularSpectralTranslation.code_shift
#print axioms F1Fecho.RegularSpectralTranslation.spectralCode_shift
