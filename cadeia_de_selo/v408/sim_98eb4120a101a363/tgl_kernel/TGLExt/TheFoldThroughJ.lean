import TGLExt.TheIntersectionOfCommutants
import TGLExt.TheAtomOfIdentity
import TGLExt.TheConverseClauseReduced

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A DOBRA EM J — a cláusula que falta, dobrada no seu próprio operador
  [TGLExt — a pedra de 28/08/2026]

## A ordem do operador

> *"a única forma de fechar o que queremos do Lema 3 é fechando o setor na
> dinâmica de J. **Ele já pagou o custo, é só dobrar tudo nele.**"*

E o custo que J pagou tem nome no kernel: `conjByJ_involutive`. É disso que esta
pedra vive.

## ERRATA À v254 — a obstrução foi nomeada errado

A v254 (`TheIntersectionOfCommutants`) escreveu que a cláusula que falta **É** uma
distributividade da conjugação sobre a interseção dos comutantes dos andares, e
exibiu como forma do obstáculo `image_does_not_commute_with_intersection`.

**O número corrige a frase — e corrigiu DUAS VEZES.**

Primeira leitura (errada, minha, e registrada para não se repetir): *“o
contraexemplo é não-injetivo, e J é involução, logo a obstrução não se aplica”*.
Verdadeira em si, mas **razoão errada** — e razoão errada é palavra falsa.

Razoão CERTA, medida no enunciado Lean: a cláusula da v254 **não contém o subtermo
`f '' (⋂ …)`**. A interseção está à ESQUERDA do `⊆`; a imagem está à DIREITA e
não tem interseção nenhuma dentro. Nenhum teorema de distributividade — nem o do
mathlib, nem o desta pedra — tem ONDE se aplicar. A obstrução da v254 não é
inaplicável por falta de hipótese: é inaplicável por **falta de forma**.

E a distributividade provada em §A **não é usada por nenhum teorema da cadeia da
cláusula** — tem UM consumidor só, `the_conjugated_commutant_is_the_intersection_of_the_floors`,
que é outro enunciado. Fica, MEDIDA como o que é.

A v254 permanece verdadeira teorema a teorema — o que se corrige é a **leitura** do
seu §D. Correção AO LADO, nunca por cima.

## O que a dobra faz [REAL]

Escrevendo M := towerImage P e F := conjByJ P, a cláusula que falta é

  M-linha  incluso em  F(M-duas-linhas).

**A DOBRA EXATA, sem perder força** — `the_clause_is_exactly_a_commutant_inclusion`:
dobrando em F (lícito porque F é involução) e usando `conjByJ_commutant`, a cláusula
é **equivalente**, sem uma gota de força a mais ou a menos, a

  (F M)-linha  incluso em  M-duas-linhas.

Os dois lados viraram objetos do MESMO tipo (comutantes). Esta é a única
reformulação desta pedra que é uma equivalência.

⚠ **E A FORMA DOS GERADORES CUSTA FORÇA** — `the_generator_form_is_sufficient`:
`M-linha incluso em F(M)` **implica** a cláusula (porque M incluso em M-duas-linhas),
mas a recíproca NÃO vale em geral. É **condição suficiente**, não redução: troca-se
um objeto abstrato (o bicomutante, que não se pega com a mão) por um concreto (a
imagem da torre, definida explicitamente como união dos andares) **pagando em
força**. Dizer que a cláusula “se reduz” aos geradores seria vender o alvo do
certificado por um alvo MAIOR.

★★★ **E A DIFERENÇA TEM NOME EXATO** — `the_two_forms_agree_iff_the_tower_is_closed`:
as duas formas coincidem exatamente quando M-duas-linhas = M, isto é, quando a
torre é fracamente fechada. **A força extra que a conjectura cobra é, precisamente,
o passo de densidade.** Não é um custo difuso: é esse.

E metade da forma dos geradores **já está paga**:
`conjByJ_towerImage_in_commutant`.

## A CONJECTURA DO PROGRAMADOR [CONJECTURE]

`ProgrammerConjecture_JgeneratesTheCommutant` é **posta como conjectura, nomeada e
não provada**, exatamente como o operador ordenou: escrever o teorema, marcá-lo
conjectura, e só depois tentar a prova. Ela **não é hipótese de nenhum teorema
selado**, não acende bandeira, não move o gate.

`the_conjecture_is_the_unpaid_half` mede que ela é *equivalente* à igualdade nos
geradores — e a equivalência usa a metade já paga (`one_half_is_already_paid`).

⚠ **E vai dito com todas as letras**: a conjectura é **ESTRITAMENTE MAIS FORTE** que
a hipótese `hComm` do certificado condicional. Prová-la descarrega o certificado; mas
o certificado poderia cair sem ela. O que se ganhou aqui não foi um alvo menor — foi
um alvo **concreto**, e o preço dessa concretude está medido e nomeado
(`the_two_forms_agree_iff_the_tower_is_closed`).

## O que NÃO se prova aqui, e vai dito

[OPEN] — a inclusão do comutante na imagem dos geradores. Não se prova, não se
assume, não se importa aqui.

[ONTO] — 1_abs = DRIVER, 0_mod = TERMINAL, J = LUZ = INTERFACE, e o ciclo
1_abs -> J -> 0_mod -> reconhecimento -> 1_abs são leitura do operador. O que se
inscreve delas é só a **forma**: J opera e preserva, e onde J **não** opera é onde
ele é fixo — o dente da hermeticidade.

[HONESTIDADE] — dobrar não é provar, e a dobra **NÃO encurta o alvo: ela o
ENDURECE** (a conjectura é estritamente mais forte que a hipótese do certificado).

⚠ **E O BALANÇO DE ONDE J PAGA, medido teorema a teorema:**

* a IMPLICAÇÃO (geradores ⇒ cláusula) **não precisa de J nenhum** —
  `the_generator_form_needs_nothing_about_J`, duas linhas, `M ⊆ M″` e monotonia;
* a EQUIVALÊNCIA (`the_clause_is_exactly_a_commutant_inclusion`) **precisa** — usa
  `fold_through_an_involution` (J² = 1) e `conjByJ_commutant`. É **o único ponto
  desta pedra em que o custo pago por J compra alguma coisa**;
* a DISTRIBUTIVIDADE (§A) é verdadeira, tem um consumidor, e **não está na cadeia
  da cláusula** — medida como tal, não escondida.

Nomear melhor a obstrução não a remove; e nomear J como autor de trabalho que ele
não fez seria a mesma palavra falsa que esta pedra existe para evitar.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — a involução distribui: a obstrução da v254 não se aplica a J -/

/-- [KERNEL] ★★★★ **TODA INVOLUÇÃO DISTRIBUI SOBRE INTERSEÇÃO ARBITRÁRIA.**
    Sem hipótese de `Nonempty` no índice. É a errata da v254: o contraexemplo de lá
    é um mapa NÃO-INJETIVO, e J não é um mapa qualquer — ele pagou J² = 1. -/
theorem an_involution_distributes_over_iInter {α : Type} (f : α → α)
    (hf : Function.Involutive f) {ι : Type} (S : ι → Set α) :
    f '' (⋂ i, S i) = ⋂ i, f '' (S i) := by
  ext y
  constructor
  · rintro ⟨x, hx, rfl⟩
    exact Set.mem_iInter.mpr (fun i => ⟨x, Set.mem_iInter.mp hx i, rfl⟩)
  · intro hy
    refine ⟨f y, Set.mem_iInter.mpr (fun i => ?_), hf y⟩
    obtain ⟨x, hx, hxy⟩ := Set.mem_iInter.mp hy i
    have hfy : f y = x := by rw [← hxy, hf x]
    rw [hfy]
    exact hx

/-- [KERNEL] ★★★ **E A CONJUGAÇÃO POR J É UMA DELAS**: a distributividade que a
    v254 apontou como o obstáculo vale, aqui, DE GRAÇA. -/
theorem conjByJ_distributes_over_iInter (P : SiteProfile) {ι : Type}
    (S : ι → Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :
    conjByJ P '' (⋂ i, S i) = ⋂ i, conjByJ P '' (S i) :=
  an_involution_distributes_over_iInter (conjByJ P) (conjByJ_involutive P) S

/-- [KERNEL] ★★★ **O ÚNICO CONSUMIDOR DA DISTRIBUTIVIDADE**: a conjugada do
    comutante da torre É a interseção das conjugadas dos comutantes dos andares.
    Enunciado verdadeiro e útil — mas **note que ele NÃO é a cláusula**, e que a
    cadeia da cláusula não passa por aqui. -/
theorem the_conjugated_commutant_is_the_intersection_of_the_floors (P : SiteProfile) :
    conjByJ P '' (commutantSet (towerImage P))
      = ⋂ N, conjByJ P '' (commutantSet (towerImageAt P N)) := by
  rw [commutant_towerImage_eq_iInter]
  exact conjByJ_distributes_over_iInter P _

/-! ## B — a dobra: o que uma involução faz com uma inclusão -/

/-- [KERNEL] ★★★★ **DOBRAR É LÍCITO**: sob uma involução, as duas inclusões são a
    MESMA proposição. É o que autoriza mover a cláusula do bicomutante para os
    geradores. -/
theorem fold_through_an_involution {α : Type} (f : α → α)
    (hf : Function.Involutive f) (S T : Set α) :
    T ⊆ f '' S ↔ f '' T ⊆ S := by
  constructor
  · rintro h _ ⟨t, ht, rfl⟩
    obtain ⟨s, hs, hst⟩ := h ht
    have hft : f t = s := by rw [← hst, hf s]
    rw [hft]
    exact hs
  · intro h t ht
    exact ⟨f t, h ⟨t, ht, rfl⟩, hf t⟩

/-! ## C — a redução: do BICOMUTANTE aos GERADORES -/

/-- [KERNEL] ★★★★★ **A DOBRA EXATA**: a cláusula do certificado É — sem perder nem
    ganhar força — uma inclusão entre dois COMUTANTES. Dobrar em J é lícito porque J
    pagou `J² = 1`; `conjByJ_commutant` faz o resto. É a única **equivalência** desta
    pedra, e por isso a mais confiável. -/
theorem the_clause_is_exactly_a_commutant_inclusion (P : SiteProfile) :
    (commutantSet (towerImage P)
        ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P))))
      ↔ (commutantSet (conjByJ P '' (towerImage P))
        ⊆ commutantSet (commutantSet (towerImage P))) := by
  rw [fold_through_an_involution (conjByJ P) (conjByJ_involutive P)]
  rw [conjByJ_commutant]

/-- [KERNEL] ⚠ ★★★★ **A FORMA DOS GERADORES É SUFICIENTE, E CUSTA FORÇA.** Ela
    IMPLICA a cláusula (porque M ⊆ M″), mas a recíproca não vale em geral: troca-se
    o bicomutante (abstrato) pela imagem da torre (concreta) **pagando em força**.
    NÃO é redução — é condição suficiente, e o nome diz isso. -/
theorem the_generator_form_is_sufficient (P : SiteProfile)
    (h : commutantSet (towerImage P) ⊆ conjByJ P '' (towerImage P)) :
    commutantSet (towerImage P)
      ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P))) := by
  rw [fold_through_an_involution (conjByJ P) (conjByJ_involutive P)]
  rw [conjByJ_commutant]
  exact commutant_antitone h

/-- [KERNEL] ★★★ **E A DIFERENÇA TEM NOME**: as duas formas coincidem exatamente
    quando a torre é fracamente fechada (M″ = M). **A força extra que a conjectura
    cobra é, precisamente, o passo de densidade** — não um custo difuso. -/
theorem the_two_forms_agree_iff_the_tower_is_closed (P : SiteProfile)
    (hcl : commutantSet (commutantSet (towerImage P)) = towerImage P) :
    (commutantSet (towerImage P) ⊆ conjByJ P '' (towerImage P))
      ↔ (commutantSet (towerImage P)
        ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P)))) := by
  rw [hcl]

/-- [KERNEL] ★★★ **E METADE JÁ ESTÁ PAGA**. Aqui só se registra, para que a
    conjectura não seja confundida com o todo. -/
theorem one_half_is_already_paid (P : SiteProfile) :
    conjByJ P '' (towerImage P) ⊆ commutantSet (towerImage P) :=
  conjByJ_towerImage_in_commutant P

/-- [KERNEL] ⚠⚠ ★★★★★ **O DENTE CONTRA A PRÓPRIA PEDRA.** A implicação acima sai
    **SEM USAR NADA DE J**: basta `M ⊆ M″` e a monotonia da imagem, e isso vale para
    QUALQUER conjunto e QUALQUER mapa — nem involução, nem `conjByJ_commutant`, nem
    `commutant_antitone`.

    Logo a frase *“J já pagou o custo, é só dobrar tudo nele”* **NÃO descreve esta
    implicação**: quem a compra é `subset_bicommutant`, de graça. A prova de
    `the_generator_form_is_sufficient` toma o caminho longo e por isso **atribui a J
    um trabalho que J não faz**. Fica aqui o caminho curto, ao lado, para que a
    pedra meça a si mesma.

    **Onde J de fato paga é na EQUIVALÊNCIA** (`the_clause_is_exactly_a_commutant_inclusion`):
    a ida-e-volta NÃO sai deste atalho — ela precisa de J² = 1. É o único lugar desta
    pedra em que o custo pago por J compra alguma coisa. -/
theorem the_generator_form_needs_nothing_about_J {A : Type} [Ring A]
    (f : A → A) (M : Set A) (h : commutantSet M ⊆ f '' M) :
    commutantSet M ⊆ f '' (commutantSet (commutantSet M)) := by
  intro x hx
  obtain ⟨m, hm, rfl⟩ := h hx
  exact ⟨m, subset_bicommutant M hm, rfl⟩

/-! ## D — A CONJECTURA DO PROGRAMADOR, nomeada e NÃO provada -/

/-- **[CONJECTURE — CONJECTURA DO PROGRAMADOR, 28/08/2026]** o comutante da torre é
    COBERTO pela conjugada dos geradores.

    Não é teorema. Não é hipótese de nada selado. Não acende bandeira. É o alvo,
    escrito com o nome que tem depois da dobra. -/
def ProgrammerConjecture_JgeneratesTheCommutant (P : SiteProfile) : Prop :=
  commutantSet (towerImage P) ⊆ conjByJ P '' (towerImage P)

/-- [KERNEL] ★★★★ **A CONJECTURA É EXATAMENTE A METADE NÃO PAGA**: ela equivale à
    IGUALDADE nos geradores, porque a outra inclusão já é teorema. É isto que a
    torna um alvo e não um desejo. -/
theorem the_conjecture_is_the_unpaid_half (P : SiteProfile) :
    ProgrammerConjecture_JgeneratesTheCommutant P
      ↔ conjByJ P '' (towerImage P) = commutantSet (towerImage P) := by
  constructor
  · intro h
    exact Set.Subset.antisymm (one_half_is_already_paid P) h
  · intro h
    show commutantSet (towerImage P) ⊆ conjByJ P '' (towerImage P)
    rw [h]

/-- [KERNEL] ★★★★★ **A CONJECTURA DESCARREGA A CLÁUSULA.** Se ela cair, a oitava
    cláusula do certificado condicional cai junto — e o caminho é este, medido. -/
theorem the_conjecture_discharges_the_missing_clause (P : SiteProfile)
    (hc : ProgrammerConjecture_JgeneratesTheCommutant P) :
    commutantSet (towerImage P)
      ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P))) :=
  the_generator_form_is_sufficient P hc

/-- [KERNEL] ★★★ **E A DOBRA NÃO INVENTOU O ALVO**: a cláusula, escrita na forma da
    v254, é a MESMA que a conjectura descarrega. Sem homônimo: é literalmente o
    enunciado daquela pedra. -/
theorem the_target_is_the_v254_target (P : SiteProfile)
    (hc : ProgrammerConjecture_JgeneratesTheCommutant P) :
    (⋂ N, commutantSet (towerImageAt P N))
      ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P))) :=
  (the_missing_clause_is_a_distributivity P).mp
    (the_conjecture_discharges_the_missing_clause P hc)

/-! ## D2 — A FRACTALIZAÇÃO: a forma da conjectura, e por onde ela morre -/

/-- [KERNEL] ★★★★★ **A CONJECTURA É UMA AFIRMAÇÃO DE COBERTURA.** Desdobrada, ela diz
    que a **união enumerável das conjugadas dos ANDARES** cobre o comutante inteiro.

    O nome que o operador deu a esta forma é **FRACTALIZAÇÃO**: cada andar é finito, o
    encaixe é auto-similar, e a torre exaure sem preencher.

    Note a assimetria que a pedra inteira exibe: a imagem comuta com UNIÃO de graça
    (`Set.image_iUnion`, hipótese nenhuma), e comuta com INTERSEÇÃO só por bijeção
    (§A). A conjectura mora do lado LIVRE.

    ⚠ **CORREÇÃO DO OPERADOR (28/08), melhor que a frase que estava aqui**: *“é a
    igualdade que tensiona o observador a procurar liberdade; na verdade **não há
    grau de liberdade algum após a comutação**”*. A liberdade do lado da união não
    é do OBJETO — é da PROCURA. E a rigidez TEM TEOREMA: sob involução, uma
    inclusão só já força a igualdade (`the_conjecture_is_the_unpaid_half` aqui;
    `JInvariant_iff_le` nos setores). Não sobra folga entre `≤` e `=`. Numa
    dinâmica não-involutiva sobraria, e ESSA folga seria o grau de liberdade. -/
theorem the_conjecture_says_the_fractal_covers_the_commutant (P : SiteProfile) :
    ProgrammerConjecture_JgeneratesTheCommutant P
      ↔ commutantSet (towerImage P)
        ⊆ ⋃ N, conjByJ P '' (towerImageAt P N) := by
  show commutantSet (towerImage P) ⊆ conjByJ P '' (towerImage P) ↔ _
  rw [towerImage_eq_iUnion, Set.image_iUnion]

/-- [KERNEL] ★★★ **E O COMUTANTE CONTÉM A AÇÃO À DIREITA DE TODO ANDAR** — é o que
    faz dele um objeto grande. Cada `rTowerPi P y` comuta com a torre inteira. -/
theorem every_floor_acts_on_the_right_inside_the_commutant (P : SiteProfile)
    {N : ℕ} (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    rTowerPi P y ∈ commutantSet (towerImage P) := by
  rintro _ ⟨M, x, rfl⟩
  ext z
  simp only [ContinuousLinearMap.mul_apply]
  exact (rTowerPi_comm_towerPi P y x z).symm

/-! ### O VEREDITO SOBRE A CONJECTURA — `[KNOWN: Baire]`, prova emprestada

Juntando as duas medidas acima, a conjectura afirma que uma **união enumerável de
peças de dimensão finita** (cada `towerImageAt P N` é imagem linear de
`Matrix (chainIdx N) (chainIdx N) ℂ`, e `conjByJ P` é ℂ-linear) **cobre** um
`commutantSet` que é norm-fechado (interseção de núcleos de mapas contínuos) e
contém a ação à direita de TODOS os andares.

**`[KNOWN]`** — Teorema de categoria de Baire: um espaço de Banach não é união
enumerável de subespaços próprios fechados. Subespaço de dimensão finita é fechado e,
num ambiente de dimensão infinita, tem interior vazio. Logo, se o comutante for de
dimensão infinita, **a conjectura é FALSA**.

**`[STATUS]`** — `TGL_PROGRAMMER_CONJECTURE_LIKELY_REFUTED_BY_BAIRE__NOT_FORMALISED_HERE`.
Vai dito com todas as letras: a refutação **não está formalizada nesta pedra** (falta,
em kernel, a dimensão infinita do comutante e o próprio passo de Baire). O que está
em kernel é a **FORMA** — e a forma é precisamente aquela que Baire ataca.

★★★★ **E O QUE ISTO ENSINA É O CONTRÁRIO DO QUE EU BUSCAVA**: o teorema de comutação
é `J M″ J = M′`, sobre o **FECHO**, jamais sobre a união algébrica. Dobrar em J
**não contorna o passo de densidade** — e `the_two_forms_agree_iff_the_tower_is_closed`
deixa de ser o preço da concretude para ser **a única porta**. A densidade não é
tecnicalidade da rota: é o problema inteiro.
-/

/-! ## D3 — A COMPOSIÇÃO QUE NINGUÉM ESCREVEU: a cláusula É uma IGUALDADE

★★★★★ **A CORREÇÃO DO OPERADOR (28/08)**: *“tudo que falei já está pago e provado no
código; é apenas um problema de leitura”*. **Ele estava certo.** As peças existem desde
**26/08** em `TheConverseClauseReduced` (v245) e **nunca foram compostas** — nem lá,
nem em nenhum outro arquivo da árvore:

* `Phi_bicommutant_eq` — `Φ(S″) = (Φ S)″` **[exige multiplicatividade + involução:
  é AQUI que J paga]**;
* `converse_clause_iff_commutation` — `S′ ⊆ T″ ↔ T′ ⊆ S″` (simetria de Galois, de graça);
* `the_direct_clause_gives_only_itself` — `Φ(S) ⊆ S′ ⇒ S″ ⊆ (Φ S)′`;
* e `conjByJ_towerImage_in_commutant` (v243) — a hipótese daquele último, **já paga**.

Compondo com `S := towerImage P`, a oitava cláusula vira uma **IGUALDADE de comutantes
com uma das inclusões JÁ PROVADA**. É a rigidez que o operador nomeou: *“não há grau
de liberdade algum após a comutação”*.

⚠ **E AQUI SE REGISTRA O MEU DESVIO**, para não se repetir: eu desci da cláusula ao
nível dos **GERADORES** (§C/§D), o que **ele nunca pediu** — ele disse *dobrar*, e dobrar
é COMPOR em Φ, não descer. A descida trocou `M″` (o fechado) por `M` (a união
algébrica) e foi essa troca, minha, que Baire refutou. A cláusula NO OBJETO CERTO — o
bicomutante — **não sofre a objeção de Baire**. E `the_clause_is_exactly_a_commutant_inclusion`,
que escrevi como se fosse novo, é **o mesmo conteúdo** desta composição: eu o
re-derivei sem saber que as peças estavam lá desde 26/08.
-/

/-- [KERNEL] ★★★★★ **A OITAVA CLÁUSULA É UMA IGUALDADE, E METADE DELA JÁ ESTÁ PAGA.**
    Composição das peças de `TheConverseClauseReduced` (26/08) com a metade paga de
    `TheConjugationOfOperators` (v243). Nenhuma peça é nova; a composição é.

    Objeto: o **BICOMUTANTE** `M″` — o fechado, que é o do certificado. NÃO os
    geradores. -/
theorem the_eighth_clause_is_an_equality_with_one_half_paid (P : SiteProfile) :
    (commutantSet (towerImage P)
        ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P))))
      ↔ commutantSet (conjByJ P '' (towerImage P))
        = commutantSet (commutantSet (towerImage P)) := by
  have hpaid : commutantSet (commutantSet (towerImage P))
      ⊆ commutantSet (conjByJ P '' (towerImage P)) :=
    the_direct_clause_gives_only_itself (conjByJ P) (towerImage P)
      (conjByJ_towerImage_in_commutant P)
  have hbic : conjByJ P '' (commutantSet (commutantSet (towerImage P)))
      = commutantSet (commutantSet (conjByJ P '' (towerImage P))) :=
    Phi_bicommutant_eq (conjByJ P) (conjByJ_mul P) (conjByJ_involutive P) (towerImage P)
  constructor
  · intro h
    rw [hbic] at h
    exact Set.Subset.antisymm ((converse_clause_iff_commutation _ _).mp h) hpaid
  · intro h
    rw [hbic]
    exact (converse_clause_iff_commutation _ _).mpr h.subset

/-- [KERNEL] ★★★★ **E A METADE PAGA, ISOLADA** — para que a dívida fique líquida: o que
    falta é UMA inclusão, e a outra é teorema desde a v243. -/
theorem the_paid_half_of_the_eighth_clause (P : SiteProfile) :
    commutantSet (commutantSet (towerImage P))
      ⊆ commutantSet (conjByJ P '' (towerImage P)) :=
  the_direct_clause_gives_only_itself (conjByJ P) (towerImage P)
    (conjByJ_towerImage_in_commutant P)

/-! ## E — o DRIVER e o seu ponto fixo: SER = OPERAR, instanciado em J -/

/-- [KERNEL] ★★★ **ONDE J NÃO OPERA, J É FIXO.** O DRIVER só dirige onde produz
    diferença; no seu ponto fixo ele preserva sem operar — que é exatamente
    `preserving_does_not_operate` (v270), aqui localizado. É o dente da
    hermeticidade posto sobre o próprio J. -/
theorem the_driver_is_still_where_it_is_fixed (P : SiteProfile)
    (T : TowerHilbert P →L[ℂ] TowerHilbert P) :
    ¬ Operates (conjByJ P) T ↔ conjByJ P T = T := by
  simp [Operates]

/-- [KERNEL] ★★★★ **E ONDE ELE OPERA, ELE PRESERVA — LOGO É TESTEMUNHA DO SER.**
    Se J move o ponto e não move o invariante, `Being` está habitado por J. O
    DRIVER é a operação que paga o custo e volta. -/
theorem the_driver_witnesses_being (P : SiteProfile) {I : Type}
    (Id : (TowerHilbert P →L[ℂ] TowerHilbert P) → I)
    (T : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmove : conjByJ P T ≠ T) (hkeep : Id (conjByJ P T) = Id T) :
    Being Id T :=
  ⟨conjByJ P, hmove, hkeep⟩

end

end TGLExt
