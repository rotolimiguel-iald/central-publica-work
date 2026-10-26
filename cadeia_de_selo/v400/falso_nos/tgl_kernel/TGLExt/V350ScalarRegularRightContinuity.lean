import TGLExt.V350ScalarRegularPolarCommutation
import TGLExt.V350ScalarGNSStrongContinuity

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit Filter
open scoped Topology
noncomputable section

theorem regularUnitary_norm_le_one (P : SiteProfile) (t : ℝ) :
    ‖regularUnitary P t‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
  intro f
  change ‖fibre (modularFlowCLM P t) (shift t f)‖ ≤ 1*‖f‖
  rw [modularFlowCLM_isometry,fibre_isometry_norm,shift_norm,one_mul]

theorem scalarGNSRegular_strongly_continuous (P : SiteProfile) (z : ScalarGNSHilbert P) :
    Continuous (fun t : ℝ => scalarGNSRepresentation P (regularRightCoreElement P t) z) := by
  apply continuous_iff_continuousAt.mpr
  intro t
  exact scalarGNSRepresentation_tendsto_of_uniformly_bounded P
    (regularRightCoreElement P) (regularRightCoreElement P t) 1
    (regularUnitary_norm_le_one P) (fun f => (regular_strongly_continuous P f).continuousAt) z

/-- Strong continuity of the same right group follows from its identification
by the already constructed polar factor, not from operator-norm continuity. -/
theorem regularRightGNS_strongly_continuous (P : SiteProfile) (z : ScalarGNSHilbert P) :
    Continuous (fun t : ℝ => regularRightGNS P t z) := by
  have hc := (scalarTomitaPolarFactor P).continuous.comp
    ((scalarGNSRegular_strongly_continuous P (scalarTomitaPolarFactor P z)).comp continuous_neg)
  apply hc.congr
  intro t
  have h := scalarTomitaPolarFactor_regular_left P t (scalarTomitaPolarFactor P z)
  simpa only [Function.comp_def,regularRightCoreElement_star,
    scalarTomitaPolarFactor_involutive P z] using h

#print axioms regularUnitary_norm_le_one
#print axioms scalarGNSRegular_strongly_continuous
#print axioms regularRightGNS_strongly_continuous
end
end TGLV350.Regular
