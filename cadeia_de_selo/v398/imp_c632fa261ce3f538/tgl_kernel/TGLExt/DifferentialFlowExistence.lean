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
import TGLExt.GeodesicFlowControls

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Flow016
open Filter Topology Set
open scoped ContDiff
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]

omit [NormedSpace ℝ E] [CompleteSpace E] in
theorem eventually_flow_rectangle (p : E) (P : E × ℝ → Prop)
    (hP : ∀ᶠ z in 𝓝 (p,(0:ℝ)), P z) :
    ∃ radius > (0:ℝ), ∀ q∈Metric.ball p radius, ∀ t∈Ioo (-radius) radius, P (q,t) := by
  obtain ⟨radius,hr,hball⟩ := Metric.mem_nhds_iff.mp hP
  refine ⟨radius,hr,?_⟩
  intro q hq t ht
  apply hball
  rw [Metric.mem_ball,Prod.dist_eq]
  apply max_lt
  · exact hq
  · simpa only [Real.dist_eq,sub_zero,abs_lt,Set.mem_Ioo] using ht

structure LipschitzLocalFlow (f : E → E) (Q : Set E) (p : E) where
  radius : ℝ
  radius_positive : 0 < radius
  constant : NNReal
  flow : E × ℝ → E
  initial : ∀ q∈Metric.ball p radius, flow (q,0)=q
  derivative : ∀ q∈Metric.ball p radius, ∀ t∈Ioo (-radius) radius,
    HasDerivAt (fun s => flow (q,s)) (f (flow (q,t))) t
  stays : ∀ q∈Metric.ball p radius, ∀ t∈Ioo (-radius) radius, flow (q,t)∈Q
  continuous : ContinuousOn flow (Metric.ball p radius ×ˢ Ioo (-radius) radius)
  lipschitz : ∀ t∈Ioo (-radius) radius,
    LipschitzOnWith constant (fun q => flow (q,t)) (Metric.ball p radius)

def lipschitzLocalFlow (Q : Set E) (hQ : IsOpen Q) (f : E → E)
    (p : E) (hp : p∈Q) (hf : ContDiffAt ℝ 1 f p) : LipschitzLocalFlow f Q p := by
  apply Classical.choice
  obtain ⟨epsilon,hepsilon,a,r,L,K,hr,hpl⟩ := IsPicardLindelof.of_contDiffAt_one hf
  obtain ⟨alpha,halpha,constant,hlip⟩ :=
    (hpl 0).exists_forall_mem_closedBall_eq_hasDerivWithinAt_lipschitzOnWith
  simp only [zero_sub,zero_add] at halpha hlip
  have hcont : ContinuousOn (Function.uncurry alpha)
      (Metric.closedBall p (r:ℝ) ×ˢ Icc (-epsilon) epsilon) := by
    apply continuousOn_prod_of_continuousOn_lipschitzOnWith _ constant _ hlip
    exact fun q hq => HasDerivWithinAt.continuousOn (halpha q hq).2
  let flow : E × ℝ → E := Function.uncurry alpha
  have h0 : (0:ℝ)∈Ioo (-epsilon) epsilon :=
    ⟨neg_neg_of_pos hepsilon,hepsilon⟩
  have hc : p∈Metric.closedBall p (r:ℝ) := Metric.mem_closedBall_self hr.le
  have ha0 : flow (p,0)=p := (halpha p hc).1
  have hbase : (p,(0:ℝ))∈Metric.ball p (r:ℝ) ×ˢ Ioo (-epsilon) epsilon :=
    ⟨Metric.mem_ball_self hr,h0⟩
  have hopen : IsOpen (Metric.ball p (r:ℝ) ×ˢ Ioo (-epsilon) epsilon) :=
    Metric.isOpen_ball.prod isOpen_Ioo
  have hdom : Metric.closedBall p (r:ℝ) ×ˢ Icc (-epsilon) epsilon∈𝓝 (p,(0:ℝ)) :=
    Filter.mem_of_superset (hopen.mem_nhds hbase)
      (Set.prod_mono Metric.ball_subset_closedBall Ioo_subset_Icc_self)
  have hca : ContinuousAt flow (p,(0:ℝ)) := hcont.continuousAt hdom
  have hst : ∀ᶠ z in 𝓝 (p,(0:ℝ)), flow z∈Q := by
    apply hca.eventually
    rw [ha0]
    exact hQ.mem_nhds hp
  have hgood : ∀ᶠ z in 𝓝 (p,(0:ℝ)),
      z∈Metric.ball p (r:ℝ) ×ˢ Ioo (-epsilon) epsilon ∧ flow z∈Q := by
    filter_upwards [hopen.mem_nhds hbase,hst] with z hz hq
    exact ⟨hz,hq⟩
  obtain ⟨radius,hradius,hrect⟩ := eventually_flow_rectangle p _ hgood
  have hz : (0:ℝ)∈Ioo (-radius) radius :=
    ⟨neg_neg_of_pos hradius,hradius⟩
  refine ⟨{
    radius := radius
    radius_positive := hradius
    constant := constant
    flow := flow
    initial := ?_
    derivative := ?_
    stays := ?_
    continuous := ?_
    lipschitz := ?_ }⟩
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
  · intro t ht
    have htt := (hrect p (Metric.mem_ball_self hradius) t ht).1.2
    apply (hlip t (Ioo_subset_Icc_self htt)).mono
    intro q hq
    exact Metric.ball_subset_closedBall (hrect q hq 0 hz).1.1

omit [CompleteSpace E] in
theorem flow_initial_distance_bound (f : E → E) (Q : Set E) (p : E)
    (F : LipschitzLocalFlow f Q p) (q r : E)
    (hq : q∈Metric.ball p F.radius) (hr : r∈Metric.ball p F.radius)
    (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    ‖F.flow (q,t)-F.flow (r,t)‖ ≤ F.constant*‖q-r‖ := by
  simpa only [dist_eq_norm] using (F.lipschitz t ht).dist_le_mul q hq r hr

omit [CompleteSpace E] in
theorem flow_joint_continuous_at (f : E → E) (Q : Set E) (p : E)
    (F : LipschitzLocalFlow f Q p) (q : E) (hq : q∈Metric.ball p F.radius)
    (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) : ContinuousAt F.flow (q,t) :=
  F.continuous.continuousAt ((Metric.isOpen_ball.prod isOpen_Ioo).mem_nhds ⟨hq,ht⟩)

#print axioms eventually_flow_rectangle
#print axioms lipschitzLocalFlow
#print axioms flow_initial_distance_bound
#print axioms flow_joint_continuous_at
end
end ChatgptAudit.Flow016
