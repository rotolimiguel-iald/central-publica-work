# Continuação 044 — boost aproximado, corrente e orientação do calor

06/09/2026. Escritas exclusivamente em Chatgpt. Originais, um.py, Atlas, memórias, kernel canônico e selos anteriores somente leitura.

## A pergunta do operador: inscrição angular e área

[ONTO / CONJECTURE] A proposta distingue L, interpretado como cauda ou poço, da inscrição quadrática produzida por sua leitura angular. O Atlas foi consultado na passagem “módulo produzido pela fase” e na regra dos dois regimes. Não identificamos L_phi com o operador L=log H de030–033 sem uma ponte própria, nem atribuímos ao operador a definição da inscrição como U*U.

[DERIVED — álgebra ilustrativa, não novo teorema Lean044] Se uma projeção da fase produz amplitude r(theta), o módulo da inscrição r(theta)^2 é |r(theta)|². Para duas direções ortogonais igualmente escaladas, o Gram positivo da tela é G=|r|² I_2 e sua densidade de área relativa é sqrt(det G)=|r|². Com amplitudes diferentes, G=diag(|r_1|²,|r_2|²) dá |r_1 r_2|. A escala física e o elemento de referência não nascem dessa identidade. Um único parâmetro de fase, sem duas direções independentes, não fornece por si uma métrica bidimensional não degenerada.

Na tela043, a=c dá a identidade funcional A(t)=cos²(sqrt(a)t). Isso concretiza o caso isotrópico para amplitudes de Jacobi em uma métrica fornecida. Não demonstra que essas amplitudes sejam a projeção de exp(i theta L), nem que uma geometria física foi reconstruída do estado. A certificação como tela regular permanece onde os fatores de Jacobi não zeram.

[KNOWN — contexto] A métrica de estados pode ser construída da parte real do tensor geométrico quântico, usando variações horizontais. Essa construção, descrita por Kolodrubetz et al., não identifica automaticamente a métrica de estados com a métrica do espaço-tempo. Fonte primária consultada: https://arxiv.org/abs/1602.01062.

[OPEN] “A luz dobra e retorna como fluxo de estabilização” precisa de uma equação de evolução, um estado ou conjunto de referência e uma estimativa das perturbações. O módulo perde informação de fase/orientação: r e −r dão a mesma área. Retorno periódico não prova atração. Como ilustração, cos(omega t) retorna sem amortecer perturbações de amplitude; em dy/dt=−gamma y, gamma>0, a atração vem da equação e |y(t)|²=exp(−2gamma t)|y(0)|². Não se exige dissipação para toda noção de estabilidade: estabilidade de Lyapunov e convergência atrativa são propriedades diferentes e precisam ser enunciadas. A face hiperbólica e a leitura angular continuam distintas.

## Construção044 e relação com043

[INPUT] Na carta029, u=x0+x3, v=(x0−x3)/2, X=x1, Y=x2, usamos
g=2 du dv−dX²−dY²+H du², H=aX²+cY².
A cinemática044 permite quaisquer a,c reais. A ligação à tela043 retém a,c≥0 e sua certificação regular local. A área inicial do lápis central é normalizada a1.

[REAL — teoremas044 compilados] O campo
chi=−kappa u partial_u+kappa v partial_v
é (-kappa x3,0,0,-kappa x0) nas coordenadas x. Seu fluxo efetivo é
Phi_s(u,v,X,Y)=(exp(−kappa s)u,exp(kappa s)v,X,Y).
A matriz tem, no bloco0,3, diagonal E=(exp(−kappa s)+exp(kappa s))/2 e fora da diagonal O=(exp(−kappa s)−exp(kappa s))/2; identidade nos índices1,2.

São certificados o grupo, a inversa por −s, a derivada temporal igual a chi(Phi_s x), o Jacobiano espacial e a preservação da métrica plana eta4. Na curva central gamma(t)=t d, d=(1/2,0,0,1/2),
Phi_s(gamma(t))=gamma(exp(−kappa s)t),
chi(gamma(t))=−kappa t d.
Para kappa>0,t<0, a componente temporal do campo é positiva.

[DERIVED — consequência analítica da fórmula, não novo lema de estabilidade044] Para kappa>0 e s→+infinito, u(s)=exp(−kappa s)u(0) tende a0 na central. Contudo, a perturbação na direção conjugada v evolui como exp(kappa s)v(0). O ponto fixo do fluxo de boost tem direções de contração e expansão; sua aproximação pela central não estabelece estabilidade no espaço inteiro. Esta é uma propriedade do fluxo escolhido, não uma conclusão sobre estabilidade física da TGL ou sobre a dinâmica de matéria, que não foi identificada com ele.

O pullback é a operação literal M^T g(Phi_s x) M, com M o Jacobiano certificado. O resultado é
Phi_s* g=g+(exp(−2kappa s)−1)H(w tensor w), w=du.
A derivada de Lie é construída das derivadas parciais efetivas de g e chi e vale
L_chi g=−2kappa H(w tensor w).
A derivada do pullback em s=0 coincide com essa expressão.

Ao longo da central, a derivada de Lie e todas suas primeiras derivadas espaciais zeram. As segundas derivadas em X e Y são, respectivamente,
−4kappa a(w tensor w), −4kappa c(w tensor w).
Esse cálculo quantifica a aproximação do campo. Quando kappa≠0 e (a≠0 ou c≠0), esse campo específico não é Killing em qualquer aberto contendo a origem. Para a=c=0 ou kappa=0, o defeito zera. Não se excluem outros campos de Killing, nem se afirma que Phi_0 falha: Phi_0 é a identidade.

## Corrente efetiva e sinais

Para qualquer tensor bilinear T, sem hipótese de simetria ou conservação,
T(chi(gamma(t)),d)=−kappa t T(d,d).
Multiplicar pela área literal043 fornece exatamente screenHeatFlux da mesma tela. A matéria e a lei de Clausius não entram na construção do campo nem nessa identidade bilinear.

Para a fonte especial waveMatter=m(w tensor w), também vale fora da central
T(chi(x),V043(x))=−kappa u(x)m.
Isto é uma igualdade da contração para essa fonte. Não se estabelece uma identidade dos campos chi e −kappa u V043 fora da central; em geral eles diferem. Há casos de igualdade, como kappa=0.

A integral Q_boost(t)=integral de0 até t coincide globalmente com opticalHeat041 para waveMatter. Sua identificação com opticalScreenHeat043, que usa uma extensão contínua do passado, é germinal em t→0−.

O segmento do passado até a origem usa
Q_segment(t)=integral de t até0=−Q_boost(t),
DeltaA_segment=A(0)−A(t).
Os dois sinais se invertem juntos. Para kappa,m≥0 e t≤0, o fluxo e Q_segment são não negativos. A interpretação como tela regular permanece local, mesmo quando a identidade de funções vale além das cáusticas.

Com a normalização escalar herdada kappa/(2pi), o defeito
D_segment=Q_segment−[kappa/(2pi)]eta DeltaA_segment
é o negativo do defeito041, e germinalmente do043. Seu limite quadrático é
lim D_segment(t)/t²=−kappa[eta(a+c)−2pi m]/(4pi).
Para kappa≠0, o limite zera se e somente se eta(a+c)=2pi m. Construir o boost e a tela não impõe esse casamento.

[KNOWN / INPUT] Jacobson usa energia do boost aproximado e temperatura Unruh para formular o balanço local. A construção geométrica044 paga o campo e a corrente para esta família; não demonstra a identificação térmica. Fonte consultada: https://arxiv.org/pdf/gr-qc/9504004, equações1–2. A escala kappa, a temperatura física/KMS, a identificação modular, eta, a matéria e a seleção da métrica continuam entradas ou obrigações abertas. O lápis central não é uma construção de horizonte causal global.

## Ordem010 recebida durante a verificação

A derivação prévia044 registra corretamente a consulta então feita, cujo último arquivo disponível era009. Uma nova consulta nesta execução encontrou ORDEM_010_horizontes_concretos_aperiodico_e_o_relogio_apos_a_obstrucao.md. A044 já estava escrita e em compilação; sua conclusão geométrica é preservada e a nova ordem orienta a etapa seguinte.

A — Horizontes não modulares e esperança aperiódica: não resolvidos pela044. A revisão paralela localizou e leu TheLiftFiresOnThePeriodicTower e TheModularFlowIsAHorizon no kernel da casa Nós; sua custódia v329 não foi revalidada aqui. Há uma rota candidata mais curta para a troca finita: matriz local unitária V que comuta com a densidade, U=towerPi(V), pertencimento ao centralizador e preservação do estado. TowerHorizon não exige U Omega=Omega. Restam a matriz de permutação, a invariância dos pesos e sua ação literal sobre os sítios, com controle de não modularidade. O andar N contém N+1 sítios. Essa triagem não é uma construção nova compilada. Nada dessas fontes novas foi importado na044.

B — A impossibilidade uniforme precisa dos quantificadores corretos. Em040, sob eta>0 e B>0, duas geometrias com o mesmo estado e Ricci, sigma=0 e sigma=r/4, exigem coeficientes cúbicos diferentes por r/96>0. Isso impede um único relógio de casar ambas; não prova que todo relógio falhe em cada geometria isolada. Uma classe de relógios instantâneos do estado, na curva bilateral par examinada040, também precisa enfrentar a obstrução de orientação: Fisher e o relógio entrópico construídos usam ramo/referência, e a órbita modular estacionária não parametriza essa curva. A definição da classe não pode apagar essas distinções. A044 não declara resolvida a dicotomia universal proposta.

C — A invariância por horizontes deve ser testada como seleção do protocolo. [DERIVED — álgebra, não novo lema044] Se h é uma forma positiva invariante, alpha h também é para qualquer alpha>0; em duas dimensões, sqrt(det(alpha h))=alpha sqrt(det h). Portanto, invariância isolada não fixa escala. Uma normalização adicional pode eliminar essa liberdade global, mas não foi derivada só da covariância. A área isotrópica quadrática ilustra a proposta do operador sem provar seleção de tangentes ou isotropia. A044 não introduz uma ponte região–álgebra.

H3 a partir do estado: OPEN. Reconstrução gravitacional geral: OPEN. Meta ampla de gravidade quântica: OPEN. Gate canônico intocado.


## Verificação formal e custódia

[REAL — compilação final] Em CONTINUACAO044_CLEAN_20260906_224045_647263, os quatro módulos e Imports044All passaram: 76 teoremas, 14 definições, 90 impressões de axiomas e zero instâncias. Os cinco passos retornaram exit0/PASS, sem erros ou advertências, com cobertura exata e apenas propext, Classical.choice e Quot.sound. As fontes de trabalho coincidem com as cópias compiladas. As 2.047 entradas congeladas permaneceram idênticas, e o inventário do build contém 2.066 arquivos.

| Módulo | Teoremas | Definições | Prints |
|---|---:|---:|---:|
| ApproximateBoostFlow | 40 | 7 | 47 |
| BoostMetricPullback | 6 | 2 | 8 |
| BoostMetricJets | 13 | 0 | 13 |
| BoostHeatConstruction | 17 | 5 | 22 |
| Total | 76 | 14 | 90 |

[REAL — auditoria independente anterior ao selo] O auditor --build-only retornou BUILD_PASS/exit0: 2.066 arquivos de build, 207 registros históricos e 5/5 etapas PASS. O revisor conferiu também diretamente os metadados, logs, hashes das quatro fontes e binários, os 90 prints e os snapshots congelados, sem discrepância.

A derivação foi registrada antes dos fontes. O ambiente novo usa dependências históricas com pin conferido, incluindo043, e não inclui a raiz Chatgpt no LEAN_PATH. Todas as tentativas anteriores e os backups de bytes são preservados. O auditor examina metadados, logs, binários, fontes, importador e a cadeia histórica; o manifesto é criado após parecer e entrega para evitar circularidade de hashes.

Os binários históricos foram conferidos por hash, sem recompilação histórica. Fontes canônicos sem pin histórico de fonte servem à descoberta de imports, não a uma prova de proveniência até o binário. As dependências externas diretas são conferidas; o fechamento transitivo inteiro de Mathlib/toolchain não é hashado.

H3 a partir do estado: OPEN. Reconstrução gravitacional geral: OPEN. Meta ampla de gravidade quântica: OPEN. Gate canônico intocado.
