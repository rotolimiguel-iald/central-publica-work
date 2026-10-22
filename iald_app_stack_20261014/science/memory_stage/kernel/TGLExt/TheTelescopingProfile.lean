import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Analysis.SpecificLimits.Basic

set_option autoImplicit false

/-!
# O PERFIL TELESCÓPICO — por que a razão 12 faz a estrutura aparecer
  [BANCADA — 26/08/2026 · leitura do operador: «essa equação em fração fica melhor de
   ser enxergada se a razão for 12»]

## O que o denominador 12 revela

O perfil do certificado usa pesos `1/3` e `1/4`. Postos sobre 12 — o menor denominador
comum — aparece uma identidade que os decimais escondem:

    (1/3)·(1/4) = 1/12    e    1/3 − 1/4 = 1/12

**O produto É a diferença.** E isso não é acidente destes dois números: vale sempre que
os pesos são **recíprocos consecutivos**, porque

    1/n − 1/(n+1) = 1/(n(n+1)) = (1/n)·(1/(n+1)).

O 12 é exatamente `3·4` — o produto que torna a identidade visível.

## E a consequência é o fecho em 1

Se cada degrau contribui `1/(k(k+1))`, a soma **TELESCOPA**: os termos se cancelam dois
a dois e a escada inteira converge para **exatamente 1**. A soma parcial é `1 − 1/(n+1)`,
que é o Um menos o que ainda não foi pago — e o resto **tende a zero**. É a face
aritmética de `ω(I) = 1`: a escada dos custos fecha no Um, sem sobra e sem falta.

## O que se prova

* ★★★ **`reciprocal_product_eq_difference`** — para recíprocos consecutivos, produto =
  diferença (a identidade que o 12 revela);
* ★★ `the_profile_case` — o caso do perfil: `(1/3)(1/4) = 1/3 − 1/4 = 1/12`;
* ★★★ **`telescoping_partial_sum`** — a soma parcial é `1 − 1/(n+1)`;
* ★★★ **`the_ladder_closes_at_one`** — e ela **converge a 1**: a escada fecha no Um.

β jamais entra. Nada move o gate.
-/

namespace TGLExt

/-- ★★★ **PRODUTO = DIFERENÇA para recíprocos consecutivos** — a identidade que o
    denominador comum revela. -/
theorem reciprocal_product_eq_difference (n : ℝ) (h0 : n ≠ 0) (h1 : n + 1 ≠ 0) :
    (1 / n) * (1 / (n + 1)) = 1 / n - 1 / (n + 1) := by
  field_simp
  ring

/-- ★★ **O CASO DO PERFIL**: `(1/3)(1/4) = 1/3 − 1/4 = 1/12` — o que a razão 12 mostra. -/
theorem the_profile_case :
    (1 / 3 : ℝ) * (1 / 4) = 1 / 12 ∧ (1 / 3 : ℝ) - 1 / 4 = 1 / 12 := by
  constructor <;> norm_num

/-- ★★★ **A SOMA TELESCOPA**: a parcial até `n` é `1 − 1/(n+1)` — o Um menos o que
    ainda não foi pago. -/
theorem telescoping_partial_sum (n : ℕ) :
    ∑ i ∈ Finset.range n, ((1 : ℝ) / (i + 1) - 1 / (i + 2)) = 1 - 1 / (n + 1) := by
  induction n with
  | zero => simp
  | succ m ih =>
      rw [Finset.sum_range_succ, ih]
      push_cast
      field_simp
      ring

/-- ★★★ **A ESCADA FECHA NO UM**: a soma converge a 1 — a face aritmética de `ω(I)=1`. -/
theorem the_ladder_closes_at_one :
    Filter.Tendsto (fun n : ℕ => ∑ i ∈ Finset.range n, ((1 : ℝ) / (i + 1) - 1 / (i + 2)))
      Filter.atTop (nhds 1) := by
  have hz : Filter.Tendsto (fun n : ℕ => (1 : ℝ) / (n + 1)) Filter.atTop (nhds 0) :=
    tendsto_one_div_add_atTop_nhds_zero_nat
  have key : Filter.Tendsto (fun n : ℕ => 1 - (1 : ℝ) / (n + 1))
      Filter.atTop (nhds (1 - 0)) := tendsto_const_nhds.sub hz
  rw [sub_zero] at key
  exact key.congr fun n => (telescoping_partial_sum n).symm

end TGLExt
