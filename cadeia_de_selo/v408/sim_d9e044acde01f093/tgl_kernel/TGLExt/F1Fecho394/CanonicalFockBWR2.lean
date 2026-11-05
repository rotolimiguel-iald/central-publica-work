import TGLExt.F1Fecho394.CanonicalZeroSectorFlowR3
import TGLExt.F1Fecho394.CanonicalTensorResolventR3
/-! Bisognano-Wichmann equality for the actual Weyl/vacuum Tomita graph on
exactly the already constructed canonical Fock space. The negative modular
parameter is explicit; the positive KMS convention is a separate theorem.
No modular-flow equality is assumed as a record field. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open UniformSpace
namespace F1Fecho.CanonicalFockBW
open TGLExt.ImportedSQ F1Rede.BosonicSectors F1Rede.BosonicFock F1Rede.CanonicalWedge
open F1Fecho.CanonicalFockPolar F1Fecho.CanonicalZeroSector
open F1Fecho.ExponentialTomita F1Fecho.WedgePairTomita ORDEM016.D6

theorem tensorGamma_zero (u:H1≃ₗᵢ[ℂ]H1) (x:TensorHilbert 0) : tensorGamma u 0 x=x := by
  refine Completion.induction_on x (isClosed_eq (tensorGamma u 0).continuous continuous_id) ?_
  intro z
  rw [tensorGamma_coe]
  rfl

theorem gamma_zero_component (u:H1≃ₗᵢ[ℂ]H1) (x:F) : gamma u x 0=x 0 := by
  apply Subtype.ext
  exact tensorGamma_zero u (x 0)

theorem actualModularFlow_eq_gamma_apply (t:ℝ) (x:F) :
    actualModularFlow t x=gamma (B0 (-(2*Real.pi*t))) x := by
  apply lp.ext
  funext n
  cases n with
  | zero => rw [modularFlow_zero_component,gamma_zero_component]
  | succ n => exact TensorCoordinates.positive_component_modularFlow n t x

theorem actualModularFlow_eq_gamma :
    actualModularFlow=(fun t=>gamma (B0 (-(2*Real.pi*t)))) := by
  funext t
  ext1 x
  exact actualModularFlow_eq_gamma_apply t x

theorem canonical_pair_tomita :
    PairTomitaAnalyticRealizationMeasured (algebra KWR) vacuum JF
      (fun t=>gamma (B0 (-(2*Real.pi*t)))) := by
  rw [←actualModularFlow_eq_gamma]
  exact actual_spectral_pair_measured

end F1Fecho.CanonicalFockBW
#print axioms F1Fecho.CanonicalFockBW.tensorGamma_zero
#print axioms F1Fecho.CanonicalFockBW.gamma_zero_component
#print axioms F1Fecho.CanonicalFockBW.actualModularFlow_eq_gamma_apply
#print axioms F1Fecho.CanonicalFockBW.actualModularFlow_eq_gamma
#print axioms F1Fecho.CanonicalFockBW.canonical_pair_tomita
