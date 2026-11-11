-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_015 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.NullGeodesicConservation

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Screen015
open Matrix Filter Topology Set
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem geodesic_flow_smooth_Icc (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (p : Phase4) (F : LocalPhaseFlow (geodesicSpray Gamma) (regularPhaseDomain U) p)
    (q : Phase4) (hq : q∈Metric.ball p F.radius) (a b : ℝ)
    (hab : Icc a b ⊆ Ioo (-F.radius) F.radius) :
    ContDiffOn ℝ ∞ (fun t => F.flow (q,t)) (Icc a b) := by
  have hf : ContDiffOn ℝ ∞ (fun z : ℝ × Phase4 => geodesicSpray Gamma z.2)
      (Icc a b ×ˢ phaseDomain U) :=
    (geodesic_spray_smooth U hU Gamma hG).comp contDiffOn_snd (fun _ hz => hz.2)
  exact ODE.contDiffOn_enat_Icc_of_hasDerivWithinAt (n := (⊤:ℕ∞))
    (f := fun (_ : ℝ) (z : Phase4) => geodesicSpray Gamma z)
    (u := phaseDomain U) (α := fun t => F.flow (q,t)) hf
    (fun t ht => (F.derivative q hq t (hab ht)).hasDerivWithinAt)
    (fun t ht => (geodesic_flow_regular U Gamma p F q hq t (hab ht)).1)

theorem geodesic_flow_smooth_time (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (p : Phase4) (F : LocalPhaseFlow (geodesicSpray Gamma) (regularPhaseDomain U) p)
    (q : Phase4) (hq : q∈Metric.ball p F.radius) :
    ContDiffOn ℝ ∞ (fun t => F.flow (q,t)) (Ioo (-F.radius) F.radius) := by
  intro t ht
  let a := (t-F.radius)/2
  let b := (t+F.radius)/2
  have hat : a < t := by dsimp [a]; linarith [ht.1]
  have htb : t < b := by dsimp [b]; linarith [ht.2]
  have hsub : Icc a b ⊆ Ioo (-F.radius) F.radius := by
    intro s hs
    dsimp [a,b] at hs
    constructor <;> linarith [ht.1,ht.2,hs.1,hs.2]
  have hd := geodesic_flow_smooth_Icc U hU Gamma hG p F q hq a b hsub
  exact ((hd t ⟨hat.le,htb.le⟩).contDiffAt (Icc_mem_nhds hat htb)).contDiffWithinAt

theorem geodesic_flow_position_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (p : Phase4) (F : LocalPhaseFlow (geodesicSpray Gamma) (regularPhaseDomain U) p)
    (q : Phase4) (hq : q∈Metric.ball p F.radius) :
    ContDiffOn ℝ ∞ (fun t => (F.flow (q,t)).1) (Ioo (-F.radius) F.radius) :=
  contDiff_fst.comp_contDiffOn (geodesic_flow_smooth_time U hU Gamma hG p F q hq)

theorem geodesic_flow_velocity_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (p : Phase4) (F : LocalPhaseFlow (geodesicSpray Gamma) (regularPhaseDomain U) p)
    (q : Phase4) (hq : q∈Metric.ball p F.radius) :
    ContDiffOn ℝ ∞ (fun t => (F.flow (q,t)).2) (Ioo (-F.radius) F.radius) :=
  contDiff_snd.comp_contDiffOn (geodesic_flow_smooth_time U hU Gamma hG p F q hq)

theorem phase_flow_jointly_continuous_at (f : Phase4 → Phase4) (Q : Set Phase4)
    (p : Phase4) (F : LocalPhaseFlow f Q p) (q : Phase4)
    (hq : q∈Metric.ball p F.radius) (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    ContinuousAt F.flow (q,t) :=
  F.continuous.continuousAt ((Metric.isOpen_ball.prod isOpen_Ioo).mem_nhds ⟨hq,ht⟩)

theorem phase_initial_data_obstruction (f : Phase4 → Phase4) (Q : Set Phase4)
    (p : Phase4) (F : LocalPhaseFlow f Q p) (q r : Phase4)
    (hq : q∈Metric.ball p F.radius) (hr : r∈Metric.ball p F.radius)
    (hposition : q.1=r.1) (hvelocity : q.2≠r.2) :
    ¬ ∃ V : VectorField4,
      V (F.flow (q,0)).1=(F.flow (q,0)).2 ∧
      V (F.flow (r,0)).1=(F.flow (r,0)).2 := by
  rw [F.initial q hq,F.initial r hr]
  rintro ⟨V,hqv,hrv⟩
  exact hvelocity (hqv.symm.trans ((congrArg V hposition).trans hrv))

#print axioms geodesic_flow_smooth_Icc
#print axioms geodesic_flow_smooth_time
#print axioms geodesic_flow_position_smooth
#print axioms geodesic_flow_velocity_smooth
#print axioms phase_flow_jointly_continuous_at
#print axioms phase_initial_data_obstruction
end
end ChatgptAudit.Screen015
