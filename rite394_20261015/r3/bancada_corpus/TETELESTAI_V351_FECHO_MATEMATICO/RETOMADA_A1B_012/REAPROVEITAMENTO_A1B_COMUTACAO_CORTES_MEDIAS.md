[OPEN — ficha anterior à comutação dos cortes com as médias]

# A1(b): as médias comutam com as raízes dos cortes originais

2026-09-14T22:01:48.045934-03:00

For P,t prove Commute(regularSpectralResolvent P)(regularUnitary P t), using SAME spectral coordinates and commuting characters. For epsilon>0 use existing cutoff CFC identity and existing hilbertPositiveSqrt=CFC.sqrt to deduce Commute(sqrt(B_epsilon))(regularUnitary P t). Integrate the actual regularUnitary using regularAverage_apply to prove Commute(sqrt(B_epsilon))(regularAverage P delta) for EVERY real delta. No new spectral transform, resolvent, average, square root or weight. Consumer: use the already established average recovery on a sqrt(B_epsilon) to extend perturbed-weight order to all positive inputs. This does not infer commutation of arbitrary b in the right algebra with the averages. Mathematical helper is generic CFC commutation instantiated on Hilbert operators.

ADAPTAR: coordenação espectral, comutação de caracteres, CFC e integral das translações existentes. Não reconstruir as coordenadas nem o resolvente. A consulta TODOS_POSITIVOS nomeia esta ponte como necessária. Mathlib Commute.cfc/IsSelfAdjoint.commute_cfc e Commute.cfcₙ_nnreal foram lidos no fornecedor ContinuousFunctionalCalculus/Commute.lean.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularGeneratorAffiliation.lean:13` — `9e172df5174e9b2b9c5315825a4a487f0fb04b34ba68dcecffd11e8d2684690e`

```lean
theorem character_commutation_realScalarMultiplier
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hB : ∀ s : ℝ, characterMultiplier s * B = B * characterMultiplier s)
    (g : ℝ → ℝ) (hg : Continuous g) (h0 : ∀ x, 0 ≤ g x) (h1 : ∀ x, g x ≤ 1) :
    realScalarMultiplier g hg h0 h1 * B = B * realScalarMultiplier g hg h0 h1
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularImaginaryPowers.lean:65` — `066b9cb14426365807ead587ca90ad28e3703a0f9efc0ce359519da7c5243b9a`

```lean
theorem regularSpectralCoordinates_character (P : SiteProfile) (t : ℝ)
    (u : RegularHilbert (TowerHilbert P)) :
    regularSpectralCoordinates P (characterMultiplier (2*Real.pi*t) u) =
      regularUnitary P t (regularSpectralCoordinates P u)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2CharacterMultiplier.lean:114` — `2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3`

```lean
theorem characterMultiplier_mul (s t : ℝ) :
    characterMultiplier (H := H) s * characterMultiplier t = characterMultiplier (s+t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:62` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_cfc (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    regularInverseGeneratorCutoff P ε =
      cfc (inverseCutoffFunction ε) (regularSpectralResolvent P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:15` — `83be0cf3f811bd6fd429c7705fdb1a00b27fdd6496ee971b9ca5f355c00d6f36`

```lean
def hilbertPositiveSqrt (T : H →L[ℂ] H) : H →L[ℂ] H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularApproximation.lean:41` — `d8e7830989e0ba3d71f0e8495f54414cedc12a9eac16b1bc0501f15342b8bb44`

```lean
theorem regularAverage_apply (P : TGLExt.SiteProfile) (h : ℝ)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    regularAverage P h v = h⁻¹ • ∫ t in 0..h, regularUnitary P t v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:84` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
theorem regularSpectralResolvent_nonneg (P : SiteProfile) :
    0 ≤ regularSpectralResolvent P
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_cutoff_average_commutation\20260914_220124_359580\searches.json. Ausência nominal nos recortes não é ausência universal.
