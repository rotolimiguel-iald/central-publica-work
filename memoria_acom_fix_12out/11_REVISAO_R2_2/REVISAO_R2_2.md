REVISOR c1: conserto ACOM R2.2

Subagente da gerência c1, independente de quem construiu a R2.2 e de quem revisou a R2.1. Medido em 13/10/2026, entre 10:00 e 10:40 (hora local). Escrevi só em `C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\11_REVISAO_R2_2\`. Estatutos: [REAL] medido aqui · [DERIVED] deduzido do código ou de medida · [DECLARADO] afirmado pelo construtor e não refeito aqui · [OPEN] · [INPUT] decisão da gerência ou do operador.

## Veredito em uma linha

**PODE_IMPLANTAR_COM_RESSALVAS.** O manifesto e o patch conferem por hash, a suíte dá 278/278 na minha cópia, os cenários K4b, K4c, K3r, P8b (e uma variante nova, P8c) fecham como a R2.2 promete, e nenhum comando do roteiro falha como escrito [REAL]. As ressalvas são de texto do runbook (três) e dois resíduos já nomeados pelo construtor. Nenhuma bloqueia.

## 0. Base e método

- Hashes lidos por script [REAL] (`runs\s1_manifesto_patch.json`): `RUNBOOK_OPERADOR.md` `8b412619a5e91563`, `CANDIDATO_MANIFESTO_R2_2.json` `58184a0173281540`, `implantar.py` `11104b0e2dd8f80d`, `reverter.py` `62f212555a845e1a`, `implantacao_lib.py` `3f42bf41edf2c6d0`, config `14422d91e08182ae`, `DIFF_R2_1_R2_2.patch` `991fe46e8dffe6bd`, `TESTES_R2_2.md` `0524b04e89eb55e1`. Todos iguais aos citados no pedido e no `RESULTADO_R2_2.md` (`d7660ef13ec44711`).
- Minha cópia da suíte é independente da do construtor: parte da cópia do revisor R2.1, troca os 28 arquivos de papel «candidato» pelos do `candidato_r2_2` (web server com a chave redigida, mesmo tamanho) e acrescenta os 2 arquivos de teste novos e as 2 linhas do `rodar.py` (`scripts\s2_montar_copia.py`). Contra a cópia do construtor: 126 arquivos iguais; diferem só o `rodar.py` (o título) e 2 JSON de evidência gerados por teste.
- O ensaio usa o script do revisor anterior (`10_REVISAO_R2_1\scripts\s5_ensaio_rev.py`, que já traz o `s5_extra.py`), gerado de novo por `scripts\s5_gerar22.py` trocando só as entradas (ferramentas, candidato e manifesto de `9_R2_2`; cópia = minha `suite_r22`) e acrescentando o cenário P8c. Ferramentas copiadas byte a byte, backend de processos simulado, banco v1 sintético, guarda ligada (`ACOM_AUDIT_ROOT` = minha pasta).
- Chave de produção: varredura por script achou **0 arquivos** da minha pasta com a chave do `iald_web_server.py` do candidato [REAL]. Três arquivos de teste trazem fichas sintéticas de propósito.
- Produção: só metadados (§5). Não rodei `implantar.py` nem `reverter.py` contra a config de produção, nem em dry-run. Sem `init`/`transition` do ACOM (escreveriam no banco de produção, contra a regra da tarefa; desvio deliberado do protocolo do CLAUDE.md global). Sem rede, sem provedor.

## 1. Manifesto e patch [REAL] (`scripts\s1_manifesto_patch.py`)

| conferência | resultado |
|---|---|
| 15 arquivos do `candidato_r2_2` contra o manifesto (sha256 e bytes) | 15/15 |
| arquivos na árvore | 15, nenhum fora do manifesto, nenhum faltando |
| mudados contra o `candidato_r2_1` | 3: `guard.py`, `session_memory.py`, `iald_web_server.py`; iguais a `r2_2_mudancas`, e os `sha256_r2_1`/`sha256_r2_2` declarados conferem com os arquivos |
| `ferramentas_implantacao` (3) | sha confere com os arquivos de `9_R2_2`, e o `sha256_r2_1` com os de `9_R2_1` |
| campo `ferramentas` (`aplicar_blocos.py`, `SESSION_BRIDGE_v2.md`) | sha confere (a ressalva documental da R2.1 foi corrigida) |
| config R2.2 contra a R2.1 | diferem só o `_comentario`, `candidato_root`, `manifesto_candidato`, `recibos_dir` e `recibos_dirs_anteriores`; o manifesto da config é o `58184a01...` |
| `git -c core.autocrlf=false apply` do patch sobre uma cópia da R2.1 (web server redigido nos dois lados; ferramentas R2.1 em `ferramentas\`) feita FORA de qualquer repositório | rc 0, **0 diferenças** nos 18 arquivos (15 do candidato e 3 ferramentas) |
| chave no patch | ausente |

Cuidado de método, para quem repetir: rodar o `git apply` numa pasta dentro do repositório da Central aplica nada, em silêncio e com rc 0, porque o git só toca caminhos da subpasta. Na primeira tentativa vi 3 arquivos «diferentes» por isso. Refeito fora do repositório (`runs\s1_manifesto_patch.json`, `base_fora_de_repo: true`).

## 2. Suíte inteira na minha cópia [REAL] (`runs\s2_RESULTADOS_TESTES.json`)

- **278 testes, 278 PASSA, 0 FALHA, 0 pulados**, numa só rodada, Python 3.14.3, sob a guarda da auditoria. A soma bate com a do construtor, por suíte (CORE 20, NÚCLEO 34, SESSÕES 17+24, APP 31+9, HEARTBEAT 15, FILA 55+5, BLOCOS 5, INTEGRAÇÃO 5, R2 15, R2.1 19+5, R2.2 16+3).
- Guarda: 3 bloqueios, todos `BLOCK_NETWORK` (a sonda IPv6 do urllib3). Leituras fora da pasta: perfil do Python em AppData (513), índice canônico do orquestrador (84 leituras e 67 aberturas sqlite em `mode=ro`), `__pycache__` (13). Nenhuma leitura do banco ACOM de produção, do psion, de `.env` nem do Escritório (`runs\s3_guarda_resumo.json`, campo `suspeitos` vazio).
- Não rodei os 19 testes novos contra a R2.1 (o «15 falham, 4 passam» é [DECLARADO]). A prova diferencial que fiz é outra: os mesmos cenários K4c, K4b e K3r em forma de ensaio, que o revisor da R2.1 mediu na R2.1 com `REVERTIDA`/`ok: true`/`acao_requerida: null` (§3).

## 3. Ensaio de implantação e reversão [REAL] (`runs\s5_ensaio_rev22.json`, `runs\s7_resumo_ensaio.json`)

17 cenários, ferramentas R2.2 byte a byte. Em todos, menos K2b/K2c/K2d (o operador renomeia, apaga ou trunca o recibo, como na R2.1), terminam os 15 originais idênticos, o banco igual ao original, a lib v1 lendo o banco e nenhum temporário órfão.

| cenário | o que a R2.2 faz | R2.1 (revisor anterior) |
|---|---|---|
| **K4c** alvo MODIFICADO (bytes do candidato) depois de `conferir_alvos` OK | `FALHOU_EM_reiniciar_app`, rc 1, falhas `[reiniciar_app, conferencia_final]`, `app_religado: false`, 1 alvo no candidato, tarefa desabilitada, app parado; `acao_requerida` preenchida com o estado LIDO e o comando; **a trava do implantar ainda vê a implantação pendente**. O 2º reverter dá `REVERTIDA`, `app_religado: true`, `acao_requerida: null`, rc 0 | `REVERTIDA`, rc 0, `ok: true`, trava liberada |
| **K4b** alvo travado em modo exclusivo depois de `conferir_alvos` | `FALHOU_EM_reiniciar_app` (`Permission denied`), ação preenchida («Estado LIDO… o app está PARADO»), trava vê a pendente; o 2º reverter dá `REVERTIDA` | `acao_requerida: null` |
| **K3r** implantação `CONCLUIDA`; o REVERTER encontra o stop sem efeito | `FALHOU_EM_parar_app`, rc 1; nada restaurado (alvos seguem 15 no candidato); **tarefa REABILITADA** (`tarefa_habilitada: true`); ação: «NADA foi restaurado… tarefa… foi REABILITADA… VIVO SEM SUPERVISOR… rode stop_iald_web.ps1 e depois Start-ScheduledTask… ou reverta com…»; **sem «fica parado»** (`diz_app_parado: false`). A reversão normal depois dá `REVERTIDA` | tarefa desabilitada, recibo dizia «fica parado» |
| **P8** saúde 8 s atrasada | rc 3, `CONCLUIDA_AGUARDANDO_REINICIO`, leitura «um só filho web, o mesmo pid em 3 amostras em 3s: APP LENTO PROVÁVEL», `manda_reverter: false` | igual (por desenho) |
| **P8b** o web v2 morre ao nascer, supervisor relançando (filho nunca de pé) | rc 3, `LAÇO DE QUEDA PROVÁVEL` («o supervisor ficou vivo em 6 amostras… NENHUM filho web ficou de pé»), com o «COMO DISTINGUIR» e o comando de reverter; sem `UnboundLocalError`. A reversão dá `REVERTIDA` | rc 3 sem distinguir os casos |
| **P8c** (variante minha) o web v2 sobe, vive 2,5 s e morre, de novo e de novo | rc 3, `diagnostico_reinicio.leitura = LACO_DE_QUEDA_PROVAVEL`: 12 amostras, 4 pids distintos, 3 reinícios, «sumiu depois de aparecer: sim»; o diagnóstico vai à saída e ao recibo. A reversão dá `REVERTIDA` | — |
| **CFG** a sequência dos comandos do runbook | dry-run rc 0 → implantar `CONCLUIDA` → `reverter --config --dry-run` (rc 0, só lê) → `reverter --config` acha a única pendente, `REVERTIDA`, `app_religado: true` → `reverter --config` de novo recusa («esperada exatamente 1… achadas 0; use --recibo») → dry-run depois passa na trava | igual |
| K2 | 1ª falha no passo 4; 2ª `RECUSADA_RECIBO_ANTERIOR_NAO_REVERTIDO`; originais restaurados | igual |
| K3, K3b | `FALHOU_EM_parar_app`, tarefa reabilitada; K3b diz «a reabilitação FALHOU: reabilite à mão» | igual |
| K4 | reverter com web server preso: `FALHOU_EM_restaurar_arquivos`, não religa; o 2º fecha | igual |
| K6, K6b, K6c | `CONCLUIDA`; `CONCLUIDA`; `FALHOU_EM_substituir_arquivos` visível com ação de reverter; as reversões dão `REVERTIDA` | igual |
| K2b, K2c, K2d | recibo renomeado/apagado/truncado: a 2ª execução falha fechada em `pre_conferencias` (K2b, K2c) ou recusa (K2d), sem tocar; estado final **não** idêntico ao original, como na R2.1 | igual |

- Não refiz K1a–K1d e K5 (matar o implantar ou o reverter no meio); a R2.2 não mexeu nos passos que eles exercitam e a suíte deles é a do construtor.
- Incidente de execução, sem relação com o código: a 1ª execução do ensaio morreu (processo encerrado de fora) durante o K6; K6 sozinho deu certo e a execução completa de depois fechou os 17 cenários. Os números acima são os da execução completa; a parcial ficou em `runs\s5_ensaio_rev22_parcial1_K2K3K4.json`.
- O texto do P8b mantém o invariante da R2.1: o caso lento nunca traz o comando de reversão (`manda_reverter: false`). O caso de laço traz o comando, depois de pedir a confirmação pelo «COMO DISTINGUIR».

## 4. Pontos de código que li e conferem [REAL / DERIVED]

- **N1.** `guard.path_shape_reason` recusa antes do `realpath`. Medida minha, mesma máquina (`runs\s6_n1_rapido.json`): 16.000 componentes passam de **2,196 s (R2.1)** para **0,016 s (R2.2)**, com recusa visível `path_too_many_components`; caminho de 40.000 caracteres passa de `ValueError` (R2.1) para a recusa `path_too_long`; 40 componentes de nome benigno seguem sem recusa.
- **N3 pela via do app.** Li o trecho do patch (`agi_validate_path`, `agi_files_read`, ação `read` do `agi_execute`): o arquivo existente é aberto pelo handle do guard (`read_checked`), o caminho final do mesmo handle também precisa estar na whitelist, e os bytes lidos vêm desse handle, sem segundo `open` por nome. A lógica fecha na leitura. Os 3 testes `test_app_r2_2` passam na minha cópia. A medida de troca ativa por hardlink do construtor (294 leituras do canário na R2.1, 0 na R2.2) é [DECLARADO]; não a refiz.
- **Reverter.** Li o trecho do patch de `reiniciar_app`/`parar_app`/`main`: alvo divergente antes de religar vira exceção (`FALHOU_EM_reiniciar_app`); `REVERTIDA` exige o app religado; `ok` só com app religado, dry-run ou ação manual registrada; `reversao_limpa` na trava. Coerente com o que o ensaio mediu.
- `exigir_app_parado` está na config e não é lido por nenhum dos três scripts (também na R2.1). Inofensivo.

## 5. Produção, só metadados [REAL, 10:2x–10:38]

- Processos: 1 filho web (`python.exe` com `iald_web_server.py`) e 1 supervisor (`powershell.exe` com `start_iald_web.ps1`), tarefa «IALD Web Server» em `Running`, `python` = `C:\Python314\python.exe` 3.14.3. Os dois scripts do app que o runbook cita (`stop_iald_web.ps1`, `start_iald_web.ps1`) existem. O `mover_backups_antigos.py` ainda não existe em `C:\IALD\MEMORIA_IALD` (nasce na implantação, como o runbook diz).
- `MEMORY.md`: **191 linhas e 19.509 B** às 10:37 (limite do `aplicar_blocos`: 200 linhas e 24.000 B). Folga de 9 linhas, não as 12 do runbook (08:57). Ele cresce a cada sessão.

## 6. O RUNBOOK_OPERADOR.md lido como o operador vai ler

**Os comandos funcionam como escritos** [REAL]:

1. Os 13 blocos PowerShell passam no parser do PowerShell, 0 erros de sintaxe (`scripts\s4_runbook_blocos.ps1`, `runs\s4_runbook_blocos.txt`). Os caminhos entre aspas que existem hoje existem (`implantar.py`, `reverter.py`, a config); `copias_de_recibos` é criada pelo próprio bloco (`New-Item`).
2. As opções citadas existem: implantar `--config --dry-run --pular-mover-backups --sem-reiniciar`; reverter `--config | --recibo`, `--dry-run`, `--mover-backups-de-volta`, `--sem-reiniciar`, `--forcar-reinicio`; mover `--state --dest --keep --dry-run`. O `DRY_RUN_OK`, a saída 3 para `CONCLUIDA_AGUARDANDO_REINICIO` e a 0/1 do reverter são os do código.
3. O `mover_backups_antigos.py` do candidato, rodado numa pasta sintética com 6 backups: o dry-run mostra `found 6`, `to_move 3` e o `plan`; sem `--dry-run` move 3, `ok: true`, `failed: null`, grava `MANIFEST.jsonl` com o sha256, e cria o destino com os pais (o `D:\IALD_ARQUIVO` ainda não existe). «Confira se `to_move` é o número de backups menos 3» vale.
4. A ordem fecha: janela quieta → dry-run (`DRY_RUN_OK`) → implantar com `--pular-mover-backups` (`CONCLUIDA` / saída 3 / 1) → conferências → mover backups → reverter só se preciso. Os quatro pontos que o revisor da R2.1 pediu (conferência pós-implantação, comando de mover, comandos superados, critério pós-reversão `REVERTIDA` + `app_religado: true` + `acao_requerida: null`, mais o aviso da saída 3) estão todos presentes.
5. A tabela da seção 5 do runbook descreve o que o ensaio produziu (K3r, K4b, K4c, `REVERTIDA_SEM_RELIGAR`).

**Correções de texto que recomendo (não são comandos quebrados):**

- **R-1 (baixa).** Seção 3, item 3: o título é «Um supervisor e um filho web», mas o comando lista só o `python.exe` com `iald_web_server.py`, ou seja, o filho. O supervisor é um `powershell.exe` com `start_iald_web.ps1`. Hoje, em produção, o comando devolve 1 processo [REAL] e o texto passa, mas confere metade do que promete. Acrescentar: `Get-CimInstance Win32_Process -Filter "name='powershell.exe'" | Where-Object { $_.CommandLine -and $_.CommandLine -match 'start_iald_web\.ps1' } | Select-Object ProcessId,CreationDate` (deve listar 1).
- **R-2 (baixa).** Seção 1: «188 linhas e 18.928 B… 12 linhas de folga» é de 08:57 e envelheceu; às 10:37 são 191 linhas e 19.509 B (9 linhas de folga). Trocar por «medir na hora; quem decide é o dry-run» e lembrar que não se abre sessão que grave no `MEMORY.md` entre o dry-run e o implantar (a janela quieta já cobre).
- **R-3 (baixa).** Seção 1, tabela de falhas do dry-run: acrescentar `FALHOU_EM_pre_conferencias` por banco ocupado (o `BEGIN IMMEDIATE` espera até 30 s por quem segura escrita, com o app ainda no ar). Ação: repetir o dry-run; se persistir, parar e chamar a gerência. O dry-run não é estritamente «só lê»: toma a trava de escrita por um instante e faz `ROLLBACK`, sem mudar nada.

## 7. Ressalvas e resíduos (nenhuma bloqueia)

1. **Cmdlets reais do Agendador** (`Disable`, `Stop`, `Enable`, `Start-ScheduledTask`) seguem nunca exercitados [OPEN]. Tudo passou pelo backend simulado. O runbook já manda conferir a tarefa na seção 3, item 2.
2. **K2b/K2c/K2d:** a recuperação automática depois de renomear ou apagar recibo continua perdida; a regra do runbook (seção 6) é a defesa.
3. **P8b em produção:** a amostragem depende de cada `listar()` do PowerShell (1–2 s por amostra) [DERIVED, não medido]; o runbook cobre com a leitura manual de `ProcessId`/`CreationDate`.
4. **N2 (conteúdo) e N3 por renomeio:** como declarados pelo construtor (decisão D4 [INPUT]; equivale a cópia).
5. O `RESULTADO_R2_2.md` §3 cita 276/277 na 1ª rodada e 278/278 na final; a minha, independente, deu 278/278 na primeira.

## 8. Veredito

**PODE_IMPLANTAR_COM_RESSALVAS.** Os sete consertos pedidos pela revisão da R2.1 estão no código e fecham nos meus cenários; o manifesto e o patch reproduzem por hash; a suíte inteira passa; o runbook serve ao operador como está, com três ajustes de texto (R-1 a R-3) que a gerência pode fazer antes de entregar, sem nova rodada de revisão. A implantação segue sendo ato do operador.

## 9. Artefatos (sha256 por script em `MANIFESTO_REVISAO_R2_2.json`)

Scripts: `scripts\s1_manifesto_patch.py`, `s2_montar_copia.py`, `s3_guarda_resumo.py`, `s4_runbook_blocos.ps1`, `s5_gerar22.py`, `s5_ensaio_rev22.py` (gerado), `s6_n1_rapido.py`, `s7_resumo_ensaio.py`, `s8_manifesto_e_registro.py`. Resultados: `runs\s1_manifesto_patch.json`, `s2_montar_copia.json`, `s2_RESULTADOS_TESTES.json`, `s2_suite_rodada1_stdout.txt`, `s3_guarda_resumo.json`, `s4_runbook_blocos.txt`, `s5_ensaio_rev22.json`, `s6_n1_rapido.json`, `s7_resumo_ensaio.json`. Cópias regeráveis: `suite_r22\`, `ensaio\`, `tmp\` (só sintético). A cópia da suíte contém o web server redigido; nenhuma chave de produção na pasta.
