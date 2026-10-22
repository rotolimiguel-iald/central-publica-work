[OPEN — ficha anterior ao par fixo de Tomita]

2026-09-15T00:31:25.635489-03:00

ADAPTAR: within original scalarWeightStarCore/GNS/S/F, prove a selfadjoint A with A.val in scalarPolarRightAlgebra has Lambda(A) simultaneously fixed by S and F. Construct the actual ScalarRightAdjointPair (right and adjoint vectors both Lambda(A)) from polar-right identity and the old left-action identity; use maximality, not a supplied fixed-vector hypothesis. Then exhibit such an A whose ambient value is EXACTLY regularAverage(delta)* star-squared, specifically star(e_delta)*e_delta, delta>0. E-membership follows from accepted algebra operations and preceding delta29; finite domain from e_delta finite and left ideal, selfadjoint by star laws. No new operator/GNS/weight/J, no average-selfadjoint assertion, no normalization or trace. Consumer: scalarTomitaSquare_domain_iff and scalarTomitaResolvent_inverse for the next eigenvector/implementator step. These later consequences are not delivered merely by naming them. Delta29 standalone audit/review in progress at fiche, wait for acceptance before final consumer delivery.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351AveragePolarRight.lean:170` — `9a982e09a318e7c306c20a9c5baf0d07a6354b34d3cf2e6cc3cf168968f334cc`

```lean
theorem regularAverage_mem_scalarPolarRightAlgebra (P : SiteProfile)
    (δ : ℝ) (hδ : 0 < δ) :
    (⟨regularAverage P δ,regularAverage_mem P δ⟩ :
      (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRightAdjointPair.lean:128` — `6db80e5fe729f47c9f8d5b9764a24ec5c14ddc8a845d38f8606b5a3abc974a7b`

```lean
theorem scalarRightAdjointPair_maximal {P : SiteProfile}
    {R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P} (d : ScalarRightAdjointPair P R) :
    ∃ hv : d.vector ∈ scalarTomitaAdjointDomain P,
      scalarTomitaAdjoint P ⟨d.vector,hv⟩ = d.adjointVector
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightTomitaIdentification.lean:71` — `d4b3043d6d76a9934d9778a0b1b7e604c26e8ffb2c1e3a7755964496ad520822`

```lean
theorem scalarClosedTomita_extends_weight_star (P : SiteProfile)
    (A : scalarWeightStarCore P) :
    scalarClosedTomita P ⟨scalarWeightStarEmbedding P A,
      scalarWeightStar_mem_closedTomitaDomain P A⟩ = scalarWeightStarEmbedding P (star A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightAction.lean:38` — `7875ce91559689c1e951f28d3a1d005dc17aae2af1db677242a27d38e40dfb5c`

```lean
theorem scalarWeightGNSAction_intertwines (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (A : scalarWeightLeftIdeal P) :
    scalarGNSRepresentation P B (scalarWeightGNSEmbedding P A) =
      scalarWeightGNSEmbedding P (scalarWeightLeftProduct P B A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351AntiunitaryResolventPhase.lean:85` — `4cd800bb6c465a55d6387ecef3517ccb57c2a087cc2e8e6a35ded13273516bd8`

```lean
theorem antiunitaryConjugate_selfadjoint (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) : IsSelfAdjoint (antiunitaryConjugate J T)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightDomain.lean:22` — `e83ada9b5abbf2c179c28b03d3c020be83861681ba3ae450999c1c64ea8e2f0f`

```lean
theorem HasFiniteScalarSquare.left_mul (P : SiteProfile)
    (B A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hA : HasFiniteScalarSquare P A) : HasFiniteScalarSquare P (B*A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualSemifiniteIdeal.lean:108` — `63c88763eaa1c837ed0a28057d044a7627e57f993f4fcc4c7bddf44dcea07cbe`

```lean
theorem regularAverage_hasFiniteDualSquare (P : TGLExt.SiteProfile)
    (h : ℝ) (hh : 0 < h) : HasFiniteDualSquare (regularAverage P h)
```

Buscas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_average_fixed_pair\20260915_003105_354376\searches.json. Ausência nominal não é ausência universal. Consulta2 V2 lida; delta29 fornece a ação direita da média, usada no quadrado auto-adjunto.
