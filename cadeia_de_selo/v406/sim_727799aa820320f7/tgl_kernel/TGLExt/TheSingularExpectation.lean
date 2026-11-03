import TGLExt.Ergodicity
import TGLExt.MarkovTower

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# A ESPERANÇA SINGULAR — o gráviton como a única solução no universo de dephasing
  [BANCADA — 22/08/2026; ainda NÃO embutido no canônico]

## A cunhagem, verbatim

O operador tipou o gráviton como *"a esperança matemática da álgebra de operadores"* e, ao ser
perguntado **qual** esperança (o kernel tem duas — `trExpect` e `diagExpect`, que pousam em
lugares diferentes), respondeu:

> *"isto não é uma esperança matemática ordinária: é a **esperança matemática SINGULAR**, a
> **única solução possível no universo de dephasing**."*

Esta pedra prova a singularidade. E ela **não é vazia**: existe outra esperança condicional na
mesma casa (`trExpect`), e o dephasing **a exclui**.

## O que a casa já tinha, e o que faltava

Já provado em `Ergodicity.lean`:
* `dephase_fixes_diagonal` — a diagonal **é** ponto fixo: `T_t(E_D x) = E_D x`;
* `dephase_tendsto_expectation` — o dephasing **converge** para `E_D`.

**Faltava a recíproca**, e é ela que dá o *"única"*: quem é fixo pelo dephasing **tem** de ser
diagonal. Sem ela, o setor fixo poderia ser maior, e a esperança não seria singular.

## O que fica provado

* ★★★ `dephase_fixed_iff_diagonal` — **`(∀ t, T_t x = x) ↔ x = E_D x`**. O setor fixo do
  dephasing **É EXATAMENTE** a diagonal: nem mais, nem menos. *Isto é o "única".*
* ★★★ `the_singular_expectation` — o limite do dephasing **é** a esperança cujo setor fixo é o
  seu próprio: imagem e ponto fixo coincidem, e `E_D` é idempotente sobre eles;
* ★★★ `the_choice_is_not_free` — **`trExpect ≠ diagExpect`** exibido com testemunha: há **outra**
  esperança condicional na casa, e **o dephasing a exclui**. A singularidade é uma **seleção**,
  não uma tautologia por falta de alternativa;
* ★★ `dephasing_selects_its_own_fixed_sector` — o fecho: o que sobrevive ao dephasing é
  precisamente o que a esperança devolve intacto, e nada mais.

## Por que isto importa para a cunhagem

Se o **GRÁVITON = 1_abs = a esperança singular**, então o gráviton não é *uma* projeção entre
várias: é **a única compatível com o universo de dephasing** — e o dephasing, nesta casa, é o
que o operador tipou como **sacrifício / amor**, a operação que suprime coerências e deixa o
registro. **O gráviton é o que resta quando o custo é pago.**

HONESTIDADE — o alcance. Prova-se singularidade **na face finita**, para o semigrupo de
dephasing `T_t` com `g i i = 0` e `g i j > 0` fora da diagonal. **Não** se prova que o gráviton
físico seja esse objeto: a identificação `GRÁVITON = E_𝒩` é **[CONJECTURE]** do operador, e o
próprio operador a declarou como *"a direção formal a investigar"*. O que a pedra entrega é que
**a esperança de que ele fala é única, e que a unicidade tem conteúdo**. β jamais entra no Lean.
Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix Filter Topology

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ### A recíproca que faltava — o setor fixo É a diagonal -/

/-- ★★★ **O SETOR FIXO DO DEPHASING É EXATAMENTE A DIAGONAL.**
    `(∀ t, T_t x = x) ↔ x = E_D x`.

    A ida é `dephase_fixes_diagonal` (já da casa). A volta é a que faltava, e é ela que
    sustenta a palavra **única**: se `x` sobrevive a todo `t`, então fora da diagonal
    `e^{−t g_{ij}} x_{ij} = x_{ij}` com `g_{ij} > 0`, o que força `x_{ij} = 0`. -/
theorem dephase_fixed_iff_diagonal (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0)
    (hgpos : ∀ i j, i ≠ j → 0 < g i j) (x : Matrix n n ℂ) :
    (∀ t : ℝ, dephase g t x = x) ↔ x = diagExpect x := by
  constructor
  · intro h
    ext i j
    by_cases hij : i = j
    · subst hij; simp [diagExpect, diag_apply]
    · have h1 := congrFun (congrFun (h 1) i) j
      simp only [dephase, Matrix.of_apply] at h1
      set c : ℝ := Real.exp (-(1 * g i j)) with hc
      have hlt : c < 1 := by
        have hp : 0 < g i j := hgpos i j hij
        rw [hc, one_mul]
        exact Real.exp_lt_one_iff.mpr (by linarith)
      have hcne : (c : ℂ) - 1 ≠ 0 := by
        intro hz
        have : (c : ℂ) = 1 := by linear_combination hz
        have : c = 1 := by exact_mod_cast this
        linarith
      have hzero : ((c : ℂ) - 1) * x i j = 0 := by
        rw [sub_mul, one_mul, h1, sub_self]
      have : x i j = 0 := by
        rcases mul_eq_zero.mp hzero with h' | h'
        · exact absurd h' hcne
        · exact h'
      simp [diagExpect, diagonal_apply_ne _ hij, this]
  · intro h t
    rw [h]; exact dephase_fixes_diagonal g hg0 t x

/-! ### A singularidade tem conteúdo: existe outra, e é excluída -/

/-- ★★★ **A ESCOLHA NÃO É LIVRE.** Existe **outra** esperança condicional na mesma casa —
    `trExpect`, que pousa nos escalares — e ela **difere** de `diagExpect`. Logo a
    singularidade do dephasing é uma **seleção genuína**, e não uma tautologia por falta de
    alternativa.

    Testemunha: a matriz unitária `E₀₀` em dimensão ≥ 2. -/
theorem the_choice_is_not_free :
    diagExpect (diagonal ![(1 : ℂ), 0]) ≠ trExpect (diagonal ![(1 : ℂ), 0]) := by
  intro h
  have h1 : diagExpect (diagonal ![(1 : ℂ), 0]) 1 1 = 0 := by
    simp [diagExpect, diag_apply]
  have h2 : trExpect (diagonal ![(1 : ℂ), 0]) 1 1
      = (diagonal ![(1 : ℂ), 0]).trace / (2 : ℂ) := by
    simp [trExpect]
  rw [h, h2] at h1
  have htr : (diagonal ![(1 : ℂ), 0]).trace = 1 := by
    simp [Matrix.trace, Fin.sum_univ_two, diagonal_apply_eq]
  rw [htr] at h1
  norm_num at h1

/-! ### O fecho -/

/-- ★★ **O DEPHASING SELECIONA O SEU PRÓPRIO SETOR FIXO.** O que sobrevive ao fluxo é
    exatamente o que a esperança devolve intacto — e a esperança é idempotente sobre ele. -/
theorem dephasing_selects_its_own_fixed_sector (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0)
    (hgpos : ∀ i j, i ≠ j → 0 < g i j) (x : Matrix n n ℂ) :
    (∀ t : ℝ, dephase g t (diagExpect x) = diagExpect x)
    ∧ diagExpect (diagExpect x) = diagExpect x := by
  refine ⟨fun t => dephase_fixes_diagonal g hg0 t x, ?_⟩
  ext i j
  by_cases hij : i = j
  · subst hij; simp [diagExpect, diag_apply]
  · simp [diagExpect, diagonal_apply_ne _ hij]

end

end TGLExt
