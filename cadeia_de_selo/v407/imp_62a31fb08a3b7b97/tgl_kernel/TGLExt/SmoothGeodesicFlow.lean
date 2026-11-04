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
import TGLExt.FlowTimePropagation

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Flow017
open Filter Topology Set ChatgptAudit.Flow016 ChatgptAudit.Screen015
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem phase_flow_of_variational_smooth {f : Phase4 → Phase4} {Q : Set Phase4} {p : Phase4}
    (V : LipschitzLocalFlow (variationalField f) (variationalDomain Q)
      (p,ContinuousLinearMap.id ℝ Phase4)) (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q) :
    ContDiffOn ℝ ∞ (phaseFlowOfVariational V).flow
      (Metric.ball p (phaseFlowOfVariational V).radius ×ˢ
        Ioo (-(phaseFlowOfVariational V).radius) (phaseFlowOfVariational V).radius) :=
  flow_smooth_on_domain (projectedVariationalFlow V) hQ hf

theorem c1_geodesic_flow_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (x v : Coordinate4) (hx : x∈U) (hv : v≠0) :
    let V := c1GeodesicFlow U hU Gamma hG x v hx hv
    ContDiffOn ℝ ∞ V.flow (Metric.ball (x,v) V.radius ×ˢ Ioo (-V.radius) V.radius) := by
  dsimp only [c1GeodesicFlow]
  exact phase_flow_of_variational_smooth _ (regular_phase_domain_open U hU)
    ((geodesic_spray_smooth U hU Gamma hG).mono (fun _ hz => hz.1))

theorem local_smooth_metric_null_geodesics (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma) (hm : MetricCompatibleOn U g Gamma)
    (x v : Coordinate4) (hx : x∈U) (hv : v≠0) :
    ∃ V : LocalPhaseFlow (geodesicSpray Gamma) (regularPhaseDomain U) (x,v),
      ContDiffOn ℝ ∞ V.flow (Metric.ball (x,v) V.radius ×ˢ Ioo (-V.radius) V.radius) ∧
      ∀ q∈Metric.ball (x,v) V.radius, tensorQuad (g q.1) q.2=0 →
        ∀ t∈Ioo (-V.radius) V.radius, tensorQuad (g (V.flow (q,t)).1) (V.flow (q,t)).2=0 := by
  let V := c1GeodesicFlow U hU Gamma hG x v hx hv
  refine ⟨V,c1_geodesic_flow_smooth U hU Gamma hG x v hx hv,?_⟩
  intro q hq hn t ht
  exact geodesic_flow_null_preserved U hU g Gamma hg hm (x,v) V q hq hn t ht

theorem local_smooth_levi_civita_null_geodesics (U : Set Coordinate4) (hU : IsOpen U)
    (A B : TensorField4) (hAB : ∀ y∈U, A y*B y=1) (hBA : ∀ y∈U, B y*A y=1)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B)
    (x v : Coordinate4) (hx : x∈U) (hv : v≠0) :
    ∃ V : LocalPhaseFlow (geodesicSpray (frameLeviCivita A B)) (regularPhaseDomain U) (x,v),
      ContDiffOn ℝ ∞ V.flow (Metric.ball (x,v) V.radius ×ˢ Ioo (-V.radius) V.radius) ∧
      ∀ q∈Metric.ball (x,v) V.radius, tensorQuad (frameMetricField A q.1) q.2=0 →
        ∀ t∈Ioo (-V.radius) V.radius,
          tensorQuad (frameMetricField A (V.flow (q,t)).1) (V.flow (q,t)).2=0 := by
  have hg := frame_metric_smooth U A hA
  have hm : MetricCompatibleOn U (frameMetricField A) (frameLeviCivita A B) :=
    levi_civita_field_metric_compatible U hU (frameMetricField A) (inverseFrameMetricField B)
      (fun y _ => frame_metric_symmetric A y)
      (fun y hy => inverse_frame_metric_left A B y (hAB y hy) (hBA y hy))
      (fun y hy => inverse_frame_metric_right A B y (hAB y hy) (hBA y hy))
  exact local_smooth_metric_null_geodesics U hU (frameMetricField A) (frameLeviCivita A B) hg
    (levi_civita_field_smooth U hU (frameMetricField A) (inverseFrameMetricField B)
      hg (inverse_frame_metric_smooth U B hB)) hm x v hx hv

#print axioms phase_flow_of_variational_smooth
#print axioms c1_geodesic_flow_smooth
#print axioms local_smooth_metric_null_geodesics
#print axioms local_smooth_levi_civita_null_geodesics
end
end ChatgptAudit.Flow017
