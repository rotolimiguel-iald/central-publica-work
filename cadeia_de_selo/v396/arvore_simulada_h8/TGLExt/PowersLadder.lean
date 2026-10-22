import TGLExt.FusedWitness
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.Data.Matrix.Basis

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A ESCADA DE POWERS: a semente de Araki–Woods — o terceiro assassino de traço
  [TGLExt — v124, o incremento 43 do programa SemifiniteAnalysis]

III₁ é a última parede formal da testemunha. Sua forma exata está nomeada
desde o v119: Araki–Woods — produtos tensoriais infinitos com estados-
produto. Esta pedra constrói a FACE FINITA COMPLETA dessa construção:

* ★★ `block_modular_identity` — TOMITA NO BLOCO: φ_ρ(ab) = φ_ρ(b·ρaρ⁻¹)
  para TODA densidade invertível, por ciclicidade do traço — a identidade
  modular (KMS em tempo imaginário) na face de matriz;
* `powersState` — o estado de Powers φ_λ no bloco 2×2 (normalizado,
  positivo);
* ★★ `powers_ratio_witness` — A TESTEMUNHA DE RAZÃO: φ_λ(E₀₁E₁₀) =
  λ·φ_λ(E₁₀E₀₁) — a assimetria λ que mata a tracialidade
  (`powersState_not_tracial`: λ ≠ 1 ⟹ φ_λ NÃO é traço);
* ★ `blockFlow_eigen` — o FLUXO do bloco σ(a) = ρaρ⁻¹ tem E₀₁ como
  autovetor de autovalor λ — o espectro modular do bloco;
* ★★★ `ratioWitness_kron` + `powers_ladder` — A LEI DA ESCADA: testemunhas
  de razão COMPÕEM por produto de Kronecker (r₁·r₂); a cadeia de N blocos
  carrega a razão λ^N — a assimetria AMPLIFICA exponencialmente;
* ★★★ `zero_mem_closure_ratio_spectrum` — A MARCA DE III: 0 pertence ao
  FECHO do espectro de razões {λ^N} — a semente da S-invariante de Connes
  tocando o zero; e `no_trace_floor` — NENHUM piso tracial sobrevive à
  escada: para todo c > 0 existe N com λ^N < c. O terceiro assassino de
  traço (v45: o fluxo; v119: a álgebra; v124: o FLUXO-PRODUTO na escada).

O QUE RESTA (nomeado, sem véu): o FATOR infinito (ITPFI R_λ; III_λ; III₁
por mistura) — o limite indutivo da escada com o estado-produto. A escada
está construída e a lei de composição provada; o limite é o programa.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Kronecker Matrix
open scoped ComplexConjugate

noncomputable section

/-! ## A — Tomita no bloco: a identidade modular por ciclicidade -/

/-- [KERNEL] ★★ A IDENTIDADE MODULAR NO BLOCO: φ_ρ(ab) = φ_ρ(b·σ(a)) com
    σ(a) = ρaρ⁻¹ — Tomita na face de matriz, por ciclicidade do traço. -/
theorem block_modular_identity {n : Type} [Fintype n] [DecidableEq n]
    (ρ a b : Matrix n n ℂ) [Invertible ρ] :
    trace (ρ * (a * b)) = trace (ρ * (b * (ρ * a * ⅟ρ))) := by
  have h1 : trace (ρ * (a * b)) = trace (b * (ρ * a)) := by
    rw [← mul_assoc]
    exact trace_mul_comm (ρ * a) b
  have h2 : trace (ρ * (b * (ρ * a * ⅟ρ))) = trace (b * (ρ * a)) := by
    have e1 : ρ * (b * (ρ * a * ⅟ρ)) = (ρ * (b * (ρ * a))) * ⅟ρ := by
      simp only [mul_assoc]
    rw [e1, trace_mul_comm, ← mul_assoc, invOf_mul_self, one_mul]
  rw [h1, ← h2]

/-! ## B — o estado de Powers no bloco 2×2 -/

/-- a densidade de Powers: pesos λ/(1+λ) e 1/(1+λ). -/
def powersDensity (l : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  diagonal fun i =>
    if i = 0 then ((l / (1 + l) : ℝ) : ℂ) else ((1 / (1 + l) : ℝ) : ℂ)

/-- o estado de Powers: φ_λ(a) = Tr(ρ_λ a). -/
def powersState (l : ℝ) (a : Matrix (Fin 2) (Fin 2) ℂ) : ℂ :=
  trace (powersDensity l * a)

theorem powersState_apply (l : ℝ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    powersState l a
      = ((l / (1 + l) : ℝ) : ℂ) * a 0 0 + ((1 / (1 + l) : ℝ) : ℂ) * a 1 1 := by
  unfold powersState powersDensity
  rw [trace, Fin.sum_univ_two, diag_apply, diag_apply, diagonal_mul,
    diagonal_mul, if_pos (rfl : (0 : Fin 2) = 0),
    if_neg (show ¬(1 : Fin 2) = 0 by decide)]

/-- [KERNEL] ★ o estado é normalizado: φ_λ(1) = 1. -/
theorem powersState_one (l : ℝ) (hl : 0 < l) : powersState l 1 = 1 := by
  rw [powersState_apply]
  have hne : (1 : ℝ) + l ≠ 0 := by positivity
  rw [one_apply_eq, one_apply_eq, mul_one, mul_one, ← Complex.ofReal_add,
    show l / (1 + l) + 1 / (1 + l) = 1 by
      field_simp
      ring]
  norm_num

/-- [KERNEL] ★ o estado é POSITIVO: φ_λ(a†a) tem parte real ≥ 0. -/
theorem powersState_positive (l : ℝ) (hl : 0 < l)
    (a : Matrix (Fin 2) (Fin 2) ℂ) :
    0 ≤ (powersState l (aᴴ * a)).re := by
  have hdiag : ∀ k : Fin 2, (aᴴ * a) k k
      = ((Complex.normSq (a 0 k) + Complex.normSq (a 1 k) : ℝ) : ℂ) := by
    intro k
    rw [mul_apply, Fin.sum_univ_two, conjTranspose_apply, conjTranspose_apply]
    rw [show (star (a 0 k) : ℂ) = conj (a 0 k) from rfl,
      show (star (a 1 k) : ℂ) = conj (a 1 k) from rfl]
    rw [← Complex.normSq_eq_conj_mul_self, ← Complex.normSq_eq_conj_mul_self]
    push_cast
    ring
  rw [powersState_apply, hdiag 0, hdiag 1]
  rw [← Complex.ofReal_mul, ← Complex.ofReal_mul, ← Complex.ofReal_add,
    Complex.ofReal_re]
  have hw0 : (0 : ℝ) ≤ l / (1 + l) := by positivity
  have hw1 : (0 : ℝ) ≤ 1 / (1 + l) := by positivity
  have hn1 : (0 : ℝ) ≤ Complex.normSq (a 0 0) := Complex.normSq_nonneg _
  have hn2 : (0 : ℝ) ≤ Complex.normSq (a 1 0) := Complex.normSq_nonneg _
  have hn3 : (0 : ℝ) ≤ Complex.normSq (a 0 1) := Complex.normSq_nonneg _
  have hn4 : (0 : ℝ) ≤ Complex.normSq (a 1 1) := Complex.normSq_nonneg _
  positivity

/-! ## C — a testemunha de razão e a morte da tracialidade -/

/-- a TESTEMUNHA DE RAZÃO: φ(ab) = r·φ(ba) — a assimetria modular medida. -/
def RatioWitness {n : Type} [Fintype n]
    (ρ a b : Matrix n n ℂ) (r : ℝ) : Prop :=
  trace (ρ * (a * b)) = (r : ℂ) * trace (ρ * (b * a))

theorem powersState_single_diag (l : ℝ) (k : Fin 2) :
    powersState l (single k k 1)
      = (if k = 0 then ((l / (1 + l) : ℝ) : ℂ)
         else ((1 / (1 + l) : ℝ) : ℂ)) := by
  rw [powersState_apply]
  by_cases hk : k = 0
  · subst hk
    rw [if_pos rfl, single_apply_same,
      single_apply_of_ne _ _ _ _ _ (by decide :
        ¬((0 : Fin 2) = 1 ∧ (0 : Fin 2) = 1)),
      mul_one, mul_zero, add_zero]
  · have hk1 : k = 1 := Fin.eq_one_of_ne_zero k hk
    subst hk1
    rw [if_neg (show ¬(1 : Fin 2) = 0 by decide), single_apply_same,
      single_apply_of_ne _ _ _ _ _ (by decide :
        ¬((1 : Fin 2) = 0 ∧ (1 : Fin 2) = 0)),
      mul_one, mul_zero, zero_add]

/-- [KERNEL] ★★ A TESTEMUNHA DE RAZÃO DO BLOCO: φ_λ(E₀₁E₁₀) = λ·φ_λ(E₁₀E₀₁)
    — a assimetria λ é o dado modular do estado de Powers. -/
theorem powers_ratio_witness (l : ℝ) (hl : 0 < l) :
    RatioWitness (powersDensity l) (single 0 1 1) (single 1 0 1) l := by
  unfold RatioWitness
  rw [single_mul_single_same, single_mul_single_same, one_mul]
  have e0 : trace (powersDensity l * single (0 : Fin 2) (0 : Fin 2) (1 : ℂ))
      = powersState l (single 0 0 1) := rfl
  have e1 : trace (powersDensity l * single (1 : Fin 2) (1 : Fin 2) (1 : ℂ))
      = powersState l (single 1 1 1) := rfl
  rw [e0, e1, powersState_single_diag, powersState_single_diag,
    if_pos (rfl : (0 : Fin 2) = 0), if_neg (show ¬(1 : Fin 2) = 0 by decide),
    ← Complex.ofReal_mul, mul_one_div]

/-- [KERNEL] ★★ λ ≠ 1 MATA A TRACIALIDADE: o estado de Powers não é traço. -/
theorem powersState_not_tracial (l : ℝ) (hl : 0 < l) (hne : l ≠ 1) :
    ∃ a b : Matrix (Fin 2) (Fin 2) ℂ,
      powersState l (a * b) ≠ powersState l (b * a) := by
  have hpos : (1 : ℝ) + l ≠ 0 := by positivity
  refine ⟨single 0 1 1, single 1 0 1, fun h => hne ?_⟩
  have hab : powersState l (single (0 : Fin 2) 1 1 * single 1 (0 : Fin 2) 1)
      = ((l / (1 + l) : ℝ) : ℂ) := by
    rw [single_mul_single_same, one_mul, powersState_single_diag,
      if_pos (rfl : (0 : Fin 2) = 0)]
  have hba : powersState l (single (1 : Fin 2) 0 1 * single 0 (1 : Fin 2) 1)
      = ((1 / (1 + l) : ℝ) : ℂ) := by
    rw [single_mul_single_same, one_mul, powersState_single_diag,
      if_neg (show ¬(1 : Fin 2) = 0 by decide)]
  rw [hab, hba] at h
  have h2 := Complex.ofReal_injective h
  field_simp at h2
  exact h2

/-! ## D — o fluxo do bloco e seu autovetor -/

theorem diagonal_mul_single_left {n : Type} [Fintype n] [DecidableEq n]
    (d : n → ℂ) (i j : n) (c : ℂ) :
    diagonal d * single i j c = single i j (d i * c) := by
  ext a b
  rw [diagonal_mul]
  by_cases h : i = a ∧ j = b
  · obtain ⟨ha, hb⟩ := h
    subst ha; subst hb
    rw [single_apply_same, single_apply_same]
  · rw [single_apply_of_ne _ _ _ _ _ h, single_apply_of_ne _ _ _ _ _ h,
      mul_zero]

theorem single_mul_diagonal_right {n : Type} [Fintype n] [DecidableEq n]
    (d : n → ℂ) (i j : n) (c : ℂ) :
    single i j c * diagonal d = single i j (c * d j) := by
  ext a b
  rw [mul_diagonal]
  by_cases h : i = a ∧ j = b
  · obtain ⟨ha, hb⟩ := h
    subst ha; subst hb
    rw [single_apply_same, single_apply_same]
  · rw [single_apply_of_ne _ _ _ _ _ h, single_apply_of_ne _ _ _ _ _ h,
      zero_mul]

/-- a inversa da densidade de Powers. -/
def powersDensityInv (l : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  diagonal fun i =>
    if i = 0 then (((1 + l) / l : ℝ) : ℂ) else ((1 + l : ℝ) : ℂ)

theorem powersDensity_mul_inv (l : ℝ) (hl : 0 < l) :
    powersDensity l * powersDensityInv l = 1 := by
  have hne : (1 : ℝ) + l ≠ 0 := by positivity
  have hlne : l ≠ 0 := ne_of_gt hl
  unfold powersDensity powersDensityInv
  rw [diagonal_mul_diagonal]
  have h : (fun i : Fin 2 =>
      (if i = 0 then ((l / (1 + l) : ℝ) : ℂ) else ((1 / (1 + l) : ℝ) : ℂ))
        * (if i = 0 then (((1 + l) / l : ℝ) : ℂ) else ((1 + l : ℝ) : ℂ)))
      = fun _ => (1 : ℂ) := by
    funext i
    by_cases hi : i = 0
    · rw [if_pos hi, if_pos hi, ← Complex.ofReal_mul,
        show l / (1 + l) * ((1 + l) / l) = 1 by field_simp]
      norm_num
    · rw [if_neg hi, if_neg hi, ← Complex.ofReal_mul,
        show 1 / (1 + l) * (1 + l) = 1 by field_simp]
      norm_num
  rw [h, diagonal_one]

/-- o fluxo do bloco: σ(a) = ρ a ρ⁻¹. -/
def blockFlow (l : ℝ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    Matrix (Fin 2) (Fin 2) ℂ :=
  powersDensity l * a * powersDensityInv l

/-- [KERNEL] ★ O AUTOVETOR DO FLUXO: σ(E₀₁) = λ·E₀₁ — o espectro modular
    do bloco carrega exatamente a razão λ. -/
theorem blockFlow_eigen (l : ℝ) (hl : 0 < l) :
    blockFlow l (single 0 1 1) = (l : ℂ) • single 0 1 1 := by
  have hne : (1 : ℝ) + l ≠ 0 := by positivity
  unfold blockFlow powersDensity powersDensityInv
  rw [diagonal_mul_single_left, single_mul_diagonal_right, smul_single]
  congr 1
  rw [if_pos (rfl : (0 : Fin 2) = 0), if_neg (show ¬(1 : Fin 2) = 0 by decide),
    mul_one, smul_eq_mul, mul_one, ← Complex.ofReal_mul,
    show l / (1 + l) * (1 + l) = l by field_simp]

/-! ## E — A LEI DA ESCADA: composição por Kronecker -/

/-- [KERNEL] ★★★ TESTEMUNHAS DE RAZÃO COMPÕEM: o produto de Kronecker
    multiplica as razões — a lei que constrói a escada. -/
theorem ratioWitness_kron {n m : Type} [Fintype n] [Fintype m]
    {ρ₁ a₁ b₁ : Matrix n n ℂ} {ρ₂ a₂ b₂ : Matrix m m ℂ} {r₁ r₂ : ℝ}
    (h₁ : RatioWitness ρ₁ a₁ b₁ r₁) (h₂ : RatioWitness ρ₂ a₂ b₂ r₂) :
    RatioWitness (ρ₁ ⊗ₖ ρ₂) (a₁ ⊗ₖ a₂) (b₁ ⊗ₖ b₂) (r₁ * r₂) := by
  unfold RatioWitness at h₁ h₂ ⊢
  rw [← mul_kronecker_mul, ← mul_kronecker_mul, ← mul_kronecker_mul,
    ← mul_kronecker_mul, trace_kronecker, trace_kronecker, h₁, h₂]
  push_cast
  ring

/-- os índices da cadeia de N+1 blocos. -/
@[reducible] def chainIdx : ℕ → Type
  | 0 => Fin 2
  | N + 1 => chainIdx N × Fin 2

instance chainIdx_fintype : ∀ N, Fintype (chainIdx N)
  | 0 => inferInstanceAs (Fintype (Fin 2))
  | (N + 1) =>
      letI := chainIdx_fintype N
      inferInstanceAs (Fintype (chainIdx N × Fin 2))

instance chainIdx_deceq : ∀ N, DecidableEq (chainIdx N)
  | 0 => inferInstanceAs (DecidableEq (Fin 2))
  | (N + 1) =>
      letI := chainIdx_deceq N
      inferInstanceAs (DecidableEq (chainIdx N × Fin 2))

/-- a densidade-produto da cadeia (o estado-produto de Araki–Woods, face finita). -/
def chainDensity (l : ℝ) : (N : ℕ) → Matrix (chainIdx N) (chainIdx N) ℂ
  | 0 => powersDensity l
  | N + 1 => chainDensity l N ⊗ₖ powersDensity l

/-- a palavra ascendente ⊗E₀₁ e a descendente ⊗E₁₀. -/
def chainUp : (N : ℕ) → Matrix (chainIdx N) (chainIdx N) ℂ
  | 0 => single 0 1 1
  | N + 1 => chainUp N ⊗ₖ single 0 1 1

def chainDown : (N : ℕ) → Matrix (chainIdx N) (chainIdx N) ℂ
  | 0 => single 1 0 1
  | N + 1 => chainDown N ⊗ₖ single 1 0 1

/-- [KERNEL] ★★★ A ESCADA DE POWERS: a cadeia de N+1 blocos carrega a
    testemunha de razão λ^(N+1) — a assimetria modular AMPLIFICA
    exponencialmente com o comprimento da cadeia. -/
theorem powers_ladder (l : ℝ) (hl : 0 < l) :
    ∀ N : ℕ, RatioWitness (chainDensity l N) (chainUp N) (chainDown N)
      (l ^ (N + 1))
  | 0 => by
      have h := powers_ratio_witness l hl
      rw [zero_add, pow_one]
      exact h
  | N + 1 => by
      have h := ratioWitness_kron (powers_ladder l hl N) (powers_ratio_witness l hl)
      rw [← pow_succ] at h
      exact h

/-! ## F — a morte assintótica: a marca de III -/

/-- [KERNEL] ★★ a escada de razões MORRE: λ^N → 0 para λ ∈ (0,1). -/
theorem ratio_ladder_dies (l : ℝ) (hl0 : 0 ≤ l) (hl1 : l < 1) :
    Filter.Tendsto (fun N : ℕ => l ^ N) Filter.atTop (nhds 0) :=
  tendsto_pow_atTop_nhds_zero_of_lt_one hl0 hl1

/-- [KERNEL] ★★★ A MARCA DE III: 0 pertence ao FECHO do espectro de razões
    {λ^N} — a semente da S-invariante de Connes toca o zero. -/
theorem zero_mem_closure_ratio_spectrum (l : ℝ) (hl0 : 0 ≤ l) (hl1 : l < 1) :
    (0 : ℝ) ∈ closure (Set.range fun N : ℕ => l ^ N) :=
  mem_closure_of_tendsto (ratio_ladder_dies l hl0 hl1)
    (Filter.Eventually.of_forall fun N => Set.mem_range_self N)

/-- [KERNEL] ★★ NENHUM PISO TRACIAL SOBREVIVE À ESCADA: para todo c > 0
    existe um comprimento N com razão λ^N < c — o terceiro assassino de
    traço (o FLUXO-PRODUTO), na face finita. -/
theorem no_trace_floor (l : ℝ) (hl1 : l < 1) (c : ℝ) (hc : 0 < c) :
    ∃ N : ℕ, l ^ N < c :=
  exists_pow_lt_of_lt_one hc hl1

end

end TGLExt
