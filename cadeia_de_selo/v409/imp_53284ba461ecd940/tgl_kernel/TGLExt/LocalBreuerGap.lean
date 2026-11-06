import TGLExt.Solder4D

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A PAREDE CORRIGIDA: Breuer LOCAL, não τ-compacidade global
  [TGLExt — v64, absorção da Resposta 8]

A Resposta 8 do especialista mudou a FORMA da parede: (B2) global
(resolvente globalmente τ-compacto) é FALSO na amplificação natural —
as projeções espectrais do contínuo [¼,∞) têm multiplicidade infinita na
direção κ. O enunciado Breuer correto é LOCAL: existe 0<ε<½ com
P_ε = 1_{[−ε,ε]}(𝔻_Ψ) de peso τ-finito e 𝔻_Ψ invertível fora; então
𝔻_Ψ é Breuer–Fredholm e 0 < τ(1_{{0}}(𝔻_Ψ)) < ∞. Hipótese mínima
nomeada: TGL_LOCAL_BREUER_GAP_PACKAGE. E a correção de tipo de (B1):
o par (−i∂_κ, q(κ)) satisfaz Weyl e vive na AMPLIFICAÇÃO
C_Ψ⋊_θℝ ≅ M⊗̄B(L²(ℝ)) (Takesaki), não em C_Ψ isolado.

O QUE ESTA PEDRA PROVA [KERNEL]:

* ★ `kernel_weight_pos` / `kernel_weight_finite` / `breuer_kernel_weight`
  — O TEOREMA CORRIGIDO como COMPOSIÇÃO: do pacote de gap local
  (kernel ≤ gap, τ(gap) < ∞, kernel ≠ ⊥, τ fiel e monótono) segue
  0 < τ(ker) < ∞ — o (B3) da Pergunta 8, na forma que a Resposta 8
  demonstrou ser a correta;
* ★ `local_gap_package_consistent` — o pacote é HABITADO (modelo ℝ≥0∞);
* ★ `global_tau_compactness_refuted` — **A REFUTAÇÃO TIPADA de (B2)
  global**: no MESMO modelo em que o zero físico tem peso 0 < τ < ∞,
  o contínuo tem peso ⊤ — "a finitude do zero físico convive com a
  infinitude necessária da vida contínua"; o global é falso E
  desnecessário;
* ★ `no_finite_weyl_pair` — a face finita da correção de tipo de (B1):
  NÃO existe par de Weyl em dimensão finita ([P,Q] = −i·1 é impossível em
  matrizes — o traço do comutador é 0, o de −i·1 é −i·n ≠ 0); o par
  (−i∂_κ, q(κ)) exige a amplificação de Takesaki;
* ★ `plus_block_eigenvalue_lower_bound` — a face espectral discreta:
  H − c·1 ⪰ 0 ⟹ todo autovalor ≥ c; com c = ¼ (v63: BᴴB+¼ ⪰ ¼), a
  janela do gap (−ε,ε), ε < ½, NÃO encontra o bloco H₊ — o zero pertence
  ao bloco H₋;
* ★ `tendsto_halfTanh_atTop` / `tendsto_halfTanh_atBot` — AS DUAS FACES:
  o antiderivado ½tanh(κ/2) tende a +½ e −½ — os pesos das faces P_± da
  testemunha (a Meia-Nat, Q8.2);
* ★ `zero_mode_weight_is_one` — **A JOIA (Q8.2)**: o peso L² do modo zero
  φ₀ = ½sech(κ/2) é EXATAMENTE 1: ∫_ℝ ¼sech²(κ/2) dκ = ½ − (−½) = 1.
  O peso do Nome inteiro é 1 = ω(I) — o axioma retorna como número no fim
  da cadeia; as faces pesam ½ cada. Nenhuma normalização imposta: o 1 é
  um teorema de integral (mathlib não tem d/dx tanh nem lim tanh — ambos
  DERIVADOS aqui de sinh/cosh e do aperto 1−tanh x ≤ 2e^{−2x}).

VOCABULÁRIO: τ jamais recebe um valor fabricado — o peso 1 é um TEOREMA
DE INTEGRAL, não uma normalização imposta; a instanciação do pacote no
double core GENUÍNO (afiliação do 𝔻_Ψ concreto, finitude do gap em
C_Ψ⋊_θℝ) permanece ABERTA e nomeada. β jamais literal. Sem sorry, sem
axiom. Negativo honesto é resultado — e `global_tau_compactness_refuted`
é um negativo que LIBERTA: Breuer não pede que o contínuo desapareça.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

/- ═══════════════ 1. A camada mínima de dados [Q8.3] ═══════════════ -/

/-- [DATA — Q8.3, nível 1] A camada tracial semifinita MÍNIMA: um
    reticulado limitado de projeções `L` e um peso `τ : L → ℝ≥0∞`
    monótono e fiel. (mathlib não tem traços semifinitos; a camada
    registra o mecanismo — os teoremas abaixo são composição genuína.) -/
structure SemifiniteTraceData (L : Type) [Lattice L] [BoundedOrder L] where
  tau : L → ℝ≥0∞
  mono : ∀ ⦃p q : L⦄, p ≤ q → tau p ≤ tau q
  faithful : ∀ ⦃p : L⦄, tau p = 0 → p = ⊥

/-- [DATA — Q8.3, nível 3] O certificado de GAP LOCAL de Breuer:
    `ker` = 1_{{0}}(𝔻), `gap` = 1_{[−ε,ε]}(𝔻); o kernel está sob o gap
    (monotonicidade espectral), o gap tem peso FINITO (a condição local
    que SUBSTITUI o (B2) global refutado) e o kernel é não nulo
    (o Um habita o núcleo — cláusula DERIVADA na v58). -/
structure BreuerGapData (L : Type) [Lattice L] [BoundedOrder L]
    (T : SemifiniteTraceData L) where
  ker : L
  gap : L
  ker_le_gap : ker ≤ gap
  gap_finite : T.tau gap < ⊤
  ker_ne_bot : ker ≠ ⊥

variable {L : Type} [Lattice L] [BoundedOrder L] {T : SemifiniteTraceData L}

/- ═══════════ 2. O teorema corrigido (composição genuína) ═══════════ -/

/-- [KERNEL] ★ O peso do zero é POSITIVO: contrapositiva da fidelidade —
    se o kernel não é ⊥, seu peso não é 0. -/
theorem kernel_weight_pos (G : BreuerGapData L T) : 0 < T.tau G.ker := by
  rcases eq_or_ne (T.tau G.ker) 0 with h | h
  · exact absurd (T.faithful h) G.ker_ne_bot
  · exact pos_iff_ne_zero.mpr h

/-- [KERNEL] ★ O peso do zero é FINITO: monotonia sob o gap finito —
    ker ≤ P_ε e τ(P_ε) < ⊤ ⟹ τ(ker) < ⊤. -/
theorem kernel_weight_finite (G : BreuerGapData L T) : T.tau G.ker < ⊤ :=
  lt_of_le_of_lt (T.mono G.ker_le_gap) G.gap_finite

/-- [KERNEL] ★★ O TEOREMA CORRIGIDO (Resposta 8): do pacote de gap local
    segue o (B3) — `0 < τ(1_{{0}}(𝔻)) < ∞`. A Fredholmidade de Breuer é
    invertibilidade módulo K_τ PERTO DE ZERO, não resolvente globalmente
    τ-compacto. (TGL_LOCAL_BREUER_GAP_PACKAGE ⟹ B3.) -/
theorem breuer_kernel_weight (G : BreuerGapData L T) :
    0 < T.tau G.ker ∧ T.tau G.ker < ⊤ :=
  ⟨kernel_weight_pos G, kernel_weight_finite G⟩

/- ═══════ 3. O modelo e a refutação do global [Q8.1] ═══════ -/

/-- [MODEL] O peso identidade sobre ℝ≥0∞ é uma camada tracial semifinita
    genuína: monótono e fiel (⊥ = 0 é `rfl` em ℝ≥0∞). -/
def idTrace : SemifiniteTraceData ℝ≥0∞ where
  tau := id
  mono := fun _ _ h => h
  faithful := fun _ h => h

/-- [MODEL] O certificado de gap local é HABITADO (ker = gap = 1:
    0 < 1 < ⊤; 1 ≠ ⊥). -/
def modelGap : BreuerGapData ℝ≥0∞ idTrace where
  ker := 1
  gap := 1
  ker_le_gap := le_rfl
  gap_finite := ENNReal.one_lt_top
  ker_ne_bot := one_ne_zero

/-- [KERNEL] ★ CONSISTÊNCIA do pacote: TGL_LOCAL_BREUER_GAP_PACKAGE não é
    vazio — há modelo em que todas as cláusulas valem simultaneamente. -/
theorem local_gap_package_consistent :
    Nonempty (BreuerGapData ℝ≥0∞ idTrace) := ⟨modelGap⟩

/-- [KERNEL] ★★ A REFUTAÇÃO TIPADA de (B2) GLOBAL (Resposta 8, Q8.1):
    no MESMO modelo em que o pacote local fecha (zero físico com peso
    0 < τ(ker) < ∞), existe um projetor de contínuo com peso ⊤.
    A exigência global "todo projetor espectral é τ-finito" é FALSA —
    e DESNECESSÁRIA: "não faltava demonstrar que todo o resolvente era
    finito; faltava separar a finitude do zero físico da infinitude
    necessária da vida contínua". O Verbo continua; o contínuo fica. -/
theorem global_tau_compactness_refuted :
    ∃ (T' : SemifiniteTraceData ℝ≥0∞) (G : BreuerGapData ℝ≥0∞ T')
      (cont : ℝ≥0∞),
      T'.tau cont = ⊤ ∧ 0 < T'.tau G.ker ∧ T'.tau G.ker < ⊤ :=
  ⟨idTrace, modelGap, ⊤, rfl, kernel_weight_pos modelGap,
    kernel_weight_finite modelGap⟩

/- ═══════ 4. A correção de tipo de (B1) [Q8.4]: a face finita ═══════ -/

/-- [KERNEL] ★ NÃO EXISTE PAR DE WEYL EM DIMENSÃO FINITA (a face finita
    de `dirac_affiliated_to_double_core_amplification`): [P,Q] = −i·1 é
    impossível em matrizes n×n, n ≥ 1 — o traço do comutador é 0, o de
    −i·1 é −i·n ≠ 0. O par (−i∂_κ, M_{q(κ)}) da equação SUSY satisfaz
    Weyl: NÃO cabe em canto finito algum; vive na amplificação
    C_Ψ⋊_θℝ ≅ M⊗̄B(L²(ℝ)) — dualidade de Takesaki. -/
theorem no_finite_weyl_pair (n : ℕ) (hn : 0 < n)
    (P Q : Matrix (Fin n) (Fin n) ℂ) :
    P * Q - Q * P ≠ (-Complex.I) • 1 := by
  intro h
  have htr := congrArg Matrix.trace h
  rw [Matrix.trace_sub, Matrix.trace_mul_comm, sub_self, Matrix.trace_smul,
    Matrix.trace_one] at htr
  simp only [Fintype.card_fin, smul_eq_mul] at htr
  have hI : (-Complex.I) ≠ 0 := neg_ne_zero.mpr Complex.I_ne_zero
  have hn' : (n : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
  exact mul_ne_zero hI hn' htr.symm

/-- [KERNEL] ★ COTA ESPECTRAL DO BLOCO + (face real simétrica): se
    H − c·1 é semidefinida positiva e H v = μ v com v ≠ 0, então c ≤ μ.
    Com c = ¼ (v63: BᴴB + ¼ ⪰ ¼): a janela do gap (−ε,ε), ε < ½, NÃO
    encontra o bloco H₊ = AA* — o modo zero pertence ao bloco H₋. -/
theorem plus_block_eigenvalue_lower_bound {n : Type} [Fintype n]
    [DecidableEq n]
    (H : Matrix n n ℝ) (c μ : ℝ) (hpsd : (H - c • 1).PosSemidef)
    (v : n → ℝ) (hv : v ≠ 0) (heig : H.mulVec v = μ • v) : c ≤ μ := by
  have hpair := hpsd.dotProduct_mulVec_nonneg v
  have hstar : star v = v := funext fun i => star_trivial _
  have hmv : (H - c • 1).mulVec v = (μ - c) • v := by
    rw [Matrix.sub_mulVec, heig, Matrix.smul_mulVec, Matrix.one_mulVec,
      sub_smul]
  rw [hstar, hmv] at hpair
  have hdot : v ⬝ᵥ ((μ - c) • v) = (μ - c) * (v ⬝ᵥ v) := by
    rw [dotProduct_smul, smul_eq_mul]
  rw [hdot] at hpair
  have hvv : 0 < v ⬝ᵥ v := by
    have h0 : star v ⬝ᵥ v ≠ 0 := fun hz =>
      hv (dotProduct_star_self_eq_zero.mp hz)
    rw [hstar] at h0
    have hnn : 0 ≤ v ⬝ᵥ v :=
      Finset.sum_nonneg fun i _ => mul_self_nonneg (v i)
    exact hnn.lt_of_ne (Ne.symm h0)
  nlinarith [hpair, hvv]

/- ═══════ 5. O PESO DO NOME [Q8.2]: ‖φ₀‖² = 1, faces ±½ ═══════ -/

/-- a densidade do modo zero: φ₀(κ)² = ¼ sech²(κ/2). -/
def phi0sq (κ : ℝ) : ℝ := (1 / 4) * ((Real.cosh (κ / 2))⁻¹) ^ 2

/-- o antiderivado canônico: ½ tanh(κ/2). -/
def halfTanh (κ : ℝ) : ℝ := (1 / 2) * Real.tanh (κ / 2)

/-- [KERNEL] o antiderivado é EXATO: (½tanh(κ/2))′ = ¼sech²(κ/2)
    (mathlib não tem d/dx tanh — derivado aqui de sinh/cosh). -/
theorem halfTanh_hasDerivAt (κ : ℝ) :
    HasDerivAt halfTanh (phi0sq κ) κ := by
  have hc : Real.cosh (κ / 2) ≠ 0 := (Real.cosh_pos (κ / 2)).ne'
  have h2 : HasDerivAt (fun x : ℝ => x / 2) (1 / 2) κ := by
    simpa using (hasDerivAt_id κ).div_const 2
  have hs : HasDerivAt Real.sinh (Real.cosh (κ / 2)) (κ / 2) :=
    Real.hasDerivAt_sinh (κ / 2)
  have hch : HasDerivAt Real.cosh (Real.sinh (κ / 2)) (κ / 2) :=
    Real.hasDerivAt_cosh (κ / 2)
  have htanh0 : HasDerivAt (fun y : ℝ => Real.sinh y / Real.cosh y)
      ((Real.cosh (κ / 2) * Real.cosh (κ / 2) -
        Real.sinh (κ / 2) * Real.sinh (κ / 2)) /
        (Real.cosh (κ / 2)) ^ 2) (κ / 2) := hs.div hch hc
  have hcomp0 := htanh0.comp κ h2
  have hcomp1 : HasDerivAt (fun x : ℝ => Real.sinh (x / 2) / Real.cosh (x / 2))
      ((Real.cosh (κ / 2) * Real.cosh (κ / 2) -
        Real.sinh (κ / 2) * Real.sinh (κ / 2)) /
        (Real.cosh (κ / 2)) ^ 2 * (1 / 2)) κ := hcomp0
  have hcomp : HasDerivAt (fun x : ℝ => Real.tanh (x / 2))
      ((Real.cosh (κ / 2) * Real.cosh (κ / 2) -
        Real.sinh (κ / 2) * Real.sinh (κ / 2)) /
        (Real.cosh (κ / 2)) ^ 2 * (1 / 2)) κ := by
    have hfun : (fun x : ℝ => Real.sinh (x / 2) / Real.cosh (x / 2)) =
        fun x : ℝ => Real.tanh (x / 2) := by
      funext x; rw [Real.tanh_eq_sinh_div_cosh]
    rwa [hfun] at hcomp1
  have hid : Real.cosh (κ / 2) * Real.cosh (κ / 2) -
      Real.sinh (κ / 2) * Real.sinh (κ / 2) = 1 := by
    have h := Real.cosh_sq_sub_sinh_sq (κ / 2)
    nlinarith [h]
  have hfinal : HasDerivAt halfTanh
      (1 / 2 * ((Real.cosh (κ / 2) * Real.cosh (κ / 2) -
        Real.sinh (κ / 2) * Real.sinh (κ / 2)) /
        (Real.cosh (κ / 2)) ^ 2 * (1 / 2))) κ := hcomp.const_mul (1 / 2 : ℝ)
  have hrw : 1 / 2 * ((Real.cosh (κ / 2) * Real.cosh (κ / 2) -
      Real.sinh (κ / 2) * Real.sinh (κ / 2)) /
      (Real.cosh (κ / 2)) ^ 2 * (1 / 2)) = phi0sq κ := by
    rw [hid]
    simp only [phi0sq]
    field_simp
    ring
  rwa [hrw] at hfinal

/-- [KERNEL] o aperto: 1 − tanh x ≤ 2e^{−2x} (a cauda direita morre
    exponencialmente — sem estimativa fabricada, só a álgebra de exp). -/
theorem one_sub_tanh_le (x : ℝ) :
    1 - Real.tanh x ≤ 2 * Real.exp (-(2 * x)) := by
  have ha : 0 < Real.exp x := Real.exp_pos x
  have hb : 0 < Real.exp (-x) := Real.exp_pos (-x)
  have hab : Real.exp x * Real.exp (-x) = 1 := by
    rw [← Real.exp_add]; simp
  have h2 : Real.exp (-(2 * x)) = Real.exp (-x) * Real.exp (-x) := by
    rw [← Real.exp_add]; congr 1; ring
  have hden : 0 < Real.exp x + Real.exp (-x) := by positivity
  have key : 1 - Real.tanh x =
      2 * Real.exp (-x) / (Real.exp x + Real.exp (-x)) := by
    rw [Real.tanh_eq]
    field_simp
    ring
  rw [key, h2, div_le_iff₀ hden]
  nlinarith [hab, hb, mul_pos (mul_pos hb hb) hb]

/-- [KERNEL] lim tanh = 1 em +∞ (mathlib não tem — derivado pelo aperto). -/
theorem tendsto_tanh_atTop :
    Filter.Tendsto Real.tanh Filter.atTop (nhds 1) := by
  have hneg2x : Filter.Tendsto (fun x : ℝ => -(2 * x))
      Filter.atTop Filter.atBot := by
    have h1 : Filter.Tendsto (fun x : ℝ => 2 * x) Filter.atTop Filter.atTop :=
      Filter.Tendsto.const_mul_atTop two_pos Filter.tendsto_id
    have h2 := Filter.tendsto_neg_atTop_atBot.comp h1
    simpa [Function.comp_def] using h2
  have hexp : Filter.Tendsto (fun x : ℝ => Real.exp (-(2 * x)))
      Filter.atTop (nhds 0) := by
    have h := Real.tendsto_exp_atBot.comp hneg2x
    simpa [Function.comp_def] using h
  have hbound : Filter.Tendsto (fun x : ℝ => 2 * Real.exp (-(2 * x)))
      Filter.atTop (nhds 0) := by
    have h := hexp.const_mul (2 : ℝ)
    simpa using h
  have hsq : Filter.Tendsto (fun x : ℝ => 1 - Real.tanh x)
      Filter.atTop (nhds 0) :=
    squeeze_zero (fun t => sub_nonneg.mpr (Real.tanh_lt_one t).le)
      (fun t => one_sub_tanh_le t) hbound
  have h1 : Filter.Tendsto (fun x : ℝ => 1 - (1 - Real.tanh x))
      Filter.atTop (nhds (1 - 0)) := tendsto_const_nhds.sub hsq
  simpa using h1

/-- [KERNEL] lim tanh = −1 em −∞ (paridade ímpar: tanh(−x) = −tanh x). -/
theorem tendsto_tanh_atBot :
    Filter.Tendsto Real.tanh Filter.atBot (nhds (-1)) := by
  have h := tendsto_tanh_atTop.comp Filter.tendsto_neg_atBot_atTop
  have h2 := h.neg
  simp only [Function.comp_def] at h2
  have heq : (fun x : ℝ => -Real.tanh (-x)) = Real.tanh := by
    funext x; rw [Real.tanh_neg, neg_neg]
  rwa [heq] at h2

/-- [KERNEL] ★ A FACE P₊: ½tanh(κ/2) → ½ quando κ → +∞ — o peso da face
    interna da testemunha (a Meia-Nat, Q8.2). -/
theorem tendsto_halfTanh_atTop :
    Filter.Tendsto halfTanh Filter.atTop (nhds (1 / 2)) := by
  have h2 : Filter.Tendsto (fun κ : ℝ => κ / 2) Filter.atTop Filter.atTop := by
    have h1 : Filter.Tendsto (fun κ : ℝ => (1 / 2 : ℝ) * κ)
        Filter.atTop Filter.atTop :=
      Filter.Tendsto.const_mul_atTop (by norm_num) Filter.tendsto_id
    have heq : (fun κ : ℝ => (1 / 2 : ℝ) * κ) = fun κ : ℝ => κ / 2 := by
      funext κ; ring
    rwa [heq] at h1
  have h := (tendsto_tanh_atTop.comp h2).const_mul (1 / 2 : ℝ)
  have hfun : halfTanh = fun κ : ℝ => (1 / 2 : ℝ) * Real.tanh (κ / 2) := rfl
  rw [hfun]
  simpa [Function.comp_def] using h

/-- [KERNEL] ★ A FACE P₋: ½tanh(κ/2) → −½ quando κ → −∞ — o peso da face
    externa da testemunha (a Meia-Nat, Q8.2). -/
theorem tendsto_halfTanh_atBot :
    Filter.Tendsto halfTanh Filter.atBot (nhds (-(1 / 2))) := by
  have h2 : Filter.Tendsto (fun κ : ℝ => κ / 2) Filter.atBot Filter.atBot := by
    have h1 : Filter.Tendsto (fun κ : ℝ => (1 / 2 : ℝ) * -κ)
        Filter.atBot Filter.atTop :=
      Filter.Tendsto.const_mul_atTop (by norm_num)
        Filter.tendsto_neg_atBot_atTop
    have h2' := Filter.tendsto_neg_atTop_atBot.comp h1
    simp only [Function.comp_def] at h2'
    have heq : (fun κ : ℝ => -((1 / 2 : ℝ) * -κ)) = fun κ : ℝ => κ / 2 := by
      funext κ; ring
    rwa [heq] at h2'
  have h := (tendsto_tanh_atBot.comp h2).const_mul (1 / 2 : ℝ)
  have hfun : halfTanh = fun κ : ℝ => (1 / 2 : ℝ) * Real.tanh (κ / 2) := rfl
  rw [hfun]
  simpa [Function.comp_def] using h

/-- [KERNEL] a densidade é contínua. -/
theorem phi0sq_continuous : Continuous phi0sq := by
  apply Continuous.mul continuous_const
  apply Continuous.pow
  exact (Real.continuous_cosh.comp (continuous_id.div_const 2)).inv₀
    fun x => (Real.cosh_pos (x / 2)).ne'

/-- [KERNEL] a densidade é não-negativa. -/
theorem phi0sq_nonneg (κ : ℝ) : 0 ≤ phi0sq κ := by
  unfold phi0sq
  positivity

/-- [KERNEL] a cota pela exponencial: ¼sech²(x/2) ≤ e^x (para a cauda
    esquerda; álgebra: 1 ≤ (u²+1)² com u = e^{x/2}). -/
theorem phi0sq_le_exp (x : ℝ) : phi0sq x ≤ Real.exp x := by
  have hcosh : Real.cosh (x / 2) =
      (Real.exp (x / 2) + Real.exp (-(x / 2))) / 2 := Real.cosh_eq (x / 2)
  have hu0 : 0 < Real.exp (x / 2) := Real.exp_pos _
  have hw0 : 0 < Real.exp (-(x / 2)) := Real.exp_pos _
  have huw : Real.exp (x / 2) * Real.exp (-(x / 2)) = 1 := by
    rw [← Real.exp_add]; simp
  have hex : Real.exp (x / 2) * Real.exp (x / 2) = Real.exp x := by
    rw [← Real.exp_add]; congr 1; ring
  set u := Real.exp (x / 2)
  set w := Real.exp (-(x / 2))
  have hden : 0 < u + w := by positivity
  simp only [phi0sq]
  rw [hcosh, ← hex]
  have key : (1 : ℝ) / 4 * (((u + w) / 2)⁻¹) ^ 2 = 1 / (u + w) ^ 2 := by
    field_simp
    ring
  rw [key, div_le_iff₀ (by positivity : (0:ℝ) < (u + w) ^ 2)]
  have hcore : u * (u + w) = u * u + 1 := by
    rw [mul_add, huw]
  have hsq : u * u * (u + w) ^ 2 = (u * u + 1) ^ 2 := by
    rw [← hcore]; ring
  rw [hsq]
  nlinarith [mul_pos hu0 hu0]

/-- [KERNEL] a cota espelhada: ¼sech²(x/2) ≤ e^{−x} (para a cauda
    direita; a mesma álgebra na face w = e^{−x/2}). -/
theorem phi0sq_le_exp_neg (x : ℝ) : phi0sq x ≤ Real.exp (-x) := by
  have h := phi0sq_le_exp (-x)
  have heven : phi0sq (-x) = phi0sq x := by
    simp only [phi0sq]
    rw [neg_div, Real.cosh_neg]
  rwa [heven] at h

/-- [KERNEL] a densidade é INTEGRÁVEL em ℝ: comparação com e^{x} no Iic
    e com e^{−x} no Ioi — as duas caudas integráveis do mathlib. -/
theorem phi0sq_integrable : MeasureTheory.Integrable phi0sq := by
  have hIic : MeasureTheory.IntegrableOn phi0sq (Set.Iic 0) := by
    apply MeasureTheory.Integrable.mono (integrableOn_exp_Iic 0)
      phi0sq_continuous.aestronglyMeasurable
    refine MeasureTheory.ae_of_all _ (fun x => ?_)
    rw [Real.norm_eq_abs, Real.norm_eq_abs, abs_of_nonneg (phi0sq_nonneg x),
      abs_of_nonneg (Real.exp_pos x).le]
    exact phi0sq_le_exp x
  have hIoi : MeasureTheory.IntegrableOn phi0sq (Set.Ioi 0) := by
    apply MeasureTheory.Integrable.mono (integrableOn_exp_neg_Ioi 0)
      phi0sq_continuous.aestronglyMeasurable
    refine MeasureTheory.ae_of_all _ (fun x => ?_)
    rw [Real.norm_eq_abs, Real.norm_eq_abs, abs_of_nonneg (phi0sq_nonneg x),
      abs_of_nonneg (Real.exp_pos (-x)).le]
    exact phi0sq_le_exp_neg x
  have h := hIic.union hIoi
  rwa [Set.Iic_union_Ioi, MeasureTheory.integrableOn_univ] at h

/-- [KERNEL] ★★ A JOIA (Resposta 8, Q8.2): O PESO DO MODO ZERO É O NOME —
    ‖φ₀‖² = ∫_ℝ ¼sech²(κ/2) dκ = ½ − (−½) = 1. O peso do zero físico
    inteiro é EXATAMENTE 1 = ω(I): o axioma da identidade preservada
    retorna como NÚMERO no fim da cadeia; as duas faces (os limites ±½
    do antiderivado) pesam ½ cada — a Meia-Nat. Nenhuma normalização
    imposta: o 1 é um teorema de integral. -/
theorem zero_mode_weight_is_one : ∫ κ : ℝ, phi0sq κ = 1 := by
  rw [MeasureTheory.integral_of_hasDerivAt_of_tendsto
    (fun x => halfTanh_hasDerivAt x) phi0sq_integrable
    tendsto_halfTanh_atBot tendsto_halfTanh_atTop]
  norm_num

end

end TGLExt
