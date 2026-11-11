import TGLExt.V350ScalarGNSLinear
import TGLExt.V350StrongOperatorField

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory
noncomputable section

def scalarGNSLeftProduct (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (A : finiteDualLeftIdeal P) :
    finiteDualLeftIdeal P :=
  ⟨B * A.val,finiteDualLeftIdeal_left_mul P B A.val A.property⟩

/-- The ambient left action uses the same dual orbit at every coordinate.
Restriction to the completed GNS range is a separate step. -/
def scalarGNSAmbientAction (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ]
      RegularHilbert (RegularHilbert (TowerHilbert P)) :=
  operatorFieldLift (dualIntegralFamily B.val)

theorem scalarGNSAmbientAction_norm_le (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    ‖scalarGNSAmbientAction P B‖ ≤ ‖B.val‖ :=
  operatorFieldLift_norm_le (dualIntegralFamily B.val)

theorem scalarGNSAmbientAction_intertwines (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (A : finiteDualLeftIdeal P) :
    scalarGNSAmbientAction P B (scalarGNSOrbit P A) =
      scalarGNSOrbit P (scalarGNSLeftProduct P B A) := by
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae (dualIntegralFamily B.val) (scalarGNSOrbit P A),
    scalarGNSOrbit_ae P A,scalarGNSOrbit_ae P (scalarGNSLeftProduct P B A)]
    with s h1 h2 h3
  change operatorFieldLift (dualIntegralFamily B.val) (scalarGNSOrbit P A) s = _
  rw [h1,h3]
  change dualAmbient s B.val (scalarGNSOrbit P A s) = _
  rw [h2]
  change dualAmbient s B.val ((↑(Real.sqrt dualHaarFactor) : ℂ) •
    dualAmbient s A.val.val (regularVacuum P)) =
    (↑(Real.sqrt dualHaarFactor) : ℂ) • dualAmbient s (B.val*A.val.val) (regularVacuum P)
  rw [map_smul,map_mul]
  rfl

#print axioms scalarGNSLeftProduct
#print axioms scalarGNSAmbientAction
#print axioms scalarGNSAmbientAction_norm_le
#print axioms scalarGNSAmbientAction_intertwines
end
end TGLV350.Regular
