import TGLV350.ScalarTomitaPolarResolvent
import TGLV350.AntiunitaryPositiveConjugation
set_option autoImplicit false
set_option synthInstance.maxHeartbeats 200000
namespace TGLV350.Regular
open TGLExt
noncomputable section
variable (P : SiteProfile)
local instance polarEndRealComm : SMulCommClass ℝ
    (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) where
  smul_comm r A B := by
    apply ContinuousLinearMap.ext
    intro x
    change r • A (B x)=A (r • B x)
    exact (map_smul_of_tower A r (B x)).symm
local instance polarEndRealTower : IsScalarTower ℝ
    (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) where
  smul_assoc r A B := by
    apply ContinuousLinearMap.ext
    intro x
    rfl
example : 0 ≤ CFC.sqrt (scalarTomitaResolvent P) := CFC.sqrt_nonneg _
end
end TGLV350.Regular
