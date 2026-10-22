# Derivação prévia — preparação unitária conjunta finita

[INPUT] Dados finitos j, pesos constantes λ_j>0 com soma 1, parâmetros canônicos de eixo a_j²+b_j²=1 e base u_j²+v_j²=1, u_j,v_j>0. Cada covetor w_j no ponto x fixa a frequência f_j=<w_j(x),d> para a direção d. O tempo prepara a curva canônica no ponto; não é amostragem do campo espacial em x+t d.

A curva conjunta tem rótulo (j,b) e peso Q_(j,b)(t)=λ_j q_(j,b)(t), onde q_j é unitaryStateCurve. Construiremos uma DiagonalStateCurve única real, com normalização global, derivada e positividade local; a tangente em 0 é zero em cada bloco, logo também na curva conjunta. A resposta quadrática, entretanto, pode ser não nula.

[DERIVED — a verificar] A mistura com rótulos preservados tem H(Q)=H(λ)+Σλ_j H(q_j). O termo H(λ) é constante e cancela nos incrementos. O incremento modular conjunto é Σλ_j ΔK_j porque cada componente mantém massa 1. Portanto os coeficientes quadráticos entrópico e modular são ambos Σλ_j unitaryResponse_j; a entropia relativa tem coeficiente quadrático zero, pela tangente zero da curva conjunta.

A matriz por blocos reúne os pairFlow canônicos. Se incluída, sua relação com os índices dos pesos será explícita: Matrix.blockDiagonal usa (b,j), enquanto os pesos usam (j,b); trata-se da troca declarada dos dois rótulos, não de identificação por nome.

[OPEN] Esta etapa constrói a preparação conjunta; não fornece ainda o matching de área, conservação de sua fonte geral, solução global gravitacional, interações quânticas ou UV. Constância de λ é hipótese física/matemática explícita. O número de blocos é finito e não se reivindica limite infinito.
