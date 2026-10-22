import TGLExt.V351RegularFlowAbsorption
set_option autoImplicit false
set_option maxHeartbeats 1500000
open TGLExt TGLV350.Regular
noncomputable section
example (P : SiteProfile) (t : ℝ) :
    (regularFlowAbsorptionUnitary P).val * shift t *
        star (regularFlowAbsorptionUnitary P).val = regularUnitary P (-t) := by
  exact regularUnitary_shift_conjugate P t
