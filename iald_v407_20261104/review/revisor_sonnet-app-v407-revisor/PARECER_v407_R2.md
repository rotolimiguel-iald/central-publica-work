# PARECER v407 R2 — revisão independente da INSTALAÇÃO (ator `sonnet-app-v407-revisor`)

Data: 2026-11-04T18:05Z. Release: `C:\IALD\Central de Patentes\work\iald_v407_20261104`. Plano sha256 `06457405144238152db0cdd678b849d82497e32d8b7222a6c355cfdc5e9092d4`.

**Veredito: ACEITO (tarefa `deploy`). Nenhum achado ALTO ou MÉDIO.** Esta rodada cobre D1–D6 e D9 (parcial); D7–D8 (`verify`) ficam para a segunda mensagem do orquestrador e a tarefa `verify` não é tocada aqui.

## Partitura (dita antes de medir; texto integral em `PARTITURA_R2_antes_de_medir.md`, sha16 `f4b78ff0c79d86bf`)
Decide se o que está instalado em `C:\IALD\projetos_pyhton\IALD` é o plano que eu revisei, se o escopo medido pelo código bate com a minha varredura própria e se o processo web novo é o esperado; **não** decide valor científico nem resposta ao vivo; um FAIL seria **parede medida** (instalado diferente do plano), nunca uma palavra sobre a teoria. Escolhas ditas antes: recálculo próprio dos bytes (não importo `verify_installed.py`), três visões de tempo, varredura de mtime da árvore inteira sem podar, re-medição própria dos agregados, só leitura de processos e o único GET permitido.

## Resultado
| item | veredito | número-chave |
|---|---|---|
| D1 | PASS | plano `0645740514423815` = `review_final` = `deployment` = `final_checks`; as 4 ferramentas têm o sha que o `review_final` pinou (`transaction.py` `85ad37fe3648e446`); `review_final.json` inalterado desde o meu aceite (`33dd393f24d01f6f`) |
| D2 | PASS | 1782/1782 destinos com o sha do plano (83373806 B); origem (staging) 1782/1782; `deployment.files` 1782 entradas, 0 divergentes |
| D3 | PASS | 7 backups `.bak_20261104_145150_458546` ao lado dos destinos, bytes = baseline do plano, todos anteriores à escrita do destino; sem `mobile_backups` nem `rollback_new_files` |
| D4(a) | PASS | RUNTIME_BASELINE 170/170 intactos + manifesto: backup `08f37779d15f12f1` = baseline, novo `2f201b5143a35dd0` = plano; 0 `.py` de runtime mudado; 0 extra/ausente/tmp no alvo |
| D4(b) | PASS | janela estrita `14:51:50.224`–`14:52:24.486` (34.26 s): **1782 plano + 7 backups + 3 logs do supervisor/web, 0 outros**; 87761 arquivos varridos sem podar; depois da janela só 2 telemetrias; os 19 caminhos do B1 nomeados abaixo |
| D4(c) | PASS | `accounts_modified`, `bench_restarted`, `client_files_changed` = `false` (booleanos, não `null`), `errors` vazio, `bench_changed` vazio; agregados antes = depois; **re-medição minha**: cliente 266 arquivos/5902150 B e estado 120/16396666 B com agregado igual ao `*_after` |
| D5 | PASS | pid antigo 14740 ausente; novo 66348 filho do supervisor 44292 (create_time exato `1793779969.9343488` = `maintenance.json`); `8082` ouve só o pid novo; `GET /login` = 200 (4727 B); 18765/18766 sem ouvir antes, depois e agora; 8081 = llama-server pid 11900, mesmo create_time |
| D6 | PASS | `iald_nucleo_fixo.json` sha `2f201b5143a35dd0` = `manifest_install.json` = plano, último item (1782 de 1782); release `v407` nos três campos; pino e commit certos; 1774 arquivos sob `canonical_releases\v407_bf9017157406` = 1774 do plano |
| D9 (parcial) | PASS | meu rastro: 1 connect permitido (127.0.0.1:8082), 0 `.env`, 0 subprocesso, 0 escrita fora da pasta; código do deploy sem rede externa nem provedor; evidências sem pista de provedor ou segredo. **Os carregadores (D7) ficam para a segunda mensagem.** |

Evidência submetida pelo construtor (`deployment.json` `75f7ceb43ada478e`, `maintenance.json` `7ad67d5f4c53ead8`, `restart.json` `4e3975b52c710728`, `deploy_stdout.txt`): inalterada desde a submissão: sim.

## O que os três campos medidos valem (declaração pedida)
`accounts_modified`, `bench_restarted` e `client_files_changed` valem **só para os arquivos que o código mediu**: 120 de estado, 266 de cliente e os listeners 18765, 18766 e 8081. **A cobertura do resto é a minha varredura de mtime**, que visitou 87761 arquivos de `C:\IALD\projetos_pyhton\IALD` (nada podado) e não achou nenhuma mudança fora do plano, dos backups e dos logs. O B1 da rodada 1 segue sem correção de código; para esta instalação o resíduo está fechado por evidência, não por código.

## D4(b): os 19 caminhos do B1, com mtime, frente à janela estrita 14:51:50.224–14:52:24.486 de 04/11/2026
| caminho | arquivos (agora / rodada 1) | mtime mais novo | dentro da janela? |
|---|---|---|---|
| `owner_private` | 38 / 38 | 2026-10-23 17:02:29 | **fora, antes** (0 dentro, 0 depois) |
| `owner_private\chat_privacy` | 15 / 15 | 2026-10-23 17:02:29 | **fora, antes** (0 dentro, 0 depois) |
| `iald_saldo_claude.json` | 1 / 1 | 2026-09-23 08:40:35 | **fora, antes** (0 dentro, 0 depois) |
| `iald_saldo_openai.json` | 1 / 1 | 2026-09-24 09:12:58 | **fora, antes** (0 dentro, 0 depois) |
| `iald_uso_claude.json` | 1 / 1 | 2026-10-07 21:55:40 | **fora, antes** (0 dentro, 0 depois) |
| `iald_uso_openai.json` | 1 / 1 | 2026-10-02 05:36:44 | **fora, antes** (0 dentro, 0 depois) |
| `iald_pedidos_acesso.json` | 1 / 1 | 2026-09-24 16:00:22 | **fora, antes** (0 dentro, 0 depois) |
| `iald_access_requests.json` | 1 / 1 | 2026-09-13 20:00:18 | **fora, antes** (0 dentro, 0 depois) |
| `iald_contract_requests.json` | 1 / 1 | 2026-03-19 11:49:31 | **fora, antes** (0 dentro, 0 depois) |
| `.iald_runtime\task_runs` | 87 / 87 | 2026-10-30 20:14:10 | **fora, antes** (0 dentro, 0 depois) |
| `.iald_runtime\task_artifacts` | 63 / 63 | 2026-10-02 08:06:32 | **fora, antes** (0 dentro, 0 depois) |
| `iald_sync_central_estado.json` | 1 / 1 | 2026-09-24 16:00:23 | **fora, antes** (0 dentro, 0 depois) |
| `iald_deadlines.json` | 1 / 1 | 2026-10-23 14:51:06 | **fora, antes** (0 dentro, 0 depois) |
| `iald_memoria.json` | 1 / 1 | 2026-09-14 14:10:06 | **fora, antes** (0 dentro, 0 depois) |
| `app` | 126 / 126 | 2026-10-23 13:56:04 | **fora, antes** (0 dentro, 0 depois) |
| `iald_chat.html` | 1 / 1 | 2026-09-14 23:02:44 | **fora, antes** (0 dentro, 0 depois) |
| `sw.js` | 1 / 1 | 2026-08-21 19:27:30 | **fora, antes** (0 dentro, 0 depois) |
| `manifest.json` | 1 / 1 | 2026-10-01 14:26:09 | **fora, antes** (0 dentro, 0 depois) |
| `icons` | 3 / 3 | 2026-03-12 09:53:36 | **fora, antes** (0 dentro, 0 depois) |

Os 19 ficam fora e antes do deploy (o mais novo é `.iald_runtime\task_runs`, 30/10/2026 20:14:10; `iald_deadlines.json` é de 23/10/2026 14:51:06, a data é outra apesar de a hora lembrar a janela). Nenhum deles é destino do plano.

## Mudanças depois da janela (web novo e outros serviços)
2 arquivos, ambos telemetria em `logs\`: `logs\gpu_20261104_072914.csv` (15:05:34.960), `logs\iald_heartbeat_telemetry.jsonl` (14:53:54.436). Nenhum arquivo de estado: os 120 de estado têm mtime anterior ao deploy (120 antes, 0 na pré-janela, 0 dentro, 0 depois) e o agregado de agora é igual ao `state_aggregate_after`; não achei diferença, então não há arquivo a explicar. Na janela, os 3 logs são `logs\web-server_20261104_051250_r2.log`, `logs\web-server_20261104_051250_r2.log.err`, `logs\web-supervisor.log`.

## Achados (nenhum ALTO ou MÉDIO)
- **INFO R2-I1**: Os três campos medidos (accounts_modified, bench_restarted, client_files_changed = false, errors vazio, agregados antes = depois) valem SÓ para os arquivos que o código mediu: 120 de estado (16396666 B), 266 de cliente (5902150 B) e os listeners das portas 18765, 18766 e 8081. A cobertura do resto é a minha varredura de mtime: 87761 arquivos de C:\IALD\projetos_pyhton\IALD, nada podado, mtime ≥ início do deploy (14:51:47.474): só o plano (1782), os backups (7), 3 logs do supervisor/web na janela e 2 telemetrias depois dela. Os 19 caminhos do B1 ficam todos antes do deploy e com a mesma contagem de arquivos da rodada 1.
- **INFO R2-I2**: O web novo não escreveu estado medido depois da janela: os 120 arquivos de estado têm mtime anterior ao deploy e o meu agregado de agora é igual ao state_aggregate_after (o do cliente também). Mudaram depois da janela só dois arquivos de telemetria em logs\: gpu_20261104_072914.csv (logger de GPU que acrescenta uma linha a cada 15 s desde 07:29, iniciado antes da instalação) e iald_heartbeat_telemetry.jsonl (telemetria do heartbeat: o log do web novo diz 'Heartbeat Iniciado' e a linha das 14:53:54 é do tipo 'beat'). Não são estado nem são do plano; achei diferença em zero arquivos de estado.
- **INFO R2-I3**: Limite do método: o mtime só mostra a última escrita e não vê remoção. Fica coberto porque nada fora da telemetria tem mtime posterior à janela, as contagens dos 19 caminhos são as da rodada 1, os agregados dos conjuntos medidos são iguais e o plano não remove nada.
- **INFO R2-I4**: deployment.json grava status INSTALLED_RESTART_REQUIRED mesmo com o reinício feito: o reinício está em restart.json (PASS; pid 14740 para 66348). A string descreve a aplicação do plano (lição 2 da v406).
- **INFO R2-I5**: O log do supervisor traz '*** WEB SERVER MORREU | exit code =' às 14:52:05 e 'reiniciando em 5 s': é o supervisor, suspenso durante a janela, vendo o filho encerrado de forma controlada; 'PID 66348 iniciado' às 14:52:10. O novo filho nasceu 2026-11-04 14:52:10.886, 5.36 s depois da última escrita do plano; o stdout do web novo não tem sinal de erro e o .err tem 0 B.
- **INFO R2-I6**: Janela de manutenção 34.26 s (v406: 87 s); escrita do plano 13.69 s (14:51:51.834 a 14:52:05.523), mtimes não decrescentes na ordem do plano e o manifesto ativo por último; os 7 backups são anteriores às escritas dos seus destinos.
- **INFO R2-I7**: B2 da rodada 1 (nome de arquivo com substituto Unicode solitário derruba scope_compare) não se manifestou: o deployment.json foi gravado. B1 continua sem correção de código; a evidência desta instalação é a varredura acima.
- **INFO R2-I8**: D9 desta rodada é parcial: meu rastro (1 connect permitido a 127.0.0.1:8082, 0 abertura de .env, 0 subprocesso, 0 escrita fora da pasta) e a trilha do deploy (código sem rede externa nem provedor; evidências sem pista de provedor ou segredo). A parte dos carregadores de produção (0 rede, 0 .env e provider_calls 0 no INSTALLED_VERIFICATION.json) fica para o D7/D9 da segunda mensagem.

## Transparência
- Dois defeitos do MEU script: r2_extra.py indexava os backups por nome de arquivo e colidia (4 de 7 conferidos); percebi pelo número de linhas da saída, passei a indexar por caminho relativo (7 de 7) e reexecutei, e o veredito não mudou. r2_d9.py tinha um apóstrofo dentro de um literal (erro de sintaxe, sem veredito).
- Rotulagem: a classe 'log do supervisor ou web' do meu script reunia tudo sob logs\; depois de ver os dois arquivos que mudaram depois da janela, passei a nomeá-los como telemetria (não são logs do supervisor). Não mudei critério: a janela estrita continua sem nenhum 'outro'.
- Nenhum critério de PASS/FAIL foi alterado depois de ver dados nesta rodada; a partitura da rodada (PARTITURA_R2_antes_de_medir.md) foi escrita antes das medições.

## Conferência da partitura no fim
Cumprida: nada aqui fala da teoria; nenhum FAIL; os dois pontos que poderiam virar achado (estado escrito pelo web novo; contas e carteira fora da medição) foram medidos e deram vazio (estado idêntico ao agregado da instalação; os 19 caminhos inalterados desde antes do deploy). Reaproveitei e adaptei `check_d1_d4.py`, `check_scope_scan.py` e `check_d5.py` do revisor da v406 (-d); são novos `r2lib.py`, `r2_extra.py`, `r2_d9.py`, `r2_d4_function.py` e a re-medição própria dos agregados.

## Limites do exame
- Não instalei, não reiniciei, não matei nem iniciei processo; não rodei deploy_controlled.py, verify_installed.py nem teste_escopo_v407.py; a única rede foi o GET http://127.0.0.1:8082/login.
- Não tenho o hash por arquivo de estado do instante da instalação (só o agregado); por isso a explicação de qualquer diferença seria por mtime e pasta. Não houve diferença para explicar.
- D7 e D8 (carregadores de produção e INSTALLED_VERIFICATION.json) não foram feitos nesta rodada, por ordem do coordenador; a parte dos carregadores do D9 também fica para lá.
- Não avalio resposta ao vivo do app, celular físico nem valor científico; o GET /login prova que o web novo responde, não que responde bem.

## Arquivos
`W\validation\review_deploy.json` (sha16 `ebe98f71ccb77e30`); scripts e saídas em `W\review\revisor_sonnet-app-v407-revisor\` (`r2_*.py`, `r2_*_out.json`).

## Aceite registrado
`mission_step.py accept deploy` por `sonnet-app-v407-revisor`: event_id `v407-deploy-accept`, revisão 10, `deploy` = `satisfied`; evidência pinada `validation/review_deploy.json` (sha256 `ebe98f71ccb77e30b7b4f53fcb3a46539c20dbba7621e4c7814452354e9cd5fc`). `verify` segue `open` (nada tocado): o construtor a reivindica e submete depois da segunda mensagem; D7, D8 e a parte dos carregadores do D9 serão `validation/review_verify.json`.


---

## Verify (D7–D8) — secção ao lado (escrita depois da segunda mensagem do orquestrador; o que está acima fica como estava)
Data: 2026-11-04T18:13Z. Evidência em exame: `INSTALLED_VERIFICATION.json` (sha16 `e9199e03d96bd03f`) e `verify_stdout.txt` (sha16 `6207f961d85792e6`), escritos às 15:07:05 pelo `verify_installed.py` (15:07:00–15:07:05). **Veredito: ACEITO (tarefa `verify`). Nenhum achado ALTO ou MÉDIO.** Esta secção substitui, para D7, D8 e D9 dos carregadores, as frases acima que diziam que ficavam para depois.

**Partitura (dita antes de medir; `PARTITURA_R2b_antes_de_medir.md`, sha16 `3266d23b7d4361a8`):** decide se os carregadores de produção aceitam a v407 instalada e se o `INSTALLED_VERIFICATION.json` coincide com o que eu meço; não decide resposta de modelo ao vivo nem celular; um FAIL seria parede medida. Escolhas ditas antes: processo novo sem rede (nenhum evento `socket` permitido), os mesmos argumentos do `iald_web_server.py`, tokens lidos de quatro fontes (não recomputados), três controles negativos (um numa cópia adulterada), D8 campo a campo.

| item | veredito | número-chave |
|---|---|---|
| D7 manifesto ativo | PASS | `operational_core.current_release` = `active_cluster.release` = `jev_control.release` = `v407`; `release_source_sha256` = pino (`833121339e649f71…`) nos três; `jev_control.sha256` `f2268cd01c699285…` = sha do `jev_control_v407.json` instalado; cluster e núcleo operacional com o sha do arquivo instalado |
| D7 kernel e release | PASS | `KernelCatalog`: sha = pino, 1756 arquivos formais (1752 `.lean`); `load_release`: identidade v407 com `cluster_sha256` `6fa0d7b23ccc6e02…` e `operational_core_sha256` `edae343584ca123b…`, ambos iguais ao sha do arquivo instalado |
| D7 contrato JEV | PASS | `load_contract`: release `v407`, `source_sha256` = pino, `result_sha256` e `proof_manifest_sha256` = os arquivos instalados, `core_packet` `core_packet_v407_bound.txt` com o sha do arquivo da raiz |
| D7 pacotes | PASS | haiku55: **807627 tokens permanentes**, 1513572 B, sobra 173418; haiku: **415829 tokens**, 841658 B, sobra 565216; carregador = manifest = native_count = recibo do staging; prefixo igual ao do staging; saída reservada 16384; 0 pedidos de geração |
| D7 controles negativos | PASS | 4 de 4 recusas (release e dois pacotes com fonte errada; cópia com 1 byte do prefixo trocado) |
| D8 | PASS | 17 de 17 comparações iguais: status, `files_verified` 1782 (= meu D2), `identity` inteira, `public_commit`, tokens e bytes de haiku55 e haiku, `native_bytes` 53165, `public_prompt_bytes` 920403, `JEV_release`, `science_executed`, `provider_calls`; `verify_stdout.txt` é a mesma linha JSON; escrito depois do restart; evidência submetida inalterada |
| D9 carregadores | PASS | **0 tentativas de rede** (0 evento `socket` de qualquer tipo), **0 aberturas de `.env`**, 0 de segredos, 0 subprocessos, 0 escritas fora da minha pasta; 94 módulos de topo importados, nenhum de provedor; `provider_calls` 0 (ver V1: é literal do verificador, e a minha medida o sustenta) |

Corroboração: o web novo imprimiu na partida `[IALD-CANONICAL-CATALOG] release=v407 source_sha256=833121339e649f71 lean_files=1752` (o antigo: `release=v406 … lean_files=1743`).

### Achados desta parte (nenhum ALTO ou MÉDIO)
- **BAIXO V1**: `provider_calls: 0` e `science_executed: false` do INSTALLED_VERIFICATION.json são LITERAIS do código de verify_installed.py (constantes no dicionário de saída: provider_calls = 0, science_executed = False), não medições; mesma classe do B2 da v406 (campos que parecem medida e são constante). O 0 é verdadeiro por construção (o script só chama carregadores) e eu o sustento com medida minha: 0 tentativas de rede (0 evento socket de qualquer tipo), 0 aberturas de .env, 0 subprocessos e nenhuma biblioteca de provedor importada. Para a v408: contar de verdade (gancho de auditoria) em vez de gravar 0.
- **INFO V2**: Os tokens permanentes são LIDOS, não recomputados (a contagem nativa é da API e não há rede). O `permanent_tokens` do carregador é o `budget.permanent_tokens` do `manifest.json`, depois de o carregador validar o manifesto contra o sha do prefixo, a política de saída/margem e a sobra ≥ 10.000. Verifiquei que quatro fontes dizem o mesmo número: carregador, manifest instalado, native_count instalado e o recibo do staging da rodada 1 (haiku55 807627; haiku 415829), e que prefixo, manifest e recibo têm o mesmo sha256.
- **INFO V3**: Corroboração independente do servidor: o stdout do web novo (`web-server_20261104_051250_r2.log`, linha 10) imprime `[IALD-CANONICAL-CATALOG] release=v407 source_sha256=833121339e649f71 lean_files=1752`, e o do web antigo (`..._r1.log`) imprimia `release=v406 source_sha256=ddcb91930982d614 lean_files=1743`: o processo que serve o app carregou a v407. `lean_files` bate com o meu `KernelCatalog` (1752; 1756 arquivos formais).
- **INFO V4**: Controles negativos: 4 de 4 recusas esperadas (release e os dois pacotes com fonte errada: «Canonical release, source and catalog differ»; cópia do haiku55 com 1 byte do prefixo trocado: «Memory changed since provider measurement»). A conferência pode falhar e não falhou. A cópia adulterada foi apagada.
- **INFO V5**: `files_verified: 1782` é o comprimento do plano que o verificador percorreu comparando sha256 de cada destino; igual ao meu D2 (1782). Não rehasheei os 1782 nesta parte (não reabri D1–D6). `iald_native_memory` importa `urllib.request` (auxiliar HTTP do llama) mas nenhum evento socket ocorreu; 94 módulos de topo importados, nenhum de provedor. Prompt público 920403 B com `private_atlas_included` = False; contexto nativo 53165 B; política `AUTOMATIC_ORDER[:2]` = ['kimi', 'mimo'].

### Transparência e limites (desta parte)
- Nenhum critério mudou depois de ver dados: a primeira execução do r2b_d7_d8.py já deu PASS. Dois ajustes de código no meu script foram feitos ANTES de rodar (a expressão que reúne os booleanos do manifesto e a leitura dos caminhos instalados do resultado selado a partir do manifesto ativo).
- A partitura desta parte (PARTITURA_R2b_antes_de_medir.md) foi escrita antes de qualquer medição dela.
- Não instalei, não reiniciei, não matei nem iniciei processo; nenhuma rede (o GET local do D5 não se repete aqui); não rodei verify_installed.py, deploy_controlled.py nem teste_escopo_v407.py; não importei verify_installed.py.
- Tokens permanentes lidos, não recomputados (contagem nativa é da API). Não há controle negativo do contrato JEV (o manifesto fixa caminhos absolutos; adulterar uma cópia exigiria reescrever o manifesto).
- O processo do construtor (15:07:00–15:07:05) já tinha terminado quando medi e não pôde ser auditado: o D9 vale para os MESMOS carregadores rodados no MEU processo novo (e sustenta o 0 do verificador por ser código só de carregadores), não é uma auditoria do processo dele.
- Não avalio resposta de modelo ao vivo nem celular físico; a carga dos carregadores e o log de partida do servidor não provam que o app responde bem.

### Aceite registrado (desta parte)
`validation/review_verify.json` sha256 `01704878c49be63d8ae9b7638273f7e90e4aedaf8d695c5c842285dc5eae951e`. O `mission_step.py accept verify` é registrado logo abaixo, depois de rodar.

`mission_step.py accept verify` por `sonnet-app-v407-revisor`: event_id `v407-verify-accept`, revisão 13, `verify` = `satisfied`; evidência pinada `validation/review_verify.json` (sha256 `01704878c49be63d8ae9b7638273f7e90e4aedaf8d695c5c842285dc5eae951e`). Missão: `active` vazio (`sources`, `app`, `deploy` e `verify` satisfeitas). Nada foi instalado, reiniciado, apagado fora da minha pasta nem escrito no runtime por mim.
