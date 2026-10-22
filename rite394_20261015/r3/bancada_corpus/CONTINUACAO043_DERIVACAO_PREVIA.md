# Continuação 043 — congruência efetiva da tela de Jacobi e calor construído
06/09/2026. Derivação anterior aos fontes. [DERIVED / INPUT / OPEN]

A etapa042 foi progresso: manifesto relido nesta continuação, PASS, 52 teoremas/12 definições/64 prints, 2209 arquivos, H3/QG OPEN. Os três hashes principais foram relidos dos bytes. Última ordem disponível:009. A revalidação normal do um.py foi impedida por acesso; a consulta com acesso ampliado leu metadados, sem executar nem editar o programa. Não se atribui aqui uma versão canônica nova sem conferência explícita. Não há arquivos043 anteriores. Originais, Atlas, memórias, kernel e selos anteriores permanecem somente leitura; escrita exclusiva em Chatgpt.

Alvo crítico: remover a lacuna041 entre a curva/tela explícita036 e o tipo EquilibriumScreenData, e provar que seu calor constructedHeat coincide como germe no passado com opticalHeat041. A existência de uma tela abstrata já está paga em019; outro Nonempty não basta. Curva e colunas devem ser literalmente as de036. O construtor geométrico não recebe matéria, entropia, eta, estado ou Clausius.

Na carta029, u=x0+x3 e v=(x0−x3)/2:
g=2 du dv−dx1²−dx2²+(a x1²+c x2²)du².
Fixam-se a,c≥0. F(u)=jacobiOscillator(a,u)=cos(√a u), G(u)=cos(√c u).
Defina q_a=F'/F e q_c=G'/G no aberto N onde F e G não zeram. Inclui a origem e um bairro sem cáusticas. A razão é uma função Lean global por divisão totalizada, mas sua suavidade e as identidades diferenciais só são afirmadas em N.
Riccati: q_a'=−a−q_a² e q_c'=−c−q_c².

Escreva X=x1, Y=x2 e B=[(q_a²−a)X²+(q_c²−c)Y²]/2.
V=(1/2+B,q_a X,q_c Y,1/2−B).
Temos du(V)=1, logo V≠0, e g(V,V)=0. Sua derivada covariante inteira é
[[-E,q_a²X,q_c²Y,−E],
 [−q_a²X,q_a,0,−q_a²X],
 [−q_c²Y,0,q_c,−q_c²Y],
 [E,−q_a²X,−q_c²Y,E]],
onde E=q_a³X²+q_c³Y². Multiplicada por V, dá zero: V é geodésico. O traço é q_a+q_c. Na curva central γ(t)=t d, d=(1/2,0,0,1/2), V(γ)=d e a matriz se reduz a diag(0,q_a,q_c,0). Na origem ela é zero.

A tela é exatamente S(t)=[F(t)e1,G(t)e2]=geometricJacobiColumns. O frame completo usa colunas [d,−waveRaised,F e1,G e2]; o sinal menos é obrigatório porque nullScreenGram usa g(d,n)=−1. Sua inversa tem linhas (1,0,0,1), (−1/2,0,0,1/2), (0,1/F,0,0), (0,0,1/G,0). O Gram é nullScreenGram(diag(−F²,−G²)), a conexão ao longo da central é zero, e q_a F=F', q_c G=G' dão o transporte. Pode-se usar LocalFrameFlow explícito e geometricScreenFromFlow se isso preserva definicionalmente as colunas; nenhuma escolha abstrata substitui a identificação. A lei de área segue de geometric_screen_area_rate, ou diretamente da derivada do produto localmente positivo.

P(a,c):EquilibriumScreenData univ g Γ 0 d deve usar N, V, γ e S acima. P não recebe m,η,b ou matching. Depois, para qualquer m e κ, screenHeatFlux(P,waveMatter,κ)=opticalHeatFlux041. Como constructedHeat usa PastContinuousExtension, a conclusão natural é igualdade eventualmente em t→0− com opticalHeat041, não igualdade global de extensões arbitrárias.

A ponte deve transportar os coeficientes existentes. Sem matching, o balanço dividido por t² tende a κ[η(a+c)−2πm]/(4π). Sob η(a+c)=2πm, transporta-se o coeficiente quártico κη(a²+c²)/(24π) e o negativo finito041. Controle adversarial obrigatório: a=c=0,m>0,κ≠0. P existe e A=1, mas Q=−κmt²/2 e H3 quadrático falha. Isso certifica que o construtor geométrico não esconde Clausius.

Módulos planejados, namespace ChatgptAudit.Optical043:
1. JacobiRiccatiProfile — razões de Jacobi, regularidade e domínio.
2. OpticalNullCongruence — campo V e certificados nulo/geodésico/gradiente.
3. OpticalEquilibriumScreen — frame/tela/construtor P literal036.
4. OpticalConstructedHeat — igualdade germinal, coeficientes e controles.

Todo def/teorema terá #print axioms; nenhuma instância anônima, sorry ou axioma extra. Compilação serial em diretório novo com importador conjunto. Fronteira histórica pinada, agora incluindo041; auditor integral adaptado042, revisão independente. Backups exatos de bytes antes de cada revisão própria não selada. Nada altera043 depois do manifesto.

Referências primárias de contexto conferidas pelo revisor: Blau–O'Loughlin–Seri, arXiv1112.3182, apêndiceA (Rosen/Brinkmann e ODE), https://arxiv.org/pdf/1112.3182; Jacobson gr-qc/9504004, equações1–5, https://arxiv.org/pdf/gr-qc/9504004. A lei de Clausius e a entropia proporcional à área são premissas físicas adicionais nessa construção de contexto.

Limites: a carta, a família de métricas e a normalização afim continuam INPUT. Não se deriva a métrica do estado, não se seleciona relógio canônico, não se identifica o peso afim exato com gerador de Killing/modular físico em todas as ordens. Há cáusticas fora do bairro: não se reivindica congruência global regular. H3 do estado e gravidade quântica geral permanecem OPEN.
