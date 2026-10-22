# Redução finita dos ghosts de isotropia e o canal de Euler

10/09/2026. Investigação084 independente, separada da083. [DERIVED — demonstração escrita, pendente de revisão independente integral]. [KNOWN — somente os teoremas finito-dimensionais de Chevalley–Eilenberg indicados no §2]. Zero CAS, Lean ou execução/importação de um.py.

**Resultado concreto.** No complexo natural fixado082, uma primitiva de grau3 de um alvo horizontal de grau4 pode ser reduzida, por fronteiras FINITAS, a uma corrente horizontal e duas cúbicas de Cartan completadas por curvatura. A cúbica de traço continua fechada. A cúbica de Euler pode produzir K²fν, mas seu coeficiente f deve ser invariante sob TODA a álgebra de Killing. Não basta ser um escalar de Lorentz.

Para o alvo a=J_Wν, o critério exato obtido é

\[
\boxed{\quad
a\in d_{\rm CE}(C_{\rm nat}^3)
\ \Longleftrightarrow\
J_W=\operatorname{div}_{\!0}V+K^2f,\quad
V\in(\mathscr N\otimes V_0)^{\mathfrak h},\
f\in\mathscr N^{\mathfrak g}.
\quad}                                                    \tag{A}
\]

Aqui \(\mathscr N=R_{\rm her}\otimes_{\mathbb R}\operatorname{Sym}^2\mathcal M\), e as igualdades usam o quociente de jatos/EOM já definido. A existência de V e f em(A) NÃO é demonstrada. A redução não declara cancelamento.

## 1. O módulo efetivo e a decomposição do diferencial

Conservamos o [complexo082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>): apresentação métrica mínima de zeroformas naturais orientadas, referência espaço-forma em quatro dimensões, K>0 e κ real não nulo fixos, φ0 constante projetada e coeficientes escalares inertes herdados. \(\mathcal M\) é o módulo linear de Weyl modulo todas as relações de EOM, não uma torre livre. Não se acrescentam coeficientes dependentes do campo dinâmico, tensores espectadores ou estruturas físicas de frame.

Escreva \(\mathfrak g=\mathfrak h\oplus V_0\), com \(\mathfrak h=\mathfrak{so}(1,3)\), \(\dim V_0=4\). É o par simétrico: \([\mathfrak h,V_0]\subset V_0\), \([V_0,V_0]\subset\mathfrak h\). O ghost de valor é p; o ghost matricial \(\theta\) desta nota é Mghost da082, isto é, \(\theta_{ab}=-m_{ab}\). Não é o M de sinal oposto da nota finita, nem o módulo \(\mathcal M\).

Defina
\[
C^{r,q}=(\mathscr N\otimes\Lambda^rV_0^*
                  \otimes\Lambda^q\mathfrak h^*)^{\mathfrak h},
\qquad 0\le r\le4,\quad0\le q\le6.
\]
O primeiro grau conta p; o segundo conta θ. A soma total é o complexo CE INVARIANTE por h, e não o complexo relativo.

Separe \(d=d_0+d_1+d_2\), de bidegraus \((0,1),(1,0),(2,-1)\). Nas fórmulas de082:

\[
\begin{array}{c|ccc}
 &p&\theta& n\in\mathscr N\\ \hline
d_0&-\theta p&-\theta^2&\rho_{\mathfrak h}(\theta)n\\
d_1&0&0&p^a\rho_{P_a}n\\
d_2&0&F&0
\end{array}
\qquad F^a{}_b=Kp^ap_b .                                  \tag{1}
\]

Em jatos de Weyl, \(\rho_{P_a}\) é a derivada covariante prolongada, incluindo as relações e os termos inferiores de curvatura. Não é uma derivada plana sobre símbolos livres.

Os sinais são os do mesmo dCE; o shuffle entre ghosts horizontais e verticais inclui a regra de Koszul. Em particular, \(d_0\) identifica-se, com esse shuffle, com CE de h nos coeficientes \(\mathscr N\otimes\Lambda^rV_0^*\). De \(d^2=0\) seguem

\[
d_0^2=0,\quad\{d_0,d_1\}=0,\quad
d_1^2+\{d_0,d_2\}=0,\quad
\{d_1,d_2\}=d_2^2=0.                                      \tag{2}
\]

O termo d2 é indispensável. Retirar os ghosts θ antes de analisar esse termo excluiria justamente a possibilidade de transgressão que calculamos abaixo.

## 2. O que a finitude local somente sob h realmente autoriza

Para cada R, a imagem dos jatos de Weyl de ordem ≤R em \(\mathcal M\) é um h-módulo finito-dimensional. Tomar seu quadrado simétrico, tensorizar com as potências exteriores finitas e passar ao quociente mantém essa propriedade. Todo elemento pertence a algum desses cortes. A extensão por Rher é escalar e inerte; cada elemento usa uma combinação finita de tensores.

Não se requer que esses cortes sejam preservados por transvecções. \(d_0\) os preserva; \(d_1\) pode elevar a ordem. Cochains de h comutam com a união dos cortes porque \(\Lambda^q\mathfrak h\) é finita-dimensional. Um ciclo e qualquer decomposição finita são tratados em um corte, sem completar os jatos.

[KNOWN — importação delimitada] [Chevalley–Eilenberg, 1948, teoremas 19.1 e 24.1, pp.110–112 e117–119](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/chev-eilen.pdf) fornecem representantes invariantes para coeficientes triviais e o desaparecimento da cohomologia com coeficientes irreducíveis finitos não triviais em uma álgebra semissimples de característica zero. A decomposição completa finita separa o setor trivial dos demais. São esses resultados FINITOS que utilizamos.

Para um h-módulo finito E, a exatidão de tomar invariantes em módulos completamente redutíveis permite também trabalhar no subcomplexo \(C^\bullet(\mathfrak h,E)^{\mathfrak h}\). As peças não triviais são acíclicas, inclusive nesse subcomplexo; a peça trivial dá \(E^{\mathfrak h}\otimes H^\bullet(\mathfrak h,\mathbb R)\). A união dos cortes e a extensão escalar inerte conservam essa igualdade. Em particular,

\[
H^q(C^{r,\bullet},d_0)=
(\mathscr N\otimes\Lambda^rV_0^*)^{\mathfrak h}
      \otimes H^q(\mathfrak h,\mathbb R).                   \tag{3}
\]

A complexificação \(\mathfrak h_{\mathbb C}\simeq
\mathfrak{sl}_2\oplus\mathfrak{sl}_2\) mostra os graus restantes diretamente. Cada fator de dimensão três tem invariantes exteriores somente em graus0 e3; os dois fatores produzem

\[
H^\bullet(\mathfrak h,\mathbb R)
\simeq\Lambda(\tau_{\rm tr},\tau_E),
\qquad |\tau_{\rm tr}|=|\tau_E|=3.                          \tag{4}
\]

Assim \(H^0=\mathbb R\), \(H^3=\mathbb R^2\), \(H^6=\mathbb R\), e os demais graus são zero. São duas classes reais em grau3. Não se substituiu h pela álgebra compacta so(3), que perderia uma delas. A conjugação real permuta os dois fatores complexos e preserva suas combinações reais.

Toda primitiva vertical utilizada abaixo pode ser escolhida h-invariante e finita: em um corte, projeta-se uma primitiva para os invariantes por uma cisão h-equivarante. Isso é álgebra de módulos finitos, não uma média no grupo Lorentz não compacto. A naturalização por contrações e transporte no fundo fixado é a mesma080/081. Nenhum denominador em jatos dinâmicos ou soma infinita é introduzido. Não se afirma uma cota causal uniforme sobre os cortes.

## 3. Duas cúbicas de Cartan, com suas curvaturas preservadas

Para matrizes em \(\mathfrak h\), fixe os dois bilineares invariantes
\[
B_{\rm tr}(X,Y)=\operatorname{tr}(XY),\qquad
B_E(X,Y)=\frac1{24}\varepsilon_{abcd}X^{ab}Y^{cd}.           \tag{5}
\]
A elevação usa g0. Essa normalização de \(B_E\) é escolhida AQUI para que seu polinômio de curvatura tenha o coeficiente simples abaixo; não se identifica por nome com outra normalização de Euler.

São independentes. O traço distingue um gerador de boost emparelhado consigo; o bilinear de volume o emparelha com a rotação dual. Na complexificação, dão as duas combinações dos bilineares dos fatores simples. Suas cúbicas
\[
\tau_B=-\tfrac13 B(\theta,\theta^2)
\]
representam a base de(4). A aplicação de um bilinear invariante a \(X,[Y,Z]\) é não nula salvo quando o bilinear é zero, pois h é perfeita; representantes invariantes triviais não são fronteiras por19.1.

Defina uma cocadeia escalar de grau3, com componentes \((0,3)\) e \((2,1)\):
\[
\operatorname{CS}_B
=B(\theta,F)-\tfrac13B(\theta,\theta^2).
\]
Então
\[
\boxed{d\,\operatorname{CS}_B=B(F,F).}                     \tag{6}
\]

Esta identidade pode ser verificada no próprio complexo: \(d\theta=F-\theta^2\), \(dp=-\theta p\) implicam \(dF=F\theta-\theta F\). Expandir dCS com Leibniz graduado e invariância de B cancela as parcelas com θ. É também a parcela de ghost da identidade de [transgressão076](<C:/IALD/Central de Patentes/Chatgpt/TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md>), mas aqui θ é o ghost da referência082 e \(F=Kpp^\flat\); não foi substituído pela curvatura dinâmica.

Para o traço,
\[
\operatorname{tr}(F^2)=K^2p^ap_bp^bp_a=0
\]
porque \(p_bp^b=0\). Para a normalização de Euler de(5),
\[
B_E(F,F)=\frac{K^2}{24}\varepsilon_{abcd}p^ap^bp^cp^d
=K^2\nu(p).
\]
Logo
\[
\boxed{d\operatorname{CS}_{\rm tr}=0,\qquad
d\operatorname{CS}_E=K^2\nu.}                              \tag{7}
\]

Se f pertence a \(\mathscr N^{\mathfrak g}\), então df=0 e pode multiplicar(7). Um escalar somente h-invariante não basta: para ele df pode ter a parcela \(p^a\rho_{P_a}f\). Aplicar(7) a um f arbitrário omitiria exatamente essa parcela.

## 4. Forma normal finita para qualquer primitiva de grau3

**Lema.** Seja \(Q\in C_{\rm nat}^3\) de jatos finitos, e suponha que dQ seja inteiramente horizontal de grau4. Existem \(f_{\rm tr},f_E\in\mathscr N^{\mathfrak g}\), uma corrente horizontal \(q_V\in C^{3,0}\) e uma cocadeia finita \(R\in C_{\rm nat}^2\) tais que
\[
\boxed{Q=q_V+f_{\rm tr}\operatorname{CS}_{\rm tr}
                  +f_E\operatorname{CS}_E+dR.}            \tag{8}
\]

**Prova.** Decomponha \(Q=Q_{0,3}+Q_{1,2}+Q_{2,1}+Q_{3,0}\).

1. A equação de bigrau(0,4) diz \(d_0Q_{0,3}=0\). Por(3–4),
   \(Q_{0,3}=f_{\rm tr}\tau_{\rm tr}+f_E\tau_E+d_0R_{0,2}\),
   com \(f_i\in\mathscr N^{\mathfrak h}\). Subtraia dR02 de Q; isso não altera dQ e remove somente a parte vertical exata.

2. A equação de bigrau(1,3) é
   \(d_1(\sum_i f_i\tau_i)+d_0Q_{1,2}=0\).
   Sua classe vertical é
   \(\sum_i(d_{\rm rel}f_i)\otimes[\tau_i]=0\).
   A independência das duas classes de Cartan força \(d_{\rm rel}f_i=0\).
   Como fi já é h-invariante, isso equivale a \(\rho_{P_a}f_i=0\) para todos os a, isto é, \(f_i\in\mathscr N^{\mathfrak g}\).
   Não se supôs finitude sob g para chegar a essa condição.

3. Subtraia agora \(\sum_i f_i\operatorname{CS}_i\). Por(7), o diferencial da diferença continua inteiramente horizontal, e sua componente(0,3) é zero. A equação(1,3) restante diz \(d_0Q_{1,2}=0\).
   Como \(H^2(\mathfrak h,\mathscr N\otimes V_0^*)=0\), na versão invariante(3), escolha \(R_{1,1}\) finita com \(Q_{1,2}=d_0R_{1,1}\) e subtraia dR11.

4. Restam Q21+Q30. A equação(2,2) diz \(d_0Q_{2,1}=0\).
   Por \(H^1(\mathfrak h,\mathscr N\otimes\Lambda^2V_0^*)=0\), escolha R20 finita com \(Q_{2,1}=d_0R_{2,0}\) e subtraia dR20. Resta apenas Q30. A equação(3,1) força \(d_0Q_{3,0}=0\), logo é uma cocadeia horizontal h-invariante.

Toda subtração foi uma fronteira d de grau2, e seus termos de curvatura foram conservados. A soma das três primitivas verticais é o R de(8). Elas usam somente cortes h-finitos; os d aplicados podem elevar a ordem finitamente. Isso conclui a prova.

O lema preserva, e não descarta, a classe Cartan de traço: o termo \(f_{\rm tr}\operatorname{CS}_{\rm tr}\) é fechado e pode permanecer em Q. Não se alega unicidade da forma normal, nem se classifica H³ inteiro por(8).

## 5. Critério horizontal exato e o alvo J_W

Em dimensão quatro, o volume identifica qualquer cocadeia horizontal h-invariante de grau3 com um vetor \(V\in(\mathscr N\otimes V_0)^{\mathfrak h}\):
\[
q_V=\frac1{3!}\varepsilon_{abcd}V^ap^bp^cp^d.
\]
A [identidade082](<C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910/CLASSE_CE_DO_RESIDUO_E_CORRENTE_GRADIENTE.md>) dá, pontualmente,
\[
dq_V=(\operatorname{div}_{0}V)\nu(p).                       \tag{9}
\]
Não há quociente por derivadas totais escondido; a divergência é a imagem concreta do diferencial.

Aplicar d a(8) fornece
\[
dQ=(\operatorname{div}_{0}V+K^2f_E)\nu .
\]
Isso prova a necessidade em(A). Reciprocamente, se a igualdade em(A) vale, a cocadeia finita \(Q=q_V+f_E\operatorname{CS}_E\) satisfaz dQ=J_Wν. Portanto(A) é necessária e suficiente NO complexo indicado.

O anel é fixado e K é real não nulo; sem restrições suplementares de peso, \(K^2\mathscr N^{\mathfrak g}=\mathscr N^{\mathfrak g}\). Mantemos K² explícito para não transportar essa simplificação a um anel restrito em K variável. Se a engenharia da primitiva for zero, o setor de f e de V também deve respeitar essa engenharia; uma igualdade no módulo maior não constitui automaticamente um contratermo Q2 admissível.

Duas ressalvas evitam tornar(A) tautológica. Primeiro, J_W ser escalar de Lorentz não prova \(J_W\in\mathscr N^{\mathfrak g}\). Segundo, o elemento unidade de Rher não pertence automaticamente ao módulo quadrático \(\mathscr N\). Um f admissível continua sendo uma classe quadrática de Weyl/jatos, com todas as condições de transvecção. Não se acrescentou um coeficiente constante de grau zero ao problema de duas pernas.

Ainda não calculamos \(\mathscr N^{\mathfrak g}\), nem mostramos que é zero. Também não construímos V que resolva(A). A corrente gradiente082 fornece apenas \(\operatorname{div}\nabla J_W=\Box_0J_W\); a redução não identifica esse resultado com J_W.

## 6. Página de termos e o diferencial de curvatura

A mesma prova pode ser organizada pela filtração decrescente no número de p. Ela tem comprimento cinco, independentemente da ordem dos jatos. A primeira página e o diferencial horizontal são
\[
E_1^{r,q}=B^r\otimes H^q(\mathfrak h,\mathbb R),\qquad
B^r=(\mathscr N\otimes\Lambda^rV_0^*)^{\mathfrak h},\quad
d_{E_1}=d_{\rm rel}\otimes1 .
\]
Em B, \(d_{\rm rel}=d_1\) e \(d_{\rm rel}^2=0\) por(2).
Assim
\[
E_2^{r,q}=H^r(B,d_{\rm rel})\otimes H^q(\mathfrak h,\mathbb R).
\]

| Grau vertical q | r=0,1,2,3,4 |
|---|---|
| 6 | \(H^r(B)\) |
| 3 | \(H^r(B)\otimes\mathbb R^2\), duas Cartan |
| 0 | \(H^r(B)\) |
| demais | 0 |

Os diferenciais de páginas2 e3 são zero por seus bidegraus \((j,1-j)\) e pelas linhas vazias. O único diferencial que pode atingir o alvo \((4,0)\) é
\[
d_4:E_4^{0,3}=\mathscr N^{\mathfrak g}\otimes\mathbb R^2
               \longrightarrow E_4^{4,0}=H^4(B).
\]
Sua realização por(7) é
\[
d_4(f\tau_{\rm tr})=0,\qquad
d_4(f\tau_E)=[K^2f\nu].                                   \tag{10}
\]
Há ainda um canal de curvatura possível \((0,6)\to(4,3)\); não se o elimina por chamar todas as classes de Cartan permanentes. Não há páginas com novo diferencial depois da4, porque r nunca excede4.

A filtração é FINITA no complexo de cochains; essa organização não usa um limite inverso de cortes de jatos nem presume Mittag–Leffler. A forma normal do §4 dá diretamente a afirmação sobre o alvo, sem depender de uma extensão oculta na passagem da página limite à cohomologia.

Este é o papel legítimo do complexo horizontal RELATIVO nesta investigação: ele aparece como a linha q=0 e na página seguinte, enquanto as classes verticais e sua transgressão continuam contabilizadas. Não se substituiu o CE invariante inteiro pelo relativo.

## 7. Próximo contrato e alcance

A [transferência080](<C:/IALD/Central de Patentes/Chatgpt/TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md>) e a identificação082 tornam a questão do próximo levantamento equivalente a(A). O trabalho remanescente foi reduzido a dois problemas do MESMO módulo quadrático com relações:

- determinar os elementos invariantes sob todas as transvecções e isotropia;
- decidir se J_W, modulo o canal de Euler desses elementos, é a divergência de um vetor natural quadrático de ordem finita.

Essa é uma redução demonstrada do número e do tipo de ghosts na busca, não uma resposta a esses dois problemas. Não há hipótese de local finitude sob g, aplicação de Whitehead a g, truncamento arbitrário de derivadas, troca para o fundo φ=id ou conclusão de QME/UV. A etapa083 não é consumida nem incorporada; esta nota084 também não deve ser incluída retroativamente em sua entrega.

[REAL — custódia] O manifesto registra as cinco fontes locais medidas antes/depois e esta fonte nova. A única importação cohomológica é a finito-dimensional indicada no §2. As identidades de curvatura e a eliminação em graus(0,3) a(3,0) são demonstrações escritas aqui. Não houve cálculo CAS ou Lean. Um controle breve do desenho pelo agente prepare_integration_83 foi recebido antes da escrita; não é apresentado como revisão integral desta nota, que permanece pendente.
