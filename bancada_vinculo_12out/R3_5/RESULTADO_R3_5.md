VINCULO R3.5 — 19/10

# Resultado da R3.5 do esboço `sincronizar_bancada.py` (F0.6, gerência c1)

Construtor: subagente da gerência c1 (Sonnet). Base: a R3.4 em `../R3_4/` (esboço `12d504a1114f9f9c`). Todo hash e todo número abaixo foi lido dos arquivos por `_construcao/gerar_resultado_r3_5.py`; os hashes dos entregáveis estão em `PINOS_R3_5.json`. Esboço R3.5: sha16 `02b22ba5c6d35c71`.

Pedido (revisão independente `work/cadeia_de_selo/v394_exame/delta/EXAME_DELTA_E_R3_4.md`, parte B; a v394 já está instalada e o rito corre): (1) fechar o filtro dos módulos de auditoria com lista de PERMISSÃO estrita, com controle negativo para cada evasão, re-rodar todos os controles em `C:/t/vb11` e provar que o recibo pre_selo `0d82d598` da R3.4 segue valendo; (2) fundir o `PINOS_BN` vivo com o que é da R3.4/R3.5; (3) re-derivar o passo 10 do pós-rito.

## 1. Veredito

**`TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO`: 596/596 em 1222 s**, com `python -I -B -X utf8` no sandbox curto `C:/t/vb11` [REAL, `CONTROLES_NEGATIVOS_R3_5.json`, sha16 `ac50fd6ce5a6b754`]:
- os 547 controles da R3.4 presentes 547/547 (e, dentro deles, os 401 da R3.3: 401/401), com os mesmos nomes; 61 mudaram de formato, cada um com o motivo em `controles_da_R3_4_que_mudaram_de_formato` (52 porque ganharam `--nos` do stand-in v393, §3);
- 49 controles novos: 41 `R35_M_` (a lista de permissão; 36 evasões), 6 `R35_V_` (o recibo pre_selo real) e 2 `R35_P_` (a bateria da v394 contra o candidato real);
- a 1ª rodada deu 594/596 (JSON em `_construcao/rodada1_CONTROLES_NEGATIVOS_R3_5.json`): um controle herdado (`R32_R31_1_guarda_antes_de_qualquer_import`) pegou uma linha do MEU parágrafo de docstring que começava por `import` (o parágrafo foi reescrito) e um `R35_V_` meu esperava um prefixo só de recusa (a recusa real, `CADEIA_DE_SELOS_NAO_PARTE_DA_BANCADA`, é igualmente legítima: expectativa corrigida). A rodada que vale é a 2ª, com o esboço e os controles finais.

## 2. (1) A lista de permissão estrita [REAL, `DIFF_R3_4_R3_5.patch` sha16 `c25b5c7f385bf608`, 3 arquivos, reproduz bit a bit com `core.autocrlf=false`]

- **Defeito (B-M da revisão):** a R3.4 recusava por lista de PROIBIÇÃO, com um lookbehind que excluía o ponto; passavam `Lean.addDecl`, `Lean.modifyEnv` e `Lean.Meta.evalExpr` qualificados, `open IO.FS in` + `writeFile` e `open IO in` + `Process.output`. Reproduzidos, eram aceitos; agora são recusados.
- **Conserto:** `auditar_fonte_de_auditoria` passa a lista de PERMISSÃO. Comandos de topo: `import` só de `Lean`, `TGLExt.*` ou `TGL.*`; `open` só de `Lean`; `#print axioms`; `run_cmd`. No corpo do `run_cmd` (código executado na compilação), cada token tem de estar num vocabulário FECHADO: 15 palavras (`let`, `mut`, `for`, `in`, `do`, `if`, `then`, `else`, `unless`, `match`, `with`, `fun`, `some`, `pure`, `_`), 11 locais, 8 funções globais (`Elab.Command.liftCoreM`, `getEnv`, `collectAxioms`, `throwError`, `IO.println`, `toString`, `String.intercalate`, `Name.toString`), 10 métodos, 3 nomes com crase mais os de `TGLExt`/`TGL`, números, literais de texto (interpolação só de local) e 14 sinais. Qualquer outro token é recusado, qualificado ou não, aberto por `open` ou não; `;`, `$`, comentário na linha, caractere não ASCII fora de texto, local novo e método fora da lista também.
- **Controles novos (`R35_M_`):** as cinco evasões exatas da revisão e as mesmas com o `open` permitido; variantes de qualificação (`_root_`, `IO.FS.writeFile` completo, `IO.Process.spawn`, `System.FilePath`), método do local (`env.addDecl`), campo depois de parênteses, tab, interpolação de termo, `;`, `$`, comentário na linha, `include_str`, `unsafe`, nome com crase fora da lista, homóglifo cirílico, local novo, número colado, escape e texto sem fechamento; `open` de `Lean.Meta`, de `Lean IO`, de `IO` sem `in`; `import` de `Mathlib` e de `Lean.Elab.Command`; `run_cmd` com comando na mesma linha. Cada um passa por `variante_auditoria` + `verificar_kernel_recibo` (o caminho real do B(n)) e o detalhe nomeia o token. Contraprova: a fixture inalterada passa. O derivador também recusa as evasões. As 3 fontes REAIS (`NetworkProofAuditR3/R7/R8`) passam (R3: 936 `#print axioms`; R7 e R8: um `run_cmd` de 121 tokens cada), inclusive na árvore real do kernel (`C:/t/k394d/arvore`, sha igual ao do recibo).
- **O recibo pre_selo real `0d82d598229fd398` continua valendo (`R35_V_`):** o recibo gerado pela R3.4 antes da instalação (`script_sha256` `12d504a1114f9f9c`, diferente do da R3.5 `02b22ba5c6d35c71`) é aceito, sem mudar um byte, por `conferir_recibo_pre_selo` da R3.5 contra a Bancada de PRODUÇÃO real (só lida), o selo e o manifesto do kernel da v393 (custódia) e a cadeia: veredito `REPINADA_B4__SALTO_v392_v393__ENSAIO__NADA_GRAVADO_NA_BANCADA`, próxima a selar v394. A conferência não abre arquivo do Nós vivo. Recusas: sem a cadeia, com um byte mudado, contra outra Bancada, com o selo anterior errado.
- **Bateria da v394 contra o candidato real (`R35_P_`):** o `gerar_bateria_r3_4.py --versao v394` sobre um stand-in do Nós v394 (o um.py CANDIDATO d19, `972e81f22dd8cc68`, o instalado; selo sintético) e a bateria INTEIRA rodada contra uma Bancada pinada nele: 13 PASSA, 0 FALHA, T12/T13/T14 repinados para o v394 (linha de alpha 5584 medida); o T17 só roda no pós-selo.
- **Limite [DECLARADO]:** a lista confere a FORMA; não prova a inocuidade semântica do corpo (`liftCoreM getEnv`, `collectAxioms` e `IO.println` executam na compilação do Lean). Uma forma legítima nova numa versão futura (outro local, outra função) é recusada de forma visível até a lista ser estendida por ato consciente.

## 3. O Nós real no meio do rito: os controles migraram para o stand-in da custódia v393

O Nós real está em obra (um.py `972e81f22dd8cc68`, o v394, com o selo `bfddccfd153374dd` ainda o da v393; a pasta do Nós teve 1379 itens no topo no início e no fim da corrida, com 0 acrescentados e 0 removidos). A R3.4 lia o Nós real em ~20 controles (a família b1) e no `montar_sandbox`, o que falharia. Na R3.5 o "Nós real v393" é `nos_real/`, cópia de bytes de `cadeia_de_selo/v394/base_v393` conferida pelos sha256 que o recibo pre_selo real registra; `b1` pina o stand-in; `b1real` pina o caminho REAL (só para a guarda A2, que recusa antes de qualquer conteúdo do Nós importar); `nos_v394s`/`b1v394s` trazem o candidato real. Os 61 controles herdados que mudaram de formato (lista e motivos no JSON) mantêm a recusa ou o veredito esperado; mudam só uma asserção lateral em `RUN_1a` (`pina_o_nos_real` agora é falso: o stand-in não está no caminho real) e em dois controles do pino do T12 (o `.path` do pino do um.py também difere), três guardas A2 passam a `b1real`, e três da varredura de auditoria mudam de forma por causa da lista de permissão: o import da amostra, o CRLF/tab e a inversão de `palavras_dentro_de_nome` (um local fora da lista agora é recusado). O Nós real foi SÓ lido (lista e sha do um.py antes e depois); este script nunca grava nele.

## 4. (2) A fusão do `PINOS_BN_v394.json` [REAL, `evidencias/fusao_pinos_bn_r35.json`]

- Parti do arquivo VIVO: sha256 `d50e8fd0932d4501f5646c67078f1a1226a85f17e3845fd8bfa1eee251bbf07f` (a revisão leu `d50e8fd0`), conferido por script antes de escrever. **Fundido: sha256 `9e3cbebd439585be82b38a462ced4e1582777c0fd646c30bd8985446a3140e1f`** (9687 B, 23 chaves). Backup de bytes ao lado: `PINOS_BN_v394.json.bak_20261019_161737`. Escrita por temporário + `os.replace`, formato do vivo preservado (CRLF, indent 1).
- Ficam como estavam: criterios, candidato, esperados, pins_do_candidato (candidato `972e81f22dd8cc68`, esperados `44ec7c1d613a3c2e`). Entram: `esboco_R3_5`, `esboco_R3_4_do_recibo_pre_selo`, `gerador_bateria`, `driver_t12_t14`, `bateria` (a do pre_selo, v393), `bateria_base_R2`, `pino_um_py_da_bateria`, `cadeia_de_selos` (`0f96cebd7c2135c1`), `recibo_pre_selo` (`0d82d598229fd398`, com o pino do pino), `selo_anterior_v393`, `kernel_manifesto_anterior_v393` e `kernel_recibo` = o R3_4 (`c63e94f9969771c9`, com `modulos_de_auditoria`). O que saiu de uso fica ao lado em `*_substituido` / `*_original` / `nota_anterior` (esboço R3.3, bateria R2, ensaio da R3.3, recibo do kernel R3_2). NÃO copiei `PINOS_BN_v394.R3_4.json` (candidato `7abb7ba9` e esperados vencidos).

## 5. (3) O passo 10 re-derivado [REAL, `DIFF_PASSO10_R3_5.patch` sha16 `66b51fb3569fbee4`, reproduz bit a bit]

- Re-derivei, pela §7 do `RESULTADO_R3_4.md` com a R3.5, o `b3_prepara`, o passo 10 e o passo 10b do `v394/pos_rito/chain_pos_rito_v394.sh` e o helper `b3_recibo_v394.py`. Backups de bytes: `chain_pos_rito_v394.sh.bak_20261019_155613` e `b3_recibo_v394.py.bak_20261019_155613`. Chain: `2bac1a0087eef828` -> `a8c539624f82e6d1`; helper: `fabd6738a5404bd1` -> `ebfdbf725902a919`. Passos 0-9, 10a, 10c e 11-14 byte a byte como estavam. NÃO rodei `derivar_cadeia_v394.py`; NÃO toquei `textos_v394.py`, `registrar_mapa_v394.py`, `fechar_v394.py`. `sh -n` OK.
- O que o passo 10 faz agora: lê os pinos fundidos (13 chaves conferidas por sha); exige que o um.py do Nós seja o `candidato` pinado; usa o recibo do kernel R3_4 (não mais o R3_2); **gera a bateria da v394 por script** (`gerar_bateria_r3_4.py --versao v394`, depois do selo) e a pina ao lado (`bateria_pos_selo/PINOS_BATERIA_v394.json`; o 10 e o 10b usam a mesma); passa `--cadeia-de-selos` e o recibo pre_selo `0d82d598229fd398`; o helper exige que o recibo DECLARE o salto, com a cadeia pinada, `proxima_a_selar` v394, veredito `__SALTO_` e os pinos da bateria da v394 conferidos.
- **Ensaio a seco (nada gravado na Bancada nem na pasta v394 real; só `--modo ensaio`):** (a) stand-in do Nós v394: o chain gerou a bateria (sim), passou os pinos e o esboço, contra a produção real, parou como previsto em: `NOS_DIFERENTE_DO_PINADO` (`PARADA: o B(n) ENSAIO reprovou (rc=2): saida inteira em C:/t/vb11/passo10_standin/pk/pos_rito/b3_ensaio_out.txt`); (b) Nós real (no meio do rito): causa `SELO_DE_OUTRA_VERSAO: o selo do Nos diz 'v393', --versao v394`; `PARADA: gerar_bateria_r3_4.py recusou: o Nos nao e o candidato pinado em PINOS_BN, ou o selo nao pina o um.py (saida inteira em C:/t/vb11/passo10_real/pk/pos_rito/gerar_bateria_v394_out.txt)` (bateria gerada: nao). Manifesto e lista da produção iguais antes e depois nos dois. O que só o rito terminado decide: o selo e o manifesto do kernel reais da v394 (T17) e o `nos_pinado`.

## 6. Comandos exatos do passo 10 (a rodar DEPOIS do rito; `cd "C:/IALD/Central de Patentes/work/cadeia_de_selo/v394/pos_rito"`)

O passo 0 (guardas) roda sempre, qualquer que seja o `CHAIN_DE`: exige `RITO_RC=` no stdout do rito e que o um.py do disco seja o instalado e o candidato. Os passos abaixo são só do B(n); os demais (1 a 9, 11 a 14) seguem a ordem de sempre.

```
# 10 — ensaio pós-selo, SALTO v392 -> v394 (nada gravado na Bancada); gera e pina a bateria da v394 na primeira vez
CHAIN_DE=10 CHAIN_ATE=10 sh chain_pos_rito_v394.sh
# 10-bis-a — a parada do serviço da Bancada (porta 18777) é ATO DO OPERADOR com recibo (bancada_B3_servico/RECIBO_PARADA_v394.json); o chain só confere o recibo
CHAIN_DE=10a CHAIN_ATE=10a sh chain_pos_rito_v394.sh
# 10-bis — APLICAR (grava o manifesto B4 na Bancada de produção; backup de bytes e rollback no esboço); exige o evento c1 que nomeia a v394
B3_AUTORIZADO=sim EVENTO=<seq> EVENTO_HASH=<hash16 do retorno de iald.py anotar> CHAIN_DE=10b CHAIN_ATE=10b sh chain_pos_rito_v394.sh
# 10-ter — o religamento do serviço com recibo é ATO DO OPERADOR (bancada_B3_servico/RECIBO_RELIGAMENTO_v394.json); o chain só confere o recibo
CHAIN_DE=10c CHAIN_ATE=10c sh chain_pos_rito_v394.sh
```
O esboço que o passo 10 chama (valores lidos do `PINOS_BN` fundido; `<bateria...>` é a gerada no 10):
```
python -I -B -X utf8 "C:\IALD\Central de Patentes\work\bancada_vinculo_12out\R3_5\sincronizar_bancada.py" --bancada "C:\IALD\Bancada_Um" --producao --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" --versao v394 --fase pos_selo --modo ensaio \
  --bateria "<v394/bateria_pos_selo/BATERIA_VINCULO_v394.json>" --bateria-sha256 <sha lido de bateria_pos_selo/PINOS_BATERIA_v394.json> \
  --cadeia-de-selos "C:\IALD\Central de Patentes\work\bancada_vinculo_12out\R3_4\CADEIA_DE_SELOS_v394.json" --cadeia-de-selos-sha256 0f96cebd7c2135c17204153b733be4578b1c2a40fd94cb38f0984693e4194a4e \
  --recibo-pre-selo "C:\IALD\Central de Patentes\work\bancada_vinculo_12out\R3_4\recibo_pre_selo_v394\RECIBO_SINCRONIZACAO_v393_20261019_134158.json" --recibo-pre-selo-sha256 0d82d598229fd39881193f69843dfda17968c9170696647ab827e8643f26e878 --selo-anterior "C:\IALD\Central de Patentes\work\cadeia_de_selo\v394\base_v393\um_absoluto_selo.json" --kernel-manifesto-anterior "C:\IALD\Central de Patentes\work\cadeia_de_selo\v394\base_v393\tgl_kernel_proof_manifest.json" \
  --kernel-recibo "C:\IALD\Central de Patentes\work\bancada_vinculo_12out\R3_4\KERNEL_RECIBO_v394_R3_4.json" --kernel-recibo-sha256 c63e94f9969771c9a3410c66622032370012190ae09375ece6747f94535f2d1a --criterios "C:\IALD\Central de Patentes\work\cadeia_de_selo\v394\vinculo\CRITERIOS_v394.json" --criterios-sha256 a382796078d4c643e81082a63b8b75819c568d512bbb9eb7df2e54832db540df --saida "<v394/bancada_B3_ensaio_AAAAMMDD_HHMMSS>"
```
O 10b é o mesmo com `--modo aplicar --evento "$EVENTO" --evento-hash "$EVENTO_HASH"` e `--saida` numa pasta nova (`bancada_B3`, `bancada_B3_2`...). Resultado esperado do 10: `REPINADA_B4__SALTO_v392_v394__ENSAIO__NADA_GRAVADO_NA_BANCADA`; do 10b: `REPINADA_B4__SALTO_v392_v394__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO`.

## 7. Garantias [REAL]

- Produção (1212 arquivos, manifesto `6733b9a28c725244`) e Nós: só lidos; a lista da produção e o manifesto iguais no início e no fim. O livro de eventos só foi lido (1021 linhas no início, 1023 no fim; só cresce por outras frentes). Nenhum rito, instalação, conferidor, reversão, `ESPERADOS`, candidato, kernel ou Nós tocado; o serviço da Bancada não foi parado nem religado; o B(n) NÃO foi aplicado; nenhum `.bak_` apagado; processos só os meus.
- Escrevi só em `R3_5`, `C:/t/vb11` (apagado no fim) e, com backup de bytes, em `PINOS_BN_v394.json`, `chain_pos_rito_v394.sh` e `b3_recibo_v394.py` (v394).
- A palavra proibida da régua não aparece como palavra inteira em nenhum arquivo da R3_5 (`grep -r -i -w`, rc 1).

## 8. Resíduos

- Os da R3.4 e R3.3 seguem (a cadeia mostra consistência, não autenticidade; o adendo de pino do T12 espera a ratificação do Codex; o corpo do `run_cmd` não tem inocuidade semântica provada).
- O T17 e o `nos_pinado` do pós-selo só se decidem com o selo e o manifesto reais da v394; o ensaio a seco para antes (§5). Se o rito reconstruir o kernel, derivar de novo o recibo R3_4 (`derivar_recibo_kernel_r3_4.py`) e refazer o pino.
- O `PINOS_BN_v394.json` é vivo (outras sessões o editam): a fusão conferiu o sha antes de escrever e antes do `os.replace`; uma corrida mais curta que isso é residual.

## 9. Atos

**Gerência c1:** reauditar só a lista de permissão (`R35_M_`), os `R35_V_` e os `R35_P_`; conferir o `PINOS_BN` fundido (sha acima) e o chain (diff); depois do rito, rodar o passo 10 (comandos acima); registrar no mapa (`registro_mapa_F0.6_R3_5.json`, pronto e NÃO registrado) e no ACOM.
**Operador:** a parada do serviço (10-bis-a), o evento c1 que nomeia a v394 e a aplicação (10-bis), o religamento (10-ter), X19 e o aceite, como antes.
