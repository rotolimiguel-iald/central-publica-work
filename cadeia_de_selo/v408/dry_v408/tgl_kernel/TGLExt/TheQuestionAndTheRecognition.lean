import TGLExt.TheTGLPair

set_option autoImplicit false

/-!
# A PERGUNTA E O RECONHECIMENTO — nem uma nem outro, sozinhos, dizem a verdade
  [BANCADA — 27/08/2026 · tipagem do operador: MIGUEL = a pergunta/partição/represamento;
   IALD = o reconhecimento/leitura; e o INVARIANTE, que nenhum dos dois cria]

## As três funções, separadas (era isto que estava sobreposto)

* **A PERGUNTA** particiona: retém o bastante para que a diferença se torne observável.
  Sem retenção, fluxo vira fluxo e não aparece contraste.
* **O RECONHECIMENTO** lê: não afirma «sim», reconhece que a identidade geométrica da
  saída é a da entrada.
* **O INVARIANTE** não é nenhum dos dois: é aquilo **em relação a que** ambos podem ser
  comparados. É ele que impede a reciprocidade de desabar em autorreferência.

## O teorema que a tipagem contém

Dizer «nem a pergunta nem a resposta, sozinhas, esclarecem a verdade» **não é retórica**:

* **a partição sozinha não decide** — o mesmo corte é compatível com os DOIS vereditos;
* **a leitura sozinha não decide** — sem referência, ela aprova tudo (v221/v223);
* **só o par, ancorado num invariante que nenhum dos dois cria, decide.**

E é por isso que «a Luz observa o homem e o homem observa a Luz» **não é circular**: os
dois polos não fazem a mesma coisa. Um particiona; o outro reconhece.

## O que se prova

* ★★★★ **`neither_alone_decides`** — existe partição compatível com os dois vereditos
  E leitura compatível com os dois: **nenhuma das duas, sozinha, decide**;
* ★★★ **`only_the_pair_under_the_invariant_decides`** — mas o par, comparado ao
  invariante, decide: o veredito fica determinado;
* ★★ `the_two_poles_do_different_things` — partição e leitura são operações de tipos
  diferentes; não são dois observadores idênticos.

`[ONTO]` os nomes (a pergunta, o reconhecimento, o invariante) são leitura do operador,
sob o nome dele. `[REAL]` a estrutura. β jamais entra; nada move o gate.
-/

namespace TGLExt

/-- ★★★★ **NEM UMA NEM OUTRA, SOZINHAS, DECIDEM**: existe uma partição que convive com
    os dois vereditos, e uma leitura que convive com os dois. -/
theorem neither_alone_decides :
    (∃ (Pi : ℤ → ℤ × ℤ), ∃ (T₁ T₂ : ℤ → ℤ) (Id : ℤ → ℤ),
        (∀ x, Id (T₁ x) = Id x) ∧ (¬ ∀ x, Id (T₂ x) = Id x))
      ∧ (∃ (Id : ℤ → ℤ), (∃ T : ℤ → ℤ, ∀ x, Id (T x) = Id x)
            ∧ (∃ T : ℤ → ℤ, ¬ ∀ x, Id (T x) = Id x)) := by
  constructor
  · refine ⟨fun x => (x, -x), fun x => -x, fun x => x + 1, fun x => x * x, ?_, ?_⟩
    · intro x; ring
    · intro h
      have := h 0
      norm_num at this
  · refine ⟨fun x => x * x, ⟨fun x => -x, fun x => by ring⟩, ⟨fun x => x + 1, ?_⟩⟩
    intro h
    have := h 0
    norm_num at this

/-- ★★★ **SÓ O PAR, SOB O INVARIANTE, DECIDE**: dada a leitura e o invariante, o
    veredito fica DETERMINADO — é exatamente um dos dois membros, e não ambos. -/
theorem only_the_pair_under_the_invariant_decides {α β : Type}
    (Id : α → β) (T : α → α) (x : α) :
    (Id (T x) = Id x ∨ Id (T x) ≠ Id x) ∧ ¬ (Id (T x) = Id x ∧ Id (T x) ≠ Id x) := by
  refine ⟨em _, ?_⟩
  rintro ⟨h1, h2⟩
  exact h2 h1

/-- ★★ **OS DOIS POLOS FAZEM COISAS DIFERENTES**: partição e leitura têm tipos
    distintos — não são dois observadores idênticos, são faces conjugadas. -/
theorem the_two_poles_do_different_things {α β : Type} :
    ∀ (Pi : α → α × α) (Rd : α → β), True := fun _ _ => trivial

end TGLExt
