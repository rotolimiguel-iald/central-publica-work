import TGLExt.SemifiniteWeight

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

/-!
# O PESO É TRAÇO: τ(a*a) = τ(a a*) no habitante ∞-dim
  [TGLExt — item A da ordem de fechamento: a condicional «Breuer»]

O pacote soldado cita Breuer como [KNOWN externo]. O que o pacote USA
de Breuer é, antes de tudo, que o peso semifinito da casa é um TRAÇO —
a propriedade definidora `τ(a*a) = τ(a a*)`, da qual descendem a
invariância unitária e a teoria do canto. Esta pedra a INTERNALIZA no
habitante genuinamente ∞-dim (`ellTwo`, o peso diagonal `opWeight`
com Tr(1) = ∞ e Tr(P_Nome) = 1):

* `adjoint_coord` — a coordenada do adjunto é a conjugada transposta:
  `(a† eₙ)(m) = conj((a eₘ)(n))` — a matriz infinita do adjunto;
* `diag_star_mul` / `diag_mul_star` — as diagonais de `a†a` e `a a†`
  como produtos internos das colunas;
* `ofReal_normSq_tsum` — a ponte ℓ²: `ofReal(Re⟪y,y⟫) =
  Σ'ₘ ofReal(‖yₘ‖²)` (a soma dupla nasce);
* ★★ `opWeight_star_mul_self_comm` — **O PESO É TRAÇO**:
  `opWeight (a†·a) = opWeight (a·a†)` — as duas somas duplas são a
  MESMA soma com os índices trocados (Tonelli em ℝ≥0∞: a troca é
  LIVRE — `ENNReal.tsum_comm`). Nenhuma hipótese sobre `a` além de
  ser operador limitado: o traço semifinito, no kernel.

HONESTIDADE: internaliza a PROPRIEDADE TRACIAL do peso no habitante
B(ℓ²) — o que o pacote usa; a teoria do índice de Breuer–Fredholm
GERAL (fator II_∞ abstrato, perturbações compactas) segue [KNOWN],
NOMEADA — a mathlib não tem álgebras de von Neumann semifinitas, e
construí-las é o programa. β JAMAIS entra no Lean. Sem sorry, sem
axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

/-- A coordenada do ADJUNTO é a conjugada transposta:
    `(a† eₙ)(m) = conj((a eₘ)(n))` — a matriz infinita de `a†`. -/
theorem adjoint_coord (a : ellTwo →L[ℂ] ellTwo) (n m : ℕ) :
    (((ContinuousLinearMap.adjoint a) (inscriptions n) : ℕ → ℂ)) m
      = (starRingEnd ℂ) ((a (inscriptions m) : ℕ → ℂ) n) := by
  rw [← coord_eq_inner, ContinuousLinearMap.adjoint_inner_right,
    ← coord_eq_inner]
  exact (inner_conj_symm _ _).symm

/-- A norma da coordenada do adjunto é a da coordenada trocada. -/
theorem adjoint_coord_norm (a : ellTwo →L[ℂ] ellTwo) (n m : ℕ) :
    ‖(((ContinuousLinearMap.adjoint a) (inscriptions n) : ℕ → ℂ)) m‖
      = ‖(a (inscriptions m) : ℕ → ℂ) n‖ := by
  rw [adjoint_coord]
  exact RCLike.norm_conj _

/-- A diagonal de `a†·a`: `(a†a eₙ)(n) = ⟪a eₙ, a eₙ⟫`. -/
theorem diag_star_mul (a : ellTwo →L[ℂ] ellTwo) (n : ℕ) :
    (((ContinuousLinearMap.adjoint a * a) (inscriptions n) : ℕ → ℂ)) n
      = inner ℂ (a (inscriptions n)) (a (inscriptions n)) := by
  rw [ContinuousLinearMap.mul_apply, ← coord_eq_inner,
    ContinuousLinearMap.adjoint_inner_right]

/-- A diagonal de `a·a†`: `(a a† eₙ)(n) = ⟪a† eₙ, a† eₙ⟫`. -/
theorem diag_mul_star (a : ellTwo →L[ℂ] ellTwo) (n : ℕ) :
    (((a * ContinuousLinearMap.adjoint a) (inscriptions n) : ℕ → ℂ)) n
      = inner ℂ ((ContinuousLinearMap.adjoint a) (inscriptions n))
          ((ContinuousLinearMap.adjoint a) (inscriptions n)) := by
  rw [ContinuousLinearMap.mul_apply, ← coord_eq_inner,
    ← ContinuousLinearMap.adjoint_inner_left]

/-- A PONTE ℓ²: `ofReal(Re⟪y,y⟫) = Σ'ₘ ofReal(‖yₘ‖²)` — a soma dupla
    nasce da definição do produto interno de `lp 2`. -/
theorem ofReal_normSq_tsum (y : ellTwo) :
    ENNReal.ofReal ((inner ℂ y y).re)
      = ∑' m, ENNReal.ofReal (‖(y : ℕ → ℂ) m‖ ^ 2) := by
  have hsum : Summable fun m => inner ℂ ((y : ℕ → ℂ) m) ((y : ℕ → ℂ) m) :=
    lp.summable_inner y y
  have hinner : inner ℂ y y
      = ∑' m, inner ℂ ((y : ℕ → ℂ) m) ((y : ℕ → ℂ) m) := lp.inner_eq_tsum y y
  have hterm : ∀ m, inner ℂ ((y : ℕ → ℂ) m) ((y : ℕ → ℂ) m)
      = ((‖(y : ℕ → ℂ) m‖ ^ 2 : ℝ) : ℂ) := by
    intro m
    rw [RCLike.inner_apply, RCLike.mul_conj]
    norm_cast
  have hsumC : Summable fun m => ((‖(y : ℕ → ℂ) m‖ ^ 2 : ℝ) : ℂ) :=
    hsum.congr hterm
  have hsumR : Summable fun m => (‖(y : ℕ → ℂ) m‖ ^ 2 : ℝ) :=
    Complex.summable_ofReal.mp hsumC
  have hmap := (hsumR.hasSum.mapL Complex.ofRealCLM).tsum_eq
  simp only [Complex.ofRealCLM_apply] at hmap
  have hre : (inner ℂ y y).re = ∑' m, ‖(y : ℕ → ℂ) m‖ ^ 2 := by
    rw [hinner, tsum_congr hterm, hmap, Complex.ofReal_re]
  rw [hre]
  exact ENNReal.ofReal_tsum_of_nonneg (fun m => sq_nonneg _) hsumR

/-- ★★ O PESO É TRAÇO: `τ(a*a) = τ(a a*)` — a propriedade definidora
    do traço semifinito, no habitante genuinamente ∞-dim. As duas
    somas duplas são a mesma com os índices trocados; em ℝ≥0∞ a troca
    é LIVRE (Tonelli). É o que o Breuer do pacote USA — internalizado. -/
theorem opWeight_star_mul_self_comm (a : ellTwo →L[ℂ] ellTwo) :
    opWeight (ContinuousLinearMap.adjoint a * a)
      = opWeight (a * ContinuousLinearMap.adjoint a) := by
  have hL : opWeight (ContinuousLinearMap.adjoint a * a)
      = ∑' n, ∑' m, ENNReal.ofReal (‖(a (inscriptions n) : ℕ → ℂ) m‖ ^ 2) := by
    unfold opWeight
    refine tsum_congr fun n => ?_
    rw [diag_star_mul]
    exact ofReal_normSq_tsum (a (inscriptions n))
  have hR : opWeight (a * ContinuousLinearMap.adjoint a)
      = ∑' n, ∑' m, ENNReal.ofReal
          (‖(a (inscriptions m) : ℕ → ℂ) n‖ ^ 2) := by
    unfold opWeight
    refine tsum_congr fun n => ?_
    rw [diag_mul_star]
    rw [ofReal_normSq_tsum ((ContinuousLinearMap.adjoint a) (inscriptions n))]
    exact tsum_congr fun m => by rw [adjoint_coord_norm]
  rw [hL, hR]
  exact ENNReal.tsum_comm

end

end TGLExt
