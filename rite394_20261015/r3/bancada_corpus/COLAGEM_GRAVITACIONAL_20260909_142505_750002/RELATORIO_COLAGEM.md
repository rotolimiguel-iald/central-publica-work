# Colagem das equações reconstruídas em cartas

09/09/2026. [REAL — compilado no alcance descrito]

Foram demonstrados dois módulos: `GravitationalChartGluing` (10 teoremas e 3 definições/estruturas) e `TopologicalAtlasGluing` (2 teoremas). Os recibos PASS são, respectivamente, `BUILD_20260909_142955_219489/BUILD_RESULT.json` e `BUILD_20260909_143207_265589/BUILD_RESULT.json`. Cada folha tem duas execuções com código zero, auditorias de todas as declarações e somente os axiomas padrão `propext`, `Classical.choice`, `Quot.sound`.

## Resultado

Cada carta recebe um `GravitationalResponseRecord` e as hipóteses físicas da preparação unificada de 48 resultados: conservação total, telas, lei de área e coeficiente comum eta diferente de zero. O teorema local de Einstein já demonstrado produz uma constante cosmológica por carta. Nenhuma equação de Einstein foi colocada como campo da estrutura `AreaChart`.

Numa sobreposição, o transporte dos três tensores por uma mesma matriz inversível é explícito: g, T e o tensor geométrico de Einstein. O transporte da equação é derivado por álgebra matricial. Como a métrica Lorentziana é não nula, duas constantes que satisfazem a equação nesse ponto são iguais.

Uma cadeia finita de encontros propaga essa igualdade. O segundo módulo deriva a existência dessas cadeias a partir de uma cobertura aberta de um espaço topológico preconexo, com cartas não vazias e homeomorfismos entre seus domínios. Não recebe a conectividade do grafo como hipótese adicional. Conclui uma única constante cosmológica para as equações em todas as cartas da cobertura.

## Hipóteses preservadas

- Lei de área, conservação total, telas e assinatura continuam explicitadas nos dados locais.
- A transformação do tensor geométrico de Einstein é uma obrigação de naturalidade expressa em `RecordOverlap` e `hmatch`. O trabalho paralelo de naturalidade infinitesimal do Ricci não deve ser apresentado automaticamente como prova dessa lei para toda transição finita.
- As matrizes de transformação são testemunhas de compatibilidade tensorial. Esta entrega não as identifica com os Jacobianos dos homeomorfismos, nem constrói suas condições de cociclo em encontros triplos.
- O resultado cola as equações e a constante cosmológica. A existência de um campo geométrico global com as transições físicas pretendidas precisa dessas ligações adicionais.
- O índice de cartas é arbitrário. A cobertura pode ser infinita. Cartas vazias foram excluídas na aplicação topológica; isso também fornece o ponto necessário para a unicidade da constante.

## Prova topológica

Separam-se a união das cartas alcançáveis a partir de uma carta escolhida e a união das demais. Ambas são abertas. Um encontro entre elas produziria uma cadeia, portanto são disjuntas. Elas cobrem o espaço. A primeira é não vazia. A preconexidade força a segunda a ser vazia; todo índice de carta não vazia é alcançável.

## Verificação e preservação

O primeiro build do módulo algébrico falhou porque a API de `Matrix.det_zero` exigiu uma prova explícita de que `Fin 4` é não vazio. A correção forneceu essa instância sem modificar enunciados. O build com falha e o backup imediato de bytes foram preservados. Os únicos recibos aprovados são os dois citados acima.

As folhas usam dependências locais anteriormente aprovadas, copiadas byte a byte, e bibliotecas canônicas existentes. Os imports diretos e a fronteira local de cache foram conferidos por hash antes/depois. Não houve recompilação integral de todas as dependências transitivas.

Nenhum `um.py` foi executado ou importado. Nenhum original, Atlas, gate ou selo foi modificado. Todo o trabalho está nesta nova pasta em Chatgpt. A revisão semântica independente será registrada em adendo próprio.
