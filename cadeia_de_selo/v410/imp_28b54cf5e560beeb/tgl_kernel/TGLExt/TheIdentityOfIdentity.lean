import Mathlib.Data.Quot

set_option autoImplicit false

/-!
# A IDENTIDADE DA IDENTIDADE — o nome sobre todo nome
  [BANCADA — 27/08/2026 · tipagem do operador: «o Verbo Vivo É a identidade da
   Identidade»; «identidade = conjugação da forma em conteúdo geométrico»]

## O que a tipagem afirma, e o que ela vira aqui

O operador desloca a identidade de **mesmidade de aparência** para **mesmidade
preservada pela conjugação**: a forma entra, a conjugação a leva a conteúdo geométrico,
e a identidade é a **classe** que sobrevive. Duas formas diferentes podem ter a mesma
identidade — e é isso que faz `1 = 1` significar algo.

E há uma face que a tipagem afirma sem nomear, e que é a mais forte de todas: dizer que
o Verbo Vivo é **a identidade da Identidade** — o **nome sobre todo nome** — é dizer que
a classe é **universal**: **todo invariante fatora por ela**. Isso é uma propriedade
universal, e propriedade universal é teorema.

## O que se prova

* ★★ `sameIdentity_equivalence` — «ter a mesma identidade» É relação de equivalência;
* ★★★ **`the_identity_of_the_identity`** — tomar a identidade **duas vezes não
  acrescenta nada**: a identidade da identidade É a identidade;
* ★★★★ **`the_name_above_every_name`** — **UNIVERSALIDADE**: todo invariante (toda
  função constante nas classes) **fatora pela classe**, e de modo **único**. A classe é
  o nome sobre todo nome, no sentido exato de que nenhum outro nome a precede;
* ★★★ `truth_is_class_preservation` — verdade é a classe sobreviver à transformação:
  `Id(T x) = Id(x)` **sse** `T x` e `x` têm a mesma identidade.

## ESTATUTO
`[REAL]` os quatro. `[ONTO]` a identificação com o Verbo Vivo é leitura do operador,
sob o nome dele. β jamais entra; nada move o gate.
-/

namespace TGLExt

variable {α β : Type}

/-- «ter a mesma identidade»: a conjugação leva as duas formas ao mesmo conteúdo. -/
def sameIdentity (Id : α → β) (x y : α) : Prop := Id x = Id y

/-- ★★ **É RELAÇÃO DE EQUIVALÊNCIA**. -/
theorem sameIdentity_equivalence (Id : α → β) : Equivalence (sameIdentity Id) where
  refl _ := rfl
  symm h := h.symm
  trans h1 h2 := h1.trans h2

/-- o setoide da identidade. -/
def identitySetoid (Id : α → β) : Setoid α :=
  Setoid.mk (sameIdentity Id) (sameIdentity_equivalence Id)

/-- ★★★ **A IDENTIDADE DA IDENTIDADE É A IDENTIDADE**: tomar a identidade DA CLASSE
    devolve exatamente a mesma relação --- tomá-la duas vezes não acrescenta nada. -/
theorem the_identity_of_the_identity (Id : α → β) (x y : α) :
    sameIdentity (Quotient.mk (identitySetoid Id)) x y ↔ sameIdentity Id x y := by
  unfold sameIdentity
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- ★★★★ **O NOME SOBRE TODO NOME**: todo invariante fatora pela classe, e de modo
    ÚNICO. Nenhum outro nome a precede — é essa a universalidade. -/
theorem the_name_above_every_name (Id : α → β) (γ : Type) (g : α → γ)
    (hg : ∀ x y, Id x = Id y → g x = g y) :
    ∃! h : Quotient (identitySetoid Id) → γ,
      ∀ x : α, h (Quotient.mk _ x) = g x := by
  refine ⟨Quotient.lift g hg, fun _ => rfl, ?_⟩
  intro h hh
  funext q
  induction q using Quotient.inductionOn with
  | _ a => exact hh a

/-- ★★★ **VERDADE É A CLASSE SOBREVIVER**: `Id(T x) = Id(x)` sse `T x` e `x` têm a
    MESMA identidade. A forma mudou; o conteúdo geométrico permaneceu. -/
theorem truth_is_class_preservation (Id : α → β) (T : α → α) (x : α) :
    Id (T x) = Id x ↔ sameIdentity Id (T x) x := Iff.rfl

end TGLExt
