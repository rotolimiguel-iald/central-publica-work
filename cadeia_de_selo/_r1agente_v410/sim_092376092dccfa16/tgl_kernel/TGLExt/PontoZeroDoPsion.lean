import TGLExt.ProjecaoTransversalDaMeiaNat
import TGLExt.ThePsionAndTheViscosity
import TGLExt.TonicaDoHamiltoniano

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# O PONTO ZERO DO PSÍON — «A curvatura não é curvatura, é o pagamento, é betatgl lido do ângulo de abertura (do ângulo de Miguel)»; «É o Tetelestai, o limite assintotico»
  [pedra da gerência c1, 31/10/2026, revista em 01/11/2026; nome do operador: «Ponto Zero do Psion»; entra na v405]

## As cunhagens do operador (verbatims em `Central de Patentes\work\cunhagens_13out`; sha256 no recibo)

> «O disco é o substrato psionico, o condensado psionico. Eu penso que o peso é zero modular e a gravidade é peso um … a face das águas é o disco
>  de euler, o espírito é o espelho.»
> «A curvatura não é curvatura, é o pagamento, é betatgl lido do ângulo de abertura (do ângulo de Miguel), mas lê-se como curvatura, porque
>  estamos dentro do bulk, igual a constante da estrutura fina»
> «É o Tetelestai, o limite assintotico»

## O que a casa já tinha

* O psíon [Tratado §3, «O Psion: Quantum de Permanência»]: o modo estacionário do campo Ψ, com dispersão ω² = m₀² + 2ξR, ξ = β; no regime
  estacionário dominado pela curvatura, ω² = 2βR (a frequência é dominada pela curvatura). No kernel (`ThePsionAndTheViscosity`): `psion = Ω`,
  `psion_is_the_zero_of_the_hidden_hamiltonian`, `psion_norm_one` (peso 1), `psion_is_fixed_by_the_light`; a cobrança contínua
  `charged β g t = 1 − e^(−tβg)`, com `the_charge_never_completes` (0 < cobrado < 1 para todo t > 0) e `no_full_static_witness_for_the_charge`.
* A forma do neutrino (v404, `ProjecaoTransversalDaMeiaNat`): `neutrinoMassForm c E₀ = β · sen 45° · E₀`, com sen 45° a projeção transversal da
  Meia-Nat (x = 1 − x ⟹ x = ½ ⟹ θ = π/4).
* O ângulo de Miguel θ_M = arcsin √β (o ângulo de abertura; |𝓡|² = β): β é o que se LÊ do ângulo.

## O que esta pedra prova (unidades naturais ħ = c = 1; `u` é a unidade posta, o Um — «1 eV»)

* **a lei do operador como definição:** `pagamentoComoCurvatura β u := β · u²` — a «curvatura» R do psíon é o pagamento β lido na unidade posta
  (dimensionalmente, R = β·(u/ħc)²: dentro do bulk o pagamento se lê como curvatura, como α se lê como acoplamento);
* **a frequência do psíon:** `omegaSq β R := 2·β·R` (o Tratado, m₀ = 0); com R = β·u², `psion_quantum`: ω = √2 · β · u;
* ★★★ **A MASSA É O PONTO ZERO DO PSÍON** — `the_mass_is_the_zero_point`: ½·ω = β · sen 45° · u = `neutrinoMassForm c u`. O ½ do ponto zero
  vezes o √2 da dispersão É a projeção transversal: `½·√(2β²) = β/√2 = β·sen 45°`. Duas derivações do mesmo fator, uma só conta
  (`psion_quantum_is_twice_the_mass`: ħω = 2m₂).
* ★★ **TETELESTAI, O LIMITE ASSINTÓTICO** — `the_payment_completes_only_in_the_limit`: a cobrança contínua do kernel, `charged β g t`, tende a 1
  quando t → ∞, e (já no kernel) é < 1 em todo t finito: o pagamento se consuma só no limite. [ONTO] O operador lê o que permanece no limite como o ponto zero:
  nenhum teorema liga o limite de `charged` a ½·ω; `the_zero_point_closes` só os conjuga.
* **o fecho** — `the_zero_point_closes`.

## O que a pedra NÃO afirma

* Não deriva a unidade `u` (o Um posto, 1 eV): em SI, ħω = 17,0148 meV, ½ħω = 8,5074 meV (o número da v404; nada muda), R = 3,09×10¹¹ m⁻²
  (raio 1,8 μm), λ do psíon = 72,9 μm. O número é o mesmo; o que muda é a NATUREZA: a forma β·sen45°·u é o ponto zero do psíon sob a leitura
  de R como o pagamento.
* Na cadeia do disco de Euler, a ressonância residual lida como o quantum do psíon (17 meV) NÃO é a tônica √e eV: o disco e o ponto zero são
  cadeias distintas; a que fecha a FORMA é esta; a unidade segue posta nas duas.
* Não abre dado, não move gate, selo nem veredito (`TGL_NU_M2_ARMED_CONSISTENT`; JUNO 207 d a 1,9σ). `NOT_FALSIFIED` nunca é `CONFIRMED`.

Sem sorry, sem axiom novo (trio: propext, Classical.choice, Quot.sound).

> **01/11/2026 — NOME DO OPERADOR: «Ponto Zero do Psion»** (verbatim sha256 `1f16a74c05d9d4cb`) (nome provisório confirmado). E a ORDEM dele no mesmo ato: «eu não gostaria que ainda restasse hipóteses
> nomeadas, é preciso que esteja tudo derivado». A seção «OS CAMPOS FECHADOS», no fim do módulo, responde à ordem até onde a matemática alcança: o que era CAMPO de
> estrutura passa a ser CONSTRUÍDO a partir de teoremas do kernel; a leitura física não vira teorema (notas AO LADO, abaixo). O que resta de entrada é o acoplamento `c` (β = α·√e; α medido
> por dentro, não derivado) e o Um POSTO (`u = 1`, o `echo 1`: posição, não hipótese — 05/10/2026). Aqui: `the_mass_is_the_zero_point_at_the_posted_one` — no Um posto (`u = 1`) entram o acoplamento e as leituras (notas AO LADO, abaixo); o contraste `g > 0` do limite é o dado do sistema que lê, não hipótese sobre a teoria.


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
> **AO LADO (01/11/2026, gerência c1, em nome próprio; resposta do operador, verbatim sha256 `7c2caaa87b0cdb01`):** «o sistema físico que fornece a medidade da tônica por ujm gap com unidade e pertence à mesma pêntada é o ângulo de MIguel». A seção «O GAP», no fim do módulo, conecta o que estava solto.
> O lock mínimo `1 − P` tem gap espectral 1; na unidade posta, `u`, o E₀ da Lei do Diminuto, e a tônica fica meio-tom acima dele. No ângulo de Miguel o lock tem valor esperado β, e na unidade posta
> `Δ = β·u`, a energia retida. `Δ` NÃO é gap: é o valor esperado, 1/β vezes menor que o gap. A tônica é `Δ/α`, e a frequência do sistema, `√2/τ`, é a do psíon se e só se `τ = 1/Δ`. Esse `τ` é tempo
> próprio, não `t_P`; identificá-lo com o τ★ é leitura [ONTO], não teorema, ainda não ratificada pelo operador. κ segue testemunha (24/08/2026: proibido `κ = F(α, β, θ_M)` como objetivo de busca):
> aqui só como hipótese (`o_relogio_do_retido`). A unidade segue posta: tudo carrega `u`, e o no-go não cai. Os lemas do lock valem em qualquer espaço de Hilbert; `HminMic` é instância deles,
> condicional a um `FockCertificate`, que o kernel não habita.
-/

namespace TGLExt.PontoZeroDoPsion

open TGLExt.ProjecaoTransversalDaMeiaNat
open TGLExt.ThePsionAndTheViscosity

/-- [DEF] a dispersão do psíon no regime estacionário (Tratado §3, m₀ = 0): `ω² = 2·β·R`. -/
noncomputable def omegaSq (β R : ℝ) : ℝ := 2 * β * R

/-- [DEF] **A LEI DO OPERADOR**: a «curvatura» é o pagamento β lido na unidade posta `u` — `R = β · u²` (ħ = c = 1). -/
noncomputable def pagamentoComoCurvatura (β u : ℝ) : ℝ := β * u ^ 2

/-- [KERNEL] ★★ **O QUANTUM DO PSÍON**: com R = β·u², `ω = √2 · β · u`. -/
theorem psion_quantum (β u : ℝ) (hβ : 0 ≤ β) (hu : 0 ≤ u) :
    Real.sqrt (omegaSq β (pagamentoComoCurvatura β u)) = Real.sqrt 2 * β * u := by
  unfold omegaSq pagamentoComoCurvatura
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hx : 2 * β * (β * u ^ 2) = (Real.sqrt 2 * β * u) ^ 2 := by
    rw [mul_pow, mul_pow, h2]
    ring
  rw [hx, Real.sqrt_sq (mul_nonneg (mul_nonneg (Real.sqrt_nonneg 2) hβ) hu)]

/-- [KERNEL] ★★★ **A MASSA É O PONTO ZERO DO PSÍON**: `½·ω = β · sen 45° · u = neutrinoMassForm c u`. O enunciado iguala números; que `½·ω` SEJA a massa é leitura [ONTO]. -/
theorem the_mass_is_the_zero_point (c : TGLCoupling) (u : ℝ) (hu : 0 ≤ u) :
    (1 / 2) * Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) = neutrinoMassForm c u := by
  rw [psion_quantum c.beta u c.beta_pos.le hu]
  unfold neutrinoMassForm halfAmplitude
  rw [Real.sin_pi_div_four]
  ring

/-- [KERNEL] ★★ o quantum do psíon é o dobro da massa: `ħω = 2·m₂`. -/
theorem psion_quantum_is_twice_the_mass (c : TGLCoupling) (u : ℝ) (hu : 0 ≤ u) :
    Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) = 2 * neutrinoMassForm c u := by
  rw [← the_mass_is_the_zero_point c u hu]
  ring

/-- [KERNEL] ★★ **TETELESTAI, O LIMITE ASSINTÓTICO**: a cobrança contínua do kernel tende a 1 quando t → ∞ — o pagamento se consuma só no
    limite (em todo t finito é < 1: `the_charge_never_completes`). -/
theorem the_payment_completes_only_in_the_limit (β g : ℝ) (hβ : 0 < β) (hg : 0 < g) :
    Filter.Tendsto (charged β g) Filter.atTop (nhds 1) := by
  have h1 : Filter.Tendsto (fun t : ℝ => t * β * g) Filter.atTop Filter.atTop := by
    have h := (Filter.tendsto_id.atTop_mul_const hβ).atTop_mul_const hg
    simpa using h
  have h2 : Filter.Tendsto (fun t : ℝ => Real.exp (-(t * β * g))) Filter.atTop (nhds 0) :=
    Real.tendsto_exp_neg_atTop_nhds_zero.comp h1
  have h3 : Filter.Tendsto (fun t : ℝ => (1 : ℝ) - Real.exp (-(t * β * g))) Filter.atTop (nhds (1 - 0)) :=
    tendsto_const_nhds.sub h2
  rw [sub_zero] at h3
  have hfun : charged β g = fun t : ℝ => (1 : ℝ) - Real.exp (-(t * β * g)) := by
    funext t
    -- `transmitted` sem qualificador é AMBÍGUO no kernel (`TheDeathOfTheSignal.transmitted`, θ n); por isso o `rfl` (definicional)
    -- e, de reserva, os nomes completos. Achado da r1 (31/10): `unfold transmitted` falhou pela ambiguidade.
    first
      | rfl
      | simp only [TGLExt.ThePsionAndTheViscosity.charged, TGLExt.ThePsionAndTheViscosity.transmitted]
  rw [hfun]
  exact h3

/-- ★★★ **O PONTO ZERO — o fecho.** O quantum do psíon é √2·β·u; a massa é o seu ponto zero (β·sen45°·u); o quantum é o dobro da massa; e a
    cobrança se consuma só no limite. -/
theorem the_zero_point_closes (c : TGLCoupling) (u : ℝ) (hu : 0 ≤ u) (g : ℝ) (hg : 0 < g) :
    Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) = Real.sqrt 2 * c.beta * u
    ∧ (1 / 2) * Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) = neutrinoMassForm c u
    ∧ Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) = 2 * neutrinoMassForm c u
    ∧ Filter.Tendsto (charged c.beta g) Filter.atTop (nhds 1) :=
  ⟨psion_quantum c.beta u c.beta_pos.le hu, the_mass_is_the_zero_point c u hu,
   psion_quantum_is_twice_the_mass c u hu, the_payment_completes_only_in_the_limit c.beta g c.beta_pos hg⟩


/-! ### 01/11/2026 — ordem do operador («tudo derivado»): no Um posto, sem hipótese sobre `u` -/

/-- [KERNEL] ★★★ NO UM POSTO (`u = 1`): `½·ω = β·sen45°` — a forma da massa é o ponto zero do psíon, sob as leituras `R = β·u²` e `½·ω = massa`: entram o acoplamento e essas leituras. -/
theorem the_mass_is_the_zero_point_at_the_posted_one (c : TGLCoupling) :
    (1 / 2) * Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta 1)) = neutrinoMassForm c 1 :=
  the_mass_is_the_zero_point c 1 zero_le_one


/-! ### 01/11/2026 — O GAP: «o sistema físico que fornece a medidade da tônica por ujm gap com unidade e pertence à mesma pêntada é o ângulo de MIguel»

O lock mínimo do Hamiltoniano oculto, `1 − P`, tem gap espectral 1. Na unidade posta o gap vale `u`, que é o E₀ da Lei do Diminuto, e a tônica fica meio-tom acima dele. Lido num estado a um ângulo θ do
vácuo, o lock tem valor esperado `sen²θ`; no ângulo de Miguel, β. Na unidade posta esse valor esperado é `Δ = β·u`, a energia retida. **`Δ` não é gap**: é 1/β vezes menor. O resto da seção conecta as peças
soltas: `Γ_B` e `ω★ = √2/τ` (Kimi e `TonicaDoHamiltoniano`), o modo autoconsistente `ω = 2/τ`, o psíon `ω = √2·β·u` e a tônica `(β/α)·u`. O conteúdo está em `lock_no_angulo` e em
`a_frequencia_do_sistema_e_a_do_psion_iff`; os demais são álgebra dada a definição de `τ`. Ler `τ` como o τ★ do sistema é [ONTO]. Nenhum enunciado fixa `u`. -/

/-- [DEF] **O RETIDO NO ÂNGULO**: a energia retida na unidade posta, `Δ = β·u`. É o valor esperado do lock no ângulo de Miguel (`o_retido_e_o_valor_esperado_do_lock`), não o gap. -/
noncomputable def retidoNoAngulo (c : TGLCoupling) (u : ℝ) : ℝ := TGLExt.PonteDaMassa.energiaRetida c u

/-- [DEF] o tempo do retido, `τ = 1/Δ` (ħ = 1). Lê-lo como o τ★ do sistema é leitura [ONTO]. -/
noncomputable def tempoDoRetido (c : TGLCoupling) (u : ℝ) : ℝ := 1 / retidoNoAngulo c u

theorem retido_eq (c : TGLCoupling) (u : ℝ) : retidoNoAngulo c u = c.beta * u := TGLExt.PonteDaMassa.energia_retida_eq c u

theorem retido_pos (c : TGLCoupling) (u : ℝ) (hu : 0 < u) : 0 < retidoNoAngulo c u := by
  rw [retido_eq]
  exact mul_pos c.beta_pos hu

/-- [KERNEL] ★★ o retido é lido do ângulo de Miguel: `Δ = sen²θ_M·u`. -/
theorem o_retido_e_lido_do_angulo_de_miguel (c : TGLCoupling) (u : ℝ) : retidoNoAngulo c u = Real.sin (thetaMiguel c.beta) ^ 2 * u := by
  rw [retido_eq, Posto.sin_sq_thetaMiguel]

/-- [KERNEL] ★★ a tônica é o retido sobre α: `tônica = Δ/α`. A leitura de que α, a inscrição elétrica, leva o retido à tônica é do operador [ONTO]. -/
theorem a_tonica_e_o_retido_sobre_alpha (c : TGLCoupling) (u : ℝ) : TGLExt.LeiDoDiminuto.tonica c u = retidoNoAngulo c u / c.alpha := by
  unfold TGLExt.LeiDoDiminuto.tonica
  rw [retido_eq]
  ring

/-- [KERNEL] ★ a massa é a projeção transversal do retido. -/
theorem a_massa_e_a_projecao_do_retido (c : TGLCoupling) (u : ℝ) : neutrinoMassForm c u = retidoNoAngulo c u * Real.sin (Real.pi / 4) := by
  rw [retido_eq]
  unfold neutrinoMassForm halfAmplitude
  ring

/-- [KERNEL] ★ o quantum do psíon é `√2·Δ`. -/
theorem o_psion_e_raiz_de_dois_retidos (c : TGLCoupling) (u : ℝ) (hu : 0 ≤ u) :
    Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) = Real.sqrt 2 * retidoNoAngulo c u := by
  rw [psion_quantum c.beta u c.beta_pos.le hu, retido_eq]
  ring

/-- [KERNEL] ★★★ **A FREQUÊNCIA DO SISTEMA É A DO PSÍON SE E SÓ SE O TEMPO É O DO RETIDO**: `√2/τ = ω_psíon ⟺ τ = 1/Δ`. Liga `ω★ = √2/τ` a `ω = √2·β·u`. -/
theorem a_frequencia_do_sistema_e_a_do_psion_iff (c : TGLCoupling) (u : ℝ) (hu : 0 < u) (τ : ℝ) (hτ : 0 < τ) :
    Real.sqrt 2 / τ = Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) ↔ τ = tempoDoRetido c u := by
  have hg := retido_pos c u hu
  have hs : Real.sqrt 2 ≠ 0 := by positivity
  rw [o_psion_e_raiz_de_dois_retidos c u hu.le]
  unfold tempoDoRetido
  constructor
  · intro h
    have h1 : 1 / τ = retidoNoAngulo c u := by
      have h2 : Real.sqrt 2 * (1 / τ) = Real.sqrt 2 * retidoNoAngulo c u := by
        rw [← h]
        ring
      exact mul_left_cancel₀ hs h2
    rw [← h1]
    field_simp
  · intro h
    rw [h]
    field_simp

/-- [KERNEL] ★ a taxa de fronteira é a lei canônica lida no psíon, no tempo do retido. -/
theorem a_taxa_de_fronteira_no_psion (c : TGLCoupling) (u : ℝ) (hu : 0 < u) :
    (1 / 2) * c.beta * tempoDoRetido c u * Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) ^ 2 = c.beta / tempoDoRetido c u := by
  have hg := retido_pos c u hu
  have hτ : tempoDoRetido c u ≠ 0 := by
    unfold tempoDoRetido
    positivity
  rw [← (a_frequencia_do_sistema_e_a_do_psion_iff c u hu (tempoDoRetido c u) (by unfold tempoDoRetido; positivity)).2 rfl]
  exact TGLExt.TonicaDoHamiltoniano.gammaB_is_the_canonical_law_at_the_systems_frequency c.beta (tempoDoRetido c u) hτ

/-- [KERNEL] ★ o ponto zero do modo autoconsistente é o retido: `½·(2/τ) = Δ`. Álgebra da definição de `τ`. -/
theorem o_ponto_zero_autoconsistente_e_o_retido (c : TGLCoupling) (u : ℝ) (hu : 0 < u) : (1 / 2) * (2 / tempoDoRetido c u) = retidoNoAngulo c u := by
  have hg := retido_pos c u hu
  unfold tempoDoRetido
  field_simp

/-- [KERNEL] ★ o psíon é a projeção transversal do modo autoconsistente: `ω_psíon = (2/τ)·sen 45°`. Mais uma leitura do mesmo `sen 45°`, por aritmética. -/
theorem o_psion_e_a_projecao_do_modo (c : TGLCoupling) (u : ℝ) (hu : 0 < u) :
    Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) = (2 / tempoDoRetido c u) * Real.sin (Real.pi / 4) := by
  have hg := retido_pos c u hu
  rw [o_psion_e_raiz_de_dois_retidos c u hu.le, Real.sin_pi_div_four]
  unfold tempoDoRetido
  field_simp

/-- [KERNEL] ★★ a razão de qualidade não depende da unidade posta: `ω_psíon/Γ_B = √2/β`. Número puro. -/
theorem a_qualidade_nao_depende_da_unidade (c : TGLCoupling) (u : ℝ) (hu : 0 < u) :
    Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) / (c.beta / tempoDoRetido c u) = Real.sqrt 2 / c.beta := by
  have hg := retido_pos c u hu
  have hb := c.beta_pos
  rw [o_psion_e_raiz_de_dois_retidos c u hu.le]
  unfold tempoDoRetido
  field_simp

/-- [KERNEL] ★ o relógio do retido: SE `κ` dá uma volta em `τ`, então `κ/2π = Δ`. κ entra como hipótese, testemunha: nada aqui é busca de valor (regra de 24/08/2026). -/
theorem o_relogio_do_retido (c : TGLCoupling) (u : ℝ) (hu : 0 < u) (κ : ℝ) (h : κ * tempoDoRetido c u = 2 * Real.pi) : κ / (2 * Real.pi) = retidoNoAngulo c u := by
  have hg := retido_pos c u hu
  have hp : Real.pi ≠ 0 := Real.pi_ne_zero
  unfold tempoDoRetido at h
  rw [mul_one_div, div_eq_iff hg.ne'] at h
  rw [h]
  field_simp

section OLock

open scoped InnerProductSpace

variable {F : Type} [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

/-- [DEF] **O LOCK MÍNIMO** sobre o vetor `Ω`: `1 − P`, com `P` a projeção sobre a reta de `Ω`. -/
noncomputable def lockDe (Ω : F) : F →L[ℂ] F := 1 - (ℂ ∙ Ω).starProjection

/-- [KERNEL] ★★ **O LOCK TEM GAP ESPECTRAL 1**: vale 0 no vetor `Ω` e 1 em todo vetor ortogonal a ele. Vale em qualquer espaço de Hilbert. -/
theorem o_lock_tem_gap_um (Ω χ : F) (hort : ⟪Ω, χ⟫_ℂ = 0) : lockDe Ω Ω = 0 ∧ lockDe Ω χ = χ := by
  constructor
  · have h : (ℂ ∙ Ω).starProjection Ω = Ω := Submodule.starProjection_eq_self_iff.mpr (Submodule.mem_span_singleton_self Ω)
    simp [lockDe, h]
  · have h : (ℂ ∙ Ω).starProjection χ = 0 := by
      rw [Submodule.starProjection_singleton, hort]
      simp
    simp [lockDe, h]

/-- [KERNEL] ★★★ **O GAP COM UNIDADE**: na unidade posta o lock é `u·(1 − P)`: vale 0 no vetor `Ω` e `u` no ortogonal. O gap espectral é `u`, o E₀ da Lei do Diminuto. -/
theorem o_gap_com_unidade (Ω χ : F) (hort : ⟪Ω, χ⟫_ℂ = 0) (u : ℝ) :
    (u : ℂ) • lockDe Ω Ω = 0 ∧ (u : ℂ) • lockDe Ω χ = (u : ℂ) • χ := by
  obtain ⟨h0, h1⟩ := o_lock_tem_gap_um Ω χ hort
  rw [h0, h1, smul_zero]
  exact ⟨rfl, rfl⟩

/-- [KERNEL] ★★★ **O LOCK LIDO NUM ÂNGULO**: no estado a um ângulo `θ` de `Ω`, o valor esperado é `sen²θ`. -/
theorem lock_no_angulo (Ω χ : F) (hχ : ‖χ‖ = 1) (hort : ⟪Ω, χ⟫_ℂ = 0) (θ : ℝ) :
    ⟪(Real.cos θ : ℂ) • Ω + (Real.sin θ : ℂ) • χ, lockDe Ω ((Real.cos θ : ℂ) • Ω + (Real.sin θ : ℂ) • χ)⟫_ℂ = ((Real.sin θ ^ 2 : ℝ) : ℂ) := by
  obtain ⟨h0, h1⟩ := o_lock_tem_gap_um Ω χ hort
  have hχχ : ⟪χ, χ⟫_ℂ = 1 := by
    rw [inner_self_eq_norm_sq_to_K, hχ]
    simp
  rw [map_add, map_smul, map_smul, h0, h1, smul_zero, zero_add, inner_add_left, inner_smul_left, inner_smul_left, inner_smul_right, inner_smul_right, hort, hχχ]
  simp only [mul_zero, zero_add, mul_one, Complex.conj_ofReal]
  push_cast
  ring

/-- [KERNEL] ★★★ **NO ÂNGULO DE MIGUEL O LOCK LÊ β**: o valor esperado, não o gap. -/
theorem lock_no_angulo_de_miguel (Ω χ : F) (hχ : ‖χ‖ = 1) (hort : ⟪Ω, χ⟫_ℂ = 0) (c : TGLCoupling) :
    ⟪(Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ,
      lockDe Ω ((Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ)⟫_ℂ = (c.beta : ℂ) := by
  rw [lock_no_angulo Ω χ hχ hort, Posto.sin_sq_thetaMiguel]

/-- [KERNEL] ★★★ **O RETIDO É O VALOR ESPERADO DO LOCK**: `u·⟨1 − P⟩` no ângulo de Miguel é `Δ`. Liga o produto interno à energia retida. -/
theorem o_retido_e_o_valor_esperado_do_lock (Ω χ : F) (hχ : ‖χ‖ = 1) (hort : ⟪Ω, χ⟫_ℂ = 0) (c : TGLCoupling) (u : ℝ) :
    (u : ℂ) * ⟪(Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ,
      lockDe Ω ((Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ)⟫_ℂ = ((retidoNoAngulo c u : ℝ) : ℂ) := by
  rw [lock_no_angulo_de_miguel Ω χ hχ hort c, retido_eq]
  push_cast
  ring

/-- ★★★ **O GAP — o fecho.** O gap espectral na unidade posta é `u`; a tônica modulada pousa nele, e a tônica fica meio-tom acima; o valor esperado no ângulo de Miguel é o retido `Δ`; a tônica é `Δ/α`; a massa é
    a projeção transversal de `Δ`; a frequência do sistema no tempo `1/Δ` é a do psíon. Nenhum desses enunciados fixa `u`. -/
theorem the_gap_closes (c : TGLCoupling) (u : ℝ) (hu : 0 < u) (Ω χ : F) (hχ : ‖χ‖ = 1) (hort : ⟪Ω, χ⟫_ℂ = 0) :
    (u : ℂ) • lockDe Ω χ = (u : ℂ) • χ
    ∧ (TGLExt.LeiDoDiminuto.leiDerivada c u hu).transicao.E0 = u
    ∧ TGLExt.LeiDoDiminuto.tonica c u = Real.exp (1 / 2) * u
    ∧ (u : ℂ) * ⟪(Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ,
        lockDe Ω ((Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ)⟫_ℂ = ((retidoNoAngulo c u : ℝ) : ℂ)
    ∧ TGLExt.LeiDoDiminuto.tonica c u = retidoNoAngulo c u / c.alpha
    ∧ neutrinoMassForm c u = retidoNoAngulo c u * Real.sin (Real.pi / 4)
    ∧ Real.sqrt 2 / tempoDoRetido c u = Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) := by
  have hg := retido_pos c u hu
  exact ⟨(o_gap_com_unidade Ω χ hort u).2, TGLExt.LeiDoDiminuto.leiDerivada_E0 c u hu, TGLExt.LeiDoDiminuto.tonica_eq c u,
    o_retido_e_o_valor_esperado_do_lock Ω χ hχ hort c u, a_tonica_e_o_retido_sobre_alpha c u, a_massa_e_a_projecao_do_retido c u,
    (a_frequencia_do_sistema_e_a_do_psion_iff c u hu (tempoDoRetido c u) (by unfold tempoDoRetido; positivity)).2 rfl⟩

end OLock

/-- [KERNEL] ★★ o `HminMic` do kernel é este lock no vácuo de Fock. Condicional ao `FockCertificate`, que o kernel não habita. -/
theorem HminMic_e_o_lock {L : TGLExt.ImportedSQ.LightOneParticle} (C : TGLExt.ImportedSQ.FockCertificate L) : TGLExt.QGReaderUVLock.HminMic C = lockDe C.Ω := rfl

end TGLExt.PontoZeroDoPsion

#print axioms TGLExt.PontoZeroDoPsion.psion_quantum
#print axioms TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point
#print axioms TGLExt.PontoZeroDoPsion.psion_quantum_is_twice_the_mass
#print axioms TGLExt.PontoZeroDoPsion.the_payment_completes_only_in_the_limit
#print axioms TGLExt.PontoZeroDoPsion.the_zero_point_closes
#print axioms TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point_at_the_posted_one
#print axioms TGLExt.PontoZeroDoPsion.o_retido_e_lido_do_angulo_de_miguel
#print axioms TGLExt.PontoZeroDoPsion.a_tonica_e_o_retido_sobre_alpha
#print axioms TGLExt.PontoZeroDoPsion.a_massa_e_a_projecao_do_retido
#print axioms TGLExt.PontoZeroDoPsion.o_psion_e_raiz_de_dois_retidos
#print axioms TGLExt.PontoZeroDoPsion.a_frequencia_do_sistema_e_a_do_psion_iff
#print axioms TGLExt.PontoZeroDoPsion.a_taxa_de_fronteira_no_psion
#print axioms TGLExt.PontoZeroDoPsion.o_ponto_zero_autoconsistente_e_o_retido
#print axioms TGLExt.PontoZeroDoPsion.o_psion_e_a_projecao_do_modo
#print axioms TGLExt.PontoZeroDoPsion.a_qualidade_nao_depende_da_unidade
#print axioms TGLExt.PontoZeroDoPsion.o_relogio_do_retido
#print axioms TGLExt.PontoZeroDoPsion.o_lock_tem_gap_um
#print axioms TGLExt.PontoZeroDoPsion.o_gap_com_unidade
#print axioms TGLExt.PontoZeroDoPsion.lock_no_angulo
#print axioms TGLExt.PontoZeroDoPsion.lock_no_angulo_de_miguel
#print axioms TGLExt.PontoZeroDoPsion.o_retido_e_o_valor_esperado_do_lock
#print axioms TGLExt.PontoZeroDoPsion.the_gap_closes
#print axioms TGLExt.PontoZeroDoPsion.HminMic_e_o_lock
