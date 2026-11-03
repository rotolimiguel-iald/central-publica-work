# RECEITA DA CADEIA DE SELO v404 -> v405, PARA REPETIR NA v406

> **Procedência:** relatório de um agente leitor (Sonnet, só-leitura) a serviço da gerência c1, devolvido em 02/11/2026 e gravado aqui pela gerência sem edição (o agente não tinha permissão de escrita). Estatuto global: [DECLARADO pelo leitor] até a gerência conferir cada comando ao executá-lo; o leitor marcou [REAL] o que leu em código/recibo/saída e [ESTIMATIVA] as contas dele.

Marcas: [REAL] = li em código, recibo ou saída de execução. [DECLARADO] = docstring ou memória sem artefato que a prove. [ESTIMATIVA] = conta minha.
Abreviações: `PK` = `C:\IALD\Central de Patentes\work\cadeia_de_selo\v405`. `NOS` = `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós`. `um.py` v405 = `0030242565cc13f6`, 40.175.869 B, 263.227 linhas.

## 0. Cinco avisos antes de tudo

1. [REAL] **O «instalador» não instala nenhuma pedra `.lean`.** `PK\instalar_v405.py` troca só o `um.py` do Nós (`os.replace`) e faz backup de 10 arquivos. As pedras já viajam dentro do `um.py` candidato, no dicionário `_EMBEDDED_KERNEL_FILES` (`um.py:8719`). O rito as escreve em `NOS\tgl_kernel` com `materialize_embedded_kernel()` (`um.py:128022`, chamada em `um.py:258315`). O instalador até recusa se algum módulo novo já estiver no Nós (`instalar_v405.py:45`).
2. [REAL] **Tempo do rito: a faixa «83–113 min» não é a faixa inteira.** Medi a partir dos `rito_horarios_vNNN.txt`:

   | versão | duração |
   |---|---|
   | v394 (bundle de 189 módulos) | 141,3 min |
   | v395 | 117,5 |
   | v396 | 160,9 |
   | v397 | 98,0 |
   | v398 | 116,1 |
   | v399 | 128,6 |
   | v400 | 95,5 |
   | v401 | 114,0 |
   | v402 | 93,1 |
   | v403 | 112,8 |
   | v404 | 82,9 |
   | **v405** | **124,8** (22:12:35 -> 00:17:26) |

3. [REAL] **O `MEMORY.md` está colado no limite.** Hoje tem 182 linhas e 23.925 B.
   - A regra do p00 (`PRECONDICOES_v405.json`, checagem 38) é: linhas+1 <= 195 e bytes+900 < 24000.
   - Para passar, o arquivo teria de estar com no máximo ~23.099 B. Faltam cerca de 826 B.
   - A superfície do pós-rito (`superficies_v405.py`) recusa com rc 3 e não compacta nada.
   - Na v405 passou por pouco: 23.090 B mais 900 = 23.990.
4. [REAL] **O sandbox `C:\t\k405c\final` está sendo alterado pela integração R3.**
   - `fechamento_02nov\integrar_fecho_bancada_02nov.py` grava ali 300 `.lean` novos em `TGLExt\F1Fecho394\`. São 1.199.883 B, média de 4.000 B.
   - Isso quebra as guardas da v405 que comparam sandbox com embutido (`preparar_kernel_v405.py conferir` e `sandbox_lean_a_mais`).
   - Para a v406, parta de um sandbox novo (`C:\t\k406c`), copiado do Nós. Não reuse o `k405c`.
5. [REAL] **O vigia da G1 hoje (`VIGIA_ULTIMO.json`, 02/11 19:08) diz que a v405 voltou a ter pendências.**
   - Pendentes: E08, E12, E15, E19, C18, C19, C20, C17C. E08 está BLOQUEADO.
   - Causas: «6 números citados defasados» em `read-brief` e `llms-full`, e o ar mudou depois do leitor de IA.
   - Ou seja, houve edição de `secoes/*` depois do commit da custódia. Isso tem de ser entendido antes de abrir a custódia da v406.

## 1. Sequência v404 -> v405

### 1.0 Nunca existiu README ou PLANO genérico na raiz `cadeia_de_selo\`
- Busquei em `C:\IALD\Central de Patentes\work\cadeia_de_selo\`.
- Só há `arvore_da_prova.py`, `atlas_indice.py` (e seus `.bak_*_pNNN`), os `vNNN_incorporacao_manifesto.json` e as pastas `vNNN`, `vNNN_kernel`, `vNNN_selo`.
- A receita vive nos scripts de cada pasta e em `v405\orquestrador\pos_treino_v405.py`.
- O orquestrador S0..S9 [REAL] codifica a ordem. Estados e logs ficam em `orquestrador\ESTADO.json` e `orquestrador.log`.

### 1(a) Pedras novas no kernel e no `um.py`; como o `um.py` embute o kernel e o manifesto
**Fase de preparação** (cwd `PK`, `python -I -B -X utf8`, exceto onde dito):

| # | comando | o que faz |
|---|---|---|
| a1 | `_mk_motor_v405.py` e depois `derivar_encanamento_v405.py [--so NOME ...] [--refazer]` | Gera `derivar_v405_motor.py` e os scripts de encanamento a partir dos da v404. Lotes `derivar_encanamento_v405_regras{A,B,C,C2_ensaio,D1_conferidor,D2_instalar,D3_diff_citacoes,E1_p00,E2_refazer,E3_comparar,F_pos_rito,H_bateria}.py`. Contagem exata por regra; aborta se casar diferente. |
| a2 | `copiar_base_v405.py` | Copia de bytes do Nós v404 selado para `base_v404\` (um.py, selo, core, manifesto do kernel, pilar, sidecar). |
| a3 | `gerar_pino_das_pedras_v405.py` | Escreve `pedras_sha16_da_ordem.json`. O arquivo manda e tem de bater com o `sha256_depois` do recibo de errata vigente (`RECIBO_ERRATA_PEDRAS_R7_01nov.json`, cadeia R7 -> R6 -> ... -> R2). Gera também `PINO_DAS_PEDRAS_DETALHE_v405.json`, com os teoremas por pedra. |
| a4 | `copiar_pedras_v405.py` | Copia de bytes das 8 pedras de `work\experimento_espelho_30out`, `cadeia_de_selo405`, `observador_terminal_31out` e `e0_cadeia_31out` para `PK\pedra\`. Escreve `PEDRAS_COPIA_v405.json`. |
| a5 | `preparar_kernel_v405.py copiar` | Chama `copiar_k405c.sh`. |
| a5b | `copiar_k405c.sh` | `robocopy` do `NOS\tgl_kernel` para `C:\t\k405c\final`, sem `.bak_`, `/XJ`, `/XD probe`. Cria junção `.lake\packages` apontando para `C:\t\k404c\final\.lake\packages`. |
| a6 | `preparar_kernel_v405.py gerar` | Grava as pedras e **gera** a raiz `TGLExt.lean` = raiz v404 + `ROOT_SUFFIX` (os 8 `import`, `delta_v405.py:159`). O Audit não muda (`AUDIT_PREFIX = ""`, `delta_v405.py:160`). |
| a7 | `preparar_kernel_v405.py conferir` | Escreve `kernel_modulos_novos_v405.json` (campo `novos`, uma LISTA). |
| a8 | `sh ./construir_kernel_v405.sh` | `lake build` e depois `lake env lean TGL/Audit.lean`, em `C:\t\k405c\final`. Logs em `kernel\`. Medido na rodada R7: build 454 s (21:04:30 -> 21:12:04) e Audit 340 s (-> 21:17:44). |
| a9 | `pos_build_kernel_v405.py` | Monta `build_full.log`. Confere rc 0, zero `sorry` (3 formas), trio, cabeçalho do `.olean`. Lê as linhas `TGL_DECL_SOURCE` e o `axiom_report` do log do Audit **com as funções do próprio um.py v404** (extraídas por AST). Deriva `kernel\FLAGS_v405.json`, `KH_N1_v405.json` e `KERNEL_RECIBO_v405.json` (contrato `KERNEL_RECIBO_R3_2`). Copia a árvore só-fontes para `C:\t\k405c\arvore`. |
| a10 | `copiar_logs_do_kernel_v405.py`, `copiar_insumos_v405.py` | Grava `LOGS_COPIADOS_v405.json` e `MANIFESTO_INSUMOS_v405.json`. |

- [REAL] Tudo de a3 a a10 e mais o candidato roda numa tacada com `sh ./regerar_v405.sh`. A docstring dele diz «build ~10 a 25 min».

**Do candidato ao `um.py`**
- [REAL] `gerar_candidato_v405.py` (recusa `-O`, nunca escreve no Nós) aplica 25 patches (`CANDIDATO_v405.json`). Cada âncora textual tem de ocorrer exatamente 1 vez na base.
- Patches de kernel:
  - `K00_TGLExt.lean`: troca o valor da raiz no dicionário embutido.
  - `K01_modulos_novos`: insere `'TGLExt/Nome.lean': <repr do texto>` antes do `}` final do dicionário (`gerar_candidato_v405.py:96-111`).
  - `V01_bandeiras`: `_LEAN_THEOREM_FLAGS` (`um.py:128109`) ganha +368 chaves `ext_pdm405_NNNN`, `ext_mtp405_`, `ext_idt405_`, `ext_obt405_`, `ext_ldd405_`, `ext_tdh405_`, `ext_dde405_`, `ext_pzp405_`.
  - `V02_escada`: `ext_flags` em `prove_external_ladder` (`um.py:140246`) ganha +368.
  - `V03_ledger`: `_ESQUELETO_STONES` (`um.py:250527`) ganha +8 linhas `("v405", nome, rel, None, None)`.
  - `W01_versao`: `UM_VERSION = 'v405'` (`um.py:96`).
- Outros patches:
  - `C12_*` (12): sobem `expected_ladder` 9698 -> 10066 em `_V394_FORMAL/QUADRATIC/NETWORK`, `_V395_PSIBIT`, `_V396_TESTEMUNHA`, `_V398_SONICO/AFINACAO`, `_V401_FALSIDADE`, `_V402_CONTRACTS`, `_V403_CONTRACTS` e `_V404_CONTRACTS`.
  - `C13_kh_n1_v404_pisos`: `kh_n1_cobertura_v404` vira piso.
  - `W02_runtime_v405`: 764.951 B.
  - `W04/W05/W09`: artigo PT/EN e `.md`.
  - `N00/N01/N02`: chamadas no `main` e resumo no selo.
- Pinos:
  - `FORMAL_MAP_v405.json` guarda o sha256 de cada um dos 1445 arquivos do kernel embutido.
  - `v405_pins.py` guarda o bloco extraído.

**Como o `um.py` verifica o kernel no rito** (`verify_tgl_kernel_formalization`, `um.py:138923`)
- `lake build` com timeout de **3600 s** (`um.py:138984`) e `lake env lean TGL/Audit.lean` com timeout de **1800 s** (`um.py:138985`).
- `parse_lean_axioms_v394` (`um.py:239859`) lê `'X' depends on axioms: [...]` e `does not depend on any axioms`. O resultado é o `axiom_report`.
- `parse_lean_provenance_v394` (`um.py:239837`) lê `TGL_DECL_SOURCE\t<decl>\t<módulo>`. O resultado é `declaration_sources_v394`.
- Cada bandeira de `_LEAN_THEOREM_FLAGS` vale `lake_build_ok` e teorema presente no `axiom_report` sem `sorryAx`, sem `Lean.trustCompiler` e sem axioma `TGL.*` ou `TGLExt.*`.
- `sha256_directory(FORMAL_DIR)` (`um.py:138771`) hasheia `.lean`, `lakefile.toml`, `lean-toolchain`, `README.md` e `lake-manifest.json` (exclui `.lake` e `ExtrairDeps.lean`). Isso dá `formal_source_hash` e `formal_files_sha256`.
- O rito grava `tgl_kernel_proof_manifest.json` (`um.py:261267`) no Nós. As chaves do cabeçalho são: `timestamp`, `formal_checker`, `build_tool`, `lean_version`, `lake_version`, `toolchain_pinned`, `mode`, `formal_source_hash`, `formal_files_sha256`, `axiom_report` (2,77 MB), `build_stdout_sha256`, `audit_stdout_sha256`, ... O selo pina seu sha256.
- O selo `um_absoluto_selo.json` traz: `um_version` = v405, `timestamp` = 2026-11-01 23:07:31, `sha256{14 arquivos}` (um.py, manifest.md, um_absoluto.json, forma_canonica.md, tex/pdf PT-EN, figuras, `tgl_kernel_proof_manifest.json`, `um_absoluto_pilar_quantico.json`), `formal_source_hash`, `result_hash`.

### 1(b) Ensaio a seco
- **O que é:** `ensaio_a_seco_v405.py` roda sem GPU e sem rito, num diretório `dry_v405\`. Chama os registros novos e alterados no ponto de chamada real.
- **Comando** (cwd `PK`, SEM `-I`, porque importa o um.py e precisa do numpy do usuário): `python -B -X utf8 ensaio_a_seco_v405.py um_v405_candidato.py v405 > ensaio_out.txt 2>&1`
- **Duração:** ~9 min na v405 (21:19:15 -> ~21:28). O ensaio da v394 levou ~4 min incluindo pdflatex.
- **Saída:** `ensaio_a_seco_v405.json`. O veredito é «TUDO PASSOU».
- **O que confere** (`ensaio_out.txt` [REAL]):
  1. Kernel embutido == sandbox, byte a byte, 1445 arquivos.
  2. `verify_tgl_kernel_formalization()` de ponta a ponta com o lake simulado devolvendo os logs crus do sandbox: 29965 constantes, 0 não lidas.
  3. Escada recomputada [10066, 10066].
  4. Vizinhos recomputados (iguais, ou a «troca dita» só de números).
  5. Fluxo principal: 13 chaves novas no core.
  6. Guarda estática de ordem de chamada, com controle negativo.
  7. 346 casos de unidade, todos True.
  8. Selo: diferença só nas chaves esperadas.
  9. Artigo PT/EN: pdflatex 2x com rc 0, quadro do 4,44 no topo.
  10. `.md`.
  11. `simular_arvore_do_nos`: hash formal com 1446 entradas.
  12. `exame_pontos_v405`.
  13. Guardas estáticas da Bancada sobre o candidato.
- **Rodar sem o ensaio é o erro que custou rito na v357:** o `&` de «Reeh & Schlieder» (memória `ensaio-a-seco-do-artigo`, [DECLARADO]).
- **Cuidado:** a v404 mostrou que o ensaio NÃO vê defeito de ordem de chamada no `main`. Por isso a guarda AST própria (item 4 da seção 4).

### 1(c) Instalar e rito
Instalar (cwd `PK`; o orquestrador usa `C:\Python314\python.exe -B -X utf8 instalar_v405.py`). Exige:
- Nós == v404 selada (`ESPERADOS_v405.origem_sha16`).
- Candidato == `ESPERADOS` == `CANDIDATO`.
- `PINO_RECIBO_PRE_SELO_v405.json` existente, utilizável e do um.py do Nós. A Bancada de produção ainda pina v404 (sha256 de `canonical_contracts.json` == pino).
- Cache do pilar guardando o resultado.
- Nenhum `um.py` ou `pilar_quantico_worker.py` vivo (`powershell Get-CimInstance`).
- As 18 pedras anteriores presentes e as 8 novas ausentes do Nós.
- Backup de bytes (`.bak_<ts>`) de **10 arquivos**: um.py, um_absoluto.json, _selo.json, _forma_canonica.md, _manifest.md, _pilar_quantico.json, _selo_acom.json, **tgl_kernel_proof_manifest.json** (lição 2 da v404), `tgl_kernel\TGLExt.lean` e `tgl_kernel\TGL\Audit.lean`.
- Cópia de bytes do resultado do pilar para `PK\pilar_anterior_v404_<ts>\`.
- Escreve `APLICADO_AO_CANONICO_<ts>.json`.
- Saída real: `{"ts": "20261101_221203", ..., "n_backups": 10, "modulos_novos": 8}` (`orquestrador\instalar_out.txt`).
- Reverter: `reverter_v405.py` (só por decisão da gerência; restaura os 10 backups e põe os módulos novos em quarentena; **não** restaura `.tex`/`.pdf` nem limpa `.lake`).

**Rito**
- **Comando** (cwd `PK`): `C:\Program Files\Git\bin\sh.exe rito_v405.sh`. O orquestrador dá timeout de 5 h.
- **O que o script faz** (`rito_v405.sh`):
  - `cd NOS`.
  - `export PYTHONIOENCODING=utf-8`.
  - `unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR` (rodada COMPLETA, sem checkpoint; o pilar quântico é reaproveitado pela chave de cache `75dc30bc9cc8d330e31f99ca`).
  - Guardas: sha16 do um.py == `ESPERADOS.candidato_sha16`; nenhum `um.py` vivo; nenhum marcador `.servidor_parado_pelo_rito` em `v404\` e `v405\`.
  - Para o servidor nativo: `Stop-ScheduledTask 'IALD Llama Server'`, depois `powershell -File C:\IALD\projetos_pyhton\IALD\stop_iald_llama.ps1 -Tudo`.
  - Confere llama-server = 0 e VRAM <= 6000 MiB (aqui, 4325 MiB). Dispara vigia contra reaparecimento.
  - Roda: `( echo 1 | python um.py > rodada_v405_stdout.txt 2>&1 ) &`, e grava `RITO_RC=<rc>` no fim do stdout.
  - Horários em `PK\rito_horarios_v405.txt`.
  - Ao final (mesmo com falha ou sinal) religa a tarefa `Start-ScheduledTask 'IALD Llama Server'` e espera a porta **8081**. Religou em 8 s (`00:17:29 -> 00:17:37`).
  - Abortar = `kill -TERM $(cat PK/.rito_v405.pid)` no Git Bash, nunca TaskStop.
- **Stdout canônico:** `NOS\rodada_v405_stdout.txt` (267.968 B). Termina com `RITO_RC=0`.
- **Tempos medidos:** v405 22:12:35 -> 00:17:26 (124,8 min). Estimativa interna do script (parâmetro de `kernel\construir_marcas.txt`): 454 s + 340 s = 794 s por passagem; o rito faz 3 passagens (rito, autoteste com `sorry` injetado em `TGL/HalfNat.lean`, restauração), ~39,7 min só de Lean.
- **Checkpoint `TGL_RITE_CHECKPOINT` (memória `rito-checkpoints-v321`):** é para versão intermediária; a versão final/custodiada roda sem.

### 1(d) Pós-rito: `pos_rito\chain_pos_rito_v405.sh`
Uso: `CHAIN_DE=<rótulo> CHAIN_ATE=<rótulo> sh pos_rito/chain_pos_rito_v405.sh`, cwd `PK`. Ordem: `0 1 2 3 4 5 6 7 8 9 10 10a 10b 10c 11 12 13 14`. Sai com rc 1 em reprovação, rc 20 em AGUARDA_OPERADOR. Não restaura nada sozinho.

| rótulo | o que faz [REAL: `chain_pos_rito_v405.sh`] | tempo na v405 |
|---|---|---|
| 0 | Guardas. um.py do disco == instalado == candidato. Ferramentas presentes. `guarda_p18_v405.py` sobre `textos`, `fechar` e `registrar_mapa`. Confere `RITO_RC=` no stdout. Fila da memória: `memoria.py` == `PINO_MEMORIA_PY_v405.json` e nenhuma `PAUSA_VIGIA.json` alheia. | 00:17:37 |
| 1 | `conferir_rito_v405.py _POS_RITO` **sem `-I`**, no lugar (cwd `PK`). Esperado «TUDO BATE». Escreve `conferencia_rito_v405_POS_RITO.json`. Copia para `pos_rito\conferidor\`. | 00:17:38 |
| 2 | `pos_rito\leitura_v405.py` (lê core, selo, sidecar, linha final do rito). Esperado «PROBLEMAS: nenhum». | 00:18:07 |
| 3 | Ensaio em CÓPIAS das superfícies: `superficies_v405.py --copias`. Árvore em dry. `exige` de marcador do selo e sha16. Recusa rc 3 se o `MEMORY.md` passaria de 195 linhas ou 24000 B. | -> 00:18:25 |
| 4 | Patch árvore/índice (opcional, pulado na v405). | |
| 5 | `arvore_da_prova.py v405` (cwd `cadeia_de_selo\`). | |
| 6 | `atlas_indice.py v405`. Regenera `TGL_INDICE_VIVO.md` e insere blocos datados no `TGL_ATLAS.md` (marcador `<!-- atlas_indice vNNN -->`). | |
| 7 | Cria `fila\PAUSA_VIGIA.json`; roda `superficies_v405.py` (real): 11 alvos. | 00:18:25 -> |
| 8 | `C:\LAR_MIGUEL\porta_memoria.py` (espelho da memória). | |
| 9 | Regra da linhagem completa: `exige` marcador `<!-- ..._v405_selada -->` e sha16 em cada superfície. Valida `MEMORY.md` < 24.000 B e <= 195 linhas. Renova a pausa, `MEMORIA_GERENCIA=claude-c1 memoria.py pinar --motivo "pos-rito v405"`, remove a pausa, `memoria.py verificar`. | 00:20:19 |
| 10 | B(n) em ENSAIO (esboço R3.5, `sincronizar_bancada.py`; nada gravado). Veredito `REPINADA_B14__ENSAIO__NADA_GRAVADO_NA_BANCADA`. | 00:20:20 -> 00:22:13 (FIM) |
| 10a | Confere `bancada_B3_servico\RECIBO_PARADA_v405.json` e porta 18777 fechada (rc 20 se faltar). | 3 s |
| 10b | B(n) APLICAR. Exige `B3_AUTORIZADO=sim`, `EVENTO`, `EVENTO_HASH` e o recibo da parada. Veredito `REPINADA_B14__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO`. | 00:22:27 -> 00:24:23 |
| 10c | Confere `RECIBO_RELIGAMENTO_v405.json`. | |
| 11 | `pos_rito\fechar_v405.py`. Recusa sem os 3 recibos do B(n) e sem os parágrafos verificados. Gera manifesto de incorporação, `MANIFESTO_ARQUIVO_v405.json` (16.414 indexados), `DIFF_v404_v405.diff`, `DIFF_KERNEL_v405.txt`, cópia para `v405_selo\` e `v405_kernel\`, handoff `memory\handoff-v405-custodia.md` + `NOS\HANDOFF_v405_CUSTODIA.md`. | 00:24:35 |
| 12 | `registrar_mapa_v405.py` monta; `C:\IALD\MAPA_DE_ROTAS\rotas.py registrar ... --quem "claude-c1 (gerência), cadeia v405"`; depois `rotas.py verificar`. Marcador idempotente `registro_mapa_v405.REGISTRADO`. | |
| 13 | `C:\IALD\Central de Patentes\work\inventario_bancada\inventario_bancada.py` e `gerar_documento.py`. Copia os 2 INVENTARIO para `memory\`. | |
| 14 | `C:\IALD\NOS_VIVO\construir.py` (lê o mapa). Mais 14-bis: `gerar_x_custodia_v405.py` escreve `pos_rito\CUSTODIA_v405_RASCUNHO.txt`; não publica. | FIM 00:33:56 |

- O orquestrador executa 0->10 em um bloco, 10a, 10b, 10c->14 em outro.
- A lição 4 da v404 diz «depois do registro da gerência no Mapa (passo 12), 13 e 14 rodam de novo». Na v405 o passo 12 registra sozinho, então isso não é mais necessário.
- Harness e textos:
  - `pos_rito\textos_v405.py` é MONTADO por `montar_textos_v405.py` a partir de `textos_v405.semente` (= v404 com a versão subida) mais `textos_v405_novo.pysnip` (autoral). Recusa importar com marca `TEXTO_A_REESCREVER`.
  - `harness_textos_ensaio_v405.py [--manter-copias]` e `harness_fechar_sandbox_v405.py` emulam um Nós em `C:\t\h405` e rodam leitura, textos, superfícies, b3_recibo, mapa e fechar, com controles negativos. Na v405: 557 controles da leitura, 61 do parágrafo novo, 28 do fechar.
  - O `fim_de_cadeia_v405.sh` os roda na ordem (11,5 min).

### 1(e) Custódia G1 (`C:\IALD\Central de Patentes\tools\custodiar.py`)
- cwd `C:\IALD\Central de Patentes`. Comandos do orquestrador `s7_g1`:

```
C:\Python314\python.exe -X utf8 C:\IALD\Central de Patentes\tools\custodiar.py planejar --versao v405 --ator <ator> --coautor "<Nome <email>>" --ordem <arquivo verbatim da ordem> --seco
... custodiar.py executar --versao v405 ... --publicar
... custodiar.py auditar --versao v405 ...
```

- Subcomandos [REAL, `custodiar.py:1-12`]:
  - `vigiar [--gravar] [--json]`: só leitura, confere as 3 marcas (selo + pino, bloco «vNNN SELADA» no diário, `HANDOFF_vNNN_CUSTODIA.md` + `rodada_vNNN_stdout.txt` + `cadeia_de_selo\vNNN`). Com `--gravar` escreve `VIGIA_ULTIMO.{json,txt}`.
  - `sondar`: grava `fatos_vNNN.json`.
  - `planejar --seco`: não escreve nada.
  - `executar --publicar`: liga os atos para fora (commit, push, subida do site, Central pública, ACOM).
  - `--ensaio`: não grava nada.
- Códigos de saída: 0 completo; 1 pendente; **5 só decisões do operador**; 10 WAIT; 20 STOP/BLOQUEADO; 30 falha de leitura; 40 divergência do ar/GitHub. Nunca `--force`.
- O que cada passo publica (`README.md` da G1 + plano real):

| passos | o que publica |
|---|---|
| E00-E09, E10-E12 | the_boundary (espelho): backup, 1096 pares, ESTADO_ATUAL, LEDGER, CITATION, **PORTAs**, laço portas/README/geradores até ponto fixo, parágrafos prontos do handoff no README, verificações, commit, push, raw. v405: commit `6a2138d7`. |
| E13-E19 | **Site** (dados do selo, `index.html`, `llms-full.txt`, `index.md`, cartão de estado, **`llms.txt`**/read-brief na E08, sitemap e manifesto, subida em ensaio e real, leitor de IA). |
| C1-C12 | Central: cofre `um_unificado` + `tgl_kernel` (1446/1446 conferem), runner, 16 dispositivos FINAL, ledger. |
| C13 | Registro: diário do site, **Atlas**, 6 memórias, linha do `MEMORY.md` pela fila da memória. |
| C14-C16 | Commit/push da Central (v405: `8f8616ac`), conferência final independente (13/13), «PUBLICADA» e rota `custodia.vN`. |
| C17A/B/C | Transições ACOM. |
| C18 | Central pública (3 repositórios, `/central/`, um.acom). |
| C19-C21 | Nós vivo e quadro; pernas do selo (Bancada, `ACTIVE.json`, memória científica); release do app. |

- **Memória da linhagem, desenho do fechamento e índice vivo NÃO são da G1.** São do pós-rito: passo 7 (`superficies_v405.py`: `MEMORIA_DA_LINHAGEM.md`, `DESENHO_DO_FECHAMENTO_QG.md`, `TGL_ATLAS.md`, `TGL_CORE_MEMORY.md`, `CLAUDE.md` da Haja_Luz, memórias) e passo 6 (`TGL_INDICE_VIVO.md`).
- **A vitrine do X não é da G1** (lição 41). `tools\gerar_vitrine_x.py` recusa sem a entrega V7 do selo corrente (perna do Codex). O `pos_rito\CUSTODIA_v405_RASCUNHO.txt` é copiado à mão para `Chatgpt\TUNEL\PARA_CHATGPT\X_VITRINE\CUSTODIA_v405.txt`.
- **Tempos:**
  - C18 (Central pública) levou ~107 min na v404 [DECLARADO, memória].
  - Na v405 a G1 rodou de 01:08 a 04:11 com várias paradas, cada uma uma lição (31-41).
  - O E09 gravou recibo às 00:57:08.
  - PUBLICADA às ~01:32.
  - Estado final do plano: 36 aplicados, 2 superados, 1 do operador, 3 faltando (C19, C20, C17C). A custódia **não diz «concluída»**.

### 1(f) O que ficou manual para a gerência
- **Troca da linha do índice CUSTODIADO -> PUBLICADA** no `MEMORY.md`. Ordem [DECLARADO, lição 12 da v404]:
  1. Trocar a linha mantendo o número de linhas.
  2. Levar a antiga para o `MEMORY_2.md`.
  3. `pinar` com motivo.
  4. `promover` os depósitos.
  5. `verificar`.
  - `promover` só acrescenta, e exige o `MEMORY.md` igual ao pino.
  - Na v405 a linha 78 já diz «PUBLICADA».
  - O `MEMORY_2.md` tem fim de linha misto: acrescentar no estilo da última linha e provar `novo.startswith(antigo)`.
- **Despacho F0.3 ao Codex** (depois de 04/11 06:37, lendo a cota antes): `C:\Python314\python.exe C:\IALD\PROGRAMA_IALD\iald.py despachar-codex --thread 01a0ce2b-8c2f-71b0-a9a8-91b17715a569 --arquivo "C:\IALD\Central de Patentes\work\custodia_v405_02nov\DESPACHO_CODEX_F03_v405.md" --quem claude-c1 --unidade F0.3.MEMORIA_CIENTIFICA_SYNC`. Depois rodar `custodiar.py executar --versao v405 --publicar` para C19/C20/C17C.
- **Filmes V7 (adendo da ORDEM 022), vitrine do X e post.**
- **Operador:**
  - C21, release do app: pipeline `work\iald_vNNN_<data>\app`, construtor diferente do revisor.
  - Zenodo (hoje v401).
  - `iald.ia.br` llms/sitemap/robots dando 404.
  - D2 [LEGAL].
  - Ratificação de `tempoDoRetido` e D27-D33.
  - Contrato JEV da Torre.
- **Itens da Torre** (CLAUDE.md das casas FISICA e NATIVA acima de 262144 B, missão recusada pelo guarda) seguram C19 em toda custódia até decisão (lição 40).
- **Atribuição:** a `--coautor` de `custodiar.py` é o trailer dos commits da G1. Na v405 foi `Claude Opus 5.5 <noreply@anthropic.com>` [REAL]. [A FAZER] conferir o vigente.
- **Gate «quem constrói não aprova»** [REAL, `pos_treino_v405.py:206`]: o orquestrador só instala se `revisao_terceiro\REVISAO_TERCEIRO_v405.json` tiver `aprovada: true` e `candidato_sha16` igual ao do candidato. Na v405: revisor R3, 0 ALTO, 0 MÉDIO, 8 BAIXO; houve duas reprovações antes (R1 e R2).
- **Seguem manuais por ordem do próprio script:** o `AVISO_GERENCIA.md` (só com `V405_AVISO_REIVINDICACAO`), a parada e o religamento do serviço da Bancada (porta 18777) com `V405_AUTORIZACAO_OPERADOR`.

## 2. Como o `um.py` v405 decide as 4 chaves do selo

**Resumo:** três são **literais False** no código, que só um patch muda. A quarta é **medida** no `axiom_report`.

**(i) `rede_fock_v394.whole_certificate_inhabited`**
- Função `rede_fock_v394(core)` em `um.py:239766`; o literal está em `um.py:239814` (`whole_certificate_inhabited=False,`).
- O `all_verified` desse registro é calculado do contrato `_V394_NETWORK_CONTRACT` (`um.py:232386`; guarda `declarations`, `declaration_sources`, `source_sha256` das 184 fontes, `expected_ladder`) contra `axiom_report`, `declaration_sources_v394` e `_EMBEDDED_KERNEL_FILES`. Nenhum desses entra na chave.
- Trecho [REAL]:
  ```
  result = dict(all_verified=passed, formal_declarations=declarations, embedded_sources=sources, exact_ladder=exact, ...,
        whole_certificate_inhabited=False,
        scope='Current compiled components on the same Fock; the remaining joint contract is explicit.', does_not_gate_core=True)
  ```
- Quem lê essa chave como falsa:
  - Spec `u4`, `'op': 'falso'` (`um.py:240824`).
  - Resumo do selo (`um.py:261395`).
  - `conferir_rito_v405.py:396`.
  - `ensaio_a_seco_v405.py:191`.
  - `pos_rito\leitura_v405.py:393-394`: «whole_certificate_inhabited deve seguir False».

**(ii) `psibit_v395.conditional_psion_face.inhabitant_exhibited`**
- Função `psibit_v395(core)` em `um.py:231063`; o literal está em `um.py:231100`:
  ```
  cond_ = face_("conditional")   # theorem TGLExt.Psibit.the_psion_face_of_the_psibit, flag ext_psb395_0101 (lidos do axiom_report)
  cond_.update({"status": "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE", "inhabitant_exhibited": False,
                "reading": "... the kernel exhibits no inhabitant of the certificate (TheImportedSecondQuantization, non-vacuity argued, no term) ...",
                "joint_contract_open_v394": ...})
  ```
- O `True/False` não é lido de nenhuma entrada; o texto «sem termo» é fixo.
- Quem lê como falso:
  - Spec `u4` (`um.py:231342`).
  - Spec `x_i` do `gap_v405` (`um.py:220817`; texto em `220826`). É checagem nova da v405 (R7): «o kernel segue sem habitante do FockCertificate».
  - `pos_rito\leitura_v405.py:399-400`.
  - `pos_rito\textos_v405.py:308` (asserção).
  - `harness_textos_ensaio_v405.py:525` (controle negativo que põe True e tem de reprovar).

**(iii) `testemunha_estatica_v396.fock_face.inhabitant_exhibited`**
- Função `testemunha_estatica_v396(core)` em `um.py:230444`; o literal está em `um.py:230481`:
  ```
  fock_ = {"theorem": fk_["theorem"], "declared_in": src_.get(fk_["theorem"]), "declared_outside_the_stone": fock_ok_,
           "status": "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE", "inhabitant_exhibited": False,
           "linked_to_the_corner_by_a_lemma": False, ...}
  ```
- `fock_ok_` é calculado (teorema em `TGLExt/Psibit.lean`, fora da pedra, no trio). `inhabitant_exhibited` e `linked_to_the_corner_by_a_lemma` são literais.
- Quem lê como falso:
  - Spec `u5` (`um.py:230690`).
  - `leitura_v405.py:403-405` (`linked_to_the_corner_by_a_lemma is False`).
  - `harness_textos_ensaio_v405.py:513`.

**(iv) `witness_layers.canonical_full_witness_term_constructed`**
- Calculada, dentro de `run_um` (`um.py:152287`), no dicionário `witness_layers` (`um.py:152379`):
  ```
  "canonical_full_witness_term_constructed": bool(((kernel_formalization or {}).get("axiom_report") or {}).get("TGL.ModularRealization.canonicalFullTGLWitness") is not None),   # v367: ... nome ausente do relatorio => False
  ```
- Só vira True se o `axiom_report` contiver **exatamente** a chave `TGL.ModularRealization.canonicalFullTGLWitness`.
- No kernel atual esse nome só aparece em comentário (`TGL/ModularRealization.lean:31`, `TGLExt/O16/PhotonModularRealization.lean:34`); não há declaração. Está RESERVADO (`um.py:152120`).
- O Audit lista toda constante de `TGL`/`TGLExt` (inclusive `def`, via `collectAxioms`), então basta declarar o nome com esse caminho completo (namespace `TGL.ModularRealization`) num módulo importado pela raiz. Se o termo canônico nascer com outro nome (por exemplo `physicalFockCertificate` ou `lightRealization ...`), a chave continua False.
- A referência histórica `selo_v391 ... canonical_full_witness_term_constructed op falso` (`um.py:209330`, `'onde': 'fonte:g2_medidas'`) lê o selo v391, não o corrente [inferência; conferir ao patchar].

## 3. Como o `um.py` incorpora ~300 módulos novos (e o que muda)

**Fatos medidos agora**
- [REAL] O kernel do Nós tem 184 módulos em `TGLExt\F1Fecho394\` (855.111 B) e 1099 itens em `TGLExt\`.
- [REAL] Os 300 novos na integração (`integracao_stdout.log`): 174 idênticos ao kernel, 1 conflito (`CanonicalGammaNoFixedR4` difere; **o kernel prevalece**), 300 novos.
- [REAL] Compilação até 19:23: 272 módulos ok, soma dos tempos 12.258 s (3,4 h de CPU com paralelismo 6; individuais de 17 a 305 s, máximo `CanonicalFockMatrixCornerR2`). Máquina: 48 CPUs, 255 GB.
- [REAL] Precedente v394: 189 módulos, `lake build` 1386 s e Audit 258 s no sandbox, `um.py` +2.408.992 B, rito 141,3 min, 3581 bandeiras. Raiz importava só 3 agregadores `NetworkProofAuditR3/R7/R8` (`TGLExt.lean:1091-1095`).

**O que muda** (padrão da v394/v405; arquivos/linhas de referência na v405)

| item | onde / como | v406 |
|---|---|---|
| Fontes embutidas | `_EMBEDDED_KERNEL_FILES` (`um.py:8719`): +1 entrada `'TGLExt/F1Fecho394/X.lean': <texto>` por módulo (patch K01 insere antes do `}` final) | +300 entradas, ~1,2 MB brutos |
| Raiz | `TGLExt.lean` (K00). **Lake só compila o que a raiz importa** (`lakefile.toml`: `[[lean_lib]] name = "TGLExt"`) | [A FAZER] decidir se importa os 2 topos ou um agregador |
| Ordem de compilação | O grafo de `import` decide (Lake). `ORDEM_DE_INSTALACAO` só ordena as linhas da raiz | |
| Audit | `AUDIT_PREFIX` vazio. `TGL/Audit.lean` importa `TGLExt` (`:387`) e termina num `run_cmd` que imprime `TGL_DECL_SOURCE` e o axioma de toda constante de `TGL` e `TGLExt`. Os ~9420 `#print axioms` explícitos são legado | nenhuma linha nova de `#print axioms` |
| `axiom_report` | Parseado de `audit.stdout` (nunca do blob build+audit; a linha `TGL_AXIOM_COVERAGE_TOTAL` duplicaria, `_v392_axiom_coverage` `um.py:215246`) | |
| Hash por arquivo | `sha256_directory` (`um.py:138771`) | entradas 1446 -> ~1746; pino h8 a regenerar |
| Bandeiras | `_LEAN_THEOREM_FLAGS` (`um.py:128109`) e `ext_flags` (`um.py:140246`): +N chaves. Política v394: só declaração **nomeada** pública; auxiliares (`eq_N`, `_simp_N`, `_proof_N`) ficam fora | N a medir em `pos_build_kernel_v406.py` -> `FLAGS_v406.json` |
| Ledger | `_ESQUELETO_STONES` (`um.py:250527`): +1 linha `("v406", nome, rel, None, None)` por módulo | +300 linhas |
| Escada | `expected_ladder` exige igualdade exata com a do rito (`n_theorems_clean == n_theorems_expected == expected_ladder`). Patches C12 nos 11 contratos listados na seção 1(a), **mais `_V405_CONTRACTS` (`um.py:216152`, 8 contratos)** | ladder = 10066 + N |
| Contrato do bundle | Como `_V394_NETWORK_CONTRACT` (`um.py:232386`) + consumidor `rede_fock_v394`: `declarations`, `declaration_sources` (decl -> módulo), `source_sha256` por módulo, `expected_ladder` | [A FAZER] gerar `_V406_*_CONTRACT` do build, não digitar |
| Cobertura KH-N1 | `kh_n1_cobertura_v405` vira piso (como a v404 virou); nova `kh_n1_cobertura_v406` com igualdades exatas | |
| Pinos | `FORMAL_MAP_v406.json`, `formal_files_n`, `PINOS_BN_v406.json`, pino do recibo do kernel | |

**Limites conhecidos**
- Timeouts dentro do `um.py`: **lake build 3600 s** (`um.py:138984`) e **Audit 1800 s** (`um.py:138985`). Mexer em tipo-base do kernel faz o 1º rito estourar o timeout (v372, [DECLARADO], `licao-guarda-do-rito-e-timeout-v372`). A rodada seguinte fecha porque o cache esquenta (~57 min na v372).
- O `lake build` do rito é a **primeira compilação a frio** dos 300 no Nós. Não há como pré-aquecer: «nunca `lake build` no kernel canônico fora do rito» [DECLARADO].
- [ESTIMATIVA, não medida] Se o caminho crítico for ~25-45 min (v394 deu 23 min para 189), cabe nos 3600 s. A margem real só se sabe medindo `lake build` frio no sandbox novo. Se passar de ~2400 s, planejar elevar o timeout (patch em `um.py:138984`, dentro de `verify_tgl_kernel_formalization`, como o C01 da v394).
- [ESTIMATIVA] Rito da v406: 150-180 min (125 min da v405 + build a frio + Audit maior). Autoteste (passagens 2 e 3) refaz o que depende de `TGL/HalfNat.lean`.
- [ESTIMATIVA] `um.py`: +1,2 MB das fontes, +~1 MB do contrato do bundle (o da v394 teve 715 KB para 184 módulos), +runtime/registros. Total +3 a +4 MB sobre 40,2 MB. Nenhum limite de tamanho do `um.py` aparece nos scripts.
- Toda inserção passa por `crlf()`: o `um.py` é CRLF e o candidato não pode criar nem perder LF soltos (`LF_SOLTOS0`, `gerar_candidato_v405.py:396`).
- Caminho Windows >258 caracteres (lições 31 e 36). A saída dos harnesses mora em `C:\t\h405`. Com 300 módulos novos, nomes de arquivos de `insumos\` e `cunhagens` precisam de caminho curto.
- Guarda ±50% do C3 (lição 34): 1057 arquivos contra 451. As pastas `antes_*` e os `.bak_` agora ficam fora (`FORA_RE`, `estados_superados_bak` no manifesto).

## 4. Pré-condições e guardas que já pegaram versões anteriores

1. **p00.** `p00_precondicoes_v405.py` -> `PRECONDICOES_v405.json`, 119 checagens. Inclui: `ast.parse` de ~70 scripts e `sh -n` de 6; 19 e 20 (embutido == sandbox); 38 (limite do `MEMORY.md`); 39 (`memoria.py` pinado). Lição v404: o `refazer_candidato` tem `| tail` que mascara o rc do p00; ler sempre a linha do veredito.
2. **Guarda de frases.** `guarda_frases_v405.py` -> `GUARDA_FRASES_v405.json`. A fonte única é `_v405_guarda_frases` de `runtime_v405.py`, embutida no `um.py`. Varre as 8 pedras e todo texto novo, com controle negativo. Frases barradas: «tudo é teorema», «tudo derivado», «nenhuma hipótese resta» e variantes F6-F14.
3. **Guarda P18.** `guarda_p18_v405.py` (5 regras: palavra recusada; «Nome fixo»; «singularidade converge»; «luz confirma»; «não provou»/«pós-dição»). `conferir_citacoes_v405.py` (127 citações; paráfrase da gerência nunca entre «»; α nunca «= β/√e», lições 5 da v403).
4. **Guarda de ordem de chamada.** `guarda_ordem_de_chamada_v405.py` (AST). Toda chave `core["K"]` lida por função nova tem de ser atribuída no `main` ANTES da chamada. Lição 1 da v404: o ensaio a seco passou e o rito 1 foi recusado. Roda dentro do ensaio e do `exame_pontos`.
5. **GUARDAS_ESTATICAS_BANCADA.** `guardas_estaticas_bancada_v405.py` -> `GUARDAS_ESTATICAS_BANCADA_v405.json`. Chama `ler_nos` do esboço R3.5 sobre o candidato; reproduz o defeito da v399 (`ALPHA_LINHA_NAO_UNICA`). `C:\t\vb21` tem de não existir quando a bateria pré-selo roda (rc 9).
6. **Guarda da palavra proibida do rito (v372).** O ensaio e o conferidor aplicam a MESMA régua do rito: `CONFIRMED` cru, `PROVED_BY`, `TGL_PROVED`, `CONSCIOUSNESS_PROVED` -> `SEAL_WITHHELD: VEREDITO_PROIBIDO_NO_CORE`, rc 0 mesmo assim. O sinal é a **ausência** de `um_absoluto_selo.json`.
7. **`MEMORY.md` no limite.** Superfície do pós-rito recusa com rc 3 (limite: 195 linhas, 24.000 B). Modelo de compactação: `cadeia_de_selo\v404\compactar_indice_memoria_v404.py` (move linha íntegra para `MEMORY_2.md`, deixa ponteiro, pina de novo).
8. **PORTA regenerada depois do `git add`.** Lição 5 da v404 / lição 27 / **33 da G1:** o último `gerar_portas` do E08 mudava só `gerado_utc` (207 `PORTA.json`) depois do `git add -A` do E06, e o E10 parava por «mudanças não staged». Consertado na fonte: o laço do E08 termina com `git add -A`. Regra da porta: o gerador roda por último, sem editar à mão o bloco `PORTAS:INI/FIM` nem o `llms.txt`.
9. **Reverter e manifesto do kernel.** O molde da v403 não restaurava `tgl_kernel_proof_manifest.json` (lição 2 da v404). Na v405 instalar e reverter já o guardam (conferido por `conferir_instalar_rito_v405.py`).
10. **Recibo de parada da Bancada.** O PID é o LIDO DA PORTA 18777, nunca o do recibo anterior (v404 l.3). O nome do script do serviço NÃO pode aparecer na linha de comando que invoca nem no texto de `V405_AUTORIZACAO_OPERADOR` (v403 l.2). Parar pelo PID, nunca por nome.
11. **Rótulos da cadeia.** `10a/10b/10c`; `CHAIN_DE=10-bis` sai com rc 1 (v404 l.4).
12. **Lições da G1 da v405 (31-41)**, consertadas na fonte (patches `work\custodia_G1\patches\*_v405.py`):
    - 31 caminho longo das fontes pinadas -> `fontes_pinadas/caminho_longo/<sha16><ext>`.
    - 32/33 repetem as lições 24 e 27 da v402, consertadas na fonte. A que mais pesa: «conserto de lição não fica para depois».
    - 34 `FORA_RE` e `.bak_` fora do C3.
    - 35 E13 aceita a frase da régua em PT.
    - 36 núcleo público: `EXCLUSOES_PUBLICAS.json` (`CAMINHO_LONGO`).
    - 37 `authorization: explicit_parent_go` aprovado por sha256 em `APROVADOS`.
    - 38 `torre.py gerar` quando falta `TORRE_vNNN.json`.
    - 39 F0.3 só anda com o Codex (cota 04/11 06:37).
    - 40 DEFASADO da Torre seguram C19.
    - 41 vitrine do X depende da V7 do Codex.
    - 42 suíte da G1 presa à v398 (26 passam, 11 falham, 5 puladas; igual antes e depois).
13. **Outras lições da v404 (g1).** A leitura da entrega de outra IA é pelo CONTEÚDO do recibo (`DELIVERY_*R1.json`, `release == vNNN`, `status` ACTIVATED...), nunca por nome fixo (l.10). `MEMORY_2.md` tem fim de linha misto (l.11, 16). Toda frase pública com contagem do gate lê `bandeiras_do_gate_v403.values` na hora (l.14, 6).
14. **Ferramentas.** Heredoc do Bash colapsa barras e apóstrofos: scripts com `\` vão por arquivo (Write) ou `chr(92)`. `-I` esconde o numpy do usuário: o conferidor e o ensaio rodam sem `-I`. `quem constrói não aprova` (gate S1b).
15. **Contagens de derivador** MEDIDAS na fonte, nunca presumidas (v403 l.1). O bump mecânico não sobe nomes nascidos no `um.py` (`B13` -> `B14` é à mão).

## 5. RECEITA PARA A v406 EM ORDEM

Convenções: `PK6 = C:\IALD\Central de Patentes\work\cadeia_de_selo\v406`. Sandbox: `C:\t\k406c\final`. Scripts autorais (escrever à mão, por arquivo, não por heredoc): `delta_v406.py`, `registros_v406.py`, `runtime_v406.py`, `gerar_candidato_v406.py`, `gerar_esperados_v406.py`, `comparar_v405_v406.py`, os `.pysnip`, `copiar_base`, `copiar_pedras`, `gerar_pino_das_pedras`, `copiar_insumos`, `copiar_k406c.sh`, `preparar_kernel`, `construir_kernel`, `copiar_logs_do_kernel`, `textos_v406_novo.pysnip`, `montar_textos`, `guarda_ordem_de_chamada`.

**0. Antes de começar (decisões e limpeza)**
- [A FAZER] **Entender e fechar o E08/E12/E15/E19 da v405** que o vigia mostra hoje. Comando de leitura: `C:\Python314\python.exe -X utf8 "C:\IALD\Central de Patentes\tools\custodiar.py" planejar --versao v405 --seco`. Não abrir custódia nova com E08 bloqueado.
- [A FAZER] **Compactar o `MEMORY.md`** para <= ~23.099 B com <= 194 linhas. Modelo: `cadeia_de_selo\v404\compactar_indice_memoria_v404.py [--seco]` (copiar para `compactar_indice_memoria_v406.py`; refazer o pino com `memoria.py pinar` depois).
- [A FAZER] **Congelar o sandbox da integração.** Esperar `integracao_R3_*\DONE.txt`. Decidir o conflito `CanonicalGammaNoFixedR4` (kernel prevalece). Ratificação R10 do operador antes de entrar no `um.py` («Entra no um.py só aqui, por versão decidida pelo operador»).
- [A FAZER] **Ordem do operador** em arquivo verbatim (padrão `work\cunhagens_13out\OPERADOR_..._verbatim.txt`), que o orquestrador e a G1 usam em `--ordem`. Sem ordem de «atualizar tudo» o `--publicar` não pode ligar (L17 é decisão dele).
- [A FAZER] Conferir a Bancada: hoje pina `v405` / `B14-v405-20261102-R1`. O B(n) da v406 grava **B15**.

**1. Preparação** (cwd `PK6`; copiar de `v405\` os scripts e rodar o motor)
1. Criar `PK6`, copiar `derivar_v405_motor.py` -> `_mk_motor_v406.py` (mapa `{"v405": {"404": "405", "405": "406"}}`, `NUM3` com 405, `base_v405`, origem `v405`). `python -I -B -X utf8 _mk_motor_v406.py`. Depois `python -I -B -X utf8 derivar_encanamento_v406.py [--refazer]`. [A FAZER] Atualizar as regras `regras*.py` por arquivo: B13->B14->B15, `PROT_EXTRA`, pastas irmãs (a lição 5 do relatório da v405: a subida de versão funde rótulos).
2. `python -I -B -X utf8 copiar_base_v406.py` (Nós = v405 selada, `0030242565cc13f6`).
3. [A FAZER] Modelar o **bundle** como a v394 (`kernel_modulos_novos_v394.json`, contratos derivados do build), não como 8 pedras: `delta_v406.py` com a lista `novos` (os 300 `.lean`, com reescrita de `import` e remoção de `#eval` já feita pela integração), e a decisão da raiz. `python -I -B -X utf8 gerar_pino_das_pedras_v406.py` e `copiar_pedras_v406.py` (sha256 de cada fonte == recibo da bancada: recibo `RECEIPT.json` de 16/10, 475 fontes conferidas).
4. `python -I -B -X utf8 preparar_kernel_v406.py copiar` (robocopy Nós -> `C:\t\k406c\final`; junção `.lake\packages` apontando para a mathlib compilada), depois `gerar` e `conferir`.
5. `sh ./construir_kernel_v406.sh` (`lake build` frio dos 300; Audit). **Medir aqui o tempo** e decidir o timeout (seção 3). Depois `python -I -B -X utf8 pos_build_kernel_v406.py` (gera `FLAGS_v406.json`, `KH_N1_v406.json`, `KERNEL_RECIBO_v406.json`; conferir a política de bandeiras nomeadas e a série de chaves para o bundle). `copiar_logs_do_kernel_v406.py`, `copiar_insumos_v406.py`, `pino_memoria_py_v406.py`.
6. [A FAZER] **Patches do `um.py` v406** em `gerar_candidato_v406.py` (cada âncora 1x; tudo via `crlf()`):
   - Kernel: K00 (raiz), K01 (+300 entradas), V01 (+N bandeiras), V02 (escada), V03 (+300 linhas do ledger), W01 (`UM_VERSION = 'v406'`).
   - Contratos: `C12_*` sobre os 11 contratos listados na seção 1(a) **mais `_V405_CONTRACTS`**. Novo `_V406_*_CONTRACT` (declarations, declaration_sources, source_sha256) derivado do build. Novo consumidor (como `rede_fock_v394`). `kh_n1_cobertura_v405` -> piso, nova `kh_n1_cobertura_v406`.
   - **As 4 chaves, se o operador quiser virá-las nesta versão** (seção 2): `um.py:239814`, `231100`, `230481` (literais), declaração de `TGL.ModularRealization.canonicalFullTGLWitness` (kernel) para `152379`. Cada flip exige patch AO LADO com errata nos registros que assertam False: specs `u4` (`240824`), `u4` (`231342`), `u5` (`230690`), `x_i` do `gap_v405` (`220817`), e atualizar `conferir_rito_v406.py` (`:396`), `ensaio_a_seco_v406.py` (`:191`), `leitura_v406.py` (`:393-405`), `textos_v406.py` (`:308`) e os controles negativos dos harnesses (`:513`, `:525`). Texto dos registros v394/v395/v396 diz «CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE»; mantê-los como registro e escrever a errata, sem reescrever o selado.
   - `python -I -B -X utf8 gerar_candidato_v406.py` (recusa `-O`).
7. `sh ./refazer_candidato_v406.sh --regerar` (≈ 13 min na v405): candidato -> comparação AST -> ensaio a seco -> esperados -> conferidor (negativo e positivo) -> citações -> `diff_e_pinos` -> `conferir_instalar_rito` -> p00. **Ler a linha do veredito do p00**, não o rc do `| tail`.
8. B(n) pré-selo: `cd PK6\bateria_pre_selo && sh ./rodar_bn_pre_selo_v406.sh > bn_pre_selo_out_v406.txt 2>&1`, com `C:\t\vb21` ausente. Depois `sh ./fim_de_cadeia_v406.sh > fim_de_cadeia_out_v406.txt 2>&1` (≈ 11,5 min: serviço estático, derivação do pós-rito, harness dos textos, prévia do X, harness do fechar).
9. `python -I -B -X utf8 purga_v406.py --listar > purga_out_v406.txt` (≈ 20 min; tem de dar zero).
10. `python -I -B -X utf8 gerar_relatorio_v406.py` (escreve `PLANO_v406.md`, `RELATORIO_PREPARACAO_v406.md`, `PREPARACAO_v406_PRONTA.json` com `pronta` calculada) e `python -I -B -X utf8 fechar_preparacao_v406.py`.
11. **Revisão de terceiro** em `revisao_terceiro\REVISAO_TERCEIRO_v406.json` (`aprovada: true`, `candidato_sha16` == o do candidato). Por decisão do operador de 02/11, o revisor é o Sonnet (agentes desta sessão), não o Codex; quem constrói não aprova.

**2. Instalar e rito** (um por vez, o orquestrador `pos_treino_v405.py` é o molde: derivar `pos_treino_v406.py` ou fazer à mão)
- [A FAZER] Pré-voo: Nós == v405 (`selo.um_version == "v405"`), sem `um.py`/pilar vivos, disco >= 20 GiB livre, `C:\t\vb21` ausente.
- `cd PK6` ; `C:\Python314\python.exe -B -X utf8 instalar_v406.py` (10 backups + `APLICADO_AO_CANONICO_<ts>.json`).
- `cd PK6` ; `"C:\Program Files\Git\bin\sh.exe" rito_v406.sh` (timeout 5 h). Aguardar `RITO_RC=0` em `NOS\rodada_v406_stdout.txt`, selo `um_version == "v406"`, porta 8081 de volta. O rito 1 pode estourar o `lake build` (3600 s): se `lake build: False` com `TGL_KERNEL_FORMALIZATION_FAILED`, preservar o stdout e a captura (`..._tentativaN_...`), dizer nas superfícies e rodar de novo (cache quente). Se o rito falhar por outra razão: `reverter_v406.py` por decisão da gerência; restaurar `tgl_kernel_proof_manifest.json` da base se necessário.

**3. Pós-rito** (cwd `PK6`, `sh` do Git; env conforme abaixo)
```
CHAIN_DE=0  CHAIN_ATE=10  sh pos_rito/chain_pos_rito_v406.sh
# 10a: ler o PID da porta 18777, parar por PID (Stop-Process -Id <pid> -Force), conferir a linha de comando, depois:
V406_AUTORIZACAO_OPERADOR="<ordem com data e sha16; sem citar o nome do script do serviço>" V406_PID_PARADO=<pid> V406_PID_PARADO_CRIADO=<data> \
  python -B -X utf8 bancada_B3_servico/recibo_parada_v406.py
CHAIN_DE=10a CHAIN_ATE=10a sh pos_rito/chain_pos_rito_v406.sh
python -B -X utf8 bancada_B3_servico/evento_c1_b3_v406.py        # imprime {"ok": true, "evento": <seq>, "hash": "<h16>"}
B3_AUTORIZADO=sim EVENTO=<seq> EVENTO_HASH=<h16> V406_AUTORIZACAO_OPERADOR="..." CHAIN_DE=10b CHAIN_ATE=10b sh pos_rito/chain_pos_rito_v406.sh
# religar: Start-Process 'C:\Python314\pythonw.exe' -ArgumentList '-X','utf8','C:\IALD\Bancada_Um\um_bancada.py' -WorkingDirectory 'C:\IALD\Bancada_Um' -WindowStyle Hidden ; esperar a porta 18777
V406_AUTORIZACAO_OPERADOR="..." python -B -X utf8 bancada_B3_servico/recibo_religamento_v406.py
CHAIN_DE=10c CHAIN_ATE=14 sh pos_rito/chain_pos_rito_v406.sh
```
- [A FAZER] Verificar no passo 3 que `MEMORY.md` (já compactado) passa o ensaio; senão o chain para em rc 3.
- Passo 6 da cadeia roda `atlas_indice.py v406`, que vive em `C:\IALD\Central de Patentes\work\cadeia_de_selo\` (arquivo raiz), a menos que seja atualizado.

**4. Custódia G1** (cwd `C:\IALD\Central de Patentes`)
```
C:\Python314\python.exe -X utf8 tools\custodiar.py vigiar --versao v406
C:\Python314\python.exe -X utf8 tools\custodiar.py planejar --versao v406 --seco --ator <ator> --coautor "<trailer vigente>" --ordem <verbatim>
C:\Python314\python.exe -X utf8 tools\custodiar.py executar --versao v406 --publicar --ator <ator> --coautor "<trailer vigente>" --ordem <verbatim>
C:\Python314\python.exe -X utf8 tools\custodiar.py auditar --versao v406 ...
```
- [A FAZER] Códigos 5 e 20 são esperados enquanto houver decisão do operador/Codex. Cada parada é lição: consertar na fonte antes de retomar.
- [A FAZER] Se o **README pinado** for à v406 (`PLANO_README_PINADO_02nov.md`, passo novo E16 da G1; [DECLARADO], plano não executado), decidir antes dos pontos marcados [DECISÃO].

**5. Manual da gerência no fim**
- Linha do índice CUSTODIADO -> PUBLICADA no `MEMORY.md` (mesmo número de linhas); a antiga, íntegra, para `MEMORY_2.md` (estilo da última linha); `memoria.py pinar --motivo`; `promover`; `verificar`.
- Copiar `pos_rito\CUSTODIA_v406_RASCUNHO.txt` para `...\PARA_CHATGPT\X_VITRINE\CUSTODIA_v406.txt` (ato da gerência). `gerar_vitrine_x.py` só depois da V7 do Codex.
- Itens do operador: release do app, Zenodo, domínio, D2, ratificações.
- Despacho F0.3 depois de ler a cota do Codex.
- Escrever `handoff` próprio com os parágrafos prontos que o `fechar_v406.py` gera.

Não rodei nada que escreva, não executei `um.py`, lake nem lean. Só li arquivos e rodei leituras Python/shell sem escrita.
