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
import TGLExt.GeodesicInitialRegularity

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Flow016
open Filter Topology Set ChatgptAudit.Screen015 TGLExt
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

theorem linear_taylor_remainder_zero (L : E →L[ℝ] E) (x y : E) :
    firstOrderRemainder (L : E → E) x y=0 := by
  simp only [firstOrderRemainder,L.hasFDerivAt.fderiv,map_sub,sub_self]

theorem zero_field_flow_constant {p : E}
    (V : LipschitzLocalFlow (variationalField (fun _ : E => 0)) (variationalDomain univ)
      (p,ContinuousLinearMap.id ℝ E))
    (q : E) (hq : q∈Metric.ball p V.radius) (t : ℝ) (ht : t∈Ioo (-V.radius) V.radius) :
    flowSolution V q t=q := by
  have hd (s : ℝ) (hs : s∈Ioo (-V.radius) V.radius) :
      HasDerivAt (flowSolution V q) 0 s := flow_solution_derivative V q hq s hs
  have h0 : (0:ℝ)∈Ioo (-V.radius) V.radius :=
    ⟨neg_neg_of_pos V.radius_positive,V.radius_positive⟩
  have he := isOpen_Ioo.is_const_of_deriv_eq_zero isPreconnected_Ioo
    (fun s hs => (hd s hs).differentiableAt.differentiableWithinAt)
    (fun s hs => (hd s hs).deriv) ht h0
  exact he.trans (flow_solution_initial V q hq)

theorem zero_field_variation_identity {p : E}
    (V : LipschitzLocalFlow (variationalField (fun _ : E => 0)) (variationalDomain univ)
      (p,ContinuousLinearMap.id ℝ E))
    (q : E) (hq : q∈Metric.ball p V.radius) (t : ℝ) (ht : t∈Ioo (-V.radius) V.radius) :
    flowVariation V q t=ContinuousLinearMap.id ℝ E := by
  have he : (fun r => flowSolution V r t) =ᶠ[𝓝 q] (fun r : E => r) := by
    filter_upwards [Metric.isOpen_ball.mem_nhds hq] with r hr
    exact zero_field_flow_constant V r hr t ht
  exact (flow_initial_hasFDerivAt V isOpen_univ contDiffOn_const q hq t ht).unique
    ((hasFDerivAt_id q).congr_of_eventuallyEq he)

def flatPhaseDerivative (t : ℝ) : Phase4 →L[ℝ] Phase4 :=
  ((ContinuousLinearMap.fst ℝ Coordinate4 Coordinate4)+
      t • (ContinuousLinearMap.snd ℝ Coordinate4 Coordinate4)).prod
    (ContinuousLinearMap.snd ℝ Coordinate4 Coordinate4)

theorem flat_geodesic_initial_derivative (p : Phase4)
    (V : LocalPhaseFlow (geodesicSpray (fun _ => 0)) (regularPhaseDomain univ) p)
    (q : Phase4) (hq : q∈Metric.ball p V.radius) (t : ℝ) (ht : t∈Ioo (-V.radius) V.radius) :
    HasFDerivAt (fun r => V.flow (r,t)) (flatPhaseDerivative t) q := by
  apply (flatPhaseDerivative t).hasFDerivAt.congr_of_eventuallyEq
  filter_upwards [Metric.isOpen_ball.mem_nhds hq] with r hr
  exact Prod.ext (zero_connection_position_affine p V r hr t ht)
    (zero_connection_velocity_constant p V r hr t ht)

theorem flat_variation_block (p : Phase4)
    (V : LipschitzLocalFlow (variationalField (geodesicSpray (fun _ => 0)))
      (variationalDomain (regularPhaseDomain univ)) (p,ContinuousLinearMap.id ℝ Phase4))
    (q : Phase4) (hq : q∈Metric.ball p V.radius) (t : ℝ) (ht : t∈Ioo (-V.radius) V.radius) :
    flowVariation V q t=flatPhaseDerivative t := by
  have hs : ContDiffOn ℝ ∞ (geodesicSpray (fun _ => 0)) (regularPhaseDomain univ) :=
    (geodesic_spray_smooth univ isOpen_univ (fun _ => 0)
      (fun _ _ _ => contDiffOn_const)).mono (fun _ hz => hz.1)
  exact (flow_initial_hasFDerivAt V (regular_phase_domain_open univ isOpen_univ) hs q hq t ht).unique
    (flat_geodesic_initial_derivative p (phaseFlowOfVariational V) q hq t ht)

theorem flat_variation_on_perturbation (p : Phase4)
    (V : LipschitzLocalFlow (variationalField (geodesicSpray (fun _ => 0)))
      (variationalDomain (regularPhaseDomain univ)) (p,ContinuousLinearMap.id ℝ Phase4))
    (q : Phase4) (hq : q∈Metric.ball p V.radius) (t : ℝ) (ht : t∈Ioo (-V.radius) V.radius)
    (h : Phase4) :
    flowVariation V q t h=(h.1+t • h.2,h.2) := by
  rw [flat_variation_block p V q hq t ht]
  rfl

theorem curved_c1_null_flow_control :
    ∃ V : LocalPhaseFlow (geodesicSpray controlConformalConnection) (regularPhaseDomain univ)
      (0,horizonControlDirection),
      ContDiffOn ℝ 1 V.flow
        (Metric.ball (0,horizonControlDirection) V.radius ×ˢ Ioo (-V.radius) V.radius) ∧
      (∀ t∈Ioo (-V.radius) V.radius,
        tensorQuad (controlConformalMetric (V.flow ((0,horizonControlDirection),t)).1)
          (V.flow ((0,horizonControlDirection),t)).2=0) ∧
      HasDerivAt (fun t => (V.flow ((0,horizonControlDirection),t)).2)
        ((-2:ℝ) • horizonControlDirection) 0 := by
  have hv : horizonControlDirection≠0 := by
    intro he
    have h0 := congrArg (fun v : Coordinate4 => v 0) he
    norm_num [horizonControlDirection] at h0
  let V := c1GeodesicFlow univ isOpen_univ controlConformalConnection
    Screen014.expanding_connection_smooth 0 horizonControlDirection (mem_univ _) hv
  have hp : ((0:Coordinate4),horizonControlDirection)∈
      Metric.ball ((0:Coordinate4),horizonControlDirection) V.radius :=
    Metric.mem_ball_self V.radius_positive
  have hn : tensorQuad (controlConformalMetric 0) horizonControlDirection=0 := by
    simpa [Screen014.expandingNullVelocity,Screen014.expandingFactor] using
      Screen014.expanding_velocity_null 0
  refine ⟨V,c1_geodesic_flow_joint_c1 univ isOpen_univ controlConformalConnection
    Screen014.expanding_connection_smooth 0 horizonControlDirection (mem_univ _) hv,?_,?_⟩
  · intro t ht
    exact geodesic_flow_null_preserved univ isOpen_univ controlConformalMetric
      controlConformalConnection Screen014.expanding_metric_smooth Screen014.expanding_connection_compatible
      (0,horizonControlDirection) V (0,horizonControlDirection) hp hn t ht
  · have hd := geodesic_flow_velocity_derivative univ controlConformalConnection
      (0,horizonControlDirection) V (0,horizonControlDirection) hp 0
      ⟨neg_neg_of_pos V.radius_positive,V.radius_positive⟩
    rw [V.initial _ hp,conformal_spray_acceleration_zero] at hd
    exact hd

#print axioms linear_taylor_remainder_zero
#print axioms zero_field_flow_constant
#print axioms zero_field_variation_identity
#print axioms flat_geodesic_initial_derivative
#print axioms flat_variation_block
#print axioms flat_variation_on_perturbation
#print axioms curved_c1_null_flow_control
end
end ChatgptAudit.Flow016
