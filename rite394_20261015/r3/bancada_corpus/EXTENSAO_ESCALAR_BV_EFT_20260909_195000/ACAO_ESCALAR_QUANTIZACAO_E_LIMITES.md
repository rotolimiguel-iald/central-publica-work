# A mesma fonte escalar: ação, realização quântica e rota BV/EFT

09/09/2026. Análise própria a partir da cópia integrada de 83 módulos e das fontes canônicas indicadas no manifesto. Somente arquivos novos nesta pasta. Nenhum `um.py` executado/importado; nenhuma folha congelada alterada. Esta nota não atribui aprovação a terceiros.

**[DERIVED] A fonte Gibbs positiva admite uma ação escalar mínima explícita e uma realização como diferença de expectativas de um tensor quântico renormalizado.** Isso fornece objetos concretos para a próxima etapa. A ação é uma escolha [INPUT/POSTULATE], e a quantização perturbativa da gravidade acoplada exige os contratos adicionais abaixo. Não se deduz uma teoria UV completa dessa escolha.

## 1. O que já ultrapassou as ondas planas

[REAL — fontes existentes lidas; sem nova compilação] No overlay da cópia83:

- `GeneralLinearizedGauge.general_smooth_einstein_gauge_invariance` cobre perturbações e parâmetros gauge suaves gerais em Minkowski. Não é apenas um teste em um modo plano.
- `MetricEinsteinVariation.metric_einstein_first_variation` prova a derivada efetiva de G[g+th] para campos suaves e métrica invertível em um aberto. Não recebe essa derivada como hipótese.
- `ScalarEinsteinLieNaturality.metric_lie_einstein_naturality` identifica a variação por ℒ_Vg com ℒ_VG[g] em fundo curvo geral. Em um fundo fora das equações, ℒ_VG não precisa ser zero; naturalidade não deve ser renomeada como anulamento gauge universal.
- `FiniteEinsteinNaturality.einstein_finite_coordinate_transformation` trata mudanças suaves finitas de coordenadas e a covariância do tensor construído.
- `ScalarStressConservation` e `FiniteCoherentSources` derivam a divergência e a conservação da fonte finita sob as equações dos covetores. `MixedGibbsGravitationalBridge.gibbs_record_source` identifica seus coeficientes com k_j/(πcosh²k_j).

O canônico `PhysicsCertificates.qgPhysicsCertificate_anomaly` é uma identidade de gauge do símbolo clássico-linear. Seu enunciado não contém laços quânticos, produtos renormalizados ou equação mestra quântica. `ContinuumTT` delimita explicitamente seu próprio controle cinético ao setor TT de ondas planas.

[REAL — busca delimitada] Os nomes exatos `EinsteinJetWard` e `TheSpectrum` não foram encontrados no texto da cópia83 nem nos caminhos de fontes Lean examinados. Eles não são tratados aqui como arquivos existentes. A busca por BRST, Batalin, antifield e master equation na cópia83 não localizou um complexo BV ou prova de anomalia interagente. A varredura pertinente de densidades/ações não encontrou a derivação variacional da fonte Gibbs; `MetricEinsteinVariation` varia o tensor, não uma ação Einstein–Hilbert integrada. Isso delimita o acervo consultado, sem afirmar ausência em todo arquivo do computador.

## 2. Ação explícita para exatamente a fonte construída

[INPUT/POSTULATE — correspondência escolhida] Considere uma variedade lorentziana 4D orientada, com assinatura (+---), e campos escalares reais φ_j, j em conjunto finito J. Escolha η>0 e κ_g=2π/η. Os parâmetros k_j>0 são constantes, com

\[
c_j=\frac{k_j}{\pi\cosh^2 k_j}>0,\qquad w_j=d\phi_j.
\]

Essa igualdade com potenciais é uma condição adicional ao contrato de covetores. Um covetor fechado admite potencial em cartas contráteis; um potencial global exige exatidão, não apenas fechamento. A hipótese de onda torna-se □_gφ_j=0.

Adote, com a convenção de curvatura que define G no kernel,

\[
S[g,\phi]=\int d^4x\,\sqrt{|\det g|}
\left[-\frac{R[g]-2\Lambda}{2\kappa_g}
+\frac12\sum_j c_jg^{ab}\partial_a\phi_j\partial_b\phi_j\right].
\]

Usam-se variações de suporte compacto no interior; uma fronteira física requer seu próprio termo de fronteira e condições. O sinal relativo foi fixado para a assinatura declarada e para obter G+Λg=κ_gT. Em convenções opostas de curvatura/assinatura, transportam-se juntos os sinais da ação e de T; não se muda apenas um deles.

[DERIVED — cálculo variacional] Escreva μ=√|det g|. Para variação da métrica inversa,

\[
\delta\mu=-\tfrac12\mu g_{ab}\delta g^{ab},\qquad
\delta S_m=\frac12\int\mu\sum_j c_j
\left(\partial_a\phi_j\partial_b\phi_j
-\tfrac12g_{ab}g^{cd}\partial_c\phi_j\partial_d\phi_j\right)\delta g^{ab}.
\]

Com T_ab=(2/μ)δS_m/δg^{ab}, recupera-se precisamente a fonte do registro Gibbs. Variar φ_j e integrar por partes dá δS_m=−∫μc_j□φ_j δφ_j. A variação de ∫μR é ∫μG_abδg^{ab} mais divergência. As equações estacionárias são, portanto,

\[
G_{ab}+\Lambda g_{ab}=\kappa_gT_{ab},\qquad \Box_g\phi_j=0.
\]

Essa dedução realiza o mesmo par de equações, mas não deriva a ação do seletor nem prova a lei de área. A conservação fora das equações de matéria é a identidade

\[
\nabla^aT_{ab}=\sum_jc_j(\Box_g\phi_j)\partial_b\phi_j.
\]

A transformação invertível σ_j=√c_j φ_j normaliza os termos cinéticos. Assim a positividade elimina sinais cinéticos escalares errados nesta ação de duas derivadas. Sem fixar como φ_j é medido, o valor c_j isolado pode ser absorvido na normalização do campo; não é automaticamente uma previsão de amplitude observável.

## 3. Uma realização quântica exata da fonte como incremento

[INPUT] Fixe um fundo globalmente hiperbólico g e os potenciais suaves globais acima. Considere o campo quântico escalar livre, mínimo e sem massa para cada σ_j; escolha um estado Hadamard centrado ω₀. Essas são entradas de uma realização de QFT no espaço-tempo, distintas da realização por qubits da torre.

[DERIVED] No álgebra CCR, o deslocamento

\[
\alpha_\sigma(\widehat\sigma_j(f))
=\widehat\sigma_j(f)+\int\sigma_j f\,d\mu_g\,I
\]

preserva os comutadores e o adjunto. Preserva a equação de campo porque □σ_j=0 e f possui suporte compacto. Sua inversa é α_{−σ}; logo ω_σ=ω₀∘α_σ é um estado. Não é necessário supor que esse automorfismo tenha implementador unitário na representação global escolhida.

Como ω₀ é centrado, a diferença de duas funções de dois pontos é σ_j(x)σ_l(y). Ela é suave; a singularidade Hadamard permanece a mesma. Para o tensor mínimo de duas derivadas, aplicar o mesmo operador de separação de pontos às duas funções e subtrair as expectativas dá exatamente

\[
\boxed{\langle\widehat T_{ab}\rangle_{\omega_\sigma}^{\rm ren}
-\langle\widehat T_{ab}\rangle_{\omega_0}^{\rm ren}
=\sum_j c_j\left(\partial_a\phi_j\partial_b\phi_j
-\tfrac12g_{ab}|d\phi_j|_g^2\right).}
\]

Termos de renormalização puramente geométricos, iguais nas duas prescrições, cancelam. Não se alterou o acoplamento mínimo para um tensor melhorado com termo Rφ²; essa seria outra ação e outra fonte. O tensor à direita é conservado pela equação de onda e coincide com o registro já reconstruído.

Esta igualdade é uma dedução escrita a partir dos CCR e da definição renormalizada do tensor. A construção covariante de produtos de Wick e as condições de conservação para escalares em dimensão maior que dois possuem fundamentação primária em [Hollands–Wald, 2005](https://arxiv.org/abs/gr-qc/0404074). A aplicação aqui é ao setor livre mínimo e a uma diferença entre estados; não declara já quantizados os grávitons ou as interações completas.

O valor absoluto ⟨T̂⟩_ω₀ pode ser não nulo. Para usar Einstein semiclassico seria necessário também tratar esse termo e os contratermos gravitacionais; ele não se torna Λg em todo fundo. Positividade nula da diferença clássica não implica positividade pontual de toda expectativa quântica. A realização não identifica o estado CCR com o estado Gibbs da torre: falta um mapa físico entre as duas álgebras/observáveis.

## 4. BRST clássico e ação BV mínima do modelo escolhido

[DERIVED — álgebra escrita] Introduza um fantasma vetorial ímpar C^a, com número de fantasma 1. Use derivação ímpar à esquerda s, com s∂=∂s e regra de Leibniz graduada. Uma convenção consistente é

\[
sg_{ab}=C^c\partial_cg_{ab}+g_{cb}\partial_aC^c+g_{ac}\partial_bC^c,
\quad s\phi_j=C^a\partial_a\phi_j,
\quad sC^a=C^b\partial_bC^a.
\]

Por exemplo,

\[
s^2\phi_j=(sC^a-C^b\partial_bC^a)\partial_a\phi_j
-C^aC^b\partial_a\partial_b\phi_j=0.
\]

O último termo anula por anticomutação dos fantasmas e simetria das derivadas. Em s²C, os dois termos com primeiras derivadas cancelam após trocar índices, e o termo com segundas derivadas anula pelo mesmo argumento. Para um tensor par A, s(ℒ_CA)=ℒ_{sC}A−ℒ_C(sA), enquanto ℒ_C²A=ℒ_{C^b∂_bC}A. Portanto s²g=0 fora das equações de movimento. Substituir os fantasmas por números reais comutantes destruiria esta prova.

A densidade escalar covariante satisfaz sℒ=∂_a(C^aℒ); com suporte compacto, sS=0. Acrescente os antifields g*, φ_j*, C*, de paridades opostas e números de fantasma −1, −1, −2. Escolhendo o antibracket de modo que (S_BV,Φ)=sΦ,

\[
S_{BV}=S+\int\left[g^{*ab}sg_{ab}
+\sum_j\phi_j^*s\phi_j+C_a^*sC^a\right]d^4x.
\]

Invariância de S e fechamento fora das equações dão (S_BV,S_BV)=0. A identidade de Jacobi graduada implica s_BV²=0 também nos antifields. Isto é a equação mestra **clássica** deste modelo, não um controle de anomalias quânticas. Convenções de antibracket à direita podem trocar os sinais de ghost/antifield; todas as fórmulas precisam ser transportadas em conjunto. A classificação de referência usa explicitamente a regra graduada em [Barnich–Brandt–Henneaux, §2](https://arxiv.org/pdf/hep-th/9505173).

## 5. Construção perturbativa acoplada: obrigações verificáveis

[INPUT/OPEN — implementação matemática do modelo acoplado] A sequência aplicável é:

1. Escolher um fundo globalmente hiperbólico (ḡ,φ̄) que satisfaça as equações da seção 2 e especificar suportes/condições de Cauchy. A existência de um registro lorentziano em uma carta não fornece automaticamente esse fundo global.
2. Expandir g=ḡ+εh e φ=φ̄+ψ. Fixar gauge de de Donder para h e acrescentar o par trivial s C̄=B, sB=0. A matriz principal das equações de h e ψ deve ser calculada: os acoplamentos por ∂φ̄ entram em ordem inferior; os operadores de onda e de ghost devem ter propagadores avançado/retardado.
3. Construir o complexo livre e suas funções de dois pontos Hadamard compatíveis com BRST. A positividade do espaço físico é a positividade da cohomologia do BRST livre, não a positividade do espaço auxiliar com ghosts. Os resultados TT existentes são dados úteis, mas não verificam isso para todo fundo.
4. Quantizar a álgebra de funcionais apropriada e construir produtos temporalmente ordenados renormalizados. A interação contém os vértices gravitacionais e h–ψ, mesmo sem potencial φ⁴. Deve-se usar a equação mestra renormalizada e sua anomalia local, não um Δ_BV formal avaliado em campos coincidentes sem definição. O tratamento primário está em [Fredenhagen–Rejzner, §§3–4](https://arxiv.org/abs/1110.5232).
5. Satisfazer a equação mestra quântica por escolhas admissíveis de contratermos, ordem a ordem, e construir as observáveis físicas na cohomologia. Depois verificar o transporte dos dados geométricos/escalares que o seletor registra. Recuperar campos em coordenadas não torna automaticamente esses campos observáveis invariantes por difeomorfismos.

[KNOWN — alcance da referência] [Brunetti–Fredenhagen–Rejzner, 2016](https://arxiv.org/html/1306.1058v4) constrói a rota localmente covariante e renormalizada para **gravidade pura**. Sua conclusão, §6, apresenta a extensão a matéria como expectativa. Portanto esse artigo não é usado aqui como certificado pronto do sistema Einstein–escalares. A rota acoplada acima tem contratos explícitos a verificar; a construção de estados positivos também tem hipóteses próprias.

## 6. O alcance preciso do controle de anomalias

[KNOWN aplicado/DERIVED na especialização] O modelo escolhido tem apenas difeomorfismos, escalares reais neutros e gravidade 4D, com ação cinética regular. Não possui fatores gauge abelianos nem matéria quiral. Na classificação local de [Barnich–Brandt–Henneaux, §§2, 9 e 10.4](https://arxiv.org/pdf/hep-th/9505173), as anomalias candidatas são classes H^{1,4}(s|d). Para esse setor mínimo, não há a descendência gravitacional quiral de grau seis nem os casos topológicos excepcionais das dimensões indicadas no artigo. Os potenciais escalares tomam valores em ℝ, sem nova topologia de alvo. A especialização fornece ausência de obstrução local dessa classe, com as hipóteses de regularidade da análise de jatos/BV e sem fronteiras.

O uso perturbativo é condicional ao princípio de ação quântica/localidade: se a primeira quebra A_L da equação mestra é um cociclo local, sua trivialidade significa A_L=sB_L+dC_L. Um contratermo −ℏ^L B_L remove essa quebra; a indução exige a mesma verificação nas ordens seguintes e espaço de contratermos suficiente. A classificação não é um recibo Lean nem uma amplitude calculada para a TGL.

A ausência de anomalia local de difeomorfismo não exclui anomalia de traço/Weyl, questões globais, efeitos de fronteira ou anomalias de setores adicionados depois. O tensor mínimo não tem simetria Weyl clássica geral que possa ser presumida exata. Para a distinção dimensional das anomalias gravitacionais quirais, a fonte primária é [Alvarez-Gaumé–Witten, 1984](https://collaborate.princeton.edu/en/publications/gravitational-anomalies/).

## 7. EFT exige mais termos que a ação mínima

[DERIVED + KNOWN] Em unidades naturais, κ_g tem dimensão de comprimento². A expansão com E√κ_g≪1 e curvaturas pequenas em unidades de κ_g é uma rota de baixa energia. Ela permite cálculo ordem a ordem; não prova convergência da série nem controle em energia arbitrária. [Donoghue, 1994](https://arxiv.org/abs/gr-qc/9405057) fundamenta a separação entre contribuições de baixa energia e coeficientes dependentes da física de alta energia.

Laços exigem uma ação efetiva com todos os operadores locais permitidos pelas simetrias adotadas. Exemplos incluem R², R_abR^{ab}, combinações Riemann², R(∂σ)², R_ab∂^aσ∂^bσ e operadores quarticos de derivadas dos escalares; a base independente deve reduzir integrações por partes, identidades e redefinições de campos. Se as translações constantes dos escalares forem mantidas como simetrias, isso também precisa constar da prescrição.

O resultado de [Gomis–Weinberg, 1996](https://arxiv.org/abs/hep-th/9510087) distingue absorver divergências em uma família infinita de operadores compatíveis com BRST de renormalizabilidade por contagem de potências com finitos parâmetros. É a primeira noção que interessa à EFT. Os coeficientes desses operadores não são determinados apenas pelos k_j.

Consequentemente, G+Λg=κ_gT é a equação líder da ação mínima escolhida. Correções quânticas acrescentam tensores de curvatura, correções de matéria e contribuições não locais. Exigir que a equação mínima continue exata após toda renormalização seria uma condição nova, ainda sem demonstração. Não se conclui uma rota UV única, estabilidade não perturbativa ou ausência universal de ghosts ao ressomar termos de derivadas altas.

## 8. Próxima folha concreta recomendada

**`ScalarMatterDensityVariation.lean`**, sem introduzir BRST abstrato apenas como registro de hipóteses.

Defina a densidade pontual, para dados finitos já usados:

\[
\mathcal L_m(g,w,c)=\frac{\operatorname{metricVolumeDensity}(g)}2
\sum_jc_j\operatorname{tensorQuad}(g^{-1},w_j).
\]

Meta central: para g e h simétricas e g invertível, provar `HasDerivAt` da função t↦ℒ_m(g+th,w,c), com valor

\[
-\frac{\sqrt{|\det g|}}2
\sum_{a,b}(g^{-1}T(g,w,c)g^{-1})_{ab}h_{ab},
\quad T=\sum_jc_j\operatorname{covectorStress}(g,g^{-1},w_j,1).
\]

O resultado não deve receber a variação de T ou da densidade como campo. A prova usa `matrix_inverse_first_variation`, mais um lema a demonstrar:

\[
\frac d{dt}\sqrt{|\det(g+th)|}\Big|_0
=\tfrac12\sqrt{|\det g|}\operatorname{tr}(g^{-1}h).
\]

Este último pode vir da fórmula finita do determinante e da adjugada, seguida de continuidade do sinal e derivada da raiz; não foi localizado um lema Mathlib pronto com o nome presumido. Uma segunda derivada em w+t z deve dar μ∑c_j g^{-1}(w_j,z_j), ligando a variação escalar à integração por partes escrita na seção 2.

Finalmente especializar c_j=k_j/(πcosh²k_j) e identificar T com `gibbs_record_source`. Isso paga uma origem variacional concreta da fonte existente. A derivação de Euler–Lagrange para a integral completa, o complexo graduado e a quantização acoplada permanecem etapas posteriores, com seus enunciados próprios.

As identidades escritas nesta nota são [DERIVED]; a ação e a correspondência com campos são [INPUT/POSTULATE]; a literatura aplicada é [KNOWN] dentro de seu escopo. Não há nova prova Lean, mudança de gate ou afirmação de gravidade quântica resolvida nesta entrega.
