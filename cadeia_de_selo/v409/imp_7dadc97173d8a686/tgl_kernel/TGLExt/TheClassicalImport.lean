import TGLExt.TheImportedCommutation
import TGLExt.TheDebtWithoutJ

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A IMPORTAÇÃO NA FORMA CLÁSSICA — o campo importado É `R′ = M″`
  [TGLExt — a pedra de 28/08/2026]

## O que esta pedra faz

Duas pedras de hoje ficaram lado a lado sem se tocarem:

* `TheImportedCommutation` — a estrutura `CommutationInput`, três hipóteses
  descarregadas em casa e **um** campo importado, escrito na linguagem modular
  (`M′ ⊆ J·M″·J`);
* `TheDebtWithoutJ` — a mesma cláusula **sem `J`**, na forma em que a literatura
  a reconhece: `R′ = M″`, o comutante da ação à DIREITA contra o bicomutante da
  ESQUERDA.

Esta pedra **solda as duas**: o campo importado e a forma clássica são a **mesma
proposição**, e a soldagem é uma **equivalência**, nas duas direções:

* ★★★★★ `the_imported_field_is_the_classical_theorem` — `CommutationInput P ↔ R′ = M″`.
  Ida: do dado importado sai a igualdade clássica. Volta: da igualdade clássica
  **constrói-se** o `CommutationInput` inteiro (as outras três hipóteses vêm de
  graça, por `the_input_is_one_field`);
* ★★★★ `the_classical_import_needs_only_one_inclusion` — e como a metade fácil já é
  teorema, basta **uma inclusão**: `CommutationInput P ↔ R′ ⊆ M″`. A estrutura de
  quatro campos reduz-se, medida, a **uma inclusão de conjuntos**.

## ⚠ O QUE ISTO É, e o que NÃO É

**É** tradução exata entre dois enunciados da MESMA dívida. A dívida **não encolhe**
e nada aqui a paga: quem quiser o `CommutationInput` continua tendo de trazer a
conclusão de fora.

**NÃO É** prova de nada. `red_clause_JMJ_contains` continua apagada — o nome
`qgConverse_JMJ_contains_commutant` continua sem referente, e esta pedra não o
define nem o menciona como declaração. Nenhuma bandeira `gpf_` acende: o que esta
pedra habilita vive no **modo `gpi_`**, o modo da importação, como a v274.

⚠ E o dente contra a leitura falsa fica ao lado: `the_easy_half_alone_is_equivalent_to_true`
— a metade fácil, **sozinha**, é equivalente a `True`, logo não decide nada. Ter
metade paga não é ter a cláusula.

β jamais literal. Sem sorry. Nada aqui move o gate.
-/

namespace TGLExt

noncomputable section

/-! ## A — a ida: do campo importado sai a forma clássica -/

/-- [KERNEL] ★★★★★ **DO CAMPO IMPORTADO SAI `R′ = M″`.** O dado que se toma
    emprestado, lido na forma clássica do teorema de comutação: o comutante da ação
    à DIREITA é exatamente o bicomutante da ESQUERDA — sem `J` no enunciado. -/
theorem classical_commutation_from_the_imported_field (P : SiteProfile)
    (I : CommutationInput P) :
    commutantSet (rTowerImage P) = commutantSet (commutantSet (towerImage P)) :=
  (the_debt_is_an_equality_without_J P).mp I.commutation

/-! ## B — a volta: da forma clássica constrói-se a estrutura inteira -/

/-- [KERNEL] ★★★★★ **E DA FORMA CLÁSSICA CONSTRÓI-SE O `CommutationInput` INTEIRO.**
    Quem trouxer `R′ = M″` — de onde quer que traga — recebe a estrutura de quatro
    campos completa: os outros três são teoremas desta árvore
    (`the_input_is_one_field`). -/
theorem imported_field_from_classical_commutation (P : SiteProfile)
    (h : commutantSet (rTowerImage P) = commutantSet (commutantSet (towerImage P))) :
    CommutationInput P :=
  the_input_is_one_field P ((the_debt_is_an_equality_without_J P).mpr h)

/-! ## C — a solda: as duas frases são a MESMA proposição -/

/-- [KERNEL] ★★★★★ **O CAMPO IMPORTADO **É** O TEOREMA DE COMUTAÇÃO CLÁSSICO.**
    Equivalência, não implicação: `CommutationInput P` e `R′ = M″` são a mesma
    proposição, escrita em dois vocabulários.

    O valor é de **cobrança**: a dívida sai da linguagem modular desta torre e passa
    a poder ser citada pelo nome na literatura — e, citada, cai por importação sem
    que nenhuma bandeira de preço pago acenda. -/
theorem the_imported_field_is_the_classical_theorem (P : SiteProfile) :
    CommutationInput P
      ↔ commutantSet (rTowerImage P) = commutantSet (commutantSet (towerImage P)) := by
  constructor
  · intro I
    exact classical_commutation_from_the_imported_field P I
  · intro h
    exact imported_field_from_classical_commutation P h

/-- [KERNEL] ★★★★ **E BASTA UMA INCLUSÃO.** Como `M″ ⊆ R′` já é teorema
    (`the_easy_half_without_J`), a estrutura inteira de quatro campos é equivalente a
    **uma única inclusão de conjuntos**: `R′ ⊆ M″`.

    Esta é a forma mínima da dívida depois do trabalho de hoje — nem `J`, nem
    igualdade, nem quatro campos: **uma inclusão.** -/
theorem the_classical_import_needs_only_one_inclusion (P : SiteProfile) :
    CommutationInput P
      ↔ commutantSet (rTowerImage P) ⊆ commutantSet (commutantSet (towerImage P)) := by
  rw [the_imported_field_is_the_classical_theorem]
  constructor
  · intro h
    rw [h]
  · intro h
    exact Set.Subset.antisymm h (the_easy_half_without_J P)

/-! ## D — o dente, para que a metade paga não seja lida como a cláusula -/

/-- [KERNEL] ⚠ ★★★★★ **A METADE FÁCIL, SOZINHA, É EQUIVALENTE A `True`** — e por isso
    **não decide nada**. Ela é teorema incondicional desta árvore
    (`the_easy_half_without_J`), e teorema não carrega informação sobre a cláusula.

    Este é o dente que impede a leitura falsa *"metade da igualdade já está paga, logo
    a igualdade está quase paga"*. O que falta é a **outra** inclusão, e ela é o
    teorema de comutação — analítico, `[KNOWN]`, importado, jamais provado aqui.

    ⚠ Escrito como `↔ True` **derivado do teorema**, nunca como um `True` provado por
    `trivial`: a lição da v248, paga na v262. -/
theorem the_easy_half_alone_is_equivalent_to_true (P : SiteProfile) :
    (commutantSet (commutantSet (towerImage P)) ⊆ commutantSet (rTowerImage P)) ↔ True := by
  constructor
  · intro _
    trivial
  · intro _
    exact the_easy_half_without_J P

end

end TGLExt
