# TESTES R2.2 — conserto ACOM 12/10 (13/10/2026)

Gerado por `scripts/gerar_testes_md.py` a partir dos JSON em disco. Estatutos: [REAL] medido aqui.

## 1. Suíte inteira do candidato R2.2 (cópia `copia\`, guarda da auditoria, sem rede, sem provedor) [REAL]

**278 testes, 278 PASSA, 0 FALHA** (2026-10-13T13:09:17.927674+00:00): as 259 da R2.1 + 19 novos. Bloqueios da guarda: 3 (`BLOCK_NETWORK`).

| suíte | rodados | OK | segundos |
|---|---|---|---|
| CORE 20 (origem, 1 reescrita D1/D2) | 20 | sim | 1.26 |
| NUCLEO novos 34 (frente 1) | 34 | sim | 98.16 |
| SESSOES 17 (origem) | 17 | sim | 9.5 |
| SESSOES novos 24 (frente 3) | 24 | sim | 9.85 |
| APP 31 (origem, 1 reescrita D3) | 31 | sim | 20.38 |
| APP novos 9 (frente 3) | 9 | sim | 0.79 |
| HEARTBEAT novos 15 (frente 2) | 15 | sim | 27.93 |
| FILA 55 (origem) | 55 | sim | 25.21 |
| FILA novos 5 (frente 3) | 5 | sim | 0.29 |
| BLOCOS 5 (frente 3) | 5 | sim | 0.37 |
| INTEGRACAO novos (esta frente) | 5 | sim | 44.46 |
| R2 novos (achados bloqueantes 13/10) | 15 | sim | 11.22 |
| R2.1 novos (revisao R2 13/10) | 19 | sim | 19.41 |
| R2.1 heartbeat novos (revisao R2 13/10) | 5 | sim | 7.44 |
| R2.2 novos (revisao R2.1 13/10) | 16 | sim | 16.23 |
| R2.2 app novos (revisao R2.1 13/10) | 3 | sim | 14.83 |

## 2. Os testes novos: antes (cópia `copia_r2_1`: candidato e ferramentas R2.1) × depois (R2.2) [REAL]

Antes: 15 de 19 FALHAM na R2.1 (os que passam são controles). Depois: 19 de 19 PASSAM.

| achado | teste | o que reproduz | R2.1 | R2.2 |
|---|---|---|---|---|
| K3r | `test_T_K3r_reverter_cannot_stop_app` | o REVERTER não consegue parar o app: nada restaurado, tarefa reabilitada, recibo com estado lido (vivo sem supervisor), nunca «fica parado» | FALHA | PASSA |
| K3r | `test_T_K3r_task_disabled_by_operator_stays_disabled` | controle: tarefa desabilitada pelo operador segue desabilitada | PASSA | PASSA |
| K4b | `test_T_K4b2_sem_reiniciar_is_explicit_status_with_action` | --sem-reiniciar: REVERTIDA_SEM_RELIGAR com a ação manual | FALHA | PASSA |
| K4b | `test_T_K4b_target_locked_after_check_fills_action` | lock EXCLUSIVO num alvo depois de conferir_alvos OK: ação preenchida (nunca null), sem religar, trava pendente | FALHA | PASSA |
| K4c | `test_T_K4c_clean_reversal_still_releases_lock` | controle: reversão boa dá REVERTIDA, ok, app_religado true, ação null, trava libera | PASSA | PASSA |
| K4c | `test_T_K4c_misleading_reverted_receipt_does_not_release_lock` | um RECIBO_REVERSAO REVERTIDA com app_religado=false não libera a trava | FALHA | PASSA |
| K4c | `test_T_K4c_target_modified_after_check_is_failure_and_lock_still_pending` | alvo com bytes do candidato depois de conferir_alvos OK: status FALHOU_EM_*, ok=false, sem religar, ação preenchida, trava ainda vê a implantação pendente | FALHA | PASSA |
| N1 | `test_G_N1c_dispatch_init_16000_components_refused_fast` | dispatch init com 16.000 componentes: recusa visível em < 50 ms | FALHA | PASSA |
| N1 | `test_G_N1c_ordinary_deep_path_not_refused_by_shape` | controle: 40 componentes benignos não são recusados | PASSA | PASSA |
| N1 | `test_G_N1c_path_reason_16000_components_refused_fast` | path_reason com 16.000 componentes: path_too_many_components em < 50 ms | FALHA | PASSA |
| N1 | `test_G_N1c_read_allowed_file_16000_components_refused_fast` | read_allowed_file com 16.000 componentes: recusa visível em < 50 ms | FALHA | PASSA |
| N1 | `test_G_N1c_too_long_refused` | caminho de 40.000 caracteres: path_too_long (a R2.1 levantava ValueError do stat) | FALHA | PASSA |
| N1 app | `test_A_N1_validate_path_16000_components_refused_fast` | agi_validate_path com 16.000 componentes: recusa em < 50 ms | FALHA | PASSA |
| N3 app | `test_A_N3_hardlink_swap_via_app_never_reads_canary` | troca ativa x.json <-> hardlink do psion sintético por 12 s pelo handler real /admin/api/agi/files/read: 0 leituras do canário | FALHA | PASSA |
| N3 app | `test_A_OK_benign_read_same_text_as_open` | controle: leitura benigna devolve o mesmo texto que open(...,"r") e recusa o psion sintético | PASSA | PASSA |
| P8b | `test_T_P8b_child_never_up_is_crash_loop` | filho web nunca de pé com supervisor vivo: rc 3, LACO_DE_QUEDA_PROVAVEL (forma achada no ensaio) | FALHA | PASSA |
| P8b | `test_T_P8b_crash_loop_is_distinguished_in_receipt_and_output` | filho web com pid trocando: rc 3, LACO_DE_QUEDA_PROVAVEL no recibo e na saída, COMO DISTINGUIR | FALHA | PASSA |
| P8b | `test_T_P8b_slow_but_stable_is_read_as_slow` | pid estável: rc 3, LENTO_PROVAVEL, «NÃO reverter» | FALHA | PASSA |
| doc | `test_M_DOC_tools_field_cites_real_sha` | campo ferramentas do manifesto cita o sha256 real do aplicar_blocos.py | FALHA | PASSA |

Rodada da R2.1: `copia_r2_1/testes_r2/RESULTADOS_TESTES_parcial.json` (2026-10-13T13:04:09.575920+00:00).

## 3. Ensaio de implantação e reversão (backend de processos SIMULADO, banco v1 sintético, guarda ligada) [REAL]

Arquivo `runs/s5_ensaio_r2_2.json` (sha16 `1bd579acfebccdc2`), ferramentas R2.2 copiadas byte a byte (preparo: {"implantar.py": "11104b0e2dd8f80d", "reverter.py": "62f212555a845e1a", "implantacao_lib.py": "3f42bf41edf2c6d0"}).

| cenário | resultado principal | originais idênticos no fim | banco = original | lib v1 lê | tmp órfão |
|---|---|---|---|---|---|
| K1a | {"alvos_apos_morte": {"original": 15}, "reverter_status": "REVERTIDA", "reverter_rc": 0, "reverter_app_religado": true, "alvos_apos_reverter": {"original": 15}} | True | True | True | 1 |
| K1b2 | {"alvos_apos_morte": {"candidato": 7, "original": 8}, "reverter_status": "REVERTIDA", "reverter_rc": 0, "reverter_app_religado": true, "alvos_apos_reverter": {"original": 15}} | True | True | True | 1 |
| K1c | {"alvos_apos_morte": {"candidato": 15}, "reverter_status": "REVERTIDA", "reverter_rc": 0, "reverter_app_religado": true, "alvos_apos_reverter": {"original": 15}} | True | True | True | 0 |
| K1d | {"alvos_apos_morte": {"original": 15}, "reverter_status": "REVERTIDA", "reverter_rc": 0, "reverter_app_religado": true, "alvos_apos_reverter": {"original": 15}} | True | True | True | 0 |
| K2 | {"alvos_apos_1": {"candidato": 14, "original": 1}, "implantar_2_status": "RECUSADA_RECIBO_ANTERIOR_NAO_REVERTIDO", "implantar_2_rc": 1, "alvos_apos_2": {"candidato": 14, "original": 1}, "reverter_com_o_recibo_indicado_status": "REVERTIDA", "reverter_com_o_recibo_indicado_rc": 0, "reverter_com_o_recibo_indicado_app_religado": true, "alvos_apos_reverter": {"original": 15}, "dry_run_depois_de_revertida_status": "DRY_RUN | True | True | True | 0 |
| K3 | {"implantar_status": "FALHOU_EM_parar_app", "implantar_rc": 1, "alvos": {"original": 15}} | True | True | True | 0 |
| K4 | {"implantar_status": "CONCLUIDA", "implantar_rc": 0, "reverter_status": "FALHOU_EM_restaurar_arquivos", "reverter_rc": 1, "reverter_app_religado": false, "alvos_apos_reverter_com_falha": {"candidato": 8, "original": 7}, "reverter_de_novo_status": "REVERTIDA", "reverter_de_novo_rc": 0, "reverter_de_novo_app_religado": true, "alvos_apos_2o_reverter": {"original": 15}} | True | True | True | 0 |
| K5 | {"implantar_status": "CONCLUIDA", "implantar_rc": 0, "alvos_apos_morte": {"candidato": 8, "ausente": 1, "original": 6}, "reverter_2_status": "REVERTIDA", "reverter_2_rc": 0, "reverter_2_app_religado": true, "alvos_apos_reverter_2": {"original": 15}} | True | True | True | 0 |
| K6 | {"implantar_status": "CONCLUIDA", "implantar_rc": 0, "alvos_apos": {"candidato": 15}, "reverter_status": "REVERTIDA", "reverter_rc": 0, "reverter_app_religado": true, "alvos_apos_reverter": {"original": 15}} | True | True | True | 0 |
| P8 | {"implantar_rc": 3, "implantar_status": "CONCLUIDA_AGUARDANDO_REINICIO", "leitura": "LENTO", "tem_como_distinguir": true, "manda_reverter": false, "sim_10s_depois": {"tarefa_habilitada": true, "sup": 1, "web": ["b213498dabb3f7e6"], "saude": true}, "reverter_final": "REVERTIDA_AGUARDANDO_REINICIO"} | True | True | True | 0 |
| K2b | {"implantar_1_status": "FALHOU_EM_substituir_arquivos", "implantar_1_rc": 1, "alvos_apos_1": {"candidato": 14, "original": 1}, "implantar_2_status": "FALHOU_EM_pre_conferencias", "implantar_2_rc": 1, "alvos_apos_2": {"candidato": 14, "original": 1}, "reverter_config_status": null, "reverter_config_rc": 1, "alvos_apos_reverter_config": {"candidato": 14, "original": 1}} | False | False | True | 0 |
| K2c | {"implantar_1_status": "FALHOU_EM_substituir_arquivos", "implantar_1_rc": 1, "alvos_apos_1": {"candidato": 14, "original": 1}, "implantar_2_status": "FALHOU_EM_pre_conferencias", "implantar_2_rc": 1, "alvos_apos_2": {"candidato": 14, "original": 1}, "reverter_config_status": null, "reverter_config_rc": 1, "alvos_apos_reverter_config": {"candidato": 14, "original": 1}} | False | False | True | 0 |
| K2d | {"implantar_1_status": "FALHOU_EM_substituir_arquivos", "implantar_1_rc": 1, "alvos_apos_1": {"candidato": 14, "original": 1}, "implantar_2_status": "RECUSADA_RECIBO_ANTERIOR_NAO_REVERTIDO", "implantar_2_rc": 1, "alvos_apos_2": {"candidato": 14, "original": 1}, "reverter_config_status": null, "reverter_config_rc": 1, "alvos_apos_reverter_config": {"candidato": 14, "original": 1}} | False | False | True | 0 |
| K3b | {"implantar_status": "FALHOU_EM_parar_app", "implantar_rc": 1, "alvos": {"original": 15}} | True | True | True | 0 |
| K3r | {"reverter_k3_status": "FALHOU_EM_parar_app", "reverter_k3_rc": 1, "diz_fica_parado": false, "sim_apos_reverter_k3": {"tarefa_habilitada": true, "sup": 0, "web": ["b213498dabb3f7e6"], "saude": true}, "alvos_apos_reverter_k3": {"candidato": 15}, "reverter_normal_status": "REVERTIDA", "promessa_tarefa_reabilitada_e_estado_lido": true} | True | True | True | 0 |
| K4b | {"reverter_1_status": "FALHOU_EM_reiniciar_app", "reverter_1_rc": 1, "reverter_1_acao_requerida": "O app NÃO foi religado por esta reversão (falhas: ['reiniciar_app', 'conferencia_final']). Estado LIDO agora: tarefa agendada DESABILITADA (Disabled); 0 supervisor(es), 0 filho(s) web, 0 processo(s) escutando a porta; o app está PARADO (lido em 2026-10-13T13:00:41.557322+00:00). Remova a causa (ver ", "trava_ve_pendente | True | True | True | 0 |
| K4c | {"reverter_1_status": "FALHOU_EM_reiniciar_app", "reverter_1_rc": 1, "reverter_1_acao_feita": true, "reverter_1_app_religado": false, "reverter_1_falhas": ["reiniciar_app", "conferencia_final"], "reverter_1_tem_acao": true, "trava_ve_pendente": {"pendentes": ["RECIBO_IMPLANTACAO_20261013_100047_478545.json"], "ilegiveis": 0}, "reverter_2_status": "REVERTIDA", "promessa_nunca_REVERTIDA_e_trava_pendente": true} | True | True | True | 0 |
| K6b | {"implantar_status": "CONCLUIDA", "implantar_rc": 0, "alvos": {"candidato": 15}, "reverter_status": "REVERTIDA", "reverter_rc": 0, "reverter_app_religado": true, "alvos_apos_reverter": {"original": 15}} | True | True | True | 0 |
| K6c | {"implantar_status": "FALHOU_EM_substituir_arquivos", "implantar_rc": 1, "alvos": {"candidato": 5, "original": 10}, "reverter_status": "REVERTIDA", "reverter_rc": 0, "reverter_app_religado": true, "alvos_apos_reverter": {"original": 15}} | True | True | True | 0 |
| P8b | {"implantar_rc": 3, "implantar_status": "CONCLUIDA_AGUARDANDO_REINICIO", "leitura": "LACO", "tem_como_distinguir": true, "manda_reverter": true, "sim_10s_depois": null, "reverter_final": "REVERTIDA"} | True | True | True | 0 |
| CFG | {"dry_run_antes": {"rc": 0, "stdout": "son\", \"acao_requerida\": null, \"passos\": {\"trava_recibo_anterior\": \"OK\", \"pre_conferencias\": \"OK\", \"parar_app\": \"OK\", \"backup_integral\": \"OK\", \"migracao\": \"OK\", \"substituir_arquivos\": \"OK\", \"aplicar_blocos\": \"OK\", \"mover_backups_antigos\": \"OK\", \"verificacao_final\": \"OK\", \"reiniciar_app\": \"PULADO\"}}\r\n"}, "implantar": {"rc": 0, "status | True | True | True | 0 |

Leitura [REAL, dos JSON]:

- «tmp órfão» conta os tempários de uma troca interrompida pela morte do processo (K1a/K1b2), que o reverter RENOMEOU para `.removido_` (nunca apaga); nenhum `.tmp_` solto ficou.
- K2b/K2c/K2d terminam com o estado misto porque o cenário do revisor só tenta `reverter --config` depois de o operador renomear, apagar ou truncar o recibo: a trava não vê o recibo renomeado/apagado e recusa o truncado; a 2ª execução do implantar falha fechada sem tocar em nada. É a regra «nunca renomear, apagar ou editar recibo» (RUNBOOK §6); igual à R2.1 (revisão R2.1 §4).
- P8: a reversão de limpeza do ensaio também encontra a saúde atrasada (o simulador mantém o atraso de 8 s e o prazo de 3 s) e termina REVERTIDA_AGUARDANDO_REINICIO, com a ação preenchida.
- A 1ª rodada completa do ensaio (`runs/s5_ensaio_r2_2_rodada1_bug_P8b.json`) achou um defeito da própria R2.2: no P8b com o filho web que nunca fica de pé, o texto do diagnóstico levantava UnboundLocalError e a implantação verificada saía como falha (rc 1). Corrigido (ramo do texto e proteção: o texto nunca transforma implantação verificada em falha), com o teste `test_T_P8b_child_never_up_is_crash_loop`; a rodada acima é a 2ª, completa.
