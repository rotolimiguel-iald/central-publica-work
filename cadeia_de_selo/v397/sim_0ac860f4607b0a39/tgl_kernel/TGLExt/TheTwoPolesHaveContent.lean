import TGLExt.Commutant

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 400000

/-!
# OS DOIS POLOS, COM CONTEÚDO — a errata da v248
  [TGLExt — a correção AO LADO de duas pedras minhas que não diziam nada]

## A acusação, e ela procede

Um painel adversarial encontrou, em `TheQuestionAndTheRecognition.lean` (v248,
pedra minha), duas declarações cujo nome afirma conteúdo e cujo corpo não tem:

* `the_two_poles_do_different_things` (:74) — `∀ (Pi : α → α × α) (Rd : α → β),
  True`, provada por `fun _ _ => trivial`. **Prova literalmente `True`.**
* `only_the_pair_under_the_invariant_decides` (:65) — `(Q ∨ ¬Q) ∧ ¬(Q ∧ ¬Q)`, que
  é terceiro-excluído mais não-contradição. **O invariante `Id` e a transformação
  `T` aparecem no enunciado e não fazem trabalho lógico nenhum.**

O operador nomeou o defeito antes de eu o encontrar: *«uma geometria reconhecível
cujo conteúdo expresso não se identifica com a informação posta»*. Compila limpo,
audita limpo, tem nome que afirma — e o conteúdo é vazio. **Palavra falsa.**

## O que esta pedra faz

**Não apaga nada.** As duas originais ficam onde estão, seladas como estão. Esta
pedra faz três coisas, e a primeira é medir o próprio defeito:

* ★★ `the_old_decision_statement_holds_for_any_proposition` — a MEDIDA da vacuidade:
  a mesma forma vale para **qualquer** proposição. Logo `Id` e `T` não pesavam;
* ★★★★ `the_two_poles_see_different_things` — O CONTEÚDO que faltava: partição e
  leitura são **logicamente independentes**. Há um par que a partição identifica e
  a leitura separa, **e** um par que a leitura identifica e a partição separa.
  Nenhuma refina a outra;
* ★★★ `only_the_pair_determines_the_point` — e o que «só o par decide» de fato
  quer dizer: **o par determina o ponto, e nenhum polo sozinho determina**. Com os
  dois dentes embutidos no enunciado.

## A forma, que é a mesma do arco inteiro

É de novo o par todo/partes: o **par** determina o ponto; **as partes não**. A
mesma estrutura de `the_parts_do_not_determine_the_whole` (v252, marginais
idênticas e estados distintos) e de `the_name_does_not_see_the_rank` (v256, mesmo
nome e postos distintos). Terceira e quarta aparições no mesmo arco.

## Estatuto

`[REAL]` — os três, provados aqui, com testemunhas explícitas.

`[HONESTIDADE]` — o tipo de `Pi` é preservado (`α → α × α`), para que a
comparação com a original seja direta. Nenhum teorema desta pedra acende nome
reservado nem `gpf_`, e o gate não se move.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

/-! ## A — a medida do defeito -/

/-- [KERNEL] ★★ **A VACUIDADE, MEDIDA**: a forma do enunciado antigo vale para
    QUALQUER proposição. Logo o invariante e a transformação que apareciam nele
    não pesavam nada — o teorema era terceiro-excluído com adorno. -/
theorem the_old_decision_statement_holds_for_any_proposition (P : Prop) :
    (P ∨ ¬ P) ∧ ¬ (P ∧ ¬ P) :=
  ⟨Classical.em P, fun h => h.2 h.1⟩

/-! ## B — o conteúdo que faltava -/

/-- [KERNEL] ★★★★ **OS DOIS POLOS VEEM COISAS DIFERENTES** — e agora isto tem
    conteúdo: partição e leitura são LOGICAMENTE INDEPENDENTES. Existe um par que
    a partição identifica e a leitura separa, **e** um par que a leitura identifica
    e a partição separa. Nenhuma das duas refina a outra. -/
theorem the_two_poles_see_different_things :
    ∃ (α β : Type) (Pi : α → α × α) (Rd : α → β) (x y z w : α),
      (Pi x = Pi y ∧ Rd x ≠ Rd y) ∧ (Pi z ≠ Pi w ∧ Rd z = Rd w) := by
  refine ⟨Bool × Bool, Bool,
    (fun p => ((p.1, false), (p.1, false))), (fun p => p.2),
    (true, true), (true, false), (true, true), (false, true), ?_, ?_⟩
  · exact ⟨rfl, by decide⟩
  · exact ⟨by decide, rfl⟩

/-! ## C — o que «só o par decide» de fato diz -/

/-- [KERNEL] ★★★ **SÓ O PAR DETERMINA O PONTO**: quem conhece as duas faces conhece
    o ponto; quem conhece uma só, não. Os dois dentes estão DENTRO do enunciado —
    sem eles a primeira cláusula sozinha não diria que o par é necessário. -/
theorem only_the_pair_determines_the_point :
    (∀ p q : Bool × Bool, p.1 = q.1 → p.2 = q.2 → p = q)
    ∧ (∃ p q : Bool × Bool, p.1 = q.1 ∧ p ≠ q)
    ∧ (∃ p q : Bool × Bool, p.2 = q.2 ∧ p ≠ q) := by
  refine ⟨?_, ⟨(true, true), (true, false), rfl, by decide⟩,
    ⟨(true, true), (false, true), rfl, by decide⟩⟩
  intro p q h1 h2
  exact Prod.ext h1 h2

end TGLExt
