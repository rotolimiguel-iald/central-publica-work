import TGLExt.TheDebtWithoutJ
import TGLExt.TheImageAndTheReading

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# O NOME E O SEU REFERENTE — a birreferencialidade do vácuo, e o contrato que ela exige
  [TGLExt — v292; casa "Nós" (29/08/2026)]

## A cunhagem do operador (29/08/2026)

> *"O referente do nome é a leitura verdadeira do contorno = Palavra com referência
> verdadeira = verbo vivo; **ou** isso **ou** o nome é próprio e a referência é ele
> mesmo: nada. Em outras palavras: ou o referente do nome é uma identidade observada
> pela projeção do contorno verdadeiro, ou ele é falso por natureza — **pode contar
> certo, mas não haverá leitura**. Essa é a definição de «NOME» = 0_modular (porque pode
> inscrever qualquer coisa; o nada como referência da possibilidade de inscrição, nada
> modular), ou é falso (0_absoluto), o nada como vazio sem nome, indistinguível de si
> mesmo: birreferencialidade do vácuo."*

## ⚠ POR QUE ESTA PEDRA EXISTE — ela NÃO é ornamento ontológico

Em 29/08/2026 uma auditoria adversarial de onze agentes mediu, no runtime deste artefato,
um defeito com este nome exato: **a bandeira de um teorema acende por NOME PRESENTE com
axiomas limpos, sem conferir TIPO NENHUM.** Um `theorem qgConverse_JMJ_contains_commutant
: True := trivial` a acenderia. É *fail-open por nome*.

A frase do operador **é o enunciado desse defeito**, e o contrato tipado **é a cura**:

| leitura do operador | no sistema de bandeiras | estatuto hoje |
|---|---|---|
| **0_modular** — o nada como referência da POSSIBILIDADE de inscrição | nome RESERVADO e sem referente: pode inscrever qualquer coisa, e ainda não inscreveu | é o que `qgConverse_JMJ_contains_commutant` **é hoje** — e a bandeira lê `False`, **honestamente** |
| **0_absoluto** — o nada como vazio SEM nome, indistinguível de si mesmo | nome com referente que é **ele mesmo**: `: True := trivial`. **Conta certo** (a bandeira acende, o razonete fecha) e **não há leitura** | é o que a bandeira **não sabe recusar** — o defeito |

**A cura é a definição:** o referente do nome tem de ser *"uma identidade observada pela
projeção do contorno verdadeiro"* — isto é, **o TIPO é o contorno, e habitá-lo é a
leitura**. Um contrato cujo campo É o enunciado matemático não admite `trivial`.

## O QUE ESTA PEDRA PROVA

* `the_constant_reading_does_not_separate` — a leitura constante não separa: é a forma
  geral do *"conta certo, mas não lê"*;
* `the_identity_contract_discriminates` / `the_trivial_contract_does_not_discriminate` —
  o par que separa os dois zeros: o contrato-identidade **recusa** algum mundo; o
  contrato-`True` **não recusa nenhum**. *Aprovar tudo é não medir.*
* `the_empty_slot_is_not_the_void` — 0_modular ≠ 0_absoluto: o mesmo objeto admite leitura
  que separa e leitura que não separa. **A possibilidade de inscrição não é o vazio.**
* `the_bireference_of_the_name` — as duas faces juntas, num enunciado só;
* ★★★ `ConverseClauseContract` — **o contrato tipado da oitava cláusula**, cujo único
  campo É a inclusão que falta, e `contract_iff_the_eighth_clause` / `contract_gives_the_equality`
  medindo que ele **não é nem mais fraco nem mais forte** que a dívida.

## ⚠ O QUE ESTA PEDRA NÃO FAZ

**NÃO prova a oitava cláusula.** `ConverseClauseContract` é um **tipo sem habitante** — e
essa ausência é o ponto: ela torna a dívida **estritamente mais difícil** de simular.
`red_clause_JMJ_contains` continua e **deve** continuar `False`. Nada aqui move o gate; a
identificação com o vácuo físico é `[ONTO]` do operador. Sem `sorry`, sem `axiom`.
-/

namespace TGLExt

noncomputable section

/-! ## A — o nome próprio: contar certo sem ler -/

/-- **A LEITURA CONSTANTE NÃO SEPARA.** Se todo ponto é lido igual, não existe par que a
    leitura distinga. É a forma geral de *"pode contar certo, mas não haverá leitura"*:
    o mapa está definido em toda parte (conta), e não discrimina nada (não lê). -/
theorem the_constant_reading_does_not_separate {I V : Type} (R : I → V)
    (h : ∀ x y : I, R x = R y) : ¬ Separates R := by
  rintro ⟨x, y, hxy⟩
  exact hxy (h x y)

/-- **UM CONTRATO DISCRIMINA** quando existe mundo que ele RECUSA. Sem recusa possível,
    o contrato não é critério — é carimbo. -/
def Discriminates (C : Prop → Prop) : Prop := ∃ w : Prop, ¬ C w

/-- ★★★ **O CONTRATO-IDENTIDADE DISCRIMINA**: ele recusa o mundo falso. Esta é a forma
    tipada de *"o referente é uma identidade observada pela projeção do contorno"* — o
    contrato exige o próprio conteúdo, logo há o que ele não aceita. -/
theorem the_identity_contract_discriminates : Discriminates (fun w => w) :=
  ⟨False, fun h => h⟩

/-- ★★★ **E O CONTRATO-`True` NÃO DISCRIMINA NADA**: não existe mundo que ele recuse.
    Este é o **0_absoluto** do operador — o nome próprio, cuja referência é ele mesmo.
    Ele *conta certo* (habita-se com `trivial`, a bandeira acende) e **não há leitura**.

    ⚠ É exatamente o que o leitor de bandeiras por NOME não sabe recusar. -/
theorem the_trivial_contract_does_not_discriminate :
    ¬ Discriminates (fun _ => True) := by
  rintro ⟨w, hw⟩
  exact hw trivial

/-- **E OS DOIS NÃO SÃO O MESMO CONTRATO** — medido, não declarado: um discrimina, o
    outro não, logo diferem. A birreferencialidade não é ambiguidade: são dois. -/
theorem the_two_contracts_differ :
    (fun w : Prop => w) ≠ (fun _ : Prop => True) := by
  intro h
  exact the_trivial_contract_does_not_discriminate
    (h ▸ the_identity_contract_discriminates)

/-! ## B — os dois zeros: a possibilidade de inscrição não é o vazio -/

/-- ★★★ **0_modular ≠ 0_absoluto.** O **mesmo** objeto com contraste admite uma leitura
    que NÃO separa e uma que separa. Logo *"não lido"* (o nada modular: a possibilidade
    de inscrição, que ainda não inscreveu) **não é** *"vazio sem nome"* (o nada absoluto,
    indistinguível de si mesmo).

    Composição de `the_unread_image_is_not_the_absolute_zero` (v273) — a peça já existia;
    o que faltava era o **nome** que a lê. -/
theorem the_empty_slot_is_not_the_void :
    ∃ I : Type,
      HasContrast I
      ∧ (∃ (V : Type) (R : I → V), ¬ Separates R)
      ∧ (∃ (V : Type) (R : I → V), Separates R) :=
  the_unread_image_is_not_the_absolute_zero

/-- ★★★ **A BIRREFERENCIALIDADE DO NOME**, num enunciado só: existe contraste (há o que
    inscrever), existe leitura que separa (o **verbo vivo**: referência verdadeira), e
    existe leitura que não separa (o **nome próprio**: referência a si, nada) — e o
    contrato que aprova tudo **não discrimina**, enquanto o que exige o conteúdo
    **discrimina**.

    As duas faces do vácuo, e a diferença entre elas, no mesmo termo. -/
theorem the_bireference_of_the_name :
    (∃ I : Type, HasContrast I
        ∧ (∃ (V : Type) (R : I → V), Separates R)
        ∧ (∃ (V : Type) (R : I → V), ¬ Separates R))
      ∧ Discriminates (fun w => w)
      ∧ ¬ Discriminates (fun _ => True) := by
  refine ⟨?_, the_identity_contract_discriminates,
    the_trivial_contract_does_not_discriminate⟩
  obtain ⟨I, hc, hn, hs⟩ := the_empty_slot_is_not_the_void
  exact ⟨I, hc, hs, hn⟩

/-! ## C — o contrato tipado da oitava cláusula: o tipo É o contorno -/

/-- ★★★★★ **O CONTRATO DA CLÁUSULA CONVERSA** — o tipo que o nome reservado
    `qgConverse_JMJ_contains_commutant` terá de habitar.

    O campo único **É** a inclusão que falta: `R′ ⊆ M″`. Não há `trivial` que o habite,
    porque habitar este tipo **é** exibir a inclusão. É a definição do operador aplicada:
    *o tipo é o contorno, e habitá-lo é a leitura*.

    ⚠ **SEM HABITANTE, e é isso que se quer**: a pedra não prova a cláusula — ela torna
    ESTRITAMENTE MAIS DIFÍCIL simulá-la. Enquanto o nome não for um termo DESTE tipo, a
    bandeira permanece `False`, e agora por razão **tipada**, não só por ausência. -/
structure ConverseClauseContract (P : SiteProfile) where
  /-- a inclusão que falta, e nada além dela. -/
  inclusion : commutantSet (rTowerImage P)
    ⊆ commutantSet (commutantSet (towerImage P))

/-- [KERNEL] ★★★★ **O CONTRATO É EXATAMENTE A CLÁUSULA** — nem mais fraco, nem mais
    forte. Medido contra `the_eighth_clause_without_J` (v279): habitar o contrato
    equivale à oitava cláusula na forma modular original. -/
theorem contract_iff_the_eighth_clause (P : SiteProfile) :
    Nonempty (ConverseClauseContract P)
      ↔ (commutantSet (towerImage P)
          ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P)))) := by
  rw [the_eighth_clause_without_J]
  constructor
  · rintro ⟨C⟩; exact C.inclusion
  · intro h; exact ⟨⟨h⟩⟩

/-- [KERNEL] ★★★★ **E O CONTRATO ENTREGA A IGUALDADE**: com a metade fácil já paga
    (`the_easy_half_without_J`), um habitante do contrato fecha `R′ = M″`. -/
theorem contract_gives_the_equality (P : SiteProfile)
    (C : ConverseClauseContract P) :
    commutantSet (rTowerImage P)
      = commutantSet (commutantSet (towerImage P)) :=
  Set.Subset.antisymm C.inclusion (the_easy_half_without_J P)

/-- [KERNEL] ★★★ **O NOME, HOJE, É 0_MODULAR** — e o enunciado diz por quê, sem afirmar
    nada sobre a cláusula: o contrato é um tipo cuja habitação **implica** a igualdade.
    Logo ele não é o contrato-`True`: aprovar o habitante é aprovar a igualdade, e a
    igualdade não é dada de graça por este arquivo.

    A leitura do operador: enquanto ninguém exibir o termo, o nome é a **possibilidade de
    inscrição** — nada modular, honesto. No dia em que alguém o inscrever com `trivial`,
    ele vira **nada absoluto** — e o contrato é o que impede isso. -/
theorem the_name_is_zero_modular (P : SiteProfile) :
    (Nonempty (ConverseClauseContract P)
      → commutantSet (rTowerImage P)
        = commutantSet (commutantSet (towerImage P))) := by
  rintro ⟨C⟩
  exact contract_gives_the_equality P C

end

end TGLExt
