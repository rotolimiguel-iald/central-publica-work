# Dedução prévia — Clausius e Einstein a partir da métrica

[DERIVED — verificar em Lean] Usar o campo g e sua inversa construída, sem E/D independentes. Para cada ponto e direção nula não nula, receber uma realização EquilibriumScreenData: a escolha da tela não contém balanço de Ricci nem Einstein.

O kernel prova que o calor construído pela integral do fluxo e a área induzida têm um resíduo de Clausius cujo coeficiente quadrático é rate/2*(eta Ric(d,d)/(2pi)-T(d,d)). Com rate e eta não nulos, o resíduo dividido por t² tende a zero se, e somente se, vale o balanço nulo de Ricci. Para duas telas normalizadas do mesmo ponto/direção, o critério é o mesmo.

Pelo teorema métrico geral já compilado, conservação de T e esse balanço produzem G+Lambda g=(2pi/eta)T, com Lambda constante no aberto pré-conexo. Alternativamente, as duas correspondências microscópicas de calor e área da família unitária já disponível produzem Clausius; elas podem entrar como leis de correspondência explícitas.

[INPUT] g suave lorentziana; T simétrico/diferenciável/conservado; telas de equilíbrio; correspondências calor/área ou Clausius a segunda ordem. Não postular igualdade finita exata: o kernel tem controle quartico que a refuta em famílias curvas. Não dizer que retipar essas correspondências deriva sua validade física.

[OPEN] Codec dos dados selecionados e existência/regularidade das telas para o g decodificado serão articulados separadamente. O objetivo é reduzir a interface até que as hipóteses físicas remanescentes fiquem identificadas, não escondê-las.
