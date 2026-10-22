# Deducao previa â€” variacao da curvatura canonica
[DERIVED â€” roteiro antes da compilacao; nenhuma prova computacional reivindicada aqui]

A fonte CoordinateCurvature define R_ij = partial_i Gamma_j - partial_j Gamma_i + Gamma_i Gamma_j - Gamma_j Gamma_i.
Para Gamma(t)=Gamma+t C, a linearidade das derivadas espaciais, com regularidade efetivamente fornecida, da exatamente:
R(Gamma+t C)=R(Gamma)+t L_Gamma(C)+t^2 [C_i,C_j],
L_Gamma(C)_ij=partial_i C_j-partial_j C_i+Gamma_i C_j+C_i Gamma_j-Gamma_j C_i-C_j Gamma_i.
Logo a derivada REAL em t=0 e L_Gamma(C), e a contracao que DEFINE coordinateRicci fornece a variacao de Ricci. O termo quadratico nao e descartado.

A direcao de gauge de referencial sera o operador mixedCovariantDerivative ja definido no kernel:
C_i=partial_i B+Gamma_i B-B Gamma_i.
Ao derivar os produtos, as derivadas segundas de B se cancelam por Schwarz, derivado de suavidade local. Os termos restantes sao R_ij B-B R_ij.
A identidade nao afirma que R e invariavel em um fundo curvo generico: sua variacao e um comutador. O traco desse comutador e zero; o objeto matricial em geral nao e zero.

[OPEN â€” elo seguinte] Gauge de referencial de conexao nao e por si a Ward metrica sob difeomorfismo. Nao se identificara esta direcao com a variacao da conexao de Levi-Civita de uma perturbacao metrica sem uma demonstracao adicional. A naturalidade da metrica/Ricci sob difeomorfismos e a identidade delta Ricci=L_xi Ricci sao metas distintas.
[ESCOPO] Conexoes matriciais reais gerais suaves numa carta de quatro coordenadas, inclusive fundos curvos. Sem quantizacao, sem ausencia de anomalias quanticas, sem conclusao de completude UV. Originais somente leitura.
