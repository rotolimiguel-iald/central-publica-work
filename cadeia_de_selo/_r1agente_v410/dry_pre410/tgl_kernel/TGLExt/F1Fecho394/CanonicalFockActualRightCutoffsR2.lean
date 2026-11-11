import TGLExt.F1Fecho394.CanonicalFockPolarRightCutoffsR13
import TGLExt.F1Fecho394.CanonicalFockRightPolarBridgeR5

/-! Candidate specialization to the already constructed polar antiunitary.
No right-action hypothesis is added: the regular generator membership is a
proved consequence of the same closed Tomita operator and positive root.
The full scaled trace and finite projection are separate obligations. -/
set_option autoImplicit false
set_option Elab.async false
set_option maxHeartbeats 400000
noncomputable section
namespace F1Fecho.CanonicalFockActualRightCutoffs
open TGLV350.Regular (hilbertPositiveSqrt)
open F1Fecho.CanonicalFockRegular F1Fecho.RegularPositiveFlow
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockWeightPolar
open F1Fecho.CanonicalFockPolarRight F1Fecho.CanonicalFockRightPolar

theorem actualRegularResolvent_right :
    (⟨regularSpectralResolvent fockFlow, regularSpectralResolvent_mem fockFlow M⟩ :
      core.toStarSubalgebra) ∈ scalarPolarRightAlgebra scalarTomitaPolarFactor :=
  regularSpectralResolvent_right scalarTomitaPolarFactor scalarPolarRightAlgebra_regular_mem

theorem actualInverseCutoff_right (ε : ℝ) (hε : 0 < ε) :
    (⟨regularInverseGeneratorCutoff fockFlow ε,
      regularInverseGeneratorCutoff_mem fockFlow M ε⟩ : core.toStarSubalgebra) ∈
        scalarPolarRightAlgebra scalarTomitaPolarFactor :=
  regularInverseGeneratorCutoff_right scalarTomitaPolarFactor
    scalarPolarRightAlgebra_regular_mem ε hε

theorem actualInverseCutoff_root_right (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow ε) ∈ core,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow ε), h⟩ :
        core.toStarSubalgebra) ∈ scalarPolarRightAlgebra scalarTomitaPolarFactor :=
  regularInverseGeneratorCutoff_sqrt_right scalarTomitaPolarFactor
    scalarPolarRightAlgebra_regular_mem ε hε

end F1Fecho.CanonicalFockActualRightCutoffs
#print axioms F1Fecho.CanonicalFockActualRightCutoffs.actualRegularResolvent_right
#print axioms F1Fecho.CanonicalFockActualRightCutoffs.actualInverseCutoff_right
#print axioms F1Fecho.CanonicalFockActualRightCutoffs.actualInverseCutoff_root_right
