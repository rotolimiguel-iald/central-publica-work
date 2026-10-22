[REAL — ficha de reaproveitamento por leitura; nenhuma nova prova declarada]

# A1 — traço no core regular da mesma torre

Para todo P:SiteProfile, τ:PositiveCoreInput P→ENNReal com zero, adição, homogeneidade NNReal, monotonia, fidelidade, normalidade IsLUB, semifinitude por supremo de minorantes positivos finitos, τ(a*a)=τ(aa*) e τ(regularDualAction P s A)=ofReal(exp(-s))*τ(A). Canonicalidade exige adicionalmente τ=(ν)_(h^-1), h^(it)=regularUnitary P t, não apenas escolher uma normalização arbitrária.

NOVO: contrato forte e suas recusas; REUSAR: cone, álgebra, ação, normalidade/ideal/peso existentes. ADAPTAR: ponte modular/perturbação do peso para τ. Não construir nova teoria genérica sem necessidade.

## Fornecedores e tipos

### structure ContinuousCoreData — ADAPTAR

[ModularRealization.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGL\ModularRealization.lean:68>) · SHA256 `17e344c8b7b40ae8f2ed4910c3b5e4712cc8ba84dd53e05d10a94f0009295348`

O contrato legado recebe Core→ENNReal sem cone positivo, fidelidade, normalidade ou semifinitude. O novo tipo restringirá o peso a PositiveCoreInput P; não se afirmará conversão automática ao legado.

```lean
structure ContinuousCoreData (W : TGLSpecificAQFTWitness) (D : WedgeModularData W) where
```

### structure ThreeLocksCoreData — CONSUMIDOR

[ModularRealization.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGL\ModularRealization.lean:100>) · SHA256 `17e344c8b7b40ae8f2ed4910c3b5e4712cc8ba84dd53e05d10a94f0009295348`

Consumidor posterior A2: PF_trace_pos e PF_trace_finite precisam do mesmo traço.

```lean
structure ThreeLocksCoreData (W : TGLSpecificAQFTWitness) (D : WedgeModularData W)
    (C : ContinuousCoreData W D) where
```

### def zeroTraceLegacyCore — REUSAR

[V350CoreContractCounterexample.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350CoreContractCounterexample.lean:12>) · SHA256 `1aaa11d4c572c2ad3c0c80a54322247233b64e6e16e28710cd4ccc0d3524de0e`

Sonda negativa: refutar a restrição zero no novo contrato. A prova antiga só refuta ThreeLocks, não fortalece o core.

```lean
def zeroTraceLegacyCore (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness)
    (D : WedgeModularData W) : ContinuousCoreData W D where
```

### def regularCoreAlgebra — REUSAR

[V350RegularGeneratedAlgebra.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularGeneratedAlgebra.lean:50>) · SHA256 `252b0fa3d5e37c42827efccfc26a555db80ac5c20a6f94269060ce2b3dcb5f71`

Mesma álgebra concreta; não reconstruir produto gerado.

```lean
def regularCoreAlgebra (P : SiteProfile) : VonNeumannAlgebra (RegularHilbert (TowerHilbert P)) :=
```

### def regularDualAction — REUSAR

[V350RegularDualAction.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularDualAction.lean:76>) · SHA256 `e7c3628d969c0dae2a971c156200acb88f6bf4286a9c648a2ad3da08c468040c`

Mesma ação dual concreta; a operação no cone usa regularDualAction_apply e dualAmbient_nonneg.

```lean
def regularDualAction (P : SiteProfile) (s : ℝ) :
    (regularCoreAlgebra P).toStarSubalgebra ≃⋆ₐ[ℂ] (regularCoreAlgebra P).toStarSubalgebra :=
```

### theorem regularCoreEmbedding_preserves_positive_directed_isLUB — REUSAR

[V350RegularNormality.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularNormality.lean:127>) · SHA256 `bcd49e92800bf99d7770bb9969879be02a9768f129ce842ae2f39cefaca3cc0a`

Normalidade da inclusão já paga; não é a normalidade do traço.

```lean
theorem regularCoreEmbedding_preserves_positive_directed_isLUB (P : SiteProfile)
    (S : Set (theFactorObject P).toStarSubalgebra)
    (B : (theFactorObject P).toStarSubalgebra)
    (hne : S.Nonempty) (hdir : DirectedOn (· ≤ ·) S)
    (hpos : ∀ A ∈ S, 0 ≤ A) (hB : IsLUB S B) :
    IsLUB (regularCoreEmbedding P '' S) (regularCoreEmbedding P B) := by
```

### abbrev PositiveCoreInput — REUSAR

[V350DualFixedWeightLaws.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualFixedWeightLaws.lean:15>) · SHA256 `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`

Cone positivo exato, adição e escala já definidos neste arquivo.

```lean
abbrev PositiveCoreInput (P : TGLExt.SiteProfile) :=
```

### def scalarDualWeight — REUSAR

[V350ScalarDualWeight.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:15>) · SHA256 `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

Peso ν concreto de partida. Não casa com traço: invariância dual não é escala e^-s.

```lean
def scalarDualWeight (P : SiteProfile) (A : PositiveCoreInput P) : ℝ≥0∞ :=
```

### theorem scalarDualWeight_normal — REUSAR

[V350ScalarDualWeight.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:46>) · SHA256 `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

Normalidade por IsLUB interno já provada para ν; preservação na perturbação ainda exigida.

```lean
theorem scalarDualWeight_normal (P : SiteProfile)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    scalarDualWeight P ⟨S.val,S.property,positive_internal_isLUB_nonneg P A S hpos hS⟩ =
      ⨆ i, scalarDualWeight P ⟨(A i).val,(A i).property,hpos i⟩ :=
```

### theorem scalarDualWeight_faithful — REUSAR

[V350ScalarDualWeight.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:36>) · SHA256 `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

Fidelidade já provada para ν.

```lean
theorem scalarDualWeight_faithful (P : SiteProfile) (A : PositiveCoreInput P) :
    scalarDualWeight P A = 0 ↔ A = PositiveCoreInput.zero P := by
```

### theorem scalarDualWeight_square_finite_strong_density — REUSAR

[V350ScalarDualWeight.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:66>) · SHA256 `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

Ideal finito fortemente denso de ν. Não identificar isso por rfl com semifinitude por minorantes positivos de τ.

```lean
theorem scalarDualWeight_square_finite_strong_density (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → dualQuadraticIntegral
      (star (A.val * regularAverage P h) * (A.val * regularAverage P h)) (regularVacuum P) < ⊤) ∧
    (∀ h : ℝ, A.val * regularAverage P h ∈ regularCoreAlgebra P) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage P h) v) (𝓝[>] 0) (𝓝 (A.val v))) := by
```

### theorem regularScalarWeightCertificate — REUSAR

[V350RegularScalarWeightCertificate.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularScalarWeightCertificate.lean:58>) · SHA256 `f7c1786097ce619e7cbe7f35269147b8bde95793de9b0b5a09bf98627a2db6c0`

Agrega leis já provadas. Explicitamente não fornece KMS nem traço.

```lean
theorem regularScalarWeightCertificate (P : SiteProfile) :
    RegularScalarWeightCertificate.{u} P where
```

### theorem dualQuadraticIntegral_dual_invariant — REUSAR

[V350DualWeightForm.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualWeightForm.lean:87>) · SHA256 `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4`

Ponte para demonstrar que renomear ν como τ falha na escala dual.

```lean
theorem dualQuadraticIntegral_dual_invariant (r : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral (dualAmbient r A) v = dualQuadraticIntegral A v := by
```

### theorem regularAverage_dualQuadraticIntegral — REUSAR

[V350RegularFiniteWeight.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularFiniteWeight.lean:108>) · SHA256 `39e417e41adf90a2d575b6a93f8a35ccd2d816a445097745fd3c540ab240baf6`

Valor finito explícito sobre quadrado de média: testemunha contra troca de ν por τ.

```lean
theorem regularAverage_dualQuadraticIntegral (P : TGLExt.SiteProfile) (h : ℝ) (hh : 0 < h)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    dualQuadraticIntegral (star (regularAverage P h) * regularAverage P h) v =
      ENNReal.ofReal (h⁻¹ * ‖v‖ ^ 2) := by
```

### theorem matrix_trace_is_faithful_weight — NAO_CASA

[SemifiniteSeed.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\SemifiniteSeed.lean:115>) · SHA256 `9e91547595c6fdfa37c5d9b786bf3b1e5b774fa90fa4ff0a01a463a775e77dc5`

Matrizes reais finitas; não fornece N(P)+→ENNReal nem escala dual.

```lean
theorem matrix_trace_is_faithful_weight :
    (∀ A : Matrix n n ℝ, A.PosSemidef → 0 ≤ A.trace) ∧
      (∀ A : Matrix n n ℝ, A.PosSemidef → (A.trace = 0 ↔ A = 0)) ∧
      (∀ A B : Matrix n n ℝ, (B - A).PosSemidef → A.trace ≤ B.trace) :=
```

### def dimTraceData — NAO_CASA

[DimensionTrace.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\DimensionTrace.lean:51>) · SHA256 `cdadc9fdf8ed641c7c260e0a5450577b4e190b102a055dc0d2c49e71f49338ea`

Reticulado de subespaços reais finitos; tipo distinto do cone positivo de N(P).

```lean
def dimTraceData (n : Type) [Fintype n] :
    SemifiniteTraceData (Submodule ℝ (n → ℝ)) where
```

### theorem opWeight_star_mul_self_comm — NAO_CASA

[BreuerTrace.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\BreuerTrace.lean:104>) · SHA256 `4a667f41d3b7bb1d6a3a02fa46f43372c2a3e4bef30c98acde05294f5c46b496`

Traço padrão de B(ellTwo), não o traço semifinito de N(P) com ação dual prescrita.

```lean
theorem opWeight_star_mul_self_comm (a : ellTwo →L[ℂ] ellTwo) :
    opWeight (ContinuousLinearMap.adjoint a * a)
      = opWeight (a * ContinuousLinearMap.adjoint a) := by
```

### structure SemifiniteTraceData — NAO_CASA

[LocalBreuerGap.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\LocalBreuerGap.lean:72>) · SHA256 `8ec73c7d9e703d6c775f53351a784ab98b27ad2dd3d253b79a3d34992e0d5d3d`

Peso fiel/monótono em reticulado: nome não fornece normalidade e semifinitude no core.

```lean
structure SemifiniteTraceData (L : Type) [Lattice L] [BoundedOrder L] where
```

## Consumidor e alcance

A1 fornece o traço para A2, que fornece o core/ThreeLocks compatíveis a A5. A bandeira qgf_continuous_modular_realization_constructed não vira True por esta ficha. Localizadores exatos de todas as ocorrências estão no JSON. O gate principal pago permanece intacto.

## Busca e limites

922 arquivos embutidos (918 Lean), buscas registradas em BUSCAS_A1.json; 625 caminhos correspondentes em outras bancadas, 7 hashes distintos.

- A busca inicial do acervo foi truncada em 50 ocorrências históricas; exige refinamento Pedersen-Takesaki, não prova ausência.

- Bancada TOE: único arquivo por padrão foi FrontierCertificate.lean, contrato não construtor de traço.

- Mathlib Analysis: busca dos nomes dá subespaços padrão e homônimos; não identifica implementação do teorema de perturbação.

- DEV não reativado: nenhum módulo suspenso fornece τ no cone positivo com escala dual.


Contrato compilado não é habitante. Falha de provedor não é impossibilidade matemática. Registrar precisamente o lema faltante e manter b NÃO PAGO se não houver construção nem parede contra sua existência.


Convenção: Λ_t=h^(it), L=log h desloca L−s; K=−log h desloca K+s. O traço é a perturbação ν_(h^-1); não trocar sinais nem inferir normalização da lei de escala.
