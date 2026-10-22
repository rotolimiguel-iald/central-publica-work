# TESTES — INTEGRAÇÃO (conserto ACOM 12/10)

Rodados em 2026-10-13T04:28:34.255772+00:00 com `C:\Python314\python.exe` sobre CÓPIAS do candidato (`testes\`), sob a guarda `sitecustomize.py` da auditoria. Nenhuma chamada a provedor. Resultado medido aqui [REAL]: **55 testes, 55 PASSA, 0 FALHA, 0 pulado(s)** — todas as suítes OK.

| suíte | módulos | rodados | PASSA | FALHA | segundos | OK |
|---|---|---|---|---|---|---|
| FILA 55 (origem) | test_coordination, test_optional_work, test_transport, test_maximum_coordination, test_request_controls, test_provider_memory.AllAdapterMemoryTests, test_canonical_memory | 55 | 55 | 0 | 25.47 | sim |

## Cada teste

| suíte | módulo | teste | resultado |
|---|---|---|---|
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

## Guarda de execução (auditoria)

processos sob guarda nesta rodada: 1; eventos por tipo: `{"GUARD_ON": 1, "CTYPES_DLOPEN": 1, "READ_OUTSIDE": 20, "SQLITE_RO_OUTSIDE": 67}`; bloqueios: 0

