import TGLExt.F1Fecho394.CoefficientTomitaSquareR2
import TGLExt.F1Fecho394.CanonicalFockRegularCoreR2
import TGLExt.F1Fecho394.CanonicalFockBWR2
import TGLExt.F1Fecho394.WeylAntiunitaryR4

/-! Concrete coefficient conjugation on the SAME canonical bosonic Fock.
The boost/reflection commutation is derived on the total exponential family.
The coefficient square and flow reuse the actual Weyl-vacuum modular data.
No identification with the regular-weight GNS is assumed here. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.CoefficientFockConjugation
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.Antilinear F1Rede.CanonicalWedge
open F1Fecho.CanonicalFockRegular F1Fecho.ExponentialTomita F1Fecho.CanonicalFockPolar
open TGLV350.Regular

def conjugateBoost (t:ℝ) : F→L[ℂ]F where
  toFun x := JF (fockFlow.U t (JF x))
  map_add' x y := by simp only [map_add]
  map_smul' c x := by
    simp only [map_smulₛₗ,map_smul,starRingEnd_apply,star_star,RingHom.id_apply]
  cont := JF.continuous.comp ((fockFlow.U t).continuous.comp JF.continuous)

theorem conjugateBoost_eq (t:ℝ) :
    conjugateBoost t=(fockFlow.U t).toLinearIsometry.toContinuousLinearMap := by
  apply WeylConstruction.clm_ext_total exponential exponential_total
  intro x
  change canonicalFockJ (gamma (B0 (-(2*Real.pi*t)))
    (canonicalFockJ (exponential x))) = gamma (B0 (-(2*Real.pi*t))) (exponential x)
  unfold canonicalFockJ
  rw [gammaJ_exponential,gamma_exponential,gammaJ_exponential,gamma_exponential]
  rw [CanonicalWedgeFlow.Jcandidate_boost,Jcandidate_involutive]

theorem JF_boost (t:ℝ) (x:F) : JF (fockFlow.U t x)=fockFlow.U t (JF x) := by
  have h := congrArg (fun A:F→L[ℂ]F => A (JF x)) (conjugateBoost_eq t)
  change JF (fockFlow.U t (JF (JF x)))=fockFlow.U t (JF x) at h
  have hi : JF (JF x)=x := canonicalFockJ_involutive x
  rwa [hi] at h

def coefficientJ : RegularHilbert F ≃ₛₗᵢ[starRingEnd ℂ] RegularHilbert F :=
  CoefficientTwistedConjugation.twist fockFlow JF

theorem coefficientJ_involutive : Function.Involutive coefficientJ :=
  CoefficientTwistedConjugation.twist_involutive fockFlow JF canonicalFockJ_involutive JF_boost

abbrev coefficientRoot := FibreModularCalculus.liftedRoot modularR modularR_nonneg modularR_injective
abbrev coefficientS := CoefficientTomitaSquare.coefficientS modularR modularR_nonneg modularR_injective fockFlow JF

theorem coefficient_square :
    ORDEM016.D6.antilinearSquareGraph (CoefficientTomitaSquare.graph coefficientRoot coefficientJ)=
      (resolventGraphOperator (fibre modularR)
        (FibreModularCalculus.fibre_operator_injective modularR modularR_injective)).graph :=
  CoefficientTomitaSquare.coefficient_square_graph modularR modularR_nonneg modularR_le_one
    modularR_injective fockFlow JF canonicalFockJ_involutive JF_boost

theorem coefficient_modular_flow (t:ℝ) (f:RegularHilbert F) :
    FibreModularCalculus.liftedFlow modularR modularR_nonneg modularR_le_one
      modularR_injective modularR_complement_injective t f=
      fibre ((fockFlow.U t).toLinearIsometry.toContinuousLinearMap) f := by
  rw [FibreModularCalculus.liftedFlow_eq_fibre]
  have he : resolventImaginaryPower modularR modularR_nonneg modularR_le_one
      modularR_injective modularR_complement_injective t=fockFlow.U t :=
    congrFun CanonicalFockBW.actualModularFlow_eq_gamma t
  rw [he]
end F1Fecho.CoefficientFockConjugation
#print axioms F1Fecho.CoefficientFockConjugation.JF_boost
#print axioms F1Fecho.CoefficientFockConjugation.coefficientJ_involutive
#print axioms F1Fecho.CoefficientFockConjugation.coefficient_square
#print axioms F1Fecho.CoefficientFockConjugation.coefficient_modular_flow
