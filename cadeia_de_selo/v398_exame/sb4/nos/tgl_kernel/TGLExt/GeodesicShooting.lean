-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_018 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.TransverseInitialData

set_option autoImplicit false
set_option maxHeartbeats 7000000
namespace ChatgptAudit.Flow018
open Matrix Filter Topology Set ChatgptAudit.Flow016 ChatgptAudit.Flow017 ChatgptAudit.Screen015
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def shootingInput (p v : Coordinate4) (ell : Coordinate4 →L[ℝ] ℝ) (W : VectorField4)
    (z : Coordinate4) : Phase4 × ℝ :=
  ((initialPosition p v ell z,W (initialPosition p v ell z)),ell z)

variable {U : Set Coordinate4} {Gamma : ConnectionField4} {p v : Coordinate4}
  (F : LipschitzLocalFlow (variationalField (geodesicSpray Gamma))
    (variationalDomain (regularPhaseDomain U)) ((p,v),ContinuousLinearMap.id ℝ Phase4))
  (ell : Coordinate4 →L[ℝ] ℝ) (W : VectorField4)

def shootingPhase (z : Coordinate4) : Phase4 :=
  flowSolution F (shootingInput p v ell W z).1 (shootingInput p v ell W z).2

def shootingPosition (z : Coordinate4) : Coordinate4 := (shootingPhase F ell W z).1
def shootingVelocity (z : Coordinate4) : Coordinate4 := (shootingPhase F ell W z).2

def shootingDomain : Set Coordinate4 :=
  interior {z | initialPosition p v ell z∈U ∧
    shootingInput p v ell W z∈Metric.ball (p,v) F.radius ×ˢ Ioo (-F.radius) F.radius}

theorem shooting_input_zero (p v : Coordinate4) (ell : Coordinate4 →L[ℝ] ℝ)
    (W : VectorField4) (hWp : W p=v) :
    shootingInput p v ell W 0=((p,v),(0:ℝ)) := by
  simp [shootingInput,initialPosition,hWp]

theorem shooting_phase_zero (hWp : W p=v) : shootingPhase F ell W 0=(p,v) := by
  simp only [shootingPhase,shooting_input_zero p v ell W hWp]
  exact flow_solution_initial F (p,v) (Metric.mem_ball_self F.radius_positive)

theorem shooting_domain_open : IsOpen (shootingDomain F ell W) := isOpen_interior

theorem shooting_domain_zero (hU : IsOpen U) (hW : ContDiffOn ℝ ∞ W U)
    (hp : p∈U) (hWp : W p=v) : (0:Coordinate4)∈shootingDomain F ell W := by
  have hP := (initial_position_smooth p v ell).continuous.continuousAt (x := (0:Coordinate4))
  have hWpC : ContinuousAt W (initialPosition p v ell 0) := by
    simpa only [initialPosition,map_zero,add_zero] using
      ((hW p hp).contDiffAt (hU.mem_nhds hp)).continuousAt
  have hI : ContinuousAt (shootingInput p v ell W) 0 :=
    (hP.prodMk (hWpC.comp (f := initialPosition p v ell) hP)).prodMk ell.continuous.continuousAt
  have hDU : U∈𝓝 (initialPosition p v ell 0) := by
    simpa only [initialPosition,map_zero,add_zero] using hU.mem_nhds hp
  have hDF : Metric.ball (p,v) F.radius ×ˢ Ioo (-F.radius) F.radius∈𝓝 (shootingInput p v ell W 0) := by
    rw [shooting_input_zero p v ell W hWp]
    exact (Metric.isOpen_ball.prod isOpen_Ioo).mem_nhds
      ⟨Metric.mem_ball_self F.radius_positive,neg_neg_of_pos F.radius_positive,F.radius_positive⟩
  apply mem_interior_iff_mem_nhds.2
  filter_upwards [hP.eventually hDU,hI.eventually hDF] with z hzU hzF
  exact ⟨hzU,hzF⟩

theorem shooting_input_smooth (hW : ContDiffOn ℝ ∞ W U) :
    ContDiffOn ℝ ∞ (shootingInput p v ell W) (shootingDomain F ell W) := by
  have hP : ContDiffOn ℝ ∞ (initialPosition p v ell) (shootingDomain F ell W) :=
    (initial_position_smooth p v ell).contDiffOn
  exact (hP.prodMk (hW.comp hP (fun _ hz => (interior_subset hz).1))).prodMk ell.contDiff.contDiffOn

theorem shooting_phase_smooth (hU : IsOpen U) (hG : SmoothConnectionOn U Gamma)
    (hW : ContDiffOn ℝ ∞ W U) :
    ContDiffOn ℝ ∞ (shootingPhase F ell W) (shootingDomain F ell W) := by
  have hs := flow_smooth_on_domain (projectedVariationalFlow F) (regular_phase_domain_open U hU)
    ((geodesic_spray_smooth U hU Gamma hG).mono (fun _ hz => hz.1))
  exact hs.comp (shooting_input_smooth F ell W hW) (fun _ hz => (interior_subset hz).2)

theorem shooting_regular (z : Coordinate4) (hz : z∈shootingDomain F ell W) :
    shootingPosition F ell W z∈U ∧ shootingVelocity F ell W z≠0 := by
  have hd := (interior_subset hz).2
  exact flow_solution_stays F (shootingInput p v ell W z).1 hd.1 (shootingInput p v ell W z).2 hd.2

theorem shooting_null (g : TensorField4) (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hm : MetricCompatibleOn U g Gamma)
    (hn : ∀ x∈U, tensorQuad (g x) (W x)=0)
    (z : Coordinate4) (hz : z∈shootingDomain F ell W) :
    tensorQuad (g (shootingPosition F ell W z)) (shootingVelocity F ell W z)=0 := by
  have hd := (interior_subset hz).2
  exact geodesic_flow_null_preserved U hU g Gamma hg hm (p,v) (phaseFlowOfVariational F)
    (shootingInput p v ell W z).1 hd.1
    (hn (initialPosition p v ell z) (interior_subset hz).1)
    (shootingInput p v ell W z).2 hd.2


theorem shooting_position_derivative_zero (hU : IsOpen U) (hG : SmoothConnectionOn U Gamma)
    (hW : ContDiffOn ℝ ∞ W U) (hp : p∈U) (hWp : W p=v) :
    HasFDerivAt (shootingPosition F ell W) (ContinuousLinearMap.id ℝ Coordinate4) 0 := by
  let P := transverseProjection v ell
  let L := (P.prod ((fderiv ℝ W p).comp P)).prod ell
  have hP : HasFDerivAt (initialPosition p v ell) P 0 := P.hasFDerivAt.const_add p
  have hWd : HasFDerivAt W (fderiv ℝ W p) (initialPosition p v ell 0) := by
    simpa only [initialPosition,map_zero,add_zero] using
      (((hW p hp).contDiffAt (hU.mem_nhds hp)).differentiableAt (by simp)).hasFDerivAt
  have hI : HasFDerivAt (shootingInput p v ell W) L 0 :=
    (hP.prodMk (hWd.comp 0 hP)).prodMk ell.hasFDerivAt
  have hbase : (p,v)∈Metric.ball (p,v) F.radius := Metric.mem_ball_self F.radius_positive
  have hzero : (0:ℝ)∈Ioo (-F.radius) F.radius :=
    ⟨neg_neg_of_pos F.radius_positive,F.radius_positive⟩
  have hFlow : HasFDerivAt (fun z : Phase4 × ℝ => flowSolution F z.1 z.2)
      (flowJointDerivative F (p,v) 0) (shootingInput p v ell W 0) := by
    rw [shooting_input_zero p v ell W hWp]
    exact (flow_joint_hasStrictFDerivAt F (regular_phase_domain_open U hU)
      ((geodesic_spray_smooth U hU Gamma hG).mono (fun _ hz => hz.1)) (p,v) hbase 0 hzero).hasFDerivAt
  have hd : HasFDerivAt (shootingPosition F ell W)
      ((ContinuousLinearMap.fst ℝ Coordinate4 Coordinate4).comp
        ((flowJointDerivative F (p,v) 0).comp L)) 0 :=
    (ContinuousLinearMap.fst ℝ Coordinate4 Coordinate4).hasFDerivAt.comp 0 (hFlow.comp 0 hI)
  have he : (ContinuousLinearMap.fst ℝ Coordinate4 Coordinate4).comp
      ((flowJointDerivative F (p,v) 0).comp L)=ContinuousLinearMap.id ℝ Coordinate4 := by
    apply ContinuousLinearMap.ext
    intro h
    change ((flowJointDerivative F (p,v) 0) (L h)).1=h
    simp only [flowJointDerivative,ContinuousLinearMap.coprod_apply,
      flow_variation_initial F (p,v) hbase,flow_solution_initial F (p,v) hbase]
    change P h+ell h • v=h
    exact transverse_projection_decomposition v ell h
  rwa [he] at hd

theorem shooting_position_along_time (hell : ell v=1)
    (z : Coordinate4) (hz : z∈shootingDomain F ell W) :
    HasDerivAt (fun s : ℝ => shootingPosition F ell W (z+s • v))
      (shootingVelocity F ell W z) 0 := by
  have hd := (interior_subset hz).2
  have hder := geodesic_flow_position_derivative U Gamma (p,v) (phaseFlowOfVariational F)
    (shootingInput p v ell W z).1 hd.1 (ell z) hd.2
  have ht : HasDerivAt (fun s : ℝ => ell z+s) 1 0 :=
    (hasDerivAt_id 0).const_add (ell z)
  have hh := hder.scomp_of_eq 0 ht (by simp)
  have heq : (fun s : ℝ => shootingPosition F ell W (z+s • v)) =
      (fun s : ℝ => (flowSolution F (shootingInput p v ell W z).1 (ell z+s)).1) := by
    funext s
    simp only [shootingPosition,shootingPhase,shootingInput,
      initial_position_shift p v ell hell z s,initial_time_shift v ell hell z s]
  rw [heq]
  convert hh using 1 <;> first | rfl | (simp only [one_smul]; rfl)

theorem shooting_velocity_along_time (hell : ell v=1)
    (z : Coordinate4) (hz : z∈shootingDomain F ell W) :
    HasDerivAt (fun s : ℝ => shootingVelocity F ell W (z+s • v))
      (sprayAcceleration Gamma (shootingPosition F ell W z) (shootingVelocity F ell W z)) 0 := by
  have hd := (interior_subset hz).2
  have hder := geodesic_flow_velocity_derivative U Gamma (p,v) (phaseFlowOfVariational F)
    (shootingInput p v ell W z).1 hd.1 (ell z) hd.2
  have ht : HasDerivAt (fun s : ℝ => ell z+s) 1 0 :=
    (hasDerivAt_id 0).const_add (ell z)
  have hh := hder.scomp_of_eq 0 ht (by simp)
  have heq : (fun s : ℝ => shootingVelocity F ell W (z+s • v)) =
      (fun s : ℝ => (flowSolution F (shootingInput p v ell W z).1 (ell z+s)).2) := by
    funext s
    simp only [shootingVelocity,shootingPhase,shootingInput,
      initial_position_shift p v ell hell z s,initial_time_shift v ell hell z s]
  rw [heq]
  convert hh using 1 <;> first | rfl | (simp only [one_smul]; rfl)

#print axioms shooting_position_derivative_zero
#print axioms shooting_position_along_time
#print axioms shooting_velocity_along_time

#print axioms shooting_input_zero
#print axioms shooting_phase_zero
#print axioms shooting_domain_open
#print axioms shooting_domain_zero
#print axioms shooting_input_smooth
#print axioms shooting_phase_smooth
#print axioms shooting_regular
#print axioms shooting_null
end
end ChatgptAudit.Flow018
