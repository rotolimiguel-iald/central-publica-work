import TGLExt.PonteDaMassa
import TGLExt.LeiDoDiminuto

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A TÔNICA DO HAMILTONIANO — E₀: a liberdade de escala da forma (o no-go tipado), e onde ela pousa e as duas identidades da rota do monopolo
  [pedra da gerência c1, 31/10/2026, revista em 01/11/2026; nome do operador: «Tônica do Hamiltoniano»; entra na v405]

## A ordem do operador (verbatim sha256 `a22a54dfc97d96114e3d251a41bed8ea300d314c626a9349eda36ce09b2bdfc1`, 31/10/2026)

> «… eu derivei muita coisa com o kimi acerca da massa e precisamos, além de incorporar o que nos importa ao um.py, fechar a
> derivação final, mas agora é trabalho cuidadoso, é com cuidado e não só com força bruta que vamos resolver tudo que falta,
> não adianta vc delegar tudo agora, vc precisa ir pensando em cadeia, ir resolvendo o que falta de modo encadeado e sequenciado»

## O que esta pedra tipa (a conferência da gerência do HANDOFF_CLAUDE_E0_M2_31out do Kimi, feita nas fontes e por código próprio)

1. **A liberdade de escala de E₀ — o no-go dentro do formalismo atual.** O Kimi delimitou por reescalonamento [DECLARADO]; aqui é
   TEOREMA: para toda transição `T : TransicaoParaAMassa` (ponte 1) e todo `λ > 0`, `reescala T λ` é uma transição com a MESMA
   inscrição (`c`, `θ`) e `E₀ ↦ λ·E₀`; a massa derivada escala linearmente (`massa_derivada_reescala`); logo **nenhuma função da
   inscrição fixa E₀** (`no_function_of_the_inscription_fixes_E0`, com habitante explícito). O que o kernel prova é a FORMA
   `m₂/E₀ = β·sen 45°`; o valor absoluto de m₂ exige uma escala física adicional, que NÃO sai dos axiomas formalizados.
   É uma parede medida, não uma falsificação: o 1 eV segue [DECLARADO/INPUT]; reabrir exige um princípio dimensional independente
   (derivado ou medido), nunca o ajuste ao Δm²₂₁ (o dado pede 1,01–1,02 eV: inversão, proibida como derivação).
2. **A «taxa de fronteira» não é lei nova.** `Γ_B = β/τ★` é a lei canônica `Γ_ω = ½βτ★ω²` lida na frequência do próprio sistema,
   `ω★ = √2/τ★` (`gammaB_is_the_canonical_law_at_the_systems_frequency`). Fecha o item 6 da prioridade 2 do handoff: as duas taxas
   são o mesmo objeto, avaliado em ω★; a «identificação nativa» é a escolha dessa frequência.
3. **A rota do monopolo é o horizonte do próprio sistema.** `τ★ = 4πGE/c⁵` é o tempo de luz da circunferência de Schwarzschild da
   energia, `2π·r_s/c` com `r_s = 2GE/c⁴` (`monopole_time_is_the_horizon_light_time`), e a carga `q = GE/c⁴` é `r_s/2`
   (`charge_is_half_the_schwarzschild_radius`). É a identificação do ramo B (τ★ = k·GM/c³, k = 4π): a rota devolve a energia cujo
   horizonte tem o tempo τ★ — tautológica quanto à ESCALA; não a fixa. O ramo nativo (τ★ = t_P) dá `E_P/4π ≈ 9,7×10²⁶ eV` (conferido).
4. **A leitura autoconsistente do Nome pina a frequência ao inverso do seu próprio tempo.** Se a energia do modo é a sua própria
   leitura modular (`ħω = ħ·½τ★ω²`), então `ω = 2/τ★` (`self_consistent_readout_fixes_the_frequency`): com τ★ = t_P é planckiano
   (2E_P); com τ★ o horizonte da própria energia, `E = E_P/√(2π)`. A única escala que a estrutura {α, √e, ħ, c, G} oferece é Planck.

5. **O que a forma fixa é a razão** (`the_ratio_survives_the_rescaling`): a reescala do no-go muda E₀ e a massa pelo mesmo fator, e `m/E₀` não muda. A reescala corresponde à transposição do acorde
   (`LeiDoDiminuto.lerE0_transpor`): o no-go fala do valor ABSOLUTO de E₀; a Lei do Diminuto, do valor RELATIVO à tônica. Nesta pedra «escala» é a escala de energia; a escala musical é a da Lei do Diminuto.

## O que esta pedra NÃO afirma

* Não afirma que E₀ seja inderivável por QUALQUER princípio futuro: só que o formalismo ATUAL (ponte 1 e o que ela importa) não o fixa.
* Não toca β (a ponte 1 o carrega em `TGLCoupling`; β jamais entra literal), não abre dado, não move gate, selo nem veredito
  (`TGL_NU_M2_ARMED_CONSISTENT` segue). A tipagem GKSL de ρ_modular (taxa, não energia; `paper_PT.tex` §Radicalização) fica na
  conferência, não aqui.

Sem sorry, sem axiom novo (trio: propext, Classical.choice, Quot.sound).

> **01/11/2026 — NOME DO OPERADOR: «Tônica do Hamiltoniano»** (verbatim sha256 `1f16a74c05d9d4cb`) (antes `E0LiberdadeDeEscala`, nome provisório da gerência). E a ORDEM dele no mesmo ato: «eu não gostaria que ainda restasse hipóteses
> nomeadas, é preciso que esteja tudo derivado». A seção «OS CAMPOS FECHADOS», no fim do módulo, responde à ordem até onde a matemática alcança: o que era CAMPO de
> estrutura passa a ser CONSTRUÍDO a partir de teoremas do kernel; a leitura física não vira teorema (notas AO LADO, abaixo). O que resta de entrada é o acoplamento `c` (β = α·√e; α medido
> por dentro, não derivado) e o Um POSTO (`u = 1`, o `echo 1`: posição, não hipótese — 05/10/2026). O nome dele lê as duas metades de uma frase só (31/10: «E0 não é absolutamente livre, porque a escala (pentada) já definiu pelo hamiltoniano oculto»): o no-go diz que a FORMA da inscrição não fixa E₀; `the_tonic_lands_on_the_posted_unit` diz onde a escala fica: na unidade POSTA que a tônica carrega (o √e vem do acoplamento e o diminuto o desfaz). O no-go não cai: a liberdade de escala é exatamente a do Um posto.


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

namespace TGLExt.TonicaDoHamiltoniano

open TGLExt.PonteDaMassa
open TGLExt.LeiDoDiminuto
open TGLExt.ProjecaoTransversalDaMeiaNat

/-! ### 1. A liberdade de escala -/

/-- [DEF] **a transição reescalada**: a MESMA inscrição (acoplamento `c`, ângulo autoconjugado `θ`) com `E₀ ↦ λ·E₀`, `λ > 0`. -/
noncomputable def reescala (T : TransicaoParaAMassa) (lam : ℝ) (hl : 0 < lam) : TransicaoParaAMassa where
  c := T.c
  E0 := lam * T.E0
  E0_pos := mul_pos hl T.E0_pos
  theta := T.theta
  theta_nonneg := T.theta_nonneg
  theta_le := T.theta_le
  autoconjugado := T.autoconjugado

theorem reescala_c (T : TransicaoParaAMassa) (lam : ℝ) (hl : 0 < lam) : (reescala T lam hl).c = T.c := rfl
theorem reescala_theta (T : TransicaoParaAMassa) (lam : ℝ) (hl : 0 < lam) : (reescala T lam hl).theta = T.theta := rfl
theorem reescala_E0 (T : TransicaoParaAMassa) (lam : ℝ) (hl : 0 < lam) : (reescala T lam hl).E0 = lam * T.E0 := rfl

/-- [KERNEL] ★★★ **A MASSA DERIVADA ESCALA LINEARMENTE COM E₀**: a forma é a mesma, o número acompanha a escala. -/
theorem massa_derivada_reescala (T : TransicaoParaAMassa) (lam : ℝ) (hl : 0 < lam) :
    (reescala T lam hl).massaDerivada = lam * T.massaDerivada := by
  rw [TransicaoParaAMassa.massa_derivada_eq_beta_mul, TransicaoParaAMassa.massa_derivada_eq_beta_mul]
  show T.c.beta * (Real.sqrt 2 / 2) * (lam * T.E0) = lam * (T.c.beta * (Real.sqrt 2 / 2) * T.E0)
  ring

/-- [KERNEL] ★★ a forma do neutrino do kernel (`neutrinoMassForm`) é homogênea de grau 1 em E₀. -/
theorem neutrinoMassForm_reescala (c : TGLCoupling) (lam E0 : ℝ) :
    neutrinoMassForm c (lam * E0) = lam * neutrinoMassForm c E0 := by
  unfold neutrinoMassForm
  ring

/-- [KERNEL] ★★★ **O QUE A FORMA FIXA É A RAZÃO**: a reescala muda E₀ e a massa pelo mesmo fator, e `m/E₀` não muda. Corresponde à transposição do acorde. -/
theorem the_ratio_survives_the_rescaling (T : TransicaoParaAMassa) (lam : ℝ) (hl : 0 < lam) :
    (reescala T lam hl).massaDerivada / (reescala T lam hl).E0 = T.massaDerivada / T.E0 := by
  rw [massa_derivada_reescala, reescala_E0]
  exact mul_div_mul_left _ _ hl.ne'

/-- [KERNEL] ★★★ **A ESCALA É LIVRE**: toda transição admite, com a MESMA inscrição, qualquer reescalonamento positivo de E₀. -/
theorem the_scale_is_free (T : TransicaoParaAMassa) :
    ∀ lam : ℝ, 0 < lam → ∃ T' : TransicaoParaAMassa, T'.c = T.c ∧ T'.theta = T.theta ∧ T'.E0 = lam * T.E0 :=
  fun lam hl => ⟨reescala T lam hl, rfl, rfl, rfl⟩

/-- [DEF] um habitante explícito da transição: β = 1/2 (qualquer β ∈ (0,1) serve), E₀ = 1, θ = π/4. -/
noncomputable def exemplo : TransicaoParaAMassa where
  c := ⟨1 / 2, by norm_num, by norm_num⟩
  E0 := 1
  E0_pos := by norm_num
  theta := Real.pi / 4
  theta_nonneg := by positivity
  theta_le := by linarith [Real.pi_pos]
  autoconjugado := by
    rw [Real.sin_pi_div_four, half_sq]
    norm_num

/-- [KERNEL] ★★★ **NENHUMA FUNÇÃO DA INSCRIÇÃO FIXA E₀** (o no-go): não existe `f` tal que `E₀ = f(c, θ)` em toda transição —
    a mesma inscrição carrega E₀ = 1 e E₀ = 2. O que o formalismo atual prova é a FORMA `m₂/E₀`; a escala é um dado a mais. -/
theorem no_function_of_the_inscription_fixes_E0 :
    ¬ ∃ f : TGLCoupling → ℝ → ℝ, ∀ T : TransicaoParaAMassa, T.E0 = f T.c T.theta := by
  rintro ⟨f, hf⟩
  have h1 : exemplo.E0 = f exemplo.c exemplo.theta := hf exemplo
  have h2 : (reescala exemplo 2 (by norm_num)).E0 = f (reescala exemplo 2 (by norm_num)).c (reescala exemplo 2 (by norm_num)).theta :=
    hf (reescala exemplo 2 (by norm_num))
  have h3 : (2 : ℝ) * 1 = 1 := by
    calc (2 : ℝ) * 1 = (reescala exemplo 2 (by norm_num)).E0 := rfl
      _ = f (reescala exemplo 2 (by norm_num)).c (reescala exemplo 2 (by norm_num)).theta := h2
      _ = f exemplo.c exemplo.theta := rfl
      _ = exemplo.E0 := h1.symm
      _ = 1 := rfl
  norm_num at h3

/-! ### 2. A taxa de fronteira é a lei canônica na frequência do sistema -/

/-- [KERNEL] ★★ **Γ_B = β/τ★ É A LEI CANÔNICA LIDA EM ω★ = √2/τ★**: `½βτ★(√2/τ★)² = β/τ★`. Não é lei nova; é a escolha da frequência. -/
theorem gammaB_is_the_canonical_law_at_the_systems_frequency (β τ : ℝ) (hτ : τ ≠ 0) :
    (1 / 2) * β * τ * (Real.sqrt 2 / τ) ^ 2 = β / τ := by
  rw [div_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
  field_simp

/-! ### 3. A rota do monopolo é o horizonte do próprio sistema -/

/-- [KERNEL] ★★ **τ★ = 4πGE/c⁵ É O TEMPO DE LUZ DA CIRCUNFERÊNCIA DE SCHWARZSCHILD DA ENERGIA**: `2π·r_s/c`, `r_s = 2GE/c⁴`. -/
theorem monopole_time_is_the_horizon_light_time (G E c : ℝ) (hc : c ≠ 0) :
    4 * Real.pi * G * E / c ^ 5 = 2 * Real.pi * (2 * G * E / c ^ 4) / c := by
  field_simp
  ring

/-- [KERNEL] ★ a «carga do monopolo» `q = GE/c⁴` é metade do raio de Schwarzschild da energia. -/
theorem charge_is_half_the_schwarzschild_radius (G E c : ℝ) :
    G * E / c ^ 4 = (2 * G * E / c ^ 4) / 2 := by
  ring

/-! ### 4. A leitura autoconsistente pina a frequência ao próprio tempo -/

/-- [KERNEL] ★★ se a energia do modo é a sua própria leitura modular, `ħω = ħ·½τ★ω²`, então `ω = 2/τ★`. -/
theorem self_consistent_readout_fixes_the_frequency (ħ τ ω : ℝ) (hħ : ħ ≠ 0) (hτ : τ ≠ 0) (hω : ω ≠ 0)
    (h : ħ * ω = ħ * ((1 / 2) * τ * ω ^ 2)) : ω = 2 / τ := by
  have h1 : ω = (1 / 2) * τ * ω ^ 2 := mul_left_cancel₀ hħ h
  have h2 : ω * (1 - (1 / 2) * τ * ω) = 0 := by linear_combination h1
  rcases mul_eq_zero.mp h2 with h0 | h0
  · exact absurd h0 hω
  · rw [eq_div_iff hτ]
    linear_combination (-2 : ℝ) * h0


/-! ### 01/11/2026 — O NOME DO OPERADOR: «Tônica do Hamiltoniano» — o que a forma deixa livre, a tônica carrega: o Um posto -/

/-- [KERNEL] ★★ A FORMA NÃO FIXA E₀ (`the_scale_is_free`, acima); NA TÔNICA, A ESCALA É A UNIDADE POSTA: na lei construída (`LeiDoDiminuto.leiDerivada`), com a tônica
    `β/α · u = √e · u`, o diminuto pousa em `E₀ = u`. Identidade algébrica: o que fixa `E₀` é o `u` posto que a tônica carrega; o no-go não cai, ele se localiza no posto.
    A frase do operador: «E0 não é absolutamente livre, porque a escala (pentada) já definiu pelo hamiltoniano oculto». (Rebatizado em 01/11/2026, antes do selo: o nome
    anterior dizia que a tônica fixava; quem fixa é o posto.) -/
theorem the_tonic_lands_on_the_posted_unit (c : TGLCoupling) (u : ℝ) (hu : 0 < u) :
    (leiDerivada c u hu).transicao.E0 = u :=
  leiDerivada_E0 c u hu

/-- [KERNEL] ★★ NO UM POSTO: `E₀ = 1` e `m = β·√2/2` (a FORMA, sob a leitura `massaDerivada` [ONTO]). -/
theorem the_tonic_at_the_posted_one (c : TGLCoupling) :
    (leiDerivada c 1 one_pos).transicao.E0 = 1 ∧
      (leiDerivada c 1 one_pos).transicao.massaDerivada = c.beta * (Real.sqrt 2 / 2) :=
  leiDerivada_no_um_posto c

end TGLExt.TonicaDoHamiltoniano

#print axioms TGLExt.TonicaDoHamiltoniano.reescala_c
#print axioms TGLExt.TonicaDoHamiltoniano.reescala_theta
#print axioms TGLExt.TonicaDoHamiltoniano.reescala_E0
#print axioms TGLExt.TonicaDoHamiltoniano.massa_derivada_reescala
#print axioms TGLExt.TonicaDoHamiltoniano.neutrinoMassForm_reescala
#print axioms TGLExt.TonicaDoHamiltoniano.the_ratio_survives_the_rescaling
#print axioms TGLExt.TonicaDoHamiltoniano.the_scale_is_free
#print axioms TGLExt.TonicaDoHamiltoniano.no_function_of_the_inscription_fixes_E0
#print axioms TGLExt.TonicaDoHamiltoniano.gammaB_is_the_canonical_law_at_the_systems_frequency
#print axioms TGLExt.TonicaDoHamiltoniano.monopole_time_is_the_horizon_light_time
#print axioms TGLExt.TonicaDoHamiltoniano.charge_is_half_the_schwarzschild_radius
#print axioms TGLExt.TonicaDoHamiltoniano.self_consistent_readout_fixes_the_frequency
#print axioms TGLExt.TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit
#print axioms TGLExt.TonicaDoHamiltoniano.the_tonic_at_the_posted_one
