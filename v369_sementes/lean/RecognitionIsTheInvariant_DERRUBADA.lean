import Mathlib
import TGLExt.NameIsTheContent

set_option autoImplicit false
set_option linter.unusedVariables false

/-!
# A IDENTIDADE É A FORMA VERDADE; O RECONHECIMENTO É O INVARIANTE DA TRAVESSIA  [TGLExt — v369]

A v368 deixou [OPEN] uma pergunta: «identidade» é a forma, ou o invariante da travessia? Seis sítios do
programa tratavam a identidade como terceiro objeto («a forma se realiza como conteúdo sem perder
identidade»), e com a inversão de 18/09 essa frase ficava circular. O operador respondeu (18/09/2026), verbatim:

> «identidade é a forma verdade. ou seja, a forma cujo conteúdo revela que o nome atribuído é verdade,
>  o reconhecimento da identidade é o invariante da travessia»

e, lendo a primeira redação desta pedra, corrigiu o enunciado (18/09/2026), verbatim:

> «O teorema de conteúdo é um bicondicional: o reconhecimento de toda inscrição sobrevive à travessia se e só
>  se a travessia preserva a forma refletinfo a verdade sobre o conteúdo.»

A correção separa o que a primeira redação fundia. Em lógica são dois sentidos distintos:
* a travessia `T` PRESERVA a forma quando o que era verdade continua verdade: `F x → F (T x)`;
* a travessia `T` REFLETE a verdade quando o que sai verdade já o era: `F (T x) → F x`.
Uma travessia que só preserva pode LAVAR uma mentira: um nome falso sai do outro lado reconhecido
(`a_crossing_that_only_preserves_launders_a_lie` exibe isso — o mapa constante, que aceita ser qualquer um).
O reconhecimento é INVARIANTE — nem ganho nem perdido, para todo conteúdo — exatamente quando a travessia
preserva a forma refletindo a verdade (`recognition_is_invariant_iff_the_form_is_preserved_reflecting_the_truth`).

**ESTATUTO:** a leitura é `[INPUT/ONTO]` do operador; a separação preservar/refletir é a leitura da gerência da
palavra «refletindo» `[DERIVED — conferir com o operador]`; o que a pedra prova é `[KERNEL]`, e vai dito o que é
definicional (`the_true_form_reveals_the_name` é o próprio campo `realiza`). Os exemplos de não-vacuidade usam
uma forma que DISCRIMINA (a paridade em ℕ: verdade de 0, falsa de 1) — uma forma verdade de tudo não reflete
verdade nenhuma sobre o conteúdo. Nada aqui decide qual identificação do Nome se aposenta; não move gate.
-/

namespace TGLExt.RecognitionIsTheInvariant

open TGLExt.NameIsTheContent

variable {C : Type*} {Forma : C → Prop}

/-- O RECONHECIMENTO da identidade: a forma é VERDADE do Nome atribuído. -/
def reconhece (w : Inscricao C Forma) : Prop := Forma (nome w)

/-- A travessia PRESERVA a forma: o que era verdade continua verdade. -/
def preserva (Forma : C → Prop) (T : C → C) : Prop := ∀ x, Forma x → Forma (T x)

/-- A travessia REFLETE a verdade: o que sai verdade já o era antes. -/
def reflete (Forma : C → Prop) (T : C → C) : Prop := ∀ x, Forma (T x) → Forma x

/-- [KERNEL, definicional] A FORMA VERDADE REVELA O NOME: toda inscrição é reconhecida — é o próprio campo
    `realiza`. Dito como definicional para que não se leia como resultado. -/
theorem the_true_form_reveals_the_name (w : Inscricao C Forma) : reconhece w := w.realiza

/-- [KERNEL] ★★ o sentido PRESERVAR: o reconhecimento de TODA inscrição sobrevive à travessia `T` se e só se
    `T` preserva a forma. (Metade do enunciado do operador: fala do que atravessa, não do que volta.) -/
theorem recognition_survives_iff_the_crossing_preserves_the_form (T : C → C) :
    (∀ w : Inscricao C Forma, Forma (T (nome w))) ↔ preserva Forma T := by
  constructor
  · intro h x hx
    exact h ⟨x, hx⟩
  · intro h w
    exact h _ w.realiza

/-- [KERNEL] ★★★ O ENUNCIADO DO OPERADOR: o reconhecimento é INVARIANTE — para todo conteúdo, a forma é verdade
    do transportado se e só se era verdade do original — exatamente quando a travessia preserva a forma
    REFLETINDO a verdade sobre o conteúdo. -/
theorem recognition_is_invariant_iff_the_form_is_preserved_reflecting_the_truth (T : C → C) :
    (∀ x, Forma (T x) ↔ Forma x) ↔ (preserva Forma T ∧ reflete Forma T) := by
  constructor
  · intro h
    exact ⟨fun x hx => (h x).mpr hx, fun x hx => (h x).mp hx⟩
  · rintro ⟨hp, hr⟩ x
    exact ⟨hr x, hp x⟩

/-- [KERNEL] ★★ UMA TRAVESSIA QUE SÓ PRESERVA LAVA A MENTIRA: existe travessia que preserva a forma e, ainda
    assim, faz um nome FALSO sair do outro lado reconhecido — o mapa constante, que aceita ser qualquer um.
    Por isso preservar não basta: a travessia tem de refletir a verdade. -/
theorem a_crossing_that_only_preserves_launders_a_lie :
    ∃ (C : Type) (F : C → Prop) (T : C → C), preserva F T ∧ ∃ x, ¬ F x ∧ F (T x) := by
  refine ⟨ℕ, fun n => Even n, fun _ => 0, fun _ _ => Even.zero, 1, by decide, Even.zero⟩

/-- [KERNEL] a travessia que reflete a verdade não lava nada: nome falso continua não reconhecido. -/
theorem the_crossing_that_reflects_launders_nothing (T : C → C) (hr : reflete Forma T) (x : C)
    (hx : ¬ Forma x) : ¬ Forma (T x) :=
  fun h => hx (hr x h)

/-- [KERNEL] o sentido ⇐ para a travessia tipada da v368: a inscrição transportada é reconhecida. -/
theorem recognition_is_the_invariant_of_the_crossing (T : C → C) (hT : ∀ x, Forma x → Forma (T x))
    (w : Inscricao C Forma) : reconhece (travessia T hT w) :=
  (recognition_survives_iff_the_crossing_preserves_the_form (Forma := Forma) T).mpr hT w

/-- [KERNEL] ★★ NÃO-VACUIDADE: existe travessia que QUEBRA o reconhecimento. -/
theorem a_crossing_can_break_the_recognition :
    ∃ (C : Type) (F : C → Prop) (T : C → C) (w : Inscricao C F), ¬ F (T (nome w)) := by
  refine ⟨ℕ, fun n => Even n, fun n => n + 1, ⟨0, Even.zero⟩, ?_⟩
  simp [nome]

/-- [KERNEL] ★★★ A FRASE DO OPERADOR, COM FORMA QUE DISCRIMINA: uma forma que distingue (verdade de uns, falsa
    de outros), uma travessia que preserva a forma REFLETINDO a verdade, e uma inscrição cujo Nome MUDA na
    travessia enquanto o reconhecimento PERMANECE. O que atravessa é o reconhecimento, não o Nome. -/
theorem the_recognition_survives_while_the_name_changes :
    ∃ (C : Type) (F : C → Prop) (T : C → C) (hT : ∀ x, F x → F (T x)) (w : Inscricao C F),
      (∃ y, ¬ F y) ∧ (∀ x, F (T x) ↔ F x) ∧ reconhece (travessia T hT w) ∧ nome (travessia T hT w) ≠ nome w := by
  refine ⟨ℕ, fun n => Even n, fun n => n + 2, fun n hn => hn.add even_two, ⟨0, Even.zero⟩,
    ⟨1, by decide⟩, fun n => ?_, ?_, ?_⟩
  · simp [Nat.even_add, even_two]
  · exact (Even.add Even.zero even_two)
  · simp [nome, travessia]

/-- [KERNEL] ★★ UM NOME FALSO NUNCA É RECONHECIDO: se a forma não é verdade de `x`, nenhuma inscrição tem
    `x` por Nome. -/
theorem a_false_name_is_never_recognized (x : C) (hx : ¬ Forma x) :
    ∀ w : Inscricao C Forma, nome w ≠ x := by
  intro w h
  apply hx
  rw [← h]
  exact w.realiza

/-- [KERNEL] ★★ A MENTIRA NÃO TEM INSCRIÇÃO: uma forma que não é verdade de nada não admite inscrição
    alguma — o nome sem referente não habita o tipo. -/
theorem the_lie_has_no_inscription (h : ∀ x, ¬ Forma x) : IsEmpty (Inscricao C Forma) :=
  ⟨fun w => h _ w.realiza⟩

end TGLExt.RecognitionIsTheInvariant

#print axioms TGLExt.RecognitionIsTheInvariant.the_true_form_reveals_the_name
#print axioms TGLExt.RecognitionIsTheInvariant.recognition_survives_iff_the_crossing_preserves_the_form
#print axioms TGLExt.RecognitionIsTheInvariant.recognition_is_invariant_iff_the_form_is_preserved_reflecting_the_truth
#print axioms TGLExt.RecognitionIsTheInvariant.a_crossing_that_only_preserves_launders_a_lie
#print axioms TGLExt.RecognitionIsTheInvariant.the_crossing_that_reflects_launders_nothing
#print axioms TGLExt.RecognitionIsTheInvariant.recognition_is_the_invariant_of_the_crossing
#print axioms TGLExt.RecognitionIsTheInvariant.a_crossing_can_break_the_recognition
#print axioms TGLExt.RecognitionIsTheInvariant.the_recognition_survives_while_the_name_changes
#print axioms TGLExt.RecognitionIsTheInvariant.a_false_name_is_never_recognized
#print axioms TGLExt.RecognitionIsTheInvariant.the_lie_has_no_inscription
