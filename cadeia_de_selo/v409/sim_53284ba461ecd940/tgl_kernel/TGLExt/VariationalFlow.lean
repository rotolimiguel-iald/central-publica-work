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
import TGLExt.DifferentialFlowExistence

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Flow016
open Filter Topology Set
open scoped ContDiff
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]

abbrev VariationalState (E : Type*) [NormedAddCommGroup E] [NormedSpace ℝ E] :=
  E × (E →L[ℝ] E)

def variationalDomain (Q : Set E) : Set (VariationalState E) := {z | z.1∈Q}

def variationalField (f : E → E) (z : VariationalState E) : VariationalState E :=
  (f z.1,(fderiv ℝ f z.1).comp z.2)

omit [CompleteSpace E] in
theorem variational_domain_open (Q : Set E) (hQ : IsOpen Q) :
    IsOpen (variationalDomain Q) := hQ.preimage continuous_fst

omit [CompleteSpace E] in
theorem variational_field_smooth (Q : Set E) (hQ : IsOpen Q)
    (f : E → E) (hf : ContDiffOn ℝ ∞ f Q) :
    ContDiffOn ℝ ∞ (variationalField f) (variationalDomain Q) := by
  have hdf : ContDiffOn ℝ ∞ (fderiv ℝ f) Q := hf.fderiv_of_isOpen hQ (by simp)
  have hmaps : MapsTo (Prod.fst : VariationalState E → E) (variationalDomain Q) Q :=
    fun _ hz => hz
  exact (hf.comp contDiffOn_fst hmaps).prodMk
    ((hdf.comp contDiffOn_fst hmaps).clm_comp contDiffOn_snd)

def variationalLocalFlow (Q : Set E) (hQ : IsOpen Q)
    (f : E → E) (hf : ContDiffOn ℝ ∞ f Q) (p : E) (hp : p∈Q) :
    LipschitzLocalFlow (variationalField f) (variationalDomain Q) (p,ContinuousLinearMap.id ℝ E) :=
  lipschitzLocalFlow (variationalDomain Q) (variational_domain_open Q hQ)
    (variationalField f) (p,ContinuousLinearMap.id ℝ E) hp
    ((((variational_field_smooth Q hQ f hf) (p,ContinuousLinearMap.id ℝ E) hp).contDiffAt
      ((variational_domain_open Q hQ).mem_nhds hp)).of_le (by simp))

def flowSolution {f : E → E} {Q : Set E} {p : E}
    (F : LipschitzLocalFlow (variationalField f) (variationalDomain Q) (p,ContinuousLinearMap.id ℝ E))
    (q : E) (t : ℝ) : E :=
  (F.flow ((q,ContinuousLinearMap.id ℝ E),t)).1

def flowVariation {f : E → E} {Q : Set E} {p : E}
    (F : LipschitzLocalFlow (variationalField f) (variationalDomain Q) (p,ContinuousLinearMap.id ℝ E))
    (q : E) (t : ℝ) : E →L[ℝ] E :=
  (F.flow ((q,ContinuousLinearMap.id ℝ E),t)).2

omit [CompleteSpace E] in
theorem diagonal_initial_mem (p q : E) (radius : ℝ) (hq : q∈Metric.ball p radius) :
    (q,ContinuousLinearMap.id ℝ E)∈Metric.ball (p,ContinuousLinearMap.id ℝ E) radius := by
  simpa only [Metric.mem_ball,Prod.dist_eq,dist_self,max_eq_left dist_nonneg] using hq

variable {f : E → E} {Q : Set E} {p : E}
  (F : LipschitzLocalFlow (variationalField f) (variationalDomain Q) (p,ContinuousLinearMap.id ℝ E))

omit [CompleteSpace E] in
theorem flow_solution_initial (q : E) (hq : q∈Metric.ball p F.radius) :
    flowSolution F q 0=q :=
  congrArg Prod.fst (F.initial _ (diagonal_initial_mem p q F.radius hq))

omit [CompleteSpace E] in
theorem flow_variation_initial (q : E) (hq : q∈Metric.ball p F.radius) :
    flowVariation F q 0=ContinuousLinearMap.id ℝ E :=
  congrArg Prod.snd (F.initial _ (diagonal_initial_mem p q F.radius hq))

omit [CompleteSpace E] in
theorem flow_solution_derivative (q : E) (hq : q∈Metric.ball p F.radius)
    (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    HasDerivAt (flowSolution F q) (f (flowSolution F q t)) t :=
  (ContinuousLinearMap.fst ℝ E (E →L[ℝ] E)).hasFDerivAt.comp_hasDerivAt t
    (F.derivative _ (diagonal_initial_mem p q F.radius hq) t ht)

omit [CompleteSpace E] in
theorem flow_variation_derivative (q : E) (hq : q∈Metric.ball p F.radius)
    (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    HasDerivAt (flowVariation F q)
      ((fderiv ℝ f (flowSolution F q t)).comp (flowVariation F q t)) t :=
  (ContinuousLinearMap.snd ℝ E (E →L[ℝ] E)).hasFDerivAt.comp_hasDerivAt t
    (F.derivative _ (diagonal_initial_mem p q F.radius hq) t ht)

omit [CompleteSpace E] in
theorem flow_variation_apply_derivative (q h : E) (hq : q∈Metric.ball p F.radius)
    (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    HasDerivAt (fun s => flowVariation F q s h)
      (fderiv ℝ f (flowSolution F q t) (flowVariation F q t h)) t :=
  (ContinuousLinearMap.apply ℝ E h).hasFDerivAt.comp_hasDerivAt t
    (flow_variation_derivative F q hq t ht)

omit [CompleteSpace E] in
theorem flow_solution_stays (q : E) (hq : q∈Metric.ball p F.radius)
    (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) : flowSolution F q t∈Q :=
  F.stays _ (diagonal_initial_mem p q F.radius hq) t ht

omit [CompleteSpace E] in
theorem flow_solution_distance_bound (q r : E)
    (hq : q∈Metric.ball p F.radius) (hr : r∈Metric.ball p F.radius)
    (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    ‖flowSolution F q t-flowSolution F r t‖ ≤ F.constant*‖q-r‖ := by
  have hd := (F.lipschitz t ht).dist_le_mul
    (q,ContinuousLinearMap.id ℝ E) (diagonal_initial_mem p q F.radius hq)
    (r,ContinuousLinearMap.id ℝ E) (diagonal_initial_mem p r F.radius hr)
  simp only [Prod.dist_eq,dist_self,max_eq_left dist_nonneg] at hd
  convert (le_max_left _ _).trans hd using 1 <;> first | rfl | simp only [flowSolution,dist_eq_norm]

omit [CompleteSpace E] in
theorem solution_and_variation_continuous (q : E) (hq : q∈Metric.ball p F.radius)
    (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    ContinuousAt (fun z : E × ℝ => (flowSolution F z.1 z.2,flowVariation F z.1 z.2)) (q,t) := by
  have hi : ContinuousAt (fun z : E × ℝ => ((z.1,ContinuousLinearMap.id ℝ E),z.2)) (q,t) := by
    fun_prop
  change ContinuousAt (fun z : E × ℝ => F.flow ((z.1,ContinuousLinearMap.id ℝ E),z.2)) (q,t)
  exact (flow_joint_continuous_at _ _ _ F _ (diagonal_initial_mem p q F.radius hq) t ht).comp
    (f := fun z : E × ℝ => ((z.1,ContinuousLinearMap.id ℝ E),z.2)) hi

#print axioms variational_domain_open
#print axioms variational_field_smooth
#print axioms variationalLocalFlow
#print axioms diagonal_initial_mem
#print axioms flow_solution_initial
#print axioms flow_variation_initial
#print axioms flow_solution_derivative
#print axioms flow_variation_derivative
#print axioms flow_variation_apply_derivative
#print axioms flow_solution_stays
#print axioms flow_solution_distance_bound
#print axioms solution_and_variation_continuous
end
end ChatgptAudit.Flow016
