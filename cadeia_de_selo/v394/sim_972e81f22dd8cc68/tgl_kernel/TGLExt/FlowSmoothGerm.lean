-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_017 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.FlowRegularityInduction

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Flow017
open Filter Topology Set ChatgptAudit.Flow016
open scoped ContDiff
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
variable {f : E → E} {Q : Set E} {p : E}

theorem flow_finite_regular_at_initial (F : LipschitzLocalFlow f Q p)
    (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q)
    (q : E) (hq : q∈Metric.ball p F.radius) (n : ℕ) :
    ContDiffAt ℝ n F.flow (q,(0:ℝ)) := by
  have h0 : (0:ℝ)∈Ioo (-F.radius) F.radius :=
    ⟨neg_neg_of_pos F.radius_positive,F.radius_positive⟩
  have hqQ : q∈Q := by
    simpa only [F.initial q hq] using F.stays q hq 0 h0
  obtain ⟨V,hV⟩ := exists_finite_regular_flow n E Q hQ f hf q hqQ
  have heq := flow_germ_eq_at_initial F V q hq (Metric.mem_ball_self V.radius_positive)
    (((hf q hqQ).contDiffAt (hQ.mem_nhds hqQ)).of_le (by simp))
  exact hV.congr_of_eventuallyEq heq

theorem flow_smooth_at_initial (F : LipschitzLocalFlow f Q p)
    (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q)
    (q : E) (hq : q∈Metric.ball p F.radius) :
    ContDiffAt ℝ ∞ F.flow (q,(0:ℝ)) :=
  contDiffAt_infty.2 (flow_finite_regular_at_initial F hQ hf q hq)

omit [CompleteSpace E] in
theorem flow_finite_regular_times_open (F : E × ℝ → E) (q : E) (n : ℕ) :
    IsOpen {t : ℝ | ContDiffAt ℝ n F (q,t)} := by
  apply isOpen_iff_mem_nhds.2
  intro t ht
  change ContDiffAt ℝ n F (q,t) at ht
  have hc : ContinuousAt (fun s : ℝ => (q,s)) t := by fun_prop
  exact hc.eventually (ht.eventually (by simp))

#print axioms flow_finite_regular_at_initial
#print axioms flow_smooth_at_initial
#print axioms flow_finite_regular_times_open
end
end ChatgptAudit.Flow017
