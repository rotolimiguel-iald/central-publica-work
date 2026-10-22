[DERIVED / INPUT / OPEN] Continuação 013 — preservação da nulidade e construção pontual da tela. Derivação anterior ao código, 05/09/2026.

A entrega 012 foi reconferida: 491 hashes, seis módulos e 45 teoremas. O turno anterior foi progresso. A ordem gerencial mais recente continua sendo 007; esta rodada é continuação espontânea, com o objetivo amplo intacto.

## Hipóteses a descarregar

O contrato de 012 ainda recebia preserves_null_pairing, embora V fosse nulo e a conexão compatível. Também recebia um referencial transversal. Esta rodada deverá provar a primeira condição e construir o segundo em cada ponto para toda direção nula não nula de uma métrica obtida pela solda lorentziana já especificada.

A construção pontual não será promovida a transporte de uma tela ao longo de uma congruência. A existência e regularidade de uma família transportada, a imersão de superfície e o vínculo quântico continuam obrigações próprias.

## Derivação analítica

1. Denote g(u,w)=uᵀgw. Para B=∇V e uma direção w, a derivada ordinária de V é dV(w)=Bw−L_w V, onde L_w=ΣwⁱΓᵢ. A compatibilidade métrica fornece dg(w)=L_wᵀg+gL_w.

2. Diferenciando g(V,V), os termos com L_w cancelam. Para g simétrica:
d[g(V,V)](w)=2g(V,Bw).
Se g(V,V)=0 numa vizinhança aberta, a derivada é zero. Portanto g(V,∇_wV)=0 para toda direção w, sem hipótese adicional de transporte ou geodesicidade.

3. Se a primeira coluna do referencial F é V, tomar w igual à segunda coluna dá (FᵀgBF)₀₁=0. Isso produz o campo preserves_null_pairing exigido por NullScreenAt. A geodesicidade continua sendo uma condição distinta: B V=0.

## Construção pontual do referencial

4. Na convenção +--- efetivamente usada pelo kernel, uma direção nula não nula v=(t,s) tem t≠0 e ‖s/t‖=1. O vetor espacial unitário u=s/t define um eixo.

5. Construir uma isometria ortogonal R de ℝ³ que leve o primeiro vetor da base canônica a u. Pode-se usar a reflexão no complemento ortogonal de e₀−u: a reflexão leva vetores de mesma norma um ao outro, inclusive quando são iguais. As imagens dos outros dois vetores canônicos dão e₁,e₂ espaciais ortonormais e ortogonais a u.

6. Tomar k=v, n=(-1/(2t),u/(2t)), E₁=(0,e₁), E₂=(0,e₂). Então:
g(k,k)=g(n,n)=0; g(k,n)=−1;
g(k,Eᵢ)=g(n,Eᵢ)=0; g(Eᵢ,Eⱼ)=−δᵢⱼ.
A matriz F de colunas (k,n,E₁,E₂) tem Gram G₀=nullScreenGram(−I). Como G₀²=I, D=G₀Fᵀη é inversa; a identidade de Gram dá DF=I e a dimensão finita dá FD=I.

7. Para g=EᵀηE com inversa D da solda, aplicar a construção ao vetor E v e transportar o referencial de volta por D. As identidades de inversa e de Gram deverão ser verificadas por multiplicação efetiva; não basta repetir a palavra “congruência”.

8. Combinando esse referencial com a prova analítica, produzir um habitante de NullScreenAt no ponto, com S=screenColumns F e Gram transversal −I. Sua densidade inicial de área é 1 na base normalizada escolhida. Essa normalização não fixa uma unidade física de área.

## Controles e estatuto

Deverá haver controle explícito de que a direção zero não pode ser a primeira coluna de uma matriz invertível. As direções nulas não nulas cobertas pelo teorema não serão restringidas a um eixo fiducial. A assinatura e a dimensão quatro permanecem INPUT da métrica soldada.

[KNOWN] As identidades de projeção/tela de uma superfície nula usam um vetor nulo auxiliar; fonte primária consultada: https://arxiv.org/abs/2009.08221. A prova aqui será algébrica/analítica explícita, sem extrair hipóteses físicas da citação.

[OPEN] Não serão declarados fechados: família de telas transportadas, existência geral de horizontes, equilíbrio apenas transversal, entropia-área microscópica, calor, H3, seleção de assinatura/dimensão, escala e globalização.

Todos os teoremas e as construções principais terão #print axioms, com o trio permitido. Falhas e revisões ficam em logs e backups de bytes. Escritas somente em Chatgpt; nenhuma execução/importação de um.py, alteração de kernel canônico, Atlas, memórias, selos ou gate. Sem dados observacionais.
