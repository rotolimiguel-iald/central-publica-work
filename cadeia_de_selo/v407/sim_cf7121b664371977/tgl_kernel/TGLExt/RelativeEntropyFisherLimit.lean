-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_021 (05-06/09/2026), transposta em 06/09/2026
-- Lote 007..023: habitante GLOBAL periodico da esperanca do centralizador; cauda nao ciclica;
--   obstrucoes de Borchers e da assinatura; e a camada GEOMETRICA GERAL em carta: tensores,
--   conexao de Levi-Civita, curvatura, Bianchi, Einstein geometrico + conservacao, Raychaudhuri,
--   Clausius local <=> balanco nulo de Ricci, telas/congruencias nulas construidas, area e calor,
--   entropia relativa, dinamica unitaria, covetor de materia. Estatuto [REAL / INPUT / OPEN]:
--   Clausius, a metrica lorentziana, H3 dinamico, assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100% nas 17 entregas; 17/17
--   auditores da bancada exit 0; recompilacao INDEPENDENTE 116/116 exit 0, todos os axiomas no
--   trio [propext, Classical.choice, Quot.sound]; zero sorry/warning; enunciados lidos.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports; nada mais.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.DiagonalStateCurve

set_option autoImplicit false
set_option maxHeartbeats 5500000
namespace ChatgptAudit.Micro021
open Matrix Filter Topology Set ChatgptAudit.Flow020
noncomputable section
variable {ι : Type} [Fintype ι] {p : ι → ℝ} (X : DiagonalStateCurve p)

theorem state_log_ratio_slope (hp : ∀ i, 0<p i) (i : ι) :
    Tendsto (fun t => (Real.log (X.weights t i)-Real.log (p i))/t)
      (𝓝[<] 0) (𝓝 (X.tangent 0 i/p i)) := by
  have hn : X.weights 0 i≠0 := by rw [X.at_zero]; exact ne_of_gt (hp i)
  have hd : HasDerivAt (fun t => Real.log (X.weights t i)-Real.log (p i))
      (X.tangent 0 i/p i) 0 := by
    simpa only [X.at_zero] using ((X.derivative_zero i).log hn).sub_const (Real.log (p i))
  simpa only [zero_add,X.at_zero,sub_self,sub_zero,smul_eq_mul,div_eq_mul_inv,mul_comm]
    using hd.tendsto_slope_zero_left

theorem relative_entropy_rate_slope (hp : ∀ i, 0<p i) :
    Tendsto (fun t => relativeEntropyRate X t/t) (𝓝[<] 0)
      (𝓝 (diagonalFisher p (X.tangent 0))) := by
  have hi (i : ι) : Tendsto
      (fun t => X.tangent t i*((Real.log (X.weights t i)-Real.log (p i))/t))
      (𝓝[<] 0) (𝓝 (X.tangent 0 i*(X.tangent 0 i/p i))) := by
    have hq : Tendsto (fun t => X.tangent t i) (𝓝[<] (0:ℝ)) (𝓝 (X.tangent 0 i)) :=
      (X.tangent_continuous i).tendsto.mono_left nhdsWithin_le_nhds
    exact hq.mul (state_log_ratio_slope X hp i)
  have hs := tendsto_finsetSum Finset.univ (fun i _ => hi i)
  have hf : (fun t => relativeEntropyRate X t/t)=
      (fun t => ∑ i, X.tangent t i*((Real.log (X.weights t i)-Real.log (p i))/t)) := by
    funext t
    unfold relativeEntropyRate
    rw [Finset.sum_div]
    apply Finset.sum_congr rfl
    intro i _
    ring
  have hc : (∑ i, X.tangent 0 i*(X.tangent 0 i/p i))=diagonalFisher p (X.tangent 0) := by
    unfold diagonalFisher
    apply Finset.sum_congr rfl
    intro i _
    ring
  rwa [←hf,hc] at hs

theorem relative_entropy_curve_quadratic_limit (hp : ∀ i, 0<p i) :
    Tendsto (fun t => diagonalRelativeEntropy (X.weights t) p/t^2)
      (𝓝[<] 0) (𝓝 (diagonalFisher p (X.tangent 0)/2)) := by
  apply primitive_quadratic_limit (relativeEntropyRate X)
    (fun t => diagonalRelativeEntropy (X.weights t) p) (diagonalFisher p (X.tangent 0))
  · exact relative_curve_derivative_past X hp
  · exact relative_curve_continuous_zero X hp
  · have hw : X.weights 0=p := funext X.at_zero
    rw [hw,relative_entropy_self]
  · exact relative_entropy_rate_slope X hp

theorem relative_entropy_quadratic_zero_iff (hp : ∀ i, 0<p i) :
    Tendsto (fun t => diagonalRelativeEntropy (X.weights t) p/t^2)
      (𝓝[<] 0) (𝓝 0) ↔ X.tangent 0=0 := by
  rw [past_zero_limit_iff _ _ (relative_entropy_curve_quadratic_limit X hp)]
  constructor
  · intro h
    apply (diagonal_fisher_zero_iff p (X.tangent 0) hp).mp
    linarith
  · intro h
    rw [(diagonal_fisher_zero_iff p (X.tangent 0) hp).mpr h]
    norm_num

theorem relative_entropy_first_order_zero (hp : ∀ i, 0<p i) :
    Tendsto (fun t => diagonalRelativeEntropy (X.weights t) p/t) (𝓝[<] 0) (𝓝 0) := by
  have hd := relative_curve_derivative_zero X hp
  have hw : X.weights 0=p := funext X.at_zero
  simpa only [zero_add,hw,relative_entropy_self,sub_zero,smul_eq_mul,div_eq_mul_inv,mul_comm]
    using hd.tendsto_slope_zero_left

#print axioms state_log_ratio_slope
#print axioms relative_entropy_rate_slope
#print axioms relative_entropy_curve_quadratic_limit
#print axioms relative_entropy_quadratic_zero_iff
#print axioms relative_entropy_first_order_zero
end
end ChatgptAudit.Micro021
