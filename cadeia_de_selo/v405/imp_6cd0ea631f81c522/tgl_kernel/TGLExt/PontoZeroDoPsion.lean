import TGLExt.ProjecaoTransversalDaMeiaNat
import TGLExt.ThePsionAndTheViscosity

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
  (raio 1,8 μm), λ do psíon = 72,9 μm. O número é o mesmo; o que muda é a NATUREZA: a forma β·sen45°·u é o ponto zero do psíon sob a lei
  «R é o pagamento».
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

end TGLExt.PontoZeroDoPsion

#print axioms TGLExt.PontoZeroDoPsion.psion_quantum
#print axioms TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point
#print axioms TGLExt.PontoZeroDoPsion.psion_quantum_is_twice_the_mass
#print axioms TGLExt.PontoZeroDoPsion.the_payment_completes_only_in_the_limit
#print axioms TGLExt.PontoZeroDoPsion.the_zero_point_closes
#print axioms TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point_at_the_posted_one
