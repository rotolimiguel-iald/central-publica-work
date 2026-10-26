import TGLExt.V350DualWeightForm

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1400000

namespace TGLV350.Regular
open MeasureTheory
open scoped ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Monotone exhaustion by finite intervals, with no finiteness assumption on the integral. -/
theorem lintegral_eq_iSup_symmetric_cuts (f : ℝ → ℝ≥0∞) (hf : Measurable f) :
    (∫⁻ s, f s) = ⨆ n : ℕ, ∫⁻ s in Set.Ioc (-(n : ℝ)) (n : ℝ), f s := by
  let cut : ℕ → Set ℝ := fun n => Set.Ioc (-(n : ℝ)) (n : ℝ)
  let g : ℕ → ℝ → ℝ≥0∞ := fun n => (cut n).indicator f
  have hg : ∀ n, Measurable (g n) := fun n => hf.indicator measurableSet_Ioc
  have hmono : Monotone g := by
    intro n m hnm s
    have hnmr : (n : ℝ) ≤ (m : ℝ) := by exact_mod_cast hnm
    by_cases hs : s ∈ cut n
    · have hsm : s ∈ cut m := ⟨by have := hs.1; dsimp [cut] at *; linarith,
        by have := hs.2; dsimp [cut] at *; linarith⟩
      simp only [g, Set.indicator_of_mem hs, Set.indicator_of_mem hsm, le_refl]
    · simp only [g, Set.indicator_of_notMem hs]
      exact zero_le
  have hs : (fun s => ⨆ n, g n s) = f := by
    funext s
    apply le_antisymm
    · apply iSup_le
      intro n
      by_cases h : s ∈ cut n
      · simp only [g, Set.indicator_of_mem h, le_refl]
      · simp only [g, Set.indicator_of_notMem h, zero_le]
    · obtain ⟨n, hn⟩ := exists_nat_gt |s|
      have h : s ∈ cut n := by
        constructor
        · have := neg_abs_le s
          linarith
        · exact (le_abs_self s).trans hn.le
      calc
        f s = g n s := by simp only [g, Set.indicator_of_mem h]
        _ ≤ ⨆ n, g n s := le_iSup (fun n => g n s) n
  calc
    (∫⁻ s, f s) = ∫⁻ s, ⨆ n, g n s := by rw [hs]
    _ = ⨆ n, ∫⁻ s, g n s := lintegral_iSup hg hmono
    _ = _ := by
      apply congrArg iSup
      funext n
      exact lintegral_indicator measurableSet_Ioc f

/-- The extended quadratic evaluation is exactly the supremum of the constructed
strong cuts, with dual Haar normalization. No bounded supremum in B(H) is asserted. -/
theorem dualQuadraticIntegral_eq_iSup_cuts
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (v : RegularHilbert H) :
    dualQuadraticIntegral A v = ⨆ n : ℕ,
      ENNReal.ofReal dualHaarFactor *
        ENNReal.ofReal (inner ℂ v (dualWeightCut (n : ℝ) A v)).re := by
  rw [dualQuadraticIntegral,
    lintegral_eq_iSup_symmetric_cuts _ (dualQuadraticIntegrand_measurable A v),
    ENNReal.mul_iSup]
  apply congrArg iSup
  funext n
  rw [dualWeightCut_quadratic (n : ℝ) (Nat.cast_nonneg n) A hA v]

/-- The unit's quadratic supremum really is infinite, so the cutoff family cannot
be mistaken for a normalized state or a bounded expectation. -/
theorem dual_unit_cut_supremum_infinite (v : RegularHilbert H) (hv : v ≠ 0) :
    (⨆ n : ℕ, ENNReal.ofReal dualHaarFactor *
      ENNReal.ofReal (inner ℂ v (dualWeightCut (n : ℝ) 1 v)).re) = ⊤ := by
  rw [← dualQuadraticIntegral_eq_iSup_cuts
    (1 : RegularHilbert H →L[ℂ] RegularHilbert H) zero_le_one v,
    dualQuadraticIntegral_one v hv]

#print axioms lintegral_eq_iSup_symmetric_cuts
#print axioms dualQuadraticIntegral_eq_iSup_cuts
#print axioms dual_unit_cut_supremum_infinite
end
end TGLV350.Regular
