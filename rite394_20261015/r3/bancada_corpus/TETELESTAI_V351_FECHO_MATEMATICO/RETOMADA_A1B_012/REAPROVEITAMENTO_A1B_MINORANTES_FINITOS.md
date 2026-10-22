[OPEN — ficha anterior aos minorantes finitos, condicional à tracialidade]

2026-09-14T23:59:19.278836-03:00

Same scalarInverseLimitWeight. First construct a sequence of contractions E_n=regularAverage(delta_n)*regularDomainCut(delta_n) with finite square weight and strong limit I using existing bounds/density. Then, EXPLICITLY conditional on traciality, prove the exact finite-positive-minorants field: tau(X)=sup{tau(Y):0<=Y<=X,tau(Y)<infinity}. For X=a*a with its existing CFC square root, use Y_n=(E_n a)*(E_n a) <= X. Finiteness follows by traciality, a a*<=norm(a)^2 I and positive homogeneity. Existing strong-square bound gives tau(X)<=sup tau(Y_n). No assumption that tau is tracial has been discharged here; no extra trace/GNS/root, no independent normalization, no completion of A1(b). Delta27 is author-validated, independent review pending at fiche creation; final acceptance of this consumer waits for27.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitSemifiniteness.lean:78` — `0af32fbe3a7f0a36ef61f8e247c24a6117fab4f2b2b778890492b21e13f2f7a1`

```lean
theorem scalarInverseLimitWeight_domainCut_finite (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ)
    (a : scalarWeightLeftIdeal P) :
    scalarInverseLimitWeight P (TGLV351.positiveSquare P (a.val * regularDomainCut P δ)) < ⊤
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:38` — `60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9`

```lean
theorem regularDomainCut_bounds (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    0 ≤ (regularDomainCut P δ).val ∧ (regularDomainCut P δ).val ≤ 1
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:113` — `60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9`

```lean
theorem regularDomainCut_tendsto_identity (P : SiteProfile)
    (v : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun n : ℕ => (regularDomainCut P (1/((n : ℝ)+1))).val v) atTop (𝓝 v)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongBoundedApplication.lean:15` — `dd68e70d90c4c475bfbe1770df5428666fd9345ed28b81c2addfef16f56017a0`

```lean
theorem bounded_application_tendsto {ι : Type*} (l : Filter ι)
    (A : ι → H →L[ℂ] H) (C : ℝ) (hbound : ∀ i, ‖A i‖ ≤ C)
    (v : ι → H) (v₀ w : H) (hv : Tendsto v l (𝓝 v₀))
    (hfixed : Tendsto (fun i => A i v₀) l (𝓝 w)) :
    Tendsto (fun i => A i (v i)) l (𝓝 w)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarDualWeight.lean:55` — `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

```lean
theorem HasFiniteDualSquare.scalar_finite (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hf : HasFiniteDualSquare A) :
    dualQuadraticIntegral (star A * A) (regularVacuum P) < ⊤
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitTracialExtension.lean:46` — `b1987ee0746e1f64da3920ac11a44a39f263ccb4108ace1b86e630f4a9d3aeb3`

```lean
theorem scalarInverseLimitWeight_square_le_of_strong (P : SiteProfile)
    (A : ℕ → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hlim : ∀ v, Tendsto (fun n => (A n).val v) atTop (𝓝 (S.val v)))
    (C : ℝ≥0∞) (hb : ∀ n, scalarInverseLimitWeight P (positiveSquare P (A n)) ≤ C) :
    scalarInverseLimitWeight P (positiveSquare P S) ≤ C
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:104` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
theorem scalarInverseLimitWeight_scale (P : SiteProfile) (r : ℝ≥0) (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P (X.scale r) = (r : ℝ≥0∞) * scalarInverseLimitWeight P X
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:109` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
theorem scalarInverseLimitWeight_mono (P : SiteProfile) (X Y : PositiveCoreInput P) (hXY : X ≤ Y) :
    scalarInverseLimitWeight P X ≤ scalarInverseLimitWeight P Y
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350LevelExpectationUniformBound.lean:57` — `6ec762be7f9014e45f88ffa9971a0e1672618f6d4289fb7e6247e5159a21e6b5`

```lean
theorem vonNeumann_norm_closed {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (M : VonNeumannAlgebra H) :
    IsClosed (M : Set (H →L[ℂ] H))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Range.lean:205` — `07acc928827e7fafe0ac6baa7cea89010f8e74854cd2f77ba0d5314e1823c388`

```lean
lemma cfcₙ_mem {𝕜' S : Type*} [Monoid 𝕜'] [MulAction 𝕜' A] [SetLike S A] [NonUnitalSubringClass S A]
    [SMul 𝕜 𝕜'] [IsScalarTower 𝕜 𝕜' A] [SMulMemClass S 𝕜' A] [StarMemClass S A] {s : S}
    [hs : IsClosed (s : Set A)] (f : 𝕜 → 𝕜) {a : A} (has : a ∈ s) :
    cfcₙ f a ∈ s
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Order.lean:195` — `0802a500623d378e8c953961cac3c6391932515a7236d44dbceea11e2eb4611b`

```lean
lemma CStarAlgebra.mul_star_le_algebraMap_norm_sq {a : A} :
    a * star a ≤ algebraMap ℝ A (‖a‖ ^ 2)
```

Buscas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_finite_minorants\20260914_235857_539749\searches.json. Ausência nominal não é ausência universal. O helper de raiz privado de V351AllPositiveWeightOrder não é refeito como novo teorema: seu consumidor usa diretamente cfcₙ_mem e sqrt_mul_sqrt_self.
