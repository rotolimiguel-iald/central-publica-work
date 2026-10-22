# Derivação prévia — um registro e uma preparação

[INPUT] GravitationalResponseRecord armazena probabilidades do codec métrico e dez coeficientes de resposta, com regularidade e assinatura explicitamente certificadas. Ele já reconstrói g e T e prepara a fonte em uma curva conjunta finita; não afirma uma origem física dos registros.

A nova composição coloca os 32 pesos recordState do bloco métrico junto aos 16 pesos da preparação calibrada. A soma disjunta tem 48 resultados. Cada bloco tem massa 1/2, e a dinâmica é avaliada em √2t. O suplemento unitário fornece U=I⊕U_dyn(√2t), amplitude normalizada, e a igualdade entre sua leitura diagonal e essa distribuição, preservada a permutação dos índices internos.

A leitura do bloco estático multiplicada por 2 retorna recordState; o decoder angular retorna g. Os coeficientes entrópicos e modulares da curva de 48 resultados são os mesmos da preparação fonte. Dez coeficientes entrópicos efetivamente atestados por limites nas direções de prova deverão ser identificados pela unicidade do limite, recuperando os dez números declarados e T.

Para a área, a diferença entre erros das duas curvas é a diferença entre os incrementos entrópicos; a parcela de área cancela. Ambas têm o mesmo coeficiente quadrático. Logo o quociente dessa diferença tende a zero, e o matching de área de uma curva equivale ao da outra. Isso permite transportar a suficiência condicional de Einstein para a curva unificada, mantendo a lei de área e a conservação total como INPUT.

[OPEN] Esta é uma realização representacional a partir de registro fornecido, não prova de que uma seleção física necessariamente produz esses dados. Não reconstrói T da base inicial sozinha, não globaliza cartas/assinatura, não constrói uma conexão com torção e não preserva custo/entropia absoluta. A entropia é diagonal da leitura, não a de von Neumann do projetor puro.
