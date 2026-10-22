# Consulta curta — DCT para multiplicadores reais em L² vetorial

[REAL — fornecedores locais lidos; DERIVED — aplicação indicada, sem Lean novo ou build.]

O caminho mais curto localizado é `MeasureTheory.tendsto_integral_of_dominated_convergence` (codomínio escalar ℝ), junto de `TGLV350.Fourier.L2_integral_norm_sq`. Este último já está na árvore própria e é genérico em H complexo completo; seu nome de arquivo Fourier não impõe hipótese Fourier/L¹ ao lema. O precedente `TGLV350.Regular.scalarWeightOrbit_rightRegularization_tendsto` já faz exatamente a passagem DCT → norma² → raiz → Tendsto L², com uma cota 4||f||². Aqui a cota pode ser só ||u||².

Fixe u : RegularHilbert H, g_n e g contínuos, 0≤g_n,g≤1 e convergência pontual g_n(x)→g(x). Use funções ESCALARES explícitas

φ_n(x)=(g_n(x)−g(x))² · ||u(x)||²,   bound(x)=||u(x)||².

Então 0≤φ_n≤bound, φ_n→0 pontualmente e φ_n é AEStronglyMeasurable. O integrável dominante sai diretamente de `(memLp_two_iff_integrable_sq_norm (Lp.memLp u).1).mp (Lp.memLp u)`. Não é necessário que u seja contínuo ou que a constante 1 seja integrável em ℝ. A hipótese de medida finita NÃO é necessária ao DCT escolhido.

Para cada n, `realScalarMultiplier_ae` aplicado a g_n e g, mais `MeasureTheory.Lp.coeFn_sub`, identificam a.e. a diferença dos vetores L² com `(ofReal(g_n−g)) • u`. `norm_smul`, a norma do real embutido em ℂ e `sq_abs` dão, por `integral_congr_ae`,

||realScalarMultiplier g_n ... u − realScalarMultiplier g ... u||² = ∫ x, φ_n(x).

É a identidade `L2_integral_norm_sq` aplicada à diferença, na orientação inversa. Cada n usa apenas os três eventos a.e. correspondentes. Escolher φ_n explicitamente, em vez de usar o representante arbitrário da diferença L² na hipótese pontual do DCT, evita exigir uma nova uniformização dos representantes. Não há interseção a.e. sobre todos u ou sobre índices não enumeráveis.

O DCT escalar com limite zero dá que a integral tende a zero. Compor com `Real.continuous_sqrt` e simplificar `Real.sqrt_sq_eq_abs`, `abs_norm`, `Real.sqrt_zero` fornece a convergência das normas; `tendsto_iff_dist_tendsto_zero` e `dist_eq_norm` concluem a convergência no MESMO L². O trecho já existente de ScalarWeightCompletion, linhas da prova que seguem a identidade de norma², é um molde direto — não há motivo para reconstruir DCT/eLpNorm/toReal.

**Consumidor seno.** Tome m=n+1, g_n(x)=sigmoid(m sin(2πx/m)) e g(x)=sigmoid(2πx). A única nova análise escalar é m sin(a/m)→a; a continuidade da sigmoid dá a convergência acima. O DCT já é genérico e não precisa conhecer seno/sigmoid. A conjugação pela mesma regularSpectralCoordinates é contínua/isométrica, logo leva esse limite ao R_n→R original. Auto-adjunção dos multiplicadores fornece o forte-* sem continuidade forte geral da estrela. Nenhuma norma-operador convergente é afirmada.

**Filtros e alternativas.** A versão sequencial usa ℕ/atTop. `tendsto_integral_filter_of_dominated_convergence` também serve, mas exige `[l.IsCountablyGenerated]`; não a anunciar como DCT de rede arbitrária. `Lp.tendsto_Lp_iff_tendsto_eLpNorm'` aceita filtros arbitrários, porém só CONVERTE uma convergência eLpNorm já demonstrada: não é DCT. `tendsto_Lp_finite_of_tendsto_ae` exige IsFiniteMeasure e UnifIntegrable; não é o atalho adequado para volume em toda ℝ. `fibre_tendsto_of_uniformly_bounded` trata operadores constantes no espaço de base, não um campo g_n(x) variável, e também não substitui esta aplicação.

Nenhuma cobertura do predual, separabilidade de H ou resultado tracial entra. Não foi lida como final a fonte de álgebra enquanto instável. Os tipos abaixo são recortes literais das declarações existentes, não código novo testado. Nas duas declarações DCT, variáveis de seção incluem `{μ : Measure α}`, `[NormedAddCommGroup G] [NormedSpace ℝ G]`; aqui G=ℝ. No lema L² próprio, `[NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]`. No critério de norma² de MemLp, basta `[NormedAddCommGroup F]`.

Data: 2026-09-14T21:03:35.988481-03:00

[tendsto_integral_of_dominated_convergence](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\MeasureTheory\Integral\DominatedConvergence.lean:58>)

```lean
theorem tendsto_integral_of_dominated_convergence {F : ℕ → α → G} {f : α → G} (bound : α → ℝ)
    (F_measurable : ∀ n, AEStronglyMeasurable (F n) μ) (bound_integrable : Integrable bound μ)
    (h_bound : ∀ n, ∀ᵐ a ∂μ, ‖F n a‖ ≤ bound a)
    (h_lim : ∀ᵐ a ∂μ, Tendsto (fun n => F n a) atTop (𝓝 (f a))) :
    Tendsto (fun n => ∫ a, F n a ∂μ) atTop (𝓝 <| ∫ a, f a ∂μ)
```

[tendsto_integral_filter_of_dominated_convergence](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\MeasureTheory\Integral\DominatedConvergence.lean:68>)

```lean
theorem tendsto_integral_filter_of_dominated_convergence {ι} {l : Filter ι} [l.IsCountablyGenerated]
    {F : ι → α → G} {f : α → G} (bound : α → ℝ) (hF_meas : ∀ᶠ n in l, AEStronglyMeasurable (F n) μ)
    (h_bound : ∀ᶠ n in l, ∀ᵐ a ∂μ, ‖F n a‖ ≤ bound a) (bound_integrable : Integrable bound μ)
    (h_lim : ∀ᵐ a ∂μ, Tendsto (fun n => F n a) l (𝓝 (f a))) :
    Tendsto (fun n => ∫ a, F n a ∂μ) l (𝓝 <| ∫ a, f a ∂μ)
```

[memLp_two_iff_integrable_sq_norm](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\MeasureTheory\Function\L2Space.lean:47>)

```lean
theorem memLp_two_iff_integrable_sq_norm {f : α → F} (hf : AEStronglyMeasurable f μ) :
    MemLp f 2 μ ↔ Integrable (fun x => ‖f x‖ ^ 2) μ
```

[memLp](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\MeasureTheory\Function\LpSpace\Basic.lean:183>)

```lean
protected theorem memLp (f : Lp E p μ) : MemLp f p μ
```

[aestronglyMeasurable](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\MeasureTheory\Function\LpSpace\Basic.lean:180>)

```lean
protected theorem aestronglyMeasurable (f : Lp E p μ) : AEStronglyMeasurable f μ
```

[coeFn_sub](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\MeasureTheory\Function\LpSpace\Basic.lean:199>)

```lean
theorem coeFn_sub (f g : Lp E p μ) : ⇑(f - g) =ᵐ[μ] f - g
```

[L2_integral_norm_sq](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350FourierL1L2.lean:56>)

```lean
theorem L2_integral_norm_sq (F : Lp (α
```

[realScalarMultiplier_ae](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350L2PositiveMultiplier.lean:30>)

```lean
theorem realScalarMultiplier_ae (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) (f : RegularHilbert H) :
    realScalarMultiplier g hg h0 h1 f =ᵐ[volume] fun s => (g s : ℂ) • f s
```

[scalarWeightOrbit_rightRegularization_tendsto](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350ScalarWeightCompletion.lean:16>)

```lean
theorem scalarWeightOrbit_rightRegularization_tendsto (P : SiteProfile)
    (A : scalarWeightLeftIdeal P) :
    Tendsto (fun h : ℝ => scalarWeightOrbit P (scalarWeightRightRegularization P A h))
      (𝓝[≠] 0) (𝓝 (scalarWeightOrbit P A))
```

[tendsto_Lp_iff_tendsto_eLpNorm'](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\MeasureTheory\Function\LpSpace\Complete.lean:110>)

```lean
theorem tendsto_Lp_iff_tendsto_eLpNorm' {ι} {fi : Filter ι} [Fact (1 ≤ p)] (f : ι → Lp E p μ)
    (f_lim : Lp E p μ) :
    fi.Tendsto f (𝓝 f_lim) ↔ fi.Tendsto (fun n => eLpNorm (⇑(f n) - ⇑f_lim) p μ) (𝓝 0)
```

[tendsto_Lp_finite_of_tendsto_ae](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\MeasureTheory\Function\UniformIntegrable.lean:519>)

```lean
theorem tendsto_Lp_finite_of_tendsto_ae [IsFiniteMeasure μ] (hp : 1 ≤ p) (hp' : p ≠ ∞)
    {f : ℕ → α → β} {g : α → β} (hf : ∀ n, AEStronglyMeasurable (f n) μ) (hg : MemLp g p μ)
    (hui : UnifIntegrable f p μ) (hfg : ∀ᵐ x ∂μ, Tendsto (fun n => f n x) atTop (𝓝 (g x))) :
    Tendsto (fun n => eLpNorm (f n - g) p μ) atTop (𝓝 0)
```
