import TGLExt.Ergodicity
import TGLExt.SMatrix

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A escada do GLOBAL_LIFT: densidade diádica, a obstrução do traço
  discreto e o canal de medição no referencial-S   [TGLExt — v45]

O esqueleto KERNELIZÁVEL da derivação do operador (13/07/2026) para o
núcleo contínuo do GLOBAL_LIFT — a escada `ℤ → ⋃ₙ 2⁻ⁿℤ → ℝ`:

* **A DENSIDADE DIÁDICA, QUANTITATIVA** (§1 da derivação): o ponto
  diádico mais próximo no estágio `n` erra no máximo `2⁻ⁿ/2`
  (`dyadic_approx`), os estágios são encaixados (`dyadic_stage_mono`) e
  a aproximação CONVERGE (`dyadic_tendsto`). No contínuo [KNOWN,
  Takesaki/Dykema]: a densidade + continuidade forte de λ dão
  `(⋃ₙ Cₙ)'' = M ⋊_σ ℝ` — a parte analítica fica EXTERNA (fecho forte
  de von Neumann não é formalizável hoje na mathlib).

* **A OBSTRUÇÃO DO TRAÇO DISCRETO** (§2 — a joia): no estágio
  `h = 2⁻ⁿ`, o parâmetro dual `s_h = 2π·2ⁿ` fixa o reticulado ponto a
  ponto (`annihilator_fixes_stage`: `e^{−i·s_h·kh} = 1`); mas a lei de
  escala de Takesaki `τ∘θ_s = e^{−s}·τ` então força `τ = 0` em todo
  elemento fixo (`DualScalingData.fixed_tau_zero`, tipada geometry-free
  no estilo TransportData). **A semifinitude do traço é IMPOSSÍVEL em
  cada estágio discreto — ela só pode emergir no fecho contínuo.** A
  frase "o que faltava era exatamente o contínuo" virou teorema.

* **O CANAL DE MEDIÇÃO MODULAR** (§4 — o encaixe das duas pontas):
  `T^S_t = Ad(Sᴴ)∘D_t∘Ad(S)` é SEMIGRUPO genuíno (`sFrame_add` — v41
  matriz-S + v43 dephasing compostos) e CONVERGE para a esperança
  comprimida (`sFrame_tendsto`); o endpoint da medição é a diagonal
  `(cos²θ, sin²θ)` (`dephased_rhoOut_*`) — a matriz-S gera a distinção,
  o dephasing a inscreve como peso.

**HONESTIDADE.** θ e taxas GENÉRICOS; `sin²θ_M = β` e a taxa de Davies
`β·gap` são leituras de RUNTIME — β JAMAIS entra aqui. O que NÃO está
aqui e segue ABERTO: o fecho forte de von Neumann da escada (EXTERNO,
[KNOWN-COMPOSED]); o iso de estágio `Cₙ ≅ M⋊_{σ_h}ℤ` [KNOWN, ação
induzida]; T1-colapso ao KMS (exige centralizador trivial = ergodicidade
do ESTADO — nomeada, condicional); a testemunha III₁ plena
(`canonicalFullTGLWitness`) e o P_F covariante com `0 < τ(P_F) < ∞`
(o resíduo físico preciso). Sem sorry, sem axiom. Negativo honesto é
resultado.
-/

namespace TGLExt

open Matrix NormedSpace Filter

noncomputable section

/-! ## A — a densidade diádica, quantitativa (§1) -/

/-- O ponto diádico mais próximo de `t` no estágio `n`: `round(t·2ⁿ)/2ⁿ`. -/
def dyadicNearest (t : ℝ) (n : ℕ) : ℝ := (round (t * 2 ^ n) : ℝ) / 2 ^ n

/-- [KERNEL] A MALHA DIÁDICA ERRA NO MÁXIMO `2⁻ⁿ/2`: a forma
    QUANTITATIVA da densidade de `⋃ₙ 2⁻ⁿℤ` em ℝ — o degrau `n` da
    escada aproxima qualquer tempo real com erro `≤ h/2`. -/
theorem dyadic_approx (t : ℝ) (n : ℕ) :
    |t - dyadicNearest t n| ≤ ((2 : ℝ) ^ n)⁻¹ / 2 := by
  have h2 : (0 : ℝ) < 2 ^ n := by positivity
  have key : t - dyadicNearest t n
      = (t * 2 ^ n - (round (t * 2 ^ n) : ℝ)) / 2 ^ n := by
    unfold dyadicNearest
    field_simp
  have h := abs_sub_round (t * 2 ^ n)
  have hfin : |t * 2 ^ n - (round (t * 2 ^ n) : ℝ)| / 2 ^ n ≤ (1 / 2) / 2 ^ n := by
    gcongr
  have hEq : (1 / 2 : ℝ) / 2 ^ n = ((2 : ℝ) ^ n)⁻¹ / 2 := by
    simp [div_eq_mul_inv, mul_comm]
  rw [key, abs_div, abs_of_pos h2]
  linarith

/-- [KERNEL] OS ESTÁGIOS SÃO ENCAIXADOS: `k/2ⁿ = 2k/2ⁿ⁺¹` — cada ponto
    do degrau `n` vive no degrau `n+1` (a monotonia `Cₙ ⊂ Cₙ₊₁`). -/
theorem dyadic_stage_mono (k : ℤ) (n : ℕ) :
    (k : ℝ) / 2 ^ n = ((2 * k : ℤ) : ℝ) / 2 ^ (n + 1) := by
  push_cast
  rw [pow_succ]
  field_simp

/-- [KERNEL] A ESCADA CONVERGE: `dyadicNearest t n → t` — todo tempo
    real é limite da sua sombra diádica (a densidade como limite;
    no contínuo, com a continuidade forte de λ [KNOWN], isto é o que
    gera o core ℝ a partir dos degraus ℤ). -/
theorem dyadic_tendsto (t : ℝ) :
    Tendsto (fun n : ℕ => dyadicNearest t n) atTop (nhds t) := by
  have hb : Tendsto (fun n : ℕ => ((2 : ℝ)⁻¹) ^ n * (1 / 2)) atTop (nhds 0) := by
    have h0 : (0 : ℝ) ≤ 2⁻¹ := by norm_num
    have h1 : (2 : ℝ)⁻¹ < 1 := by norm_num
    simpa using (tendsto_pow_atTop_nhds_zero_of_lt_one h0 h1).mul_const (1 / 2 : ℝ)
  have hle : ∀ n : ℕ, |dyadicNearest t n - t| ≤ ((2 : ℝ)⁻¹) ^ n * (1 / 2) := by
    intro n
    have h1 := dyadic_approx t n
    have hEq : ((2 : ℝ)⁻¹) ^ n * (1 / 2) = ((2 : ℝ) ^ n)⁻¹ / 2 := by
      simp [inv_pow, div_eq_mul_inv, mul_comm]
    rw [abs_sub_comm, hEq]
    exact h1
  rw [Metric.tendsto_atTop]
  intro eps heps
  rcases (Metric.tendsto_atTop.mp hb) eps heps with ⟨N, hN⟩
  refine ⟨N, fun n hn => ?_⟩
  have h1 := hN n hn
  have h2 : ((2 : ℝ)⁻¹) ^ n * (1 / 2) < eps := by
    have : |((2 : ℝ)⁻¹) ^ n * (1 / 2) - 0| < eps := by
      simpa [Real.dist_eq] using h1
    have hpos : (0 : ℝ) ≤ ((2 : ℝ)⁻¹) ^ n * (1 / 2) := by positivity
    rwa [sub_zero, abs_of_nonneg hpos] at this
  calc dist (dyadicNearest t n) t = |dyadicNearest t n - t| := Real.dist_eq _ _
    _ ≤ ((2 : ℝ)⁻¹) ^ n * (1 / 2) := hle n
    _ < eps := h2

/-! ## B — o aniquilador do estágio e a obstrução do traço discreto (§2) -/

/-- [KERNEL] O ANIQUILADOR DO ESTÁGIO: em `h = 2⁻ⁿ`, o parâmetro dual
    `s_h = 2π·2ⁿ` fixa TODO o reticulado: `e^{−i·s_h·(k·h)} = 1` para
    todo `k ∈ ℤ` — a ação dual em `s_h` age trivialmente no degrau `n`. -/
theorem annihilator_fixes_stage (n : ℕ) (k : ℤ) :
    Complex.exp (-Complex.I * (2 * (Real.pi : ℂ) * 2 ^ n)
      * ((k : ℂ) * ((2 : ℂ) ^ n)⁻¹)) = 1 := by
  have h2 : ((2 : ℂ) ^ n) ≠ 0 := pow_ne_zero n two_ne_zero
  have harg : -Complex.I * (2 * (Real.pi : ℂ) * 2 ^ n) * ((k : ℂ) * ((2 : ℂ) ^ n)⁻¹)
      = ((-k : ℤ) : ℂ) * (2 * (Real.pi : ℂ) * Complex.I) := by
    push_cast
    field_simp
  rw [harg, Complex.exp_int_mul_two_pi_mul_I]

/-- [KERNEL] ESCALA ≠ 1 MATA O VALOR FIXO (o passo algébrico da
    obstrução): se `x = c·x` com `c ≠ 1`, então `x = 0`. -/
theorem scaling_fixed_eq_zero {c x : ℝ} (hc : c ≠ 1) (h : x = c * x) : x = 0 := by
  have h1 : (1 - c) * x = 0 := by linarith
  rcases mul_eq_zero.mp h1 with h2 | h2
  · exact absurd (by linarith : c = 1) hc
  · exact h2

/-- OS DADOS DA ESCALA DUAL (geometry-free, estilo TransportData): um
    funcional `τ`, uma família `θ_s` e a LEI DE ESCALA de Takesaki
    `τ∘θ_s = e^{−s}·τ`. [Os campos são DADOS; no core real, `τ` é o
    traço canônico e `θ` a ação dual — KNOWN, Takesaki 1973.] -/
structure DualScalingData (M : Type) where
  /-- O funcional (no core: o traço canônico). -/
  tau : M → ℝ
  /-- A família de transformações (no core: a ação dual `θ_s`). -/
  theta : ℝ → M → M
  /-- A LEI DE ESCALA de Takesaki: `τ(θ_s(m)) = e^{−s}·τ(m)`. -/
  scaling : ∀ (s : ℝ) (m : M), tau (theta s m) = Real.exp (-s) * tau m

/-- [KERNEL] ★ A OBSTRUÇÃO DO ESTÁGIO DISCRETO: qualquer elemento fixado
    por `θ_{s₀}` com `s₀ > 0` tem `τ = 0`. Com o aniquilador
    `s₀ = 2π·2ⁿ` (que fixa o degrau `n` inteiro), NENHUM degrau discreto
    porta um elemento de traço finito positivo — **a semifinitude do
    traço só pode emergir no fecho contínuo**. O no-go
    `dualInvariant_PF_no_go` da casa deixa de ser obstáculo e vira
    bússola: o canto `P_F` deve ser fixado pelo fluxo INTERNALIZADO
    `Ad λ(s)` (τ-preservante), jamais pela ação dual. -/
theorem DualScalingData.fixed_tau_zero {M : Type} (D : DualScalingData M)
    {s₀ : ℝ} (hs : 0 < s₀) {m : M} (hfix : D.theta s₀ m = m) : D.tau m = 0 := by
  have h := D.scaling s₀ m
  rw [hfix] at h
  have hlt : Real.exp (-s₀) < 1 := Real.exp_lt_one_iff.mpr (by linarith)
  exact scaling_fixed_eq_zero (ne_of_lt hlt) h

/-- [KERNEL] O corolário diádico: com `s₀ = 2π·2ⁿ`, todo elemento do
    degrau `n` fixado pela ação dual tem `τ = 0`. -/
theorem DualScalingData.dyadic_stage_tau_zero {M : Type} (D : DualScalingData M)
    (n : ℕ) {m : M} (hfix : D.theta (2 * Real.pi * 2 ^ n) m = m) : D.tau m = 0 :=
  D.fixed_tau_zero (by positivity) hfix

/-! ## C — o canal de medição no referencial-S (§4: v41 + v43 encaixados) -/

/-- O SEMIGRUPO NO REFERENCIAL DA MATRIZ-S:
    `T^S_t = Ad(Sᴴ)∘D_t∘Ad(S)` — o encaixe exato das duas pontas já
    provadas no kernel (matriz-S v41 + dephasing v43). -/
def sFrame (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (t : ℝ)
    (x : Matrix (Fin 2) (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  (Smat θ)ᴴ * dephase g t (Smat θ * x * (Smat θ)ᴴ) * Smat θ

/-- `T^S_0 = id`. -/
theorem sFrame_zero (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ)
    (x : Matrix (Fin 2) (Fin 2) ℂ) : sFrame θ g 0 x = x := by
  unfold sFrame
  rw [dephase_zero]
  simp only [← mul_assoc]
  rw [Smat_conjTranspose_mul, one_mul, mul_assoc, Smat_conjTranspose_mul, mul_one]

/-- [KERNEL] LEI DE SEMIGRUPO NO REFERENCIAL-S: `T^S_{s+t} = T^S_s∘T^S_t`
    — a composição v41+v43 é um semigrupo GENUÍNO (a família de medição
    `D_t∘Ad(S)` sozinha não é; o referencial-S conserta). -/
theorem sFrame_add (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (s t : ℝ)
    (x : Matrix (Fin 2) (Fin 2) ℂ) :
    sFrame θ g (s + t) x = sFrame θ g s (sFrame θ g t x) := by
  unfold sFrame
  have hinner : Smat θ * ((Smat θ)ᴴ * dephase g t (Smat θ * x * (Smat θ)ᴴ) * Smat θ)
        * (Smat θ)ᴴ
      = dephase g t (Smat θ * x * (Smat θ)ᴴ) := by
    simp only [← mul_assoc]
    rw [Smat_mul_conjTranspose, one_mul, mul_assoc, Smat_mul_conjTranspose, mul_one]
  rw [hinner, ← dephase_add]

/-- [KERNEL] CONVERGÊNCIA NO REFERENCIAL-S:
    `T^S_t(x) → Ad(Sᴴ)∘E_D∘Ad(S)(x)` — o semigrupo composto converge
    para a esperança condicional comprimida pelo canal: U (matriz-S) +
    T1 (dephasing) = canal modular de medição. -/
theorem sFrame_tendsto (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0)
    (hgpos : ∀ i j, i ≠ j → 0 < g i j) (x : Matrix (Fin 2) (Fin 2) ℂ) :
    Tendsto (fun t => sFrame θ g t x) atTop
      (nhds ((Smat θ)ᴴ * diagExpect (Smat θ * x * (Smat θ)ᴴ) * Smat θ)) := by
  have h := dephase_tendsto_expectation g hg0 hgpos (Smat θ * x * (Smat θ)ᴴ)
  have hcont : Continuous fun y : Matrix (Fin 2) (Fin 2) ℂ => (Smat θ)ᴴ * y * Smat θ :=
    (continuous_const.matrix_mul continuous_id).matrix_mul continuous_const
  exact ((hcont.tendsto _).comp h : _)

/-- [KERNEL] O ENDPOINT DA MEDIÇÃO, peso transmitido:
    `E_D(ρ_out)₀₀ = cos²θ` (runtime: `1−β`). -/
theorem dephased_rhoOut_zero_zero (θ : ℝ) :
    diagExpect (rhoOut θ) 0 0 = (Real.cos θ : ℂ) ^ 2 := by
  rw [show diagExpect (rhoOut θ) 0 0 = rhoOut θ 0 0 by
    simp [diagExpect, Matrix.diag_apply]]
  exact rhoOut_zero_zero θ

/-- [KERNEL] O ENDPOINT DA MEDIÇÃO, peso refletido:
    `E_D(ρ_out)₁₁ = sin²θ` — NO RUNTIME (e só lá): `sin²θ_M = β`. A
    matriz-S gera a distinção; o dephasing a inscreve como peso. -/
theorem dephased_rhoOut_one_one (θ : ℝ) :
    diagExpect (rhoOut θ) 1 1 = (Real.sin θ : ℂ) ^ 2 := by
  rw [show diagExpect (rhoOut θ) 1 1 = rhoOut θ 1 1 by
    simp [diagExpect, Matrix.diag_apply]]
  exact rhoOut_one_one θ

/-- [KERNEL] O CANAL DE MEDIÇÃO MODULAR CONVERGE:
    `D_t(ρ_out(θ)) → E_D(ρ_out(θ))` — o estado puro de saída do canal
    v41 defasa (v43) para a mistura diagonal `(cos²θ, sin²θ)`. -/
theorem measurement_channel_endpoint (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ)
    (hg0 : ∀ i, g i i = 0) (hgpos : ∀ i j, i ≠ j → 0 < g i j) :
    Tendsto (fun t => dephase g t (rhoOut θ)) atTop
      (nhds (diagExpect (rhoOut θ))) :=
  dephase_tendsto_expectation g hg0 hgpos (rhoOut θ)

end

end TGLExt
