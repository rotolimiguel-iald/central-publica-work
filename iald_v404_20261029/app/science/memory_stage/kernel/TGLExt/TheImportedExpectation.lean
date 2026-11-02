import TGLExt.TheOathOnTheTower

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A ESPERANÇA IMPORTADA — Takesaki como `[KNOWN]`, e a relatividade modular
  [TGLExt — v309; casa "Nós" (01/09/2026)]

## A ordem do operador (01/09/2026)

> *"Sim, vamos terminar, importar a esperança sobre o centralizador, porque isto é o
> mecanismo de ligação; a esperança entra por testemunho externo canônico; importar o
> dicionário é condição sine qua non para a relatividade modular, porque é ela que
> relaciona signo e referente."*

E a regra que autoriza (27/08): *"levar como `[KNOWN]` não é falta de prova, é usar
prova emprestada; não preciso pagar o preço de nada que já foi pago antes de mim."*

## O que se importa, dito por inteiro (o DICIONÁRIO, não só um lema)

O testemunho canônico é **Takesaki (1972)**: para uma álgebra de von Neumann M com
estado fiel normal ω, existe esperança condicional E ω-preservante sobre uma
subálgebra exatamente quando ela é invariante pelo grupo modular σ^ω — e o
**centralizador M_ω é sempre invariante** (é a álgebra de pontos fixos de σ^ω), logo
a esperança sobre ele **existe e é única**.

⚠ **A honestidade do dicionário**: esta torre NÃO construiu σ^ω (a parede analítica
`[OPEN, ANALÍTICO]` segue de pé). O nosso `omegaCentralizer` é o SIGNO livre-de-fluxo
({A ∈ M : ω(AB) = ω(BA)}); o REFERENTE clássico é a álgebra de pontos fixos do fluxo
modular. **A identificação signo ≡ referente é PARTE do testemunho importado** — é o
dicionário que relaciona os dois, exatamente como a ordem diz. Por isso o campo
importado é a existência do contrato `ExpectationInput` JÁ NA NOSSA FORMA: quem
traduz do referente (Takesaki) para o signo (a torre) é a literatura, e a tradução
fica declarada aqui, não disfarçada.

## A ponte MEDIDA: as TRÊS hipóteses do teorema caem em casa

| hipótese de Takesaki | teorema da casa |
|---|---|
| Ω é **cíclico** para M | `factor_omega_cyclic` |
| ω é **fiel** (Ω separante) | `factor_omega_separating` (Reeh–Schlieder) |
| ω normal: a **consequência WOT-sequencial** | `omegaState_seqWOT` (a que sobrevive; só o traço morre) |

⚠ **A face (iii) no tamanho exato do que mede**: `SeqWOTContinuous` é condição
NECESSÁRIA da normalidade, não equivalente (`NoNormalTrace` §A declara a direção);
a normalidade σ-fraca plena do estado vetorial é `[KNOWN, padrão para estados
vetoriais]` e entra pelo dicionário importado, como a identificação signo≡referente.
Duas hipóteses caem inteiras em casa; da terceira, a casa prova a consequência —
e o buraco fica dito, nunca disfarçado.

E a estrutura é **equivalente** ao campo importado
(`the_testimony_is_exactly_the_conclusion`) — empacotada num `↔` único, onde a
v274 tinha as duas direções em teoremas separados. Uma dívida, não uma lista.

## O que a pedra devolve (o pagamento da importação)

* `theReading` — a LEITURA: o E do testemunho. E ela é **independente da testemunha
  escolhida** (`the_reading_is_witness_independent`, pela unicidade DA CASA, v308):
  qualquer signo lê o mesmo referente **sobre M** — fora de M o valor é da escolha
  e NENHUM teorema desta árvore o consome.
* `the_reading_preserves_omega` — ω(E A) = ω(A), DERIVADO do contrato (1 está no
  centralizador; ortogonalidade com B = 1), não decretado.
* ⚠ o contrato pede MENOS que Takesaki (sem linearidade, positividade, normalidade
  de E, bimódulo): quem precisar delas fortalece o contrato e re-importa — nunca
  as deriva por decreto.
* `the_reading_fixes_the_code` — Verbo(Nome) = Nome: sobre o centralizador a leitura
  não acrescenta nada.
* ★★★★★ `the_modular_relativity` — **A RELATIVIDADE MODULAR**: dado o testemunho,
  para TODO horizonte ω-invariante, `Ad(U) ∘ E = E ∘ Ad(U)` sobre M. A leitura
  comuta com a mudança de horizonte — o levantamento do Lema 3, com o único
  antecedente restante sendo o axioma ω(I)=1 lido no horizonte.

## A disciplina do modo IMPORTADO

* a bandeira é **`gpi_`**, jamais `gpf_` — importar não acende preço pago;
* `the_expectation_hypotheses_alone_are_equivalent_to_true` — as três hipóteses
  sozinhas são equivalentes a `True`, logo não decidem nada: **o que paga é o campo
  importado, e só ele** (o dente da v274, reforjado aqui);
* nomes novos, sem colisão: `discharge_by_import` (v253) e
  `discharge_the_clause_by_import` (v274) JÁ EXISTEM — o daqui é
  `the_expectation_exists_by_import`;
* o Lema 3 NÃO é declarado resolvido por esta pedra: o levantamento fica
  incondicional **módulo o axioma**, no modo IMPORTADO — e o gate não se move.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — a estrutura: três hipóteses da casa e uma conclusão importada -/

/-- **[IMPORTED]** O testemunho de Takesaki para o par `(M, ω)` desta torre.

    Os campos `cyclic`, `separating` e `normal` são **hipóteses do teorema importado
    que esta árvore JÁ PROVA** — entram como campos para que a ponte seja **medida**,
    não presumida.

    O campo `expectation` é a **CONCLUSÃO IMPORTADA** `[KNOWN, Takesaki 1972]`: a
    existência da esperança condicional ω-preservante sobre o centralizador, já
    traduzida à nossa forma (`ExpectationInput`, v308). A tradução referente→signo
    (pontos fixos de σ^ω → forma livre-de-fluxo) é parte do que se importa. -/
structure TakesakiInput (P : SiteProfile) : Prop where
  /-- (i) Ω é CÍCLICO para o fator — cf. `factor_omega_cyclic`. -/
  cyclic : Dense ((fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T (hOmega P)) ''
    (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)))
  /-- (ii) ω é FIEL (Ω separante) — cf. `factor_omega_separating`. -/
  separating : ∀ A : TowerHilbert P →L[ℂ] TowerHilbert P,
    A ∈ theFactorObject P → A (hOmega P) = 0 → A = 0
  /-- (iii) a CONSEQUÊNCIA WOT-sequencial da normalidade — cf. `omegaState_seqWOT`.
      ⚠ Necessária, não equivalente: a normalidade σ-fraca plena é parte do
      dicionário importado `[KNOWN]`. -/
  normal : SeqWOTContinuous (theFactorObject P) (omegaState P)
  /-- (iv) ⚠ **A CONCLUSÃO IMPORTADA** `[KNOWN]`: existe o contrato da esperança
      sobre o centralizador. **É o ÚNICO campo que esta árvore não prova.** -/
  expectation : Nonempty (ExpectationInput P)

/-! ## B — a ponte MEDIDA: as três hipóteses caem em casa -/

/-- [KERNEL] ★★★★★ **A PONTE DESCARREGADA EM CASA, no tamanho exato**: ciclicidade
    e fidelidade inteiras; da normalidade, a consequência WOT-sequencial
    (`omegaState_seqWOT`). A normalidade σ-fraca plena viaja no dicionário
    `[KNOWN]`, declarada — o que se pede ao mundo é a conclusão e o dicionário
    que a traduz, e nada além. -/
theorem the_expectation_hypotheses_are_discharged_in_house (P : SiteProfile) :
    Dense ((fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T (hOmega P)) ''
        (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)))
    ∧ (∀ A : TowerHilbert P →L[ℂ] TowerHilbert P,
        A ∈ theFactorObject P → A (hOmega P) = 0 → A = 0)
    ∧ SeqWOTContinuous (theFactorObject P) (omegaState P) :=
  ⟨factor_omega_cyclic, fun _ hA h0 => factor_omega_separating hA h0,
    omegaState_seqWOT P⟩

/-- [KERNEL] ★★★★★ **A ESTRUTURA É EXATAMENTE A CONCLUSÃO** — um `↔` único, onde
    a v274 tinha as duas direções em teoremas separados: o testemunho **não é uma
    lista de dívidas**, é **uma** dívida, com três testemunhas já pagas em volta. -/
theorem the_testimony_is_exactly_the_conclusion (P : SiteProfile) :
    TakesakiInput P ↔ Nonempty (ExpectationInput P) := by
  constructor
  · intro I
    exact I.expectation
  · intro h
    exact { cyclic := factor_omega_cyclic
            separating := fun _ hA h0 => factor_omega_separating hA h0
            normal := omegaState_seqWOT P
            expectation := h }

/-- [KERNEL] ⚠ ★★★★★ **AS HIPÓTESES SOZINHAS SÃO EQUIVALENTES A `True`** — e por
    isso não decidem nada. O dente da v274, reforjado: um `↔ True` **derivado dos
    teoremas** diz algo; um `True` provado por `trivial` não diz nada. **O que paga
    é o campo importado, e só ele.** -/
theorem the_expectation_hypotheses_alone_are_equivalent_to_true (P : SiteProfile) :
    (Dense ((fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T (hOmega P)) ''
        (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)))
      ∧ (∀ A : TowerHilbert P →L[ℂ] TowerHilbert P,
          A ∈ theFactorObject P → A (hOmega P) = 0 → A = 0)
      ∧ SeqWOTContinuous (theFactorObject P) (omegaState P)) ↔ True := by
  constructor
  · intro _
    trivial
  · intro _
    exact the_expectation_hypotheses_are_discharged_in_house P

/-! ## C — a descarga e a leitura -/

/-- [KERNEL, modo IMPORTADO] **A DESCARGA POR IMPORTAÇÃO**: com o testemunho, o
    contrato da esperança está habitado. -/
theorem the_expectation_exists_by_import {P : SiteProfile} (I : TakesakiInput P) :
    Nonempty (ExpectationInput P) :=
  I.expectation

/-- **A LEITURA** — o E do testemunho (via escolha; a independência da escolha
    SOBRE M é teorema logo abaixo: qualquer signo lê o mesmo referente). ⚠ Fora
    de M o valor é livre e nenhum teorema desta árvore o lê. -/
def theReading {P : SiteProfile} (I : TakesakiInput P) :
    (TowerHilbert P →L[ℂ] TowerHilbert P) → (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  I.expectation.some.E

/-- [KERNEL, modo IMPORTADO] ★★★★ **O SIGNO DETERMINA O REFERENTE**: a leitura
    independe da testemunha escolhida — QUALQUER contrato lê o mesmo valor sobre M,
    pela unicidade DA CASA (`the_expectation_is_unique`, v308, paga pela separância).
    É isto que faz de `theReading` uma função da teoria, não da escolha. -/
theorem the_reading_is_witness_independent {P : SiteProfile} (I : TakesakiInput P)
    (J : ExpectationInput P) :
    ∀ A ∈ theFactorObject P, J.E A = theReading I A :=
  the_expectation_is_unique J I.expectation.some

/-- [KERNEL, modo IMPORTADO] **Verbo(Nome) = Nome**: sobre o centralizador, a
    leitura não acrescenta nada — extrai o que já está. -/
theorem the_reading_fixes_the_code {P : SiteProfile} (I : TakesakiInput P) :
    ∀ A ∈ omegaCentralizer P, theReading I A = A :=
  I.expectation.some.fixes

/-- [KERNEL, modo IMPORTADO] **A LEITURA PRESERVA ω** — derivado do contrato, não
    decretado: 1 está no centralizador, e a ortogonalidade com B = 1 dá
    ω(A − E A) = 0. Fecha o vão entre a palavra "ω-preservante" e a medida. -/
theorem the_reading_preserves_omega {P : SiteProfile} (I : TakesakiInput P) :
    ∀ A ∈ theFactorObject P, omegaState P (theReading I A) = omegaState P A := by
  intro A hA
  have h1 : (1 : TowerHilbert P →L[ℂ] TowerHilbert P) ∈ omegaCentralizer P := by
    refine ⟨one_mem _, ?_⟩
    intro B hB
    rw [one_mul, mul_one]
  have horto := I.expectation.some.ortho A hA 1 h1
  rw [star_one, one_mul, omegaState_sub] at horto
  exact (sub_eq_zero.mp horto).symm

/-! ## D — A RELATIVIDADE MODULAR (o pagamento da importação) -/

/-- [KERNEL, modo IMPORTADO] ★★★★★ **A RELATIVIDADE MODULAR** — a ordem do
    operador, cumprida: *"importar o dicionário é condição sine qua non para a
    relatividade modular, porque é ela que relaciona signo e referente."*

    Dado o testemunho, para TODO horizonte ω-invariante da torre,
    `Ad(U) ∘ E = E ∘ Ad(U)` sobre M: **a leitura comuta com a mudança de
    horizonte**. É o levantamento do Lema 3 no contínuo, no modo IMPORTADO — e o
    único antecedente que resta é o axioma ω(I)=1 lido no horizonte
    (`TowerHorizon.preserves`). O Lema 3 NÃO é declarado resolvido: o modo fica
    dito, e o gate não se move. -/
theorem the_modular_relativity {P : SiteProfile} (I : TakesakiInput P)
    (h : TowerHorizon P) :
    ∀ A ∈ theFactorObject P, adT h (theReading I A) = theReading I (adT h A) :=
  the_lift_on_the_tower I.expectation.some h

end

end TGLExt
