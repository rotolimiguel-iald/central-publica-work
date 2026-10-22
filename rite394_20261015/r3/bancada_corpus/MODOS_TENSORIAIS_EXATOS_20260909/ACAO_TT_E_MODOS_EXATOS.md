# Setor tensorial Einstein–sigma: ação reduzida e modos exatos

[DERIVED — demonstração escrita, não nova compilação Lean] Esta nota deduz o setor tensorial da extensão ambiente Einstein–sigma usada na entrega 066. Os controles simbólicos associados conferem identidades determinadas; não substituem a demonstração de redução, a completude espectral ou a condição de Hadamard.

## 1. Modelo e hipóteses

A ação adotada é [INPUT]

\[
S=-\frac1{2\kappa}\int\mu_g(R-2\Lambda)
 +\frac c2\int\mu_g g^{\mu\nu}\langle\partial_\mu\phi,\partial_\nu\phi\rangle,
\qquad \phi:M\to S^3,\quad c>0,\quad\kappa c=4,\quad\Lambda=3/4.
\]

Assinatura `+---` e convenção de curvatura são as da [nota acoplada anterior](<C:/IALD/Central de Patentes/Chatgpt/QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md>). O fundo on-shell é

\[
g=dr^2-a(r)^2\gamma,\qquad a(r)=2\cos(r/2),\qquad \phi(r,z)=z,
\qquad 0<r<\pi,
\]

onde γ é a métrica da esfera unitária. A positividade de κ segue de c>0. A ação é uma entrada declarada; sua escolha não é deduzida aqui apenas da normalização de probabilidades.

Para usar harmônicos completos, consideramos a extensão geométrica `M=(0,π)×S³`, globalmente hiperbólica com seções de Cauchy compactas. Isso estende g e φ suavemente. Não transforma os cinco pesos `P_a=(1−P_0)z_a²` em coordenadas globais estritamente positivas: esses pesos anulam nas faces e perdem sinais. A leitura categórica anterior continua local no octante; a extensão geométrica e quântica tem estatuto próprio. Não se inclui a fronteira singular a=0.

## 2. Variação TT dentro do sistema acoplado

Seja t uma seção simétrica espacial, com `tr_γ t=0` e `D^it_ij=0`. Parametrize a métrica espacial positiva por

\[
h_{ij}(\varepsilon)=a^2\gamma_{ik}(e^{\varepsilon t})^k{}_j,
\quad N=1,\quad b^i=0,\quad\delta\phi=0.
\]

A exponencial preserva exatamente o determinante espacial. A condição TT é condição da perturbação inicial; não se exige que a métrica não linear permaneça numa superfície de calibre definida pela mesma fórmula linear.

O setor é fechado nas equações **linearizadas**. Na fórmula da entrega 066,

\[
\delta\tau=J\xi-h^{\mu\nu}B_{\mu\nu}-C^\mu(h)u_\mu,
\]

temos ξ=0, B_AB=0, h apenas espacial TT e C(h)=0. Logo δτ=0. As partes escalar e vetorial das restrições gravitacionais e da fonte também se anulam: δT_rr e a variação escalar de curvatura são proporcionais a traços, enquanto as componentes de momento são divergências de t. Portanto lapse e shift de primeira ordem iguais a zero satisfazem as restrições nesse setor. Correções de segunda ordem ao lapse/shift multiplicariam as equações de fundo na ação quadrática e não alteram a redução on-shell.

## 3. Segunda variação da curvatura espacial

É útil derivar o termo de curvatura, pois omitir a resposta anisotrópica da matéria mudaria a frequência.

Para a esfera unitária tridimensional, `Ric(γ)=2γ`, `R(γ)=6`. Em uma direção TT,

\[
\delta\operatorname{Ric}=\tfrac12(-\Delta_\gamma+6)t,
\qquad \delta R=0,
\qquad \delta G^{(3)}_{\rm cov}=-\tfrac12\Delta_\gamma t.
\]

A primeira identidade segue da fórmula de variação de Ricci, comutando derivadas e usando curvatura seccional +1. O laplaciano tem sinal `Δ=D^iD_i`. Como `G^{(3)}=-γ`, elevar os índices na variação dá

\[
\delta G^{(3)\,ij}=-\tfrac12\Delta t^{ij}+2t^{ij}.
\]

Para `I[q]=∫√q R[q]`, a primeira variação é `δI=−∫√q G^{ij}δq_ij`. Na curva `q=γe^{εt}`, `q''(0)=γt²` e o determinante é constante. Assim

\[
I''(0)=\int_{S^3}\left(\tfrac12\langle t,\Delta t\rangle-|t|^2\right)dV_\gamma
=-\frac12\int_{S^3}(|Dt|^2+2|t|^2)dV_\gamma.
\]

O coeficiente de ε² na ação é metade da segunda derivada. O termo espacial de Einstein–Hilbert fornece, portanto,

\[
-\frac{a}{8\kappa}\int_{S^3}(|Dt|^2+2|t|^2)dV_\gamma.
\]

Não há fronteira espacial em S³; para deduções locais, a integração por partes exige o suporte/condição de contorno correspondente.

## 4. Cinética e contribuição da matéria

Na forma ADM compatível com as convenções acima, a parte cinética da gravidade é
`√h(K^i_jK^j_i−K²)/(2κ)`. Como

\[
K^i{}_j=H\delta^i{}_j+\tfrac12\varepsilon\dot t^i{}_j+O(\varepsilon^2),
\quad \operatorname{tr}(e^{-\varepsilon t}\partial_re^{\varepsilon t})=0,
\]

a contribuição quadrática é `a³|ṫ|²/(8κ)`. Comutadores que aparecem em ordem dois têm traço zero. O volume e o termo cosmológico não variam nessa parametrização.

O mapa sigma fica fixado em φ=id, portanto seu tensor espacial de derivadas é **γ**, não a métrica perturbada. Consequentemente,

\[
L_m=-\frac{ca}{2}\operatorname{tr}(e^{-\varepsilon t})
=-\frac{3ca}{2}-\varepsilon^2\frac{ca}{4}|t|^2+O(\varepsilon^3).
\]

Essa é a contribuição de matéria que deve acompanhar o operador gravitacional. A ação reduzida é

\[
\boxed{S^{(2)}_{TT}=\frac1{8\kappa}\int dr\,a^3dV_\gamma
\left[|\dot t|^2-\frac1{a^2}\left(|Dt|^2+(2+2\kappa c)|t|^2\right)\right].}
\tag{4.1}
\]

Usando κc=4, o termo de massa espacial é 10. A equação é

\[
\ddot t+3H\dot t+\frac1{a^2}(-\Delta_\gamma+10)t=0.
\tag{4.2}
\]

A cinética tem sinal positivo. O Hamiltoniano quadrático em tempo r é uma soma de termos positivos no setor TT; isso não o torna uma energia conservada, pois o fundo depende de r.

[REAL — controle simbólico exato, alcance finito] Para o modo homogêneo anisotrópico de Bianchi IX, `q=diag(e^{εu},e^{εv},e^{-ε(u+v)})` em referencial invariante, a curvatura espacial possui coeficiente quadrático `−2[u²+v²+(u+v)²]`. Esse modo TT tem autovalor −Δ igual a 6. O resultado coincide com `(6+2)/4=2` na fórmula geral e confere separadamente a parcela sigma. O [recibo de controles](<C:/IALD/Central de Patentes/Chatgpt/MODOS_TENSORIAIS_EXATOS_20260909/VERIFICACAO_MODOS_TT.json>) distingue esse controle da prova geral acima.

## 5. Harmônicos e normalização canônica

[KNOWN] Em S³ unitária existe uma base ortonormal completa de tensores TT com

\[
-\Delta_\gamma T_{\ell A}=[\ell(\ell+2)-2]T_{\ell A},\qquad\ell\ge2.
\]

O índice A percorre a degenerescência e as duas famílias tensorias. As identidades espectrais e de traço/divergência estão organizadas em [Lindblom–Taylor–Zhang, seções 3–4](https://arxiv.org/html/1709.08020v1); a construção de bitensores TT é tratada por [Allen](https://arxiv.org/abs/gr-qc/9411023). Aqui ℓ designa o grau total, chamado k na primeira referência.

Expanda `t=Σt_{ℓA}T_{ℓA}`. Cada amplitude tem frequência espacial quadrada `ℓ(ℓ+2)+8`. Introduza tempo conforme

\[
\eta=\log(\sec(r/2)+\tan(r/2)),\qquad dr=a\,d\eta,
\quad a=2\operatorname{sech}\eta,\quad 0<\eta<\infty,
\]

e variável canônica `v_{ℓA}=a t_{ℓA}/(2√κ)`. Após um termo de fronteira temporal, a ação por modo é

\[
S^{(2)}_{\ell A}=\frac12\int d\eta\,[|v'|^2-(p_\ell^2+2\operatorname{sech}^2\eta)|v|^2],
\qquad p_\ell^2=(\ell+1)^2+6\ge15.
\tag{5.1}
\]

Foi usado `a''/a=1−2sech²η`. O coeficiente é estritamente positivo para todos os modos TT permitidos.

## 6. Solução exata, Wronskiano e estado positivo por modos

Para qualquer p>0, defina

\[
\boxed{f_p(\eta)=\frac{(p-i\tanh\eta)e^{-ip\eta}}{\sqrt{2p(p^2+1)}}.}
\tag{6.1}
\]

Escrevendo T=tanhη e T'=1−T², a diferenciação direta dá

\[
f_p''+(p^2+2\operatorname{sech}^2\eta)f_p=0,
\quad f_p\overline{f_p'}-f_p'\overline{f_p}=i,
\quad |f_p|^2=\frac{p^2+\tanh^2\eta}{2p(p^2+1)}.
\tag{6.2}
\]

Por exemplo, para o numerador F=(p−iT)e^{-ipη}, os termos restantes na equação são `2iT(1−T²)−2p(1−T²)+2(1−T²)(p−iT)=0`. Seu Wronskiano é `2ip(p²+1)`; o denominador de (6.1) produz exatamente i. Essas identidades foram conferidas simbolicamente, sem amostragem numérica, nos controles associados.

Em η→∞, (6.1) tende a uma onda de frequência positiva multiplicada pela fase constante `(p−i)/√(p²+1)`. Isso escolhe um estado; não demonstra unicidade de um vácuo físico. O extremo do espaço-tempo não é acrescentado ao domínio.

A covariância dos modos canônicos é

\[
W_{TT}(\eta,x;\eta',x')=\hbar\sum_{\ell,A}f_{p_\ell}(\eta)\overline{f_{p_\ell}(\eta')}
T_{\ell A}(x)\otimes\overline{T_{\ell A}(x')}.
\tag{6.3}
\]

Para qualquer truncamento finito e função teste complexa F, o valor `W(F*,F)` é `ℏΣ|∫f̄T̄·F|²≥0`. Os coeficientes de um teste suave decaem mais rapidamente que qualquer potência do grau, enquanto a multiplicidade e as derivadas dos modos possuem crescimento polinomial. Isso define o limite como distribuição, preserva positividade e permite a diferenciação distribucional. O Wronskiano fixa o comutador canônico reduzido. Para a perturbação métrica t, a covariância correspondente recebe o fator `4κ/[a(η)a(η')]`.

Assim há um estado quase livre positivo **do setor tensorial reduzido**, que satisfaz sua equação exata. A condição microlocal pode ser examinada pelo operador de Darboux espacial

\[
\mathcal D_\eta=(A-i\tanh\eta)(A^2+1)^{-1/2},\qquad
A=\sqrt{-\Delta_{TT}+9},
\]

aplicado aos modos ultrastáticos `e^{-iAη}(2A)^{-1/2}`. A prova microlocal e a passagem ao sistema físico acoplado são registradas separadamente na revisão desse contrato. A projeção TT é espacialmente não local: não se infere causalidade de todos os campos projetados a partir do nome “tensorial”, nem se identifica (6.3) com um estado de todas as treze componentes sem resolver as restrições e os setores restantes.

## 7. O que foi estabelecido

- [DERIVED] Fechamento linear do setor TT dentro do modelo Einstein–sigma adotado, ação quadrática (4.1), sinal cinético e equação (4.2).
- [DERIVED + KNOWN] Redução espectral em S³ e normalização canônica (5.1).
- [DERIVED; REAL para os controles CAS] Modos exatos, Wronskiano e covariância positiva reduzida.
- [OPEN nesta nota isolada] Subida de estado Hadamard ao quociente físico acoplado, interações quânticas, anomalias e UV. Os trabalhos simultâneos podem reduzir a primeira obrigação, mediante suas próprias provas.

Não foram executados `um.py`, testes da natureza ou compilação Lean nesta construção. Não há afirmação de fechamento quântico não linear, de confirmação observacional ou de representação global pelos cinco pesos originais.
