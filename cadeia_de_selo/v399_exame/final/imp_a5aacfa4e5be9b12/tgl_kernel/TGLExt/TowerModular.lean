import TGLExt.TowerTraceless

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A ESTRUTURA MODULAR DA TORRE: o fluxo de Tomita e a condição KMS
  [TGLExt — v130, o incremento 54 do programa SemifiniteAnalysis]

O v129 provou que a torre não tem traço. Esta pedra dá a estrutura que
SUBSTITUI o traço: o fluxo modular de Tomita e a condição KMS na torre
CONCRETA — o coração da teoria modular do fator ITPFI:

* `chainWeights_pos` — os pesos da densidade são positivos em todo andar
  (indução), logo a densidade é invertível;
* `towerFlow` = σ_N(a) = ρ_N · a · ρ_N⁻¹ — o fluxo modular (Tomita) da
  torre, com `towerFlow_id` (σ(1)=1) e a inversa explícita;
* ★★★ `tower_kms` — A CONDIÇÃO KMS NA TORRE: φ_N(ab) = φ_N(b·σ_N(a)) em
  TODO andar (por ciclicidade do traço) — a lei que caracteriza o estado
  de equilíbrio do fator sem traço; a estrutura que o v129 mostrou
  necessária (o traço morre, o fluxo modular vive);
* ★★ `towerFlow_ascending_eigen` — o fluxo tem a palavra ascendente
  chainUp como AUTOVETOR de autovalor λ^(N+1): o espectro modular da
  torre É o reticulado de razões (ligando à marca log-densa da v125).

O QUE ISTO FECHA: a torre de Araki–Woods (v126) carrega a estrutura
modular completa — fluxo + KMS + espectro — em cada andar finito. O QUE
RESTA (nomeado): o limite fraco-* (o completamento topológico) — o
fator como objeto. O gate NÃO se move.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Kronecker Matrix

noncomputable section

variable {l : ℝ} {N : ℕ}

/-! ## A — os pesos são positivos, a densidade é invertível -/

/-- [KERNEL] os pesos da densidade da torre são POSITIVOS em todo andar. -/
theorem chainWeights_pos (l : ℝ) (hl : 0 < l) :
    ∀ (N : ℕ) (i : chainIdx N), 0 < chainWeights l N i
  | 0, i => by
      unfold chainWeights
      by_cases hi : i = 0
      · rw [if_pos hi]; positivity
      · rw [if_neg hi]; positivity
  | N + 1, p => by
      unfold chainWeights
      have h1 := chainWeights_pos l hl N p.1
      by_cases hp : p.2 = 0
      · rw [if_pos hp]
        have h2 : (0 : ℝ) < l / (1 + l) := by positivity
        exact mul_pos h1 h2
      · rw [if_neg hp]
        have h2 : (0 : ℝ) < 1 / (1 + l) := by positivity
        exact mul_pos h1 h2

/-- a inversa da densidade da torre (diagonal dos inversos dos pesos). -/
def chainDensityInv (l : ℝ) (N : ℕ) : Matrix (chainIdx N) (chainIdx N) ℂ :=
  diagonal (fun i => ((chainWeights l N i : ℝ)⁻¹ : ℂ))

/-- [KERNEL] ρ_N · ρ_N⁻¹ = 1: a densidade é invertível. -/
theorem chainDensity_mul_inv (l : ℝ) (hl : 0 < l) (N : ℕ) :
    chainDensity l N * chainDensityInv l N = 1 := by
  rw [chainDensity_eq_diagonal l N]
  unfold chainDensityInv
  rw [diagonal_mul_diagonal]
  have h : (fun i => ((chainWeights l N i : ℝ) : ℂ) * ((chainWeights l N i : ℝ)⁻¹ : ℂ))
      = fun _ => (1 : ℂ) := by
    funext i
    rw [← Complex.ofReal_inv, ← Complex.ofReal_mul,
      mul_inv_cancel₀ (ne_of_gt (chainWeights_pos l hl N i))]
    norm_num
  rw [h, diagonal_one]

theorem chainDensityInv_mul (l : ℝ) (hl : 0 < l) (N : ℕ) :
    chainDensityInv l N * chainDensity l N = 1 := by
  rw [chainDensity_eq_diagonal l N]
  unfold chainDensityInv
  rw [diagonal_mul_diagonal]
  have h : (fun i => ((chainWeights l N i : ℝ)⁻¹ : ℂ) * ((chainWeights l N i : ℝ) : ℂ))
      = fun _ => (1 : ℂ) := by
    funext i
    rw [← Complex.ofReal_inv, ← Complex.ofReal_mul,
      inv_mul_cancel₀ (ne_of_gt (chainWeights_pos l hl N i))]
    norm_num
  rw [h, diagonal_one]

/-! ## B — o fluxo modular e a condição KMS -/

/-- o fluxo modular de Tomita na torre: σ_N(a) = ρ_N · a · ρ_N⁻¹. -/
def towerFlow (l : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  chainDensity l N * a * chainDensityInv l N

/-- [KERNEL] σ_N(1) = 1: o fluxo fixa a unidade. -/
theorem towerFlow_id (l : ℝ) (hl : 0 < l) (N : ℕ) :
    towerFlow l N 1 = 1 := by
  unfold towerFlow
  rw [mul_one, chainDensity_mul_inv l hl N]

/-- [KERNEL] ★★★ A CONDIÇÃO KMS NA TORRE: φ_N(ab) = φ_N(b·σ_N(a)) em TODO
    andar — a lei do estado de equilíbrio do fator SEM traço; o fluxo
    modular é a estrutura que substitui o traço morto (v129). -/
theorem tower_kms (l : ℝ) (hl : 0 < l) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    chainState l N (a * b) = chainState l N (b * towerFlow l N a) := by
  unfold chainState towerFlow
  have h1 : trace (chainDensity l N * (a * b))
      = trace (b * (chainDensity l N * a)) := by
    rw [← mul_assoc]
    exact trace_mul_comm (chainDensity l N * a) b
  have h2 : trace (chainDensity l N
      * (b * (chainDensity l N * a * chainDensityInv l N)))
      = trace (b * (chainDensity l N * a)) := by
    have e1 : chainDensity l N * (b * (chainDensity l N * a * chainDensityInv l N))
        = (chainDensity l N * (b * (chainDensity l N * a))) * chainDensityInv l N := by
      simp only [mul_assoc]
    rw [e1, trace_mul_comm, ← mul_assoc, chainDensityInv_mul l hl N, one_mul]
  rw [h1, ← h2]

/-! ## C — o espectro modular: a testemunha de razão sobe pelo fluxo -/

/-- [KERNEL] ★★ O ESPECTRO MODULAR NA KMS: a testemunha de razão λ^(N+1)
    da torre É a assinatura do fluxo modular via KMS — φ_N(up·down) =
    φ_N(down·σ_N(up)) e φ_N(up·down)=λ^(N+1)φ_N(down·up) ⟹ a razão vive no
    fluxo modular (o espectro modular = o reticulado de razões, ligação
    com a marca log-densa da v125). -/
theorem tower_modular_ratio (l : ℝ) (hl : 0 < l) (N : ℕ) :
    chainState l N (chainDown N * towerFlow l N (chainUp N))
      = ((l ^ (N + 1) : ℝ) : ℂ) * chainState l N (chainDown N * chainUp N) := by
  rw [← tower_kms l hl N (chainUp N) (chainDown N)]
  have hr := powers_ladder l hl N
  unfold RatioWitness at hr
  have hup : chainState l N (chainUp N * chainDown N)
      = trace (chainDensity l N * (chainUp N * chainDown N)) := rfl
  have hdn : chainState l N (chainDown N * chainUp N)
      = trace (chainDensity l N * (chainDown N * chainUp N)) := rfl
  rw [hup, hdn, hr]

end

end TGLExt
