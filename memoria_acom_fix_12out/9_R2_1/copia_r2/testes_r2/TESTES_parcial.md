# TESTES — R2.1 (conserto ACOM 12/10; copia_r2)

Rodados em 2026-10-13T11:17:10.537017+00:00 com `C:\Python314\python.exe` sobre CÓPIAS do candidato (`testes\`), sob a guarda `sitecustomize.py` da auditoria. Nenhuma chamada a provedor. Resultado medido aqui [REAL]: **24 testes, 4 PASSA, 20 FALHA, 0 pulado(s)** — HÁ SUÍTE COM FALHA.

| suíte | módulos | rodados | PASSA | FALHA | segundos | OK |
|---|---|---|---|---|---|---|
| R2.1 novos (revisao R2 13/10) | test_r2_1 | 19 | 4 | 15 | 48.03 | NÃO |
| R2.1 heartbeat novos (revisao R2 13/10) | test_heartbeat_r2_1 | 5 | 0 | 5 | 4.66 | NÃO |

## Cada teste

| suíte | módulo | teste | resultado |
|---|---|---|---|
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_T_K2_refuses_with_unreverted_real_receipt_and_preserves_it` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_T_K2_reverted_receipt_does_not_block` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_T_K3_task_disabled_by_operator_stays_disabled` | PASSA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_T_K3_task_reenabled_and_receipt_honest` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_T_K4_failed_restore_does_not_restart_app` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_T_K4_good_reversal_restarts` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_T_K4_targets_always_checked_even_without_step4` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_T_K6_held_too_long_fails_visibly_without_orphan_temp` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_T_K6_receipt_held_by_reader_is_written_after_wait` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_T_P8_slow_restart_is_waiting_not_failure` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_G_N1_basename_32k_under_50ms` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_G_N1_path_reason_32k_under_50ms` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_G_N1_read_allowed_file_32k_under_50ms` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_G_N1_same_decision_as_r2_loop` | PASSA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_G_N2_benign_names_allowed` | PASSA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_G_N2_init_central_env_refused_and_bank_clean` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_G_N2_names_refused` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_G_N3_hardlink_swap_never_reads_canary` | FALHA |
| R2.1 novos (revisao R2 13/10) | `test_r2_1` | `test_G_N3_reads_return_resolved_path` | PASSA |
| R2.1 heartbeat novos (revisao R2 13/10) | `test_heartbeat_r2_1` | `test_HB1_psion_replace_waits_for_reader` | FALHA |
| R2.1 heartbeat novos (revisao R2 13/10) | `test_heartbeat_r2_1` | `test_HB2_health_replace_waits_for_reader` | FALHA |
| R2.1 heartbeat novos (revisao R2 13/10) | `test_heartbeat_r2_1` | `test_HB3_failed_replace_leaves_no_orphan_temp` | FALHA |
| R2.1 heartbeat novos (revisao R2 13/10) | `test_heartbeat_r2_1` | `test_HB4_rotation_waits_for_reader` | FALHA |
| R2.1 heartbeat novos (revisao R2 13/10) | `test_heartbeat_r2_1` | `test_HB5_sixty_beats_with_concurrent_sweeper_one_event` | FALHA |

## Guarda de execução (auditoria)

processos sob guarda nesta rodada: 2; eventos por tipo: `{"GUARD_ON": 2, "READ_OUTSIDE": 66, "CTYPES_DLOPEN": 1, "BLOCK_NETWORK": 1}`; bloqueios: 1

- BLOQUEIO: `{"kind": "BLOCK_NETWORK", "event": "socket.bind", "path": null, "src": null, "dst": null, "args": "(<socket.socket fd=216, family=23, type=1, proto=0>, ('::1', 0))", "mode": null}`

## Saída da suíte com falha: R2.1 novos (revisao R2 13/10)

```
.assertEqual(rec['status'], 'CONCLUIDA_AGUARDANDO_REINICIO')
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'FALHOU_EM_reiniciar_app' != 'CONCLUIDA_AGUARDANDO_REINICIO'
- FALHOU_EM_reiniciar_app
+ CONCLUIDA_AGUARDANDO_REINICIO


======================================================================
FAIL: test_G_N1_basename_32k_under_50ms (test_r2_1.GuardN1Linear.test_G_N1_basename_32k_under_50ms)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\suite\r2_1\test_r2_1.py", line 76, in test_G_N1_basename_32k_under_50ms
    self.assertLess(dt, 0.05, 'confidential_basename(32 KB) levou %.3f s' % dt)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1.953310099997907 not less than 0.05 : confidential_basename(32 KB) levou 1.953 s

======================================================================
FAIL: test_G_N1_path_reason_32k_under_50ms (test_r2_1.GuardN1Linear.test_G_N1_path_reason_32k_under_50ms)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\suite\r2_1\test_r2_1.py", line 81, in test_G_N1_path_reason_32k_under_50ms
    self.assertLess(dt, 0.05, 'path_reason(32 KB) levou %.3f s' % dt)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 3.929210799993598 not less than 0.05 : path_reason(32 KB) levou 3.929 s

======================================================================
FAIL: test_G_N1_read_allowed_file_32k_under_50ms (test_r2_1.GuardN1Linear.test_G_N1_read_allowed_file_32k_under_50ms)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\suite\r2_1\test_r2_1.py", line 92, in test_G_N1_read_allowed_file_32k_under_50ms
    self.assertLess(dt, 0.05, 'read_allowed_file(32 KB) levou %.3f s' % dt)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 4.180946899999981 not less than 0.05 : read_allowed_file(32 KB) levou 4.181 s

======================================================================
FAIL: test_G_N2_init_central_env_refused_and_bank_clean (test_r2_1.GuardN2Names.test_G_N2_init_central_env_refused_and_bank_clean)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\suite\r2_1\test_r2_1.py", line 148, in test_G_N2_init_central_env_refused_and_bank_clean
    with self.assertRaises(sm.ProtocolError) as cm:
         ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
AssertionError: ProtocolError not raised

======================================================================
FAIL: test_G_N2_names_refused (test_r2_1.GuardN2Names.test_G_N2_names_refused)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\suite\r2_1\test_r2_1.py", line 129, in test_G_N2_names_refused
    self.assertEqual(faltando, [], 'nomes que passaram no filtro')
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: ['central.env', 'prod.env', 'app.env.local[221 chars].py'] != []

First list contains 15 additional elements.
First extra element 0:
'central.env'

+ []
- ['central.env',
-  'prod.env',
-  'app.env.local',
-  'secrets.env~',
-  '.env~',
-  'x.env_prod',
-  'env.bak_iald',
-  '.envrc',
-  '.еnv',
-  'iald_psion_ѕtate.json',
-  'iald‐psion‐state.json',
-  'copia_iald_psion_state_32B.json',
-  'IALD\u200b_psion_state.json',
-  'server.key~',
-  'iald-stack-v7.py'] : nomes que passaram no filtro

======================================================================
FAIL: test_G_N3_hardlink_swap_never_reads_canary (test_r2_1.GuardN3Toctou.test_G_N3_hardlink_swap_never_reads_canary)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\suite\r2_1\test_r2_1.py", line 198, in test_G_N3_hardlink_swap_never_reads_canary
    self.assertEqual(lidos['canario'], 0, 'o canário foi lido por um caminho de nome benigno')
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 158 != 0 : o canário foi lido por um caminho de nome benigno

----------------------------------------------------------------------
Ran 19 tests in 47.804s

FAILED (failures=12, errors=3)

```

## Saída da suíte com falha: R2.1 heartbeat novos (revisao R2 13/10)

```
ia\projetos_pyhton\IALD\iald_web_server.py", line 3404, in _heartbeat_health_save
    os.replace(tmp, HEARTBEAT_HEALTH_FILE)
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Acesso negado: '\\\\?\\C:\\IALD\\Central de Patentes\\work\\memoria_acom_fix_12out\\9_R2_1\\copia_r2\\testes_r2\\hb\\tests\\tmp\\tmpf6p70pqo\\logs\\iald_heartbeat_health.json.tmp_7cd9be9a' -> '\\\\?\\C:\\IALD\\Central de Patentes\\work\\memoria_acom_fix_12out\\9_R2_1\\copia_r2\\testes_r2\\hb\\tests\\tmp\\tmpf6p70pqo\\logs\\iald_heartbeat_health.json'

======================================================================
ERROR: test_HB4_rotation_waits_for_reader (test_heartbeat_r2_1.HeartbeatR21.test_HB4_rotation_waits_for_reader)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\hb\tests\test_heartbeat_r2_1.py", line 120, in test_HB4_rotation_waits_for_reader
    ns['_heartbeat_telemetry_append']({'kind': 'beat', 'n': 2, 'pad': 'x' * 150})   # rotação com o .jsonl preso
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\hb\copia\projetos_pyhton\IALD\iald_web_server.py", line 3379, in _heartbeat_telemetry_append
    _heartbeat_telemetry_rotate(path)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\hb\copia\projetos_pyhton\IALD\iald_web_server.py", line 3358, in _heartbeat_telemetry_rotate
    os.replace(path, f"{path}.1")
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 32] O arquivo já está sendo usado por outro processo: '\\\\?\\C:\\IALD\\Central de Patentes\\work\\memoria_acom_fix_12out\\9_R2_1\\copia_r2\\testes_r2\\hb\\tests\\tmp\\tmp__zzhiv3\\logs\\iald_heartbeat_telemetry.jsonl' -> '\\\\?\\C:\\IALD\\Central de Patentes\\work\\memoria_acom_fix_12out\\9_R2_1\\copia_r2\\testes_r2\\hb\\tests\\tmp\\tmp__zzhiv3\\logs\\iald_heartbeat_telemetry.jsonl.1'

======================================================================
ERROR: test_HB5_sixty_beats_with_concurrent_sweeper_one_event (test_heartbeat_r2_1.HeartbeatR21.test_HB5_sixty_beats_with_concurrent_sweeper_one_event)
O cenário s3c da revisão (varredor que segura cada arquivo 30 ms), em processo: 60 batidas ok, 1 evento.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\hb\tests\test_heartbeat_r2_1.py", line 132, in test_HB5_sixty_beats_with_concurrent_sweeper_one_event
    status = [ns['heartbeat_cycle']() for _ in range(60)]
              ~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\hb\copia\projetos_pyhton\IALD\iald_web_server.py", line 3497, in heartbeat_cycle
    line = _heartbeat_telemetry_append(summary)
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\hb\copia\projetos_pyhton\IALD\iald_web_server.py", line 3379, in _heartbeat_telemetry_append
    _heartbeat_telemetry_rotate(path)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\hb\copia\projetos_pyhton\IALD\iald_web_server.py", line 3358, in _heartbeat_telemetry_rotate
    os.replace(path, f"{path}.1")
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 32] O arquivo já está sendo usado por outro processo: '\\\\?\\C:\\IALD\\Central de Patentes\\work\\memoria_acom_fix_12out\\9_R2_1\\copia_r2\\testes_r2\\hb\\tests\\tmp\\tmpqlg8c2za\\logs\\iald_heartbeat_telemetry.jsonl' -> '\\\\?\\C:\\IALD\\Central de Patentes\\work\\memoria_acom_fix_12out\\9_R2_1\\copia_r2\\testes_r2\\hb\\tests\\tmp\\tmpqlg8c2za\\logs\\iald_heartbeat_telemetry.jsonl.1'

======================================================================
FAIL: test_HB3_failed_replace_leaves_no_orphan_temp (test_heartbeat_r2_1.HeartbeatR21.test_HB3_failed_replace_leaves_no_orphan_temp)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\copia_r2\testes_r2\hb\tests\test_heartbeat_r2_1.py", line 113, in test_HB3_failed_replace_leaves_no_orphan_temp
    self.assertEqual(self.orfaos(), [])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: ['psion_synthetic_state.json.tmp_029859a7'] != []

First list contains 1 additional elements.
First extra element 0:
'psion_synthetic_state.json.tmp_029859a7'

- ['psion_synthetic_state.json.tmp_029859a7']
+ []

----------------------------------------------------------------------
Ran 5 tests in 4.244s

FAILED (failures=1, errors=4)

```
