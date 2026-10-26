-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_017 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.FlowGermUniqueness

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Flow017
open Filter Topology Set ChatgptAudit.Flow016
open scoped ContDiff
noncomputable section
universe u
variable {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
variable {f : E → E} {Q : Set E} {p : E}

def projectedVariationalFlow
    (V : LipschitzLocalFlow (variationalField f) (variationalDomain Q)
      (p,ContinuousLinearMap.id ℝ E)) : LipschitzLocalFlow f Q p where
  radius := V.radius
  radius_positive := V.radius_positive
  constant := V.constant
  flow := fun z => flowSolution V z.1 z.2
  initial := flow_solution_initial V
  derivative := flow_solution_derivative V
  stays := flow_solution_stays V
  continuous := fun z hz =>
    (solution_and_variation_continuous V z.1 hz.1 z.2 hz.2).fst.continuousWithinAt
  lipschitz := by
    intro t ht
    apply LipschitzOnWith.of_dist_le_mul
    intro q hq r hr
    simpa only [dist_eq_norm] using flow_solution_distance_bound V q r hq hr t ht

theorem variational_projection_contDiffAt
    (V : LipschitzLocalFlow (variationalField f) (variationalDomain Q)
      (p,ContinuousLinearMap.id ℝ E)) (n : ℕ)
    (hV : ContDiffAt ℝ n V.flow ((p,ContinuousLinearMap.id ℝ E),(0:ℝ))) :
    ContDiffAt ℝ n (fun z : E × ℝ => flowSolution V z.1 z.2) (p,(0:ℝ)) ∧
    ContDiffAt ℝ n (fun z : E × ℝ => flowVariation V z.1 z.2) (p,(0:ℝ)) := by
  have hi : ContDiffAt ℝ n
      (fun z : E × ℝ => ((z.1,ContinuousLinearMap.id ℝ E),z.2)) (p,(0:ℝ)) := by
    fun_prop
  have hc : ContDiffAt ℝ n
      (fun z : E × ℝ => V.flow ((z.1,ContinuousLinearMap.id ℝ E),z.2)) (p,(0:ℝ)) :=
    hV.comp (p,(0:ℝ)) hi
  exact ⟨hc.fst,hc.snd⟩

theorem variational_regular_flow_successor
    (V : LipschitzLocalFlow (variationalField f) (variationalDomain Q)
      (p,ContinuousLinearMap.id ℝ E)) (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q)
    (hp : p∈Q) (n : ℕ)
    (hV : ContDiffAt ℝ n V.flow ((p,ContinuousLinearMap.id ℝ E),(0:ℝ))) :
    ContDiffAt ℝ (n+1) (projectedVariationalFlow V).flow (p,(0:ℝ)) := by
  obtain ⟨hPhi,hJ⟩ := variational_projection_contDiffAt V n hV
  have hpball : p∈Metric.ball p V.radius := Metric.mem_ball_self V.radius_positive
  have h0 : (0:ℝ)∈Ioo (-V.radius) V.radius :=
    ⟨neg_neg_of_pos V.radius_positive,V.radius_positive⟩
  have hdom : Metric.ball p V.radius ×ˢ Ioo (-V.radius) V.radius∈𝓝 (p,(0:ℝ)) :=
    (Metric.isOpen_ball.prod isOpen_Ioo).mem_nhds ⟨hpball,h0⟩
  have hfc : ContDiffAt ℝ n f (flowSolution V p 0) := by
    rw [flow_solution_initial V p hpball]
    exact contDiffAt_infty.1 ((hf p hp).contDiffAt (hQ.mem_nhds hp)) n
  have htime : ContDiffAt ℝ n (fun z : E × ℝ =>
      (ContinuousLinearMap.id ℝ ℝ).smulRight (f (flowSolution V z.1 z.2))) (p,(0:ℝ)) :=
    contDiffAt_const.smulRight (hfc.comp (p,(0:ℝ)) hPhi)
  have hD : ContDiffAt ℝ n (fun z : E × ℝ => flowJointDerivative V z.1 z.2) (p,(0:ℝ)) := by
    simp only [flowJointDerivative,←ContinuousLinearMap.comp_fst_add_comp_snd]
    exact (hJ.clm_comp contDiffAt_const).add (htime.clm_comp contDiffAt_const)
  apply contDiffAt_succ_iff_hasFDerivAt.2
  refine ⟨fun z => flowJointDerivative V z.1 z.2,⟨_,hdom,?_⟩,hD⟩
  intro z hz
  exact (flow_joint_hasStrictFDerivAt V hQ hf z.1 hz.1 z.2 hz.2).hasFDerivAt

theorem exists_finite_regular_flow (n : ℕ) :
    ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E],
      ∀ (Q : Set E) (_ : IsOpen Q) (f : E → E) (_ : ContDiffOn ℝ ∞ f Q)
        (p : E), p∈Q →
        ∃ F : LipschitzLocalFlow f Q p, ContDiffAt ℝ n F.flow (p,(0:ℝ)) := by
  induction n with
  | zero =>
    intro E _ _ _ Q hQ f hf p hp
    let F := lipschitzLocalFlow Q hQ f p hp
      (((hf p hp).contDiffAt (hQ.mem_nhds hp)).of_le (by simp))
    refine ⟨F,?_⟩
    rw [Nat.cast_zero,contDiffAt_zero]
    exact ⟨Metric.ball p F.radius ×ˢ Ioo (-F.radius) F.radius,
      (Metric.isOpen_ball.prod isOpen_Ioo).mem_nhds
        ⟨Metric.mem_ball_self F.radius_positive,neg_neg_of_pos F.radius_positive,F.radius_positive⟩,
      F.continuous⟩
  | succ n ih =>
    intro E _ _ _ Q hQ f hf p hp
    obtain ⟨V,hV⟩ := ih (VariationalState E) (variationalDomain Q) (variational_domain_open Q hQ)
      (variationalField f) (variational_field_smooth Q hQ f hf) (p,ContinuousLinearMap.id ℝ E) hp
    exact ⟨projectedVariationalFlow V,variational_regular_flow_successor V hQ hf hp n hV⟩

#print axioms projectedVariationalFlow
#print axioms variational_projection_contDiffAt
#print axioms variational_regular_flow_successor
#print axioms exists_finite_regular_flow
end
end ChatgptAudit.Flow017
