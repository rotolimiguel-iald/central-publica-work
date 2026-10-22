import TGLExt.SignedGibbsCoverage

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.SignedGibbsFinite
open Matrix Filter Topology Set TGLExt ChatgptAudit
  ChatgptAudit.SignedGibbsCoverage ChatgptAudit.FullSourceResponse
  ChatgptAudit.FiniteResponseRecord ChatgptAudit.GeneralMetric ChatgptAudit.SignedCoverage
noncomputable section

/-- Exactly ten entropy limits suffice; no response function on all directions is an input. -/
theorem ten_entropy_limits_reconstruct_source {k : ℝ} (hk : 0<k)
    (g gi T : Tensor4) (hi : gi*g=1) (hg : gᵀ=g) (hT : Tᵀ=T)
    (s : ResponseSamples)
    (hlim : ∀ i : Fin 10,
      Tendsto (fun t => entropyProbe k (traceReverse g gi T) (probeDirections i) t/t^2)
        (𝓝[<] (0:ℝ)) (𝓝 (s i))) :
    decodeSource g gi s=T := by
  have hs : s=sampleResponse (calibratedPointResponse g gi T) := by
    funext i
    exact tendsto_nhds_unique (hlim i)
      (source_entropy_limit hk g gi T hg hT (probeDirections i))
  rw [hs]
  exact ten_responses_reconstruct_source g gi T hi hg hT

/-- The same finite readout is sufficient for ten modular limits. -/
theorem ten_modular_limits_reconstruct_source {k : ℝ} (hk : 0<k)
    (g gi T : Tensor4) (hi : gi*g=1) (hg : gᵀ=g) (hT : Tᵀ=T)
    (s : ResponseSamples)
    (hlim : ∀ i : Fin 10,
      Tendsto (fun t => modularProbe k (traceReverse g gi T) (probeDirections i) t/t^2)
        (𝓝[<] (0:ℝ)) (𝓝 (s i))) :
    decodeSource g gi s=T := by
  have hs : s=sampleResponse (calibratedPointResponse g gi T) := by
    funext i
    exact tendsto_nhds_unique (hlim i)
      (source_modular_limit hk g gi T hg hT (probeDirections i))
  rw [hs]
  exact ten_responses_reconstruct_source g gi T hi hg hT

#print axioms ten_entropy_limits_reconstruct_source
#print axioms ten_modular_limits_reconstruct_source
end
end ChatgptAudit.SignedGibbsFinite
