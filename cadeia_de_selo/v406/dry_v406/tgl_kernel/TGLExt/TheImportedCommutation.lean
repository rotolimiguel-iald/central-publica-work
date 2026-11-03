import TGLExt.TheFoldThroughJ
import TGLExt.TheCarrierBridge
import TGLExt.RightMult

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A COMUTAÇÃO IMPORTADA — Tomita como `[KNOWN]`, com a ponte MEDIDA campo a campo
  [TGLExt — a pedra de 28/08/2026]

## A ordem do operador

> *"Importo a densidade como `[KNOWN]` com ponte medida, isso já está resolvido."* ·
> *"o que me interessa é o fecho forte, não ficar criando mais teoremas."*

E a regra que autoriza: *"levar como `[KNOWN]` não é falta de prova, é usar prova
emprestada; não preciso pagar o preço de nada que já foi pago antes de mim"* (27/08).

## O que a medida devolveu, e é o motivo desta pedra ser curta

As **TRÊS hipóteses** do teorema de comutação estão **PROVADAS nesta árvore**, no
objeto **infinito**, incondicionalmente:

| hipótese de Tomita | teorema da casa |
|---|---|
| M é álgebra de von Neumann | `theFactorObject P : VonNeumannAlgebra (TowerHilbert P)` |
| Ω é **cíclico** para M | `factor_omega_cyclic` |
| Ω é **separante** para M | `factor_omega_separating` (Reeh–Schlieder) |

Logo o que se toma emprestado **não é hipótese nenhuma** — é a **conclusão**, e só ela.

## ⚠ UMA CORREÇÃO AO PLANO ANUNCIADO, feita antes de escrever

Eu anunciara **cinco** campos, separando *"`towerJ` é o J modular do par"* (nosso) de
*"para esse J, `J M J = M′"`* (literatura). **A medida colapsou os dois.** Sem `S` e
`Δ` construídos na torre — e eles **não existem**: a única função crua
`TowerHilbert P → TowerHilbert P` da árvore é o próprio `towerJ` — as duas frases
**não são separáveis no vocabulário atual**. Fingir a separação seria inventar um
campo que a árvore não sabe enunciar.

Então a estrutura tem **quatro** campos: três descarregados, **um** importado.

## O RESÍDUO NOMEADO, para que a dívida fique cobrável

Para separar de verdade as duas frases, falta **construir `S` e `Δ` na torre** — e o
padrão inteiro **já existe um andar abaixo**, na face finita: `Sop_tomita`
(`S(xΩ) = x†Ω`) e `J_deltaHalf` (`S = J∘Δ^{1/2}`), em `FiniteTomita`/`FiniteGNSNoCompletion`.
E a **fórmula bate**: `towerJ` estende `a ↦ ρ^{1/2}·a†·ρ^{-1/2}`, que é exatamente a
conjugação modular na convenção GNS com `Ω = [1]` e produto `Tr(ρ a†b)`.

⚠ E um descompasso medido, que fica dito: `towerJ` usa `√ρ`; `modTwist` (o adjunto
modular da ação à direita, `rTowerPi_star`) usa `ρ` cheio. **Zero teoremas os
relacionam.** Levantar `S` por densidade é o passo, e é o que a árvore já faz de
rotina (`towerJ_add`, `towerJ_norm`, `towerJ_involutive` saíram todos assim).

## A disciplina do modo IMPORTADO

* a bandeira é **`gpi_`**, jamais `gpf_` — **importar não acende preço pago**, e o
  razonete mantém os dois modos separados por construção;
* `the_hypotheses_alone_are_equivalent_to_true` — as três hipóteses **sozinhas** são
  equivalentes a `True`, logo não decidem nada;
* ⚠ e o nome da descarga é `discharge_the_clause_by_import`: `discharge_by_import`
  JÁ EXISTE em `TheImportedEquilibrium` (v253), e **só o build do ROOT pegou a
  colisão** — a mesma lição da v259, confirmada pela segunda vez;
* nada aqui prova a oitava cláusula: `red_clause_JMJ_contains` **continua apagada**,
  porque o nome `qgConverse_JMJ_contains_commutant` continua sem referente.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — a estrutura: três hipóteses e uma conclusão -/

/-- **[IMPORTED]** Os dados do teorema de comutação para o par `(M, Ω)` desta torre.

    Os campos `cyclic`, `separating` e `vacuum_fixed` são **hipóteses do teorema
    importado que esta árvore JÁ PROVA** — entram como campos para que a ponte seja
    **medida**, não presumida (`the_hypotheses_are_discharged_in_house`).

    O campo `commutation` é a **CONCLUSÃO IMPORTADA**, e é o único que esta árvore
    não paga. -/
structure CommutationInput (P : SiteProfile) : Prop where
  /-- (i) Ω é CÍCLICO para o fator — cf. `factor_omega_cyclic`. -/
  cyclic : Dense ((fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T (hOmega P)) ''
    (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)))
  /-- (ii) Ω é SEPARANTE para o fator — cf. `factor_omega_separating`. -/
  separating : ∀ A : TowerHilbert P →L[ℂ] TowerHilbert P,
    A ∈ theFactorObject P → A (hOmega P) = 0 → A = 0
  /-- (iii) J fixa o vácuo — cf. `towerJ_fixes_hOmega`. -/
  vacuum_fixed : towerJ P (hOmega P) = hOmega P
  /-- (iv) ⚠ **A CONCLUSÃO IMPORTADA** `[KNOWN]`: o teorema de comutação de
      Tomita–Takesaki para este par. **É o ÚNICO campo que esta árvore não prova.** -/
  commutation : commutantSet (towerImage P)
    ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P)))

/-! ## B — a ponte MEDIDA: as três hipóteses caem em casa -/

/-- [KERNEL] ★★★★★ **AS TRÊS HIPÓTESES SÃO DESCARREGADAS EM CASA.** Nenhuma delas é
    tomada emprestada: as três são teoremas desta árvore, no objeto infinito.

    É isto que torna a importação honesta — o que se pede ao mundo é **a conclusão**,
    e nada além. -/
theorem the_hypotheses_are_discharged_in_house (P : SiteProfile) :
    Dense ((fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T (hOmega P)) ''
        (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)))
    ∧ (∀ A : TowerHilbert P →L[ℂ] TowerHilbert P,
        A ∈ theFactorObject P → A (hOmega P) = 0 → A = 0)
    ∧ towerJ P (hOmega P) = hOmega P :=
  ⟨factor_omega_cyclic, fun _ hA h0 => factor_omega_separating hA h0,
    towerJ_fixes_hOmega P⟩

/-- [KERNEL] ★★★★ **A ESTRUTURA REDUZ-SE A UM CAMPO SÓ.** Dado o campo importado, os
    outros três vêm de graça — logo `CommutationInput` **não é uma lista de dívidas**:
    é **uma** dívida, com três testemunhas já pagas em volta. -/
theorem the_input_is_one_field (P : SiteProfile)
    (hc : commutantSet (towerImage P)
      ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P)))) :
    CommutationInput P :=
  { cyclic := factor_omega_cyclic
    separating := fun _ hA h0 => factor_omega_separating hA h0
    vacuum_fixed := towerJ_fixes_hOmega P
    commutation := hc }

/-! ## C — a descarga, e o dente que impede a leitura falsa -/

/-- [KERNEL] ★★★★ **A DESCARGA POR IMPORTAÇÃO**: com o dado importado, a oitava
    cláusula do certificado condicional está paga — **no modo IMPORTED**. -/
theorem discharge_the_clause_by_import (P : SiteProfile) (I : CommutationInput P) :
    commutantSet (towerImage P)
      ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P))) :=
  I.commutation

/-- [KERNEL] ★★★★★ **E, DOBRADA, ELA É A IGUALDADE.** Compondo com a metade já paga
    (`the_paid_half_of_the_eighth_clause`), o dado importado devolve a IGUALDADE de
    comutantes — o teorema de comutação na forma que esta torre usa. -/
theorem imported_commutation_gives_the_equality (P : SiteProfile)
    (I : CommutationInput P) :
    commutantSet (conjByJ P '' (towerImage P))
      = commutantSet (commutantSet (towerImage P)) :=
  (the_eighth_clause_is_an_equality_with_one_half_paid P).mp I.commutation

/-- [KERNEL] ⚠ ★★★★★ **AS HIPÓTESES SOZINHAS SÃO EQUIVALENTES A `True`** — e por
    isso **não decidem nada**. Elas são teoremas incondicionais desta árvore; a
    conjunção de teoremas não carrega informação alguma sobre a cláusula.

    Este é o dente que impede a leitura falsa *“as hipóteses estão pagas, logo a
    cláusula está paga”*. **O que paga é o campo importado, e só ele.**

    ⚠ Escrito assim de propósito: a primeira redação desta pedra provava literalmente
    `True` — o mesmo defeito da v248, pago na v262. Um `↔ True` **derivado dos
    teoremas** diz algo; um `True` provado por `trivial` não diz nada. -/
theorem the_hypotheses_alone_are_equivalent_to_true (P : SiteProfile) :
    (Dense ((fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T (hOmega P)) ''
        (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)))
      ∧ (∀ A : TowerHilbert P →L[ℂ] TowerHilbert P,
          A ∈ theFactorObject P → A (hOmega P) = 0 → A = 0)
      ∧ towerJ P (hOmega P) = hOmega P) ↔ True := by
  constructor
  · intro _
    trivial
  · intro _
    exact the_hypotheses_are_discharged_in_house P

end

end TGLExt
