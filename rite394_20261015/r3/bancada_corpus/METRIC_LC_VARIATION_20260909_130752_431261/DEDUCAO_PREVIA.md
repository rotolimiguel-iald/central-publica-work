# Deducao previa â€” variacao metrica da Levi-Civita
[DERIVED â€” roteiro antes da fonte e compilacao]

A inversa matricial real e identificada com Ring.inverse pela biblioteca. Em uma matriz g invertivel, a derivada de (g+t h)^-1 em t=0 e -g^-1 h g^-1; aplicar hasFDerivAt_ringInverse e a regra da cadeia, com a norma matricial de operador. A funcao real (g+t h)^-1 e a fonte da derivada, nao uma nova operacao homonima.

A definicao canonica e leviCivitaField(g,gi)(x,i)=gi(x)*lowerChristoffelJet(tensorFieldJet(g)(x))(i).
A suavidade dos componentes de g e h permite derivar tensorFieldJet(g+t h)=tensorFieldJet(g)+t tensorFieldJet(h). O operador lowerChristoffelJet e linear no jet.
Portanto, pela regra de produto, a conexao REAL associada a g+t h e a sua inversa tem derivada
delta Gamma_i = -g^-1 h g^-1 lowerChristoffelJet(dg)_i + g^-1 lowerChristoffelJet(dh)_i.
Equivalentemente, delta Gamma_i = -g^-1 h Gamma_i + g^-1 lowerChristoffelJet(dh)_i.

[ESCOPO] Nao postular a derivada da inversa nem o jet de perturbacao. A invertibilidade sera a hipotese geometrica explicita no ponto; simetria e invertibilidade local devem ser fornecidas para interpretar como metrica nao degenerada. Ainda nao se afirma troca da derivada temporal com derivadas espaciais da conexao, naturalidade por difeomorfismo, Ward metrica geral ou ausencia de anomalias quanticas.
Originais somente leitura. Nova pasta propria. Fonte anterior congelada.
