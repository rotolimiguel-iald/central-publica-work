import Mathlib

set_option autoImplicit false

/-!
# Meia-Nat (Half-Nat) -- ponto fixo auto-conjugado   [KERNEL/UNCONDITIONAL]

A fronteira auto-conjugada `x = 1 - x` forca `x = 1/2`. O passo principal e'
algebrico (2x = 1), demonstrado por `linarith` -- nao por `norm_num`.
-/

namespace TGL.HalfNat

/-- A fronteira auto-conjugada `x = 1 - x` tem unico ponto fixo `x = 1/2`. -/
theorem halfNat_of_selfConjugate (x : ℝ) (h : x = 1 - x) : x = 1 / 2 := by
  linarith

/-- Caracterizacao: `x = 1 - x ↔ x = 1/2`. -/
theorem selfConjugate_halfNat_unique (x : ℝ) : x = 1 - x ↔ x = 1 / 2 := by
  constructor <;> intro h <;> linarith

end TGL.HalfNat
