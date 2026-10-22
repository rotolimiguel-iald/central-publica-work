# Derivação prévia050 — reconstrução por raízes limitadas do resolvente
[DERIVED — proposta em formalização; ainda não compilada]

Para o Δ_c que será identificado com S_c†S_c=T_(2c), definir C_c=A_c². Mostrar que C leva qualquer f a D(Δ), que Δ C f=B² f e que (I+Δ)C f=f. Na direção inversa, C(x+Δx)=x para todo x∈D(Δ). Essas duas identidades identificam C=(I+Δ)^(-1) e dão unicidade do resolvente entre os operadores que satisfazem as mesmas identidades de domínio.

A positividade dos pesos ainda precisa ser promovida a 0≤A e 0≤B na ordem da álgebra de operadores limitados. A integral L² do pareamento de A f com f é ∫a|f|²≥0; A auto-adjunto já foi provado. O mesmo vale para B.

Então CFC.sqrt_unique fornece sqrt(C)=A e sqrt(I-C)=B a partir de A²=C, B²=I-C e A,B≥0. O grafo de T_c fica literalmente {(sqrt(C)h,sqrt(I-C)h):h∈H}. Essa caracterização reconstrói T a partir do resolvente de Δ e de raízes CFC genuínas, sem presumir uma operação de raiz já existente em LinearPMap.

Limite preciso: ainda é preciso provar que uma raiz positiva auto-adjunta arbitrária Q, com Q²=Δ, admite essa mesma parametrização para obter a unicidade abstrata entre TODAS as raízes não limitadas. A reconstrução concreta do grafo via resolvente não será anunciada como esse teorema geral. Referência de revisão: Sebestyén–Tarcsay, On the square root of a positive selfadjoint operator, teorema2.3; argumento de domínio/cálculo funcional a conferir na fonte antes de citar como KNOWN.
