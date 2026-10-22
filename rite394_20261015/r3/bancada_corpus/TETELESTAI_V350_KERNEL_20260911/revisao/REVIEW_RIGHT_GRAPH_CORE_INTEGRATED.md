# Revisão integrada — graph-core do F original

2026-09-13T02:18:26.056723-03:00. **PRELIMINAR ESTÁTICO — sem marcador ou veredito integrado final.**

[REAL — inspeção de fontes/bytes/AST] **Sem P0, P1 ou P2 na parte estática concluída.** Build e testes estão pendentes de aviso final do autor; os JSONs vivos de compilação, testes e evidence não foram consumidos nesta rodada.

- Cópia `e0dc36a1c982c01187c58ce5007c7683804a4064ef87b9846f183ea0f8973cc1`, **909 embutidos**. Os seis DEV coincidem com as fontes próprias revisadas e os binários DEV pinados; as seis fontes TGLExt e seus embutidos resultam exclusivamente de `import TGLV350.` → `import TGLExt.V350`. Os demais embutidos permanecem iguais à mãe, exceto as duas raízes com os imports/prints acrescentados.
- Na **fonte** de Audit: **7.039 declarações distintas = 6.982 preservadas +57 do manifesto**, mantendo também as multiplicidades anteriores. Esta contagem não é ainda a auditoria do stream integrado novo.
- AST Python fora do dicionário Lean idêntico ao backup da mãe; `gate_extension.py` idêntico ao pin. Original canônico e cópia-base relidos somente por hash: `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`. Mãe `scalar_vna_custody.json`: `f9f3fc9f6e6592c679daad828b688bc2419d242f7b3b0c8ee6b132ac4520a4ff`. As **34 memórias e os pareceres selados** conferem com os pins maternos.
- Diffs dos scripts: integrador acrescenta seis módulos e batch625→682; compilador os coloca antes das duas raízes; teste acrescenta um grupo de **nove nomes** que exige as seis flags falsas e gate/full-plan preservados. Nenhuma alteração na lógica existente de Audit atual/histórico. A diferença entre flags qgf/gpf e entradas `formal/physics/experiment` do avaliador legado permanece no AST, com `kernel_frontier` anexado depois.
- Os cinco helpers permanecem byte a byte como lidos na revisão DEV. Preparador exige leitura do parecer; recorder exige também revisão integrada; prevê 34 backups imediatos de bytes e append/troca temporária; verifier relê fonte/binário e backup/prefixo. Nenhum deles foi executado pelo revisor. Os artefatos de nova custódia, verificação e relatório integrado autoral estavam ausentes na inspeção.

[Evidência estática e pins](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/right_graph_core_integrated_20260913_021820_613463/static_verification.json>); [fiação do gate por AST](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/right_graph_core_integrated_20260913_021820_613463/gate_wiring.json>); [DEV6/57 preservado](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_RIGHT_GRAPH_CORE_DEV.md>), SHA `93c130aa2924d9c9f3592b4d6572d7125a611d8beb0adc5ebbc5d42b03cd32fc`. Nenhuma execução Lean, teste autoral, monólito, integrador ou recorder nesta revisão integrada. Escritas somente `revisao/`.

**Pendente para o parecer final:** aviso de build/testes concluídos; leitura dos oito logs novos (seis módulos e duas raízes), todos os registros fonte/binário/log/streams e sua herança, mapa Audit corrente contra os 57 próprios e os 6.982 anteriores, hashes de streams/metadados históricos, controles e flags efetivos. **207 registros, 199 herdados+8 novos e 102 controles são expectativas, não resultados aceitos aqui.**

O resultado matemático herdado é a igualdade do fecho do grafo dos pares direitos com o gráfico do **F original no mesmo H_I**. Inclusão inversa dos comutantes pelo J original, reconstrução R=Jπ(b)J, Δ^it/KMS, traço, consumo de certificados e runtime permanecem fora desse resultado. Nenhuma promoção de gate.


---

2026-09-13T02:32:34-03:00 — **RIGHT_GRAPH_CORE_INTEGRATED_REVIEW**

[REAL — inspeção integrada concluída] **Nenhum achado P0, P1 ou P2.** As pendências do estrato preliminar foram resolvidas pela leitura dos artefatos finais. Escopo: seis módulos/57 alvos do DEV preservado, transposição, duas raízes, evidências e helpers. As recompilações independentes são as documentadas no DEV; nesta rodada não houve execução Lean nem de programas autorais.

| Evidência conferida | Resultado | Proveniência |
|---|---|---|
| Embutidos | **909**; seis adições, somente imports reescritos; entre os antigos, apenas duas raízes alteradas | Comparação própria de bytes/AST com a mãe |
| Registros Lean | **207 rc0 = 199 herdados idênticos + 8 novos** (seis módulos + duas raízes) | Compilações autorais; fonte/binário/log/streams relidos pelo revisor |
| Alvos novos | **57**, tipos preservados pela transposição literal e axiomas iguais ao auditor DEV próprio | Fontes, prints integrados e auditor próprio anterior |
| Audit corrente | **7.039 = 6.982 preservados +57**, apenas `propext`, `Classical.choice`, `Quot.sound` | Mapa reparsado do stdout atual, igual ao `axiom_report` |
| Controles | **102/102**, preservados os 101 anteriores e acrescido um grupo | Resultados autorais inspecionados, sem reexecução |
| Memórias | **34 hashes iguais à mãe** | Leitura própria, nenhuma escrita |

Os oito registros novos têm `returncode = lean_returncode = 0`, fonte inalterada durante a compilação, binário pinado, stderr vazio e nenhum warning. Dependências diretas de projeto e frescor foram conferidos. Os 199 herdados mantêm os mesmos registros e hashes de fonte, binário, log e streams. A biblioteca e a cadeia herdada não foram reconstruídas; a evidência própria de tipos/universos e axiomas continua no DEV6/57.

| Fonte/raiz | Log autoral final, relido e pinado |
|---|---|
| TGLExt/V350ComplexGraphProjection.lean | `V350ComplexGraphProjection_20260913_021640_396216.json` |
| TGLExt/V350ScalarRightMultiplicationGraph.lean | `V350ScalarRightMultiplicationGraph_20260913_021708_579440.json` |
| TGLExt/V350HilbertProjectionBlocks.lean | `V350HilbertProjectionBlocks_20260913_021839_153079.json` |
| TGLExt/V350ScalarRightProjectionPair.lean | `V350ScalarRightProjectionPair_20260913_021907_551886.json` |
| TGLExt/V350FixedVectorGraphCore.lean | `V350FixedVectorGraphCore_20260913_022208_915659.json` |
| TGLExt/V350ScalarRightGraphCore.lean | `V350ScalarRightGraphCore_20260913_022223_578439.json` |
| TGLExt.lean | `TGLExt_20260913_022356_796984.json` |
| TGL/Audit.lean | `Audit_20260913_022423_039893.json` |

Audit atual: **891975 bytes**, SHA256 `9d25fc4123d6b8a571f0d424abe3557c9383b002f20f62dfe731a10d8818ab60`; log SHA256 `9e6502c532fdc1ff9fd712139aa50a1c427354a3776c7cd0a8622aee38db7081`. Os dois campos globais `audit_stdout_sha256` e `audit_capture_sha256_full` coincidem com os bytes atuais, sob `CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES`. Os valores de `historical_v350_audit_metadata` permanecem iguais aos da mãe e não foram usados como stream atual. Nomes, axiomas e multiplicidades anteriores foram preservados; o acréscimo é exatamente o manifesto57, incluindo cobertura transitiva dos auxiliares privados.

Controle novo: `right_pair_graph_core_equals_original_F_does_not_discharge_KMS_trace_or_physical_frontier`. Sua lógica exige nove nomes-chave, as seis flags maiores falsas e ausência de promoção do gate/full-plan. AST Python fora do dicionário Lean e `gate_extension.py` permanecem iguais à mãe. `legacy_gate` e `frontier` também são idênticos. O rótulo herdado `PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT` continua referido à torre-produto; não certifica a inclusão inversa pelo J original do peso. As entradas diretas do avaliador legado e o anexo `kernel_frontier` continuam distintos.

Os cinco helpers `make/record_draft/prepare_stage/record_progress/verify_custody` de `right_graph_core` foram lidos estaticamente e seus pins finais reconferidos. O recorder exige leitura dos pareceres, mãe e pins antes dos 34 backups imediatos de bytes, append e troca por temporário; o verifier relê pares fonte/binário e backups/prefixos. Os diffs efetivos do integrador/compilador/teste correspondem às adições previstas. **Isto verifica a lógica prévia à gravação:** nova custódia, verificação e relatório integrado autoral estavam ausentes; nenhuma execução futura desses scripts está certificada aqui.

[REAL — hashes lidos] Cópia `e0dc36a1c982c01187c58ce5007c7683804a4064ef87b9846f183ea0f8973cc1`; original e base `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`; mãe `scalar_vna_custody.json`, `f9f3fc9f6e6592c679daad828b688bc2419d242f7b3b0c8ee6b132ac4520a4ff`. DEV selado e pareceres maternos preservados.

- `integration.json`: `691fcfb22cd802cfd04efbee7efca396e509c58de9222623f641e072acd06d57`.
- `integrated_compile.json`: `1112f536adb47f3de9fd06b3149df708089c36e4047f90e13d439de3843b3a14`.
- `gate_tests.json`: `bcad0bc6448c6e3ed6abb75aa0ee1ee2939139f3e000bb233bed6778e2b23165`.
- `kernel_incremental_evidence.json`: `0d18a617c6f7c820153e90b86a90c7ad1bfce6cef102bb2eb16d23684e38147f`.

[Verificação própria completa](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/right_graph_core_integrated_20260913_021820_613463/verification.json>) — SHA256 `1cc8c71d3378005e4f1425376866c887212dbf4fe754a1c8783c56ace7e4a9a5`: contém os 207 pares, logs, streams, dependências, controles e pins. [Audit reparsado](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/right_graph_core_integrated_20260913_021820_613463/axioms.json>); [57 alvos integrados por módulo](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/right_graph_core_integrated_20260913_021820_613463/new_module_axioms.json>); [auditor DEV reutilizado](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/right_graph_core_integrated_20260913_021820_613463/own_DEV_axioms.json>); [parecer DEV imutável](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_RIGHT_GRAPH_CORE_DEV.md>).

Alcance confirmado pela transposição: **o fecho do grafo dos pares direitos é o gráfico de F original, no mesmo H_I**, com densidade real dos auto-adjuntos em Fix F. Não se afirma igualdade algébrica de domínios, continuidade de F, troca de J ou igualdade I=nν. [OPEN] Reconstrução `R=Jπ(b)J`, inclusão inversa dos comutantes pelo J original, identificação de Δ^it/KMS, traço, consumo das obrigações físicas e runtime não decorrem deste lote. As seis flags e `full_plan_complete` permanecem falsas. **Não resta pendência nesta revisão integrada delimitada.**
