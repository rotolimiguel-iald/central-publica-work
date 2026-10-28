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
import TGLExt.CongruenceScreenIntegration

set_option autoImplicit false
set_option maxHeartbeats 7000000
namespace ChatgptAudit.Flow018
open Matrix Filter Topology Set ChatgptAudit.Screen014 ChatgptAudit.Screen015 TGLExt
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem control_direction_nonzero : horizonControlDirection≠0 := by
  intro he
  have h0 := congrArg (fun v : Coordinate4 => v 0) he
  norm_num [horizonControlDirection] at h0

theorem flat_constructed_congruence_control :
    ∃ N : Set Coordinate4, IsOpen N ∧ (0:Coordinate4)∈N ∧
      ∃ V : VectorField4, SmoothVectorOn N V ∧ V 0=horizonControlDirection ∧
        (∀ x∈N, V x≠0) ∧ (∀ x∈N, tensorQuad eta4 (V x)=0) ∧
        EqOn (vectorAcceleration (frameLeviCivita (fun _ => 1) (fun _ => 1)) V)
          (fun _ => 0) N := by
  have hn : tensorQuad (frameMetricField (fun _ => 1) 0) horizonControlDirection=0 := by
    norm_num [frameMetricField,horizonControlDirection,tensorQuad,eta4,Matrix.mulVec,
      dotProduct,Fin.sum_univ_four,Matrix.cons_val_two,Matrix.cons_val_three]
  obtain ⟨N,hN,_,h0,V,hV,hVp,hvN,hnN,hgeo⟩ :=
    local_levi_civita_null_congruence univ isOpen_univ (fun _ => 1) (fun _ => 1)
      (fun _ _ => by simp) (fun _ _ => by simp)
      (fun _ _ => contDiffOn_const) (fun _ _ => contDiffOn_const)
      0 horizonControlDirection (mem_univ _) control_direction_nonzero hn
  refine ⟨N,hN,h0,V,hV,hVp,hvN,?_,hgeo⟩
  intro x hx
  simpa only [frameMetricField,Matrix.transpose_one,one_mul,mul_one] using hnN x hx

theorem curved_constructed_congruence_control :
    (∃ N : Set Coordinate4, IsOpen N ∧ (0:Coordinate4)∈N ∧
      ∃ V : VectorField4, SmoothVectorOn N V ∧ V 0=horizonControlDirection ∧
        (∀ x∈N, V x≠0) ∧ (∀ x∈N, tensorQuad (controlConformalMetric x) (V x)=0) ∧
        EqOn (vectorAcceleration controlConformalConnection V) (fun _ => 0) N) ∧
    coordinateCurvature controlConformalConnection (0:Coordinate4) 1 2 1 2=1 := by
  have hseed : expandingNullVelocity (0:Coordinate4)=horizonControlDirection := by
    simp [expandingNullVelocity,expandingFactor]
  obtain ⟨N,hN,_,h0,V,hV,hVp,hvN,hnN,hgeo⟩ :=
    local_null_congruence_from_seed univ isOpen_univ controlConformalMetric
      controlConformalConnection expanding_metric_smooth expanding_connection_smooth
      expanding_connection_compatible expandingNullVelocity (contDiffOn_pi.2 expanding_velocity_smooth)
      (fun x _ => expanding_velocity_null x) 0 horizonControlDirection (mem_univ _)
      control_direction_nonzero hseed
  exact ⟨⟨N,hN,h0,V,hV,hVp,hvN,hnN,hgeo⟩,expanding_background_curvature⟩

theorem geodesic_nullity_does_not_force_zero_expansion :
    SmoothVectorOn univ expandingNullVelocity ∧
    (∀ x, expandingNullVelocity x≠0) ∧
    (∀ x, tensorQuad (controlConformalMetric x) (expandingNullVelocity x)=0) ∧
    (∀ x, vectorAcceleration controlConformalConnection expandingNullVelocity x=0) ∧
    vectorExpansion controlConformalConnection expandingNullVelocity 0=2 := by
  refine ⟨expanding_velocity_smooth,?_,expanding_velocity_null,expanding_velocity_geodesic,?_⟩
  · intro x
    exact smul_ne_zero (Real.exp_ne_zero _) control_direction_nonzero
  · rw [expanding_velocity_expansion]
    simp [expandingFactor]

#print axioms control_direction_nonzero
#print axioms flat_constructed_congruence_control
#print axioms curved_constructed_congruence_control
#print axioms geodesic_nullity_does_not_force_zero_expansion
end
end ChatgptAudit.Flow018
