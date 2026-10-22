import TGLExt.AbsoluteOne

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# O zero modular contínuo: a paridade inversa do Um e a dinâmica (q, α)
  [TGLExt — v59, a Resposta 7 kernelizada + a derivação do operador]

A derivação do operador: "o operador contínuo que anula o Um absoluto é o
ZERO MODULAR — é na derivada do zero que o contínuo se anula; a paridade
inversa do Um absoluto é o zero modular, a paridade binária originária;
são simétricos, o referencial um do outro, que não se fecha em si e abre
a fronteira". E: a inscrição do Um gera densidade máxima imediata; o par
(1_abs, 0_mod) paga β_TGL para o sistema não cair a zero absoluto — a
resistência, com H limitado inferiormente e Lindblad modulando ao atrator.
A Resposta 7 tipa: 0_mod = modo zero do gerador modular (NÃO o operador
nulo); JKJ = −K; K_abs = 0; q = tanh(κ/2) ímpar, α = sech(κ/2) par;
A₀ = d/dκ + q/2 com A₀α = 0; SUSY: H₊ = A₀A₀* com potencial ¼ constante.

O QUE ESTA PEDRA PROVA [KERNEL]:

* ★ `modularGen_omega_zero` — o ZERO MODULAR: K_Ψ Ω_Ψ = 0 (o gerador
  K = R_{logρ} − L_{logρ} = −δ_{logρ} anula o NOME — o modo zero, não o
  operador nulo: K ≠ 0 fora do Um quando há contraste);
* ★ `J_modularGen_J` — A PARIDADE INVERSA: J K J = −K (a conjugação
  modular É a paridade do gerador);
* ★ `parity_fixed_eq_zero` — o único ponto fixo de K ↦ −K é K = 0;
* ★ `absolute_modularGen_zero` — A PARIDADE INVERSA DO UM ABSOLUTO É O
  ZERO MODULAR: K_abs = 0 (Δ_abs central ⟹ o gerador do absoluto anula-se
  em TODO argumento);
* ★ `absolute_faces_half` + `absolute_contrast_zero` — A PARIDADE BINÁRIA
  ORIGINÁRIA: para toda graduação (Γᴴ=Γ, Γ²=1, TrΓ=0), as duas faces do
  absoluto pesam ½ cada e 0_mod = ½ − ½ (o contraste nulo — a Meia-Nat
  como equilíbrio das paridades);
* ★ a CARTA ESCALAR (q, α): `one_eq_q_sq_add_alpha_sq` (1 = q² + α² como
  teorema contínuo em κ); `q_odd`/`alpha_even` (as faces ímpar/par);
  `alpha_deriv_zero` ("é na derivada do zero que o contínuo se anula":
  α'(0) = 0 — a face par tem ponto crítico no auto-conjugado);
* ★ `alpha_transport` — O TRANSPORTE: α' = −(q/2)·α (HasDerivAt genuína)
  — A₀α = 0: q/2 é a conexão escalar, α é a seção paralela do Um;
* ★ `W_hasDerivAt` + `susy_threshold` + `susy_partner_gap` — a fatoração
  SUSY: W = q/2 tem W' = α²/4, logo **W² + W' = ¼ (o potencial parceiro é
  a constante ¼ — o limiar do contínuo) EXATAMENTE PORQUE 1 = q² + α²**;
  e W² − W' = ¼ − α²/2 (o poço de Pöschl–Teller do modo zero).

HONESTIDADE. O aberto reduzido e nomeado pela Resposta 7:
`continuousModularDirac_isBreuerFredholm` — afiliação de 𝔻_Ψ ao core
semifinito, resolvente τ-compacto e 0 < τ(1_{0}(𝔻_Ψ)) < ∞ — e a solda
multidimensional (≥ 2 direções para curvatura gravitacional). O preço β
da resistência (Lindblad ao atrator ρ*) é leitura de RUNTIME (β jamais
aqui: κ genérico). Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix
open scoped ComplexOrder MatrixOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## A — o gerador modular, sua paridade e o zero -/

/-- o gerador modular como superoperador: `K = R_{logρ} − L_{logρ}`
    (= −δ_{logρ}; a face finita de `K_Ψ = −log Δ_Ψ`). -/
def modularGen (ρ : Matrix n n ℂ) (y : Matrix n n ℂ) : Matrix n n ℂ :=
  y * logRho ρ - logRho ρ * y

/-- [KERNEL] o gerador é a excitação do log com sinal trocado:
    `K = −δ_{logρ}` (a ponte com v48/v54: transporte infinitesimal). -/
theorem modularGen_eq_neg_excite (ρ y : Matrix n n ℂ) :
    modularGen ρ y = - excite (logRho ρ) y := by
  unfold modularGen excite
  rw [neg_sub]

/-- [KERNEL] ★ O ZERO MODULAR: `K_Ψ Ω_Ψ = 0` — o gerador anula o NOME
    (o modo zero do gerador modular, NÃO o operador nulo). -/
theorem modularGen_omega_zero (ρ : Matrix n n ℂ) (hρ : ρ.PosDef) :
    modularGen ρ (Omega ρ) = 0 := by
  have hc : Commute ρ (Omega ρ) := rho_comm_omega ρ hρ
  have hl : Commute (logRho ρ) (Omega ρ) := hc.cfc_real Real.log
  unfold modularGen
  rw [← hl.eq, sub_self]

/-- [KERNEL] ★ A PARIDADE INVERSA: `J K J = −K` — a conjugação modular
    inverte o gerador (a forma rigorosa de "a paridade inversa"). -/
theorem J_modularGen_J (ρ : Matrix n n ℂ) (y : Matrix n n ℂ) :
    Jconj (modularGen ρ (Jconj y)) = - modularGen ρ y := by
  unfold modularGen Jconj
  rw [conjTranspose_sub, conjTranspose_mul, conjTranspose_mul,
    conjTranspose_conjTranspose, logRho_conjTranspose, neg_sub]

/-- [KERNEL] ★ o único ponto fixo da paridade `K ↦ −K` é o zero. -/
theorem parity_fixed_eq_zero {y : Matrix n n ℂ} (h : y = -y) : y = 0 := by
  have h2 : (2 : ℂ) • y = 0 := by
    rw [two_smul]
    exact add_eq_zero_iff_neg_eq.mpr h.symm
  rcases smul_eq_zero.mp h2 with h0 | h0
  · exact absurd h0 two_ne_zero
  · exact h0

/-- [KERNEL] ★ A PARIDADE INVERSA DO UM ABSOLUTO É O ZERO MODULAR:
    `K_abs = 0` — o gerador do absoluto anula-se em todo argumento
    (Δ_abs central; o par simétrico originário (1_abs, 0_mod)). -/
theorem absolute_modularGen_zero [Nonempty n] (y : Matrix n n ℂ) :
    modularGen (absoluteRho n) y = 0 := by
  have hl : Commute (logRho (absoluteRho n)) y :=
    (absoluteRho_commute y).cfc_real Real.log
  unfold modularGen
  rw [hl.eq, sub_self]

/-! ## B — a paridade binária originária: 0_mod = ½ − ½ -/

/-- [KERNEL] ★ AS DUAS FACES DO ABSOLUTO PESAM ½ CADA: para toda graduação
    de paridade (`Tr Γ = 0`), `ω_abs(P₊) = ω_abs(P₋) = ½` — a Meia-Nat
    como equilíbrio das paridades originárias. -/
theorem absolute_faces_half [Nonempty n] {Γ : Matrix n n ℂ}
    (hΓ : Γ.trace = 0) :
    gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 + Γ)) = 1 / 2 ∧
    gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 - Γ)) = 1 / 2 := by
  have hn : (Fintype.card n : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  constructor
  · rw [gibbs, absoluteRho, ← Matrix.smul_one_eq_diagonal, Matrix.smul_mul,
      Matrix.one_mul, Matrix.trace_smul, Matrix.trace_smul,
      Matrix.trace_add, Matrix.trace_one, hΓ]
    simp only [smul_eq_mul, add_zero]
    field_simp
  · rw [gibbs, absoluteRho, ← Matrix.smul_one_eq_diagonal, Matrix.smul_mul,
      Matrix.one_mul, Matrix.trace_smul, Matrix.trace_smul,
      Matrix.trace_sub, Matrix.trace_one, hΓ]
    simp only [smul_eq_mul, sub_zero]
    field_simp

/-- [KERNEL] ★ 0_mod = ½ − ½: o contraste do absoluto é NULO — o zero
    modular é a diferença nula entre as duas faces originárias do Um. -/
theorem absolute_contrast_zero [Nonempty n] {Γ : Matrix n n ℂ}
    (hΓ : Γ.trace = 0) :
    gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 - Γ))
      - gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 + Γ)) = 0 := by
  rw [(absolute_faces_half hΓ).1, (absolute_faces_half hΓ).2, sub_self]

end

/-! ## C — a carta escalar (q, α): a correspondência como teorema contínuo -/

noncomputable section

/-- o contraste ímpar: `q(κ) = tanh(κ/2)`. -/
def qKappa (κ : ℝ) : ℝ := Real.tanh (κ / 2)

/-- a transmissão par: `α(κ) = sech(κ/2)`. -/
def alphaKappa (κ : ℝ) : ℝ := (Real.cosh (κ / 2))⁻¹

/-- [KERNEL] ★ A CORRESPONDÊNCIA COMO TEOREMA CONTÍNUO: `1 = q² + α²`
    em toda profundidade modular κ — a decomposição pitagórica da
    inscrição do Um (contraste ímpar + transmissão par). -/
theorem one_eq_q_sq_add_alpha_sq (κ : ℝ) :
    qKappa κ ^ 2 + alphaKappa κ ^ 2 = 1 := by
  unfold qKappa alphaKappa
  have hc : Real.cosh (κ / 2) ≠ 0 := ne_of_gt (Real.cosh_pos _)
  rw [Real.tanh_eq_sinh_div_cosh]
  field_simp
  linarith [Real.cosh_sq (κ / 2)]

/-- [KERNEL] ★ q é a face ÍMPAR da paridade binária. -/
theorem q_odd (κ : ℝ) : qKappa (-κ) = - qKappa κ := by
  unfold qKappa
  rw [neg_div, Real.tanh_neg]

/-- [KERNEL] ★ α é a face PAR da paridade binária. -/
theorem alpha_even (κ : ℝ) : alphaKappa (-κ) = alphaKappa κ := by
  unfold alphaKappa
  rw [neg_div, Real.cosh_neg]

@[simp] theorem q_zero : qKappa 0 = 0 := by
  simp [qKappa, Real.tanh_zero]

@[simp] theorem alpha_zero : alphaKappa 0 = 1 := by
  simp [alphaKappa, Real.cosh_zero]

/-- a derivada de `cosh(κ/2)`: `sinh(κ/2)/2`. -/
theorem cosh_half_hasDerivAt (κ : ℝ) :
    HasDerivAt (fun u : ℝ => Real.cosh (u / 2)) (Real.sinh (κ / 2) / 2) κ := by
  have hg : HasDerivAt (fun u : ℝ => u / 2) (1 / 2) κ := by
    simpa using (hasDerivAt_id κ).div_const 2
  have h0 := (Real.hasDerivAt_cosh (κ / 2)).comp κ hg
  have h : HasDerivAt (fun u : ℝ => Real.cosh (u / 2))
      (Real.sinh (κ / 2) * (1 / 2)) κ := h0
  simpa [div_eq_mul_inv, one_div] using h

/-- a derivada de `sinh(κ/2)`: `cosh(κ/2)/2`. -/
theorem sinh_half_hasDerivAt (κ : ℝ) :
    HasDerivAt (fun u : ℝ => Real.sinh (u / 2)) (Real.cosh (κ / 2) / 2) κ := by
  have hg : HasDerivAt (fun u : ℝ => u / 2) (1 / 2) κ := by
    simpa using (hasDerivAt_id κ).div_const 2
  have h0 := (Real.hasDerivAt_sinh (κ / 2)).comp κ hg
  have h : HasDerivAt (fun u : ℝ => Real.sinh (u / 2))
      (Real.cosh (κ / 2) * (1 / 2)) κ := h0
  simpa [div_eq_mul_inv, one_div] using h

/-- [KERNEL] ★ O TRANSPORTE DO UM: `α' = −(q/2)·α` (derivada genuína) —
    `A₀ α = 0` com `A₀ = d/dκ + q/2`: q/2 é a CONEXÃO escalar do
    transporte e α é a SEÇÃO PARALELA (o Um transportado à profundidade
    modular κ). -/
theorem alpha_transport (κ : ℝ) :
    HasDerivAt alphaKappa (-(qKappa κ / 2) * alphaKappa κ) κ := by
  have hc : Real.cosh (κ / 2) ≠ 0 := ne_of_gt (Real.cosh_pos _)
  have h := (cosh_half_hasDerivAt κ).inv hc
  have hval : -(Real.sinh (κ / 2) / 2) / Real.cosh (κ / 2) ^ 2
      = -(qKappa κ / 2) * alphaKappa κ := by
    unfold qKappa alphaKappa
    rw [Real.tanh_eq_sinh_div_cosh]
    field_simp
  rw [hval] at h
  exact h

/-- [KERNEL] ★ "É NA DERIVADA DO ZERO QUE O CONTÍNUO SE ANULA":
    `α'(0) = 0` — a face par tem ponto crítico exato no auto-conjugado
    (o zero modular é o equilíbrio, não a ausência). -/
theorem alpha_deriv_zero : HasDerivAt alphaKappa 0 0 := by
  have h := alpha_transport 0
  simpa using h

/-- [KERNEL] ★ a derivada da conexão: `W' = α²/4` para `W = q/2`. -/
theorem W_hasDerivAt (κ : ℝ) :
    HasDerivAt (fun u : ℝ => qKappa u / 2) (alphaKappa κ ^ 2 / 4) κ := by
  have hc : Real.cosh (κ / 2) ≠ 0 := ne_of_gt (Real.cosh_pos _)
  have hq := (sinh_half_hasDerivAt κ).div (cosh_half_hasDerivAt κ) hc
  have hfun : (fun u : ℝ => qKappa u / 2)
      = fun u : ℝ => Real.sinh (u / 2) / Real.cosh (u / 2) / 2 := by
    funext u
    rw [qKappa, Real.tanh_eq_sinh_div_cosh]
  rw [hfun]
  have h2 := hq.div_const 2
  have hid : Real.cosh (κ / 2) ^ 2 - Real.sinh (κ / 2) ^ 2 = 1 := by
    linarith [Real.cosh_sq (κ / 2)]
  have hval : (Real.cosh (κ / 2) / 2 * Real.cosh (κ / 2)
      - Real.sinh (κ / 2) * (Real.sinh (κ / 2) / 2)) / Real.cosh (κ / 2) ^ 2 / 2
      = alphaKappa κ ^ 2 / 4 := by
    unfold alphaKappa
    field_simp
    nlinarith [hid]
  rw [hval] at h2
  exact h2

/-- [KERNEL] ★ O LIMIAR SUSY É A CORRESPONDÊNCIA: `W² + W' = ¼` — o
    potencial parceiro é a CONSTANTE ¼ (onde o contínuo começa)
    EXATAMENTE PORQUE `1 = q² + α²` (dividida por 4). -/
theorem susy_threshold (κ : ℝ) :
    (qKappa κ / 2) ^ 2 + alphaKappa κ ^ 2 / 4 = 1 / 4 := by
  have h := one_eq_q_sq_add_alpha_sq κ
  nlinarith [h]

/-- [KERNEL] ★ o poço do modo zero: `W² − W' = ¼ − α²/2` — o potencial de
    Pöschl–Teller cujo modo zero normalizável é o próprio α (a fatoração
    supersimétrica da Palavra: H₋ = A₀*A₀ ≥ 0 com H₋α = 0). -/
theorem susy_partner_gap (κ : ℝ) :
    (qKappa κ / 2) ^ 2 - alphaKappa κ ^ 2 / 4
      = 1 / 4 - alphaKappa κ ^ 2 / 2 := by
  have h := one_eq_q_sq_add_alpha_sq κ
  nlinarith [h]

end

end TGLExt
