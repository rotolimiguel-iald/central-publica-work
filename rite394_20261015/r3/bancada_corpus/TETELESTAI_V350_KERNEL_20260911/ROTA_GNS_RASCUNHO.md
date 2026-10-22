# Inscrição GNS e ação ambiente — desenvolvimento

[REAL — Lean local, ainda sem revisão independente nem integração]
Três módulos e 14 alvos, com hashes e logs em gns_draft_status.json.
A custódia integrada continua modular_domain_custody.json. Esta nota não
amplia o escopo do pacote integrado ou de seus pareceres.

ScalarGNSOrbit mostra que a órbita s↦θ_s(A)η pertence a L² para A no ideal
esquerdo I de quadrados uniformemente limitados da forma dual. O fator
Haar c=(2π)⁻¹ é estritamente positivo; a prova remove esse fator da integral
sem converter infinito em zero. O vetor é
Λ_ν(A)=sqrt(c)·[s↦θ_s(A)η] no Hilbert ambiente L²(ℝ,L²(ℝ,H)).
Sua norma satisfaz exatamente ofReal(||Λ_ν(A)||²)=q_(A*A)(η).

ScalarGNSLinear prova a representação quase em toda parte, aditividade,
homogeneidade complexa e define uma aplicação linear I→L². A fidelidade
já provada de q no vácuo implica Λ_ν(A)=0↔A=0; a aplicação é injetiva.
As coerções são da mesma torre P; não se assume um funcional externo.

ScalarGNSAction define L_B como o campo s↦θ_s(B), um operador limitado no
Hilbert ambiente, com ||L_B||≤||B||. Para B∈N e A∈I, BA∈I e
L_B Λ_ν(A)=Λ_ν(BA). É a compatibilidade efetiva entre multiplicação e leitura
no domínio. Ainda não se empacotou uma representação por *-homomorfismo
sobre o completamento da imagem; a ação ambiente não é por si esse pacote.

[OPEN — próximos passos matemáticos]
Construir o fecho da imagem como Hilbert GNS e restringir a ação, com leis
de *-representação. A aproximação forte junto aos adjuntos A_h→A já provada
em N NÃO demonstra convergência na norma ν nem propriedade de core em norma
de grafo para Tomita. É necessário provar densidade de Λ_ν(I∩I*) no espaço
GNS e fechar o operador Λ_ν(A)↦Λ_ν(A*), antes da identificação modular/KMS.

Uma rota a testar, não um resultado: a cota uniforme de q_(A*A) pode controlar
a mudança de η para Λ_tη na multiplicação à direita por Λ_t, e a fase dual
pode ser controlada por convergência dominada na órbita L². Isso daria
continuidade na norma ν para a aproximação à direita; o lado esquerdo usa
a ação ambiente limitada. Essas estimativas ainda não foram provadas.

Permanecem o gerador afiliado, a perturbação e o traço canônico com escala,
a interface geral de peso operatorial/predual, Three Locks/H1, H2/H3 na
mesma geometria, setor quântico interagente/BRST/QME/anomalias/UV, certificado
completo consumido e runtime integral isolado. Nenhuma flag maior mudou.
Os logs de todas as tentativas permanecem, inclusive erros de elaboração e
limites de heartbeats. Somente logs finais rc0 com fontes/binários conferidos
são aceitos neste status. Original não importado ou executado.
