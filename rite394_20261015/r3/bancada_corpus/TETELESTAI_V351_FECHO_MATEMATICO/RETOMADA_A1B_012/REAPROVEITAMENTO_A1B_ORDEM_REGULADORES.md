[OPEN — ficha anterior à ordem dos reguladores]

# A1(b): os cortes originais crescem quando o regulador diminui

2026-09-14T22:22:49.061721-03:00

For epsilon,eta>0 derive the resolvent identity B_epsilon-B_eta=(eta-epsilon) smul (B_eta*B_epsilon) directly from the SAME graph and inverse equation. CFC of the same R proves the cuts commute, so their positive product is nonnegative. If epsilon<=eta, obtain B_eta<=B_epsilon. Then discharge membership, square-root norm products and original-average commutation to instantiate the already constructed all-positive weight comparison for sqrt(B_eta) and sqrt(B_epsilon), for EVERY X in PositiveCoreInput P. No finite-weight premise, new resolvent, spectral coordinates, trace definition or physics coupling. The regulator epsilon is mathematical, not beta_TGL. Consumer: define monotone cutoff weights and their supremum on the same cone. Trace and semifinitude of its limit remain obligations.

ADAPTAR: consumir graph_iff e positividade já provadas. Mathlib cfc_commute_cfc e Commute.mul_nonneg foram lidos nas fontes pinadas; adendo anterior ao alvo. Não redefinir o inverso ou instalar hipótese de ordem como resultado.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:50` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_graph (P : SiteProfile) (ε : ℝ) (hε : 0 < ε)
    (x : RegularHilbert (TowerHilbert P)) :
    (regularInverseGeneratorCutoff P ε x,
      x-(ε : ℂ) • regularInverseGeneratorCutoff P ε x) ∈
        (regularPositiveGenerator P).graph
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:99` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_graph_iff (P : SiteProfile) (ε : ℝ) (hε : 0 < ε)
    (x y : RegularHilbert (TowerHilbert P)) :
    (x,y) ∈ (regularPositiveGenerator P).graph ↔
      regularInverseGeneratorCutoff P ε (y+(ε : ℂ) • x) = x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:24` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_nonneg (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    0 ≤ regularInverseGeneratorCutoff P ε
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:62` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_cfc (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    regularInverseGeneratorCutoff P ε =
      cfc (inverseCutoffFunction ε) (regularSpectralResolvent P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351AllPositiveWeightOrder.lean:73` — `e91306108a0a296b320907a2899f5776747869dffae14f65fe3fe45197bf07bb`

```lean
theorem scalarWeight_right_perturbed_mono_all_positive (P : SiteProfile)
    (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (hc : c ∈ scalarPolarRightAlgebra P)
    (hbc : b * star b ≤ c * star c)
    (hbe : ∀ δ : ℝ, Commute b.val (regularAverage P δ))
    (hce : ∀ δ : ℝ, Commute c.val (regularAverage P δ))
    (X : PositiveCoreInput P) :
    dualQuadraticIntegral (star b.val * X.val * b.val) (regularVacuum P) ≤
      dualQuadraticIntegral (star c.val * X.val * c.val) (regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:125` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_sqrt_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),h⟩ :
        (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351CutoffAverageCommutation.lean:49` — `bc881ee5df7e027859ef14d7379b27bc9c2a27bea3b08cf42d6604805afa2a66`

```lean
theorem regularInverseCutoffSqrt_commutes_average (P : SiteProfile)
    (ε : ℝ) (hε : 0 < ε) (δ : ℝ) :
    Commute (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε))
      (regularAverage P δ)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:15` — `83be0cf3f811bd6fd429c7705fdb1a00b27fdd6496ee971b9ca5f355c00d6f36`

```lean
def hilbertPositiveSqrt (T : H →L[ℂ] H) : H →L[ℂ] H
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_regulator_order\20260914_222228_030596\searches.json. Ausência nominal nos recortes não é ausência universal.
