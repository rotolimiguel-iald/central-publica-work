[REAL / INPUT / OPEN] Continuação 012 — densidade de área geométrica, reconstrução e restrição dinâmica da entropia
Data: 05/09/2026. Bancada ChatGPT. Continuação espontânea de 011; o túnel segue sem ordem gerencial 012.

## O avanço

[REAL — Lean] A lei A'=θA foi calculada para a densidade de área de uma tela transversal regular. A definição agora é A(t)=√det(S(t)ᵀg(γ(t))S(t)), com duas direções de tela S, e θ é o traço de ∇V usado na reconstrução anterior. A igualdade entre o traço transversal e o ambiente foi demonstrada, sob as condições geométricas explicitadas.

[REAL — implicação Lean] GeometricHorizonPencil recebe a tela, o referencial nulo e seu transporte. Não recebe um campo area nem um campo area_rate. geometricHorizonToLocal calcula ambos e produz o contrato anterior. geometric_area_einstein_reconstruction compõe isso com a conexão e o tensor de Einstein efetivos de 009–010, mantendo as premissas de calor, Clausius e conservação da matéria.

[REAL — Lean] Entropia fixa implica expansão zero se S=ηA vale no ponto e numa vizinhança unilateral passada, com η≠0 e A≠0. Logo o estado de um perfil e andar fixos da torre não acompanha uma tela em expansão apenas por renomear sua entropia como área.

[OPEN] Ainda falta construir a relação microscópica entre o estado, uma região/corte e essa densidade de área, além da dinâmica de calor e de H3. O resultado desta rodada paga uma identidade geométrica sob dados especificados; não conclui o objetivo amplo.

## Derivação e composição verificadas

### Cálculo da tela

[REAL] ScreenAreaCalculus.lean prova as regras de derivada de matrizes e da matriz de Gram. Para uma matriz 2×2 h e uma variação h'=bᵀh+hb, o determinante satisfaz (det h)'=2 tr(b) det h. Com det h>0, a regra da raiz quadrada dá A'=tr(b)A.

[REAL] NullScreenAlgebra.lean usa um referencial F=(k,n,e₁,e₂), inversa D, e b=D B F, onde B é a derivada covariante do campo de velocidade. Bk=0 e g(k,Bn)=0 anulam as duas contribuições longitudinais ao traço. A invariância do traço por mudança de base então identifica tr(B) com o traço do bloco transversal. O cálculo do bloco de Gram dá a variação transversal necessária.

[REAL] GeometricScreenTransport.lean liga a compatibilidade métrica já provada para Levi-Civita à derivada do campo g ao longo da curva. Para L=Σ VⁱΓᵢ, g'=Lᵀg+gL. O transporte S'=(B−L)S cancela os termos de conexão na derivada de SᵀgS. Daí sai coordinate_screen_area_derivative, com a expansão covariante efetiva.

### O contrato geométrico

[INPUT] GeometricScreenAlong exige duas direções contínuas no ponto de referência, tangência da curva ao campo V no ramo passado, referenciais nulos regulares e o transporte das direções. NullScreenAt exige inversa, a igualdade de Gram, primeiro vetor igual a V, regularidade espacial e g(k,Bn)=0. A geodesicidade do campo fornece Bk=0 por teorema.

A condição preserves_null_pairing permanece um campo explícito do testemunho. Sua dedução sistemática a partir de V nulo, diferenciabilidade e compatibilidade métrica ainda não foi implementada nesta rodada. Ela não foi escondida dentro de uma declaração de existência.

[REAL] GeometricAreaHorizon.lean deduz a continuidade, a não nulidade inicial e a lei de variação da área. A reconstrução pede testemunhos apenas para direções nulas não nulas. A direção zero é tratada diretamente, pois a forma quadrática vale zero nela. Isso evita exigir um referencial invertível com primeiro vetor zero.

[INPUT / OPEN] O restante do contrato de horizonte segue explícito: equilíbrio B=0 no ponto, corrente de calor, coeficiente η, taxa κ e limite de Clausius de segunda ordem. A condição B=0 ainda é mais forte que expansão e cisalhamento da tela nulos. A existência dos testemunhos para todos os pontos e todas as direções nulas não nulas não foi demonstrada.

## Correção de assinatura que o controle exigiu

[REAL] O kernel usa eta4=diag(1,−1,−1,−1), a convenção +---. A primeira versão de NullScreenAt exigia h₀₀>0, incompatível com uma tela espacial nessa assinatura. O controle plano falhou e revelou o problema antes da entrega.

A versão final exige h₀₀<0 e det h>0. O referencial plano tem k=(1,1,0,0), n=(−1/2,1/2,0,0) e Gram transversal −I. A métrica espacial positiva é −h; screen_area_signature_flip prova √det(−h)=√det h em dimensão dois. A fórmula da área, portanto, permanece a correta nessa convenção.

Uma compilação sem erros do teorema condicional anterior não quitava essa incompatibilidade geométrica. O auditor identifica os hashes das versões com first_screen_positive e preserva seus logs como rejeitados por condição de assinatura incompatível. Os hashes são lidos dos backups; não vêm de uma lista lembrada.

Essa correção pertence às cópias da bancada. Não seleciona nem deriva a assinatura da teoria; alinha o novo contrato à assinatura já assumida no kernel.

## Relação necessária entre a entropia e o movimento da área

[REAL] ScreenEntropyObstruction.lean compara derivadas unilaterais de S e ηA. Para igualdade no ponto e no ramo passado, obtém S'=ηA'. Uma entropia constante força A'=0 quando η≠0; numa tela regular isso força θ=0.

A instanciação usa exatamente reducedDiagonalEntropy(towerCutDensity(P,N)), de 011. P e N estão fixos no teorema. O resultado não exclui uma evolução do estado, um corte móvel, uma mudança de álgebra ou uma variação do número de fatores.

[REAL] Para pesos p_i>0 e uma variação normalizada p_i+εq_i, Σq_i=0, finite_entropy_area_rate_constraint liga a primeira lei diagonal já existente à área:
Σ_i q_i(−log p_i)=η θ A(0).

[INPUT / OPEN] A igualdade de entropia e área é premissa desse último teorema. Ele fornece uma condição que a dinâmica microscópica terá de satisfazer; não constrói q nem prova a lei entropia-área.

## Controles que delimitam a interpretação

[REAL] GeometricScreenControls.lean constrói flatGeometricHorizon: um testemunho completo do novo contrato em Minkowski, com direção (1,1,0,0) não nula, curva tangente, tela constante, conexão zero, calor zero e densidade de área calculada igual a 1. Assim o contrato final é habitado nesse caso.

[REAL] A família stretchedScreen(t)=(1+t)S₀ tem densidade de área (1+t)² e derivada 2 em t=0. Ela fornece um controle exato da obstrução à entropia congelada.

Essa família estirada é um controle de áreas de paralelogramos transversais parametrizados. Não foi apresentada como um segundo habitante completo de GeometricHorizonPencil nem como uma congruência nula construída. O habitante completo desta rodada é o plano de área constante.

A é uma densidade/elemento local de área associado às duas direções fornecidas. Não foi construída uma imersão de superfície geral, sua integral de área, nem uma identificação canônica entre o par de vetores e os fatores quânticos.

## Verificação e custódia

[REAL] Os seis módulos finais passaram no Lean. Todos os teoremas e as quatro construções principais de testemunhos/adaptação têm #print axioms. O manifesto calcula as contagens e lista cada dependência impressa, os bytes, os hashes e os logs correspondentes à versão final.

Além de erros de elaboração e avisos, o histórico preserva a falha semântica de assinatura. A ausência de sorryAx é necessária, mas não substitui verificar se as hipóteses descrevem o objeto pretendido. O controle plano é parte dessa verificação.

A entrega 011 foi reconferida em modo somente leitura durante esta rodada. A conferência dos inventários locais não substitui a recompilação e revisão independente da gerência. O ambiente Lean/mathlib continua externo ao pacote, instalado nesta máquina.

[KNOWN] A fonte primária de referência é [Jacobson, 1995](https://arxiv.org/html/gr-qc/9504004), equações (3)–(6). A igualdade de variação de área foi demonstrada aqui; as premissas termodinâmicas dessa referência continuam distinguidas das identidades geométricas.

Escritas da bancada somente em Chatgpt. Nenhuma execução/importação de um.py, nenhuma edição no kernel canônico, Atlas, memórias, selos ou gate. Nenhum dado observacional utilizado.

## Próximas obrigações

[OPEN] Completar a construção dos dados de tela/congruência e a dedução de preserves_null_pairing; vincular regiões e fatores quânticos à densidade de área definida independentemente; produzir uma dinâmica de estado que satisfaça a restrição de primeira lei e o balanço de calor. Assinatura, dimensão, globalização e as demais folhas do objetivo amplo permanecem separadas e abertas.
