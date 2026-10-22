# Rodada 02 — execução concluída e regressões auxiliares

Data: 2026-09-13T10:20:27.829323-03:00. Escopo: contrato ativo v350, consolidação/reuso.

**[REAL — arquivos conferidos] A rodada terminou rc0 e reproduziu o terminal do gate principal. Há três achados P2 abaixo; não atesto a integração auxiliar como completa.** Nenhum P0/P1 foi identificado neste exame delimitado. O resultado não autoriza apagar recusas, substituir saídas por `True` ou acrescentar exigências original-S/KMS/UV ao gate principal.

Esta leitura começou durante o autoteste: snapshots preliminares de 10:07 permanecem preservados. Após o sinal de término, reli o manifesto do processo, selo, JSON, proof_manifest e capturas finais. O parecer formal anterior permanece intocado e é herdado; não repeti compilações, não executei/importei o monólito, não consumi sessão 94059 e não controlei PID58040. Toda escrita foi em `revisao/`.

## Execução, selos e alcance formal

`runtime_process_02.json` registra início 2026-09-13T08:37:09.916276-03:00, término **2026-09-13T10:08:08.831694-03:00**, rc **0**, duração **5458.9154s**. O stdout termina com `FAIL_CLOSED_SELFTEST_PASSED`; o selo final registra o mesmo resultado. A chave de checkpoints ficou desligada, com zero ritos reaproveitados. Isso não significa recompilação fria de todas as dependências Lean: a proveniência de cache descrita no parecer formal continua válida.

Na adulteração autoral, build e Audit Lean retornaram rc0, mas imprimiram `sorryAx` em `TGL.HalfNat.halfNat_of_selfConjugate`; o verificador recusou corretamente (`TGL_KERNEL_FORMALIZATION_FAILED`, `sorryAx_absent=False`). Após restauração, o stdout registra `all_verified=True`; a fonte `TGL/HalfNat.lean` voltou aos bytes embutidos e os mapas limpos de axiomas foram recuperados. Portanto rc0 isolado não foi confundido com prova limpa.

Os **13 arquivos** da tabela `sha256` do selo conferem com seus bytes atuais. ROOT/um.py e r/um.py são idênticos. Pins efetivamente lidos:

| Artefato | SHA256 |
|---|---|
| Programa ROOT e r | `fd611111866dc6ff30e9ed355b62bec32cdba505b742d550ffa3351ffd08e566` |
| um_absoluto.json | `656ef62d42bd9df046e30e1d780de92f5e14b437d8602cf7a8642d990322c3c7` |
| Selo após autoteste | `6ca767916e17e8be04e5fab69fb83d0f57a8dab0c65b4fce0cd29248af17e8de` |
| proof_manifest | `6f40c1d2e548e779ed8e0174c7dbe240bea769fca38c039e0e6fa73402bee0b5` |
| runtime_process_02.json | `fca661e5b1b6c4cddb05403193b9bd30f4f2a4c83ad5f0c434969adbbe40e3a7` |

Os seis fornecedores `qgc` e cinco `qgp` do contrato principal estão `True` no JSON, com os termos explícitos e axiomas permitidos. O terminal coincide com a referência em `fontes/um_absoluto.json` e com o selo:

`TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`

Esse é o texto emitido pelo programa, no alcance do contrato existente; não é declaração de confirmação física desta revisão. As seis flags maiores do anexo continuam falsas, `legacy_gate_changed=False` e `full_plan_complete=False`; esses campos não foram convertidos em novas entradas do gate principal.

**Escopos do mapa de axiomas:** Audit explícito = **7.140 mensagens / 7.133 nomes únicos**; build = **13.884 mensagens / 7.985 nomes únicos**. A união build+Audit coincide **exatamente** com as **7.985 entradas** de `axiom_report` no JSON e proof_manifest, sem conflitos, entradas sem suporte ou axiomas fora de `propext`, `Classical.choice`, `Quot.sound`. Os **852 adicionais vêm do build**, inclusive os quatro exemplos `ChatgptAudit.AdmissibleInteraction` apontados pelo autor. O código concatena os dois streams em [um.py:134443](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:134443>) e faz parsing em [um.py:134453](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:134453>)–134461. Não há síntese indevida nem motivo para corrigir o parser. Os 50 resultados sem axiomas e os nomes com apóstrofo continuam reconhecidos.

A comparação inicial da minha evidência entre mapa total e Audit isolado retornou `False`: era comparação entre escopos distintos, não falta de prova. Preservei o resultado e acrescentei [axiom_scope_resolution.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/runtime_seals_preliminary_20260913_100700_656494/axiom_scope_resolution.json>), que resolve a diferença. Os hashes de stdout no proof_manifest coincidem com os streams recuperados da etapa formal aprovada; não confundi hash de captura com hash de stdout.

## P2-01 — montagem: progresso válido reprova uma condição histórica

Em [um.py:155665](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:155665>) exige-se `provadas == 7`; em [um.py:155666](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:155666>), `provadas == total - 1`. A execução mede **8/8 e `flag_lit=True`**, mas ambas condições falham. As linhas 155689–155693 ainda dizem 7/8, oitava devida e bandeira escura. É regressão real do consumidor auxiliar diante da integração, **não regressão das provas**.

Os provedores já disponíveis são `towerJ_add`, `towerJ_conj_smul`, `towerJ_norm`, `towerJ_involutive`, `towerJ_fixes_hOmega`, `J_M_J_in_commutant` e, para a oitava, `qgConverse_JMJ_contains_commutant` com `TGLExt.V350Gate.checkedConverse`. A contagem é de oito cláusulas, não de oito nomes distintos; `towerJ_add` fornece duas entradas do mapeamento legado.

**Correção mínima recomendada, sem implementação nesta revisão:** manter a lista de oito e os demais checks; exigir presença com tipo booleano, primeiras sete provadas e coerência `not bandeira or all(clausulas)`. Acrescentar/reutilizar `v350_frontier_flag_has_proof` para a oitava e o Ato III **quando acesos**. Assim passam tanto 7/8 pendente quanto 8/8 comprovado, mas não uma bandeira acesa com cláusula falsa ou com termo/ponte ausente. Relato e verdict devem distinguir 7/8, 8/8 com bandeira apagada e 8/8 com certificado consumido; “leitura coerente” não significa “dívida quitada”.

A guarda já existe em [gate_extension.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/gate_extension.py>): build válido + Audit rc0 + `all_verified` + termo **e ponte de tipo exato**, ambos no mapa limpo. `checkedConverse : (P : SiteProfile) → ConverseClauseContract P`; `checkedModular` e `checkedActIII : ModularRealizationCertificate`. A construção em `V350ModularCertificate.lean` usa `towerJ mixProfile` e o mesmo certificado. O alcance é **PRODUCT_TOWER**, não uma identificação nova com o J polar do peso/GNS escalar. Não basta homonímia nem dois booleanos `True`.

## P2-02 — Atlas: condição alheia aos seus próprios provedores

Em [um.py:158779](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:158779>) são contadas todas as flags qgf/gpf acesas; [um.py:158798](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:158798>) exige `not _preco`. Nesta rodada há duas: `qgf_modular_realization_constructed` e `gpf_tower_act_III_inhabitant_constructed`. Os **6/6 nomes Atlas + 6/6 nomes Índice passaram**; só a condição global reprova o selo.

**Aceito a proposta de escopo mínimo do autor:** remover essa condição de `all_verified`, conservando `_preco` e `_kernel_import` como diagnósticos. Manter obrigatórias as doze entradas próprias e os checks correspondentes, sem reatribuir flags ou modificar `core`. O módulo verifica Atlas/Índice; a autorização de outras flags pertence ao kernel/frontier. Não substituir o teste por “há exatamente duas acesas”, nem deslocar para este módulo uma guarda global de todos os futuros certificados. O texto deve abandonar “não pagou preço nenhum” como descrição medida do estado global.

O arquivo [consumer_repair_design.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/runtime_seals_preliminary_20260913_100700_656494/consumer_repair_design.json>) registra avaliações próprias de predicados sobre fixtures: montagem aceita 7/8 e 8/8 coerentes; rejeita entrada faltante, flag sem cláusula, ponte removida e `sorryAx`. Atlas rejeita perda de nome próprio e permanece independente de flags alheias. **São validações do desenho proposto, não teste de uma versão corrigida do monólito.** A futura implementação precisa preservar essa distinção.

## P2-03 — insumos da cópia incompletos e efeitos em cascata

`locate_desivast`, [um.py:385](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:385>)–427, procura cache e dois caminhos relativos `TGL_CODE_ONE_REAL_FALSIFIER/release_clean/data/voids/desivast`; a rodada offline não encontrou os REVOLVER. Não classifiquei negação do sandbox como arquivo inexistente: a leitura externa elevada confirmou os provedores documentais. Conferi também os bytes staged, sem instalá-los:

| Insumo staged | Bytes | SHA256 |
|---|---:|---|
| `STOKES_A_Prova_do_Contorno.md` | 5559 | `9dc17cd4cfa67e743f2767200a96e5742e0437a86f98f1a6cc212a2c5cd1eb40` |
| `DESIVAST_BGS_VOLLIM_V2_REVOLVER_NGC.fits` | 611812800 | `08d94b3e1740e154bde865b470c1f1a8d05d6e30ea4800fae2df2f5adec317b8` |
| `DESIVAST_BGS_VOLLIM_V2_REVOLVER_SGC.fits` | 87442560 | `297e51d92b7955d81d68c674af78f43f2bc6c04247f7510c0224d1f81a984ad2` |

Ambos FITS contêm cabeçalhos `VOIDS` e `GALZONE` com as colunas requeridas; só li cabeçalhos e hashes, sem refazer análise científica. O `results.json` existente em `C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/results.json` tem SHA256 `bcb828091d4dff2bc5f6661b1878b4481e4727474bb7596913a99ff0d5c1198f` e `multiprobe_D1_D9.D10.beta_acoustic_crosslock = -0.01696958621339946`. Os dois candidatos consultados pela cópia estavam ausentes no snapshot. Não alterar o requisito de valor negativo: transportar o arquivo existente para um caminho efetivamente lido, com pin.

| Novo item não selado | Causa observada / ligação existente | Correção mínima |
|---|---|---|
| `void_density_opening`, `void_density_v41` | `GALZONE ausente`; ambos só extraem GALZONE dos REVOLVER | Incluir os dois FITS existentes na preparação da próxima cópia; preservar a recusa desta rodada. |
| `void_density_power` | `tabelas ausentes`, na mesma dependência REVOLVER/GALZONE | Mesma correção de insumo. |
| `void_floor_final`, `void_floor_v2` | 438 lentes VIDE e **0 REVOLVER**; checks `n_lens > 500` falham ([um.py:145795](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:145795>), [um.py:146125](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:146125>)) | Restaurar cobertura dos catálogos; não baixar o limiar para fabricar selo. “Mesmos 1049” é ainda rótulo histórico e precisa acompanhar a amostra realmente lida. |
| `void_shear_v2` | 290 vazios, contra 700 na referência; condição `n_voids >= 500` falha em [um.py:151447](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:151447>) | Mesmo insumo faltante. Exibir esse motivo no diagnóstico: os checks impressos passam, mas omitem esse fator de `gates_ok`. Não declarar novo resultado físico por isso. |
| `arc_consolidation` | Cadeia histórica exige `SIGNAL_NOT_OPENED`, `INCONCLUSIVE_SYSTEMATICS` e `NOT_FALSIFIED_POWERED` ([um.py:154360](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:154360>)–154366); faltam as saídas de densidade desta cópia | Reexecutar com insumos completos; não copiar verdict antigo para a saída atual. |
| `closure_roadmap` | Exige `NOT_FALSIFIED_POWERED` de v41 ([um.py:153412](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:153412>)–153432), agora AWAITING_DATA | Mesmo efeito em cascata; não é nova lacuna Lean. |
| `love_reading` | Espera a recusa científica v91, mas recebeu ausência de dado ([um.py:152620](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:152620>)–152630) | Mesma reposição de insumos, mantendo a diferença entre recusa científica e ausência. |
| `stokes_contour` | Só o documento junto ao programa faltou; sete entradas Lean e laboratório passaram ([um.py:6037](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:6037>)–6040, 6096) | Preparar o documento staged no caminho consultado, sem mudar prova ou hash esperado à mão. |
| `evidence_audit` | `fifth_entry_live=None`; procura `BASE/results.json` ou parent/results.json ([um.py:4396](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:4396>)–4418) | Preparar o `results.json` existente e manter `fifth < 0`. Não criar prova/valor substituto. |

O selo classifica por **texto de verdict**, em [um.py:179961](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py:179961>)–179967. Por isso esses nove novos itens da lista “formais” não equivalem a nove provas Lean ausentes: ela inclui documentos/dados faltantes e consumidores históricos. Medição do delta: **4→13** itens nessa lista e **6→10** recusas de dado; nenhum item anterior foi removido. As quatro novas recusas são opening/power/v41/shear_v2. Isso não altera o conjunto das onze entradas principais.

## Disposição e evidência

Preservar esta rodada e suas recusas como executadas. Corrigir a preparação e os **dois consumidores** numa versão posterior sob custódia, usando as pontes existentes e relatos dinâmicos; não retocar `um_absoluto.json` ou selo. A presença dos insumos torna a execução possível, mas não autoriza prever que todos os vereditos científicos serão iguais aos antigos. O aceite da versão corrigida dependerá de seus próprios resultados e testes, sem novo módulo Lean.

Evidência principal: [final_inspection.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/runtime_seals_preliminary_20260913_100700_656494/final_inspection.json>); ajuste de escopo dos axiomas: [axiom_scope_resolution.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/runtime_seals_preliminary_20260913_100700_656494/axiom_scope_resolution.json>); desenho dos consumidores: [consumer_repair_design.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/runtime_seals_preliminary_20260913_100700_656494/consumer_repair_design.json>). Snapshots preliminares e finais, pins, trechos com linhas e scripts de leitura ficam na mesma pasta. O hash do programa e os 13 hashes do selo foram conferidos; não foi feita auditoria científica exaustiva de todos os ritos, nem se executou código corrigido. **Execução integral rc0 está verificada; integração auxiliar sem regressões ainda não está aprovada.**
