-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_021 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.QuadraticStateResponse

set_option autoImplicit false
set_option maxHeartbeats 7000000
namespace ChatgptAudit.Micro021
open Matrix Filter Topology Set ChatgptAudit.Flow019 ChatgptAudit.Flow020
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section
variable {ι : Type} [Fintype ι] {p : ι → ℝ} (X : DiagonalStateCurve p)

def microscopicAreaError (eta : ℝ) (area : ℝ → ℝ) (t : ℝ) : ℝ :=
  (finiteEntropy (X.weights t)-finiteEntropy p)-eta*(area t-area 0)

def microscopicHeatError (rate : ℝ) (heat : ℝ → ℝ) (t : ℝ) : ℝ :=
  heat t-rate/(2*Real.pi)*modularIncrement p (X.weights t)

theorem residual_entropy_decomposition (rate eta : ℝ) (area heat : ℝ → ℝ) (t : ℝ) :
    horizonBalancePrimitive rate eta area heat t=
      microscopicHeatError X rate heat t+
        rate/(2*Real.pi)*diagonalRelativeEntropy (X.weights t) p+
        rate/(2*Real.pi)*microscopicAreaError X eta area t := by
  unfold horizonBalancePrimitive microscopicHeatError microscopicAreaError
  rw [relative_entropy_identity]
  ring

theorem microscopic_residual_coefficient (hp : ∀ i, 0<p i) (rate eta : ℝ) (area heat : ℝ → ℝ)
    (hheat : Tendsto (fun t => microscopicHeatError X rate heat t/t^2) (𝓝[<] 0) (𝓝 0))
    (harea : Tendsto (fun t => microscopicAreaError X eta area t/t^2) (𝓝[<] 0) (𝓝 0)) :
    Tendsto (fun t => horizonBalancePrimitive rate eta area heat t/t^2) (𝓝[<] 0)
      (𝓝 (rate/(2*Real.pi)*(diagonalFisher p (X.tangent 0)/2))) := by
  have hc : Tendsto (fun _ : ℝ => rate/(2*Real.pi)) (𝓝[<] 0) (𝓝 (rate/(2*Real.pi))) :=
    tendsto_const_nhds
  have hl := (hheat.add (hc.mul (relative_entropy_curve_quadratic_limit X hp))).add (hc.mul harea)
  have hf : (fun t => horizonBalancePrimitive rate eta area heat t/t^2)=
      (fun t => microscopicHeatError X rate heat t/t^2+
        rate/(2*Real.pi)*(diagonalRelativeEntropy (X.weights t) p/t^2)+
        rate/(2*Real.pi)*(microscopicAreaError X eta area t/t^2)) := by
    funext t
    rw [residual_entropy_decomposition X rate eta area heat t]
    ring
  simpa only [←hf,zero_add,mul_zero,add_zero] using hl

theorem microscopic_clausius_iff_zero_tangent (hp : ∀ i, 0<p i) (rate eta : ℝ) (hrate : rate≠0)
    (area heat : ℝ → ℝ)
    (hheat : Tendsto (fun t => microscopicHeatError X rate heat t/t^2) (𝓝[<] 0) (𝓝 0))
    (harea : Tendsto (fun t => microscopicAreaError X eta area t/t^2) (𝓝[<] 0) (𝓝 0)) :
    Tendsto (fun t => horizonBalancePrimitive rate eta area heat t/t^2) (𝓝[<] 0) (𝓝 0) ↔
      X.tangent 0=0 := by
  rw [past_zero_limit_iff _ _ (microscopic_residual_coefficient X hp rate eta area heat hheat harea)]
  constructor
  · intro hh
    have hc : rate/(2*Real.pi)≠0 := div_ne_zero hrate (mul_ne_zero (by norm_num) Real.pi_ne_zero)
    have hf := (mul_eq_zero.mp hh).resolve_left hc
    apply (diagonal_fisher_zero_iff p (X.tangent 0) hp).mp
    linarith
  · intro hq
    rw [(diagonal_fisher_zero_iff p (X.tangent 0) hp).mpr hq]
    simp

theorem quadratic_matching_gives_clausius (p q : ι → ℝ)
    (hs : ∑ i, p i=1) (hq : ∑ i, q i=0) (hp : ∀ i, 0<p i)
    (rate eta : ℝ) (area heat : ℝ → ℝ)
    (hheat : Tendsto (fun t => microscopicHeatError (quadraticStateCurve p q hs hq) rate heat t/t^2)
      (𝓝[<] 0) (𝓝 0))
    (harea : Tendsto (fun t => microscopicAreaError (quadraticStateCurve p q hs hq) eta area t/t^2)
      (𝓝[<] 0) (𝓝 0)) :
    Tendsto (fun t => horizonBalancePrimitive rate eta area heat t/t^2) (𝓝[<] 0) (𝓝 0) := by
  have hh := microscopic_residual_coefficient (quadraticStateCurve p q hs hq) hp rate eta area heat hheat harea
  simpa [quadraticStateCurve,diagonalFisher] using hh

theorem geometric_microscopic_compatibility
    (U : Set Coordinate4) (hU : IsOpen U) (g : TensorField4) (Gamma : ConnectionField4)
    (T : TensorField4) (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (x v : Coordinate4) (P : EquilibriumScreenData U g Gamma x v)
    (ht : ∀ i j a, Gamma x i a j=Gamma x j a i)
    (hp : ∀ i, 0<p i) (rate eta : ℝ) (hrate : rate≠0)
    (hheat : Tendsto (fun t => microscopicHeatError X rate
      (constructedHeat P T rate hU hg hT) t/t^2) (𝓝[<] 0) (𝓝 0))
    (harea : Tendsto (fun t => microscopicAreaError X eta
      (inducedArea g P.curve P.screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0)) :
    eta*tensorQuad (coordinateRicci Gamma x) v=
      2*Real.pi*tensorQuad (T x) v+diagonalFisher p (X.tangent 0) := by
  have hm := microscopic_residual_coefficient X hp rate eta
    (inducedArea g P.curve P.screen.vectors) (constructedHeat P T rate hU hg hT) hheat harea
  have hgq := screen_clausius_coefficient P T rate eta hU hg hG hT ht
    (screenHeatExtension P T rate hU hg hT)
  have he := tendsto_nhds_unique hgq hm
  unfold clausiusCoefficient at he
  have hc : rate/(2*Real.pi)*(diagonalFisher p (X.tangent 0)/2)=
      rate/2*(diagonalFisher p (X.tangent 0)/(2*Real.pi)) := by ring
  rw [hc] at he
  have hh := mul_left_cancel₀ (div_ne_zero hrate (by norm_num : (2:ℝ)≠0)) he
  field_simp [Real.pi_ne_zero] at hh
  nlinarith only [hh]

#print axioms residual_entropy_decomposition
#print axioms microscopic_residual_coefficient
#print axioms microscopic_clausius_iff_zero_tangent
#print axioms quadratic_matching_gives_clausius
#print axioms geometric_microscopic_compatibility
end
end ChatgptAudit.Micro021
