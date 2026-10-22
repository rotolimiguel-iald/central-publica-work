[OPEN — ficha anterior à pertença da média à álgebra direita]

2026-09-15T00:20:30.703642-03:00

ADAPTAR: prove the EXISTING regularAverage delta (delta>0) belongs to the EXISTING scalarPolarRightAlgebra, supplying the right action for z=e*e needed by ScalarRightAdjointPair with the same weight/GNS/S/F. Construct bounded finite sums of the existing regular unitaries b_n=(n+1)^(-1) sum_{k<n+1} lambda_(delta*k/(n+1)). Exact interval partition gives e_delta=b_n e_(delta/(n+1)), so contraction bounds and existing small-average convergence give strong convergence; commuting factors and the existing adjoint convergence give strong-star. Apply already proved bounded strong-star closure twice. This avoids a new generic Riemann-integral framework, operator-norm continuity, Bochner integration in B(H), alternate average, GNS or trace. The fixed S/F vector, modular implementator identity, Q and traciality remain later obligations. No claim average is selfadjoint; use e*e for later fixed vector.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:164` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
theorem scalarPolarRightAlgebra_regular_mem (P : SiteProfile) (t : ℝ) :
    regularRightCoreElement P t ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionLimits.lean:26` — `ab55b5a1e05d6f8317bc61e0a303b960dc7e9888999e03cbb1c63287e4b37b9d`

```lean
theorem scalarRightAction_closed_of_bounded_strongStar (P : SiteProfile)
    {ι : Type*} {l : Filter ι} [NeBot l]
    (b : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (C : ℝ)
    (hbound : ∀ i, ‖(b i).val‖ ≤ C)
    (hstrong : ∀ x, Tendsto (fun i => (b i).val x) l (𝓝 (B.val x)))
    (hadjoint : ∀ x, Tendsto (fun i => (star (b i)).val x) l (𝓝 ((star B).val x)))
    (A : scalarWeightLeftIdeal P)
    (hact : ∀ i, ∃ hi : A.val * b i ∈ scalarWeightLeftIdeal P,
      scalarWeightGNSEmbedding P ⟨A.val*b i,hi⟩ =
        antiunitaryConjugate (scalarTomitaPolarFactor P)
          (scalarGNSRepresentation P (star (b i))) (scalarWeightGNSEmbedding P A)) :
    ∃ hAB : A.val * B ∈ scalarWeightLeftIdeal P,
      scalarWeightGNSEmbedding P ⟨A.val*B,hAB⟩ =
        antiunitaryConjugate (scalarTomitaPolarFactor P)
          (scalarGNSRepresentation P (star B)) (scalarWeightGNSEmbedding P A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularApproximation.lean:41` — `d8e7830989e0ba3d71f0e8495f54414cedc12a9eac16b1bc0501f15342b8bb44`

```lean
theorem regularAverage_apply (P : TGLExt.SiteProfile) (h : ℝ)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    regularAverage P h v = h⁻¹ • ∫ t in 0..h, regularUnitary P t v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularApproximation.lean:68` — `d8e7830989e0ba3d71f0e8495f54414cedc12a9eac16b1bc0501f15342b8bb44`

```lean
theorem regularAverage_tendsto_identity (P : TGLExt.SiteProfile)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    Tendsto (fun h : ℝ => regularAverage P h v) (𝓝[≠] 0) (𝓝 v)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ContractionAdjointLimit.lean:51` — `75c191ec2110441b6554ca7beddfc7806f3e3aac6e879e8461f7632cfa78eaa5`

```lean
theorem regularAverage_star_tendsto_identity (P : TGLExt.SiteProfile)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    Tendsto (fun h : ℝ => star (regularAverage P h) v) (𝓝[≠] 0) (𝓝 v)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorIntegral.lean:59` — `7ee0e23dc3319a72734ce420f540251f59a27561fa61221d6ab5f98b2989dfa7`

```lean
theorem operatorIntegral_commutes (F : Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularTowerRepresentation.lean:23` — `21638dcca0d86b6a62050dee85212ee74cf07d783e43bdf6fecd28a04fb5b41f`

```lean
theorem regular_mul (P : SiteProfile) (s t : ℝ) :
    regularUnitary P s * regularUnitary P t = regularUnitary P (s+t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\MeasureTheory\Integral\IntervalIntegral\Basic.lean:1115` — `c71e2f79bad2a043032169e58b596779588df187470be980e5198b9bafe5be18`

```lean
theorem sum_integral_adjacent_intervals {a : ℕ → ℝ} {n : ℕ}
    (hint : ∀ k < n, IntervalIntegrable f μ (a k) (a <| k + 1)) :
    ∑ k ∈ Finset.range n, ∫ x in a k..a <| k + 1, f x ∂μ = ∫ x in (a 0)..(a n), f x ∂μ
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\MeasureTheory\Integral\IntervalIntegral\Basic.lean:954` — `c71e2f79bad2a043032169e58b596779588df187470be980e5198b9bafe5be18`

```lean
theorem integral_comp_add_right (d) : (∫ x in a..b, f (x + d)) = ∫ x in a + d..b + d, f x
```

Buscas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_average_polar_right\20260915_002009_898046\searches.json. Ausência nominal não é ausência universal. Consulta2 corrigida V2 já lida; rota reduzida à partição exata da integral e limites existentes.
