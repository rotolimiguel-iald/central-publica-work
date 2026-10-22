# Derivação046 — média aperiódica de fases e pinching local

06/09/2026. [DERIVED — registrada antes do código; validação Lean pendente]

Para T>0 e r real, defina phaseAverage(T,r)=T⁻¹∫₀ᵀ exp(i r t)dt, usando literalmente modularPhase da torre. Se r=0, a média é1. Se r≠0, a integral é (modularPhase(T,r)−1)/(i r). Como a fase tem norma1, a norma da média é limitada por T⁻¹·(2/|r|). Tomando T=n+1, a cota tende a0. Assim phaseAverage(n+1,r) tende a1 exatamente nas frequências nulas e a0 nas demais, sem período comum.

Em cada corte N, flowLevel(P,t,N,A) tem entrada (i,j) igual à fase de frequência log(towerW_i)−log(towerW_j) multiplicada por A_ij. O funcional matrixEntryCLM já existente comuta com a integral. Portanto a matriz média normalizada tem entrada phaseAverage(T,log w_i−log w_j)A_ij. A positividade dos pesos torna frequência nula equivalente a w_i=w_j. O limite finito é specExpect(towerW P N)A, incluindo blocos degenerados completos, e não apenas as entradas diagonais.

O limite matricial deve ser provado em sua topologia Pi finita por convergência de cada entrada. A aplicação contínua levelEmbeddingCLM, junto com sua comutação com a integral, transporta esse limite aos vetores locais do GNS, se incluída no módulo.

Hipóteses: P é qualquer SiteProfile; N é qualquer corte finito; A é qualquer matriz do corte; r é qualquer real. A normalização exata no caso r=0 requer T≠0; a estimativa usa T>0; a sequência n+1 sempre satisfaz ambas. Nenhuma LocalPhasePeriod, TakesakiInput ou ExpectationInput será hipótese.

[OPEN] Este módulo não constrói ainda a esperança global. Faltam a extensão da convergência por densidade/cota uniforme, o levantamento limitado a todos os vetores usando a ação direita e o fechamento dos campos do contrato. Normalidade e positividade completa da restrição à álgebra continuam propriedades adicionais a provar.

Escopo de escrita: somente este DERIVACAO046_APERIODICA.md e AperiodicPhaseAverage.lean, novos na bancada Chatgpt. Canônicos, módulos045, selos e memórias permanecem somente leitura. Revisões próprias terão backup imediato de bytes e temporário verificado. Nenhuma compilação pelo agente.
