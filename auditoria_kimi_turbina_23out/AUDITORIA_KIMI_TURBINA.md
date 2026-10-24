AUDITORIA KIMI — turbina e modo dobrado — 23/10
**NÃO BLOQUEANTE para o modo dobrado:** todo pacote dobrado traz o aviso no texto do prompt e `folded/fold_layers/fold_notice` no recibo; nenhum caminho lido ou testado faz índice + trechos parciais passarem por memória completa (`coverage` fica `PARTIAL_RETRIEVAL_NOT_FULL_CORPUS`). **ALTOS (não da dobra):** o benchmark v1 se aprova por construção e a «deriva de gabarito 12/36» é um falso negativo de formato (§4, §3). **MÉDIO fora da dobra:** o Nós Vivo entrega fontes como prefixo de 2.400 caracteres sem marcador no texto (§2.7).

Aferidora: subagente Claude (Sonnet 5.5), por ordem da gerência c1 · 23/10/2026, ~20:30 · só leitura fora desta pasta e da cópia de teste (`C:\t\orq_copia_kimi`, apagada ao fim) · nenhuma chamada a provedor, nenhum processo vivo tocado, nada registrado no mapa, quadro, memória, túnel, site ou git (o rascunho de ANOTACAO está em `registro_mapa_anotacao_kimi.json`; quem registra é a gerência).
Estatutos: **[REAL]** reproduzido aqui por script (saídas em `evidencias/saidas`) · **[DECLARADO]** afirmado por Kimi ou Codex e não reproduzido · **[INPUT]** palavra do operador citada por terceiros, sem verbatim pinado.

---

## 0. Veredito por item (A–D do briefing v2)

| Item | Veredito | Núcleo da prova |
|---|---|---|
| **A** Turbina: descida em camadas, critério de parada, ranking | **ASSINA** a aritmética (economia 95,49 %, fator 22,2×, pins c3/c2/c1) · **CONTESTA** a leitura: «recall 0,6667 / deriva de gabarito 12/36» (refutada), «grep» (é consulta por chave), «dobrar o acervo sobe uma oitava» (o custo é linear) · **FALTA** o pré-registro do critério de parada e do ranking | §3, §5 |
| **B** Benchmark pré-registrado (seq 1288) | **CONTESTA**: não assinar o v1 e não rodar o pacote v1. **ASSINA** o adendo v2 do Codex como base, com 5 acréscimos | §4 |
| **C** Cabeçalho de confiança «v2» e modo dobrado | Cabeçalho v1: **CONTESTA** (4 contraexemplos) · «v2» do Kimi: **FALTA** (só existe a constante v1 no caderno) · v2 do Codex (`HEADER_V2.txt`): **ASSINA** com 1 ressalva · Dobra do Kimi (`57bf9be7`): **CONTESTA** (superada) · Produção atual (`f95ed18e`): **ASSINA** | §2, §4.4 |
| **D** Manutenção de 21/10 e esta resposta | Título F9.9 e reindexação do Nós Vivo: bytes **ASSINA**; processo **CONTESTA** (PROGRAMA.json «só pelo `iald.py`»); **FALTA** o verbatim das ordens de 19:11 e 09:40 | §6 |
| extras | 1302 (Bancada): **FALTA** (livro não tem a observação) · 1301 (kilonova): **ASSINA** · 1303 (vigília): **ASSINA** 2 de 3 bloqueios, **CONTESTA** o 1.º («curado pela dobra») | §6 |

---

## 1. Método e limites

- **Livro e caderno:** lidos `rotas.jsonl` (cadeia verificada: `rotas.py verificar` = ok, 1366 registros, cabeça `83e5c5f0…`), os seqs 1285–1304 e 1308, o caderno do Kimi e as entregas do Codex de 21/10 (`work\kimi_stack_upgrade_20261021`).
- **Cópia de teste:** `make_copy.py` copia só o código (sem `state`, sem segredos) para `C:\t\orq_copia_kimi`; três variantes de `canonical_memory.py` vêm dos backups de bytes ao lado da produção; memória canônica **sintética** selada (13 fontes, mesmas regras de `_verify_snapshot`), `provenance.json` sem pinos, estado ACOM em pasta-sandbox, PATH sem CLIs de provedor, proxy morto. [REAL] `iald_orchestrator.__file__` resolve dentro da cópia.
- **Limites:** não rodei fila real nem provedor; a memória é sintética (reproduz o número do Kimi, 7.364 B, ver §2.2); o χ² da Bancada (seq 1302) não foi reproduzido (um POST escreveria no livro de produção); o prompt da VOZ (item 4 da ordem dele) não foi revisado.
- **Reprodução:** `evidencias\run_all.py` refaz tudo em ~2 min (`C:\Python314\python.exe -X utf8 run_all.py`).

---

## 2. O MODO DOBRADO em `canonical_memory.prepare()` (o ponto mais sensível)

### 2.1 O que mudou de fato
| versão | sha256 (16) | bytes | mudança |
|---|---|---|---|
| pré-Kimi (`.bak_20261020_191500_dobra_envelope`) | `7cb8f3225a02c46f` | 22.372 | — |
| **Kimi** (20/10 19:15) = `.bak_20261021_133553_…` | `57bf9be7842bcafd` | 24.165 | só `prepare()` (AST); +24/−4 linhas: dobra, `if not references and not folded`, 3 campos no recibo |
| **produção atual** (21/10 10:35:53) | `f95ed18ee33e180f` | 24.714 | só `prepare()` de novo; +32/−20 em relação ao Kimi |

[REAL] **A produção já não é a versão do Kimi.** Em 21/10 10:35 o Codex (`codex-kimi-envelope`, revisão `codex-readability-reviewer`, instalação revista por `codex-app-01a094df`; ordem do operador em `OPERADOR.txt`) substituiu a dobra por uma versão endurecida, junto com `layered_retrieval.py`, `nos_packet.py` e `transport_cli.py` (seq 1308). O backup `…133553_…` é a versão do Kimi: difere do pré-Kimi só pela cirurgia que ele descreve (AST: apenas `prepare()`), e nenhum outro arquivo do orquestrador mudou entre 20/10 19:00 e a instalação. Os 4 processos `mcp_server.py` do orquestrador em execução foram iniciados em 23/10 (07:52 ×3, 10:38), depois dessa instalação [REAL, `Win32_Process.CreationDate`]; por inferência carregam `f95ed18e`.

### 2.2 «Impossibilidade verdadeira segue bloqueando com a mensagem original»: **só em parte**
[REAL] Tabela de reprodução (`saidas/02_fold_tabela.txt`; `ACEITA` = `prepare()` devolveu pacote):

| caso | pré-Kimi | Kimi | produção atual |
|---|---|---|---|
| C1: o caso do próprio Kimi (prompt real do briefing + reserva 20.911, teto 12.000) | recusa | **ACEITA dobrado: 28.028 chars = 2,3× o teto** (pacote 7.364 B, **o número que ele reportou**) | recusa |
| C1b: fila real (reserva 15.852 da F9.9, teto 20.000; seq 1304) | recusa | **ACEITA: 22.969 > 20.000** | recusa |
| C2: `maximum`, reserva = teto de bytes | recusa | **ACEITA: 911.379 B > 909.312** | recusa |
| C2b: `deepseek_maximum` | recusa | **ACEITA: 649.235 > 647.168** | recusa |
| C3x: pedido multibyte (`ç`×17.000 e ×17.400), **sem reserva nenhuma**, padrão 36.000 B | recusa | **ACEITA: 36.055 e 36.855 B > 36.000** | recusa |
| C7: lista de fontes autorizadas vazia + reserva | recusa | **ACEITA com 0 fontes, 7.152 > 7.000** | recusa (mensagem nova) |
| C4: pedido de 20.000 chars, teto 12.000 | recusa (original) | recusa (original) | recusa (mensagem nova) |
| C5: dobra legítima (reserva 21.300, teto 24.000) | — | dobra, 0 trechos, 23.318 ≤ 24.000, aviso | dobra `INDEX_ONLY_NO_PASSAGES`, 23.306, aviso |
| C6: caminho normal | 1 trecho, 3.512 | idem | idem |

Leitura: a mensagem original só sobrevive na dimensão «pedido sozinho maior que o teto de caracteres» (C4). O teste do próprio Kimi (`teste_dobra_envelope.py`, sha `5f31500d…`) **não pode detectar** o resto: o critério do caso 1 é `folded and len(r["prompt"]) <= 12000`, **sem somar a reserva**. [REAL] Rodado contra as três variantes na cópia (`saidas/04_…`): **3/3 PASS no Kimi**; **na produção atual o caso 1 FALHA** (recusa) e o caso 3 passa com `erro_original_preservado=false` (a mensagem mudou). Ou seja, o resultado que ele chama de «caso bloqueado agora passa» deixou de valer, e nunca valeu para o envelope agregado.

### 2.3 O segundo portão desfaz o «desbloqueio» (e protege o provedor)
[REAL] `nos_packet.prepare_queue` → `operational_memory.attach` → `request_controls.enforce_packet` (`saidas/03_attach_*`):
- caso A (teto 12.000, reserva 20.911) e caso B (teto 20.000, reserva 15.852): na versão do Kimi o `prepare()` passa e o **`attach` recusa** («Projeção com memória e orientação excede o teto do pedido»). A dobra só deslocou a recusa de lugar.
- [REAL, tasks.sqlite3 em leitura] os três jobs do Kimi (`e1ce17ac`, `9dd45d6a`, `90528e45`) seguem `awaiting_dispatch` hoje; a frase da ordem «foi esse bloqueio que segurou o teu briefing» não se sustenta, e o próprio Kimi recuou na seq 1304 («a dobra do envelope NÃO é o gargalo»).
- caso C (dobra legítima, reserva 21.300, teto 24.000): atravessa todos os portões, **com o aviso no prompt final e os três campos no recibo** (versão do Kimi e atual).

### 2.4 Pergunta do BLOQUEANTE: a dobra pode entregar memória científica incompleta sem aviso legível?
**Não.** [REAL] Em todos os casos `folded=True` das duas versões (C1, C1b, C2, C2b, C3x, C5, C7) o prompt contém «MODO DOBRADO…»; o recibo tem `folded`, `fold_layers`, `fold_notice`; na atual também `retrieval_scope`, `budget_skipped_passages`, `document_pins`, `index_sha256`. Após `attach` o recibo é copiado integralmente (`deepcopy`). Texto vigente do aviso: «…segue o ÍNDICE dos documentos da geração verificada. Trechos só entram se couberem; índice sem trechos não equivale à leitura do conteúdo.»

### 2.5 Algum caminho passa «índice pinado + trechos parciais» por memória completa?
**Não encontrado.** `grep` no repositório: nenhum consumidor testa completude; `coverage` é sempre `PARTIAL_RETRIEVAL_NOT_FULL_CORPUS` (também dobrado). `runtime.py` só confere `memory_mode`; `enforce_packet` confere teto, geração e allowlist. **Mudança de invariante a decidir (ato do operador):** a regra antiga «pelo menos um trecho científico, senão bloqueia» foi derrogada na dobra. Uma dobra `INDEX_ONLY` entrega CORE + lista de arquivos e zero trechos. A régua de ACOM diz «estado obrigatório nunca é omitido para caber»; aqui o CORE e o índice são obrigatórios e os trechos, opcionais, mas isso é uma escolha de política que ninguém ratificou.

### 2.6 Os testes da casa: as falhas são pré-existentes?
[REAL] `evidencias/run_tests.py`, cinco configurações × quatro módulos, mesma suíte (`saidas/testes`):

| configuração | canonical_memory (9) | request_controls (11) | coordination (6) | transport (7) |
|---|---|---|---|---|
| A0 ambiente 20/10 + pré-Kimi | 1F+1E | 1E | OK | OK |
| A1 ambiente 20/10 + Kimi | 1F+1E | 1E | OK | OK |
| B0 hoje + pré-Kimi | 1F+1E | 1E | OK | OK |
| B1 hoje + Kimi | 1F+1E | 1E | OK | OK |
| B2 hoje + produção atual | 1F+1E | 1E | OK | OK |

Os **mesmos 3 testes** falham com a **mesma causa** em todas: `test_every_executor_receives_same_packet_without_network`, `test_changed_packet_fails_before_network` e `test_large_packet_not_cut_to_old_transport_cap` chamam `providers.execute` direto e esbarram em `opmem.verify_packet` («Operational memory required; submit through the durable queue»). **Pré-existentes, não causados pela dobra: ASSINA a afirmação do Kimi.** Ressalvas: (i) ambiente com memória sintética (coordination/transport 6/6 e 7/7 não são contra a memória real); (ii) o valor probatório é fraco: dois dos três testes mortos são os que mediriam pacote e teto, e **nenhum teste do repositório cobre `folded`** (grep: zero), nem a reserva (`reserved_context_*` só aparece num teste com mock).

### 2.7 Achados
| # | sev. | achado | estado |
|---|---|---|---|
| F1 | MÉDIO | A dobra do Kimi aceitava pacote acima do teto agregado (chars, bytes, allowlist vazia, pedido multibyte): falso sucesso em `prepare()`; o teste dele mede só o pacote | **corrigido na produção; verificado** (§2.2) |
| F2 | MÉDIO | «O caso bloqueado agora passa» e «foi esse bloqueio que segurou o briefing» são falsos para o envelope agregado | afirmação refutada; o Kimi já recuou na 1304 |
| F3 | BAIXO | Na produção atual **qualquer reserva ≥ 1 destrava a dobra**: `ç`×16.700, reserva 0 → recusa; reserva 1 → `INDEX_ONLY` aceito. O critério «a pressão vem da reserva» é só «existe reserva» | residual; aviso presente |
| F4 | MÉDIO | Sem teste do repositório para a dobra; 3 testes vermelhos obsoletos mascaram o caminho de pacote | **FALTA**: integrar `envelope/test_envelope.py` (19 testes do Codex) à suíte e consertar/aposentar os 3 |
| F5 | BAIXO | «Peça fatias por nome de arquivo» não é acionável numa chamada única; o prompt só leva o hash de geração e os nomes (pinos por documento só no recibo) | residual |
| F6 | MÉDIO | **Fora da dobra, pré-existente:** `nos_packet.build` entrega cada fonte como `body[:2400]` sem marcador no texto (só `source_prefix_truncated` no recibo); o cabeçalho diz «partial selection does not establish absence», não «prefixo» | **FALTA** marcador textual por fonte |
| F7 | INFO | A dobra **nunca foi exercida em produção**: 0 recibos `"folded": true` em `tasks.sqlite3` e nos 84 `session_requests` (os 13 acertos de `fold_notice` são prosa nos prompts do Kimi) | implantado ≠ exercido |
| F8 | PROCESSO | Edição em `Chatgpt\…`, pasta de escrita exclusiva do ChatGPT desde a ordem de 06/09, sob ordem de 20/10 19:11 [DECLARADO, sem verbatim pinado] | pedir o verbatim |

---

## 3. A descida «grep-c3» (seq 1285/1286)

[REAL] **O que reproduz.** O livro tem a cauda crescendo, mas o prefixo de **1284 registros = 3.427.185 B** (o tamanho citado) existe e dá exatamente: 254 rotas, 46 domínios, c3 = 823, c2 = 31.319, c1 = 767.724 chars, pins `052e71f9…/558296fc…/3c791151…`, custo médio 34.647, **economia 95,49 %, fator 22,2×** (`saidas/06_…`). O livro é só-acréscimo de fato. (O Kimi diz 1.283 registros; são 1.284: erro de contagem sem efeito.)

[REAL] **O que não se sustenta.**
1. **«Deriva de gabarito 12/36» é um falso negativo de formato, não deriva.** As 12 divergências são **exatamente as 12 perguntas «Quais artefatos a rota X registra (caminhos)?»**, cuja resposta congelada é uma **lista JSON de caminhos**; o teste `resposta[:60] in json.dumps(registro)` compara essa lista contra um dicionário serializado com outro escape e **nunca pode passar**. Conferindo os conjuntos: **12/12 listas congeladas = `artefatos[].caminho` vivos** (2, 5, 2, 1, 16, 2, 1, 4, 12, 2, 3, 1 = **51/51 caminhos**), em todo o histórico das rotas; as 24 respostas de texto passam 24/24. Concordância real gabarito × livro: **36/36; deriva medida: 0**. Logo o 0,6667 não mede recall, e a lição «gabarito sobre memória viva envelhece em horas» não vem desta medição (`saidas/07_…`). A descida do Kimi nunca foi falha; o instrumento é que estava errado, e o diagnóstico «uma a uma» das 12 não o viu.
2. **`hit_c2` não é grep:** é `c2_linhas.get(rota_id_do_gabarito)`. Vale como consulta por entidade nomeada só porque as 36 perguntas contêm o id literal (36/36); um grep ingênuo por sobreposição de termos da pergunta acha o alvo em top-1 em 4/36. «Zero falhas de recuperação» e «controles 6/6» (ids `zz.inexistente_NNNNNN`) são triviais por construção. O Kimi ressalvou que o recall temático não foi medido; falta ressalvar que o de entidade também é só consulta por chave.
3. **«Dobrar o acervo sobe uma oitava» / «custo cresce com o log» contradiz o modelo de custo dele:** custo = |c2| + |c1 do alvo|; |c2| é 90 % do total (31.319 de 34.647) e cresce **linear** com N; o fator satura em ~24,5× (3.022 chars por registro ÷ 123 por linha de c2). Na seq 1289 ele próprio mede que no Nós Vivo o c2 (2,05 M chars) não cabe. A descida só vira sublinear com c2 hierárquico (c3 → fatia do domínio) ou FTS, e isso não foi medido.
4. **Nós Vivo (seq 1289):** [REAL] 13.802 nós / 23.617 arestas / sha256 nativo 12.488 (90,5 %) / caminho 6.060 / 240 rotas conferem no backup do índice de 19/10; as razões 71,1× / 27,9× / 4,4× são aritmética de tamanhos de camada, não de qualidade.

---

## 4. Benchmark pré-registrado (seq 1288) e cabeçalho de confiança

### 4.1 O que o pacote v1 mede (pacote `e662b198…`, 36.206.375 B, 42 itens)
[REAL] (`saidas/08_…`):
- **Braço B com oráculo:** o harness anexa o c1 da rota-alvo escolhida pelo **gabarito** em **36/36** perguntas factuais; a resposta esperada (veredito/próximo passo) aparece **verbatim no contexto de B em 24/24** itens. B mede leitura de um registro entregue, não a descida. (O Codex chegou à mesma conclusão no adendo v2.)
- **Chave incompleta:** o `gabarito_vivo` tem `{veredito, resultado, proximo_passo, estatuto, status, titulo}` e **não tem `artefatos`**: **12/36 perguntas (um terço) não têm chave de correção**, e a premissa que justificou o «gabarito vivo» (deriva 12/36) é falsa (§3.1).
- **H2 (densidade > 5×) é aritmética de tamanhos:** A = 264.881 tok est. (único contexto, igual nas 42), B = 11.306–17.817 (média 12.456); razão 14,9–23,4×. H2 vale sempre que o nº de afirmações suportadas de B passe de **23 %** das de A (49 % se A fosse cortado a 128k). O limiar 5× foi fixado às 17:20, **13 min depois** de o Kimi registrar o fator 22,2× (seq 1286, 17:07): não é limiar vinculante.
- **H3 (citação ≥ 80 %)** compara um braço instruído a citar (B tem o cabeçalho) com um não instruído (A): mede obediência a instrução. **H5** (A excede a janela) é o tamanho do dump contra 128k/200k «de referência». **H4** (6/6 recusa): os controles são `zz.inexistente_NNNNNN` e B recebe a instrução «responde não consta» sem nenhum c1.
- **A não é truncado como o pré-registro manda:** nada o corta; e A (778.872 B com instrução) **cabe** no teto de bytes que a própria pilha usa para MiMo/Kimi (909.312). A premissa «A não cabe» depende das janelas de referência, não do respondedor sugerido.
- **Só H1 é substantiva**, e a regra não fixa procedimento inferencial: com n = 36 e diferença zero, o limite inferior conservador da fórmula do adendo v2 é ≈ −0,45, longe da margem −0,05. «TURBINA CONFIRMADA sse H1∧H2∧H4» pode ser satisfeita sem informação sobre a turbina (e o rótulo conflita com a régua; o adendo do Codex proíbe emiti-lo).
- **Fixação no livro:** a ROTA 1288 não tem `artefatos`; o pré-registro (mtime 17:21, sha `5d22e1af…`) só foi pinado pelo Codex em 21/10 10:22 (`SOURCES.json`, mesmo sha: não mudou desde então). Quem monta e audita o harness é a mesma parte (o texto do pré-registro: «kimi monta e audita o harness»).

### 4.2 Veredito B
**CONTESTA o pré-registro v1 e a corrida do pacote v1** (resultado aprovável por construção). **ASSINA o adendo v2 do Codex** (sha `0862cd56…`: B oráculo × B autônomo, A_full × A_budget, unidades-alvo fixadas por dois revisores, S/U/C, Hoeffding, guardas, `NOT_EXECUTABLE`, nunca emitir o rótulo de aprovação) **como base**, com 5 acréscimos mínimos (FALTA):
1. chave de correção para as 12 perguntas de `artefatos` (conjunto de caminhos; comparação por conjunto, não por substring) e `gabarito_vivo` regenerado com `artefatos`;
2. controles não triviais (id plausível e ausente, quase-homônimo, pergunta temática sem id) e corpus temático sem o id na pergunta, com gabarito separado do contexto;
3. limiares e função de veredito (teste, α, dados ausentes) **pinados no livro antes** de qualquer resposta, em ROTA com `artefatos` (hash do `analysis_v2.py` e do manifesto);
4. H2 reescrita sobre unidades-alvo verificadas por revisor humano ou de outra família, sem usar a razão de tamanhos como evidência; H3 só com ablação do cabeçalho (braço A com a mesma instrução);
5. o respondedor e o teto de bytes declarados no manifesto; se A_full couber, medi-lo sem truncar.

### 4.3 O cabeçalho de confiança v1 (`CABECALHO_CONFIANCA`, sha da harness `097606ee…`)
[REAL] Quatro contraexemplos:
1. **«o conteúdo é EXATAMENTE o que a casa escreveu»:** o c1/c2 é uma dobra por campo («último que escreve vence»): das 255 rotas, **146 têm `tipo` ≠ ROTA** na versão dobrada, **123 têm título diferente do registro da ROTA** e **98 linhas de c2 têm o título cortado a 110 chars**. Ex.: `infra.grep_acom_camadas` aparece como `ANOTACAO` seq 1287 com o título da anotação. O pin autentica o texto que o harness montou, não os registros do livro.
2. **«REAL > DERIVED > OPEN»:** cria escala de peso a partir de rótulo autodeclarado; a régua trata o estatuto como declaração a conferir (`[DECLARADO]`).
3. **«se não estiver nas camadas, responde não consta — a borda do acervo é o dado»:** com recuperação parcial, a borda das camadas não é a do acervo; deve ser «não consta no contexto fornecido».
4. Pins truncados a 16 hex; o cabeçalho de B mostra o pin do «gabarito vivo» (artefato do harness visível ao modelo) e só B o recebe.

### 4.4 «v2» do cabeçalho
Não existe «v2» no caderno do Kimi (a constante é única, sem versão). O único v2 é o `HEADER_V2.txt` do Codex (21/10 10:20), cujo conteúdo já corrige 1–3 (manifesto de trechos entregues, «não consta no contexto fornecido», SHA-256 atesta bytes, não verdade). **ASSINA com uma ressalva (BAIXO):** pedir ao modelo que cite o **SHA-256 completo** convida a hash fabricado (régua nº 2); citar `source_id` + intervalo e conferir o hash por script, fora do modelo.

---

## 5. Cap/ranking e critério de parada (pedido A, item 1 da ordem)

- **Kimi:** não pré-registrou nenhum dos dois; o «cap ~60 nós ≈ 50k tokens» (seq 1289) é orçamento, não critério de parada.
- **Codex:** pré-registrou **outra política** (`POLICY_PREREGISTERED_R1.json`, sha `5eb06af6…`, 21/10 10:17, antes do código das 10:20 e da instalação das 10:35): âncora exata → sobreposição de termos → diversificação por tipo → recência e grau **só como desempate final**; estatuto não entra («nunca verdade/validação»). Em produção a centralidade é sempre 0 (a tabela `nos` não tem a coluna) e a parada é só o orçamento.
- [REAL] O ranker instalado (`rank_nodes`), `saidas/05_…`: **(i)** conta tokens sem retirar palavras vazias: um nó genérico (sobreposição 9) passa à frente do nó curto no tema (5); **(ii)** ignora `estatuto` (duas linhas que só diferem no estatuto: decide a recência); **(iii)** em `nos_packet.build` descarta a ordem do `bm25` (FTS) e o piso de relevância de 40 % que o `consultar.py` do próprio Nós Vivo já usa. O teste do Codex (`RANK600`) mede velocidade e equivalência, **não qualidade**.
- **ASSINA** a decisão de não pesar por estatuto (autodeclarado) e de pré-registrar antes de codar. **FALTA:** o pedido do Kimi era recência × estatuto × centralidade; a gerência/operador decide se o estatuto vale como peso (recomendo: rótulo e filtro, nunca pontuação).
- **Proposta para pré-registro (não implantada; [DECLARADO] como proposta):** (a) ordem lexicográfica âncora → relevância normalizada (`bm25`/tf-idf sem palavras vazias) → diversidade por tipo → «última versão por rota vence, errata supersede» → grau do grafo (calculado de `arestas`); (b) parada = orçamento em **bytes UTF-8** **e** piso de relevância (40 % do melhor, como no `consultar.py` v2.1) **e** saturação (dois candidatos seguidos sem termo-chave novo da pergunta); obrigatórios (erratas, contradições, pendências, decisões) fora do cap por fechamento transitivo, overflow recusa; sempre listar omitidos recuperáveis por id; (c) teste: ≥ 30 consultas temáticas **sem id na pergunta**, gabarito separado, juiz de outra família, métrica recall@N e nDCG contra o baseline `bm25` puro, ablação de cada fator, tudo pinado no livro antes do código.

---

## 6. Manutenção de 21/10, Bancada, hipótese e vigília

### 6.1 Título da unidade F9.9 (`PROGRAMA.json.bak_20261021_kimi_titulo_f99`)
[REAL] O backup do Kimi (463.040 B, sha `c14bdcf6…`) e o próximo backup do sistema (10:12:33, 463.038 B, sha `885aba21…`) diferem em **uma linha**: `"…descida grep-ACOM de Kimi"` → `"…descida grep-c3 de Kimi"` (−2 B); 122 unidades iguais, só `F9.9.TURBINA_20261020` difere, nenhuma outra chave do quadro. **Bytes: ASSINA.** **Processo: CONTESTA.** O README do quadro diz `PROGRAMA.json` **«só pelo `iald.py`»**; a edição foi direta, sem evento (0 eventos às 09:4x em `eventos.jsonl`), e a ordem das 09:40 é [INPUT] só na boca do Kimi (sem verbatim). Uma hora antes, a rota 1303 dele registrara «não editar PROGRAMA.json … para furar o DENIED» e «Kimi NÃO contorna gate de segurança por conta própria». O gate (`\bACOM\b`) continua valendo para o resto do conteúdo; a decisão de renomear é do operador, e a pendência é o verbatim.

### 6.2 Reindexação do Nós Vivo
[REAL] `nos_vivo.sqlite3.bak_20261021_093151` (29.179.904 B, `2f6c33d8…`): índice gerado em **19/10 18:00:13**, 13.802 nós, 23.617 arestas, **sem** a unidade F9.9; `…_094237` (29.323.264 B, `7e3d2b31…`): gerado em 21/10 09:31:30, 13.910 nós, 23.774 arestas, **com** a unidade; `integrity_check` ok nos dois. **ASSINA** os bytes e o relato (21,5 s, remédio prescrito pela ferramenta). Notas: o Nós Vivo é «intocável» na lista de réguas do próprio briefing (ele reconstruiu, com backup automático e remédio prescrito); e o índice ficou 39,5 h sem reconstrução, o que é pendência de infraestrutura.

### 6.3 Bancada Um (seq 1302)
[REAL] `estado\livro.sqlite3`: 103 linhas, última **01/10 16:52**, **0** do cliente «kimi-work membro-iald», 0 depois de 20/10. A frase do `MODO_DE_USO` «gravada no livro pela própria casa» **não se sustenta** (talvez `avaliar` não seja registrado por desenho; o README diz que o livro guarda «buscas de evidência»). β em runtime, estatuto repetido e contrato B4 (19/10 17:43) conferem; o χ² 162,1296 é [DECLARADO]. **FALTA** corrigir a frase ou mostrar o registro.

### 6.4 Hipótese kilonova (seq 1301) e vigília (seq 1303)
- **1301: ASSINA.** Estatuto CONJECTURE, regra de morte simétrica a 5σ, proíbe calibrar no GW170817; θ_M = arcsin√β ≈ 6,30° confere (6,297°); o precedente «pares onda-eco falsificados» tem lastro no livro (`FALSIFIED_AT_DELAY_LAW`, seqs 245/246/255/259), com a ressalva da seq 265 (os pares «nunca foram devidos pela regra»).
- **1303: ASSINA** os bloqueios 2 (unidade fora do grafo; verificado em 6.2) e 3 (`\bACOM\b` no título; regex em `nos_packet.DENIED`). **CONTESTA o 1.º** («curado ontem pelo envelope dobrado»): ver §2.3. Seq 1304: `SYSTEM = 471` e briefing v2 = 3.377 chars **conferem**.

---

## 7. Resumo do que fica por fazer
**Do Kimi:** (1) ERRATA ao lado da 1286 (deriva refutada; 36/36) e da 1294 (falso sucesso; dobra superada pela `f95ed18e`); (2) não rodar o pacote v1; refazer o benchmark pelo adendo v2 + 5 acréscimos; (3) corrigir a frase do livro da Bancada; (4) pinar o verbatim das ordens de 19:11 e 09:40; (5) retirar a afirmação de escala log.
**Da gerência:** registrar (se concordar) o rascunho; integrar os 19 testes do Codex à suíte e consertar os 3 vermelhos (F4); marcador textual de prefixo no Nós Vivo (F6); incorporar ao `rodar_incremental` a reconstrução do índice.
**Do operador:** (a) estatuto como peso no ranking (recomendo: não); (b) dobra `INDEX_ONLY` em missão científica: permitir com aviso (hoje) ou recusar; (c) ratificar ou não as edições do Kimi em `Chatgpt\` e `PROGRAMA.json`.

---

## 8. Evidências (todas nesta pasta)
`evidencias\run_all.py` (reproduz tudo) · `make_copy.py`, `synth.py`, `run_tests.py`, `fold_cases.py`, `run_fold_cases.py`, `attach_check.py`, `run_kimi_test.py`, `rank_counterexample.py`, `check_descida.py`, `check_deriva2.py`, `check_pacote.py`, `check_manutencao.py` · saídas em `evidencias\saidas\` (`00_…` a `10_…`, `testes\`, `fold\`). Hashes dos artefatos auditados em `evidencias\sha256_dos_artefatos.json` (inclui as três versões de `canonical_memory.py`, os dois backups do quadro, os dois do Nós Vivo, o pacote e o gabarito vivo). Nenhum arquivo do Kimi, do Codex ou da produção foi alterado.
