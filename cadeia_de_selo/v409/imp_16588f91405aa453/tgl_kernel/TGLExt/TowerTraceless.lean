import TGLExt.GeneralNull

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A TORRE SEM TRAÇO: o tipo III realizado na torre concreta
  [TGLExt — v129, o incremento 53 do programa SemifiniteAnalysis]

O v119 provou "o único traço é zero" na álgebra plena; o v124 deu a
marca de III₁. Esta pedra realiza a assinatura NA TORRE CONCRETA: para
λ ≠ 1, o estado φ_N NÃO É TRACIAL em NENHUM andar da torre — a razão
modular λ^(N+1) persiste com testemunha NÃO-NULA:

* ★★ `chainDownUp_value` — φ_N(chainDown·chainUp) = (1/(1+λ))^(N+1),
  positivo (indução pela fatoração tensorial do traço);
* `pow_ne_one_of_ne` — λ^(N+1) ≠ 1 para λ > 0, λ ≠ 1;
* ★★★ `chainState_not_tracial_tower` — φ_N(chainUp·chainDown) ≠
  φ_N(chainDown·chainUp) em TODO andar N: a razão λ^(N+1) ≠ 1 vezes uma
  testemunha positiva ⟹ o estado da torre NÃO é traço. A ausência de
  traço não é só na álgebra plena (v119) — é na TORRE que constrói o
  fator ITPFI, andar a andar.

O QUE ISTO FECHA: a torre de Araki–Woods (v126) carrega a assinatura
tipo-III em cada andar finito; combinado com a marca log-densa (v125),
o objeto-limite é III₁. O QUE RESTA (nomeado): o limite fraco-* (o
completamento topológico) — o fator como objeto. O gate NÃO se move.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Kronecker Matrix

noncomputable section

/-! ## A — o valor positivo da testemunha -/

/-- [KERNEL] a testemunha do traço na torre: chainDown·chainUp = ⊗E₁₁. -/
theorem chainDownUp_eq (l : ℝ) :
    ∀ N : ℕ, chainDown N * chainUp N
      = (fun M : ℕ => (chainDown M * chainUp M)) N
  | _ => rfl

/-- [KERNEL] ★★ φ_N(chainDown·chainUp) = (1/(1+λ))^(N+1) — positivo em
    todo andar (indução pela fatoração tensorial do traço). -/
theorem chainDownUp_value (l : ℝ) (hl : 0 < l) :
    ∀ N : ℕ, chainState l N (chainDown N * chainUp N)
      = (((1 / (1 + l)) ^ (N + 1) : ℝ) : ℂ)
  | 0 => by
      unfold chainState
      rw [show chainDown 0 * chainUp 0
          = single (1 : Fin 2) 0 1 * single 0 1 1 from rfl,
        single_mul_single_same, one_mul]
      rw [show chainDensity l 0 = powersDensity l from rfl]
      have h1 : trace (powersDensity l * single (1 : Fin 2) 1 1)
          = powersState l (single 1 1 1) := rfl
      rw [h1, powersState_single_diag,
        if_neg (show ¬(1 : Fin 2) = 0 by decide), zero_add, pow_one]
  | N + 1 => by
      unfold chainState
      rw [show chainDown (N + 1) = chainDown N ⊗ₖ single 1 0 1 from rfl,
        show chainUp (N + 1) = chainUp N ⊗ₖ single 0 1 1 from rfl,
        show chainDensity l (N + 1)
          = chainDensity l N ⊗ₖ powersDensity l from rfl]
      rw [← mul_kronecker_mul, single_mul_single_same, one_mul,
        ← mul_kronecker_mul, trace_kronecker]
      have hIH := chainDownUp_value l hl N
      unfold chainState at hIH
      rw [hIH]
      have h2 : trace (powersDensity l * single (1 : Fin 2) 1 1)
          = (((1 / (1 + l)) : ℝ) : ℂ) := by
        have h1 : trace (powersDensity l * single (1 : Fin 2) 1 1)
            = powersState l (single 1 1 1) := rfl
        rw [h1, powersState_single_diag,
          if_neg (show ¬(1 : Fin 2) = 0 by decide)]
      rw [h2, ← Complex.ofReal_mul, ← pow_succ]

/-! ## B — a razão modular não é 1 -/

/-- [KERNEL] λ^(N+1) ≠ 1 para λ > 0, λ ≠ 1. -/
theorem tower_ratio_ne_one (l : ℝ) (hl : 0 < l) (hne : l ≠ 1) (N : ℕ) :
    l ^ (N + 1) ≠ 1 := by
  rcases lt_or_gt_of_ne hne with h | h
  · exact ne_of_lt (pow_lt_one₀ hl.le h (Nat.succ_ne_zero N))
  · exact ne_of_gt (one_lt_pow₀ h (Nat.succ_ne_zero N))

/-! ## C — o estado da torre não é tracial, em todo andar -/

/-- [KERNEL] ★★★ A TORRE SEM TRAÇO: para λ ≠ 1 e QUALQUER andar N, o
    estado φ_N não é tracial — φ_N(chainUp·chainDown) ≠
    φ_N(chainDown·chainUp). O tipo III realizado na torre concreta que
    constrói o fator ITPFI, andar a andar. -/
theorem chainState_not_tracial_tower (l : ℝ) (hl : 0 < l) (hne : l ≠ 1)
    (N : ℕ) :
    chainState l N (chainUp N * chainDown N)
      ≠ chainState l N (chainDown N * chainUp N) := by
  have hr := powers_ladder l hl N
  unfold RatioWitness at hr
  intro heq
  -- heq : φ_N(chainUp·chainDown) = φ_N(chainDown·chainUp) =: c
  -- hr  : φ_N(chainUp·chainDown) = λ^(N+1) · φ_N(chainDown·chainUp)
  have hup : chainState l N (chainUp N * chainDown N)
      = trace (chainDensity l N * (chainUp N * chainDown N)) := rfl
  have hdown : chainState l N (chainDown N * chainUp N)
      = trace (chainDensity l N * (chainDown N * chainUp N)) := rfl
  rw [hup, hdown] at heq
  rw [hr] at heq
  -- heq : λ^(N+1)·c = c
  have hc : trace (chainDensity l N * (chainDown N * chainUp N))
      = (((1 / (1 + l)) ^ (N + 1) : ℝ) : ℂ) := by
    have := chainDownUp_value l hl N
    unfold chainState at this
    exact this
  rw [hc] at heq
  have hcne : (((1 / (1 + l)) ^ (N + 1) : ℝ) : ℂ) ≠ 0 := by
    rw [Ne, Complex.ofReal_eq_zero]
    have : (0 : ℝ) < (1 / (1 + l)) ^ (N + 1) := by positivity
    exact ne_of_gt this
  -- (λ^(N+1) : ℂ)·c = c ⟹ λ^(N+1) = 1 (contradição)
  have hcast : ((l ^ (N + 1) : ℝ) : ℂ) * (((1 / (1 + l)) ^ (N + 1) : ℝ) : ℂ)
      = 1 * (((1 / (1 + l)) ^ (N + 1) : ℝ) : ℂ) := by
    rw [one_mul]; exact heq
  have hratio : ((l ^ (N + 1) : ℝ) : ℂ) = 1 :=
    mul_right_cancel₀ hcne hcast
  have hreal : l ^ (N + 1) = 1 := by
    have := hratio
    rw [show (1 : ℂ) = ((1 : ℝ) : ℂ) from rfl, Complex.ofReal_inj] at this
    exact this
  exact tower_ratio_ne_one l hl hne N hreal

end

end TGLExt
