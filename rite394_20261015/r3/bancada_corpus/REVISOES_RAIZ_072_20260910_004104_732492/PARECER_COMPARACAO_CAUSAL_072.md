# Parecer da raiz — comparação causal e Ward em referência fixa

10/09/2026. [DERIVED — revisão analítica interna das demonstrações escritas] [KNOWN — importação delimitada] [REAL — pins medidos]. Nenhuma execução/importação de um.py, compilação Lean ou cálculo CAS. Esta revisão é da frente causal072, escrita por outra frente, e não se apresenta como aprovação externa.

**Conclusão: favorável no alcance enunciado.** Foram lidas integralmente as notas de admissibilidade e de transporte/Ward. O reparo do CCR é infinitesimal; a Ward construída é anômala e conserva a referência B0. Não há nesta nota demonstração da remoção geral da anomalia, da QME ou de independência física de fundo.

## Conferência das identidades

1. Na derivada de mu exp(hbar Gamma_H), os operadores de contração com kernels independentes dos campos comutam. A regra do produto produz exatamente o termo adicional hbar mu exp(hbar Gamma_H) Gamma_dotH. Nos observáveis lineares a parte antissimétrica é i hbar dotE. Uma mudança de Wick simétrica fixa esses observáveis e, portanto, não corrige o CCR variável. Trata-se da falha de uma identificação específica, não de uma prova de anomalia física não removível.

2. A diferenciação dos Green com as condições causais dá dotG=-G dotP G. Com E=Gret-Gadv, a expansão de -Gret dotP E-E dotP Gadv cancela os dois termos mistos e reproduz dotE. A adjunção é tomada no par dual previamente identificado, de modo que r*=1-epsilon dotP Gadv. A expansão de r E r* confere com E_epsilon na primeira ordem.

3. O controle escalar usa o modo espacial constante em R x S3. Entre dois tempos separados por menos de pi/m, os dois senos da integral são positivos no suporte de chi. Seu sinal negativo fornece um pareamento não nulo para testes próximos. Esse exemplo controla a variação do propagador; não foi apresentado como diagrama Einstein–sigma.

4. A antissimetrização de w=dotH+Gret dotP H+H dotP Gadv é i vezes dotE+Gret dotP E+E dotP Gadv, que se anula. A nota corretamente exige uma comparação Hadamard compatível para afirmar suavidade. Simetria sozinha não basta. O suporte ampliado de r*f também é conservado como limitação, sem aplicar diretamente a r o requisito de derivação local de inserções.

## Conferência da extensão com fontes

Na referência B0 fixa, d_theta não deriva os propagadores e comuta graduadamente com o diferencial livre, pois atua em fatores distintos. Isso prova D0 ao quadrado igual a zero e a regra graduada de Leibniz. A extensão multilinear dos produtos por coeficientes externos suaves é válida coeficiente a coeficiente; ação por partes inclui as derivadas desses coeficientes. A identidade (13) segue da mesma regra e não constitui uma hipótese de remoção de anomalia.

O domínio exclui os antifields externos theta*, omega*. A parte forte linear theta* omega serve para extrair a CME reduzida. A transformação de gauge mantém o termo omega delta_theta Psi. Separar Sigma0,B0 fornece M(Vext)=0 na região de cutoffs constantes, com s0 clássico distinto de s-hat0. Conservar os termos lineares ao variar fundos arbitrários evita pressupor que o novo fundo continua on-shell.

A filtração explicitada controla tadpoles e alterações quadráticas por grau externo, e os demais vértices por peso perturbativo, laços e truncagem. Deve ser usada como filtração combinada, com parte Laurent negativa finita por grau externo; não é licença para somar uma série não filtrada em t ou ignorar os termos dependentes dos campos. Constantes centrais e seus fatores na matriz relativa foram separados no enunciado.

A Ward original aplicada aos coeficientes e somada à identidade exata de d_theta dá (16), com a mesma normalização i/hbar. As inserções marcadas são obtidas por polarização. A consistência de primeira ordem não removida é (19); ela declara fechamento modulo d, não exatidão. A projeção theta=omega=0 recupera a identidade de B0. Esses passos constroem um levantamento em uma álgebra fixa, não a equivalência de toda família de produtos com operadores livres variáveis.

## Importação e fronteira

Conferi diretamente o Teorema 3 e a equação (154) de [Fröb, 1803.10235v3](https://arxiv.org/pdf/1803.10235). O primeiro exige uma derivação local e covariante da álgebra livre; a segunda conserva expressamente a anomalia na identidade BV. A construção de referência satisfaz a parte relativa às fontes sem postular a ausência da anomalia. A aplicação ao multiplet e aos contatos ainda consome o dicionário e a construção Q2_069 explicitados pela fonte.

A retração age nos doublets adicionados e não na referência B0 dos kernels. A primitiva necessária vive, portanto, na classe admissível com os espectadores ainda presentes, salvo uma prova adicional que elimine sua dependência. O resultado H1,4 de071 para outra classe não foi usado por homonímia. A normalização de acordo perturbativo, sua compatibilidade de gauge, os contatos, a QME, a representação física e UV permanecem obrigações.

Não encontrei erro material nas identidades conferidas. A aprovação é restrita às demonstrações acima e às hipóteses analíticas já identificadas. Não implica uma nova auditoria completa das fontes 067–071 ou compilação de qualquer prova.
