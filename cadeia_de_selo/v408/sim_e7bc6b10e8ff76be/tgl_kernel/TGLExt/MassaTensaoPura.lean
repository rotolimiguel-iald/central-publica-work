import TGLExt.PonteDaMassa
import TGLExt.BoostHeatConstruction
import TGLExt.ThePsionAndTheViscosity
import TGLExt.O16.PeriodHeatCalibration_v3

set_option autoImplicit false

/-!
# MASSA = TENSÃO PURA (o empréstimo da massa) — a segunda ponte: a massa como resíduo do acoplamento, e o que cada volta do relógio paga
[pedra da sessão-espelho (claude-espelho), 30/10/2026, revista pela gerência c1 em 01/11/2026; nome do operador: «Massa=tensão pura»; entra na v405]

## A pergunta nas quatro línguas (30/10/2026, feita a pedido do operador antes do desenho)

«A massa é o que a volta paga e fecha, ou o que a volta deixa sem fechar? E, se é o que paga, de que lado se lê:
no que atravessa ou no que fica?» (TGL · teológica · linguística · jurídica; verbatim do pedido em
`OPERADOR_30out_segunda_ponte_pergunta_nas_quatro_linguas_verbatim.txt`, sha16 `f4d6cadf59bbfe37`).

## A resposta do operador (verbatim em `OPERADOR_30out_massa_e_emprestimo_residuo_do_acoplamento_verbatim.txt`,
sha16 `fdd78cac25c947a0`)

> «o único objeto sem massa com acoplamento gravitacional é o fóton, logo a massa não é originária da luz, mas do
> acoplamento, ela é o produto do acoplamento luminodinâmico. [...] eu penso que a massa seja um empréstimo então, e por
> isso precisa haver o pagamento do custo de betatgl, digo ser um empréstimo por ser residual neste caso, ela não é
> origem, mas o resíduo do acoplamento, a forma em que o acoplamento se inscreve.»

Onde a resposta cai nas três alternativas do balanço por volta (calor que atravessa · diferença de área que fica ·
defeito que não fecha): **a massa é o PRINCIPAL do empréstimo — o que fica inscrito (a diferença de área por volta) —,
a cobrança `β` é a PARCELA (o que cada volta paga), e o credor é o acoplamento (a luz que atravessa).** Não é o defeito:
sob Clausius o defeito é zero e a parcela é o que o mantém zero.

## O que esta pedra prova (só álgebra sobre termos que o kernel já tem; nada do dado)

* **«ela é o produto do acoplamento luminodinâmico»** (`massa_e_produto_do_acoplamento`): a massa da primeira ponte é
  `β · (√2/2) · E₀` — o acoplamento vezes a projeção transversal da energia inscrita;
* **«o único objeto sem massa com acoplamento gravitacional é o fóton»** (`foton_sem_massa`,
  `acoplamento_positivo_da_massa`): com acoplamento zero nada fica retido — massa zero, toda a energia atravessa
  (o fóton acopla pela energia que carrega, não por massa); com acoplamento positivo há massa e a transmissão é
  estritamente menor que o incidente. [REAL] `massaForma 0 E₀ = 0` é álgebra de uma forma genérica; [ONTO] `b = 0` é LIDO como o fóton:
  `TGLCoupling` exclui `b = 0`, e nenhum termo do kernel tem fóton;
* **«não é origem, mas o resíduo»** (`massa_e_o_residuo`): a massa é o incidente menos o transmitido, lido na projeção
  transversal — o que fica depois da peneira;
* **o empréstimo** (`Emprestimo`): o principal é a massa inscrita; a parcela é o custo cobrado em UMA volta do relógio do
  boost (tempo modular = o período derivado, `κ·P = 2π`, `uma_volta`); **a parcela nunca quita**
  (`parcela_nunca_quita`: `0 < parcela < 1` em toda volta — o kernel já dizia: a cobrança nunca se completa, `the_charge_never_completes`); **o juro é
  a regra**: a parcela por volta é no máximo `β · g · P = β · 2πg/κ` (`parcela_le_beta`, `parcela_le_beta'`); e principal
  e parcela carregam o mesmo `β` (`principal_e_beta_vezes`): o resíduo e o juro são o mesmo acoplamento;
* **a diferença de cada ciclo** (`volta_paga_area`): no modelo da tela ótica do kernel, o balanço de Clausius do
  segmento de boost (defeito/t² → 0 na origem) vale se e só se `η(a+c) = 2π · massa` — uma volta inteira (2π) da massa
  paga `η(a+c)`; logo a massa é `η(a+c)/(2π)`, a diferença de área por radiano de volta;
* **A SEGUNDA PONTE** (`area_por_volta_da_massa_inscrita`): se o acoplamento da onda de matéria do segmento de boost É a
  massa inscrita da primeira ponte (hipótese NOMEADA, lida no próprio argumento do defeito), então a área que uma volta
  paga é `η(a+c) = √2 · π · β · E₀` — a massa do neutrino escrita como diferença de área por volta do relógio.

## O que esta pedra NÃO prova (dito antes)

Não deriva `E₀`; não deriva β; não liga o defeito do ciclo à equação da torção (o fornecedor em forma fechada da v364
vive em `TracialDissipativeTorsion`, e a identificação do campo `A` com β segue [OPEN]); não tem termo algum de
eletromagnetismo — «ainda falta a ligação», nas palavras do operador (tensão → atrito → temperatura → magnetismo)
tem no kernel a tensão (`frameCovectorStress`), o atrito constante `βg` (`viscosity_is_the_constant_friction`) e a
temperatura derivada `κ/2π` (`reciprocal_temperature`), e NÃO tem o magnetismo; a identificação «acoplamento da onda =
massa inscrita» é hipótese nomeada [ONTO]; `a`, `c`, `η`, `g`, `κ` são parâmetros do modelo da tela ótica [INPUT]; não
abre dado; não move o gate.

> **01/11/2026 — NOME DO OPERADOR: «Massa=tensão pura»** (verbatim sha256 `1f16a74c05d9d4cb`) (antes `EmprestimoDaMassa`, nome provisório da gerência). E a ORDEM dele no mesmo ato: «eu não gostaria que ainda restasse hipóteses
> nomeadas, é preciso que esteja tudo derivado». A seção «OS CAMPOS FECHADOS», no fim do módulo, responde à ordem até onde a matemática alcança: o que era CAMPO de
> estrutura passa a ser CONSTRUÍDO a partir de teoremas do kernel; a leitura física não vira teorema (notas AO LADO, abaixo). O que resta de entrada é o acoplamento `c` (β = α·√e; α medido
> por dentro, não derivado) e o Um POSTO (`u = 1`, o `echo 1`: posição, não hipótese — 05/10/2026). Aqui: o período fiel deixa de ser campo (`one_turn_gives_faithful_period`, com `P = 2π/κ`), a transição vem derivada da primeira ponte, e o teorema `massa_e_tensao_pura` diz o que o nome diz: o principal é a energia RETIDA (`β·u`, o que fica tenso, sem parcela transmitida) projetada no transversal. Restam, como DADOS do sistema que lê (não hipóteses sobre a teoria), o contraste `g > 0` e o relógio `κ > 0`.


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

namespace TGLExt.MassaTensaoPura

open Filter Topology
open scoped Topology
open TGLExt.PonteDaMassa TGLExt.PonteDaMassa.TransicaoParaAMassa
open TGLExt.ThePsionAndTheViscosity
open ChatgptAudit.Boost044 ChatgptAudit.PolarPeriod016

/-- A forma da massa para um acoplamento genérico `b` (inclusive `b = 0`, o fóton): `b · (√2/2) · E₀`. -/
noncomputable def massaForma (b E0 : ℝ) : ℝ := b * (Real.sqrt 2 / 2) * E0

/-- A energia transmitida para um acoplamento genérico `b`: `(1 − b) · E₀`. -/
noncomputable def transmitidaForma (b E0 : ℝ) : ℝ := (1 - b) * E0

/-- [★] «ela é o produto do acoplamento luminodinâmico» (sob a leitura `massaDerivada` [ONTO]): a massa da primeira ponte é `β` vezes a projeção
transversal da energia inscrita. -/
theorem massa_e_produto_do_acoplamento (T : TransicaoParaAMassa) :
    T.massaDerivada = massaForma T.c.beta T.E0 :=
  T.massa_derivada_eq_beta_mul

/-- [★★] «o único objeto sem massa com acoplamento gravitacional é o fóton»: com acoplamento zero nada fica retido —
a massa é zero e toda a energia atravessa. O fóton acopla pela energia que carrega, não por massa. [REAL] é álgebra da forma genérica;
[ONTO] `b = 0` é lido como o fóton: `TGLCoupling` exclui `b = 0`. -/
theorem foton_sem_massa (E0 : ℝ) : massaForma 0 E0 = 0 ∧ transmitidaForma 0 E0 = E0 := by
  constructor
  · unfold massaForma
    ring
  · unfold transmitidaForma
    ring

/-- [★] Com acoplamento positivo há massa, e a transmissão é estritamente menor que o incidente. -/
theorem acoplamento_positivo_da_massa (b E0 : ℝ) (hb : 0 < b) (hE : 0 < E0) :
    0 < massaForma b E0 ∧ transmitidaForma b E0 < E0 := by
  constructor
  · unfold massaForma
    have h2 : 0 < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
    positivity
  · unfold transmitidaForma
    nlinarith [mul_pos hb hE]

/-- [★] «não é origem, mas o resíduo»: a massa é o incidente menos o transmitido, lido na projeção transversal —
o que fica depois da peneira. -/
theorem massa_e_o_residuo (b E0 : ℝ) :
    massaForma b E0 = (E0 - transmitidaForma b E0) * (Real.sqrt 2 / 2) := by
  unfold massaForma transmitidaForma
  ring

/-- O EMPRÉSTIMO — os campos (desde 01/11/2026 habitados por construção, `emprestimoDerivado`): a massa inscrita (primeira ponte), o contraste `g`, o relógio do boost `κ`
com período derivado `P` (a leitura angular identifica o tempo fielmente: `κ·P = 2π`). -/
structure Emprestimo where
  T : TransicaoParaAMassa
  g : ℝ
  g_pos : 0 < g
  kappa : ℝ
  kappa_pos : 0 < kappa
  period : ℝ
  period_pos : 0 < period
  fiel : AngularQuotientFaithful kappa period

namespace Emprestimo

variable (L : Emprestimo)

/-- O principal: a massa inscrita, `β · (√2/2) · E₀`. -/
noncomputable def principal : ℝ := L.T.massaDerivada

/-- A parcela: o custo cobrado em UMA volta do relógio do boost (tempo modular = o período derivado). -/
noncomputable def parcelaPorVolta : ℝ := charged L.T.c.beta L.g L.period

/-- [★] O período derivado é uma volta: `κ·P = 2π`. -/
theorem uma_volta : L.kappa * L.period = 2 * Real.pi := by
  have hP := positive_faithful_period L.kappa_pos L.period_pos L.fiel
  have hk : L.kappa ≠ 0 := ne_of_gt L.kappa_pos
  rw [hP]
  field_simp

/-- [★★] A parcela nunca quita: `0 < parcela < 1` — o empréstimo não se paga numa volta; para qualquer tempo finito, `the_charge_never_completes`. -/
theorem parcela_nunca_quita : 0 < L.parcelaPorVolta ∧ L.parcelaPorVolta < 1 :=
  the_charge_never_completes L.T.c.beta_pos L.g_pos L.period L.period_pos

/-- [★★] O juro é a regra: a parcela por volta é no máximo `β · g · P`. -/
theorem parcela_le_beta : L.parcelaPorVolta ≤ L.T.c.beta * (L.g * L.period) := by
  show 1 - Real.exp (-(L.period * L.T.c.beta * L.g)) ≤ L.T.c.beta * (L.g * L.period)
  have h := Real.add_one_le_exp (-(L.period * L.T.c.beta * L.g))
  have e : L.T.c.beta * (L.g * L.period) = L.period * L.T.c.beta * L.g := by ring
  linarith

/-- [★★] Com o período derivado: a parcela por volta é no máximo `β · 2πg/κ`. -/
theorem parcela_le_beta' : L.parcelaPorVolta ≤ L.T.c.beta * (2 * Real.pi * L.g / L.kappa) := by
  have h := L.parcela_le_beta
  have hP := positive_faithful_period L.kappa_pos L.period_pos L.fiel
  rw [hP] at h
  have e : L.T.c.beta * (L.g * (2 * Real.pi / L.kappa)) = L.T.c.beta * (2 * Real.pi * L.g / L.kappa) := by
    ring
  linarith

/-- [★] Principal e parcela carregam a mesma regra: o principal é `β` vezes a projeção transversal de `E₀` —
o resíduo e o juro são o mesmo acoplamento. -/
theorem principal_e_beta_vezes : L.principal = L.T.c.beta * ((Real.sqrt 2 / 2) * L.T.E0) := by
  unfold principal
  rw [massa_derivada_eq_beta_mul]
  ring

end Emprestimo

/-- [★★ — a diferença de cada ciclo] No modelo da tela ótica do kernel, o balanço de Clausius do segmento de boost
(defeito/t² → 0 na origem) vale se e só se `η(a+c) = 2π · massa`; logo a massa é a diferença de área por radiano de
volta: `massa = η(a+c)/(2π)`. Uma volta inteira da massa paga `η(a+c)`. -/
theorem volta_paga_area (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c) (rate mass eta : ℝ) (hrate : rate ≠ 0)
    (h : Tendsto (fun t => boostSegmentDefect a c rate mass eta t / t ^ 2) (𝓝[<] 0) (𝓝 0)) :
    mass = eta * (a + c) / (2 * Real.pi) := by
  have h1 := (boost_segment_quadratic_balance_iff a c ha hc rate mass eta hrate).mp h
  rw [eq_div_iff (by positivity : (2 : ℝ) * Real.pi ≠ 0)]
  linarith

/-- [★★★] A SEGUNDA PONTE: se o acoplamento da onda de matéria do segmento de boost É a massa inscrita da primeira
ponte (hipótese NOMEADA: o principal entra no lugar do acoplamento), então a área que uma volta do relógio paga é
`η(a+c) = √2 · π · β · E₀` — a massa do neutrino escrita como diferença de área por volta. -/
theorem area_por_volta_da_massa_inscrita (L : Emprestimo) (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c)
    (rate eta : ℝ) (hrate : rate ≠ 0)
    (h : Tendsto (fun t => boostSegmentDefect a c rate L.principal eta t / t ^ 2) (𝓝[<] 0) (𝓝 0)) :
    eta * (a + c) = Real.sqrt 2 * Real.pi * L.T.c.beta * L.T.E0 := by
  have h1 := (boost_segment_quadratic_balance_iff a c ha hc rate L.principal eta hrate).mp h
  rw [h1, L.principal_e_beta_vezes]
  ring


/-! ### 01/11/2026 — OS CAMPOS FECHADOS, e o nome do operador: «Massa=tensão pura» -/

/-- O EMPRÉSTIMO CONSTRUÍDO (o nome `emprestimoDerivado` fica): a transição construída da primeira ponte (sem campo aberto; a leitura `θ = π/4` está escrita nela), o relógio `κ` e o período de UMA volta `P = 2π/κ`,
    cuja fidelidade é TEOREMA (`one_turn_gives_faithful_period`), não campo. O que resta de entrada são os dados do sistema que lê —
    o contraste `g > 0` e o relógio `κ > 0` —, a unidade posta `u` e as leituras da nota AO LADO. -/
noncomputable def emprestimoDerivado (c : TGLCoupling) (u : ℝ) (hu : 0 < u) (g : ℝ) (hg : 0 < g) (κ : ℝ) (hκ : 0 < κ) :
    Emprestimo where
  T := transicaoDerivada c u hu
  g := g
  g_pos := hg
  kappa := κ
  kappa_pos := hκ
  period := 2 * Real.pi / κ
  period_pos := by positivity
  fiel := by
    have hk : κ ≠ 0 := ne_of_gt hκ
    refine one_turn_gives_faithful_period hk (Or.inl ?_)
    first
      | (field_simp; done)
      | (field_simp; ring)

/-- [KERNEL] a fidelidade derivada: uma volta, `κ·P = 2π`. -/
theorem emprestimo_derivado_uma_volta (c : TGLCoupling) (u : ℝ) (hu : 0 < u) (g : ℝ) (hg : 0 < g) (κ : ℝ) (hκ : 0 < κ) :
    (emprestimoDerivado c u hu g hg κ hκ).kappa * (emprestimoDerivado c u hu g hg κ hκ).period = 2 * Real.pi :=
  (emprestimoDerivado c u hu g hg κ hκ).uma_volta

/-- [KERNEL] ★★ o principal derivado: `β · (√2/2) · u`. -/
theorem principal_derivado (c : TGLCoupling) (u : ℝ) (hu : 0 < u) (g : ℝ) (hg : 0 < g) (κ : ℝ) (hκ : 0 < κ) :
    (emprestimoDerivado c u hu g hg κ hκ).principal = c.beta * (Real.sqrt 2 / 2) * u := by
  show (transicaoDerivada c u hu).massaDerivada = c.beta * (Real.sqrt 2 / 2) * u
  exact massa_da_transicao_derivada c u hu

/-- [KERNEL] a parcela derivada nunca quita: `0 < parcela < 1` (o kernel: `the_charge_never_completes`). -/
theorem parcela_derivada_nunca_quita (c : TGLCoupling) (u : ℝ) (hu : 0 < u) (g : ℝ) (hg : 0 < g) (κ : ℝ) (hκ : 0 < κ) :
    0 < (emprestimoDerivado c u hu g hg κ hκ).parcelaPorVolta ∧ (emprestimoDerivado c u hu g hg κ hκ).parcelaPorVolta < 1 :=
  (emprestimoDerivado c u hu g hg κ hκ).parcela_nunca_quita

/-- [KERNEL] ★★★ «Massa=tensão pura» (nome do operador, 01/11/2026; a leitura abaixo é da gerência, [ONTO]): o principal do
    empréstimo derivado é a ENERGIA RETIDA pela fronteira — `β·u`, o que fica tenso, sem parcela transmitida — projetada no transversal
    (`√2/2`). A massa não é o incidente nem o transmitido: é o retido, puro, lido na projeção. -/
theorem massa_e_tensao_pura (c : TGLCoupling) (u : ℝ) (hu : 0 < u) (g : ℝ) (hg : 0 < g) (κ : ℝ) (hκ : 0 < κ) :
    (emprestimoDerivado c u hu g hg κ hκ).principal = energiaRetida c u * (Real.sqrt 2 / 2) := by
  rw [principal_derivado, energia_retida_eq]
  ring

end TGLExt.MassaTensaoPura

#print axioms TGLExt.MassaTensaoPura.massa_e_produto_do_acoplamento
#print axioms TGLExt.MassaTensaoPura.foton_sem_massa
#print axioms TGLExt.MassaTensaoPura.acoplamento_positivo_da_massa
#print axioms TGLExt.MassaTensaoPura.massa_e_o_residuo
#print axioms TGLExt.MassaTensaoPura.Emprestimo.uma_volta
#print axioms TGLExt.MassaTensaoPura.Emprestimo.parcela_nunca_quita
#print axioms TGLExt.MassaTensaoPura.Emprestimo.parcela_le_beta
#print axioms TGLExt.MassaTensaoPura.Emprestimo.parcela_le_beta'
#print axioms TGLExt.MassaTensaoPura.Emprestimo.principal_e_beta_vezes
#print axioms TGLExt.MassaTensaoPura.volta_paga_area
#print axioms TGLExt.MassaTensaoPura.area_por_volta_da_massa_inscrita
#print axioms TGLExt.MassaTensaoPura.emprestimo_derivado_uma_volta
#print axioms TGLExt.MassaTensaoPura.principal_derivado
#print axioms TGLExt.MassaTensaoPura.parcela_derivada_nunca_quita
#print axioms TGLExt.MassaTensaoPura.massa_e_tensao_pura
