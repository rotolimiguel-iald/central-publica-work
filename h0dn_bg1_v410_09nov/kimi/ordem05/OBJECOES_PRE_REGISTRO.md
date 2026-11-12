# ORDEM 05 — objeções ao pré-registro V411

**Parecer:** `OBJECOES_MATERIAIS__NAO_SELAR_SEM_RESOLVER`  
**Data da revisão:** 2026-11-11  
**Método:** revisão documental e estática; nenhuma rotina científica foi executada.

## 1. Conclusão executiva

A recentragem pelo BG1 está presente e correta; a reprodução da colaboração usa a mesma convenção explícita de pseudoinversa do `solver.py`; a projeção fora do suporte é registrada somente depois do portão; e os diagnósticos de coerência não alimentam portão nem veredito. Não encontrei erro numérico demonstrado nesses pontos com os artefatos pinados.

Há, contudo, objeções materiais que devem ser resolvidas antes do selo:

1. falta a etiqueta obrigatória `POST_GUARD_AMENDMENT__RETRODICTION_NOT_BLIND`; no ramo 4, justamente o previsto pelos agregados, também se perde o sufixo genérico `RETRODICTION_WITHOUT_FIT` por omissão na dependência de veredito;
2. o registro pós-guarda está apenas parcial no rascunho e não é vinculado, pelo hash do pré-registro selado, à saída do executor;
3. as três âncoras não vêm acompanhadas das diferenças pareadas e covariâncias conjuntas exigidas na mensagem 008;
4. faltam as decomposições por hospedeira e por âncora que devem acompanhar as linhas novas;
5. o modelo de ruído da linha (i) não declara no pré-registro, de forma explícita, independência, homoscedasticidade e seu caráter pós-observação;
6. a grade do envelope por hospedeira não coincide entre texto e código, e a fórmula verbal admite duas agregações diferentes;
7. uma falha da conferência de centragem produz recusa de integridade sem saída, não ramo 1; o contrato textual precisa dizer sem ambiguidade qual das duas consequências é a pré-registrada;
8. a abertura não confere ortonormalidade/nulidade da base, posto 170, 111 linhas tocadas nem a coerência dos agregados auxiliares dos estresses; a preparação e os pinos mitigam, mas a guarda de abertura, sozinha, não basta.

As objeções O01–O08 são materiais de protocolo, inferência ou verificação, não meros problemas de estilo. O09 é uma divergência moderada de custódia; O10–O11 são lacunas formais de menor grau. Nenhuma dessas objeções autoriza afirmar que o estimador primário esteja numericamente errado.

## 2. Fontes, alcance e hashes

### 2.1 Arquivos principais revisados

| arquivo | bytes | SHA-256 medido nesta revisão |
|---|---:|---|
| `EMENDA_E_PRE_REGISTRO_V411_rascunho.md` | 22638 | `d84edbdc02e15bd4c6da6726076df9eaecf0f9efa2ecdd178bcf53ed078a8d68` |
| `codigo/abertura_v411.py` | 24108 | `13f88cf8b8626b0ec5330aec5d0ddd3186aa73d5de271cb154fc26f0b5b5056b` |
| `codigo/executar_abertura_v411.py` | 7498 | `45869ac339ad9fc660b9362646a47c763684446f36dc6505e1e4af610de5736b` |

Os dois hashes de código coincidem com os declarados no rascunho, linhas 46, 168 e 171. O rascunho continua expressamente não pinado em sua linha 3; o hash acima identifica os bytes da edição de 19:35 efetivamente revisados ao final.

**Controle de versão durante a revisão:** a primeira leitura foi da edição de 19:12, com 20988 bytes e SHA-256 `4c9146470f933007060c227122baa40c28d31d5adcdf920724988930e810e072`. O rascunho foi atualizado por outro processo para a edição de 19:35, sem alteração dos dois códigos. Reli integralmente a edição atual: ela acrescenta proveniência do artefato na linha 35, declara ensaio de produção na linha 46, atualiza a seção 10 e amplia os pinos. As objeções continuam aplicáveis; as duas referências fora das seções 3–7 foram ajustadas para as linhas atuais. Não restaurei nem editei o rascunho.

### 2.2 Fontes estáticas auxiliares abertas só para verificar importações e convenções

| arquivo | SHA-256 medido nesta revisão |
|---|---|
| `conversa_c1_kimi/008_KIMI_para_C1.md` | `7dba8f32136bf4078ac84a8215fca472393d520b1561782ff723c09fe2a4890b` |
| `codigo/estimator_v411.py` | `af3908441a4f0a8d38a77b1ac836bc6ee47ac07f3b6f77cb9ef8305f64682333` |
| `codigo/veredito_v411.py` | `4a33389a01067e80f2675e19529a0e2017b37e1c52064cfb2e4277b097a730e1` |
| `codigo/preparar_estimador_s0.py` | `2e429608fc64f1d08a3ad77de380db7630ea14c7d78accdc817180d7624dfe7f` |
| `artefatos/MANIFESTO_S0.json` | `51753d34e812eaecda5eb6f396106f853350deb006c9bf3053fb5d9c4fdb0440` |
| `artefatos/RAMOS_V410.json` | `6f7e52c5433f770c16a50c3d79a1b7c4e562f5ee83fb445db251733abe3fcb83` |
| `solver.py` da colaboração | `d44ac2d7d2f8b0ec8d2b33ebdc7102397010efe7135bc3ec30ba014d8ccf0136` |

A comparação principal é com as seções 3–7 do rascunho. A mensagem 008 é usada nos pontos expressamente pedidos pela ORDEM 05: recentragem, registro pós-guarda, etiqueta de retrodição não-cega, convenções das três linhas novas e pseudoinversa. Não reabri PV, S3, S5, CAP13 nem os estados de S1/S2/S4.

## 3. Flags de não execução

Nesta revisão:

- `abertura_executada = false`;
- `abrir_executado = false`;
- `evaluate_executado = false`;
- `solver_executado = false`;
- `testes_sinteticos_executados = false`;
- `vetor_observado_aberto = false`;
- `y_obs_aberto = false`;
- `np_load_sobre_vetor_observado = false`;
- `estimativa_calculada = false`;
- `H0_calculado = false`;
- `D_calculado = false`;
- `razao_calculada = false`;
- `Z_calculado = false`;
- `pesos_recalculados = false`;
- `agregados_recalculados = false`;
- `S1_S2_S4_recalculados = false`;
- `BG1_reprocessado = false`;
- `codigo_ou_pre_registro_alterado = false`.

Foram feitos somente leitura de texto, busca textual, contagem de bytes/linhas e SHA-256 de arquivos-fonte. Os números da seção 5 e os números de desenho citados abaixo são transcrições, não recomputações. Os 18 testes sintéticos declarados no rascunho não foram reexecutados nem validados por esta revisão.

## 4. Objeções materiais, com linhas exatas

### O01 — `MATERIAL_ALTA__ROTULAGEM_POS_GUARDA_E_NAO_CEGUEIRA`

**Achado confirmado.** A etiqueta exigida `POST_GUARD_AMENDMENT__RETRODICTION_NOT_BLIND` está ausente do rascunho, dos dois programas e da dependência de veredito. Além disso, o ramo 4 não concatena nem o sufixo genérico de retrodição.

**Evidências:**

- a mensagem 008 fixa o nome em `008_KIMI_para_C1.md:60`;
- o rascunho declara «retrodição sem ajuste» em `EMENDA...md:79` e prevê o ramo 4 em `EMENDA...md:79,94`;
- a palavra literal da marca da emenda ainda aparece como pendente, com candidatas não ratificadas, em `EMENDA...md:138`;
- a saída do executor contém versão, pinos, alvos e resultado, mas nenhum campo de emenda/cegueira em `executar_abertura_v411.py:147-150`;
- o sufixo genérico é definido em `artefatos/RAMOS_V410.json:33`;
- os ramos 1, 2, 3, 5 e 6 concatenam `suf_` em `veredito_v411.py:23-28,31-34`;
- o ramo 4 retorna apenas `_v410_h0dn_cabeca(...) % n`, sem `+ suf_`, em `veredito_v411.py:29-30`;
- as partes do ramo 4 contêm validade/não-creditação/gate, mas não `RETRODICTION_WITHOUT_FIT`, em `RAMOS_V410.json:19-23`;
- a chamada ao veredito primário e à linha inseparável ocorre em `abertura_v411.py:401-407`.

**Impacto:** a superfície mais provável pode omitir tanto a natureza pós-guarda/não-cega quanto a etiqueta genérica de retrodição. Não muda estimador ou escore; muda materialmente a descrição epistêmica do resultado.

**Antes do selo:** aplicar a etiqueta literal exigida a toda superfície e corrigir a composição do ramo 4, preservando a palavra do operador sobre a cabeça.

### O02 — `MATERIAL_ALTA__REGISTRO_POS_GUARDA_PARCIAL_E_NAO_VINCULADO_A_SAIDA`

**Achado confirmado.** O registro pós-guarda existe em parte no texto, mas falta a cláusula explícita de não seleção de cenário/`τ`/âncora/envelope pelo resultado, e a saída não carrega o hash do pré-registro que autoriza a emenda.

**O que já está presente:**

- regra antiga, ramo 1 conhecido, data e motivo: `EMENDA...md:7-9,15-18,22-31`;
- preservação de pesos, desvios, limiar e demais ramos: `EMENDA...md:18-20,29`;
- pino do desenho S0 de 242 linhas: `EMENDA...md:39,167`;
- hashes dos códigos novos: `EMENDA...md:46,168,171`;
- projeção registrada depois do portão: `abertura_v411.py:375-400`.

**O que falta:**

- a lista completa exigida para o registro está em `008_KIMI_para_C1.md:49-54`;
- o texto só enuncia genericamente «não escolher o melhor modelo» em `EMENDA...md:20`; não proíbe nominalmente escolher cenário, `τ`, âncora ou envelope depois do resultado;
- os únicos insumos de arquivo pinados pelo executor são `rede`, `congelado`, `s0`, `bg`, `readme`, `ramos` e `vetor`, em `executar_abertura_v411.py:26-28,43-74`; o pré-registro/emenda não é um deles;
- a saída não contém `pre_registro_sha256`, regra antiga, motivo/data da emenda ou declaração de preservação, em `executar_abertura_v411.py:147-150`.

**Impacto:** o arquivo de resultado, isoladamente, não estabelece qual texto selado autorizou a mudança nem impede documentalmente seleção pós-resultado de linhas auxiliares. A existência do rascunho ao lado não substitui a vinculação criptográfica.

**Antes do selo:** completar o registro e incluir no pacote/saída o hash do texto efetivamente selado e os hashes old/new pertinentes.

### O03 — `MATERIAL_MEDIA__ANCRAS_SEM_COVARIANCIAS_PAREADAS`

**Achado confirmado.** O código produz cada âncora contra o primário e uma dispersão `max-min`, mas não produz as diferenças âncora–âncora nem suas covariâncias conjuntas.

**Evidências:**

- a exigência de `Δ_ab` com covariâncias conjuntas está em `008_KIMI_para_C1.md:33-37`;
- o rascunho promete somente as três estimativas e a dispersão em `EMENDA...md:115`;
- os pares de coerência são primário/rede completa, Cefeidas livres/primário e cada âncora/primário em `abertura_v411.py:292-309`;
- a coerência calcula `dif`, `sd_dif` e `z_dif` somente para esses pares em `abertura_v411.py:312-320`;
- a linha de âncora única guarda resultados individuais e `T.max-T.min` em `abertura_v411.py:421-437`;
- não há par `N4258–LMC`, `N4258–MW` ou `LMC–MW` com covariância nessa saída.

**Impacto:** âncora/primário não substitui a covariância conjunta entre as três estimativas; a dispersão não é erro-padrão independente. O código corretamente não divide por `√3`, mas também não entrega o objeto exigido para interpretar as diferenças.

**Antes do selo:** acrescentar diferenças pareadas e covariâncias conjuntas, mantendo a ressalva de sistemática compartilhada e a proibição de escolher âncora pelo resultado ou por D.

### O04 — `MATERIAL_MEDIA__DECOMPOSICOES_EXIGIDAS_AUSENTES_DA_SAIDA`

**Achado confirmado.** Não são publicados no resultado os resíduos, `a_g`, `Σ_i w_i²`, contribuições e cruzamentos por hospedeiro e âncora exigidos pela mensagem 008.

**Evidências:**

- a exigência está em `008_KIMI_para_C1.md:49-53`;
- o rascunho traz apenas os resumos numéricos em `EMENDA...md:112-116`;
- a linha (i) devolve `tau_hat`, desvios agregados, escores e D em `abertura_v411.py:411-420`;
- a linha (ii) devolve estimativas, escores, D, suporte e dispersão em `abertura_v411.py:421-437`;
- a linha (iii) devolve apenas `delta_t` e limites agregados de escore em `abertura_v411.py:438-445`;
- o preparador declara salvar `touched`, `sum_w2_touched`, `s_host` e `host_names` no artefato de desenho em `preparar_estimador_s0.py:177-186`, mas o executor não os expõe como decomposição no resultado.

**Impacto:** o resultado não permite auditar, por si só, quais hospedeiras/âncoras dominam `τ`, o envelope ou as diferenças. Não é evidência de fórmula errada; é omissão material de auditabilidade.

### O05 — `MATERIAL_MEDIA__MODELO_DE_RUIDO_DA_LINHA_I_SUBESPECIFICADO`

**Achado confirmado.** A fórmula implementada é a correta para base ortonormal, mas o pré-registro não declara completamente o modelo estocástico nem o estatuto pós-observação de `τ`.

**Evidências:**

- independência e homoscedasticidade nas 111 linhas, com `R_extra=τ²I_111`, são exigidas em `008_KIMI_para_C1.md:25-31`;
- o rascunho diz apenas «ruído por linha nas 111 linhas» em `EMENDA...md:114`;
- o comentário do código declara independência, e um único `tau_hat` multiplica `sum_w2_touched`, em `abertura_v411.py:412-420`;
- a estimação usa `support_l2/sqrt(nnull)` em `abertura_v411.py:414-417`, coerente com `||Nᵀy||₂/√72` somente se `N` for ortonormal e tiver 72 colunas;
- `support_l2` é a norma da projeção nula em `estimator_v411.py:75-88`;
- a mensagem 008 classifica o recálculo como pós-observação e não certificado cego em `008_KIMI_para_C1.md:31`; o rascunho não o diz nessa linha específica.

**Impacto:** «ruído por linha» não distingue, sem a declaração, `τ²I_111` de ruído no espaço nulo, cuja contribuição ao estimador seria nula. Também fica obscurecido que `τ` é estimado do vetor no rito.

**Antes do selo:** nomear ruído adicional independente e homoscedástico nas 111 linhas brutas, pesos mantidos, RMS em torno de zero e caráter pós-observação/não-cego.

### O06 — `MATERIAL_MEDIA__ENVELOPE_POR_HOSPEDEIRA_AMBIGUO_E_GRADE_DIVERGENTE`

**Achado confirmado em duas partes.**

1. **Convenção verbal ambígua; código correto.** «Soma dos módulos dos pesos por hospedeira» em `EMENDA...md:116` pode ser lida como `Σ_g Σ_i|w_i|`. A convenção acordada é `Σ_g |Σ_(i∈g) w_i|`, conforme `008_KIMI_para_C1.md:39-47`. O código faz primeiro a soma com sinal por hospedeira em `preparar_estimador_s0.py:112-125`, e só depois toma módulos e soma em `abertura_v411.py:438-444`. Portanto, o código implementa a convenção correta; o texto deve ser tornado inequívoco.
2. **Grade texto–código diferente.** O texto menciona 0,05 mag e os limiares 0,0156 e 0,1816 mag em `EMENDA...md:116`. A abertura fixa `TAUS_B=(0.02,0.05)` em `abertura_v411.py:31` e só itera esses dois valores em `abertura_v411.py:440-445`. O valor 0,02 aparece no código sem constar da linha correspondente do texto; os dois limiares do texto não são campos dessa saída.

**Impacto:** a primeira parte pode mudar inteiramente o envelope se a frase for implementada por outra pessoa; a segunda impede correspondência um-a-um entre o pré-registro verbal e a superfície publicada. Não altera o veredito primário.

**Antes do selo:** escrever a fórmula com a ordem das agregações e fixar uma única grade/conjunto de limiares antes da abertura, sem escolha posterior pelo resultado.

### O07 — `MATERIAL_MEDIA__FALHA_DE_CENTRAGEM_COMO_RECUSA_NAO_COMO_RAMO_1`

**Achado confirmado de diferença de contrato, não de fórmula.** A recentragem está certa, mas sua conferência falha por recusa dura de integridade, sem JSON de resultado; não por ramo 1.

**Evidências:**

- o rascunho define recusas e portão em `EMENDA...md:48-59`;
- a mensagem 008 pede «centragem como portão» em `008_KIMI_para_C1.md:54`;
- `1c` só é avaliada quando `1b.reproduz` é verdadeiro em `abertura_v411.py:352-361`;
- inconsistência dos pesos ou de `1c` levanta `ValueError("integridade: ...")` em `abertura_v411.py:362-365`;
- `portao_1_ok` é somente `b1.reproduz and d1.ok` em `abertura_v411.py:368-375`;
- o executor transforma esse `ValueError` em código 3 e «nada gravado» em `executar_abertura_v411.py:142-146`;
- ramo 1 com `estatistica/coerencia/estresse=None` ocorre apenas quando `portao_1_ok` é falso em `abertura_v411.py:375-381`.

**Impacto:** há dois desfechos operacionalmente distintos para o que a linguagem «portão de centragem» pode designar. A classificação como erro de fiação é defensável — depois de 1b, a identidade deveria valer —, mas precisa ser explícita no pré-registro para não converter uma recusa esperada em ramo científico ou vice-versa.

### O08 — `MATERIAL_MEDIA__GUARDA_NAO_CONFERE_BASE_POSTO_E_AUXILIARES_DOS_ESTRESSES`

**Achado de lacuna de verificação, não de valor atual errado.** A abertura confere formas parciais e ortogonalidade aos pesos/covariância, mas não confere as propriedades das quais dependem o RMS e a impressão digital.

**Evidências:**

- o texto fixa posto 170, 72 direções e 111 linhas em `EMENDA...md:39,57,114`;
- a abertura verifica formas de `weights/null_basis`, `W@N` e `C@N` em `abertura_v411.py:189-215`, mas não `N.shape[1]==72` nem `NᵀN=I`;
- o RMS divide pela quantidade de colunas da base fornecida em `abertura_v411.py:414-417`;
- `sum_w2_touched` e `s_host` são consumidos diretamente em `abertura_v411.py:412,438-444`, sem reconferência contra pesos, linhas tocadas e nomes de hospedeiras na abertura;
- a preparação, não a abertura, confere posto 170/nulidade 72 em `preparar_estimador_s0.py:77-98` e 111 linhas tocadas em `preparar_estimador_s0.py:104-110`;
- a base produzida por `geometry` vem de autovetores e é ortonormal por construção em `estimator_v411.py:27-39`;
- o manifesto registra posto 170, nulidade 72 e tolerância de geometria em `MANIFESTO_S0.json:95-103`, e 111 linhas em `MANIFESTO_S0.json:156-159`.

**Impacto:** com o NPZ correto e seu pino, a convenção está documentada; uma base escalada/não ortonormal ou auxiliares incompatíveis poderiam, porém, atravessar parte da guarda se os pinos fossem coerentemente substituídos. Não afirmo que o artefato pinado atual tenha esse defeito.

### O09 — `DIVERGENCIA_MODERADA_DE_CUSTODIA__UMA_VEZ_HASH_E_AUTOPINO`

Três limites concretos ficam fora da descrição resumida «feita uma vez» e «resultado gravado com hash» de `EMENDA...md:46`:

1. **Uma vez por nome de saída, não global.** O executor recusa apenas uma `--saida` já existente em `executar_abertura_v411.py:104-110,158-162`. Uma nova execução com outro nome não é bloqueada por registro de abertura.
2. **Hash impresso, não persistido ao lado.** O JSON é montado sem autohash em `executar_abertura_v411.py:147-150`; o SHA-256 é calculado e impresso no `stdout` em `executar_abertura_v411.py:163`, sem sidecar `.sha256`. Se o console for custodiado, a exigência pode ser satisfeita operacionalmente; o arquivo sozinho não a carrega.
3. **O executor em curso não é executado dos bytes autoconferidos.** Ele lê e confere seu próprio arquivo em `executar_abertura_v411.py:69-73`, mas `carregar_codigo` só executa dos bytes conferidos `estimator`, `veredito` e `abertura` em `executar_abertura_v411.py:77-87`. A afirmação ampla de que todo o código é carregado dos mesmos bytes conferidos, no docstring `executar_abertura_v411.py:8-10`, não vale literalmente para o executor já em curso.

São limites de custódia, não evidência de resultado alterado. Uma política externa de nome único, captura do `stdout` e lançador verificado pode mitigá-los.

### O10 — `FORMAL_BAIXA__CHAVE_YVAL_E_RAW_MAS_NAO_IMPOSITAS_PELO_EXECUTOR`

O texto exige `yval`, convenção `raw_MAS`, sem centragem, em `EMENDA...md:35`. O executor aceita qualquer `vetor.chave` não vazia em `executar_abertura_v411.py:47-48` e carrega essa chave em `executar_abertura_v411.py:137-143`; não exige o literal `yval` nem registra um campo `convencao="raw_MAS"`.

O pino do arquivo, o portão 1 e a recusa de precisão simples mitigam fortemente o risco. Não há evidência de chave errada; a lacuna é de imposição/rastreabilidade formal. A flexibilidade também é usada pelos testes sintéticos, portanto eventual correção deve distinguir produção de ensaio.

### O11 — `FORMAL_BAIXA__COERENCIA_EM_H_LOG10_NAO_EM_H0_LINEAR`

O rascunho chama os diagnósticos de diferenças entre estimativas de «H0» em `EMENDA...md:61-65`. O código calcula `wa@y-wb@y` em `abertura_v411.py:312-319`, isto é, diferenças de `h=log10(H0)` segundo a estatística definida em `EMENDA...md:59` e os pesos usados em `abertura_v411.py:292-308`.

A implementação é coerente com o estimador e com a notação `ĥ` da mensagem 008. O texto deveria dizer explicitamente `h=log10(H0)` para evitar atribuir unidade errada a `dif`; os escores padronizados não mudam por essa correção editorial de contrato.

## 5. Portão 1 — tolerâncias e consequências

### 5.1 Tolerâncias externas do portão

| item | regra implementada | tolerância | linhas |
|---|---|---:|---|
| H0 da colaboração | diferença absoluta `<= TOL_H0` | `0,5e-4 = 0,00005` km/s/Mpc | `abertura_v411.py:26,340-346` |
| desvio publicado | diferença absoluta `<= TOL_SIG` | `0,5e-4 = 0,00005` km/s/Mpc | `abertura_v411.py:26,340-346` |
| qui-quadrado | diferença absoluta `<= TOL_CHI2` | `0,5e-4 = 0,00005` | `abertura_v411.py:26,340-346` |
| graus de liberdade | igualdade inteira com o README | exatamente o alvo; o texto fixa 119 | `abertura_v411.py:91-92,107-108,342-346` |
| impressão digital | diferença absoluta `<= TOL_FP` | `1e-9`, na unidade da projeção em mag | `abertura_v411.py:27,368-375` |

Os três `0,5e-4` implementam corretamente «meia unidade da quarta casa» do rascunho, linha 56. A comparação é inclusiva (`<=`). A impressão digital é `max(abs(y@null_basis))` em `abertura_v411.py:111-112`; seu alvo vem de `alvo_fp`, não do README, em `executar_abertura_v411.py:49-56,127-129`.

`1b.reproduz` exige H0, desvio, qui-quadrado e ndof simultaneamente; `portao_1_ok` exige `1b.reproduz` e `1d.ok` em `abertura_v411.py:339-375`. O texto chama os dois itens de (a) e (b); o código usa os rótulos internos `1b` e `1d`.

### 5.2 Tolerâncias internas associadas

| conferência | regra/tolerância | linhas |
|---|---|---|
| peso congelado contra `logh` da colaboração | absoluta `<= 1e-10` | `abertura_v411.py:28,352-356,362-363` |
| identidade de centragem `1c` | absoluta `<= 1e-10` | `abertura_v411.py:28,357-365` |
| pesos·desenho, pesos·nulo, C·nulo | máximo absoluto estritamente `< 1e-9` | `abertura_v411.py:29,189-215,249-271` |
| consistência `local0` com `local255[keep]` | máximo absoluto `<= 1e-12` | `abertura_v411.py:383-390` |
| igualdade de `logK` entre S0/congelado/BG1 | absoluta `<= 1e-15` | `abertura_v411.py:217-228` |
| gradientes entre S0/congelado/BG1 | máximo absoluto `<= 1e-15` | `abertura_v411.py:224-228` |
| H0 entre S0/congelado/BG1 | absoluta `<= 1e-12` | `abertura_v411.py:229-233` |
| desvios recalculados | relativa `<= 1e-12` | `abertura_v411.py:30,236-246` |
| D contra `logK/sd_null` | diferença absoluta `<= 1e-12` | `abertura_v411.py:241-246` |
| limiar/faixa de 95 % | igualdade a `5.0` e `1.959963984540054` | `abertura_v411.py:273-281` |

Essas conferências internas são recusas de integridade; em particular, `1c` não entra como terceiro fator booleano de `portao_1_ok`. Ver O07.

## 6. Recentragem BG1 e registro pós-portão — verificação positiva

A recentragem está correta e não é reajuste:

1. `x_ref` tem zeros e recebe `log10(H0_BG1)` apenas na coluna `h` em `abertura_v411.py:349-350`;
2. `local255 = y - A@x_ref` em `abertura_v411.py:351`;
3. a identidade `w0@local255 = logh_colaboração-log10(H0_BG1)` é conferida em `abertura_v411.py:352-365`;
4. o S0 repete a referência somente em `h_index_s0` em `abertura_v411.py:383-388`;
5. a equivalência com o recorte da rede completa é conferida em `abertura_v411.py:389-390`;
6. as âncoras recebem `local255[keep_a]`, portanto a mesma recentragem, em `abertura_v411.py:424-428`;
7. o BG entra como vetor de parâmetros zero em `abertura_v411.py:391-393`, sem reotimização;
8. os demais centros são zero por convenção explícita no código e são irrelevantes para `h` porque `pesos·desenho=e_h`, conferido em `abertura_v411.py:189-215`.

O registro da projeção ocorre somente depois de o portão passar: o retorno precoce está em `abertura_v411.py:375-381`; `evaluate` é chamado em `abertura_v411.py:391-397`; `support_max_abs` e `support_l2` são gravados em `abertura_v411.py:398-400`. A dependência registra e prossegue, sem antiga guarda, em `estimator_v411.py:62-88`.

## 7. Seção 5 — o que os agregados públicos permitem prever

**Tudo nesta seção é transcrição do rascunho, linhas 67–79; nada foi recalculado.**

Os agregados públicos são o número local publicado `73,4988 ± 0,8088`, o fundo congelado `68,531 ± 0,301` e a previsão local da lei K `74,27`. O rascunho apresenta a conta pública agregada de `5,76` contra o nulo e `-0,90` contra K. Com pesos e desvios de desenho, sob o modelo publicado, ele registra:

| linha | Z esperado contra o nulo | chance de passar de 5 | Z esperado contra K |
|---|---:|---:|---:|
| primário, 13 fora | 5,83 | praticamente certa | -0,88 |
| Cefeidas livres | 4,51 | 23 % | -0,68 |
| só MW | 5,57 | 95 % | -0,84 |
| só LMC | 5,19 | 66 % | -0,78 |
| só N4258 | 4,06 | 10 % | -0,61 |

O que isso permite dizer antes da abertura:

- é **expectativa, não resultado**;
- se o portão passar, o primário é previsto no ramo 4 com `n=5`;
- a linha inseparável tende a ficar abaixo de 5;
- outro ramo primário exigiria afastamento da estimativa publicada por muitos desvios da diferença primário/rede completa, de desvio relativo 0,18;
- o rito confere uma conta já previsível por agregados; não descobre um número novo;
- é retrodição sem ajuste e, pela informação já disponível, **não é confirmação cega**.

Nenhum desses valores esperados deve ser usado como alvo de seleção ou apresentado como valor observado.

## 8. Pseudoinversa no modelo primário

### 8.1 Convenção

A convenção adequada é a de Moore–Penrose na métrica GLS singular usada pela colaboração. Não recomendo substituí-la por outra norma no primário. Ela preserva as direções estimáveis, dá peso zero às 72 direções nulas na influência de `h` e fixa a mesma solução publicada. A norma mínima dos parâmetros de incômodo é convenção algébrica, não evidência física sobre esses parâmetros.

A pseudoinversa não fecha a covariância física nem prova que o vetor pertence ao suporte. Registrar a projeção e prosseguir continua sendo uma emenda inferencial e de protocolo, não uma consequência gratuita da álgebra.

### 8.2 Conformidade estática do código

- o portão da rede completa usa `scipy.linalg.pinv(C, atol=1e-10, rtol=0.0, return_rank=True)` em `abertura_v411.py:95-108`;
- é exatamente a convenção do `solver.py:84-87`, e as fórmulas de ajuste/resíduo/qui-quadrado correspondem a `solver.py:104-113`;
- o primário S0 não chama `pinv` dentro de `abrir`: carrega pesos congelados em `abertura_v411.py:48-52,121-124`;
- na preparação do S0, `pinv(C0, atol=1e-10, rtol=0.0)` confere posto 170 em `preparar_estimador_s0.py:77-98`;
- os pesos efetivos vêm da `geometry` congelada, por decomposição espectral/SVD, e são comparados aos pesos da colaboração em `preparar_estimador_s0.py:77-103` e `estimator_v411.py:22-59`;
- o manifesto registra posto 170/nulidade 72 e as duas vias em `MANIFESTO_S0.json:95-103`.

Logo, não há troca oculta de norma no primário: há pesos congelados preparados pela geometria pinada e conferidos contra a pseudoinversa da colaboração. O08 registra a diferença entre essa garantia de preparação/pinos e o que a abertura reconferiria isoladamente.

## 9. As três novas linhas de estresse

### 9.1 Linha (i) — RMS da projeção nula e ruído por linha

**Conforme, condicionado à base ortonormal.** `support_l2/sqrt(nnull)` implementa o RMS em torno de zero, não desvio-padrão amostral, em `abertura_v411.py:414-417`; os pesos são mantidos e o acréscimo é `tau_hat²*sum_w2_touched` em `abertura_v411.py:412,417-420`.

**Pendências:** O05 e O08. O texto deve fixar `R_extra=τ²I_111`, independência/homoscedasticidade, 111 linhas brutas e caráter pós-observação. A abertura deveria garantir ou declarar como dependência pinada a ortonormalidade/nulidade 72.

Os números de desenho 0,035/0,10/0,104 mag do rascunho não foram recalculados.

### 9.2 Linha (ii) — três âncoras únicas

**Conforme parcialmente.** Cada âncora tem pesos, desenho, escalas e recorte próprios conferidos em `abertura_v411.py:249-272`; a avaliação usa o respectivo recorte recentrado em `abertura_v411.py:421-437`; recusas de preparação são preservadas em `abertura_v411.py:272,433-434`.

A dispersão é `max-min`, sem divisão por `√3`, em `abertura_v411.py:435-437`. Isso está correto como dispersão descritiva, mas não é erro-padrão independente.

**Pendências:** O03 e O04 — faltam covariâncias/diferenças pareadas e decomposições; nenhuma âncora pode ser escolhida pelo maior D ou pelo resultado.

### 9.3 Linha (iii) — viés por hospedeira

**Conforme na agregação algébrica.** O preparador calcula `a_g=Σ_(i∈g)w_i` com sinal em `preparar_estimador_s0.py:112-125`; a abertura calcula `delta=B*Σ_g|a_g|` em `abertura_v411.py:438-444`. Não é a soma de módulos linha a linha.

A faixa `z_null_min/max` corresponde a deslocar a estimativa por `±delta` mantendo o desvio, em `abertura_v411.py:441-444`. É envelope de viés determinístico da média, não variância aleatória por hospedeira.

**Pendências:** O06 — fórmula verbal ambígua e grade `0,02/0,05` versus menções textuais `0,05/0,0156/0,1816`; O04 — falta decomposição por hospedeira.

### 9.4 S1/S2/S4

Não recalculados, não reavaliados e não executados. A ausência de suas versões com dado nestes dois programas é coerente com a pendência de estimadores pinados declarada no rascunho atual, linha 140.

## 10. Diagnósticos de coerência

A implementação é estática e conceitualmente conforme, ressalvadas O03 e O11:

- primário contra rede completa e Cefeidas livres contra primário são definidos em `abertura_v411.py:297-303`;
- cada âncora contra o primário entra em `abertura_v411.py:302-303`;
- pesos são levados às 255 linhas por `_pad255` em `abertura_v411.py:285-289`;
- a variância da diferença usa a covariância completa e o vetor de diferença de pesos em `abertura_v411.py:305-308`;
- `z_dif=dif/sd_dif` é padronizado pelo desvio da própria diferença; também se publicam `sd_dif/sd_null_primario` e `sd_dif/sd_null_wa` em `abertura_v411.py:312-320`;
- os valores 0,18 e 0,63 citados no rascunho são razões de desvio de desenho, não foram recalculados;
- a coerência é calculada depois do veredito e não retorna a portão/veredito em `abertura_v411.py:401-409`;
- como usa diferenças de pesos do mesmo `h`, a referência BG1 e K cancelam conceitualmente; nenhum `logK` ou BG entra em `coerencia`.

A saída cobre os três tipos prometidos pela seção 4, mas não as covariâncias âncora–âncora exigidas pela mensagem 008.

## 11. Outras conformidades texto–código

- **242 linhas e 13 últimos calibradores fora:** `abertura_v411.py:168-183`, conforme `EMENDA...md:39,51`.
- **ordem dos dois modelos e linha inseparável:** `abertura_v411.py:32,163-166,401-407`; no ramo 1 a linha ao lado também é preenchida em `abertura_v411.py:377-380`.
- **vetor float64, 255 entradas finitas:** `abertura_v411.py:324-331`, conforme `EMENDA...md:35,52`.
- **pinos antes de carregar arrays:** `executar_abertura_v411.py:39-74,111-129`; no ensaio não há `np.load` do vetor e não se grava saída em `executar_abertura_v411.py:133-136`.
- **falha de 1b/1d impede estatística, coerência e estresse:** `abertura_v411.py:375-381`.
- **não escolha do melhor modelo:** não há maximização/seleção entre modelos; o veredito primário usa índice 0 e a outra linha fica ao lado em `abertura_v411.py:401-407`.
- **estresses não mudam veredito:** são calculados depois e em campo separado em `abertura_v411.py:401-445`.
- **S1/S2/S4:** nenhum estimador correspondente é executado pelos dois arquivos.

## 12. Limites desta revisão e condição de fechamento

Não abri o vetor, não conferi resultados de abertura, não reexecutei testes, não recalculei pesos/agregados/S1/S2/S4 e não verifiquei o recálculo externo pelo `um.py`. A promessa de que o `um.py` recalcula e reproduz, em `EMENDA...md:46`, não é implementada nem testada pelos dois arquivos revisados; fica como dependência externa, não como falha demonstrada.

**Condição recomendada para fechar a ORDEM 05:** resolver O01–O07 no texto/pacote; decidir e documentar O08; estabelecer a custódia de O09; e registrar O10–O11 como precisões formais. Depois disso, uma nova revisão estritamente estática pode verificar os diffs e os novos hashes, novamente sem abrir o vetor.
