import TGLExt.V351ScalarGNSClosedness
open TGLExt TGLV350.Regular
example (P : SiteProfile) (r : ℝ) (A : scalarWeightLeftIdeal P) :
    scalarGNSCutMap P r (scalarWeightGNSEmbedding P A) =
      (2 : ℂ) • dualOrbitRepresentation A.val.val (scalarCutVacuum P r) := by
  exact scalarGNSCutMap_weight_embedding P r A
