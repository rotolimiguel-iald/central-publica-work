import TGLExt.V351ScalarTomitaImaginaryConjugation

set_option autoImplicit false
open TGLV350.Regular TGLExt ChatgptAudit
noncomputable section
example (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P
      (scalarTomitaImaginaryPower P t ((scalarTomitaPolarFactor P).symm x)) =
        (2 : ℝ) • scalarTomitaImaginaryPower P t x := by
  exact scalarTomitaImaginaryPower_polar_conjugate P t x
end
