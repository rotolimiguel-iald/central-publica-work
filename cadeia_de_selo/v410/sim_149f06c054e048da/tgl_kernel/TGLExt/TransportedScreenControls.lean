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
import TGLExt.TransportedScreenExistence
import TGLExt.ScreenImportIntegration

set_option autoImplicit false
set_option maxHeartbeats 6000000
set_option maxRecDepth 4096
namespace ChatgptAudit.Screen014
open Matrix TGLExt Filter Topology Set
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem zero_generator_frames_constant (V : VectorField4) (x : Coordinate4) (F : Tensor4)
    (P : LocalFrameFlow univ V (fun _ => 0) x F)
    (t : ℝ) (ht : t∈Ioo (-P.radius) P.radius) : P.frame t=F := by
  have h0 : (0:ℝ)∈Ioo (-P.radius) P.radius :=
    ⟨neg_neg_of_pos P.radius_positive,P.radius_positive⟩
  ext a b
  have hd (s : ℝ) (hs : s∈Ioo (-P.radius) P.radius) :
      HasDerivAt (fun r => P.frame r a b) 0 s := by
    have h := P.transport s hs a b
    simpa only [Matrix.zero_mul,Matrix.zero_apply] using h
  have he := isOpen_Ioo.is_const_of_deriv_eq_zero isPreconnected_Ioo
    (fun s hs => (hd s hs).differentiableAt.differentiableWithinAt)
    (fun s hs => (hd s hs).deriv) ht h0
  simpa only [P.frame_zero] using he

theorem flat_frame_flow_control :
    ∃ P : LocalFrameFlow univ (fun _ => horizonControlDirection) (fun _ => 0)
      0 ChatgptAudit.flatNullFrame,
      ∀ t∈Ioo (-P.radius) P.radius, screenColumns (P.frame t)=flatScreenVectors := by
  let P := localFrameFlow univ isOpen_univ (fun _ => horizonControlDirection) (fun _ => 0)
    (fun _ => contDiffOn_const) (fun _ _ => contDiffOn_const) 0 (mem_univ _) ChatgptAudit.flatNullFrame
  refine ⟨P,?_⟩
  intro t ht
  rw [zero_generator_frames_constant _ _ _ P t ht]
  rfl

def expandingFactor (x : Coordinate4) : ℝ := Real.exp (-2*x 0)
def expandingNullVelocity (x : Coordinate4) : Coordinate4 := expandingFactor x • horizonControlDirection
def expandingGradientMatrix : Tensor4 := !![-1,1,0,0; -1,1,0,0; 0,0,1,0; 0,0,0,1]

theorem expanding_factor_partial (x : Coordinate4) (i : Fin 4) :
    coordinatePartial expandingFactor x i=
      -2*expandingFactor x*(Pi.single i (1:ℝ) : Coordinate4) 0 := by
  have hf := ((hasFDerivAt_apply (𝕜 := ℝ) 0 x).const_mul (-2:ℝ)).exp
  unfold coordinatePartial expandingFactor
  rw [hf.fderiv]
  simp only [_root_.smul_apply,smul_eq_mul,ContinuousLinearMap.proj_apply]
  ring

theorem expanding_velocity_partial (x : Coordinate4) (i : Fin 4) :
    vectorPartial expandingNullVelocity x i=
      (-2*expandingFactor x*(Pi.single i (1:ℝ) : Coordinate4) 0) • horizonControlDirection := by
  have hf : DifferentiableAt ℝ expandingFactor x :=
    (((hasFDerivAt_apply (𝕜 := ℝ) 0 x).const_mul (-2:ℝ)).exp).differentiableAt
  funext a
  change coordinatePartial (fun y => expandingFactor y*horizonControlDirection a) x i=_
  rw [coordinatePartial_mul expandingFactor (fun _ => horizonControlDirection a) x hf
    (differentiableAt_const _) i,expanding_factor_partial]
  simp [coordinatePartial]

theorem expanding_velocity_gradient (x : Coordinate4) :
    covariantVectorGradient controlConformalConnection expandingNullVelocity x=
      expandingFactor x • expandingGradientMatrix := by
  ext a i
  simp only [covariantVectorGradient,covariantVectorDerivative,expanding_velocity_partial]
  fin_cases a <;> fin_cases i <;>
    norm_num [expandingNullVelocity,expandingGradientMatrix,controlConformalConnection,
      horizonControlDirection,Matrix.mulVec,dotProduct,Fin.sum_univ_four,Pi.single_apply,
      Matrix.cons_val_two,Matrix.cons_val_three,Fin.isValue] <;> ring

theorem expanding_velocity_null (x : Coordinate4) :
    tensorQuad (controlConformalMetric x) (expandingNullVelocity x)=0 := by
  simp [expandingNullVelocity,controlConformalMetric,horizonControlDirection,tensorQuad,
    eta4,Matrix.mulVec,dotProduct,Fin.sum_univ_four,Matrix.cons_val_two,Matrix.cons_val_three]

theorem expanding_velocity_geodesic (x : Coordinate4) :
    vectorAcceleration controlConformalConnection expandingNullVelocity x=0 := by
  unfold vectorAcceleration
  rw [expanding_velocity_gradient]
  ext a
  fin_cases a <;>
    simp [expandingNullVelocity,expandingGradientMatrix,horizonControlDirection,
      Matrix.mulVec,dotProduct,Fin.sum_univ_four,Matrix.cons_val_two,Matrix.cons_val_three]

theorem expanding_velocity_expansion (x : Coordinate4) :
    vectorExpansion controlConformalConnection expandingNullVelocity x=2*expandingFactor x := by
  unfold vectorExpansion
  rw [expanding_velocity_gradient]
  simp [expandingGradientMatrix,Matrix.trace,Matrix.diag,Fin.sum_univ_four,
    Matrix.cons_val_two,Matrix.cons_val_three]
  ring

theorem expanding_velocity_smooth : SmoothVectorOn univ expandingNullVelocity := by
  intro a
  change ContDiffOn ℝ ∞ (fun x : Coordinate4 => Real.exp (-2*x 0)*horizonControlDirection a) univ
  fun_prop

theorem expanding_metric_smooth : SmoothMatrixOn univ controlConformalMetric := by
  intro a b
  change ContDiffOn ℝ ∞ (fun x : Coordinate4 => Real.exp (2*x 0)*eta4 a b) univ
  fun_prop

theorem expanding_connection_smooth : SmoothConnectionOn univ controlConformalConnection := by
  intro i a b
  exact contDiffOn_const

theorem expanding_metric_symmetric (x : Coordinate4) :
    (controlConformalMetric x)ᵀ=controlConformalMetric x := by
  simp [controlConformalMetric,eta4,Matrix.transpose_smul]

theorem expanding_metric_inverse (x : Coordinate4) :
    controlConformalInverse x*controlConformalMetric x=1 := by
  have hf : controlConformalFactor x≠0 := Real.exp_ne_zero _
  ext a b
  fin_cases a <;> fin_cases b <;>
    norm_num [controlConformalInverse,controlConformalMetric,eta4,Matrix.mul_apply,
      Fin.sum_univ_four,Matrix.diagonal_apply,Fin.isValue,Matrix.cons_val_two,Matrix.cons_val_three] <;> field_simp [hf]

theorem expanding_connection_compatible :
    MetricCompatibleOn univ controlConformalMetric controlConformalConnection := by
  have he : leviCivitaField controlConformalMetric controlConformalInverse=controlConformalConnection :=
    funext control_conformal_levi_civita
  rw [← he]
  exact levi_civita_field_metric_compatible univ isOpen_univ
    controlConformalMetric controlConformalInverse (fun x _ => expanding_metric_symmetric x)
    (fun x _ => expanding_metric_inverse x)
    (fun x _ => mul_eq_one_comm.mp (expanding_metric_inverse x))

def expandingInitialFrame :
    Screen013.NormalizedNullFrame (controlConformalMetric 0) (expandingNullVelocity 0) := by
  have hg0 : controlConformalMetric 0=eta4 := by
    simp [controlConformalMetric,controlConformalFactor]
  have hv0 : expandingNullVelocity 0=horizonControlDirection := by
    simp [expandingNullVelocity,expandingFactor]
  rw [hg0,hv0]
  refine {
    frame := ChatgptAudit.flatNullFrame
    inverse := flatNullInverse
    right_inverse := flat_null_inverse
    gram := flat_null_gram
    first_column := ?_ }
  intro a
  fin_cases a <;> rfl

theorem expanding_screen_nonconstant :
    ∃ curve : ℝ → Coordinate4, curve 0=0 ∧
      ∃ S : GeometricScreenAlong controlConformalMetric controlConformalConnection expandingNullVelocity curve,
        inducedArea controlConformalMetric curve S.vectors 0=1 ∧
        HasDerivAt (inducedArea controlConformalMetric curve S.vectors) 2 0 ∧
        ¬ (∀ᶠ t in 𝓝 (0:ℝ), inducedArea controlConformalMetric curve S.vectors t=1) := by
  let F := expandingInitialFrame
  let P := localFrameFlow univ isOpen_univ expandingNullVelocity
    (transportGenerator controlConformalConnection expandingNullVelocity) expanding_velocity_smooth
    (transport_generator_smooth univ isOpen_univ controlConformalConnection expandingNullVelocity
      expanding_connection_smooth expanding_velocity_smooth) 0 (mem_univ _) F.frame
  let S := geometricScreenFromFlow univ isOpen_univ controlConformalMetric controlConformalConnection
    expandingNullVelocity expanding_connection_compatible (fun x _ => expanding_metric_symmetric x)
    expanding_metric_smooth expanding_velocity_smooth (fun x _ => expanding_velocity_null x)
    (fun x _ => expanding_velocity_geodesic x) 0 (mem_univ _) F P
  have hd := flow_screen_area_derivative_zero univ isOpen_univ controlConformalMetric controlConformalConnection
    expandingNullVelocity expanding_connection_compatible (fun x _ => expanding_metric_symmetric x)
    expanding_metric_smooth expanding_velocity_smooth (fun x _ => expanding_velocity_null x)
    (fun x _ => expanding_velocity_geodesic x) 0 (mem_univ _) F P
  rw [expanding_velocity_expansion] at hd
  norm_num [expandingFactor] at hd
  have hder : HasDerivAt (inducedArea controlConformalMetric P.curve S.vectors) 2 0 := hd
  have hinit : inducedArea controlConformalMetric P.curve S.vectors 0=1 := by
    change screenArea (screenGram (controlConformalMetric (P.curve 0))
      (screenColumns (P.frame 0)))=1
    rw [P.curve_zero,P.frame_zero,Screen013.normalized_frame_screen_gram,
      Screen013.negative_identity_screen_area]
  refine ⟨P.curve,P.curve_zero,S,hinit,hder,?_⟩
  intro hconst
  have hz : HasDerivAt (inducedArea controlConformalMetric P.curve S.vectors) 0 0 :=
    (hasDerivAt_const 0 (1:ℝ)).congr_of_eventuallyEq hconst
  have hbad := hder.unique hz
  norm_num at hbad

theorem expanding_background_curvature :
    coordinateCurvature controlConformalConnection (0:Coordinate4) 1 2 1 2=1 := by
  have he : leviCivitaField controlConformalMetric controlConformalInverse=controlConformalConnection :=
    funext control_conformal_levi_civita
  rw [← he]
  exact control_conformal_curvature_nonzero 0

#print axioms zero_generator_frames_constant
#print axioms flat_frame_flow_control
#print axioms expanding_factor_partial
#print axioms expanding_velocity_partial
#print axioms expanding_velocity_gradient
#print axioms expanding_velocity_null
#print axioms expanding_velocity_geodesic
#print axioms expanding_velocity_expansion
#print axioms expanding_velocity_smooth
#print axioms expanding_metric_smooth
#print axioms expanding_connection_smooth
#print axioms expanding_metric_symmetric
#print axioms expanding_metric_inverse
#print axioms expanding_connection_compatible
#print axioms expandingInitialFrame
#print axioms expanding_screen_nonconstant
#print axioms expanding_background_curvature
end
end ChatgptAudit.Screen014
