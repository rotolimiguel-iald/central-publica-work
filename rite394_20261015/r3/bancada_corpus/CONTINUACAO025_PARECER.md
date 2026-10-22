[REAL / INPUT / OPEN] CONTINUAÇÃO 025 — perfil térmico global, limite da preparação e dependência do corte

06/09/2026. Esta etapa mostra o que acontece com a construção de 024 ao aumentar o número de sítios. Há um perfil térmico compatível em todos os andares, mas, no caso estacionário não tracial, a preparação vetorial específica não converge em norma no espaço original. A resposta escolhida depende do corte; uma escala explícita estabiliza seu coeficiente e, ao mesmo tempo, faz cada observável local retornar à referência.

A etapa 024 é classificada como PROGRESSO: seu auditor foi reexecutado e conferiu 684 hashes, sete módulos, 85 teoremas e três definições impressas. O túnel continua com ordens 001–007. A árvore canônica consultada mantém H3 como INPUT; o objetivo amplo de gravidade quântica permanece aberto.

## Compatibilidade e representação global

[REAL] Para pesos estritamente positivos p e q, a perturbação de Gibbs de 024 satisfaz

    K_(p⊗q)(i,j) = K_p(i) + K_q(j)
    Z_(p⊗q)(s) = Z_p(s) Z_q(s)
    r_(p⊗q)(s) = r_p(s) ⊗ r_q(s).

Define-se thermalProfile(P,s) com peso do sítio n igual à coordenada zero de r_(siteW(P.w n))(s). Esse peso pertence a (0,1), comprovadamente, e

    towerW(thermalProfile(P,s),N) = r_(towerW(P,N))(s)

para todo andar finito N. A construção canônica da torre aplicada a esse novo perfil fornece sua representação H(P_s) e um estado fiel na álgebra representada. Não se identifica automaticamente essa representação com H(P).

[REAL] Para um observável a no andar L e qualquer N≥L, o estado preparado no espaço original satisfaz

    ω_s^(N)(π_P(a)) = ω_s^(L)(π_P(a))
                   = ω_(P_s)(π_(P_s)(a)).

Isso demonstra compatibilidade das marginais de preparações feitas em andares diferentes. É mais forte que a igualdade entre duas representações do mesmo observável, já obtida em 024. Ainda assim, não prova convergência dos vetores dessas preparações.

## A distância que decide o limite em norma

Defina a afinidade finita

    c(p,r) = Σ_i sqrt(p_i) sqrt(r_i).

[REAL] Para pesos positivos normalizados, 0<c≤1, e c=1 exatamente quando p=r. A identidade usada é

    Σ_i [sqrt(p_i)-sqrt(r_i)]² = 2-2c(p,r).

A afinidade é multiplicativa sob produtos. Para r=r_p(s), com s≠0, a igualdade r=p força p tracial: a identidade de log dos pesos dá s(K_i-K_j)=0 para todos i,j.

Na preparação efetiva Ψ_N(s)=π_P(a_s^(N))Ω de 024, foram calculados no H(P) original:

    ⟨Ω, Ψ_N(s)⟩ = produto das afinidades dos sítios até N
    ||Ψ_N(s)-Ψ_(N+1)(s)||² = 2[1-c_site(N+1,s)].

[REAL] Se P é constante, com peso q∈(0,1), q≠1/2, e s≠0 é fixo, a afinidade de sítio é uma constante c∈(0,1). Logo

    ⟨Ω, Ψ_N(s)⟩ = c^(N+1) → 0
    ||Ψ_N(s)-Ψ_(N+1)(s)||² = 2(1-c) > 0.

A sequência não é Cauchy e não converge em norma a vetor algum de H(P). Os enunciados são thermal_vectors_not_cauchy e thermal_vectors_no_norm_limit.

O alcance negativo é preciso: refere-se à sequência específica de vetores preparados. Não foi provada aqui a inexistência de outro vetor com dadas marginais, nem disjunção, quase-equivalência, impossibilidade de toda extensão normal ou convergência fraca a zero. Sobreposição com Ω tendendo a zero, isoladamente, não autoriza essas conclusões.

[KNOWN] O tema das afinidades e produtos infinitos tem tratamento clássico em [Promislow, The Kakutani theorem for tensor products of W*-algebras](https://msp.org/pjm/1971/36-2/pjm-v36-n2-p20-s.pdf). O artigo trata estados normais e produtos de álgebras com condições próprias. Seu teorema geral não foi introduzido como axioma Lean. Aqui se verificou a sequência concreta da bancada.

## O corte aparece no coeficiente da fonte

[REAL] A variância modular soma para produtos normalizados:

    V_(p⊗q) = V_p + V_q
    V_N = Σ_(n≤N) V_site(n).

Para perfil constante, V_N=(N+1)V_site. O andar zero contém um sítio; daí o fator N+1. A aditividade da entropia em si já estava em TowerEntropyScaling e foi reutilizada.

O coeficiente de tensor escolhido em 024, gibbsCoupling(towerW(P,N)), é V_N/π. No caso estacionário não tracial,

    coupling_N = (N+1) V_site/π → +∞.

Esse coeficiente não é uma constante de Newton medida nem a aceleração de superfície. Sua normalização foi escolhida para a correspondência do calor. A divergência mostra que não se pode ignorar o corte ao transportar essa escolha para a torre inteira.

## Escala escolhida e duas ordens de limite

[INPUT] Escolha ℓ_N=ℓ/sqrt(N+1), de modo que

    s_N(t) = (ℓ_N t)² = (ℓt)²/(N+1).

[REAL] Para cada N fixo, no limite temporal t→0 pelo lado esquerdo,

    ΔK_N(t)/t² → -ℓ² V_site
    ΔS_N(t)/t² → -ℓ² V_site
    D_N(t)/t² → 0.

O limite de entropia também está escrito diretamente em termos dos pesos lidos do estado vetorial efetivo, em cutoff_state_entropy_limit.

[REAL] Em outra ordem de limite, com t fixo e N→∞, s_N(t)→0. Para qualquer observável a de qualquer andar L fixo,

    ω_(s_N(t))^(N)(π_P(a)) → ω_P(π_P(a)).

O teorema cutoff_local_state_returns_reference vale até para perfil não estacionário; a escala linear da variância e sua simplificação por sítio exigem o perfil constante.

| Situação | Marginais locais | Vetores da preparação em H(P) | Resposta |
|---|---|---|---|
| Perfil constante não tracial, s≠0 fixo | Compatíveis com P_s | Não são Cauchy | Variância total proporcional a N+1 |
| Escala s_N=(ℓt)²/(N+1) | Retornam à referência para t fixo | Convergência em norma não demonstrada nesta etapa | Coeficiente temporal por sítio, para cada N |
| Perfil tracial q=1/2 | Permanecem iguais à referência | Todos os vetores são Ω | Variância zero |

Não foi provada troca dos limites N→∞ e t→0, nem uniformidade em N. Não se chama a resposta extensiva de uma nova variação local não trivial que sobreviva no limite: os observáveis locais fixos retornam à referência. N conta sítios; o pacote não o identifica com raio ou área geométrica.

## Consequência para a reconstrução gravitacional

Usa-se o tensor de 024 com coupling_site=V_site/π, um covetor comum w e q_g=gInv(w,w):

    T = coupling_site [w⊗w - (q_g/2)g].

[REAL] A família reescalada satisfaz a correspondência com o calor temporal efetivo para esse tensor. A correspondência de área continua equivalente a

    η Ric(d,d) = 2π T(d,d)

em direções nulas, sob a regularidade geométrica declarada. Os enunciados novos são cutoff_heat_matching e cutoff_area_matching_iff_ricci.

[REAL] O controle plano foi transportado para todo corte N: com covetor temporal constante e perfil estacionário não tracial, o tensor é conservado, a correspondência de calor vale e a de área falha para toda η. A conservação é reutilizada de 024/023, não redescoberta. Os controles tracial q=1/2 e não tracial q=1/3 são termos explícitos e passam no mesmo conjunto de provas.

[OPEN / INPUT] A origem da lei de área, a escolha física da escala e da perturbação, covetor e equação de onda, quatro dimensões, assinatura, solda, unidades, temperatura e coeficiente de Newton permanecem antecedentes ou lacunas. A representação global do perfil produto não é a reconstrução global de um espaço-tempo. A nova escala não produz H3.

## Verificação e custódia

A tabela abaixo é gerada dos fontes e dos logs. Todos os teoremas e a definição construída thermalProfile têm axiomas impressos. As compilações finais têm exit 0, fontes estáveis, zero erros, avisos ou sorryAx. A lista de axiomas contém apenas propext, Classical.choice e Quot.sound. As contagens incluem lemas auxiliares e controles.

O inventário fixa os fontes, oleans, logs, metadados, backups e dependências locais. Lean/mathlib externos são resolvidos pelo wrapper, não constituindo pacote integral portátil. A conferência da bancada não substitui a recompilação e leitura adversarial da gerência.

Somente Chatgpt recebeu escrita. Originais, um.py, kernel canônico, Atlas, memórias, diários, gate e entregas anteriores permaneceram intocados. A incorporação cabe à sessão irmã conforme o protocolo.

| Modulo | Teoremas | Definicoes impressas |
|---|---:|---:|
| [GibbsProductLaw.lean](<C:/IALD/Central de Patentes/Chatgpt/GibbsProductLaw.lean>) | 7 | 0 |
| [GibbsProductVariance.lean](<C:/IALD/Central de Patentes/Chatgpt/GibbsProductVariance.lean>) | 7 | 0 |
| [TowerThermalProfile.lean](<C:/IALD/Central de Patentes/Chatgpt/TowerThermalProfile.lean>) | 9 | 1 |
| [GibbsAffinity.lean](<C:/IALD/Central de Patentes/Chatgpt/GibbsAffinity.lean>) | 13 | 0 |
| [TowerThermalOverlap.lean](<C:/IALD/Central de Patentes/Chatgpt/TowerThermalOverlap.lean>) | 11 | 0 |
| [ThermalCutoffResponse.lean](<C:/IALD/Central de Patentes/Chatgpt/ThermalCutoffResponse.lean>) | 15 | 0 |
| [ThermalLimitControls.lean](<C:/IALD/Central de Patentes/Chatgpt/ThermalLimitControls.lean>) | 10 | 0 |

Medicao: 7 modulos limpos; 72 teoremas; 1 definicao impressa; 7 tentativas rejeitadas preservadas.

Reproducao da custodia (somente leitura, apos a emissao do manifesto):

    & 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation025.py'

Manifesto e entrega sao emitidos pelo auditor com hashes calculados dos bytes, nunca preenchidos de memoria.
