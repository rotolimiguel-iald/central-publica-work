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
import TGLExt.GeodesicSpray

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Screen015
open Matrix Filter Topology Set
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

structure LocalPhaseFlow (f : Phase4 → Phase4) (Q : Set Phase4) (p : Phase4) where
  radius : ℝ
  radius_positive : 0 < radius
  flow : Phase4 × ℝ → Phase4
  initial : ∀ q∈Metric.ball p radius, flow (q,0)=q
  derivative : ∀ q∈Metric.ball p radius, ∀ t∈Ioo (-radius) radius,
    HasDerivAt (fun s => flow (q,s)) (f (flow (q,t))) t
  stays : ∀ q∈Metric.ball p radius, ∀ t∈Ioo (-radius) radius, flow (q,t)∈Q
  continuous : ContinuousOn flow (Metric.ball p radius ×ˢ Ioo (-radius) radius)

def localPhaseFlow (Q : Set Phase4) (hQ : IsOpen Q) (f : Phase4 → Phase4)
    (p : Phase4) (hp : p∈Q) (hf : ContDiffAt ℝ 1 f p) : LocalPhaseFlow f Q p := by
  apply Classical.choice
  obtain ⟨epsilon,hepsilon,a,r,L,K,hr,hpl⟩ := IsPicardLindelof.of_contDiffAt_one hf
  obtain ⟨alpha,halpha,hcont⟩ :=
    (hpl 0).exists_forall_mem_closedBall_eq_hasDerivWithinAt_continuousOn
  simp only [zero_sub,zero_add] at halpha hcont
  have h0 : (0:ℝ)∈Ioo (-epsilon) epsilon :=
    ⟨neg_neg_of_pos hepsilon,hepsilon⟩
  have hc : p∈Metric.closedBall p (r:ℝ) := Metric.mem_closedBall_self hr.le
  have ha0 : alpha (p,0)=p := (halpha p hc).1
  have hbase : (p,(0:ℝ))∈Metric.ball p (r:ℝ) ×ˢ Ioo (-epsilon) epsilon :=
    ⟨Metric.mem_ball_self hr,h0⟩
  have hopen : IsOpen (Metric.ball p (r:ℝ) ×ˢ Ioo (-epsilon) epsilon) :=
    Metric.isOpen_ball.prod isOpen_Ioo
  have hdom : Metric.closedBall p (r:ℝ) ×ˢ Icc (-epsilon) epsilon∈𝓝 (p,(0:ℝ)) :=
    Filter.mem_of_superset (hopen.mem_nhds hbase)
      (Set.prod_mono Metric.ball_subset_closedBall Ioo_subset_Icc_self)
  have hca : ContinuousAt alpha (p,(0:ℝ)) := hcont.continuousAt hdom
  have hst : ∀ᶠ z in 𝓝 (p,(0:ℝ)), alpha z∈Q := by
    apply hca.eventually
    rw [ha0]
    exact hQ.mem_nhds hp
  have hgood : ∀ᶠ z in 𝓝 (p,(0:ℝ)),
      z∈Metric.ball p (r:ℝ) ×ˢ Ioo (-epsilon) epsilon ∧ alpha z∈Q := by
    filter_upwards [hopen.mem_nhds hbase,hst] with z hz hq
    exact ⟨hz,hq⟩
  obtain ⟨radius,hradius,hrect⟩ := eventually_phase_rectangle p _ hgood
  have hz : (0:ℝ)∈Ioo (-radius) radius :=
    ⟨neg_neg_of_pos hradius,hradius⟩
  refine ⟨{
    radius := radius
    radius_positive := hradius
    flow := alpha
    initial := ?_
    derivative := ?_
    stays := ?_
    continuous := ?_ }⟩
  · intro q hq
    exact (halpha q (Metric.ball_subset_closedBall (hrect q hq 0 hz).1.1)).1
  · intro q hq t ht
    have hd := hrect q hq t ht
    have ha := (halpha q (Metric.ball_subset_closedBall hd.1.1)).2 t
      (Ioo_subset_Icc_self hd.1.2)
    exact ha.hasDerivAt (Icc_mem_nhds hd.1.2.1 hd.1.2.2)
  · intro q hq t ht
    exact (hrect q hq t ht).2
  · apply hcont.mono
    intro z hz'
    have hg := (hrect z.1 hz'.1 z.2 hz'.2).1
    exact ⟨Metric.ball_subset_closedBall hg.1,Ioo_subset_Icc_self hg.2⟩

def regularPhaseDomain (U : Set Coordinate4) : Set Phase4 :=
  phaseDomain U ∩ {p | p.2≠0}

theorem regular_phase_domain_open (U : Set Coordinate4) (hU : IsOpen U) :
    IsOpen (regularPhaseDomain U) :=
  (phase_domain_open U hU).inter (isOpen_ne_fun continuous_snd continuous_const)

def localGeodesicFlow (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (x v : Coordinate4) (hx : x∈U) (hv : v≠0) :
    LocalPhaseFlow (geodesicSpray Gamma) (regularPhaseDomain U) (x,v) :=
  localPhaseFlow (regularPhaseDomain U) (regular_phase_domain_open U hU)
    (geodesicSpray Gamma) (x,v) ⟨hx,hv⟩ (geodesic_spray_c1 U hU Gamma hG x v hx)

theorem geodesic_flow_position_derivative (U : Set Coordinate4) (Gamma : ConnectionField4)
    (p : Phase4) (F : LocalPhaseFlow (geodesicSpray Gamma) (regularPhaseDomain U) p)
    (q : Phase4) (hq : q∈Metric.ball p F.radius) (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    HasDerivAt (fun s => (F.flow (q,s)).1) (F.flow (q,t)).2 t :=
  (ContinuousLinearMap.fst ℝ Coordinate4 Coordinate4).hasFDerivAt.comp_hasDerivAt t
    (F.derivative q hq t ht)

theorem geodesic_flow_velocity_derivative (U : Set Coordinate4) (Gamma : ConnectionField4)
    (p : Phase4) (F : LocalPhaseFlow (geodesicSpray Gamma) (regularPhaseDomain U) p)
    (q : Phase4) (hq : q∈Metric.ball p F.radius) (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    HasDerivAt (fun s => (F.flow (q,s)).2)
      (sprayAcceleration Gamma (F.flow (q,t)).1 (F.flow (q,t)).2) t :=
  (ContinuousLinearMap.snd ℝ Coordinate4 Coordinate4).hasFDerivAt.comp_hasDerivAt t
    (F.derivative q hq t ht)

theorem geodesic_flow_regular (U : Set Coordinate4) (Gamma : ConnectionField4)
    (p : Phase4) (F : LocalPhaseFlow (geodesicSpray Gamma) (regularPhaseDomain U) p)
    (q : Phase4) (hq : q∈Metric.ball p F.radius) (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    (F.flow (q,t)).1∈U ∧ (F.flow (q,t)).2≠0 := F.stays q hq t ht

#print axioms localPhaseFlow
#print axioms regular_phase_domain_open
#print axioms localGeodesicFlow
#print axioms geodesic_flow_position_derivative
#print axioms geodesic_flow_velocity_derivative
#print axioms geodesic_flow_regular
end
end ChatgptAudit.Screen015
