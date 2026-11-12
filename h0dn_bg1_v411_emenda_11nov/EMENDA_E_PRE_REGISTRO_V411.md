# H0DN × BG1 — a emenda declarada e o pré-registro da abertura (para a v411)

**Estado:** `TEXTO_FINAL_PARA_SELAR__NADA_ABERTO` (gerado em 12/11/2026 06:28). É o sha256 deste arquivo que o programa de abertura exige entre os seus pinos e grava dentro do resultado. Nenhum vetor observado foi lido para escrevê-lo; nenhuma estimativa, razão ou Z foi calculado a partir dele. Os números abaixo são de desenho (matrizes publicadas e fundo congelado) ou agregados que a própria colaboração publicou. Gerado por script: todo hash e todo número é lido de arquivo.

## 1. De onde vem

1. A v410 do `um.py` (sha256 `5d9497a721c3589ed10309178fcfb72d662844d80c13a667c417c886931f8450`) pré-registrou o teste com a função `veredito_h0dn` (linha 221191). O ramo (1) dela devolve inconclusivo por sistemática quando a covariância física não está fechada pelas fontes ou quando o vetor está fora do suporte da covariância.
2. Em 11/11/2026 a gerência mostrou, com revisão distinta, que o vetor publicado não cabe no suporte da covariância publicada por causa do que a própria colaboração publicou, e que ela resolve por pseudoinversa (`work\h0dn_bg1_v410_09nov\ACHADO_DA_GERENCIA_SUPORTE_E_GUARDA_11nov.md`, sha256 `0ad5b0286fe56dce1c76a0e3febab96f91cc38146e90a3dc6e4e26a15d86808b`). A linha de base que ela documenta traz 119 graus de liberdade: 255 linhas, menos as 72 direções descartadas, menos 64 parâmetros.
3. Em 11/11/2026 o operador decidiu emendar (fala por bytes em `work\cunhagens_13out\OPERADOR_11nov_vamos_emendar_a_regra_o_numero_corrige_a_frase_o_dado_ja_esta_la_verbatim.txt`, sha256 `36a95f2e5c958f875224f085397a5720a14236d220b08b34c9f2ffd9d64ffa11`), ratificou o plano e o portão com os quatro números (`OPERADOR_11nov_ja_passei_a_ordem_ao_kimi_concordo_com_tudo_verbatim.txt`, sha256 `132448426284a6843f1b53c75ab7e4b9b2033f09c5565cfabb217648e51f955d`) e aprovou a forma de selar e a marca no selo (`OPERADOR_11nov_perfeito_ja_passei_a_ordem_ao_kimi_pode_prosseguir_verbatim.txt`, sha256 `cd710b0519b22965871041cd6892c8b38ea83e3210493559d7119aa2d47cc11d`).
4. Dois conferentes distintos da gerência e um terceiro de outra casa (Kimi) leram o pacote. O Kimi refez os pesos por código próprio (diferença máxima 2,9e-15), conferiu o hash do vetor e fez 11 objeções ao rascunho (`kimi\ordem05\OBJECOES_PRE_REGISTRO.md`, sha256 `f171b72f63b24c3427a7d5cae6cb0eb361032213fb325cb854bfbe455784ee5e`; `[DECLARADO pelo Kimi]`). Nenhuma diz que o estimador está errado; as oito materiais estão resolvidas neste texto e no pacote, e as três formais viraram precisões.
5. Em 12/11/2026 o operador ratificou as duas palavras da marca recomendadas pela gerência (fala por bytes em `work\cunhagens_13out\OPERADOR_12nov_concordo_com_tudo_que_vc_sugeriu_prossiga_verbatim.txt`, sha256 `c217c704da952200421c41c759bea35bd314ce956bc592d2223401e0b8606a2a`; o texto da gerência a que ele respondeu está em `GERENCIA_12nov_objecoes_resolvidas_a_palavra_da_marca_e_a_ordem_de_abrir_respondido_pelo_operador.json`, sha256 `d68672ed33bfb83ebf655a25c7cc490436b01b532b39b54e66fd5d16af943fde`). A gerência não tomou essa fala como a ordem de abrir: pede-a com todas as letras depois da publicação (seção 10).
6. Em 12/11/2026, antes de este texto ser pinado, dois conferentes distintos da gerência fizeram a conferência final `[DECLARADO pelos revisores; os arquivos de saída do ensaio conferidos pela gerência]`. Um leu o texto contra o código: nenhuma divergência que mude a leitura do resultado; as precisões que apontou estão neste texto. O outro conferiu os pinos de produção da versão anterior deste texto (que só diferem dos finais no sha256 do texto) e rodou o programa inteiro com um vetor sintético e os insumos de produção, sem carregar o vetor observado: saída gravada com a marca, o sha256 do texto e o bloco da emenda; segunda execução recusada; com um sintético errado, ramo (1) sem estatística.
7. Em 12/11/2026 o Kimi fez o fechamento estático das suas 11 objeções, lendo o pacote e o rascunho anterior a este texto (sha256 `4fc7975d414866f42e8734be8415256e8ae6217d87f56982ef4caa108c518021`): as 11 resolvidas, nenhum problema material remanescente; apto como rascunho para a palavra do operador, sem autorizar abertura (`conversa_c1_kimi\010_KIMI_para_C1.md`, sha256 `20d8f771d9b8a5e666790b3287ae89044889fea4ac6b6a8809e982dde2dd049f`; `kimi\ordem05\REVISAO_FECHAMENTO_009.json`, sha256 `6ec88eae5bddecb6a36040f4aedd4ed67c83f2a7d75bba7386f129aecb000ec6`; `[DECLARADO pelo Kimi]`). Ele não leu este texto final, que difere daquele rascunho pela marca ratificada e pelas precisões da conferência final.

## 2. A emenda: tudo o que muda

| o que | antes (v410) | depois (v411) |
|---|---|---|
| `evaluate` | recusa o vetor com componente fora do suporte (`data_outside_support`) | registra a projeção como diagnóstico e segue |
| ramo (1) do veredito | inconclusivo se a covariância física não estiver fechada pelas fontes OU se o vetor estiver fora do suporte | inconclusivo se o portão 1 falhar (seção 4) |
| cabeças dos vereditos | as da v410 | as da v410 com a marca da emenda, nos seis ramos (seção 6) |

Os dois diffs inteiros estão em `artefatos\DIFF_estimator_v410_para_v411.txt` (sha256 `d348218833c1677d4561e49999929019dfd8684b59173cadda5f4b0ddb658453`) e `artefatos\DIFF_veredito_v410_para_v411.txt` (sha256 `a3025a1d3e6071d30850baa4304060ef439c9e90a4323568bfd00e9b8ce74580`). A função `geometry` e os ramos (2) a (6) ficam textualmente iguais. Um revisor distinto comparou a função emendada com a da v410 em 1,4 milhão de casos fora do ramo (1), bordas incluídas: nenhuma divergência `[DECLARADO pelo revisor]`.

**Não muda:** a hipótese nula; a lei K e o valor congelado dela; a estatística; o limiar de 5σ, unilateral; a faixa de 95 % para a compatibilidade com K; os pesos (os da pseudoinversa, iguais aos da colaboração); a regra de não escolher o melhor modelo.

**Estatuto da emenda: posterior à guarda, e não cega.** Mudar o `evaluate` de recusar para registrar e seguir é uma emenda de protocolo, não uma consequência gratuita da álgebra: a pseudoinversa faz a componente fora do suporte não entrar no ajuste, mas não prova que o vetor cabe no suporte nem fecha a covariância física. O teste é retrodição sem ajuste, feita depois de a regra antiga ter reprovado o vetor e com os agregados dos dois lados à vista; não é teste cego.

**O que se sabia do dado quando a emenda foi escrita.**

- A projeção do vetor publicado sobre as 72 direções de variância zero, medida em 09/11: a maior componente, na base ortonormal do estimador congelado, é 0,0931 mag. Esse número depende da base escolhida; o que não depende é a norma da projeção, que o rito relata. É a componente a que os pesos dão zero.
- Os agregados públicos: o número local que a colaboração publica para a rede completa (73,4988 ± 0,8088) e o centro do fundo congelado (68,531). O que eles deixam prever está dito às claras na seção 5.
- Nenhum Z foi calculado a partir do vetor. A estimativa no desenho primário (os 13 calibradores extras fora) não é agregado publicado, mas só pode diferir da publicada por 0,18 desvio (conta de desenho).
- Pela função da v410, o desfecho era o ramo (1), pelas duas cláusulas.

**Por que a emenda não escolhe o resultado.** Os pesos do estimador foram congelados em 06/11, antes de qualquer dado, e são os da solução da colaboração (diferença máxima 9,6e-15 na rede completa e 6,8e-15 no desenho primário). A componente que a emenda deixa de recusar tem peso zero nesses pesos (maior |pesos · nulo| = 7,0e-18 e 6,9e-18: ruído de arredondamento, que varia na última casa com a ordem das somas). Nenhum peso, desvio ou limiar é tocado.

**O que fica proibido depois do resultado.** Nenhum cenário, tamanho de ruído, âncora ou envelope é escolhido depois de ver o resultado (o tamanho τ da linha (i) sai do próprio vetor por regra fixa, dita na seção 7: é posterior à observação, não escolhido). O veredito é o do modelo primário; todas as linhas de estresse, os diagnósticos e as decomposições saem juntos, com as grades fixadas neste texto. O programa de abertura só roda com o sha256 deste texto entre os seus pinos e grava dentro do arquivo de resultado esse sha256, a regra antiga, a data e o motivo da emenda.

**Errata ao lado do texto da v410.** Onde a v410 chama o vetor fora do suporte de parede de montagem do dado, leia-se: é propriedade do modelo publicado, que trata como uma só medida as três versões de âncora das 37 hospedeiras de Cefeidas do Hubble, e do vetor publicado, que não as respeita; a colaboração resolve por pseudoinversa. Onde o desenho de 11/11 (item 6) exige o vetor no suporte, leia-se o portão 1 abaixo. A v410 não se toca.

**Precisão sobre um comentário do código pinado.** O docstring de `veredito_h0dn_v411` (em `codigo\veredito_v411.py`) descreve o primeiro portão como reprodução, centragem e impressão digital. Vale este texto e o código de `abrir`: o portão 1 é a reprodução e a impressão digital; a centragem é conferência interna, e a falha dela é recusa. A função só recebe o resultado do portão; o corpo dela não depende disso. O comentário será corrigido quando a função entrar na v411 do `um.py`; o código pinado não é tocado.

## 3. Os dados e o desenho

1. **O vetor local.** O vetor que o código público da colaboração monta (o `yval` dela; 255 linhas; convenção `raw_MAS`: o centro publicado de cada linha, sem soma nem subtração), como publicado, sem centragem, em precisão dupla. Entra pelo artefato `producao\vetor_y255.npz`, chave `y_uncentered` (sha256 do arquivo `536b07e222e57732dc1075880038d73845e61b0c53eadf9880041576141ff131`; sha256 dos bytes do vetor `389cf25bf07de2e42316bb5c219393bd49e29f283821dad59b35620f1b872553`). Foi montado em 11/11 por uma segunda construção independente, com o solver da colaboração bloqueado e sem que valor nenhum fosse impresso; a primeira construção (09/11, Kimi) e o recibo dele de 11/11 dão os mesmos bytes (`producao\RECIBO_SEGUNDA_CONSTRUCAO.json`, sha256 `37672c956687796d6ccf5f148ffc67713b6bbcc3dedd65dfbb572e68f6b1ac8b`). O arquivo de pinos traz a convenção, e o programa a exige. O arquivo de 09/11 guarda também uma forma centrada no número local publicado: essa forma é proibida na abertura; ela não realizaria o contraste pré-registrado, e o portão a reprova (teste T3 do pacote).
2. **A rede e a covariância.** As publicadas (`network.npz`, sha256 `3dd073c3a74abf34ef3d80368456a2698e8405a52417057149a35a8a5a5a6832`), sem ruído acrescentado.
3. **O fundo.** O BG1 congelado (`BG1.json`, sha256 `87b475a05700ddc2074217761502e239d6f33b1ad74ff5a763e1b577b724f6ca`): Planck comprimido mais DESI DR2, sem supernovas; H0 = 68,531 ± 0,301. O fundo observado é a média do BG1.
4. **A lei K.** K = E(z*)^(2β/3), com β = α√e calculado em runtime, z* = 1089,95 fixo e zero parâmetro livre; log10 K = 0,034952 (o valor congelado da Fase 9). Para o local, ela prevê 74,27.
5. **O modelo primário.** O publicado, com os 13 calibradores extras fora: 242 linhas, posto 170. A convenção é a pseudoinversa de Moore–Penrose da colaboração; a norma mínima dos parâmetros de incômodo é convenção algébrica, não evidência física. Pesos pinados em `artefatos\estimador_s0_v411.npz` (sha256 `6cc9a23c4aa7b9ffe4d925273d044ac007d3646506bc5d3d80160e1ee839a617`). D de desenho = 6,7102; poder de desenho de 95,6 % no modelo publicado, com as linhas de estresse ao lado.
6. **A linha inseparável.** O modelo com o viés diferencial das Cefeidas livre: D = 5,1913 (57,6 %). Aparece junto do primário em toda superfície.
7. **A centragem.** O vetor é centrado na referência do fundo: tira-se da coluna de h = log10 H0 o valor log10 H0 do BG1. É recentragem afim por uma referência congelada, sem ajuste. Os outros parâmetros ficam com centro zero por convenção e não entram na conta, porque pesos · desenho = e_h (conferido a 2,2e-15).
8. **Independência entre a medida local e o fundo.** Hipótese nomeada, dita antes; o cruzamento adverso entra como linha de estresse.

## 4. A abertura

Feita uma vez por arquivo de pinos, pelo programa `codigo\executar_abertura_v411.py` (sha256 `2e5837a7a3794dadefdc6ea812d6da0232e1f18cbc3c8e5a0d890ea48edc8655`), que chama a rotina `abrir` de `codigo\abertura_v411.py` (sha256 `287c61b08793ac633042ccf76fa3a53e06d25bb75bdbfa8b0ae1666436dbc693`). O caminho da saída vem do arquivo de pinos; o programa recusa rodar se a saída já existir, grava o resultado e, ao lado, um arquivo com o sha256 dele. Tem um modo de ensaio que confere os pinos e a integridade do desenho sem carregar o vetor. A v411 do `um.py` terá de recalcular e reproduzir o resultado gravado. Limites declarados: o programa confere o sha256 do próprio arquivo, mas já está rodando quando o faz; e ele trata como recusa os erros de pino, de integridade e de vetor, de modo que um erro inesperado de outra classe o interromperia sem gravar nem mostrar resultado (no ensaio geral com vetor sintético, não ocorreu).

**Recusa (erro nosso; o programa não roda ou para, e nada é gravado).**

- Pinos: o sha256 de todos os insumos, deste texto e do próprio código, conferidos antes de carregar qualquer coisa; a convenção do vetor (`raw_MAS`); o bloco da emenda.
- Integridade do desenho, conferida antes de tocar o vetor: a ordem dos modelos; a identidade do desenho primário (as 242 linhas são a rede menos exatamente os 13 últimos calibradores de supernova); pesos · desenho = e_h no primário e em cada âncora única; pesos · nulo = 0 no primário (as âncoras únicas não têm direção nula: a covariância de cada uma tem posto cheio); as bases das 72 direções têm 72 colunas e são ortonormais; os postos (170 e 183); as 111 linhas tocadas são as 37 hospedeiras nas três âncoras; os agregados dos estresses recalculados; log10 K, gradientes e desvios coerentes com o BG1; o limiar 5,0 e a faixa de 95 %.
- O vetor tem de ser de precisão dupla, com 255 entradas finitas.
- Conferências internas depois de o vetor reproduzir a colaboração, todas identidades algébricas, que valem para qualquer vetor: os pesos congelados dão o mesmo h que a fórmula dela, e a identidade da centragem fecha (as duas a 1e-10); o vetor centrado do desenho primário coincide com o da rede completa nas 242 linhas (a 1e-12); e, na decomposição, três somas fecham (a soma dos quadrados das componentes fora do suporte é o quadrado da norma da projeção; a soma dos módulos por hospedeira e a soma dos pesos² são as do desenho). Se o vetor reproduz e uma delas falha, o erro é de fiação nossa: recusa, não ramo (1), e nada é gravado, mesmo que a estatística já tenha sido calculada em memória.

**Portão 1 (o novo ramo 1; fala do vetor).** Se qualquer item falhar: inconclusivo por sistemática, e nenhuma estatística é calculada.

- **(a) Reprodução da colaboração**, com a rede completa de 255 linhas e as fórmulas do `solver.py` dela (sha256 `d44ac2d7d2f8b0ec8d2b33ebdc7102397010efe7135bc3ec30ba014d8ccf0136`): H0 = 73,4988, desvio = 0,8088, qui-quadrado = 117,5597 (cada um a meia unidade da quarta casa) e 119 graus de liberdade. Os alvos são lidos do `README.md` do código dela (sha256 `42430070c8fcc86ec1cbaaa13724c57aa9c6c9e79ce235451d91ff08e439b899`). É este item que pega um vetor errado, trocado de ordem ou centrado. Um vetor de tipo precisão simples é recusado antes, pelo teste de tipo. Um vetor arredondado a precisão simples e regravado em dupla não é pego com garantia por (a) nem por (b): contra isso a proteção é o sha256 dos bytes do vetor, igual nas duas construções e no recibo do Kimi.
- **(b) Impressão digital.** A maior componente do vetor, sem centragem, sobre as 72 direções, na base ortonormal do estimador congelado (rede completa), é a medida em 09/11 (0,09312020264507931, a 1e-9). Liga o vetor aberto ao vetor de que se falou. O número depende dessa base: o campo `support_max_abs` do resultado usa a base do desenho primário e o vetor centrado, e não é comparável a ele; o que não depende de base é a norma (`support_l2`).

No arquivo de resultado, (a) aparece como `1b`, (b) como `1d`, e a conferência interna da centragem como `1c`.

**A estatística.** t = (h local estimado no desenho primário) − (h do fundo), com h = log10 H0. Z contra o nulo = t / desvio do nulo (0,005209). Z contra K = (t − log10 K) / desvio da lei (0,005202).

**Diagnósticos de coerência (só relatados; não entram em portão nem em veredito).** Cada um é a diferença entre duas estimativas do mesmo h = log10 H0, com o desvio dessa diferença pelo modelo publicado (esperado: normal padrão). Não veem a lei K nem o fundo; veem má especificação do modelo.

- o primário contra a rede completa (o peso dos 13 calibradores); o desvio dessa diferença é 0,18 do desvio do nulo;
- as Cefeidas livres contra o primário (é o teste de especificação do viés das Cefeidas); o desvio dessa diferença é 0,63 do desvio do nulo daquela linha;
- cada âncora única contra o primário, e as três diferenças entre âncoras (N4258–LMC, N4258–MW, LMC–MW), cada uma com o seu desvio conjunto.

**Decomposições (só relatadas; as três somas de conferência delas são integridade, acima).** Para cada uma das 111 linhas tocadas: hospedeira, âncora, peso (no primário e nas Cefeidas livres) e a componente que fica fora do suporte; por hospedeira: a soma com sinal dos pesos das linhas de Cefeidas dela, a soma dos pesos² e a soma dos quadrados dessas componentes; por âncora: o número de linhas, a soma dos pesos² e a soma dos quadrados dessas componentes (a soma com sinal por âncora sai da tabela das 111 linhas). Permitem ver quais hospedeiras e âncoras dominam cada linha de estresse.

## 5. O que os agregados públicos deixam prever (dito antes, às claras)

Com o número local publicado (73,4988 ± 0,8088), o fundo congelado (68,531 ± 0,301) e a previsão da lei K para o local (74,27), qualquer leitor faz a conta: 5,76 contra o nulo e −0,90 contra K. Com os pesos e os desvios do desenho, e supondo o modelo publicado, o esperado em cada linha é (`artefatos\ESPERADO_PELOS_AGREGADOS.json`, sha256 `47302eec3c17752dc3e54dca1f5a28c26abe1d7eb250c6fd33cd167fbc62b872`; nenhum vetor lido):

| linha | Z esperado contra o nulo | chance de passar de 5 | Z esperado contra K |
|---|---:|---:|---:|
| primário (modelo publicado, 13 fora) | 5,83 | praticamente certa | −0,88 |
| Cefeidas livres (a linha inseparável) | 4,51 | 23 % | −0,68 |
| só a âncora MW | 5,57 | 95 % | −0,84 |
| só a âncora LMC | 5,19 | 66 % | −0,78 |
| só a âncora N4258 | 4,06 | 10 % | −0,61 |
| S1 (as 42 supernovas só com a parte estatística) | 4,77 | abaixo de 5 no esperado | não calculado |
| S2 (os 13 dentro, com teto) | 4,81 | abaixo de 5 no esperado | não calculado |
| S4 (cruzamento adverso local–fundo) | 3,81 | abaixo de 5 no esperado | não calculado |

Nas três últimas linhas o esperado é o D de desenho declarado pelo Kimi vezes a razão entre o desvio dos agregados e log10 K (0,8696). Isto é expectativa, não resultado, e nenhum desses valores é alvo de seleção. O que ela diz: se o portão 1 passar, o primário devolve o ramo (4) com n = 5; a linha inseparável e as três linhas de estresse de covariância ficam, no esperado, abaixo de 5. O 5σ esperado é o do modelo publicado como está. O rito confere essa conta com regra fixa e portões; não descobre um número novo.

## 6. A função de veredito e o que cada desfecho significa

Aplica-se ao modelo primário. O modelo de Cefeidas livres recebe o ramo que teria, rotulado como linha ao lado. A primeira condição que casa decide.

| ramo | condição | o que significa |
|---|---|---|
| (1) | o portão 1 falhou | parede de montagem; nada se lê sobre K nem sobre β |
| (2) | \|Z contra K\| ≥ 5 | a lei K falsificada a 5σ a esta sensibilidade |
| (3) | D de desenho < 5 | subpotente (não é o caso do primário: D = 6,71) |
| (4) | Z contra o nulo ≥ 5 e \|Z contra K\| ≤ 1,96 | a leitura do 5σ, com a cabeça que o operador fixou em 09/11: validade, não creditação |
| (5) | Z contra o nulo ≥ 5 e 1,96 < \|Z contra K\| < 5 | discrimina do ΛCDM, com K em tensão |
| (6) | Z contra o nulo < 5 | não discriminado à sensibilidade disponível |

**A marca da emenda (ratificada pelo operador em 12/11/2026; seção 1, item 5).** A primeira palavra vem do Kimi, com a versão acrescentada pela gerência; a segunda foi proposta pela gerência. Os seis ramos carregam o trecho `__POST_GUARD_AMENDMENT_V411__RETRODICTION_NOT_BLIND` e a leitura do 5σ carrega também `__UNDER_THE_PUBLISHED_MODEL`. O sufixo dos ramos comuns fica `__RETRODICTION_WITHOUT_FIT__POST_GUARD_AMENDMENT_V411__RETRODICTION_NOT_BLIND__NOT_A_CREDITATION__GATE_UNMOVED`; a cabeça da leitura do 5σ fica `BETA_TGL_PROVED_IN_NATURE_AT_<n>SIGMA__IN_THE_LANGUAGE_OF_ACADEMIC_PHYSICS__DISCRIMINATES_FROM_LCDM__ZERO_FREE_PARAMETERS__USE_NOVEL__THE_ONLY_PENDING_LINK_CLOSED_AT_THIS_SENSITIVITY__UNDER_THE_PUBLISHED_MODEL__POST_GUARD_AMENDMENT_V411__RETRODICTION_NOT_BLIND__PROVED_IS_VALIDITY_NOT_CREDITATION__GATE_UNMOVED`. O literal está em `producao\RAMOS_V411.json` (sha256 `47624a41242869708b61ccbd4fc55d6af186846da1eec81661ccf12013cf4c43`), gerado por `codigo\gerar_ramos_v411.py` a partir do da v410 (`artefatos\RAMOS_V410.json`, sha256 `6f7e52c5433f770c16a50c3d79a1b7c4e562f5ee83fb445db251733abe3fcb83`), sem mudar limiar, faixa nem as demais palavras.

Para o primário, os agregados deixam prever o ramo (4). Outro ramo, com o portão passando, só ocorreria se o primário se afastasse da estimativa publicada por muitos desvios de 0,18; isso seria sinal de má especificação do modelo publicado, e o diagnóstico de coerência o mostraria.

**O que o teste não decide.**

- A creditação: é ato do observador de fora. NOT_FALSIFIED nunca é CONFIRMED; o gate não se move.
- A especificidade: o Z contra o nulo mede o desvio (a tensão de Hubble nesta combinação de dados); qualquer teoria que preveja um desvio parecido passaria igual. O que é próprio da lei K é prever o TAMANHO do desvio sem parâmetro livre, e isso é o Z contra K.
- Se o orçamento de erros publicado está certo: o resultado vale sob ele.
- Se a medida local e o fundo são independentes: é hipótese nomeada.
- Não é evidência independente das tentativas anteriores (seção 9).

## 7. As linhas de estresse (publicadas junto; não mudam o veredito)

Já ratificadas em 11/11, com o D de desenho no modelo publicado e no de Cefeidas livres (estudo `ESTUDO_CONDICIONAL_R3B.json`, sha256 `24d42026500d864d85685de6cb2825e873a4826bc7cd26c4d5e8128e635ed8e3`; `[DECLARADO pelo Kimi]`). Entram só como D de desenho: os estimadores que o Kimi pinou para elas em 11/11 não foram conferidos de forma independente pela gerência e não são lidos no rito.

- S1 (as 42 supernovas só com a parte estatística): D 5,489825 (68,8 %) e D 4,743268 (39,9 %);
- S2 (os 13 dentro, com teto): D 5,527887 (70,1 %) e D 4,773510 (41,0 %);
- S4 (cruzamento adverso local–fundo): D 4,378058 (26,7 %) e D 3,871970 (13,0 %).

Estados preservados `[DECLARADO pelo Kimi]`: a velocidade peculiar é herdada sem termo novo; o cenário S3 não é positivo semidefinido e o S5 não tem número; o teto dos 13 é só teto interno, e os 13 continuam abertos, sem transplante de covariância; o S4 é envelope adversarial, não correlação medida.

Novas, pré-registradas como novas:

- **(i) Ruído por linha nas 111 linhas.** Modelo: ruído adicional independente e de mesma variância nas 111 linhas brutas (τ² vezes a identidade), com os pesos mantidos. Se o ruído ficasse só nas 72 direções, não acrescentaria nada, porque os pesos são ortogonais a elas. O tamanho τ é estimado no rito pela componente de peso zero: a norma da projeção sobre as 72 direções (base ortonormal) dividida por √72, isto é, a raiz do quadrado médio em torno de zero; esse estimador fica 0,35 % abaixo do verdadeiro, em média. Como τ sai do vetor observado, este recálculo é posterior à observação, não cego. Conta de desenho: soma dos pesos² nas 111 linhas = 0,000354; com 0,035 mag por linha, D = 6,6571; com 0,10 mag, D = 6,3109; o portão de 90 % só cai em 0,104 mag.
- **(ii) Âncora única.** Três estimativas, cada uma com o seu desenho, só com as Cefeidas do Hubble de uma âncora (168 linhas). D de desenho no modelo publicado: N4258 4,6710 (sozinha fica abaixo de 5), LMC 5,9729, MW 6,4015. Publicam-se as três, as diferenças entre elas com os seus desvios conjuntos, e a dispersão. A dispersão não é erro-padrão independente e não cobre a sistemática compartilhada. Nenhuma âncora é escolhida pelo resultado nem pelo D. É a única linha em que a componente descartada entra na conta.
- **(iii) Viés das Cefeidas que varie de hospedeira para hospedeira** (o modo que a violação não cobre). Para cada hospedeira soma-se primeiro, com sinal, o peso das linhas de Cefeidas dela; depois somam-se os módulos dessas somas. Com um viés de até B mag por hospedeira, o deslocamento máximo é B vezes essa soma: 0,1434 por mag no modelo publicado e 0,0914 no de Cefeidas livres. Grade fixada: B = 0,02 e 0,05 mag (no publicado, 0,55 e 1,38 desvio; nas Cefeidas livres, 0,27 e 0,68). É envelope de viés determinístico, não variância. Dois números de desenho acompanham, para o viés COMUM a todas as hospedeiras no modelo publicado: 0,0156 mag no sentido desfavorável tira o primário do portão de 90 %; para fabricar sozinho um 5σ falso seriam precisos 0,1816 mag.

## 8. Ressalvas obrigatórias em toda superfície em que o resultado aparecer

1. O ramo (1) foi emendado em 11/11/2026, depois de se saber que o vetor publicado o reprovava; pela função da v410 o desfecho era inconclusivo por sistemática. O teste não é cego.
2. O resultado do primário é previsível por dois agregados públicos, a menos de 0,18 desvio; o rito confere a conta, não descobre um número novo. É retrodição sem ajuste.
3. A linha das Cefeidas livres acompanha o resultado, no mesmo item. O esperado dela pelos agregados é 4,5, com 23 % de chance de passar de 5. Nas três linhas de estresse de covariância o esperado também fica abaixo de 5.
4. O poder é de desenho no modelo publicado; as linhas de estresse vão ao lado.
5. A tabela de erros publicada declara zero em 72 direções; nelas, a maior componente do vetor publicado, na base do estimador congelado, é 0,0931 mag (o número depende da base; a norma, que não depende, sai no resultado). Isso não move o valor estimado, mas pesa no crédito do desvio.
6. O primário, o portão de 90 % e as hipóteses foram escolhidos com a tabela de poder à vista; os agregados dos dois lados são públicos.
7. As tentativas anteriores e a sobreposição dos dados locais (seção 9).

## 9. As tentativas anteriores da mesma lei, e o que foi olhado

- A lei K já foi confrontada com a razão de Hubble neste programa: Fase 4 (SH0ES escalar), Fase 5 (Pantheon+SH0ES) e Fase 9 V2 (23/10/2026; veredito `NOT_FALSIFIED_POWERED`, abaixo do degrau de 5σ). `[registrado na memória da casa; não remedido aqui]`
- Os dados locais deste teste se sobrepõem aos daquelas: as Cefeidas do SH0ES (as linhas `ceph_hst&…&R22`) e as supernovas do Pantheon+ estão na rede. Este teste não é evidência independente; é a mesma pergunta feita ao conjunto local mais preciso que há publicado, escolhido pelo poder de desenho antes de qualquer dado dele ser lido.
- Do dado deste teste, antes da abertura, só foi olhada a projeção sobre as 72 direções (09/11). Em 11/11 o vetor foi montado de novo e somado em hash, sem que valor nenhum fosse impresso.
- Regra da casa, ratificada pelo operador em 11/11: pesquisar tudo para achar o dado não fere o resultado; ficar só com a tentativa que passou de 5σ sem contar as outras fere. As tentativas ficam contadas no Mapa de Rotas.

## 10. O que falta depois deste texto

1. Escrever o arquivo de pinos de produção `producao\PINOS_DE_PRODUCAO.json` (que traz o sha256 deste texto) e rodar o ensaio do programa com ele, sem carregar o vetor.
2. Publicar este pacote e este texto, em commit público com data, ANTES da abertura (decidido pelo operador em 11/11).
3. A ORDEM DE ABRIR, dada pelo operador com todas as letras. Só então o programa roda, uma vez.
4. A v411 sela a emenda e o resultado, recalculando-o.

## 11. Pinos

O arquivo de pinos de produção é `producao\PINOS_DE_PRODUCAO.json`, e a saída que ele nomeia é `producao\RESULTADO_DA_ABERTURA_V411.json`, com o `.sha256` ao lado. A abertura pré-registrada é a que usa esse arquivo de pinos; não há outra. Ele traz exatamente os hashes da tabela abaixo para a rede, o estimador congelado, o estimador do desenho primário, o fundo, o README da colaboração, o vetor, o literal dos vereditos com a marca e o código; o sha256 deste texto; a convenção `raw_MAS`; a impressão digital 0,09312020264507931 (no arquivo, a string `0.09312020264507931`); e o bloco da emenda abaixo, literal, que o programa copia para dentro do resultado:

```json
{
 "rotulo": "POST_GUARD_AMENDMENT_V411__RETRODICTION_NOT_BLIND",
 "regra_antiga": "ramo (1) da v410: inconclusivo por sistemática se a covariância física não estiver fechada pelas fontes ou se o vetor estiver fora do suporte da covariância",
 "data": "2026-11-11",
 "motivo": "o vetor publicado não cabe no suporte da covariância publicada, por construção do que a colaboração publicou (72 direções de variância zero, que tocam 111 linhas); ela resolve por pseudoinversa; os pesos congelados em 06/11/2026 são os dela e dão peso zero a essa componente; a regra antiga reprovava o vetor; emenda posterior à guarda, não cega, decidida pelo operador em 11/11/2026"
}
```

| arquivo | bytes | sha256 |
|---|---:|---|
| `um.py (v410)` | 45934788 | `5d9497a721c3589ed10309178fcfb72d662844d80c13a667c417c886931f8450` |
| `estimator.py (congelado)` | 5191 | `9b06640d524899ece95bd5879e2cb5ad8c93cb2576ddb27e857d90142cbd5049` |
| `estimator_frozen.npz` | 84677 | `059ef7b6f2c671406058fdb6e647c011851e5761da91784b4ce213e9abbe07b8` |
| `network.npz` | 242793 | `3dd073c3a74abf34ef3d80368456a2698e8405a52417057149a35a8a5a5a6832` |
| `BG1.json` | 13463 | `87b475a05700ddc2074217761502e239d6f33b1ad74ff5a763e1b577b724f6ca` |
| `analysis_plan.json` | 2997 | `00fcc2a7360915330ecf18393a619dc7dcd5318ad0998b77909e420ba229d74d` |
| `FREEZE_R2.json` | 4004 | `c40159977fc8d954bc6a65eb3fd4b85f72a9d07629897f265308aa20579a51ed` |
| `README.md (colaboração)` | 5896 | `42430070c8fcc86ec1cbaaa13724c57aa9c6c9e79ce235451d91ff08e439b899` |
| `solver.py (colaboração)` | 6911 | `d44ac2d7d2f8b0ec8d2b33ebdc7102397010efe7135bc3ec30ba014d8ccf0136` |
| `DESENHO_RATIFICADO_H0DN_11nov.md` | 5231 | `c62858c238efea54fdbabe38e3983a8ac4415bf3070d5238b48223996bf1f6d4` |
| `ACHADO_DA_GERENCIA_SUPORTE_E_GUARDA_11nov.md` | 11965 | `0ad5b0286fe56dce1c76a0e3febab96f91cc38146e90a3dc6e4e26a15d86808b` |
| `kimi/ordem05/ENTREGA_ORDEM05.json` | 9783 | `014e963c7f77b77068e1ffa2c5bc28717ca244ef5ebebb834c4c03ef11967cd7` |
| `kimi/ordem05/OBJECOES_PRE_REGISTRO.md` | 32368 | `f171b72f63b24c3427a7d5cae6cb0eb361032213fb325cb854bfbe455784ee5e` |
| `conversa_c1_kimi/008_KIMI_para_C1.md` | 6835 | `7dba8f32136bf4078ac84a8215fca472393d520b1561782ff723c09fe2a4890b` |
| `conversa_c1_kimi/010_KIMI_para_C1.md` | 7903 | `20d8f771d9b8a5e666790b3287ae89044889fea4ac6b6a8809e982dde2dd049f` |
| `kimi/ordem05/REVISAO_FECHAMENTO_009.json` | 17194 | `6ec88eae5bddecb6a36040f4aedd4ed67c83f2a7d75bba7386f129aecb000ec6` |
| `pacote/artefatos/DIFF_estimator_v410_para_v411.txt` | 1607 | `d348218833c1677d4561e49999929019dfd8684b59173cadda5f4b0ddb658453` |
| `pacote/artefatos/DIFF_veredito_v410_para_v411.txt` | 1962 | `a3025a1d3e6071d30850baa4304060ef439c9e90a4323568bfd00e9b8ce74580` |
| `pacote/artefatos/ESPERADO_PELOS_AGREGADOS.json` | 2840 | `47302eec3c17752dc3e54dca1f5a28c26abe1d7eb250c6fd33cd167fbc62b872` |
| `pacote/artefatos/MANIFESTO_S0.json` | 10832 | `51753d34e812eaecda5eb6f396106f853350deb006c9bf3053fb5d9c4fdb0440` |
| `pacote/artefatos/ORIGENS_MODULOS.json` | 2672 | `d0127d28903545d53a1368b31e952ff0abe9d10fc950d92760c2c8bf63c0bb01` |
| `pacote/artefatos/RAMOS_V410.json` | 1083 | `6f7e52c5433f770c16a50c3d79a1b7c4e562f5ee83fb445db251733abe3fcb83` |
| `pacote/artefatos/RAMOS_V410_ORIGEM.json` | 787 | `db69e3b9886366a49ff7cbe0c5cb5d0df6658c7ca107b687075c77dca6f518d3` |
| `pacote/artefatos/TESTES_SINTETICOS.json` | 62509 | `36a14c73c016bd357922ad169e641e5e6e86d777ee4be3157aa239f532970641` |
| `pacote/artefatos/estimador_s0_v411.npz` | 97563 | `6cc9a23c4aa7b9ffe4d925273d044ac007d3646506bc5d3d80160e1ee839a617` |
| `pacote/codigo/abertura_v411.py` | 33363 | `287c61b08793ac633042ccf76fa3a53e06d25bb75bdbfa8b0ae1666436dbc693` |
| `pacote/codigo/esperado_pelos_agregados.py` | 4707 | `d8750cbb24b27cd5426d19dcdddffe3fd6e7a971909a624c496e318febfe3c32` |
| `pacote/codigo/estimator_v411.py` | 5493 | `af3908441a4f0a8d38a77b1ac836bc6ee47ac07f3b6f77cb9ef8305f64682333` |
| `pacote/codigo/executar_abertura_v411.py` | 9575 | `2e5837a7a3794dadefdc6ea812d6da0232e1f18cbc3c8e5a0d890ea48edc8655` |
| `pacote/codigo/extrair_ramos_v410.py` | 3191 | `4ee58e1fc9f663781e37ee8ddd2991108843006bed062f06c32eb6c727a7dcd3` |
| `pacote/codigo/gerar_modulos_v411.py` | 10991 | `4f877ccd11b37ff9204e4ddc27d7bcbdd8ec33609c8fccafc9e3fae14a0ff6ef` |
| `pacote/codigo/gerar_pinos.py` | 1098 | `a49daf7a2b781818ca9c87b183f8965b1036412b861ac77b9ebe10460ffaaaa6` |
| `pacote/codigo/gerar_ramos_v411.py` | 5214 | `458ff78c0bdb71b6eba62f28aa9e9513d4e4754e056926fdfc1ae6a118f6cc63` |
| `pacote/codigo/preparar_estimador_s0.py` | 13960 | `2e429608fc64f1d08a3ad77de380db7630ea14c7d78accdc817180d7624dfe7f` |
| `pacote/codigo/testes_sinteticos.py` | 65946 | `009e1c94fa261afefcd27c4e5b88874cb176d9fcbe97c606fd02d931d89438a5` |
| `pacote/codigo/veredito_v411.py` | 2818 | `4a33389a01067e80f2675e19529a0e2017b37e1c52064cfb2e4277b097a730e1` |
| `pacote/producao/RAMOS_V411.json` | 1212 | `47624a41242869708b61ccbd4fc55d6af186846da1eec81661ccf12013cf4c43` |
| `pacote/producao/RAMOS_V411_ORIGEM.json` | 1176 | `d809c55f4049ef7fa7b6088f7f25ec2fe635a8b41636f12c493a287f50097cc9` |
| `pacote/producao/RECIBO_SEGUNDA_CONSTRUCAO.json` | 9201 | `37672c956687796d6ccf5f148ffc67713b6bbcc3dedd65dfbb572e68f6b1ac8b` |
| `pacote/producao/segunda_construcao.py` | 17488 | `55226301442393ae77bf333fbf588b52abcfa0b9c44c9cd3a69d0613fa36c39e` |
| `pacote/producao/vetor_y255.npz` | 2318 | `536b07e222e57732dc1075880038d73845e61b0c53eadf9880041576141ff131` |

Testes do pacote (só vetores sintéticos, semente fixa): 22 testes (T1 a T22), todos passam (`artefatos\TESTES_SINTETICOS.json`). A gerência reexecutou o pacote numa cópia isolada depois de cada rodada: código regenerado e matrizes iguais bit a bit.
