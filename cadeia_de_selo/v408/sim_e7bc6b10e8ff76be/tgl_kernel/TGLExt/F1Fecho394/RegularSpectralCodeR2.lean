import TGLExt.V350UnitIntervalShiftProjection
import TGLExt.V350StrongOperatorField
/-! Concrete norm-preserving regular spectral code. The range is not yet
identified with the weight GNS completion, and no modular identification is assumed. -/
set_option autoImplicit false
set_option maxErrors 3
set_option maxHeartbeats 900000
noncomputable section
namespace F1Fecho.RegularSpectralCode
open TGLV350.Regular MeasureTheory Filter
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def testLp : RegularHilbert H →L[ℂ] RegularHilbert (RegularHilbert H) :=
  (testEmbeddingCLM (H := H)).compLpL 2 volume

theorem testLp_ae (f : RegularHilbert H) :
    testLp f =ᵐ[volume] fun a : ℝ => testVector (f a) :=
  (testEmbeddingCLM (H := H)).coeFn_compLpL f

theorem testLp_norm (f : RegularHilbert H) : ‖testLp f‖ = ‖f‖ := by
  rw [Lp.norm_def,Lp.norm_def]
  congr 1
  apply eLpNorm_congr_norm_ae
  filter_upwards [testLp_ae f] with a ha
  rw [ha,testVector_norm]

def code : RegularHilbert H →L[ℂ] RegularHilbert (RegularHilbert H) :=
  (operatorFieldLift (shiftIntegralFamily (H := H))).comp testLp

theorem code_ae (f : RegularHilbert H) :
    code f =ᵐ[volume] fun a : ℝ => shift a (testVector (f a)) := by
  filter_upwards [operatorFieldLift_ae (shiftIntegralFamily (H := H)) (testLp f),
    testLp_ae f] with a ha hb
  change operatorFieldLift (shiftIntegralFamily (H := H)) (testLp f) a = _
  rw [ha,hb]
  rfl

theorem code_norm (f : RegularHilbert H) : ‖code f‖ = ‖f‖ := by
  rw [Lp.norm_def,Lp.norm_def]
  congr 1
  apply eLpNorm_congr_norm_ae
  filter_upwards [code_ae f] with a ha
  rw [ha,shift_norm,testVector_norm]

def codeIsometry : RegularHilbert H →ₗᵢ[ℂ] RegularHilbert (RegularHilbert H) where
  toLinearMap := code.toLinearMap
  norm_map' := code_norm

theorem code_injective : Function.Injective (code (H := H)) :=
  codeIsometry.injective

theorem code_fibre (C : H →L[ℂ] H) (f : RegularHilbert H) :
    code (fibre C f) = fibre (fibre C) (code f) := by
  apply Lp.ext
  filter_upwards [code_ae (fibre C f),fibre_ae C f,
    fibre_ae (fibre C) (code f),code_ae f] with a ha hb hc hd
  rw [ha,hb,hc,hd,← fibre_testVector]
  exact congrArg (fun T : RegularHilbert H →L[ℂ] RegularHilbert H => T (testVector (f a)))
    (shift_commutes_fibre a C)

end F1Fecho.RegularSpectralCode
#print axioms F1Fecho.RegularSpectralCode.testLp_ae
#print axioms F1Fecho.RegularSpectralCode.testLp_norm
#print axioms F1Fecho.RegularSpectralCode.code_ae
#print axioms F1Fecho.RegularSpectralCode.code_norm
#print axioms F1Fecho.RegularSpectralCode.codeIsometry
#print axioms F1Fecho.RegularSpectralCode.code_injective
#print axioms F1Fecho.RegularSpectralCode.code_fibre
