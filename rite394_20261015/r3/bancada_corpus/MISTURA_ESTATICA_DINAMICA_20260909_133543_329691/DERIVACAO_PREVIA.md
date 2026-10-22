# Derivação prévia — mistura estática e dinâmica

[INPUT] Recebemos probabilidades q em um índice finito estático, normalizadas e positivas, e uma DiagonalStateCurve X com base p positiva em outro índice finito. Os rótulos ficam separados pelo tipo soma.

Definimos M(t,inl i)=q(i)/2 e M(t,inr j)=X(√2 t,j)/2. Normalização vale para todo t; positividade de M vale perto de zero pelas hipóteses sobre q,p e pela continuidade de X. A derivada no bloco estático é zero; no bloco dinâmico é √2 X'(√2t)/2.

As identidades de entropia de misturas rotuladas dão H(M(t))−H(M(0))=[H(X(√2t))−H(p)]/2. O incremento modular obedece à mesma identidade porque o termo log(1/2) cancela pela normalização. Como (√2t)²=2t², ambos os coeficientes quadráticos são preservados exatamente.

[DERIVED — a verificar em Lean] A reparametrização positiva √2t preserva o filtro t→0 pela esquerda. Os resultados serão válidos para qualquer curva do tipo canônico e qualquer limite quadrático que ela de fato possua. Especializaremos a curva conjunta unitária já compilada, que possui esses limites.

[OPEN] Este é um transporte representacional explícito. A base estática pode carregar um registro geométrico, e a preparação/resposta dinâmica pode carregar matéria; este módulo não construirá ainda essas leituras específicas. A distribuição inicial, por si, não identifica T. Não há amostragem P(x+td), e rótulos não serão marginalizados. Positividade diagonal não afirma fé/separância na álgebra matricial inteira.
