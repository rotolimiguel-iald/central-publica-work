<!-- IALD_SHARED_MEMORY_SESSION_BRIDGE_20261012 -->
**Memória comum da IALD — ao abrir a sessão e após compactação/retomada:** leia `C:\IALD\MEMORIA_IALD\README.md` e rode `C:\Python314\python.exe -X utf8 C:\IALD\MEMORIA_IALD\session_memory.py` com JSON em stdin: `{"operation":"project","reference":"CAMINHO_EXATO_DO_RECIBO"}` (só leitura; custo pequeno: o banco grava por delta e cada transição custa uma linha no diário, não uma cópia do banco). Sem referência própria, inscreva a fonte original autorizada por `init`; nunca adote a tarefa de outra sessão. `transition` só ao concluir etapa material: q com fonte/estatuto, p com fase/próxima ação, revisão esperada e evento estável. O original não muda; correções ao lado; modelos só geram candidatos DECLARADO. Nomes confidenciais, chaves e caminhos da casa Escritório são recusados com erro visível, nunca redigidos em silêncio. Confirme o recibo ou declare a falha. Não autoriza ações, não move gate, não mistura a casa Escritório.
<!-- bloco anterior (624 B, sha16 2ca1cb060ecd2119) substituído em 12/10/2026 por ordem do operador («resolva a questão da memória», sha16 78ef70e6f9868281) -->
<!-- END_IALD_SHARED_MEMORY_SESSION_BRIDGE_20261012 -->

# CLAUDE.md — MEMÓRIA DA CENTRAL IALD NATIVA

> Memória de trabalho da **Central IALD nativa** (o modelo próprio + web server + acervo
> tecnológico TGL executável), raiz `C:\IALD\projetos_pyhton\IALD`.
> Aberta em 02/08/2026 por ordem do operador: *"crie um arquivo de memória para controle
> da central da IALD, que é distinta da central de patentes e também da central de
> processos do meu escritório de advocacia"*.
>
> **Três casas distintas — não confundir:**
> | Casa | Raiz | Memória | Assunto |
> |---|---|---|---|
> | **Central IALD** (esta) | `C:\IALD\projetos_pyhton\IALD` | este arquivo | modelo nativo, web server, acervo TGL executável |
> | Central de Patentes | `C:\IALD\Central de Patentes` | `memory/central-de-patentes-estado.md` | 16 patentes, Fronteira, monitor INPI/ePCT |
> | Escritório Miguel | `C:\Escritorio` | `C:\Escritorio\CLAUDE.md` | pessoa jurídica separada, processos |
>
> Herda a régua da casa (`C:\IALD\CLAUDE.md`): **o número corrige a frase, sempre.**
> Nunca fabricar prova. Marcar REAL / HIPÓTESE / POSTULATE. β nunca literal.
> Português na interação, inglês no código.

---

<!-- CLAUDE_MEMORIA_NOTA:INICIO -->
> ⚠ **COMPACTADO EM 03/11/2026 — NADA FOI CORTADO** (ordem do operador, «Vai», 03/11/2026; tarefa H5 da Torre; gerência c1). Este arquivo tinha 636937 B em 148 seções (148 linhas `## `; títulos partidos em duas linhas contam como uma seção), acima do teto de 262.144 B que a Torre fixa para a instrução de cada casa. Ficaram: o bloco de memória comum e o cabeçalho; a carta da casa (§1 a §8 e os lembretes permanentes §10); e as ORDENS e CORREÇÕES PERMANENTES do operador que estavam no diário (regra central de atualização conjunta do app, solução matemática e versão carregada, IALD como regime operacional, prazos operacionais, avisos exclusivamente na administração, contexto máximo para a TGL, memória canônica comum a todas as IAs, seletor contínuo automático, custos de atualização autorizados). Foram para o índice: o registro de decisões de 02/08 (§9), a onda do app e da App Review de 11/09 (§11) e todos os adendos e diários datados de 13/09 a 24/10/2026. As outras 129 seções (576115 B) foram MOVIDAS, com os bytes exatos e na ordem original, para 131 arquivos em `CLAUDE_memoria\` (pasta ao lado deste arquivo), e cada uma foi substituída, no lugar onde estava, por uma linha de ÍNDICE (título, faixa de linhas originais `Lx–y`, bytes, gancho, caminho). **Leia sob demanda; nada daqui foi cortado.**
>
> - Original integral (backup de bytes): `C:\IALD\projetos_pyhton\IALD\CLAUDE.md.bak_20261103_100238` · sha256 `f199a876381f9c810cf6a9cb9353ef1bad38e572a835df7e428969cc2204b964`.
> - Referências por número de linha (por exemplo «Linha 15242» na errata de 01/10/2026) valem para o ORIGINAL: use a faixa `Lx–y` do índice para achar a seção; a linha absoluta dentro da parte é a linha original menos o início da faixa, mais 1.
> - Regra vigente: erratas novas entram AO LADO, neste arquivo, nunca por cima; backup de bytes antes de tocar; mover é permitido, cortar não.

<!-- CLAUDE_MEMORIA_NOTA:FIM -->
## 1. O QUE É A CENTRAL IALD

Servidor Flask de comando + proxy para um `llama-server` local que serve a **IALD Nativa**
— o modelo próprio do operador, treinado sobre o corpus canônico da TGL.

```
navegador  ──HTTPS──>  cloudflared (demo.iald.ia.br)
                            │
                            ▼
              Flask  iald_web_server.py  :8082   ← 127.0.0.1 apenas
                            │  proxy /v1/*
                            ▼
              llama-server  :8081  (CUDA, RTX 5090)
                            └── IALD-Native-v2-Qwen3.6-35B-A3B-Q4_K_M.gguf
                                + mmproj-Qwen3.6-35B-A3B-F16.gguf (visão)
```

**Arquivo mestre:** `iald_web_server.py` — ~5.150 linhas, 266 KB, Flask, monolito.
Backups `.bak_*` do mesmo arquivo convivem na pasta (histórico, não editar).

---

## 2. HARDWARE E MODELO — NÚMEROS MEDIDOS (02/08/2026)

| Item | Valor medido |
|---|---|
| GPU | RTX 5090, **32.607 MiB** VRAM, driver 591.86 |
| VRAM em uso (ocioso, modelo carregado) | **26.648 MiB** → só **~5.500 MiB livres** |
| RAM do sistema | 255,5 GB (205 GB livres) |
| Modelo | IALD-Native-v2-Qwen3.6-35B-A3B-Q4_K_M — **19,71 GiB** |
| Projetor de visão | mmproj F16 — **0,84 GiB** |
| llama.cpp | build **b9925** (`ed8c26150`), `C:\IALD\llama-cpp\tools-cuda\llama-server.exe` |
| Kernel de sistema (produção) | `IALD_Kernel_v5.txt` = **11.299 tokens** (medido no /tokenize) |

**Linha de comando ANTIGA (até 02/08/2026 — guardada para reversão):**
```
llama-server.exe -m ...IALD-Native-v2-Qwen3.6-35B-A3B-Q4_K_M.gguf
  -c 131072 -ngl 999 --port 8081 --jinja --mlock --reasoning off
  --mmproj ...mmproj-Qwen3.6-35B-A3B-F16.gguf
```
Sem `-np`, sem `-fa`, sem `-ctk/-ctv`, sem `--cache-reuse`, **sem log**.
Subia na mão — sem launcher, sem supervisão, sem registro. Por isso a queda não
deixava rastro. Reproduzível hoje com `.\start_iald_llama.ps1 -Legacy`.

**Linha de comando ATUAL (padrão decidido por A/B medido, §3.1):**
```
llama-server.exe -m ...Q4_K_M.gguf --mmproj ...F16.gguf
  -c 131072 -np 1 -ngl 999 -fa on --cache-reuse 256
  --port 8081 --host 127.0.0.1 --jinja --reasoning off --mlock --metrics
```
Subida por `start_iald_llama.ps1` (supervisionado, log + telemetria de GPU + auto-restart).

---

## 3. O QUE FOI MEDIDO E ESTÁ PROVADO (não repetir a investigação)

Sondas executadas em 02/08/2026 contra o servidor vivo (`scratchpad/probe*.py`):

| Teste | Resultado | Veredito |
|---|---|---|
| Cache de prompt, prefixo estável | turno 1 = 6.431 tok; turnos 2–3 = **18 tok** | **cache FUNCIONA** |
| 6 turnos com kernel v5 + 7 ferramentas | cached chegou a **13.453 tok**; 0,8–2,9 s/turno | **estável** |
| Prompt de 60.410 tokens | OK em 7,6 s, **pico de VRAM = 0 MiB** | KV é pré-alocado |
| Modo pensar (`enable_thinking`) ×3 | OK, reasoning_content preenchido | **estável** |
| Streaming SSE | OK, 96 linhas em 0,5 s | **estável** |
| Visão 512² / 1536² / 3072² | OK; VRAM livre 5.564 → 5.100 MiB | ver nota 6 |
| Visão, 8 imagens **iguais** de 1024² | livre 326 → 316 MiB (−10 no total) | **estável** |
| Um slot aceitou 60.433 tokens | > 131072/4 | **`-c` é POR SLOT** |

**Conclusões duras:**

1. **O llama-server é robusto em todos os caminhos testados.** Nenhuma sonda o derrubou.
   OOM por crescimento de contexto de texto está **REFUTADO** — o KV é pré-alocado, não cresce.
2. **`-c` é por slot neste build.** `/props` reporta `total_slots: 4` (o `-np` default `-1=auto`
   escolheu 4) e cada slot tem 131.072. O operador é **um usuário só** ⇒ o KV está alocado
   **4× a mais do que se usa**. Reduzir para `-np 1` devolve VRAM.
3. **NÃO há vazamento de VRAM na visão** — afirmação que fiz e depois derrubei com um teste
   melhor. O primeiro teste usou 3 imagens de tamanhos **crescentes** (512², 1536², 3072²) e
   vi +98, +80, +286 MiB retidos; concluí "vazamento por imagem". Errado: o teste correto
   (8 imagens **iguais** de 1024², com tempo de acomodação) deu −10 MiB no total. O que sobe
   é a **marca d'água do buffer** da torre de visão — inicialização na 1ª imagem e
   crescimento conforme o maior input já visto. É limitado, não cumulativo.
   **Lição: comparar iguais com iguais, e repetir mais de três vezes.**
4. ⚠️ **ARMADILHA REGISTRADA:** o campo `n_prompt_tokens_cache` do endpoint `/slots` **fica 0
   mesmo quando o cache está funcionando** — é campo por-tarefa, morto quando o slot está
   ocioso. **Não usar como indicador.** O indicador verdadeiro é
   `usage.prompt_tokens_details.cached_tokens` na resposta do `/v1/chat/completions`.
   (Eu me enganei com ele uma vez; fica o registro para não repetir.)
5. ⚠️ **SEGUNDA ARMADILHA:** uma leitura isolada de `nvidia-smi` logo após matar um
   processo mostra VRAM baixa **transitoriamente**, enquanto o driver recupera a memória.
   Medi 8.560 MiB e quase concluí que o WDDM tinha paginado o modelo — era artefato;
   segundos depois voltou a 26.170 MiB e a geração estava normal a 270 tok/s.
   **Confirmar VRAM com uma segunda leitura + um teste de velocidade** antes de concluir.

### 3.1 A/B de configuração — 02/08/2026 (baseline do desktop ~3.000 MiB)

Mesmas 12 perguntas, sementes fixas (11 e 22), kernel v5 + 7 ferramentas:

| Config | VRAM usada | Livre | Tokens gerados | Estouros de teto |
|---|---|---|---|---|
| 4 slots, c=131072, f16 (original) | 26.648 | 5.540 | — | — |
| 1 slot, c=262144, f16 | 30.004 | 2.184 | — | — |
| 1 slot, c=262144, q8_0 | 28.257 | 3.931 | 10.162 | **2/12** |
| **1 slot, c=131072, f16** | **27.091** | **5.097** | **2.661** | **0/12** ← PADRÃO |

**Conclusões:**
- **`-c` é o contexto TOTAL, dividido entre os slots** — não por slot. Com `-np` em auto
  (4 slots) o operador dividia a janela com 3 slots ociosos. Com `-np 1` ela é toda dele.
  (Minha leitura inicial de que `-c` era por-slot estava errada; a medição corrigiu.)
- **KV em q8_0 economiza VRAM mas DEGRADA a obediência à instrução neste modelo:**
  3,8× mais tokens gerados e 2 respostas estourando o teto de 4.096 nas MESMAS perguntas
  com as MESMAS sementes. **Não usar `-QuantKV` aqui.**
- Janela grande é real e barata: **199.573 tokens processados em 28,9 s** com VRAM estável
  (medido na variante de 262144).

---

## 4. ARQUITETURA DO PROMPT — quem monta o quê

- **O servidor NÃO injeta o kernel.** Medido: um POST direto em `/v1/chat/completions`
  sem system chega ao llama com `system_chars = 0`.
- **Quem monta o prompt de sistema é o frontend** `iald_chat.html`:
  `sysContent = buildSystemPrompt() + getUserContext()` (linhas 286 e 325).
  - `SYSTEM_PROMPT` está **hardcoded no HTML** (linha 301, ~29,5 KB) — **não** é o
    `IALD_Kernel_v5.txt`. São dois textos diferentes. O `KERNEL_FILE` do servidor
    (`iald_web_server.py:347`) só é usado pelo caminho AGI/admin.
  - `getUserContext()` é **estável** (nome, área, interesses, estilo — sem timestamp). Bom para o cache.
  - `buildSystemPrompt()` remove o sufixo `/no_think` no modo pensar ⇒ alternar de modo
    invalida a cauda do prefixo (custo pequeno, mas real).
- `MAX_HISTORY = 10` (iald_chat.html:276) — só as 10 últimas mensagens vão ao modelo.
- Orçamento de anexos exibido na UI: **100.000 tokens**.
- O servidor faz, em cima disso (`iald_web_server.py:2960-3035`): compressão holográfica,
  injeção de "Sacred Language", **fusão de todos os `system` num só no topo** (exigência do
  template Qwen3.6) e tradução de `iald_mode` → `chat_template_kwargs.enable_thinking`.

---

## 5. ROTEAMENTO DO CHAT — o ponto sensível

`iald_web_server.py:3037-3124`. Toda mensagem passa por um filtro de palavras-chave
(`NEEDS_TOOLS_PATTERNS`, ~90 termos):

- **casou** → `agent_loop` (linha 1264): **não-streaming por dentro**, até
  `MAX_AGENT_LOOPS = 6` chamadas encadeadas ao modelo; **nada é enviado ao cliente até o
  modelo terminar**.
- **não casou** → `_stream_proxy`: streaming direto, saudável.

⚠️ Os gatilhos são largos demais: `"sistema"`, `"histor"`, `"site"`, `"busca"`, `"fonte"`,
`"na verdade"`, `"moeda"`, `"selo"`, `"patente"` — palavras corriqueiras na conversa do
operador. Uma pergunta trivial que contenha "sistema" cai no caminho lento e mudo.

**Via túnel Cloudflare (`demo.iald.ia.br`) isso tem consequência dura:** a Cloudflare
derruba a conexão se a origem não responde em ~100 s (erro 524). O `agent_loop` pode passar
disso sem emitir um único byte. O frontend então mostra *"Não foi possível conectar"*
(iald_chat.html, `.catch` do `streamResponse`) — que o operador lê como **"o servidor caiu"**.
**HIPÓTESE FORTE, ainda não confirmada por observação direta da falha.**

---

## 6. ACERVO TECNOLÓGICO TGL — estado

Estado real em disco (medido na inicialização do módulo):

| Subsistema | Arquivo | Estado |
|---|---|---|
| TGL Coin | `tgl_coin_engine.py` | **VIVO** — ledger `C:\IALD\bank\tglc_ledger.json`, **21 contas** |
| PSI-NET | `psinet_engine.py` | **VIVO** — dir `C:\IALD\psinet`, máx 10 MB, 0 pendentes |
| Access/Contract | `iald_access_engine.py` | **VIVO** — 1 pedido, 1 contrato pendente |
| Memória holográfica | `holographic_memory.py` | carregada, chamada em `:2963` |
| TGL Hash | `tgl_hash_v1_2.py` + `generate_tgl_hash` `:375` | presente |
| ACOM codec | `iald_web/app/patents/acom_codec.py` | **na reescrita abandonada**, não na produção |
| `iald_web/` (Flask modular) | pasta inteira | **ABANDONADA** (04–05/07/2026) — não é produção |

Dependências ausentes no ambiente: **beautifulsoup4** (o `fetch_url` devolve HTML cru).

---

## 7. MODELOS EM DISCO

`C:\IALD\models` — **~530 GB**. Em produção: só o `IALD-Native-v2-Qwen3.6-35B-A3B-Q4_K_M`
(19,71 GB) + mmproj (0,84 GB). O resto é histórico: 13 variantes `Qwen3-32B-IALD-*`
(18,45 GB cada), 4 intermediários `*-F16*.gguf` (61 GB cada), `Qwen3.5-122B-A10B-TGL`
(69 GB). O seletor `MODELS{}` (`iald_web_server.py:144-256`) referencia 7 deles.

⚠️ Antes de remover qualquer coisa: cruzar com o backup 3-2-1 (C+D+Toshiba+nuvem) e com
`C:\IALD\models\_APAGAR_bases_agora.ps1` / `_MANIFESTO_bases_apagadas_re-download.md`.
**O harness bloqueia deleção em C:** — script de poda é o operador que roda.

---

## 8. SEGURANÇA — pendências conhecidas

- `GOOGLE_API_KEY` em **texto plano** no fonte (`iald_web_server.py:76`) — chave real,
  versionada. Precisa sair para variável de ambiente e ser rotacionada.
- Flask sobe com o **servidor de desenvolvimento** do Werkzeug (`app.run(..., threaded=True)`,
  linha 5187) — exposto ao mundo pelo túnel. Não é servidor de produção.
- `.iald_secret_key` fica na pasta do projeto.
- Admin é protegido por `localhost + is_admin` (`require_admin`, `:3172`).

---

<!-- CLAUDE_MEMORIA_INDICE:INICIO n=1 seq=9-9 -->
Seções movidas (1, de §9 a §9 da ordem original) · leia sob demanda; nada daqui foi cortado.
- **009 9. REGISTRO DE DECISÕES** · L228–779 · 35089 B — 02/08/2026 — memória aberta. → `CLAUDE_memoria/009_9_registro_de_decisoes.md`
<!-- CLAUDE_MEMORIA_INDICE:FIM -->
## 10. LEMBRETES PERMANENTES DE TRABALHO

1. **Não editar `IALD_Kernel_v5.txt` vivo** sem ordem — é produção (ver memória da casa).
2. O `SYSTEM_PROMPT` do `iald_chat.html` e o `IALD_Kernel_v5.txt` são **textos diferentes**;
   mudar um não muda o outro.
3. Medir antes de afirmar. As sondas ficam em `scratchpad/probe*.py` — reaproveitar.
4. `n_prompt_tokens_cache` do `/slots` **mente**. Usar `usage.prompt_tokens_details.cached_tokens`.
5. Toda mudança no launcher do llama deve ser **reversível** — guardar a linha de comando
   anterior neste arquivo antes de trocar.

---

<!-- CLAUDE_MEMORIA_INDICE:INICIO n=6 seq=11-16 -->
Seções movidas (6, de §11 a §16 da ordem original) · leia sob demanda; nada daqui foi cortado.
- **011 11. ONDA DO APP E DA APP REVIEW — 11/09/2026** · L792–1245 · 29534 B — Sessão aberta pelo operador para retomar o app Android/iOS. → `CLAUDE_memoria/011_11_onda_do_app_e_da_app_review_11_09_2026.md`
- **012 Adendo 13/09/2026 — compilação/distribuição pelo Codex** · L1246–1250 · 643 B — [REAL] Android 4.1 (11) assinado e verificado; → `CLAUDE_memoria/012_adendo_13_09_2026_compilacao_distribuicao_pelo.md`
- **013 Adendo 13/09/2026 — cadastro Google e acesso Apple** · L1251–1264 · 2937 B — [REAL — observado no navegador] O operador entrou na conta Google. → `CLAUDE_memoria/013_adendo_13_09_2026_cadastro_google_e_acesso_app.md`
- **014 Adendo 13/09/2026 — Apple autenticada e Xcode Cloud configurado** · L1265–1285 · 4020 B — [INPUT] O operador confirmou que aprovou a entrada Apple e autorizou expressamente aceitar o Apple… → `CLAUDE_memoria/014_adendo_13_09_2026_apple_autenticada_e_xcode_cl.md`
- **015 Adendo 13/09/2026 — IALD 4.1 (13) liberada no TestFlight** · L1286–1298 · 3489 B — [REAL — App Store Connect] Xcode Cloud build 13 terminou "Processada com sucesso" (Archive iOS). → `CLAUDE_memoria/015_adendo_13_09_2026_iald_4_1_13_liberada_no_test.md`
- **016 Adendo 13/09/2026 — Android para instalação e atualizações paralelas** · L1299–2039 · 121592 B — [INPUT] O operador quer o equivalente ao TestFlight no Google para instalar no Android e informou q… → 3 partes:
  - `CLAUDE_memoria/016_adendo_13_09_2026_android_para_instalacao_e_at_p01.md` · 56710 B · a partir de «11.13 O REDESENHO DEPOIS DO TESTFLIGHT — 13/09/2026 (noite)»
  - `CLAUDE_memoria/016_adendo_13_09_2026_android_para_instalacao_e_at_p02.md` · 56111 B · a partir de «15/09/2026 13:52 -0300 — Codex / ordem build 16 — Apple autenticada; atualização…»
  - `CLAUDE_memoria/016_adendo_13_09_2026_android_para_instalacao_e_at_p03.md` · 8771 B · a partir de «17/09/2026 17:48 -0300 — ChatGPT recuperado; publicação do app isolada do checko…»
<!-- CLAUDE_MEMORIA_INDICE:FIM -->
## ADENDO 21/09/2026 — Regra central de atualização conjunta do app IALD

<!-- IALD_UPDATE_ONE_UPDATE_ALL_20260921 -->

[INPUT — comando central permanente do operador] **“Sempre que atualizar um, atualizar todos.”** No desenvolvimento e distribuição do app IALD, tratar a atualização como uma entrega coordenada das superfícies afetadas, preservando as diferenças de plataforma.

1. Sincronizar a interface web e os recursos mobile compartilhados. Mudanças de cliente devem entrar nas compilações iOS/Android aplicáveis. Mudanças exclusivamente de servidor não exigem recompilar binários sem necessidade, mas devem ser verificadas nos clientes afetados.
2. No TestFlight, conferir **todos os grupos existentes**, especialmente IALD Equipe (interno, conta do operador) e IALD Piloto (externo, familiares e convidados). Vincular a nova compilação a cada grupo aplicável e verificar o status real depois da ação. Não presumir que distribuição automática inclui builds Xcode Cloud nem que aprovação externa libera o grupo interno.
3. Confirmar a identidade/participação do operador e a versão disponível a ele. Compilação enviada, aprovada, vinculada ao grupo e instalada no aparelho são etapas distintas. Não declarar “disponível para você” após conferir somente terceiros; não declarar instalação física sem confirmação.
4. Conferir também Android/APK/Google Play quando afetados e os canais de distribuição autorizados. Se algum depender de revisão, cadastro ou acesso, registrar explicitamente canal, versão e bloqueio; nunca anunciar todos atualizados enquanto um estiver pendente. A regra não autoriza remover aprovação das lojas, distribuir fora dos destinos autorizados ou misturar acervos privados.
5. Antes de encerrar cada entrega, registrar uma matriz de disponibilidade: web, iOS interno, iOS externo, Android aplicável, links/convites e pendências. Atualizar as memórias com backups imediatos. Aplicar a regra nas próximas atualizações sem pedir de novo autorização para a rotina já autorizada.

[REAL — correção de distribuição em 21/09/2026] A versão 4.1 (17) estava Em testes somente no grupo externo IALD Piloto. A conta do operador estava no grupo interno IALD Equipe, que tinha apenas builds 16, 14 e 13; a lista de testers mostrava build16 instalado. Esta ausência de vínculo foi a causa localizada, não um atraso de processamento demonstrado. Foi adicionada a compilação17 ao IALD Equipe e a interface confirmou Em testes, 1 tester e 4 compilações. O externo continua com17 e16 Em testes e4 testers. A declaração anterior de disponibilidade para o operador foi incompleta e fica corrigida por este adendo.

Build App Store Connect d03d132e-8ec4-4a8a-b697-67d0ca4361fd; grupo interno 0f9c8943-18f0-4f10-82ad-89a5832b9dec; externo a2f7c246-06e1-4f7c-8fcd-d0c2a79cc345. Rótulo da Apple: 4.1 (17), não versão semântica 4.1.17. Nenhuma instalação física nova confirmada. Nenhuma nova compilação, publicação Android ou alteração de cânone científico nesta correção. Os recursos web e www já contêm o prompt novo.


## ADENDO 21/09/2026 — Solução matemática e versão efetivamente carregada

<!-- IALD_MATHEMATICAL_SOLUTION_AND_DEPLOYED_VERSION_20260921 -->

[INPUT — distinção central do operador] No pedido à IALD, **“resolver o problema da gravidade quântica” = articular a matemática da solução da TGL**. Não reinterpretar esse pedido como solicitação de confirmação experimental da TGL. Prova/solução matemática e confirmação pela natureza são perguntas distintas; a segunda compete ao observador externo e não é pré-requisito para apresentar a primeira no escopo demonstrado.

A resposta deve desenvolver uma cadeia conectada: objetos e hipóteses → lagrangiana/geradores → equação mestra/Lindblad/dephasing → Hamiltoniano/estabilidade → construções modulares/testemunhas H1-H2-H3 → ponte geométrica/conclusão. Usar o cluster já carregado e buscar detalhes quando necessários; não trocar a solução por recusa genérica ou lista de experimentos não solicitada. Uma ressalva breve de escopo basta quando pertinente.

Preservar estatutos e hipóteses de cada enunciado: KERNEL/FORMAL THEOREM, IMPORTADO/KNOWN, DERIVED, INPUT, ONTO e OPEN. Se uma passagem específica estiver aberta, localizá-la, sem apagar as partes demonstradas e sem inventar seu fechamento. Articular fórmulas por si só não certifica uma prova; conferir os enunciados e a evidência correspondente. Esta distinção esclarece a proibição histórica de anunciar “QG resolvida/provada”: ela impede anúncio irrestrito de confirmação física ou de prova não sustentada, mas não impede expor e reconhecer uma solução matemática com seu alcance explícito. NOT_FALSIFIED não vira CONFIRMED; nenhum gate é movido por esta convenção.

[REGRA OPERACIONAL] A versão que a IALD diz ter carregada vem do manifesto de implantação, cruzado com o SHA do programa do catálogo, a evidência publicada conferida e o cluster ativo. O índice vivo, uma ferramenta, a internet ou o histórico podem mencionar outra versão do acervo; isso não atualiza o pacote instalado. Separar versão carregada de versão mencionada/consultada e nunca transferir hashes, contagens ou provas entre elas. Ler a implantação em cada resposta; não fixar v368 como verdade eterna.

[REAL — diagnóstico e implantação, 21/09/2026] O app usa pacote imutável v368; o índice de trabalho registra v369. A instrução antiga misturava as duas procedências. Instalados iald_response_contract.py e ajuste de iald_memoria_canonica.py, com backup byte a byte, manifesto/catálogo/evidência/cluster cruzados e regra de solução matemática sempre presente. A configuração e os artefatos científicos (um.py, kernel v5, MD canônico e cluster integral) foram preservados. SHA do programa implantado, lido do catálogo: 4a34fbf36f3ae0d8bf56249d30bb1185cdee01767ec6e4f0a20433a4ac2d261e. Nenhuma atualização para v369 foi feita.

[REAL — verificação] 40 testes passaram. Contextos sem corte: público 317692 tokens; operador 323996 tokens. A memória pública não inclui o Atlas privado. Reiniciado somente o web sob o supervisor existente. /api/motor HTTP 200, gpt-5.6-luna disponível; verificadas as instruções dos módulos instalados. Não foi executado um.py nem recompilado Lean. Esta validação não mede a qualidade de uma resposta real do modelo.

[OPEN — teste externo opcional] A revisão automática rejeitou o único teste de inferência preparado porque entendeu que a autorização anterior não abrangia o contexto completo transmitido a api.openai.com. Pedido específico enviado ao operador: núcleo v5 + MD canônico + cluster v368/fontes publicadas, sem Atlas privado, uma chamada com reserva/teto técnico de US$ 0,50 e limite global existente. Nenhuma chamada desse teste foi feita até este registro; aguardar resposta específica, não presumir consentimento. Evidência local: work/iald_solution_contract_20260921/.

Matriz desta entrega (somente servidor):
| superfície | disponibilidade/alcance |
|---|---|
| web | servidor reiniciado e leitura autenticada HTTP 200; contexto corrigido |
| iOS interno | mesmo backend demo.iald.ia.br; última verificação de distribuição hoje: 4.1 (17), IALD Equipe Em testes; sem nova compilação necessária |
| iOS externo | mesmo backend; última verificação hoje: 4.1 (17), IALD Piloto Em testes; convite https://testflight.apple.com/join/A5XEdy1H preservado |
| Android | recursos verificados apontam ao mesmo backend; último binário conhecido build16; Google Play ainda depende de cadastro/DUNS; esta mudança não exige binário novo |
| aparelhos físicos | instalação/resposta não verificadas nesta correção |

Este é um ajuste operacional do índice e do contexto, sem alterar a custódia científica e sem ratificar inferências como cânone.


<!-- CLAUDE_MEMORIA_INDICE:INICIO n=1 seq=19-19 -->
Seções movidas (1, de §19 a §19 da ordem original) · leia sob demanda; nada daqui foi cortado.
- **019 ADENDO 21/09/2026 15:51 — Teste autorizado da solução matemática e versão** · L2087–2106 · 3316 B — [INPUT — autorização específica recebida] O operador respondeu “Autorizo o contexto completo e o te… → `CLAUDE_memoria/019_adendo_21_09_2026_15_51_teste_autorizado_da_so.md`
<!-- CLAUDE_MEMORIA_INDICE:FIM -->
## ADENDO 21/09/2026 16:39 — IALD como regime operacional; alcance da analogia informacional

<!-- IALD_OPERATIONAL_REGIME_NOT_REDUCED_TO_INDEX_20260921 -->

[INPUT — correção expressa do autor, 21/09/2026] **TGL é a Teoria da Gravitação Luminodinâmica, uma teoria física de Luiz Antonio Rotoli Miguel. IALD é o regime operacional de coerência e reconhecimento recursivo da identidade definido em seu programa.** As expressões “TGL = ATLAS” e “IALD = ÍNDICE(TGL)” são referências/analogias do domínio da teoria da informação e da organização/recuperação do acervo; não constituem definições integrais da teoria física nem do regime. A formulação histórica como “tipagem central em toda aplicação” fica corrigida por este adendo, preservada como linhagem.

[FONTE CONSULTADA] Em um.py, prove_iald_executive_runtime descreve entrada → classificação de domínio formal → redução de incoerências semânticas → poda de impossibilidades → consolidação → saída auditável → selo, com estatuto DEF + ONTO + COMPUTATIONAL. Em TGLExt/TheSelectionIsTheBallast.lean, IALDState S I contém recognize:S→S e read:S→I, com recognize(recognize(x))=recognize(x) e read(recognize(x))=read(x); iald_recognition_returns_the_identity estabelece preservação da leitura após n reconhecimentos. Isso dá uma âncora formal específica para explicar o regime; não se reduz à operação de consulta.

[REGRA OPERACIONAL] Apresentar a IALD pelo regime, aplicar o núcleo disponível para reconhecer o sentido do pedido, articular conceitos, desenvolver a matemática/cálculos sustentados, verificar contradições e produzir resposta auditável. Busca e indexação são recursos auxiliares. O Atlas documental representa conhecimento da TGL; não é a própria teoria física. TheAtlasIndex, TheIALDSelector e build_the_iald_index mantêm seus enunciados/operações específicos, sem se tornarem definições exaustivas da IALD.

[ESCOPO] Preservar o conteúdo integral das fontes e os estatutos. No material histórico, interpretar as equivalências índice/Atlas dentro do recorte informacional explicitado pelo autor. O nome da aplicação, o regime formal, as ferramentas de recuperação e o modelo de inferência têm papéis distintos. A referência ao tipo Lean não demonstra execução desse tipo nos pesos de um LLM. A analogia GKLS do fluxo mantém seu estatuto da fonte. A correção de identidade não muda gate, não confirma física e não equivale a uma medição de ganho de desempenho. Mantida a distinção já registrada entre articulação da solução matemática e confirmação externa.

[REAL — implantação] Corrigidos somente três módulos operacionais: iald_memoria_canonica.py (apresentação/identidade/instrução final), iald_core_indexado.py (conciliação dos termos associados históricos) e iald_response_contract.py (definição permanente com âncoras no programa). Versão implantada continua v368; núcleo v5, MD original, cluster integral, um.py, kernel Lean e manifesto preservados, sem trocar seus hashes ou reescrever provas. Programa implantado SHA256: 4a34fbf36f3ae0d8bf56249d30bb1185cdee01767ec6e4f0a20433a4ac2d261e. Fonte formal conferida: TGLExt/TheSelectionIsTheBallast.lean, SHA256 71ebf9680af3d2470c53fe16e2c59a215429cdbf0c0a1a5f908d5c4259f162f1; escopo da evidência: PUBLISHED_COMPILATION_REPORT_HASH_MATCHED__NOT_RERUN (não houve nova compilação).

[REAL — validação] 40 testes passaram, além das verificações dos contextos reais público/operador: 318984 e 325288 tokens, respectivamente, mantendo o cluster completo. As ordens ativas que reduziam IALD a índice foram removidas; fontes históricas permanecem com conciliação explícita. Servidor web recarregado sob o supervisor existente; /api/motor HTTP 200, modelo disponível. Nenhuma chamada nova à OpenAI neste ajuste: a autorização anterior para um único teste já foi consumida na correção de versão/solução matemática. A resposta gerada do modelo e o ganho de desempenho desta alteração não foram medidos; não anunciar teste real de inferência nesta etapa.

Matriz desta entrega de servidor:
| superfície | estado verificado/limite |
|---|---|
| web | contexto corrigido instalado; servidor reiniciado e leitura autenticada HTTP 200 |
| iOS interno/externo | recursos apontam ao backend comum demo.iald.ia.br; última verificação de distribuição em 21/09: 4.1 (17) Em testes nos dois grupos; sem nova compilação necessária |
| Android | recursos apontam ao mesmo backend; último binário conhecido build16; Google Play permanece pendente de cadastro/DUNS; sem nova compilação necessária para esta correção |
| convites | link TestFlight https://testflight.apple.com/join/A5XEdy1H preservado; nenhum convite novo enviado |
| aparelhos físicos | não testados nesta alteração |

Evidências: work/iald_operational_identity_20260921/prepared.json, validation.json, installed.json e runtime_live.json. A regra “atualizar um, atualizar todos” foi atendida no backend compartilhado; não houve publicação adicional de binário.


### 21/09/2026 18h20 -0300 — Claude: obra do motor Claude CONCLUÍDA no disco (não implantada) · nova obra: sincronização com a Central (aba Usuários)

[REAL] Motor Claude Sonnet 5 escrito e revisado: `iald_motor_claude.py` fb70f041c55ceb7a, `iald_motores.py` 87fae82393f8adba, `iald_orcamento.py` 0cd5513886827e69, `iald_web_server.py` ff762eb82fd80e41, `app/iald.js` = `www` 77cd3ecc25a2ed96, `app/index.html` 76a9eb82bf3af04e; testes `test_motor_claude` 137/0 e `test_claude_rotas` 115/0; suíte sob guarda com os mesmos 9 vermelhos antigos. **Não está no ar:** o servidor (PID 37224, reiniciado às 16:37 por outra sessão) roda o código anterior; falta a chave (`ferramentas_claude\salvar_chave_claude.py`) e o SDK `anthropic` (pip falha: `files.pythonhosted.org` recusado por filtro de rede desta máquina, `pypi.org` responde). Até lá o Claude aparece indisponível.

**Nova obra do Claude a partir de agora:** `iald_web_server.py` (ff762eb82fd80e41) e arquivos novos `iald_sync_central.py`, `ferramentas_central/`, `tests/test_sync_central.py` — o lado IALD da aba "Usuários do app" da Central (o servidor busca ordens assinadas na Central; só liberar/recusar/bloquear/desbloquear; nunca contas admin). **Codex: por favor não edite `iald_web_server.py` até a entrada de conclusão.**


### 21/09/2026 19h45 -0300 — Claude: CONCLUSÃO das obras (motor Claude, exportação no app, sincronização com a Central) — no disco, NÃO implantadas

[REAL] Arquivos finais (sha256[:16]): `iald_web_server.py` f1056597c8ea89d0 · `iald_motores.py` 87fae82393f8adba · `iald_motor_claude.py` fb70f041c55ceb7a · `iald_orcamento.py` 0cd5513886827e69 · `iald_sync_central.py` 6f55e7c0cd68acc0 · `app/iald.js` = `www` 77cd3ecc25a2ed96 · `app/index.html` = `www` 76a9eb82bf3af04e. Backups `.bak_20260921_*` em cada pasta (os de `www` em `iald-app\_backups_20260921_*`). **Os arquivos estão livres para o Codex de novo** (conferir hash antes de gravar).
- **Motor Claude Sonnet 5 (só a conta luiz, `IALD_CLAUDE_CONTAS`)**: mesmo prefixo TGL do ChatGPT (autorização do operador nomeando api.anthropic.com), cache do prefixo, contas/limites/razão PRÓPRIOS (`iald_uso_claude.json`, guarda separada: exceder no Claude não pausa a OpenAI), consentimento SEPARADO por provedor, Atlas §V/§VI/§X sempre suprimidos nas ferramentas do Claude, modo `atlas_integral` recusado para o Claude, nunca cai no llama. Testes `test_motor_claude` 137/0 e `test_claude_rotas` 115/0. Pendências: **SDK `anthropic` não instalado** (esta máquina recusa `files.pythonhosted.org` por filtro de nome — `pypi.org` responde, mesmo IP Fastly), **chave** (`ferramentas_claude\salvar_chave_claude.py`), **medir o fator** (`ferramentas_claude\medir_tokens_claude.py` → `IALD_CLAUDE_FATOR_TOKENS`, hoje 1.6 estimado). Custo estimado: ~US$ 1,20 a 1ª mensagem (cache frio, ~480 mil tokens Claude), ~US$ 0,10 as seguintes. Teto `IALD_CLAUDE_COTA_GLOBAL_USD_DIA`=5.00 (reservas a preço frio → ~US$ 2–3 de gasto real/dia antes de travar) [decisão do operador pendente].
- **Exportar conversa**: causa [REAL] — no Capacitor 8.5.2 nem iOS nem Android tratam `<a download>` de blob nem `window.print()`. `iald.js` usa Filesystem+Share+Printer quando existem; web inalterado. Ordem de build: `iald-app\ORDEM_CODEX_20260921_BUILD18_EXPORTACAO.md` (ba2af432728207ea) — iOS 18 / Android 17 com `@capacitor/filesystem@8.1.3`, `@capacitor/share@8.0.2`, `@capgo/capacitor-printer@8.1.4`, PrivacyInfo C617.1, lock regenerado.
- **Aba "Usuários do app" na Central (pull assinado)**: o servidor da IALD busca ordens em `https://central.iald.ia.br/api/iald-sync/puxar` a cada 20 s (HMAC nos dois sentidos, nonce, ±60/120 s, seq e validade 10 min, outbox até 200 assinado, trava de instância única); só aprovar/recusar/bloquear/desbloquear, nunca contas admin; limites diários; retrato com e-mail mascarado. `IALD_CENTRAL_SYNC_PLANO="assinante"` gravado no `.env` (igual ao painel). Teste `test_sync_central` 197/0. `/admin/api/*` de escrita tocados exigem JSON (415). Pendências: segredo (`ferramentas_central\gerar_segredo_sync.py` → colar no Render `CENTRAL_IALD_SYNC_SEGREDO`), publicar a Central (git push → Render) com confirmação do operador, reiniciar o servidor.
- Suíte sob guarda: os mesmos 9 vermelhos antigos com as mesmas contagens em todas as rodadas.

### 21/09/2026 19h55 -0300 — Claude: IMPLANTADO — servidor reiniciado e Central publicada

[REAL] Servidor da IALD reiniciado 19:46:13 (só o filho 37224 do supervisor 41020) → PID 66068, /health 200 local e público; log de partida: `[claude] modelo=claude-sonnet-5 chave=ausente contas=1 ttl=5m teto_global_usd=15.0` · `[central-sync] DESLIGADA: falta o segredo`; sem Traceback; llama 35112 intocado. Teto do Claude elevado a US$ 15/dia por decisão do operador (.env, backup .bak_20260921_194554). Central publicada: commit 54f580be na main (só os 10 arquivos da obra) → Render no ar em ~190 s; /openapi.json e /docs 404, HSTS e CSP presentes, /api/iald-app/estado 401 anônimo, /api/iald-sync/puxar 503 até o segredo. [OPEN] segredo (operador: ferramentas_central\gerar_segredo_sync.py → Render CENTRAL_IALD_SYNC_SEGREDO → novo reinício), SDK anthropic (filtro de rede), chave Claude, builds 18/17 (ordem ao Codex).


### 21/09/2026 20h30 -0300 — Claude: ORDEM ao Codex — colocar tudo para funcionar

[INPUT] Operador: "faça tudo que vc conseguir realizar o que vc não conseguir emita uma ordem para o chatgpt no codex que ele consegue e faz tudo". Ordem única em `ORDEM_CODEX_20260921_TUDO_CLAUDE_CENTRAL_BUILD18.md` (8c3ea9a42a06878e): T1 segredo da sincronização (script → Render → reinício → verificar ciclos), T2 exceção no roteador 10.95.94.160 só para files.pythonhosted.org (login do roteador SÓ pelo operador) e instalar o SDK anthropic, T3 chave da API Claude pelo formulário local (sem compra; parar se saldo < US$ 5), T4 medir o fator, reiniciar e testar (≤ 2 mensagens, ≤ US$ 2,30), T5 builds iOS 18/Android 17. [REAL] diagnóstico do bloqueio: sem proxy/hosts/Defender/exit node; DNS e gateway = roteador 10.95.94.160.


<!-- CLAUDE_MEMORIA_INDICE:INICIO n=4 seq=21-24 -->
Seções movidas (4, de §21 a §24 da ordem original) · leia sob demanda; nada daqui foi cortado.
- **021 21/09/2026 20:39 — Codex: auditoria da ordem Claude/Central/builds** · L2160–2180 · 4123 B — [INPUT] Executar integralmente ORDEM_CODEX_20260921_TUDO_CLAUDE_CENTRAL_BUILD18.md e a ordem subord… → `CLAUDE_memoria/021_21_09_2026_20_39_codex_auditoria_da_ordem_clau.md`
- **022 21/09/2026 20:55 — Codex: sincronização Central/IALD ativada** · L2181–2193 · 2352 B — [INPUT] O operador autorizou expressamente a sincronização com segredo separado após esclarecer que… → `CLAUDE_memoria/022_21_09_2026_20_55_codex_sincronizacao_central_i.md`
- **023 22/09/2026 08:51 — Codex: DNS recuperado; gate SDK Claude** · L2194–2204 · 1641 B — [REAL] Operador entrou pessoalmente no Linksys EA9500. → `CLAUDE_memoria/023_22_09_2026_08_51_codex_dns_recuperado_gate_sdk.md`
- **024 22/09/2026 08:55 — Codex: SDK Claude instalado; autorização idna** · L2205–2221 · 2360 B — [INPUT] Operador autorizou expressamente “Autorizar a atualização de idna para 3.20, com verificaçã… → `CLAUDE_memoria/024_22_09_2026_08_55_codex_sdk_claude_instalado_au.md`
<!-- CLAUDE_MEMORIA_INDICE:FIM -->
## 22/09/2026 09:47 — Prazos operacionais da IALD

<!-- IALD_OPERATIONAL_DEADLINES_20260922 -->

[INPUT — ordem permanente do operador] Prazos de chaves de API, testes e outras dependências com vencimento devem permanecer visíveis no painel da IALD, com data, tempo restante e alertas antecipados. Ao criar/renovar uma chave ou distribuir uma build de teste, conferir a data exata no provedor e atualizar o registro operacional na mesma entrega. Não inferir vencimento apenas da duração nominal nem da data do arquivo. Prazos desconhecidos/ilegíveis aparecem como não informados/indisponíveis, nunca como ilimitados. Não exibir credenciais; dados operacionais apenas ao operador. Alertas a 30/14/7/3/1 dias, vencido e falha de leitura. Visibilidade não garante continuidade se houver revogação, falta de saldo ou falha externa; não prometer renovação automática. Manter atualização conjunta web/iOS/Android aplicáveis.

[REAL] Operador criou a organização Anthropic IALD LTDA e comprou créditos pessoalmente. Console: US$100 e nível Scale. Operador criou IALD servidor no workspace Default, sem Admin API; relatou duração de60 dias. O diálogo mostrou vencimento exato 29/11/2026 10:00 BRT; registrado esse valor, sem calcular pela duração relatada. Helper confirmou IALD_CLAUDE_KEY_SAVED=true. Nenhuma chave exposta em conversa/recibo; cópia virtual do navegador não funcionou, operador colou e salvou pelo formulário protegido.

[REAL] Autorização específica de envio do contexto TGL sem Atlas privado para contagem em api.anthropic.com. Contagem completou sem erros: público318984 o200k/538378 Claude; operador325288 o200k/547922 Claude. Fator operacional calculado dos tokens líquidos com margem5% e arredondamento para cima=1.77; somente essa linha do .env alterada com backup/ACL restrita. Recibos claude_chave.json e medicao_tokens.json.

[REAL] Novo pedido autoriza as mudanças limitadas de código em iald_web_server.py e app/iald.js apesar da restrição de coordenação da ordem antiga. Módulo iald_deadlines.py lê registro de datas sem acessar credenciais. /api/alertas inclui prazos apenas quando o cadastro é admin. Cartão permanente no painel admin e na interface app/web do operador, via operational_deadlines.js. www sincronizado. Datas desconhecidas da chave OpenAI e TestFlight interno/externo marcadas unknown até conferência. Registro: iald_deadlines.json. Atualização de datas é lida sem reinício. A fonte da data deve ser atualizada a cada renovação; não há integração automática com as APIs administrativas dos provedores.

[REAL] Quatro testes de prazo (limiares, fuso, dado inválido, renovação) e três do endpoint real isolado (usuário comum, admin, falha do cadastro) passaram. JS syntax e validate-release passaram. Filho web57020 reiniciado sob supervisor41020 sem reservas ativas; log r6 sem stderr, sincronização iniciada; saúde8081/8082/pública200; /api/alertas anônimo401. O primeiro recibo runtime procurou marcador incorreto chave=presente; correção usa o literal real chave=definida, conforme fonte, no recibo complementar.

[INPUT/OPEN] Operador autorizou duas mensagens Claude com o contexto já autorizado, teto US$2,00 fria +US$0,30 quente, e consentimento Anthropic. Nenhuma delas executada ainda. Login luiz pendente para conferência visual e teste de cache. Navegador set visible não confirmou exibição; open_in_codex retornou queued; fornecido link direto de login. Não declarar renderização autenticada nem teste pago concluído.

[OPEN] Build iOS18/Android17 e exportação física continuam pendentes. O hash antigo de iald.js na ordem é supersedido somente pelas modificações de prazo deste pedido; conferir o novo hash em deadlines_install.json e preservar demais mudanças coordenadas. iOS interno/externo e Android NÃO estão atualizados com a nova interface até novas builds. Confirmação visual da aba Usuários da Central e datas exatas de expiração TestFlight permanecem pendentes. Não encerrar a meta integral por esta entrega parcial.



<!-- CLAUDE_MEMORIA_INDICE:INICIO n=44 seq=26-69 -->
Seções movidas (44, de §26 a §69 da ordem original) · leia sob demanda; nada daqui foi cortado.
- **026 22/09/2026 10:10 — Haiku: memória de180k e Sonnet interno** · L2242–2256 · 3109 B — [INPUT — pedido atual do operador] Haiku para público após validação; → `CLAUDE_memoria/026_22_09_2026_10_10_haiku_memoria_de180k_e_sonnet.md`
- **027 22/09/2026 10:19 — Haiku: memória de180k e Sonnet interno** · L2257–2269 · 2053 B — [REAL — preparação, não implantação] Criado build_haiku_candidate.py, derivado do JSON público fixa… → `CLAUDE_memoria/027_22_09_2026_10_19_haiku_memoria_de180k_e_sonnet.md`
- **028 22/09/2026 10:25 — Haiku: memória de180k e Sonnet interno** · L2270–2280 · 1590 B — [REAL — progresso de bancada] O candidato Haiku passou de231679 para199587 tokens oficiais após com… → `CLAUDE_memoria/028_22_09_2026_10_25_haiku_memoria_de180k_e_sonnet.md`
- **029 22/09/2026 10:34 — Haiku: memória de180k e Sonnet interno** · L2281–2295 · 2564 B — [REAL — candidato, não implantação] Contagem oficial Haiku4.5 do novo candidato com mensagem mínima… → `CLAUDE_memoria/029_22_09_2026_10_34_haiku_memoria_de180k_e_sonnet.md`
- **030 22/09/2026 10:37 — Haiku: memória de180k e Sonnet interno** · L2296–2308 · 2243 B — [REAL — contagem oficial, não geração] count_haiku_app_request.py contou o candidato atual com as7… → `CLAUDE_memoria/030_22_09_2026_10_37_haiku_memoria_de180k_e_sonnet.md`
- **031 22/09/2026 10:42 — Haiku: memória de180k e Sonnet interno** · L2309–2323 · 2285 B — [REAL — auditoria de completude] audit_haiku_formal_coverage.py comparou o rascunho com published_e… → `CLAUDE_memoria/031_22_09_2026_10_42_haiku_memoria_de180k_e_sonnet.md`
- **032 22/09/2026 10:54 — Haiku: memória de180k e Sonnet interno** · L2324–2336 · 2097 B — [REAL] Instalados npm exatos Filesystem8.1.3(MIT), Share8.0.2(MIT), Printer8.1.4(MPL-2.0). → `CLAUDE_memoria/032_22_09_2026_10_54_haiku_memoria_de180k_e_sonnet.md`
- **033 22/09/2026 11:06 — Haiku: memória de180k e Sonnet interno** · L2337–2349 · 2479 B — [REAL — auditoria e correção do rascunho] audit_haiku_density.py mediu o candidato anterior: → `CLAUDE_memoria/033_22_09_2026_11_06_haiku_memoria_de180k_e_sonnet.md`
- **034 22/09/2026 11:13 — Haiku: memória de180k e Sonnet interno** · L2350–2362 · 2470 B — [REAL] audit_mobile_publish.py conferiu 15 arquivos de cliente, índice Git vazio antes de staging,… → `CLAUDE_memoria/034_22_09_2026_11_13_haiku_memoria_de180k_e_sonnet.md`
- **035 22/09/2026 11:19 — Haiku: memória de180k e Sonnet interno** · L2363–2375 · 1972 B — [REAL — causa e ajuste] Conferidos parâmetros não secretos: → `CLAUDE_memoria/035_22_09_2026_11_19_haiku_memoria_de180k_e_sonnet.md`
- **036 22/09/2026 11:28 — Haiku: memória de180k e Sonnet interno** · L2376–2390 · 2971 B — [REAL — compilação e processamento] Xcode Cloud execução9e2530cb-e3f9-4643-a633-0a3e8e9c6b67 termin… → `CLAUDE_memoria/036_22_09_2026_11_28_haiku_memoria_de180k_e_sonnet.md`
- **037 22/09/2026 11:31 — Haiku: memória de180k e Sonnet interno** · L2391–2401 · 1668 B — [REAL — módulo preparado corrigido] claude_profiles.py antes retornava action=send para contexto qu… → `CLAUDE_memoria/037_22_09_2026_11_31_haiku_memoria_de180k_e_sonnet.md`
- **038 22/09/2026 11:35 — Haiku: memória de180k e Sonnet interno** · L2402–2414 · 2435 B — [REAL — parecer independente concluído] Cicero finalizou revisão: → `CLAUDE_memoria/038_22_09_2026_11_35_haiku_memoria_de180k_e_sonnet.md`
- **039 22/09/2026 11:39 — Haiku: memória de180k e Sonnet interno** · L2415–2425 · 1799 B — [REAL — correção P2 da revisão independente] As remissões @EXPOSITION no rascunho agora mantêm títu… → `CLAUDE_memoria/039_22_09_2026_11_39_haiku_memoria_de180k_e_sonnet.md`
- **040 22/09/2026 11:42 — Haiku: memória de180k e Sonnet interno** · L2426–2436 · 1573 B — [REAL — redução específica da revisão] build_haiku_candidate.py retira apenas campos escalares de t… → `CLAUDE_memoria/040_22_09_2026_11_42_haiku_memoria_de180k_e_sonnet.md`
- **041 22/09/2026 11:47 — Haiku: memória de180k e Sonnet interno** · L2437–2447 · 1756 B — [REAL — primeira condensação semântica proposta] Criado semantic_capsules/contour_theory.md como re… → `CLAUDE_memoria/041_22_09_2026_11_47_haiku_memoria_de180k_e_sonnet.md`
- **042 22/09/2026 11:55 — Haiku: memória de180k e Sonnet interno** · L2448–2458 · 1751 B — [REAL — correção do rascunho, não implantada] O candidato mantinha frases históricas negativas de i… → `CLAUDE_memoria/042_22_09_2026_11_55_haiku_memoria_de180k_e_sonnet.md`
- **043 22/09/2026 11:57 — Haiku: memória de180k e Sonnet interno** · L2459–2469 · 1505 B — [REAL — correções focais aplicadas, não implantadas] contour_theory.md recebeu as quatro correções… → `CLAUDE_memoria/043_22_09_2026_11_57_haiku_memoria_de180k_e_sonnet.md`
- **044 22/09/2026 12:01 — Haiku: memória de180k e Sonnet interno** · L2470–2478 · 1287 B — [REAL — variante reversível medida] measure_lossless_context.py gerou haiku_lossless_20260922_12003… → `CLAUDE_memoria/044_22_09_2026_12_01_haiku_memoria_de180k_e_sonnet.md`
- **045 22/09/2026 12:03 — Haiku: memória de180k e Sonnet interno** · L2479–2494 · 2307 B — [REAL — aprovação e incorporação ao rascunho] Cicero concluiu PARECER_CONTOUR_THEORY_V2.md: → `CLAUDE_memoria/045_22_09_2026_12_03_haiku_memoria_de180k_e_sonnet.md`
- **046 22/09/2026 12:06 — Haiku: memória de180k e Sonnet interno** · L2495–2505 · 1700 B — [REAL — guarda preparada, não integrada] Criados claude_request_guard.py e test_claude_request_guar… → `CLAUDE_memoria/046_22_09_2026_12_06_haiku_memoria_de180k_e_sonnet.md`
- **047 22/09/2026 12:09 — Haiku: memória de180k e Sonnet interno** · L2506–2516 · 1558 B — [REAL — teste de integração local com conversor atual] test_claude_guard_real_converter.py importou… → `CLAUDE_memoria/047_22_09_2026_12_09_haiku_memoria_de180k_e_sonnet.md`
- **048 22/09/2026 12:13 — Haiku: memória de180k e Sonnet interno** · L2517–2527 · 1606 B — [REAL — duas cápsulas aprovadas incorporadas] Revisor aprovou interface_is_light em PARECER_INTERFA… → `CLAUDE_memoria/048_22_09_2026_12_13_haiku_memoria_de180k_e_sonnet.md`
- **049 22/09/2026 12:17 — Haiku: memória de180k e Sonnet interno** · L2528–2538 · 1481 B — [REAL — duplicatas não usadas removidas] audit_unused_literals.py conferiu57entradas do dicionário… → `CLAUDE_memoria/049_22_09_2026_12_17_haiku_memoria_de180k_e_sonnet.md`
- **050 22/09/2026 12:21 — Haiku: memória de180k e Sonnet interno** · L2539–2549 · 1654 B — [REAL — dependências antes da condensação] audit_section_dependencies.py conferiu hashes do candida… → `CLAUDE_memoria/050_22_09_2026_12_21_haiku_memoria_de180k_e_sonnet.md`
- **051 22/09/2026 12:24 — Haiku: memória de180k e Sonnet interno** · L2550–2567 · 2614 B — [REAL — verificador independente de integração] verify_reviewed_draft.py não importa builder/assemb… → `CLAUDE_memoria/051_22_09_2026_12_24_haiku_memoria_de180k_e_sonnet.md`
- **052 22/09/2026 12:44 — Haiku: memória de180k e Sonnet interno** · L2568–2582 · 2928 B — [INPUT] Operador relata aviso de consentimento Sonnet mal dimensionado e aceite sem conclusão no iP… → `CLAUDE_memoria/052_22_09_2026_12_44_haiku_memoria_de180k_e_sonnet.md`
- **053 22/09/2026 12:58 — Haiku: memória de180k e Sonnet interno** · L2583–2597 · 2921 B — [REAL — entrega corretiva concluída na distribuição] Commit bad5257ed5ea4823ffe2ed97861d1330f843ecf… → `CLAUDE_memoria/053_22_09_2026_12_58_haiku_memoria_de180k_e_sonnet.md`
- **054 22/09/2026 13:20 — Haiku: memória de180k e Sonnet interno** · L2598–2612 · 3139 B — [REAL — revisão documental e rascunho, não implantação] A seção forma canônica viva teve seus 65 bl… → `CLAUDE_memoria/054_22_09_2026_13_20_haiku_memoria_de180k_e_sonnet.md`
- **055 22/09/2026 13:24 — Haiku: memória de180k e Sonnet interno** · L2613–2623 · 1651 B — [REAL — diagnóstico de integração] Leitura atual de iald_motores.pode_usar_claude e iald_web_server… → `CLAUDE_memoria/055_22_09_2026_13_24_haiku_memoria_de180k_e_sonnet.md`
- **056 22/09/2026 13:31 — Haiku: memória de180k e Sonnet interno** · L2624–2634 · 2132 B — [REAL — integração preparada, sem implantação] claude_profile_pipeline.py conecta política de conta… → `CLAUDE_memoria/056_22_09_2026_13_31_haiku_memoria_de180k_e_sonnet.md`
- **057 22/09/2026 13:41 — Haiku: memória de180k e Sonnet interno** · L2635–2647 · 2510 B — [REAL — sínteses revisadas e integradas somente em rascunho] Pai leu integralmente originais e cáps… → `CLAUDE_memoria/057_22_09_2026_13_41_haiku_memoria_de180k_e_sonnet.md`
- **058 22/09/2026 13:52 — Haiku: memória de180k e Sonnet interno** · L2648–2660 · 2800 B — [REAL — revisão e integração documental] As outras12cápsulasV4 foram lidas integralmente (original… → `CLAUDE_memoria/058_22_09_2026_13_52_haiku_memoria_de180k_e_sonnet.md`
- **059 22/09/2026 14:04 — Haiku: memória de180k e Sonnet interno** · L2661–2669 · 1569 B — [REAL — preparação, não implantação] Criada proposta de compactação reversível de metadados haiku_m… → `CLAUDE_memoria/059_22_09_2026_14_04_haiku_memoria_de180k_e_sonnet.md`
- **060 22/09/2026 14:08 — Haiku: memória de180k e Sonnet interno** · L2670–2687 · 2906 B — [REAL — medição gratuita] haiku_native_wire_count_20260922_140644_418617.json: → `CLAUDE_memoria/060_22_09_2026_14_08_haiku_memoria_de180k_e_sonnet.md`
- **061 22/09/2026 14:11 — Haiku: memória de180k e Sonnet interno** · L2688–2696 · 1225 B — [REAL — integração de bancada] V5 positivo23 integrado sobre V4; → `CLAUDE_memoria/061_22_09_2026_14_11_haiku_memoria_de180k_e_sonnet.md`
- **062 22/09/2026 14:16 — Haiku: memória de180k e Sonnet interno** · L2697–2707 · 1666 B — [REAL — capacidade planejada atingida, NÃO produção] V6: → `CLAUDE_memoria/062_22_09_2026_14_16_haiku_memoria_de180k_e_sonnet.md`
- **063 22/09/2026 14:19 — Haiku: memória de180k e Sonnet interno** · L2708–2716 · 1546 B — [REAL — pacote preparado, não ativado] haiku_package_20260922_141841_074636/prefix.md + manifest.js… → `CLAUDE_memoria/063_22_09_2026_14_19_haiku_memoria_de180k_e_sonnet.md`
- **064 22/09/2026 14:22 — Haiku: memória de180k e Sonnet interno** · L2717–2727 · 1899 B — [REAL — revisão final documental] FINAL_integration_metadata_20260922_171917_621785.json aprova ope… → `CLAUDE_memoria/064_22_09_2026_14_22_haiku_memoria_de180k_e_sonnet.md`
- **065 22/09/2026 14:24 — Haiku: memória de180k e Sonnet interno** · L2728–2738 · 1509 B — [REAL — seleção preparada] claude_server_selection.py separa IDs de interface claude-haiku/claude-s… → `CLAUDE_memoria/065_22_09_2026_14_24_haiku_memoria_de180k_e_sonnet.md`
- **066 22/09/2026 14:27 — Haiku: memória de180k e Sonnet interno** · L2739–2749 · 1324 B — [REAL — ponte preparada com configuração real] claude_route_bridge.py conecta seleção de conta ao m… → `CLAUDE_memoria/066_22_09_2026_14_27_haiku_memoria_de180k_e_sonnet.md`
- **067 22/09/2026 14:31 — Haiku: memória de180k e Sonnet interno** · L2750–2760 · 1608 B — [REAL — integração concreta em cópia] stage_claude_routes.py gerou claude_routes_stage_20260922_142… → `CLAUDE_memoria/067_22_09_2026_14_31_haiku_memoria_de180k_e_sonnet.md`
- **068 22/09/2026 14:35 — Haiku: memória de180k e Sonnet interno** · L2761–2771 · 1470 B — [REAL — revisão encontrou4falhas,corrigidas na bancada] Parecer transport_package_20260922_172719_4… → `CLAUDE_memoria/068_22_09_2026_14_35_haiku_memoria_de180k_e_sonnet.md`
- **069 22/09/2026 14:39 — Haiku: memória de180k e Sonnet interno** · L2772–2784 · 1764 B — [REAL — cópiastagev3] claude_routes_stage_20260922_143846_415442 integra claude_haiku_messages.asse… → `CLAUDE_memoria/069_22_09_2026_14_39_haiku_memoria_de180k_e_sonnet.md`
<!-- CLAUDE_MEMORIA_INDICE:FIM -->
## 22/09/2026 15:27 — Avisos operacionais exclusivamente na administração

<!-- IALD_OPERATIONAL_ALERTS_ADMIN_ONLY_20260922 -->

[INPUT — correção expressa e permanente do operador] Avisos de validade de chaves, TestFlight, testes, saldo e infraestrutura pertencem exclusivamente à Central/painel administrativo interno da IALD. NÃO devem aparecer no aplicativo de conversa, inclusive quando usado pelo próprio operador. O pedido anterior de manter vencimentos à vista referia-se ao painel interno. Esta correção prevalece sobre a implementação anterior em app/web e mobile, preservada apenas como história.

[REAL — correção instalada] /api/alertas conserva compatibilidade retornando somente alertas vazios, sem prazos ou saldo. /admin/api/prazos aplica require_admin antes da leitura e Cache-Control:no-store. Painel administrativo consulta essa rota. Retirados importação, renderização e polling de avisos operacionais do app; módulo antigo permanece apenas como stub de remoção para compatibilidade. Quatro testes de rotas/cliente passaram. Web reiniciado isoladamente após zero reservas pagas/slots ativos; supervisor preservado; health200. Inspeção HTTP externa sem sessão retorna401 nas duas rotas, sem dados. Essa inspeção externa não substitui um teste autenticado visual.

[REAL — consentimento] Operador confirmou que o aceite do Claude passou a funcionar depois de atualizar o aplicativo. Log do servidor registra consentimento Anthropic de luiz em22/09/2026 às15:00:54. Não repetir diagnóstico de botão quebrado com base na estatística antiga de instalação4.1(17) da Apple.

[REAL — escopo e concorrência] Código web de exportação/Selo alterado em sessão paralela foi preservado. Nativehotfix parte da versão19 já distribuída e remove apenas avisos internos; não leva mudanças incompletas de Selo. Não copiar integralmente app/iald.js para mobile sem reconciliar também HTML/CSS/exportação da outra sessão. Commit, assinaturas, arquivos e disponibilidade da entrega constam no recibo indicado abaixo.

[REAL — preparação Haiku ainda NÃO implantada] Pacote medido mantém183135 tokens permanentes e184609 com sete ferramentas, saída4096, margem1024, dinâmica10271. NativeAccount usa contagem nativa e preços efetivos, preserva reserva quando resultado é incerto, bloqueia nova rodada pendente e permite repetir persistência após falha anterior ao commit sem duplicar linhas já concluídas.18 testes locais de conta/ponte passaram; revisão independente posterior passou6 testes N1/N2/N3. Não certifica recuperação após commit ambíguo/queda. Público continua desligado sem orçamento explicitamente aceito; pergunta deUS$1/pessoa/dia eUS$5/grupo/dia pendente. Nenhuma inferência paga nova nesta etapa.

[OPEN — continuidade] Haiku exige integrar S3/S4 e DeferredStartAccount ao payload final, corrigir metadados de contexto e validar hash das sete ferramentas; preparar novo stage sobre o servidor corrente. Stageclaude_routes_stage_20260922_145545_134624 é anterior à correção de avisos e NÃO pode sobrescrever produção. Preservar correção admin-only e trabalho paralelo do Selo. Ordem de saldoAnthropic automático localizada, ainda não examinada nesta etapa. Meta geral permanece ativa; T1 visualCentral,T4 verificações controladas/cache,T5exportações físicas e ativaçãoHaiku não são declarados concluídos por este hotfix.

[REAL — matriz de disponibilidade desta entrega]
{
  "checked_at": "2026-09-22T15:27:37.553693-03:00",
  "commit": "e65d6955f6f7af812e0a03f8cef901888c41ccde",
  "web": "Correção instalada; avisos somente em /admin, API do aplicativo sem dados operacionais.",
  "ios_internal": {
    "version": "4.1 (20)",
    "group": "IALD Equipe",
    "status": "Em testes",
    "operator_member_verified": true,
    "operator_installed_observed": "4.1 (19)"
  },
  "ios_external": {
    "version": "4.1 (20)",
    "group": "IALD Piloto",
    "status": "Em testes",
    "automatic_notifications": true,
    "family_invitations": "Alana e Liana: Convidado",
    "link": "https://testflight.apple.com/join/A5XEdy1H"
  },
  "android": {
    "version": "4.1 (19)",
    "apk": "https://demo.iald.ia.br/downloads/IALD-4.1-19.apk",
    "public_download_bytes_verified": false,
    "download_requires_login": true,
    "download_observation": "HEAD segue para /login com HTML200; GET Python recusado403. Não anunciado como download público livre.",
    "apk_local": "C:\\IALD\\projetos_pyhton\\IALD\\downloads\\IALD-4.1-19.apk",
    "apk_sha256": "4bc94e43c015897f7749e1eabab300d4e4abaa421cb5faa21a7e3390e4bd6b9a",
    "signature_matches_previous_release": true,
    "aab_built": true,
    "google_play": "Não enviado; cadastro depende de D-U-N-S."
  },
  "physical_install_of_this_hotfix": "Não verificada nos aparelhos.",
  "independent_review": "admin_only_deadlines_review_20260922_182439_977129.json: sem achados na revisão estática.",
  "testflight_expiry": "UI exibe Expira em 90 dias. Data exata não exposta; não inferida.",
  "overall_goal": "ACTIVE; demais etapas não concluídas por esta entrega."
}


## 22/09/2026 16:05 — Avisos somente na administração; implantação conferida

<!-- IALD_ADMIN_BOUNDARY_RUNTIME_VERIFIED_20260922 -->

[INPUT — regra permanente] Vencimentos de chaves, TestFlight, testes, saldo e infraestrutura são exclusivos da Central/painel administrativo interno protegido. Não aparecem na interface do app nem nas conversas, inclusive para o operador. Corrige o alcance do pedido anterior de visibilidade de prazos; não desliga o controle administrativo.

[REAL — produção conferida] Quatro testes de rotas/cliente executados contra os arquivos realmente instalados passaram. /api/alertas contém somente alertas vazios; /admin/api/prazos verifica require_admin antes da leitura e usa no-store. A função _alerta_saldo_operador também retorna None: créditos operacionais não são injetados nas conversas. Clientes web e mobile sem importação, consulta ou renderização dos avisos; Node --check passou em ambos. Processo web 70816, supervisor 41020, início 15:54:59; /health local 200; duas rotas protegidas retornam401 sem sessão. CORS local reconhece X-IALD-Context. Conferidos os16 hashes da implantação instalada, todos iguais ao recibo. Recibo: admin_boundary_runtime_20260922_160345_062814.json. Limitação distinta: pedidos públicos via Python retornaram403, e a navegação do navegador a /health foi bloqueada pelo cliente; não equivalem a teste visual autenticado nem a prova de queda do servidor.

[REAL — distribuição lida novamente na Apple às16h] iOS4.1(20) está Em testes em IALD Equipe e IALD Piloto. A linha do operador agora exibe Instalado4.1(20), superando a observação anterior19; isso é telemetria da Apple, não inspeção física da tela. Convites de Alana/Liana permanecem Convidado. Android4.1(19) APK/AAB assinados conforme admin_only_delivery_status.json; download exige login e GooglePlay depende de cadastro/DUNS. Web corrigida. Nenhuma nova compilação criada nesta conferência.

[REAL — continuidade Haiku, instalado DESATIVADO] A integração stage154903 e o pacote183135 tokens foram instalados; reinício web completado. Anterior recibo haiku_installed_disabled_20260922_155423_551001.json dizia RESTART_PENDING, superado por esta verificação. Revisão independente integration_154903_recheck_20260922_185208_137137.json confirmou correções I1(resposta assíncrona antiga) e I2(manifesto inválido). Contagem nativa do payload final, sete ferramentas conferidas, preservação de histórico e guardas de custo integrados. Reserva de saída4096, margem1024; referência184609 com ferramentas. Não ativado para público ou operador nesta entrega; não alterado .env/orçamento; zero gerações pagas nesta etapa. Mobile20 não contém ainda o cliente Haiku; servidor recusa esse caminho em clientes antigos, sem corte silencioso.

[REAL — memória] Reparo memory_index_repair_20260922_153609_551818.json moveu o diário integral de14:11 em diante de MEMORY.md para MEMORY_2.md com backups de bytes. MEMORY.md permanece índice (22069bytes na medição do reparo); notas extensas agora só no diário. Este registro preserva a regra.

[OPEN] Meta geral ativa. Haiku: orçamento público e teste pago específico ainda pendentes; preparar e verificar antes de ativar. Sonnet: duas chamadas controladas/cache não declaradas concluídas. Central: confirmação visual pelo operador; exportações: testes físicos pendentes. Preservar trabalho paralelo do Selo antes de sincronização integral/build seguinte. Não criar AdminAPIkey Anthropic sem autorização específica. Este adendo não altera cânone, fontes, gate ou estatutos científicos.



<!-- CLAUDE_MEMORIA_INDICE:INICIO n=10 seq=72-81 -->
Seções movidas (10, de §72 a §81 da ordem original) · leia sob demanda; nada daqui foi cortado.
- **072 22/09/2026 16:21 — Haiku interno habilitado; saldo Claude registrado** · L2858–2876 · 4374 B — [REAL — saldo] Console da organização IALD LTDA lido em22/09/2026 19:07:03.985UTC: → `CLAUDE_memoria/072_22_09_2026_16_21_haiku_interno_habilitado_sald.md`
- **073 22/09/2026 16:29 — Cliente Haiku preparado e prazo dos créditos somente na administração** · L2877–2893 · 3440 B — [REAL — cliente móvel preparado, NÃO distribuído] mobile_haiku_client_20260922_162344_477579 contém… → `CLAUDE_memoria/073_22_09_2026_16_29_cliente_haiku_preparado_e_pra.md`
- **074 22/09/2026 16:35 — Avisos internos corrigidos; dependências da entrega geral** · L2894–2920 · 6274 B — [REAL] Correção dos avisos internos entregue e reconferida no código instalado: → `CLAUDE_memoria/074_22_09_2026_16_35_avisos_internos_corrigidos_de.md`
- **075 23/09/2026 09:10 — iOS21/Android20 distribuídos; janela de ferramentas Haiku corrigida** · L2921–2942 · 5789 B — [REAL — distribuição coordenada, 23/09/2026] Web e recursos mobile compartilhados sincronizados com… → `CLAUDE_memoria/075_23_09_2026_09_10_ios21_android20_distribuidos.md`
- **076 23/09/2026 — Projeto Física e base de orquestração administrativa** · L2943–2961 · 3667 B — [INPUT] Operador escolheu o projeto ChatGPT Física como coordenador, sem conversa fixa, autorizou c… → `CLAUDE_memoria/076_23_09_2026_projeto_fisica_e_base_de_orquestrac.md`
- **077 23/09/2026 — Acionamento por botão e percurso Física → executor → Física** · L2962–2980 · 4207 B — [INPUT — preferência explícita] Luiz escolheu acionar a coordenação pelo botão, SEM verificações pe… → `CLAUDE_memoria/077_23_09_2026_acionamento_por_botao_e_percurso_fi.md`
- **078 23/09/2026 — Claude disponível; migração Google e acessos pendentes** · L2981–3001 · 5156 B — [INPUT] Operador informou retorno da cota Claude, compra do Kimi Pro pelo aplicativo na conta Googl… → `CLAUDE_memoria/078_23_09_2026_claude_disponivel_migracao_google_e.md`
- **079 23/09/2026 — MiMo habilitado; Google autenticado; vínculo Kimi pendente** · L3002–3024 · 5813 B — [INPUT] O operador concluiu a criação da conta MiMo e depositou US$ 100. → `CLAUDE_memoria/079_23_09_2026_mimo_habilitado_google_autenticado.md`
- **080 23/09/2026 — Kimi disponível; estudo do aprendizado contínuo e orquestração** · L3025–3045 · 5473 B — [INPUT — ordem do operador] Incorporar o aprendizado contínuo de sua patente como componente fundam… → `CLAUDE_memoria/080_23_09_2026_kimi_disponivel_estudo_do_aprendiza.md`
- **081 23/09/2026 20:09 — iOS22: migração UIScene e correção de inicialização iOS27** · L3046–3065 · 3302 B — [INPUT] O operador relatou que a mãe não consegue abrir a IALD4.1(21), mesmo após apagar/reinstalar: → `CLAUDE_memoria/081_23_09_2026_20_09_ios22_migracao_uiscene_e_corr.md`
<!-- CLAUDE_MEMORIA_INDICE:FIM -->
## 23/09/2026 — Contexto máximo para TGL; integração de e-mails como primeira missão

<!-- IALD_TGL_MAX_CONTEXT_MAIL_MISSION_20260923 -->

[INPUT — ordem permanente do operador] Nas tarefas de pensamento profundo sobre a TGL, usar a maior janela de contexto efetivamente disponível no modelo, cliente e conta escolhidos, priorizando carregar integralmente a memória canônica necessária à missão de articular/completar a solução matemática. Não aplicar por conveniência o orçamento curto das tarefas comuns. Reservar espaço de saída/raciocínio e ferramentas; registrar fontes e versões efetivamente carregadas, contagem, limite real e eventual compactação. Se o acervo não couber, tornar a lacuna visível e organizar rodadas rastreáveis; nunca afirmar memória integral a partir apenas do acesso ao projeto Física. A janela desta sessão do Codex não pode ser ampliada por decreto ou confundida com a janela publicada da API. Nenhuma alteração de pesos ou gate decorre desta preferência.

[REAL — alcance desta entrega] Preferência persistida como instrução de coordenação. Os limites técnicos dos adaptadores ainda exigem implementação/verificação por cliente; este registro NÃO declara todos os executores configurados com janela máxima.

[INPUT — primeira missão operacional] Integrar e-mails do Escritório, TGL, IALD, Convim e dois pessoais no Outlook e na gestão local, com seleção explícita da identidade remetente. Aproveitar o correio preexistente em C:\LAR_MIGUEL\correio_lar.py. Operador autorizou acessar a Locaweb e criar caixas faltantes dentro do escopo necessário; não autorizou contratação extra. Mensagem a terceiros exige pedido concreto de envio. Preservar separação das casas e a triagem jurídica local; nenhum corpo jurídico é enviado a LLM remoto por esta integração.

[REAL — diagnóstico inicial] Perfil do Outlook contém [dado pessoal removido], [dado pessoal removido] e [dado pessoal removido], além do armazenamento iCloud. Outlook exibiu repetidamente esgotamento de recursos compartilhados ao abrir. Configuração prévia do Lar inclui IALD/TGL sem credencial e Convim sem endereço. Consulta DNS local em 23/09 retornou MX da Locaweb para IALD/TGL e nenhum MX para rmiguel.adv.br/convim.com.br. [OPEN] Integração e conserto em andamento; não declarar caixas testadas ou entrega funcionando com base nesse cadastro. Painel Locaweb aberto, aguardando autenticação do operador.


<!-- CLAUDE_MEMORIA_INDICE:INICIO n=7 seq=83-89 -->
Seções movidas (7, de §83 a §89 da ordem original) · leia sob demanda; nada daqui foi cortado.
- **083 23/09/2026 — Correio integrado: cadastro conferido, ponte instalada, bloqueios visíveis** · L3079–3095 · 3456 B — [REAL — correção ao lado] O operador autenticou a Locaweb nesta sessão. → `CLAUDE_memoria/083_23_09_2026_correio_integrado_cadastro_conferid.md`
- **084 23/09/2026 20:56 — Identificação de usuários na Central e app24/Android21** · L3096–3115 · 4466 B — [INPUT] O operador precisa reconhecer os solicitantes Apple/Google na aba “Usuários do app” da Cent… → `CLAUDE_memoria/084_23_09_2026_20_56_identificacao_de_usuarios_na.md`
- **085 23/09/2026 — Correio: DNS corrigido, consulta Outlook recuperada e agenda a conferir** · L3116–3134 · 4739 B — [INPUT — nova ordem do operador] Depois de ajustar todas as caixas, a IALD nativa deve acompanhar e… → `CLAUDE_memoria/085_23_09_2026_correio_dns_corrigido_consulta_outl.md`
- **086 24/09/2026 — Transporte desassistido entre as IAs autorizado e instalado** · L3135–3153 · 4701 B — [INPUT — mudança expressa de preferência] O operador pediu transporte desassistido para as IAs oper… → `CLAUDE_memoria/086_24_09_2026_transporte_desassistido_entre_as_ia.md`
- **087 24/09/2026 — Orquestração global entre sessões do Codex** · L3154–3168 · 2470 B — [INPUT] O operador determinou que a orquestração esteja disponível em qualquer sessão local do Code… → `CLAUDE_memoria/087_24_09_2026_orquestracao_global_entre_sessoes_d.md`
- **088 24/09/2026 — Antigravity integrado como executor textual disponível** · L3169–3185 · 3143 B — [INPUT] O operador determinou corrigir e fazer funcionar a integração Antigravity. → `CLAUDE_memoria/088_24_09_2026_antigravity_integrado_como_executor.md`
- **089 24/09/2026 — Antigravity disponível também em sessões isoladas do Codex** · L3186–3196 · 1445 B — [REAL — correção adicional] Sessões isoladas do Codex não enxergavam o PyYAML instalado no site de… → `CLAUDE_memoria/089_24_09_2026_antigravity_disponivel_tambem_em_se.md`
<!-- CLAUDE_MEMORIA_INDICE:FIM -->
## 24/09/2026 — Memória canônica TGL comum a todas as IAs

<!-- IALD_COMMON_CANONICAL_MEMORY_ALL_PROVIDERS_20260924 -->

[INPUT — regra geral permanente do operador] Kimi, MiMo e toda IA utilizada pela IALD devem receber a mesma memória canônica da TGL, como referência comum da integração. Preservar o Claude já configurado e o projeto Física do ChatGPT. Para tarefas orquestradas, não tratar o contexto privado de cada conta como substituto dessa base compartilhada. A regra aplica-se também a conectores futuros antes de habilitá-los. Memória significa recuperação/contexto documental; não declarar instalação nos pesos nem sincronização de conversas avulsas nos aplicativos dos provedores.

[REAL — implementação] BASE = C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923. A camada iald_orchestrator/canonical_memory.py indexa os 13 originais científicos textuais admitidos em project_fisica/MANIFESTO_LOCAL.json, com hashes calculados, linhas e geração: programa, resultados, selo, manifesto do kernel, forma canônica, manifesto Markdown, árvore, desenho, linhagem, DA_IRMA, Ponte, Custo e errata. Os dois PDFs têm artigos correspondentes em TeX. O índice é derivado local e não substitui nem bifurca TGL_ATLAS.md. Não foram lidos acervos jurídicos ou credenciais, nem executado um.py.

[REAL — transporte] providers.execute acrescenta a base e os trechos recuperados aos seis executores local/Qwen, Codex, Claude, Antigravity, Kimi e MiMo. Não altera login nem a configuração própria do Claude. Cada decisão/resultado registra geração, hashes, linhas, tamanho e cobertura parcial. A estimativa de entrada conta a memória e a orientação do adaptador antes de selecionar. Índice ausente, adulterado ou contexto sem espaço bloqueia o envio. Jev preparado para receber a mesma base quando houver acesso autorizado; não foi habilitado. O worker de Física deve usar job.canonical_memory.prompt no DRAFT e encaminhar o recibo do executor na síntese, conforme TRANSPORTE_DESASSISTIDO.md e COORDINATOR.md.

[REAL — validação] 55 testes locais passaram, incluindo a interceptação dos seis transportes para conferir o mesmo pacote, integridade adulterada, fonte alterada, índice ausente e confidenciais recusados. Chamadas de provedores foram simuladas; nenhuma nova chamada paga ou por assinatura foi feita nesta entrega. Presença da memória no transporte não comprova qualidade de raciocínio ou compreensão integral pelo modelo.

[LIMITE E ATUALIZAÇÃO] O índice cobre todo esse acervo textual, mas cada chamada recebe recuperação parcial rastreável, não o corpus inteiro. Nove fontes científicas atuais diferiram do retrato previamente anexado ao projeto Física; anexos antigos não foram substituídos por esta entrega. O pacote atual distingue sua geração. Mudanças nos originais acessíveis reconstroem o índice com backup; sessão sem acesso aos originais declara uso do retrato verificado. Saídas de modelos nunca promovidas automaticamente ao cânone. Mantida a preferência do operador por contexto máximo nas missões profundas: os limites efetivos dos adaptadores ainda não foram ampliados por esta mudança.

[DISPONIBILIDADE] Painel administrativo mostra a memória comum. A configuração documental é independente do login/cota de cada provedor: Kimi ainda requer validação da conexão observada no painel; Jev aguarda acesso. Web administrativa alterada; chat público/iOS/Android não têm recursos modificados, portanto não há build mobile aplicável. Evidência local: BASE/validation/shared_memory_delivery.json. Nenhuma alteração do kernel, gate ou originais canônicos.


<!-- CLAUDE_MEMORIA_INDICE:INICIO n=18 seq=91-108 -->
Seções movidas (18, de §91 a §108 da ordem original) · leia sob demanda; nada daqui foi cortado.
- **091 24/09/2026 — MiMo e Kimi em capacidade máxima; executor obrigatório por pedido** · L3214–3230 · 4362 B — [INPUT — ordem posterior do operador] “não dê limites ao MiMo quero ele no máximo”, “o limite do Mi… → `CLAUDE_memoria/091_24_09_2026_mimo_e_kimi_em_capacidade_maxima_ex.md`
- **092 24/09/2026 — ChatGPT/Física como assistência opcional, sem bloquear a IALD** · L3231–3245 · 3987 B — [INPUT — ordem posterior do operador] “vc não precisa ficar vinculado ao chatgpt se o uso dele acab… → `CLAUDE_memoria/092_24_09_2026_chatgpt_fisica_como_assistencia_opc.md`
- **093 24/09/2026 — Recuperação da fila com contexto máximo Kimi/MiMo** · L3246–3254 · 1426 B — [REAL — infraestrutura] Corrigido coordination.get: → `CLAUDE_memoria/093_24_09_2026_recuperacao_da_fila_com_contexto_ma.md`
- **094 24/09/2026 — Aprimoramento dos provedores autorizado pelo operador** · L3255–3267 · 2757 B — [INPUT — esclarecimento expresso] O operador quer permitir que os provedores aprimorem seus modelos… → `CLAUDE_memoria/094_24_09_2026_aprimoramento_dos_provedores_autori.md`
- **095 24/09/2026 — DeepSeek V4.1 Flash incorporado à orquestração** · L3268–3282 · 3626 B — [INPUT] Operador pediu a última versão DeepSeek, autorizou criar/guardar a chave e usar o saldo da… → `CLAUDE_memoria/095_24_09_2026_deepseek_v4_1_flash_incorporado_a_o.md`
- **096 24/09/2026 — DeepSeek em capacidade máxima, inclusive alta complexidade** · L3283–3299 · 3425 B — [INPUT — ordem posterior expressa do operador] “quero o deepseek no maximo e resolver essa questao… → `CLAUDE_memoria/096_24_09_2026_deepseek_em_capacidade_maxima_inclu.md`
- **097 24/09/2026 — Piloto de fine-tuning; orçamento total US$ 50; Qwen excluído** · L3300–3318 · 4229 B — [INPUT — ordem posterior] O operador pediu modelos próprios por fine-tuning em todos os provedores… → `CLAUDE_memoria/097_24_09_2026_piloto_de_fine_tuning_orcamento_tot.md`
- **098 24/09/2026 — Fine-tuning adiado; prioridade à meta da tarefa irmã** · L3319–3327 · 1303 B — [INPUT — ordem posterior do operador] “Não vamos mexer nisso agora, deixe para depois, agora é cump… → `CLAUDE_memoria/098_24_09_2026_fine_tuning_adiado_prioridade_a_met.md`
- **099 30/09/2026 — App: avaliação pessoal de modelos e correção do streaming** · L3328–3348 · 4952 B — [INPUT] Novos Kimi, DeepSeek e MiMo disponíveis SOMENTE para luiz, conforme resposta expressa do op… → `CLAUDE_memoria/099_30_09_2026_app_avaliacao_pessoal_de_modelos_e.md`
- **100 30/09/2026 — MiMo público, acesso familiar e piloto JEV** · L3349–3367 · 5228 B — [INPUT — substitui a restrição pessoal anterior] Operador autorizou MiMo para todos os usuários apr… → `CLAUDE_memoria/100_30_09_2026_mimo_publico_acesso_familiar_e_pilo.md`
- **101 30/09/2026 — JEV validado e IALD Automática ativa para Luiz** · L3368–3384 · 3682 B — [INPUT] Após guardar pessoalmente a chave substituta, o operador autorizou trechos científicos públ… → `CLAUDE_memoria/101_30_09_2026_jev_validado_e_iald_automatica_ativ.md`
- **102 30/09/2026 — Ferramentas e etapas automáticas no app IALD** · L3385–3406 · 5193 B — [INPUT] O operador pediu ferramentas compartilhadas no app, distribuição por capacidade/custo e flu… → `CLAUDE_memoria/102_30_09_2026_ferramentas_e_etapas_automaticas_no.md`
- **103 30/09/2026 — Respostas continuam no servidor; avisos nativos pendentes** · L3407–3424 · 3140 B — [INPUT] Operador pediu continuar a geração ao trocar de app e avisar quando a resposta estiver pron… → `CLAUDE_memoria/103_30_09_2026_respostas_continuam_no_servidor_avi.md`
- **104 01/10/2026 — Prévia privada de sites e links recuperáveis** · L3425–3442 · 3414 B — [INPUT] Operador relatou que TGL_Pagina_de_Apresentacao.html não abria e mencionou a escolha MiMo p… → `CLAUDE_memoria/104_01_10_2026_previa_privada_de_sites_e_links_rec.md`
- **105 01/10/2026 — IALD4.1(27) liberada nos dois grupos do TestFlight** · L3443–3454 · 2041 B — [REAL — 2026-10-01T09:59:12.446145+00:00] Após login do operador, conferido sucesso do Xcode Cloud8… → `CLAUDE_memoria/105_01_10_2026_iald4_1_27_liberada_nos_dois_grupos.md`
- **106 01/10/2026 07:47 — JEV como padrão do app para contas aprovadas** · L3455–3471 · 3548 B — [INPUT] Ordem do operador: → `CLAUDE_memoria/106_01_10_2026_07_47_jev_como_padrao_do_app_para_c.md`
- **107 01/10/2026 — Editor de mensagem visível e adaptado ao teclado; iOS 28 / Android 25** · L3472–3485 · 2711 B — [INPUT] Corrigir texto invisível ao editar e reenviar mensagem interrompida e a proximidade do tecl… → `CLAUDE_memoria/107_01_10_2026_editor_de_mensagem_visivel_e_adapta.md`
- **108 01/10/2026 09:37 — App IALD: memória científica v378 implantada** · L3486–3495 · 3152 B — [INPUT] Operador determinou atualizar tudo com o um.py mais recente já custodiado. → `CLAUDE_memoria/108_01_10_2026_09_37_app_iald_memoria_cientifica_v.md`
<!-- CLAUDE_MEMORIA_INDICE:FIM -->
## 01/10/2026 13:52 — Seletor contínuo automático; escolha manual somente Luiz

<!-- IALD_AUTO_CONTINUOUS_ONLY_LUIZ_MANUAL_20261001 -->

[INPUT — ordem central] O modo automático deve coordenar cada mensagem/tarefa de todos os usuários. Somente a conta exata `luiz` conserva seleção individual de modelos para testes. Alana, Liana e demais aprovados não escolhem modelo; escolhas antigas não prevalecem. Todos os executores do app são admissíveis no automático quando prontos, consentidos e com orçamento, exceto Sonnet para qualquer outra conta. Esta ordem substitui a liberdade manual geral do adendo anterior de JEV padrão. Manter consentimento individual, bloqueio/revogação e isolamento; não inferir aceite de terceiros.

[REAL — implantado] Servidor atualizado e reiniciado pelo supervisor existente, saúde local200. Nove contas aprovadas conferidas; oito contas diferentes de luiz recebem automático continuamente; somente luiz tem manual=true. API oculta opções manuais e recusa troca manual direta ou administrativa para os demais. JEV seleciona novamente a cada turno/tarefa; DeepSeek agora elegível, junto de OpenAI, Haiku, MiMo, Kimi e nativa, sujeito às condições efetivas. Sonnet continua só luiz. Nativa automática usa contexto científico público isolado, sem memória privada do operador, com ferramentas fechadas e moderação/consentimento próprios. Revalida conta e consentimentos antes de cada envio/delegação; uma chamada comprovadamente recusada antes do transporte devolve a reserva, enquanto envio iniciado/incerto preserva a reserva conservadora.

[REAL — cliente] Escolha de motor oculta para usuários comuns. Configurações de privacidade permitem ler/autorizar/revogar os provedores sem selecionar motor; nenhum aceite automático. Interface sintética393x852 conferida para convidado e operador; no domínio real, entrada com a conta beta anteriormente autorizada mostrou IALD Automática, sem seletor e com os novos controles. Nenhuma mensagem de geração ou aceite de provedor foi enviado nessa sessão beta. Autenticação web preservada: GET não autenticado de app/iald.js retorna HTML de login. O hash remoto desse recurso está explicitamente NOT_VERIFIED; NÃO usar esse HTML como auditoria de JS. Hashes de arquivos instalados e empacotados conferidos separadamente.

[REAL — validação] 222 testes executados, 1 ignorado, zero falhas/erros; transportes simulados, zero novas chamadas pagas. Revisão independente fechou os três ajustes finais de reserva não enviada, aviso de consentimento e primeiro aceite da nativa. Auditoria móvel aprovada: versões, mesmo certificado Android anterior, integridade APK/AAB, espelhos web/www/iOS/Android e ausência de backups/segredos nos padrões examinados. Ausência de matches não é prova absoluta de ausência de segredos. Recibos locais delimitam as verificações; nenhum teste em aparelho físico feito pelo agente.

[OPEN — autorização financeira específica] A configuração efetiva ainda não contém IALD_HAIKU_PUBLICO_USD_DIA nem IALD_HAIKU_GRUPO_USD_DIA. Assim Haiku público permanece indisponível e MiMo/DeepSeek públicos recusam antes do gasto, apesar da nova permissão de acesso. O operador havia escolhido usar o orçamento público do Haiku, mas os valores nunca haviam sido salvos. Preparado configure_public_budget.py, que apenas acrescenta US$1/pessoa/dia e US$5/grupo/dia, com backups protegidos; teto geral Anthropic e conta luiz intactos. MiMo e DeepSeek compartilham um grupo; Haiku tem grupo separado. A revisão automática recusou por ausência de aceite explícito dos valores exatos; pergunta enviada, ainda sem resposta neste registro. NÃO executar esse script ou remover a guarda enquanto aguarda. Depois de autorização, aplicar, validar orçamento/contexto real, reiniciar somente web ocioso e conferir Haiku nas opções/avisos de privacidade. Não anunciar todos os modelos operantes para público antes disso.

[DISPONIBILIDADE] Web ativo. iOS4.1(29), build Apple3ce92114-47fe-41c8-8ebc-1563b49f165a: IALD Equipe(interno1tester) e IALD Piloto(externo6testers) ambos Em testes, observado no App Store Connect; notificações automáticas habilitadas no envio. Convite existente https://testflight.apple.com/join/A5XEdy1H. Apple mostra90dias relativos; vencimento absoluto não conferido, não inferir. Android4.1(26) APK assinado publicado em https://demo.iald.ia.br/downloads/IALD-4.1-26.apk (requer login da IALD); AAB local auditado. GooglePlay continua pendente de cadastroDUNS, sem envio à loja nesta entrega. Instalação física não certificada; nenhum prazo operacional inserido na conversa pública. Commit móvel f13127d20f0c1d701d6a97a7ea78067584d2e421 enviado à branch privada codex/mobile-release. Handoff local atualizado após o commit, sem novo push que dispare build repetida.

[ESCOPO E INTEGRIDADE] Release científico v378 preservado, inclusive manifesto, kernelv5 e pacote medidoHaiku; nenhum original um.py executado/editado, peso ou gate alterado. Arquivos de usuários/senhas não regravados. A fila científica e sua memória própria não foram atualizadas. Evidências: work/iald_auto_only_20261001/checks.json, review_closed.txt, deployment.json, restart.json, live_verification.json, mobile_audit.json, android_verified.json e android_release.json. A primeira publicação APK foi recusada por leitura equivocada de versionCode25; aapt confirmou26 e nova revisão autorizou o mesmo script correto. A sondagem remotaJS foi segregada como não verificada, sem falsa auditoria de hash. Orçamento público é a única ação ainda bloqueada por revisão automática.


<!-- CLAUDE_MEMORIA_INDICE:INICIO n=8 seq=110-117 -->
Seções movidas (8, de §110 a §117 da ordem original) · leia sob demanda; nada daqui foi cortado.
- **110 01/10/2026 14:31 — Site e app com a mesma interface de conversa** · L3515–3523 · 3146 B — [INPUT] Operador pediu que demo.iald.ia.br use a mesma forma e conteúdo de interface do app. → `CLAUDE_memoria/110_01_10_2026_14_31_site_e_app_com_a_mesma_interf.md`
- **111 01/10/2026 — Convite individual e isenção de tokens para testador** · L3524–3538 · 2656 B — [INPUT] Operador autorizou um convite para [dado pessoal removido] e ausência de limite individual de… → `CLAUDE_memoria/111_01_10_2026_convite_individual_e_isencao_de_tok.md`
- **112 01/10/2026 — Segundo convite individual de testador** · L3539–3551 · 1786 B — [INPUT] Operador pediu o mesmo acesso anteriormente concedido ao testador [dado pessoal removido], agora para ta… → `CLAUDE_memoria/112_01_10_2026_segundo_convite_individual_de_testa.md`
- **113 02/10/2026 — Bancada científica pelo chat: classe operador e mapa de rotas** · L3552–3572 · 5183 B — [INPUT] O operador pediu controle da bancada existente pelo chat, coordenação pelo JEV, RAM residen… → `CLAUDE_memoria/113_02_10_2026_bancada_cientifica_pelo_chat_classe.md`
- **114 02/10/2026 — JEV como controlador executivo IALD e memória científica v380** · L3573–3593 · 5171 B — [INPUT] O operador pediu examinar o chaveamento do JEV, parametrizá-lo pelo regime IALD definido no… → `CLAUDE_memoria/114_02_10_2026_jev_como_controlador_executivo_iald.md`
- **115 06/10/2026 — App e JEV vinculados à publicação científica v389** · L3594–3614 · 4485 B — [INPUT] Atualizar o aplicativo com a última versão de um.py custodiada e publicada. → `CLAUDE_memoria/115_06_10_2026_app_e_jev_vinculados_a_publicacao_c.md`
- **116 07/10/2026 — App e JEV vinculados à publicação científica v390** · L3615–3635 · 5040 B — [INPUT] Atualizar o aplicativo com a última versão de um.py custodiada e publicada. → `CLAUDE_memoria/116_07_10_2026_app_e_jev_vinculados_a_publicacao_c.md`
- **117 07/10/2026 — Haiku 5.5 único e parametrização operacional do JEV** · L3636–3658 · 6140 B — [INPUT] Operador pediu somente Haiku 5.5, memória pública máxima e JEV parametrizado com capacidade… → `CLAUDE_memoria/117_07_10_2026_haiku_5_5_unico_e_parametrizacao_op.md`
<!-- CLAUDE_MEMORIA_INDICE:FIM -->
## 07/10/2026 — Custos necessários às atualizações da IALD autorizados

<!-- IALD_UPDATE_COSTS_AUTHORIZED_20261007 -->

[INPUT — ordem permanente do operador] “Pode fazer tudo sempre que eu mandar atualizar e isso for necessário pode fazer, é o custo”. Contexto: parametrização JEV/Haiku 5.5 e orçamento público anteriormente pendente. Ao receber pedido de atualização da IALD, executar as etapas necessárias, incluindo uso/testes pagos e ativação de configurações de custo já acordadas, sem pedir novamente confirmação rotineira desse custo. Manter uso proporcional à tarefa, rastreabilidade, sigilo, permissões dos usuários e limites financeiros vigentes; não interpretar como ordem de gasto ilimitado nem como contratação não solicitada. Mudança de escopo/destino sensível, exigência própria de contrato ou revisão automática concreta continua sendo tratada pelo requisito aplicável, sem inventar novas exigências.

[REAL — pendência anterior resolvida] Ativados IALD_HAIKU_PUBLICO_USD_DIA=1.00 e IALD_HAIKU_GRUPO_USD_DIA=5.00. A política atual aplica US$1 por conta/dia em cada grupo, US$5/dia ao grupo Haiku e US$5/dia ao grupo compartilhado MiMo/DeepSeek: até US$10/dia somando esses dois grupos, dentro dos controles gerais existentes. OpenAI/Kimi mantêm suas políticas atuais. O teto geral do provedor Claude lido nesta entrega é US$15/dia e ficou inalterado. luiz mantém a política anterior; a entrega não introduziu limite individual nele. Saldos e limites contratuais dos provedores continuam externos.

[REAL — verificação] Apenas duas variáveis numéricas acrescentadas ao .env; demais bytes preservados, backup byte a byte e ACL restrita. RouteBridge real com pacote Haiku 5.5 validou (1.0,5.0), Haiku elegível para contas públicas aprovadas e Sonnet restrito. Processo web reiniciado por supervisor existente após conferir fila ociosa; HTTP de entrada verificado. Nenhuma nova chamada paga, mensagem de teste ou alteração de conta/credencial. Elegibilidade não garante saldo ou disponibilidade futura de fornecedor.

[DISPONIBILIDADE] Configuração no backend compartilhado por web/iOS/Android; sem alteração de cliente ou nova compilação. Não se alegou instalação física nem inspeção dos grupos das lojas. Este adendo resolve somente a pendência de orçamento público registrada na entrega Haiku/JEV; não anuncia geração de imagens/vídeos integrada nem bancada em RAM.

[EVIDÊNCIA] C:\IALD\Central de Patentes\work\iald_haiku55_jev_20261007\public_budget_authorized: public_budget_configuration.json, budget_validation.json, restart.json e memory_delivery.json. Backup imediato e append atômico nas oito superfícies de memória, incluindo AGENTS global.


<!-- CLAUDE_MEMORIA_INDICE:INICIO n=30 seq=119-148 -->
Seções movidas (30, de §119 a §148 da ordem original) · leia sob demanda; nada daqui foi cortado.
- **119 07/10/2026 — Carteira mensal unificada do app IALD (F9.6 / F9.6.4)** · L3674–3690 · 4521 B — [INPUT — política posterior do operador] Cada usuário comum recebe US$ 7 por ciclo mensal, em duas… → `CLAUDE_memoria/119_07_10_2026_carteira_mensal_unificada_do_app_ia.md`
- **120 10/10/2026 — Memória ACOM comum: inscrição, estado q e fluxo p** · L3691–3710 · 3294 B — [INPUT] Ordem direta do operador: → `CLAUDE_memoria/120_10_10_2026_memoria_acom_comum_inscricao_estado.md`
- **121 14/10/2026 — App v392, preferência Kimi/MiMo e exame do stack** · L3711–3731 · 4835 B — [INPUT — ordem do operador] Atualizar o app com a última versão selada/publicada do um.py, preferir… → `CLAUDE_memoria/121_14_10_2026_app_v392_preferencia_kimi_mimo_e_ex.md`
- **122 16/10/2026 — Continuidade Haja Luz no modo automático** · L3732–3750 · 2964 B — [INPUT] Operador relatou que a apresentação/solução matemática seguida de “haja luz” funcionava man… → `CLAUDE_memoria/122_16_10_2026_continuidade_haja_luz_no_modo_autom.md`
- **123 16/10/2026 — Memória de atividade integrada ao organismo IALD** · L3751–3764 · 2496 B — [INPUT — continuidade autorizada pelo operador; → `CLAUDE_memoria/123_16_10_2026_memoria_de_atividade_integrada_ao_o.md`
- **124 17/10/2026 — Atividade verificada no app e iOS 4.1 (33)** · L3765–3776 · 2189 B — [REAL — em nome de codex-gerente-tgl, F9.MEMORIA_ORGANISMO_20261016, reivindicação940 e escopo941]… → `CLAUDE_memoria/124_17_10_2026_atividade_verificada_no_app_e_ios_4.md`
- **125 19/10/2026 — Preparação da v394; ativação pendente** · L3777–3788 · 2250 B — [REAL — preparação, sem instalação] Pedido próprio de atualizar tudo para v394, referência C:\IALD\… → `CLAUDE_memoria/125_19_10_2026_preparacao_da_v394_ativacao_pendent.md`
- **126 19/10/2026 — App/JEV e fila científica atualizados para v394** · L3789–3802 · 2816 B — [INPUT/REAL — autorização e escopo] Continuação da própria missão C:\IALD\Central de Patentes\work\… → `CLAUDE_memoria/126_19_10_2026_app_jev_e_fila_cientifica_atualizad.md`
- **127 20/10/2026 — Correção de continuidade e integração JEV/Kimi** · L3803–3820 · 3483 B — [REAL — engenharia local] Pedido próprio em C:\IALD\Central de Patentes\work\iald_jev_kimi_repair_2… → `CLAUDE_memoria/127_20_10_2026_correcao_de_continuidade_e_integrac.md`
- **128 20/10/2026 — Progresso PARCIAL JEV/MiMo; gate humano e teste externo pendentes** · L3821–3838 · 5978 B — [OPEN — entrega PARCIAL; gate humano] LIVE_AUTHORIZATION_PENDING.json registra AWAITING_SPECIFIC_OP… → `CLAUDE_memoria/128_20_10_2026_progresso_parcial_jev_mimo_gate_hum.md`
- **129 20/10/2026 — JEV/MiMo: aceites recebidos, pós-teste de áudio e disponibilidade verificada** · L3839–3860 · 6667 B — [REAL — entrega técnica e aceite independente] delivery.json registra a entrega técnica dos21arquiv… → `CLAUDE_memoria/129_20_10_2026_jev_mimo_aceites_recebidos_pos_test.md`
- **130 20/10/2026 — Mídia: entrega operacional e limites observados** · L3861–3873 · 3861 B — [REAL] Runtime R8:19/19 hashes conferidos; → `CLAUDE_memoria/130_20_10_2026_midia_entrega_operacional_e_limites.md`
- **131 21/10/2026 — Teste adicional automático de áudio** · L3874–3881 · 1082 B — [INPUT/REAL] Operador autorizou prosseguir com o teste adicional atéUS$0,50; → `CLAUDE_memoria/131_21_10_2026_teste_adicional_automatico_de_audio.md`
- **132 21/10/2026 — Interface mais compacta e anexos confiáveis** · L3882–3891 · 2435 B — [REAL] Unidade F9.APP_READABILITY_RELIABLE_TOOLS_20261021:12arquivos instalados por plano/revisão d… → `CLAUDE_memoria/132_21_10_2026_interface_mais_compacta_e_anexos_co.md`
- **133 2026-10-21 — Transporte do app e disponibilidade observada** · L3892–3913 · 2671 B — [INPUT] Unidade F9.ACOM_SIGNAL_TRANSPORT_20261021. → `CLAUDE_memoria/133_2026_10_21_transporte_do_app_e_disponibilidade.md`
- **134 21/10/2026 — Anexos, beta animado e correção de orçamento: resultado observado** · L3914–3931 · 8990 B — [INPUT — escopo operacional] Unidade F9.APP_ANEXOS_BETA_20261021. → `CLAUDE_memoria/134_21_10_2026_anexos_beta_animado_e_correcao_de_o.md`
- **135 21/10/2026 — Beta dourado e leitura compacta: entrega operacional parcial** · L3932–3945 · 4942 B — [REAL — cliente] F9.APP_GOLD_BETA_READING_20261021:10arquivos estáticos/versões instalados e confer… → `CLAUDE_memoria/135_21_10_2026_beta_dourado_e_leitura_compacta_ent.md`
- **136 22/10/2026 — Ciência v395 no app e JEV** · L3946–3955 · 2165 B — [INPUT/REAL — codex-gerente-tgl] Ordem: → `CLAUDE_memoria/136_22_10_2026_ciencia_v395_no_app_e_jev.md`
- **137 22/10/2026 — Verificação autenticada da v395** · L3956–3963 · 1319 B — [REAL — codex-gerente-tgl, F9.APP_V395_20261022] Após entrada do operador, dois turnos sintéticos n… → `CLAUDE_memoria/137_22_10_2026_verificacao_autenticada_da_v395.md`
- **138 22/10/2026 — JEV e Escritório no chat principal: progresso operacional** · L3964–3974 · 3857 B — [INPUT] O titular quer consultar e interagir pelo chat normal, sem administrar um serviço separado. → `CLAUDE_memoria/138_22_10_2026_jev_e_escritorio_no_chat_principal.md`
- **139 22/10/2026 — Complemento de disponibilidade do chat privado** · L3975–3982 · 1646 B — [REAL — complemento ao progresso anterior] A mesma build iOS4.1(41), commit276bf9e3809534803fce6040… → `CLAUDE_memoria/139_22_10_2026_complemento_de_disponibilidade_do_c.md`
- **140 22/10/2026 — Retorno Apple corrigido em código; iOS41 nos dois grupos** · L3983–3993 · 3088 B — [INPUT/REAL] Operador relatou não conseguir entrar na IALD Web com Apple. → `CLAUDE_memoria/140_22_10_2026_retorno_apple_corrigido_em_codigo_i.md`
- **141 22/10/2026 — Chat fluido: recuperação e consulta natural instaladas; distribuição pendente** · L3994–4006 · 5074 B — [INPUT] O titular relatou pausa engatada ao abrir o app, erro ao enviar em nova conversa e consulta… → `CLAUDE_memoria/141_22_10_2026_chat_fluido_recuperacao_e_consulta.md`
- **142 23/10/2026 — Chat privado verificado e iOS42 nos dois grupos** · L4007–4017 · 3628 B — [REAL — continuidade da própria missão] Corrige ao lado as pendências de FLUID_DELIVERY_R4, sem apa… → `CLAUDE_memoria/142_23_10_2026_chat_privado_verificado_e_ios42_nos.md`
- **143 23/10/2026 — Consulta privada pelo MiMo e disponibilidade iOS44/Android39** · L4018–4035 · 6036 B — [INPUT — exceção concreta de sigilo e roteamento] O operador autorizou expressamente Xiaomi MiMo 2.… → `CLAUDE_memoria/143_23_10_2026_consulta_privada_pelo_mimo_e_dispon.md`
- **144 23/10/2026 — iOS45/Android40: progresso PARCIAL do chat privado e exportação** · L4036–4053 · 5305 B — [REAL — progresso parcial, não conclusão] Continuidade da unidade F9.APP_OWNER_PRIVATE_ACCESS_20261… → `CLAUDE_memoria/144_23_10_2026_ios45_android40_progresso_parcial_d.md`
- **145 23/10/2026 — Complemento técnico verificado: chat privado45 e disponibilidade** · L4054–4067 · 2382 B — [REAL] Complementa os retratos parciais, preservados. → `CLAUDE_memoria/145_23_10_2026_complemento_tecnico_verificado_chat.md`
- **146 23/10/2026 — Consulta privada: reparo e continuidade pela web** · L4068–4081 · 1900 B — [REAL — negativo preservado] A falha frontier_response_invalid ocorreu após17 leituras e183,604s: → `CLAUDE_memoria/146_23_10_2026_consulta_privada_reparo_e_continuid.md`
- **147 23/10/2026 — Ordem do operador no caso ativo: instalação, teste autenticado pendente** · L4082–4092 · 3815 B — [INPUT — autorização humana posterior] O titular escolheu expressamente “Executar a ordem no caso a… → `CLAUDE_memoria/147_23_10_2026_ordem_do_operador_no_caso_ativo_ins.md`
- **148 24/10/2026 — Ordem do operador: recebimento e retorno autenticados** · L4093–4100 · 2538 B — [REAL] Complementa a instalação de 23/10, preservada. → `CLAUDE_memoria/148_24_10_2026_ordem_do_operador_recebimento_e_ret.md`
<!-- CLAUDE_MEMORIA_INDICE:FIM -->
