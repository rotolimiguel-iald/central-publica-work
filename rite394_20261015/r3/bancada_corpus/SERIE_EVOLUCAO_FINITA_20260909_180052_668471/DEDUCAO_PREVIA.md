# Série dos comutadores e evolução finita real

[DERIVED — fonte proposta; ainda sem compilação]

Multiplicação à esquerda L_H e à direita R_K são mapas contínuos no espaço dos operadores reais do TowerHilbert. Eles comutam por associatividade, sem pressupor que H,K comutem. Avaliar as séries de exp(L_H) e exp(R_H) mostra exp(L_H)(A)=exp(H)A e exp(R_H)(A)=Aexp(H).

Da identidade z·ad(H)=L_(zH)+R_(-zH), a exponencial da soma comutante fornece exp(z·ad(H))(A)=exp(zH)Aexp(-zH). A série existente da exponencial, transportada pela avaliação contínua, produz a série dos comutadores. Uma indução identifica as potências do superoperador com iteratedCutoffBracket do H_N efetivo da folha congelada BondLocalityEstimates.

Finalmente z=it entrega HasSum para evolution(H_N,t) A evolution(H_N,-t), exatamente com evolution de UnitaryDuhamel. A prova finita não restringe t e não afirma convergência uniforme no volume. A passagem ao limite extensivo exige o majorante local já preparado e uma etapa analítica adicional.

Nenhum original é alterado e nenhum um.py é executado ou importado.
