[OPEN — ficha anterior à identidade de norma do peso perturbado]

# A1(b): consumir a ação dos cortes nos valores do peso

2026-09-14T21:30:50.225336-03:00

For P, b in the same scalarPolarRightAlgebra and A in n_nu, prove dualQuadraticIntegral(star b.val*(star A.val.val*A.val.val)*b.val)(regularVacuum P) = ENNReal.ofReal(norm(scalarGNSRepresentation P (star b) ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A)))^2). Obtain A*b membership from the already proved right identity, rewrite the GNS norm-square and use the isometry of the SAME J. Consumer: bounded cut perturbations with b=hilbertPositiveSqrt(B_epsilon), already constructed. This only gives values on squares of n_nu; do not claim it extends to all positive inputs, proves monotonicity in epsilon, or gives a trace. PositiveCoreInput.conjugate is only a pattern because it requires b in dualFixedCore, whereas our cut lies in regularCoreAlgebra; do not pass it by homonym or claim theta-fixity.

ADAPTAR: a identidade da ação direita já fornece Ab no domínio e seu vetor GNS. Basta a ponte algébrica para a norma do peso; não criar outra realização, peso escalar ou inscrição. A normalidade/aditividade de ν são fornecedores, não novos alvos. Não usar a caracterização falsa por minorantes positivos finitos para ν. A passagem a todos positivos e a tracialidade são obrigações posteriores nomeadas, não consequências deste lema isolado.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:14` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
def ScalarPolarRight (P : SiteProfile) (b : (regularCoreAlgebra P).toStarSubalgebra) : Prop
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:94` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
def scalarPolarRightAlgebra (P : SiteProfile) :
    StarSubalgebra ℂ (regularCoreAlgebra P).toStarSubalgebra
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightAction.lean:44` — `7875ce91559689c1e951f28d3a1d005dc17aae2af1db677242a27d38e40dfb5c`

```lean
theorem scalarWeightGNSEmbedding_norm_sq (P : SiteProfile) (A : scalarWeightLeftIdeal P) :
    ENNReal.ofReal (‖scalarWeightGNSEmbedding P A‖^2) =
      dualQuadraticIntegral (star A.val.val*A.val.val) (regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:25` — `83be0cf3f811bd6fd429c7705fdb1a00b27fdd6496ee971b9ca5f355c00d6f36`

```lean
theorem antiunitaryConjugate_apply (T : H →L[ℂ] H) (x : H) :
    antiunitaryConjugate U T x=U (T (U.symm x))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:125` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_sqrt_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),h⟩ :
        (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarDualWeight.lean:15` — `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

```lean
def scalarDualWeight (P : SiteProfile) (A : PositiveCoreInput P) : ℝ≥0∞
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarDualWeight.lean:46` — `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

```lean
theorem scalarDualWeight_normal (P : SiteProfile)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    scalarDualWeight P ⟨S.val,S.property,positive_internal_isLUB_nonneg P A S hpos hS⟩ =
      ⨆ i, scalarDualWeight P ⟨(A i).val,(A i).property,hpos i⟩
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualFixedWeightLaws.lean:38` — `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`

```lean
def PositiveCoreInput.conjugate {P : TGLExt.SiteProfile}
    (A : PositiveCoreInput P)
    (B : (dualFixedCore P).toStarSubalgebra) : PositiveCoreInput P
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_perturbed_weight_norm\20260914_213020_145263\searches.json. Ausência nominal nos recortes não é ausência universal.
