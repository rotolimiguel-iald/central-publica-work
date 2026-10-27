-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_054 (06-07/09/2026), transposta em 07/09/2026
-- Lote 046..054 (ORDEM_008 cumprida; «tudo o que a bancada podia», 9 entregas, 43 modulos).
--   046: a ESPERANCA APERIODICA — aperiodicExpectationInput P : ExpectationInput P para TODO perfil da torre
--     (media de Cesaro do fluxo modular; limite forte; into/fixes/ortho); o levantamento do Lema 3 dispara para
--     todo perfil e todo horizonte (the_lift_fires_on_the_aperiodic_tower); unicidade; E comuta com sigma_t.
--   047: propriedades da esperanca — linear sobre M, preserva 1/estado/adjunto, bimodular sobre o centralizador,
--     COMPLETAMENTE POSITIVA (CompletelyPositiveMap da mathlib), contracao GNS, NORMAL (supremos positivos dirigidos).
--   048: obstrucoes da identificacao modular/geometrica — Borchers trivial sobrevive ao transporte de estado (027);
--     periodo do fluxo forca retorno de rotulos em localizacao fiel covariante; ligado ao boost 044 (negativos tipados).
--   049-050: SUBESPACO PADRAO CONTINUO em L^2 — T_c = M_exp(-c xi) positivo auto-adjunto (grafo limitado), J
--     antiunitaria, S_c = J T_c involucao fechada, K_c = Fix S_c subespaco padrao; adjunto S_c^dagger = T_c J,
--     Delta_c = S_c^dagger S_c = T_c^2 = T_{2c} com igualdade de dominios, resolvente (I + Delta_c)^{-1}.
--     Identificacao T_c = Delta_c^{1/2} e BW seguem OPEN.
--   051: balanco optico finito — Q - K DeltaA = K E com E >= 0 (integral optica), E/t^4 -> (a^2 + c^2)/12; Riccati;
--     no caso variavel o drift Z_R(s) - s R(s) persiste (controles).
--   052: setor horizontal (plano de Pauli X,Y do 1o sitio) — a esperanca centralizante zera as duas direcoes;
--     o horizonte modular faz o quarto de volta; forma invariante = c x produto GNS real; [INPUT] traco relativo = 1
--     fixa c = 1/2 (densidade de area 1/2); forma efetiva de densidade |2p - 1|. Escala livre sem calibracao por Omega.
--   053: polarizador D = P_R(-i)P_R no Hilbert real; acao GNS de todo TowerHorizon preserva Omega e entrelaca D;
--     radical = centralizador (setor auto-adjunto); CONTRAEXEMPLO: covariancia + calibracao comum NAO da unicidade
--     da area (9/10 vs 1377/1250 no 2o par).
--   054: custo modular do polarizador C_D(x) = sum 2||D^(n+1)x||^2/(2n+1): l.s.c., preservado por todo TowerHorizon,
--     custo zero <=> centralizador; f(0)=0, f(0)=2 localModularCost; C_D(X_1 Omega) = log2/3 na referencia p = 1/3.
--   Estatuto: [REAL] o que esta compilado; [INPUT] calibracao por Omega, traco relativo = 1; [OPEN] H3, selecao
--   fisica da area, escala dimensional, regiao <-> algebra, BW/identificacao T_c = Delta^{1/2}, reconstrucao geral.
-- Auditoria da gerencia (sessao d554e796, 07/09/2026): hashes 185/185 (9 entregas); 9/9 auditores exit 0;
--   recompilacao INDEPENDENTE 43/43, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.Normed.Operator.ContinuousLinearMap
import Mathlib.Topology.Semicontinuity.Basic

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Cost054

open scoped ENNReal NNReal
noncomputable section

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

/-- The positive coefficients of the modular-cost series. -/
def polarizerCostWeight (n : ℕ) : ℝ := 2 / (2 * (n : ℝ) + 1)

theorem polarizer_cost_weight_pos (n : ℕ) : 0 < polarizerCostWeight n := by
  unfold polarizerCostWeight
  positivity

/-- Every summand is finite, even when the full cost is infinite. -/
def polarizerCostTerm (D : H →L[ℝ] H) (x : H) (n : ℕ) : ℝ≥0∞ :=
  ENNReal.ofReal (polarizerCostWeight n * ‖(D ^ (n + 1)) x‖ ^ 2)

/-- An extended cost: divergence is retained as infinity. -/
def polarizerModularCost (D : H →L[ℝ] H) (x : H) : ℝ≥0∞ :=
  ∑' n : ℕ, polarizerCostTerm D x n

theorem polarizer_modular_cost_eq_tsum (D : H →L[ℝ] H) (x : H) :
    polarizerModularCost D x =
      ∑' n : ℕ, ENNReal.ofReal ((2 : ℝ) / (2 * (n : ℝ) + 1) *
        ‖(D ^ (n + 1)) x‖ ^ 2) := rfl

theorem polarizer_cost_term_zero (D : H →L[ℝ] H) (n : ℕ) :
    polarizerCostTerm D 0 n = 0 := by
  simp [polarizerCostTerm]

theorem polarizer_modular_cost_zero (D : H →L[ℝ] H) :
    polarizerModularCost D 0 = 0 := by
  simp [polarizerModularCost, polarizer_cost_term_zero]

theorem polarizer_cost_term_smul (D : H →L[ℝ] H) (a : ℝ) (x : H) (n : ℕ) :
    polarizerCostTerm D (a • x) n =
      ENNReal.ofReal (a ^ 2) * polarizerCostTerm D x n := by
  unfold polarizerCostTerm
  rw [map_smul, norm_smul, mul_pow, Real.norm_eq_abs, sq_abs,
    ← ENNReal.ofReal_mul (sq_nonneg a)]
  congr 1
  ring

theorem polarizer_modular_cost_smul (D : H →L[ℝ] H) (a : ℝ) (x : H) :
    polarizerModularCost D (a • x) =
      ENNReal.ofReal (a ^ 2) * polarizerModularCost D x := by
  simp only [polarizerModularCost, polarizer_cost_term_smul, ENNReal.tsum_mul_left]

theorem polarizer_cost_term_add_le (D : H →L[ℝ] H) (x y : H) (n : ℕ) :
    polarizerCostTerm D (x + y) n ≤
      2 * polarizerCostTerm D x n + 2 * polarizerCostTerm D y n := by
  have hn : ‖(D ^ (n + 1)) x + (D ^ (n + 1)) y‖ ^ 2 ≤
      2 * ‖(D ^ (n + 1)) x‖ ^ 2 + 2 * ‖(D ^ (n + 1)) y‖ ^ 2 := by
    have hp := parallelogram_law_with_norm ℝ ((D ^ (n + 1)) x) ((D ^ (n + 1)) y)
    nlinarith [sq_nonneg ‖(D ^ (n + 1)) x - (D ^ (n + 1)) y‖]
  have hw := (polarizer_cost_weight_pos n).le
  unfold polarizerCostTerm
  rw [map_add]
  calc
    ENNReal.ofReal (polarizerCostWeight n *
        ‖(D ^ (n + 1)) x + (D ^ (n + 1)) y‖ ^ 2) ≤
      ENNReal.ofReal (2 * (polarizerCostWeight n * ‖(D ^ (n + 1)) x‖ ^ 2) +
        2 * (polarizerCostWeight n * ‖(D ^ (n + 1)) y‖ ^ 2)) := by
      apply ENNReal.ofReal_le_ofReal
      nlinarith [mul_le_mul_of_nonneg_left hn hw]
    _ = _ := by
      rw [ENNReal.ofReal_add (by positivity) (by positivity),
        ENNReal.ofReal_mul (by norm_num : (0 : ℝ) ≤ 2),
        ENNReal.ofReal_mul (by norm_num : (0 : ℝ) ≤ 2)]
      norm_num

theorem polarizer_modular_cost_add_le (D : H →L[ℝ] H) (x y : H) :
    polarizerModularCost D (x + y) ≤
      2 * polarizerModularCost D x + 2 * polarizerModularCost D y := by
  unfold polarizerModularCost
  calc
    (∑' n : ℕ, polarizerCostTerm D (x + y) n) ≤
        ∑' n : ℕ, (2 * polarizerCostTerm D x n + 2 * polarizerCostTerm D y n) :=
      ENNReal.tsum_le_tsum (polarizer_cost_term_add_le D x y)
    _ = _ := by rw [ENNReal.tsum_add, ENNReal.tsum_mul_left, ENNReal.tsum_mul_left]

/-- The first positive summand detects the entire radical. -/
theorem polarizer_modular_cost_first_le (D : H →L[ℝ] H) (x : H) :
    ENNReal.ofReal (2 * ‖D x‖ ^ 2) ≤ polarizerModularCost D x := by
  simpa only [polarizerModularCost, polarizerCostTerm, polarizerCostWeight, Nat.cast_zero, mul_zero,
    zero_add, div_one, pow_one] using
      (ENNReal.le_tsum (f := polarizerCostTerm D x) 0)

theorem polarizer_modular_cost_zero_iff (D : H →L[ℝ] H) (x : H) :
    polarizerModularCost D x = 0 ↔ D x = 0 := by
  constructor
  · intro hz
    have ht : ENNReal.ofReal (2 * ‖D x‖ ^ 2) = 0 :=
      le_antisymm (hz ▸ polarizer_modular_cost_first_le D x) bot_le
    have hr := ENNReal.ofReal_eq_zero.mp ht
    apply norm_eq_zero.mp
    nlinarith [norm_nonneg (D x), sq_nonneg ‖D x‖]
  · intro hx
    have hp (n : ℕ) : (D ^ (n + 1)) x = 0 := by
      rw [pow_succ]
      change (D ^ n) (D x) = 0
      rw [hx, map_zero]
    simp [polarizerModularCost, polarizerCostTerm, hp]

/-- The domain consists exactly of vectors with finite extended cost. -/
def polarizerCostDomain (D : H →L[ℝ] H) : Submodule ℝ H where
  carrier := {x | polarizerModularCost D x < ∞}
  zero_mem' := by
    change polarizerModularCost D 0 < ∞
    rw [polarizer_modular_cost_zero]
    exact bot_lt_top
  add_mem' := by
    intro x y hx hy
    exact lt_of_le_of_lt (polarizer_modular_cost_add_le D x y)
      (ENNReal.add_lt_top.mpr
        ⟨ENNReal.mul_lt_top (by norm_num) hx, ENNReal.mul_lt_top (by norm_num) hy⟩)
  smul_mem' := by
    intro a x hx
    change polarizerModularCost D (a • x) < ∞
    rw [polarizer_modular_cost_smul]
    exact ENNReal.mul_lt_top ENNReal.ofReal_lt_top hx

theorem mem_polarizerCostDomain (D : H →L[ℝ] H) (x : H) :
    x ∈ polarizerCostDomain D ↔ polarizerModularCost D x < ∞ := Iff.rfl

theorem polarizer_cost_kernel_mem_domain (D : H →L[ℝ] H) (x : H) (hx : D x = 0) :
    x ∈ polarizerCostDomain D := by
  rw [mem_polarizerCostDomain, (polarizer_modular_cost_zero_iff D x).mpr hx]
  exact bot_lt_top

theorem polarizer_power_covariant (D : H →L[ℝ] H) (W : H ≃ₗᵢ[ℝ] H)
    (hW : ∀ x : H, D (W x) = W (D x)) (n : ℕ) (x : H) :
    (D ^ n) (W x) = W ((D ^ n) x) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ', mul_apply_eq_comp, mul_apply_eq_comp, ih, hW]

theorem polarizer_cost_term_covariant (D : H →L[ℝ] H) (W : H ≃ₗᵢ[ℝ] H)
    (hW : ∀ x : H, D (W x) = W (D x)) (x : H) (n : ℕ) :
    polarizerCostTerm D (W x) n = polarizerCostTerm D x n := by
  unfold polarizerCostTerm
  rw [polarizer_power_covariant D W hW, W.norm_map]

theorem polarizer_modular_cost_covariant (D : H →L[ℝ] H) (W : H ≃ₗᵢ[ℝ] H)
    (hW : ∀ x : H, D (W x) = W (D x)) (x : H) :
    polarizerModularCost D (W x) = polarizerModularCost D x := by
  simp only [polarizerModularCost, polarizer_cost_term_covariant D W hW]

theorem polarizer_cost_domain_covariant (D : H →L[ℝ] H) (W : H ≃ₗᵢ[ℝ] H)
    (hW : ∀ x : H, D (W x) = W (D x)) (x : H) :
    W x ∈ polarizerCostDomain D ↔ x ∈ polarizerCostDomain D := by
  rw [mem_polarizerCostDomain, mem_polarizerCostDomain,
    polarizer_modular_cost_covariant D W hW]

/-- A convergent real series can be transferred to the extended cost without losing divergence. -/
theorem polarizer_modular_cost_eq_of_hasSum (D : H →L[ℝ] H) (x : H) (c : ℝ)
    (hs : HasSum (fun n : ℕ =>
      (2 : ℝ) / (2 * (n : ℝ) + 1) * ‖(D ^ (n + 1)) x‖ ^ 2) c) :
    polarizerModularCost D x = ENNReal.ofReal c := by
  rw [polarizer_modular_cost_eq_tsum,
    ← ENNReal.ofReal_tsum_of_nonneg (fun n : ℕ => by positivity) hs.summable,
    hs.tsum_eq]

theorem polarizer_cost_mem_domain_of_hasSum (D : H →L[ℝ] H) (x : H) (c : ℝ)
    (hs : HasSum (fun n : ℕ =>
      (2 : ℝ) / (2 * (n : ℝ) + 1) * ‖(D ^ (n + 1)) x‖ ^ 2) c) :
    x ∈ polarizerCostDomain D := by
  rw [mem_polarizerCostDomain, polarizer_modular_cost_eq_of_hasSum D x c hs]
  exact ENNReal.ofReal_lt_top

/-- The extended cost is lower semicontinuous, including at its infinite values. -/
theorem polarizer_modular_cost_lowerSemicontinuous (D : H →L[ℝ] H) :
    LowerSemicontinuous (polarizerModularCost D) := by
  unfold polarizerModularCost polarizerCostTerm
  apply lowerSemicontinuous_tsum
  intro n
  exact (ENNReal.continuous_ofReal.comp
    (continuous_const.mul (((D ^ (n + 1)).continuous.norm).pow 2))).lowerSemicontinuous

#print axioms polarizerCostWeight
#print axioms polarizer_cost_weight_pos
#print axioms polarizerCostTerm
#print axioms polarizerModularCost
#print axioms polarizer_modular_cost_eq_tsum
#print axioms polarizer_cost_term_zero
#print axioms polarizer_modular_cost_zero
#print axioms polarizer_cost_term_smul
#print axioms polarizer_modular_cost_smul
#print axioms polarizer_cost_term_add_le
#print axioms polarizer_modular_cost_add_le
#print axioms polarizer_modular_cost_first_le
#print axioms polarizer_modular_cost_zero_iff
#print axioms polarizerCostDomain
#print axioms mem_polarizerCostDomain
#print axioms polarizer_cost_kernel_mem_domain
#print axioms polarizer_power_covariant
#print axioms polarizer_cost_term_covariant
#print axioms polarizer_modular_cost_covariant
#print axioms polarizer_cost_domain_covariant
#print axioms polarizer_modular_cost_eq_of_hasSum
#print axioms polarizer_cost_mem_domain_of_hasSum
#print axioms polarizer_modular_cost_lowerSemicontinuous

end
end ChatgptAudit.Cost054
