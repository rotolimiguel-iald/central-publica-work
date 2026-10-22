# Reconstrução gravitacional geral: derivação condicional e dados ainda ausentes

## Resultado desta etapa

**[DERIVED]** É possível passar da condição de Clausius em TODOS os horizontes locais à equação tensorial de Einstein numa variedade lorentziana geral, sem o ansatz particular de `EmergentEinstein.lean`, sob as hipóteses abaixo. **[REAL — Lean]** A etapa algébrica para um tensor simétrico arbitrário em quatro dimensões foi verificada em `GeneralNullCone.lean`.

**[OPEN]** Não foi reconstruída uma variedade lorentziana física a partir de `SiteProfile`, M, Ω, J e Δ. A identificação JS=Δ¹ᐟ² organiza a análise modular; ela não fornece por si só dimensão, localização, métrica e lei de entropia de área. Este documento distingue a derivação tensorial condicional da realização dessas hipóteses pela TGL.

## 1. O dado modular ainda não determina a métrica

O parâmetro de Δ^{it} é um parâmetro de automorfismos. Associá-lo a transformações de regiões espaciais exige uma família localizada de álgebras e relações entre suas ações modulares. Uma única álgebra com um estado não especifica essas regiões.

[KNOWN] Buchholz, Dreyer, Florig e Summers estudam [Geometric Modular Action and Spacetime Symmetry Groups](https://arxiv.org/abs/math-ph/9805026). Sua reconstrução de ações geométricas envolve condições adicionais sobre a ação modular e estruturas ordenadas. A existência da polar, isoladamente, não satisfaz essas condições.

Há ainda uma ambiguidade mesmo depois de obter cones nulos. Em ℝ⁴, compare

\[
g_0=dt^2-dx^2-dy^2-dz^2,\qquad g_1=e^{2t}g_0.
\]

Como e^{2t}>0, ambas têm os mesmos vetores nulos em todos os pontos. Contudo g₀ é plana e g₁ tem escalar R=−6e^−2t na convenção de curvatura registrada no script. Não são isométricas. **[REAL]** O cálculo de Christoffel, Ricci e R foi feito simbolicamente em `check_modular_geometry.py`; não é uma inferência numérica.

O exemplo mostra que cones, sozinhos, não fixam a escala conforme ou a curvatura. Não demonstra impossibilidade de reconstrução a partir de dados modulares mais ricos. Se a proposta já oferece observáveis adicionais que fixam essa escala, é preciso demonstrar a ligação.

Analogamente, uma matriz real positiva C não se torna lorentziana por congruência: vᵀ(BᵀCB)v=(Bv)ᵀC(Bv)≥0. Uma matriz dissipativa positiva não paga uma direção temporal negativa apenas por mudança real de base. A estrutura que introduz essa assinatura precisa ser identificada. Os quatro componentes usados abaixo são [INPUT], não uma dedução de ω(I)=1.

## 2. Hipóteses explícitas para a derivação geral

Trabalhe numa variedade conexa, suave, lorentziana de dimensão quatro, com conexão de Levi-Civita e regularidade suficiente para Raychaudhuri e Bianchi. Assuma:

1. **[INPUT]** Um tensor de energia-momento simétrico e conservado, ∇ᵃT_ab=0, com significado físico definido independentemente da equação a obter.
2. **[INPUT]** Para toda direção nula em todo ponto, horizontes locais em equilíbrio no ponto: expansão e cisalhamento inicialmente nulos e congruência sem torção.
3. **[INPUT]** Temperatura local de Unruh T_U=ℏa/(2π), com aceleração a>0, e identificação do fluxo de calor com o fluxo de energia de boost.
4. **[INPUT]** Entropia de horizonte δS=ηδA com η>0 constante universal e equilíbrio de Clausius δQ=T_UδS para todos esses horizontes.

Unidades c=k_B=1. Esses dados não são extraídos automaticamente da auto-adjunticidade de JS. Em particular, uma variação de entropia modular não foi identificada aqui com área geométrica.

## 3. Raychaudhuri e a contração nula

Para um gerador afim k, com parâmetro λ=0 no ponto de equilíbrio, a equação de Raychaudhuri e θ(0)=σ(0)=0 dão, à primeira ordem,

\[
\theta(\lambda)=-\lambda R_{ab}k^ak^b+O(\lambda^2),\qquad
\delta A=-\int\lambda R_{ab}k^ak^b\,d\lambda\,dA+\text{ordens superiores}.
\]

Na porção passada λ<0, use o gerador de boost χ=−aλk. Então

\[
\delta Q=-a\int\lambda T_{ab}k^ak^b\,d\lambda\,dA.
\]

Inserir T_U e δS em Clausius, encolher o segmento e o elemento transversal e comparar os coeficientes locais produz, para todo k nulo,

\[
(R_{ab}-\kappa T_{ab})k^ak^b=0,\qquad
\kappa=\frac{2\pi}{\hbar\eta}.
\]

O caráter local e a exigência para TODAS as direções são essenciais. Uma identidade integrada sobre apenas uma trajetória não é essa hipótese. A expansão é usada no limite infinitesimal; não se exige que os termos de ordem superior desapareçam em segmentos finitos.

## 4. Rigidez do cone sem ansatz de métrica

Se E_ab é simétrico e E(k,k)=0 para todo k nulo num espaço lorentziano de dimensão quatro, então E=f g.

Prova: escolha um referencial ortonormal de assinatura (+−−−). Os testes k=e₀+eᵢ e k=e₀−eᵢ dão E₀ᵢ=0 e Eᵢᵢ=−E₀₀. Para i≠j espaciais, use k=5e₀+3eᵢ+4eⱼ, que é nulo. A parte diagonal já se anula, restando 24Eᵢⱼ=0. Logo todos os termos mistos desaparecem e E=E₀₀g. Como a afirmação é tensorial, independe do referencial escolhido.

**[REAL — Lean]** `general_null_cone_rigidity` realiza exatamente esses nove testes nas dez componentes independentes e conclui a identidade das formas quadráticas para TODO vetor. Não fixa previamente um perfil q(t) nem componentes de Ricci. **[OPEN — Lean]** O transporte desse lema a campos tensoriais sobre uma variedade, a construção de referenciais e a etapa diferencial seguinte não estão formalizados neste arquivo.

Aplicado a E=Ric−κT, o lema dá

\[
R_{ab}-\kappa T_{ab}=f g_{ab}.
\]

## 5. Bianchi e a constante cosmológica

A identidade de Bianchi contraída é ∇ᵃR_ab=(1/2)∂_b R. Pela compatibilidade métrica, conservação de T e constância de κ, segue

\[
\partial_b f=\tfrac12\partial_b R,\qquad
\partial_b(R/2-f)=0.
\]

A conexidade permite escrever f=R/2−Λ, com Λ constante. Portanto

\[
\boxed{R_{ab}-\tfrac12 Rg_{ab}+\Lambda g_{ab}=\kappa T_{ab}.}
\]

Se, adicionalmente, η=1/(4ℏG), então κ=8πG. A álgebra determina esse coeficiente A PARTIR da normalização de entropia de área; não determina G a partir do estado normalizado. Λ permanece constante de integração, a fixar por condições físicas adicionais. Em componentes conexas distintas, as constantes podem diferir.

**[KNOWN]** Essa rota termodinâmica é a de [Ted Jacobson, Thermodynamics of Spacetime: The Einstein Equation of State](https://arxiv.org/abs/gr-qc/9504004). Não reivindicamos uma nova derivação histórica. O avanço formal desta bancada é a etapa de rigidez tensorial, aplicável além do ansatz anterior. A derivação recupera uma equação gravitacional sob hipóteses; não fornece uma teoria quântica completa de gravidade.

## 6. O que precisa ser construído a partir da torre

| Ponte | Entrega necessária | Estatuto nesta bancada |
|---|---|---|
| Análise modular | S fechado, polar, grupo modular | Provas Lean parciais e demonstração analítica completa para a torre produto; ver documento de JS |
| Localização | Família de subálgebras, inclusões e relações modulares com ação geométrica demonstrada | [OPEN] |
| Geometria | Variedade, dimensão, assinatura e escala métrica a partir de dados identificados | [OPEN]; ℝ⁴ lorentziano é hipótese na derivação acima |
| Matéria e horizonte | T conservado, fluxo de boost, temperatura e condição de equilíbrio | [INPUT] na derivação; realização pela torre [OPEN] |
| Entropia-área | Correspondência e valor de η, com controle de limites e regularização quando necessário | [INPUT]; não pago pela normalização ω(I)=1 |
| Dinâmica | Cone nulo → tensor proporcional → Einstein por Bianchi | [DERIVED] geral condicionado; núcleo algébrico [REAL — Lean] |
| Física | Observáveis, regimes de validade e testes discriminantes | [OPEN] |

Não foi adotada a equação de Einstein como campo de um contrato e apresentada como conclusão independente. A condição no cone foi ligada a hipóteses termodinâmicas explícitas; o trabalho restante é construí-las, ou substituí-las por uma rota demonstrada, nos objetos da teoria.

## 7. Próxima obrigação formal concreta

Concluir o transporte unitário U da base de excitações para `TowerHilbert P`, obtendo a igualdade tipada JS=D. Em paralelo lógico, a especificação de uma rede de subálgebras e seus dados de localização deve identificar quais informações fixam dimensão e escala. Uma nova estrutura com campos já afirmando essas conclusões seria apenas um contrato; ela precisa de uma construção e de testemunhos não circulares.

Tudo foi escrito sob `Chatgpt`. O acervo, o programa canônico, as memórias e os selos originais permanecem fora das escritas desta bancada.


## ADENDO — 05/09/2026: avanço formal da análise modular

[REAL — Lean] A parte positiva JS agora tem positividade, auto-adjunticidade, injetividade, imagem densa e fatoração S=J(JS) verificadas sobre a torre completa. Consulte `FECHO_FORMAL_JS.md`. Esse resultado atualiza a primeira linha da tabela de pontes acima. As obrigações de localização, dimensão, assinatura, escala e correspondência termodinâmica permanecem [OPEN]; elas não são consequências automáticas da análise funcional concluída.


## ADENDO — 05/09/2026: Δ positivo auto-adjunto e a identidade modular

[REAL — Lean] A análise da torre agora inclui Δ=(JS)² com domínio correto, positividade, auto-adjunticidade, fechamento, construção maximal do adjunto antilinear S† e identidade S†S=Δ. Também foi verificada a reciprocidade JΔJ=Δ⁻¹ em gráficos. Consulte `DELTA_FORMAL.md`. Estes resultados atualizam o bloco de análise modular; localização, dimensão, assinatura, escala e realização termodinâmica continuam [OPEN].


## ADENDO — 05/09/2026: potência imaginária, grupo e invariância modular verificados

[REAL — Lean] Foi construído `deltaImaginaryPower P t`, um grupo unitário fortemente contínuo no Hilbert da torre. A caracterização espectral foi verificada: os vetores locais E_ij pertencem ao domínio de Δ, têm autovalores λ=w_i/w_j>0, geram um span denso e recebem a fase exp(it log λ). O operador limitado com essa ação é único. A construção, portanto, liga a potência imaginária ao Δ existente.

[REAL — Lean] Também foram provadas a conjugação da representação local, a invariância do bicomutante `theFactorObject P`, Ω fixo e a invariância de `omegaState P` sob a conjugação. Não se presumiu o grupo nem a invariância como campos de um contrato. A invariância do estado usa Ω fixo e unitariedade, não apenas ω(I)=1.

Esses resultados superam a pendência de formalizar o grupo Δ^{it}, sua continuidade forte e a invariância de M para esta torre produto. [OPEN] Permanecem a biblioteca geral de cálculo funcional, a construção da esperança condicional para as subálgebras pretendidas e as pontes geométricas/físicas. O parâmetro modular não foi identificado automaticamente com tempo próprio ou geometria.

O registro atual é `FLUXO_MODULAR_FORMAL.md`. Os seis módulos finais, de `ModularFlowLevel` a `ModularPower`, compilaram com código 0, sem avisos, sorry ou novos axiomas. As listas impressas foram conferidas contra propext, Classical.choice e Quot.sound. Os hashes e a contagem de teoremas foram lidos dos artefatos. Os 290 originais do manifesto foram rehasheados; o resultado de preservação acompanha a verificação consolidada. Nenhuma memória canônica ou selo foi alterado.
