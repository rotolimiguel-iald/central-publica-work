# Continuidade forte uniformemente limitada — amplificação em L²

[REAL — Lean, bancada local] `kernel/TGLV350/L2BoundedStrongContinuity.lean` compilado com exit 0.
Namespace `TGLV350.Regular`; importação direta `TGLV350.L2StrongContinuity`.
H é um espaço de Hilbert complexo completo, com as mesmas hipóteses da base:
`H : Type`, `NormedAddCommGroup H`, `InnerProductSpace ℂ H`, `CompleteSpace H`.
`RegularHilbert H` é `MeasureTheory.Lp H 2 (volume : Measure ℝ)`.

[REAL — enunciados compilados]

| Nome | Enunciado |
|---|---|
| `fibre_norm_le` | Para T operador limitado em H, `‖fibre T‖ ≤ ‖T‖`. |
| `fibre_apply_norm_le` | Para f em L², `‖fibre T f‖ ≤ ‖T‖ * ‖f‖`. |
| `fibre_lipschitz_of_norm_le` | Se `‖T‖ ≤ C`, `fibre T` é Lipschitz com constante não negativa `max C 0`. |
| `fibre_bounded_jointly_continuous` | Para qualquer espaço topológico Z, se `∀ z, ‖T z‖ ≤ C` e `∀ v, Continuous (fun z => T z v)`, então `(f,z) ↦ fibre (T z) f` é contínua. |
| `fibre_bounded_strongly_continuous` | Sob as mesmas hipóteses, para cada f em L², `z ↦ fibre (T z) f` é contínua. |
| `fibre_tendsto_of_uniformly_bounded` | Para qualquer `ι : Type*`, filtro `l : Filter ι`, operadores `T : ι → (H →L[ℂ] H)` e `S : H →L[ℂ] H`, se `∀ i, ‖T i‖ ≤ C` e `∀ v, Tendsto (fun i => T i v) l (𝓝 (S v))`, então `∀ f, Tendsto (fun i => fibre (T i) f) l (𝓝 (fibre S f))`. |

A hipótese de continuidade/convergência do parâmetro é pontual em cada vetor de H, isto é, forte.
Não se exige continuidade nem convergência em norma de operador. O índice dos limites não precisa
de topologia, estrutura de sequência ou primeira enumerabilidade. O limite S já é um operador
linear contínuo, mas não se assume separadamente uma cota para `‖S‖`.
O limite uniforme C é real; `max C 0` evita impor uma hipótese extra de positividade,
inclusive no caso de índice vazio.

[REAL — método]

1. `ContinuousLinearMap.norm_compLpL_le` fornece o controle uniforme da amplificação.
2. Indicadores de conjuntos de medida finita são transportados por `fibre_indicatorConst`;
   `indicatorConst_continuous` transfere a continuidade ou convergência dos valores em H.
3. `Lp.simpleFunc.induction` estende aos elementos simples por adição.
4. A continuidade conjunta segue de `Lp.simpleFunc.dense` e
   `continuous_prod_of_dense_continuous_lipschitzWith`.
5. Para filtros gerais, o controle de Lipschitz implica equicontinuidade;
   `Equicontinuous.isClosed_setOf_tendsto` e `Lp.simpleFunc.denseRange` estendem a
   convergência dos elementos simples a todo L².

[REAL — evidência]

- Comando: `C:\Python314\python.exe compile_lean.py TGLV350/L2BoundedStrongContinuity.lean`.
- Registro: `logs/L2BoundedStrongContinuity_20260911_211710_826211.json`.
- Stdout: `logs/L2BoundedStrongContinuity_20260911_211710_826211.stdout.txt`.
- Stderr vazio, exit 0, sem erros ou avisos no stdout.
- 6/6 declarações auditadas com `#print axioms`, exclusivamente `propext`, `Classical.choice`, `Quot.sound`.
- Sem `sorry`, `axiom` ou `admit` na fonte.
- SHA-256 da fonte: `afc18b6b9c10d8427ef5f5750ae612b22cae485950e7577b6122273b9bf0f5dc`.
- SHA-256 do .olean: `2ba4fb3cf1cf79e6c70eda4d35f0623b74330b13c24feecf96652a8d11b440f1`.
- Fonte e .olean atuais conferidos contra o registro de compilação.
- Fonte da dependência `L2StrongContinuity.lean` conferida contra seu registro exit 0.
- Fonte e .olean de `L2CharacterMultiplier` permanecem com os hashes da entrega anterior.

[OPEN — fora desta subtarefa] A passagem desses lemas para normalidade da representação,
integração nas raízes/monólito e revisão independente cabe à tarefa principal.
Esta entrega não afirma normalidade de *-homomorfismo e não altera o gate.
As escritas desta subtarefa se limitam ao novo módulo, ao seu build/logs de compilação e a esta nota.
