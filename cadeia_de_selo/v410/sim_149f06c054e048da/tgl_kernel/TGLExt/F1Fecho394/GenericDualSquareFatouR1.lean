import TGLExt.V351InverseLimitTracialExtension
/-! Generic lower semicontinuity for the actual dual quadratic integral. No finite value, monotone sequence, or convergence of adjoints is assumed. Reused from the v393 proof. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
namespace F1Fecho.QuadraticTraceForms
open TGLV350.Regular MeasureTheory Filter
open scoped Topology ENNReal
theorem dualSquare_le_of_strong {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : ℕ → RegularHilbert H →L[ℂ] RegularHilbert H)
    (S : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H)
    (hlim : ∀ w, Tendsto (fun n => A n w) atTop (𝓝 (S w)))
    (C : ℝ≥0∞) (hb : ∀ n, dualQuadraticIntegral (star (A n)*A n) v ≤ C) :
    dualQuadraticIntegral (star S*S) v ≤ C := by
  let f : ℕ → ℝ → ℝ≥0∞ := fun n s => ENNReal.ofReal dualHaarFactor *
    dualQuadraticIntegrand (star (A n)*A n) v s
  let g : ℝ → ℝ≥0∞ := fun s => ENNReal.ofReal dualHaarFactor *
    dualQuadraticIntegrand (star S*S) v s
  have hm (n : ℕ) : Measurable (f n) :=
    measurable_const.mul (dualQuadraticIntegrand_measurable _ _)
  have hl (s : ℝ) : Tendsto (fun n => f n s) atTop (𝓝 (g s)) := by
    have ht := (dualAmbient_tendsto_strong A S hlim s v).norm.pow 2
    have he := ENNReal.continuous_ofReal.continuousAt.tendsto.comp ht
    have hh := (ENNReal.continuous_const_mul (a := ENNReal.ofReal dualHaarFactor)
      ENNReal.ofReal_ne_top).continuousAt.tendsto.comp he
    simpa only [f,g,Function.comp_def,dualQuadraticIntegrand_star_mul] using hh
  have hi (n : ℕ) : (∫⁻ s, f n s) = dualQuadraticIntegral (star (A n)*A n) v :=
    lintegral_const_mul _ (dualQuadraticIntegrand_measurable _ _)
  have hg : (∫⁻ s, g s) = dualQuadraticIntegral (star S*S) v :=
    lintegral_const_mul _ (dualQuadraticIntegrand_measurable _ _)
  calc
    _ = ∫⁻ s, g s := hg.symm
    _ = ∫⁻ s, liminf (fun n => f n s) atTop :=
      lintegral_congr_ae (Eventually.of_forall fun s => (hl s).liminf_eq.symm)
    _ ≤ liminf (fun n => ∫⁻ s, f n s) atTop := lintegral_liminf_le hm
    _ ≤ C := liminf_le_of_frequently_le'
      (Eventually.of_forall (fun n => by rw [hi]; exact hb n)).frequently


end F1Fecho.QuadraticTraceForms
#print axioms F1Fecho.QuadraticTraceForms.dualSquare_le_of_strong
