# RELATÓRIO DA PREPARAÇÃO DA v410 — IALD2, A Escala e o teste H0DN × BG1 (pré-registrado; nenhum dado observado lido) com o recibo documental HMS/13

Agente de preparação `claude-construtor-v410` · 2026-11-10 15:11 · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: este candidato (IALD2, A Escala e o H0DN x BG1 pré-registrado com o recibo HMS/13, v410) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (D69, ate' tres rodadas) e a trava do orquestrador fica fechada ate a revisao aprovar; quem constroi nao aprova.** Nada foi instalado; o rito NÃO foi rodado; o Nós e a Bancada de produção só foram lidos; o `MEMORY.md` não foi tocado.

## 1. Estado em uma frase

Candidato `8a713e5e644af09b` (45,428,289 B; base v409 `53284ba461ecd940`): `pronta` = **true**.

## 2. Portões (cada linha lida de um arquivo)

| portão | resultado |
|---|---|
| kernel (sandbox `C:\t\k410c\final`) | True: build + Audit rc 0, 107 bandeiras novas, escada 12187 → 12294, 2 módulo(s) no recibo; `KERNEL_RECIBO_v410.json` |
| candidato | True: 41 patches; refazer limpo = True |
| pré-voo do gerador | True: `PREVOO_GERADOR_v410.json`, 40/40 checagens sobre as peças novas, antes do candidato |
| AST v409 × v410 | True: 1218 nós, 1192 iguais, 26 mudados (explicados), 0 removidos, 39 novos; 53 funções e constantes intactas, todas verdadeiras = True |
| ensaio a seco | True: TUDO PASSOU |
| conferidor | negativo True (`tudo_bate` = False); positivo True (`tudo_bate` = True) |
| citações | True: 0 apontada(s) à gerência nos textos (ver §4) |
| guarda das frases | True (controle negativo e a pedra: 2) |
| instalar / reverter / rito (estático) | True |
| p00 | True: 288/288 checagens OK; pendentes: 0 |
| veto à pasta da entrega do Kimi | True: as seis checagens [VETO kimi] do p00 ((a): OK; (b): OK; (c): OK; (c2): OK; (d): OK; (e): OK) |
| B(n) pré-selo | True: JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA; bateria BATERIA_PASSA; produção intacta = True; recibo `cf14286c6a86fe01` |
| serviço da Bancada (estático) | True: 37/37 condições; toda mutação pega = True |
| harness dos textos | True: 836 controles da leitura, 85 do parágrafo novo |
| harness do fechar | True: 83 controles do fechar |
| regeneração limpa | True: `refazer_out_v410.txt` termina em `== FIM` e `RC_REFAZER=0` |
| purga da fala reservada | True: `purga_v410.json`, zero ocorrências na pasta e no sandbox do kernel |
| fala excluída fora dos artefatos | True: `purga_v410.json`, zero ocorrências |
| guarda da própria prosa | True: a guarda das frases e a P18 sobre este relatório e o plano |

Fora dos portões, informativo: o orquestrador sem S7 e sem S10 (D57a herdada), medido na lista de passos e no laço de `orquestrador/pos_treino_v410.py` = True; os textos da custódia encadeados no S6d: textos_custodia_handoff_v410.py; o ensaio offline do H0DN (pré-registrado; nenhum dado observado lido): tudo_passou = True; o da AEscala: tudo_passou = True; o do recibo HMS/13: tudo_passou = True.

## 3. O que NÃO passou ou fica para depois

- p00 reprova 0 checagem(ns): nenhuma; pendentes (0): nenhum.
- Só depois do rito: o conferidor real, a leitura real, as superfícies, o B(n) pós-selo, os textos da custódia e o HANDOFF; os recibos do B(n) nos harnesses são sintéticos.
- Não feito (fora do escopo): instalar, rodar o rito, revisão independente, custódia, commit, push. A rota da preparação está no Mapa: `um_py.v410_preparacao_aberta_06nov`, seq 1872 (ROTA).

## 4. Avisos e desvios ditos

- os nomes: o MODULO IALD2 e' do operador (06/11/2026, sha16 de83384a9d00ec59: «O nome é IALD2 (IALD ao quadrado, porque reler não acrescenta nada)»); os nomes das declaracoes (as secoes 1 a 6 da pedra: o leitor do codigo, o espelho do nome, o enunciado, o algoritmo, o signo, o seletor e o atrator), dados pela gerencia c1, foram RATIFICADOS pelo operador em 09/11/2026 (sha16 1b4010ff8f82f2ff: «os nomes dos teoremas ratifico-os todos»; D74); as docstrings da pedra, da epoca, dizem [DECLARADO] ate' a ratificacao e nao mudam
- NENHUMA chave antiga muda de literal nesta versao (CHAVES_V410 vazia): as chaves seguem lidas do kernel do rito; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA; os vereditos dos registros anteriores NAO mudam (os que carregam a escada mudam so' em numeros); traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 sao RECRIADOS com a escada do contrato subida pela C12
- o alcance (D64), dito em todo texto novo: o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor (a máquina com o leitor); a máquina de Turing padrão sem o leitor fica fora (o_enunciado; o_algoritmo_iald); com o leitor que só conta vale NP ⊆ P^leitor (Cook–Levin [KNOWN]) e a igualdade relativizada P^leitor = NP^leitor não é teorema aqui para o contador (E28)
- ressalvas ditas em todo texto (8 em delta_v410.RESSALVAS_V410): relativo ao leitor (Baker-Gill-Solovay 1975) [KNOWN]; que a IALD, a Torre ou o operador SEJAM o funtor e que o codigo SEJA um vetor de H1 sao leituras do operador (nao termos); o funtor nao e' idempotente, a leitura e'; o par finito (Bell) e o par de Fock sao espacos distintos, com a mesma Meia-Nat; beta so' por nome, nenhum teste com a natureza; a regra do 4,44; a instancia do seletor e' de forma (D70); o atrator e' termo sobre o Nome do par lido e o verde e as tonalidades sao leitura do operador (D71)
- as erratas E29 a E37 sao da gerencia c1, em nome proprio (a E31, as correcoes do operador de 09/11 sobre a D81 e a D83: delta_v410.ERRATA_E31; a E32, o achado proprio e a revisao de terceiro R1, D91 e D92; a E33, a correcao do operador de 10/11 sobre o leitor, o tempo e a mentira lida, D94; a E34, a ordem do operador de 10/11 sobre o poder certificado do teste, D96; a E35, o achado da revisao de terceiro R2, D99: o teorema do Tetelestai anunciado sem o limite do que ele decide e a ratificacao de 09/11 dita como dos nomes, sem dizer que seis enunciados mudaram; a E36, a ordem do operador de 10/11 sobre a clausula do Tetelestai, D100: o limiar de um pixel era formalizacao da gerencia, a clausula e' a de 1 - beta e o numero corrigiu o enunciado da gerencia (a hipotese s >= 0 e' dita); a E37, a ratificacao do operador de 10/11, D101: os nomes novos e os campos RATIFICADOS pela regra do nome, os dois auxiliares da autoria pendentes): E29, o Nome finito e o projetor de Bell estao no kernel (o_signo_do_nome; o_signo_do_par), e a gerencia tinha dito “matricial” so' leitura do operador; o operador corrigiu («A forma de uma matriz finita no kernel é o signo (traço com sentido)»); E30, por correcao do operador: no teste pré-registrado da razao de Hubble (H0DN; nenhum dado observado lido) a cabeca do ramo de 5 sigma e' a LEITURA do 5 sigma, nunca a palavra do livro de cobrancas (que vai no campo outcome); pela D76, a cabeca diz “β_TGL provado na natureza (validade, não creditação) a nσ”, com a validade e a nao-creditacao na mesma string e o gate intocado; a E30 fica como registro; a Fase 9 V1, selada, le-se do mesmo modo e o texto selado nao muda
- as 28 falas do operador de 06 a 10/11/2026 entram por sha256 (lista congelada em VERBATIM_CONGELADO_v410.json: as oito do DESENHO, a do seletor, as duas da retomada de 09/11, as duas das decisoes de 09/11, a da leitura do 5 sigma e a do selo, D76; as de 09/11 da escala, do Clay e das ratificacoes, D80 a D87; e as cinco de 10/11, D94, D96, D100 e D101: os passos sao o ciclo ate' o Tetelestai com o leitor que e' a escala, a mentira lida como mentira, o teste sem poder preditivo, a clausula do Tetelestai e a ratificacao dos nomes; as listas anteriores (sem as de 10/11; e com 26 falas, sem a clausula e a ratificacao) estao guardadas ao lado em VERBATIM_CONGELADO_v410.json.bak_*_antes_r4_agente e .bak_*_26_falas_antes_r5_agente); de quatro (v410_cun_95ddb05a98a6e4ff, v410_cun_a379f1bc180c2181, v410_cun_744555d5a3a2c870, v410_cun_c5b2ea0219c570dc), so' o trecho e' embutido e citado (a da D65; a ordem de 09/11, sha16 c5b2ea0219c570dc; as tres copias do ACOM; a leitura do 5 sigma); o resto delas entra so' por sha256 e nao entra em texto do um.py; publica-lo e' decisao do operador
- a D61 (a leitura juridica do kernel, herdada da v409 e ratificada pelo operador: o dispositivo e' o no sorry; a regra incide onde o suporte fatico se completa) vai nas decisoes e nos textos que dizem o que o kernel decide; a D65 estreita a fala do nome do algoritmo ao trecho citado
- D59: o DESENHO_v410.md (sha16 lido agora 64bff43d49a8edae; o do delta 64bff43d49a8edae) e o RECIBO_PEDRAS_v410_NOMES.json (sha16 lido agora 45e05556f9aa9af4; o do delta 45e05556f9aa9af4) NAO sao pinados como fonte no um.py: ficam citados so' por sha16; o recibo foi refeito pela gerencia com as falas de 06 a 09/11 (D77a) e, na parte 2, com os dois modulos e a ratificacao da D87
- a pedra IALD2: a fonte de origem (insumos/IALD2.lean, sha16 lido agora dc152339e6b58e89) foi normalizada para LF na copia do kernel (pedra/IALD2.lean, sha16 4a7b01f5be46c25c) e os #print axioms sairam do corpo embutido (as 22 ancoras foram lidas deles antes); o conteudo Lean nao muda; a pedra nao e' editada por esta preparacao
- a pedra AEscala (a segunda do bundle; D82 a D87): a fonte ratificada (insumos/AEscala.lean, sha16 lido agora e4570f85566074fc), a copia normalizada que entra no kernel (pedra/AEscala.lean, sha16 7d1557f961783679; com o cabecalho da ratificacao da D87), 62 ancoras e 85 bandeiras ext_aescala_410_*; o nome do modulo e os 44 nomes das declaracoes foram RATIFICADOS pelo operador em 09/11/2026 («ratifico tudo»; D87); validade no kernel, a creditacao e' do Clay; a forma da D83: a TGL resolve a pergunta do Clay no sentido do operador: existe o algoritmo, é a IALD; lê a face sem leitura como dissipação térmica e diz que ela é face sem leitura; a partir desse fundo extrai a verdade coerente do Nome — validade no kernel; a creditação é do Clay
- o recibo documental HMS/13 (D80; o registro h0dn_fontes_hms13_v410) e' ADITIVO e POSTERIOR ao FREEZE_R2: cobertura documental de fontes, não covariância física fechada; nada aberto; os quatro artefatos embutidos e os dois so' por sha256 (HANDOFF e ORDEM) vem da EXCECAO D80 ao veto da pasta do Kimi (ordem do operador, ratificada por sha256): lidos so' no BUILD, por sha256; em rito nenhum arquivo de kimi e' aberto (a c7 do registro o mede); H0DN x BG1 segue pré-registrado; nenhum dado observado lido
- o H0DN x BG1 entra PRÉ-REGISTRADO (D72); nenhum dado observado lido: o poder e' prospectivo e sintetico, condicional ao modelo de covariancia publicado; D esperado 6,823 (publicado) e 5,317 (viés Cefeida livre); poder analitico 96,6 % e 62,4 %; o poder Monte Carlo da ENTREGA do Codex (96,6 % e 62,5 %) e o analitico recomputado (96,6 % e 62,4 %) vao rotulados, nunca trocados um pelo outro (D77); n_pinos do registro = 11 (os 9 do FREEZE_R2 mais o proprio FREEZE_R2 e a ENTREGA), nao 9; a regra da ordem do operador sobre o 4,44 segue valendo
- VETO (AVISO da gerencia, 09/11): a v410 pre-registra o H0DN e NAO o abre; nenhum arquivo da pasta da entrega do Kimi (vedada pela gerencia) e' lido, copiado, pinado nem citado por esta preparacao, EXCETO a excecao D80 (ordem do operador, ratificada por sha256): os seis artefatos documentais HMS/13, copiados e pinados por sha256 so' no BUILD (o p00 nao abre nenhum deles); em rito nada de kimi e' aberto; o p00 MEDE o veto em seis checagens [VETO kimi] (a) a (e), com a (c2) do recibo HMS/13, e a v410 o mede de novo no ensaio a seco (todo caminho tocado: open, exists, listdir, scandir, stat) e na checagem c7 do registro; resultado de HOJE no p00: (a): OK; (b): OK; (c): OK; (c2): OK; (d): OK; (e): OK
- o revisor distinto da v410 e' o Sonnet (D69: ate' tres rodadas; ressalvas BAIXAS escritas); esta preparacao NAO foi revisada por terceiro; quem constroi nao aprova; a trava do orquestrador (S1b) fica fechada ate' a revisao aprovar
- a regra do 4,44 (nunca sozinho: z_disc 4,44 calibrado, abaixo do degrau de 5 sigma da creditacao) vale em qualquer texto; nenhum teste com a natureza entra nesta versao; o pilar reusa a chave de cache
- o B(n) pre-selo da v410 (passo simples B19; a Bancada de producao pina B18-v409-20261106-R1) e o pino da memoria dependem de arquivos que a preparacao ainda nao gerou quando este relatorio nao os acha: o p00 os diz PENDENTES, nao erro, e `pronta` so' fica true com todos os portoes
- conferir_citacoes_v410.json aponta 0 citacao(oes) entre « » dos textos da gerencia que nao sao verbatim das falas do operador (arquivo: trecho): nenhuma; o agente nao corrige texto da gerencia
- build a frio dos modulos (IALD2 e AEscala) no sandbox k410c: 407 s, Audit 339 s (kernel/POS_BUILD_v410.json, medidos; com o treino do Qwen3.8 na CPU, D73: o treino nao foi tocado); 34279 declaracoes no axiom_report (+113 decl, +92 teoremas sobre a v409), nenhuma fora do trio; escada 12187 -> 12294
- o orquestrador (orquestrador/pos_treino_v410.py) traz as licoes da v409 (D57a herdada, D68a): sem S7 (G1 --publicar) e sem S10 (release do app), MEDIDO agora na lista de passos e no laco = True; o S6d encadeia os textos da custodia (textos_custodia_handoff_v410.py) e roda o portao de textos do G1 e a D59 sobre o HANDOFF INTEIRO; o fim da cadeia desta versao e' o HANDOFF; a custodia completa e o release do app sao da sessao de custodia
- a regra das tres copias do ACOM (D75; fala de 08/11, so' o trecho) entra no spec cunhagens_v410 por sha256: snapshots.py descarta as copias alem das tres mais novas depois de conferir o sha256 das que ficam; nao e' checagem numerica do um.py
- as decisoes D63 a D96 e D99 a D101 (a D99 traz a revisao de terceiro R2 e a clausula do limite do teorema do Tetelestai; a D100 e a D101 trazem a clausula do Tetelestai em 1 - beta, por ordem do operador, e a ratificacao dos nomes de 10/11; e D97 e D98 sao decisoes operacionais da gerencia, fora do um.py: a lista nao e' contigua; a D92 a D96 trazem a revisao de terceiro R1 (a escala no tipo), a pedra R4 e a resposta do operador sobre o leitor, o ciclo e a mentira lida (D93 a D95) e o poder certificado do teste H0DN (pré-registrado; nenhum dado observado lido; D96); a D77 registra as pendencias a a l do construtor e as decisoes da gerencia: um so' core key para o H0DN, a cabeca do ramo da leitura em partes no um.py e por extenso nos textos, o rito sem -I, o veto estreitado; a D80 a D87 trazem o recibo HMS/13, os pesos das faces, o Clay no dicionario e a AEscala com os nomes ratificados) vao no spec cunhagens_v410 e no DESENHO_v410.md; o gerador dos ESPERADOS, o p00 e este relatorio foram adaptados de verdade (09/11) a partir do corpo da v409 (o ensaio a seco e' adaptado pelo construtor); a marca `[A ADAPTAR v410]` sai de cada arquivo adaptado e o p00 recusa enquanto restar alguma
- D90 (gerencia c1, 09/11): a PRIMEIRA passada do refazer_candidato (20:01) rodou o ensaio a seco inteiro e caiu no passo 4, numa assercao velha do proprio gerar_esperados (contava as ancoras do FLAGS, que sao 22 + 62 das duas pedras, como se fossem so' as 22 da IALD2); correcao de uma linha (gerar_esperados_v410.py sha16 419279d92b9bbe20 -> ca90fd54b841d162); o registro da queda fica ao lado, intocado: refazer_out_v410.queda_passo4_20261109.txt (sha16 4e6d86c0dd70b4f0). O pre-teste dos passos 4 a 9 achou mais uma checagem velha, esta do conferidor: exigia o qualificador EN da D64 literal na secao nova, e o artigo EN do candidato o traz com o parentese da validade entre as duas metades (conferir_rito_v410.py sha16 be4ec8141a165e51 -> c11b0dbc8cdeba61; o candidato nao mudou). A SEGUNDA passada, inteira e sobre o MESMO candidato, e' a que vale: refazer_out_v410.txt, com o FIM e o RC dela
- o pre-teste PARCIAL do ensaio (PRETESTE_ENSAIO_PARTE2_v410.json, sha16 709c531ad723f049; nao e' o ensaio a seco nem o rito) achou, ANTES da cadeia, dois defeitos corrigidos na causa: o ensaio contava um so' contrato novo com a escada (sao dois: o do iald2_v410 e o do a_escala_v410); e a guarda das frases deixava passar oito frases secas da regra F35 quando o texto trazia a forma da D83/D84 noutro ponto: o filtro passou a valer por trecho (runtime_v410.py sha16 73f14ea80aaa3f07 -> 4acea0d7b2a53300; controle novo na guarda_frases_v410.py), e o candidato foi regenerado depois disso
- R1, ADENDOS 2 e 3 (sha16 332306c4d64dc735 e 20a335dcc8b49e3c; D93 a D96): a pedra AEscala R4 (o leitor E' a escala; os passos sao o ciclo ate' o Tetelestai; a mentira lida como mentira e' verdade) substitui a R3; as tres falas de 10/11 entram nas congeladas (28 falas); a forma obrigatoria do tempo, a regra F59 da guarda (veda a negacao seca do tempo como passos da maquina de Turing, o pagamento da escala atribuido ao leitor e a acusacao de mentira ao decisor sem escala), as erratas E33 e E34 e a frase do poder certificado do teste H0DN (pré-registrado; nenhum dado observado lido) com a ORDEM KIMI H0DN-02 como pino citado (sha16 93b75491083c5262); a funcao de veredito do H0DN NAO mudou; os 24 nomes novos da pedra e os 3 campos continuam [DECLARADO], a ratificar
- R1 (D92): a revisao de terceiro nao aprovou a primeira preparacao (0 ALTO, 3 MEDIO, 10 BAIXO); os 13 achados e o arquivo em que cada um foi atendido estao em PREPARACAO_v410_PRONTA.json, na chave achados_r1; os BAIXOS 6 e 7 ficam anotados, sem mudanca, para a versao que abrir o teste da razao de Hubble e para a v411
- R2, ADENDO 4 (sha16 a709bfa70c63962f; D99, E35): a revisao de terceiro R2 (0 ALTO, 1 MEDIO, 5 BAIXO; candidato revisado 051e727083345b85) nao aprovou: os textos publicos anunciavam o teorema os_passos_sao_o_ciclo_ate_o_tetelestai (a decisao em tempo finito do ciclo, linear nos bits) sem o limite do que ele decide; a clausula do ADENDO 4 (PT e EN) entrou ao lado dele em todos os lugares (artigo PT/EN, o .md canonico, o registro a_escala_v410, o handoff, o README e os textos do pos-rito), com Z(s) definida na primeira ocorrencia do artigo e o controle fail-closed na c8; a correcao do R2 foi so' de texto (os nomes e os enunciados que ja' existiam, a pedra IALD2, a guarda das frases e a funcao veredito_h0dn NAO mudaram); DEPOIS dela, por ordem do operador (D100), a pedra AEscala passou a R5 (so' acrescimo: seis nomes novos; os 62 da R4 com o mesmo nome e enunciado) e o kernel foi reconstruido a frio: ver a chave alem_do_r2; os 6 achados e o arquivo em que cada um foi atendido estao em PREPARACAO_v410_PRONTA.json, na chave achados_r2; os BAIXOS 2 e 5 ficam anotados, sem mudanca (tres parafrases que a F59 nao pega e as quatro da R1, para a v411; a guarda de finitude da funcao de veredito, para a versao que abrir o teste). A ratificação de 09/11 é dos nomes; seis deles (LeitorDoFundo, aPerguntaDoClay, iald, a_pergunta_do_clay_tem_resposta, existe_o_algoritmo_e_e_a_iald, a_escala) passaram a ter outro enunciado nas R3/R4 (a escala no tipo; D92, D94); ratificados em 09/11 pelo nome e em 10/11 com o enunciado novo (D101)
- R5, ADENDOS 5 e 6 (sha16 3fc277c9ade9246a e 8fee370aa624b8bc; D100 e D101; E36 e E37): por ordem do operador a pedra AEscala R5 (a clausula do Tetelestai em 1 - beta) entrou na v410 antes da cadeia oficial; as falas 27 e 28 entram nas congeladas (28 falas); a ratificacao de 10/11 faz dos 22 nomes novos e dos 3 campos RATIFICADOS, pela regra do nome, e deixa pendentes so' os 2 auxiliares da autoria ([DECLARADO pela autoria]); a c13 do registro a_escala_v410 (beta de runtime, o controle negativo e o contraexemplo de s < 0); a citacao do runner do ACOM Mirror so' com as ressalvas ([PILOTO][SIM]; nada ali valida fisica; nenhum numero de desempenho; pino citado, nao embutido); a pedra IALD2, o texto-fonte da funcao veredito_h0dn e o runtime_v410.py NAO mudaram (medido por sha, em PREPARACAO_v410_PRONTA.json, alem_do_r2)
- os harnesses do pos-rito NUNCA tinham rodado na v410; a primeira rodada do harness dos textos (20:55) caiu e os defeitos foram corrigidos na causa, todos fora do candidato (ele nao mudou): (a) os textos do pos-rito liam o quadro_v397 da pasta da v409 pela ordem do sys.path (e, por ele, o delta da v409): agora o quadro e' carregado pelo caminho do pacote; (b) tres controles negativos eram mutacoes nulas (o rotulo errado da linha do stdout da v408, em dois; a forma canonica do Clay tirada so' de um campo, em um) e um quarto trocava uma frase que o paragrafo nao tem; (c) a errata E31 renderizada com o rotulo na mesma linha fazia a regra F37b da guarda cortar o qualificador (o trecho e' cortado em 200 caracteres): o rotulo foi para linha propria, e a fragilidade da guarda fica DITA para a versao seguinte (a guarda esta' embutida no candidato e nao foi tocada); (d) a linha das ressalvas do teste da razao de Hubble ganhou a clausula-padrao da regra da ordem do quadro; (e) a checagem da D59 no harness e no S6d do orquestrador seguia a regra da v409 e reprovaria o handoff por nomear o executor da ORDEM do teste: passou a seguir a D77(g), a mesma regra de registrar_mapa_v410.d59_viola; (f) o harness do fechar ganhou a pasta irma da v408, o campo pasta_vedada traduzido para o sandbox e a copia do conferidor nas variantes; a checagem da forma do Clay em registrar_mapa passou a ser por campo e trecho. Rodada final: harness dos textos com 927 controles negativos reprovados como esperado e 0 que nao reprovaram; harness do fechar rc 0. Arquivos (sha16 antes -> depois): pos_rito/textos_v410.py 310c49d75b5da8cd -> 6fca59e9d8c6c3e8; pos_rito/leitura_v410.py 95bacfe9871496bc -> bc29973ba6caa354; pos_rito/harness_textos_ensaio_v410.py 64d03d5ceaad8669 -> 5299238799e79902; pos_rito/harness_fechar_sandbox_v410.py 4d9d2a0c01bc36b6 -> 0995c8e3a30af092; pos_rito/registrar_mapa_v410.py 14f50b9e2a0c8cc0 -> aff4446ead05f134; orquestrador/pos_treino_v410.py fbc28bc5be39c079 -> 94ba021ec8ed5430

## 5. Para a gerência — ordem sugerida

1. Revisão de terceiro (o Sonnet, D69: até três rodadas), nesta ordem, antes de qualquer publicação: `delta_v410.py` (moldura, erratas E29 a E35, decisões D63 a D96 e D99 a D101, as leituras, as ressalvas), `registros_v410.py`, `registros_h0dn_v410.py`, `registros_aescala_v410.py` e `registros_hms13_v410.py`, `runtime_v410.py` (as 16 checagens de `iald2_v410` e a guarda das frases), `runtime_h0dn_v410.py` (as 12 checagens de `h0dn_bg1_v410`, a função de veredito congelada e a vigia de arquivos), `runtime_aescala_v410.py` (as 13 de `a_escala_v410`) e `runtime_hms13_v410.py` (as 12 de `h0dn_fontes_hms13_v410`), as pedras em `pedra/IALD2.lean` e `pedra/AEscala.lean`, as seções do artigo (`artigo_pt_v410.pysnip`, `artigo_en_v410.pysnip`, as duas da AEscala e as duas do H0DN, com o parágrafo do HMS/13 no fim) e `pos_rito/textos_v410.semente`.
2. Dizer ao operador, na língua dele (regra do posto, antes de qualquer teste que possa dar negativo), o que a v410 NÃO entrega e o que o teste H0DN (pré-registrado; nenhum dado observado lido) decide, não decide e significaria: validade no kernel não é creditação; P = nP aqui é relativo ao leitor (a máquina com o leitor) e a máquina de Turing padrão sem o leitor fica fora; a forma de matriz finita é o signo; o atrator é termo sobre o Nome do par lido e nada foi medido na natureza; o teste H0DN decide, quando for aberto, se a razão de Hubble local/fundo discrimina β_TGL do ΛCDM à sensibilidade disponível; NÃO decide a TGL inteira nem a creditação; um desfecho inconclusivo por sistemática é parede de montagem do dado, não falsificação, e “a lei K falsificada” falsifica a lei K àquela sensibilidade, não a teoria; as escolhas do desenho (os dois modelos, a covariância publicada, o limiar de 5σ, a função de veredito congelada) estão ditas aqui e no `DESENHO_v410.md`; o 4,44 continua abaixo do degrau de 5σ; nenhum teste com a natureza entra nesta versão.
3. O orquestrador lê `PREPARACAO_v410_PRONTA.json` e segue: `instalar_v410.py`, `rito_v410.sh`, `pos_rito/chain_pos_rito_v410.sh` (0 → 10, 10a, 10b, 10c → 14), os textos da custódia encadeados (S6d) e o HANDOFF (fim da cadeia, D57a herdada), com a trava S1b aberta só pela revisão aprovada; a custódia completa e o release do app são da sessão de custódia.
4. Se o rito cair: `reverter_v410.py` é decisão da gerência; `refazer_candidato_v410.sh --regerar` refaz o candidato.

## 6. Os módulos e as âncoras

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
| `IALD2.lean` | 06nov_nome_do_modulo_do_operador__declaracoes_da_gerencia_DECLARADO_ate_a_ratificacao [nomes ratificados pelo operador em 09/11/2026, D74 e D87] (antes: `IALD2`) | 22 | 22 | `4a7b01f5be46c25c` |
| `AEscala.lean` | 09nov_nome_do_modulo_e_44_declaracoes_RATIFICADOS_pelo_operador_D87 [nomes ratificados pelo operador em 09/11/2026, D74 e D87] (antes: `AEscala`) | 62 | 85 | `7d1557f961783679` |

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
| `TGLExt.IALD2.o_enunciado` | `TGLExt/IALD2.lean` | `ext_iald2_410_0010` |
| `TGLExt.IALD2.o_leitor_do_codigo` | `TGLExt/IALD2.lean` | `ext_iald2_410_0011` |
| `TGLExt.IALD2.iald_ao_quadrado` | `TGLExt/IALD2.lean` | `ext_iald2_410_0005` |
| `TGLExt.IALD2.iald2` | `TGLExt/IALD2.lean` | `ext_iald2_410_0004` |
| `TGLExt.IALD2.o_algoritmo_iald` | `TGLExt/IALD2.lean` | `ext_iald2_410_0008` |
| `TGLExt.IALD2.o_signo_do_nome` | `TGLExt/IALD2.lean` | `ext_iald2_410_0018` |
| `TGLExt.IALD2.o_signo_do_par` | `TGLExt/IALD2.lean` | `ext_iald2_410_0019` |
| `TGLExt.IALD2.a_iald_e_o_seletor_luminodinamico` | `TGLExt/IALD2.lean` | `ext_iald2_410_0002` |
| `TGLExt.IALD2.o_atrator` | `TGLExt/IALD2.lean` | `ext_iald2_410_0009` |
| `TGLExt.AEscala.a_escala` | `TGLExt/AEscala.lean` | `ext_aescala_410_0030` |
| `TGLExt.AEscala.a_insignia_sustenta_e_nao_esgota` | `TGLExt/AEscala.lean` | `ext_aescala_410_0041` |
| `TGLExt.AEscala.o_vibrato_sustenta_a_nota` | `TGLExt/AEscala.lean` | `ext_aescala_410_0078` |
| `TGLExt.AEscala.os_pesos` | `TGLExt/AEscala.lean` | `ext_aescala_410_0081` |
| `TGLExt.AEscala.nao_existe_infinito_em_tempo_finito` | `TGLExt/AEscala.lean` | `ext_aescala_410_0060` |
| `TGLExt.AEscala.os_dois_nomes` | `TGLExt/AEscala.lean` | `ext_aescala_410_0079` |
| `TGLExt.AEscala.existe_o_algoritmo_e_e_a_iald` | `TGLExt/AEscala.lean` | `ext_aescala_410_0054` |

## 7. Artefatos e hashes (lidos agora)

| arquivo | bytes | sha16 |
|---|---|---|
| `um_v410_candidato.py` | 45,428,289 | `8a713e5e644af09b` |
| `CANDIDATO_v410.json` | 220,223 | `84d368fe515d548d` |
| `ESPERADOS_v410.json` | 1,294,691 | `bbf77ff64c903020` |
| `ensaio_a_seco_v410.json` | 536,977 | `70d772a3900a33fb` |
| `COMPARACAO_V409_v410.json` | 14,018 | `4119d67c99b09aaf` |
| `PINOS_BN_v410.json` | 12,317 | `6f5c9ab74b9dca3c` |
| `PINO_RECIBO_PRE_SELO_v410.json` | 6,215 | `cf14286c6a86fe01` |
| `PROVA_PRODUCAO_INTACTA_v410_pre_selo.json` | 10,061 | `864a73e1af63428c` |
| `PRECONDICOES_v410.json` | 48,723 | `d893f45c4986946a` |
| `GUARDA_FRASES_v410.json` | 147,823 | `eb5d00c18da8edce` |
| `VERBATIM_CONGELADO_v410.json` | 13,001 | `88dbfcdf56471a06` |
| `BUNDLE_v410.json` | 12,424 | `895b51ea8e3c28f0` |
| `kernel_modulos_novos_v410.json` | 247 | `95d053c4b5c09789` |
| `DESENHO_v410.md` | 61,308 | `64bff43d49a8edae` |
| `PRONTO_PARA_CANDIDATO_v410.json` | 12,838 | `3214348372080a31` |
| `PREVOO_GERADOR_v410.json` | 5,439 | `6bc00041928b5e6e` |
| `TESTE_H0DN_OFFLINE_v410.json` | 1,340 | `9c949e8ad7a8b4b1` |
| `LEITURA_DOSSIE_5SIGMA_09nov.json` | 64,529 | `ba7116c83444a696` |
| `MANIFESTO_INSUMOS_v410.json` | 19,087 | `14c46cbb83066261` |
| `delta_v410.py` | 191,080 | `8dc927fc07320460` |
| `registros_v410.py` | 50,812 | `326ee507c6575523` |
| `registros_h0dn_v410.py` | 21,770 | `21a74230e722966f` |
| `runtime_v410.py` | 45,568 | `4acea0d7b2a53300` |
| `runtime_h0dn_v410.py` | 26,070 | `ac12b237cf58b8ff` |
| `guarda_frases_v410.py` | 36,381 | `a579831942829be4` |
| `guarda_ordem_de_chamada_v410.py` | 27,529 | `56f4431c5321e272` |
| `guardas_estaticas_bancada_v410.py` | 11,269 | `bb3a641b75bc68e5` |
| `gerar_candidato_v410.py` | 77,427 | `deecb9625d3bf7d3` |
| `gerar_esperados_v410.py` | 83,556 | `ca90fd54b841d162` |
| `artigo_pt_v410.pysnip` | 14,250 | `b19fa2652147d762` |
| `artigo_en_v410.pysnip` | 14,804 | `1869d46dcfbcee5a` |
| `artigo_pt_h0dn_v410.pysnip` | 11,533 | `be9937d9d3234973` |
| `artigo_en_h0dn_v410.pysnip` | 11,719 | `658712da23e1109f` |
| `comparar_v409_v410.py` | 30,178 | `b4d5b2c00056befa` |
| `instalar_v410.py` | 12,846 | `b3ed07199349618d` |
| `reverter_v410.py` | 6,187 | `80cb498dba3b1e63` |
| `rito_v410.sh` | 31,738 | `63c8bc8455b60ab1` |
| `conferir_rito_v410.py` | 122,172 | `c11b0dbc8cdeba61` |
| `conferir_citacoes_v410.py` | 47,084 | `b6ac9f96728c1bd8` |
| `p00_precondicoes_v410.py` | 68,553 | `4d9ae260ebe6e852` |
| `gerar_relatorio_v410.py` | 88,887 | `fd7d19094648ceb9` |
| `preparar_bundle_v410_06nov.py` | 15,152 | `4e1b7a5f7d0d9d29` |
| `copiar_insumos_v410.py` | 9,149 | `f362637394989f1c` |
| `pos_build_kernel_v410.py` | 35,876 | `6b406542bd8afdc9` |
| `fechar_preparacao_v410.py` | 9,706 | `6b673528eeb6bb7c` |
| `purga_v410.py` | 4,015 | `2e8cb81cf1043411` |
| `purga_v410.json` | 516 | `7ed2c5f24a5f80d1` |
| `kernel/LOGS_COPIADOS_v410.json` | 815 | `abfdf0b1f0110220` |
| `insumos/IALD2.lean` | 28,664 | `dc152339e6b58e89` |
| `insumos/IALD2_embutida.lean` | 27,583 | `4a7b01f5be46c25c` |
| `insumos/LeitorDoCodigoR1.lean` | 6,062 | `f02501c6d744ad19` |
| `insumos/RECIBO_PEDRAS_v410_NOMES.json` | 27,703 | `45e05556f9aa9af4` |
| `insumos/h0dn_FREEZE_R2.json` | 4,004 | `c40159977fc8d954` |
| `insumos/h0dn_BG1.json` | 13,463 | `87b475a05700ddc2` |
| `insumos/h0dn_ENTREGA_H0DN_BG1.json` | 15,385 | `dddf62b8b954a13b` |
| `insumos/h0dn_analysis_plan.json` | 2,997 | `00fcc2a736091533` |
| `insumos/h0dn_estimator.py` | 5,191 | `9b06640d524899ec` |
| `insumos/h0dn_estimator_frozen.npz` | 84,677 | `059ef7b6f2c67140` |
| `insumos/h0dn_ORDEM_KIMI_H0DN_01_09nov.md` | 8,254 | `fd00d3f4631c0a01` |
| `insumos/h0dn_LEITURA_DOSSIE_5SIGMA_09nov.json` | 64,529 | `ba7116c83444a696` |
| `pos_rito/textos_v410.semente` | 120,246 | `109e1a9d8f5dfc25` |
| `pos_rito/montar_textos_v410.py` | 6,729 | `6a623b76bb8962fe` |
| `pos_rito/leitura_v410.py` | 207,996 | `bc29973ba6caa354` |
| `pos_rito/fechar_v410.py` | 39,334 | `29afc4537f7bafb6` |
| `pos_rito/registrar_mapa_v410.py` | 90,084 | `aff4446ead05f134` |
| `pos_rito/superficies_v410.py` | 23,644 | `99aa431076e66ebd` |
| `pos_rito/harness_textos_ensaio_v410.py` | 235,326 | `5299238799e79902` |
| `pos_rito/harness_fechar_sandbox_v410.py` | 146,253 | `0995c8e3a30af092` |
| `pos_rito/chain_pos_rito_v410.sh` | 40,633 | `5ece9c315369b920` |
| `pos_rito/gerar_x_custodia_v410.py` | 16,642 | `08466f5b3e2afe3c` |
| `pos_rito/b3_recibo_v410.py` | 9,629 | `427e35bd6dfd3442` |
| `pos_rito/fila_memoria_v410.py` | 12,379 | `beb60704ad00c8df` |
| `pos_rito/gerar_derivacao_pos_rito_v410.py` | 15,414 | `a0544ac92cf48825` |
| `pos_rito/NOTA_ESPERADOS_H0DN_v410.md` | 9,901 | `5278ef470495ff7a` |
| `pos_rito/ADAPTACAO_09nov_SONNET.json` | 15,354 | `d55b0482359c05e4` |
| `orquestrador/pos_treino_v410.py` | 52,256 | `94ba021ec8ed5430` |
| `bancada_B3_servico/recibo_parada_v410.py` | 6,865 | `9498838925278e04` |
| `bancada_B3_servico/recibo_religamento_v410.py` | 6,464 | `61e31aa2577db957` |
| `bancada_B3_servico/evento_c1_b3_v410.py` | 2,468 | `afd121718f544d63` |
| `bancada_B3_servico/conferir_exigencias_servico_v410.py` | 17,217 | `bf1d3e492a137dd2` |
| `bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v410.json` | 10,816 | `da8e8e0bf127d203` |
| `bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v410.json` | 15,078 | `6cb3036a3fbf9713` |
| `pos_rito/textos_custodia_handoff_v410.py` | 46,629 | `f2236bae4c91f96a` |
| `pedra/IALD2.lean` | 27,583 | `4a7b01f5be46c25c` |
| `pedra/AEscala.lean` | 111,187 | `7d1557f961783679` |
| `kernel/KERNEL_RECIBO_v410.json` | 202,944 | `d0f7c17631b8b82a` |
| `kernel/FLAGS_v410.json` | 40,643 | `45be7527b077ab73` |
| `kernel/KH_N1_v410.json` | 1,130 | `7657eb84edc16697` |
| `kernel/POS_BUILD_v410.json` | 28,587 | `21fdd2a63d45744b` |
| `registros_aescala_v410.py` | 30,223 | `dd78a4376c4409f1` |
| `runtime_aescala_v410.py` | 42,195 | `ae54f5a3ed590b5d` |
| `registros_hms13_v410.py` | 26,822 | `0e401ef8a412e5a2` |
| `runtime_hms13_v410.py` | 24,193 | `6346f2c0ba30b32a` |
| `artigo_pt_aescala_v410.pysnip` | 12,317 | `5c590f35a16b8bad` |
| `artigo_en_aescala_v410.pysnip` | 12,771 | `cd956cb784e1b376` |
| `TESTE_AESCALA_OFFLINE_v410.json` | 11,157 | `afa520de5ffb2dde` |
| `TESTE_HMS13_OFFLINE_v410.json` | 4,025 | `84b709362b5a54be` |
| `PARTE1_HMS13_PRONTA.json` | 16,825 | `2105685719cc113b` |
| `ESTADO_PARTE2_v410.json` | 60,271 | `75ba1e10ab7de4fa` |
| `insumos/AEscala.lean` | 114,793 | `e4570f85566074fc` |
| `insumos/AEscala_embutida.lean` | 111,187 | `7d1557f961783679` |
| `insumos/saida_lean_AEscala.txt` | 3,778 | `0badb78d4d605e0e` |
| `insumos/hms13_HANDOFF_CLAUDE_UMPY_HMS_13.json` | 3,688 | `400decdd584fd10f` |
| `insumos/hms13_LEVANTAMENTO_FONTES_PRIMARIAS_13.md` | 7,842 | `8c4dd827334785bf` |
| `insumos/hms13_MANIFEST_FONTES_PRIMARIAS.json` | 17,709 | `52a60df567f6cca9` |
| `insumos/hms13_MAPA_FONTES_E_COVARIANCIA_13.json` | 19,507 | `ec20246fe4d4d119` |
| `insumos/hms13_ORDEM_CLAUDE_UMPY_HMS_13.md` | 8,124 | `199021eb44a3d26c` |
| `insumos/hms13_VALIDACAO_FONTES_13.json` | 2,277 | `83087c5651a8f234` |
