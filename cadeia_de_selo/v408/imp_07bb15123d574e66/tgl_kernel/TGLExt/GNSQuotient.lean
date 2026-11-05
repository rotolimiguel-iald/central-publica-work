import TGLExt.SecondCone

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# O QUOCIENTE GNS: o pré-fator REPRESENTADO — o radical é um ideal à esquerda
  [TGLExt — v128, o incremento 50 do programa SemifiniteAnalysis]

A v127 deu o pré-Hilbert isométrico. O FECHO pede o quociente pelo
núcleo e a ação que desce. Esta pedra faz o passo ALGÉBRICO exato —
sem Cauchy–Schwarz, sem completamento:

* `gnsInner_conj_symm` — a forma é HERMITIANA: ⟨a,b⟩ = conj⟨b,a⟩
  (via ρ auto-adjunta e a ciclicidade do traço);
* `gnsInner_smul_left`/`add_left` — conjugada-linear à esquerda;
* ★★ `gnsRadical` — o RADICAL N = {a : ∀b, ⟨a,b⟩ = 0} como Submodule ℂ;
* ★★★ `gnsRadical_left_ideal` — N É UM IDEAL À ESQUERDA: a ∈ N ⟹
  x·a ∈ N (⟨x a, b⟩ = ⟨a, x† b⟩ = 0) — a condição EXATA para a álgebra
  agir no quociente;
* ★★★ `gnsInner_wd_left`/`gnsInner_wd_right` — o produto interno DESCE
  ao quociente M/N (independe do representante nas duas faces);
* ★★★ `leftAction_wd` — a ação esquerda x·[a] = [x·a] DESCE ao
  quociente (bem-definida pelo ideal) — O PRÉ-FATOR REPRESENTADO.

O QUE RESTA (nomeado, sem véu): o completamento de Hilbert de M/N e o
fecho fraco-* da álgebra representada — o fator de von Neumann como
objeto topológico. A representação algébrica (GNS finito) está fechada;
o completamento é o programa.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Kronecker Matrix
open scoped ComplexConjugate

noncomputable section

variable {l : ℝ} {N : ℕ}

/-! ## A — a forma é hermitiana e conjugada-linear -/

/-- [KERNEL] a densidade da torre é auto-adjunta (diagonal real). -/
theorem chainDensity_selfadjoint (l : ℝ) (N : ℕ) :
    (chainDensity l N)ᴴ = chainDensity l N := by
  rw [chainDensity_eq_diagonal l N]
  rw [diagonal_conjTranspose]
  congr 1
  funext i
  rw [Pi.star_apply, Complex.star_def, Complex.conj_ofReal]

/-- [KERNEL] ★ A FORMA É HERMITIANA: ⟨a,b⟩ = conj⟨b,a⟩. -/
theorem gnsInner_conj_symm (l : ℝ) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    gnsInner l N a b = conj (gnsInner l N b a) := by
  unfold gnsInner chainState
  rw [show conj ((chainDensity l N * (bᴴ * a)).trace)
      = star ((chainDensity l N * (bᴴ * a)).trace) from rfl]
  rw [← trace_conjTranspose]
  rw [conjTranspose_mul, conjTranspose_mul, conjTranspose_conjTranspose,
    chainDensity_selfadjoint]
  exact trace_mul_comm (chainDensity l N) (aᴴ * b)

/-- [KERNEL] ★ conjugada-linear à esquerda (soma). -/
theorem gnsInner_add_left (l : ℝ) (N : ℕ)
    (a b c : Matrix (chainIdx N) (chainIdx N) ℂ) :
    gnsInner l N (a + b) c = gnsInner l N a c + gnsInner l N b c := by
  unfold gnsInner chainState
  rw [conjTranspose_add, add_mul, mul_add, trace_add]

/-- [KERNEL] ★ conjugada-linear à esquerda (escalar). -/
theorem gnsInner_smul_left (l : ℝ) (N : ℕ) (c : ℂ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    gnsInner l N (c • a) b = conj c * gnsInner l N a b := by
  unfold gnsInner chainState
  rw [conjTranspose_smul, smul_mul_assoc, mul_smul_comm, trace_smul]
  rw [Complex.star_def, smul_eq_mul]

/-! ## B — o radical como ideal à esquerda -/

/-- ★★ O RADICAL GNS: N = {a : ∀ b, ⟨a,b⟩ = 0} — o núcleo à esquerda
    da forma, como submódulo ℂ. -/
def gnsRadical (l : ℝ) (N : ℕ) :
    Submodule ℂ (Matrix (chainIdx N) (chainIdx N) ℂ) where
  carrier := {a | ∀ b, gnsInner l N a b = 0}
  zero_mem' := by
    intro b
    unfold gnsInner chainState
    rw [conjTranspose_zero, zero_mul, mul_zero, trace_zero]
  add_mem' := by
    intro a b ha hb c
    rw [gnsInner_add_left, ha c, hb c, add_zero]
  smul_mem' := by
    intro c a ha b
    rw [gnsInner_smul_left, ha b, mul_zero]

theorem mem_gnsRadical (l : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    a ∈ gnsRadical l N ↔ ∀ b, gnsInner l N a b = 0 := Iff.rfl

/-- [KERNEL] ★ a chave: ⟨x·a, b⟩ = ⟨a, x†·b⟩. -/
theorem gnsInner_mul_left_adjoint (l : ℝ) (N : ℕ)
    (x a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    gnsInner l N (x * a) b = gnsInner l N a (xᴴ * b) := by
  unfold gnsInner chainState
  rw [conjTranspose_mul, mul_assoc, ← mul_assoc aᴴ]

/-- [KERNEL] ★★★ O RADICAL É UM IDEAL À ESQUERDA: a ∈ N ⟹ x·a ∈ N —
    a condição EXATA para a álgebra agir no quociente. -/
theorem gnsRadical_left_ideal (l : ℝ) (N : ℕ)
    {a : Matrix (chainIdx N) (chainIdx N) ℂ} (ha : a ∈ gnsRadical l N)
    (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    x * a ∈ gnsRadical l N := by
  intro b
  rw [gnsInner_mul_left_adjoint]
  exact ha (xᴴ * b)

/-! ## C — o produto interno e a ação DESCEM ao quociente -/

/-- [KERNEL] ★★★ o produto interno DESCE (face esquerda): se a − a' ∈ N
    então ⟨a,b⟩ = ⟨a',b⟩. -/
theorem gnsInner_wd_left (l : ℝ) (N : ℕ)
    {a a' : Matrix (chainIdx N) (chainIdx N) ℂ}
    (h : a - a' ∈ gnsRadical l N) (b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    gnsInner l N a b = gnsInner l N a' b := by
  have hz : gnsInner l N (a - a') b = 0 := h b
  rw [sub_eq_add_neg, gnsInner_add_left] at hz
  have hneg : gnsInner l N (-a') b = - gnsInner l N a' b := by
    rw [show (-a') = (-1 : ℂ) • a' by rw [neg_one_smul], gnsInner_smul_left]
    simp
  rw [hneg] at hz
  linear_combination (norm := module) hz

/-- [KERNEL] ★★★ o produto interno DESCE (face direita): usa a
    hermiticidade. -/
theorem gnsInner_wd_right (l : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    {b b' : Matrix (chainIdx N) (chainIdx N) ℂ}
    (h : b - b' ∈ gnsRadical l N) :
    gnsInner l N a b = gnsInner l N a b' := by
  rw [gnsInner_conj_symm l N a b, gnsInner_conj_symm l N a b']
  congr 1
  exact gnsInner_wd_left l N h a

/-- [KERNEL] ★★★ A AÇÃO ESQUERDA DESCE: se a − a' ∈ N então
    x·a − x·a' ∈ N — a ação x·[a] = [x·a] é bem-definida no quociente.
    O PRÉ-FATOR REPRESENTADO. -/
theorem leftAction_wd (l : ℝ) (N : ℕ)
    (x : Matrix (chainIdx N) (chainIdx N) ℂ)
    {a a' : Matrix (chainIdx N) (chainIdx N) ℂ}
    (h : a - a' ∈ gnsRadical l N) :
    x * a - x * a' ∈ gnsRadical l N := by
  rw [← mul_sub]
  exact gnsRadical_left_ideal l N h x

end

end TGLExt
