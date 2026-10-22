# TESTES — frente FILTROS (conserto ACOM 12/10)

Rodados em 2026-10-13T03:23:13.866383+00:00 com `C:\Python314\python.exe` sobre CÓPIAS (`suite\`), sob a guarda `sitecustomize.py` da auditoria (sem rede, sem escrita fora desta pasta, sem sqlite gravável fora dela, sem abrir confidenciais). Nenhuma chamada a provedor. Resultado medido aqui [REAL]: **90 testes, 90 PASSA, 0 FALHA, 0 pulado(s)** — todas as suítes OK.

| suíte | módulo | teste | resultado |
|---|---|---|---|
| SESSOES (origem) | `test_sessions` | `test_cas_conflict_is_visible_without_retry` | PASSA |
| SESSOES (origem) | `test_sessions` | `test_child_reattachment_cannot_change_parent_constraints_or_scope` | PASSA |
| SESSOES (origem) | `test_sessions` | `test_child_reattachment_inherits_parent_constraints_in_fresh_processes` | PASSA |
| SESSOES (origem) | `test_sessions` | `test_default_model_cannot_change_flow` | PASSA |
| SESSOES (origem) | `test_sessions` | `test_model_output_survives_only_as_declared_candidate` | PASSA |
| SESSOES (origem) | `test_sessions` | `test_new_process_recovers_original_q_and_p` | PASSA |
| SESSOES (origem) | `test_sessions` | `test_operator_actor_is_not_accepted_from_session_payload` | PASSA |
| SESSOES (origem) | `test_sessions` | `test_reference_store_mismatch_is_visible` | PASSA |
| SESSOES (origem) | `test_sessions` | `test_scope_override_fails` | PASSA |
| SESSOES (origem) | `test_sessions` | `test_second_session_attaches_same_core_without_new_objective` | PASSA |
| SESSOES (origem) | `test_sessions` | `test_source_hash_and_existing_reference_identity_are_enforced` | PASSA |
| SESSOES (origem) | `test_sessions` | `test_too_small_projection_fails_instead_of_dropping_anchor` | PASSA |
| SESSOES (origem) | `test_hooks` | `test_both_adapters_project_same_live_q_and_p` | PASSA |
| SESSOES (origem) | `test_hooks` | `test_unbound_session_does_not_leak_another_context` | PASSA |
| SESSOES (origem) | `test_hooks` | `test_unsupported_hook_cannot_approve_tool_calls` | PASSA |
| SESSOES (origem) | `test_hooks` | `test_user_prompt_event_uses_current_input_without_overwriting_anchor` | PASSA |
| SESSOES (origem) | `test_hooks` | `test_wrong_cwd_is_fail_closed` | PASSA |
| SESSOES (novos) | `test_filters` | `test_confidential_name_variants_refused` | PASSA |
| SESSOES (novos) | `test_filters` | `test_content_keys_refused_at_init_and_transition` | PASSA |
| SESSOES (novos) | `test_filters` | `test_escritorio_path_variants_refused` | PASSA |
| SESSOES (novos) | `test_filters` | `test_escritorio_scope_refused` | PASSA |
| SESSOES (novos) | `test_filters` | `test_hardlink_identity_refused` | PASSA |
| SESSOES (novos) | `test_filters` | `test_hook_inherits_path_refusal` | PASSA |
| SESSOES (novos) | `test_filters` | `test_junction_refused_by_realpath` | PASSA |
| SESSOES (novos) | `test_filters` | `test_projection_refuses_confidential_content_without_echo` | PASSA |
| SESSOES (novos) | `test_filters` | `test_reference_and_changes_file_use_the_same_guard` | PASSA |
| SESSOES (novos) | `test_filters` | `test_refusal_log_written_beside_the_bank_without_text` | PASSA |
| SESSOES (novos) | `test_guard` | `test_log_failure_does_not_hide_refusal` | PASSA |
| SESSOES (novos) | `test_guard` | `test_non_string_values_are_serialized` | PASSA |
| SESSOES (novos) | `test_guard` | `test_refusal_never_echoes_and_logs_without_text` | PASSA |
| SESSOES (novos) | `test_guard` | `test_rules` | PASSA |
| SESSOES (novos) | `test_guard` | `test_hardlink_refused_before_identity` | PASSA |
| SESSOES (novos) | `test_guard` | `test_identity_match_refused_even_with_single_link` | PASSA |
| SESSOES (novos) | `test_guard` | `test_junction_resolved` | PASSA |
| SESSOES (novos) | `test_guard` | `test_no_identity_and_stat_failure_fail_closed` | PASSA |
| SESSOES (novos) | `test_guard` | `test_plain_file_directory_and_missing_are_allowed` | PASSA |
| SESSOES (novos) | `test_guard` | `test_registry_from_stat_only` | PASSA |
| SESSOES (novos) | `test_guard` | `test_escritorio_components` | PASSA |
| SESSOES (novos) | `test_guard` | `test_fold` | PASSA |
| SESSOES (novos) | `test_guard` | `test_variants` | PASSA |
| SESSOES (novos) | `test_guard` | `test_escritorio_scope` | PASSA |
| APP (origem) | `test_app_memory` | `test_actual_admin_execute_preserves_plan_actions_and_analysis` | PASSA |
| APP (origem) | `test_app_memory` | `test_actual_admin_handler_two_model_cycles` | PASSA |
| APP (origem) | `test_app_memory` | `test_actual_admin_test_prompt_dispatcher_and_budget` | PASSA |
| APP (origem) | `test_app_memory` | `test_actual_api_dispatcher_stream_transports_and_commits` | PASSA |
| APP (origem) | `test_app_memory` | `test_actual_api_nonstream_commits_content` | PASSA |
| APP (origem) | `test_app_memory` | `test_actual_heartbeat_transport_and_uncertain_block` | PASSA |
| APP (origem) | `test_app_memory` | `test_actual_legacy_completion_transport_scalar_and_stream` | PASSA |
| APP (origem) | `test_app_memory` | `test_actual_native_preparation_places_projection_before_count` | PASSA |
| APP (origem) | `test_app_memory` | `test_actual_sandbox_sdk_receives_same_scope_projection` | PASSA |
| APP (origem) | `test_app_memory` | `test_anchor_overflow_is_visible_before_dispatch` | PASSA |
| APP (origem) | `test_app_memory` | `test_autonomous_crash_after_tool_still_blocks_started_handle` | PASSA |
| APP (origem) | `test_app_memory` | `test_autonomous_crash_and_failure_never_reinvoke_provider` | PASSA |
| APP (origem) | `test_app_memory` | `test_concurrent_same_mission_refuses_without_changing_owner` | PASSA |
| APP (origem) | `test_app_memory` | `test_interrupted_stream_is_uncertain_without_retry` | PASSA |
| APP (origem) | `test_app_memory` | `test_legacy_generation_cannot_bypass_memory` | PASSA |
| APP (origem) | `test_app_memory` | `test_local_outbox_recovers_no_provider_call` | PASSA |
| APP (origem) | `test_app_memory` | `test_migration_explicit_and_history_unverified` | PASSA |
| APP (origem) | `test_app_memory` | `test_missions_separate_in_same_house_and_principal` | PASSA |
| APP (origem) | `test_app_memory` | `test_original_is_stable_across_commands_and_accounts_isolated` | PASSA |
| APP (origem) | `test_app_memory` | `test_patches_cover_native_agents_workers_and_delegates` | PASSA |
| APP (origem) | `test_app_memory` | `test_pending_flow_handles_do_not_grow_per_turn` | PASSA |
| APP (origem) | `test_app_memory` | `test_projection_refreshes_without_accumulating_blocks` | PASSA |
| APP (origem) | `test_app_memory` | `test_provider_two_cycles_refresh_memory_from_real_tool_result` | PASSA |
| APP (origem) | `test_app_memory` | `test_result_persisted_before_done_and_candidate_only` | PASSA |
| APP (origem) | `test_app_memory` | `test_router_real_code_receives_projection_and_updates_state` | PASSA |
| APP (origem) | `test_app_memory` | `test_same_request_never_replays` | PASSA |
| APP (origem) | `test_app_memory` | `test_scoped_record_reader_actual_tool_handler_and_pagination` | PASSA |
| APP (origem) | `test_app_memory` | `test_steering_is_input_and_never_omitted` | PASSA |
| APP (origem) | `test_app_memory` | `test_thread_propagates_same_scope` | PASSA |
| APP (origem) | `test_app_memory` | `test_typed_continuity_never_grants_authority` | PASSA |
| APP (novos) | `test_app_filters` | `test_append_and_projection_refuse_confidential_content` | PASSA |
| APP (novos) | `test_app_filters` | `test_begin_refuses_confidential_objective_before_inscription` | PASSA |
| APP (novos) | `test_app_filters` | `test_dispatch_admin_returns_409_on_confidential` | PASSA |
| APP (novos) | `test_app_filters` | `test_dispatch_returns_409_on_confidential` | PASSA |
| APP (novos) | `test_app_filters` | `test_legacy_names_still_refused` | PASSA |
| APP (novos) | `test_app_filters` | `test_protected_path_variants` | PASSA |
| APP (novos) | `test_app_filters` | `test_read_record_refuses_confidential_slice` | PASSA |
| APP (novos) | `test_app_filters` | `test_stream_response_refusal_recorded` | PASSA |
| APP (novos) | `test_app_filters` | `test_tool_result_refusal_is_recorded_visibly_without_the_text` | PASSA |
| FILA (novos) | `test_filters_queue` | `test_attach_rechecks_projection` | PASSA |
| FILA (novos) | `test_filters_queue` | `test_clean_projection_passes` | PASSA |
| FILA (novos) | `test_filters_queue` | `test_forbidden_escritorio_and_tokens` | PASSA |
| FILA (novos) | `test_filters_queue` | `test_nos_packet_safe_text_inherits_new_rules` | PASSA |
| FILA (novos) | `test_filters_queue` | `test_projection_refused_before_dispatch` | PASSA |
| BLOCOS (novos) | `test_blocks` | `test_cas_abort_on_unexpected_head` | PASSA |
| BLOCOS (novos) | `test_blocks` | `test_cli_dry_run_writes_nothing` | PASSA |
| BLOCOS (novos) | `test_blocks` | `test_memory_md_single_line_and_limits` | PASSA |
| BLOCOS (novos) | `test_blocks` | `test_replace_block_exact_bytes_lf_and_crlf` | PASSA |
| BLOCOS (novos) | `test_blocks` | `test_session_bridge_whole_file` | PASSA |

## Por suíte

| suíte | módulos | rodados | segundos | returncode | OK |
|---|---|---|---|---|---|
| SESSOES (origem) | test_sessions, test_hooks | 17 | 7.81 | 0 | sim |
| SESSOES (novos) | test_filters, test_guard | 24 | 8.9 | 0 | sim |
| APP (origem) | test_app_memory | 31 | 22.59 | 0 | sim |
| APP (novos) | test_app_filters | 9 | 0.78 | 0 | sim |
| FILA (novos) | test_filters_queue | 5 | 0.29 | 0 | sim |
| BLOCOS (novos) | test_blocks | 5 | 0.39 | 0 | sim |

## Guarda de execução (auditoria)

processos sob guarda: 124; bloqueios: 1; leituras fora da pasta (só leitura, amostra): 179

- BLOQUEIO: `{"kind": "BLOCK_NETWORK", "event": "socket.bind", "path": null, "src": null, "dst": null, "args": "(<socket.socket fd=380, family=23, type=1, proto=0>, ('::1', 0))"}`
