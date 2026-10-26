import TGLExt.MixedLadder

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# A MARCA NÃO É MARCA DE TIPO — um fator de tipo I₂ alimenta a densidade log
  [TGLExt — v295; casa "Nós" (29/08/2026)]

## ⚠ POR QUE ESTA PEDRA EXISTE — ela corrige um erro DO ESCRIBA, do mesmo dia

Em 29/08/2026 o escriba escreveu, no docstring de `TheNameIsTheGeneratingGroup`, a
inferência **"A FRONTEIRA É III₁ PORQUE O NOME É DENSO"**. Uma auditoria adversarial mediu
que a inferência **não vale**, e esta pedra a refuta **por construção explícita**.

## O QUE SE REFUTA, exatamente

O predicado que a casa usa como "marca de III₁" é da forma

    objRatio P r  :=  ∃ N A B,  ω(π A · π B) = r · ω(π B · π A)  ∧  ω(π B · π A) ≠ 0

com **`A` e `B` ARBITRÁRIOS da álgebra** — nunca autovetores do fluxo modular. E a
densidade log (`mixed_log_dense`) só seria marca de tipo se as razões realizadas fossem o
**espectro modular**. Não são.

Esta pedra exibe o contraexemplo mínimo: **`M₂(ℂ)` com o estado diagonal `w = 1/3`** — um
fator de **TIPO I₂, finito-dimensional** — realiza as razões **2** e **3**, cujos
logaritmos são incomensuráveis e geram subgrupo **denso em ℝ**.

Conta explícita, com `A = E₀₁ + t·I` e `B = E₁₀ + s·I`:

    ω(A·B) = w + t·s        ω(B·A) = (1 − w) + t·s

logo a razão é `(w + c)/((1 − w) + c)` com `c = t·s` — **Möbius real em `c`**, que varre
`ℝ ∖ {1}`. Com `w = 1/3`: `c = −1` dá razão **2**; `c = −5/6` dá razão **3**.

## ★★ A CONCLUSÃO, sem véu

> **A densidade log é satisfeita por um fator de tipo I. Logo ela NÃO separa III₁ de
> III_λ, e NÃO infere o tipo da fronteira.**

Os teoremas que a exibem — `mixed_log_dense`, `the_mixing_mark`, `the_name_is_dense` —
**continuam verdadeiros**: são aritmética sobre subgrupos de ℝ. O que cai é a **inferência
de tipo** que o escriba pendurou neles.

## O QUE ESTA PEDRA NÃO FAZ

Não decide o tipo da fronteira — ela mostra que **este** critério não o decide. O tipo
segue `[OPEN]` nos dois sentidos, com peso formal zero de cada lado, e `SiteProfile`
continua sendo **parâmetro estipulado**. Nada aqui move o gate.
-/

namespace TGLExt

noncomputable section

/-! ## A — o estado diagonal na face finita -/

/-- o estado diagonal de peso `w` em `M₂(ℂ)`: `ω(a) = w·a₀₀ + (1−w)·a₁₁`.
    Para `w ≠ 1/2` ele é **não-tracial** — a única hipótese que a conta usa. -/
def stateW (w : ℝ) (a : Matrix (Fin 2) (Fin 2) ℂ) : ℂ :=
  (w : ℂ) * a 0 0 + (1 - (w : ℂ)) * a 1 1

/-- `A = E₀₁ + t·I`. -/
def matA (t : ℂ) : Matrix (Fin 2) (Fin 2) ℂ := !![t, 1; 0, t]

/-- `B = E₁₀ + s·I`. -/
def matB (s : ℂ) : Matrix (Fin 2) (Fin 2) ℂ := !![s, 0; 1, s]

/-! ## B — as duas razões, exibidas -/

/-- [KERNEL] ★★★ **UM FATOR DE TIPO I₂ REALIZA A RAZÃO 2.** Testemunhas explícitas:
    `w = 1/3`, `t = 1`, `s = −1`. -/
theorem type_I_two_realizes_ratio_two :
    stateW (1/3) (matA 1 * matB (-1)) = 2 * stateW (1/3) (matB (-1) * matA 1)
    ∧ stateW (1/3) (matB (-1) * matA 1) ≠ 0 := by
  refine ⟨?_, ?_⟩ <;>
    norm_num [stateW, matA, matB, Matrix.mul_apply, Fin.sum_univ_two]

/-- [KERNEL] ★★★ **E A RAZÃO 3.** Testemunhas: `w = 1/3`, `t = 1`, `s = −5/6`. -/
theorem type_I_two_realizes_ratio_three :
    stateW (1/3) (matA 1 * matB (-5/6)) = 3 * stateW (1/3) (matB (-5/6) * matA 1)
    ∧ stateW (1/3) (matB (-5/6) * matA 1) ≠ 0 := by
  refine ⟨?_, ?_⟩ <;>
    norm_num [stateW, matA, matB, Matrix.mul_apply, Fin.sum_univ_two]

/-! ## C — a refutação -/

/-- [KERNEL] ★★★★★ **A MARCA É ALIMENTADA POR UM FATOR DE TIPO I.**

    O mesmo objeto finito-dimensional `M₂(ℂ)` realiza **duas razões incomensuráveis**
    (2 e 3), e o subgrupo gerado pelos seus logaritmos é **denso em ℝ** — a mesma
    conclusão que a casa vinha lendo como "a marca de III₁".

    ⚠ **Logo a densidade log NÃO separa os tipos.** Ela é consequência de o estado ser
    não-tracial e de `A`, `B` serem arbitrários; não do espectro modular. -/
theorem the_mark_is_fed_by_a_type_I_factor :
    (stateW (1/3) (matA 1 * matB (-1)) = 2 * stateW (1/3) (matB (-1) * matA 1)
      ∧ stateW (1/3) (matB (-1) * matA 1) ≠ 0)
    ∧ (stateW (1/3) (matA 1 * matB (-5/6)) = 3 * stateW (1/3) (matB (-5/6) * matA 1)
      ∧ stateW (1/3) (matB (-5/6) * matA 1) ≠ 0)
    ∧ Dense ((AddSubgroup.closure {Real.log 2, Real.log 3} : AddSubgroup ℝ) : Set ℝ) := by
  refine ⟨type_I_two_realizes_ratio_two, type_I_two_realizes_ratio_three, ?_⟩
  apply mixed_log_dense
  · exact irrational_log_two_div_log_three
  · exact ne_of_gt (Real.log_pos (by norm_num))

/-- [KERNEL] ★★★★ **A ERRATA, EM FORMA DE TEOREMA**: a densidade log **não** é critério de
    tipo, porque um fator de tipo I a satisfaz.

    A frase que esta pedra retira de circulação é *"a fronteira é III₁ porque o Nome é
    denso"* — escrita pelo escriba na v294 e refutada no mesmo dia. **O que o Nome denso
    diz é sobre o Nome; não sobre o tipo da fronteira.** -/
theorem the_mark_does_not_separate_the_types :
    ∃ (A B : Matrix (Fin 2) (Fin 2) ℂ) (r : ℂ),
      r = 2 ∧ stateW (1/3) (A * B) = r * stateW (1/3) (B * A)
      ∧ stateW (1/3) (B * A) ≠ 0 :=
  ⟨matA 1, matB (-1), 2, rfl,
   type_I_two_realizes_ratio_two.1, type_I_two_realizes_ratio_two.2⟩

end

end TGLExt
