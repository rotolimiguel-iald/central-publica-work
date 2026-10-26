import TGLExt.ContinuumTT

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A TORRE DO FATOR: o colimite ITPFI começa — o objeto, não mais a assinatura
  [TGLExt — v126, o incremento 46 do programa SemifiniteAnalysis]

A v124 construiu a escada; a v125 provou a marca de III₁. O que resta é
O OBJETO: o fator ITPFI — o limite da torre M₂ ⊂ M₄ ⊂ M₈ ⊂ … com o
estado-produto. Esta pedra constrói a TORRE INTEIRA e prova que ela é
um sistema dirigido de *-álgebras com estado COERENTE:

* `towerStep` — o degrau a ↦ a ⊗ₖ 1: *-homomorfismo UNITAL e INJETIVO
  (`towerStep_mul`, `towerStep_star`, `towerStep_one`,
  `towerStep_injective`) — a inclusão M_{2^N} ↪ M_{2^{N+1}};
* `chainState` — o estado-produto em cada andar;
  ★★★ `chainState_towerStep` — A COERÊNCIA: φ_{N+1}(a⊗1) = φ_N(a) —
  o estado-produto é UM SÓ estado na torre inteira (a condição exata
  da construção de Araki–Woods);
* ★★ `ratio_persists_up_tower` — A ASSIMETRIA SOBE INALTERADA: toda
  testemunha de razão r no andar N persiste com a MESMA razão r em
  todos os andares acima — o dado modular é estável no colimite.

O QUE RESTA (nomeado, sem véu): o FECHO — completar a torre na
representação GNS do estado coerente e tomar o fecho fraco-* (o fator
de von Neumann). A torre, o estado e a estabilidade modular estão em
kernel; o fecho é o programa.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Kronecker Matrix

noncomputable section

/-! ## A — o degrau da torre: *-homomorfismo unital injetivo -/

/-- o degrau: a ↦ a ⊗ₖ 1 (a inclusão M_{2^N} ↪ M_{2^{N+1}}). -/
def towerStep {N : ℕ} (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Matrix (chainIdx (N + 1)) (chainIdx (N + 1)) ℂ :=
  a ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ)

/-- [KERNEL] ★ o degrau é UNITAL. -/
theorem towerStep_one (N : ℕ) :
    towerStep (1 : Matrix (chainIdx N) (chainIdx N) ℂ) = 1 := by
  unfold towerStep
  exact one_kronecker_one

/-- [KERNEL] ★★ o degrau é MULTIPLICATIVO: a torre é de álgebras. -/
theorem towerStep_mul {N : ℕ}
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerStep (a * b) = towerStep a * towerStep b := by
  unfold towerStep
  rw [show (1 : Matrix (Fin 2) (Fin 2) ℂ) = 1 * 1 by rw [one_mul]]
  rw [mul_kronecker_mul]
  rw [one_mul]

/-- [KERNEL] ★★ o degrau respeita a ESTRELA: *-homomorfismo. -/
theorem towerStep_star {N : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerStep aᴴ = (towerStep a)ᴴ := by
  unfold towerStep
  rw [conjTranspose_kronecker]
  rw [conjTranspose_one]

/-- [KERNEL] ★★ o degrau é INJETIVO: nada se perde subindo a torre. -/
theorem towerStep_injective (N : ℕ) :
    Function.Injective (towerStep (N := N)) := by
  intro a b h
  ext i j
  have h2 := congrFun (congrFun h (i, 0)) (j, 0)
  unfold towerStep at h2
  rw [kronecker_apply, kronecker_apply, one_apply_eq] at h2
  rw [mul_one, mul_one] at h2
  exact h2

/-! ## B — o estado coerente da torre -/

/-- o estado-produto no andar N da torre. -/
def chainState (l : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : ℂ :=
  trace (chainDensity l N * a)

/-- [KERNEL] ★★★ A COERÊNCIA: φ_{N+1}(a ⊗ 1) = φ_N(a) — o estado-produto
    é UM SÓ estado na torre inteira (a condição de Araki–Woods). -/
theorem chainState_towerStep (l : ℝ) (hl : 0 < l) {N : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    chainState l (N + 1) (towerStep a) = chainState l N a := by
  unfold chainState towerStep
  rw [show chainDensity l (N + 1)
      = chainDensity l N ⊗ₖ powersDensity l from rfl]
  rw [← mul_kronecker_mul, trace_kronecker]
  have h1 : trace (powersDensity l * 1) = 1 := by
    rw [mul_one]
    have h2 := powersState_one l hl
    rw [powersState_apply] at h2
    unfold powersDensity
    rw [trace, Fin.sum_univ_two, diag_apply, diag_apply,
      diagonal_apply_eq, diagonal_apply_eq,
      if_pos (rfl : (0 : Fin 2) = 0),
      if_neg (show ¬(1 : Fin 2) = 0 by decide)]
    rw [one_apply_eq, one_apply_eq, mul_one, mul_one] at h2
    exact h2
  rw [h1, mul_one]

/-- [KERNEL] ★ o estado da torre é normalizado em TODO andar. -/
theorem chainState_one (l : ℝ) (hl : 0 < l) :
    ∀ N : ℕ, chainState l N (1 : Matrix (chainIdx N) (chainIdx N) ℂ) = 1
  | 0 => by
      unfold chainState
      have h2 := powersState_one l hl
      unfold powersState at h2
      exact h2
  | N + 1 => by
      have h := chainState_towerStep l hl
        (1 : Matrix (chainIdx N) (chainIdx N) ℂ)
      rw [towerStep_one] at h
      rw [h]
      exact chainState_one l hl N

/-! ## C — a assimetria sobe a torre inalterada -/

/-- [KERNEL] ★ a testemunha TRIVIAL no bloco novo: razão 1 em (1,1). -/
theorem trivial_ratio_witness {n : Type} [Fintype n] [DecidableEq n]
    (ρ : Matrix n n ℂ) :
    RatioWitness ρ (1 : Matrix n n ℂ) (1 : Matrix n n ℂ) 1 := by
  unfold RatioWitness
  rw [Complex.ofReal_one, one_mul, one_mul]

/-- [KERNEL] ★★ A ASSIMETRIA SOBE A TORRE INALTERADA: toda testemunha de
    razão r no andar N persiste com a MESMA razão no andar N+1 — o dado
    modular é ESTÁVEL no colimite. -/
theorem ratio_persists_up_tower (l : ℝ) {N : ℕ}
    {ρ a b : Matrix (chainIdx N) (chainIdx N) ℂ} {r : ℝ}
    (h : RatioWitness ρ a b r) :
    RatioWitness (ρ ⊗ₖ powersDensity l) (towerStep a) (towerStep b) r := by
  have h2 := ratioWitness_kron h (trivial_ratio_witness (powersDensity l))
  rw [mul_one] at h2
  exact h2

end

end TGLExt
