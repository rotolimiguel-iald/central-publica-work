import TGLExt.V351ScalarImaginaryRightTransport

set_option autoImplicit false
open TGLV350.Regular TGLExt ChatgptAudit
noncomputable section
example (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (homogeneousRightGNS (matrixUnitRightData P N i j) x)=
      modularPhase t (Real.log (localEigenvalue P N i j)) •
        homogeneousRightGNS (matrixUnitRightData P N i j) (scalarTomitaImaginaryPower P t x) := by
  exact matrixUnit_imaginaryPower_right_scaling P N i j t x
end
