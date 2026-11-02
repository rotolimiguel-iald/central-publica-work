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
import TGLExt.FlowSmoothGerm
import Mathlib.Topology.Connected.Basic

set_option autoImplicit false
set_option maxHeartbeats 8000000
namespace ChatgptAudit.Flow017
open Filter Topology Set ChatgptAudit.Flow016
open scoped ContDiff
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
variable {f : E → E} {Q : Set E} {p : E}

omit [CompleteSpace E] [NormedSpace ℝ E] in
theorem eventually_flow_time_box (q : E) (T : ℝ) (P : E → ℝ → ℝ → Prop)
    (hP : ∀ᶠ z : (E × ℝ) × ℝ in 𝓝 ((q,T),T), P z.1.1 z.1.2 z.2) :
    ∃ radius > (0:ℝ), ∀ a∈Metric.ball q radius,
      ∀ b∈Ioo (T-radius) (T+radius), ∀ c∈Ioo (T-radius) (T+radius), P a b c := by
  obtain ⟨radius,hr,hball⟩ := Metric.mem_nhds_iff.mp hP
  refine ⟨radius,hr,?_⟩
  intro a ha b hb c hc
  apply hball (a := ((a,b),c))
  rw [Metric.mem_ball,Prod.dist_eq,Prod.dist_eq]
  have hb' : dist b T < radius := by
    rw [Real.dist_eq,abs_lt]
    constructor <;> linarith [hb.1,hb.2]
  have hc' : dist c T < radius := by
    rw [Real.dist_eq,abs_lt]
    constructor <;> linarith [hc.1,hc.2]
  exact max_lt (max_lt ha hb') hc'

theorem flow_finite_regular_nearby_transfer (F : LipschitzLocalFlow f Q p)
    (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q)
    (q : E) (hq : q∈Metric.ball p F.radius) (T : ℝ) (hT : T∈Ioo (-F.radius) F.radius) (n : ℕ) :
    ∃ radius > (0:ℝ), ∀ t₀∈Ioo (T-radius) (T+radius),
      ContDiffAt ℝ n F.flow (q,t₀) → ContDiffAt ℝ n F.flow (q,T) := by
  let y := F.flow (q,T)
  have hy : y∈Q := F.stays q hq T hT
  have hfy : ContDiffAt ℝ 1 f y := ((hf y hy).contDiffAt (hQ.mem_nhds hy)).of_le (by simp)
  obtain ⟨K,S,hS,hL⟩ := hfy.exists_lipschitzOnWith
  obtain ⟨G,hG⟩ := exists_finite_regular_flow n E Q hQ f hf y hy
  have hGball : y∈Metric.ball y G.radius := Metric.mem_ball_self G.radius_positive
  have hGzero : (0:ℝ)∈Ioo (-G.radius) G.radius :=
    ⟨neg_neg_of_pos G.radius_positive,G.radius_positive⟩
  have hFc := flow_joint_continuous_at f Q p F q hq T hT
  have hGc := flow_joint_continuous_at f Q y G y hGball 0 hGzero
  have hFD : Metric.ball p F.radius ×ˢ Ioo (-F.radius) F.radius∈𝓝 (q,T) :=
    (Metric.isOpen_ball.prod isOpen_Ioo).mem_nhds ⟨hq,hT⟩
  have hGD : Metric.ball y G.radius ×ˢ Ioo (-G.radius) G.radius∈𝓝 (y,(0:ℝ)) :=
    (Metric.isOpen_ball.prod isOpen_Ioo).mem_nhds ⟨hGball,hGzero⟩
  have hFS : ∀ᶠ z in 𝓝 (q,T), F.flow z∈S := hFc.eventually hS
  have hGS : ∀ᶠ z in 𝓝 (y,(0:ℝ)), G.flow z∈S := by
    apply hGc.eventually
    rwa [G.initial y hGball]
  have hGgood : ∀ᶠ z in 𝓝 (y,(0:ℝ)),
      z∈Metric.ball y G.radius ×ˢ Ioo (-G.radius) G.radius ∧
      G.flow z∈S ∧ ContDiffAt ℝ n G.flow z := by
    filter_upwards [hGD,hGS,hG.eventually (by simp)] with z hz hs hn
    exact ⟨hz,hs,hn⟩
  have htarget : ContinuousAt
      (fun z : (E × ℝ) × ℝ => (z.1.1,z.2)) ((q,T),T) := by fun_prop
  have hinit : ContinuousAt (fun z : (E × ℝ) × ℝ => F.flow z.1) ((q,T),T) :=
    hFc.comp (f := Prod.fst) continuousAt_fst
  have hargs : ContinuousAt
      (fun z : (E × ℝ) × ℝ => (F.flow z.1,z.2-z.1.2)) ((q,T),T) :=
    hinit.prodMk (continuousAt_snd.sub continuousAt_fst.snd)
  have hFgood : ∀ᶠ z in 𝓝 (q,T),
      z∈Metric.ball p F.radius ×ˢ Ioo (-F.radius) F.radius ∧ F.flow z∈S := by
    filter_upwards [hFD,hFS] with z hz hs
    exact ⟨hz,hs⟩
  have hFpull := htarget.eventually hFgood
  have hGpull : ∀ᶠ z : (E × ℝ) × ℝ in 𝓝 ((q,T),T),
      (F.flow z.1,z.2-z.1.2)∈Metric.ball y G.radius ×ˢ Ioo (-G.radius) G.radius ∧
      G.flow (F.flow z.1,z.2-z.1.2)∈S ∧
      ContDiffAt ℝ n G.flow (F.flow z.1,z.2-z.1.2) := by
    have ha : Tendsto (fun z : (E × ℝ) × ℝ => (F.flow z.1,z.2-z.1.2))
        (𝓝 ((q,T),T)) (𝓝 (y,(0:ℝ))) := by
      simpa only [sub_self,y] using hargs.tendsto
    exact ha.eventually hGgood
  let P := fun (a : E) (b c : ℝ) =>
    (a,c)∈Metric.ball p F.radius ×ˢ Ioo (-F.radius) F.radius ∧ F.flow (a,c)∈S ∧
    (F.flow (a,b),c-b)∈Metric.ball y G.radius ×ˢ Ioo (-G.radius) G.radius ∧
    G.flow (F.flow (a,b),c-b)∈S ∧ ContDiffAt ℝ n G.flow (F.flow (a,b),c-b)
  have hP : ∀ᶠ z : (E × ℝ) × ℝ in 𝓝 ((q,T),T), P z.1.1 z.1.2 z.2 := by
    filter_upwards [hFpull,hGpull] with z hzF hzG
    exact ⟨hzF.1,hzF.2,hzG.1,hzG.2.1,hzG.2.2⟩
  obtain ⟨radius,hr,hbox⟩ := eventually_flow_time_box q T P hP
  have hcenter : T∈Ioo (T-radius) (T+radius) := by constructor <;> linarith
  refine ⟨radius,hr,?_⟩
  intro t₀ ht₀ hregular
  have hbase := hbox q (Metric.mem_ball_self hr) t₀ ht₀ T hcenter
  have hGat : ContDiffAt ℝ n G.flow (F.flow (q,t₀),T-t₀) := hbase.2.2.2.2
  have hmap : ContDiffAt ℝ n
      (fun z : E × ℝ => (F.flow (z.1,t₀),z.2-t₀)) (q,T) :=
    (hregular.comp (q,T) (contDiffAt_fst.prodMk contDiffAt_const)).prodMk
      (contDiffAt_snd.sub contDiffAt_const)
  have hcomposition := hGat.comp (q,T) hmap
  apply hcomposition.congr_of_eventuallyEq
  have hdom : Metric.ball q radius ×ˢ Ioo (T-radius) (T+radius)∈𝓝 (q,T) :=
    (Metric.isOpen_ball.prod isOpen_Ioo).mem_nhds ⟨Metric.mem_ball_self hr,hcenter⟩
  filter_upwards [hdom] with z hz
  have hderF (s : ℝ) (hs : s∈Ioo (T-radius) (T+radius)) :
      HasDerivAt (fun a => F.flow (z.1,a)) (f (F.flow (z.1,s))) s ∧ F.flow (z.1,s)∈S := by
    obtain ⟨hd,hfs,_,_,_⟩ := hbox z.1 hz.1 t₀ ht₀ s hs
    exact ⟨F.derivative z.1 hd.1 s hd.2,hfs⟩
  have hderG (s : ℝ) (hs : s∈Ioo (T-radius) (T+radius)) :
      HasDerivAt (fun a => G.flow (F.flow (z.1,t₀),a-t₀))
        (f (G.flow (F.flow (z.1,t₀),s-t₀))) s ∧ G.flow (F.flow (z.1,t₀),s-t₀)∈S := by
    obtain ⟨_,_,hd,hgs,_⟩ := hbox z.1 hz.1 t₀ ht₀ s hs
    refine ⟨?_,hgs⟩
    convert (G.derivative (F.flow (z.1,t₀)) hd.1 (s-t₀) hd.2).scomp s
      ((hasDerivAt_id s).sub_const t₀) using 1 <;> first | rfl | simp only [one_smul]
  have hinitEq : F.flow (z.1,t₀)=G.flow (F.flow (z.1,t₀),t₀-t₀) := by
    have hi := hbox z.1 hz.1 t₀ ht₀ t₀ ht₀
    simpa only [sub_self] using (G.initial (F.flow (z.1,t₀)) hi.2.2.1.1).symm
  have he := ODE_solution_unique_of_mem_Ioo (v := fun _ : ℝ => f) (s := fun _ : ℝ => S)
    (fun _ _ => hL) ht₀ hderF hderG hinitEq
  exact he hz.2


theorem flow_finite_regular_on_domain (F : LipschitzLocalFlow f Q p)
    (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q) (n : ℕ) :
    ContDiffOn ℝ n F.flow (Metric.ball p F.radius ×ˢ Ioo (-F.radius) F.radius) := by
  intro z hz
  let A : Set ℝ := {t | ContDiffAt ℝ n F.flow (z.1,t)}
  have hA : IsOpen A := flow_finite_regular_times_open F.flow z.1 n
  have h0 : (0:ℝ)∈Ioo (-F.radius) F.radius :=
    ⟨neg_neg_of_pos F.radius_positive,F.radius_positive⟩
  have hinitial : (0:ℝ)∈A := flow_finite_regular_at_initial F hQ hf z.1 hz.1 n
  have hclosed : closure A ∩ Ioo (-F.radius) F.radius ⊆ A := by
    intro T hTs
    obtain ⟨radius,hr,htransfer⟩ := flow_finite_regular_nearby_transfer F hQ hf z.1 hz.1 T hTs.2 n
    obtain ⟨t₀,ht₀,hdist⟩ := Metric.mem_closure_iff.1 hTs.1 radius hr
    have ht₀I : t₀∈Ioo (T-radius) (T+radius) := by
      rw [Real.dist_eq,abs_lt] at hdist
      constructor <;> linarith [hdist.1,hdist.2]
    exact htransfer t₀ ht₀I ht₀
  have hall : Ioo (-F.radius) F.radius ⊆ A :=
    isPreconnected_Ioo.subset_of_closure_inter_subset hA ⟨0,h0,hinitial⟩ hclosed
  have hc : ContDiffAt ℝ n F.flow (z.1,z.2) := hall hz.2
  exact hc.contDiffWithinAt

theorem flow_smooth_on_domain (F : LipschitzLocalFlow f Q p)
    (hQ : IsOpen Q) (hf : ContDiffOn ℝ ∞ f Q) :
    ContDiffOn ℝ ∞ F.flow (Metric.ball p F.radius ×ˢ Ioo (-F.radius) F.radius) :=
  contDiffOn_infty.2 (flow_finite_regular_on_domain F hQ hf)

#print axioms flow_finite_regular_on_domain
#print axioms flow_smooth_on_domain

#print axioms eventually_flow_time_box
#print axioms flow_finite_regular_nearby_transfer
end
end ChatgptAudit.Flow017
