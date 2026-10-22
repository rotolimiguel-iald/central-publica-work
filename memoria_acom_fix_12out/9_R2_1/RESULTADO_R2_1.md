ACOM R2.1 — 13/10

# Conserto ACOM 12/10, R2.1: os achados da revisão independente R2 (K2, K3, K4, K6, passo 8, heartbeat, N1, N2, N3)

Construtor: subagente da gerência c1, 13/10/2026. Base conferida por script antes de tocar: `CANDIDATO_MANIFESTO_R2.json`
`1dd4a837bd33dc40`, `implantar.py` `f2c9b3facc91500f`, `reverter.py` `7c12615545382ac7`, `implantacao_lib.py`
`928118ee223976c3`, `implantar_config_producao.json` `52ae2d489e6c7c0c`, `REVISAO_R2.md` `13e8287d5b5e0ff7`.
Escrevi só em `9_R2_1\`. Estatutos: [REAL] medido aqui · [DERIVED] deduzido do código ou de medida · [OPEN] · [INPUT].

## Veredito em uma linha

**R2.1 PRONTO PARA A DECISÃO DO OPERADOR** [REAL nas cópias]: os 6 consertos pedidos estão no código, cada um com teste que
FALHA no R2 e PASSA na R2.1; a suíte inteira da R2.1 dá **259 de 259 PASSA** (as 235 do revisor + 24 novas); o ensaio de
implantação e reversão com processos simulados fecha os 10 cenários (K1a, K1b2, K1c, K1d, K2, K3, K4, K5, K6, P8). Nada
foi rodado em produção.

## 1. O que mudou (3 arquivos do candidato + as 3 ferramentas)

| arquivo | sha16 R2 → R2.1 | conserto |
|---|---|---|
| `MEMORIA_IALD\lib\iald_memory\guard.py` | `bdb82e165c8d6987` → `0a49de819f89b4d5` | N1, N2, N3 (§2.5) |
| `MEMORIA_IALD\session_memory.py` | `5faa2ae2cf8abb5c` → `ca5409aa8359cf08` | N3: lê pelo `guard.read_checked` (mesmos códigos de erro) |
| `projetos_pyhton\IALD\iald_web_server.py` | `f687697a93eac214` → `68698c9583efac1c` | heartbeat: nova tentativa nos `os.replace`/`os.remove` (§2.4) |
| `implantar.py` | `f2c9b3facc91500f` → `b913952cb2592b84` | K2, K3, passo 8 |
| `reverter.py` | `7c12615545382ac7` → `b6e3906baa88a7e5` | K4, K2 (recibo com carimbo), `--config`, `--forcar-reinicio` |
| `implantacao_lib.py` | `928118ee223976c3` → `c72ddd0a5686a4e0` | K6, recibos pendentes, `ReinicioPendente`, `estado_real`, simulador sem engano por pid reaproveitado |

Os outros 12 arquivos do candidato são byte a byte os do R2. Os sha256 completos estão em `CANDIDATO_MANIFESTO_R2_1.json`
(`f7ccb802d2388ac3`, campo `r2_1_mudancas`) e em `MANIFESTO_R2_1.json`.

## 2. Os consertos

1. **K2 — recibo nunca sobrescrito; trava de implantação anterior** [REAL]. O recibo agora tem carimbo
   (`RECIBO_IMPLANTACAO_<carimbo>.json`; o dry-run também) e nunca é sobrescrito. O primeiro passo, `trava_recibo_anterior`,
   lê as pastas de recibo (a da R2.1 e, por `recibos_dirs_anteriores`, a do R2): uma implantação REAL que mudou algo, ou que
   foi morta no meio (`EM_CURSO`), ou que concluiu, e que não tem `RECIBO_REVERSAO` real `REVERTIDA` citando o seu carimbo
   (ou caminho) **recusa** a nova execução antes de tocar em qualquer coisa: status `RECUSADA_RECIBO_ANTERIOR_NAO_REVERTIDO`,
   com o comando de reversão do recibo pendente em `acao_requerida`. Recibo ilegível também recusa. Ensaio K2: a 2ª
   execução foi recusada, o recibo da 1ª ficou byte a byte igual, o reverter com o recibo indicado deu `REVERTIDA`, e um
   dry-run depois passou na trava.
2. **K4 — o reverter não religa sobre estado misto** [REAL]. Novo passo `conferir_alvos` (sempre roda, mesmo sem o passo 4
   no recibo) confere os 15 alvos contra o original; a conferência se repete logo antes de religar. Se QUALQUER passo falhou
   ou um alvo diverge, o app NÃO é religado (`reiniciar_app` = `NAO_EXECUTADO`), a tarefa fica desabilitada e o recibo traz
   `acao_requerida` (remover a causa e rodar de novo; `--forcar-reinicio` só por decisão explícita). Além disso, nenhum passo
   de restauração roda se o reverter não conseguiu parar o app (no R2 a restauração seguia com o app vivo). Ensaio K4: com o
   web server preso, `FALHOU_EM_restaurar_arquivos`, app parado (0 supervisor, 0 web), tarefa desabilitada; solto o arquivo,
   o 2º reverter deu `REVERTIDA`, 15 alvos no original, banco = original, app de volta com o store v1.
3. **K3 — a tarefa volta se e só se esta execução a desabilitou** [REAL]. `restaurar_tarefa` usa o registro
   `tarefa_desabilitada_por_esta_execucao`; uma tarefa desabilitada pelo operador nunca é reabilitada (teste de controle).
   O recibo descreve a tarefa e os processos LIDOS (`estado_real`) e não diz mais «nada mudou» quando a tarefa foi
   desabilitada. Ensaio K3: `FALHOU_EM_parar_app`, tarefa reabilitada, recibo honesto («a tarefa FOI desabilitada por esta
   execução e foi reabilitada; o app pode ter ficado PARCIALMENTE parado»). Leitura que fiz do pedido [INPUT para a
   gerência]: depois de uma falha COM mudança iniciada (passos 3–7) a tarefa continua desabilitada **por desenho** (o app não
   volta sozinho sobre estado misto; o reverter a reabilita); o recibo diz isso.
4. **K6 e heartbeat — nova tentativa curta e limitada** [REAL]. Ferramentas: `com_nova_tentativa` em todo `os.replace` de
   recibo e de arquivo e na remoção do tempário (20 ms dobrando até 500 ms; recibos até 30 s, demais até 10 s); depois a
   falha sobe, visível e sem tempário órfão. Heartbeat (`_heartbeat_retry`, até `HEARTBEAT_REPLACE_RETRY_S` = 3 s, 10 ms
   dobrando até 200 ms) nos `os.replace` do psion, da cópia diária, do health e da rotação da telemetria, e
   `_heartbeat_discard_temp` remove o tempário de uma troca que falhou. O psion segue opaco: só as trocas foram envolvidas;
   nada do arquivo de estado real foi lido. Ensaio K6: um leitor segurou o recibo 2 s no meio do passo 4 e a implantação
   CONCLUIU (15 arquivos); no K1a o harness leu o recibo 338 vezes durante a execução sem abortá-la.
   **O `3 != 1`** [REAL, `runs\s3c_copia_r2.json` e `runs\s3c_copia.json`, teste original sem alteração]: no R2, 1/30
   sequencial e 12/60 com o varredor concorrente (`3 != 1`, `'psion_error' != 'ok'`, `PermissionError` 5/32); na R2.1, 0/30
   e **0/60 falhas do teste** com o varredor (1.287 aberturas). Na R2.1 ficaram 6/60 erros só no `tempfile.cleanup()` do
   tearDown da FIXTURE (o varredor externo ainda segura um arquivo quando o teste apaga o seu tempdir): o corpo do teste
   passou nas 60 (`runs\diag_s3c_copia.json` com os tracebacks completos). O teste novo HB5 faz as 60 batidas com o varredor
   dentro do processo: todas `ok`, 1 evento, sem tempário.
5. **Filtro (guard.py)** [REAL].
   - N2: as regras de nome rodam sobre um esqueleto do nome (NFKC, caracteres de formato removidos, casefold, homóglifos
     cirílicos/gregos e travessões Unicode mapeados, acentos fora; NFKC sozinho não mapeia o `ѕ` cirílico). Radicais
     `iald?psion?state` e `iald?stack?v` em qualquer posição; `.env`, `.envrc`, `env`, `*.env`, `*.env.<x>`, `*.env_<x>`,
     sufixo `~`. Exceção mantida pela suíte da frente 3: `envelope.env.txt` (cauda com extensão de documento/código) segue
     aceito. `central.env` com senha/AKIA sintéticos: recusado, nada no banco.
   - N1: remoção de sufixos de backup LINEAR, com a mesma decisão do laço do R2 (3.000 nomes aleatórios): nome de 32 KB
     4,5 ms (R2: 1,30 s); `path_reason` 32 KB 19 ms (R2: 2,59 s); `read_allowed_file` 32 KB 20 ms (R2: 2,61 s).
   - N3: `guard.read_checked` abre o HANDLE antes de checar (leitura, SEM `FILE_SHARE_DELETE`), confere contagem de
     links, identidade e o caminho FINAL desse handle, e só então lê do MESMO handle. Troca ativa x.json ↔ hardlink do
     psion sintético por 12 s: R2 leu o canário 140 vezes; R2.1, 0 (844 recusas `hardlink`). Achado do próprio teste: um
     primeiro rascunho com handle só de atributos ainda leu o canário 13 vezes (handle sem acesso a dados não entra na
     checagem de compartilhamento, e o link foi removido entre o open e a contagem); corrigido para handle de leitura.
6. **Passo 8 lento ≠ falha** [REAL]. Se o comando de início foi aceito e há processo do app vivo mas a saúde não chegou em
   `esperar_inicio_s`, o passo fica `AGUARDANDO_REINICIO`, o recibo `CONCLUIDA_AGUARDANDO_REINICIO` (saída 3) e a ação diz
   «NÃO reverter… conferir». Se o reinício falha de verdade depois da verificação final, o recibo diz que a implantação foi
   verificada e manda diagnosticar antes de reverter. Ensaio P8: saúde atrasada 8 s com prazo de 3 s → `CONCLUIDA_
   AGUARDANDO_REINICIO`, sem mandar reverter; 10 s depois o app estava saudável.

## 3. Medidas [REAL] (detalhe em `TESTES_R2_1.md` `28bbd0d186e6e42f`)

- Suíte inteira R2.1 (`copia\`, guarda da auditoria, Python 3.14.3, sem rede, sem provedor): **259/259 PASSA**, 2 bloqueios
  da guarda, ambos `BLOCK_NETWORK` (a sonda IPv6 do urllib3, como no revisor). Rodada final em
  `runs\suite_completa_r2_1_final_stdout.txt`; resultado em `copia\testes_r2\RESULTADOS_TESTES.json`.
- Os 24 testes novos na cópia do R2 (candidato e ferramentas R2): **20 FALHAM, 4 passam** (os controles); na R2.1, 24/24.
  O controle `test_T_K4_good_reversal_restarts` falha no R2 só porque confere o carimbo citado no recibo de reversão, que é
  da R2.1.
- Ensaio (`runs\s5_ensaio_r2_1.json`): K1a, K1b2, K1c, K1d, K2, K4, K5 e K6 terminam `REVERTIDA` com os originais
  idênticos, banco igual ao original, lib v1 lendo o banco e o app de volta com o store v1 `2d4f6214`; K3 e P8 como acima.
  O R2 nesses cenários é o do revisor (`8_REVISAO_R2\runs\s5_ensaio_*.json`), não refeito.
- `DIFF_R2_R2_1.patch` (`fbf1990188955854`, 25.670 B, 3 arquivos): `git -c core.autocrlf=false apply` sobre uma cópia do
  candidato_r2 reproduz os 15 arquivos da R2.1 byte a byte (`DIFF_R2_R2_1_APPLY_CHECK.json` `204eb00d49d93d46`). O patch
  não contém a chave; na prova o `iald_web_server.py` entrou redigido dos dois lados (a chave está fora de todo trecho do
  patch e é a mesma nos dois candidatos, conferido por script).

## 4. Comandos para o operador (atos do operador; janela quieta da §5 do REVISAO_R2.md vale igual)

0. Fechar as sessões Claude Code/Codex que hospedam os MCPs `iald-orchestrator`/`bancada-um`; não rodar `session_memory.py`
   durante a janela.
1. **Dry-run** (só lê: trava de recibos, CAS dos 15 alvos, banco, tarefa e processos). Exigir `"status": "DRY_RUN_OK"`:

   `python -X utf8 "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\implantar.py" --config "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\implantar_config_producao_r2_1.json" --dry-run`

2. **Implantar** (sem mover os backups legados agora). Exigir `"status": "CONCLUIDA"`; se vier
   `CONCLUIDA_AGUARDANDO_REINICIO` (saída 3), NÃO reverter: conferir `/login` e a tarefa em alguns minutos:

   `python -X utf8 "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\implantar.py" --config "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\implantar_config_producao_r2_1.json" --pular-mover-backups`

3. **Reverter** (se algo falhar; o implantar imprime o caminho exato do recibo e a ação). Com `--config` o reverter acha a
   única implantação pendente; com mais de uma, ou nenhuma, recusa e pede `--recibo`:

   `python -X utf8 "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\reverter.py" --config "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_1\implantar_config_producao_r2_1.json"`

   ou, com o recibo impresso: `python -X utf8 "…\9_R2_1\reverter.py" --recibo "…\9_R2_1\recibos_producao_r2_1\RECIBO_IMPLANTACAO_<carimbo>.json"`.
   Se o reverter devolver `FALHOU_*`, o app fica PARADO (não religa sobre estado misto): remover a causa e rodar o mesmo
   comando de novo. Rodar o implantar de novo antes de reverter agora é recusado pela própria ferramenta.
4. Depois, com o app v2 no ar, mover os backups legados com o script INSTALADO (dry-run primeiro), como na §5.4 do
   REVISAO_R2.md.

A config `implantar_config_producao_r2_1.json` (`66f8caea867e91e1`) é a do R2 com: candidato `9_R2_1\candidato_r2_1\C`,
manifesto `CANDIDATO_MANIFESTO_R2_1.json`, recibos em `9_R2_1\recibos_producao_r2_1` (criada pelo implantar), e
`recibos_dirs_anteriores` = `4_INTEGRACAO\recibos_producao_r2` (hoje só tem o dry-run do R2: a trava não acusa nada,
conferido por leitura). `aplicar_blocos.py` (`9c86bcc996922653`) e `SESSION_BRIDGE_v2.md` (`cf1ed9e2ff847e20`) continuam
os de `4_INTEGRACAO\ferramentas`, inalterados.

## 5. O que NÃO fiz, e o que resta

- **Nada em produção**: não toquei `C:\IALD\MEMORIA_IALD`, `C:\IALD\projetos_pyhton\IALD`, a tarefa agendada, processos reais
  nem `D:\IALD_ARQUIVO`; não rodei `implantar.py`/`reverter.py` contra a config de produção, nem em dry-run. Sem rede, sem
  provedor. Leituras fora da pasta [REAL, guarda]: as suítes herdadas abrem em `mode=ro` o índice canônico do orquestrador
  (67 aberturas, como no revisor) e leem `__pycache__` e módulos de apoio do app; nenhuma leitura do banco ACOM nem de
  confidencial. Os `.env` reais e o psion real não foram abertos; tudo foi sintético.
- **Desvio deliberado**: não executei o `init`/`transition` da memória ACOM do CLAUDE.md global (escreveria no banco de
  produção, contra a regra desta tarefa). Mapa de rotas: consultado antes (`programa.memoria_acom.conserto_delta_12out`
  existe); o registro sai em `registro_mapa_F9.MEMORIA_ACOM_R2_1.json` para a gerência registrar.
- **Chave**: o `iald_web_server.py` de `candidato_r2_1` carrega a chave de produção (é o que se instala; o `.gitignore` da
  Central exclui `**/iald_web_server*`, conferido). Nas cópias de teste, no ensaio e na prova do patch ela está redigida.
  Não publicar `work\memoria_acom_fix_12out`.
- **N3, o que resta** [DERIVED]: (a) quem tem direito de RENOMEAR o arquivo confidencial (não só de criar link) pode
  movê-lo para um nome benigno com um só link; o guard não lê conteúdo para reconhecê-lo — mas esse processo já pode ler o
  arquivo direto; (b) o caminho do APP (`agi_validate_path` → `protected_path`) ainda checa e depois abre por nome: não
  converti o web server para `read_checked` (fora do pedido; ficou só no `session_memory`); (c) em sistemas de arquivos
  sem identificador ou sem `GetFinalPathNameByHandle` (rede, `NUL`) a leitura é recusada, não aceita.
- **N2, o que resta** [INPUT D4]: regras de CONTEÚDO para senha, JWT, AKIA, PEM e chave partida não foram acrescentadas
  (a decisão D4 segue aberta); a regra de nome cobre `central.env` e variantes.
- **Cmdlets reais** do Agendador (`Disable/Stop/Enable/Start-ScheduledTask`) seguem nunca exercitados [OPEN]; tudo foi
  pelo backend simulado. No K3 com o web vivo e o supervisor morto, a ferramenta reabilita a tarefa mas não relança nada:
  o recibo sugere `stop_iald_web.ps1` e depois `Start-ScheduledTask`.
- **Simulador**: o ensaio achou um falso «app vivo» por pid reaproveitado pelo Windows (arquivo `pids\*.json` antigo); o
  `ProcessosSim` agora confere a hora de criação do processo. Só o backend simulado mudou; o de produção lista por linha de
  comando.
- Os ganhos e os riscos de escala da v2 (instantâneo do banco inteiro por hora, ~8,6 GB/dia para D:) não mudaram: são da
  decisão D1-B [INPUT], fora da R2.1.
- Não refiz: as 235 do revisor contra o R2, os ataques A/B originais, o ensaio K1–K6 contra o R2.

## 6. Artefatos (sha256 por script em `MANIFESTO_R2_1.json`)

`candidato_r2_1\C` (15) · `CANDIDATO_MANIFESTO_R2_1.json` · `implantar.py` · `reverter.py` · `implantacao_lib.py` ·
`implantar_config_producao_r2_1.json` · `DIFF_R2_R2_1.patch` + `DIFF_R2_R2_1_APPLY_CHECK.json` · `TESTES_R2_1.md` ·
`src_r2_1\` (testes novos) · `scripts\` (edições, cópias, s3c, s4, s5, geradores) · `runs\` (resultados) ·
`registro_mapa_F9.MEMORIA_ACOM_R2_1.json`. Cópias regeráveis: `copia\` (R2.1), `copia_r2\` (R2), `ensaio\`, `ref_r2\`
(as 3 ferramentas R2, byte a byte).
