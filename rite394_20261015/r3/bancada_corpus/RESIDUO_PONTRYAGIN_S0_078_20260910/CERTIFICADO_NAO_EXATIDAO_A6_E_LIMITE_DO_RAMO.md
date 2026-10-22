# Primeiro resíduo de Pontryagin: certificado de não exatidão para s₀

10/09/2026. Investigação078, separada da entrega077. [DERIVED — demonstração escrita, aguardando revisão independente]. Somente novos arquivos em Chatgpt; nenhum original, fonte congelada, um.py ou gate alterado. Zero CAS, Lean e execução/importação de um.py.

**Resultado.** Na referência permitida de curvatura constante K=Λ/3>0, com sigma de fundo constante e a convenção de curvatura declarada, o resíduo homogêneo A₆ da transgressão de Pontryagin não é s₀-exato, mesmo permitindo antifields e coeficientes coordenados regulares de jatos finitos. Uma solução explícita das equações linearizadas e quatro ghosts de Killing fornecem um mapa para uma álgebra exterior com diferencial zero, no qual A₆ permanece não nulo.

Consequência delimitada: a classe específica [T≤5] construída077 não se levanta de C₅ a C₆. Isso não exclui outras classes em H³(C₅) com a mesma imagem cúbica em H³(C₃), obtidas por escolhas diferentes de α₄/α₅. Nenhuma obstrução final da anomalia ou do levantamento de toda a linha CE é deduzida.

## 1. O problema e a categoria exata

Na [construção077](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md>), com o [dicionário de sinais](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/DICIONARIO_CARTAN_DO_RECIBO_077.md>), obteve-se sT=A_P e

\[
A_6=\rho_{[2]}[h,h]\,C^0C^1C^2C^3,
\qquad
\rho_{[2]}dx^0dx^1dx^2dx^3
=\operatorname{tr}(W_{[1]}[h]\wedge W_{[1]}[h]).
\tag{1}
\]

O polinômio característico é P(X,Y)=tr(XY). A normalização p₁=−tr(R∧R)/(8π²) apenas multiplica os resultados por um escalar não nulo. Aqui W[1] é a curvatura de Weyl linearizada como 2-forma com valores em End(TM), e C é o ghost normalizado c=tC. A₆ tem ghost4 e valência6, sendo quadrático em h e quártico em C. O parâmetro t de Rees não é uma coordenada temporal.

A apresentação é métrica mínima, sem fontes externas θ/ω ou campos não mínimos de gauge fixing. O fundo B0=(g0,φ0) é inerte e on-shell. Os argumentos dinâmicos da álgebra são off-shell. Antifields são admitidos, com a correção do [adendo KT077](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>):

\[
s_0u=R_0C,\qquad s_0C=0,\qquad
s_0u^*=+H_0u,\qquad s_0C^*=R_0^\dagger u^*.
\tag{2}
\]

u=(h,ξ) e H0 é a Hessiana da ação Einstein–sigma física, sem fixação de gauge. Todas as fórmulas são prolongadas aos jatos. Não se substitui s₀ por d_H e não se descarta uma divergência como se fosse uma fronteira s₀.

O teste será local sobre uma vizinhança suficientemente pequena, longe de z=0. Uma vizinhança causalmente convexa e globalmente hiperbólica pode ser escolhida dentro da carta. Não se exige que a carta inteira do espaço forma seja globalmente hiperbólica nem se alteram as condições do estado físico de outra referência.

## 2. Critério de avaliação que inclui antifields

Sejam u_sol uma solução das equações LINEARIZADAS H0u=0 numa vizinhança e v_A campos de Killing de g0 que preservam φ0. Tome geradores ímpares constantes θ^A e atribua

\[
u\mapsto u_{\rm sol},\qquad
C\mapsto\sum_A\theta^A v_A,
\qquad u^*\mapsto0,\qquad C^*\mapsto0.
\tag{3}
\]

Prolongue essas atribuições a todos os jatos pelas derivadas dos campos indicados e avalie em um ponto p. Os coeficientes feitos de B0 são avaliados no mesmo fundo. Isso define um homomorfismo graduado

\[
\operatorname{ev}_p:(\mathcal A,s_0)
\longrightarrow(\Lambda(\theta),0).
\tag{4}
\]

Com efeito, cada gerador no lado direito de (2) avalia em zero: R0v_A=0, H0u_sol=0, R0†u*=0 e s0C=0. A mesma afirmação vale para todos os prolongamentos. Assim ev_p(s0F)=0 para toda expressão local finita F, incluindo expressões com antifields. Não é preciso que os v_A escolhidos fechem uma subálgebra de Lie: o diferencial de chegada é zero e s0C=0; não estamos aplicando aqui o diferencial CE não linear.

Equivalentemente, passa-se ao quociente pelo ideal diferencial gerado por R0C, H0u e todos os antifields, no qual o diferencial induzido é zero. A avaliação abaixo demonstra que A₆ não se anula nesse quociente. É um certificado mais concreto do que apenas nomear o ideal de Killing/EOM.

Se alguma primitiva formal B existisse na completação por valência, s0 preservaria valência, e sua componente B₆ satisfaria s0B₆=A₆. B₆ é um polinômio finito em jatos na classe [Rees074](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>). Basta avaliar esse coeficiente. Não avaliamos uma série formal inteira em amplitude numérica, operação que não seria justificada em geral.

## 3. Um habitante linearizado com o sinal de Λ da casa

Use coordenadas x⁰=τ, x¹=x, x²=y, x³=z, com z>0, assinatura (+---), orientação dτ∧dx∧dy∧dz e

\[
\eta=\operatorname{diag}(1,-1,-1,-1),\qquad
g_0=a(z)^2\eta,\qquad a(z)=\ell/z,\qquad
\Lambda=3/\ell^2>0.
\tag{5}
\]

A convenção é R^a{}_{bcd}=∂cΓ^a_bd−∂dΓ^a_bc+Γ^a_ecΓ^e_bd−Γ^a_edΓ^e_bc. Com ela, (5) satisfaz Ric(g0)=+3g0/ℓ². O fator conforme depende de uma coordenada ESPACIAL; isso evita trocar inadvertidamente o sinal de Λ ao usar a carta conforme temporal e a assinatura (+---). O nome de Sitter/anti-de Sitter não será usado para decidir esse sinal.

Para conferir, ponha w=ln a. A fórmula conformal em quatro dimensões é

\[
\operatorname{Ric}(e^{2w}\widetilde g)
=\operatorname{Ric}(\widetilde g)
-2(\widetilde\nabla dw-dw\otimes dw)
-\widetilde g\bigl(\widetilde\Box w+2|dw|_{\widetilde g}^2\bigr).
\tag{6}
\]

Em η, w_z=−1/z, w_zz=1/z², □ηw=−1/z² e |dw|²η=−1/z². O termo tensorial intermediário é zero, dando Ric(g0)=3η/z²=Λg0. A invariância conforme do Weyl implica W(g0)=0; junto à Ricci calculada, isso dá precisamente o tensor espaço forma com K=1/ℓ².

[KNOWN] A transformação conforme da conexão/Ricci e a invariância do Weyl são tratadas em [Wheeler, Weyl geometry, §2](https://arxiv.org/pdf/1801.03178). A conta (6) e seus sinais na assinatura e coordenadas utilizadas são explicitados aqui; não atribuo à referência o habitante específico abaixo.

Escolha k≠0 e z0>0. Seja f a solução real analítica da equação ordinária

\[
f''-\frac2z f'+k^2 f=0,\qquad f(z_0)=0,\qquad f'(z_0)=1.
\tag{7}
\]

Essa solução existe numa vizinhança de z0 porque os coeficientes da EDO são analíticos ali. Também pode ser construída pela combinação das soluções cos(kz)+kz sin(kz) e sin(kz)−kz cos(kz), cujo Wronskiano é k³z²≠0. Não se pressupõe qualquer extensão de jatos arbitrários a uma solução de PDE.

Defina o tensor γ com componentes somente no bloco xy:

\[
\gamma_{11}=f(z)\cos(k\tau),\quad
\gamma_{22}=-f(z)\cos(k\tau),\quad
\gamma_{12}=\gamma_{21}=f(z)\sin(k\tau),
\qquad h=a^2\gamma,\qquad\xi=0.
\tag{8}
\]

γ tem traço e divergência planos zero, e γ_zμ=γ_0μ=0. Para a família g_t=a²(η+tγ)=g0+t h, a variação plana da Ricci é δRic(η)_ij=−½□ηγ_ij. Além disso, δΓ^z_ij=½∂zγ_ij para i,j∈{1,2}; por isso δ(∇_i∂_jw)=γ'_ij/(2z). A variação do escalar □w+2|dw|² é zero, pela ausência de componentes z e pelo traço zero. Substituindo em (6),

\[
\delta\operatorname{Ric}(g_t)_{ij}-\Lambda h_{ij}
=-\tfrac12\Box_\eta\gamma_{ij}-\frac1z\partial_z\gamma_{ij}.
\tag{9}
\]

As demais componentes são zero. Como □ηγ=−(k²f+f'')Q(τ), (7) anula (9). Portanto δRic−Λh=0 em toda a vizinhança, não só no ponto. O traço da perturbação é zero e δR=0, de modo que também δ(G+Λg)=0. Em φ0 constante, a mistura linear métrica–sigma é zero e ξ=0 satisfaz as equações sigma linearizadas. Assim u_sol=(h,0) é solução do H0 acoplado exigida por (3), na convenção KT corrigida.

Não alegamos que g0+t h seja uma solução NÃO linear para t≠0. A solução que o teste precisa é exatamente a perturbação linearizada (8), e ela foi verificada por (9).

## 4. Weyl linearizado e valor não nulo da densidade

Como tensor de tipo (1,3), W(a²\widetilde g)=W(\widetilde g). Assim a 2-forma matricial W[1][h] e tr(W[1]∧W[1]) podem ser calculadas em η+tγ, com a mesma base coordenada. Não se introduz um fator de volume a⁴ adicional no traço das 2-formas.

Avalie em p=(0,0,0,z0). Nesse ponto f=0, f'=1, f''=2/z0. Escreva

\[
Q=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad
\dot Q=\begin{pmatrix}0&k\\k&0\end{pmatrix}.
\]

Os jatos necessários são γ_ττ=0, γ_zz=(2/z0)Q e γ_τz=dot Q. A fórmula linearizada da curvatura plana dá, para i,j em {1,2},

\[
(R_{[1]})_{0i0j}=0,\qquad
(R_{[1]})_{3i3j}=-Q_{ij}/z_0,\qquad
(R_{[1]})_{0i3j}=-\dot Q_{ij}/2.
\tag{10}
\]

A Ricci plana vale Q_ij/z0 e seu escalar é zero. Logo o Schouten plano linearizado é Q_ij/(2z0). Subtrair o produto métrico–Schouten produz

\[
(W_{[1]})_{0i0j}=-Q_{ij}/(2z_0),\quad
(W_{[1]})_{3i3j}=-Q_{ij}/(2z_0),\quad
(W_{[1]})_{0i3j}=-\dot Q_{ij}/2.
\tag{11}
\]

Para tornar o sinal e a não nulidade diretamente verificáveis, ponha A=1/(2z0), B=k/2 e e^{ab}=dx^a∧dx^b. As únicas 2-formas matriciais com ambos os índices ABAIXADOS que não se anulam são, além das obtidas por antissimetria,

\[
\begin{aligned}
W_{01}&=-A e^{01}+B e^{23},&
W_{02}&= A e^{02}+B e^{13},\\
W_{13}&= B e^{02}-A e^{13},&
W_{23}&= B e^{01}+A e^{23}.
\end{aligned}
\tag{12}
\]

W03=W12=0. Os fatores ½ da 2-forma já foram consumidos ao escrever os pares ordenados; não se conta cada par novamente. Levantando o primeiro índice com η,

\[
\operatorname{tr}(W\wedge W)
=-2\sum_{a<b}\eta_{aa}\eta_{bb}W_{ab}\wedge W_{ab}.
\tag{13}
\]

Cada um dos quatro pares de (12) contribui −4AB dτ∧dx∧dy∧dz: usa-se e02∧e13=−dτ∧dx∧dy∧dz. Portanto

\[
\boxed{\rho_{[2]}(p)=-16AB=-\frac{4k}{z_0}\ne0.}
\tag{14}
\]

Essa é uma conta algébrica escrita de quatro produtos de formas, não um resultado de CAS. Se a orientação ou a normalização de Pontryagin mudar, o sinal/fator correspondente muda; a não nulidade permanece. A amplitude de h pode ser multiplicada por qualquer escalar real pequeno não nulo, multiplicando (14) por seu quadrado. Assim o teste não depende de uma perturbação de amplitude finita afastada da origem formal.

## 5. Ghosts de Killing e certificado de cohomologia

Na carta (5), os quatro campos

\[
v_0=\partial_\tau,\quad v_1=\partial_x,\quad
v_2=\partial_y,\quad
v_3=\frac1{z_0}(\tau\partial_\tau+x\partial_x+y\partial_y+z\partial_z)
\tag{15}
\]

são Killing. Os três primeiros preservam a métrica por independência das coordenadas respectivas. A dilatação em (15) varia η por 2η e a² por −2a², cancelando-se. Todos preservam φ0 constante. Em p, seus valores são exatamente ∂0,∂1,∂2,∂3.

Tome C=Σ_(A=0)^3 θ^A v_A. Então C^μ(p)=θ^μ. A avaliação (3–4), usando (8), satisfaz

\[
\boxed{\operatorname{ev}_p(A_6)
=-\frac{4k}{z_0}\theta^0\theta^1\theta^2\theta^3\ne0.}
\tag{16}
\]

Toda fronteira s₀ tem avaliação zero por (2–4). Logo não existe B local finito regular, natural ou coordenado, de ghost3 e valência6 tal que s0B=A6. Antifields não removem o certificado: sua variação é H0u e seus prolongamentos, todos zero na solução explícita. O campo C* tampouco o remove, pois seus valores são zero e R0†u*=0.

Além disso, A₆ é s₀-fechado. W0=0 implica W[1][Lie_Cg0]=Lie_CW0=0 pela naturalidade do Weyl. Assim s0W[1]=0, enquanto s0C=0. Concluímos

\[
\boxed{[A_6]\ne0\quad\text{em }H^{4}(s_0)
\text{ no componente de valência seis dessa referência.}}
\tag{17}
\]

A afirmação vale para a álgebra regular que contém o habitante (8). Uma categoria que excluísse artificialmente esse habitante por denominadores singulares em jatos físicos teria outro domínio e não é a classe de polinômios/coeficientes formais de Rees usada aqui. Referência inerte on-shell e argumentos dinâmicos off-shell continuam separados: a avaliação em uma solução é um instrumento para detectar uma classe na álgebra off-shell, não uma mudança silenciosa do seu diferencial.

Uma primitiva universal regular que valesse para todos os B0 admissíveis também se restringiria a esse teste e daria uma contradição. Não se conclui, porém, a mesma não nulidade em toda referência, em particular no fundo não constante φ0=id, cujo setor de Killing preservando a matéria é diferente.

## 6. Consequência exata para a classe construída em077

Na [transgressão076](<C:/IALD/Central de Patentes/Chatgpt/TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md>), T=T≤5+t⁶α6+… e sT=A_P. O resíduo do truncamento T≤5 em valência seis é

\[
r_6=(sT_{\le5})_{[6]}=A_6-s_0\alpha_6.
\tag{18}
\]

Assim [r6]=[A6]≠0 em H(s0). Adicionar uma correção de valência seis B6 mudaria r6 somente por s0B6. Não pode torná-lo zero. Portanto o representante T≤5 não admite extensão a um ciclo em C6.

O resultado vale também para a sua CLASSE em H³(C5). Se algum ciclo em C6 se restringisse a T≤5+sB em C5, poderíamos escolher uma extensão finita de B a C6 e subtrair sua fronteira sB. Restaria um ciclo de C6 cuja restrição seria exatamente T≤5, contradizendo (18). Logo

\[
\boxed{[T_{\le5}]\notin
\operatorname{im}\bigl(H^3(C_6)\longrightarrow H^3(C_5)\bigr).}
\tag{19}
\]

Esta é uma obstrução ao prolongamento de UMA classe já construída. Não decide se existe outra classe β∈H³(C5) com a mesma imagem α3 em H³(C3) que pertença à imagem de C6. Uma alteração das correções de valências quatro e cinco pode acrescentar uma classe na fibra da restrição a C3 e mudar o resíduo de ordem seis. Os diferenciais não lineares que agem sobre essas alterações, incluindo os setores com antifields na valência apropriada, ainda precisam ser calculados.

Em particular, o fato de a linha CE inicial ter dimensão um não torna único seu levantamento em H³(C5). Não se substitui essa informação pela afirmação de que nenhum levantamento da linha existe. Tampouco (19) implica lim¹ não nulo ou falha de Mittag–Leffler: mapas posteriores e estabilização das imagens continuam questões distintas.

## 7. Estatuto e limites preservados

[DERIVED — aguardando revisão] (14–17) são um certificado explícito de não exatidão de A₆ no BRST linear mínimo, com sinal KT corrigido e antifields permitidos. A consequência (19) delimita o prolongamento da classe específica077. Não se usa a identidade de divergência da densidade para identificá-la com uma fronteira s₀.

[OPEN] Outras escolhas α₄/α₅ com o mesmo líder, obstruções subsequentes da linha inteira, imagens estabilizadas, cohomologia natural completa, consumo pela hierarquia de renormalização causal, anomalia efetiva/QME e UV. Este teste não refuta a TGL nem uma lei de área e não altera dados físicos, selos ou gates.

[REAL — documental] O manifesto mede cinco fontes locais antes/depois e os novos arquivos. Apenas escrita exclusiva em pasta078. Nenhum CAS/Lean foi executado para as fórmulas; nenhuma revisão prévia077 foi reaproveitada como aprovação desta investigação. O estado físico de outras entregas não foi reexaminado aqui.
