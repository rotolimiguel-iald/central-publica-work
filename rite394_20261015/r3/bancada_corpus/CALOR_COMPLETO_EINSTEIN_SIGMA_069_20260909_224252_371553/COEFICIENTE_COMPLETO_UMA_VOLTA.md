# Coeficiente local completo de uma volta — Einstein–sigma

09/09/2026. [DERIVED — demonstração escrita] [KNOWN — coeficiente universal de calor] [REAL — controles simbólicos exatos]. Todo material desta pasta é novo; nenhuma fonte canônica ou nota congelada foi alterada. Nenhum um.py foi executado ou importado. Não há nova prova Lean nesta entrega.

**Resultado.** Para a ação Einstein–sigma adotada e um fundo on-shell, o calibre de de Donder produz um operador de Laplace tipo em **10 componentes métricas mais 3 tangentes sigma**, com conexão efetiva não diagonal. Um par Grassmann de fantasmas difeomórficos tem quatro componentes. A combinação diferencial de uma volta é

\[
\mathcal C_4=\frac12\,\mathrm{tr}_{13}b_4(L_B)
-\mathrm{tr}_{4}b_4(L_{\rm gh}).
\tag{0.1}
\]

A conexão, o endomorfismo e todos os seus traços são construídos abaixo. No fundo específico \(a=2\cos(r/2)\), \(\phi=\mathrm{id}\), \(\kappa c=4\), a avaliação local covariante, com \(x=a^{-2}\), é

\[
\boxed{\mathcal C_4(x)=\frac{7440x^2+1616x-211}{96}.}
\tag{0.2}
\]

Incluem-se as divergências totais na expressão. A parcela explicitamente divergente é \(5x/4\). O número não é inferido do setor sigma em métrica externa: vêm incluídos os blocos mistos e o determinante ghost. A interpretação como divergência de uma volta usa a normalização diferencial, a medida e o contorno descritos nas seções 6–7. (0.2) não afirma existência de um traço de calor Lorentziano ou de uma rotação global de Wick.

## 1. Entradas geométricas e operador físico

[INPUT] A ação ambiente é a da [Hessiana Jacobi 066](<C:/IALD/Central de Patentes/Chatgpt/QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md>):

\[
S=-\frac1{2\kappa}\int\mu_g(R-2\Lambda)
+\frac c2\int\mu_g\,Q,\qquad \phi:M^4\to S^3,\quad c,\kappa>0.
\]

A convenção Lorentziana é \(+---\) e
\(R^\rho{}_{\sigma\mu\nu}=\partial_\mu\Gamma^\rho_{\nu\sigma}
-\partial_\nu\Gamma^\rho_{\mu\sigma}+\cdots\),
\(\mathrm{Ric}_{\sigma\nu}=R^\rho{}_{\sigma\rho\nu}\).
Na versão Riemanniana, a esfera tem escalar positivo. Para as contrações escreva

\[
s=\kappa c,\quad u_\mu=d\phi(\partial_\mu),\quad
W_{\mu\nu}=\langle u_\mu,u_\nu\rangle,\quad Q=g^{\mu\nu}W_{\mu\nu},
\]
\[
U=u_\mu\otimes u^\mu,\qquad B_{\mu\nu}=D_\mu u_\nu,\qquad
B^2=\langle B_{\mu\nu},B^{\mu\nu}\rangle .
\]

D inclui a conexão do alvo e a do índice covetor. B é simétrico. O fundo é on-shell:

\[
\tau=g^{\mu\nu}B_{\mu\nu}=0,\qquad
\mathrm{Ric}=\Lambda g+sW,\qquad R=4\Lambda+sQ.
\tag{1.1}
\]

O fibrado bosônico é \(V=\mathrm{Sym}^2T^*M\oplus\phi^*TS^3\), de posto 13. Não há quarta flutuação sigma normal à esfera: o vínculo foi eliminado pelo mapa exponencial tangente. Seja \(\nabla^0\) a conexão direta de Levi–Civita mais a conexão sigma e \(I_{\rm tr}h=h-g\,\mathrm{tr}(h)/2\).

O calibre é \(C_\nu h=\nabla^\mu(I_{\rm tr}h)_{\mu\nu}\), com
\(\ell=1/(2\kappa)\). A Hessiana gauge-fixada e sua normalização são

\[
D=\mathcal H+\ell C^*C,\qquad
\mathcal B=\mathrm{diag}(-I_{\rm tr}/(4\kappa),-cI_3),
\qquad \mathcal P=\mathcal B^{-1}D .
\tag{1.2}
\]

A forma de fibra física é a parelha de fundo multiplicada por \(\mathcal B\), e é indefinida. Não foi substituída por uma norma positiva. \(\mathcal B\) é paralela e invertível, pois os acoplamentos são constantes e \(I_{\rm tr}^2=1\) em quatro dimensões.

O fantasma é o operador efetivamente derivado \(Q_{\rm gh}=CK=\nabla^2+\mathrm{Ric}\) em covetores. Ele não é identificado com \(K^*K\).

## 2. Extração explícita da conexão e de E

A normalização de (1.2) fornece

\[
\mathcal P=(\nabla^0)^2+2\omega^\rho\nabla^0_\rho+V_0.
\]

Os blocos fora da diagonal da conexão são

\[
(\omega_\rho\xi)_{\mu\nu}
=s\big(g_{\mu\rho}\langle u_\nu,\xi\rangle
+g_{\nu\rho}\langle u_\mu,\xi\rangle\big),
\]
\[
\omega_\rho h=-\frac12u^\nu h_{\rho\nu}
+\frac14u_\rho\,\mathrm{tr}(h).
\tag{2.1}
\]

Os blocos diagonais de \(\omega_\rho\) são zero. A parte de ordem zero é

\[
(V_0h)_{\mu\nu}
=2R_{\mu\rho\nu\sigma}h^{\rho\sigma}
-s(W_\mu{}^\rho h_{\rho\nu}+W_\nu{}^\rho h_{\rho\mu}),
\]
\[
(V_0)_{\xi h}h=-B_{\mu\nu}h^{\mu\nu},\qquad
(V_0)_{h\xi}=0,\qquad (V_0)_{\xi\xi}=QI_3-U .
\tag{2.2}
\]

Para verificar a origem de (2.2), aplique \(-2I_{\rm tr}\) ao bloco métrico (4.4) da nota 066. Na variação da fonte, a parte derivativa
\(A_{\mu\nu}(\xi)-g_{\mu\nu}\langle u^\alpha,D_\alpha\xi\rangle\)
vira simplesmente \(A_{\mu\nu}(\xi)\) após \(I_{\rm tr}\). A parte algébrica em h e a curvatura simplificam por (1.1), restando exatamente o primeiro bloco de (2.2). O bloco de matéria normalizado é
\(D^2\xi+(QI-U)\xi-B:h-u^\nu C_\nu h\), que fornece a segunda linha de (2.1) e os demais blocos. Nenhum C(h) foi posto a zero antes de calcular o operador completo.

Defina

\[
\widehat\nabla=\nabla^0+\omega,\qquad
E=V_0-\nabla^0_\rho\omega^\rho-\omega_\rho\omega^\rho .
\tag{2.3}
\]

A forma normal é \(\mathcal P=\widehat\nabla^2+E\), e o operador elíptico diferencial correspondente é \(L_B=-\mathcal P\), quando a base é Riemanniana. A regra de forma normal é a das equações (2.1)–(2.4) de [Vassilevich](https://arxiv.org/html/hep-th/0306138v3). Aqui seus coeficientes são calculados da Hessiana específica.

As contrações intermediárias são

\[
(\nabla^0\!\cdot\omega)_{h\xi}=2sB,\qquad
(\nabla^0\!\cdot\omega)_{\xi h}=-B:h/2,
\]
\[
(\omega_\rho\omega^\rho)_{hh}h
=-\frac s2(W\cdot h+h\cdot W)+\frac s2W\,\mathrm{tr}(h),
\qquad
(\omega_\rho\omega^\rho)_{\xi\xi}=-2sU .
\]

Usou-se \(\tau=0\) na segunda expressão da primeira linha. Portanto

\[
\boxed{\begin{aligned}
(E_{hh}h)_{\mu\nu}
 &=2R_{\mu\rho\nu\sigma}h^{\rho\sigma}
-\frac s2\big(W_\mu{}^\rho h_{\rho\nu}
+W_\nu{}^\rho h_{\rho\mu}+W_{\mu\nu}\mathrm{tr}(h)\big),\\
(E_{h\xi}\xi)_{\mu\nu}&=-2s\langle B_{\mu\nu},\xi\rangle,\\
E_{\xi h}h&=-\tfrac12 B_{\mu\nu}h^{\mu\nu},\\
E_{\xi\xi}&=QI_3+(2s-1)U .
\end{aligned}}
\tag{2.4}
\]

As misturas métricas alteram tanto E quanto sua curvatura. Tratar o setor sigma como três operadores desacoplados perderia esses termos. Em particular, seu potencial efetivo não é apenas \(QI-U\).

A integração por partes da Hessiana e, diretamente, (2.1) dão
\(\omega_\rho^{\,t}G_{\mathcal B}+G_{\mathcal B}\omega_\rho=0\) e
\(E^tG_{\mathcal B}=G_{\mathcal B}E\), onde \(G_{\mathcal B}\) inclui o pareamento em tensores simétricos. Isto afirma compatibilidade com a forma indefinida especificada, não positividade.

## 3. Curvatura efetiva e prova dos traços

A curvatura completa é

\[
\widehat\Omega_{\rho\sigma}
=\Omega^0_{\rho\sigma}
+\nabla^0_\rho\omega_\sigma-\nabla^0_\sigma\omega_\rho
+[\omega_\rho,\omega_\sigma].
\tag{3.1}
\]

A curvatura base em tensores covariantes é
\((\Omega^0_{\rho\sigma}h)_{\mu\nu}
=-R^\lambda{}_{\mu\rho\sigma}h_{\lambda\nu}
-R^\lambda{}_{\nu\rho\sigma}h_{\mu\lambda}\).
No alvo, \(A_{\rho\sigma}=u_\rho\otimes u_\sigma-u_\sigma\otimes u_\rho\).
O bloco sigma de (3.1) é \((1+s)A_{\rho\sigma}\). Os blocos mistos são

\[
(\widehat\Omega_{\rho\sigma}\xi)_{\mu\nu}
=s\big(g_{\mu\sigma}\langle B_{\rho\nu},\xi\rangle
+g_{\nu\sigma}\langle B_{\rho\mu},\xi\rangle
-g_{\mu\rho}\langle B_{\sigma\nu},\xi\rangle
-g_{\nu\rho}\langle B_{\sigma\mu},\xi\rangle\big),
\]
\[
\widehat\Omega_{\rho\sigma}h
=-\tfrac12(B_\rho{}^\nu h_{\sigma\nu}
-B_\sigma{}^\nu h_{\rho\nu}).
\tag{3.2}
\]

O bloco métrico é \(\Omega^0_{hh}+C_{\rho\sigma}\), com

\[
(C_{\rho\sigma}h)_{\mu\nu}
=-\frac s2(g_{\mu\rho}W_\nu{}^\lambda h_{\sigma\lambda}
+g_{\nu\rho}W_\mu{}^\lambda h_{\sigma\lambda}
-(\rho\leftrightarrow\sigma))
\]
\[
\hspace{12mm}
+\frac s4(g_{\mu\rho}W_{\nu\sigma}
+g_{\nu\rho}W_{\mu\sigma}
-(\rho\leftrightarrow\sigma))\,\mathrm{tr}(h).
\tag{3.3}
\]

Essas fórmulas tornam todos os blocos computáveis apenas com Riem, u e B. Não há curvatura efetiva recebida como hipótese.

As contrações em dimensão quatro são

\[
\boxed{\mathrm{tr}_{13}E=-R+(2-s)Q,}
\tag{3.4}
\]
\[
\boxed{\mathrm{tr}_{13}E^2
=3\,\mathrm{Riem}^2
+\left(\frac{s^2}2+4s+1\right)Q^2
+\left(\frac{13s^2}2-4s+1\right)W^2+2sB^2,}
\tag{3.5}
\]
\[
\boxed{\begin{aligned}
\mathrm{tr}_{13}\widehat\Omega_{\rho\sigma}\widehat\Omega^{\rho\sigma}
={}&-6\,\mathrm{Riem}^2+4s\,\mathrm{Ric}_{\mu\nu}W^{\mu\nu}+2sRQ\\
&+(-3s^2+4s+2)W^2+(-3s^2-4s-2)Q^2-8sB^2 .
\end{aligned}}
\tag{3.6}
\]

Aqui W² é \(W_{\mu\nu}W^{\mu\nu}\). Traços são os traços ordinários de endomorfismos do fibrado, sem usar sinais extras de norma para contar componentes.

**Prova das contrações.** Ponha \(\mathcal Rh=R_{\mu\rho\nu\sigma}h^{\rho\sigma}\), \(\mathcal S_Wh=W\cdot h+h\cdot W\) e \(\mathcal T_Wh=W\,\mathrm{tr}(h)\). A simetrização dos dois índices fornece
\(\mathrm{tr}\mathcal R=-R/2\),
\(\mathrm{tr}\mathcal R^2=3\mathrm{Riem}^2/4\),
\(\mathrm{tr}\mathcal S_W=5Q\),
\(\mathrm{tr}\mathcal T_W=Q\).
Além disso,
\(\mathrm{tr}\mathcal R\mathcal S_W=-\mathrm{Ric}\cdot W\) e
\(\mathrm{tr}\mathcal R\mathcal T_W=\mathrm{Ric}\cdot W\); o termo cruzado cancela em Ehh². Se W é diagonal com autovalores \(w_i\),
\(\mathrm{tr}(\mathcal S_W+\mathcal T_W)^2=10W^2+2Q^2\).
Os dois blocos mistos de E² somam \(2sB^2\); o bloco sigma usa
\(\mathrm{tr}U=Q\), \(\mathrm{tr}U^2=W^2\). Isso prova (3.4)–(3.5).

Para (3.6), a parte base métrica vale \(-6\mathrm{Riem}^2\). Em uma base que diagonaliza W, para cada par \(\rho<\sigma\), (3.3) dá

\[
\mathrm{tr}C_{\rho\sigma}^2
=-\frac{s^2}{2}\big(W^2+2w_\rho w_\sigma\big).
\]

Ao somar os pares ordenados, resulta
\(\mathrm{tr}C_{\rho\sigma}C^{\rho\sigma}
=-s^2(5W^2+Q^2)\).
Só as entradas seccionais de Riem participam do traço cruzado nessa base; para cada par,
\(\mathrm{tr}(\Omega^0_{\rho\sigma}C_{\rho\sigma})
=sR_{\rho\sigma\rho\sigma}(Q+w_\rho+w_\sigma)\).
A soma com o fator cruzado 2 é \(2sRQ+4s\,\mathrm{Ric}\cdot W\).

A parte sigma contribui \(2(1+s)^2(W^2-Q^2)\). Para cada componente alvo de B, a contração dos blocos mistos (3.2), somada nos pares ordenados e nos dois blocos diagonais de Ω², é
\(-2s(4B^2-|\mathrm{tr}B|^2)\); com \(\tau=0\), ela vale \(-8sB^2\). Somar essas quatro parcelas prova (3.6). A diagonalização é legítima na base Riemanniana; as identidades resultantes são polinomiais tensoriais e continuam à complexificação e às contrações Lorentzianas. Não se pressupõe diagonalização ortogonal real de todo tensor Lorentziano.

No fantasma,
\[
E_{\rm gh}=\mathrm{Ric}_\nu{}^\rho,\qquad
(\Omega_{{\rm gh},\mu\nu})_\alpha{}^\beta=-R^\beta{}_{\alpha\mu\nu},
\]
\[
\mathrm{tr}_4E_{\rm gh}=R,\qquad
\mathrm{tr}_4E_{\rm gh}^2=\mathrm{Ric}^2,\qquad
\mathrm{tr}_4\Omega_{\rm gh}^2=-\mathrm{Riem}^2 .
\tag{3.7}
\]

## 4. Coeficiente geral completo

[KNOWN] Para \(L=-(\widehat\nabla^2+E)\), o coeficiente interior de calor, na convenção em que
\(K(t;x,x)\sim(4\pi t)^{-2}(I+t b_2+t^2b_4+\cdots)\), é

\[
\mathrm{tr}\,b_4=
\mathrm{tr}\left(\frac{\widehat\nabla^2E}{6}+\frac{RE}{6}
+\frac{E^2}{2}+\frac{\widehat\Omega^2}{12}\right)
+\frac{\mathrm{rank}(V)}{360}
(12\Box R+5R^2-2\mathrm{Ric}^2+2\mathrm{Riem}^2).
\tag{4.1}
\]

É a fórmula interior (4.28) de [Vassilevich](https://arxiv.org/html/hep-th/0306138v3). A conexão induzida em endomorfismos satisfaz
\(\mathrm{tr}\widehat\nabla^2E=\Box\mathrm{tr}E\); não é preciso calcular individualmente derivadas de todos os componentes de E.

Substituir (3.4)–(3.7) em (0.1) dá

\[
\boxed{\begin{aligned}
\mathcal C_4={}&\frac{43}{72}\mathrm{Riem}^2
-\frac{37}{72}\mathrm{Ric}^2-\frac{31}{144}R^2
+\frac16 RQ+\frac s6\,\mathrm{Ric}_{\mu\nu}W^{\mu\nu}\\
&+\frac{5s+1}{6}Q^2+\frac{9s^2-5s+2}{6}W^2+\frac s6B^2
-\frac16\Box R+\frac{2-s}{12}\Box Q .
\end{aligned}}
\tag{4.2}
\]

Esta é uma fórmula local geral **on-shell**, no calibre e parametrização declarados. Um cálculo off-shell precisa restaurar os termos da Hessiana proporcionais às equações de fundo; (4.2) não os fornece por extrapolação.

A identidade de Bochner para a aplicação harmônica ao S³ é

\[
\tfrac12\Box Q=B^2+\mathrm{Ric}\cdot W-(Q^2-W^2).
\]

Se desejado, ela permite a forma equivalente

\[
\mathcal C_4=\frac{43}{72}\mathrm{Riem}^2-\frac{37}{72}\mathrm{Ric}^2
-\frac{31}{144}R^2+\frac16RQ
+\left(s+\frac16\right)Q^2
+\left(\frac32s^2-s+\frac13\right)W^2
-\frac16\Box R+\frac16\Box Q .
\tag{4.3}
\]

A derivada de \(\tau=0\) é usada nessa identidade. As duas formas são controles recíprocos, não diferentes escolhas de fonte.

## 5. Redução explícita no fundo curvo

Para \(g=dr^2-a^2h_{S^3}\), \(a=2\cos(r/2)\), \(\phi=\mathrm{id}\), ponha \(x=a^{-2}\) e \(H=a'/a\). Em um referencial ortonormal Lorentziano,

\[
u_0=0,\quad u_i=a^{-1}e_i,\quad
B_{0i}=B_{i0}=-Ha^{-1}e_i,\quad B_{00}=B_{ij}=0,
\]
\[
R_{0i0j}=-\tfrac14\delta_{ij},\quad
R_{ijkl}=-(2x-\tfrac14)(\delta_{ik}\delta_{jl}-\delta_{il}\delta_{jk}),
\]
\[
H^2=x-\tfrac14,\quad H'=-x,\quad \Box x=x/2 .
\]

As contrações resultam em

| Invariante | Valor |
|---|---|
| R | \(3-12x\) |
| Ric² | \(48x^2-18x+9/4\) |
| Riem² | \(48x^2-12x+3/2\) |
| Q; W² | \(-3x;\ 3x^2\) |
| Ric·W | \(12x^2-9x/4\) |
| B² | \(-6x^2+3x/2\) |
| □R; □Q | \(-6x;\ -3x/2\) |

O sinal de B² é o de uma contração Lorentziana; ele não é uma norma Hilbert positiva. Com s=4, os traços completos são

\[
\mathrm{tr}E=18x-3,\qquad
\mathrm{tr}E^2=588x^2-24x+9/2,\qquad
\mathrm{tr}\widehat\Omega^2=-300x^2-84x-9,
\qquad \Box\mathrm{tr}E=9x.
\]

Separando somente para mostrar o determinante combinado,

\[
\mathrm{tr}_{13}b_4=\frac{62160x^2-4240x+377}{240},
\qquad
\mathrm{tr}_{4}b_{4,\rm gh}=\frac{3120x^2-1540x+179}{60}.
\tag{5.1}
\]

A combinação é (0.2). Seu termo x² é \(155x^2/2\); não houve cancelamento desse coeficiente no cálculo completo. A parte total divergente de (4.2) é \(5x/4\); retirando-a formalmente, resta
\((7440x^2+1496x-211)/96\).
Só se pode descartar uma divergência integrada depois de declarar o suporte, a função de acoplamento ou as condições de bordo. O domínio aberto cosmológico não permite apagar termos de bordo por nome.

O valor não é nulo no intervalo físico x>1/4. Isto identifica uma divergência local a subtrair no esquema diferencial adotado. Uma classificação de quais combinações são removíveis por redefinições de campos, mudanças de parâmetros ou termos topológicos requer manter sua classe de funcionais e seu esquema de medida explícitos. A avaliação em um fundo único não distingue todos os invariantes presentes em (4.2).

**Controle de gravidade pura.** Retirando o bloco sigma inteiro e tomando u=B=0 e Ric=Rg/4, os traços dão
\[
\mathcal C_{4,\rm grav}=-\frac{29}{80}R^2+\frac{53}{90}\mathrm{Riem}^2.
\]
É metade da convenção \(b_{4,\rm grav}-2b_{4,\rm ghost}\) da equação (47) de [Bastianelli, Bonezzi e Melis](https://link.springer.com/article/10.1140/epjc/s10052-022-11119-w). Se apenas u=0 mantendo o sigma tangente, somam-se três escalares minimais; o teste não os apaga. Esse controle externo confere os sinais de Ric, E e o fator ghost.

## 6. Medida, modo conforme e auxiliares

O dado diferencial \(L_B=-\mathcal B^{-1}D\) não é toda a definição da integral funcional. Em base de fibra Riemanniana, a forma principal
\[
-\mathcal B=\mathrm{diag}(I_{\rm tr}/(4\kappa),cI_3)
\]
tem nove autovalores \(1/(4\kappa)\), um autovalor \(-1/(4\kappa)\) na direção de traço e três autovalores c. Logo
\[
\det_{\rm fibra}(-\mathcal B)=-\frac{c^3}{(4\kappa)^{10}}.
\tag{6.1}
\]

Há uma direção conforme negativa, mesmo antes de discutir o espectro baixo do operador. Para dar sentido à gaussiana formal euclidiana, especifica-se um contorno para essa direção, ou uma prescrição de fase espectral. A rotação do componente de traço por i é uma normalização local possível: após a reescala paralela dos módulos, transforma a forma principal em identidade, e o operador diferencial transformado é similar ao normalizado. Os coeficientes de traço de calor são invariantes por essa similaridade. Isso não prova convergência da integral funcional interagente nem torna positiva uma medida gravitacional não perturbativa.

Na normalização desta nota, o determinante diferencial é definido pelos operadores de símbolo principal identidade, e os fatores de fibra são mantidos como fatores **ultralocais de medida**. Uma escrita formal é
\(\hbar\,\mathrm{Tr}_{\rm reg}\log(-\mathcal B)/2\), com a fase de (6.1) e o regulador da identidade declarados separadamente. Não se aplica uma identidade irrestrita
\(\det_\zeta(\mathcal B L)=\det\mathcal B\,\det_\zeta L\).
Outro regulador conjunto pode exigir um funcional local de conversão, incluindo a escolha de normalização da medida. Os resultados (4.2) e (0.2) dizem exatamente qual é a contribuição diferencial no esquema fixado; não presumem cancelamento por um fator de medida não calculado.

Antes de eliminar b, a parte bosônica da ação quadrática é
\[
\frac12\langle u,\mathcal Hu\rangle+\langle b,Cu\rangle
-\frac1{2\ell}\langle b,b\rangle .
\]
Completar o quadrado fornece a Hessiana D e o fator formal
\[
\big[\det_{\rm ultra}(-\ell^{-1}I_4)\big]^{-1/2}.
\tag{6.2}
\]
É um operador de multiplicação, sem derivadas. Sua fase e o fator constante de normalização do calibre pertencem à medida escolhida. Ele não é um quinto operador de onda nem justifica acrescentar ou subtrair quatro componentes em (0.1). Regularizá-lo usando algum operador diferencial de referência introduziria a correspondente escolha local de medida, a ser registrada.

A [apresentação Grassmann da raiz](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md>) distingue a matriz sesquilinear WZ da Hessiana graduada. Na ordem (c,barc), a Hessiana é
\(\bigl(\begin{smallmatrix}0&-Q_{\rm gh}\\Q_{\rm gh}&0\end{smallmatrix}\bigr)\)
e a ação é \(\langle\bar c,Q_{\rm gh}c\rangle\). Um único par de quatro componentes produz \(\det Q_{\rm gh}\); portanto sua ação efetiva é \(-\hbar\,\mathrm{Tr}\log L_{\rm gh}\). Os sinais constantes da conversão não dobram a contribuição fantasma.

## 7. Logaritmo UV e passagem de assinatura

Fixe a contribuição diferencial euclidiana formal por
\[
\Gamma_1^{\rm diff}
=\frac\hbar2\mathrm{Tr}\log L_B-\hbar\,\mathrm{Tr}\log L_{\rm gh}.
\]
Com corte de tempo próprio \(\rho^{-2}\), a parcela logarítmica é

\[
\boxed{\Gamma_{1,\log}^{\rm diff}
=-\frac{\hbar}{(4\pi)^2}
\log\frac{\rho^2}{\mu^2}\int\mu_g\,\mathcal C_4.}
\tag{7.1}
\]

O contra-termo nessa convenção tem sinal oposto. Zero-modos, autovalores negativos e volume infinito requerem tratamento infravermelho próprio; não foram resolvidos pelo limite de tempo próprio pequeno. Condições de bordo poderiam acrescentar coeficientes que esta nota não calcula.

A fórmula local foi deduzida para o operador elíptico Riemanniano e então expressa como identidade de jatos tensoriais. Avaliar essa expressão na métrica Lorentziana produz o coeficiente covariante local usado na prescrição de renormalização correspondente. A seção 2.3 de [Vassilevich](https://arxiv.org/html/hep-th/0306138v3) distingue esse uso de uma expansão global de calor Lorentziana. No determinante de Feynman, os fatores de i da ação e da densidade seguem a convenção Lorentziana; (7.1) fixa somente a convenção euclidiana exibida.

Nenhuma transformação global \(r\mapsto it\), nenhum espaço euclidiano global positivo associado ao cilindro e nenhuma escolha única de vácuo são inferidos. O coeficiente local diferencial não depende da parte suave escolhida da covariância Hadamard livre; isso não determina a parte não local e dependente de estado da ação efetiva. O estado físico e a extensão BRST 068 são entradas já construídas para a teoria causal, com seus escopos próprios.

## 8. Controles, alcance e incorporação

[REAL] VERIFICACAO_CALOR_COMPLETO.json contém **23 controles exatos**: a Hessiana normalizada reconstruída antes de E; equações do fundo; preservação da forma de fibra; curvatura efetiva; traços ghosts; contração no fundo; normalização e controle de gravidade pura. Os tensores simétricos são representados pelas dez entradas independentes, com as entradas fora da diagonal duplicadas ao reconstruir h; o pareamento usa o fator 2 correspondente.

[REAL] VERIFICACAO_TRACOS_INVARIANTES.json acrescenta **8 controles exatos**. Uma matriz dφ densa, Hessianas tangentes com traço zero e uma curvatura de Kulkarni–Nomizu densa conferem (3.4)–(3.6), com o acoplamento s ainda simbólico. A álgebra dos invariantes, a redução Bochner e a especialização ao fundo são verificadas separadamente. Um conjunto finito de controles não substitui a prova tensorial da seção 3; sua função é detectar sinais, multiplicidades e contrações erradas.

[DERIVED + KNOWN] Foram pagos a conexão e o endomorfismo efetivos do sistema completo, seus traços e o coeficiente local de uma volta no calibre adotado, incluindo redução explícita no fundo. O sigma externo anterior permanece correto em seu escopo, mas já não é o único determinante calculado.

[OPEN] O cálculo não fecha as identidades mestras interagentes, anomalias locais/globais, a medida de uma quantização independente dos dados P, condições finitas de renormalização, convergência perturbativa, estabilidade de fundos corrigidos ou uma conclusão UV. O resultado é on-shell e local; generalizações off-shell, de calibre, domínio ou ação precisam de seus operadores e comparações próprios. A adoção da ação e da correspondência física continua explícita. Não se declara gravidade quântica resolvida.

Nenhum original foi modificado. Os dois recibos, os scripts e as fontes desta nota ficam identificados por hashes medidos no manifesto acompanhante. O total desta pasta é **31 controles CAS e zero compilação Lean**.
