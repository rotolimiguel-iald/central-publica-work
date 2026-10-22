# A carga conforme no fundo Einstein–sigma recuperado

16/09/2026. [DERIVED — cálculo clássico escrito, com controles numéricos independentes]. Reutiliza a contração já formalizada em `DiamondConformalCurrent.conformal_current_divergence`; não reivindica outro teorema Lean. O objeto desta nota é a carga de matéria do fundo da 066–067, não o operador modular do estado interagente.

## 1. Tensor e traço da própria ação

Na convenção das fontes, \(T_{\mu\nu}=c(W_{\mu\nu}-\tfrac12 g_{\mu\nu}X)\), com \(W=\bar\phi^*\gamma\), \(X=\operatorname{tr}_gW=-3/a^2\). Em quatro dimensões,

\[
\operatorname{tr}_gT=-cX=3c/a^2,
\qquad\rho=3c/(2a^2),\qquad p=-c/(2a^2).
\]

Não acrescentamos a constante cosmológica a T: trata-se precisamente do tensor de matéria que aparece em \(G+\Lambda g=\kappa T\) na ação adotada. Uma definição diferente de carga total exigiria explicitar seus termos gravitacionais, melhorias e fronteiras.

## 2. O diamante esférico e seu vetor conforme

Escreva \(g=a(\eta)^2[d\eta^2-d\chi^2-\sin^2\chi\,d\Omega_2^2]\), \(a=2\operatorname{sech}\eta\). Fixe centro temporal \(\eta_0>0\) e raio angular \(0<L<\min(\eta_0,\pi)\), ajustando o intervalo temporal para conter o diamante interior \(|\eta-\eta_0|+\chi<L\). O raio próprio da bola central é \(\ell=a_0 L\).

Com \(u=\eta-\eta_0\), o vetor, sem incorporar o fator 2π, é

\[
\xi^\eta=\frac{\cos u\cos\chi-\cos L}{\sin L},\qquad
\xi^\chi=-\frac{\sin u\sin\chi}{\sin L}.
\]

No cilindro estático, a componente ηη da equação conforme dá
\(\bar\psi=\partial_\eta\xi^\eta=-\sin u\cos\chi/\sin L\).
A componente χχ dá \(\partial_\chi\xi^\chi=\bar\psi\), a mista anula por \(\partial_\chi\xi^\eta=\partial_\eta\xi^\chi\), e a angular usa \(\xi^\chi\cot\chi=\bar\psi\). Portanto \(\mathcal L_\xi\bar g=2\bar\psi\bar g\). Após o fator a²,

\[
\mathcal L_\xi g=2\psi g,\qquad
\psi=-\frac{\sin u\cos\chi}{\sin L}-\tanh\eta\,\xi^\eta.
\]

Por conservação e simetria de T,

\[
\boxed{\nabla_\mu(T^{\mu\nu}\xi_\nu)=\psi\operatorname{tr}_gT
=\frac{3c}{a^2}\psi.}
\tag{1}
\]

É uma aplicação direta da identidade de corrente conforme já demonstrada na bancada. O fundo tem tensor não sem traço; não se substitui a equação por zero como em uma matéria conforme sem anomalia.

## 3. Primeiro coeficiente da carga de fundo, explicitamente delimitado

Para comparar superfícies próximas sem ambiguidade de bordo, use a bola de raio angular fixo L. A superfície central pertence ao diamante; as superfícies próximas aqui são uma família de controle da corrente no mesmo aberto de fundo. Não se afirma que sejam todas seções completas do mesmo diamante. O resultado diferencial central também vale para a família de seções com borda deslocada, quando sua contribuição inicial desaparece por \(\xi=0\) na borda central.

Defina \(Q(\eta)=2\pi\int_{B_L}T_{\mu\nu}\xi^\mu n^\nu\,d\Sigma\). Na seção central, a componente radial da corrente é zero. Integrando as outras componentes,

\[
Q(\eta_0)=12\pi^2 c a_0^2 I(L),\qquad
I(L)=\frac1{\sin L}\int_0^L(\cos\chi-\cos L)\sin^2\chi\,d\chi
=\frac{2+\cos^2L}{6}-\frac{L\cot L}{2}.
\]

A primeira derivada temporal de \(\xi^\eta\) se anula nessa seção; \((a^2)'=-2a^2\tanh\eta\). Logo

\[
\boxed{Q'(\eta_0)=-24\pi^2 c a_0^2\tanh\eta_0\,I(L).}
\tag{2}
\]

O integrando que define I é positivo no interior para 0<L<π, logo I>0. Na expansão de bola pequena,

\[
I(L)=L^4/15+O(L^6),\qquad
\left.\frac{dQ}{dr}\right|_0
=\frac{8\pi^2}{5}\,\frac{c H_0}{a_0^2}\,\ell^4+O(\ell^6)
\]

com \(H_0=(\dot a/a)_0=-\tanh\eta_0/a_0\); no resto, os dados do centro são mantidos fixos. Unidades são as da solução adotada pelas fontes, sem inventar uma escala experimental para seu raio unitário.

## 4. A conclusão que este número permite

O script [verify_sigma_conformal_current.py](verify_sigma_conformal_current.py) integra Q por Gauss–Legendre e diferencia a corrente densitizada por diferenças centrais. Três configurações independentes verificam (1)–(2); a redução de passo mostrou convergência de segunda ordem. O controle que impõe traço zero é recusado. Valores e erros estão em [SIGMA_CONFORMAL_CURRENT_CHECKS.json](SIGMA_CONFORMAL_CURRENT_CHECKS.json).

**(2) não é o primeiro coeficiente não central de \(R=K_\omega-K_\xi\).** Nesta conta T é o tensor clássico do fundo: sua contribuição à teoria linear é um número vezes a identidade. Pode mudar com a seção e continuar central. Subtrair essa constante não determina a ação do tensor quântico renormalizado nas flutuações. O teste demonstra que a carga não tem a conservação conforme usual nessa apresentação; não demonstra, por si, falha da igualdade das derivações modulares.

Também não identifica o sinal negativo de (2) com uma taxa de Lindblad. Ele resulta da contração deste fundo e da normalização da corrente. A escala \(\Gamma_\omega\), o efeito do dephasing no resto e a geometricidade regional exigem seus próprios operadores já tipados na [ponte regional](ESTADO_EINSTEIN_SIGMA_E_MODULAR_LOCAL.md).
