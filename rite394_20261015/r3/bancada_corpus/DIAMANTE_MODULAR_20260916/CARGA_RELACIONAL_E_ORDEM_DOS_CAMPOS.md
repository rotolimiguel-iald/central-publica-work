# A carga candidata: dressing linear, ordem dos campos e o que ainda precisa ser construído

16/09/2026. [DERIVED — cálculo escrito, não Lean]. Usa a tensão da fonte066 e o extrator local088; não cria um segundo extrator e não define por decreto a carga física completa do diamante.

## 1. A primeira variação pode ser tornada física sem inventar outra fonte

Para a ação sigma existente,

\[
T_{\mu\nu}=c\left(W_{\mu\nu}-\tfrac12Xg_{\mu\nu}\right),
\quad W=\phi^*\gamma,\quad X=g^{-1}:W,\quad \bar X=-3/a^2.
\]

Denote a perturbação por u=(h,χ), reservando ξ para o vetor do diamante. A fonte088 já fornece ζ=F(u), FK_g=Id e P u=u−K_gζ=(H,0), com δX[H,0]=0. Por naturalidade tensorial,

\[
\delta T[K_gv]=\mathcal L_v\bar T.
\]

Logo a combinação local

\[
\mathfrak t[u]:=\delta T[u]-\mathcal L_{F(u)}\bar T
=\delta T[Pu]
\]

é invariante sob u↦u+K_gv. Na imagem de P temos δφ=0, δW=0 e δX=0, portanto

\[
\boxed{\mathfrak t_{\mu\nu}=\frac{3c}{2a^2}H_{\mu\nu}.} \tag{1}
\]

É uma identidade local linear off-shell nas perturbações, no fundo especificado e no interior onde F existe. A expressão geral sob δW=δX=0 é −c X̄H/2; o coeficiente 3c/(2a²) usa este fundo. Os fatores de fundo não são operadores adicionais. Isso constrói a primeira variação vestida da tensão; não equivale a construir todos os produtos renormalizados da tensão completa.

As fontes exatas são [066, §3](../QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md) e [088, §§5–6](../RELOGIOS_RELACIONAIS_FUNDO_FISICO_088_20260910/RELOGIOS_X_SIGMA_E_RETRACAO_DE_JATOS.md). A existência de F não deve voltar a aparecer como uma lacuna desta etapa.

## 2. Uma carga linear não é o gerador modular quase livre

Integrar (1) com um teste geométrico fixado produz um funcional linear de H. Quando esse smearing define um observável da álgebra física, ele tem a forma Φ(v). No contínuo deve-se justificar eventual limite à fatia e bordo; a afirmação seguinte vale diretamente para testes suaves compactos.

Fixe as convenções CCR

\[
W(v)W(f)=e^{-i\sigma(v,f)/2}W(v+f),\quad W(v)=e^{i\Phi(v)}.
\]

As relações de Weyl dão sem cálculo de domínios

\[
\boxed{e^{is\Phi(v)}W(f)e^{-is\Phi(v)}
=e^{-is\sigma(v,f)}W(f).} \tag{2}
\]

Isso é um deslocamento afim do campo, não um transporte linear homogêneo dos testes. No estado quase livre centrado067,

\[
\omega(W(f))=e^{-\mu(f,f)/2}>0.
\]

A invariância desse estado por (2), para todo s real, exigiria σ(v,f)=0 para todos os testes regionais f. Portanto uma carga puramente linear com ação não trivial na região não pode implementar o fluxo modular dessa referência centrada. Se σ(v,·)=0 na região, sua ação ali é trivial; não se conclui v=0 globalmente.

O fluxo modular construído anteriormente age como W(v)↦W(S_sv), com S_s=δ_D^(is) sobre o subespaço real fechado L(D) de uma partícula. Aqui v é o vetor de uma partícula associado ao teste, ou seu limite em L(D). Não foi demonstrado que S_s preserve a classe original de testes suaves compactos; a segunda quantização fornece o fluxo na álgebra de von Neumann. Seu gerador é quadrático no sentido de Fock, sujeito aos domínios próprios; uma primeira variação linear da tensão não o substitui. As fórmulas não proíbem uma carga completa que contenha termos quadráticos e outros termos necessários.

Referência de contexto, com convenções de forma simplética a ajustar: [Longo, introdução e estrutura modular de estados gaussianos](https://arxiv.org/pdf/2111.11266). A dedução curta de (2) e do teste de invariância está escrita acima.

## 3. O setor TT mostra concretamente a diferença entre as ordens

Na fatia central do diamante, ξ=f(z)∂η. Para uma perturbação puramente TT, H00=H0i=0 e o traço espacial é zero. Assim a contração de (1) com ξ e a normal de fundo se anula. Isso não diz que os gravitons não carregam energia: diz que essa primeira variação não contém a energia quadrática das flutuações TT.

Podemos calcular também um caminho explícito para o funcional **de matéria**, antes de lhe atribuir um significado físico de segunda ordem. Tome

\[
g_\varepsilon=a^2[d\eta^2-(\gamma+\varepsilon t)],\quad
\phi_\varepsilon=\mathrm{id},\quad\operatorname{tr}_\gamma t=0,
\quad \xi=f\partial_\eta,
\]

com f e a fatia fixos, I+εt positivo e t visto como endomorfismo espacial. Não se impõe que esse caminho seja uma solução não linear nem um corte relacional em segunda ordem. Nessa família,

\[
T_{00}=\tfrac c2\operatorname{tr}(I+\varepsilon t)^{-1},\quad
n^0=1/a,\quad d\Sigma=a^3\sqrt{\det(I+\varepsilon t)}\,dV_\gamma.
\]

Consequentemente,

\[
Q_{\xi}^{\rm matter}(\varepsilon)
=\pi ca^2\int f\,
\operatorname{tr}(I+\varepsilon t)^{-1}\sqrt{\det(I+\varepsilon t)}\,dV_\gamma.
\]

Expandindo inversa e determinante,

\[
\operatorname{tr}(I+\varepsilon t)^{-1}=3+\varepsilon^2\operatorname{tr}t^2+O(\varepsilon^3),
\quad\sqrt{\det(I+\varepsilon t)}=1-\tfrac14\varepsilon^2\operatorname{tr}t^2+O(\varepsilon^3),
\]

\[
\boxed{Q_{\xi}^{\rm matter}(\varepsilon)=Q_0+
\varepsilon^2\frac{\pi ca^2}{4}\int f\,\operatorname{tr}t^2\,dV_\gamma
+O(\varepsilon^3).} \tag{3}
\]

O coeficiente de ε² é metade da segunda derivada. O fator 1/4 inclui a variação da medida; usar só δ²T daria outro resultado. Esse termo não contém o momento TT. No sistema canônico reduzido, seu colchete com a coordenada t é zero; ele altera o momento. Portanto ele, isoladamente, tampouco é o Hamiltoniano de evolução de ondas TT.

## 4. Por que (3) não resolve a definição da carga completa

Em segunda ordem, X já varia nesse caminho: Xε=−a⁻²[3+ε² tr(t²)+…]. Assim F/P lineares não garantem que a região e os relógios físicos permaneçam fixos em segunda ordem. Lapse, shift, restrições, medida, domínio e eventual deslocamento da fatia precisam ser tratados no mesmo funcional. Em gravidade dinâmica, a carga total ainda requer as contribuições gravitacionais e de fronteira apropriadas; a tensão de matéria não é identificada com elas.

Essas distinções não são novas hipóteses acrescentadas ao gate. Elas impedem substituir objetos diferentes ao construir Kξ. O cálculo (3) fornece um controle para a futura construção, não um operador renormalizado interagente já pronto.

## 5. Entrega para o motor e próximo contrato

Não adicionar outra rotina de reconhecimento ou pinching. No fornecedor de Kξ existente, é preciso registrar qual objeto ele usa:

- tensão clássica de fundo: contribuição escalar;
- primeira variação vestida (1): campo linear, deslocamento (2);
- termo quadrático de matéria no caminho fixado (3): controle de expansão, ainda não a carga física completa;
- carga relacional/renormalizada completa: ainda por construir e confrontar com o fluxo modular.

A obrigação seguinte é derivar o funcional quadrático completo de carga no mesmo quociente físico e na mesma região, com seu domínio, termos de fronteira e normalização. A [ação TT existente](../MODOS_TENSORIAIS_EXATOS_20260909/ACAO_TT_E_MODOS_EXATOS.md) já contém a cinética; não é necessário pedir novamente uma ação. A passagem de sua energia reduzida à carga específica de um vetor conforme do diamante precisa ser demonstrada.

Nada nesta nota calcula R1, o centralizador físico ou a completude UV. Ela determina a primeira variação vestida e evita comparar o gerador modular quadrático a uma carga de ordem errada.


## Conferência independente e controles

Goodall conferiu independentemente as duas derivações e a ação CCR, com parecer favorável. Ressaltou o smearing congelado, o domínio interior de F, a condição de admissibilidade do campo suavizado e a distinção entre coeficiente de epsilon² e segunda derivada. Essas condições estão explícitas no texto. O parecer não constrói a carga completa ou seu operador renormalizado.

verify_charge_orders.py executou três perfis de métrica/perturbação e controles de fase CCR. A variação por diferenças finitas da tensão completa confirmou (1); a expansão de inversa vezes determinante confirmou o fator 1/4 de (3) e recusou sua substituição pelo fator obtido omitindo a medida. Os controles são finitos, não a quantização da carga regional.
