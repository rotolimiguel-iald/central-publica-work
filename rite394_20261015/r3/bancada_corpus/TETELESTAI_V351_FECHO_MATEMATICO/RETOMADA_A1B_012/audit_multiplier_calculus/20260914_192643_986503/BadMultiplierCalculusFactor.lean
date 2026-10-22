import TGLExt.V351ScalarMultiplierCalculus
open TGLExt TGLV350.Regular MeasureTheory
example (g : ℝ → ℝ) (hg : Continuous g) (h0 : ∀ x, 0 ≤ g x) (h1 : ∀ x, g x ≤ 1)
    (f : ℂ → ℂ) (hf : Continuous f) (u : RegularHilbert ℂ) :
    cfc f (realScalarMultiplier g hg h0 h1) u =ᵐ[volume]
      fun x => (2 * f (g x : ℂ)) • u x := by
  exact realScalarMultiplier_cfc_ae g hg h0 h1 f hf u
