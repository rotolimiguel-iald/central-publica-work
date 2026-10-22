VINCULO R3.4 — 19/10

# Resultado da R3.4 do esboço `sincronizar_bancada.py` (F0.6, gerência c1)

Construtor: subagente da gerência c1 (Sonnet). Base: a R3.3 em `../R3_3/`, com o esboço conferido em `71507fd02b70b115` antes de tocar [REAL]. Todo hash e todo número abaixo foi lido dos arquivos por `_construcao/gerar_resultado_r3_4.py` (nenhum digitado); os hashes dos entregáveis estão em `PINOS_R3_4.json`. Esboço R3.4: sha16 `12d504a1114f9f9c`.

Ordem do operador (12/10): «a bateria nossa de teste precisa ficar sempre vinculada ao um.py, de modo que nossos avanços no programa também implique em aperfeiçoamento da bancada para não ficar para trás».

Problema medido [DECLARADO no pedido da gerência; reproduzido aqui nos controles `R34_S_atrasada_sem_cadeia_recusa` e `R34_P_bateria_R2_T12_contra_o_nos_atual_falha`]: a Bancada de produção pina a v392 (`B3-v392-20261013-R1`, um.py `b590c0aa80055e2a`); o Nós tem a v393 (um.py `18be2ddb06c60f90`); o elo da v393 nunca rodou. A R3.3 só aceita `JA_SINCRONIZADA` no pre_selo; a bateria R2 pina o um.py v391 (T12/T13/T14 falham contra o Nós atual); três módulos de auditoria do kernel v394 não têm declarações (a N1k recusa).

## 1. Veredito

**`TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO`: 547/547 em 876 s**, rodados com `python -I -B -X utf8` no sandbox curto `C:/t/vb10` [REAL, `CONTROLES_NEGATIVOS_R3_4.json`, sha16 `6d54b84e52c6649f`]:
- os 401 controles da R3.3 presentes 401/401, com os mesmos nomes (dentro deles, R3.2 399/399, R3.1 337/337, R3 235/235), e os runs 1a, 1b, 2 e 2bis refeitos e passando; 21 controles herdados mudaram de formato (listados com o motivo em `controles_da_R3_3_que_mudaram_de_formato`; 20 porque a família b1 agora pina o Nós REAL v393 e não a v391, e o run 1b porque a cópia v391 do Nós vem da custódia e a bateria por versão é gerada para ela; a recusa ou o veredito esperado não mudou em nenhum);
- 146 controles novos: 69 do salto (`R34_S_`), 33 da bateria por versão (`R34_P_`), 44 dos módulos de auditoria (`R34_M_`); por nível, 84 unitários, 55 em subprocesso e 7 em processo (produção-decoy trocada só na memória do processo);
- cada item pedido tem controle novo que recusa: sem cadeia verificável o salto é recusado (`R34_S_atrasada_sem_cadeia_recusa` e 30 variantes de cadeia adulterada, mal formada ou fora de lugar, `R34_S_cadeia_*`); bateria com o pino velho recusa antes de qualquer teste (`R34_P_pino_velho_bateria_v391_contra_o_nos_v393_recusa`); módulo sem declarações fora da lista é recusado pela N1k (`R34_M_pedra_comum_sem_declaracoes_fora_da_lista_recusada`) e fonte com comando fora da gramática de auditoria é recusada (19 controles `R34_M_fonte_*`).

## 2. O que mudou no esboço [REAL, `DIFF_R3_3_R3_4.patch` sha16 `61481bbef09b7242`, 7 arquivos, +2037 -61 linhas, reproduz bit a bit com `core.autocrlf=false`]

**S — salto (recuperação de atraso).**
- Em `--fase pre_selo`, se a Bancada pina N-k e o Nós tem N-1, o esboço exige `--cadeia-de-selos` e `--cadeia-de-selos-sha256` (lido de vNNN_pins) e confere a cadeia POR HASH: contrato `CADEIA_DE_SELOS_R3_4` de chaves fechadas, sem chave duplicada, um elo por versão, consecutivas; cada elo traz cópias de bytes pinadas do um.py, do selo e do manifesto do kernel; o selo do elo pina o um.py e o manifesto dele e `UM_VERSION` confere; cada elo menos o último traz o registro do instalador (`APLICADO_AO_CANONICO`) e os `.bak_` de bytes, que têm de ser, byte a byte, o um.py e o selo do elo; o INÍCIO da cadeia é a Bancada (versão, um.py, selo, manifesto do kernel) e o FIM é o Nós vivo (pre_selo) ou o recibo pre_selo pinado (pos_selo). Sem cadeia verificável: recusa (`BANCADA_ATRASADA_SEM_CADEIA_DE_SELOS`, `CADEIA_DE_SELOS_*`, `BANCADA_A_FRENTE_DO_NOS`).
- Medido [REAL, `R34_S_o_selo_nao_pina_o_selo_anterior_medido`]: o selo NÃO pina o selo anterior. Por isso a ligação entre elos é o registro do instalador mais as cópias de bytes dos backups, e não «cada selo pina o anterior».
- O recibo declara o salto (de, até, versões puladas, próxima a selar, cadeia por sha) e o veredito `REPINADA_B<n>__SALTO_<de>_<ate>__ENSAIO...`; o pos_selo aceita esse recibo no lugar de `JA_SINCRONIZADA` (conferido com a cadeia e com o selo e o manifesto do kernel do FIM da cadeia, `--selo-anterior` e `--kernel-manifesto-anterior`) e grava `sincronizacao.salto` no manifesto novo; o evento c1 tem de nomear a versão.
- `gerar_cadeia_de_selos.py` gera a cadeia por script a partir das pastas `vNNN/base_vJ` e do registro do instalador que confere (registros de tentativas revertidas ficam de fora); nada é digitado.

**P — bateria por versão.**
- `gerar_bateria_r3_4.py` (determinístico, sem relógio) regenera a bateria a cada versão a partir da base R2 e dos pinos da cadeia (`PINOS_BN` da versão instalada: `candidato.sha256` == um.py do Nós == o que o selo pina). A bateria traz `pinos_da_versao` {versão, um.py sha256 e bytes, selo sha256}, e os testes que pinam o um.py trazem `pina_o_um_py: true`.
- O esboço confere os pinos contra o Nós que leu ANTES de qualquer teste (`BATERIA_COM_PINO_VELHO`, `BATERIA_SEM_PINOS_DA_VERSAO`, `BATERIA_PINOS_DA_VERSAO_INVALIDOS`, `BATERIA_TESTE_PINA_O_UM_PY_NAO_BOOLEANO`) e entrega o um.py medido ao teste pelos marcadores `{um_py_path}`, `{um_py_sha256}`, `{um_py_bytes}`. Bateria sem teste marcado (a R2) segue aceita e o recibo diz que não tem pinos da versão.
- O driver `bateria_r3_4/t12_t14_atrator_r3_4.py` repina SÓ a entrada do um.py do pré-registro congelado da F1.ATRATOR, NA CÓPIA do replay (e o sha do pré-registro no `RUN_MANIFEST_R3` da cópia), roda os runners congelados (cópias byte a byte) e compara com os resultados arquivados trocando só os campos que dependem do um.py (3 no T12, 4 no T13) por valores independentes (sha da cópia do pré-registro, sha do um.py, linha do alpha no um.py). Se o pino da cadeia não é o um.py medido, o teste FALHA sem rodar runner. O replay lê o um.py como texto; nenhum comando da bateria o executa.

**M — módulos de auditoria.**
- Contrato `KERNEL_RECIBO_R3_4` (a R3_2 segue admitida) com `modulos_de_auditoria`: um módulo sem declarações só passa se estiver na lista do recibo E a fonte, varrida por script (`auditar_fonte_de_auditoria`), tiver só comandos de auditoria (`import`, `open ... in`, `#print axioms`, `run_cmd`) de gramática fechada. Lista vazia, repetida, com item que não é pedra do recibo ou com pedra que traz declarações é recusada; fonte com `theorem`, `def`, `axiom`, `sorry`, `addDecl`, escrita de arquivo, processo, comentário de bloco, caractere invisível ou comando desconhecido é recusada; a N1k vale para todo o resto.
- `derivar_recibo_kernel_r3_4.py` deriva o recibo R3_4 do R3_2 (só `contrato` e `modulos_de_auditoria` mudam; a fonte de cada módulo é lida da árvore do recibo e passa pela varredura): `KERNEL_RECIBO_v394_R3_4.json` (sha16 `c63e94f9969771c9`, 190 pedras, 3 módulos de auditoria: NetworkProofAuditR3, R7 e R8) é PROPOSTA; o recibo original não foi tocado.

## 3. O recibo pre_selo REAL da v394 (ensaio, nada gravado): a bateria PASSA

- Arquivo `recibo_pre_selo_v394/RECIBO_SINCRONIZACAO_v393_20261019_134158.json` (sha16 `0d82d598229fd398`, 64970 B); pino `PINO_RECIBO_PRE_SELO_v394_R3_4.json` (traz o comando exato, o esboço, a bateria e a cadeia por sha). Contra a Bancada de PRODUÇÃO (só leitura) e o Nós real v393: `--modo ensaio --fase pre_selo --versao v393`, rc 0, veredito `REPINADA_B4__SALTO_v392_v393__ENSAIO__NADA_GRAVADO_NA_BANCADA`.
- Bateria: **`BATERIA_PASSA`**, 13 PASSA, 0 FALHA, 1 NAO_EXECUTADO de 14 testes (o NAO_EXECUTADO é o T17, que só roda no pos_selo, lido do recibo do kernel). T12/T13/T14 (replay do F1.ATRATOR repinado para o um.py v393): PASSA / PASSA / PASSA.
- Salto declarado: de `v392` (um.py `b590c0aa80055e2a`, `B3-v392-20261013-R1`) até `v393` (um.py `18be2ddb06c60f90`); versões puladas `v393` (a Bancada nunca foi pinada nela); próxima a selar `v394`; cadeia sha16 `0f96cebd7c2135c1` com 2 elos (v392, v393) e 1 ligação (registro do instalador sha16 `4e8c837b8b4362ac`).
- Pinos da versão conferidos contra o Nós lido: v393, um.py `18be2ddb06c60f90`, selo `bfddccfd153374dd`; teste que pina o um.py: `T12_T13_T14_ATRATOR`. Adendo de pino do T12 declarado no recibo: o pré-registro congelado pinava o um.py v391 (`8e7b9927ceae64b8`); o replay o repinou, na cópia, para o v393 (`18be2ddb06c60f90`).
- Aceito pelo caminho do B(n) pos_selo: `conferir_recibo_pre_selo` do esboço R3.4 contra a produção real em leitura (`evidencias/VERIFICACAO_RECIBO_PRE_SELO_REAL.json`, rc 0, `aceito: true`; `utilizavel_como_recibo_pre_selo_do_B_n: true`). O ensaio de 19/10 da R3.3 era `false` (BATERIA_FALHOU e versão alvo diferente da pinada).
- Pinado numa CÓPIA de PINOS_BN: `PINOS_BN_v394.R3_4.json` (sha16 `c4bab7414aae3054`): esboço R3.4, bateria v393, pino do um.py, driver, cadeia, recibo pre_selo e recibo do kernel R3_4 proposto, com as entradas substituídas (esboço R3.3, bateria R2, ensaio da R3.3) guardadas nas chaves `esboco_R3_3_substituido`, `bateria_R2_substituida` e `recibo_pre_selo_ensaio_R3_3_substituido`. As chaves originais (criterios, kernel_recibo, candidato, esperados, pins_do_candidato) estão iguais às do `PINOS_BN_v394.json` vivo (sha16 `e9c470f14a548317`), que NÃO foi tocado; a gerência copia.

## 4. Garantias [REAL]

- Produção e Nós: só lidos. A lista da produção (1212 arquivos) e o manifesto (sha16 `6733b9a28c725244`) iguais no início e no fim; o topo do Nós e os arquivos-chave (um.py, selo, core, manifesto do kernel, pilar) iguais em sha256 e mtime; as pastas `base_vNNN` iguais (`_construcao/baseline_antes.json` x `baseline_final.json`, pelo script `medir_baseline.py`). O livro de eventos só foi lido: 1012 linhas no início e 1021 no fim; as linhas iniciais ficaram idênticas (o sha256 do prefixo confere) e os 9 elos novos (seq 1013 a 1021; tipos REVISAO_CANDIDATA_AUTORIZADA, avancar) são todos de codex-gerente-tgl, outra frente; nenhum é `SINCRONIZACAO_BANCADA`.
- A pasta da cadeia v394 não foi tocada por mim; ela é VIVA (outra sessão a edita: 1851 arquivos no início, 9186 no fim; 5898 arquivos mudados já medidos no pino do recibo, com nomes como `.bak_..._c1`). Por isso os controles M de dado real usam um SNAPSHOT pinado do recibo do kernel (`evidencias/KERNEL_RECIBO_v394_SNAPSHOT_R3_2.json`; igual ao vivo no fecho: sim) e das 3 fontes de auditoria (`evidencias/fontes_reais_v394/`).
- `C:/t/vb10`: 5 junções criadas e desfeitas com `os.rmdir` no link, 0 restantes; apagado no fim (nenhuma junção restava; lista da produção igual antes e depois). Sem HTTP, sem MCP, sem serviço real; processos só os meus; sem `init`/`transition` no ACOM; quadro, mapa, memória, túnel, site e git intocados (o mapa só foi LIDO, com `rotas.py ver`).
- A palavra proibida da régua não aparece como palavra inteira em nenhum arquivo da R3_4 (`grep -r -i -w`, rc 1); a única ocorrência como SUBSTRING está num comentário do esboço herdado da R3.3 (nome de uma chave do manifesto do kernel), que não afirma nada.

## 5. Resíduos que seguem declarados

- A cadeia mostra CONSISTÊNCIA de cópias de bytes e de registros do instalador, não autenticidade: o selo não pina o selo anterior (medido) e não há assinatura. Forjar exige forjar o arquivo da cadeia, as cópias e o registro E o sha da cadeia que a gerência pina em vNNN_pins; as pontas (Bancada e Nós vivos, ou o recibo pinado) são conferidas contra o disco. Limite [DECLARADO].
- O repino do pré-registro da F1.ATRATOR na cópia é um ADENDO ao pré-registro congelado (o pré-registro é do teste, fixado por hash antes); fica declarado no recibo e precisa ser ratificado pelo dono da F1.ATRATOR (Codex) e registrado. O replay mostra que os runners congelados reproduzem os resultados arquivados com o um.py da versão; não mostra que o número vale para o novo um.py além do que o runner lê dele (sha, linha do alpha).
- Módulo de auditoria: a gramática do topo e a lista fechada de palavras do corpo do `run_cmd` são conferidas por script; a inocuidade semântica do corpo (executado na compilação do Lean) não é demonstrada. O recibo do kernel R3_4 é PROPOSTA derivada do R3_2 de 190 pedras; a decisão de qual pinar é da gerência; o kernel não foi reconstruído por mim.
- O B(n) pos_selo REAL da v394 NÃO foi rodado: falta o selo da v394 (o Nós ainda é v393), o recibo do kernel pinado, a bateria da v394 (gerada depois do selo) e o `CRITERIOS_v394.json`. O que foi exercitado: o pos_selo completo do salto na produção-decoy em processo (`R34_S_decoy_*`, 7 controles) e a conferência do recibo real contra a produção real em leitura.
- O T17 não roda no pre_selo; o recibo diz NAO_EXECUTADO e `BATERIA_PASSA` é o veredito da bateria nessa fase.
- Os resíduos da §5 da R3.3 seguem (site do sistema sob `-I`; código hostil antes da guarda; 2ª gravação alheia; selo v391 na custódia [OPEN]; tokens; kernel real, links e corrida em `caminho_canonico`, autenticação do evento e rota do sorry com aspas no `um.py` não medidos).
- Dependência de dado vivo: o `PINOS_BN_v394.json` e o recibo do kernel da v394 são editados por outra sessão; a cópia e o snapshot valem pelo estado lido; se o kernel for reconstruído, derivar de novo o recibo R3_4 (`derivar_recibo_kernel_r3_4.py`) e refazer o pino.

## 6. Comando do pre_selo real (reproduz o recibo; ensaio, só leitura)

```
python -I -B -X utf8 "C:\IALD\Central de Patentes\work\bancada_vinculo_12out\R3_4\sincronizar_bancada.py" --bancada "C:\IALD\Bancada_Um" --producao --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" --versao v393 --fase pre_selo --modo ensaio --bateria "C:\IALD\Central de Patentes\work\bancada_vinculo_12out\R3_4\BATERIA_VINCULO_v393.json" --bateria-sha256 e47ce2e944e487adde3a29d2c7f16a5bf5b08c51084d52708785f13ff85455b9 --cadeia-de-selos "C:\IALD\Central de Patentes\work\bancada_vinculo_12out\R3_4\CADEIA_DE_SELOS_v394.json" --cadeia-de-selos-sha256 0f96cebd7c2135c17204153b733be4578b1c2a40fd94cb38f0984693e4194a4e --saida "C:\t\vb10\real_pre_selo_v394"
```

Para reproduzir, troque `--saida` por uma pasta NOVA sob `C:/t/vb*` (o `vb10` foi apagado; a cópia do recibo está em `recibo_pre_selo_v394/`). O ensaio não grava na Bancada nem no Nós.

## 7. Comandos exatos do B(n) pos_selo da v394 com salto

Sequência depois do selo da v394 (o Nós passa a ter a v394). Cada `<...>` é um arquivo que ainda não existe e cujo sha256 a gerência lê do disco e pina em `v394_pins`; nenhum hash vai digitado. O recibo pre_selo e a cadeia são os já pinados (§3). O `--selo-anterior` e o `--kernel-manifesto-anterior` são as cópias da v393 em `work/cadeia_de_selo/v394/base_v393/` (no salto, o selo anterior é o do FIM da cadeia).

1. Regenerar a bateria da v394 por script (nunca à mão):
```
python -I -B -X utf8 gerar_bateria_r3_4.py --base <R2/BATERIA_VINCULO.json> --versao v394 --nos <dir do Nós> --driver bateria_r3_4/t12_t14_atrator_r3_4.py --pinos-bn <cadeia_de_selo/v394/PINOS_BN_v394.json> --pino-saida <bateria_r3_4/PINO_UM_PY_v394.json> --saida <BATERIA_VINCULO_v394.json>
```
2. Ensaio do pos_selo (mesmos argumentos do passo 3, com `--modo ensaio` e sem `--evento`/`--evento-hash`), para ver `REPINADA_B4__SALTO_v392_v394__ENSAIO...` e a bateria da v394 PASSAR.
3. Aplicar (ato do operador, com o evento c1 `SINCRONIZACAO_BANCADA` que nomeia a v394):
```
python -I -B -X utf8 sincronizar_bancada.py --bancada <C:/IALD/Bancada_Um> --producao --nos <dir do Nós> --versao v394 --fase pos_selo --modo aplicar --bateria <BATERIA_VINCULO_v394.json> --bateria-sha256 <sha lido> --cadeia-de-selos <CADEIA_DE_SELOS_v394.json> --cadeia-de-selos-sha256 <sha lido> --recibo-pre-selo <recibo_pre_selo_v394/RECIBO_SINCRONIZACAO_v393_20261019_134158.json> --recibo-pre-selo-sha256 <sha lido> --selo-anterior <cadeia_de_selo/v394/base_v393/um_absoluto_selo.json> --kernel-manifesto-anterior <cadeia_de_selo/v394/base_v393/tgl_kernel_proof_manifest.json> --kernel-recibo <KERNEL_RECIBO_v394_R3_4.json> --kernel-recibo-sha256 <sha lido> --criterios <CRITERIOS_v394.json> --criterios-sha256 <sha lido> --evento <seq do evento c1> --evento-hash <hash16 do elo> --saida <pasta NOVA sob work/cadeia_de_selo/v394 (raiz de saída admitida para a v394)>
```
Resultado esperado pelo desenho: `REPINADA_B4__SALTO_v392_v394__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO` (salto de v392 até v394, versão pulada v393; o reinício do serviço com o recibo é ato à parte). O mesmo desenho foi exercitado na produção-decoy (`R34_S_decoy_salto_aplica_na_producao_decoy`); na produção real ainda não.

## 8. Atos

**Gerência c1:** reauditar só as partes novas (S, P, M); pinar em `v394_pins` o esboço R3.4, a bateria v393, o pino do um.py, o driver, a cadeia e o recibo pre_selo (`PINOS_BN_v394.R3_4.json` é a cópia pronta para fusão); decidir o recibo do kernel R3_4 (proposta) e o `CRITERIOS_v394.json`; pedir ao Codex a ratificação do adendo de pino do T12; registrar no mapa (`registro_mapa_F0.6_R3_4.json`, pronto e NÃO registrado) e no ACOM.
**Operador:** X19, o B(n) da v394 (aplicar, com o evento c1), 10-bis-a e 10-ter, como na R3.3.
