# Continuação045 A — permutações finitas como horizontes da torre

06/09/2026. Derivação anterior aos novos fontes. [DERIVED / INPUT / OPEN]

A ORDEM010 pede horizontes não modulares concretos e ação literal sobre sítios. O andar N contém N+1 sítios. A construção usará todos os elementos de Equiv.Perm (Fin (N+1)), sem trocar N por número de sítios.

1. Identificar recursivamente chainIdx N com as palavras Fin(N+1) → Fin2, preservando a ordem original: o último fator acrescentado é o sítio N. Um produto tensorial local tem entradas dadas pelo produto das entradas dos fatores. Provar a ligação dessa expressão ao towerStep, lastSiteMatrix e tPush existentes.

2. Uma permutação sigma dos sítios age nas palavras por deslocamento de coordenadas. Sua matriz V_sigma é uma matriz de permutação real, vista sobre complexos. Provar unitariedade, composição e conjugação dos produtos tensoriais. Em particular a conjugação deve enviar literalmente siteOperator P n a para siteOperator P (sigma n) a no prefixo, e fixar os sítios posteriores.

3. Para perfil estacionário P.w n=p, towerW P N é invariante por essa permutação. Logo V_sigma comuta com rhoD(towerW P N). Aplicar density_commuting_local_is_global_centralizer para obter towerPi P V_sigma no centralizador global.

4. Definir o implementador U_sigma=towerPi P V_sigma. A representação já possui completamento, produto, estrela e unidade certificados. U_sigma é unitário dentro do fator; normaliza o fator nas duas direções, e a ciclicidade do centralizador dá preservação de omega. Isso produz TowerHorizon sem assumir campos do alvo como hipóteses. Não requer reconstruir o fluxo modular nem uma extensão GNS nova.

TowerHorizon não exige que U_sigma fixe hOmega. O implementador interno aqui é diferente do implementador padrão da permutação em vetores GNS que fixa hOmega; ambos podem realizar a mesma ação em observáveis, mas não serão identificados.

A covariância da esperança resulta dos teoremas v329 the_lift_on_the_tower e the_lift_fires_on_the_stationary_tower, com controle tracial. Uma troca de sítios distintos move uma projeção local que o fluxo modular diagonal preserva; provar esse controle se a API existente permitir sem novos pressupostos.

O shift não será inventado: ausência de implementação existente deve permanecer visível. Não se deriva horizonte causal físico, área física, temperatura, fluxo modular geométrico ou H3. O perfil estacionário, a rede e a escolha dos sítios permanecem dados da construção.

Fontes novos autorizados: FiniteSitePermutations.lean e FiniteSiteHorizons.lean, namespace ChatgptAudit.Horizons045. Toda declaração terá impressão de axiomas; zero instância anônima, sorry, axiom ou native_decide. Sem compilação pelo autor nesta etapa. Originais, memórias e selos somente leitura; escrita apenas nos novos arquivos045, com backup de bytes antes de revisões e temporário verificado antes da substituição.
