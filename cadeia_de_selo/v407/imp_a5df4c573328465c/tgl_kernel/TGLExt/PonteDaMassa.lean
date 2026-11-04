import TGLExt.ProjecaoTransversalDaMeiaNat
import TGLExt.Posto
import TGLExt.ContinuousModularZero

set_option autoImplicit false

/-!
# A PONTE DA MASSA — a transição da identificação: ela entra como DEFINIÇÃO, e a forma é teorema dada essa definição
[pedra da sessão-espelho (claude-espelho), 30/10/2026, revista pela gerência c1 em 01/11/2026; nome do operador: «Ponte da Massa»; entra na v405]

## A ordem (30/10/2026; verbatim em
`work\experimento_espelho_30out\OPERADOR_30out_ordem_ponte_da_massa_transversal_verbatim.txt`, sha16 `493172b80e96eb60`)

> «consegue resolver o problema que ainda resta nomeado, a transição da identificação da massa com a projeção
> transversal, realizar a prova que falta, a ponte»

## As cunhagens que a pedra traduz (28/10/2026; verbatim em `work\projecao_transversal_28out\`)

> «Matéria não é proporcional ao raio de betatgl, foi isso que erramos, a matéria é a projeção do eixo transversal,
> e por isso meu ângulo agudo para o neutrino faz sentido, então a matéria não é proporcional, ela seria a derivada.»

## O que esta pedra prova (só álgebra sobre termos que o kernel já tem; nada do dado)

A pedra anterior (`ProjecaoTransversalDaMeiaNat`) derivou o `sen 45°` e deixou NOMEADA, fora do kernel, a identificação
«a massa é a projeção transversal». Esta pedra faz da identificação uma DEFINIÇÃO, nas palavras do operador — a massa é a
energia retida pela fronteira vezes a DERIVADA da projeção transversal no ponto inscrito — e prova:

* **a projeção transversal `sen θ` tem derivada `cos θ`** (`projecao_hasDerivAt`), e **no ponto autoconjugado a projeção
  É a sua própria derivada**: `cos(π/4) = sen(π/4)` (`deriv_eq_projecao_at_half`) — **e só ali**: em `[0, π/2]`,
  `sen θ = cos θ ↔ θ = π/4` (`projecao_eq_deriv_iff`). As duas falas do operador — «projeção do eixo transversal» e
  «ela seria a derivada» — são a MESMA leitura, e coincidem exatamente no ponto em que o estado inscrito é autoconjugado;
* **a energia incidente se reparte sem perda entre o retido e o transmitido** (`retida_add_transmitida`), e o retido é
  `β · E₀` pelo Teorema S-∂ (`energia_retida_eq`);
* **A PONTE** (`massa_derivada_eq_form`): sob as hipóteses nomeadas de `TransicaoParaAMassa` — o acoplamento `c`, a
  energia inscrita `E₀`, e o estado inscrito AUTOCONJUGADO (`x = 1 − x`, a Meia-Nat) —, a massa como derivada da
  projeção transversal é exatamente a forma do neutrino do programa, `β · sen 45° · E₀`. O `sen 45°` não é escolhido:
  é `cos(π/4)`, a derivada da projeção no único ângulo em que o estado é autoconjugado (`theta_eq_pi_div_four`);
* **o discriminante entre as duas leituras** (`massa_derivada_eq_sqrt_two_mul_proporcional`,
  `massa_proporcional_ne_derivada`): a leitura «proporcional» (peso `sen²θ`) difere da leitura «derivada» exatamente por
  `√2`. Em runtime (β = α√e, E₀ = 1 eV): 8,507 meV contra 6,016 meV — distinguíveis pelo dado; o programa arma a
  derivada;
* **controle negativo** (`controle_nao_autoconjugado`): num estado que NÃO é autoconjugado, projeção e derivada não
  coincidem — a ponte não é genérica, é do ponto fixo.

## O que esta pedra NÃO prova (dito antes)

Não deriva `E₀` (a escala «1 eV» segue DECLARADA; o dado pede ~1,02 eV); não deriva β (β = α√e é a regra, do axioma);
não prova que a massa do neutrino na natureza É esta grandeza — a identificação entra como DEFINIÇÃO nomeada
(`massaDerivada`), cunhagem do operador [ONTO], e quem a testa é o rito do neutrino (bilateral, regra de morte a 5σ);
não abre dado; não move o gate. Estatuto do que se prova: [KERNEL]; da definição: [ONTO/INPUT]; da escala: [INPUT].

> **01/11/2026 — NOME DO OPERADOR: «Ponte da Massa»** (verbatim sha256 `1f16a74c05d9d4cb`) (antes `PonteDaMassaTransversal`, nome provisório da gerência). E a ORDEM dele no mesmo ato: «eu não gostaria que ainda restasse hipóteses
> nomeadas, é preciso que esteja tudo derivado». A seção «OS CAMPOS FECHADOS», no fim do módulo, responde à ordem até onde a matemática alcança: o que era CAMPO de
> estrutura passa a ser CONSTRUÍDO a partir de teoremas do kernel; a leitura física não vira teorema (notas AO LADO, abaixo). O que resta de entrada é o acoplamento `c` (β = α·√e; α medido
> por dentro, não derivado) e o Um POSTO (`u = 1`, o `echo 1`: posição, não hipótese — 05/10/2026). Aqui: a autoconjugação vem de `absolute_faces_half` (no estado absoluto do kernel cada face pesa ½), o ângulo é derivado (π/4, único), a estrutura `TransicaoParaAMassa` fica como TIPO e passa a ser HABITADA por construção (`transicaoDerivada`), não por hipótese.


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

namespace TGLExt.PonteDaMassa

open TGLExt.ProjecaoTransversalDaMeiaNat

/-- A projeção transversal de um estado lido no ângulo `θ` do regime da projeção: a amplitude `sen θ`. -/
noncomputable def projecaoTransversal (θ : ℝ) : ℝ := Real.sin θ

/-- [★] A projeção transversal tem derivada `cos θ` em todo `θ`. -/
theorem projecao_hasDerivAt (θ : ℝ) : HasDerivAt projecaoTransversal (Real.cos θ) θ :=
  Real.hasDerivAt_sin θ

/-- `(√2/2)² = 1/2` — o peso transversal do ponto autoconjugado. -/
theorem half_sq : (Real.sqrt 2 / 2) ^ 2 = 1 / 2 := by
  rw [div_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
  norm_num

/-- [★★] NO PONTO AUTOCONJUGADO A PROJEÇÃO É A SUA PRÓPRIA DERIVADA: `cos(π/4) = sen(π/4)`. -/
theorem deriv_eq_projecao_at_half : Real.cos (Real.pi / 4) = Real.sin (Real.pi / 4) := by
  rw [Real.cos_pi_div_four, Real.sin_pi_div_four]

/-- [★★] E SÓ ALI: em `[0, π/2]`, `sen θ = cos θ ↔ θ = π/4`. -/
theorem projecao_eq_deriv_iff (θ : ℝ) (h0 : 0 ≤ θ) (h1 : θ ≤ Real.pi / 2) :
    Real.sin θ = Real.cos θ ↔ θ = Real.pi / 4 := by
  constructor
  · intro h
    have h' : Real.sin θ = Real.sin (Real.pi / 2 - θ) := by
      rw [Real.sin_pi_div_two_sub]
      exact h
    have hθ := Real.injOn_sin
      ⟨by linarith [Real.pi_pos], h1⟩
      ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩ h'
    linarith
  · intro h
    rw [h]
    exact deriv_eq_projecao_at_half.symm

/-- A energia retida pela fronteira: o peso da reflexão, `sen²θ_M · E₀`. -/
noncomputable def energiaRetida (c : TGLCoupling) (E0 : ℝ) : ℝ :=
  Real.sin (thetaMiguel c.beta) ^ 2 * E0

/-- A energia transmitida: o peso da transmissão, `cos²θ_M · E₀`. -/
noncomputable def energiaTransmitida (c : TGLCoupling) (E0 : ℝ) : ℝ :=
  Real.cos (thetaMiguel c.beta) ^ 2 * E0

/-- [★] O retido é `β · E₀` (Teorema S-∂: `sen²θ_M = β`). -/
theorem energia_retida_eq (c : TGLCoupling) (E0 : ℝ) : energiaRetida c E0 = c.beta * E0 := by
  unfold energiaRetida
  rw [Posto.sin_sq_thetaMiguel]

/-- [★] Nada se perde na fronteira: retido + transmitido = incidente (`sen² + cos² = 1`). -/
theorem retida_add_transmitida (c : TGLCoupling) (E0 : ℝ) :
    energiaRetida c E0 + energiaTransmitida c E0 = E0 := by
  unfold energiaRetida energiaTransmitida
  rw [← add_mul, Real.sin_sq_add_cos_sq, one_mul]

/-- A TRANSIÇÃO PARA A MASSA — os CAMPOS da leitura do operador (28 e 30/10/2026); desde 01/11/2026 habitados por construção
(`transicaoDerivada`, no fim do módulo), não por hipótese:
* `c`: o acoplamento da fronteira (β = sen²θ_M, Teorema S-∂);
* `E0`: a energia do estado fundamental inscrito [INPUT — «1 eV» no programa, DECLARADO];
* `theta`: o ângulo em que o estado inscrito é lido no regime da projeção;
* `autoconjugado`: o estado inscrito é autoconjugado — o seu peso transversal `sen²θ` satisfaz `x = 1 − x`
  (a Meia-Nat; `observer_inverse_projection_halfnat`). -/
structure TransicaoParaAMassa where
  c : TGLCoupling
  E0 : ℝ
  E0_pos : 0 < E0
  theta : ℝ
  theta_nonneg : 0 ≤ theta
  theta_le : theta ≤ Real.pi / 2
  autoconjugado : Real.sin theta ^ 2 = 1 - Real.sin theta ^ 2

namespace TransicaoParaAMassa

variable (T : TransicaoParaAMassa)

/-- [★] O estado inscrito autoconjugado é lido em 45°: `θ = π/4` (a Meia-Nat é o ângulo; unicidade). -/
theorem theta_eq_pi_div_four : T.theta = Real.pi / 4 := by
  have hx : Real.sin T.theta ^ 2 = 1 / 2 := half_from_self_conjugate _ T.autoconjugado
  exact forty_five_unique T.theta T.theta_nonneg T.theta_le hx

/-- A LEITURA DO OPERADOR, como DEFINIÇÃO [ONTO]: «a matéria não é proporcional, ela seria a derivada» —
a massa é a energia retida vezes a DERIVADA da projeção transversal no ponto inscrito. -/
noncomputable def massaDerivada : ℝ :=
  energiaRetida T.c T.E0 * deriv projecaoTransversal T.theta

/-- A leitura rival, «proporcional»: a energia retida vezes o PESO transversal `sen²θ` no ponto inscrito. -/
noncomputable def massaProporcional : ℝ :=
  energiaRetida T.c T.E0 * Real.sin T.theta ^ 2

/-- A leitura «projeção»: a energia retida vezes a PROJEÇÃO (amplitude) `sen θ` no ponto inscrito. -/
noncomputable def massaProjecao : ℝ :=
  energiaRetida T.c T.E0 * projecaoTransversal T.theta

/-- [★★★] A PONTE: a massa como derivada da projeção transversal, no ponto autoconjugado, É a forma do
neutrino do programa, `β · sen 45° · E₀`. O `sen 45°` não é postulado nem escolhido: é `cos(π/4)`, a derivada da
projeção no único ângulo em que o estado inscrito é autoconjugado. -/
theorem massa_derivada_eq_form : T.massaDerivada = neutrinoMassForm T.c T.E0 := by
  unfold massaDerivada neutrinoMassForm halfAmplitude
  rw [(projecao_hasDerivAt T.theta).deriv, T.theta_eq_pi_div_four, deriv_eq_projecao_at_half,
    energia_retida_eq]
  ring

/-- [★★] A forma explícita: `m = β · (√2/2) · E₀`. -/
theorem massa_derivada_eq_beta_mul : T.massaDerivada = T.c.beta * (Real.sqrt 2 / 2) * T.E0 := by
  rw [massa_derivada_eq_form]
  unfold neutrinoMassForm halfAmplitude
  rw [Real.sin_pi_div_four]

/-- [★★] Derivada e projeção coincidem no ponto inscrito: «projeção do eixo transversal» e «ela seria a derivada»
são a MESMA leitura em 45°. -/
theorem massa_derivada_eq_projecao : T.massaDerivada = T.massaProjecao := by
  have h : deriv projecaoTransversal T.theta = projecaoTransversal T.theta := by
    rw [(projecao_hasDerivAt T.theta).deriv, T.theta_eq_pi_div_four]
    exact deriv_eq_projecao_at_half
  unfold massaDerivada massaProjecao
  rw [h]

/-- [★★ — o DISCRIMINANTE] A leitura «proporcional» (peso) difere da leitura «derivada» exatamente por `√2`:
`m_derivada = √2 · m_proporcional`. Em runtime (β = α√e, E₀ = 1 eV): 8,507 meV contra 6,016 meV. -/
theorem massa_derivada_eq_sqrt_two_mul_proporcional :
    T.massaDerivada = Real.sqrt 2 * T.massaProporcional := by
  unfold massaDerivada massaProporcional
  rw [(projecao_hasDerivAt T.theta).deriv, T.theta_eq_pi_div_four, Real.cos_pi_div_four,
    Real.sin_pi_div_four, half_sq]
  ring

/-- A massa é positiva: `β > 0`, `E₀ > 0`, `cos(π/4) > 0`. -/
theorem massa_derivada_pos : 0 < T.massaDerivada := by
  rw [massa_derivada_eq_beta_mul]
  have h2 : 0 < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  have hb := T.c.beta_pos
  have he := T.E0_pos
  positivity

/-- [★★] As duas leituras NÃO coincidem: o par «proporcional / derivada» é um discriminante real, não um nome. -/
theorem massa_proporcional_ne_derivada : T.massaProporcional ≠ T.massaDerivada := by
  intro h
  have hs := T.massa_derivada_eq_sqrt_two_mul_proporcional
  have hpos : 0 < T.massaProporcional := by
    unfold massaProporcional
    rw [energia_retida_eq, T.theta_eq_pi_div_four, Real.sin_pi_div_four, half_sq]
    have hb := T.c.beta_pos
    have he := T.E0_pos
    positivity
  have h1 : (Real.sqrt 2 - 1) * T.massaProporcional = 0 := by
    rw [sub_mul, one_mul]
    linarith
  rcases mul_eq_zero.mp h1 with h3 | h3
  · have hq : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
    have h4 : Real.sqrt 2 = 1 := by linarith
    rw [h4] at hq
    norm_num at hq
  · exact absurd h3 (ne_of_gt hpos)

end TransicaoParaAMassa

/-- [controle negativo] Num estado que NÃO é autoconjugado (`sen²θ ≠ ½`), projeção e derivada NÃO coincidem:
a ponte não é genérica, é do ponto fixo. -/
theorem controle_nao_autoconjugado (θ : ℝ) (h0 : 0 ≤ θ) (h1 : θ ≤ Real.pi / 2)
    (h : Real.sin θ ^ 2 ≠ 1 / 2) : Real.sin θ ≠ Real.cos θ := by
  intro heq
  have hθ := (projecao_eq_deriv_iff θ h0 h1).mp heq
  apply h
  rw [hθ, Real.sin_pi_div_four, half_sq]


/-! ### 01/11/2026 — OS CAMPOS FECHADOS (ordem do operador: «é preciso que esteja tudo derivado»; os campos fecharam, a leitura física não virou teorema)

O que era CAMPO da estrutura vira CONSTRUÇÃO; isso fecha o campo, não deriva a leitura. (1) o VALOR ½ — no estado absoluto do kernel (`absoluteRho n = 1/n`, o
Gibbs do Hamiltoniano nulo, `K_abs = 0`) cada face de qualquer graduação de paridade pesa ½ (`absolute_faces_half`, `ContinuousModularZero`): teorema; que o estado
inscrito seja lido nesse peso é a leitura do operador [ONTO]; (2) o ÂNGULO — único em `[0, π/2]` com `sen² = ½` (`forty_five_unique`): teorema condicional a (1);
(3) a UNIDADE — o Um POSTO, `umPosto = 1` (o `echo 1`; posição, não hipótese — 05/10/2026). Entram o acoplamento `c` (β = α·√e; α medido por dentro, não derivado) e
as leituras `massaDerivada` e `θ = π/4`. -/

/-- [KERNEL] ★★ o peso da face no estado ABSOLUTO é ½, para toda graduação de paridade `Γ` (`Tr Γ = 0`) (`absolute_faces_half`). Isso é sobre o peso
    da face; que o estado inscrito seja lido nesse peso é a leitura do operador [ONTO]: coincidência de valor, não ponte. -/
theorem peso_da_face_absoluta {n : Type} [Fintype n] [DecidableEq n] [Nonempty n] {Γ : Matrix n n ℂ}
    (hΓ : Γ.trace = 0) :
    (gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 + Γ))).re = 1 / 2 := by
  rw [(absolute_faces_half hΓ).1]
  first
    | (norm_num; done)
    | (simp; done)
    | (simp [Complex.div_ofNat_re]; done)

/-- [KERNEL] ★★ SE a projeção transversal pesa o que a face absoluta pesa (a premissa `hθ`, que é a leitura), o ângulo é `π/4`: a conclusão é teorema, a premissa não. -/
theorem angulo_derivado_do_absoluto {n : Type} [Fintype n] [DecidableEq n] [Nonempty n] {Γ : Matrix n n ℂ}
    (hΓ : Γ.trace = 0) (θ : ℝ) (h0 : 0 ≤ θ) (h1 : θ ≤ Real.pi / 2)
    (hθ : Real.sin θ ^ 2 = (gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 + Γ))).re) : θ = Real.pi / 4 :=
  forty_five_unique θ h0 h1 (by rw [hθ, peso_da_face_absoluta hΓ])

/-- A TRANSIÇÃO CONSTRUÍDA (o nome `transicaoDerivada` fica): entram o acoplamento `c` e a unidade posta `u`; o ângulo `π/4` é ESCRITO aqui (é a leitura; nenhum teorema o
    deduz do estado inscrito); a autoconjugação é então a aritmética `sen²(π/4) = ½ = 1 − ½`. Os campos fecham; a leitura não vira teorema. -/
noncomputable def transicaoDerivada (c : TGLCoupling) (u : ℝ) (hu : 0 < u) : TransicaoParaAMassa where
  c := c
  E0 := u
  E0_pos := hu
  theta := Real.pi / 4
  theta_nonneg := by positivity
  theta_le := by linarith [Real.pi_pos]
  autoconjugado := by
    rw [Real.sin_pi_div_four, half_sq]
    norm_num

/-- [KERNEL] ★ o peso transversal da transição construída tem o MESMO VALOR do peso da face absoluta do kernel (½ = ½): coincidência de valor, conferida; a ponte entre
    os dois é a leitura, não este teorema. -/
theorem transicao_derivada_le_o_absoluto {n : Type} [Fintype n] [DecidableEq n] [Nonempty n] {Γ : Matrix n n ℂ}
    (hΓ : Γ.trace = 0) (c : TGLCoupling) (u : ℝ) (hu : 0 < u) :
    Real.sin (transicaoDerivada c u hu).theta ^ 2 = (gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 + Γ))).re := by
  rw [peso_da_face_absoluta hΓ]
  show Real.sin (Real.pi / 4) ^ 2 = 1 / 2
  rw [Real.sin_pi_div_four, half_sq]

/-- [KERNEL] ★★★ a massa da transição construída: `β · (√2/2) · u` (a definição `massaDerivada` aplicada a ela). -/
theorem massa_da_transicao_derivada (c : TGLCoupling) (u : ℝ) (hu : 0 < u) :
    (transicaoDerivada c u hu).massaDerivada = c.beta * (Real.sqrt 2 / 2) * u :=
  (transicaoDerivada c u hu).massa_derivada_eq_beta_mul

/-- O UM POSTO: a unidade é 1 — posição (o `echo 1`), não hipótese (05/10/2026). -/
noncomputable def umPosto : ℝ := 1

theorem umPosto_pos : 0 < umPosto := by
  unfold umPosto
  exact one_pos

/-- [KERNEL] ★★★ NO UM POSTO: `m = β · √2/2`. O que entra: o 1 posto, o acoplamento (β = α√e, α medido por dentro) e as leituras `massaDerivada` e `θ = π/4`. -/
theorem massa_no_um_posto (c : TGLCoupling) :
    (transicaoDerivada c umPosto umPosto_pos).massaDerivada = c.beta * (Real.sqrt 2 / 2) := by
  rw [massa_da_transicao_derivada]
  unfold umPosto
  ring

/-- [KERNEL] ★★ A TRANSIÇÃO EXISTE PARA TODO ACOPLAMENTO, com `E₀ = 1`, `θ = π/4` e `m = β·√2/2`: a estrutura é habitada por construção, logo nenhum CAMPO fica por supor.
    Isto NÃO prova que a massa do neutrino seja esta: `massaDerivada` e `θ = π/4` são a leitura do operador [ONTO]. (Rebatizado em 01/11/2026, antes do selo: o nome
    anterior, `nenhuma_hipotese_resta`, dizia mais do que o teorema.) -/
theorem a_transicao_existe_para_todo_acoplamento (c : TGLCoupling) :
    ∃ T : TransicaoParaAMassa, T.c = c ∧ T.E0 = 1 ∧ T.theta = Real.pi / 4 ∧
      T.massaDerivada = c.beta * (Real.sqrt 2 / 2) :=
  ⟨transicaoDerivada c umPosto umPosto_pos, rfl,
   (by first | rfl | (unfold umPosto; rfl) | (simp [transicaoDerivada, umPosto])), rfl, massa_no_um_posto c⟩

end TGLExt.PonteDaMassa

#print axioms TGLExt.PonteDaMassa.projecao_hasDerivAt
#print axioms TGLExt.PonteDaMassa.half_sq
#print axioms TGLExt.PonteDaMassa.deriv_eq_projecao_at_half
#print axioms TGLExt.PonteDaMassa.projecao_eq_deriv_iff
#print axioms TGLExt.PonteDaMassa.energia_retida_eq
#print axioms TGLExt.PonteDaMassa.retida_add_transmitida
#print axioms TGLExt.PonteDaMassa.TransicaoParaAMassa.theta_eq_pi_div_four
#print axioms TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_form
#print axioms TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_beta_mul
#print axioms TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_projecao
#print axioms TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_sqrt_two_mul_proporcional
#print axioms TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_pos
#print axioms TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_proporcional_ne_derivada
#print axioms TGLExt.PonteDaMassa.controle_nao_autoconjugado
#print axioms TGLExt.PonteDaMassa.peso_da_face_absoluta
#print axioms TGLExt.PonteDaMassa.angulo_derivado_do_absoluto
#print axioms TGLExt.PonteDaMassa.transicao_derivada_le_o_absoluto
#print axioms TGLExt.PonteDaMassa.massa_da_transicao_derivada
#print axioms TGLExt.PonteDaMassa.umPosto_pos
#print axioms TGLExt.PonteDaMassa.massa_no_um_posto
#print axioms TGLExt.PonteDaMassa.a_transicao_existe_para_todo_acoplamento
