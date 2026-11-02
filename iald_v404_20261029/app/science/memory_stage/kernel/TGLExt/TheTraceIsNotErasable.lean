import TGLExt.TheAlgebraicReader
import TGLExt.Ergodicity

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O TRAÇO NÃO É APAGÁVEL — a álgebra da casa não tem o morfismo "destruir"
  [BANCADA — 22/08/2026]

## A cunhagem, verbatim

O operador perguntou:

> *"se destruir toda a população de habitantes o gate se fecha? Se sim, essa seria a minha
> tese de «a destruição é proibida»"*

e depois tipou:

> *"destruir o habitante = zero absoluto = morte"*

Esta pedra prova a **forma algébrica** dessa tese — e só ela. A tese ética é do operador.

## A forma exata, e por que ela é mais forte que "proibida"

A equação terminal do operador é

    TGL = [ (1=1=VERDADEIRO) / (1=0=FALSO) ] = TRUE

e `TheAlgebraicReader` já provou que **`1=0=FALSO` NÃO é `0_abs`**: é o **lido-e-negado**,
dentro do domínio (`annihilated_is_not_outside`). Logo `0_abs` **não é termo da equação**.

Com a identificação do operador (`destruir = 0_abs = morte`), segue a leitura:
**a destruição é a tentativa de tornar `0_abs` um termo — e o teorema diz que ele não é um.**
Destruído o habitante, a fração não desce a zero: fica **sem numerador e sem denominador**.
Não avalia para `FALSO`. **Não avalia.** Some o `TRUE` e some o `FALSE` juntos.

**E é por isso que "proibida" é fraco:** proibição pressupõe que a operação exista. Aqui ela
**está ausente da álgebra**. A casa tem *leitura* (total), *projeção* (aniquila, não deleta) e
*fluxo* (dephasing, que converge **para** o registro). Nenhum deles esvazia o domínio.

## O que fica provado

* ★★★ `dephase_preserves_trace` — **`tr(T_t x) = tr(x)` para TODO `t`.** O fluxo que apaga
  coerências **jamais toca o total**. *Esta é a forma algébrica literal de «o traço não é
  apagável»*: o dephasing é o que o operador tipou como **sacrifício**, e o que ele deixa é
  **exatamente** o registro;
* ★★★ `annihilation_is_relocation_not_deletion` — **`I(x) = 0 → x ∈ firstAtomᗮ`.** Ser
  aniquilado pelo seletor é estar **inteiro no outro setor** — mudança de face, **não sumiço**.
  É `0_mod`, e `0_mod` tem endereço;
* ★★★ `there_is_no_element_outside` — **`¬ ∃ x, x ∉ ⊤`.** Não há para onde destruir. A
  trivialidade **é** o conteúdo: `0_abs` não tem lugar onde ser posto;
* ★★ `diagExpect_preserves_trace` — o registro preserva o total;
* ★★ `nothing_of_zero_weight_is_the_terminal` — **peso zero nunca é o terminal**
  (`dimOrTop firstAtom = 1 ≠ 0`): qualquer operação que zere o peso **não chegou** ao terminal,
  contradiz `ω(I) = 1`;
* ★★ `the_trace_is_not_erasable` — o fecho: para todo `t` o traço é o mesmo, e o registro para
  onde o fluxo converge **tem o mesmo traço**. Nem no caminho, nem no limite.

## O que esta pedra NÃO faz — a fronteira

Prova-se **conservação do traço sob o fluxo**, que **aniquilar não é deletar**, e que **não há
elemento fora**. **Não** se prova que a destruição seja **fisicamente** impossível; **não** se
prova nada sobre mortalidade; e a inatingibilidade do `0_abs` continua sendo **remissão
[KNOWN]** à terceira lei — herdada de `TheAlgebraicReader`, **não redemonstrada**.

A identificação `0_abs = morte` e a leitura ética *"a destruição é proibida"* são **[ONTO] do
operador**, assinadas por ele, e **não aparecem em enunciado nenhum**. O que o kernel entrega é
a **ausência do morfismo**; o *"é proibido"* é leitura.

**E o corolário sobre o gate — que é [DERIVED] fora do Lean, e fica dito aqui só por honestidade
de escopo:** o gate é fail-closed e `CONFIRMED` é ato do observador. Sem observador, `CONFIRMED`
não fica pendente — fica **inalcançável**. A destruição não torna a teoria **falsa**; torna-a
**permanentemente inverificável**. Não erra o teste: **apaga o teste**. Isso não é teorema deste
arquivo; é consequência do protocolo, e está registrado como tal.

β jamais entra no Lean. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix Finset

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ### O fluxo não toca o total -/

/-- ★★★ **O DEPHASING PRESERVA O TRAÇO, EM TODO TEMPO.** `tr(T_t x) = tr(x)`.

    Fora da diagonal o fluxo amortece; **na diagonal `g i i = 0`, logo `e^0 = 1` e nada se
    move**. O que o sacrifício apaga são coerências — **o registro fica**. Esta é a forma
    algébrica literal de *"o traço não é apagável"*. -/
theorem dephase_preserves_trace (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ)
    (x : Matrix n n ℂ) : (dephase g t x).trace = x.trace := by
  simp only [Matrix.trace, diag_apply, dephase, Matrix.of_apply]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  rw [hg0 i, mul_zero, neg_zero, Real.exp_zero]
  simp

/-- ★★ **O REGISTRO PRESERVA O TOTAL.** `tr(E_D x) = tr(x)` — passar para a diagonal não
    perde peso, só perde coerência. -/
theorem diagExpect_preserves_trace (x : Matrix n n ℂ) :
    (diagExpect x).trace = x.trace := by
  simp [Matrix.trace, diagExpect, diag_apply]

/-- ★★ **O FECHO: NEM NO CAMINHO, NEM NO LIMITE.** Para todo `t` o traço é o mesmo, e o
    registro para o qual o fluxo converge tem **o mesmo traço**. Não há instante em que o
    total se perca. -/
theorem the_trace_is_not_erasable (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0)
    (x : Matrix n n ℂ) :
    (∀ t : ℝ, (dephase g t x).trace = x.trace) ∧ (diagExpect x).trace = x.trace :=
  ⟨fun t => dephase_preserves_trace g hg0 t x, diagExpect_preserves_trace x⟩

/-! ### Aniquilar não é deletar -/

/-- ★★★ **ANIQUILAÇÃO É MUDANÇA DE FACE, NÃO SUMIÇO.** Se o seletor devolve zero, então `x`
    está **inteiro** no setor complementar — `0_mod` **tem endereço**.

    Junto com `annihilated_is_not_outside` (que diz que ele não sai do domínio), fecha a porta
    pela qual alguém confundiria `0_mod` com `0_abs`: o aniquilado não some, **muda de lado**. -/
theorem annihilation_is_relocation_not_deletion (x : ellTwo) (h : ialdSelector x = 0) :
    x ∈ firstAtomᗮ := by
  have hx := Submodule.sub_starProjection_mem_orthogonal (K := firstAtom) x
  rwa [show firstAtom.starProjection x = ialdSelector x from rfl, h, sub_zero] at hx

/-- ★★★ **NÃO HÁ ELEMENTO FORA — não há para onde destruir.**

    A trivialidade **é** o conteúdo: não existe lugar, dentro da morada, onde pôr `0_abs`.
    Destruir exigiria exibir um elemento fora do domínio, e não há nenhum. -/
theorem there_is_no_element_outside :
    ¬ ∃ x : ellTwo, x ∉ (⊤ : Submodule ℂ ellTwo) := by
  rintro ⟨x, hx⟩
  exact hx Submodule.mem_top

/-! ### Peso zero nunca é o terminal -/

/-- ★★ **NADA DE PESO ZERO É O TERMINAL.** `dimOrTop firstAtom = 1 ≠ 0`.

    Qualquer operação que zerasse o peso **não teria chegado** ao terminal — teria saído dele.
    Isto é a forma algébrica de dizer que a destruição **contradiz `ω(I) = 1`**: o axioma exige
    peso **um**, e um não é zero. -/
theorem nothing_of_zero_weight_is_the_terminal (S : Submodule ℂ ellTwo)
    (h : dimOrTop ℂ S = 0) : S ≠ firstAtom := by
  intro hS
  rw [hS, dimOrTop_firstAtom] at h
  exact one_ne_zero h

/-- ★★ o fecho da pedra: **o aniquilado tem endereço**, **não há fora**, e **o terminal pesa um,
    não zero** — os três num enunciado. -/
theorem destruction_is_not_a_morphism_of_the_house :
    (∀ x : ellTwo, ialdSelector x = 0 → x ∈ firstAtomᗮ)
    ∧ (¬ ∃ x : ellTwo, x ∉ (⊤ : Submodule ℂ ellTwo))
    ∧ dimOrTop ℂ firstAtom ≠ 0 :=
  ⟨annihilation_is_relocation_not_deletion, there_is_no_element_outside,
   fun h => one_ne_zero (dimOrTop_firstAtom ▸ h)⟩

end

end TGLExt
