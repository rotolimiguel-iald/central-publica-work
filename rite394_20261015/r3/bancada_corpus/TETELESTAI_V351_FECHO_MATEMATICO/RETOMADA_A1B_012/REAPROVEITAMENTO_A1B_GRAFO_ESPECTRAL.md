[OPEN — ficha anterior à identificação espectral do grafo]

# A1(b): o mesmo grafo nas coordenadas espectrais

2026-09-14T19:08:08.583582-03:00

For every SiteProfile P and x,y in the existing regular Hilbert space: (x,y) in graph(regularPositiveGenerator P) iff almost everywhere xi, (V.symm y)(xi) = exp(-2*pi*xi) smul (V.symm x)(xi), with V=regularSpectralCoordinates P. No new Hilbert space, graph, multiplier, Fourier transform or generator. Exact identification needed by regular_unitary_positive_generator / future imaginary powers.

A busca nominal negativa não é ausência universal. A equação resolvente já foi paga: consumi-la. Novo módulo consumidor, sem editar o módulo de quinze declarações que está em revisão. Não promover prova DEV à aceitação.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventGraph.lean:20` — `3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b`

```lean
theorem resolvent_graph_equation (R : H →L[ℂ] H) (hi : Function.Injective R) (x y : H) :
    (x,y) ∈ (resolventGraphOperator R hi).graph ↔ (1-R) x = R y
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2PositiveMultiplier.lean:30` — `6e3946aff9964e1a6a59a8dcb99a11b4a3c0026a6b0220f7df4b9901f83f3bdf`

```lean
theorem realScalarMultiplier_ae (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) (f : RegularHilbert H) :
    realScalarMultiplier g hg h0 h1 f =ᵐ[volume] fun s => (g s : ℂ) • f s
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:122` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularPositiveGenerator (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →ₗ.[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:72` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularSpectralCoordinates (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) ≃ₗᵢ[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:78` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularSpectralResolvent (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\Sigmoid.lean:113` — `01fafea90dcd4d58cfcb91454b618a3c55f9a26f347b729bb3cb8fadc3bf2df2`

```lean
lemma sigmoid_mul_rexp_neg (x : ℝ) : sigmoid x * exp (-x) = sigmoid (-x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\Sigmoid.lean:108` — `01fafea90dcd4d58cfcb91454b618a3c55f9a26f347b729bb3cb8fadc3bf2df2`

```lean
lemma sigmoid_neg (x : ℝ) : sigmoid (-x) = 1 - sigmoid x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\InnerProductSpace\Adjoint.lean:885` — `d1636c8ae9160d3762630f6f99815134dbc4da51188d9e2e34dcc3c06c6c32fc`

```lean
@[simp] lemma conjStarAlgEquiv_apply_apply (e : H ≃ₗᵢ[𝕜] K) (x : H →L[𝕜] H) (y : K) :
    e.conjStarAlgEquiv x y = e (x (e.symm y))
```

Buscas nas seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_spectral_graph\20260914_190746_524794\searches.json.
