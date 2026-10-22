# Continuação 048 — mapa das hipóteses geométricas

Data UTC: 2026-09-07T01:27:55.958665+00:00

## A dívida dinâmica

[REAL — fontes já existentes, sujeitas aos pins de cada entrega] SummableGravityBridge.lean separa amplitude_heat_matching de amplitude_area_matching_iff_ricci. O primeiro fornece o casamento quadrático de calor; o segundo identifica o casamento de área ainda exigido com eta Ric(d,d)=2 pi T(d,d). O teorema de reconstrução transporta essa obrigação, não a produz.

[OPEN] É preciso selecionar a mesma geometria a partir do estado localizado e obter o casamento infinitesimal em cada ponto/direção nula, com uma fonte admissível e conservada. Inserir area_matching como campo de um contrato ou escolher a+c para satisfazê-lo não remove essa hipótese. PlaneWaveEntropyMatching.lean já constrói a família ajustada. A043 constrói congruência/tela sem impor o casamento; a044 dá um boost explícito cuja simetria métrica tem condições; a045 mostra que invariância de forma não fixa sua escala.

## Por que os controles048

[DERIVED — a verificar em Lean] Uma troca de representação por isometria unitária transporta também a obstrução de Borchers. A expressão “outra representação” precisa dizer o que muda: o fluxo027 conjugado de outro perfil-produto continua dentro da classe obstruída, mesmo que o perfil seja aperiódico.

[DERIVED — a verificar em Lean] Se uma associação de regiões/rótulos a conjuntos de operadores distingue rótulos e é covariante, um período do fluxo algébrico tem de voltar ao mesmo rótulo. A dilatação central044 não retorna a r=1 num tempo não nulo para taxa não nula. Logo a referência modular periódica não pode realizar essa localização fiel exata. Não se supõe que toda rede seja injetiva; o negativo enuncia a propriedade de separação necessária.

Esses controles restringem tentativas específicas. Não impedem uma álgebra de wedge fixada pelo boost, não excluem reconstrução modular em outras representações e não demonstram uma impossibilidade geral de gravitação.

## Próximas construções possíveis, ainda não realizadas

[OPEN] Uma rede com regiões físicas, ação geométrica efetiva, estado e variações admissíveis, além de uma lei dinâmica microscópica independente do casamento visado. Precisará passar os controles espectrais/temporais048; a mera mudança unitária do perfil produto não basta se a proposta exige a relação de Borchers.

[DERIVED — proposta analítica não formalizada nesta entrega] No fecho real das tangentes centradas de sítios de um perfil estacionário, invariância sob todas as permutações finitas e continuidade podem selecionar a forma bilinear até uma escala. As entradas fora da diagonal teriam de ser zero porque a norma quadrática de somas de N tangentes cresce como N enquanto um coeficiente cruzado constante não nulo produziria crescimento N². Isso exigiria construir a ação sobre o subespaço e provar a densidade; não confundir essa proposta com um resultado compilado048, nem com a seleção de uma tela física ou da constante eta.

[KNOWN] Jacobson (1995) deriva a equação de Einstein sob proporcionalidade entre entropia e área e Clausius em todos os horizontes locais de Rindler. É uma referência para o tipo de hipótese a fornecer, não um preenchimento automático da dívida da torre.
Fonte: https://arxiv.org/abs/gr-qc/9504004

[KNOWN] Jacobson (2016) relaciona equilíbrio do entrelaçamento a volume fixo com Einstein para variações de primeira ordem de campos conformes no vácuo local; campos não conformes exigem hipótese adicional na análise do artigo.
Fonte: https://arxiv.org/abs/1505.04753

[POSTULATE — se adotado] Exigir tal equilíbrio para uma construção nova seria uma lei física adicional até ser derivada de outra dinâmica explicitada. A presente entrega não a adota por definição, não chama cosmologia de prova e não muda o gate.

## Custódia

O índice vivo e a árvore canônica são mapas históricos; as entregas046/047 da bancada já ultrapassam a folha antiga que ainda chama a expectativa aperiódica de OPEN. Não editar esses documentos nesta bancada: o túnel comunica a atualização ao responsável pela integração. O Atlas e os arquivos originais permanecem somente leitura.
