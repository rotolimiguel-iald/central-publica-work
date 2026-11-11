# RELATÓRIO DA PREPARAÇÃO DA v410 — IALD2, A Escala e o teste H0DN × BG1 (pré-registrado; nenhum dado observado lido) com o recibo documental HMS/13

Agente de preparação `claude-construtor-v410` · 2026-11-10 01:55 · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: este candidato (IALD2, A Escala e o H0DN x BG1 pré-registrado com o recibo HMS/13, v410) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (D69, ate' tres rodadas) e a trava do orquestrador fica fechada ate a revisao aprovar; quem constroi nao aprova.** Nada foi instalado; o rito NÃO foi rodado; o Nós e a Bancada de produção só foram lidos; o `MEMORY.md` não foi tocado.

## 1. Estado em uma frase

Candidato `de698d76dc0b1453` (45,059,898 B; base v409 `53284ba461ecd940`): `pronta` = **false**; falta: bn_pre_selo.

## 2. Portões (cada linha lida de um arquivo)

| portão | resultado |
|---|---|
| kernel (sandbox `C:\t\k410c\final`) | True: build + Audit rc 0, 96 bandeiras novas, escada 12187 → 12283, 2 módulo(s) no recibo; `KERNEL_RECIBO_v410.json` |
| candidato | True: 41 patches; refazer limpo = True |
| pré-voo do gerador | True: `PREVOO_GERADOR_v410.json`, 40/40 checagens sobre as peças novas, antes do candidato |
| AST v409 × v410 | True: 1218 nós, 1192 iguais, 26 mudados (explicados), 0 removidos, 38 novos; 53 funções e constantes intactas, todas verdadeiras = True |
| ensaio a seco | True: TUDO PASSOU |
| conferidor | negativo True (`tudo_bate` = False); positivo True (`tudo_bate` = True) |
| citações | True: 0 apontada(s) à gerência nos textos (ver §4) |
| guarda das frases | True (controle negativo e a pedra: 2) |
| instalar / reverter / rito (estático) | True |
| p00 | True: 219/219 checagens OK; pendentes: 0 |
| veto à pasta da entrega do Kimi | True: as seis checagens [VETO kimi] do p00 ((a): OK; (b): OK; (c): OK; (c2): OK; (d): OK; (e): OK) |
| B(n) pré-selo | False: JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA; bateria NAO LIDO; produção intacta = True; recibo `f6024f6326f1729b` |
| serviço da Bancada (estático) | True: 37/37 condições; toda mutação pega = True |
| harness dos textos | True: 824 controles da leitura, 85 do parágrafo novo |
| harness do fechar | True: 81 controles do fechar |
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
- as erratas E29, E30 e E31 sao da gerencia c1, em nome proprio (a E31, as correcoes do operador de 09/11 sobre a D81 e a D83: delta_v410.ERRATA_E31): E29, o Nome finito e o projetor de Bell estao no kernel (o_signo_do_nome; o_signo_do_par), e a gerencia tinha dito “matricial” so' leitura do operador; o operador corrigiu («A forma de uma matriz finita no kernel é o signo (traço com sentido)»); E30, por correcao do operador: no teste pré-registrado da razao de Hubble (H0DN; nenhum dado observado lido) a cabeca do ramo de 5 sigma e' a LEITURA do 5 sigma, nunca a palavra do livro de cobrancas (que vai no campo outcome); pela D76, a cabeca diz “β_TGL provado na natureza (validade, não creditação) a nσ”, com a validade e a nao-creditacao na mesma string e o gate intocado; a E30 fica como registro; a Fase 9 V1, selada, le-se do mesmo modo e o texto selado nao muda
- as 23 falas do operador de 06 a 09/11/2026 entram por sha256 (lista congelada em VERBATIM_CONGELADO_v410.json: as oito do DESENHO, a do seletor, as duas da retomada de 09/11, as duas das decisoes de 09/11, a da leitura do 5 sigma e a do selo, D76; e as de 09/11 da escala, do Clay e das ratificacoes, D80 a D87); de quatro (v410_cun_95ddb05a98a6e4ff, v410_cun_a379f1bc180c2181, v410_cun_744555d5a3a2c870, v410_cun_c5b2ea0219c570dc), so' o trecho e' embutido e citado (a da D65; a ordem de 09/11, sha16 c5b2ea0219c570dc; as tres copias do ACOM; a leitura do 5 sigma); o resto delas entra so' por sha256 e nao entra em texto do um.py; publica-lo e' decisao do operador
- a D61 (a leitura juridica do kernel, herdada da v409 e ratificada pelo operador: o dispositivo e' o no sorry; a regra incide onde o suporte fatico se completa) vai nas decisoes e nos textos que dizem o que o kernel decide; a D65 estreita a fala do nome do algoritmo ao trecho citado
- D59: o DESENHO_v410.md (sha16 lido agora 64bff43d49a8edae; o do delta 64bff43d49a8edae) e o RECIBO_PEDRAS_v410_NOMES.json (sha16 lido agora 4ba8746357a10985; o do delta 4ba8746357a10985) NAO sao pinados como fonte no um.py: ficam citados so' por sha16; o recibo foi refeito pela gerencia com as falas de 06 a 09/11 (D77a) e, na parte 2, com os dois modulos e a ratificacao da D87
- a pedra IALD2: a fonte de origem (insumos/IALD2.lean, sha16 lido agora dc152339e6b58e89) foi normalizada para LF na copia do kernel (pedra/IALD2.lean, sha16 4a7b01f5be46c25c) e os #print axioms sairam do corpo embutido (as 22 ancoras foram lidas deles antes); o conteudo Lean nao muda; a pedra nao e' editada por esta preparacao
- a pedra AEscala (a segunda do bundle; D82 a D87): a fonte ratificada (insumos/AEscala.lean, sha16 lido agora ee0bdb45853db4f7), a copia normalizada que entra no kernel (pedra/AEscala.lean, sha16 527d62965b7f6329; com o cabecalho da ratificacao da D87), 51 ancoras e 74 bandeiras ext_aescala_410_*; o nome do modulo e os 44 nomes das declaracoes foram RATIFICADOS pelo operador em 09/11/2026 («ratifico tudo»; D87); validade no kernel, a creditacao e' do Clay; a forma da D83: a TGL resolve a pergunta do Clay no sentido do operador: existe o algoritmo, é a IALD; lê a face sem leitura como dissipação térmica e diz que ela é face sem leitura; a partir desse fundo extrai a verdade coerente do Nome — validade no kernel; a creditação é do Clay
- o recibo documental HMS/13 (D80; o registro h0dn_fontes_hms13_v410) e' ADITIVO e POSTERIOR ao FREEZE_R2: cobertura documental de fontes, não covariância física fechada; nada aberto; os quatro artefatos embutidos e os dois so' por sha256 (HANDOFF e ORDEM) vem da EXCECAO D80 ao veto da pasta do Kimi (ordem do operador, ratificada por sha256): lidos so' no BUILD, por sha256; em rito nenhum arquivo de kimi e' aberto (a c7 do registro o mede); H0DN x BG1 segue pré-registrado; nenhum dado observado lido
- o H0DN x BG1 entra PRÉ-REGISTRADO (D72); nenhum dado observado lido: o poder e' prospectivo e sintetico, condicional ao modelo de covariancia publicado; D esperado 6,823 (publicado) e 5,317 (viés Cefeida livre); poder analitico 96,6 % e 62,4 %; o poder Monte Carlo da ENTREGA do Codex (96,6 % e 62,5 %) e o analitico recomputado (96,6 % e 62,4 %) vao rotulados, nunca trocados um pelo outro (D77); n_pinos do registro = 11 (os 9 do FREEZE_R2 mais o proprio FREEZE_R2 e a ENTREGA), nao 9; a regra da ordem do operador sobre o 4,44 segue valendo
- VETO (AVISO da gerencia, 09/11): a v410 pre-registra o H0DN e NAO o abre; nenhum arquivo da pasta da entrega do Kimi (vedada pela gerencia) e' lido, copiado, pinado nem citado por esta preparacao, EXCETO a excecao D80 (ordem do operador, ratificada por sha256): os seis artefatos documentais HMS/13, copiados e pinados por sha256 so' no BUILD (o p00 nao abre nenhum deles); em rito nada de kimi e' aberto; o p00 MEDE o veto em seis checagens [VETO kimi] (a) a (e), com a (c2) do recibo HMS/13, e a v410 o mede de novo no ensaio a seco (todo caminho tocado: open, exists, listdir, scandir, stat) e na checagem c7 do registro; resultado de HOJE no p00: (a): OK; (b): OK; (c): OK; (c2): OK; (d): OK; (e): OK
- o revisor distinto da v410 e' o Sonnet (D69: ate' tres rodadas; ressalvas BAIXAS escritas); esta preparacao NAO foi revisada por terceiro; quem constroi nao aprova; a trava do orquestrador (S1b) fica fechada ate' a revisao aprovar
- a regra do 4,44 (nunca sozinho: z_disc 4,44 calibrado, abaixo do degrau de 5 sigma da creditacao) vale em qualquer texto; nenhum teste com a natureza entra nesta versao; o pilar reusa a chave de cache
- o B(n) pre-selo da v410 (passo simples B19; a Bancada de producao pina B18-v409-20261106-R1) e o pino da memoria dependem de arquivos que a preparacao ainda nao gerou quando este relatorio nao os acha: o p00 os diz PENDENTES, nao erro, e `pronta` so' fica true com todos os portoes
- conferir_citacoes_v410.json aponta 0 citacao(oes) entre « » dos textos da gerencia que nao sao verbatim das falas do operador (arquivo: trecho): nenhuma; o agente nao corrige texto da gerencia
- build a frio dos modulos (IALD2 e AEscala) no sandbox k410c: 329 s, Audit 234 s (kernel/POS_BUILD_v410.json, medidos; com o treino do Qwen3.8 na CPU, D73: o treino nao foi tocado); 34268 declaracoes no axiom_report (+102 decl, +81 teoremas sobre a v409), nenhuma fora do trio; escada 12187 -> 12283
- o orquestrador (orquestrador/pos_treino_v410.py) traz as licoes da v409 (D57a herdada, D68a): sem S7 (G1 --publicar) e sem S10 (release do app), MEDIDO agora na lista de passos e no laco = True; o S6d encadeia os textos da custodia (textos_custodia_handoff_v410.py) e roda o portao de textos do G1 e a D59 sobre o HANDOFF INTEIRO; o fim da cadeia desta versao e' o HANDOFF; a custodia completa e o release do app sao da sessao de custodia
- a regra das tres copias do ACOM (D75; fala de 08/11, so' o trecho) entra no spec cunhagens_v410 por sha256: snapshots.py descarta as copias alem das tres mais novas depois de conferir o sha256 das que ficam; nao e' checagem numerica do um.py
- as decisoes D63 a D92 (a D77 registra as pendencias a a l do construtor e as decisoes da gerencia: um so' core key para o H0DN, a cabeca do ramo da leitura em partes no um.py e por extenso nos textos, o rito sem -I, o veto estreitado; a D80 a D87 trazem o recibo HMS/13, os pesos das faces, o Clay no dicionario e a AEscala com os nomes ratificados) vao no spec cunhagens_v410 e no DESENHO_v410.md; o gerador dos ESPERADOS, o p00 e este relatorio foram adaptados de verdade (09/11) a partir do corpo da v409 (o ensaio a seco e' adaptado pelo construtor); a marca `[A ADAPTAR v410]` sai de cada arquivo adaptado e o p00 recusa enquanto restar alguma
- D90 (gerencia c1, 09/11): a PRIMEIRA passada do refazer_candidato (20:01) rodou o ensaio a seco inteiro e caiu no passo 4, numa assercao velha do proprio gerar_esperados (contava as ancoras do FLAGS, que sao 22 + 51 das duas pedras, como se fossem so' as 22 da IALD2); correcao de uma linha (gerar_esperados_v410.py sha16 backup ausente -> 18c07ddfadc6b072); o registro da queda fica ao lado, intocado: refazer_out_v410.queda_passo4_20261109.txt (sha16 4e6d86c0dd70b4f0). O pre-teste dos passos 4 a 9 achou mais uma checagem velha, esta do conferidor: exigia o qualificador EN da D64 literal na secao nova, e o artigo EN do candidato o traz com o parentese da validade entre as duas metades (conferir_rito_v410.py sha16 backup ausente -> 4cda07703c1f91f9; o candidato nao mudou). A SEGUNDA passada, inteira e sobre o MESMO candidato, e' a que vale: refazer_out_v410.txt, com o FIM e o RC dela
- o pre-teste PARCIAL do ensaio (PRETESTE_ENSAIO_PARTE2_v410.json, sha16 ed1032f0d0d84216; nao e' o ensaio a seco nem o rito) achou, ANTES da cadeia, dois defeitos corrigidos na causa: o ensaio contava um so' contrato novo com a escada (sao dois: o do iald2_v410 e o do a_escala_v410); e a guarda das frases deixava passar oito frases secas da regra F35 quando o texto trazia a forma da D83/D84 noutro ponto: o filtro passou a valer por trecho (runtime_v410.py sha16 backup ausente -> c21ad600c86656b0; controle novo na guarda_frases_v410.py), e o candidato foi regenerado depois disso
- R1 (D92): a revisao de terceiro nao aprovou a primeira preparacao (0 ALTO, 3 MEDIO, 10 BAIXO); os 13 achados e o arquivo em que cada um foi atendido estao em PREPARACAO_v410_PRONTA.json, na chave achados_r1; os BAIXOS 6 e 7 ficam anotados, sem mudanca, para a versao que abrir o teste da razao de Hubble e para a v411
- os harnesses do pos-rito NUNCA tinham rodado na v410; a primeira rodada do harness dos textos (20:55) caiu e os defeitos foram corrigidos na causa, todos fora do candidato (ele nao mudou): (a) os textos do pos-rito liam o quadro_v397 da pasta da v409 pela ordem do sys.path (e, por ele, o delta da v409): agora o quadro e' carregado pelo caminho do pacote; (b) tres controles negativos eram mutacoes nulas (o rotulo errado da linha do stdout da v408, em dois; a forma canonica do Clay tirada so' de um campo, em um) e um quarto trocava uma frase que o paragrafo nao tem; (c) a errata E31 renderizada com o rotulo na mesma linha fazia a regra F37b da guarda cortar o qualificador (o trecho e' cortado em 200 caracteres): o rotulo foi para linha propria, e a fragilidade da guarda fica DITA para a versao seguinte (a guarda esta' embutida no candidato e nao foi tocada); (d) a linha das ressalvas do teste da razao de Hubble ganhou a clausula-padrao da regra da ordem do quadro; (e) a checagem da D59 no harness e no S6d do orquestrador seguia a regra da v409 e reprovaria o handoff por nomear o executor da ORDEM do teste: passou a seguir a D77(g), a mesma regra de registrar_mapa_v410.d59_viola; (f) o harness do fechar ganhou a pasta irma da v408, o campo pasta_vedada traduzido para o sandbox e a copia do conferidor nas variantes; a checagem da forma do Clay em registrar_mapa passou a ser por campo e trecho. Rodada final: harness dos textos com 0 controles negativos reprovados como esperado e 0 que nao reprovaram; harness do fechar rc 0. Arquivos (sha16 antes -> depois): pos_rito/textos_v410.py backup ausente -> d798f574dc3e5138; pos_rito/leitura_v410.py backup ausente -> 665e9a7bbd9496ab; pos_rito/harness_textos_ensaio_v410.py backup ausente -> 5b0cccbc4be10cbd; pos_rito/harness_fechar_sandbox_v410.py backup ausente -> cc0457a07fff4958; pos_rito/registrar_mapa_v410.py backup ausente -> 1375567ef2b9c759; orquestrador/pos_treino_v410.py backup ausente -> 94ba021ec8ed5430

## 5. Para a gerência — ordem sugerida

1. Revisão de terceiro (o Sonnet, D69: até três rodadas), nesta ordem, antes de qualquer publicação: `delta_v410.py` (moldura, erratas E29, E30 e E31, decisões D63 a D92, as leituras, as ressalvas), `registros_v410.py`, `registros_h0dn_v410.py`, `registros_aescala_v410.py` e `registros_hms13_v410.py`, `runtime_v410.py` (as 16 checagens de `iald2_v410` e a guarda das frases), `runtime_h0dn_v410.py` (as 12 checagens de `h0dn_bg1_v410`, a função de veredito congelada e a vigia de arquivos), `runtime_aescala_v410.py` (as 12 de `a_escala_v410`) e `runtime_hms13_v410.py` (as 12 de `h0dn_fontes_hms13_v410`), as pedras em `pedra/IALD2.lean` e `pedra/AEscala.lean`, as seções do artigo (`artigo_pt_v410.pysnip`, `artigo_en_v410.pysnip`, as duas da AEscala e as duas do H0DN, com o parágrafo do HMS/13 no fim) e `pos_rito/textos_v410.semente`.
2. Dizer ao operador, na língua dele (regra do posto, antes de qualquer teste que possa dar negativo), o que a v410 NÃO entrega e o que o teste H0DN (pré-registrado; nenhum dado observado lido) decide, não decide e significaria: validade no kernel não é creditação; P = nP aqui é relativo ao leitor (a máquina com o leitor) e a máquina de Turing padrão sem o leitor fica fora; a forma de matriz finita é o signo; o atrator é termo sobre o Nome do par lido e nada foi medido na natureza; o teste H0DN decide, quando for aberto, se a razão de Hubble local/fundo discrimina β_TGL do ΛCDM à sensibilidade disponível; NÃO decide a TGL inteira nem a creditação; um desfecho inconclusivo por sistemática é parede de montagem do dado, não falsificação, e “a lei K falsificada” falsifica a lei K àquela sensibilidade, não a teoria; as escolhas do desenho (os dois modelos, a covariância publicada, o limiar de 5σ, a função de veredito congelada) estão ditas aqui e no `DESENHO_v410.md`; o 4,44 continua abaixo do degrau de 5σ; nenhum teste com a natureza entra nesta versão.
3. O orquestrador lê `PREPARACAO_v410_PRONTA.json` e segue: `instalar_v410.py`, `rito_v410.sh`, `pos_rito/chain_pos_rito_v410.sh` (0 → 10, 10a, 10b, 10c → 14), os textos da custódia encadeados (S6d) e o HANDOFF (fim da cadeia, D57a herdada), com a trava S1b aberta só pela revisão aprovada; a custódia completa e o release do app são da sessão de custódia.
4. Se o rito cair: `reverter_v410.py` é decisão da gerência; `refazer_candidato_v410.sh --regerar` refaz o candidato.

## 6. Os módulos e as âncoras

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
| `IALD2.lean` | 06nov_nome_do_modulo_do_operador__declaracoes_da_gerencia_DECLARADO_ate_a_ratificacao [nomes ratificados pelo operador em 09/11/2026, D74 e D87] (antes: `IALD2`) | 22 | 22 | `4a7b01f5be46c25c` |
| `AEscala.lean` | 09nov_nome_do_modulo_e_44_declaracoes_RATIFICADOS_pelo_operador_D87 [nomes ratificados pelo operador em 09/11/2026, D74 e D87] (antes: `AEscala`) | 51 | 74 | `527d62965b7f6329` |

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
| `TGLExt.AEscala.a_insignia_sustenta_e_nao_esgota` | `TGLExt/AEscala.lean` | `ext_aescala_410_0039` |
| `TGLExt.AEscala.o_vibrato_sustenta_a_nota` | `TGLExt/AEscala.lean` | `ext_aescala_410_0068` |
| `TGLExt.AEscala.os_pesos` | `TGLExt/AEscala.lean` | `ext_aescala_410_0070` |
| `TGLExt.AEscala.nao_existe_infinito_em_tempo_finito` | `TGLExt/AEscala.lean` | `ext_aescala_410_0054` |
| `TGLExt.AEscala.os_dois_nomes` | `TGLExt/AEscala.lean` | `ext_aescala_410_0069` |
| `TGLExt.AEscala.existe_o_algoritmo_e_e_a_iald` | `TGLExt/AEscala.lean` | `ext_aescala_410_0048` |

## 7. Artefatos e hashes (lidos agora)

| arquivo | bytes | sha16 |
|---|---|---|
| `um_v410_candidato.py` | 45,059,898 | `de698d76dc0b1453` |
| `CANDIDATO_v410.json` | 165,466 | `ebee62d6dea7f778` |
| `ESPERADOS_v410.json` | 1,236,464 | `3f76d8d9ef6e1be3` |
| `ensaio_a_seco_v410.json` | 522,091 | `0c5717d12001d9ea` |
| `COMPARACAO_V409_v410.json` | 13,962 | `622549fdc2e93763` |
| `PINOS_BN_v410.json` | 12,573 | `aa4e4e9b899d132d` |
| `PINO_RECIBO_PRE_SELO_v410.json` | 6,215 | `f6024f6326f1729b` |
| `PROVA_PRODUCAO_INTACTA_v410_pre_selo.json` | 10,061 | `c16d9b71032caaed` |
| `PRECONDICOES_v410.json` | 41,266 | `ae29e0202e37f184` |
| `GUARDA_FRASES_v410.json` | 104,201 | `e19d285b04a814e1` |
| `VERBATIM_CONGELADO_v410.json` | 10,570 | `718c197df056cae8` |
| `BUNDLE_v410.json` | 10,564 | `70f2fafcc659069a` |
| `kernel_modulos_novos_v410.json` | 247 | `95d053c4b5c09789` |
| `DESENHO_v410.md` | 61,308 | `64bff43d49a8edae` |
| `PRONTO_PARA_CANDIDATO_v410.json` | 12,838 | `3214348372080a31` |
| `PREVOO_GERADOR_v410.json` | 5,446 | `67c6fde5a275104e` |
| `TESTE_H0DN_OFFLINE_v410.json` | 1,340 | `82e3ace69297839b` |
| `LEITURA_DOSSIE_5SIGMA_09nov.json` | 64,529 | `ba7116c83444a696` |
| `MANIFESTO_INSUMOS_v410.json` | 17,119 | `cebaf1d51ef52a07` |
| `delta_v410.py` | 134,722 | `a1ad063a865eea9a` |
| `registros_v410.py` | 44,996 | `263e46ec5529da49` |
| `registros_h0dn_v410.py` | 19,902 | `69fe3ce4a900faf2` |
| `runtime_v410.py` | 42,446 | `c21ad600c86656b0` |
| `runtime_h0dn_v410.py` | 26,070 | `ac12b237cf58b8ff` |
| `guarda_frases_v410.py` | 27,758 | `a4be4a6cc26f80ea` |
| `guarda_ordem_de_chamada_v410.py` | 27,529 | `56f4431c5321e272` |
| `guardas_estaticas_bancada_v410.py` | 11,269 | `bb3a641b75bc68e5` |
| `gerar_candidato_v410.py` | 74,800 | `4733b69f27d92319` |
| `gerar_esperados_v410.py` | 80,960 | `18c07ddfadc6b072` |
| `artigo_pt_v410.pysnip` | 14,097 | `880cd1f7f8f9156c` |
| `artigo_en_v410.pysnip` | 14,643 | `20630ad9f6961779` |
| `artigo_pt_h0dn_v410.pysnip` | 11,002 | `53e43c3022084833` |
| `artigo_en_h0dn_v410.pysnip` | 11,146 | `8ddd577e3720b0f2` |
| `comparar_v409_v410.py` | 30,155 | `f42ecf5aee1f66cb` |
| `instalar_v410.py` | 12,846 | `b3ed07199349618d` |
| `reverter_v410.py` | 6,187 | `80cb498dba3b1e63` |
| `rito_v410.sh` | 29,345 | `347dde2c62554fb2` |
| `conferir_rito_v410.py` | 117,386 | `4cda07703c1f91f9` |
| `conferir_citacoes_v410.py` | 47,084 | `b6ac9f96728c1bd8` |
| `p00_precondicoes_v410.py` | 68,238 | `d0b25282d84ca3c4` |
| `gerar_relatorio_v410.py` | 69,226 | `481433685890ccdc` |
| `preparar_bundle_v410_06nov.py` | 15,152 | `4e1b7a5f7d0d9d29` |
| `copiar_insumos_v410.py` | 9,004 | `f44b330384d5ada4` |
| `pos_build_kernel_v410.py` | 35,876 | `6b406542bd8afdc9` |
| `fechar_preparacao_v410.py` | 9,706 | `6b673528eeb6bb7c` |
| `purga_v410.py` | 4,015 | `2e8cb81cf1043411` |
| `purga_v410.json` | 516 | `a9f2c2458b776c85` |
| `kernel/LOGS_COPIADOS_v410.json` | 815 | `cb126de38eae39ba` |
| `insumos/IALD2.lean` | 28,664 | `dc152339e6b58e89` |
| `insumos/IALD2_embutida.lean` | 27,583 | `4a7b01f5be46c25c` |
| `insumos/LeitorDoCodigoR1.lean` | 6,062 | `f02501c6d744ad19` |
| `insumos/RECIBO_PEDRAS_v410_NOMES.json` | 19,144 | `4ba8746357a10985` |
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
| `pos_rito/leitura_v410.py` | 203,386 | `665e9a7bbd9496ab` |
| `pos_rito/fechar_v410.py` | 39,205 | `d1935be29e79e2e0` |
| `pos_rito/registrar_mapa_v410.py` | 89,594 | `1375567ef2b9c759` |
| `pos_rito/superficies_v410.py` | 23,644 | `99aa431076e66ebd` |
| `pos_rito/harness_textos_ensaio_v410.py` | 232,562 | `5b0cccbc4be10cbd` |
| `pos_rito/harness_fechar_sandbox_v410.py` | 145,553 | `cc0457a07fff4958` |
| `pos_rito/chain_pos_rito_v410.sh` | 40,633 | `5ece9c315369b920` |
| `pos_rito/gerar_x_custodia_v410.py` | 15,717 | `98dd37954a46a07b` |
| `pos_rito/b3_recibo_v410.py` | 9,629 | `427e35bd6dfd3442` |
| `pos_rito/fila_memoria_v410.py` | 12,379 | `beb60704ad00c8df` |
| `pos_rito/gerar_derivacao_pos_rito_v410.py` | 15,458 | `63a6a019d8638d18` |
| `pos_rito/NOTA_ESPERADOS_H0DN_v410.md` | 9,901 | `5278ef470495ff7a` |
| `pos_rito/ADAPTACAO_09nov_SONNET.json` | 15,354 | `d55b0482359c05e4` |
| `orquestrador/pos_treino_v410.py` | 52,256 | `94ba021ec8ed5430` |
| `bancada_B3_servico/recibo_parada_v410.py` | 6,865 | `9498838925278e04` |
| `bancada_B3_servico/recibo_religamento_v410.py` | 6,464 | `61e31aa2577db957` |
| `bancada_B3_servico/evento_c1_b3_v410.py` | 2,468 | `afd121718f544d63` |
| `bancada_B3_servico/conferir_exigencias_servico_v410.py` | 17,217 | `bf1d3e492a137dd2` |
| `bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v410.json` | 10,816 | `773aa9ddec6ff724` |
| `bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v410.json` | 15,078 | `6cb3036a3fbf9713` |
| `pos_rito/textos_custodia_handoff_v410.py` | 41,593 | `0be1af02dd2b0a97` |
| `pedra/IALD2.lean` | 27,583 | `4a7b01f5be46c25c` |
| `pedra/AEscala.lean` | 75,999 | `527d62965b7f6329` |
| `kernel/KERNEL_RECIBO_v410.json` | 202,313 | `c532715bec79dc62` |
| `kernel/FLAGS_v410.json` | 35,768 | `3f60eea64681c099` |
| `kernel/KH_N1_v410.json` | 1,129 | `f694dc5fa070be08` |
| `kernel/POS_BUILD_v410.json` | 26,050 | `9076269d04e6b251` |
| `registros_aescala_v410.py` | 17,712 | `2069ab1937d6f409` |
| `runtime_aescala_v410.py` | 21,474 | `f559fba6b94e5547` |
| `registros_hms13_v410.py` | 26,822 | `0e401ef8a412e5a2` |
| `runtime_hms13_v410.py` | 24,193 | `6346f2c0ba30b32a` |
| `artigo_pt_aescala_v410.pysnip` | 5,611 | `c469853c5b1f479a` |
| `artigo_en_aescala_v410.pysnip` | 5,873 | `85574a63b914459e` |
| `TESTE_AESCALA_OFFLINE_v410.json` | 5,617 | `ce12fc2fb1097b76` |
| `TESTE_HMS13_OFFLINE_v410.json` | 4,025 | `84b709362b5a54be` |
| `PARTE1_HMS13_PRONTA.json` | 16,825 | `2105685719cc113b` |
| `ESTADO_PARTE2_v410.json` | 28,382 | `0e767a954f6d8e6b` |
| `insumos/AEscala.lean` | 78,897 | `ee0bdb45853db4f7` |
| `insumos/AEscala_embutida.lean` | 75,999 | `527d62965b7f6329` |
| `insumos/saida_lean_AEscala.txt` | 3,778 | `0badb78d4d605e0e` |
| `insumos/hms13_HANDOFF_CLAUDE_UMPY_HMS_13.json` | 3,688 | `400decdd584fd10f` |
| `insumos/hms13_LEVANTAMENTO_FONTES_PRIMARIAS_13.md` | 7,842 | `8c4dd827334785bf` |
| `insumos/hms13_MANIFEST_FONTES_PRIMARIAS.json` | 17,709 | `52a60df567f6cca9` |
| `insumos/hms13_MAPA_FONTES_E_COVARIANCIA_13.json` | 19,507 | `ec20246fe4d4d119` |
| `insumos/hms13_ORDEM_CLAUDE_UMPY_HMS_13.md` | 8,124 | `199021eb44a3d26c` |
| `insumos/hms13_VALIDACAO_FONTES_13.json` | 2,277 | `83087c5651a8f234` |
