# TESTES — INTEGRAÇÃO R2 (conserto ACOM 12/10; candidato_r2)

Rodados em 2026-10-13T09:36:16.522882+00:00 com `C:\Python314\python.exe` sobre CÓPIAS do candidato (`testes\`), sob a guarda `sitecustomize.py` da auditoria. Nenhuma chamada a provedor. Resultado medido aqui [REAL]: **235 testes, 235 PASSA, 0 FALHA, 0 pulado(s)** — todas as suítes OK.

| suíte | módulos | rodados | PASSA | FALHA | segundos | OK |
|---|---|---|---|---|---|---|
| CORE 20 (origem, 1 reescrita D1/D2) | test_store | 20 | 20 | 0 | 1.28 | sim |
| NUCLEO novos 34 (frente 1) | test_store_v2 | 34 | 34 | 0 | 67.26 | sim |
| SESSOES 17 (origem) | test_sessions, test_hooks | 17 | 17 | 0 | 8.63 | sim |
| SESSOES novos 24 (frente 3) | test_filters, test_guard | 24 | 24 | 0 | 9.35 | sim |
| APP 31 (origem, 1 reescrita D3) | test_app_memory | 31 | 31 | 0 | 13.63 | sim |
| APP novos 9 (frente 3) | test_app_filters | 9 | 9 | 0 | 0.79 | sim |
| HEARTBEAT novos 15 (frente 2) | test_heartbeat_v2, test_heartbeat_stub_server | 15 | 15 | 0 | 18.39 | sim |
| FILA 55 (origem) | test_coordination, test_optional_work, test_transport, test_maximum_coordination, test_request_controls, test_provider_memory.AllAdapterMemoryTests, test_canonical_memory | 55 | 55 | 0 | 20.98 | sim |
| FILA novos 5 (frente 3) | test_filters_queue | 5 | 5 | 0 | 0.3 | sim |
| BLOCOS 5 (frente 3) | test_blocks | 5 | 5 | 0 | 0.39 | sim |
| INTEGRACAO novos (esta frente) | test_integracao | 5 | 5 | 0 | 34.12 | sim |
| R2 novos (achados bloqueantes 13/10) | test_r2 | 15 | 15 | 0 | 8.41 | sim |

## Cada teste

| suíte | módulo | teste | resultado |
|---|---|---|---|
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_abrupt_process_exit_recovers_whole_previous_state` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_all_consolidated_record_types_cannot_disappear_under_compaction` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_cas_and_stable_replay` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_concurrent_processes_no_lost_records_or_handles` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_constraints_immutable_and_children_inherit` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_cross_scope_all_entry_points` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_database_update_delete_guards` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_errata_are_additive_and_handles_merge` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_explicitly_required_candidate_never_drops_and_remains_unverified` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_failure_after_insert_rolls_back_q_and_p` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_model_cannot_establish_anchor_or_flow_or_promote_output` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_original_bytes_and_strict_idempotent_anchor` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_projection_is_bounded_auditable_and_does_not_destroy` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_projection_never_separates_original_and_correction` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_state_and_flow_commit_together_and_survive_restart` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_steering_after_original_goal_is_required_or_overflows` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_tampered_blob_and_missing_guard_fail_closed` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_tampered_chain_with_guards_restored_fails` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_tampered_objective_with_guards_restored_fails` | PASSA |
| CORE 20 (origem, 1 reescrita D1/D2) | `test_store` | `test_validation_rejects_path_identifiers_and_nonfinite_values` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_archive_legacy_backups_corrupt_copy_aborts_without_deleting` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_archive_legacy_backups_mover_manifest_and_sha` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_delta_events_store_no_state_and_replay_from_snapshot` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_errata_and_handles_replay_identically_through_snapshots` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_stored_json_digest_equals_v1_formula_and_falls_back_when_noncanonical` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_public_contract_fields_unchanged` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_v1_frozen_copy_is_pinned` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_growth_n300_bytes_db_journal_snapshots` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_transition_time_bounded_n300` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_abrupt_exit_after_journal_append_voids_orphan` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_journal_chain_and_rebuild_equals_db` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_journal_missing_or_truncated_is_visible` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_journal_tail_cache_validated_by_stat_across_instances` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_journal_written_before_commit_and_orphan_voided` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_covering_index_serves_chain_reads_without_legacy_state` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_legacy_v1_db_refused_without_migration` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_migration_dry_run_writes_nothing` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_migration_is_idempotent` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_migration_preserves_head_state_sha_and_chain` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_mixed_legacy_delta_replay` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_v1_code_refuses_v2_schema` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_migrar_para_delta_cli_dry_run_apply_verify` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_mover_backups_antigos_cli` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_archive_unavailable_keeps_local_copies` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_due_snapshot_that_does_not_verify_fails_the_mutation` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_snapshot_keep3_and_archive_move_verified` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_snapshot_policy_50_mutations` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_snapshot_policy_60_minutes` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_snapshot_policy_counts_committed_mutations_only` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_context_state_revision_lag_fails_closed` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_delta_event_tamper_fails_closed` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_materialized_row_tamper_fails_closed` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_snapshot_row_tamper_fails_closed` | PASSA |
| NUCLEO novos 34 (frente 1) | `test_store_v2` | `test_stray_snapshot_beyond_head_fails_closed` | PASSA |
| SESSOES 17 (origem) | `test_sessions` | `test_cas_conflict_is_visible_without_retry` | PASSA |
| SESSOES 17 (origem) | `test_sessions` | `test_child_reattachment_cannot_change_parent_constraints_or_scope` | PASSA |
| SESSOES 17 (origem) | `test_sessions` | `test_child_reattachment_inherits_parent_constraints_in_fresh_processes` | PASSA |
| SESSOES 17 (origem) | `test_sessions` | `test_default_model_cannot_change_flow` | PASSA |
| SESSOES 17 (origem) | `test_sessions` | `test_model_output_survives_only_as_declared_candidate` | PASSA |
| SESSOES 17 (origem) | `test_sessions` | `test_new_process_recovers_original_q_and_p` | PASSA |
| SESSOES 17 (origem) | `test_sessions` | `test_operator_actor_is_not_accepted_from_session_payload` | PASSA |
| SESSOES 17 (origem) | `test_sessions` | `test_reference_store_mismatch_is_visible` | PASSA |
| SESSOES 17 (origem) | `test_sessions` | `test_scope_override_fails` | PASSA |
| SESSOES 17 (origem) | `test_sessions` | `test_second_session_attaches_same_core_without_new_objective` | PASSA |
| SESSOES 17 (origem) | `test_sessions` | `test_source_hash_and_existing_reference_identity_are_enforced` | PASSA |
| SESSOES 17 (origem) | `test_sessions` | `test_too_small_projection_fails_instead_of_dropping_anchor` | PASSA |
| SESSOES 17 (origem) | `test_hooks` | `test_both_adapters_project_same_live_q_and_p` | PASSA |
| SESSOES 17 (origem) | `test_hooks` | `test_unbound_session_does_not_leak_another_context` | PASSA |
| SESSOES 17 (origem) | `test_hooks` | `test_unsupported_hook_cannot_approve_tool_calls` | PASSA |
| SESSOES 17 (origem) | `test_hooks` | `test_user_prompt_event_uses_current_input_without_overwriting_anchor` | PASSA |
| SESSOES 17 (origem) | `test_hooks` | `test_wrong_cwd_is_fail_closed` | PASSA |
| SESSOES novos 24 (frente 3) | `test_filters` | `test_confidential_name_variants_refused` | PASSA |
| SESSOES novos 24 (frente 3) | `test_filters` | `test_content_keys_refused_at_init_and_transition` | PASSA |
| SESSOES novos 24 (frente 3) | `test_filters` | `test_escritorio_path_variants_refused` | PASSA |
| SESSOES novos 24 (frente 3) | `test_filters` | `test_escritorio_scope_refused` | PASSA |
| SESSOES novos 24 (frente 3) | `test_filters` | `test_hardlink_identity_refused` | PASSA |
| SESSOES novos 24 (frente 3) | `test_filters` | `test_hook_inherits_path_refusal` | PASSA |
| SESSOES novos 24 (frente 3) | `test_filters` | `test_junction_refused_by_realpath` | PASSA |
| SESSOES novos 24 (frente 3) | `test_filters` | `test_projection_refuses_confidential_content_without_echo` | PASSA |
| SESSOES novos 24 (frente 3) | `test_filters` | `test_reference_and_changes_file_use_the_same_guard` | PASSA |
| SESSOES novos 24 (frente 3) | `test_filters` | `test_refusal_log_written_beside_the_bank_without_text` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_log_failure_does_not_hide_refusal` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_non_string_values_are_serialized` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_refusal_never_echoes_and_logs_without_text` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_rules` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_hardlink_refused_before_identity` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_identity_match_refused_even_with_single_link` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_junction_resolved` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_no_identity_and_stat_failure_fail_closed` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_plain_file_directory_and_missing_are_allowed` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_registry_from_stat_only` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_escritorio_components` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_fold` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_variants` | PASSA |
| SESSOES novos 24 (frente 3) | `test_guard` | `test_escritorio_scope` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_actual_admin_execute_preserves_plan_actions_and_analysis` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_actual_admin_handler_two_model_cycles` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_actual_admin_test_prompt_dispatcher_and_budget` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_actual_api_dispatcher_stream_transports_and_commits` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_actual_api_nonstream_commits_content` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_actual_heartbeat_transport_generation_only_never_blocks` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_actual_legacy_completion_transport_scalar_and_stream` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_actual_native_preparation_places_projection_before_count` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_actual_sandbox_sdk_receives_same_scope_projection` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_anchor_overflow_is_visible_before_dispatch` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_autonomous_crash_after_tool_still_blocks_started_handle` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_autonomous_crash_and_failure_never_reinvoke_provider` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_concurrent_same_mission_refuses_without_changing_owner` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_interrupted_stream_is_uncertain_without_retry` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_legacy_generation_cannot_bypass_memory` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_local_outbox_recovers_no_provider_call` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_migration_explicit_and_history_unverified` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_missions_separate_in_same_house_and_principal` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_operator_json_byte_backup_migration_and_soft_delete` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_original_is_stable_across_commands_and_accounts_isolated` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_patches_cover_native_agents_workers_and_delegates` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_pending_flow_handles_do_not_grow_per_turn` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_projection_refreshes_without_accumulating_blocks` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_provider_two_cycles_refresh_memory_from_real_tool_result` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_result_persisted_before_done_and_candidate_only` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_router_real_code_receives_projection_and_updates_state` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_same_request_never_replays` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_scoped_record_reader_actual_tool_handler_and_pagination` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_steering_is_input_and_never_omitted` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_thread_propagates_same_scope` | PASSA |
| APP 31 (origem, 1 reescrita D3) | `test_app_memory` | `test_typed_continuity_never_grants_authority` | PASSA |
| APP novos 9 (frente 3) | `test_app_filters` | `test_append_and_projection_refuse_confidential_content` | PASSA |
| APP novos 9 (frente 3) | `test_app_filters` | `test_begin_refuses_confidential_objective_before_inscription` | PASSA |
| APP novos 9 (frente 3) | `test_app_filters` | `test_dispatch_admin_returns_409_on_confidential` | PASSA |
| APP novos 9 (frente 3) | `test_app_filters` | `test_dispatch_returns_409_on_confidential` | PASSA |
| APP novos 9 (frente 3) | `test_app_filters` | `test_legacy_names_still_refused` | PASSA |
| APP novos 9 (frente 3) | `test_app_filters` | `test_protected_path_variants` | PASSA |
| APP novos 9 (frente 3) | `test_app_filters` | `test_read_record_refuses_confidential_slice` | PASSA |
| APP novos 9 (frente 3) | `test_app_filters` | `test_stream_response_refusal_recorded` | PASSA |
| APP novos 9 (frente 3) | `test_app_filters` | `test_tool_result_refusal_is_recorded_visibly_without_the_text` | PASSA |
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
| FILA 55 (origem) | `test_coordination` | `test_cancel_during_dispatch_prevents_model_call` | PASSA |
| FILA 55 (origem) | `test_coordination` | `test_claim_and_project_binding_are_fail_closed` | PASSA |
| FILA 55 (origem) | `test_coordination` | `test_failed_execution_never_creates_synthesis` | PASSA |
| FILA 55 (origem) | `test_coordination` | `test_full_lifecycle_preserves_original_classification_and_single_execution` | PASSA |
| FILA 55 (origem) | `test_coordination` | `test_idempotent_button_contains_no_original_prompt_in_url` | PASSA |
| FILA 55 (origem) | `test_coordination` | `test_two_runtimes_share_serial_execution_and_recovery_does_not_interrupt` | PASSA |
| FILA 55 (origem) | `test_optional_work` | `test_cannot_invent_budget_exhaustion` | PASSA |
| FILA 55 (origem) | `test_optional_work` | `test_confirmed_unavailable_work_can_be_released_without_new_call` | PASSA |
| FILA 55 (origem) | `test_optional_work` | `test_failed_executor_cannot_be_presented_as_local_completion` | PASSA |
| FILA 55 (origem) | `test_optional_work` | `test_local_synthesis_can_label_its_own_review_without_work` | PASSA |
| FILA 55 (origem) | `test_optional_work` | `test_optional_local_preparation_preserves_original_and_constraints` | PASSA |
| FILA 55 (origem) | `test_optional_work` | `test_uncertain_work_dispatch_is_not_skipped` | PASSA |
| FILA 55 (origem) | `test_optional_work` | `test_work_budget_exhausted_still_completes_one_executor_call` | PASSA |
| FILA 55 (origem) | `test_transport` | `test_disabled_never_advances_job` | PASSA |
| FILA 55 (origem) | `test_transport` | `test_idle_does_not_discover_or_call_providers` | PASSA |
| FILA 55 (origem) | `test_transport` | `test_missing_creation_authorization_blocks_new_handoff` | PASSA |
| FILA 55 (origem) | `test_transport` | `test_receipt_has_no_prompt_and_keeps_byte_backup` | PASSA |
| FILA 55 (origem) | `test_transport` | `test_resume_active_before_new_request` | PASSA |
| FILA 55 (origem) | `test_transport` | `test_submit_is_idempotent` | PASSA |
| FILA 55 (origem) | `test_transport` | `test_terminal_jobs_are_not_replayed` | PASSA |
| FILA 55 (origem) | `test_maximum_coordination` | `test_long_persisted_request_is_readable_and_prepared_without_losing_memory` | PASSA |
| FILA 55 (origem) | `test_request_controls` | `test_bench_mission_is_named_and_other_missions_stay_closed` | PASSA |
| FILA 55 (origem) | `test_request_controls` | `test_large_packet_not_cut_to_old_transport_cap` | PASSA |
| FILA 55 (origem) | `test_request_controls` | `test_maximum_providers_ignore_old_daily_branch_and_lemma_caps` | PASSA |
| FILA 55 (origem) | `test_request_controls` | `test_measured_accounting_is_not_a_billing_claim` | PASSA |
| FILA 55 (origem) | `test_request_controls` | `test_mimo_payload_uses_maximum_output_and_thinking` | PASSA |
| FILA 55 (origem) | `test_request_controls` | `test_required_executor_never_falls_back` | PASSA |
| FILA 55 (origem) | `test_request_controls` | `test_source_and_generation_restrictions_remain` | PASSA |
| FILA 55 (origem) | `test_request_controls` | `test_uncertain_result_consumes_unit_without_retry` | PASSA |
| FILA 55 (origem) | `test_request_controls` | `test_unknown_restrictions_and_stale_financial_cap_rejected` | PASSA |
| FILA 55 (origem) | `test_request_controls` | `test_wrong_provider_rejected_before_transport` | PASSA |
| FILA 55 (origem) | `test_request_controls` | `test_maximum_memory_grows_past_old_cap_but_preserves_scope` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_all_seven_adapters_receive_same_original_q_p` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_checkpoint_refusal_prevents_provider` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_cross_context_original_mismatch_fails` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_free_route_rite_pauses_once_without_retry_loop` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_idempotent_request_cannot_change_memory_binding` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_legacy_terminal_unchanged_and_legacy_pending_cannot_send` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_missing_or_tampered_packet_blocked_before_adapter` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_no_repeat_if_checkpoint_fails_after_result_persisted` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_original_bytes_state_and_flow_cross_whole_lifecycle` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_original_transported_once_and_context_budget_reserved` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_outbox_replay_after_core_commit_before_queue_ack` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_restart_immediately_updates_shared_flow` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_typed_jev_body_contains_same_controller_state` | PASSA |
| FILA 55 (origem) | `test_provider_memory` | `test_untrusted_output_cannot_change_anchor_or_authority` | PASSA |
| FILA 55 (origem) | `test_canonical_memory` | `test_blocked_source_chunk_is_never_forwarded` | PASSA |
| FILA 55 (origem) | `test_canonical_memory` | `test_changed_packet_fails_before_network` | PASSA |
| FILA 55 (origem) | `test_canonical_memory` | `test_changed_source_requires_refresh` | PASSA |
| FILA 55 (origem) | `test_canonical_memory` | `test_every_executor_receives_same_packet_without_network` | PASSA |
| FILA 55 (origem) | `test_canonical_memory` | `test_missing_index_fails_before_transport` | PASSA |
| FILA 55 (origem) | `test_canonical_memory` | `test_packet_has_verifiable_source_and_partial_coverage` | PASSA |
| FILA 55 (origem) | `test_canonical_memory` | `test_secret_request_is_rejected` | PASSA |
| FILA 55 (origem) | `test_canonical_memory` | `test_standard_memory_respects_projection_cap_with_long_prompt` | PASSA |
| FILA 55 (origem) | `test_canonical_memory` | `test_tampered_index_prevents_call` | PASSA |
| FILA novos 5 (frente 3) | `test_filters_queue` | `test_attach_rechecks_projection` | PASSA |
| FILA novos 5 (frente 3) | `test_filters_queue` | `test_clean_projection_passes` | PASSA |
| FILA novos 5 (frente 3) | `test_filters_queue` | `test_forbidden_escritorio_and_tokens` | PASSA |
| FILA novos 5 (frente 3) | `test_filters_queue` | `test_nos_packet_safe_text_inherits_new_rules` | PASSA |
| FILA novos 5 (frente 3) | `test_filters_queue` | `test_projection_refused_before_dispatch` | PASSA |
| BLOCOS 5 (frente 3) | `test_blocks` | `test_cas_abort_on_unexpected_head` | PASSA |
| BLOCOS 5 (frente 3) | `test_blocks` | `test_cli_dry_run_writes_nothing` | PASSA |
| BLOCOS 5 (frente 3) | `test_blocks` | `test_memory_md_single_line_and_limits` | PASSA |
| BLOCOS 5 (frente 3) | `test_blocks` | `test_replace_block_exact_bytes_lf_and_crlf` | PASSA |
| BLOCOS 5 (frente 3) | `test_blocks` | `test_session_bridge_whole_file` | PASSA |
| INTEGRACAO novos (esta frente) | `test_integracao` | `test_e2e_init_300_transitions_project_verify` | PASSA |
| INTEGRACAO novos (esta frente) | `test_integracao` | `test_merged_init_exports_union_of_both_fronts` | PASSA |
| INTEGRACAO novos (esta frente) | `test_integracao` | `test_migration_rehearsal_three_contexts` | PASSA |
| INTEGRACAO novos (esta frente) | `test_integracao` | `test_record_measurement_passes_through_guard_before_any_write` | PASSA |
| INTEGRACAO novos (esta frente) | `test_integracao` | `test_sessions_cli_refuses_v1_database_until_migrated` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_adversarial_battery_one_megabyte_each` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_growth_is_linear_not_quadratic` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_key_pem_regex_was_also_quadratic_and_now_is_linear` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_review_A_E7_drive_letters_32000_was_43s` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_review_A_E7b_listing_4000_paths_was_71s` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_review_B_content_table` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_same_decision_as_r1_on_every_r1_form` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_contexts_differing_only_in_case_have_distinct_journals` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_backup_suffix_and_case_variants_refused` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_confidential_named_reference_is_never_opened` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_extra_key_refused_without_echo` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_hardlinked_reference_refused` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_normal_flow_and_reuse_return_only_protocol_keys` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_production_reference_format_accepted` | PASSA |
| R2 novos (achados bloqueantes 13/10) | `test_r2` | `test_reference_operand_is_guarded_too` | PASSA |

## Guarda de execução (auditoria)

processos sob guarda nesta rodada: 129; eventos por tipo: `{"GUARD_ON": 136, "READ_OUTSIDE": 137, "SUBPROCESS": 84, "CTYPES_DLOPEN": 4, "SQLITE_RO_OUTSIDE": 67}`; bloqueios: 0

