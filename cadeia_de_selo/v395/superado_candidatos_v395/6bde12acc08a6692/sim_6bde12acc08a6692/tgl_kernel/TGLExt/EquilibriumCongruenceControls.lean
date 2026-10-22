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
import TGLExt.EquilibriumScreenIntegration

set_option autoImplicit false
set_option maxHeartbeats 8000000
namespace ChatgptAudit.Flow019
open Matrix Filter Topology Set ChatgptAudit.Flow018 ChatgptAudit.Screen014 TGLExt
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def controlNullCompanion : Coordinate4 := ![-(1/2:ℝ),(1/2:ℝ),0,0]

theorem control_companion_null (x : Coordinate4) :
    tensorQuad (controlConformalMetric x) controlNullCompanion=0 := by
  simp [controlConformalMetric,controlNullCompanion,tensorQuad,eta4,Matrix.mulVec,
    dotProduct,Fin.sum_univ_four,Matrix.cons_val_two,Matrix.cons_val_three]

theorem control_companion_pair :
    tensorPair (controlConformalMetric 0) horizonControlDirection controlNullCompanion= -1 := by
  norm_num [controlConformalMetric,controlConformalFactor,controlNullCompanion,
    horizonControlDirection,tensorPair,eta4,Matrix.mulVec,dotProduct,
    Fin.sum_univ_four,Matrix.cons_val_two,Matrix.cons_val_three]

theorem zero_gradient_differs_from_expanding_field (V : VectorField4)
    (hV : covariantVectorGradient controlConformalConnection V 0=0) :
    V≠expandingNullVelocity := by
  intro he
  have hz : vectorExpansion controlConformalConnection expandingNullVelocity 0=0 := by
    rw [←he]
    simp [vectorExpansion,hV]
  have ht : vectorExpansion controlConformalConnection expandingNullVelocity 0=2 := by
    rw [expanding_velocity_expansion]
    simp [expandingFactor]
  linarith

theorem flat_equilibrium_congruence_control :
    ∃ N : Set Coordinate4, IsOpen N ∧ (0:Coordinate4)∈N ∧
      ∃ V : VectorField4, SmoothVectorOn N V ∧ V 0=horizonControlDirection ∧
        (∀ x∈N, V x≠0) ∧ (∀ x∈N, tensorQuad eta4 (V x)=0) ∧
        EqOn (vectorAcceleration (frameLeviCivita (fun _ => 1) (fun _ => 1)) V)
          (fun _ => 0) N ∧
        covariantVectorGradient (frameLeviCivita (fun _ => 1) (fun _ => 1)) V 0=0 := by
  have hn : tensorQuad (frameMetricField (fun _ => 1) 0) horizonControlDirection=0 := by
    norm_num [frameMetricField,horizonControlDirection,tensorQuad,eta4,Matrix.mulVec,
      dotProduct,Fin.sum_univ_four,Matrix.cons_val_two,Matrix.cons_val_three]
  obtain ⟨N,hN,_,h0,V,hV,hVp,hvN,hnN,hgeo,hgrad⟩ :=
    local_levi_civita_equilibrium_congruence univ isOpen_univ (fun _ => 1) (fun _ => 1)
      (fun _ _ => by simp) (fun _ _ => by simp)
      (fun _ _ => contDiffOn_const) (fun _ _ => contDiffOn_const)
      0 horizonControlDirection (mem_univ _) control_direction_nonzero hn
  refine ⟨N,hN,h0,V,hV,hVp,hvN,?_,hgeo,hgrad⟩
  intro x hx
  simpa only [frameMetricField,Matrix.transpose_one,one_mul,mul_one] using hnN x hx

theorem curved_equilibrium_congruence_control :
    (∃ N : Set Coordinate4, IsOpen N ∧ (0:Coordinate4)∈N ∧
      ∃ V : VectorField4, SmoothVectorOn N V ∧ V 0=horizonControlDirection ∧
        (∀ x∈N, V x≠0) ∧ (∀ x∈N, tensorQuad (controlConformalMetric x) (V x)=0) ∧
        EqOn (vectorAcceleration controlConformalConnection V) (fun _ => 0) N ∧
        covariantVectorGradient controlConformalConnection V 0=0 ∧
        V≠expandingNullVelocity) ∧
    coordinateCurvature controlConformalConnection (0:Coordinate4) 1 2 1 2=1 := by
  have hn : tensorQuad (controlConformalMetric 0) horizonControlDirection=0 := by
    simpa [expandingNullVelocity,expandingFactor] using expanding_velocity_null 0
  obtain ⟨D,hD,hDU,h0D,W,hW,hWp,hnW,hJ,_⟩ :=
    null_seed_with_companion univ isOpen_univ controlConformalMetric controlConformalConnection
      expanding_metric_smooth expanding_connection_compatible (fun x _ => expanding_metric_symmetric x)
      (fun _ => controlNullCompanion) (fun _ => contDiffOn_const)
      (fun x _ => control_companion_null x) 0 horizonControlDirection (mem_univ _) hn
      (by rw [control_companion_pair]; norm_num)
  obtain ⟨N,hN,_,h0,V,hV,hVp,hvN,hnN,hgeo,hgrad⟩ :=
    local_equilibrium_congruence_from_seed D hD controlConformalMetric controlConformalConnection
      (fun a b => (expanding_metric_smooth a b).mono hDU)
      (fun i a b => (expanding_connection_smooth i a b).mono hDU)
      (fun x hx => expanding_connection_compatible x (hDU hx))
      W (contDiffOn_pi.2 hW) hnW 0 horizonControlDirection h0D control_direction_nonzero hWp hJ
  exact ⟨⟨N,hN,h0,V,hV,hVp,hvN,hnN,hgeo,hgrad,
    zero_gradient_differs_from_expanding_field V hgrad⟩,expanding_background_curvature⟩

#print axioms control_companion_null
#print axioms control_companion_pair
#print axioms zero_gradient_differs_from_expanding_field
#print axioms flat_equilibrium_congruence_control
#print axioms curved_equilibrium_congruence_control
end
end ChatgptAudit.Flow019
