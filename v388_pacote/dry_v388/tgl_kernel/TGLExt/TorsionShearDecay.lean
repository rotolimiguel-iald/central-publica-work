import Mathlib

set_option autoImplicit false
set_option linter.unusedVariables false

/-!
# A VISCOSIDADE NEGATIVA NÃO FAZ O CISALHAMENTO CRESCER
  [TGLExt — a dinâmica do fornecedor de torção da v364, a parte algébrica]

Em Bianchi I com a torção tracial (A = α n) e matéria perfeita, a parte sem traço de G̊ = κ(T^mat + T^tors)
é σ̇ = −(3H − 2α)σ (o lado de Einstein dá σ̇ + 3Hσ; o fornecedor dá +2ασ — a viscosidade de cisalhamento
negativa; medido em runtime). No ramo em expansão da lei com torção, H = α + √(κρ/3) ≥ α. Esta pedra prova a
parte algébrica: a taxa de amortecimento é positiva nesse ramo (o cisalhamento decai), vale α na assíntota
H = α, e a torção reduz a taxa em exatamente 2α. Não identifica α com uma escala física [INPUT], não move
gate. Nenhuma lacuna de prova e nenhum axioma novo.
-/

namespace TGLExt.TorsionShearDecay

/-- [KERNEL] ★ no ramo em expansão (H ≥ α > 0) a taxa de amortecimento do cisalhamento é positiva -/
theorem shear_damping_rate_positive (H α : ℝ) (hα : 0 < α) (hH : α ≤ H) : 0 < 3 * H - 2 * α := by
  linarith

/-- [KERNEL] a taxa é pelo menos α no ramo em expansão -/
theorem shear_damping_rate_at_least_alpha (H α : ℝ) (hH : α ≤ H) : α ≤ 3 * H - 2 * α := by
  linarith

/-- [KERNEL] na assíntota de de Sitter (H = α) a taxa vale exatamente α (sem torção valeria 3α) -/
theorem shear_damping_rate_at_asymptote (α : ℝ) : 3 * α - 2 * α = α := by
  ring

/-- [KERNEL] o ramo em expansão da lei com torção: se H − α = √(κρ/3) então H ≥ α -/
theorem expanding_branch_H_ge_alpha (H α κρ : ℝ) (h : H - α = Real.sqrt (κρ / 3)) : α ≤ H := by
  have := Real.sqrt_nonneg (κρ / 3)
  linarith

/-- [KERNEL] a lei de decaimento: se s(t) = s0·exp(−r t) com r > 0, então s(t) → 0 só no limite t → ∞
    (para todo t finito, s(t) ≠ 0 quando s0 ≠ 0) -/
theorem shear_never_zero_at_finite_time (s0 r t : ℝ) (hs0 : s0 ≠ 0) : s0 * Real.exp (-(r * t)) ≠ 0 :=
  mul_ne_zero hs0 (Real.exp_pos _).ne'

end TGLExt.TorsionShearDecay
