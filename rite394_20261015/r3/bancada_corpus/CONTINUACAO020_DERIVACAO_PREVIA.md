[DERIVED / INPUT / OPEN] CONTINUAÇÃO 020 — área quadrática, calor construído e condição de Clausius

06/09/2026. Derivação anterior ao código Lean. O turno 019 foi progresso: seu auditor acaba de reconferir 588 hashes, sete módulos limpos, 38 teoremas e uma definição impressa. Permanecem somente as ordens gerenciais 001–007. O objetivo amplo continua ativo e não alcançado.

## Alvo

Partir dos dados geométricos de equilíbrio construídos em 019. Provar o limite quadrático da área da tela, construir uma primitiva do fluxo estipulado de energia-momento e calcular o coeficiente do resíduo de Clausius. Habitar GeometricHorizonPencil sob a hipótese termodinâmica explicitamente nomeada e obter a implicação geral de Einstein com a geometria já construída, sem receber o lápis inteiro como INPUT.

## Derivação

1. Seja P:EquilibriumScreenData, θ(t) sua expansão, A(t) a área normalizada e M(t)=T(curve(t))(V,V). O resultado 019 dá θ(0)=0, A(0)=1 e θ′(0)=−r, onde r=Ric_p(v,v). A área é contínua em zero e satisfaz A′=θA eventualmente à esquerda. O lema primitive_quadratic_limit deve então dar
   lim_{t→0−}(A(t)−1)/t²=−r/2.

2. Sob diferenciabilidade de T, M é contínua em zero e eventualmente contínua nos tempos negativos próximos. A curva permanece no aberto do campo nesse intervalo. A área também é contínua nesses tempos, por sua derivada já provada. Logo f(t)=−κ t M(t)A(t) tem essa continuidade e f(0)=0.

3. Construir uma extensão contínua global de f que coincida com f perto de zero pelo lado negativo. Escolher um intervalo fechado [a,0] com a<0 onde f é contínua e usar a função de truncamento max(a,min(t,0)). Definir Q(t)=∫₀ᵗ f_ext(s)ds. Pelo teorema fundamental do cálculo, Q é contínua, Q(0)=0 e Q′=f nos tempos negativos próximos de zero. A extensão não altera o germe à esquerda.

4. Como f(t)/t→−κ M(0), provar
   lim_{t→0−}Q(t)/t²=−κ M(0)/2.
   Aqui Q é a integral matemática do fluxo postulado a partir de T. Identificá-la com calor físico ou energia modular permanece INPUT/OPEN.

5. Para o resíduo B(t)=Q(t)−κη/(2π)(A(t)−1), provar
   lim_{t→0−}B(t)/t²=κ/2·[η r/(2π)−M(0)].
   Se κ≠0 e η≠0, a condição de Clausius de segunda ordem B(t)=o(t²) equivale a r=(2π/η)T_p(v,v). Essa equivalência NÃO autoriza assumir Clausius provado. Ela impede esconder a equação pretendida dentro de uma condição aceita sem justificativa.

6. Construir GeometricHorizonPencil a partir de P e Q, recebendo somente a condição de Clausius restante, além dos parâmetros não nulos. Reunir os lápis construídos para cada p e v nulo, T simétrico/conservado e aberto conexo para aplicar a reconstrução já existente:
   G+Λg=(2π/η)T.
   Toda hipótese física deve continuar no enunciado final.

## Controles e limites

Controlar sinais e fatores 1/2 com exemplos planos explícitos, inclusive um fluxo de matéria cujo resíduo NÃO zera. A geometria e a existência da primitiva não devem fabricar Clausius. Se couber, mostrar a independência do coeficiente em relação à extensão contínua escolhida.

A integração acima é temporal e trata a área da tela ao longo de uma curva. Não constrói uma hipersuperfície nula imersa nem uma integral espacial de área sobre horizonte. Permanecem abertas a ponte região–álgebra, entropia–área microscópica, unidade e coeficiente físicos, identificação do calor com energia modular, justificação microscópica de Clausius/H3, origem modular da solda e globalização.

Escritas apenas em Chatgpt; originais, um.py, kernel canônico, Atlas, memórias, selos e gate intocados. Revisões com backup de bytes e tentativas falhas preservadas. Auditoria independente da gerência separada.
