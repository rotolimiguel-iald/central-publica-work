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
import TGLExt.FlowLinearizationError
import Mathlib.Analysis.Calculus.ContDiff.RCLike
import Mathlib.Topology.Compactness.Compact

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Flow016
open Filter Topology Set
open scoped ContDiff
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

theorem taylor_remainder_eventually (f : E → E) (x : E)
    (hf : ContDiffAt ℝ ∞ f x) (epsilon : ℝ) (hepsilon : 0 < epsilon) :
    ∀ᶠ z : E × E in 𝓝 (x,x),
      ‖firstOrderRemainder f z.2 z.1‖ ≤ epsilon*‖z.1-z.2‖ := by
  have hs := (hf.hasStrictFDerivAt (by simp)).isLittleO.bound (half_pos hepsilon)
  have hdc : ContinuousAt (fun z : E × E => fderiv ℝ f z.2) (x,x) :=
    (hf.continuousAt_fderiv (by simp)).comp (f := Prod.snd) continuousAt_snd
  have hD : ∀ᶠ z : E × E in 𝓝 (x,x),
      ‖fderiv ℝ f z.2-fderiv ℝ f x‖ < epsilon/2 := by
    simpa only [dist_eq_norm] using Metric.tendsto_nhds.1 hdc.tendsto (epsilon/2) (half_pos hepsilon)
  filter_upwards [hs,hD] with z hz hdz
  have he : firstOrderRemainder f z.2 z.1 =
      (f z.1-f z.2-fderiv ℝ f x (z.1-z.2))+
        (fderiv ℝ f x-fderiv ℝ f z.2) (z.1-z.2) := by
    simp only [firstOrderRemainder,sub_apply]
    abel
  rw [he]
  have hlinear := (fderiv ℝ f x-fderiv ℝ f z.2).le_opNorm (z.1-z.2)
  have hb : ‖fderiv ℝ f x-fderiv ℝ f z.2‖ ≤ epsilon/2 := by
    rw [norm_sub_rev]
    exact hdz.le
  calc
    ‖(f z.1-f z.2-fderiv ℝ f x (z.1-z.2))+
        (fderiv ℝ f x-fderiv ℝ f z.2) (z.1-z.2)‖
      ≤ ‖f z.1-f z.2-fderiv ℝ f x (z.1-z.2)‖+
        ‖(fderiv ℝ f x-fderiv ℝ f z.2) (z.1-z.2)‖ := norm_add_le _ _
    _ ≤ (epsilon/2)*‖z.1-z.2‖+(epsilon/2)*‖z.1-z.2‖ :=
      add_le_add hz (hlinear.trans (mul_le_mul_of_nonneg_right hb (norm_nonneg _)))
    _ = _ := by ring

variable {f : E → E} {Q : Set E} {p : E}
  (F : LipschitzLocalFlow (variationalField f) (variationalDomain Q) (p,ContinuousLinearMap.id ℝ E))

theorem flow_taylor_uniform (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q)
    (r : E) (hr : r∈Metric.ball p F.radius) (a b : ℝ)
    (hab : Icc a b ⊆ Ioo (-F.radius) F.radius) (epsilon : ℝ) (hepsilon : 0 < epsilon) :
    ∀ᶠ q in 𝓝 r, ∀ s∈Icc a b,
      ‖firstOrderRemainder f (flowSolution F r s) (flowSolution F q s)‖ ≤
        epsilon*‖flowSolution F q s-flowSolution F r s‖ := by
  apply isCompact_Icc.eventually_forall_of_forall_eventually
  intro s hs
  have hst := hab hs
  have hx := flow_solution_stays F r hr s hst
  have hfx : ContDiffAt ℝ ∞ f (flowSolution F r s) := (hf _ hx).contDiffAt (hQ.mem_nhds hx)
  have hleft : ContinuousAt (fun z : E × ℝ => flowSolution F z.1 z.2) (r,s) :=
    (solution_and_variation_continuous F r hr s hst).fst
  have hright : ContinuousAt (fun z : E × ℝ => flowSolution F r z.2) (r,s) :=
    (flow_solution_derivative F r hr s hst).continuousAt.comp
      (f := (Prod.snd : E × ℝ → ℝ)) (x := (r,s)) continuousAt_snd
  exact (hleft.prodMk hright).tendsto.eventually
    (taylor_remainder_eventually f (flowSolution F r s) hfx epsilon hepsilon)

theorem flow_derivative_norm_bounded (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q)
    (r : E) (hr : r∈Metric.ball p F.radius) (a b : ℝ)
    (hab : Icc a b ⊆ Ioo (-F.radius) F.radius) :
    ∃ M : ℝ, ∀ s∈Icc a b, ‖fderiv ℝ f (flowSolution F r s)‖ ≤ M := by
  have hc : ContinuousOn (fun s => ‖fderiv ℝ f (flowSolution F r s)‖) (Icc a b) := by
    intro s hs
    have hx := flow_solution_stays F r hr s (hab hs)
    have hfx : ContDiffAt ℝ ∞ f (flowSolution F r s) := (hf _ hx).contDiffAt (hQ.mem_nhds hx)
    exact ((hfx.continuousAt_fderiv (by simp)).comp
      (f := flowSolution F r) (flow_solution_derivative F r hr s (hab hs)).continuousAt).norm.continuousWithinAt
  have hcompact : IsCompact ((fun s : ℝ => ‖fderiv ℝ f (flowSolution F r s)‖) '' Icc a b) :=
    isCompact_Icc.image_of_continuousOn hc
  obtain ⟨M,hM⟩ := hcompact.bddAbove
  exact ⟨M,fun s hs => hM ⟨s,hs,rfl⟩⟩

theorem flow_initial_hasFDerivAt_nonnegative (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q)
    (r : E) (hr : r∈Metric.ball p F.radius) (T : ℝ) (hT : 0 ≤ T) (hTr : T < F.radius) :
    HasFDerivAt (fun q => flowSolution F q T) (flowVariation F r T) r := by
  have hsub : Icc 0 T ⊆ Ioo (-F.radius) F.radius := by
    intro s hs
    constructor <;> linarith [F.radius_positive,hs.1,hs.2]
  obtain ⟨M,hM⟩ := flow_derivative_norm_bounded F hQ hf r hr 0 T hsub
  rw [hasFDerivAt_iff_isLittleO,Asymptotics.isLittleO_iff]
  intro c hc
  let B := (F.constant:ℝ)*gronwallBound 0 M 1 T
  let epsilon := c/(|B|+1)
  have hden : 0 < |B|+1 := by positivity
  have hepsilon : 0 < epsilon := div_pos hc hden
  have hbound : epsilon*B ≤ c := by
    calc
      epsilon*B ≤ epsilon*(|B|+1) :=
        mul_le_mul_of_nonneg_left (le_trans (le_abs_self B) (by linarith)) hepsilon.le
      _ = c := by dsimp [epsilon]; field_simp
  have htaylor := flow_taylor_uniform F hQ hf r hr 0 T hsub epsilon hepsilon
  have hball : ∀ᶠ q in 𝓝 r, q∈Metric.ball p F.radius := Metric.isOpen_ball.mem_nhds hr
  filter_upwards [htaylor,hball] with q hqt hq
  change ‖flowRemainder F q r T‖ ≤ c*‖q-r‖
  exact (flow_remainder_normalized_bound F q r hq hr T M epsilon hT hTr hepsilon.le hM hqt
    T ⟨hT,le_rfl⟩).trans (mul_le_mul_of_nonneg_right hbound (norm_nonneg _))

theorem flow_remainder_normalized_bound_nonpositive (q r : E)
    (hq : q∈Metric.ball p F.radius) (hr : r∈Metric.ball p F.radius)
    (T M epsilon : ℝ) (hT : T ≤ 0) (hTl : -F.radius < T) (hepsilon : 0 ≤ epsilon)
    (hM : ∀ s∈Icc T 0, ‖fderiv ℝ f (flowSolution F r s)‖ ≤ M)
    (hTaylor : ∀ s∈Icc T 0,
      ‖firstOrderRemainder f (flowSolution F r s) (flowSolution F q s)‖ ≤
        epsilon*‖flowSolution F q s-flowSolution F r s‖) :
    ‖flowRemainder F q r T‖ ≤ epsilon*(F.constant*gronwallBound 0 M 1 (-T))*‖q-r‖ := by
  have hsub : Icc T 0 ⊆ Ioo (-F.radius) F.radius := by
    intro s hs
    constructor <;> linarith [F.radius_positive,hs.1,hs.2]
  have hneg (s : ℝ) (hs : s∈Icc 0 (-T)) : -s∈Icc T 0 := by
    constructor <;> linarith [hs.1,hs.2]
  let rhs := fun s => fderiv ℝ f (flowSolution F r s) (flowRemainder F q r s)+
      firstOrderRemainder f (flowSolution F r s) (flowSolution F q s)
  have hd (s : ℝ) (hs : s∈Icc 0 (-T)) :
      HasDerivAt (fun a => flowRemainder F q r (-a)) (-rhs (-s)) s := by
    have hh := (flow_remainder_derivative F q r hq hr (-s) (hsub (hneg s hs))).scomp s
      (hasDerivAt_id s).neg
    convert hh using 1 <;> first | rfl | simp only [rhs,neg_one_smul]
  have hc : ContinuousOn (fun s => flowRemainder F q r (-s)) (Icc 0 (-T)) :=
    fun s hs => (hd s hs).continuousAt.continuousWithinAt
  have hb (s : ℝ) (hs : s∈Ico 0 (-T)) :
      ‖-rhs (-s)‖ ≤ M*‖flowRemainder F q r (-s)‖+epsilon*F.constant*‖q-r‖ := by
    have hs' := hneg s ⟨hs.1,hs.2.le⟩
    have hlin := (fderiv ℝ f (flowSolution F r (-s))).le_opNorm (flowRemainder F q r (-s))
    have hlin' := hlin.trans (mul_le_mul_of_nonneg_right (hM (-s) hs') (norm_nonneg _))
    have hrest := (hTaylor (-s) hs').trans (mul_le_mul_of_nonneg_left
      (flow_solution_distance_bound F q r hq hr (-s) (hsub hs')) hepsilon)
    rw [norm_neg]
    calc
      ‖rhs (-s)‖ ≤ ‖fderiv ℝ f (flowSolution F r (-s)) (flowRemainder F q r (-s))‖+
          ‖firstOrderRemainder f (flowSolution F r (-s)) (flowSolution F q (-s))‖ := norm_add_le _ _
      _ ≤ M*‖flowRemainder F q r (-s)‖+epsilon*(F.constant*‖q-r‖) := add_le_add hlin' hrest
      _ = _ := by ring
  have hbound := norm_le_gronwallBound_of_norm_deriv_right_le hc
    (fun s hs => (hd s ⟨hs.1,hs.2.le⟩).hasDerivWithinAt)
    (show ‖flowRemainder F q r (-(0:ℝ))‖ ≤ (0:ℝ) by
      rw [neg_zero,flow_remainder_initial F q r hq hr,norm_zero]) hb
  have hh := hbound (-T) ⟨neg_nonneg.mpr hT,le_rfl⟩
  simp only [neg_neg,sub_zero] at hh
  have he : gronwallBound 0 M (epsilon*F.constant*‖q-r‖) (-T) =
      epsilon*(F.constant*gronwallBound 0 M 1 (-T))*‖q-r‖ := by
    calc
      gronwallBound 0 M (epsilon*F.constant*‖q-r‖) (-T) =
          (epsilon*F.constant*‖q-r‖)*gronwallBound 0 M 1 (-T) := by
        simpa only [mul_one] using gronwall_zero_scaling M (epsilon*F.constant*‖q-r‖) 1 (-T)
      _ = _ := by ring
  rwa [he] at hh

theorem flow_initial_hasFDerivAt_nonpositive (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q)
    (r : E) (hr : r∈Metric.ball p F.radius) (T : ℝ) (hT : T ≤ 0) (hTl : -F.radius < T) :
    HasFDerivAt (fun q => flowSolution F q T) (flowVariation F r T) r := by
  have hsub : Icc T 0 ⊆ Ioo (-F.radius) F.radius := by
    intro s hs
    constructor <;> linarith [F.radius_positive,hs.1,hs.2]
  obtain ⟨M,hM⟩ := flow_derivative_norm_bounded F hQ hf r hr T 0 hsub
  rw [hasFDerivAt_iff_isLittleO,Asymptotics.isLittleO_iff]
  intro c hc
  let B := (F.constant:ℝ)*gronwallBound 0 M 1 (-T)
  let epsilon := c/(|B|+1)
  have hden : 0 < |B|+1 := by positivity
  have hepsilon : 0 < epsilon := div_pos hc hden
  have hbound : epsilon*B ≤ c := by
    calc
      epsilon*B ≤ epsilon*(|B|+1) :=
        mul_le_mul_of_nonneg_left (le_trans (le_abs_self B) (by linarith)) hepsilon.le
      _ = c := by dsimp [epsilon]; field_simp
  have htaylor := flow_taylor_uniform F hQ hf r hr T 0 hsub epsilon hepsilon
  have hball : ∀ᶠ q in 𝓝 r, q∈Metric.ball p F.radius := Metric.isOpen_ball.mem_nhds hr
  filter_upwards [htaylor,hball] with q hqt hq
  change ‖flowRemainder F q r T‖ ≤ c*‖q-r‖
  exact (flow_remainder_normalized_bound_nonpositive F q r hq hr T M epsilon hT hTl
    hepsilon.le hM hqt).trans (mul_le_mul_of_nonneg_right hbound (norm_nonneg _))

theorem flow_initial_hasFDerivAt (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q)
    (r : E) (hr : r∈Metric.ball p F.radius) (T : ℝ) (hT : T∈Ioo (-F.radius) F.radius) :
    HasFDerivAt (fun q => flowSolution F q T) (flowVariation F r T) r := by
  rcases le_total 0 T with ht | ht
  · exact flow_initial_hasFDerivAt_nonnegative F hQ hf r hr T ht hT.2
  · exact flow_initial_hasFDerivAt_nonpositive F hQ hf r hr T ht hT.1

#print axioms flow_remainder_normalized_bound_nonpositive
#print axioms flow_initial_hasFDerivAt_nonpositive
#print axioms flow_initial_hasFDerivAt

#print axioms taylor_remainder_eventually
#print axioms flow_taylor_uniform
#print axioms flow_derivative_norm_bounded
#print axioms flow_initial_hasFDerivAt_nonnegative
end
end ChatgptAudit.Flow016
