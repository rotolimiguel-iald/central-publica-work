[OPEN — fornecedores recuperados antes do código]

2026-09-14T22:15:22.996428-03:00

Reusar vonNeumann_norm_closed no MESMO core. O corpo de vonNeumann_starOrdered já mostra a pertença da raiz por cfcₙ_mem e sua identidade quadrática; adaptar somente o empacotamento do hilbertPositiveSqrt, sem nova raiz e sem nova demonstração de fechamento. Não inferir que StarOrderedRing abstrato sozinho fornece uma única raiz. Os fornecedores mathlib abaixo foram lidos antes do alvo.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350LevelExpectationUniformBound.lean:57

```lean
theorem vonNeumann_norm_closed {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (M : VonNeumannAlgebra H) :
    IsClosed (M : Set (H →L[ℂ] H))
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350LevelExpectationUniformBound.lean:65

```lean
theorem vonNeumann_starOrdered {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (M : VonNeumannAlgebra H) :
    StarOrderedRing M.toStarSubalgebra
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Range.lean:205

```lean
lemma cfcₙ_mem {𝕜' S : Type*} [Monoid 𝕜'] [MulAction 𝕜' A] [SetLike S A] [NonUnitalSubringClass S A]
    [SMul 𝕜 𝕜'] [IsScalarTower 𝕜 𝕜' A] [SMulMemClass S 𝕜' A] [StarMemClass S A] {s : S}
    [hs : IsClosed (s : Set A)] (f : 𝕜 → 𝕜) {a : A} (has : a ∈ s) :
    cfcₙ f a ∈ s
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\ContinuousFunctionalCalculus\Rpow\Basic.lean:302

```lean
lemma sqrt_eq_real_sqrt (a : A) (ha : 0 ≤ a := by cfc_tac) :
    CFC.sqrt a = cfcₙ Real.sqrt a
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\ContinuousFunctionalCalculus\Rpow\Basic.lean:265

```lean
lemma sqrt_mul_sqrt_self (a : A) (ha : 0 ≤ a := by cfc_tac) : sqrt a * sqrt a = a
```

