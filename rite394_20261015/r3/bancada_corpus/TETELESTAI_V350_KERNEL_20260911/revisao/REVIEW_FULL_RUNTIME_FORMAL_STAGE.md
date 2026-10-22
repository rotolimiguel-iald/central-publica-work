# Revisão parcial da etapa formal da rodada integral

Data do parecer: 2026-09-13T09:38:41.130375-03:00. Captura independente: 2026-09-13T09:34:18.886098-03:00.
Estatuto: **[REAL — inspeção independente de fontes e capturas autorais; etapa formal parcial]**.

**Nenhum achado P0–P2 no escopo conferido.** As capturas frescas de build e Audit registram rc0; a cobertura de axiomas corresponde exatamente aos 7.133 nomes únicos solicitados por `#print axioms`. Os onze fornecedores formais do gate estão presentes e auditados. Isto encerra esta verificação formal, sem declarar concluídos o processo integral, os probes, o autoteste, o selo ou os JSONs finais.

## Evidência própria e método

Usei somente leitura de arquivos, análise AST sem execução do monólito, comparação de bytes e parsing independente das capturas. Não iniciei Lean/Lake, não importei/executei `um.py`, não consumi a sessão 94059 nem interrompi o processo do autor. As únicas escritas foram em `revisao/`.

Evidência detalhada: [evidence.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/full_runtime_formal_stage_20260913_093418_886098/evidence.json>); SHA256 `364b495cf0e51b4025c6ff3ada1338a50bb3220f19f3b8467905a8d8d04bfa5b`. Script de verificação: [review_full_runtime_formal_stage.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/review_full_runtime_formal_stage.py>). A evidência contém o mapa completo nome→axiomas, os 922 pares de fontes, os onze fornecedores e pins das capturas, manifestos e raízes. As capturas atuais foram preservadas na mesma subpasta. A verificação própria terminou rc0; isso é execução do script de leitura, **não recompilação independente**.

## Capturas frescas e integridade

| Captura | rc | Bytes | mtime BRT | SHA256 do arquivo capturado |
|---|---:|---:|---|---|
| Build | 0 | 2,329,173 | 2026-09-13T09:27:50.265088-03:00 | `6b0c5d0eb8d8cec3055f6cab3dfaec7b09944420675ef463292b0c1d42643547` |
| Audit | 0 | 913,059 | 2026-09-13T09:27:50.267088-03:00 | `38b708e2428bd5c9e83577182d88089ae72aef041ad811b0e9e35d555999a5df` |

Os cabeçalhos registram `lake build` e `lake env lean TGL/Audit.lean`. Ambos são posteriores ao início da tentativa 02, `2026-09-13T08:37:09.916276-03:00`. Não há linhas de erro nas capturas atuais. Os comprimentos de stdout/stderr recuperados coincidem com os comprimentos em caracteres declarados pelo gravador. O JSON distingue hash dos bytes da captura de hash UTF-8 do stdout recuperado com normalização CRLF; não os equipara ao hash de um stream bruto separado.

O build termina com `Build completed successfully (9467 jobs).` Há 208 eventos visíveis `Built` e 499 `Replayed`; não interpretei 9.467 jobs como 9.467 recompilações novas. A preparação informa cache herdado. Os avisos incluem lint e `aesop ... has local changes`: não houve auditoria nova de todo o pacote aesop nem revalidação dos 127.078 arquivos do inventário de preparação. Esse limite de proveniência permanece explícito.

`ROOT/um.py` e `ROOT/r/um.py` são byte a byte iguais, SHA256 `fd611111866dc6ff30e9ed355b62bec32cdba505b742d550ffa3351ffd08e566`, também igual ao pin do contrato ativo. Os **922 arquivos embutidos**, incluindo **218 módulos TGLExt/V350**, coincidem literalmente em bytes com os materializados em `r/tgl_kernel`. A fonte `TGL/Audit.lean` e suas listas de comandos coincidem com o embutido. As duas raízes binárias foram lidas e pinadas:

- `TGLExt.olean`: `cafa57bff7e165e35019d23e826aed19dcbdc2b5e4d61c57deba3085b2969663`, mtime 2026-09-13T09:26:17.515803-03:00.
- `Audit.olean`: `cba1498af7af85de2eef3232ca89cd6a90bfbca27ddba344ea95fbae6f41a2cd`, mtime 2026-09-13T09:26:43.122026-03:00.

Os rc1 de `r/failed_attempt_01` foram identificados e excluídos; não são a evidência da tentativa 02. Os manifestos de preparação, com caminho e estado antigos, foram tratados como histórico de preparação. O hash canônico neles declarado foi preservado como dado de origem; esta etapa não fez nova releitura do original externo nem revalidou toda a cadeia de binários das dependências.

## Cobertura formal e onze entradas do contrato

Foram encontrados **7.140 comandos/mensagens `#print axioms`, 7.133 nomes únicos e sete repetições consistentes**. Nenhum nome faltante, extra ou com conjuntos conflitantes. O parser reconhece os **50 resultados `does not depend on any axioms`**, incluindo `TGLExt.comm_of_fixed'`; apóstrofos não truncam nomes. Todos os conjuntos retornados estão contidos em `propext`, `Classical.choice`, `Quot.sound`; os conjuntos vazios são válidos. Não apareceu axioma fora da lista permitida. A saída do build também cobre o mesmo conjunto auditado.

Há ainda 656 comandos `#check`; 174 nomes únicos desses comandos não têm impressão individual de axiomas no Audit existente. O rc0 confere sua elaboração, não fornece para cada um uma lista individual de axiomas. A cobertura exata acima refere-se aos comandos explícitos `#print axioms`. Essa distinção não foi convertida em nova exigência matemática; todos os onze fornecedores do gate têm impressão explícita.

| Entrada consumida | Declaração auditada | Fonte materializada |
|---|---|---|
| `qgc_concrete_aqft_core_constructed` | `TGLExt.qgStrongCertificate_core` | `TGLExt/StrongAssembly.lean:127` |
| `qgc_concrete_breuer_corner_constructed` | `TGLExt.qgStrongCertificate_corner` | `TGLExt/StrongAssembly.lean:135` |
| `qgc_concrete_modular_four_frame_constructed` | `TGLExt.qgStrongCertificate_frame` | `TGLExt/StrongAssembly.lean:143` |
| `qgc_concrete_solder_field_constructed` | `TGLExt.qgStrongCertificate_solder` | `TGLExt/SolderField.lean:155` |
| `qgc_concrete_emergent_einstein_proved` | `TGLExt.qgStrongCertificate_einstein` | `TGLExt/EmergentEinstein.lean:340` |
| `qgc_canonical_boundary_transport_witness_constructed` | `TGLExt.qgClosureCertificateV2` | `TGLExt/TheCoinage.lean:50` |
| `qgp_massless_spin2_proved` | `TGLExt.qgPhysicsCertificate_massless` | `TGLExt/PhysicsCertificates.lean:109` |
| `qgp_exactly_two_helicities_proved` | `TGLExt.qgPhysicsCertificate_helicities` | `TGLExt/PhysicsCertificates.lean:212` |
| `qgp_ghost_free_proved` | `TGLExt.qgPhysicsCertificate_ghostfree` | `TGLExt/PhysicsCertificates.lean:231` |
| `qgp_stress_energy_conserved` | `TGLExt.qgPhysicsCertificate_conservation` | `TGLExt/PhysicsCertificates.lean:259` |
| `qgp_relevant_anomalies_absent` | `TGLExt.qgPhysicsCertificate_anomaly` | `TGLExt/PhysicsCertificates.lean:292` |

Cada linha foi extraída das listas do próprio monólito por AST, localizada em uma fonte embutida/materializada e confrontada com o Audit fresco; todas têm exatamente o trio permitido. A ligação dessas seis entradas `qgc` e cinco `qgp` ao avaliador principal mantém o escopo da auditoria anterior. A cobertura formal está confirmada aqui; não antecipei os valores persistidos no futuro JSON final da rodada.

## Limite do parecer

O contrato lido tem SHA256 `d1b51e807e1c811e2f3c9a12693757d46c4f99b5a8f3f7e15871e08419d19d0f`. Nenhuma obrigação original-S/KMS, UV ou flag adicional foi criada ou cobrada como bloqueio do gate principal. A separação já estabelecida entre suas entradas e o anexo `kernel_frontier` permanece; uma subdecisão literal não foi tratada como prova nova.

**[OPEN — nesta revisão]** Restante dos cálculos, probes, autoteste, emissão de selo e JSONs finais. O manifesto da tentativa 02 foi lido como registro de início/estado, sem consulta ou controle da sessão/processo. Este parecer não certifica o término da rodada, não promove gate e não declara confirmação física. Os pareceres anteriores, originais, fontes, memórias e custódias permaneceram intocados.
