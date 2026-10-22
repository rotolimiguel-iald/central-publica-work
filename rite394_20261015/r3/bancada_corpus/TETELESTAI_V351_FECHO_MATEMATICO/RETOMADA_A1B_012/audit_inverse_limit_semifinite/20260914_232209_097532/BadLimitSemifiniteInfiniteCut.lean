import TGLExt.V351InverseLimitSemifiniteness
open TGLExt TGLV350.Regular
open scoped ENNReal
example (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) (a : scalarWeightLeftIdeal P) :
    scalarInverseLimitWeight P (TGLV351.positiveSquare P (a.val*regularDomainCut P δ)) = ⊤ := by
  exact scalarInverseLimitWeight_domainCut_finite P δ hδ a
