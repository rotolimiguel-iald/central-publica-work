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
import TGLExt.PolarizerModularCost
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Topology.Algebra.InfiniteSum.ENNReal
import Mathlib.Tactic

set_option autoImplicit false

namespace ChatgptAudit.Cost054

noncomputable section

/-- Every term is nonnegative, including for a negative transition ratio. -/
theorem polarizer_cost_series_term_nonneg (d : ℝ) (n : ℕ) :
    0 ≤ (2 : ℝ) / (2 * (n : ℝ) + 1) * d ^ (2 * (n + 1)) := by
  apply mul_nonneg
  · positivity
  · rw [pow_mul]
    positivity

/-- The scalar series gives the quadratic coefficient, not the second derivative. -/
theorem polarizer_cost_hasSum (d : ℝ) (hd : |d| < 1) :
    HasSum (fun n : ℕ =>
      (2 : ℝ) / (2 * (n : ℝ) + 1) * d ^ (2 * (n + 1)))
      (d * (Real.log (1 + d) - Real.log (1 - d))) := by
  have hs := (Real.hasSum_log_sub_log_of_abs_lt_one hd).mul_left d
  apply hs.congr_fun
  intro n
  rw [show 2 * (n + 1) = 2 * n + 1 + 1 by omega, pow_succ]
  ring

theorem polarizer_cost_log_ratio_hasSum (d : ℝ) (hd : |d| < 1) :
    HasSum (fun n : ℕ =>
      (2 : ℝ) / (2 * (n : ℝ) + 1) * d ^ (2 * (n + 1)))
      (d * Real.log ((1 + d) / (1 - d))) := by
  have hp : 0 < 1 + d := by
    have hh := (abs_lt.mp hd).1
    linarith
  have hm : 0 < 1 - d := by
    have hh := (abs_lt.mp hd).2
    linarith
  simpa only [Real.log_div (ne_of_gt hp) (ne_of_gt hm)] using
    polarizer_cost_hasSum d hd

theorem polarizer_weight_ratio_abs_lt_one (wi wj : ℝ)
    (hi : 0 < wi) (hj : 0 < wj) :
    |(wi - wj) / (wi + wj)| < 1 := by
  rw [abs_lt]
  constructor
  · apply (lt_div_iff₀ (add_pos hi hj)).2
    linarith
  · apply (div_lt_iff₀ (add_pos hi hj)).2
    linarith

/-- This identity does not divide by the signed ratio, so equal weights are included. -/
theorem polarizer_weight_ratio_identity (wi wj : ℝ)
    (hi : 0 < wi) (hj : 0 < wj) :
    (1 + (wi - wj) / (wi + wj)) /
      (1 - (wi - wj) / (wi + wj)) = wi / wj := by
  have hsum : wi + wj ≠ 0 := ne_of_gt (add_pos hi hj)
  have hden : 1 - (wi - wj) / (wi + wj) ≠ 0 := by
    have hh := (abs_lt.mp (polarizer_weight_ratio_abs_lt_one wi wj hi hj)).2
    linarith
  field_simp [hsum, hden, ne_of_gt hj]
  ring

theorem polarizer_cost_weights_hasSum (wi wj : ℝ)
    (hi : 0 < wi) (hj : 0 < wj) :
    HasSum (fun n : ℕ =>
      (2 : ℝ) / (2 * (n : ℝ) + 1) *
        ((wi - wj) / (wi + wj)) ^ (2 * (n + 1)))
      (((wi - wj) / (wi + wj)) * (Real.log wi - Real.log wj)) := by
  have hs := polarizer_cost_log_ratio_hasSum ((wi - wj) / (wi + wj))
    (polarizer_weight_ratio_abs_lt_one wi wj hi hj)
  simpa only [polarizer_weight_ratio_identity wi wj hi hj,
    Real.log_div (ne_of_gt hi) (ne_of_gt hj)] using hs

theorem polarizer_cost_scalar_nonneg (d : ℝ) (hd : |d| < 1) :
    0 ≤ d * (Real.log (1 + d) - Real.log (1 - d)) := by
  rw [← (polarizer_cost_hasSum d hd).tsum_eq]
  exact tsum_nonneg (polarizer_cost_series_term_nonneg d)

/-- The extended sum is identified only after real summability has been proved. -/
theorem polarizer_cost_scalar_ennreal (d : ℝ) (hd : |d| < 1) :
    (∑' n : ℕ, ENNReal.ofReal
      ((2 : ℝ) / (2 * (n : ℝ) + 1) * d ^ (2 * (n + 1)))) =
      ENNReal.ofReal (d * (Real.log (1 + d) - Real.log (1 - d))) := by
  have hs := polarizer_cost_hasSum d hd
  rw [← ENNReal.ofReal_tsum_of_nonneg
    (polarizer_cost_series_term_nonneg d) hs.summable, hs.tsum_eq]

theorem polarizer_cost_weights_ennreal (wi wj : ℝ)
    (hi : 0 < wi) (hj : 0 < wj) :
    (∑' n : ℕ, ENNReal.ofReal
      ((2 : ℝ) / (2 * (n : ℝ) + 1) *
        ((wi - wj) / (wi + wj)) ^ (2 * (n + 1)))) =
      ENNReal.ofReal (((wi - wj) / (wi + wj)) *
        (Real.log wi - Real.log wj)) := by
  have hs := polarizer_cost_weights_hasSum wi wj hi hj
  rw [← ENNReal.ofReal_tsum_of_nonneg
    (polarizer_cost_series_term_nonneg ((wi - wj) / (wi + wj)))
    hs.summable, hs.tsum_eq]

section NormPowers

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

/-- A proved norm law evaluates the existing extended cost; no spectral law is assumed
for arbitrary vectors. -/
theorem polarizer_cost_of_norm_powers (D : H →L[ℝ] H) (x : H)
    (d : ℝ) (hd : |d| < 1)
    (hnorm : ∀ n : ℕ,
      ‖(D ^ (n + 1)) x‖ ^ 2 = d ^ (2 * (n + 1)) * ‖x‖ ^ 2) :
    polarizerModularCost D x =
      ENNReal.ofReal (d * (Real.log (1 + d) - Real.log (1 - d)) * ‖x‖ ^ 2) := by
  apply polarizer_modular_cost_eq_of_hasSum
  have hs := (polarizer_cost_hasSum d hd).mul_right (‖x‖ ^ 2)
  apply hs.congr_fun
  intro n
  rw [hnorm n]
  ring

theorem polarizer_cost_of_weight_norm_powers (D : H →L[ℝ] H) (x : H)
    (wi wj : ℝ) (hi : 0 < wi) (hj : 0 < wj)
    (hnorm : ∀ n : ℕ, ‖(D ^ (n + 1)) x‖ ^ 2 =
      ((wi - wj) / (wi + wj)) ^ (2 * (n + 1)) * ‖x‖ ^ 2) :
    polarizerModularCost D x =
      ENNReal.ofReal (((wi - wj) / (wi + wj)) *
        (Real.log wi - Real.log wj) * ‖x‖ ^ 2) := by
  apply polarizer_modular_cost_eq_of_hasSum
  have hs := (polarizer_cost_weights_hasSum wi wj hi hj).mul_right (‖x‖ ^ 2)
  apply hs.congr_fun
  intro n
  rw [hnorm n]
  ring

theorem polarizer_cost_norm_powers_lt_top (D : H →L[ℝ] H) (x : H)
    (d : ℝ) (hd : |d| < 1)
    (hnorm : ∀ n : ℕ,
      ‖(D ^ (n + 1)) x‖ ^ 2 = d ^ (2 * (n + 1)) * ‖x‖ ^ 2) :
    polarizerModularCost D x < ⊤ := by
  rw [polarizer_cost_of_norm_powers D x d hd hnorm]
  exact ENNReal.ofReal_lt_top

end NormPowers

#print axioms polarizer_cost_series_term_nonneg
#print axioms polarizer_cost_hasSum
#print axioms polarizer_cost_log_ratio_hasSum
#print axioms polarizer_weight_ratio_abs_lt_one
#print axioms polarizer_weight_ratio_identity
#print axioms polarizer_cost_weights_hasSum
#print axioms polarizer_cost_scalar_nonneg
#print axioms polarizer_cost_scalar_ennreal
#print axioms polarizer_cost_weights_ennreal
#print axioms polarizer_cost_of_norm_powers
#print axioms polarizer_cost_of_weight_norm_powers
#print axioms polarizer_cost_norm_powers_lt_top

end
end ChatgptAudit.Cost054
