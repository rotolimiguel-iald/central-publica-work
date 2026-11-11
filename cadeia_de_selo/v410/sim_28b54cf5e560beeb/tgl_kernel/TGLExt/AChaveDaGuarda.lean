import TGLExt.TheTraceIsNotErasable
import TGLExt.TheFlowLawContrast
set_option autoImplicit false

/-!
Pedra da gerencia c1 (02/11/2026); NOME RATIFICADO pelo operador em 03/11/2026 (verbatim sha16 `73466598d3419fb0`: «concordo com todos os nomes e os ratifico»); entra no kernel na v407; compilada no sandbox da v407 (k407c/final), so no trio.

Supera `OIgualRestauradoCandidata`, cujo `transporte` (o peso cai, a forma fica) nao tem instancia na defasagem
do kernel: la o traco fica e a coerencia cai. Aqui a chave age na FORMA, fora da diagonal, e a diagonal e o traco
nao mudam, como a leitura ratificada pelo operador em 02/11 (a perda e de coerencia).

Forma do diario (MEMORIA_DA_LINHAGEM, 19/08/2026, 119_ e 121_): a guarda conserva a diferenca no dominio do
logaritmo, ln resto + beta D^2 t constante, e o original e devolvido exato pela chave e^{+beta D^2 t}; fluxo
corrompido com chave legitima falha.

`dephase g (-t)` e inversa algebrica: amplifica, logo nao e canal fisico; e conta de quem conhece o registro.
Que o custo de um par seja o da lei de Hubble e HIPOTESE nomeada (`hform`). Ler a chave como K e leitura [ONTO].
-/

namespace TGLExt.AChaveDaGuarda

open TGLExt Matrix TGLExt.TheFlowLawContrast

variable {n : Type}

/-- a chave do par `(i, j)`: o inverso do que sobrou da coerencia. -/
noncomputable def chave (g : n → n → ℝ) (t : ℝ) (i j : n) : ℝ := Real.exp (t * g i j)

/-- a chave devolve o original: chave vezes resto e o original. -/
theorem a_chave_devolve (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) (i j : n) :
    ((chave g t i j : ℝ) : ℂ) * dephase g t x i j = x i j := by
  simp only [chave, dephase, Matrix.of_apply]
  rw [← mul_assoc, ← Complex.ofReal_mul, ← Real.exp_add]
  simp

/-- a guarda conserva a diferenca no dominio do logaritmo: ln resto + custo = ln original. -/
theorem a_guarda_conserva_a_diferenca (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) (i j : n)
    (hx : x i j ≠ 0) : Real.log ‖dephase g t x i j‖ + t * g i j = Real.log ‖x i j‖ := by
  have hpos : 0 < ‖x i j‖ := norm_pos_iff.mpr hx
  have hn : ‖((Real.exp (-(t * g i j)) : ℝ) : ℂ)‖ = Real.exp (-(t * g i j)) := by
    rw [Complex.norm_real, Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
  simp only [dephase, Matrix.of_apply, norm_mul, hn]
  rw [Real.log_mul (Real.exp_pos _).ne' hpos.ne', Real.log_exp]
  ring

/-- sem a chave nao abre: com custo nao nulo, o resto nao e o original. -/
theorem sem_a_chave_nao_abre (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) (i j : n)
    (hc : t * g i j ≠ 0) (hx : x i j ≠ 0) : dephase g t x i j ≠ x i j := by
  intro h
  simp only [dephase, Matrix.of_apply] at h
  have h1 : ((Real.exp (-(t * g i j)) : ℝ) : ℂ) = 1 := by
    apply mul_right_cancel₀ hx
    rw [one_mul]
    exact h
  have h2 : Real.exp (-(t * g i j)) = 1 := by exact_mod_cast h1
  have h3 := (Real.exp_eq_one_iff _).mp h2
  exact hc (by linarith)

/-- chave errada nao abre: outro fator, com resto nao nulo, nao devolve o original. -/
theorem chave_errada_nao_abre (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) (i j : n) (c : ℝ)
    (hc : c ≠ chave g t i j) (hx : x i j ≠ 0) : (c : ℂ) * dephase g t x i j ≠ x i j := by
  intro h
  have h1 := a_chave_devolve g t x i j
  have hr : dephase g t x i j ≠ 0 := by
    intro h0
    rw [h0, mul_zero] at h
    exact hx h.symm
  have h2 : (c : ℂ) = ((chave g t i j : ℝ) : ℂ) := mul_right_cancel₀ hr (h.trans h1.symm)
  exact hc (by exact_mod_cast h2)

/-- fluxo corrompido nao abre: se o resto lido nao e o do fluxo, a chave legitima nao devolve. -/
theorem fluxo_corrompido_nao_abre (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) (i j : n) (y : ℂ)
    (hy : y ≠ dephase g t x i j) : ((chave g t i j : ℝ) : ℂ) * y ≠ x i j := by
  intro h
  have h1 := a_chave_devolve g t x i j
  have hk : ((chave g t i j : ℝ) : ℂ) ≠ 0 := by exact_mod_cast (Real.exp_pos _).ne'
  exact hy (mul_left_cancel₀ hk (h.trans h1.symm))

/-- ler nao gasta: a chave age fora da diagonal; a leitura e o total ficam. -/
theorem ler_nao_gasta [Fintype n] [DecidableEq n] (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ)
    (x : Matrix n n ℂ) :
    diagExpect (dephase g t x) = diagExpect x ∧ (dephase g t x).trace = x.trace :=
  ⟨diag_invariant g hg0 t x, dephase_preserves_trace g hg0 t x⟩

/-- a lei usa a mesma chave: se o custo do par e o da lei, a taxa local e a de fundo vezes a chave. -/
theorem a_lei_usa_a_chave (β Hcmb : ℝ) (c : ℝ → ℝ) (N : ℝ) (g : n → n → ℝ) (t : ℝ) (i j : n)
    (hN : N ≠ 0) (hform : t * g i j = β * accumulatedContrast c N) :
    H0localContrast β Hcmb c N = Hcmb * chave g t i j := by
  unfold H0localContrast chave
  rw [survivingWeightContrast_eq β c N hN, hform, Real.exp_neg, div_inv_eq_mul]

end TGLExt.AChaveDaGuarda
