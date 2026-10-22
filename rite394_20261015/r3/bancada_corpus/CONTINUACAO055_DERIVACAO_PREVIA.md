# Continuação055 — corrente conservada e entropia regional na torre
[DERIVED — derivação anterior à implementação055; não é anúncio de compilação]

A054 identifica o custo global do polarizador nos vetores locais com uma resposta quadrática da energia modular. Falta construir uma energia microscópica com corrente conservada e restrições regionais efetivas antes da identificação com o calor da tela. A055 ataca este elo da mesma torre, preservando o objetivo completo de reconstrução gravitacional e suas lacunas. A revisão do caminho crítico também excluiu obter inclusão modular própria mantendo o par produto atual: essa outra linha precisará de novos dados e não será disfarçada como consequência055.

## Dados independentes e convenções

Fixar qualquer SiteProfile P, p=P.w 0 e q=P.w 1, ambos estritamente entre zero e um. O prefixo N=1 contém os dois primeiros sítios. Usar energias locais com níveis 0 e 1:

    e=diag(0,1), E0=e⊗I, E1=I⊗e,
    G=(X⊗X+Y⊗Y)/2, U(t)=exp(i t G).

[INPUT] A escolha de interação, energia de nível unitário e parâmetro t define o protocolo microscópico. Não deriva escala dimensional, temperatura física, Newton G ou tempo de boost. Para uma interpretação de temperatura positiva, restringir p,q>1/2; os resultados algébricos usarão todo o domínio fiel.

Em 00,01,10,11, G só troca 01 e 10. Logo G*=G, G³=G e [G,E0+E1]=0. A exponencial tem fórmula literal

    U(t)=I+(cos t-1)G²+i sin t G.

A inclusão dessas matrizes é o towerPi existente no MESMO TowerHilbert P. A055 deve demonstrar a identidade entre a fórmula explícita e boundedPhase, não tratar duas curvas com o mesmo nome como uma só.

A convenção de estado é ω_t(B)=ω(U(t)* B U(t)); a densidade finita correspondente é U(t)ρU(t)*. Portanto a corrente do sítio j é

    Jj=i(Ej G-G Ej), dω_t(Ej)/dt=ω_t(Jj),
    J0+J1=0, ω_t(E0+E1)=ω(E0+E1).

O gerador G conserva a energia nua total. Nenhuma igualdade com fluxo de stress gravitacional é presumida.

## Marginais reais e transferência

Da multiplicação matricial e da referência-produto diag(p,1-p)⊗diag(q,1-q):

    p_t=p+(q-p)sin²t, q_t=q+(p-q)sin²t;
    Q0=ω_t(E0)-ω(E0)=(p-q)sin²t, Q1=-Q0.

p_t e q_t são combinações convexas dos pesos iniciais, logo permanecem fiéis em todo t. A derivada dos pesos em zero é nula. A leitura marginal deve ser provada para a restrição efetiva da órbita, preferencialmente para toda matriz de um sítio; apenas definir p_t não prova que seja a marginal.

## Primeira lei regional e mesmo custo054

Definir ν(p)=log p-log(1-p), S(p)=-p log p-(1-p)log(1-p), e relativo Bernoulli D(p_t||p). A identidade exata é

    S(p_t)-S(p)=ν(p)Q0-D(p_t||p).

A regularidade e a tangente inicial zero dão D(p_t||p)/t²→0. Logo

    (S(p_t)-S(p))/t²→ν(p)(p-q).

O análogo vale para q, com sinal de Q invertido. A soma dos incrementos modulares é

    ν(p)Q0+ν(q)Q1=C(p,q)sin²t,
    C(p,q)=(p-q)(ν(p)-ν(q))≥0.

ν é estritamente crescente em (0,1), de modo que C=0 exatamente quando p=q. A energia nua total é conservada, embora as energias modulares somadas possam aumentar por serem ponderadas por ν distintos.

O K local054 se decompõe em

    K1=-(log p+log q)I+ν(p)E0+ν(q)E1.

Consequentemente a resposta literal de finiteModularEnergy054 ao G é C sin²t. A fórmula do mesmo statePolarizer D054 deve dar

    towerModularCost P (towerPi P G Ω)=ofReal(C(p,q)).

O relativo clássico de cada marginal é o(t²); a entropia total da órbita unitária finita é constante. Não confundir esses fatos: a correlação gerada entre os sítios explica a variação da soma das entropias regionais. Uma eventual afirmação formal sobre entropia quântica mútua depende de uma implementação específica; não será contada só por esta derivação.

## Controles independentes

- p=q: a transferência e C são zero, mesmo com interação G não nula.
- p=2/3, q=3/4: Q0=-(1/12)sin²t, Q1=(1/12)sin²t e C=(log3-log2)/12>0. Ambos correspondem a ν positivos.
- [DERIVED] Se p≠q e sin t≠0, o estado muda: a órbita não é um TowerHorizon ω-invariante.
- Nenhuma Ricci, massa, eta ou área é escolhida para acertar C.

## Módulos e critérios antes do código

Namespace único ChatgptAudit.Exchange055, ordem:
1. ExchangeEntropyResponse: curva Bernoulli, fidelidade, primeira lei regional, limites e sinais.
2. ExchangeMicroscopicDynamics: matrizes, conservação, exponencial, restrições reais e corrente na torre.
3. ExchangeModularCost: decomposição do K real054, custo do mesmo polarizador, transferência modular e controles.

Nomes auxiliares podem ser acrescentados dentro desse escopo. Mudanças materiais de escopo recebem adendo datado antes do código. Registros auxiliares previstos: DERIVACAO055_ENTROPIA.md, DERIVACAO055_DINAMICA.md, DERIVACAO055_CUSTO.md e DERIVACAO055_INFRA.md.

As entregas finais exigem fontes compiladas juntas em ambiente limpo, Imports055All, #print axioms de todas as declarações novas, censo e ausência de avisos/sorry/native_decide/axiomas extra, relatório critério por critério, revisão científica independente, revisão cruzada da infraestrutura, manifesto e auditor. O histórico054 deve ser fixado por seu próprio manifesto, sem promover fontes avulsas a evidência histórica. O importador conjunto inclui os três módulos. Não anunciar seal antes de todas as etapas concluídas.

## Fronteiras mantidas

[OPEN] A energia e a corrente aqui construídas ainda não são a contração de T_ab com um boost sobre uma tela. Faltam localização física dos sítios, identificação de tempo/energia/temperatura e orientação com os dados geométricos. Os dois limites hheat e harea da reconstrução microscópica continuam sendo obrigações; harea não decorre de C≥0. A055 não seleciona área, dimensão, assinatura, estado físico universal ou dinâmica quântica gravitacional completa.

H3=OPEN; physical_reconstruction=OPEN; broad_quantum_gravity_goal=OPEN; canonical_gate_changed=false. Não há confirmação física por este lote.

Escritas somente em Chatgpt. Originais, canônicos, memórias e selos≤054 permanecem somente leitura. Fontes novas ainda não seladas: antes de alterar, backup imediato dos bytes na mesma pasta; gravação por temporário verificado e substituição. Não rodar um.py original. Não consultar observações ou E:.

## Âncoras lidas na emissão
| Artefato | Bytes | SHA256 |
|---|---:|---|
| CONTINUACAO054_MANIFESTO.json | 1604686 | f707b670f96939cc3c9a95f21f2d0dc56783f66f5677dc2e959c315eade2f6a6 |
| CONTINUACAO054_CLEAN_BUILD.json | 1511972 | c2e2e6069652164b07c079cb58afa9cd2a372cea8d5057bb0589da5eb03a5835 |
| ModularCostDerivative.lean | 16664 | e2bf3e4080b8bfcd9e541731de819d5f47ad249d45371120138bb5c271913d50 |
| TowerModularCost.lean | 16091 | ab4216f6fb6cffa80d8ce452d745203c043a42aa4ecc2a63e28597a57759e451 |
| SitePauliObservables.lean | 13615 | 6b387f33c09a4700066505e970a68234636cefbae38824f68fe0ddc48046724b |
| UnitaryMarginalDynamics.lean | 4467 | 1b6844219157a386a7c6731497f83f48c45ea4d61e01029524fbfc440613f623 |
| MicroscopicClausiusBridge.lean | 5469 | 90075186edbfbc8aadd379c46e4e822e7051dfa50f5cb08e4aa5b3c063f83451 |

Emissão UTC: 2026-09-07T07:19:44.118617+00:00
