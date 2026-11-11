import Mathlib.Analysis.Fourier.LpSpace
import TGLExt.V350L2CharacterMultiplier

set_option autoImplicit false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open MeasureTheory FourierTransform SchwartzMap Filter
open scoped FourierTransform ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The existing L² translation agrees with translation of a Schwartz function. -/
theorem shift_schwartz_toLp (t : ℝ) (f : 𝓢(ℝ, H)) :
    shift t (f.toLp 2) = (f.compSubConstCLM ℂ t).toLp 2 := by
  apply Lp.ext
  filter_upwards [shift_ae t (f.toLp 2),
    (f.compSubConstCLM ℂ t).coeFn_toLp 2,
    (measurePreserving_sub_right volume t).quasiMeasurePreserving.ae (f.coeFn_toLp 2 volume)]
    with x h1 h2 h3
  change (shift t (f.toLp 2)) x = ((f.compSubConstCLM ℂ t).toLp 2) x
  rw [h1, h2, h3]
  rfl

/-- Fourier converts translation into the existing negative-sign character multiplier. -/
theorem fourier_shift_schwartz (t : ℝ) (f : 𝓢(ℝ, H)) :
    𝓕 (shift t (f.toLp 2)) =
      characterMultiplier (2 * Real.pi * t) (𝓕 (f.toLp 2)) := by
  rw [shift_schwartz_toLp, SchwartzMap.toLp_fourier_eq, SchwartzMap.toLp_fourier_eq]
  apply Lp.ext
  filter_upwards [(𝓕 (f.compSubConstCLM ℂ t)).coeFn_toLp 2,
    characterMultiplier_ae (2 * Real.pi * t) ((𝓕 f).toLp 2),
    (𝓕 f).coeFn_toLp 2] with x h1 h2 h3
  rw [h1, h2, h3]
  have h := congrFun (VectorFourier.fourierIntegral_comp_add_right
    Real.fourierChar volume (innerₗ ℝ) (f : ℝ → H) (-t)) x
  change (𝓕 (fun y : ℝ => f (y + -t))) x =
    Real.fourierChar (inner ℝ (-t) x) • (𝓕 (f : ℝ → H)) x at h
  change (𝓕 (fun y : ℝ => f (y-t))) x = _
  rw [show (fun y : ℝ => f (y-t)) = (fun y : ℝ => f (y + -t)) by rfl, h]
  rw [Circle.smul_def, Real.fourierChar_apply]
  congr 2
  simp only [Real.inner_apply, Complex.ofReal_mul, Complex.ofReal_neg]
  ring

/-- Spectral translation law on all of the same Lebesgue L² space, by Schwartz density. -/
theorem fourier_shift (t : ℝ) (f : RegularHilbert H) :
    Lp.fourierTransformₗᵢ ℝ H (shift t f) =
      characterMultiplier (2 * Real.pi * t) (Lp.fourierTransformₗᵢ ℝ H f) := by
  let p : RegularHilbert H → Prop := fun g =>
    Lp.fourierTransformₗᵢ ℝ H (shift t g) =
      characterMultiplier (2 * Real.pi * t) (Lp.fourierTransformₗᵢ ℝ H g)
  apply DenseRange.induction_on (p := p)
    (SchwartzMap.denseRange_toLpCLM (E := ℝ) (F := H) (p := 2) ENNReal.ofNat_ne_top) f
  · exact isClosed_eq
      ((Lp.fourierTransformₗᵢ ℝ H).continuous.comp (shift t).continuous)
      ((characterMultiplier (2 * Real.pi * t)).continuous.comp
        (Lp.fourierTransformₗᵢ ℝ H).continuous)
  intro g
  exact fourier_shift_schwartz t g

#print axioms shift_schwartz_toLp
#print axioms fourier_shift_schwartz
#print axioms fourier_shift
end
end TGLV350.Regular
