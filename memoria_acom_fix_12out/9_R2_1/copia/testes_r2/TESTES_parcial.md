# TESTES — INTEGRAÇÃO R2 (conserto ACOM 12/10; candidato_r2)

Rodados em 2026-10-13T09:45:41.670634+00:00 com `C:\Python314\python.exe` sobre CÓPIAS do candidato (`testes\`), sob a guarda `sitecustomize.py` da auditoria. Nenhuma chamada a provedor. Resultado medido aqui [REAL]: **15 testes, 15 PASSA, 0 FALHA, 0 pulado(s)** — todas as suítes OK.

| suíte | módulos | rodados | PASSA | FALHA | segundos | OK |
|---|---|---|---|---|---|---|
| HEARTBEAT novos 15 (frente 2) | test_heartbeat_v2, test_heartbeat_stub_server | 15 | 15 | 0 | 26.99 | sim |

## Cada teste

| suíte | módulo | teste | resultado |
|---|---|---|---|
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_v2` | `test_degraded_measurement_never_reaches_psion` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_v2` | `test_heartbeat_failure_does_not_block_next_cycle` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_v2` | `test_heartbeat_measures_generation_only` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_v2` | `test_heartbeat_memory_event_only_on_class_change_or_hourly` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_v2` | `test_heartbeat_source_has_no_memory_inside_the_measurement` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_v2` | `test_heartbeat_telemetry_rotation` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_v2` | `test_heartbeat_tok_s_prefers_server_timings` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_v2` | `test_memory_event_is_fact_real_without_bodies_and_legacy_context_untouched` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_v2` | `test_psion_save_atomic_and_daily_bak` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_v2` | `test_record_measurement_idempotent_scoped_and_validated` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_v2` | `test_sixty_beats_in_process_zero_or_one_memory_event` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_v2` | `test_skipped_busy_and_aborted_user_write_telemetry_only` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_stub_server` | `test_sixty_beats_stub_server_zero_or_one_memory_event` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_stub_server` | `test_stub_http_500_then_offline_then_recovers_without_blocking` | PASSA |
| HEARTBEAT novos 15 (frente 2) | `test_heartbeat_stub_server` | `test_stub_without_timings_measures_only_the_generation_window` | PASSA |

## Guarda de execução (auditoria)

processos sob guarda nesta rodada: 1; eventos por tipo: `{"GUARD_ON": 1, "READ_OUTSIDE": 60, "BLOCK_NETWORK": 1}`; bloqueios: 1

- BLOQUEIO: `{"kind": "BLOCK_NETWORK", "event": "socket.bind", "path": null, "src": null, "dst": null, "args": "(<socket.socket fd=412, family=23, type=1, proto=0>, ('::1', 0))", "mode": null}`
