[OPEN — ficha anterior ao fechamento do mapa GNS do peso]

# A1(b): fechamento da inscrição GNS do peso sob duas convergências

2026-09-14T20:25:13.984148-03:00

Closedness of the EXISTING full weight GNS embedding: for any nontrivial filter l, A_i in n_nu uniformly bounded in operator norm, A_i converging strongly to A in the same core, and Lambda_nu(A_i) converging in GNS norm to v, prove A in n_nu and Lambda_nu(A)=v. Both convergences are hypotheses; strong convergence alone does not imply GNS convergence. Reuse existing finite cut maps and the dualOrbit factorization for arbitrary nets, and hasFiniteScalarSquare_iff_memLp. Consumer: extension of the already constructed right action of regular unitaries to bounded centralizer elements sqrt(B_epsilon) in pedersen_takesaki_inverse_generator_trace, LACUNAS_A1 item4. No new Hilbert space, state, trace or abstract predual.

O ideal, os cortes e a representação são os existentes. O lema só fecha o grafo da inscrição; não produz convergência GNS a partir da convergência forte. A entrada consumidora é a ação direita dos cortes inversos na fórmula de τ do item4 de LACUNAS_A1.md. As propriedades do traço seguem pendentes.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarHomogeneousRightOrbit.lean:14` — `dea570f1f1d43c026874d322b44fbf7e9c30856c2fac17e252319d799085c730`

```lean
theorem hasFiniteScalarSquare_iff_memLp (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) :
    HasFiniteScalarSquare P A ↔ MemLp (fun s : ℝ => dualAmbient s A (regularVacuum P)) 2
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightCompletion.lean:90` — `b8a87c9b03f233e8e0a04a92aaa7c6cd4499fb8421746902f2b0b90feb883d7c`

```lean
def scalarWeightGNSEmbedding (P : SiteProfile) : scalarWeightLeftIdeal P →ₗ[ℂ] ScalarGNSHilbert P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightOrbit.lean:57` — `9d170b4b28f7ad8da5cce31e9d2e1b7b7216ccef6519a626e42be39ef0b27255`

```lean
theorem scalarWeightOrbit_ae (P : SiteProfile) (A : scalarWeightLeftIdeal P) :
    (scalarWeightOrbit P A : ℝ → RegularHilbert (TowerHilbert P)) =ᵐ[volume]
      fun s => (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val.val (regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSCutMaps.lean:50` — `2daee56a03944695f137e54fa8a0f76883cbd453d707aa626e5d201700286b5e`

```lean
def scalarGNSCutMap (P : SiteProfile) (R : ℝ) :
    ScalarGNSHilbert P →L[ℂ] RegularHilbert (RegularHilbert (TowerHilbert P))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarCutVacuum.lean:20` — `524ca91fbe926c9cca9d556da92933d7b1ba037cf57dfd572250a7f12770c24e`

```lean
theorem scalarCutVacuum_ae (P : SiteProfile) (R : ℝ) :
    (scalarCutVacuum P R : ℝ → RegularHilbert (TowerHilbert P)) =ᵐ[volume]
      (Set.Ioc (-R) R).indicator (fun _ => (Real.sqrt dualHaarFactor : ℝ) • regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarCutVacuum.lean:35` — `524ca91fbe926c9cca9d556da92933d7b1ba037cf57dfd572250a7f12770c24e`

```lean
theorem scalarGNSCutMap_embedding_eq_action (P : SiteProfile) (R : ℝ)
    (A : finiteDualLeftIdeal P) :
    scalarGNSCutMap P R (scalarGNSEmbedding P A) =
      dualOrbitRepresentation A.val.val (scalarCutVacuum P R)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualOrbitStrongLimits.lean:45` — `a1c944185a25d4fe2c57491cae8f063845c2ae0d9c64d536ddfb7e4e797b15a3`

```lean
theorem dualOrbit_tendsto_of_uniformly_bounded {ι : Type*} {l : Filter ι}
    (T : ι → (RegularHilbert H →L[ℂ] RegularHilbert H))
    (S : RegularHilbert H →L[ℂ] RegularHilbert H) (C : ℝ)
    (hbound : ∀ i, ‖T i‖ ≤ C)
    (hT : ∀ v, Tendsto (fun i => T i v) l (𝓝 (S v)))
    (f : RegularHilbert (RegularHilbert H)) :
    Tendsto (fun i => dualOrbitRepresentation (T i) f) l
      (𝓝 (dualOrbitRepresentation S f))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightGNS.lean:98` — `92ac2b64b81b6389a2900ddd63dceabcc2f150a05bab59ce8e903352a7fa12fa`

```lean
theorem regularRightGNS_intertwines (P : SiteProfile) (t : ℝ) (A : scalarWeightLeftIdeal P) :
    regularRightGNS P t (scalarWeightGNSEmbedding P A) =
      scalarWeightGNSEmbedding P (scalarRegularRightProduct P t A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightPolar.lean:105` — `cab5601b5e0a1e1ef950638a2025c814488c3f5baa083c14d85028a1ca9d95c9`

```lean
theorem scalarTomitaPolar_conjugate_regular_right (P : SiteProfile) (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor P) (regularRightGNS P t) =
      scalarGNSRepresentation P (star (regularRightCoreElement P t))
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_gns_closedness\20260914_202444_467404\searches.json. Ausência nominal nos recortes não é ausência universal.
