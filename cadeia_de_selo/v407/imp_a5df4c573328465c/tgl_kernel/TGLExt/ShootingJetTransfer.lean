-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_019 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.NullSeedWithJet

set_option autoImplicit false
set_option maxHeartbeats 8000000
namespace ChatgptAudit.Flow019
open Matrix Filter Topology Set ChatgptAudit.Flow016 ChatgptAudit.Flow017
  ChatgptAudit.Flow018 ChatgptAudit.Screen014 ChatgptAudit.Screen015
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

variable {U : Set Coordinate4} {Gamma : ConnectionField4} {p v : Coordinate4}
  (F : LipschitzLocalFlow (variationalField (geodesicSpray Gamma))
    (variationalDomain (regularPhaseDomain U)) ((p,v),ContinuousLinearMap.id ℝ Phase4))
  (ell : Coordinate4 →L[ℝ] ℝ) (W : VectorField4)

theorem shooting_velocity_derivative_zero (hU : IsOpen U) (hG : SmoothConnectionOn U Gamma)
    (hWp : W p=v) (J : Coordinate4 →L[ℝ] Coordinate4) (hJ : HasFDerivAt W J p)
    (hJv : J v=sprayAcceleration Gamma p v) :
    HasFDerivAt (shootingVelocity F ell W) J 0 := by
  let P := transverseProjection v ell
  let L := (P.prod (J.comp P)).prod ell
  have hP : HasFDerivAt (initialPosition p v ell) P 0 := P.hasFDerivAt.const_add p
  have hWd : HasFDerivAt W J (initialPosition p v ell 0) := by
    simpa only [initialPosition,map_zero,add_zero] using hJ
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
  have hd : HasFDerivAt (shootingVelocity F ell W)
      ((ContinuousLinearMap.snd ℝ Coordinate4 Coordinate4).comp
        ((flowJointDerivative F (p,v) 0).comp L)) 0 :=
    (ContinuousLinearMap.snd ℝ Coordinate4 Coordinate4).hasFDerivAt.comp 0 (hFlow.comp 0 hI)
  have he : (ContinuousLinearMap.snd ℝ Coordinate4 Coordinate4).comp
      ((flowJointDerivative F (p,v) 0).comp L)=J := by
    apply ContinuousLinearMap.ext
    intro h
    change ((flowJointDerivative F (p,v) 0) (L h)).2=J h
    simp only [flowJointDerivative,ContinuousLinearMap.coprod_apply,
      flow_variation_initial F (p,v) hbase,flow_solution_initial F (p,v) hbase]
    change J (P h)+ell h • sprayAcceleration Gamma p v=J h
    rw [←hJv,←map_smul,←map_add,transverse_projection_decomposition]
  rwa [he] at hd

variable (C : SmoothLocalChart (shootingPosition F ell W) (shootingDomain F ell W) 0)

theorem shooting_inverse_base_zero (hWp : W p=v) : C.chart.symm p=0 := by
  have hxp : shootingPosition F ell W 0=p :=
    congrArg Prod.fst (shooting_phase_zero F ell W hWp)
  have hpC : C.chart (0:Coordinate4)=p := by rw [C.map_eq]; exact hxp
  simpa only [hpC] using C.chart.left_inv C.base_mem

theorem shooting_inverse_derivative_base (hWp : W p=v)
    (hX : HasFDerivAt (shootingPosition F ell W) (ContinuousLinearMap.id ℝ Coordinate4) 0) :
    HasFDerivAt C.chart.symm (ContinuousLinearMap.id ℝ Coordinate4) p := by
  have hd : HasFDerivAt (C.chart : Coordinate4 → Coordinate4)
      (ContinuousLinearMap.id ℝ Coordinate4) (C.chart.symm p) := by
    rw [shooting_inverse_base_zero F ell W C hWp]
    simpa only [C.map_eq] using hX
  exact C.chart.hasFDerivAt_symm (f' := ContinuousLinearEquiv.refl ℝ Coordinate4)
    (congruence_base_mem F ell W C hWp) hd

theorem congruence_derivative_base (hWp : W p=v)
    (hX : HasFDerivAt (shootingPosition F ell W) (ContinuousLinearMap.id ℝ Coordinate4) 0)
    (J : Coordinate4 →L[ℝ] Coordinate4) (hY : HasFDerivAt (shootingVelocity F ell W) J 0) :
    HasFDerivAt (shootingCongruence F ell W C) J p := by
  have hYi : HasFDerivAt (shootingVelocity F ell W) J (C.chart.symm p) := by
    simpa only [shooting_inverse_base_zero F ell W C hWp] using hY
  have hh := hYi.comp p (shooting_inverse_derivative_base F ell W C hWp hX)
  convert hh using 1 <;> rfl

theorem congruence_prescribed_gradient_zero (hU : IsOpen U)
    (hG : SmoothConnectionOn U Gamma) (hW : ContDiffOn ℝ ∞ W U) (hp : p∈U)
    (hWp : W p=v) (hJ : HasFDerivAt W (connectionInitialJet Gamma p v) p) :
    covariantVectorGradient Gamma (shootingCongruence F ell W C) p=0 := by
  have hJv : connectionInitialJet Gamma p v v=sprayAcceleration Gamma p v :=
    connection_initial_jet_apply Gamma p v v
  have hY := shooting_velocity_derivative_zero F ell W hU hG hWp _ hJ hJv
  have hX := shooting_position_derivative_zero F ell W hU hG hW hp hWp
  have hd := congruence_derivative_base F ell W C hWp hX _ hY
  have he : covariantVectorGradient Gamma (shootingCongruence F ell W C) p=
      covariantVectorGradient Gamma (affineInitialSeed Gamma p v) p := by
    ext a i
    simp only [covariantVectorGradient,covariantVectorDerivative,
      vector_partial_of_derivative _ p _ hd,
      vector_partial_of_derivative _ p _ (affine_seed_derivative Gamma p v p),
      congruence_base_value F ell W C hWp,affine_seed_initial]
  rw [he,affine_seed_gradient_zero]

#print axioms shooting_velocity_derivative_zero
#print axioms shooting_inverse_base_zero
#print axioms shooting_inverse_derivative_base
#print axioms congruence_derivative_base
#print axioms congruence_prescribed_gradient_zero
end
end ChatgptAudit.Flow019
