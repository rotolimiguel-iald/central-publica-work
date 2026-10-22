# TESTES R2.1 — conserto ACOM 12/10 (13/10/2026)

Gerado por `scripts/gerar_testes_md.py` a partir dos JSON em disco. Estatutos: [REAL] medido aqui.

## 1. Suíte inteira do candidato R2.1 (cópia `copia\`, guarda da auditoria, sem rede, sem provedor) [REAL]

**259 testes, 259 PASSA, 0 FALHA** (2026-10-13T11:42:54.586867+00:00): as 235 do revisor + 24 novos. Bloqueios da guarda: 2 (`BLOCK_NETWORK`).

| suíte | rodados | OK | segundos |
|---|---|---|---|
| CORE 20 (origem, 1 reescrita D1/D2) | 20 | sim | 1.31 |
| NUCLEO novos 34 (frente 1) | 34 | sim | 96.52 |
| SESSOES 17 (origem) | 17 | sim | 10.12 |
| SESSOES novos 24 (frente 3) | 24 | sim | 10.99 |
| APP 31 (origem, 1 reescrita D3) | 31 | sim | 20.34 |
| APP novos 9 (frente 3) | 9 | sim | 0.87 |
| HEARTBEAT novos 15 (frente 2) | 15 | sim | 26.92 |
| FILA 55 (origem) | 55 | sim | 25.2 |
| FILA novos 5 (frente 3) | 5 | sim | 0.3 |
| BLOCOS 5 (frente 3) | 5 | sim | 0.4 |
| INTEGRACAO novos (esta frente) | 5 | sim | 43.75 |
| R2 novos (achados bloqueantes 13/10) | 15 | sim | 10.84 |
| R2.1 novos (revisao R2 13/10) | 19 | sim | 19.42 |
| R2.1 heartbeat novos (revisao R2 13/10) | 5 | sim | 7.39 |

## 2. Os 24 testes novos: antes (cópia do R2: candidato e ferramentas R2) × depois (R2.1) [REAL]

Antes: 20 de 24 FALHAM no R2 (os 4 que passam são controles). Depois: 24 de 24 PASSAM.

| achado | teste | o que reproduz | R2 | R2.1 |
|---|---|---|---|---|
| N1 | `test_G_N1_basename_32k_under_50ms` | nome de 32 KB (`a` + `.bak`×8000): confidential_basename < 50 ms (melhor de 3) | FALHA | PASSA |
| N1 | `test_G_N1_path_reason_32k_under_50ms` | caminho de 32 KB: path_reason < 50 ms | FALHA | PASSA |
| N1 | `test_G_N1_read_allowed_file_32k_under_50ms` | caminho de 32 KB pelo session_memory.read_allowed_file < 50 ms | FALHA | PASSA |
| N1 | `test_G_N1_same_decision_as_r2_loop` | controle: a remoção linear decide igual ao laço do R2 (3000 nomes aleatórios) | PASSA | PASSA |
| N2 | `test_G_N2_names_refused` | *.env e variantes, radicais psion/stack, homóglifos (ѕ cirílico, ‐, ZWSP, largura total), `~` | FALHA | PASSA |
| N2 | `test_G_N2_benign_names_allowed` | controle: nomes benignos (environment.json, envoy.yaml, venv.txt…) seguem aceitos | PASSA | PASSA |
| N2 | `test_G_N2_init_central_env_refused_and_bank_clean` | init com `central.env` (senha/AKIA sintéticos): recusado, nada no banco | FALHA | PASSA |
| N3 | `test_G_N3_hardlink_swap_never_reads_canary` | troca ativa x.json ↔ hardlink do psion sintético por 12 s: 0 leituras do canário | FALHA | PASSA |
| N3 | `test_G_N3_reads_return_resolved_path` | controle: a leitura devolve o caminho resolvido (como o R2) | PASSA | PASSA |
| K2 | `test_T_K2_refuses_with_unreverted_real_receipt_and_preserves_it` | implantar com recibo real anterior não revertido: RECUSADA, recibo anterior byte a byte intocado, recibo novo com carimbo | FALHA | PASSA |
| K2 | `test_T_K2_reverted_receipt_does_not_block` | com RECIBO_REVERSAO REVERTIDA citando o carimbo, a trava passa | FALHA | PASSA |
| K3 | `test_T_K3_task_reenabled_and_receipt_honest` | stop script não derruba o web: a tarefa volta HABILITADA; o recibo não diz «nada mudou»; estado_real lido | FALHA | PASSA |
| K3 | `test_T_K3_task_disabled_by_operator_stays_disabled` | controle: tarefa desabilitada pelo operador não é reabilitada | PASSA | PASSA |
| K4 | `test_T_K4_failed_restore_does_not_restart_app` | reverter com passo 2 FALHOU: o app NÃO é religado; ação manual no recibo | FALHA | PASSA |
| K4 | `test_T_K4_targets_always_checked_even_without_step4` | recibo sem passo 4 e alvo com bytes do candidato: conferir_alvos FALHOU, sem religar | FALHA | PASSA |
| K4 | `test_T_K4_good_reversal_restarts` | controle: reversão boa restaura e religa; o recibo de reversão cita o carimbo da implantação | FALHA | PASSA |
| K6 | `test_T_K6_receipt_held_by_reader_is_written_after_wait` | leitor segura o recibo 1 s: write_json_atomic espera e grava; sem tempário | FALHA | PASSA |
| K6 | `test_T_K6_held_too_long_fails_visibly_without_orphan_temp` | leitor além do limite: PermissionError visível, alvo intacto, sem tempário | FALHA | PASSA |
| P8 | `test_T_P8_slow_restart_is_waiting_not_failure` | saúde fora do prazo com processo vivo: CONCLUIDA_AGUARDANDO_REINICIO, sem mandar reverter | FALHA | PASSA |
| HB | `test_HB1_psion_replace_waits_for_reader` | psion sintético preso 0,4 s: _save_psion_state espera e grava; sem tempário | FALHA | PASSA |
| HB | `test_HB2_health_replace_waits_for_reader` | health preso 0,4 s: _heartbeat_health_save espera e grava | FALHA | PASSA |
| HB | `test_HB3_failed_replace_leaves_no_orphan_temp` | psion preso além do limite: falha visível, psion intacto, SEM tempário órfão | FALHA | PASSA |
| HB | `test_HB4_rotation_waits_for_reader` | rotação da telemetria com o .jsonl preso: espera e roda | FALHA | PASSA |
| HB | `test_HB5_sixty_beats_with_concurrent_sweeper_one_event` | 60 batidas com varredor em processo (30 ms por arquivo): todas ok, 1 evento, sem tempário | FALHA | PASSA |

## 3. Heartbeat: a repetição s3c do revisor (teste ORIGINAL `test_sixty_beats…`, sem injeção) [REAL]

| cópia | fase | n | falhas do teste | falhas só da limpeza do tempdir no tearDown | aberturas do varredor |
|---|---|---|---|---|---|
| R2 | S_sequencial | 30 | 1 | 0 | None |
| R2 | V_paralelo_4_com_varredor | 60 | 12 | 0 | 1337 |
| R2.1 | S_sequencial | 30 | 0 | 0 | None |
| R2.1 | V_paralelo_4_com_varredor | 60 | 0 | 6 | 1287 |

Mensagens R2: `AssertionError: 'psion_error' != 'ok'`, `AssertionError: 3 != 1`, `PermissionError: [WinError 32] O arquivo já está sendo usado por outro`, `PermissionError: [WinError 5] Acesso negado: '\\\\?\\C:\\IALD\\Central`.
R2.1: as únicas falhas são `PermissionError` no `tempfile.cleanup()` do tearDown da fixture (o varredor externo ainda segura um arquivo do tempdir quando o teste tenta apagá-lo). O corpo do teste passou em todas: 0 `3 != 1`, 0 `psion_error`. Traceback completo em `runs/diag_s3c_copia.json`.

## 4. Filtro: medidas N1/N2 (fora do unittest) [REAL]

| medida | R2 (s) | R2.1 (s) |
|---|---|---|
| basename_bak_x2000 (8001 car.) | 0.0867 | 0.0013 |
| basename_bak_x4000 (16001 car.) | 0.3253 | 0.0022 |
| basename_bak_x8000 (32001 car.) | 1.2985 | 0.0045 |
| basename_bak_x16000 (64001 car.) | 5.1681 | 0.0092 |
| path_reason_32k (32082 car.) | 2.5927 | 0.0194 |
| read_allowed_file_32k (32082 car.) | 2.6056 | 0.0204 |

| nome | R2 | R2.1 |
|---|---|---|
| `central.env` | None | dotenv_name |
| `prod.env` | None | dotenv_name |
| `app.env.local` | None | dotenv_name |
| `secrets.env~` | None | dotenv_name |
| `.env~` | None | dotenv_name |
| `env` | None | dotenv_name |
| `.env` | dotenv_name | dotenv_name |
| `x.env_prod` | None | dotenv_name |
| `.envrc` | None | dotenv_name |
| `iald_psion_\u0455tate.json` | None | psion_name |
| `iald\u2010psion\u2010state.json` | None | psion_name |
| `copia_iald_psion_state_32B.json` | None | psion_name |
| `IALD\u200b_psion_state.json` | None | psion_name |
| `server.key~` | None | key_name |
| `environment.json` | None | None |
| `objetivo.md` | None | None |

## 5. Ensaio de implantação e reversão (cópia sintética, backend simulado, ferramentas R2.1) [REAL]

Script `scripts/s5_ensaio_r2_1.py`; resultado `runs/s5_ensaio_r2_1.json`. O R2 nos mesmos cenários é o do revisor (`8_REVISAO_R2/runs/s5_ensaio_*.json`), não refeito aqui; os testes T_K* da §2 dão o antes/depois por cenário.

| cenário | resultado R2.1 |
|---|---|
| K1a | morto=True, 338 leituras do recibo durante a execução; após a morte: alvos {'original': 15}, schema 2; reverter REVERTIDA; final: originais idênticos=True, banco=original True, lib lê o banco rc=0, sim={'tarefa_habilitada': True, 'sup': 1, 'web': ['2d4f6214fa433534'], 'saude': True} |
| K1b2 | morto=True, — leituras do recibo durante a execução; após a morte: alvos {'candidato': 7, 'original': 8}, schema 2; reverter REVERTIDA; final: originais idênticos=True, banco=original True, lib lê o banco rc=0, sim={'tarefa_habilitada': True, 'sup': 1, 'web': ['2d4f6214fa433534'], 'saude': True} |
| K1c | morto=True, 711 leituras do recibo durante a execução; após a morte: alvos {'candidato': 15}, schema 2; reverter REVERTIDA; final: originais idênticos=True, banco=original True, lib lê o banco rc=0, sim={'tarefa_habilitada': True, 'sup': 1, 'web': ['2d4f6214fa433534'], 'saude': True} |
| K1d | morto=True, 189 leituras do recibo durante a execução; após a morte: alvos {'original': 15}, schema 1; reverter REVERTIDA; final: originais idênticos=True, banco=original True, lib lê o banco rc=0, sim={'tarefa_habilitada': True, 'sup': 1, 'web': ['2d4f6214fa433534'], 'saude': True} |
| K2 | 1ª: FALHOU_EM_substituir_arquivos (alvos {'candidato': 14, 'original': 1}); 2ª: RECUSADA_RECIBO_ANTERIOR_NAO_REVERTIDO, passos {'trava_recibo_anterior': 'FALHOU'}, recibo 1 intocado=True; reverter com o recibo indicado: REVERTIDA; dry-run depois: trava OK, DRY_RUN_OK; final: originais idênticos=True, banco=original True, lib lê o banco rc=0, sim={'tarefa_habilitada': True, 'sup': 1, 'web': ['2d4f6214fa433534'], 'saude': True} |
| K3 | FALHOU_EM_parar_app; tarefa desabilitada por esta execução=True; reabilitada={'cmdlet': 'Enable-ScheduledTask (simulado)'}; diz «nada mudou»=False; sim depois={'tarefa_habilitada': True, 'sup': 0, 'web': ['2d4f6214fa433534'], 'saude': True}; nota: arquivos e banco intocados; a tarefa agendada FOI desabilitada por esta execução e foi reabilitada; o app pode ter ficado PARCIALMENTE parado (ver estado_real) |
| K4 | implantar CONCLUIDA; reverter com o web server preso: FALHOU_EM_restaurar_arquivos, app_religado=False, sim={'tarefa_habilitada': False, 'sup': 0, 'web': [], 'saude': False}, alvos {'candidato': 8, 'original': 7}; 2º reverter: REVERTIDA, alvos {'original': 15}, sim={'tarefa_habilitada': True, 'sup': 1, 'web': ['2d4f6214fa433534'], 'saude': True}; final: originais idênticos=True, banco=original True, lib lê o banco rc=0, sim={'tarefa_habilitada': True, 'sup': 1, 'web': ['2d4f6214fa433534'], 'saude': True} |
| K5 | implantar CONCLUIDA; reverter morto=True (alvos {'candidato': 8, 'ausente': 1, 'original': 6}); 2º reverter REVERTIDA, alvos {'original': 15}; final: originais idênticos=True, banco=original True, lib lê o banco rc=0, sim={'tarefa_habilitada': True, 'sup': 1, 'web': ['2d4f6214fa433534'], 'saude': True} |
| K6 | leitor segurou o recibo 2 s=True; implantar CONCLUIDA (15 arquivos substituídos), sim={'tarefa_habilitada': True, 'sup': 1, 'web': ['b213498dabb3f7e6'], 'saude': True}; reverter REVERTIDA; final: originais idênticos=True, banco=original True, lib lê o banco rc=0, sim={'tarefa_habilitada': True, 'sup': 1, 'web': ['2d4f6214fa433534'], 'saude': True} |
| P8 | implantar CONCLUIDA_AGUARDANDO_REINICIO (passo 8 AGUARDANDO_REINICIO), manda reverter=False; sim logo após={'tarefa_habilitada': True, 'sup': 1, 'web': ['b213498dabb3f7e6'], 'saude': False}; 10 s depois={'tarefa_habilitada': True, 'sup': 1, 'web': ['b213498dabb3f7e6'], 'saude': True}; reversão de limpeza: REVERTIDA_AGUARDANDO_REINICIO |

## 6. Arquivos dos testes (sha256 lido)

- `src_r2_1\hb\test_heartbeat_r2_1.py` `c82fef47d1c7d620`
- `src_r2_1\test_r2_1.py` `db97c2b2acf22374`
