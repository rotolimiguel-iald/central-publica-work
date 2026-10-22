# Ponte da seleção à geometria — resultado da bancada

[REAL — Lean compilado] 17 teoremas e 10 outras declarações, 27 relatórios de axiomas no conjunto permitido; duas invocações do Lean com saída zero e sem mensagens extras. [Fonte](C:/IALD/Central de Patentes/Chatgpt/SELECAO_GEOMETRIA_20260909_110405_1043089/SelectedAmplitudeGeometry.lean); [compilação](C:/IALD/Central de Patentes/Chatgpt/SELECAO_GEOMETRIA_20260909_110405_1043089/BUILD_20260909_111235_577496/BUILD_RESULT.json). SHA-256 da fonte calculado: 5ef5f3c97387d68d7dee55ed5bee26ac4035b27f127b9ebdd8383354ca8f0b8c.

## O que foi construído

A leitura do observável siteMark no MESMO Hilbert de referência retorna p_n=1/3−b_n r(t), r(t)=t²/(1+t²). O ângulo da seleção satisfaz sin²θ_n=p_n. Para t conhecido e não zero, a fórmula explícita recupera b_n=(1/3−sin²θ_n)/r(t).

AngularAmplitudeRecord contém os ângulos, o parâmetro de preparação e as condições de admissibilidade dessa amplitude: não negativa, limitada por sítio e somável. Não contém Einstein, campo geométrico, Clausius ou hipótese de casamento. decodeAmplitude constrói o objeto SummableAmplitude; encodeAmplitude produz registros admissíveis da família existente.

O kernel novo demonstra ida e volta para toda amplitude codificada e demonstra que TODO registro admissível se realiza no nível das probabilidades do estado construído. Não promete recuperar o representante angular original a partir de sin², que é periódico.

A massa recuperada é o limite dos prefixos da sequência decodificada. Essa massa alimenta a matéria do modelo: amplitudeCoupling=ln(2)·M/π. Com eta e cisalhamento explícitos, são construídos selectedWaveSolder, selectedWaveInverse e selectedWaveMatter. O casamento de área é aplicado e exportado; dele se obtém a equação de Einstein existente. O teorema de Einstein do módulo não recebe area_matching como hipótese: usa o habitante construído dessa família.

Mesma massa lida e mesmo cisalhamento implicam a mesma solda. O contraste com cisalhamento distinto preserva o registro de amplitudes e distingue uma componente da curvatura no referencial fixado.

## Critério geral de suficiência, com escopo exato

Para read:S→R e geom:S→G, existe decodificador na imagem de read com D(read x)=geom x se e somente se read x=read y implica geom x=geom y. O decodificador é único na imagem.

Essa condição exige apenas que a geometria seja constante nas fibras do registro; não exige recuperar todo o estado. O teorema permite também escolher G como classe de equivalência geométrica, desde que essa classe seja definida. A direção de existência usa escolha clássica: não garante algoritmo, continuidade, estabilidade ou realização instrumental.

## Hipóteses preservadas e fronteira

- As leituras p_n são expectativas/probabilidades, não resultados individuais Bernoulli.
- É usada a sequência completa de leituras exatas. Prefixos convergem; não foi derivada uma taxa universal nem substituída a sequência por um escalar de precisão finita.
- t é o parâmetro de preparação conhecido. Não foi identificado com o tempo modular, que preserva o estado fixo.
- Eta, cisalhamento e carta/referencial continuam dados adicionais.
- A geometria aplicada é a família de ondas planas já construída. O critério de suficiência vale em geral, mas esta aplicação não constitui um construtor geral de geometria/área.
- O controle distingue componentes de curvatura na carta fixada; não declara classificação por isometria.

## Revisão e rastreabilidade

Uma revisão adversarial independente das fontes não encontrou hipótese gravitacional oculta ou troca de Hilbert. Sua sugestão de provar a realização inversa das probabilidades foi incorporada e compilada. A primeira tentativa com eliminação dependente falhou e foi preservada; a tentativa intermediária válida e a extensão final também permanecem em diretórios separados. Há backups imediatos dos bytes antes das alterações.

Dependências diretas foram conferidas por hash antes e depois; não houve reconstrução ou auditoria de todas as dependências transitivas. Esta sessão não executou nem importou o um.py original e não escreveu no kernel canônico. Nenhum gate foi alterado.

O objetivo de reconstrução gravitacional GERAL permanece ativo: o próximo requisito é uma lei de geometria/área que satisfaça o critério de descida para os dados TGL e tenha aplicação além da família de ondas construída.


## Adendo de precisão — ângulos de sítio

Os ângulos reconstruídos neste módulo são os das probabilidades de sítio da família amplitudeProfile. A fórmula selectionAngle é a mesma função usada no novo kernel, mas seus argumentos aqui são essas probabilidades. O módulo não identifica cada ângulo de sítio com o ângulo canônico de Miguel em beta_TGL. Essa identificação adicional não foi usada como hipótese nem como conclusão.

O manifesto inicial preserva o hash da primeira emissão do relatório. Este adendo foi acrescentado com backup imediato dos bytes; a emissão final será referenciada pelo manifesto conjunto do lote.
