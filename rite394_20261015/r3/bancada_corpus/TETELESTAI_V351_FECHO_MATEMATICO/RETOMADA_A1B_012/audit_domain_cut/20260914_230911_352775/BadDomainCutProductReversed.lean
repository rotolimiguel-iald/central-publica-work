import TGLExt.V351RegularDomainCut
open TGLExt TGLV350.Regular
example (P : SiteProfile) (ε δ : ℝ) (hε : 0 < ε) (hδ : 0 < δ) :
    (δ⁻¹ : ℂ) • 1 ≤ regularInverseGeneratorCutoff P ε *
      (regularDomainCut P δ).val * (regularDomainCut P δ).val := by
  exact regularDomainCut_product_bound P ε δ hε hδ
