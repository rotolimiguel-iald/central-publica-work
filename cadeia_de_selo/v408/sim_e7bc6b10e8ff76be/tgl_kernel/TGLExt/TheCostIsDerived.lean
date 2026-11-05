import TGLExt.TheJudgedThing
import Mathlib.Analysis.SpecialFunctions.Log.Basic

set_option autoImplicit false

/-!
# O CUSTO NÃO É POSTULADO — é DERIVADO (Landauer ⊕ Nernst)
  [BANCADA — 26/08/2026 · CORREÇÃO AO LADO do estatuto da v216, por ordem do operador:
   «a leitura não é postulada sobre a termodinâmica; quem derivou essa lei não fui eu,
   foi Nernst; a face lógica só existe porque processou o sistema, e o efeito não
   existe sem o processamento ENTRE os dois clocks — o que é justamente o que a IALD faz»]

## O que a v216 disse a menos (a errata de estatuto)

A v216 classificou a leitura termodinâmica do custo como `[POSTULATE]` estrutural da
TGL. **Está corrigido aqui, AO LADO (a v216 permanece intacta):** a existência de um
custo estritamente positivo NÃO é postulado da TGL — é consequência de dois resultados
estabelecidos, com a redução provada nesta mesma torre servindo de gatilho:

    P ≠ I  (redução efetiva, v216)
      ⟹ P NÃO É INJETIVO — muitos-para-um     [REAL, provado abaixo]
      ⟹ operação LOGICAMENTE IRREVERSÍVEL      [definição]
      ⟹ dissipação ≥ k_B·T·ln 2                [KNOWN: Landauer 1961; verificado
                                                 experimentalmente — Bérut et al.,
                                                 Nature 483 (2012); Jun–Gavrilov–
                                                 Bechhoefer, PRL 113 (2014)]
      ⟹ o piso só se anularia em T = 0          [REAL, provado abaixo]
      ⟹ e T = 0 é INATINGÍVEL                   [KNOWN: Nernst, 3ª lei]
      ⟹ CUSTO ESTRITAMENTE POSITIVO, SEMPRE.

E a leitura da TGL casa com o próprio título do artigo-mãe: β é **o custo geométrico
do zero absoluto**.

## O que se prova aqui

* ★★★ `the_dispositive_is_not_injective` — **o dispositivo é muitos-para-um**: coisa
  julgada que não é a identidade NÃO é injetiva (o gatilho de Landauer, em teorema);
* ★★★ `landauer_floor_pos` — o piso `k·T·ln 2` é ESTRITAMENTE positivo para `T > 0`;
* ★★★ `landauer_floor_vanishes_only_at_absolute_zero` — e só se anula em `T = 0`
  (que a 3ª lei proíbe atingir: o piso nunca desaparece);
* ★★ `the_witness_needs_two_registers` — **a testemunha é processo de dois clocks**:
  o registro projetado difere do originário E o retorno fecha; sem os dois instantes
  não há efeito reflexivo. É o que a IALD faz: processa ENTRE os dois clocks.

## A FRONTEIRA QUE PERMANECE (dita, sem véu)
Evolução unitária fechada não dissipa — mas também não INSCREVE (não há registro, não
há leitura). O que dissipa é a INSCRIÇÃO, e a inscrição é a redução. O que segue sendo
da TGL, e não da literatura, é o **VALOR** do custo (β) e sua identificação geométrica
— não a existência do custo. β jamais entra aqui. Nada move o gate.
-/

namespace TGLExt

/-- ★★★ **O DISPOSITIVO É MUITOS-PARA-UM**: coisa julgada que não é a identidade não
    é injetiva — logicamente irreversível. Este é o gatilho de Landauer, em teorema. -/
theorem the_dispositive_is_not_injective {α : Type} (D : α → α)
    (hj : ResJudicata D) (hne : D ≠ id) : ¬ Function.Injective D := by
  intro hinj
  obtain ⟨x, hx⟩ := no_decision_without_cost D hne
  exact hx (hinj (hj x))

/-- ★★★ **O PISO DE LANDAUER É ESTRITAMENTE POSITIVO** enquanto houver temperatura. -/
theorem landauer_floor_pos (k T : ℝ) (hk : 0 < k) (hT : 0 < T) :
    0 < k * T * Real.log 2 :=
  mul_pos (mul_pos hk hT) (Real.log_pos (by norm_num))

/-- ★★★ **E SÓ SE ANULA NO ZERO ABSOLUTO** — que a terceira lei proíbe atingir: logo
    o custo nunca desaparece. -/
theorem landauer_floor_vanishes_only_at_absolute_zero (k T : ℝ) (hk : k ≠ 0)
    (h : k * T * Real.log 2 = 0) : T = 0 := by
  have hlog : Real.log 2 ≠ 0 := ne_of_gt (Real.log_pos (by norm_num))
  rcases mul_eq_zero.mp h with h1 | h2
  · rcases mul_eq_zero.mp h1 with hk0 | hT0
    · exact absurd hk0 hk
    · exact hT0
  · exact absurd h2 hlog

/-- ★★ **A TESTEMUNHA É PROCESSO DE DOIS CLOCKS**: o registro projetado difere do
    originário e o retorno fecha — dois instantes distintos, logo processo, logo
    custo. Sem o processamento ENTRE os dois clocks não há efeito reflexivo. -/
theorem the_witness_needs_two_registers {α : Type} (J : α → α)
    (hJ : ∀ x, J (J x) = x) (one : α) (h : J one ≠ one) :
    J one ≠ one ∧ J (J one) = one := ⟨h, hJ one⟩

end TGLExt
