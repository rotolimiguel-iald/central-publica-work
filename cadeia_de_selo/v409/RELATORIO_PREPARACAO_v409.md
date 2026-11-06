# RELATÓRIO DA PREPARAÇÃO DA v409 — A tradução às classes de Turing e o par na face de Fock

Agente de preparação `claude-construtor-v409` · 2026-11-05 23:38 · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: este candidato (A traducao as classes de Turing, v409) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (D58, ate' tres rodadas) e a trava do orquestrador fica fechada ate a revisao aprovar; quem constroi nao aprova.** Nada foi instalado; o rito NÃO foi rodado; o Nós e a Bancada de produção só foram lidos; o `MEMORY.md` não foi tocado.

## 1. Estado em uma frase

Candidato `53284ba461ecd940` (43,970,027 B; base v408 `e7bc6b10e8ff76be`): `pronta` = **true**.

## 2. Portões (cada linha lida de um arquivo)

| portão | resultado |
|---|---|
| kernel (sandbox `C:\t\k409c\final`) | True: build + Audit rc 0, 158 bandeiras novas, escada 12029 → 12187, 2 módulo(s) no recibo; `KERNEL_RECIBO_v409.json` |
| candidato | True: 42 patches; refazer limpo = True |
| AST v408 × v409 | True: 1204 nós, 1177 iguais, 27 mudados (explicados), 0 removidos, 14 novos; 38 funções e constantes intactas, todas verdadeiras = True |
| ensaio a seco | True: TUDO PASSOU |
| conferidor | negativo True (`tudo_bate` = False); positivo True (`tudo_bate` = True) |
| citações | True: 0 apontada(s) à gerência nos textos (ver §4) |
| guarda das frases | True (controle negativo e a pedra: 2) |
| instalar / reverter / rito (estático) | True |
| p00 | True: 189/189 checagens OK; pendentes: 0 |
| B(n) pré-selo | True: JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA; bateria BATERIA_PASSA; produção intacta = True; recibo `5e4a4f8ded740fd7` |
| serviço da Bancada (estático) | True: 37/37 condições; toda mutação pega = True |
| harness dos textos | True: 657 controles da leitura, 67 do parágrafo novo |
| harness do fechar | True: 47 controles do fechar |
| regeneração limpa | True: `refazer_out_v409.txt` termina em `== FIM` e `RC_REFAZER=0` |
| purga da fala reservada | True: `purga_v409.json`, zero ocorrências na pasta e no sandbox do kernel |
| fala excluída fora dos artefatos | True: `purga_v409.json`, zero ocorrências |

Fora dos portões, informativo: o orquestrador sem S7 e sem S10 (D57a), medido na lista de passos e no laço de `orquestrador/pos_treino_v409.py` = True; os textos da custódia encadeados no S6d: textos_custodia_handoff_v409.py.

## 3. O que NÃO passou ou fica para depois

- p00 reprova 0 checagem(ns): nenhuma; pendentes (0): nenhum.
- Só depois do rito: o conferidor real, a leitura real, as superfícies, o B(n) pós-selo, os textos da custódia e o HANDOFF; os recibos do B(n) nos harnesses são sintéticos.
- Não feito (fora do escopo): instalar, rodar o rito, revisão independente, custódia, commit, push. A rota da preparação está no Mapa: `NAO LIDA (registro_mapa_prep_v409_ABERTA.json)`, seq .

## 4. Avisos e desvios ditos

- os nomes: o modulo TraducaoTuring e as declaracoes das rodadas R1 a R8, dados pela gerencia c1 e RATIFICADOS pelo operador em 05/11/2026; os acrescentados na R9 (a inscricao no psion e a formula SAT) e os da ParNaFaceDeFock (o modulo e as 10 declaracoes), da gerencia, foram RATIFICADOS por ele em 05/11 («Ratifico os nomes», D62; as docstrings das pedras dizem [DECLARADO] ate a ratificacao, registro da epoca da pedra; recibo revisto de 05/11 ~19h30; D55; a fala tem sha16 8b9b77e992902ff4, lido do arquivo agora: «Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados»); a ordem da traducao, da mesma data, tem sha16 c7ee4106eb7f2c83: «precisamos fechar o que ficou ainda em aberto em relação à identificação das classes de turing dentro do nosso dicionário»
- NENHUMA chave antiga muda de literal nesta versao (CHAVES_V409 vazia): as chaves seguem lidas do kernel do rito; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA; os vereditos dos registros anteriores NAO mudam (os que carregam a escada mudam so' em numeros); tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 sao RECRIADOS com a escada do contrato subida pela C12
- o alcance (D56), dito em todo texto novo: P = nP é teorema da TGL no modo seleção, relativo ao leitor (o psíon); a máquina sem leitor fica fora: é a fita sem escala («eu sou eu mesmo»); a tradução às classes das máquinas de Turing, [OPEN] na v408, fica fechada relativa ao leitor (TraducaoTuring; p_igual_np_no_modo_selecao)
- ressalvas ditas em todo texto (9 em delta_v409.RESSALVAS_V409): relativa ao leitor (Baker-Gill-Solovay 1975) [KNOWN]; a sombra de «eu sou eu mesmo» (a autorreferencia sozinha nao decide a pergunta das classes) [KNOWN]; a fisica fica fora (o lugar do teste com a natureza); a ponte entre o Omega do psion e o estado uniforme da instancia e' a inscricao, e a identidade de vetores fica podada (D60 revista); com o leitor que so' conta vale NP contido em P numa leitura, e a igualdade completa e' a do leitor que se le (E28); a leitura teologica nao e' termo de kernel; o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock; D60 revista); beta so' por nome; nenhum teste com a natureza; a regra do 4,44
- as erratas E24 a E28 e a E21 ao lado sao da gerencia c1, em nome proprio: E24, o juiz das classes de Turing e' o kernel, nao a fisica (correcao do operador); E25, saiu a frase da gerencia sobre o sistema ter de achar o lado do Nome em cada bifurcacao (o operador: ele trava no Nome; a_trava_no_nome); E26, AO LADO do registro tetelestai_terminal_v408 selado: a traducao a Turing, [OPEN] na v408, fica fechada relativa ao leitor na v409; o texto selado nao e' reescrito; E27, o dispositivo e' o no sorry (D61); E28, a igualdade com o leitor que so' conta: NP numa leitura, e a igualdade completa e' a do leitor que se le; E21 ao lado: a ligacao do par na face de Fock foi feita na v409
- as 14 falas do operador de 05/11/2026 entram por sha256 (lista congelada em VERBATIM_CONGELADO_v409.json; as quatro ultimas vieram dos AO LADO do fim do DESENHO: a 11a, a 12a, a 13a (a ordem de tudo entrar na v409) e a 14a (a ratificacao dos nomes, D62)); de tres (v409_cun_0d6468d77b5cc990, v409_cun_d63c0a91a5271fcb, v409_cun_9ee7d5a1b161437f), so' o trecho e' embutido e citado (duas pela D59; uma, a ratificacao da D61, porque o resto e' aviso operacional); o resto delas entra so' por sha256 e nao entra em texto do um.py; publicar o resto das duas da D59 e' decisao do operador
- a D61 (a leitura juridica do kernel, dada pelo operador e RATIFICADA por ele: o dispositivo e' o no sorry; o teorema e' a regra posta; a regra incide onde o suporte fatico se completa) vai nas decisoes e nos textos que dizem o que o kernel decide; a E27 (da gerencia c1, em nome proprio) vai ao lado
- D59: o DESENHO_v409.md (sha16 lido agora 3a05af6e5218fc94; o do delta 3a05af6e5218fc94) e o RECIBO_PEDRAS_v409_NOMES.json (sha16 lido agora a404f11878157258; o do delta a404f11878157258) NAO sao pinados como fonte no um.py: ficam citados so' por sha16
- D57(d): o pino do insumo do acervo da v407 (_V407_FONTES['psion_no_acervo_do_imac_03nov']) passa a copia purgada (sha16 f0b1c79a5caa75df, do delta); a integra so' por sha16; a errata da D57(d) vai AO LADO em cunhagens_v407
- as pedras TraducaoTuring e ParNaFaceDeFock: as fontes de origem (insumos/TraducaoTuring.lean, sha16 lido agora 86ddaa69fabd67f5; insumos/ParNaFaceDeFock.lean, sha16 e998d73d3ce60835) foram normalizadas para LF nas copias do kernel (pedra/TraducaoTuring.lean, sha16 4fe1c5ba2bc28300; pedra/ParNaFaceDeFock.lean, sha16 4b7ed028ebf5855d) e os #print axioms sairam do corpo embutido (as 82 ancoras foram lidas deles antes); o conteudo Lean nao muda
- o revisor distinto da v409 e' o Sonnet (D58: ate' tres rodadas; ressalvas BAIXAS escritas); esta preparacao NAO foi revisada por terceiro; quem constroi nao aprova; a trava do orquestrador (S1b) fica fechada ate' a revisao aprovar
- a regra do 4,44 (nunca sozinho: z_disc 4,44 calibrado, abaixo do degrau de 5 sigma da creditacao) vale em qualquer texto; nenhum teste com a natureza entra nesta versao; o pilar reusa a chave de cache
- o B(n) pre-selo da v409 (passo simples B18; a Bancada de producao pina B17-v408-20261105-R1) e o pino da memoria dependem de arquivos que a preparacao ainda nao gerou quando este relatorio nao os acha: o p00 os diz PENDENTES, nao erro, e `pronta` so' fica true com todos os portoes
- conferir_citacoes_v409.json aponta 0 citacao(oes) entre « » dos textos da gerencia que nao sao verbatim das falas do operador (arquivo: trecho): nenhuma; o agente nao corrige texto da gerencia
- na docstring da pedra TraducaoTuring ha citacoes entre « » que nao sao verbatim das falas (a fala escreve nP entre aspas e sem espaco; /psi por ψ; uma expressao da gerencia, «nada lido»; uma parafrase, «nP = modo seleção»): APONTADAS a gerencia em conferir_citacoes_v409.py (_APONTADAS_PEDRAS), com a razao conferida por grep; o agente nao corrige pedra
- build a frio do modulo no sandbox k409c: 366 s, Audit 257 s (kernel/POS_BUILD_v409.json, medidos); 34166 declaracoes no axiom_report (+223 decl, +182 teoremas sobre a v408), nenhuma fora do trio; escada 12029 -> 12187
- o orquestrador (orquestrador/pos_treino_v409.py) traz as licoes da v408 (D57): sem S7 (G1 --publicar) e sem S10 (release do app), MEDIDO agora na lista de passos e no laco = True; o S6d encadeia os textos da custodia (textos_custodia_handoff_v409.py) e roda o portao de textos do G1 e a D59 sobre o HANDOFF INTEIRO; o fim da cadeia desta versao e' o HANDOFF; a custodia completa e o release do app sao da sessao de custodia
- a guarda das frases ganhou a F37b (05/11; a causa de uma falha do ensaio): a obrigacao do qualificador relativo ao leitor vale tambem no proprio trecho onde «P = nP» e Turing aparecem juntos (a F37 do texto inteiro deixava passar uma frase plantada sem qualificador); a regra ficou mais estrita; nenhum teste foi relaxado
- o fim_de_cadeia_v409.sh PAROU no passo 2 (B(n) pre-selo: RC_BN=0, BATERIA_PASSA, producao intacta) porque o p00 que ele roda deu NENHUMA FALHA com 1 PENDENTE (o pino do memoria.py, PINO_MEMORIA_PY_v409.json, ato da gerencia) e o script exige TODAS PASSARAM; os passos 3 a 7 (servico estatico, derivacao do pos-rito, os dois harnesses, a previa do X) rodaram a mao com os MESMOS comandos do script (saida em fim_de_cadeia_passos3a7_out_v409.txt); o script nao foi mudado
- o conferidor do servico da Bancada (bancada_B3_servico/conferir_exigencias_servico_v409.py) so' lia o AUT do orquestrador como literal; o AUT da v409 e' MONTADO do delta (o prefixo de sha16 da ordem e a frase): corrigido na causa (so' a expressao do AUT e' avaliada, com o delta desta pasta, sem builtins); a checagem seguinte e' a mesma (o sha16 CALCULADO do arquivo da fala esta' no AUT); 37/37 e o controle negativo pegou toda mutacao
- duas outras causas do ensaio corrigidas na fonte (nenhum teste relaxado): o bloco herdado do terminal comparava o baseline do contrato da v408 com a base desta cadeia (v408) em vez da v407; o exame dos pontos de chamada nao retirava do core da base os registros da v408, que o bloco recria; e o rotulo herdado do C15 no conferidor (o defeito das guardas estaticas da Bancada) dizia que ele recusou a v408: o defeito e' o da v399

## 5. Para a gerência — ordem sugerida

1. Revisão de terceiro (o Sonnet, D58: até três rodadas), nesta ordem, antes de qualquer publicação: `delta_v409.py` (moldura, erratas E24 a E28 e a E21 ao lado, decisões D55 a D62, as leituras, as ressalvas), `registros_v409.py`, `runtime_v409.py` (as 20 checagens de `traducao_turing_v409` e a guarda das frases com a F37b), as pedras em `pedra/` (TraducaoTuring e ParNaFaceDeFock), as seções do artigo (`artigo_pt_v409.pysnip`, `artigo_en_v409.pysnip`) e `pos_rito/textos_v409.semente`.
2. Dizer ao operador, na língua dele (regra do posto), o que a v409 NÃO entrega: validade no kernel não é creditação; P = nP é teorema da TGL no modo seleção, relativo ao leitor (o psíon); a máquina sem leitor (a pergunta do Clay) fica fora e não é decidida aqui; o par na face de Fock está ligado nesta versão (ParNaFaceDeFock; D60 revista); a identidade Ω = uniforme está podada (a ponte é a inscrição); com o leitor que só conta, a igualdade completa não está provada (E28, validade não afirmada); as duas chaves que ficam False ficam por teorema; o 4,44 continua abaixo do degrau de 5 sigma; nenhum teste com a natureza entra nesta versão.
3. O orquestrador lê `PREPARACAO_v409_PRONTA.json` e segue: `instalar_v409.py`, `rito_v409.sh`, `pos_rito/chain_pos_rito_v409.sh` (0 → 10, 10a, 10b, 10c → 14), os textos da custódia encadeados (S6d) e o HANDOFF (fim da cadeia, D57a), com a trava S1b aberta só pela revisão aprovada; a custódia completa e o release do app são da sessão de custódia.
4. Se o rito cair: `reverter_v409.py` é decisão da gerência; `refazer_candidato_v409.sh --regerar` refaz o candidato.

## 6. O módulo e as âncoras

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
| `TraducaoTuring.lean` | 05nov_nome_da_gerencia_ratificado_R1_a_R8__acrescimos_da_R9_DECLARADO (antes: `TraducaoTuring`) | 72 | 110 | `4fe1c5ba2bc28300` |
| `ParNaFaceDeFock.lean` | 05nov_nome_da_gerencia_DECLARADO_ate_a_ratificacao (antes: `ParNaFaceDeFock`) | 10 | 48 | `4b7ed028ebf5855d` |

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
| `TGLExt.TraducaoTuring.p_igual_np_no_modo_selecao` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0138` |
| `TGLExt.ParNaFaceDeFock.o_par_na_face_de_fock` | `TGLExt/ParNaFaceDeFock.lean` | `ext_tu409_0027` |
| `TGLExt.TraducaoTuring.a_traducao` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0088` |
| `TGLExt.TraducaoTuring.a_trava_no_nome` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0093` |
| `TGLExt.TraducaoTuring.a_fita_e_o_hamiltoniano_oculto` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0070` |
| `TGLExt.TraducaoTuring.z_e_o_modo_leitor` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0157` |
| `TGLExt.TraducaoTuring.a_fita_sem_escala` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0071` |
| `TGLExt.TraducaoTuring.o_pai_da_mentira` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0126` |
| `TGLExt.TraducaoTuring.a_identidade_performada` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0073` |
| `TGLExt.TraducaoTuring.a_maquina_com_o_leitor` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0077` |
| `TGLExt.TraducaoTuring.o_canto_do_psion_da_luz_le_z` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0118` |
| `TGLExt.ParNaFaceDeFock.reduzido_do_par` | `TGLExt/ParNaFaceDeFock.lean` | `ext_tu409_0047` |
| `TGLExt.ParNaFaceDeFock.meia_nat_do_projetor` | `TGLExt/ParNaFaceDeFock.lean` | `ext_tu409_0023` |

## 7. Artefatos e hashes (lidos agora)

| arquivo | bytes | sha16 |
|---|---|---|
| `um_v409_candidato.py` | 43,970,027 | `53284ba461ecd940` |
| `CANDIDATO_v409.json` | 162,345 | `06f30fc9783e3081` |
| `ESPERADOS_v409.json` | 1,118,823 | `f74e24abb9cfe567` |
| `ensaio_a_seco_v409.json` | 416,384 | `9d3958a9daec260b` |
| `COMPARACAO_V408_v409.json` | 12,253 | `e67e1bb11d346159` |
| `PINOS_BN_v409.json` | 5,085 | `9221ff82b5b706af` |
| `PINO_RECIBO_PRE_SELO_v409.json` | 6,215 | `5e4a4f8ded740fd7` |
| `PROVA_PRODUCAO_INTACTA_v409_pre_selo.json` | 10,061 | `6a164a0acc2f4c0e` |
| `PRECONDICOES_v409.json` | 31,357 | `69714da377dcfa4a` |
| `GUARDA_FRASES_v409.json` | 29,285 | `a546f57a481cb0b7` |
| `VERBATIM_CONGELADO_v409.json` | 7,238 | `ecefa04ddf021bef` |
| `BUNDLE_v409.json` | 9,730 | `b218d3bdc44e94c7` |
| `kernel_modulos_novos_v409.json` | 202 | `70be69218e62fd41` |
| `DESENHO_v409.md` | 22,432 | `3a05af6e5218fc94` |
| `delta_v409.py` | 72,639 | `bf546f1dd6fc7bb3` |
| `registros_v409.py` | 45,761 | `54a886d8ce1eb83a` |
| `runtime_v409.py` | 33,356 | `3a7fcf271dd52ea8` |
| `guarda_frases_v409.py` | 22,807 | `c929b3c3e0928be5` |
| `guarda_ordem_de_chamada_v409.py` | 19,714 | `898a41aae9308d14` |
| `guardas_estaticas_bancada_v409.py` | 11,105 | `04a015a6ebc22e58` |
| `gerar_candidato_v409.py` | 52,540 | `13f2902d70714ebd` |
| `gerar_esperados_v409.py` | 40,209 | `c0e61558ad26f8ec` |
| `artigo_pt_v409.pysnip` | 16,755 | `6f693be7b2872fed` |
| `artigo_en_v409.pysnip` | 17,564 | `9b8523e29395e3ca` |
| `comparar_v408_v409.py` | 29,074 | `1c6c5aa4b6a54eb4` |
| `instalar_v409.py` | 11,909 | `f29a8400c3571461` |
| `reverter_v409.py` | 5,725 | `d1a40cdd9665d642` |
| `rito_v409.sh` | 26,295 | `9438e3c930b70083` |
| `conferir_rito_v409.py` | 93,504 | `102f906ddd35f88f` |
| `conferir_citacoes_v409.py` | 31,086 | `d0713c3ccf6642a5` |
| `p00_precondicoes_v409.py` | 40,672 | `ceb29109b02b24e2` |
| `preparar_bundle_v409_05nov.py` | 15,588 | `72d4569adbdedf28` |
| `MANIFESTO_INSUMOS_v409.json` | 8,169 | `3a5b53b7851c648a` |
| `pos_build_kernel_v409.py` | 34,668 | `54da187505dcc530` |
| `fechar_preparacao_v409.py` | 8,408 | `87ab7a4345160d40` |
| `purga_v409.py` | 3,916 | `77f6fe651d20c070` |
| `purga_v409.json` | 516 | `b32708f8c2472de7` |
| `kernel/LOGS_COPIADOS_v409.json` | 815 | `dcd427e9554e3dc8` |
| `insumos/TraducaoTuring.lean` | 77,924 | `86ddaa69fabd67f5` |
| `insumos/TraducaoTuring_embutida.lean` | 72,462 | `4fe1c5ba2bc28300` |
| `insumos/ParNaFaceDeFock.lean` | 26,209 | `e998d73d3ce60835` |
| `insumos/ParNaFaceDeFock_embutida.lean` | 25,214 | `4b7ed028ebf5855d` |
| `insumos/TraducaoTuringR9.lean` | 77,900 | `6b318e7fc07de29a` |
| `insumos/ParNaFaceDeFockR2.lean` | 22,528 | `50b5cc16ddaec8db` |
| `insumos/RECIBO_PEDRAS_v409_NOMES.json` | 9,910 | `a404f11878157258` |
| `pos_rito/textos_v409.semente` | 115,916 | `c356e851a85f2c6c` |
| `pos_rito/montar_textos_v409.py` | 6,500 | `17a0308d62e25f06` |
| `pos_rito/leitura_v409.py` | 151,683 | `cade8f2956ab71b4` |
| `pos_rito/fechar_v409.py` | 26,231 | `4bdec628a26f669b` |
| `pos_rito/registrar_mapa_v409.py` | 58,627 | `17a4b7f20ef63ae1` |
| `pos_rito/superficies_v409.py` | 19,068 | `e0487ca9cea1f00b` |
| `pos_rito/harness_textos_ensaio_v409.py` | 183,226 | `c007b50cd7670063` |
| `pos_rito/harness_fechar_sandbox_v409.py` | 117,609 | `dac0a0f224e229d2` |
| `pos_rito/chain_pos_rito_v409.sh` | 39,806 | `d5416c8e3068e7fb` |
| `pos_rito/gerar_x_custodia_v409.py` | 7,635 | `a85dcb20b716182f` |
| `pos_rito/b3_recibo_v409.py` | 9,549 | `607244670aeaad31` |
| `pos_rito/fila_memoria_v409.py` | 11,369 | `c21ed1c33456cd8e` |
| `pos_rito/gerar_derivacao_pos_rito_v409.py` | 9,958 | `d076b14d2dda58e7` |
| `orquestrador/pos_treino_v409.py` | 50,933 | `8bdd16f45c7ec5c2` |
| `bancada_B3_servico/recibo_parada_v409.py` | 6,696 | `959a6882584d3ee7` |
| `bancada_B3_servico/recibo_religamento_v409.py` | 6,295 | `808e6ae5ef904284` |
| `bancada_B3_servico/evento_c1_b3_v409.py` | 2,315 | `f5bf1dd1a61f1b20` |
| `bancada_B3_servico/conferir_exigencias_servico_v409.py` | 16,308 | `3c6b3a45d60ef8f5` |
| `bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v409.json` | 10,670 | `e2fa2617997efb41` |
| `bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v409.json` | 14,775 | `93d52a9a41680425` |
| `pos_rito/textos_custodia_handoff_v409.py` | 21,883 | `ef9df32a0a80f252` |
| `pedra/TraducaoTuring.lean` | 72,462 | `4fe1c5ba2bc28300` |
| `pedra/ParNaFaceDeFock.lean` | 25,214 | `4b7ed028ebf5855d` |
| `kernel/KERNEL_RECIBO_v409.json` | 205,701 | `12a71b3cc86924ab` |
| `kernel/FLAGS_v409.json` | 60,972 | `fd9ab8820880fe91` |
| `kernel/KH_N1_v409.json` | 1,131 | `ef646b95adf6c3c0` |
| `kernel/POS_BUILD_v409.json` | 28,512 | `e3f21e1dd152f93a` |
