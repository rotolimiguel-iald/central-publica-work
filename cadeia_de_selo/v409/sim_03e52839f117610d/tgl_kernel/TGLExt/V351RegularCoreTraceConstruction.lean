import TGLExt.V351QuadraticTrace
import TGLExt.V351InverseLimitFiniteMinorants
import TGLExt.V351InverseLimitFaithful
import TGLExt.V351InverseLimitScaling

set_option autoImplicit false
universe u

namespace TGLV350.Regular
open TGLExt TGLV351
noncomputable section

/-- The already constructed weight, with the complete contract on its original
regular core. Every field reuses a proved supplier; no normalization is changed. -/
def scalarInverseLimitTraceData (P : SiteProfile) : RegularCoreTraceData.{u} P where
  value := scalarInverseLimitWeight P
  zero := scalarInverseLimitWeight_zero P
  additive := scalarInverseLimitWeight_add P
  homogeneous := scalarInverseLimitWeight_scale P
  monotone := scalarInverseLimitWeight_mono P
  faithful := scalarInverseLimitWeight_faithful P
  normal := scalarInverseLimitWeight_normal P
  semifinite := scalarInverseLimitWeight_finite_minorants P (scalarInverseLimitWeight_tracial P)
  tracial := scalarInverseLimitWeight_tracial P
  dual_scaling := scalarInverseLimitWeight_dual P

#print axioms scalarInverseLimitTraceData
end
end TGLV350.Regular
