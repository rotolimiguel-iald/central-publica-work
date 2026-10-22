# Continuação 043 — tela efetiva e calor construído

06/09/2026. [REAL / DERIVED / INPUT / OPEN]. Compilação final e auditoria independente do build concluídas. Complemento à ORDEM009; o manifesto final reúne a custódia desta entrega.

Esta etapa liga a curva e os campos de Jacobi explícitos036 a um habitante concreto de EquilibriumScreenData. Isso permite comparar o constructedHeat dessa mesma tela com o calor041. Uma tela abstrata já existia019; o avanço pretendido é certificar as funções literais036, incluindo a congruência no bairro, sem inserir Clausius no construtor.

## A precisão angular do operador

[ONTO / CONJECTURE] O operador distingue L, interpretado como cauda ou poço, do módulo da inscrição quadrática produzida por sua angulação. A leitura mais fiel dessa proposta envolve a projeção ou a variação de fase. Não se presume que ele tenha definido a inscrição como U*U. O Atlas consultado diz “raiz do módulo produzido pela fase”, e sua direção luz→gravidade é marcada como ONTO. Não identificamos L_phi do Atlas com L=log H da030 sem uma ponte própria.

[DERIVED — construção ilustrativa, fora dos módulos043] Se U é unitário e P_in,P_out são projeções ortogonais, a amplitude de passagem R=P_out U P_in define E=R*R, com 0≤E≤P_in. Um estado normalizado pode medir omega(E), um peso quadrático de passagem. Esse peso pode variar apesar de U*U=I. Portanto a unitariedade da fase não impede uma inscrição quadrática não trivial após projeção. A escolha das projeções faz parte da construção; não é derivada aqui do estado. Isso não demonstra variação na família centralizante atual: com P_in=I e P_out em M, omega(R*R)=omega(P_out) permanece constante. Uma variação exige um protocolo de preparação/projeção ou observáveis que efetivamente a produzam.

[KNOWN / DERIVED] Para duas direções de variação horizontal v_1,v_2 no espaço projetivo de vetores normalizados, G_ab=Re〈v_a,v_b〉 é uma forma quadrática positiva semidefinida. Ela define a densidade de área sqrt(det G). Uma só direção repetida dá determinante zero. A distinção é entre a amplitude, sua forma quadrática e a medida de área obtida dessa forma. Um único peso angular não determina sozinho uma métrica de duas dimensões. Referência primária: Kolodrubetz et al., https://arxiv.org/abs/1602.01062. A ponte da métrica de estados à área física, com normalização e unidades, continua OPEN.

[DERIVED — álgebra, fora dos módulos043] Existe um caso exato da leitura proposta pelo operador. Se duas direções ortogonais têm amplitude comum r(theta), G=|r(theta)|² I_2 implica sqrt(det G)=|r(theta)|². Com amplitudes diferentes, G=diag(|r_1|²,|r_2|²) fornece sqrt(det G)=|r_1 r_2|. Assim, uma densidade de área pode coincidir com um módulo quadrático sob essas hipóteses, que precisam ser derivadas no modelo. Na tela043 isotrópica a=c, o Gram espacial negativo é −cos²(√a t)I_2 e a área é cos²(√a t). Essa identidade funcional vale globalmente; a certificação como tela regular fica onde o cosseno não zera. Isso não identifica a amplitude de Jacobi com uma projeção de exp(i theta L), nem deriva isotropia, métrica ou escala física do estado. A034 mostra também que uma área dos raios GNS pode ser positiva enquanto o estado restrito a M permanece constante.

O cálculo de fases também não demonstra o retorno estabilizador. O módulo quadrático pode perder orientação; uma dinâmica deve especificar o transporte e provar estabilidade. Reversibilidade, positividade e existência de equilíbrio são propriedades diferentes. A face hiperbólica e a leitura angular permanecem distintas. Esta043 estuda transporte geométrico local de raios em uma métrica já escolhida; não identifica essa métrica com a inscrição proposta.

## Congruência explícita

[INPUT] Usamos a carta029, assinatura +--- e a família de métricas
g=2 du dv−dX²−dY²+(aX²+cY²)du²,
com u=x0+x3, v=(x0−x3)/2 e a,c≥0.

[REAL — teoremas043 compilados] Se F=cos(√a u), G=cos(√c u), q_a=F'/F e q_c=G'/G, o domínio N={F≠0 e G≠0} é aberto e contém a origem. Um bairro da origem precede as cáusticas. N inteiro pode ser desconexo; não o chamamos inteiro de região anterior à primeira cáustica.

As equações de Riccati são q_a'=−a−q_a² e q_c'=−c−q_c². Defina
B=[(q_a²−a)X²+(q_c²−c)Y²]/2
e V=(1/2+B,q_a X,q_c Y,1/2−B).
O campo é suave em N, não nulo, nulo para g e geodésico para a conexão de Levi-Civita. Na curva central gamma(t)=t(1/2,0,0,1/2), V=gamma' e seu gradiente covariante é diag(0,q_a,q_c,0), zero na origem.

[DERIVED — consequência analítica] Aqui “equilíbrio” significa gradiente zero no ponto escolhido. Pela própria equação de Riccati, q_a(0)=0 e q_a'(0)=−a. Para a>0, o valor zero não é uma solução estacionária dessa equação. O fator de Jacobi zera em pi/(2 sqrt(a)), e a certificação regular não atravessa esse ponto. Isso não demonstra instabilidade de uma solução; demonstra que o equilíbrio instantâneo certificado não é, por si, um teorema de retorno estável.

A tela usa literalmente as colunas036 [F(t)e1,G(t)e2]. O frame completo tem colunas [d,−waveRaised,F e1,G e2], cujo parceiro nulo obedece g(d,n)=−1. Sua inversa só é certificada onde F e G não zeram. A taxa de área decorre do teorema geométrico de transporte existente.

O construtor opticalEquilibriumScreen recebe apenas a,c e suas não negatividades. Não recebe estado, matéria, entropia, eta, calor ou casamento de Clausius. A área é literalmente geometricJacobiArea036=|F G|, normalizada a1 na origem.

## Calor efetivo e condição independente de balanço

[REAL — teoremas043 compilados] Para qualquer massa m e taxa kappa, o fluxo da tela é
screenHeatFlux=−kappa t m |F(t)G(t)|.
opticalScreenHeat instancia constructedHeat com a tela explícita e waveMatter. Como esse construtor usa uma extensão contínua do passado, sua identificação com opticalHeat041 vale como germe em t→0−. Não se afirma igualdade global de extensões escolhidas arbitrariamente. A igualdade local das integrais inclui o ponto0 e todo intervalo suficientemente pequeno entre t e0.

O defeito D=Q−[kappa/(2pi)]eta[A(t)−A(0)] satisfaz
lim D(t)/t²=kappa[eta(a+c)−2pi m]/(4pi).
Para kappa≠0, o balanço quadrático equivale a eta(a+c)=2pi m. Assim, construir a geometria não impõe esse casamento.

Controle: a=c=0 produz uma tela plana com A=1, mas m≠0 e kappa≠0 impedem balanço quadrático. Sob casamento e kappa,eta>0,a+c>0,
lim D(t)/t⁴=kappa eta(a²+c²)/(24pi)>0.
O resíduo positivo impede igualdade finita exata nesse modelo e preserva o balanço infinitesimal. Não é um defeito de sinal negativo nem uma refutação de todo balanço termodinâmico possível.

## Verificação e alcance

[REAL — compilação final e auditoria independente] Em CONTINUACAO043_CLEAN_20260906_215833_696140, os quatro módulos e Imports043All passaram: 60 teoremas, 15 definições, 75 impressões de axiomas e zero instâncias. Os cinco passos retornaram exit0/PASS, sem erros ou advertências, com cobertura exata e apenas propext, Classical.choice e Quot.sound. As quatro fontes de trabalho são idênticas às cópias compiladas; os snapshots de 2.029 entradas congeladas permaneceram idênticos em bytes. O auditor independente --build-only retornou BUILD_PASS/exit0, conferindo 2.048 arquivos de build e 180 registros históricos. O revisor também conferiu diretamente os cinco metadados, logs, hashes de fonte/binário, o censo real das linhas de axiomas e o importador literal. As tentativas anteriores e os backups foram preservados. O manifesto final será produzido depois do parecer e da entrega; sua auditoria somente leitura confere a custódia completa.

A derivação foi registrada antes dos fontes. Os quatro módulos são JacobiRiccatiProfile, OpticalNullCongruence, OpticalEquilibriumScreen e OpticalConstructedHeat, namespace Optical043. Cada definição e teorema tem impressão de axiomas; o importador conjunto passou. O ambiente novo usa fronteira histórica pinada, sem a raiz Chatgpt no LEAN_PATH. As tentativas e backups de bytes são preservados.

Os binários históricos são conferidos por hash, sem recompilação nesta etapa. Fontes canônicos sem pin histórico de fonte servem à descoberta de imports, não a uma prova de proveniência até o binário. As dependências externas diretas são conferidas; o fechamento transitivo inteiro de Mathlib/toolchain não é hashado.

Referências de contexto: Blau–O'Loughlin–Seri, apêndiceA, https://arxiv.org/pdf/1112.3182; Jacobson, equações1–5, https://arxiv.org/pdf/gr-qc/9504004. A construção aqui continua condicionada à métrica, à carta e à normalização afim escolhidas. Não deriva relógio canônico do estado nem identifica o peso −kappa t com um gerador físico de Killing ou modular em todas as ordens. Não constrói horizonte causal global nem atravessa as cáusticas.

Originais, um.py, kernel canônico, Atlas, memórias, gates e entregas anteriores permanecem somente leitura. Escritas somente em Chatgpt.

H3 a partir do estado: OPEN. Reconstrução gravitacional geral: OPEN. Meta ampla de gravidade quântica: OPEN. Gate canônico intocado.
