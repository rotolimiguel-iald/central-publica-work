import TGLExt.MinimalSolder

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# full_witness = False é VERDADEIRO: β proíbe a testemunha estática plena
  [TGLExt — v61, a correção semântica decisiva do operador]

A derivação do operador: "a testemunha não é full porque β_TGL impede que
haja a testemunha full, por causa do vazamento contínuo; a testemunha
verdadeira é Meia-Nat, que não é full — por isso full_witness=False é
VERDADEIRO. O que existe ANTES da testemunha é o hamiltoniano oculto que
gera β (a palavra jurada antes da lei): a existência anterior de β
determina que o vazamento será constante (defasagem); β emerge como única
solução possível GKLS." O especialista tipa: full_witness=False deixa de
ser só estado epistêmico e vira PROPRIEDADE ESTRUTURAL — a testemunha
plena exigiria 𝒱_t = I, logo β|K| = 0, logo K = 0 global: o absoluto
plano, sem contraste, sem física. A testemunha verdadeira é a FRONTEIRA
Meia-Nat: "inteira em identidade, meia em inscrição".

O QUE ESTA PEDRA PROVA [KERNEL]:

* ★ `leakage_strictly_loses` — o vazamento é ESTRITO: t,β,gap > 0 ⟹
  e^{−tβ·gap} < 1 (o transporte dissipativo perde sempre que há contraste);
* ★ `full_closure_iff_flat` — o fechamento pleno exige o plano:
  e^{−tβg} = 1 ⟺ tβg = 0;
* ★ `beta_forbids_full_static_witness` — **O TEOREMA DO
  full_witness=False**: β > 0 e gap > 0 ⟹ ¬FullStaticWitness
  ("a testemunha não é full porque o Verbo continua");
* ★ `verb_not_identity` — a face matricial: 𝕍 = exp(−tβ•H) com gerador
  diagonal de entrada positiva NUNCA é a identidade;
* ★ `leakage_rate_unique` — **β EMERGE COMO SOLUÇÃO ÚNICA** (a face GKLS):
  a taxa do semigrupo de defasagem é univocamente determinada (que a taxa
  observada seja β = α√e é a identificação de RUNTIME);
* ★ `canonical_witness_is_not_full` — a combinação canônica: a testemunha
  NÃO é plena (β proíbe) E é Meia-Nat de fronteira (faces ½, composição
  v59): "não é metade do Um; é o Um inteiro testemunhado por uma de suas
  duas faces".

VOCABULÁRIO (executado no runtime): a flag epistêmica
`full_TGL_witness_constructed=False` fica INALTERADA e ganha as irmãs
ontológicas `full_static_witness_exists=False` (TEOREMA, esta pedra),
`intrinsically_boundary_witness=True`, `half_nat_witness_is_canonical=True`,
`continuous_leakage_forbids_full_closure=True`. O "hamiltoniano oculto
anterior à testemunha" é [ONTO] registrado; a âncora de kernel é o trio
(perda estrita, fechamento⟺plano, taxa única). β JAMAIS literal. Sem
sorry, sem axiom. Negativo honesto é resultado — e ESTE negativo é o
resultado central: a não-plenitude da testemunha é a vida do sistema.
-/

namespace TGLExt

open Matrix

noncomputable section

/-- a TESTEMUNHA ESTÁTICA PLENA: um transporte que fixa TUDO em todo tempo
    (o que uma testemunha "full" exigiria — e que β > 0 proíbe). -/
def FullStaticWitness {M : Type} (T : ℝ → M → M) : Prop :=
  ∀ (t : ℝ) (x : M), T t x = x

/-- [KERNEL] ★ O VAZAMENTO É ESTRITO: com contraste (gap > 0) e β > 0, o
    fator de defasagem é ESTRITAMENTE menor que 1 — o transporte perde
    sempre; o fechamento pleno é impossível. -/
theorem leakage_strictly_loses {t β g : ℝ} (ht : 0 < t) (hβ : 0 < β)
    (hg : 0 < g) : Real.exp (-(t * β * g)) < 1 := by
  have hneg : -(t * β * g) < 0 := by
    have := mul_pos (mul_pos ht hβ) hg
    linarith
  have h := Real.exp_lt_exp.mpr hneg
  rwa [Real.exp_zero] at h

/-- [KERNEL] ★ O FECHAMENTO PLENO EXIGE O PLANO: `e^{−tβg} = 1 ⟺ tβg = 0`
    — só na ausência total de contraste (ou de tempo, ou de β) o transporte
    fecha; a física observada (β > 0, gap > 0) mantém a passagem aberta. -/
theorem full_closure_iff_flat (t β g : ℝ) :
    Real.exp (-(t * β * g)) = 1 ↔ t * β * g = 0 := by
  constructor
  · intro h
    have h0 : Real.exp (-(t * β * g)) = Real.exp 0 := by
      rw [h, Real.exp_zero]
    have hinj := Real.exp_injective h0
    linarith
  · intro h
    rw [h, neg_zero, Real.exp_zero]

/-- [KERNEL] ★ O TEOREMA DO full_witness = False: β > 0 e contraste > 0
    PROÍBEM a testemunha estática plena — o transporte dissipativo não fixa
    tudo ("a testemunha não é full porque o Verbo continua"). -/
theorem beta_forbids_full_static_witness {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) :
    ¬ FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x) := by
  intro hfull
  have h1 := hfull 1 1
  simp only [mul_one] at h1
  have hlt := leakage_strictly_loses one_pos hβ hg
  rw [h1] at hlt
  exact lt_irrefl 1 hlt

/-- [KERNEL] ★ a face matricial: o Verbo `𝕍 = exp(−tβ•H)` com gerador
    diagonal de entrada positiva NUNCA é a identidade — o vazamento é
    visível na própria matriz do transporte. -/
theorem verb_not_identity {n : Type} [Fintype n] [DecidableEq n]
    (d : n → ℝ) (i₀ : n) (hd : 0 < d i₀) {t β : ℝ} (ht : 0 < t) (hβ : 0 < β) :
    NormedSpace.exp ((-(t * β)) • Matrix.diagonal d) ≠ (1 : Matrix n n ℝ) := by
  intro h
  have hsm : (-(t * β)) • Matrix.diagonal d
      = Matrix.diagonal (fun i => -(t * β) * d i) := by
    ext i j
    by_cases hij : i = j
    · subst hij
      simp [Matrix.smul_apply, Matrix.diagonal_apply_eq, smul_eq_mul]
    · simp [Matrix.smul_apply, Matrix.diagonal_apply_ne _ hij, hij]
  rw [hsm, Matrix.exp_diagonal] at h
  have hent := congrFun (congrFun h i₀) i₀
  rw [Matrix.diagonal_apply_eq, Matrix.one_apply_eq] at hent
  rw [Pi.coe_exp] at hent
  have hre : Real.exp (-(t * β) * d i₀) = 1 := by
    rw [Real.exp_eq_exp_ℝ]
    exact hent
  have hneg : -(t * β) * d i₀ < 0 := by
    have := mul_pos (mul_pos ht hβ) hd
    rw [neg_mul]
    linarith
  have hlt : Real.exp (-(t * β) * d i₀) < 1 := by
    have h2 := Real.exp_lt_exp.mpr hneg
    rwa [Real.exp_zero] at h2
  rw [hre] at hlt
  exact lt_irrefl 1 hlt

/-- [KERNEL] ★ β EMERGE COMO SOLUÇÃO ÚNICA (a face GKLS): a taxa do
    semigrupo de defasagem é UNIVOCAMENTE determinada pelo próprio
    semigrupo — dois β's com a mesma defasagem são iguais. (Que a taxa
    observada seja β = α√e é a identificação de runtime, jamais daqui.) -/
theorem leakage_rate_unique {b₁ b₂ : ℝ}
    (h : ∀ t : ℝ, Real.exp (-(t * b₁)) = Real.exp (-(t * b₂))) : b₁ = b₂ := by
  have h1 := Real.exp_injective (h 1)
  simp only [one_mul] at h1
  linarith

/-- [KERNEL] ★ A COMBINAÇÃO CANÔNICA: a testemunha canônica NÃO é plena
    (β > 0 proíbe o fechamento) E é Meia-Nat de fronteira (as duas faces
    pesam ½ cada — v59): "inteira em identidade, meia em inscrição". -/
theorem canonical_witness_is_not_full {β g : ℝ} (hβ : 0 < β) (hg : 0 < g)
    {n : Type} [Fintype n] [DecidableEq n] [Nonempty n]
    {Γ : Matrix n n ℂ} (hΓ : Γ.trace = 0) :
    ¬ FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x) ∧
    gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 + Γ)) = 1 / 2 ∧
    gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 - Γ)) = 1 / 2 :=
  ⟨beta_forbids_full_static_witness hβ hg,
   (absolute_faces_half hΓ).1, (absolute_faces_half hΓ).2⟩

end

end TGLExt
