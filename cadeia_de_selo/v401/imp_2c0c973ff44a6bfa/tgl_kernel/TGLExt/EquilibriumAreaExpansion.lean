-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_020 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.EquilibriumCongruenceControls

set_option autoImplicit false
set_option maxHeartbeats 7000000
namespace ChatgptAudit.Flow020
open Matrix Filter Topology Set ChatgptAudit.Flow019
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem screen_area_continuous_zero (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (hg : SmoothMatrixOn U g)
    (p v : Coordinate4) (P : EquilibriumScreenData U g Gamma p v) :
    ContinuousAt (inducedArea g P.curve P.screen.vectors) 0 := by
  apply induced_area_continuous g P.curve P.screen.vectors 0
  · intro a b
    have hd := smooth_matrix_differentiableAt U hU g hg p
      (P.neighborhood_subset P.point_mem) a b
    have hc : ContinuousAt (fun y => g y a b) (P.curve 0) := by
      simpa only [P.curve_zero] using hd.continuousAt
    exact hc.comp P.curve_tangent.continuousAt
  · exact P.screen.continuous_zero

theorem screen_curve_eventually_neighborhood (U : Set Coordinate4) (g : TensorField4)
    (Gamma : ConnectionField4) (p v : Coordinate4) (P : EquilibriumScreenData U g Gamma p v) :
    ∀ᶠ t in 𝓝[<] (0:ℝ), P.curve t∈P.neighborhood := by
  have hmem : P.neighborhood∈𝓝 (P.curve 0) := by
    rw [P.curve_zero]
    exact P.neighborhood_open.mem_nhds P.point_mem
  exact (P.curve_tangent.continuousAt.eventually hmem).filter_mono nhdsWithin_le_nhds

theorem screen_matter_continuous_at (U : Set Coordinate4) (hU : IsOpen U)
    (g T : TensorField4) (Gamma : ConnectionField4)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (p v : Coordinate4) (P : EquilibriumScreenData U g Gamma p v)
    (t : ℝ) (ht : P.curve t∈P.neighborhood) (hc : ContinuousAt P.curve t) :
    ContinuousAt (fun s => tensorQuad (T (P.curve s)) (P.velocity (P.curve s))) t := by
  have hV := smooth_vector_differentiableAt P.neighborhood P.neighborhood_open
    P.velocity P.velocity_smooth (P.curve t) ht
  have hq := tensor_quad_field_continuous T P.velocity (P.curve t)
    (fun a b => ((hT a b).differentiableAt
      (hU.mem_nhds (P.neighborhood_subset ht))).continuousAt)
    (fun a => (hV a).continuousAt)
  exact hq.comp hc

theorem screen_matter_continuous_zero (U : Set Coordinate4) (hU : IsOpen U)
    (g T : TensorField4) (Gamma : ConnectionField4)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (p v : Coordinate4) (P : EquilibriumScreenData U g Gamma p v) :
    ContinuousAt (fun s => tensorQuad (T (P.curve s)) (P.velocity (P.curve s))) 0 :=
  screen_matter_continuous_at U hU g T Gamma hT p v P 0
    (by rw [P.curve_zero]; exact P.point_mem) P.curve_tangent.continuousAt

theorem screen_matter_continuous_past (U : Set Coordinate4) (hU : IsOpen U)
    (g T : TensorField4) (Gamma : ConnectionField4)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (p v : Coordinate4) (P : EquilibriumScreenData U g Gamma p v) :
    ∀ᶠ t in 𝓝[<] (0:ℝ),
      ContinuousAt (fun s => tensorQuad (T (P.curve s)) (P.velocity (P.curve s))) t := by
  filter_upwards [screen_curve_eventually_neighborhood U g Gamma p v P,
    P.screen.curve_tangent] with t ht hc
  exact screen_matter_continuous_at U hU g T Gamma hT p v P t ht hc.continuousAt

theorem area_quadratic_limit (theta area : ℝ → ℝ) (thetaPrime : ℝ)
    (htheta : HasDerivAt theta thetaPrime 0) (htheta0 : theta 0=0)
    (harea : ContinuousAt area 0)
    (hrate : ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt area (theta t*area t) t) :
    Tendsto (fun t => (area t-area 0)/t^2) (𝓝[<] 0) (𝓝 (thetaPrime*area 0/2)) := by
  apply primitive_quadratic_limit (fun t => theta t*area t) (fun t => area t-area 0)
    (thetaPrime*area 0)
  · filter_upwards [hrate] with t ht
    exact ht.sub_const (area 0)
  · exact harea.sub continuousAt_const
  · simp
  · have hs : Tendsto (fun t => theta t/t) (𝓝[<] 0) (𝓝 thetaPrime) := by
      simpa only [zero_add,htheta0,sub_zero,smul_eq_mul,div_eq_mul_inv,mul_comm]
        using htheta.tendsto_slope_zero_left
    have ha : Tendsto area (𝓝[<] (0:ℝ)) (𝓝 (area 0)) :=
      harea.tendsto.mono_left nhdsWithin_le_nhds
    simpa only [div_mul_eq_mul_div] using hs.mul ha

theorem screen_area_quadratic_limit (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (hg : SmoothMatrixOn U g)
    (hG : SmoothConnectionOn U Gamma) (p v : Coordinate4)
    (P : EquilibriumScreenData U g Gamma p v)
    (ht : ∀ i j a, Gamma p i a j=Gamma p j a i) :
    Tendsto (fun t => (inducedArea g P.curve P.screen.vectors t-1)/t^2)
      (𝓝[<] 0) (𝓝 (-tensorQuad (coordinateRicci Gamma p) v/2)) := by
  have hz : vectorExpansion Gamma P.velocity (P.curve 0)=0 := by
    rw [P.curve_zero]
    exact equilibrium_screen_expansion_zero U g Gamma p v P
  have hlim := area_quadratic_limit
    (fun t => vectorExpansion Gamma P.velocity (P.curve t))
    (inducedArea g P.curve P.screen.vectors) _
    (equilibrium_screen_focusing U g Gamma hG p v P ht) hz
    (screen_area_continuous_zero U hU g Gamma hg p v P) P.area_rate
  simpa only [equilibrium_screen_area_initial U g Gamma p v P,mul_one] using hlim

#print axioms screen_area_continuous_zero
#print axioms screen_curve_eventually_neighborhood
#print axioms screen_matter_continuous_at
#print axioms screen_matter_continuous_zero
#print axioms screen_matter_continuous_past
#print axioms area_quadratic_limit
#print axioms screen_area_quadratic_limit
end
end ChatgptAudit.Flow020
