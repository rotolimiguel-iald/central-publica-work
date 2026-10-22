[OPEN — ficha anterior aos vetores fixos do grupo modular]

2026-09-15T00:47:22.429681-03:00

ADAPTAR: for the SAME S,F,Delta_nu=FS,T_nu and U_t, prove a vector fixed by S and F in their actual domains is fixed by every U_t. Use the exact composition domain, the inverse identity to get T_nu*x=(1/2)*x, then the existing damped phase intertwiner with rankOne(x,x) and (1/2)I to read g_t(1/2)=1/4. Evaluate at x and cancel norm squared only when x is nonzero; handle zero separately. Damping is also (1/4)*x, so existing U*damping=phase fixes x. Then consume the preceding fixed pair of star(e_delta)*e_delta to exhibit those same modular-fixed vectors. Consumer is core covariance for equality of U with pi(lambda)R_-t on pi(N)Lambda(z_delta), followed by a separate totality argument. No new CFC, imaginary group, generator, GNS, weight, normalization, or claim that a single vector is cyclic. Delta30 standalone/review pending when fiche created; source frozen and target delivery depends on its acceptance. One generic private phase/eigenvector adapter is anticipated; no generic CFC framework.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351AverageFixedPair.lean:60` — `3365edaea7a5b9a10db767dae3bc5517298673232151234d9510e6ec1773804c`

```lean
theorem regularAverage_square_fixed_pair (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    ∃ A : scalarWeightStarCore P,
      A.val.val = star (regularAverage P δ)*regularAverage P δ ∧
      scalarClosedTomita P ⟨scalarWeightStarEmbedding P A,
        scalarWeightStar_mem_closedTomitaDomain P A⟩ = scalarWeightStarEmbedding P A ∧
      ∃ hF : scalarWeightStarEmbedding P A ∈ scalarTomitaAdjointDomain P,
        scalarTomitaAdjoint P ⟨scalarWeightStarEmbedding P A,hF⟩ =
          scalarWeightStarEmbedding P A
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarTomitaSquare.lean:40` — `ca781e13f5857fcb348fd2cc1e68a2fb3397ae352b168e9ba9a6425517634a2a`

```lean
theorem scalarTomitaSquare_domain_iff (x : ScalarGNSHilbert P) :
    x ∈ (scalarTomitaSquare P).domain ↔
      ∃ hx : x ∈ scalarClosedTomitaDomain P,
        scalarClosedTomita P ⟨x,hx⟩ ∈ scalarTomitaAdjointDomain P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarTomitaSquare.lean:45` — `ca781e13f5857fcb348fd2cc1e68a2fb3397ae352b168e9ba9a6425517634a2a`

```lean
theorem scalarTomitaSquare_apply (x : scalarTomitaSquareDomain P) :
    scalarTomitaSquare P x = scalarTomitaAdjoint P
      ⟨scalarClosedTomita P (scalarTomitaSquareInput P x),
        scalarTomitaSquareInput_image_mem P x⟩
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarTomitaResolvent.lean:24` — `50e9437f0a572187103933b7b4847b82599da0a687e439a3b7ab48735e2c3127`

```lean
theorem scalarTomitaResolvent_inverse (x : (scalarTomitaSquare P).domain) :
    scalarTomitaResolvent P ((x : ScalarGNSHilbert P)+scalarTomitaSquare P x)=
      (x : ScalarGNSHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarTomitaImaginaryPowers.lean:29` — `b8871f05b5b9605a8b193a8ed25346d79eac72d025d3ad95c8f9c884f28b4e52`

```lean
theorem scalarTomitaImaginaryPower_damping (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (resolventDampingOperator (scalarTomitaResolvent P) x)=
      resolventPhaseOperator (scalarTomitaResolvent P) t x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryIntertwining.lean:57` — `789f68095379e02a203191b258c359787c12b24c1282f34d39835dc5347c76d5`

```lean
theorem resolventPhaseOperator_intertwines (T Q R : H →L[ℂ] H)
    (hT : IsSelfAdjoint T) (hQ : IsSelfAdjoint Q) (h : T*R=R*Q) (t : ℝ) :
    resolventPhaseOperator T t * R = R * resolventPhaseOperator Q t
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventPhaseFunctions.lean:79` — `8eb2f7fb43b753d739c276b9e98655529860084586e311d94c8984cde361aea5`

```lean
theorem resolventPhaseFunction_continuous (t : ℝ) : Continuous (resolventPhaseFunction t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Unital.lean:693` — `f67b42738af5e91dbef05da3f0b841de4bf421bb6b54114688d7c08649761e86`

```lean
lemma cfc_algebraMap (r : R) (f : R → R) : cfc f (algebraMap R A r) = algebraMap R A (f r)
```

Buscas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_modular_fixed_vectors\20260915_004657_689673\searches.json. Ausência nominal não é ausência universal. Consulta2 V2 e consulta curta do revisor de 15/09 relidas: usar o intertwiner de fase já especializado, sem construir o grupo de (1/2)I. rankOne_apply consultado na Mathlib Analysis/InnerProductSpace/LinearMap.lean:322; enumeração de fornecedores registra também o contexto desse import.
