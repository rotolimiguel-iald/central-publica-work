[OPEN — ficha anterior à fidelidade do peso limite]

# A1(b): um corte já basta para a fidelidade do limite

2026-09-14T22:40:01.259796-03:00

Prove scalarInverseCutoffWeight P 1 faithful on PositiveCoreInput P using B_1=R, membership of the existing sqrt(R) in N and faithfulness of the SAME vacuum dual weight. The ORIGINAL positive_sqrt_injective and resolventSquareRoot_dense imply injectivity and dense range of the bounded CFC root; adapt the wrapper only. If star sqrt(R) X sqrt(R)=0, injectivity cancels the left root and continuity/dense range cancels the right root, giving X=0. Then scalarInverseLimitWeight dominates n=0 (epsilon_0=1), so it is faithful. No new GNS/root/resolvent and no need to prove every regulator inverse injective. Consumer: faithful field of RegularCoreTraceData for the candidate value. Neither semifinitude, traciality nor dual scaling follows from this.

ADAPTAR: o domínio do fornecedor resolventSquareRoot_dense é a imagem da raiz LIMITADA CFC.sqrt R. Não confundir essa raiz com o operador parcial resolventSquareRoot. A dupla injetividade/densidade é reutilizada; não é pressuposta a fidelidade do limite.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventSquareRoot.lean:13` — `6a1ad3a2fa7041aa45d56b2448e18a5fce6b90e9e069f045df89483ecb1e3f90`

```lean
theorem positive_sqrt_injective (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) : Function.Injective (CFC.sqrt R : H →L[ℂ] H)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventSquareRoot.lean:47` — `6a1ad3a2fa7041aa45d56b2448e18a5fce6b90e9e069f045df89483ecb1e3f90`

```lean
theorem resolventSquareRoot_dense (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) : Dense ((resolventSquareRoot R hR hi).domain : Set H)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarDualWeightFaithfulness.lean:54` — `3ff3e31e49de71f035a425202ef1796be18da2b46bdb60a7f6c34b8a2e73f61c`

```lean
theorem dualQuadraticIntegral_vacuum_faithful (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hm : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A) :
    dualQuadraticIntegral A (regularVacuum P) = 0 ↔ A = 0
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:98` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
theorem regularSpectralResolvent_injective (P : SiteProfile) :
    Function.Injective (regularSpectralResolvent P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:84` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
theorem regularSpectralResolvent_nonneg (P : SiteProfile) :
    0 ≤ regularSpectralResolvent P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:43` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_one (P : SiteProfile) :
    regularInverseGeneratorCutoff P 1 = regularSpectralResolvent P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:125` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_sqrt_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),h⟩ :
        (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:94` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
theorem scalarInverseCutoffWeight_le_limit (P : SiteProfile) (n : ℕ) (X : PositiveCoreInput P) :
    scalarInverseCutoffWeight P (1/((n : ℝ)+1)) X ≤ scalarInverseLimitWeight P X
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:90` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
theorem scalarInverseLimitWeight_zero (P : SiteProfile) :
    scalarInverseLimitWeight P (PositiveCoreInput.zero P) = 0
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_limit_weight_faithful\20260914_223938_431313\searches.json. Ausência nominal nos recortes não é ausência universal.
