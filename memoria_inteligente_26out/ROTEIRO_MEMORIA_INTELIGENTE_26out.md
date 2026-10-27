# ROTEIRO — O DIRETÓRIO DA MEMÓRIA VIRA SISTEMA (26/10/2026)

**Ordem do operador (26/10/2026, verbatim, sha256 `68f6824467163d4f4fa45c2ba0788e7ca2cffccef87db6842b3f77f51cece70e`, em
`work\cunhagens_13out\OPERADOR_26out_memoria_principal_so_a_gerencia_escreve_fila_subespaco_verbatim.txt`):** a inscrição na memória
principal passa a ser privilégio da gerência; todas as demais IAs depositam no subespaço da fila; a memória sobe um degrau; tudo
acontece no diretório da memória, que vira um sistema inteligente; a gerência elabora o roteiro e distribui as tarefas.

**Por que agora (medido):** em 24–26/10 o `MEMORY.md` foi escrito por quatro mãos — a gerência c1 (pós-rito), a sessão do site (linhas
«PUBLICADA»), a fila científica do Codex («Memória científica da fila vNNN») e a coordenadora do Codex (diário) — e chegou a 196 linhas,
acima do teto de 195 que o pós-rito exige; a gerência compactou três vezes em três dias. Um índice com muitos escritores não é índice.

## Os três degraus

| degrau | o que é | quem escreve |
|---|---|---|
| **L2 — o índice** `MEMORY.md` (+ `MEMORY_2.md`, o transbordo verbatim) | diz ONDE está e QUAL manda; ≤ 195 linhas, ≤ 24 000 B | **só a gerência c1**, por `memoria.py promover` (ou pelo pós-rito da cadeia de selo, que é a gerência) |
| **L1 — os arquivos-tópico** `memory\*.md` | o detalhe, com frontmatter; correção ao lado; backup de bytes | só a gerência c1 |
| **L0 — a fila** `memory\fila\depositos\<quem>\` + livro `fila.jsonl` | o subespaço de depósito de toda outra IA/sessão; só acréscimo | todos (Codex, Kimi, fila científica, sessões Claude do site/app/custódia, a própria gerência quando quiser deixar rastro) |

Acima dos três, o **vigia**: `PINO_MEMORY.json` (sha256 do `MEMORY.md`) + `memoria.py vigiar` a cada 30 min pela tarefa agendada do G1.
Alteração fora da promoção ⟹ as linhas estranhas vão **verbatim** para `fila\depositos\estranho\` e o índice volta ao pino. **Modo sombra
48 h** (só relata) → enforcement após aceite da gerência. Nada se perde, nunca: a versão estranha fica em `.bak_estranho_<ts>`.

## O sistema (`memory\fila\memoria.py`, contrato)

| operação | quem chama | o que faz |
|---|---|---|
| `depositar --quem Q --tipo T --estatuto E --alvo A --fonte F=sha --texto-arquivo X.md` | qualquer IA | grava `depositos\Q\AAAAMMDD_HHMMSS_<slug>.md` com frontmatter; linha no `fila.jsonl` (hash-chain); recusa dado pessoal/chave/`iald_stack`/`psion_state`/«só entre nós» (fail-closed, erro visível) |
| `listar [--pendentes]` | gerência | os depósitos e seus estados (PENDENTE / PROMOVIDO / ADIADO / RECUSADO) |
| `promover <id> --para <arquivo-tópico ou MEMORY.md> [--linha-indice "…"]` | **só gerência** (`MEMORIA_GERENCIA=claude-c1` no ambiente + registro de quem) | backup de bytes; append datado AO LADO no tópico; linha de índice se pedida; réguas do índice (≤ 195 / ≤ 24 000 B, transbordo verbatim ao `MEMORY_2.md`); re-pina; marca no livro |
| `adiar <id> --motivo` / `recusar <id> --motivo` | gerência | marca no livro; o depósito fica |
| `vigiar [--enforcar]` | tarefa agendada (G1) | compara `MEMORY.md` ao pino; relata (`fila\VIGIA_<ts>.json`); com `--enforcar`, move as linhas estranhas a `depositos\estranho\` e restaura o pino |
| `verificar` | qualquer | invariantes: pino bate; ≤ 195 linhas; ≤ 24 000 B; a regra dos dois arquivos; frontmatter dos tópicos; nenhum depósito editado (hash-chain íntegra) |
| `projetar` | gerência | gera `fila\PROJECAO.md` (o que está pendente, por quem, há quanto tempo) para o quadro e para o operador |

Desenho herdado do **Mapa de Rotas** (`C:\IALD\MAPA_DE_ROTAS\rotas.py`: livro só-acréscimo com cadeia de hash, correção ao lado) e da
**memória ACOM** (`C:\IALD\MEMORIA_IALD`: inscrição imutável, delta, recibo). A fila NÃO substitui nem a ACOM nem o Mapa: é o degrau de
entrada do índice da gerência.

## A distribuição das tarefas

| # | tarefa | quem | quando | aceite |
|---|---|---|---|---|
| 1 | regra no índice (1 linha em «Ler primeiro»), `fila\README.md`, pastas, `PINO_MEMORY.json` | gerência c1 | **feito 26/10** | — |
| 2 | regra nas memórias globais: bloco datado no `~/.claude/CLAUDE.md` (todas as sessões Claude) e no `~/.codex/AGENTS.md` (Codex), com backup de bytes | gerência c1 | 26/10 | operador lê |
| 3 | construir `memoria.py` (contrato acima) + testes (depositar, promover com as réguas, vigiar detecta linha estranha, verificar, hash-chain) | agente Sonnet (código médio) | 26/10 | revisor independente (Opus) antes de ligar o vigia |
| 4 | **ORDEM 026** ao Codex: a fila científica e toda sessão Codex deixam de escrever no `MEMORY.md`; depositam em `fila\depositos\codex-*`/`fila-cientifica`; recibo em `DO_CHATGPT\ORDEM_026` | Codex (coordenadora + gerente TGL) | enfileirada 26/10 | gerência confere o próximo sync científico (v402) |
| 5 | Kimi: no próximo handoff da sessão do site, a instrução de depositar em `fila\depositos\kimi\` (hoje ele não escreve no índice) | sessão do site → Kimi | próximo handoff | gerência |
| 6 | sessões Claude do site/app/custódia: as linhas «PUBLICADA» dos handoffs passam a depósito em `fila\depositos\claude-site\`; a gerência promove | sessão do site (lê a regra no índice) | a partir de 26/10 | gerência |
| 7 | vigia agendado: tarefa `IALD_memoria_vigia` a cada 30 min (lição dos caminhos com espaço: `schtasks-caminhos-com-espaco-24out.md`), modo sombra | gerência c1, após o item 3 | 26–27/10 | 48 h de sombra sem falso positivo |
| 8 | enforcement (restauração automática) | gerência c1 | após o item 7 | operador informado |
| 9 | o pós-rito da cadeia de selo passa a promover pela `memoria.py` (mesma regra; a gerência continua sendo quem escreve) | preparador da v402+ | v402 | exame final |

## O que NÃO muda

A régua inteira (backup de bytes, correção ao lado, hash lido do arquivo, nunca verbatim do que o operador reservou); a memória ACOM
e o Mapa de Rotas seguem como estão; o Atlas continua «à mão NUNCA se toca» fora do append do pós-rito; a casa do Escritório não entra.
