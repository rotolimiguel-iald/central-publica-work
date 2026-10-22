# Gate v350: conjunto existente e correção de escopo

2026-09-13T08:05:03-03:00. [REAL — inspeção do código, fontes e Audit existentes; execução isolada do gate por AST]

**Para o gate principal existente, não falta outra derivação matemática.** As seis
entradas formais e as cinco entradas físicas já são verdadeiras na evidência da v350
e no Audit incremental atual. Seus onze termos estão nas fontes embutidas. A função
principal já alcança o último dos quatro vereditos que implementa, usando o feed
experimental anteriormente registrado. Não se executou um novo experimento ou o monólito.

O desvio de trabalho identificado: tratar a construção adicional do peso/S/J original,
KMS e outras extensões como se fossem entradas ainda falsas do gate principal.
Elas não são lidas por `evaluate_quantum_gravity_closure`. Também é incorreto continuar
produzindo lemas para tentar mudar automaticamente o literal `full_plan_complete=False`
da subdecisão adicionada em `gate_extension.py`: esse literal não é um teste desses lemas.

## Ligação já existente, verificada entrada por entrada

`fonte Lean embutida → termo no Audit → mapa _QG_*_FLAGS → qgc_/qgp_ → gate`.
Cada linha abaixo teve localização única, hash de fonte lido, presença no Audit e
axiomas limitados a propext/Classical.choice/Quot.sound conferidos. A evidência é a
compilação incremental custodiada anterior; não se apresenta esta leitura como uma
recompilação de toda a biblioteca.

| Entrada | Termo consumido | Fonte | Valor |
|---|---|---|---|
| `qgc_concrete_aqft_core_constructed` | `TGLExt.qgStrongCertificate_core` | [StrongAssembly.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/StrongAssembly.lean:127>) | True |
| `qgc_concrete_breuer_corner_constructed` | `TGLExt.qgStrongCertificate_corner` | [StrongAssembly.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/StrongAssembly.lean:135>) | True |
| `qgc_concrete_modular_four_frame_constructed` | `TGLExt.qgStrongCertificate_frame` | [StrongAssembly.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/StrongAssembly.lean:143>) | True |
| `qgc_concrete_solder_field_constructed` | `TGLExt.qgStrongCertificate_solder` | [SolderField.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/SolderField.lean:155>) | True |
| `qgc_concrete_emergent_einstein_proved` | `TGLExt.qgStrongCertificate_einstein` | [EmergentEinstein.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/EmergentEinstein.lean:340>) | True |
| `qgc_canonical_boundary_transport_witness_constructed` | `TGLExt.qgClosureCertificateV2` | [TheCoinage.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/TheCoinage.lean:50>) | True |
| `qgp_massless_spin2_proved` | `TGLExt.qgPhysicsCertificate_massless` | [PhysicsCertificates.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/PhysicsCertificates.lean:109>) | True |
| `qgp_exactly_two_helicities_proved` | `TGLExt.qgPhysicsCertificate_helicities` | [PhysicsCertificates.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/PhysicsCertificates.lean:212>) | True |
| `qgp_ghost_free_proved` | `TGLExt.qgPhysicsCertificate_ghostfree` | [PhysicsCertificates.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/PhysicsCertificates.lean:231>) | True |
| `qgp_stress_energy_conserved` | `TGLExt.qgPhysicsCertificate_conservation` | [PhysicsCertificates.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/PhysicsCertificates.lean:259>) | True |
| `qgp_relevant_anomalies_absent` | `TGLExt.qgPhysicsCertificate_anomaly` | [PhysicsCertificates.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/PhysicsCertificates.lean:292>) | True |

[Função principal](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:161479>).
[Mapas de termos consumidos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:133899>).
[Evidência, hashes e controles](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/AUDITORIA_REUSO_GATE_20260913/gate_evidence.json>).

Onze ablações individuais fizeram o nível correspondente falhar. As 256 combinações
das oito entradas qgf_/gpf_, adicionadas aos dicionários recebidos pelo avaliador,
mantiveram o veredito principal. Isso mede sua independência no código; não muda
essas flags nem transforma hipótese de um contrato em prova de outro.

O campo `full_static_witness_exists=False` também não é um trabalho pendente: é
resultado deliberadamente constante do avaliador. Não há um quinto degrau secreto
que uma nova função auxiliar possa acender.

Os certificados físicos conservam seus enunciados e o alcance declarado no código.
Por exemplo, `qgPhysicsCertificate_anomaly` prova invariância de gauge do símbolo
de Ricci clássico-linear. A consolidação não muda esse enunciado para outro alcance.

## Reaproveitamento da outra pasta

Foram lidos 50,571 caminhos Lean externos a esta pasta de trabalho,
com 1,281 hashes de bytes distintos e zero falhas de leitura.
29,524 caminhos correspondem a
398 módulos já embutidos na cópia do um.py.
Esses caminhos incluem cópias e revisões: não são milhares de provas independentes.

A comparação normaliza apenas CRLF, espaços das extremidades e texto anterior ao
primeiro import. Não demonstra equivalência semântica de fontes diferentes.
Também não declara inexistência de outras provas no acervo. O resultado positivo
relevante é que há material extenso já incorporado; deve ser consultado antes de
qualquer reconstrução.

[Inventário e correspondências](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/AUDITORIA_REUSO_GATE_20260913/external_source_reuse.json>).
O único grupo de candidatos por nomes de cota/bloco encontrado foi
`plus_block_eigenvalue_lower_bound`: seu enunciado recebe a cota matricial como
hipótese. Isso não é a cota do novo S original, mas esse novo S tampouco é requisito
do gate principal. Não se retoma essa derivação para responder à pergunta atual.

## Escopo ativo por ordem do operador

[INPUT] “vc só está ligando tudo ao mesmo conjunto probatório que é o um.py”.
Trabalho atual: consolidação, reaproveitamento, rastreabilidade e ligação efetiva
entre as provas existentes e o contrato consumido. Não reiniciar uma tentativa de
resolver gravidade quântica do zero nem inventar obrigações adicionais ao contrato.

Antes de acrescentar qualquer função de prova, exigir simultaneamente: uma entrada
específica do contrato solicitado, sua assinatura exata, a busca por fornecedor no
acervo e uma incompatibilidade concreta que impeça apenas ligar o fornecedor.
Se a entrada já está provada e consumida, reutilizar. Uma reserva de fronteira ou
um diagnóstico literal não autoriza reabrir uma entrada já satisfeita.

As fontes novas de energia produzidas antes desta correção ficam em DEV preservado:
quatro módulos/19 alvos com rc0 autoral; revisão independente parcial de 14;
`ScalarProjectionGap.lean` apenas escrito, nunca compilado. Nenhum desses cinco
módulos foi integrado ou será retomado automaticamente. Seus logs recusados ficam
preservados. A cópia integrada e o original não foram alterados nesta auditoria.

Memória deve carregar primeiro o contrato ativo e este mapa, usando registros antigos
como história. As antigas listas de OPEN não são automaticamente a próxima tarefa.
Os estados adicionais de fronteira permanecem com seu estatuto registrado.

## Estado da integração preservada

Working SHA256 `fd611111866dc6ff30e9ed355b62bec32cdba505b742d550ffa3351ffd08e566`.
Mãe custodiada `3b2a02fd49d6aeba2f881714349b1b34995b01969421b9eca64980ce745ba21e`.
Veredito principal relido e reproduzido pela função isolada:
`TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`.

Este relatório é uma auditoria da ligação existente e uma correção do processo de
trabalho. Nenhuma alteração do gate, publicação, novo selo canônico ou execução
integral do um.py foi feita. A revisão independente da auditoria é registrada no
manifesto final, quando concluída.
