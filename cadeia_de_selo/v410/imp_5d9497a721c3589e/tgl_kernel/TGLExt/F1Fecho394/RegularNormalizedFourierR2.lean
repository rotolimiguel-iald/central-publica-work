import TGLExt.F1Fecho394.RegularL2RescaleR4
import TGLExt.F1Fecho394.RegularFourierFibreR1
import TGLExt.F1Fecho394.RegularSpectralCodeR2
/-! The actual normalized Fourier isometry and regular coefficient code.
The range is closed and bounded fibre operators intertwine. Identification
with the dual-weight GNS range is a separate obligation, not an input here. -/
set_option autoImplicit false
set_option maxErrors 3
set_option maxHeartbeats 900000
noncomputable section
namespace F1Fecho.RegularNormalizedFourier
open MeasureTheory TGLV350.Regular
open scoped FourierTransform
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem rescale_fibre (c : ℝ) (hc : 0 < c) (C : H →L[ℂ] H) (f : RegularHilbert H) :
    RegularL2Rescale.rescale c hc (fibre C f) =
      fibre C (RegularL2Rescale.rescale c hc f) := by
  apply Lp.ext
  filter_upwards [RegularL2Rescale.rescale_ae c hc (fibre C f),
    (RegularL2Rescale.div_qmp c hc).ae (fibre_ae C f),
    fibre_ae C (RegularL2Rescale.rescale c hc f),RegularL2Rescale.rescale_ae c hc f]
    with x h1 h2 h3 h4
  rw [h1,h2,h3,h4]
  exact (C.map_smul_of_tower ((Real.sqrt c)⁻¹ : ℝ) (f (x/c))).symm

def normalizedFourier : RegularHilbert H ≃ₗᵢ[ℂ] RegularHilbert H :=
  (Lp.fourierTransformₗᵢ ℝ H).trans
    (RegularL2Rescale.rescaleEquiv (2*Real.pi) (by positivity))

theorem normalizedFourier_ae (f : RegularHilbert H) :
    normalizedFourier f =ᵐ[volume] fun s : ℝ =>
      ((Real.sqrt (2*Real.pi))⁻¹ : ℝ) • (Lp.fourierTransformₗᵢ ℝ H f) (s/(2*Real.pi)) :=
  RegularL2Rescale.rescale_ae (2*Real.pi) (by positivity) _

theorem normalizedFourier_fibre (C : H →L[ℂ] H) (f : RegularHilbert H) :
    normalizedFourier (fibre C f) = fibre C (normalizedFourier f) := by
  change RegularL2Rescale.rescale (2*Real.pi) (by positivity) (Lp.fourierTransformₗᵢ ℝ H (fibre C f)) = _
  rw [RegularFourierFibre.fourier_fibre,rescale_fibre]
  rfl

def spectralCode : RegularHilbert H →ₗᵢ[ℂ] RegularHilbert (RegularHilbert H) :=
  normalizedFourier.toLinearIsometry.comp RegularSpectralCode.codeIsometry

theorem spectralCode_fibre (C : H →L[ℂ] H) (f : RegularHilbert H) :
    spectralCode (fibre C f) = fibre (fibre C) (spectralCode f) := by
  change normalizedFourier (RegularSpectralCode.code (fibre C f)) = _
  rw [RegularSpectralCode.code_fibre,normalizedFourier_fibre]
  rfl

theorem spectralCode_injective : Function.Injective (spectralCode (H:=H)) :=
  spectralCode.injective

theorem spectralCode_closedRange : IsClosed (Set.range (spectralCode (H:=H))) :=
  spectralCode.isometry.isClosedEmbedding.isClosed_range

end F1Fecho.RegularNormalizedFourier
#print axioms F1Fecho.RegularNormalizedFourier.rescale_fibre
#print axioms F1Fecho.RegularNormalizedFourier.normalizedFourier
#print axioms F1Fecho.RegularNormalizedFourier.normalizedFourier_ae
#print axioms F1Fecho.RegularNormalizedFourier.normalizedFourier_fibre
#print axioms F1Fecho.RegularNormalizedFourier.spectralCode
#print axioms F1Fecho.RegularNormalizedFourier.spectralCode_fibre
#print axioms F1Fecho.RegularNormalizedFourier.spectralCode_injective
#print axioms F1Fecho.RegularNormalizedFourier.spectralCode_closedRange
