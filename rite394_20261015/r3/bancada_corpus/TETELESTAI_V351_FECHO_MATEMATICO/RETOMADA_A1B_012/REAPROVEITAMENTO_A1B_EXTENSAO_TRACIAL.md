[OPEN — ficha anterior à extensão tracial]

# A1(b): o núcleo existente basta para a igualdade tracial

2026-09-14T23:50:30.408996-03:00

ADAPTAR: for the SAME scalarInverseLimitWeight, prove bounded square values survive strong limits, tau(positiveSquare(regularSandwich a delta)) <= tau(positiveSquare a), then traciality on the EXISTING finiteDualStarCore iff traciality on all regularCoreAlgebra. Consumer: RegularCoreTraceData.tracial, V351RegularCoreTraceContract.lean:59 (recheck line). No traciality assumed globally, no new weight/core/GNS, no replacement trace contract. The core equality remains an explicit missing lemma; this extension alone does not inhabit the trace contract. Strong convergence of adjoints is taken from existing sandwich theorem, never presumed for arbitrary strong limits.

A prova usa Fatou em cada corte e a comutação já paga com as médias. Não compara sanduíches por ordem do conjugador. As buscas nominais abaixo são complementadas pela leitura dos enunciados e fontes destes fornecedores. Nenhuma ausência universal é alegada.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:94` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
theorem scalarInverseCutoffWeight_le_limit (P : SiteProfile) (n : ℕ) (X : PositiveCoreInput P) :
    scalarInverseCutoffWeight P (1/((n : ℝ)+1)) X ≤ scalarInverseLimitWeight P X
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:109` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
theorem scalarInverseLimitWeight_mono (P : SiteProfile) (X Y : PositiveCoreInput P) (hXY : X ≤ Y) :
    scalarInverseLimitWeight P X ≤ scalarInverseLimitWeight P Y
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualCutNormality.lean:49` — `026f5042bd6adee2fcf90ce1db5b9831ee312b3bccaf4a194b8631936d543d65`

```lean
theorem dualAmbient_tendsto_strong {ι : Type*} {l : Filter ι}
    (A : ι → RegularHilbert H →L[ℂ] RegularHilbert H)
    (S : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hlim : ∀ v, Tendsto (fun i => A i v) l (𝓝 (S v))) (s : ℝ) (v : RegularHilbert H) :
    Tendsto (fun i => dualAmbient s (A i) v) l (𝓝 (dualAmbient s S v))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRightAverage.lean:70` — `64d49e1de18504e9e66e7559f48df9f6811c80821524b85324ee0a1305793aed`

```lean
theorem scalarWeight_right_average_le (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (h : ℝ) :
    dualQuadraticIntegral (star (A.val * regularAverage P h) * (A.val * regularAverage P h))
      (regularVacuum P) ≤ dualQuadraticIntegral (star A.val * A.val) (regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351CutoffAverageCommutation.lean:49` — `bc881ee5df7e027859ef14d7379b27bc9c2a27bea3b08cf42d6604805afa2a66`

```lean
theorem regularInverseCutoffSqrt_commutes_average (P : SiteProfile)
    (ε : ℝ) (hε : 0 < ε) (δ : ℝ) :
    Commute (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε))
      (regularAverage P δ)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350FiniteDualStarCore.lean:55` — `017fd7d4c1efd3c0ddfba91b3a6464fdbc194dce8e4ee0a6ad4580a0a6ac98ce`

```lean
theorem regularSandwich_star (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (h : ℝ) :
    star (regularSandwich P A h) = regularSandwich P (star A) h
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350FiniteDualStarCore.lean:63` — `017fd7d4c1efd3c0ddfba91b3a6464fdbc194dce8e4ee0a6ad4580a0a6ac98ce`

```lean
theorem regularSandwich_mem_finiteDualStarCore (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (h : ℝ) (hh : 0 < h) :
    regularSandwich P A h ∈ finiteDualStarCore P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350FiniteDualStarCore.lean:94` — `017fd7d4c1efd3c0ddfba91b3a6464fdbc194dce8e4ee0a6ad4580a0a6ac98ce`

```lean
theorem regularSandwich_tendsto (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra)
    (v : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun h : ℝ => (regularSandwich P A h).val v) (𝓝[>] 0) (𝓝 (A.val v))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351WeightAverageRecovery.lean:16` — `a72b71ac86bb0b2a5c81d5bfaba3c6ad964bf4a8beffd0a9df89f7ee26391fac`

```lean
theorem scalarWeight_square_eq_iSup_averages (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    dualQuadraticIntegral (star A.val*A.val) (regularVacuum P) =
      ⨆ n : ℕ, dualQuadraticIntegral
        (star (A.val*regularAverage P (1/((n : ℝ)+1))) *
          (A.val*regularAverage P (1/((n : ℝ)+1)))) (regularVacuum P)
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_tracial_extension\20260914_235009_395646\searches.json. Ausência nominal nos recortes não é ausência universal.
