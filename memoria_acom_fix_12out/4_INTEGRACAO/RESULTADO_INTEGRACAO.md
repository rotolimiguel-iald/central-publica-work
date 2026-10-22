INTEGRAÇÃO — conserto ACOM 12/10

Integrador do conserto da memória ACOM, subagente da gerência c1. Escrevi só em
`C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\4_INTEGRACAO\`. Nada em produção foi tocado (medido ao fim por
`conferir_producao_intocada.py` → `evidencias\PRODUCAO_INTOCADA.json`, `producao_intocada: true` [REAL]). Nenhum provedor, nenhuma
rede, nenhum script de selo, nenhum `um.py`; confidenciais nunca abertos (só nomes nas fixtures sintéticas). Estatutos: [REAL] medido
aqui · [DERIVED] · [DECLARADO] · [INPUT] decisão da gerência · [OPEN].

Ordem do operador [REAL, hash lido do arquivo]: `work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt`,
1.342 B, sha16 `78ef70e6f9868281` — «resolva a questão da memória». Decisões D1–D6 [INPUT].

## 0. Resumo em números

| o quê | número [REAL] |
|---|---|
| candidato único | **15 arquivos** (9 modificados, 6 novos) em árvore espelho `candidato\C\...`; 13 das 3 frentes com sha256 conferido contra os manifestos delas; **2 merges a três vias** (`__init__.py`: 1 conflito no `__all__`, resolvido pela união; `iald_app_memory.py`: automático, 0 conflitos, CRLF puro 555→651 CRLF, 0 LF solto) + **1 acréscimo do integrador** (4 linhas: o guard D4 escaneia a medida do heartbeat D3b antes do `ensure_context`) |
| suítes contra o candidato | **11 suítes, 220 testes, 220 PASSA, 0 FALHA** — CORE 20 · SESSOES 17 · APP 31 · FILA 55 (as 123 da origem, com as 2 reescritas obrigatórias) + NUCLEO 34 + SESSOES/FILTROS 24 + APP/FILTROS 9 + HEARTBEAT 15 + FILA/FILTROS 5 + BLOCOS 5 + INTEGRACAO 5 |
| ponta a ponta N=300 | init (CLI) → 300 transitions (295 lib + 5 CLI) → project (CLI) → verify (CLI + deep): banco **3.231.744 B**, diário **629.755 B** (1 arquivo, 301 linhas), instantâneos 3 locais **7.537.018 B** + 3 em «D:» **2.947.146 B**; transição mediana **17,5 ms** (10,0 / 17,3 / 29,9 ms por centena), p90 32,3 ms, máx. 88,7 ms (mutação com instantâneo); `get`+project 23.610 caracteres; verify deep 0,34 s; **0 eventos com estado inteiro, 0 `memory.sqlite3.bak_*`** |
| ensaio de migração (3 contextos, 150/25/0 eventos, código v1 congelado = `store.py` instalado `2d4f6214fa433534`) | dry-run sem mudar bytes; `--apply` 0,51 s; cabeças (revisão, state_sha256, event_hash) iguais à v1; linhas de `events` byte-iguais; verify deep ok nos 3; idempotente; backup pre_v2 + 2ª cópia com sha256 iguais ao banco original; 178 backups legados → 175 movidos (1.159.172.096 B), 3 mantidos, manifesto |
| ensaio de implantação + reversão (cópia completa da instalação, banco sintético v1 com 3 contextos e 83 backups por mutação) | `implantar.py --dry-run` → `DRY_RUN_OK`, **nada mudou**; `implantar.py` → `CONCLUIDA` (9 passos OK, 3,1 s); conferência independente: 15 alvos == candidato, schema 2, 3 `.bak_` em C:, 80 em «D:», 5 blocos + MEMORY.md aplicados, CLI instalado faz get/transition/verify em processo novo; `reverter.py` → `REVERTIDA` (6 passos OK, 0,45 s): **todo arquivo original byte-igual ao antes**, banco com o mesmo sha256; variante B com `--mover-backups-de-volta`: **identidade total** (80 backups devolvidos) |
| produção | intocada: 9 alvos byte-iguais aos originais congelados, 6 novos ausentes, 5 superfícies com o bloco antigo no topo, `state` sem `journal\`/`snapshots\`/`pre_v2`, `D:\IALD_ARQUIVO` ausente. Hoje 13/10 01:5x: banco **357.388.288 B**, **772 backups = 95.123.988.480 B** (o heartbeat segue gravando; +1 backup desde 00:55) |

## 1. O candidato (`candidato\C\...`, `CANDIDATO_MANIFESTO.json`)

Os originais das três frentes são byte-iguais à produção e entre si (`originais_das_frentes_iguais_a_producao: true`) [REAL]. Todo arquivo
tomado de uma frente foi conferido contra o sha256 declarado no manifesto/resumo da própria frente (coluna «declarado»).

| alvo (produção) | origem | B | sha16 | declarado pela frente |
|---|---|---|---|---|
| `MEMORIA_IALD\lib\iald_memory\store.py` | 1_NUCLEO | 49.064 | `b213498dabb3f7e6` | igual |
| `MEMORIA_IALD\lib\iald_memory\journal.py` (novo) | 1_NUCLEO | 11.763 | `64454375b5f7eb9f` | igual |
| `MEMORIA_IALD\lib\iald_memory\snapshots.py` (novo) | 1_NUCLEO | 13.171 | `3562fe7e769cc9dd` | igual |
| `MEMORIA_IALD\lib\iald_memory\migrate.py` (novo) | 1_NUCLEO | 23.221 | `cd8bd05498a2e32c` | igual |
| `MEMORIA_IALD\migrar_para_delta.py` (novo) | 1_NUCLEO | 3.619 | `bf08f0e7231c0377` | igual |
| `MEMORIA_IALD\mover_backups_antigos.py` (novo) | 1_NUCLEO | 2.147 | `b3b8d49efb2868e7` | igual |
| `MEMORIA_IALD\CORE.md` (correção AO LADO, +14 linhas) | 1_NUCLEO | 18.242 | `a572ab36f4566629` | igual |
| `projetos_pyhton\IALD\iald_web_server.py` (só o trecho do heartbeat + `_save_psion_state`) | 2_HEARTBEAT | 749.203 | `f687697a93eac214` | igual |
| `MEMORIA_IALD\session_memory.py` | 3_FILTROS | 11.950 | `9cfc53af2005d29c` | igual |
| `MEMORIA_IALD\SESSION_BRIDGE.md` (bloco novo + linha de substituição) | 3_FILTROS | 1.247 | `70c67257c04703a1` | igual |
| `MEMORIA_IALD\lib\iald_memory\guard.py` (novo) | 3_FILTROS | 9.796 | `5ef08688963e4207` | igual |
| `...\iald_orchestrator\policy.py` | 3_FILTROS | 4.845 | `7df276df8518ee66` | igual |
| `...\iald_orchestrator\operational_memory.py` | 3_FILTROS | 9.417 | `ef6ea57468860e4d` | igual |
| `MEMORIA_IALD\lib\iald_memory\__init__.py` | **merge** 1_NUCLEO × 3_FILTROS | 1.204 | `6eebca8cb2ef3c96` | — |
| `projetos_pyhton\IALD\iald_app_memory.py` | **merge** 2_HEARTBEAT × 3_FILTROS + integrador | 38.079 | `33060408cc005c39` | — |

**Conflitos entre frentes e como foram resolvidos (`merge\`, `git merge-file` a três vias, base = original instalado):**

1. `__init__.py` — NUCLEO acrescenta `SchemaMigrationRequired` (import + `__all__`); FILTROS acrescenta `from . import guard`,
   `ConfidentialContent` (import + `__all__`). O `git merge-file` reportou **1 conflito** (as duas frentes editaram a última linha do
   `__all__`; `merge\__init__.merged.py` guarda os marcadores). Resolução registrada: **união** dos dois acréscimos, docstring da NUCLEO
   (`merge\__init__.resolvido.py`, sha16 `6eebca8cb2ef3c96`). Teste: `test_merged_init_exports_union_of_both_fronts` prova que
   `__all__` ⊇ exportações v1 ∪ {`SchemaMigrationRequired`, `ConfidentialContent`, `guard`} e que cada nome existe.
2. `iald_app_memory.py` — HEARTBEAT insere `record_measurement` (+43 linhas, D3b); FILTROS troca `protected_path` pelo guard e escaneia
   append/projection/begin/tool_result/observe_stream/read_record/dispatch (+63/−14, D4). Hunks disjuntos: merge **automático, 0 conflitos**
   (`merge\iald_app_memory.merged.py`, `f2133ed6a34cd536`). O arquivo é CRLF puro antes e depois (555 → 651 CRLF, 0 LF solto) [REAL].
3. **Acréscimo do integrador** (D4 ∩ D3b, 4 linhas, sha256 do trecho `0411332ec85a4412…`): `record_measurement` chama
   `guard.assert_clean_text(canonical({objective, text, source_ref, flow}), 'app.record_measurement:<id>', log_path=_guard_log())`
   **antes** de `ensure_context` — a medida do heartbeat passa pelo mesmo filtro de conteúdo que todo texto que entra no banco; recusa
   visível (`ConfidentialContent`), nada gravado (nem contexto), log `guard_refusals.jsonl` com regras e sha16, nunca o trecho. Sem isto, o
   D3b teria sido o único caminho de escrita no banco comum fora do D4. Teste: `test_record_measurement_passes_through_guard_before_any_write`
   (chave `sk-…` e caminho `C:\Escritorio\…` recusados; texto limpo entra como `fact/REAL`; o contexto legado de 10/10 não é criado).

Sem conflito (um só dono): `store.py`, `journal.py`, `snapshots.py`, `migrate.py`, scripts e `CORE.md` (NUCLEO); `iald_web_server.py`
(HEARTBEAT); `session_memory.py`, `SESSION_BRIDGE.md`, `guard.py`, `policy.py`, `operational_memory.py` (FILTROS). Conferido por diff:
`DIFF.patch` (originais → candidato, bytes, terminadores preservados; `DIFF_APPLY_CHECK.json` prova que `git apply` sobre cópia dos
originais reproduz o candidato byte a byte). **Instalação = cópia de bytes com backup (implantar.py), nunca `git apply`.**

## 2. As suítes contra o candidato (`testes\TESTES.md`, `testes\RESULTADOS_TESTES.json`) [REAL]

Harness montado por `testes\montar_suite.py` a partir do candidato (28 cópias conferidas por sha256 contra `CANDIDATO_MANIFESTO.json`),
das suítes da origem (`iald_memoria_acom_20261010`) e dos testes novos das três frentes; rodado por `testes\rodar.py` sob a guarda
`sitecustomize.py` da auditoria (cópia byte a byte, sha16 `08f378651f8c0f74`; `ACOM_AUDIT_ROOT=4_INTEGRACAO`: sem rede, sem escrita nem
sqlite gravável fora da pasta, sem abrir confidenciais, só subprocessos Python; TEMP dentro da pasta; o «D:» dos testes é `tmp\arquivo_D`).

| suíte | módulos | rodados | PASSA | FALHA | s |
|---|---|---|---|---|---|
| CORE 20 (origem, 1 reescrita D1/D2) | test_store | 20 | 20 | 0 | 1,2 |
| NUCLEO novos 34 (frente 1) | test_store_v2 | 34 | 34 | 0 | 97,9 |
| SESSOES 17 (origem) | test_sessions, test_hooks | 17 | 17 | 0 | 9,1 |
| SESSOES novos 24 (frente 3) | test_filters, test_guard | 24 | 24 | 0 | 10,0 |
| APP 31 (origem, 1 reescrita D3) | test_app_memory | 31 | 31 | 0 | 19,9 |
| APP novos 9 (frente 3) | test_app_filters | 9 | 9 | 0 | 0,8 |
| HEARTBEAT novos 15 (frente 2) | test_heartbeat_v2, test_heartbeat_stub_server | 15 | 15 | 0 | 26,8 |
| FILA 55 (origem) | os 7 módulos da validação de 10/10 | 55 | 55 | 0 | 25,8 |
| FILA novos 5 (frente 3) | test_filters_queue | 5 | 5 | 0 | 0,3 |
| BLOCOS 5 (frente 3) | test_blocks | 5 | 5 | 0 | 0,4 |
| INTEGRACAO novos 5 (esta frente) | test_integracao | 5 | 5 | 0 | 43,9 |
| **total** | | **220** | **220** | **0** | |

Diferenças importantes em relação às rodadas das frentes: (a) a lib sob teste é a **v2 do candidato** em TODAS as suítes (as frentes 2 e 3
tinham rodado APP/SESSOES/FILA com a v1 congelada) — os adaptadores `session_memory.py`, `iald_app_memory.py` e a fila passam contra a v2
(era o passo M6 da especificação, até aqui [OPEN]); (b) a FILA 55 roda com **injeção de configuração**, como a auditoria de 12/10: 11 casos
de `test_coordination`/`test_transport` resolvem a memória canônica ativa da fila por caminho absoluto (`snapshot_root` fixado no
manifesto; cópia não resolve), e `testes\suite\queue\rodar_fila55.py` aponta `canonical_memory.ACTIVE/RELEASES` para o estado instalado,
que o próprio código abre só em `mode=ro` (a guarda registrou 67 `SQLITE_RO_OUTSIDE`, 0 bloqueios) — dependência de ambiente R11,
documentada; (c) o `__init__.py` e o `iald_app_memory.py` testados são os **merges**, não os arquivos de nenhuma frente.

Guarda (rodada final, 13/10 01:37–01:42): 138 processos; bloqueios **2**, ambos `BLOCK_NETWORK socket.bind ('::1', 0)` = o teste de IPv6 que o urllib3 faz no `import requests`
(mesmo bloqueio registrado pela auditoria e pelas frentes 2 e 3); 0 `BLOCK_WRITE_OUTSIDE`, 0 `BLOCK_MUTATION_OUTSIDE`, 0 `BLOCK_CONFIDENTIAL_*`.

Iteração registrada (honestidade): a primeira rodada completa teve **30 falhas, nenhuma do candidato**: 3 artefatos do meu harness (TEMP com
prefixo `\\?\` quebra o `sqlite3.connect('file:…?mode=ro', uri=True)` do teste `test_snapshot_policy_50_mutations` da frente 1 → TEMP simples
nas suítes que não precisam de caminho longo; `hb\tests\tmp` não existia; a FILA precisa de `provenance.json`/`coordinator.json`/
`transport.json` ao lado do pacote e da memória canônica ativa) e 2 erros no meu teste novo (asserção errada de `replay_from_revision` em
`verify(deep=True)`, que replaya desde a âncora por desenho — a leitura normal parte do instantâneo 256; conexões sqlite não fechadas). Um
veredito do APP 31 (`test_operator_json_byte_backup_migration_and_soft_delete`) cai na linha seguinte a um print do código testado; o
parser do runner passou a tratá-lo (o `unittest` sempre contou 31 OK; por isso a rodada anterior somava 219 na minha tabela e a final soma 220 — o total real sempre foi 220).

## 3. Ponta a ponta N=300 (`evidencias\e2e_n300.json`) e comparação

| grandeza | medido [REAL] | frente 1 (N=300, `1_NUCLEO\TESTES.md`) [DECLARADO pela frente] | v1 (auditoria 12/10) [DECLARADO] |
|---|---|---|---|
| banco | 3.231.744 B | 3.215.360 B | ≈ 54,8 MB extrapolados [DERIVED] |
| diário | 629.755 B (301 linhas, 1 arquivo) | 607.616 B | — |
| instantâneos | 3 locais 7.537.018 B + 3 arquivados 2.947.146 B | 7.475.200 + 2.912.256 B | 300 backups ≈ 5,19 GB [DERIVED] |
| transição mediana (últimos 100 / geral) | 29,9 ms / 17,5 ms | 30,2 / 17,3 ms | 0,41 s em N=150, expoente 1,36 |
| p90 / máx. | 32,3 / 88,7 ms | 34,1 / 93,6 ms | — |
| transição pelo CLI de sessões (processo novo) | mediana 0,168 s | — | ≈ 5,3 s + cópia de 357 MB (produção hoje) |
| verify deep (replay desde a âncora) | 0,34 s | — | — |

O diário e o CLI estão no caminho: 5 das 300 transições passaram por `session_memory.py` em processo novo (init, project e verify também),
com o mesmo guard D4 ativo. A projeção (24 KB) e o verify do CLI devolvem os campos v1 (contrato) mais os v2 (aditivos).

## 4. Ensaio de migração (`evidencias\migracao_ensaio_3ctx.json`) [REAL]

Banco v1 sintético construído pelo **código v1 congelado** (`tests\store_v1_frozen.py`, sha256 = `store.py` instalado `2d4f6214fa433534`):
`ctx_0` 150 eventos, `ctx:1` 25 (id com `:` como os do app), `ctx_2` 0 — 16.019.456 B e 178 `memory.sqlite3.bak_*` (um por mutação, como a
produção). `migrar_para_delta.py` do candidato: dry-run devolve as cabeças e **não muda um byte** (sha256 igual, sem `journal\`); `--apply`
em 0,51 s com `--receipt`, `--second-copy-dir` e `--snapshot-archive-dir`: `ok`, 0 `head_mismatches`, cabeça de cada contexto (revisão,
`state_sha256`, `event_hash`) igual à v1, `verify_after` ok nos 3; backup `memory.sqlite3.pre_v2_*` + sidecar `.sha256` + 2ª cópia com o
sha256 do banco original; **linhas de `events` byte-iguais** antes/depois (só acréscimo); diário com N+1 linhas por contexto
(151/26/1); `--verify-only --deep` ok; segundo `--apply` → `already_migrated`; depois da migração uma transição v2 em cada contexto
(`legacy_events = N`, `delta_events = 1`, `journal_ok`); o código v1 congelado **recusa** o banco migrado. `mover_backups_antigos.py`:
dry-run não move; `--keep 3` move 175 (1.159.172.096 B) com sha256 conferido e `MANIFEST.json`/`.jsonl`, mantém os 3 mais recentes.

## 5. `implantar.py` / `reverter.py` e o ensaio (`ensaio_implantacao\ENSAIO_RECIBO.json`) [REAL]

`implantar.py --config <json>` (ordem exata, recibo gravado após cada passo, qualquer falha interrompe visível):
0 pré-conferências (Python ≥ 3.12; candidato == manifesto; **CAS**: cada alvo existente == original congelado, novos ausentes; banco sem
`-journal`, `journal_mode=delete`, sonda `BEGIN IMMEDIATE`; espaço em D: ≥ 2× banco + backups a mover) → 1 parar o app
(`stop_iald_web.ps1`: supervisor + filho; `gerir_processos`) → 2 backup integral (`memory.sqlite3.pre_v2_<stamp>` + `.sha256` em `state\` e 2ª
cópia conferida em `D:\IALD_ARQUIVO\MEMORIA_IALD\pre_v2\`) → 3 migração (`migrar_para_delta.py` do candidato: dry-run, depois `--apply`
com recibo; verify deep) → 4 substituição dos 15 arquivos (`<alvo>.bak_<stamp>` de bytes conferido; tempário → fsync → `os.replace`;
`__pycache__` da lib posto de lado) → 5 `aplicar_blocos.py` (CAS pelo sha16 do bloco; 5 arquivos + linha do MEMORY.md ≤ 200 linhas/24.000 B)
→ 6 `mover_backups_antigos.py` INSTALADO (`--keep 3`, para `D:\IALD_ARQUIVO\MEMORIA_IALD\backups_ate_20261012`; `--pular-mover-backups`
adia) → 7 verificação final (sha256 de cada alvo == candidato; `import iald_memory` da lib instalada; `--verify-only --deep`) → 8 reiniciar
o app (`start_iald_web.ps1` desacoplado; `/login` 200) → `RECIBO_IMPLANTACAO.json` com sha256 antes/depois de cada arquivo.
`--dry-run` só confere e roda os dry-runs (migração, blocos, backups) — nada muda. Config de produção:
`implantar_config_producao.json` (raízes = identidade, `gerir_processos: true`, `exigir_app_parado: true`).

`reverter.py --recibo RECIBO_IMPLANTACAO.json`: parar o app → restaurar cada arquivo do seu `.bak_` (sha256 conferido contra o recibo; o
conteúdo atual vai para `<alvo>.v2_revertido_<stamp>`; os 6 novos viram `<alvo>.removido_<stamp>`) → restaurar o banco do `pre_v2_*`
(sha256 conferido; o banco v2 vai para `memory.sqlite3.v2_revertido_<stamp>`; `journal\` e `snapshots\` ficam como evidência: os eventos
posteriores à migração **não voltam** ao banco v1 — ficam nos diários) → restaurar os blocos dos `.bak_` do `BLOCOS_RECIBO` → os backups
legados **ficam em D:** (íntegros, manifesto) salvo `--mover-backups-de-volta` → reiniciar → `RECIBO_REVERSAO.json`. **Nada é apagado.**

Ensaio (`ensaio_implantacao\rodar_ensaio.py`, sob a guarda): cópia completa da instalação em `ensaio_implantacao\raiz\` (22 arquivos
originais + exemplos; banco v1 sintético de 3 contextos, 60/20/0 eventos, 2.912.256 B, **83 backups por mutação** 113.192.960 B; as 6
superfícies D5 copiadas de produção; «D:» sintético). Resultados: `--dry-run` → `DRY_RUN_OK` e inventário idêntico (0 extras);
`implantar.py` → `CONCLUIDA`, 9/9 passos OK em 3,1 s; conferência independente: 15 alvos == candidato, `schema_version = 2`, 3 linhas em
`snapshots` e `context_state`, 3 `.bak_` em C: e 80 em «D:» (manifesto 80 linhas), `pre_v2` local + em «D:», bloco novo no topo dos 5 e
bloco antigo ausente, linha nova no MEMORY.md (186 linhas, 18.563 B), o **CLI de sessões instalado** faz `get` (rev 60) → `transition`
(rev 61) → `verify` (ok, 62 eventos, `journal_ok`) em processo novo, cabeças da migração iguais à v1; `reverter.py --dry-run` e
`reverter.py` → `REVERTIDA`, 6/6 OK: **todo arquivo original byte-igual ao inventário de antes**, banco com o mesmo sha256, 80 backups
legados íntegros em «D:» (sha256 igual) — extras só `.bak_*`, `.removido_*`, `.v2_revertido_*`, `pre_v2`, `journal\`, `snapshots\`.
Variante B (segundo ciclo, reversão com `--mover-backups-de-volta`): **identidade total**, 80 devolvidos. Guarda: 0 bloqueios.

## 6. O que a gerência precisa saber antes de implantar [INPUT/OPEN]

1. **Janela quieta.** Hoje 13/10 o filho web (PID 64412, supervisor 58980) está vivo com o llama `:8081` online e o heartbeat v1
   gravando (banco 357.388.288 B; 772 backups = 95,1 GB; +1 desde 00:55). `implantar.py` para o app via `stop_iald_web.ps1` e o sobe
   via `start_iald_web.ps1` desacoplado — o supervisor novo nasce de um `Start-Process`, não do lugar de onde o atual foi lançado; se o
   operador prefere subir à mão, use `--sem-reiniciar`. Os 8 `mcp_server.py`/`mcp_um.py` vivos importam `iald_memory` preguiçosamente:
   se já importaram a v1, falham fechado (`SchemaMigrationRequired`, visível) até reinício (R2 da especificação).
2. **Custo em disco.** A migração do banco real (764+ eventos, 354 MB de `state_json` legado) mantém os eventos imutáveis: o banco não
   encolhe (R1); o `pre_v2` são **2 cópias de 357 MB em C:** (passo 2 + a interna da migração) e 1 em D:; os instantâneos D2(b) de um banco
   de 357 MB custam 357 MB cada (3 em C:, resto em D:) até a gerência decidir a opção D1-B da especificação [OPEN]. Mover os 772 backups
   (95 GB) para D: leva dezenas de minutos: `--pular-mover-backups` permite fazê-lo depois com o script instalado.
3. **Psion (D3c).** Não há restauração: a frente 2 mediu que a condição «só o heartbeat gravou depois» não é verificável por script
   (dois pilotos também gravam o arquivo) → dúvida → não restaurar; só o feed degradado para. O script condicional da frente 2
   (`2_HEARTBEAT\scripts\psion_restore_conditional.py`) exige atestação explícita do operador. Fora do `implantar.py`.
4. **MEMORY.md está sendo editado por outra sessão durante a integração** (mtimes 13/10 01:12 e 01:39; na última medida 18.690 B, 187
   linhas, sha16 `cb28870582a02883`). O `aplicar_blocos.py` só exige exatamente 1 linha `- Memória ACOM:` (há 1) e os limites
   (≤ 200 linhas, ≤ 24.000 B; hoje 187/18.690) — segue aplicável, mas a margem de linhas é de 13; o CAS dos 5 blocos é pelo sha16 do bloco
   (`3106d7234c7a3b71` ×4, `2ca1cb060ecd2119`), inalterados [REAL, `PRODUCAO_INTOCADA.json`].
5. **Primeiro passo recomendado:** `python -X utf8 implantar.py --config implantar_config_producao.json --dry-run` (só leitura, salvo a
   sonda `BEGIN IMMEDIATE`/`ROLLBACK`, que toma a trava de escrita por um instante) — eu NÃO o rodei em produção por ordem desta tarefa.
6. **Registros de casa que não cabem a mim:** mapa de rotas, quadro, Atlas, memória da gerência, `README.md`/`SESSION_MEMORY.md` da
   memória (correção ao lado) e o aceite F9 — atos da gerência.

## 7. Entregáveis (`MANIFESTO.json` com sha256 de cada arquivo)

`candidato\` (15 arquivos) · `originais\` (13, byte-iguais à produção) · `merge\` (evidências dos dois merges) · `CANDIDATO_MANIFESTO.json` ·
`DIFF.patch` + `DIFF_APPLY_CHECK.json` · `implantar.py`, `reverter.py`, `implantacao_lib.py`, `implantar_config_producao.json` ·
`ferramentas\aplicar_blocos.py`, `ferramentas\SESSION_BRIDGE_v2.md` · `testes\` (`montar_suite.py`, `rodar.py`, `src_integracao\`,
`TESTES.md`, `RESULTADOS_TESTES.json`, `SUITE_MANIFEST.json`) · `ensaio_implantacao\` (`rodar_ensaio.py`, `ENSAIO_RECIBO.json`, `raiz\` com os
recibos do ensaio) · `evidencias\` (`e2e_n300.json`, `migracao_ensaio_3ctx.json`, `PRODUCAO_INTOCADA.json`, `unittest\*.txt`) · `guard\`
(cópia da guarda) · `guard_log\`.


> ⚠ **AO LADO (13/10/2026, R2):** a revisão de 13/10 achou 4 defeitos bloqueantes neste candidato: reversão de implantação parcial, ReDoS no filtro D4, gestão de processos sem ensaio e em conflito com a Tarefa Agendada, e leitura do `write_reference` sem guard. A correção está em `RESULTADO_INTEGRACAO_R2.md`, com o candidato `candidato_r2\`, o `CANDIDATO_MANIFESTO_R2.json` e os `implantar.py`/`reverter.py` R2. As versões R1 dos scripts ficaram em `*.bak_r1_*`. O texto acima fica como registro do R1; o candidato e as ferramentas vigentes são os da R2.
