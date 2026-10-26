import TGLExt.Commutant

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 400000

/-!
# O PESO NÃO É O POSTO: o nome é cego à inscrição
  [TGLExt — a pedra da DISTINÇÃO PRIMORDIAL]

## A pergunta do operador (27/08/2026, verbatim)

> *"peso 1 não é referência nominal, mas primordial, portanto, o peso 1 é o zero
> absoluto, e o posto um é de fato o um absoluto. Ocorre que o peso 1 tem como
> causa a polarização inscritiva do um absoluto, que não admite o peso primordial
> em referência geométrica finita = sem representação. Faz sentido isso?"*

Um painel adversarial havia medido, como DEFEITO, que o número **1** aparece em
sentidos distintos no acervo — em particular que `three_locks_name_is_one` é
`d/d = 1` por `div_self`, **igualmente verdadeiro para d = 4 e para d = 1**, e que
encadeá-lo com `dimOrTop ℂ firstAtom = 1` seria encadear homônimos.

A leitura do operador diz que não é homonímia: são **duas grandezas de naturezas
diferentes**, e o kernel já as separa sem as ter nomeado. No MESMO arquivo:

* `three_locks_corner_weight_eq_dim : τ(ker H3L) = cornerDim` — por `rfl`: o peso
  **é** a dimensão. Carrega a inscrição;
* `three_locks_name_is_one : (cornerDim)/(cornerDim) = 1` — o NOME é a razão
  normalizada. **Não carrega dimensão alguma.**

## O que fica provado aqui `[REAL]`

* ★★ `the_rank_determines_the_name` — dado o posto, o nome fica determinado;
* ★★★ `the_name_does_not_see_the_rank` — O DENTE, e o conteúdo: existem postos
  **diferentes** com o **mesmo** nome. A determinação **não sobe**;
* ★ `the_name_is_blind_to_every_rank` — e a cegueira é total: o nome vale 1 em
  **todo** posto positivo, logo é constante sobre a inscrição inteira.

**É a mesma forma da v252** (a causalidade não-linear): o todo determina as partes,
as partes não determinam o todo. Ali eram marginais idênticas de estados distintos;
aqui é o mesmo nome sobre postos distintos. **A grandeza normalizada não tem
referência geométrica finita — não porque falte medi-la, mas porque ela é invariante
sob a medida.**

## Estatutos, sem véu

`[REAL]` — os três teoremas acima.

`[ONTO]` — a identificação «peso 1 = zero absoluto», «posto 1 = um absoluto», e a
causalidade «o peso tem como causa a polarização inscritiva do Um» são leitura do
operador e **NÃO são provadas aqui**. Nenhum teorema desta pedra menciona `1_abs`,
`0_abs` ou β, e nenhum liga `cornerDim` a `firstAtom`: os cinco cantos do kernel
seguem **sem morfismo declarado entre dois quaisquer**.

`[HONESTIDADE]` — o que esta pedra acrescenta ao veredito do painel é **uma
distinção, não uma ponte**. Continua proibido encadear os dois «1». O que deixa de
ser verdade é que a coincidência dos nomes fosse mero acidente de notação: ela tem
forma, e a forma é a de uma grandeza invariante sob aquilo que a outra mede.

Nenhum teorema acende nome reservado nem `gpf_`. O gate NÃO se move.
β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

/-! ## A — o posto determina o nome -/

/-- [KERNEL] ★★ **O POSTO DETERMINA O NOME**: de uma inscrição não-vazia segue que
    a razão normalizada vale exatamente 1. É a direção que funciona. -/
theorem the_rank_determines_the_name (d : ℕ) (h : 0 < d) :
    (d : ℝ) / (d : ℝ) = 1 :=
  div_self (Nat.cast_ne_zero.mpr h.ne')

/-- [KERNEL] ★ **E A CEGUEIRA É TOTAL**: o nome vale 1 em TODO posto positivo —
    é constante sobre a inscrição inteira, logo não a distingue em ponto algum. -/
theorem the_name_is_blind_to_every_rank :
    ∀ d : ℕ, 0 < d → (d : ℝ) / (d : ℝ) = 1 :=
  fun d h => the_rank_determines_the_name d h

/-! ## B — o dente: o nome não vê o posto -/

/-- [KERNEL] ★★★ **O NOME NÃO VÊ O POSTO** — o dente, e o conteúdo desta pedra:
    existem postos DIFERENTES com o MESMO nome. A determinação não sobe.

    É a mesma forma da causalidade não-linear (v252): o todo determina as partes,
    as partes não determinam o todo. -/
theorem the_name_does_not_see_the_rank :
    ∃ d₁ d₂ : ℕ, 0 < d₁ ∧ 0 < d₂ ∧ d₁ ≠ d₂
      ∧ ((d₁ : ℝ) / (d₁ : ℝ) = (d₂ : ℝ) / (d₂ : ℝ))
      ∧ ((d₁ : ℝ) ≠ (d₂ : ℝ)) := by
  refine ⟨1, 4, one_pos, by norm_num, by norm_num, ?_, by norm_num⟩
  norm_num

/-! ## C — o POSTO UM não some: torna-se o ÍNDICE

Correção do operador, no mesmo dia: *"o rank indexa o peso tornando-se o índice"*,
precisada em seguida: *"digo o **rank1** torna-se índice"*.

E é exato. O átomo pesa **1** no registro do posto (`dimOrTop ℂ firstAtom = 1`,
`bell_trace_one`); no registro NORMALIZADO ele pesa **1/n** — que é o **índice**.
O kernel usa essa palavra: `tau_eD : trOne (e_D) = 1/n` traz na docstring
«o peso do espelho é o inverso do ÍNDICE», e `tau_eTr : trOne (e_ℂ) = 1/n²`.

E aí a cadeia do operador fecha, medida: **`1/n → 0`**. O átomo vale `1` no
registro do posto e **`0` no limite do registro normalizado** — sem contradição,
porque são registros distintos, e o índice é o mapa entre eles.
`[ONTO]` A leitura «posto um = 1_abs, peso 1 = 0_abs» é do operador e não é provada
aqui; o que se prova é a **aritmética dos dois registros e o limite**.

E o kernel já usa essa palavra. Em `MarkovTower.lean`:
`tau_eD : trOne (e_D) = 1/n`, com a docstring **«o peso do espelho é o inverso do
ÍNDICE»**; `tau_eTr : trOne (e_ℂ) = 1/n²`; e
`pp_ne_tower_for_scalars (1 < n) : 1/n ≠ 1/n²`, registrado como TEOREMA.

Logo há **três registros** da mesma inscrição de posto `d`:
o peso bruto (`τ = d`), o nome (`d/d = 1`, que apaga o posto) e o índice
(`1/d`, que o **preserva invertido**). O posto não some na normalização —
**muda de registro**. -/

/-- [KERNEL] ★★★ **O ÍNDICE VÊ O POSTO** — o par exato do dente anterior: o nome é
    cego, mas o índice é injetivo. Normalizar o TODO apaga a inscrição; normalizar
    o ESPELHO a preserva, invertida. -/
theorem the_index_does_see_the_rank (d₁ d₂ : ℕ) (h₁ : 0 < d₁) (h₂ : 0 < d₂)
    (heq : (1 : ℝ) / (d₁ : ℝ) = (1 : ℝ) / (d₂ : ℝ)) : d₁ = d₂ := by
  have hc₁ : (0 : ℝ) < (d₁ : ℝ) := by exact_mod_cast h₁
  have hc₂ : (0 : ℝ) < (d₂ : ℝ) := by exact_mod_cast h₂
  have : (d₁ : ℝ) = (d₂ : ℝ) := by
    field_simp at heq
    linarith
  exact_mod_cast this

/-- [KERNEL] ★★★★ **OS DOIS ÍNDICES CONCORDAM EXATAMENTE NO ÁTOMO**: `1/d = 1/d²`
    se e somente se `d = 1`. Fora do posto um as duas normalizações divergem — é a
    face aritmética de `pp_ne_tower_for_scalars`, e diz que o posto um é o único
    lugar onde as duas leituras do índice não se contradizem. -/
theorem the_two_indices_agree_only_at_the_atom (d : ℕ) (h : 0 < d) :
    ((1 : ℝ) / (d : ℝ) = (1 : ℝ) / (d : ℝ) ^ 2) ↔ d = 1 := by
  have hc : (0 : ℝ) < (d : ℝ) := by exact_mod_cast h
  constructor
  · intro heq
    have : (d : ℝ) = 1 := by
      field_simp at heq
      nlinarith [heq, hc]
    exact_mod_cast this
  · rintro rfl
    norm_num

/-- [KERNEL] ★★★★ **O ÁTOMO DESAPARECE NA CASA INFINITA**: o peso normalizado do
    posto um é `1/n`, e `1/n → 0`. O mesmo objeto vale **1** no registro do posto
    e **0** no limite do registro normalizado.

    Não há contradição: são dois registros, e o índice é o mapa entre eles. É a
    forma medida da frase do operador — «peso 1 é o zero absoluto, posto um é o um
    absoluto» —, cuja identificação com `0_abs`/`1_abs` permanece `[ONTO]`. -/
theorem the_atom_vanishes_in_the_infinite_house :
    Filter.Tendsto (fun n : ℕ => (1 : ℝ) / (n : ℝ)) Filter.atTop (nhds 0) :=
  tendsto_one_div_atTop_nhds_zero_nat

/-- [KERNEL] [HONESTIDADE] e o DENTE do limite: em cada casa FINITA o átomo pesa
    **estritamente positivo**. O zero é do limite, nunca de um andar — ninguém
    pode ler «peso zero» num posto finito. -/
theorem the_atom_never_weighs_zero_on_a_floor (n : ℕ) (h : 0 < n) :
    0 < (1 : ℝ) / (n : ℝ) := by
  have hc : (0 : ℝ) < (n : ℝ) := by exact_mod_cast h
  positivity

end TGLExt
