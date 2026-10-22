import TGLExt.V351ScalarRightActionLimits
open TGLExt TGLV350.Regular
example (P : SiteProfile) (t : ℝ) (A : scalarWeightLeftIdeal P) :
    scalarWeightGNSEmbedding P (scalarRegularRightProduct P t A) =
      antiunitaryConjugate (scalarTomitaPolarFactor P)
        (scalarGNSRepresentation P (regularRightCoreElement P t))
          (scalarWeightGNSEmbedding P A) := by
  exact scalarRightAction_regular P t A
