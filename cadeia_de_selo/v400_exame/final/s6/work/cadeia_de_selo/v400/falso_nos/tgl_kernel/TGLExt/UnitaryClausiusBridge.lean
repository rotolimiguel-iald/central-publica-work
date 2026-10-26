-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_022 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.UnitaryEntropyResponse

set_option autoImplicit false
set_option maxHeartbeats 8500000
namespace ChatgptAudit.Unitary022
open Matrix Filter Topology Set ChatgptAudit.Micro021 ChatgptAudit.Flow019 ChatgptAudit.Flow020
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem unitary_matching_gives_clausius (a b frequency u v : ℝ)
    (hs : u^2+v^2=1) (hu : 0<u) (hv : 0<v) (rate eta : ℝ) (area heat : ℝ → ℝ)
    (hheat : Tendsto (fun t => microscopicHeatError (unitaryStateCurve a b frequency u v hs)
      rate heat t/t^2) (𝓝[<] 0) (𝓝 0))
    (harea : Tendsto (fun t => microscopicAreaError (unitaryStateCurve a b frequency u v hs)
      eta area t/t^2) (𝓝[<] 0) (𝓝 0)) :
    Tendsto (fun t => horizonBalancePrimitive rate eta area heat t/t^2) (𝓝[<] 0) (𝓝 0) := by
  have hh := microscopic_residual_coefficient (unitaryStateCurve a b frequency u v hs)
    (base_weights_positive u v hu hv) rate eta area heat hheat harea
  have hf : diagonalFisher (baseWeights u v) ((unitaryStateCurve a b frequency u v hs).tangent 0)=0 := by
    simp [unitaryStateCurve,pairTangent,diagonalFisher]
  rw [hf] at hh
  simpa only [zero_div,mul_zero] using hh

theorem unitary_heat_matching_requires_matter
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x direction : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x direction) (T : TensorField4)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun y => T y i j) U)
    (a b frequency u v rate : ℝ) (hs : u^2+v^2=1) (hu : 0<u) (hv : 0<v) (hrate : rate≠0)
    (hheat : Tendsto (fun t => microscopicHeatError (unitaryStateCurve a b frequency u v hs)
      rate (constructedHeat P T rate hU hg hT) t/t^2) (𝓝[<] 0) (𝓝 0)) :
    tensorQuad (T x) direction= -unitaryResponse a b frequency u v/Real.pi := by
  have hl := unitary_heat_error_limit a b frequency u v rate hs hu hv
    (constructedHeat P T rate hU hg hT) (-rate*tensorQuad (T x) direction/2)
    (constructed_heat_quadratic_limit P T rate hU hg hT)
  have he := tendsto_nhds_unique hl hheat
  have hx : rate*(Real.pi*tensorQuad (T x) direction+unitaryResponse a b frequency u v)=0 := by
    field_simp [Real.pi_ne_zero] at he
    nlinarith only [he]
  have hh := (mul_eq_zero.mp hx).resolve_left hrate
  apply (eq_div_iff Real.pi_ne_zero).mpr
  nlinarith only [hh]

theorem positive_response_blocks_nonnegative_heat_matching
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x direction : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x direction) (T : TensorField4)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun y => T y i j) U)
    (a b frequency u v rate : ℝ) (hs : u^2+v^2=1) (hu : 0<u) (hv : 0<v) (hrate : rate≠0)
    (hL : 0<unitaryResponse a b frequency u v) (hTnull : 0≤tensorQuad (T x) direction) :
    ¬Tendsto (fun t => microscopicHeatError (unitaryStateCurve a b frequency u v hs)
      rate (constructedHeat P T rate hU hg hT) t/t^2) (𝓝[<] 0) (𝓝 0) := by
  intro hh
  have he := unitary_heat_matching_requires_matter P T hU hg hT a b frequency u v rate
    hs hu hv hrate hh
  have hn : -unitaryResponse a b frequency u v/Real.pi<0 :=
    div_neg_of_neg_of_pos (neg_lt_zero.mpr hL) Real.pi_pos
  rw [←he] at hn
  exact (not_lt_of_ge hTnull) hn

structure UnitaryScreenMatching
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x direction : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x direction) (T : TensorField4) (rate eta : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun y => T y i j) U) where
  axis_a : ℝ
  axis_b : ℝ
  frequency : ℝ
  initial_u : ℝ
  initial_v : ℝ
  axis_normalized : axis_a^2+axis_b^2=1
  initial_normalized : initial_u^2+initial_v^2=1
  positive_u : 0 < initial_u
  positive_v : 0 < initial_v
  heat_matching : Tendsto (fun t => microscopicHeatError
    (unitaryStateCurve axis_a axis_b frequency initial_u initial_v initial_normalized) rate
    (constructedHeat P T rate hU hg hT) t/t^2) (𝓝[<] 0) (𝓝 0)
  area_matching : Tendsto (fun t => microscopicAreaError
    (unitaryStateCurve axis_a axis_b frequency initial_u initial_v initial_normalized) eta
    (inducedArea g P.curve P.screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0)

theorem unitary_screen_matching_produces_clausius
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x direction : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x direction) (T : TensorField4) (rate eta : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun y => T y i j) U)
    (M : UnitaryScreenMatching P T rate eta hU hg hT) :
    Tendsto (fun t => horizonBalancePrimitive rate eta (inducedArea g P.curve P.screen.vectors)
      (constructedHeat P T rate hU hg hT) t/t^2) (𝓝[<] 0) (𝓝 0) :=
  unitary_matching_gives_clausius M.axis_a M.axis_b M.frequency M.initial_u M.initial_v
    M.initial_normalized M.positive_u M.positive_v rate eta _ _ M.heat_matching M.area_matching

theorem einstein_from_unitary_microscopic_matching
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (A B T : TensorField4) (rate eta : ℝ) (hrate : rate≠0) (heta : eta≠0)
    (hAB : ∀ x∈U, A x*B x=1) (hBA : ∀ x∈U, B x*A x=1)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B)
    (hT : ∀ i j, DifferentiableOn ℝ (fun y => T y i j) U)
    (hsT : ∀ x∈U, (T x)ᵀ=T x)
    (hdT : ∀ x∈U, ∀ j, tensorFieldDivergence (inverseFrameMetricField B)
      (frameLeviCivita A B) T x j=0)
    (hmatch : ∀ x (hx : x∈U) direction (hv : direction≠0)
      (hn : tensorQuad (frameMetricField A x) direction=0),
      Nonempty (UnitaryScreenMatching
        (localEquilibriumScreen U hU A B hAB hBA hA hB x direction hx hv hn)
        T rate eta hU (frame_metric_smooth U A hA) hT)) :
    ∃ cosmological : ℝ, ∀ x∈U,
      frameEinsteinTensor A B x+cosmological • frameMetricField A x=(2*Real.pi/eta) • T x := by
  apply einstein_from_constructed_clausius U hU A B hAB hBA hA hB T hT rate eta
    hconn hrate heta hsT hdT
  intro x hx direction hv hn
  obtain ⟨M⟩ := hmatch x hx direction hv hn
  exact unitary_screen_matching_produces_clausius
    (localEquilibriumScreen U hU A B hAB hBA hA hB x direction hx hv hn)
    T rate eta hU (frame_metric_smooth U A hA) hT M

#print axioms unitary_matching_gives_clausius
#print axioms unitary_heat_matching_requires_matter
#print axioms positive_response_blocks_nonnegative_heat_matching
#print axioms unitary_screen_matching_produces_clausius
#print axioms einstein_from_unitary_microscopic_matching
end
end ChatgptAudit.Unitary022
