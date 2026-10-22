[OPEN — ficha anterior à afiliação do mesmo gerador regular]

# A1(b): o resolvente pertence ao core

2026-09-14T19:37:20.302875-03:00

Prove on the existing regular space: regularSpectralResolvent P belongs to regularCoreAlgebra P; every B in its commutant preserves the graph of the already constructed positive generator. Reuse local pairings from character commutation, conjugation by V=W F^-1 and the double commutant. No simple-function approximation machinery, new affiliated-form object or replacement generator. This is the commutant criterion of affiliation of the closed operator; dual scaling and trace remain separate.

A prova usa character_commutation_local_pairing antes de tentar reconstruir funções simples. O critério de afiliação é a preservação do grafo por todo operador do comutante. O grafo anterior é mantido intacto; não se confunde com as formas afiliadas de outro contrato.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350CharacterLocality.lean:40` — `7a5d2f1b70b3d61307045c4460034e3821976c8b30b02d5bcf165d157f33419a`

```lean
theorem character_commutation_local_pairing
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hB : ∀ s : ℝ, characterMultiplier s * B = B * characterMultiplier s)
    (f g : RegularHilbert H) :
    (fun x : ℝ => inner ℂ ((B.adjoint f) x) (g x)) =ᵐ[volume]
      (fun x : ℝ => inner ℂ (f x) ((B g) x))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2PositiveMultiplier.lean:30` — `6e3946aff9964e1a6a59a8dcb99a11b4a3c0026a6b0220f7df4b9901f83f3bdf`

```lean
theorem realScalarMultiplier_ae (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) (f : RegularHilbert H) :
    realScalarMultiplier g hg h0 h1 f =ᵐ[volume] fun s => (g s : ℂ) • f s
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularImaginaryPowers.lean:65` — `066b9cb14426365807ead587ca90ad28e3703a0f9efc0ce359519da7c5243b9a`

```lean
theorem regularSpectralCoordinates_character (P : SiteProfile) (t : ℝ)
    (u : RegularHilbert (TowerHilbert P)) :
    regularSpectralCoordinates P (characterMultiplier (2*Real.pi*t) u) =
      regularUnitary P t (regularSpectralCoordinates P u)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:78` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularSpectralResolvent (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventGraph.lean:20` — `3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b`

```lean
theorem resolvent_graph_equation (R : H →L[ℂ] H) (hi : Function.Injective R) (x y : H) :
    (x,y) ∈ (resolventGraphOperator R hi).graph ↔ (1-R) x = R y
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularGeneratedAlgebra.lean:57` — `252b0fa3d5e37c42827efccfc26a555db80ac5c20a6f94269060ce2b3dcb5f71`

```lean
theorem regularUnitary_mem (P : SiteProfile) (t : ℝ) :
    regularUnitary P t ∈ regularCoreAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\VonNeumannAlgebra\Basic.lean:133` — `bd6c64fbead6d030dbcc311533319d9da1a35ca16b12956979cd523dfb763a86`

```lean
theorem mem_commutant_iff {S : VonNeumannAlgebra H} {z : H →L[ℂ] H} :
    z ∈ S.commutant ↔ ∀ g ∈ S, g * z = z * g
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\VonNeumannAlgebra\Basic.lean:139` — `bd6c64fbead6d030dbcc311533319d9da1a35ca16b12956979cd523dfb763a86`

```lean
theorem commutant_commutant (S : VonNeumannAlgebra H) : S.commutant.commutant = S
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_regular_affiliation\20260914_193659_398254\searches.json. Ausência nominal nos recortes não é ausência universal.
