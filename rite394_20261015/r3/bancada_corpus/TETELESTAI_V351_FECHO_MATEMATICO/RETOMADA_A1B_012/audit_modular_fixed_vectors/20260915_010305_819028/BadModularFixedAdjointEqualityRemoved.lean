import TGLExt.V351ModularFixedVectors
open TGLExt TGLV350.Regular
example (P : SiteProfile) (x : ScalarGNSHilbert P)
    (hS : x ∈ scalarClosedTomitaDomain P) (hF : x ∈ scalarTomitaAdjointDomain P)
    (hxS : scalarClosedTomita P ⟨x,hS⟩ = x) (t : ℝ) :
    scalarTomitaImaginaryPower P t x = x :=
  scalarTomitaImaginaryPower_fixed_of_fixed_pair P x hS hF hxS
