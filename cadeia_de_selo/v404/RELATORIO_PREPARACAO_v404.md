# RELATÓRIO DA PREPARAÇÃO DA v404 — Jo 8,32 e a projeção transversal da Meia-Nat

Agente de preparação `claude-prep-v404` · 2026-10-28 20:33 · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: nada aqui foi revisado por terceiro.** Nada foi instalado; o rito NÃO foi rodado; o Nós, o `MEMORY.md` e o `MEMORY_2.md` não foram tocados.

## 1. Estado em uma frase

O candidato `3820476c83267f61` (39,313,509 B; base v403 `2ffe9edc7d7545bd`) está gerado, comparado (AST), ensaiado a seco (**TUDO PASSOU**), conferido (controle negativo + caminho positivo), com o B(n) pré-selo gerado e pinado (**JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA**, bateria **BATERIA_PASSA**) e os scripts do pós-rito (leitura, textos, fechar, mapa, serviço da Bancada) escritos e testados em harness (**TUDO PASSOU: o conferidor da v404 (16 itens C1-C16 e o round** / **TUDO PASSOU: a FILA DA MEMORIA funciona em copia (pausa ante**). **Falta, e é da gerência:** decidir o `MEMORY.md` (p00 reprova 1 de 104), revisar, instalar, rodar o rito.

## 2. O que foi preparado e passou (cada linha lida de um arquivo)

| etapa | resultado |
|---|---|
| kernel (sandbox `C:\t\k404c\final`) | build incremental + Audit rc 0, zero sorry; 14 bandeiras novas (projecao 13, jo8v32 1); escada 9684 → 9698; recibo `KERNEL_RECIBO_v404.json` (contrato R3_2) |
| as duas pedras | `ProjecaoTransversalDaMeiaNat` `1e53257273395c7c`, `Jo8v32` `18df8f686e524845` (conferidas com o pino da ordem da gerência) |
| candidato | 33 patches determinísticos; gerado duas vezes (antes e depois do `refazer`): sha16 3820476c83267f61 — refazer terminou NAO terminou limpo (ver refazer_out_v404.txt) |
| AST v403 × v404 | 1097 nós, 1077 iguais, 20 mudados (todos explicados), 0 removidos, 17 novos; as 5 funções do gate/neutrino/ramo B intactas |
| ensaio a seco | TUDO PASSOU; guardas estáticas da Bancada: GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA__DEFEITO_REAL_DA_V399_REPRODUZIDO__CONTROLES |
| conferidor | controle negativo (Nós v403): `tudo_bate` = False; positivo (Nós falso do ensaio): `tudo_bate` = True |
| citações | TODAS CONFEREM |
| instalar / reverter / rito (estático) | zero falhas; sintaxe ok |
| B(n) pré-selo | recibo `PINO_RECIBO_PRE_SELO_v404.json` `b0432d85d7b2cf48`; produção intacta = True; conferência pelo esboço R3.5 23/23 e 5/5 controles |
| B(n) pós-selo (scripts) | `bancada_B3_servico\` derivado (5 arquivos; conferidor estático 27/27; controle negativo: toda mutação foi pega = True); `b3_recibo_v404.py` e `chain_pos_rito_v404.sh` com B12 → B13 |
| pós-rito: leitura | `leitura_v404.py` adaptada: zero problemas contra o Nós emulado; 359 controles negativos reprovam como esperado |
| pós-rito: textos | `textos_v404_novo.pysnip` + `montar_textos_v404.py` → `textos_v404.py`; todas as funções renderizam, guarda P18 limpa, regra do 4,44 conferida; parágrafo novo (README/site) com 61 controles negativos; nota ao lado do parágrafo da v403; `cita_so_o_que_existe` sem pendência |
| pós-rito: harness dos textos | PASSOU (sem --nao-exigir-refazer) |
| pós-rito: harness do fechar | PASSOU (sem --nao-exigir-refazer); 26 controles negativos do fechar |
| p00 | 104/104 checagens OK |

## 3. O que NÃO passou ou fica AGUARDA

- **p00 reprova 0 checagem(ns) (real, não é defeito de script):** nenhuma. O `MEMORY.md` (índice) está no limite de linhas/bytes; a superfície do pós-rito **não compacta** e recusa com rc 3 (isto foi exercitado no harness: cenário (a) recusa, (b) com folga grava, (c) no limite recusa). Quem decide o que sai do índice é a gerência.
- **Aguarda o rito / a instalação:** `ESPERADOS`/`PINOS_BN` já pinados; o `conferir_rito_v404.py` só dá `TUDO BATE` depois do rito (controle negativo e positivo falso já exercitados); `leitura`/`fechar`/`registrar_mapa` reais só rodam depois do rito.
- **Aguarda a palavra do operador:** o aplicar do B(n) (parada e religamento do serviço da Bancada; `V404_AUTORIZACAO_OPERADOR` — o texto **não pode citar o nome do script do serviço**, porque o recibo de parada conta processos cuja linha de comando o cita).
- **O post do X** (`pos_rito\gerar_x_custodia_v404.py`) é rascunho que só nasce da v404 selada (recusa o Nós v403); a prévia `CUSTODIA_v404_PREVIA_do_Nos_emulado_NAO_PUBLICAR.txt` é do Nós emulado. Publicar é ato da gerência/Codex.
- **Não feito (fora do escopo da preparação):** instalar; rodar o rito; revisão independente; custódia; commit/push; registro da rota SELADA no Mapa (o `registrar_mapa_v404.py` só monta; a rota de preparação foi registrada: seq 1513 (ROTA), 1515 (ANOTACAO), 1516 (ANOTACAO)).

## 4. Achados e lições (para a próxima subida)

1. **Contagens de derivador medidas na fonte** (bateria pré-selo, serviço da Bancada): as presumidas falharam em versões anteriores; aqui o derivador as MEDE e aborta se casar diferente.
2. **O bump mecânico não conhece a semântica:** `B11` não sobe sozinho (a Bancada pina B12, `B12-v403-20261028-R1`; o B(n) da v404 grava B13) e os nomes nascidos no `um.py` base ficam protegidos do bump — por isso `caminho_v403`, `vida_v403`, `bandeiras_do_gate_v403` etc. ficaram, na semente da leitura/textos, com o papel de «novos» e tiveram de ser reescritos à mão como «recriados» (e os novos `projecao_transversal_v404`, `jo8v32_v404`, `f2b_errata_v404` entram como funções).
3. **Heredoc do Bash colapsa barras invertidas** (`\\n` virava quebra de linha dentro de string): os scripts com barra foram escritos por arquivo; o conserto foi reconstruir com `chr(92)`.
4. **`-I` esconde o numpy do usuário:** o conferidor positivo e o teste do Nós falso rodam com `python -B -X utf8` (sem `-I`), como na v403.
5. **O sandbox curto `C:/t/vb21`** precisa NÃO existir quando a bateria pré-selo roda (ela recusa com rc 9 se existir). `guardas_estaticas_bancada_v404.py` (chamada pelo ensaio a seco) e o controle negativo do conferidor do serviço criam ali uma pasta VAZIA; removi com `rmdir` (só funciona se vazia) e ela volta a existir depois de cada ensaio a seco: se for rodar a bateria de novo, `rmdir C:/t/vb21` antes.
6. **A errata de F2b é decisão da gerência lida a partir das falas** [DECLARADO]: o operador ratificou a leitura («calibrar Não significa validar»), não nomeou a retirada. Está escrito assim em todos os textos.

## 5. Para a gerência — ordem sugerida

1. Ler `PLANO_v404.md` e este relatório; revisar `delta_v404.py`, `registros_v404.py`, `runtime_v404.py` e `pos_rito\textos_v404_novo.pysnip` (o conteúdo novo); pedir a revisão independente (não afirmada aqui).
2. Decidir o `MEMORY.md` (p00) e rodar `python -I -B -X utf8 p00_precondicoes_v404.py` até `TODAS PASSARAM`.
3. `instalar_v404.py` → `rito_v404.sh` (compila a frio; ~1,5 h) → `pos_rito\chain_pos_rito_v404.sh` (passos 0 a 14; o 10a/10c param em AGUARDA_OPERADOR).
4. Depois do fechar: `registrar_mapa_v404.py` (só monta; a gerência registra), `gerar_x_custodia_v404.py`, custódia G1.

## 6. Artefatos e hashes (lidos agora)

Pedras:

| módulo | sha16 | bandeiras |
|---|---|---|
| `TGLExt/ProjecaoTransversalDaMeiaNat.lean` | `1e53257273395c7c` | 13 |
| `TGLExt/Jo8v32.lean` | `18df8f686e524845` | 1 |

| arquivo | bytes | sha16 |
|---|---|---|
| `um_v404_candidato.py` | 39,313,509 | `3820476c83267f61` |
| `CANDIDATO_v404.json` | 30,532 | `699642c638700bf0` |
| `ESPERADOS_v404.json` | 746,582 | `360ea756e0fb250f` |
| `ensaio_a_seco_v404.json` | 205,948 | `f48c156fef9379f9` |
| `PINOS_BN_v404.json` | 4,862 | `35dcebfca56eecdd` |
| `PINO_RECIBO_PRE_SELO_v404.json` | 6,215 | `b0432d85d7b2cf48` |
| `PROVA_PRODUCAO_INTACTA_v404_pre_selo.json` | 9,923 | `0a337588f4b5c152` |
| `PRECONDICOES_v404.json` | 17,975 | `a427d65080009251` |
| `PLANO_v404.md` | 8,138 | `01f2245d4cc7d062` |
| `delta_v404.py` | 23,022 | `58934a25b0bfaf2c` |
| `registros_v404.py` | 46,554 | `08fd2987bbb2956f` |
| `runtime_v404.py` | 28,244 | `234b935fa8f0a170` |
| `gerar_candidato_v404.py` | 50,589 | `242777a285fce166` |
| `gerar_esperados_v404.py` | 21,370 | `0ed1f2bd477c67aa` |
| `artigo_pt_v404.pysnip` | 11,397 | `32b06b4043b0d0cc` |
| `artigo_en_v404.pysnip` | 12,198 | `7401b0e9cb2321c0` |
| `comparar_v403_v404.py` | 7,719 | `24cabd321d31ad70` |
| `instalar_v404.py` | 9,108 | `63a390042ac36bb8` |
| `rito_v404.sh` | 24,363 | `71ef80d552e0884a` |
| `conferir_rito_v404.py` | 62,439 | `3b18617bb3ca2436` |
| `p00_precondicoes_v404.py` | 25,053 | `944d73a15e76ad8d` |
| `bancada_B3_servico/derivar_servico_v404.py` | 6,019 | `e2fd3cb49afb0595` |
| `bateria_pre_selo/derivar_pre_selo_v404.py` | 7,458 | `6376ff5aed8db022` |
| `pos_rito/textos_v404_novo.pysnip` | 107,130 | `97e57bac3f645aff` |
| `pos_rito/montar_textos_v404.py` | 6,351 | `40035fdf230c8a85` |
| `pos_rito/textos_v404.py` | 131,490 | `190f1d4d11e80621` |
| `pos_rito/leitura_v404.py` | 98,378 | `e4d560b12d80f06d` |
| `pos_rito/fechar_v404.py` | 23,751 | `bb315db58aa37966` |
| `pos_rito/registrar_mapa_v404.py` | 45,736 | `79c58a868ef32469` |
| `pos_rito/harness_textos_ensaio_v404.py` | 140,954 | `ad8337117de18fe2` |
| `pos_rito/harness_fechar_sandbox_v404.py` | 101,696 | `bfc7f8ace371a4b0` |
| `pos_rito/chain_pos_rito_v404.sh` | 38,100 | `6cc23130572bcbdf` |
| `pos_rito/gerar_x_custodia_v404.py` | 4,828 | `41100b8477b09896` |
| `kernel/KERNEL_RECIBO_v404.json` | 161,818 | `d5311a8455862c99` |
