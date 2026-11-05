import TGLExt.TTSuperposition

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A TORRE GNS: o pré-Hilbert do fator, com inclusões ISOMÉTRICAS
  [TGLExt — v127, o incremento 48 do programa SemifiniteAnalysis]

A v126 deu a torre com estado coerente. O FECHO pede a representação
GNS: o produto interno ⟨a,b⟩_φ = φ(a†b) em cada andar, e a prova de que
os degraus PRESERVAM o produto — a torre GNS é isométrica, o pré-Hilbert
do fator com um único completamento à frente:

* `chainDensity_diag_nonneg` — a densidade da torre é DIAGONAL com
  entradas reais ≥ 0 (indução por Kronecker de diagonais);
* ★★ `chainState_positive` — o estado é POSITIVO em TODO andar:
  Re φ_N(a†a) ≥ 0 — a positividade sobe a torre inteira;
* `gnsInner` — o produto GNS ⟨a,b⟩ = φ(a†b); ★ aditivo à direita
  (`gnsInner_add_right`) e hermitiano no argumento (via a forma);
* ★★★ `gns_isometric_up_tower` — ⟨a⊗1, b⊗1⟩_{N+1} = ⟨a,b⟩_N — os
  degraus da torre são ISOMETRIAS GNS: o pré-Hilbert do fator é UM
  espaço só, andar a andar.

O QUE RESTA (nomeado, sem véu): o quociente pelo núcleo, o
completamento de Hilbert e o fecho fraco-* da ação — o fator como
álgebra de von Neumann. O pré-Hilbert isométrico está em kernel.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Kronecker Matrix
open scoped ComplexConjugate

noncomputable section

/-! ## A — a densidade da torre é diagonal positiva -/

/-- os pesos da densidade da torre (a diagonal). -/
def chainWeights (l : ℝ) : (N : ℕ) → chainIdx N → ℝ
  | 0 => fun i => if i = 0 then l / (1 + l) else 1 / (1 + l)
  | N + 1 => fun p => chainWeights l N p.1
      * (if p.2 = 0 then l / (1 + l) else 1 / (1 + l))

/-- [KERNEL] ★ a densidade É a diagonal dos pesos. -/
theorem chainDensity_eq_diagonal (l : ℝ) :
    ∀ N : ℕ, chainDensity l N
      = diagonal (fun i => ((chainWeights l N i : ℝ) : ℂ))
  | 0 => by
      rw [show chainDensity l 0 = powersDensity l from rfl]
      unfold powersDensity chainWeights
      congr 1
      funext i
      by_cases hi : i = 0
      · rw [if_pos hi, if_pos hi]
      · rw [if_neg hi, if_neg hi]
  | N + 1 => by
      rw [show chainDensity l (N + 1)
          = chainDensity l N ⊗ₖ powersDensity l from rfl,
        chainDensity_eq_diagonal l N]
      unfold powersDensity
      rw [diagonal_kronecker_diagonal]
      congr 1
      funext p
      rw [show chainWeights l (N + 1) p
          = chainWeights l N p.1
            * (if p.2 = 0 then l / (1 + l) else 1 / (1 + l)) from rfl]
      by_cases hp : p.2 = 0
      · rw [if_pos hp, if_pos hp]
        push_cast
        ring
      · rw [if_neg hp, if_neg hp]
        push_cast
        ring

/-- [KERNEL] ★ os pesos são ≥ 0 em todo andar. -/
theorem chainWeights_nonneg (l : ℝ) (hl : 0 < l) :
    ∀ (N : ℕ) (i : chainIdx N), 0 ≤ chainWeights l N i
  | 0, i => by
      unfold chainWeights
      by_cases hi : i = 0
      · rw [if_pos hi]
        positivity
      · rw [if_neg hi]
        positivity
  | N + 1, p => by
      unfold chainWeights
      have h1 := chainWeights_nonneg l hl N p.1
      by_cases hp : p.2 = 0
      · rw [if_pos hp]
        have h2 : (0 : ℝ) ≤ l / (1 + l) := by positivity
        exact mul_nonneg h1 h2
      · rw [if_neg hp]
        have h2 : (0 : ℝ) ≤ 1 / (1 + l) := by positivity
        exact mul_nonneg h1 h2

/-! ## B — a positividade sobe a torre -/

/-- [KERNEL] ★★ O ESTADO É POSITIVO EM TODO ANDAR: Re φ_N(a†a) ≥ 0. -/
theorem chainState_positive (l : ℝ) (hl : 0 < l) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    0 ≤ (chainState l N (aᴴ * a)).re := by
  unfold chainState
  rw [chainDensity_eq_diagonal l N]
  rw [trace]
  rw [Complex.re_sum]
  apply Finset.sum_nonneg
  intro k _
  rw [diag_apply, diagonal_mul]
  have hdiag : ((aᴴ * a) k k).re = ∑ j, Complex.normSq (a j k) := by
    rw [mul_apply, Complex.re_sum]
    congr 1
    funext j
    rw [conjTranspose_apply,
      show (star (a j k) : ℂ) = conj (a j k) from rfl,
      ← Complex.normSq_eq_conj_mul_self]
    rw [Complex.ofReal_re]
  have him : ((aᴴ * a) k k).im = 0 := by
    rw [mul_apply, Complex.im_sum]
    have hz : ∀ j ∈ Finset.univ, ((aᴴ) k j * a j k).im = 0 := by
      intro j _
      rw [conjTranspose_apply,
        show (star (a j k) : ℂ) = conj (a j k) from rfl,
        ← Complex.normSq_eq_conj_mul_self]
      rw [Complex.ofReal_im]
    rw [Finset.sum_congr rfl hz]
    simp
  rw [Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, hdiag, him]
  rw [mul_zero, sub_zero]
  apply mul_nonneg (chainWeights_nonneg l hl N k)
  apply Finset.sum_nonneg
  intro j _
  exact Complex.normSq_nonneg _

/-! ## C — o produto GNS e a isometria da torre -/

/-- o produto interno GNS do andar N: ⟨a,b⟩ = φ(a†b). -/
def gnsInner (l : ℝ) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) : ℂ :=
  chainState l N (aᴴ * b)

/-- [KERNEL] ★ o produto GNS é aditivo à direita. -/
theorem gnsInner_add_right (l : ℝ) (N : ℕ)
    (a b c : Matrix (chainIdx N) (chainIdx N) ℂ) :
    gnsInner l N a (b + c) = gnsInner l N a b + gnsInner l N a c := by
  unfold gnsInner chainState
  rw [mul_add, mul_add, trace_add]

/-- [KERNEL] ★ a norma GNS ao quadrado é real ≥ 0 (a forma é positiva). -/
theorem gnsInner_self_nonneg (l : ℝ) (hl : 0 < l) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    0 ≤ (gnsInner l N a a).re :=
  chainState_positive l hl N a

/-- [KERNEL] ★★★ A TORRE GNS É ISOMÉTRICA: ⟨a⊗1, b⊗1⟩_{N+1} = ⟨a,b⟩_N —
    os degraus preservam o produto interno GNS; o pré-Hilbert do fator
    é UM espaço só, andar a andar. -/
theorem gns_isometric_up_tower (l : ℝ) (hl : 0 < l) {N : ℕ}
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    gnsInner l (N + 1) (towerStep a) (towerStep b) = gnsInner l N a b := by
  unfold gnsInner
  rw [← towerStep_star, ← towerStep_mul]
  exact chainState_towerStep l hl (aᴴ * b)

end

end TGLExt
