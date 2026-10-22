import TGLExt.V351ScalarImaginaryLeftTransport
set_option autoImplicit false
set_option maxHeartbeats 1500000
open TGLExt ChatgptAudit TGLV350.Regular
noncomputable section
example (P : SiteProfile) (N : ℕ) (i j : chainIdx N) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t
        (scalarGNSRepresentation P
          (star (homogeneousRightCoreElement (matrixUnitRightData P N i j))) x) =
      modularPhase t (Real.log (localEigenvalue P N i j)) •
        scalarGNSRepresentation P
          (star (homogeneousRightCoreElement (matrixUnitRightData P N i j)))
          (scalarTomitaImaginaryPower P t x) := by
  exact matrixUnit_imaginaryPower_left_scaling P N i j t x
