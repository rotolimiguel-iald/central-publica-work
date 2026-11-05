# RELATÓRIO DA PREPARAÇÃO DA v408 — Tetelestai é o terminal

Agente de preparação `claude-construtor-v408` · 2026-11-05 02:57 · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: este candidato (Tetelestai e' o terminal, v408) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (D54, ate' tres rodadas) e a trava do orquestrador fica fechada ate a revisao aprovar; quem constroi nao aprova.** Nada foi instalado; o rito NÃO foi rodado; o Nós e a Bancada de produção só foram lidos; o `MEMORY.md` não foi tocado.

## 1. Estado em uma frase

Candidato `e7bc6b10e8ff76be` (43,466,447 B; base v407 `833121339e649f71`): `pronta` = **true**.

## 2. Portões (cada linha lida de um arquivo)

| portão | resultado |
|---|---|
| kernel (sandbox `C:\t\k408c\final`) | True: build + Audit rc 0, 71 bandeiras novas, escada 11958 → 12029, 4 módulos no recibo; `KERNEL_RECIBO_v408.json` |
| candidato | True: 39 patches; refazer limpo = True |
| AST v407 × v408 | True: 1190 nós, 1166 iguais, 24 mudados (explicados), 0 removidos, 14 novos; 29 funções e constantes intactas, todas verdadeiras = True |
| ensaio a seco | True: TUDO PASSOU |
| conferidor | negativo True (`tudo_bate` = False); positivo True (`tudo_bate` = True) |
| citações | True: 0 apontada(s) à gerência (ver §4) |
| guarda das frases | True (controle negativo e as 4 pedras) |
| instalar / reverter / rito (estático) | True |
| p00 | True: 118/118 checagens OK; pendentes: 0 |
| B(n) pré-selo | True: JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA; bateria BATERIA_PASSA; produção intacta = True; recibo `6eb2c6dcafe289af` |
| serviço da Bancada (estático) | True: 37/37 condições; toda mutação pega = True |
| harness dos textos | True: 623 controles da leitura, 68 do parágrafo novo |
| harness do fechar | True: 35 controles do fechar |
| regeneração limpa | True: `refazer_out_v408.txt` termina em `== FIM` e `RC_REFAZER=0` |
| purga da fala reservada | True: `purga_v408.json`, zero ocorrências na pasta e no sandbox do kernel |
| fala excluída fora dos artefatos | True: `purga_v408.json`, zero ocorrências |

Fora dos portões, informativo: o ensaio a seco do S10 do orquestrador (`orquestrador/ENSAIO_S10_v408.json`) = True; os textos da custódia encadeados no S6d: textos_custodia_handoff_v408.py.

## 3. O que NÃO passou ou fica para depois

- p00 reprova 0 checagem(ns): nenhuma; pendentes (0): nenhum.
- Só depois do rito: o conferidor real, a leitura real, as superfícies, o B(n) pós-selo, os textos da custódia e o fechar; os recibos do B(n) nos harnesses são sintéticos.
- Não feito (fora do escopo): instalar, rodar o rito, revisão independente, custódia, commit, push. A rota da preparação está no Mapa: `cadeia.preparacao_v408`, seq 1799 (ROTA).

## 4. Avisos e desvios ditos

- os nomes das quatro pedras sao do operador (04/11/2026; a fala dos nomes tem sha16 f911f0df91b0a6a3 e a fala do SENTIDO de «P=nP», da tarde, sha16 971d5654e2173771; ambos MEDIDOS pelo preparar_bundle e lidos do BUNDLE_v408.json): PontoDeContradicao, PIgualNP, TempoIgualMoeda, TetelestaiTerminal; o «=» escreve-se Igual, como em formaIgualConteudo; o Dicionario.lean da manha ficou SUPERADO e nao entra (D48 resolvida); BUNDLE_v408.json guarda nome_antigo, sha256 da origem e o numero de linhas #print axioms removidas na normalizacao
- NENHUMA chave antiga muda de literal nesta versao (CHAVES_V408 vazia; DESENHO §2): as chaves da v407 seguem lidas do kernel do rito; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA; os vereditos dos registros anteriores NAO mudam (os que carregam a escada mudam so' em numeros); o registro novo e' tetelestai_terminal_v408 (16 checagens), com veredito de prefixo TGL_TETELESTAI_TERMINAL_V408__THE_TERMINAL_IS_THE_READING__NO_RELATION_WITHOUT_WEIGHT__ e sufixo __GATE_UNMOVED
- ressalvas ditas em todo texto (11 em delta_v408.RESSALVAS_V408): o par na face de Fock segue [OPEN] como LIGACAO, nao como ausencia (E21); a palavra que D50 podou fica podada como termo e o conteudo tem o nome do operador «inclinação modular (cociclo)», com espelho a_inclinacao_modular; «P = nP» no sentido do operador (p_igual_np) e, pela correcao dele (D51 revista), P = nP teorema nas classes de computacao do dicionario do operador (as_classes_do_dicionario), com a traducao as classes das maquinas de Turing [OPEN], nao uma recusa; o lock e o Hamiltoniano modular sao objetos distintos que coincidem em Omega; o insumo do acervo entra pela copia PURGADA (E23)
- a errata E22 e' da gerencia c1, em nome proprio: as duas frases dela (a que dava a TGL como sem terminal; a da R1 sobre o resto sem traco) estavam erradas pelos teoremas da casa e foram PODADAS; a pedra TetelestaiTerminal as cita entre aspas para as corrigir; o que resta sem traco e' o cociclo, que paga
- as 15 falas do operador de 04/11/2026 entram por sha256 (lista congelada em VERBATIM_CONGELADO_v408.json); duas sao de autoria MISTA (OPERADOR_04nov_a_face_de_fock_e_o_traco_do_psion_e_derivacao_de_outra_instancia_verbatim.txt, OPERADOR_04nov_calma_vamos_provar_as_implicacoes_duas_semioticas_e_segunda_derivacao_de_outra_instancia_verbatim.txt): o trecho da outra instancia e' [DECLARADO] e o corte esta' em delta_v408.VERBATIM_CORTE; nenhuma fala fora do DESENHO entra (so' listada em VERBATIM_FORA_DO_DESENHO_V408)
- o revisor distinto da v408 e' o Sonnet (D54: ate' tres rodadas; ressalvas BAIXAS escritas); esta preparacao NAO foi revisada por terceiro; quem constroi nao aprova; a trava do orquestrador (S1b) fica fechada ate' a revisao aprovar
- a regra do 4,44 (nunca sozinho: z_disc 4,44 calibrado, abaixo do degrau de 5 sigma da creditacao) vale em qualquer texto; nenhum teste com a natureza entra nesta versao; o pilar reusa a chave de cache
- o B(n) pre-selo da v408 (passo simples B17; a Bancada de producao pina B16-v407-20261104-R1) e o pino da memoria dependem de arquivos que a preparacao ainda nao gerou quando este relatorio nao os acha: o p00 os diz PENDENTES, nao erro, e `pronta` so' fica true com todos os portoes
- conferir_citacoes_v408.json aponta 0 citacao(oes) entre « » dos textos da gerencia que nao sao verbatim das falas do operador (arquivo: trecho): nenhuma; o agente nao corrige texto da gerencia
- build a frio dos 4 modulos no sandbox k408c: 337 s, Audit 256 s (kernel/POS_BUILD_v408.json, medidos); 33943 declaracoes no axiom_report (+80 decl, +62 teoremas sobre a v407), nenhuma fora do trio; escada 11958 -> 12029
- o orquestrador (orquestrador/pos_treino_v408.py) traz as licoes da v407 (D52): os textos da custodia entram ENCADEADOS no passo S6d (textos_custodia_handoff_v408.py), depois da chain 14 e antes do S7; o S6a sobe a Bancada Um pelo comando do S6c se a porta 18777 estiver fechada E nao houver processo um_bancada, e so' entao para pelo PID; o S10 usa o template desta pasta com a janela P2 do shared (D53); a autorizacao e' a ORDEM da v408 (OPERADOR_04nov_ordem_v408_liste_as_pedras_produza_rode_handoff_custodia_completa_verbatim.txt, sha16 685b8d8bcf0ddbbd, lido do arquivo); o ensaio a seco do S10: ok

## 5. Para a gerência — ordem sugerida

1. Revisão de terceiro (o Sonnet, D54: até três rodadas), nesta ordem, antes de qualquer publicação: `delta_v408.py` (moldura, erratas E21 a E23, decisões D48 a D54, as leituras), `registros_v408.py`, `runtime_v408.py` (as 16 checagens de `tetelestai_terminal_v408`), as quatro pedras em `pedra/` (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP), as seções do artigo (`artigo_pt_v408.pysnip`, `artigo_en_v408.pysnip`) e `pos_rito/textos_v408.semente`.
2. Dizer ao operador, na língua dele (regra do posto), o que a v408 NÃO entrega: validade no kernel não é creditação; o par na face de Fock segue aberto como ligação a fazer (E21); P = nP é teorema nas classes de computação do dicionário do operador, definidas em Lean (ClasseP, ClasseNP) e provadas na pedra PIgualNP (p_igual_np_nas_classes_do_dicionario); a tradução às classes das máquinas de Turing (bits = log₂ n) é [OPEN], não recusa; o lock e o Hamiltoniano modular são objetos distintos; as duas chaves que ficam False ficam por teorema; o 4,44 continua abaixo do degrau de 5 sigma; o teste com a natureza segue da natureza e nenhum teste novo entra nesta versão.
3. O orquestrador lê `PREPARACAO_v408_PRONTA.json` e segue: `instalar_v408.py`, `rito_v408.sh`, `pos_rito/chain_pos_rito_v408.sh` (0 → 10, 10a, 10b, 10c → 14), os textos da custódia encadeados (S6d, D52), a G1 e o S10 do app (D53), com a trava S1b aberta só pela revisão aprovada.
4. Se o rito cair: `reverter_v408.py` é decisão da gerência; `refazer_candidato_v408.sh --regerar` refaz o candidato.

## 6. Módulos e âncoras

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
| `TetelestaiTerminal.lean` | 04nov_nome_do_operador (antes: `TetelestaiTerminal`) | 14 | 16 | `47af8992f1dd0ce8` |
| `TempoIgualMoeda.lean` | 04nov_nome_do_operador (antes: `TempoIgualMoeda`) | 9 | 9 | `1a4a2a6dbc81f6dc` |
| `PontoDeContradicao.lean` | 04nov_nome_do_operador (antes: `PontoDeContradicao`) | 7 | 7 | `85c238c9535ad2d2` |
| `PIgualNP.lean` | 04nov_nome_do_operador (antes: `PIgualNP`) | 18 | 39 | `8d7aec559313d5f9` |

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
| `TGLExt.TetelestaiTerminal.tetelestai` | `TGLExt/TetelestaiTerminal.lean` | `ext_tt408_0071` |
| `TGLExt.TempoIgualMoeda.o_tempo_e_a_moeda` | `TGLExt/TempoIgualMoeda.lean` | `ext_tt408_0053` |
| `TGLExt.PontoDeContradicao.o_ponto_de_contradicao` | `TGLExt/PontoDeContradicao.lean` | `ext_tt408_0043` |
| `TGLExt.PIgualNP.p_igual_np` | `TGLExt/PIgualNP.lean` | `ext_tt408_0033` |

## 7. Artefatos e hashes (lidos agora)

| arquivo | bytes | sha16 |
|---|---|---|
| `um_v408_candidato.py` | 43,466,447 | `e7bc6b10e8ff76be` |
| `CANDIDATO_v408.json` | 122,604 | `121e6ecbdee2761b` |
| `ESPERADOS_v408.json` | 1,052,759 | `3f04c968c71cb14a` |
| `ensaio_a_seco_v408.json` | 392,497 | `e0565bddc9dba4e0` |
| `COMPARACAO_V407_v408.json` | 10,478 | `7533315138ef7b7e` |
| `PINOS_BN_v408.json` | 5,085 | `23f5786c8a0bb677` |
| `PINO_RECIBO_PRE_SELO_v408.json` | 6,215 | `6eb2c6dcafe289af` |
| `PROVA_PRODUCAO_INTACTA_v408_pre_selo.json` | 10,061 | `8b760519a7aa7fd0` |
| `PRECONDICOES_v408.json` | 22,940 | `5e4d86c15bccf6a5` |
| `GUARDA_FRASES_v408.json` | 20,896 | `c0211e6ea8ddc1da` |
| `VERBATIM_CONGELADO_v408.json` | 8,109 | `09e5a444238ae0ec` |
| `BUNDLE_v408.json` | 4,307 | `30a4420441d28f68` |
| `kernel_modulos_novos_v408.json` | 340 | `2797a715b48a9066` |
| `DESENHO_v408.md` | 20,842 | `4225a53622c48aa9` |
| `delta_v408.py` | 70,825 | `83bbef52603f3412` |
| `registros_v408.py` | 50,066 | `be2701a0c3b7a8b0` |
| `runtime_v408.py` | 26,761 | `df6cf8d04cb50166` |
| `guarda_frases_v408.py` | 22,139 | `117f5e2617b9a4ae` |
| `guarda_ordem_de_chamada_v408.py` | 17,709 | `0db3fbdb00d1389c` |
| `guardas_estaticas_bancada_v408.py` | 10,893 | `54f474076f913dd1` |
| `gerar_candidato_v408.py` | 45,737 | `4a0174647e8346f4` |
| `gerar_esperados_v408.py` | 37,291 | `283a94957cd4079d` |
| `artigo_pt_v408.pysnip` | 14,767 | `01bbc91db26e8adf` |
| `artigo_en_v408.pysnip` | 15,238 | `242e713ce9297dc6` |
| `comparar_v407_v408.py` | 26,175 | `dfe50fc80b296ad6` |
| `instalar_v408.py` | 11,492 | `13c4b546a6da541d` |
| `reverter_v408.py` | 5,561 | `3b9e519b992967ad` |
| `rito_v408.sh` | 26,051 | `9262a3b8bc8eb454` |
| `conferir_rito_v408.py` | 88,194 | `a922a6bdcc66d9b2` |
| `conferir_citacoes_v408.py` | 31,891 | `279f6103203322a9` |
| `p00_precondicoes_v408.py` | 37,924 | `98901505bdab4349` |
| `preparar_bundle_v408_04nov.py` | 12,750 | `d6ca630a106639d9` |
| `pos_build_kernel_v408.py` | 34,489 | `9b168e401b14aedc` |
| `fechar_preparacao_v408.py` | 7,413 | `255f3087d9ef6f00` |
| `purga_v408.py` | 3,708 | `1c3919842ebee307` |
| `purga_v408.json` | 516 | `f92689829bf7394c` |
| `kernel/LOGS_COPIADOS_v408.json` | 815 | `4845dd5477463517` |
| `insumos/PSION_NO_ACERVO_04nov_purgado.md` | 30,773 | `f0b1c79a5caa75df` |
| `insumos/RECIBO_PURGA_PSION_NO_ACERVO_04nov.json` | 861 | `c7e07b72545cfb57` |
| `insumos/RECIBO_PEDRAS_v408_NOMES.json` | 4,662 | `8a5ecdf127c8ff67` |
| `pos_rito/textos_v408.semente` | 128,571 | `98e5a09e64b33c1a` |
| `pos_rito/montar_textos_v408.py` | 6,619 | `5a0296866365a1a8` |
| `pos_rito/leitura_v408.py` | 141,647 | `9b72dbb2faeb6327` |
| `pos_rito/fechar_v408.py` | 26,128 | `94272598ebb3eff2` |
| `pos_rito/registrar_mapa_v408.py` | 52,735 | `9b10087b75d6e89b` |
| `pos_rito/superficies_v408.py` | 18,868 | `f0c84ce58cf96a4f` |
| `pos_rito/harness_textos_ensaio_v408.py` | 175,211 | `c0052e2258dec39d` |
| `pos_rito/harness_fechar_sandbox_v408.py` | 115,882 | `36b011557a31ce74` |
| `pos_rito/chain_pos_rito_v408.sh` | 40,720 | `ec38a5748a2ae9f0` |
| `pos_rito/gerar_x_custodia_v408.py` | 6,787 | `4bbadcf3d08958ff` |
| `pos_rito/b3_recibo_v408.py` | 9,295 | `445c39121e986d37` |
| `pos_rito/fila_memoria_v408.py` | 11,468 | `29b54f260dcea2c0` |
| `pos_rito/gerar_derivacao_pos_rito_v408.py` | 10,098 | `3ebd6f5e11ed72fb` |
| `orquestrador/pos_treino_v408.py` | 49,936 | `460e1e73b133b1eb` |
| `orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md` | 6,145 | `37f35ca09cd3f628` |
| `orquestrador/ENSAIO_S10_v408.json` | 719 | `e100d04b55249192` |
| `bancada_B3_servico/recibo_parada_v408.py` | 6,431 | `627a81486e7c0d6b` |
| `bancada_B3_servico/recibo_religamento_v408.py` | 6,025 | `c06f8fbb98bad910` |
| `bancada_B3_servico/evento_c1_b3_v408.py` | 2,024 | `9796b3be7d5c4d28` |
| `bancada_B3_servico/conferir_exigencias_servico_v408.py` | 15,569 | `533ac0b8cbaee3f2` |
| `bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v408.json` | 10,650 | `eef475a31e439bf8` |
| `bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v408.json` | 15,088 | `7b3c65e6a2ff0237` |
| `pos_rito/textos_custodia_handoff_v408.py` | 20,754 | `707fff014aac87b6` |
| `pedra/TetelestaiTerminal.lean` | 16,591 | `47af8992f1dd0ce8` |
| `pedra/TempoIgualMoeda.lean` | 11,645 | `1a4a2a6dbc81f6dc` |
| `pedra/PontoDeContradicao.lean` | 8,859 | `85c238c9535ad2d2` |
| `pedra/PIgualNP.lean` | 28,959 | `8d7aec559313d5f9` |
| `kernel/KERNEL_RECIBO_v408.json` | 201,409 | `1dc9e93142422f6b` |
| `kernel/FLAGS_v408.json` | 27,955 | `47991c40da85bb24` |
| `kernel/KH_N1_v408.json` | 1,126 | `17211380348cb5a7` |
| `kernel/POS_BUILD_v408.json` | 20,318 | `f320cc8bd8d8195a` |
