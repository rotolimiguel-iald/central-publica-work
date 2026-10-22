[OPEN — ficha anterior à extensão de ordem]

# A1(b): ordem em todos os positivos do mesmo core

2026-09-14T22:14:00.904198-03:00

Extend scalarWeight_right_perturbed_mono from A in n_nu to EVERY A in N, using exact average recovery for A*b and A*c, finite averages A*e_n, and explicit hypotheses that b and c commute with the SAME regularAverage P delta. Then for EVERY positive X in the SAME N instantiate A as the EXISTING hilbertPositiveSqrt(X), proving its membership in N by norm closure and existing real CFC membership, and A*A=X by existing sqrt identity. Keep b b* <= c c*, membership in scalarPolarRightAlgebra and average commutation explicit. No new definition of weight, root, GNS, core or regularizer. The actual cutoff roots discharge those hypotheses via existing suppliers; regulator-order B_epsilon <= B_eta itself is a separate consumer/obligation. Infinite values allowed. This does not prove traciality, final semifinitude, or completion of A1(b).

ADAPTAR: compor os três fornecedores já provados; não criar outro ideal ou peso. A aproximação é dos VALORES e não de minorantes positivos. Reusar CFC.sqrt_eq_real_sqrt, cfcₙ_mem e CFC.sqrt_mul_sqrt_self para o mesmo wrapper de raiz. O adendo dos fornecedores mathlib será anexado antes do alvo.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351PerturbedWeightOrder.lean:29` — `9af750ad0099449655e5350b76219d51986849e434584359bd09de475fe936d6`

```lean
theorem scalarWeight_right_perturbed_mono (P : SiteProfile)
    (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (hc : c ∈ scalarPolarRightAlgebra P)
    (hbc : b * star b ≤ c * star c) (A : scalarWeightLeftIdeal P) :
    dualQuadraticIntegral (star b.val * (star A.val.val*A.val.val) * b.val)
      (regularVacuum P) ≤
    dualQuadraticIntegral (star c.val * (star A.val.val*A.val.val) * c.val)
      (regularVacuum P)
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

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarDualWeight.lean:66` — `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

```lean
theorem scalarDualWeight_square_finite_strong_density (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → dualQuadraticIntegral
      (star (A.val * regularAverage P h) * (A.val * regularAverage P h)) (regularVacuum P) < ⊤) ∧
    (∀ h : ℝ, A.val * regularAverage P h ∈ regularCoreAlgebra P) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage P h) v) (𝓝[>] 0) (𝓝 (A.val v)))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351CutoffAverageCommutation.lean:49` — `bc881ee5df7e027859ef14d7379b27bc9c2a27bea3b08cf42d6604805afa2a66`

```lean
theorem regularInverseCutoffSqrt_commutes_average (P : SiteProfile)
    (ε : ℝ) (hε : 0 < ε) (δ : ℝ) :
    Commute (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε))
      (regularAverage P δ)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:125` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_sqrt_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),h⟩ :
        (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:15` — `83be0cf3f811bd6fd429c7705fdb1a00b27fdd6496ee971b9ca5f355c00d6f36`

```lean
def hilbertPositiveSqrt (T : H →L[ℂ] H) : H →L[ℂ] H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:173` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
theorem scalarRightAction_cfc (P : SiteProfile)
    (b : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (f : ℂ → ℂ) :
    ∃ hf : cfc f b.val ∈ regularCoreAlgebra P,
      (⟨cfc f b.val,hf⟩ : (regularCoreAlgebra P).toStarSubalgebra) ∈
        scalarPolarRightAlgebra P
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_all_positive_weight_order\20260914_221338_858806\searches.json. Ausência nominal nos recortes não é ausência universal.
