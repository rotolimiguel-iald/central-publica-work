[OPEN — ficha anterior ao balanço limitado dos cortes]

2026-09-15T01:17:59.404386-03:00

ADAPTAR/OPEN: proposed next exact bounded balance for epsilon,eta>0 in SAME H_nu: (1-T) C_epsilon q_eta = T p_epsilon D_eta, where T=scalarTomitaResolvent P, C_epsilon=pi(B_epsilon), D_eta=antiunitaryConjugate J (pi(B_eta)), p_epsilon=1-epsilon C_epsilon, q_eta=1-eta D_eta, B_epsilon=regularInverseGeneratorCutoff P epsilon. Names C,D,p,q here are notation, not new global definitions. This identity is NOT paid by equal group names or commutation. Delta32 equality of original groups has author rc0 and independent review pending at fiche time. CorePolarInclusion already pays C/D cross commutation on the SAME GNS: do not reprove right action or commutant inclusion. The real missing step is recovering the bounded balance from the actual spectral/group realization, or an equally concrete quadratic equality directly on finiteDualStarCore. Next consumption: original root graph x=sqrt(T)u, B_nu*x=sqrt(1-T)u plus positive_sqrt_intertwines, two cut limits -> Q(B_nu Lambda(a))=Q(J Lambda(a)), including infinity; existing tracial_iff_core then extends. This is a proof strategy, not a compiled consequence. No h=Delta_nu, new GNS, arbitrary product of unbounded operators, new field assuming balance, or full joint CFC unless a located concrete consumer truly requires it. Existing regularSineResolvent_tendsto is a particular regular spectral construction, NOT a generic inverse theorem recovering T_nu from U_t. Do not count conditional form rearrangements as payment of balance.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ModularImplementation.lean:16` — `3d16720656388fc14f70b5e5ded6a8a4d3fc6f72034992bbeee10364c8202a9f`

```lean
theorem scalarTomitaImaginaryPower_eq_regular_implementation (P : SiteProfile)
    (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t x =
      scalarGNSRepresentation P (regularRightCoreElement P t) (regularRightGNS P (-t) x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350CorePolarInclusion.lean:52` — `4d5d416c82894dcc93562986ce8eae7ebc2c11f313eb658dc18e356af37dbd8d`

```lean
theorem scalarTomitaPolar_core_commutes (P : SiteProfile)
    (A B : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute (antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P A)) (scalarGNSRepresentation P B)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:17` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_mem (P : SiteProfile) (ε : ℝ) :
    regularInverseGeneratorCutoff P ε ∈ regularCoreAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:24` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_nonneg (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    0 ≤ regularInverseGeneratorCutoff P ε
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarTomitaPositiveRoot.lean:15` — `721afac12bff6654a1f1cdeadc1077d8df9a531d81dc1eac91a017e9bdec59b2`

```lean
def scalarTomitaPositiveRoot : ScalarGNSHilbert P →ₗ.[ℂ] ScalarGNSHilbert P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventSquareRoot.lean:37` — `6a1ad3a2fa7041aa45d56b2448e18a5fce6b90e9e069f045df89483ecb1e3f90`

```lean
theorem resolventSquareRoot_domain (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) :
    (resolventSquareRoot R hR hi).domain = (CFC.sqrt R).range
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350PositiveRootIntertwining.lean:50` — `f357246ac96d1d98fc1376238be4ca039f425d2782dd23d909ac5cdd3d1afaa5`

```lean
theorem positive_sqrt_intertwines (A B U : H →L[ℂ] H)
    (hA : 0 ≤ A) (hB : 0 ≤ B) (h : A*U=U*B) :
    CFC.sqrt A * U = U * CFC.sqrt B
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:113` — `60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9`

```lean
theorem regularDomainCut_tendsto_identity (P : SiteProfile)
    (v : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun n : ℕ => (regularDomainCut P (1/((n : ℝ)+1))).val v) atTop (𝓝 v)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351PerturbedWeightNorm.lean:37` — `9b4edeb94844ded88ec595b50160936d42e34637f4432493d02894dd7731bab9`

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

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitTracialExtension.lean:125` — `b1987ee0746e1f64da3920ac11a44a39f263ccb4108ace1b86e630f4a9d3aeb3`

```lean
theorem scalarInverseLimitWeight_tracial_iff_core (P : SiteProfile) :
    (∀ A : (regularCoreAlgebra P).toStarSubalgebra,
      scalarInverseLimitWeight P (positiveSquare P A) =
        scalarInverseLimitWeight P (positiveSquare P (star A))) ↔
    (∀ A : (regularCoreAlgebra P).toStarSubalgebra, A ∈ finiteDualStarCore P →
      scalarInverseLimitWeight P (positiveSquare P A) =
        scalarInverseLimitWeight P (positiveSquare P (star A)))
```

Buscas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_double_cut_balance\20260915_011735_080466\searches.json. Ausência nominal não é ausência universal. Consulta curta do revisor após31 e antes32 lida: balanço limitado proposto, não provado. Principal relê CorePolarInclusion para evitar nova prova de comutação já disponível. Novo extrator respeita parênteses antes de procurar :=, evitando truncamento em argumentos nomeados; fichas históricas preservadas.
