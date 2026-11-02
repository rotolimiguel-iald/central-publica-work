import TGLExt.PonteDaMassaTransversal
import TGLExt.BoostHeatConstruction
import TGLExt.ThePsionAndTheViscosity
import TGLExt.O16.PeriodHeatCalibration_v3

set_option autoImplicit false

/-!
# O EMPRÉSTIMO DA MASSA — a segunda ponte: a massa como resíduo do acoplamento, e o que cada volta do relógio paga
[pedra candidata; nome PROVISÓRIO da sessão-espelho (claude-espelho), 30/10/2026 — o nome é do operador]

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

* **«a massa é o produto do acoplamento»** (`massa_e_produto_do_acoplamento`): a massa da primeira ponte é
  `β · (√2/2) · E₀` — o acoplamento vezes a projeção transversal da energia inscrita;
* **«o único objeto sem massa com acoplamento gravitacional é o fóton»** (`foton_sem_massa`,
  `acoplamento_positivo_da_massa`): com acoplamento zero nada fica retido — massa zero, toda a energia atravessa
  (o fóton acopla pela energia que carrega, não por massa); com acoplamento positivo há massa e a transmissão é
  estritamente menor que o incidente;
* **«não é origem, mas o resíduo»** (`massa_e_o_residuo`): a massa é o incidente menos o transmitido, lido na projeção
  transversal — o que fica depois da peneira;
* **o empréstimo** (`Emprestimo`): o principal é a massa inscrita; a parcela é o custo cobrado em UMA volta do relógio do
  boost (tempo modular = o período derivado, `κ·P = 2π`, `uma_volta`); **a parcela nunca quita**
  (`parcela_nunca_quita`: `0 < parcela < 1` em toda volta — o kernel já dizia «a cobrança nunca se completa»); **o juro é
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
eletromagnetismo — a «ligação que ainda falta» nas palavras do operador (tensão → atrito → temperatura → magnetismo)
tem no kernel a tensão (`frameCovectorStress`), o atrito constante `βg` (`viscosity_is_the_constant_friction`) e a
temperatura derivada `κ/2π` (`reciprocal_temperature`), e NÃO tem o magnetismo; a identificação «acoplamento da onda =
massa inscrita» é hipótese nomeada [ONTO]; `a`, `c`, `η`, `g`, `κ` são parâmetros do modelo da tela ótica [INPUT]; não
abre dado; não move o gate.
-/

namespace TGLExt.EmprestimoDaMassa

open Filter Topology
open scoped Topology
open TGLExt.PonteDaMassaTransversal TGLExt.PonteDaMassaTransversal.TransicaoParaAMassa
open TGLExt.ThePsionAndTheViscosity
open ChatgptAudit.Boost044 ChatgptAudit.PolarPeriod016

/-- A forma da massa para um acoplamento genérico `b` (inclusive `b = 0`, o fóton): `b · (√2/2) · E₀`. -/
noncomputable def massaForma (b E0 : ℝ) : ℝ := b * (Real.sqrt 2 / 2) * E0

/-- A energia transmitida para um acoplamento genérico `b`: `(1 − b) · E₀`. -/
noncomputable def transmitidaForma (b E0 : ℝ) : ℝ := (1 - b) * E0

/-- [★] «a massa é o produto do acoplamento luminodinâmico»: a massa da primeira ponte é `β` vezes a projeção
transversal da energia inscrita. -/
theorem massa_e_produto_do_acoplamento (T : TransicaoParaAMassa) :
    T.massaDerivada = massaForma T.c.beta T.E0 :=
  T.massa_derivada_eq_beta_mul

/-- [★★] «o único objeto sem massa com acoplamento gravitacional é o fóton»: com acoplamento zero nada fica retido —
a massa é zero e toda a energia atravessa. O fóton acopla pela energia que carrega, não por massa. -/
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

/-- O EMPRÉSTIMO — hipóteses nomeadas: a massa inscrita (primeira ponte), o contraste `g`, o relógio do boost `κ`
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

/-- [★★] A parcela nunca quita: `0 < parcela < 1` — o empréstimo não se paga numa volta, nem em volta nenhuma finita. -/
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

end TGLExt.EmprestimoDaMassa

#print axioms TGLExt.EmprestimoDaMassa.massa_e_produto_do_acoplamento
#print axioms TGLExt.EmprestimoDaMassa.foton_sem_massa
#print axioms TGLExt.EmprestimoDaMassa.acoplamento_positivo_da_massa
#print axioms TGLExt.EmprestimoDaMassa.massa_e_o_residuo
#print axioms TGLExt.EmprestimoDaMassa.Emprestimo.uma_volta
#print axioms TGLExt.EmprestimoDaMassa.Emprestimo.parcela_nunca_quita
#print axioms TGLExt.EmprestimoDaMassa.Emprestimo.parcela_le_beta
#print axioms TGLExt.EmprestimoDaMassa.Emprestimo.parcela_le_beta'
#print axioms TGLExt.EmprestimoDaMassa.Emprestimo.principal_e_beta_vezes
#print axioms TGLExt.EmprestimoDaMassa.volta_paga_area
#print axioms TGLExt.EmprestimoDaMassa.area_por_volta_da_massa_inscrita
