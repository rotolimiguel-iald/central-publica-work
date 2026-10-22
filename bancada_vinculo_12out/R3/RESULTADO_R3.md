VINCULO R3 — 13/10

# R3 do vínculo Bancada Um ↔ um.py (F0.6) — achado → conserto → controle negativo → resultado

Construtor da R3: subagente da gerência c1 (sessão 6da8f00d), 13/10/2026. Objeto: os achados N1–N16 da re-auditoria da R2 (`C:\IALD\PROGRAMA_IALD\auditorias\F0.6\AUDITORIA_F0_6_C1_a645d974.md`, sha16 `f2c30295ccea37f5`; relatório `art_a645d974\AUDITORIA_VINCULO_R2_C1.md`, sha16 `4e245f718a9e3467`), sobre o esboço R2 (`sincronizar_bancada.py` sha16 `8c055a45362fe733`).

**Onde escrevi.** Só em `work\bancada_vinculo_12out\R3\` e no sandbox de raiz curta `C:\t\vb3`. O sandbox foi apagado no fim, depois de desfazer as junções (4 criadas, 0 restantes), sem segui-las. As evidências pequenas foram copiadas para `R3\evidencias_sandbox\`.

**O que não toquei.** Nada na Bancada de produção, no Nós, no um.py, no quadro, no mapa, na memória ou no túnel. As listas da produção e do Nós ficaram iguais antes e depois. O manifesto de produção segue `54fc9e27e4599c49` e o livro de eventos real `dafc4b24b5db64fa` (os dois só lidos). Não rodei o um.py nem o selo. Não abri dado observado. Não usei HTTP nem MCP. Não parei nem religuei serviço: o serviço foi simulado, trocando a sonda em processo. Não li confidenciais.

**A palavra recusada da régua** não aparece em nenhum arquivo da R3 (varredura por script com o token montado em RAM; ver §8). Memória ACOM: não fiz `init` nem `transition`, porque a tarefa restringe a escrita a R3 e ao sandbox. O registro da etapa fica com a c1.

**Estatutos.** [REAL] = medido aqui por script · [DERIVED] = composto · [INPUT da gerência] = decisão tomada na encomenda desta R3 · [DECLARADO] = dito na origem e não conferido aqui · [OPEN] = em aberto. Um PASSA vale só na face testada. NOT_FALSIFIED nunca é creditação. Nada aqui move o gate; nenhum σ nasce aqui.

## 1. Veredito dos controles [REAL]

`CONTROLES_NEGATIVOS_R3.json` (sha16 `2da78fc8dd617421`): **TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO**.

- **235 de 235** controles recusam (ou aceitam) como esperado.
- Os **94 da R2** estão todos presentes (94/94), com o mesmo nome; os argumentos foram ajustados às flags novas.
- **141 controles são novos** da R3.
- Tempo: 585 s.

Arquivos medidos:

- `sincronizar_bancada.py` R3: `8894b74cb1e6d5a0`;
- `montar_sandbox.py` R3: `518cd2af4f67093b`;
- `controles_negativos_r3.py`: `9815086af0547a7f`;
- `BATERIA_VINCULO.json`, da R2 e **inalterada**: `61368649456cdd9f`;
- `gerar_canais_mcp.py`, da R2 e inalterado: `1fc12a5fc8da3109`.

## 2. Os runs 1a, 1b e 2, refeitos no sandbox R3 [REAL]

| run | o que | recibo (sha16) | veredito | bateria |
|---|---|---|---|---|
| 1a | pré-selo, ensaio, Bancada **b1** (pina o Nós REAL), Nós real v391 | `2d6d05c83b93d5a8` | `JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA` | BATERIA_PASSA — 14 testes: 13 PASSA, 0 FALHA, 1 n.e. (T16 PASSA; T12–T14 PASSA; T17 NAO_EXECUTADO) |
| 1b | pré-selo, ensaio, Bancada **b2** (pina `nos\`, cópia do Nós v391) | `9d842901a1d8d23a` | `JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA` | BATERIA_PASSA — 14 testes: 13 PASSA, 0 FALHA, 1 n.e. (T16 PASSA; T12–T14 PASSA; T17 NAO_EXECUTADO) |
| 2 | pós-selo, **aplicar** `--sandbox`, b2, com todos os pinos da R3 | `975f1807c32a5582` | `REPINADA_B3__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO` | BATERIA_PASSA — 14 testes: 13 PASSA, 0 FALHA, 1 n.e. (T16 PASSA; T12–T14 NAO_EXECUTADO; T17 PASSA) |

No run 2:

- O `canonical.py` instalado em b2 recusou o pino velho de verdade (`PIN_CHANGED`).
- O evento 717 foi verificado pela cadeia, com o hash do elo conferido (`badd3364953e9711`, N6).
- O recibo pré-selo do run 1b foi conferido por pino (`9d842901a1d8d23a`, N2) e encadeado no manifesto.
- O T17 PASSA pelo recibo do kernel no contrato `KERNEL_RECIBO_R3` (sha16 `3a4afcf92230a914`). O detalhe: «recibo do kernel 3a4afcf92230a914 (KERNEL_RECIBO_R3): versao=v392 rc=0 sorry=0 erros=0 (recontados nos logs); 2 pedras + raiz + Audit == manifesto do kernel 543e643dc0625269 pinado pelo selo e re-hasheados na arvore; statuses e axiomas no trio; cruzado com o recibo pre-selo».
- Foi gravado o manifesto B3 `B3-v392-20261013-R1` (sha16 `9df1b322b3f99a5d`), com backup = o manifesto lido no passo 3 (`73aa4653e6b05f0a`, N4).
- O contrato do kernel ficou encadeado no manifesto (`kernel_recibo_sha256` = `3a4afcf92230a914`).
- β runtime = `0.012031300400803142`, igual bit a bit ao β do contrato instalado.
- Cada teste executado rodou isolado (N5): `-E -P`, ambiente sem `PYTHON*`, cwd numa pasta vazia nova.
- Nenhum `__pycache__` nasceu.

A re-execução (`RUN_2bis_idempotente`) deu `JA_SINCRONIZADA__NADA_A_GRAVAR`.

## 3. Os achados N1–N16: conserto → controle → resultado

N7 é documental: está em `REMISSOES_PLANO_R3.md` (§5 abaixo).

| achado | grav. | o que a R2 fazia | conserto R3 | controles novos | resultado [REAL] |
|---|---|---|---|---|---|
| **N1** | ALTA | O T17 era autodeclarado: 4 campos bastavam e o log não era lido | Contrato `KERNEL_RECIBO_R3` (`CONTRATO_KERNEL_RECIBO.md`). O recibo é pinado por `--kernel-recibo-sha256`. Os logs são **lidos**: o sha confere, e sorry e erros são recontados por script. `rc`, `sorry` e `erros` são int estritos. A toolchain, os `statuses` e o `axiom_report` vêm do `tgl_kernel_proof_manifest.json` **pinado pelo selo**. Os sha DEPOIS da raiz, do Audit e das pedras batem com `formal_files_sha256` e são re-hasheados na árvore. O ANTES é cruzado com o kernel anterior registrado no recibo pré-selo. Os critérios da §4.6 são conferidos como medido == esperado. `um_py_sha256` virou campo **proibido**. O recibo pré-selo passou a trazer `nos.kernel`. | `N1_ler_nos_manifesto_do_kernel_nao_pinado_pelo_selo`<br>`N1_ler_nos_manifesto_do_kernel_pinado_aceito`<br>`N1_sub_kernel_recibo_r2_minimo_4_campos`<br>`N1_sub_kernel_recibo_log_com_sorry`<br>`N1_sub_kernel_recibo_raiz_depois_diverge`<br>`N1_sub_kernel_recibo_arvore_mudou`<br>`N1_unit_kernel_recibo_sorry`<br>`N1_unit_kernel_recibo_versao`<br>… e mais 51 (todos em `CONTROLES_NEGATIVOS_R3.json`) | **59/59 PASSA** |
| **N2** | MÉDIA | O recibo pré-selo era aceito por conteúdo; um JSON escrito à mão passava, também com `--producao` | `--recibo-pre-selo-sha256` (lido de `v392_pins`): obrigatório em `--producao` e em aplicar fora do sandbox; divergente = recusa. | `N2_aplicar_fora_do_sandbox_sem_sha_do_pre_selo`<br>`N2_sha_do_pre_selo_divergente`<br>`N2_decoy_producao_sem_sha_do_pre_selo`<br>`N2_decoy_recibo_pre_selo_escrito_a_mao`<br>`N2_decoy_ensaio_producao_sem_sha_do_pre_selo` | **5/5 PASSA** |
| **N3** | MÉDIA | O serviço era sondado uma vez só, antes da bateria | `guarda_servico(momento)` sonda no início e **imediatamente antes de cada gravação**: backup, contrato, temporário, troca e recibo em `estado\`. Se o serviço voltou: recusa e desfaz (rollback). A porta é lida na hora da chamada. | `N3_decoy_servico_no_ar_no_inicio`<br>`N3_decoy_servico_volta_durante_a_bateria`<br>`N3_decoy_servico_volta_antes_do_contrato`<br>`N3_decoy_servico_volta_imediatamente_antes_da_troca`<br>`N3_decoy_servico_volta_antes_do_recibo_em_estado` | **5/5 PASSA** |
| **N4** | MÉDIA | Atualização perdida: o aplicar comparava com os bytes que ele mesmo acabara de ler | O aplicar compara com `anterior['_raw']` (passo 3) no início e de novo imediatamente antes do `os.replace`: `MANIFESTO_MUDOU_DESDE_A_LEITURA`, e a mudança fica. | `N4_decoy_manifesto_muda_durante_a_bateria` | **1/1 PASSA** |
| **N5** | MÉDIA | Código não pinado executava dentro de testes pinados (`hashlib.py` ao lado; `PYTHONPATH`) | Os testes rodam com `-E -P`, ambiente sem `PYTHON*` e cwd numa pasta vazia nova. A guarda recusa módulo-sombra (`.py`, `.pyc`, `.pyd` ou pacote) da stdlib ou de site-packages ao lado de fonte pinada. O esboço recusa `PYTHONPATH`, `PYTHONHOME`, `PYTHONSTARTUP` e `PYTHONUSERBASE` no próprio ambiente sem `-E`. **Não** usei `-I`/`-S`: numpy, scipy e torch vivem no site do USUÁRIO [REAL, 13/10], e `-I`/`-s`/`-S` os cortariam (limite declarado). | `N5_modulo_sombra_ao_lado_da_fonte`<br>`N5_PYTHONPATH_injetado_nao_chega_ao_teste`<br>`N5_PYTHONPATH_sem_E_recusado` | **3/3 PASSA** |
| **N6** | MÉDIA | A autoria do evento era autodeclarada | [INPUT da gerência] `--evento-hash <hash16>` confere o hash do elo na cadeia. Continuam conferidos tipo, `quem == claude-c1`, versão e Bancada nomeadas. **Isto não é autenticação**: `quem` é convenção do quadro, e o recibo o diz. | `N6_evento_hash_ausente`<br>`N6_evento_hash_divergente`<br>`N6_evento_hash_de_outro_elo`<br>`N6_evento_hash_invalido`<br>`N6_evento_hash_curto`<br>`N6_autoria_declarada_como_convencao`<br>`N6_sub_aplicar_sem_evento_hash`<br>`N6_sub_aplicar_evento_hash_errado` | **8/8 PASSA** |
| **N8** | BAIXA | As raízes de `--saida` eram largas (todo o `work\` e todo o `C:\t`) | [INPUT da gerência] Ficam só `work\bancada_vinculo_12out`, `work\cadeia_de_selo\<alvo>`, `work\<alvo>_bateria` e `C:\t\vb*`, onde o alvo é a versão em `pos_selo` e a seguinte em `pre_selo`. Nunca a pasta do esboço nem as das fontes ou cópias da bateria. A versão só é aceita na forma `vNNN`. | `N8_saida_C_t_fora_do_vb`<br>`N8_saida_C_t_raiz`<br>`N8_saida_work_outra_pasta`<br>`N8_saida_cadeia_de_outra_versao`<br>`N8_saida_pasta_das_fontes_da_bateria`<br>`N8_saida_pasta_da_bateria_R2`<br>`N8_saida_pasta_do_esboco_R3`<br>`N8_saida_pasta_de_fonte_no_tunel`<br>… e mais 11 (todos em `CONTROLES_NEGATIVOS_R3.json`) | **19/19 PASSA** |
| **N9** | BAIXA | Nomes reservados criados como arquivos | `relativo_seguro` recusa, por componente, CON/PRN/AUX/NUL/COMn/LPTn (com sobrescritos), cauda `.`/espaço e caracteres inválidos. | `N9_nome_reservado_em_copias_para`<br>`N9_relativo_seguro_CON`<br>`N9_relativo_seguro_aux_txt`<br>`N9_relativo_seguro_prn_minusculo`<br>`N9_relativo_seguro_COM1_txt`<br>`N9_relativo_seguro_NUL_json`<br>`N9_relativo_seguro_LPT9`<br>`N9_relativo_seguro_COM_sobrescrito`<br>… e mais 5 (todos em `CONTROLES_NEGATIVOS_R3.json`) | **13/13 PASSA** |
| **N10** | BAIXA | O recibo do aplicar seguia junção em `estado\` | `sem_juncao`: pré-voo do manifesto, do contrato e do recibo em `estado\sincronizacao` **antes da primeira gravação**. Nenhum componente léxico pode ser junção ou link, nem para fora nem para dentro. | `N10_estado_juncao_para_fora`<br>`N10_estado_juncao_para_dentro` | **2/2 PASSA** |
| **N11** | BAIXA | O filtro de negação era contornável por NFD e por chaves | A negação é procurada em chaves **e** valores normalizados (NFKC; NFD sem Mn/Cf; caixa dobrada; `_` vira espaço). O conjunto de chaves de `dados` é fechado. A guarda da palavra também normaliza. | `N11_nfd`<br>`N11_largura_cheia`<br>`N11_largura_zero`<br>`N11_chave_negacao`<br>`N11_chave_proibido`<br>`N11_chave_desconhecida`<br>`N11_guarda_palavra_largura_cheia`<br>`N11_guarda_palavra_largura_zero`<br>`N11_json_bytes_palavra_na_chave`<br>`N11_json_bytes_palavra_por_escape`<br>`N11_texto_comum_nao_e_negacao` | **11/11 PASSA** |
| **N12** | BAIXA | Hardlink dos arquivos do Nós noutra pasta admitia `--sandbox` | `pina_o_nos_real` também confere os arquivos (`samefile` do `um.py` e do selo), não só a pasta. | `N12_hardlink_do_nos_recusa_sandbox`<br>`N12_copia_simples_admitida` | **2/2 PASSA** |
| **N13** | BAIXA | `Volume{GUID}` recusado por acidente | Regra explícita: depois do prefixo de dispositivo só se admite letra de disco. `Volume{GUID}` recusa com `CAMINHO_VOLUME_GUID_NAO_ADMITIDO`; GLOBALROOT, pipe etc. com `CAMINHO_DISPOSITIVO_NAO_ADMITIDO`. `\??\C:` é normalizado. | `N13_bancada_volume_guid_prefixo_longo`<br>`N13_bancada_volume_guid_prefixo_ponto`<br>`N13_bancada_globalroot`<br>`N13_bancada_pipe`<br>`N13_saida_volume_guid`<br>`N13_producao_prefixo_nt` | **6/6 PASSA** |
| **N14** | BAIXA | O log era gravado antes da guarda de palavra; o token na bateria dava traceback | A guarda vem antes de gravar o log, e com a palavra o log sai suprimido (só o sha). `fechar` grava um recibo **mínimo** sem a palavra (rc 2), e há pré-voo antes da primeira gravação na Bancada. | `N14_token_na_saida_do_teste_log_suprimido`<br>`N14_token_na_bateria_recibo_minimo` | **2/2 PASSA** |
| **N15** | BAIXA | Mesma versão, mesmo um.py, selo diferente: era re-pinado em silêncio | [INPUT da gerência] `SEAL_CHANGED_SAME_VERSION`, salvo `--reparo-de-pino` em aplicar com evento c1 `dados.reparo=true` que nomeie o selo novo. | `N15_selo_diferente_mesma_versao_ensaio`<br>`N15_selo_diferente_aplicar_sem_reparo`<br>`N15_selo_diferente_reparo_nomeado_aplica` | **3/3 PASSA** |
| **N16** | BAIXA | A guarda de `.py` deixava passar `-c`, `-m`, zip e pasta | Gramática fechada: `{py}`, depois só `-B` e `-X utf8`, depois um `.py` absoluto e pinado. `-c`, `-m`, `-I`, zip, pasta, comando sem `{py}` e `.py` relativo são recusados antes de executar. | `N16_formas_de_comando_fora_da_gramatica` | **1/1 PASSA** |

Os A1 da R2 (`A1_kernel_recibo_invalido_{sorry,versao,log,um_py}`) rodam agora contra o contrato R3. O `um_py` passou a ser recusado como **campo proibido**.

## 4. Decisões da gerência registradas nesta R3 [INPUT da gerência]

- **N6.** A autoria do evento segue **convenção, não autenticação**. O que se endureceu:
  - o B(n) recebe `--evento <n> --evento-hash <hash16>` da cadeia;
  - confere tipo `SINCRONIZACAO_BANCADA`, `quem == claude-c1`, a versão, a Bancada (por identidade), o um.py e o selo nomeados;
  - confere o hash do elo na cadeia, e a cadeia de hash do primeiro elo até ele;
  - limita as chaves de `dados` a um conjunto fechado.

  **Isto não autentica quem escreveu**: `iald.py anotar` aceita `--quem` livre. O recibo do B(n) diz «convencao (quem=claude-c1), nao autenticacao».
- **N8.** As raízes estreitas da §3.
- **N15.** `SEAL_CHANGED_SAME_VERSION`, salvo `--reparo-de-pino`.

## 5. Documentos

- **`CONTRATO_KERNEL_RECIBO.md`** (sha16 `a6a3f1ba3254b576`): os campos que `construir_kernel_vNNN.sh` tem de escrever e o que o B(n) confere, em ordem. Atende o §5 da re-auditoria.
- **`REMISSOES_PLANO_R3.md`** (sha16 `1806fdb58a589886`): texto pronto para a gerência aplicar **ao lado**, sem editar o plano. Substitui `R2\REMISSOES_PLANO.md`. Cobre:
  - o comando completo (com `--bancada`, `--bateria`, `--saida` e as flags R3);
  - §3: a bateria R2/R3 substitui a H12;
  - §4: o contrato do kernel;
  - §5: o que `v392_pins` pina;
  - §11: a numeração 9 → 10 → 10-bis-a (parada com recibo) → 10-bis → 10-ter → 11 Fechar;
  - §12, item 1, contra o 12-bis;
  - a errata ao lado dos itens 1 e 4 do 12-bis, com a regra R2/R3 do evento;
  - §14;
  - a ressalva do cabeçalho falso.
- **`DIFF_R2_R3.patch`** (sha16 `c9af70b18fda6dd6`): todos os `.py` da R2 para a R3: `sincronizar_bancada.py`, `montar_sandbox.py` e `controles_negativos_r2.py` → `controles_negativos_r3.py`. `gerar_canais_mcp.py` e `gerar_bateria.py` não mudaram e não têm hunk. A aplicação com `git apply` sobre uma cópia da R2 foi conferida bit a bit (§8).
- **`DIFF_R1_R2_montar_sandbox.patch`** (sha16 `0d3820d956aaa60b`): a omissão da R2, o `montar_sandbox.py` da R1 para a R2.

## 6. O que NÃO fiz, e por quê

- **Autenticação do evento (N6).** Fica convenção: é decisão da gerência e precisa de mecanismo fora do esboço (assinatura, ou o evento ligado ao `request_id` da sessão na memória ACOM).
- **`-I`/`-S` nos testes (N5).** Cortariam numpy, scipy e torch, que estão no site do usuário. Uso `-E -P` mais ambiente limpo mais a guarda de módulo-sombra.
  - [OPEN] O site do usuário segue gravável por qualquer processo desta conta. Um `.pth` ou `usercustomize` ali executaria nos testes.
  - A custódia da bateria numa pasta selada da cadeia é a derivação para `cadeia_de_selo\v392\vinculo\`, ato da gerência.
- **Recibo de parada do serviço exigido por flag (N3).** O esboço só sonda a porta. O recibo da parada (10-bis-a) é ato do operador e fica no `fechar` (Remissão 4).
- **Corrida TOCTOU dentro de `caminho_canonico`** (troca de junção entre a guarda e o `mkdir`). Não está coberta, e o resíduo fica declarado. O pré-voo de `sem_juncao` reduz a janela no aplicar.
- **Link simbólico.** Não testado: sem privilégio nesta conta. Junção, hardlink e `subst` cobrem a classe.
- **T17 com kernel real, aplicar na produção real, religamento do serviço e reconexão MCP.** Nada disso foi feito: é proibido aqui. A produção foi simulada por decoy **em processo** numa cópia (`pd\`).
- **`construir_kernel_v392.sh`, `derivar_cadeia_v392.py`, o registro no mapa e a edição do plano.** São atos da gerência: escrevi os textos e o contrato, não os apliquei.

## 7. Atos do operador

- **B3:** autorizar o primeiro re-pino da produção sob evento c1. Sem isso, a cadeia da v392 para em 10-bis-a (`AGUARDA_OPERADOR`), e a custódia espera.
- **A parada do `um_bancada.py` com recibo (10-bis-a), o religamento com recibo de identidade (10-ter) e a reconexão dos adaptadores MCP.**
- **O que entra na implantação B3 de código:**
  - a rota genérica;
  - a unicidade de α e de `UM_VERSION` no `canonical.py`;
  - a custódia da bateria junto da Bancada;
  - o README;
  - a sobra D6 da F7.2.
- **Se a ordem permanente de 12/10 vale da v393 em diante.**

## 8. Pinos, sandbox e varreduras [REAL]

- **`PINOS_R3.json`** (sha16 `225022f85850942d`): 116 entradas medidas por script, 0 ausentes. As 54 fontes e cópias pinadas na bateria: 54 conferem com o disco.
- **Produção e Nós:** listas iguais antes e depois dos controles. O manifesto de produção é `54fc9e27e4599c49`.
- **Livro de eventos real:** `dafc4b24b5db64fa` durante os controles (só lido; ele é vivo).
- **Sandbox `C:\t\vb3`:** as junções foram desfeitas pelo próprio script dos controles (`os.rmdir` no link, nunca no alvo). A árvore foi apagada sem seguir junção. O que ficou de evidência está em `R3\evidencias_sandbox\`.

- **Verificações finais** (`VERIFICACOES_FINAIS_R3.json`, sha16 `d22f887511ce35a7`):
  - evidencias_copiadas: 83
  - juncoes_no_sandbox_antes_de_apagar: 0
  - sandbox_apagado: True
  - diff_R2_R3: patch sha16 `c9af70b18fda6dd6`, 286240 B; `git apply` rc 0; reproduz bit a bit: True. a R2 tem sincronizar_bancada.py, gerar_canais_mcp.py e gerar_bateria.py em CRLF: o patch aplica sobre a R2 NORMALIZADA para LF e reproduz os .py da R3 bit a bit; gerar_canais_mcp.py e gerar_bateria.py nao mudam (sem hunk)
  - diff_R1_R2_montar_sandbox: patch sha16 `0d3820d956aaa60b`, 16431 B; `git apply` rc 0; reproduz bit a bit: True. a omissao da R2 (re-auditoria, ressalva BAIXA): o montar_sandbox.py da R1 para a R2, sem normalizar (os dois em LF)
  - palavra_guardada_em_R3: []
  - confidenciais_em_R3: []
  - producao_manifesto_sha256: 54fc9e27e4599c49990adb9587a45a8858393f2d8f5d66ec3e022b8140757c1b
  - quando: 2026-10-13T06:58:53

Nada aqui é leitura física. NOT_FALSIFIED nunca é creditação. O gate não se move.
