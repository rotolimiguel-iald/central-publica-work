[REAL — antecedente localizado, com diferença de tipo explícita]

# A1(b): reaproveitamento da construção escalar 049–050

2026-09-14T18:47:50.379044-03:00

A leitura do cabeçalho de BoundedGraphOperator levou às fontes ContinuousModular*. Elas já contêm o multiplicador exponencial positivo, domínio denso e autoadjunção. Contudo SpectralHilbert é fixado a Lp ℂ 2 volume. O alvo desta retomada tem fibra TowerHilbert P. A identificação entre espaços e suas representações não vem do nome nem de uma isometria abstrata.

Decisão: adaptar a positividade ao multiplicador vetorial que a casa já tem. Consumir o resolventGraphOperator genérico para construir e provar as propriedades do grafo, sem repetir essas provas. A construção escalar não é reescrita. A identificação espectral, afiliação e escala do novo grafo continuam obrigações posteriores.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\ContinuousModularMultipliers.lean:52` — `494be0d93285c97abece403bc5503c5207b10ba430df4bb965db4bba8d814f21`

```lean
abbrev SpectralHilbert := Lp ℂ 2 (volume : Measure ℝ)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\ContinuousModularResolvent.lean:59` — `4b25b03984382f826607325e228e286cc254143c6ec1d9a43d6c2e31b166d2dc`

```lean
theorem bounded_spectral_multiplier_nonneg (w : ℝ → ℝ) (hw : Continuous w)
    (hb : ∀ x, ‖w x‖ ≤ 1) (hn : ∀ x, 0 ≤ w x) :
    0 ≤ boundedSpectralMultiplier w hw hb
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\ContinuousModularDomain.lean:46` — `fbb043925f4a05859b335d0d7180e0037eb7f4cb969210288baf38fe59db6c0e`

```lean
def continuousModularOperator (c : ℝ) : SpectralHilbert →ₗ.[ℂ] SpectralHilbert
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\ContinuousModularDomain.lean:69` — `fbb043925f4a05859b335d0d7180e0037eb7f4cb969210288baf38fe59db6c0e`

```lean
theorem continuous_modular_graph_iff (c : ℝ) (f g : SpectralHilbert) :
    (f,g) ∈ (continuousModularOperator c).graph ↔
      g =ᵐ[volume] fun x => (Real.exp (-c * x) : ℂ) * f x
```

