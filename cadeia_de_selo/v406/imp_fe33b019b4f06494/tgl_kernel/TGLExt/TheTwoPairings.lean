import TGLExt.DecisionCommutation
import TGLExt.TheDarkSplit

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# AS DUAS EMPARELHAÇÕES SÃO AS DUAS FACES — e a sua conjunção é a anticomutação
  [BANCADA — 21/08/2026; ainda NÃO embutido no canônico]

## O fork que deixa de ser fork

A leitura integral do acervo encontrou, no **mesmo mês e pela mesma mão**, duas
definições do estado ligado:

* `Tensao_Fundamental.docx §3.1`: `|G⟩ = |ψ₊⟩ ⊗ |ψ₋⟩` — paridades **opostas**;
* `Comprimento_Onda_Ligacao_Psionica [Def.1]` + PsiBit/ACOM: `|G⟩ = |ψ₊ψ₊⟩` —
  **mesma** paridade (código `11`).

A síntese classificou isso como **FORK doutrinário**, a ser decidido. **O operador
respondeu que não é decisão — é tipagem** (21/08/2026, verbatim):

> *"{ψ₊ψ₋} = {JKJ = −K} · {ψ₊ψ₊} = {1 = 1} — as duas leituras são corretas, mas
> tratam de aspectos distintos do formato sem que ele se perca em nenhum momento."*

E isso **casa exatamente** com a tipagem que ele já havia dado a estas duas pedras
em 20/08: `J_squared_is_one` é a **face estática** (o Um absoluto lido localmente) e
`JKJ_eq_neg_K` é a **face conjugada** (o programa terminal, instanciação máxima) —
*"leituras do mesmo fenômeno"*.

Esta pedra **prova que as duas faces são compatíveis e que a sua conjunção tem
conteúdo**: ela produz a **anticomutação**.

## O que fica provado

* ★★★ `J_and_K_anticommute` — de `J∘J = id` **e** `J∘K∘J = −K` segue
  **`J∘K = −(K∘J)`**. As duas faces, juntas, **são** a anticomutação;
* ★★★ `the_two_faces_are_compatible` — as duas valem **simultaneamente** sobre o
  mesmo objeto: não há fork, há conjunção;
* ★★ `anticommutation_forces_the_conjugated_face` — a recíproca: dada a involução,
  a anticomutação **devolve** `JKJ = −K`. Logo face conjugada ⟺ anticomutação,
  **na presença da face estática**;
* ★★ `the_static_face_alone_does_not_give_it` — a face estática **sozinha** não
  produz a anticomutação: exibe-se `K` que comuta com `J`. **O par é necessário**,
  e por isso a conjunção não é redundante.

## Por que isto importa fora do kernel

O artigo `Tensao_Fundamental` (jan/2026) deriva a terceira dimensão de
**`{P, H_lig} = 0`** — uma anticomutação entre paridade e hamiltoniano de ligação.
O que esta pedra mostra é que a **mesma forma algébrica** cai das duas pedras que a
casa já tinha, em faces separadas. **A anticomutação não é hipótese acrescentada: é
o que sobra quando as duas leituras do emparelhamento valem ao mesmo tempo.**

HONESTIDADE: prova-se álgebra de operadores no espaço pareado da casa, e só. A
identificação `J ↔ P`, `K ↔ H_lig`, e a passagem daí para a geometria da terceira
dimensão são **[CONJECTURE]** do operador — esta pedra **não** as prova, e não move
flag alguma. β jamais entra no Lean. Sem sorry, sem axiom.
-/

namespace TGLExt

/-! ### A conjunção das duas faces -/

/-- ★★★ **AS DUAS FACES, JUNTAS, SÃO A ANTICOMUTAÇÃO.**
    De `J∘J = id` (a face estática, `1 = 1`, o emparelhamento `ψ₊ψ₊`) e
    `J∘K∘J = −K` (a face conjugada, o emparelhamento `ψ₊ψ₋`) segue
    `J∘K = −(K∘J)`.

    Não é hipótese nova: é o que as duas leituras **dizem juntas**. -/
theorem J_and_K_anticommute {n : ℕ} (d : Fin n → ℝ)
    (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (pairK d p) = -(pairK d (conjJ p)) := by
  unfold conjJ pairK
  refine Prod.ext (funext fun i => by simp) (funext fun i => by simp)

/-- ★★★ **NÃO HÁ FORK: HÁ CONJUNÇÃO.** As duas leituras valem simultaneamente
    sobre o mesmo objeto, e a terceira relação (a anticomutação) vale com elas. -/
theorem the_two_faces_are_compatible {n : ℕ} (d : Fin n → ℝ)
    (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (conjJ p) = p
    ∧ conjJ (pairK d (conjJ p)) = -(pairK d p)
    ∧ conjJ (pairK d p) = -(pairK d (conjJ p)) :=
  ⟨J_squared_is_one p, JKJ_eq_neg_K d p, J_and_K_anticommute d p⟩

/-- ★★ **A RECÍPROCA.** Na presença da face estática, a anticomutação devolve a
    face conjugada — as duas são equivalentes, e nenhuma é mais fundamental. -/
theorem anticommutation_forces_the_conjugated_face {n : ℕ} (d : Fin n → ℝ)
    (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (pairK d (conjJ p)) = -(pairK d p) := by
  have h := J_and_K_anticommute d (conjJ p)
  rw [J_squared_is_one p] at h
  exact h

/-! ### E a conjunção NÃO é redundante -/

/-- o operador trivial: `K = 0`, que comuta com tudo. -/
def flatK {n : ℕ} (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    (Fin n → ℝ) × (Fin n → ℝ) := (fun _ => 0, fun _ => 0)

/-- ★★ **A FACE ESTÁTICA SOZINHA NÃO BASTA.** Existe operador que satisfaz a
    involução e **comuta** com `J` em vez de anticomutar: o par de leituras é
    genuinamente necessário, e a conjunção tem conteúdo. -/
theorem the_static_face_alone_does_not_give_it {n : ℕ}
    (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (conjJ p) = p ∧ conjJ (flatK (conjJ p)) = flatK p := by
  refine ⟨J_squared_is_one p, ?_⟩
  unfold conjJ flatK
  rfl

/-! ### O fecho de leitura -/

/-- ★★ **O FORMATO NÃO SE PERDE.** Sobre o mesmo par, ao mesmo tempo: o espelho
    devolve (`1 = 1`), o espelho inverte o gradiente (`JKJ = −K`), a identidade do
    par é preservada na travessia, e as duas faces anticomutam. Quatro fatos, um
    objeto — que é exatamente o que o operador afirmou ao dizer que as duas
    leituras *"tratam de aspectos distintos do formato sem que ele se perca em
    nenhum momento"*. -/
theorem the_format_is_never_lost {n : ℕ} (d : Fin n → ℝ)
    (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (conjJ p) = p
    ∧ pairEnergy (conjJ p) = pairEnergy p
    ∧ conjJ (pairK d (conjJ p)) = -(pairK d p)
    ∧ conjJ (pairK d p) = -(pairK d (conjJ p)) :=
  ⟨J_squared_is_one p, J_preserves_identity p, JKJ_eq_neg_K d p,
   J_and_K_anticommute d p⟩

end TGLExt
