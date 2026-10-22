# Einstein com contribuição informacional explícita
[REAL — alcance Lean] FisherCorrectedEinstein acrescenta 11 teoremas e 2 definições. A compilação conjunta com suas duas bases auditou 32 teoremas e 7 definições, todos no trio padrão ou sem axiomas. Quatro comandos encerrados com código zero, sem avisos. Uma tentativa anterior por tempo excedido e sua fonte foram preservadas; o reparo apenas substituiu a prova de suavidade de uma soma por uma prova explícita, sem alterar os enunciados.

O balanço microscópico canônico é:
η Ric(v,v) = 2π T(v,v) + F(v,v).

Definimos I = F − ½ tr_g(F) g e T_eff = T + I/(2π). Como g(v,v)=0, I(v,v)=F(v,v). Portanto, sob conservação de T_eff, regularidade e assinatura declaradas:
G + Λg = (2π/η) T_eff.
O sinal é positivo e o fator da contribuição informacional é 1/(2π). Não se está inferindo Clausius de equilíbrio com Fisher não nulo: usa-se seu balanço corrigido.

[INPUT] A conservação assumida é a de T_eff. Não decorre automaticamente da positividade de Fisher nem da conservação isolada de T. A completação por −½ tr_g(F)g é uma escolha explícita fora do cone nulo: os dados nulos não fixam esse coeficiente, pois não veem múltiplos de g. O teorema é condicionado à conservação dessa escolha.

A variante microscópica recebe um mesmo campo de probabilidades-base, curvas por ponto/direção, igualdade entre Fisher direcional e F(v,v), uma família de telas e os matchings de área/calor. Desses dados deriva o balanço nulo e aplica a reconstrução. Não assume que as curvas sejam P(x+t v). O módulo separado FisherInformationTensor oferece essa amostragem como construção matemática; AffineSamplingObstruction mostra por que sua imposição universal de área é restritiva.

[OPEN] A lei que fornece g, T, a resposta e os matchings de uma mesma origem selecionada continua a ser explicitada. Fora da contração nula F ainda é um campo simétrico suave fornecido; a prova geral não o declara automaticamente um Fisher positivo de uma família única. A construção física canônica deve definir esse vínculo, sua conservação e sua transformação entre cartas.

Revisão semântica: raiz e selected_geometry_design, favoráveis aos enunciados e coeficientes com as hipóteses acima. Nenhum um.py executado/importado; nenhum original alterado; nenhum gate ou selo promovido.
