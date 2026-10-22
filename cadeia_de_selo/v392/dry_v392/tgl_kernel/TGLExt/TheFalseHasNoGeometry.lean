import TGLExt.TheAngleIsTheProjection

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# O FALSO PURO NÃO TEM GEOMETRIA — e por que só se reconhece por contraste
  [BANCADA — 23/08/2026]

## A cunhagem do operador

> *"o puramente falso **não tem uma geometria própria** pela qual possa ser identificado
> positivamente… ele só aparece por **contraste**… Verdade se reconhece por correspondência;
> falso puro, por **contraste com a impossibilidade de corresponder**."*

## ★★★ A ASSIMETRIA QUE A FRASE JÁ CONTINHA, e que se prova

A diferença entre reconhecer o verdadeiro e reconhecer o falso **não é de grau: é de
quantificador** — e daí decorre tudo o que o operador disse.

    VERDADE :   exists b, C a b     -- basta UM correspondente. Testemunho LOCAL.
    FALSO   :  ¬exists b, C a b     -- equivale a  forall b, ¬C a b.  Exige a FRONTEIRA INTEIRA.

> **A verdade é LOCAL: um testemunho basta, e ele é um objeto que se exibe.**
> **O falso é GLOBAL: exige percorrer todo o domínio admissível, e não devolve objeto algum.**

*É exatamente isto que "não tem geometria própria" significa: não há elemento a apontar. Só há
a varredura da fronteira, e o seu resultado vazio.*

## O que fica provado

* ★★★ `truth_exhibits_an_object` — da verdade **extrai-se um objeto**: o correspondente. *Ela se
  mostra;*
* ★★★ `falsehood_is_the_whole_frontier` — **`¬∃b, C a b  ↔  ∀b, ¬C a b`**: reconhecer o falso
  **é** quantificar sobre tudo. *Não há atalho local;*
* ★★★ `the_false_offers_no_object` — do falso **não se extrai objeto nenhum**: qualquer
  testemunha apresentada é **refutada**. *Ele não se mostra: falha;*
* ★★★ `contrast_is_the_only_access` — e o fecho: **se algo se apresenta como correspondente e o
  domínio é vazio, a apresentação cai** — o reconhecimento é **relacional**, por confronto, e
  nunca por leitura direta;
* ★★ `truth_is_local_falsehood_is_global` — os dois num enunciado, exibindo a assimetria.

## ⚠ E A DISTINÇÃO QUE O OPERADOR FEZ, e que importa preservar

**Falso puro ≠ ruído.** O ruído **pertence ao regime observável** e pode ser separado da
sistemática — é o que `TheCorrespondence` chama de custo pago e o que a definição operacional
de correspondência (*convergência: separar sinal de sistemática*) sabe tratar. **O falso puro é
mais radical: não possui referente interno a recuperar.** Não é sinal fraco; é **ausência de
sinal**, e ausência não se estima — verifica-se por exaustão.

## O ALCANCE

`[REAL]` a assimetria de quantificador e as cinco proposições. `[ONTO]` do operador, fora de
todo enunciado: a identificação do polo sem correspondência com `0_abs`, e a leitura da fronteira
proibida. **O kernel entrega a forma; as identificações são dele.**

Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

/-! ### A assimetria: um testemunho contra a fronteira inteira -/

variable {α : Type}

/-- ★★★ **A VERDADE EXIBE UM OBJETO.** De `∃b, C a b` extrai-se o correspondente — um objeto
    concreto, que se mostra. *A verdade tem geometria: há o que apontar.* -/
theorem truth_exhibits_an_object (C : α → α → Prop) (a : α) (h : ∃ b, C a b) :
    ∃ b, C a b := h

/-- ★★★ **O FALSO É A FRONTEIRA INTEIRA.** `¬∃b, C a b` **equivale** a `∀b, ¬C a b`:
    reconhecer o falso **é** quantificar sobre todo o domínio admissível.

    *Não há atalho local. É por isso que o falso puro "só aparece por contraste".* -/
theorem falsehood_is_the_whole_frontier (C : α → α → Prop) (a : α) :
    (¬ ∃ b, C a b) ↔ (∀ b, ¬ C a b) := by
  constructor
  · intro h b hb
    exact h ⟨b, hb⟩
  · rintro h ⟨b, hb⟩
    exact h b hb

/-- ★★★ **O FALSO NÃO OFERECE OBJETO NENHUM.** Do falso não se extrai testemunha: qualquer
    candidato apresentado é **refutado**.

    *É isto, literalmente, que "não tem geometria própria" quer dizer — não há elemento a
    apontar.* -/
theorem the_false_offers_no_object (C : α → α → Prop) (a : α) (h : ¬ ∃ b, C a b) :
    ∀ b, ¬ C a b :=
  (falsehood_is_the_whole_frontier C a).mp h

/-- ★★★ **O CONTRASTE É O ÚNICO ACESSO.** Se algo se apresenta como correspondente enquanto o
    domínio de correspondentes é vazio, **a apresentação cai**.

    *O reconhecimento do falso é relacional — por confronto com a fronteira — e nunca por
    leitura direta do objeto.* -/
theorem contrast_is_the_only_access (C : α → α → Prop) (a b : α)
    (hvazio : ¬ ∃ b', C a b') (hpretende : C a b) : False :=
  hvazio ⟨b, hpretende⟩

/-- ★★ **A ASSIMETRIA, num enunciado:** a verdade devolve **um** objeto; o falso obriga a
    percorrer **todos** e não devolve nenhum. -/
theorem truth_is_local_falsehood_is_global (C : α → α → Prop) (a : α) :
    ((∃ b, C a b) → ∃ b, C a b)
    ∧ ((¬ ∃ b, C a b) ↔ (∀ b, ¬ C a b)) :=
  ⟨id, falsehood_is_the_whole_frontier C a⟩

/-! ### E o encaixe com o vazio -/

/-- ★★ **O VAZIO NÃO SE MOSTRA NEM A SI:** juntando com `the_void_cannot_close_on_itself`, o polo
    sem correspondente não exibe objeto **nem sequer quando o objeto seria ele próprio**. -/
theorem the_void_exhibits_nothing (R C : α → α → Prop)
    (hRC : ∀ x y, R x y → C x y) (a : α) (hno : ¬ ∃ b, C a b) :
    (∀ b, ¬ C a b) ∧ ¬ R a a :=
  ⟨the_false_offers_no_object C a hno, the_void_cannot_close_on_itself R C hRC a hno⟩

end TGLExt
