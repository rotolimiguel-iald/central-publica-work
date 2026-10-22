[OPEN — ficha anterior aos aproximantes explícitos do mesmo resolvente]

# A1(b): translações, seno, CFC e limite forte-*

2026-09-14T21:03:40.386751-03:00

Construct actual b_n in the SAME regularCoreAlgebra P with b_n and b_n* satisfying the original polar right identity, uniform norm at most 1, and strong-star limit regularSpectralResolvent P. Use m=n+1, X_m=1/2 I + (1/(4i))(Lambda_{-1/m}-Lambda_{1/m}), g_m(x)=(1+sin(2*pi*x/m))/2, f_m(z)=sigmoid(m*(2*Re(z)-1)), b_n=cfc(f_m,X_m). Prove spectral identity with the same regularSpectralCoordinates, then symbol sigmoid(m*sin(2*pi*x/m)) convergence to sigmoid(2*pi*x). Reuse cfc_mem through scalarRightAction_cfc, bounded strong-star closure and L2 dominated convergence. The final consumer is P(R) and hence sqrt(B_epsilon) after a separate exact CFC identification. No norm convergence, no monotonicity b_n, no bounded h or log(h), no trace claimed.

ADAPTAR: os fornecedores identificam translações e CFC, mas não produzem a família de aproximantes nem o seu limite no tipo exigido. O alvo consome exatamente esses fornecedores, sem novo GNS/J/core. O ramo por grafos/Schwartz/Kaplansky não será construído. A álgebra da ação direita tem DEV limpo e está em validação autoral/revisão neste instante; não é presumida aceita.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:173` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
theorem scalarRightAction_cfc (P : SiteProfile)
    (b : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (f : ℂ → ℂ) :
    ∃ hf : cfc f b.val ∈ regularCoreAlgebra P,
      (⟨cfc f b.val,hf⟩ : (regularCoreAlgebra P).toStarSubalgebra) ∈
        scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:164` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
theorem scalarPolarRightAlgebra_regular_mem (P : SiteProfile) (t : ℝ) :
    regularRightCoreElement P t ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionLimits.lean:26` — `ab55b5a1e05d6f8317bc61e0a303b960dc7e9888999e03cbb1c63287e4b37b9d`

```lean
theorem scalarRightAction_closed_of_bounded_strongStar (P : SiteProfile)
    {ι : Type*} {l : Filter ι} [NeBot l]
    (b : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (C : ℝ)
    (hbound : ∀ i, ‖(b i).val‖ ≤ C)
    (hstrong : ∀ x, Tendsto (fun i => (b i).val x) l (𝓝 (B.val x)))
    (hadjoint : ∀ x, Tendsto (fun i => (star (b i)).val x) l (𝓝 ((star B).val x)))
    (A : scalarWeightLeftIdeal P)
    (hact : ∀ i, ∃ hi : A.val * b i ∈ scalarWeightLeftIdeal P,
      scalarWeightGNSEmbedding P ⟨A.val*b i,hi⟩ =
        antiunitaryConjugate (scalarTomitaPolarFactor P)
          (scalarGNSRepresentation P (star (b i))) (scalarWeightGNSEmbedding P A)) :
    ∃ hAB : A.val * B ∈ scalarWeightLeftIdeal P,
      scalarWeightGNSEmbedding P ⟨A.val*B,hAB⟩ =
        antiunitaryConjugate (scalarTomitaPolarFactor P)
          (scalarGNSRepresentation P (star B)) (scalarWeightGNSEmbedding P A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularImaginaryPowers.lean:65` — `066b9cb14426365807ead587ca90ad28e3703a0f9efc0ce359519da7c5243b9a`

```lean
theorem regularSpectralCoordinates_character (P : SiteProfile) (t : ℝ)
    (u : RegularHilbert (TowerHilbert P)) :
    regularSpectralCoordinates P (characterMultiplier (2*Real.pi*t) u) =
      regularUnitary P t (regularSpectralCoordinates P u)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarMultiplierCalculus.lean:73` — `4dfa6cbd81aa481d695c2eec89985eb06487e7ba32432528d06c62ee7147f06c`

```lean
theorem realScalarMultiplier_cfc_ae (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ x, 0 ≤ g x) (h1 : ∀ x, g x ≤ 1)
    (f : ℂ → ℂ) (hf : Continuous f) (u : RegularHilbert H) :
    cfc f (realScalarMultiplier g hg h0 h1) u =ᵐ[volume]
      fun x => f (g x : ℂ) • u x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2PositiveMultiplier.lean:35` — `6e3946aff9964e1a6a59a8dcb99a11b4a3c0026a6b0220f7df4b9901f83f3bdf`

```lean
theorem realScalarMultiplier_norm_le (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) (f : RegularHilbert H) :
    ‖realScalarMultiplier g hg h0 h1 f‖ ≤ ‖f‖
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:78` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularSpectralResolvent (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularGeneratorAffiliation.lean:32` — `9e172df5174e9b2b9c5315825a4a487f0fb04b34ba68dcecffd11e8d2684690e`

```lean
theorem regularSpectralResolvent_mem (P : SiteProfile) :
    regularSpectralResolvent P ∈ regularCoreAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\Trigonometric\Sinc.lean:86` — `6b41ff5abfd8616b22dacab2a8bf81dc5a79431157fed67a3132df2e11ae6635`

```lean
lemma continuous_sinc : Continuous sinc
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecificLimits\Basic.lean:69` — `dbbeb301e5b9dacc96ecd233fd05a02846a1fc88c9606f1b1d413d08aff5142e`

```lean
theorem tendsto_one_div_add_atTop_nhds_zero_nat {𝕜 : Type*} [DivisionSemiring 𝕜] [CharZero 𝕜]
    [TopologicalSpace 𝕜] [ContinuousSMul ℚ≥0 𝕜] :
    Tendsto (fun n : ℕ ↦ 1 / ((n : 𝕜) + 1)) atTop (𝓝 0)
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_sine_resolvent\20260914_210305_572797\searches.json. Ausência nominal nos recortes não é ausência universal.
