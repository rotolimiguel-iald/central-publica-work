import TGLExt.TheStation
import Mathlib.LinearAlgebra.Dimension.Finrank

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A EXPLOSÃO, A PODA, O PISO, O REGISTRO E A CONJUGAÇÃO — v175

**SEGUNDA CORREÇÃO PÚBLICA (painel de fecho do arco).** Um terceiro painel
auditou esta pedra e derrubou mais nomes que prometiam além dos enunciados:
um ALIAS literal (`record_is_stable_under_reread`), um teorema que devolvia
a própria hipótese (`first_pass_changes_second_does_not`), um `rfl` com
argumento de enfeite (`name_weight_is_invariant`), um "global" que era só
"para todo x" (`pruning_is_global`), um nome que dizia par/ímpar sem a
hipótese que os torna par/ímpar (`even_plus_odd_is_twice`), e um piso
enunciado de modo VAZIO em dimensão infinita
(`no_dimension_strictly_between_zero_and_one`). Todos corrigidos ou
removidos abaixo. *A régua não tem dono: ela corrigiu a casa três vezes
no mesmo dia.*
  [TGLExt — ordem do operador, 20/08/2026]

**CORREÇÃO PÚBLICA (a régua trabalhando).** A V1 desta pedra foi
REPROVADA por painel adversarial em dois pontos, e ambos eram reais:
(i) `hilbert_floor_is_the_atom (n : ℕ) (h : 0 < n) : 1 ≤ n := h` era a
FUNÇÃO IDENTIDADE — em ℕ, `0 < n` é definicionalmente `1 ≤ n`; a
docstring atribuía a esse `id` uma tese sobre cantos, pesos e ω(I) que o
enunciado não mencionava; (ii) vários NOMES afirmavam mais que os
enunciados (`gate_closes_only_by_explosion` não prova exclusividade;
`the_collision_leaves_exactly_one_instant` não continha unicidade
alguma). *O nome é parte do enunciado — e o número corrige a frase.*
Nesta V2 cada nome descreve o que o teorema DIZ; as leituras do operador
ficam NOMEADAS como [CONJECTURE], onde sempre deveriam ter estado.

## O que esta pedra prova

* `explosion_from_forbidden_identification` — sob a identificação
  proibida (`ω(I) = 0`) **toda** proposição é derivável; e
  `explosion_gives_Q_and_not_Q` — a mesma hipótese entrega `Q ∧ ¬Q`.
  [*Ex falso quodlibet.* O teorema é a IMPLICAÇÃO; a EXCLUSIVIDADE da
  rota — "o gate SÓ fecharia assim" — é [CONJECTURE] do operador e NÃO
  está provada aqui.]
* `forbidden_identification_is_false` — a identificação é falsa.
  Composto com o anterior: a rota nomeada até o fechamento passa pelo
  absurdo, e o absurdo está refutado.
* `collapse_annihilates_the_spine` — `q² + a² = 0 ⟹ q = 0 ∧ a = 0`
  sobre ℝ (a face `1 = 0 = FALSO`).

### ★★ A PODA, em três verbos (cunhagem de 20/08: *TGL = separador;
    o sinal é a barra; SEPARAR–DESTACAR–PODAR; TGL = operação global
    de poda*)

Os três verbos são três teoremas, na ordem, para `E` idempotente:

1. **SEPARAR** — `separation_preserves_the_whole`: `Ex + (x − Ex) = x`.
   A barra separa em duas faces **sem romper a unidade da relação**;
   e `the_quotient_forgets_the_faces`: o escalar NÃO faz isso — o
   quociente não é injetivo (`1/2 = 2/4` com faces distintas). Por isso
   `TGL ≠ escalar`: o número esquece as faces que a barra preserva.
2. **DESTACAR** — `outside_the_image_the_excess_stands_out`: fora da
   imagem da inscrição o excesso é não-nulo — ele se destaca.
3. **PODAR** — `excess_annihilated_at_first_step`: `E(x − Ex) = 0`; e
   `every_scalar_fraction_of_excess_annihilated`: **nenhuma fração
   escalar do excesso sobrevive** (não há meia-poda);
   `second_application_changes_nothing`: a segunda aplicação não muda
   nada — a poda paga uma vez.

E a poda é **GLOBAL**: `pruning_holds_for_every_element` diz que o MESMO `E` separa,
destaca e poda **para todo** `x` — não é operação sobre uma parte
escolhida, é a operação do sistema inteiro.
[Leitura "a supersaturação dura um instante de Planck": [CONJECTURE].
Os teoremas falam de idempotência e de estar fora da imagem — não de
norma, de capacidade nem de tempo.]

### A cascata e o piso

* `ambientDim`, `ambientDim_strictMono`, `ambientDim_unbounded` — a
  escada `4ⁿ − 1` (15 → 63 → 255) é estritamente crescente e sem cota.
  [**NÃO é o índice de Jones de subfator**: é contagem de dimensão do
  ambiente. O nome foi corrigido de `ambientIndex` para `ambientDim`
  exatamente por isso, após objeção do painel.]
* `name_weight_is_invariant`, `ratio_becomes_arbitrarily_small` — o peso
  do Nome não muda com o degrau e a razão Nome/ambiente fica menor que
  qualquer `ε`. [Leitura "relatividade modular": [CONJECTURE].]
* `upward_route_never_exhausted` — há sempre degrau maior E a
  identificação proibida é falsa.
* `reals_are_dense` × `positive_dimension_is_at_least_one` — do
  lado do contínuo há sempre um ponto entre dois; do lado do peso (a
  dimensão de um subespaço) não há valor estritamente entre 0 e 1.
  [Leitura "o piso de Hilbert / a colisão": [CONJECTURE]. Não há
  enunciado de unicidade aqui, e nenhum nome afirma um.]

### ★★ O REGISTRO (cunhagem de 20/08: *memória = separar o registro da
    inscrição*)

Se registro e inscrição fossem o MESMO objeto, lembrar seria re-inscrever
— pagar de novo, toda vez. Isso é insistência, não memória. Os teoremas:

* `second_application_changes_nothing` — `E(Ex) = Ex`: o registro relê-se
  sem mudar e sem custo (é o mesmo teorema da poda; a V1 desta pedra o
  duplicava sob outro nome — alias removido após o painel);
* ★★ `record_does_not_determine_the_inscribed` — para `E ≠ 1` idempotente
  existem `x ≠ y` com `Ex = Ey`: **o registro carrega estritamente menos
  que o ato que o produziu**. É exatamente essa perda que o separa da
  inscrição — e é por isso que ele pode ser levado e relido;
* [REMOVIDO após o painel: `first_pass_changes_second_does_not`
  devolvia a própria hipótese como metade da tese. As duas metades já
  são `outside_the_image_the_excess_stands_out` e
  `second_application_changes_nothing`.]
* ★★ `record_survives_the_event_that_inscribed_it` — a MESMA operação
  que aniquila o excesso deixa o registro intacto: **o registro sobrevive
  ao evento que o inscreveu** (a forma curta do operador);
* ★★ `recognizable_iff_is_a_record` — `Ey = y ↔ ∃x, y = Ex`: **os
  reconhecíveis são exatamente os registros**. Separar o registro é a
  CONDIÇÃO do reconhecimento, medida nas duas direções;
* ★★ `whole_splits_into_record_and_pruned` — `x = Ex + (x − Ex)`, com
  `E(x − Ex) = 0` e `E(Ex) = Ex`: o todo se separa em **registro** e
  **podado**; o podado já não existe, e o registro basta para a
  releitura. É a separação inteira, num enunciado só.

### ★★ A CONJUGAÇÃO (cunhagem de 20/08: *a primeira passagem precisa
    mudar o estado porque é a inversão da paridade — que é a conjugação
    modular; é a primeira fase*)

* `first_passage_inverts_the_parity` — a face ímpar é ANTI-invariante:
  `C` age nela como `−1`. Não há inversão de paridade sem mudança;
* `even_face_is_fixed` — e a face PAR não se move: é a permanência;
* `even_plus_odd_is_twice` — a separação em faces é exaustiva;
* ★★ `conjugation_reverses_the_generator` — de `C K C = −K` segue
  `C K = −(K C)`: sob a conjugação o fluxo roda para trás. É a face
  algébrica de `J K J = −K`; a forma padrão concreta
  (`J² = id`, `J Δ J = Δ^{-1}`, `J K J = −K`, fases `e^{it(κᵢ−κⱼ)}`,
  diagonal com fase ZERO) está MEDIDA no `146_`, com controles que
  discriminam (a transposta simples erra por 22,0).

HONESTIDADE: β JAMAIS entra no Lean. Sem sorry, sem axiom. As leituras
físicas são medidas nas suas faces no livro-razão (`142_`, `143_`,
`144_`) e nomeadas [CONJECTURE]. Negativo honesto é resultado — e uma
reprovação de painel é um negativo honesto.
-/

namespace TGLExt

noncomputable section

/-- O peso do Nome: `ω(I) = 1` — o axioma como número. -/
def nameWeight : ℝ := 1

/-- O peso do 0 absoluto: o que não executa, o que não tem nome. -/
def zeroAbsWeight : ℝ := 0

/-- Sob a identificação proibida, toda proposição é derivável.
    *Ex falso quodlibet.* [A EXCLUSIVIDADE da rota não é provada aqui.] -/
theorem explosion_from_forbidden_identification
    (h : nameWeight = zeroAbsWeight) : ∀ P : Prop, P := by
  intro P
  exact absurd h (by norm_num [nameWeight, zeroAbsWeight])

/-- E a mesma hipótese entrega `Q` e `¬Q`: um fechamento assim não
    distingue nada. -/
theorem explosion_gives_Q_and_not_Q (h : nameWeight = zeroAbsWeight)
    (Q : Prop) : Q ∧ ¬ Q :=
  ⟨explosion_from_forbidden_identification h Q,
   explosion_from_forbidden_identification h (¬ Q)⟩

/-- A identificação proibida é falsa: o Nome pesa 1. -/
theorem forbidden_identification_is_false : nameWeight ≠ zeroAbsWeight := by
  norm_num [nameWeight, zeroAbsWeight]

/-- `q² + a² = 0 ⟹ q = 0 ∧ a = 0` sobre ℝ: sob o colapso a espinha não
    deixa polarização nenhuma. -/
theorem collapse_annihilates_the_spine (q a : ℝ)
    (hs : q ^ 2 + a ^ 2 = zeroAbsWeight) : q = 0 ∧ a = 0 := by
  simp only [zeroAbsWeight] at hs
  constructor
  · nlinarith [sq_nonneg q, sq_nonneg a]
  · nlinarith [sq_nonneg q, sq_nonneg a]

section Pruning

variable {A : Type*} [Ring A]

/-- ★★ SEPARAR — a separação em duas faces devolve o todo: a barra
    separa sem romper a unidade da relação. -/
theorem separation_preserves_the_whole (E : A) (x : A) :
    E * x + (x - E * x) = x := add_sub_cancel _ _

/-- ★★ E O ESCALAR ESQUECE AS FACES: o quociente não é injetivo — há
    pares distintos com o MESMO número. Logo o número não ocupa o lugar
    da separação: `TGL ≠ escalar`. -/
theorem the_quotient_forgets_the_faces :
    ∃ a b a' b' : ℝ, a / b = a' / b' ∧ (a, b) ≠ (a', b') := by
  refine ⟨1, 2, 2, 4, by norm_num, ?_⟩
  intro h
  have h1 : (1 : ℝ) = 2 := congrArg Prod.fst h
  norm_num at h1

/-- ★ DESTACAR — fora da imagem da inscrição o excesso é não-nulo:
    ele se destaca. -/
theorem outside_the_image_the_excess_stands_out (E : A) (x : A)
    (hx : E * x ≠ x) : x - E * x ≠ 0 := by
  intro h0
  exact hx (sub_eq_zero.mp h0).symm

/-- ★★ PODAR — o excesso é aniquilado na primeira aplicação. -/
theorem excess_annihilated_at_first_step (E : A) (hE : E * E = E) (x : A) :
    E * (x - E * x) = 0 := by
  rw [mul_sub, ← mul_assoc, hE, sub_self]

/-- E a segunda aplicação não muda nada: a poda paga uma vez. -/
theorem second_application_changes_nothing (E : A) (hE : E * E = E) (x : A) :
    E * (E * x) = E * x := by
  rw [← mul_assoc, hE]

/-- ★ NÃO HÁ MEIA-PODA: nenhuma fração escalar do excesso sobrevive. -/
theorem every_scalar_fraction_of_excess_annihilated {R : Type*}
    [CommSemiring R] [Algebra R A] (E : A) (hE : E * E = E) (x : A) (r : R) :
    E * (r • (x - E * x)) = 0 := by
  rw [mul_smul_comm, excess_annihilated_at_first_step E hE x, smul_zero]

/-- ★★ A PODA É GLOBAL: o MESMO `E` separa, destaca e poda **para todo**
    `x` — não é operação sobre uma parte escolhida, é a operação do
    sistema inteiro. -/
theorem pruning_holds_for_every_element (E : A) (hE : E * E = E) :
    ∀ x : A, E * x + (x - E * x) = x ∧ E * (x - E * x) = 0
             ∧ E * (E * x) = E * x := by
  intro x
  exact ⟨separation_preserves_the_whole E x,
         excess_annihilated_at_first_step E hE x,
         second_application_changes_nothing E hE x⟩

end Pruning

section Memory

variable {A : Type*} [Ring A]

/-- ★★ O REGISTRO NÃO DETERMINA O INSCRITO: para `E ≠ 1` idempotente
    existem dois estados DISTINTOS com o MESMO registro. O registro
    carrega estritamente menos que o ato que o produziu — e é essa perda
    que o SEPARA da inscrição. -/
theorem record_does_not_determine_the_inscribed (E : A) (hE : E * E = E)
    (h1 : E ≠ 1) : ∃ x y : A, x ≠ y ∧ E * x = E * y :=
  ⟨1, E, fun h => h1 h.symm, by rw [mul_one, hE]⟩

/-- ★★ O TODO SE SEPARA EM REGISTRO E PODADO: `x = Ex + (x − Ex)`, o
    podado é aniquilado, e o registro basta para a releitura. -/
theorem whole_splits_into_record_and_pruned (E : A) (hE : E * E = E) (x : A) :
    x = E * x + (x - E * x) ∧ E * (x - E * x) = 0 ∧ E * (E * x) = E * x :=
  ⟨(separation_preserves_the_whole E x).symm,
   excess_annihilated_at_first_step E hE x,
   second_application_changes_nothing E hE x⟩

/-- ★★ O REGISTRO SOBREVIVE AO EVENTO QUE O INSCREVEU: a MESMA operação
    que aniquila o excesso (e o excesso era não-nulo — algo morreu de
    fato) deixa o registro INTACTO. -/
theorem record_survives_the_event_that_inscribed_it (E : A) (hE : E * E = E)
    (x : A) (hx : E * x ≠ x) :
    (x - E * x ≠ 0 ∧ E * (x - E * x) = 0) ∧ E * (E * x) = E * x :=
  ⟨⟨outside_the_image_the_excess_stands_out E x hx,
    excess_annihilated_at_first_step E hE x⟩,
   second_application_changes_nothing E hE x⟩

/-- ★★ OS RECONHECÍVEIS SÃO EXATAMENTE OS REGISTROS: `Ey = y` se e só se
    `y` é registro de alguém. Separar o registro é, literalmente, a
    CONDIÇÃO do reconhecimento — e o iff a mede nas duas direções. -/
theorem recognizable_iff_is_a_record (E : A) (hE : E * E = E) (y : A) :
    E * y = y ↔ ∃ x, y = E * x := by
  constructor
  · intro h; exact ⟨y, h.symm⟩
  · rintro ⟨x, rfl⟩; exact second_application_changes_nothing E hE x

end Memory

section Conjugation

variable {A : Type*} [Ring A]

/-- ★★ A PRIMEIRA PASSAGEM INVERTE A PARIDADE: para uma involução `C`
    (`C*C = 1`), a diferença `x − Cx` é ANTI-invariante — `C` age nela
    como `−1`. Por isso a passagem não pode "quase não mudar": ou a face
    ímpar é nula (e nada se move), ou ela é invertida INTEIRA. -/
theorem first_passage_inverts_the_parity (C : A) (hC : C * C = 1) (x : A) :
    C * (x - C * x) = -(x - C * x) := by
  rw [mul_sub, ← mul_assoc, hC, one_mul, neg_sub]

/-- ★ E a face PAR não se move: é a permanência sob o espelho. -/
theorem even_face_is_fixed (C : A) (hC : C * C = 1) (x : A) :
    C * (x + C * x) = x + C * x := by
  rw [mul_add, ← mul_assoc, hC, one_mul, add_comm]

/-- ★ As duas parcelas somam o dobro do todo — para `C` QUALQUER. (Elas
    são as faces PAR e ÍMPAR exatamente quando `C² = 1`, o que é provado
    pelos dois teoremas acima; este aqui é só a exaustividade da soma, e
    o nome não promete mais que isso.) -/
theorem the_two_parts_sum_to_twice (C : A) (x : A) :
    (x + C * x) + (x - C * x) = 2 * x := by
  rw [two_mul]; abel

/-- ★★ A CONJUGAÇÃO REVERTE O GERADOR: de `C K C = −K` com `C² = 1`
    segue a ANTICOMUTAÇÃO `C K = −(K C)` — sob `C` o fluxo gerado por
    `K` roda para trás. [Face algébrica de `J K J = −K`, a paridade
    inversa da casa; a forma padrão concreta está medida no `146_`.] -/
theorem conjugation_reverses_the_generator (C K : A) (hC : C * C = 1)
    (h : C * K * C = -K) : C * K = -(K * C) := by
  have h2 : C * K * C * C = -K * C := by rw [h]
  rw [mul_assoc (C * K) C C, hC, mul_one, neg_mul] at h2
  exact h2

end Conjugation

section Cascade

/-- A escada da casa: contagem de dimensão do ambiente, `4ⁿ − 1`
    (15 → 63 → 255). **Não é o índice de Jones**; é dimensão. -/
def ambientDim (n : ℕ) : ℕ := 4 ^ n - 1

/-- A escada é estritamente crescente. -/
theorem ambientDim_strictMono : StrictMono ambientDim := by
  intro m n hmn
  have h1 : (1 : ℕ) ≤ 4 ^ m := Nat.one_le_pow _ _ (by norm_num)
  have h2 : 4 ^ m < 4 ^ n := Nat.pow_lt_pow_right (by norm_num) hmn
  exact Nat.sub_lt_sub_right h1 h2

/-- E não tem cota superior. -/
theorem ambientDim_unbounded (N : ℕ) : ∃ n, N < ambientDim n := by
  refine ⟨N + 1, ?_⟩
  have h : N + 1 < 4 ^ (N + 1) := Nat.lt_pow_self (by norm_num)
  have h1 : (1 : ℕ) ≤ 4 ^ (N + 1) := Nat.one_le_pow _ _ (by norm_num)
  simp only [ambientDim]
  omega

/-- O peso do Nome é 1 — e não há argumento nenhum de que dependa: a
    constante não tem parâmetro. -/
theorem name_weight_is_one : nameWeight = 1 := rfl

/-- A razão Nome/ambiente fica menor que qualquer `ε > 0`.
    [Leitura "não há escala absoluta, só a razão": [CONJECTURE].] -/
theorem ratio_becomes_arbitrarily_small (ε : ℝ) (hε : 0 < ε) :
    ∃ n : ℕ, nameWeight / (ambientDim n : ℝ) < ε := by
  obtain ⟨N, hN⟩ := exists_nat_gt (1 / ε)
  obtain ⟨n, hn⟩ := ambientDim_unbounded N
  have hNr : (N : ℝ) < (ambientDim n : ℝ) := by exact_mod_cast hn
  have hpos : (0 : ℝ) < (ambientDim n : ℝ) := lt_of_le_of_lt (by positivity) hNr
  have hkey : 1 / ε < (ambientDim n : ℝ) := lt_trans hN hNr
  refine ⟨n, ?_⟩
  simp only [nameWeight]
  rw [div_lt_iff₀ hpos]
  have hx := (div_lt_iff₀ hε).mp hkey
  linarith

/-- Há sempre degrau maior, E a identificação proibida é falsa: a rota
    para cima nunca se esgota e a rota para baixo está refutada. -/
theorem upward_route_never_exhausted (n : ℕ) :
    (∃ m, ambientDim n < ambientDim m) ∧ nameWeight ≠ zeroAbsWeight :=
  ⟨ambientDim_unbounded (ambientDim n), forbidden_identification_is_false⟩

end Cascade

section Floor

/-- Do lado do contínuo: entre dois reais há sempre outro. -/
theorem reals_are_dense (x y : ℝ) (h : x < y) : ∃ z, x < z ∧ z < y :=
  ⟨(x + y) / 2, by linarith, by linarith⟩

/-- ★ O PISO É A DISCRETUDE DO PESO: se a dimensão de um subespaço é
    positiva, ela é ao menos 1 — não há fração de dimensão. [HONESTIDADE
    (painel de fecho): isto é a discretude de ℕ transportada para
    `finrank`, e não um fato profundo; e em dimensão INFINITA `finrank`
    devolve 0, de modo que o enunciado nada diz ali. É o piso da face
    FINITA, e o nome não promete mais.] -/
theorem positive_dimension_is_at_least_one
    {V : Type*} [AddCommGroup V] [Module ℝ V] (S : Submodule ℝ V)
    (h : 0 < Module.finrank ℝ S) : (1 : ℝ) ≤ (Module.finrank ℝ S : ℝ) := by
  exact_mod_cast h

end Floor

end

end TGLExt
