import PolarizerModularCost
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Topology.Algebra.InfiniteSum.ENNReal
import Mathlib.Tactic

set_option autoImplicit false

namespace ChatgptAudit.Cost054

noncomputable section

/-- Every term is nonnegative, including for a negative transition ratio. -/
theorem polarizer_cost_series_term_nonneg (d : ℝ) (n : ℕ) :
    0 ≤ (2 : ℝ) / (2 * (n : ℝ) + 1) * d ^ (2 * (n + 1)) := by
  apply mul_nonneg
  · positivity
  · rw [pow_mul]
    positivity

/-- The scalar series gives the quadratic coefficient, not the second derivative. -/
theorem polarizer_cost_hasSum (d : ℝ) (hd : |d| < 1) :
    HasSum (fun n : ℕ =>
      (2 : ℝ) / (2 * (n : ℝ) + 1) * d ^ (2 * (n + 1)))
      (d * (Real.log (1 + d) - Real.log (1 - d))) := by
  have hs := (Real.hasSum_log_sub_log_of_abs_lt_one hd).mul_left d
  apply hs.congr_fun
  intro n
  rw [show 2 * (n + 1) = 2 * n + 1 + 1 by omega, pow_succ]
  ring

theorem polarizer_cost_log_ratio_hasSum (d : ℝ) (hd : |d| < 1) :
    HasSum (fun n : ℕ =>
      (2 : ℝ) / (2 * (n : ℝ) + 1) * d ^ (2 * (n + 1)))
      (d * Real.log ((1 + d) / (1 - d))) := by
  have hp : 0 < 1 + d := by
    have hh := (abs_lt.mp hd).1
    linarith
  have hm : 0 < 1 - d := by
    have hh := (abs_lt.mp hd).2
    linarith
  simpa only [Real.log_div (ne_of_gt hp) (ne_of_gt hm)] using
    polarizer_cost_hasSum d hd

theorem polarizer_weight_ratio_abs_lt_one (wi wj : ℝ)
    (hi : 0 < wi) (hj : 0 < wj) :
    |(wi - wj) / (wi + wj)| < 1 := by
  rw [abs_lt]
  constructor
  · apply (lt_div_iff₀ (add_pos hi hj)).2
    linarith
  · apply (div_lt_iff₀ (add_pos hi hj)).2
    linarith

/-- This identity does not divide by the signed ratio, so equal weights are included. -/
theorem polarizer_weight_ratio_identity (wi wj : ℝ)
    (hi : 0 < wi) (hj : 0 < wj) :
    (1 + (wi - wj) / (wi + wj)) /
      (1 - (wi - wj) / (wi + wj)) = wi / wj := by
  have hsum : wi + wj ≠ 0 := ne_of_gt (add_pos hi hj)
  have hden : 1 - (wi - wj) / (wi + wj) ≠ 0 := by
    have hh := (abs_lt.mp (polarizer_weight_ratio_abs_lt_one wi wj hi hj)).2
    linarith
  field_simp [hsum, hden, ne_of_gt hj]
  ring

theorem polarizer_cost_weights_hasSum (wi wj : ℝ)
    (hi : 0 < wi) (hj : 0 < wj) :
    HasSum (fun n : ℕ =>
      (2 : ℝ) / (2 * (n : ℝ) + 1) *
        ((wi - wj) / (wi + wj)) ^ (2 * (n + 1)))
      (((wi - wj) / (wi + wj)) * (Real.log wi - Real.log wj)) := by
  have hs := polarizer_cost_log_ratio_hasSum ((wi - wj) / (wi + wj))
    (polarizer_weight_ratio_abs_lt_one wi wj hi hj)
  simpa only [polarizer_weight_ratio_identity wi wj hi hj,
    Real.log_div (ne_of_gt hi) (ne_of_gt hj)] using hs

theorem polarizer_cost_scalar_nonneg (d : ℝ) (hd : |d| < 1) :
    0 ≤ d * (Real.log (1 + d) - Real.log (1 - d)) := by
  rw [← (polarizer_cost_hasSum d hd).tsum_eq]
  exact tsum_nonneg (polarizer_cost_series_term_nonneg d)

/-- The extended sum is identified only after real summability has been proved. -/
theorem polarizer_cost_scalar_ennreal (d : ℝ) (hd : |d| < 1) :
    (∑' n : ℕ, ENNReal.ofReal
      ((2 : ℝ) / (2 * (n : ℝ) + 1) * d ^ (2 * (n + 1)))) =
      ENNReal.ofReal (d * (Real.log (1 + d) - Real.log (1 - d))) := by
  have hs := polarizer_cost_hasSum d hd
  rw [← ENNReal.ofReal_tsum_of_nonneg
    (polarizer_cost_series_term_nonneg d) hs.summable, hs.tsum_eq]

theorem polarizer_cost_weights_ennreal (wi wj : ℝ)
    (hi : 0 < wi) (hj : 0 < wj) :
    (∑' n : ℕ, ENNReal.ofReal
      ((2 : ℝ) / (2 * (n : ℝ) + 1) *
        ((wi - wj) / (wi + wj)) ^ (2 * (n + 1)))) =
      ENNReal.ofReal (((wi - wj) / (wi + wj)) *
        (Real.log wi - Real.log wj)) := by
  have hs := polarizer_cost_weights_hasSum wi wj hi hj
  rw [← ENNReal.ofReal_tsum_of_nonneg
    (polarizer_cost_series_term_nonneg ((wi - wj) / (wi + wj)))
    hs.summable, hs.tsum_eq]

section NormPowers

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

/-- A proved norm law evaluates the existing extended cost; no spectral law is assumed
for arbitrary vectors. -/
theorem polarizer_cost_of_norm_powers (D : H →L[ℝ] H) (x : H)
    (d : ℝ) (hd : |d| < 1)
    (hnorm : ∀ n : ℕ,
      ‖(D ^ (n + 1)) x‖ ^ 2 = d ^ (2 * (n + 1)) * ‖x‖ ^ 2) :
    polarizerModularCost D x =
      ENNReal.ofReal (d * (Real.log (1 + d) - Real.log (1 - d)) * ‖x‖ ^ 2) := by
  apply polarizer_modular_cost_eq_of_hasSum
  have hs := (polarizer_cost_hasSum d hd).mul_right (‖x‖ ^ 2)
  apply hs.congr_fun
  intro n
  rw [hnorm n]
  ring

theorem polarizer_cost_of_weight_norm_powers (D : H →L[ℝ] H) (x : H)
    (wi wj : ℝ) (hi : 0 < wi) (hj : 0 < wj)
    (hnorm : ∀ n : ℕ, ‖(D ^ (n + 1)) x‖ ^ 2 =
      ((wi - wj) / (wi + wj)) ^ (2 * (n + 1)) * ‖x‖ ^ 2) :
    polarizerModularCost D x =
      ENNReal.ofReal (((wi - wj) / (wi + wj)) *
        (Real.log wi - Real.log wj) * ‖x‖ ^ 2) := by
  apply polarizer_modular_cost_eq_of_hasSum
  have hs := (polarizer_cost_weights_hasSum wi wj hi hj).mul_right (‖x‖ ^ 2)
  apply hs.congr_fun
  intro n
  rw [hnorm n]
  ring

theorem polarizer_cost_norm_powers_lt_top (D : H →L[ℝ] H) (x : H)
    (d : ℝ) (hd : |d| < 1)
    (hnorm : ∀ n : ℕ,
      ‖(D ^ (n + 1)) x‖ ^ 2 = d ^ (2 * (n + 1)) * ‖x‖ ^ 2) :
    polarizerModularCost D x < ⊤ := by
  rw [polarizer_cost_of_norm_powers D x d hd hnorm]
  exact ENNReal.ofReal_lt_top

end NormPowers

#print axioms polarizer_cost_series_term_nonneg
#print axioms polarizer_cost_hasSum
#print axioms polarizer_cost_log_ratio_hasSum
#print axioms polarizer_weight_ratio_abs_lt_one
#print axioms polarizer_weight_ratio_identity
#print axioms polarizer_cost_weights_hasSum
#print axioms polarizer_cost_scalar_nonneg
#print axioms polarizer_cost_scalar_ennreal
#print axioms polarizer_cost_weights_ennreal
#print axioms polarizer_cost_of_norm_powers
#print axioms polarizer_cost_of_weight_norm_powers
#print axioms polarizer_cost_norm_powers_lt_top

end
end ChatgptAudit.Cost054
