import TGLExt.TheTraceIsNotErasable

set_option autoImplicit false

/-!
# Pedra da gerência c1 (02/11/2026), sobre a fala do operador; NOME RATIFICADO pelo operador em 03/11/2026 (verbatim sha16 `73466598d3419fb0`: «concordo com todos os nomes e os ratifico»); entra no kernel na v407; compilada no sandbox da v407 (k407c/final), só no trio.

«nunca se chega inteiro no sentido de 100% mas se chega inteiro no sentido de perfeitamente identificável ao núcleo
invariável da identidade mesmo que haja alteração na forma, o conteúdo preservado permite reconstruir integralmente a forma»

Fora da diagonal está a forma (a coerência); na diagonal, o registro (a leitura). Dimensão finita. `dephase g (-t)` é a inversa
algébrica: amplifica, logo não é canal físico; é conta de quem conhece o registro `t`, não processo. Vale para `t` finito.
-/

namespace TGLExt.LeituraPreservada
open TGLExt Matrix

variable {n : Type} [Fintype n] [DecidableEq n]

omit [Fintype n] [DecidableEq n] in
/-- A forma se reconstrói integralmente: conhecido o registro `t`, a inversa algébrica devolve `x`. -/
theorem a_forma_se_reconstroi (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) :
    dephase g (-t) (dephase g t x) = x := by
  rw [← dephase_add, neg_add_cancel, dephase_zero]

omit [Fintype n] [DecidableEq n] in
/-- Há perda: fora da diagonal, com taxa positiva, a coerência cai estritamente. Nunca 100%. -/
theorem ha_perda (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) (i j : n)
    (ht : 0 < t) (hg : 0 < g i j) (hx : x i j ≠ 0) :
    ‖dephase g t x i j‖ < ‖x i j‖ := by
  have hpos : 0 < ‖x i j‖ := norm_pos_iff.mpr hx
  have hexp : Real.exp (-(t * g i j)) < 1 := by
    rw [Real.exp_lt_one_iff]
    nlinarith [mul_pos ht hg]
  have hn : ‖((Real.exp (-(t * g i j)) : ℝ) : ℂ)‖ = Real.exp (-(t * g i j)) := by
    rw [Complex.norm_real, Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
  simp only [dephase, Matrix.of_apply, norm_mul, hn]
  nlinarith

omit [Fintype n] [DecidableEq n] in
/-- A perda nunca chega a zero: em tempo finito, coerência não nula segue não nula. -/
theorem a_forma_nunca_zera (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) (i j : n) (hx : x i j ≠ 0) :
    dephase g t x i j ≠ 0 := by
  simp only [dephase, Matrix.of_apply]
  exact mul_ne_zero (by exact_mod_cast (Real.exp_pos _).ne') hx

/-- O fecho: a perda é da forma; a leitura e o total ficam; a forma se reconstrói. -/
theorem a_leitura_preservada (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ) (ht : 0 < t)
    (x : Matrix n n ℂ) (i j : n) (hg : 0 < g i j) (hx : x i j ≠ 0) :
    ‖dephase g t x i j‖ < ‖x i j‖ ∧
    dephase g t x i j ≠ 0 ∧
    diagExpect (dephase g t x) = diagExpect x ∧
    (dephase g t x).trace = x.trace ∧
    dephase g (-t) (dephase g t x) = x :=
  ⟨ha_perda g t x i j ht hg hx, a_forma_nunca_zera g t x i j hx, diag_invariant g hg0 t x,
    dephase_preserves_trace g hg0 t x, a_forma_se_reconstroi g t x⟩

end TGLExt.LeituraPreservada
