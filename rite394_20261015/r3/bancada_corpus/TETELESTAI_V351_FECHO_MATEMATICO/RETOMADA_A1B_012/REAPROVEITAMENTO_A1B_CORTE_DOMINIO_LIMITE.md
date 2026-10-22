[OPEN — ficha anterior ao corte de domínio do peso limite]

# A1(b): corte algébrico sem outra raiz

2026-09-14T23:03:13.391858-03:00

Use q_delta=1-delta*B_delta, in the SAME regular core and polar right algebra. Prove positivity/contraction, the uniform product bound B_epsilon*q_delta^2 <= delta^(-1)*I and strong convergence q_(1/(n+1)) to I. Reuse the inverse identity, positivity of commuting products and dense range of 1-R. Consumers: finite-domain cutoff estimate of scalarInverseLimitWeight and WOT density of its square-finite set. This fiche covers that sequential route; it does not assert any new theorem or semifinal contract. No new root, spectral calculus, GNS, traciality or positive finite minorants of the original nontracial weight.

ADAPTAR a rota menor q_delta da consulta independente revisao_consulta_semifinitude_limite/CONSULTA_SEMIFINITUDE_LIMITE. A cota pode depender de delta, mas deve ser uniforme em epsilon antes do supremo. Semifinitude usual e minorantes positivos do contrato são obrigações distintas.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:24` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_nonneg (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    0 ≤ regularInverseGeneratorCutoff P ε
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:31` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_le (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    regularInverseGeneratorCutoff P ε ≤
      (ε⁻¹ : ℂ) • (1 : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:43` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_one (P : SiteProfile) :
    regularInverseGeneratorCutoff P 1 = regularSpectralResolvent P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegulatorWeightOrder.lean:22` — `b908f79a4d20ca8f456eb245e2a605a6cc6e611667e1c8a8d6cb1cee2ee4f838`

```lean
theorem regularInverseGeneratorCutoff_commutes (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    Commute (regularInverseGeneratorCutoff P ε) (regularInverseGeneratorCutoff P η)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegulatorWeightOrder.lean:29` — `b908f79a4d20ca8f456eb245e2a605a6cc6e611667e1c8a8d6cb1cee2ee4f838`

```lean
theorem regularInverseGeneratorCutoff_resolvent_identity (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    regularInverseGeneratorCutoff P ε - regularInverseGeneratorCutoff P η =
      ((η-ε : ℝ) : ℂ) • (regularInverseGeneratorCutoff P η * regularInverseGeneratorCutoff P ε)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:94` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    (⟨regularInverseGeneratorCutoff P ε,regularInverseGeneratorCutoff_mem P ε⟩ :
      (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:94` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
def scalarPolarRightAlgebra (P : SiteProfile) :
    StarSubalgebra ℂ (regularCoreAlgebra P).toStarSubalgebra
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:104` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
theorem regularSpectralResolvent_complement_injective (P : SiteProfile) :
    Function.Injective (1-regularSpectralResolvent P :
      RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\BoundedGraphOperator.lean:118` — `4d70d27d25f31fed13b73a7ae60601478718e41bbc38c24c38117b0cc26dc84f`

```lean
theorem bounded_graph_domain_dense [CompleteSpace E] (A B : E →L[ℂ] E) (hAi : Function.Injective A)
    (hA : IsSelfAdjoint A) :
    Dense ((boundedGraphOperator A B hAi).domain : Set E)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\UniformSpace\Equicontinuity.lean:980` — `dd3e8de0798b50489e45f0e117af17473290e2e1c1fc26218e7beccd3cdce692`

```lean
theorem Equicontinuous.isClosed_setOf_tendsto {l : Filter ι} {F : ι → X → α} {f : X → α}
    (hF : Equicontinuous F) (hf : Continuous f) :
    IsClosed {x | Tendsto (F · x) l (𝓝 (f x))}
```

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

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarWeightSemifiniteness.lean:16` — `f5e7e85b034949be6517286f60c692d3d97d29c341aeba42a1f7172b7e610c2a`

```lean
theorem scalarWeight_square_finite_wot_closure (P : SiteProfile) :
    closure {A : RegularHilbert (TowerHilbert P) →WOT[ℂ]
        RegularHilbert (TowerHilbert P) |
      A.toCLM ∈ regularCoreAlgebra P ∧ HasFiniteScalarSquare P A.toCLM} =
    {A : RegularHilbert (TowerHilbert P) →WOT[ℂ]
        RegularHilbert (TowerHilbert P) | A.toCLM ∈ regularCoreAlgebra P}
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularNormality.lean:19` — `bcd49e92800bf99d7770bb9969879be02a9768f129ce842ae2f39cefaca3cc0a`

```lean
theorem strong_tendsto_wot {ι : Type*} {l : Filter ι}
    (T : ι → (H →L[ℂ] H)) (B : H →L[ℂ] H)
    (hstrong : ∀ v, Tendsto (fun i => T i v) l (𝓝 (B v))) :
    Tendsto (fun i => ContinuousLinearMapWOT.ofCLM (T i)) l
      (𝓝 (ContinuousLinearMapWOT.ofCLM B))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularTopology.lean:39` — `13c92b1d8948bc4d2c3891d4cbfa9bf43ac353a95e9126e2c128b1379db0ebd5`

```lean
theorem regularCore_wot_closed (P : TGLExt.SiteProfile) :
    IsClosed {A : RegularHilbert (TGLExt.TowerHilbert P) →WOT[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P) | A.toCLM ∈ regularCoreAlgebra P}
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_domain_cut\20260914_230247_301032\searches.json. Ausência nominal nos recortes não é ausência universal.
