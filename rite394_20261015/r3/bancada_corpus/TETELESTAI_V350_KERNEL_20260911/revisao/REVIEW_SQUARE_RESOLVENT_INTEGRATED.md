# Revisão integrada — resolventes, quadrados e teste do S original

2026-09-13T06:20:21-03:00 — **SQUARE_RESOLVENT_INTEGRATED_REVIEW**

**[REAL] Sem achados P0–P2 no delta integrado de três módulos/20 alvos.** Inspeção e cinco recompilações próprias concluídas, com a herança binária delimitada abaixo. O [parecer DEV20](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_SQUARE_RESOLVENT_DEV.md>) permanece byte a byte, SHA256 `1f22c91229e42c079ebc5ba36d0dd7843ce4aa2a0f47c12d97f0baecb11ba02c`.

## Evidência própria e evidência autoral

As fontes integradas são exatamente os bytes DEV, com a única substituição `import TGLV350.` → `import TGLExt.V350`. Preservam os nomes, tipos e hipóteses conferidos no auditor DEV20. As raízes acrescentam somente os três imports e os 20 pedidos de axiomas; nenhuma declaração anterior foi retirada ou teve sua multiplicidade reduzida.

**[REAL — execução própria]** Executei Lean diretamente em árvore isolada de `revisao/`, sobre cópias dos três módulos integrados e das duas raízes. Todos os cinco binários resultantes são byte a byte iguais aos binários autorais finais.

| Módulo | rc | Segundos | Declarações impressas distintas | Binário |
|---|---:|---:|---:|---|
| TGLExt.V350SquareResolventSupport | 0 | 29.784 | 6 | igual |
| TGLExt.V350ScalarRightSquareApproximation | 0 | 316.286 | 9 | igual |
| TGLExt.V350ScalarSquareAdjointTest | 0 | 323.289 | 5 | igual |
| TGLExt | 0 | 24.033 | 0 | igual |
| TGL.Audit | 0 | 31.325 | 7106 | igual |

O Audit próprio contém exatamente **7106 declarações distintas**, todas com axiomas contidos em `propext`, `Classical.choice`, `Quot.sound`. Seu mapa coincide com o stream autoral corrente e com `axiom_report`; os **7086 alvos anteriores** permanecem iguais, e os **20 novos** coincidem com o manifesto e o auditor DEV próprio.

**Limitação de proveniência:** esta não foi uma reconstrução independente integral das dependências. A árvore congelou **897 módulos herdados**: 307 do cache próprio previamente pinado, 205 binários integrados da custódia mãe e 385 binários da base canônica, lidos e copiados sem alteração. Os 385 fontes adicionais conferem com o manifesto formal da base. Não havia cache próprio dos aliases integrados recentes `TGLExt.V350…`; não renomeei `.olean` DEV para simular essa proveniência. `LEAN_PATH` contém somente a árvore congelada e oito caminhos de pacotes externos readonly, sem caminho do build autoral. Fontes, binários herdados, companheiros e imports externos diretos permaneceram nos pins lidos. Pacotes e dependências antigas não foram recompilados. A correspondência fonte→binário herdada conserva, portanto, essa limitação.

**[REAL — inspeção de registros, sem reexecutar testes autorais]** Foram relidos os **216 pares fonte/binário**, os JSON de compilação e seus streams: **211 registros idênticos aos da mãe e cinco novos**, estes com fonte inalterada durante compilação. As dependências diretas dos cinco novos são anteriores aos outputs. Os **106/106 controles** do autor estão registrados como aprovados; preservam os 105 anteriores e acrescentam `rational_squares_and_original_adjoint_test_does_not_discharge_KMS_trace_or_physical_frontier`.

## Integração, fiação e custódia ainda não gravada

- Cópia lida: `0d6be544852eec20fe1755a68f52d4c4be7007af4ee8c0f0bf4c19fd0e7ed7f9`; **918 embutidos**, batch **749**.
- Mãe `bidual_right_support_custody.json`: `d5e5d1e5c24e5b729b28b8d9a5a3132f886dc8dcc28f9841a67ac6c82929dc32`.
- Original canônico e cópia-base relidos somente por hash: `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`.
- AST Python fora de `_EMBEDDED_KERNEL_FILES` idêntico à mãe; `gate_extension.py` idêntico. O avaliador legado usa `qgc_`, `qgp_` e feed; as seis flags maiores pertencem ao anexo `kernel_frontier`, sem se tornarem entradas diretas desse avaliador.
- O Audit corrente foi obtido pelo registro **Audit_20260913_060848_538521.json** → stdout bruto → mapa reanalisado. SHA256 do stream: `fb82afaccc84e1acff1f8f0cca1c7caf6581fa7f44338dafcaffc860df9e7b2b`. Ambos os hashes globais atuais coincidem com esses bytes; `historical_v350_audit_metadata` conserva os valores históricos separados.
- As **34 superfícies de memória** permanecem nos hashes da mãe, relidos antes da conclusão. Recorders/verifier novos, relatório integrado autoral e nova custódia ainda não foram executados/gravados. A revisão não fez essas escritas.

Leitura estática integral dos helpers atuais: o preparador exige leitura do parecer e os três pins fonte/binário no DEV; o recorder confronta fontes/binários/rc0, pais, streams e 34 estados anteriores; o verifier relê todos os pares compilados e os backups/prefixos. Os appends previstos usam backup imediato de bytes na mesma pasta e temporário conferido antes de substituir cada arquivo. Isso é inspeção da lógica de gravação, não evidência de sua execução nem promessa de transação única das 34 superfícies.

O guia **PROXIMA_ETAPA_BLOCOS_GUIA_DE_TIPOS.md**, SHA256 `ef9ee16719753a6c30355113ada7ec04e255197af9915db50c019f479335183c`, e seus links no recorder foram lidos na versão final. Mantém **OPEN/zero novos alvos**; distingue o gráfico de `E,j,Fix S` do antigo ideal/`Λ,Fix F`, exige cota inferior além de injetividade e preserva a ordem dos blocos. Não auditei nem promovi suas construções futuras.

## Alcance matemático preservado

O limite dos resolventes é forte e restrito ao fecho de `Ran A`; não prova gap ou convergência em norma de operador. As diferenças de quadrados aproximam vetores auto-adjuntos na mesma álgebra não unital, sem pôr sua unidade ou o resolvente nessa álgebra. O teste caracteriza o **S original**; a aplicação com `K` ainda recebe explicitamente **as duas ações de K e K***. Não constrói automaticamente o multiplicador limitado proposto pelos blocos.

Permanecem abertos a aplicação desse critério ao candidato, a estimativa inferior do bloco, a inclusão inversa pelo J original, identificação de `Δ^it`/KMS, traço e obrigações posteriores. O escopo legado `PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT` não identifica por homonímia seu J com o J original do peso. Seis flags maiores falsas, gate legado preservado, `full_plan_complete=false`; nenhuma execução/importação de monólito ou runtime integral. **Conclusão limitada ao pacote integrado20; nenhuma aprovação QG.**

## Artefatos reproduzíveis

- [Verificação final](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/square_resolvent_integrated_20260913_060615_561897/verification.json>) — SHA256 `3349e6a1da84a69af3577c4276ab12fb13747cfbdfd5d06d8769e1a9babaf9da`.
- [Cinco recompilações próprias e axiomas](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/square_resolvent_integrated_20260913_060615_561897/compilation.json>) — SHA256 `eca10fd066a1b09db755ce9c077eab9516b69dbffbe06230393dc6951aa21945`.
- [Árvore, fontes e proveniência de cada dependência](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/square_resolvent_integrated_20260913_060615_561897/build_manifest.json>) — SHA256 `17f797f85687d57cf2133bf20c2c0cff6826dd5459ce6cdb93a3eea245fcfdb9`.
- [Inspeção estática dos helpers e guia](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/square_resolvent_integrated_20260913_060615_561897/helper_static_inspection.json>) — SHA256 `6cd6cb2e7ab48dbf809e2f90b1356d4d8e95d0c62ddddf1d790a32ceeb4c1d28`.
- [Mapa Audit corrente reanalisado](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/square_resolvent_integrated_20260913_060615_561897/axioms.json>); [Conferência dos fontes adicionais da base](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/square_resolvent_integrated_20260913_060615_561897/base_source_provenance.json>); logs próprios e cópias dos streams autorais na mesma pasta.

### Pins dos três módulos integrados

**TGLExt/V350SquareResolventSupport.lean**

- Fonte integrada: `f07a8bd5c7fa6dc6f9dfe52901d46293eba4883f3a597232882bb5ab538f2334`.
- Binário próprio = autoral: `fdb366738c77e5247f89f3998c25307c9baf96c858cfdbd979baacede45ef3e2`.

**TGLExt/V350ScalarRightSquareApproximation.lean**

- Fonte integrada: `6c45fb3595b39fbc6330cc9c4e9d5a3723efc8bdf0047c3d5b4b39f65a25c527`.
- Binário próprio = autoral: `a3cc0996c78e5bdf8611e38390d0c6c5b373c843116293541898474a6ac1be12`.

**TGLExt/V350ScalarSquareAdjointTest.lean**

- Fonte integrada: `d173d21fff82cce7852669ee868f20ce29c45b81500e8029c48b58f9b0912e14`.
- Binário próprio = autoral: `fc1a2c7413533541e6557beb16b26988a3a911341061b62c1542958c387f917f`.
