# Realização matricial e fatorização no mesmo estado produto

09/09/2026. Complemento à nota `REEXAME_GIBBS_DINAMICA_20260909/DEDUCAO_RESPOSTA_E_FRONTEIRA.md`. Esta análise própria explicita a realização dos pesos já formalizados. Não atribui aprovação a terceiros. Nenhuma folha Lean foi alterada ou recompilada nesta subtarefa.

**[DERIVED] O protocolo misto realiza, no mesmo estado produto da torre, os pesos de `MixedQuadraticGibbsResponse` e sua soma finita de respostas.** Na ordem quadrática escolhida, coincidem a variação de Shannon da medição Z, a variação da entropia de von Neumann e o incremento do próprio gerador de referência −log ρ₀. A preparação, os observáveis e o relógio continuam [INPUT]. A realização não determina a métrica nem a correspondência de área.

## 1. Um sítio: matrizes antes dos pesos

[INPUT] Fixe 0<p<1, inicialmente p>1/2, e ponha

\[
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
k=\tfrac12\log\frac p{1-p}>0,\quad
\rho_0=\operatorname{diag}(p,1-p)=\frac{e^{kZ}}{2\cosh k}.
\]

Escolha W=X+Z e a perturbação de Gibbs

\[
\rho_s=\frac{e^{\log\rho_0+sW}}{\operatorname{Tr}e^{\log\rho_0+sW}}.
\]

[DERIVED] O termo escalar de log ρ₀ cancela na normalização. Como X²=Z²=I e XZ+ZX=0, a matriz H_s=(k+s)Z+sX satisfaz

\[
H_s^2=((k+s)^2+s^2)I=r(s)^2I.
\]

Para k>0, r(s)>0 em todo s real: seu anulamento exigiria simultaneamente s=0 e k+s=0. As potências pares e ímpares da série exponencial dão

\[
e^{H_s}=\cosh r(s)I+\frac{\sinh r(s)}{r(s)}H_s,\qquad
\rho_s=\frac12\left(I+\frac{\tanh r(s)}{r(s)}H_s\right).
\]

Os autovalores de ρ_s são e^{±r}/(2 cosh r), positivos, de soma um. A matriz é, portanto, uma densidade fiel. A perturbação não pertence ao centralizador do estado: [W,log ρ₀]=k[X,Z]≠0.

[INPUT] Meça os projetores fixos E₊=(I+Z)/2 e E₋=(I−Z)/2. [DERIVED] Usando Tr X=Tr Z=Tr XZ=0 e Tr Z²=2, obtém-se

\[
q_\pm(s)=\operatorname{Tr}(\rho_sE_\pm)
=\frac12\left(1\pm\frac{k+s}{r(s)}\tanh r(s)\right).
\]

Essa é exatamente a função `mixedWeights k s`, com o índice 0 associado ao sinal + e o índice 1 ao sinal −. A fonte Lean define e analisa os pesos reais; a identificação matricial demonstrada neste parágrafo é [DERIVED], sem um novo recibo Lean para exponenciais matriciais.

## 2. Relógio quadrático e três respostas na mesma ordem

[DERIVED] Em s=0, r=k, r′=1, q₊=p e q′₊=1/(2 cosh²k). A entropia de Shannon S_Z(s)=−∑q_i(s)log q_i(s) satisfaz

\[
S_Z'(0)=\log\frac{1-p}{p}\,q'_+(0)
=-\frac{k}{\cosh^2k}.
\]

O gerador intrínseco de referência é

\[
K_0=-\log\rho_0=\log(2\cosh k)I-kZ
=\sum_{i=\pm}(-\log p_i)E_i.
\]

Logo, para todo s, sem aproximar e sem exigir que ρ_s seja diagonal,

\[
\Delta K_{\rm intr}(s)
=\operatorname{Tr}[(\rho_s-\rho_0)K_0]
=\sum_i(q_i(s)-p_i)(-\log p_i)
=-k\left(\frac{k+s}{r(s)}\tanh r(s)-\tanh k\right).
\]

É precisamente o `modularIncrement` dos pesos medidos. Em particular, ΔK′_intr(0)=−k/cosh²k. Não se trocou K₀ por um operador associado a outra base de medição.

A entropia de von Neumann tem fórmula espectral

\[
S_{\rm vN}(\rho_s)=\log(2\cosh r(s))-r(s)\tanh r(s).
\]

Sua derivada em s=0 também é −k/cosh²k. Fora de s=0, Shannon Z e entropia de von Neumann não são identificadas: a primeira é a entropia da distribuição medida, a segunda depende dos autovalores da densidade.

[INPUT] Agora escolha **s=v²t²**, com v real fixo. Não se deduz essa escolha da evolução modular, nem se identifica t com tempo físico ou parâmetro afim sem uma correspondência adicional. [DERIVED] A expansão diferenciável f(s)=f(0)+f′(0)s+o(s) dá

\[
\lim_{t\to0}\frac{\Delta S_Z(t)}{t^2}
=\lim_{t\to0}\frac{\Delta S_{\rm vN}(t)}{t^2}
=\lim_{t\to0}\frac{\Delta K_{\rm intr}(t)}{t^2}
=-\frac{k}{\cosh^2k}v^2.
\]

[REAL — escopo dos recibos lidos] A folha `MixedQuadraticGibbsResponse` prova os limites de Shannon e do incremento modular dos pesos para t→0⁻, além de positividade, normalização, tangente temporal zero, Fisher temporal zero e D_cl(q(t)∥p)/t²→0. A realização matricial, o limite bilateral escrito e a entropia de von Neumann não são contabilizados como provas Lean desta folha. A identidade ΔS_Z=ΔK_intr−D_cl explica a coincidência; não afirma D_cl=0 em t≠0.

## 3. Finitos sítios distintos: produto, sem mistura

[INPUT] Fixe um perfil canônico `P : SiteProfile`, um conjunto finito F de sítios distintos e, em cada j∈F, uma orientação com k_j>0. Cada sítio tem seu W_j=X_j+Z_j e s_j=v_j²t². A exigência de sítios distintos importa: repetir operações não comutantes no mesmo sítio não produz a fatorização abaixo.

[DERIVED] Em um prefixo que contém F, a densidade de referência é D_N=⊗_{j=0}^N ρ_{0,j}. Os pesos `towerW` são exatamente produtos dos `siteW`; `tState` é a soma diagonal ponderada por esses produtos. Seu produto GNS é `tInner(a,b)=tState(a†b)`. As inclusões `towerStep` acrescentam a identidade e preservam o estado por `tState_towerStep`.

Defina V_F=∑_{j∈F}s_jW_j, atuando em seus respectivos fatores. É auto-adjunto e limitado, com ‖V_F‖≤√2∑_{j∈F}|s_j|. Operadores em fatores distintos comutam. Assim,

\[
e^{\log D_N+V_F}
=\bigotimes_{j\in F}e^{\log\rho_{0,j}+s_jW_j}
\otimes\bigotimes_{j\notin F,\,j\le N}\rho_{0,j}.
\]

A normalização também fatora, e a densidade normalizada é o produto das ρ_{s_j,j} com os sítios não perturbados. A medição conjunta usa E_𝐢=⊗_{j∈F}E_{j,i_j}, com 2^{|F|} resultados. Portanto

\[
Q_t(\mathbf i)=\prod_{j\in F}q_{j,t}(i_j),\qquad
P_F(\mathbf i)=\prod_{j\in F}p_j(i_j).
\]

Somar sobre os outros índices produz marginal q_{j,t}. Usando log∏q_j=∑log q_j e a normalização dos fatores, segue exatamente

\[
S(Q_t)=\sum_jS(q_{j,t}),\qquad
\Delta K_{P_F}(Q_t)=\sum_j\Delta K_{p_j}(q_{j,t}).
\]

O mesmo vale para a entropia de von Neumann do produto finito, por seus autovalores produto. Logo o coeficiente comum é

\[
-\sum_{j\in F}\frac{k_j}{\cosh^2k_j}v_j^2.
\]

A folha canônica `FiniteEntropyAlgebra` contém o caso binário `finiteEntropy_product`; iterá-lo dá a identidade finita. Esta nota apresenta a aplicação ao estado conjunto como [DERIVED]. A ponte Gibbs calcula formalmente a soma das respostas, sem declarar que construiu esse tensor produto matricial em Lean. Uma mistura rotulada teria pesos de mistura e outro cálculo de entropia; não é o estado aqui usado.

## 4. Por que esse produto é a perturbação de Araki da mesma torre

[DERIVED] A identificação com o GNS canônico pode ser construída diretamente. No prefixo finito, envie a classe de a ao vetor aD_N^{1/2} no espaço de Hilbert–Schmidt. Seu produto interno é

\[
\operatorname{Tr}[(aD_N^{1/2})^*(bD_N^{1/2})]
=\operatorname{Tr}(D_Na^*b)=\operatorname{tInner}(a,b).
\]

A inclusão a↦a⊗I vira aD_N^{1/2}↦aD_N^{1/2}⊗ρ_{0,N+1}^{1/2}. Essas isometrias compatíveis estendem-se à completude da torre. Um prefixo e sua cauda fornecem, assim, a decomposição H≃HS(prefixo)⊗H_cauda, Ω=D_N^{1/2}⊗Ω_cauda. Ela vem da forma produto concreta; não supõe um traço global no fator.

Na primeira componente, o operador modular é Δ_N=L_{D_N}R_{D_N^{-1}}. Seus autovalores nas unidades matriciais são as razões dos pesos, em acordo com `flowLevel` e a ação modular canônica. O fluxo total fatora pelo fluxo da cauda; sua implementação fixa Ω_cauda. Por isso L_cauda Ω_cauda=0, onde L_cauda=log Δ_cauda, e

\[
\log\Delta+L_{V_F}
=\left(L_{\log D_N+V_F}-R_{\log D_N}\right)\otimes I
+I\otimes L_{\rm cauda}.
\]

As partes atuam em fatores distintos e comutam fortemente. A primeira é limitada. O cálculo espectral aplicado a Ω dá

\[
\exp\!\left(\frac{\log\Delta+L_{V_F}}2\right)\Omega
=e^{(\log D_N+V_F)/2}D_N^{1/2}e^{-(\log D_N)/2}
\otimes\Omega_{\rm cauda}
=e^{(\log D_N+V_F)/2}\otimes\Omega_{\rm cauda}.
\]

Este cálculo também demonstra o domínio de Ω nessa especialização: a ação exponencial da cauda sobre seu vetor é a identidade, e o fator do prefixo é finito. A norma quadrada do vetor é Tr e^{log D_N+V_F}, estritamente positiva. Após normalizar, sua restrição ao prefixo é exatamente a densidade produto da seção 3; o estado da cauda permanece inalterado. Não se deduz que a álgebra inteira possua densidade ou traço globais.

[KNOWN aplicado + DERIVED na especialização] O construtor de perturbação limitada de Araki usa esse vetor na convenção local +V. O Hamiltoniano relativo do artigo tem sinal −V, com correção escalar após normalização. A aplicação geral já está explicitada em `ESTADO_ARAKI_20260909/DEDUCAO_ESTADO_PERTURBADO_ARAKI.md`; aqui se calculou seu valor para a perturbação finita. A existência do estado fiel normal é, portanto, a da mesma construção. [Araki, 1973, §§1 e 4](https://ems.press/journals/prims/articles/2638).

Esta identificação finita não formaliza novamente todo o construtor analítico de Araki. Também não transfere automaticamente a fatorização a uma perturbação com termos entre sítios: esses termos podem criar correlações e exigem outro cálculo.

## 5. Orientação, sítio tracial e disponibilidade no perfil

[INPUT + DERIVED] Se p<1/2 na base original, k₀=(1/2)log(p/(1−p))<0. Use Z′=−Z, X′=X e k=−k₀>0. Isso equivale a trocar os vetores da base por conjugação com X, pois XZX=−Z. Então ρ₀=e^{kZ′}/(2cosh k), W=X′+Z′=X−Z na base original e E′_±=(I±Z′)/2. O projetor denominado + corresponde agora ao peso maior 1−p. Com essa escolha explícita de observáveis e rótulos, todas as fórmulas anteriores se aplicam. Não se manteve W=X+Z na base original enquanto se alterou silenciosamente o sinal de k.

[DERIVED] No sítio tracial p=1/2, k=0 e ρ₀=I/2. O gerador K₀=log2·I tem incremento zero para qualquer densidade. Para W=X+Z, o limite contínuo da fórmula dá q₊(s)=(1+tanh(√2s)/√2)/2. Com s=v²t², ΔS_Z é de ordem t⁴ e o coeficiente dividido por t² é zero; o mesmo vale para S_vN. A folha mista pede k>0 e não afirma cobrir esse caso. O caso tracial é um controle escrito, não um setor com coeficiente positivo nessa ordem.

`SiteProfile` exige somente 0<P.w j<1. Ele pode ser inteiramente tracial ou ter apenas poucos sítios não traciais. Portanto uma família física de m setores positivos requer **m sítios distintos não traciais disponíveis**, ou outra realização explicitada. Não decorre de um perfil arbitrário que essa quantidade exista.

## 6. Controle transversal: três quantidades diferentes

[DERIVED] Considere agora outro protocolo: ρ_s^X∝exp(kZ+sX), medição X, s=vt. Ponha r_X=√(k²+s²) e χ(k)=tanh|k|/|k|, com χ(0)=1. A magnetização X é s tanh r_X/r_X, prolongada continuamente em k=s=0, exatamente como `transverseMagnetization`.

[REAL — folha transversal e recibo lidos] A distribuição X de referência é (1/2,1/2); seu Fisher temporal é χ²v², seu incremento modular **medido nessa distribuição uniforme** é identicamente zero e

\[
\Delta S_X/t^2\longrightarrow-\chi(k)^2v^2/2.
\]

[DERIVED — precisão indispensável] Para k≠0, isso não zera o incremento do gerador intrínseco K₀=log(2cosh k)I−kZ. A magnetização Z do estado é k tanh r_X/r_X. Expandindo em s=0, obtém-se

\[
\Delta K_{\rm intr}/t^2\longrightarrow
\tfrac12\bigl(\chi(k)-\operatorname{sech}^2k\bigr)v^2,
\qquad
\Delta S_{\rm vN}/t^2\longrightarrow
-\tfrac12\operatorname{sech}^2k\,v^2.
\]

Ambas as fórmulas estendem-se ao caso k=0. O normalizador relativo é Z(s)=cosh r_X/cosh k, e (log Z)″(0)=χ(k). Assim, a susceptibilidade de Kubo–Mori/BKM nessa parametrização é χv²; a informação de Fisher da medição X é χ²v². A entropia relativa quântica tem coeficiente χv²/2, consistente com ΔK_intr−ΔS_vN. Essas quantidades só coincidem nos casos apropriados; não se troca χ por χ².

O ganho do protocolo misto quadrático é específico: mede em uma base que diagonaliza K₀ e possui tangente temporal nula, de modo que Shannon, energia intrínseca e entropia quântica coincidem **na ordem necessária**, embora os estados intermediários sejam não comutantes.

## Evidência e alcance

O manifesto acompanha hashes e tamanhos lidos agora, contagens dos recibos e âncoras das fontes. Os dois recibos informam compilação de folha e importador contra biblioteca aprovada, com dependências diretas medidas; não significam recompilação transitiva integral. Esta subtarefa verifica os arquivos e lê esses resultados, sem relançar Lean ou executar/importar `um.py`.

As escolhas de W, medição, orientação, relógio e sítios pertencem ao protocolo [INPUT]. A fatorização e a identificação de densidades são [DERIVED], apoiadas no GNS produto concreto e na aplicação de Araki [KNOWN]. Os limites dos pesos são [REAL — Lean no escopo indicado]. A lei de área, a seleção física do registro, a reconstrução experimental com precisão finita e o alcance quântico geral não são demonstrados por esta realização.
