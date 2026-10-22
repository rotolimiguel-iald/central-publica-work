DIAGNÓSTICO ACOM — 12/10

# ESPECIFICAÇÃO — correção da memória comum da IALD (decisões D1–D6)

Diagnosticador da memória ACOM, subagente da gerência c1 (sessão 6da8f00d). Escrevi só em
`C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\0_DIAGNOSTICO\` (este arquivo, `ESPECIFICACAO.json`
e `evidencias\`). Nada em produção foi tocado; nenhum provedor, nenhuma rede, nenhum script de selo. Hashes por
script. Estatutos: [REAL] medido aqui · [DERIVED] · [DECLARADO] · [INPUT] decisão da gerência · [OPEN] · [KNOWN].

Fonte da ordem do operador [REAL, hash lido do arquivo]:
`C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt`,
1.342 B, sha256 `78ef70e6f9868281d44e8a306e60a0cb162843e54f3a74389ddf14ed325d535d` (sha16 `78ef70e6f9868281`,
igual ao declarado) — linha 1: «resolva a questão da memória».
Auditoria lida inteira [REAL]: `C:\IALD\PROGRAMA_IALD\exame_12out\E_ACOM\AUDITORIA_F9_MEMORIA_ACOM_C1.md`
(29.137 B, sha16 `e44bb32480c80f63`).

**Protocolo ACOM desta tarefa:** NÃO inscrevi esta tarefa no banco de produção. Motivo: a ordem desta tarefa
proíbe qualquer escrita em `C:\IALD\MEMORIA_IALD`, e hoje cada `init`/`transition` custa uma cópia integral de
357 MB (é o defeito P1 que esta especificação corrige). A referência da tarefa é da gerência c1. Registro o
desvio aqui, com o motivo, como fez a auditoria.

---

## 0. Resumo executivo

1. **Inventário [REAL, 12/10 19:42:56]:** banco `memory.sqlite3` com **357.326.848 B**; **764 backups
   integrais** somando **92.265.140.224 B** (85,9 GiB) na mesma pasta; **7 contextos, 764 eventos**; o contexto
   do heartbeat (`IALD_APP_SERVICES / service.native-heartbeat`) tem **735 eventos** e **354.555.543 caracteres
   de `state_json` (99,3 % do banco)**. A soma de todos os `changes_json` é **1.116.685 caracteres**: o estado
   por delta (D1) reduz o volume armazenado por evento em **≈318×** [DERIVED das duas somas].
   Entre 19:32:50 e 19:42:56 (minha primeira e segunda medição) nasceu 1 contexto novo e 1 backup de 357 MB:
   o custo está vivo, não é hipótese.
2. **Heartbeat:** parado em STANDBY desde o reinício de 12/10 11:05 (`[Heartbeat] Adiado — llama-server
   offline` no log r1) [REAL]; o llama voltou (PID 34752, :8081) mas o heartbeat só arma no boot. O último
   evento do heartbeat no banco é 11/10 20:57:31Z (= 17:57 local), mesmo instante do mtime do
   `iald_psion_state_32B.json` [REAL]. A projeção da memória entrou na janela cronometrada
   (`_operational_native_payload` dentro de `t0…elapsed`, linhas 3188–3200) e 10 `tool_result` por batida
   gravam o corpo das respostas no banco (linha 3205).
3. **Psion:** existe cópia anterior a 10/10 09:20 — `D:\IALD\projetos_pyhton\IALD\iald_psion_state_32B.json`
   (24.011 B, mtime 27/09 04:00:05, sha256 `f9a5ec88…`) e a série diária `D:\_VERSOES\…` até 27/09 — mas
   **há dúvida** (13 dias de batidas legítimas entre 27/09 e 10/10 09:11; outros programas referenciam o
   arquivo). Pela própria D3(c): **não restaurar automaticamente; parar o feed degradado e relatar** (§3.3).
4. **Filtros:** as lacunas da auditoria são reproduzíveis por leitura do código: `FORBIDDEN_NAMES` exato
   (`session_memory.py` l.14), `protected_path` exato (`iald_app_memory.py` l.541–543), projeção do app sem
   filtro de conteúdo (`projection()` l.133–142), `policy.FORBIDDEN` sem Escritório (l.8). D4 desenha um
   guarda único compartilhado (`guard.py`) e os pontos exatos de inserção (§4).
5. **Blocos:** os cinco arquivos têm no topo o bloco de 620 B (sha16 `3106d7234c7a3b71`; no CLAUDE.md da
   IALD Nativa, 624 B em CRLF, sha16 `2ca1cb060ecd2119`) [REAL]; em todos os cinco o restante começa com os
   bytes do backup de 10/10 (verificado por prefixo) [REAL]. D5 substitui só o bloco (§5).
6. **Testes:** 123 casos existentes devem continuar passando, **com duas reescritas obrigatórias**
   (uma no CORE, uma no APP) porque afirmam o comportamento que D2 e D3 mudam (§7.1). Os novos testes estão
   nomeados um a um (§7.2), incluindo o crescimento N=300 medindo bytes do banco, do diário e dos instantâneos.

---

## 1. Inventário [REAL] do estado atual (metadados e contagens; nenhum conteúdo lido)

Fonte: `evidencias\INVENTARIO_MEMORIA_12out.json` (gerado por `sqlite3` em `mode=ro&immutable=1`, só
`count`/`length`/`substr`), `evidencias\PSION_BACKUPS_METADADOS_12out.json`, `Get-NetTCPConnection`,
`Get-CimInstance Win32_Process`, `Get-FileHash`.

### 1.1 Banco comum — `C:\IALD\MEMORIA_IALD\state\memory.sqlite3`
| medida | valor |
|---|---|
| bytes | 357.326.848 (mtime 12/10 19:38:51) |
| journal_mode / page_size / page_count / freelist | delete / 4096 / 87.238 / 0 |
| cabeçalho | `SQLite format 3`, write/read version 1/1 (não-WAL) |
| metadata | `schema_version = 1` |
| tabelas / gatilhos | `contexts`, `events`, `metadata` / 6 gatilhos `*_no_update`/`*_no_delete` |
| arquivos laterais `-journal/-wal/-shm` | ausentes |
| contextos / eventos | 7 / 764 |
| Σ `length(state_json)` / Σ `length(changes_json)` | 354.699.793 / 1.116.685 caracteres |
| `app_outbox\` | 1 pasta, 1.468 arquivos (734 `.json` + 734 `.committed`), 1.841.400 B |

### 1.2 Contextos (só contagens; `context_id` abreviado)
| contexto | house / principal | eventos | Σ state (chars) | máx. state | registros no último estado | último evento (UTC) |
|---|---|---|---|---|---|---|
| `a3f615c9-a7d…` | IALD / operator (inscrição de 12.788 B) | 7 | 41.564 | 11.437 | 10 (9 fact/REAL, 1 erratum/REAL) | 2026-10-12T22:26:16 |
| `app_service_…` | IALD_APP_SERVICES / service.native-heartbeat | **735** | **354.555.543** | 964.334 | 734 candidate/DECLARADO | 2026-10-11T20:57:31 |
| `84a8b4da-fdd…` | IALD / luiz-antonio-rotoli-miguel | 13 | 81.729 | 13.324 | 12 | 2026-10-10T14:07:12 |
| `a228d32a-518…` | IALD / operator | 3 | 5.851 | 3.982 | 8 | 2026-10-12T14:26:53 |
| `1bcf55a4-06f…` | IALD / operator | 4 | 14.952 | 7.543 | 12 (inclui 1 pending/LEGAL) | 2026-10-12T17:20:07 |
| `31488c7e-d2d…` | IALD / operator | 1 | 77 | 77 | 0 | 2026-10-12T22:13:34 |
| `f8cd4426-a75…` | IALD / operator | 1 | — | — | 0 | 2026-10-12T22:38:51 |

Eventos por dia (UTC): 10/10 = 283 · 11/10 = 468 · 12/10 = 13. O heartbeat tem 124 `actor_json` distintos
(um par system/agent por ciclo) [REAL].

### 1.3 Backups integrais na mesma pasta
| medida | valor |
|---|---|
| quantidade | **764** (`memory.sqlite3.bak_<data>_<uuid8>`) |
| soma | **92.265.140.224 B** |
| primeiro / último | `…bak_20261010_092013_691200_60d7eee3` (32.768 B) / `…bak_20261012_193850_427393_3b8a9bea` |
| por dia | 10/10 = 355 · 11/10 = 396 · 12/10 = 13 |
| maior / menor | 357.314.560 B / 32.768 B |
| três mais recentes (19:42) | `…_191333_…_99396e79`, `…_191625_…_852ddc4a`, `…_192616_…_fe055081`, e depois `…_193850_…_3b8a9bea` |

### 1.4 Processos (portas 8081/8082) e heartbeat
| porta | PID | processo | início | observação |
|---|---|---|---|---|
| 8082 | 64412 | `C:\Python314\python.exe iald_web_server.py 8082` | 12/10 11:05:38 | pai PID 58980 = `powershell … start_iald_web.ps1` (supervisor) |
| 8081 | 34752 | `llama-server.exe` (IALD-Native-v3-Qwen3.6-35B-A3B-Q4_K_M) | 12/10 11:04:27 | online agora |

Log atual `logs\web-server_20261012_110528_r1.log`: `Heartbeat: STANDBY (llama offline)` e `[Heartbeat] Adiado —
llama-server offline` (o supervisor sondou o :8081 às 11:05:37, antes de o llama responder) [REAL]. Logo **não há
batida desde 11/10 17:57** e nenhum evento do heartbeat em 12/10 [REAL, banco]. O web server anterior morreu em
11/10 17:59:13 (`web-supervisor.log`: `reiniciando em 5 s…`); últimas batidas registradas: 7,3 / 7,2 / 7,1 tok/s
contra baseline 52,96 → 51,86 [REAL, log]. Em 7 processos `mcp_server.py` da fila (11:05–11:08) e 7 `mcp_um.py`
estão vivos [REAL]; se já importaram `iald_memory`, carregam a v1 (§8, R2).

### 1.5 Psion (só nome, bytes, mtime, sha256 — conteúdo nunca lido)
| arquivo | bytes | mtime | sha256 |
|---|---|---|---|
| `C:\IALD\projetos_pyhton\IALD\iald_psion_state_32B.json` (atual) | 23.977 | 2026-10-11 17:57:18.539 | `aa6387e6dd75782e7f4bc4597690e013da46627a1d4771513207881f77c93758` |
| `C:\IALD\projetos_pyhton\IALD\iald_psion_state.json` | 2.722 | 2026-03-09 09:21:38 | `541ccfed77944fa0cb4b7e0186d38a111812644400de4cf94f4ab205241ce512` |
| `D:\IALD\projetos_pyhton\IALD\iald_psion_state_32B.json` (espelho) | 24.011 | **2026-09-27 04:00:05** | `f9a5ec88aa212f0a182154fca1859743fd30de07b8df83f5a4fdae9040abe7af` |
| `D:\_VERSOES\2026-09-27T04-00-02\projetos_pyhton\IALD\iald_psion_state_32B.json` | 24.019 | 2026-09-26 03:54:12 | `b7b5842a455fbe453fb77b861b1eef0f62cced9dabc0122692886dda8f0bab4a` |
| `D:\_VERSOES\2026-09-26T04-00-02\…` | 24.022 | 2026-09-25 03:48:17 | `3a7c76c2be52f1d17c2c75b80d2178702a61da6906a57c62d0d774b69d1477b7` |

Série diária em `D:\_VERSOES\` de 2026-08-19 a 2026-09-27 (última pasta `2026-09-27T04-00-02`); **nenhuma cópia
entre 27/09 e 10/10 09:20**; nenhum `*.bak_*` do psion em `C:\IALD` nem em `C:\Users\rotol` [REAL, busca por nome
em C:\IALD, D:\ (profundidade 5) e C:\Users\rotol (profundidade 6), excluído tudo que contém «Escrit»].

### 1.6 Discos e caminhos
C: 3.724,9 GB, **890,2 GB livres**; D: 3.726 GB, **1.954,5 GB livres**; `D:\IALD_ARQUIVO` **não existe** ainda;
`LongPathsEnabled = 0` (limite de 260 caracteres por caminho) [REAL].

### 1.7 Código instalado (hash lido do disco) — bate com os recibos
Core: `store.py` `2d4f6214fa433534` (31.434 B), `__init__.py` `fc534f8d3b18cddd`, `session_memory.py`
`c9c3aa2135235723` (10.233 B), `session_hook.py` `f39fba680caa9472`, `SESSION_BRIDGE.md` `49f1626d52d9cd6c` (887 B),
`README.md` `57f63b419a2149a2`, `CORE.md` `4691f443fcf81a7c`, `SESSION_MEMORY.md` `fe6fd24b6900710d`.
App: os 8 alvos do `APP_DEPLOYMENT.json` batem (`iald_web_server.py` `7e48e90afcad6b05`, 733.452 B; backup
`43eb137702dea4b1`, 728.600 B; diff de 361 linhas em `evidencias\diff_iald_web_server_bak20261010_vs_instalado.txt`).
Fila: os 9 alvos do `QUEUE_DEPLOYMENT.json` batem (`operational_memory.py` `1d6bf484063b118b`, etc.).

### 1.8 Superfícies de instrução (D5) [REAL]
| arquivo | bytes | sha16 do arquivo | bloco no topo | restante após o bloco |
|---|---|---|---|---|
| `C:\Users\rotol\.claude\CLAUDE.md` | 30.145 | `0ba264cb1f504a44` | 620 B LF, `3106d7234c7a3b71` | começa com o backup de 10/10 (26.251 B) + 3.274 B acrescidos no fim |
| `C:\Users\rotol\.codex\AGENTS.md` | 80.123 | `6e44107cb52ae846` | 620 B LF, `3106d7234c7a3b71` | idem (76.229 B) + 3.274 B |
| `C:\IALD\projetos_pyhton\IALD\CLAUDE.md` | 535.893 | `1e07f4ea610ec1c9` | **624 B CRLF, `2ca1cb060ecd2119`** | backup (531.975 B) + 3.294 B |
| `C:\IALD\PROGRAMA_IALD\README.md` | 6.332 | `5b8ef990a3aa1090` | 620 B LF, `3106d7234c7a3b71` | **igual** ao backup (5.712 B) |
| `…\IALD_ORQUESTRACAO_20260923\COORDINATOR.md` | 66.471 | `42746e6f2c15d317` | 620 B LF, `3106d7234c7a3b71` | **igual** ao backup (65.851 B) |

`MEMORY.md` da Central: 18.419 B, 166 linhas, mtime **12/10 19:31:42** (foi mexido por outra sessão durante este
diagnóstico; a auditoria media 229 linhas ao meio-dia); a linha-alvo é a 14: `- Memória ACOM: …`.

---

## 2. D1 — ESTADO POR DELTA [INPUT]

### 2.1 Causa no código (store.py `2d4f6214fa433534`)
- `transition` l.525–533 grava `state_json` **inteiro** por evento; `_read` l.363–388 **reserializa o estado
  inteiro de cada evento** a cada leitura (`_dump(state)` + comparação) — custo O(N·|estado|): 5,3 s por leitura
  do heartbeat (auditoria) e 354,7 MB de estado redundante no banco [REAL].
- `_apply` l.220–239 clona o estado inteiro (`_clone`) por evento aplicado → replay O(N·|estado|) mesmo em delta.

### 2.2 Desenho
**Esquema v2** (`SCHEMA_VERSION = 2`, l.17; `_SCHEMA` l.252–270 ganha):
```sql
CREATE TABLE IF NOT EXISTS context_state (            -- ÚNICA tabela mutável: o estado corrente materializado
  context_id TEXT PRIMARY KEY REFERENCES contexts(context_id),
  revision INTEGER NOT NULL, state_json TEXT NOT NULL, state_sha256 TEXT NOT NULL,
  event_hash TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS snapshots (                -- instantâneos de estado, só-acréscimo
  context_id TEXT NOT NULL REFERENCES contexts(context_id), revision INTEGER NOT NULL,
  state_json TEXT NOT NULL, state_sha256 TEXT NOT NULL, event_hash TEXT NOT NULL, created_at TEXT NOT NULL,
  reason TEXT NOT NULL,                                -- 'migration_v2' | 'periodic'
  PRIMARY KEY(context_id, revision));
CREATE TRIGGER IF NOT EXISTS context_state_no_delete BEFORE DELETE ON context_state BEGIN SELECT RAISE(ABORT,'materialized state is not deletable'); END;
CREATE TRIGGER IF NOT EXISTS snapshots_no_update BEFORE UPDATE ON snapshots BEGIN SELECT RAISE(ABORT,'append-only snapshot'); END;
CREATE TRIGGER IF NOT EXISTS snapshots_no_delete BEFORE DELETE ON snapshots BEGIN SELECT RAISE(ABORT,'append-only snapshot'); END;
```
- `events` **não muda de forma**: eventos em modo delta gravam `state_json = ''` (coluna segue `NOT NULL`) e
  `state_sha256` do estado resultante; `changes_json`, `previous_hash`, `event_hash` e `_event_hash()` (l.246–249)
  ficam **idênticos** — a cadeia de hashes é a mesma fórmula, então eventos legados e delta encadeiam sem quebra.
- **Eventos legados ficam como estão** (gatilhos `events_no_update/no_delete` mantidos). Um evento é "legado"
  sse `state_json != ''`.
- **Leitura (`_read`, l.341–399):** (1) confere âncora e envelope do objetivo como hoje; (2) **cadeia de hashes
  inteira** sobre `events` (recalcula `_event_hash` de cada evento a partir de `actor_json`, `changes_json`,
  `state_sha256`, `previous_hash`, `created_at` — sem desserializar `state_json`; custo ≈ O(N·|changes|), pequeno);
  (3) carrega o **último `snapshots`** com `revision ≤ head` (ou o estado inicial se não houver), confere
  `sha256(state_json) == state_sha256` do instantâneo e `event_hash` igual ao do evento daquela revisão;
  (4) aplica os deltas posteriores com `_apply_inplace` (clona uma vez, muta no lugar; eventos legados no trecho
  aplicam seu `changes_json` igualmente e, opcionalmente, conferem o `state_json` legado quando `deep=True`);
  (5) confere `sha256(_dump(estado)) == state_sha256` do último evento **e** `== context_state.state_sha256`
  com `context_state.revision == head` — divergência → `IntegrityError('Materialized state lags or differs')`.
- **Escrita (`transition`, l.503–544):** mesma ordem de hoje (BEGIN IMMEDIATE → `_read` → idempotência → CAS →
  novo evento), depois: `INSERT events(... state_json='' ...)`; `UPDATE context_state SET revision=?,
  state_json=?, state_sha256=?, event_hash=?, updated_at=? WHERE context_id=? AND revision=?` (rowcount ≠ 1 →
  `IntegrityError`); a cada `SNAPSHOT_EVERY_EVENTS = 256` revisões, `INSERT snapshots(..., reason='periodic')`;
  linha de diário (D2a) antes do `commit`; `_read` final de conferência (mantém o par de chamadas a `_read` de
  que os testes `test_failure_after_insert_rolls_back_q_and_p` e `crash_after_insert` dependem).
- **`ensure_context` (l.409–476):** insere `contexts`, `events` rev 0 (como hoje, com `state_json` do estado
  inicial, tamanho 77 B) e **`context_state` rev 0**; linha `anchor` no diário.
- **`verify` (l.495–501):** = leitura completa + conferência do diário (D2a) + `deep=False` por padrão; com
  `deep=True` reserializa também os `state_json` legados (é o que a migração roda antes e depois). Chaves de
  retorno existentes preservadas (`ok`, `event_count`, `objective_bytes`, `receipt`, `validation_scope`); chaves
  **aditivas**: `schema_version`, `replay_from_revision`, `legacy_events`, `delta_events`, `journal_ok`.
- **`__init__` (l.281–303) e `_schema_check` (l.313–324):** banco novo nasce em v2; banco v1 encontrado →
  `SchemaMigrationRequired` (nova exceção, subclasse de `IntegrityError`): **nunca migrar implicitamente**.
  `_schema_check` exige `schema_version == '2'`, os 9 gatilhos e `journal_mode = delete`.
- **Contrato público inalterado:** assinaturas de `ensure_context/get/receipt/project/transition/verify`,
  exceções, campos de snapshot/recibo/projeção. `project` (l.546–623) não muda.
- **Dimensionamento [DERIVED do inventário]:** o contexto do heartbeat, hoje 354,6 MB de estado redundante,
  custaria em delta ≈ 1,08 MB de `changes_json` + 735 × ~200 B de hashes + 1 instantâneo de 0,96 MB por 256
  eventos; o estado materializado (0,96 MB) é reescrito no lugar (páginas reaproveitadas pela freelist, sem
  crescimento).

### 2.3 Arquivos e funções a mudar (D1)
| arquivo | função / ponto | linhas (hoje) | mudança |
|---|---|---|---|
| `C:\IALD\MEMORIA_IALD\lib\iald_memory\store.py` | `SCHEMA_VERSION` | 17 | 1 → 2; `SNAPSHOT_EVERY_EVENTS = 256` |
| idem | `_SCHEMA` | 252–270 | + `context_state`, `snapshots`, 3 gatilhos, índice `snapshots(context_id, revision)` |
| idem | `MemoryStore.__init__` | 281–303 | v1 → `SchemaMigrationRequired`; v2 → ok; vazio → cria v2 |
| idem | `_schema_check` | 313–324 | versão 2 + 9 gatilhos |
| idem | `_backup` | 326–339 | **removida**; substituída por `_journal_append` + `_snapshot_if_due` (D2) |
| idem | `_read` | 341–399 | replay a partir do último instantâneo; cadeia de hashes sem reserializar estados; conferência da linha materializada |
| idem | `_apply` | 220–239 | mantida; + `_apply_inplace(state, changes)` para o loop de replay |
| idem | `ensure_context` | 409–476 | + `context_state` rev 0; + linha `anchor` no diário |
| idem | `transition` | 503–544 | `state_json=''`; `UPDATE context_state` com CAS; instantâneo periódico; diário antes do commit |
| idem | `verify` | 495–501 | `deep=False`; chaves aditivas; conferência do diário |
| `…\lib\iald_memory\__init__.py` | exportações | 6–17 | + `SchemaMigrationRequired`, `ConfidentialContent` (D4) |
| `…\lib\iald_memory\migrate_v2.py` (novo) | `migrate(store_root, *, archive_dir, dry_run)` | — | §6 |
| `C:\IALD\MEMORIA_IALD\memoria_admin.py` (novo) | `status`, `verify-all [--deep]`, `rebuild-from-journal`, `archive-backups`, `snapshot-now` | — | CLI local sem rede; só-leitura exceto `archive-backups`/`snapshot-now` |
| `C:\IALD\MEMORIA_IALD\CORE.md` | §Persistência e limites | 69–75 | correção AO LADO datada (12/10): delta, diário, instantâneos; "backup integral antes de escrita" deixa de valer |

---

## 3. D2 — BACKUP [INPUT]

### 3.1 (a) Diário só-acréscimo por contexto, gravado ANTES do commit
- Pasta `C:\IALD\MEMORIA_IALD\state\journal\`; um arquivo por contexto: `<context_id com ':' → '%3A'>.events.jsonl`
  (`_ID` admite `:`; NTFS não).
- Uma linha JSON (ASCII, sem quebras internas) por mutação, com cadeia própria:
  `{"seq", "kind": "anchor"|"event"|"void", "context_id", "revision", "event_id", "actor_json", "changes_json",
  "state_sha256", "previous_hash", "event_hash", "created_at", "legacy": false, "prev_line_sha256",
  "line_sha256"}`; `line_sha256 = sha256(prev_line_sha256 + canonical(linha sem line_sha256))`. A linha `anchor`
  carrega ainda `scope_json`, `anchor_json` e `objective_b64` → o diário sozinho reconstrói o contexto inteiro.
- **Ordem na transação:** `BEGIN IMMEDIATE` → … → `INSERT events` → `UPDATE context_state` → **append + fsync
  da linha** → `_read` de conferência → `commit`. Morte do processo entre o append e o commit deixa uma linha
  **órfã** (revisão > head do banco): a próxima mutação do contexto detecta e **acrescenta** uma linha `void`
  que a referencia (`reason: not_committed`); nunca se apaga nem reescreve linha. Leituras nunca consultam o
  diário; `verify` confere que **todo evento do banco tem linha com o mesmo `event_hash`** (`journal_ok`).
- Bootstrap na migração: uma linha por evento legado (`legacy: true`), a partir das colunas de `events`.
- Tamanho [DERIVED]: ≈ `changes_json` + 600 B por linha; para os 764 eventos atuais ≈ 1,6 MB no total.

### 3.2 (b) Instantâneo integral do banco (cópia de bytes)
- Política avaliada **no caminho de escrita, sob o lock** (não há daemon): `SNAPSHOT_EVERY_MUTATIONS = 50` ou
  `SNAPSHOT_MAX_AGE_SECONDS = 3600`, o que vier primeiro, **contado desde o último instantâneo** e só quando há
  mutação (sem mutação, nada é copiado — nota para a gerência: "60 minutos" lê-se "na primeira mutação após
  60 minutos"). Contador em `state\snapshot_policy.json` (gravado dentro do lock, tempário + verificação).
- A cópia é feita **antes** da mutação (como o `_backup` de hoje, com o banco em `delete` e sem WAL):
  `state\snapshots\memory.sqlite3.snap_<AAAAMMDD_HHMMSS_us>_<sha16>` + fsync + conferência de tamanho e sha256 +
  sidecar `.sha256`.
- Retenção: manter os **3 mais recentes em C:**; os anteriores são **movidos** (copiar → conferir sha256 →
  apagar origem → linha no `MANIFEST.jsonl`) para `D:\IALD_ARQUIVO\MEMORIA_IALD\snapshots\`. Se D: não estiver
  disponível ou a conferência falhar: **não apaga nada em C:** e registra aviso visível (fail-safe).
- **Custo [DERIVED]:** com o banco em 357 MB (os eventos legados **não encolhem** o banco, ver R1), cada
  instantâneo custa 357 MB; com ≤ ~3 mutações/hora após D3, ≈ 24 instantâneos/dia ≈ 8,6 GB/dia para D:
  (1.954 GB livres ≈ 7 meses). Ver a **opção D1-B** em R1 para reduzir o banco vivo a ~3 MB.

### 3.3 (c) Backup integral antes de migração ou operação não-aditiva
Obrigatório e automatizado em `migrate_v2.py` e em `memoria_admin.py archive-backups` (§6, passo M2).

### 3.4 Os 764 backups existentes — MOVER, nunca apagar
`memoria_admin.py archive-backups --state C:\IALD\MEMORIA_IALD\state --dest D:\IALD_ARQUIVO\MEMORIA_IALD\backups_ate_20261012 --keep 3`:
1. lista `memory.sqlite3.bak_*` ordenados pelo carimbo do nome; exclui os 3 mais recentes **no momento da execução**
   (não os de 19:42: recomputar); nunca toca `memory.sqlite3`, `-journal`, `snapshots\`, `journal\`;
2. para cada um: sha256 da origem → copia (buffer 8 MiB) → fsync → sha256 do destino → iguais? → apaga a origem →
   linha em `MANIFEST.jsonl` `{name, bytes, sha256, src, dst, moved_at}`; diferentes → mantém a origem e aborta com
   erro visível (o que já foi movido fica registrado);
3. ao fim: `MANIFEST.json` consolidado (quantidade, soma de bytes, sha256 do próprio `MANIFEST.jsonl`).
Volume [REAL]: 92,27 GB; tempo estimado 15–40 min [DERIVED, depende do disco]. Backups criados pelo processo
durante a movimentação são mais novos que o corte e não são tocados.

### 3.5 Arquivos e funções (D2)
| arquivo | função | mudança |
|---|---|---|
| `…\lib\iald_memory\journal.py` (novo) | `path_for(root, context_id)`, `append(root, line)`, `tail(root, context_id)`, `verify_chain(root, context_id, db_rows)`, `rebuild(root, out_db)` | diário encadeado |
| `…\lib\iald_memory\snapshots.py` (novo) | `due(policy, now)`, `take(db_path, snap_dir)`, `prune_and_archive(snap_dir, archive_dir, keep=3)`, `archive_legacy_backups(state_dir, dest, keep=3)` | cópia de bytes, manifesto, fail-safe |
| `store.py` `transition`/`ensure_context` | `_journal_append(conn, line)` antes de `commit`; `_snapshot_if_due()` antes da mutação | substitui `_backup` |
| `store.py` `verify` | + `journal_ok` | — |

---

## 4. D3 — HEARTBEAT E PSION [INPUT]

### 4.1 Causa no código (`iald_web_server.py` `7e48e90afcad6b05`; diff em `evidencias\`)
- l.3156–3159 `heartbeat_cycle` → `app_memory.run_autonomous(...)`: 2 eventos por ciclo (`service_cycle`,
  `service_result`) e, em falha, fase `requires_reconciliation` que **bloqueia o ciclo seguinte** (`run_autonomous`
  l.520–524 de `iald_app_memory.py`).
- l.3188–3200: `t0 = perf_counter()` → `req_lib.post(json=_operational_native_payload({...}))` → `elapsed`.
  `_operational_native_payload` (l.5688–5695) chama `app_memory.project_messages` (replay do livro + projeção de
  até 24 KB **inserida no prompt**) e `native_memory.check_text_window` (tokenização) — tudo dentro da janela; e o
  bloco de memória no prompt eleva o pré-processamento (prefill) do llama, que entra em `elapsed` e derruba
  `completion_tokens/elapsed` [DERIVED; o log mostra 88,8 → 14,5 tok/s de mediana].
- l.3205–3206 `app_memory.tool_result("heartbeat_sample", …, {"response": data, …})`: 10 eventos por batida com o
  corpo das respostas (os 734 candidatos de ~1,3 KB).
- l.3201–3202 e l.3211–3212: `raise` em vez de `continue` (regime antigo, backup `43eb1377…`).
- l.3228–3236: a medida degradada entra em `_update_psion_from_heartbeat` (EMA com taxa β = 0,01203…) e
  `_save_psion_state` (`open(..., "w")` direto, l.3093 — sem tempário, sem backup).

### 4.2 Desenho
**(a) Medida só de geração.** `_heartbeat_cycle_with_memory` → `_heartbeat_measure()` (puro):
- payload **idêntico ao regime r60** (`{"model":"qwen3","messages":[sys_msg, prompt],"max_tokens":256,
  "temperature":0.7,"stream":false}`), **sem** `_operational_native_payload`, **sem** `project_messages`, **sem**
  `check_text_window`;
- `t0`/`elapsed` só em volta do `post`; tok/s = `timings.predicted_n / timings.predicted_ms × 1000` quando o
  llama-server devolver `timings` [KNOWN — llama.cpp inclui `timings` na resposta; conferir na primeira batida e
  registrar na telemetria qual fórmula foi usada], senão `completion_tokens / elapsed`;
- HTTP ≠ 200 ou exceção de rede → `continue` (amostra perdida) e classe `falha` se não sobrar amostra; o heartbeat
  é medição local gratuita: a regra "não repetir chamada incerta" é para provedores pagos e não se aplica;
- nenhuma chamada à memória comum dentro de `_heartbeat_measure`.
**(b) Escrita na memória só por mudança de classe ou 1/h.**
- classe: `ok` se `avg ≥ 0,8 × baseline`; `alerta` se abaixo (mesmo critério do alerta atual, l.3134); `falha` se
  `skipped_offline`, `no_results` ou exceção;
- estado em `logs\iald_heartbeat_health.json` `{class, since, last_memory_event_at, last_memory_event_id}`;
- `should_record = class != previous_class or now − last_memory_event_at ≥ 3600`; quando verdadeiro, **uma**
  `transition` via nova função `iald_app_memory.record_measurement(identifier, objective, text, source_ref)`:
  registro `kind='fact', statute='REAL', sources=[{'kind':'measurement','ref':'heartbeat_telemetry:<line_sha256>'}]`,
  ator `{'id':'service.native-heartbeat','kind':'measurement'}`, texto = resumo canônico (`class, avg_tok_s, cv,
  n_prompts, baseline_before/after, regime`) — **sem corpos de resposta**; fluxo `phase='heartbeat_'+class`;
  `event_id` estável = `'hb.' + sha256(telemetry line)`; sem `run_autonomous` (fica para outros serviços);
- telemetria por batida em `C:\IALD\projetos_pyhton\IALD\logs\iald_heartbeat_telemetry.jsonl` (uma linha por
  batida: `at, regime:'generation_only', formula, class, avg_tok_s, cv, samples[], n_prompts, baseline_before,
  baseline_after, memory_event_id|null, line_sha256`), teto `HEARTBEAT_TELEMETRY_MAX_BYTES = 4 MiB`, rotação
  `.1….5` por renomeação encadeada, nunca truncar a linha corrente;
- dimensionamento [DERIVED]: 48 batidas/dia × ~400 B = 20 KB/dia de telemetria; ≤ 24 eventos/dia no banco, ~300 B
  de delta cada.
**(c) Psion.**
- O feed degradado para por (a): com o payload original, a próxima batida mede no regime r60.
- `_save_psion_state` (l.3091–3094): tempário → fsync → `os.replace` (atômico) e **uma cópia diária**
  `iald_psion_state_32B.json.bak_<AAAAMMDD>` (primeira escrita do dia; ~24 KB/dia) — o nome casa com o filtro D4
  (`iald_psion_state*`). Isso cria os pontos de restauração que hoje não existem desde 27/09. [INPUT: a gerência
  decide se quer a cópia diária.]
- **Restauração: NÃO executar agora.** Existe cópia anterior a 10/10 09:20 (`D:\IALD\…\iald_psion_state_32B.json`,
  27/09 04:00:05, sha256 `f9a5ec88…`), mas há dúvida nos dois termos da condição de D3(c): (i) entre 27/09 e
  10/10 09:11 houve ~121 batidas legítimas (log r60) que a cópia não contém — restaurar apaga 13 dias de
  contabilidade sadia (gerações, histórico, total de batidas); (ii) "únicas escritas posteriores forem as do
  heartbeat" não é verificável por mim: `iald_pilot_engine.py` l.105/120 e `iald_pilot_gguf.py` l.60/78 também
  referenciam o arquivo e podem gravá-lo quando rodados à mão. Pela regra "se houver dúvida, NÃO restaurar":
  parar o feed (a) e **relatar ao operador** as opções: (1) restaurar os bytes de 27/09 (perde 13 dias de
  contabilidade, baseline sadio imediato); (2) manter os bytes atuais e deixar a EMA recuperar (meia-vida ≈ 57
  batidas ≈ 28 h de batidas a 2/h [DERIVED de (1−β)^n = ½]); (3) reconstrução derivada invertendo a EMA pelas
  61 batidas do histórico (lê o conteúdo: só o operador). Metadados completos em
  `evidencias\PSION_BACKUPS_METADADOS_12out.json`.

### 4.3 Arquivos e funções (D3)
| arquivo | função | linhas | mudança |
|---|---|---|---|
| `C:\IALD\projetos_pyhton\IALD\iald_web_server.py` | `heartbeat_cycle` | 3156–3159 | orquestra: `_heartbeat_measure` → psion → telemetria → `_heartbeat_record_memory_if_due`; sem `run_autonomous` |
| idem | `_heartbeat_cycle_with_memory` → `_heartbeat_measure` | 3162–3242 | payload r60; `t0/elapsed` só no `post`; `timings` quando houver; `continue` em falha; **remover** l.3191 (`_operational_native_payload`) e l.3205–3206 (`tool_result`) |
| idem | novas: `_heartbeat_class`, `_heartbeat_telemetry_append`, `_heartbeat_record_memory_if_due` | após 3242 | §4.2 |
| idem | constantes | após 3037 | `HEARTBEAT_TELEMETRY_FILE`, `HEARTBEAT_TELEMETRY_MAX_BYTES`, `HEARTBEAT_TELEMETRY_KEEP=5`, `HEARTBEAT_MEMORY_MIN_INTERVAL=3600`, `HEARTBEAT_HEALTH_FILE` |
| idem | `_save_psion_state` | 3091–3094 | tempário + `os.replace`; cópia diária `.bak_<AAAAMMDD>` |
| idem | `_operational_native_payload` | 5688–5695 | **mantida** para as rotas de chat/admin (l.9806, 10753, 10842, 10992); só o heartbeat deixa de usá-la |
| `C:\IALD\projetos_pyhton\IALD\iald_app_memory.py` | nova `record_measurement(identifier, objective, text, source_ref, *, flow=None)` | após 538 | `ensure_context` (idempotente) + 1 `transition` com CAS local (reuso de `_commit` sem spool) |
| idem | `run_autonomous` | 508–538 | inalterada (outros serviços e testes) |

---

## 5. D4 — FILTROS, fail-closed [INPUT]

### 5.1 Módulo único `C:\IALD\MEMORIA_IALD\lib\iald_memory\guard.py` (novo; stdlib)
- `CONFIDENTIAL_BASENAMES`: padrões sobre o basename **normalizado** (NFKC + casefold, remoção repetida de
  sufixo `.bak_*`/`.bak*`/`.tmp_*`): `iald_psion_state*`, `iald_stack_v*`, `.env`, `.env.*`, `*.key`, `*.pem`.
- `ESCRITORIO_PART`: qualquer componente do caminho cujo NFKC+casefold comece por `escritorio` (pega
  `Escritório`, `ESCRITÓRIO`, NFD, `Escritorio Miguel`); e `realpath` sob `C:\Escritorio`.
- `is_confidential_path(path) -> str|None`: (1) `os.path.realpath` (resolve junções e links simbólicos no Windows,
  Python ≥ 3.8); (2) nome do caminho pedido **e** do caminho resolvido; (3) `os.stat` → `st_nlink > 1` → recusa
  (`hardlink`); (4) identidade `(st_dev, st_ino)` comparada ao **registro de identidades confidenciais**
  construído em tempo de chamada por `stat` dos arquivos reais em `C:\IALD\projetos_pyhton\IALD` (+ `files\`),
  `C:\IALD\MEMORIA_IALD`, `C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923` que casem com os
  padrões (meia dúzia de `stat`, sem ler conteúdo); `st_ino == 0` (sistema sem identificador) → recusa fail-closed.
- `scan_text(text) -> list[str]` (nomes de regras, **nunca o trecho casado**): `sk-[A-Za-z0-9_-]{12,}` (cobre
  `sk-proj-`), `AIza[0-9A-Za-z_-]{20,}`, `ghp_[A-Za-z0-9]{20,}`, `xox[bp]-[A-Za-z0-9-]{10,}`,
  `(?i)bearer\s+[A-Za-z0-9._~+/=-]{16,}`, `(?i)[a-z]:[\\/]+escrit[oó]rio` e `\\\\[^\\]+\\escrit[oó]rio` (caminhos,
  não a palavra solta), `(?i)iald_psion_state`, `(?i)iald_stack_v\d`, `(?i)(^|[\\/\s"'])\.env(\.[a-z0-9_-]+)?\b`,
  `(?i)\b[\w-]+\.(key|pem)\b`.
- `assert_clean_text(text, where)` → levanta `ConfidentialContent(rules, where)` (subclasse de `MemoryError`) com
  mensagem só com nomes de regra, `where` e `sha256(text)[:16]`; registra uma linha em
  `state\guard_refusals.jsonl` (mesmos campos; nunca o texto). **Recusa visível, nunca redação silenciosa.**

### 5.2 Pontos de aplicação (todos fail-closed)
| arquivo | função | linhas | aplicação |
|---|---|---|---|
| `C:\IALD\MEMORIA_IALD\session_memory.py` | `FORBIDDEN_NAMES`, `FORBIDDEN_PARTS` | 14–15 | removidos; `read_allowed_file` l.25–33 usa `guard.is_confidential_path` (caminho pedido + resolvido + identidade) |
| idem | `dispatch` `init` | 92–96 | `guard.assert_clean_text(objective, 'init.objective')` antes de `ensure_context` |
| idem | `dispatch` `transition` | 162–175 | `assert_clean_text(json.dumps(changes), 'transition.changes')` |
| idem | `dispatch` `get`/`project` | 155–159 | `assert_clean_text(result text, 'project')` (defesa em profundidade: a projeção vai ao provedor da sessão) |
| `C:\IALD\MEMORIA_IALD\session_hook.py` | `load_context` | 20, 31 | herda por `read_allowed_file` e `dispatch` |
| `C:\IALD\projetos_pyhton\IALD\iald_app_memory.py` | `protected_path` | 541–543 | `return guard.is_confidential_path(path) is not None` |
| idem | `Binding.append` | 75–85 | `assert_clean_text(text, 'app.append:'+label)` antes de `_spool` |
| idem | `Binding.projection` | 133–142 | `assert_clean_text(result['text'], 'app.projection')` — cobre `project_messages` (205–224), `routing_state` (238–244), `project_completion_payload` (546–555) |
| idem | `read_record` | 437–464 | `assert_clean_text` sobre a fatia devolvida ao modelo |
| idem | `dispatch`/`dispatch_admin` | 378–379, 504–505 | `ConfidentialContent` → HTTP 409 com `{'error': 'Conteúdo confidencial recusado pela memória: <regras>'}` |
| `C:\IALD\projetos_pyhton\IALD\iald_web_server.py` | `agi_validate_path` | 2614 | inalterada (delega a `protected_path`) |
| `…\iald_orchestrator\policy.py` | `FORBIDDEN` | 8 | + `escrit[oó]rio` em caminho, `ghp_`, `xox[bp]-`, `bearer`, `.key/.pem`, `sk-proj-`; ou delegar a `guard.scan_text` mantendo a regex como atalho |
| `…\iald_orchestrator\operational_memory.py` | `projection` | 101–103 | `guard.scan_text(value['text'])` → `ValueError('Confidential reference in operational memory; dispatch refused: <regras>')` |
| idem | `attach` | 109–131 | re-conferir `projection['text']` antes de concatenar ao pacote |
| `C:\IALD\projetos_pyhton\IALD\iald_task_sandbox.py` | `_CONFIDENTIAL` | 118 | **recomendado (fora do mínimo):** alinhar ao `guard` |

Cuidado operacional: a auditoria varreu o livro de produção e achou **zero** ocorrências das chaves/nomes
confidenciais e 2 registros com a palavra «Escritório» num contexto de 12/10 [DECLARADO pela auditoria, s21]. A
regra D4 é por **caminho** (`C:\Escritorio…`), não pela palavra solta; se esses 2 registros contiverem o caminho,
a projeção daquele contexto passará a ser recusada (visível) — conferência cabe à gerência (R5).

---

## 6. D5 — BLOCOS DE INSTRUÇÃO [INPUT]

### 6.1 Texto novo (proposta; a gerência fixa o texto final e o hash é lido na instalação)
```
<!-- IALD_SHARED_MEMORY_SESSION_BRIDGE_20261012 -->
**Memória comum da IALD — ao abrir a sessão e após compactação/retomada:** leia `C:\IALD\MEMORIA_IALD\README.md` e rode `C:\Python314\python.exe -X utf8 C:\IALD\MEMORIA_IALD\session_memory.py` com JSON em stdin: `{"operation":"project","reference":"CAMINHO_EXATO_DO_RECIBO"}` (só leitura; custo pequeno — o banco grava por delta e cada transição custa uma linha no diário, não uma cópia do banco). Sem referência própria, inscreva a fonte original autorizada por `init`; nunca adote a tarefa de outra sessão. `transition` só ao concluir etapa material: q com fonte/estatuto, p com fase/próxima ação, revisão esperada e evento estável. O original não muda; correções ao lado; modelos só geram candidatos DECLARADO. Confirme o recibo ou declare a falha. Não autoriza ações, não move gate, não mistura a casa Escritório.
<!-- bloco anterior (620 B, sha16 3106d7234c7a3b71) substituído em 12/10/2026 por ordem do operador («resolva a questão da memória», sha16 78ef70e6f9868281) -->
<!-- END_IALD_SHARED_MEMORY_SESSION_BRIDGE_20261012 -->
```
(no CLAUDE.md da IALD Nativa a linha de registro cita `624 B, sha16 2ca1cb060ecd2119` e o bloco é gravado em
CRLF, como o arquivo.) O mesmo texto substitui `C:\IALD\MEMORIA_IALD\SESSION_BRIDGE.md` (backup de bytes).

### 6.2 Script `replace_blocks.py` (na pasta de implementação, não aqui) — por arquivo
1. lê os bytes; **CAS**: `sha256(bytes[:620])[:16] == '3106d7234c7a3b71'` (Nativa: `[:624] == '2ca1cb060ecd2119'`)
   senão aborta esse arquivo com erro visível (outra sessão mexeu — MEMORY.md mudou às 19:31 enquanto eu media);
2. backup de bytes `<arquivo>.bak_20261012_<HHMMSS>_<us>` + conferência;
3. `novo = BLOCO_NOVO (LF ou CRLF conforme o arquivo) + bytes[620:]` (Nativa: `[624:]`); tempário → verificação
   → `os.replace`; pós-conferência: `novo[len(BLOCO_NOVO):] == bytes[620:]` byte a byte — **nada mais do arquivo
   muda** (os 3.274/3.294 B acrescidos no fim de CLAUDE.md/AGENTS.md/Nativa ficam);
4. recibo `BLOCOS_RECIBO.json` com `old_sha256`, `new_sha256`, `block_old_sha16`, `block_new_sha16`, `backup`.
**MEMORY.md da Central** (`C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md`): backup
de bytes; localizar a única linha que começa com `- Memória ACOM:` (hoje a 14) e substituí-la por
`- Memória ACOM: `C:\IALD\MEMORIA_IALD\README.md` + `SESSION_BRIDGE.md` (12/10: delta + diário + instantâneos; `project` ao abrir e após compactação; `transition` só em etapa material). Diário: MEMORY_2.md.`;
pós-condição: ≤ 200 linhas e ≤ 24.000 B (hoje 166 linhas, 18.419 B) — senão aborta e restaura do backup.

---

## 7. D6 — PARTIÇÃO [INPUT]
- `store.py` `_scope` (l.114–121): `house`/`principal` cujo NFKC+casefold contenha `escritorio` → `ScopeViolation`
  (`'Escritório house never enters the IALD common memory'`); idem em `session_memory.py` `reference_for`/`init`
  (l.65–82, 97) antes de qualquer escrita. `iald_app_memory.begin` mantém `house='IALD_APP'` fixo; a fila mantém
  `SCOPE` fixo (`operational_memory.py` l.16). Autenticação segue no chamador (sem mudança).

---

## 8. TESTES

### 7.1 Existentes que têm de continuar passando (123) — e as duas reescritas obrigatórias
| suíte | casos | mudança necessária |
|---|---|---|
| CORE `core\tests\test_store.py` | 20 | **1 reescrita:** `test_state_and_flow_commit_together_and_survive_restart` (l.95–106) afirma `len(backups) == 2` e abre o `.bak_` — passa a afirmar: diário com 2 linhas (`anchor`, `event`) com cadeia válida, `context_state.revision == 1`, e nenhum `memory.sqlite3.bak_*`. Os outros 19 passam sem mudança: os gatilhos de `events`/`contexts`/`metadata` continuam; `_read` continua sendo chamado 2× por `transition` (l.290–320); CAS/replay/escopo/projeção não mudam |
| SESSOES `sessions\test_sessions.py` + `test_hooks.py` | 12 + 5 | nenhuma (`test_scope_override_fails` l.120 passa a falhar por `ScopeViolation` explícita, continua `ok=False`) |
| APP `app\test_app_memory.py` | 31 | **1 reescrita:** `test_actual_heartbeat_transport_and_uncertain_block` (l.270–284) afirma `'operational memory' in sent[0]['messages'][0]['content']`, candidato `synthetic-heartbeat` no banco e bloqueio por `RuntimeError` no ciclo seguinte — tudo o que D3 muda. Substituída pelos testes de 7.2 (APP). Os 30 restantes passam (`run_autonomous` fica; `protected_path` continua a função chamada) |
| FILA (29 arquivos em `queue\`) | 55 | nenhuma; mantém a dependência de ambiente da memória canônica (`state\canonical_memory`, 140 MB) documentada pela auditoria |

### 7.2 Novos (nome → o que prova)
**CORE — `core\tests\test_store_v2.py`**
- `test_growth_n300_bytes_db_journal_snapshots`: contexto com 300 candidatos de ~1.313 B (mesmo gerador da auditoria); mede bytes do banco, do diário e dos instantâneos em N=100/200/300; afirma incremento de banco ≈ linear (`(b300−b200)/(b200−b100)` em [0,7; 1,5]), banco < 6 MB em N=300 (v1 extrapolado ≈ 56 MB [DERIVED da auditoria: 15,0 MB em N=150, expoente 1,87]), diário ≈ N × (|changes|+600 B) ± 20 %, instantâneos = ⌊300/50⌋ = 6 com só 3 em "C:" (pasta temporária) e 3 no "D:" (pasta temporária) com sha256 conferido; grava `evidencias\crescimento_n300.json`.
- `test_transition_time_bounded_n300`: mediana de `transition` < 50 ms e `get` < 50 ms em N=300 (v1: 0,41 s em N=150).
- `test_public_contract_fields_unchanged`: chaves de snapshot, recibo, projeção e `verify` iguais às de `CORE.md` (lista literal).
- `test_legacy_v1_db_refused_without_migration`: banco criado pela cópia congelada `tests\store_v1_frozen.py` (sha256 pinado = `2d4f6214…`) → `MemoryStore` v2 levanta `SchemaMigrationRequired`.
- `test_migration_preserves_head_state_sha_and_chain`: v1 com 3 contextos (um com 200 eventos) → `migrate_v2` → `verify(deep=True)` ok; `state_sha256` de cabeça igual antes/depois; `snapshots` com `reason='migration_v2'` em cada contexto; `schema_version='2'`; linha `schema_upgrade_2_at`; eventos legados byte-iguais.
- `test_mixed_legacy_delta_replay`: após migrar, 50 transições novas; `get`/`project`/`verify` ok; `state_json==''` só nos novos.
- `test_v1_code_refuses_v2_schema`: `store_v1_frozen.MemoryStore` sobre o banco migrado → `IntegrityError('Unsupported or missing memory schema')`.
- `test_materialized_row_tamper_fails_closed`, `test_snapshot_row_tamper_fails_closed`, `test_delta_event_tamper_fails_closed`, `test_context_state_revision_lag_fails_closed` (gatilhos derrubados e restaurados, como os testes atuais).
- `test_journal_written_before_commit_and_orphan_voided`: `patch` que falha após o append e antes do commit → banco em `revision` anterior, diário com linha órfã; próxima transição acrescenta `void` e segue; `verify()['journal_ok']` é `True`.
- `test_journal_chain_and_rebuild_equals_db`: `journal.rebuild` → banco novo com os mesmos `state_sha256`/`event_hash` por contexto.
- `test_snapshot_policy_50_mutations` e `test_snapshot_policy_60_minutes` (relógio injetado) e `test_snapshot_keep3_and_archive_move_verified` e `test_archive_unavailable_keeps_local_copies`.
- `test_archive_legacy_backups_mover_manifest_and_sha`: 12 `.bak_` sintéticos, `--keep 3` → 9 movidos, manifesto, sha256 conferidos, origem apagada só após conferência; um destino corrompido de propósito → aborta sem apagar.
- `test_escritorio_scope_refused` (D6): `house='Escritório'`, `'ESCRITORIO'`, NFD, `principal='escritorio-x'` → `ScopeViolation` em `ensure_context/get/transition`.

**SESSÕES — `sessions\test_filters.py`** (processo novo por operação, como `test_sessions.py`)
- `test_confidential_name_variants_refused`: tabela `iald_psion_state_32B.json`, `IALD_PSION_STATE.JSON`, `iald_psion_state.json.bak_20261010_092013`, `iald_stack_v7.py`, `iald_stack_v8.py`, `.env`, `.env.local`, `.ENV.production`, `chave.key`, `cert.pem`, `cert.pem.bak_1`, caminho com `Escritório` NFD, `Escritorio Miguel\x.txt` → todos `source_path_not_allowed`; nomes inocentes aceitos.
- `test_hardlink_identity_refused`: `os.link(confidencial_sintético, nome_inocente)` → recusado (`st_nlink>1` e identidade); `test_junction_refused`: junção (`mklink /J`, via `_winapi.CreateJunction`) para pasta com confidencial sintético → recusado pelo `realpath`.
- `test_content_keys_refused_at_init_and_transition`: objetivo e `changes` com `sk-…`, `sk-proj-…`, `AIza…`, `ghp_…`, `xoxb-…`, `Bearer …`, `C:\Escritorio\x`, `c:/escritorio/x`, `iald_psion_state_32B.json` → `ConfidentialContent`, código 2, mensagem **sem** o trecho (afirmado por `assertNotIn`).
- `test_projection_refuses_confidential_content_without_echo`: banco com registro injetado por v1 congelado contendo chave sintética → `project` recusa; `get` recusa; nada no stdout contém a chave.

**APP — `app\test_app_memory_v2.py`** (mesmo `load_handlers` por AST de `test_app_memory.py`)
- `test_heartbeat_measures_generation_only`: `post` falso com latência 0,2 s e `project_messages` monkeypatched com `sleep(1.0)` e contador; afirma: contador = 0 durante `_heartbeat_measure`, payload enviado == payload r60 (sem bloco de memória, mensagens exatamente `[sys_msg, prompt]`), `elapsed` em [0,2; 0,25] s, e tok/s calculado de `timings` quando presente (`test_heartbeat_tok_s_prefers_server_timings`).
- `test_heartbeat_memory_event_only_on_class_change_or_hourly`: 3 batidas `ok` → 0 eventos; 1 `alerta` → 1 evento; relógio +61 min → 1 evento; eventos com `kind='fact'`, `statute='REAL'`, `sources[0].kind='measurement'`, texto sem `response`.
- `test_heartbeat_telemetry_rotation`: teto de 4 KiB no teste → 5 rotações, linha corrente íntegra.
- `test_heartbeat_failure_does_not_block_next_cycle`: HTTP 500 → `continue`; `no_results` → classe `falha`, 1 evento; o ciclo seguinte roda.
- `test_psion_save_atomic_and_daily_bak`: arquivo sintético; `_save_psion_state` grava por `os.replace`; 2 gravações no mesmo dia → 1 `.bak_<dia>`.
- `test_protected_path_variants` (mesma tabela da sessão) e `test_append_and_projection_refuse_confidential_content` e `test_read_record_refuses_confidential_slice` e `test_dispatch_returns_409_on_confidential`.

**FILA — `queue\test_filters_queue.py`**: `test_forbidden_escritorio_and_tokens` (policy), `test_projection_refused_before_dispatch` (`operational_memory.projection`), `test_attach_rechecks_projection`.

**BLOCOS — `work\memoria_acom_fix_12out\tests\test_blocks.py`**: `test_replace_block_exact_bytes_lf_and_crlf` (cópias dos 5 arquivos: resultado == bloco novo + `old[620:]`/`old[624:]`), `test_cas_abort_on_unexpected_head`, `test_memory_md_single_line_and_limits`.

**Guarda de execução:** todos os novos testes rodam sob a mesma guarda `sitecustomize.py` da auditoria (sem rede,
sem escrita fora da pasta, sem sqlite gravável fora da pasta, sem abrir confidenciais), em cópias.

---

## 9. MIGRAÇÃO DO BANCO DE PRODUÇÃO (passo a passo)

Pré-condições: janela quieta anunciada pela gerência (hoje há sessões gravando: contextos criados às 19:13 e
19:38); heartbeat em STANDBY (está) — se estiver armado, parar o filho web antes (M7 reinicia).

| passo | ação | artefato / conferência |
|---|---|---|
| M1 | Medir antes: inventário + `state_sha256` de cabeça por contexto (replay só-leitura v1) + sha256 do banco | `MIGRACAO_ANTES.json` |
| M2 | **Backup integral (D2c):** cópia de bytes de `memory.sqlite3` → `state\memory.sqlite3.pre_v2_20261012_<HHMMSS>` + `.sha256`; segunda cópia em `D:\IALD_ARQUIVO\MEMORIA_IALD\pre_v2\` (criar a pasta) conferida | sha256 iguais nas duas |
| M3 | Instalar código com backup de bytes por arquivo (`.bak_20261012_<stamp>`): `lib\iald_memory\{store.py, __init__.py, guard.py, journal.py, snapshots.py, migrate_v2.py}`, `memoria_admin.py`, `session_memory.py`, `iald_app_memory.py`, `iald_web_server.py` (só o trecho do heartbeat + `_save_psion_state`), `iald_orchestrator\{policy.py, operational_memory.py}`, `SESSION_BRIDGE.md`, `CORE.md` (correção ao lado) | `INSTALACAO_12out.json` com sha256 antes/depois |
| M4 | `migrate_v2.py --store C:\IALD\MEMORIA_IALD\state --dry-run` → relatório; depois `--apply`: `BEGIN IMMEDIATE`; replay **deep** v1 de todos os contextos (confere cada `state_json` legado); cria tabelas/gatilhos/índice; `snapshots` (`reason='migration_v2'`) na revisão de cabeça de cada contexto; `context_state`; bootstrap dos diários (`legacy:true`); `DROP TRIGGER metadata_no_update` → `UPDATE metadata SET value='2' WHERE key='schema_version'` → recria o gatilho; `INSERT metadata('schema_upgrade_2_at', iso)`; `commit`; pós-verificação `verify(deep=True)` em todos os contextos e comparação com M1 | `MIGRACAO_RECIBO.json` (contagens, hashes de cabeça antes/depois, bytes, tempo) |
| M5 | `memoria_admin.py archive-backups --keep 3 --dest D:\IALD_ARQUIVO\MEMORIA_IALD\backups_ate_20261012` (§3.4; pode rodar antes ou depois de M4; 15–40 min) | `MANIFEST.jsonl` + `MANIFEST.json` |
| M6 | Suítes inteiras em cópias (CORE 20 + SESSOES 17 + APP 31 + FILA 55, com as 2 reescritas) + novos (§7.2) | `TESTES_12out.json` |
| M7 | Reiniciar só o filho web (cópia de `restart_web.ps1` apontando a um recibo novo; o original aborta se já existe `APP_RESTART.json`) → `/login` 200 → log mostra `[Heartbeat] Iniciado` e a 1ª batida com `regime=generation_only`; **aceite de D3(a): tok/s da 1ª batida dentro da banda r60 (66,8–138,9)** | `APP_RESTART_12out.json`, linha de telemetria |
| M8 | D5: `replace_blocks.py` (CAS + backups) nos 5 arquivos + MEMORY.md | `BLOCOS_RECIBO.json` |
| M9 | Vigilância 24 h: Δ bytes do banco < 2 MB; diário; ≤ 24 instantâneos (3 em C:); 0 `memory.sqlite3.bak_*` novos; eventos do heartbeat ≤ 24; baseline do psion pela telemetria (não pelo arquivo) | `VIGILANCIA_24H.json` |

**Reversão:** (R-code) restaurar cada `.bak_20261012_*`; (R-db) restaurar `memory.sqlite3.pre_v2_*` por cópia de
bytes conferida por sha256 — os eventos gravados entre a migração e a reversão ficam preservados nos diários
(não reimportáveis na v1; permanecem como evidência); (R-web) reiniciar o filho web; (R-blocos) restaurar os
`.bak_20261012_*` dos 5 arquivos e do MEMORY.md. Ordem: parar escritores → R-code → R-db → R-web → R-blocos.

---

## 10. PLANO DE IMPLANTAÇÃO (ordem, backups, reversão) — resumo
1. Implementar e testar **em cópia** (`work\memoria_acom_fix_12out\1_IMPLEMENTACAO\`): lib v2, guard, journal,
   snapshots, migrate, admin, adaptadores; rodar 123 + novos.
2. Revisão independente do código (quem constrói não aprova) → hash dos artefatos revisados.
3. Janela quieta → M1 → M2 → M3 → M4 → M6 (rápido, em cópia do banco migrado) → M7 → M8; M5 em paralelo ou depois.
4. Recibos em `work\memoria_acom_fix_12out\2_IMPLANTACAO\`; rotas no mapa (`rotas.py registrar`); correção AO LADO
   em `CORE.md`, `SESSION_MEMORY.md`, `README.md` da memória; registro no quadro (ato da gerência).
5. Nada toca `um.py`, kernel, selo, gate ou originais científicos; o nome «ACOM» não entra no `um.py` (homônimo da
   patente — erro nº 2 da casa).

---

## 11. RISCOS
- **R1 — O banco não encolhe com D1 como decidida.** Os 354,7 MB de `state_json` legado ficam (eventos imutáveis);
  cada instantâneo (D2b) custa 357 MB → ≈ 8,6 GB/dia para D: [DERIVED]. **Opção D1-B [INPUT]:** preservar o banco
  v1 inteiro, byte a byte, como `memory_v1_legacy_20261012.sqlite3` (imutável, sha256 no manifesto) e reconstruir o
  banco vivo com os mesmos eventos **menos** o `state_json` dos legados (`''`; `state_sha256` mantido e conferível
  contra o arquivo) → banco vivo ≈ 3 MB, instantâneos triviais. Viola «ficam como estão» só no banco vivo, não no
  acervo. Decisão da gerência; o operador pode vetar.
- **R2 — Processos com a v1 carregada.** O filho web (PID 64412) importou `iald_memory` v1; após M4 ele falha
  fechado (`Unsupported or missing memory schema`) em qualquer uso da memória até M7 (visível: 409/`[Heartbeat] Erro`).
  Os 7 `mcp_server.py` da fila só importam `iald_memory` dentro de `core()` (preguiçoso); `memory_outbox` tem 0
  linhas [DECLARADO pela auditoria], logo provavelmente nunca importaram — mas não é verificável de fora; se já
  importaram, falham fechado até reinício (decisão da gerência/operador; os MCPs científicos seguem sem reinício).
- **R3 — Escritores concorrentes na migração.** `BEGIN IMMEDIATE` serializa; um CLI que colida espera 30 s e falha
  visivelmente (`busy_timeout`); repetição local idempotente é permitida. Anunciar a janela.
- **R4 — Detecção de hardlink/junção no Windows.** `os.stat().st_nlink/st_ino/st_dev` são preenchidos no Windows
  via `GetFileInformationByHandle`; `realpath` resolve junções (Python ≥ 3.8). Em volumes sem identificador
  (`st_ino == 0`) o guarda recusa (fail-closed) — pode recusar demais em exFAT/USB; aceitável (a memória vive em NTFS).
- **R5 — Falsos positivos do filtro de conteúdo.** `Bearer …`, `sk-…` em texto legítimo → recusa visível (a sessão
  reescreve). Registros existentes com caminho `C:\Escritorio` tornam a projeção daquele contexto irrecuperável
  para provedor (não há apagamento); conferir os 2 registros apontados pela auditoria antes de M3.
- **R6 — Concorrência nas superfícies de instrução.** MEMORY.md mudou às 19:31 durante este diagnóstico; o
  `replace_blocks.py` faz CAS pelos bytes do bloco e aborta por arquivo se o topo não for o esperado.
- **R7 — Psion sem ponto de restauração fiel.** A cópia mais recente anterior a 10/10 é de 27/09 (13 dias de
  batidas legítimas depois dela). Não restaurar sem o operador (§4.2c). A cópia diária proposta evita repetir isso.
- **R8 — «60 minutos» sem daemon.** O instantâneo por idade só acontece na primeira mutação após 60 min; sem
  mutação, não há cópia nova (nem necessidade). Se a gerência quiser cadência de relógio, é um agendamento do LAR
  (fora desta especificação).
- **R9 — `app_outbox` cresce 2 arquivos por evento do app** (1.468 hoje). Fora de D1–D6; propor arquivamento
  dos pares `.json/.committed` com mais de 7 dias para D: [INPUT].
- **R10 — Caminhos longos** (`LongPathsEnabled=0`): nomes de instantâneo/arquivo ≤ ~120 caracteres; pastas de
  arquivo em D: curtas (`D:\IALD_ARQUIVO\MEMORIA_IALD\…`).
- **R11 — Dependência de ambiente da FILA55** (memória canônica de 140 MB) permanece; os novos testes não a usam.
- **R12 — `timings` do llama-server** [KNOWN, não conferido aqui]: se ausente na resposta, a fórmula cai para
  `completion_tokens/elapsed` e a telemetria registra `formula`; a comparação com r60 (que usava essa fórmula)
  continua válida.
- **R13 — Reversão parcial.** Após M4, eventos v2 não entram no banco v1 restaurado; ficam nos diários. Reverter
  só com a gerência ciente dessa perda no banco (não no acervo).

---

## 12. O que esta especificação NÃO faz
Não implementa, não migra, não move backups, não reinicia processos, não toca os cinco arquivos nem o psion.
Não leu conteúdo de confidenciais (só nome/bytes/mtime/sha256 por script) nem o acervo do Escritório. Não rodou
`um.py`, selos, atlas ou mapa. Nenhuma chamada a provedor. Conteúdo do banco: só contagens e metadados.

Arquivos desta pasta: `ESPECIFICACAO.md` (este), `ESPECIFICACAO.json`, `evidencias\INVENTARIO_MEMORIA_12out.json`,
`evidencias\PSION_BACKUPS_METADADOS_12out.json`, `evidencias\diff_iald_web_server_bak20261010_vs_instalado.txt`.
