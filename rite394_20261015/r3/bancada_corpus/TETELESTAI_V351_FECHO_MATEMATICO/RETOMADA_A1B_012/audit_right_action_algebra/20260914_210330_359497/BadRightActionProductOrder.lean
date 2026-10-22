import TGLExt.V351ScalarRightActionAlgebra
open TGLExt TGLV350.Regular
example (P : SiteProfile) (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : ScalarPolarRight P b) (hc : ScalarPolarRight P c)
    (A : scalarWeightLeftIdeal P) :
    ∃ h : A.val*(b*c) ∈ scalarWeightLeftIdeal P,
      scalarWeightGNSEmbedding P ⟨A.val*(b*c),h⟩ =
        antiunitaryConjugate (scalarTomitaPolarFactor P)
          (scalarGNSRepresentation P (star (c*b))) (scalarWeightGNSEmbedding P A) := by
  exact scalarPolarRight_mul P b c hb hc A
