[OPEN — ficha anterior à passagem da ação direita por CFC]

# A1(b): a álgebra fechada que permite consumir cfc_mem

2026-09-14T20:43:21.434382-03:00

Construct a norm-closed star subalgebra of the EXISTING core, consisting of b and b* for which the actual original polar right identity holds on ALL n_nu. Characterize the property by the existing natural cut equations (of_cut_actions), so closedness follows from equality of continuous maps, without a new GNS or trace. Map this algebra by the same core inclusion into ambient bounded operators; the ambient image is closed since the core is a norm-closed bicommutant. Consume mathlib cfc_mem in the ambient CFC to pass the right identity to continuous functions. Consumer: (a) R_n=sigmoid(n sin(k/n)), with k determined by Lambda, to obtain the right action of actual R by bounded strong limits; (b) sqrt(B_epsilon) as an identified continuous function of R. Do not assume a CFC or CompleteSpace instance on N and do not claim that R_n convergence, identification of sqrt(B_epsilon), the trace or traciality are proved by this step.

O novo empacotamento algébrico tem consumidor preciso: cfc_mem exige uma subálgebra estrela fechada, e transportará a identidade direita já produzida. Não é nova realização do core ou novo operador. O fechamento GNS foi aceito; os limites da ação direita têm auditoria autoral rc0 e aguardam revisão neste instante.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarGNSClosedness.lean:35` — `13a1e9e22229c905922b94bc56c6fedc24dd80ea5072544934ffad2fa33e8bc8`

```lean
theorem scalarWeightGNSEmbedding_of_cut_actions (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (v : ScalarGNSHilbert P)
    (hcut : ∀ n : ℕ, scalarGNSCutMap P (n : ℝ) v =
      dualOrbitRepresentation A.val (scalarCutVacuum P (n : ℝ))) :
    ∃ hA : A ∈ scalarWeightLeftIdeal P, scalarWeightGNSEmbedding P ⟨A,hA⟩ = v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarGNSClosedness.lean:14` — `13a1e9e22229c905922b94bc56c6fedc24dd80ea5072544934ffad2fa33e8bc8`

```lean
theorem scalarGNSCutMap_weight_embedding (P : SiteProfile) (r : ℝ)
    (A : scalarWeightLeftIdeal P) :
    scalarGNSCutMap P r (scalarWeightGNSEmbedding P A) =
      dualOrbitRepresentation A.val.val (scalarCutVacuum P r)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionLimits.lean:15` — `ab55b5a1e05d6f8317bc61e0a303b960dc7e9888999e03cbb1c63287e4b37b9d`

```lean
theorem scalarRightAction_regular (P : SiteProfile) (t : ℝ)
    (A : scalarWeightLeftIdeal P) :
    scalarWeightGNSEmbedding P (scalarRegularRightProduct P t A) =
      antiunitaryConjugate (scalarTomitaPolarFactor P)
        (scalarGNSRepresentation P (star (regularRightCoreElement P t)))
          (scalarWeightGNSEmbedding P A)
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

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSAction.lean:25` — `529982d9d3489dd900c8259599cede7cbf866525e4001e8196054679fae8f65a`

```lean
theorem scalarGNSAmbientAction_norm_le (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    ‖scalarGNSAmbientAction P B‖ ≤ ‖B.val‖
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualOrbitRepresentation.lean:14` — `01d61dbe3b2f4193dc48b345a1e765f017964a73a9e05070bf4e34e0510753dd`

```lean
def dualOrbitRepresentation : (RegularHilbert H →L[ℂ] RegularHilbert H) →⋆ₐ[ℂ]
    (RegularHilbert (RegularHilbert H) →L[ℂ] RegularHilbert (RegularHilbert H))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:28` — `83be0cf3f811bd6fd429c7705fdb1a00b27fdd6496ee971b9ca5f355c00d6f36`

```lean
theorem antiunitaryConjugate_mul (T V : H →L[ℂ] H) :
    antiunitaryConjugate U (T*V)=antiunitaryConjugate U T * antiunitaryConjugate U V
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\Algebra\Group\Basic.lean:49` — `486110e92d9149d3a9fadef92c8f7d2cb5907fbe534452f88844996135f52526`

```lean
lemma Set.isClosed_centralizer {M : Type*} (s : Set M) [Mul M] [TopologicalSpace M]
    [SeparatelyContinuousMul M] [T2Space M] : IsClosed (centralizer s)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Range.lean:96` — `07acc928827e7fafe0ac6baa7cea89010f8e74854cd2f77ba0d5314e1823c388`

```lean
lemma cfc_mem {𝕜' S : Type*} [Monoid 𝕜'] [MulAction 𝕜' A] [SetLike S A] [SubringClass S A]
    [SMul 𝕜 𝕜'] [IsScalarTower 𝕜 𝕜' A] [SMulMemClass S 𝕜' A] [StarMemClass S A] {s : S}
    [hs : IsClosed (s : Set A)] (f : 𝕜 → 𝕜) {a : A} (has : a ∈ s) :
    cfc f a ∈ s
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_right_action_algebra\20260914_204252_823508\searches.json. Ausência nominal nos recortes não é ausência universal.
