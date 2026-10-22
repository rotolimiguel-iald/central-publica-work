# Limite local em tempo pequeno — dedução antes da compilação

[DERIVED — alvo ainda não compilado] Para A suportado em [0,R], os comutadores iterados estabilizam no corte N≥R+k. O majorante uniforme é (2J)^k·(R+k)!/R!·‖A‖. A divisão por k! na evolução real dá q^k·choose(k+R,R)·‖A‖, com q=2J|t|. A série binomial é somável para q<1; o raio temporal é comum aos suportes finitos R.

O candidato é a soma dos coeficientes estabilizados, e a convergência da evolução unitária real dos cortes será DEDUZIDA por convergência dominada de séries (Tannery), usando a identidade efetiva já compilada em FiniteCommutatorEvolution. Não se assume que a dinâmica limite existe.

[INPUT] BondInteractionData exige termos auto-adjuntos em {j,j+1}, norma uniformemente limitada por J≥0. Não exige soma global finita nem comutação entre termos. A matriz local continua sendo a cadeia canônica de qubits do mesmo TowerHilbert P.

[OPEN] Esta folha não estende a construção a todo t, não faz a extensão ao fecho quase local, nem ao fator por normalidade, e não acrescenta fundo modular ou estado KMS. Fora de q<1 o símbolo tsum da definição não é atestado de convergência. As conclusões operacionais recebem explicitamente hA e q<1.
