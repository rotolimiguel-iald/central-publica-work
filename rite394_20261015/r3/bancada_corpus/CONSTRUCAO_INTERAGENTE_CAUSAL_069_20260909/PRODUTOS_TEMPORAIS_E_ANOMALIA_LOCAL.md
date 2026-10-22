# Construção causal da interação Einstein–sigma e localização da anomalia

09/09/2026. [DERIVED + KNOWN — aplicação demonstrada de teoremas analíticos, sem Lean]. Esta nota trata Q2 da entrega 068. Ela constrói a álgebra interagente auxiliar como expansão formal em torno do fundo físico e estabelece o contrato da primeira quebra local. A cohomologia que permite remover essa quebra continua uma obrigação distinta.

## 1. Enunciado e dados já disponíveis

Trabalhe em \(M=(0,\pi)\times S^3\), \(\bar g=dr^2-4\cos^2(r/2)\gamma\), \(\bar\phi=\mathrm{id}\), com a ação e parâmetros de 067. Testes e interações localizadas têm suporte compacto interior. A Cauchy S³ é compacta; os extremos temporais não são incluídos.

Entradas locais efetivamente usadas:

- [Jacobi 066](<C:/IALD/Central de Patentes/Chatgpt/QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md>): Hessiana D com parte principal normalizável, Q=CK e identidades de Green.
- [BRST 068](<C:/IALD/Central de Patentes/Chatgpt/EXTENSAO_BRST_COMPLETA_20260909_220941_811364/EXTENSAO_BRST_E_CORRECOES_SUAVES.md>) e [Feynman 068](<C:/IALD/Central de Patentes/Chatgpt/EXTENSAO_BRST_COMPLETA_20260909_220941_811364/ADENDO_FEYNMAN_PARIDADE_E_CONTATOS.md>): contrações completas, Ward livres e frente de onda.
- [Dicionário de ação graduada](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md>): P_gr, covariâncias com reciprocidade, ação BV quadrática e gauge fixado não linear que a reproduz.

**Teorema de alcance formal.** Para o modelo ambiente e o domínio acima, admitindo a classe completa de contratermos locais da ação efetiva, existem produtos temporais renormalizados locais e covariantes, coeficiente a coeficiente na expansão de flutuações e em ħ, com fatorização causal, simetria graduada, realidade/unitariedade formal, independência funcional dos campos, condições de escala/microlocais e identidade da ação por partes. Eles definem campos interagentes auxiliares e álgebras locais, via matrizes S relativas. A quebra da identidade BV é uma série local de número fantasma um, de ordem pelo menos ħ, com identidade de consistência. Se as ordens inferiores foram removidas, sua primeira ordem não nula é fechada pelo diferencial clássico modulo d.

Não se afirma neste enunciado que a quebra seja exata, que os observáveis físicos interagentes já estejam construídos, que haja estado interagente positivo global ou convergência das séries. Os itens seguintes verificam as hipóteses e a composição que levam ao teorema.

## 2. A expansão é feita diretamente no fundo físico

Introduza um parâmetro formal \(t\), distinto do tempo r, e escreva
\[
g_t=\bar g+t h,\qquad
\phi_t=\operatorname{Exp}_{\bar\phi}(t\xi),
\qquad \xi\in\Gamma(\bar\phi^*TS^3).
\tag{1}
\]
Exp é a exponencial da métrica alvo. Cada derivada em t em zero é tensorial e local. Em particular, \(\xi\) é uma seção global do fibrado pullback; não precisamos de uma única carta escalar contendo toda a imagem de \(\bar\phi\). O domínio perturbativo é uma vizinhança formal da seção zero, sem mudança do setor topológico do mapa.

Após a mesma escala dos campos ghost, auxiliares e anticampos, expanda a ação BV gauge fixada e retire sua constante de fundo. Com o fator de organização \(t^{-2}\),
\[
S_t^{\rm BV}=S_0^{\rm BV}+\sum_{n\ge3}t^{n-2}S_n^{\rm BV}.
\tag{2}
\]
O termo linear é zero porque o fundo resolve as equações completas. Cada \(S_n\) é um polinômio de grau finito nas flutuações e seus jatos, com coeficientes suaves construídos de \(\bar g,\bar\phi\), suas conexões e curvaturas. Os termos originais possuem no máximo duas derivadas. As séries de g⁻¹, volume e Exp produzem infinitos vértices, mas somente um número finito deles contribui a um coeficiente fixado de t e número de inserções.

A forma (2) é para a ação inicial. Contratermos de laços podem conter termos de grau zero, um ou dois nas flutuações; não são excluídos por essa escrita. Eles são organizados também pela sua ordem em ħ. Os termos constantes fatorizam e cancelam nas matrizes S relativas normalizadas. Um termo de ordem \(\hbar^L\) com n pernas, gerado pela ação inicial de duas derivadas, carrega o peso formal \(t^{n+2L-2}\); isso segue somando os pesos \(v-2\) dos vértices de um grafo conectado. Termos quadráticos de laço não são colocados silenciosamente no operador livre: podem ser tratados como inserções.

Não usamos a deformação \(h_\varepsilon\) em torno do sigma plano para construir (2). A existência de (2) não afirma a especialização das primitivas cohomológicas daquela outra série em \(\varepsilon=1\).

## 3. Os contratos de extensão são satisfeitos

[KNOWN] Usamos o teorema de extensão com grau de escala finito de [Brunetti–Fredenhagen, Teoremas 5.2–5.3 e §6.4](https://arxiv.org/pdf/math-ph/9903028). Ele fornece extensão às diagonais e caracteriza a liberdade por distribuições locais. A covariância da prescrição exige um passo adicional, realizado pela expansão local de escala de [Hollands–Wald, §§3–4](https://arxiv.org/pdf/gr-qc/0111108). Não se afirma que um corte arbitrário em coordenadas já seja covariante.

[KNOWN] A versão com tensores, sistemas de ondas e campos Grassmann é explicitada em [Hollands, §3.5, com Teorema 2 e axiomas T1–T11](https://arxiv.org/pdf/0705.3340). A Proposição 1 trata extensões Lorentz covariantes, inclusive tensorais. Importamos essa construção de produtos, sem importar a remoção de anomalias de Yang–Mills do §4 para o sigma gravitacional.

Aqui estão os pontos que tornam essa importação aplicável ao modelo presente:

1. **Sistema diferencial e fibrados.** D normaliza-se a um operador de onda com símbolo principal escalar no fibrado de posto 13; Q é de onda no fibrado de posto 4. As conexões e endomorfismos de ordem inferior são locais nos campos de fundo. A normalização pela forma de fibra invertível é mantida nos Green. Não se requer uma métrica positiva no espaço não físico para estender distribuições.
2. **Setor ímpar.** O dicionário verifica explicitamente antissimetria da Hessiana ghost e reciprocidade graduada. Há um par c/barc de quatro componentes, não oito determinantes independentes. Os sinais apenas acompanham as contrações finitas dos grafos.
3. **Auxiliar.** O gauge escolhido é linear em h. Portanto b não participa dos vértices internos de interação sem anticampos. Suas inserções são recuperadas pelas derivadas dos kernels de onda e pelos contatos já fixados. Não aparece uma nova família indefinida de produtos de propagadores ultralocais em laços de b.
4. **Anticampos.** São fontes externas, sem propagador. Sua dependência polinomial e seus jatos entram como coeficientes nas distribuições a estender. Não se tenta inverter uma Hessiana degenerada acrescentando propagadores de anticampos.
5. **Escala e localização.** Cada coeficiente de um vértice em (2) tem ordem diferencial finita; cada contração tem grau de escala finito. Os testes têm suporte compacto, e o fundo é globalmente hiperbólico. Portanto não há um problema infravermelho escondido na extensão às diagonais.
6. **Naturalidade.** Os coeficientes transformam como tensores do fibrado natural de fundo e do pullback alvo. Hadamard e sua expansão de escala usam transporte paralelo e jatos desses coeficientes. Mudanças de cartas de S³ são mudanças de apresentação desse mesmo fibrado; não exigem soma sobre outros setores de mapas. O potencial/endomorfismo adicional de um sistema de ondas aparece nos coeficientes de transporte e nos contratermos, sem alterar a extensão dos kernels universais de escala.

Em particular, a construção é local e covariante em relação a embeddings que transportam **todos** os dados de fundo. Essa é uma condição de naturalidade dos produtos. Ela não é a independência quântica da cisão fundo–perturbação, que compara escolhas diferentes por outra conexão e exige identidades adicionais.

## 4. Recorrência concreta para os produtos

Escolha primeiro os produtos de Wick locais com a matriz parametrix de Hadamard dos operadores acima. O estado 067/068 serve para representá-los; não define os coeficientes de renormalização mediante sua decomposição global em modos. Duas realizações Hadamard diferem por um kernel suave e são relacionadas pela exponencial de contrações suaves, coeficiente a coeficiente.

Suponha \(T_k\) construído para \(k<n\). Fora da diagonal total de \(M^n\), a fatorização causal dá, nos abertos em que um subconjunto de pontos é posterior aos demais,
\[
T_n(F_1,\ldots,F_n)=T_{|I|}(F_I)\star T_{|I^c|}(F_{I^c}).
\tag{3}
\]
Os produtos coincidem nas sobreposições pela associatividade e causalidade das ordens inferiores. Uma configuração não totalmente coincidente em um espaço globalmente hiperbólico admite essa separação local; as diagonais parciais já estão tratadas pela hipótese de indução. Isso define \(T_n^0\) fora da diagonal total.

Expanda \(T_n^0\) em monômios de Wick e coeficientes numéricos com índices tensorais. Para cada termo, use coordenadas normais relativas \(y\in\mathbb R^{4(n-1)}\), mantendo um ponto x na diagonal. Se o grau transversal for \(\sigma\), a extensão é única quando \(\sigma<4(n-1)\). Caso contrário, a liberdade tem a forma
\[
\sum_{|\alpha|\le\lfloor\sigma-4(n-1)\rfloor}
C_\alpha(x)\nabla_y^\alpha\delta(y).
\tag{4}
\]
Os coeficientes C são tensores locais dos dados de fundo e dos campos/anticampos remanescentes.

Para manter a naturalidade, expanda o kernel próximo da diagonal em um número finito de jatos covariantes multiplicando distribuições universais quase homogêneas em y, mais um resto cujo grau é menor que a codimensão. Estenda o resto unicamente; estenda os termos universais pela prescrição Lorentz covariante tensorial. Essa operação também permite a graduação, realidade, escala e a identidade da ação por partes do contrato T1–T11. Termos de curvatura e da conexão alvo participam dos jatos, sem alterar a lógica da extensão. A indução define todos os \(T_n\), com liberdade exatamente local da classe escolhida.

A identidade da ação por partes significa que \(\int f\,dO\) e \(-\int df\wedge O\) dão o mesmo funcional inserido. Ela não deve ser confundida com o enunciado falso de que aplicações das equações de campo a um produto temporal nunca produzem contatos. Esses contatos já aparecem em \(P_{\rm gr}G_{\rm gr}^F=1\).

## 5. Finitude perturbativa, ação efetiva e campos interagentes

Para um grafo conectado com I linhas internas, V vértices, L laços e ordens diferenciais d_v, a contagem de momento dos propagadores de onda dá
\[
\delta=4L-2I+\sum_vd_v
=2+2L+\sum_v(d_v-2).
\tag{5}
\]
Ela é um limite para os termos locais necessários, não uma prova de que cada coeficiente permitido seja não nulo. Derivadas nas pernas externas e fatores de curvatura distribuem essa ordem em invariantes covariantes. O papel de (5) é garantir um problema finito a cada ordem/truncagem especificada, permitindo novos operadores quando exigidos. Os contratermos de quatro derivadas de 068 são compatíveis com esse contrato. Não se impõe fechamento em apenas \(\kappa,c,\Lambda\).

Para uma interação compacta \(V\) construída de (2), defina formalmente
\[
\mathcal S(V)=\sum_{n\ge0}\frac1{n!}\left(\frac i\hbar\right)^nT_n(V^{\otimes n}),
\qquad
\mathcal S_V(F)=\mathcal S(V)^{-1}_{\star}\star\mathcal S(V+F),
\]
\[
R_V(F)=\left.\frac\hbar i\frac{d}{ds}\mathcal S_V(sF)\right|_{s=0}.
\tag{6}
\]
O fator ħ/i faz \(R_0(F)=T_1(F)\). As potências negativas aparentes de ħ organizam a exponencial S; os campos conectados/relativos têm a contagem formal apropriada pela relação \(I-V+1=L\). Não se avalia uma série numérica em ħ para obter esse resultado.

A fatorização (3) garante causalidade dos campos (6). Para uma região relativamente compacta O, escolhas de cutoff que coincidam numa vizinhança causal pertinente definem álgebras locais isomorfas, por matrizes S relativas. O procedimento forma o limite adiabático **algébrico**. A aplicação do mesmo mecanismo a flutuações gravitacionais, com seus limites efetivos, está descrita em [Brunetti–Fredenhagen–Rejzner, §3.4, equações (52)–(59)](https://arxiv.org/html/1306.1058v4). Aqui os vértices e o sistema livre incluem o sigma, conforme as verificações acima. Isso não é um limite adiabático de estados nem uma matriz de espalhamento global já existente.

## 6. A anomalia existe como objeto local computável

A ação quadrática BV do dicionário é nilpotente e seu diferencial \(\widehat s_0\) é uma derivação graduada da álgebra livre. Isso fornece o dado exigido pelo teorema geral de Ward anômala de [Fröb, Teoremas 3, 6 e 7, equações (154)–(156)](https://arxiv.org/pdf/1803.10235). O resultado se aplica a campos e anticampos fora das equações; não pressupõe a nulidade da anomalia.

Em nossas convenções, existe um mapa local \(\mathcal A(e_\otimes^V)=O(\hbar)\), de número fantasma um, tal que a falha de \(\widehat s_0\) com o exponencial temporal é expressa por inserção de
\[
\frac12(S_0^{\rm BV}+V,S_0^{\rm BV}+V)+\mathcal A(e_\otimes^V).
\tag{7}
\]
A expressão com S_0 é abreviação local de \(s_0V+\frac12(V,V)\); não exige integrar a ação livre global sem cutoff. Para V vindo da ação clássica completa, o termo clássico se anula onde o cutoff é constante. A quebra remanescente é justamente o objeto de renormalização a calcular.

A razão de sua **localidade** é também verificável na recorrência: se todas as ordens inferiores satisfazem a identidade anômala, a diferença na ordem n se cancela em cada aberto causal de (3), pela regra de derivação. Logo só pode ter suporte na diagonal total. O teorema de estrutura de distribuições suportadas na diagonal dá uma expressão do tipo (4), agora com graduação um. O limite clássico dos termos de árvore reproduz o antibracket; o resto começa em ħ. Essa localização não é a afirmação de que o coeficiente vale zero.

Aplicar novamente \(\widehat s_0\), usar sua nilpotência e a Jacobi graduada fornece a identidade de consistência. Escrevendo a primeira quebra não removida como \(\hbar^N a_N\), as inserções de anomalias nas anomalias começam em ordem superior. Consequentemente,
\[
sa_N+db_N=0,
\tag{8}
\]
no mesmo espaço de densidades locais admitido pela prescrição. Isso verifica o passo de consistência usado pela recorrência 068. Para remover \(a_N\), ainda é necessário provar \(a_N=sB_N+dD_N\) com B_N real, covariante e admissível. Essa é Q3/cohomologia; não foi deduzida da existência de \(T_n\).

## 7. Resultado de Q2 e próximas dependências

[DERIVED + KNOWN] Q2 passa de pedido genérico a construção formal efetiva: existe a família de produtos renormalizados do sistema acoplado, a álgebra interagente **auxiliar**, o mapa de quebra local e sua condição de consistência, sob o contrato EFT explicitado. As escolhas finitas de renormalização ainda parametrizam uma família; não foram fixadas por normalização probabilística.

[OPEN] A remoção da quebra e o quociente físico interagente exigem a cohomologia no espaço correto, incluindo as condições de realidade/covariância. Também permanecem distintos: independência entre fundos, anomalias globais, estado físico interagente, estabilidade, rota UV e convergência. Os campos probabilísticos P só recebem o que o transporte de observáveis definido permite; uma quantização independente de sua redundância não é provada aqui.

Não houve nova prova Lean, execução/importação de um.py, alteração de originais ou teste de natureza. Os teoremas de extensão e Ward são importações da literatura primária com hipóteses verificadas; as traduções de campo, expansão no fundo e aplicação ao Einstein–sigma são as demonstrações desta nota.
