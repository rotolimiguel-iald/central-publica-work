[REAPROVEITAMENTO — ANTES DO CÓDIGO FORMAL]

# A1: forma dual na base

2026-09-14T08:39:58.871426

Consumidor: `RegularCoreTraceData P`, via a ponte 1 de `LACUNAS_A1.md` e a perturbação do peso. O alvo local é transportar `AffiliatedPositiveForm (dualFixedCore P)` para `AffiliatedPositiveForm (theFactorObject P)`, usando `testVectorIsometry` e provando afiliação. A avaliação no mesmo Ω deve ser igual ao peso escalar em ENNReal, sem hipótese de finitude.

- **CONSUMIDOR** `structure RegularCoreTraceData`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351RegularCoreTraceContract.lean:43`; SHA256 `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0`. A1(b): o traço neste cone e nesta ação. A ponte de base integra a identificação do peso usado para a perturbação; não fornece ainda o traço.

```lean
structure RegularCoreTraceData (P : SiteProfile) where
```

- **REUSAR** `structure AffiliatedPositiveForm`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualClosedForm.lean:84`; SHA256 `69a47c01fc1a366a61b871b86e1d7114e43e865b025a04cd57918f09ed7c5be7`. Forma positiva fechada estendida com invariância sob o comutante unitário; mesma tipagem, agora na base.

```lean
structure AffiliatedPositiveForm (N : VonNeumannAlgebra H) extends ClosedPositiveForm H where
```

- **ADAPTAR** `def dualFixedWeight`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualFixedWeightLaws.lean:50`; SHA256 `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`. Fornecedor retorna AffiliatedPositiveForm(dualFixedCore P); exigimos saída em AffiliatedPositiveForm(theFactorObject P).

```lean
def dualFixedWeight (P : TGLExt.SiteProfile) (A : PositiveCoreInput P) :
    AffiliatedPositiveForm (dualFixedCore P) :=
```

- **REUSAR** `theorem dualFixedWeight_bimodule`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualFixedWeightLaws.lean:93`; SHA256 `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`. Transportar pela equivalência e pela isometria já construídas.

```lean
theorem dualFixedWeight_bimodule (P : TGLExt.SiteProfile)
    (A : PositiveCoreInput P) (B : (dualFixedCore P).toStarSubalgebra) :
    dualFixedWeight P (A.conjugate B) =
      (dualFixedWeight P A).conjugate B.val B.property := by
```

- **REUSAR** `theorem dualFixedWeight_preserves_internal_isLUB`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualFixedWeightLaws.lean:126`; SHA256 `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`. Normalidade do mesmo integral, aplicada aos vetores da base.

```lean
theorem dualFixedWeight_preserves_internal_isLUB (P : TGLExt.SiteProfile)
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    IsLUB (Set.range (fun i => dualFixedWeight P ⟨(A i).val, (A i).property, hpos i⟩))
      (dualFixedWeight P ⟨S.val, S.property, positive_internal_isLUB_nonneg P A S hpos hS⟩) := by
```

- **REUSAR** `def fixedBaseEquiv`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350FixedBaseEquivalence.lean:29`; SHA256 `6b4cda490d27efc86fdac21e57b91c30778477221d08ff9c90f31a1bf8b8f278`. Equivalência concreta entre M e F, não hipótese abstrata.

```lean
def fixedBaseEquiv (P : SiteProfile) :
    (theFactorObject P).toStarSubalgebra ≃⋆ₐ[ℂ] (dualFixedCore P).toStarSubalgebra :=
```

- **REUSAR** `theorem dualFixedCore_eq_amplified_base`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350FixedCoreBaseIdentification.lean:21`; SHA256 `0454ce14669be84c8384143a8ace33b7e795bc5b262355afc97284d1a963f4a1`. Identificação de cada operador fixo com fibre de um elemento da base.

```lean
theorem dualFixedCore_eq_amplified_base (P : SiteProfile)
    (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) :
    B ∈ dualFixedCore P ↔ ∃ C ∈ theFactorObject P, B = fibre C := by
```

- **REUSAR** `def testVectorIsometry`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350L2Order.lean:14`; SHA256 `763b6ebd38541bb028c6a007c492b5155fd5859d2bc9572a0016ab8bef93f46d`. H →ₗᵢ[ℂ] L²(R,H); fornece continuidade e linearidade para restrição da forma.

```lean
def testVectorIsometry : H →ₗᵢ[ℂ] RegularHilbert H where
```

- **REUSAR** `def fibreRepresentation`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350L2OperatorLift.lean:53`; SHA256 `bbdf07f64bc1abdfb50fed8420911c868a11cc6c8036b6f06167f021a1db7465`. Amplifica o unitário de M′ para provar afiliação da forma restrita.

```lean
def fibreRepresentation : (H →L[ℂ] H) →⋆ₐ[ℂ] (RegularHilbert H →L[ℂ] RegularHilbert H) where
```

- **ADAPTAR** `theorem scalarDualWeight_bounded_base_value`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:77`; SHA256 `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`. A hipótese exige output limitado; o novo caso cobrirá ENNReal inclusive infinito.

```lean
theorem scalarDualWeight_bounded_base_value (P : SiteProfile) (A : PositiveCoreInput P)
    (D : (theFactorObject P).toStarSubalgebra)
    (hrep : ∀ v, dualQuadraticIntegral A.val v =
      ENNReal.ofReal (inner ℂ v (fibre D.val v)).re) :
    scalarDualWeight P A = ENNReal.ofReal (inner ℂ (hOmega P) (D.val (hOmega P))).re := by
```

- **REUSAR** `theorem scalarDualWeight_square_finite_strong_density`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:66`; SHA256 `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`. Não substituir a semifinitude de peso por exigência mais forte de minorantes finitos de cada positivo.

```lean
theorem scalarDualWeight_square_finite_strong_density (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → dualQuadraticIntegral
      (star (A.val * regularAverage P h) * (A.val * regularAverage P h)) (regularVacuum P) < ⊤) ∧
    (∀ h : ℝ, A.val * regularAverage P h ∈ regularCoreAlgebra P) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage P h) v) (𝓝[>] 0) (𝓝 (A.val v))) := by
```

As seis modalidades de busca de A1 constam da ficha original e de seus adendos, cujos hashes são referidos no JSON. As duas buscas adicionais estão registradas integralmente. Não se afirma ausência universal de fornecedor.

Este marco não paga A1(b): a identificação abstrata do cone/predual e as pontes modulares/gerador/traço continuam explícitas. Não se cria nova camada Python nem se altera o gate.
