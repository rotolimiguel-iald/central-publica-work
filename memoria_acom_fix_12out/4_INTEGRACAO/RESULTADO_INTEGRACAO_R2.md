INTEGRAÇÃO R2: conserto ACOM 12/10, achados bloqueantes da revisão de 13/10

Integrador (subagente da gerência c1), segunda volta. Escrevi só em
`C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\4_INTEGRACAO\`. O R1 continua intacto ao lado: `candidato\`,
`CANDIDATO_MANIFESTO.json`, `DIFF.patch`, `testes\`, `ensaio_implantacao\` e `RESULTADO_INTEGRACAO.md`. As versões R1
dos scripts que a R2 reescreveu ficaram como `*.bak_r1_20261013_060656` (e `ferramentas\aplicar_blocos.py.bak_r1_20261013_062835`),
cópias de bytes. Estatutos: [REAL] medido aqui · [DERIVED] · [DECLARADO] · [INPUT] decisão da gerência · [OPEN].

Não fiz nada em produção. A conferência só-leitura do fim (`r2_producao_somente_leitura.py`, saída em
`evidencias_r2\PRODUCAO_R2_LEITURA.json`) deu `producao_intocada: true` [REAL]: os 9 alvos estão byte-iguais aos originais
congelados, os 6 novos não existem, as 5 superfícies ainda têm o bloco antigo no topo, `state` não tem `journal\`,
`snapshots\` nem `pre_v2`, e `D:\IALD_ARQUIVO` não existe. Não chamei nenhum provedor, não usei rede (nem a porta 8082),
não rodei script de selo nem `um.py` e não abri nenhum confidencial. O único arquivo com nome de psion que os testes tocam é
SINTÉTICO, foi criado pelo próprio teste, e o teste prova que o código não o abre.

Ordem do operador [REAL, sha16 `78ef70e6f9868281`]: «resolva a questão da memória». Decisões D1–D6 [INPUT].

## 0. Resumo

| o quê | resultado [REAL] |
|---|---|
| candidato R2 | `candidato_r2\C\...`, 15 arquivos, 3 diferentes do R1: `guard.py` (achado 2), `session_memory.py` (achado 4) e `journal.py` (colisão de caixa da revisão B). `CANDIDATO_MANIFESTO_R2.json` sha16 `1dd4a837bd33dc40` |
| patches | `DIFF_R2.patch` (originais → R2): 174.725 B, sha16 `19814b492cd16f3d`. `DIFF_R1_R2.patch` (só a R2): 10.577 B, sha16 `dcbf148a80c5d9ac`. Nos dois, `git apply` reproduz o alvo byte a byte (`DIFF_R2_APPLY_CHECK.json`) |
| suítes | 12 suítes, **235 testes, 235 PASSA, 0 FALHA** (as 220 do R1 mais 15 novas da R2). Guarda: 129 processos, **0 bloqueios** (`testes_r2\TESTES.md`, `RESULTADOS_TESTES.json`). Uma intermitência no HEARTBEAT está na §6 |
| testes dos revisores que falharam, de novo, com os scripts deles copiados byte a byte (`revisores_r2\`) | E7b (4.000 caminhos, 240 KB): **71,2 s → 0,041 s**. E7 (`a:/`×32.000): **43,3 s → 0,018 s**. t3/C: o JSON de nome confidencial **não é aberto**, `ProtocolError source_path_not_allowed:psion_name`. t3/E: dois diários, os dois verificam. E6 literal: recusado na pré-conferência, nada muda, reversão `REVERTIDA` |
| ensaio de implantação e reversão com processos geridos e falhas parciais (`ensaio_implantacao_r2\ENSAIO_R2_RECIBO.json`) | **7 de 7 cenários ok, em duas rodadas seguidas** (`ENSAIO_R2_RECIBO_rodada1/2.json`), cerca de 103 s cada |
| produção, só leitura | Tarefa «IALD Web Server» lida pelo backend de produção do `implantar.py`: `Running`, habilitada, RestartCount 3, PT2M, IgnoreNew. Processos: 1 supervisor, 1 web, 1 escuta. Banco 357.412.864 B, 777 backups somando 96.910.958.592 B (o heartbeat v1 continua gravando). Filtro D4 sobre os 12 contextos reais: **R1 e R2 decidem igual em todos** |

## 1. Achado 1: a reversão não cobria implantação parcial (ALTA) → CORRIGIDO

Defeito [REAL, E6 da revisão A]: a lista de arquivos só entrava no recibo quando o passo terminava bem. O `reverter.py` então
pulava os arquivos e restaurava o banco para v1, o que deixava a lib v2 diante de um banco v1. Também falhava nos passos
ausentes e não religava o app.

Correção (`implantar.py`, `reverter.py`, `implantacao_lib.py`):
- **Registro antes de tocar.** No passo 4, cada arquivo entra no recibo e o recibo é gravado ANTES de mexer no arquivo, com a
  fase `pendente → backup_ok → substituido` (ou `falhou_na_troca`). O `aplicar_blocos` grava o caminho do seu recibo antes
  de rodar. O `mover_backups` grava o destino antes de rodar. A migração grava `mudancas_iniciadas` antes do `--apply`.
- **Tempário.** `write_bytes_atomic` remove o tempário que ele mesmo criou quando a troca falha; o alvo fica como estava.
  `ferramentas\aplicar_blocos.py` recebeu a mesma correção, porque o cenário F mostrou que ele deixava
  `COORDINATOR.md.tmp_*` para trás.
- **Pré-conferência.** Um alvo somente-leitura passa a ser recusado no passo 0, antes de qualquer mudança. É o E6 literal.
- **Reversão.**
  - Restaura todo arquivo registrado, seja qual for o status do passo 4. Alvo já igual ao original fica como está; arquivo
    novo vira `.removido_`; tempário órfão vira `.removido_`.
  - Depois confere TODOS os 15 alvos do manifesto contra o original. Um alvo divergente sem registro é falha visível.
  - O banco só volta DEPOIS dos arquivos (se os arquivos falharem: `NAO_EXECUTADO`), e só quando está em v2. Banco ainda v1
    fica como está, porque restaurar o `pre_v2` perderia gravações v1 posteriores ao backup.
  - Passo ausente no recibo vira `PULADO`.
  - Uma falha não interrompe os passos independentes, e o reinício é **sempre tentado**.
- **Falha na implantação.** Se nada mudou (passos 0–2), o app volta sozinho pela tarefa reabilitada (cenário E). Se algo
  mudou, o app fica parado, a tarefa fica desabilitada e o recibo traz em `apos_falha.acao_requerida` o comando do reverter
  (cenários C e F).

Ensaio [REAL]:
- **C.** O último alvo fica preso aberto por outro processo, de modo que a troca falha depois de 14 de 15 arquivos e a
  pré-conferência não tinha como prever. O recibo traz os 15 arquivos com 14 `substituido` e 1 `falhou_na_troca`, e o
  tempário foi removido. App parado, tarefa desabilitada, **0 relançamentos** nos 3,5 s seguintes. O reverter dá
  `REVERTIDA`: 14 arquivos restaurados e 1 `ja_original`, banco com o sha256 original, a lib v1 lê o banco, o app volta pela
  tarefa com o store v1 `2d4f6214fa433534`, e o inventário fica idêntico nos originais.
- **F.** A falha acontece no passo 5, com os blocos aplicados em parte. O reverter devolve arquivos, banco, os 4 blocos
  aplicados mais o MEMORY.md, e o app.

## 2. Achado 2: ReDoS no filtro D4 (ALTA) → CORRIGIDO

Defeito [REAL, E7/E7b]: `_ESCRITORIO_PATH` era quadrático. Medi aqui, no R1, um segundo padrão quadrático que a revisão
não listou: `key_pem_name` (`\b[\w\-]+\.(?:key|pem)\b`) levou **23,2 s** com `'a-'×32.000` (64 KB) [REAL].

Correção (`guard.py`, varredura linear):
- **Escritório.** As duas primeiras alternativas do R1 sempre terminam numa barra imediatamente antes de `escritorio`, então
  o padrão inteiro tem o mesmo valor de verdade de `[\\/]escritorio`. A R2 mantém isso e acrescenta duas formas de caminho
  que o R1 não pegava: relativo ao drive (`c:escritorio`) e separador codificado (`%5c`, `%2f`). Todas as alternativas têm
  comprimento fixo [DERIVED].
- **`key_pem_name`.** Virou varredura linear: acha cada `.key`/`.pem` e anda para trás só sobre hífens. Tem o mesmo valor de
  verdade do regex do R1 (raciocínio na docstring).

Medidas [REAL]:
- Bateria adversarial de 23 entradas de cerca de 1 MB cada (todas as famílias de regra, mais E7/E7b/F): pior caso
  **0,54 s**, que é o NFKD de 1 MB acentuado. Os demais ficam entre 0,15 e 0,30 s.
- Crescimento com 4× o tamanho: razão entre **3,95 e 4,07** (linear; um padrão quadrático daria cerca de 16).
- Fuzz de 60.000 casos contra as regras do R1 (extraídas do `guard.py` R1): sem as formas novas, a decisão é **idêntica**;
  com elas, as únicas diferenças (1.293 casos) são `escritorio_path` a mais em texto que contém uma forma nova.
- No banco real, R1 e R2 deram a mesma decisão nos 12 contextos; o tempo total caiu de 0,273 s para 0,199 s.

## 3. Achado 3: gestão de processos sem ensaio e conflito com a Tarefa Agendada (ALTA) → CORRIGIDO NO CÓDIGO E NO ENSAIO SIMULADO; CMDLETS DE ESCRITA NÃO EXECUTADOS

A gestão de processos agora passa por um backend (`ProcessosPS` em produção, `ProcessosSim` no ensaio), e a ordem é esta:
- **Passo 0, só leitura.** Lê e registra a tarefa e os processos.
- **Parar o app (`parar_app_gerido`).** `Disable-ScheduledTask`, conferido com uma releitura → `Stop-ScheduledTask` se a
  instância está rodando → `stop_iald_web.ps1` → espera → **silêncio** (configurável; 10 s em produção) → nada pode ter
  renascido.
- **Antes da migração e antes da troca de arquivos.** `assegurar_parado` é chamado de novo e falha fechado se o app reapareceu.
- **Reinício.** Se a tarefa estava habilitada ANTES, ela é reabilitada e o app sobe por `Start-ScheduledTask`: o processo
  nasce no Agendador, fora do job object do shell, e o `MultipleInstances IgnoreNew` evita duplicata. Sem tarefa, o app sobe
  por `Win32_Process.Create` (WMI). Nos dois casos se exigem 1 supervisor, 1 web e saúde.
- **`--sem-reiniciar`.** Deixa a tarefa desabilitada e o recibo diz como religar.

Ensaio com processos Python REAIS (`ensaio_implantacao_r2\sim\`): o agendador simula RestartCount, RestartInterval,
IgnoreNew e Disabled; o supervisor tem trava de instância única; o filho web registra o sha do `store.py` que carregou.
- **A, controle.** A ordem do R1 (stop script com a tarefa habilitada) **reproduz o perigo**: o agendador relança o
  supervisor em cerca de 1,5 s (`restart_on_failure`).
- **B e B2.** Dry-run sem mudar nada, com os mesmos PIDs. Implantar `CONCLUIDA`, **0 lançamentos** na janela parada
  (cerca de 3,6 s), conferência de app parado antes dos passos 3 e 4, reinício pela tarefa, 1 supervisor e 1 web com o store
  R2 `b213498dabb3f7e6`, tarefa habilitada. Reverter `REVERTIDA`, 0 lançamentos na janela, app de volta com o store v1. B2
  também tem identidade total, com os 80 backups devolvidos.
- **E.** Falha antes de mudar: o app volta sozinho.

Honestidade [REAL]: na terceira rodada completa, B e B2 falharam por **defeito do simulador**. O agendador simulado morria
num `os.replace` disputado com um leitor (PermissionError do Windows). O `implantar.py` e o `reverter.py` **falharam
visivelmente** (`FALHOU_EM_reiniciar_app`) em vez de declarar sucesso. Corrigi o simulador (novas tentativas e erro
registrado sem matar o laço) e as duas rodadas seguintes deram 7 de 7.

## 4. Achado 4: `session_memory.py` lia arquivo confidencial sem o guard (alta) → CORRIGIDO

- `write_reference` passa pelo `is_confidential_path` ANTES de `exists`/`read`/`create`.
- A leitura de uma referência (`write_reference` existente e `reference` das operações) é feita por `load_reference`: guard
  de caminho, no máximo 64 KB, JSON objeto, **só as chaves do protocolo** (as 8 que as referências de produção têm e
  `source{path,sha256,bytes}`), varredura de conteúdo, e nada do arquivo é devolvido se houver chave estranha (`reference_unexpected_keys:<n>`).
- O código de recusa ficou o mesmo das demais leituras (`source_path_not_allowed:<regra>`), como exige o teste da frente 3.
- Compatibilidade [REAL]: as 4 referências em `C:\IALD\MEMORIA_IALD\sessions` têm exatamente essas chaves (só os nomes das
  chaves foram lidos).
- Testes novos: nome confidencial com sufixo `.bak_` e em maiúsculas, hardlink, chave canário, o operando `reference` e o
  fluxo normal de reuso. Em todos, o arquivo de nome confidencial **não aparece entre os abertos** (gancho de auditoria) e
  nenhum contexto é criado.

## 5. Além dos 4: colisão de caixa nos diários (revisão B, t3/E; não listado como bloqueante) → CORRIGIDO

`CtxCase` e `ctxcase` dividiam um diário no NTFS e os dois falhavam no verify [REAL, revisão B]. Agora `journal.path_for`
escapa as maiúsculas ASCII (`A` → `%41`); as minúsculas, os dígitos, `-`, `_`, `.` e os escapes do `quote` não mudam, e os
ids de produção não têm maiúscula [REAL, revisão B t4: 0 ids]. Os nomes dos diários existentes ficam iguais.

## 6. O que ficou sem corrigir, e por quê

1. **Cmdlets de escrita do Agendador não executados** [OPEN]. `Disable/Enable/Stop/Start-ScheduledTask` não têm `-WhatIf`,
   e rodá-los mudaria a produção. Validei aqui a leitura (`Get-ScheduledTask`, `Win32_Process`, `Get-NetTCPConnection`) pelo
   próprio `ProcessosPS` [REAL] e a lógica com o simulador [REAL]. Três pontos continuam [DERIVED]: que uma tarefa
   desabilitada não é relançada pelo RestartCount, que o usuário `rotol` (dono da tarefa, RunLevel Limited) pode
   desabilitá-la, e que o processo iniciado pelo Agendador sobrevive ao fim do shell. Mitigação já no código: se o
   `Disable` falhar, a implantação para antes de mudar qualquer coisa; se o app reaparecer, `assegurar_parado` aborta antes
   dos passos 3 e 4.
2. **Intermitência no HEARTBEAT** [OPEN]. `test_sixty_beats_in_process_zero_or_one_memory_event` falhou uma vez na primeira
   rodada completa (`AssertionError: 3 != 1` na linha 147: dois eventos a mais na segunda série de 60 batidas). O log dessa
   rodada foi sobrescrito pela seguinte; a mensagem ficou registrada nesta sessão. Não reproduziu em 24 execuções isoladas,
   nem sob carga, nem em 6 rodadas da suíte. Hipótese [DERIVED, não comprovada]: uma leitura transitória falha do
   `heartbeat_health.json` faz `_heartbeat_health_load` devolver `{}`, e a batida então trata o evento como devido. O erro
   vai para o lado de gravar a mais, nunca de perder. Não mexi no `iald_web_server.py` (código da frente 2) sem reproduzir
   o defeito. Recomendação: distinguir arquivo ausente de ilegível, com nova tentativa curta.
3. **Lacunas de cobertura do filtro de conteúdo** (revisão B, t3/D; não bloqueantes). Ficam sem regra: chave partida em
   linhas, base64, JWT/refresh token, `github_pat_`, `AKIA…`, bloco PEM e atribuição de senha. Ficam como falsos positivos
   `sk-learn…` e `record.key`. O conjunto de regras do D4 é decisão da gerência [INPUT]: acrescentar regra pode tornar
   ilegíveis contextos existentes, porque `get`/`project` varrem o estado. As únicas adições da R2 são formas de caminho do
   Escritório, e elas não mudaram nenhuma decisão no banco real.
4. **Um contexto de produção será recusado pelo D4 depois da implantação** [REAL, mesma decisão no R1 e no R2]: o
   `1bcf55a4-06fe-5e57-a2ad-640f2de13b53` (casa IALD, revisão 3) dispara `escritorio_path`. Pelo D4 a recusa é visível e
   nunca vem com redação silenciosa. O que fazer com esse contexto é decisão da gerência e do operador [OPEN].
5. **Outras observações da revisão B (t5, psion/heartbeat) e da revisão A que não foram listadas como bloqueantes**, por
   exemplo `H3b`: uma segunda corrupção do psion no mesmo dia perde a geração. Não foram tratadas nesta volta.
6. **Herdados do R1, inalterados.**
   - A reversão não devolve ao banco v1 os eventos posteriores à migração (eles ficam nos diários).
   - Uma sessão que grave com a lib v1 entre o backup (passo 2) e a migração (passo 3) entra na migração, mas se perde numa
     reversão. Por isso é preciso uma **janela quieta** também para as sessões, e não só para o app.
   - Os MCPs que já importaram a v1 falham fechado até reiniciar.
   - O custo em disco do `pre_v2` continua.
   - Psion (D3c): não restaurar.

## 7. Como implantar e reverter (atos da gerência; eu não rodei nada em produção)

- Ensaio só-leitura: `python -X utf8 "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\4_INTEGRACAO\implantar.py" --config "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\4_INTEGRACAO\implantar_config_producao.json" --dry-run`
  Lê os alvos (CAS), o banco (sonda `BEGIN IMMEDIATE`/`ROLLBACK`), a tarefa e os processos, e roda os dry-runs. Nada muda.
- Implantar: o mesmo comando sem `--dry-run` (opcional `--pular-mover-backups` para mover os 96,9 GB depois). Recibos em
  `4_INTEGRACAO\recibos_producao_r2\`.
- Reverter: `python -X utf8 "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\4_INTEGRACAO\reverter.py" --recibo "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\4_INTEGRACAO\recibos_producao_r2\RECIBO_IMPLANTACAO.json"`
  Serve também para recibo de implantação parcial. Opções: `--dry-run`, `--mover-backups-de-volta`, `--sem-reiniciar`.
- Config de produção R2 (`implantar_config_producao.json`, sha16 `52ae2d489e6c7c0c`): `candidato_r2`, manifesto R2,
  `gerir_processos: true`, `processos_backend: powershell`, `tarefa_agendada: "IALD Web Server"`, `silencio_s: 10`.

## 8. Entregáveis R2 (sha256 de cada um em `MANIFESTO_R2.json`)

- Candidato: `candidato_r2\` · `CANDIDATO_MANIFESTO_R2.json` · `DIFF_R2.patch` · `DIFF_R1_R2.patch` · `DIFF_R2_APPLY_CHECK.json` · `gerar_candidato_r2.py`
- Implantação: `implantar.py` · `reverter.py` · `implantacao_lib.py` · `implantar_config_producao.json` · `ferramentas\aplicar_blocos.py`
- Testes: `testes_r2\` (montagem, runner, `TESTES.md`, `RESULTADOS_TESTES.json`) · `testes_r2_src\` (`test_r2.py`, `perf_inputs.py`)
- Ensaio: `ensaio_implantacao_r2\` (`rodar_ensaio_r2.py`, `sim\`, `ENSAIO_R2_RECIBO*.json`)
- Revisores: `revisores_r2\` (os scripts deles, verbatim, e os resultados)
- Evidências: `evidencias_r2\` (`r2_testes_novos.json`, `PRODUCAO_R2_LEITURA.json`, `unittest\*.txt`, `e2e_n300.json`) · `r2_producao_somente_leitura.py`

Registros de casa (mapa de rotas, quadro, Atlas, memória da gerência, sessão ACOM) e o aceite são atos da gerência. Eu não
os toquei.
