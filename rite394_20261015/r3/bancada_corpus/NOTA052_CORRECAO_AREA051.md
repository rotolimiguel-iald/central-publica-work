# Correção ao lado da candidata de área051 — pivô052

[DERIVED — revisão analítica; nenhum teorema052 compilado ou selo novo]

A NOTA051_AREA_COVARIANTE_PENDENTE permanece intacta. Sua família por E e I−E demonstra, sob as hipóteses indicadas, que covariância e uma normalização de traço não selecionam uma forma no espaço ampliado de amplitudes GNS. Estado, álgebra, esperança, ação e par de tangentes podem ficar fixos; a invariância transporta o par, não exige que cada horizonte o fixe. A normalização é relativa à célula escolhida e suas imagens transportadas. Esse negativo não classifica todas as formas invariantes.

A revisão adversarial encontrou dois limites decisivos. Primeiro, angularScreenGram034 já é definido pelo produto interno GNS efetivo: trocar o peso relativo para lambda diferente de1 muda esse critério, não prova não unicidade da forma já especificada. Segundo, no par misto Z/X da nota, Z pertence ao centralizador e não muda o estado sob a órbita unitária. A forma real GNS pode medir essa direção de amplitude mesmo quando todas as leituras no fator têm derivada zero, como demonstrado em AngularAreaObservability034. Portanto esse par não fornece duas direções efetivas de estados observáveis.

A definição canônica livre de fluxo de omegaCentralizer é omega(AB)=omega(BA) para todo B no fator. Com U(s)=exp(isA), a resposta é i*omega(BA−AB); ela anula as direções centralizantes. Após restringir aos representantes horizontais ker(E), h_lambda reduz-se a lambda vezes a forma GNS. A liberdade não escalar do exemplo misto desaparece nesse setor e, após calibração, resta o controle de escala já conhecido. Isso não invalida a álgebra da nota051, mas impede vendê-la como nova não unicidade da área operacional ou física.

## Pivô local positivo

Fixar o primeiro sítio, p=P.w0 em(0,1), r=2p−1 diferente de0 e V=span_real{X,Y}, com os operadores de Pauli035. Deve-se provar literalmente EX=EY=0 e a resposta da torre, sem tratar a densidade local como densidade de traço global.

Para rho_local=diag(p,1−p), delta_A rho=i[A,rho], logo delta_X rho=rY e delta_Y rho=−rX. As leituras locais X,Y de A=uX+vY respondem por(−2rv,2ru); determinante4r². Elas certificam tangentes independentes do estado global, não apenas uma matriz escolhida fora dele. O plano é tangente da órbita unitária de espectro fixo; não inclui todas as variações de estado ou todo ker(E) da torre.

X,Y são ortonormais para g_GNS(A,B)=Re omega(A*B). O fluxo modular atua por rotação de frequência nu=log(p)−log(1−p), com sigma_t(X)=cos(nu*t)X−sin(nu*t)Y. Uma forma bilinear real simétrica invariante pelo quarto de volta efetivo é c*g_GNS no plano. A condição tr_{g_GNS|V}(g)=1 equivale a g(X,X)+g(Y,Y)=1 e não depende da escolha de base GNS-ortonormal de V. Ela seleciona c=1/2, área1/2. O plano local e essa normalização permanecem explicitamente dados; isso não escolhe uma região física.

## Calibração distinta pela forma comutadora

Omega_q(A,B)=Im omega(A*B) é alternada nos geradores autoadjuntos e anula direções centralizantes. Em V, Omega_q(X,Y)=r. Com QX=sign(r)Y e QY=−sign(r)X, tem-se Q²=−I e g_Omega(u,v)=Omega_q(u,Qv)=|r|g_GNS(u,v). A área nesse par é|r|.

Nas convenções atuais, esse Q é realizado pelo horizonte no tempo −pi/(2|nu|). O quarter-turn de tempo positivo daria o sinal oposto para g_Omega nesta ordem dos argumentos. A identidade de compatibilidade correta é Omega_q(u,v)=−g_Omega(u,Qv)=g_Omega(Qu,v). Q é uma estrutura complexa real no plano, não a conjugação modular antilinear J de quadrado I.

Essa calibração usa dados já construídos do estado e da ação modular, sem escolher trace1. Entretanto, exigir compatibilidade com Omega_q e Q é um critério adicional à mera covariância. A forma resultante não deve ser identificada automaticamente com Fisher, Bures ou métrica espacial. As calibrações c=1/2 e c=|r| são distintas e devem receber enunciados separados.

## Limites e fontes

Em p=1/2, a resposta da órbita local é zero, a esperança fixa X,Y, a frequência modular e Omega_q são zero. Nenhum inverso de nu ou plano não degenerado de estados é admitido nesse controle. O tempo modular é usado como isotropia do estado-base; não vira relógio de uma curva não constante de estados, preservando040.

Fontes diretamente conferidas na bancada: TheOathOnTheTower.lean, omegaCentralizer/ExpectationInput/TowerHorizon; AperiodicCentralizerExpectation.lean, imagem/fixação/ortogonalidade; AperiodicTowerLift.lean, covariância por todos os horizontes; ChainSiteFlow.lean, modularConjugation_site; SitePauliObservables.lean, produtos e estados de Pauli; UnitaryStateDerivative.lean, unitary_expectation_derivative_zero; AngularScreenMetric.lean e AngularAreaObservability.lean, distinção entre amplitudes e leituras; HorizonAreaScale.lean e AffineClockAndRegion.lean, controles045/040. Os scripts052 devem preservar os pins e cópias históricas adequados, inclusive as instâncias nomeadas035.

Nas fontes examinadas, a prescrição GNS e a Fisher da medição especificada são critérios matemáticos já fixados, mas não existe uma identificação física demonstrada que os transforme por si em área gravitacional. H3, localização, colagem entre regiões, escala física e reconstrução geral permanecem OPEN. A052 proposta fornece seleção dentro de um bloco horizontal efetivo, não uma classificação global. Nenhuma escrita em051, Atlas, memórias, kernel ou um.py.

Emissão UTC: 2026-09-07T04:06:21.046380+00:00
