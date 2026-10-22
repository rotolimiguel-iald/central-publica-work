import TGLExt.V351ScalarImaginaryCoreAction
set_option autoImplicit false
set_option maxHeartbeats 1500000
open TGLExt TGLV350.Regular
noncomputable section
example (P : SiteProfile) (t : ℝ)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (scalarGNSRepresentation P A x) =
      scalarGNSRepresentation P (regularRightCoreElement P t * A)
        (scalarTomitaImaginaryPower P t x) := by
  exact scalarTomitaImaginaryPower_core_conjugation P t A x
