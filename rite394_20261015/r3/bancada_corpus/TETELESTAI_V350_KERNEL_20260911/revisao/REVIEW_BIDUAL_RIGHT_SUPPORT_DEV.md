# Revisão DEV — bidual original e suporte direito

## Estrato parcial — 2026-09-13T04:24:58.751950-03:00

[REAL — leitura integral e recompilação independente.] Escopo concluído neste estrato: somente `ScalarTomitaBidual.lean`, dois alvos. Nenhum P0–P2 matemático identificado. Não constitui aceite cumulativo dos nove alvos.

- `scalarClosedTomita_bidual_maximal` (linha 49): um pareamento contra TODO D(F) produz pertinência ao D(S) original e o valor S y=z.
- `scalarClosedTomita_bidual_graph_iff` (linha 63): equivalência exata entre esse pareamento e o grafo original, incluindo a direção fornecida pelo pareamento de F.

Os auxiliares privados `bidualPairingTransfer` e `bidualMaximalFromTransport` foram lidos e são cobertos transitivamente pelos axiomas dos alvos. `antiunitary_inner_conj` não exige involutividade; `antiunitary_pairing_flip` a exige e recebe `scalarTomitaPolarFactor_involutive P`. A prova transporta o teste por J, aplica maximalidade já estabelecida de F e retorna por J²=I. As hipóteses genéricas de domínio, valor e maximalidade são descarregadas na aplicação concreta. Não há novo S, F ou J nem hipótese de bidualidade usada para provar a própria conclusão.

| Reprodução própria | rc | segundos |
|---|---:|---:|
| ScalarTomitaBidual | 0 | 29.081 |
| Auditor separado `#check` com universos + `#print axioms` dos dois | 0 | 24.071 |

Os dois alvos retornaram exatamente `propext`, `Classical.choice`, `Quot.sound`; binário próprio idêntico ao final autoral. Fonte SHA256 `7aaece20ddf3f9a2b197e0ef92319a7d5be7a49543e79123c22e057932f179b9`; .olean `b0947b675d0aa3f8b2e782106632f173d51b1dcb0b7ad6d13adc0a9c531e375c`; log final `ScalarTomitaBidual_20260913_040447_744548.json`, SHA `1bda6c68e1951face940b59a5d5473275e8eb9f80040823ea78dcb2ab539061c`.

Evidência: `revisao\bidual_partial_independent_20260913_041717_226833/manifest.json` e `compilation.json` (SHA `c7f5bf50a604bfdf5349ceca7685a1729979bdabfb2c7b86c42812dcb0bed5cb`). Foram congeladas 426 dependências de projeto provenientes exclusivamente de árvores próprias anteriores, com origem individual no manifesto; oito pacotes externos readonly e 11 pins diretos herdados, sem rebuild dos pacotes. LEAN_PATH não contém build autoral. Herança principal: `phase_variational_final_independent_20260913_034807_811147` e `adjoint_polar_first_independent_20260913_025326_236836`.

A tentativa autoral `_040333_134788` é rc1 e contém `sorryAx`: rejeitada integralmente, preservada em `author_history`. A primeira preparação própria falhou ao procurar um registro novo de uma dependência herdada; nenhum Lean foi iniciado nessa tentativa. Registro próprio de falha e backup do script foram preservados; a execução aceita é a indicada acima.

[OPEN] Segundo módulo/auditor cumulativo e reconciliação documental ainda pendentes neste estrato. Não houve integração, execução de monólito/recorders, escrita em memórias ou alteração de pareceres custodiados. Inversa dos comutantes, cortes racionais, quadrados como núcleo de gráfico, KMS e traço não são conclusões destes dois alvos.


## Adendo cumulativo final — 2026-09-13T04:26:31.352689-03:00

BIDUAL_RIGHT_SUPPORT_DEV_REVIEW

[REAL — DEV revisto e recompilado independentemente.] Escopo final: dois módulos, nove alvos exatos (2+7). **Nenhum P0 ou P1; nenhum P2 pendente.** O erro documental de nomes de flags está registrado abaixo como corrigido. Não há revisão integrada nem promoção de gate.

**Segundo módulo, leitura integral.** `ScalarRightFunctionalStability.lean:21` extrai comutação de T com TODA π(N) da pertinência ao comutante concreto. Linhas 40 e 62 constroem o par e o elemento de E para T a com hipóteses expressas a*=a, T*=T, T∈M′ e Ta=aT. T não é presumido em E. Ambos os vetores são T j(a); a ordem do produto/adjunto é justificada por `adjoint_comp`, auto-adjunticidade e comutação. Linhas 68 e 77 provam auto-adjunticidade e a inscrição exata pela unicidade já existente. Não há novo produto, norma, representação ou vetor por homonímia.

Linhas 87 e 100 demonstram suporte em `closure (Set.range R)` para QUALQUER par direito, sem hipótese de auto-adjunticidade ou injetividade de R. O filtro é `𝓝[>] 0` em ℝ, não vazio; a prova restringe o limite existente, usa h>0 para inserir a média no ideal finito e então em nν, e aplica fechamento à igualdade RΛ(e_h)=π(e_h)v. Não assume I=nν, continuidade pontual de L², continuidade limitada de S/F, nem cota uniforme de Λ(e_h).

**Reprodução própria.** O primeiro módulo e seu auditor2 são herdados do estrato acima, sem repetir compilação. O segundo módulo rc0 em 163.144 s; auditor separado9 rc0 em 24.94 s. Auditor imprime todos os tipos com universos e axiomas; conjunto exatamente igual aos nove alvos do manifesto e aos outputs finais autorais. Axiomas exclusivamente `propext`, `Classical.choice`, `Quot.sound`, incluindo transitivamente dois auxiliares privados do primeiro módulo e três do segundo. Ambos os .olean próprios são idênticos aos finais autorais.

| Fonte | SHA256 fonte DEV | SHA256 .olean próprio = autor |
|---|---|---|
| ScalarTomitaBidual | `7aaece20ddf3f9a2b197e0ef92319a7d5be7a49543e79123c22e057932f179b9` | `b0947b675d0aa3f8b2e782106632f173d51b1dcb0b7ad6d13adc0a9c531e375c` |
| ScalarRightFunctionalStability | `4fe83c09767c53a903ad0abeaee648ad4838ea8731c612314cb8c8eeb89c421e` | `4f4826a24b9cd7b2b0ba4719325a8370576af2ed1759698b20be49022cef473b` |

Evidências próprias finais: `revisao\bidual_support_final_independent_20260913_042239_895782/manifest.json`, `compilation.json` (SHA `a912f836f339e66b0128ceeb6cd58dbb53fe81844c8bb59fee3b645a18e07798`), `logs/BidualSupportAudit9.stdout.txt` (SHA `2fce58c395c22968bb8ba143c06edf426546a45630e58aa15efe75ea1dd2bb93`). O manifesto identifica cada origem de dependência e pin anterior. A árvore final contém 444 dependências próprias: as 426 do estrato inicial e 18 adicionais do catálogo próprio `adjoint_polar_graph_final_independent_20260913_025725_898901`; 419 são alcançadas pelos imports do segundo módulo. Nenhuma dependência antiga foi recompilada; pacotes externos continuam readonly, oito caminhos e 11 pins diretos herdados. A biblioteca inteira não foi reauditoria binária nesta rodada.

**Histórico excluído.** Duas tentativas autorais rc1: Bidual `_040333_134788`, erro de conversão do produto interno conjugado; Stability `_040725_588950`, identificador de centralizador, elaboração/timeout e filtro, com erros derivados. Seus prints com `sorryAx` não contam. Há também preparação própria final recusada por catálogo incompleto (antes do Lean) e uma execução de 1,017 s recusada por busca de módulo numa raiz parcial. Os registros foram preservados. A correção reuniu somente binários próprios já pinados numa única raiz de projeto; nenhuma Lean fonte foi corrigida pelo revisor. O catálogo inicial também teve a falha anterior já descrita no estrato parcial.

**Metadados — P2 documental encerrado.** O manifesto inicial continha `real_bidual_right_support_solution_unique` e `original_S_bidual_right_support_constructed`, decorrentes de substituição de nomes do estágio anterior. Esses nomes não evidenciam seleção variacional nova. A correção foi anunciada e feita pelo autor; conferi por bytes os backups imediatos e a substituição literal dos dois campos no manifesto, draft recorder, progress recorder e verifier, além do ajuste de ordem no gerador. Nomes finais: `original_S_is_maximal_adjoint_of_F`, `selfadjoint_right_pairs_stable_under_commuting_multipliers` e `right_pair_vectors_in_multiplier_range_closure`. Diferenças/pins em `metadata_correction_inspection.json`; scripts apenas parseados/lidos no delta, nunca executados. Isto não equivale a revisão integral de futuros helpers de integração.

Manifesto corrente SHA `5b773ee3eb8fb5cd0bfe7426ba4d65cb82ed2b244ab4def2664d2f72e70b5dc7`; relatório autoral integral SHA `16dd3ff011aab524f967f91bc0bf66fbb1717ef685dd0240e57c3e51e8ed33d1`; mãe `phase_variational_custody.json` SHA `49ee6ee4981f189562e67f2d4b5de5ad83860f20f0858cb53b58bf9f5aaa4a76`. Fonte/binário/log/streams dos dois conferem o manifesto atual; relatório e provas permaneceram intactos na correção. A mãe e sua verificação foram lidas/pinadas, sem repetir auditoria das 34 memórias. Cópia integrada anterior e gate_extension mantiveram os pins; as seis flags da mãe seguem falsas. O DEV não está integrado.

**Alvos próprios auditados (2+7):**

- `TGLV350.Regular.scalarClosedTomita_bidual_maximal`
- `TGLV350.Regular.scalarClosedTomita_bidual_graph_iff`
- `TGLV350.Regular.scalarGNSCommutant_commutes`
- `TGLV350.Regular.scalarSelfadjointRightPairMultiplier`
- `TGLV350.Regular.scalarSelfadjointRightMultiplier`
- `TGLV350.Regular.scalarSelfadjointRightMultiplier_star`
- `TGLV350.Regular.scalarSelfadjointRightMultiplier_vector`
- `TGLV350.Regular.scalarRightAdjointPair_vector_mem_range_closure`
- `TGLV350.Regular.scalarRightPairVector_mem_range_closure`

[OPEN] Não se concluem ainda limite racional no suporte, densidade de combinações de quadrados no gráfico, pertinência automática de pares ponderados a D(S), cota de multiplicador, inclusão inversa pelo J original, identificação de Δ^it/KMS, traço ou quitação de flags. A bidualidade é uma equivalência exata de pareamento/grafo no H_I original, sem redefinir o operador; a estabilidade é condicional às hipóteses explícitas de T. Não resta análise DEV necessária para estes nove alvos e documentos delimitados. Não foram executados monólito, integrador, testes autorais, recorders ou escrita de memórias.
