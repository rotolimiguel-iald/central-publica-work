# PARECER F0.3.MEMORIA_CIENTIFICA_SYNC — release v407 (R1)

Revisor independente (não construiu nada; somente leitura). Data: 2026-11-04, 07:43–08:00 (-03:00).
Release revisado: `C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\state\canonical_memory\releases\v407_4323b401f15cc971` (INATIVO; ACTIVE ainda v404).

## Veredito: PODE ATIVAR

Nenhum achado ALTO nem MÉDIO. Cinco observações BAIXAS (operacionais ou herdadas), nenhuma é defeito do release.
A condição prática é uma só: a ativação só vale se os 13 originais do Nós ainda forem os mesmos no instante da ativação (o próprio `activate` recusa, fail-closed, se mudarem; ver B1).

### A partitura (o que este parecer decide)
- DECIDE: se o release v407 preparado é fiel às 13 fontes admitidas lidas do Nós, e se a preparação não tocou em nada além do release novo na árvore `canonical_memory`/`Chatgpt\`.
- NÃO DECIDE: a ciência (conteúdo de `um.py`, kernel, vereditos do selo), o gate, nem se a v407 deve ser a versão ativa para os consumidores.
- Um NAO ATIVAR significaria só «a preparação tem defeito»; foi corrigível/refazível. Aqui o resultado foi positivo, não induzido por desenho de teste: todas as comparações abaixo são de igualdade de bytes/hash/linhas entre fontes e cópias, e cada uma podia falhar.

## Resultado por item da lista Q (consulta → resultado)

### Q1. Fontes (13 originais) — OK
Consulta: `scripts_revisor\rev_q1.py` (lê o catálogo `project_fisica\MANIFESTO_LOCAL.json`, exclui os 2 PDFs, compara bytes do VIVO no Nós/the_boundary × cópia em `snapshots\v407_4323b401f15cc971\` × `PREPARATION.sources` × `manifest.documents`). Saída: `REV_Q1_Q2.json`.
- Os 13 nomes do catálogo == `cm.SNAPSHOT_NAMES`. Para os 13: igualdade byte a byte vivo == snapshot (comparação de `bytes`, não só de hash); sha256 e tamanho iguais nas 4 fontes de verdade (vivo, cópia, PREPARATION, manifest); `mtime_ns` do vivo == `mtime_ns` registrado na preparação (nenhuma fonte mexida depois do prepare); catálogo `MANIFESTO_LOCAL.json` com o mesmo pin (4790 B, sha 98d2e9cc…).
- Reexecutado às 07:56:04: JSON inteiro idêntico ao da primeira execução (07:46) → fontes estáveis durante a revisão.
- sha16 (16 primeiros hex), bytes: `um.py` 833121339e649f71 (43.065.098); `um_absoluto.json` a67a29763f416334 (15.361.561); `um_absoluto_selo.json` d84834f41ec3d87c (247.049); `tgl_kernel_proof_manifest.json` b4b2eb7c53abcf8d (4.485.115); `um_absoluto_forma_canonica.md` fffb971e973d601e; `um_absoluto_manifest.md` 5cf089e0002bc959; `A_PROVA_DA_QG_TGL_arvore.md` 8e036027a26b925c; `DESENHO_DO_FECHAMENTO_QG.md` 902668ce29b4b61e; `MEMORIA_DA_LINHAGEM.md` c02475fdf718161c; `DA_IRMA.md` 5f348cd19e77f0a0; `A Ponte Einstein Cartan Miguel.tex` 8a2792d3c9ce52b6; `paper_PT.tex` 559d79fb81b0af6c; `ERRATA_20260919_…md` 060c82abee57a5d0.
- Selo (lido do vivo): `um_version = v407`; `fail_closed_selftest = FAIL_CLOSED_SELFTEST_PASSED`; `formal_source_hash` do selo == o do `tgl_kernel_proof_manifest.json` (048bffe0b4c5e9af…). `seal['sha256']` lista 14 nomes: os 5 que estão entre os 13 (`um.py`, `um_absoluto.json`, `tgl_kernel_proof_manifest.json`, `um_absoluto_forma_canonica.md`, `um_absoluto_manifest.md`) conferem, e os outros 9 (4 figuras PDF, 2 PDF, 2 .tex, `um_absoluto_pilar_quantico.json`) também conferem com o vivo: 14/14.
- `UM_VERSION`: regex do helper `findall == ['v407']`; a linha literal `UM_VERSION = "v407"` ocorre exatamente 1 vez (o token `UM_VERSION` aparece 12 vezes no total, as outras 11 são usos).
- Registros `estatuto_*` no core do `um_absoluto.json`: exatamente 3 (`estatuto_da_prova_v391`, `estatuto_da_prova_ressalva_v392`, `estatuto_reafirmado_v392`), todos `all_verified True` e `does_not_gate_core True`; `certificacao.um_py_sha256_lido_de_si` do v391 == sha256 do `um.py` vivo (833121339e64…). `ESTATUTOS_v407_….json` == esses registros (igualdade de objeto) e a fonte pinada dele é a cópia do snapshot (sha igual ao vivo). Versus v404: os 3 registros mudam só em contagens/hash dependentes da rodada (teoremas 9698→11958; declarações 29484→33863; auto-hash do um.py), sem registro novo ou perdido.
- Cada superfície conhece a v407 (regra da linhagem completa, medida por contagem): `um.py` 281, `um_absoluto.json` 102, selo 8, `forma_canonica` 7, `manifest.md` 5, `A_PROVA` 2, `DESENHO` 7, `MEMORIA_DA_LINHAGEM` 60 (última menção na linha 9797 de 9798). Zero em `tgl_kernel_proof_manifest.json` e `DA_IRMA.md` é da natureza deles (não versionados).

### Q2. Generation e epoch — OK
Consulta: `rev_q1.py` (sha256 de `json.dumps([(nome, sha256)…], ensure_ascii=False)` na ordem do catálogo).
- Recalculada a partir do VIVO, das CÓPIAS e da lista do manifest: as três dão `4323b401f15cc9715771c3129038f0ff43ad87fdeac7f71693bcfe725ab6147a` == `manifest.generation` == `PREPARATION.generation` == `CHECK_ANTES.sealed_generation`. A ordem dos documentos no manifest == ordem do catálogo.
- `epoch = 'v407_' + generation[:16] = v407_4323b401f15cc971` == nome do diretório do release == nome do `snapshot_root` == `PREPARATION.epoch`. (O `manifest.json` não tem campo `epoch`; o epoch está no `snapshot_root` e no nome do diretório. Não é defeito: `cm._verify_snapshot` exige `root.name == release + '_' + generation[:16]`.)

### Q3. Integridade do release — OK
Consulta: `scripts_revisor\rev_q3.py`. Saída: `REV_Q3.json`.
- `manifest.json`: 6.503 B, sha256 838dfcddd83b6816fb85910566c95cf8601001814f7d49485d702c46c5176511 == `PREPARATION.manifest`. O `manifest.json.bak_20261104_073912_267183` (6.178 B) é o primeiro manifesto do `build` e é igual ao final menos os 3 campos de snapshot (`source_mode`, `snapshot_root`, `snapshot_manifest_sha256`).
- `SEALED_SNAPSHOT.json` (2.458 B, sha 430891bfa0308bce…): bate com `manifest.snapshot_manifest_sha256`; `schema 1`; `release v407`; `generation`, `index_sha256` e a lista de documentos (nome, sha, bytes) iguais às do manifest; `formal_source_hash` (048bffe0…) igual ao do selo e ao do proof manifest dentro do próprio snapshot; `snapshot_root` aponta o diretório real; só os 13 nomes admitidos + o descritor, sem extras, sem symlinks, sem `.tmp_`/`-journal`/`-wal`/`-shm`.
- `index.sqlite3` (155.185.152 B): sha256 7aa60fdc68675dc87bcf2d038bf3072f61819fa6d829ee54064ddfa95bae580c == `manifest.index_sha256`. Cabeçalho SQLite: modo de diário legado (bytes 18/19 = 1/1, não-WAL), então a abertura `mode=ro` não cria arquivos. Aberto com `uri mode=ro`: `PRAGMA integrity_check` = `ok` (SQLite 3.50.4); `COUNT(*) FROM passages` = 32.302 == `manifest.chunks`; só a tabela `passages` (fts5) e suas 5 tabelas-sombra.
- Trechos/linhas: para os 13 documentos (não só 3), `passages` (first_line, last_line, body) == `cm.chunks(texto.decode('utf-8-sig'))` calculado sobre o VIVO e também sobre a CÓPIA; além disso a concatenação dos corpos de cada documento == o texto inteiro (nada perdido nem duplicado), a numeração de linhas é contígua e a última linha == `len(text.splitlines())`. Fim de linha preservado (os arquivos CRLF seguem CRLF no índice; nenhum tem BOM). Soma por documento = 32.302. Os números de linha coincidem com a contagem de `\n` do editor nos 13 (não há CR solto nem separadores exóticos).
- Reconstrução independente: `cm.build` sobre o catálogo staged, em diretório do scratchpad (nada em `Chatgpt\`), deu índice BYTE A BYTE idêntico (sha 7aa60fdc…580c), mesma generation e mesmos 32.302 trechos (`REV_REBUILD.json`, 2,1 s; o diretório de teste foi apagado depois).
- Nomes `estatuto_*` indexados: busca FTS `"<nome>"` acha trechos dos 3 (v391: 8 documentos, 15 trechos no `um_absoluto.json`; ressalva_v392: 6 documentos; reafirmado_v392: 6 documentos) e a busca literal confirma presença no `um_absoluto.json` para os 3.
- Recibos: `PREPARE_RESULT.json` == `PREPARATION` (objeto); `BUILD_INTENT` (fontes e pin do ACTIVE) == `PREPARATION`; `CATALOG_…json` == catálogo original só com as 13 fontes de texto redirecionadas às cópias do snapshot (PDFs e demais campos intactos) (`REV_RECIBOS.json`).

### Q4. Nada além do release novo na árvore `canonical_memory` — OK
Consulta: `scripts_revisor\rev_q4.py` (fotografia minha no formato de `baseline_f03.py`, com `sha256` até 4 MB; diff pelos campos bytes/sha256/mtime_ns). Saídas: `REV_BASELINE_A/B.json`, `REV_DIFF_A/B.json` (rodadas 07:49 e 07:56; na A uma bandeira informativa, `worker_lock_unchanged`, comparava formatos diferentes de registro e saiu False; corrigida na B; os números do diff não dependem dela).
- `BASELINE_ANTES` (338 arquivos, 16 releases) → fotografia nova (355 arquivos, 17 releases): 17 novos, 0 removidos, 0 alterados; os 17 novos estão todos sob `releases\v407_4323b401f15cc971\` (index, manifest, manifest.bak, SEALED_SNAPSHOT e 13 cópias). Contra `BASELINE_APOS_PREPARE`: 0/0/0 (nada mudou depois da fotografia do orquestrador, nem por minhas leituras).
- `ACTIVE.json` inalterado: 247 B, sha 1315b97c7dfb3b5629ab7d753bef59b6b465848c2deb07bae04b308bf9840efa (mtime 2026-10-28 22:03:11); `ACTIVE.json.worker.lock` (1 B) e os 14 `ACTIVE.json.bak_*` existentes (`ls | grep -c`) inalterados; manifests sha256 dos 16 releases anteriores inalterados.
- Nenhum arquivo preexistente tem mtime de hoje; o último escrito antes foi a ativação da v404 (28/10 22:03:11).
- Reforço sem baseline: `cm.load(release, refresh=False)` aprovou os 17 releases (índice e as 13 fontes de cada um conferem com o manifest do próprio release, `SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED`), inclusive os >4 MB que o baseline não hasheia. Layout do release novo == layout do v404 (mesmos 17 arquivos).

### Q5. `Chatgpt\` — o que mudou desde 07:30 de hoje (reportado sem julgar quem escreveu)
Consultas: (a) exatamente `find . -maxdepth 4 -newermt '2026-11-04 07:30'` excluindo o release novo (iniciado 07:43:11, terminou antes das 07:51; o `find` com `-printf` leva vários minutos nessa árvore); (b) varredura completa por `os.scandir` (`scripts_revisor\rev_q5.py`: 1.853.009 entradas, 1.792.613 arquivos, 60.396 diretórios), duas passagens (07:48 e 07:56).
- Resultado, idêntico em (a) e (b): UM item: o diretório `…\state\canonical_memory\releases` (mtime 2026-11-04 07:39:09.279; muda porque ganhou o subdiretório do release novo). Nada mais em `Chatgpt\`, em nenhuma profundidade; nada em `state\canonical_memory` fora do release novo; `__pycache__` não mudou. As duas passagens têm o mesmo total de entradas, logo minhas leituras não criaram arquivos lá.
- 4 entradas ilegíveis na varredura, todas em `ORDEM_013_RINGDOWN\cache\…` (venv/vendor, erro de acesso ou de caminho): sem relação com a memória.

### Q6. Módulo, CAS, quadro e o que `activate_release` grava — OK
Consulta: `scripts_revisor\rev_q67.py`. Saída: `REV_Q6_Q7.json`.
- `canonical_memory.py`: 24.714 B, sha256 f95ed18ee33e180f0b630fa713020304e8017a30d8961decf45bf8041102e97b == `PREPARATION.module_pin`; mtime 2026-10-21 10:35:53 (anterior a hoje). Pins dos outros módulos usados na ativação (todos com mtime anterior a hoje): `program_controls.py` 17159764a8cb9557 (07/10), `safe_files.py` 78fc572d31f8fcb0 (13/10), `process_lock.py` 1cbc947acc160688 (27/09), `policy.py` 7df276df8518ee66, `matrix.py` 96c9eef0d72700c4, `__init__.py` 8e7c75b276f4d936; helper `scientific_memory_sync.py` a1416481339cedc1 (13/10, não alterado); wrapper `rodar_f03_v407.py` ae9939bb489d08b2 (hoje 07:39).
- CAS: `PREPARATION.baseline_active_pin.sha256` (1315b97c…0efa, 247 B) == sha256 do `ACTIVE.json` AGORA; o conteúdo atual == `PREPARATION.previous_active` (v404_302dc102683e9fb1). `activate_release` exige `expected_active_sha256` de 64 hex, compara com o ACTIVE lido DENTRO do `process_lock` e recusa com «ACTIVE advanced since preparation; no overwrite» se divergir; se o alvo já for o ativo, devolve o ponteiro sem escrever.
- Quadro: `iald.py ver F0.3.MEMORIA_CIENTIFICA_SYNC` (leitura) e `require_claim` do próprio módulo: 1 unidade com esse id; `reivindicacao.quem = claude-app-orquestrador`, desde 07:36:39, `vence_em 2026-11-04T10:36:39-03:00` (vigente às 07:52; ~2h44min de folga); `status = ENTREGUE`, sem `gate` → `require_claim` devolve OK para claude-app-orquestrador e RECUSA `codex-coordenadora` (controle negativo). A unidade está na lista de `activate_release` (`F0.3`, `F9.2`, `F0.3.MEMORIA_CIENTIFICA_SYNC`).
- O que `activate_release` grava (para conferir o diff pós-ativação): nada em diário/evento; só em `state\canonical_memory\`:
  1. `ACTIVE.json.worker.lock` é aberto em `a+b` (já existe, 1 B; só escreve se vazio) e travado 1 byte durante a operação: deve ficar inalterado.
  2. `replace_bytes`: cria `ACTIVE.json.bak_<AAAAMMDD_HHMMSS_microseg>` com os bytes do ACTIVE antigo (esperado: 247 B, sha 1315b97c…0efa) e `ACTIVE.json.tmp_<mesmo carimbo>`, e faz `os.replace(tmp, ACTIVE.json)`: o `.tmp_` não deve sobrar.
  3. `ACTIVE.json` novo (formato `json.dumps(indent=2, ensure_ascii=False)`, que reproduz exatamente os 247 B atuais). Previsto por mim: 247 B, **sha256 b1869b7b821648e9e4555b080e07ed5306721e05b5ff2b50854cca0b43ce4df1**, conteúdo `{schema 1, release "v407", epoch "v407_4323b401f15cc971", generation "4323b401f15cc971…147a", manifest_sha256 "838dfcddd83b6816…6511"}`; o ponteiro previsto passa todas as regras de `resolve_directory`.
  4. Diff esperado: `ACTIVE.json` ALTERADO; 1 arquivo NOVO `ACTIVE.json.bak_*` (cairá em «novos fora do prefixo» no `diff_f03.py`: esperado, não anomalia); todo o resto igual (os 14 `.bak_*` antigos, o lock, os releases, o release v407 com seus 17 arquivos); mtime do diretório `canonical_memory` muda. O helper `activate` não grava recibo: o JSON `{status: ACTIVATED_BY_EXISTING_API, pointer: …}` sai no stdout do wrapper e o orquestrador precisa guardá-lo.
  5. Modos de falha (sem ativar): CAS divergente → exceção antes de escrever; lock indisponível → espera em laço (bloqueante, 0,1 s); `PermissionError` em `os.replace` (leitor com o arquivo aberto) deixaria `.bak_` e `.tmp_` e o ACTIVE antigo, repetível.

### Q7. Recuperação — OK
Consulta: `rev_q67.py` (chamo `cm.prepare` com o release como alvo e `allowed_sources` do helper, `mode='standard'`, `max_chars=24000`, consulta = os 3 nomes `estatuto_*`; só leitura, abre o índice `mode=ro`).
- `VERIFY_RESULT.json`: `PASS`, 13 documentos, 32.302 trechos; os recibos de `standard`, `maximum` e `deepseek_maximum` têm `generation` == a do manifest, `index_sha256` == o do manifest, `freshness = SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED`, pins dos documentos e sha das fontes dos trechos == os do manifest; `provider_calls 0`, `source_execution false`.
- Minha recuperação: `generation` == manifest; `packet_sha256` 06d374a10f787e16ee9462197ae9c92b177b64476f73d0ecb439a242987fa64a == sha256 do prompt == o `packet_sha256` do VERIFY (reprodutível, mesmas 6 fontes); 16.185 B, 0 bloqueados, `weights_modified False`. Conferi cada um dos 6 trechos devolvidos (arquivo, linha inicial, linha final) contra o texto do snapshot: corpo == fatia exata de linhas, em todos. Sonda com «UM_VERSION v407 rodada selo»: o release novo devolve 14 menções a v407 (de `um.py`, `forma_canonica`, selo) e, hoje, pelo ponteiro ACTIVE (v404), só 1 (eco da própria pergunta): é a diferença que a ativação produzirá.

### Q8. Escopo da escrita — OK, com a ressalva do que é declarado
Consulta: leitura de `work\scientific_memory_sync_20261103_v406\DECISAO_DO_OPERADOR_F03_VALE_PARA_V407_04nov.json`.
- A decisão (de `claude-app-orquestrador`, 05:37:57-03:00) cita as palavras do operador no chat: «Autorizo a escrita» (autorização anterior) e «Vale para a v407». Escopo literal: «uma escrita única de uma sessão Claude em Chatgpt\IALD_ORQUESTRACAO_20260923\state\canonical_memory (prepare + activate da sincronização), para a versão SELADA no Nós … v407 … Nada além disso em Chatgpt\»; esgota-se na ativação (ou recusa registrada), e depois `Chatgpt\` volta a ser só leitura para sessão Claude.
- Escrito: um release novo sob `state\canonical_memory\releases\` (17 arquivos e 3 diretórios), com recibos em `work\` (fora de `Chatgpt\`). Está dentro do «prepare». Não houve nenhuma outra escrita em `Chatgpt\` (Q4, Q5). A ativação, ainda não feita, é a outra metade autorizada.
- As palavras do operador eu só as vejo citadas no JSON escrito pelo orquestrador: `[DECLARADO]`, não verificado por mim (não vejo o chat).

## Achados

ALTO: nenhum. MÉDIO: nenhum.

BAIXO (observações; nenhuma exige refazer o release):
- B1 (operacional) — O Nós ainda se move: `HANDOFF_v407_CUSTODIA.md` foi escrito às 07:48:25 (`find . -maxdepth 1 -newermt '2026-11-04 06:30'` no Nós), isto é, a custódia está em curso. Dos 13 originais, os últimos a mudar foram `A_PROVA`, `MEMORIA_DA_LINHAGEM` e `DESENHO` às 07:30:00–07:30:12, e continuam idênticos ao release às 07:56:04. Se qualquer um dos 13 mudar antes da ativação, `activate` falha de modo seguro («Original changed; prepare a new sealed generation») e exigirá uma geração nova; e, se mudar depois, o `check` pós-ativação voltará `SEALED_ADVANCE_PENDING_SYNC` em vez de `CURRENT`. Sugestão: rodar `scripts_revisor\rev_q1.py` (1 s) imediatamente antes de ativar.
- B2 (por desenho) — O selo cobre 5 dos 13 originais; os outros 8 (`um_absoluto_selo.json`, `A_PROVA`, `DESENHO`, `MEMORIA_DA_LINHAGEM`, `DA_IRMA`, os 2 .tex e a errata) ficam fixados só pelo sha256 do próprio release (cópia de bytes), não pelo selo do programa.
- B3 (herdado) — `manifest.documents[].matches_fisica_snapshot` é False para 9 dos 13: o catálogo `project_fisica\MANIFESTO_LOCAL.json` é uma lista de pins de v369 (preparada em 2026-09-23). Idêntico no v404: não é novo.
- B4 (herdado) — 1 trecho (`DESENHO_DO_FECHAMENTO_QG.md`, linhas 38–74) casa a regex `FORBIDDEN` (confidenciais) tanto no v404 quanto no v407, na mesma posição; é recusado na recuperação (fail-closed), não por falha do release. Varredura dos 32.302 trechos: nenhum caso novo (`REV_FORBIDDEN_SCAN.json`; o conteúdo casado não foi impresso).
- B5 (procedimento) — `require_claim` recusa se o status da unidade for `AGUARDA_OPERADOR`, `FECHADA`, `AUDITADA` ou `BLOQUEADA`, ou se houver gate `OPERADOR:`; hoje é `ENTREGUE`. Não avançar a unidade antes de ativar. A reivindicação vence às 10:36:39.

## O que NÃO verifiquei
- A conversa em que o operador autorizou (Q8) e o «chamado da c1/gerência do LAR» (condição 2 da decisão; a nota da reivindicação o afirma): não há ORDEM de hoje sobre isso em `C:\IALD\TUNEL_CLAUDE_APP` (só filmes/relatórios). `[DECLARADO]`.
- O efeito da ativação nos consumidores (fila, web, MCP): pedidos já enfileirados com `memory_generation` fixada, processos que guardem a geração anterior, a regra «ACTIVE_POINTER_PER_REQUEST» em uso real. Nenhum consumidor foi exercitado.
- A ciência: não executei `um.py`, não li o kernel nem julguei os vereditos/gate do selo (só a igualdade de hashes e os guardas).
- O guarda compartilhado `iald_memory` não é importável neste ambiente, então a recuperação que fiz usou só a regex `FORBIDDEN` de `policy.py`.
- Não rodei `check`, `prepare`, `verify`, `activate` do helper nem o wrapper; repliquei as verificações com scripts meus (leitura). Não inscrevi esta revisão na memória ACOM (`session_memory.py` grava no banco comum; o escopo era somente leitura).
- Escritas por outros processos fora de `Chatgpt\` e de `state\canonical_memory` (Nós, quadro) estão fora do escopo; o quadro (`PROGRAMA.json`) mudou durante a revisão por ação de terceiros (atualizado_em 07:46:53).

## Como reexecutar
Todos os scripts estão em `review\scripts_revisor\` (Python 3.14, `-B -X utf8`, só leitura; escrevem apenas em `review\`; `rev_rebuild.py` constrói em diretório do scratchpad e o apaga depois — o diretório de teste já foi removido). Ordem sugerida antes da ativação: `rev_q1.py`, `rev_q4.py <tag>`, `rev_q67.py`.
Resumo numérico em `REV_*.json` (mesma pasta).
