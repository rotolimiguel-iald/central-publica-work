[OPEN] Construir, nos objetos originais, para A:N e ha:A in finiteDualStarCore P, scalarInverseLimitWeight P (positiveSquare P A)=scalarInverseLimitWeight P (positiveSquare P (star A)). O balanço33 e as duas comutações passaram compilação própria e controle negativo; revisão independente33 ainda pendente nesta ficha. Não assumir Q nem tracialidade como campo, e não reabrir as entregas1–32. Reaproveitar o grafo original da raiz: x=sqrt(T)u, B_nu x=sqrt(1-T)u. A partir do balanço, obter igualdade de formas limitadas Re<y,C_epsilon q_eta y>=Re<x,p_epsilon D_eta x>. Retirar um corte de cada vez na sequência 1/(n+1), usando positividade e contração de p/q, e comparar supremos em ENNReal, inclusive infinito. Identificar normas quadradas das raízes representadas com as formas por map_star/map_mul/sqrt_mul_sqrt_self e a identidade de peso perturbado existente. Não criar limite forte de sqrt(p_n), outro GNS, outra medida, h=Delta_nu ou produto ilimitado sem domínio. A extensão do núcleo para todo N e os minorantes finitos já existem27–28; depois deste consumidor devem ser aplicados, não reprovados. Ausência nas buscas limitadas não demonstra ausência universal.

2026-09-15T02:47:45.207362-03:00

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ModularCutBalance.lean:512
```lean
theorem scalarTomitaResolvent_double_cut_balance (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    let π := scalarGNSRepresentation P
    let J := scalarTomitaPolarFactor P
    let C := π ⟨regularInverseGeneratorCutoff P ε,regularInverseGeneratorCutoff_mem P ε⟩
    let D := antiunitaryConjugate J
      (π ⟨regularInverseGeneratorCutoff P η,regularInverseGeneratorCutoff_mem P η⟩)
    Commute (scalarTomitaResolvent P) C ∧ Commute (scalarTomitaResolvent P) D ∧
      (1-scalarTomitaResolvent P)*C*antiunitaryConjugate J (π (regularDomainCut P η)) =
        scalarTomitaResolvent P * π (regularDomainCut P ε) * D
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350PositiveRootIntertwining.lean:50
```lean
theorem positive_sqrt_intertwines (A B U : H →L[ℂ] H)
    (hA : 0 ≤ A) (hB : 0 ≤ B) (h : A*U=U*B) :
    CFC.sqrt A * U = U * CFC.sqrt B
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventSquareRoot.lean:37
```lean
theorem resolventSquareRoot_domain (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) :
    (resolventSquareRoot R hR hi).domain = (CFC.sqrt R).range
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\BoundedGraphOperator.lean:50
```lean
theorem bounded_graph_parameter_apply (A : E →L[ℂ] E) (hAi : Function.Injective A)
    (x : A.range) :
    A (boundedGraphParameter A hAi x) = (x : E)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\BoundedGraphOperator.lean:65
```lean
theorem bounded_graph_apply (A B : E →L[ℂ] E) (hAi : Function.Injective A)
    (x : (boundedGraphOperator A B hAi).domain) :
    boundedGraphOperator A B hAi x = B (boundedGraphParameter A hAi x)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarTomitaPositiveRoot.lean:15
```lean
def scalarTomitaPositiveRoot : ScalarGNSHilbert P →ₗ.[ℂ] ScalarGNSHilbert P
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarTomitaPolarFactor.lean:54
```lean
theorem scalarTomitaPolarFactor_factorization (x : scalarClosedTomitaDomain P) :
    scalarTomitaPolarFactor P
      (scalarTomitaPositiveRoot P (Submodule.inclusion (scalarClosedTomitaDomain_le_root P) x))=
        scalarClosedTomita P x
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:38
```lean
theorem regularDomainCut_bounds (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    0 ≤ (regularDomainCut P δ).val ∧ (regularDomainCut P δ).val ≤ 1
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:113
```lean
theorem regularDomainCut_tendsto_identity (P : SiteProfile)
    (v : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun n : ℕ => (regularDomainCut P (1/((n : ℝ)+1))).val v) atTop (𝓝 v)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSStrongContinuity.lean:16
```lean
theorem scalarGNSRepresentation_tendsto_of_uniformly_bounded (P : SiteProfile)
    {ι : Type*} {l : Filter ι}
    (T : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (C : ℝ)
    (hbound : ∀ i, ‖(T i).val‖ ≤ C)
    (hT : ∀ v, Tendsto (fun i => (T i).val v) l (𝓝 (B.val v)))
    (v : ScalarGNSHilbert P) :
    Tendsto (fun i => scalarGNSRepresentation P (T i) v) l
      (𝓝 (scalarGNSRepresentation P B v))
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351PerturbedWeightNorm.lean:37
```lean
theorem scalarWeight_inverseCutoff_perturbed_norm (P : SiteProfile)
    (ε : ℝ) (hε : 0 < ε) (A : scalarWeightLeftIdeal P) :
    ∃ hb : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      dualQuadraticIntegral
        (star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) *
          (star A.val.val * A.val.val) *
          hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) (regularVacuum P) =
      ENNReal.ofReal (‖scalarGNSRepresentation P
        (star (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),hb⟩ :
          (regularCoreAlgebra P).toStarSubalgebra))
        ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A))‖^2)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:87
```lean
def scalarInverseLimitWeight (P : SiteProfile) (X : PositiveCoreInput P) : ℝ≥0∞
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitTracialExtension.lean:125
```lean
theorem scalarInverseLimitWeight_tracial_iff_core (P : SiteProfile) :
    (∀ A : (regularCoreAlgebra P).toStarSubalgebra,
      scalarInverseLimitWeight P (positiveSquare P A) =
        scalarInverseLimitWeight P (positiveSquare P (star A))) ↔
    (∀ A : (regularCoreAlgebra P).toStarSubalgebra, A ∈ finiteDualStarCore P →
      scalarInverseLimitWeight P (positiveSquare P A) =
        scalarInverseLimitWeight P (positiveSquare P (star A)))
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitFiniteMinorants.lean:84
```lean
theorem scalarInverseLimitWeight_finite_minorants (P : SiteProfile)
    (htr : ∀ a : (regularCoreAlgebra P).toStarSubalgebra,
      scalarInverseLimitWeight P (positiveSquare P a) =
        scalarInverseLimitWeight P (positiveSquare P (star a)))
    (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P X =
      ⨆ (Y : PositiveCoreInput P) (_ : Y ≤ X)
        (_ : scalarInverseLimitWeight P Y < ⊤), scalarInverseLimitWeight P Y
```

Buscas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_quadratic_trace\20260915_024720_414956\searches.json
