[OPEN — ficha anterior à recuperação de valores estendidos por médias]

# A1(b): recuperar todos os valores sem supor minorantes finitos

2026-09-14T21:55:44.270084-03:00

For EVERY A in regularCoreAlgebra P, prove nu(A*A)=iSup_n nu((A e_n)*(A e_n)), e_n=regularAverage P (1/(n+1)). No finite-weight hypothesis on A; values may be infinity. Consume pointwise orbit convergence and the existing upper bound under right averages, via Fatou for a SEQUENCE atTop. No monotonicity of e_n or of its squares asserted. A e_n is already uniformly square-finite by existing ideal lemmas. Consumer: extend the cut-weight order from square-finite inputs to all positive inputs, after proving commutation of cuts with the SAME averages. This does not claim finite positive minorants or normal-weight semifiniteness in that stronger sense.

ADAPTAR: limite pontual e cota já pagos, compostos com Fatou. Reutilizar a família regularAverage, sem novo regularizador ou novo peso. Consulta independente TODOS_POSITIVOS é roteiro, não prova.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRightAverage.lean:70` — `64d49e1de18504e9e66e7559f48df9f6811c80821524b85324ee0a1305793aed`

```lean
theorem scalarWeight_right_average_le (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (h : ℝ) :
    dualQuadraticIntegral (star (A.val * regularAverage P h) * (A.val * regularAverage P h))
      (regularVacuum P) ≤ dualQuadraticIntegral (star A.val * A.val) (regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRightAverage.lean:63` — `64d49e1de18504e9e66e7559f48df9f6811c80821524b85324ee0a1305793aed`

```lean
theorem scalarOrbit_right_average_tendsto (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (s : ℝ) :
    Tendsto (fun h : ℝ => dualAmbient s (A.val * regularAverage P h) (regularVacuum P))
      (𝓝[≠] 0) (𝓝 (dualAmbient s A.val (regularVacuum P)))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualSemifiniteIdeal.lean:108` — `63c88763eaa1c837ed0a28057d044a7627e57f993f4fcc4c7bddf44dcea07cbe`

```lean
theorem regularAverage_hasFiniteDualSquare (P : TGLExt.SiteProfile)
    (h : ℝ) (hh : 0 < h) : HasFiniteDualSquare (regularAverage P h)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualSemifiniteIdeal.lean:51` — `63c88763eaa1c837ed0a28057d044a7627e57f993f4fcc4c7bddf44dcea07cbe`

```lean
theorem HasFiniteDualSquare.left_mul
    (B A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : HasFiniteDualSquare A) :
    HasFiniteDualSquare (B*A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualWeightForm.lean:62` — `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4`

```lean
def dualQuadraticIntegral (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (v : RegularHilbert H) : ℝ≥0∞
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualWeightForm.lean:47` — `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4`

```lean
theorem dualQuadraticIntegrand_measurable
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    Measurable (dualQuadraticIntegrand A v)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularFiniteWeight.lean:95` — `39e417e41adf90a2d575b6a93f8a35ccd2d816a445097745fd3c540ab240baf6`

```lean
theorem dualQuadraticIntegrand_star_mul
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) (s : ℝ) :
    dualQuadraticIntegrand (star A * A) v s =
      ENNReal.ofReal (‖dualAmbient s A v‖ ^ 2)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\MeasureTheory\Integral\Lebesgue\Add.lean:231` — `e330b98eb9686290a3257802c38ad756150b110deb39fe32c66da46cf1211e4f`

```lean
theorem lintegral_liminf_le {ι : Type*} {f : ι → α → ℝ≥0∞} {u : Filter ι}
    [IsCountablyGenerated u] (h_meas : ∀ i, Measurable (f i)) :
    ∫⁻ a, liminf (fun i => f i a) u ∂μ ≤ liminf (fun i => ∫⁻ a, f i a ∂μ) u
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecificLimits\Basic.lean:69` — `dbbeb301e5b9dacc96ecd233fd05a02846a1fc88c9606f1b1d413d08aff5142e`

```lean
theorem tendsto_one_div_add_atTop_nhds_zero_nat {𝕜 : Type*} [DivisionSemiring 𝕜] [CharZero 𝕜]
    [TopologicalSpace 𝕜] [ContinuousSMul ℚ≥0 𝕜] :
    Tendsto (fun n : ℕ ↦ 1 / ((n : 𝕜) + 1)) atTop (𝓝 0)
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_weight_average_recovery\20260914_215512_951496\searches.json. Ausência nominal nos recortes não é ausência universal.
