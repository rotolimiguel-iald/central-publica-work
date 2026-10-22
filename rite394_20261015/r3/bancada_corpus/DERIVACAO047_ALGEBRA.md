# Derivação047 — álgebra da esperança no fator

[INPUT] Continuação autorizada da construção046. Esta derivação precede o novo fonte ExpectationAlgebra.lean. As fontes046, memórias, Atlas e acervo canônico permanecem somente leitura. O escopo é todo P : SiteProfile desta torre binária e qualquer I : ExpectationInput P.

[REAL — leitura das APIs] O contrato contém apenas E, into, fixes e ortho. A construção046 fornece um habitante e limite forte das médias, com cota de norma. TheOathOnTheTower fornece omega_definite e unicidade entre contratos. CentralizerDensity fornece fechamento do centralizador por zero, unidade, soma, escalares e produto; seu override035 com instâncias nomeadas será selecionado pela infraestrutura limpa.

[DERIVED — prova planejada] Denote M = theFactorObject P, N = omegaCentralizer P e ω = omegaState P. Para A∈M e C∈N, se ω(B*(A−C))=0 para todo B∈N, então I.E A=C. De fato D=I.E A−C pertence a N; as duas ortogonalidades testadas em D implicam ω(D*D)=0; a definitude no fator implica D=0. Esta é unicidade pontual da imagem, sem inserir a conclusão como hipótese de um novo contrato.

As imagens candidatas I.E A+I.E B e c I.E A pertencem a N e satisfazem a ortogonalidade por linearidade de ω. O mesmo argumento paga diferenças. Zero e unidade seguem de fixes. A ortogonalidade com B=1 dá ω(I.E A)=ω(A).

A identidade ω(A*)=conj(ω(A)) vem diretamente do adjunto e da simetria conjugada do produto interno. Para A∈N, aplicar a ciclicidade de A a B* e conjugar dá a ciclicidade de A*, logo N é fechado por estrela. Para a estrela da esperança, a ortogonalidade testada em B* dá ω(B(A−I.E A))=0. A ciclicidade de B permite mover B à direita; conjugar produz ω(B*(A*−(I.E A)*))=0. A unicidade pontual identifica a imagem.

Para C,D∈N, a ortogonalidade de CA com candidato C I.E A vem de testar A em C*B. Para AD e candidato (I.E A)D, a ciclicidade de D move o fator direito à esquerda, e o teste apropriado é BD*. Compor as duas identidades dá a bimodularidade I.E(CAD)=C(I.E A)D. Não se presume que elementos do centralizador comutem com A.

A restrição a M é um mapa linear complexo. O domínio empacotado será o subtipo (theFactorObject P).toStarSubalgebra, que tem as instâncias escalares e normadas herdadas. O conjunto de operadores é exatamente M. A igualdade com aperiodicExpectationInput, pela unicidade já provada, transporta a cota046 para qualquer I. Só então se empacota um mapa linear contínuo com norma ≤1. A linearidade nunca é alegada para valores arbitrários fora de M.

[OPEN nesta derivação] Positividade, amplificações finitas e continuidade de redes estão em outros módulos047. Normalidade e o record CStarMatrix de CP exigem suas pontes próprias. Nada aqui identifica horizonte físico, área, calor, H3 ou gravidade quântica geral, nem muda o gate. Antes da compilação os enunciados propostos são DERIVED; eventual verificação Lean será registrada separadamente.
