# ESPEC_CENTRAL — a perna Central da custódia do um.py (privada, pública e quadro)

**Para:** o workflow G1 do organismo (`custodia.py <vNNN>` parametrizado; CLI `tools\custodiar.py`; pacote `tools\custodia_g1\`).
**Escrita em 24/10/2026 09:40** (hora local), por subagente de leitura. **Só leitura do que existe**: nenhum arquivo existente foi alterado; nenhum commit, push, subida, `--publicar`, ACOM ou mapa de rotas foi tocado. Os rascunhos de medição ficaram no scratchpad da sessão, fora do repositório.

**Estatutos usados:** `[REAL]` medido aqui, por leitura ou por script somente-leitura; `[DECLARADO]` dito por docstring, comentário ou memória e não reexecutado aqui; `[PROPOSTA]` desenho a implementar (ainda não existe). Nenhum hash, pino ou contagem foi digitado de memória: os `sha16` de §1 foram calculados por script na hora da escrita; as contagens vêm dos arquivos citados.

**Convenção de nomes neste documento:** `vNNN` = versão nova a custodiar; `vANT` = o maior cofre `um_unificado_v*` que já existe e é menor que `vNNN` (não necessariamente `NNN-1`: a custódia conjunta v392→v394 teve base v391); `CEN` = `C:\IALD\Central de Patentes`; `NOS` = `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós`; `OC` = `CEN\vault\originals_copy`; `W` = `CEN\work\custodia_<vNNN>_<DDmes>\` (hoje `custodia_v397_23out`); `MEM` = `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory`.

**Índice:** §0 em uma página · §1 fontes lidas · §2 regras transversais · §3 fluxo, dependências e tempos · §4 contratos de dados (`fatos` schema 2, `FATOS_CUSTODIA`, `SEMANTICA_CUSTODIA`, recibos, moldes e portão de texto) · §5 os passos C0 a C20 (comando, entradas por versão e origem, saídas, idempotência, gates, prosa manual → molde) · §6 pedra genérica do runner · §7 item genérico do módulo dos dispositivos · §8 testes de aceitação e ordem de implementação · §9 o que é do operador · §10 lacunas (L1 a L31).

---

## 0. Em uma página

**O que existe hoje [REAL].** A perna Central de uma custódia é uma sequência de 21 operações em ordem fixa (§3). Na v397, para fazê-las, a gerência: derivou **por trocas contadas** do script da versão anterior cinco scripts (cofre 34 trocas + 1 regex; medir 2; snapshot 3; conferência final 14; registro "publicada" 10 = **63 trocas + 1 regex**), mais `acom_transicao.py` (3 trocas) e `rodar_16` (por `sed` no scratchpad); **escreveu à mão** o patch do runner (14,4 KB), o patch do módulo dos 16 dispositivos (8,7 KB), o registro nas superfícies (12,3 KB), três JSON de transição ACOM (11,3 KB), a rota (4,8 KB) e a mensagem de commit (1,2 KB); e rodou cinco ferramentas fixas (`build_final_code.py`, `ledger_de_pinos.py`, `rodar_finais_v394.py`, `atualizar_central_publica.py`, `estado_do_organismo.py`). Do disparo (handoff 17:17) ao commit da Central (18:20) correram **63 min**; a Central pública (1h45) correu depois.

**O que a leitura mostra ser parametrizável [REAL, medido].** Apliquei, em script somente-leitura, a parte *mecânica* da pedra do runner (blocos novos bem formados, bandeiras, cobertura kh, escada, kernel, registro PT/EN, mudanças de veredito, gate, `CONFIRMED`, `checks` e `guarda_p18_violacoes` dos blocos) às transições **v394→v395, v395→v396, v396→v397 e v397→v398** lendo só os cofres (o da v398 foi emitido pela sessão em curso enquanto eu lia): **passa nas quatro, sem semântica por versão**; a única ressalva, que o gerador deve tratar, está em §6.2, item S8: o veredito de `estatuto_da_prova_v391` muda a cada versão no *pino autocertificado*, e o texto PT do artigo corta esse pino; o gerador tem de ler o veredito do `core` (inteiro) e normalizar dígitos **e** pino.

**O que não é parametrizável.** (a) o *sentido* das negações de cada registro novo (hoje codificado à mão na função `_v397(c)` da pedra e em `conferir_v397_no_cofre`); (b) a prosa de docstrings, do veredito do runner, do `nao_se_afirma`, do ESTADO e da rota; (c) os gates que a régua reserva ao operador (§9). Para (a) e (b) proponho **molde + rascunho mecânico `DECLARADO` + revisor distinto** (§4.3, §4.5), e a prosa citada **verbatim do `HANDOFF_vNNN_CUSTODIA.md` e dos campos `diz/nao_diz/limites/erratas` do próprio `core`**, nunca composta.

> [nota operacional do operador — omitida no retrato público]

**Defeitos medidos agora (detalhe em §10).** L1: os `CUSTODY_MANIFEST.json` dos cofres v394–v398 saem com `registros_novos_vNNN = {}` e `pilar_quantico.* = null` por um erro de uma linha (`core` lido do arquivo, não de `["core"]`); o `cofre_v398.py` da custódia em curso repete. L2: o registro não é idempotente. L3: números do console entram no texto sem recibo. L4: o `combined_sha256` dos FINAL não é reprodutível. L5: `git add -u patents memory` varre modificações alheias.

---

## 1. Fontes lidas

| arquivo | bytes | sha16 | papel | como foi lido |
|---|---|---|---|---|
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\sondar_v397.py` | 5982 | `a1f1bd2b39f6d06a` | C1 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\fatos_v397.json` | 2410 | `27e107f4c3d8f0eb` | C1, §4.1 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v398_24out\fatos_v398.json` † | 3357 | `da3793d738ddf6d2` | §4.1 (v398) | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\cofre_v397.py` | 12672 | `544c3f5a706c8d25` | C3 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\medir_v397_contra_v396.py` | 3334 | `3b0a844101dde3f1` | C4 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\snapshot_chatgpt_v397.py` | 5722 | `2a51cccdb2a76569` | C5 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\snapshot_chatgpt_v397_saida.txt` | 258 | `2350622f886222c6` | C5 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\patch_runner_v62.py` | 14407 | `260464a4c097dc36` | C6, §6 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\patch_formula_v397.py` | 8660 | `075a51962662b8f1` | C8, §7 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\registro_v397.py` | 12329 | `d8a511f3a72e0263` | C13 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\registro_v397_publicada.py` | 3893 | `3a84866eefdb59ae` | C16 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\conferencia_final_v397.py` | 5590 | `e035858935e45949` | C15 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\CONFERENCIA_FINAL_v397.json` | 1518 | `981e5d0ff296dd96` | C15 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\acom_init.py` | 1478 | `d7f5a5263913b4cd` | C2 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\acom_transicao.py` | 2000 | `83d26a30c98225f8` | C17 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\acom_t1.json` | 4544 | `a33a010a2706fc3d` | C17 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\acom_t2.json` | 2061 | `2547477799b85ac6` | C17 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\acom_t3.json` | 4670 | `23484c8a485b0769` | C17 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\derivar_central_v397.py` | 13959 | `d98dac8549cb8476` | taxonomia das trocas | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\derivar_passo0_v397.py` | 1815 | `e1b92905097dbb0f` | perna 1 (contagem de trocas) | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\derivar_espelho_v397.py` | 4229 | `7048daa1a0bd6e48` | perna 1 (contagem de trocas) | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\rota_custodia_v397.json` | 4833 | `73d7774c42957429` | C13 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\central_publica_v397_saida.txt` | 3440 | `63f50c2306e625c6` | C18 (tempos) | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\runner_v62_r1.txt` | 48068 | `c81fc2f0285d264f` | C7 | grep e diff |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\runner_v62_r2.txt` | 48068 | `06b865398103ae63` | C7 | grep e diff |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\apendices_memoria_23out_noite.py` | 2981 | `1f84a61ea8da5108` | C13 (apêndices) | integral |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\registro_x_e_gatilho_23out.py` | 5817 | `9d28b8d980871b5a` | C13 (apêndices) | parcial |
| `C:\IALD\Central de Patentes\work\custodia_v396_22out\cadeia_v395_comandos.txt` | 13433 | `68b9c702d13106c0` | ordem dos comandos (v395) | 150 primeiras linhas |
| `C:\IALD\Central de Patentes\work\custodia_v396_22out\sondar_core_v396.py` | 1735 | `f725edaabeff54ff` | C1 | integral |
| `C:\IALD\Central de Patentes\work\custodia_v396_22out\derivar_fim_v396.py` | 6165 | `b580f581a86a1f8b` | C15, C16 | início |
| `C:\IALD\Central de Patentes\work\custodia_v396_22out\registro_v396.py` | 12162 | `95fa92d374db6e79` | C13 | por diferença |
| `C:\IALD\Central de Patentes\work\custodia_v396_22out\patch_runner_v61.py` | 13590 | `5ebb19744b332c6f` | C6 | por diferença |
| `C:\IALD\Central de Patentes\work\custodia_v396_22out\patch_formula_v396.py` | 8447 | `8b07719147b222dc` | C8 | por diferença |
| `C:\IALD\Central de Patentes\work\custodia_v396_22out\cofre_v396.py` | 12575 | `2c88d177d4878d5c` | C3 | por diferença |
| `C:\IALD\Central de Patentes\work\custodia_v396_22out\rota_central_publica_v396.json` | 3720 | `6079c8052ea10741` | C18 | integral |
| `C:\IALD\Central de Patentes\tools\build_final_code.py` | 10410 | `b1cac7b7aa380493` | C10 | integral |
| `C:\IALD\Central de Patentes\tools\ledger_de_pinos.py` | 7501 | `09a94e540a05c309` | C12 | integral |
| `C:\IALD\Central de Patentes\tools\estado_do_organismo.py` † | 31629 | `c513b41d379a0ece` | C19 | integral |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\rodar_16_v396.py` | 1846 | `dfd3849e172978c4` | C9 | integral |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\rodar_16_v397.py` | 1846 | `e9d59ee2ca056132` | C9 | integral |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\rodar_finais_v394.py` | 1326 | `63abda382743fa64` | C11 | integral |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\commit_central_v397.txt` | 1158 | `9fb3fd34d58c2459` | C14 | integral |
| `C:\IALD\Central de Patentes\fronteira_tgl\runner\one_fronteira.py` † | 777668 | `24e3962c5c1e490d` | C6, C7, §6 | parcial (as funções _medir_v396/_v397_custodia, repin, station, veredito) |
| `C:\IALD\Central de Patentes\patents\_formula_completa\tgl_formula_completa.py` † | 63369 | `7226c7b8f507835e` | C8, §7 | parcial (conferir_v396/v397, camada, USOS) |
| `C:\IALD\Central de Patentes\work\central_publica_22out\atualizar_central_publica.py` | 6989 | `968cdc13ee88bc49` | C18 | integral (+ --listar executado) |
| `C:\IALD\Central de Patentes\work\central_publica_22out\rodar_incremental.py` | 2412 | `16f81e6d18c7a13d` | C18 | cabeçalho |
| `C:\IALD\Central de Patentes\organismo\ORGANISMO_TORRE_DE_COMANDO.md` † | 17655 | `793a2ea849309146` | G0 a G4 | parcial (§3) |
| `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\HANDOFF_v398_CUSTODIA.md` † | 19061 | `29cc6c45ec520aa7` | §4.5, C0 | estrutura e cabeçalhos |
| `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\HANDOFF_v397_CUSTODIA.md` | 13643 | `5efc1157be1b0eb0` | §4.5, C0 | cabeçalhos |
| `C:\IALD\MAPA_DE_ROTAS\rotas.py` | 25186 | `50c29fa871abb34b` | C13 | modelo e registrar |
| `C:\IALD\MEMORIA_IALD\README.md` | 8998 | `a4bf3c1bbfe3a442` | C2, C17 | integral |
| `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\custodiar-quando-o-handoff-aparecer-23out.md` | 3876 | `9599c71a99c136c6` | regra do operador | integral |
| `C:\IALD\Central de Patentes\work\custodia_v398_24out\sondar_v398.py` † | 5982 | `1716dbd760feb06f` | §4.1 | por diferença |
| `C:\IALD\Central de Patentes\work\custodia_v398_24out\cofre_v398.py` † | 12710 | `fa845054ff608e56` | L1 | linha 56 |
| `C:\IALD\Central de Patentes\work\custodia_v398_24out\patch_estado_pernas_do_selo.py` † | 2331 | `80a00147a0457822` | C20 | integral |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\g1_tmp\medir_mecanico.py` | 4394 | `c6647e72537fd475` | medição S1 a S14 (§6.2) | scratch, não versionado |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\g1_tmp\medir_v398_nos.py` | 3186 | `bd7ae915bfc6eee9` | medição v398 (§6.2) | scratch, não versionado |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\g1_tmp\medir_mecanico_v398.py` | 4359 | `f779096b34e95184` | medição v398 sobre o cofre (§6.2) | scratch, não versionado |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\g1_tmp\checks_blocos_v398.py` | 1150 | `df95ac76ad91dd3f` | checks da v398 (§6.2 S3) | scratch, não versionado |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\g1_tmp\dif_core_v398.py` | 1387 | `03526a70d274baa3` | medição do pino (§6.2) | scratch, não versionado |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\g1_tmp\igualdade_blocos2.py` | 2068 | `bf99fcc4bc1470ed` | medição de reescrita de blocos (§7.1) | scratch, não versionado |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\g1_tmp\ancoras2.py` | 2616 | `bb257dbb9ba370a9` | contagem de âncoras (§6.7, §7.4) | scratch, não versionado |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\g1_tmp\tempo_ast.py` | 752 | `04fe89532484889b` | custo do ast (§4.1) | scratch, não versionado |
| `C:\IALD\Central de Patentes\work\custodia_G1\ESPEC_ESPELHO_SITE.md` † | 109329 | `78bb0ebcfe6cb9ab` | alinhamento entre pernas (§5, §6, L10, L11, L15, L17, L20) | §2 E00, §5, §6, §8 |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\g1_tmp\kh397.py` | 1637 | `fbddc4fba14d1d7e` | reescrita de kh_n1_cobertura_v397 (§7.1) | scratch, não versionado |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\g1_tmp\checks_blocos.py` | 1185 | `9f55c03edab6902b` | checks e guarda_p18 dos blocos novos (§6.2 S3) | scratch, não versionado |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\g1_tmp\contar_trocas.py` | 1553 | `0c1451946c4c1a9a` | contagem das trocas contadas (§0) | scratch, não versionado |
| `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\g1_tmp\extrair_v397.py` | 1585 | `0b0f5fd5b44fa118` | comandos da v397 no transcrito (§3.3) | scratch, não versionado |

† em obra por outra sessão (a v398 está sendo custodiada agora): o hash é o do momento da escrita deste documento, não necessariamente o do momento da leitura. Os demais arquivos não foram tocados durante a leitura.

Lido só por diferença (contra a v397): `patch_runner_v61.py`, `patch_formula_v396.py`, `registro_v396.py`, `cofre_v396.py`, `snapshot_chatgpt_v396.py`, `registro_v396_publicada.py`, `conferencia_final_v396.py`, `medir_v396_contra_v395.py`. Não lidos por serem de outras pernas ou de outra tarefa: `patch_readme_v397*.py` (espelho), `registro_final_php_v396.py` (PHP), `custodia_v398_24out\*` (outra sessão em curso: só listado, mais `fatos_v398.json`, `sondar_v398.py`, o `patch_estado_pernas_do_selo.py` e a linha 56 de `cofre_v398.py`).

---

## 2. Regras transversais (valem para todo passo)

> [nota operacional do operador — omitida no retrato público]

## 3. O fluxo: passos, dependências, tempos medidos e chamada

### 3.1 Os 21 passos (C0 a C20)

| id | passo | script de hoje (v397) | tipo hoje |
|---|---|---|---|
| C0 | disparo e pré-condições (as três marcas) | laço de leitura na sessão + `estado_do_organismo.py` | sem script único |
| C1 | sondagem → `fatos_vNNN.json` | `sondar_v397.py` | derivado por edição |
| C2 | inscrição ACOM (`init`) | `acom_init.py` | derivado |
| C3 | cofre `um_unificado_vNNN` + `tgl_kernel_vNNN` | `cofre_v397.py` | derivado (34 trocas + 1 regex) |
| C4 | medição cofre × cofre | `medir_v397_contra_v396.py` | derivado (2 trocas) |
| C5 | snapshot incremental do `Chatgpt\` | `snapshot_chatgpt_v397.py` | derivado (3 trocas) |
| C6 | runner da Fronteira: repin + pedra nova | `patch_runner_v62.py` | **à mão** |
| C7 | runner, duas execuções | `fronteira_tgl\runner\one_fronteira.py` | fixo |
| C8 | módulo dos 16 dispositivos: camada nova | `patch_formula_v397.py` | **à mão** |
| C9 | os 16 dispositivos | `rodar_16_v397.py` (scratchpad) | derivado por `sed` |
| C10 | os 16 `*_FINAL.py` (build) | `tools\build_final_code.py` | fixo |
| C11 | os 16 `*_FINAL.py` (rodar) | `rodar_finais_v394.py` (scratchpad) | fixo |
| C12 | ledger de pinos | `tools\ledger_de_pinos.py` | fixo |
| C13 | registro nas superfícies (diário, memórias, Atlas, MEMORY, rota) | `registro_v397.py` | **à mão** |
| C14 | commit e push da Central | `git add/commit/push` + mensagem | **à mão** |
| C15 | conferência final independente | `conferencia_final_v397.py` | derivado (14 trocas) |
| C16 | registro "publicada" | `registro_v397_publicada.py` | derivado (10 trocas) |
| C17 | transições ACOM t1, t2, t3 | `acom_transicao.py` + `acom_t1/t2/t3.json` | derivado + **à mão** |
| C18 | Central pública (3 repositórios, `/central/`, `um.acom`) | `atualizar_central_publica.py --publicar` | fixo (27 passos) |
| C19 | Nós vivo e quadro do organismo | `NOS_VIVO\construir.py`; `tools\estado_do_organismo.py` | fixo |
| C20 | pernas que o selo já puxa (Bancada Um; memória canônica da fila) | — | só conferir |

### 3.2 Dependências

```
C0 ─┬─ C1 ─ C2 ─ C3 ─┬─ C4
    │                ├─ C6 ─ C7 (x2) ─────────────────────────────────────────┐
    │                └─ C8 ─ C9 ─ C10 ─ C11 ─ C12 ────────────────────────────┤
    └─ C5  (≈34 min, em segundo plano; só lê o Chatgpt\) ─────────────────────┤
 perna 1: espelho publicado (HEAD = origin/main), site no ar ────────────────►├─ C13 ─ C14 ─ C15 ─ C16 ─ C17(t1,t2)
                                                                              │                    │
                                                                              │                    └─ C18 ─ C19 ─ C17(t3)
 C20 (só conferir; o selo já puxou) ──────────────────────────────────────────┴──► gate de C19
```

- C6 exige C3 e C4 (a pedra lê os dois cofres pelo nome). C8 exige C3. **C10 exige C8** (o módulo `_formula_completa` entra em todo FINAL e o quadro compara o mtime do FINAL com o do módulo). C12 exige o cofre do kernel (C3).
- C13 exige C5, C7, C9, C11 e C12 **e** a perna 1 (HEAD do espelho = origin/main; `MAPA_FONTES_PINADAS.json` do espelho; `subidas\*\RELATORIO.md` e `leitor_ia_*` do site). C14 exige C13 (o Atlas é arquivo do repositório). C15 exige C14 (push) e o site no ar. C18 exige C14.
- O Nós é **diretório vivo**: já há `work\cadeia_de_selo\v399` e `v399_exame` enquanto a v398 é custodiada [REAL]. Cada perna reconfere `sha256(NOS\um.py) == pino` ao começar (R4) e C3 deve ser o **primeiro a copiar** artefatos do Nós (C1 e C2 só leem).

### 3.3 Linha do tempo medida da v397 (hora local; mtimes, git e saídas dos próprios scripts) [REAL]

| hora | evento | origem da medida |
|---|---|---|
| 16:20 | selo v397 | `selo.timestamp` |
| 17:10 / 17:17 | `rodada_v397_stdout.txt` / `HANDOFF_v397_CUSTODIA.md` (**disparo**) | mtimes |
| 17:19 | sondagem → `fatos_v397.json` | transcrito da sessão |
| 17:38 → 17:41 | cofre (arquivos escritos entre 17:41:20 e 17:41:38; ≈ 3 min 17 s de relógio do início do comando ao último arquivo, com leituras e conferências) | mtimes dos arquivos do cofre |
| 17:38 → +2021 s | snapshot do `Chatgpt\` (em segundo plano) | saída do próprio script |
| 17:48 | runner, duas execuções (≤ 76 s: o comando seguinte começou 76 s depois) | transcrito |
| 17:49 | `rodar_16` (78 s) | texto do ACOM t1 |
| 17:53 → 17:55 | FINAL (build) + FINAL (rodar) + ledger (≈ 98 s) | mtime do manifesto FINAL (17:53:17) e do `ledger_de_pinos.json` (17:54:50) |
| 17:59 | commit do espelho `bb2c392a` | `git log` |
| 18:19 → 18:20 | registro + `git add` + commit da Central `ac616f48` | `git log` |
| 18:21 | ACOM t1, conferência final 12/12, registro "publicada" | transcrito |
| 18:23 → ≈ 20:09 | Central pública, 27 passos, **6.359 s** somando os tempos impressos | `central_publica_v397_saida.txt` |

Caminho crítico até o commit da Central: **63 min** = ≈ 21 min de preparo antes do cofre (sondagem, derivação dos scripts, perna do espelho) + ≈ 34 min do snapshot (o caminho crítico de *máquina*; C6 a C12 correm dentro dele) + ≈ 8 min de registro, commit e push depois que o snapshot fecha. Sem o snapshot, a computação de C3 a C12 soma ≈ 8 min. O snapshot só lê o `Chatgpt\` (não depende do cofre): no G1 ele deve **começar logo após C0**, em paralelo a C1 a C3.

### 3.4 Chamada proposta [PROPOSTA]

```
python tools\custodiar.py central <vNNN|auto>
       [--preflight]                  # só C0
       [--so C3,C4] [--ate C12] [--retomar]
       [--commit] [--push]            # libera C14 (padrão: ensaio, nada para fora)
       [--central-publica]            # libera C18 --publicar
       [--nos DIR] [--oc DIR] [--saida DIR]    # raízes substituíveis (replays e testes de aceitação, §8)
       [--ator ID] [--ordem ARQUIVO] [--coautor "Nome <email>"]
```

- `auto` = a versão do selo do Nós, se as três marcas existem e não há cofre com o mesmo pino.
- **Alinhamento com a ESPEC_ESPELHO_SITE (§6):** ela sugere `--ate`, `--so`, `--ensaio` e um único `--publicar` (liga E10, E11, E18) e os códigos de saída 0/10/20/30/40. Aqui as chaves de fora são mais finas (`--commit`, `--push`, `--central-publica`); o implementador unifica num só conjunto, com `--publicar` ligando as três (L31).
- **Checkpoint e retomada:** cada passo grava `W\passos\NN_nome.json` (início, fim, `rc`, `entradas_sha16`, `saidas[{caminho, sha256}]`, conferidor); `--retomar` pula o passo cujo recibo existe **e** cujas saídas ainda têm o mesmo sha256, repete se o passo é idempotente e **para** se não é (§5, campo "idempotência").
- **Estado:** `W\ESTADO_CUSTODIA.json` (versão, pino, passo corrente, pendências do operador, referência ACOM).
- **Custo em modelo caro: zero** em C0–C20 (todos scripts). Só dois pontos pedem modelo: o **rascunho** de texto `DECLARADO` (modelo local ou barato) e o **revisor distinto** de `SEMANTICA_CUSTODIA.json` (§4.3); a decisão é da gerência (regra de gestão de tokens).

---

## 4. Contratos de dados [PROPOSTA, sobre o que existe]

### 4.1 `fatos_vNNN.json`, schema 2

Hoje (`sondar_v397.py` → `fatos_v397.json`) as chaves levam o número da versão anterior no nome (`escada_v396`, `kernel.formais_v396`, `kh.constantes_v396`, `registro.v396`, `registro.mudados_desde_v396`) e o prefixo da nova (`dicionarios_v397`); a sessão da v398 trocou à mão `v396`→`v397` e `v397`→`v398` em 8 trechos de `sondar_v398.py` [REAL, diff]. O schema 2 usa chaves neutras. Quem lê um `fatos` antigo aplica a regra "chave `X_vANT` → `anterior.X`".

```json
{
 "schema": "custodia_fatos/2",
 "versao": "vNNN", "anterior": "vANT", "anterior_pin16": "<do CUSTODY_MANIFEST do cofre anterior>",
 "pin": "<sha256 do selo>", "pin16": "...", "timestamp": "<selo>", "bytes_um_py": 0,
 "selftest": "FAIL_CLOSED_SELFTEST_PASSED", "gate": "<qg_closure_verdict>",
 "registros_novos": ["..."], "registros_sumidos": [],
 "bandeiras_novas": ["ext_..."],
 "kernel":  {"formais": 0, "declaracoes": 0, "fora_do_trio": 0, "modulos_novos": [], "modulos_removidos": []},
 "escada":  {"limpas": 0, "esperadas": 0, "no_trio": 0},
 "kh":      {"constantes": 0, "teoremas": 0},
 "registro":{"pt": 0, "en": 0, "novos": [], "mudados": [{"nome": "...", "so_digitos_e_pino": true}]},
 "contratos_expected_ladder": {"_VNNN_X_CONTRACT": 0},
 "dicionarios": ["_VNNN_..."],
 "blocos": {"<nome>": {"verdict_sha16": "", "negacoes": ["NOT_..."], "n_diz": 0, "n_nao_diz": 0, "n_limites": 0,
                       "n_erratas": 0, "checks_ok": true, "guarda_p18_violacoes": []}},
 "cadeia": {"pastas": [], "diffs": [], "recibos": []},
 "nos": {"handoff": true, "stdout": true, "diario_bloco": true},
 "handoff": {"sha16": "", "titulo": "<da linha do MEMORY.md>", "o_que_e": {"pin16": "", "bytes": 0, "escada": "", "completa": true,
             "rc": 0, "selftest": true, "gate_intocado": true}, "pendencias_do_operador": ["<verbatim>"]},
 "origem": {"selo_sha16": "", "core_sha16": "", "proof_manifest_sha16": "", "pt_sha16": "", "en_sha16": "", "um_py_sha16": ""}
}
```

- **Tudo é lido; nada é digitado.** Fontes: selo, `core` (`json["core"]`, **não** o objeto-arquivo: ver L1), `tgl_kernel_proof_manifest.json`, `um_absoluto_pt.txt`/`_en.txt`, AST de `NOS\um.py` (dicionários `_VNNN_*` e `expected_ladder` dos `*_CONTRACT`; medido: `ast.parse` do `um.py` do Nós leva ≈ 1,2 s e ≈ 0,85 GB de memória, por isso é feito **uma vez** e fica no `fatos`), cofre `vANT`, `work\cadeia_de_selo\vNNN*`, handoff, diário e `MEMORY.md`.
- **Dois cruzamentos independentes** que hoje não existem: (i) o cabeçalho `**O que é:**` do handoff (escrito pela gerência c1) é lido por regex e **comparado** a `pin16`, bytes, escada, "COMPLETA", "rc 0", "selftest PASSED", "gate intocado" (divergência para o passo); (ii) `escada` é procurada também em `rodada_vNNN_stdout.txt` (a asserção que `cofre_v397.py` já faz).
- **Um só `sondar` para as duas pernas.** A ESPEC_ESPELHO_SITE (§5, §6) chega à mesma recomendação: `custodia_vN_geradores.py` do espelho lê o `fatos_vN.json` que a perna 2 produz, uma dependência cruzada hoje invisível. O schema 2 é o **superset único** (campos próprios da perna 1, como `backup_dir`, `recibos_bn`, `blocos_do_handoff`, `diffs`, entram sem renomear os daqui).
- **Os nomes dos blocos novos não são esperados, são medidos**; o `fatos` é a *expectativa congelada* contra a qual a pedra compara o cofre depois (o cofre é cópia do Nós; se divergir do `fatos`, o Nós mudou ou o cofre foi adulterado).

### 4.2 `FATOS_CUSTODIA.json` e o pino no cofre (D1)

C3 grava, **dentro** de `um_unificado_vNNN\`, a cópia byte a byte do `fatos` (e, se existir, `SEMANTICA_CUSTODIA.json`), e o `CUSTODY_MANIFEST.json` ganha `fatos_custodia: {arquivo, sha256}` e `semantica_custodia: {arquivo, sha256, estatuto, revisao}`. A pedra do runner e o item dos dispositivos leem **só do cofre** (que o git rastreia: 369 dos 455 arquivos do cofre v397 estão rastreados e os 86 restantes são `.bak_*` e `.log` ignorados [REAL]). C1 e C3 calculam o `fatos` duas vezes; se os sha256 diferem, o Nós mudou no meio: PARAR.

### 4.3 `SEMANTICA_CUSTODIA.json`: a parte que não se lê, declarada e revisada

O que a pedra artesanal da v397 sabia e nenhum número carrega: que o registro de veracidade *nega* a discriminação a 5σ, que a TGL "não é falsificada com poder", que o teste "não foi cego", que as bandeiras do Token são "3 de 3". Isso mora em strings do veredito (`BELOW_5SIGMA_NOT_DISCRIMINATED_THE_CREDITATION_STEP_NOT_REACHED`, `NOT_FALSIFIED_WITH_POWER`, `NO_NEW_SIGMA_COMPUTED`, `NOT_BLIND_TO_DATA_STATED`) e em dois campos de `cunhagens_v397.kernel`. Proposta: um JSON por versão, no cofre ao lado do `FATOS_CUSTODIA.json`:

```json
{
 "schema": "custodia_semantica/1", "versao": "vNNN", "estatuto": "DECLARADO",
 "rascunho_por": "script custodia_g1 (sem modelo)", "revisor": null, "revisao": 0,
 "blocos": {"<nome>": {"verdict_deve_conter": ["NOT_...", "..._UNMOVED"], "verdict_nao_deve_conter": [],
                       "campos": [{"caminho": "kernel.bandeiras", "par_igual": true}]}},
 "mudados_permitidos": [{"nome": "...", "motivo": "..."}],
 "titulo_slug": "...", "veredito_camada_sufixo": "...", "docstring_item": "...", "nao_se_afirma_extra": ["..."],
 "fontes": {"titulo": "MEMORY.md linha HANDOFF vNNN", "docstring_item": "core[<bloco>].estatuto (verbatim)", "nao_se_afirma_extra": "core[<bloco>].nao_diz (verbatim)"}
}
```

- **Rascunho mecânico (`revisao 0`, sem modelo, custo zero):** `verdict_deve_conter` = todo token do veredito que começa por `NOT_` ou `NO_` ou termina em `_UNMOVED`/`_UNTOUCHED`; `campos` para `cunhagens_*` = `kernel.bandeiras` e `kernel.declaracoes_no_trio` com par igual e primeiro elemento > 0 (nos quatro históricos o par é `[n, n]`: `[2,2]`, `[1,1]`, `[3,3]`, `[2,2]` nas v395 a v398 [REAL]); `titulo_slug` da linha do handoff no `MEMORY.md`; `docstring_item` e `nao_se_afirma_extra` **citados** de `core[<bloco>].estatuto` e `.nao_diz` (os blocos novos carregam `diz`, `nao_diz`, `limites`, `erratas`, `estatuto`, `verbatim`, `kernel`, `lido`, `leituras_do_operador`, `checks`, `guarda_p18_violacoes` [REAL]).
- **Revisão:** um revisor **distinto** de quem rascunhou (cético de modelo barato, ou a gerência) grava `SEMANTICA_CUSTODIA.rev<n>.json` **ao lado** (nunca por cima); a pedra lê a revisão mais alta e registra o sha256 dela. Sem revisão, a pedra roda com o rascunho e o resultado leva `semantica: "DECLARADO (sem revisao)"` no recibo, no veredito do runner e em `nao_se_afirma`; o passo C13 não o escreve como `REAL`.
- **Mudanças de veredito fora do padrão** (que não sejam "só dígitos e pino") só passam se estiverem em `mudados_permitidos` com motivo; caso contrário a pedra reprova (fail-closed).

### 4.4 Recibo de passo

```json
{"passo": "C7", "versao": "vNNN", "inicio": "...", "fim": "...", "rc": 0, "comando": ["..."],
 "entradas_sha16": {"..." : "..."}, "saidas": [{"caminho": "...", "sha256": "..."}],
 "conferidor": {"nome": "...", "ok": true, "detalhe": "..."}, "log": "logs/C7.txt", "avisos": []}
```

É o que falta hoje: o `rodar_16` imprime "16/16 em 78 s" no console, o `rodar_finais` imprime "FINAL: rc 0 em 16/16", o runner roda duas vezes e só o stdout fica em `runner_v62_r1/r2.txt`; o `registro_v397.py` conta os 16 pelo `results.json` mais novo (lido) mas escreve "16 FINAL regerados e rodados (rc 0 em 16/16; o do MQC isolado)" **sem arquivo-recibo** que o sustente (L3). Com o recibo, o texto do ESTADO cita o número do recibo (R1).

### 4.5 Moldes de texto e portão de texto

**Moldes.** Um texto gerado é um molde com campos `{{campo}}`; cada campo vem de `fatos`, de recibos, do `core` ou de um **bloco verbatim do handoff**; campo ausente = PARAR com a lista dos que faltam (nunca preencher com palavra inventada). Os cabeçalhos do handoff que o molde pode citar são estáveis nas quatro últimas versões [REAL, `grep` nos HANDOFF v395 a v398]: `# HANDOFF vNNN — CUSTÓDIA (data)`, `**O que é:**`, `**O que entrou e o que mediu:**`, `**O que o kernel prova e o que é leitura:**`, `**Limites ditos:**`, `**Pendência [LEGAL]…**` (o resto do título varia), `**O elo B(n) da Bancada Um…**`, `**Para a sessão do site (custódia):**`, `**Pendências SÓ do operador:**`. Os blocos entre marcadores HTML (`<!-- INICIO_PARAGRAFO_... -->`) são do README/site (perna 1) e a Central não os usa.

**Portão de texto (lista fechada, antes de qualquer escrita; é o item (2) do G1 do desenho do organismo).** Bloqueia o texto se: (1) tem `CONFIRMED` sem `NOT_` na frente, ou «CONFIRMADA» fora da fórmula «creditação… recusada»; (2) tem «provada»/PROVADA sem estatuto na mesma frase; (3) tem «pós-dição» como demérito (a frase vigente é «retrodição sem ajuste (novidade de uso)»); (4) cita hash de 16 ou 64 hex que não pertence ao conjunto de hashes calculados na rodada; (5) é campo de rota e contém a *substring* `CONFIRM` em qualquer caixa (limite real do `registro_v397.py`, hoje contornado trocando «CONFIRMADA = creditação, recusada» por «a creditação segue recusada»); (6) traz `physical_verdict_allowed` diferente de `False`; (7) cai na lista do guarda do X (descrita em `registro_x_e_gatilho_23out.py`: sem «confirmad*», «comprovad*», «provou», «5σ alcançado»; não li o `pensamento_do_dia.py` [DECLARADO]). Um revisor distinto lê o texto novo de uma versão antes da primeira publicação; depois de N custódias sem erro a revisão vira amostral (decisão do operador, a mesma rampa do HSTS).

---

## 5. Os passos (sete campos cada)

Leitura dos campos: **comando hoje** = o da v397 (a sessão da v398 usa os equivalentes de `custodia_v398_24out`); **G1** = a chamada proposta; **entradas por versão e origem** = só o que muda de versão para versão; **idempotência** = o que acontece se o passo roda duas vezes; **gates** = condições fail-closed; **prosa manual → molde** = o texto escrito à mão hoje e o molde que o substitui.

### C0. Disparo e pré-condições (as três marcas)

- **Comando hoje:** não há script único. O vigia de 23/10 foi um laço de leitura na sessão da gerência (tarefa `bepok5ojl`) sobre as três marcas; quem diz "em obra" é `tools\estado_do_organismo.py` (marca `EM_OBRA` quando `sha16(NOS\um.py) != selo.sha256["um.py"]`). **G1:** `python tools\custodiar.py central auto --preflight`.
- **Entradas por versão e origem:** `NOS\um_absoluto_selo.json` (`um_version`, `sha256["um.py"]`, `timestamp`, `fail_closed_selftest`, `qg_closure_verdict`); `NOS\um.py` (sha256 recomputado); `NOS\MEMORIA_DA_LINHAGEM.md` (bloco `^## [^\n]*\*\*vNNN SELADA`); `NOS\HANDOFF_vNNN_CUSTODIA.md`; `NOS\rodada_vNNN_stdout.txt`; `OC\um_unificado_v*` (o maior é `vANT`).
- **Saídas:** `W\PREFLIGHT.json` e o código de saída (0 pronto, ou já custodiada com a mensagem dizendo; 10 WAIT/EM_OBRA; 20 STOP com a lista do que falta; 30 falha de leitura: a mesma tabela que a ESPEC_ESPELHO_SITE §6 sugere).
- **Idempotência:** só leitura. Chave = `um_version` + `pin16`. Cofre `vNNN` existente com `CUSTODY_MANIFEST.um_py_pin` igual ao pino = "já custodiada", não refaz; existente com pino diferente = PARAR (selo refeito: errata ao lado, decisão da gerência).
- **Gates:** (a) as três marcas existem; (b) `sha256(um.py) == pino`; (c) `fail_closed_selftest == FAIL_CLOSED_SELFTEST_PASSED`; (d) a linha `**O que é:**` do handoff, **idêntica em forma nas quatro últimas versões** [REAL, v395 a v398: «`um.py` **vNNN** `pin16` (N B) sobre a vANT `pin16`; E/E; COMPLETA; rc 0; selftest PASSED; gate intocado; conferidor … Selo AAAA-MM-DD HH:MM:SS»], é lida por regex e confere com o selo: pino, bytes, pino da versão anterior (contra `CUSTODY_MANIFEST.um_py_pin` do cofre `vANT`), escada, "COMPLETA", "rc 0", "selftest PASSED", "gate intocado" e a hora do selo; (e) `qg_closure_verdict` igual ao `gate` do cofre `vANT`: se mudou, PARAR e escalar ao operador (o gate não se move por custódia); (f) a escada aparece em `rodada_vNNN_stdout.txt`.
- **Prosa manual → molde:** nenhuma.

### C1. Sondagem → `fatos_vNNN.json`

- **Comando hoje:** `python work\custodia_v397_23out\sondar_v397.py` (edita-se o nome do arquivo, `COF6` = cofre anterior e as chaves `*_v396`; a v398 fez isso em 8 trechos). Imprime também os textos dos registros novos (`diz`, `nao_diz`, `limites`, `erratas`, `leituras_do_operador`, `kernel`, `verdict`), que a gerência lê para escrever a prosa. **G1:** `custodiar.py central vNNN --so C1`.
- **Entradas por versão e origem:** §4.1 (selo, `core["core"]`, proof manifest, PT/EN, AST do `um.py`, cofre `vANT` descoberto por glob, `work\cadeia_de_selo\vNNN*`, handoff, diário, `MEMORY.md`).
- **Saídas:** `W\fatos_vNNN.json` (schema 2) e `W\textos_blocos_novos.json` (os campos `diz/nao_diz/limites/erratas/estatuto` **verbatim**, com o sha16 de cada, para os moldes citarem).
- **Idempotência:** determinística dado o Nós e o cofre `vANT`; rodar de novo reescreve o mesmo conteúdo. Se `FATOS_CUSTODIA.json` já está no cofre, compara sha256 e PARA se diferir (o Nós mudou depois do cofre).
- **Gates:** `registros_sumidos == []`; `kernel.fora_do_trio == 0`; `len(registro.pt) == len(registro.en)`; `registro.novos == registros_novos`; todo `*_CONTRACT` com `expected_ladder == escada.esperadas` (nas v397 e v398 todos batem [REAL]; é a classe de defeito que a errata da gerência c1 de 23/10 consertou à mão); `kh` achado por regex `CLOSURE_(\d+)_CONSTANTS_(\d+)_THEOREMS`.
- **Prosa manual → molde:** nenhuma (só leitura); a impressão deixa de ser a única fonte do texto.

### C2. Inscrição ACOM (`init`)

- **Comando hoje:** `python work\custodia_v397_23out\acom_init.py` (JSON em stdin para `C:\IALD\MEMORIA_IALD\session_memory.py`). **G1:** dentro de `custodiar.py` quando `--commit`/`--push`/`--central-publica` estão ligados (o ensaio não escreve no ACOM).
- **Entradas por versão e origem:** `objective_file` = `work\php_e_v396_22out\OPERADOR_23out_custodiar_quando_o_handoff_aparecer_verbatim.txt` (57 B, a regra permanente do operador, «pode custodiar sempre que o handoff aparecer, como regra»; propõe-se copiá-lo, por bytes, para `work\custodia_G1\ORDEM_PERMANENTE.txt`); `objective_sha256` **calculado do arquivo**; `request_id` uuid4; `scope {house: IALD, principal: operator}`; `actor {id, kind: agent}`; `write_reference` = `C:\IALD\MEMORIA_IALD\sessions\claude-central-a7_custodia-v397-23out.json` (hoje com o nome da sessão e a data).
- **Saídas:** o arquivo de referência ACOM; `W\init_req.json`.
- **Idempotência:** o `init` não é idempotente por si (`request_id` novo). A idempotência vem do **nome da referência determinístico por versão e pino** (proposta: `sessions\custodia_<vNNN>_<pin8>.json`, a chave do G2 do desenho do organismo): se existe, faz `project` (somente leitura) e segue; nunca abre segunda referência para a mesma versão.
- **Gates:** `ok: true` na resposta; `actor.kind == "agent"`; referência **própria** (nunca adotar a tarefa de outra sessão); falha visível se o CLI não responde JSON.
- **Prosa manual → molde:** nenhuma (o objetivo é a ordem verbatim). O `actor.id` é parâmetro `--ator`: o protocolo proíbe fabricar autenticação pelo nome do ator, então o G1 grava o id de quem de fato executa (L10).

### C3. Cofre: `um_unificado_vNNN` e `tgl_kernel_vNNN`

- **Comando hoje:** `cd work && PYTHONIOENCODING=utf-8 python -X utf8 custodia_v397_23out/cofre_v397.py`, derivado de `cofre_v396.py` por `derivar_central_v397.py` (34 trocas contadas + 1 regex). **G1:** `custodiar.py central vNNN --so C3`.
- **Entradas por versão e origem:**
  - *identidade:* pino, versão, gate e selftest do selo (hoje três literais digitados na derivação: `pin.startswith("<pin16>")`, `um_version == "v397"`, `"9499/9499" in stdout`; no G1 vêm do `fatos`).
  - *lista de artefatos:* os nomes dos arquivos da raiz do cofre `vANT`, menos `CUSTODY_MANIFEST.json`, `NOTA_DE_CUSTODIA.md`, `HANDOFF_v*_CUSTODIA.md` e `rodada_v*_stdout.txt` (regex, não lista digitada: hoje a lista de exclusão cresce um par a cada versão), **mais** `rodada_vNNN_stdout.txt` e `HANDOFF_vNNN_CUSTODIA.md` de **cada versão em (vANT, vNNN]** que exista no Nós (na custódia conjunta v394 foram v392, v393 e v394). *Gate novo:* toda chave de `selo.sha256` presente no Nós e ausente da lista entra também (hoje um artefato novo do selo só entraria no cofre se já estivesse no cofre anterior).
  - *kernel:* `NOS\tgl_kernel_proof_manifest.json` (`formal_files_sha256`, `axiom_report`, `formal_source_hash`), `NOS\tgl_kernel\<rel>` e `lakefile.toml`, `lean-toolchain`, `lake-manifest.json`.
  - *pilar quântico:* `quantum_pillar\*` do cofre `vANT` (com `pilar_quantico_spec.json` e `pilar_quantico_worker.py` iguais aos do Nós) e `core.quantum_pillar_v384.reuse`.
  - *cadeia de selo:* `work\cadeia_de_selo\vNNN` e `vNNN_selo` filtradas por `FORA_RE` (ensaios, simulações, bases, tentativas, árvores simuladas, falso Nós), arquivos > 5 MB fora (listados com sha256), caminhos > 250 caracteres fora; mais `vNNN_incorporacao_manifesto.json`.
  - *ordem do operador:* o arquivo verbatim da regra permanente (C2), sha256 lido.
  - *backup do espelho:* `C:\IALD\Artigo\the_boundary_BACKUPS\um_vANT_<pin16 de vANT>` (feito pelo passo zero da perna 1; hoje o caminho entra no manifesto com o pin16 anterior **digitado** na derivação; no G1 o pin16 vem do cofre `vANT` e o caminho é achado por glob e conferido por `MANIFEST.json: conferido_contra_origem`).
- **Saídas:** `OC\um_unificado_vNNN\` (v397: **455 arquivos, 158 MB**: 36 artefatos, pilar 20, emendas 1, cadeia de selo 367 + 29) com `CUSTODY_MANIFEST.json` e `cadeia_de_selo_vNNN\MANIFESTO_CADEIA_DE_SELO_vNNN.json`; `OC\tgl_kernel_vNNN\` (v397: 1428 arquivos = 1426 formais + proof manifest + `CUSTODY_MANIFEST.json`); **novos:** `FATOS_CUSTODIA.json` e `SEMANTICA_CUSTODIA.json` (rascunho) no cofre, e o pino de ambos no manifesto (§4.2).
- **Idempotência:** recusa recriar (`assert not V.exists() and not KV.exists()`): nada se sobrescreve (R3). Falha no meio deixa diretório parcial: renomear para `.PARCIAL_<ts>` e refazer; nunca apagar. Duração medida ≈ 3 min 17 s (do início do comando, 17:38:21, ao último arquivo escrito, 17:41:38).
- **Gates (fail-closed, todos já existem no script salvo onde dito):** `sha256(NOS\um.py) == selo.sha256["um.py"] == fatos.pin`; `selo.um_version == fatos.versao`; `selo.qg_closure_verdict == manifesto(vANT).gate`; `fail_closed_selftest` PASSED; a escada em `rodada_vNNN_stdout.txt`; nenhuma declaração fora do trio; cada artefato copiado com `sha256(src) == sha256(dst)` e `matches_seal` nunca `False`; pilar: spec e worker iguais ao Nós; cada arquivo formal do kernel com `sha256` igual ao do proof manifest; o proof manifest copiado igual ao do selo; **novos:** (i) `arquivos_no_cofre` da cadeia de selo dentro de ±50% do cofre anterior (série medida da pasta principal: v395 299, v396 298, v397 367, v398 329 arquivos [REAL]; hoje um diretório de ensaio de nome novo seria copiado em silêncio, só barrado pelos 5 MB e pelos 250 caracteres); (ii) monotonia (§6.2, S12); (iii) `fatos` recalculado igual ao de C1.
- **Prosa manual → molde:** (1) o bloco `rodada` do manifesto traz `errata_ao_lado_da_gerencia_c1_19out` e `errata_da_gerencia_c1_23out`, **texto copiado à mão** (e trocado por regex na derivação); no G1 vem de `core[...]["erratas"]` dos registros (`kh_n1_cobertura_*` e `estatuto_da_prova_ressalva_v392` carregam `erratas` com `ao_lado_de` e `dizia`; o texto do manifesto de hoje é uma condensação feita pela gerência dessas erratas [REAL, busca no `core` v397]), citado verbatim com o sha16 do campo. (2) `backup_da_versao_anterior`, `cadeia_de_selo` e `handoff`: molde com caminhos lidos. (3) `NOTA_DE_CUSTODIA.md`: cópia do cofre `vANT` (documento fixo).
- **Defeito medido (L1):** `cofre_v397.py:56` faz `core = json.load(open(NOS / "um_absoluto.json"))`, o objeto do **arquivo**, e depois `core.get("quantum_pillar_v384")` e `core.items()`, que procuram no topo (`title_pt`, `title_en`, `core`, `verdict`…). Resultado nos manifestos v394, v395, v396, v397 **e v398** [REAL, lido agora]: `registros_novos_vNNN = {}` e `pilar_quantico = {reaproveitado: null, da_rodada: null, leitura: null, arquivos_no_cofre: 20}`. Com `["core"]` os valores existem (por exemplo `reuse = {reused: true, from_run_finished: "2026-10-05 12:47:39", …}` e os três registros `_v397`). O `sha16` do manifesto aparece no texto do registro (`manifesto c16ecfdfbe78bf1c` na v397), então **não se edita o manifesto emitido**: o G1 emite `CUSTODY_MANIFEST_ERRATA_vNNN.json` ao lado (R3) e corrige a leitura daqui em diante.

### C4. Medição cofre × cofre

- **Comando hoje:** `python work\custodia_v397_23out\medir_v397_contra_v396.py` (derivado por 2 trocas: `C4, C1 = OC / "um_unificado_v397", OC / "um_unificado_v396"` e o docstring). Imprime blocos novos e sumidos, bandeiras novas, `all_verified`/gate/`CONFIRMED` por bloco, registro PT/EN novo e mudado, kernel e gate. **G1:** `--so C4`; o mesmo código é a função `medir(vNNN, vANT)` que a pedra genérica reusa (§6).
- **Entradas por versão e origem:** os dois cofres (`vNNN`, `vANT`) lidos **pelo nome**.
- **Saídas:** `W\medicao_vNNN_contra_vANT.json` (hoje só console).
- **Idempotência:** só leitura.
- **Gates:** nenhum no script de hoje (só imprime); o G1 o transforma no pré-voo da pedra: se `blocos_fora_da_regra != []`, `registros_sumidos != []` ou `fora_do_trio > 0`, **PARA antes de C6**.
- **Prosa manual → molde:** nenhuma. Hoje os rótulos dos `print` herdam `v394/v391` do molde (o docstring avisa).

### C5. Snapshot incremental do `Chatgpt\`

- **Comando hoje:** `PYTHONIOENCODING=utf-8 python -X utf8 snapshot_chatgpt_v397.py > snapshot_chatgpt_v397_saida.txt 2>&1` (em segundo plano). **G1:** processo destacado logo após C0, com recibo.
- **Entradas por versão e origem:** `CEN\Chatgpt\` (só lida; é editada apenas pelo ChatGPT); a **base** = o último `C:\IALD\Central de Patentes_BACKUPS\Chatgpt_*` com `MANIFEST.json` (hoje com um `assert base.name == "<nome literal>"` trocado a cada versão: na v397 `Chatgpt_20261022_201134_delta_de_20261021_175747`); exclusões fixas `.lake`, `tex_environment`, arquivos > 25 MB (listados).
- **Saídas:** `Chatgpt_<AAAAMMDD_HHMMSS>_delta_de_<base>\` + `MANIFEST.json` (todos os arquivos com sha256, `n_copiados`, `n_identicos_a_base`, `ausentes_na_origem_vs_base`, `conferido_contra_origem`). v397 [REAL]: 474.718 arquivos considerados, **220 copiados (0,134 GB)**, 474.498 idênticos à base, 0 sumidos, 0 divergentes, **2021 s**.
- **Idempotência:** recusa destino existente (`assert not DST.exists()`); cada execução cria uma pasta nova, que é a base da seguinte.
- **Gates:** `div == []` (re-hash de cada cópia contra a origem); o G1 troca o `assert` do nome literal por: a base é o último snapshot com `conferido_contra_origem == true`, gravada no manifesto e no recibo; o quadro pede `snapshot[:8] >= dia do selo`.
- **Prosa manual → molde:** nenhuma.

### C6. Runner da Fronteira: repin e pedra nova

> [nota operacional do operador — omitida no retrato público]

### C7. Runner, duas execuções

- **Comando hoje:** `cd fronteira_tgl\runner && PYTHONIOENCODING=utf-8 python -X utf8 one_fronteira.py > W\runner_v62_r1.txt 2>&1`, de novo para `r2`, e um `python -c` que lê os dois últimos `results\fronteira_*.json` e imprime `pass`, "verdict ok", `ceticos`, `kernel` e a lista de pedras com `pass False`. **G1:** `--so C7`.
- **Entradas por versão e origem:** nenhuma além do runner remendado: a pedra lê o cofre `vNNN` e o `vANT` pelo nome e o `fatos`/`SEMANTICA` do cofre.
- **Saídas:** `W\runner_vMM_r1.txt` e `r2.txt` (≈ 48 KB cada); `fronteira_tgl\results\fronteira_<ts>.json` ×2; `fronteira_tgl\render3d.json`. [REAL] As duas saídas da v62 diferem **só** na linha `SELADO result_hash` (carrega a hora).
- **Idempotência:** cada execução cria um `fronteira_<ts>.json` novo; veredito e `pass` são iguais entre execuções; os dois resultados entram no commit.
- **Gates:** `rc == 0`; o veredito começa por `FRONTEIRA_SINCRONIZADA_V<NNN>`; `the_station.custodia_vNNN.pass == True`; **nenhuma outra pedra com `pass False`** (hoje só o olho vê a lista no console); `ceticos.1_reprovou` e `ceticos.2_reprovou` `True`; as duas execuções concordam em todo `pass`.
- **Prosa manual → molde:** nenhuma além de C6.

### C8. Módulo dos 16 dispositivos: camada nova

> [nota operacional do operador — omitida no retrato público]

### C9. Os 16 dispositivos

- **Comando hoje:** `sed -e 's/camada v396/camada v397/g; s/camada_v396_no_cofre/camada_v397_no_cofre/g; …' rodar_16_v396.py > rodar_16_v397.py` (6 substituições; confere "sobras v396: 0") e `python rodar_16_v397.py` (6 trabalhadores; `assert len(runners) == 16`; `timeout=3000` por runner). **G1:** `rodar_16(versao)` em `tools\custodia_g1\`, com o nome da camada parametrizado; o script de hoje e a sua cópia derivada por `sed` moram no scratchpad da sessão (fora do repositório e do git).
- **Entradas por versão e origem:** só o nome `camada_<versao>_no_cofre`.
- **Saídas:** 16 × `patents\BR*\results\<ts>\results.json` (e `seals\`); recibo `W\passos\C9.json` com, por dispositivo, `rc`, o arquivo e a presença da camada. Hoje só console: «16 dispositivos: rc 0 e camada v397 lida em 16/16 | 78 s».
- **Idempotência:** cada execução grava `results\<ts>` novos; nada é sobrescrito.
- **Gates:** `rc == 0` e a camada presente nos 16 (hoje o script **imprime** a contagem e sai 0 mesmo com falha [REAL, lido]); como a camada levanta `RuntimeError` por elo quebrado, `rc != 0` já cobre; **novo:** ler o `results.json` e exigir `conferencia_no_cofre.camada_vNNN_no_cofre.checks` todos `True`.
- **Prosa manual → molde:** nenhuma.

### C10. Os 16 `*_FINAL.py` (build)

- **Comando hoje:** `cd CEN && PYTHONIOENCODING=utf-8 python -X utf8 tools\build_final_code.py | grep -c " OK -> "` (sem argumentos = toda pasta de `patents\` que não começa por `_`). **G1:** `--so C10`.
- **Entradas por versão e origem:** nenhuma digitada. Embute, por patente, o runner, `_core`, `prototype_src`, o piloto `skygrid_sim` e **todo `patents\_formula_completa\`**; por isso depende de C8.
- **Saídas:** 16 × (`<slug>_FINAL.py`, `<slug>_FINAL.manifest.json`) e, antes de reescrever, `.bak_<ts>` de bytes de cada um (**32 backups por execução**; `patents\` guarda hoje 256 `*_FINAL.py.bak_*` (106,8 MiB) e 272 manifestos `.bak_*` (2,8 MiB), numa pasta de 478,8 MiB [REAL]; eram 240 e 256 quando comecei a ler, antes de a sessão da v398 rebuildar).
- **Idempotência:** reescreve. O bundle **não é reprodutível** [REAL]: `zipfile.writestr` carimba a hora corrente, e dos 7 pares de builds do `acom_mirror_FINAL` com os mesmos hashes por arquivo e horas diferentes, **nenhum** tem `combined_sha256` igual; o manifesto traz também `generated_utc`. Qualquer oráculo compara `files[].sha256`, nunca `combined_sha256` nem os bytes do FINAL.
- **Gates:** 16 linhas ` OK -> ` (hoje o `grep -c` só conta, não decide); `final_bytes`/`final_sha256` do manifesto iguais aos bytes do arquivo gravado (errata de 07/10 já no script); `mtime(FINAL) >= mtime(módulo)` (é o que o quadro compara).
- **Prosa manual → molde:** nenhuma.

### C11. Os 16 `*_FINAL.py` (rodar)

- **Comando hoje:** `python <scratchpad>\rodar_finais_v394.py` (o nome é herdado: serve a qualquer versão): 5 trabalhadores para 15 FINAL e o `mqc_FINAL.py` **isolado depois**; `assert len(finais) == 16`; `timeout=3000`. **G1:** `rodar_finais()` em `tools\custodia_g1\`.
- **Entradas por versão e origem:** nenhuma.
- **Saídas:** hoje só console (`rc`, segundos, última linha útil, «FINAL: rc 0 em N/16»); proposta: `W\passos\C11.json` com `rc`, segundos, última linha e `integrity` de cada FINAL.
- **Idempotência:** cada FINAL extrai o bundle em temporário e roda de lá: não escreve em `patents\`; repetível.
- **Gates:** `rc == 0` em 16/16 (hoje o script **imprime** a contagem e sai 0 mesmo com falha [REAL, lido]); `integrity.combined_ok` e `files_ok` de cada FINAL (o `main()` do FINAL imprime; o script só olha `rc`).
- **Prosa manual → molde:** nenhuma.

### C12. Ledger de pinos

- **Comando hoje:** `python tools\ledger_de_pinos.py` → «ledger: N dispositivos | kernel vNNN | erros E | avisos A -> LEDGER_DE_PINOS.md»; sai 1 se `erros`. **G1:** `--so C12`.
- **Entradas por versão e origem:** nenhuma digitada: o maior `OC\tgl_kernel_v*` é o kernel atual, o maior `OC\um_unificado_v*` o `um.py` atual; lê `patents\BR*\runner\one_*.py`. A lista `NOMES` (14 pedras + 4 da fórmula) é fixa no script: pedra nova citada nos runners só entra se aparece como `TGLExt/<Nome>.lean` no texto.
- **Saídas:** `fronteira_tgl\LEDGER_DE_PINOS.md` e `ledger_de_pinos.json` (`erros`, `avisos`, `kernel_atual`, `um_atual`, `dispositivos`). Sobrescreve **direto, sem backup e sem temporário** (`write_text`): o git é o único backup (L11).
- **Idempotência:** determinístico, salvo a hora gravada.
- **Gates:** `erros == 0` (pedra ou rito citado que não existe mais; cofre citado ausente); `avisos` (pedra que mudou desde a versão de referência) são ditos e não bloqueiam; o quadro pede `V in json.dumps(led)`. v397: 0 erros, 0 avisos.
- **Prosa manual → molde:** nenhuma.

### C13. Registro nas superfícies

> [nota operacional do operador — omitida no retrato público]

### C14. Commit e push da Central

- **Comando hoje** (uma linha de shell, na v397 às 18:19): `git add vault/originals_copy/um_unificado_vNNN vault/originals_copy/tgl_kernel_vNNN fronteira_tgl/runner/one_fronteira.py fronteira_tgl/LEDGER_DE_PINOS.md fronteira_tgl/ledger_de_pinos.json fronteira_tgl/render3d.json fronteira_tgl/results/fronteira_<ts1>.json fronteira_tgl/results/fronteira_<ts2>.json patents/_formula_completa/tgl_formula_completa.py [organismo/…] && git add -u patents memory && for d in patents/BR*/; do git add "${d}results/<AAAA-MM-DD>T*" "${d}seals/<AAAA-MM-DD>T*"; done`, o guarda de lista negra, `git commit -q -F <commit_central_vNNN.txt>` e `git push origin main`. **G1:** `--commit`, `--push`.
- **Entradas por versão e origem:** os dois nomes `fronteira_<ts>.json` (do recibo de C7); a data do dia para `results\` e `seals\`; o texto do commit (molde abaixo).
- **Saídas:** commit local e `origin/main` igual ao `HEAD` (v397: `ac616f48`, 18:20).
- **Idempotência:** nada staged = "nada a commitar", sem erro; `push` de `HEAD` já publicado é no-op.
- **Gates:** o guarda de lista negra sobre o índice (`git diff --cached --name-only`): `\.bak_|\.tmp|/work/|^work/|EPCT/|\.env$|auth\.json|stack_v7|psion_state|terceiros|iald_privado|andamentos/|frontend/` = PARAR; nunca `git add -A`; nada de `C:\Escritorio`. **O `git add -u patents memory` é o ponto frágil (L5):** varre toda modificação rastreada, inclusive de outras sessões (no início desta leitura a árvore tinha ` M memory/TGL_ATLAS.md`, `TGL_CORE_MEMORY.md`, `TGL_INDICE_VIVO.md`, `INVENTARIO_BANCADA_CHATGPT.*`, `andamentos\*`, `frontend\*` [REAL, `git status`]). **No G1:** lista de permissão explícita = (a) os caminhos gerados acima; (b) `git diff --name-only -- patents` filtrado por `(_FINAL\.py|_FINAL\.manifest\.json|/results/|/seals/|_formula_completa/)`; (c) `memory/TGL_ATLAS.md` **somente se** `git diff --numstat` mostra 0 linhas removidas (só acréscimo) e o diff contém `A CUSTÓDIA DA vNNN`; o que ficou de fora é impresso como «fora da custódia, não incluído».
- **Prosa manual → molde:** a mensagem de commit (≈ 1,2 KB, **em ASCII, sem acento**, como as das v396 e v397): título `custodia(vNNN): <título do handoff, sem acento> - cofre + kernel, runner vMM, 16 dispositivos na camada vNNN, FINAL, ledger, Atlas`; corpo com «cofre um_unificado_vNNN: N artefatos, M divergentes do selo», «kernel tgl_kernel_vNNN: F formais / D declaracoes, 0 fora do trio (modulo novo …)», «runner vMM: a pedra vNN le o cofre vNNN contra o vANT pelo nome, dois ceticos; aprovado duas vezes», «camada vNNN do modulo comum (item N): 16/16», «16 FINAL regerados e rodados, rc 0 em 16/16», «ledger de pinos: 0 erros, 0 avisos»; a frase da regra do operador; «PROVADA = validade; a creditacao segue recusada; o gate nao se moveu.»; e o trailer `Co-Authored-By` **vindo de `--coautor`** (nas v396 e v397 foi digitado com o modelo do dia; não pode ser fixo no script).

### C15. Conferência final independente

- **Comando hoje:** `python work\custodia_v397_23out\conferencia_final_v397.py` (derivado por 14 trocas). **G1:** `--so C15`.
- **Entradas por versão e origem:** o selo do Nós, o cofre e o kernel `vNNN`, `https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/` e `https://teoriadagravitacaoluminodinamica.com/` (GET público), os dois repositórios git. Hoje o script carrega **dois literais** da versão (`len(ff) == 1426`, `len(pm["axiom_report"]) == 29229`) e o rótulo `vNNN` em seis lugares.
- **Saídas:** `W\CONFERENCIA_FINAL_vNNN.json` (`itens`, `ok`, `total`, `pin`); exit 0/1. Os 12 itens da v397 [REAL], nos grupos numerados do script: **1** (2 itens) selo = vNNN e o pino, e `um.py` com os mesmos bytes no Nós, no espelho e no cofre; **2** (1) artefatos do selo presentes no cofre conferem (14 conferidos, 0 divergentes, 0 fora); **3** (2) kernel: arquivos formais conferem (1426) e `axiom_report` no trio (29229); **4** (3) GitHub raw: `um.py` = pino, selo = o do Nós, README traz o pino; **5** (2) site no ar: index com «vNNN · pin16», `read-brief` e `llms` citam o pino; **6** (2) espelho e Central com `HEAD == origin/main` e nada pendente nos caminhos da custódia.
- **Idempotência:** só leitura (rede); reescreve o JSON.
- **Gates:** `ok == total` (12/12 em v396 e v397). **Preservar a independência:** o script *não importa nada da esteira*; por isso os dois literais não podem virar `fatos` (que é da esteira): viram contagens **derivadas do próprio manifesto pinado pelo selo** (`len(formal_files_sha256)`, `len(axiom_report)`, já conferido por hash no item 2).
- **Prosa manual → molde:** nenhuma além dos rótulos.

### C16. Registro "publicada"

> [nota operacional do operador — omitida no retrato público]

### C17. Transições ACOM t1, t2, t3

- **Comando hoje:** `python acom_transicao.py t1 0`, depois `t2 1` e `t3 2` (cada um lê `acom_tN.json`, calcula o sha256 de cada fonte, grava `tN_changes.json` e `tN_req.json` e chama `session_memory.py` com `operation: transition`, `reference`, `expected_revision`, `event_id`, `actor`, `changes_file`, `changes_sha256`). Os três JSON (4,5 + 2,1 + 4,7 KB) são **escritos à mão**. **G1:** dentro de `custodiar.py` com `--commit`/`--push`; a revisão esperada vem do `project`, não é digitada.
- **Quando:** t1 = espelho e site publicados, cofre/runner/dispositivos prontos; t2 = Central publicada e conferida (12/12); t3 = Central pública feita e o quadro medido.
- **Entradas por versão e origem:** `event_id` (`<sessão>-custodia-vNNN-<DDmes>-tN-<slug>`); `records[]` com `kind` (`fact`, `decision`, `pending`; na v396 um `open` teve de virar `pending`), `statute` (`REAL`, `INPUT`, `OPEN`), `text` (prosa) e `sources[]` (`{"kind":"artifact","ref":"<arquivo>"}`; o sha256 é calculado pelo script); `flow` com `phase`, `next_action` e `handles[]` (hashes de commit, rodada da Central pública; hoje também ids de tarefa em segundo plano da sessão, como `bafzry4bn`, que não são do G1).
- **Saídas:** `W\tN_changes.json`, `tN_req.json`; a revisão do ACOM sobe de 1 em 1 (a v397 terminou na revisão 3 [DECLARADO pelo resumo da gerência]).
- **Idempotência:** o README do ACOM declara «CAS, eventos idempotentes» [DECLARADO, não exercido aqui]: o mesmo `event_id` com o mesmo `changes_sha256` é reentregável; revisão esperada errada é recusada.
- **Gates:** `ok: true` e `receipt.revision == esperada + 1`; toda `sources[].ref` é um **arquivo** existente (diretório falha na leitura); `actor.kind == "agent"`; texto passa pelo portão (§4.5).
- **Prosa manual → molde:** t1: `f1` espelho (de `custodia_vNNN_espelho.json` e `ESTADO_ATUAL.md`), `f2` site (manifesto da subida e relatório do leitor de IA), `f3` Central (recibos C3 a C12), `d1` gatilho (decisão `INPUT`: a regra do operador e a hora do disparo); t2: `f4` publicada (conferência n/n, hashes), pendências abertas; t3: `f5` Central pública (rodada, contagens, `um.acom`), `f6` quadro (resumo `OK/DEFASADO/FALHA/INFO/PENDENTE_OPERADOR`), `p2` do operador (= as linhas `PENDENTE_OPERADOR` do quadro **mais** o parágrafo `**Pendências SÓ do operador:**` do handoff, verbatim).
- **Defeito [REAL]:** na v397 o t1 foi gravado depois do commit da Central (`acom_t1.json` às 18:20; commit às 18:20) e ainda diz «falta commit da Central» em `flow.phase` e `next_action`, sem o `git_central` nos `handles`: o texto foi rascunhado antes e postado depois. O G1 gera cada transição **do estado real dos recibos**.

### C18. Central pública (perna 3)

- **Comando hoje:** `cd CEN && PYTHONIOENCODING=utf-8 python -X utf8 work\central_publica_22out\atualizar_central_publica.py --publicar > W\central_publica_vNNN_saida.txt 2>&1` (em segundo plano). `--listar` (somente leitura; rodei agora) imprime os **27 passos**; aceita `--grupo repos|site|tudo`, `--desde "AAAA-MM-DD HH:MM:SS"`, `--so p1,p2`, `--ate p`, `--titulo`. **G1:** `--central-publica` chama este mesmo comando; **não o reimplementa**.
- **Os 27 passos:** *repos:* `incremental_nucleo`, `incremental_work`, `incremental_Chatgpt`, `esteira_no_work`, `readmes`, `indexar_raiz_*` ×3, `conferir_delta_*` ×3, `publicar_*` ×3 (só com `--publicar`); *site:* `retrato`, `acom_anterior`, `acom`, `conferir_acom`, `vincular`, `montar`, `conferir_central`, `llms_site`, `sitemap`, `manifesto`, `subir_ensaio`, `subir` (só com `--publicar`); *fim:* `estado_do_organismo`.
- **Entradas por versão e origem:** nenhuma digitada (o script não tem número de versão [REAL]); `--desde` padrão = hora do último commit de cada preparo (`git log -1 --format=%ct`); o **backend local da Central em `127.0.0.1:8765`** (o `retrato` exporta por GET: `exportar_cockpit_publico.py`, `BASE = "http://127.0.0.1:8765"`); `frontend\dist_publica` **já construído**: o `vite build` não está na cadeia, o `montar` copia o que estiver lá (L15).
- **Sobreposição com a perna 1 [DECLARADO pela ESPEC_ESPELHO_SITE §5, L10 e L11; os cinco nomes conferem com o `--listar` [REAL]]:** `llms_site`, `sitemap`, `manifesto`, `subir_ensaio` e `subir` repetem a cauda da perna 1, e o manifesto cobre o `v3.0` inteiro: quem sobe primeiro publica também o meio-trabalho da outra; `gerar_llms_site.py` depende do `um_acom_info.json` que o passo `acom` desta perna gera. **Ordem imposta pelo G1:** a perna 1 inteira (do gatilho à leitura de IA) e só depois `--central-publica`; ou `--so` sem esses cinco quando a perna 1 já os fez; uma trava comum impede as duas ao mesmo tempo.
- **Saídas:** `C:\IALD\Central_publica\{central-publica, central-publica-work, central-publica-bancada}` (v397: +1.916/50 atualizados; +28.572/3; +12/3; deltas conferidos 1.969 / 28.587 / 18 arquivos, APROVADO), `um.acom` público (88 arquivos, 3.889.836 B), `/central/` no site (1.112 arquivos, 76,5 MB), `llms.txt`, sitemap, manifesto, subida; `rodadas\<ts>.json`. Duração v397: **6.359 s** (os maiores: `incremental_work` 1.255 s, `conferir_delta_work` 876 s, `subir` 852 s, `retrato` 799 s, `publicar_bancada` 693 s, `publicar_work` 650 s).
- **Idempotência:** por desenho: cada incremental cria `_incr_<ts>_<tipo>` novo (`assert not T.exists()`), publica só o delta, e sem delta diz «igual (nada muda)»; retomável por `--so/--ate/--desde`; o registro da rodada é gravado mesmo se parou («PARADO em <passo>»).
- **Gates:** `rc != 0` interrompe a cadeia (exceto `estado_do_organismo`, que é medida); `conferir_delta` APROVADO antes de cada `publicar_*`; `conferir_acom` (0 identificadores de terceiro, 0 padrões de dado pessoal); `conferir_central` APROVADO; `guarda_publica.py`; **ação para fora somente com `--publicar`** (R7).
- **Prosa manual → molde:** o `--titulo` dos commits públicos (padrão com a data); os READMEs públicos são gerados por script. Texto público novo passa pelo portão de texto e, na fase inicial, por revisor distinto (G1 do desenho do organismo).

### C19. Nós vivo e quadro do organismo (a medida final)

- **Comando hoje:** `python C:\IALD\NOS_VIVO\construir.py` (≈ 2 s; regrava `nos_vivo.sqlite3` com backup de bytes do anterior) [DECLARADO: não aparece nos comandos da v397 do transcrito; o quadro cobra `nos_vivo.sqlite3` gravado depois do selo] e `python tools\estado_do_organismo.py [--sem-rede]` (≈ 21 s com rede). **G1:** os dois, nesta ordem, ao fim.
- **Entradas por versão e origem:** o selo (a verdade); cada superfície é lida no disco ou no ar (GET público); nenhuma credencial.
- **Saídas:** `organismo\ESTADO_DO_ORGANISMO.md` e `.json` (ignorados pelo git: `.gitignore` linha 125); resumo no stdout.
- **Idempotência:** só mede; sobrescreve o quadro.
- **Gates:** código de saída 0 (tudo OK), 1 (há `DEFASADO`), 2 (há `FALHA` de leitura). O G1 exige **0 DEFASADO e 0 FALHA** nas superfícies da perna Central; aceita `PENDENTE_OPERADOR` (vai ao t3) e `EM_OBRA` (do Nós, versão seguinte). v397 [REAL, texto do t3]: 84 OK · 0 DEFASADO · 0 FALHA · 9 INFO · 5 PENDENTE_OPERADOR.
- **Mapa item do quadro → passo** (é a ligação "critério = linha do quadro" do desenho do organismo): cofre e kernel `vNNN` → C3; «runner lê o cofre» (`_medir_vNNN_custodia`) → C6; «último resultado do runner» → C7; `VERSAO_DA_CAMADA` → C8; «dispositivos com a camada» 16/16 → C9; «FINAL regerados depois da camada» 16/16 → C10 (depois de C8); ledger → C12; Atlas «A CUSTÓDIA DA vNNN» → C13; git da Central → C14; snapshot posterior ao selo → C5; Central pública (HEAD, README com pino, `llms.txt`, `um.acom` gerado depois do selo e montado igual, cartão das linhas de pesquisa, no ar) → C18; rota `custodia.vNNN`, linha do `MEMORY.md` («CUSTODIADO»/«PUBLICADA») e `handoff-vNNN-custodia.md` → C13/C16; `nos_vivo.sqlite3` → C19; Bancada Um, `ACTIVE.json` e memória científica da fila → C20.
- **Prosa manual → molde:** nenhuma.

### C20. As pernas que o selo já puxa (só conferir)

- **O que são [DECLARADO pela tarefa; medido pelo quadro]:** (a) **Bancada Um**: o selo dispara o elo B(n); recibo `C:\IALD\Bancada_Um\estado\sincronizacao\RECIBO_SINCRONIZACAO_vNNN_<ts>.json` (mais os de parada e religamento do serviço, que `fatos.cadeia.recibos` lista); (b) **memória canônica da fila/app**: `Chatgpt\IALD_ORQUESTRACAO_20260923\state\canonical_memory\ACTIVE.json` com `release == vNNN`; (c) **memória científica da fila**: `work\scientific_memory_sync_*_vNNN\DELIVERY_R1.json` (produzida pela fila do Codex, ordem permanente de 13/10).
- **Comando hoje:** nenhum desta cadeia; o quadro mede (as duas primeiras entraram no medidor em 24/10 por `patch_estado_pernas_do_selo.py`, da sessão em curso). **G1:** só **conferir**, com espera limitada (proposta: 10 min, configurável) e registrar em t3; nunca executar nem reiniciar serviço.
- **Entradas por versão e origem:** `fatos.cadeia.recibos`; o nome do recibo traz a versão.
- **Saídas:** linhas no recibo de C19 e no t3.
- **Idempotência:** leitura.
- **Gates:** `RECIBO_SINCRONIZACAO_<vNNN>` mais novo existe; `ACTIVE.json.release == vNNN`; `DELIVERY_R1.json` existe. Falta = `DEFASADO` visível: **não bloqueia o commit da Central**, bloqueia dizer «custódia concluída» no t3.
- **Prosa manual → molde:** nenhuma.
- **Sobre a pergunta do operador («interligação total … bancada de teste, app e tudo mais»):** o que a perna Central garante é *conferir* (C19, C20): a atualização da Bancada Um e da memória canônica do app acontece pelo selo e pela fila, e a Central **mostra DEFASADO** se não aconteceu. Compilar e publicar o app (TestFlight, Android) é do operador (§9).

---

## 6. PROPOSTA: a pedra genérica do runner (`_medir_vNNN_custodia`)

### 6.1 Contrato

- **Onde mora.** Arquivo novo `fronteira_tgl\runner\custodia_generica.py`, carregado por `one_fronteira.py` **por caminho** (`importlib.util.spec_from_file_location`, como os 16 dispositivos já carregam a camada comum), para não inflar o arquivo (8.628 linhas na v397, 8.757 depois da pedra v47: ≈ 129 linhas por pedra artesanal [REAL]) e para a pedra ser testável sozinha. Assinatura: `medir_custodia_generica(oc, versao, anterior) -> dict`.
- **O que o runner ganha.** Uma vez ("G1.0", troca única): `_custodia_generica(versao, anterior)`, quatro linhas que carregam o módulo e chamam a função com `oc = CUSTODY_DIR.parent`. **Por versão:** o stub de duas linhas `def _medir_vNNN_custodia(): return _custodia_generica("vNNN", "vANT")` (o nome é o que o quadro procura: R6), a chave `"custodia_vNNN"` na `station`, `vNN_pass`, o `and` em `all_pass` e o veredito: as onze trocas da §6.7, e **nenhuma função de 100 linhas**.
- **Lê pelo nome, nunca pelo cofre corrente.** `oc / ("um_unificado_" + versao)` e `oc / ("um_unificado_" + anterior)`: é o que torna a pedra "exata para sempre" (a lição do runner v59) e é o motivo de não precisar de errata nas pedras antigas quando o cofre corrente muda.
- **Fonte das expectativas.** `FATOS_CUSTODIA.json` **dentro do cofre `vNNN`**, com o sha256 conferido contra o `CUSTODY_MANIFEST.json` do mesmo cofre (D1). Se o arquivo falta ou o hash não bate, a pedra reprova com `erro` (fail-closed).
- **O que a pedra *não* faz:** não calcula nada físico, não move o gate, não "conserta" expectativa: se um check falha, o G1 para em C7 e a gerência decide; a pedra nunca é afrouxada por script.

### 6.2 O que se lê de `fatos` e do cofre, e o que não

Já medido: os itens S2 a S10, S12 e S14 passam nas quatro transições v394→v395, v395→v396, v396→v397 e v397→v398 lendo só os cofres [REAL; `medir_mecanico.py`, `medir_mecanico_v398.py`, `checks_blocos.py` e `checks_blocos_v398.py`, no scratchpad], com a ressalva do pino em S8 (abaixo). S1, S11 e S13 dependem do `fatos` schema 2 e **não foram medidos**.

| id | verificação | esperado (fonte) | achado (fonte) | generaliza? |
|---|---|---|---|---|
| S1 | identidade | `fatos.versao`, `fatos.pin` | `selo.um_version`, `selo.sha256["um.py"]`, `sha256(cofre\um.py)` | sim |
| S2 | blocos novos | `fatos.registros_novos`; sumidos = ∅ | chaves de `core` novas e sumidas entre os dois cofres | sim |
| S3 | bloco bem formado | regra fixa: `all_verified` e `does_not_gate_core` `True`; `GATE_UNMOVED` ou `GATE_UNTOUCHED` no veredito; sem `CONFIRMED` sem `NOT_`; **novo:** `checks` (lista de `{ok}` ou dict) todo `True`; `guarda_p18_violacoes == []` | cada bloco novo | sim |
| S4 | bandeiras | `fatos.bandeiras_novas` | chaves novas de `core.kernel_formalization`, todas `True` | sim |
| S5 | cobertura kh | `fatos.kh` | `kh_n1_cobertura_vNNN.lido`; `constantes == len(axiom_report)`; `NONE_OUTSIDE_THE_TRIO` | sim |
| S6 | escada | `fatos.escada` | `estatuto_da_prova_v391.prova_1_kernel`; `KERNEL_{N}_OF_{N}_FLAGS` no veredito | sim |
| S7 | kernel | `fatos.kernel` | proof manifest do cofre: formais, declarações, nada fora do trio, módulos novos = diferença de conjuntos, removidos = ∅ | sim |
| S8 | registro | `fatos.registro` | PT = EN; nomes do anterior presentes; novos = blocos novos; **mudados**: ler `core[nome].verdict` **inteiro** nos dois cofres e normalizar `[0-9a-f]{16,64}`→`<PIN>` e `\d+`→`#`; igual = aceito, senão tem de estar em `SEMANTICA.mudados_permitidos` | sim, **com a ressalva do pino** (abaixo) |
| S9 | gate | `manifesto(vANT).gate` | `selo.qg_closure_verdict` igual; `core.qg_closure.gate.full_static_witness_exists is False` | sim |
| S10 | sem `CONFIRMED` | regra fixa | nenhum `*_verdict` do selo | sim |
| S11 | contratos | `fatos.contratos_expected_ladder` | todos `== fatos.escada.esperadas` | sim (valor já medido por AST na sondagem) |
| S12 | monotonia (novo) | regra fixa | formais, declarações, escada, registro e kh não diminuem; módulos removidos = ∅ | sim: 1424→1425→1426→1428 formais; 9451→9498→9499→9539 de escada [REAL] |
| S13 | negações | `fatos.blocos[k].negacoes` | mesmo conjunto extraído do veredito no cofre | sim: congela o que o rito disse |
| S14 | cunhagens | regra fixa | `cunhagens_vNNN.kernel.bandeiras` e `.declaracoes_no_trio` com par igual e > 0; `len(verbatim) >= 1` | sim: `[2,2]`, `[1,1]`, `[3,3]`, `[2,2]` nas v395 a v398 [REAL] |
| S15 | semântica específica | `SEMANTICA_CUSTODIA.json` (maior revisão) | `verdict_deve_conter`, `verdict_nao_deve_conter`, `campos` | **não se lê: é autoria** (rascunho + revisão) |
| S16 | dois céticos | derivados de S3, S6, S13, S15 | injeções em cópia JSON do `core` (§6.5) | sim |
| S17 | `nao_se_afirma` | união de fixos, `core[k].nao_diz` e `SEMANTICA.nao_se_afirma_extra` | — | parcial |

**A ressalva do pino (S8) [REAL].** Na v398 contra a v397 os cinco registros que mudam são os mesmos cinco das três transições anteriores (`estatuto_da_prova_v391`, `pedras_v392`, `pedras_v393`, `three_stress_tests_v387`, `varredura_e_sorry_v392`). Lendo o texto PT do artigo (a regex `^([a-z][a-z0-9_]{3,}) & ([A-Z][A-Z0-9_]{12,})` da pedra de hoje), o de `estatuto_da_prova_v391` parece diferir além de dígitos, porque o veredito termina em `CERTIFIED_BY_SELF_HASH_<pin16>` e a regex **corta no primeiro minúsculo do pino** (na v397 o pino começa por `388`, na v398 por `c632`: `…SELF_HASH_388` contra `…SELF_HASH_`). Lendo `core["estatuto_da_prova_v391"]["verdict"]` (633 caracteres nas duas versões) e normalizando dígitos **e** pino, os cinco são «só dígitos e pino». A pedra de hoje compara só os **nomes** dos mudados (lista literal), então não quebra; um gerador que quisesse a regra «só dígitos» pela regex do texto PT quebraria na v398.

### 6.3 O que não se pode ler (fica com autoria humana e revisão)

1. **O sentido das negações.** O `fatos` congela *o que o rito disse*; que `…CREDITATION_STEP_NOT_REACHED` é o que **deve** ser dito, e que sua troca por `…REACHED` seria falsificação, é juízo: vem do `SEMANTICA` revisado (§4.3).
2. **Se uma mudança de veredito fora de «dígitos e pino» é legítima** (`mudados_permitidos` com motivo).
3. **Título, sufixo semântico do veredito do runner, docstring do item, `nao_se_afirma` específico:** moldes e citações (§4.5), não leitura.
4. **Se o conteúdo científico do registro novo é verdadeiro.** A pedra confere forma, número e escopo, nunca ciência.
5. **Nomes definitivos de pedras e registros** (todos «provisórios» até o operador nomear) e **a decisão [LEGAL]** da paridade do ACOM Mirror.

### 6.4 Algoritmo

```python
def medir_custodia_generica(oc, v, a):                       # oc = vault\originals_copy ; v = "vNNN" ; a = "vANT"
    out = {"pass": False, "physical_verdict_allowed": False,
           "estatuto": "REAL(lido do cofre %s e do %s pelo nome) / dois ceticos por injecao" % (v, a)}
    try:
        cv, ca = oc / ("um_unificado_" + v), oc / ("um_unificado_" + a)
        man_v, man_a = ler_json(cv / "CUSTODY_MANIFEST.json"), ler_json(ca / "CUSTODY_MANIFEST.json")
        F = ler_json_com_pino(cv, man_v["fatos_custodia"])          # sha256 conferido; ausente ou divergente = erro
        S = semantica_de_maior_revisao(cv, man_v)                   # pode nao existir: DECLARADO sem revisao
        core, core_a = ler_json(cv / "um_absoluto.json")["core"], ler_json(ca / "um_absoluto.json")["core"]
        selo = ler_json(cv / "um_absoluto_selo.json")
        pm = ler_json(oc / ("tgl_kernel_" + v) / "tgl_kernel_proof_manifest.json")
        pt, en, pt_a = ler_txt(cv / "um_absoluto_pt.txt"), ler_txt(cv / "um_absoluto_en.txt"), ler_txt(ca / "um_absoluto_pt.txt")
    except (OSError, ValueError, KeyError) as e:
        out["erro"] = "cofre ilegivel: %r" % (e,); return out       # fail-closed
    mec = _mecanica(core, core_a, selo, pm, pt, en, pt_a, man_a, F, S)     # S1..S14, cada um {ok, esperado, achado}
    sem = lambda c: _semantica(c, F, S)                                    # S13 (+ S15 se ha semantica revisada)
    c1 = copia_profunda(core); injetar_negacao_removida(c1, F, S)          # cetico 1
    c2 = copia_profunda(core); injetar_contagem(c2)                        # cetico 2
    cet1, cet2 = (sem(c1) is False), (sem(c2) is False)                    # a injecao TEM de reprovar
    out.update(_relatorio(mec, sem(core), cet1, cet2, F, S))
    out["pass"] = bool(all(x["ok"] for x in mec.values()) and sem(core) and cet1 and cet2)
    return out
```

- `_mecanica` é a transcrição de `medir_mecanico.py` (S1 a S12 e S14) e do S13 sobre `fatos`; `_semantica` junta S13, S14 e S15 numa função **pura** sobre um `core` (para poder ser rodada sobre as cópias injetadas).
- `ler_json_com_pino` lê o arquivo, calcula o sha256 e compara com `man_v["fatos_custodia"]["sha256"]`.
- **Sem estado e sem relógio:** a pedra não grava nada, não lê `CUSTODY_DIR`, não olha o Nós (que já seguiu adiante), só os dois cofres.

### 6.5 Os dois céticos

- **Cético 1, polaridade** (mantém o desenho atual, que injeta «NOT_REACHED → REACHED» no veredito de veracidade): em cópia profunda do `core`, tira de **um bloco novo que tenha negação em `fatos.blocos`** um token `NOT_…` do `verdict` (ou o troca por `…` sem o `NOT_`); `_semantica` tem de reprovar. Se nenhum bloco novo tem negação, o cético 1 vira: `all_verified` do primeiro bloco novo = `False`.
- **Cético 2, contagem** (mantém o desenho atual, que injeta `bandeiras = [2, 3]`): em cópia profunda, soma 1 a `estatuto_da_prova_v391.prova_1_kernel.n_theorems_expected`; se existe `cunhagens_vNNN`, também tira 1 de `kernel.bandeiras[0]`; `_semantica` tem de reprovar.
- **Regra herdada:** se uma injeção *não* reprova, o check não discrimina e **a pedra reprova**. Os controles negativos dos testes (§8) vão além: uma mutação por check S1 a S14.

### 6.6 Saída (mesmas chaves das pedras artesanais, para os consumidores não mudarem)

`pass`, `estatuto`, `physical_verdict_allowed` (sempre `False`), `blocos_novos_desde_<vANT>` `{n, nomes, sumidos, fora_da_regra, ok}`, `bandeiras_novas_desde_<vANT>` `{n, ok}`, `registros_<vNNN>` `{ok, estatuto}`, `ceticos` `{1_injecao, 1_reprovou, 2_injecao, 2_reprovou, leitura}`, `gate` `{full_static_witness_exists, identico_ao_cofre_<vANT>}`, `registro_de_vereditos` `{pt, en, esperado, nomes_<vANT>, novos, mudados_desde_<vANT>, ok}`, `kernel` `{formais, termos, ok}`, `vereditos_do_selo_com_CONFIRMED`, `nao_se_afirma`. Acrescenta: `semantica` (`"REVISADA rev<n>"` ou `"DECLARADO (sem revisao)"`), `fatos_sha16`, `checks` (S1 a S14, cada um `{ok, esperado, achado}`) e `mudados` (`so_digitos_e_pino` por nome). O `registro_vNNN.py`, o `rodar` e o quadro leem `the_station.custodia_vNNN.pass` e o veredito: nada disso muda.

### 6.7 O patch do runner: onze trocas contadas, por âncora regex

> [nota operacional do operador — omitida no retrato público]

| # | âncora (regex sobre o texto em LF) | n | troca |
|---|---|---|---|
| 1 | `"""FRONTEIRA TEORICA TGL v(\d+) — auto-auditoria honesta do fechamento, SINCRONIZADA ao um\.py v(\d+)\.` | 1 | `v{MM+1}`, `v{NNN}` |
| 2 | `A custodia viva passou a ser vault/originals_copy/um_unificado_v(\d+)\. O RENOME v209: o selo` | 1 | `v{NNN}` |
| 3 | `\((\d+) arquivos formais no manifesto v(\d+); entre` | 1 | `{formais}`, `v{NNN}` |
| 4 | `Fonte canonica sincronizada \(custodia\): um\.py unificado v(\d+) \(pin` | 1 | `v{NNN}` |
| 5 | `CUSTODY_DIR = CENTRAL_DIR / "vault" / "originals_copy" / "um_unificado_v(\d+)"` | 1 | `v{NNN}` |
| 6 | `print\(f"\[fronteira v30\] CUSTODIA um\.py v(\d+): pin` | 1 | `v{NNN}` |
| 7 | `^def shadow_the_station\(core, selo\):$` | 1 | inserir o stub antes (e, na primeira vez, o carregador G1.0) |
| 8 | `^        "custodia_v(\d+)": _medir_v\1_custodia\(\),$` | 5 | acrescentar a nova depois da última |
| 9 | `^    v(\d+)_pass = station\["custodia_v(\d+)"\]\["pass"\]$` | 5 | acrescentar `vNN_pass` (com comentário) depois da última |
| 10 | `and v(\d+)_pass\)$` | 1 | `and v{NN}_pass and v{NN+1}_pass)` |
| 11 | `^        verdict = \("FRONTEIRA_SINCRONIZADA_V(\d+)"$` | 1 | as três linhas da §6.8 |

- `vMM` (runner) e `vNN` (pedra) são lidos do próprio arquivo (cabeçalho e último comentário `# vNN (vMM): A CUSTODIA…`) e incrementados: nada digitado. Nas trocas de repin, a diferença para o patch artesanal da v62 é que as âncoras **capturam a versão** em vez de casar a prosa da versão anterior (o patch da v62 casa, por exemplo, `"(1425 arquivos formais no manifesto v396; entre"`, que só existe uma vez porque a anterior o escreveu assim).
- **G1.0 (troca única, antes da primeira versão genérica):** inserir antes de `def shadow_the_station` o carregador

```python
def _custodia_generica(versao, anterior):
    import importlib.util as _ilu
    _s = _ilu.spec_from_file_location("custodia_generica", str(HERE / "custodia_generica.py"))
    _m = _ilu.module_from_spec(_s); _s.loader.exec_module(_m)
    return _m.medir_custodia_generica(CUSTODY_DIR.parent, versao, anterior)
```

> [nota operacional do operador — omitida no retrato público]

### 6.8 O veredito do runner

O veredito é uma cadeia de segmentos `__V<NNN>_<descrição>` por versão, do mais novo ao mais velho. O patch substitui a linha `verdict = ("FRONTEIRA_SINCRONIZADA_V<ANT>"` por

```
        verdict = ("FRONTEIRA_SINCRONIZADA_V<NNN>"
                   "__V<NNN>_<TITULO_SLUG>__COFRE_V<NNN>_CONTRA_O_V<ANT>_PELO_NOME__<N>_BLOCOS_NOVOS_VERIFICADOS_NENHUM_MOVE_O_GATE__<NB>_BANDEIRAS__ESCADA_<E>_DE_<E>_BANDEIRAS__KERNEL_<F>_<D>_NO_TRIO__<SUFIXO_SEMANTICO>__REGISTRO_<NREG>_COM_OS_<NREGANT>_DA_V<ANT>_E_<NMUD>_MUDADOS_DITOS__DOIS_CETICOS__GATE_INALTERADO"
                   "__V<ANT>"
```

e a linha seguinte (já existente, `"__V<ANT>_<descrição antiga>"`) continua a cadeia. `<TITULO_SLUG>` e `<SUFIXO_SEMANTICO>` vêm do `SEMANTICA` (maiúsculas, `_`, ASCII); sem revisão, o sufixo é `SEMANTICA_DECLARADA_SEM_REVISAO` e o slug é derivado do título da linha do handoff no `MEMORY.md`. O quadro só exige o prefixo `FRONTEIRA_SINCRONIZADA_V<NNN>`.

### 6.9 Compatibilidade (R6) e falhas

- Ficam com os mesmos nomes: `_medir_vNNN_custodia` (stub), `the_station["custodia_vNNN"]`, `vNN_pass`, o prefixo do veredito, as chaves da saída (§6.6).
- **Falha de um check:** a pedra reprova, o runner devolve outro veredito (sem `FRONTEIRA_SINCRONIZADA_V<NNN>`), C7 para, o recibo diz qual `S<k>` falhou com `esperado` e `achado`. Não há reparo automático: reparar = decisão da gerência e, se for o caso, `mudados_permitidos` no `SEMANTICA` (revisado).
- **Em caso de custódia conjunta** (`vANT` não é `NNN-1`): a pedra recebe o `anterior` do `fatos` e compara com ele; os segmentos de veredito das versões intermediárias não existem, e o sufixo `__V<ANT>` aponta para a pedra anterior que existe.

---

## 7. PROPOSTA: o item genérico do módulo dos 16 dispositivos (`conferir_vNNN_no_cofre`)

### 7.1 Contrato

- **Onde mora.** Em `patents\_formula_completa\`, num módulo irmão `tgl_custodia_generica.py` carregado **por caminho** a partir de `tgl_formula_completa.py` (`Path(__file__).parent / …`), porque os dispositivos carregam a camada comum por `spec_from_file_location` e porque `build_final_code.py` empacota **toda** a pasta `_formula_completa` em cada `*_FINAL.py` [REAL: `_walk(PATENTS / "_formula_completa", …)`]. Alternativa: o código dentro de `tgl_formula_completa.py` (um arquivo só; o diff por versão fica maior). Assinatura: `conferir_custodia_generica(core, selo, versao, cofre_raiz) -> dict`, que levanta `RuntimeError` (fail-closed) em qualquer check que falhe, como as camadas v386 a v397.
- **O que o módulo principal ganha** (G1.0, uma vez): `CAMADAS_GENERICAS = ("vNNN", …)`, o laço dentro de `conferir_no_cofre` e a mistura das chaves `camada_<v>_no_cofre` no dicionário devolvido. **Por versão**: acrescentar a versão à tupla, `VERSAO_DA_CAMADA`, o parágrafo da docstring, o sufixo do `veredito`, os itens de `nao_se_afirma` e a entrada de `USOS` (§7.4).
- **A camada roda contra o cofre *corrente*, não contra o da sua versão.** Quando a v400 chegar, a camada da v399 continua rodando nos 16 dispositivos, lendo o cofre v400. Logo ela só pode checar o que **sobrevive à reescrita**: os blocos `*_vNNN` nunca somem do `core` (`registros_sumidos == []` em toda custódia), mas o *conteúdo* de vários é reescrito a cada rito [REAL, comparação em profundidade do `core` do Nós v398 com o do cofre v397: 56 blocos diferem, 25 deles com sufixo de versão]: `runtime_s`, contagens da escada, `lido` dos `kh_n1_cobertura_*` (o de `kh_n1_cobertura_v397` passou de 29229 para 29294 constantes, ganhou uma `erratas` e teve `checks[].descricao` emendados) etc.; já o **veredito** desses blocos, e blocos como `cunhagens_v397` e `teste_de_veracidade_fase9_v397`, ficam idênticos em profundidade. Por isso a camada checa presença, forma, negações **normalizadas** e pares de `cunhagens`, e **nunca** números que andam (escada, kh, kernel). Ela lê o `FATOS_CUSTODIA.json` **do cofre `vNNN` pelo nome**.

### 7.2 O que se lê e o que não

| id | verificação (todas invariantes à reescrita dos blocos) | fonte | observação |
|---|---|---|---|
| I1 | os blocos `*_vNNN` do `core` corrente são exatamente `fatos.registros_novos` | `core` (cofre corrente) × `FATOS_CUSTODIA` do cofre `vNNN` | hoje: `novos = sorted(k for k in core if re.search(r"_vNNN$", k))` |
| I2 | cada bloco bem formado (regra S3: `all_verified`, `does_not_gate_core`, gate, sem `CONFIRMED`, `checks` ok, `guarda_p18_violacoes == []`) | `core` | igual às camadas v394 a v397 + os dois campos novos |
| I3 | `escada_limpa`: `n_theorems_clean == n_theorems_expected` e `declaracoes_auditadas == no_trio` | `core.estatuto_da_prova_v391.prova_1_kernel` do cofre corrente | **consistência interna**, sem comparar com o número da versão (a escada anda) |
| I4 | as negações congeladas no `fatos` continuam no veredito do bloco, comparadas com dígitos e pinos normalizados (`\d+`→`#`, hex de 16 a 64→`<PIN>`) | `fatos.blocos[k].negacoes` ⊂ `core[k].verdict` | substitui a checagem artesanal de `THE_CREDITATION_STEP_NOT_REACHED` etc.; o veredito de `kh_n1_cobertura_v397` é idêntico na v398 [REAL] |
| I5 | `cunhagens_vNNN`: pares de `kernel` iguais e > 0; `len(verbatim) >= 1` | `core` | hoje: `list(kn.get("bandeiras")) == [3, 3]` (literal) |
| I6 | a semântica revisada, se existe, vale | `SEMANTICA_CUSTODIA` do cofre `vNNN` | `verdict_deve_conter`, `campos` |

**Não se lê (autoria + moldes):** o sentido das negações; o parágrafo da docstring; os itens de `nao_se_afirma`; o sufixo do `veredito`; os nomes definitivos (§6.3). Os números (escada, kh, kernel) **não** entram na camada: ficam na pedra do runner, que lê os dois cofres congelados.

### 7.3 Saída (a camada devolve, o runner do dispositivo grava em `results.json`)

```json
{"checks": {"registros_vNNN_verificados_sem_gate": true, "negacoes_congeladas_presentes": true,
            "cunhagens_par_igual": true, "falas_do_operador_por_sha256": true, "escada_limpa": true},
 "registros_vNNN": ["..."], "escada": "n/m", "declaracoes_no_trio": 0,
 "veredictos": {"<bloco>": "<verdict[:160]>"}, "nao_diz": {"<bloco>": ["<verbatim do core>"]},
 "semantica": "DECLARADO (sem revisao)", "estatuto": "lidos do cofre e conferidos, sem interpretacao; nao move gate; nao muda numero de dispositivo"}
```

A chave externa continua `camada_vNNN_no_cofre` dentro de `conferencia_no_cofre`: é o texto que `rodar_16`, `registro_vNNN.py` (`'"camada_vNNN_no_cofre"' in results.json`) e o quadro procuram.

### 7.4 O patch do módulo: âncoras regex (CRLF; contagens medidas hoje)

> [nota operacional do operador — omitida no retrato público]

| # | âncora (regex em LF) | n | uso |
|---|---|---|---|
| 1 | `^VERSAO_DA_CAMADA = "v(\d+)"` | 1 / 1 | trocar para `v{NNN}`; o comentário `# (era "vANT"; …)` que cresce a cada versão sai |
| 2 | `^Régua: β NUNCA literal \(sempre ALPHA_FINE_CODATA_2018` | 1 / 1 | inserir antes o parágrafo da docstring (§7.5) |
| 3 | `^def conferir_no_cofre\(rt: dict\) -> dict:$` | 1 / 1 | **G1.0:** inserir antes `CAMADAS_GENERICAS = ()` e o carregador de `tgl_custodia_generica.py` |
| 4 | `^    v(\d+) = conferir_v\1_no_cofre\(core, selo\)\s+# camada v\1 \(item (\d+)\); fail-closed$` | 5 / 6 | **G1.0:** depois da última, o laço `for _v in CAMADAS_GENERICAS: …`; o número do item vem do último `(item N)` + 1 |
| 5 | `"camada_v(\d+)_no_cofre": v\1\}$` | 1 / 1 | **G1.0:** trocar `}` por `, **_camadas_genericas}` |
| 6 | `"RECALCULADA_E_CONFERIDA_NO_COFRE__NOT_A_CONFIRMATION"\) % VERSAO_DA_CAMADA\.upper\(\),$` | 1 / 1 | inserir antes a linha do sufixo do veredito |
| 7 | `"\],\n    \}\n\n\nif __name__ == "__main__":` | 1 / 1 | inserir antes do `]` os itens de `nao_se_afirma` |
| 8 | `\n\}\n\n\ndef uso_no_dispositivo` | 1 / 1 | inserir antes do `}` a entrada de `USOS` |
| 9 | `^CAMADAS_GENERICAS = \((.*)\)$` | 1 depois do G1.0 | por versão: acrescentar `"vNNN",` à tupla |

- As camadas artesanais v386 a v397 **ficam como estão** (exatas para sempre); a v398 (em curso, artesanal) também.
- **Não aplicar agora.** A sessão da v398 acabou de remendar este módulo (780 → 839 linhas). O G1.0 e os patches por versão são escritos em `work\custodia_G1\patches\` e só são aplicados depois de a v398 estar publicada e conferida.
- **Depois do patch**, o passo executa `python tgl_formula_completa.py` (o `__main__` de hoje roda `camada(__file__)` e imprime `veredito` e `conferencia_no_cofre`): um elo quebrado levanta `RuntimeError` e o passo para antes de C9.
- **Efeito colateral esperado:** o `modulo_sha256` que cada `results.json` grava muda; os 16 `*_FINAL.py` têm de ser regenerados depois (C10), e o quadro confere isso por mtime.

### 7.5 Moldes do item

- **Parágrafo da docstring:** `Camada vNNN (custódia vNNN na Central, DD/MM/AAAA, <ator>; handoff vNNN da gerência c1):` + ` N. os registros novos da vNNN (<b1>, <b2>, …), lidos e conferidos no cofre, sem interpretação: ` + para cada bloco, a primeira sentença de `core[bloco].estatuto` **entre « »**, mais `SEMANTICA.docstring_item` se houver revisão + ` Nada disso muda número algum de dispositivo.` (a frase final é fixa e é a das camadas v390 a v397).
- **`USOS` (medida de ocorrências no código do dispositivo; não interpreta):** chave `<slug>_vNNN`; regex gerada de `fatos.kernel.modulos_novos` (o nome do módulo sem `.lean`, como `TGLExt\.(Token)`) e dos nomes dos blocos novos. Nas v395 a v397 as regexes foram escritas à mão com as mesmas fontes.
- **`nao_se_afirma`:** `"(vNNN, <bloco>) <nao_diz[i]>"` citando **verbatim** cada item de `core[bloco].nao_diz` (os blocos novos têm de 1 a 8 itens; na v398: `sonico` 6, `afinacao` 8, `cunhagens` 4, `kh` 1 [REAL]) mais `SEMANTICA.nao_se_afirma_extra`. O item fixo sobre `[LEGAL]` (paridade do ACOM Mirror) e os que a v394 a v397 acumularam ficam.
- **Sufixo do `veredito`:** `SEMANTICA.veredito_camada_sufixo` ou, na falta, `REGISTROS_VNNN_VERIFICADOS_SEM_GATE__SEMANTICA_DECLARADA_SEM_REVISAO__`.
- **`estatuto` do retorno:** frase fixa («lidos do cofre e conferidos, sem interpretação; não move o gate; validade no kernel não é creditação; nada disto muda número de dispositivo») + `SEMANTICA.estatuto`.

---

## 8. Oráculo e testes de aceitação [PROPOSTA]

O desenho do organismo pede o oráculo do G1 em dois níveis: **artefatos finais iguais aos de ontem** e **as mesmas asserções passando**, validado contra **duas transições** (v394→v395 e v395→v396), não uma. Para a perna Central isso se traduz em testes que rodam em `work\custodia_G1\testes\`, **sem tocar no estado vivo** (raízes substituíveis `--nos/--oc/--saida`):

> [nota operacional do operador — omitida no retrato público]

- **Limites honestos do oráculo.** O Nós já não tem os artefatos selados da v395 a v397: o replay do cofre (T4) precisa do «Nós substituto» montado a partir dos próprios cofres (por isso mede a *cópia*, não a origem). O espelho, o site e o ar não são reproduzíveis para uma versão passada (perna 1). Para o FINAL o critério é `files[].sha256`, nunca `combined_sha256` (§C10).
- **Barra mínima antes do primeiro uso vivo:** T1, T2, T5, T6 e T7 verdes. T4 antes de o construtor de cofre substituir o `cofre_vNNN.py` derivado.
- **Quem constrói não aprova:** os testes são revisados por um agente distinto do que escreveu o G1 (regra da casa).

### 8.1 Ordem sugerida de implementação (cada item termina com os seus testes)

1. `fatos` schema 2 + construtor de cofre (corrige L1) + `FATOS_CUSTODIA.json` no cofre — T4.
2. Pedra genérica + item genérico + patches por âncora (G1.0) — T1, T2, T3, T5, T6.
3. Recibos de passo + registro por moldes com sentinelas (L2, L3, L6, L7) — T7, T8.
4. Commit com lista de permissão e conferência final parametrizada (L5) — T8.
5. `custodiar.py central` com `--preflight`/`--retomar`, trava e portão de texto (L30) — ensaio completo contra a v399 quando ela selar.
6. Só então ligar o vigia (G2), na modalidade que o operador decidir (L17).

---

## 9. O que não é do G1 (gates que a régua reserva ao operador)

O G1 **registra como `PENDENTE_OPERADOR`** (no t3 e no quadro) e **nunca age** sobre:

1. **Nomear** pedras e registros (todos «provisórios» até o operador dizer; o G1 detecta a palavra «provisório» no handoff e lista).
2. **[LEGAL]:** a paridade do ACOM Mirror (BR 10 2026 003428-2), com a agente de PI.
3. **Zenodo** (a versão depositada fica atrás do selo: o quadro a marca `PENDENTE_OPERADOR`).
4. **Reescrever histórico público** (o que a Central pública já publicou).
5. **Mudança do `qg_closure_verdict`:** o gate não se move por custódia; C0 e C3 param.
6. **Painéis e credenciais** (hospedagem de `iald.ia.br`, Cloudflare, rotações de chave): modo seguro, o operador digita; o G1 não lê credencial (`.env`, `auth.json`, `.credentials.json`, `~/.iald_keys`).
7. **Builds e distribuição do app** (TestFlight, Android): fora da cadeia.
8. **Texto público novo:** portão de texto + revisor distinto, e aprovação do operador na fase inicial até N custódias sem erro.
9. **Commit/push e `--publicar`:** são da gerência pela regra de 23/10 («pode custodiar sempre que o handoff aparecer, como regra»), mas o `custodiar.py` os liga **só** com `--commit`, `--push` e `--central-publica`. Se o vigia (G2) pode ligá-los sozinho é decisão do operador (L17).

---

## 10. Lacunas

Gravidade: **A** = pode produzir estado errado ou perda se não tratado antes de automatizar; **M** = degrada a confiança ou o custo; **B** = limpeza. «Dono» = quem decide ou executa. Cada item traz a evidência.

### 10.1 Defeitos medidos nos scripts de hoje

> [nota operacional do operador — omitida no retrato público]

### 10.2 Riscos de desenho

> [nota operacional do operador — omitida no retrato público]

### 10.3 Decisões e limites que não são de código

- **L16 [M] Oráculo parcial.** O Nós já não guarda os artefatos selados da v395 a v397: o replay do cofre usa um «Nós substituto» montado dos cofres (mede a cópia, não a origem); espelho, site e ar não se reproduzem para versão passada (§8).
- **L17 [A, decisão do operador] Publicação sem a gerência.** A regra de 23/10 («pode custodiar sempre que o handoff aparecer, como regra») foi dada à gerência, que na v397 fez commit, push e `--publicar`. Se o vigia (G2) pode ligar `--commit --push --central-publica` sozinho, ou se para em «pronto para publicar» até N custódias sem erro (a rampa do HSTS), é o operador quem diz.
- **L18 [M] Quem revisa o `SEMANTICA`.** Sem revisão a pedra roda `DECLARADO`. O revisor distinto pode ser um cético de modelo barato ou a gerência; o custo e o prazo da revisão não estão medidos. Decisão da gerência (gestão de tokens: o modelo caro só no essencial).
- **L19 [M] Concorrência nas memórias.** `tocar()` lê, altera e substitui o arquivo inteiro (o Atlas tem 8,6 MB); outra sessão apendou ao Atlas em 23/10 («apêndice do Atlas de outra sessão») e a árvore tem ` M memory/TGL_ATLAS.md` agora [REAL]. Entre a leitura e o `os.replace` uma escrita alheia se perde em silêncio. **Ação:** trava de arquivo e, antes de substituir, comparar tamanho e mtime com os lidos; se mudaram, reler e refazer o apêndice.
- **L20 [M] O quadro procura por nome.** `estado_do_organismo.py` procura `_medir_<V>_custodia`, `camada_<V>_no_cofre`, `VERSAO_DA_CAMADA`, `A CUSTÓDIA DA <V>`, `custodia.<V>` e a linha `HANDOFF <V>` (R6). O G1 mantém esses nomes; se algum dia mudar, o medidor muda junto (não foi alterado aqui). Proposta: o medidor aceitar também a chave `custodia_<V>` no último resultado do runner. Dois pressupostos do medidor vencem na v400 ou numa custódia conjunta [REAL, lidos no código; a ESPEC_ESPELHO_SITE L15 e L20 os mediu também]: a regex do diário é `\*\*(v3\d\d) SELADA` (na v400 o item «última versão selada» reprova) e o backup do espelho é procurado como `um_v<N-1>_*` (numa custódia conjunta dá `DEFASADO` falso).
- **L21 [B] Dois pontos de retenção.** Backups `.bak_*` (FINAL; Atlas de 8,6 MB a cada registro) crescem sem teto; «nunca apagar» vale para a sessão, a retenção entre sessões é do operador.
- **L22 [B] `FORA_RE` é lista manual.** Diretório de ensaio com nome novo entra em silêncio na cadeia de selo do cofre; o gate de ±50% na contagem mitiga (§C3).
- **L23 [M] A esteira de hoje vive fora do git.** `git ls-files work` = 0 [REAL]: `sondar`, `cofre`, patches, registro e conferência só sobrevivem em disco e na Central pública (`central-publica-work`); `rodar_16_vNNN.py` e `rodar_finais_v394.py` moram no scratchpad temporário da sessão. O G1 vai para `tools\custodia_g1\` (rastreado).
- **L24 [B] Fuso.** O transcrito da sessão grava UTC (local = UTC−3); os recibos do G1 devem gravar ISO com fuso.
- **L25 [M] Falta um contrato de recibos entre pernas.** C13 lê o git do espelho, `MAPA_FONTES_PINADAS.json`, `subidas\*\RELATORIO.md` e `leitor_ia_*` («o mais novo por mtime»). **Ação:** cada perna grava um JSON de saída com campos fixos (commit, pino, estado, caminhos) que a Central lê.
- **L26 [B] `NOS_VIVO\construir.py` não aparece nos comandos da v397** [DECLARADO: a leitura do transcrito]; o quadro cobra o banco gravado depois do selo. Quem o regravou em 23/10 não foi esta cadeia.
- **L27 [B] O runner rodado duas vezes.** As duas saídas da v62 só diferem em `result_hash`; cada execução custa ≈ 38 s e acrescenta um `fronteira_<ts>.json` ao commit. Manter duas como gate de estabilidade, ou uma mais confirmação opcional, é decisão da gerência.
- **L28 [B] Adoção.** A v398 está sendo custodiada pelos scripts artesanais (`patch_runner_v63.py`, `patch_formula_v398.py`, `registro_v398_publicada.py` já existem na pasta da sessão). O G1 vale a partir da v399; as âncoras da §6.7 e da §7.4 foram contadas com a v398 já no runner e toleram as duas.
- **L29 [M] Protocolo de missão.** Esta especificação usa só `session_memory.py` (init/project/transition). O desenho do organismo (G2) prevê `mission_cli.py configure` com critérios = linhas do quadro; não li `mission_cli.py` nem `MISSION_PROTOCOL.md` e não o especifiquei.
- **L30 [M] O portão de texto não existe como script.** O item (2) do G1 (lista fechada) é descrito no desenho, e há um guarda parecido no `pensamento_do_dia.py` (do X); nenhum script da custódia o aplica hoje (as únicas travas são `assert "CONFIRM" not in v.upper()` na rota e `assert size > len(raw)`). Ver também a ESPEC_ESPELHO_SITE L17: não há hook de pré-push.

- **L31 [M] Duas esteiras, duas travas, dois conjuntos de chaves.** A ESPEC_ESPELHO_SITE propõe a trava `BK\.custodia_lock.json`, `--ensaio`/`--publicar` e os códigos 0/10/20/30/40; esta propõe `W\LOCK` e `--commit`/`--push`/`--central-publica`. **Ação:** o implementador unifica: uma trava por versão em `work\custodia_G1\runs\`, um só conjunto de chaves (`--publicar` liga as três finas) e a mesma tabela de códigos de saída.

### 10.4 O que esta leitura não cobre

Não reexecutei nenhum passo que escreve; a idempotência do ACOM é [DECLARADO]; os tempos de C3 e C4 vêm de mtimes e do transcrito, não de cronômetro; não li `guarda_publica.py`, `conferir_delta.py`, `mesclar_incremento.py`, `gerar_readmes_publicos.py`, `pensamento_do_dia.py`, `mission_cli.py`, `MISSION_PROTOCOL.md` (só o encadeador `atualizar_central_publica.py`, `rodar_incremental.py` e o cabeçalho de `refazer_retrato.py`/`exportar_cockpit_publico.py`); não conferi se `rotas.py registrar` aceita um `RESULTADO` sobre rota de outra sessão; o `--listar` foi o único comando da perna 3 que rodei.
