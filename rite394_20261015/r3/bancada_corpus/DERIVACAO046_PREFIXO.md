# Derivação prévia 046 — limite nos cortes finitos

[DERIVED — alvo antes da compilação] Para qualquer T>0 e operador A, a ação em Ω do corte N de periodAverage(T,A) coincide com a imagem GNS da média finita flowAverage(T,N,expectationMatrix(N,A)). A projeção levelProject comuta com o fluxo modular; Ω é fixo; a integral atravessa aplicações lineares contínuas.

Quando T=n+1 tende ao infinito, o lema escalar/matricial de AperiodicPhaseAverage identifica o limite com specExpect, preservando blocos de pesos iguais. Nenhum período comum é assumido.

Se B é qualquer operador limitado e as médias de A em Ω convergem para BΩ, a continuidade de levelProject identifica a ação em Ω de towerExpectation(N,B) com a imagem desse pinching. Os dois operadores locais pertencem ao fator, e a separância paga sua igualdade. O resultado é uma identidade prefixal condicional somente ao limite em Ω. A existência desse limite e de B será fornecida separadamente por AperiodicVectorAverage e BoundedOmegaLimit.

[OPEN] Este módulo isolado não constrói a esperança. Não confundir identidade de limites com igualdade exata de médias em T finito. Nenhuma alteração no acervo canônico.
