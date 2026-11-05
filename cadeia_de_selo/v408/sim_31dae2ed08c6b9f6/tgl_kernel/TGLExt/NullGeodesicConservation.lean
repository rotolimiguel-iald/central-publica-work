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
import TGLExt.LocalGeodesicFlow

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Screen015
open Matrix Filter Topology Set
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem geodesic_energy_derivative (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hm : MetricCompatibleOn U g Gamma)
    (curve velocity : ℝ → Coordinate4) (t : ℝ) (ht : curve t∈U)
    (hc : HasDerivAt curve (velocity t) t)
    (hv : HasDerivAt velocity (sprayAcceleration Gamma (curve t) (velocity t)) t) :
    HasDerivAt (fun s => tensorQuad (g (curve s)) (velocity s)) 0 t := by
  let L := connectionAlong Gamma (curve t) (velocity t)
  have hdg := metric_along_curve_derivative U g Gamma hm (curve t) (velocity t) ht
    (smooth_matrix_differentiableAt U hU g hg (curve t) ht) curve t hc rfl
  have hd := Screen014.pair_curve_derivative (fun s => g (curve s)) velocity velocity
    (Lᵀ*g (curve t)+g (curve t)*L) (-(L.mulVec (velocity t))) (-(L.mulVec (velocity t)))
    t hdg hv hv
  rw [geodesic_energy_algebra] at hd
  exact hd

theorem geodesic_flow_energy_conserved (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hm : MetricCompatibleOn U g Gamma)
    (p : Phase4) (F : LocalPhaseFlow (geodesicSpray Gamma) (regularPhaseDomain U) p)
    (q : Phase4) (hq : q∈Metric.ball p F.radius) (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    tensorQuad (g (F.flow (q,t)).1) (F.flow (q,t)).2=tensorQuad (g q.1) q.2 := by
  let energy := fun s => tensorQuad (g (F.flow (q,s)).1) (F.flow (q,s)).2
  have hd (s : ℝ) (hs : s∈Ioo (-F.radius) F.radius) : HasDerivAt energy 0 s :=
    geodesic_energy_derivative U hU g Gamma hg hm
      (fun a => (F.flow (q,a)).1) (fun a => (F.flow (q,a)).2) s
      (geodesic_flow_regular U Gamma p F q hq s hs).1
      (geodesic_flow_position_derivative U Gamma p F q hq s hs)
      (geodesic_flow_velocity_derivative U Gamma p F q hq s hs)
  have h0 : (0:ℝ)∈Ioo (-F.radius) F.radius :=
    ⟨neg_neg_of_pos F.radius_positive,F.radius_positive⟩
  have he : energy t=energy 0 := isOpen_Ioo.is_const_of_deriv_eq_zero isPreconnected_Ioo
    (fun s hs => (hd s hs).differentiableAt.differentiableWithinAt)
    (fun s hs => (hd s hs).deriv) ht h0
  simpa only [energy,F.initial q hq] using he

theorem geodesic_flow_null_preserved (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hm : MetricCompatibleOn U g Gamma)
    (p : Phase4) (F : LocalPhaseFlow (geodesicSpray Gamma) (regularPhaseDomain U) p)
    (q : Phase4) (hq : q∈Metric.ball p F.radius) (hn : tensorQuad (g q.1) q.2=0)
    (t : ℝ) (ht : t∈Ioo (-F.radius) F.radius) :
    tensorQuad (g (F.flow (q,t)).1) (F.flow (q,t)).2=0 :=
  (geodesic_flow_energy_conserved U hU g Gamma hg hm p F q hq t ht).trans hn

def leviCivitaGeodesicFlow (U : Set Coordinate4) (hU : IsOpen U)
    (E D : TensorField4) (hE : SmoothMatrixOn U E) (hD : SmoothMatrixOn U D)
    (x v : Coordinate4) (hx : x∈U) (hv : v≠0) :
    LocalPhaseFlow (geodesicSpray (frameLeviCivita E D)) (regularPhaseDomain U) (x,v) :=
  localGeodesicFlow U hU (frameLeviCivita E D)
    (levi_civita_field_smooth U hU (frameMetricField E) (inverseFrameMetricField D)
      (frame_metric_smooth U E hE) (inverse_frame_metric_smooth U D hD)) x v hx hv

theorem local_levi_civita_null_geodesics (U : Set Coordinate4) (hU : IsOpen U)
    (E D : TensorField4) (hED : ∀ y∈U, E y*D y=1) (hDE : ∀ y∈U, D y*E y=1)
    (hE : SmoothMatrixOn U E) (hD : SmoothMatrixOn U D)
    (x v : Coordinate4) (hx : x∈U) (hv : v≠0) :
    ∃ F : LocalPhaseFlow (geodesicSpray (frameLeviCivita E D)) (regularPhaseDomain U) (x,v),
      ∀ q∈Metric.ball (x,v) F.radius, tensorQuad (frameMetricField E q.1) q.2=0 →
        ∀ t∈Ioo (-F.radius) F.radius,
          tensorQuad (frameMetricField E (F.flow (q,t)).1) (F.flow (q,t)).2=0 := by
  let F := leviCivitaGeodesicFlow U hU E D hE hD x v hx hv
  have hm : MetricCompatibleOn U (frameMetricField E) (frameLeviCivita E D) :=
    levi_civita_field_metric_compatible U hU (frameMetricField E) (inverseFrameMetricField D)
      (fun y _ => frame_metric_symmetric E y)
      (fun y hy => inverse_frame_metric_left E D y (hED y hy) (hDE y hy))
      (fun y hy => inverse_frame_metric_right E D y (hED y hy) (hDE y hy))
  refine ⟨F,?_⟩
  intro q hq hn t ht
  exact geodesic_flow_null_preserved U hU (frameMetricField E) (frameLeviCivita E D)
    (frame_metric_smooth U E hE) hm (x,v) F q hq hn t ht

#print axioms geodesic_energy_derivative
#print axioms geodesic_flow_energy_conserved
#print axioms geodesic_flow_null_preserved
#print axioms leviCivitaGeodesicFlow
#print axioms local_levi_civita_null_geodesics
end
end ChatgptAudit.Screen015
