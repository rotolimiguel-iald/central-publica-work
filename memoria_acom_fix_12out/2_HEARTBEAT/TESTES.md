# TESTES — frente HEARTBEAT (conserto ACOM 12/10, decisão D3)

Rodada: 2026-10-13T00:21:09 · Python 3.14.3 · guarda da auditoria `sitecustomize.py` sha256 `08f378651f8c0f74…` (cópia byte a byte de `C:\IALD\PROGRAMA_IALD\exame_12out\E_ACOM\guard\sitecustomize.py`) · estatuto: **[REAL]** (resultados capturados do `unittest -v` por `scripts\run_tests.py`, gravados em `tests\RESULTADOS.json`).

Ambiente de cada suíte: processo novo, `PYTHONPATH=tests\guard`, `ACOM_AUDIT_ROOT=<pasta da frente>`, sem bytecode, temporários dentro da pasta com prefixo `\\?\` (LongPathsEnabled=0 nesta máquina: os nomes do outbox do app, ~190 caracteres, estouram MAX_PATH a partir desta pasta). Nenhum provedor, nenhuma rede, nenhum confidencial lido: o psion dos testes é um arquivo sintético; o banco comum é um `MemoryStore` sintético na pasta temporária; a lib `iald_memory` usada é a cópia congelada v1 (`tests\core`, sha256 no MANIFESTO).

## NOVA — req_lib falso em processo — `tests\test_heartbeat_v2.py`

`OK` · 12 caso(s) · 19.7 s

| caso | o que prova | resultado |
|---|---|---|
| `test_degraded_measurement_never_reaches_psion` | medidas com regime `operational_memory_included`, payload que não é o r60 (sha256 estranho) ou amostra sem fórmula → `inadmissible`, bytes do psion intactos, telemetria `refused_*`, classe `falha`; medida admissível entra (total_beats 11); ancoragem violada (beta 0,5) → `anchoring_error` e psion não salvo. | **PASSA** |
| `test_heartbeat_failure_does_not_block_next_cycle` | HTTP 500 → `continue` → `no_results`, classe `falha`, 1 evento, psion intocado; depois 200 → `ok` (mudança de classe → evento); exceção de rede não propaga; memória comum indisponível (`record_measurement` lança OSError) → batida completa, linha `memory_event_failed`, classe do health não avança, batida seguinte grava o alerta. | **PASSA** |
| `test_heartbeat_measures_generation_only` | post falso com 0,2 s de latência; `project_messages` e `_operational_native_payload` trocados por versões que dormem 1 s e contam; contador = 0 durante `_heartbeat_measure`; payload enviado == payload r60 (mensagens exatamente `[sys_msg, prompt]`, sem bloco de memória); `elapsed` de cada amostra em [0,2; 0,3] s; fórmula `completion_tokens/elapsed`; corpos de resposta ausentes da medida. | **PASSA** |
| `test_heartbeat_memory_event_only_on_class_change_or_hourly` | relógio injetado; estado de saúde prévio `ok`; 3 batidas `ok` → 0 eventos; 1 batida `alerta` (50 vs baseline 100) → 1 evento; mesma classe < 1 h → nada; +61 min → 1 evento; registros `fact/REAL`, fonte `measurement` `heartbeat_telemetry:<sha>`, id `hb.<sha>`, texto sem `response`/`choices`; fase `heartbeat_alerta`; linhas `memory_event` da telemetria casam com os ids do livro; health.json com classe e revisão. | **PASSA** |
| `test_heartbeat_source_has_no_memory_inside_the_measurement` | estático (AST, código sem docstrings): `heartbeat_cycle`, `_heartbeat_measure` e `_heartbeat_record_memory_if_due` não chamam `run_autonomous`, `tool_result`, `_operational_native_payload`, `project_messages`, `check_text_window`, `.projection`, `routing_state`; `_heartbeat_cycle_with_memory` não existe; `_operational_native_payload` e `_prepare_native_payload` continuam para chat/admin; `_save_psion_state` usa `os.replace` e não `open(..., "w")`; o gatilho admin chama `heartbeat_cycle()`. | **PASSA** |
| `test_heartbeat_telemetry_rotation` | teto de 4 KiB: 120 linhas → `.1`…`.5` existem (cada ≤ 4 KiB), `.6` não existe, arquivo corrente ≤ 4 KiB, cada linha íntegra com sha conferido, sequência contígua até a linha corrente. | **PASSA** |
| `test_heartbeat_tok_s_prefers_server_timings` | `_heartbeat_tok_s`: com `timings` → `predicted_n/predicted_ms×1000` (200 tok/s com elapsed 9 s); sem `timings` → `completion_tokens/elapsed`; timings inválidos (0/0) caem na fórmula do elapsed; sem tokens → `(None, None)`; numa medida com latência 0,3 s e timings 128/400 ms o tok/s é 320,0. | **PASSA** |
| `test_memory_event_is_fact_real_without_bodies_and_legacy_context_untouched` | contexto legado de 10/10 criado por `run_autonomous` fica com o mesmo recibo depois da batida; livro novo `app_service_<sha(native-heartbeat:health)>` no mesmo escopo, restrições `no_response_bodies`/`gate_authority=false`, âncora do serviço; registro `fact/REAL` com fonte `measurement`, texto < 600 caracteres, sem corpo de resposta nem chaves; projeção sem corpo. | **PASSA** |
| `test_psion_save_atomic_and_daily_bak` | `_save_psion_state` sobre arquivo sintético: bytes CRLF iguais aos do gravador antigo; 3 gravações no mesmo dia → exatamente 1 `.bak_<AAAAMMDD>` com os bytes da primeira versão; nenhum tempário sobrando; com `HEARTBEAT_PSION_DAILY_BAK=False` não nasce cópia. | **PASSA** |
| `test_record_measurement_idempotent_scoped_and_validated` | `record_measurement`: mesmo event_id → recibo replayed na mesma revisão; outra linhagem → outro contexto; objetivo alterado na mesma linhagem → AnchorConflict (ValueError); texto vazio, identificador inválido e flow ilegal → ValueError; partição: escopo de outra casa não lê. | **PASSA** |
| `test_sixty_beats_in_process_zero_or_one_memory_event` | 60 batidas com req_lib falso (timings 100 tok/s): 60× `ok`, exatamente 1 evento na memória (classe estabelecida), psion sintético com total_beats 70 e generation 60, telemetria com rotação (teto 16 KiB) e 61 linhas íntegras (60 beats + 1 memory_event); mais 60 batidas com estado prévio → 0 eventos novos. | **PASSA** |
| `test_skipped_busy_and_aborted_user_write_telemetry_only` | `skipped_busy` (servidor ocupado) → só telemetria, classe nula, sem evento, psion não criado; `skipped_offline` → classe `falha` → 1 evento. | **PASSA** |

## STUB — servidor de modelo falso, 60 batidas — `tests\test_heartbeat_stub_server.py`

`OK` · 3 caso(s) · 5.7 s

| caso | o que prova | resultado |
|---|---|---|
| `test_sixty_beats_stub_server_zero_or_one_memory_event` | servidor de modelo FALSO (adaptador de transporte do `requests`, sem socket) com `/health` e `/v1/chat/completions` no formato llama.cpp (timings 64 tok / 640 ms): 60 batidas com `_heartbeat_llama_ok` e `_heartbeat_is_idle` REAIS → 60× `ok`; 600 POSTs e 60 GETs; cada corpo recebido == payload r60 (Content-Type application/json, timeout 60); `project_messages`/`tool_result`/`run_autonomous` nunca chamados; tok/s = 100,0 em todas as amostras pela fórmula dos timings; psion sintético 70 beats / generation 60 / baseline 100,0 / sem alertas; rotação com teto de 32 KiB; 1 evento na memória (fase `heartbeat_ok`) cujo id casa com a linha `memory_event`; variante com saúde prévia: 60 batidas → 0 eventos. | **PASSA** |
| `test_stub_http_500_then_offline_then_recovers_without_blocking` | stub devolve 500 → `no_results`, psion intocado, classe `falha` (1 evento); `/health` 503 → `skipped_offline` (sem evento novo); volta 200 → `ok` sem conciliação (evento por mudança de classe); telemetria `[no_results, skipped_offline, ok]`. | **PASSA** |
| `test_stub_without_timings_measures_only_the_generation_window` | stub sem `timings` e com 0,2 s de latência; `project_messages` lento (1 s) nunca chamado; fórmula `completion_tokens/elapsed`; `elapsed` em [0,2; 0,3] s; tok/s em [210; 330]; classe `ok`. | **PASSA** |

## APP 31 (10/10) com 1 caso reescrito — `tests\app\test_app_memory.py`

`OK` · 31 caso(s) · 23.2 s

| caso | o que prova | resultado |
|---|---|---|
| `test_actual_admin_execute_preserves_plan_actions_and_analysis` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_actual_admin_handler_two_model_cycles` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_actual_admin_test_prompt_dispatcher_and_budget` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_actual_api_dispatcher_stream_transports_and_commits` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_actual_api_nonstream_commits_content` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_actual_heartbeat_transport_generation_only_never_blocks` | REESCRITA do caso `test_actual_heartbeat_transport_and_uncertain_block` (l.270–284 da suíte de 10/10), que afirmava o bloco de memória no pedido, o candidato `synthetic-heartbeat` no banco e o bloqueio por RuntimeError: agora afirma payload r60 exato, `project_messages` não chamado, contexto legado nunca criado, livro de saúde na revisão 1 com fase `heartbeat_falha` e sem corpo de resposta, exceção de rede não propaga e o ciclo seguinte roda sem evento novo. | **PASSA** |
| `test_actual_legacy_completion_transport_scalar_and_stream` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_actual_native_preparation_places_projection_before_count` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_actual_sandbox_sdk_receives_same_scope_projection` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_anchor_overflow_is_visible_before_dispatch` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_autonomous_crash_after_tool_still_blocks_started_handle` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_autonomous_crash_and_failure_never_reinvoke_provider` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_concurrent_same_mission_refuses_without_changing_owner` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_interrupted_stream_is_uncertain_without_retry` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_legacy_generation_cannot_bypass_memory` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_local_outbox_recovers_no_provider_call` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_migration_explicit_and_history_unverified` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_missions_separate_in_same_house_and_principal` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_operator_json_byte_backup_migration_and_soft_delete` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_original_is_stable_across_commands_and_accounts_isolated` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_patches_cover_native_agents_workers_and_delegates` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_pending_flow_handles_do_not_grow_per_turn` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_projection_refreshes_without_accumulating_blocks` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_provider_two_cycles_refresh_memory_from_real_tool_result` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_result_persisted_before_done_and_candidate_only` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_router_real_code_receives_projection_and_updates_state` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_same_request_never_replays` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_scoped_record_reader_actual_tool_handler_and_pagination` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_steering_is_input_and_never_omitted` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_thread_propagates_same_scope` | (suíte APP de 10/10, inalterada) | **PASSA** |
| `test_typed_continuity_never_grants_authority` | (suíte APP de 10/10, inalterada) | **PASSA** |

**Total: 46 casos; falhas: 0 ; `all_pass = True`.**

## Eventos da guarda durante as três suítes [REAL]

- `BLOCK_NETWORK`: 3
- `CTYPES_DLOPEN`: 3
- `GUARD_ON`: 3
- `READ_OUTSIDE`: 298

Leitura: `BLOCK_WRITE_OUTSIDE` (quando aparece) são as sondagens do `tempfile.gettempdir()` nos diretórios temporários do sistema (recusadas pela guarda, por isso os temporários caem dentro da pasta); `BLOCK_NETWORK` é o `socket.socketpair()` emulado no `import requests` (um `bind` em `::1` por processo, recusado — conferido com `import requests` isolado); `READ_OUTSIDE` são leituras de módulos de produção importados pela suíte APP (só leitura); nenhum `BLOCK_CONFIDENTIAL_*`, nenhum `BLOCK_MUTATION_OUTSIDE`, nenhum `SQLITE_RW` fora da pasta. Nesta rodada não houve `BLOCK_WRITE_OUTSIDE` nem `BLOCK_MUTATION_OUTSIDE`; os eventos medidos são só os listados acima.
