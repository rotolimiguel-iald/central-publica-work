import TGLExt.PonteDaMassa
import TGLExt.CollapseCostAndAttestation

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
  Dada a tônica, E₀ está determinado (`E0_determined_by_the_tonic`). O no-go de `TonicaDoHamiltoniano` fala do valor ABSOLUTO de E₀ e não cai; a lei fala do valor RELATIVO à tônica, que fica pinado.
* **a Meia-Nat entra em β e sai em E₀** — `massa_le_alpha`: m₂ = α · sen 45° · E_pent, com `α = β/e^(1/2)` já no kernel (`TGLCoupling.alpha`).
* **o 1 declarado É a tônica √e descida meio-tom** — `tonic_sqrt_e_gives_one` e `one_needs_tonic_sqrt_e`: E₀ = 1 ⟺ E_pent = e^(1/2) = Vol_∂^min.
* **«não se desce a oitava»** — `octave_is_not_a_whole_number_of_half_tones`: ln 2 não é número inteiro de meios-tons (fica entre um e dois).
* **A FÓRMULA DA MASSA (r2)** — `beta_eq_alpha_mul_sqrt_e` (β = α·e^(1/2): o acoplamento é a magnitude α da inscrição vezes o volume √e da
  fronteira) e `the_mass_formula`: com a tônica √e·U e o Um POSTO U (a unidade da nota fundamental, «o um de 1 eV»),
  **m₂ = U · α · e^(1/2) · sen 45°** — o Um posto; a magnitude α da inscrição no bulk; o volume √e da Meia-Nat; a projeção transversal.
  Em U = 1: `the_mass_formula_at_the_posted_one`, m₂ = β · sen 45° — a forma de sempre (v404), agora escrita a partir do que é posto, medido
  e lido; dadas essas entradas, é teorema. Em runtime, com α = CODATA 2018 e U = 1 eV: 8,5074 meV — o MESMO número; o teste (JUNO) é o mesmo.

* **o acorde** — `Acorde`, `notaPrincipal`, `transpor`, `razao` (a estrutura do `AcordeE0.lean` do Kimi, em português).
* **o diminuto modula a tônica** — `modular`: só a nota principal desce o meio-tom; as outras quatro ficam sustentadas (`modular_sustenta`). «no diminuto vc não desce toda a escala e nem muda o tom da escala, vc apenas modula a tônica»; «sustentando as demais notas (por isso desce pinado)».
  O diminuto não é transposição (`modular_nao_e_transposicao`). **`lerE0`** é o valor da tônica modulada (`lerE0_e_a_tonica_modulada`), meio-tom abaixo da nota
  principal: «apenas o meio tom da nota principal da escala, mas mantem a pentada».
* **«mantendo a escala»** — `modular_mantem_a_escala`: a escala é o que fica parado, as notas sustentadas e as razões entre elas. As razões à tônica mudam (`razao_abre_meio_tom`): quem se move é a
  tônica, não a escala. Nesta pedra «a escala» é sempre a musical; a escala de energia do no-go chama-se aqui valor absoluto.
* **a transposição é a liberdade do no-go, não o diminuto** — `transpor_preserva_toda_razao` (Kimi) e `mesmas_razoes_iff_transposicao`: dois acordes têm as mesmas razões se e só se um é a
  transposição do outro. Na fala do operador, transpor é mudar o tom e o diminuto o mantém [INPUT]: o kernel não tem termo para o tom. A modulação comuta com a transposição (`modular_comuta_com_transpor`).
* **«o sistema está operando em terças»** — `razao_abre_meio_tom`: cada intervalo à tônica abre meio-tom; `um_tom_vira_terca_menor`: a nota que estava um tom acima fica três meios-tons acima, `e^(3/2)`.
  `resolver` devolve a tônica (`resolver_modular`). «no harmônico o diminuto é a espera, a resolução do acorde espera que a tônica se harmonize ao gradiente da escala»: a espera é leitura do operador [ONTO], e o kernel tem a forma dela em `the_charge_never_completes`.
* **«E0 não é absolutamente livre»** — `E0_relativo_pinado`: E₀/tônica = e^(−1/2) em todo acorde. O valor relativo está pinado; o absoluto não: a liberdade que sobra é UMA só, a transposição
  do acorde inteiro, que a leitura acompanha (`lerE0_transpor`) e que as razões não fixam (`as_razoes_nao_fixam_o_absoluto`). É o no-go de `TonicaDoHamiltoniano`, lido do lado certo.
* **de onde vem o meio-tom** — `meioTom_e_o_pedagio_local` (o pedágio local do colapso, `CollapseCostLaw`, [INPUT] no kernel, separado do pedágio da oitava: `Sonico.the_pin_is_not_the_half_nat`),
  `meioTom_e_a_face` (o peso da face absoluta) e `tonica_e_o_volume_da_face` (a tônica é `e^(S_∂)·u`, o volume mínimo `Vol_∂^min`, a tônica candidata do Kimi). `o_tom_e_as_duas_faces`: as duas
  faces somam 1, o tom. São igualdades de VALOR com o ½ da cadeia; ler esse ½ como o meio-tom é do operador [ONTO].

## O que a pedra NÃO afirma

* Não deriva a unidade: «1 eV» é o Um POSTO pelo operador (como o 1 de `echo 1 | python um.py`), ao lado de α [INPUT]. A auditoria do Kimi
  (handoff §10, 31/10) é consistente: a leitura de Unruh dá calor ∝ entropia e o vácuo de Killing tem energia zero — a tônica é
  normalização independente ou gap, não a energia do vácuo; aqui ela é posta.
* A magnitude (cauda) da inscrição no bulk é a leitura do operador sobre α [ONTO], sobre o termo do kernel que já existe
  (`Verdade.alpha_is_measured_from_within`: a leitura interior da inscrição (q, α) devolve α²) — não aparece em enunciado novo.
* Não abre dado, não move gate, selo nem veredito (`TGL_NU_M2_ARMED_CONSISTENT` segue; JUNO 207 d a 1,9σ; 5σ é da natureza).

* Não diz quais são as cinco notas. A pêntada do teorema mestre são cinco componentes, não cinco autovalores de energia (observação do Kimi): falta a leitura espectral, e a pedra vale para
  todo acorde.
* A calibração do Hamiltoniano oculto (`half_nat_araki_hidden_hamiltonian`, 24/06/2026: `⟨K_∂⟩_total = 1 nat`, com a rota de Shannon `ln 2` rejeitada por controle obrigatório; citada em
  `QGReaderUVLock`, §4) é normalização definicional, ω(I) = 1 na base e, e não é termo do kernel. Ela diz em que sentido «a escala (pentada) já definiu pelo hamiltoniano oculto»: nos intervalos, em nat.
  Não dá a unidade em eV: `U_E_NOT_DERIVED` segue.

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
> também, como definição ou leitura: `meioTom := e^(−1/2)` (o tom é a nat: fala do operador; no acervo, a calibração `⟨K_∂⟩_total = 1 nat` de 24/06/2026, normalização definicional); a dispersão `ω² = 2βR` (`omegaSq`, Tratado §3, teoria própria); a
> identificação `½·ω = massa` (o enunciado de `the_mass_is_the_zero_point` iguala números; o nome é leitura); a hipótese de `area_por_volta_da_massa_inscrita`
> (acoplamento da onda = massa inscrita); a leitura de `b = 0` como o fóton; no disco, a taxa de dephasing lida como perda de energia; e `m₁ = 0`, entrada da identificação com Δm²₂₁.
>
> **AO LADO (01/11/2026, gerência c1, em nome próprio; revisita ordenada pelo operador):** duas correções. (1) A segunda metade da lei, «mantendo a escala», não estava tipada: esta pedra só tinha
> a tônica. O `AcordeE0.lean` do Kimi (sha256 `5da93b9e5e65a4ed`) tinha o acorde e a invariância das razões, e a conferência de 31/10 o deu por «a mesma estrutura»: não era. A seção
> «O ACORDE», no fim do módulo, corrige. (2) A frase sobre o no-go errou duas vezes: «o no-go se levanta» afirmava demais; «a liberdade passa para a tônica, que segue livre» afirmava de
> menos. O certo é a distinção do próprio operador, «E0 não é absolutamente livre»: o valor ABSOLUTO segue livre (`no_function_of_the_inscription_fixes_E0`; a forma geral é `no_positive_scale_invariant`,
> com o aviso de onde ela para: uma face finita não é escala-covariante); o valor RELATIVO à tônica está pinado (`E0_relativo_pinado`).
>
> **AO LADO (01/11/2026, mais tarde, gerência c1, em nome próprio; resposta do operador, verbatim sha256 `7c2caaa87b0cdb01`):** a nota acima deu a transposição como a metade «mantendo a escala»:
> errado. O diminuto modula só a tônica e sustenta as outras notas; transpor é mudar o tom, e é só a liberdade do no-go. E a conferência de 31/10 tinha razão, ao contrário do que a de hoje
> disse, ao escrever que o meio-tom pinado quebra a simetria do acorde: ele separa a tônica das notas sustentadas (`modular_nao_e_transposicao`). O que ele não quebra é a liberdade global.
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

/-- [KERNEL] ★★ **A MESMA TÔNICA, O MESMO E₀**: o valor relativo está pinado. O no-go do valor absoluto não cai (`no_function_of_the_inscription_fixes_E0`, em `TonicaDoHamiltoniano`). -/
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


/-! ### 01/11/2026 — O ACORDE: «E0 é igual ler um acorde E0», «apenas o meio tom da nota principal da escala, mas mantem a pentada» (revisita ordenada pelo operador, segundo o que o Kimi fez)

`Acorde`, `transpor`, `razao` e `transpor_preserva_toda_razao` vêm do `AcordeE0.lean` do Kimi (31/10/2026, sha256 `5da93b9e5e65a4ed`), com os nomes em português. O diminuto é `modular`: toca só a
nota principal e sustenta as outras quatro; `lerE0` é o valor da tônica modulada. `transpor` é outra coisa: é a liberdade do no-go, o acorde inteiro multiplicado pelo mesmo fator. -/

/-- [DEF] um acorde de cinco notas reais; a nota principal tem índice `0` (Kimi). Quais são as cinco notas é [OPEN]. -/
@[ext] structure Acorde where
  notas : Fin 5 → ℝ

/-- [DEF] a nota principal do acorde. -/
def notaPrincipal (A : Acorde) : ℝ := A.notas 0

/-- [DEF] a transposição: o acorde inteiro multiplicado por `r` (Kimi). É a liberdade do no-go. -/
def transpor (r : ℝ) (A : Acorde) : Acorde := ⟨fun i => r * A.notas i⟩

/-- [DEF] a razão de cada nota à nota principal (Kimi). Não é a escala: a modulação muda esta razão e mantém a escala (`modular_mantem_a_escala`). -/
noncomputable def razao (A : Acorde) (i : Fin 5) : ℝ := A.notas i / notaPrincipal A

/-- [DEF] **LER O ACORDE**: E₀ é o meio-tom pinado abaixo da nota principal. A leitura devolve um número; o acorde fica como está. -/
noncomputable def lerE0 (A : Acorde) : ℝ := meioTom * notaPrincipal A

/-- [KERNEL] ★★★ **A TRANSPOSIÇÃO PRESERVA TODA RAZÃO** (`AcordeE0.transpose_preserves_every_ratio`, do Kimi). -/
theorem transpor_preserva_toda_razao (r : ℝ) (hr : r ≠ 0) (A : Acorde) (i : Fin 5) :
    razao (transpor r A) i = razao A i := by
  simp only [razao, notaPrincipal, transpor]
  exact mul_div_mul_left _ _ hr

/-- [KERNEL] ★★★ **AS RAZÕES SÃO EXATAMENTE O INVARIANTE DA TRANSPOSIÇÃO**: dois acordes têm as mesmas razões à nota principal se e só se um é a transposição do outro. Fixadas as razões, sobra UM número real. -/
theorem mesmas_razoes_iff_transposicao (A B : Acorde) (hA : notaPrincipal A ≠ 0) (hB : notaPrincipal B ≠ 0) :
    (∀ i, razao B i = razao A i) ↔ ∃ r : ℝ, r ≠ 0 ∧ B = transpor r A := by
  constructor
  · intro h
    refine ⟨notaPrincipal B / notaPrincipal A, div_ne_zero hB hA, ?_⟩
    ext i
    have hi := h i
    unfold razao at hi
    rw [div_eq_div_iff hB hA] at hi
    show B.notas i = notaPrincipal B / notaPrincipal A * A.notas i
    rw [div_mul_eq_mul_div, eq_div_iff hA]
    linear_combination hi
  · rintro ⟨r, hr, rfl⟩ i
    exact transpor_preserva_toda_razao r hr A i

/-- [KERNEL] ★★ **A LEITURA ACOMPANHA A TRANSPOSIÇÃO**: `lerE0 (r·A) = r·lerE0 A`. A leitura não fixa o valor absoluto. -/
theorem lerE0_transpor (r : ℝ) (A : Acorde) : lerE0 (transpor r A) = r * lerE0 A := by
  simp only [lerE0, notaPrincipal, transpor]
  ring

/-- [KERNEL] ★★ **E₀ NÃO É ABSOLUTAMENTE LIVRE**: relativo à nota principal ele está pinado, `E₀/tônica = e^(−1/2)`, em todo acorde. Segue da definição de `lerE0`: a razão é a própria lei, que entra como definição [INPUT/ONTO]. -/
theorem E0_relativo_pinado (A : Acorde) (hA : notaPrincipal A ≠ 0) : lerE0 A / notaPrincipal A = meioTom := by
  unfold lerE0
  rw [mul_div_assoc, div_self hA, mul_one]

/-- [KERNEL] ★★ **AS RAZÕES NÃO FIXAM O ABSOLUTO**: com as mesmas razões há outro acorde com outro E₀. É o no-go, na língua do acorde. -/
theorem as_razoes_nao_fixam_o_absoluto (A : Acorde) (hA : 0 < notaPrincipal A) :
    ∃ B : Acorde, (∀ i, razao B i = razao A i) ∧ lerE0 B ≠ lerE0 A := by
  refine ⟨transpor 2 A, transpor_preserva_toda_razao 2 two_ne_zero A, ?_⟩
  rw [lerE0_transpor]
  have h : 0 < lerE0 A := mul_pos meioTom_pos hA
  intro h2
  linarith

/-- [DEF] **MODULAR A TÔNICA**: só a nota principal desce o meio-tom pinado; as outras quatro ficam sustentadas. Que o tom fique é fala do operador [INPUT]: o kernel não tem termo para o tom. -/
noncomputable def modular (A : Acorde) : Acorde := ⟨Function.update A.notas 0 (meioTom * A.notas 0)⟩

/-- [DEF] **RESOLVER**: a tônica sobe o meio-tom de volta; as outras notas seguem sustentadas. -/
noncomputable def resolver (A : Acorde) : Acorde := ⟨Function.update A.notas 0 (Real.exp (1 / 2) * A.notas 0)⟩

/-- [KERNEL] ★★ a tônica desce o meio-tom pinado. -/
theorem modular_tonica (A : Acorde) : notaPrincipal (modular A) = meioTom * notaPrincipal A := by
  simp [notaPrincipal, modular]

/-- [KERNEL] ★★★ **AS DEMAIS NOTAS FICAM SUSTENTADAS**: a modulação não toca em nenhuma outra nota. -/
theorem modular_sustenta (A : Acorde) (i : Fin 5) (hi : i ≠ 0) : (modular A).notas i = A.notas i := by
  simp [modular, Function.update, hi]

/-- [KERNEL] ★★★ **MANTENDO A ESCALA**: as razões entre as notas sustentadas não mudam. A escala é o que fica parado; quem se move é a tônica. -/
theorem modular_mantem_a_escala (A : Acorde) (i j : Fin 5) (hi : i ≠ 0) (hj : j ≠ 0) :
    (modular A).notas i / (modular A).notas j = A.notas i / A.notas j := by
  rw [modular_sustenta A i hi, modular_sustenta A j hj]

/-- [KERNEL] ★★ E₀ é o valor da tônica modulada. -/
theorem lerE0_e_a_tonica_modulada (A : Acorde) : lerE0 A = notaPrincipal (modular A) :=
  (modular_tonica A).symm

/-- [KERNEL] ★★ a modulação comuta com a transposição: o diminuto não fixa o tom absoluto. -/
theorem modular_comuta_com_transpor (r : ℝ) (A : Acorde) : modular (transpor r A) = transpor r (modular A) := by
  ext i
  by_cases hi : i = 0
  · subst hi
    simp [modular, transpor]
    ring
  · simp [modular, transpor, Function.update, hi]

/-- [KERNEL] ★★★ **O DIMINUTO NÃO É TRANSPOSIÇÃO**: com tônica e outra nota não nulas, nenhum fator leva o acorde ao acorde modulado. Por isso ele separa a tônica das notas sustentadas. -/
theorem modular_nao_e_transposicao (A : Acorde) (hA : notaPrincipal A ≠ 0) (i : Fin 5) (hi : i ≠ 0) (hn : A.notas i ≠ 0) :
    ¬ ∃ r : ℝ, modular A = transpor r A := by
  rintro ⟨r, h⟩
  have h0 : notaPrincipal (modular A) = notaPrincipal (transpor r A) := by rw [h]
  have h1 : (modular A).notas i = (transpor r A).notas i := by rw [h]
  rw [modular_tonica] at h0
  rw [modular_sustenta A i hi] at h1
  have hr0 : meioTom = r := mul_right_cancel₀ hA h0
  have hr1 : (1 : ℝ) = r := by
    have h2 : 1 * A.notas i = r * A.notas i := by
      rw [one_mul]
      exact h1
    exact mul_right_cancel₀ hn h2
  have := meioTom_lt_one
  linarith

/-- [KERNEL] ★★ cada intervalo à tônica abre meio-tom: `razão ↦ e^(1/2)·razão`. -/
theorem razao_abre_meio_tom (A : Acorde) (hA : notaPrincipal A ≠ 0) (i : Fin 5) (hi : i ≠ 0) :
    razao (modular A) i = Real.exp (1 / 2) * razao A i := by
  have hm : meioTom ≠ 0 := meioTom_pos.ne'
  have hinv : Real.exp (1 / 2) = meioTom⁻¹ := eq_inv_of_mul_eq_one_right meioTom_mul_sqrt_e
  unfold razao
  rw [modular_tonica, modular_sustenta A i hi, hinv]
  field_simp

/-- [KERNEL] ★★ **UMA NOTA UM TOM ACIMA VIRA TERÇA MENOR**: sob a hipótese `h`, a nota que estava um tom acima da tônica (um tom é uma nat) fica três meios-tons acima da tônica modulada, `e^(3/2)`. Que o sistema opere em terças é fala do operador; as cinco notas são [OPEN]. -/
theorem um_tom_vira_terca_menor (A : Acorde) (hA : notaPrincipal A ≠ 0) (i : Fin 5) (hi : i ≠ 0)
    (h : A.notas i = Real.exp 1 * notaPrincipal A) : razao (modular A) i = Real.exp (3 / 2) := by
  rw [razao_abre_meio_tom A hA i hi]
  unfold razao
  rw [h, mul_div_assoc, div_self hA, mul_one, ← Real.exp_add]
  norm_num

/-- [KERNEL] ★★ a resolução devolve o acorde: `resolver (modular A) = A`. Que ela espere é leitura do operador [ONTO]. -/
theorem resolver_modular (A : Acorde) : resolver (modular A) = A := by
  ext i
  by_cases hi : i = 0
  · subst hi
    have h : Real.exp (1 / 2) * (meioTom * A.notas 0) = A.notas 0 := by
      rw [← mul_assoc, mul_comm (Real.exp (1 / 2)) meioTom, meioTom_mul_sqrt_e, one_mul]
    simpa [resolver, modular] using h
  · simp [resolver, modular, Function.update, hi]

/-- [KERNEL] ★★ a lei é a leitura do acorde cuja nota principal é a tônica: `E₀ = lerE0 A`. -/
theorem Lei.E0_e_a_leitura (L : Lei) (A : Acorde) (h : notaPrincipal A = L.E_pent) : L.transicao.E0 = lerE0 A := by
  rw [Lei.E0_eq, lerE0, h]

/-- [KERNEL] ★★ O MEIO-TOM É O PEDÁGIO LOCAL do colapso, `e^(−localNats)` (`CollapseCostLaw`, [INPUT] no kernel). O pedágio da oitava é outro componente (`Sonico.the_pin_is_not_the_half_nat`). -/
theorem meioTom_e_o_pedagio_local (K : ChatgptAudit.Collapse057.CollapseCostLaw) : meioTom = Real.exp (-K.localNats) := by
  rw [K.local_half]
  rfl

/-- [KERNEL] ★★ O MEIO-TOM TEM O VALOR DO PESO DA FACE ABSOLUTA. Igualdade de valor; ler esse ½ como o meio-tom é do operador [ONTO]. -/
theorem meioTom_e_a_face {n : Type} [Fintype n] [DecidableEq n] [Nonempty n] {Γ : Matrix n n ℂ} (hΓ : Γ.trace = 0) :
    meioTom = Real.exp (-(gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 + Γ))).re) := by
  rw [peso_da_face_absoluta hΓ]
  rfl

/-- [KERNEL] ★★ A TÔNICA É O VOLUME DA FACE vezes a unidade posta: `tonica c u = e^(S_∂)·u`, a tônica candidata do Kimi (`Vol_∂^min = e^(S_∂) = √e`). Igualdade de valor. -/
theorem tonica_e_o_volume_da_face {n : Type} [Fintype n] [DecidableEq n] [Nonempty n] {Γ : Matrix n n ℂ} (c : TGLCoupling) (u : ℝ)
    (hΓ : Γ.trace = 0) : tonica c u = Real.exp ((gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 + Γ))).re) * u := by
  rw [peso_da_face_absoluta hΓ, tonica_eq]

/-- [KERNEL] ★★ AS DUAS FACES SOMAM O TOM: `S(+) + S(−) = 1`. -/
theorem o_tom_e_as_duas_faces {n : Type} [Fintype n] [DecidableEq n] [Nonempty n] {Γ : Matrix n n ℂ} (hΓ : Γ.trace = 0) :
    (gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 + Γ))).re + (gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 - Γ))).re = 1 := by
  rw [(absolute_faces_half hΓ).1, (absolute_faces_half hΓ).2]
  first
    | (norm_num; done)
    | (simp; norm_num; done)
    | (simp [Complex.div_ofNat_re]; norm_num; done)

/-- ★★★ **A LEI DO DIMINUTO — o fecho do acorde.** Só a tônica desce o meio-tom; as demais notas ficam sustentadas, e a escala fica; o diminuto não é transposição; cada intervalo à tônica abre meio-tom; a
    resolução devolve o acorde; E₀ está pinado à nota principal; a transposição é a liberdade que sobra e as razões não fixam o absoluto; e a oitava não se desce em meios-tons. -/
theorem the_diminished_law_closes (A : Acorde) (hA : 0 < notaPrincipal A) :
    notaPrincipal (modular A) = meioTom * notaPrincipal A
    ∧ (∀ i : Fin 5, i ≠ 0 → (modular A).notas i = A.notas i)
    ∧ (∀ i j : Fin 5, i ≠ 0 → j ≠ 0 → (modular A).notas i / (modular A).notas j = A.notas i / A.notas j)
    ∧ (∀ i : Fin 5, i ≠ 0 → A.notas i ≠ 0 → ¬ ∃ r : ℝ, modular A = transpor r A)
    ∧ (∀ i : Fin 5, i ≠ 0 → razao (modular A) i = Real.exp (1 / 2) * razao A i)
    ∧ resolver (modular A) = A
    ∧ lerE0 A / notaPrincipal A = meioTom
    ∧ (∀ r : ℝ, r ≠ 0 → ∀ i, razao (transpor r A) i = razao A i)
    ∧ (∀ r : ℝ, lerE0 (transpor r A) = r * lerE0 A)
    ∧ (∃ B : Acorde, (∀ i, razao B i = razao A i) ∧ lerE0 B ≠ lerE0 A)
    ∧ (∀ n : ℕ, (n : ℝ) * (1 / 2) ≠ Real.log 2) :=
  ⟨modular_tonica A, modular_sustenta A, modular_mantem_a_escala A, fun i hi hn => modular_nao_e_transposicao A hA.ne' i hi hn,
   razao_abre_meio_tom A hA.ne', resolver_modular A, E0_relativo_pinado A hA.ne',
   fun r hr i => transpor_preserva_toda_razao r hr A i, fun r => lerE0_transpor r A,
   as_razoes_nao_fixam_o_absoluto A hA, octave_is_not_a_whole_number_of_half_tones⟩

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
#print axioms TGLExt.LeiDoDiminuto.transpor_preserva_toda_razao
#print axioms TGLExt.LeiDoDiminuto.mesmas_razoes_iff_transposicao
#print axioms TGLExt.LeiDoDiminuto.lerE0_transpor
#print axioms TGLExt.LeiDoDiminuto.E0_relativo_pinado
#print axioms TGLExt.LeiDoDiminuto.as_razoes_nao_fixam_o_absoluto
#print axioms TGLExt.LeiDoDiminuto.Lei.E0_e_a_leitura
#print axioms TGLExt.LeiDoDiminuto.meioTom_e_o_pedagio_local
#print axioms TGLExt.LeiDoDiminuto.meioTom_e_a_face
#print axioms TGLExt.LeiDoDiminuto.tonica_e_o_volume_da_face
#print axioms TGLExt.LeiDoDiminuto.o_tom_e_as_duas_faces
#print axioms TGLExt.LeiDoDiminuto.modular_tonica
#print axioms TGLExt.LeiDoDiminuto.modular_sustenta
#print axioms TGLExt.LeiDoDiminuto.modular_mantem_a_escala
#print axioms TGLExt.LeiDoDiminuto.lerE0_e_a_tonica_modulada
#print axioms TGLExt.LeiDoDiminuto.modular_comuta_com_transpor
#print axioms TGLExt.LeiDoDiminuto.modular_nao_e_transposicao
#print axioms TGLExt.LeiDoDiminuto.razao_abre_meio_tom
#print axioms TGLExt.LeiDoDiminuto.um_tom_vira_terca_menor
#print axioms TGLExt.LeiDoDiminuto.resolver_modular
#print axioms TGLExt.LeiDoDiminuto.the_diminished_law_closes
