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
import TGLExt.VariationalFlow

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Flow016
open Filter Topology Set
open scoped ContDiff
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

def firstOrderRemainder (f : E → E) (x y : E) : E :=
  f y-f x-fderiv ℝ f x (y-x)

def flowRemainder {f : E → E} {Q : Set E} {p : E}
    (F : LipschitzLocalFlow (variationalField f) (variationalDomain Q) (p,ContinuousLinearMap.id ℝ E))
    (q r : E) (t : ℝ) : E :=
  flowSolution F q t-flowSolution F r t-flowVariation F r t (q-r)

variable {f : E → E} {Q : Set E} {p : E}
  (F : LipschitzLocalFlow (variationalField f) (variationalDomain Q) (p,ContinuousLinearMap.id ℝ E))

theorem flow_remainder_initial (q r : E)
    (hq : q∈Metric.ball p F.radius) (hr : r∈Metric.ball p F.radius) :
    flowRemainder F q r 0=0 := by
  simp only [flowRemainder,flow_solution_initial F q hq,flow_solution_initial F r hr,
    flow_variation_initial F r hr,ContinuousLinearMap.id_apply,sub_self]

theorem flow_remainder_derivative (q r : E)
    (hq : q∈Metric.ball p F.radius) (hr : r∈Metric.ball p F.radius)
    (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    HasDerivAt (flowRemainder F q r)
      (fderiv ℝ f (flowSolution F r t) (flowRemainder F q r t)+
        firstOrderRemainder f (flowSolution F r t) (flowSolution F q t)) t := by
  have hd := ((flow_solution_derivative F q hq t ht).sub
    (flow_solution_derivative F r hr t ht)).sub
      (flow_variation_apply_derivative F r (q-r) hr t ht)
  have he :
      f (flowSolution F q t)-f (flowSolution F r t)-
          fderiv ℝ f (flowSolution F r t) (flowVariation F r t (q-r)) =
      fderiv ℝ f (flowSolution F r t) (flowRemainder F q r t)+
        firstOrderRemainder f (flowSolution F r t) (flowSolution F q t) := by
    simp only [flowRemainder,firstOrderRemainder,map_sub]
    abel
  rw [he] at hd
  exact hd

theorem flow_remainder_gronwall (q r : E)
    (hq : q∈Metric.ball p F.radius) (hr : r∈Metric.ball p F.radius)
    (T M epsilon : ℝ) (hT : 0 ≤ T) (hTr : T < F.radius) (hepsilon : 0 ≤ epsilon)
    (hM : ∀ s∈Icc 0 T, ‖fderiv ℝ f (flowSolution F r s)‖ ≤ M)
    (hTaylor : ∀ s∈Icc 0 T,
      ‖firstOrderRemainder f (flowSolution F r s) (flowSolution F q s)‖ ≤
        epsilon*‖flowSolution F q s-flowSolution F r s‖) :
    ∀ t∈Icc 0 T, ‖flowRemainder F q r t‖ ≤
      gronwallBound 0 M (epsilon*F.constant*‖q-r‖) t := by
  have hsub : Icc 0 T ⊆ Ioo (-F.radius) F.radius := by
    intro s hs
    constructor <;> linarith [F.radius_positive,hs.1,hs.2]
  let rhs := fun s => fderiv ℝ f (flowSolution F r s) (flowRemainder F q r s)+
      firstOrderRemainder f (flowSolution F r s) (flowSolution F q s)
  have hd (s : ℝ) (hs : s∈Icc 0 T) : HasDerivAt (flowRemainder F q r) (rhs s) s :=
    flow_remainder_derivative F q r hq hr s (hsub hs)
  have hc : ContinuousOn (flowRemainder F q r) (Icc 0 T) :=
    fun s hs => (hd s hs).continuousAt.continuousWithinAt
  have hb (s : ℝ) (hs : s∈Ico 0 T) :
      ‖rhs s‖ ≤ M*‖flowRemainder F q r s‖+epsilon*F.constant*‖q-r‖ := by
    have hs' : s∈Icc 0 T := ⟨hs.1,hs.2.le⟩
    have hlin := (fderiv ℝ f (flowSolution F r s)).le_opNorm (flowRemainder F q r s)
    have hlin' := hlin.trans (mul_le_mul_of_nonneg_right (hM s hs') (norm_nonneg _))
    have hrest := (hTaylor s hs').trans (mul_le_mul_of_nonneg_left
      (flow_solution_distance_bound F q r hq hr s (hsub hs')) hepsilon)
    calc
      ‖rhs s‖ ≤ ‖fderiv ℝ f (flowSolution F r s) (flowRemainder F q r s)‖+
          ‖firstOrderRemainder f (flowSolution F r s) (flowSolution F q s)‖ := norm_add_le _ _
      _ ≤ M*‖flowRemainder F q r s‖+epsilon*(F.constant*‖q-r‖) := add_le_add hlin' hrest
      _ = _ := by ring
  have hbound := norm_le_gronwallBound_of_norm_deriv_right_le hc
    (fun s hs => (hd s ⟨hs.1,hs.2.le⟩).hasDerivWithinAt)
    (show ‖flowRemainder F q r 0‖ ≤ (0:ℝ) by rw [flow_remainder_initial F q r hq hr,norm_zero])
    hb
  intro t ht
  simpa only [sub_zero] using hbound t ht

theorem gronwall_zero_scaling (M a b t : ℝ) :
    gronwallBound 0 M (a*b) t=a*gronwallBound 0 M b t := by
  by_cases hM : M=0
  · simp [gronwallBound,hM]
    ring
  · simp only [gronwallBound,if_neg hM,zero_mul,zero_add]
    ring

theorem flow_remainder_normalized_bound (q r : E)
    (hq : q∈Metric.ball p F.radius) (hr : r∈Metric.ball p F.radius)
    (T M epsilon : ℝ) (hT : 0 ≤ T) (hTr : T < F.radius) (hepsilon : 0 ≤ epsilon)
    (hM : ∀ s∈Icc 0 T, ‖fderiv ℝ f (flowSolution F r s)‖ ≤ M)
    (hTaylor : ∀ s∈Icc 0 T,
      ‖firstOrderRemainder f (flowSolution F r s) (flowSolution F q s)‖ ≤
        epsilon*‖flowSolution F q s-flowSolution F r s‖) :
    ∀ t∈Icc 0 T, ‖flowRemainder F q r t‖ ≤
      epsilon*(F.constant*gronwallBound 0 M 1 t)*‖q-r‖ := by
  intro t ht
  have hb := flow_remainder_gronwall F q r hq hr T M epsilon hT hTr hepsilon hM hTaylor t ht
  have he : gronwallBound 0 M (epsilon*F.constant*‖q-r‖) t =
      epsilon*(F.constant*gronwallBound 0 M 1 t)*‖q-r‖ := by
    calc
      gronwallBound 0 M (epsilon*F.constant*‖q-r‖) t =
          (epsilon*F.constant*‖q-r‖)*gronwallBound 0 M 1 t := by
        simpa only [mul_one] using gronwall_zero_scaling M (epsilon*F.constant*‖q-r‖) 1 t
      _ = _ := by ring
  rwa [he] at hb

#print axioms flow_remainder_initial
#print axioms flow_remainder_derivative
#print axioms flow_remainder_gronwall
#print axioms gronwall_zero_scaling
#print axioms flow_remainder_normalized_bound
end
end ChatgptAudit.Flow016
