import TGLExt.RegularRep

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A PAREDE DE FUNDO, PRIMEIRO TIJOLO: "o único traço é zero" — em kernel
  [TGLExt — v119, o incremento 40 do programa SemifiniteAnalysis]

A última parede da testemunha é o fator III₁ — teoria modular de von
Neumann, ausente da mathlib. O mandato: "se tiver que ser feita à mão,
que seja feito." Esta pedra põe o primeiro tijolo:

* ★★ `evenShift`/`oddShift` + retrações — A BIPARTIÇÃO DE ℓ²: quatro
  operadores contínuos com cE·u = 1, cO·v = 1 e u·cE + v·cO = 1 (a casa
  é isomorfa a DUAS cópias de si — a marca das álgebras infinitas), com
  as três identidades PONTUAIS;
* `TracialState` — o contrato tipado do traço limitado (linear,
  positivo-real, *-simétrico, tracial), com star = adjunto da C*-face;
* ★★ `tracial_one_eq_zero` — a bipartição mata φ(1) por traço puro:
  φ(1) = φ(cE·u) = φ(u·cE), idem ímpar; somando, 2φ(1) = φ(1);
* ★★★ `tracial_state_is_zero` — O TEOREMA: TODO estado tracial sobre
  B(ℓ²) é IDENTICAMENTE ZERO — "o único traço é zero" (a leitura do
  operador, v117) no nível da ÁLGEBRA: o argumento quadrático da
  positividade sobre φ(1) = 0;
* ★★ `fullAlgebra` — B(ℓ²) como ÁLGEBRA DE VON NEUMANN (o primeiro
  objeto de von Neumann do programa) e a bipartição mora nela.

HONESTIDADE (sem véu): B(ℓ²) é tipo I∞, não III — o que sobrevive nela
é o PESO semifinito Tr (não-limitado). Este teorema mata os traços
LIMITADOS (estados); a parede III₁ verdadeira = matar também o peso
semifinito normal. Dois mecanismos independentes agora em kernel: o
assassino de FLUXO (v45: τ∘θ_s = e^{−s}τ ⟹ τ = 0) e o assassino de
ÁLGEBRA (v119: a bipartição). O que falta para III₁: pesos, normalidade
e um fator concreto (Araki–Woods) — o programa, pedra a pedra.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ComplexConjugate ENNReal

noncomputable section

/-! ## A — as funções da bipartição -/

/-- (u x)ₖ = x_{k/2} se k é par, 0 se ímpar. -/
def evenShiftFun (x : ℕ → ℂ) : ℕ → ℂ :=
  fun k => if k % 2 = 0 then x (k / 2) else 0

/-- (v x)ₖ = x_{k/2} se k é ímpar, 0 se par. -/
def oddShiftFun (x : ℕ → ℂ) : ℕ → ℂ :=
  fun k => if k % 2 = 1 then x (k / 2) else 0

/-- a retração par: (cE y)ₙ = y_{2n}. -/
def coEvenFun (y : ℕ → ℂ) : ℕ → ℂ := fun n => y (2 * n)

/-- a retração ímpar: (cO y)ₙ = y_{2n+1}. -/
def coOddFun (y : ℕ → ℂ) : ℕ → ℂ := fun n => y (2 * n + 1)

theorem evenShiftFun_double (x : ℕ → ℂ) (n : ℕ) :
    evenShiftFun x (2 * n) = x n := by
  unfold evenShiftFun
  rw [if_pos (by omega : (2 * n) % 2 = 0)]
  congr 1
  omega

theorem oddShiftFun_double (x : ℕ → ℂ) (n : ℕ) :
    oddShiftFun x (2 * n + 1) = x n := by
  unfold oddShiftFun
  rw [if_pos (by omega : (2 * n + 1) % 2 = 1)]
  congr 1
  omega

theorem double_injective : Function.Injective (fun n : ℕ => 2 * n) := by
  intro a b h
  simpa using h

theorem double_succ_injective :
    Function.Injective (fun n : ℕ => 2 * n + 1) := by
  intro a b h
  simpa using h

theorem evenShiftFun_support (x : ℕ → ℂ) (k : ℕ)
    (hk : k ∉ Set.range (fun n : ℕ => 2 * n)) :
    ‖evenShiftFun x k‖ ^ (2 : ℝ≥0∞).toReal = 0 := by
  have hodd : k % 2 = 1 := by
    by_contra h
    exact hk ⟨k / 2, show 2 * (k / 2) = k by omega⟩
  unfold evenShiftFun
  rw [if_neg (by omega)]
  rw [norm_zero]
  rw [Real.zero_rpow (by norm_num)]

theorem oddShiftFun_support (x : ℕ → ℂ) (k : ℕ)
    (hk : k ∉ Set.range (fun n : ℕ => 2 * n + 1)) :
    ‖oddShiftFun x k‖ ^ (2 : ℝ≥0∞).toReal = 0 := by
  have heven : k % 2 = 0 := by
    by_contra h
    exact hk ⟨k / 2, show 2 * (k / 2) + 1 = k by omega⟩
  unfold oddShiftFun
  rw [if_neg (by omega)]
  rw [norm_zero]
  rw [Real.zero_rpow (by norm_num)]

/-! ## B — pertinência e limitação -/

theorem evenShiftFun_support' (x : ℕ → ℂ) :
    (Function.support fun k => ‖evenShiftFun x k‖ ^ (2 : ℝ≥0∞).toReal)
      ⊆ Set.range (fun n : ℕ => 2 * n) := by
  intro k hk
  by_contra hr
  exact hk (evenShiftFun_support x k hr)

theorem oddShiftFun_support' (x : ℕ → ℂ) :
    (Function.support fun k => ‖oddShiftFun x k‖ ^ (2 : ℝ≥0∞).toReal)
      ⊆ Set.range (fun n : ℕ => 2 * n + 1) := by
  intro k hk
  by_contra hr
  exact hk (oddShiftFun_support x k hr)

theorem memℓp_two_iff_summable (f : ℕ → ℂ) :
    Memℓp f 2 ↔ Summable (fun k => ‖f k‖ ^ (2 : ℝ≥0∞).toReal) := by
  constructor
  · intro h
    exact h.summable (by norm_num)
  · intro h
    exact memℓp_gen h

theorem evenShiftFun_memℓp (x : ellTwo) :
    Memℓp (evenShiftFun (x : ℕ → ℂ)) 2 := by
  rw [memℓp_two_iff_summable]
  rw [← Function.Injective.summable_iff double_injective
    (evenShiftFun_support (x : ℕ → ℂ))]
  have hcong : ((fun k => ‖evenShiftFun (x : ℕ → ℂ) k‖ ^ (2 : ℝ≥0∞).toReal)
      ∘ (fun n : ℕ => 2 * n))
      = fun n => ‖(x : ℕ → ℂ) n‖ ^ (2 : ℝ≥0∞).toReal := by
    funext n
    show ‖evenShiftFun (x : ℕ → ℂ) (2 * n)‖ ^ (2 : ℝ≥0∞).toReal = _
    rw [evenShiftFun_double]
  rw [hcong]
  exact (lp.memℓp x).summable (by norm_num)

theorem oddShiftFun_memℓp (x : ellTwo) :
    Memℓp (oddShiftFun (x : ℕ → ℂ)) 2 := by
  rw [memℓp_two_iff_summable]
  rw [← Function.Injective.summable_iff double_succ_injective
    (oddShiftFun_support (x : ℕ → ℂ))]
  have hcong : ((fun k => ‖oddShiftFun (x : ℕ → ℂ) k‖ ^ (2 : ℝ≥0∞).toReal)
      ∘ (fun n : ℕ => 2 * n + 1))
      = fun n => ‖(x : ℕ → ℂ) n‖ ^ (2 : ℝ≥0∞).toReal := by
    funext n
    show ‖oddShiftFun (x : ℕ → ℂ) (2 * n + 1)‖ ^ (2 : ℝ≥0∞).toReal = _
    rw [oddShiftFun_double]
  rw [hcong]
  exact (lp.memℓp x).summable (by norm_num)

theorem coEvenFun_memℓp (y : ellTwo) :
    Memℓp (coEvenFun (y : ℕ → ℂ)) 2 := by
  rw [memℓp_two_iff_summable]
  have hy : Summable (fun k => ‖(y : ℕ → ℂ) k‖ ^ (2 : ℝ≥0∞).toReal) :=
    (lp.memℓp y).summable (by norm_num)
  refine summable_of_sum_range_le
    (c := ∑' k, ‖(y : ℕ → ℂ) k‖ ^ (2 : ℝ≥0∞).toReal) ?_ ?_
  · intro n
    positivity
  · intro N
    have himg : ∑ n ∈ Finset.range N,
        ‖coEvenFun (y : ℕ → ℂ) n‖ ^ (2 : ℝ≥0∞).toReal
        = ∑ k ∈ (Finset.range N).image (fun n => 2 * n),
            ‖(y : ℕ → ℂ) k‖ ^ (2 : ℝ≥0∞).toReal := by
      rw [Finset.sum_image (fun a _ b _ h => double_injective h)]
      rfl
    rw [himg]
    exact Summable.sum_le_tsum _ (fun k _ => by positivity) hy

theorem coOddFun_memℓp (y : ellTwo) :
    Memℓp (coOddFun (y : ℕ → ℂ)) 2 := by
  rw [memℓp_two_iff_summable]
  have hy : Summable (fun k => ‖(y : ℕ → ℂ) k‖ ^ (2 : ℝ≥0∞).toReal) :=
    (lp.memℓp y).summable (by norm_num)
  refine summable_of_sum_range_le
    (c := ∑' k, ‖(y : ℕ → ℂ) k‖ ^ (2 : ℝ≥0∞).toReal) ?_ ?_
  · intro n
    positivity
  · intro N
    have himg : ∑ n ∈ Finset.range N,
        ‖coOddFun (y : ℕ → ℂ) n‖ ^ (2 : ℝ≥0∞).toReal
        = ∑ k ∈ (Finset.range N).image (fun n => 2 * n + 1),
            ‖(y : ℕ → ℂ) k‖ ^ (2 : ℝ≥0∞).toReal := by
      rw [Finset.sum_image (fun a _ b _ h => double_succ_injective h)]
      rfl
    rw [himg]
    exact Summable.sum_le_tsum _ (fun k _ => by positivity) hy

/-! ## C — os quatro operadores contínuos -/

def evenShiftLM : ellTwo →ₗ[ℂ] ellTwo where
  toFun x := ⟨evenShiftFun (x : ℕ → ℂ), evenShiftFun_memℓp x⟩
  map_add' x y := by
    apply Subtype.ext
    funext k
    show evenShiftFun ((x : ℕ → ℂ) + (y : ℕ → ℂ)) k
        = evenShiftFun (x : ℕ → ℂ) k + evenShiftFun (y : ℕ → ℂ) k
    unfold evenShiftFun
    by_cases h : k % 2 = 0 <;> simp [h]
  map_smul' c x := by
    apply Subtype.ext
    funext k
    show evenShiftFun (c • (x : ℕ → ℂ)) k = c • evenShiftFun (x : ℕ → ℂ) k
    unfold evenShiftFun
    by_cases h : k % 2 = 0 <;> simp [h]

def oddShiftLM : ellTwo →ₗ[ℂ] ellTwo where
  toFun x := ⟨oddShiftFun (x : ℕ → ℂ), oddShiftFun_memℓp x⟩
  map_add' x y := by
    apply Subtype.ext
    funext k
    show oddShiftFun ((x : ℕ → ℂ) + (y : ℕ → ℂ)) k
        = oddShiftFun (x : ℕ → ℂ) k + oddShiftFun (y : ℕ → ℂ) k
    unfold oddShiftFun
    by_cases h : k % 2 = 1 <;> simp [h]
  map_smul' c x := by
    apply Subtype.ext
    funext k
    show oddShiftFun (c • (x : ℕ → ℂ)) k = c • oddShiftFun (x : ℕ → ℂ) k
    unfold oddShiftFun
    by_cases h : k % 2 = 1 <;> simp [h]

def coEvenLM : ellTwo →ₗ[ℂ] ellTwo where
  toFun y := ⟨coEvenFun (y : ℕ → ℂ), coEvenFun_memℓp y⟩
  map_add' x y := by
    apply Subtype.ext
    funext n
    show coEvenFun ((x : ℕ → ℂ) + (y : ℕ → ℂ)) n
        = coEvenFun (x : ℕ → ℂ) n + coEvenFun (y : ℕ → ℂ) n
    unfold coEvenFun
    simp
  map_smul' c x := by
    apply Subtype.ext
    funext n
    show coEvenFun (c • (x : ℕ → ℂ)) n = c • coEvenFun (x : ℕ → ℂ) n
    unfold coEvenFun
    simp

def coOddLM : ellTwo →ₗ[ℂ] ellTwo where
  toFun y := ⟨coOddFun (y : ℕ → ℂ), coOddFun_memℓp y⟩
  map_add' x y := by
    apply Subtype.ext
    funext n
    show coOddFun ((x : ℕ → ℂ) + (y : ℕ → ℂ)) n
        = coOddFun (x : ℕ → ℂ) n + coOddFun (y : ℕ → ℂ) n
    unfold coOddFun
    simp
  map_smul' c x := by
    apply Subtype.ext
    funext n
    show coOddFun (c • (x : ℕ → ℂ)) n = c • coOddFun (x : ℕ → ℂ) n
    unfold coOddFun
    simp

theorem norm_sq_eq_tsum (z : ellTwo) :
    ‖z‖ ^ (2 : ℝ≥0∞).toReal
      = ∑' k, ‖(z : ℕ → ℂ) k‖ ^ (2 : ℝ≥0∞).toReal :=
  lp.norm_rpow_eq_tsum (by norm_num) z

theorem sq_le_of_rpow_le {a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b)
    (h : a ^ (2 : ℝ≥0∞).toReal ≤ b ^ (2 : ℝ≥0∞).toReal) : a ≤ b := by
  have h2 : (2 : ℝ≥0∞).toReal = 2 := by norm_num
  rw [h2] at h
  rw [Real.rpow_two, Real.rpow_two] at h
  calc a = Real.sqrt (a ^ 2) := (Real.sqrt_sq ha).symm
    _ ≤ Real.sqrt (b ^ 2) := Real.sqrt_le_sqrt h
    _ = b := Real.sqrt_sq hb

theorem evenShiftLM_norm (x : ellTwo) : ‖evenShiftLM x‖ ≤ 1 * ‖x‖ := by
  rw [one_mul]
  refine sq_le_of_rpow_le (norm_nonneg _) (norm_nonneg _) (le_of_eq ?_)
  rw [norm_sq_eq_tsum, norm_sq_eq_tsum]
  show (∑' k, ‖evenShiftFun (x : ℕ → ℂ) k‖ ^ (2 : ℝ≥0∞).toReal) = _
  rw [← Function.Injective.tsum_eq double_injective
    (evenShiftFun_support' (x : ℕ → ℂ))]
  congr 1
  funext n
  show ‖evenShiftFun (x : ℕ → ℂ) (2 * n)‖ ^ (2 : ℝ≥0∞).toReal = _
  rw [evenShiftFun_double]

theorem oddShiftLM_norm (x : ellTwo) : ‖oddShiftLM x‖ ≤ 1 * ‖x‖ := by
  rw [one_mul]
  refine sq_le_of_rpow_le (norm_nonneg _) (norm_nonneg _) (le_of_eq ?_)
  rw [norm_sq_eq_tsum, norm_sq_eq_tsum]
  show (∑' k, ‖oddShiftFun (x : ℕ → ℂ) k‖ ^ (2 : ℝ≥0∞).toReal) = _
  rw [← Function.Injective.tsum_eq double_succ_injective
    (oddShiftFun_support' (x : ℕ → ℂ))]
  congr 1
  funext n
  show ‖oddShiftFun (x : ℕ → ℂ) (2 * n + 1)‖ ^ (2 : ℝ≥0∞).toReal = _
  rw [oddShiftFun_double]

theorem coEvenLM_norm (y : ellTwo) : ‖coEvenLM y‖ ≤ 1 * ‖y‖ := by
  rw [one_mul]
  have hy : Summable (fun k => ‖(y : ℕ → ℂ) k‖ ^ (2 : ℝ≥0∞).toReal) :=
    (lp.memℓp y).summable (by norm_num)
  have hc : Summable
      (fun n => ‖coEvenFun (y : ℕ → ℂ) n‖ ^ (2 : ℝ≥0∞).toReal) := by
    have h := coEvenFun_memℓp y
    rw [memℓp_two_iff_summable] at h
    exact h
  refine sq_le_of_rpow_le (norm_nonneg _) (norm_nonneg _) ?_
  rw [norm_sq_eq_tsum, norm_sq_eq_tsum]
  show (∑' n, ‖coEvenFun (y : ℕ → ℂ) n‖ ^ (2 : ℝ≥0∞).toReal) ≤ _
  refine Summable.tsum_le_tsum_of_inj (fun n => 2 * n) double_injective
    (fun k _ => by positivity) (fun n => le_of_eq rfl) hc hy

theorem coOddLM_norm (y : ellTwo) : ‖coOddLM y‖ ≤ 1 * ‖y‖ := by
  rw [one_mul]
  have hy : Summable (fun k => ‖(y : ℕ → ℂ) k‖ ^ (2 : ℝ≥0∞).toReal) :=
    (lp.memℓp y).summable (by norm_num)
  have hc : Summable
      (fun n => ‖coOddFun (y : ℕ → ℂ) n‖ ^ (2 : ℝ≥0∞).toReal) := by
    have h := coOddFun_memℓp y
    rw [memℓp_two_iff_summable] at h
    exact h
  refine sq_le_of_rpow_le (norm_nonneg _) (norm_nonneg _) ?_
  rw [norm_sq_eq_tsum, norm_sq_eq_tsum]
  show (∑' n, ‖coOddFun (y : ℕ → ℂ) n‖ ^ (2 : ℝ≥0∞).toReal) ≤ _
  refine Summable.tsum_le_tsum_of_inj (fun n => 2 * n + 1) double_succ_injective
    (fun k _ => by positivity) (fun n => le_of_eq rfl) hc hy

/-- u : o mergulho par (isometria). -/
def evenShift : ellTwo →L[ℂ] ellTwo :=
  LinearMap.mkContinuous evenShiftLM 1 evenShiftLM_norm

/-- v : o mergulho ímpar (isometria). -/
def oddShift : ellTwo →L[ℂ] ellTwo :=
  LinearMap.mkContinuous oddShiftLM 1 oddShiftLM_norm

/-- cE : a retração par. -/
def coEven : ellTwo →L[ℂ] ellTwo :=
  LinearMap.mkContinuous coEvenLM 1 coEvenLM_norm

/-- cO : a retração ímpar. -/
def coOdd : ellTwo →L[ℂ] ellTwo :=
  LinearMap.mkContinuous coOddLM 1 coOddLM_norm

/-! ## D — as identidades da bipartição (PONTUAIS) -/

/-- [KERNEL] ★ cE · u = 1. -/
theorem coEven_evenShift : coEven * evenShift = 1 := by
  ext x n
  show coEvenFun (evenShiftFun (x : ℕ → ℂ)) n = (x : ℕ → ℂ) n
  unfold coEvenFun
  rw [evenShiftFun_double]

/-- [KERNEL] ★ cO · v = 1. -/
theorem coOdd_oddShift : coOdd * oddShift = 1 := by
  ext x n
  show coOddFun (oddShiftFun (x : ℕ → ℂ)) n = (x : ℕ → ℂ) n
  unfold coOddFun
  rw [oddShiftFun_double]

/-- [KERNEL] ★★ A BIPARTIÇÃO: u·cE + v·cO = 1 — a casa é DUAS cópias
    de si mesma (a marca das álgebras infinitas). -/
theorem shift_partition :
    evenShift * coEven + oddShift * coOdd = 1 := by
  ext y k
  show evenShiftFun (coEvenFun (y : ℕ → ℂ)) k
      + oddShiftFun (coOddFun (y : ℕ → ℂ)) k = (y : ℕ → ℂ) k
  unfold evenShiftFun oddShiftFun coEvenFun coOddFun
  by_cases h : k % 2 = 0
  · rw [if_pos h, if_neg (by omega)]
    have hk : 2 * (k / 2) = k := by omega
    rw [hk, add_zero]
  · rw [if_neg h, if_pos (by omega : k % 2 = 1)]
    have hk : 2 * (k / 2) + 1 = k := by omega
    rw [hk, zero_add]

/-! ## E — o contrato do traço limitado e O TEOREMA -/

/-- [DATA — o contrato do traço limitado] linear + positivo-real +
    *-simétrico + tracial (star = adjunto da C*-face). Normalidade NÃO
    é exigida: o teorema mata até os não-normais. -/
structure TracialState where
  φ : (ellTwo →L[ℂ] ellTwo) → ℂ
  map_add : ∀ a b, φ (a + b) = φ a + φ b
  map_smul : ∀ (c : ℂ) a, φ (c • a) = c * φ a
  pos_real : ∀ a, ∃ r : ℝ, 0 ≤ r ∧ φ (star a * a) = (r : ℂ)
  star_symm : ∀ a, φ (star a) = conj (φ a)
  tracial : ∀ a b, φ (a * b) = φ (b * a)

/-- [KERNEL] ★★ A BIPARTIÇÃO MATA φ(1): φ(1) = φ(cE·u) = φ(u·cE) e
    φ(1) = φ(cO·v) = φ(v·cO); somando, 2φ(1) = φ(u·cE + v·cO) = φ(1). -/
theorem tracial_one_eq_zero (T : TracialState) : T.φ 1 = 0 := by
  have h1 : T.φ 1 = T.φ (evenShift * coEven) := by
    rw [← coEven_evenShift]
    exact T.tracial coEven evenShift
  have h2 : T.φ 1 = T.φ (oddShift * coOdd) := by
    rw [← coOdd_oddShift]
    exact T.tracial coOdd oddShift
  have hsum : T.φ 1 + T.φ 1
      = T.φ (evenShift * coEven + oddShift * coOdd) := by
    rw [T.map_add, ← h1, ← h2]
  rw [shift_partition] at hsum
  have h3 : T.φ 1 + T.φ 1 - T.φ 1 = T.φ 1 - T.φ 1 := by rw [hsum]
  simpa using h3

/-- [KERNEL] ★★★ O TEOREMA DO TRAÇO ZERO: todo estado tracial sobre
    B(ℓ²) é IDENTICAMENTE ZERO — "o único traço é zero" (v117), agora
    no nível da álgebra, pelo argumento quadrático da positividade. -/
theorem tracial_state_is_zero (T : TracialState)
    (a : ellTwo →L[ℂ] ellTwo) : T.φ a = 0 := by
  by_contra hne
  have hApos : 0 < ‖T.φ a‖ := norm_pos_iff.mpr hne
  -- a fase w com |w| = 1 e w·φ(a) = ‖φ(a)‖
  set w : ℂ := conj (T.φ a) / (‖T.φ a‖ : ℂ) with hw
  have hwa : w * T.φ a = (‖T.φ a‖ : ℂ) := by
    rw [hw, div_mul_eq_mul_div]
    rw [Complex.conj_mul']
    rw [div_eq_iff (by
      simpa using ne_of_gt hApos : ((‖T.φ a‖ : ℝ) : ℂ) ≠ 0)]
    norm_cast
    ring
  have hwmod : w * conj w = 1 := by
    rw [hw]
    rw [map_div₀, Complex.conj_conj, Complex.conj_ofReal]
    rw [div_mul_div_comm, Complex.conj_mul']
    rw [div_eq_one_iff_eq (by
      have : ((‖T.φ a‖ : ℝ) : ℂ) ≠ 0 := by simpa using ne_of_gt hApos
      exact mul_ne_zero this this)]
    norm_cast
    ring
  obtain ⟨r, hr, hφaa⟩ := T.pos_real a
  -- para todo t real, 0 ≤ 2t‖φ(a)‖ + t²r (a positividade da forma)
  have hkey : ∀ t : ℝ, 0 ≤ 2 * t * ‖T.φ a‖ + t ^ 2 * r := by
    intro t
    set z : ℂ := (t : ℂ) * w with hz
    set b : ellTwo →L[ℂ] ellTwo := 1 + z • a with hb
    obtain ⟨s, hs, hφbb⟩ := T.pos_real b
    -- star b * b expandido
    have hstar : star b = 1 + conj z • star a := by
      rw [hb, star_add, star_one, star_smul]
      rfl
    have hexp : star b * b
        = 1 + z • a + conj z • star a
          + (conj z * z) • (star a * a) := by
      rw [hb, hstar]
      have hsm : (conj z • star a) * (z • a)
          = (conj z * z) • (star a * a) := by
        rw [smul_mul_assoc, mul_smul_comm, smul_smul]
      rw [add_mul]
      rw [mul_add, mul_add]
      simp only [one_mul, mul_one]
      rw [hsm]
      abel
    -- φ do produto
    have hφexp : T.φ (star b * b)
        = z * T.φ a + conj z * conj (T.φ a) + (conj z * z) * (r : ℂ) := by
      rw [hexp]
      rw [T.map_add, T.map_add, T.map_add]
      rw [T.map_smul, T.map_smul, T.map_smul]
      rw [tracial_one_eq_zero T, T.star_symm, hφaa]
      ring
    -- os termos com a fase
    have hz1 : z * T.φ a = ((t * ‖T.φ a‖ : ℝ) : ℂ) := by
      rw [hz, mul_assoc, hwa]
      norm_cast
    have hz2 : conj z * conj (T.φ a) = ((t * ‖T.φ a‖ : ℝ) : ℂ) := by
      have : conj z * conj (T.φ a) = conj (z * T.φ a) :=
        (map_mul (starRingEnd ℂ) z (T.φ a)).symm
      rw [this, hz1, Complex.conj_ofReal]
    have hz3 : conj z * z = ((t ^ 2 : ℝ) : ℂ) := by
      rw [hz, map_mul, Complex.conj_ofReal]
      have : (t : ℂ) * conj w * ((t : ℂ) * w) = (t : ℂ) * (t : ℂ) * (w * conj w) := by
        ring
      rw [this, hwmod]
      norm_cast
      ring
    rw [hz1, hz2, hz3] at hφexp
    rw [hφbb] at hφexp
    -- s real = expressão real: extrair a igualdade em ℝ
    have hreal : (s : ℂ)
        = ((t * ‖T.φ a‖ + t * ‖T.φ a‖ + t ^ 2 * r : ℝ) : ℂ) := by
      rw [hφexp]
      push_cast
      ring
    have hs_eq : s = t * ‖T.φ a‖ + t * ‖T.φ a‖ + t ^ 2 * r :=
      Complex.ofReal_inj.mp hreal
    have : 0 ≤ t * ‖T.φ a‖ + t * ‖T.φ a‖ + t ^ 2 * r := by
      rw [← hs_eq]
      exact hs
    linarith
  -- o t que refuta: t₀ = −‖φ(a)‖/(r+1)
  set A := ‖T.φ a‖ with hA
  have hr1 : (0 : ℝ) < r + 1 := by linarith
  set t₀ : ℝ := -(A / (r + 1)) with ht₀
  have h2 := hkey t₀
  have h3 : (2 * t₀ * A + t₀ ^ 2 * r) * (r + 1) ^ 2
      = -(A ^ 2 * (r + 2)) := by
    rw [ht₀]
    field_simp
    ring
  have h4 : 0 ≤ -(A ^ 2 * (r + 2)) := by
    rw [← h3]
    exact mul_nonneg h2 (by positivity)
  nlinarith [h4, hApos]

/-! ## F — B(ℓ²) como álgebra de von Neumann -/

/-- [KERNEL] ★★ O PRIMEIRO OBJETO DE VON NEUMANN DO PROGRAMA:
    B(ℓ²) — o bicomutante de tudo é tudo. -/
def fullAlgebra : VonNeumannAlgebra ellTwo where
  toStarSubalgebra := ⊤
  centralizer_centralizer' := by
    ext x
    constructor
    · intro _
      show x ∈ (⊤ : StarSubalgebra ℂ (ellTwo →L[ℂ] ellTwo)).carrier
      exact trivial
    · intro _ y hy
      exact (hy x trivial).symm

/-- [KERNEL] ★ a bipartição MORA na álgebra de von Neumann. -/
theorem bipartition_mem_fullAlgebra :
    evenShift ∈ (fullAlgebra : Set (ellTwo →L[ℂ] ellTwo))
      ∧ coEven ∈ (fullAlgebra : Set (ellTwo →L[ℂ] ellTwo)) := by
  constructor <;> exact trivial

end

end TGLExt
