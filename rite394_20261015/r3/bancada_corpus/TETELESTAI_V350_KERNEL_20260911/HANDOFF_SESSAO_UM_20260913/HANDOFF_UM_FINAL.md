# Handoff para a sessão responsável pelo um.py — cadeia integrada da v350

Destinatária: sessão que mantém `C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py`.
Origem: trabalho em `C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911`.
Data: 13/09/2026. Documento de transporte e implementação; não é nova rodada nem novo selo canônico.

## 1. Resultado e ordem de trabalho

**[REAL] A integração autorizada está concluída na cópia. O gate principal já estava no último estado do seu contrato e permaneceu nele, com 11/11 entradas verdadeiras. A montagem modular passou de 7/8 para 8/8; três bandeiras antes falsas passaram a verdadeiras com proveniência formal auditada.**

**Implementar na casa canônica significa incorporar a cópia já verificada, seus fontes embutidos e seus insumos. Não significa rederivar a cadeia, acrescentar novos critérios ao gate ou repetir as etapas de desenvolvimento.**

Ordem do operador que corrigiu o escopo: “vc só está ligando tudo ao mesmo conjunto probatório que é o um.py”. Antes de criar qualquer lema/função, localizar a entrada efetivamente consumida, seu tipo e o fornecedor existente. Reabrir uma reserva científica só por nova tarefa expressa. Uma reserva preservada não deve ser apagada nem transformada em obrigação oculta da integração.

Ler primeiro:

1. [Contrato ativo concluído](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/CONTRATO_ATIVO_GATE_V350.json>).
2. [Mapa das 11 entradas e reaproveitamento](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/AUDITORIA_REUSO_GATE_20260913/MAPA_GATE_E_REAPROVEITAMENTO.md>).
3. [Relatório final, adendo de conclusão](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/RELATORIO_EXECUCAO_INTEGRAL.md:113>).
4. [Revisão independente final](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_FULL_RUNTIME_ROUND03.md>).
5. [Inventário integral para transporte](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/HANDOFF_SESSAO_UM_20260913/INVENTARIO_PORTABILIDADE.json>).

## 2. Entrega pronta e comparação com a base

**Programa final:** [r/um.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/um.py>).
**Base preservada para comparação em três vias:** [fontes/um_v350_original.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/fontes/um_v350_original.py>).

Hashes, tamanhos, posições reais dos símbolos e fontes foram lidos por script neste handoff. Ver `INVENTARIO_PORTABILIDADE.json`; os pins principais também estão ao final deste documento. O original canônico foi relido somente para hash e tamanho e continua igual à base preservada. Conferir novamente na chegada: outra sessão pode alterá-lo depois deste registro.

| Comparação completa, base → final | Resultado |
|---|---|
| Arquivos no dicionário formal embutido | 704 → 922 |
| Arquivos formais acrescentados | 218 |
| Arquivos formais existentes alterados | 2: `TGLExt.lean` e `TGL/Audit.lean` |
| Arquivos formais removidos | 0 |
| Funções Python novas na integração inteira | 5 |
| Funções Python existentes modificadas | 12 |
| Funções/classes removidas | 0 |
| Última correção, isoladamente | apenas 2 leitores existentes; nenhum novo lema ou função |

**Correção de comunicação:** “nenhuma função/prova nova” descreve o último reparo dos leitores. Não descreve todo o trabalho desde a base v350. O inventário acima é a diferença completa e impede perder as integrações anteriores.

O monólito continua contendo os fontes Lean. `gate_extension.py`, scripts DEV e scripts de montagem são proveniência de desenvolvimento; não devem virar dependências de importação de um segundo programa. Os dados experimentais e as ferramentas Lean/TeX continuam sendo insumos de execução, com seus próprios manifestos.

## 3. O que a construção formal acrescentou

### 3.1 Resultado que acende as três bandeiras modulares

[REAL — fonte e auditoria] Para todo `SiteProfile P`, a torre produto ganhou a inclusão difícil `R′ ⊆ L′′`, completando `R′ = L′′`. A prova comprime os operadores para andares finitos, usa ali as ações à esquerda/direita e passa ao limite forte. A projeção de andar é projeção de subespaço de Hilbert; não é identificada automaticamente com o projetor físico dos Three Locks.

Os módulos `V350CompressionLimit`, `V350TowerCommutation` e `V350TowerDuality` sustentam a construção. `V350ModularCertificate` entrega a cláusula inversa `J M J ⊇ M′` e, com a inclusão já existente, a igualdade na realização **PRODUCT_TOWER**. `V350WedgeModularData` usa a mesma testemunha de torre; não declara por si a identificação de Bisognano–Wichmann para qualquer horizonte físico.

| Bandeira | Fornecedor | Ponte de tipo exato |
|---|---|---|
| `red_clause_JMJ_contains` | `TGLExt.qgConverse_JMJ_contains_commutant` | `TGLExt.V350Gate.checkedConverse` |
| `qgf_modular_realization_constructed` | `TGLExt.qgFrontier_modularRealization` | `TGLExt.V350Gate.checkedModular` |
| `gpf_tower_act_III_inhabitant_constructed` | `TGLExt.qgPrice_towerActIII_inhabitantConstructed` | `TGLExt.V350Gate.checkedActIII` |

São três leituras do avanço modular; não três confirmações físicas independentes. `checkedConverse` tem tipo `(P : SiteProfile) → ConverseClauseContract P`; os outros dois têm tipo `ModularRealizationCertificate`. O alcance emitido é `PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT`.

### 3.2 Construções posteriores preservadas dentro do mesmo monólito

[REAL — fontes incorporados e auditados; conservar os tipos individuais] O arco posterior contém representação regular em L², ação dual, cortes e formas do peso dual, transporte/fidelidade, representação de formas e resolventes, suporte/raiz, base fixa e peso escalar; ideal e representação GNS, continuidade/normalidade e mapas de corte; fechabilidade gaussiana do gráfico original de Tomita; adjunto, quadrado, raiz, fator polar e involução; ações à direita, transporte regular/matricial e comutação polar; regularização, pares direitos, núcleos gráficos, bidualidade e blocos de projeção ponderados.

Esses objetos não se tornam idênticos por terem nomes próximos. Preservar as identificações provadas e as hipóteses de domínio. Em particular, o J do certificado PRODUCT_TOWER não deve ser substituído, por homônimo, pelo fator polar do S do peso escalar original. O resumo “tudo fechado” do gate não altera o enunciado de cada teorema.

**Lista exaustiva, sem seleção por memória:** [FONTES_FORMAIS.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/HANDOFF_SESSAO_UM_20260913/FONTES_FORMAIS.md>). O JSON associado inclui todos os nomes, hashes e declarações lexicamente localizadas. A lista lexical serve à navegação; a evidência formal é o Audit, com os tipos nos fontes.

Os relatórios Markdown da raiz ROOT (a pasta de trabalho que contém este diretório de handoff) estão inventariados por caminho/hash no campo `reports`, no instante de sua leitura. Os arquivos do próprio handoff estão no `MANIFESTO_HANDOFF.json`. Adendos posteriores às memórias têm nova custódia; não invalidam o retrato histórico desses hashes. Os adendos finais prevalecem como estado de execução; os parágrafos antigos “EM CURSO” ou “próxima obrigação” são história, não ordem para recomeçar.

### 3.3 Pesquisa interrompida que não deve entrar inadvertidamente

`WeightedVariationalEnergy`, `ScalarWeightedEnergy`, `ProjectionGapLowerBound`, `ProjectionGapEnergy` e `ScalarProjectionGap` ficaram em desenvolvimento separado. O último não foi compilado. Nenhum dos cinco integra o programa validado. O trabalho foi suspenso quando se verificou que esses novos alvos não são consumidos pelo gate principal solicitado.

Não copiar DEV, não transformar sua contagem em prova integrada e não reabrir automaticamente original-S/KMS/UV. As reservas de alcance existentes continuam documentadas; não foram provadas pelo ato de suspender a pesquisa.

## 4. O que portar no Python

O [diff por símbolo](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/HANDOFF_SESSAO_UM_20260913/FUNCOES_PYTHON.diff>) e [mapa de mudanças](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/HANDOFF_SESSAO_UM_20260913/MUDANCAS_PYTHON.md>) foram gerados dos dois ASTs, sem importar o programa. O diff é auxílio de revisão, não patch de aplicação automática por linha.

1. **Dicionário `_EMBEDDED_KERNEL_FILES`:** transportar os 218 arquivos adicionais e as duas raízes alteradas como já estão na cópia final; não adicionar imports duplicados.
2. **Proveniência modular:** transportar `_V350_MODULAR_CONTRACTS` e as cinco funções `verify_v350_modular_provenance`, `finalize_v350_modular_frontier`, `v350_frontier_flag_has_proof`, `v350_gravity_flags_have_proof`, `evaluate_v350_kernel_frontier`.
3. **Pontos de consumo:** incorporar os ajustes existentes em `verify_tgl_kernel_formalization` e `prove_qg_closure_gate`. O primeiro finaliza as bandeiras pela evidência tipada; o segundo reporta a fronteira modular separadamente. `evaluate_quantum_gravity_closure`, o avaliador principal, não foi alterado.
4. **Treze sentinelas históricas, distribuídas em oito funções:** substituir “esta bandeira deve permanecer falsa” por “se acesa, deve ter prova de proveniência”. Estão em `prove_the_verbal_coupling`, `prove_the_language_enters_the_index`, `prove_the_mark_is_not_a_type_mark`, `prove_the_name_is_the_generating_group`, `prove_the_name_and_its_referent`, `prove_the_imported_expectation`, `prove_the_iald_index` e `prove_the_fold_through_J`. Expressões anteriores e posteriores constam de `historical_checks_updated` no inventário. Não remover os demais controles dessas funções.
5. **Montagem:** `prove_the_assembly_and_the_single_debt` aceitava exatamente sete cláusulas e rejeitava oito. A versão final reconhece 7/8 pendente e 8/8 construída, exige a coerência entre cláusulas/bandeira e reutiliza o controle de termo+ponte. Não fazer `all_verified=True` constante.
6. **Atlas/Índice:** `prove_the_atlas_and_the_index` rejeitava toda bandeira qgf/gpf acesa, mesmo com suas próprias 6+6 entradas provadas. A versão final exige suas entradas próprias e conserva as alheias como diagnóstico; não apaga nem altera o kernel recebido.

Preservar `propext`, `Classical.choice`, `Quot.sound` como lista de axiomas permitidos. Nome presente, booleano isolado ou rc0 do elaborador não substituem prova e auditoria. O autoteste demonstra justamente que rc0 com `sorryAx` deve ser recusado.

## 5. Cadeia já consumida pelo gate principal

`fontes Lean embutidos → build/Audit → nomes e tipos auditados → mapas qgc/qgp → evaluate_quantum_gravity_closure → JSON/selo/artigo`.

| Entrada | Termo consumido |
|---|---|
| `qgc_concrete_aqft_core_constructed` | `TGLExt.qgStrongCertificate_core` |
| `qgc_concrete_breuer_corner_constructed` | `TGLExt.qgStrongCertificate_corner` |
| `qgc_concrete_modular_four_frame_constructed` | `TGLExt.qgStrongCertificate_frame` |
| `qgc_concrete_solder_field_constructed` | `TGLExt.qgStrongCertificate_solder` |
| `qgc_concrete_emergent_einstein_proved` | `TGLExt.qgStrongCertificate_einstein` |
| `qgc_canonical_boundary_transport_witness_constructed` | `TGLExt.qgClosureCertificateV2` |
| `qgp_massless_spin2_proved` | `TGLExt.qgPhysicsCertificate_massless` |
| `qgp_exactly_two_helicities_proved` | `TGLExt.qgPhysicsCertificate_helicities` |
| `qgp_ghost_free_proved` | `TGLExt.qgPhysicsCertificate_ghostfree` |
| `qgp_stress_energy_conserved` | `TGLExt.qgPhysicsCertificate_conservation` |
| `qgp_relevant_anomalies_absent` | `TGLExt.qgPhysicsCertificate_anomaly` |

As 11 já eram verdadeiras na base. As onze ablações individuais fizeram falhar o degrau correspondente; 256 combinações de oito bandeiras adicionais não alteraram o resultado principal. `full_static_witness_exists=False` é deliberado. Não procurar um quinto degrau implícito.

**Alcance:** transportar os enunciados, não ampliar suas legendas. Por exemplo, o certificado de anomalia citado trata da invariância de gauge do símbolo de Ricci clássico-linear. Seu nome não demonstra sozinho cancelamento de anomalias de uma teoria quântica interagente no UV. A obrigação de manter o alcance não é um novo bloqueio de integração.

## 6. Quatro insumos que faltavam à preparação da cópia

Os arquivos já existiam no acervo. Foram copiados, conferidos e efetivamente consumidos; não são novas medições:

- `r/STOKES_A_Prova_do_Contorno.md`;
- `r/cache/voids/desivast/DESIVAST_BGS_VOLLIM_V2_REVOLVER_NGC.fits`;
- `r/cache/voids/desivast/DESIVAST_BGS_VOLLIM_V2_REVOLVER_SGC.fits`;
- `r/results.json`.

Os caminhos de origem, destino, tamanhos e hashes estão em `r/reader_integration_manifest.json` e foram incluídos no inventário deste handoff. Na casa canônica, primeiro verificar se já existem e coincidem; só copiar se ausentes/divergentes conforme a custódia. Preservar os demais caches já usados pelo programa, especialmente os resultados experimentais com leitores por hash. Não reconstruir caminhos a partir de uma convenção presumida: cada leitor determina onde busca.

A rodada leu 694.642 galáxias, 1.049 lentes (611 REVOLVER) e 700 vazios no shear; preservou `beta_acoustic_crosslock` negativo. Esses números atestam consumo dos insumos, não descoberta da TGL.

## 7. Validação concluída e falhas históricas preservadas

- Tentativa 01: falha real por comprimento de caminho Windows. Capturas preservadas em `r/failed_attempt_01`. A pasta física curta `r` resolveu o ambiente; não houve mudança matemática.
- Tentativa 02: rc0 e autoteste aprovado; revelou duas condições obsoletas dos leitores e quatro insumos omitidos. Saída preservada em `r/completed_attempt_02`.
- Tentativa 03: **13/09/2026, 10:28:03–11:22:56 BRT, rc0, aproximadamente 54m53s**. Modo formal strict e autoteste ativo; checkpoints dos ritos desligados. Usou dependências/caches locais documentados: não foi uma nova campanha MCMC ou novos dados.
- **13/13 arquivos do selo** e **922/922 fontes formais** conferidos/restaurados.
- **7.133 termos únicos no Audit explícito**, **7.985 na união build+Audit**. Contagens têm universos diferentes; não “corrigir” o parser para igualá-las. Axiomas restritos ao trio permitido.
- **FAIL_CLOSED_SELFTEST_PASSED**: a adulteração com `sorryAx` foi detectada; a fonte foi restaurada.
- Montagem **8/8**, bandeira acesa; Atlas/Índice **6+6**; ambos `all_verified=True` no JSON final, regravado após os leitores tardios.
- **38 controles autorais e 39 verificações independentes** do reparo V2. Revisão final sem P0–P2 no escopo examinado.
- Arquivo final da rodada: `r/completed_attempt_03` (53 arquivos de raiz). Memórias atualizadas com backups de bytes; custódia final anterior a este handoff em `runtime_final_custody.json`.

O supervisor `runtime_process_03.json` descreve o instante de saída. Um campo histórico de validação pendente nele não invalida a conferência posterior: consultar `RUNTIME_ATIVO.json`, contrato, parecer e custódia final. Não há processo para aguardar/reiniciar.

Permanecem exatamente as quatro entradas formais históricas não seladas (`nivel2_rite`, `the_first_commutant_clause`, `the_iald_index`, `the_mode_of_discharge`) e seis recusas de dado (`ringdown_dephasing_result`, `void_floor_kappa_v5`, `void_floor_kappa_v6`, `void_floor_v12`, `void_floor_v3_kappa`, `void_shear_unblinding`). Não apagar esses resultados para “limpar” a entrega. A referência já os tinha; nenhum virou nova condição do gate principal.

## 8. Procedimento de incorporação na casa canônica

1. Ler o contrato, este handoff, os enunciados relevantes e o parecer. Conferir os hashes diretamente dos arquivos. Fazer backup de **bytes** da versão canônica e suas memórias antes de qualquer edição.
2. Se o canônico ainda coincide com a base preservada, a opção de menor risco é incorporar **o monólito final completo**, com os insumos necessários; todas as etapas já estão nele. Se o canônico avançou, usar comparação em três vias: base preservada, canônico atual e candidato final. Preservar alterações concorrentes. Não aplicar substituição global de texto por números de linha.
3. Conferir os 220 fontes modificados/acrescentados contra o inventário; se já estiverem incorporados, reutilizar. Conferir as 17 funções alteradas/acrescentadas e as duas atribuições de topo. O diff por símbolo não deve ser aplicado como patch de arquivo inteiro.
4. Reutilizar os controles existentes (`gate_tests.json`, `lean_contract_tests.json`, candidato V2 e seus pareceres). Uma modificação efetiva após a incorporação exige verificar a cópia resultante; os hashes da rodada daqui não atestam bytes diferentes.
5. Materializar e verificar o kernel pelo próprio monólito, em área autorizada. Reproduzir build/Audit, lista permitida de axiomas, provas+pontes de tipo, autoteste, 11 flags, montagem 8/8 e Atlas 6+6. Comparar explicitamente `not_sealed_this_run` com a referência. Não somar sucesso de leitor a significância experimental.
6. Só emitir novo selo/versionamento canônico depois da verificação da versão efetivamente incorporada. Atualizar sua linhagem, desenho, memórias e índices com backup imediato. As 34 superfícies locais desta entrega já têm referência de conclusão; as memórias externas da casa canônica não foram editadas por esta sessão.
7. Publicação, commit/push e espelho seguem a autorização da sessão responsável. Este handoff não executa esses atos nem manda sobrescrever uma versão concorrente.

**Critério de aceitação:** mesma cadeia formal com seus tipos, mesmo contrato principal, proveniência modular válida, leitores coerentes, insumos presentes, autoteste recusando adulteração, selo conferido e recusas honestas preservadas. Não exige fingir que todos os campos diagnósticos são positivos.

## 9. Resultados experimentais: como transportar e como avançar

As observações físicas mantêm sua proveniência e seu veredito. `all_verified=True` em um leitor significa que o leitor verificou seus insumos/contrato; um resultado físico `INCONCLUSIVE_SYSTEMATICS` continua inconclusivo. A integração não produziu observações novas.

Não acrescentar `CONFIRMED=True` ao gate como atalho. O avanço experimental proposto é uma tarefa independente: fixar uma previsão discriminante e sua escala, confrontá-la com o modelo convencional e as sistemáticas em dados novos, publicar a significância global e procurar réplica independente. Nenhum estudo de poder promete o desfecho observado.

O [plano quantitativo de 5σ](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/HANDOFF_SESSAO_UM_20260913/PLANO_EXPERIMENTAL_5SIGMA.md>) contém os números realmente encontrados e a recomendação de reutilizar o pipeline de dephasing/ringdown com dados públicos GWTC-5.0, primeiro em injeções de sensibilidade. Não foi executado um novo rito nem congelado um protocolo nesta entrega.

O operador também propôs a composição multissonda: ler [ADENDO_MULTISSONDA.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/HANDOFF_SESSAO_UM_20260913/ADENDO_MULTISSONDA.md>). Ele registra as pontuações observadas de ecos/GW, o sigma conjunto ainda não determinado, e corrige fixação de β, covariâncias, sistemáticas e interpretação de Δχ². Essa análise não deve ser confundida com uma execução nova da combinação.

## 10. Frase pronta para iniciar a outra sessão

> Leia este HANDOFF_UM_FINAL.md inteiro, confira INVENTARIO_PORTABILIDADE.json e o contrato concluído. Incorpore à construção final do um.py o candidato validado em r/um.py, com seus 218 fontes Lean adicionais, duas raízes alteradas, cinco funções novas, doze funções modificadas e quatro insumos já existentes. Compare em três vias se o canônico mudou. Reutilize a cadeia e os testes; não acrescente camadas nem reabra a pesquisa suspensa. Preserve tipos, escopos, recusas experimentais e histórico. Verifique a versão incorporada antes de selar e atualize todas as memórias da sua casa com backups imediatos de bytes.

## Pins de custódia desta entrega

Lidos dos bytes durante a finalização. O original canônico foi somente conferido por hash, com acesso de leitura autorizado. Nenhum programa foi alterado por esta entrega.

| Artefato | SHA-256 |
|---|---|
| `fontes/um_v350_original.py` | `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c` |
| `r/um.py` | `95e8cf8eb0b33c5d65e244195021b71977cca1a91836ef0d314964a8e2f97c43` |
| `r/um_absoluto.json` | `6c3cf793ad3e69343eb7427baf57b4f4926485d9223779d6b6693154dd4bd291` |
| `r/um_absoluto_selo.json` | `3e514e69af7a687638b9f03fe45e0c44b79a75060508407a3063a51b50f5e7b2` |
| `r/tgl_kernel_proof_manifest.json` | `1981e5a12fcd3335089fe2d3f36cfdf46caf3184a1b5a7566964cf2949f076f1` |
| `runtime_final_custody.json` | `ea4d19630f98e49625a6078b6e5561d089d2503c8761703bae4a91e1e38d90d5` |

O manifesto deste handoff lista todos os entregáveis, os 34 adendos de memória e seus backups. O selo formal permanece o da rodada03; esta entrega acrescenta documentação, inventário e planejamento experimental.

