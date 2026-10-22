# Derivação055 — dinâmica microscópica de troca entre dois sítios

[DERIVED — anterior ao fonte ExchangeMicroscopicDynamics.lean; ainda sem compilação]

Autoria: Newton (/root/relative_operator_domains). Namespace previsto: ChatgptAudit.Exchange055.

A definição canônica chainIdx é recursiva: chainIdx 0=Fin 2 e chainIdx(N+1)=chainIdx N×Fin 2. Portanto o nível 1 possui os dois sítios pretendidos, sem deslocamento de índice.

Escolhemos e=diag(0,1), E0=e⊗I, E1=I⊗e e G=(X⊗X+Y⊗Y)/2. Em índices (00,01,10,11), G só troca 01 e 10. As identidades verificáveis por entradas são G*=G, G³=G e [G,E0+E1]=0. O perfil fiel P, a interação G, as energias de nível unitário e o parâmetro t são dados independentes; nenhum parâmetro geométrico entra.

Definimos a matriz explícita U(t)=I+(cos t−1)G²+i sin t G. Sua unitariedade, adjunto e derivada serão provados. No TowerHilbert real do projeto, o operador é a imagem de U por towerPi no nível 1. A igualdade com boundedPhase P (towerPi G) t não será presumida: o produto boundedPhase(-t)·towerPi(U(t)) tem derivada zero, vale I em zero e é constante pelo teorema do valor médio. O inverso unitário de boundedPhase então identifica as duas curvas para todo t.

O estado evoluído é ω_t(B)=ω(U(t)* B U(t)). Pela inclusão algébrica e omegaState_pi, a restrição de ω_t ao primeiro sítio é diagonal de peso p_t=p+(q−p)sin²t, p=P.w0 e q=P.w1. A igualdade será mostrada para toda matriz 2×2, incluindo entradas fora da diagonal. No segundo sítio, q_t=q+(p−q)sin²t. Assim, trata-se das marginais efetivas do estado, não de uma fórmula escalar postulada.

As transferências são diferenças de expectativas das energias: Q0(t)=ω_t(E0)−ω(E0)=(p−q)sin²t, Q1=−Q0. As correntes operatoriais Jj=i(EjG−GEj) são autoadjuntas. J0+J1=0 decorre da comutação de G com E0+E1. A continuidade será uma igualdade de derivada real: Qj'(t)=Re ω_t(Jj). A igualdade das expectativas totais é válida para todo tempo, sem hipótese de matching.

Usaremos funções escalares de ExchangeEntropyResponse quando disponíveis para evitar definições concorrentes. A inclusão dos operadores, as derivadas, as expectativas e as marginais devem ser ligadas literalmente aos objetos da torre. Nenhuma execução de um.py ou alteração de fontes anteriores é autorizada.

[OPEN] Esta energia microscópica não está identificada com fluxo material através de uma tela, o tempo não está identificado com o boost e não se constrói área espacial. A transferência entre pesos diferentes em geral muda o estado, portanto não é apresentada como TowerHorizon preservador de ω. A seleção física e H3 continuam abertas.

Emissão UTC: 2026-09-07T07:20:50.360046+00:00
