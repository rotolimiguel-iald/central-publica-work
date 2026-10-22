[REAL / INPUT / OPEN] CONTINUAÇÃO 020 — área quadrática, calor integrado e reconstrução condicional

06/09/2026. Continuação espontânea de 019; a ordem gerencial mais recente encontrada é 007. O auditor da entrega 019 reconferiu seus 588 hashes sem alteração. O turno 019 foi progresso; o objetivo amplo continua ativo e não alcançado.

## O resultado

Partindo da solda suave inversível, a cadeia local agora constrói a congruência de equilíbrio, a tela e uma integral temporal do fluxo estipulado de energia-momento. O teorema einstein_from_constructed_clausius recebe uma condição de Clausius explicitamente nomeada sobre esses objetos e conclui a equação tensorial G+Λg=(2π/η)T em um aberto conexo.

O avanço é na construção dos objetos e na explicitação da hipótese restante. A integral existir não prova Clausius. constructed_clausius_at_iff demonstra que essa condição, no regime considerado, equivale à própria relação Ric(v,v)=(2π/η)T(v,v) para a direção nula. O controle negativo impede apresentar essa hipótese como consequência automática da geometria ou da conservação de T.

## Derivação verificada

Sejam p o ponto inicial, v sua tangente nula não zero, A(t) a área da tela transportada e θ(t) a expansão do campo construído em 019. Escreva r=Ric_p(v,v) e m=T_p(v,v).

A normalização geométrica fornece A(0)=1 e θ(0)=0; a focalização dá θ′(0)=−r. Como A′=θA nos tempos negativos próximos e A é contínua em zero, o limite provado é

    (A(t)−1)/t² → −r/2, quando t→0−.

Para f(t)=−rate·t·T_curve(t)(V,V)·A(t), a diferenciabilidade de T, a suavidade de V e a continuidade da curva e da área dão a continuidade necessária em zero e nos tempos negativos próximos. pastContinuousExtension escolhe a<0, com f contínua em [a,0], e estende o germe usando max(a,min(t,0)). A escolha é não computável, sustentada por prova de existência.

Define-se efetivamente

    Q(t)=∫ de 0 a t de f_ext(s) ds.

O teorema fundamental do cálculo prova a continuidade de Q, Q(0)=0 e Q′(t)=f(t) eventualmente à esquerda. Segue

    Q(t)/t² → −rate·m/2.

Duas extensões contínuas admitidas podem diferir longe do ponto; a diferença de suas integrais dividida por t² tende a zero. Portanto, o coeficiente desta construção não depende dessa escolha.

Para o resíduo

    B(t)=Q(t)−rate·η/(2π)·(A(t)−1),

o limite exato é

    B(t)/t² → rate/2·(ηr/(2π)−m).

Com rate≠0 e η≠0, B(t)/t²→0 se e somente se r=(2π/η)m. O limite é sempre pelo lado t<0; a prova não troca esse filtro por uma aproximação discreta.

## Enunciado tensorial e hipóteses

einstein_from_constructed_clausius trabalha com U⊆Coordinate4 aberto e IsPreconnected U, A,B suaves com AB=BA=I em U, T diferenciável por componentes, simétrico e com divergência covariante zero, e os parâmetros rate≠0 e η≠0. Coordinate4 tem dimensão quatro; a assinatura Lorentziana entra pela métrica frameMetricField A.

Para cada p∈U e v≠0 nulo, localEquilibriumScreen fornece os dados de equilíbrio, e constructedHeat fornece a integral. A hipótese hbalance exige ConstructedClausiusAt para todos esses pontos e direções. horizonPencilFromScreen produz então o tipo GeometricHorizonPencil; a reconstrução de 012, junto à cadeia tensorial, de curvatura e Bianchi anterior, conclui

    existe Λ real constante tal que G_AB(x)+Λg_A(x)=(2π/η)T(x), para todo x∈U.

Não se assume um GeometricHorizonPencil já pronto no enunciado final. A condição termodinâmica permanece no antecedente, com equivalência formal que permite auditá-la sem ambiguidade.

## Controles

A solda identidade tem conexão de Levi-Civita e Ricci zero. A direção usada é v=(1,1,0,0), nula e não zero. Os controles empregam a tela e a integral da construção geral, não primitivas recebidas como entradas.

Com T=0, a condição construída de Clausius vale. Com T=diag(1,0,0,0), rate=1 e η=2π, T é diferenciável, simétrico e covariantemente conservado, e T(v,v)=1. O coeficiente do resíduo é −1/2, de modo que Clausius falha.

conserved_matter_does_not_force_constructed_clausius reúne a simetria, a conservação e a negação da condição no mesmo enunciado. Trata-se de um contraexemplo à suficiência dessas premissas, não de uma refutação de uma teoria física com hipóteses adicionais.

## Estatutos e fronteira

[REAL] Os novos lemas analíticos e a implicação tensorial são verificações formais locais. As contagens, dependências de axiomas e hashes finais constam do manifesto e da entrega, obtidos por script.

[INPUT] A solda, sua inversa suave, dimensão, assinatura, tensor T e suas propriedades, parâmetros não nulos e a condição de Clausius no enunciado tensorial. A expressão usada para fluxo de calor é estipulada matematicamente a partir de T.

[OPEN] A origem modular da solda, a correspondência região–álgebra, a identificação microscópica de entropia com área, o valor/unidade física de η, a temperatura e identificação de Q com calor físico ou energia modular, a identificação de T com o estado microscópico, e a derivação independente de Clausius/H3.

[OPEN] A construção de hipersuperfície nula imersa, a integração espacial da área de horizonte e a colagem global de cartas. A área considerada é a área da tela normalizada ao longo da curva; a nova integral é temporal. O nome GeometricHorizonPencil não acrescenta essas estruturas ausentes.

Nenhuma afirmação de gravidade quântica resolvida ou confirmada, nenhum movimento de gate. O próximo avanço precisa pagar uma dessas identificações ou premissas com conteúdo independente, pois rebatizar a condição de Clausius não a demonstra.

## Reprodução e custódia

O auditor audit_continuation020.py, sem argumentos, é somente leitura. Ele confere os bytes registrados, os logs finais limpos, a estabilidade do fonte durante a compilação, a contagem de teoremas e a cobertura de #print axioms. O manifesto inclui os fontes locais importados e os objetos copiados TGL/TGLExt. Lean 4.31.0 e mathlib externos são resolvidos por verify_stage.ps1; não se declara empacotamento integral das dependências.

As tentativas rejeitadas e os avisos intermediários são preservados com logs próprios. Backups são cópias de bytes, e nenhuma versão entregue anterior é substituída. A auditoria independente da gerência continua pendente; a checagem da bancada não se apresenta como aprovação adversarial.

Todas as escritas desta etapa ficaram em C:\IALD\Central de Patentes\Chatgpt. Nenhum um.py executado, importado ou editado; kernel canônico, Atlas, memórias, selos e gate não foram alterados pela bancada.

## Contagens verificadas antes da entrega

7 módulos com compilação final limpa, 48 teoremas e 6 definições com axiomas impressos separadamente. Foram preservadas 6 tentativas rejeitadas, incluindo uma compilação com aviso.

| Módulo | Teoremas | Definições impressas |
|---|---:|---:|
| PastContinuousExtension | 8 | 1 |
| EquilibriumAreaExpansion | 7 | 0 |
| ConstructedHeatPrimitive | 10 | 2 |
| ScreenClausiusCoefficient | 6 | 0 |
| ConstructedHorizonPencil | 1 | 1 |
| ConstructedEinsteinReconstruction | 2 | 1 |
| ConstructedClausiusControls | 14 | 1 |

Os números foram lidos pelo auditor dos fontes e dos logs. O inventário final de hashes é emitido somente após este adendo, para incluir seu backup imediato.
