# O subsetor puro h*C⁴: fatoração natural por Bianchi e efeito nulo no levantamento

10/09/2026. Arco079. [DERIVED — prova escrita nova, aguardando revisão independente]. Autor: /root/selected_geometry_design. Nenhum um.py, CAS ou Lean executado. Fontes anteriores somente lidas; esta nota não integra nem altera078.

**Resultado.** No complexo BV métrico mínimo do fundo Einstein com mapa sigma constante, todo b5 puramente linear em jatos do antifield métrico e quártico nos jatos do ghost, com s0b5=0 universalmente, é s0-exato na mesma categoria natural de ordem finita. Logo sua classe em C5 e sua contribuição à aplicação δ de levantamento são zero. A prova constrói o operador de fatoração das identidades de Noether pelo símbolo de Einstein; não toma a exatidão KT como hipótese.

Este resultado trata somente b4=Q=0 na [nota de liberdade079](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md>). Uma correção antifield acoplada a termos u²C³ ou uC³ pode não ser s0-fechada separadamente; não é eliminada pelo presente teorema.

## 1. Categoria e normalizações

B0=(g0,φ0) é inerte, g0 Lorentziana suave não degenerada, Einstein com Λ fixada, e φ0 constante. A curvatura constante K>0 do teste079 satisfaz essas hipóteses. A prova métrica abaixo requer apenas a condição Einstein, que assegura a identidade linear de Bianchi exata, não a inexistência de campos de Killing.

Os coeficientes são naturais sob mudanças simultâneas de coordenadas, suaves ou analíticos nos parâmetros conforme a categoria de entrada, com as contrações por g0, g0⁻¹ e sua densidade já permitidas. São polinômios finitos nos jatos de ghosts e usam finitamente muitos jatos de referência em cada expressão. Não há inversos de curvatura, inversos de derivadas, fontes externas de ghost positivo ou quociente por divergências. A categoria deve ser fechada sob somas, contrações e derivadas covariantes finitas, como na nota079; uma eventual classe de normalizações quânticas com inserções e contatos não é identificada automaticamente com essa categoria de cochains.

Escreva p_can^{ab}=h*^{ab} para o antifield densitizado da métrica covariante e q_can,b=C*_b. O [sinal KT077](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>) fornece
s0 p_can=H_can h e s0 q_can=R0† p_can.
Aqui (R0C)_ab=∇aC_b+∇bC_a. O adjunto variacional é
(R0†p_can)_b=−2 g0_bc ∇a p_can^{ac},
com a conexão da densidade incluída.

Se v0=√|det g0|, introduza apenas para a prova
\[
 p_{ab}=v_0^{-1}g_{0,ac}g_{0,bd}p_{\rm can}^{cd},
 \qquad q_b=-\frac{q_{{\rm can},b}}{2v_0}.
 \tag{1}
\]
São mudanças invertíveis naturais, não novos campos. Como os fatores de referência são s-inertes e paralelos,
\[
 s_0p=Hh,\qquad s_0q=\mathcal Dp,\qquad
 (\mathcal Dp)_b=\nabla^a p_{ab},\qquad \mathcal D H=0.
 \tag{2}
\]
Para a ação071, H=(2κ)⁻¹δ(G+Λg) com índices baixos: o fundo resolve a EOM, portanto a variação dos fatores de densidade/elevação não acrescenta termos. A constante não nula não muda o núcleo do símbolo. O operador H é formalmente autoadjunto na identificação da fibra e possui o símbolo principal de Einstein, a menos desse fator.

A última igualdade em (2) vem da variação da identidade não linear ∇^a(G+Λg)_ab=0 no fundo Einstein. Termos que variam a conexão multiplicam a EOM de fundo e desaparecem. Nenhuma escolha de gauge foi feita.

## 2. A condição de fechamento é uma identidade de operadores

Um b5 do subsetor pode ser escrito
\[
 b_5=P_C[p]=\sum_{|I|\le r} A^{I,ab}(jC,jB_0)\,
                 \nabla_{(I)}p_{ab}.
 \tag{3}
\]
Os coeficientes A são pares, de ghost4 e valência quatro, sem campos h,ξ nem antifields. O operador P_C é um operador DIFERENCIAL no argumento p; os jatos de C ficam nos coeficientes à esquerda. Usam-se derivadas covariantes simetrizadas; comutadores de curvatura são recolhidos nas ordens inferiores.

Como s0 anula todos os coeficientes e comuta com a conexão de fundo,
\[
 \boxed{s_0b_5=0\quad\Longleftrightarrow\quad P_C H=0.}
 \tag{4}
\]
A igualdade vale sobre jatos livres de h e C, não somente sobre soluções de Hh=0 nem sobre ghosts de Killing. Ela não é uma igualdade integrada. Em particular, não se troca P_C H por seu adjunto por integração por partes.

## 3. Lema algébrico explícito para o símbolo de Einstein

Seja n≥3 e g uma forma não degenerada. Para uma covariável real p_a, ponha
q(p)=g^{ab}p_ap_b,
v_b=p^a A_ab e a=g^{ab}A_ab.
Um representante do símbolo de Einstein é
\[
 2\mathsf E_p(A)_{ab}
 =p_av_b+p_bv_a-qA_{ab}-p_ap_b a
       -g_{ab}(p^cv_c-qa).
 \tag{5}
\]
O fator global e a convenção de Fourier não afetam seu núcleo.

**Lema.** Se A_ab(p) é um tensor simétrico cujas componentes são polinômios homogêneos de grau r≥0 e \(\mathsf E_p(A(p))=0\) como identidade polinomial, então A=0 para r=0. Para r≥1 existe um fator polinomial natural B_b(p), homogêneo de grau r−1, com
\[
 A_{ab}=p_aB_b+p_bB_a.
 \tag{6}
\]
Ele é dado explicitamente abaixo, sem dividir por q(p).

**Prova.** O traço de (5) dá
\[
 (2-n)(p^av_a-qa)=0.
\]
Para q≠0, a equação restante fornece
\[
 A_{ab}=p_a\frac{v_b-p_ba/2}{q}
        +p_b\frac{v_a-p_aa/2}{q}.
 \tag{7}
\]
A fração é usada apenas para inferir uma identidade polinomial no aberto q≠0, não para construir um operador inverso.

Defina a dupla curl algébrica
\[
 \mathscr C_{abcd}
 =p_ap_cA_{bd}-p_bp_cA_{ad}
   -p_ap_dA_{bc}+p_bp_dA_{ac}.
 \tag{8}
\]
Substituir (7) dá \(\mathscr C=0\) no aberto q≠0. Este aberto é denso, pois q é uma forma quadrática não nula. Logo o polinômio \(\mathscr C\) é identicamente zero, inclusive no cone nulo.

Ponha N=n+r e escreva \(\partial_p^a=\partial/\partial p_a\),
\[
 D_b=\partial_p^a A_{ab},\qquad
 S=\partial_p^a\partial_p^b A_{ab}.
\]
A regra de Leibniz e a homogeneidade dão a identidade
\[
 \partial_p^a\partial_p^c\mathscr C_{abcd}
 =N(N-1)A_{bd}
  -(N-1)(p_bD_d+p_dD_b)+p_bp_dS.
 \tag{9}
\]
Uma forma de conferir os fatores é separar os quatro termos de (8): o primeiro fornece N(N+1)A; cada um dos dois negativos fornece −(N+1)(A+pD); o último fornece 2A+2p_bD_d+2p_dD_b+p_bp_dS.

Como (9) é zero,
\[
 \boxed{B_b=
 \frac1N\left(D_b-\frac{p_bS}{2(N-1)}\right)}
 \tag{10}
\]
satisfaz (6). Os denominadores N e N−1 são inteiros estritamente positivos. Para r=0, D=S=0 e (9) força A=0. Para r=1, S=0, como deve ocorrer. A prova termina. ∎

A contração entre ∂/∂p_a e um índice covariante de A é intrínseca no fibrado cotangente. A fórmula é GL-natural; a métrica entrou apenas na identificação do núcleo em (5). Não há média sobre o grupo Lorentz, denominador p² na saída, série infinita ou escolha de vetor temporal.

Se os coeficientes contêm um polinômio Grassmann, aplica-se o argumento a cada monômio independente. A fórmula (10) é linear nos coeficientes e por isso os recombina sem mudança. Dependência suave/analítica em parâmetros é preservada pelas operações explícitas.

## 4. Fatoração diferencial finita e natural

**Teorema de compatibilidade neste alcance.** Se P é um operador diferencial finito no argumento tensor simétrico, com coeficientes da categoria da seção1, e PH=0 universalmente, então existe um operador diferencial finito B na mesma categoria tal que
\[
 \boxed{P=B\mathcal D.}
 \tag{11}
\]
Se P tem ordem r≥1 no argumento, B pode ser escolhido com ordem no máximo r−1. Se r=0, P=0.

**Prova construtiva.** Ponha P em ordem covariante simetrizada. Seu símbolo superior σ_r(P) é um polinômio homogêneo de grau r, com um índice dual da fibra de tensores simétricos. A igualdade PH=0 implica
\[
 \sigma_r(P)\,\sigma_2(H)=0.
\]
Pela autoadjunticidade do símbolo de Einstein, identificar o índice dual com g transforma essa igualdade no núcleo do lema da seção3. A fórmula (10) produz um covetor B_b(p) polinomial. Como
\(A^{ab}p_{ab}^{\rm arg}=(p^aB^b+p^bB^a)p_{ab}^{\rm arg}
=2B^b p^a p_{ab}^{\rm arg}\),
o fator para o símbolo da DIVERGÊNCIA é \(2B^b\), e não B^b.

Quantize esse símbolo \(2B\) substituindo os monômios em p por derivadas covariantes simetrizadas de fundo, com todos os coeficientes à esquerda. Chame o operador obtido B_(r−1). Então
\[
 P'=P-B_{(r-1)}\mathcal D
\]
tem ordem no máximo r−1 e ainda satisfaz P'H=0 por (2). A composição contém os termos inferiores de conexão e curvatura; eles não são apagados e entram no próximo P'.

Repita. A ordem do argumento cai estritamente, sem exigir cota sobre a ordem inicial dos jatos do ghost. Ao chegar à ordem zero, o lema força o resto a zero. Somar os operadores produzidos dá (11). Há no máximo r etapas.

Cada passo usa apenas contrações, derivadas covariantes, soma, a divisão pelos inteiros de (10) e as identificações invertíveis já autorizadas em (1). A construção é natural; não escolhe primitivas coordenadas para depois supor que elas possam ser covariantizadas. Derivadas de coeficientes de referência e termos de curvatura só produzem um número finito de jatos em cada estágio. Os coeficientes de ghost permanecem homogêneos de grau quatro. ∎

Este argumento não depende de H ter inverso, nem afirma que todo tensor divergenceless global seja Hh. A conclusão é a FATORAÇÃO DE IDENTIDADES LOCAIS DE OPERADORES. A terminologia de operador de compatibilidade universal é a de [Khavkine, seção2](https://arxiv.org/pdf/1805.03751). A fonte trata também o complexo do operador Killing; esse teorema não foi confundido com uma prova pronta para H. A fatoração particular de (11) foi demonstrada aqui pelo símbolo e pela indução finita.

## 5. Primitiva em C5 e correção em C6

Aplique (11) a P_C de (3). Defina
\[
 \chi_5=B_C[q].
 \tag{12}
\]
B_C tem coeficientes C⁴; q é par de ghost−2. Logo χ5 é par, tem ghost2, valência cinco e espécie C*C⁴, podendo conter jatos. Como s0B_C=0,
\[
 \boxed{s_0\chi_5=B_C[\mathcal Dp]=P_C[p]=b_5.}
 \tag{13}
\]
Portanto b5 é s0-exato. Sua classe em H³(C5) é zero: em C5, o diferencial completo de χ5 coincide com s0χ5, pois os demais termos têm valência maior.

A nilpotência fornece s0s1+s1s0=0, de modo que
\[
 s_1b_5=-s_0(s_1\chi_5).
 \tag{14}
\]
Assim a classe de s1b5 no grupo receptor da aplicação de conexão δ é zero. Para a evolução do representante b5 sozinho, a correção
\[
 \boxed{b_6=s_1\chi_5}
 \tag{15}
\]
satisfaz s0b6+s1b5=0. O sinal é positivo em (15).

É importante distinguir as espécies. A PRIMITIVA χ5 usa C*C⁴ em ghost2. A CORREÇÃO b6=s1χ5 usa tanto h*hC⁴, proveniente do termo de s1C* linear no antifield físico e no campo, quanto C*C⁵, proveniente de sua parte de gauge e da variação dos coeficientes. Não foi demonstrado que o último tipo sozinho bastasse. Essa distinção evita perder justamente os termos de antifields físicos do sistema079.

No teste TT078,
\[
 \operatorname{ev}(s_1b_5)
 =\operatorname{ev}\bigl(P_C[E_{g,2}[h,h]]\bigr)
 =-\operatorname{ev}\bigl(s_0s_1\chi_5\bigr)=0.
 \tag{16}
\]
A primeira igualdade inclui todos os jatos de E_g,2 emparelhados com jatos de h*. A última usa que a avaliação anula s0, não que E_g,2 seja zero ponto a ponto. Ela vale para candidatos que satisfaçam a condição UNIVERSAL (4).

**Corolário sem jatos do antifield.** Se b5 não deriva h*, então P_C tem ordem zero e o teorema fornece P_C=0. Portanto esse subcaso fechado é a expressão zero, mesmo que seus coeficientes usem jatos altos do ghost.

## 6. Matéria e campos de Killing da referência

No fundo φ0 constante, a Hessiana quadrática Einstein–sigma é bloco diagonal: o stress matéria começa em ordem dois em ξ, e o bloco sigma é um operador de onda com matriz de fibra invertível, pois c_sigma≠0 e a métrica alvo é positiva. Um b5 puro em antifields físicos gerais satisfaz separadamente P_g H_g=0 e P_sigma H_sigma=0, pela independência dos jatos de h e ξ.

O símbolo de H_sigma é uma matriz invertível multiplicada por p². Se P_sigma H_sigma=0, seu símbolo superior é zero: após expansão em monômios Grassmann, um polinômio real multiplicado pelo polinômio não nulo p² só pode ser zero. Indução na ordem dá P_sigma=0. O setor restante é o métrico já tratado. Assim, neste fundo, a conclusão também cobre o subsetor puro u*C⁴ do modelo completo, sem supor uma identidade adicional sigma.

A presença dos dez campos de Killing locais da referência de curvatura constante não contradiz o argumento. Há três objetos distintos:

- soluções k(x) da equação R0k=0;
- identidades diferenciais PH0=0 em argumentos ARBITRÁRIOS;
- cohomologia relativa módulo divergências e cargas globais.

Uma solução Killing não define um operador de redutibilidade sobre funções arbitrárias: R0(fk)=2k_(a ∂b)f em geral é não zero. Mais geralmente, se um operador diferencial finito Z satisfizesse R0Z=0 identicamente em um argumento livre, a injetividade do símbolo v↦p_av_b+p_bv_a forçaria o símbolo superior de Z a zero; indução daria Z=0. Isso não diz que ker R0 sobre seções seja zero.

Também não usamos integração por partes. Para um Killing k, a contração k·D p pode virar divergência após usar a equação de Killing; ela não é a zeroforma identicamente nula exigida por (4). As classes relativas ligadas a Killing não são descartadas pelo presente teorema.

## 7. Regularidade e alcance exato

A hipótese técnica efetivamente usada é a categoria da seção1: operadores finitos e naturais, coeficientes herdados fechados sob as operações explícitas e métrica de fundo Einstein não degenerada. Não foi importada a ausência universal de Killing da nota071, que não vale após especializar ao fundo com simetrias. Não se pressupôs aciclicidade KT, exatidão de um complexo de soluções ou sobrejetividade global de um operador hiperbólico.

As fórmulas preservam finitude elemento a elemento, ghost, paridade e valência. A passagem de p com r derivadas para q com r−1 compensa os pesos de engenharia usuais [p]=4 e [q]=5. Comutadores trocam duas derivadas por curvatura de peso dois. Essa observação não fornece automaticamente um contratermo admissível em cada aridade/loop de Q2, com todos os contatos e normalizações; o resultado é na categoria de cochains079.

Não há avaliação numérica de uma série de Rees nem limite de uma sequência infinita de operadores. Para cada b5 há uma ordem r finita; o algoritmo termina. Uma família de b5 com ordens crescentes não foi substituída por uma única base finita.

## 8. O que fica efetivamente pago

[DERIVED] Sob b4=Q=0, uma espécie pura h*C⁴ admissível só define ciclo se for uma identidade de Noether fatorável pelo operador de Bianchi; a fatoração natural finita foi aqui construída. O ciclo é s0-exato, a aplicação de conexão δ é zero nesse subsetor e a avaliação de seu s1 também é zero no teste078. A extensão ao bloco sigma constante foi demonstrada acima.

[OPEN] No sistema inteiro079, (9) permite s0b5 cancelar s1b4, e também permite que a contribuição do antifield cancele s0 da parte Q. Nesses casos o termo puro em antifields não é um ciclo isolado e a hipótese (4) não se aplica. Não eliminamos esses termos mistos, não decidimos −[A6]∈δ(K), nem demonstramos cancelamento ou obstrução de toda a linha cúbica.

Não se concluem QME, H³/H⁴ completos, lim¹, Mittag–Leffler, UV ou confirmação de gravidade quântica. A identidade de Noether aqui demonstrada permanece uma prova escrita até eventual formalização independente.
