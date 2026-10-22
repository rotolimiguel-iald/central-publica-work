[OPEN — ficha anterior à identificação das potências do mesmo gerador regular]

# A1(b): as potências existentes geram Λ_t

2026-09-14T19:28:18.315946-03:00

For every SiteProfile P,t and x on the actual regular Hilbert space: resolventImaginaryPower (regularSpectralResolvent P), with its already proved positive contraction and injectivity certificates, maps x exactly to regularUnitary P t x. Prove from CFC on the sigmoid multiplier, damping density, existing resolvent intertwining, Fourier and absorption. Do not define a replacement imaginary-power group equal to Lambda by decree. Affiliation, dual scaling and trace remain distinct obligations.

A identificação usa exatamente resolventImaginaryPower e regularSpectralResolvent. Não há novo grupo definido como Λ_t; o grafo fechado anterior é h=(1−R)/R. Os módulos predecessores permanecem intactos.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarMultiplierCalculus.lean:73` — `4dfa6cbd81aa481d695c2eec89985eb06487e7ba32432528d06c62ee7147f06c`

```lean
theorem realScalarMultiplier_cfc_ae (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ x, 0 ≤ g x) (h1 : ∀ x, g x ≤ 1)
    (f : ℂ → ℂ) (hf : Continuous f) (u : RegularHilbert H) :
    cfc f (realScalarMultiplier g hg h0 h1) u =ᵐ[volume]
      fun x => f (g x : ℂ) • u x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryPowers.lean:38` — `0cfc297376410ff6bd259eeaf921a9d6e6ca47829b5d389c6b5c30bf4c5accf5`

```lean
def resolventImaginaryPower (t : ℝ) : H ≃ₗᵢ[ℂ] H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryPowers.lean:45` — `0cfc297376410ff6bd259eeaf921a9d6e6ca47829b5d389c6b5c30bf4c5accf5`

```lean
theorem resolventImaginaryPower_damping (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1 hi hj t (resolventDampingOperator T x)=
      resolventPhaseOperator T t x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryPowers.lean:20` — `0cfc297376410ff6bd259eeaf921a9d6e6ca47829b5d389c6b5c30bf4c5accf5`

```lean
theorem resolventDampingOperator_denseRange : DenseRange (resolventDampingOperator T)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryIntertwining.lean:64` — `789f68095379e02a203191b258c359787c12b24c1282f34d39835dc5347c76d5`

```lean
theorem resolventImaginaryPower_intertwines (T Q R : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1T : T ≤ 1) (hiT : Function.Injective T)
    (hjT : Function.Injective (1-T : H →L[ℂ] H))
    (hQ : 0 ≤ Q) (h1Q : Q ≤ 1) (hiQ : Function.Injective Q)
    (hjQ : Function.Injective (1-Q : H →L[ℂ] H)) (h : T*R=R*Q)
    (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1T hiT hjT t (R x) =
      R (resolventImaginaryPower Q hQ h1Q hiQ hjQ t x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventPhaseCalculus.lean:18` — `cd207e3a21c50f65fe3b199e201b2b148a0d98fc2e3a3cf7e40a80e61ba4f818`

```lean
theorem resolventDampingOperator_cfc (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) :
    cfc (fun z : ℂ => (resolventDamping z.re : ℂ)) T = resolventDampingOperator T
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351FourierTranslation.lean:47` — `a0fe8f689855aebeefcc6d1d1a7ece3314bf5dcd65d74017569597dd7df1a9b2`

```lean
theorem fourier_shift (t : ℝ) (f : RegularHilbert H) :
    Lp.fourierTransformₗᵢ ℝ H (shift t f) =
      characterMultiplier (2 * Real.pi * t) (Lp.fourierTransformₗᵢ ℝ H f)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularFlowAbsorption.lean:60` — `4760792d98c8d625e9109bd7d0b2a97713bd236dcb7d6db1a4f07251cdc0c9f9`

```lean
theorem regularUnitary_shift_conjugate (P : SiteProfile) (t : ℝ) :
    (regularFlowAbsorptionUnitary P).val * shift t *
        star (regularFlowAbsorptionUnitary P).val = regularUnitary P t
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:78` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularSpectralResolvent (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
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

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2CharacterMultiplier.lean:98` — `2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3`

```lean
theorem characterMultiplier_ae (s : ℝ) (f : RegularHilbert H) :
    characterMultiplier s f =ᵐ[volume]
      fun x : ℝ => Complex.exp (-Complex.I * (s : ℂ) * (x : ℂ)) • f x
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_regular_powers\20260914_192752_671120\searches.json. Ausência nominal nos recortes não é ausência universal.
