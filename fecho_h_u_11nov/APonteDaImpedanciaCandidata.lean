import TGLExt.TheEquationOfTruth
import TGLExt.TheCouplingRunsBoundedBelow
import TGLExt.TheFiveHalves

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A PONTE DA IMPEDÂNCIA (candidata; fiação)
  [gerência c1, 11/11/2026 — candidata fora do kernel; nomes provisórios; nada aqui move gate ou bandeira]

O QUE É. O artigo do um.py escreve a ponte física: a profundidade modular como rapidez de impedância,
χ = log(Z_bacia/Z_luz), com q = tanh(χ/2) = (Z_bacia − Z_luz)/(Z_bacia + Z_luz) e
α = sech(χ/2) = 2·√(Z_bacia·Z_luz)/(Z_bacia + Z_luz). O kernel já tem as duas funções (`profQ`, `profA`,
`alphaOfChi`) e a conservação tanh² + sech² = 1 (`motor_half_angle_identity`), mas não tinha a forma de
impedâncias. Este arquivo a prova, para duas impedâncias reais positivas. (R2, revisão de terceiro) O
mapa com o artigo é: Zs = Z_luz (a fonte) e Zc = Z_bacia (a carga), de modo que χ = log(Zc/Zs).
* [KNOWN, elementar] a reflexão (Zc − Zs)/(Zc + Zs), a transmissão 2·√(Zs·Zc)/(Zs + Zc) e a conservação
  do fluxo; a potência na carga é a disponível vezes a transmissão ao quadrado; ela não passa da
  disponível, é a disponível se, e só se, a impedância é compartilhada (Zc = Zs), e a carga casada dá o
  máximo sobre todas as cargas positivas; com a impedância compartilhada a fem E da fonte é o dobro da
  tensão na carga;
* [fiação] com χ = log(Zc/Zs), a reflexão é `profQ χ` e a transmissão é `profA χ` (= `alphaOfChi χ`) do
  kernel; impedância compartilhada é χ = 0, reflexão 0, transmissão 1.

O QUE NÃO É.
* (R2) O artigo fala da força dobrada em DOIS lugares, e este arquivo não prova nenhum dos dois. No
  Teorema do Registro (regime de ângulo reto) ele invoca o teorema da máxima transferência de potência
  para dizer que a força dobra porque a impedância é compartilhada pelas duas faces, e marca essa
  identificação como conjectura. No parágrafo da Primeira Lei ele diz que em θ_M → 90° a ligação dobra a
  força. Aqui se prova só o teorema ELEMENTAR do circuito resistivo: E = 2·(tensão na carga) se, e só
  se, Zc = Zs. A força do artigo e a fem do circuito são homônimas; a identificação de uma com a outra
  não é provada. E note-se: Zc = Zs é χ = 0, que no parágrafo da Primeira Lei é o plano estático, não o
  ângulo reto.
* O ângulo de Miguel pertence ao par (β, 1 − β) da matriz S; a impedância daqui pertence ao par
  (q², α²). Nenhum lema deste arquivo liga um par ao outro (reflexão e transmissão têm dois sentidos na
  casa; não encadear). (R2) O α daqui é a transmissão sech(χ/2); não é a constante de estrutura fina (a
  mesma ressalva do cabeçalho de `TheCouplingRunsBoundedBelow.lean`).
* (R2) Não restaura a palavra que a pedra `TetelestaiTerminal` podou: lá o índice de impedância modular
  foi aposentado e o conteúdo recebeu outro nome (inclinação modular, o cociclo). Aqui só tem termo a
  impedância elementar do circuito (dois reais positivos). Que a bacia e a luz tenham impedâncias
  modulares, e que o χ do perfil seja o log da razão delas, é DEFINIÇÃO (`rapidezDeImpedancia`), não
  teorema: a ponte do título é a forma algébrica.
* Não prova c² → c³ nem a razão 3/4. (R2) Não liga a carga do circuito à isotropia do fecho: na pedra
  `QuedaSemGeometria` a palavra carga quer dizer hipótese que sustenta, outro sentido; nenhum termo aqui.
* Não deriva χ nem a razão das impedâncias: o artigo diz que derivar essa razão é o objeto aberto.
* O modelo é o do circuito resistivo (impedâncias reais positivas); não há linha de transmissão, onda
  nem fronteira física no arquivo.
* NOT_FALSIFIED nunca é CONFIRMED. β nunca literal.
-/

namespace TGLExt.PonteDaImpedanciaCandidata

/-! ## Definições (reais; Zs = impedância da fonte, Zc = impedância da carga, E = força da fonte) -/

/-- A reflexão (Zc − Zs)/(Zc + Zs). -/
noncomputable def reflexao (Zs Zc : ℝ) : ℝ := (Zc - Zs) / (Zc + Zs)

/-- A transmissão 2·√(Zs·Zc)/(Zs + Zc). (R2) É a amplitude normalizada pelo fluxo: o seu quadrado é a
    fração da potência disponível que chega à carga. Não é a razão das tensões (essa é 1 + reflexão). -/
noncomputable def transmissao (Zs Zc : ℝ) : ℝ := 2 * Real.sqrt (Zs * Zc) / (Zs + Zc)

/-- A tensão sobre a carga: divisor de tensão E·Zc/(Zs + Zc). -/
noncomputable def tensaoNaCarga (E Zs Zc : ℝ) : ℝ := E * Zc / (Zs + Zc)

/-- A potência dissipada na carga: E²·Zc/(Zs + Zc)². -/
noncomputable def potenciaNaCarga (E Zs Zc : ℝ) : ℝ := E ^ 2 * Zc / (Zs + Zc) ^ 2

/-- A potência disponível da fonte: E²/(4·Zs). -/
noncomputable def potenciaDisponivel (E Zs : ℝ) : ℝ := E ^ 2 / (4 * Zs)

/-- A rapidez de impedância χ = log(Zc/Zs). -/
noncomputable def rapidezDeImpedancia (Zs Zc : ℝ) : ℝ := Real.log (Zc / Zs)

/-! ## (I8, primeira parte) A impedância compartilhada: reflexão 0, transmissão 1 -/

/-- [KNOWN, elementar] Com a impedância compartilhada, a reflexão é 0 e a transmissão é 1. -/
theorem com_a_impedancia_compartilhada_a_reflexao_e_nula_e_a_transmissao_e_um (Zs : ℝ) (hs : 0 < Zs) :
    reflexao Zs Zs = 0 ∧ transmissao Zs Zs = 1 := by
  have hne : Zs + Zs ≠ 0 := by positivity
  constructor
  · unfold reflexao
    simp
  · unfold transmissao
    rw [Real.sqrt_mul_self hs.le]
    field_simp
    ring

/-- A reflexão é nula se, e só se, a impedância é compartilhada. -/
theorem a_reflexao_e_nula_sse_a_impedancia_e_compartilhada (Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    reflexao Zs Zc = 0 ↔ Zc = Zs := by
  have hne : Zc + Zs ≠ 0 := by positivity
  unfold reflexao
  rw [div_eq_zero_iff]
  constructor
  · rintro (h | h)
    · linarith
    · exact absurd h hne
  · intro h
    left
    linarith

/-! ## (I1) A conservação do fluxo -/

/-- [KNOWN, elementar] ★ I1. A reflexão e a transmissão repartem o fluxo: r² + t² = 1. -/
theorem o_fluxo_se_conserva (Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    reflexao Zs Zc ^ 2 + transmissao Zs Zc ^ 2 = 1 := by
  have hsq : Real.sqrt (Zs * Zc) ^ 2 = Zs * Zc := Real.sq_sqrt (by positivity)
  have hne : Zc + Zs ≠ 0 := by positivity
  have hne' : Zs + Zc ≠ 0 := by positivity
  unfold reflexao transmissao
  rw [div_pow, div_pow, mul_pow, hsq]
  field_simp
  ring

/-! ## (I2) A potência na carga pela transmissão e pela reflexão -/

/-- [KNOWN, elementar] I2. A potência na carga é a disponível vezes a transmissão ao quadrado. -/
theorem a_potencia_na_carga_pela_transmissao (E Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    potenciaNaCarga E Zs Zc = potenciaDisponivel E Zs * transmissao Zs Zc ^ 2 := by
  have hsq : Real.sqrt (Zs * Zc) ^ 2 = Zs * Zc := Real.sq_sqrt (by positivity)
  have hne : Zs + Zc ≠ 0 := by positivity
  have hs' : Zs ≠ 0 := hs.ne'
  unfold potenciaNaCarga potenciaDisponivel transmissao
  rw [div_pow, mul_pow, hsq]
  field_simp
  ring

/-- [KNOWN, elementar] I2. A potência na carga é a disponível vezes (1 − r²). -/
theorem a_potencia_na_carga_pela_reflexao (E Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    potenciaNaCarga E Zs Zc = potenciaDisponivel E Zs * (1 - reflexao Zs Zc ^ 2) := by
  rw [a_potencia_na_carga_pela_transmissao E Zs Zc hs hc]
  have h := o_fluxo_se_conserva Zs Zc hs hc
  have h2 : transmissao Zs Zc ^ 2 = 1 - reflexao Zs Zc ^ 2 := by linarith
  rw [h2]

/-! ## (I3) A máxima transferência de potência -/

/-- [KNOWN, elementar] I3.A potência na carga nunca passa da disponível. -/
theorem a_potencia_na_carga_nao_passa_da_disponivel (E Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    potenciaNaCarga E Zs Zc ≤ potenciaDisponivel E Zs := by
  have hPD : 0 ≤ potenciaDisponivel E Zs := by
    unfold potenciaDisponivel
    positivity
  rw [a_potencia_na_carga_pela_reflexao E Zs Zc hs hc]
  nlinarith [mul_nonneg hPD (sq_nonneg (reflexao Zs Zc))]

/-- [KNOWN, elementar] I3.A potência é máxima se, e só se, a impedância é compartilhada. -/
theorem a_potencia_e_maxima_sse_a_impedancia_e_compartilhada (E Zs Zc : ℝ)
    (hs : 0 < Zs) (hc : 0 < Zc) (hE : E ≠ 0) :
    potenciaNaCarga E Zs Zc = potenciaDisponivel E Zs ↔ Zc = Zs := by
  have hPD : 0 < potenciaDisponivel E Zs := by
    unfold potenciaDisponivel
    positivity
  rw [a_potencia_na_carga_pela_reflexao E Zs Zc hs hc]
  constructor
  · intro h
    have h1 : potenciaDisponivel E Zs * reflexao Zs Zc ^ 2 = 0 := by
      linear_combination (-1 : ℝ) * h
    rcases mul_eq_zero.mp h1 with h2 | h2
    · exact absurd h2 hPD.ne'
    · have h3 : reflexao Zs Zc = 0 := pow_eq_zero_iff (two_ne_zero) |>.mp h2
      exact (a_reflexao_e_nula_sse_a_impedancia_e_compartilhada Zs Zc hs hc).mp h3
  · intro h
    have h0 : reflexao Zs Zc = 0 :=
      (a_reflexao_e_nula_sse_a_impedancia_e_compartilhada Zs Zc hs hc).mpr h
    rw [h0]
    ring

/-- [KNOWN, elementar] (R2) Com a impedância compartilhada, a potência na carga É a disponível. -/
theorem com_a_impedancia_compartilhada_a_potencia_e_a_disponivel (E Zs : ℝ) (hs : 0 < Zs) :
    potenciaNaCarga E Zs Zs = potenciaDisponivel E Zs := by
  unfold potenciaNaCarga potenciaDisponivel
  rw [div_eq_div_iff (by positivity) (by positivity)]
  ring

/-- [KNOWN, elementar] (R2) A MÁXIMA TRANSFERÊNCIA DE POTÊNCIA: para toda carga positiva, a potência na
    carga não passa da potência na carga casada (Zc = Zs). -/
theorem maxima_transferencia_de_potencia (E Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    potenciaNaCarga E Zs Zc ≤ potenciaNaCarga E Zs Zs := by
  rw [com_a_impedancia_compartilhada_a_potencia_e_a_disponivel E Zs hs]
  exact a_potencia_na_carga_nao_passa_da_disponivel E Zs Zc hs hc

/-! ## (I4) Com a impedância compartilhada, a fem é o dobro da tensão na carga -/

/-- [KNOWN, elementar] I4. Com a impedância compartilhada, a fem E da fonte é 2·(tensão na carga).
    (R2) A fem do circuito e a força do artigo são homônimas; nada aqui as identifica. -/
theorem com_a_impedancia_compartilhada_a_fem_e_o_dobro_da_tensao_na_carga (E Zs : ℝ) (hs : 0 < Zs) :
    E = 2 * tensaoNaCarga E Zs Zs := by
  have hne : Zs + Zs ≠ 0 := by positivity
  unfold tensaoNaCarga
  field_simp
  ring

/-- [KNOWN, elementar] I4. A fem E é o dobro da tensão na carga se, e só se, a impedância é
compartilhada. -/
theorem a_fem_e_o_dobro_da_tensao_na_carga_sse_a_impedancia_e_compartilhada (E Zs Zc : ℝ)
    (hs : 0 < Zs) (hc : 0 < Zc) (hE : E ≠ 0) :
    E = 2 * tensaoNaCarga E Zs Zc ↔ Zc = Zs := by
  have hne : Zs + Zc ≠ 0 := by positivity
  constructor
  · intro h
    unfold tensaoNaCarga at h
    have h1 : E * (Zs + Zc) = 2 * (E * Zc) := by
      calc E * (Zs + Zc) = (2 * (E * Zc / (Zs + Zc))) * (Zs + Zc) := by rw [← h]
        _ = 2 * (E * Zc) := by field_simp
    have h2 : E * (Zs - Zc) = 0 := by linear_combination h1
    rcases mul_eq_zero.mp h2 with h3 | h3
    · exact absurd h3 hE
    · linarith
  · intro h
    rw [h]
    exact com_a_impedancia_compartilhada_a_fem_e_o_dobro_da_tensao_na_carga E Zs hs

/-! ## (I5) A tensão na carga pela reflexão -/

/-- [KNOWN, elementar] I5. A tensão na carga é a metade da força vezes (1 + r). -/
theorem a_tensao_na_carga_pela_reflexao (E Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    tensaoNaCarga E Zs Zc = E / 2 * (1 + reflexao Zs Zc) := by
  have hne : Zs + Zc ≠ 0 := by positivity
  have hne' : Zc + Zs ≠ 0 := by positivity
  unfold tensaoNaCarga reflexao
  field_simp
  ring

/-! ## (I6) A reflexão fica abaixo de um; a tensão na carga fica abaixo da força -/

/-- [KNOWN, elementar] I6. |r| < 1. -/
theorem a_reflexao_fica_abaixo_de_um (Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    |reflexao Zs Zc| < 1 := by
  unfold reflexao
  have hpos : 0 < Zc + Zs := by positivity
  rw [abs_div, abs_of_pos hpos, div_lt_one hpos, abs_lt]
  constructor <;> linarith

/-- [KNOWN, elementar] I6. Com força positiva, a tensão na carga fica abaixo da força. -/
theorem a_tensao_na_carga_fica_abaixo_da_forca (E Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc)
    (hE : 0 < E) : tensaoNaCarga E Zs Zc < E := by
  have hpos : 0 < Zs + Zc := by positivity
  unfold tensaoNaCarga
  rw [div_lt_iff₀ hpos]
  nlinarith [mul_pos hE hs]

/-! ## (I7) A ligação com o kernel: reflexão = profQ, transmissão = profA = alphaOfChi -/

/-- O quadrado da meia-rapidez: exp(χ/2)·exp(χ/2) = Zc/Zs. -/
theorem exp_meia_rapidez_ao_quadrado (Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    Real.exp (rapidezDeImpedancia Zs Zc / 2) * Real.exp (rapidezDeImpedancia Zs Zc / 2)
      = Zc / Zs := by
  rw [← Real.exp_add, add_halves]
  unfold rapidezDeImpedancia
  exact Real.exp_log (div_pos hc hs)

/-- tanh(χ/2) com χ = log(Zc/Zs) é a reflexão. -/
theorem tanh_da_meia_rapidez (Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    Real.tanh (rapidezDeImpedancia Zs Zc / 2) = reflexao Zs Zc := by
  have hupos := Real.exp_pos (rapidezDeImpedancia Zs Zc / 2)
  have huu := exp_meia_rapidez_ao_quadrado Zs Zc hs hc
  have hneg := Real.exp_neg (rapidezDeImpedancia Zs Zc / 2)
  rw [Real.tanh_eq_sinh_div_cosh, Real.sinh_eq, Real.cosh_eq, hneg]
  generalize Real.exp (rapidezDeImpedancia Zs Zc / 2) = u at hupos huu ⊢
  have hZc : Zc = Zs * (u * u) := by
    rw [huu]
    field_simp
  have hu : u ≠ 0 := hupos.ne'
  have h1 : u * u + 1 ≠ 0 := by positivity
  have h2 : Zs * (u * u) + Zs ≠ 0 := by positivity
  have h3 : u + u⁻¹ ≠ 0 := by positivity
  unfold reflexao
  rw [hZc]
  field_simp

/-- sech(χ/2) com χ = log(Zc/Zs) é a transmissão. -/
theorem sech_da_meia_rapidez (Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    (Real.cosh (rapidezDeImpedancia Zs Zc / 2))⁻¹ = transmissao Zs Zc := by
  have hupos := Real.exp_pos (rapidezDeImpedancia Zs Zc / 2)
  have huu := exp_meia_rapidez_ao_quadrado Zs Zc hs hc
  have hneg := Real.exp_neg (rapidezDeImpedancia Zs Zc / 2)
  rw [Real.cosh_eq, hneg]
  generalize Real.exp (rapidezDeImpedancia Zs Zc / 2) = u at hupos huu ⊢
  have hZc : Zc = Zs * (u * u) := by
    rw [huu]
    field_simp
  have hu : u ≠ 0 := hupos.ne'
  have h1 : u * u + 1 ≠ 0 := by positivity
  have h2 : Zs + Zs * (u * u) ≠ 0 := by positivity
  have h3 : u + u⁻¹ ≠ 0 := by positivity
  have hsqrt : Real.sqrt (Zs * (Zs * (u * u))) = Zs * u := by
    rw [show Zs * (Zs * (u * u)) = (Zs * u) * (Zs * u) by ring]
    exact Real.sqrt_mul_self (by positivity)
  unfold transmissao
  rw [hZc, hsqrt]
  field_simp
  ring

/-- [fiação] ★★ I7. A reflexão é o perfil q do kernel, na rapidez de impedância. -/
theorem a_reflexao_e_o_perfil_q_do_kernel (Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    reflexao Zs Zc = TGLExt.EquationOfTruth.profQ (rapidezDeImpedancia Zs Zc) := by
  unfold TGLExt.EquationOfTruth.profQ
  exact (tanh_da_meia_rapidez Zs Zc hs hc).symm

/-- [fiação] ★★ I7. A transmissão é o perfil a do kernel, na rapidez de impedância. -/
theorem a_transmissao_e_o_perfil_a_do_kernel (Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    transmissao Zs Zc = TGLExt.EquationOfTruth.profA (rapidezDeImpedancia Zs Zc) := by
  unfold TGLExt.EquationOfTruth.profA
  exact (sech_da_meia_rapidez Zs Zc hs hc).symm

/-- [fiação] ★★ I7. A transmissão é o `alphaOfChi` do kernel, na rapidez de impedância. (R2) Esse alfa é
a transmissão sech(χ/2), não a constante de estrutura fina. -/
theorem a_transmissao_e_o_alphaOfChi_do_kernel (Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    transmissao Zs Zc
      = TGLExt.TheCouplingRunsBoundedBelow.alphaOfChi (rapidezDeImpedancia Zs Zc) := by
  unfold TGLExt.TheCouplingRunsBoundedBelow.alphaOfChi
  rw [one_div]
  exact (sech_da_meia_rapidez Zs Zc hs hc).symm

/-! ## (I8, segunda parte) A impedância compartilhada é a profundidade zero -/

/-- [fiação] I8. A impedância é compartilhada se, e só se, a rapidez de impedância é zero. -/
theorem a_impedancia_compartilhada_e_a_rapidez_de_impedancia_zero (Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    Zc = Zs ↔ rapidezDeImpedancia Zs Zc = 0 := by
  constructor
  · intro h
    unfold rapidezDeImpedancia
    rw [h, div_self hs.ne']
    exact Real.log_one
  · intro h
    have h1 := Real.exp_log (div_pos hc hs)
    unfold rapidezDeImpedancia at h
    rw [h, Real.exp_zero] at h1
    field_simp at h1
    linarith

/-! ## (I9) A conservação do fluxo, pela segunda rota: o kernel -/

/-- [fiação] I9. A conservação do fluxo obtida por I7 mais `motor_half_angle_identity`. -/
theorem o_fluxo_se_conserva_pelo_kernel (Zs Zc : ℝ) (hs : 0 < Zs) (hc : 0 < Zc) :
    reflexao Zs Zc ^ 2 + transmissao Zs Zc ^ 2 = 1 := by
  rw [a_reflexao_e_o_perfil_q_do_kernel Zs Zc hs hc, a_transmissao_e_o_perfil_a_do_kernel Zs Zc hs hc]
  unfold TGLExt.EquationOfTruth.profQ TGLExt.EquationOfTruth.profA
  have h := TGLExt.motor_half_angle_identity (rapidezDeImpedancia Zs Zc)
  rw [one_div] at h
  exact h

end TGLExt.PonteDaImpedanciaCandidata

open TGLExt.PonteDaImpedanciaCandidata

#print axioms reflexao
#print axioms transmissao
#print axioms tensaoNaCarga
#print axioms potenciaNaCarga
#print axioms potenciaDisponivel
#print axioms rapidezDeImpedancia
#print axioms com_a_impedancia_compartilhada_a_reflexao_e_nula_e_a_transmissao_e_um
#print axioms a_reflexao_e_nula_sse_a_impedancia_e_compartilhada
#print axioms o_fluxo_se_conserva
#print axioms a_potencia_na_carga_pela_transmissao
#print axioms a_potencia_na_carga_pela_reflexao
#print axioms a_potencia_na_carga_nao_passa_da_disponivel
#print axioms a_potencia_e_maxima_sse_a_impedancia_e_compartilhada
#print axioms com_a_impedancia_compartilhada_a_potencia_e_a_disponivel
#print axioms maxima_transferencia_de_potencia
#print axioms com_a_impedancia_compartilhada_a_fem_e_o_dobro_da_tensao_na_carga
#print axioms a_fem_e_o_dobro_da_tensao_na_carga_sse_a_impedancia_e_compartilhada
#print axioms a_tensao_na_carga_pela_reflexao
#print axioms a_reflexao_fica_abaixo_de_um
#print axioms a_tensao_na_carga_fica_abaixo_da_forca
#print axioms exp_meia_rapidez_ao_quadrado
#print axioms tanh_da_meia_rapidez
#print axioms sech_da_meia_rapidez
#print axioms a_reflexao_e_o_perfil_q_do_kernel
#print axioms a_transmissao_e_o_perfil_a_do_kernel
#print axioms a_transmissao_e_o_alphaOfChi_do_kernel
#print axioms a_impedancia_compartilhada_e_a_rapidez_de_impedancia_zero
#print axioms o_fluxo_se_conserva_pelo_kernel
