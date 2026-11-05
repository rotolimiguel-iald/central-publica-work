import TGLExt.MassaTensaoPura
set_option autoImplicit false

/-!
Pedra da gerencia c1 (02/11/2026); NOME RATIFICADO pelo operador em 03/11/2026 (verbatim sha16 `73466598d3419fb0`: «concordo com todos os nomes e os ratifico»); entra no kernel na v407; compilada no sandbox da v407 (k407c/final), so no trio.

Pergunta do operador (02/11/2026, verbatim sha16 e36df7f1245c7f16, em work\cunhagens_13out): «Consegue derivar a ponte agora?» — a ponte atrito → temperatura da cadeia dele,
tensao → atrito → temperatura → magnetismo (registrada em `MassaTensaoPura`, sem aspas: e a sequencia, nao uma frase dele), com a leitura dele, verbatim:
«[parcela que mantém o balanço fechado a cada observação cíclica]=equilíbrio» e «o Atrito constante gera a viscosidade, que impede o zero absoluto, porque seu efeito é calor e isso
fractaliza o Um absoluto pelo decaimento de seu expoente».

O que esta pedra faz, por termo, sobre o que o kernel ja tem (nada do dado; nenhum gate se move):
* A TEMPERATURA DERIVADA `T := 1/P` e `κ/2π` no periodo fiel (`reciprocal_temperature`), e e positiva.
* O CALOR DA VOLTA e o atrito constante `βg` (`viscosity_is_the_constant_friction`) LIDO como energia, ħ = k_B = 1:
  isto e a leitura do operador [ONTO], tipada como definicao, nao derivada. A ENTROPIA DA VOLTA e Clausius: `δS = δQ/T`.
* ★ A PONTE (`o_atrito_lido_na_temperatura`): o que atravessa numa volta do relogio do boost, `e^{−Pβg}`, e `e^{−βg/T}` com
  `T = 1/P`. TRIVIAL POR DEFINICAO (algebra do expoente), dito: o nome e a leitura, o conteudo e a definicao. As duas pontas
  que o kernel tinha separadas (o atrito `βg` e a temperatura `κ/2π`) aparecem numa identidade so. «Peso de Boltzmann» e
  ROTULO [ONTO]: `βg` e uma taxa de decaimento, nao uma energia; a leitura «ħ = k_B = 1» e do operador.
* A PARCELA POR VOLTA e `1 − e^{−δS}` (`a_parcela_e_um_menos_o_peso`) e nunca excede `δS` (`a_parcela_nao_excede_a_entropia`,
  que e `parcela_le_beta` em forma de temperatura). Tem a FORMA de Clausius: `δS := δQ/T` e DEFINICAO desta pedra e `δQ := βg`
  e leitura do operador [ONTO]; nenhum balanco termodinamico e provado aqui.
* O EQUILIBRIO DAS CONTAS (operador): atravessado + cobrado = 1 em toda volta (`o_balanco_fecha_a_cada_volta`), re-exportacao
  de `the_charge_is_continuous_both_sides`, que o kernel marca TRIVIAL POR DEFINICAO (ThePsionAndTheViscosity.lean:87-88).
* A FRACTALIZACAO: depois de `n` voltas resta `(e^{−δS})^n` — o expoente decai linearmente nas voltas
  (`o_expoente_decai_por_volta`) — e a soma das parcelas de todas as voltas, cada uma a MESMA fracao do que restava,
  e exatamente 1 (`o_um_se_fractaliza`): o Um e a serie geometrica das suas parcelas.
* O ZERO ABSOLUTO: no periodo fiel `T = κ/2π > 0` (`o_zero_absoluto_nao_e_lido`); e no limite `T → 0⁺` a parcela
  quitaria numa volta (`no_zero_absoluto_a_parcela_quitaria`), o que `parcela_nunca_quita` proibe para todo periodo fiel.
  Esse limite e um CALCULO sobre a funcao generica `T ↦ 1 − e^{−q/T}`, `q > 0` arbitrario, nao sobre o modelo (nao usa `Emprestimo`).
  Que o ATRITO cause `T > 0` NAO e termo: no kernel `T > 0` vem de `κ > 0` (dado do boost). Dito antes.

Homonimos e entradas: a temperatura aqui e `1/P = κ/2π` do periodo fiel (`reciprocal_temperature`); o kernel a chama
«normalizacao herdada (sem Unruh/KMS)» (BoostHeatConstruction.lean:16), e que seja a temperatura de Unruh e [KNOWN] fora do
termo; nao e temperatura de laboratorio. `g` (o contraste) e `κ` sao dados livres de `Emprestimo` [INPUT]. O «calor da volta»
e a leitura do operador do coeficiente `βg`. O balanco de Clausius da tela otica (`boost_defect_with_derived_period`) e outro
objeto, nao ligado aqui por termo. `ThePsionAndTheViscosity.transmitted` e citado pelo nome inteiro porque `TGLExt.transmitted`
(TheDeathOfTheSignal.lean:60) e homonimo.
-/

namespace TGLExt.APonteDoAtrito

open TGLExt TGLExt.ThePsionAndTheViscosity TGLExt.MassaTensaoPura TGLExt.MassaTensaoPura.Emprestimo
open ChatgptAudit.PolarPeriod016
open Filter Topology
open scoped Topology

/-- a temperatura derivada do relogio do boost: `T = 1/P`. -/
noncomputable def temperatura (L : Emprestimo) : ℝ := 1 / L.period

/-- no periodo fiel, `T = κ/2π` (`reciprocal_temperature`). -/
theorem temperatura_e_kappa_sobre_dois_pi (L : Emprestimo) : temperatura L = L.kappa / (2 * Real.pi) :=
  reciprocal_temperature L.kappa_pos L.period_pos L.fiel

/-- a temperatura derivada e positiva: o periodo fiel nao le o zero absoluto. -/
theorem o_zero_absoluto_nao_e_lido (L : Emprestimo) : 0 < temperatura L := by
  unfold temperatura
  have := L.period_pos
  positivity

/-- o calor da volta: o atrito constante `βg` lido como energia (ħ = k_B = 1) — leitura do operador [ONTO]. -/
noncomputable def calorDaVolta (L : Emprestimo) : ℝ := L.T.c.beta * L.g

/-- a entropia da volta: `δS := δQ / T`. DEFINICAO com a forma de Clausius, nao teorema termodinamico. -/
noncomputable def entropiaDaVolta (L : Emprestimo) : ℝ := calorDaVolta L / temperatura L

/-- `δS = δQ · P`: a entropia da volta e o calor vezes o periodo. -/
theorem entropia_e_calor_vezes_periodo (L : Emprestimo) : entropiaDaVolta L = calorDaVolta L * L.period := by
  unfold entropiaDaVolta temperatura
  rw [div_div_eq_mul_div, div_one]

/-- `δS = 2π·δQ/κ`: a entropia da volta com a temperatura derivada escrita em `κ`. -/
theorem entropia_e_dois_pi_calor_sobre_kappa (L : Emprestimo) :
    entropiaDaVolta L = 2 * Real.pi * calorDaVolta L / L.kappa := by
  unfold entropiaDaVolta
  rw [temperatura_e_kappa_sobre_dois_pi, div_div_eq_mul_div]
  ring

/-- ★ A PONTE: o que atravessa numa volta, `e^{−Pβg}`, e `e^{−βg/T}` com `T = 1/P`. Trivial por definicao (algebra do
expoente), dito; «peso de Boltzmann» e rotulo [ONTO]. -/
theorem o_atrito_lido_na_temperatura (L : Emprestimo) :
    ThePsionAndTheViscosity.transmitted L.T.c.beta L.g L.period = Real.exp (-(calorDaVolta L / temperatura L)) := by
  unfold ThePsionAndTheViscosity.transmitted calorDaVolta temperatura
  congr 1
  rw [div_div_eq_mul_div, div_one]
  ring

/-- a parcela por volta e `1 − e^{−δS}`: a FORMA de Clausius, por definicao de `entropiaDaVolta`. -/
theorem a_parcela_e_um_menos_o_peso (L : Emprestimo) :
    L.parcelaPorVolta = 1 - Real.exp (-(entropiaDaVolta L)) := by
  show 1 - ThePsionAndTheViscosity.transmitted L.T.c.beta L.g L.period = _
  rw [o_atrito_lido_na_temperatura]
  rfl

/-- a parcela nunca excede a entropia de Clausius da volta (`parcela_le_beta` em forma de temperatura). -/
theorem a_parcela_nao_excede_a_entropia (L : Emprestimo) : L.parcelaPorVolta ≤ entropiaDaVolta L := by
  rw [entropia_e_calor_vezes_periodo]
  have h := L.parcela_le_beta
  have e : calorDaVolta L * L.period = L.T.c.beta * (L.g * L.period) := by
    unfold calorDaVolta
    ring
  rw [e]
  exact h

/-- o equilibrio das contas (operador): atravessado + cobrado = 1 em toda volta. Re-exportacao de
`the_charge_is_continuous_both_sides` (trivial por definicao no kernel; o nome e a leitura). -/
theorem o_balanco_fecha_a_cada_volta (L : Emprestimo) :
    ThePsionAndTheViscosity.transmitted L.T.c.beta L.g L.period + L.parcelaPorVolta = 1 :=
  the_charge_is_continuous_both_sides _ _ _

/-- depois de `n` voltas resta a `n`-esima potencia do peso: o expoente decai linearmente nas voltas. -/
theorem o_expoente_decai_por_volta (L : Emprestimo) (n : ℕ) :
    ThePsionAndTheViscosity.transmitted L.T.c.beta L.g (n * L.period) = (ThePsionAndTheViscosity.transmitted L.T.c.beta L.g L.period) ^ n := by
  unfold ThePsionAndTheViscosity.transmitted
  rw [← Real.exp_nat_mul]
  congr 1
  ring

/-- o peso de uma volta fica estritamente entre 0 e 1 (a cobranca nunca se completa, nunca e nula). -/
theorem o_peso_entre_zero_e_um (L : Emprestimo) :
    0 < ThePsionAndTheViscosity.transmitted L.T.c.beta L.g L.period ∧ ThePsionAndTheViscosity.transmitted L.T.c.beta L.g L.period < 1 := by
  have h := L.parcela_nunca_quita
  have hq : L.parcelaPorVolta = 1 - ThePsionAndTheViscosity.transmitted L.T.c.beta L.g L.period := rfl
  rw [hq] at h
  constructor <;> linarith [h.1, h.2]

/-- ★ o Um se fractaliza: a soma das parcelas de todas as voltas, cada uma a mesma fracao do que restava, e 1. -/
theorem o_um_se_fractaliza (L : Emprestimo) :
    ∑' n : ℕ, L.parcelaPorVolta * (ThePsionAndTheViscosity.transmitted L.T.c.beta L.g L.period) ^ n = 1 := by
  have h := o_peso_entre_zero_e_um L
  rw [tsum_mul_left, tsum_geometric_of_lt_one h.1.le h.2]
  have hq : L.parcelaPorVolta = 1 - ThePsionAndTheViscosity.transmitted L.T.c.beta L.g L.period := rfl
  rw [hq]
  exact mul_inv_cancel₀ (by linarith [h.2])

/-- no limite do zero absoluto a parcela quitaria numa volta: `1 − e^{−q/T} → 1` quando `T → 0⁺`, para `q > 0`.
Calculo sobre a funcao generica em `q`, nao sobre o modelo. O periodo fiel nao chega la (`o_zero_absoluto_nao_e_lido`,
`parcela_nunca_quita`). -/
theorem no_zero_absoluto_a_parcela_quitaria (q : ℝ) (hq : 0 < q) :
    Tendsto (fun T : ℝ => 1 - Real.exp (-(q / T))) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hinv : Tendsto (fun T : ℝ => T⁻¹) (𝓝[>] (0 : ℝ)) atTop := tendsto_inv_nhdsGT_zero
  have hmul : Tendsto (fun T : ℝ => q * T⁻¹) (𝓝[>] (0 : ℝ)) atTop := hinv.const_mul_atTop hq
  have hneg : Tendsto (fun T : ℝ => -(q * T⁻¹)) (𝓝[>] (0 : ℝ)) atBot := tendsto_neg_atTop_atBot.comp hmul
  have hexp : Tendsto (fun T : ℝ => Real.exp (-(q * T⁻¹))) (𝓝[>] (0 : ℝ)) (𝓝 0) :=
    Real.tendsto_exp_atBot.comp hneg
  have hsub : Tendsto (fun T : ℝ => (1 : ℝ) - Real.exp (-(q * T⁻¹))) (𝓝[>] (0 : ℝ)) (𝓝 (1 - 0)) :=
    tendsto_const_nhds.sub hexp
  rw [sub_zero] at hsub
  refine hsub.congr' (Filter.Eventually.of_forall fun T => ?_)
  simp only [div_eq_mul_inv]

end TGLExt.APonteDoAtrito
