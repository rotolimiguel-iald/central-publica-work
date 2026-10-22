VERIFICAÇÃO FINAL — conserto ACOM 12/10

Verificador independente do implantador. Só leitura em produção. Medido em 13/10/2026, 06:56–07:08 (hora local).
Ordem do operador: «resolva a questão da memória» (`cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt`, sha16 `78ef70e6f9868281`, medido por script) [REAL].

## Veredito em uma linha

**A IMPLANTAÇÃO NÃO FOI EXECUTADA EM PRODUÇÃO.** Os quinze alvos, os cinco blocos, o MEMORY.md, o banco e o app estão exatamente no estado «antes» do recibo de dry-run. Todo item que pede o estado «depois» dá **NÃO CONFERE**, porque a produção não mudou. Não houve defeito na implantação: ela simplesmente não aconteceu [REAL]. Conferem a integridade do banco v1 (verify numa cópia), o app (HTTP 200), a ausência de eventos em 10 minutos e o limite do MEMORY.md.

## Base

- Recibo lido: `4_INTEGRACAO\recibos_producao_r2\RECIBO_IMPLANTACAO_dry_run.json` (sha256 `c904d4b5b7334ed7…`), `status = DRY_RUN_OK`, `dry_run = true`, `mudancas_iniciadas = []` [REAL].
- Recibo dos blocos: `BLOCOS_RECIBO_20261013_064943_568793_dry_run.json` (sha16 `f68495b35c1a6d91`), `dry_run = true`, `new_sha256 = null` em todos [REAL].
- `RECIBO_IMPLANTACAO.json` de produção: **não existe** em `recibos_producao_r2` (glob de `RECIBO_IMPLANTACAO*.json` devolve só o dry-run) [REAL]. Os que existem estão em `ensaio_implantacao*\raiz\recibos` e `5_REVISAO_A\int\…`: são ensaios em sandbox, não produção.
- Os quinze candidatos em `candidato_r2` têm o sha256 que o recibo registra: 15 de 15 [REAL].

## Itens

| # | Item | Resultado | Medida |
|---|---|---|---|
| 1 | sha256 atual de cada arquivo substituído = sha256 «depois» | **NÃO CONFERE** | 0 de 15 iguais ao «depois». Os 8 alvos que já existiam têm hoje exatamente o sha256 «antes» (CORE.md `4691f443…`, store.py `2d4f6214…`, iald_web_server.py `7e48e90a…`, session_memory.py `c9c3aa21…`, SESSION_BRIDGE.md `49f1626d…`, policy.py `252bdeb7…`, operational_memory.py `1d6bf484…`, `__init__.py` `fc534f8d…`, iald_app_memory.py `422bd3aa…`). Os 7 novos (migrar_para_delta.py, mover_backups_antigos.py, journal.py, snapshots.py, migrate.py, guard.py) **não existem** [REAL]. |
| 2 | Backups existem e batem com «antes» | **NÃO CONFERE** | O recibo traz `backup: null` para todos os alvos. Nenhum `.bak_*` de 13/10 ao lado de qualquer alvo. Os 75 `.bak_*` antigos de iald_web_server.py e os 5 de policy.py são de setembro e outubro, anteriores, e nenhum bate com o «antes» de 13/10 [REAL]. Coerente com nada ter sido trocado. |
| 3 | O banco migrado passa em verify | **NÃO CONFERE** quanto à migração · **CONFERE** quanto à integridade do banco v1 | O banco **não foi migrado**: `schema_version = 1`, tabelas `contexts, events, metadata`, sem `snapshot_policy`, sem diário; 357.412.864 B; sha256 `9995fe8f49763e47…`, igual a `banco_antes` do recibo [REAL]. `PRAGMA quick_check = ok` (conexão `mode=ro`) [REAL]. O CLI instalado (`session_memory.py`, operation=verify) rodou numa **cópia** byte a byte do banco (sha da origem antes = depois = cópia = `9995fe8f…`; a cópia continuou com o mesmo sha depois do verify): **13 de 13 contextos ok**, 777 eventos ao todo (app_service 735) [REAL]. Rodei na cópia e não na produção porque o `MemoryStore` abre `BEGIN IMMEDIATE`, que pega o trinco de escrita do banco vivo. |
| 4 | Diário e instantâneos existem com a política | **NÃO CONFERE** | `state\journal`, `state\snapshots` e `state\snapshot` não existem. A única subpasta de `state` é `app_outbox`. No banco, nenhuma tabela `snapshot_policy` [REAL]. |
| 5 | Backups antigos em D: com os hashes do manifesto | **NÃO CONFERE** | `D:\IALD_ARQUIVO` não existe (nem `MEMORIA_IALD`, `backups_ate_20261012`, `pre_v2` ou `snapshots`). Não há manifesto. Os 777 backups legados continuam em `C:\IALD\MEMORIA_IALD\state`, com 96.910.958.592 B, número igual ao do recibo [REAL]. |
| 6 | O app responde HTTP 200 | **CONFERE** | `GET http://127.0.0.1:8082/login`: 200 no início, no fim da observação (07:06:47) e na medida final [REAL]. Só local, sem rede externa. |
| 7a | O heartbeat gerou telemetria | **NÃO CONFERE** | `C:\IALD\projetos_pyhton\IALD\logs\iald_heartbeat_telemetry.jsonl` não existe. O heartbeat com telemetria própria existe só no candidato (`HEARTBEAT_TELEMETRY_FILE`, D3), que não foi instalado [REAL]. |
| 7b | Nenhum evento na memória comum em 10 minutos | **CONFERE (não discrimina)** | Observação de 605,6 s (06:56:42–07:06:47), 21 amostras a cada 30 s: eventos 777 → 777, backups `.bak_` 777 → 777, tamanho e mtime do banco sem mudança [REAL]. **Ressalva:** a janela não testa o conserto. O intervalo do heartbeat é de 1.800 s, e o heartbeat instalado não grava evento desde **2026-10-11T20:57:31Z** (revisão 734 do contexto app_service). O último evento do banco (09:41:11Z de 13/10) é de sessão, não do heartbeat [REAL]. Silêncio por ausência de batida, não por correção. |
| 8 | Os cinco blocos têm o texto novo e a linha de substituição | **NÃO CONFERE** | Os cinco arquivos (`~\.claude\CLAUDE.md`, `~\.codex\AGENTS.md`, `projetos_pyhton\IALD\CLAUDE.md`, `PROGRAMA_IALD\README.md`, `COORDINATOR.md`) começam pelo marcador **antigo** `IALD_COMMON_ACOM_SESSION_ENTRY_20261010`. Nenhum tem o marcador novo `…SESSION_BRIDGE_20261012` nem a linha «substituído em 12/10/2026 por ordem do operador». Os sha256 são iguais ao `old_sha256` do recibo. Os backups que o recibo nomeia não existem [REAL]. O `SESSION_BRIDGE.md` continua o de 10/10 (`49f1626d…`) [REAL]. |
| 9 | MEMORY.md da Central ≤ 200 linhas e ≤ 24.000 B | **CONFERE** (limite) · linha nova **não aplicada** | 187 linhas, 18.690 B, sha256 `cb28870582a02883…` = `old_sha256` do recibo. Há uma única linha «- Memória ACOM:», ainda a de 10/10; a linha nova de 12/10 não está [REAL]. O limite vale hoje, e o dry-run projeta 187 linhas e 18.758 B depois da troca [DECLARADO pelo recibo]. |
| 10 | Produção intocada durante esta verificação | **CONFERE** | A segunda medida completa no fim (`MEDIDAS_PRODUCAO_FIM.json`) deu o mesmo resultado da primeira em alvos, blocos, MEMORY.md, SESSION_BRIDGE, backups, D: e telemetria. O banco manteve o sha `9995fe8f…` [REAL]. |

## O que falta para cada NÃO CONFERE virar CONFERE [DERIVED]

Todos dependem de um mesmo ato: rodar `implantar.py` sem `--dry-run`, com a configuração de produção. É **ato da gerência ou do operador** [INPUT]; o verificador não o executa. O dry-run de 06:49 garante que o CAS ainda vale: os 15 «antes» e os 5+1 `old_sha256` dos blocos batem com a produção medida às 07:08. Depois da implantação real, esta verificação deve ser repetida contra o `RECIBO_IMPLANTACAO.json` real. Para o item 7b, a janela de observação precisa conter pelo menos uma batida do heartbeat, isto é, mais de 30 min com o llama ONLINE. Sem isso, o silêncio não discrimina.

## Notas de método

- Nenhuma escrita em produção. Conexões SQLite só `mode=ro`, CLI de verify só na cópia (scratchpad da sessão), HTTP só em 127.0.0.1. Não rodei um.py nem scripts de selo, e não fiz chamada a provedor.
- Não executei o `init`/`transition` da memória ACOM que o CLAUDE.md global pede. Isso escreveria no banco de produção, contra a regra de só leitura desta tarefa, e criaria justamente o evento que o item 7b mede. Fica registrado como desvio deliberado [INPUT da tarefa].
- Confidenciais: não li nem copiei. Os `.bak_*` listados são só de arquivos não confidenciais.
- Evidências (sha256 por script):
  - `MEDIDAS_PRODUCAO.json` `9a9552a6e3a4032e…`
  - `MEDIDAS_PRODUCAO_FIM.json` `3f4ccf04dda957f7…`
  - `VERIFY_COPIA_BANCO.json` `2f4e20261c26199c…`
  - `OBSERVACAO_10MIN.json` `ed6376cc50f986ae…`
