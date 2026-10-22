[OPEN — ficha anterior à escala dual do mesmo gerador regular]

# A1(b): transformação do domínio e do grafo

2026-09-14T19:53:41.130187-03:00

Prove dual scaling of the SAME existing closed regular positive generator h: (x,y) in graph h iff (C_s x, exp(s) C_s y) in graph h, equivalently theta_s(h)=exp(-s)h with theta_s=Ad(C_s). Reuse V=W F^-1, the exact spectral graph e^(-2pi xi), operatorFieldLift and Fourier translation. Add inverse Fourier translation and Fourier modulation only as consumed lemmas; do not create another Fourier transform, group, generator or affiliated object. Domain transformation must be proved, not just formal exponentials. The inverse-generator trace is separate.

A convenção C_s(x)=exp(-isx) dá F C_s = S_(-s/(2pi)) F. Portanto h C_s=exp(s) C_s h e Ad(C_s)h=exp(-s)h. O sinal será conferido pela identidade de grafos e por controle adulterado. Nenhum traço é definido nesta etapa.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351FourierTranslation.lean:14` — `a0fe8f689855aebeefcc6d1d1a7ece3314bf5dcd65d74017569597dd7df1a9b2`

```lean
theorem shift_schwartz_toLp (t : ℝ) (f : 𝓢(ℝ, H)) :
    shift t (f.toLp 2) = (f.compSubConstCLM ℂ t).toLp 2
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351FourierTranslation.lean:26` — `a0fe8f689855aebeefcc6d1d1a7ece3314bf5dcd65d74017569597dd7df1a9b2`

```lean
theorem fourier_shift_schwartz (t : ℝ) (f : 𝓢(ℝ, H)) :
    𝓕 (shift t (f.toLp 2)) =
      characterMultiplier (2 * Real.pi * t) (𝓕 (f.toLp 2))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\Fourier\FourierTransform.lean:475` — `96d179f52654504228b5f536ed5076fbe33f2e1ddd333bfda576c7ffef88324a`

```lean
lemma fourierInv_eq_fourier_neg (f : V → E) (w : V) :
    𝓕⁻ f w = 𝓕 f (-w)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\Fourier\LpSpace.lean:111` — `82b647b1998edea8d60ac8f986fd5735d697044e586464a05d71d0a346522cfe`

```lean
theorem SchwartzMap.toLp_fourierInv_eq (f : 𝓢(E, F)) : 𝓕⁻ (f.toLp 2) = (𝓕⁻ f).toLp 2
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2CharacterMultiplier.lean:98` — `2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3`

```lean
theorem characterMultiplier_ae (s : ℝ) (f : RegularHilbert H) :
    characterMultiplier s f =ᵐ[volume]
      fun x : ℝ => Complex.exp (-Complex.I * (s : ℂ) * (x : ℂ)) • f x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2CharacterMultiplier.lean:124` — `2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3`

```lean
theorem characterMultiplier_inverse (s : ℝ) (f : RegularHilbert H) :
    characterMultiplier s (characterMultiplier (-s) f) = f
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorField.lean:68` — `83fcc9ee4e6cdecee9f130183b7d1e6a0e2436caf40670e4d64dce8933f86a4c`

```lean
theorem operatorFieldLift_ae (F : StrongIntegral.Family (H := H)) (f : RegularHilbert H) :
    operatorFieldLift F f =ᵐ[volume] fun x : ℝ => F.op x (f x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:72` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularSpectralCoordinates (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) ≃ₗᵢ[ℂ] RegularHilbert (TowerHilbert P)
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

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_regular_dual_scaling\20260914_195057_334158\searches.json. Ausência nominal nos recortes não é ausência universal.
