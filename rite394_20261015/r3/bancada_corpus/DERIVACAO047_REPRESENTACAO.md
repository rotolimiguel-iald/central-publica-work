# Derivação047 — representação dos blocos em Hilbert

[INPUT] Módulo novo OperatorBlockRepresentation.lean, genérico em um Hilbert complexo completo H e k natural, inclusive k=0. Esta derivação é anterior ao código. Todos os originais e selos permanecem somente leitura.

[REAL — leitura das APIs Mathlib] CStarMatrix é uma cópia de Matrix com a norma C*-algébrica; a operação toCLM da biblioteca age por multiplicação à direita em um módulo C*, com codomínio algébrico oposto. Não é a representação Hilbert desejada. PiLp.continuousLinearEquiv, PiLp.proj e ContinuousLinearMap.single fornecem inclusões e projeções contínuas da soma finita. PiLp.inner_apply identifica o produto interno com a soma das entradas. StarAlgEquiv e map_nonneg permitem transportar positividade nos dois sentidos entre C*-álgebras.

[DERIVED — construção] Definir ρ(M)v por (ρ(M)v)i=Σj Mij(vj), onde o espaço vetorial é PiLp 2 (fun _:Fin k=>H). A aplicação é contínua como soma finita de composições de operadores contínuos, sem pressupor uma estimativa ótima de norma. Recuperar cada entrada de T por proj_i ∘ T ∘ single_j. Testar em single_j(v) prova que a recuperação de ρ(M) devolve M; decompor qualquer vetor como Σj single_j(vj) prova que ρ da matriz recuperada devolve T.

A distributividade e a troca de somas finitas mostram ρ(MN)=ρ(M)ρ(N). A identidade do adjunto decorre de Σi,j⟨wi,(Mji)*vj⟩=Σj,i⟨Mji wi,vj⟩. Portanto ρ é uma equivalência de álgebras estreladas, não apenas uma aplicação injetiva.

A positividade C*-algébrica de M equivale à de ρ(M), porque a equivalência e sua inversa preservam positivos. Pela caracterização de operadores positivos no Hilbert, isso equivale exatamente a:
(1) star(Mij)=Mji para todas as entradas;
(2) Re Σi,j⟨vi,Mij vj⟩≥0 para todo v:Fin k→H.
São as condições do módulo independente ExpectationBlockPositive. Essa ponte permite transportar o teorema de preservação de todas as formas de blocos para a ordem CStarMatrix.

[OPEN antes da compilação] Os resultados propostos ainda requerem elaboração e verificação Lean. Empacotar a aplicação concreta do fator como CompletelyPositiveMap requer também instâncias C*-algébricas corretas do domínio e o teorema de blocos do colega; não se insere CP como hipótese. Nenhuma consequência física, H3 ou QG geral é afirmada.
