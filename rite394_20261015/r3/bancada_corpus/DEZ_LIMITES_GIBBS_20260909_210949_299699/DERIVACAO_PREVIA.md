# Derivação prévia — somente dez limites Gibbs

[DERIVED — anterior à compilação] A folha SignedGibbsCoverage prova um coeficiente conhecido para cada direção, mas seu teorema de observação pede limites em todas as direções. O decoder sampleResponse utiliza apenas probeDirections i para i:Fin 10.

A nova interface recebe diretamente s:ResponseSamples=Fin 10→R e dez limites nessas direções. A unicidade do limite fornece s_i=calibratedPointResponse(g,gi,T)(probeDirections i) para cada i. Logo s=sampleResponse(calibratedPointResponse g gi T); o teorema de reconstrução existente dá decodeSource g gi s=T. A mesma prova funciona para o protocolo modular, em um segundo teorema.

[INPUT] k>0, métrica simétrica g e inversa gi com gi*g=I, fonte simétrica T utilizada para calibrar os oito probes. A folha reduz a quantidade de limites exigidos, mas não remove T da construção da preparação nem infere dinâmica física.

[OPEN] Dez limites exatos não são dez amostras temporais finitas e ruidosas. A precisão experimental é uma questão adicional. A construção de uma distribuição conjunta e sua interpretação física não são acrescentadas aqui.

Todas as fontes anteriores PASS são preservadas; nova folha, derivação e parecer nascem somente em Chatgpt.
