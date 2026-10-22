[REAL — 1 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — As médias existentes recuperam todos os valores quadráticos do peso

2026-09-14T22:04:55.818547-03:00

Um teorema, sem definições ou helpers privados. Para todo A no core original, ν(A*A) é o supremo dos valores ν((Ae_n)*(Ae_n)), com e_n=regularAverage P (1/(n+1)). A igualdade aceita valores infinitos e não recebe hipótese A∈nν. Fatou para a sequência de integrandos ENNReal, incluindo o mesmo fator de Haar, fornece a desigualdade inferior; a cota de médias existente fornece a superior. A pertença de Ae_n ao ideal finito é fornecida pelos lemas antigos, não reprovada.

Não se afirma monotonia da sequência, Ae_n abaixo de A, ou (Ae_n)*(Ae_n)≤A*A. A igualdade é de valores. A aplicação aos pesos dos cortes requer ainda a comutação entre as médias e os cortes/raízes; limite tracial e habitante final não são produzidos aqui. Nenhuma mudança de gate.

## Critérios

| Critério | Resultado |
|---|---|
| Ficha anterior e consumidor nomeado | PAGO; fichas integrais anexas, fornecedores pinados. |
| Mesmos espaços e fornecedores | PAGO no alcance dos tipos abaixo; fontes antigas preservadas. |
| Lake isolado e tipos completos | PAGO; autor e revisor rc0, sem herança de objetos DEV. |
| Axiomas | PAGO; somente propext, Classical.choice e Quot.sound, ou subconjuntos. |
| Adulteração | PAGO; controles autorais recusados por TypeMismatch; alcance e eventual leitura do revisor discriminados em seu parecer. |
| Revisão distinta da autoria | PAGO; nenhuma pendência P0/P1/P2 no delta. |
| Habitante do contrato do traço | NÃO PAGO por esta entrega. |
| Incorporação ao um.py / mudança de gate | NÃO EXECUTADA; escopo da gerência. |

## Reprodução

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\weight_average_recovery_attempts\20260914_215916_138194\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1WeightAverageRecovery']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_recuperacao_medias\independent_20260914_220028_858888\run.json`. `672` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351WeightAverageRecovery` | `a72b71ac86bb0b2a5c81d5bfaba3c6ad964bf4a8beffd0a9df89f7ee26391fac` | `306d98e971c8d9a20ff11deb84ad33978a89bf32de07d985ea47a956678d38ec` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.scalarWeight_square_eq_iSup_averages (P : TGLExt.SiteProfile)
  (A : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P))) :
  Eq.{1}
    (TGLV350.Regular.dualQuadraticIntegral (HMul.hMul.{0, 0, 0} (star.{0} ↑A) ↑A) (TGLV350.Regular.regularVacuum P))
    (⨆ n,
      TGLV350.Regular.dualQuadraticIntegral
        (HMul.hMul.{0, 0, 0}
          (star.{0}
            (HMul.hMul.{0, 0, 0} (↑A)
              (TGLV350.Regular.regularAverage P (HDiv.hDiv.{0, 0, 0} 1 (HAdd.hAdd.{0, 0, 0} (↑n) 1)))))
          (HMul.hMul.{0, 0, 0} (↑A)
            (TGLV350.Regular.regularAverage P (HDiv.hDiv.{0, 0, 0} 1 (HAdd.hAdd.{0, 0, 0} (↑n) 1)))))
        (TGLV350.Regular.regularVacuum P))
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_RECUPERACAO_MEDIAS_A1B.json` — SHA256 `840f7ff79c5384ad70acbec4f0111682de62fb24d31e2f08f93defe7f4a86b10`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_recuperacao_medias\REVIEW_A1_WEIGHT_AVERAGE_RECOVERY_FINAL.json` — SHA256 `72c28ec7a1d4954d5f26afe3fc1a43090b4eb6a0b89868af86d1d6f349cfa018`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_recuperacao_medias\compilation.json` — SHA256 `40d39606c66fedf7130413a4f56bd5b1b918bc237fd0753e4273c45173bca783`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_WEIGHT_AVERAGE_RECOVERY.json` — SHA256 `52d12fe78515216b9afb1bee575c2322c3f80b1f180908616a4e2be0e183d37a`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — recuperação do peso pelas médias

2026-09-14T22:03:43.054862-03:00

**A1_WEIGHT_AVERAGE_RECOVERY_REVIEW_ACCEPTED__CUTOFF_COMMUTATION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2: **1 teorema público, 0 definições/helpers privados**. Fonte inteiro relido, módulo e auditor próprios rc0; #check completo com universos e #print axioms: somente propext, Classical.choice e Quot.sound.

[REAL — tipo e domínio] scalarWeight_square_eq_iSup_averages recebe somente P e A no core N. Não recebe HasFiniteScalarSquare, MemLp, finitude da integral, monotonicidade das amostras ou hipótese sobre seus minorantes. O resultado é uma igualdade em ENNReal para o mesmo dualQuadraticIntegral, regularVacuum, dualAmbient e regularAverage P (1/(n+1)), incluindo ν(A*A)=∞.

[REAL — limite e Haar] A sequência d_n=1/(n+1) converge a zero na vizinhança perfurada, com d_n≠0 provado. A convergência pontual da órbita existente passa a norma-quadrado e ofReal. O fator fixo ofReal dualHaarFactor permanece dentro de f_n e g; continuous_const_mul usa explicitamente ofReal_ne_top. Isso exige finitude da CONSTANTE, não finitude da integral. dualQuadraticIntegrand_star_mul liga exatamente as avaliações quadráticas às normas. Measurabilidade e lintegral_const_mul recuperam a normalização original.

[REAL — duas desigualdades] Fatou para a sequência atTop dá integral(g)≤liminf integral(f_n); a cota por iSup de todos os termos fecha esse sentido. No sentido oposto, iSup_le aplica scalarWeight_right_average_le a cada d_n, cujo fornecedor vale para todo A∈N. Não há DCT com integrabilidade escondida, rede arbitrária exigida por Fatou, ordenação das amostras, ou comparação (Ae_n)*(Ae_n)≤A*A em ordem de operadores.

[REAL — ficha, história e negativo] A ficha anterior ao código foi relida, com nove fornecedores pinados; a consulta é identificada como roteiro, não prova. Os dois DEV rc1 efetivamente encontrados são 215633_172434 e 215716_269572, ambos excluídos. O DEV 215753_855426 rc0 tem um aviso de change inútil; a remoção exata de uma linha (40 bytes) foi medida entre seu snapshot histórico e a fonte final reproduzida. Pins antigos apontam aos snapshots reais, nunca ao caminho vivo com hash antigo. A auditoria autoral final rc0 foi conferida; substituir o supremo por um único corte produz Type mismatch com imports resolvidos. Esse negativo não foi reexecutado e não demonstra que igualdade num corte seja impossível em casos especiais.

[REAL — proveniência] 672 objetos anteriores do Lake próprio preservados; acrescentados apenas módulo e auditor (total 674). Nenhum fornecedor antigo recompilado, nenhum objeto autoral/DEV herdado. Pacotes externos: cache pinado da reprodução anterior, sem nova auditoria integral. Run próprio rc0 em 34.624 s; zero avisos do alvo/auditor. 178 mensagens históricas de fornecedores constam no JSON. LEAN_PATH dos traces contém apenas V e seus pacotes.

| Artefato | SHA256 lido |
|---|---|
| Fonte final | `a72b71ac86bb0b2a5c81d5bfaba3c6ad964bf4a8beffd0a9df89f7ee26391fac` |
| .olean próprio | `306d98e971c8d9a20ff11deb84ad33978a89bf32de07d985ea47a956678d38ec` |
| .olean cold autoral (comparação somente) | `306d98e971c8d9a20ff11deb84ad33978a89bf32de07d985ea47a956678d38ec` |
| Snapshot DEV anterior ao ajuste do linter | `a13db1e1d1cfcc902d660156b6aa47ff405805e63b06d5ceff159ad6741c58d8` |

Igualdade binária do alvo final medida: True.

[OPEN — limites] Há recuperação dos valores quadráticos para todo A∈N, inclusive ∞. A finitude dos quadrados regularizados é fornecedor anterior, não premissa desta prova nem novo alvo. Comutação dos cortes com as mesmas médias e a extensão correspondente da ordem dos pesos dos cortes ainda são obrigações posteriores. Tracialidade/A1(b) permanecem abertos; não se usa a propriedade falsa de minorantes positivos finitos de ν. Sem novas consultas, testes extra, monólito, recorder, escrita autoral ou alteração de memória/gate.

Artefatos próprios:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_recuperacao_medias\compilation.json>) — SHA256 `40d39606c66fedf7130413a4f56bd5b1b918bc237fd0753e4273c45173bca783`.
- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_recuperacao_medias\independent_20260914_220028_858888\run.json>) — SHA256 `74f0ef759cfabc4051d145f145f6c2521ce246bd5f7216a5877f074ed34d8bad`.
- [tipos e axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_recuperacao_medias\independent_20260914_220028_858888\type_axiom_audit.json>) — SHA256 `7111aa61f06873fe52b06f3b31dc899d0e772c4d71c45be72eae8d2c5ac46c23`.
- [histórico/diff](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_recuperacao_medias\history_read.json>) — SHA256 `9a20a699bca7fe6a8b44941830ff40315b088f05698df1619fd4ac7abcfa0a17`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_RECUPERACAO_PELAS_MEDIAS

[OPEN — ficha anterior à recuperação de valores estendidos por médias]

# A1(b): recuperar todos os valores sem supor minorantes finitos

2026-09-14T21:55:44.270084-03:00

For EVERY A in regularCoreAlgebra P, prove nu(A*A)=iSup_n nu((A e_n)*(A e_n)), e_n=regularAverage P (1/(n+1)). No finite-weight hypothesis on A; values may be infinity. Consume pointwise orbit convergence and the existing upper bound under right averages, via Fatou for a SEQUENCE atTop. No monotonicity of e_n or of its squares asserted. A e_n is already uniformly square-finite by existing ideal lemmas. Consumer: extend the cut-weight order from square-finite inputs to all positive inputs, after proving commutation of cuts with the SAME averages. This does not claim finite positive minorants or normal-weight semifiniteness in that stronger sense.

ADAPTAR: limite pontual e cota já pagos, compostos com Fatou. Reutilizar a família regularAverage, sem novo regularizador ou novo peso. Consulta independente TODOS_POSITIVOS é roteiro, não prova.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRightAverage.lean:70` — `64d49e1de18504e9e66e7559f48df9f6811c80821524b85324ee0a1305793aed`

```lean
theorem scalarWeight_right_average_le (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (h : ℝ) :
    dualQuadraticIntegral (star (A.val * regularAverage P h) * (A.val * regularAverage P h))
      (regularVacuum P) ≤ dualQuadraticIntegral (star A.val * A.val) (regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRightAverage.lean:63` — `64d49e1de18504e9e66e7559f48df9f6811c80821524b85324ee0a1305793aed`

```lean
theorem scalarOrbit_right_average_tendsto (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (s : ℝ) :
    Tendsto (fun h : ℝ => dualAmbient s (A.val * regularAverage P h) (regularVacuum P))
      (𝓝[≠] 0) (𝓝 (dualAmbient s A.val (regularVacuum P)))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualSemifiniteIdeal.lean:108` — `63c88763eaa1c837ed0a28057d044a7627e57f993f4fcc4c7bddf44dcea07cbe`

```lean
theorem regularAverage_hasFiniteDualSquare (P : TGLExt.SiteProfile)
    (h : ℝ) (hh : 0 < h) : HasFiniteDualSquare (regularAverage P h)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualSemifiniteIdeal.lean:51` — `63c88763eaa1c837ed0a28057d044a7627e57f993f4fcc4c7bddf44dcea07cbe`

```lean
theorem HasFiniteDualSquare.left_mul
    (B A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : HasFiniteDualSquare A) :
    HasFiniteDualSquare (B*A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualWeightForm.lean:62` — `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4`

```lean
def dualQuadraticIntegral (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (v : RegularHilbert H) : ℝ≥0∞
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualWeightForm.lean:47` — `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4`

```lean
theorem dualQuadraticIntegrand_measurable
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    Measurable (dualQuadraticIntegrand A v)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularFiniteWeight.lean:95` — `39e417e41adf90a2d575b6a93f8a35ccd2d816a445097745fd3c540ab240baf6`

```lean
theorem dualQuadraticIntegrand_star_mul
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) (s : ℝ) :
    dualQuadraticIntegrand (star A * A) v s =
      ENNReal.ofReal (‖dualAmbient s A v‖ ^ 2)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\MeasureTheory\Integral\Lebesgue\Add.lean:231` — `e330b98eb9686290a3257802c38ad756150b110deb39fe32c66da46cf1211e4f`

```lean
theorem lintegral_liminf_le {ι : Type*} {f : ι → α → ℝ≥0∞} {u : Filter ι}
    [IsCountablyGenerated u] (h_meas : ∀ i, Measurable (f i)) :
    ∫⁻ a, liminf (fun i => f i a) u ∂μ ≤ liminf (fun i => ∫⁻ a, f i a ∂μ) u
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecificLimits\Basic.lean:69` — `dbbeb301e5b9dacc96ecd233fd05a02846a1fc88c9606f1b1d413d08aff5142e`

```lean
theorem tendsto_one_div_add_atTop_nhds_zero_nat {𝕜 : Type*} [DivisionSemiring 𝕜] [CharZero 𝕜]
    [TopologicalSpace 𝕜] [ContinuousSMul ℚ≥0 𝕜] :
    Tendsto (fun n : ℕ ↦ 1 / ((n : 𝕜) + 1)) atTop (𝓝 0)
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_weight_average_recovery\20260914_215512_951496\searches.json. Ausência nominal nos recortes não é ausência universal.
