# TESTES — R2.2 (conserto ACOM 12/10; copia)

Rodados em 2026-10-13T12:36:56.440346+00:00 com `C:\Python314\python.exe` sobre CÓPIAS do candidato (`testes\`), sob a guarda `sitecustomize.py` da auditoria. Nenhuma chamada a provedor. Resultado medido aqui [REAL]: **18 testes, 18 PASSA, 0 FALHA, 0 pulado(s)** — todas as suítes OK.

| suíte | módulos | rodados | PASSA | FALHA | segundos | OK |
|---|---|---|---|---|---|---|
| R2.2 novos (revisao R2.1 13/10) | test_r2_2 | 15 | 15 | 0 | 11.94 | sim |
| R2.2 app novos (revisao R2.1 13/10) | test_app_r2_2 | 3 | 3 | 0 | 14.76 | sim |

## Cada teste

| suíte | módulo | teste | resultado |
|---|---|---|---|
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_G_N1c_dispatch_init_16000_components_refused_fast` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_G_N1c_ordinary_deep_path_not_refused_by_shape` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_G_N1c_path_reason_16000_components_refused_fast` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_G_N1c_read_allowed_file_16000_components_refused_fast` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_G_N1c_too_long_refused` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_P8b_crash_loop_is_distinguished_in_receipt_and_output` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_P8b_slow_but_stable_is_read_as_slow` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_M_DOC_tools_field_cites_real_sha` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K3r_reverter_cannot_stop_app` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K3r_task_disabled_by_operator_stays_disabled` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K4b2_sem_reiniciar_is_explicit_status_with_action` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K4b_target_locked_after_check_fills_action` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K4c_clean_reversal_still_releases_lock` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K4c_misleading_reverted_receipt_does_not_release_lock` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K4c_target_modified_after_check_is_failure_and_lock_still_pending` | PASSA |
| R2.2 app novos (revisao R2.1 13/10) | `test_app_r2_2` | `test_A_N1_validate_path_16000_components_refused_fast` | PASSA |
| R2.2 app novos (revisao R2.1 13/10) | `test_app_r2_2` | `test_A_N3_hardlink_swap_via_app_never_reads_canary` | PASSA |
| R2.2 app novos (revisao R2.1 13/10) | `test_app_r2_2` | `test_A_OK_benign_read_same_text_as_open` | PASSA |

## Guarda de execução (auditoria)

processos sob guarda nesta rodada: 2; eventos por tipo: `{"GUARD_ON": 2, "CTYPES_DLOPEN": 6, "READ_OUTSIDE": 120}`; bloqueios: 0

