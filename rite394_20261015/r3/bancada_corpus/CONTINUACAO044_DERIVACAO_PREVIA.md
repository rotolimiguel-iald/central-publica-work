# Continuação 044 — gerador de boost aproximado e orientação do calor
06/09/2026. Derivação anterior aos fontes. [DERIVED / INPUT / OPEN]

043 foi progresso efetivo, revalidado nesta retomada: manifesto PASS, 60 teoremas/15 definições/75 prints, 2308 arquivos, H3/QG OPEN, gate intocado. Os hashes do parecer, entrega e manifesto foram relidos dos bytes. Última ordem disponível009, nenhuma010. Não há fonte044 anterior. Escrita exclusivamente em Chatgpt; originais, um.py, Atlas, memórias, kernel e selos anteriores somente leitura.

Alvo alinhado: justificar o peso −kappa t usado em041/043 por um campo e fluxo geométricos efetivos. Construir somente uma obstrução a boost exato seria insuficiente: a reconstrução local de Jacobson usa boost aproximado. A construção positiva vem primeiro; o defeito de simetria é calculado para delimitar seu alcance.

Na carta029, u=x0+x3, v=(x0−x3)/2, X=x1,Y=x2:
g=2 du dv−dX²−dY²+H du², H=aX²+cY².
A parte cinemática deve valer para quaisquer a,c reais. A ligação à tela043 retém a,c≥0.

Campo: chi=−kappa u∂u+kappa v∂v, ou chi(x)=(-kappa x3,0,0,-kappa x0).
Fluxo: Phi_s(u,v,X,Y)=(exp(−kappa s)u,exp(kappa s)v,X,Y).
Matriz em (x0,x1,x2,x3): bloco nos índices0,3 com diagonal (exp(−kappa s)+exp(kappa s))/2 e fora da diagonal (exp(−kappa s)−exp(kappa s))/2; identidade nas duas direções transversais.
Provar grupo, inversa por −s, derivada temporal efetiva igual a chi(Phi_s), Jacobiano espacial igual à matriz, e preservação exata de eta4. Na curva gamma(t)=t d, d=(1/2,0,0,1/2), Phi_s(gamma(t))=gamma(exp(−kappa s)t) e chi(gamma(t))=−kappa t d. Para kappa>0,t<0, chi aponta no sentido temporal positivo da central.

Pullback efetivo por esse mapa linear:
Phi_s* g = g+(exp(−2kappa s)−1)H (w⊗w), w=du.
Não definir um “defeito” e apenas chamá-lo de pullback: usar M^T g(Phi_s x)M, com Jacobiano certificado. A derivada em s=0 deve corresponder à expressão de Lie em coordenadas:
(L_chi g)_ij = chi^k partial_k g_ij + g_kj partial_i chi^k + g_ik partial_j chi^k.
Ela vale −2kappa H w⊗w.

Na central X=Y=0, o defeito de Lie e todas suas primeiras derivadas espaciais zeram. As segundas derivadas transversais são −4kappa a w⊗w e −4kappa c w⊗w. Isso é controle exato de ordem, não “Killing exato”. O campo é Killing para a família inteira se kappa=0 ou a=c=0; se kappa≠0 e algum parâmetro nãozero, o resíduo impede igualdade exata num aberto contendo a origem. Para cada mapa Phi_s, qualquer alegação negativa exige s≠0, pois Phi_0=identidade. Não se precisa anunciar inexistência de TODA isometria com prescrição semelhante; a naturalidade global de Ricci não está paga aqui.

Calor: para qualquer tensor bilinear T,
T(chi(gamma(t)),d)=−kappa t T(d,d).
Multiplicar pela área043 liga o fluxo efetivo de energia do boost ao screenHeatFlux da mesma tela, sem inserir Clausius. Para waveMatter, ligar à integral041 e ao constructedHeat043 germinal no passado. Não promover a identidade central a chi=−kappa lambda V fora da central.

Orientação: Q043(t)=integral de0 até t, enquanto o segmento passado→origem usa Q_segment(t)=integral de t até0=−Q043(t), e DeltaA_segment=A(0)−A(t). Os dois sinais se invertem juntos. O matching quadrático permanece eta(a+c)=2pi m, para kappa≠0. Esse sinal deve ficar explícito; calor orientado negativo não é automaticamente fluxo físico negativo.

Módulos planejados, namespace ChatgptAudit.Boost044:
1. ApproximateBoostFlow — campo, matriz, fluxo, grupo e derivadas; identidades na central.
2. BoostMetricPullback — pullback verdadeiro, expressão de Lie e derivada do pullback.
3. BoostMetricJets — ordem do defeito, controles planos/taxa zero e falha local de Killing exato para esse campo.
4. BoostHeatConstruction — corrente efetiva e ligação literal ao calor043; orientação de segmento e balanço.

Não introduzir temperatura física por definição. O escalar kappa/(2pi), quando reaproveitado no balanço existente, permanece normalização INPUT até que efeito Unruh/KMS e identificação do fluxo do estado sejam demonstrados. Também não se deriva a escala kappa, a métrica, eta, matéria ou H3 do estado. A ambiguidade de escala de kappa cancela no balanço normalizado, mas não seleciona um relógio modular.

Referência primária consultada: Jacobson, “Thermodynamics of Spacetime: The Einstein Equation of State”, arXiv:gr-qc/9504004v2, eqs(1)–(2) e discussão do campo de Killing aproximado, https://arxiv.org/pdf/gr-qc/9504004. O artigo usa temperatura Unruh e entropia proporcional à área como entradas físicas adicionais. A aproximação geométrica não as demonstra.

Auditoria: derivação antes do código; cada definição/teorema com #print axioms; zero instâncias anônimas; compilação serial em diretório novo, importador conjunto, somente os três axiomas-base aceitos. Fronteira histórica pinada incluindo043; sem raizChatgpt no LEAN_PATH. Backup imediato de bytes em revisões próprias não seladas. Revisão independente antes e depois do selo. H3 e objetivo amplo de gravidade quântica continuam OPEN.
