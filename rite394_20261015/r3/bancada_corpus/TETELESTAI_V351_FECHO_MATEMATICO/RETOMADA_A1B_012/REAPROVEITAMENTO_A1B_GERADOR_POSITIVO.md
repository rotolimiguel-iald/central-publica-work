[OPEN — ficha anterior à construção do grafo positivo regular]

# A1(b): o candidato concreto ao gerador positivo

2026-09-14T18:42:39.905040-03:00

Consumidor: LACUNAS_A1.md:31, regular_unitary_positive_generator.

For each SiteProfile P: V=W F^{-1}; R=V M[sigmoid(2*pi*xi)] V^{-1}. Construct R on the actual regular Hilbert space, prove 0<=R<=1 and injectivity of both R and 1-R. Define h=resolventGraphOperator R hi, prove its graph closed, domain dense, self-adjointness, positivity and zero kernel. Affiliation, imaginary powers, dual scaling and trace remain subsequent consumers, not hypotheses assumed true here.

Real.sigmoid já existe: nenhum novo logistic/sigmoid. O resolventGraphOperator já constrói domínio e grafo; não reconstruí-los. O campo/multiplicador L² já existe; acrescentar apenas positividade/complemento que seus consumidores precisam. A transformação unitária é a Fourier existente com W já construído. Não se declara h afiliado nem identificado pelas potências antes das provas respectivas. O critério do módulo é produzir o objeto positivo, fechado, autoadjunto e não singular, com tipo e domínio; não fechar A1(b).

## Fornecedores

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2PositiveMultiplier.lean:25` — `6e3946aff9964e1a6a59a8dcb99a11b4a3c0026a6b0220f7df4b9901f83f3bdf`

```lean
def realScalarMultiplier (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) :
    RegularHilbert H →L[ℂ] RegularHilbert H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2PositiveMultiplier.lean:45` — `6e3946aff9964e1a6a59a8dcb99a11b4a3c0026a6b0220f7df4b9901f83f3bdf`

```lean
theorem realScalarMultiplier_injective (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) (hpos : ∀ s, 0 < g s) :
    Function.Injective (realScalarMultiplier (H := H) g hg h0 h1)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2PositiveMultiplier.lean:30` — `6e3946aff9964e1a6a59a8dcb99a11b4a3c0026a6b0220f7df4b9901f83f3bdf`

```lean
theorem realScalarMultiplier_ae (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) (f : RegularHilbert H) :
    realScalarMultiplier g hg h0 h1 f =ᵐ[volume] fun s => (g s : ℂ) • f s
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:57` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_star (F G : StrongIntegral.Family (H := H))
    (h : ∀ x, G.op x = star (F.op x)) :
    operatorFieldLift G = star (operatorFieldLift F)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:33` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_mul (F G K : StrongIntegral.Family (H := H))
    (h : ∀ x, K.op x = F.op x * G.op x) :
    operatorFieldLift K = operatorFieldLift F * operatorFieldLift G
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventGraph.lean:13` — `3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b`

```lean
def resolventGraphOperator (R : H →L[ℂ] H) (hi : Function.Injective R) : H →ₗ.[ℂ] H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventGraph.lean:36` — `3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b`

```lean
theorem resolvent_graph_closed (R : H →L[ℂ] H) (hi : Function.Injective R) :
    (resolventGraphOperator R hi).IsClosed
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventGraph.lean:46` — `3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b`

```lean
theorem resolvent_graph_domain_dense (R : H →L[ℂ] H) (hi : Function.Injective R)
    (hR : IsSelfAdjoint R) : Dense ((resolventGraphOperator R hi).domain : Set H)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventGraph.lean:50` — `3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b`

```lean
theorem resolvent_graph_selfadjoint (R : H →L[ℂ] H) (hi : Function.Injective R)
    (hR : IsSelfAdjoint R) : IsSelfAdjoint (resolventGraphOperator R hi)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventGraph.lean:78` — `3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b`

```lean
theorem resolvent_graph_positive (R : H →L[ℂ] H) (hi : Function.Injective R)
    (hR : 0 ≤ R) (hone : R ≤ 1) (x : (resolventGraphOperator R hi).domain) :
    0 ≤ (inner ℂ (x : H) (resolventGraphOperator R hi x)).re
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularFlowAbsorption.lean:51` — `4760792d98c8d625e9109bd7d0b2a97713bd236dcb7d6db1a4f07251cdc0c9f9`

```lean
def regularFlowAbsorptionUnitary (P : SiteProfile) :
    unitary (RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\Fourier\LpSpace.lean:50` — `82b647b1998edea8d60ac8f986fd5735d697044e586464a05d71d0a346522cfe`

```lean
def fourierTransformₗᵢ : (Lp (α := E) F 2) ≃ₗᵢ[ℂ] (Lp (α := E) F 2)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\Sigmoid.lean:63` — `01fafea90dcd4d58cfcb91454b618a3c55f9a26f347b729bb3cb8fadc3bf2df2`

```lean
noncomputable def sigmoid (x : ℝ)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\InnerProductSpace\Adjoint.lean:881` — `d1636c8ae9160d3762630f6f99815134dbc4da51188d9e2e34dcc3c06c6c32fc`

```lean
def conjStarAlgEquiv (e : H ≃ₗᵢ[𝕜] K) : (H →L[𝕜] H) ≃⋆ₐ[𝕜] (K →L[𝕜] K)
```

## Buscas e aceitação

Seis modalidades e outras bancadas registradas em C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_positive_generator\20260914_184229_267676\searches.json. Ausência nos recortes não é ausência universal. Build, axiomas e controles/revisão separados antecedem aceite. Nenhum fornecedor antigo é alterado.
