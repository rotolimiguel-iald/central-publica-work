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
import TGLExt.FlowDifferentiabilityControls

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Flow017
open Filter Topology Set ChatgptAudit.Flow016
open scoped ContDiff
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
variable {f : E → E} {Q R : Set E} {p r : E}

theorem flow_germ_eq_at_initial
    (F : LipschitzLocalFlow f Q p) (G : LipschitzLocalFlow f R r)
    (q : E) (hqF : q∈Metric.ball p F.radius) (hqG : q∈Metric.ball r G.radius)
    (hf : ContDiffAt ℝ 1 f q) :
    F.flow =ᶠ[𝓝 (q,(0:ℝ))] G.flow := by
  obtain ⟨K,S,hS,hL⟩ := hf.exists_lipschitzOnWith
  have h0F : (0:ℝ)∈Ioo (-F.radius) F.radius :=
    ⟨neg_neg_of_pos F.radius_positive,F.radius_positive⟩
  have h0G : (0:ℝ)∈Ioo (-G.radius) G.radius :=
    ⟨neg_neg_of_pos G.radius_positive,G.radius_positive⟩
  have hFc := flow_joint_continuous_at f Q p F q hqF 0 h0F
  have hGc := flow_joint_continuous_at f R r G q hqG 0 h0G
  have hFS : ∀ᶠ z in 𝓝 (q,(0:ℝ)), F.flow z∈S := by
    apply hFc.eventually
    rwa [F.initial q hqF]
  have hGS : ∀ᶠ z in 𝓝 (q,(0:ℝ)), G.flow z∈S := by
    apply hGc.eventually
    rwa [G.initial q hqG]
  have hDF : Metric.ball p F.radius ×ˢ Ioo (-F.radius) F.radius∈𝓝 (q,(0:ℝ)) :=
    (Metric.isOpen_ball.prod isOpen_Ioo).mem_nhds ⟨hqF,h0F⟩
  have hDG : Metric.ball r G.radius ×ˢ Ioo (-G.radius) G.radius∈𝓝 (q,(0:ℝ)) :=
    (Metric.isOpen_ball.prod isOpen_Ioo).mem_nhds ⟨hqG,h0G⟩
  have hgood : ∀ᶠ z in 𝓝 (q,(0:ℝ)),
      z∈Metric.ball p F.radius ×ˢ Ioo (-F.radius) F.radius ∧
      z∈Metric.ball r G.radius ×ˢ Ioo (-G.radius) G.radius ∧
      F.flow z∈S ∧ G.flow z∈S := by
    filter_upwards [hDF,hDG,hFS,hGS] with z hzF hzG hzFS hzGS
    exact ⟨hzF,hzG,hzFS,hzGS⟩
  obtain ⟨radius,hradius,hrect⟩ := eventually_flow_rectangle q _ hgood
  have h0 : (0:ℝ)∈Ioo (-radius) radius :=
    ⟨neg_neg_of_pos hradius,hradius⟩
  have hdom : Metric.ball q radius ×ˢ Ioo (-radius) radius∈𝓝 (q,(0:ℝ)) :=
    (Metric.isOpen_ball.prod isOpen_Ioo).mem_nhds ⟨Metric.mem_ball_self hradius,h0⟩
  filter_upwards [hdom] with z hz
  have hi := hrect z.1 hz.1 0 h0
  have he := ODE_solution_unique_of_mem_Ioo
    (v := fun _ : ℝ => f) (s := fun _ : ℝ => S)
    (fun _ _ => hL) h0
    (fun t ht => ⟨F.derivative z.1 (hrect z.1 hz.1 t ht).1.1 t
      (hrect z.1 hz.1 t ht).1.2,(hrect z.1 hz.1 t ht).2.2.1⟩)
    (fun t ht => ⟨G.derivative z.1 (hrect z.1 hz.1 t ht).2.1.1 t
      (hrect z.1 hz.1 t ht).2.1.2,(hrect z.1 hz.1 t ht).2.2.2⟩)
    ((F.initial z.1 hi.1.1).trans (G.initial z.1 hi.2.1.1).symm)
  exact he hz.2

#print axioms flow_germ_eq_at_initial
end
end ChatgptAudit.Flow017
