# Mapas GNS dos cortes — desenvolvimento posterior

[REAL — compilado na cópia; ainda sem revisão independente ou integração]
Dois módulos, nove alvos: `ScalarGNSCutMaps` e `ScalarGNSCutNorm`.
As saídas `#print axioms` usam apenas `propext`, `Classical.choice`, `Quot.sound`.
Os pins são extraídos dos arquivos e logs pelo registro de desenvolvimento.

Para o mesmo espaço H_I e sua representação π_I, construiu-se

T_R : H_I → L²(ℝ,K),   T_R v = 1_{(-R,R]} v.

T_R é complexo-linear e contínuo, com ‖T_R v‖≤‖v‖. O contradomínio
é o L² ambiente já existente, não se afirma que o corte preserve H_I.
O entrelaçamento tem exatamente a tipagem

T_R π_I(B) v = ρ(B) T_R v,

onde ρ é a mesma representação ambiente pela órbita dual. O lema
de comutação com campos de operadores vale para todo conjunto mensurável,
sem pressupor invariância de um subespaço ou normalidade nova.

[REAL — identidade compilada] Para A no ideal I e R≥0:

‖T_R Λ(A)‖² = Re ψ_R(A* A),
ψ_R(B) = c⟨η,C_R(B)η⟩, c = (2π)⁻¹.

O fator é o mesmo de ν e de Λ; nenhum ajuste ou nova normalização foi
inserido. A igualdade usa o integral sobre (-R,R] e, para R≥0,
sua identificação com o integral orientado de -R até R. Para R<0
a igualdade não foi afirmada. A expressão do funcional como integral
orientado vale para todo R; pode ter sinal oposto nesse caso.

Também foi provado que T_n v=0 para todo n natural implica v=0.
Usa-se uma interseção enumerável de conjuntos de medida total e a
exaustão da reta pelos intervalos; não uma interseção sobre todos os
reais. Isso é injetividade conjunta, não fidelidade de cada funcional.

[OPEN] Estes mapas realizam a seminorma dos funcionais de corte no
ambiente concreto. Não foi construído aqui um novo espaço GNS cíclico
de cada ψ_R nem vetor separante para ele. Não se conclui que a
involução de cada corte seja fechável, e muito menos que
(0,y)∈fecho(G_Tomita) force T_n y=0. Essa é a obrigação que resta.
Injetividade do gráfico inicial, injetividade conjunta dos cortes e
normalidade da representação não suprem essa estimativa.

O parecer `REVIEW_BOUNDED_SCALAR_CUTS.md`, solicitado para os três
módulos de funcionais anteriores, não cobre estes dois módulos.
Todos os campos maiores, traço, KMS, H1–H3 e o gate continuam com
seus estatutos anteriores. O monólito não foi executado/importado.
