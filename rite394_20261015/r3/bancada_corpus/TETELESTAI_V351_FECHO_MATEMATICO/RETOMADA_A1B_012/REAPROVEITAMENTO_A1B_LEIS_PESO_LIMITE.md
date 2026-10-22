[OPEN — ficha anterior às leis do peso limite]

# A1(b): o peso limite pelos cortes já construídos

2026-09-14T22:30:29.369753-03:00

Define scalarInverseCutoffWeight P epsilon on the EXISTING PositiveCoreInput as nu(star sqrt(B_epsilon) X sqrt(B_epsilon)). Prove zero, addition, NNReal homogeneity, input monotonicity and normality for internal positive directed suprema, using the old strong operator limit and old normality of dualQuadraticIntegral. Read scalarWeight_inverseCutoff_antitone as regulator order, and prove the natural-number sequence epsilon_n=1/(n+1) gives monotone weights. Define scalarInverseLimitWeight as that SAME sequence supremum; prove zero/add/homogeneous/monotone/normal and domination of each sequence cutoff. All values ENNReal, no finiteness premise. No separate GNS, trace structure inhabitant, final semifinitude, faithfulness, traciality or dual scaling claimed by these laws. Explicit two definitions are consumers of already constructed cutoffs and of the final RegularCoreTraceData value field. Existing PositiveCoreInput.conjugate is NOT usable directly: requires dualFixedCore; use raw integral laws without asserting that cuts are theta-fixed.

ADAPTAR: leis integrais e supremos existentes; não criar outro espaço de estados. A normalidade do sanduíche segue por limite forte de redes positivas, não por presumir que uma conjugação não invertível preserva qualquer supremo. Fornecedores ENNReal serão registrados em adendo antes do alvo.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegulatorWeightOrder.lean:66` — `b908f79a4d20ca8f456eb245e2a605a6cc6e611667e1c8a8d6cb1cee2ee4f838`

```lean
theorem scalarWeight_inverseCutoff_antitone (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) (hεη : ε ≤ η)
    (X : PositiveCoreInput P) :
    dualQuadraticIntegral
      (star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P η)) * X.val *
        hilbertPositiveSqrt (regularInverseGeneratorCutoff P η)) (regularVacuum P) ≤
    dualQuadraticIntegral
      (star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) * X.val *
        hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) (regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualWeightForm.lean:66` — `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4`

```lean
theorem dualQuadraticIntegral_zero (v : RegularHilbert H) :
    dualQuadraticIntegral (0 : RegularHilbert H →L[ℂ] RegularHilbert H) v = 0
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualWeightForm.lean:74` — `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4`

```lean
theorem dualQuadraticIntegral_add
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hB : 0 ≤ B)
    (v : RegularHilbert H) :
    dualQuadraticIntegral (A+B) v = dualQuadraticIntegral A v + dualQuadraticIntegral B v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualQuadraticLaws.lean:61` — `7085d5ad460720e87ea5e1e3cc8bcbf5b55193be77b2ba283988fbf03120c1f3`

```lean
theorem dualQuadraticIntegral_smul_operator (r : ℝ) (hr : 0 ≤ r)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral (r • A) v = ENNReal.ofReal r * dualQuadraticIntegral A v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualFormFaithfulness.lean:79` — `6fca7648f9345bd4e83ed364bc0f551d587b99651b1c7c86574b1d0b090bea83`

```lean
theorem dualQuadraticIntegral_mono
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H) (hAB : A ≤ B)
    (v : RegularHilbert H) : dualQuadraticIntegral A v ≤ dualQuadraticIntegral B v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualFormNormality.lean:18` — `feace23e31954e69de8103646211acd6d59a1b859e3b9ec109c142b1c994fdaa`

```lean
theorem dualQuadraticIntegral_of_monotone_strong_limit
    (A : ι → RegularHilbert H →L[ℂ] RegularHilbert H)
    (S : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (hlim : ∀ v, Tendsto (fun i => A i v) atTop (𝓝 (S v)))
    (v : RegularHilbert H) :
    dualQuadraticIntegral S v = ⨆ i, dualQuadraticIntegral (A i) v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularNormality.lean:52` — `bcd49e92800bf99d7770bb9969879be02a9768f129ce842ae2f39cefaca3cc0a`

```lean
theorem vonNeumann_exists_positive_isLUB (N : VonNeumannAlgebra H)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (T : ι → N.toStarSubalgebra) (hpos : ∀ i, 0 ≤ T i) (hmono : Monotone T)
    (C : ℝ) (hC : 0 ≤ C) (hbound : ∀ i, ‖(T i : H →L[ℂ] H)‖ ≤ C) :
    ∃ B : N.toStarSubalgebra, 0 ≤ B ∧ ‖(B : H →L[ℂ] H)‖ ≤ C ∧
      (∀ v, Tendsto (fun i => (T i : H →L[ℂ] H) v) atTop
        (𝓝 ((B : H →L[ℂ] H) v))) ∧
      IsLUB (Set.range (fun i => (T i : H →L[ℂ] H))) (B : H →L[ℂ] H) ∧
      IsLUB (Set.range T) B
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualFixedWeightLaws.lean:38` — `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`

```lean
def PositiveCoreInput.conjugate {P : TGLExt.SiteProfile}
    (A : PositiveCoreInput P)
    (B : (dualFixedCore P).toStarSubalgebra) : PositiveCoreInput P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualFixedWeightLaws.lean:118` — `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`

```lean
theorem positive_internal_isLUB_nonneg (P : TGLExt.SiteProfile)
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hS : IsLUB (Set.range A) S) : 0 ≤ S
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_limit_weight\20260914_223003_335432\searches.json. Ausência nominal nos recortes não é ausência universal.
