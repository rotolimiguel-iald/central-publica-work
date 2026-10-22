[OPEN — ficha anterior à passagem da ação direita por limites]

# A1(b): ação direita e limites fortes-* limitados

2026-09-14T20:34:24.167831-03:00

Extend the existing right action through actual bounded strong-star limits. For A in n_nu, b_i and b in the same core, ||b_i||<=C, b_i and b_i* tending strongly to b and b*, and already proved Lambda_nu(A b_i)=J pi(b_i*) J Lambda_nu(A), construct A b in n_nu and the same identity at b. J is scalarTomitaPolarFactor, not the tower J by name. Derive norm convergence of the right vectors from existing normality of pi and continuity of J; then consume full GNS closedness. Also exhibit the initial identity for each regular unitary by consuming existing regularRightGNS_intertwines and scalarTomitaPolarFactor_regular_left. Consumer: actual action of sqrt(B_epsilon) for the inverse-generator weight perturbation, LACUNAS_A1 item4. Do not claim any approximating net has been constructed, or that all of W*(Lambda) is reached.

O fechamento do mapa GNS é fornecedor recém compilado, ainda em revisão. A continuidade forte limitada de π aplicada aos adjuntos produz a convergência dos vetores direitos. Não será inventada uma rede de aproximação de R: fornecê-la ou uma rota alternativa segue sendo a próxima obrigação. Sem novo tipo de representação.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarGNSClosedness.lean:79` — `13a1e9e22229c905922b94bc56c6fedc24dd80ea5072544934ffad2fa33e8bc8`

```lean
theorem scalarWeightGNSEmbedding_closed_of_bounded_strong (P : SiteProfile)
    {ι : Type*} {l : Filter ι} [NeBot l]
    (T : ι → scalarWeightLeftIdeal P)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (v : ScalarGNSHilbert P) (C : ℝ)
    (hbound : ∀ i, ‖(T i).val.val‖ ≤ C)
    (hstrong : ∀ x, Tendsto (fun i => (T i).val.val x) l (𝓝 (A.val x)))
    (hgns : Tendsto (fun i => scalarWeightGNSEmbedding P (T i)) l (𝓝 v)) :
    ∃ hA : A ∈ scalarWeightLeftIdeal P, scalarWeightGNSEmbedding P ⟨A,hA⟩ = v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSStrongContinuity.lean:16` — `a01a6e42e191d7bc7ce2a37e529fead8d04463b62d19f081fd640f249e2b3938`

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

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightGNS.lean:98` — `92ac2b64b81b6389a2900ddd63dceabcc2f150a05bab59ce8e903352a7fa12fa`

```lean
theorem regularRightGNS_intertwines (P : SiteProfile) (t : ℝ) (A : scalarWeightLeftIdeal P) :
    regularRightGNS P t (scalarWeightGNSEmbedding P A) =
      scalarWeightGNSEmbedding P (scalarRegularRightProduct P t A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightGNS.lean:30` — `92ac2b64b81b6389a2900ddd63dceabcc2f150a05bab59ce8e903352a7fa12fa`

```lean
def scalarRegularRightProduct (P : SiteProfile)
    (t : ℝ) (A : scalarWeightLeftIdeal P) : scalarWeightLeftIdeal P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightPolar.lean:113` — `cab5601b5e0a1e1ef950638a2025c814488c3f5baa083c14d85028a1ca9d95c9`

```lean
theorem scalarTomitaPolarFactor_regular_left (P : SiteProfile) (t : ℝ)
    (z : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P
      (scalarGNSRepresentation P (star (regularRightCoreElement P t)) z) =
        regularRightGNS P t (scalarTomitaPolarFactor P z)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarTomitaPolarInvolution.lean:72` — `b7cecd7d64b40a7de3bb5cb81ad90feeed1883943c0e566442eeb12abc83984d`

```lean
theorem scalarTomitaPolarFactor_involutive : Function.Involutive (scalarTomitaPolarFactor P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:25` — `83be0cf3f811bd6fd429c7705fdb1a00b27fdd6496ee971b9ca5f355c00d6f36`

```lean
theorem antiunitaryConjugate_apply (T : H →L[ℂ] H) (x : H) :
    antiunitaryConjugate U T x=U (T (U.symm x))
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_right_action_limits\20260914_203357_459349\searches.json. Ausência nominal nos recortes não é ausência universal.
