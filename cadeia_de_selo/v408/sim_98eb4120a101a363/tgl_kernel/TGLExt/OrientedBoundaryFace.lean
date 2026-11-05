import TGLExt.ThermodynamicFriedmann

set_option autoImplicit false
set_option linter.unusedVariables false

/-!
# A ORIENTAÇÃO É O SINAL: qual face fecha o balanço de Clausius
  [TGLExt — v367; a pedra pedida pelo operador em 17/09/2026]

Correção do operador (17/09/2026) [INPUT/ONTO]: «o acoplamento é negativo e isso aparece na
lagrangiana, mas a geometria é positiva»; «o sinal invertido neste caso demonstra a paridade
inversa ao acoplamento, se a entrada tiver a geometria negativa a saída obedecerá a métrica
invertida no sinal».

A pedra B4 (`ThermodynamicFriedmann`) recebe a lei de entropia modificada como CAMPO DE ENTRADA
(`differential_entropy : entropyRate = dA/(4·G·Φ)`) e não diz em QUE FACE ela está escrita. Esta
pedra tipa essa orientação e prova que ela É o sinal do efeito na métrica:

* a paridade inversa (JKJ = −K) entra como campo: o valor lido na face espelhada é o oposto do
  valor lido na face do acoplamento;
* pela primeira lei modular (δS = δ⟨K⟩, lida na face que fecha o balanço), o Φ da B4 é
  Φ = (1 + s)⁻¹, com s o incremento dessa face;
* consequência EXATA: a face do acoplamento dá Φ < 1 (em primeira ordem, δ ↦ −δ) e a face
  espelhada dá Φ > 1 (o que o programa implementou); a diferença é 2δ/(1 − δ²);
* o fator implementado, 1 + δ, é a face espelhada em PRIMEIRA ORDEM, com resto nomeado
  δ²/(1 − δ).

O que esta pedra NÃO faz: não escolhe a face (a escolha é um BIT nomeado, [INPUT], e a leitura do
operador é que a entrada tem geometria negativa); não deriva δ = β|1+w| (isso é da B1/B4 e do
artigo); não olha para nenhum dado; não move gate. Nenhuma lacuna de prova e nenhum axioma novo.
-/

namespace TGLExt.OrientedFace

open ChatgptAudit.FLRW

/-- As duas faces da fronteira modular: aquela em que o acoplamento age e o espelho dela. -/
inductive Face where
  | coupling : Face
  | mirror : Face

/-- Os dados da orientação: a amplitude da resposta na face do acoplamento, a paridade inversa
    (o espelho inverte o gerador) e a primeira lei modular lida na face do acoplamento. -/
structure OrientedResponse where
  delta : ℝ
  delta_nonneg : 0 ≤ delta
  delta_lt_one : delta < 1
  gen : ℝ
  mirrorGen : ℝ
  parity : mirrorGen = -gen
  firstLaw : gen = delta

/-- O incremento de entropia por área lido na face que FECHA o balanço de Clausius. -/
def increment (R : OrientedResponse) : Face → ℝ
  | Face.coupling => R.gen
  | Face.mirror => R.mirrorGen

/-- [KERNEL] na face do acoplamento o incremento é a própria resposta (primeira lei). -/
theorem increment_coupling (R : OrientedResponse) : increment R Face.coupling = R.delta :=
  R.firstLaw

/-- [KERNEL] ★ a paridade inversa em ato: na face espelhada o incremento é o oposto. -/
theorem increment_mirror (R : OrientedResponse) : increment R Face.mirror = -R.delta := by
  show R.mirrorGen = -R.delta
  rw [R.parity, R.firstLaw]

/-- O Φ da pedra B4 lido da face que fecha o balanço: dS = dA(1 + s)/(4G) = dA/(4GΦ). -/
noncomputable def phiOf (R : OrientedResponse) (f : Face) : ℝ := (1 + increment R f)⁻¹

theorem phi_coupling (R : OrientedResponse) : phiOf R Face.coupling = (1 + R.delta)⁻¹ := by
  rw [phiOf, increment_coupling]

theorem phi_mirror (R : OrientedResponse) : phiOf R Face.mirror = (1 - R.delta)⁻¹ := by
  rw [phiOf, increment_mirror]
  ring_nf

/-- [KERNEL] ★ a face do acoplamento enfraquece a gravidade: Φ < 1. -/
theorem phi_coupling_lt_one (R : OrientedResponse) (h : 0 < R.delta) :
    phiOf R Face.coupling < 1 := by
  have h1 : (0:ℝ) < 1 + R.delta := by linarith
  have h2 : (1 + R.delta)⁻¹ * (1 + R.delta) = 1 := inv_mul_cancel₀ h1.ne'
  have h3 : (0:ℝ) < (1 + R.delta)⁻¹ := inv_pos.mpr h1
  rw [phi_coupling]
  nlinarith [h2, h3, h]

/-- [KERNEL] ★ a face espelhada reforça a gravidade: Φ > 1 (é o que o programa implementou). -/
theorem one_lt_phi_mirror (R : OrientedResponse) (h : 0 < R.delta) :
    1 < phiOf R Face.mirror := by
  have h1 : (0:ℝ) < 1 - R.delta := by linarith [R.delta_lt_one]
  have h2 : (1 - R.delta)⁻¹ * (1 - R.delta) = 1 := inv_mul_cancel₀ h1.ne'
  have h3 : (0:ℝ) < (1 - R.delta)⁻¹ := inv_pos.mpr h1
  rw [phi_mirror]
  nlinarith [h2, h3, h]

/-- [KERNEL] a distância exata entre as duas leituras: 2δ/(1 − δ²). -/
theorem phi_gap (R : OrientedResponse) (h : 0 < R.delta) :
    phiOf R Face.mirror - phiOf R Face.coupling = 2*R.delta/(1 - R.delta^2) := by
  have h1 : (1:ℝ) + R.delta ≠ 0 := by linarith
  have h2 : (1:ℝ) - R.delta ≠ 0 := by linarith [R.delta_lt_one]
  have h3 : (1:ℝ) - R.delta^2 ≠ 0 := by
    have hfac : (1:ℝ) - R.delta^2 = (1 - R.delta)*(1 + R.delta) := by ring
    rw [hfac]
    exact mul_ne_zero h2 h1
  rw [phi_mirror, phi_coupling]
  field_simp
  ring

/-- [KERNEL] ★★ o fator implementado (1 + δ) é a face ESPELHADA em primeira ordem, com o resto
    nomeado δ²/(1 − δ). -/
theorem mirror_is_one_plus_delta_to_first_order (R : OrientedResponse) :
    phiOf R Face.mirror = 1 + R.delta + R.delta^2/(1 - R.delta) := by
  have h2 : (1:ℝ) - R.delta ≠ 0 := by linarith [R.delta_lt_one]
  rw [phi_mirror]
  field_simp
  ring

/-- [KERNEL] ★★ a face do ACOPLAMENTO é, em primeira ordem, a troca δ ↦ −δ, com o resto
    nomeado δ²/(1 + δ). -/
theorem coupling_is_minus_delta_to_first_order (R : OrientedResponse) (h : 0 < R.delta) :
    phiOf R Face.coupling = 1 - R.delta + R.delta^2/(1 + R.delta) := by
  have h1 : (1:ℝ) + R.delta ≠ 0 := by linarith
  rw [phi_coupling]
  field_simp
  ring

/-- [KERNEL] ★★★ A ORIENTAÇÃO É O SINAL: escolher a face que fecha o balanço é escolher de que
    lado de 1 cai o fator da métrica, e as duas leituras distam 2δ/(1 − δ²). -/
theorem orientation_is_the_sign (R : OrientedResponse) (h : 0 < R.delta) :
    phiOf R Face.coupling < 1 ∧ 1 < phiOf R Face.mirror ∧
      phiOf R Face.mirror - phiOf R Face.coupling = 2*R.delta/(1 - R.delta^2) :=
  ⟨phi_coupling_lt_one R h, one_lt_phi_mirror R h, phi_gap R h⟩

/-- [KERNEL] ★★★ O RAMO DO ESTADO: se o balanço fecha na face em que a primeira lei foi lida — a
    face onde vive a matriz de densidade, antes da conjugação —, então o fator da métrica é MENOR
    que 1 e é, em primeira ordem, a troca δ ↦ −δ, com o resto nomeado δ²/(1 + δ).
    [A escolha da face continua sendo o BIT de entrada; este teorema diz o que ela implica.] -/
theorem balance_on_the_state_face (R : OrientedResponse) (h : 0 < R.delta) :
    increment R Face.coupling = R.delta ∧ phiOf R Face.coupling < 1 ∧
      phiOf R Face.coupling = 1 - R.delta + R.delta^2/(1 + R.delta) :=
  ⟨increment_coupling R, phi_coupling_lt_one R h, coupling_is_minus_delta_to_first_order R h⟩

/-- [KERNEL] ★★ O RAMO CONJUGADO: se o balanço fecha na face conjugada, o incremento entra com o
    sinal oposto (paridade) e o fator é MAIOR que 1 — é o ramo que o programa implementou. -/
theorem balance_on_the_conjugate_face (R : OrientedResponse) (h : 0 < R.delta) :
    increment R Face.mirror = -R.delta ∧ 1 < phiOf R Face.mirror ∧
      phiOf R Face.mirror = 1 + R.delta + R.delta^2/(1 - R.delta) :=
  ⟨increment_mirror R, one_lt_phi_mirror R h, mirror_is_one_plus_delta_to_first_order R⟩

/-- [KERNEL] a ponte com a B4: com o Φ da face escolhida, a segunda equação de Friedmann sai do
    balanço de Clausius já existente — a pedra nova não refaz a B4, ela a orienta. -/
theorem friedmann_of_face (R : OrientedResponse) (f : Face) (H : ℝ → ℝ) (t G enthalpy : ℝ)
    (D : HubbleHorizonInput H t G (phiOf R f) enthalpy) :
    deriv H t = -4*Real.pi*G*(phiOf R f)*enthalpy :=
  tgl_second_friedmann_from_clausius H t G (phiOf R f) enthalpy D

/-- [KERNEL] o fator da B4 (`entropyFactor`) é o primeiro termo da face espelhada quando a
    resposta é a da Ponte, δ = β|1 + w|. -/
theorem entropyFactor_is_one_plus_response (c : TGLCoupling) (w : ℝ) (R : OrientedResponse)
    (h : R.delta = c.beta*|1 + w|) : entropyFactor c w = 1 + R.delta := by
  rw [h, entropyFactor]

end TGLExt.OrientedFace
