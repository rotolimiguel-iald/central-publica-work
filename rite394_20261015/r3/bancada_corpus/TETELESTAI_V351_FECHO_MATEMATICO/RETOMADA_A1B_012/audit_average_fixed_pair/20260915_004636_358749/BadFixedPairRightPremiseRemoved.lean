import TGLExt.V351AverageFixedPair
open TGLExt TGLV350.Regular
example (P : SiteProfile) (A : scalarWeightStarCore P) (hstar : star A = A) :
    scalarClosedTomita P ⟨scalarWeightStarEmbedding P A,
      scalarWeightStar_mem_closedTomitaDomain P A⟩ = scalarWeightStarEmbedding P A ∧
    ∃ hF : scalarWeightStarEmbedding P A ∈ scalarTomitaAdjointDomain P,
      scalarTomitaAdjoint P ⟨scalarWeightStarEmbedding P A,hF⟩ =
        scalarWeightStarEmbedding P A :=
  scalarWeightStar_fixed_pair_of_polarRight P A hstar
