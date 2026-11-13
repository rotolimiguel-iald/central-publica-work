# REVISAO DE TERCEIRO v411 - R1 - ESCOPO B (os textos rendidos)

Revisor: Claude Sonnet 5.5 (nao construiu a v411). Quando: 2026-11-12T18:55:15. Candidato no inicio e no fim: 21e87eb3df5098f8 / 21e87eb3df5098f8 (mudou: False).

**Resultado: aprovada = False** (ALTO 1, MEDIO 2, BAIXO 6).

## Achados

### B-01 - ALTO
- **onde:** um_absoluto_pt.txt:155 (Os estresses) e :157 (O esperado pelos agregados); um_absoluto_en.txt:155 e :157; fonte quadro_v411.py l.174-177 (PT) e l.199-202 (EN)
- **o que:** Dois blocos da secao nova trazem o Z do primario contra o nulo (6,11 observado, 5,83 esperado; 6,09, 5,56 a 6,66 e 4,73 a 7,48 sob estresse) sem 'sob o modelo de erros publicado', sem 'validade, nao creditacao' e sem 'retrodicao' e 'nao cego' no mesmo bloco. A promessa do cabecalho do quadro_v411.py (em todo bloco onde o primario aparece estao as quatro obrigacoes) e a F67 do DESENHO secao 4 (mesmo paragrafo ou bloco) nao se cumprem; o pedido (regra 4) poe o primario sem os quatro obrigatorios como ALTO.
- **evidencia:** b_02_obrigatorios.py e b_02g.py: nos paragrafos PT @25130 e @25493 (EN @26480 e @26859) faltam a_modelo, c_validade, d_retro, d_naocego; o paragrafo @25493 contem a cadeia 6,11 e o rotulo primario_publicado_13_fora. b_02h.py: guarda_frases_v411.violacoes() devolve [] para as linhas 8 e 9 de amostras_quadro_v411/secao_pt.tex e secao_en.tex.
- **correcao pedida:** Em _v411_secao_tex (quadro_v411.py l.174-177 PT e l.199-202 EN), acrescentar ao fim dos dois blocos a cola das quatro obrigacoes montada dos mesmos textos fixos do quadro (sob o modelo de erros publicado; as Cefeidas livres com o numero 4,38 lido do core; retrodicao sem ajuste, teste nao cego; validade, nao creditacao), ou fundir os dois blocos ao bloco O resultado. Regerar o candidato e o ensaio.

### B-02 - MEDIO
- **onde:** runtime_h0dn_v411.py:54-55 (variavel gat_ da F67); a mesma funcao embutida no candidato; guarda_frases_v411.py (controle_negativo)
- **o que:** A F67 nao dispara sobre o Z contra o nulo escrito em TeX: o disparador pede Z, espaco, contra o nulo, e o fonte traz cifrao entre o Z e a palavra. So o termo primario antes de contra o nulo (ate 160 caracteres) salva o quadro e o bloco do resultado. A checagem existe, passa, e nao recusa o caso que deveria (e e por isso que o B-01 passou pela guarda e pela c16). Idem EN (Z against the null).
- **evidencia:** b_02h.py: violacoes('Z contra o nulo = 6,11 no H0DN') = F67; violacoes('$Z$ contra o nulo $=6{,}11$ no H0DN') = []; violacoes('$Z$ against the null $=6.11$ in H0DN') = []; as linhas do esperado e dos estresses de secao_pt.tex e secao_en.tex dao [].
- **correcao pedida:** Tornar o disparador tolerante ao cifrao (aceitar Z, opcionalmente cifrao, espaco, contra o nulo; e o equivalente no EN) e acrescentar ao controle_negativo() de guarda_frases_v411.py uma frase proibida em TeX e uma limpa em TeX (com as quatro). Como a funcao e a mesma embutida no um.py, a mudanca entra no candidato; refazer o controle da c16.

### B-03 - MEDIO
- **onde:** um_absoluto_pt.txt:206-215 (secao O teste pre-registrado da razao de Hubble com a rede de distancias, texto da v410, sem versao no cabecalho); um_absoluto_en.txt:206-215; .md l.139 (esta com rotulo v410)
- **o que:** O texto herdado da v410 vai identico para o artigo v411 e diz o contrario do que a secao nova (e o rito) dizem: nenhum dado observado lido (o um.py nao le vetor observado); a abertura e de versao futura; esta versao roda sem o resultado do teste; o um.py nao le esse vetor; e que o vetor fora do suporte e parede de montagem do dado. Esta ultima e a leitura que a F62 do DESENHO secao 4 proibe e que o achado da gerencia de 11/11 e a emenda D162 superaram. No PT e no EN o cabecalho da secao nao leva v410 e nenhuma errata (E41, E42, E43) cobre as frases; a secao 5.2 so diz o que a v410 tinha pre-registrado, sem apontar essas frases. (No .md a linha esta rotulada v410: fica claro.)
- **evidencia:** b_02c.py, b_02e.py, b_03f.py: as frases em PT :213-215 e EN :213-215. b_09c.py e b_09e.py: o paragrafo e identico ao selado da v410 (258 dos 269 paragrafos antigos alterados so diferem por agrupamento de expoente; os outros 11 sao os listados em B9). b_02f.py: os unicos ao lado da v411 no corpo sao o estatuto (2x) e o P2. b_02i.py: a propria guarda da v411 recusaria o paragrafo :215 (F61 poder_certificado e F67) se fosse texto novo.
- **correcao pedida:** Errata AO LADO, em nome proprio da gerencia (E44), no fim da secao 5.2 PT e EN e na linha H0DN do .md: a secao da v410 O teste pre-registrado da razao de Hubble... e o texto selado da v410; onde diz esta versao, nenhum dado observado lido, a abertura e de versao futura, o um.py nao le esse vetor, e parede de montagem do dado, le-se: estado da v410; na v411 o vetor e lido (embutido, recalculado) e o vetor fora do suporte e propriedade do modelo publicado (D162, E41, achado da gerencia de 11/11), nao erro de montagem. O texto selado da v410 nao e reescrito.

### B-04 - BAIXO
- **onde:** um_absoluto_pt.txt:65 e :103; EN :65 e :103; quadro_v411.py l.325-333; DESENHO 5.1 c
- **o que:** A frase ao lado do estatuto da prova e do item O coracao diz que o elo foi lido e fechado a esta sensibilidade, com as Cefeidas livres so como abaixo de 5 (sem o numero) e sem retrodicao nem teste nao cego no mesmo bloco, nem ponteiro para as sete ressalvas. Nao e gatilho da F67 (nao diz provado na natureza, nem traz Z ou cabeca) e e o texto do DESENHO 5.1 c; o resumo ratificado tambem nao aponta para as sete ressalvas (nao se toca).
- **evidencia:** b_02g.py: nesses blocos faltam b_cefeidas_numero, c_validade, d_retro, d_naocego, e_sete.
- **correcao pedida:** Opcional: acrescentar ao fim da frase ao lado, PT: retrodicao sem ajuste, teste nao cego; as sete ressalvas estao no quadro do topo; EN: retrodiction without fit, test not blind; the seven reservations are in the box at the top.

### B-05 - BAIXO
- **onde:** quadro_v411.py l.66 e l.102-103; registro h0dn_bg1_v411.o_que_o_teste_nao_decide (runtime_h0dn_v411.py l.419)
- **o que:** O que o teste nao decide e um resumo digitado pela gerencia (decisao (d) do DESENHO, aprovada), nao o texto da secao 6 do pre-registro; o registro mede so o numero de itens (5) e o sha256 da secao. O resumo perde a frase da secao 6 de que qualquer teoria que preveja um desvio parecido passaria igual (o ponto central da especificidade).
- **evidencia:** b_05_ressalvas.py: o item 2 da secao 6 traz qualquer teoria que preveja um desvio parecido passaria igual; o resumo do core nao.
- **correcao pedida:** Opcional: acrescentar essa clausula ao item da especificidade (PT) e any theory that predicts a similar deviation would pass equally (EN).

### B-06 - BAIXO
- **onde:** quadro_v411.py l.94 e l.204 (EN); ressalva 7 (secao 9 do pre-registro)
- **o que:** No EN as sete ressalvas (obrigatorias em toda superficie) entram em portugues (o quadro diz in Portuguese): fiel ao arquivo embutido, mas o leitor EN le as obrigatorias num idioma que pode nao ler. A ressalva 7 diz (secao 9), que e a do pre-registro e pode ser lida como a do artigo.
- **evidencia:** b_05_ressalvas.py: as sete do EN sao as do PT, byte a byte.
- **correcao pedida:** Opcional: acrescentar no EN uma versao inglesa marcada como traducao da gerencia, mantendo o original; e dizer (pre-registration, section 9).

### B-07 - BAIXO
- **onde:** conferir_citacoes_v411.py l.77-100 (regra (g) portada da v410: _corpus_um e _corpus_ok)
- **o que:** A regra (g) aceita como verbatim qualquer citacao que seja subcadeia do Atlas, do um.py da base, do adendo, das pedras ou do C:/IALD/CLAUDE.md, e aceita colagens ligadas por reticencias (cada fragmento de 8 ou mais caracteres basta), alem de saltar citacoes curtas ou com + ou %s: nao prova autoria do operador. Vale so para os textos do pos-rito; o escopo do um.py e estrito (falas do operador por bytes) e os rendidos de B passaram nele e no meu teste proprio.
- **evidencia:** b_07c.py: uma frase da gerencia presente em C:/IALD/CLAUDE.md passa em _corpus_um; b_07_aspas.py: 3 citacoes angulares nos textos novos, todas verbatim de OPERADOR_12nov_ratifico...txt (sha256 igual ao TOPO).
- **correcao pedida:** Nenhuma para a v411 (herdada da v410, por ordem da gerencia); o revisor C confere o que passa por ela no pos-rito.

### B-08 - BAIXO
- **onde:** um_absoluto_pt.txt:577 (O que nao se declara, v392) e a linha de registro estatuto_da_prova_v391 (BETA_IN_NATURE_AWAITS_5_SIGMA); EN equivalentes
- **o que:** Mais dois trechos antigos continuam dizendo que beta na natureza a 5 sigma aguarda instrumentos (incluindo a razao de Hubble com a covariancia fixada), sem ao lado da v411: o paragrafo O que nao se declara e a cadeia de maquina da lista de veredictos (chave antiga, nao muda de literal por desenho). O estatuto e o coracao, no topo, tem o ao lado.
- **evidencia:** b_03g.py: contextos em :577; b_09d.py: a linha estatuto_da_prova_v391 so muda o hash.
- **correcao pedida:** Opcional: incluir esses dois pontos na errata E44 (ao lado).

### B-09 - BAIXO
- **onde:** um_absoluto_pt.txt:157 e EN :157 (rotulos primario_publicado_13_fora, ancora_unica_N4258_publicado); quadro_v411.py l.157 e l.182; secao PT/EN em geral
- **o que:** Legibilidade: rotulos de maquina crus (primario_publicado_13_fora) na prosa; os marcadores de espacamento 1pt, 4pt e 0pt aparecem como linhas no TXT (ja existiam na v410: 2, 1 e 3 contra 3, 2 e 4 agora); no EN, datas em dd/mm (09/11, 11/11, 06/11) ao lado de 12 Nov 2026, e the weights ... are hers (a colaboracao) em vez de its. O titulo da secao diz teste decisivo (palavra do operador, D169) na mesma secao que lista o que o teste nao decide.
- **evidencia:** b_12.py; b_02b.py; leitura do quadro_v411.py.
- **correcao pedida:** Opcional. PT: os pesos congelados em 06/11 sao os dela; EN rendido: the weights frozen on 06/11 are hers; EN proposto: the weights frozen on 6 Nov are its (the collaboration's). PT: em 11/11 o operador emendou; EN rendido: On 11/11 the operator amended; EN proposto: On 11 Nov the operator amended.

## Conferencias por item do pedido

- **B1.** OK. b_01_topo.py e b_01d.py: o resumo PT e EN do ensaio e IGUAL ao TOPO_RATIFICADO_v411.json com os 12 marcadores trocados pelos valores do core (comparacao normalizada e por tokens e numeros; so diferem as formas TeX para TXT); formatos: 2 casas, sinal e menos tipografico em Z contra K (-0,61), z_delta (-1,48), n inteiro (6), N e categorias inteiras (11; 6, 2, 2, 1). Nenhuma palavra a mais ou a menos. Painel curto e frase de estado: nao estao em nenhum rendido de B (b_01b.py, b_01f.py); so nos blocos do README/handoff (pos_rito/blocos_custodia_v411.py): fica ao revisor C (C7).
- **B2.** ACHADOS B-01 (ALTO), B-02 (MEDIO), B-04 (BAIXO). b_02_obrigatorios.py, b_02g.py (saida em C:/t/k411c/revisao_B/b02_resultado.json): resumo, quadro item 1, secao 5.2 O resultado, Origem, P2 ao lado, O metodo e a linha de maquina (manifesto e stdout) trazem as quatro (o resumo EN diz under the error model published by the collaboration, aceito: ratificado). O stdout (b_03e.py) traz as quatro no mesmo bloco. Os paragrafos da v410 com provado na natureza sem as quatro (:213 e :215) sao texto selado antigo (ver B-03).
- **B3.** OK para texto novo; achado herdado B-03. b_03_proibido.py, b_03c.py, b_03d.py: sondas proprias (confirm, certificad, montagem, cego, evidencia independente, descoberta, pos-dicao, nao provou, beta literal, Clay resolvido, poder certificado) sobre PT, EN, md, manifesto e stdout contra a v410 selada e sobre todos os paragrafos novos ou alterados: nenhuma ocorrencia nova fora da negacao, do nome da convencao dos 5 sigma (criterio de descoberta, discovery criterion) e da fala verbatim; nenhum beta literal novo (o 1.20313004x10^-2 do metodo e impresso do runtime e ja existia).
- **B4.** OK. b_04b.py, b_04c.py: 17 decimais do quadro PT e 17 do EN casados com h0dn_bg1_v411.values no arredondamento do TOPO; PT == EN == MD token a token; secao PT == EN; stdout em precisao cheia (6.1057575347088955 etc.) arredonda para os mesmos; commits 769fcb2697d8 e f24d954a3b90 e horas conferem com os dois recibos da custodia (b_04_numeros.py). Os numeros digitados no texto da secao (72, 111, 37, 13, 90 por cento) conferem com o pre-registro.
- **B5.** OK. b_05_ressalvas.py: as sete ressalvas do core sao iguais as da secao 8 do pre-registro (arquivo sha16 06af740a8812a622, igual ao pino); numeradas no quadro PT (1. a 7.) e EN, na secao 5.2 PT e EN e no .md. O que o teste nao decide e resumo digitado (B-05, BAIXO).
- **B6.** OK. b_06g.py: livro de cobrancas contado por mim em the_ledger_of_charges_v383.ledger: 11 linhas, 0 FALSIFIED, 6 NOT_FALSIFIED, 2 INCONCLUSIVE, 2 AWAITING, 1 EXCLUDED_IN_READING; confere com a frase do topo e com o estatuto_da_prova_v391. b_06h.py: o 4,44 novo (resumo) traz calibrado, abaixo do degrau de 5 sigma, z_delta, ln B que nao e sigma, NOT_FALSIFIED_POWERED e nao e evidencia independente; as demais mencoes sao do texto selado antigo. b_06i.py: a palavra sela so aparece na fala do autor.
- **B7.** OK. b_07_aspas.py: as citacoes angulares dos paragrafos novos (2 PT/EN) e do .md (1) sao verbatim por bytes de OPERADOR_12nov_ratifico_a_formula... (sha256 igual ao do TOPO); b_07b.py: nenhum vocativo, milenio, navier, kimi, leitura do operador, leitura dele ou etiqueta ontologica em texto novo. A regra (g): B-07.
- **B8.** OK, sem alteracao de sentido; BAIXO B-09 e B-06. Titulo do quadro EN, frase ao lado do estatuto EN, secao 5.2 EN e quadro EN lidos lado a lado com o PT e com o fonte quadro_v411.py: fieis, reservations (nao caveats), creditation mantido; accredit e caveat ausentes dos textos novos (b_08a.py).
- **B9.** OK com observacoes. b_09c.py e b_09e.py: dos 269 paragrafos antigos que mudam, 258 so diferem por agrupamento de expoente (A2, DESENHO secao 7: entrou como mudanca contida no conversor para TXT; a medicao esta em A2_MEDIDA_v411.json); os 11 restantes: o resumo (as duas trocas ditas, 5.1 b), O metodo (a troca dita), O selo pela propria tecnologia e A certificacao e o proprio codigo (tamanho e hash lidos do arquivo), a Introducao e o titulo (v384 a v411), 436 chaves (433 mais 3 novas), a linha estatuto_da_prova_v391 (so o hash proprio), e DOIS que nao sao troca dita: o paragrafo de Spohn (A descida em unidades do custo: numeros 0.3002, 0.2324, 0.1841 viram --, --, --) e a linha interface_is_light (PENDING_FORM_CONTENT vira VERIFIED). Os dois vem do ensaio a seco (b_09f.py, b_09g.py, b_09h.py): o codigo usa _satf.get(1, nan) com chaves inteiras e o core do ensaio vem de JSON (chaves texto); e o runtime em memoria da v410 dizia PENDING enquanto o core JSON diz VERIFIED. Esperado no rito real: iguais a v410 [inferencia minha, nao medida]. Linhas do .md: 5 antigas somem (versao, hash, tabela, contagem) e 17 novas, todas ditas.
- **B10.** OK. b_10_p18.py rodado sobre a funcao _v411_p18_sem_cabeca e a _v392_guarda_texto EXTRAIDAS DO CANDIDATO: a exata sai; a exata escapada para TeX sai; um caractere trocado recusado; a crua recusada (R1); outro n recusado; mais controles meus: cabeca truncada recusada, cabeca mais palavra proibida recusada, texto comum com palavra proibida recusado, e o texto limpo passa. Uma funcao so; a cabeca montada do literal e igual a cabeca do core.
- **B11.** OK. b_11_pnp.py: o unico P = nP novo e o do resumo ratificado: traz relativo ao leitor (a maquina com o leitor), a maquina de Turing padrao sem o leitor fica fora, validade nao creditacao, e a pergunta do Clay tal qual apresentada pela TGL, resolvida no kernel, com a creditacao de quem fala em nome do Clay; nenhum Clay resolvido seco; a frase canonica da D84 segue intacta no texto antigo (2 ocorrencias PT e EN).
- **B12.** OK. b_12.py: PT, EN e md: quadro acima de O Teste da Unica Palavra (que fica, com a linha de remissao logo apos o seu quadro); secao nova (PT :140) antes de IALD ao quadrado e da secao H0DN da v410, com as 11 partes da 5.2 e titulo igual ao do DESENHO em PT e EN; linha H0DN x BG1 ABERTO (v411, 12/11/2026) no .md antes da IALD2 (v410). Sumario (.toc) e PDF PT (paginas 1-4 por texto, pagina 2 por imagem) com o quadro, a secao e as sete ressalvas.

## Nao verificado

- Painel curto e frase de estado do TOPO: nao existem em nenhum rendido do escopo B; sao do handoff/README (pos_rito/blocos_custodia_v411.py; HARNESS_TEXTOS_ENSAIO_v411.json nao guarda os textos): ficam ao revisor C (C7).
- Os rendidos sao do ensaio a seco (emulado): o manifesto tem 1012 linhas contra 165859 do real da v410 e o stdout 200 contra 1971; so o bloco do H0DN no stdout e a lista de modulos foram lidos, e o codigo que imprime o bloco (um_v411_candidato.py, main) confere com o emulado. O texto completo do rito real (manifesto, stdout, valores do pilar na GPU) so existe depois do rito.
- Spohn com tres tracos e interface_is_light VERIFIED: causas lidas no codigo e no core, mas a igualdade com a v410 no rito real e inferencia minha.
- PDF: so o PT paginas 1-4 por texto e a pagina 2 por imagem; o PDF EN, a secao 5.2 em PDF e o restante nao foram conferidos visualmente; pdflatex nao foi reexecutado (vedado).
- A regeneracao com as correcoes B-01 a B-03 nao foi feita (nao edito arquivos da cadeia); o efeito delas no candidato e nos conferidores (c16, conferir_rito) fica para a rodada de conserto.
- As 11 cobrancas, o 4,44 e o restante do corpo antigo (Fase 9 V2, livro) nao foram reabertos: so contei o livro no core e conferi as mencoes novas.

## Arquivos revisados (sha16)

- `quadro_v411.py` `67c95796bcab3965`
- `topo_com_resultado_v411.py` `edc590f6fc5a811d`
- `guarda_frases_v411.py` `98a9039c6def1a69`
- `guarda_p18_v411.py` `ef0cee5097564b8e`
- `conferir_citacoes_v411.py` `adcf9470460291f4`
- `runtime_h0dn_v411.py` `de32fdbc7b8db32f`
- `um_v411_candidato.py` `21e87eb3df5098f8`
- `TOPO_RATIFICADO_v411.json` `22224f90d68cce9b`
- `DESENHO_v411.md` `931b80adf3557b88`

## Artefatos renderizados lidos (sha16)

- `C:/t/k411c/falso_nos_v411/um_absoluto_pt.txt` `77fe099c381d009a`
- `C:/t/k411c/falso_nos_v411/um_absoluto_en.txt` `6456080fb011e5c1`
- `C:/t/k411c/falso_nos_v411/um_absoluto_forma_canonica.md` `d874c69564c355ff`
- `C:/t/k411c/falso_nos_v411/um_absoluto_manifest.md` `5ebd082fb827ec08`
- `C:/t/k411c/falso_nos_v411/rodada_v411_stdout.txt` `9d3baa156a7add2d`
- `C:/t/k411c/falso_nos_v411/um_absoluto.json` `07f353f19d5a64d8`
- `C:/t/k411c/falso_nos_v411/um_absoluto_pt.pdf` `2c47c561ab886c15`
- `C:/t/k411c/falso_nos_v411/um_absoluto_pt.toc` `4b58f30050d3037a`
- `C:/t/k411c/falso_nos_v411/um_absoluto_en.toc` `912ad2a1275b6137`
- `C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um_absoluto_pt.txt  [v410 selada, so leitura]` `a8924eb6c889bcaf`
- `C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um_absoluto_en.txt  [v410 selada, so leitura]` `c9a383843df10a59`
- `C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um_absoluto_forma_canonica.md  [v410 selada, so leitura]` `6774c43b8d49c347`
- `C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um_absoluto_manifest.md  [v410 selada, so leitura]` `9b040f3ef05bd15a`
- `C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/rodada_v410_stdout.txt  [v410 selada, so leitura]` `9b713973c8162354`
- `C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um_absoluto.json  [v410 selada, so leitura]` `338e7712caa147cd`

## Rotas examinadas (Mapa de Rotas; nao registrei)

- cadeia.preparacao_v411 (EM_CURSO): lido: README projetado com folga de 39 B; nao afeta B
- estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov (EXAMINADA): lido: nao esconder a linha das Cefeidas livres nem a selecao pos-guarda; nao chamar prova absoluta, confirmacao cega ou CONFIRMED (conferido nas sondas B3)
- estatistica.h0dn_bg1.cov_injecoes_06nov (EXAMINADA_COM_DEFEITO): lido: covariancia fisica aberta; nenhum numero novo
- gate.qg_closure (EXAMINADA_COM_DEFEITO): lido: o gate nao e teste e nao discrimina o LCDM raso; NOT_FALSIFIED nunca e a palavra da creditacao
- hubble.fase9_razao_discriminante (EXAMINADA): lido: o 4,44 e da Fase 9; sem efeito em B
- infra.custodia_g1.cabeca_h0dn_p18_12nov (EXAMINADA): listada; B10 refeito por mim sobre o candidato
- umpy.v410.selada_iald2_06nov (EXAMINADA): listada (confronto com a v410 selada no Nos)
