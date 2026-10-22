# Eliminação relativa suave por compatibilidade e homotopia de Spencer

10/09/2026, arco 071. [DERIVED — demonstração escrita, usando resultados primários identificados]. Não houve execução de um.py, Lean ou CAS. A nota acrescenta um resultado à entrega 070; não altera suas fontes.

**Resultado novo.** Na álgebra **local coordenada** de coeficientes suaves nos valores (x,g,y), polinomial e finita nos jatos diferenciados, o Einstein–sigma de alvo S³ redondo satisfaz H⁴₂(δ|d_H)=0. Em particular, um ciclo M₂ puramente quadrático nos antifields tem uma primitiva relativa suave nessa álgebra. A demonstração usa o complexo de compatibilidade da Hessiana, a ausência universal de reducibilidade já demonstrada e homotopias finitas; não completa os valores y em séries formais. O resultado não identifica essa álgebra com a subálgebra natural covariante e não conclui H²_char,cov=0.

## 1. A álgebra do enunciado e a diferença em relação à pergunta covariante

Fixe uma carta contrátil O do espaço-tempo, uma vizinhança contrátil V de uma métrica Lorentziana não degenerada no espaço de seus valores e uma carta estrelada U do S³. Pode-se reduzir V para que a interpolação de valores utilizada numa homotopia permaneça não degenerada. Considere

\[
\mathcal A_{\rm coord}=C^\infty(O\times V\times U)
 [\partial_I g,\partial_J y,\partial_L\Phi^*,\partial_M C^*],
 \quad |I|,|J|\ge1,
\tag{1}
\]

com cada elemento envolvendo um número finito de jatos e um polinômio finito nas variáveis indicadas. Antifields têm a paridade e o número usuais. Formas horizontais, formas de contato e operadores diferenciais usam a mesma regra de coeficientes. A classe permite dependência coordenada explícita em x; não exige que cada primitiva seja um tensor natural de g,y. Não permite funções não polinomiais dos jatos diferenciados nem inversos de dy ou de curvaturas.

**Essa escolha é explícita.** Uma homotopia nos valores da métrica pode gerar uma função suave de g que não seja uma expressão racional tensorial em g⁻¹. O enunciado abaixo não promete eliminar essa dependência por covariantização. Ele paga o lema relativo suave ordinário nesta classe local; voltar à classe natural admissível do problema de anomalias exige um mapa adicional.

Tome a ação ambiente já escolhida, com κ,c não nulos,

\[
 S=-{1\over2\kappa}\int(R-2\Lambda)dV_g
   +{c\over2}\int g^{ab}h_{AB}(y)u_a^Au_b^B\,dV_g,
 \qquad u=dy,
\tag{2}
\]

onde h é a métrica positiva suave do S³ e Λ é qualquer constante. O gauge é somente difeomorfismo. Escreva F_i=δS/δΦ^i para as 13 equações de Euler densitizadas, Φ=(g,y). Elas são múltiplos invertíveis das equações E_ab e τ^A utilizadas em 069–070. O ideal diferencial e a superfície estacionária formal E_∞ são os mesmos.

## 2. A contribuição precisa das fontes

[KNOWN] Verbovetsky formula o complexo de compatibilidade de operadores diferenciais e sua comparação com a cohomologia horizontal. Seu Teorema 3.1 e Corolário 3.3 relacionam os grupos com formas de contato à homologia do complexo adjunto. Para um complexo de comprimento três, o teorema de três linhas anula E₁^{p,q} em p>0,q≤n−3. A prova usa resoluções de Spencer e complexos de operadores em argumentos auxiliares. A álgebra geral do artigo admite funções suaves de um número finito de jatos; preservar a subclasse polinomial de (1) é uma obrigação adicional demonstrada abaixo. [Verbovetsky, §§2.2–2.3 e 3.1](https://arxiv.org/pdf/math/9803115v1).

[KNOWN] O Teorema 6.4 de BBH, se a ordem de Cauchy for dois, só anula os graus característicos p<2 em dimensão quatro: não resolve o grau limítrofe desta tarefa. O Teorema 6.2 compara H⁴₂(δ|d_H) à cohomologia característica ordinária em grau dois, usando a KT ordinária e o lema de Poincaré algébrico. O Teorema 4.2 trata a dependência polinomial nos derivados. A rota abaixo usa esses mecanismos sem invocar a normalidade como substituto de uma primitiva suave. [BBH2000, §§4.5, 6.3–6.4](https://arxiv.org/pdf/hep-th/0002245v3).

## 3. Entrada regular já construída e sua consequência linear

[INPUT — demonstração escrita anterior] A nota `REGULARIDADE_KT_JATOS_20260909_224852/CERTIFICADO_POLINOMIAL_EINSTEIN_SIGMA.md` constrói, ordem por ordem, coordenadas estacionárias livres q e coordenadas independentes de equações z. As transformações e suas inversas são polinomiais nos jatos diferenciados, com coeficientes suaves nos valores. As relações entre equações restantes são exatamente as prolongações da identidade de Noether. A projeção de uma ordem estacionária à anterior é sobrejetiva. Esse resultado vale para Λ arbitrário; a presente nota não altera sua prova.

Na versão coordenada, incluem-se entre os q os jatos de escolha de coordenadas/referencial que parametrizam a apresentação de jatos métricos normais. A passagem entre jatos parciais e essa apresentação é triangular, de ordem finita e polinomial nos derivados. As escolhas auxiliares podem ser feitas suavemente sobre O×V×U. Não se exige aqui invariância dessas escolhas.

Seja

\[
R(v)=(\mathcal L_vg,\ v^a\partial_a y),\qquad
\Delta=R^\dagger,\qquad H=\ell_F.
\tag{3}
\]

H é a linearização universal das equações de Euler; como Hessiana variacional, é formalmente autoadjunta. A identidade de Noether é ΔF=0. Linearizá-la sobre E_∞ dá ΔH=0, pois o termo (δΔ)F desaparece nesse espaço.

**Lema 1 — compatibilidade completa na classe polinomial.** Sobre E_∞,

\[
P_0\xrightarrow{\ H\ }P_1\xrightarrow{\ \Delta\ }P_2\longrightarrow0
\tag{4}
\]

é um complexo formalmente exato de compatibilidade: em cada ordem finita, a imagem prolongada de H é exatamente o núcleo das relações prolongadas Δ, e Δ prolongado é sobrejetivo. Os levantamentos necessários podem ser escolhidos com coeficientes na classe (1).

**Demonstração.** Diferencie, num jato estacionário z=0, a transformação triangular invertível (q,z) da KT069. A variação de z é livre. As variações de todas as componentes de F são obtidas dessas variações livres mediante as relações linearizadas de Noether; são, portanto, precisamente ker jΔ. Reciprocamente, escolha δq=0 e δz igual às componentes independentes de uma coleção que satisfaz essas relações. A derivada da transformação inversa fornece um jato de variação dos campos cuja imagem por jH é a coleção prescrita. Tanto essa matriz quanto as relações têm coeficientes polinomiais nos jatos diferenciados, suaves nos valores.

Para a última sobrejetividade, o símbolo principal de Δ é a divergência do tensor métrico simétrico; as parcelas sigma e de conexão são de ordem inferior no argumento. A divergência sobre polinômios homogêneos é sobrejetiva em toda ordem, como construído em KT069. Seu levantamento, seguido da correção triangular dos termos inferiores, resolve jΔv=w para qualquer w de ordem finita. Há um número finito de correções porque a ordem do argumento diminui. Não existe um novo operador de compatibilidade após Δ. ∎

É a exatidão de (4), com os levantamentos indicados, que se usa a seguir. A mera existência de uma Hessiana hiperbólica após gauge-fixing não teria fornecido essa afirmação. Não se faz gauge-fixing nem se troca o complexo por um propagador.

## 4. Homotopia de operadores que preserva suavidade e finitude

[DERIVED] Esta seção paga a preservação da subálgebra (1) nos passos da comparação de Verbovetsky.

Considere um operador diferencial em um argumento auxiliar v, de ordem r, tomando valores em q-formas horizontais. Seu símbolo é um polinômio homogêneo de grau r numa covariável auxiliar ζ. No complexo em que o diferencial é composição com d_H, a parte de maior ordem no argumento é

\[
\sigma=\zeta_a\,dx^a\wedge .
\]

Defina

\[
h=\sum_a\partial_{\zeta_a}\,\iota_{\partial_a}.
\]

Usando ι_a(dx^b∧)+(dx^b∧)ι_a=δ_a^b e a regra do produto em ζ, obtemos, sobre símbolos de graus (r,q),

\[
\sigma h+h\sigma=(r+n-q)\,\mathrm{id}.
\tag{5}
\]

Em n=4 e q<4, o denominador é estritamente positivo. Se σA_r=0, então A_r=σ(hA_r/(r+4−q)). O primitivo tem ordem r−1 no argumento. Subtrair a composição d_H desse operador remove o termo de maior ordem. A derivada dos coeficientes só produz termos de ordem inferior no argumento. Repetindo, a ordem r desce estritamente. Na ordem zero, um símbolo fechado abaixo do grau máximo é zero. Logo o processo termina em um número finito de etapas.

Todas as operações são somas, contrações, derivadas totais e divisão por inteiros positivos. Diferenciar um coeficiente C∞(x,g,y) continua suave e apenas acrescenta fatores de primeiros jatos. Não há inversão de uma função dos jatos. Cada entrada polinomial produz uma saída polinomial com ordem finita, embora não se afirme que seu peso K seja idêntico ao da entrada.

Se há outros argumentos de contato, trata-se um deles como argumento distinguido. Os demais ficam no módulo de coeficientes; suas derivadas continuam finitas em cada etapa. A antissimetrização final é uma soma finita. Os levantamentos através de (4) são as matrizes finitas do Lema 1. Assim os zigzags de complexos duplos usados para a comparação têm um número finito de setas horizontais e cada homotopia usada nelas termina em ordem finita.

**Conclusão da adaptação.** O cálculo de contato que, na fonte, é formulado para funções suaves gerais, vale também na subálgebra (1). Não se apela ao fato insuficiente de que um primitivo suave em todos os jatos existe: a construção acima controla sua polinomialidade nos jatos diferenciados. Também não há série formal nos valores materiais.

## 5. Os grupos de contato necessários ao grau dois

Denote por E₁^{p,q} a cohomologia horizontal com p fatores de contato e q fatores horizontais, restrita à superfície estacionária. Aplicar a comparação da seção 2 ao complexo (4), com a preservação provada na seção 4, dá

\[
E_1^{1,2}\cong\ker\Delta^\dagger=\ker R,
\tag{6}
\]

porque n−q=2 e não há P₃ no complexo adjunto. Para p>0 e q≤1, n−q≥3 está além do último termo de (4), portanto

\[
E_1^{p,q}=0\qquad(p>0,\ q\le1).
\tag{7}
\]

Essas são afirmações sobre formas de contato no espaço estacionário, não ainda sobre cohomologia característica covariante.

**Lema 2 — o núcleo em (6) é zero.** A prova da entrega 070 aplica-se a funções locais da classe coordenada (1): se Rv=0 sobre E_∞, então v anula dy¹,dy²,dy³ e dQ, com Q=|dy|². Para cada valor y e g, há jatos estacionários com u_i^A=δ_i^A, u_0=0 e Hessiano B^1_01=B^1_10=b≠0 em bases adaptadas. Neles τ=0 e dQ=−2b dx⁰; os quatro covetores formam uma base.

O determinante é um polinômio não identicamente zero nos parâmetros livres de cada fibra estacionária finita. O subconjunto onde é não nulo é denso. A adjugata dá Dv=0, e a continuidade estende v=0 a toda a fibra. A dependência adicional suave em x,g não altera o argumento fibra a fibra. A função v pode depender de jatos de ordem superior: a sobrejetividade das projeções estacionárias conserva os parâmetros superiores livres. Assim ker R=0 na classe (1), sem dividir por D. ∎

Juntando (6) e (7), temos os três grupos exatos de que precisaremos:

\[
E_1^{1,2}=E_1^{2,1}=E_1^{3,0}=0.
\tag{8}
\]

## 6. De uma 2-forma horizontal fechada a uma forma total fechada

Seja ρ de grau horizontal dois sobre E_∞, d_Hρ=0. A distribuição de Cartan é plana e separa o diferencial total em d=d_H+d_V, com d_H²=d_V²={d_H,d_V}=0.

Por E₁^{1,2}=0, existe uma forma α₁₁ de bidegrau (contato,horizontal)=(1,1), na mesma classe, tal que

\[
d_V\rho+d_H\alpha_{11}=0.
\]

Aplicando d_V, vemos que d_Vα₁₁ é d_H-fechada. Por E₁^{2,1}=0, existe α₂₀ com

\[
d_V\alpha_{11}+d_H\alpha_{20}=0.
\]

Finalmente d_Vα₂₀ é d_H-fechada e tem bidegrau (3,0). A nulidade de E₁^{3,0} força d_Vα₂₀=0, pois não há primitivas de grau horizontal −1. Portanto

\[
\Omega=\rho+\alpha_{11}+\alpha_{20},\qquad d\Omega=0.
\tag{9}
\]

A construção usa duas correções de contato e um último teste de anulação. As primitivas são finitas pelas seções 3–4. Não há uma sequência infinita de correções de campos nem uma premissa de convergência.

## 7. A homotopia total no espaço estacionário preserva polinômios

Pelas coordenadas triangulares da KT069, E_∞ é localmente uma torre de fibrados afins/polinomiais sobre os valores (x,g,y), com coordenadas livres q de peso derivativo positivo. Em cada ordem finita, a transformação e sua inversa são polinomiais nessas coordenadas e compatíveis com a projeção à ordem anterior. O valor q=0 fornece uma seção formal estacionária; para Λ≠0 ela inclui a curvatura determinada pelas equações, não exige uma métrica plana.

Contraia as coordenadas livres por F_t:q↦tq, deixando x,g,y fixos. Para uma forma polinomial nas fibras, o operador

\[
H_{\rm fib}\Omega=\int_0^1\frac{dt}{t}F_t^*(\iota_{E_q}\Omega),
\qquad E_q=q^\Iota\partial_{q^\Iota},
\tag{10}
\]

satisfaz dH_fib+H_fib d=id−π*ι*. Cada monômio de grau positivo nas coordenadas e seus diferenciais produz somente a divisão por seu grau inteiro. A saída continua polinomial. A operação não aumenta infinitamente a ordem do jato, porque a forma de entrada depende de uma etapa finita da torre e as coordenadas são triangulares nessa etapa.

Essa contração não precisa preservar holonomicidade ou soluções globais: é uma homotopia do espaço de jatos estacionários para calcular o diferencial total de de Rham. As soluções e o diferencial horizontal já foram usados nas etapas anteriores.

A base O×V×U foi escolhida contrátil. Uma homotopia de Poincaré nos **valores** produz primitivas suaves dos termos restantes. Nessa etapa a integração é de funções suaves de x,g,y num intervalo compacto dentro da carta; não se expande essas funções em Taylor. Como ela não integra funções não polinomiais dos q, a polinomialidade dos jatos diferenciados continua preservada.

Logo a 2-forma total fechada Ω de (9) é Ω=dβ com β da classe (1). Projetar para grau de contato zero dá

\[
\rho=d_H\beta_{01}.
\tag{11}
\]

**Teorema horizontal local ordinário.** H²_hor(E_∞,A_coord)=0, com primitivas suaves nos valores e polinomiais finitas nos jatos diferenciados. O enunciado vale sobre a carta completa escolhida, incluindo jatos de matéria degenerados; não foi obtido pela localização em dy.

## 8. Retorno explícito à eliminação relativa M₂

[DERIVED] A KT069 resolve o ideal estacionário na mesma classe coordenada. O lema de Poincaré horizontal off-shell é aplicável em O×V×U e preserva a classe polinomial derivada; sua homotopia nos valores é uma integral suave, não uma série formal.

Parta de um ciclo a₂⁴, em particular M₂, com

\[
\delta a_2^4+d_Ha_1^3=0.
\tag{12}
\]

O descendente usual existe porque aplicar δ a (12) torna δa₁³ horizontalmente fechado. O lema off-shell permite encontrar a₀² com

\[
\delta a_1^3+d_Ha_0^2=0.
\tag{13}
\]

Sobre E_∞, a₀² é fechada. Pela seção 7, a₀²=d_Hb₀¹ sobre E_∞. A diferença fraca tem certificado KT, então, off-shell,

\[
a_0^2=d_Hb_0^1+\delta b_1^2.
\tag{14}
\]

Adotando δd_H+d_Hδ=0, (13)–(14) dão δ(a₁³−d_Hb₁²)=0. Pela KT ordinária positiva, a₁³−d_Hb₁²=δb₂³. Substituir em (12) dá δ(a₂⁴−d_Hb₂³)=0. Novamente KT fornece a₂⁴−d_Hb₂³=δb₃⁴. Portanto

\[
\boxed{a_2^4=\delta b_3^4+d_Hb_2^3.}
\tag{15}
\]

Todas as operações acima permanecem na classe (1) e são de ordem finita. Se outras convenções fazem δ comutar com d_H em vez de anticomutar, os sinais dos descendentes mudam, mas (15) conserva seu significado de exatidão relativa.

Isso demonstra H⁴₂(δ|d_H,A_coord)=0 e elimina M₂ suave **ordinário**. Não se usou o Teorema 6.7 de BBH com uma hipótese de normalidade suave ainda não paga; a comparação necessária foi obtida pelo complexo de compatibilidade e pelas homotopias descritas.

## 9. Controle independente de baixo peso

[DERIVED] Há uma verificação simples na subclasse natural da nota 070. Com K=N_∂+2N_Φ*+3N_C*, um M₂ puro de peso mínimo K=4 não contém derivados: M₂=½Φ_i* A^{ij}(g,y)Φ_j* d⁴x, com A antissimétrica nas componentes bosônicas. A derivada de Euler em Φ* da equação de ciclo relativo dá A^{ij}F_i=0. Os treze valores F_i podem ser prescritos independentemente nos jatos de segunda ordem, pelo split KT069; logo A=0. Nesse peso o representante é zero, não apenas exato.

Para densidades naturais escalares construídas dos antifields métricos de posto dois, antifields sigma de posto zero, métrica e volume, os pesos K ímpares são excluídos pela paridade do número de índices de Lorentz: cada derivada acrescenta um índice, enquanto métrica e ε possuem número par. Esse controle não é o argumento geral de (15), nem uma exclusão de todos os pesos maiores.

## 10. Consequência prática e resíduo que continua aberto

O resultado novo permite retirar a obrigação **“M₂ relativo suave ordinário numa carta”** da lista de lacunas, desde que a primitiva seja aceita na álgebra coordenada (1). Preserva funções C∞ genuínas do alvo e ordem finita; não precisa de normalidade formal ou de convergência de séries nos valores.

O contrato restante para o canal de anomalias é real: construir o retorno de tais primitivas para a classe natural covariante admissível, preservar a classe de coeficientes métricos desejada e efetuar a colagem/descida pertinentes. A primitiva β₀₁ da seção 7 pode depender das escolhas de carta e da homotopia dos valores. H²_hor ordinário nulo não garante uma primitiva estritamente covariante; classes de Chern–Weil dão exemplos gerais dessa diferença em outros graus/modelos.

Não se declara aqui H²_char,cov=0, ausência de toda anomalia, QME satisfeita, estado interagente físico, independência de fundo ou completude UV. Também não se impõe a identificação g[P],φ[P] à ação ambiente: a compatibilidade e a Hessiana desta nota pertencem à ação (2) com campos independentes.

O ganho é uma demonstração relativa suave local efetiva, com a classe alargada de primitivas explicitada e um único retorno covariante ainda separado. Fonte, notas de entrada e este artefato são pinados no manifesto novo; nenhum estatuto Lean ou gate foi produzido.
