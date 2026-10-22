# Einstein–sigma em quatro dimensões: BV local, anomalias e extensão formal

Data: 09/09/2026. Análise matemática de autoria desta sessão, arco 068.

**[DERIVED] Resultado novo:** exibe-se uma deformação explícita do sigma-modelo S³ e uma recorrência que transporta a nulidade da cohomologia de anomalias da referência para a teoria **formal nessa deformação**. Outra recorrência remove a anomalia quântica em cada ordem de ħ, quando os contratos cohomológico e de renormalização abaixo são satisfeitos. As duas recorrências são demonstradas; suas hipóteses de aplicação ao modelo completo não são declaradas pagas por essa demonstração.

**[OPEN] Limite determinante:** a ausência de anomalia local de difeomorfismos, a existência de uma matriz livre BV compatível, a especialização da deformação formal na esfera de raio um e a independência quântica do fundo são contratos diferentes. O estado físico linear construído no arco 067 não quita os quatro por si. Nenhum resultado desta nota é uma nova prova Lean ou uma execução do programa terminal.

## 1. Modelo e álgebra de gauge efetivamente escolhidos

**[INPUT]** Mantém-se a extensão ambiente da ação do habitante curvo, com campos independentes g e φ:

\[
S_{\rm cl}[g,\phi]= -\frac1{2\kappa}\int_M\mu_g(R-2\Lambda)
 +\frac c2\int_M\mu_g\,g^{\mu\nu}
 h_{AB}(\phi)\partial_\mu\phi^A\partial_\nu\phi^B,
\qquad \phi:M\longrightarrow S^3.
\tag{1.1}
\]

A assinatura é (+---), as convenções de curvatura são as da nota de Jacobi, e c=k/(π cosh²k)>0. O habitante particular usa κc=4 e Λ=3/4. A escala física que converte c e κ para unidades dimensionais continua sendo uma entrada; nenhum fator novo de π é absorvido na cohomologia.

O gauge considerado é somente o grupo de difeomorfismos conectado à identidade, localmente. As isometrias O(4) do alvo são **simetrias rígidas**, sem conexão gauge nem ghost interno. Weyl não é gauge de (1.1). Em coordenadas y no alvo, com ghost ímpar C^μ, o diferencial clássico nos campos é

\[
sg=\mathcal L_Cg,\qquad sy^A=C^\mu\partial_\mu y^A,
\qquad sC^\mu=C^\nu\partial_\nu C^\mu.
\tag{1.2}
\]

Acrescentam-se antifields e, para fixar gauge, o par não mínimo s\bar C=b, sb=0. Pode-se escolher a convenção do anticolchete de modo que sΦ seja a derivada de S_BV em Φ†. A ação mínima contém S_cl mais os acoplamentos Φ†sΦ; os sinais dos antifields seguem essa convenção, sem alterar (1.2).

**[DERIVED]** Como C é ímpar, \(\mathcal L_C^2=\mathcal L_{[C,C]}/2\), enquanto \(sC=[C,C]/2\). A regra de Leibniz graduada fornece \(s(\mathcal L_Cg)=\mathcal L_{sC}g-\mathcal L_C^2g=0\); o mesmo vale para y. A identidade de Jacobi graduada dá s²C=0. A ação clássica é invariante modulo uma derivada total, e a álgebra fecha fora das equações de movimento. A extensão mínima satisfaz a equação mestra clássica. Os pares não mínimos são contráteis e não criam classes de cohomologia local.

Isso estabelece nilpotência **clássica**. O produto coincidente dos campos exige renormalização e introduz um problema adicional, tratado na seção 5.

## 2. Qual cohomologia controla a anomalia local

Fixe uma região espaço-temporal contrátil e uma carta contrátil do alvo. Tome formas locais em jatos dos campos, ghosts e antifields; cada coeficiente da expansão formal tem ordem finita de jato. Restrinja os coeficientes e primitivas à mesma classe admissível, incluindo as condições de realidade e simetrias externas que se pretende preservar. A álgebra não inclui inversas de gradientes de campos, operadores de Green ou projetores SVT não locais. Uma classe admissível maior pode ter cohomologia diferente.

Uma primeira quebra local da identidade de gauge é uma 4-forma a de número de ghost 1. A condição de consistência e a equivalência por contra-termos são

\[
sa+db=0,\qquad a\sim a+sB+dD,
\quad \mathrm{gh}(B)=0,\quad \deg B=4.
\tag{2.1}
\]

Logo a obstrução pertence a \(H^{1,4}_{\rm loc}(s\mid d)\). Anomalia **removível** significa classe nula, não necessariamente que uma prescrição arbitrária produza a=0 antes da renormalização finita.

**[KNOWN — importação delimitada]** Barnich–Brandt–Henneaux classificam a cohomologia local de Einstein–Yang–Mills com matéria sob regularidade/normalidade e hipóteses explícitas sobre a álgebra e topologia. Na análise usada aqui, a condição (7.33) exige que classes características de grau máximo permaneçam não triviais na cohomologia equivariante mesmo on-shell. Ausentes fatores gauge abelianos, a classificação deixa as classes quirais e certas classes topológicas de vielbein; estas últimas não aparecem em dimensão quatro. A hipótese (7.33) não se reduz à normalidade: o artigo mostra um acoplamento axion–curvatura que a viola. A matéria globalmente não contrátil também requer tratamento adicional. Referência exata: [BBH 1995, §§2, 4, 7, 9 e 10.4](https://arxiv.org/pdf/hep-th/9505173).

**[DERIVED — eliminação dos candidatos quirais no caso de referência]** Para aplicar essa classificação à referência com três escalares reais e nenhum gauge interno, resta o setor local de Lorentz, caso se use vielbein. Em quatro dimensões seu complexo é so(4,ℂ)≅sl₂(ℂ)⊕sl₂(ℂ). Os geradores invariantes têm graus 2 e 2; não há polinômio invariante homogêneo de grau 3. Não existe, portanto, o polinômio de curvatura de grau seis cujo descenso produziria uma anomalia quiral local de 4-forma. Não há fator abeliano de grau um para uma classe mista. Escalares Lorentz-singlet não acrescentam um grupo gauge interno. A conclusão usa a **lista completa sob as hipóteses anteriores**, além dessa conta de graus; a frase “não há férmions quirais” isolada seria insuficiente.

O uso de vielbein é uma apresentação auxiliar: em uma carta de referenciais não degenerados, remover as rotações locais deve ser a equivalência local usual com a apresentação métrica. Não se acrescenta uma simetria física O(4) gauge ao sigma-modelo.

**Contrato C0, ainda explicitamente condicional nesta entrega.** Para a referência Einstein mais três escalares minimamente acoplados, adotar/verificar o complexo local regular e normal apropriado, sua equivalência métrica–vielbein e a condição (7.33), na mesma classe de coeficientes e primitivas que conterá os contra-termos. A classificação e a conta acima então dão

\[
H^{1,4}_{\rm loc}(s_{\rm ref}\mid d)=0.
\tag{2.2}
\]

O lagrangiano de referência tem cinética não degenerada de matéria e não contém o acoplamento axion do contraexemplo. Isso identifica o caso a verificar; não substitui uma prova específica de (7.33). Também não se confunde a existência de simetrias de Killing no fundo particular com uma nova identidade gauge entre os jatos de campos genéricos. A regularidade BV local e as restrições globais de integrabilidade das perturbações são questões distintas.

## 3. Uma deformação efetiva e explícita até o sigma-modelo

No hemisfério φ⁴>0, escreva φ=(y,√(1−q)), q=Σ_A(y^A)²<1. A métrica induzida é

\[
h_{AB}(1,y)=\delta_{AB}+\frac{y_Ay_B}{1-q}.
\]

Introduza um parâmetro formal ε e a família

\[
h_{AB}(\varepsilon,y)=\delta_{AB}
 +\frac{\varepsilon y_Ay_B}{1-\varepsilon q},\qquad
h^{AB}(\varepsilon,y)=\delta^{AB}-\varepsilon y^Ay^B.
\tag{3.1}
\]

**[DERIVED]** A multiplicação das duas matrizes cancela o coeficiente de yyᵀ:
\(-\varepsilon+\varepsilon/(1-\varepsilon q)-\varepsilon^2q/(1-\varepsilon q)=0\).
A fórmula do determinante de uma atualização de posto um dá det h=(1−εq)⁻¹. A derivada direta de (3.1) na fórmula de Levi-Civita dá

\[
\Gamma^A_{BC}(h_\varepsilon)=\varepsilon y^Ah_{BC}(\varepsilon,y).
\tag{3.2}
\]

Assim h₀ é plana e h₁ é exatamente a métrica esférica da ação (1.1). Para valores reais 0≤ε≤1 e q<1 a matriz é positiva definida. Este fato geométrico real não autoriza avaliar uma série formal de contra-termos em ε=1.

A expansão da ação é explícita:

\[
S_\varepsilon=S_{\rm ref}+
\frac c2\sum_{m\ge1}\varepsilon^m\int_M\mu_g\,
q^{m-1}g^{\mu\nu}(y\cdot\partial_\mu y)(y\cdot\partial_\nu y).
\tag{3.3}
\]

Cada coeficiente contém duas derivadas e 2m+2 ocorrências de y. A ação de referência contém Einstein e a cinética plana dos três escalares, com o mesmo c>0. Não se introduziu cinética de sinal oposto. A derivada de S_ε em y reproduz

\[
\frac{\delta S_\varepsilon}{\delta y^A}
=-c\mu_g h_{AB}(\varepsilon,y)
\left(\Box_g y^B+\Gamma^B_{CD}(h_\varepsilon)
 g^{\mu\nu}\partial_\mu y^C\partial_\nu y^D\right).
\tag{3.4}
\]

As transformações de gauge (1.2) não dependem de ε. Portanto a solução BV existe para toda a família, e

\[
s_\varepsilon=s_{\rm ref}+\sum_{m\ge1}\varepsilon^m s_m,
\qquad s_\varepsilon^2=0.
\tag{3.5}
\]

Os termos s_m modificam a parte das equações nos antifields de g e y; não modificam os geradores nos campos nem o colchete dos difeomorfismos. É uma deformação concreta do mesmo setor de gauge, não uma analogia entre modelos de nomes parecidos.

**[KNOWN]** O tratamento por séries formais cujos coeficientes são locais, e a aplicação da resolução de Koszul–Tate por recorrência, são apresentados em [BBH 2000, §§4.7, 5.3 e 6.4](https://arxiv.org/pdf/hep-th/0002245). Seu teorema específico de teorias Yang–Mills do §11 não é importado como se fosse automaticamente um teorema Einstein–sigma. A passagem necessária aqui é demonstrada abaixo no complexo precisamente escolhido.

## 4. Lema de transporte ε-ádico, com prova

**[DERIVED] Lema.** Seja \(\mathcal A^g=\Omega^{g,4}_{\rm loc}/d\Omega^{g,3}_{\rm loc}\), na classe admissível fixa. Suponha que \(s_\varepsilon\) induza um diferencial em \(\mathcal A[[\varepsilon]]\), que esse módulo seja completo e separado na topologia ε-ádica e que \(H^1(\mathcal A,s_{\rm ref})=0\). Então

\[
H^1(\mathcal A[[\varepsilon]],s_\varepsilon)=0.
\tag{4.1}
\]

**Prova.** Trabalhe primeiro modulo d. Para um cociclo a=Σ_{n≥0}εⁿa_n, suponha construído B^{(<N)} de modo que

\[
a-s_\varepsilon B^{(<N)}=\varepsilon^N r_N+O(\varepsilon^{N+1}).
\]

Aplicar s_ε e usar sua nilpotência dá \(s_{\rm ref}r_N=0\) no coeficiente εᴺ. Pela hipótese existe b_N de ghost zero com \(r_N=s_{\rm ref}b_N\). Defina

\[
B^{(<N+1)}=B^{(<N)}+\varepsilon^N b_N.
\tag{4.2}
\]

O resto passa a O(εᴺ⁺¹). A construção começa com B^{(<0)}=0 e vale por indução para todo N. A completude fornece B=Σ εⁿb_n e a separação implica a=s_εB. Antes de passar ao quociente, cada etapa é \(r_N=s_{\rm ref}b_N+dc_N\), e a série dos c_N produz a igualdade de formas modulo d. □

Há uma versão finita imediata: modulo εᴺ⁺¹, N+1 etapas cancelam o cociclo exatamente nesse quociente. Todos os coeficientes têm jato finito se as primitivas da hipótese o tiverem; não se exige uma única ordem máxima de jato para a série inteira.

**Aplicação condicional.** C0 e (3.3)–(3.5) produzem a nulidade formal de anomalias da família Einstein–sigma em \(\mathbb R[[\varepsilon]]\). O parâmetro ε não é o relógio Gibbs, o fator angular nem ħ. Sua função é organizar a deformação da métrica alvo.

**O ponto em que seria errado ampliar a conclusão.** A aplicação ε↦1 não é uma operação definida em todas as séries formais: por exemplo Σ_{n≥0}εⁿ é legítima formalmente, mas sua soma em 1 diverge. A família clássica (3.1) ser regular até ε=1 não garante regularidade da série de primitivas escolhida em (4.2). Para transferir o resultado diretamente ao sigma S³ de raio um, é preciso uma destas duas provas adicionais:

1. calcular \(H^{1,4}(s_{\sigma}|d)\) diretamente na álgebra de germes/coordenadas do sigma escolhido; ou
2. construir a recorrência preservando uma filtração de campos/acoplamentos que permita especializar ε=1 coeficiente a coeficiente na expansão pertinente, com finitude demonstrada em cada coeficiente.

Não se afirmou nenhuma dessas duas concluída. A prova ε-ádica já fornece um contrato formal não trivial; não permite uma conclusão irrestrita sobre funções suaves no alvo global. Ela tampouco transporta automaticamente o estado do fundo ε=1 para uma família de fundos on-shell em todos os ε: a cohomologia desta seção é a do lagrangiano não cindido em fundo e perturbação.

## 5. Recorrência da equação mestra quântica

Para tornar a passagem à interação rigorosa, são necessários contratos separados da nulidade cohomológica:

**Q1 — quantização livre BV.** Em um domínio globalmente hiperbólico, fornecer o sistema completo gauge-fixado, seus propagadores causal/Feynman e uma estrutura Hadamard graduada compatível com o diferencial livre e os adjuntos. Em linguagem de Wick, a parte antissimétrica graduada deve reproduzir o propagador de **todos** os componentes e as identidades de Ward livres. Não é necessário exigir positividade dos ghosts; positividade tem seu lugar no quociente físico. Uma construção por parametrizes é aceitável se os defeitos suaves e suas correções forem controlados.

**Q2 — renormalização causal local.** Construir os produtos temporalmente ordenados coeficiente a coeficiente, com fatorização causal, realidade/unitariedade, independência funcional dos campos, condição microlocal, condições de escala apropriadas à EFT e identidade de ação/Ward anômala. A primeira quebra deve ser local e satisfazer a condição de consistência. A classe admissível deve permitir os contra-termos que a recorrência usa, sem uma restrição escondida a finitos termos da ação original.

**Q3 — compatibilidade do espaço de primitivas.** A nulidade cohomológica deve valer no mesmo espaço de densidades permitido por Q2. Se o esquema exige naturalidade/covariância externa, as primitivas precisam pertencer à classe correspondente; uma primitiva que quebre essa exigência não paga esse contrato mais forte. Condições globais de fundo e de alvo não são deduzidas do cálculo em uma carta.

**[KNOWN]** A identidade mestra anômala, a equação mestra quântica renormalizada e sua transformação sob renormalização finita são formuladas em [Fredenhagen–Rejzner, §§4.1–4.2](https://arxiv.org/html/1110.5232v3). [Brunetti–Fredenhagen–Rejzner, §3.4](https://arxiv.org/html/1306.1058v4) aplicam a remoção cohomológica em gravidade pura 4D. Esse caso puro não é citado como prova já pronta do acoplamento sigma.

**[DERIVED] Teorema condicional de remoção em todas as ordens.** Assuma Q1–Q3 e nulidade de H^{1,4}(s|d) no complexo admissível, seja diretamente para s_σ, seja na versão formal s_ε da seção 4. Então pode-se escolher renormalizações finitas em cada ordem de ħ para satisfazer a QME local como série formal.

**Prova.** Suponha que todas as ordens menores que N já satisfaçam a QME. Escreva a primeira quebra como

\[
\mathfrak A(\Gamma)=\hbar^N a_N+O(\hbar^{N+1}).
\tag{5.1}
\]

A identidade de consistência obtida da identidade de Ward anômala e da Jacobi graduada implica \(sa_N+db_N=0\). As correções quânticas ao próprio diferencial são O(ħ); ao atuar na primeira quebra não alteram essa equação na ordem N. Pela hipótese,

\[
a_N=sB_N+dD_N.
\tag{5.2}
\]

Defina a renormalização finita de ordem N de forma que sua variação da quebra seja \(-\hbar^NsB_N\). Na convenção em que a linearização da quebra é s, isso corresponde a adicionar \(-\hbar^NB_N\) à ação renormalizada. Termos de borda são tratados modulo d. A quebra passa a O(ħᴺ⁺¹), e ordens anteriores permanecem intactas. Repetir para N=1,2,… constrói uma solução formal da QME. Se s=s_ε, resolver (5.2) usa a segunda recorrência, a de ε da seção 4. As séries são lidas coeficiente a coeficiente em ambos os parâmetros. □

Esse resultado é “todas as ordens” no sentido formal; não prova convergência em ħ, existência de integral funcional não perturbativa ou unicidade da teoria. O operador BV quântico correspondente é nilpotente no contrato renormalizado e define a cohomologia física H⁰(ŝ); não se identifica a nilpotência clássica com a quântica antes de impor a QME.

O trabalho é local com um cutoff suave igual a um numa vizinhança causal da região observada. As identidades são exigidas nessa região, modulo termos suportados onde o cutoff varia. Construir a álgebra local pelo limite adiabático **algébrico** não afirma existência de um S-matrix global nem de limite adiabático de estados, que podem enfrentar problemas infravermelhos.

## 6. Contrato com o estado físico do arco 067

A [nota do estado físico](<C:/IALD/Central de Patentes/Chatgpt/HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912/ESTADO_FISICO_HADAMARD_E_CONTRATOS.md>) constrói uma covariância positiva via os modos S/V/TT, no quociente de testes \((\ker K^\dagger\cap\Gamma_c)/H\Gamma_c\). Seu texto distingue expressamente essa construção de uma matriz completa de gauge/ghost. A [nota Jacobi](<C:/IALD/Central de Patentes/Chatgpt/QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md>) contém H, K, C e o sistema hiperbólico acoplado a completar.

**[DERIVED — consequência de escopo]** A covariância física admite contração de observáveis lineares invariantes. Q1 pede também contrações fora desse subespaço, necessárias nos vértices e nas identidades de Ward. Não se pode estender seu CCR a testes arbitrários por redefinir o nome do estado. É uma obrigação concreta de extensão, não uma crítica à positividade física demonstrada. A distinção aparece também em [Wrochna–Zahn, Observação 3.3](https://arxiv.org/html/1407.8079v2).

A liberdade de mudar uma representação Hadamard por uma diferença suave permite comparar ordenações de Wick quando ambas já satisfazem os contratos. Ela não cria a matriz BV compatível que ainda falta. Tampouco a covariância livre positiva produz automaticamente um estado positivo da teoria interagente a todos os tempos; a presente conclusão principal é algébrica e formal.

No habitante, pode-se trabalhar em um diamante globalmente hiperbólico contido no hemisfério/ortante positiva. A extensão geométrica I×S³ inteira permite a decomposição global usada no arco 067, mas não transforma os cinco pesos em uma carta global de probabilidades positivas. A expansão ambiente em g e φ continua sendo [INPUT]; a família mínima de cinco P, localmente pura gauge, não recebe graus de liberdade adicionais por uma prova de renormalização.

## 7. Três anomalias que precisam permanecer separadas

**Gauge de difeomorfismos.** É a quebra de ghost 1 controlada pela seção 2. O teorema condicional da seção 5 trata esse problema local e perturbativo.

**Traço/Weyl.** Não há ghost de Weyl em (1.2), e a ação Einstein–sigma escolhida já possui escalas. Termos de traço renormalizado, fluxo de escala ou beta-funções não são automaticamente uma falha da conservação covariante ou da QME de difeomorfismos. Preservar a identidade de difeomorfismos não exige tornar o traço zero. Nenhum coeficiente de traço foi calculado nesta nota.

**Independência quântica da cisão fundo–perturbação.** Ela exige identificar observáveis entre fundos e controlar a conexão correspondente sobre as álgebras. QME em cada fundo não demonstra esse transporte. [Taslimi Tehrani–Zahn, §4](https://arxiv.org/html/1804.07640) exibem possíveis obstruções adicionais na gravidade perturbativa: a condição envolve a anomalia com inserção da variação da férmion de gauge. Sem uma restrição renormalizável de contagem de potência, admitem-se infinitos tensores covariantes candidatos; sua ocorrência efetiva permanece aberta naquele trabalho. Isso não é uma anomalia já calculada para o nosso sigma-modelo, nem uma refutação da QME em fundo fixado.

Uma verificação independente no caminho futuro deve estudar, para variação k do fundo, a inserção que esquematicamente se escreve \(A^{\rm int}_1(\bar\delta_k\Psi)\), e a planura modulo BRST do transporte. A nulidade de H^{1,4}(s|d) usada em (5.2) não é prova dessa condição com inserção. As fórmulas podem ganhar termos de variação do fundo da matéria no sigma; não se restringe o transporte somente a \(\bar g\) se \(\bar\phi\) também muda.

Também não se usa uma verificação a um loop como atalho universal: o teorema de [Zahn, Background independence and the Adler–Bardeen theorem](https://arxiv.org/abs/2209.02393) assume Yang–Mills **renormalizável**, com as condições de grupo ali declaradas. A ação Einstein–sigma EFT desta nota não satisfaz essa hipótese. Um cálculo de divergência a₄ da matéria em g externo trata contra-termos de ghost zero; não é o cálculo da quebra BV total com gravitons/ghosts, nem a remoção de todas as ordens.

## 8. Alvo global, anomalias globais e conteúdo EFT

O cálculo em uma carta não cobre efeitos de mudanças de carta ou setores topológicos de mapas M→S³. A 3-forma de volume de S³ é globalmente fechada e não exata, enquanto numa carta é exata; logo a passagem global pode alterar a análise de formas locais. Isso não demonstra, por si, uma anomalia de 4-forma e ghost 1. É necessário calcular a classe pertinente, em vez de transformar toda topologia em “anomalia”.

O grupo S³≅SU(2) aparecer como **alvo** também não põe o modelo no teorema de [Henneaux–Wilch sobre o sigma principal gauged](https://arxiv.org/pdf/hep-th/9802118): ali uma ação do grupo é gauge e há seus ghosts/conexões. Aqui somente difeomorfismos são gauge. Usar o resultado gauged apagaria essa diferença de complexo.

Possíveis fases sob grandes difeomorfismos, holonomias do feixe determinante, topologia de bordas e transições de setor requerem análise global específica. A cohomologia BRST local infinitesimal não as decide. Esta nota não apresenta exemplo de anomalia global no Einstein–sigma bosônico e tampouco prova sua ausência.

Renormalizar preservando gauge admite a família de invariantes locais da EFT, com coeficientes de Wilson e condições de renormalização. Isso pode manter a simetria em todas as ordens formais sem fechar em um número fixo dos parâmetros originais. A perspectiva formal e sua truncagem efetiva são também o escopo de [BFR, Locally covariant approach to effective quantum gravity](https://arxiv.org/abs/2212.07800). Não se demonstra limite UV, convergência, seleção única dos coeficientes ou completude não perturbativa. A contagem de potência e o coeficiente a₄ são objetos da frente complementar, não resultados duplicados aqui.

## 9. Entrega utilizável e próximas verificações concretas

| Objeto | Estatuto nesta nota | Uso permitido |
|---|---|---|
| Ação ambiente Einstein–sigma | INPUT | Modelo sobre o qual os contratos são formulados |
| Gauge difeomorfismo e CME | DERIVED | Diferencial clássico definido, sem ghost Weyl/target |
| Família h_ε, vértices e s_ε | DERIVED | Deformação local explícita com referência plana |
| Transporte de H¹ por ε-ádica | DERIVED | Teorema e recorrência; C0 é hipótese |
| Referência BBH no complexo admissível | KNOWN + contrato C0 | Falta verificação específica completa de regularidade/7.33 e classe de primitivas |
| QME em todas as ordens | DERIVED condicional | Segue de Q1–Q3 e nulidade cohomológica apropriada |
| Matriz BV completa do fundo 067 | OPEN | Não decorre somente da covariância física reduzida |
| Especialização formal na esfera ε=1 | OPEN | Requer prova direta ou filtração que autorize a avaliação |
| Transporte entre fundos e alvo global | OPEN | Obrigações diferentes de QME local |
| UV / teoria não perturbativa | OPEN | Nenhuma conclusão nova de existência |

**Primeira tarefa concreta:** construir a extensão Hadamard graduada Q1 para os operadores H_gf e Q do fundo 067, conferindo em fórmulas os adjuntos e as identidades de Ward em todas as entradas. A meta é uma matriz, com recibo das identidades, e não apenas uma contagem de graus de liberdade.

**Tarefa cohomológica paralela:** provar C0 na classe exata de contra-termos e resolver a especialização da seção 4. A folha Lean pequena recomendada é `FormalLocalAnomalyLifting.lean`: primeiro uma versão truncada do lema (4.2) para um complexo graduado e um diferencial formal nilpotente, com hipótese explícita de exatidão em grau 1. Essa folha não deve afirmar que o H¹ do Einstein–sigma foi calculado. Sua contribuição seria tornar verificável a passagem algébrica, deixando os contratos físicos/importados tipados.

**Depois:** escolher produtos temporais e calcular a primeira quebra de Ward do sistema completo, verificar sua decomposição (5.2) e registrar o contra-termo real permitido. Para ampliar o resultado a fundo variável, tratar a inserção da seção 7; a prova da QME sozinha não autoriza pular essa etapa.

## 10. Custódia

Apenas esta pasta nova recebe arquivos. O manifesto acompanhante mede os bytes e hashes das fontes locais citadas e desta nota, sem executar/importar um.py. Não há compilação Lean nova, cálculo de Feynman, aprovação de terceiro ou atualização de gate atribuídos a esta entrega. Os resultados escritos são DERIVED; as hipóteses ainda abertas permanecem no enunciado. Os documentos anteriores são preservados como fontes, inclusive quando registram um estado histórico anterior do caminho.
