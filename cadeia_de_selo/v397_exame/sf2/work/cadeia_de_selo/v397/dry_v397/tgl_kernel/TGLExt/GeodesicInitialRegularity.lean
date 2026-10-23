-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_016 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.FlowDifferentiability
import Mathlib.Analysis.Calculus.FDeriv.Partial

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Flow016
open Filter Topology Set
open scoped ContDiff
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
variable {f : E → E} {Q : Set E} {p : E}
  (F : LipschitzLocalFlow (variationalField f) (variationalDomain Q) (p,ContinuousLinearMap.id ℝ E))

def flowJointDerivative (q : E) (t : ℝ) : E × ℝ →L[ℝ] E :=
  (flowVariation F q t).coprod ((ContinuousLinearMap.id ℝ ℝ).smulRight (f (flowSolution F q t)))

theorem flow_time_derivative_continuous (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q)
    (r : E) (hr : r∈Metric.ball p F.radius) (T : ℝ) (hT : T∈Ioo (-F.radius) F.radius) :
    ContinuousAt (fun z : E × ℝ =>
      (ContinuousLinearMap.id ℝ ℝ).smulRight (f (flowSolution F z.1 z.2))) (r,T) := by
  have hx := flow_solution_stays F r hr T hT
  have hfc : ContinuousAt f (flowSolution F r T) :=
    ((hf _ hx).contDiffAt (hQ.mem_nhds hx)).continuousAt
  have hc : ContinuousAt (fun z : E × ℝ => f (flowSolution F z.1 z.2)) (r,T) :=
    hfc.comp (f := fun z : E × ℝ => flowSolution F z.1 z.2)
      (solution_and_variation_continuous F r hr T hT).fst
  exact (ContinuousLinearMap.smulRightL ℝ ℝ E (ContinuousLinearMap.id ℝ ℝ)).continuous.continuousAt.comp hc

theorem flow_joint_hasStrictFDerivAt (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q)
    (r : E) (hr : r∈Metric.ball p F.radius) (T : ℝ) (hT : T∈Ioo (-F.radius) F.radius) :
    HasStrictFDerivAt (fun z : E × ℝ => flowSolution F z.1 z.2) (flowJointDerivative F r T) (r,T) := by
  have hdom : Metric.ball p F.radius ×ˢ Ioo (-F.radius) F.radius∈𝓝 (r,T) :=
    (Metric.isOpen_ball.prod isOpen_Ioo).mem_nhds ⟨hr,hT⟩
  unfold flowJointDerivative
  apply hasStrictFDerivAt_uncurry_coprod (f := flowSolution F) (u := (r,T))
    (f₁ := flowVariation F)
    (f₂ := fun q t => (ContinuousLinearMap.id ℝ ℝ).smulRight (f (flowSolution F q t)))
  · filter_upwards [hdom] with z hz
    exact flow_initial_hasFDerivAt F hQ hf z.1 hz.1 z.2 hz.2
  · filter_upwards [hdom] with z hz
    exact (flow_solution_derivative F z.1 hz.1 z.2 hz.2).hasFDerivAt
  · exact (solution_and_variation_continuous F r hr T hT).snd
  · exact flow_time_derivative_continuous F hQ hf r hr T hT

theorem flow_joint_derivative_continuous (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q)
    (r : E) (hr : r∈Metric.ball p F.radius) (T : ℝ) (hT : T∈Ioo (-F.radius) F.radius) :
    ContinuousAt (fun z : E × ℝ => flowJointDerivative F z.1 z.2) (r,T) :=
  (solution_and_variation_continuous F r hr T hT).snd.continuousLinearMapCoprod
    (flow_time_derivative_continuous F hQ hf r hr T hT)

theorem flow_joint_c1 (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q) :
    ContDiffOn ℝ 1 (fun z : E × ℝ => flowSolution F z.1 z.2)
      (Metric.ball p F.radius ×ˢ Ioo (-F.radius) F.radius) := by
  have hopen : IsOpen (Metric.ball p F.radius ×ˢ Ioo (-F.radius) F.radius) :=
    Metric.isOpen_ball.prod isOpen_Ioo
  apply (contDiffOn_succ_iff_hasFDerivWithinAt_of_uniqueDiffOn (n := 0) hopen.uniqueDiffOn).2
  refine ⟨by simp,fun z => flowJointDerivative F z.1 z.2,?_,?_⟩
  · rw [contDiffOn_zero]
    intro z hz
    exact (flow_joint_derivative_continuous F hQ hf z.1 hz.1 z.2 hz.2).continuousWithinAt
  · intro z hz
    exact (flow_joint_hasStrictFDerivAt F hQ hf z.1 hz.1 z.2 hz.2).hasFDerivAt.hasFDerivWithinAt


open ChatgptAudit.Screen015
open scoped Matrix.Norms.Elementwise

def phaseFlowOfVariational {f : Phase4 → Phase4} {Q : Set Phase4} {p : Phase4}
    (V : LipschitzLocalFlow (variationalField f) (variationalDomain Q)
      (p,ContinuousLinearMap.id ℝ Phase4)) : LocalPhaseFlow f Q p where
  radius := V.radius
  radius_positive := V.radius_positive
  flow := fun z => flowSolution V z.1 z.2
  initial := flow_solution_initial V
  derivative := flow_solution_derivative V
  stays := flow_solution_stays V
  continuous := fun z hz =>
    (solution_and_variation_continuous V z.1 hz.1 z.2 hz.2).fst.continuousWithinAt

theorem phase_flow_of_variational_c1 {f : Phase4 → Phase4} {Q : Set Phase4} {p : Phase4}
    (V : LipschitzLocalFlow (variationalField f) (variationalDomain Q)
      (p,ContinuousLinearMap.id ℝ Phase4)) (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q) :
    ContDiffOn ℝ 1 (phaseFlowOfVariational V).flow
      (Metric.ball p (phaseFlowOfVariational V).radius ×ˢ
        Ioo (-(phaseFlowOfVariational V).radius) (phaseFlowOfVariational V).radius) :=
  flow_joint_c1 V hQ hf

def c1GeodesicFlow (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (x v : Coordinate4) (hx : x∈U) (hv : v≠0) :
    LocalPhaseFlow (geodesicSpray Gamma) (regularPhaseDomain U) (x,v) :=
  phaseFlowOfVariational (variationalLocalFlow (regularPhaseDomain U)
    (regular_phase_domain_open U hU) (geodesicSpray Gamma)
    ((geodesic_spray_smooth U hU Gamma hG).mono (fun _ hz => hz.1)) (x,v) ⟨hx,hv⟩)

theorem c1_geodesic_flow_joint_c1 (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (x v : Coordinate4) (hx : x∈U) (hv : v≠0) :
    let V := c1GeodesicFlow U hU Gamma hG x v hx hv
    ContDiffOn ℝ 1 V.flow (Metric.ball (x,v) V.radius ×ˢ Ioo (-V.radius) V.radius) := by
  dsimp only [c1GeodesicFlow]
  exact phase_flow_of_variational_c1 _ (regular_phase_domain_open U hU)
    ((geodesic_spray_smooth U hU Gamma hG).mono (fun _ hz => hz.1))

theorem local_c1_metric_null_geodesics (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma) (hm : MetricCompatibleOn U g Gamma)
    (x v : Coordinate4) (hx : x∈U) (hv : v≠0) :
    ∃ V : LocalPhaseFlow (geodesicSpray Gamma) (regularPhaseDomain U) (x,v),
      ContDiffOn ℝ 1 V.flow (Metric.ball (x,v) V.radius ×ˢ Ioo (-V.radius) V.radius) ∧
      ∀ q∈Metric.ball (x,v) V.radius, tensorQuad (g q.1) q.2=0 →
        ∀ t∈Ioo (-V.radius) V.radius, tensorQuad (g (V.flow (q,t)).1) (V.flow (q,t)).2=0 := by
  let V := c1GeodesicFlow U hU Gamma hG x v hx hv
  refine ⟨V,c1_geodesic_flow_joint_c1 U hU Gamma hG x v hx hv,?_⟩
  intro q hq hn t ht
  exact geodesic_flow_null_preserved U hU g Gamma hg hm (x,v) V q hq hn t ht

theorem local_c1_levi_civita_null_geodesics (U : Set Coordinate4) (hU : IsOpen U)
    (A B : TensorField4) (hAB : ∀ y∈U, A y*B y=1) (hBA : ∀ y∈U, B y*A y=1)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B)
    (x v : Coordinate4) (hx : x∈U) (hv : v≠0) :
    ∃ V : LocalPhaseFlow (geodesicSpray (frameLeviCivita A B)) (regularPhaseDomain U) (x,v),
      ContDiffOn ℝ 1 V.flow (Metric.ball (x,v) V.radius ×ˢ Ioo (-V.radius) V.radius) ∧
      ∀ q∈Metric.ball (x,v) V.radius, tensorQuad (frameMetricField A q.1) q.2=0 →
        ∀ t∈Ioo (-V.radius) V.radius,
          tensorQuad (frameMetricField A (V.flow (q,t)).1) (V.flow (q,t)).2=0 := by
  have hg := frame_metric_smooth U A hA
  have hm : MetricCompatibleOn U (frameMetricField A) (frameLeviCivita A B) :=
    levi_civita_field_metric_compatible U hU (frameMetricField A) (inverseFrameMetricField B)
      (fun y _ => frame_metric_symmetric A y)
      (fun y hy => inverse_frame_metric_left A B y (hAB y hy) (hBA y hy))
      (fun y hy => inverse_frame_metric_right A B y (hAB y hy) (hBA y hy))
  exact local_c1_metric_null_geodesics U hU (frameMetricField A) (frameLeviCivita A B) hg
    (levi_civita_field_smooth U hU (frameMetricField A) (inverseFrameMetricField B)
      hg (inverse_frame_metric_smooth U B hB)) hm x v hx hv

#print axioms phaseFlowOfVariational
#print axioms phase_flow_of_variational_c1
#print axioms c1GeodesicFlow
#print axioms c1_geodesic_flow_joint_c1
#print axioms local_c1_metric_null_geodesics
#print axioms local_c1_levi_civita_null_geodesics

#print axioms flow_time_derivative_continuous
#print axioms flow_joint_hasStrictFDerivAt
#print axioms flow_joint_derivative_continuous
#print axioms flow_joint_c1
end
end ChatgptAudit.Flow016
