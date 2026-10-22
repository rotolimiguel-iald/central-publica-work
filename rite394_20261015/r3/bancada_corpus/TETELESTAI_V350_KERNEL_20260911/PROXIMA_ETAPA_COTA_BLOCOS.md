# Próxima etapa: da identidade ponderada à cota inferior

[OPEN — roteiro de implementação, não constitui novos alvos Lean]

A etapa DEV27 já compilou o grafo dos pares e a identidade complexa
2〈ξ,Zη〉=z〈η,Zη〉+conj(z)〈Yη,η〉, com Y=eBB*, Z=B*eB.
Sua revisão/integração é registrada separadamente. A prova mantém e∈M,
e*=e e [e,A]=0 como hipóteses. O próximo passo deve quitá-las para a
escolha efetiva de e e provar a estimativa; não basta citar a identidade.

1. Tomar ξ=j(a₀), a₀*=a₀, m=‖a₀.val‖, c=1+m². Para a estimativa
   registrada na consulta RVD, exigir Re z=1. O teorema DEV aceita Re z>0,
   mas isso sozinho não dá a mesma constante c. η é o vetor variacional
   correspondente e permanece fixo pelo S original.
2. Para e≥0, auto-adjunto, comutante com A e pertencente a M,
   Z≥0 e Y=eA(I−A)≥0. Só então os termos relevantes são reais.
   Re z=1 permite extrair a identidade real, aplicar Cauchy–Schwarz e obter
   Re〈η,eA(I−A)η〉≤m² Re〈η,eA²η〉. √e deve comutar com a₀.val;
   não se pode trocar e ou √e com B.
3. Escolher e=(I−cA)⁺, provar e(I−cA)=e² por
   CFC.posPart_sub_negPart e CFC.posPart_mul_negPart. I−cA deve ser
   auto-adjunto; a definição total de posPart também vale zero em entradas
   não auto-adjuntas e não autoriza concluir que essas entradas são ≤0.
4. A estimativa força √A eη=0. A densidade de j(E), B j(a)=a Aη
   e a comutação com E devem então promover a anulação vetorial a eB=0.
   BB*=A(I−A) e a injetividade de A dão e(I−A)=0. Segue eA=e e
   e²=(1−c)e≤0, portanto e=0, I≤cA e c⁻¹I≤A.
   Não dividir por m ou c−1: o caso m=0 também deve passar.
5. Só após a cota positiva, construir A⁻¹ e o multiplicador A⁻¹B,
   provar suas ações e simetria. A inclusão inversa pelo J original
   ainda requer as etapas adicionais da família variacional RVD.

Rota de pertença por comutação: o arquivo Mathlib VonNeumannAlgebra/Basic.lean
consultado define a álgebra concreta por bicomutante e não oferece, ali,
uma instância pronta de fechamento normado/CompleteSpace para ela.
`cfc_mem` em Range.lean exige explicitamente IsClosed da subálgebra.
Não inventar essa instância. Uma rota mais curta para esta aplicação usa
IsSelfAdjoint.commute_cfcₙ (posPart é cfcₙ) para transportar a comutação
com todo a∈E; `scalarPairedCommutant_mem_GNS` conclui e∈M a partir de E'=M.
A versão `Commute.cfc_real` também foi localizada para cfc unital.
Se se escolher converter cfcₙ em cfc, a conversão deve ser provada.

Estatuto: roteiro [OPEN/DERIVED], sem nova compilação, sem promoção de flags
ou de gate. Os nomes acima são APIs lidas; o roteiro não declara as etapas
futuras como teoremas já implementados. Pins das fontes consultadas no JSON
adjacente; consultas anteriores e suas limitações permanecem preservadas.

Reaproveitamento verificado: `boundedPositiveSquareRoot_energy`, em
`kernel/TGLV350/DualFormRepresentation.lean`, já consta no axiom_report
integrado herdado, somente com o trio padrão. Sua orientação é
‖sqrt(R)v‖²=Re〈Rv,v〉. Para usar Re〈v,Rv〉, fazer a conversão explicitamente.
O arquivo `OperatorOrderLimits.lean` está rotulado RETIRED PROTOTYPE,
NOT COMPILED/NOT INTEGRATED; seus lemas não são evidência aproveitável.

Refinamento [DERIVED — ainda não compilado]: a passagem da identidade real
à estimativa admite usar diretamente a norma de uma diferença. Com L=√e B,
Z=L*L, a identidade real dá 2 Re〈Lξ,Lη〉=‖Lη‖²+Re〈Yη,η〉.
De ‖Lξ−Lη‖²≥0 segue Re〈Yη,η〉≤‖Lξ‖².
Isso evita introduzir uma estimativa intermediária de Cauchy–Schwarz.
`norm_sub_sq` foi localizado em Mathlib/Analysis/InnerProductSpace/Basic.lean.
Ainda é preciso provar Z=L*L, transportar os pareamentos, justificar a
realidade das formas para Re z=1 e mostrar Lξ=a₀.val √e Aη. A identidade
abstrata de norma não quita essas identificações concretas.
