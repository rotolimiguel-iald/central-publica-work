# A1 — parecer independente final do marco parcial

2026-09-14T08:22:06.509232-03:00

**[REAL — recompilação e auditoria próprias] Nenhum achado P0–P2 pendente no candidato delimitado. Aceitos (a) e (c); (b) permanece NÃO PAGO. A1 e a ORDEM_011 não estão concluídas.** O [parecer preliminar](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/REVIEW_A1_CONTRATO_PRELIMINAR.md>) permanece intacto; este documento atualiza somente o estatuto do candidato final e da evidência agora disponível.

| Critério A1 | Conclusão independente |
|---|---|
| **a — contrato forte e recusa do zero legado** | **PAGO_KERNEL neste módulo.** `RegularCoreTraceData` e `legacy_zero_trace_cannot_supply` foram conferidos e recompilados. Isto não altera automaticamente o contrato legado ou seus consumidores. |
| **b — habitante concreto para todo P, ou impossibilidade de existência** | **NÃO PAGO.** Nenhum habitante foi construído; nenhuma impossibilidade de existência foi provada. Recusar zero e recusar renomear ν como τ não paga esta alternativa. |
| **c — axiomas permitidos** | **PAGO_KERNEL_AUDIT neste módulo.** Onze declarações — quatro definições auxiliares, uma estrutura e seis teoremas — conferidas por `#check` com universos e `#print axioms` próprios; somente `propext`, `Classical.choice`, `Quot.sound`. |

**Matemática e tipos.** Referência: [fonte final](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351RegularCoreTraceContract.lean>), linhas 15–120.

- Linhas 15–28 e 43–60: valor ENNReal no **mesmo cone positivo do core regular**, ação dual existente, ordem de operadores, soma e escala NNReal; normalidade de supremos internos de redes positivas crescentes, dirigidas e não vazias, com universo de índices explícito. Não é apenas normalidade sequencial e não recebe convergência SOT como premissa. Semifinitude é a igualdade com o supremo de **todos** os minorantes positivos de valor finito; densidade de um ideal não a substitui por definição. A lei tracial compara τ(a*a) com τ(aa*), e o sinal dual é e⁻ˢ.
- Linhas 30–37 e 62–77: unidade não nula demonstrada pelo vácuo de norma 1; fidelidade recusa o valor zero mesmo após qualquer transporte do fornecedor legado. A combinação fidelidade/semifinitude também impede a degeneração “infinito em todo positivo não nulo”. Isto não demonstra inhabitância do contrato. Não se exige τ(1) finito.
- Linhas 80–108: o peso existente ν é dual-invariante e vale **exatamente 1** no quadrado da média de comprimento 1, no mesmo vácuo. Se fosse o valor de um T escalado, teríamos 1=e⁻¹. Prova válida de incompatibilidade desse fornecedor, sem conversão de infinito em real, sem alegar impossibilidade de construir outro traço.

**Evidência própria e herança.** [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/a1_independent_20260914_081736_089694/compilation.json>) e [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/a1_independent_20260914_081736_089694/verification.json>).

- Candidato recompilado **rc0**, sem warnings, em 27.504s; `.olean` próprio **idêntico byte a byte** ao autoral. Auditor separado com onze tipos/universos, onze listas de axiomas e impressão dos campos da estrutura: **rc0**, sem warnings, em 21.035s. As saídas brutas estão na mesma pasta.
- As **375 dependências de projeto** foram copiadas para a árvore própria após comparar fonte, objeto e objeto de origem com `DEPENDENCIAS_A1.json`; pins preservados ao terminar. São **binários herdados** da construção anterior do autor, não 375 recompilações independentes. O LEAN_PATH de projeto aponta apenas à cópia congelada em `revisao/`; bibliotecas externas foram usadas somente para leitura, conforme o run aceito. Não reconstruí Mathlib ou o corpus anterior.
- Histórico próprio preservado: uma checagem preparatória excessiva exigiu um diretório opcional `Cli`; outra tentativa usou dois diretórios para o mesmo prefixo `TGLExt`, causando sombreamento. Corrigida a preparação, o módulo passou. A primeira saída do auditor já era verde, mas o pós-processamento recusou sufixos de universos como `Classical.choice.{u}`; parser normalizado e auditor reexecutado com registro explícito de rc0. Nenhum desses incidentes foi imputado à prova ou apagado.

**Auditoria autoral e controle negativo.** Li [AUDITORIA_A1.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/AUDITORIA_A1.json>), os streams e snapshots dos seis runs registrados e a versão final de [audit_a1.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/audit_a1.py>).

- O run aceito é `20260914_081118_098129`, com fonte idêntica ao candidato. O rc0 anterior `080951_993951` pertence a outro pin e não foi usado como aceite final. Os rc1 `080121` (preparação) e `080332` (elaboração/sintaxe, com `sorryAx`) ficam excluídos.
- O probe `081310_479904` altera o valor 1 para 2; sua fonte/snapshot/hash foram conferidos. O Lean retorna rc1 por incompatibilidade do alvo no `change` e erro derivado, com `sorryAx` nas provas afetadas. A tentativa anterior `081233_145150` falhou pelo root e **não conta como recusa matemática**. Não recompilei o probe: esta evidência é autoral relida.
- Os **oito controles** autorais foram confrontados e reproduzidos em memória, extraindo por AST somente a função pura `check`, sem executar o escritor do script. Rc não zero, entrada ausente, axioma desconhecido, duplicação e a saída do falso valor são recusados. Todos coincidem com PASS. O parser autoral basta para os onze nomes e formato desta saída; não o certifico como parser universal de logs Lean.
- A alteração de reexecução preserva `AUDITORIA_A1.json` existente e destina novas emissões a `audits/audit_<data>.json` por temporário. Não executei esse escritor nem declarei novo registro autoral. O script não fornece por si um pin completo do binário final: a comparação independente acima fecha essa verificação **para este candidato**, sem certificar futuras execuções.

**Lacuna restante, sem expansão de escopo.** [LACUNAS_A1.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/LACUNAS_A1.md>) distingue corretamente ausência de fornecedor de impossibilidade. Falta um termo `RegularCoreTraceData P` para todo P, ligado à perturbação canônica do ν fixado e à ação do mesmo core; a lei de escala isolada não seleciona normalização. A rota descrita ainda precisa das identificações de peso/grupo modular, gerador afiliado e perturbação com suas leis de normalidade e semifinitude. É obrigação de existência/ligação, não razão para reprovar (a)/(c). O fecho do grafo do peso completo com o **S original** já é fornecido por `TGLV350.Regular.scalarClosedTomita_graph_eq_weight`, em `V350ScalarWeightTomitaIdentification.lean`; não é exigido novamente, nem se presume igualdade dos ideais algébricos. A futura adaptação ao consumidor legado do core/ThreeLocks permanece fora deste marco.

**Pins lidos por script:**

| Artefato | SHA-256 |
|---|---|
| Fonte final | `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0` |
| `.olean` autoral = próprio | `057225cc3d7aace6ff789cb7dce81b0209b054bcc938584b0763250e6aeecb56` |
| `AUDITORIA_A1.json` | `4ac68cd343edd3aa1d27cefff660c9e8fb37ba5a9c0894fa09a9dc465f8acd3c` |
| `audit_a1.py` final | `9d43c2b9c708d5ba03f25aacbbe5c51cd95fc0c09908fa0d11b05d6b0e9ec4ea` |
| `LACUNAS_A1.md` | `bafdb810542d83dde5dc0fe6f1bc8722c0147aa923c1edbcb28372a879bdfa92` |
| Compilação independente | `2dcf853e8f0d0f0cb766338878f3ba56a16db4a7e99c1dff5cc8507bbc8fd592` |
| Verificação independente | `a2b1d7a177a05d49e8693dbb0fc3a682467c83117a1373e5fae4c0499f01bdd8` |
| Cópia `um.py` preservada | `95e8cf8eb0b33c5d65e244195021b71977cca1a91836ef0d314964a8e2f97c43` |

Somente `revisao/` recebeu saídas. Não houve implementação autoral, integração, execução/importação de `um.py`, promoção de gate, atualização de memórias/Atlas ou alteração de pareceres anteriores. Não há análise pendente deste candidato; **o marco parcial a/c está aceito e b continua aberto**.
