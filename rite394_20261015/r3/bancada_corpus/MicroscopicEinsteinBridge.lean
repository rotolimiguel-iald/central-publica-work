import MicroscopicClausiusBridge

set_option autoImplicit false
set_option maxHeartbeats 8000000
namespace ChatgptAudit.Micro021
open Matrix Filter Topology Set ChatgptAudit.Flow019 ChatgptAudit.Flow020
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

structure QuadraticScreenMatching (ι : Type) [Fintype ι]
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x v : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x v) (T : TensorField4) (rate eta : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U) where
  reference : ι → ℝ
  response : ι → ℝ
  positive : ∀ i, 0<reference i
  normalized : ∑ i, reference i=1
  trace_response : ∑ i, response i=0
  heat_matching : Tendsto (fun t => microscopicHeatError
      (quadraticStateCurve reference response normalized trace_response) rate
      (constructedHeat P T rate hU hg hT) t/t^2) (𝓝[<] 0) (𝓝 0)
  area_matching : Tendsto (fun t => microscopicAreaError
      (quadraticStateCurve reference response normalized trace_response) eta
      (inducedArea g P.curve P.screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0)

theorem matching_produces_clausius {ι : Type} [Fintype ι]
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x v : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x v) (T : TensorField4) (rate eta : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (M : QuadraticScreenMatching ι P T rate eta hU hg hT) :
    Tendsto (fun t => horizonBalancePrimitive rate eta
      (inducedArea g P.curve P.screen.vectors) (constructedHeat P T rate hU hg hT) t/t^2)
      (𝓝[<] 0) (𝓝 0) :=
  quadratic_matching_gives_clausius M.reference M.response M.normalized M.trace_response M.positive
    rate eta _ _ M.heat_matching M.area_matching

theorem einstein_from_quadratic_microscopic_matching (ι : Type) [Fintype ι]
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (A B T : TensorField4) (rate eta : ℝ) (hrate : rate≠0) (heta : eta≠0)
    (hAB : ∀ x∈U, A x*B x=1) (hBA : ∀ x∈U, B x*A x=1)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (hsT : ∀ x∈U, (T x)ᵀ=T x)
    (hdT : ∀ x∈U, ∀ j, tensorFieldDivergence (inverseFrameMetricField B)
      (frameLeviCivita A B) T x j=0)
    (hmatch : ∀ x (hx : x∈U) v (hv : v≠0) (hn : tensorQuad (frameMetricField A x) v=0),
      Nonempty (QuadraticScreenMatching ι
        (localEquilibriumScreen U hU A B hAB hBA hA hB x v hx hv hn)
        T rate eta hU (frame_metric_smooth U A hA) hT)) :
    ∃ cosmological : ℝ, ∀ x∈U,
      frameEinsteinTensor A B x+cosmological • frameMetricField A x=(2*Real.pi/eta) • T x := by
  apply einstein_from_constructed_clausius U hU A B hAB hBA hA hB T hT rate eta
    hconn hrate heta hsT hdT
  intro x hx v hv hn
  obtain ⟨M⟩ := hmatch x hx v hv hn
  exact matching_produces_clausius
    (localEquilibriumScreen U hU A B hAB hBA hA hB x v hx hv hn)
    T rate eta hU (frame_metric_smooth U A hA) hT M

#print axioms matching_produces_clausius
#print axioms einstein_from_quadratic_microscopic_matching
end
end ChatgptAudit.Micro021
