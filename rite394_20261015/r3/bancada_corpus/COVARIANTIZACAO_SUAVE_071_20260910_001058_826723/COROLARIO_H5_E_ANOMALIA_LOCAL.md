# Corolário: grau BRST cinco e alcance da cohomologia local de anomalias

10/09/2026, arco 071. [DERIVED — consequência escrita]. A nota COVARIANTIZACAO_E_H2_GLOBAL.md permanece intacta. Este corolário explicita o consumo do resultado H²_char,cov=0 pela redução de grau da entrega 070. Distingue três álgebras: os tensores covariantes \(\mathcal B\), a álgebra local completa com dependência suave no vielbein \(\mathcal A_{\rm sm}\), e um eventual espaço mais estreito de contratermos. Não houve Lean ou cálculo numérico.

## 1. H⁵(s,B)=0 na álgebra covariante com coeficientes suaves globais no S³

\(\mathcal B\) é a álgebra da nota principal: tensores covariantes, antifields covariantes, quatro ghosts de translação ξ e seis de Lorentz C. Os coeficientes são C∞ globais no S³ e os jatos diferenciados/antifields são polinomiais finitos. A dependência métrica volta à classe racional tensorial em g,g⁻¹ e volume.

Filtre o diferencial por grau em ξ:

\[
s=s_0+s_1+s_2,\qquad s_0=\delta+\gamma_L,\qquad
\deg_\xi(s_j)=j.
\]

A resolução KT global continua acíclica nos antifields positivos: δ não age nos valores y, portanto as primitivas KT locais podem ser coladas por uma partição de unidade sem termos δρ. Depois de KT, a cohomologia de \(\gamma_L\) é a cohomologia de Chevalley–Eilenberg de so(1,3) nos módulos tensoriais finitos. Suavidade em y não altera esse cálculo algébrico nos índices Lorentz.

[KNOWN] Para a álgebra real so(1,3), a complexificação é sl₂(C)⊕sl₂(C). Seu CE com coeficientes triviais é uma álgebra exterior sobre duas classes de grau 3. Os graus possíveis são 0,3,6. A redução correspondente usada aqui já foi explicitada na [nota topológica070](../TOPOLOGIA_BRST_SIGMA_070_20260909_233042_647697/TOPOLOGIA_ALVO_E_REDUCAO_H1.md); o mecanismo de decomposição está em [BBH1995, §7 e apêndices B–C](https://arxiv.org/pdf/hep-th/9505173v2).

**[DERIVED] Seleção de grau.** Em ghost total 5, o primeiro termo não nulo da sequência espectral só pode ter

\[
(\deg_\xi,\deg_{\rm CE})=(2,3).
\tag{1.1}
\]

O par (5,0) é impossível porque há somente quatro ξ. O par (−1,6) é impossível após a eliminação KT, que deixa representantes sem antifields.

Assim um candidato inicial tem a forma \(\sum_{\alpha=1}^2\theta_\alpha^{(3)}\,b_{\alpha,2}(\xi,T)\). O diferencial seguinte é a derivação covariante fraca de b₂. A condição de ciclo exige que b₂ represente uma classe de H²_char,cov. A nota principal prova que essa classe é zero, **na classe suave global do alvo e racional natural da métrica**. Logo o termo (1.1) é eliminado por uma primitiva na mesma classe. Não restam outros pares de grau total 5:

\[
\boxed{H^5(s,\mathcal B)=0.}
\tag{1.2}
\]

A convergência aqui é finita: o grau ξ varia de 0 a 4; em ghost 5, antigh≤5 na álgebra \(\mathcal B\). Em cada levantamento há somente operações de ordem finita. Não se avalia um parâmetro de perturbação em 1 e não se expande y em série.

O volume do alvo permanece no grau total 3. Para entrar neste canal de grau 5 teria de se combinar com uma classe CE de grau 2, inexistente. Essa observação não substitui a prova de H²_char,cov; (1.2) a usa explicitamente.

## 2. A álgebra completa padrão, suave no vielbein

Agora amplie a apresentação local para a classe padrão

\[
\mathcal A_{\rm sm}=
 C^\infty(GL^+(4,\mathbb R)\times S^3)
 [\text{jatos diferenciados, ghosts e antifields}],
\]

com dependência de ordem finita e polinomial nos jatos diferenciados. Os coeficientes podem ser funções suaves conjuntas de e e y; não se exige uma soma finita de produtos separados dessas variáveis. A definição é intrínseca pelos feixes de jatos. Os campos completos são e,φ e seus ghosts/antifields. Não se acrescentam uma métrica de fundo fixa ou outros campos espectadores.

A separação por (U,V;\(\mathcal B\)) identifica a parte U,V ao complexo de de Rham do espaço de vielbeins, mais pares contráteis dos jatos de ordem positiva. A contração desses pares é finita sobre os polinômios. Para a parte de valores e, a dependência **suave** permite usar a cohomologia de de Rham usual.

[DERIVED/KNOWN] GL⁺(4,R) retrai-se por decomposição polar em SO(4). Com coeficientes reais, SO(4) tem cohomologia exterior em duas classes de grau 3 (a cobertura finita Spin(4)=S³×S³ dá o mesmo resultado real). Portanto

\[
H^p_{\rm dR}(GL^+(4,\mathbb R))\ne0
 \quad\text{somente em }p=0,3,6.
\tag{2.1}
\]

A decomposição é a de [BBH1995, §§4–5](https://arxiv.org/pdf/hep-th/9505173v2). Sua aplicação abaixo mantém C∞ genuíno em e e y; não troca cohomologia de de Rham por cohomologia de um anel racional.

**Precisão paramétrica.** Para funções suaves conjuntas de e,y, não se presume um produto tensorial algébrico de espaços C∞. A retração polar e uma contração de de Rham em SO(4), por sua decomposição de Hodge, atuam somente nas variáveis U,V. Seus operadores são independentes de y e dos tensores de \(\mathcal B\), portanto comutam com o diferencial desse fator e preservam dependência suave paramétrica em y. A projeção harmônica tem imagem finita, nos graus (2.1). Aplicada a um coeficiente de um polinômio finito de jatos, continua produzindo um coeficiente suave, sem acrescentar jatos ou um inverso diferencial no espaço-tempo. Isso justifica a decomposição de cohomologia também para a classe C∞ conjunta declarada.

No grau total 5, a decomposição de cohomologia só permite

\[
H^5(s,\mathcal A_{\rm sm})\cong
 H^0_{\rm dR}(GL^+_4)\otimes H^5(s,\mathcal B)
 \oplus H^3_{\rm dR}(GL^+_4)\otimes H^2(s,\mathcal B)
 \oplus H^6_{\rm dR}(GL^+_4)\otimes H^{-1}(s,\mathcal B).
\tag{2.2}
\]

A primeira parcela é zero por (1.2). As outras duas são zero pela nota principal, §§3–5. Logo

\[
\boxed{H^5(s,\mathcal A_{\rm sm})=0.}
\tag{2.3}
\]

Não se apagou A₁ “por ser gauge”: sua topologia foi conservada em (2.1) e cruzada explicitamente com os graus do outro fator. Não se multiplicou uma segunda vez a cohomologia de S³, pois ela já foi incluída na análise global de \(\mathcal B\).

## 3. O que a comparação com H¹,⁴(s|d) fornece

Considere a cohomologia **local coordenada** de formas, em uma carta contrátil do espaço-tempo, com a álgebra \(\mathcal A_{\rm sm}\). As primitivas são permitidas nessa mesma álgebra local completa; não se exige de saída que sejam Lorentz-básicas ou densidades estritamente invariantes sob o gauge quântico.

[KNOWN] A comparação gravitacional [BBH1995, §6, equação (6.15)](https://arxiv.org/pdf/hep-th/9505173v2) relaciona o grau de forma máximo ao grau BRST total, dividindo as constantes no grau em que são pertinentes. Em (g,n)=(1,4), não há constante a subtrair:

\[
H^{1,4}(s\mid d_H;\mathcal A_{\rm sm})
 \cong H^5(s,\mathcal A_{\rm sm}).
\tag{3.1}
\]

Os coeficientes explícitos em x e os termos dω de sua descida são mantidos até a comparação, como descrito na nota principal §3. A ausência de obstruções topológicas em uma carta de espaço-tempo é usada nesse passo. Não se está afirmando uma cohomologia global de formas em todo espaço-tempo arbitrário.

**[DERIVED] Consequência na classe declarada:**

\[
\boxed{H^{1,4}(s\mid d_H;\mathcal A_{\rm sm})=0.}
\tag{3.2}
\]

Ou seja, todo cociclo local de anomalia \(a_4^1\) nessa classe possui \(b_4^0,b_3^1\) na mesma classe tais que

\[
a_4^1=s b_4^0+d_H b_3^1.
\tag{3.3}
\]

A globalidade suave em **valores do alvo S³** está incluída. As equações e os campos são os completos Einstein–sigma; não se congelou uma metade do sistema para calcular s. A topologia do alvo não foi removida por uma expansão em uma carta.

## 4. Por que o qualificador suave no vielbein é necessário

A passagem (2.1) não pode ser feita sem comentário no anel estritamente racional em e,det(e)⁻¹. Um controle elementar é

\[
d\log\det e={d(\det e)\over\det e}.
\tag{4.1}
\]

A 1-forma pertence ao anel racional localizado, mas sua primitiva log(det e) é suave em GL⁺ e não é racional. Restrinja à curva e=diag(t,1,1,1), t>0: a forma vira dt/t. Ela não possui primitiva racional, pois a derivada de uma função racional não tem resíduo simples não nulo em t=0. Portanto a álgebra restrita não herda automaticamente o cálculo de de Rham suave (2.1).

Isso não altera (1.1) da nota principal nem (1.2) deste corolário: ambos são enunciados na álgebra **covariante** \(\mathcal B\), para a qual a primitiva foi construída e devolvida à classe racional tensorial. Mas impede promover (3.2) a um teorema de existência de primitivas racionais em toda a apresentação de vielbein sem outro argumento.

Também é diferente exigir que todo contratermo seja uma densidade antifield-free estritamente natural somente de g e φ. Uma densidade desse tipo transforma por derivada de Lie, logo seu funcional é s-fechado módulo d_H; ela não cancela por si um cociclo não nulo apenas por se chamar “contratermo”. A classe de primitivas deve ser fixada antes de importar (3.3).

## 5. Efeito sobre a lista de obrigações

- [DERIVED] H²_char,cov=0 foi obtido na classe natural racional métrica, C∞ global no alvo, consumindo a exatidão ordinária suave071 e KT069.
- [DERIVED] O canal global H⁵(s,\(\mathcal B\)) da redução070 é zero na mesma classe covariante.
- [DERIVED] H¹,⁴(s|d_H)=0 segue na classe local completa padrão, **suave no vielbein**, com as primitivas autorizadas por essa classe.
- [OPEN — comparação de espaços] O espaço admissível Q2 pode incluir fundos externos fixos, restrições de covariância, suporte, dependência analítica ou outros requisitos. É necessário provar que sua anomalia e uma primitiva pertencem ao espaço correto e que a comparação preserva suas identidades. (3.2) não decide isso por nome.
- [OPEN] A remoção indutiva das anomalias renormalizadas/QME, sua compatibilidade com independência de fundo e com o estado físico interagente permanecem enunciados distintos.
- [FORA DO ESCOPO] Anomalias globais discretas, grandes transformações, bordos, torção, completude UV e confirmação física.

O resultado novo é a eliminação de uma obstrução cohomológica local precisamente tipada. Não constitui uma declaração de que a gravidade quântica foi resolvida.
