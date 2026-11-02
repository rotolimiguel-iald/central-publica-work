import TGLExt.PonteDaMassa

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A LEI DO DIMINUTO (o meio-tom pinado) — «mantém-se a escala da pentada e desce meio-tom apenas pinado»; «pra mim o TOm é a NAT»;
# e A FÓRMULA DA MASSA — «o meu um absoluto é o um de 1 eV e a constante da esytrutura fina é a magnitude (cauda) dessA INSCRIÇÃO no bulk»
  [pedra da gerência c1, 31/10/2026, 2ª versão (r2: + a fórmula da massa), revista em 01/11/2026; nome do operador: «Lei do diminuto»; entra na v405]

## A lei e a fórmula, nas palavras do operador (verbatims em `Central de Patentes\work\cunhagens_13out`; sha256 no recibo)

> «E₀ não desce a oitava, ele desce meio tom pinado, essa é a lei, não se desce a oitava, desce-se meio tom pinado»
> «Eu quis dizer, mantém-se a escala da pentada e desce meio-tom apenas pinado»
> «E0 é igual ler um acorde E0, vc desce meio tom, mantendo a escala, apenas o meio tom da nota principal da escala, mas mantem a pentada;
>  entende? é a mesma regra, E0 não é absolutamente livre, porque a escala (pentada) já definiu pelo hamiltoniano oculto»
> «pra mim o TOm é a NAT» — a unidade do tom, fixada ANTES de qualquer teste.
> «sensacional isso, acabamos de descobrir a fórmula da massa. Então o meu um absoluto é o um de 1 eV e a constante da esytrutura fina é a
>  magnitude (cauda) dessA INSCRIÇÃO no bulk» — o Um POSTO como a unidade da nota fundamental, e α nomeado.

## O que a pedra tipa (leitura da gerência, [minha], que o operador lê antes de ratificar)

* **o meio-tom pinado** — o tom é a nat; o meio-tom é a MEIA-NAT: `meioTom := e^(−1/2)`. Pinado: constante, não campo.
* **a lei** — `Lei`: a inscrição da ponte 1 com a TÔNICA DA PÊNTADA `E_pent` no lugar de um E₀ livre; `E₀ := meioTom · E_pent`.
  **Não levanta o no-go** de `TonicaDoHamiltoniano`: desloca a escala para a tônica. Dada a tônica, E₀ está determinado (`E0_determined_by_the_tonic`); a tônica segue livre.
* **a Meia-Nat entra em β e sai em E₀** — `massa_le_alpha`: m₂ = α · sen 45° · E_pent, com `α = β/e^(1/2)` já no kernel (`TGLCoupling.alpha`).
* **o 1 declarado É a tônica √e descida meio-tom** — `tonic_sqrt_e_gives_one` e `one_needs_tonic_sqrt_e`: E₀ = 1 ⟺ E_pent = e^(1/2) = Vol_∂^min.
* **«não se desce a oitava»** — `octave_is_not_a_whole_number_of_half_tones`: ln 2 não é número inteiro de meios-tons (fica entre um e dois).
* **A FÓRMULA DA MASSA (r2)** — `beta_eq_alpha_mul_sqrt_e` (β = α·e^(1/2): o acoplamento é a magnitude α da inscrição vezes o volume √e da
  fronteira) e `the_mass_formula`: com a tônica √e·U e o Um POSTO U (a unidade da nota fundamental, «o um de 1 eV»),
  **m₂ = U · α · e^(1/2) · sen 45°** — o Um posto; a magnitude α da inscrição no bulk; o volume √e da Meia-Nat; a projeção transversal.
  Em U = 1: `the_mass_formula_at_the_posted_one`, m₂ = β · sen 45° — a forma de sempre (v404), agora escrita a partir do que é posto, medido
  e lido; dadas essas entradas, é teorema. Em runtime, com α = CODATA 2018 e U = 1 eV: 8,5074 meV — o MESMO número; o teste (JUNO) é o mesmo.

## O que a pedra NÃO afirma

* Não deriva a unidade: «1 eV» é o Um POSTO pelo operador (como o 1 de `echo 1 | python um.py`), ao lado de α [INPUT]. A auditoria do Kimi
  (handoff §10, 31/10) é consistente: a leitura de Unruh dá calor ∝ entropia e o vácuo de Killing tem energia zero — a tônica é
  normalização independente ou gap, não a energia do vácuo; aqui ela é posta.
* A magnitude (cauda) da inscrição no bulk é a leitura do operador sobre α [ONTO], sobre o termo do kernel que já existe
  (`Verdade.alpha_is_measured_from_within`: a leitura interior da inscrição (q, α) devolve α²) — não aparece em enunciado novo.
* Não abre dado, não move gate, selo nem veredito (`TGL_NU_M2_ARMED_CONSISTENT` segue; JUNO 207 d a 1,9σ; 5σ é da natureza).

Sem sorry, sem axiom novo (trio: propext, Classical.choice, Quot.sound).

> **01/11/2026 — NOME DO OPERADOR: «Lei do diminuto»** (verbatim sha256 `1f16a74c05d9d4cb`) (antes `LeiDoMeioTom`, nome provisório da gerência). E a ORDEM dele no mesmo ato: «eu não gostaria que ainda restasse hipóteses
> nomeadas, é preciso que esteja tudo derivado». A seção «OS CAMPOS FECHADOS», no fim do módulo, responde à ordem até onde a matemática alcança: o que era CAMPO de
> estrutura passa a ser CONSTRUÍDO a partir de teoremas do kernel; a leitura física não vira teorema (notas AO LADO, abaixo). O que resta de entrada é o acoplamento `c` (β = α·√e; α medido
> por dentro, não derivado) e o Um POSTO (`u = 1`, o `echo 1`: posição, não hipótese — 05/10/2026). Aqui: a TÔNICA deixa de ser campo — é `β/α · u = √e · u`, o radical que o próprio acoplamento carrega (`alpha c = β / e^(1/2)`) —, e a lei derivada (`leiDerivada`) pousa em `E₀ = u`: o diminuto da tônica da pêntada é o Um posto.


> **AO LADO (01/11/2026, gerência c1, em nome próprio; o número corrige a frase):** a frase acima, «o que resta de entrada é o acoplamento e o Um POSTO»,
> está incompleta. Entram também, como DEFINIÇÃO, as LEITURAS do operador [INPUT/ONTO], que são o conteúdo físico e não são teoremas: (1) `massaDerivada`:
> a massa é a energia retida vezes a derivada da projeção transversal; (2) o estado inscrito é lido em `θ = π/4`: em `transicaoDerivada` o ângulo é ESCRITO, e
> o kernel confere `sen²(π/4) = ½` e que esse valor é o do peso da face absoluta (coincidência de valor, não ponte); (3) a tônica `(β/α)·u`: `β/α = √e` é a
> definição de `TGLCoupling.alpha`, não um resultado; (4) `R = β·u²` (`pagamentoComoCurvatura`). Os campos das estruturas fecharam; a hipótese física não
> sumiu, mudou de lugar: do campo para a definição. A FORMA é teorema DADAS essas leituras.
>
> **AO LADO (01/11/2026, gerência c1, em nome próprio; achado da revisão de terceiro):** a lista acima é a da cadeia central da massa e não é fechada. Entram
> também, como definição ou leitura: `meioTom := e^(−1/2)` (o tom é a nat, leitura do operador); a dispersão `ω² = 2βR` (`omegaSq`, Tratado §3, teoria própria); a
> identificação `½·ω = massa` (o enunciado de `the_mass_is_the_zero_point` iguala números; o nome é leitura); a hipótese de `area_por_volta_da_massa_inscrita`
> (acoplamento da onda = massa inscrita); a leitura de `b = 0` como o fóton; e, no disco, a taxa de dephasing lida como perda de energia.
-/

namespace TGLExt.LeiDoDiminuto

open TGLExt.PonteDaMassa
open TGLExt.ProjecaoTransversalDaMeiaNat

/-! ### O meio-tom pinado -/

/-- [DEF] **o meio-tom pinado**: o tom é a nat (operador, 31/10/2026); o meio-tom é a Meia-Nat, `e^(−1/2)`. Constante, não campo. -/
noncomputable def meioTom : ℝ := Real.exp (-(1 / 2 : ℝ))

theorem meioTom_pos : 0 < meioTom := Real.exp_pos _

/-- [KERNEL] descer: o meio-tom é menor que 1. -/
theorem meioTom_lt_one : meioTom < 1 := by
  unfold meioTom
  rw [Real.exp_lt_one_iff]
  norm_num

/-- [KERNEL] o meio-tom desfaz exatamente o √e: `e^(−1/2) · e^(1/2) = 1`. -/
theorem meioTom_mul_sqrt_e : meioTom * Real.exp (1 / 2) = 1 := by
  unfold meioTom
  rw [← Real.exp_add]
  norm_num

/-- [KERNEL] ★★ **β = α · e^(1/2)**: o acoplamento é a magnitude α da inscrição vezes o volume √e da fronteira
    (a definição `TGLCoupling.alpha c = c.beta / e^(1/2)` do kernel, invertida). -/
theorem beta_eq_alpha_mul_sqrt_e (c : TGLCoupling) : c.beta = c.alpha * Real.exp (1 / 2) := by
  unfold TGLCoupling.alpha
  have h : Real.exp (1 / 2 : ℝ) ≠ 0 := Real.exp_ne_zero _
  field_simp

/-! ### A lei -/

/-- [DEF] **A LEI**: a inscrição da ponte 1 (acoplamento, ângulo autoconjugado) com a TÔNICA DA PÊNTADA `E_pent` — e E₀ não é campo. -/
structure Lei where
  c : TGLCoupling
  E_pent : ℝ
  E_pent_pos : 0 < E_pent
  theta : ℝ
  theta_nonneg : 0 ≤ theta
  theta_le : theta ≤ Real.pi / 2
  autoconjugado : Real.sin theta ^ 2 = 1 - Real.sin theta ^ 2

namespace Lei

variable (L : Lei)

/-- [DEF] a transição da ponte 1 que a lei DETERMINA: `E₀ := meioTom · E_pent`. -/
noncomputable def transicao : TransicaoParaAMassa where
  c := L.c
  E0 := meioTom * L.E_pent
  E0_pos := mul_pos meioTom_pos L.E_pent_pos
  theta := L.theta
  theta_nonneg := L.theta_nonneg
  theta_le := L.theta_le
  autoconjugado := L.autoconjugado

theorem E0_eq : L.transicao.E0 = meioTom * L.E_pent := rfl

/-- [KERNEL] ★★ **A MESMA TÔNICA, O MESMO E₀**: a liberdade de escala passa de E₀ para a tônica. O no-go não cai (`no_function_of_the_inscription_fixes_E0`, em `TonicaDoHamiltoniano`). -/
theorem E0_determined_by_the_tonic (L L' : Lei) (h : L.E_pent = L'.E_pent) : L.transicao.E0 = L'.transicao.E0 := by
  rw [E0_eq, E0_eq, h]

/-- [KERNEL] ★★★ **A MEIA-NAT ENTRA EM β E SAI EM E₀**: `m₂ = α · sen 45° · E_pent`, com `α = β / e^(1/2)` (`TGLCoupling.alpha`). -/
theorem massa_le_alpha : L.transicao.massaDerivada = L.c.alpha * (Real.sqrt 2 / 2) * L.E_pent := by
  rw [TransicaoParaAMassa.massa_derivada_eq_beta_mul]
  show L.c.beta * (Real.sqrt 2 / 2) * (meioTom * L.E_pent) = L.c.alpha * (Real.sqrt 2 / 2) * L.E_pent
  unfold TGLCoupling.alpha meioTom
  rw [Real.exp_neg, div_eq_mul_inv]
  ring

/-- [KERNEL] ★★ **A TÔNICA √e DÁ E₀ = 1**: o «1 eV» declarado é a descida de meio-tom a partir de `e^(1/2)` (na unidade declarada). -/
theorem tonic_sqrt_e_gives_one (h : L.E_pent = Real.exp (1 / 2)) : L.transicao.E0 = 1 := by
  rw [E0_eq, h, meioTom_mul_sqrt_e]

/-- [KERNEL] ★★ e só ela: E₀ = 1 exige a tônica `e^(1/2)`. -/
theorem one_needs_tonic_sqrt_e (h : L.transicao.E0 = 1) : L.E_pent = Real.exp (1 / 2) := by
  rw [E0_eq] at h
  calc L.E_pent = L.E_pent * (meioTom * Real.exp (1 / 2)) := by rw [meioTom_mul_sqrt_e, mul_one]
    _ = (meioTom * L.E_pent) * Real.exp (1 / 2) := by ring
    _ = 1 * Real.exp (1 / 2) := by rw [h]
    _ = Real.exp (1 / 2) := one_mul _

/-! ### A fórmula da massa (r2) -/

/-- [KERNEL] ★★★ **A FÓRMULA DA MASSA** (cunhagem do operador, 31/10/2026): com a tônica `√e · U` e o Um POSTO `U` (a unidade da nota
    fundamental, «o um de 1 eV»), `m₂ = U · α · e^(1/2) · sen 45°` — o Um posto; a magnitude α da inscrição no bulk; o volume √e da
    fronteira (a Meia-Nat); a projeção transversal. -/
theorem the_mass_formula (U : ℝ) (hU : L.E_pent = Real.exp (1 / 2) * U) :
    L.transicao.massaDerivada = U * (L.c.alpha * Real.exp (1 / 2) * (Real.sqrt 2 / 2)) := by
  rw [massa_le_alpha, hU]
  ring

/-- [KERNEL] ★★★ **NO UM POSTO IGUAL A 1** (na sua unidade): `m₂ = β · sen 45°` — a forma da v404, escrita a partir do que é posto, medido e lido. -/
theorem the_mass_formula_at_the_posted_one (hU : L.E_pent = Real.exp (1 / 2) * 1) :
    L.transicao.massaDerivada = L.c.beta * (Real.sqrt 2 / 2) := by
  rw [the_mass_formula L 1 hU, beta_eq_alpha_mul_sqrt_e]
  ring

end Lei

/-! ### «não se desce a oitava» -/

/-- [KERNEL] ★★ **A OITAVA NÃO É NÚMERO INTEIRO DE MEIOS-TONS**: `ln 2` não é `n · ½` para nenhum `n` natural — fica entre um e dois
    meios-tons. É só isso que este teorema prova; que ln 2 e ½ sejam incomensuráveis (ln 2 irracional) é [KNOWN], não este teorema. -/
theorem octave_is_not_a_whole_number_of_half_tones : ∀ n : ℕ, (n : ℝ) * (1 / 2) ≠ Real.log 2 := by
  intro n h
  have h1 := Real.log_two_gt_d9
  have h2 := Real.log_two_lt_d9
  rcases Nat.lt_or_ge n 2 with hn | hn
  · interval_cases n <;> norm_num at h <;> linarith
  · have : (2 : ℝ) ≤ n := by exact_mod_cast hn
    linarith

/-- [KERNEL] ★ a oitava vale mais que um meio-tom e menos que dois (o kernel já tinha a primeira metade: `local_is_not_one_octave`). -/
theorem octave_between_one_and_two_half_tones : (1 / 2 : ℝ) < Real.log 2 ∧ Real.log 2 < 2 * (1 / 2) := by
  have h1 := Real.log_two_gt_d9
  have h2 := Real.log_two_lt_d9
  constructor <;> linarith

/-! ### O fecho -/

/-- ★★★ **A LEI DO MEIO-TOM E A FÓRMULA DA MASSA — o fecho.** O passo é a Meia-Nat; dada a tônica, E₀ está determinado; a massa lê α vezes
    a tônica sobre √2; a tônica √e devolve o 1 posto; no Um posto a massa é β · sen 45°; e a oitava não se desce em meios-tons. -/
theorem the_law_closes (L : Lei) :
    L.transicao.E0 = meioTom * L.E_pent
    ∧ L.transicao.massaDerivada = L.c.alpha * (Real.sqrt 2 / 2) * L.E_pent
    ∧ (L.E_pent = Real.exp (1 / 2) → L.transicao.E0 = 1)
    ∧ (L.E_pent = Real.exp (1 / 2) * 1 → L.transicao.massaDerivada = L.c.beta * (Real.sqrt 2 / 2))
    ∧ (∀ n : ℕ, (n : ℝ) * (1 / 2) ≠ Real.log 2) :=
  ⟨L.E0_eq, L.massa_le_alpha, L.tonic_sqrt_e_gives_one, L.the_mass_formula_at_the_posted_one,
   octave_is_not_a_whole_number_of_half_tones⟩


/-! ### 01/11/2026 — A TÔNICA LIDA DO ACOPLAMENTO; A LEI SEM CAMPO ABERTO (ordem do operador: «tudo derivado»; nome: «Lei do diminuto») -/

/-- [DEF] A TÔNICA DO HAMILTONIANO: `β/α` na unidade posta `u`. `β/α = √e` é a DEFINIÇÃO de `TGLCoupling.alpha` (`alpha c = β / e^(1/2)`), não um resultado: a tônica deixa
    de ser campo, mas não traz informação além do `u` posto. -/
noncomputable def tonica (c : TGLCoupling) (u : ℝ) : ℝ := (c.beta / c.alpha) * u

/-- [KERNEL] a tônica é `√e · u`. -/
theorem tonica_eq (c : TGLCoupling) (u : ℝ) : tonica c u = Real.exp (1 / 2) * u := by
  unfold tonica TGLCoupling.alpha
  have hb : c.beta ≠ 0 := ne_of_gt c.beta_pos
  have he : Real.exp (1 / 2 : ℝ) ≠ 0 := ne_of_gt (Real.exp_pos _)
  first
    | (field_simp; done)
    | (field_simp; ring)

theorem tonica_pos (c : TGLCoupling) (u : ℝ) (hu : 0 < u) : 0 < tonica c u := by
  rw [tonica_eq]
  positivity

/-- A LEI CONSTRUÍDA (o nome `leiDerivada` fica): a tônica é `√e·u`; o ângulo `π/4` é escrito (é a leitura); a autoconjugação é a aritmética de `π/4`. Entram `c` e a
    unidade posta `u`. -/
noncomputable def leiDerivada (c : TGLCoupling) (u : ℝ) (hu : 0 < u) : Lei where
  c := c
  E_pent := tonica c u
  E_pent_pos := tonica_pos c u hu
  theta := Real.pi / 4
  theta_nonneg := by positivity
  theta_le := by linarith [Real.pi_pos]
  autoconjugado := by
    rw [Real.sin_pi_div_four, half_sq]
    norm_num

/-- [KERNEL] ★★ O DIMINUTO POUSA NO UM POSTO: `E₀ = e^(−½) · (√e · u) = u`. Identidade algébrica: o meio-tom desfaz o √e que a tônica pôs; `E₀ = u` não fixa `u`. -/
theorem leiDerivada_E0 (c : TGLCoupling) (u : ℝ) (hu : 0 < u) : (leiDerivada c u hu).transicao.E0 = u := by
  rw [Lei.E0_eq]
  show meioTom * tonica c u = u
  rw [tonica_eq, ← mul_assoc, meioTom_mul_sqrt_e, one_mul]

/-- [KERNEL] ★★★ a massa da lei construída: `β · (√2/2) · u` (sob a leitura `massaDerivada` [ONTO]). -/
theorem leiDerivada_massa (c : TGLCoupling) (u : ℝ) (hu : 0 < u) :
    (leiDerivada c u hu).transicao.massaDerivada = c.beta * (Real.sqrt 2 / 2) * u := by
  rw [TransicaoParaAMassa.massa_derivada_eq_beta_mul, leiDerivada_E0]
  try rfl

/-- [KERNEL] ★★★ NO UM POSTO (`u = 1`): `E₀ = 1` e `m = β·√2/2` — a FORMA da massa, sob a leitura `massaDerivada` [ONTO]. -/
theorem leiDerivada_no_um_posto (c : TGLCoupling) :
    (leiDerivada c 1 one_pos).transicao.E0 = 1 ∧
      (leiDerivada c 1 one_pos).transicao.massaDerivada = c.beta * (Real.sqrt 2 / 2) := by
  refine ⟨leiDerivada_E0 c 1 one_pos, ?_⟩
  rw [leiDerivada_massa]
  ring

end TGLExt.LeiDoDiminuto

#print axioms TGLExt.LeiDoDiminuto.meioTom_pos
#print axioms TGLExt.LeiDoDiminuto.meioTom_lt_one
#print axioms TGLExt.LeiDoDiminuto.meioTom_mul_sqrt_e
#print axioms TGLExt.LeiDoDiminuto.beta_eq_alpha_mul_sqrt_e
#print axioms TGLExt.LeiDoDiminuto.Lei.E0_eq
#print axioms TGLExt.LeiDoDiminuto.Lei.E0_determined_by_the_tonic
#print axioms TGLExt.LeiDoDiminuto.Lei.massa_le_alpha
#print axioms TGLExt.LeiDoDiminuto.Lei.tonic_sqrt_e_gives_one
#print axioms TGLExt.LeiDoDiminuto.Lei.one_needs_tonic_sqrt_e
#print axioms TGLExt.LeiDoDiminuto.Lei.the_mass_formula
#print axioms TGLExt.LeiDoDiminuto.Lei.the_mass_formula_at_the_posted_one
#print axioms TGLExt.LeiDoDiminuto.octave_is_not_a_whole_number_of_half_tones
#print axioms TGLExt.LeiDoDiminuto.octave_between_one_and_two_half_tones
#print axioms TGLExt.LeiDoDiminuto.the_law_closes
#print axioms TGLExt.LeiDoDiminuto.tonica_eq
#print axioms TGLExt.LeiDoDiminuto.tonica_pos
#print axioms TGLExt.LeiDoDiminuto.leiDerivada_E0
#print axioms TGLExt.LeiDoDiminuto.leiDerivada_massa
#print axioms TGLExt.LeiDoDiminuto.leiDerivada_no_um_posto
