# Ponte gravitacional da fonte geral — 09/09/2026

[REAL] GeneralSourceEinsteinBridge.lean está congelado e passou em BUILD_20260909_133048_581015: **3 teoremas**, 3 auditorias, dois processos com saída zero, zero warnings/erros, axiomas restritos a propext, Classical.choice e Quot.sound. SHA-256 lido: cbb7b512d4b181b9255bb82d282e0679eb04f430e416b89fd79377362f199f6d. A folha foi compilada sobre oito dependências locais PASS copiadas, verificadas por recibos e hashes; as dependências locais não foram recompiladas nesta rodada.

[REAL] general_source_heat_matching (linha 15) usa a curva calibrada da fonte T e o calor geométrico construído do MESMO T. O limite de calor é −rate·T(d,d)/2; o incremento modular tem coeficiente −πT(d,d). A conversão rate/(2π) cancela os dois coeficientes. Este enunciado vale inclusive para rate=0, caso degenerado que não fornece conteúdo térmico não nulo. Não se infere uma medição independente de calor a partir dessa construção.

[REAL] general_source_area_matching_iff_ricci (linha 45) identifica exatamente a condição restante, para a tela e direção fornecidas:

erro de área o(t²) ⇔ η·Ric(d,d)=2π·T(d,d).

A fonte é simétrica e a métrica lorentziana no ponto; o enunciado recebe regularidade e a condição de torção da conexão exigidas pela expansão de área. A lei de área não é produzida pela representação de T; a equivalência exibe seu conteúdo dinâmico.

[REAL] general_source_einstein_from_area (linha 67) fornece, em U aberto e preconexo,

G[g] + Λg = (2π/η)T,

com Λ constante. As hipóteses explícitas são: g e T suaves, g lorentziana, T simétrica, η≠0, família de telas de equilíbrio MetricScreenFamily, conservação TOTAL de T pela conexão de Levi-Civita construída e matching de área para cada ponto e cada direção nula não zero. O vetor nulo zero é tratado algebricamente na ponte importada.

[DERIVED] A representação usa os oito covetores calibrados da entrega anterior. Sua conservação é transportada da igualdade com T num aberto; não se introduzem equações de onda ou fechamento dos covetores polarizados como premissas ocultas. Assim a capacidade algébrica de representar fontes não ficou restrita aos casos em que cada setor é conservado separadamente.

[INPUT / OPEN] Assinatura lorentziana, regularidade, conservação total, telas e lei de área têm os papéis descritos. A realização de uma fonte fornecida não demonstra sua preparação física, não fornece uma observação independente e não transforma o ângulo de uma base fixa em identificação da fonte arbitrária. Os sinais dos acoplamentos também não dão positividade de energia por setor.

[REAL — revisão independente] O módulo recebeu revisão somente leitura favorável de /root/review_remaining_hypotheses e /root/selected_geometry_design, além da leitura integral do root. As revisões verificaram identidade do T usado, fatores de conversão, manutenção da hipótese de área e transporte da conservação total. Não realizaram recompilação independente deste módulo.

[REAL] Nenhum original foi modificado, nenhum um.py foi executado/importado e nenhum gate foi alterado. A integração requer somente transpor imports locais para TGLExt.GeneralSourceUnitaryRealization e TGLExt.JointCoherentGravitation numa nova cópia, preservando namespace e acrescentando os três teoremas ao Audit.
