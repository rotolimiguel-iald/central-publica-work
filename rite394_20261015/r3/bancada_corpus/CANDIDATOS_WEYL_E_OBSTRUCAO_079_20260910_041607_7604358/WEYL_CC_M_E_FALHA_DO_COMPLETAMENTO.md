# Dois candidatos de Weyl: obstrução já na equação de completamento de valência cinco

10/09/2026, investigação079. [DERIVED — demonstração escrita própria, sem CAS ou Lean]. A nota não altera as fontes077–079. Os pins e a preservação dos bytes têm estatuto [REAL — documental] no manifesto. Nenhum um.py foi executado ou importado.

**Resultado.** No teste permitido de curvatura constante com matéria sigma constante, os candidatos naturais P=W[1]CCm e seu dual são s0-fechados, mas s1P tem classe não nula para s0. Portanto nenhum operador quadrático Q, nem qualquer termo com antifields u*R, pode completá-los pela equação (9) da nota079. A mesma conclusão vale para toda combinação não nula desses dois candidatos com coeficientes escalares herdados do mesmo fundo. Não se afirma que essa família esgote os candidatos lineares em h.

O certificado usa uma solução Einstein linearizada já construída078 e quatro outros campos de Killing, escolhidos por seus dados no ponto. Dois têm valor não nulo e dois têm somente primeiro jato não nulo. Isso detecta um termo de tipo W[1]C²m². Este teste é diferente daquele que detecta A6, de tipo W[1]²C⁴: aqui C(p)³=0, de modo que A6 se anula no próprio funcional. Os dois certificados não são intercambiáveis.

## 1. Contrato, valência e sinais

Use a [redução e o sistema local079](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md>), com apresentação métrica mínima, sem fontes centrais externas, B0=(g0,φ0) inerte, Ric(g0)=3K g0, K>0, e φ0 constante. Os argumentos dinâmicos u=(h,ξ) permanecem off-shell. Uma expressão tem ordem finita de jatos em cada coeficiente; nenhum corte universal adicional de derivadas é imposto.

A expansão por valência é s=s0+t s1+… e usa a [correção KT077](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>):

\[
s_0u=R_0C,\quad s_0C=0,\quad
s_0u^*=+H_0u,\quad s_0C^*=R_0^\dagger u^*;
\qquad s_1h=\mathcal L_Ch,\quad s_1C=C\cdot\bar\nabla C.
\tag{1}
\]

A última expressão coincide com C·∂C porque a conexão de fundo é sem torção. As transformações prolongam-se a todos os jatos, e sB0=0. H0 é a Hessiana física sem gauge fixing.

Denote por W=W[1][h] o Weyl linearizado, com índices covariantes baixados por g0. Defina

\[
m_{ab}=\bar\nabla_{[a}C_{b]},\qquad
P=W_{abcd}C^aC^b m^{cd}.
\tag{2}
\]

Os colchetes contêm o fator 1/2. Todos os produtos de ghosts são Grassmann. P tem ghost3 e valência4: um fator h, dois valores de C e um primeiro jato de C.

Escolha a orientação e o dual na SEGUNDA dupla:

\[
(W^\star)_{abcd}=\frac12W_{abef}\,\varepsilon^{ef}{}_{cd},
\qquad
P^\star=(W^\star)_{abcd}C^aC^b m^{cd}.
\tag{3}
\]

Para o tensor de Weyl em quatro dimensões, dualizar na segunda dupla preserva as simetrias de curvatura, inclusive a troca das duplas. Aqui é suficiente a identidade de troca W*_{abcd}=W*_{cdab}. Ela segue da decomposição do operador de curvatura em Λ²: a parte que anticomuta com o Hodge é exatamente a Ricci sem traço, ausente no Weyl. Alternativamente, a contração de dois epsilons na diferença das duas expressões a reduz às contrações W^a{}_{bad}=0. O dual usado não é um novo campo nem uma escolha de autodualidade complexa. A assinatura (+---) dá *²=−1 em duas-formas, mas não é necessário diagonalizar esse operador.

Como W(g0)=0, a naturalidade fornece W[1][Lie_Cg0]=Lie_CW(g0)=0 para todo C, sem impor Killing. Logo

\[
s_0W=0,\qquad s_0P=s_0P^\star=0.
\tag{4}
\]

Isso verifica a condição (8) de079. A condição seguinte, permitindo todas as espécies da valência cinco, seria

\[
Q[u,R_0C;C^3]+\langle H_0u,R(C^4)\rangle+s_1P=0.
\tag{5}
\]

O pareamento inclui jatos e é pontual; não se trabalha módulo divergências. O sinal +H0 em (1) é o corrigido. A conclusão abaixo permite Q e R de todas as ordens FINITAS admitidas, e não apenas ansätze sem derivadas.

## 2. Avaliação que anula todas as fronteiras de s0

O [certificado078](<C:/IALD/Central de Patentes/Chatgpt/RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md>) demonstra o seguinte procedimento, que reaplico com outros Killing. Escolha uma solução H0u=0 em uma vizinhança e campos vA de Killing de g0 que preservem φ0. Coloque

\[
u\mapsto u_{\rm sol},\quad
C\mapsto\sum_{A=0}^3\theta^A v_A,\quad
u^*\mapsto0,\quad C^*\mapsto0,
\tag{6}
\]

prolongue aos jatos e avalie num ponto p. A álgebra de chegada é Λ(θ0,…,θ3) com diferencial zero. Todos os termos de (1), inclusive seus prolongamentos, avaliam em zero. Portanto

\[
\operatorname{ev}_p(s_0F)=0
\tag{7}
\]

para qualquer expressão local regular finita F, incluindo antifields. Não é necessário que os quatro vA fechem uma subálgebra. Esta é uma avaliação do complexo LINEAR s0; s1 não é definido como diferencial na álgebra de chegada.

Em particular, uma avaliação não nula de s1P contradiz (5), pois Q[u,R0C] e todos os termos H0u emparelhados com R se anulam. Isso inclui qualquer tentativa de usar jatos de u* para absorver a obstrução. A solução precisa existir na vizinhança para anular todos os jatos das equações, não somente seus valores em p.

## 3. Identidade matricial para a variação

Nesta seção, imponha Killing apenas DEPOIS de aplicar as transformações indicadas. Escreva

\[
p^a=C^a,\qquad A^a{}_b=\bar\nabla_bC^a,
\qquad U^a{}_b=\frac12W^a{}_{bcd}p^cp^d.
\tag{8}
\]

Em um campo de Killing, A é antissimétrico para g0 e A_ab=−m_ab. Assim, pela troca das duplas de W,

\[
\boxed{P=2\operatorname{tr}(AU).}
\tag{9}
\]

Para conferir o sinal: tr(AU)=m^{ab}W_abcd p^cp^d/2. Trocar as duplas dá exatamente (2)/2; mover m através dos dois p não muda o sinal. Portanto A=−m com um índice elevado NÃO significa P=−2tr(AU). Os índices do traço efetuam a segunda troca de sinal. O [dicionário Cartan077](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/DICIONARIO_CARTAN_DO_RECIBO_077.md>) usa essa mesma matriz A sob o nome M. Se alguém definir um candidato diretamente com M^{cd}=−m^{cd}, o candidato é −P e todos os valores abaixo recebem o sinal global oposto; a obstrução é idêntica.

A integrabilidade de Killing no espaço forma e s1C=C·∇C dão

\[
s_1p=-Ap,\qquad s_1A=-A^2+\Omega_0,
\qquad \Omega_0=Kpp^\flat.
\tag{10}
\]

Este é também o dicionário CE077. O sinal −A² pode ser conferido antes de usar curvatura: ∇b(Ce∇eCa) contém (∇bCe)(∇eCa)=A^e_b A^a_e=−(A²)^a_b. O termo com ∇∇C dá Ω0. Não se trata A como uma matriz par.

Para cada vA Killing, a equivariância do operador linear W[1] pelas isometrias de g0 implica W[1][Lie_vA h]=Lie_vA W[1][h]. Isso fixa a variação do tensor mesmo quando h é arbitrário. Levantar seus índices com g0 é compatível com Lie_vA porque Lie_vAg0=0. Ao incluir a variação dos dois p em U, os termos de Lie nos dois índices da forma cancelam exatamente. Restam

\[
s_1U=UA-AU+V,
\qquad V^a{}_b=\frac12p^e\bar\nabla_eW^a{}_{bcd}p^cp^d.
\tag{11}
\]

Exemplo do cancelamento: o termo +(∇cCe)W_abed p^cp^d/2 em Lie_CW é cancelado pelo termo W_abcd(s1pc)pd/2 com s1pc=−A^c_epe. O segundo índice segue pela regra s(pcpd)=(spc)pd−pc(spd). A ordenação ímpar não pode ser omitida.

Como A é ímpar e U é par, (9–11) e a ciclicidade GRADUADA do traço dão

\[
\begin{aligned}
s_1P
&=2\operatorname{tr}\bigl[(s_1A)U-A(s_1U)\bigr]\\
&=2\operatorname{tr}\bigl(\Omega_0U+A^2U-AV\bigr).
\end{aligned}
\tag{12}
\]

De fato, tr(AUA)=−tr(A²U), pois ao mover o primeiro A através de UA atravessa-se um fator ímpar. Sem esse sinal, o termo que detecta a obstrução seria perdido.

As mesmas fórmulas valem para W* e U*=W*CC/2: o Hodge de fundo é preservado pelos Killing locais que preservam a orientação. Não se exige aqui uma identidade diferencial adicional de W*. Conservamos explicitamente V, em vez de o eliminar por uma Bianchi não demonstrada na classe em discussão.

## 4. Uma escolha de dados de Killing que elimina os termos de transporte

Fixe uma base ortonormal em p, g0(p)=η=diag(1,−1,−1,−1), com ε0123=+1. Para a<b, defina as matrizes reais

\[
(J_{ab})^a{}_b=\eta_{aa},\qquad
(J_{ab})^b{}_a=-\eta_{bb},
\tag{13}
\]

e demais entradas zero. Escolha os quatro Killing por

\[
\begin{array}{c|cc}
&v_A(p)&\bar\nabla v_A(p)\\\hline
v_0&e_0&0\\
v_1&e_1&0\\
v_2&0&J_{02}\\
v_3&0&J_{12}.
\end{array}
\tag{14}
\]

Esses dados são realizáveis por campos de Killing genuínos: no espaço forma não nulo, o valor de um Killing e sua derivada antissimétrica em um ponto são dez dados independentes. A [construção077 por quádrica](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/S0_KILLING_E_PRIMEIRA_TRANSICAO.md>) demonstra isso usando as matrizes ortogonais do espaço ambiente de dimensão cinco. Decompor o espaço ambiente em RX⊕TpM separa os quatro valores tangentes e as seis matrizes de isotropia. Cada matriz ambiente fornece X↦BX tangente à quádrica. Portanto (14) não especifica primeiros jatos arbitrários sem prolongamento. Como φ0 é constante, todos os quatro campos também preservam a matéria.

Com (6), em p temos

\[
p=\theta^0e_0+\theta^1e_1,
\qquad A=\theta^2J_{02}+\theta^3J_{12}.
\tag{15}
\]

Consequentemente qualquer produto de três valores p é zero. Assim V(p)=0, e Ω0U(p)=0 por conter quatro p. Isso vale sem impor equações diferenciais ao Weyl ou ao seu dual. As equações H0u=0 serão usadas para o mapa (7), não para remover V.

Pelas matrizes (13),

\[
[J_{02},J_{12}]=J_{01},\qquad
\operatorname{tr}(J_{01}^2)=2,\qquad
\operatorname{tr}(J_{01}J_{23})=0.
\tag{16}
\]

Por exemplo, J02 envia e2 em e0 e e0 em e2; J12 envia e2 em −e1 e e1 em e2. Seu comutador envia e0 em e1 e e1 em e0. Como θ2θ3=−θ3θ2,

\[
A^2=\theta^2\theta^3J_{01},\qquad
U=W^a{}_{b01}\theta^0\theta^1.
\tag{17}
\]

Não há fator dois extra em U: o 1/2 em (8) cancela os dois pares 01/10. Das equações (12) e (15–17),

\[
\boxed{\operatorname{ev}_p(s_1P)
=2\operatorname{tr}(J_{01}W_{01}^{\rm end})\,
\theta^0\theta^1\theta^2\theta^3.}
\tag{18}
\]

Aqui (W01^end)^a_b=W^a_b01; a base usada em (14) é apenas um instrumento de avaliação. O candidato (2) continua natural e não contém esse frame como coeficiente extra.

## 5. Valor no mesmo habitante linearizado078

Tome precisamente as coordenadas (τ,x,y,z), z>0 ESPACIAL, assinatura (+---),

\[
g_0=a^2\eta,\qquad a=\ell/z,\qquad K=1/\ell^2,
\qquad \operatorname{Ric}(g_0)=+3g_0/\ell^2.
\tag{19}
\]

O sinal é o da convenção primeira–terceira de Ricci explicitada078. Não se troca z por tempo nem se muda a convenção de curvatura.

Fixe z0=ℓ, de modo que a(p)=1 em p=(0,0,0,z0). Essa é a escolha de um ponto no mesmo fundo, sem alterar o acoplamento Λ. Seja k qualquer real não nulo e

\[
f''-2f'/z+k^2f=0,\qquad f(z_0)=0,\quad f'(z_0)=1.
\tag{20}
\]

A solução analítica local existe, e a perturbação078 é h=a²γ, ξ=0, com

\[
\gamma_{11}=f\cos(k\tau),\quad
\gamma_{22}=-f\cos(k\tau),\quad
\gamma_{12}=\gamma_{21}=f\sin(k\tau),
\tag{21}
\]

demais componentes zero. A nota078 demonstra em toda a vizinhança

\[
\delta\operatorname{Ric}-3K h
=\tfrac12(f''-2f'/z+k^2f)Q(\tau)=0,
\qquad H_0(h,0)=0.
\tag{22}
\]

Assim esse h é adequado ao mapa (6–7), incluindo todos os jatos e o setor sigma. Não se afirma que g0+t h resolva as equações não lineares.

Defina aW=1/(2z0), bW=k/2. As componentes necessárias do Weyl de078 são

\[
W_{0101}=-a_W,\qquad W_{2301}=W_{0123}=b_W.
\tag{23}
\]

Os demais índices do endomorfismo W01 só dão

\[
W_{01}^{\rm end}=-a_WJ_{01}+b_WJ_{23}.
\tag{24}
\]

Em z0=ℓ não há fator de escala entre o Weyl com índices abaixados pelo fundo e a expressão plana usada para seu cálculo conforme. O Weyl de tipo (1,3) já era conformemente invariante; a escolha a(p)=1 elimina até essa possível ambiguidade de índices.

Para o dual na segunda dupla, ε^{23}{}01=+1 na orientação e assinatura fixadas. Logo

\[
(W^\star)_{0101}=W_{0123}=b_W.
\tag{25}
\]

Somente essa componente contribui ao traço com J01. Substituindo (23–25) em (18), obtemos os dois valores separados:

\[
\boxed{\operatorname{ev}_p(s_1P)
=-4a_W\theta^{0123}
=-\frac2{z_0}\theta^{0123}\ne0,}
\tag{26}
\]

\[
\boxed{\operatorname{ev}_p(s_1P^\star)
=+4b_W\theta^{0123}
=+2k\theta^{0123}\ne0.}
\tag{27}
\]

Mover θ2θ3 através de θ0θ1 envolve quatro trocas e conserva o sinal. As fórmulas são contas escritas com matrizes 4×4 e quatro geradores exteriores; não são novas execuções de CAS. Mudar a orientação ou o sinal global do candidato dual muda o sinal indicado, sem mudar a não nulidade.

## 6. Consequência para s1P módulo s0 e para a equação (9)

De s0P=0 e s0s1+s1s0=0 segue que s1P é s0-fechado. As avaliações (26–27) e (7) mostram que não pode ser s0-exato. Portanto

\[
\boxed{[s_1P]\ne0,\qquad[s_1P^\star]\ne0
\quad\text{em }H^4(s_0)_{E=5}.}
\tag{28}
\]

Em particular, P e P* também não são s0-exatos: se P=s0B, então s1P=−s0(s1B), contradizendo (26). Isso é uma conclusão no componente linear de valência quatro e no seu primeiro diferencial, não um cálculo de toda H³(C4).

Se existisse b5=Q[u,u;C³]/2+⟨u*,R(C⁴)⟩ satisfazendo s0b5=−s1P, o lado esquerdo teria avaliação zero. O lado direito não tem. Assim a equação (5), que é a equação (9) de079, NÃO tem solução para esse b4. O resultado permite termos Q e R com derivadas arbitrárias finitas e permite coeficientes coordenados regulares na primitiva; é mais forte do que descartar apenas um ansatz quadrático simples.

Para a combinação Pλμ=λP+μP*, com λ,μ escalares herdados de B0 e dos acoplamentos, s1λ=s1μ=0. Fixe o mesmo fundo, o mesmo valor de φ0 e o mesmo ponto; varie somente a solução h pelo parâmetro k. Então

\[
\operatorname{ev}_{p,k}(s_1P_{\lambda\mu})
=2\left(-\frac\lambda{z_0}+\mu k\right)\theta^{0123}.
\tag{29}
\]

Uma identidade universal em h deve valer tanto para k quanto para −k. Somando e subtraindo, ela exigiria λ=μ=0 no fundo considerado. Portanto nenhum elemento não nulo da extensão escalar dessa família de dois candidatos admite o completamento. Os coeficientes não podem depender do k da solução de teste: k é dado dinâmico do h usado na avaliação, não um coeficiente herdado. Coeficientes que se anulam no teste simplesmente representam o elemento zero da família RESTRITA a esse fundo; a nota não conclui sua nulidade universal em outros fundos.

Adicionar a b4 uma fronteira s0B não remove a conclusão: s1(P+s0B)=s1P−s0s1B tem a mesma classe (28). Adicionar OUTRO ciclo b4 independente pode, em princípio, alterar a classe de obstrução. Não foi demonstrado que todos os ciclos lineares em h e cúbicos em ghosts sejam representados por (2–3).

## 7. Alcance útil e limite do resultado

[DERIVED] A família concreta W[1]CCm e seu dual foi examinada com sinais e normalizações explícitos. Seus membros não nulos passam pela primeira condição de fechamento, mas falham a seguinte, mesmo com antifields permitidos. Isso elimina essa tentativa de completar a transgressão quadrática I_CJ2 da nota079: ela não pode ser reparada usando SOMENTE esses b4, qualquer que seja a escolha posterior de Q/R.

Não se classifica o espaço inteiro de P: ainda podem ocorrer outros operadores em W, seus derivados, jatos de Ricci/EOM, jatos superiores do ghost e combinações entre eles. Tampouco se demonstra que os dois candidatos esgotem o setor de menor ordem numa classe universal; uma afirmação assim exigiria um argumento de invariantes e relações de jatos que não foi fornecido aqui.

[OPEN] Continua aberto se −[A6] pertence à imagem δ(𝒦), onde 𝒦=ker[H³(C5)→H³(C3)]. O presente funcional anula A6 porque só dois valores de C são independentes em p. Sua finalidade é detectar o defeito anterior s1P, não avaliar a obstrução de valência seis. Não substitui a avaliação078, não exclui todas as classes com o mesmo líder CE e não determina Mittag–Leffler, lim¹, anomalia efetiva, QME, carga interagente ou UV.

[REAL — documental] Cinco fontes são lidas e medidas antes/depois pelo script novo do diretório. O manifesto registra igualdade dos pins e verificação dos links locais. Não há reexecução de078, não há CAS/Lean nesta nota e não se atribui aprovação a outro agente ou ao operador. Todo resultado matemático aqui apresentado tem estatuto de demonstração escrita a ser confrontada com suas hipóteses.
