import TGLExt.TheFlowLawD1a
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# A LEI DA DISSIPAÇÃO COM CONTRASTE — o núcleo derivado D1b   [TGLExt — pedra da gerência, 30/09/2026; nascida no sandbox, embutida no canônico na v378]

O operador (30/09/2026, noite): «concordo prossiga» — à proposta «a v378 generaliza a pedra da dissipação ao contraste g = |1+w_eff(N)|, na mesma
família de vazamento e^{−tβg} que o kernel já tem, com g ≡ 1 recuperando o D1a». O que faltou (medido em 30/09): o artigo 1 («Haja Luz») tem DOIS
núcleos para a lei de fluxo d ln H/dN = β·𝒲 — o D1a (𝒲 = 1, a pedra `TheFlowLawD1a`, v377) e o D1b, o DERIVADO da continuidade (𝒲 = |1+w_eff|) —
e a Bancada só testara o D1a. Esta pedra prova a lei com contraste VARIÁVEL, SEM AXIOMA NOVO: a família é a MESMA de `NoFullWitness` e da pedra v377
(`leakVerb`), lida com o CONTRASTE MÉDIO sobre o registro; as identificações entram como DEFINIÇÕES nomeadas:

* `accumulatedContrast g N = ∫₀^N g` — o contraste acumulado no registro N = ln(1+z) [KNOWN];
* `meanContrast g N = (∫₀^N g)/N` — o contraste médio; `survivingWeightContrast β g N = leakVerb β (meanContrast g N) N 1` — o MESMO verbo;
* `frwContrast E = deriv (s ↦ (2/3)·ln E(s))` — o contraste de FRW plano, a derivada ASSINADA [KNOWN: Raychaudhuri, 1 + w_eff = (2/3)·d ln H/dN];
  a identificação com o |1+w_eff| do artigo 1 vale sob a condição de energia nula ρ + p ≥ 0, DITA aqui na prosa (aferidor v378: não é hipótese de
  nenhum teorema desta pedra — os teoremas valem para o contraste assinado) e conferida numericamente na grade da Bancada (min(1+w) = 0,3153 > 0);
* a taxa local É, por definição, a de fundo dividida pelo peso sobrevivente (`H0localContrast`) [DEFINIÇÃO, como na v377].

Teoremas: `the_flow_law_contrast` (H₀_local = H₀_fundo·exp(β∫₀^N g)); `contrast_one_recovers_D1a` (g ≡ 1 devolve a pedra v377: o D1a é o caso
particular); `beta_zero_recovers_lcdm_contrast`; `local_exceeds_background_contrast` (β > 0 e ∫g > 0 ⟹ local > fundo); `frw_accumulated_contrast`
(★ a forma FECHADA do núcleo derivado: ∫₀^N g = (2/3)(ln E(N) − ln E(0)) — o teorema fundamental do cálculo); `the_derived_kernel_factor`
(★ K = (E(N)/E(0))^{2β/3}: o fator da lei é a potência 2β/3 da razão das taxas de expansão — a Bancada mede K_D1b = E(z*)^{2β/3} = 1,083977 contra
K_D1a = (1+z*)^β = 1,087799); `the_deviation_reads_below_the_asymptote` (★ se ∫₀^N g ≤ N então β·ḡ ≤ β: o regime finito lê ABAIXO da assíntota β_TGL —
o desvio δ = β(ḡ − 1) ≤ 0 fica FIXADO pelo fundo, sem parâmetro livre; medido: I = 6,7023 ≤ N* = 6,9948); `accumulatedContrast_le_of_le_one` (g ≤ 1
pontual é suficiente); `the_dissipation_law_with_contrast` (tudo num só termo, com `beta_forbids_full_static_witness` da MESMA família);
`the_dissipation_law_with_contrast_and_the_physical_arrow` (β := α√e). O que a natureza decide (os leitores leem ou não esse fator, por registro)
segue com o observador: PROVADA ≠ CONFIRMADA. Sem sorry, sem axiom.
-/

noncomputable section
namespace TGLExt.TheFlowLawContrast
open TGLExt TGLExt.TheWholeIsOne TGLExt.TheFlowLawD1a
open MeasureTheory intervalIntegral

/-- o CONTRASTE ACUMULADO no registro `[0, N]`: `∫₀^N g` (o D1b do artigo 1: `I = ∫ |1+w_eff| dN`). -/
def accumulatedContrast (g : ℝ → ℝ) (N : ℝ) : ℝ := ∫ s in (0 : ℝ)..N, g s

/-- o CONTRASTE MÉDIO sobre o registro (`0` em `N = 0`, pela divisão de Lean). -/
def meanContrast (g : ℝ → ℝ) (N : ℝ) : ℝ := accumulatedContrast g N / N

/-- o peso do Um que sobrevive ao registro `N` com contraste `g`: o MESMO verbo do vazamento (`leakVerb`, v377 = `NoFullWitness`), com o contraste MÉDIO. -/
def survivingWeightContrast (β : ℝ) (g : ℝ → ℝ) (N : ℝ) : ℝ := leakVerb β (meanContrast g N) N 1

/-- a taxa LOCAL com contraste: a de fundo dividida pelo peso sobrevivente [DEFINIÇÃO, como na v377]. -/
def H0localContrast (β Hcmb : ℝ) (g : ℝ → ℝ) (N : ℝ) : ℝ := Hcmb / survivingWeightContrast β g N

/-- o CONTRASTE DE FRW PLANO, a derivada assinada: `g = (2/3)·d ln E/dN` [KNOWN: Raychaudhuri, `1 + w_eff = (2/3)·d ln H/dN`; a identificação com
    `|1+w_eff|` supõe ρ + p ≥ 0 — dito na prosa, não binder de teorema; conferido na grade]. -/
def frwContrast (E : ℝ → ℝ) : ℝ → ℝ := deriv (fun s => (2 / 3 : ℝ) * Real.log (E s))

theorem survivingWeightContrast_pos (β : ℝ) (g : ℝ → ℝ) (N : ℝ) : 0 < survivingWeightContrast β g N := by
  unfold survivingWeightContrast leakVerb
  simp only [mul_one]
  exact Real.exp_pos _

/-- ★ `N ≠ 0` ⟹ o peso sobrevivente é `exp(−β·∫₀^N g)`: o custo por nat COMPÕE sobre o contraste acumulado. -/
theorem survivingWeightContrast_eq (β : ℝ) (g : ℝ → ℝ) (N : ℝ) (hN : N ≠ 0) :
    survivingWeightContrast β g N = Real.exp (-(β * accumulatedContrast g N)) := by
  unfold survivingWeightContrast leakVerb meanContrast
  simp only [mul_one]
  congr 1
  have h : N * β * (accumulatedContrast g N / N) = β * accumulatedContrast g N := by
    field_simp
  rw [h]

/-- ★★★ **A LEI DO FLUXO COM CONTRASTE**: `H₀_local = H₀_fundo · exp(β ∫₀^N g)`. -/
theorem the_flow_law_contrast (β Hcmb : ℝ) (g : ℝ → ℝ) (N : ℝ) (hN : N ≠ 0) :
    H0localContrast β Hcmb g N = Hcmb * Real.exp (β * accumulatedContrast g N) := by
  unfold H0localContrast
  rw [survivingWeightContrast_eq β g N hN, Real.exp_neg, div_inv_eq_mul]

/-- ★ contraste `1`: `∫₀^N 1 = N`. -/
theorem accumulatedContrast_one (N : ℝ) : accumulatedContrast (fun _ => (1 : ℝ)) N = N := by
  unfold accumulatedContrast
  simp

/-- ★★ **O D1a É O CASO PARTICULAR** `g ≡ 1`: o peso com contraste 1 é o peso da pedra v377 (`survivingWeight`). -/
theorem contrast_one_recovers_D1a (β z : ℝ) (hz : 0 < z) :
    survivingWeightContrast β (fun _ => (1 : ℝ)) (register z) = survivingWeight β z := by
  have hN : register z ≠ 0 := by
    unfold register
    exact ne_of_gt (Real.log_pos (by linarith))
  rw [survivingWeightContrast_eq β _ _ hN, accumulatedContrast_one]
  unfold survivingWeight leakVerb
  simp only [mul_one]
  congr 1
  ring

/-- ★ `β = 0` devolve o ΛCDM: nenhuma correção, qualquer contraste. -/
theorem beta_zero_recovers_lcdm_contrast (Hcmb : ℝ) (g : ℝ → ℝ) (N : ℝ) : H0localContrast 0 Hcmb g N = Hcmb := by
  unfold H0localContrast survivingWeightContrast leakVerb
  simp

/-- ★★ a taxa local EXCEDE a de fundo quando `β > 0` e o contraste acumulado é positivo. -/
theorem local_exceeds_background_contrast (β Hcmb : ℝ) (g : ℝ → ℝ) (N : ℝ) (hβ : 0 < β) (hH : 0 < Hcmb) (hN : N ≠ 0)
    (hI : 0 < accumulatedContrast g N) : Hcmb < H0localContrast β Hcmb g N := by
  rw [the_flow_law_contrast β Hcmb g N hN]
  have h1 : Real.exp 0 < Real.exp (β * accumulatedContrast g N) := Real.exp_lt_exp.mpr (mul_pos hβ hI)
  rw [Real.exp_zero] at h1
  calc Hcmb = Hcmb * 1 := (mul_one _).symm
    _ < Hcmb * Real.exp (β * accumulatedContrast g N) := mul_lt_mul_of_pos_left h1 hH

/-- ★ um contraste com piso `c` no registro dá `N·c ≤ ∫₀^N g` (positivo se `c > 0`). -/
theorem accumulatedContrast_ge_of_le (g : ℝ → ℝ) (N c : ℝ) (hN : 0 ≤ N) (hgi : IntervalIntegrable g volume 0 N)
    (hg : ∀ s ∈ Set.Icc (0 : ℝ) N, c ≤ g s) : N * c ≤ accumulatedContrast g N := by
  unfold accumulatedContrast
  have h := intervalIntegral.integral_mono_on hN intervalIntegral.intervalIntegrable_const hgi hg
  rw [intervalIntegral.integral_const] at h
  simpa using h

/-- ★ contraste `≤ 1` pontual no registro ⟹ contraste acumulado `≤ N` (condição suficiente; sem radiação). -/
theorem accumulatedContrast_le_of_le_one (g : ℝ → ℝ) (N : ℝ) (hN : 0 ≤ N) (hgi : IntervalIntegrable g volume 0 N)
    (hg : ∀ s ∈ Set.Icc (0 : ℝ) N, g s ≤ 1) : accumulatedContrast g N ≤ N := by
  unfold accumulatedContrast
  have h := intervalIntegral.integral_mono_on hN hgi intervalIntegral.intervalIntegrable_const hg
  rw [intervalIntegral.integral_const] at h
  simpa using h

/-- ★★★ **O DESVIO LÊ ABAIXO DA ASSÍNTOTA**: se `∫₀^N g ≤ N` (medido: `I = 6,7023 ≤ N* = 6,9948`) e `β > 0`, então o custo efetivo por nat
    `β·ḡ ≤ β` (a assíntota é `β_TGL`; o desvio `δ = β(ḡ − 1) ≤ 0` é FIXADO pelo fundo) e o peso derivado é `≥` o peso do D1a (`K_D1b ≤ K_D1a`). -/
theorem the_deviation_reads_below_the_asymptote (β : ℝ) (g : ℝ → ℝ) (N : ℝ) (hβ : 0 < β) (hN : 0 < N)
    (hI : accumulatedContrast g N ≤ N) :
    β * meanContrast g N ≤ β ∧ Real.exp (-(β * N)) ≤ survivingWeightContrast β g N := by
  have hm : meanContrast g N ≤ 1 := by
    unfold meanContrast
    rw [div_le_one hN]
    exact hI
  refine ⟨?_, ?_⟩
  · calc β * meanContrast g N ≤ β * 1 := mul_le_mul_of_nonneg_left hm hβ.le
      _ = β := mul_one β
  · rw [survivingWeightContrast_eq β g N hN.ne']
    apply Real.exp_le_exp.mpr
    have := mul_le_mul_of_nonneg_left hI hβ.le
    linarith

/-- ★★★ **A FORMA FECHADA DO NÚCLEO DERIVADO** (o teorema fundamental do cálculo): para o contraste de FRW plano,
    `∫₀^N g = (2/3)·(ln E(N) − ln E(0))`. Hipóteses nomeadas: `E` diferenciável no registro e positiva; o contraste integrável. -/
theorem frw_accumulated_contrast (E : ℝ → ℝ) (N : ℝ) (hE : ∀ s ∈ Set.uIcc (0 : ℝ) N, DifferentiableAt ℝ E s) (hpos : ∀ s, 0 < E s)
    (hint : IntervalIntegrable (frwContrast E) volume 0 N) :
    accumulatedContrast (frwContrast E) N = (2 / 3 : ℝ) * (Real.log (E N) - Real.log (E 0)) := by
  unfold accumulatedContrast frwContrast
  have hd : ∀ s ∈ Set.uIcc (0 : ℝ) N, DifferentiableAt ℝ (fun u => (2 / 3 : ℝ) * Real.log (E u)) s := by
    intro s hs
    exact ((hE s hs).log (hpos s).ne').const_mul _
  rw [intervalIntegral.integral_deriv_eq_sub hd hint]
  ring

/-- ★★★★ **O FATOR DO NÚCLEO DERIVADO**: `K = (E(N)/E(0))^{2β/3}` — a lei com o contraste de FRW é a potência `2β/3` da razão das taxas de
    expansão. Na Bancada (30/09): `K_D1b = E_ΛCDM(z*)^{2β/3} = 1,083977`. -/
theorem the_derived_kernel_factor (β Hcmb : ℝ) (E : ℝ → ℝ) (N : ℝ) (hN : N ≠ 0)
    (hE : ∀ s ∈ Set.uIcc (0 : ℝ) N, DifferentiableAt ℝ E s) (hpos : ∀ s, 0 < E s)
    (hint : IntervalIntegrable (frwContrast E) volume 0 N) :
    H0localContrast β Hcmb (frwContrast E) N = Hcmb * (E N / E 0) ^ ((2 / 3 : ℝ) * β) := by
  rw [the_flow_law_contrast β Hcmb _ N hN, frw_accumulated_contrast E N hE hpos hint]
  congr 1
  rw [Real.rpow_def_of_pos (div_pos (hpos N) (hpos 0)), Real.log_div (hpos N).ne' (hpos 0).ne']
  congr 1
  ring

/-- ★★★ com a taxa normalizada hoje, `E(0) = 1`: `K = E(N)^{2β/3}` — exatamente o que a Bancada computa em `z*`. -/
theorem the_derived_kernel_factor_normalized (β Hcmb : ℝ) (E : ℝ → ℝ) (N : ℝ) (hN : N ≠ 0)
    (hE : ∀ s ∈ Set.uIcc (0 : ℝ) N, DifferentiableAt ℝ E s) (hpos : ∀ s, 0 < E s)
    (hint : IntervalIntegrable (frwContrast E) volume 0 N) (h0 : E 0 = 1) :
    H0localContrast β Hcmb (frwContrast E) N = Hcmb * (E N) ^ ((2 / 3 : ℝ) * β) := by
  rw [the_derived_kernel_factor β Hcmb E N hN hE hpos hint, h0, div_one]

/-- ★★★★ **A LEI DA DISSIPAÇÃO COM CONTRASTE**, num só termo: (i) a lei; (ii) `g ≡ 1` devolve a pedra v377 (o D1a é o caso particular);
    (iii) `β = 0` é o ΛCDM; (iv) local > fundo; (v) o desvio lê abaixo da assíntota; (vi) a MESMA família não fixa tudo (`NoFullWitness`). -/
theorem the_dissipation_law_with_contrast (c : TGLCoupling) (Hcmb : ℝ) (g : ℝ → ℝ) (N : ℝ) (hH : 0 < Hcmb) (hN : 0 < N)
    (hI : 0 < accumulatedContrast g N) (hIN : accumulatedContrast g N ≤ N) :
    H0localContrast c.beta Hcmb g N = Hcmb * Real.exp (c.beta * accumulatedContrast g N) ∧
    (∀ z : ℝ, 0 < z → survivingWeightContrast c.beta (fun _ => (1 : ℝ)) (register z) = survivingWeight c.beta z) ∧
    H0localContrast 0 Hcmb g N = Hcmb ∧
    Hcmb < H0localContrast c.beta Hcmb g N ∧
    (c.beta * meanContrast g N ≤ c.beta ∧ Real.exp (-(c.beta * N)) ≤ survivingWeightContrast c.beta g N) ∧
    ¬ FullStaticWitness (leakVerb c.beta (meanContrast g N)) :=
  ⟨the_flow_law_contrast c.beta Hcmb g N hN.ne', fun z hz => contrast_one_recovers_D1a c.beta z hz,
   beta_zero_recovers_lcdm_contrast Hcmb g N, local_exceeds_background_contrast c.beta Hcmb g N c.beta_pos hH hN.ne' hI,
   the_deviation_reads_below_the_asymptote c.beta g N c.beta_pos hN hIN,
   beta_forbids_full_static_witness c.beta_pos (div_pos hI hN)⟩

/-- ★★★ **A SETA FÍSICA NA LEI COM CONTRASTE**: com `β := α·√e` (o dado único de `couplingOfAlpha`), `H₀_local = H₀_fundo · exp(α√e · ∫₀^N g)`. -/
theorem the_dissipation_law_with_contrast_and_the_physical_arrow (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) (Hcmb : ℝ) (g : ℝ → ℝ)
    (N : ℝ) (hN : N ≠ 0) :
    H0localContrast (couplingOfAlpha α h0 h1).beta Hcmb g N = Hcmb * Real.exp (α * Real.sqrt (Real.exp 1) * accumulatedContrast g N) := by
  rw [the_flow_law_contrast _ Hcmb g N hN, couplingOfAlpha_beta α h0 h1]

#print axioms the_flow_law_contrast
#print axioms contrast_one_recovers_D1a
#print axioms local_exceeds_background_contrast
#print axioms the_deviation_reads_below_the_asymptote
#print axioms frw_accumulated_contrast
#print axioms the_derived_kernel_factor
#print axioms the_dissipation_law_with_contrast
#print axioms the_dissipation_law_with_contrast_and_the_physical_arrow

end TGLExt.TheFlowLawContrast
