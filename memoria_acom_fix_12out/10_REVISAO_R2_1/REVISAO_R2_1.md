REVISOR ADVERSARIAL c1: conserto ACOM R2.1

Subagente da gerência c1, independente de quem construiu a R2.1 e de quem revisou o R2. Medido em 13/10/2026, entre
08:50 e 09:20 (hora local). Escrevi só em `C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\10_REVISAO_R2_1\`.
Estatutos: [REAL] medido aqui · [DERIVED] deduzido do código ou de medida · [DECLARADO] afirmado pelo construtor e não
refeito aqui · [OPEN] · [INPUT] decisão da gerência ou do operador.

## Veredito em uma linha

**PODE_IMPLANTAR_COM_RESSALVAS.** Os nove achados da revisão R2 estão corrigidos no caminho que foi pedido [REAL]. O
patch reproduz a R2.1, a suíte dá 259/259 na minha cópia, o `3 != 1` sumiu em 180 execuções com varredor concorrente,
e os cenários K2, K3, K4, K6 e P8 refeitos fecham. Achei defeitos novos só em formas que ninguém tinha testado: um status
`REVERTIDA` enganoso (K4c), o K3 do lado do reverter (K3r), uma forma nova de N1 e as fronteiras de projeto do filtro
(N2/N3). Nenhum mexe no caminho feliz. O operador precisa de três cuidados, listados na §6.

## 0. Base e método

- Hashes lidos por script [REAL] (`runs\s1_manifesto_patch.json`). Todos iguais aos citados: `RESULTADO_R2_1.md`
  `f0f4637f39e131c8`, `CANDIDATO_MANIFESTO_R2_1.json` `f7ccb802d2388ac3`, `implantar.py` `b913952cb2592b84`,
  `reverter.py` `b6e3906baa88a7e5`, `implantacao_lib.py` `c72ddd0a5686a4e0`, `implantar_config_producao_r2_1.json`
  `66f8caea867e91e1`, `DIFF_R2_R2_1.patch` `fbf1990188955854`, `REVISAO_R2.md` `13e8287d5b5e0ff7` e `TESTES_R2_1.md`
  `28bbd0d186e6e42f`.
- Minha cópia da suíte é independente da do construtor. Ela parte da cópia do revisor R2, já redigida. Troquei os 28
  arquivos de papel «candidato» pelos do `candidato_r2_1`, com a chave redigida, e conferi os 28 contra a origem
  [REAL] (`runs\s2_montar_copia.json`). Contra a cópia do construtor, 124 arquivos são iguais. Só diferem o `rodar.py`
  (o título) e dois JSON de evidência gerados pelos testes.
- O ensaio usa o script do construtor (`9_R2_1\scripts\s5_ensaio_r2_1.py`). Ele adapta o `s5_ensaio.py` do revisor R2,
  e li o diff inteiro antes de usar: só mudam os caminhos, os recibos com carimbo e o atraso de saúde do P8. As entradas
  vêm de `9_R2_1`, e as saídas e a guarda (`ACOM_AUDIT_ROOT`) ficam em `10_REVISAO_R2_1`. As ferramentas foram copiadas
  byte a byte, com o sha conferido no preparo. Gerador: `scripts\s5_gerar.py`. Cenários novos: `scripts\s5_extra.py`.
- Chave: o `iald_web_server.py` do candidato tem 1 chave de produção, nunca impressa. Em todas as minhas cópias ela está
  redigida. Uma varredura por script achou 0 arquivos da minha pasta com a chave de produção [REAL]. Os testes trazem
  fichas `FAKE_*` sintéticas de propósito.
- Produção: só metadados (§5). Não rodei `implantar.py` nem `reverter.py` contra a config de produção, nem em dry-run.
  Não fiz `init`/`transition` no ACOM, por ordem desta tarefa. É desvio deliberado do protocolo do CLAUDE.md global,
  porque esses comandos escreveriam no banco de produção. Sem rede e sem provedor. Mapa de rotas consultado antes: a rota
  `programa.memoria_acom.conserto_delta_12out` existe e está `EXAMINADA_COM_DEFEITO`.

## 1. Manifesto e patch [REAL] (`scripts\s1_manifesto_patch.py`)

| conferência | resultado |
|---|---|
| 15 arquivos do `candidato_r2_1` contra o manifesto R2.1 (sha256 e bytes) | 15/15 |
| arquivos na árvore R2.1 | 15, nenhum fora do manifesto |
| mudados contra o `candidato_r2` | 3: `guard.py`, `session_memory.py` e `iald_web_server.py`, iguais a `r2_1_mudancas`. Os outros 12 são byte a byte os do R2 |
| `candidato_r2` em disco contra o `CANDIDATO_MANIFESTO_R2.json` (`1dd4a837bd33dc40`, citado pelo R2.1) | 15/15 |
| `git -c core.autocrlf=false apply` sobre a cópia do `candidato_r2` (web server redigido dos dois lados) | rc 0, **0 diferenças** nos 15 |
| o mesmo com `core.autocrlf=true` (o padrão desta máquina) | rc 0, mas `guard.py` e `session_memory.py` saem diferentes (CRLF). Não afeta a implantação, que copia os bytes do candidato |
| chave no patch | ausente. A chave é a mesma nos dois candidatos |

Ressalva documental (baixa): o campo `ferramentas` do manifesto ainda cita o `aplicar_blocos.py` do R1
(`df08a17e7cc71f40`). O arquivo em `4_INTEGRACAO\ferramentas` é `9c86bcc996922653`, como diz o RESULTADO §4. O
`implantar.py` não confere esse campo; o BLOCOS_RECIBO grava o sha real. Também está desatualizado o comentário do
`_guarded_read` no `session_memory.py`: ele fala em «handle (attributes only)», mas o guard abre com leitura. É só
texto.

## 2. Suíte inteira na minha cópia [REAL] (`runs\s2_*`)

- **Rodada 1: 259 testes, 258 PASSA, 1 ERRO.** O erro é `test_filters.test_escritorio_path_variants_refused
  (folder='Escritório')`: o `os.rename` da própria fixture levou `WinError 5`. É o mesmo erro de fixture que o revisor R2
  teve na rodada 1 dele.
- **Rodada 2: 259 testes, 259 PASSA, 0 FALHA** (`runs\s2_RESULTADOS_rodada2.json`). Guarda: 3 bloqueios por rodada,
  todos `BLOCK_NETWORK ('::1', 0)` (a sonda IPv6 do urllib3). Leituras fora da pasta: o índice canônico do orquestrador
  em `mode=ro` (67) e o `__pycache__` de módulos de apoio do app, como nas revisões anteriores. Nenhuma leitura do
  banco ACOM nem de confidencial.

## 3. Heartbeat: o `3 != 1` e os erros de tearDown [REAL] (`scripts\s3_heartbeat.py`, `s3_hb_um.py`)

Rodei o teste ORIGINAL `test_sixty_beats_in_process_zero_or_one_memory_event`, sem alteração e sem injeção, na minha
cópia, 4 em paralelo, com um varredor externo que abre (`rb`, sem `FILE_SHARE_DELETE`) cada arquivo novo do tmp. Cada
execução separa o veredito do CORPO do veredito do tearDown pelo TestResult na entrada do tearDown e pelo traceback.

| cópia | varredor | n | ok | falha no corpo | `3 != 1` | só tearDown |
|---|---|---|---|---|---|---|
| R2.1 | 30 ms por arquivo | 120 | 116 | **0** | **0** | 4 |
| R2.1 | 150 ms por arquivo (forma nova) | 60 | 60 | **0** | **0** | 0 |
| controle R2 (mesmo detector, web server do R2 redigido) | 30 ms | 60 | 53 | 7 | 3 | 5 |

- **O `3 != 1` sumiu em 180 execuções com varredor concorrente.** O controle mostra que o detector acha a falha quando
  ela existe.
- **Os erros de tearDown são de fixture.** Os tracebacks param todos em `tearDown → tempfile.cleanup()`, com
  `PermissionError WinError 32` num arquivo que o varredor ainda segura. O corpo terminou sem nenhuma falha registrada.
  Em produção ninguém apaga a pasta de logs.
- Lapso meu, corrigido: o primeiro detector lia `_outcome.success` dentro do tearDown, e o executor do tearDown reinicia
  esse campo para True. O controle R2 o denunciou com 0 falhas de corpo. Troquei pela contagem do TestResult e refiz as
  duas rodadas, R2.1 e controle. Os números acima são os da versão corrigida.

## 4. Cenários de implantação e reversão [REAL] (`runs\s5_ensaio_rev_principal.json`, `runs\s5_ensaio_rev_CFG.json`)

Ferramentas R2.1 byte a byte, backend de processos simulado, banco v1 sintético e guarda ligada. Todos os cenários
terminam com os originais idênticos, o banco igual ao original, a lib v1 lendo o banco e o app de volta com o store v1
`2d4f6214`. A exceção é onde a tabela diz outra coisa.

| cenário | o que acontece | leitura |
|---|---|---|
| **K2** (refeito) | 1ª execução `FALHOU_EM_substituir_arquivos` (14 candidato + 1 original). A 2ª dá `RECUSADA_RECIBO_ANTERIOR_NAO_REVERTIDO` e o recibo 1 fica intocado. O reverter com o recibo indicado dá `REVERTIDA`, e o dry-run depois passa na trava | corrigido |
| **K2b** recibo RENOMEADO à mão (`.json.lido`) | a trava não o vê (lê `RECIBO_IMPLANTACAO*.json`). Mas a 2ª execução falha em `pre_conferencias` ANTES de tocar em nada: os arquivos novos da v2 existem sem original conhecido. `reverter --config` acha 0 pendentes e recusa | não piora o estado. A recuperação pede `--recibo` com o arquivo renomeado |
| **K2c** recibo APAGADO à mão | igual ao K2b: a 2ª execução falha fechada, sem tocar | recuperação automática perdida. Os `.bak_` e o `pre_v2` seguem no disco [REAL] |
| **K2d** recibo truncado | a 2ª execução é `RECUSADA` («recibo ilegível»). `reverter --config` recusa | fail-closed |
| **K3** (refeito) | `FALHOU_EM_parar_app`, tarefa reabilitada. O recibo não diz «nada mudou». Estado lido: web v1 vivo, sem supervisor | corrigido |
| **K3b** stop sem efeito + `Enable-ScheduledTask` falha | recibo: «a reabilitação FALHOU: reabilite à mão», com `acao_sugerida` | honesto |
| **K3r** implantação CONCLUIDA; o REVERTER encontra o stop sem efeito | `FALHOU_EM_parar_app`, nada restaurado, conferência com 15 divergentes, sem religar. Estado real: **web v2 vivo e saudável, sem supervisor, tarefa DESABILITADA**. O recibo diz «Ele fica parado e a tarefa agendada desabilitada» | **ressalva**: o K3 foi corrigido no implantar, não no reverter. O app v2 (estado coerente) fica sem relançamento e a frase do recibo é falsa. Um reverter normal depois fecha |
| **K4** (refeito) | web server preso: `FALHOU_EM_restaurar_arquivos`, app NÃO religado. O 2º reverter dá `REVERTIDA` | corrigido |
| **K4b** alvo travado em modo exclusivo só depois de `conferir_alvos` OK | a conferência final levanta `Permission denied`: `FALHOU_EM_reiniciar_app`, app parado, a trava ainda vê a implantação pendente. O 2º reverter dá `REVERTIDA` | correto. Detalhe: `acao_requerida` fica `null` nesse caminho |
| **K4c** alvo MODIFICADO (bytes do candidato) depois de `conferir_alvos` OK | **status `REVERTIDA`, rc 0, `"ok": true`, `falhas: []`**, mas `app_religado: false`, 1 alvo no candidato e `acao_requerida` dizendo que não religou. **A trava do implantar passa a ver 0 pendentes** | **ressalva**: o `reiniciar_app` devolve `NAO_EXECUTADO` sem entrar em `falhas`, então o status final mente. O 2º reverter fecha |
| **K6** (refeito) | leitor segura o recibo 2 s no meio do passo 4: `CONCLUIDA` (15) | corrigido |
| **K6b** leitor segura um ALVO (CORE.md) 2,5 s no início do passo 4 | `CONCLUIDA` (15) | a nova tentativa cobre também os alvos |
| **K6c** leitor segura o recibo 40 s (acima do teto de 30 s) | `FALHOU_EM_substituir_arquivos` visível, recibo coerente (5 substituídos), ação = reverter, sem tempário órfão. O reverter fecha | falha visível, como prometido |
| **P8** (refeito) | saúde 8 s atrasada, prazo de 3 s: `CONCLUIDA_AGUARDANDO_REINICIO` (rc 3), «NÃO reverter». Saudável 10 s depois | corrigido |
| **P8b** o web v2 morre ao nascer (supervisor vivo relançando) | também `CONCLUIDA_AGUARDANDO_REINICIO` (rc 3) com «NÃO reverter… só se o app v2 não subir, diagnosticar» | por desenho. **O operador precisa saber que a saída 3 também cobre um app v2 em laço de queda** |
| **CFG** os comandos da §4 na forma positiva | dry-run `DRY_RUN_OK` → implantar `CONCLUIDA` → `reverter --config --dry-run` (só lê; app intocado) → `reverter --config` acha a única pendente e dá `REVERTIDA` → `reverter --config` de novo recusa (0 pendentes) → dry-run passa na trava | os comandos funcionam como escritos |

[DERIVED, não medido] Se a 1ª implantação falhar depois da migração mas antes de criar qualquer arquivo novo (por
exemplo, no 1º alvo) e o recibo for APAGADO, a 2ª execução passa a pré-conferência. Ela pula o backup integral («banco
já em v2») e conclui. A reversão do recibo 2 então não teria `pre_v2` registrado. É erro de operador, coberto pela regra
«nunca apagar recibo».

## 5. Filtro: N1, N2, N3 [REAL] (`scripts\s4_ataques.py`, `runs\s4_ataques.json`)

O registro de identidades do guard foi apontado para o sandbox: zero stat em produção, e o psion sintético conta como o
real contaria.

**N1 (custo).** As formas do revisor R2 e as novas no nome são todas lineares. Dobrar o tamanho multiplica o tempo por
cerca de 2 (`.bak`, `~` e `.env`).

| forma (32 KB, salvo indicação) | R2.1 |
|---|---|
| `'a'+'.bak'×8000` (do revisor) | 4,6 ms |
| `'a'+'.bak_1'×8000` (48 KB) | 9,4 ms |
| `'~'×32000`, `'.bak~'×6400`, `'.env'×8000`, `'.tmp_x'×5000`, ligatura `ﬃ`×32000, `ѕ` cirílico ×32000 | 3,5–13 ms |
| **caminho com 16.000 componentes** (`a\` repetido), `path_reason` / `read_allowed_file` / `dispatch init` | **2,83 s / 3,73 s / 3,68 s** |

Forma nova que resta: o custo está no `os.path.realpath` do stdlib, que sobe componente a componente quando o caminho não
existe. É quadrático no número de componentes: 2.000 → 0,056 s, 8.000 → 0,60 s, 16.000 → 2,83 s. Afeta a CLI e o
`agi_validate_path` do app, que chama `realpath` antes do guard. A gravidade é baixa, da mesma classe do N1 do R2: um
processo de CLI ou uma thread de pedido, fora da trava do banco. O conserto é um teto de comprimento do caminho antes do
`realpath`.

**N2 (nomes).** Os casos foram testados pela via do app (`realpath` + `path_reason`, como no `agi_validate_path`) e pela
via do `session_memory` (`read_checked`).

| forma nova | app | session_memory |
|---|---|---|
| `.ENV`, `env` (sem ponto), `CENTRAL.ENV`, `central.ｅｎｖ` (largura total), `central.env.json`, `central.env.1` | recusa | recusa |
| `central.env ` (espaço no fim), `central.env.` (ponto no fim) | recusa (o realpath normaliza) | recusa (nome resolvido) |
| ADS `central.env::$DATA`, `.env::$DATA`, `server.key::$DATA`; `chave.pem ` | recusa pelo nome resolvido | recusa (`resolved:`) |
| ADS nomeado `notas.txt:central.env` | recusa | recusa |
| nomes curtos 8.3: `IALD_P~1.JSO` (psion), `ENVRC~1` (.envrc), `CENTRA~1.ENV` | recusa (o realpath expande) | recusa |
| **`central.env.txt`** (a exceção de projeto do `envelope.env.txt`) | aceita | **lido; senha sintética no banco** |
| **ADS nomeado `notas.txt:oculto`** (conteúdo confidencial num stream de arquivo benigno) | aceita | **lido; senha sintética no banco** |

Os dois aceitos são da classe «nome benigno com conteúdo confidencial», que nenhuma regra de nome pega. O remédio são
as regras de CONTEÚDO (senha, JWT, AKIA, PEM), ainda abertas na decisão D4 [INPUT]. O stream ADS é invisível no
Explorer, mas é a mesma classe.

**N3 (troca ativa, 12 s cada).**

| forma | leituras do canário | leitura |
|---|---|---|
| hardlink x.json ↔ psion sintético, pelo `session_memory` | **0** em 29.503 (3.401 recusas `hardlink`) | **corrigido** |
| **renomear** o psion sintético para x.json e de volta, pelo `session_memory` | **551** em 7.451 | passa, como o construtor declarou |
| hardlink, pela via do APP (`agi_validate_path` e depois `open` pelo nome) | **40** em 17.136 | resíduo declarado pelo construtor: o app não usa `read_checked` |
| renomear, pela via do app | 2.386 em 9.216 | idem |
| renomeado de forma persistente / CÓPIA (controle) | lidos | o guard por nome nunca pegou cópia |
| symlink | não criado (`WinError 1314`, sem privilégio) | não testável aqui |

**Gravidade do renomeio: baixa.** Equivale a copiar o arquivo para um nome benigno, e o controle mostra que a cópia
também passa. Exige direito de renomear na pasta do confidencial, e quem tem esse direito já lê o arquivo direto. O
resíduo que pesa mais é a via do app: o modelo escolhe o caminho, e quem faz a troca é um processo local.

## 5b. Produção, só metadados [REAL, 08:57] (`runs\s8_producao_metadados.json`)

- CAS dos 15 alvos ok. As 5 superfícies de instrução são iguais às do dry-run do R2. O `MEMORY.md` mudou, como era de
  esperar: o `aplicar_blocos` só exige uma linha `- Memória ACOM:`, no máximo 200 linhas e 24.000 B. Hoje ele tem 188
  linhas e 18.928 B (18.996 B depois da troca). **Folga de 12 linhas**: o dry-run imediatamente antes acusa se estourar.
- O banco tem 357.490.688 B e mtime 08:53: a produção segue gravando. Sem `-journal`. São 785 backups legados (99,8 GB).
  `D:\IALD_ARQUIVO` não existe. C: tem 918 GB livres e D: 2,10 TB.
- A pasta `9_R2_1\recibos_producao_r2_1` ainda não existe. A trava R2.1 leria hoje **0 pendentes e 0 ilegíveis** (em
  `recibos_producao_r2` só há o dry-run do R2). `python` resolve para `C:\Python314\python.exe` (3.14.3).

## 6. Os comandos da §4 do RESULTADO e o que o operador precisa saber

Os comandos estão **corretos**: caminhos e opções existem, e a forma positiva foi exercitada no cenário CFG. Eles estão
**incompletos** em quatro pontos:

1. **Falta o passo de conferência depois de implantar.** Ele está na §5 do REVISAO_R2, não na §4 do RESULTADO: `/login`
   200, `Get-ScheduledTask -TaskName 'IALD Web Server'` habilitada e rodando, a `7_VERIFICACAO` repetida contra o recibo
   real com janela de mais de 30 min e o llama online, e as sessões reabertas.
2. **O comando de mover os backups não está escrito.** A §4 remete à §5.4 do REVISAO_R2, que é:
   `python -X utf8 C:\IALD\MEMORIA_IALD\mover_backups_antigos.py --state C:\IALD\MEMORIA_IALD\state --dest D:\IALD_ARQUIVO\MEMORIA_IALD\backups_ate_20261012 --keep 3 --dry-run`,
   e o mesmo sem `--dry-run`, com o app v2 no ar.
3. **Os comandos da §5 do REVISAO_R2 apontam para `4_INTEGRACAO\implantar.py` (as ferramentas e o candidato R2) e estão
   SUPERADOS.** Usar só os da §4 do RESULTADO_R2_1. A trava R2.1 lê os recibos do R2, mas o implantar R2 não lê os da
   R2.1.
4. Ao critério «exigir `CONCLUIDA`» e «se o reverter devolver `FALHOU_*`» falta acrescentar: **depois de reverter,
   exigir `REVERTIDA` E `app_religado: true` E `acao_requerida: null`** (por causa do K4c). Se a saída da implantação for
   3, conferir `/login` em alguns minutos: a saída 3 também cobre um v2 em laço de queda (P8b).

O que o operador precisa saber antes de rodar:

- **Janela quieta**: fechar as sessões Claude Code/Codex que hospedam `iald-orchestrator` e `bancada-um`, incluindo a
  sessão da gerência. Quem já importou a lib v1 falha fechado até reiniciar.
- Rodar o **dry-run imediatamente antes** e exigir `DRY_RUN_OK`. Ele pega CAS, banco, espaço e o limite do `MEMORY.md`.
- **Nunca renomear, apagar ou editar um recibo** (K2b/c/d). Para guardar uma cópia, copiar para FORA da pasta de
  recibos [DERIVED do código]. Uma cópia dentro dela, com o prefixo `RECIBO_IMPLANTACAO`, conta como segunda pendente,
  e o `reverter --config` recusa até se usar `--recibo`.
- Se o reverter falhar no `parar_app` (K3r), o app v2 pode continuar NO AR com a tarefa desabilitada, ao contrário do
  que o recibo diz. Conferir `Get-ScheduledTask` e os processos. Depois, ou reverter de novo (removida a causa), ou
  reabilitar a tarefa.
- Os cmdlets reais do Agendador seguem nunca exercitados [OPEN]. Tudo aqui passou pelo backend simulado.

## 7. Veredito

**PODE_IMPLANTAR_COM_RESSALVAS.**

Nenhum achado novo bloqueia: todos ficam em caminhos de falha raros ou em fronteiras de projeto já nomeadas (D4).
Recomendações para um R2.2 pequeno, decisão da gerência:

1. `reverter.reiniciar_app`: quando não religa por alvo divergente, entrar em `falhas` (status `FALHOU_EM_reiniciar_app`
   ou `REVERTIDA_SEM_RELIGAR`), para a trava continuar vendo a implantação pendente (K4c). No caminho de exceção,
   preencher `acao_requerida` (K4b).
2. `reverter.parar_app`: o mesmo conserto K3 do implantar. Reabilitar a tarefa se ESTA execução a desabilitou e a
   parada falhou, e escrever o estado lido, não «fica parado» (K3r).
3. `guard`: teto de comprimento do caminho antes do `realpath` (N1 por componentes). Converter o `agi_validate_path`
   para `read_checked` ou reabrir por handle (N3 na via do app).
4. Textos: o campo `ferramentas` do manifesto e o comentário do `_guarded_read`.

## 8. Artefatos (sha256 por script em `MANIFESTO_REVISAO_R2_1.json`)

Scripts: `scripts\s1_manifesto_patch.py`, `s2_montar_copia.py`, `s3_heartbeat.py`, `s3_hb_um.py`, `s4_ataques.py`,
`s5_gerar.py`, `s5_extra.py`, `s5_ensaio_rev.py` (gerado) e `s8_producao_metadados.py`. Resultados:
`runs\s1_manifesto_patch.json`, `s2_montar_copia.json`, `s2_RESULTADOS_rodada1.json`, `s2_RESULTADOS_rodada2.json`,
`s2_suite_rodada*_stdout.txt`, `s3_heartbeat.json`, `s3_heartbeat_controle_R2.json`, `s4_ataques.json`,
`s5_ensaio_rev_principal.json`, `s5_ensaio_rev_CFG.json` e `s8_producao_metadados.json`. Cópias regeráveis:
`suite_r21\` (a suíte e as ferramentas), `ensaio\` e `sb_ataques\` (só sintético). Não refiz: os 24 testes contra a
cópia do R2 (o «20 falham no R2» é [DECLARADO]) e o ensaio K1a–K1d/K5.
