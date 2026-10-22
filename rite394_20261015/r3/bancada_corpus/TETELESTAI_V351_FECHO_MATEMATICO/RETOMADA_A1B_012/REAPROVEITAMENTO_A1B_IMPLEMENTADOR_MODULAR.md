[OPEN — ficha anterior à igualdade dos implementadores modulares]

2026-09-15T01:04:16.845321-03:00

ADAPTAR: prove on ALL vectors of the SAME scalar GNS that U_t equals pi(lambda_t) R_{-t}. Use actual fixed vectors Lambda(z_delta), z_delta=e_delta* e_delta (star(e_delta)*e_delta), from delta31, plus existing all-core covariance. Prove the same W_t fixes Lambda(z_delta) by the actual left/right product identities and z_delta commutation with regular unitaries. That commutation reuses StrongIntegral.operatorIntegral_commutes, not the inaccessible private proof of delta29. Transfer the existing contraction strong/strong-star approximation z_delta to pi(z_delta), then conjugate by original J to obtain rho(z_delta) -> I strongly. Right identity gives rho(z_delta)Lambda(a)=pi(a)Lambda(z_delta), so limits plus dense original Lambda(n_nu) prove totality and equality. No premise of single-vector cyclicity, no inference of implementator identity from covariance alone. No new operator definition or general integration/CFC framework. One public theorem, local or private adapters only where type transport requires. Delta31 standalone underway when fiche created; final delivery depends on independent acceptance. Consumer tracial field remains INDIRECT: later half-power/Q domain compatibility still required, not furnished merely by this implementation identity. Same h, Delta_nu, nu, tau, GNS; never identify h=Delta_nu.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ModularFixedVectors.lean:94` — `53ccbe3b65e326c618e0c4a4864571b5ab318b31b6f0843b1e91273082a05ff0`

```lean
theorem regularAverage_square_modular_fixed (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    ∃ A : scalarWeightStarCore P,
      A.val.val = star (regularAverage P δ)*regularAverage P δ ∧
      ∀ t : ℝ, scalarTomitaImaginaryPower P t (scalarWeightStarEmbedding P A) =
        scalarWeightStarEmbedding P A
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarImaginaryCoreAction.lean:47` — `db4109dceeab1e948d7d5e664e8d76b347c719b00e62031761aaf5e924862a83`

```lean
theorem scalarTomitaImaginaryPower_core_conjugation (P : SiteProfile) (t : ℝ)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (scalarGNSRepresentation P A x) =
      scalarGNSRepresentation P
        (regularRightCoreElement P t * A * star (regularRightCoreElement P t))
          (scalarTomitaImaginaryPower P t x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularPolarCommutation.lean:13` — `1c238b53abf26177ed621f2daf98383b9e14a6e0d97cc85ac98cc995ee4dfb70`

```lean
theorem regularRightGNS_commutes_left (P : SiteProfile) (t : ℝ)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute (regularRightGNS P t) (scalarGNSRepresentation P B)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularPolarCommutation.lean:50` — `1c238b53abf26177ed621f2daf98383b9e14a6e0d97cc85ac98cc995ee4dfb70`

```lean
theorem scalarTomitaPolar_regular_generator (P : SiteProfile) (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P (regularRightCoreElement P t)) =
        regularRightGNS P (-t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightGNS.lean:98` — `92ac2b64b81b6389a2900ddd63dceabcc2f150a05bab59ce8e903352a7fa12fa`

```lean
theorem regularRightGNS_intertwines (P : SiteProfile) (t : ℝ) (A : scalarWeightLeftIdeal P) :
    regularRightGNS P t (scalarWeightGNSEmbedding P A) =
      scalarWeightGNSEmbedding P (scalarRegularRightProduct P t A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorIntegral.lean:59` — `7ee0e23dc3319a72734ce420f540251f59a27561fa61221d6ab5f98b2989dfa7`

```lean
theorem operatorIntegral_commutes (F : Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ContractionAdjointLimit.lean:51` — `75c191ec2110441b6554ca7beddfc7806f3e3aac6e879e8461f7632cfa78eaa5`

```lean
theorem regularAverage_star_tendsto_identity (P : TGLExt.SiteProfile)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    Tendsto (fun h : ℝ => star (regularAverage P h) v) (𝓝[≠] 0) (𝓝 v)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightAction.lean:54` — `7875ce91559689c1e951f28d3a1d005dc17aae2af1db677242a27d38e40dfb5c`

```lean
theorem scalarWeightGNSEmbedding_denseRange (P : SiteProfile) :
    DenseRange (scalarWeightGNSEmbedding P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightAction.lean:38` — `7875ce91559689c1e951f28d3a1d005dc17aae2af1db677242a27d38e40dfb5c`

```lean
theorem scalarWeightGNSAction_intertwines (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (A : scalarWeightLeftIdeal P) :
    scalarGNSRepresentation P B (scalarWeightGNSEmbedding P A) =
      scalarWeightGNSEmbedding P (scalarWeightLeftProduct P B A)
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

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:14` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
def ScalarPolarRight (P : SiteProfile) (b : (regularCoreAlgebra P).toStarSubalgebra) : Prop
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongBoundedApplication.lean:15` — `dd68e70d90c4c475bfbe1770df5428666fd9345ed28b81c2addfef16f56017a0`

```lean
theorem bounded_application_tendsto {ι : Type*} (l : Filter ι)
    (A : ι → H →L[ℂ] H) (C : ℝ) (hbound : ∀ i, ‖A i‖ ≤ C)
    (v : ι → H) (v₀ w : H) (hv : Tendsto v l (𝓝 v₀))
    (hfixed : Tendsto (fun i => A i v₀) l (𝓝 w)) :
    Tendsto (fun i => A i (v i)) l (𝓝 w)
```

Buscas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_modular_implementation\20260915_010352_101732\searches.json. Ausência nominal não é ausência universal. Consulta2 V2 relida; consumidores futuros Q/meias potências/tracialidade continuam abertos. A fonte StrongIntegral.operatorIntegral_commutes foi lida integralmente antes de propor a adaptação; usar esse fornecedor evita reproduzir integração vetorial.
