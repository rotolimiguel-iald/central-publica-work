# Equivalência BV formal entre métrica e vielbein

09/09/2026, continuidade 070. [DERIVED — demonstração escrita]. Esta nota paga uma equivalência **perturbativa local** dos complexos, incluindo antifields e cohomologia módulo a derivada horizontal. Não presume equivalência global entre todos os setores topológicos de referenciais, nem calcula a cohomologia de anomalias da matéria.

## 1. Espaço em que a comparação é feita

Fixe uma métrica de fundo não degenerada gbar de assinatura (+---). Em uma carta espaço-temporal escolha um vielbein de fundo ebar, com gbar=ebarᵀη ebar. O fundo é parâmetro externo da apresentação: o diferencial de gauge quântico s não atua sobre ebar. Mudanças simultâneas de coordenadas e referenciais dos dados de fundo serão tratadas na seção 6.

Os campos físicos são a métrica g e o mapa phi para S³. O segundo pode ser descrito em uma carta regular do alvo ou pela expansão formal Exp_phibar(xi) já usada na construção causal. A transformação de variáveis desta nota não altera o mapa ou seus valores; não especializa séries em um parâmetro de curvatura do alvo.

Trabalha-se formalmente perto de e=ebar, ou equivalentemente g=gbar e transformação Lorentz identidade. Os coeficientes de cada grau perturbativo têm jato finito; a transformação abaixo não requer uma soma numérica de flutuações grandes. A expansão é polinomial em jatos diferenciados em cada grau, com coeficientes suaves no alvo e nos dados externos admitidos. A ordem máxima de jato pode depender do grau, como no espaço formal de EFT. A inversa de gbar já é um dado regular permitido.

[INPUT] A ação clássica depende de e exclusivamente através de g=eᵀηe e do volume orientado, e a matéria é Lorentz-escalar. É precisamente a ação Einstein–sigma adotada. Não há férmions, conexão de spin independente ou interação que use um referencial físico adicional. A substituição não provaria a mesma afirmação para qualquer outra ação de vielbein.

## 2. Decomposição explícita sem uma raiz quadrada global assumida

Escreva A=gbar⁻¹(g−gbar). A é gbar-autoadjunto: Aᵀgbar=gbar A. Defina formalmente

\[
S=(I+A)^{1/2}=\sum_{n\ge0}{1/2\choose n}A^n,
\qquad S^{-1}=(I+A)^{-1/2}.
\tag{1}
\]

O coeficiente de cada grau é finito. Como todas as potências pertencem à mesma matriz A, as identidades de séries em uma variável dão S²=I+A e SS⁻¹=I, sem hipótese de comutatividade entre matrizes distintas. Cada potência é gbar-autoadjunta, portanto

\[
S^T\,\bar g\,S=\bar g S^2=g.
\tag{2}
\]

Ponha e_sigma(g)=ebar S. Para um e próximo de ebar e g=eᵀηe, defina

\[
L=e\,[e_\sigma(g)]^{-1}.
\tag{3}
\]

Então LᵀηL=η, L=I+O(e−ebar). A série chi=log L está na álgebra so(1,3), porque a identidade L⁻¹=η⁻¹Lᵀη e log L⁻¹=−log L implicam chiᵀη+ηchi=0. A exponencial formal inverte o logaritmo. Assim

\[
e=\exp(\chi)\,\bar e\,S(g)
\tag{4}
\]

é uma mudança inversível de 16 componentes para 10 componentes métricas e 6 componentes chi. A escolha de componente/orientação é a da identidade formal. Nenhum argumento sobre positividade euclidiana ou decomposição polar global foi usado.

## 3. Ghosts: a variável contrátil é s chi

Adote uma convenção de sinais em que o BRST mínimo nos campos seja

\[
se=\mathcal L_C e+c_L e,\quad
sC^\mu=C^\nu\partial_\nu C^\mu,\quad
sc_L=\mathcal L_C c_L+c_L^2,
\tag{5}
\]

e sphi=Lie_C phi. O ghost c_L é uma matriz ímpar η-antissimétrica. A regra graduada, junto com a identidade de Jacobi, dá s²=0. Em g=eᵀηe, os termos c_L se cancelam e sg=Lie_C g. A ação de s sobre g,phi,C não depende de chi ou c_L.

Defina o novo ghost de seis componentes

\[
\upsilon:=s\chi.
\tag{6}
\]

Sua dependência em c_L é linear, com bloco diagonal inversível. De fato, para uma variação Lorentz pura delta e=c_L e, g e e_sigma(g) ficam fixos, e delta L=c_L L. A derivada esquerda da exponencial dá

\[
\delta L\,L^{-1}
=\frac{e^{\operatorname{ad}\chi}-1}{\operatorname{ad}\chi}\,\delta\chi,
\]
\[
\upsilon
=\frac{\operatorname{ad}\chi}{e^{\operatorname{ad}\chi}-1}\,c_L
 +F(g,\chi,C;\bar e),
\tag{7}
\]

onde F é a parte proveniente de difeomorfismos, local em jatos e linear em C e suas primeiras derivadas. O fator ad chi/(exp(ad chi)−1) tem termo constante I; sua escrita não divide por um campo: é a série formal regular dos números de Bernoulli. Sua inversa é (exp(ad chi)−1)/(ad chi), igualmente regular.

Logo (c_L,C)↔(upsilon,C), para g,chi fixados, é uma mudança triangular local e inversível. A inversão usa no máximo os mesmos primeiros jatos dos campos/ghosts; não requer resolver uma equação diferencial. De s²chi=0 decorre

\[
s\chi=\upsilon,\qquad s\upsilon=0.
\tag{8}
\]

A compensação F não precisa ser omitida nem fixada a zero para obter esses pares. Definir upsilon=c_L, ignorando F, não seria suficiente quando ebar permanece fixo sob o gauge quântico.

## 4. Levantamento canônico aos antifields

A mudança anterior envolve somente campos e ghosts, não antifields. Denote coletivamente as variáveis antigas por q e as novas por Q(q,∂q). Seu levantamento cotangente local pode ser definido pelo gerador

\[
\mathcal F[q,Q^*]=\int Q^A(q,\partial q;\bar e)\,Q_A^*.
\tag{9}
\]

As derivadas variacionais, com as derivadas à esquerda/direita apropriadas à paridade, definem os antifields antigos em função dos novos. Integrar por partes move apenas um número finito de derivadas para Q*. A identidade de cadeia para as variações mostra que a forma canônica BV é preservada, modulo uma derivada horizontal. O levantamento da mudança inversa é a inversa desse levantamento, portanto ele não acrescenta uma hipótese de inversão de operador diferencial.

A ação mínima original é a ação clássica mais o acoplamento dos antifields ao vetor BRST (5). Por invariância do pareamento cotangente e porque a ação clássica só depende de g e phi, a ação transformada é, na convenção em que sQ é a derivada de S_BV em Q*,

\[
S_{\rm BV}^{\rm new}
=S_{\rm BV}^{\rm metric}[g,\phi,C;g^*,\phi^*,C^*]
 +\int\chi_A^*\,\upsilon^A.
\tag{10}
\]

Esta é uma igualdade de funcionais locais formais. Não se está projetando antifields a zero antes de comparar cohomologias. As alterações do antifield de C contêm os termos de compensação de (7); eles são exatamente os termos necessários para (10).

Além do par (chi,upsilon), a parte dupla dos antifields forma um segundo par contrátil. Para evitar depender de convenções de sinal do antibracket, defina p_A:=s upsilon_A*; por (10), p_A é chi_A* ou seu negativo, com coeficiente unitário. Então

\[
s\upsilon_A^*=p_A,\qquad sp_A=0.
\tag{11}
\]

O diferencial sobre o setor métrico e seus antifields é independente desses dois pares.

## 5. Contração incluindo jatos e módulo d

Seja rho a derivação ímpar de número de ghost −1 que envia upsilon a chi, p a upsilon*, anula chi e upsilon*, e anula todas as variáveis métricas, de matéria, C e seus antifields. Prolongue rho com as derivadas totais. Seja N o operador que conta os quatro tipos de variáveis dos pares e todos os seus jatos. Verificação sobre os geradores dá

\[
\{s,\rho\}=N,\qquad [N,s]=0.
\tag{12}
\]

Na álgebra de formas com a convenção sd+ds=0, o prolongamento dá também rho d+d rho=0. Se sa+dm=0 e a_k,m_k têm grau N=k>0, então

\[
a_k=\frac1k(s\rho+\rho s)a_k
=s\left(\frac{\rho a_k}{k}\right)
 +d\left(\frac{\rho m_k}{k}\right).
\tag{13}
\]

Portanto toda dependência nos pares é trivial também módulo d. A projeção pi que põe os pares e seus jatos iguais a zero comuta com s e d; se uma forma puramente métrica for exata no complexo maior, aplicar pi à primitiva mostra que já era exata no complexo métrico. Inclusão e projeção induzem inversas:

\[
H^{g,p}_{\rm formal}(s_{\rm vielbein}\mid d)
\cong H^{g,p}_{\rm formal}(s_{\rm metric}\mid d).
\tag{14}
\]

Os divisores em (13) são inteiros positivos. Para uma série formal, a contração é coeficiente a coeficiente; não produz denominadores em campos. Não há aumento não controlado da ordem de jato em uma aplicação de rho. O levantamento canônico anterior pode aumentar finitamente essa ordem, mas sua inversa também é local de ordem finita em cada coeficiente.

[KNOWN — apoio delimitado] O mecanismo geral de pares contráteis, incluindo cohomologia módulo d e os pares dos antifields, encontra-se em [BBH 2000, §§2.6–2.7](https://arxiv.org/pdf/hep-th/0002245v3). As fórmulas (1)–(11) constroem aqui os pares efetivamente usados para esta ação de vielbein; não se atribui àquela referência a decomposição específica no fundo Einstein–sigma.

## 6. Naturalidade nos dados de fundo e limites de colagem

Sob uma mudança simultânea de referencial local e→Omega e, ebar→Omega ebar, com Omega(x) Lorentz, a matriz A e S não mudam como endomorfismos do espaço-tempo, enquanto L→Omega L Omega⁻¹. Assim chi e upsilon se transformam na mesma representação adjunta. Como sOmega=0 para essa mudança de apresentação externa, a igualdade upsilon=s chi é preservada. Os antifields transformam na representação dual densitizada.

A contração rho usa a identidade entre dois exemplares do mesmo fibrado, portanto é compatível com essas mudanças, inclusive seus prolongamentos em jatos. Sob mudanças simultâneas de coordenadas dos campos e fundos, A,S e os pareamentos são tensoriais. Isso mostra que o procedimento pode ser usado nas cartas de um fibrado de referenciais sobre um fundo fixado, sem escolher um coframe global adicional. A isometria relativa representada por L precisa permanecer no setor formal da identidade; a afirmação não atravessa componentes ou ciclos globais do espaço de referenciais.

Naturalidade **nos dados externos transportados conjuntamente** não é independência quântica da escolha de gbar. O procedimento pode produzir primitivas com dependência em gbar; remover ou controlar essa dependência é uma exigência adicional quando requerida. Tampouco se identifica uma densidade covariante de fundo com uma densidade invariável sob o gauge quântico não linear.

## 7. O contrato pago e os contratos que permanecem

[DERIVED] A comparação local formal métrica–vielbein não precisa ficar limitada ao ideal H0 das equações: a transformação canônica e os pares explícitos fornecem a equivalência dos complexos BV relativos completos neste espaço perturbativo. Ela aplica-se em particular ao grau (ghost,forma)=(1,4), **se** uma classificação de anomalias tiver sido demonstrada no mesmo espaço formal admissível.

[OPEN] A nulidade desse grupo para o sigma não decorre da equivalência. Persistem a compatibilidade entre classes de coeficientes nas importações, a cohomologia característica relativa requerida, a admissibilidade das primitivas na construção causal e as questões globais/entre fundos. A presente prova não identifica funções suaves arbitrárias com suas séries de Taylor nem avalia uma série de flutuações em um campo distante do fundo.

Sem CAS, Lean, execução de um.py, escrita em originais, alteração de gate ou teste de natureza.
