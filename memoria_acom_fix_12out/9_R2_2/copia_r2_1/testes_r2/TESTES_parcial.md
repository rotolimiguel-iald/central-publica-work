# TESTES — R2.2 (conserto ACOM 12/10; copia_r2_1)

Rodados em 2026-10-13T13:04:09.575920+00:00 com `C:\Python314\python.exe` sobre CÓPIAS do candidato (`testes\`), sob a guarda `sitecustomize.py` da auditoria. Nenhuma chamada a provedor. Resultado medido aqui [REAL]: **19 testes, 4 PASSA, 15 FALHA, 0 pulado(s)** — HÁ SUÍTE COM FALHA.

| suíte | módulos | rodados | PASSA | FALHA | segundos | OK |
|---|---|---|---|---|---|---|
| R2.2 novos (revisao R2.1 13/10) | test_r2_2 | 16 | 3 | 13 | 25.5 | NÃO |
| R2.2 app novos (revisao R2.1 13/10) | test_app_r2_2 | 3 | 1 | 2 | 27.15 | NÃO |

## Cada teste

| suíte | módulo | teste | resultado |
|---|---|---|---|
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_G_N1c_dispatch_init_16000_components_refused_fast` | FALHA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_G_N1c_ordinary_deep_path_not_refused_by_shape` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_G_N1c_path_reason_16000_components_refused_fast` | FALHA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_G_N1c_read_allowed_file_16000_components_refused_fast` | FALHA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_G_N1c_too_long_refused` | FALHA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_P8b_child_never_up_is_crash_loop` | FALHA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_P8b_crash_loop_is_distinguished_in_receipt_and_output` | FALHA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_P8b_slow_but_stable_is_read_as_slow` | FALHA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_M_DOC_tools_field_cites_real_sha` | FALHA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K3r_reverter_cannot_stop_app` | FALHA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K3r_task_disabled_by_operator_stays_disabled` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K4b2_sem_reiniciar_is_explicit_status_with_action` | FALHA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K4b_target_locked_after_check_fills_action` | FALHA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K4c_clean_reversal_still_releases_lock` | PASSA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K4c_misleading_reverted_receipt_does_not_release_lock` | FALHA |
| R2.2 novos (revisao R2.1 13/10) | `test_r2_2` | `test_T_K4c_target_modified_after_check_is_failure_and_lock_still_pending` | FALHA |
| R2.2 app novos (revisao R2.1 13/10) | `test_app_r2_2` | `test_A_N1_validate_path_16000_components_refused_fast` | FALHA |
| R2.2 app novos (revisao R2.1 13/10) | `test_app_r2_2` | `test_A_N3_hardlink_swap_via_app_never_reads_canary` | FALHA |
| R2.2 app novos (revisao R2.1 13/10) | `test_app_r2_2` | `test_A_OK_benign_read_same_text_as_open` | PASSA |

## Guarda de execução (auditoria)

processos sob guarda nesta rodada: 2; eventos por tipo: `{"GUARD_ON": 2, "READ_OUTSIDE": 120, "CTYPES_DLOPEN": 6}`; bloqueios: 0


## Saída da suíte com falha: R2.2 novos (revisao R2.1 13/10)

```
L: test_T_K4b2_sem_reiniciar_is_explicit_status_with_action (test_r2_2.ReverterK4b.test_T_K4b2_sem_reiniciar_is_explicit_status_with_action)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\copia_r2_1\testes_r2\suite\r2_2\test_r2_2.py", line 308, in test_T_K4b2_sem_reiniciar_is_explicit_status_with_action
    self.assertEqual(out['status'], 'REVERTIDA_SEM_RELIGAR', out)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'REVERTIDA' != 'REVERTIDA_SEM_RELIGAR'
- REVERTIDA
+ REVERTIDA_SEM_RELIGAR
 : {'ok': True, 'status': 'REVERTIDA', 'recibo': 'C:\\IALD\\Central de Patentes\\work\\memoria_acom_fix_12out\\9_R2_2\\copia_r2_1\\tmp\\run\\tmpnow8w3f2\\recibos\\RECIBO_REVERSAO_20261013_100341_463020.json', 'falhas': [], 'app_religado': False, 'acao_requerida': None, 'passos': {'parar_app': 'OK', 'restaurar_arquivos': 'OK', 'conferir_alvos': 'OK', 'restaurar_banco': 'PULADO', 'restaurar_blocos': 'PULADO', 'backups_legados': 'PULADO', 'reiniciar_app': 'PULADO'}}

======================================================================
FAIL: test_T_K4b_target_locked_after_check_fills_action (test_r2_2.ReverterK4b.test_T_K4b_target_locked_after_check_fills_action)
Cenário do revisor: lock EXCLUSIVO num alvo depois de conferir_alvos OK: a conferência antes de religar
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\copia_r2_1\testes_r2\suite\r2_2\test_r2_2.py", line 297, in test_T_K4b_target_locked_after_check_fills_action
    self.assertTrue(out.get('acao_requerida'), 'acao_requerida null com o app não religado')
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: None is not true : acao_requerida null com o app não religado

======================================================================
FAIL: test_T_K4c_misleading_reverted_receipt_does_not_release_lock (test_r2_2.ReverterK4c.test_T_K4c_misleading_reverted_receipt_does_not_release_lock)
Um RECIBO_REVERSAO REVERTIDA com app_religado=false (o que a R2.1 gravava no K4c) não prova reversão.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\copia_r2_1\testes_r2\suite\r2_2\test_r2_2.py", line 261, in test_T_K4c_misleading_reverted_receipt_does_not_release_lock
    self.assertEqual(pendentes(rd), ['RECIBO_IMPLANTACAO_X.json'])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: [] != ['RECIBO_IMPLANTACAO_X.json']

Second list contains 1 additional elements.
First extra element 0:
'RECIBO_IMPLANTACAO_X.json'

- []
+ ['RECIBO_IMPLANTACAO_X.json']

======================================================================
FAIL: test_T_K4c_target_modified_after_check_is_failure_and_lock_still_pending (test_r2_2.ReverterK4c.test_T_K4c_target_modified_after_check_is_failure_and_lock_still_pending)
Cenário do revisor: alvo com os bytes do candidato DEPOIS de conferir_alvos OK, antes de religar.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\copia_r2_1\testes_r2\suite\r2_2\test_r2_2.py", line 241, in test_T_K4c_target_modified_after_check_is_failure_and_lock_still_pending
    self.assertNotEqual(out['status'], 'REVERTIDA', out)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'REVERTIDA' == 'REVERTIDA' : {'ok': True, 'status': 'REVERTIDA', 'recibo': 'C:\\IALD\\Central de Patentes\\work\\memoria_acom_fix_12out\\9_R2_2\\copia_r2_1\\tmp\\run\\tmpzo7bqzjm\\recibos\\RECIBO_REVERSAO_20261013_100342_174232.json', 'falhas': [], 'app_religado': False, 'acao_requerida': 'O app NÃO foi religado (estado possivelmente misto: [\'alvos_divergentes:1\']). Ele fica parado e a tarefa agendada desabilitada. Remova a causa (ver os passos FALHOU e a mensagem; ex.: arquivo preso por outro processo) e rode de novo: python -X utf8 "C:\\IALD\\Central de Patentes\\work\\memoria_acom_fix_12out\\9_R2_2\\ref_r2_1\\reverter.py" --recibo "C:\\IALD\\Central de Patentes\\work\\memoria_acom_fix_12out\\9_R2_2\\copia_r2_1\\tmp\\run\\tmpzo7bqzjm\\recibos\\RECIBO_IMPLANTACAO_SINTETICO.json" . Só religue sobre este estado por decisão explícita: o mesmo comando com --forcar-reinicio.', 'passos': {'parar_app': 'OK', 'restaurar_arquivos': 'OK', 'conferir_alvos': 'OK', 'restaurar_banco': 'PULADO', 'restaurar_blocos': 'PULADO', 'backups_legados': 'PULADO', 'reiniciar_app': 'NAO_EXECUTADO'}}

----------------------------------------------------------------------
Ran 16 tests in 25.277s

FAILED (failures=12, errors=1)

```

## Saída da suíte com falha: R2.2 app novos (revisao R2.1 13/10)

```
test_A_N1_validate_path_16000_components_refused_fast (test_app_r2_2.AppR22.test_A_N1_validate_path_16000_components_refused_fast) ... FAIL
test_A_N3_hardlink_swap_via_app_never_reads_canary (test_app_r2_2.AppR22.test_A_N3_hardlink_swap_via_app_never_reads_canary) ... 
[A_N3] trocas=1903 {"canario": 294, "benigno": 704, "recusa": 1754, "outros": 5430}
FAIL
test_A_OK_benign_read_same_text_as_open (test_app_r2_2.AppR22.test_A_OK_benign_read_same_text_as_open) ... ok

======================================================================
FAIL: test_A_N1_validate_path_16000_components_refused_fast (test_app_r2_2.AppR22.test_A_N1_validate_path_16000_components_refused_fast)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\copia_r2_1\testes_r2\suite\app\test_app_r2_2.py", line 133, in test_A_N1_validate_path_16000_components_refused_fast
    self.assertLess(dt, 0.05, 'agi_validate_path levou %.3f s' % dt)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 11.91780410001229 not less than 0.05 : agi_validate_path levou 11.918 s

======================================================================
FAIL: test_A_N3_hardlink_swap_via_app_never_reads_canary (test_app_r2_2.AppR22.test_A_N3_hardlink_swap_via_app_never_reads_canary)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\copia_r2_1\testes_r2\suite\app\test_app_r2_2.py", line 125, in test_A_N3_hardlink_swap_via_app_never_reads_canary
    self.assertEqual(lidos['canario'], 0, 'o app devolveu o canário por um caminho de nome benigno')
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 294 != 0 : o app devolveu o canário por um caminho de nome benigno

----------------------------------------------------------------------
Ran 3 tests in 26.969s

FAILED (failures=2)

```
