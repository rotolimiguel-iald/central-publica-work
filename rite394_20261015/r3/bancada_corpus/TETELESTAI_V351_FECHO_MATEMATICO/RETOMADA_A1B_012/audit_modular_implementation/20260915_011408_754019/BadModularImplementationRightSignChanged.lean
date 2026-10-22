import TGLExt.V351ModularImplementation
open TGLExt TGLV350.Regular
example (P : SiteProfile) (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t x =
      scalarGNSRepresentation P (regularRightCoreElement P t) (regularRightGNS P t x) :=
  scalarTomitaImaginaryPower_eq_regular_implementation P t x
