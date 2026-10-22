[REAL — 2 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — O peso limite se anula exatamente no positivo zero

2026-09-14T22:51:59.556579-03:00

Dois teoremas públicos e um auxiliar privado, sem definições. O corte ε=1 coincide com R; sua raiz pertence ao mesmo core. A fidelidade do peso dual implica que o sanduíche se anula. A injetividade e a imagem densa da raiz, consumidas de fornecedores antigos, cancelam os dois lados e forçam X=0. O limite domina esse corte (n=0), portanto scalarInverseLimitWeight é fiel no cone positivo existente, inclusive quando os outros valores são infinitos.

Não foi construída outra raiz, outro GNS ou outra realização. Não se exigiu provar injetividade para cada ε nem finitude do peso em X. Semifinitude, tracialidade e escala dual do limite continuam obrigações distintas; nenhum habitante do contrato final ou mudança de gate é afirmado.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\inverse_limit_faithful_attempts\20260914_224327_939224\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1InverseLimitFaithful']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fidelidade_peso_limite\independent_20260914_224649_553739\run.json`. `682` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351InverseLimitFaithful` | `c8ea383ff05cfee0c3ae5b92e9fffee44c56b0f0c2224eef4cba81ecc398ff99` | `60897208886b53c73af3bcd9e69a3c70b075abda465117cef563a35f1c08e462` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.scalarInverseCutoffWeight_one_faithful (P : TGLExt.SiteProfile)
  (X : TGLV350.Regular.PositiveCoreInput P) :
  Eq.{1} (TGLV350.Regular.scalarInverseCutoffWeight P 1 X) 0 ↔ Eq.{1} X (TGLV350.Regular.PositiveCoreInput.zero P)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseLimitWeight_faithful (P : TGLExt.SiteProfile) (X : TGLV350.Regular.PositiveCoreInput P) :
  Eq.{1} (TGLV350.Regular.scalarInverseLimitWeight P X) 0 ↔ Eq.{1} X (TGLV350.Regular.PositiveCoreInput.zero P)
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_FIDELIDADE_PESO_LIMITE_A1B.json` — SHA256 `8257c147c72d192800f41abde7ccf47cc2f9cb985dd61a051e980696a1daf7da`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fidelidade_peso_limite\REVIEW_A1_INVERSE_LIMIT_FAITHFUL_FINAL.json` — SHA256 `57e6b52e290ac49752f0657475404e006a0008e145aed1739eefa8c40c542724`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fidelidade_peso_limite\compilation.json` — SHA256 `2d9ccc34f5bb5b2e43cc04808017dc4811cecb4ed98c81aac925025aae0e125d`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_INVERSE_LIMIT_FAITHFUL.json` — SHA256 `e005151ee5d5db6e3a0ab79a48e0f9cf17ecfdd5b9e448d2f56f432979812c00`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — fidelidade do peso limite

2026-09-14T22:49:02.815060-03:00

**A1_INVERSE_LIMIT_FAITHFUL_REVIEW_ACCEPTED__SEMIFINITE_TRACIAL_SCALING_OPEN**

[REAL] **Sem achados P0/P1/P2.** Dois teoremas públicos + um helper privado, zero definições. Módulo completo e auditor próprios rc0; dois #check com universos e axiomas exclusivamente do trio permitido. Aceite delimitado ao enunciado efetivamente compilado.

[REAL — alvo e identidade] Dois teoremas públicos, um helper privado e nenhuma definição. A conclusão usa scalarInverseCutoffWeight P 1 e scalarInverseLimitWeight P definidos e aceitos no delta22, com o mesmo PositiveCoreInput P, dualQuadraticIntegral, regularVacuum e regularSpectralResolvent. Não se introduz outro peso, raiz, GNS ou representante do gerador.

[REAL — cancelamento genérico] O helper recebe R positivo e injetivo, X um CLM limitado e a igualdade star sqrt(R) X sqrt(R)=0. positive_sqrt_injective dá injetividade da raiz limitada CFC.sqrt R. resolventSquareRoot_dense tem enunciado em termos do domínio de um operador parcial, mas resolventSquareRoot_domain e sua definição identificam ESSE domínio com a imagem da raiz limitada. Essa redução é efetiva na aplicação a DenseRange, não uma confusão entre os dois operadores. Auto-adjunção elimina a estrela da raiz; sua injetividade fornece X(sqrt(R)v)=0. Continuidade de X e DenseRange.induction estendem a igualdade a todo H. Não se pressupõe inversa limitada, gap, R≤1 ou fidelidade do peso neste helper.

[REAL — corte ε=1] A pertença da raiz ao core é obtida de regularInverseGeneratorCutoff_sqrt_right P 1. Fechamento por produto/estrela e X≥0 fornecem as hipóteses hm/hA exigidas por dualQuadraticIntegral_vacuum_faithful. A anulação do sanduíche é então transportada por B1=R, e os fatos concretos regularSpectralResolvent_nonneg/injective descarregam as premissas do helper. X.val=0 vira X=PositiveCoreInput.zero por extensionalidade do subtipo. Não resta hipótese extra de fidelidade, densidade ou injetividade no tipo público, apenas P e X positivo.

[REAL — limite] O segundo teorema usa scalarInverseCutoffWeight_le_limit P 0 X; ε0=1 exatamente. Se o supremo vale zero, seu termo n=0 também vale zero pela ordem de ENNReal. O primeiro teorema identifica X=0; a recíproca usa a lei zero do delta22. Isso é fidelidade no cone positivo limitado, sem hipótese de valor finito. Não usa minorantes positivos finitos de ν e não necessita provar injetividade de todos os Bε.

[REAL — documentos e proveniência] Ficha 22:40:01 e adendo 22:41:20 foram lidos integralmente; ambos precedem a tentativa22:41:26. Nove fornecedores foram confrontados por nomes, linhas, enunciados e hashes com as cópias próprias. O adendo escolhe explicitamente reusar a dupla injetividade/densidade da raiz existente; a alternativa RXR da consulta não foi implantada. O exemplo denseAntilinearExtension_norm fornece somente o padrão de indução por densidade e não é tomado como teorema de fidelidade.

[REAL — auditoria e histórico] Módulo completo e auditor próprio de dois tipos/axiomas passaram. O helper privado é lido e compilado, coberto transitivamente pelos dois alvos; não se emite print privado separado. Não há sorry, axioma novo, native_decide, trustCompiler ou hipótese de conclusão. As duas tentativas DEV foram rc0: a primeira tinha exatamente dois avisos de aliases depreciados, substituídos na final pelos nomes mul_apply_eq_comp e zero_apply. A primeira não é evidência da fonte final, e nenhum objeto DEV foi utilizado. O negativo autoral troca X=0 por X≠0 no bicondicional e falha por Type mismatch; fonte/streams foram relidos e pinados, sem reexecutá-lo.

[REAL — proveniência] 682 objetos próprios anteriores preservados; somente módulo e auditor novos, total 684. Zero fornecedor antigo recompilado; cache de pacotes pinado e herdado, sem nova auditoria integral da biblioteca. LEAN_PATH dos traces contém somente V e seus pacotes, nenhum build autoral ou DEV. Run próprio rc0 em 34.371 s; zero avisos do alvo/auditor e 178 mensagens históricas de fornecedores separadas no JSON. O stderr preserva ainda o aviso do cache aesop com alterações locais, já presente na base; não é aviso do alvo. A contagem total de jobs do Lake não significa recompilação dessa quantidade de objetos.

| Artefato | SHA256 lido |
|---|---|
| Fonte final (K=cópia própria) | c8ea383ff05cfee0c3ae5b92e9fffee44c56b0f0c2224eef4cba81ecc398ff99 |
| .olean próprio | 60897208886b53c73af3bcd9e69a3c70b075abda465117cef563a35f1c08e462 |
| .olean autoral standalone, apenas comparação | 60897208886b53c73af3bcd9e69a3c70b075abda465117cef563a35f1c08e462 |

Igualdade binária medida: True.

[OPEN — limites] Aceite separado de dois teoremas públicos e um helper privado; zero definições. Fidelidade paga para o candidato scalarInverseLimitWeight no cone positivo limitado do mesmo core, sem afirmar isomorfismo do predual/cone estendido. Semifinitude, tracialidade e escala dual do candidato permanecem OPEN neste delta; nenhum habitante completo de RegularCoreTraceData ou quitação de A1(b) é declarado. A aceitação do delta22 e de todos os anteriores foi preservada por pins; suas contagens vêm dos artefatos lidos, não de uma base presumida. Somente objetos próprios anteriores e cache de pacotes pinado; nenhum objeto autoral/DEV, monólito, recorder, writer ou memória executado/modificado.

Artefatos de evidência:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fidelidade_peso_limite\compilation.json>) — SHA256 2d9ccc34f5bb5b2e43cc04808017dc4811cecb4ed98c81aac925025aae0e125d.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fidelidade_peso_limite\independent_20260914_224649_553739\run.json>) — SHA256 c2d9f47faddf08b41388986def6984f9253346c0139ccf3c97c0bbc29803ab1a.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fidelidade_peso_limite\independent_20260914_224649_553739\type_axiom_audit.json>) — SHA256 fdadc75643f21d978e144c18acacb7723fe54d5a321bbf05801ec74909a5ab5a.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fidelidade_peso_limite\history_read.json>) — SHA256 0ed35a9b687b07a1b047e93afff504dde7f6fc672df217b3bfa8cefa3ef649cd.
- [fornecedores da ficha](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fidelidade_peso_limite\provider_checks.json>) — SHA256 a36184cfdd0fcac26203c6b5fe9b15d8750e15176544848b6615dc3ad237a646.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_FIDELIDADE_PESO_LIMITE

[OPEN — ficha anterior à fidelidade do peso limite]

# A1(b): um corte já basta para a fidelidade do limite

2026-09-14T22:40:01.259796-03:00

Prove scalarInverseCutoffWeight P 1 faithful on PositiveCoreInput P using B_1=R, membership of the existing sqrt(R) in N and faithfulness of the SAME vacuum dual weight. The ORIGINAL positive_sqrt_injective and resolventSquareRoot_dense imply injectivity and dense range of the bounded CFC root; adapt the wrapper only. If star sqrt(R) X sqrt(R)=0, injectivity cancels the left root and continuity/dense range cancels the right root, giving X=0. Then scalarInverseLimitWeight dominates n=0 (epsilon_0=1), so it is faithful. No new GNS/root/resolvent and no need to prove every regulator inverse injective. Consumer: faithful field of RegularCoreTraceData for the candidate value. Neither semifinitude, traciality nor dual scaling follows from this.

ADAPTAR: o domínio do fornecedor resolventSquareRoot_dense é a imagem da raiz LIMITADA CFC.sqrt R. Não confundir essa raiz com o operador parcial resolventSquareRoot. A dupla injetividade/densidade é reutilizada; não é pressuposta a fidelidade do limite.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventSquareRoot.lean:13` — `6a1ad3a2fa7041aa45d56b2448e18a5fce6b90e9e069f045df89483ecb1e3f90`

```lean
theorem positive_sqrt_injective (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) : Function.Injective (CFC.sqrt R : H →L[ℂ] H)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventSquareRoot.lean:47` — `6a1ad3a2fa7041aa45d56b2448e18a5fce6b90e9e069f045df89483ecb1e3f90`

```lean
theorem resolventSquareRoot_dense (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) : Dense ((resolventSquareRoot R hR hi).domain : Set H)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarDualWeightFaithfulness.lean:54` — `3ff3e31e49de71f035a425202ef1796be18da2b46bdb60a7f6c34b8a2e73f61c`

```lean
theorem dualQuadraticIntegral_vacuum_faithful (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hm : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A) :
    dualQuadraticIntegral A (regularVacuum P) = 0 ↔ A = 0
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:98` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
theorem regularSpectralResolvent_injective (P : SiteProfile) :
    Function.Injective (regularSpectralResolvent P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:84` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
theorem regularSpectralResolvent_nonneg (P : SiteProfile) :
    0 ≤ regularSpectralResolvent P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:43` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_one (P : SiteProfile) :
    regularInverseGeneratorCutoff P 1 = regularSpectralResolvent P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:125` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_sqrt_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),h⟩ :
        (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:94` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
theorem scalarInverseCutoffWeight_le_limit (P : SiteProfile) (n : ℕ) (X : PositiveCoreInput P) :
    scalarInverseCutoffWeight P (1/((n : ℝ)+1)) X ≤ scalarInverseLimitWeight P X
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:90` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
theorem scalarInverseLimitWeight_zero (P : SiteProfile) :
    scalarInverseLimitWeight P (PositiveCoreInput.zero P) = 0
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_limit_weight_faithful\20260914_223938_431313\searches.json. Ausência nominal nos recortes não é ausência universal.


## Ficha/adendo integral: ADENDO_FICHA_FIDELIDADE_ROTA

[OPEN — escolha da rota antes do código]

2026-09-14T22:41:20.742727-03:00

Consulta lida antes do código: basta ε=1; a alternativa RXR=0 é válida. Reusar diretamente positive_sqrt_injective e resolventSquareRoot_dense, que já fornecem injetividade/imagem densa da raiz limitada. Não acrescentar teorema de densidade novo. Um auxiliar genérico apenas cancela os dois lados usando essas propriedades e a auto-adjunção da mesma raiz. O exemplo antigo denseAntilinearExtension_norm mostra a forma da indução de DenseRange; consultar o corpo não o transforma em prova de fidelidade. Escala dual será outro alvo.
