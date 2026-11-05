-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_015 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.GeodesicFlowRegularity
import TGLExt.TransportedScreenControls

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Screen015
open Matrix TGLExt Filter Topology Set
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem zero_connection_velocity_constant (p : Phase4)
    (F : LocalPhaseFlow (geodesicSpray (fun _ => 0)) (regularPhaseDomain univ) p)
    (q : Phase4) (hq : q∈Metric.ball p F.radius) (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    (F.flow (q,t)).2=q.2 := by
  have hd (s : ℝ) (hs : s∈Ioo (-F.radius) F.radius) :
      HasDerivAt (fun a => (F.flow (q,a)).2) 0 s := by
    have hv := geodesic_flow_velocity_derivative univ (fun _ => 0) p F q hq s hs
    simpa [sprayAcceleration,connectionAlong] using hv
  have h0 : (0:ℝ)∈Ioo (-F.radius) F.radius :=
    ⟨neg_neg_of_pos F.radius_positive,F.radius_positive⟩
  have he := isOpen_Ioo.is_const_of_deriv_eq_zero isPreconnected_Ioo
    (fun s hs => (hd s hs).differentiableAt.differentiableWithinAt)
    (fun s hs => (hd s hs).deriv) ht h0
  simpa only [F.initial q hq] using he

theorem zero_connection_position_affine (p : Phase4)
    (F : LocalPhaseFlow (geodesicSpray (fun _ => 0)) (regularPhaseDomain univ) p)
    (q : Phase4) (hq : q∈Metric.ball p F.radius) (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    (F.flow (q,t)).1=q.1+t • q.2 := by
  ext j
  have hd (s : ℝ) (hs : s∈Ioo (-F.radius) F.radius) :
      HasDerivAt (fun a => (F.flow (q,a)).1 j-a*q.2 j) 0 s := by
    have hp := geodesic_flow_position_derivative univ (fun _ => 0) p F q hq s hs
    rw [zero_connection_velocity_constant p F q hq s hs] at hp
    have ht' : HasDerivAt (fun a : ℝ => a*q.2 j) (q.2 j) s := by
      simpa only [one_mul,id_eq] using (hasDerivAt_id s).mul_const (q.2 j)
    convert (hasDerivAt_pi.mp hp j).sub ht' using 1 <;> first | rfl | simp only [sub_self]
  have h0 : (0:ℝ)∈Ioo (-F.radius) F.radius :=
    ⟨neg_neg_of_pos F.radius_positive,F.radius_positive⟩
  have he := isOpen_Ioo.is_const_of_deriv_eq_zero isPreconnected_Ioo
    (fun s hs => (hd s hs).differentiableAt.differentiableWithinAt)
    (fun s hs => (hd s hs).deriv) ht h0
  have hdiff : (F.flow (q,t)).1 j-t*q.2 j=q.1 j := by
    simpa only [F.initial q hq,zero_mul,sub_zero] using he
  exact sub_eq_iff_eq_add.mp hdiff

theorem flat_geodesic_flow_control (x v : Coordinate4) (hv : v≠0) :
    ∃ F : LocalPhaseFlow (geodesicSpray (fun _ => 0)) (regularPhaseDomain univ) (x,v),
      ∀ q∈Metric.ball (x,v) F.radius, ∀ t∈Ioo (-F.radius) F.radius,
        F.flow (q,t)=(q.1+t • q.2,q.2) := by
  let F := localGeodesicFlow univ isOpen_univ (fun _ => 0)
    (fun _ _ _ => contDiffOn_const) x v (mem_univ _) hv
  refine ⟨F,?_⟩
  intro q hq t ht
  exact Prod.ext (zero_connection_position_affine (x,v) F q hq t ht)
    (zero_connection_velocity_constant (x,v) F q hq t ht)

theorem phase_flow_cannot_assign_one_field (f : Phase4 → Phase4) (Q : Set Phase4)
    (p : Phase4) (F : LocalPhaseFlow f Q p) :
    ¬ ∃ V : VectorField4, ∀ q∈Metric.ball p F.radius,
      V (F.flow (q,0)).1=(F.flow (q,0)).2 := by
  let q : Phase4 := (p.1,p.2+Pi.single (0:Fin 4) (F.radius/2))
  have hq : q∈Metric.ball p F.radius := by
    rw [Metric.mem_ball,Prod.dist_eq]
    apply max_lt
    · simpa only [q,dist_self] using F.radius_positive
    · rw [dist_pi_lt_iff F.radius_positive]
      intro i
      by_cases hi : i=0
      · subst i
        simp only [q,Pi.add_apply,Pi.single_eq_same,Real.dist_eq,add_sub_cancel_left,
          abs_of_pos (half_pos F.radius_positive)]
        linarith [F.radius_positive]
      · simp [q,hi,F.radius_positive]
  have hv : p.2≠q.2 := by
    intro he
    have ha := congrArg (fun w : Coordinate4 => w 0) he
    simp only [q,Pi.add_apply,Pi.single_eq_same] at ha
    linarith [F.radius_positive]
  rintro ⟨V,hV⟩
  exact phase_initial_data_obstruction f Q p F p q
    (Metric.mem_ball_self F.radius_positive) hq rfl hv
    ⟨V,hV p (Metric.mem_ball_self F.radius_positive),hV q hq⟩

theorem conformal_spray_acceleration_zero :
    sprayAcceleration controlConformalConnection 0 horizonControlDirection=
      (-2:ℝ) • horizonControlDirection := by
  ext a
  fin_cases a <;>
    norm_num [sprayAcceleration,connectionAlong,horizonControlDirection,controlConformalConnection,
      Matrix.mulVec,dotProduct,Fin.sum_univ_four,Matrix.add_apply,Matrix.smul_apply,
      Matrix.cons_val_two,Matrix.cons_val_three,Fin.isValue]

theorem conformal_spray_acceleration_nonzero :
    sprayAcceleration controlConformalConnection 0 horizonControlDirection≠0 := by
  rw [conformal_spray_acceleration_zero]
  intro he
  have h0 := congrArg (fun v : Coordinate4 => v 0) he
  norm_num [horizonControlDirection] at h0

theorem curved_null_geodesic_flow_control :
    ∃ F : LocalPhaseFlow (geodesicSpray controlConformalConnection) (regularPhaseDomain univ)
      (0,horizonControlDirection),
      (∀ t∈Ioo (-F.radius) F.radius,
        tensorQuad (controlConformalMetric (F.flow ((0,horizonControlDirection),t)).1)
          (F.flow ((0,horizonControlDirection),t)).2=0) ∧
      HasDerivAt (fun t => (F.flow ((0,horizonControlDirection),t)).2)
        ((-2:ℝ) • horizonControlDirection) 0 := by
  have hv : horizonControlDirection≠0 := by
    intro he
    have h0 := congrArg (fun v : Coordinate4 => v 0) he
    norm_num [horizonControlDirection] at h0
  let F := localGeodesicFlow univ isOpen_univ controlConformalConnection
    Screen014.expanding_connection_smooth 0 horizonControlDirection (mem_univ _) hv
  have hp : ((0:Coordinate4),horizonControlDirection)∈Metric.ball ((0:Coordinate4),horizonControlDirection) F.radius :=
    Metric.mem_ball_self F.radius_positive
  have hn : tensorQuad (controlConformalMetric 0) horizonControlDirection=0 := by
    simpa [Screen014.expandingNullVelocity,Screen014.expandingFactor] using
      Screen014.expanding_velocity_null 0
  refine ⟨F,?_,?_⟩
  · intro t ht
    exact geodesic_flow_null_preserved univ isOpen_univ controlConformalMetric
      controlConformalConnection Screen014.expanding_metric_smooth Screen014.expanding_connection_compatible
      (0,horizonControlDirection) F (0,horizonControlDirection) hp hn t ht
  · have hd := geodesic_flow_velocity_derivative univ controlConformalConnection
      (0,horizonControlDirection) F (0,horizonControlDirection) hp 0
      ⟨neg_neg_of_pos F.radius_positive,F.radius_positive⟩
    rw [F.initial _ hp,conformal_spray_acceleration_zero] at hd
    exact hd

theorem curved_flow_background_nonzero :
    coordinateCurvature controlConformalConnection (0:Coordinate4) 1 2 1 2=1 :=
  Screen014.expanding_background_curvature

#print axioms zero_connection_velocity_constant
#print axioms zero_connection_position_affine
#print axioms flat_geodesic_flow_control
#print axioms phase_flow_cannot_assign_one_field
#print axioms conformal_spray_acceleration_zero
#print axioms conformal_spray_acceleration_nonzero
#print axioms curved_null_geodesic_flow_control
#print axioms curved_flow_background_nonzero
end
end ChatgptAudit.Screen015
