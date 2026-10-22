[REAL / INPUT / KNOWN / OPEN] Continuação espontânea 010 — focalização e reconstrução a partir de balanço local de calor e área.

## Resultado e alcance

A reconstrução da entrega 009 recebia diretamente a igualdade de Ricci e matéria no cone nulo. Esta continuação deriva essa igualdade de dados locais explícitos: campo geodésico em equilíbrio, uma curva tangente no ponto, funções de área e calor com suas leis de derivação e um resíduo integrado de Clausius que é o(λ²) no ramo passado. O resultado final é

    G_geom[g] + Λg = (2π/η) T,

com Λ constante no domínio aberto preconexo da carta, η constante e não nula, e T conservado. Em unidades ħ=1, a escolha η=1/(4G) dá 8πG. Essa escolha continua entrada física. A taxa do horizonte pode variar entre os testemunhos; só é exigida sua não nulidade, e ela cancela na dedução.

A cadeia usa o mesmo Γ de Levi-Civita, a mesma curvatura, Ricci e G da continuação 009. Não foi introduzido um campo de Ricci com a conclusão desejada como hipótese.

## O elo diferencial construído

Para um campo vetorial V e uma conexão sem torção, ambos suaves no aberto, os fontes definem por derivadas reais:

    Bᵃᵢ = ∂ᵢVᵃ + Γᵃᵢb Vᵇ,
    θ = tr B,
    a = BV,
    Cᵢ = ∂ᵢB + ΓᵢB − BΓᵢ.

O comutador de derivadas covariantes é identificado com FᵢⱼV. A contração resulta em

    D_V θ = div a − tr(B²) − Ric(V,V).

Esse enunciado é geral para campos na carta, sem impor nulidade de V e sem impor equilíbrio. Para um campo geodésico na vizinhança, com B=0 no ponto, segue D_Vθ=−Ric(V,V). A regra da cadeia transporta essa derivada para qualquer curva com o vetor tangente V naquele ponto.

**Delimitação do equilíbrio:** B=0 é mais forte que anular apenas expansão e cisalhamento da tela. A decomposição em cisalhamento, expansão e torção ópticos, e a identificação de tr B com a expansão de uma área transversal geométrica, não foram formalizadas nesta continuação. As matrizes e a identidade diferencial não dependem dessa identificação.

## O elo analítico

Com funções θ, A e m ao longo do parâmetro, o resíduo de fluxo é

    r(λ) = −κ λ m(λ) A(λ) − [κ/(2π)] η θ(λ) A(λ).

A derivada de θ no equilíbrio fornece o limite de r(λ)/λ quando λ→0 pelo lado negativo. Sob continuidade de A e m, A(0)≠0 e κ≠0, esse limite é zero somente se Ric(v,v)=(2π/η)m(0).

O resíduo integrado é uma função efetiva dos dados:

    F(λ) = Q(λ) − [κ/(2π)] η [A(λ)−A(0)].

As leis A'=θA e Q'=−κλmA implicam F'=r. Um lema de L'Hôpital prova que, se r(λ)/λ→c e F(0)=0, então F(λ)/λ²→c/2. Portanto o requisito F(λ)/λ²→0 implica o balanço nulo de Ricci. Não se exige F identicamente zero em intervalos finitos.

Q e a diferença de área têm orientação de 0 para λ<0. Inverter ambos para a orientação física de λ até 0 muda os dois sinais, preservando a condição de resíduo nulo. Essa convenção evita trocar o sinal do ramo passado pela mera aparência das fórmulas.

## O contrato e o teorema final

LocalHorizonPencil guarda uma vizinhança aberta contida na carta, V suave e nulo, V(x)=v, aceleração zero na vizinhança, B(x)=0, uma curva com ponto e tangente dados, κ≠0, A(0)≠0, Q(0)=0, continuidade, as duas leis de derivação e o resíduo o(λ²).

A curva só precisa coincidir com a trajetória do campo até a primeira derivada no ponto; não se construiu aqui o fluxo geodésico completo. As funções de área e calor são dados com leis explícitas. Não se provou que A é o determinante de uma tela geométrica ou que Q é obtido de um estado quântico específico.

pencil_ricci_balance deduz a contração de Ricci de cada testemunho. horizon_einstein_reconstruction recebe testemunhos para todas as direções nulas em todos os pontos, além de E,D suaves inversos e T simétrico conservado. Descarrega o balanço nulo do teorema de 009; a conservação do G geométrico continua provada, não assumida.

**A existência desses testemunhos na situação física pretendida continua [INPUT/OPEN].** A substituição de um balanço algébrico por dados de horizonte não é uma demonstração de H3 a partir da dinâmica modular.

## Controles e relação com KMS

Os controles têm escopos distintos:

- Uma escolha escalar com θ=−λ, A=exp(−λ²/2), m=1, κ=1 e η=2π anula o resíduo de fluxo exatamente. Esse controle testa o sinal e o coeficiente da fórmula local.
- flatHorizonPencil constrói o contrato completo no caso plano g=η_mink, Γ=0, T=0, V=v constante nulo, γ(λ)=λv, A=1, Q=0. O vetor v=(1,1,0,0) é não zero. Isso verifica a não-vacuidade do contrato; não estabelece sua existência em métricas curvas gerais.
- No controle curvo de 009, g=exp(2x⁰)η_mink e Ric=diag(0,2,2,2). Em x=0, v=(1,1,0,0) é nulo e Ric(v,v)=2. Com T=0 e η≠0, não existe testemunho LocalHorizonPencil com todos os campos exigidos.
- O certificado KMS algébrico de towerEquilibriumInput pode coexistir com esse par independente de geometria e matéria incompatíveis. O teorema usa a definição canônica efetiva, não uma nova definição chamada KMS.

O último controle refuta apenas a inferência universal de KMS para um balanço de horizonte sobre dados geométricos e materiais arbitrariamente escolhidos. Não refuta uma futura ponte que vincule corretamente estado, métrica e matéria; mostra que essa vinculação é uma obrigação real.

## O que foi pago e o que permanece aberto

| Elo | Estatuto |
|---|---|
| Derivadas vetoriais e comutador com a curvatura efetiva | [REAL] |
| Identidade diferencial geral D_Vθ=div a−tr(B²)−Ric(V,V) | [REAL] |
| Focalização no equilíbrio B=0 e transporte da derivada para uma curva | [REAL], sob as hipóteses indicadas |
| Resíduo integrado o(λ²) ⇒ balanço nulo de Ricci | [REAL], com leis de derivação, continuidade e fatores não nulos |
| Reconstrução com G geométrico e Λ constante | [REAL] como implicação |
| Consistência do contrato completo em caso plano não trivial na direção nula | [REAL], verificação registrada no manifesto |
| Área geométrica da tela, existência geral das congruências/testemunhos, lei de entropia e calor oriundos da dinâmica | [OPEN/INPUT] |
| Assinatura, quatro dimensões, origem do referencial, colagem global e gravitação quântica completa | [OPEN] |

[KNOWN] A rota termodinâmica clássica toma entropia de área, temperatura de Unruh e equilíbrio local como hipóteses. A fonte primária consultada foi [Ted Jacobson, 1995](https://arxiv.org/html/gr-qc/9504004), especialmente as relações entre fluxo, focalização e equação de estado. A referência não foi usada como axioma Lean nem como prova de que um estado abstrato fornece H3.

## Custódia e integração

O manifesto lê contagens dos fontes e hashes dos bytes; registra logs finais, #print axioms, versões intermediárias e tentativas rejeitadas. A derivação foi registrada antes do código principal; o controle curvo reutiliza o cálculo prévio de 009, e o habitante plano recebeu adendo prévio próprio. A aprovação independente continua sendo da gerência.

Somente Chatgpt recebeu escritas. Nenhum um.py foi executado, importado ou editado. Kernel canônico, Atlas, memórias, selos, gate e entregas anteriores permaneceram intactos. A solução ampla de gravitação quântica não foi declarada concluída.
