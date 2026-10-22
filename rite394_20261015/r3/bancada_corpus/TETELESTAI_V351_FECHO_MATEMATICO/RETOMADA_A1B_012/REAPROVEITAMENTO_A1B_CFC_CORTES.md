[OPEN — ficha anterior à identificação CFC dos cortes existentes]

# A1(b): o mesmo Bε, sua raiz positiva e a ação direita

2026-09-14T21:18:11.581799-03:00

For epsilon>0 identify the EXISTING regularInverseGeneratorCutoff P epsilon with cfc F_epsilon (regularSpectralResolvent P), F_epsilon(z)=ofReal(z.re / max(min(1,epsilon),1+(epsilon-1)*z.re)). Prove global continuity from the positive clamped denominator and equality to 1/(epsilon+exp(-kappa)) at z=sigmoid(kappa). Use original graph_iff and inverse-cutoff graph_iff to identify candidate Y through (Yx,x-epsilonYx) in the SAME graph. This avoids a new inverse of I+(epsilon-1)R or a new shifted scalar multiplier. Then consume the already proved P(R), cfc membership and standard CFC.sqrt bridges to obtain the SAME CFC.sqrt B_epsilon right action on ALL n_nu. Consumer: norm identity for the bounded positive cut perturbations of the SAME scalar weight. Do not claim their limit, monotonicity or traciality in this target.

ADAPTAR: o inverso regular, seu grafo e P(R) já estão produzidos. A ponte é identidade escalar/CFC com a equação inversa existente, sem novo h, J ou GNS. factor_positive_sqrt_mem é molde somente: seu tipo é o fator da torre, não a álgebra da ação direita. Serão usados os conversores CFC existentes. Os aproximantes têm auditoria autoral rc0 e revisão pendente neste instante.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:13` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
def regularInverseGeneratorCutoff (P : SiteProfile) (ε : ℝ) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:99` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_graph_iff (P : SiteProfile) (ε : ℝ) (hε : 0 < ε)
    (x y : RegularHilbert (TowerHilbert P)) :
    (x,y) ∈ (regularPositiveGenerator P).graph ↔
      regularInverseGeneratorCutoff P ε (y+(ε : ℂ) • x) = x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularSpectralGraph.lean:40` — `2a859d88def186591e98f2a0594bc95ae0a9c6eb74c17ea1124ce5844be1b642`

```lean
theorem regularPositiveGenerator_graph_iff (P : SiteProfile)
    (x y : RegularHilbert (TowerHilbert P)) :
    (x,y) ∈ (regularPositiveGenerator P).graph ↔
      ∀ᵐ ξ ∂volume, ((regularSpectralCoordinates P).symm y) ξ =
        (Real.exp (-(2*Real.pi*ξ)) : ℂ) •
          ((regularSpectralCoordinates P).symm x) ξ
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351SineResolventApprox.lean:231` — `a1c6f5e77916ee527da3716f634431ddaf1f36c9dd80376ceee83aeb63c20c01`

```lean
theorem regularSpectralResolvent_right (P : SiteProfile) :
    (⟨regularSpectralResolvent P,regularSpectralResolvent_mem P⟩ :
      (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:173` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
theorem scalarRightAction_cfc (P : SiteProfile)
    (b : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (f : ℂ → ℂ) :
    ∃ hf : cfc f b.val ∈ regularCoreAlgebra P,
      (⟨cfc f b.val,hf⟩ : (regularCoreAlgebra P).toStarSubalgebra) ∈
        scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarMultiplierCalculus.lean:73` — `4dfa6cbd81aa481d695c2eec89985eb06487e7ba32432528d06c62ee7147f06c`

```lean
theorem realScalarMultiplier_cfc_ae (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ x, 0 ≤ g x) (h1 : ∀ x, g x ≤ 1)
    (f : ℂ → ℂ) (hf : Continuous f) (u : RegularHilbert H) :
    cfc f (realScalarMultiplier g hg h0 h1) u =ᵐ[volume]
      fun x => f (g x : ℂ) • u x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\GeneralExpectationCP.lean:55` — `698dd6c7d5d2125671b3a3c0cf70a27c144e3dc2d845ab54e093bea018d18aee`

```lean
theorem factor_positive_sqrt_mem (P : SiteProfile)
    (A : (theFactorObject P).toStarSubalgebra) (hA : 0 ≤ A) :
    CFC.sqrt (A : TowerHilbert P →L[ℂ] TowerHilbert P) ∈
      (theFactorObject P).toStarSubalgebra
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\ContinuousFunctionalCalculus\Rpow\Basic.lean:302` — `ef03c823cc3798b288a7f00a2902b1fae092f1181bd44cb8b41ef133db389d5f`

```lean
lemma sqrt_eq_real_sqrt (a : A) (ha : 0 ≤ a := by cfc_tac) :
    CFC.sqrt a = cfcₙ Real.sqrt a
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\NonUnital.lean:870` — `61fe6bca314e50e5408d7f3e5b30c22f6dc7184924a203bfb545e799a9ad3c8d`

```lean
lemma cfcₙ_eq_cfc [ContinuousFunctionalCalculus R A p] [ContinuousMapZero.UniqueHom R A] {f : R → R}
    {a : A} (hf : ContinuousOn f (σₙ R a) := by cfc_cont_tac) (hf0 : f 0 = 0 := by cfc_zero_tac) :
    cfcₙ f a = cfc f a
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Instances.lean:352` — `f05652edd12f24ddd2aa058ceb8762cceabda14a4580d7d237dcde26aaf8d6f4`

```lean
lemma cfc_real_eq_complex {a : A} (f : ℝ → ℝ) (ha : IsSelfAdjoint a := by cfc_tac) :
    cfc f a = cfc (fun x ↦ f x.re : ℂ → ℂ) a
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_cutoff_cfc\20260914_211744_334623\searches.json. Ausência nominal nos recortes não é ausência universal.
