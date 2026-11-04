import TGLExt.PonteDaMassa
import TGLExt.TheLedgerOfCharges
import TGLExt.TheSelectionIsTheBallast
import TGLExt.TheVerbalCoupling
set_option autoImplicit false

/-!
Pedra da gerencia c1 (02/11/2026); NOME RATIFICADO pelo operador em 03/11/2026 (verbatim sha16 `73466598d3419fb0`: «concordo com todos os nomes e os ratifico»); entra no kernel na v407; compilada no sandbox da v407 (k407c/final), so no trio.

Cunhagens do operador (02/11/2026): «K e a tangente; e como se fosse o acorde sendo tocado» e «Decidir e crivar».

O que esta pedra faz, por termo, sobre o que o kernel ja tem:
* `K θ := tan θ` e a razao projecao/derivada da projecao transversal (`projecao_hasDerivAt`), e `K² = |R|²/|T|²`
  nas amplitudes de `S(θ)` (`faceWeight`, `reflectionWeight`): a raiz da razao custo/pagamento.
* O CRIVO e `K = 1`. Em `[0, π/2)` ele deixa passar um unico angulo, `π/4`: o posto (`injOn_tan`, `tan_pi_div_four`).
  A mesma forma do piso (`the_floor_fixes_the_cut`: `e^{-a} = 1 ↔ a = 0`), sem ligacao de termo com ela.
* O angulo da selecao justa (peso ½, `selectionAngle`, ja no kernel) passa pelo crivo; o angulo de Miguel
  (`thetaMiguel`, peso β) nao passa: la `K² = β/(1 − β) < 1`.
* A massa lida no acorde (a derivada, `massaDerivada`) e a massa lida na projecao dividida por `K`. Em TODA
  `TransicaoParaAMassa` vale θ = π/4 (teorema `theta_eq_pi_div_four`, derivado do campo `autoconjugado`), logo K = 1
  sempre: a divisao e por 1, e `no_posto_o_acorde_e_a_projecao` repete `massa_derivada_eq_projecao` (PonteDaMassa.lean:181)
  na forma de K. O conteudo desta pedra e a FORMA `massa = projecao / K`, nao um fato novo (dito, revisao Sonnet 02/11). Que a massa seja o acorde e nao a escala (o peso,
  `massaProporcional`) segue DEFINICAO do operador [ONTO]; a pedra da-lhe a forma, nao a deriva.
* `transicaoLida`: a transicao com o angulo dado pela regra da selecao, `selectionAngle (1/2)`. O numero ½ SEGUE
  ESCRITO na definicao; `o_angulo_e_lido_do_absoluto` mostra so que esse ½ coincide com o peso da face absoluta
  (`peso_da_face_absoluta`, por `rw`): COINCIDENCIA DE VALOR, nao ponte, como o kernel ja avisa (PonteDaMassa.lean:245-246,
  275-276). A hipotese nao some nem muda de lugar; a regra de leitura ja era termo. Coincide com `transicaoDerivada`.

Homonimos: este K (tangente do angulo lido) nao e o K de Hubble, nem o K modular, nem `genK` (TheAngleIsTheProjection.lean:76,
o gerador 2×2); «posto» aqui e o angulo π/4 da selecao justa, nao o Um POSTO do `echo 1` nem o posto como cargo. Dito para nao
encadear homonimos; a ponte e leitura.
-/

namespace TGLExt.KEhATangente

open TGLExt TGLExt.PonteDaMassa TGLExt.ProjecaoTransversalDaMeiaNat TGLExt.TheLedgerOfCharges

/-- K: a tangente do angulo lido. -/
noncomputable def K (θ : ℝ) : ℝ := Real.tan θ

/-- o crivo: `K = 1`. -/
def crivo (θ : ℝ) : Prop := K θ = 1

/-- K e a projecao transversal dividida pela sua derivada. -/
theorem K_eq_projecao_div_derivada (θ : ℝ) : K θ = projecaoTransversal θ / Real.cos θ := by
  unfold K projecaoTransversal
  rw [Real.tan_eq_sin_div_cos]

/-- `K² = |R|²/|T|²`: o quadrado da tangente e o custo sobre o pagamento, nas amplitudes de `S(θ)`. -/
theorem K_sq_eq_custo_div_pagamento (θ : ℝ) : K θ ^ 2 = reflectionWeight θ / faceWeight θ := by
  unfold K reflectionWeight faceWeight
  rw [normSq_reflection, normSq_transmission, Real.tan_eq_sin_div_cos, div_pow]

/-- o crivo deixa passar so o posto: em `[0, π/2)`, `K = 1 ↔ θ = π/4`. -/
theorem crivo_iff_posto (θ : ℝ) (h0 : 0 ≤ θ) (h1 : θ < Real.pi / 2) : crivo θ ↔ θ = Real.pi / 4 := by
  unfold crivo K
  constructor
  · intro h
    have hθ : θ ∈ Set.Ioo (-(Real.pi / 2)) (Real.pi / 2) := ⟨by linarith [Real.pi_pos], h1⟩
    have h4 : Real.pi / 4 ∈ Set.Ioo (-(Real.pi / 2)) (Real.pi / 2) :=
      ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩
    exact Real.injOn_tan hθ h4 (by rw [h, Real.tan_pi_div_four])
  · intro h
    rw [h, Real.tan_pi_div_four]

/-- a selecao justa (peso ½) passa pelo crivo. -/
theorem a_selecao_justa_passa : crivo (selectionAngle (1 / 2)) := by
  unfold crivo K
  rw [fair_selection_opens_forty_five, Real.tan_pi_div_four]

/-- no angulo de Miguel, `K² = β/(1 − β)`: a razao custo/pagamento da primeira reflexao. -/
theorem K_sq_no_angulo_de_miguel {β : ℝ} (h0 : 0 ≤ β) (h1 : β < 1) :
    K (thetaMiguel β) ^ 2 = β / (1 - β) := by
  have hs : Real.sin (thetaMiguel β) ^ 2 = β := by
    rw [sin_thetaMiguel h0 h1.le, Real.sq_sqrt h0]
  have hc : Real.cos (thetaMiguel β) ^ 2 = 1 - β := by
    have := Real.sin_sq_add_cos_sq (thetaMiguel β)
    linarith
  unfold K
  rw [Real.tan_eq_sin_div_cos, div_pow, hs, hc]

/-- o angulo de Miguel nao e o posto: com `β < ½`, `K² < 1`. -/
theorem miguel_nao_passa {β : ℝ} (h0 : 0 ≤ β) (h1 : β < 1 / 2) : K (thetaMiguel β) ^ 2 < 1 := by
  rw [K_sq_no_angulo_de_miguel h0 (by linarith), div_lt_one (by linarith)]
  linarith

/-- Miguel e o posto sao lidos pela MESMA regra: `thetaMiguel β = selectionAngle β`, por definicao. -/
theorem miguel_e_a_mesma_regra_de_leitura (β : ℝ) : thetaMiguel β = selectionAngle β := rfl

/-- Miguel aponta para o posto (operador, 02/11: «e angulo de abertura de leitura, reflete o posto, porque aponta
pra ele»): `K²` no angulo de Miguel vale 1 exatamente no peso do posto, `β = ½`; com `β < ½` nunca o alcanca. -/
theorem miguel_aponta_para_o_posto {β : ℝ} (h0 : 0 ≤ β) (h1 : β < 1) :
    K (thetaMiguel β) ^ 2 = 1 ↔ β = 1 / 2 := by
  rw [K_sq_no_angulo_de_miguel h0 h1, div_eq_one_iff_eq (by linarith : (1 - β) ≠ 0)]
  constructor <;> intro h <;> linarith

/-- a massa lida no acorde (a derivada) e a massa lida na projecao dividida por `K`. Como θ = π/4 em toda transicao
(`theta_eq_pi_div_four`), K = 1 e a divisao e por 1: a FORMA, nao um fato novo. -/
theorem massa_derivada_eq_projecao_div_K (T : TransicaoParaAMassa) :
    T.massaDerivada = T.massaProjecao / K T.theta := by
  have hc : Real.cos T.theta ≠ 0 := by
    rw [T.theta_eq_pi_div_four, Real.cos_pi_div_four]
    positivity
  have hs : Real.sin T.theta ≠ 0 := by
    rw [T.theta_eq_pi_div_four, Real.sin_pi_div_four]
    positivity
  unfold TransicaoParaAMassa.massaDerivada TransicaoParaAMassa.massaProjecao K
  rw [(projecao_hasDerivAt T.theta).deriv, Real.tan_eq_sin_div_cos]
  unfold projecaoTransversal
  field_simp

/-- no posto `K = 1`: o acorde (a derivada) e a projecao sao a mesma massa (repete `massa_derivada_eq_projecao`,
PonteDaMassa.lean:181, na forma de K). -/
theorem no_posto_o_acorde_e_a_projecao (T : TransicaoParaAMassa) :
    T.massaDerivada = T.massaProjecao := by
  rw [massa_derivada_eq_projecao_div_K]
  have h1 : K T.theta = 1 := by
    unfold K
    rw [T.theta_eq_pi_div_four, Real.tan_pi_div_four]
  rw [h1, div_one]

/-- a transicao com o angulo LIDO pela regra da selecao (peso ½), em vez de escrito. -/
noncomputable def transicaoLida (c : TGLCoupling) (u : ℝ) (hu : 0 < u) : TransicaoParaAMassa where
  c := c
  E0 := u
  E0_pos := hu
  theta := selectionAngle (1 / 2)
  theta_nonneg := by
    rw [fair_selection_opens_forty_five]
    positivity
  theta_le := by
    rw [fair_selection_opens_forty_five]
    linarith [Real.pi_pos]
  autoconjugado := by
    rw [selection_angle_reflection (by norm_num) (by norm_num)]
    norm_num

/-- o angulo da transicao lida, `selectionAngle (1/2)`, coincide com o peso da face absoluta passado pela mesma regra
(`peso_da_face_absoluta`): o ½ esta escrito na definicao e a igualdade e um `rw`; coincidencia de valor, nao ponte. -/
theorem o_angulo_e_lido_do_absoluto {n : Type} [Fintype n] [DecidableEq n] [Nonempty n]
    {Γ : Matrix n n ℂ} (hΓ : Γ.trace = 0) (c : TGLCoupling) (u : ℝ) (hu : 0 < u) :
    (transicaoLida c u hu).theta = selectionAngle ((gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 + Γ))).re) := by
  show selectionAngle (1 / 2) = _
  rw [peso_da_face_absoluta hΓ]

/-- a transicao lida coincide com a construida: mesmo angulo, mesma massa `β · √2/2 · u`. -/
theorem transicao_lida_eq_derivada (c : TGLCoupling) (u : ℝ) (hu : 0 < u) :
    (transicaoLida c u hu).theta = (transicaoDerivada c u hu).theta ∧
    (transicaoLida c u hu).massaDerivada = c.beta * (Real.sqrt 2 / 2) * u :=
  ⟨by
    show selectionAngle (1 / 2) = Real.pi / 4
    exact fair_selection_opens_forty_five,
   (transicaoLida c u hu).massa_derivada_eq_beta_mul⟩

end TGLExt.KEhATangente
