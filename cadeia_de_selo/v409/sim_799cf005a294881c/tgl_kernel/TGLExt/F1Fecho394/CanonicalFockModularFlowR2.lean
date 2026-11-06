import TGLExt.F1Fecho394.CanonicalFockGraphRealizationR3
import TGLExt.V351ResolventImaginaryContinuity
import TGLExt.O16.ContentContractProposal
/-! Actual spectral imaginary powers of the Weyl/vacuum Tomita square.
The flow is constructed by CFC from that operator, and is not renamed Gamma(B0).
Equality to the prescribed geometric boost remains a separate obligation. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 200000
noncomputable section
namespace F1Fecho.CanonicalFockPolar
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.CanonicalWedge
open F1Fecho.ExponentialTomita F1Fecho.WedgePairTomita TGLV350.Regular ORDEM016.D6

def actualModularFlow : ℝ → F ≃ₗᵢ[ℂ] F :=
  resolventImaginaryPower modularR modularR_nonneg modularR_le_one
    modularR_injective modularR_complement_injective

theorem actualModularFlow_zero (x : F) : actualModularFlow 0 x=x :=
  resolventImaginaryPower_zero _ _ _ _ _ x

theorem actualModularFlow_add (s t : ℝ) (x : F) :
    actualModularFlow s (actualModularFlow t x)=actualModularFlow (s+t) x :=
  resolventImaginaryPower_add _ _ _ _ _ s t x

theorem actualModularFlow_continuous (x : F) : Continuous (fun t => actualModularFlow t x) :=
  resolventImaginaryPower_strongly_continuous _ _ _ _ _ x

theorem actualModularFlow_readout (t : ℝ) (x : F) :
    actualModularFlow t (resolventDampingOperator modularR x)=resolventPhaseOperator modularR t x :=
  resolventImaginaryPower_damping _ _ _ _ _ t x

/-- Analytic realization for the constructed spectral flow, not for the target Gamma boost. -/
theorem actual_spectral_pair_measured :
    PairTomitaAnalyticRealizationMeasured (algebra KWR) vacuum JF actualModularFlow :=
  ⟨actualGraphRealization,rfl,actualModularFlow_readout⟩

end F1Fecho.CanonicalFockPolar
#print axioms F1Fecho.CanonicalFockPolar.actualModularFlow
#print axioms F1Fecho.CanonicalFockPolar.actualModularFlow_zero
#print axioms F1Fecho.CanonicalFockPolar.actualModularFlow_add
#print axioms F1Fecho.CanonicalFockPolar.actualModularFlow_continuous
#print axioms F1Fecho.CanonicalFockPolar.actualModularFlow_readout
#print axioms F1Fecho.CanonicalFockPolar.actual_spectral_pair_measured
