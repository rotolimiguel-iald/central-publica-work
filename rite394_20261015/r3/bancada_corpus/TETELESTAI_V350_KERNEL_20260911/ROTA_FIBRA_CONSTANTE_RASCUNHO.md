# Rota da ação constante na fibra — rascunho de desenvolvimento

Este arquivo orienta o próximo trabalho. Não é parecer independente nem
substitui a custódia `fixed_locality_custody.json`. Os hashes e estados de
compilação dos protótipos serão lidos de seus logs, sem promover tentativas
falhas a provas integradas.

O resultado custodiado é: todo B∈F comuta com as translações ordinárias e
com todos os recortes mensuráveis em L²(ℝ,H). F=base permanece aberto.

A rota em desenvolvimento usa I=(0,1], e:H→L² como v↦1_I v, e Q=e e*.
`UnitIntervalProjection` constrói a isometria, e*f=∫_I f, Q²=Q e Q*=Q.
`TranslationCorrelation` usa Fubini e integrabilidade da correlação para
provar ∫dt∫dx⟨g(x),f(x−t)⟩=⟨∫g,∫f⟩ para f,g integráveis.
`UnitIntervalShiftProjection` identifica Q com
P_I (∫_{−2}^{2} S_t dt) P_I. A janela contém todas as diferenças de pontos
de I; fora dela o pareamento recortado é zero. As integrais de operadores
são fortes em vetores, sem hipótese de continuidade em norma de B(H).
Disso resulta QB=BQ para B∈F.

`ConstantFibreCandidate` define C=e*Be e busca registrar Be=eC e e*B=Ce*.
Isso ainda não afirma B=fibre(C), nem C∈M.

Passagem posterior sugerida, ainda a provar:

1. Definir A=B−fibre(C). A comuta com recortes e translações. Mostrar e*A=0
   por e*B=Ce* e pela comutação de C com a integral vetorial no intervalo.
2. De e* P_S A=e*A P_S=0 para todo conjunto mensurável S, obter
   ∫_S P_I(Af)=0. Usar a unicidade ae por todos os integrais de conjuntos
   finitos (`Lp.ae_eq_zero_of_forall_setIntegral_eq_zero`), não avaliação
   pontual de L² ou um conjunto excepcional comum a vetores arbitrários.
   Isso deve dar P_I A=0 como identidade de operadores.
3. Transportar por S_n, n inteiro. A comutação faz A desaparecer em cada
   intervalo I+n. A cobertura contável de ℝ permite concluir A=0; a
   escolha de n em função de x só é feita após obter a propriedade ae
   simultânea para a família contável de inteiros. Uma opção é trabalhar
   com x+n∈I e n=1−ceil(x).
4. Só então identificar B=fibre(C). Separar a obrigação C∈M: construir
   os operadores do comutante regular de fibra variável dados por
   x↦Δ^{ix} C' Δ^{−ix}, C'∈M′. Sua comutação com B deve, por continuidade
   e avaliação da igualdade contínua em x=0, dar [C,C']=0. O bicomutante
   da base conclui C∈M. Essa construção ainda não está implementada.

A etapa completa não pode receber o estatuto F=base antes dos itens 3 e 4.
O traço canônico e o gate composto continuam obrigações posteriores.
