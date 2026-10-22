-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_014 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.CovariantNullPreservation
import Mathlib.Analysis.ODE.ExistUnique
import Mathlib.Analysis.Matrix.Normed

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Screen014
open Matrix Filter Topology Set
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

abbrev FrameFlowState := Coordinate4 × Tensor4

def transportGenerator (Gamma : ConnectionField4) (V : VectorField4) (x : Coordinate4) : Tensor4 :=
  covariantVectorGradient Gamma V x-connectionAlong Gamma x (V x)

def coupledFrameField (V : VectorField4) (A : TensorField4) (p : FrameFlowState) : FrameFlowState :=
  (V p.1,A p.1*p.2)

theorem transport_generator_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V) :
    SmoothMatrixOn U (transportGenerator Gamma V) := by
  have hB := covariantVectorGradient_smooth U hU Gamma V hG hV
  intro a b
  have hL : ContDiffOn ℝ ∞ (fun x => connectionAlong Gamma x (V x) a b) U := by
    change ContDiffOn ℝ ∞ (fun x => ∑ i, V x i*Gamma x i a b) U
    unfold SmoothVectorOn at hV
    unfold SmoothConnectionOn SmoothMatrixOn at hG
    fun_prop
  exact (hB a b).sub hL

theorem coupled_frame_field_c1 (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (A : TensorField4) (hV : SmoothVectorOn U V)
    (hA : SmoothMatrixOn U A) (x : Coordinate4) (hx : x∈U) (F : Tensor4) :
    ContDiffAt ℝ 1 (coupledFrameField V A) (x,F) := by
  have hv (a : Fin 4) : ContDiffAt ℝ 1 (fun p : FrameFlowState => V p.1 a) (x,F) :=
    (((hV a x hx).contDiffAt (hU.mem_nhds hx)).of_le (by simp)).comp (x,F) contDiffAt_fst
  have ha (a b : Fin 4) : ContDiffAt ℝ 1 (fun p : FrameFlowState => A p.1 a b) (x,F) :=
    (((hA a b x hx).contDiffAt (hU.mem_nhds hx)).of_le (by simp)).comp (x,F) contDiffAt_fst
  have hf (a b : Fin 4) : ContDiffAt ℝ 1 (fun p : FrameFlowState => p.2 a b) (x,F) := by
    fun_prop
  apply ContDiffAt.prodMk (contDiffAt_pi.2 hv)
  apply contDiffAt_pi.2
  intro a
  apply contDiffAt_pi.2
  intro b
  change ContDiffAt ℝ 1 (fun p : FrameFlowState => ∑ i, A p.1 a i*p.2 i b) (x,F)
  simp only [Fin.sum_univ_four]
  exact ((((ha a 0).mul (hf 0 b)).add ((ha a 1).mul (hf 1 b))).add
    ((ha a 2).mul (hf 2 b))).add ((ha a 3).mul (hf 3 b))

theorem eventually_symmetric_interval (P : ℝ → Prop) (hP : ∀ᶠ t in 𝓝 (0:ℝ), P t) :
    ∃ radius > (0:ℝ), ∀ t∈Ioo (-radius) radius, P t := by
  obtain ⟨radius,hr,hball⟩ := Metric.mem_nhds_iff.mp hP
  refine ⟨radius,hr,?_⟩
  intro t ht
  apply hball
  simpa only [Metric.mem_ball,Real.dist_eq,sub_zero,abs_lt,Set.mem_Ioo] using ht

theorem matrix_derivative_components (F : ℝ → Tensor4) (dF : Tensor4) (t : ℝ)
    (hF : HasDerivAt F dF t) : HasMatrixDerivAt F dF t := by
  intro a b
  exact hasDerivAt_pi.mp (hasDerivAt_pi.mp hF a) b

structure LocalFrameFlow (U : Set Coordinate4) (V : VectorField4) (A : TensorField4)
    (x : Coordinate4) (F : Tensor4) where
  radius : ℝ
  radius_positive : 0 < radius
  curve : ℝ → Coordinate4
  frame : ℝ → Tensor4
  curve_zero : curve 0=x
  frame_zero : frame 0=F
  curve_mem : ∀ t∈Ioo (-radius) radius, curve t∈U
  tangent : ∀ t∈Ioo (-radius) radius, HasDerivAt curve (V (curve t)) t
  transport : ∀ t∈Ioo (-radius) radius, HasMatrixDerivAt frame (A (curve t)*frame t) t

def localFrameFlow (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (A : TensorField4) (hV : SmoothVectorOn U V)
    (hA : SmoothMatrixOn U A) (x : Coordinate4) (hx : x∈U) (F : Tensor4) :
    LocalFrameFlow U V A x F := by
  apply Classical.choice
  obtain ⟨alpha,ha0,epsilon,he,halpha⟩ :=
    (coupled_frame_field_c1 U hU V A hV hA x hx F).exists_forall_mem_closedBall_exists_eq_forall_mem_Ioo_hasDerivAt₀ 0
  have h0 : (0:ℝ)∈Ioo (0-epsilon) (0+epsilon) := by constructor <;> linarith
  have hcont : ContinuousAt (fun t => (alpha t).1) 0 :=
    continuous_fst.continuousAt.comp (halpha 0 h0).continuousAt
  have hmem : ∀ᶠ t in 𝓝 (0:ℝ), (alpha t).1∈U := by
    apply hcont.eventually
    change U∈𝓝 ((alpha 0).1)
    rw [ha0]
    exact hU.mem_nhds hx
  have hg : ∀ᶠ t in 𝓝 (0:ℝ), t∈Ioo (0-epsilon) (0+epsilon) ∧ (alpha t).1∈U := by
    filter_upwards [Ioo_mem_nhds h0.1 h0.2,hmem] with t ht hm
    exact ⟨ht,hm⟩
  obtain ⟨r,hr,hgood⟩ := eventually_symmetric_interval _ hg
  refine ⟨{
    radius := r
    radius_positive := hr
    curve := fun t => (alpha t).1
    frame := fun t => (alpha t).2
    curve_zero := congrArg Prod.fst ha0
    frame_zero := congrArg Prod.snd ha0
    curve_mem := fun t ht => (hgood t ht).2
    tangent := ?_
    transport := ?_ }⟩
  · intro t ht
    exact (ContinuousLinearMap.fst ℝ Coordinate4 Tensor4).hasFDerivAt.comp_hasDerivAt t
      (halpha t (hgood t ht).1)
  · intro t ht
    apply matrix_derivative_components
    exact (ContinuousLinearMap.snd ℝ Coordinate4 Tensor4).hasFDerivAt.comp_hasDerivAt t
      (halpha t (hgood t ht).1)

theorem local_frame_flow_continuous_zero (U : Set Coordinate4) (V : VectorField4)
    (A : TensorField4) (x : Coordinate4) (F : Tensor4) (P : LocalFrameFlow U V A x F) :
    ContinuousAt P.curve 0 ∧ (∀ a b, ContinuousAt (fun t => P.frame t a b) 0) := by
  have h0 : (0:ℝ)∈Ioo (-P.radius) P.radius :=
    ⟨neg_neg_of_pos P.radius_positive,P.radius_positive⟩
  exact ⟨(P.tangent 0 h0).continuousAt,fun a b => (P.transport 0 h0 a b).continuousAt⟩

theorem ordinary_velocity_generator (Gamma : ConnectionField4) (V : VectorField4)
    (x : Coordinate4) (a : Fin 4) :
    fderiv ℝ (fun y => V y a) x (V x)=(transportGenerator Gamma V x).mulVec (V x) a := by
  rw [← scalarAlong_eq_fderiv V (fun y => V y a) x]
  simp only [scalarAlong,transportGenerator,covariantVectorGradient,covariantVectorDerivative,
    vectorPartial,connectionAlong,Matrix.mulVec,dotProduct,Matrix.sub_apply,Matrix.add_apply,
    Matrix.smul_apply,smul_eq_mul,Pi.add_apply,Fin.sum_univ_four]
  ring

theorem velocity_along_flow_derivative (Gamma : ConnectionField4) (V : VectorField4)
    (curve : ℝ → Coordinate4) (t : ℝ)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) (curve t))
    (hc : HasDerivAt curve (V (curve t)) t) :
    HasDerivAt (fun s => V (curve s))
      ((transportGenerator Gamma V (curve t)).mulVec (V (curve t))) t := by
  apply hasDerivAt_pi.2
  intro a
  have hd := (hV a).hasFDerivAt.comp_hasDerivAt t hc
  rw [ordinary_velocity_generator] at hd
  exact hd

#print axioms transport_generator_smooth
#print axioms coupled_frame_field_c1
#print axioms eventually_symmetric_interval
#print axioms matrix_derivative_components
#print axioms localFrameFlow
#print axioms local_frame_flow_continuous_zero
#print axioms ordinary_velocity_generator
#print axioms velocity_along_flow_derivative
end
end ChatgptAudit.Screen014
