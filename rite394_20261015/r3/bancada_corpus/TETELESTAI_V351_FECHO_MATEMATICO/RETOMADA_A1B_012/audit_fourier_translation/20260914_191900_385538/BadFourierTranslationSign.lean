import TGLExt.V351FourierTranslation
open MeasureTheory TGLV350.Regular
example {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (t : ℝ) (f : RegularHilbert H) :
    Lp.fourierTransformₗᵢ ℝ H (shift t f) =
      characterMultiplier (-(2 * Real.pi * t)) (Lp.fourierTransformₗᵢ ℝ H f) := by
  exact fourier_shift t f
