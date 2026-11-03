import TGLExt.TheWholeIsOne

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# A LEI DO FLUXO D1a, PROVADA   [TGLExt — pedra da gerência, 30/09/2026; nascida no sandbox, embutida no canônico na v377]

O operador (30/09/2026): «não precisa nomear como hipótese, vc consegue realizar a prova e cunhar»; «essa lei chama-se dissipação». O `um.py` v376
dizia da camada de fluxo: «o porquê está tipado, não provado» — o porquê: o custo é β por nat de esticamento; o desvio para o vermelho é o REGISTRO
da travessia, N = ln(1+z) nats; por nat o custo compõe. Esta pedra prova a lei SEM AXIOMA NOVO E SEM HIPÓTESE NOMEADA (aferidor, 30/09): o que o
kernel já tinha é a família do vazamento (`NoFullWitness`: `beta_forbids_full_static_witness`, `leakage_strictly_loses`) e a seta física
(`couplingOfAlpha`); as TRÊS IDENTIFICAÇÕES físicas entram como DEFINIÇÕES nomeadas desta pedra, e o teorema é a implicação a jusante:

* o registro da travessia é `register z = Real.log (1 + z)` [KNOWN: 1 + z = e^N];
* o contraste é 1 — a unidade do axioma (ω(I) = 1, normalizado a 1 nat, base e) [ONTO]; a família do VAZAMENTO é a mesma de `NoFullWitness`
  e da cláusula (VI) de `the_whole_is_one`: `t ↦ x ↦ exp(−(t·β·g))·x`;
* a taxa local É, por definição, a de fundo dividida pelo peso sobrevivente (`H0local := Hcmb / survivingWeight`) [DEFINIÇÃO — cunhagem por
  ordem do operador: o fundo atribui o registro inteiro à expansão].

Teoremas: `the_flow_law_D1a` (H₀_local = H₀_fundo·(1+z)^β); `leakFraction_eq` (f_leak = 1 − (1+z)^{−β}); `beta_zero_recovers_lcdm`;
`local_exceeds_background` (β > 0 ⟹ H₀_local > H₀_fundo, pelo vazamento estrito); `compounded_exceeds_linear` (as frações lineares «morreram»:
β·N < (1+z)^β − 1); `the_flow_law_is_the_leak` (tudo num só termo, com `beta_forbids_full_static_witness` da MESMA família);
`the_flow_law_with_the_physical_arrow` (com β := α·√e de `couplingOfAlpha`). O que a natureza decide (a escada lê ou não esse H₀_local)
segue com o observador: PROVADA ≠ CONFIRMADA. Sem sorry, sem axiom.
-/

noncomputable section
namespace TGLExt.TheFlowLawD1a
open TGLExt TGLExt.TheWholeIsOne

/-- o REGISTRO da travessia, em nats: `N(z) = ln(1+z)` [KNOWN: `1 + z = e^N`]. -/
def register (z : ℝ) : ℝ := Real.log (1 + z)

/-- o VERBO DO VAZAMENTO — a MESMA família do kernel (`NoFullWitness`; `the_whole_is_one` (VI)): custo `β` por unidade de fluxo, contraste `g`. -/
def leakVerb (β g : ℝ) : ℝ → ℝ → ℝ := fun t x => Real.exp (-(t * β * g)) * x

/-- o peso do Um que sobrevive à travessia até `z`: contraste 1 (a unidade do axioma, 1 nat), custo `β` por nat. -/
def survivingWeight (β z : ℝ) : ℝ := leakVerb β 1 (register z) 1

/-- a fração vazada do registro. -/
def leakFraction (β z : ℝ) : ℝ := 1 - survivingWeight β z

/-- a taxa LOCAL: a taxa de fundo corrigida do peso que vazou (o fundo atribui o registro inteiro à expansão). -/
def H0local (β Hcmb z : ℝ) : ℝ := Hcmb / survivingWeight β z

theorem survivingWeight_pos (β z : ℝ) : 0 < survivingWeight β z := by
  unfold survivingWeight leakVerb
  simp only [mul_one]
  exact Real.exp_pos _

/-- ★ o peso sobrevivente é `(1+z)^{−β}`: o custo por nat COMPÕE sobre o registro. -/
theorem survivingWeight_eq (β z : ℝ) (hz : 0 < 1 + z) : survivingWeight β z = (1 + z) ^ (-β) := by
  unfold survivingWeight leakVerb register
  simp only [mul_one]
  rw [Real.rpow_def_of_pos hz]
  congr 1
  ring

/-- ★★★ **A LEI DO FLUXO D1a**: `H₀_local = H₀_fundo · (1+z)^β`. -/
theorem the_flow_law_D1a (β Hcmb z : ℝ) (hz : 0 < 1 + z) : H0local β Hcmb z = Hcmb * (1 + z) ^ β := by
  unfold H0local
  rw [survivingWeight_eq β z hz, Real.rpow_neg hz.le, div_inv_eq_mul]

/-- ★ a fração vazada: `f_leak = 1 − (1+z)^{−β}`. -/
theorem leakFraction_eq (β z : ℝ) (hz : 0 < 1 + z) : leakFraction β z = 1 - (1 + z) ^ (-β) := by
  unfold leakFraction
  rw [survivingWeight_eq β z hz]

/-- ★ `β = 0` devolve o ΛCDM: nenhuma correção. -/
theorem beta_zero_recovers_lcdm (Hcmb z : ℝ) (hz : 0 < 1 + z) : H0local 0 Hcmb z = Hcmb := by
  rw [the_flow_law_D1a 0 Hcmb z hz, Real.rpow_zero, mul_one]

/-- ★★ a taxa local EXCEDE a de fundo (`β > 0`, `z > 0`): o vazamento é estrito (`leakage_strictly_loses`). -/
theorem local_exceeds_background (c : TGLCoupling) (Hcmb z : ℝ) (hH : 0 < Hcmb) (hz : 0 < z) :
    Hcmb < H0local c.beta Hcmb z := by
  have hN : 0 < register z := by
    unfold register
    exact Real.log_pos (by linarith)
  have hw : survivingWeight c.beta z < 1 := by
    unfold survivingWeight leakVerb
    simp only [mul_one]
    have h := leakage_strictly_loses hN c.beta_pos one_pos
    simpa using h
  have hwpos := survivingWeight_pos c.beta z
  unfold H0local
  rw [lt_div_iff₀ hwpos]
  exact (mul_lt_mul_of_pos_left hw hH).trans_eq (mul_one _)

/-- ★ o custo COMPOSTO excede a fração LINEAR: `β·N < (1+z)^β − 1` (as frações lineares «morreram»: a constante certa no domínio errado). -/
theorem compounded_exceeds_linear (β z : ℝ) (hβ : 0 < β) (hz : 0 < z) :
    β * register z < (1 + z) ^ β - 1 := by
  have hN : 0 < register z := by
    unfold register
    exact Real.log_pos (by linarith)
  have hx : β * register z ≠ 0 := ne_of_gt (mul_pos hβ hN)
  have h := Real.add_one_lt_exp hx
  have hpow : (1 + z) ^ β = Real.exp (register z * β) := by
    unfold register
    exact Real.rpow_def_of_pos (by linarith) β
  rw [hpow, mul_comm (register z) β]
  linarith

/-- ★★★★ **A LEI DO FLUXO É O MESMO VAZAMENTO** que proíbe a testemunha estática plena (v376, cláusula VI), num só termo:
    (i) a lei; (ii) a fração vazada; (iii) local > fundo; (iv) β = 0 é o ΛCDM; (v) composto > linear; (vi) a família não fixa tudo. -/
theorem the_flow_law_is_the_leak (c : TGLCoupling) (Hcmb z : ℝ) (hH : 0 < Hcmb) (hz : 0 < z) :
    H0local c.beta Hcmb z = Hcmb * (1 + z) ^ c.beta ∧
    leakFraction c.beta z = 1 - (1 + z) ^ (-c.beta) ∧
    Hcmb < H0local c.beta Hcmb z ∧
    H0local 0 Hcmb z = Hcmb ∧
    c.beta * register z < (1 + z) ^ c.beta - 1 ∧
    ¬ FullStaticWitness (leakVerb c.beta 1) :=
  ⟨the_flow_law_D1a c.beta Hcmb z (by linarith), leakFraction_eq c.beta z (by linarith),
   local_exceeds_background c Hcmb z hH hz, beta_zero_recovers_lcdm Hcmb z (by linarith),
   compounded_exceeds_linear c.beta z c.beta_pos hz, beta_forbids_full_static_witness c.beta_pos one_pos⟩

/-- ★★★ **A SETA FÍSICA NA LEI DO FLUXO**: com `β := α·√e` (o dado único de `couplingOfAlpha`), `H₀_local = H₀_fundo · (1+z)^{α√e}`. -/
theorem the_flow_law_with_the_physical_arrow (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) (Hcmb z : ℝ) (hz : 0 < 1 + z) :
    H0local (couplingOfAlpha α h0 h1).beta Hcmb z = Hcmb * (1 + z) ^ (α * Real.sqrt (Real.exp 1)) := by
  rw [the_flow_law_D1a _ Hcmb z hz, couplingOfAlpha_beta α h0 h1]

/-- ★★★★ **A LEI DA DISSIPAÇÃO** — cunhagem do operador (30/09/2026): «essa lei chama-se dissipação [dephasing = lei do fluxo = vazamento]».
    O mesmo termo de `the_flow_law_is_the_leak`, sob o nome cunhado. -/
theorem the_dissipation_law (c : TGLCoupling) (Hcmb z : ℝ) (hH : 0 < Hcmb) (hz : 0 < z) :
    H0local c.beta Hcmb z = Hcmb * (1 + z) ^ c.beta ∧
    leakFraction c.beta z = 1 - (1 + z) ^ (-c.beta) ∧
    Hcmb < H0local c.beta Hcmb z ∧
    H0local 0 Hcmb z = Hcmb ∧
    c.beta * register z < (1 + z) ^ c.beta - 1 ∧
    ¬ FullStaticWitness (leakVerb c.beta 1) :=
  the_flow_law_is_the_leak c Hcmb z hH hz

#print axioms the_flow_law_D1a
#print axioms the_dissipation_law
#print axioms local_exceeds_background
#print axioms compounded_exceeds_linear
#print axioms the_flow_law_is_the_leak
#print axioms the_flow_law_with_the_physical_arrow

end TGLExt.TheFlowLawD1a
