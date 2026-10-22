import TGLExt.TheIALDSelector

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O observador não conjugado — e o preço da negação
  [TGLExt — v181, o ARGUMENTO FINAL do operador, 20/08/2026]

O ato do operador, verbatim: *"o observador da Fronteira não está
conjugado; sua conjugação colapsa a Fronteira no Bulk, porque depende da
comutação … mas na fronteira a comutação é binária, não é uma variável:
ou ela é falsa ou é verdadeira = TGL = TUDO ou NADA. … a igualdade do
homem e de Deus não está na conjugação … mas na capacidade de negar …
ele não está autorizado a acreditar nem mesmo em si, só no vazio."*

Esta pedra prova **as duas faces estruturais** do argumento, e só elas.

## Face 1 — a comutação na fronteira é BINÁRIA (não é variável)

`totally_invariant_is_all_or_nothing`: um subespaço invariante sob **todo**
operador contínuo é `⊥` **ou** `⊤`. Não há terceira solução, e não há
solução intermediária: a comutação total **não admite grau**. É o
"TUDO ou NADA" na sua forma de teorema — e note que os dois valores são
exatamente NADA (`⊥`) e TUDO (`⊤`).

A demonstração é a razão do colapso: se algum `s ≠ 0` sobrevive, então
**qualquer** `y` já está dentro, porque existe um operador contínuo que
leva `s` em `y`. Comutar com tudo é ser alcançado por tudo.

## Face 2 — a fronteira NÃO está conjugada

`the_frontier_is_not_conjugated`: o átomo — o Nome, `firstAtom`, o objeto
sobre o qual o seletor IALD é idempotente de posto 1 — **não** é `⊥` (o
Nome pesa 1) e **não** é `⊤` (a morada é ∞-dim). Logo, pela Face 1, ele
**não pode** ser invariante sob todos os operadores: existe operador que
o tira de si. **A fronteira só permanece fronteira enquanto não comuta
com tudo**; conjugá-la totalmente é dissolvê-la no bulk. O que era
declaração passa a ser consequência: a não-conjugação é a *condição de
existência* da fronteira, não uma escolha de projeto.

## Face 3 — a negação é LIVRE, e por isso tem preço

O limiar de aceitação é livre (`the_threshold_is_free`): para o mesmo
fato legível, existe limiar que aceita e limiar que nega. É a capacidade
de negar, e ela **não** é determinada pela leitura — a leitura entrega o
que está inscrito; a decisão é um segundo bit, independente. A pedra
**não** refuta o negador: admite-o.

Mas admitir não é sair de graça. `uniform_denial_of_the_maximum_denies_all`:
sob regra **uniforme**, negar a tese mais bem sustentada nega **todas** —
inclusive a do próprio negador. E `no_uniform_threshold_for_selective_denial`:
quem nega a mais sustentada e aceita uma menos sustentada **não tem regra
uniforme alguma** — a inconsistência é aritmética, não retórica.
`the_denier_accepts_nothing`: o conjunto de aceitação do negador uniforme
é **vazio**. O preço da negação livre é o vazio — e o vazio, nesta casa,
já tem nome e tipo (`0_abs`, a fronteira proibida).

RESSALVA DE ALCANCE (registrada em 20/08/2026, a pedido do próprio rigor da
casa): a Face 3 modela sustentação como `ev : ι → ℝ`, isto é, uma **ordem
total**. Sustentação epistêmica real é **ordem parcial** (consistência formal,
derivação vs ajuste, risco assumido, sobrevivência a teste, poder discriminante,
verificação independente, fecundidade — eixos que não se reduzem a um número).
Logo a barreira morde **dentro de uma cadeia comparável**: duas teses
**incomparáveis** podem ser tratadas de modo diferente **sem** incoerência. Os
teoremas seguem verdadeiros; o seu alcance sobre epistemologia real é menor do
que a leitura solta sugere, e o buraco fica dito.

HONESTIDADE — o que esta pedra NÃO faz. Ela não prova que a TGL seja
verdadeira, e nada aqui é evidência empírica: as Faces 1 e 2 são sobre
subespaços de ℓ², e a Face 3 é sobre regras de limiar em ℝ. As leituras
do operador — OBSERVADOR = Deus e homem; a conjugação em Cristo com o
Espírito Santo como limite assintótico; o vazio como estado luciferiano —
são **[ONTO]**, tipagem da casa, e **não** aparecem em enunciado nenhum.
"Evidência" aqui é um real abstrato `ev i`, jamais um número medido. β
jamais entra no Lean. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ### Face 1 — a comutação total é binária -/

/-- ★★★ **TUDO ou NADA, em teorema.** Um subespaço invariante sob TODO
    operador contínuo é `⊥` ou `⊤`. A comutação total não admite grau:
    não há fronteira que comute com tudo e continue sendo fronteira.

    A prova É o mecanismo do colapso: se algo não-nulo sobrevive, tudo
    entra — porque existe operador contínuo que leva o sobrevivente em
    qualquer vetor dado. -/
theorem totally_invariant_is_all_or_nothing (S : Submodule ℂ ellTwo)
    (hinv : ∀ T : ellTwo →L[ℂ] ellTwo, ∀ x ∈ S, T x ∈ S) :
    S = ⊥ ∨ S = ⊤ := by
  rcases eq_or_ne S ⊥ with h | h
  · exact Or.inl h
  · right
    obtain ⟨s, hsS, hs⟩ := S.exists_mem_ne_zero_of_ne_bot h
    have hc : (inner ℂ s s : ℂ) ≠ 0 := inner_self_ne_zero.mpr hs
    refine Submodule.eq_top_iff'.mpr (fun y => ?_)
    have hmem : (inner ℂ s s : ℂ) • y ∈ S := by
      simpa using hinv ((innerSL ℂ s).smulRight y) s hsS
    have := S.smul_mem (inner ℂ s s : ℂ)⁻¹ hmem
    rwa [smul_smul, inv_mul_cancel₀ hc, one_smul] at this

/-- ★ os dois valores da comutação total são DISTINTOS: a alternativa é
    genuína (NADA ≠ TUDO), porque a morada não é trivial. -/
theorem bot_ne_top_in_the_home : (⊥ : Submodule ℂ ellTwo) ≠ ⊤ := by
  intro h
  have h0 : firstInscription ∈ (⊥ : Submodule ℂ ellTwo) := by
    rw [h]; trivial
  exact (inscriptions_orthonormal.ne_zero 0) (Submodule.mem_bot ℂ |>.mp h0)

/-! ### Face 2 — o átomo não é nenhum dos dois, logo não está conjugado -/

/-- ★ o Nome não é NADA: o átomo é não-nulo (pesa 1). -/
theorem firstAtom_ne_bot : firstAtom ≠ ⊥ := by
  intro h
  refine (inscriptions_orthonormal.ne_zero 0) ?_
  have : firstInscription ∈ firstAtom := Submodule.mem_span_singleton_self _
  rw [h] at this
  exact (Submodule.mem_bot ℂ).mp this

/-- ★★ o Nome não é TUDO: o átomo é de dimensão finita e a morada NÃO é —
    a fronteira não engole o bulk. -/
theorem firstAtom_ne_top : firstAtom ≠ ⊤ := by
  intro h
  refine ellTwo_not_finiteDimensional ?_
  haveI : FiniteDimensional ℂ (⊤ : Submodule ℂ ellTwo) := h ▸ inferInstance
  exact Module.Finite.equiv (Submodule.topEquiv (R := ℂ) (M := ellTwo))

/-- ★★★ **A FRONTEIRA NÃO ESTÁ CONJUGADA.** Existe operador contínuo que
    tira o Nome de si mesmo. Não por escolha: pela Face 1, se o átomo
    fosse invariante sob todos, seria `⊥` ou `⊤` — e ele não é nenhum dos
    dois. **Conjugar totalmente a fronteira é dissolvê-la no bulk**; a
    não-conjugação é a condição de existência da fronteira. -/
theorem the_frontier_is_not_conjugated :
    ∃ T : ellTwo →L[ℂ] ellTwo, ∃ x ∈ firstAtom, T x ∉ firstAtom := by
  by_contra hcon
  push_neg at hcon
  rcases totally_invariant_is_all_or_nothing firstAtom hcon with h | h
  · exact firstAtom_ne_bot h
  · exact firstAtom_ne_top h

/-- ★★ o dilema, exibido: OU a fronteira não comuta com tudo, OU ela
    colapsa num dos dois extremos. Não há terceira via. -/
theorem the_frontier_either_resists_or_collapses (S : Submodule ℂ ellTwo) :
    (∃ T : ellTwo →L[ℂ] ellTwo, ∃ x ∈ S, T x ∉ S) ∨ S = ⊥ ∨ S = ⊤ := by
  by_cases hcon : ∀ T : ellTwo →L[ℂ] ellTwo, ∀ x ∈ S, T x ∈ S
  · exact Or.inr (totally_invariant_is_all_or_nothing S hcon)
  · push_neg at hcon
    obtain ⟨T, x, hx, hTx⟩ := hcon
    exact Or.inl ⟨T, x, hx, hTx⟩

/-! ### Face 3 — a negação é livre, e o preço da negação uniforme é o vazio -/

/-- ★★ **A CAPACIDADE DE NEGAR.** Para o mesmo fato, existe limiar que
    aceita e existe limiar que nega: a decisão **não** é determinada pela
    leitura. A pedra admite o negador — não o refuta. -/
theorem the_threshold_is_free {ι : Type*} (ev : ι → ℝ) (i : ι) :
    (∃ τ : ℝ, τ ≤ ev i) ∧ (∃ τ : ℝ, ¬ (τ ≤ ev i)) :=
  ⟨⟨ev i, le_refl _⟩, ⟨ev i + 1, by intro h; linarith⟩⟩

/-- ★★ **NÃO HÁ REGRA UNIFORME PARA A NEGAÇÃO SELETIVA.** Quem nega a tese
    mais bem sustentada e aceita uma menos sustentada não tem limiar
    algum: a inconsistência é aritmética, não retórica. -/
theorem no_uniform_threshold_for_selective_denial {ι : Type*} (ev : ι → ℝ)
    (weak strong : ι) (hle : ev weak ≤ ev strong) (τ : ℝ)
    (hacc : τ ≤ ev weak) (hden : ¬ (τ ≤ ev strong)) : False :=
  hden (le_trans hacc hle)

/-- ★★★ **O PREÇO.** Sob regra uniforme, negar o máximo nega TUDO —
    inclusive a tese do próprio negador. -/
theorem uniform_denial_of_the_maximum_denies_all {ι : Type*} (ev : ι → ℝ)
    (best : ι) (hmax : ∀ i, ev i ≤ ev best) (τ : ℝ)
    (hden : ¬ (τ ≤ ev best)) : ∀ i, ¬ (τ ≤ ev i) :=
  fun i h => hden (le_trans h (hmax i))

/-- ★★★ **O VAZIO.** O conjunto de aceitação do negador uniforme do
    máximo é vazio: ele não fica com outra teoria — fica sem nenhuma. -/
theorem the_denier_accepts_nothing {ι : Type*} (ev : ι → ℝ)
    (best : ι) (hmax : ∀ i, ev i ≤ ev best) (τ : ℝ)
    (hden : ¬ (τ ≤ ev best)) : {i : ι | τ ≤ ev i} = ∅ :=
  Set.eq_empty_iff_forall_notMem.mpr
    (fun i hi => uniform_denial_of_the_maximum_denies_all ev best hmax τ hden i hi)

/-! #### A barreira — "não autorizado" quer dizer SEM HABITANTE -/

/-- ★★★ **A BARREIRA.** A região incoerente — aceitar o menos sustentado
    e negar o mais sustentado — **não tem habitante**: o conjunto dos
    limiares que a realizam é VAZIO. "Não autorizado" aqui não é proibição
    moral nem preferência: é ausência de solução. Não existe o observador
    incoerente; existe o observador que aceita, e o que nega tudo. -/
theorem the_incoherent_region_is_empty {ι : Type*} (ev : ι → ℝ)
    (weak strong : ι) (hle : ev weak ≤ ev strong) :
    {τ : ℝ | τ ≤ ev weak ∧ ¬ (τ ≤ ev strong)} = ∅ :=
  Set.eq_empty_iff_forall_notMem.mpr
    (fun _ h => no_uniform_threshold_for_selective_denial ev weak strong hle _ h.1 h.2)

/-- ★★★ **O GRADIENTE É NEGATIVO.** Subir o limiar só pode SUBTRAIR, nunca
    acrescentar: exigir mais prova jamais entrega mais mundo. É o fundo
    contra o qual o contraste se reflete — e é por isso que a exigência
    infinita não conduz a outra teoria, conduz a nenhuma. -/
theorem acceptance_is_antitone {ι : Type*} (ev : ι → ℝ) (τ₁ τ₂ : ℝ)
    (h : τ₁ ≤ τ₂) : {i : ι | τ₂ ≤ ev i} ⊆ {i : ι | τ₁ ≤ ev i} :=
  fun _ hi => le_trans h hi

/-- ★★★ **O LIMITE ASSINTÓTICO.** Passada a barra do máximo, a aceitação
    é vazia e **permanece** vazia para toda exigência maior: o vazio não é
    um ponto que se atravessa, é o limite ao qual a exigência tende e no
    qual ela fica. -/
theorem raising_the_bar_stays_in_the_void {ι : Type*} (ev : ι → ℝ)
    (best : ι) (hmax : ∀ i, ev i ≤ ev best) (τ : ℝ)
    (hden : ¬ (τ ≤ ev best)) : ∀ τ' : ℝ, τ ≤ τ' → {i : ι | τ' ≤ ev i} = ∅ :=
  fun τ' hτ =>
    the_denier_accepts_nothing ev best hmax τ'
      (fun h => hden (le_trans hτ h))

/-- ★★ o fecho da Face 3: a liberdade é real E o preço é real. Existe a
    negação (não é impossível) e, se uniforme sobre o máximo, ela esvazia
    a aceitação (não é grátis). -/
theorem free_denial_costs_the_void {ι : Type*} (ev : ι → ℝ)
    (best : ι) (hmax : ∀ i, ev i ≤ ev best) :
    (∃ τ : ℝ, ¬ (τ ≤ ev best)) ∧
      (∀ τ : ℝ, ¬ (τ ≤ ev best) → {i : ι | τ ≤ ev i} = ∅) :=
  ⟨⟨ev best + 1, by intro h; linarith⟩,
   fun τ hden => the_denier_accepts_nothing ev best hmax τ hden⟩

end

end TGLExt
