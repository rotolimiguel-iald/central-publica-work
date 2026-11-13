# CONSERTO R1 v411 (rodada unica, D109)

Quando: 2026-11-12T23:04:00. Candidato FINAL (lido do disco): `1203b1f9202020d6`.

## contagem de controles

{
 "guarda_frases (proibidas/limpas/falas pela excecao)": "27/18/11 -> 29/20/11 (+2 proibidas e +2 limpas em TeX, B-02)",
 "guarda_conversa (NOVA)": "no candidato (p00): 6 controles (linha plantada, nome plantado, linha curta alem da base, core com cadeia plantada, core com nome na chave, o limpo passa); nos rendidos do ensaio e do conferidor: 21 (3 por alvo em seis alvos de texto, mais 2 do core, mais o limpo passa) 21 de 21 recusam e o limpo passa",
 "conferidor do rito (itens deve_mudar)": "84 -> 89 (+ conversa, quadro sem a fala do autor, linha da v411 no stdout, falas citadas, PDF e TeX); controles internos novos: 3 (quadro: PT, EN e .md) + 3 (stdout: aspas angulares, linha antiga, sha16 trocado) + 4 (cunhagens: texto, lista fora do desenho, nome de arquivo, sha256 trocado) + 4 reprovacoes e 2 passes (PDF e TeX)",
 "p00 (checagens)": "28 -> 33; controles novos: 3 (C-01: nome inexistente na lista do passo 0, no laco do passo 1, erro de sintaxe) + 1 (C-05: indice de 196+ linhas) + a guarda de conversa",
 "harness dos textos": "variante( no fonte 526 -> 531 (+5: 4 de D181 no lugar de 1 de embedded_ok e 2 de C-04); controles da leitura executados 760 -> 765; paragrafo da v411: 100 -> 100 (o de citacao nao verbatim passou a plantar a citacao); falha( 53 -> 53",
 "harness do fechar": "88 -> 89 (fechar_negativos: a de embedded_ok virou a de citado_por_sha256 e entrou a do texto plantado)",
 "leitura (P.append no fonte)": "170 -> 170 (a condicao verb_ok passou a exigir citadas_ok)",
 "testes sem candidato do pos-rito": "textos 80 etapas e 0 falhas (a primeira execucao depois das minhas mudancas deu 35 falhas por tres causas, todas consertadas: a assercao dos ids das erratas, o F34 do papel do testemunho na lista das ordens citadas e o fixture do paragrafo sem os values do h0dn); mapa PASSOU; textos_custodia 20 ok 0; gatilho 23 casos 20 negativos; blocos 90 ok 0; x_custodia PASSOU"
}

## readme

{
 "medida": "teste_blocos_custodia_v411.py depois do conserto: README 40.921 B (hoje 40.179; liquido +742), teto 40.960, folga 39 B, 90 ok e 0 falha; nenhum texto que vai ao README foi tocado (o painel, a NOTA e as linhas do H0DN sao de blocos_custodia_v411.py e do TOPO)",
 "memory_md": "nao foi tocado; nenhum texto que o pos-rito escreve no indice cresceu (marca_missao e linha_handoff nao mudaram); o p00 projeta 194 linhas e dentro de 24.000 B e passou"
}

## chain

{
 "cadeia_v411.sh": "inteira em modo real (V411_REGERAR=1; o candidato saiu identico), de 22:08:20 a 23:03:25 de 12/11: 21 de 21 linhas rc=0, nenhum PARADO; saida em cadeia_v411_out.txt e C:\\t\\k411c\\conserto_r1\\cadeia_final2_stdout.txt",
 "PREPARACAO_v411_PRONTA.json": {
  "pronta": true,
  "falta": [],
  "portoes": "30 de 30 (29 anteriores + o novo guarda_da_conversa_d181)",
  "p00": {
   "veredito": "TODAS PASSARAM",
   "passaram": 33,
   "n": 33,
   "pendentes": [],
   "sha16": "50be8067b34c84ea"
  },
  "ensaio_a_seco": {
   "veredito": "TUDO PASSOU",
   "sha16_do_candidato": "1203b1f9202020d6",
   "json_sha16": "982039c1845756fb"
  }
 },
 "historico": "a primeira cadeia completa (19:51) parou no passo 15, no harness dos textos (20:28); o fim_de_cadeia avulso seguinte (20:30) passou o harness dos textos e parou no harness do fechar (20:49); causas (todas consertadas): o conferidor do sandbox do fechar nao tinha os modulos novos, o Nos emulado do harness nao tinha os horarios do rito (C-02) e o harness esperava a citacao entre aspas angulares no paragrafo (O4, D181); uma cadeia inteira (20:55:45 a 22:05:12) passou; depois troquei por palavras as aspas angulares de dois textos meus do pos-rito (a regra do pedido) e repeti a cadeia INTEIRA (22:08:20 a 23:03:25): a que vale"
}

## ressalvas que ficam

[
 "B-05 (o resumo do que o teste nao decide e o aprovado; a custodia tem o texto pinado)",
 "B-06 (as sete ressalvas em ingles ficam em portugues no EN)",
 "B-07 (a regra (g) das citacoes do pos-rito)",
 "A-B1 a A-B6 (os seis BAIXOS do revisor A)",
 "C-03 (a cota de 10 s tem margem de cinco vezes nos ritos reais)",
 "C-06 (a gerencia registra o sha16 dos modulos da G1 antes do rito e avisa a custodia)",
 "C-07",
 "C-08 (o reverter nao restaura o artigo: herdado do molde)",
 "C-09 (b) (nota: o teto de 5 h nao encerra a arvore do um.py)"
]

## perguntas para a gerencia

[
 "Os insumos pinados em base64 (o pre-registro publicado e os recibos da abertura: 5 ocorrencias de nomes de arquivo OPERADOR_* por dentro, em 4 blobs) nao mudam sem rebater os pinos de producao: o invariante (iii) e a guarda leem texto em claro (fonte, core, artigo, forma canonica, manifesto, stdout) e esse esta limpo; se a gerencia quer a regra tambem sobre o interior dos blobs, e' decisao dela (re-pin, o que contradiz a publicacao).",
 "O delta_v411.py (casa) continua lendo o texto das falas para a guarda de frases, a conferencia de citacoes e a guarda da conversa; o campo text nunca vai ao candidato, ao core, ao artigo nem a saida do rito. Se a gerencia quer o texto lido SO' pela guarda (nenhum outro script da preparacao), o guarda_frases e o conferir_citacoes teriam de ler dela.",
 "O orquestrador (pos_treino_v411.py) e o PREPARACAO_v411_PRONTA.json citam a ordem de abrir pelo arquivo e pelo sha16; o orquestrador ainda le o texto do arquivo da casa para a frase de autorizacao (AUT_FRASE, superficie de memoria e conferidor estatico do servico): conforme O4, mas nao foi tocado."
]

## nao feito

[
 "fechar_preparacao, acom_inscrever_prep, instalar, rito, orquestrador, tarefa agendada, commit, push, DESENHO, TOPO, memoria, Mapa de Rotas (consultado, nao registrado), kimi\\, o Nos, a pasta da nativa, tools\\custodia_g1\\, Chatgpt\\: vedados e intactos",
 "nenhuma junction nem link simbolico foi criado; as copias de ensaio foram para C:\\t\\k411c\\conserto_r1",
 "o scan do que o pos-rito escreve nas superficies de memoria (ensaio_superficies da pasta do harness) acha as mesmas ocorrencias do Atlas real (conteudo antigo, de sessoes anteriores) e nenhuma a mais: o texto novo da v411 nao transcreve"
]

## itens

### O1 - o registro cunhagens_v411 sem transcricao

- feito: As 11 falas saem do programa e entram como itens CITADOS (quando, sha256 lido do arquivo da casa na construcao, papel da tabela do DESENHO, autor): o motor v392 so' embute texto, entao _V411_VERBATINS2 vai vazio e o _v411_citar_falas poe os itens citados em core[cunhagens_v411].verbatim (citado_por_sha256, texto_transcrito falso) e em extras.falas_citadas; extras.autores passou a ser por chave derivada do sha256 (nao pelo nome do arquivo); a lista das falas FORA do desenho saiu do extras; o veredito do spec passou a OPERATOR_ORDERS_OF_11_AND_12_NOV_CITED_BY_DATE_AND_SHA256_NOT_TRANSCRIBED_11__DECISIONS_..._D181__ERRATA_E41_E42_E43_E44_BESIDE__...; limites, diz e estatuto do spec falam em ordens citadas; o contrato do registro H0DN (fala_da_ordem_de_abrir e falas) leva quando, sha256, papel e autor, sem nome de arquivo. Em rito nada da casa e' lido: a conferencia e' estrutural (conferir_conversa_v411.citadas_ok: 11 itens, sha256 de 64 hex, iguais aos pinos de ESPERADOS).
- controle: guarda_conversa (candidato: 0 achados nas regras a, b e c; controles: linha plantada, nome plantado, linha curta alem da base, core com cadeia plantada e nome na chave: todos recusados); o ensaio a seco e o conferidor repetem sobre os rendidos; o candidato anterior (21e87eb3df5098f8), com as falas embutidas, e RECUSADO pela mesma guarda (10 de 10 falas longas achadas; 33 achados)
- nao feito: os insumos pinados em base64 (o pre-registro publicado e os recibos da abertura) trazem nomes OPERADOR_* por dentro: sao arquivos publicados e pinados por sha256, nao se mexem; a guarda olha o texto do programa, nao o interior desses blobs (ver pergunta no relatorio)
- `delta_v411.py` l.222: antes `f1cbdb9bf6a77040`, depois `8746e98bafa463f9`
- `registros_v411.py` l.27: antes `1f660686c660ead8`, depois `c3cda65a92ad34d3`
- `registros_v411.py` l.65: antes `1f660686c660ead8`, depois `c3cda65a92ad34d3`
- `registros_h0dn_v411.py` l.81: antes `e92972ea402e32d7`, depois `c525b52c5b4f3c34`
- `gerar_candidato_v411.py` l.228: antes `0efeb11822830c37`, depois `2d60e4b9578b763b`
- `gerar_candidato_v411.py` l.296: antes `0efeb11822830c37`, depois `2d60e4b9578b763b`
- `gerar_esperados_v411.py` l.96: antes `cbaf246b3f287763`, depois `c659ea3d27d3a05d`
- `pos_rito/leitura_v411.py` l.246: antes `42261fd74035937b`, depois `d61564af102518e3`

### O2 - a saida do rito cita a ordem de abrir por data e sha16

- feito: A linha da v411 na saida do rito passou a: 'a ordem do operador de 12/11/2026, citada por data e sha16 <16 hex lidos do arquivo da casa>, nao transcrita'; o docstring de h0dn_bg1_v411 idem (o marcador __SHA16_DA_ORDEM_DE_ABRIR__ do fonte e' trocado pelo gerador, lido do arquivo da casa); o docstring do gerador tambem. As linhas das versoes anteriores nao mudam.
- controle: conferir_conversa.linha_v411_do_stdout_ok com tres controles (aspas angulares plantadas, a linha antiga com a fala, sha16 trocado) no conferidor; o stdout do ensaio passa pela guarda da conversa
- `gerar_candidato_v411.py` l.196: antes `0efeb11822830c37`, depois `2d60e4b9578b763b`
- `runtime_h0dn_v411.py` l.413: antes `de32fdbc7b8db32f`, depois `f9dab163f5d5b7fe`

### O3 - o quadro do topo sem o item da fala do autor

- feito: Saem de quadro_v411.py as funcoes _v411_fala_do_autor_tex e _v411_fala_do_autor_md, as constantes _V411_AB e _V411_FE e os tres pontos de uso (PT, EN e .md); do gerador saem _V411_FALA_DO_AUTOR e os cinco nomes da lista de nomes novos; delta_v411.py passou a EXIGIR a ausencia da chave fala_do_autor_para_o_quadro no TOPO (fail-closed) e a presenca do registro da retirada (ao_lado_d181_12nov).
- controle: conferir_conversa.quadro_sem_fala_do_autor com controles nos tres (PT, EN, .md) e o ensaio a seco (quadro_sem_o_item_da_fala_do_autor)
- `delta_v411.py` l.407: antes `f1cbdb9bf6a77040`, depois `8746e98bafa463f9`
- `quadro_v411.py` l.104: antes `67c95796bcab3965`, depois `48bb2f08f81d3d0f`
- `gerar_candidato_v411.py` l.436: antes `0efeb11822830c37`, depois `2d60e4b9578b763b`

### O4 - superficies publicas e textos do pos-rito

- feito: O artigo, a forma canonica, o manifesto e a saida do rito nao transcrevem (guarda). No pos-rito: o paragrafo pronto (README e site) e o handoff deixam de transcrever a ordem e o testemunho (so' data, sha16, papel e autor); as listas passam a usar o papel (texto da gerencia) no lugar do tema tirado do nome do arquivo; 'inscricoes embutidas' virou 'ordens e ratificacoes citadas por data e sha256, nao transcritas' em todos os textos do pos-rito, no Mapa e no rito_v411.sh; a lista curta/longa leva o qualificador de P = nP porque o papel do testemunho diz P = nP (guarda F34).
- controle: teste_textos_sem_candidato 80 etapas 0 falhas; teste_blocos_custodia 90 ok 0 falhas; os dois harnesses (ver contagens)
- nao feito: o orquestrador (pos_treino_v411.py) segue lendo a fala de abrir do arquivo da casa para o texto de autorizacao (AUT_FRASE: superficie de memoria da casa e conferidor estatico do servico); a linhagem, o Atlas, o ACOM, o handoff e o topico de memoria continuam podendo citar a ordem por arquivo e hash
- `pos_rito/textos_v411_novo.pysnip` l.362: antes `c11728744b1c82c0`, depois `e371d11ad941fe4f`
- `pos_rito/textos_v411_novo.pysnip` l.353: antes `c11728744b1c82c0`, depois `e371d11ad941fe4f`
- `pos_rito/textos_v411.py` l.299: antes `None`, depois `36e379e267b48cb1`
- `pos_rito/registrar_mapa_v411.py` l.264: antes `0da699e83bc1a250`, depois `7c200186ee13ea46`
- `rito_v411.sh` l.3: antes `6e3485418f18cbe7`, depois `1a2c658172681e25`

### O5 - tres termos entre aspas angulares

- feito: As aspas angulares viraram curvas nos tres termos (delta_v411.py l.267: provado na natureza; runtime_h0dn_v411.py l.15: teste cego e descoberta; l.16: provado na natureza).
- controle: grep de aspas angulares nos cinco arquivos novos: 0
- `delta_v411.py` l.303: antes `f1cbdb9bf6a77040`, depois `8746e98bafa463f9`
- `runtime_h0dn_v411.py` l.15: antes `de32fdbc7b8db32f`, depois `f9dab163f5d5b7fe`

### GUARDA - guarda_conversa_v411.py (obrigatoria e duravel)

- feito: Modulo novo: para cada uma das 11 falas da casa (lidas do arquivo, sha256 conferido contra o delta): (a) o texto normalizado inteiro e cada linha de 24+ caracteres tem 0 ocorrencias (formas: cru, escapado em JSON, escapado em repr, literais adjacentes do pprint juntados; o core entra como a juncao das suas cadeias); (b) as linhas de 12 a 23 caracteres nao ocorrem mais do que no alvo correspondente da v410 selada (um.py da base, core, artigo PT e EN, forma canonica, manifesto, stdout; contagens por sha16 da linha em GUARDA_CONVERSA_BASE_v410.json, sem texto); (c) os nomes dos 11 arquivos, o da ordem de 12/11 sobre a conversa e os radicais tem 0. Informativo (nao reprova): fragmentos de 40+ caracteres. Chamada: p00 (candidato), ensaio a seco (fonte, core, artigo PT e EN, forma canonica, manifesto, stdout do dry), conferidor (saidas reais), relatorio (portao novo guarda_da_conversa_d181).
- controle: controle negativo dos dois lados (linha plantada, nome plantado, linha curta alem da base, core com cadeia plantada, nome na chave do core: todos recusados; o limpo passa)
- `guarda_conversa_v411.py` l.140: antes `7da0de1971722c5b`, depois `4a97e9d7be844fd2`
- `conferir_conversa_v411.py` l.96: antes `None`, depois `30738ad264c7a632`
- `p00_precondicoes_v411.py` l.156: antes `6b3fd74d37a090a1`, depois `4815ea861682c82b`
- `ensaio_a_seco_v411.py` l.3520: antes `25e4d4b36c9c9f3d`, depois `bf30e53cef035fe9`
- `conferir_rito_v411.py` l.23: antes `256c254d20f954c5`, depois `979b10b0c69dd0db`
- `gerar_relatorio_v411.py` l.122: antes `9bf6956723bc5232`, depois `155670de1d7dc22e`

### B-01 - o fecho nos dois blocos (estresses e esperado pelos agregados)

- feito: Fecho do DESENHO (texto da gerencia, lido pelo delta, byte a byte) no fim dos dois blocos, PT e EN; o marcador e o Z das Cefeidas livres lido do core no formato do topo.
- controle: ensaio a seco: fecho_nos_dois_blocos_dos_estresses_e_dos_agregados (2 ocorrencias no tex e na secao); _teste_quadro e o gerador: 0 violacoes em todos os blocos
- `quadro_v411.py` l.126: antes `67c95796bcab3965`, depois `48bb2f08f81d3d0f`
- `delta_v411.py` l.260: antes `f1cbdb9bf6a77040`, depois `8746e98bafa463f9`

### B-02 - o disparador da F67 tolera o cifrao do TeX

- feito: O disparador passou a Z\$?\s+ (PT e EN); guarda_frases ganha 2 proibidas (PT e EN em TeX, sem as quatro: recusadas) e 2 limpas (PT e EN em TeX, com as quatro: passam). A guarda rodou sobre todos os blocos da secao e do quadro em TeX: nada novo acusado alem dos blocos do B-01, ja consertados.
- controle: guarda_frases: 29 proibidas reprovadas, 20 limpas passam (antes 27 e 18)
- `runtime_h0dn_v411.py` l.54: antes `de32fdbc7b8db32f`, depois `f9dab163f5d5b7fe`
- `guarda_frases_v411.py` l.53: antes `98a9039c6def1a69`, depois `a7ddeef3d2fa9b21`

### B-03/B-08 - a errata E44

- feito: E44 PT e EN (texto da gerencia, lido do DESENHO) entra como ultimo paragrafo da secao nova (PT e EN), na linha do H0DN do .md e na lista de erratas do spec (ERRATAS_V411 passa a quatro; token E41_E42_E43_E44); inclui os dois trechos antigos sobre beta a 5 sigma (B-08).
- controle: ensaio a seco: errata_e44_no_fim_da_secao_nova; leitura e conferidor: erratas == DL.ERRATAS_V411 (4 + a dos pisos)
- `delta_v411.py` l.251: antes `f1cbdb9bf6a77040`, depois `8746e98bafa463f9`
- `quadro_v411.py` l.141: antes `67c95796bcab3965`, depois `48bb2f08f81d3d0f`
- `registros_v411.py` l.74: antes `1f660686c660ead8`, depois `c3cda65a92ad34d3`

### B-04 - o fecho da frase ao lado do estatuto e do item O coracao

- feito: O fecho do DESENHO (PT e EN) entra depois da frase ao lado, na mesma funcao que serve aos dois lugares.
- controle: ensaio a seco: fecho_do_estatuto_e_do_coracao
- `quadro_v411.py` l.327: antes `67c95796bcab3965`, depois `48bb2f08f81d3d0f`

### B-09 - rotulos e EN da secao nova

- feito: Os rotulos do bloco dos agregados (tabela do DESENHO, PT e EN; chave desconhecida cai no proprio nome); no EN da secao, 'hers' virou 'its (the collaboration's)' e as datas dd/mm viraram '6 Nov' e '11 Nov'.
- controle: ensaio a seco: rotulos_dos_agregados_sem_chave_de_maquina e en_sem_hers_e_sem_datas_dd_mm_nas_duas_frases
- nao feito: o resto do B-09 fica (ordenado)
- `quadro_v411.py` l.135: antes `67c95796bcab3965`, depois `48bb2f08f81d3d0f`
- `quadro_v411.py` l.184: antes `67c95796bcab3965`, depois `48bb2f08f81d3d0f`

### C-01 - o chain_pos_rito_v411.sh e a checagem estatica

- feito: runtime_v411.py (inexistente) saiu da lista do passo 0 e do laco do passo 1 e entrou runtime_h0dn_v411.py; entram tambem conferir_conversa_v411.py, guarda_conversa_v411.py e a base GUARDA_CONVERSA_BASE_v410.json (o conferidor os importa); as duas listas foram relidas contra a pasta. O p00 ganha a checagem estatica: sh -n no chain e no rito_v411.sh, todo $PK/ e $SEL/ da lista do passo 0 e do laco do passo 1 existe, todo script invocado existe e compila (em memoria, sem .pyc), com tres controles negativos (nome inexistente na lista do passo 0, no laco do passo 1 e erro de sintaxe: recusados).
- controle: p00: (C-01) tres checagens ok; o chain original (com runtime_v411.py) e recusado pela mesma funcao (a lista obrigatoria nao existe)
- `pos_rito/chain_pos_rito_v411.sh` l.117: antes `00e159b24f8f3cf8`, depois `9297de7f28a8de24`
- `p00_precondicoes_v411.py` l.95: antes `6b3fd74d37a090a1`, depois `4815ea861682c82b`

### C-02 - o artigo em PDF e TeX no conferidor

- feito: conferir_conversa.pdf_tex_ok: o .tex PT e EN do Nos traz a abertura do resumo ratificado (lida do _V411_TOPO do candidato) e o titulo do quadro novo; cada .pdf tem tamanho > 0 e mtime >= o inicio do rito (rito_horarios_v411.txt; caminho por V411_RITO_HORARIOS ou o da pasta); o Nos falso do teste positivo ganha os .tex e um rito_horarios; controles numa copia: PDF velho, PDF vazio, TeX sem a abertura, TeX sem o titulo reprovam.
- controle: conferidor positivo no Nos falso: 5 itens novos; controles negativos dos dois lados
- `conferir_conversa_v411.py` l.52: antes `None`, depois `30738ad264c7a632`
- `teste_conferidor_positivo_v411.py` l.62: antes `51ca0de664b9b182`, depois `b9141d26e76f78e9`

### C-04 - 13a chave do resumo do selo

- feito: Dois controles no harness dos textos: sem a chave p2_ao_lado_da_v387 e com o valor trocado; os dois reprovam.
- controle: harness dos textos
- `pos_rito/harness_textos_ensaio_v411.py` l.974: antes `626aed64fcee4092`, depois `8687a1ab869dc921`

### C-05 - controle do MEMORY.md no p00

- feito: _memory_md_conferido aceita uma copia do indice; o controle injeta um indice de 196+ linhas (copia, em temporario) e exige pendente; nada e' escrito no indice real.
- controle: p00: (C-05) ok (indice projetado 205 linhas, limite 195)
- `p00_precondicoes_v411.py` l.188: antes `6b3fd74d37a090a1`, depois `4815ea861682c82b`

### C-09a - arquivo revisado ausente conta como diferente

- feito: pos_treino_v411.py s1b: ruins inclui o arquivo que nao e mais arquivo.
- controle: leitura do codigo (nao exercido: o orquestrador e vedado)
- nao feito: C-09 (b) fica como nota
- `orquestrador/pos_treino_v411.py` l.237: antes `2ea8768e613b0e35`, depois `04fe6274461a2fdd`

### C-10 - o portao do kernel exige as chaves

- feito: all(k in KR for k in (rc, sorry, erros)) alem do valor.
- controle: o relatorio passa com o recibo real (chaves presentes)
- `gerar_relatorio_v411.py` l.112: antes `9bf6956723bc5232`, depois `155670de1d7dc22e`

### C-11 - resumos de depuracao fora de work

- feito: Os dois resumos _DEPURACAO_sem_refazer.json de pos_rito\ foram movidos para C:\t\k411c\conserto_r1\depuracao\ (sha16 639359d6b18c6f7c e de67be4bab227204).
- controle: ls pos_rito: nenhum *_DEPURACAO*
