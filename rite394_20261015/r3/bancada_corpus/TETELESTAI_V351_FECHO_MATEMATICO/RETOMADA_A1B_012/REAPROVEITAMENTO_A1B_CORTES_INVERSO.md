[OPEN — ficha anterior aos cortes do inverso do mesmo gerador]

# A1(b): cortes limitados para a perturbação do peso

2026-09-14T20:05:51.744458-03:00

Construct the actual bounded inverse-generator cutoffs B_epsilon=(h+epsilon)^(-1) for epsilon>0 as epsilon^(-1) theta_(log epsilon)(R), with the SAME R=(1+h)^(-1). Prove core membership, positivity, bound by epsilon^(-1), graph equation h(B_epsilon x)=x-epsilon B_epsilon x, and dual transport theta_s B_epsilon=exp(s) B_(epsilon exp(s)). Consumer: the existing inverse-generator trace formula in LACUNAS_A1 item4. Reuse dual action and graph scaling; no new CFC, generator, base L2 or substitute trace. No assertion of additivity or traciality of a supremum before its monotonicity is established.

R é o resolvente já pago; a escala dual fornece os demais parâmetros sem uma segunda construção espectral. ε é regulador positivo do limite, não parâmetro físico. A entrada consumidora é a fórmula de τ no item4 de LACUNAS_A1.md. As propriedades do traço seguem pendentes.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:78` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularSpectralResolvent (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:84` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
theorem regularSpectralResolvent_nonneg (P : SiteProfile) :
    0 ≤ regularSpectralResolvent P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:89` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
theorem regularSpectralResolvent_le_one (P : SiteProfile) :
    regularSpectralResolvent P ≤ 1
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularGeneratorAffiliation.lean:32` — `9e172df5174e9b2b9c5315825a4a487f0fb04b34ba68dcecffd11e8d2684690e`

```lean
theorem regularSpectralResolvent_mem (P : SiteProfile) :
    regularSpectralResolvent P ∈ regularCoreAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularGeneratorDualScaling.lean:102` — `2bd647d5a4c6526780853e16b5ef1ee8f1acddc36570ebdcdc8d74f230e08d50`

```lean
theorem regularPositiveGenerator_dual_graph (P : SiteProfile) (s : ℝ)
    (x y : RegularHilbert (TowerHilbert P))
    (hxy : (x,y) ∈ (regularPositiveGenerator P).graph) :
    (characterMultiplier s x,(Real.exp s : ℂ) • characterMultiplier s y) ∈
      (regularPositiveGenerator P).graph
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularDualAction.lean:30` — `e7c3628d969c0dae2a971c156200acb88f6bf4286a9c648a2ad3da08c468040c`

```lean
theorem dualAmbient_add (s t : ℝ) :
    dualAmbient (H := H) (s+t) = (dualAmbient (H := H) s).trans (dualAmbient (H := H) t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularDualAction.lean:76` — `e7c3628d969c0dae2a971c156200acb88f6bf4286a9c648a2ad3da08c468040c`

```lean
def regularDualAction (P : SiteProfile) (s : ℝ) :
    (regularCoreAlgebra P).toStarSubalgebra ≃⋆ₐ[ℂ] (regularCoreAlgebra P).toStarSubalgebra
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventGraph.lean:89` — `3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b`

```lean
theorem resolvent_graph_resolvent_equation (R : H →L[ℂ] H) (hi : Function.Injective R)
    (u : H) : ∃ x : (resolventGraphOperator R hi).domain,
      (x : H) = R u ∧ (x : H) + resolventGraphOperator R hi x = u
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2CharacterMultiplier.lean:124` — `2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3`

```lean
theorem characterMultiplier_inverse (s : ℝ) (f : RegularHilbert H) :
    characterMultiplier s (characterMultiplier (-s) f) = f
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_inverse_cutoff\20260914_200529_560958\searches.json. Ausência nominal nos recortes não é ausência universal.
