# Derivação prévia047 — normalidade por supremos dirigidos

[DERIVED — roteiro, antes da fonte] A meta é a formulação de normalidade pela preservação de supremos de TODAS as redes positivas crescentes limitadas superiormente, indexadas por qualquer pré-ordem dirigida não vazia. Não se substitui rede por sequência; o limite forte será conclusão.

1. Generalizar a passagem ao bicomutante de046 a um filtro arbitrário não trivial: cada comutação fixa Y*A_i=A_i*Y passa ao limite por continuidade de Y e unicidade do limite. A segunda comutação usa star Y fixo. Não se alega continuidade forte do adjunto de uma família.
2. Provar ordem preservada por E em M: A≤B implica B−A≥0; linearidade e positividade já derivadas dão E(B)−E(A)≥0.
3. Aplicar MonotoneOperatorLimit à rede positiva uniformemente limitada em norma. O teorema constrói B, seu limite forte e IsLUB(range A) B. A etapa1 prova B∈M.
4. ExpectationContinuity preserva o limite forte das redes limitadas, via sua convergência em Ω. A rede E(A_i) é crescente pela etapa2. O lema monotone_strong_limit_isLUB conclui IsLUB(range E(A_i)) E(B).
5. Trocar a limitação de norma pelo majorante de ordem D usando a monotonicidade da norma positiva: 0≤A_i≤D implica ||A_i||≤||D||.
6. Para um supremo B já dado, aplicar a construção e unicidade de IsLUB. Assim a preservação não é hipótese escondida em um contrato.
7. Instanciar com aperiodicExpectationInput P de046: o resultado concreto vale para todo SiteProfile da torre binária existente, sem hipótese de periodicidade.

[OPEN] A geometria física, H3 e a reconstrução gravitacional geral não seguem deste teorema de operadores. Não haverá alegação de confirmação de gravidade quântica. A palavra normalidade refere-se expressamente à preservação dos supremos positivos dirigidos aqui quantificados; não se acrescenta uma equivalência topológica não formalizada.
