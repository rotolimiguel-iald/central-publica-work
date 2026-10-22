[OPEN — ficha anterior ao transporte da ordem para os valores perturbados]

# A1(b): ordem dos valores no mesmo domínio do peso

2026-09-14T21:44:52.493896-03:00

For P, b,c in scalarPolarRightAlgebra P with b*star b <= c*star c in the same core, and A in scalarWeightLeftIdeal P, prove nu(star b*(star A*A)*b) <= nu(star c*(star A*A)*c). Consume the previously proved perturbed norm identity, positivity/order preservation of the original star representation and the adjoint quadratic-form identity. Consumer: order of inverse-generator cut perturbations. This is an order theorem on the existing square-finite domain only; no all-positive extension, no new weight, no trace. The comparison is b b* rather than b* b; selfadjoint square roots later discharge that distinction.

ADAPTAR: norma GNS, positividade de homomorfismos estrela e produto interno de A†A já existem. Uma ponte compõe esses fornecedores. Nenhuma nova representação ou peso.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351PerturbedWeightNorm.lean:12` — `9b4edeb94844ded88ec595b50160936d42e34637f4432493d02894dd7731bab9`

```lean
theorem scalarWeight_right_perturbed_norm (P : SiteProfile)
    (b : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (A : scalarWeightLeftIdeal P) :
    dualQuadraticIntegral (star b.val * (star A.val.val * A.val.val) * b.val)
      (regularVacuum P) =
    ENNReal.ofReal (‖scalarGNSRepresentation P (star b)
      ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A))‖^2)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:94` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
def scalarPolarRightAlgebra (P : SiteProfile) :
    StarSubalgebra ℂ (regularCoreAlgebra P).toStarSubalgebra
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\InnerProductSpace\Adjoint.lean:143` — `d1636c8ae9160d3762630f6f99815134dbc4da51188d9e2e34dcc3c06c6c32fc`

```lean
theorem apply_norm_sq_eq_inner_adjoint_left (A : E →L[𝕜] F) (x : E) :
    ‖A x‖ ^ 2 = re ⟪(A† ∘L A) x, x⟫
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Algebra\Order\Star\Basic.lean:433` — `a69d1f87e8b63fd9e2816e7060218a76269b2fe4cbf1c4962a7af0359781fe84`

```lean
lemma NonUnitalStarRingHom.map_le_map_of_map_star (f : R →⋆ₙ+* S) {x y : R} (hxy : x ≤ y) :
    f x ≤ f y
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:125` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_sqrt_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),h⟩ :
        (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRightAverage.lean:70` — `64d49e1de18504e9e66e7559f48df9f6811c80821524b85324ee0a1305793aed`

```lean
theorem scalarWeight_right_average_le (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (h : ℝ) :
    dualQuadraticIntegral (star (A.val * regularAverage P h) * (A.val * regularAverage P h))
      (regularVacuum P) ≤ dualQuadraticIntegral (star A.val * A.val) (regularVacuum P)
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_perturbed_weight_order\20260914_214440_512718\searches.json. Ausência nominal nos recortes não é ausência universal.
