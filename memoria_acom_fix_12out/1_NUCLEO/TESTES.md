# FRENTE NUCLEO — conserto ACOM 12/10 — TESTES (rodada final 13/10/2026 00:48–00:49)

Construtor da frente NÚCLEO (D1 estado por delta; D2 diário, instantâneos, migração, arquivamento), subagente da gerência c1. Tudo rodou em **cópia** (`1_NUCLEO\copia\MEMORIA_IALD\lib\iald_memory`) e em **bancos sintéticos** criados pelos próprios testes; da produção só se leu código e metadados (e conferiu-se por `cmp` que `originais` é byte-igual aos arquivos instalados); nada foi escrito fora de `1_NUCLEO`. Estatutos: [REAL] medido aqui · [DERIVED] · [DECLARADO] · [INPUT] · [OPEN].

Esta é a segunda sessão da frente. A primeira (12/10, 20:09–20:32) construiu a v2 e fechou 51/51; esta («Continue») reexecutou as suítes sobre os bytes finais daquela sessão, encontrou **1 falha** (`test_transition_time_bounded_n300`: 54,4 ms contra o limiar de 50 ms), perfilou, otimizou o caminho de leitura e de I/O sem mudar a fórmula do hash nem o contrato, acrescentou 3 testes e fechou **54/54**.

## Como rodar (reprodutível)

```
cd "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\1_NUCLEO\tests"
C:\Python314\python.exe -X utf8 run_tests.py test_store test_store_v2
C:\Python314\python.exe -X utf8 guard_summary.py ..
C:\Python314\python.exe -X utf8 make_diff_and_manifest.py   # regenera DIFF.patch e MANIFESTO.json
```

`run_tests.py` fixa o ambiente: `ACOM_AUDIT_ROOT=1_NUCLEO` com a guarda da auditoria (`guard\sitecustomize.py`, byte-igual a `C:\IALD\PROGRAMA_IALD\exame_12out\E_ACOM\guard\sitecustomize.py`, conferido por `cmp`: sem rede, sem escrita/sqlite gravável fora da pasta, sem abrir confidenciais), `PYTHONPATH = guard + copia\MEMORIA_IALD\lib + tests`, `TMP/TEMP` dentro de `1_NUCLEO\tmp`, `IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR` dentro de `1_NUCLEO\tmp` (o «D:» dos testes é uma pasta temporária; `D:\IALD_ARQUIVO` não foi criado). Saída bruta e JSON por suíte em `evidencias\unittest_*.txt|json`. Python 3.14.3, SQLite 3.50.4 [REAL]. Os logs da guarda das rodadas de 12/10 ficaram em `guard_log\rodadas_anteriores_12out`.

Guarda da rodada final [REAL — `evidencias\guarda_resumo.json`]: 17 processos registrados; **0 escritas fora da pasta** (os 4 `BLOCK_WRITE_OUTSIDE` são o próprio Python tentando gravar `.pyc` em `C:\Python314\Lib\...\__pycache__`, bloqueados e inofensivos); leituras fora da pasta só `\\.\nul`; 8 subprocessos, todos Python.

## Resultado da rodada final [REAL]

| suíte | casos | PASSA | FALHA | tempo |
|---|---|---|---|---|
| `tests\test_store.py` (os 20 do core, 1 reescrita obrigatória) | 20 | 20 | 0 | 0,97 s |
| `tests\test_store_v2.py` (novos) | 34 | 34 | 0 | 96,1 s |
| **total** | **54** | **54** | **0** | |

### Iteração desta sessão (13/10), registrada

1. Reexecução das suítes sobre o `store.py` de 20:32:39 (gravado DEPOIS da última rodada de 12/10, 20:27): 20/20 e 30/31; **FALHA** `test_transition_time_bounded_n300` — mediana dos últimos 100 em N=300 = **54,4 ms** (limiar 50 ms). A rodada de 12/10 já registrava margem pequena (45,3 ms).
2. Perfil (`evidencias\perfil\profile_n300.py`, cProfile, N=250..300): as duas `_read` por transição faziam `json.loads` + `_actor`/`_clone` + `_dump` de **todos** os 300 eventos só para recomputar o digest (≈56 mil `dumps` em 50 transições); `open()` de arquivo para escrita/leitura-após-escrita custava 2–4,6 ms cada (`evidencias\perfil\custo_io_13out.txt`: `rb` 0,15 ms, `ab` 0,19 ms, `r+b` 4,2–4,9 ms, `tmp+fsync+replace` 2,2–2,7 ms, reabrir o diário recém-acrescentado 4,6 ms, `stat` 0,03 ms).
3. Otimizações aplicadas na cópia, nenhuma muda a fórmula do hash nem o contrato público:
   - `_event_hash_stored`: digest por concatenação do JSON canônico armazenado (`actor_json`, `changes_json`) — a mesma string que `_dump` produziria —, com **fallback à fórmula completa** (`_event_hash`) quando a stored-JSON não é canônica; a desserialização passa a ocorrer só na âncora e nos deltas posteriores ao último instantâneo (`verify(deep=True)` continua a usar a fórmula completa em todo evento). Teste novo prova a igualdade e o fallback.
   - Diário: rabo lido em `rb` e acréscimo em `ab` (uma tentativa intermediária de «abertura única» em `r+b` saiu 20× mais cara e foi revertida pela medida); cache em memória do rabo do último acréscimo **confirmado**, validado por `stat` (tamanho + `mtime_ns`); entrada descartada antes de cada acréscimo e reposta só após o commit.
   - Contador da política de instantâneos movido do arquivo `snapshot_policy.json` para a tabela `snapshot_policy` do próprio banco (uma linha, gatilho contra DELETE, lida antes da cópia e atualizada depois dela na transação da mutação). Conta mutações confirmadas; sem I/O de arquivo; sem arquivo rasgado capaz de bloquear mutações. **Desvio declarado em relação à especificação de 12/10** (que previa o `.json`); o esquema passa a ter 10 gatilhos (a especificação dizia 9).
   - Perfil sob cProfile: 73,7 → 49,6 → 47,2 → 40,0 → **34,1 ms**; sem profiler, na suíte: 54,4 → **30,2 ms** (mediana dos últimos 100 em N=300, rodada final).
4. Rodada intermediária: 20/20 e 29/32 — 3 falhas, todas de **teste**: a asserção nova do teste de 50 mutações comparava a linha do banco com uma política capturada 50 mutações antes (e deixava a conexão aberta na falha → ERROR de limpeza no Windows); o teste de 60 min injetava o relógio **depois** de `MemoryStore()` ter nascido a política com o relógio real — a política voltou a nascer na primeira mutação (como na versão de 12/10; a migração insere a linha explicitamente). Corrigidos; rodada final 54/54.
5. `run_tests.py` passou a contar os testes cujo docstring empurra o veredito para a linha seguinte (antes contava 31 de 33).
6. Medido antes de fechar: `Path.write_text` no Windows traduz LF em CRLF; os arquivos reescritos por script nesta sessão (store.py, journal.py, snapshots.py, migrate.py, test_store_v2.py, run_tests.py, CORE.md) tinham virado CRLF enquanto os originais são LF. Normalizados **por bytes** para LF (a pasta `originais` ficou intocada) e a rodada final repetida sobre os bytes finais — os números desta página são dessa rodada (00:48–00:49); os bytes do banco/diário/instantâneos são determinísticos e iguais aos da rodada anterior; os tempos variam com a carga.

### `test_store.py` — os 20 existentes (v1) contra a v2

| teste | resultado | observação |
|---|---|---|
| test_original_bytes_and_strict_idempotent_anchor | PASSA | |
| test_state_and_flow_commit_together_and_survive_restart | PASSA | **reescrito** (D1/D2): nenhum `memory.sqlite3.bak_*`; diário com 2 linhas (`anchor`, `event`) encadeadas; `context_state.revision == 1`; `state_json == ''` no evento 1; `journal_ok` |
| test_cas_and_stable_replay | PASSA | |
| test_cross_scope_all_entry_points | PASSA | |
| test_model_cannot_establish_anchor_or_flow_or_promote_output | PASSA | |
| test_constraints_immutable_and_children_inherit | PASSA | |
| test_errata_are_additive_and_handles_merge | PASSA | |
| test_projection_is_bounded_auditable_and_does_not_destroy | PASSA | |
| test_projection_never_separates_original_and_correction | PASSA | |
| test_steering_after_original_goal_is_required_or_overflows | PASSA | |
| test_all_consolidated_record_types_cannot_disappear_under_compaction | PASSA | |
| test_explicitly_required_candidate_never_drops_and_remains_unverified | PASSA | |
| test_database_update_delete_guards | PASSA | |
| test_tampered_blob_and_missing_guard_fail_closed | PASSA | |
| test_tampered_chain_with_guards_restored_fails | PASSA | |
| test_failure_after_insert_rolls_back_q_and_p | PASSA | depende das 2 chamadas a `_read` por transição — mantidas |
| test_abrupt_process_exit_recovers_whole_previous_state | PASSA | morte do processo após INSERT + diário e antes do commit; o banco volta inteiro |
| test_tampered_objective_with_guards_restored_fails | PASSA | |
| test_validation_rejects_path_identifiers_and_nonfinite_values | PASSA | |
| test_concurrent_processes_no_lost_records_or_handles | PASSA | 5 processos escritores |

### `test_store_v2.py` — os 34 novos (31 de 12/10 + 3 de 13/10, marcados ★)

| classe.teste | resultado | o que prova |
|---|---|---|
| FrozenAndContract.test_v1_frozen_copy_is_pinned | PASSA | `tests\store_v1_frozen.py` tem sha256 = `tests\store_v1_frozen.sha256` (lido do artefato por script; `2d4f6214fa433534…` = store.py instalado) |
| FrozenAndContract.test_public_contract_fields_unchanged | PASSA | chaves de snapshot (14), recibo (9), projeção (10) e `verify` ⊇ v1; exportações v1 ⊂ `__all__` + `SchemaMigrationRequired`; CAS, replay idempotente e invariante de modelo preservados |
| DeltaReplay.test_delta_events_store_no_state_and_replay_from_snapshot | PASSA | `state_json == ''` nas transições; âncora com estado inicial; `snapshots` a cada 4 revisões (constante reduzida no teste); `replay_from_revision` = último instantâneo; `verify(deep=True)` replaya de 0 |
| DeltaReplay.test_errata_and_handles_replay_identically_through_snapshots | PASSA | erratas, merge de handles e fase atravessam instantâneos sem mudar; duplicata recusada; projeção com linhagem |
| ★ DeltaReplay.test_stored_json_digest_equals_v1_formula_and_falls_back_when_noncanonical | PASSA | `_event_hash_stored == _event_hash == event_hash` em todas as linhas; linha montada à mão com JSON **não canônico** e digest v1 correto (calculado pelo código v1 congelado) é aceita pelo leitor v2 via fallback; adulterar essa linha é recusado |
| TamperFailsClosed.test_materialized_row_tamper_fails_closed | PASSA | `context_state.state_json` adulterado → `IntegrityError('Materialized…')` em `get` e `transition` |
| TamperFailsClosed.test_context_state_revision_lag_fails_closed | PASSA | revisão materializada atrasada → `IntegrityError('…lags…')` |
| TamperFailsClosed.test_snapshot_row_tamper_fails_closed | PASSA | gatilhos de `snapshots`/`context_state` barram DELETE/UPDATE; gatilho derrubado + linha adulterada + gatilho restaurado → recusa (raso e profundo) |
| TamperFailsClosed.test_delta_event_tamper_fails_closed | PASSA | `changes_json` de evento delta adulterado → digest da cadeia recusa |
| TamperFailsClosed.test_stray_snapshot_beyond_head_fails_closed | PASSA | linha `snapshots` além da cabeça → recusa |
| Journal.test_journal_written_before_commit_and_orphan_voided | PASSA | falha após o append e antes do commit: banco na revisão anterior, linha órfã visível (`journal_orphans=1`); a transição seguinte acrescenta `void` e segue; cadeia íntegra; `journal_ok` |
| Journal.test_abrupt_exit_after_journal_append_voids_orphan | PASSA | mesmo cenário com `os._exit(73)` em processo filho |
| Journal.test_journal_missing_or_truncated_is_visible | PASSA | linha truncada (morte a meio da escrita) fica contada como malformada e não corrompe a próxima; diário apagado → `ok=False`, `journal_ok=False`, `journal_missing_events` = eventos; leituras não dependem do diário |
| Journal.test_journal_chain_and_rebuild_equals_db | PASSA | `rebuild_from_journal` reconstrói 2 contextos (um com `:` no id, filho com restrições herdadas, erratas, handles): `get` idêntico, recibos iguais, `verify(deep=True)` ok; recusa reconstruir sobre raiz ocupada |
| ★ Journal.test_journal_tail_cache_validated_by_stat_across_instances | PASSA | duas instâncias alternam acréscimos: cache obsoleto é rejeitado pelo `stat` e relido — cadeia íntegra, 0 `void`, 0 órfãs; transição falhada descarta a entrada do cache e a órfã é anulada no acréscimo seguinte (`journal_voided=1`, `journal_orphans=0`) |
| SnapshotPolicy.test_snapshot_policy_50_mutations | PASSA | 49 mutações → 0 instantâneos; 50ª → 1, cópia é um sqlite válido na revisão pré-mutação (48), sidecar `.sha256` confere, contador zera; 100ª → 2; nenhum `.bak_`; **não existe `snapshot_policy.json`**; a linha `snapshot_policy` do banco == `snapshot_policy()` e não aceita DELETE |
| ★ SnapshotPolicy.test_snapshot_policy_counts_committed_mutations_only | PASSA | mutação que falha depois de avaliada a política não avança o contador (3 → 3) nem a revisão |
| SnapshotPolicy.test_snapshot_policy_60_minutes | PASSA | relógio injetado: 3599 s → nada; 3600 s → instantâneo; janela reinicia no instantâneo |
| SnapshotPolicy.test_snapshot_keep3_and_archive_move_verified | PASSA | 12 mutações a cada 2 → 6 instantâneos: 3 locais, 3 movidos ao «D:» com sidecar, `MANIFEST.jsonl` com sha256 igual ao arquivo; nenhum aviso |
| SnapshotPolicy.test_archive_unavailable_keeps_local_copies | PASSA | arquivo indisponível → 6 locais mantidos, `AVISOS.jsonl` + `RuntimeWarning`; mutações nunca bloqueadas |
| SnapshotPolicy.test_due_snapshot_that_does_not_verify_fails_the_mutation | PASSA | instantâneo devido que não confere → `IntegrityError`, mutação não acontece (fail-closed) |
| ArchiveLegacyBackups.test_archive_legacy_backups_mover_manifest_and_sha | PASSA | 12 `.bak_` sintéticos, `keep=3`: dry-run não toca nada; 9 movidos, sha256 origem = destino = manifesto, `MANIFEST.json` consistente; `memory.sqlite3`, `snapshots`, `journal` intocados; segunda execução move 0 (idempotente) |
| ArchiveLegacyBackups.test_archive_legacy_backups_corrupt_copy_aborts_without_deleting | PASSA | cópia corrompida de propósito no 3º arquivo: 2 movidos, aborto visível, origem preservada, parcial renomeada `.mismatch` |
| Migration.test_legacy_v1_db_refused_without_migration | PASSA | banco v1 (código congelado) → `SchemaMigrationRequired` (é `IntegrityError`); bytes do banco iguais depois da recusa |
| Migration.test_migration_dry_run_writes_nothing | PASSA | dry-run devolve cabeças, não cria backup, diário nem muda bytes |
| Migration.test_migration_preserves_head_state_sha_and_chain | PASSA | 3 contextos (200/5/0 eventos): backup `pre_v2` + sidecar + 2ª cópia iguais; `schema_version='2'`, `schema_upgrade_2_at`; **linhas de `events` e `contexts` byte-iguais**; `snapshots` `migration_v2` e `context_state` na cabeça; `verify(deep=True)` ok; recibos e `get` iguais aos da v1; diário com N+1 linhas `legacy:true`; `metadata` segue imutável |
| Migration.test_migration_is_idempotent | PASSA | segunda execução: `already_migrated`, sha256 do banco igual, diário igual, nenhum backup novo; `append_many` re-executado escreve 0 linhas |
| Migration.test_mixed_legacy_delta_replay | PASSA | 200 legados + 60 deltas: estado completo, `legacy_events=200`, `delta_events=60`, `replay_from_revision=256`, `state_json==''` só em 201..260 |
| Migration.test_v1_code_refuses_v2_schema | PASSA | o código v1 congelado recusa o banco migrado (`Unsupported or missing memory schema`) |
| Migration.test_covering_index_serves_chain_reads_without_legacy_state | PASSA | contexto legado com 35,7 MB de `state_json` (121 eventos): plano `SEARCH events USING COVERING INDEX events_chain_idx`; `get` v2 32 ms vs v1 273 ms, resultado idêntico (`evidencias\indice_cobertura_legado.json`) |
| Scripts.test_migrar_para_delta_cli_dry_run_apply_verify | PASSA | CLI em subprocesso: dry-run → `--apply --second-copy-dir --receipt` → `--verify-only --deep` → `--apply` de novo (`already_migrated`) → `--rebuild-from-journal`; raiz inexistente → código 1 e `ok:false` |
| Scripts.test_mover_backups_antigos_cli | PASSA | CLI em subprocesso com 6 arquivos pequenos: dry-run não move; `--keep 3` move 3, mantém os 3 mais recentes, `memory.sqlite3` intocado |
| GrowthN300.test_growth_n300_bytes_db_journal_snapshots | PASSA | ver tabela abaixo; grava `evidencias\crescimento_n300.json` |
| GrowthN300.test_transition_time_bounded_n300 | PASSA | mediana da transição < 50 ms (geral e na última centena) e `get` < 50 ms em N=300 — **30,2 ms / 17,3 ms / 10,6 ms** |

## Crescimento N=300 — números [REAL — `evidencias\crescimento_n300.json`, rodada final] e comparação com a auditoria

Gerador: um contexto, 300 candidatos `DECLARADO` de ~1,35 KB cada (`changes_json` médio 1.354,9 B; a auditoria usou ~1.313 B), fase atualizada a cada transição; política de instantâneos de produção (50 mutações / 60 min), 3 locais, arquivo em pasta temporária; sob a guarda da auditoria.

| N | banco (B) | diário (B) | instantâneos locais / arquivados (B) | transição mediana (últimos 100) | p90 | `get` mediana |
|---|---|---|---|---|---|---|
| 100 | 991.232 | 202.816 | 2 / 0 (1.470.464 / 0) | 10,2 ms | 13,7 ms | 3,7 ms |
| 200 | 1.921.024 | 405.216 | 3 / 1 (4.317.184 / 499.712) | 17,2 ms | 28,2 ms | 9,4 ms |
| 300 | 3.215.360 | 607.616 | 3 / 3 (7.475.200 / 2.912.256) | 30,2 ms | 34,1 ms | 10,6 ms |

| grandeza | v2 medida [REAL] | v1 (auditoria 12/10, N=50→150) [DECLARADO pela auditoria] | leitura |
|---|---|---|---|
| expoente do banco em N | **1,07** (100→300) | 1,87 (assíntota 2) | o banco deixou de carregar o estado inteiro por evento; o resto é a linha materializada reescrita, o índice de cobertura (cópia de `changes_json`) e a linha `snapshots` em 256 |
| banco em N=300 | **3,22 MB** | ≈ 54,8 MB extrapolado de 15,0 MB em N=150 [DERIVED] | 17× menor |
| incremento (300−200)/(200−100) | 1,39 | — | dentro de [0,7; 1,5]; crescimento ≈ linear com termos constantes |
| expoente do diário | **1,00** | — | linear por construção; +3,5 % sobre N×(|changes|+600 B) |
| expoente do total de bytes de instantâneos | **1,78** (Σ de 6 cópias de um banco linear) | 2,78 nos backups por mutação (assíntota 3) | total em N=300: **10,4 MB** (7,5 locais + 2,9 arquivados) contra ≈ 5,19 GB da v1 extrapolados [DERIVED]; a pegada local é limitada a 3 cópias |
| tempo por transição | mediana geral **17,3 ms**; 10,2 / 17,2 / 30,2 ms por centena; p90 34,1 ms em N=300; máx. 93,6 ms (mutação com instantâneo) | 0,41 s em N=150, expoente 1,36 | ainda cresce ≈ linearmente com N porque toda leitura verifica a cadeia inteira (duas vezes por transição) e reescreve o estado materializado; a garantia é a da v1 com custo linear |

Honestidades: (a) o limiar de 50 ms foi cumprido com margem de ~20 ms na última centena (na primeira rodada de hoje falhou a 54,4 ms, com a máquina a ~14 % de CPU e llama-server/ChatGPT/Codex vivos — o tempo de parede depende da carga; a diferença veio do código, medida por perfil, não de afrouxar o limiar); (b) o «60 min» foi testado com relógio injetado, não com relógio de parede; (c) o «D:» dos testes é uma pasta temporária; `D:\IALD_ARQUIVO` não existe e não foi criado (ato da gerência, passo M5); (d) nenhum teste tocou o banco de produção (357 MB) nem os 764 backups reais: `mover_backups_antigos.py` só foi ensaiado com arquivos pequenos sintéticos, como ordenado; (e) extrapolação para o heartbeat (735 eventos): ≈ 60–70 ms por transição [DERIVED], contra 5,3 s + cópia de 357 MB hoje; (f) o cache do rabo do diário é por instância e por processo; um acerto errado (mesmo tamanho **e** mesmo `mtime_ns` após modificação externa) quebraria a cadeia do diário de forma visível em `verify`, nunca o banco.

## Desvios declarados em relação à especificação de 12/10 (`0_DIAGNOSTICO\ESPECIFICACAO.md`)

1. Contador da política de instantâneos em tabela `snapshot_policy` do banco, não em `state\snapshot_policy.json` (motivo medido acima); 10 gatilhos, não 9.
2. Scripts entregues com os nomes pedidos na TAREFA (`migrar_para_delta.py`, `mover_backups_antigos.py`); o `memoria_admin.py` da especificação (`status | verify-all | rebuild-from-journal | archive-backups | snapshot-now`) não foi construído — `verify-all`/`rebuild-from-journal` existem como `--verify-only`/`--rebuild-from-journal` do primeiro e `archive-backups` é o segundo; `status` e `snapshot-now` ficam [OPEN].
3. `test_escritorio_scope_refused` (D6) não pertence a esta frente e não foi escrito.

## O que NÃO foi testado aqui
Migração do banco de produção (M4), arquivamento dos 764 backups reais (M5), reinício do filho web (M7), D3/D4/D5/D6 (outras frentes), adaptadores (`session_memory.py`, `iald_app_memory.py`, fila) contra a v2 — o contrato público não mudou, mas a conferência das suítes SESSOES 17 / APP 31 / FILA 55 contra a lib v2 pertence ao passo M6. Relógio de parede para o gatilho de 60 min. Carga concorrente de vários processos contra o cache do diário além do teste de duas instâncias no mesmo processo e dos 5 escritores do core.
