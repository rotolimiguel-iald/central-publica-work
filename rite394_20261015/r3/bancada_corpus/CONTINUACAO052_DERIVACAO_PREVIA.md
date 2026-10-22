# Continuação052 — tangentes efetivos e seleção angular no primeiro sítio
[DERIVED — derivação prévia; nenhum teorema052 compilado]

## Estado e decisão
A051 foi revalidada por auditoria somente leitura: PASS selado,45T/10D/55prints. A ordem vigente ainda é010. Esta rodada trata seu alvoC, dentro da meta maior de reconstrução; H3 e QG geral continuam OPEN.

A proposta NOTA051_AREA_COVARIANTE_PENDENTE permanece preservada. Sua família h_lambda em E e I-E pode variar formas no espaço ampliado GNS, mas a034 já especifica a forma GNS e o setor centralizante E é vertical para a órbita unitária do estado. O par Z/X proposto não dá duas direções efetivas do estado. Assim a nota não será promovida a uma nova não unicidade de área física. A construção052 examina o setor horizontal local verdadeiro.

## Dados reais e horizontalidade
Fixar SiteProfile P, p=P.w0∈(0,1), r=2p−1 e nu=log p−log(1−p), com p≠1/2. Os operadores são sitePauliX/Y P 0 já construídos035; a esperança é aperiodicExpectationInput P já construída046.
O teorema global_expectation_restricts_to_pinching liga essa esperança ao pinching local. No sítio0 não tracial, EX=EY=0. X,Y são autoadjuntos, centrados e normalizados em GNS; Re〈XΩ,YΩ〉=0 e Im〈XΩ,YΩ〉=r.
O plano real de geradores A=uX+vY representa direções efetivas da ÓRBITA UNITÁRIA, não todos os tangentes de estados (variações de autovalores ficam fora). Para ρp=diag(p,1−p), δρ=i[A,ρp]=r(uY−vX). As derivadas globais de leituras locais X,Y são (−2rv,2ru); o determinante4r² torna esse mapa injetivo se r≠0. Evitar substituir este elo com a torre por uma matriz sem identificação.
A igualdade kerE=span_R{X,Y}, se formalizada, refere-se somente ao espaço autoadjunto de um sítio; não ao núcleo global.

## Horizonte e seleção
O horizonte real modularHorizon P t já tem seus campos provados045. Sua ação no plano satisfaz:
σ_t(X)=cos(nu*t)X−sin(nu*t)Y,
σ_t(Y)=sin(nu*t)X+cos(nu*t)Y.
Com t=−π/(2nu), X→Y e Y→−X. A invariância de uma forma real simétrica por esse quarto de volta força Gram=cI. A normalização de traço1 dá c=1/2 e área1/2 no par escolhido. A isotropia deriva da simetria efetiva; a escala dessa versão é INPUT da normalização.

## Calibração pela forma comutadora
Definir Ω_q(A,B)=Im ω(A*B), para geradores autoadjuntos. A ortogonalidade/ciclicidade faz a parcela centralizante desaparecer nessa forma alternada; no plano Ω_q(u,v)=r(u0*v1−u1*v0).
A escolha de orientação compatível positiva é QX=sign(r)Y, QY=−sign(r)X, realizada pelo horizonte no tempo NEGATIVO −π/(2|nu|). O quarto de volta no tempo positivo teria sinal oposto e produziria métrica negativa nesta ordem dos argumentos.
Construir gΩ(u,v)=Ω_q(u,Qv)=|r|dot(u,v); área|r|. Na convenção adotada, Ω_q(u,v)=−gΩ(u,Qv)=gΩ(Qu,v). Q²=−I no plano e Q não é a conjugação modular J (que é antilinear e tem quadrado I).
Esta é uma calibração geométrica explícita pela forma comutadora e pela orientação modular. Não é prova de que seja Fisher, Bures, métrica espacial ou área gravitacional. A compatibilidade usada deve aparecer no enunciado de qualquer alegação de seleção. Não confundir a calibração gΩ com a versão normalizada de traço1, que em geral tem outra escala.

## Controle tracial e alcance
Em p=1/2, a órbita unitária local reduz-se ao estado fixo, a respostaXY é zero, o módulo local é identidade, a esperança fixaX,Y e Ω_q=0. O procedimento não é não degenerado nesse ponto. Nenhuma fórmula com 1/nu pode ser aplicada sem hipótese.
O resultado pretendido é local ao primeiro sítio e a uma órbita unitária. A dimensão física, localização, colagem entre regiões, seleção da área física, termodinâmica e H3 permanecem OPEN. O fluxo modular aqui age como isotropia; não se torna relógio de uma curva de estados, preservando a obstrução040.

## Literatura e estatutos
[KNOWN — contexto, não axioma Lean] Petz–Sudar, Extending the Fisher metric to density matrices: https://arxiv.org/abs/quant-ph/0102132, discute a família não única de métricas quânticas monótonas. Contreras–Ercolessi–Schiavina, On the geometry of mixed states and the Fisher information tensor: https://arxiv.org/abs/1501.00054, distingue geometria de órbitas, tensor Fisher e forma simplética. Os resumos primários foram lidos; nenhuma identificação técnica além do que for provado localmente será atribuída a eles.

## Custódia
Somente arquivos novos e cópias em Chatgpt. Originais, um.py, kernel, Atlas, índice, memórias e selos≤051 somente leitura. Derivação antes de cada fonte, backup exato antes de revisão, pasta limpa exclusiva, prints de todas declarações/instâncias nomeadas, zero avisos/erros, revisão independente por autoria e auditoria.
Módulos previstos: LocalHorizontalPauli, ModularHorizontalRotation, HorizontalAreaSelection, QuantumOrbitArea. Namespace ChatgptAudit.Orbit052. Não há alteração do gate canônico.

Emissão UTC: 2026-09-07T04:04:22.600884+00:00
