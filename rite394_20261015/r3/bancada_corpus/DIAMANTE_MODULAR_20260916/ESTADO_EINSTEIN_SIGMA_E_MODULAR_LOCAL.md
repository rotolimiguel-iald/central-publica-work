# Do estado Einstein–sigma já construído ao operador modular local

16/09/2026. **[DERIVED — demonstração escrita; não é nova compilação Lean nem resultado experimental.]** Esta nota usa a ação e o estado linear das entregas 066–067, a álgebra perturbativa 069 e o projetor local 088. Não introduz outra ação, outro estado ou outro motor de dephasing. A construção perturbativa interagente não é promovida a estado positivo interagente.

## 1. Correção de endereço e alcance

A construção física já estava em `Chatgpt`. A pergunta anterior por ação e estado tinha uma resposta parcial concreta que precisava ser recuperada:

| Fonte | Dado utilizado | Alcance |
|---|---|---|
| [066: Jacobi e álgebra](../QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md) | Ação, Hessiana, gauge, propagador causal | Einstein–sigma ambiente, linearizado |
| [067: estado positivo](../HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912/ESTADO_FISICO_HADAMARD_E_CONTRATOS.md) | Modos S/V/TT, covariância de Gram, CCR físicas | Estado quase livre explícito no fundo escolhido |
| [S/V: reconstrução](../REDUCAO_ESCALAR_VETOR_SIGMA_20260909_212531/REDUCAO_ADM_MODOS_FISICOS.md) | Restrições, coeficientes, mapas de teste | Modos físicos ℓ≥2 |
| [TT: reconstrução](../MODOS_TENSORIAIS_EXATOS_20260909/ACAO_TT_E_MODOS_EXATOS.md) | Normalização tensorial | Mesmo fundo e mesma ação |
| [069: interação causal](../CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md) | Álgebra interagente auxiliar formal | Não fornece estado físico interagente nem completude UV |
| [088: relógios e projetor](../RELOGIOS_RELACIONAIS_FUNDO_FISICO_088_20260910/RELOGIOS_X_SIGMA_E_RETRACAO_DE_JATOS.md) | Extrator local F, FK=Id, P=Id−KF | Diferencial local no interior do fundo físico |

A conclusão anterior sobre `WedgeNet` continua correta **para aquela rede**: seu diamante limitado recebe `scalarAlg`. A rede física induzida pelos testes de 066–067 é outra construção. Não existe aqui uma identificação provada entre as duas redes. Tampouco se reabre a dualidade `PRODUCT_TOWER` aceita no v358.

Adotamos explicitamente a convenção [067 de sinais](../CONVENCAO_ACAO_ESTADO_LOCAL_20260909_214710_215498/CONVENCAO_SINAL_E_TRANSPORTE.md):

\[
S=-\frac1{2\kappa}\int(R-2\Lambda)\,d\mu_g
 +\frac c2\int g^{\mu\nu}\gamma(d_\mu\phi,d_\nu\phi)\,d\mu_g,
\quad c>0,\quad \kappa c=4,\quad\Lambda=3/4.
\]

O fundo é \(g=dr^2-a^2\gamma\), \(a=2\cos(r/2)\), \(\bar\phi=z\), em um intervalo aberto interior a \((0,\pi)\), vezes \(S^3\). Em tempo conforme, \(a=2\operatorname{sech}\eta\), com \(\eta>0\). A ação ambiente e a extensão global à esfera são entradas declaradas pelas fontes. Não passam a ser consequências de \(\omega(I)=1\) por esta nota.

## 2. Localidade antes da decomposição em modos

Para evitar a confusão entre o gerador modular e o gauge, escrevemos \(K_{\rm g}\) para o operador de difeomorfismos de 066/088. A 088 fornece um operador diferencial local real \(F\), com coeficientes analíticos no interior, tal que

\[
F K_{\rm g}=1,\qquad P=1-K_{\rm g}F,\qquad
P^2=P,\quad P K_{\rm g}=0.
\]

Se \(u=(h,\xi)\), então \(Pu=(H,0)\), onde
\(H=h-\mathcal L_{Fu}\bar g\) é um tensor de traço espacial zero. Este H é um **campo local linear invariante de gauge**, e não um projetor espectral ou hamiltoniano. Seus coeficientes usam \(a,H_{\rm Hub}\) e suas inversas, regulares e analíticas em compactos interiores. A singularidade em \(r=0\) não está no domínio.

Se q é um teste tensorial compacto, a leitura \(\langle q,H\rangle\) corresponde ao teste físico \(P^*(q,0)\). Seu suporte está contido no de q e
\(K_{\rm g}^*P^*(q,0)=0\). Reciprocamente, para qualquer teste físico f,

\[
K_{\rm g}^*f=0\ \Longrightarrow\ P^*f=f.
\]

Como a componente de matéria de Pu é zero, \(P^*f=P^*(f_h,0)\). Logo os testes de H geram **a mesma álgebra local induzida** que os testes físicos de 067; não a enlarguecem por permitir testes arbitrários antes da projeção. Relações de equação e o radical da representação continuam quocientados.

Esta passagem é útil: permite trabalhar com um campo em fibrado analítico e testes locais arbitrários, sem declarar os potenciais SVT, individualmente, observáveis locais. A comutatividade em separação espacial vem do propagador causal de 066 e da identidade (6.2) de 067.

## 3. O espaço de uma partícula vem da covariância existente

Para teste físico real f, definimos o vetor

\[
(k f)_{A,n}=\sqrt\hbar\int \overline{f_{p_{A,n}}(\eta)}\,
 j_{A,n}[f](\eta)\,d\eta,
\qquad
f_p(\eta)=\frac{(p-i\tanh\eta)e^{-ip\eta}}{\sqrt{2p(p^2+1)}}.
\]

Os j são **exatamente** (5.2)–(5.4) de 067, não novos pesos ajustáveis. Ponha
\(\mathcal H_1=\overline{\operatorname{span}_{\mathbb C}k\mathcal V_{\rm obs}}\)
no espaço das sequências dos modos. A igualdade de Gram de 067 dá

\[
\langle kf,kg\rangle=\Lambda(f,g),\qquad
2\operatorname{Im}\langle kf,kg\rangle=\hbar\,\sigma(f,g).
\]

Para cada aberto O, seja

\[
L(O)=\overline{\{kP^*(q,0):q\text{ real},\ \operatorname{supp}q\subset O\}}^{\ \mathbb R}.
\]

Usamos o fecho real **no mesmo** \(\mathcal H_1\); não substituímos L(O) pelo subespaço de todos os modos com ℓ abaixo de um corte. A álgebra é a de Weyl em Fock bosônico sobre \(\mathcal H_1\),
\(\mathcal A_{\rm lin}(O)=\{W(v):v\in L(O)\}''\), com a normalização de Weyl escolhida para a CCR acima. A restrição do vácuo de Fock reproduz a covariância 067. Aqui “vácuo de Fock” nomeia essa representação; não prova seleção única da natureza.

## 4. Analiticidade suficiente: a estimativa que falta a um argumento apenas Hadamard

**Lema, neste fundo e para estes modos.** O campo de uma partícula associado a H é valor de fronteira de uma função holomorfa em um tubo local com cone imaginário aberto e apontado. Em consequência, sua frente de onda analítica está, em cada carta, contida num cone que não encontra seu negativo.

**Objeto da estimativa.** Se \(u^+_{A,n}=R_A(f_{p_{A,n}}e_{A,n})\), escreva \(h^+_{A,n}=[P u^+_{A,n}]_h\). Em uma trivialização real analítica, o vetor-kernel é \(\Psi_H(x)=(\sqrt\hbar\,\overline{h^+_{A,n}(x)})_{A,n}\), com a contração tensorial e a medida da fonte 067. Assim \(kP^*(q,0)=\int\langle q(x),\Psi_H(x)\rangle\,d\mu_g(x)\). Sua continuação usa \(P R_A(g_p e_{A,n})\), onde todos os coeficientes de fundo são continuados analiticamente; (A) é a estimativa da norma desse vetor, componente tensorial por componente.

**Prova.** Escolha um compacto temporal interior, uma carta analítica de \(S^3\) e uma trivialização analítica dos tensores. Para os vetores-ket usa-se a continuação de \(\bar f_p\):

\[
g_p(z)=\frac{(p+i\tanh z)e^{ipz}}{\sqrt{2p(p^2+1)}},
\qquad z=\eta+i s,\quad s>0.
\]

Em um pequeno tubo que evite os polos de tanh e as singularidades das inversas de fundo, suas derivadas de ordem fixada são limitadas por
\(C_m(1+p)^{m+N}e^{-ps}\). A derivação temporal e a reconstrução S/V/TT acrescentam apenas potências de p e coeficientes analíticos uniformemente limitados nesse tubo.

As frequências são
\(p_A^2=(\ell+1)^2+b_A\), com \(b_A=2,3,6\), \(\ell\ge2\).
Em particular, \(p_A\ge\ell+1\). Os harmônicos da esfera são finitas representações de SO(4), com pesos de ordem ℓ; vetores e tensores acrescentam posto fixo. Ao continuar uma rotação local para parâmetros complexos, a norma da representação é limitada por \(e^{C(\ell+1)|y|}\). A avaliação de um harmônico normalizado, sua multiplicidade e derivadas de ordem fixada crescem polinomialmente em ℓ. Alternativamente, obtém-se a mesma estimativa pela realização em polinômios harmônicos homogêneos e suas versões tensoriais. Assim, nas cartas escolhidas,

\[
\sum_m |D^j e_{A,\ell m}(x+i y)|^2
\le C_j(1+\ell)^{N_j}e^{2C(\ell+1)|y|}.
\]

Os denominadores \(\lambda+3,D+8,K_S,K_V\) da reconstrução não zeram para ℓ≥2. A reconstrução sobre cada harmônico tem crescimento polinomial; a projeção diferencial local P mantém essa propriedade. Portanto a norma quadrada da série de uma partícula, com todas as suas derivadas de ordem fixada, é majorada por

\[
C\sum_{\ell\ge2}(1+\ell)^N
 e^{-2(\ell+1)(s-C|y|)}.
\tag{A}
\]

Em todo subtubo \(s>C|y|\), s suficientemente pequeno, (A) converge normalmente. Ao aproximar a fronteira com \(\delta=s-C|y|>0\), a soma é limitada por \(C'\delta^{-(N+1)}\). Logo há valor de fronteira distribucional, igual à série real de 067, e controle de crescimento polinomial. Não usamos “suave implica analítico”: são as frequências positivas, os coeficientes analíticos e esta estimativa que dão o acréscimo.

O [Corolário 2.9 de Strohmaier–Verch–Wollenberg](https://arxiv.org/pdf/math-ph/0202003), para distribuições com valores em Hilbert e o tubo acima, coloca a frente de onda analítica no cone dual do tubo. Na convenção de Fourier correspondente ao ket \(e^{ip\eta}\), ele obedece a \(\tau\ge C^{-1}|\zeta|\); trocar a convenção troca o cone inteiro. Nenhum covetor não nulo e seu negativo podem pertencer simultaneamente a esse cone. Não é necessário identificar aqui a frente de onda analítica exata nem provar que ela satura o cone nulo. ∎

A estimativa exponencial dos harmônicos é explicitada na prova para não confundir o cálculo pseudodiferencial **suave** da 067 com um resultado analítico automático. A fonte primária [Lindblom–Taylor–Zhang](https://arxiv.org/html/1709.08020v1) fixa os setores e autovalores. O uso de continuação complexa acima é argumento desta nota.

## 5. Densidade local e separação, sem supor um vácuo estacionário

**Proposição.** Para todo aberto não vazio O do fundo conectado,
\(\overline{L(O)+iL(O)}=\mathcal H_1\).

**Prova.** Se v é ortogonal à imagem complexa dos testes em O, a distribuição tensorial
\(u_v(q)=\langle v,kP^*(q,0)\rangle\) se anula em O. Pelo lema, sua frente de onda analítica não encontra seu negativo. A continuação única analítica de [Strohmaier–Verch–Wollenberg, Proposição 5.3 e Observação 5.7](https://arxiv.org/pdf/math-ph/0202003) implica que ela se anula no fundo inteiro. Para fibrados, aplica-se o argumento em trivializações analíticas e propaga-se por cartas sobrepostas. Pela definição de \(\mathcal H_1\), v=0. ∎

**Proposição.** Se D tem complemento causal contendo um aberto O não vazio, então \(L(D)\cap iL(D)=\{0\}\).

**Prova.** A localidade já estabelecida dá \(\operatorname{Im}\langle x,y\rangle=0\) para x∈L(D), y∈L(O). Se x e ix pertencem a L(D), a mesma igualdade para ix anula também a parte real. Assim x é ortogonal a L(O)+iL(O), denso pela proposição anterior, e x=0. ∎

Portanto L(D) é **subespaço real standard** para diamantes interiores com complemento causal aberto. A conclusão utiliza a reconstrução física 067, o projetor local 088 e a estimativa analítica desta nota. Não decorre apenas da palavra Hadamard e não vale, por esta demonstração, para um estado interagente formal arbitrário.

## 6. O operador modular regional está definido pelo mesmo estado

Defina, com domínio denso \(L(D)+iL(D)\),

\[
s_D(x+i y)=x-i y,\qquad x,y\in L(D).
\]

É bem definido pela interseção nula, fechado porque L(D) é fechado, e sua decomposição polar fornece \(s_D=j_D\delta_D^{1/2}\), com \(\delta_D=s_D^*s_D\) positivo e sem núcleo. A segunda quantização dá

\[
\boxed{J_D=\Gamma(j_D),\qquad \Delta_D=\Gamma(\delta_D),
\qquad K_{\omega,D}=-\log\Delta_D=d\Gamma(-\log\delta_D).}
\tag{B}
\]

São os objetos modulares de \((\mathcal A_{\rm lin}(D),\Omega)\). O contrato de segunda quantização é o de [Conti–Morsella, §2](https://arxiv.org/pdf/2305.07606). A fórmula (B) é construção operatorial a partir da covariância e do suporte local. **Não é uma diagonalização explícita de \(\delta_D\), nem uma matriz densidade regional ordinária, nem uma prova de tipo III₁.**

Não se usa \(-\log\rho_D\) de uma truncagem como definição do operador contínuo. Também não se identifica o tempo conforme η com o parâmetro modular t.

## 7. Teste exato da ponte geométrica

Se uma transformação geométrica proposta age nos testes por \(T_t\), ela precisa primeiro descer ao quociente físico, preservar suporte em D, a forma simplética e a referência de estado. Preservar apenas a forma simplética fornece, quando bem definido, um automorfismo CCR; preservar a covariância permite sua realização unitária em uma partícula.

O teste necessário e suficiente para coincidir com o fluxo modular **nessa realização quase livre**, com o sinal/normalização escolhidos, é

\[
\boxed{kT_t f=\delta_D^{it}kf\quad
\text{para todo teste físico local }f.}
\tag{C}
\]

De fato os dois fluxos agem nos geradores de Weyl por seus mapas em uma partícula; a representação de Weyl distingue os vetores, e os geradores geram a álgebra. A igualdade em todos eles dá a igualdade normal dos automorfismos. A direção inversa é a mesma leitura nos geradores. Para um gerador geométrico autoadjunto definido independentemente, a versão infinitesimal exige os domínios comuns e a integração da ação; a igualdade formal de um comutador em poucos testes não substitui (C).

A invariância de duas pontas
\(\Lambda(T_t f,T_t g)=\Lambda(f,g)\) é necessária, mas insuficiente: muitas simetrias preservam um estado sem ser seu fluxo modular. Uma comparação somente de índices também não fixa (C).

## 8. O que a identificação com dephasing já resolve — e o que não resolve

O [handoff V2](HANDOFF_TECNICO_V2.md) já foi recebido no v358. Sua ponte de dephasing parcial e a prova do centralizador não devem ser reimplementadas aqui. Neste novo endereço regional, (B) fornece o fluxo a partir do qual se formula a esperança sobre o centralizador da referência. Sobre o centralizador, a ação modular é estacionária por definição.

Há duas precauções de tipo:

1. O centralizador da álgebra de Fock não é simplesmente o espaço de uma partícula com \(\delta_D=1\). Produtos podem ter pesos modulares que se compensam. A análise deve continuar na álgebra preservada correta.
2. Na convenção \(K=-\log\Delta\), o resto não limitado requer domínio ou formulação pelas derivações. Mesmo para operadores limitados, comutar com a subálgebra não prova pertencer ao seu centro sem a condição de pertença. Essas diferenças já foram demonstradas em [CentralizerRemainderPerturbation.lean](CentralizerRemainderPerturbation.lean).

Ainda não calculamos nesta nota (C) para \(K_\xi=2\pi\int\xi\cdot T\). Também não calculamos o primeiro coeficiente **não central** de R neste modelo. A covariância existente agora dá um endereço efetivo para esse cálculo, em lugar de substituir o diamante por um fator abstrato com o mesmo nome.

## 9. Fronteira atual do resultado

**[DERIVED nesta nota]** Continuação local dos modos, densidade local, separação e construção modular de uma partícula/Fock para a rede linear física recuperada. **[KNOWN]** Continuação única analítica e segunda quantização modular, nas referências primárias indicadas. **[INPUT]** Ação ambiente, extensão a S³ e estado 067. **[OPEN]** Expressão geométrica do fluxo no diamante, primeiro coeficiente não central de R, estado interagente físico e completude UV.

A 069 já constrói produtos temporais e a álgebra auxiliar perturbativa; isso não deve voltar a aparecer como trabalho inexistente. A passagem de uma série formal a uma representação positiva física com estado normal fiel continua distinta. Tampouco se conclui que todos os modelos interagentes e diamantes tenham um coeficiente universal.

Não houve alteração do `um.py`, do kernel canônico, de seu gate ou dos originais da tarefa irmã. Esta prova escrita recebeu revisão adversarial independente favorável dos §§2–6, registrada em REVISAO_INDEPENDENTE_ESTADO_LOCAL.md; as duas explicitações menores solicitadas foram incorporadas. O parecer não revisa uma conclusão interagente/UV e não equivale a verificação em Lean. Controles numéricos de modos não substituem a análise funcional acima.
