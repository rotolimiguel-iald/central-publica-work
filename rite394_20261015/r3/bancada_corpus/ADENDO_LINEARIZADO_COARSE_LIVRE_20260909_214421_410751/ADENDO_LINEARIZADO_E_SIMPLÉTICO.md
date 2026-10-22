# Adendo: equivalência do sistema linearizado e corrente simplética no representante livre

[DERIVED — prova escrita, não compilada em Lean] O certificado livre do adendo anterior permite transportar a equação de Jacobi inteira entre a extensão probabilística e Einstein–sigma, localmente e depois de remover as direções redundantes. A corrente simplética também se transporta nas soluções linearizadas, mediante a escolha explícita de potencial e as condições de contorno abaixo.

Este arquivo acrescenta resultados à [prova congelada do bloco livre](<C:/IALD/Central de Patentes/Chatgpt/COARSE_GRAINING_VARIACIONAL_LIVRE_20260909_212902_6343960/PROVA_COARSE_GRAINING_LIVRE.md>), sobretudo §§4–7. Não altera essa prova nem os contraexemplos da classe anterior. A ação Einstein–Hilbert mais sigma é [POSTULATE]; partição dos ramos, relógio e representante estendido são [INPUT]. Não se atribui esta extensão ao `um.py` canônico.

## 1. Domínio e Hessiana correta do sistema com vínculo

Trabalhamos numa carta aberta `U` de dimensão quatro, com um representante suave `P_*` estritamente positivo, relógio temporal e bloco livre de Gram positivo. A construção anterior fornece esses dados localmente, inclusive para o habitante ajustado `g=dr²−4cos²(r/2)γ`, `Λ=3/4`, `κC=4`, com um novo relógio lento escolhido para tornar o residual positivo.

O mapa é

\[
\Phi(P)=(g[P],\phi[P]),\qquad
\phi_a[P]=\sqrt{\frac{\sum_\ell P_{a\ell}}{1-P_0}},
\qquad \sum_a\phi_a^2=1.
\]

Use uma carta `y=(y¹,…,y^{m−1})` no alvo esférico positivo e escreva `X=(g,y)`. Isso trata o vínculo exatamente. Seja `S_c[X]` a ação restrita à esfera e `E[X]` seu operador de Euler–Lagrange, com densidades incorporadas à notação. O fundo é on-shell: `E[X_*]=0`, onde `X_*=Φ(P_*)`. Defina

\[
A=D\Phi_{P_*},\qquad H=DE_{X_*}=\operatorname{Hess}S_c[X_*].
\]

`H` é a Hessiana **restrita ao sigma normalizado**, com todos os blocos mistos entre métrica e matéria. Não é a Hessiana do campo `φ` tratado como independente e sem vínculo. O índice `*` em `A^*` abaixo denota adjunto formal por integração, não conjugação de Hilbert num domínio já especificado.

Uma descrição equivalente mantém os componentes extrínsecos `φ_a` e usa o multiplicador reconstruído

\[
\lambda_* =\sum_a\phi_a\Box_g\phi_a
=-\sum_a g^{-1}(d\phi_a,d\phi_a).
\]

A segunda variação restrita é a Hessiana da ação completa com esse multiplicador, testada em `φ·ψ=0`. De fato, ao longo de uma família normalizada de duas variáveis,

\[
\phi\cdot\partial_{st}\phi=-\psi_s\cdot\psi_t.
\]

A equação não restrita da ação sem multiplicador é `E_{0,φ}=C√|g| λ_*φ` no fundo. Seu produto com `∂_{st}φ` fornece o termo `−C√|g|λ_* ψ_s·ψ_t`, exatamente o termo quadrático do multiplicador. Ignorá-lo daria uma Hessiana diferente. Não acrescentamos um grau de liberdade físico independente para `δλ`; ele é reconstruído da variação dos campos.

## 2. Inverso à direita: operador diferencial que preserva suporte

Na carta, `A` tem ordem no máximo um: `g[P]` depende de `P,dP`, enquanto `φ[P]` depende de `P`. Em coordenadas locais independentes `p^i` para a variação normalizada das probabilidades,

\[
(Ap)^\alpha=a^\alpha{}_i p^i+b^{\alpha\mu}{}_i\partial_\mu p^i.
\]

A construção explícita anterior dá um operador linear `R` tal que

\[
\boxed{A R=\operatorname{Id}.}
\]

Para explicitar sua dependência diferencial, escreva `s=1−q`, `c=dq`, `w=F^{-1}c`, `b=c(w)` e

\[
L_F(h)=-h+2h(w,w)c\otimes c/b^2,\qquad L_F^2=\operatorname{Id}.
\]

Para `v=(h,ψ)`, com `φ·ψ=0`, a parte coletiva produz

\[
D_\phi F[\psi]=4s\sum_a d\phi_a\odot d\psi_a
+2s\sum_a\phi_a\psi_aF[Q_a],
\]

onde `α⊙β=α⊗β+β⊗α`. No grupo livre `a_*`, de peso interno constante `η`, escolha

\[
K_v=\frac{L_F(h)-D_\phi F[\psi]}{s\phi_{a_*}^2\eta},
\qquad W_v=O N_x(-D K_v/4).
\]

A variação interna induzida por `W_v`, somada à variação coletiva `ψ`, é `Rv`. Ela mantém `δq=0` e satisfaz `A(Rv)=(h,ψ)`. Em termos da carta `y`, basta substituir `ψ=D_yφ\,δy`. `R` tem ordem no máximo um; a dependência em `∂ψ` é compensação explícita, não inversão de uma equação diferencial.

Os coeficientes são suaves e limitados em compactos interiores com margens positivas. Em particular,

\[
\operatorname{supp}(Rv)\subseteq\operatorname{supp}v.
\]

Portanto `R:C_c^∞(U,TX)→C_c^∞(U,TP)` é contínuo na topologia usual dos testes. Aqui “preserva suporte compacto” não significa “operador compacto” no sentido de análise funcional. A prova também dá estimativas locais do tipo `||Rv||_{H^k}≤C_K||v||_{H^{k+1}}`; não fornece um inverso limitado na mesma norma de Sobolev sem perda de derivada.

A igualdade `AR=Id` é uma identidade de operadores diferenciais suaves no fundo. Logo vale também sobre distribuições, depois de usar trivializações locais dos fibrados.

## 3. Injetividade distribucional do adjunto

No interior, o adjunto formal de `A` é

\[
(A^*T)_i=a^\alpha{}_iT_\alpha
-\partial_\mu(b^{\alpha\mu}{}_iT_\alpha).
\]

Para uma distribuição `T` e um teste compacto `f` no alvo, a identidade do inverso dá

\[
\langle T,f\rangle
=\langle T,ARf\rangle
=\langle A^*T,Rf\rangle.
\]

Assim,

\[
\boxed{A^*T=0\ \Longrightarrow\ T=0,\qquad R^*A^*=\operatorname{Id}.}
\]

Não foi suposta uma sobrejetividade abstrata de variações: o teste `Rf` é exatamente o fornecido pelo bloco quadrático explícito. O resultado é interior/distribucional e não pressupõe condições de contorno de um operador autoadjunto. Não prova auto-adjunticidade espectral de `H` ou de `A^*HA`.

## 4. Segunda variação e equação de Jacobi composta

Para `S_P=S_c∘Φ`, a regra da cadeia funcional antes de impor as equações é

\[
D^2S_P(p_1,p_2)
=D^2S_c(Ap_1,Ap_2)
+DS_c[D^2\Phi(p_1,p_2)].
\]

Para testes compactos, a última parcela é o pareamento de `E` com `D²Φ`; o termo de fronteira desaparece. No fundo on-shell **restrito**, `E=0`, e obtemos

\[
\boxed{\operatorname{Hess}S_P[P_*]=B=A^* H A.}
\]

Equivalentemente, a primeira equação composta é `E_P=A^*E`; sua variação é `DE_P=(DA^*)E+A^*HA`, com o primeiro termo nulo no fundo. Como `A` tem ordem um e `H` ordem dois para Einstein–sigma, `B` pode apresentar ordem até quatro. Essa ordem aparente não autoriza contar soluções ou graus de liberdade adicionais: a fatoração e o inverso impõem a degenerescência exata examinada a seguir.

Para qualquer perturbação suave local `p`, e também distribucional no sentido linear,

\[
\boxed{Bp=0\ \Longleftrightarrow\ H(Ap)=0.}
\]

A ida aplica `R^*` a `A^*HAp=0`; a volta é imediata. Reciprocamente, se `Hv=0`, então `p=Rv` satisfaz `Bp=0` e `Ap=v`. O levantamento conserva o suporte existente; não pressupõe que soluções hiperbólicas não triviais tenham suporte compacto no espaço-tempo inteiro. Suporte compacto foi exigido dos **testes**, e condições de dados de Cauchy são outro problema.

Temos a sequência exata cindida de espaços de soluções locais,

\[
0\longrightarrow\ker A\longrightarrow\ker B
\mathrel{\mathop{\longrightarrow}^{A}}\ker H
\longrightarrow0,
\]

com cisão `R` sobre `ker H`. Explicitamente,

\[
p=R(Ap)+(p-RAp),\qquad A(p-RAp)=0.
\]

Portanto `ker B/ker A≅ker H`. As direções de `ker A` são redundâncias **linearizadas** da representação; este argumento não afirma que todas integrem um grupo global de simetrias finitas.

## 5. Difeomorfismos e quociente linear físico

O mapa completo `Φ` é natural sob difeomorfismos quando os rótulos da partição são fixos e os pesos são campos escalares. Sua linearização satisfaz

\[
A K_P\xi=K_X\xi,
\qquad K_P\xi=\mathcal L_\xi P_*,
\qquad K_X\xi=(\mathcal L_\xi g_*,\mathcal L_\xi\phi_*).
\]

A invariância da ação no fundo dá `H K_Xξ=0`, portanto `K_Pξ∈ker B`. A escolha de levantamento que fixa o relógio, `R K_Xξ`, difere de `K_Pξ` por uma direção de `ker A`. Assim não há conflito entre fixar `δq=0` na fórmula do inverso e incluir o gauge infinitesimal completo no quociente.

Para parâmetros de gauge admitidos no mesmo domínio e nas mesmas condições de fronteira,

\[
\boxed{
\frac{\ker B}{\ker A+\operatorname{im}K_P}
\simeq
\frac{\ker H}{\operatorname{im}K_X}.
}
\]

Se a classe de parametrização mantiver `q` fixo em todas as variações, use `R im K_X` no denominador esquerdo; a conclusão linear permanece. Não inferimos daqui um gauge finito global dessa fatia.

A correspondência prova que um modo físico não nulo da teoria ambiente, quando estabelecido no domínio local adotado, possui um levantamento fino `Rv` que não pode ser somente vertical mais difeomorfismo. Se o fosse, sua imagem seria gauge. Isso supera precisamente a limitação anterior de cinco categorias/posto quatro, na qual toda imagem de variação era gauge. Não acrescenta modos físicos além dos da ação Einstein–sigma adotada, nem presume uma contagem global por harmônicos de `S³`.

## 6. O termo de fronteira criado pelas derivadas de Φ

Fixe um potencial local para a ação ambiente,

\[
\delta L_X=E_\alpha\delta X^\alpha+\partial_\mu\theta_X^\mu(X;\delta X).
\]

Os coeficientes `E_α` são densidades, de modo que esta escrita coordenada usa uma divergência ordinária. A fórmula vale para Einstein–Hilbert, embora `θ_X` possa conter derivadas de `δg`. A construção padrão de potencial, corrente e suas ambiguidades está em [Iyer–Wald, §§3 e 6, equações (20), (40)–(47) e (75)](https://arxiv.org/pdf/gr-qc/9403028). A integração por partes específica do mapa diferencial `Φ` é feita aqui.

Como `δX=Ap`,

\[
E_\alpha(Ap)^\alpha
=(A^*E)_i p^i+\partial_\mu J^\mu(E,p),
\qquad
\boxed{J^\mu(E,p)=E_\alpha b^{\alpha\mu}{}_i p^i.}
\]

Logo uma escolha exata de potencial para a Lagrangiana composta é

\[
\boxed{\theta_P^\mu(P;p)
=\theta_X^\mu(\Phi(P);D\Phi_Pp)+J^\mu(E[\Phi(P)],p).}
\]

O termo `J` não pode ser omitido fora da solução: resulta da transferência da derivada de `p` para `E`. Esta fórmula usa o operador `A(P)=DΦ_P` dependente do campo, antes da avaliação em `P_*`.

Defina a corrente pela derivada exterior no espaço de campos, com convenção

\[
\omega(p_1,p_2)=\delta_1\theta(p_2)-\delta_2\theta(p_1)
-\theta([\delta_1,\delta_2]).
\]

Para extensões que comutam, o último termo é zero. Na parcela `θ_X`, os termos `δ_1(DΦp_2)−δ_2(DΦp_1)` cancelam pela simetria da segunda variação de `Φ` — ou pelo termo de comutador na forma invariante. A dependência diferencial de `Φ` não permite descartar esse cancelamento sem justificativa.

No fundo `E=0`, a derivada de `J` deixa precisamente

\[
\boxed{\begin{aligned}
\omega_P^\mu(p_1,p_2)
={}&\omega_X^\mu(Ap_1,Ap_2)\\
&+(HAp_1)_\alpha b^{\alpha\mu}{}_i p_2^i
-(HAp_2)_\alpha b^{\alpha\mu}{}_i p_1^i.
\end{aligned}}
\]

Os termos que contêm `E δb` desaparecem, mas os termos que contêm `δE` em geral permanecem. Se `Bp_1=Bp_2=0`, a injetividade de `A^*` já demonstrada implica `HAp_1=HAp_2=0`. Portanto, para **soluções linearizadas**, com esses potenciais escolhidos,

\[
\boxed{\omega_P(p_1,p_2)=\omega_X(Ap_1,Ap_2).}
\]

Esta é uma igualdade local de correntes, não apenas uma alegação de invariância da integral. Fora das equações linearizadas, a fórmula anterior exibe a diferença explicitamente.

## 7. Integral sobre uma hipersuperfície e ambiguidades

Seja `Σ⊂U` uma hipersuperfície espacial na região de validade do representante. Para perturbações para as quais as integrais existam, a igualdade anterior implica

\[
\Omega^P_\Sigma(p_1,p_2)
=\int_\Sigma\omega_P(p_1,p_2)
=\Omega^X_\Sigma(Ap_1,Ap_2).
\]

Com a escolha casada de potenciais da seção 6, a igualdade vale na mesma `Σ`. Para interpretá-la como forma conservada no espaço de soluções, é necessário ainda controlar o fluxo pela fronteira lateral entre hipersuperfícies. Em um domínio de dependência contido na carta, dados de suporte espacial adequado, ou condições de fluxo nulo devidamente especificadas, fornecem esse controle; não se pressupõe um `S³` global dentro da carta positiva.

Se outra convenção usa `θ→θ+dY`, então

\[
\Omega_\Sigma\longmapsto\Omega_\Sigma
+\int_{\partial\Sigma}
\big(\delta_1Y(p_2)-\delta_2Y(p_1)-Y([\delta_1,\delta_2])\big).
\]

Assim a preservação da forma integrada exige potenciais casados ou o desaparecimento desse termo, por exemplo quando as perturbações e seus jatos relevantes se anulam numa vizinhança de `∂Σ`. Acrescentar `dβ` à Lagrangiana acrescenta `δβ` ao potencial e não muda sua derivada exterior de campo quando o mesmo termo é transportado. Uma ação de fronteira escolhida independentemente, ou condições de contorno diferentes nos dois modelos, requerem comparação própria; não estão pagas pela prova interior.

Para difeomorfismos, a identidade de Noether no fundo e nas soluções linearizadas dá a corrente ambiente como derivada exterior de uma carga de superfície. Logo parâmetros que se anulam com os jatos necessários perto da fronteira geram direções nulas de `Ω`; parâmetros com carga de superfície não devem ser eliminados automaticamente. Esta distinção acompanha a identidade local de Iyer–Wald citada acima.

Todas as direções de `ker A` pertencem ao radical de `Ω^P`, pois sua imagem é zero. Mais precisamente, pela sobrejetividade em soluções,

\[
\boxed{\operatorname{rad}\Omega^P=A^{-1}(\operatorname{rad}\Omega^X).}
\]

Consequentemente os espaços de soluções reduzidos pelos **radicais completos**, nas mesmas condições admitidas, são isomorfos como espaços simpléticos. Para identificar esses radicais somente com difeomorfismos e redundâncias, é preciso que a análise ambiente de vínculos e modos nulos já esteja completa. Não substituímos essa análise por uma contagem de componentes.

## 8. Alcance quântico e o que continua sendo condição

[DERIVED] Esta construção fornece, no representante livre local on-shell, uma equivalência entre equações de Jacobi, classes lineares de soluções e formas pré-simpléticas, com os termos de fronteira explicitados. Não exige um inverso não linear suave da construção de Nash: usa apenas o inverso diferencial explícito no fundo. Não demonstra que toda solução linearizada se integre a uma família global de soluções exatas; obstruções de estabilidade linear em espaços globais ficam fora do enunciado.

[INPUT] Se uma construção da álgebra CCR ou de estados físicos do sistema Einstein–sigma reduzido foi estabelecida no mesmo domínio e com o mesmo espaço de soluções, o isomorfismo simplético permite transportá-la ao quociente da parametrização fina. Tal transporte depende desse resultado ambiente; não é uma nova demonstração de existência de estados de Hadamard, positividade de Hamiltoniano, renormalização ou ausência de anomalias. Sem forma reduzida não degenerada e condições de suporte/contorno compatíveis, essa conclusão deve permanecer condicional.

A positividade das probabilidades usada aqui é uma propriedade do **fundo clássico** e de curvas suaves para parâmetro suficientemente pequeno. A flutuação linear `p=Rv` vive em um espaço tangente linear. Sua promoção eventual a distribuição operador-valuada não demonstra `P_*+\widehat p≥0` como operador, nem que todos os valores de amplitude de um estado gaussiano permaneçam no simplex positivo. Um estado gaussiano de perturbações não é uma distribuição limitada apenas a configurações clássicas positivas. Qualquer definição quântica não linear de probabilidades normalizadas exigiria construção adicional.

[OPEN] A extensão global, sua compatibilidade entre cartas, a identificação com dados selecionados fisicamente, a escolha de observáveis não lineares, o tratamento quântico interagente e uma prova de preservação de positividade operatorial não são conclusões deste adendo. O estatuto é local e linear; a prova escrita ainda não foi compilada em Lean nem incorporada ao programa canônico.
