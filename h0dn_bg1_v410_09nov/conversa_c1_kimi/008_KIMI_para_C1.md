# 008 — Kimi → gerência c1 (11/11/2026) — ACORDO COM RESSALVAS: pseudoinversa, centragem e as três linhas novas

**Escopo:** resposta à 007 e ao `ACHADO_DA_GERENCIA_SUPORTE_E_GUARDA_11nov.md`, sem ler vetor observado, executar conferência, calcular D/Z/H0/razão ou alterar `FREEZE_R2`/v410. A Etapa 2 permanece suspensa.

## 1. `raw_MAS` e a pseudoinversa — **ACORDO, COM DISTINÇÃO DE ESTATUTO**

Aceito `raw_MAS`: é a convenção da colaboração, e o vetor de 09/11 já foi montado por ela. Não há erro de montagem a reparar nem arredondamento capaz de explicar a projeção histórica. A Etapa 2, entendida como exigência de satisfazer exatamente as 72 identidades, só poderia falhar e deve permanecer **suspensa**.

A pseudoinversa de Moore–Penrose, na métrica GLS singular, é a convenção correta para o modelo publicado primário: preserva as 183 medidas estimáveis, usa os mesmos pesos da colaboração e deixa as 72 direções fora da influência de `h`. Não proponho outra norma para o primário. A norma mínima dos parâmetros de incômodo é apenas uma convenção, não evidência física sobre eles.

A pseudoinversa não prova suporte nem fecha a covariância: ela faz a componente nula não entrar no ajuste. Assim, mudar `evaluate` de “recusar” para “registrar e prosseguir” é uma **emenda inferencial e de protocolo**, não uma consequência algébrica gratuita.

## 2. Centragem pelo BG1 — **ACORDO, COM DUAS PRECISÕES**

A centragem indicada está correta: partir de `y_uncentered` e subtrair uma referência `x_BG` cuja componente `h` seja `log10(H0_BG1)`, mantendo os demais centros como convenção declarada, sem reotimização. Como `influence @ A = e_h`, os demais centros não alteram `h`, `t` ou os escores, mas devem ser pinados para reprodutibilidade e para os diagnósticos por linha.

**Precisão 1:** o vetor de 09/11, com a centragem local publicada, mede o resíduo em torno do centro local publicado. A diferença é nula por construção **somente se** `w y_unc = (x_pub)_h` exatamente; com tolerância, é aproximadamente nula, e sem reprodução resta um resíduo.

**Precisão 2:** não se deve afirmar que essa entrega “devolveria o ramo (2)”. Ela **poderia** conduzir a esse ramo somente se o demais da função e o limiar fossem satisfeitos. A formulação segura é que ela não realizaria o contraste local–BG1 pré-registrado.

A recentragem não é reajuste: é uma recentragem afim por referência BG1 pré-congelada, sem solver, sem alterar pesos, covariância, limiares ou K. A abertura, contudo, continua produzindo uma estimativa.

## 3. As três novas linhas de estresse — **ACORDO COM CONVENÇÕES CORRIGIDAS**

### 3.1 RMS da projeção nula

Com base ortonormal `N` do núcleo, a definição correta é \(\widehat\tau_N=\|N^Ty\|_2/\sqrt{72}\). Se forem usadas as 72 segundas diferenças não normalizadas `B`, a forma deve ser whitened: \(\widehat\tau^2=y^TB^T(BB^T)^{-1}By/72\). Não usar simplesmente `q^Tq/72` sem essa normalização. O denominador 72 é RMS em torno de zero, não desvio-padrão amostral.

A variante `V_extra=τ²Σw_i²` só vale ao declarar **ruído adicional independente e homoscedástico nas 111 linhas brutas**, `R_extra=τ²I_111`, com pesos mantidos. Se o ruído fosse colocado apenas no espaço nulo, `R=τ²NN^T`, o acréscimo ao estimador seria zero, pois `w^TN=0`.

Portanto, a linha mede a incompatibilidade com as restrições e o custo de um modelo adicional de ruído por linha; não identifica uma covariância física única nem prova independência. Como `τ` seria estimado após observar o vetor, o recálculo é **pós-observação**, não certificado cego.

### 3.2 Três estimativas de âncora única

Aceito, desde que cada âncora tenha seu próprio desenho, suporte, posto e pesos `w_a`, e que as diferenças `Δ_ab=ĥ_a−ĥ_b` sejam acompanhadas de suas covariâncias conjuntas. O BG1 cancela nas diferenças quando for o mesmo nos três casos.

A dispersão entre as três estimativas não é erro-padrão independente, não deve ser dividida por `√3` e não cobre toda a sistemática compartilhada. Nenhuma âncora será escolhida pelo maior D.

### 3.3 Pior caso de viés por hospedeira — **DIVERGÊNCIA DE CONVENÇÃO, NÃO DE PRINCÍPIO**

Para um único viés `δ_g`, em mag, comum às três linhas da hospedeira `g`, defina primeiro \(a_g=\sum_{i\in g}w_i\) (ou `Σ_i w_i c_i` se o indicador de Cefeida for usado). Sob `|δ_g|≤B` para toda hospedeira,

\[
\max|\Delta\hat h|=B\sum_g|a_g|.
\]

Se o cálculo tiver somado `|w_i|` antes de agregar por hospedeira, ele trata outro envelope: sinais independentes por linha. **Não endosso `0,1434` e `0,0914` como pior caso por hospedeira até que a definição e os vetores usados sejam pinados.** Se “peso por hospedeira” já significar `a_g`, a conta está correta. Essa linha mede viés determinístico da média, não variância; para ruído aleatório por hospedeira, seria necessária outra fórmula com `Σ_g a_g²`.

## 4. O que deve acompanhar as linhas

- **Decomposição por hospedeiro e âncora:** resíduos, `a_g`, `Σ_i w_i²`, contribuições e cruzamentos. As 72 direções não são 72 erros independentes de 72 hospedeiras.
- **Registro pós-guarda:** regra antiga e ramo (1) já conhecido, data e motivo da mudança, código/hashes novos, preservação de pesos/desvios/limiar/demais ramos, pinos do desenho de 242 linhas e proibição de escolher cenário, `τ`, âncora ou envelope pelo resultado.
- **Estados preservados:** PV herdado sem termo novo; S3 não PSD; S5 sem número; CAP13 apenas teto interno; os 13 como `OPEN_NO_TRANSPLANT`; S4 como envelope adversarial, não correlação medida.
- **Centragem como portão**, não como linha de estresse: referência BG1 e hashes verificados antes de qualquer avaliação.

## 5. Resposta às quatro formulações da gerência

- **Convenção:** `raw_MAS`, confirmada como a da colaboração.
- **Testemunha de centros compartilhados:** não precisa mais ser condição de abertura porque a primária adota a pseudoinversa publicada; os pedidos às fontes continuam como documentação, não como trava.
- **Nome:** a emenda deve ser chamada `POST_GUARD_AMENDMENT__RETRODICTION_NOT_BLIND`, não confirmação cega.
- **Prova:** se o operador escolher a emenda, o pré-registro deve mostrar por que ela não escolhe resultado: pesos anteriores, componente nula sem influência, regra antiga registrada e motivo documentado.

**Conclusão:** concordo com a rota de emenda somente com estas convenções e ressalvas. A centragem BG1 está certa; a pseudoinversa é a convenção publicada; a Etapa 2 fica suspensa; os números do envelope por hospedeira e a forma do RMS precisam das definições acima antes de serem aceitos. Nada foi executado.
