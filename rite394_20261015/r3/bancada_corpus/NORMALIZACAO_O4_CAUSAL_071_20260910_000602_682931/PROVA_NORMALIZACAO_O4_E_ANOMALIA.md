# Normalização causal exatamente O(4)-equivariante e setor da anomalia

10/09/2026, continuidade 071. [DERIVED — demonstração escrita] [KNOWN — existência e liberdade de renormalização de Q2]. Nenhum CAS, Lean ou um.py executado. Fontes anteriores preservadas.

**Resultado.** A construção Q2 Einstein–sigma admite uma escolha exatamente equivariante sob a ação rígida O(4) do alvo, como **família de prescrições sobre os dados de fundo transportados conjuntamente**. A demonstração faz a média na liberdade local da ordem corrente e reconstrói a prescrição completa pelo teorema de renormalização. Ela preserva a fatorização causal e a unitariedade. Não faz média indiscriminada de famílias completas de produtos temporais.

A anomalia BV produzida por essa normalização pertence ao setor O(4)-invariante global **dessa família de cochains de fundo**. Isso não supõe uma primitiva nem prova sua existência. Também não remove a dependência de fundo, não equivale a uma ação de O(4) inteiro num único completamento formal centrado em phi_bar=id e não identifica automaticamente o setor com uma álgebra que dependa somente do campo completo phi.

## 1. Entradas e apoio primário precisamente usados

A [construção Q2 de 069](../CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md) fornece produtos locais causais do sistema métrica–sigma–ghost, no espaço formal EFT, com campos/anticampos e coeficientes locais dos dados de fundo. O [dicionário graduado](../CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md) fixa o BRST livre, a involução, as contrações e a ação gauge fixada. Usam-se esses resultados no alcance já examinado; não se importa a ausência de anomalias de Yang–Mills como se fosse um resultado sigma.

[KNOWN] O ingrediente de renormalização é a determinação causal fora da diagonal e a liberdade local nas extensões. O Teorema 2 inclui a recíproca: contratermos com as propriedades indicadas definem outra família admissível. As condições de realidade, suporte diagonal, escala e ação por partes da liberdade estão explicitadas em (254)–(259); a identidade de unitariedade em (151) é a que usaremos abaixo. [Hollands, §§3.3, 3.5–3.6, Teorema 2](https://arxiv.org/pdf/0705.3340v4).

[KNOWN] O mapa de anomalia para uma derivação graduada resulta da identidade de Ward e de sua recorrência local. A especialização ao BV livre e a identidade de consistência não exigem que a anomalia seja zero. A liberdade de renormalização por Z aparece também em (30)–(31). [Fröb, §2, Teoremas 3, 6 e 7](https://arxiv.org/pdf/1803.10235).

A média compacta e sua aplicação à liberdade afim abaixo são demonstradas aqui. Não se atribui aos artigos a construção específica com alvo S³ ou a equivalência de quaisquer classes de cohomologia adicionais.

## 2. A ação global do grupo nos dados reais do modelo

Denote coletivamente o fundo por b=(gbar,phi_bar,...), incluindo os dados externos declarados. Para R∈O(4),

\[
b\longmapsto Rb=(\bar g,R\bar\phi,\ldots),\qquad
(h,\xi,b_{\rm aux},c,\bar c)\longmapsto
(h,R\xi,b_{\rm aux},c,\bar c).
\tag{1}
\]

A conexão do alvo, a métrica e a exponencial são transportadas. A identidade global

\[
R\operatorname{Exp}_{\bar\phi}(t\xi)
=\operatorname{Exp}_{R\bar\phi}(tR\xi)
\tag{2}
\]

segue da expressão Exp_z(v)=cos|v| z+(sin|v|/|v|)v na esfera. A extensão suave em v=0 e cada coeficiente formal são preservados. A parte métrica e os ghosts de difeomorfismos são singletos; os anticampos de matéria transformam na representação dual. Não se adiciona um ghost de gauge O(4): a simetria considerada é rígida.

A ação Einstein–sigma, os seus vértices, a fixação de de Donder e a ação BV são equivariantes. R é constante no espaço-tempo, portanto R Lie_C phi=Lie_C(Rphi). O antibracket é preservado pelo levantamento dual; consequentemente o BRST completo e o livre comutam com o transporte entre b e Rb. O mapa de gauge K também é transportado, enquanto C ignora o slot sigma.

Os operadores livres satisfazem P_Rb=U_R P_b U_R⁻¹, com U_R igual a R no slot tangente e identidade nos demais. A unicidade dos Green retarded/advanced fornece a mesma relação para os Green. Os parametrices locais de Hadamard podem ser escolhidos equivariantes: suas equações de transporte, dados iniciais, contrações e conexões são preservados por U_R. Uma normalização com outra realização Hadamard é comparada pelo isomorfismo de ordenação suave já descrito em Q2; não se exige que o estado usado para representar a álgebra seja O(4)-invariante.

Assim existem isomorfismos de álgebras livres

\[
\alpha_{R,b}:\mathcal W_b\longrightarrow\mathcal W_{Rb}
\tag{3}
\]

que preservam produto estrela, unidade, suporte, ghost, paridade e a involução. A mesma notação será usada para transportar funcionais de entrada. A realidade é direta: R é real e age em campos bosônicos tangentes; o sinal barc*=−barc permanece no slot inalterado. Não há transformação antiunitária associada a det R=−1, pois a orientação espaço-temporal não foi invertida.

## 3. Qual espaço admite a média

Para uma prescrição T sobre essa família de fundos, defina a prescrição transportada, de volta ao mesmo objeto b, por

\[
T^R_{n,b}(F_1,\ldots,F_n)
=\alpha_{R,b}^{-1}\,
 T_{n,Rb}(\alpha_{R,b}F_1,\ldots,\alpha_{R,b}F_n).
\tag{4}
\]

Equivariância significa T^R=T para todo R. O grupo não move as posições espaço-temporais, as diagonais ou os suportes dos testes. Comuta com embeddings espaço-temporais que transportam os dados e com as operações de derivação usadas na identidade de ação por partes.

A classe Q2 utilizada aqui é a de contratermos locais formais, em cada coeficiente de ordem de jato e valência finitas, com a graduação e as condições de escala daquela construção. Os coeficientes no alvo são globais suaves; a dependência geométrica de cada termo local é a permitida pela construção de escala. R transporta linearmente os tensores e os jatos globais do mapa e da flutuação. Logo preserva valência perturbativa, ordem de jato e grau diferencial. A média de um coeficiente suave sobre o compacto O(4) é suave; derivadas finitas podem ser trocadas com a integral. Não se cria um denominador em campos nem se aumenta a ordem de delta derivada.

As condições microlocais não pioram: o grupo age nos índices internos e em coeficientes locais, sem alterar cones espaço-temporais. Nas diferenças de prescrições, somente distribuições sobre a diagonal com coeficientes suaves são integradas. As cotas de ordem são comuns e os parâmetros do grupo percorrem um compacto. A escala quase homogênea e os seus limites de potências/logaritmos são preservados, porque R é adimensional e comuta com a escala.

Quando se usa a condição analítica da construção Q2 para dependência geométrica, a média atua nos coeficientes/tensores internos da expansão local de escala; não faz média sobre a métrica nem altera seus denominadores regulares. Na apresentação global tensorial dos dados sigma, isso preserva a mesma classe analítica geométrica e a classe suave do alvo. Não se inclui uma classe arbitrariamente mais restrita de normalizações que não seja estável sob essas operações.

A integral é feita sobre cochains globais da família. Uma expressão disponível apenas numa carta do alvo não pode ser avaliada ao longo de toda órbita de R sem antes ser globalizada. Aqui Q2 usa xi∈phi_bar*TS³ e Exp global, sem uma carta que omita parte da imagem do mapa; as extensões são coeficientes/tensores desse fibrado. O procedimento não troca uma primitiva local de anomalia por uma primitiva global que não tenha sido construída.

## 4. Indução afim: preservação de fatorização causal

Escolha T1 equivariantemente usando os produtos locais de Wick da seção 2. Correções lineares locais necessárias às identidades de um fator também podem ser projetadas na mesma classe, preservando os campos lineares e a unidade. Admita que T_k, k<n, já sejam equivariantes e satisfaçam Q2.

A fatorização causal determina T_n fora da diagonal total, com valor T_i estrela T_(n−i) em cada aberto causal. Como ambos os fatores de menor ordem são equivariantes, esse valor é exatamente o mesmo para T_n e T_n^R. Portanto

\[
\Delta_n^R:=T_n^R-T_n
\quad\hbox{tem suporte na diagonal total.}
\tag{5}
\]

É uma diferença de extensões do mesmo objeto, não uma nova contribuição fora da diagonal. Pela liberdade de renormalização, pertence ao espaço linear real de contratermos admissíveis da primeira aridade em que duas prescrições diferem.

Defina a média **nesta fibra afim**, mantendo as ordens inferiores fixas:

\[
\widetilde T_n=T_n+\int_{O(4)}\Delta_n^R\,dR
=\int_{O(4)}T_n^R\,dR.
\tag{6}
\]

Por invariância de Haar, Ttilde_n é equivariante. Fora da diagonal, todos os integrandos são o mesmo T_n^0, logo a fatorização causal é preservada. Não aparece o produto de duas médias independentes: os fatores de ordens menores já foram fixados e são invariantes.

Para garantir uma **família completa** de produtos após esse passo, aplique a recíproca do teorema de renormalização à média do contratermo de aridade n, com os demais componentes novos iguais a zero. Em convenção de matriz S, se Z(F)=F+Z_n(F^n)/n! começa nessa aridade,

\[
\mathcal S_{\rm new}(F)=\mathcal S(Z(F)),\qquad
\widetilde T_n-T_n=(\hbar/i)^{n-1}T_1Z_n .
\tag{7}
\]

A relação é linear em Z_n nessa primeira aridade. A média preserva as condições homogêneas da liberdade de renormalização, inclusive sua realidade na convenção adotada. O teorema fornece todos os produtos superiores resultantes de (7); estes mudam de forma não linear e não foram obtidos por média simples. Os produtos de aridade menor que n permanecem intactos.

Repita em n+1. Cada T_k estabiliza após um número finito de passos. O limite é apenas coeficiente a coeficiente em aridade, valência e laços; não requer convergência numérica de uma série infinita de contratermos. Obtém-se uma família Q2 exatamente equivariante em todas as ordens formais. A liberdade finita restante consiste nas escolhas admissíveis que já respeitam a simetria.

## 5. Por que unitariedade e demais identidades sobrevivem

A equação de unitariedade na ordem n tem a forma, para entradas pares reais e com polarização graduada nos demais casos,

\[
T_n^*=(-1)^{n+1}T_n+\mathcal U_n(T_1,\ldots,T_{n-1}),
\tag{8}
\]

pois o termo da partição com um único bloco é o único que contém T_n. Todas as outras partições contêm somente aridades menores. Com estas fixas, (8) é uma condição **afim real** sobre T_n. Assim diferenças admissíveis obedecem Δ_n*=(-1)^(n+1)Δ_n. Como alpha_R comuta com *, a integral em (6) obedece à mesma relação e conserva o termo inferior U_n. Isso resolve especificamente a objeção de que uma média de operadores unitários não costuma ser unitária: não se fez essa média, mas uma projeção na condição afim de uma única ordem.

Simetria graduada, número fantasma, identidade de ação por partes e independência funcional dos campos são relações lineares entre os componentes da prescrição de aridade n. A média deve ser aplicada à aplicação multilinear inteira, para todas as inserções, e não só a um componente escolhido. Ela então comuta com essas relações e com as derivadas variacionais transformadas. As identidades de inserção de campos lineares e seus contatos são preservadas, porque seus termos de menor aridade já são equivariantes. A construção conserva a normalização livre, sem apagar contatos do auxiliar.

O BRST livre continua uma derivação da álgebra livre e é entrelaçado por alpha_R. Não se impôs, nem se deduziu, a identidade BV interagente sem anomalia. Para cada prescrição obtida por (7), os teoremas gerais de Ward anômala continuam aplicáveis. Se uma identidade de gauge adicional já tiver sido obtida em ordens anteriores, sua preservação por futuras correções exige a correspondente condição sobre esses contratermos; não é consequência de O(4) sozinho.

## 6. A anomalia agora pode ser escolhida no setor invariante global

Seja V_b a interação com cutoff escalar, que transporta como V_Rb=alpha_R V_b. A prescrição equivariante, a derivação livre e o antibracket fornecem uma identidade de Ward que é entrelaçada por alpha_R em ambos os lados.

O mapa de quebra é extraído recursivamente dessa identidade: na aridade n, subtraem-se os termos clássicos e as inserções de anomalias de aridades anteriores; a parte nova aparece por T1. Na álgebra fora das equações, a identificação de Wick local tem inversa formal sobre os funcionais locais. Logo a parte nova também é transportada. Por indução,

\[
\boxed{\mathcal A_{Rb}(e_\otimes^{\alpha_R V})
=\alpha_R\mathcal A_b(e_\otimes^V).}
\tag{9}
\]

Não se fez média de soluções da identidade não linear de consistência; a equivariância vem da própria construção e extração da quebra. Em particular, a primeira quebra ainda não removida, a_N, pode ser representada por uma densidade global invariante na ação diagonal sobre a família de fundos/campos. Se uma escolha de densidade representa o mesmo funcional apenas módulo d, projetar essa escolha por Haar mantém o funcional e fornece a representação invariante no mesmo quociente.

A consistência sa_N+db_N=0 continua válida e pode ser projetada simultaneamente. A realidade da quebra é a herdada da prescrição unitária e do dicionário BV; alpha_R é real e par, portanto não muda nenhum sinal dessa condição.

**Contribuição efetivamente paga:** não é mais necessário supor a simetria rígida da quebra produzida por alguma prescrição arbitrária. Existe uma prescrição Q2 que a produz no setor O(4)-invariante global da classe de fundo descrita. Isso não calcula esse setor nem mostra que seu elemento seja zero ou exato.

## 7. Primitivas: o que a projeção permite e o que continua faltando

Agora, se a_N=sB+dD já possuir primitivas **globais e admissíveis nessa mesma família**, a projeção de Haar fornece a_N=sP_GB+dP_GD. A existência inicial não foi presumida em (4)–(9), pois ali se promediavam diferenças de extensões, garantidas pela liberdade Q2, e não primitivas de uma anomalia. Esse é o avanço em relação ao lema condicional de 070.

Se B,D já satisfazem a condição graduada de realidade requerida, sua média também a satisfaz: alpha_R comuta com a involução do dicionário. Tornar uma primitiva complexa arbitrária real é outro passo e usa a realidade apropriada de a_N e as convenções de s,d; não se obtém de uma média compacta por decreto. Nenhuma média sobre Lorentz não compacto ou difeomorfismos foi usada.

Um candidato em uma representação de O(4) sem componente invariante não pode aparecer isoladamente na quebra desta normalização. Por exemplo, a orientação de H³(S³) muda de sinal sob uma reflexão do alvo; um termo nessa representação com todos os outros fatores singletos é projetado a zero. Isso não elimina produtos com outro fator da mesma paridade, nem calcula a cohomologia total. Não se importa uma conclusão sobre anomalias globais de uma seleção de representações locais.

## 8. Fronteira essencial: invariância diagonal não é independência de fundo

Para Rphi_bar diferente de phi_bar, a transformação finita não preserva o ponto central da expansão Exp_phi_bar(t xi). Tentar descrevê-la na mesma carta formal exigiria um deslocamento com termo constante não nulo antes de dividir por t; não seria a mesma série de flutuações. Em (1)–(9), o fundo também é transportado e tRxi permanece de ordem t. Se det R=−1 troca o grau topológico do mapa de fundo, a afirmação compara duas famílias formais correspondentes; não soma setores de mapas na integral funcional.

Assim O(4) inteiro age naturalmente sobre a família. Num único fundo mantido fixo, somente o seu estabilizador age dessa forma sem uma comparação adicional. A escolha de um estado representativo também não foi declarada invariante por essa construção de produtos.

Além disso, um coeficiente como 〈phi,phi_bar〉 é O(4)-invariante sob transformação simultânea, mas depende do fundo. Seu BRST quântico mantém phi_bar fixo, de modo que sua variação não é a variação natural dos dois argumentos sob uma difeomorfia conjunta. Logo a invariância paga aqui não identifica o complexo com o subcomplexo de funções do único campo completo phi, nem satisfaz independência da cisão fundo–flutuação.

Antes de usar uma classificação limitada a esse subcomplexo menor para cancelar (9), ainda se deve demonstrar a comparação apropriada e a admissibilidade das primitivas. Permanecem abertos a exatidão da quebra, o transporte entre esquemas quando requerido, a QME da construção causal, o setor físico interagente e as questões globais/UV. A simetria rígida exata não é uma Ward para transformações O(4) arbitrariamente dependentes do espaço-tempo.

## 9. Custódia

[DERIVED] A indução afim e a aplicação ao transporte O(4) dos dados Einstein–sigma são demonstrações escritas desta nota. [KNOWN] A existência de Q2 e a descrição/recíproca da sua liberdade de renormalização são as importações primárias delimitadas na seção 1. [REAL] O manifesto mede esta nota e as três fontes locais lidas antes/depois; nenhuma foi alterada. Não houve CAS, Lean, execução/importação de um.py, modificação de gate ou teste de natureza.
