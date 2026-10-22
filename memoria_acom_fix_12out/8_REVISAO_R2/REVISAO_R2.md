REVISOR ADVERSARIAL c1: conserto ACOM R2

Subagente da gerência c1, independente de quem construiu e de quem revisou o R1. Medido em 13/10/2026, 07:08–07:45
(hora local). Escrevi só em `C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\8_REVISAO_R2\`. Estatutos:
[REAL] medido aqui · [DERIVED] deduzido do código ou de medida · [DECLARADO] afirmado pelo integrador e não refeito
aqui · [OPEN] · [INPUT] decisão da gerência ou do operador.

## Veredito em uma linha

**PODE_IMPLANTAR_COM_RESSALVAS.** Os quatro achados bloqueantes do R1 estão corrigidos [REAL]. Achei defeitos novos só
nos caminhos de falha (K2, K3, K4, K6), no filtro (N1, N2, N3) e no heartbeat (a causa do `3 != 1`). Nenhum deles
mexe no caminho feliz. Dois exigem cuidado do operador se algo der errado: não rodar o implantar de novo antes de
reverter (K2) e desligar o app à mão se o reverter falhar (K4). O procedimento está na §5.

## 0. Base e método

- Hashes conferidos por script [REAL]. Todos iguais aos citados: `CANDIDATO_MANIFESTO_R2.json` `1dd4a837bd33dc40`,
  `DIFF_R2.patch` `19814b492cd16f3d`, `DIFF_R1_R2.patch` `dcbf148a80c5d9ac`, `implantar.py` `f2c9b3facc91500f`,
  `reverter.py` `7c12615545382ac7`, `implantacao_lib.py` `928118ee223976c3`, `implantar_config_producao.json`
  `52ae2d489e6c7c0c` e `RECIBO_IMPLANTACAO_dry_run.json` `c904d4b5b7334ed7`.
- `DIFF_R2.patch` aplicado por mim sobre `originais\` reproduz o candidato em 15 de 15 arquivos [REAL]
  (`runs\s7_diffcheck.json`). Precisa de `git -c core.autocrlf=false`: esta máquina tem `core.autocrlf=true`, e com ele
  13 arquivos saem em CRLF. Isso não afeta a implantação, que copia bytes do candidato.
- Os relatórios das revisões A e B **não estão em disco**: só os scripts e os resultados. Li a lista dos bloqueantes
  em `RESULTADO_INTEGRACAO_R2.md` §1–§5 e na errata do R1 (linha 201). Para a B, examinei também as observações que o
  R2 classificou como não bloqueantes (t1, t2, t3/D, t3/E, t3/G e t5).
- Chave embutida: o `iald_web_server.py` do candidato carrega uma chave de API do Google (1 ocorrência, 39
  caracteres; nunca impressa). Ela também está em `originais\` e nas cópias de teste da integração. Nas minhas cópias
  (suítes, ensaio, diffcheck) ela foi **redigida** por um marcador do mesmo tamanho, e o manifesto do ensaio recebeu o
  sha recalculado só dessa linha. O `.gitignore` da Central exclui `**/iald_web_server*` [REAL, `git check-ignore`].
- Produção: só metadados (§4.10). Não toquei o banco, a tarefa, processos de produção ou `D:\IALD_ARQUIVO`. Não rodei
  `implantar.py` nem `reverter.py` contra a config de produção, nem em dry-run. Não chamei provedor e não usei rede.
- Desvio deliberado: não executei o `init`/`transition` da memória ACOM que o CLAUDE.md global pede. Eles escreveriam no
  banco de produção, contra a regra desta tarefa [INPUT].

## 1. Os achados bloqueantes do R1: estão corrigidos?

| achado | ataque original contra o R2 [REAL] | formas novas [REAL] | situação |
|---|---|---|---|
| **A1** reversão não cobria implantação parcial | O E6 e os cenários C/F do integrador já cobrem falha dentro da ferramenta. Refiz por morte dura (TerminateProcess) em quatro pontos (tabela da §2.2): K1a (1º arquivo em `backup_ok`, com tempário a meio da troca), K1b2 (8º arquivo em `backup_ok`), K1c (no passo 5, com o `aplicar_blocos.py` filho órfão) e K1d (na migração `--apply`, com o filho órfão). Morte do **reverter** no passo 2 seguida de novo reverter (K5). Todos: `REVERTIDA`, originais idênticos, banco = sha original, lib v1 lê o banco e o app volta pela tarefa com o store v1 `2d4f6214` | **K2, K3, K4, K6** (§2.2): o reverter religa o app sobre estado misto quando falha (K4) ou quando o recibo foi sobrescrito (K2); falha no `parar_app` deixa a tarefa desabilitada (K3); um leitor do recibo aborta a implantação (K6) | **CORRIGIDO** como especificado. Restam defeitos nos caminhos de falha (ressalvas) |
| **A2** ReDoS no filtro D4 | E7 (`a:/`×32.000): **0,018 s** (era 43,3 s). E7b (4.000 caminhos, 240 KB): **0,042 s** (era 71,2 s). B/F (200 k): 0,035–0,038 s | **N1**: o laço que remove sufixos de backup do NOME é quadrático no comprimento do caminho pedido. `'a'+'.bak'×8000` (32 KB) custa 1,28 s, e 48 KB com `.bak_1` custam 2,44 s; pelo `session_memory` (init com `objective_file` desse caminho), 32 KB custam **4,09 s**; a razão é ≈4 a cada dobra. O `agi_validate_path` do web server chama `protected_path` sobre caminho vindo de ferramenta do modelo | **CORRIGIDO** no `scan_text`. N1 é ressalva (baixa): é um processo de CLI ou uma thread de pedido, fora da trava do banco |
| **A3** gestão de processos e Tarefa Agendada | O controle A do integrador reproduz o perigo. No ensaio (backend simulado do próprio R2), a tarefa é desabilitada antes de parar, e há 0 relançamentos nas janelas paradas de K1–K6 | **K3**: se o stop script não derrubar o app em `esperar_parada_s`, o `parar_app` falha DEPOIS do `Disable` → a tarefa fica **desabilitada**, o supervisor está morto e o filho web segue vivo, e o recibo diz «nada mudou e o app não foi parado por esta execução» (falso) | **CORRIGIDO** no código e no simulador. Os cmdlets reais nunca foram exercitados [OPEN, como o integrador declara]. K3 é ressalva |
| **B1** `session_memory.py` lia confidencial no `write_reference` e devolvia campos | t3/C literal: `ProtocolError source_path_not_allowed:psion_name`, **arquivo não aberto** (gancho de auditoria) | **N5**: `IALD_PSION_STATE_r2.json`, `…json.bak_20261013`, `.env.r2ref` e `r2.pem` como `write_reference` são todos recusados sem abrir; a referência legítima é criada, reusada (igual) e serve ao `project`. **N3** (TOCTOU): o guard checa nome, realpath, `st_nlink` e identidade, e só DEPOIS abre por nome. Com uma thread trocando `x.json` entre arquivo comum e hardlink para um `iald_psion_state_SYN.json` sintético, **184 leituras devolveram o canário** (contra 2.143 recusas `hardlink`) em 20 s. **N4**: oráculos menores (contagem de chaves e «too_large» de um JSON qualquer) | **CORRIGIDO**. N3 é ressalva baixa: exige um processo local correndo contra o guard, que poderia ler o arquivo direto |
| B, t3/E (colisão de caixa) | `%43tx%43ase.events.jsonl` e `ctxcase.events.jsonl` são diários distintos; os dois `verify` ok | Nomes reservados do Windows (`nul`, `com0`, `lpt0`) com extensão gravam normalmente neste Windows 11 [REAL]; o `_ID` exige alfanumérico no início, então não há colisão com o prefixo `_` | CORRIGIDO |
| B, t1/t2/t3/D (lacunas de nome e conteúdo, não bloqueantes no R2) | Iguais ao R1: lidos `iald_psion_ѕtate.json` (homóglifo), `iald‐psion‐state.json`, `copia_iald_psion_state_32B.json`, `.env~`, `server.key~` e `env.bak_iald`; sem regra: chave partida, base64, JWT, PEM, AKIA, senha | **N2**: um arquivo `central.env` (o nome do arquivo real `backend\central.env` que a B listou) passa no nome; o `init` o lê e grava no banco senha, JWT e AKIA sintéticos [REAL, sandbox]. `prod.env`, `app.env.local` e `secrets.env~` também passam | ABERTO por decisão [INPUT] (D4). Recomendo a regra `*.env` e `*.env.*` antes de abrir a memória a mais casas |
| B, t3/G (diário antes do commit) | Igual: a linha do diário existe antes do commit | A revisão A (e3) já mostrou que a linha órfã de uma morte é anulada na transição seguinte | Aceitável |

## 2. Suítes e ensaio

### 2.1 Suítes (cópia em `8_REVISAO_R2\copia\testes_r2`, guarda da auditoria, Python 3.14.3)

- As 28 cópias de arquivos «candidato» na suíte são byte-iguais ao `candidato_r2` [REAL] (`runs\s0_montar_copia.json`).
  A suíte do heartbeat roda sobre o store v2 `b213498d`; o comentário do `hb_fixture.py` que fala em «lib v1
  congelada» está desatualizado.
- **Rodada 1: 235 testes, 234 PASSA, 1 ERRO** [REAL]. O erro é `test_filters.test_escritorio_path_variants_refused
  (folder='Escritório')`: o `os.rename` da própria fixture (pasta recém-criada → `Escritório`) levou
  `WinError 5`. Não é do produto; é o mesmo fenômeno de compartilhamento da §3. A guarda registrou 168 processos e 2
  bloqueios, os dois `BLOCK_NETWORK ('::1', 0)` (sonda IPv6 do urllib3), como na integração.
- **Rodada 2: 235 testes, 235 PASSA, 0 FALHA** [REAL] (`runs\s1_RESULTADOS_rodada2.json`). Guarda: 152 processos, 2
  bloqueios (os mesmos `BLOCK_NETWORK` IPv6), nenhum outro. O teste do heartbeat passou nas duas rodadas da suíte;
  a intermitência só apareceu na repetição da §3.
- As suítes da FILA abrem em `mode=ro` o índice da memória canônica do orquestrador (67 aberturas, herdado do
  integrador) e importam 7 módulos de apoio instalados do app. **O banco ACOM de produção não foi aberto.**

### 2.2 Ensaio adversarial de implantação e reversão (cópia sintética; `scripts\s5_ensaio.py`)

As ferramentas são as do R2, byte a byte. O banco v1 é sintético, gerado pelo `store_v1_frozen`. Os processos são
reais, mas rodam pelo backend simulado do R2 (agendador com RestartCount/IgnoreNew/Disabled, supervisor com mutex e
web). Por cima vai a guarda da auditoria, mais um gancho de lentidão em `os.rename` para conseguir matar no meio.

| cenário | o que acontece [REAL] | resultado |
|---|---|---|
| K1a morte no passo 4, 1º arquivo em `backup_ok` | Recibo `EM_CURSO` sem `acao_requerida`, tempário órfão `CORE.md.tmp_*`, banco v2, app parado, tarefa desabilitada | reverter `REVERTIDA`; tempário → `.removido_`; identidade; banco = original; app volta com o store v1 |
| K1b2 morte com o 8º arquivo (`iald_web_server.py`) em `backup_ok` | 7 substituídos, tempário órfão | `REVERTIDA`, identidade |
| K1c morte no passo 5 (filho `aplicar_blocos.py` órfão termina sozinho) | Os 15 são candidato e os blocos foram aplicados | `REVERTIDA`, blocos restaurados, identidade |
| K1d morte na migração `--apply` | O filho órfão morreu (banco segue v1 e igual ao original) | `REVERTIDA` (banco `PULADO`, v1) |
| K5 morte do reverter no passo 2, depois novo reverter | 9 alvos ainda candidato, app parado, tarefa desabilitada | 2º reverter `REVERTIDA`, identidade |
| K6 um leitor segura o `RECIBO_IMPLANTACAO.json` por 2 s no meio do passo 4 | O `os.replace` do recibo falha, e a implantação **aborta** com 5 arquivos trocados. O recibo em disco fica `EM_CURSO`, com o 5º arquivo em `pendente` e sem `acao_requerida` (o stdout tinha a ação) | o reverter recupera tudo (o arquivo novo em `pendente` presente vira `.removido_`). **Ressalva**: falha espúria, e o recibo em disco não diz o que fazer |
| K1b (primeira tentativa) | A implantação falhou sozinha no passo 4 porque o meu harness lia o recibo a cada 20 ms: é o K6 sem querer | Mesma causa do K6 |
| **K2** falha no passo 4 (alvo preso; 14 trocados), depois o operador **roda o implantar de novo** | A 2ª execução falha na pré-conferência (os arquivos novos já existem), mas antes **sobrescreve `RECIBO_IMPLANTACAO.json`** (`recibo_1_sobrescrito: true`). O reverter com o recibo novo dá `restaurar_arquivos PULADO` (e não confere os 15 alvos), `restaurar_banco FALHOU` («banco em v2 e sem backup integral registrado»), e **religa o app** por WMI com a tarefa **desabilitada** | **Estado final misto e no ar**: 14 alvos candidato + 1 original, banco v2, web com o store R2, tarefa desabilitada. Os `.bak_` e o `pre_v2` continuam no disco, então a recuperação manual é possível; a automática se perdeu. **Ressalva forte** |
| **K3** o stop script não derruba o app (só o simulador muda) | `FALHOU_EM_parar_app`, `tarefa_desabilitada_por_esta_execucao: true`. Depois: tarefa desabilitada, supervisor 0, web 1 (v1). O recibo diz «nada mudou e o app não foi parado» | **Ressalva**: a tarefa fica desabilitada sem aviso |
| **K4** implantação `CONCLUIDA`, depois reverter com `iald_web_server.py` preso | `FALHOU_EM_restaurar_arquivos` (`WinError 32`), banco `NAO_EXECUTADO`, blocos restaurados, **app religado** sobre: store, journal, snapshots, migrate e o web server v2 + `__init__`, app_memory, session_memory, policy e operational_memory v1 (guard.py removido) + banco v2. **A lib mista lê o banco v2** (rc 0). A docstring do reverter diz que «num estado misto a memória recusa visivelmente»: aqui **não recusa** | O 2º reverter (lock solto) dá `REVERTIDA` com identidade. **Ressalva**: entre os dois, o app roda um código misto não revisado, e o que gravar se perde na reversão do banco |

Achado de leitura [DERIVED]: se só o passo 8 falhar (o web demora mais de `esperar_inicio_s` = 180 s para ficar
saudável), o recibo manda rodar o reverter e diz «app PARADO e tarefa agendada DESABILITADA». Nesse ponto a tarefa
já foi reabilitada e iniciada. Uma implantação boa pode ser revertida por engano: antes de reverter, confira o app.

## 3. A intermitência do heartbeat (`test_sixty_beats_in_process_zero_or_one_memory_event`, `3 != 1`)

- **Reproduz sem injeção** [REAL] (`runs\s3c_heartbeat_repeticao.json`): **2/30** execuções sequenciais e **1/60** com
  8 em paralelo, sempre `AssertionError: 3 != 1`. Com um «varredor» que abre (rb, 30 ms) cada arquivo novo do TEMP do
  teste, como faria um antivírus ou indexador, foram **27/30**. Nesse caso aparecem também `'psion_error' != 'ok'` e
  `PermissionError WinError 5/32` no `os.replace` do health.
- **Causa** [REAL no mecanismo, DERIVED na atribuição] (`runs\s3_heartbeat_injecao.json`): uma falha transitória de
  compartilhamento no `os.replace(tmp, psion)` de `_save_psion_state` (outro processo com o arquivo aberto sem
  `FILE_SHARE_DELETE`). A batida vira `psion_error`, com classe `falha` → +1 evento. A batida seguinte volta a `ok` →
  mudança de classe → +1 evento. Total 3. A injeção F1 (`os.replace` do psion falha 1×) e o leitor real F4 (sem mock)
  dão **exatamente +2**. A hipótese do integrador (o `health_load` devolve `{}`) dá **+1** (`2 != 1`) e não explica o
  `3`. No teste não há leitor concorrente no processo; quem segura o arquivo é externo (provavelmente o antivírus em
  tempo real ou o indexador; não verifiquei, por isso [DERIVED]).
- **Efeito em produção** [DERIVED]: raro. O `get_status` lê o psion e o health sob o mesmo `_heartbeat_lock`; o risco é
  de leitor externo. Por incidente: 2 eventos a mais na memória comum, a atualização EMA daquela batida perdida e um
  **tempário órfão com a cópia dos bytes do psion** (`iald_psion_state_32B.json.tmp_*`) no diretório do app, porque o
  `_save_psion_state` não remove o tempário quando a troca falha. Uma falha no `_heartbeat_health_save` depois do
  evento gravado sobe do ciclo (o `_beat` captura e reagenda), e o evento se repete na batida seguinte.
- **Conserto sugerido**: nova tentativa curta em `PermissionError` nos `os.replace` do psion, do health e da rotação
  da telemetria; remover o tempário quando a troca falha. Não bloqueia: o sentido do erro é gravar a mais, nunca perder.

## 4. O que o operador precisa saber antes de rodar

1. **Parada do app.** Com `--pular-mover-backups`, a janela vai do passo 1 ao 8: silêncio de 10 s, duas cópias de
   357 MB (C: e D:), migração (11 s num banco de 357 MB, revisão B t6 [REAL lá]), troca de 15 arquivos, blocos, verify
   deep e reinício, que espera até 180 s. Estimo 1–4 min [DERIVED]. **Sem** a opção, o passo 6 move 774 backups,
   95,8 GB: cópia, conferência e remoção, cerca de 3× esse volume em E/S. Pela vazão C→C de 265 MB/s da revisão A, são
   +10–25 min com o app parado [DERIVED]. Recomendo `--pular-mover-backups` e mover depois, com o app v2 no ar: o
   arquivador só toca `memory.sqlite3.bak_*`, que a v2 não cria.
2. **Tarefa agendada.** `Disable/Stop/Enable/Start-ScheduledTask` nunca rodaram de verdade [OPEN]. Se o `Disable`
   falhar, nada muda (seguro). Se o app não parar a tempo (K3), a tarefa fica desabilitada: conferir com
   `Get-ScheduledTask -TaskName 'IALD Web Server'` e reabilitar à mão. Se só o passo 8 falhar, esperar e conferir
   `http://127.0.0.1:8082/login` antes de pensar em reverter.
3. **MCPs e sessões.** Há 5 processos MCP do orquestrador vivos (iniciados entre 12/10 20:58 e 13/10 06:33) e 8 da
   bancada [REAL, só pid, horário e padrão casado; linha de comando não impressa]. O `operational_memory` importa a
   `iald_memory` sob demanda. Quem já importou a lib v1 **falha fechado** (`Unsupported or missing memory schema`) até
   reiniciar [REAL no código e no teste de integração]. Quem já carregou o `operational_memory` v1 mas ainda não a lib
   vai pegar a lib v2 do disco: código misto, com o filtro antigo `FORBIDDEN` [DERIVED]. **Fechar as sessões Claude
   Code/Codex antes, ou reabri-las logo depois.** Uma sessão que grave pela v1 entre o backup (passo 2) e a migração
   (passo 3) entra na migração, mas some numa reversão: daí a **janela quieta** (a produção ainda grava: o banco passou
   de 357.412.864 B no dry-run para 357.433.344 B às 07:21, e os backups de 777 para 779 [REAL]).
4. **Contexto `1bcf55a4-06fe-5e57-a2ad-640f2de13b53`** (IALD/operator, rev. 3): depois da implantação, `get` e
   `project` são recusados (`escritorio_path`); `verify` e `transition` seguem. Uma sessão que o use verá a recusa. O
   destino é decisão do operador [INPUT].
5. **Disco.** C: tem 934 GB livres e D: 2,10 TB [REAL]. O `pre_v2` fica em 2 cópias no C: (a do implantar e a da
   migração) e 1 no D:, 357 MB cada. Os backups legados agora são 779, com 97,6 GB [REAL]. **Crescimento da v2**: o
   instantâneo é o BANCO INTEIRO e sai na primeira mutação depois de 60 min. Contei no sandbox: 24 mutações horárias
   dão **24 instantâneos** (3 locais + 21 arquivados) [REAL]. Como os eventos legados não encolhem o banco, são 357 MB
   × 24 ≈ **8,6 GB/dia para D:**, sem poda (a especificação §3.2 já estima isso: cerca de 7 meses de D:) e cerca de 1,1
   GB fixo no C:. Cada instantâneo custa 0,8–2,3 s dentro da trava de escrita (revisão B t6). A saída é a opção D1-B
   (compactar) ou uma retenção em D: [INPUT].
6. **Primeira batida depois do reinício**: 90 s após o start ela grava **1 evento** (classe estabelecida). Isso vale
   com o llama ONLINE (`ok`) e também OFFLINE: `skipped_offline` conta como classe `falha`. Depois o limite é 1/h com
   classe estável. Cada evento horário dispara um instantâneo de 357 MB (item 5). A verificação 7b só discrimina com
   janela de mais de 30 min e o llama online.
7. **Recibos.** Não abra `RECIBO_IMPLANTACAO.json` nem `RECIBO_REVERSAO.json` durante a execução: K6 mostrou que um
   leitor aborta a implantação no meio. Depois de qualquer falha, **copie o recibo para outro nome antes de qualquer
   coisa** e **nunca rode o `implantar.py` de novo antes de reverter** (K2).
8. **Se o reverter devolver `FALHOU_*`**, ele já terá religado o app sobre estado misto (K4). Pare o app na hora
   (`Disable-ScheduledTask` + `stop_iald_web.ps1`), remova a causa (arquivo preso etc.) e rode o reverter de novo: o 2º
   reverter fecha (K4, K5).
9. **Chave embutida**: o candidato e as cópias da integração carregam a chave do web server de produção. Não publicar
   `work\memoria_acom_fix_12out`; o git já ignora `**/iald_web_server*`.
10. **Produção agora** [REAL, 07:31, `runs\s8_producao_metadados.json`]: CAS dos 15 alvos ok, 6 superfícies iguais ao
    dry-run, sem `-journal`, `D:\IALD_ARQUIVO` inexistente.

## 5. Veredito e passos

**PODE_IMPLANTAR_COM_RESSALVAS.**

Passos (atos do operador; os caminhos são os de produção do R2):

0. Janela quieta: fechar as sessões Claude Code e Codex que hospedam os MCPs `iald-orchestrator`/`bancada-um`, e não
   rodar `session_memory.py` durante a janela. O llama pode ficar como está.
1. **Dry-run** (só lê; refaz o CAS com a produção de agora):
   `python -X utf8 "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\4_INTEGRACAO\implantar.py" --config "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\4_INTEGRACAO\implantar_config_producao.json" --dry-run`
   Exigir `"status": "DRY_RUN_OK"`.
2. **Implantar** (sem mover os 95,8 GB agora):
   `python -X utf8 "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\4_INTEGRACAO\implantar.py" --config "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\4_INTEGRACAO\implantar_config_producao.json" --pular-mover-backups`
   Não abrir o recibo enquanto roda. Exigir `"status": "CONCLUIDA"`.
3. Conferir: `/login` 200, `Get-ScheduledTask -TaskName 'IALD Web Server'` habilitada e rodando, e repetir a
   `7_VERIFICACAO` contra o `RECIBO_IMPLANTACAO.json` real, com janela de mais de 30 min e o llama online. Reabrir as
   sessões.
4. Depois, com o app no ar, mover os backups legados com o script INSTALADO (primeiro o dry-run):
   `python -X utf8 C:\IALD\MEMORIA_IALD\mover_backups_antigos.py --state C:\IALD\MEMORIA_IALD\state --dest D:\IALD_ARQUIVO\MEMORIA_IALD\backups_ate_20261012 --keep 3 --dry-run`
   e o mesmo comando sem `--dry-run`.
5. Se algo falhar: copiar o recibo para outro nome e rodar
   `python -X utf8 "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\4_INTEGRACAO\reverter.py" --recibo "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\4_INTEGRACAO\recibos_producao_r2\RECIBO_IMPLANTACAO.json"`
   (o `--dry-run` antes é opcional). Nunca o `implantar.py` de novo. Se o reverter falhar, aplicar o item 8 da §4.

Para tirar as ressalvas antes de rodar, um R2.1 pequeno [recomendação; decisão da gerência]:

1. o `implantar.py` recusa começar se já existe um `RECIBO_IMPLANTACAO.json` de execução real (ou passa a usar recibo
   com carimbo);
2. o `reverter.py` sempre confere os 15 alvos (mesmo sem o passo no recibo) e **não religa** o app se algum passo de
   restauração falhou (opção `--forcar-reinicio`);
3. o `apos_falha` reabilita a tarefa quando foi esta execução que a desabilitou, e a mensagem do passo 8 passa a dizer
   o estado real;
4. nova tentativa em `PermissionError` no `write_json_atomic` dos recibos e nos `os.replace` do heartbeat;
5. no guard: regra `*.env`/`*.env.*`, remoção de sufixo linear (ou teto de comprimento do caminho) e abrir antes de
   checar (`os.fstat` no handle: `st_nlink` e identidade) para fechar o N3.

## 6. Artefatos (sha256 por script em `runs\MANIFESTO_REVISAO_R2.json`)

- Scripts: `scripts\s0_montar_copia.py`, `s2_montar_revisores.py`, `s3_heartbeat_injecao.py`,
  `s3c_heartbeat_repeticao.py`, `s4_ataques_novos.py`, `s5_ensaio.py` e `s8_producao_metadados.py`.
- Resultados: `runs\s1_RESULTADOS_rodada1.json` e `_rodada2.json`, `s3_heartbeat_injecao.json`,
  `s3c_heartbeat_repeticao.json`, `s4_ataques_novos.json`, `s5_ensaio_rodada1_K1a_K1b_K1c.json`,
  `s5_ensaio_K1d_K2_K3_K4_K5_K6_K1b2.json`, `s6_snapshot_horario.json`, `s7_diffcheck.json` e
  `s8_producao_metadados.json`; os resultados dos revisores rodados contra o R2 ficam em `rev_a\exp\runs\` e
  `rev_b\testes\`.
- Registro para o mapa: `registro_mapa_F9.MEMORIA_ACOM.json`. A rota `programa.memoria_acom.conserto_delta_12out`
  **não existe** no mapa: é preciso registrar a ROTA antes deste RESULTADO.
