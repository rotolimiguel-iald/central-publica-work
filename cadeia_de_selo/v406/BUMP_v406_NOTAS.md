# BUMP v406 (cópia + subida de rótulo a partir de `v405\`): notas do executor mecânico

Data: 02/11/2026 (executor mecânico a serviço da gerência c1). Resultado por arquivo: `BUMP_v406_RESULTADO.json`; diffs: `bump\<nome>.diff`; gerador (reproduzível): `_bump_copia_v406.py`.
Estatuto: tudo aqui é [REAL] medido ao rodar, **exceto** o que está marcado [A ADAPTAR] (conteúdo que continua o da v405 e que só a gerência pode decidir) e o deployment `B14-v405-20261102-R1` (lido de `v405\bancada_B3_servico\RECIBO_RELIGAMENTO_v405.json`, campo `identidade.deployment_id`). Nada foi executado; nada fora de PK6 foi tocado (`v405\`, Nós, `k405c`, `k406c`, memória: intactos; conferido por `find -newermt`).

## 1. O que foi feito, em números

- **41 scripts** gravados em PK6 (29 da lista pedida + 12 extras que os scripts da cadeia chamam: ver 2.8). **1259 linhas alteradas** no total, **33 comentários de uma linha** `# [A ADAPTAR v406] ...` no topo (um por arquivo cujo corpo ainda é da v405). **52 diffs** em `bump\` (41 de cópia e 11 contra os derivados do motor).
- **Prova de que só mudam rótulos** (feita duas vezes, por dois códigos diferentes: o do gerador e um conferidor separado que reabre molde e cópia do disco): mesma contagem de linhas (descontado o cabeçalho), toda linha alterada contém `404`/`405`/`B13`/`B14` e, normalizando os dois lados (403..406 -> `#`, B13..B15 -> `@`, datas do deployment), as duas linhas ficam IGUAIS; **1259 linhas alteradas, 0 fora de rótulo**. sha16 de molde e cópia relidos do disco conferem com o JSON. Sintaxe: `ast.parse` / `sh -n` **41/41 ok**.
- Tokens mudados: `404->405` **849**, `405->406` **1570**, `B13->B14`/`B14->B15` (palavra solta) **9**, deployment `B13-v404-20261028-R1 -> B14-v405-20261102-R1` **2** (b3_recibo e derivar_pre_selo). Palavras com 404/405 **preservadas** de propósito: **676** ocorrências, **81** palavras distintas (lista por arquivo no JSON, campo `palavras_com_404_405_preservadas_lista`).
- Os **24 derivados pelo motor e os 44 itens do relatório do executor anterior estão intactos** (sha16 relido de cada um == o do `DERIVACAO_v406_RESULTADO.json`: 44/44). Não sobrescrevi nenhum; comparei a minha cópia em memória com cada derivado (seção 4).
- Rodadas: a 1ª gravou os 41 destinos; as seguintes (numeração de linhas do cabeçalho, seções de achados, 3 classes novas de [A ADAPTAR]) reescreveram 8 destinos com **backup de bytes** (`<nome>.bak_<ts>`) e o JSON de resultado (`BUMP_v406_RESULTADO.json.bak_*`). Os `.bak_*` e `bump\` ficam; nada foi apagado.

## 2. Decisões minhas (cada uma dita para a gerência desfazer se discordar)

1. **Mapa**: usei só a função `bump()` do `derivar_v406_motor.py` (a mesma que gerou os 24 derivados; **nenhuma regra de contagem exata**, nenhum texto reescrito). Ela sobe `404->405` e `405->406` numa passada só, também `k405c->k406c`, `h405->h406`, `base_v404->base_v405`, nomes de arquivo/módulo, e **preserva** os identificadores que **nasceram no `um.py` v405** (chaves do core `registros_v405`, `cunhagens_v405`; funções `ponte_da_massa_v405`, `_v405_rodar_specs`...; constantes `_V405_SPECS`...; etiquetas de stdout `[v405]`/`[v404]`) e hex longo. Isto **desvia da letra** de «TODAS as ocorrências» de propósito: trocá-los apontaria para nomes que não existem no `um.py` v406 (continuam existindo, vêm da base). Na dúvida, não mudei e anotei: a lista inteira das preservadas está no JSON.
2. **Defeito do motor corrigido nas minhas cópias**: o motor preserva por coincidência o nome de **módulo da cadeia** quando ele também é identificador do `um.py` (`import runtime_v405 as RT` em `gerar_candidato_v406.py` e `guarda_frases_v406.py` ficaria importando o módulo velho). Nas cópias, `import X`/`from X import` de módulo que existe como `v405\X.py` sobe (2 imports). O mesmo defeito está nos derivados (seção 4).
3. **B(n)**: `B13->B14` e `B14->B15` só como palavra solta (9 casos; nenhum inteiro de B(n) está digitado: o `n` é lido do recibo). `REPINADA_B13__` (palavra com sublinhado) em `diff_e_pinos_v406.py` l.44 **não mudei** (narrativa herdada; no texto da v405 já estava defasada).
4. **Variável `V14`** («caminho da cadeia anterior») em `conferir_exigencias_servico_v406.py` e `mutar_conferidor_v406.py`: mantida (o valor sobe: `"v404" -> "v405"`; o nome seguiria a analogia V15, mas é só nome e os dois arquivos concordam). Não mudei.
5. **403 e anteriores não sobem** (regra do motor e da receita): `comparar_v403_v404.py` etc. ficam como estão; `comparar_v402_v405.py` aparece na docstring de `comparar_v405_v406.py` l.6 como **nome fantasma** (o molde citava `comparar_v402_v404.py`, que também não existe; é só docstring).
6. **Não copiei `bancada_B3_servico\derivar_servico_v405.py`**: é um GERADOR com o mapa `403->404` embutido (`M = {"404": "405", "403": "404"}`); subir o rótulo daria `{"405": "406", "403": "405"}`, que quebra. O papel dele (gerar os 5 do serviço) foi cumprido pela cópia direta. Se quiser o gerador, reescrever o mapa.
7. **Cabeçalho `# [A ADAPTAR v406]`** em 33 arquivos: 1 linha, depois do shebang/`coding`; desloca a numeração em +1 (os números de linha deste arquivo e do JSON são os do arquivo GRAVADO). Fica fora da prova de «só rótulos» (é a única linha adicionada; cada diff mostra).
8. **Extras** (não estavam na lista mínima; todos são chamados por scripts da cadeia e existem em `v405\`): `gerar_candidato_v406.py`, `gerar_pino_das_pedras_v406.py`, `copiar_pedras_v406.py`, `copiar_insumos_v406.py`, `copiar_logs_do_kernel_v406.py`, `guarda_frases_v406.py`, `bateria_pre_selo/derivar_pre_selo_v406.py`, `bateria_pre_selo/conferir_recibo_pre_selo_v406.py`, `bateria_pre_selo/gerar_pino_recibo_pre_selo_v406.py`, `bateria_pre_selo/limpar_sandbox_vb21.py`, `bateria_pre_selo/snap_producao_v406.py`, `bateria_pre_selo/rodar_ensaio_1_pre_selo_v406.sh`. Se a gerência preferir escrever os autorais à mão (receita 5), basta ignorar/sobrescrever; os `bateria_pre_selo\*` são necessários ao `rodar_bn_pre_selo_v406.sh` derivado.
9. `regras_v406.py` (muda `~/.claude/settings.json` por ato da gerência) foi copiado **sem rodar** e mantém a trava `V406_REGRAS_AUTORIZADAS=sim`.
10. Não propaguei a guarda `noqa: E403 -> E402` do motor (não há `E403` nos moldes).

## 3. O que ficou [A ADAPTAR] para a gerência

**Regra de leitura**: nenhum corpo foi adaptado. Onde a v405 cita **as 8 pedras da v405 como «as novas»**, a v406 tem **bundle de 301 módulos** (`kernel_modulos_novos_v406.json`: `novos` com 301 entradas). Toda cópia abaixo roda a lógica da v405 sobre rótulos da v406; **não use nenhuma sem adaptar**. Linhas = arquivo gravado.

### 3.1 Por arquivo (classe -> nº de linhas que casam; as primeiras linhas estão em `a_adaptar` no JSON)

| arquivo gravado | linhas alt. | classes [A ADAPTAR] |
|---|---|---|
| `conferir_rito_v406.py` | 102 | pedras_stones=15; oito_pedras_8_modulos=8; esperados=72; kernel_modulos_novos=1; chaves_witness_False_True=3; delta_v406=45 |
| `teste_conferidor_positivo_v406.py` | 12 | esperados=1; delta_v406=2 |
| `gerar_esperados_v406.py` | 69 | pedras_stones=7; oito_pedras_8_modulos=3; esperados=10; kernel_modulos_novos=2; delta_v406=26 |
| `diff_e_pinos_v406.py` | 25 | pedras_stones=1; oito_pedras_8_modulos=1; esperados=2; delta_v406=8 |
| `conferir_citacoes_v406.py` | 24 | pedras_stones=15; oito_pedras_8_modulos=2; delta_v406=15 |
| `p00_precondicoes_v406.py` | 62 | pedras_stones=13; oito_pedras_8_modulos=7; esperados=13; kernel_modulos_novos=5; delta_v406=21 |
| `regerar_v406.sh` | 12 | pedras_stones=3; oito_pedras_8_modulos=1; esperados=1; delta_v406=1 |
| `comparar_v405_v406.py` | 16 | oito_pedras_8_modulos=5; esperados=3; delta_v406=3 |
| `pos_build_kernel_v406.py` | 47 | pedras_stones=12; oito_pedras_8_modulos=6; kernel_modulos_novos=6; delta_v406=18; bandeiras_ext_8_prefixos=1 |
| `ensaio_a_seco_v406.py` | 186 | pedras_stones=16; oito_pedras_8_modulos=8; kernel_modulos_novos=1; chaves_witness_False_True=3; delta_v406=70 |
| `simular_arvore_do_nos_v406.py` | 5 | pedras_stones=2; oito_pedras_8_modulos=1; delta_v406=4 |
| `exame_pontos_v406.py` | 57 | pedras_stones=11; oito_pedras_8_modulos=1; delta_v406=21 |
| `guardas_estaticas_bancada_v406.py` | 21 | delta_v406=7 |
| `instalar_v406.py` | 27 | pedras_stones=2; oito_pedras_8_modulos=2; esperados=12; kernel_modulos_novos=9 |
| `reverter_v406.py` | 14 | esperados=7; kernel_modulos_novos=3 |
| `rito_v406.sh` | 40 | treino_da_nativa_v4=1; pedras_stones=1; oito_pedras_8_modulos=3; esperados=1; kernel_modulos_novos=1 |
| `conferir_instalar_rito_v406.py` | 26 | oito_pedras_8_modulos=3; esperados=10; kernel_modulos_novos=10; delta_v406=4 |
| `guarda_ordem_de_chamada_v406.py` | 7 | pedras_stones=9 |
| `fim_de_cadeia_v406.sh` | 14 | - |
| `gerar_relatorio_v406.py` | 67 | pinos_intermediarios_da_v405=3; pedras_stones=11; oito_pedras_8_modulos=7; esperados=5; chaves_witness_False_True=1; delta_v406=3 |
| `fechar_preparacao_v406.py` | 20 | treino_da_nativa_v4=1; pinos_intermediarios_da_v405=4; oito_pedras_8_modulos=1; esperados=1 |
| `regras_v406.py` | 11 | - |
| `bancada_B3_servico/conferir_exigencias_servico_v406.py` | 36 | autorizacao_e_ordem_do_operador_da_v405=9; esperados=5 |
| `bancada_B3_servico/evento_c1_b3_v406.py` | 5 | esperados=3 |
| `bancada_B3_servico/recibo_parada_v406.py` | 16 | autorizacao_e_ordem_do_operador_da_v405=2 |
| `bancada_B3_servico/recibo_religamento_v406.py` | 10 | autorizacao_e_ordem_do_operador_da_v405=2 |
| `bancada_B3_servico/controle_negativo/mutar_conferidor_v406.py` | 26 | autorizacao_e_ordem_do_operador_da_v405=3; esperados=2 |
| `pos_rito/b3_recibo_v406.py` | 22 | oito_pedras_8_modulos=1 |
| `orquestrador/pos_treino_v406.py` | 40 | autorizacao_e_ordem_do_operador_da_v405=5; treino_da_nativa_v4=4; esperados=3 |
| `gerar_candidato_v406.py` | 115 | pedras_stones=16; oito_pedras_8_modulos=24; esperados=1; kernel_modulos_novos=4; delta_v406=37 |
| `gerar_pino_das_pedras_v406.py` | 7 | pedras_stones=27; oito_pedras_8_modulos=35 |
| `copiar_pedras_v406.py` | 6 | pedras_stones=4; oito_pedras_8_modulos=2; delta_v406=2 |
| `copiar_insumos_v406.py` | 10 | pedras_stones=2; oito_pedras_8_modulos=1; delta_v406=11 |
| `copiar_logs_do_kernel_v406.py` | 6 | pedras_stones=1 |
| `guarda_frases_v406.py` | 9 | pedras_stones=3; oito_pedras_8_modulos=3; delta_v406=9 |
| `bateria_pre_selo/derivar_pre_selo_v406.py` | 23 | - |
| `bateria_pre_selo/conferir_recibo_pre_selo_v406.py` | 21 | - |
| `bateria_pre_selo/gerar_pino_recibo_pre_selo_v406.py` | 26 | - |
| `bateria_pre_selo/limpar_sandbox_vb21.py` | 2 | - |
| `bateria_pre_selo/snap_producao_v406.py` | 3 | - |
| `bateria_pre_selo/rodar_ensaio_1_pre_selo_v406.sh` | 12 | - |

Classes: `autorizacao_e_ordem_do_operador_da_v405` = textos de autorização/ordem do operador da v405 (ordem de 01/11, sha 2c3da184ebefc7c4); `treino_da_nativa_v4` = espera do treino v4 da nativa (STATE_v4.json); `pinos_intermediarios_da_v405` = sha16 dos candidatos intermediários da preparação da v405 (narrativa das revisões); `pedras_stones` = pedras / STONES / REGISTRO_DE_PEDRA / FUNCOES_PEDRAS / nomes dos registros com função da v405; `oito_pedras_8_modulos` = «OITO», «8 pedras/módulos» e os nomes das 8 pedras; `esperados` = ESPERADOS / ESP[...] (chaves geradas por gerar_esperados); `kernel_modulos_novos` = kernel_modulos_novos / módulos novos do kernel; `chaves_witness_False_True` = specs das chaves whole_certificate_inhabited / inhabitant_exhibited / flags literais do gate; `delta_v406` = DL.* (delta) e alias do predecessor D1..D5; `bandeiras_ext_8_prefixos` = as 8 séries de bandeiras ext_{pdm,mtp,idt,obt,ldd,tdh,dde,pzp}405_NNNN; `constantes_numericas_v405` = constantes numéricas da v405 (10066, 9698, 1445, 368, 24971, 6901, 764951). (`pedras_mencao_em_texto` também está no JSON, mas é só menção em prosa e não gera cabeçalho.)

### 3.2 Contagens e listas fixadas na v405 (conferir/trocar primeiro)

- `conferir_rito_v406.py` l.230: `pedras_v405_ok ... len(ESP["pedras_v405_sha256"]) == 5` (as 5 anteriores; na v406 as anteriores incluem as 8 da v405 e a lista de pedras vira 301); l.4-5 e l.343: «os OITO registros com função»; l.393-394: `pedras_ok`, `ESP["kernel"]["raiz_sha16"]`/`audit_sha16`.
- `p00_precondicoes_v406.py` l.42: `sorted(novos) == sorted(DL.STONE_RELS) and len(DL.STONES) == 8`; l.76-87: «oito arquivos», «oito pedras» (guarda de frases e conferência de citações varrem **8** pedras; passam a varrer 301).
- `gerar_relatorio_v406.py` l.48: `len(KR.get("pedras")) == 8`; l.55: `len(GF.get("pedras")) == 8`.
- `conferir_instalar_rito_v406.py` l.5, l.73-74: o trecho do instalador é executado com `N` **igual a 8** (`passa_com_N_igual_a_oito`) e recusa se `n_passa != 8`; l.33-38 exigem tokens `NOVOS_V406`, `modulos_novos_v406`.
- `instalar_v406.py` l.38-48: `_PEDRAS_ANTERIORES` (lista de pedras já no Nós; na v406 inclui as 8 da v405) e `NOVOS_V406 = _nj["novos"]` (301) conferido contra `ESP["kernel"]["modulos_novos"]`; `reverter_v406.py` usa a lista que o instalar gravou (l.4, 18, 22).
- `guarda_ordem_de_chamada_v406.py` l.10-15: `FUNCOES_PEDRAS`/`FUNCOES_V405` = os nomes das 8 funções da v405 (`ponte_da_massa_v405`...) e `INSUMOS_EXIGIDOS`; na v406 a lista é a das funções NOVAS da v406 (preservei os nomes porque nasceram no `um.py` v405).
- `pos_build_kernel_v406.py`: o laço `for s in DL.STONES` (l.94-120: **cada pedra = um módulo, um teorema nomeado `s["theorem"]`, um grupo, um prefixo de bandeira `s["flag_prefix"]`**: `ext_{pdm,mtp,idt,obt,ldd,tdh,dde,pzp}405_NNNN`, l.6 e l.223-233) não tem o formato de um bundle de 301 (receita: modelar como a v394, `kernel_modulos_novos_v394.json`, e «conferir a política de bandeiras nomeadas e a série de chaves»); l.90: o conjunto de módulos com declaração tem de ser igual a `NEWMODS` (hoje 8, derivado de `novos`); l.134: Audit `< 900 s` (timeout do um.py: 1800 s, l.210); l.229-233: `x19='nao'` e «recibo só com as OITO novas»; a nota do recibo (l.~229) diz que o build do sandbox foi INCREMENTAL (na v406 o `lake build` dos 301 é frio).
- `gerar_candidato_v406.py` (extra): os 25 patches da v405 (K00/K01 raiz e +8 entradas, V01/V02/V03 bandeiras/escada/ledger, C12_* sobre `expected_ladder`, W01 `UM_VERSION`, N00..N02); na v406: K01 com 301 entradas, C12 sobre os 11 contratos **mais `_V405_CONTRACTS`**, `kh_n1_cobertura_v405 -> piso`. As etiquetas de stdout `[v404]`/`[v405]` casadas por regex (l.~103-124) são as que o `um.py` imprime e foram **preservadas**.
- `rito_v406.sh` l.24 (e comentário): tempo esperado e marcas **medidas na v405** (build incremental 454 s, Audit 340 s, 794 s por passagem; 399,65 s/158 s herdados): na v406 o build é a frio dos 301; `kernel\construir_marcas.txt` já existe em PK6 (início 19:56:34): o rito e o `lake build` do um.py (timeout 3600 s) têm de caber no tempo medido.
- `ensaio_a_seco_v406.py` (183 KB): 8 pedras em blocos `(6i)`/`(6j)`, `TAMPER405`, `R404`/`R405` (tabelas de registros), `D1..D4`; `exame_pontos_v406.py` l.403-404, 482, 517-520; `simular_arvore_do_nos_v406.py` l.55, 68.

### 3.3 Specs de False/True das chaves (receita 5.6: flip das 4 chaves só se o operador decidir, com patch AO LADO e errata)

Linhas que assertam o estado atual (None/False) e que mudam se alguma chave virar nesta versão: `conferir_rito_v406.py` l.321, 352, 397; `ensaio_a_seco_v406.py` l.192, 917, 963; `gerar_relatorio_v406.py` l.208 (todas minhas cópias, com cabeçalho). Nos **derivados do motor** (não tocados): `pos_rito\leitura_v406.py` l.393-405 (`whole_certificate_inhabited is not False`, `inhabitant_exhibited is False`) e l.544 (`null_tests_passed_blind`); `pos_rito\textos_v406.semente` l.308; `pos_rito\harness_textos_ensaio_v406.py` l.513, 525, 935; `pos_rito\harness_fechar_sandbox_v406.py` l.866 (controles negativos).

### 3.4 Autorização/ordem do operador e treino da nativa (texto da v405, não vale para a v406)

- `rito_v406.sh`: treino l.24
- `gerar_relatorio_v406.py`: pinos l.110,114,181
- `fechar_preparacao_v406.py`: treino l.21; pinos l.22,23,24,31
- `bancada_B3_servico/conferir_exigencias_servico_v406.py`: autorizacao l.5,63,82,87,88,89
- `bancada_B3_servico/recibo_parada_v406.py`: autorizacao l.10,11
- `bancada_B3_servico/recibo_religamento_v406.py`: autorizacao l.13,14
- `bancada_B3_servico/controle_negativo/mutar_conferidor_v406.py`: autorizacao l.6,50,52
- `orquestrador/pos_treino_v406.py`: autorizacao l.3,53,325,339,352; treino l.8,144,158,378

`recibo_parada_v406.py`/`recibo_religamento_v406.py` carregam `V406_AUTORIZACAO_OPERADOR` com o texto da ordem de **01/11 para a v405** (o recibo de parada/religamento da Bancada é ato do operador); `orquestrador\pos_treino_v406.py` S0 espera o **treino v4 da nativa** (STATE_v4.json), traz o ator/AUT de 01/11 e o extra das 17:36 do pensamento do dia: nada disso é da v406 sem nova ordem.

### 3.5 `delta_v406.py`: a API que as cópias esperam (117 nomes distintos, 106 NÃO definidos no esqueleto)

Esqueleto define só: `ARVORE`, `BASE_DIR`, `BASE_SHA16_DA_ORDEM`, `BASE_VERSION`, `C`, `CANDIDATO`, `CH`, `HERE`, `KERNEL_DIR`, `NOS`, `PACKAGES_ORIGEM`, `SANDBOX`, `SANDBOX_CURTO`, `SANDBOX_ORIGEM`, `SANDBOX_PAI`, `UM_VERSION`, `V405`.

Referenciados e **não definidos**: `ACOM_FONTES_OPERADOR`, `ACOM_FONTES_OPERADOR.items`, `ACORDE_KIMI_ARQ`, `ADENDO_ARQ`, `ADENDO_SHA16_DA_ORDEM`, `ANGLE_STATUS_ANTIGO_PREFIXO`, `AUDIT_PREFIX`, `AUX_CLASSES`, `CAMPOS_FECHADOS`, `CAMPOS_REGISTRO`, `CUNHAGENS_REGISTRO`, `D1.STONES`, `D1.VERBATIM_ORIGEM_V401`, `D2.N_CHECKS`, `D2.STONES`, `D2.STONE_BY_KEY`, `D2.VERBATIM_ORIGEM_V402`, `D3.N_CHECKS`, `D3.N_CHECKS_CAMINHO`, `D3.N_CHECKS_VERDADE_ADENDO`, `D3.N_CHECKS_VIDA`, `D3.REGISTRO_DE_PEDRA`, `D3.STONES`, `D3.STONE_BY_KEY`, `D3.STONE_RELS`, `D4.F2B_FUTURO_TOKEN`, `D4.JO8_IDX`, `D4.N_CHECKS`, `D4.REGISTRO_DE_PEDRA`, `D4.STONES`, `D4.STONE_BY_KEY`, `D4.STONE_RELS`, `D4.verbatins405`, `DECISOES`, `DECLARACAO_IDX`, `ERRATAS_V406`, `ERRATA_E10`, `ERRATA_E13`, `ESTUDO_E0`, `F2B_FUTURO_TOKEN`, `F81_LITERAIS`, `F81_PREFIXO_LS2`, `F81_ROTULO_PREREG`, `F9_CAMINHOS`, `F9_CAMINHOS.items`, `F9_DIR_DURAVEL`, `F9_RESULTADO_NOME`, `F9_RESULTADO_SHA256_DA_ORDEM`, `FORMA_REAL`, `FRASE_DA_MOLDURA_EN`, `FRASE_DA_MOLDURA_PT`, `FRASE_DA_MOLDURA_PT.replace`, `FRASE_DERIVAR_ALFA`, `FRASE_DO_OPERADOR_4_44`, `FRASE_IDENTIDADE_NOME`, `FRASE_ISSO_E_A_TGL`, `FRASE_NOMEACAO`, `FRASE_NOMES`, `FRASE_NOMES.replace`, `FRASE_SINGULARIDADE`, `FRASE_UM_DE_1EV`, `GAP_N_CHECKS`, `GAP_REGISTRO`, `GA_CLASSE_AGORA`, `GA_CLASSE_ANTES`, `GA_MEDIDA_ARQ`, `GA_PARECER_ARQ`, `GA_RECLASS_ARQ`, `GA_REGISTRO`, `HALF_NAT_ARQ`, `KH_N1_INSUMO`, `KH_REGISTRO`, `LEITURAS_DEFINICOES`, `LEITURA_V406`, `N_CHECKS`, `N_CHECKS_FALSIDADE`, `POSTOS_E_MEDIDA`, `REGISTROS_FUNCAO`, `REGISTRO_DE_PEDRA`, `ROOT_SUFFIX`, `SIDECAR_NOME`, `STONES`, `STONE_BY_KEY`, `STONE_MODS`, `STONE_RELS`, `TRIO_SET`, `V399`, `V400`, `V403`, `VERBATIM_EXCLUIDAS_V406`, `VERBATIM_ORIGEM`, `VERBATIM_ORIGEM_V403`, `VERBATIM_ORIGEM_V405`, `VERBATIM_ORIGEM_V406`, `VERBATIM_PREFIXOS_DA_ORDEM_V406`, `WK`, `_ENSAIO_R2_MD`, `classe`, `ensaio_identidade_r2`, `errata_entrega_005`, `lido`, `pedras_fontes`, `sha256`, `verbatim_origem_pelo_glob`, `verbatins403`, `verbatins406`.

**Alias do predecessor**: as copias usam DL.D4 (=delta_v404 no delta_v405) 23x, DL.D3 22x, DL.D2 10x, DL.D1 3x: na v406 o predecessor e' o delta_v405 (por convencao D5); decisao da gerencia: expor D5 e renomear, ou redefinir D1..D4 (o `delta_v405` fazia `D4 = delta_v404`, `D3 = delta_v403`...). As cópias seguem usando `DL.D4.*` para «o predecessor»: ou o `delta_v406` expõe `D5 = delta_v405` e as cópias trocam `D4->D5`, ou redefine `D4 = delta_v405` (o que muda o sentido de `D3`/`D2`). O lote C do executor anterior parou exatamente aqui.

### 3.6 `kernel_modulos_novos_v406.json`

O de PK6 (gerado em 19:56) tem `novos` (301), `n`, `root_suffix`, `gerado`. As cópias leem **só `novos`** (lista): `instalar` l.42-43, `p00` l.42/80, `pos_build_kernel` l.39, `conferir_instalar_rito` l.53, `gerar_esperados` l.36 [conferido por grep]. As chaves da v405 que ele não tem (`pedras`, `raiz_sha16`, `audit_sha16`, `raiz_v404_sha16`, `audit_v404_sha16`, `ordem_de_instalacao`, `sandbox_*`) **não são lidas daí** por estas cópias; `ESP["kernel"]["pedras"]`, `raiz_v405_sha16` etc. vêm do `CANDIDATO_v406.json` (gerar_candidato l.433-434), não deste JSON.

### 3.7 Nomes de arquivo citados que ainda não existem (a gerar) e fantasmas

**Saídas ou scripts da v406 ainda inexistentes cujo análogo da v405 existe** (66; são o que a cadeia vai produzir, ou o que a gerência ainda escreve: `runtime_v406.py`, `registros_v406.py`, `v406_pins.py`, `um_v406_candidato.py`, `textos_v406.py`, `*.pysnip`, `aplicar_errata_pedras_v406.py`, `adaptar_pos_rito_v406.py`):

`CANDIDATO_v406.json`, `COMPARACAO_V405_v406.json`, `CONFERENCIA_EXIGENCIAS_SERVICO_v406.json`, `CRITERIOS_v406.json`, `CUSTODIA_v406_RASCUNHO.txt`, `DEPOSITO_PREPARACAO_v406.md`, `DERIVACAO_PRE_SELO_v406.json`, `DERIVACAO_v406.json`, `DIFF_KERNEL_v406.txt`, `ESPERADOS_v406.json`, `FLAGS_v406.json`, `FORMAL_MAP_v406.json`, `GUARDAS_ESTATICAS_BANCADA_v406.json`, `GUARDA_FRASES_v406.json`, `HARNESS_FECHAR_SANDBOX_v406.json`, `HARNESS_TEXTOS_ENSAIO_v406.json`, `KERNEL_RECIBO_v406.json`, `KH_N1_v406.json`, `LOGS_COPIADOS_v406.json`, `MANIFESTO_INSUMOS_v406.json`, `PEDRAS_COPIA_v406.json`, `PINOS_BN_v406.json`, `PINO_DAS_PEDRAS_DETALHE_v406.json`, `PINO_MEMORIA_PY_v406.json`, `PINO_RECIBO_PRE_SELO_v406.json`, `PLANO_v406.md`, `POS_BUILD_v406.json`, `PRECONDICOES_v406.json`, `PREPARACAO_v406_PRONTA.json`, `PROVA_PRODUCAO_INTACTA_v406_pre_selo.json`, `RECIBO_PARADA_v406.json`, `RECIBO_RELIGAMENTO_v406.json`, `RELATORIO_POS_TREINO_v406.json`, `RELATORIO_POS_TREINO_v406.md`, `RELATORIO_PREPARACAO_v406.md`, `RESULTADO_CONTROLE_NEGATIVO_v406.json`, `REVISAO_TERCEIRO_v406.json`, `REVISAO_TERCEIRO_v406.md`, `REVISAO_TERCEIRO_v406_R1.md`, `SESSION_REFERENCE_prep_v406.json`, `VERBATIM_CONGELADO_v406.json`, `adaptar_pos_rito_v406.py`, `aplicar_errata_pedras_v406.py`, `artigo_en_v406.pysnip`, `artigo_pt_v406.pysnip`, `bn_pre_selo_out_v406.txt`, `conferencia_pelo_esboco_v406.json`, `conferencia_rito_v406_CONTROLE_NEGATIVO_PRE_RITO.json`, `conferencia_rito_v406_POSITIVO_FALSO_NOS.json`, `conferir_citacoes_v406.json`, `ensaio_a_seco_v406.json`, `fim_de_cadeia_out_v406.txt`, `harness_fechar_out_v406.txt`, `harness_textos_out_v406.txt`, `purga_out_v406.txt`, `purga_v406.json`, `refazer_out_v406.txt`, `registro_mapa_preparacao_v406_ANOTACAO.json`, `registros_v406.py`, `rito_horarios_v406.txt`, `rito_servidor_v406.log`, `runtime_v406.py`, `textos_v406.py`, `textos_v406_novo.pysnip`, `um_v406_candidato.py`, `v406_pins.py`

**Citados mas não classificados (8)**: `CUSTODIA_v406.txt` (gerar_relatorio_v406.py); `ESTADO_V406.md` (diff_e_pinos_v406.py); `_v405.json` (conferir_exigencias_servico_v406.py); `_v406.py` (mutar_conferidor_v406.py); `comparar_v402_v405.py` (comparar_v405_v406.py); `rito_v406_sinal.txt` (rito_v406.sh); `rodada_v406_stdout.txt` (conferir_instalar_rito_v406.py, conferir_rito_v406.py); `s_v406.pysnip` (conferir_citacoes_v406.py). São nomes de saída novos (`rodada_v406_stdout.txt`, `rito_v406_sinal.txt`, `CUSTODIA_v406.txt`, `ESTADO_V406.md`) ou pedaços de nome em prosa (`_v405.json`, `_v406.py`, `s_v406.pysnip`); o único fantasma real é `comparar_v402_v405.py` (docstring, item 5 da seção 2).

## 4. Achados nos 24 derivados do motor (NÃO tocados; para a gerência decidir)

- **13 de 24 são idênticos à minha cópia (subida pura de rótulo)**: `purga_v406.py`, `guarda_p18_v406.py`, `acom_conferencias_v406.py`, `runtime_quadro_v397.py`, `quadro_v397.py`, `refazer_candidato_v406.sh`, `refazer_sandbox_v406_pos_selo.sh`, `refazer_arvore_v406_pos_selo.py`, `pino_memoria_py_v406.py`, `bateria_pre_selo/rodar_bn_pre_selo_v406.sh`, `pos_rito/fila_memoria_v406.py`, `pos_rito/gerar_x_custodia_v406.py`, `pos_rito/textos_v406.semente`.
- **11 diferem** (regra/nota que o motor acrescentou ou correção do lote I): `copiar_base_v406.py`, `preparar_kernel_v406.py`, `pos_rito/superficies_v406.py`, `pos_rito/montar_textos_v406.py`, `pos_rito/fechar_v406.py`, `pos_rito/registrar_mapa_v406.py`, `pos_rito/leitura_v406.py`, `pos_rito/harness_textos_ensaio_v406.py`, `pos_rito/harness_fechar_sandbox_v406.py`, `pos_rito/chain_pos_rito_v406.sh`, `pos_rito/gerar_derivacao_pos_rito_v406.py`. Diffs em `bump\*.vs_derivado.diff` (`-` = minha cópia, `+` = derivado).
- **Defeito 1, `import` de módulo da cadeia não subido** (o motor preservou `leitura_v405` por coincidência com identificador do `um.py`; o arquivo `pos_rito\leitura_v405.py` NÃO existe em PK6, só `leitura_v406.py`): `pos_rito/superficies_v406.py` l.19: `import leitura_v405, textos_v406 as T`; `pos_rito/fechar_v406.py` l.21: `import leitura_v405 as L`; `pos_rito/registrar_mapa_v406.py` l.15: `import leitura_v405 as L`. Dentro do harness isso passa (ele registra `sys.modules["leitura_v405"]`, `harness_textos_ensaio_v406.py` l.192-196), **mas no `chain_pos_rito_v406.sh` real o import falharia**. Cuidado: a chave `leitura_v405` do core/ESPERADOS (ex.: `registrar_mapa_v406.py` l.218) é outro papel da mesma palavra e deve ficar.
- **Defeito 2, B(n) não subido nos derivados** (narrativa/comentário, não lógica; deveria ser B14 -> B15 e deployment `B14-v405-20261102-R1`): `pos_rito/harness_textos_ensaio_v406.py` l.1596 (B13, B14); `pos_rito/harness_fechar_sandbox_v406.py` l.1032 (B13, B14); `pos_rito/chain_pos_rito_v406.sh` l.23 (B13, B13-v405-20261028-R1); `pos_rito/chain_pos_rito_v406.sh` l.29 (B13); `pos_rito/gerar_derivacao_pos_rito_v406.py` l.23 (B13, B14). Em `chain_pos_rito_v406.sh` l.23 consta **`B13-v405-20261028-R1`, deployment que não existe** (o real, lido do recibo da v405, é `B14-v405-20261102-R1`); os `B11/B12` de `harness_fechar_sandbox_v406.py` l.12, 736, 775 já estavam errados no texto da v405 (o passo simples era B13->B14). `copiar_base_v406.py` l.3 está certo.

## 5. Como refazer / reconferir

`python -B -X utf8 _bump_copia_v406.py --seco` mede e compara sem gravar; sem `--seco` grava (backup de bytes se o destino existir e diferir). O gerador lê `v405\` só para leitura e escreve só em PK6 (`bump\`, destinos, `BUMP_v406_RESULTADO.json`).

