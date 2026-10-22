# Invariantes quadráticos de Killing: nulidade por KT linear e cohomologia horizontal

10/09/2026. Investigação085 NOVA, excluída da entrega084. [DERIVED — demonstração escrita, aguardando revisão independente específica]. [KNOWN — aplicação delimitada de BBH2000 nos enunciados citados]. Zero CAS, Lean ou execução/importação de um.py. Somente arquivos novos em Chatgpt.

**Resultado no domínio fixado.** Se \(\mathcal M\) é o módulo real de observáveis lineares de jatos métricos modulo as equações Einstein lineares da referência espaço-forma080–082, então
\[
\boxed{
\left(R_{\rm her}\otimes_{\mathbb R}\operatorname{Sym}^2\mathcal M\right)^{\mathfrak g}=0.
}
\tag{1}
\]
\(\mathfrak g\) é toda a álgebra de Killing, não apenas sua isotropia. Cada elemento tem ordem finita de jatos. Não se demonstra nem se presume liberdade da torre de Weyl, local finitude sob \(\mathfrak g\), um princípio de separação pelos testes TT ou ausência de nilpotentes em \(R_{\rm her}\).

O argumento passa por uma injeção no quociente polinomial dos jatos de h pelas EOM lineares. A invariância fornece uma função horizontalmente constante nesse quociente. A resolução KT estritamente linear é local e acíclica; a cohomologia característica ordinária de grau zero reduz a função a uma constante. Sua homogeneidade quadrática força essa constante a ser zero. A injeção retorna ao módulo original sem precisar naturalizar uma primitiva.

## 1. Categoria e diferença entre os três quocientes

Mantemos a [categoria080](<C:/IALD/Central de Patentes/Chatgpt/GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md>): referência g0 Lorentziana orientada em dimensão quatro, espaço-forma com K>0 real fixado, κ não nulo fixado, \(\phi_0\) constante projetada, setor métrico mínimo. \(R_{\rm her}\) é uma álgebra real unital de escalares inertes depois de fixar os parâmetros do operador. Nenhum espectador tensorial ou não constante é acrescentado.

No começo da prova trabalhamos sobre o corpo real. Em um ponto x, seja U o espaço das combinações lineares FINITAS dos jatos de h. Todos esses jatos são livres antes das equações. Seja \(\mathcal E\subset U\) a imagem das combinações lineares finitas dos jatos de \(H_0h\). Denote por
\[
\gamma:U\longrightarrow U_C
\]
o mapa linear induzido por \(s_0h=R_0C\), com \(R_0C=2\bar\nabla_{(a}C_{b)}\). A identidade \(H_0R_0=0\) implica \(\mathcal E\subset\ker\gamma\).

Assim, diretamente da definição do módulo linear,
\[
\mathcal M=\ker\gamma/\mathcal E
\ \lhook\joinrel\longrightarrow\
\mathcal U:=U/\mathcal E.
\tag{2}
\]
Não há aqui uma afirmação de que qualquer tensor formal de Weyl possa ser prescrito independentemente. Os jatos de Weyl geram \(\mathcal M\) por080; todas as suas relações permanecem em \(\mathcal M\).

O quociente polinomial on-shell dos jatos originais é
\[
\mathcal A_{\rm os}=\operatorname{Sym}(U)/(\mathcal E)
\simeq\operatorname{Sym}(U/\mathcal E).
\tag{3}
\]
Esta igualdade decorre do ideal gerado por relações LINEARES, e não de um teorema de coordenadas livres para a torre de Weyl. Sobre um corpo, uma inclusão de espaços vetoriais cinde; sua potência simétrica é injetiva. Aplicando isso a(2),
\[
\boxed{\operatorname{Sym}^2\mathcal M
\ \lhook\joinrel\longrightarrow\
\operatorname{Sym}^2\mathcal U
\subset\mathcal A_{\rm os}.}
\tag{4}
\]

A prova usará temporariamente formas locais com coeficientes \(C^\infty(x)\) numa carta contrátil, polinomiais nos jatos de h e nos antifields. Isso é uma classe COORDENADA auxiliar, maior que a natural. Ela não será identificada com a classe natural. Quando se obtiver zero em(3), a inclusão(4) bastará para concluir zero no módulo natural inicial.

Distinções preservadas: \(\mathcal M\) é a cohomologia linear gauge-invariante; \(\mathcal A_{\rm os}\) é o quociente pelas EOM; a cohomologia horizontal de grau zero mede \(d_HF=0\) nesse quociente. Nenhuma delas é confundida com toda a cohomologia CE ou com a cohomologia relativa de isotropia.

## 2. KT da teoria estritamente linear: a regularidade necessária

Nesta seção δ é somente Koszul–Tate, não o s0 completo. O ghost C não é necessário na álgebra auxiliar. Mantemos h, o antifield de h e o antifield do ghost. Usando a [normalização081](<C:/IALD/Central de Patentes/Chatgpt/COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md>) e o [sinal KT corrigido077](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>), escrevemos os antifields normalizados como p e q:
\[
\delta h=0,\qquad
\delta p=Hh,\qquad
\delta q=\mathcal Dp,\qquad
(\mathcal Dp)_b=\bar\nabla^ap_{ab},\quad \mathcal DH=0.
\tag{5}
\]
p tem antifield number um e q tem antifield number dois. As normalizações densitizadas são invertíveis com coeficientes de g0; H é o mesmo Hessiano Einstein, após esses isomorfismos algébricos. δ é LINEAR nos geradores e preserva seu grau polinomial total.

### 2.1. Todas as relações lineares das EOM são geradas pela Bianchi

A [fatoração079](<C:/IALD/Central de Patentes/Chatgpt/SUBSETOR_ANTIFIELD_PURO_079_20260910_041018_659161/ANTIFIELD_PURO_FATORACAO_BIANCHI_E_DELTA.md>) e a aplicação pontual de081 demonstram
\[
PH=0\quad\Longrightarrow\quad P=B\mathcal D
\tag{6}
\]
para operadores finitos, inclusive com saída tensorial. O fator B tem ordem no máximo \(\operatorname{ord}P-1\); o ciclo de ordem zero é zero. O algoritmo é linear nos coeficientes: usa a fatoração polinomial do núcleo do símbolo Einstein e subtrai Bianchi, reduzindo a ordem até zero.

Essa mesma construção funciona para coeficientes suaves x-dependentes na carta auxiliar. Os coeficientes ficam à esquerda. Na composição \(B\mathcal D\), as derivadas agem no operador \(\mathcal D\) e no argumento, não numa extensão escolhida arbitrariamente para os coeficientes de B. O símbolo e cada resto inferior dependem suavemente dos coeficientes iniciais e dos jatos finitos de g0. A identidade \(\mathcal DH=0\) é exata em toda a carta.

Logo o módulo linear de antifield number um é exato no complexo KT. Não se está usando a falta de soluções Killing: a afirmação é sobre identidades diferenciais para argumentos arbitrários.

### 2.2. Não há identidades entre as identidades de Bianchi

É necessário também verificar o extremo q, que não era exigido pela contagem E5 de081. Suponha
\[
Z\mathcal D=0
\]
como operador sobre todo p simétrico, ou como relação entre seus jatos em um ponto. No símbolo superior, levantar e baixar índices identifica essa condição com
\[
\zeta_a z_b(\zeta)+\zeta_b z_a(\zeta)=0
\tag{7}
\]
para o polinômio símbolo z de Z e a covariável \(\zeta\).

Para cada \(\zeta\ne0\), escolha um índice j com \(\zeta_j\ne0\). A componente jj de(7) dá \(z_j=0\); a componente jb dá \(z_b=0\) para todo b. Portanto o símbolo é zero para todo \(\zeta\ne0\) e, sendo polinomial, é identicamente zero. A ordem de Z diminui. A repetição termina e dá Z=0.

Esse argumento não divide por \(\zeta^2\), não escolhe um cone causal e não constrói denominadores em jatos. O índice j é usado apenas para provar nulidade pontual de um polinômio. Também não depende de uma ausência de Killing: uma solução \(R_0v=0\) não é um operador que produza \(R_0Z[f]=0\) para todo parâmetro f.

Com(6), isso estabelece a exatidão positiva do complexo LINEAR KT:
\[
0\longrightarrow L_q\xrightarrow{\delta}L_p
\xrightarrow{\delta}U\longrightarrow\mathcal U\longrightarrow0.
\tag{8}
\]
Esta é a irreducibilidade diferencial necessária para aplicar o teorema linear. A existência de cargas associadas a Killing em outro grau relativo não contraria(8).

### 2.3. Acyclicidade polinomial com ordem finita

Os cortes auxiliares
\[
w(h_I)=|I|+1,\qquad
w(p_I)=|I|+3,\qquad
w(q_I)=|I|+4
\tag{9}
\]
são finitos e estáveis por δ. A fatoração(6) conserva esse corte: p com r derivadas tem peso r+3; sua primitiva q usa no máximo r−1 derivadas e tem o mesmo peso. A injetividade no extremo q vale em cada corte. Assim esses complexos finitos são exatos nos graus positivos.

Em componentes de um frame ortonormal LOCAL da referência, os mapas entre jatos covariantes simetrizados são matrizes tensoriais numéricas dependentes do K fixado. Comutadores só produzem K e ordens inferiores. Podem-se escolher cisões reais nessas matrizes finitas e transportá-las suavemente pela carta. O frame é ferramenta de coordenadas para a prova, não um dado físico acrescentado.

Cada corte cinde em representantes de \(\mathcal U\) e pares \(u_i,v_i=\delta u_i\). Na álgebra simétrica graduada, a homotopia
\[
\rho=\sum_i u_i\,\frac{\partial}{\partial v_i},
\qquad
\delta\rho+\rho\delta=N_{\rm pares}
\]
contrai os monômios que contêm algum par, dividindo por seu número positivo de fatores. O número é um inteiro; não se divide por um campo. Um polinômio finito usa um corte finito, e sua primitiva continua nesse corte. Coeficientes \(C^\infty(x)\) são inertes para δ e não alteram a conta.

Portanto
\[
\boxed{H_{k>0}(\delta)=0,\qquad H_0(\delta)=\mathcal A_{\rm os}}
\tag{10}
\]
na classe auxiliar local, polinomial e de ordem finita. A construção conserva o grau total nos geradores. Esse pagamento da aciclicidade é próprio do sistema LINEAR em estudo. Não importa por nome uma resolução não linear inteira de Einstein–sigma.

## 3. O resultado horizontal primário que se aplica

[KNOWN — fonte primária conferida] [BBH2000, Teorema6.2, equação(6.17)](https://arxiv.org/pdf/hep-th/0002245v3) identifica \(H^0_0(d_H\mid\delta)/\mathbb R\) com \(H^4_4(\delta\mid d_H)\). O Teorema6.5(i) anula \(H^4_k(\delta\mid d_H)\) para k≥3 em sistemas lagrangianos LINEARES irreducíveis com a resolução KT local. Li também sua prova no apêndice6.B, de(6.44) a(6.49) e o encerramento do caso linear. Ali os restos que aumentariam o grau desaparecem quando a ação é quadrática e os geradores de gauge não dependem de h. A extensão a teorias apenas linearizáveis é tratada separadamente por série formal.

Aqui a ação auxiliar é precisamente a ação quadrática do Hessiano Einstein no fundo on-shell; R0 tem coeficientes de g0 e é independente de h. O §2 paga a resolução local e a irreducibilidade. Logo
\[
\boxed{H^0_0(d_H\mid\delta)=\mathbb R.}
\tag{11}
\]
Não se aplica Whitehead nem se presume Cauchy order de um modelo não linear.

**Controle da classe da aplicação.** Os coeficientes de g0 podem depender de x; isso não altera a homogeneidade estrita da ação quadrática e dos mapas(5) em h,p,q. As operações de Euler e integração por partes empregadas no argumento local diferenciam esses coeficientes suavemente, mas preservam ordem finita. A aciclicidade(10) fornece preimagens polinomiais finitas a cada uso. A homotopia de escala nos geradores reduz-se, em grau homogêneo E>0, à divisão pelo inteiro E. Não aparece uma iteração que aumente indefinidamente E: os termos não lineares responsáveis por essa iteração são zero neste sistema.

A comparação de grau zero usa a álgebra de formas locais ordinárias na carta contrátil, com dependência explícita em x permitida. O lema algébrico de Poincaré e a resolução(10) são aplicados somente em graus de forma de zero a quatro. Nenhuma sequência infinita de formas ou de jatos é introduzida por essa descida. A conclusão de(11) é igualdade em(3), não somente uma afirmação sobre valores em algumas soluções analíticas.

O teorema não elimina correntes conservadas ou classes de antifield number dois associadas a Killing. Ele elimina aqui \(H^4_4\), cujo grau corresponde às funções horizontalmente constantes. Esses grupos não devem ser identificados.

## 4. Toda invariância de Killing fornece uma função horizontalmente constante

Tome
\[
n\in(\operatorname{Sym}^2\mathcal M)^{\mathfrak g}.
\]
Em particular n é invariante pela isotropia \(\mathfrak h\). Por080/081, os jatos de Weyl geram \(\mathcal M\) e cada elemento pertence a um corte tensorial finito da isotropia. Nesse corte, a exatidão de tomar invariantes fornece um representante quadrático F(h) com contrações naturais em g0 e ε0. Essa escolha não exige invariância da primitiva ou local finitude sob toda \(\mathfrak g\); usa apenas a isotropia no corte finito.

A [identificação082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>) paga a ação nas classes dos jatos:
\[
\rho_{P_a}[W_r]=[\bar\nabla_aW_r]
\]
no ponto base da referência. Todos os índices de derivadas e as relações inferiores por curvatura estão incluídos. Pelo Leibniz, e porque os coeficientes de uma contração natural são paralelos,
\[
\rho_{P_a}n=[\bar\nabla_aF].
\tag{12}
\]
Não se substituiu \(\bar\nabla\) por uma multiplicação formal em uma torre livre.

A hipótese de invariância por \(\mathfrak g\) zera(12) para todos os quatro a. A inclusão(4) transporta essa nulidade para o quociente on-shell dos jatos de h. A expressão natural e a homogeneidade local da espaço-forma transportam a mesma identidade do ponto base para toda uma carta: as relações de EOM e a contração são equivariantes pelas isometrias.

F é escalar, logo sua derivada covariante é a derivada total ordinária da função local. Obtemos
\[
\boxed{d_HF=0\quad\text{em }\mathcal A_{\rm os}.}
\tag{13}
\]
Essa etapa não exige realizar quaisquer dados de Weyl arbitrários por soluções convergentes. Trata-se de identidade no quociente linear de jatos e no ideal polinomial que ele gera.

## 5. Retorno ao módulo original: a constante de grau dois é zero

Por(11) e(13), existe um número real c tal que
\[
[F]=c\quad\text{em }\mathcal A_{\rm os}.
\]
O ideal \((\mathcal E)\) é homogêneo, pois as EOM são estritamente lineares. F tem grau polinomial dois em h e seus jatos. Sua classe não pode coincidir com uma constante não nula de grau zero. Equivalentemente, a avaliação em h=0 e todos os seus jatos zero é bem definida no quociente, e dá 0=c.

Consequentemente \([F]=0\) em(3). Pela INJETIVIDADE de(4), segue n=0 no próprio \(\operatorname{Sym}^2\mathcal M\):
\[
\boxed{(\operatorname{Sym}^2\mathcal M)^{\mathfrak g}=0.}
\tag{14}
\]

Este é o motivo de a ampliação auxiliar para coeficientes suaves em x não ser uma troca indevida de classe. A conclusão é zero no quociente pontual original. Não precisamos transformar uma primitiva coordenada arbitrária numa primitiva natural. Uma eventual expressão auxiliar F−c=δB, avaliada no ponto, já coloca F no ideal das MESMAS EOM lineares; a inclusão(4) faz o retorno.

Também não há uso de radicalização do ideal por avaliações numéricas. A igualdade é obtida dentro do quociente algébrico pelas relações lineares. Não se deduziu pertencimento ao ideal simplesmente de anulação em uma família de soluções.

## 6. Extensão por Rher, inclusive com nilpotentes

Seja \(V=\operatorname{Sym}^2\mathcal M\) sobre \(\mathbb R\). Escolha uma base finita \(X_A\), A=1,...,10, de \(\mathfrak g\), e forme o mapa real
\[
\Phi:V\longrightarrow V^{\oplus10},\qquad
\Phi(v)=(\rho_{X_A}v)_A.
\]
Seu núcleo é \(V^{\mathfrak g}=0\), por(14). Toda álgebra real é plana como módulo sobre o corpo real. Tensorizar a sequência exata no núcleo por \(R_{\rm her}\) preserva a injetividade:
\[
0\longrightarrow R_{\rm her}\otimes V
\xrightarrow{1\otimes\Phi}
(R_{\rm her}\otimes V)^{\oplus10}.
\]
O núcleo à direita é precisamente a invariância da extensão escalar inerte. Isso prova(1).

Uma descrição equivalente evita qualquer leitura geométrica dos coeficientes: cada elemento do produto tensorial algébrico é uma soma finita \(\sum_i r_i\otimes v_i\); pode-se escolher os \(r_i\) linearmente independentes como vetores REAIS. As equações de invariância então valem para cada \(v_i\). Essa separação linear não é uma avaliação multiplicativa \(R_{\rm her}\to\mathbb R\) e não apaga nilpotentes.

Não se mudou o anel herdado. A exigência é a já fixada080–084: o operador e K/κ foram fixados antes, e \(R_{\rm her}\) atua como extensão escalar trivial. A prova não trata um diferencial dependente de K variável como se fosse \(1\otimes\delta_{\mathbb R}\), nem introduz localizações novas. Produtos completados de jatos fora da categoria de elementos finitos não são inferidos dessa sequência.

## 7. Consequência exata para o canal de Euler084

O [critério084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>) fornece, no complexo natural indicado,
\[
J_W\nu\in d_{\rm CE}(C_{\rm nat}^3)
\ \Longleftrightarrow\
J_W=\operatorname{div}_0V+K^2f,\qquad
f\in\mathscr N^{\mathfrak g},
\quad\mathscr N=R_{\rm her}\otimes\operatorname{Sym}^2\mathcal M.
\]
Por(1), f=0. Portanto a condição reduz-se a
\[
\boxed{
J_W\nu\in d_{\rm CE}(C_{\rm nat}^3)
\ \Longleftrightarrow\
J_W=\operatorname{div}_0V,
\quad V\in(\mathscr N\otimes V_0)^{\mathfrak h}
\text{ de ordem finita}.
}
\tag{15}
\]
O mesmo resultado retira coeficientes quadráticos invariantes de ambas as cúbicas de Cartan na forma normal084. Para uma primitiva cujo diferencial seja inteiramente horizontal, sobra uma corrente horizontal mais uma fronteira CE finita. Isso depende do lema de forma normal084; não é uma classificação de toda a cohomologia com outros alvos.

A unidade escalar do anel não reabre o canal: ela tem grau zero em h e não pertence ao setor quadrático homogêneo em que f era exigido.

[OPEN] Não construímos V de(15) e não demonstramos sua inexistência. A nulidade de funções horizontalmente constantes é um problema de grau zero; a divergência exigida em(15) é um problema de grau quatro. O teorema usado para o primeiro não resolve automaticamente o segundo.

Também permanecem fora: a cohomologia CE completa, ordens seguintes da torre, admissibilidade causal Q2, espectadores tensoriais, o fundo físico \(\phi=\mathrm{id}\), coeficientes com K variável, construções globais, QME e UV. Não se conclui fechamento geral da gravidade quântica.

## 8. Custódia e estatuto

[DERIVED] A novidade é(1), pela sequência(2)–(14), e sua consequência(15). A prova não consome resultados dos detectores TT para separar o módulo, não transforma a sobrejeção da torre080 em isomorfismo e não pressupõe ausência de nilpotentes em coeficientes.

[KNOWN] A importação horizontal é a explicitada no §3, depois de pagar a KT local do sistema estritamente linear. As fontes079–082 são antecedentes escritos delimitados. Seus pareceres não são apresentados como aprovação antecipada desta investigação085.

[REAL — documental] O manifesto mede as oito fontes antes/depois, esta nota final e o helper novo. Seus controles são documentais, não testes matemáticos. Nenhum original, fonte congelada, Atlas, índice, memória canônica ou gate foi alterado; nenhuma execução/importação de um.py, CAS ou Lean ocorreu. O resultado aguarda revisão independente específica antes da consolidação.
