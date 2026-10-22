[OPEN — ficha anterior à ligação Fourier/translação no L² existente]

# A1(b): fase espectral da translação regular

2026-09-14T18:31:33.320389-03:00

Consumidor: LACUNAS_A1.md:31, regular_unitary_positive_generator, seguindo ROTA_GERADOR_REGULAR_A1B.

```text
forall t : Real, forall f : RegularHilbert H, Lp.fourierTransformₗᵢ Real H (shift t f) = characterMultiplier (2 * Real.pi * t) (Lp.fourierTransformₗᵢ Real H f)
```

ADAPTAR. O sinal é o da casa: S_t f(x)=f(x−t), Fourier usa exp(−2πixξ), characterPhase(s,ξ)=exp(−isξ); s=2πt. Usar a Fourier L² da mathlib e a extensão densa de Schwartz. O fornecedor L1/L2 existente é uma alternativa; não refazer Plancherel. Lemas auxiliares só os consumidos pela igualdade acima. Nenhum novo espaço, Fourier, gerador ou traço.

## Fornecedores

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2Translation.lean:19` — `1fc45298e186caf37d2b04779e64f3e000e7384511bede3bdce57ab9b429b267`

```lean
theorem shift_ae (t : ℝ) (f : RegularHilbert H) :
    shift t f =ᵐ[volume] fun x : ℝ => f (x-t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2CharacterMultiplier.lean:98` — `2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3`

```lean
theorem characterMultiplier_ae (s : ℝ) (f : RegularHilbert H) :
    characterMultiplier s f =ᵐ[volume]
      fun x : ℝ => Complex.exp (-Complex.I * (s : ℂ) * (x : ℂ)) • f x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350FourierL1L2.lean:26` — `49c8e43b55cbd48b3a2c9f1bdfa01a31af9566e7a3cccbb4eed119fc1c750f13`

```lean
theorem fourier_integral_ae_eq_L2 (f : ℝ → H) (hf1 : Integrable f) (hf2 : MemLp f 2) :
    (𝓕 f) =ᵐ[volume] (𝓕 (hf2.toLp f) : Lp (α
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\Fourier\LpSpace.lean:50` — `82b647b1998edea8d60ac8f986fd5735d697044e586464a05d71d0a346522cfe`

```lean
def fourierTransformₗᵢ : (Lp (α
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\Fourier\LpSpace.lean:99` — `82b647b1998edea8d60ac8f986fd5735d697044e586464a05d71d0a346522cfe`

```lean
theorem SchwartzMap.toLp_fourier_eq (f : 𝓢(E, F)) : 𝓕 (f.toLp 2) = (𝓕 f).toLp 2
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\Distribution\SchwartzSpace\Basic.lean:1068` — `21568645b0fdb30aa8c2ba91ba49a89ba481d2f049eda4250bc4c59dd07fd300`

```lean
def compSubConstCLM (a : E) : 𝓢(E, F) →L[𝕜] 𝓢(E, F)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\Fourier\FourierTransform.lean:107` — `96d179f52654504228b5f536ed5076fbe33f2e1ddd333bfda576c7ffef88324a`

```lean
theorem fourierIntegral_comp_add_right [MeasurableAdd V] (e : AddChar 𝕜 𝕊) (μ : Measure V)
    [μ.IsAddRightInvariant] (L : V →ₗ[𝕜] W →ₗ[𝕜] 𝕜) (f : V → E) (v₀ : V) :
    fourierIntegral e μ L (f ∘ fun v ↦ v + v₀) =
      fun w ↦ e (L v₀ w) • fourierIntegral e μ L f w
```

## Busca e aceitação

Seis modalidades e outras bancadas registradas em C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_fourier_translation\20260914_183104_029467\searches.json. Os resultados identificam fornecedores, não uma prova de ausência em todo computador. Cada saída foi preservada, inclusive eventual erro de acesso; a ficha só é escrita se as sete leituras terminarem sem erro. A aceitação requer Lake isolado, axiomas, negativo com sinal trocado e revisão distinta. Até lá, desenvolvimento somente.
